---
name: secure-package-consumption-pnpm
description: pnpm files, commands, registry controls, and secure integration checks.
license: EUPL-1.2
metadata:
  version: "2.0-beta"
  package_managers: [pnpm]
  ecosystems: [javascript, typescript, node]
---

# pnpm

## Scope

Use for pnpm projects, including monorepos using `pnpm-workspace.yaml`.

## Files to inspect

- Manifests: `package.json`, workspace package manifests.
- Lockfiles/resolution/vendor files: `pnpm-lock.yaml`, existing `node_modules/.pnpm` metadata.
- Workspace files: `pnpm-workspace.yaml`, `.pnpmfile.cjs`.
- Registry/source/proxy/mirror/auth/scope mapping: `.npmrc`, `publishConfig`, `packageManager`, CI pnpm config.
- SBOM/vulnerability/license files: existing SBOMs, audit outputs, dependency-review config.

## Command safety

- Metadata-only: static reads; `pnpm config get registry`; `pnpm list --depth Infinity --json` when it only reads existing state.
- Network/cache-writing: `pnpm view <pkg> --json`; `pnpm audit --json`; `pnpm outdated --format json`; `osv-scanner -r .`.
- Project-code-executing: lifecycle scripts during install/rebuild; `.pnpmfile.cjs` hooks; `pnpm run <script>`.
- Project-mutating: `pnpm add --save-exact <pkg>@<ver>`; `pnpm remove <pkg>`; `pnpm update <pkg>`; `pnpm install`; `pnpm install --frozen-lockfile`; lockfile or `.npmrc` edits.
- Lifecycle/build/plugin/native/binary caveats: dependency hooks, lifecycle scripts, patched dependencies, native addons, downloaded binaries.

## Selection checks

- Package/source identity: verify package name, scope, registry, repository URL, and workspace target.
- Vulnerability/advisory: use pnpm audit, OSV, and project advisory feeds.
- Provenance/signature/hash/integrity: check `pnpm-lock.yaml` integrity and provenance/signature evidence when policy expects it.
- Maintainer/project health/deprecation/ownership: inspect metadata, release timing, deprecation, maintainers, and repository consistency.
- License: check package metadata and transitive licenses.
- Transitive impact: review lockfile tree and workspace impact.
- Confusion risks: verify `.npmrc` scope mapping and avoid public resolution of private scopes/names.

## Integration controls

- Pin/lock/reproducible install: commit `package.json` and `pnpm-lock.yaml`; use `pnpm install --frozen-lockfile` in CI.
- Registry/source enforcement: preserve approved `.npmrc`, scope mappings, and workspace settings.
- Script/native/binary controls: use `--ignore-scripts` only when compatible; review `.pnpmfile.cjs`.
- SBOM/vulnerability/license checks: run audit/SBOM/license checks after lockfile changes.

## Monitor and mitigate

- Outdated/advisory commands or feeds: `pnpm audit`, `pnpm outdated`, Dependabot/equivalent, OSV, SBOM scanners.
- Upgrade/patch/remove/rollback/isolate notes: prefer fixed versions through `pnpm update <pkg>` or `pnpm add <pkg>@<fixed>` scoped to the affected workspace.
- Approval/block conditions specific to this manager: approve lifecycle hooks, `.pnpmfile.cjs`, patches, registry changes, direct sources, or missing lockfile for production; block confusion targets and malicious/lookalike packages.
