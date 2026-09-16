---
name: secure-package-consumption-yarn
description: Yarn files, commands, registry controls, and secure integration checks.
license: EUPL-1.2
metadata:
  version: "2.0-beta"
  package_managers: [yarn]
  ecosystems: [javascript, typescript, node]
---

# Yarn

## Scope

Use for Yarn Classic or modern Yarn projects. Match commands to the project's Yarn major version.

## Files to inspect

- Manifests: `package.json`, workspace manifests.
- Lockfiles/resolution/vendor files: `yarn.lock`, `.pnp.cjs`, `.yarn/cache`, `.yarn/patches` when present.
- Workspace files: `workspaces` in `package.json`, `.yarnrc.yml`.
- Registry/source/proxy/mirror/auth/scope mapping: `.yarnrc.yml`, `.npmrc`, `npmScopes`, `npmRegistryServer`, CI Yarn config.
- SBOM/vulnerability/license files: existing SBOMs, audit outputs, dependency-review config.

## Command safety

- Metadata-only: static reads; `yarn config get npmRegistryServer` (modern) / `yarn config get registry` (classic); local `yarn why <pkg>` when it does not install or modify state.
- Network/cache-writing: `yarn npm info <pkg> --json` (modern) / `yarn info <pkg> --json` (classic); `yarn npm audit --json` (modern) / `yarn audit --json` (classic); ; `osv-scanner -r .`.
- Project-code-executing: lifecycle scripts during install/rebuild; Yarn plugin execution; `yarn run <script>`.
- Project-mutating: `yarn add <pkg>@<ver>`; `yarn remove <pkg>`; `yarn up <pkg>@<ver>` (modern) / `yarn upgrade <pkg>@<ver>` (classic); `yarn install`; `yarn install --immutable` (modern) / `yarn install --frozen-lockfile` (classic); lockfile, cache, or config edits.
- Lifecycle/build/plugin/native/binary caveats: install scripts, Yarn plugins, patches, unplugged packages, native addons, downloaded binaries.

## Selection checks

- Package/source identity: verify package name, scope, registry, repository URL, and workspace target.
- Vulnerability/advisory: use yarn audit, osv-scanner, and repository alerts when available.
- Provenance/signature/hash/integrity: check `yarn.lock` checksums and zero-install cache integrity when used.
- Maintainer/project health/deprecation/ownership: inspect metadata, deprecation, release cadence, maintainers, and repository consistency.
- License: check package and transitive licenses.
- Transitive impact: review lockfile/workspace impact and avoid large trees for small features.
- Confusion risks: verify `npmScopes`/registry mapping for private scopes.

## Integration controls

- Pin/lock/reproducible install: commit `package.json` and `yarn.lock`; use `yarn install --immutable` in CI for modern Yarn.
- Registry/source enforcement: preserve approved `.yarnrc.yml` and private scope mappings.
- Script/native/binary controls: review scripts, plugins, patches, and unplugged/native packages.
- SBOM/vulnerability/license checks: run audit/SBOM/license checks after lockfile changes.

## Monitor and mitigate

- Outdated/advisory commands or feeds: yarn audit, Dependabot/equivalent, osv-scanner, SBOM scanners.
- Upgrade/patch/remove/rollback/isolate notes: prefer fixed versions through `yarn up <pkg>@<fixed>` or scoped manifest edits.
- Approval/block conditions specific to this manager: approve new Yarn plugins, patches, direct sources, registry changes, install scripts, and missing lockfile/immutable install for production; block malicious/lookalike packages and public resolution of private names.
