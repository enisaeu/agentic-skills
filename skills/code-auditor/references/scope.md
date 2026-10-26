# Scope and Preparation

Resolve scope before substantive security analysis. Treat the confirmed file inventory as the coverage source of truth.

## Procedure

1. Identify the project root and the exact requested path or paths.
2. Enumerate files directly from the filesystem. Do not invoke Git by default.
3. Identify product areas, languages, manifests, entry points, privileged components, configuration, tests, infrastructure, deployment files, generated output, vendored code, binaries, and unreadable files.
4. Exclude only source-control metadata and the active audit-output directory by default, normally `.git/**` and `.security-reviews/**`.
5. Propose every other exclusion. Explain the security tradeoff before excluding generated, vendored, test, example, migration, infrastructure, or deployment code.
6. Record binary, non-text, oversized, missing, or unreadable files as non-reviewable inventory; do not hide them as ordinary exclusions.
7. Treat an explicit user path as authoritative. Read adjacent dependencies when necessary for cross-file reasoning, but do not silently claim coverage outside the confirmed scope.
8. If scope was omitted or is ambiguous, present the proposed scope, exact exclusions, non-reviewable inventory, and supporting files, then wait for confirmation before creating a review directory.
9. If Git-aware operation was explicitly requested, record the enumeration mode, revision, and working-tree state. Keep every later phase functional without Git.
10. State that the review assumes scoped source remains stable. If material changes occur, restart or reassess the affected file coverage.

Do not read credential stores, private keys, production data, `.env` files, or equivalent secret material merely to inventory them.
Record their presence and sensitivity.
Inspect contents only when necessary to the authorized question and without reproducing secret values.

## Review identity and output

Use a collision-resistant UTC review ID such as `YYYYMMDDTHHMMSSZ-nogit`; replace `nogit` with a short revision only in explicitly Git-aware operation.
Put artifacts under `.security-reviews/<review-id>/` unless the user selected another contained output directory.

## `Scope.md` contract

Record:

- project root and confirmed scope;
- UTC review ID and creation time;
- source-control mode and revision or `nogit`;
- source-stability assumption;
- included capabilities and paths;
- exact applied exclusions with rationale and approval source;
- eligible text-file count and canonical inventory path;
- binary/non-reviewable and missing/unreadable inventory;
- supporting files read outside scope without claiming them as covered;
- unresolved scope limitations.

## Exit gate

Close the phase only when:

- the scope is explicit and, when needed, confirmed;
- every enumerated path is eligible, excluded with rationale, or non-reviewable with reason;
- the output directory cannot recursively enter its own scope;
- source-control and source-stability assumptions are recorded; and
- the eligible inventory is non-empty.
