# Selected-Finding Remediation

Require an existing validated review. Recheck source when it differs from the reviewed state. Work only on the selected root causes and preserve unrelated user changes.

## Default report-only mode

1. Identify the failed root control and every equivalent affected entry point.
2. Design the smallest safe containment and the correct long-term fix.
3. Create a concrete proposed diff or patch under `patches/SEVERITY-NNN/` without changing product source.
4. Specify tests for the vulnerable path, intended allowed path, relevant variants, and not-applicable configurations.
5. Analyse compatibility, migration, rollout, monitoring, and residual risk.

Do not edit source merely because the user asked how to fix a finding. Require an explicit request to apply changes. Do not apply changes and stay in report-only mode when conducting a full code audit.

## Apply mode

If the runtime cannot present and record a bounded plan approval, stay in report-only mode and reject source application.

1. Inspect existing source changes without assuming Git. Preserve them and use Git only when explicitly requested.
2. Present a bounded plan listing selected findings, exact source paths, intended changes, test commands, expected writes, and rollback approach. Obtain approval.
3. Snapshot the approved paths and relevant file inventory before editing.
4. Apply only changes required for the selected findings; do not mix refactoring or cleanup.
5. Run the narrowest relevant tests first and broader existing tests when practical.
6. Record each exact argument vector, working directory, exit code, stdout, stderr, and result.
7. Compare the final changes with the snapshot. Reject changes outside approved paths, no-op fixes, failing tests, or incomplete verification.
8. If no responsible test can run, record the exact reason. Describe the result as verified-without-tests or unverified, never fully verified.
9. If verification fails, preserve the evidence and report the failure. Do not hide it or destructively reset unrelated work.

A material path, design, test, or side-effect change requires renewed approval.

## Verification matrix

Cover, where applicable:

| Case | Required result |
| --- | --- |
| Previously vulnerable path | Blocked by the restored root control |
| Intended allowed path | Still succeeds |
| Sibling entry points or providers | Enforce the same boundary |
| Malformed and boundary inputs | Fail safely and consistently |
| Not-applicable configuration | Remains correctly classified |
| Operational behaviour | Produces useful audit or detection evidence |

## Fix and hardening addendum

Append, never replace, an addendum to every selected finding:

```markdown
## Fix And Hardening Addendum

**Mode:** report-only | applied

**Finding:** SEVERITY-NNN

#### Root Control And Remediation Design

#### Changed Or Proposed Files

#### Transaction And Diff Evidence

#### Verification

#### Compatibility Rollout And Monitoring

#### Systemic Hardening And Remaining Risk
```

Reference the proposed patch or final diff, snapshot or transaction record, every test result, and any explicit test gap. Update aggregate triage and the remediation roadmap. Rerun report and ledger validation before claiming success.
