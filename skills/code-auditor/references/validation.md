# Candidate Merge, Triage, and Static Validation

Begin only after independent discovery closes. Add private tool candidates at this point.
Validate from source and configuration evidence; do not execute proposed payloads or start a target.

## Merge without losing provenance

Merge candidates only when all of these match:

- root cause;
- failed control;
- reachable vulnerable instance;
- security outcome.

Preserve distinct entry points or independently reachable instances even when their CWE is the same. Retain every worker and tool origin on the surviving analysis. Never delete suppressed, not-applicable, or deferred candidates.

## Validate each candidate

1. Reconstruct the complete path from attacker-controlled source to sensitive operation, including wrappers, transformations, and shared controls.
2. Determine whether validation, authorization, canonicalization, isolation, or state enforcement blocks the path.
3. Establish minimum attacker capability, required feature or configuration, required user interaction, and environmental assumptions.
4. Prove the outcome, assets affected, blast radius, and source-backed limits on chaining.
5. Search sibling entry points and equivalent control sites to distinguish one instance from a systemic root cause.
6. State expected vulnerable, fixed, and not-applicable results. Label all steps as proposed unless execution evidence exists.
7. Assign one disposition:
   - `reportable`: source evidence establishes a plausible exploitable boundary failure;
   - `suppressed`: evidence disproves reachability, attacker control, control failure, or security impact;
   - `not-applicable`: the surface is intentionally trusted or outside the confirmed deployment or scope;
   - `deferred`: a named runtime fixture or missing component is required to resolve the claim.
8. Assign severity and confidence separately using the rating reference.
9. Map CWE to the root cause, not only the symptom. Add OWASP, CAPEC, or MITRE mappings only when the relationship is direct and explain why it applies.

Severity must reflect demonstrated impact and preconditions. Confidence must reflect evidence quality. Do not lower severity merely because confidence is low.

## Durable candidate analysis

Allocate `CAN-001`, `CAN-002`, and so on in stable merged-candidate order. Create `candidates/CAN-NNN.md` for every disposition with this complete shape:

```markdown
# CAN-NNN: concise title

**Origins:** worker or tool references

**Disposition:** reportable | suppressed | not-applicable | deferred

## Security Boundary

## Attacker-Controlled Source

## Reachability And Transformations

1. Source and entry point.
2. Parsing, transformation, or canonicalization.
3. Validation, authorization, or isolation control.
4. Security-sensitive sink or privileged effect.

## Existing Controls And Bypass

## Security Outcome And Blast Radius

## Affected Conditions

### Applies When

### Does Not Apply When

## Evidence

| Reference | Claim Supported |
| --- | --- |

## Proof Gaps

## Validation Summary

- **Severity:** canonical label or unassigned
- **Confidence:** canonical label and rationale
- **Root Cause / CWE:** mapping or explicit no-mapping rationale
- **Expected Vulnerable Result:** ...
- **Expected Fixed Result:** ...
- **Expected Not-Applicable Result:** ...
```

Give suppressed, not-applicable, and deferred dispositions an exact reason. Update the whole artifact when a title or disposition changes; a ledger row is not a substitute for reasoning.

## Exit gate

Close triage only after all raw candidates are merged and registered. Close static validation only after every merged candidate has a complete artifact and final disposition.
Treat `deferred` candidates and remaining runtime-dependent questions as gaps and route selected runtime work through the exploit-analysis stage.
