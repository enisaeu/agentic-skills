> [!WARNING]
> The skills and guidance in this repository are provided for demonstration and reference purposes only.
>
> They must not be deployed in production environments without appropriate review, testing, and adaptation to the specific system, product, risks, policies, and operating constraints in question.
>
> Some skills may instruct the model to invoke potentially hazardous operations, including modifying files or dependency state, deleting or overwriting local state, executing third-party or project-controlled code, and accessing credentials or sensitive configuration.
>
> Clients should be granted only the permissions, system credentials, tools, and network access necessary to perform the intended task. Where possible, operate within isolated or non-production environments and apply suitable access controls and safeguards around destructive or sensitive operations.
>
> The examples and recommended controls provided are general-purpose starting points, not guarantees of safety, security, correctness, or suitability for any particular environment.


# ENISA's Skills for AI Agents

This repository publishes agentic skills derived from ENISA cybersecurity publications and research.

## Using a skill

A skill directory can be copied into the skill-discovery location used by a compatible agent or development tool.

Example:

```bash
cp -r skills/skill-name <your-agent-skills-directory>/
```

## Licence

© European Union Agency for Cybersecurity (ENISA), 2026 

Unless otherwise noted, the artefacts of this repository are licensed under the EUPL-1.2-or-later licence. See the [LICENSE.txt](./LICENSE.txt) file for details, and check the metadata and licence files associated with each skill before use.

> [!NOTE]
> Unless explicitly stated otherwise, experimental skills in this repository should not be treated as official certification tools, compliance determinations, or automated statements of ENISA policy. Refer to ENISA publications as the authoritative source for recommendations and conclusions.
