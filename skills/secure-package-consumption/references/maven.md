---
name: secure-package-consumption-maven
description: Maven files, commands, repositories, plugins, and secure JVM dependency controls.
license: EUPL-1.2
metadata:
  version: "2.0-beta"
  package_managers: [maven]
  ecosystems: [java, kotlin, scala, jvm]
---

# Maven

## Scope

Use for Maven projects using `pom.xml`, Maven Central, private repositories, or Maven build plugins.

## Files to inspect

- Manifests: `pom.xml`, parent POMs, module POMs.
- Lockfiles/resolution/vendor files: dependency lock outputs if used; vendored jars.
- Workspace files: `.mvn/maven.config`, `.mvn/extensions.xml`.
- Registry/source/proxy/mirror/auth/scope mapping: `settings.xml`, repository blocks, mirrors, profiles, credentials references.
- SBOM/vulnerability/license files: CycloneDX/OWASP/SBOM outputs, license policy, dependency review config.

## Command safety

- Metadata-only: static POM/settings inspection.
- Network/cache-writing: repository metadata/advisory lookups; `osv-scanner -r .` when it does not execute the build.
- Project-code-executing: `mvn dependency:tree`; `mvn help:effective-pom`; OWASP/CycloneDX Maven plugin runs; any command resolving build plugins or evaluating build lifecycle.
- Project-mutating: `mvn versions:use-dep-version -Dincludes=<groupId>:<artifactId> -DdepVersion=<ver>`; lockfile/SBOM/config edits; manual dependency edits.
- Lifecycle/build/plugin/native/binary caveats: build plugins, annotation processors, Maven extensions, classifiers with native artifacts, repositories in POMs.

## Selection checks

- Package/source identity: verify `groupId:artifactId`, repository, project URL, SCM URL, and organization.
- Vulnerability/advisory: use OSV, NVD/vendor advisories, OWASP Dependency-Check or equivalent when available.
- Provenance/signature/hash/integrity: prefer Maven Central/internal approved repos; verify checksums/signatures when policy supports them.
- Maintainer/project health/deprecation/ownership: inspect release cadence, project activity, security policy, and ownership.
- License: check POM license metadata and transitive licenses.
- Transitive impact: review dependency tree with approval if build execution is required.
- Confusion risks: ensure internal artifacts cannot resolve from public repositories; avoid adding arbitrary repositories.

## Integration controls

- Pin/lock/reproducible install: prefer explicit versions, parent-managed versions, or approved BOM/dependencyManagement.
- Registry/source enforcement: use approved mirrors/repositories in settings; avoid project-level arbitrary repos unless approved.
- Script/native/binary controls: review plugins, extensions, annotation processors, native classifiers, and generated code.
- SBOM/vulnerability/license checks: run approved Maven or external scanners after changes.

## Monitor and mitigate

- Outdated/advisory commands or feeds: OWASP Dependency-Check, OSV, Dependabot/equivalent, SBOM scanners, Maven repository advisories.
- Upgrade/patch/remove/rollback/isolate notes: update dependencyManagement/BOM or direct dependency to fixed version; exclude vulnerable transitives when justified.
- Approval/block conditions specific to this manager: approve new repositories, snapshots in production, build plugin changes, Maven extensions, native artifacts, and project-code-executing analysis before the gate; block public resolution of internal coordinates and unresolved reachable high/critical issues.
