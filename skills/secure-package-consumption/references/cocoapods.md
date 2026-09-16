---
name: secure-package-consumption-cocoapods
description: CocoaPods files, commands, spec repositories, script phases, vendored binaries, and secure dependency controls.
license: EUPL-1.2
metadata:
  version: "2.0-beta"
  package_managers: [cocoapods, pod]
  ecosystems: [swift, objective-c, apple]
---

# CocoaPods

## Scope

Use for iOS/macOS projects using `Podfile`, `Podfile.lock`, podspecs, public or private spec repositories.

## Files to inspect

- Manifests: `Podfile`, `*.podspec`.
- Lockfiles/resolution/vendor files: `Podfile.lock`, `Pods/Manifest.lock`, existing `Pods/` metadata.
- Workspace files: Xcode workspace/project files that define pods integration.
- Registry/source/proxy/mirror/auth/scope mapping: spec repo sources, private spec repos, Git/source pods.
- SBOM/vulnerability/license files: SBOMs, scanner outputs, license policy.

## Command safety

- Metadata-only: static `Podfile`, lockfile, and podspec inspection.
- Network/cache-writing: `pod search <pod>`; `pod ipc spec <pod.podspec>`; `pod repo update`; repository/advisory lookups; `osv-scanner -r .`.
- Project-code-executing: Podfile Ruby evaluation, podspec evaluation, script phases, build/test commands.
- Project-mutating: `pod install`; `pod update <pod>`; lockfile/source config edits; manual Podfile edits.
- Lifecycle/build/plugin/native/binary caveats: `script_phase`, vendored frameworks/libraries, prepare commands, Git/path pods, binary pods.

## Selection checks

- Package/source identity: verify pod name, spec repo, source URL, tag, owner, and expected project.
- Vulnerability/advisory: use osv-scanner/vendor advisories and repository alerts when available.
- Provenance/signature/hash/integrity: preserve `Podfile.lock` checksums and verify source tags/checksums when available.
- Maintainer/project health/deprecation/ownership: inspect release cadence, repo activity, security policy, and ownership.
- License: inspect podspec license and transitive licenses.
- Transitive impact: review lockfile and podspec dependencies.
- Confusion risks: ensure private specs/source repos cannot be shadowed by public specs.

## Integration controls

- Pin/lock/reproducible install: commit `Podfile` and `Podfile.lock`; pin tags/versions.
- Registry/source enforcement: preserve approved spec repos and private source ordering.
- Script/native/binary controls: approve script phases, prepare commands, vendored binaries, and Git/path pods.
- SBOM/vulnerability/license checks: run SBOM/advisory/license checks after lock changes.

## Monitor and mitigate

- Outdated/advisory commands or feeds: repository advisories, osv-scanner, Dependabot/equivalent where supported, SBOM scanners.
- Upgrade/patch/remove/rollback/isolate notes: update pod to fixed version or remove/replace risky pod.
- Approval/block conditions specific to this manager: approve script phases, prepare commands, vendored frameworks, private spec repo changes, Git/path pods, and missing lockfile for production apps; block malicious/lookalike pods and unresolved reachable high/critical issues.
