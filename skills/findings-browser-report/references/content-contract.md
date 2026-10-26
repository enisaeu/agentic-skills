---
name: findings-browser-report-content-contract
description: the content contract for the findings browser report
license: EUPL-1.2
metadata:
  version: "1.0-beta"
---

# Findings Browser Report Content Contract

Use this contract with schema `3.0.0` and the bundled static HTML renderer. It describes canonical report data, evidence discipline, omission behavior, and publication checks. The report presents supported findings; it is not a remediation tracker.

## Canonical data semantics

- Require `report` and `findings`.
- Require only `report.id`, `report.title`, and `report.version` within the report identity, and only `id`, `title`, and `severity` within each finding.
- Treat a missing or `null` optional source value as unsupported. Omit its property from canonical JSON and let the renderer omit the corresponding UI.
- Use `[]` only when an array is known to be empty and that fact matters. Do not add empty arrays merely to satisfy a shape.
- Require `findings` to be an array. `"findings": []` is a valid, explicit zero-finding result.
- Never emit empty strings, placeholder text, `TBD`, `N/A`, sample records, or synthetic names to hold a layout open.
- Keep all strings as plain text. Do not embed HTML or Markdown for the renderer to interpret.

The JSON Schema rejects `null` in canonical output. During collection, normalize missing and `null` optional values by deleting their properties before schema validation.

## Evidence and provenance discipline

Maintain an evidence ledger while collecting data, even though the ledger is not rendered. Classify every proposed report claim as one of:

- **Directly supported**: exact source, tool output, validation record, supplied notes, or other inspectable artifact supports the claim.
- **User-supplied**: an identified person or supplied document states the fact, but the project assets do not independently establish it.
- **Derived**: a narrow inference follows from cited facts. Keep the inference conservative and identify its basis in the working ledger.
- **Conflicting**: available sources disagree. Resolve the conflict with the user or omit the claim.
- **Unsupported**: no reliable source supports the claim. Omit it.

Use report fields to preserve useful provenance:

- `scope.targets[].revision`, included paths, and excluded paths bind conclusions to a particular source snapshot.
- `affectedTargetRefs` connects a finding to `scope.targets[].id`.
- `sourceContexts` supplies exact file paths and numbered excerpts.
- `supportingArtifacts[].source` names the supplied or reviewer-created origin of a request, response, log, trace, output, or other evidence record.
- `reviewBasis` briefly states the basis of the result, such as `manual-code-review`, `source-to-sink-analysis`, `supplied-scanner-result`, or `targeted-validation`.
- `validation` records what was actually demonstrated. Do not describe planned tests as observed results.

Do not invent source locations, revisions, exploit behavior, business impact, CVSS data, people, dates, findings, or evidence. Avoid false precision. When a claim is useful but not supportable, ask once for the missing fact or omit it.

## Top-level contract

```json
{
  "report": {
    "id": "REPORT-001",
    "title": "Report",
    "version": "1.0",
    "status": "draft",
    "classification": "confidential"
  },
  "findings": []
}
```

`report.status` describes document governance only and may be `draft` or `final`. It does not describe finding remediation. `report.classification` is organization-defined plain text. Optional identity fields are `language`, `client`, `provider`, `authors`, `reviewers`, `issuedAt`, and `reviewPeriod`.

Omit unidentified people or organizations; never use fictional placeholders.

## Executive summary

Omit `executiveSummary` when no supported summary is available. When present, include only supported properties:

- `overview` and `conclusion` for concise result statements.
- `overallRisk` when the assessment basis supports a single report-level rating.
- `businessImpacts`, `keyObservations`, `strengths`, and `topRecommendations` when project evidence supports them.
- `keyFindingRefs` as references to existing finding IDs.

Do not derive `overallRisk` solely by counting findings unless the assessment's defined rating model says to do so. Do not manufacture business impact from a technical condition. Every entry in `keyFindingRefs` must resolve to an actual finding.

## Audited source scope

Omit `scope` when the available data cannot support it. When present, use only the properties that are known: `auditObjective`, `sourceAvailability`, `buildStatus`, `reviewFocus`, `targets`, and `reviewBoundaries`.

Give each identified source target a stable `SRC-` ID:

```json
{
  "id": "SRC-001",
  "name": "Application API",
  "repository": "example/application",
  "branch": "audit-snapshot",
  "revision": "0123456789abcdef",
  "includedPaths": ["apps/api/src/**"],
  "excludedPaths": ["generated/**", "vendor/**"],
  "languages": ["TypeScript"],
  "frameworks": ["Node.js"]
}
```

Prefer an immutable commit SHA, archive hash, release tag, or supplied snapshot identifier. A branch name alone is not an immutable boundary. Use `reviewBoundaries` only for concise facts required to interpret results, such as excluded generated code or an unavailable runtime component. Do not turn it into a methodology, activity diary, rules-of-engagement section, or appendix.

## Finding contract

Each finding requires only:

```json
{
  "id": "F-001",
  "title": "Tenant constraint omitted from object lookup",
  "severity": "high"
}
```

Allowed severities are `critical`, `high`, `medium`, `low`, and `informational`. Use stable, unique `F-` IDs. Keep an ID stable across report revisions even if the title or severity changes.

Add optional finding fields only when evidence supports them:

| Field | Purpose |
| --- | --- |
| `confidence` | Evidence confidence: `confirmed`, `high`, `medium`, or `low` |
| `summary`, `description` | Concise result and fuller technical explanation |
| `category`, `tags`, `mappings` | Supported classification and external mappings |
| `affectedTargetRefs` | References to existing `SRC-` targets |
| `affectedComponents` | Paths, symbols, endpoints, packages, or configuration units |
| `reviewBasis` | Short labels for the evidence or analysis basis |
| `codeFlow` | Up to four reader-oriented source/control/sink/impact steps |
| `impact`, `risk` | Supported technical/business impact and calibrated risk detail |
| `preconditions` | Conditions actually required to reach the issue |
| `rootCause` | The underlying control or design failure |
| `securityConsequence` | The supported attack result or security property violation |
| `sourceContexts` | Exact, line-numbered code evidence |
| `supportingArtifacts` | Validation inputs, outputs, traces, logs, or supplied evidence |
| `validation` | Demonstrated steps and expected/observed behavior |
| `remediation` | Corrective guidance and an optional illustrative patch |
| `references` | Directly relevant external references |

Do not add finding status, fixed/not-fixed state, remediation state, owner, ticket, due date, priority, effort, completion percentage, retest status, verification result, or other patch-tracking data. A finding describes the audited condition. Remediation text explains a safe correction; it does not assert that anyone implemented it.

## Code flow

Use `codeFlow` only when a short path makes the issue easier to understand. Use at most four ordered steps, normally:

1. Attacker-controlled source or entry point.
2. Missing or incomplete security control.
3. Security-sensitive sink or observable branch.
4. Supported impact.

Every step must agree with the detailed description and source evidence. A configuration weakness may use equivalent stages, such as configuration source, control gap, response sink, and impact. Omit the flow rather than inventing a stage to complete the sequence.

## Source excerpts and annotations

Each source context requires `path` and a non-empty `lines` array. Provide `language` for highlight.js when known, `symbol` when useful, and `startLine` only when it equals the first numbered line.

```json
{
  "path": "src/api/integrations/get-integration.ts",
  "startLine": 69,
  "language": "typescript",
  "symbol": "getIntegration",
  "lines": [
    {
      "number": 69,
      "state": "source",
      "code": "const integrationId = request.params.integrationId;",
      "annotations": [
        {
          "type": "source",
          "label": "User-controlled key",
          "text": "The route parameter selects the record."
        }
      ]
    },
    {
      "number": 70,
      "state": "vulnerable",
      "code": "const integration = await repository.findById(integrationId);",
      "annotations": [
        {
          "type": "vulnerable",
          "text": "The lookup is not constrained by the authenticated tenant."
        }
      ]
    }
  ]
}
```

Allowed line states are `source`, `vulnerable`, `validation`, and `sink`. Allowed annotation types add `note`. Do not use `fixed`, `patched`, or similar states. Number lines exactly as they appear in the reviewed revision and keep them strictly increasing within an excerpt. Include enough adjacent context to understand the issue, but avoid dumping whole files. Never alter code to make an excerpt look vulnerable.

## Supporting artifacts and validation

Give supporting artifacts stable `EV-` IDs. An artifact records evidence, not a future task. Require `id`, `type`, and `title`; optionally include `description`, `source`, `content`, and a redaction record. Use `source` to distinguish supplied scanner output from reviewer-created validation material.

Use `validation` only for actions or observations that actually occurred:

- `steps` describes the completed or directly reproducible validation path.
- `demonstration` contains a redacted request, command, test, or other concise reproduction input.
- `expectedSecurityBehavior` describes the security property that should hold.
- `observedCodeBehavior` states the supported behavior found in the reviewed code or validation run.

Omit the validation object when none of these are supported. Validation proves or explains the finding; it is not a retest or patch-verification record.

Never include passwords, tokens, private keys, session cookies, customer data, unredacted personal data, or exploitable secrets. Preserve only the minimum content necessary and record redaction when applied.

## Remediation and unified diffs

Remediation may contain `summary`, `steps`, `compensatingControls`, `whyItWorks`, `validationSteps`, `residualRisk`, `references`, and `patch`. These are recommendations. Write them in implementation-neutral terms unless the reviewed code supports a precise change.

A patch is illustrative and must not imply that the repository has been modified. Use a complete unified diff accepted by Diff2Html:

```diff
diff --git a/src/service.ts b/src/service.ts
index 1111111..2222222 100644
--- a/src/service.ts
+++ b/src/service.ts
@@ -10,2 +10,5 @@ function loadRecord(id, tenantId) {
-  return repository.findById(id);
+  return repository.findOne({
+    id,
+    tenantId,
+  });
 }
```

Set `patch.format` to `unified-diff`. Include valid old/new file headers and at least one valid hunk header. Hunk counts must match their body. Use `-` and `+` lines exactly; do not wrap the diff in Markdown inside JSON. `patch.path` is optional metadata and must agree with the diff when supplied. Preserve exact line breaks. Keep the patch narrow enough to explain the control change and do not present speculative surrounding code as exact source.

If a reliable exact patch cannot be formed from available source, omit `patch` and retain supported prose guidance. `remediation.validationSteps` are suggested regression checks, not evidence that a patch was tested.

## References and URL safety

References require `label` and an absolute URL. Prefer authoritative primary sources that directly explain the mapped weakness or control. The renderer allowlists safe URL schemes; the generation workflow must still reject unsafe, credential-bearing, or irrelevant URLs.

## Cross-record invariants

JSON Schema validates shape. The generation script must additionally enforce:

- Unique `SRC-`, `F-`, and `EV-` IDs.
- Every `affectedTargetRefs` value resolves to a supplied target.
- Every `keyFindingRefs` value resolves to a supplied finding.
- Source line numbers are strictly increasing; `startLine`, when present, equals the first line number.
- CVSS version, vector prefix, and score agree when CVSS data is supplied.
- Unified diffs parse, have valid file and hunk headers, and have body counts consistent with hunk headers.
- Real output contains no sample data, placeholder records, unsupported fields, or sensitive secrets.
- Report claims remain attributable to the evidence ledger.

## Conservative publication gate

Before generating a deliverable:

1. Resolve conflicts and request only material user-owned facts, preferably in one consolidated question set after project assets have been inspected.
2. Omit unanswered optional fields and entire unsupported sections or tabs.
3. Re-check every severity, evidence excerpt, observed behavior, target revision, person, date, reference, and remediation claim.
5. Treat the HTML as a draft until a qualified human has reviewed it. Never silently promote the document from `draft` to `final`.

The renderer may calculate counts and severity distributions from canonical findings. Do not duplicate those values in JSON. It must not infer omitted facts, render unsupported placeholders, or manufacture empty sections.
