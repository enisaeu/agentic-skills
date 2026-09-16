---
name: secure-package-consumption-maven-gradle
description: Routing reference for JVM package-manager-specific files.
license: EUPL-1.2
metadata:
  version: "2.0-beta"
  package_managers: [maven, gradle]
  ecosystems: [java, kotlin, scala, jvm]
---

# Maven and Gradle

Use an exact manager reference instead of this router when possible:

- `maven.md` for `pom.xml`, `.mvn`, Maven plugins, Maven Central, or Maven repository settings.
- `gradle.md` for `build.gradle`, `build.gradle.kts`, `settings.gradle`, version catalogs, dependency locking, or Gradle plugins.

If both managers are present, identify the active build workflow from CI and wrapper files. Do not switch build tools unless the user requested it.
