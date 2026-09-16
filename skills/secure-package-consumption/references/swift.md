---
name: secure-package-consumption-swift
description: Routing reference for Swift package-manager-specific files.
license: EUPL-1.2
metadata:
  version: "2.0-beta"
  package_managers: [swiftpm, cocoapods]
  ecosystems: [swift, objective-c, apple]
---

# Swift Package Managers

Use an exact manager reference instead of this router when possible:

- `swiftpm.md` for `Package.swift`, `Package.resolved`, SwiftPM plugins, source packages, or binary targets.
- `cocoapods.md` for `Podfile`, `Podfile.lock`, podspecs, CocoaPods spec repositories, or `Pods/` integration.

If both managers are present, identify the active dependency workflow from CI and project files. Do not switch managers unless the user requested it.
