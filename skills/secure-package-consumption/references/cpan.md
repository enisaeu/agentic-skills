---
name: secure-package-consumption-cpan
description: CPAN, cpanminus, and Carton files, commands, mirrors, native code, and secure Perl dependency controls.
license: EUPL-1.2
metadata:
  version: "2.0-beta"
  package_managers: [cpan, cpanminus, carton]
  ecosystems: [perl, cpan]
---

# CPAN, cpanminus, and Carton

## Scope

Use for Perl modules installed from CPAN or private mirrors, including cpanfile and Carton workflows.

## Files to inspect

- Manifests: `cpanfile`, `Makefile.PL`, `Build.PL`, `META.json`, `META.yml`.
- Lockfiles/resolution/vendor files: `cpanfile.snapshot`, `local/` metadata when already present.
- Registry/source/proxy/mirror/auth/scope mapping: CPAN mirror config, cpanminus options, private repositories.
- SBOM/vulnerability/license files: `cpan-audit` outputs, SBOMs, license policy.

## Command safety

- Metadata-only: static reads of cpanfile, snapshots, and META files.
- Network/cache-writing: `cpanm --info <Module::Name>`; `cpan-audit deps .`; `osv-scanner -r .`.
- Project-code-executing: `Makefile.PL`, `Build.PL`, tests, build/install hooks, XS compilation.
- Project-mutating: `cpanm <Module::Name>@<ver>`; `carton install`; `carton update <Module::Name>`; `cpan`; snapshot/config edits.
- Lifecycle/build/plugin/native/binary caveats: XS/native code, configure/build scripts, test-time network access, git/path modules.

## Selection checks

- Package/source identity: verify module name, distribution, author/maintainer, mirror/source, and repository URL.
- Vulnerability/advisory: use cpan-audit, osv-scanner, vendor advisories, and repository alerts when available.
- Provenance/signature/hash/integrity: prefer snapshots/approved mirrors; verify signatures/checksums when project policy supports them.
- Maintainer/project health/deprecation/ownership: inspect release cadence, maintainer activity, issue tracker, and deprecation.
- License: inspect META license and transitive licenses.
- Transitive impact: review snapshot/dependency expansion.
- Confusion risks: protect private module names and mirror priority.

## Integration controls

- Pin/lock/reproducible install: commit `cpanfile` and `cpanfile.snapshot` when Carton is used.
- Registry/source enforcement: use approved CPAN mirrors/private repositories.
- Script/native/binary controls: approve XS/native code, build scripts, git/path modules, and test-time network access.
- SBOM/vulnerability/license checks: run cpan-audit/osv-scanner/license/SBOM checks after snapshot changes.

## Monitor and mitigate

- Outdated/advisory commands or feeds: cpan-audit, osv-scanner, repository alerts, SBOM scanners.
- Upgrade/patch/remove/rollback/isolate notes: update snapshot to fixed version; remove/replace abandoned vulnerable modules.
- Approval/block conditions specific to this manager: approve XS/native code, git/path modules, private mirror changes, and missing snapshot for production; block malicious/lookalike modules and unresolved reachable high/critical issues.
