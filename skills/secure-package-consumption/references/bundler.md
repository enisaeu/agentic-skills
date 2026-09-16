---
name: secure-package-consumption-bundler
description: Bundler files, commands, sources, lockfiles, and secure Ruby dependency controls.
license: EUPL-1.2
metadata:
  version: "2.0-beta"
  package_managers: [bundler, bundle]
  ecosystems: [ruby, rubygems]
---

# Bundler

## Scope

Use for Ruby applications or libraries where `Gemfile` and `Gemfile.lock` manage dependencies.

## Files to inspect

- Manifests: `Gemfile`, `*.gemspec`.
- Lockfiles/resolution/vendor files: `Gemfile.lock`, `vendor/cache`.
- Workspace files: `.ruby-version`, `.tool-versions`.
- Registry/source/proxy/mirror/auth/scope mapping: `.bundle/config`, source blocks, mirrors, private gem sources.
- SBOM/vulnerability/license files: `bundle-audit` outputs, SBOMs, license policy.

## Command safety

- Metadata-only: static reads; `bundle config list` when it only reads local config.
- Network/cache-writing: `gem info <gem> --remote --all`; `gem dependency <gem> --remote`; `bundle-audit check --format json`; `osv-scanner -r .`.
- Project-code-executing: Bundler commands that evaluate `Gemfile` or gemspec Ruby code; extension builds; tests.
- Project-mutating: `bundle add <gem> --version <ver>`; `bundle update <gem>`; `bundle install`; lockfile/source config edits.
- Lifecycle/build/plugin/native/binary caveats: native extensions, `extconf.rb`, git/path gems, post-install behavior.

## Selection checks

- Package/source identity: verify gem name, source, source blocks, homepage/repository, owners, and expected project.
- Vulnerability/advisory: use bundle-audit/osv-scanner and repository alerts.
- Provenance/signature/hash/integrity: preserve `Gemfile.lock`; use checksums/signatures if the project enforces them.
- Maintainer/project health/deprecation/ownership: inspect release cadence, owners, repo activity, deprecation, and security policy.
- License: inspect gemspec/license metadata and transitive licenses.
- Transitive impact: review dependency tree and lockfile diff.
- Confusion risks: verify source blocks/mirrors and avoid public resolution of internal gem names.

## Integration controls

- Pin/lock/reproducible install: commit `Gemfile` and `Gemfile.lock`; use frozen/deployment install modes in CI when configured.
- Registry/source enforcement: preserve approved sources, mirrors, and source blocks.
- Script/native/binary controls: review native extensions, git/path gems, and post-install behavior.
- SBOM/vulnerability/license checks: run bundle-audit/osv-scanner/license/SBOM checks after lock changes.

## Monitor and mitigate

- Outdated/advisory commands or feeds: `bundle outdated`, bundle-audit, osv-scanner, Dependabot/equivalent, SBOM scanners.
- Upgrade/patch/remove/rollback/isolate notes: use `bundle update <gem>` or pin fixed versions; remove/replace abandoned vulnerable gems.
- Approval/block conditions specific to this manager: approve git/path gems, private source changes, native extensions, source block ambiguity, and missing lockfile for production; block malicious/lookalike gems and unresolved reachable high/critical issues.
