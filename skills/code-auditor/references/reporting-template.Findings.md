<!--
Template purpose: Generate Findings.md for a project manager, engineering leader, or other decision maker who understands the product at a high level but should not need internal implementation knowledge.
Output filename: Findings.md.
Generation rules:
- Explain product-specific terms the first time they appear. Do not assume the reader knows internal component names, permission models, protocols, or feature flags.
- Use plain-language finding descriptions that state the failed security boundary and the attacker outcome. Avoid vague labels such as "authorization bypass" without saying what can be changed, viewed, or reached.
- Keep the executive summary focused on decisions: what requires action now, what remains unconfirmed, what ownership is needed, and what business or operational risk exists.
- Use ⬜ Informational, 🟨 Low, 🟧 Medium, 🟥 High, or ⬛ Critical for the estimated finding severity.
- Use 🟩 Low, 🟨 Medium, or 🟥 High for reproduce effort, exploit effort, and patch effort.
- Map findings to CWE, OWASP, MITRE and CAPEC frameworks. Do not force a mapping where it is weak or speculative.
- Remove HTML comments from the final report.
- Highlight key words or statements with bold so that stakeholders can skim through the report easily.
Generation workflow:
1. Record the reviewed scope, exact build, tested environment, and verification limitations.
2. Write a plain-language system context and threat model before summarizing findings.
3. Classify each finding by severity, and estimate reproduce, exploit, and patch effort.
4. Fill the executive tables from the validated finding set, then write one readable overview section per finding.
5. Summarize recurring root causes, attack chains only when supported, and the remediation roadmap.
-->

# Findings Report - PROJECT_NAME Security Review

**Date Time:** YYYY-MM-DD hh:mm

**Reviewed Version / Commit:** SHORT_VERSION_CODE_OR_COMMIT

**AI MODEL:** NAME_OF_THE_MODEL (THINKING_MODE_AND_LEVEL)

## Contents

- [Executive Summary](#executive-summary)
- [Findings Overview](#findings-overview)
- [Recommended Triage](#recommended-triage)
- [Scope and Methodology](#scope-and-methodology)
- [System Context](#system-context)
- [Threat Model](#threat-model)
- [Findings Analysis](#findings-analysis)
- [Cross-Finding Themes](#cross-finding-themes)
- [Remediation Roadmap](#remediation-roadmap)
- [Assumptions And Limitations](#assumptions-and-limitations)
- [Appendix](#appendix)

## Executive Summary

<!-- Explain what was reviewed, why it matters to the organization, and the overall security result in one short paragraph. -->

SUMMARY_OF_REVIEW_SCOPE_AND_OVERALL_RESULT.

<!-- State the highest-priority action, the most important confirmed risks, and any important candidates that still need verification. -->

SUMMARY_OF_PRIORITY_ACTIONS_CONFIRMED_RISKS_AND_UNCONFIRMED_CANDIDATES.

### Findings Overview

<!-- Update the variables with the appropriate aggregated number of findings -->
```mermaid
---
config:
  xyChart:
    height: 300
  themeVariables:
    xyChart:
      plotColorPalette: "#414140, #F34435, #FE9900, #FFCC32, #E0E0DF"
---
xychart-beta
    title "Findings"
    x-axis "Severity" [Critical, High, Medium, Low, Informational]
    y-axis "Number of Findings" 0 --> VARIABLE_MAX_NUMBER_OF_FINDINGS_HERE
    bar [VARIABLE_NUMBER_OF_CRITICAL_FINDINGS_HERE, 0, 0, 0, 0]
    bar [0, VARIABLE_NUMBER_OF_HIGH_FINDINGS_HERE, 0, 0, 0]
    bar [0, 0, VARIABLE_NUMBER_OF_MEDIUM_FINDINGS_HERE, 0, 0]
    bar [0, 0, 0, VARIABLE_NUMBER_OF_LOW_FINDINGS_HERE, 0]
    bar [0, 0, 0, 0, VARIABLE_NUMBER_OF_INFORMATIONAL_FINDINGS_HERE]
```

<!-- Keep this table short enough to scan. The Finding column must describe the actual failure and outcome, not only the vulnerability class. -->
<!-- For severity use: ⬜ Informational, 🟨 Low, 🟧 Medium, 🟥 High, or ⬛ Critical -->

| ID | Severity | Finding |
| --- | --- | --- |
| FINDING_ID | SEVERITY | A caller with ATTACKER_ACCESS can SECURITY_FAILURE, which lets them ATTACKER_OUTCOME. IMPACT_IN_BUSINESS_OR_OPERATIONAL_TERMS. |

## Recommended Triage

<!-- This section helps a leader assign work. Sort by business priority, not only by severity. -->

| Priority | ID | Immediate Next Action |
| --- | --- | --- |
| 1 | FINDING_ID | ACTION_REQUIRED_NOW. |

---

## Scope and Methodology

### Reviewed Areas

<!-- Describe product capabilities, not only directory paths. Include paths only when they help scope accountability. -->

- CAPABILITY_OR_COMPONENT_AREA_1.
- CAPABILITY_OR_COMPONENT_AREA_2.
- CAPABILITY_OR_COMPONENT_AREA_3.

### Methodology

<!-- State whether the work included source review, threat modelling, configuration review, runtime testing, PoC execution, manual verification, or other methods. -->

METHODOLOGY_SUMMARY.

### Verification Approach

<!-- Explain how findings were verified and how candidates were handled. -->

VERIFICATION_APPROACH_AND_EVIDENCE_THRESHOLD.

---

## System Context

<!-- Explain the system in terms a project manager can understand: what it does, what it protects, and which administrative or integration boundaries matter. -->

HIGH_LEVEL_SYSTEM_DESCRIPTION.

<!-- Explain important terms used later, such as tenant, realm, client, identity provider, directory provider, delegated administrator, or provisioning API. -->

PLAIN_LANGUAGE_EXPLANATION_OF_RELEVANT_TERMS_AND_BOUNDARIES.

---

## Threat Model

### Assets At Risk

- ASSET_1_AND_WHY_IT_MATTERS.
- ASSET_2_AND_WHY_IT_MATTERS.
- ASSET_3_AND_WHY_IT_MATTERS.

### Relevant Threat Actors

- THREAT_ACTOR_1_WITH_REQUIRED_ACCESS.
- THREAT_ACTOR_2_WITH_REQUIRED_ACCESS.
- THREAT_ACTOR_3_WITH_REQUIRED_ACCESS.

### Trust Boundaries

<!-- Describe the boundary in plain language, for example "a delegated administrator should not become a full realm administrator" or "a public URL supplied by a client should not let the server reach private network services." -->

- TRUST_BOUNDARY_1_AND_EXPECTED_CONTROL.
- TRUST_BOUNDARY_2_AND_EXPECTED_CONTROL.
- TRUST_BOUNDARY_3_AND_EXPECTED_CONTROL.

### Assumptions And Preconditions

<!-- State the deployment conditions that materially change risk, such as enabled features, provider choice, trusted network egress, or delegated administration use. -->

- ASSUMPTION_OR_PRECONDITION_1.
- ASSUMPTION_OR_PRECONDITION_2.
- ASSUMPTION_OR_PRECONDITION_3.

---

## Findings Analysis

<!-- Repeat this subsection once per finding. Keep this section readable without code knowledge. -->

### FINDING_ID: PLAIN_LANGUAGE_FINDING_TITLE

**Severity:** SEVERITY

**Affected Capability:** HIGH_LEVEL_FEATURE_OR_WORKFLOW

#### What Happens

<!-- State the normal behaviour, the failed control, and the attacker outcome in one paragraph. -->

PLAIN_LANGUAGE_DESCRIPTION_OF_THE_SECURITY_FAILURE_AND_OUTCOME.

#### Why It Matters

<!-- Explain the practical consequence for users, administrators, data, operations, or compliance. -->

IMPACT_EXPLAINED_WITHOUT_INTERNAL_IMPLEMENTATION_JARGON.

#### Who Can Exploit It

<!-- State the minimum attacker position and whether user interaction, special configuration, or prior access is required. -->

ATTACKER_PROFILE_AND_REQUIRED_ACCESS.

#### Conditions

<!-- State when the issue applies and when it does not apply. This prevents overgeneralizing feature-gated or provider-specific findings. -->

- Applies when: APPLICABLE_CONDITION.
- Does not apply when: NON_APPLICABLE_CONDITION.

#### Effort

| Activity | Estimate | Rationale |
| --- | --- | --- |
| Reproduce | LOW_MEDIUM_HIGH | WHY_A_DEFENDER_CAN_OR_CANNOT_VERIFY_IT_EASILY. |
| Exploit | LOW_MEDIUM_HIGH | WHY_AN_ATTACKER_CAN_OR_CANNOT_ABUSE_IT_EASILY. |
| Patch | LOW_MEDIUM_HIGH | WHY_THE_FIX_IS_SMALL_OR_REQUIRES_BROADER_DESIGN_OR_TEST_WORK. |

#### Framework Mapping

<!-- Include mappings that lets stakeholders understand impact and techniques. Do not force a mapping where it is weak or speculative. For each framework list all matching codes or ids, names etc. -->

- CWE:
  - CWE_ID_AND_NAME_1_IF_APPLICABLE
  - CWE_ID_AND_NAME_2_IF_APPLICABLE
- OWASP:
  - OWASP_CATEGORY_1_IF_APPLICABLE
  - OWASP_CATEGORY_2_IF_APPLICABLE
- CAPEC:
  - CAPEC_INFO_1_IF_APPLICABLE
  - CAPEC_INFO_2_IF_APPLICABLE
- MITRE:
  - MITRE_INFO_1_IF_APPLICABLE
  - MITRE_INFO_2_IF_APPLICABLE

#### Recommended Next Action

NEXT_ACTION_FOR_OWNER_AND_TRIAGE_TEAM.

---

## Cross-Finding Themes

<!-- Summarize recurring root causes and systemic feedback. This should help leaders fund broad fixes instead of treating every issue as isolated. -->

### Recurring Root Causes

- ROOT_CAUSE_THEME_1.
- ROOT_CAUSE_THEME_2.
- ROOT_CAUSE_THEME_3.

### Generic Feedback

- GENERIC_FEEDBACK_OR_ENGINEERING_RECOMMENDATION_1.
- GENERIC_FEEDBACK_OR_ENGINEERING_RECOMMENDATION_2.
- GENERIC_FEEDBACK_OR_ENGINEERING_RECOMMENDATION_3.

### Potential Attack Chains

<!-- Include this section only when multiple findings can realistically combine. Record confirmed escalation, deployment-dependent amplification, and rejected or conditional chains separately so stakeholders can see what does and does not change severity. Do not invent a chain only to make the report look more severe. -->

ATTACK_CHAIN_DESCRIPTION_OR_NOT_APPLICABLE.

---

## Remediation Roadmap

### Immediate

- IMMEDIATE_ACTION_1.
- IMMEDIATE_ACTION_2.
- IMMEDIATE_ACTION_3.

### Short Term

- SHORT_TERM_ACTION_1.
- SHORT_TERM_ACTION_2.
- SHORT_TERM_ACTION_3.

### Medium Term

- MEDIUM_TERM_ACTION_1.
- MEDIUM_TERM_ACTION_2.
- MEDIUM_TERM_ACTION_3.

---

## Assumptions And Limitations

<!-- State assumptions made, what was not tested, which features or providers were unavailable, and what environmental differences could change the result. -->

- ASSUMPTION_OR_LIMITATION_1.
- ASSUMPTION_OR_LIMITATION_2.
- ASSUMPTION_OR_LIMITATION_3.

---

## Appendix

### Severity Rubric

| Severity | General Meaning |
| --- | --- |
| ⬛ Critical | Exploitation can directly lead to broad compromise, unauthenticated control, or equivalent impact with minimal barriers. |
| 🟥 High | Exploitation can cross an important security boundary, expose sensitive data, or provide meaningful privilege escalation. |
| 🟧 Medium | Exploitation causes a material security weakness but requires additional access, feature enablement, configuration, or chaining. |
| 🟨 Low | Exploitation has limited direct impact, narrow preconditions, or mainly improves an attacker's reliability or information. |
| ⬜ Informational | No exploitable security weakness was identified; use this level for hardening advice, design observations, or other feedback without direct attacker impact. |

### Effort Rubric

| Effort | Reproduce Effort | Exploit Effort | Patch Effort |
| --- | --- | --- | --- |
| 🟩 Low | A standard test deployment and common tools are enough, typically within one hour. | A typical attacker with the stated access can abuse the issue with little custom work. | The fix is localized and can be covered with focused tests. |
| 🟨 Medium | Verification needs custom configuration, a feature fixture, or several manual steps, typically within half a day to two days. | Abuse needs specific knowledge, a non-default feature, or a custom request or script. | The fix touches shared behaviour, compatibility, or multiple tests and needs careful review. |
| 🟥 High | Verification needs a custom provider, external integration, signed fixture, unusual deployment, or extensive setup. | Abuse needs rare access, significant preparation, or multiple chained conditions. | The fix requires design work, migration planning, or broad regression testing. |
