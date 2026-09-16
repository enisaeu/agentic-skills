---
name: secure-package-consumption-mamba
description: Mamba and Micromamba files, commands, channels, lockfiles, and secure environment controls.
license: EUPL-1.2
metadata:
  version: "2.0-beta"
  package_managers: [mamba, micromamba]
  ecosystems: [python, r, conda]
---

# Mamba and Micromamba

## Scope

Use for Mamba or Micromamba environments that consume Conda channels and environment files.

## Files to inspect

- Manifests: `environment.yml`, `environment.yaml`, explicit spec files, `meta.yaml`.
- Lockfiles/resolution/vendor files: `conda-lock.yml`, platform lockfiles, explicit specs.
- Registry/source/proxy/mirror/auth/scope mapping: `.condarc`, channel order, channel priority, private channels, CI config.
- SBOM/vulnerability/license files: SBOMs, scanner outputs, license policy.

## Command safety

- Metadata-only: static reads; `mamba info`; `mamba list --explicit` for existing environments.
- Network/cache-writing: `mamba repoquery search <pkg>`; `mamba repoquery depends <pkg>`; advisory/SBOM scanner lookups; `osv-scanner -r .`.
- Project-code-executing: package install scripts during environment creation/update; build recipes; tests.
- Project-mutating: `mamba install <pkg>=<ver>`; `mamba update <pkg>`; `mamba env update -f environment.yml`; `micromamba install <pkg>=<ver>`; lock/channel edits.
- Lifecycle/build/plugin/native/binary caveats: pre/post-link scripts, compiled packages, solver changes, mixed pip sections.

## Selection checks

- Package/source identity: verify channel, package name, build string/platform, and source recipe when relevant.
- Vulnerability/advisory: use available SBOM/vulnerability scanners and channel/vendor advisories.
- Provenance/signature/hash/integrity: prefer lockfiles with exact builds/hashes when production/CI uses the environment.
- Maintainer/project health/deprecation/ownership: inspect channel trust, package maintenance, and deprecation.
- License: inspect package metadata and transitive licenses.
- Transitive impact: review solver changes and platform-specific dependency expansion.
- Confusion risks: enforce approved channels and strict priority; review `pip:` sections with Python refs.

## Integration controls

- Pin/lock/reproducible install: commit environment file and lockfile/spec together for CI/production.
- Registry/source enforcement: use approved channels and strict channel priority where available.
- Script/native/binary controls: approve packages with install scripts, native libraries, direct URLs, or local paths.
- SBOM/vulnerability/license checks: update SBOM and scan locked environments when tools exist.

## Monitor and mitigate

- Outdated/advisory commands or feeds: channel advisories, SBOM scanners, OSV/Grype where supported, release monitoring.
- Upgrade/patch/remove/rollback/isolate notes: update lock/environment files to fixed builds; remove or isolate vulnerable packages when no fix exists.
- Approval/block conditions specific to this manager: approve unpinned channels, mixed pip/conda resolution, direct URLs/local paths, channel priority changes, and missing lockfiles for production; block unapproved channels and unresolved reachable high/critical issues.
