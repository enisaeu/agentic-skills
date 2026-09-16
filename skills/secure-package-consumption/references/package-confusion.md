---
name: secure-package-consumption-package-confusion
description: Typosquatting, slopsquatting, dependency-confusion, namespace, registry, and source identity checks.
license: EUPL-1.2
metadata:
  version: "2.0-beta"
---

# Package Confusion Checks

Use for new public packages, AI-suggested or unfamiliar names, internal-looking names, scoped packages, renamed packages, direct URLs, and names similar to existing dependencies.

## Checks

- Compare the requested name with existing dependencies, official docs, popular ecosystem packages, and organization-owned names/scopes.
- Flag edit-distance lookalikes, pluralization/abbreviation tricks, swapped or repeated characters, extra hyphens, misleading scopes, Unicode homoglyphs, and mixed scripts.
- Verify registry/source, repository URL, package description, maintainer/publisher, organization scope, and release history match the expected project.
- Treat hallucinated or AI-suggested names as untrusted until confirmed in the intended registry and official project documentation.
- For private/internal names, inspect the manager-specific source mapping file before accepting public resolution.
- Prefer registry artifacts from approved sources over Git, tarball, arbitrary URL, or local-path dependencies.

## Outcomes

- `block`: likely typosquat/slopsquat, dependency-confusion target, misleading source identity, or package designed to capture mistaken installs.
- `needs approval`: unclear source identity, direct URL/Git/path dependency, private/public registry ambiguity, unusual recent ownership change, or low evidence for production/sensitive use.
