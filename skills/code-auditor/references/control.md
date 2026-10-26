# Ledger, Artifacts, and Closure

Use durable filesystem state rather than chat history to coordinate, resume, and validate a review.

## Contents

- [Artifact layout](#artifact-layout)
- [Phase ledger](#phase-ledger)
- [State invariants](#state-invariants)
- [Hard errors and completeness gaps](#hard-errors-and-completeness-gaps)
- [Closure check](#closure-check)

## Artifact layout

Use this portable layout:

```text
.security-reviews/<review-id>/
├── Scope.md
├── Findings.md
├── Ledger.md
├── ThreatModel.md
├── files.txt
├── non-reviewable.txt
├── candidates/
│   └── CAN-NNN.md
├── findings/
│   └── SEVERITY-NNN-short-name.md
├── evidence/
│   ├── tools/
│   └── discovery/
├── patches/
└── poc/
```

Keep every path contained below the review directory.

## Phase ledger

Create `Ledger.md` with:

```markdown
# Review Ledger — REVIEW_ID

## Metadata

- Created at: UTC timestamp
- Project root: path
- Confirmed scope: path or paths
- Source-control mode: filesystem | git-aware
- Revision: revision | nogit
- Model: visible identifier | unavailable
- Passes: count
- Worker mode: delegated | sequential

## Phase State

| Phase | Status | Updated UTC | Evidence | Note |
| --- | --- | --- | --- | --- |
| scope | complete | ... | `Scope.md`, `files.txt` | ... |
| tools | pending | | | |
| threats | pending | | | |
| discovery | pending | | | |
| triage | pending | | | |
| remediation | pending | | | |
| reporting | pending | | | |

## Coverage

| Pass | Assignment | Expected paths | Receipt | Deferred paths |
| --- | --- | --- | --- | --- |

## Candidates

| ID | Origins | Disposition | Finding | Analysis | Note |
| --- | --- | --- | --- | --- | --- |

## Tool Runs

| Run | Command record | Result | Evidence |
| --- | --- | --- | --- |

## Specialized Evidence

| Kind | Finding | Plan or transaction | Run, diff, or tests | Cleanup or gap |
| --- | --- | --- | --- | --- |

## Partial Decision

- Decision: undecided | accepted
- Reason:
- Accepted gaps:
- Decided at:

## History

- UTC timestamp — state transition and reason.
```

Allowed phase states are `pending`, `in_progress`, `complete`, `partial`, `skipped`, and `blocked`.
A complete phase needs existing evidence. A skipped tool phase needs a reason.
Partial or blocked phases are gaps even when later analysis can responsibly proceed.

Candidate dispositions are `reportable`, `suppressed`, `not-applicable`, and `deferred`.
Use `open` only transiently before static validation. Give every non-reportable disposition a reason and every candidate a durable analysis path.

## State invariants

- Start later phases only after every earlier phase has a closed, explained state.
- Preserve phase evidence, complete worker results, candidate analyses, and specialized records; do not replace them with ledger summaries.
- Allocate candidate and finding IDs monotonically and never reuse an ID.
- Link every reportable candidate and finding bidirectionally.
- Record changes in history. Any phase, candidate, finding, execution, or fix change invalidates a previous partial acceptance until the current gaps are accepted again.
- On resume, verify artifact existence and consistency before trusting a status.

## Hard errors and completeness gaps

Repair hard errors before closure.

Examples include:

- invalid or missing required report sections;
- unresolved placeholders or generation comments;
- broken or escaping paths;
- missing, duplicate, or unowned coverage rows;
- a complete phase with absent evidence;
- malformed or missing candidate analyses;
- inconsistent dispositions, finding IDs, severity counts, or links;
- uncited tool, PoC, fix, test, or cleanup records;
- source changes outside an approved remediation plan;
- claims of executed or verified behaviour without records.

Treat these as completeness gaps:

- partial or blocked phases;
- deliberately skipped tools;
- deferred files or candidates;
- fewer requested passes or workers;
- sequential rather than independent workers;
- unavailable deployment facts or fixtures;
- no runtime confirmation;
- a fix without runnable tests;
- pending or failed PoC cleanup.

## Closure check

Call a review complete only when:

- every eligible file has an accepted receipt in every configured pass;
- the threat-model contract is complete;
- every raw candidate is accounted for and every merged candidate has a final static disposition and durable analysis;
- every reportable candidate has exactly one detailed report and aggregate entry;
- every phase is complete, except an intentionally skipped tool phase with a reason;
- all counts, links, citations, and artifact paths agree;
- no hard error or completeness gap remains.

If only gaps remain, present the exact list and the evidence-based consequence of each. Resume work where practical. Record partial acceptance only after the user explicitly accepts those current gaps and supplies or confirms a reason. Preserve the reason and gaps in `Ledger.md` and `Findings.md`. Label the result `valid but partial`.

Never convert a hard error into an accepted limitation.
A no-findings review follows the same closure gate.
