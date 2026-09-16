---
name: secure-package-consumption-other-ecosystems
description: Generic secure package-consumption workflow when no exact manager reference exists.
license: EUPL-1.2
metadata:
  version: "2.0-beta"
  package_managers: [any]
  ecosystems: [any]
---

# Other Package Managers

## Scope

Use only when no exact manager or ecosystem-family reference applies.

## Files to inspect

- Manifests, lockfiles/resolution files, vendor directories, registry/source/mirror/proxy/auth config, CI install steps, SBOMs, vulnerability and license policy files.

## Command safety

- Metadata-only: static file inspection and local config reads.
- Network/cache-writing: registry, advisory, package metadata, and repository lookups.
- Project-code-executing: commands that evaluate manifests, build scripts, plugins, hooks, generated code, tests, or source code.
- Project-mutating: commands that install, add, update, remove, resolve, restore, vendor, rewrite lockfiles, change source config, or update SBOMs.

## Selection checks

- Verify need, source identity, approved registry, vulnerability status, provenance/signature/hash support, maintainer health, license, transitive impact, scripts/hooks, native/binary behavior, and confusion risk.

## Integration controls

- Pin exact versions or commit resolution files with checksums.
- Enforce approved registries/mirrors/proxies and source priority.
- Disable or restrict install/build hooks when supported.
- Update SBOM and vulnerability/license scans for production when tools exist.

## Post-change verification and evidence

- After an allowed change, verify the resolved package state, source/integrity controls, relevant vulnerability/license results, and project tests/builds where applicable and permitted.
- Record checks performed, checks that failed, checks that were unavailable or not attempted, changed artefacts, approvals, and residual concerns.

## Monitor and mitigate

- Use available advisory feeds, SBOM correlation, and outdated/deprecation/ownership monitoring.
- Require approval when lockfile, checksum, source mapping, or advisory support is weak for production/sensitive use.
- Require approval for unresolved high/critical vulnerabilities or other material security findings unless project policy defines a stricter outcome.
- Block malicious packages, confusion targets, policy-forbidden sources, failed integrity checks, and other policy-defined hard-stop conditions.
