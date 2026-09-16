---
name: secure-package-consumption-<package-manager-name>
description: <package managers/ecosystems covered> files, commands, controls, and secure integration checks for secure package consumptions
license: EUPL-1.2
metadata:
  version: "2.0-beta"
  package_managers: [<manager>, <alias>]
  ecosystems: [<language/platform>]
---

# <Package Manager or Ecosystem>

## Scope

Use for: <manager aliases, registry types, project shapes>.

## Files to inspect

- Manifests:
- Lockfiles/resolution/vendor files:
- Workspace files:
- Registry/source/proxy/mirror/auth/scope mapping:
- SBOM/vulnerability/license files:

## Command safety

- Metadata-only:
- Network/cache-writing:
- Project-code-executing:
- Project-mutating:
- Lifecycle/build/plugin/native/binary caveats:

## Selection checks

- Package/source identity:
- Vulnerability/advisory:
- Provenance/signature/hash/integrity:
- Maintainer/project health/deprecation/ownership:
- License:
- Transitive impact:
- Confusion risks:

## Integration controls

- Pin/lock/reproducible install:
- Registry/source enforcement:
- Script/native/binary controls:
- SBOM/vulnerability/license checks:

## Post-change verification and evidence

- Resolved package/version/source and manifest/lockfile consistency:
- Integrity/reproducibility checks:
- Vulnerability/license checks:
- Project test/build checks:
- SBOM or other evidence retained:
- Failed, unavailable, or not-attempted checks:

## Monitor and mitigate

- Outdated/advisory commands or feeds:
- Upgrade/patch/remove/rollback/isolate notes:
- Approval/block conditions specific to this manager:
