#!/usr/bin/env python3
"""Validate report data and embed it safely in the static report template."""

from __future__ import annotations

import argparse
import ast
import base64
import binascii
import json
import math
import os
import re
import secrets
import stat
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse


SCHEMA_VERSION = "3.0.0"
START_MARKER = "<!-- REPORT_DATA_START -->"
END_MARKER = "<!-- REPORT_DATA_END -->"
TOKEN_MARKER = "/*__REPORT_DATA__*/"
DATA_SCRIPT_ID = "findings-report-data"
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", flags=re.DOTALL)
REPORT_DATA_SCRIPT_RE = re.compile(
    r"(<script\b(?=[^>]*\bid\s*=\s*['\"]"
    + re.escape(DATA_SCRIPT_ID)
    + r"['\"])(?=[^>]*\btype\s*=\s*['\"]application/json['\"])[^>]*>)"
    r"(.*?)"
    r"(</script\s*>)",
    flags=re.IGNORECASE | re.DOTALL,
)
DEFAULT_SCHEMA_PATH = (
    Path(__file__).resolve().parent.parent / "references" / "report-data.schema.json"
)

FINDING_ID_RE = re.compile(r"^F-[A-Za-z0-9][A-Za-z0-9._-]*$")
SOURCE_ID_RE = re.compile(r"^SRC-[A-Za-z0-9][A-Za-z0-9._-]*$")
EVIDENCE_ID_RE = re.compile(r"^EV-[A-Za-z0-9][A-Za-z0-9._-]*$")
UNIFIED_HUNK_RE = re.compile(
    r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(?: .*)?$", re.MULTILINE
)
RFC3339_DATETIME_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[Zz]|[+-]\d{2}:\d{2})$"
)
RFC3339_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SURROGATE_RE = re.compile("[\ud800-\udfff]")
URI_RE = re.compile(
    r"^[A-Za-z][A-Za-z0-9+.-]*:"
    r"(?:[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=-]|%[0-9A-Fa-f]{2})*$"
)
DIFF_METADATA_RE = re.compile(
    r"^(?:index |old mode |new mode |deleted file mode |new file mode |"
    r"copy from |copy to |rename from |rename to |similarity index |dissimilarity index )"
)

SEVERITIES = {"critical", "high", "medium", "low", "informational"}
CONFIDENCES = {"confirmed", "high", "medium", "low"}
REPORT_STATUSES = {"draft", "final"}
RISK_LEVELS = SEVERITIES
LIKELIHOOD_LEVELS = {"high", "medium", "low"}
IMPACT_LEVELS = {"critical", "high", "medium", "low"}
LINE_STATES = {"source", "vulnerable", "validation", "sink"}
ANNOTATION_TYPES = LINE_STATES | {"note"}

SUPPORTED_SCHEMA_KEYWORDS = {
    "$defs",
    "$id",
    "$ref",
    "$schema",
    "additionalProperties",
    "const",
    "dependentRequired",
    "description",
    "enum",
    "format",
    "items",
    "maxItems",
    "maxLength",
    "maximum",
    "minItems",
    "minLength",
    "minProperties",
    "minimum",
    "pattern",
    "properties",
    "required",
    "title",
    "type",
    "uniqueItems",
}
SUPPORTED_SCHEMA_TYPES = {
    "array",
    "boolean",
    "integer",
    "null",
    "number",
    "object",
    "string",
}
SUPPORTED_SCHEMA_FORMATS = {"date", "date-time", "uri"}

# These are finding-lifecycle or delivery-tracking fields, not report content.
# Normalization makes due_date, due-date, and dueDate equivalent.
DISALLOWED_KEYS = {
    "assignee",
    "duedate",
    "effort",
    "fixed",
    "fixedat",
    "fixversion",
    "generatedby",
    "implemented",
    "implementedat",
    "isfixed",
    "issue",
    "notfixed",
    "notremediated",
    "owner",
    "ownership",
    "patchstatus",
    "priority",
    "remediated",
    "remediatedat",
    "remediationstatus",
    "resolution",
    "resolved",
    "resolvedat",
    "retest",
    "retestedat",
    "retestresult",
    "reteststatus",
    "ticket",
    "verification",
    "verified",
    "verifiedat",
}

# An empty findings array is the explicit, meaningful zero-finding result.
EMPTY_ARRAY_KEYS = {"findings"}

PLACEHOLDER_EXACT = {
    "-",
    "?",
    "changeme",
    "demo",
    "example",
    "fixme",
    "n/a",
    "none provided",
    "not provided",
    "placeholder",
    "sample",
    "tbd",
    "todo",
    "unknown",
}
PLACEHOLDER_RE = re.compile(
    r"(?i)(?:lorem\s+ipsum|replace[_ -]?me|change[_ -]?me|"
    r"\[\s*(?:insert|replace)(?:[^\]]*)\]|"
    r"<\s*(?:insert|replace)(?:[^>]*)>|"
    r"\{\{\s*(?:insert|replace)(?:[^}]*)\}\})"
)
EXPLICIT_FIELD_PLACEHOLDER_RE = re.compile(
    r"(?i)^\s*(?:"
    r"\[(?:client|customer|company|project)(?:[^\]]*)\]|"
    r"<(?:client|customer|company|project)(?:[^>]*)>|"
    r"\{\{(?:client|customer|company|project)(?:[^}]*)\}\}"
    r")\s*$"
)

SECRET_PATTERNS = (
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
    (
        "JWT",
        re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"),
    ),
)
PRIVATE_KEY_HEADER_RE = re.compile(
    r"-----BEGIN (?P<kind>(?:[A-Z0-9 ]+ )?PRIVATE KEY)-----"
)
PRIVATE_KEY_END_RE = re.compile(r"-----END (?:[A-Z0-9 ]+ )?PRIVATE KEY-----")
CREDENTIAL_URL_RE = re.compile(
    r"\b[a-z][a-z0-9+.-]*://(?P<username>[^\s/:@]+):(?P<password>[^\s/@]+)@",
    re.IGNORECASE,
)
AUTH_HEADER_RE = re.compile(
    r"(?im)^\s*(Authorization|Proxy-Authorization)\s*:\s*"
    r"(?:Bearer|Basic)\s+(.+?)\s*$"
)
COOKIE_HEADER_RE = re.compile(r"(?im)^\s*(Cookie|Set-Cookie)\s*:\s*(.+)$")
SECRET_LITERAL_RE = re.compile(
    r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password|passwd)"
    r"\s*[:=]\s*(?P<quote>['\"])(?P<value>[^\r\n]*?)(?P=quote)"
)
SAFE_SECRET_VALUES = {
    "[redacted]",
    "<redacted>",
    "redacted",
    "[masked]",
    "<masked>",
    "masked",
    "***",
}


class DataLoadError(Exception):
    """Input could not be read as a unique-key JSON document."""


class TemplateError(Exception):
    """The template cannot be populated safely."""


class DuplicateKeyError(ValueError):
    pass


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON object key {key!r}")
        result[key] = value
    return result


def _reject_nonfinite_json(value: str) -> Any:
    raise ValueError(f"non-standard JSON number {value!r} is not allowed")


def load_json(path: Path) -> Any:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise DataLoadError(f"cannot read {path}: {exc}") from exc
    try:
        return json.loads(
            text,
            object_pairs_hook=_unique_object,
            parse_constant=_reject_nonfinite_json,
        )
    except (json.JSONDecodeError, DuplicateKeyError, ValueError) as exc:
        raise DataLoadError(f"invalid JSON in {path}: {exc}") from exc


def json_path(parent: str, key: str | int) -> str:
    if isinstance(key, int):
        return f"{parent}[{key}]"
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
        return f"{parent}.{key}"
    return f"{parent}[{json.dumps(key)}]"


def walk(value: Any, path: str = "$") -> Iterable[tuple[str, str | None, Any]]:
    """Yield (path, containing key, value) for every node."""
    yield path, None if path == "$" else path.rsplit(".", 1)[-1], value
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = json_path(path, key)
            yield from walk(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk(child, json_path(path, index))


def normalized_key(key: str) -> str:
    return re.sub(r"[^a-z0-9]", "", key.lower())


def is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def is_redacted(value: str) -> bool:
    normalized = value.strip()
    if len(normalized) >= 2 and normalized[0] == normalized[-1] and normalized[0] in "'\"":
        normalized = normalized[1:-1].strip()
    return normalized.lower() in SAFE_SECRET_VALUES


def is_code_or_patch_path(path: str) -> bool:
    return bool(
        re.search(r"\.lines\[\d+\]\.code$", path)
        or re.search(r"\.patch\.content$", path)
        or re.search(r"\.supportingArtifacts\[\d+\]\.content\.(?:text|content)$", path)
        or re.search(r"\.validation\.demonstration\.text$", path)
    )


def is_source_code_path(path: str) -> bool:
    return bool(re.search(r"\.lines\[\d+\]\.code$", path))


def is_source_path_value(path: str) -> bool:
    return bool(
        re.search(r"\.sourceContexts\[\d+\]\.path$", path)
        or re.search(r"\.patch\.path$", path)
        or re.search(r"\.(?:includedPaths|excludedPaths)\[\d+\]$", path)
        or re.search(r"\.affectedComponents\[\d+\]$", path)
    )


def check_iso_datetime(value: Any) -> bool:
    if not isinstance(value, str) or RFC3339_DATETIME_RE.fullmatch(value) is None:
        return False
    normalized = value[:10] + "T" + value[11:]
    if normalized.endswith(("Z", "z")):
        normalized = normalized[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return False
    return parsed.tzinfo is not None


def check_iso_date(value: Any) -> bool:
    if not isinstance(value, str) or RFC3339_DATE_RE.fullmatch(value) is None:
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def check_absolute_uri(value: Any) -> bool:
    if not isinstance(value, str) or URI_RE.fullmatch(value) is None:
        return False
    try:
        parsed = urlparse(value)
        if not parsed.scheme:
            return False
        if parsed.scheme.lower() in {"http", "https"}:
            if not parsed.netloc or parsed.hostname is None:
                return False
            _ = parsed.port
    except ValueError:
        return False
    return True


CVSS3_METRIC_VALUES = {
    "AV": {"N", "A", "L", "P"},
    "AC": {"L", "H"},
    "PR": {"N", "L", "H"},
    "UI": {"N", "R"},
    "S": {"U", "C"},
    "C": {"N", "L", "H"},
    "I": {"N", "L", "H"},
    "A": {"N", "L", "H"},
    "E": {"X", "U", "P", "F", "H"},
    "RL": {"X", "O", "T", "W", "U"},
    "RC": {"X", "U", "R", "C"},
    "CR": {"X", "L", "M", "H"},
    "IR": {"X", "L", "M", "H"},
    "AR": {"X", "L", "M", "H"},
    "MAV": {"X", "N", "A", "L", "P"},
    "MAC": {"X", "L", "H"},
    "MPR": {"X", "N", "L", "H"},
    "MUI": {"X", "N", "R"},
    "MS": {"X", "U", "C"},
    "MC": {"X", "N", "L", "H"},
    "MI": {"X", "N", "L", "H"},
    "MA": {"X", "N", "L", "H"},
}
CVSS3_REQUIRED_METRICS = {"AV", "AC", "PR", "UI", "S", "C", "I", "A"}


def parse_cvss3_vector(vector: str) -> tuple[str, dict[str, str]] | None:
    parts = vector.split("/")
    if not parts or parts[0] not in {"CVSS:3.0", "CVSS:3.1"}:
        return None
    metrics: dict[str, str] = {}
    for component in parts[1:]:
        if component.count(":") != 1:
            return None
        name, value = component.split(":", 1)
        if name in metrics or name not in CVSS3_METRIC_VALUES:
            return None
        if value not in CVSS3_METRIC_VALUES[name]:
            return None
        metrics[name] = value
    if not CVSS3_REQUIRED_METRICS.issubset(metrics):
        return None
    return parts[0], metrics


def cvss3_base_score(vector: str) -> float | None:
    """Calculate a CVSS 3.0/3.1 base score; return None for malformed vectors."""
    parsed = parse_cvss3_vector(vector)
    if parsed is None:
        return None
    version, metrics = parsed
    weights = {
        "AV": {"N": 0.85, "A": 0.62, "L": 0.55, "P": 0.2},
        "AC": {"L": 0.77, "H": 0.44},
        "UI": {"N": 0.85, "R": 0.62},
        "CIA": {"N": 0.0, "L": 0.22, "H": 0.56},
    }
    scope = metrics["S"]
    if scope not in {"U", "C"}:
        return None
    pr_weights = (
        {"N": 0.85, "L": 0.62, "H": 0.27}
        if scope == "U"
        else {"N": 0.85, "L": 0.68, "H": 0.5}
    )
    try:
        exploitability = (
            8.22
            * weights["AV"][metrics["AV"]]
            * weights["AC"][metrics["AC"]]
            * pr_weights[metrics["PR"]]
            * weights["UI"][metrics["UI"]]
        )
        confidentiality = weights["CIA"][metrics["C"]]
        integrity = weights["CIA"][metrics["I"]]
        availability = weights["CIA"][metrics["A"]]
    except KeyError:
        return None
    impact_subscore = 1 - (1 - confidentiality) * (1 - integrity) * (1 - availability)
    if scope == "U":
        impact = 6.42 * impact_subscore
    elif version == "CVSS:3.1":
        impact = (
            7.52 * (impact_subscore - 0.029)
            - 3.25 * (impact_subscore * 0.9731 - 0.02) ** 13
        )
    else:
        impact = 7.52 * (impact_subscore - 0.029) - 3.25 * (impact_subscore - 0.02) ** 15
    if impact <= 0:
        return 0.0
    raw = min(impact + exploitability, 10) if scope == "U" else min(1.08 * (impact + exploitability), 10)
    return math.ceil((raw - 1e-10) * 10) / 10


def _diff_header_path(line: str, path: str, errors: list[str]) -> str | None:
    raw = line[4:].split("\t", 1)[0].strip()
    if not raw:
        errors.append(f"{path}: diff file header has an empty path")
        return None
    if raw.startswith('"'):
        try:
            decoded = ast.literal_eval(raw)
        except (SyntaxError, ValueError):
            errors.append(f"{path}: diff file header has a malformed quoted path")
            return None
        if not isinstance(decoded, str):
            errors.append(f"{path}: diff file header path must be text")
            return None
        raw = decoded
    if raw == "/dev/null":
        return None
    if raw.startswith(("a/", "b/")):
        raw = raw[2:]
    return raw


def validate_unified_diff(
    content: Any, path: str, errors: list[str], declared_path: Any = None
) -> None:
    if not is_nonempty_string(content):
        errors.append(f"{path}: unified diff content must be a non-empty string")
        return
    assert isinstance(content, str)
    lines = content.splitlines()
    if not lines:
        errors.append(f"{path}: unified diff is empty")
        return
    if not (lines[0].startswith("diff --git ") or lines[0].startswith("--- ")):
        errors.append(f"{path}: unified diff must start with 'diff --git ' or '--- '")
        return

    index = 0
    section_count = 0
    hunk_count = 0
    changed_lines = 0
    candidate_paths: set[str] = set()
    while index < len(lines):
        section_count += 1
        if lines[index].startswith("diff --git "):
            index += 1
            while index < len(lines) and not lines[index].startswith("--- "):
                if lines[index].startswith(("diff --git ", "+++ ", "@@")):
                    errors.append(f"{path}: file section {section_count} is missing ---/+++ headers")
                    return
                if DIFF_METADATA_RE.match(lines[index]) is None:
                    errors.append(
                        f"{path}: unexpected metadata in file section {section_count}: "
                        f"{lines[index]!r}"
                    )
                    return
                index += 1
        if index >= len(lines) or not lines[index].startswith("--- "):
            errors.append(f"{path}: file section {section_count} is missing an --- header")
            return
        old_header = lines[index]
        if index + 1 >= len(lines) or not lines[index + 1].startswith("+++ "):
            errors.append(f"{path}: every --- file header must be followed by a +++ header")
            return
        new_header = lines[index + 1]
        for header in (old_header, new_header):
            candidate = _diff_header_path(header, path, errors)
            if candidate is not None:
                candidate_paths.add(candidate)
        index += 2

        section_hunks = 0
        while index < len(lines):
            if lines[index].startswith("diff --git "):
                break
            if (
                lines[index].startswith("--- ")
                and index + 1 < len(lines)
                and lines[index + 1].startswith("+++ ")
            ):
                break
            match = UNIFIED_HUNK_RE.fullmatch(lines[index])
            if match is None:
                errors.append(
                    f"{path}: unexpected line outside a hunk in file section "
                    f"{section_count}: {lines[index]!r}"
                )
                return
            section_hunks += 1
            hunk_count += 1
            expected_old = int(match.group(2)) if match.group(2) is not None else 1
            expected_new = int(match.group(4)) if match.group(4) is not None else 1
            index += 1
            old_count = 0
            new_count = 0
            body_lines = 0
            while old_count < expected_old or new_count < expected_new:
                if index >= len(lines):
                    break
                line = lines[index]
                if line == "\\ No newline at end of file":
                    if body_lines == 0:
                        errors.append(f"{path} hunk {hunk_count}: misplaced no-newline marker")
                        return
                    index += 1
                    continue
                if line.startswith(" "):
                    old_count += 1
                    new_count += 1
                elif line.startswith("-"):
                    old_count += 1
                    changed_lines += 1
                elif line.startswith("+"):
                    new_count += 1
                    changed_lines += 1
                else:
                    errors.append(f"{path} hunk {hunk_count}: body line lacks a diff prefix")
                    return
                body_lines += 1
                index += 1
                if old_count > expected_old or new_count > expected_new:
                    errors.append(
                        f"{path} hunk {hunk_count}: body exceeds the declared line counts"
                    )
                    return
            if old_count != expected_old or new_count != expected_new:
                errors.append(
                    f"{path} hunk {hunk_count}: header declares {expected_old} old/"
                    f"{expected_new} new lines but body contains {old_count} old/"
                    f"{new_count} new lines"
                )
                return
            while index < len(lines) and lines[index] == "\\ No newline at end of file":
                if body_lines == 0:
                    errors.append(f"{path} hunk {hunk_count}: misplaced no-newline marker")
                    return
                index += 1
        if section_hunks == 0:
            errors.append(f"{path}: file section {section_count} has no unified-diff hunk")
            return

    if hunk_count == 0:
        errors.append(f"{path}: unified diff must include at least one valid @@ hunk header")
    if changed_lines == 0:
        errors.append(f"{path}: unified diff must include at least one added or removed line")

    patch_path = path.rsplit(".", 1)[0] + ".path"
    if declared_path is not None:
        if not is_nonempty_string(declared_path):
            errors.append(f"{patch_path}: must be a non-empty string")
        elif candidate_paths and declared_path not in candidate_paths:
            errors.append(f"{patch_path}: {declared_path!r} does not match diff headers")


def validate_source_context(context: Any, path: str, errors: list[str]) -> None:
    if not isinstance(context, dict):
        errors.append(f"{path}: source context must be an object")
        return
    if not is_nonempty_string(context.get("path")):
        errors.append(f"{path}.path: source path is required")
    lines = context.get("lines")
    if not isinstance(lines, list) or not lines:
        errors.append(f"{path}.lines: source context must include at least one line")
        return
    numbers: list[int] = []
    for index, line in enumerate(lines):
        line_path = f"{path}.lines[{index}]"
        if not isinstance(line, dict):
            errors.append(f"{line_path}: source line must be an object")
            continue
        number = line.get("number")
        if isinstance(number, bool) or not isinstance(number, int) or number < 1:
            errors.append(f"{line_path}.number: line number must be a positive integer")
        else:
            numbers.append(number)
        if not isinstance(line.get("code"), str):
            errors.append(f"{line_path}.code: code must be a string")
        state = line.get("state")
        if state is not None and state not in LINE_STATES:
            errors.append(
                f"{line_path}.state: expected one of {', '.join(sorted(LINE_STATES))}"
            )
        annotations = line.get("annotations")
        if annotations is not None:
            if not isinstance(annotations, list):
                errors.append(f"{line_path}.annotations: annotations must be an array")
            else:
                for annotation_index, annotation in enumerate(annotations):
                    annotation_path = f"{line_path}.annotations[{annotation_index}]"
                    if not isinstance(annotation, dict):
                        errors.append(f"{annotation_path}: annotation must be an object")
                        continue
                    kind = annotation.get("type")
                    if kind is not None and kind not in ANNOTATION_TYPES:
                        errors.append(
                            f"{annotation_path}.type: expected one of "
                            f"{', '.join(sorted(ANNOTATION_TYPES))}"
                        )
    if len(numbers) == len(lines):
        if numbers != sorted(set(numbers)):
            errors.append(f"{path}.lines: line numbers must be unique and strictly increasing")
        start = context.get("startLine")
        if start is not None:
            if isinstance(start, bool) or not isinstance(start, int) or start < 1:
                errors.append(f"{path}.startLine: must be a positive integer")
            elif numbers and start != numbers[0]:
                errors.append(f"{path}.startLine: must equal the first source line number")
        end = context.get("endLine")
        if end is not None:
            if isinstance(end, bool) or not isinstance(end, int) or end < 1:
                errors.append(f"{path}.endLine: must be a positive integer")
            elif numbers and end != numbers[-1]:
                errors.append(f"{path}.endLine: must equal the last source line number")


def validate_secret_string(value: str, path: str, errors: list[str]) -> None:
    for label, pattern in SECRET_PATTERNS:
        if pattern.search(value):
            errors.append(f"{path}: possible {label} must be removed or redacted")
    for match in PRIVATE_KEY_HEADER_RE.finditer(value):
        tail = value[match.end() :]
        end = PRIVATE_KEY_END_RE.search(tail)
        body = tail[: end.start()] if end is not None else tail
        if body.strip() and not is_redacted(body):
            errors.append(f"{path}: private-key material must be removed or redacted")
    for match in CREDENTIAL_URL_RE.finditer(value):
        if not is_redacted(match.group("password")):
            errors.append(f"{path}: credential-bearing URL password must be redacted")
    for match in AUTH_HEADER_RE.finditer(value):
        if not is_redacted(match.group(2)):
            errors.append(f"{path}: authorization credential must be redacted")
    for match in COOKIE_HEADER_RE.finditer(value):
        header_name = match.group(1).lower()
        fields = [part.strip() for part in match.group(2).split(";") if part.strip()]
        cookie_fields = fields if header_name == "cookie" else fields[:1]
        if not cookie_fields or any(
            "=" not in field or not is_redacted(field.split("=", 1)[1])
            for field in cookie_fields
        ):
            errors.append(f"{path}: cookie value must be redacted")
    for match in SECRET_LITERAL_RE.finditer(value):
        secret_value = match.group("value")
        if secret_value and not is_redacted(secret_value):
            errors.append(f"{path}: hard-coded credential-like literal must be redacted")


def validate_sparse_and_safe(data: Any, errors: list[str]) -> None:
    def visit(value: Any, path: str, key: str | None) -> None:
        if value is None:
            errors.append(f"{path}: omit unsupported optional values instead of using null")
            return
        if isinstance(value, str):
            if SURROGATE_RE.search(value):
                errors.append(f"{path}: string contains an unpaired Unicode surrogate")
            stripped = value.strip()
            if not stripped:
                if not is_source_code_path(path):
                    errors.append(f"{path}: omit empty optional strings")
                return
            if not is_code_or_patch_path(path) and not is_source_path_value(path):
                if (
                    stripped.lower() in PLACEHOLDER_EXACT
                    or PLACEHOLDER_RE.search(stripped)
                    or EXPLICIT_FIELD_PLACEHOLDER_RE.fullmatch(stripped)
                ):
                    errors.append(f"{path}: placeholder text is not report data")
            validate_secret_string(value, path, errors)
            return
        if isinstance(value, dict):
            if not value:
                errors.append(f"{path}: omit empty optional objects")
                return
            for child_key, child in value.items():
                normalized = normalized_key(child_key)
                child_path = json_path(path, child_key)
                if normalized == "status" and child_path != "$.report.status":
                    errors.append(
                        f"{child_path}: finding/workflow status is out of scope; only report.status is allowed"
                    )
                elif normalized in DISALLOWED_KEYS:
                    errors.append(
                        f"{child_path}: tracking or patch-lifecycle field {child_key!r} is out of scope"
                    )
                if normalized == "url" and isinstance(child, str):
                    try:
                        parsed = urlparse(child)
                    except ValueError:
                        parsed = None
                    if (
                        not check_absolute_uri(child)
                        or parsed is None
                        or parsed.scheme not in {"http", "https"}
                        or not parsed.netloc
                    ):
                        errors.append(f"{child_path}: reference URL must be an absolute HTTP(S) URL")
                    elif parsed.username is not None or parsed.password is not None:
                        errors.append(f"{child_path}: reference URL must not contain credentials")
                visit(child, child_path, child_key)
            return
        if isinstance(value, list):
            if not value and (key is None or normalized_key(key) not in EMPTY_ARRAY_KEYS):
                errors.append(f"{path}: omit empty optional arrays")
                return
            for index, child in enumerate(value):
                visit(child, json_path(path, index), key)

    visit(data, "$", None)


def validate_data(data: Any, *, for_build: bool = False) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["$: report data must be a JSON object"]

    required_root = ("report", "findings")
    for key in required_root:
        if key not in data:
            errors.append(f"$.{key}: required property is missing")

    report = data.get("report")
    if not isinstance(report, dict):
        errors.append("$.report: must be an object")
    else:
        for key in ("id", "title", "version"):
            if not is_nonempty_string(report.get(key)):
                errors.append(f"$.report.{key}: non-empty string is required")
        status = report.get("status")
        if status is not None and status not in REPORT_STATUSES:
            errors.append(f"$.report.status: expected one of {', '.join(sorted(REPORT_STATUSES))}")

    source_ids: set[str] = set()
    scope = data.get("scope")
    if scope is not None and not isinstance(scope, dict):
        errors.append("$.scope: must be an object when present")
    elif isinstance(scope, dict):
        targets = scope.get("targets")
        if targets is not None:
            if not isinstance(targets, list):
                errors.append("$.scope.targets: must be an array")
            else:
                for index, target in enumerate(targets):
                    path = f"$.scope.targets[{index}]"
                    if not isinstance(target, dict):
                        errors.append(f"{path}: target must be an object")
                        continue
                    target_id = target.get("id")
                    if not isinstance(target_id, str) or not SOURCE_ID_RE.fullmatch(target_id):
                        errors.append(f"{path}.id: expected stable ID matching SRC-...")
                    elif target_id in source_ids:
                        errors.append(f"{path}.id: duplicate source ID {target_id!r}")
                    else:
                        source_ids.add(target_id)

    findings = data.get("findings")
    finding_ids: set[str] = set()
    evidence_ids: set[str] = set()
    pending_finding_refs: list[tuple[str, Any]] = []
    pending_source_refs: list[tuple[str, Any]] = []
    if not isinstance(findings, list):
        errors.append("$.findings: must be an array")
    else:
        for index, finding in enumerate(findings):
            path = f"$.findings[{index}]"
            if not isinstance(finding, dict):
                errors.append(f"{path}: finding must be an object")
                continue
            finding_id = finding.get("id")
            if not isinstance(finding_id, str) or not FINDING_ID_RE.fullmatch(finding_id):
                errors.append(f"{path}.id: expected stable ID matching F-...")
            elif finding_id in finding_ids:
                errors.append(f"{path}.id: duplicate finding ID {finding_id!r}")
            else:
                finding_ids.add(finding_id)
            if not is_nonempty_string(finding.get("title")):
                errors.append(f"{path}.title: non-empty string is required")
            severity = finding.get("severity")
            if severity not in SEVERITIES:
                errors.append(f"{path}.severity: expected one of {', '.join(sorted(SEVERITIES))}")
            confidence = finding.get("confidence")
            if confidence is not None and confidence not in CONFIDENCES:
                errors.append(f"{path}.confidence: expected one of {', '.join(sorted(CONFIDENCES))}")

            risk = finding.get("risk")
            if risk is not None:
                if not isinstance(risk, dict):
                    errors.append(f"{path}.risk: must be an object")
                else:
                    likelihood = risk.get("likelihood")
                    if likelihood is not None and likelihood not in LIKELIHOOD_LEVELS:
                        errors.append(
                            f"{path}.risk.likelihood: expected one of "
                            f"{', '.join(sorted(LIKELIHOOD_LEVELS))}"
                        )
                    impact = risk.get("impact")
                    if impact is not None and impact not in IMPACT_LEVELS:
                        errors.append(
                            f"{path}.risk.impact: expected one of "
                            f"{', '.join(sorted(IMPACT_LEVELS))}"
                        )
                    score = risk.get("cvssScore")
                    if score is not None and (
                        isinstance(score, bool)
                        or not isinstance(score, (int, float))
                        or not 0 <= score <= 10
                    ):
                        errors.append(f"{path}.risk.cvssScore: must be a number from 0 through 10")
                    version = risk.get("cvssVersion")
                    vector = risk.get("cvssVector")
                    if version is not None and version not in {"3.0", "3.1", "4.0"}:
                        errors.append(f"{path}.risk.cvssVersion: expected 3.0, 3.1, or 4.0")
                    if vector is not None and not is_nonempty_string(vector):
                        errors.append(f"{path}.risk.cvssVector: must be a non-empty string")
                    if vector is not None and version is None:
                        errors.append(f"{path}.risk.cvssVersion: required when cvssVector is supplied")
                    if score is not None and (version is None or vector is None):
                        errors.append(
                            f"{path}.risk: cvssScore requires both cvssVersion and cvssVector"
                        )
                    if isinstance(version, str) and isinstance(vector, str):
                        expected_prefix = f"CVSS:{version}/"
                        if not vector.startswith(expected_prefix):
                            errors.append(
                                f"{path}.risk.cvssVector: must start with {expected_prefix!r}"
                            )
                        elif version in {"3.0", "3.1"}:
                            calculated = cvss3_base_score(vector)
                            if calculated is None:
                                errors.append(
                                    f"{path}.risk.cvssVector: malformed, unknown, or missing required CVSS v3 metrics"
                                )
                            elif (
                                isinstance(score, (int, float))
                                and not isinstance(score, bool)
                                and abs(float(score) - calculated) > 0.001
                            ):
                                errors.append(
                                    f"{path}.risk.cvssScore: {score} does not match vector base score {calculated}"
                                )

            contexts = finding.get("sourceContexts")
            if contexts is not None:
                if not isinstance(contexts, list):
                    errors.append(f"{path}.sourceContexts: must be an array")
                else:
                    for context_index, context in enumerate(contexts):
                        validate_source_context(
                            context, f"{path}.sourceContexts[{context_index}]", errors
                        )

            artifacts = finding.get("supportingArtifacts")
            if artifacts is not None:
                if not isinstance(artifacts, list):
                    errors.append(f"{path}.supportingArtifacts: must be an array")
                else:
                    for artifact_index, artifact in enumerate(artifacts):
                        artifact_path = f"{path}.supportingArtifacts[{artifact_index}]"
                        if not isinstance(artifact, dict):
                            errors.append(f"{artifact_path}: supporting artifact must be an object")
                            continue
                        artifact_id = artifact.get("id")
                        if not isinstance(artifact_id, str) or not EVIDENCE_ID_RE.fullmatch(
                            artifact_id
                        ):
                            errors.append(f"{artifact_path}.id: expected stable ID matching EV-...")
                        elif artifact_id in evidence_ids:
                            errors.append(f"{artifact_path}.id: duplicate evidence ID {artifact_id!r}")
                        else:
                            evidence_ids.add(artifact_id)
                        for required_key in ("type", "title"):
                            if not is_nonempty_string(artifact.get(required_key)):
                                errors.append(
                                    f"{artifact_path}.{required_key}: non-empty string is required"
                                )

            remediation = finding.get("remediation")
            if remediation is not None:
                if not isinstance(remediation, dict):
                    errors.append(f"{path}.remediation: must be an object")
                else:
                    patch = remediation.get("patch")
                    if patch is not None:
                        patch_path = f"{path}.remediation.patch"
                        if not isinstance(patch, dict):
                            errors.append(f"{patch_path}: must be an object")
                        else:
                            if patch.get("format") != "unified-diff":
                                errors.append(f"{patch_path}.format: must be 'unified-diff'")
                            validate_unified_diff(
                                patch.get("content"),
                                f"{patch_path}.content",
                                errors,
                                patch.get("path"),
                            )

            target_refs = finding.get("affectedTargetRefs")
            if target_refs is not None:
                if not isinstance(target_refs, list):
                    errors.append(f"{path}.affectedTargetRefs: must be an array")
                else:
                    for ref_index, ref in enumerate(target_refs):
                        pending_source_refs.append(
                            (f"{path}.affectedTargetRefs[{ref_index}]", ref)
                        )

    executive = data.get("executiveSummary")
    if executive is not None and not isinstance(executive, dict):
        errors.append("$.executiveSummary: must be an object when present")
    elif isinstance(executive, dict):
        overall_risk = executive.get("overallRisk")
        if overall_risk is not None and overall_risk not in RISK_LEVELS:
            errors.append(
                "$.executiveSummary.overallRisk: expected one of "
                + ", ".join(sorted(RISK_LEVELS))
            )

    # Resolve any explicit *FindingRef(s) fields, including future compatible fields.
    def collect_refs(value: Any, path: str) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                child_path = json_path(path, key)
                normalized = normalized_key(key)
                if normalized.endswith("findingref"):
                    pending_finding_refs.append((child_path, child))
                elif normalized.endswith("findingrefs"):
                    if not isinstance(child, list):
                        errors.append(f"{child_path}: finding references must be an array")
                    else:
                        for index, ref in enumerate(child):
                            pending_finding_refs.append((json_path(child_path, index), ref))
                collect_refs(child, child_path)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                collect_refs(child, json_path(path, index))

    collect_refs(data, "$")
    for path, ref in pending_finding_refs:
        if not isinstance(ref, str) or not FINDING_ID_RE.fullmatch(ref):
            errors.append(f"{path}: expected finding reference matching F-...")
        elif ref not in finding_ids:
            errors.append(f"{path}: unresolved finding reference {ref!r}")
    for path, ref in pending_source_refs:
        if not isinstance(ref, str) or not SOURCE_ID_RE.fullmatch(ref):
            errors.append(f"{path}: expected source reference matching SRC-...")
        elif ref not in source_ids:
            errors.append(f"{path}: unresolved source reference {ref!r}")

    validate_sparse_and_safe(data, errors)
    return sorted(set(errors))


def _json_equal(left: Any, right: Any) -> bool:
    if isinstance(left, bool) or isinstance(right, bool):
        return isinstance(left, bool) and isinstance(right, bool) and left == right
    if (
        isinstance(left, (int, float))
        and isinstance(right, (int, float))
        and not isinstance(left, bool)
        and not isinstance(right, bool)
    ):
        return left == right
    if isinstance(left, list) and isinstance(right, list):
        return len(left) == len(right) and all(
            _json_equal(left_item, right_item)
            for left_item, right_item in zip(left, right)
        )
    if isinstance(left, dict) and isinstance(right, dict):
        return left.keys() == right.keys() and all(
            _json_equal(left[key], right[key]) for key in left
        )
    return type(left) is type(right) and left == right


def _resolve_local_ref(root: dict[str, Any], reference: str) -> Any:
    if not reference.startswith("#/"):
        raise ValueError(f"only local JSON Schema references are supported: {reference}")
    current: Any = root
    for encoded_part in reference[2:].split("/"):
        part = encoded_part.replace("~1", "/").replace("~0", "~")
        if not isinstance(current, dict) or part not in current:
            raise ValueError(f"unresolved JSON Schema reference: {reference}")
        current = current[part]
    return current


def validate_supported_schema(schema: dict[str, Any]) -> list[str]:
    """Fail closed when a schema uses syntax outside the stdlib validator subset."""
    errors: list[str] = []

    def inspect(rule: Any, path: str) -> None:
        if isinstance(rule, bool):
            return
        if not isinstance(rule, dict):
            errors.append(f"{path}: schema node must be an object or boolean")
            return

        for keyword in rule:
            if keyword not in SUPPORTED_SCHEMA_KEYWORDS:
                errors.append(f"{json_path(path, keyword)}: unsupported schema keyword")

        dialect = rule.get("$schema")
        if "$schema" in rule and dialect != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"{json_path(path, '$schema')}: unsupported JSON Schema dialect")
        for annotation in ("$id", "title", "description"):
            if annotation in rule and not isinstance(rule[annotation], str):
                errors.append(f"{json_path(path, annotation)}: schema annotation must be a string")

        definitions = rule.get("$defs")
        if "$defs" in rule:
            if not isinstance(definitions, dict):
                errors.append(f"{json_path(path, '$defs')}: schema definitions must be an object")
            else:
                for name, child in definitions.items():
                    inspect(child, json_path(json_path(path, "$defs"), name))

        reference = rule.get("$ref")
        if "$ref" in rule:
            if not isinstance(reference, str) or not reference.startswith("#/"):
                errors.append(f"{json_path(path, '$ref')}: only local JSON Pointer references are supported")
            else:
                try:
                    _resolve_local_ref(schema, reference)
                except (TypeError, ValueError) as exc:
                    errors.append(f"{json_path(path, '$ref')}: {exc}")

        expected = rule.get("type")
        if "type" in rule:
            expected_types = [expected] if isinstance(expected, str) else expected
            if (
                not isinstance(expected_types, list)
                or not expected_types
                or not all(isinstance(item, str) for item in expected_types)
                or len(expected_types) != len(set(expected_types))
            ):
                errors.append(f"{json_path(path, 'type')}: invalid schema type declaration")
            else:
                unsupported_types = set(expected_types) - SUPPORTED_SCHEMA_TYPES
                if unsupported_types:
                    errors.append(
                        f"{json_path(path, 'type')}: unsupported schema type(s): "
                        + ", ".join(sorted(unsupported_types))
                    )

        properties = rule.get("properties")
        if "properties" in rule:
            if not isinstance(properties, dict):
                errors.append(f"{json_path(path, 'properties')}: schema properties must be an object")
            else:
                for name, child in properties.items():
                    inspect(child, json_path(json_path(path, "properties"), name))

        for keyword in ("additionalProperties", "items"):
            child = rule.get(keyword)
            if keyword in rule:
                if not isinstance(child, (bool, dict)):
                    errors.append(f"{json_path(path, keyword)}: expected a schema or boolean")
                else:
                    inspect(child, json_path(path, keyword))

        required = rule.get("required")
        if "required" in rule and (
            not isinstance(required, list)
            or not all(isinstance(item, str) for item in required)
            or len(required) != len(set(required))
        ):
            errors.append(f"{json_path(path, 'required')}: expected unique property names")

        dependent = rule.get("dependentRequired")
        if "dependentRequired" in rule:
            if not isinstance(dependent, dict):
                errors.append(f"{json_path(path, 'dependentRequired')}: expected an object")
            else:
                for trigger, dependencies in dependent.items():
                    if (
                        not isinstance(dependencies, list)
                        or not all(isinstance(item, str) for item in dependencies)
                        or len(dependencies) != len(set(dependencies))
                    ):
                        errors.append(
                            f"{json_path(json_path(path, 'dependentRequired'), trigger)}: "
                            "expected unique property names"
                        )

        enum = rule.get("enum")
        if "enum" in rule:
            if not isinstance(enum, list) or not enum:
                errors.append(f"{json_path(path, 'enum')}: expected a non-empty array")
            elif any(
                _json_equal(value, previous)
                for index, value in enumerate(enum)
                for previous in enum[:index]
            ):
                errors.append(f"{json_path(path, 'enum')}: values must be unique")

        for keyword in ("minProperties", "minItems", "maxItems", "minLength", "maxLength"):
            constraint = rule.get(keyword)
            if keyword in rule and (
                isinstance(constraint, bool)
                or not isinstance(constraint, int)
                or constraint < 0
            ):
                errors.append(f"{json_path(path, keyword)}: expected a non-negative integer")
        for minimum_keyword, maximum_keyword in (
            ("minItems", "maxItems"),
            ("minLength", "maxLength"),
        ):
            minimum_value = rule.get(minimum_keyword)
            maximum_value = rule.get(maximum_keyword)
            if (
                isinstance(minimum_value, int)
                and not isinstance(minimum_value, bool)
                and isinstance(maximum_value, int)
                and not isinstance(maximum_value, bool)
                and minimum_value > maximum_value
            ):
                errors.append(f"{path}: schema minimum exceeds maximum")

        pattern = rule.get("pattern")
        if "pattern" in rule:
            if not isinstance(pattern, str):
                errors.append(f"{json_path(path, 'pattern')}: expected a string")
            else:
                try:
                    re.compile(pattern)
                except re.error as exc:
                    errors.append(f"{json_path(path, 'pattern')}: invalid pattern: {exc}")

        value_format = rule.get("format")
        if "format" in rule and value_format not in SUPPORTED_SCHEMA_FORMATS:
            errors.append(f"{json_path(path, 'format')}: unsupported schema format")

        unique_items = rule.get("uniqueItems")
        if "uniqueItems" in rule and not isinstance(unique_items, bool):
            errors.append(f"{json_path(path, 'uniqueItems')}: expected a boolean")

        for keyword in ("minimum", "maximum"):
            constraint = rule.get(keyword)
            if keyword in rule and (
                isinstance(constraint, bool)
                or not isinstance(constraint, (int, float))
                or not math.isfinite(constraint)
            ):
                errors.append(f"{json_path(path, keyword)}: expected a finite number")
        minimum = rule.get("minimum")
        maximum = rule.get("maximum")
        if (
            isinstance(minimum, (int, float))
            and not isinstance(minimum, bool)
            and isinstance(maximum, (int, float))
            and not isinstance(maximum, bool)
            and minimum > maximum
        ):
            errors.append(f"{path}: schema minimum exceeds maximum")

    inspect(schema, "$schema")
    return sorted(set(errors))


def _schema_type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        if isinstance(value, int) and not isinstance(value, bool):
            return True
        return isinstance(value, float) and math.isfinite(value) and value.is_integer()
    if expected == "number":
        return (
            isinstance(value, int)
            and not isinstance(value, bool)
            or isinstance(value, float)
            and math.isfinite(value)
        )
    if expected == "null":
        return value is None
    return False


def validate_schema_stdlib(schema: dict[str, Any], data: Any) -> list[str]:
    """Validate the keyword subset used by the bundled Draft 2020-12 schema."""
    errors = validate_supported_schema(schema)
    if errors:
        return errors

    def apply(rule: Any, value: Any, path: str, ref_stack: tuple[str, ...] = ()) -> None:
        if isinstance(rule, bool):
            if not rule:
                errors.append(f"{path}: schema does not allow this value")
            return
        if not isinstance(rule, dict):
            errors.append(f"{path}: invalid JSON Schema node")
            return
        if "$ref" in rule:
            reference = rule["$ref"]
            if reference in ref_stack:
                errors.append(f"{path}: schema: circular references are not supported")
                return
            try:
                target = _resolve_local_ref(schema, reference)
            except (TypeError, ValueError) as exc:
                errors.append(f"{path}: schema: {exc}")
                return
            apply(target, value, path, ref_stack + (reference,))

        expected = rule.get("type")
        if expected is not None:
            expected_types = [expected] if isinstance(expected, str) else expected
            if not isinstance(expected_types, list) or not all(
                isinstance(item, str) for item in expected_types
            ):
                errors.append(f"{path}: schema has an invalid type declaration")
                return
            if not any(_schema_type_matches(value, item) for item in expected_types):
                errors.append(f"{path}: schema: expected type {' or '.join(expected_types)}")
                return
        if "const" in rule and not _json_equal(value, rule["const"]):
            errors.append(f"{path}: schema: expected constant {rule['const']!r}")
        if "enum" in rule and not any(_json_equal(value, item) for item in rule["enum"]):
            errors.append(f"{path}: schema: value is not in the allowed enum")

        if isinstance(value, dict):
            required = rule.get("required", [])
            if isinstance(required, list):
                for key in required:
                    if key not in value:
                        errors.append(f"{json_path(path, key)}: schema: required property is missing")
            min_properties = rule.get("minProperties")
            if isinstance(min_properties, int) and len(value) < min_properties:
                errors.append(f"{path}: schema: expected at least {min_properties} properties")
            properties = rule.get("properties", {})
            if not isinstance(properties, dict):
                properties = {}
            for key, child in value.items():
                child_path = json_path(path, key)
                if key in properties:
                    apply(properties[key], child, child_path, ref_stack)
                else:
                    additional = rule.get("additionalProperties", True)
                    if additional is False:
                        errors.append(f"{child_path}: schema: additional property is not allowed")
                    elif isinstance(additional, dict):
                        apply(additional, child, child_path, ref_stack)
            dependent = rule.get("dependentRequired", {})
            if isinstance(dependent, dict):
                for trigger, dependencies in dependent.items():
                    if trigger in value and isinstance(dependencies, list):
                        for dependency in dependencies:
                            if dependency not in value:
                                errors.append(
                                    f"{json_path(path, dependency)}: schema: required when {trigger!r} is present"
                                )

        if isinstance(value, list):
            min_items = rule.get("minItems")
            max_items = rule.get("maxItems")
            if isinstance(min_items, int) and len(value) < min_items:
                errors.append(f"{path}: schema: expected at least {min_items} items")
            if isinstance(max_items, int) and len(value) > max_items:
                errors.append(f"{path}: schema: expected at most {max_items} items")
            if rule.get("uniqueItems") is True:
                if any(
                    _json_equal(item, previous)
                    for index, item in enumerate(value)
                    for previous in value[:index]
                ):
                    errors.append(f"{path}: schema: array items must be unique")
            item_rule = rule.get("items")
            if item_rule is not None:
                for index, child in enumerate(value):
                    apply(item_rule, child, json_path(path, index), ref_stack)

        if isinstance(value, str):
            min_length = rule.get("minLength")
            max_length = rule.get("maxLength")
            if isinstance(min_length, int) and len(value) < min_length:
                errors.append(f"{path}: schema: string is shorter than {min_length} characters")
            if isinstance(max_length, int) and len(value) > max_length:
                errors.append(f"{path}: schema: string is longer than {max_length} characters")
            pattern = rule.get("pattern")
            if isinstance(pattern, str):
                try:
                    if re.search(pattern, value) is None:
                        errors.append(f"{path}: schema: string does not match required pattern")
                except re.error as exc:
                    errors.append(f"{path}: schema has an invalid pattern: {exc}")
            value_format = rule.get("format")
            if value_format == "date-time" and not check_iso_datetime(value):
                errors.append(f"{path}: schema: expected ISO 8601 date-time with timezone")
            elif value_format == "date" and not check_iso_date(value):
                errors.append(f"{path}: schema: expected ISO 8601 calendar date")
            elif value_format == "uri" and not check_absolute_uri(value):
                errors.append(f"{path}: schema: expected an absolute URI")

        if isinstance(value, (int, float)) and not isinstance(value, bool):
            minimum = rule.get("minimum")
            maximum = rule.get("maximum")
            if isinstance(minimum, (int, float)) and value < minimum:
                errors.append(f"{path}: schema: value is below minimum {minimum}")
            if isinstance(maximum, (int, float)) and value > maximum:
                errors.append(f"{path}: schema: value is above maximum {maximum}")

    apply(schema, data, "$")
    return sorted(set(errors))


def load_and_check_schema(schema_path: Path, data: Any) -> tuple[list[str], list[str]]:
    """Apply the supported JSON Schema subset using only the standard library."""
    schema = load_json(schema_path)
    if not isinstance(schema, dict):
        return [f"{schema_path}: JSON Schema root must be an object"], []
    return validate_schema_stdlib(schema, data), []


def external_asset_tags(html: str) -> list[str]:
    tags: list[str] = []
    for tag in re.findall(r"<(?:script|link)\b[^>]*>", html, flags=re.IGNORECASE):
        match = re.search(
            r"\s(?:src|href)\s*=\s*['\"]([^'\"]+)['\"]", tag, flags=re.IGNORECASE
        )
        if match is not None and match.group(1).lower().startswith(
            ("https://", "http://", "//")
        ):
            tags.append(tag)
    return tags


def _asset_url(tag: str) -> str | None:
    match = re.search(
        r"\s(?:src|href)\s*=\s*['\"]([^'\"]+)['\"]", tag, flags=re.IGNORECASE
    )
    return match.group(1) if match is not None else None


def _valid_sri_token(token: str) -> bool:
    algorithm, separator, digest = token.partition("-")
    expected_lengths = {"sha256": 32, "sha384": 48, "sha512": 64}
    if not separator or algorithm.lower() not in expected_lengths or not digest:
        return False
    normalized = digest.replace("-", "+").replace("_", "/")
    normalized += "=" * (-len(normalized) % 4)
    try:
        decoded = base64.b64decode(normalized, validate=True)
    except (binascii.Error, ValueError):
        return False
    return len(decoded) == expected_lengths[algorithm.lower()]


def require_external_asset_integrity(html: str) -> None:
    for index, tag in enumerate(external_asset_tags(html), start=1):
        asset_url = _asset_url(tag)
        if asset_url is None or not asset_url.lower().startswith("https://"):
            raise TemplateError(f"external CDN asset tag {index} must use HTTPS")
        integrity = re.search(
            r"\bintegrity\s*=\s*['\"]([^'\"]+)['\"]",
            tag,
            flags=re.IGNORECASE,
        )
        if integrity is None or not integrity.group(1).split() or not all(
            _valid_sri_token(token) for token in integrity.group(1).split()
        ):
            raise TemplateError(f"external CDN asset tag {index} is missing a valid SRI hash")
        crossorigin = re.search(
            r"\bcrossorigin\s*=\s*['\"]anonymous['\"]", tag, flags=re.IGNORECASE
        )
        if crossorigin is None:
            raise TemplateError(f"external CDN asset tag {index} must use crossorigin='anonymous'")
        referrer_policy = re.search(
            r"\breferrerpolicy\s*=\s*['\"]no-referrer['\"]", tag, flags=re.IGNORECASE
        )
        if referrer_policy is None:
            raise TemplateError(
                f"external CDN asset tag {index} must use referrerpolicy='no-referrer'"
            )


def safe_json_for_html(data: Any) -> str:
    serialized = json.dumps(
        data,
        ensure_ascii=True,
        indent=2,
        sort_keys=True,
        separators=(",", ": "),
    )
    return (
        serialized.replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


def prepare_html_data(data: dict[str, Any]) -> dict[str, Any]:
    """Add renderer-only metadata without exposing it in canonical report data."""
    html_data = dict(data)
    html_data["schemaVersion"] = SCHEMA_VERSION
    html_data["generation"] = {
        "generatedAt": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "requiresHumanVerification": True,
        "sampleData": False,
    }
    return html_data


def reject_template_preview_data(template: str, data: Any) -> None:
    """Prevent a deliverable from reusing the template's bundled preview content."""
    if template.count(START_MARKER) != 1 or template.count(END_MARKER) != 1:
        return
    start = template.index(START_MARKER) + len(START_MARKER)
    end = template.index(END_MARKER)
    if start >= end:
        return
    matches = list(REPORT_DATA_SCRIPT_RE.finditer(template[start:end]))
    if len(matches) != 1:
        return
    try:
        preview = json.loads(
            matches[0].group(2),
            object_pairs_hook=_unique_object,
            parse_constant=_reject_nonfinite_json,
        )
    except (json.JSONDecodeError, DuplicateKeyError, ValueError) as exc:
        raise TemplateError(f"template preview data is invalid JSON: {exc}") from exc
    if not isinstance(preview, dict) or not (
        isinstance(preview.get("generation"), dict)
        and preview["generation"].get("sampleData") is True
    ):
        return

    preview_report = preview.get("report")
    report = data.get("report") if isinstance(data, dict) else None
    if isinstance(preview_report, dict) and isinstance(report, dict):
        for field in ("id", "title"):
            if is_nonempty_string(preview_report.get(field)) and report.get(field) == preview_report[field]:
                raise TemplateError(
                    f"report.{field} still uses the template preview value; replace demo data before building"
                )

    preview_findings = {
        (finding.get("id"), finding.get("title"))
        for finding in preview.get("findings", [])
        if isinstance(finding, dict)
        and is_nonempty_string(finding.get("id"))
        and is_nonempty_string(finding.get("title"))
    }
    for finding in data.get("findings", []) if isinstance(data, dict) else []:
        if isinstance(finding, dict) and (finding.get("id"), finding.get("title")) in preview_findings:
            raise TemplateError(
                f"finding {finding.get('id')!r} still uses template preview content; replace demo data before building"
            )


def embed_report_data(template: str, serialized: str) -> str:
    require_external_asset_integrity(template)
    start_count = template.count(START_MARKER)
    end_count = template.count(END_MARKER)
    if start_count == 1 and end_count == 1:
        start = template.index(START_MARKER) + len(START_MARKER)
        end = template.index(END_MARKER)
        if start >= end:
            raise TemplateError("report data markers are out of order")
        block = template[start:end]
        matches = list(REPORT_DATA_SCRIPT_RE.finditer(block))
        if len(matches) != 1:
            raise TemplateError(
                f"expected one application/json script with id {DATA_SCRIPT_ID!r} between markers"
            )
        match = matches[0]
        populated_block = (
            block[: match.start()]
            + match.group(1)
            + "\n"
            + serialized
            + "\n  "
            + match.group(3)
            + block[match.end() :]
        )
        result = template[:start] + populated_block + template[end:]
    elif start_count or end_count:
        raise TemplateError("expected exactly one REPORT_DATA_START/REPORT_DATA_END marker pair")
    elif template.count(TOKEN_MARKER) == 1:
        result = template.replace(TOKEN_MARKER, serialized, 1)
    else:
        raise TemplateError(
            "template needs one report-data marker pair or one /*__REPORT_DATA__*/ token"
        )

    if external_asset_tags(result) != external_asset_tags(template):
        raise TemplateError("external CDN asset tags changed while embedding report data")
    if "</script" in serialized.lower():
        raise TemplateError("serialized data contains an unsafe script terminator")
    return result


def finalize_report_html(report: str, serialized: str) -> str:
    """Remove template-only comments and verify that no sample payload remains."""
    result = HTML_COMMENT_RE.sub("", report)
    if "<!--" in result or "-->" in result:
        raise TemplateError("final report contains a malformed or unterminated HTML comment")
    if TOKEN_MARKER in result:
        raise TemplateError("final report contains an unresolved report-data token")

    matches = list(REPORT_DATA_SCRIPT_RE.finditer(result))
    if len(matches) != 1:
        raise TemplateError(
            f"final report must contain one application/json script with id {DATA_SCRIPT_ID!r}"
        )
    if matches[0].group(2).strip() != serialized:
        raise TemplateError("final report data does not exactly match the validated input")
    return result


def atomic_write(path: Path, content: str, mode: int | None = None) -> None:
    parent = path.parent
    try:
        parent.mkdir(parents=True, exist_ok=True)
        descriptor: int | None = None
        temporary_name: Path | None = None
        for _ in range(100):
            candidate = parent / f".{path.name}.{secrets.token_hex(8)}.tmp"
            try:
                descriptor = os.open(
                    candidate,
                    os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                    0o666,
                )
                temporary_name = candidate
                break
            except FileExistsError:
                continue
        if descriptor is None or temporary_name is None:
            raise TemplateError(f"cannot allocate a temporary output file in {parent}")
        try:
            if mode is not None:
                os.fchmod(descriptor, mode & 0o777)
            with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary_name, path)
        except Exception:
            try:
                os.unlink(temporary_name)
            except OSError:
                pass
            raise
    except OSError as exc:
        raise TemplateError(f"cannot write {path}: {exc}") from exc


def print_errors(errors: list[str]) -> None:
    print(f"Validation failed with {len(errors)} error(s):", file=sys.stderr)
    for error in errors:
        print(f"  - {error}", file=sys.stderr)


def run_validation(
    data_path: Path, schema_path: Path | None, *, for_build: bool
) -> tuple[Any | None, int]:
    try:
        data = load_json(data_path)
    except DataLoadError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return None, 2
    errors = validate_data(data, for_build=for_build)
    warnings: list[str] = []
    if schema_path is not None:
        try:
            schema_errors, schema_warnings = load_and_check_schema(schema_path, data)
        except DataLoadError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return None, 2
        errors.extend(schema_errors)
        warnings.extend(schema_warnings)
    if errors:
        print_errors(sorted(set(errors)))
        return None, 1
    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    if for_build:
        assert isinstance(data, dict)
        data = prepare_html_data(data)
    return data, 0


def command_validate(args: argparse.Namespace) -> int:
    data, result = run_validation(args.data, args.schema, for_build=False)
    if result:
        return result
    assert isinstance(data, dict)
    print(f"Valid report data: {len(data['findings'])} finding(s), schema {SCHEMA_VERSION}.")
    return 0


def _paths_collide(left: Path, right: Path) -> bool:
    try:
        if left.exists() and right.exists() and os.path.samefile(left, right):
            return True
    except OSError:
        pass
    try:
        return left.resolve() == right.resolve()
    except OSError:
        return left.absolute() == right.absolute()


def command_build(args: argparse.Namespace) -> int:
    inputs = (("data", args.data), ("template", args.template))
    if args.schema is not None:
        inputs += (("schema", args.schema),)
    for label, input_path in inputs:
        if _paths_collide(args.output, input_path):
            print(f"error: output path must not overwrite the {label} input: {input_path}", file=sys.stderr)
            return 2
    data, result = run_validation(args.data, args.schema, for_build=True)
    if result:
        return result
    assert data is not None
    try:
        template = args.template.read_text(encoding="utf-8")
        reject_template_preview_data(template, data)
        serialized = safe_json_for_html(data)
        populated = embed_report_data(template, serialized)
        final_report = finalize_report_html(populated, serialized)
        output_mode = stat.S_IMODE(args.data.stat().st_mode)
        atomic_write(args.output, final_report, mode=output_mode)
    except (OSError, TemplateError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"Built report: {args.output}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate findings report JSON and build the static HTML report."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser(
        "validate", help="validate report JSON without writing HTML"
    )
    validate_parser.add_argument("data", type=Path, metavar="DATA.json")
    validate_parser.add_argument(
        "--schema",
        type=Path,
        metavar="PATH",
        default=DEFAULT_SCHEMA_PATH,
        help=f"JSON Schema to apply (default: {DEFAULT_SCHEMA_PATH})",
    )
    validate_parser.set_defaults(handler=command_validate)

    build_command = subparsers.add_parser(
        "build", help="validate data and embed it in a report template"
    )
    build_command.add_argument("data", type=Path, metavar="DATA.json")
    build_command.add_argument("--template", type=Path, required=True, metavar="TEMPLATE.html")
    build_command.add_argument("--output", type=Path, required=True, metavar="REPORT.html")
    build_command.add_argument(
        "--schema",
        type=Path,
        metavar="PATH",
        default=DEFAULT_SCHEMA_PATH,
        help=f"JSON Schema to apply (default: {DEFAULT_SCHEMA_PATH})",
    )
    build_command.set_defaults(handler=command_build)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.handler(args))


if __name__ == "__main__":
    raise SystemExit(main())
