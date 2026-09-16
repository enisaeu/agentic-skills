---
name: secure-package-consumption-swiftpm
description: Swift Package Manager files, commands, repositories, plugins, binary targets, and secure dependency controls.
license: EUPL-1.2
metadata:
  version: "2.0-beta"
  package_managers: [swiftpm, swift-package-manager]
  ecosystems: [swift, apple]
---

# Swift Package Manager

## Scope

Use for Swift Package Manager projects using `Package.swift`, `Package.resolved`, source packages, plugins, or binary targets.

## Files to inspect

- Manifests: `Package.swift`.
- Lockfiles/resolution/vendor files: `Package.resolved`, `.build` metadata if already present.
- Workspace files: `.swiftpm/configuration`, Xcode package resolution files.
- Registry/source/proxy/mirror/auth/scope mapping: package URLs, registry config, mirrors, branch/tag/revision pins.
- SBOM/vulnerability/license files: SBOMs, scanner outputs, license policy.

## Command safety

- Metadata-only: static manifest/resolved-file inspection.
- Network/cache-writing: repository/advisory metadata lookups; `osv-scanner -r .` when it does not build.
- Project-code-executing: `swift package show-dependencies`; `swift package dump-package`; build/test commands; plugins.
- Project-mutating: manual `Package.swift` edits; `swift package add-dependency <url> --from <ver>` when available; `swift package resolve`; resolved-file/config edits.
- Lifecycle/build/plugin/native/binary caveats: build tool plugins, command plugins, binary targets, branch/revision dependencies, unsafe flags.

## Selection checks

- Package/source identity: verify repository URL, tag/release, owner, package identity, and expected project.
- Vulnerability/advisory: use OSV/vendor advisories and repository alerts when available.
- Provenance/signature/hash/integrity: prefer tagged releases and resolved pins; verify checksums for binary targets.
- Maintainer/project health/deprecation/ownership: inspect release cadence, repository activity, security policy, and ownership.
- License: inspect package/repository license and transitive licenses.
- Transitive impact: review resolved dependency graph with approval if command execution is needed.
- Confusion risks: avoid lookalike repositories, branch tracking, and unverified source moves.

## Integration controls

- Pin/lock/reproducible install: commit `Package.swift` and `Package.resolved` for applications.
- Registry/source enforcement: use approved repositories, registries, mirrors, and tagged releases over floating branches.
- Script/native/binary controls: approve plugins, binary targets, unsafe flags, and native artifacts.
- SBOM/vulnerability/license checks: run SBOM/advisory/license checks after resolution changes.

## Monitor and mitigate

- Outdated/advisory commands or feeds: repository advisories, OSV, Dependabot/equivalent where supported, SBOM scanners.
- Upgrade/patch/remove/rollback/isolate notes: update package requirement to fixed tag/version; remove or replace risky packages.
- Approval/block conditions specific to this manager: approve binary targets, plugins, branch/revision dependencies, repository moves, private registries, and missing `Package.resolved` for production apps; block malicious/lookalike repos and unresolved reachable high/critical issues.
