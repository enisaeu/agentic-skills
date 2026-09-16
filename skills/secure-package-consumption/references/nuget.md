---
name: secure-package-consumption-nuget
description: NuGet and .NET files, commands, sources, package-source mapping, and secure dependency controls.
license: EUPL-1.2
metadata:
  version: "2.0-beta"
  package_managers: [nuget, dotnet]
  ecosystems: [dotnet, csharp, fsharp, vb]
---

# NuGet and .NET

## Scope

Use for .NET projects using NuGet packages, `dotnet` CLI, central package management, or packages.config.

## Files to inspect

- Manifests: `*.csproj`, `*.fsproj`, `*.vbproj`, `packages.config`, `Directory.Packages.props`.
- Lockfiles/resolution/vendor files: `packages.lock.json`, `obj/project.assets.json` when already present.
- Workspace files: `global.json`, solution files, `Directory.Build.props`, `Directory.Build.targets`.
- Registry/source/proxy/mirror/auth/scope mapping: `NuGet.config`, package sources, package source mapping, credentials references.
- SBOM/vulnerability/license files: SBOMs, `dotnet list package` (.NET 9 or earlier) outputs / `dotnet package list --no-restore` (.NET 10+) outputs, license policy.

## Command safety

- Metadata-only: static reads; `dotnet nuget list source`; `dotnet list package --no-restore` when restore is not triggered.
- Network/cache-writing: `dotnet list package --vulnerable --include-transitive --no-restore` when existing assets allow it; advisory/repository lookups; `osv-scanner -r .`.
- Project-code-executing: restore/MSBuild evaluation, analyzers/source generators during build, custom targets, tests.
- Project-mutating: `dotnet add package <pkg> --version <ver>` (.NET 9 or earlier) / `dotnet package add  <pkg> --version <ver>` (.NET 10+); `dotnet remove package <pkg>` (.NET 9 or earlier) / `dotnet package remove <pkg>` (.NET 10+); `dotnet restore`; lockfile/source config edits.
- Lifecycle/build/plugin/native/binary caveats: build targets, analyzers, source generators, native assets, init/build transitive props/targets.

## Selection checks

- Package/source identity: verify package ID, source/feed, owner, repository URL, and source mapping.
- Vulnerability/advisory: use `dotnet list package --vulnerable`, GitHub/osv-scanner/NuGet advisories, and SBOM scanners.
- Provenance/signature/hash/integrity: preserve lockfiles and package signing policy where used.
- Maintainer/project health/deprecation/ownership: inspect deprecation, downloads/release cadence, repository activity, and ownership.
- License: inspect package metadata and transitive licenses.
- Transitive impact: review package list and central package effects.
- Confusion risks: package source mapping must protect private IDs when public/private feeds coexist.

## Integration controls

- Pin/lock/reproducible install: use central package management when present; commit `packages.lock.json`; use `dotnet restore --locked-mode` in CI.
- Registry/source enforcement: preserve `NuGet.config` package source mapping and approved feeds.
- Script/native/binary controls: review build targets, analyzers, source generators, and native assets.
- SBOM/vulnerability/license checks: run vulnerability/license/SBOM checks after restore/lock changes.

## Monitor and mitigate

- Outdated/advisory commands or feeds: `dotnet list package --outdated`, `--vulnerable`, Dependabot/equivalent, NuGet advisories, SBOM scanners.
- Upgrade/patch/remove/rollback/isolate notes: update `Directory.Packages.props` or project references to fixed versions; remove/replace vulnerable packages.
- Approval/block conditions specific to this manager: approve new feeds, source mapping changes, unsigned packages when signing policy exists, packages with build targets/analyzers/source generators/native assets, and missing lockfile for production; block public resolution of private IDs and unresolved reachable high/critical issues.
