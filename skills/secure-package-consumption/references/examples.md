---
name: examples
description: Example secure package consumption decision notes and follow-up actions for common dependency risk scenarios.
license: EUPL-1.2
version: "1.0"
---

# Decision Examples

Use these as patterns, not as fixed outcomes. Real decisions depend on current evidence, available tools, and project policy.

## Safe Dev Dependency

Scenario: Add a mature test-only npm package from the approved registry, exact version, no install scripts, and no high/critical vulnerabilities found by available checks.

```text
Dependency decision: allow with controls
Risk: low
Confidence: high
Evidence status: complete
Package: example-test-lib 1.2.3 (npm, development)
Evidence:
- Approved registry and expected package identity.
- No install scripts and no high/critical advisories found with available checks.
Required controls:
- Pin the exact version and commit package.json with the lockfile.
- Run the project package-manager audit after lockfile update.
Next action: proceed with controls
```

## Suspicious Typo Package

Scenario: Requested package name is one character away from a popular package, has a new maintainer, minimal release history, and a repository URL that does not match the expected project.

```text
Dependency decision: block
Risk: critical
Confidence: high
Evidence status: complete
Package: suspicious-name 0.1.0 (npm, production)
Evidence:
- Name is likely to mislead maintainers into installing the wrong package.
- Package age, maintainer history, and repository URL do not match the expected project.
Required controls:
- None; do not install this package.
Next action: stop
```

## Business-Critical Package With Missing Provenance

Scenario: Production dependency from an approved registry has no provenance in an ecosystem that supports it, has a single maintainer, and will run in a sensitive path.

```text
Dependency decision: needs approval
Risk: high
Confidence: medium
Evidence status: partial
Package: critical-lib 4.5.6 (pypi, production)
Capability limits:
- Registry metadata was available, but maintainer ownership history could not be fully verified.
Evidence:
- Approved registry, but no provenance where supported.
- Single maintainer and sensitive production use.
Required controls:
- Reviewer approval before dependency changes.
- Exact pin or lockfile enforcement, SBOM update, and scheduled advisory monitoring if approved.
Next action: ask approval
```

If asking the user or reviewer is unavailable, stop after this note and state that approval is required.

## Vulnerability Alert With Unclear Reachability

Scenario: Existing production dependency has a high severity advisory. The vulnerable symbol may be reachable, but the call path is not confirmed.

```text
Dependency decision: needs approval
Risk: high
Confidence: low
Evidence status: partial
Package: existing-lib 2.0.0 (maven, production)
Capability limits:
- Reachability is not confirmed with available tools.
Evidence:
- High severity advisory affects the installed version.
- Fixed version exists, but compatibility impact is unknown.
Required controls:
- Upgrade or patch if tests pass.
- Record VEX status as under_investigation until reachability is resolved.
Next action: ask approval
```
