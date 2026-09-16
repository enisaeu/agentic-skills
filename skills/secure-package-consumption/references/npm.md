---
name: secure-package-consumption-npm
description: npm files, commands, registry controls, and secure integration checks for secure package consumptions
license: EUPL-1.2
metadata:
  version: "2.0-beta"
  package_managers: [npm]
  ecosystems: [javascript, typescript, node]
---

# npm

## Scope

Use for npm projects using the npm registry, private npm registries, or npm workspaces.

## Files to inspect

- Manifests: `package.json`, workspace `package.json` files.
- Lockfiles/resolution/vendor files: `package-lock.json`, `npm-shrinkwrap.json`, `node_modules` metadata when already present.
- Registry/source/proxy/mirror/auth/scope mapping: `.npmrc`, `publishConfig`, `packageManager`, CI npm config.
- SBOM/vulnerability/license files: existing SBOMs, audit outputs, dependency-review config.

## Command safety

- Metadata-only: static reads; `npm config get registry`; `npm pkg get <field>`; `npm ls --all --json` when reading existing project state.
- Network/cache-writing: `npm view <pkg> --json`; `npm view <pkg>@<ver> --json`; `npm view <pkg> deprecated`; `npm view <pkg> license`; `npm view <pkg> maintainers --json`; `npm view <pkg> time --json`; `npm view <pkg> scripts --json`; `npm audit --json`; `npm outdated --json`; `osv-scanner -r .`.
- Project-code-executing: lifecycle scripts during install/rebuild; `npm run <script>`; build/test commands.
- Project-mutating: `npm install`; `npm install --save-exact <pkg>@<ver>`; `npm uninstall <pkg>`; `npm update <pkg>`; `npm ci`; `npm rebuild`; lockfile or `.npmrc` edits.
- Lifecycle/build/plugin/native/binary caveats: preinstall/install/postinstall/prepare scripts, native addons, downloaded binaries, credential or profile changes.

## Selection checks

- Package/source identity: verify package name, scope owner, registry, repository URL, and `.npmrc` scope mapping.
- Vulnerability/advisory: use npm audit, OSV, and project advisory feeds when available.
- Provenance/signature/hash/integrity: check lockfile `integrity`; use provenance or `npm audit signatures` when project policy expects it.
- Maintainer/project health/deprecation/ownership: inspect maintainers, publisher, time data, deprecation, repo activity, and ownership changes.
- License: inspect package metadata and project license policy.
- Transitive impact: inspect lockfile/audit tree; avoid large trees for small features.
- Confusion risks: check private scopes, unscoped internal names, lookalikes, and AI-suggested names.

## Integration controls

- Pin/lock/reproducible install: commit `package.json` with exactly one npm lockfile; prefer `npm ci` in CI; use `--save-exact` when policy requires exact direct versions.
- Registry/source enforcement: preserve approved `.npmrc` registry and scope mappings.
- Script/native/binary controls: inspect lifecycle scripts before adoption. Where lifecycle scripts are not required, use `--ignore-scripts`, `ignore-scripts=true`, or equivalent project controls when compatible. Where scripts are required, review and approve their behavior according to project policy.
- SBOM/vulnerability/license checks: run audit/license/SBOM checks after lockfile changes when tools exist.
- Integrity controls: preserve package-manager lockfile and integrity verification; do not bypass them without explicit approval.

## Post-change verification and evidence

- Confirm `package.json` and the lockfile contain only the intended dependency changes.
- Confirm the resolved package/version and registry/source are the intended ones.
- Run appropriate vulnerability/advisory checks against the resolved dependency state.
- Run relevant project tests/builds after the gate when appropriate and permitted.
- Update or verify the SBOM when the project maintains one.
- Record actual checks and results and distinguish failed, unavailable, and not-attempted checks.

## Monitor and mitigate

- Outdated/advisory commands or feeds: `npm audit`, `npm outdated`, Dependabot or equivalent, OSV, SBOM scanners.
- Upgrade/patch/remove/rollback/isolate notes: prefer fixed versions through `npm install <pkg>@<fixed>`; remove or replace if abandoned or malicious.
- Approval/block conditions specific to this manager: approve install scripts, opaque binaries, new scopes, direct tarballs/Git URLs, registry changes, or missing lockfile for production; block malicious packages, likely typosquats/slopsquats, public resolution of private names, and unmitigated reachable high/critical issues.
