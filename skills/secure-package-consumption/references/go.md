---
name: secure-package-consumption-go
description: Go modules files, commands, proxy/checksum controls, and secure dependency controls.
license: EUPL-1.2
metadata:
  version: "2.0-beta"
  package_managers: [go]
  ecosystems: [go, modules]
---

# Go Modules

## Scope

Use for Go projects using modules, module proxies, checksum databases, or vendored modules.

## Files to inspect

- Manifests: `go.mod`.
- Lockfiles/resolution/vendor files: `go.sum`, `vendor/modules.txt`, `vendor/`.
- Workspace files: `go.work`, `go.work.sum`.
- Registry/source/proxy/mirror/auth/scope mapping: `GOPRIVATE`, `GONOSUMDB`, `GONOPROXY`, `GOSUMDB`, `GOPROXY`, CI env.
- SBOM/vulnerability/license files: govulncheck outputs, SBOMs, license policy.

## Command safety

- Metadata-only: static reads; existing `go.mod`, `go.sum`, and vendor metadata inspection.
- Network/cache-writing: `go list -m -json <module>@<ver>`; `go list -m -versions <module>`; `go list -m -u -json all`; `go mod graph`; `go mod why -m <module>`; `go mod download`; `osv-scanner -r .`. These commands may access the network, populate the module cache, and add missing entries to `go.sum`.
- Project-code-analyzing: `govulncheck ./...` and `go list -deps -json ./...` load and analyze project packages but do not normally execute the resulting project binaries; build, test, and generate commands can execute toolchain or project-controlled behavior.
- Project-mutating: `go get <module>@<ver>`; `go mod tidy`; `go mod vendor`; `go mod edit`; `go.work` edits; and any otherwise informational module command that writes missing `go.sum` entries.
- Lifecycle/build/plugin/native/binary caveats: cgo/native code, generated code, module path changes, `replace` directives, pseudo-versions.

## Selection checks

- Package/source identity: verify module path, repository, tags, vanity import path, and owner.
- Vulnerability/advisory: use govulncheck/OSV and repository alerts when available.
- Provenance/signature/hash/integrity: preserve `go.sum`; verify checksum database/private module exceptions.
- Maintainer/project health/deprecation/ownership: inspect release cadence, repository activity, security policy, and ownership changes.
- License: inspect module and transitive licenses.
- Transitive impact: review module graph and `go mod why`.
- Confusion risks: protect private modules with `GOPRIVATE`/related settings and avoid public proxy/checksum leaks.

## Integration controls

- Pin/lock/reproducible install: commit `go.mod` and `go.sum`; use tagged versions where possible.
- Registry/source enforcement: preserve `GOPRIVATE`, `GONOSUMDB`, `GONOPROXY`, `GOSUMDB`, and `GOPROXY` settings.
- Script/native/binary controls: review cgo/native code, generated code, and module replacements.
- SBOM/vulnerability/license checks: run govulncheck/OSV/SBOM/license checks after changes when available.

## Monitor and mitigate

- Outdated/advisory commands or feeds: govulncheck, OSV, Dependabot/equivalent, SBOM scanners.
- Upgrade/patch/remove/rollback/isolate notes: use `go get <module>@<fixed>` then `go mod tidy` after approval; remove or replace abandoned modules.
- Approval/block conditions specific to this manager: approve new `replace` directives, pseudo-versions in production, private module setting changes, cgo/native dependencies, direct VCS/private sources, and public leakage risk; block module path confusion and unresolved reachable high/critical issues.
