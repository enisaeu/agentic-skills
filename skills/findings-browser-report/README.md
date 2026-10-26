# Findings Browser Report

An ENISA agentic skill that ports cybersecurity findings and their assets to an interactive HTML report. Using this skill, agentic AI assistants can process cybersecurity findings in a generic format and generate a structured interactive report, allowing human operators to easier go through them and process the information.

> [!NOTE]
> This ENISA agentic AI skill was developed by ENISA using AI tools and it was used to transform unformatted candidate findings to a human friendly browser report format.

---

| Property               | Value                   |
| ---------------------- | ----------------------- |
| **Skill Name**         | Findings Browser Report |
| **Version**            | 2.0-beta                |
| **License**            | EUPL-1.2                |

---

## Overview

The recent advances of AI have resulted in an increase in findings reported through Coordinated Vulnerability Disclosure (CVD). AI assisted scanning for vulnerabilities is now generating vast amounts of data that human maintainers may find difficult to process.

This skill aims at making easier the processing of findings assets by using agentic assistants to aggregate the findings into a single HTML report featuring a simple interface that the human operator can consume easier through a browser.

The skill instructs the overarching ai agent on how to process findings and related assets and embed them inside a HTML report wrapper, supporting the following:
* an executive summary with number of findings, conclusions, observations and recommendations
* a scope analysis covering the scan focus, review boundaries and components scanned
* a findings browser allowing the search and filter of the findings
* a per finding analysis, featuring an overview, list of evidences, remediation actions and validation info, tags

---

## Usage Notes

A cybersecurity scan can be started by referencing the skill and pointing to the target codebase to scan:
```
/findings-browser-report generate a findings browser report using the information under the `.security-reviews/` folder. The referenced code is also avalilable under the `./src` folder. Store the report in the current folder as `findings-browser-report.html` and the data as `findings-browser-data.json`.
```

Other things to consider when using the skill:
* Less capable or low cost models can be used for efficiency (cost and speed)
* The output may be influenced by availability of vulnerability information or the capabilities of the ai model utilised
* The output HTML file is using external CSS and Javascript libraries loaded through a CDN.

---

## Repository contents

```text
findings-browser-report/
├── README.md    # (This file here) provides information for repository users
├── SKILL.md     # Contains the operational instructions consumed by compatible AI systems
├── assets/      # Contains the base HTML template file
├── references/  # Contains supporting material used by the skill
└── scripts/     # Contains a script that handles the final report file generation
```

---

## Installation

Copy the `findings-browser-report` directory into the skill location used by your compatible AI client/platform.

```text
.agents/
└── skills/ <-- Find the skills folder used by your AI client/platform
    └── findings-browser-report/ <-- Copy inside, this repository folder
```

Refer to the documentation of your AI client/platform for installation and discovery instructions.

---

## Intended use

This skill can be used by:

* human handlers of vulnerability findings to aggregate cybersecurity findings into a simple report;
* agentic ai systems that want to export cybersecurity findings in a human friendly format.

---

## License

This skill is distributed under the license specified in the repository.

The licensing terms applicable to any related ENISA publication may differ from those governing the software-like artifacts contained in this repository.

---

## Disclaimer

This skill is intended to assist AI systems in aggregating vulnerability information into an HTML report. Depending on the context, the aggregated data may not include all the information needed to assist human operator's needs.

AI tools were used to support the development of this skill.
