---
name: secure-package-consumption-composer
description: Composer and Packagist files, commands, repositories, plugins, and secure PHP dependency controls.
license: EUPL-1.2
metadata:
  version: "2.0-beta"
  package_managers: [composer]
  ecosystems: [php, packagist]
---

# Composer

## Scope

Use for PHP projects using Composer, Packagist, private Composer repositories, or Composer plugins.

## Files to inspect

- Manifests: `composer.json`.
- Lockfiles/resolution/vendor files: `composer.lock`, existing `vendor/composer/installed.json`.
- Registry/source/proxy/mirror/auth/scope mapping: repository blocks, `auth.json`, Composer config, Packagist settings, CI config.
- SBOM/vulnerability/license files: `composer audit` outputs, SBOMs, license policy.

## Command safety

- Metadata-only: static reads.
- Network/cache-writing: `composer show <vendor/package> --all --no-plugins --no-scripts`; `composer show --locked --tree --no-plugins --no-scripts`; `composer audit --locked --format=json --no-plugins --no-scripts`; `osv-scanner -r .`.
- Project-code-executing: Composer scripts, plugins, installers, autoload dumps that execute plugin behavior, tests.
- Project-mutating: `composer require <vendor/package>:<ver> --no-scripts`; `composer update <vendor/package> --with-dependencies --no-scripts`; `composer remove <vendor/package>`; `composer install`; lockfile/config edits.
- Lifecycle/build/plugin/native/binary caveats: plugins, scripts, installers, VCS/path repositories, binaries.

## Selection checks

- Package/source identity: verify vendor/package, repository block, Packagist/private source, project URL, and vendor owner.
- Vulnerability/advisory: use Composer audit, FriendsOfPHP/advisories, OSV, and repository alerts.
- Provenance/signature/hash/integrity: preserve `composer.lock` dist/source references and content hashes.
- Maintainer/project health/deprecation/ownership: inspect abandonment metadata, release cadence, repository activity, and ownership.
- License: inspect Composer license metadata and transitive licenses.
- Transitive impact: review locked tree and dependency diff.
- Confusion risks: protect private package names from public Packagist through repository configuration.

## Integration controls

- Pin/lock/reproducible install: commit `composer.json` and `composer.lock`; use locked install in CI.
- Registry/source enforcement: preserve approved repositories and disable Packagist for private-only namespaces when needed.
- Script/native/binary controls: keep `allow-plugins` minimal; use `--no-scripts` during dependency changes unless scripts are required and approved.
- SBOM/vulnerability/license checks: run Composer audit/license/SBOM checks after lock changes.

## Monitor and mitigate

- Outdated/advisory commands or feeds: `composer audit`, `composer outdated`, FriendsOfPHP/advisories, OSV, Dependabot/equivalent, SBOM scanners.
- Upgrade/patch/remove/rollback/isolate notes: update to fixed version or remove/replace abandoned packages; avoid broad updates unless requested.
- Approval/block conditions specific to this manager: approve VCS/path repositories, plugins, scripts, private repository changes, Packagist source changes, and abandoned production packages; block malicious/lookalike packages and unresolved reachable high/critical issues.
