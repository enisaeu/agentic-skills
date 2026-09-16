---
name: secure-package-consumption-gradle
description: Gradle files, commands, repositories, plugins, and secure JVM dependency controls.
license: EUPL-1.2
metadata:
  version: "2.0-beta"
  package_managers: [gradle]
  ecosystems: [java, kotlin, scala, jvm, android]
---

# Gradle

## Scope

Use for Gradle projects using Groovy or Kotlin DSL, version catalogs, dependency locking, or Gradle plugins.

## Files to inspect

- Manifests: `build.gradle`, `build.gradle.kts`, module build files, `settings.gradle`, `settings.gradle.kts`.
- Lockfiles/resolution/vendor files: `gradle.lockfile`, `gradle/verification-metadata.xml`, vendored jars.
- Workspace files: `gradle.properties`, `gradle/libs.versions.toml`, `init.gradle`, Gradle wrapper files.
- Registry/source/proxy/mirror/auth/scope mapping: repository blocks, plugin repositories, dependency verification, credentials references.
- SBOM/vulnerability/license files: dependency-check, CycloneDX, SBOM, license policy outputs.

## Command safety

- Metadata-only: static build/settings/catalog inspection.
- Network/cache-writing: repository/advisory metadata lookups; `osv-scanner -r .` when it does not execute the build.
- Project-code-executing: `./gradlew dependencies`; `./gradlew dependencyInsight --dependency <artifact> --configuration <configuration>`; dependency-check/CycloneDX Gradle tasks; any task evaluating build scripts/plugins.
- Project-mutating: `./gradlew dependencies --write-locks`; dependency lock/verification metadata edits; manifest/catalog edits.
- Lifecycle/build/plugin/native/binary caveats: buildscript classpath, Gradle plugins, init scripts, annotation processors, source generators, native artifacts.

## Selection checks

- Package/source identity: verify coordinates, repository, plugin portal source, SCM/project URL, and organization.
- Vulnerability/advisory: use OSV, NVD/vendor advisories, dependency-check or equivalent when available.
- Provenance/signature/hash/integrity: preserve dependency verification metadata and lockfiles where used.
- Maintainer/project health/deprecation/ownership: inspect release cadence, project activity, security policy, and ownership.
- License: check POM metadata and transitive licenses.
- Transitive impact: review dependency insight/tree with approval if build execution is required.
- Confusion risks: enforce repository order/content filtering so internal coordinates do not resolve publicly.

## Integration controls

- Pin/lock/reproducible install: use version catalogs/platforms/BOMs and dependency locks where the project uses them.
- Registry/source enforcement: preserve repository content filters, plugin repositories, and verification metadata.
- Script/native/binary controls: review plugins, buildscript classpath, annotation processors, source generators, and native artifacts.
- SBOM/vulnerability/license checks: run approved Gradle or external scanners after changes.

## Monitor and mitigate

- Outdated/advisory commands or feeds: Dependabot/equivalent, OSV, dependency-check, SBOM scanners, release monitoring.
- Upgrade/patch/remove/rollback/isolate notes: update version catalog, platform/BOM, constraint, or direct dependency; use exclusions only with documented compatibility evidence.
- Approval/block conditions specific to this manager: approve new repositories, plugin/buildscript changes, snapshots/dynamic versions in production, native artifacts, and project-code-executing analysis before the gate; block public resolution of internal coordinates and unresolved reachable high/critical issues.
