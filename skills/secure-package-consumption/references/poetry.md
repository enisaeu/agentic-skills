---
name: secure-package-consumption-poetry
description: Poetry files, commands, sources, and secure Python dependency controls.
license: EUPL-1.2
metadata:
  version: "2.0-beta"
  package_managers: [poetry]
  ecosystems: [python, pypi]
---

# Poetry

## Scope

Use for Python projects where `pyproject.toml` and `poetry.lock` define dependencies.

## Files to inspect

- Manifests: `pyproject.toml` Poetry sections.
- Lockfiles/resolution/vendor files: `poetry.lock`.
- Registry/source/proxy/mirror/auth/scope mapping: Poetry `source` entries, `poetry.toml`, CI Poetry config.
- SBOM/vulnerability/license files: existing SBOMs, audit outputs, license policy.

## Command safety

- Metadata-only: static reads; `poetry show --tree` when it reads the existing lock/environment only.
- Network/cache-writing: `poetry search <pkg>`; `poetry show <pkg> --latest`; `pip-audit -f json`; `osv-scanner -r .`.
- Project-code-executing: dependency builds from sdists, custom build backends, editable/local/path dependencies, tests.
- Project-mutating: `poetry add <pkg>@<ver>`; `poetry remove <pkg>`; `poetry update <pkg>`; `poetry lock`; `poetry install`; source config edits.
- Lifecycle/build/plugin/native/binary caveats: build backends, Poetry plugins, path/VCS dependencies, compiled extensions, binary wheels.

## Selection checks

- Package/source identity: verify Poetry source priority, normalized name, repository URL, and internal index protections.
- Vulnerability/advisory: use pip-audit/OSV and repository alerts when available.
- Provenance/signature/hash/integrity: preserve `poetry.lock` hashes; avoid direct URLs/VCS without approval.
- Maintainer/project health/deprecation/ownership: inspect release cadence, maintainers, project URLs, deprecation, and security policy.
- License: inspect metadata and transitive licenses.
- Transitive impact: use lock diff or tree to assess dependency expansion.
- Confusion risks: source priority and multiple indexes can cause private/public ambiguity.

## Integration controls

- Pin/lock/reproducible install: commit `pyproject.toml` and `poetry.lock`; use lock-enforced CI installs.
- Registry/source enforcement: preserve approved Poetry sources and private index mapping.
- Script/native/binary controls: review build backends, VCS/path dependencies, native extensions, and plugin behavior.
- SBOM/vulnerability/license checks: run audit/SBOM/license checks after lock changes.

## Monitor and mitigate

- Outdated/advisory commands or feeds: `poetry show --outdated`, pip-audit, OSV, Dependabot/equivalent, SBOM scanners.
- Upgrade/patch/remove/rollback/isolate notes: use `poetry update <pkg>` or pin fixed versions in `pyproject.toml` and regenerate the lockfile after approval.
- Approval/block conditions specific to this manager: approve new sources, source-priority changes, VCS/path/direct URL deps, opaque build backends, native extensions, and missing lockfile for production; block confusion targets and malicious/lookalike packages.
