# Secure Package Consumption
 
This skill can help AI assistants make safer decisions when recommending, installing, updating, reviewing, or managing software packages and dependencies across common package ecosystems.

> [!NOTE]
> This ENISA agentic AI skill operationalises the recommendations of the **[ENISA Technical Advisory for Secure Use of Package Managers](https://www.enisa.europa.eu/publications/enisa-technical-advisory-for-secure-use-of-package-managers)** ([DOI:10.2824/6157993](https://doi.org/10.2824/6157993)). This skill was created as a practical example for encoding secure by design expectations through reusable skills, presented on **ENISA Technical Advisory on AI-assisted software development**.

---

| Property               | Value                      |
| ---------------------- | -------------------------- |
| **Skill Name**         | Secure Package Consumption |
| **Version**            | 2.0-beta                   |
| **License**            | EUPL-1.2                   |

---

## Overview

Modern software development relies heavily on third-party packages and open-source ecosystems. AI assistants are increasingly involved in tasks such as selecting dependencies, updating packages, resolving version conflicts, and reviewing software supply chain changes.

This skill translates the recommendations of the **[ENISA Technical Advisory for Secure Use of Package Managers](https://www.enisa.europa.eu/publications/enisa-technical-advisory-for-secure-use-of-package-managers)** into operational guidance that AI systems can apply during these workflows.

Rather than replacing developer judgement or automated security tools, the skill encourages AI assistants to consistently consider software supply chain security when interacting with package managers.

---

## Capabilities

The skill provides information that can assist with activities including:

* selecting appropriate software packages;
* reviewing dependency additions or removals;
* analysing package manifests and lockfiles;
* recommending package upgrades;
* evaluating package trustworthiness;
* identifying package confusion risks;
* checking package provenance and authenticity;
* interpreting vulnerability reports;
* reviewing package manager configuration;
* recommending safer dependency management practices.

The skill embeds information to support common package ecosystems, such as:

* npm
* pip
* yarn
* Maven
* Gradle
* Cargo
* NuGet
* Composer
* RubyGems
* Swift Package Manager
* Go Modules


Existing ecosystem-specific files (in `./references`) can be edited to customise the guidance, and new ecosystems can be added by creating additional files there and registering them in `./SKILL.md`.

---

## Repository contents

```text
secure-package-consumption/
├── README.md     # (This file here) provides information for repository users
├── SKILL.md      # Contains the main operational instructions to be consumed by compatible AI systems
└── references/   # Contains supporting material used by the skill (e.g. ecosystem specific information)
    ├── npm.md
    ├── pip.md
    └── ...      # (additional supporting material)
```

---

## Relationship to the source publication

This skill is an operational implementation of the recommendations contained in the **ENISA Technical Advisory for Secure Use of Package Managers**.

It reorganises the publication into instructions suitable for AI-assisted workflows while preserving the intent of the original guidance.

The skill:

* does not replace the publication;
* does not introduce normative requirements beyond those contained in the source publication;
* restructures guidance solely to improve its application by AI systems;
* should be used alongside the original ENISA publication when authoritative guidance is required.

Where implementation-specific assumptions or simplifications exist, they are documented within the skill and its supporting references.

---

## Intended use

This skill is intended to support AI-assisted workflows involving software package management, including:

* dependency management;
* package selection;
* software supply chain reviews;
* pull request analysis;
* dependency updates;
* package ecosystem migration;
* secure software development.

The skill complements existing software supply chain security practices and can be used alongside:

* Software Composition Analysis (SCA) tools;
* vulnerability scanners;
* SBOM generation tools;
* secure development lifecycle practices;
* organisational security policies.

---

## Installation

Copy the `secure-package-consumption` directory into the skill location used by your compatible AI client/platform.

```text
.agents/
└── skills/ <-- Find the skills folder used by your AI client/platform
    └── secure-package-consumption/ <-- Copy inside this repository folder
```

Refer to the documentation of your AI client/platform for installation and discovery instructions.

---

## Limitations

The effectiveness of this skill depends on the capabilities of the hosting AI system.

Recommendations may be influenced by:

* available tools and permissions;
* access to package registries;
* availability of vulnerability information;
* the completeness and accuracy of user input;
* the configuration of the hosting AI platform.

The skill only provide guidance to the AI system and cannot independently verify external information that is unavailable to the host environment.

---

## Contributing

Contributions should preserve traceability between this skill and its source publication.

Changes that materially affect the interpretation or implementation of ENISA guidance should be clearly documented and justified.

---

## License

This skill is distributed under the license specified in the repository.

The licensing terms applicable to the accompanying ENISA publication may differ from those governing the software-like artifacts contained in this repository.

---

## Disclaimer

This skill is intended to assist AI systems in applying ENISA guidance during software package management tasks. It is not a substitute for professional judgement, organisational policy, or formal security assessment.

AI tools were used to support the development of this skill.

The accompanying ENISA publication remains the authoritative source for all recommendations and should be consulted where precise interpretation is required.
