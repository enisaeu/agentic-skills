---
name: findings-browser-report
description: Create or update a self-contained, static, browser-friendly HTML report from existing code-audit findings and available project evidence.
license: EUPL-1.2
metadata:
  version: "2.0-beta"
  notice: AI tools were used to support the development of this skill.
---

# Generate Findings Browser Report

Produce an evidence-based static HTML report from existing code-audit findings. Inspect the available project before questioning the user, include only supported material, and let unsupported optional sections disappear cleanly.
The agent will have to gather supplied audit results, inspect project assets for corroboration, ask for material missing context, and produce a conservative code-audit findings report with source evidence, syntax-highlighted code, unified diffs, validation evidence, and remediation guidance.

## Establish the operating mode

Treat this skill as reporting-only.

- Start from supplied findings, audit notes, scanner output, tickets, disclosure material, or a completed security review.
- Inspect source code and project artifacts only to locate, corroborate, contextualize, and accurately quote those supplied findings.
- Do not conduct a new repository-wide vulnerability search under this skill.
- If no findings or completed audit results are available and the user actually wants discovery, pause and recommend the appropriate security-scan workflow before generating the report.
- Do not track remediation progress. Exclude fixed/not-fixed state, finding owner, assignee, ticket, due date, implementation status, retest status, remediation effort, and remediation priority.
- Keep remediation guidance and illustrative patches when supported; they explain how to address a finding and do not imply that a patch was implemented.
- Keep validation evidence that demonstrates the reported behavior; do not convert it into fix verification.

Resolve the directory containing this file as the skill root. Read [references/content-contract.md](references/content-contract.md) and [references/report-data.schema.json](references/report-data.schema.json) before assembling report data. Use [assets/report-template.html](assets/report-template.html) as the renderer and `scripts/report.py` as the build and validation entry point.

## Follow the workflow

### 1. Tell the user what information the report can use

Briefly state that you will look for the following categories before asking questions:

- report identity and governance: title, version, report ID, issue date, client or product, provider, classification, authors, and reviewers;
- audit scope: repositories, revisions, components, paths, languages, exclusions, constraints, and build or test context;
- executive context: audit objective, high-level conclusion, business impact, strengths, observations, and prioritized recommendations;
- finding content: stable ID, title, severity, confidence, description, affected targets, preconditions, root cause, impact, and mappings;
- evidence: exact files, revisions, line ranges, excerpts, data flow, logs, requests and responses, commands, traces, test output, or other artifacts;
- remediation: concise guidance, steps, compensating controls, residual risk, and an illustrative unified diff where evidence supports one;
- references: standards, advisories, project documentation, and other relevant sources.

Do not demand every category. The renderer is deliberately adaptive.

### 2. Investigate the available assets

Inventory the project and supplied materials before asking the user to fill gaps. Prefer fast targeted discovery such as `rg --files` and `rg`.

Look for:

- audit notes and reports in Markdown, JSON, HTML, PDF, DOCX, CSV, SARIF, or scanner-specific formats;
- issue exports, vulnerability write-ups, evidence bundles, screenshots, logs, traces, HTTP captures, PoCs, and test results;
- patches, diffs, pull requests, commits, branches, and repository metadata;
- manifests, lockfiles, build files, CI configuration, architecture documentation, and security guidance;
- source locations cited by findings, including the exact revision and surrounding code needed to understand the issue;
- explicit scope, limitations, exclusions, and contributor or reviewer names in the supplied material.

Avoid broad source exploration unrelated to the supplied findings. Never expose secrets found during inspection. Redact tokens, credentials, session material, personal data, and sensitive infrastructure details unless the user explicitly requires them and publication is appropriate.

### 3. Build an evidence ledger

For each prospective claim, record its provenance and publication state:

- **asset-supported**: stated or directly evidenced in supplied/project material;
- **user-supplied**: confirmed by the user but not independently present in project assets;
- **derived**: a narrow, reproducible calculation or summary of supported facts;
- **conflicting**: credible sources disagree;
- **unsupported**: absent or too ambiguous to publish.

Publish asset-supported, user-supplied, and transparent derived claims. Resolve material conflicts through the question gate. Omit unsupported claims and sections. Never turn an inference into a fact merely to make the report look complete.

### 4. Ask one consolidated set of material questions

After asset inspection, decide whether user input would materially change the report. Ask only about:

- user-owned facts that cannot be discovered, such as client-facing names, authors, reviewers, or desired report identity;
- material scope ambiguity, conflicting revisions, or unclear exclusions;
- contradictions that affect severity, impact, evidence, or publication;
- a required output path or naming decision when none is inferable.

Prefer a single concise batch. Mark optional questions as optional. Do not block on cosmetic metadata, people/team credits, an executive narrative, or any other optional field. If the user does not answer, omit the unsupported content.

Do not ask the user for facts already available in the project. Do not ask whether a finding is fixed.

### 5. Assemble canonical report data

Create one JSON document that conforms to the machine-readable report schema.

- Use stable report and finding identifiers. Prefer `F-001`, `F-002`, and so on for findings and `SRC-001`, `SRC-002`, and so on for source contexts.
- Preserve exact technical meaning while writing for both decision-makers and engineers.
- Separate observed evidence from impact analysis and remediation guidance.
- Quote source exactly and keep file paths, revisions, and line ranges consistent with the inspected artifact.
- Use unified-diff syntax for illustrative patches. Never label an illustrative patch as applied, merged, fixed, or verified.
- Make confidence describe confidence in the finding, not remediation state.
- Use `findings: []` only when the known audit result set contains no reportable findings. Do not infer a clean audit merely because findings were not supplied.
- Omit unsupported optional keys instead of writing `null`, empty decorative arrays, placeholders, “TBD,” or “Not provided.”

Follow the field semantics, conditional sections, and examples in [references/content-contract.md](references/content-contract.md). Treat [references/report-data.schema.json](references/report-data.schema.json) as the machine-readable contract.

### 6. Build the static report

Keep canonical JSON separate from the HTML until the build step. Run:

```bash
python scripts/report.py validate report-data.json
python scripts/report.py build report-data.json \
  --template assets/report-template.html \
  --output findings-browser-report.html
```

Keep `scripts/report.py` limited to Python's standard library so the skill remains portable. If a third-party Python package becomes necessary, stop and discuss the available options with the user before adding it.
Use the build command for every deliverable: it removes template-only HTML comments and replaces the preview payload with the validated report data. Do not distribute a copied or manually populated template.

The resulting file must remain self-contained except for the pinned CDN assets already declared by the template. Do not alter Bootstrap, Diff2Html, highlight.js, DOMPurify, their versions, integrity hashes, or their loading order unless the task explicitly requires a dependency update and the new integrity values are independently verified.

Never populate the report by concatenating untrusted strings into markup. Use the builder's safe JSON embedding and the renderer's text-node/sanitized rendering path.

### 7. Validate content and presentation

Run the builder validation again on the final canonical JSON, then inspect the generated HTML.

Verify at minimum:

- no schema, enum, duplicate-ID, broken-reference, line-range, or malformed-diff errors;
- no sample data, placeholder copy, accidental secret, unsupported claim, or tracking field;
- no HTML comments, report-data markers, or template preview payload in the generated report;
- executive counts and severity summaries agree with the finding set;
- omitted data produces no empty card, tab, heading, navigation item, filter, or “Not provided” text;
- rich findings show syntax-highlighted, line-numbered code and red/green Diff2Html patches;
- sparse findings remain readable with only the supported tabs and fields;
- a known zero-finding result renders as a deliberate empty result, not a broken report;
- hostile text is displayed as text, not executed as HTML or script;
- the report remains usable with CDN failure fallbacks, keyboard navigation, print mode, narrow screens, and dark mode;
- report-level draft/confidential markings remain visible when provided.

State clearly that human review is required before external publication. Do not imply the renderer, schema validator, or agent independently proves that every finding is correct.

## Apply conservative publication rules

- Prefer omission over speculation.
- Preserve uncertainty explicitly when it is relevant and supported.
- Do not inflate severity to fill a visual hierarchy.
- Do not invent executive conclusions, business impact, team credits, review dates, revisions, code excerpts, line numbers, commands, test results, or patches.
- Do not silently resolve conflicting sources.
- Do not publish secrets or unsafe reproduction details without a clear need and appropriate audience.
- Do not add methodology, generic appendices, boilerplate disclaimers, or issue-tracking sections.
- Keep the final report focused on what was found, why it matters, the evidence, how it can be addressed, and how the finding itself was validated.

## Deliver the result

Return the generated HTML report and, when useful for future regeneration, its canonical JSON data file. Summarize which optional sections were omitted because they lacked support and identify any unresolved evidence conflict that still requires human attention.
