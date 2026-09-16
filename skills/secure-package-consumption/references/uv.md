---
name: secure-package-consumption-uv
description: uv files, commands, sources, and secure Python dependency controls.
license: EUPL-1.2
metadata:
  version: "2.0-beta"
  package_managers: [uv]
  ecosystems: [python, pypi]
---

# uv

## Scope

Use for Python projects managed by uv, including `uv.lock`, `pyproject.toml`, and uv pip compatibility workflows.

## Files to inspect

- Manifests: `pyproject.toml`, requirements files when uv pip is used.
- Lockfiles/resolution/vendor files: `uv.lock`, generated requirements or constraints.
- Registry/source/proxy/mirror/auth/scope mapping: uv source/index settings, pip config, environment variables, CI config.
- SBOM/vulnerability/license files: existing SBOMs, audit outputs, license policy.

## Command safety

- Metadata-only: static reads; `uv pip list`; `uv pip tree`.
- Network/cache-writing: `uv lock --check`; `pip-audit -f json`; `osv-scanner -r .`.
- Project-code-executing: dependency builds from sdists, custom build backends, editable/local/path dependencies, tests.
- Project-mutating: `uv add <pkg>==<ver>`; `uv remove <pkg>`; `uv lock`; `uv sync`; `uv pip install <pkg>==<ver>`; generated requirements edits.
- Lifecycle/build/plugin/native/binary caveats: build backends, VCS/path dependencies, native extensions, binary wheels, Python executable management.

## Selection checks

- Package/source identity: verify indexes/sources, normalized package name, repository URL, and internal index protections.
- Vulnerability/advisory: use pip-audit/OSV and repository alerts when available.
- Provenance/signature/hash/integrity: preserve `uv.lock` hashes; avoid direct URLs/VCS without approval.
- Maintainer/project health/deprecation/ownership: inspect release cadence, maintainers, project URLs, deprecation, and security policy.
- License: inspect metadata and transitive licenses.
- Transitive impact: review `uv.lock` diff or `uv pip tree`.
- Confusion risks: multiple indexes and extra indexes can cause private/public ambiguity.

## Integration controls

- Pin/lock/reproducible install: commit `pyproject.toml` and `uv.lock`; use locked/frozen CI sync where supported.
- Registry/source enforcement: preserve approved indexes and private source mapping.
- Script/native/binary controls: review build backend, VCS/path, native extension, and binary wheel behavior.
- SBOM/vulnerability/license checks: run audit/SBOM/license checks after lock changes.

## Monitor and mitigate

- Outdated/advisory commands or feeds: pip-audit, OSV, Dependabot/equivalent, SBOM scanners.
- Upgrade/patch/remove/rollback/isolate notes: use `uv add <pkg>==<fixed>` or adjust constraints and regenerate lock after approval.
- Approval/block conditions specific to this manager: approve new sources, VCS/path/direct URL deps, opaque build backends, native extensions, Python/runtime changes, and missing lockfile for production; block confusion targets and malicious/lookalike packages.
