---
name: secure-package-consumption-pip
description: pip and requirements-file controls for secure Python dependency use.
license: EUPL-1.2
metadata:
  version: "2.0-beta"
  package_managers: [pip]
  ecosystems: [python, pypi]
---

# pip

## Scope

Use for pip-managed projects using requirements files, constraints, `pyproject.toml`, or setup metadata without Poetry/Pipenv/uv as the primary manager.

## Files to inspect

- Manifests: `requirements*.txt`, `constraints*.txt`, `pyproject.toml`, `setup.cfg`, `setup.py`.
- Lockfiles/resolution/vendor files: hash-pinned requirements, generated lock files, vendored wheels.
- Registry/source/proxy/mirror/auth/scope mapping: `pip.conf`, `pip.ini`, `PIP_INDEX_URL`, `PIP_EXTRA_INDEX_URL`, CI pip config.
- SBOM/vulnerability/license files: existing SBOMs, `pip-audit` outputs, license policy.

## Command safety

- Metadata-only: static reads; `python -m pip inspect --local`; `python -m pip list --format json` for installed environment only; `pipdeptree --json-tree`.
- Network/cache-writing: `python -m pip index versions <pkg>`; `pip-audit -r requirements.txt -f json`; `pip-audit -f json`; `osv-scanner -r .`.
- Project-code-executing: builds from sdist, PEP 517 build backends, `setup.py`, editable installs, tests.
- Project-mutating: `python -m pip install <pkg>==<ver>`; `python -m pip uninstall <pkg>`; lock/requirements rewrites; environment sync commands.
- Lifecycle/build/plugin/native/binary caveats: build backends, custom setup code, compiled extensions, binary wheels, post-install data downloads.

## Selection checks

- Package/source identity: verify PyPI/internal index source, normalized package name, repository URL, and index configuration.
- Vulnerability/advisory: use pip-audit, OSV, NVD/vendor advisories when available.
- Provenance/signature/hash/integrity: prefer hashes with `--require-hashes` when the project uses them; avoid direct URLs without approval.
- Maintainer/project health/deprecation/ownership: inspect release history, maintainers/project URLs, security policy, and deprecation.
- License: inspect package metadata and transitive license policy.
- Transitive impact: review requirements/lock impact; avoid broad dependency trees for small utilities.
- Confusion risks: treat `extra-index-url` as dependency-confusion risk unless private names are protected.

## Integration controls

- Pin/lock/reproducible install: use exact pins or approved lock workflow; preserve hash-pinned requirements.
- Registry/source enforcement: prefer one approved index or explicit internal/private index controls.
- Script/native/binary controls: inspect sdists/build metadata; prefer trusted wheels only when source and publisher are acceptable.
- SBOM/vulnerability/license checks: run pip-audit/OSV/license/SBOM checks after changes.

## Monitor and mitigate

- Outdated/advisory commands or feeds: `pip-audit`, OSV, Dependabot/equivalent, SBOM scanners, package release feeds.
- Upgrade/patch/remove/rollback/isolate notes: update exact pins to fixed versions; remove/replace abandoned vulnerable packages.
- Approval/block conditions specific to this manager: approve direct URLs, VCS/path installs, custom indexes, `extra-index-url`, build backends with opaque behavior, native extensions in production, and missing hashes where policy requires them; block dependency-confusion targets and unresolved reachable high/critical vulnerabilities.
