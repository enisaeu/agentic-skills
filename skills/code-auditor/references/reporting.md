# Security Reporting

Create final reports only from durable, validated candidate artifacts. Use plain language in the aggregate and exact source-backed detail in individual findings.

## Identity and traceability

- Allocate stable finding IDs in reportable-candidate order as `SEVERITY-001`, `SEVERITY-002`, and so on (e.g. CRITICAL-001, HIGH-002).
- Link every aggregate entry to its finding report.
- Link each finding to its `candidates/CAN-NNN.md` analysis and all material source, tool, PoC, fix/patch, test, and cleanup evidence.
- Record UTC time, scope, source-control mode, revision or `nogit`, and the visible model identifier when available.

Never cite chat history as evidence. Use contained artifact paths and exact source `path:line` or symbol references.

## Aggregate report contract

Produce a `Findings.md` with the aggregated findings strictly following the [Findings.md Template](reporting-template.Findings.md) structure and guidance.

For no-findings reviews, keep the only applicable sections, state that no reportable finding was established; do not claim the product is secure.

## Detailed finding contract

For every finding, produce a `SEVERITY-NNN-short-name.md` technical report includes all the technical information needed to understand and remediate the issue, by strictly following the [finding reporting template](reporting-template.SEVERITY-NNN-short-name.md) structure and guidance.

## Report validation

Before closure, verify:

- all required headings exist and no placeholder or generation comment remains;
- severity counts match linked finding files;
- each reportable candidate links to exactly one finding and vice versa;
- every claim has a source or artifact reference;
- tool, PoC, fix/patch, test, and cleanup records are cited/provided where applicable;
- severity, confidence, and effort use the canonical rubrics;
- mappings include rationales and unsupported mappings are omitted;
- proposed and observed evidence are clearly separated;
- limitations and accepted-partial wording match the ledger.
