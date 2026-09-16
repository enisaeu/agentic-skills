---
name: secure-package-consumption-ruby
description: Routing reference for Ruby package-manager-specific files.
license: EUPL-1.2
metadata:
  version: "2.0-beta"
  package_managers: [rubygems, bundler]
  ecosystems: [ruby]
---

# Ruby Package Managers

Use an exact manager reference instead of this router when possible:

- `bundler.md` for `Gemfile` and `Gemfile.lock` application dependency changes.
- `rubygems.md` for direct `gem` commands, gemspec-only work, or RubyGems package assessment.

If both apply, prefer `bundler.md` for application dependency mutations because the lockfile owns reproducibility.
