---
name: secure-package-consumption-cargo
description: Cargo files, commands, registries, and secure Rust crate controls.
license: EUPL-1.2
metadata:
  version: "2.0-beta"
  package_managers: [cargo]
  ecosystems: [rust, crates.io]
---

# Cargo

## Scope

Use for Rust projects using Cargo, crates.io, alternate registries, or vendored crates.

## Files to inspect

- Manifests: `Cargo.toml`, workspace member manifests.
- Lockfiles/resolution/vendor files: `Cargo.lock`, `vendor/`, `.cargo-checksum.json`.
- Workspace files: workspace `Cargo.toml`, `rust-toolchain.toml`.
- Registry/source/proxy/mirror/auth/scope mapping: `.cargo/config.toml`, alternate registries, source replacement, credentials references.
- SBOM/vulnerability/license files: `cargo audit`, `cargo deny`, SBOM outputs, license policy.

## Command safety

- Metadata-only: static reads; local lockfile inspection.
- Network/cache-writing: `cargo search <crate>`; `cargo info <crate>`; `cargo tree --locked`; `cargo tree --locked -i <crate>`; `cargo audit`; `cargo deny check advisories`; `cargo deny check licenses`; `osv-scanner -r .`.
- Project-code-executing: `cargo build`; `cargo check`; `cargo test`; build scripts (`build.rs`); proc macros; generated code.
- Project-mutating: `cargo add <crate>@<ver>`; `cargo update -p <crate> --precise <ver>`; `cargo vendor`; lockfile/config/manifest edits.
- Lifecycle/build/plugin/native/binary caveats: `build.rs`, proc macros, FFI/native libraries, downloaded binaries, alternate registries.

## Selection checks

- Package/source identity: verify crate name, registry, repository URL, docs, and owner/organization.
- Vulnerability/advisory: use cargo-audit, cargo-deny, RustSec, osv-scanner, and project alerts.
- Provenance/signature/hash/integrity: preserve `Cargo.lock` checksums and approved source replacement.
- Maintainer/project health/deprecation/ownership: inspect release cadence, owners, repository activity, deprecation, and security policy.
- License: use cargo-deny or equivalent when policy exists.
- Transitive impact: inspect `cargo tree --locked` and feature expansion.
- Confusion risks: verify alternate registry/source replacement and internal crate naming.

## Integration controls

- Pin/lock/reproducible install: commit `Cargo.toml` and `Cargo.lock` for applications; use `--locked` in CI.
- Registry/source enforcement: preserve `.cargo/config.toml` and source replacement.
- Script/native/binary controls: review `build.rs`, proc macros, FFI/native dependencies, and binary downloads.
- SBOM/vulnerability/license checks: run cargo audit/deny or external scanners after lock changes.

## Monitor and mitigate

- Outdated/advisory commands or feeds: RustSec, cargo-audit, cargo-deny, osv-scanner, Dependabot/equivalent, SBOM scanners.
- Upgrade/patch/remove/rollback/isolate notes: use precise updates or patch sections; remove abandoned vulnerable crates when no fix exists.
- Approval/block conditions specific to this manager: approve alternate registries, source replacement, path/git deps, build scripts/proc macros in sensitive use, native code, and missing `Cargo.lock` for applications; block malicious/confusion crates and unresolved reachable high/critical issues.
