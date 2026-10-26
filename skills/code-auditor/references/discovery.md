# Independent Candidate Discovery

Run full-file coverage passes independently from repository-native tool output and prior candidate conclusions.

## Pass design

Default to three passes:

1. **Attack surface and data flow:** trust boundaries, untrusted sources, parsing, validation/canonicalization, and security-sensitive sinks.
2. **Identity and state:** authentication, authorization, isolation, state transitions, business logic, workflow bypasses, confused deputies, and concurrency.
3. **Platform and chaining:** configuration, secrets, cryptography, dependencies, serialization, filesystem/process/network boundaries, resource or memory safety, and cross-component chains.

For an additional pass, choose a fresh adversarial lens from unresolved threat-model frontiers and record it before assigning files. Each pass must account for every eligible file; risk sampling is not full coverage.

## Partition and dispatch

- Partition the canonical inventory deterministically and keep assignments disjoint within a pass.
- Use up to six (unless specified) workers when supported, bounded by requested capacity and scope size. Never require delegation for correctness.
- Give a worker only the confirmed scope, its assigned paths, the pass lens, necessary threat-model facts, and the output contract below.
- Do not reveal tool output, previous-pass candidates, or another worker's conclusions.
- Require the worker to read each assigned eligible file completely enough to issue a receipt.
- Prohibit source edits, payload execution, service startup, external requests, and nested delegation.

When delegation is unavailable, process the same deterministic assignments sequentially. Keep pass notes separate, postpone merge decisions, and record that worker independence was not available.

## Candidate evidence threshold

Keep a candidate only when it identifies:

- the security boundary and intended control;
- the minimum attacker position and attacker-controlled source;
- parsing, transformations, canonicalization, validation, authorization, or isolation along the path;
- the reachable sensitive sink or privileged effect;
- a concrete outcome and source-backed blast radius;
- affected and not-affected conditions;
- exact source paths, symbols, and line references;
- a preliminary root-cause category and explicit proof gaps.

Do not infer exploitability from a dangerous function name. Do not turn hardening advice into a vulnerability without a concrete attacker outcome. Record meaningful negative results for high-risk surfaces where controls hold.

## Complete assignment result

Require one self-contained Markdown result in this shape:

```markdown
# Pass N Result — worker-NN

## Coverage

| Path | Status | Notes |
| --- | --- | --- |
| `relative/path` | reviewed | Surface checked and concise outcome. |

## Candidates

### Candidate — concise title

- Security boundary and intended control: ...
- Attacker-controlled source and minimum position: ...
- Reachability, transformations, controls, and sink: ...
- Outcome, blast radius, affected conditions, and proof gaps: ...
- Evidence: `path:line` and symbol references.

## Negative Results

- High-risk surface checked, control observed, and why no candidate remains.
```

If no candidate remains, write `No security candidates were identified.` under `## Candidates`. Do not omit any top-level section.

Allowed coverage states are:

- `reviewed`: security-relevant behaviour was examined;
- `not-applicable`: the file contains no reviewable behaviour for this pass, with a reason;
- `deferred`: a concrete unreadable format, missing dependency, or unresolved cross-file question prevents a receipt, with the exact reason.

## Register receipts

Save the entire assignment result below `evidence/discovery/pass-N/`; never reconstruct only its coverage table. Verify that:

- every assigned path appears exactly once;
- no unassigned path appears;
- every status is allowed;
- every deferred row has a reason;
- candidate and negative-result sections are intact.

Close discovery only after every assignment in every pass has a valid receipt. Treat deferred files, missing results, reduced requested capacity, and incomplete pass coverage as explicit gaps.
