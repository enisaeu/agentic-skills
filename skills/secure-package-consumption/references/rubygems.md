---
name: secure-package-consumption-rubygems
description: RubyGems files, commands, sources, native extensions, and secure gem controls.
license: EUPL-1.2
metadata:
  version: "2.0-beta"
  package_managers: [gem, rubygems]
  ecosystems: [ruby, rubygems]
---

# RubyGems

## Scope

Use for direct `gem` usage, gemspec dependency work, or RubyGems package assessment. Use `bundler.md` when `Gemfile.lock` owns application dependencies.

## Files to inspect

- Manifests: `*.gemspec`, `Gemfile` if present.
- Lockfiles/resolution/vendor files: `Gemfile.lock` if Bundler is used.
- Registry/source/proxy/mirror/auth/scope mapping: `.gemrc`, Bundler source config, private gem sources.
- SBOM/vulnerability/license files: `bundle-audit` outputs, SBOMs, license policy.

## Command safety

- Metadata-only: static reads.
- Network/cache-writing: `gem info <gem> --remote --all`; `gem dependency <gem> --remote`; `osv-scanner -r .`.
- Project-code-executing: gemspec/Gemfile Ruby evaluation, extension builds, tests.
- Project-mutating: `gem install <gem> -v <ver>`; `gem uninstall <gem>`; source config edits.
- Lifecycle/build/plugin/native/binary caveats: native extensions, `extconf.rb`, post-install messages/hooks, git/path gems.

## Selection checks

- Package/source identity: verify gem name, source, homepage/repository, owners, and expected project.
- Vulnerability/advisory: use bundle-audit/osv-scanner when available.
- Provenance/signature/hash/integrity: preserve lockfile checksums if Bundler uses them; verify signatures only when project policy supports them.
- Maintainer/project health/deprecation/ownership: inspect release cadence, owners, repo activity, deprecation, and security policy.
- License: inspect gemspec/license metadata and transitive licenses.
- Transitive impact: inspect dependencies before adding broad gems.
- Confusion risks: verify private gem source mapping and avoid public resolution of internal gem names.

## Integration controls

- Pin/lock/reproducible install: prefer Bundler with `Gemfile.lock` for applications.
- Registry/source enforcement: use approved gem sources/mirrors and avoid mixed unscoped sources.
- Script/native/binary controls: review native extension builds and git/path gems.
- SBOM/vulnerability/license checks: run bundle-audit/osv-scanner/license/SBOM checks after changes.

## Monitor and mitigate

- Outdated/advisory commands or feeds: RubySec, bundle-audit, osv-scanner, Dependabot/equivalent, SBOM scanners.
- Upgrade/patch/remove/rollback/isolate notes: update fixed gem versions through Bundler where possible; remove abandoned vulnerable gems.
- Approval/block conditions specific to this manager: approve git/path gems, private source changes, native extensions, unsigned/unknown-source gems under signing policy, and direct `gem install` for production; block malicious/lookalike gems and unresolved reachable high/critical issues.
