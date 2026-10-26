# Code Auditor
 
This skill can guide AI assistants in performing a cybersecurity focused code auditing to uncover possible cybersecurity-related findings.

> [!NOTE]
> This ENISA agentic AI skill was developed by ENISA using AI tools and it was used to scan codebases and identify possible vulnerabilities.

---

| Property               | Value        |
| ---------------------- | ------------ |
| **Skill Name**         | Code Auditor |
| **Version**            | 1.0-beta     |
| **License**            | EUPL-1.2     |

---

## Overview

Modern software development relies heavily on third-party packages and open-source ecosystems. AI assistants are increasingly involved in tasks such as selecting dependencies, updating packages, resolving version conflicts, and reviewing software supply chain changes.

This skill instructs the agent to follow a simple phases based methodology to conduct the cybersecurity code auditing and produce appropriate artifacts under the `.security-reviews/` folder:

1. Control Phase - Check and coordinate the scan by looking into the available artifacts, decide what phase to start.
2. Scope Phase - Try to define the audit scope before the analysis by identifying the target codebase and inventory.
3. Tools Phase - Identity and invoke available security tools and treat their output as possible evidence.
4. Threats Phase - Try to build a threat model based on the scope of the target.
5. Discovery Phase - Deploy multiple sub-agents (6 by default) to scan the code for possible cybersecurity issues. (Unless specified) The scan is organised in at-least 3 passes:
  - **Attack surface and data flow** focused pass
  - **Identity and state** focused pass
  - **Platform and chaining** focused pass
  - (possibly) passes with additional focus requested by the user or deriving from the threat model
6. Triage Phase - Aggregating all the findings and validating them, to produce the final list of possible issues
7. Remediation Phase - Looking into the possible remediation of the identified findings
8. Reporting Phase - Producing both an aggregated report and per finding specific report (using the 2 templates available under the references)
9. (per request) Exploitation Phase - Looking into the development of a Proof-of-Concept (PoC) for the finding specified

---

## Usage Notes

A cybersecurity scan can be started by referencing the skill and pointing to the target codebase to scan:
```
/code-auditor Perform a deep code audit on the codebase locally available in this project.
```
Please note that the way to mention the skill may change depending on the AI client you are using.

Of course, you may modify the way the scan is performed according to your needs. Here is an example assuming an antivirus software code is audited:
```
/code-auditor Perform a deep code audit on the antivirus source code available under the `./src` folder. You can find additional information on the various components of the software inside the `COMPONENTS.md`. Start the scanning from the core components and expand to the rest. Utilise the CodeAuditGuidelines_for_Antivirus.md that include antivirus specific code audit priorities.
```

Other things to consider when using the skill:
* The ai identified findings may include false positives (maintainer/pentester verification is needed and suggested)
* The per finding severity reported by an AI agent may be invalid (maintainer/business-owner verification is needed)
* Consider providing additional context related to the target codebase to improve efficiency and reduce noise in the output
* You may have to customise the Tools Phase so that the agent can use the tools available to your environment
* Depending on the guardrails applied to your interactions with the model your requests may be blocked
* Depending on the model used your requests may be denied
* The Exploitation Phase may require red team capabilities to be allowed by your deployment
* You may instruct your AI agent to use a specific number of sub-agents for the discovery phase
* You may instruct your AI agent to follow specific guidelines (tailored to your target software) during the discovery phase

---

## Repository contents

```text
code-auditor/
├── README.md     # (This file here) provides information for repository users
├── SKILL.md      # Contains the main operational instructions to be consumed by compatible AI systems
└── references/   # Contains supporting material used by the skill (e.g. per phase specific instructions)
    ├── control.md
    ├── scope.md
    ├── ...
    ├── reporting.md
    ├── reporting-template.Findings.md                # (aggregated findings reporting template)
    ├── reporting-template.SEVERITY-NNN-short-name.md # (per finding reporting template)
    └── ...                                           # (additional supporting material)
```

---

## Default Output

Here is a layout of the most important files expected as an output after running the default code audit procedure:
```text
.security-reviews/
├── <review-id>/
    ├── ...
    ├── Findings.md                        # aggregated findings report
    ├── findings/
    │   └── SEVERITY-NNN-short-name.md     # per finding report
    ├── patches/
    │   └── SEVERITY-NNN/                  # per finding remediation related material
    ├── poc/
    │   └── SEVERITY-NNN/                  # per finding PoC related material
    └── ...
```

Please note that your agentic tool not store the `.security-reviews` folder under your current working directory.

---

## Intended use

This skill is intended to support AI-assisted vulnerability identification, reporting as well as patching.

---

## Installation

Copy the `code-auditor` directory into the skill location used by your compatible AI client/platform.

```text
.agents/
└── skills/ <-- Find the skills folder used by your AI client/platform
    └── code-auditor/ <-- Copy inside, this repository folder
```

Refer to the documentation of your AI client/platform for installation and discovery instructions.

---

## License

This skill is distributed under the license specified in the repository.

The licensing terms applicable to any related ENISA publication may differ from those governing the software-like artifacts contained in this repository.

---

## Disclaimer

This skill is intended to guide AI agents in conducting a cybersecurity focused code audit and identify possible vulnerabilities and/or possible security issues. The output findings of an AI agent using this skill, should be verified (as true positive) and corrected (edit metadata) by a professional.

AI tools were used to support the development of this skill.
