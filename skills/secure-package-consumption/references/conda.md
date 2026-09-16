---
name: secure-package-consumption-conda
description: Conda files, commands, channels, lockfiles, and secure environment controls.
license: EUPL-1.2
metadata:
  version: "2.0-beta"
  package_managers: [conda]
  ecosystems: [python, r, conda]
---

# Conda

## Scope

Use for Conda-managed environments, including projects that use `environment.yml`, channel policy, or conda-lock.

## Files to inspect

- Manifests: `environment.yml`, `environment.yaml`, explicit spec files, `meta.yaml`.
- Lockfiles/resolution/vendor files: `conda-lock.yml`, platform lockfiles, explicit specs.
- Registry/source/proxy/mirror/auth/scope mapping: `.condarc`, channel order, channel priority, private channels, CI config.
- SBOM/vulnerability/license files: SBOMs, scanner outputs, license policy.

## Command safety

- Metadata-only: static reads; `conda config --show-sources`; `conda list --explicit` for existing environments.
- Network/cache-writing: `conda search <pkg> --info`; advisory/SBOM scanner lookups; `osv-scanner -r .`; `grype sbom:./sbom.json`.
- Project-code-executing: package install scripts during environment creation/update; build recipes; tests.
- Project-mutating: `conda install <pkg>=<ver>`; `conda update <pkg>`; `conda env update -f environment.yml`; `conda-lock lock`; environment/lock/channel edits.
- Lifecycle/build/plugin/native/binary caveats: pre/post-link scripts, compiled packages, solver changes, mixed pip sections.

## Selection checks

- Package/source identity: verify channel, package name, build string/platform, and source recipe when relevant.
- Vulnerability/advisory: use available SBOM/vulnerability scanners and channel/vendor advisories.
- Provenance/signature/hash/integrity: prefer lockfiles with exact builds/hashes when production/CI uses the environment.
- Maintainer/project health/deprecation/ownership: inspect channel trust, package maintenance, and deprecation.
- License: inspect conda package metadata and transitive licenses.
- Transitive impact: review solver changes and platform-specific dependency expansion.
- Confusion risks: enforce approved channels and strict priority; review `pip:` sections separately with Python refs.

## Integration controls

- Pin/lock/reproducible install: commit environment file and lockfile/spec together for CI/production.
- Registry/source enforcement: use approved channels and strict channel priority where available.
- Script/native/binary controls: approve packages with install scripts, native libraries, direct URLs, or local paths.
- SBOM/vulnerability/license checks: update SBOM and scan locked environments when tools exist.

## Monitor and mitigate

- Outdated/advisory commands or feeds: channel advisories, SBOM scanners, OSV/Grype where supported, release monitoring.
- Upgrade/patch/remove/rollback/isolate notes: update lock/environment files to fixed builds; remove or isolate vulnerable packages when no fix exists.
- Approval/block conditions specific to this manager: approve unpinned channels, mixed pip/conda resolution, direct URLs/local paths, channel priority changes, and missing lockfiles for production; block unapproved channels and unresolved reachable high/critical issues.
