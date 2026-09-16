---
name: secure-package-consumption-renv
description: renv files, commands, repositories, lockfiles, and secure R dependency controls.
license: EUPL-1.2
metadata:
  version: "2.0-beta"
  package_managers: [renv]
  ecosystems: [r, cran]
---

# renv

## Scope

Use for R projects where `renv.lock` and renv settings manage reproducibility.

## Files to inspect

- Manifests: `DESCRIPTION`, `NAMESPACE`, project R dependency declarations.
- Lockfiles/resolution/vendor files: `renv.lock`, `renv/library` metadata when already present.
- Workspace files: `renv/settings.json`, `.Rprofile`, `renv/activate.R`.
- Registry/source/proxy/mirror/auth/scope mapping: repository settings in `renv.lock`, Posit Package Manager, Bioconductor, private repos, CI R config.
- SBOM/vulnerability/license files: SBOMs, scanner outputs, license policy.

## Command safety

- Metadata-only: static reads of `renv.lock` and settings; use `R --vanilla` when possible.
- Network/cache-writing: repository metadata lookups; `osv-scanner -r .`; SBOM scanner lookups.
- Project-code-executing: `renv` operations that evaluate project startup files or install/build packages; package configure/build/test hooks.
- Project-mutating: `R --vanilla -q -e 'renv::install("<pkg>@<ver>")'`; `R --vanilla -q -e 'renv::snapshot()'`; `R --vanilla -q -e 'renv::restore()'`; lock/settings edits.
- Lifecycle/build/plugin/native/binary caveats: configure scripts, compiled code, GitHub/remotes, binary packages, project `.Rprofile` effects.

## Selection checks

- Package/source identity: verify package name, recorded repository/source, maintainer, and project URL.
- Vulnerability/advisory: use OSV/SBOM scanners and vendor/repository advisories when available.
- Provenance/signature/hash/integrity: preserve `renv.lock` package source records and hashes where present.
- Maintainer/project health/deprecation/ownership: inspect CRAN/archive status, release cadence, maintainer, and repository activity.
- License: inspect DESCRIPTION/license metadata and transitive licenses.
- Transitive impact: review lock diff and dependency declarations.
- Confusion risks: review repository order, GitHub/remotes, and private packages.

## Integration controls

- Pin/lock/reproducible install: commit `renv.lock` with manifest changes; use project-approved repository snapshots.
- Registry/source enforcement: preserve approved repositories and snapshot URLs.
- Script/native/binary controls: approve configure scripts, compiled code, remotes, and unknown binary sources.
- SBOM/vulnerability/license checks: run SBOM/advisory/license checks after lock changes.

## Monitor and mitigate

- Outdated/advisory commands or feeds: repository status, OSV/SBOM scanners, release monitoring, GitHub advisories where available.
- Upgrade/patch/remove/rollback/isolate notes: update lockfile to fixed version/snapshot; restore prior lockfile to roll back.
- Approval/block conditions specific to this manager: approve GitHub/remotes, unknown binaries, configure scripts, repository changes, and missing lockfile for production; block malicious/lookalike packages and unresolved reachable high/critical issues.
