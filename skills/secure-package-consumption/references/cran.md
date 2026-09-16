---
name: secure-package-consumption-cran
description: CRAN-style R package repositories, files, commands, mirrors, native code, and secure dependency controls.
license: EUPL-1.2
metadata:
  version: "2.0-beta"
  package_managers: [cran, r]
  ecosystems: [r, cran]
---

# R and CRAN

## Scope

Use for R projects using CRAN-style repositories, Posit Package Manager, Bioconductor packages, or direct R package installs. Use `renv.md` when `renv.lock` owns reproducibility.

## Files to inspect

- Manifests: `DESCRIPTION`, `NAMESPACE`, `install.R`.
- Lockfiles/resolution/vendor files: `renv.lock` when present.
- Workspace files: `.Rprofile`, `renv/settings.json`.
- Registry/source/proxy/mirror/auth/scope mapping: R `repos` options, Posit Package Manager, Bioconductor repository config, CI R config.
- SBOM/vulnerability/license files: SBOMs, scanner outputs, license policy.

## Command safety

- Metadata-only: static reads; use `R --vanilla` for local metadata commands to avoid `.Rprofile` side effects.
- Network/cache-writing: `R --vanilla -q -e 'available.packages()["<pkg>", ]'`; `R --vanilla -q -e 'tools::CRAN_package_db()[tools::CRAN_package_db()$Package == "<pkg>", ]'`; `osv-scanner -r .`.
- Project-code-executing: package build/check, configure scripts, install hooks, `.Rprofile` startup, vignettes/tests.
- Project-mutating: `install.packages("<pkg>")`; Bioconductor install commands; `renv::install("<pkg>@<ver>")`; `renv::restore()`; `renv::snapshot()`; repository/config edits.
- Lifecycle/build/plugin/native/binary caveats: source package configure scripts, compiled code, binary packages, GitHub/remotes dependencies.

## Selection checks

- Package/source identity: verify package name, repository/mirror, maintainer, project URL, and expected ecosystem.
- Vulnerability/advisory: use osv-scanner/SBOM scanners and vendor/repository advisories when available.
- Provenance/signature/hash/integrity: prefer reproducible repository snapshots and lockfiles when production/CI depends on them.
- Maintainer/project health/deprecation/ownership: inspect CRAN status, archive status, release cadence, maintainer, and repository activity.
- License: inspect DESCRIPTION license and transitive licenses.
- Transitive impact: review Depends/Imports/LinkingTo and system requirements.
- Confusion risks: review repository order, GitHub/remotes, and private package names.

## Integration controls

- Pin/lock/reproducible install: use renv/Posit Package Manager snapshots for production when available.
- Registry/source enforcement: preserve approved CRAN/Posit/Bioconductor/internal repositories.
- Script/native/binary controls: approve configure scripts, compiled code, GitHub/remotes, and unknown binary sources.
- SBOM/vulnerability/license checks: run SBOM/advisory/license checks after lock or repository changes.

## Monitor and mitigate

- Outdated/advisory commands or feeds: repository status, osv-scanner/SBOM scanners, release monitoring, GitHub advisories where available.
- Upgrade/patch/remove/rollback/isolate notes: update to fixed package version or repository snapshot; remove/replace archived vulnerable packages.
- Approval/block conditions specific to this manager: approve GitHub/remotes, unknown binaries, configure scripts, repository changes, and missing lock/snapshot for production; block malicious/lookalike packages and unresolved reachable high/critical issues.
