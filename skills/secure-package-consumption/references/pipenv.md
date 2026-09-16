---
name: secure-package-consumption-pipenv
description: Pipenv files, commands, sources, and secure Python dependency controls.
license: EUPL-1.2
metadata:
  version: "2.0-beta"
  package_managers: [pipenv]
  ecosystems: [python, pypi]
---

# Pipenv

## Scope

Use for Python projects where `Pipfile` and `Pipfile.lock` define dependencies.

## Files to inspect

- Manifests: `Pipfile`.
- Lockfiles/resolution/vendor files: `Pipfile.lock`.
- Registry/source/proxy/mirror/auth/scope mapping: `[[source]]` entries, pip environment variables, CI pip/Pipenv config.
- SBOM/vulnerability/license files: existing SBOMs, audit outputs, license policy.

## Command safety

- Metadata-only: static reads; `pipenv requirements`; `pipenv graph --json-tree` when it reads existing state only.
- Network/cache-writing: `pip-audit -f json`; `osv-scanner -r .`.
- Project-code-executing: dependency builds from sdists, custom build backends, editable/local/path dependencies, tests.
- Project-mutating: `pipenv install <pkg>==<ver>`; `pipenv uninstall <pkg>`; `pipenv update <pkg>`; `pipenv lock`; `pipenv sync`.
- Lifecycle/build/plugin/native/binary caveats: build backends, VCS/path dependencies, native extensions, binary wheels.

## Selection checks

- Package/source identity: verify `[[source]]` entries, normalized package name, repository URL, and internal index protections.
- Vulnerability/advisory: use pip-audit/OSV and repository alerts when available.
- Provenance/signature/hash/integrity: preserve `Pipfile.lock` hashes; avoid direct URLs/VCS without approval.
- Maintainer/project health/deprecation/ownership: inspect release history, maintainers, project URLs, deprecation, and security policy.
- License: inspect metadata and transitive licenses.
- Transitive impact: review lock diff or graph.
- Confusion risks: multiple sources can cause private/public ambiguity.

## Integration controls

- Pin/lock/reproducible install: commit `Pipfile` and `Pipfile.lock`; use lock-enforced CI sync/install.
- Registry/source enforcement: preserve approved sources and private index mapping.
- Script/native/binary controls: review build backend, VCS/path, native extension, and binary wheel behavior.
- SBOM/vulnerability/license checks: run audit/SBOM/license checks after lock changes.

## Monitor and mitigate

- Outdated/advisory commands or feeds: pip-audit, OSV, Dependabot/equivalent, SBOM scanners.
- Upgrade/patch/remove/rollback/isolate notes: use `pipenv update <pkg>` or edit pins and regenerate lock after approval.
- Approval/block conditions specific to this manager: approve new sources, VCS/path/direct URL deps, opaque build backends, native extensions, and missing lockfile for production; block confusion targets and malicious/lookalike packages.
