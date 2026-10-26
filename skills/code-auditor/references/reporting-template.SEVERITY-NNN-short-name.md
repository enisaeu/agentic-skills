<!--
Template purpose: Generate one technical report for a single finding for a system administrator, system developer, or component owner.
Output filename: SEVERITY-NNN-short-name.md.
Generation rules:
- Start with a plain-language explanation of the feature and the failed security boundary before discussing code.
- Define every product-specific term, protocol, permission, feature flag, and provider that is required to understand the issue.
- State exact affected conditions, attacker prerequisites, required configuration, tested build, and any feature or provider dependency.
- Include source-backed evidence with file paths, classes, functions, routes, configuration keys, and the relevant data flow from attacker-controlled input to security-sensitive sink.
- Include both automated reproduction and a manual UI or UI-assisted verification path when possible. If no UI path exists, say why and provide the closest administrator workflow plus the required API or browser-console step.
- Use ⬜ Informational, 🟨 Low, 🟧 Medium, 🟥 High, or ⬛ Critical for the estimated finding severity.
- Use 🟩 Low, 🟨 Medium, or 🟥 High for reproduce effort, exploit effort, and patch effort.
- Describe the expected vulnerable result, expected fixed result, and expected not-applicable result separately so operators can interpret their own environment correctly.
- Include cleanup steps for temporary users, clients, providers, files, or configuration added during testing.
- Provide interim mitigations that administrators can apply before a code patch is available.
- Provide two fix recommendations when useful: a quick containment fix and a correct long-term fix that preserves the intended security model.
- Recommend regression tests that prove both the vulnerable path and the intended allowed path.
- Avoid vague conclusions such as "authorization bypass" or "input validation issue" without stating the concrete object, permission, trust boundary, and attacker outcome.
- Highlight key words or statements with bold so that stakeholders can skim through the report easily.
Generation workflow:
1. Establish the affected feature, exact conditions, tested build, and minimum attacker capability.
2. Trace the attacker-controlled source through parsing, validation, authorization, and the security-sensitive sink.
3. Write automated and manual verification steps with vulnerable, fixed, and not-applicable outcomes.
4. Define interim mitigations, then propose a quick containment patch and a correct long-term fix with regression tests.
5. Add framework mappings, remaining questions, and artifact references only after the technical conclusion is stable.
-->

# FINDING_ID: PLAIN_LANGUAGE_FINDING_TITLE

**Severity:** SEVERITY

**Date Time:** YYYY-MM-DD hh:mm

**Reviewed Version / Commit:** VERSION_OR_COMMIT

**AI MODEL:** NAME_OF_THE_MODEL (THINKING_MODE_AND_LEVEL)

**Required Feature Flags / Providers / Configuration:** REQUIRED_FEATURES_OR_NONE

## Executive Summary

<!-- Explain the issue in one paragraph for an administrator or developer who knows the product but not this code path. State normal behaviour, failed control, and attacker outcome. -->

EXECUTIVE_SUMMARY_OF_THE_VULNERABILITY.

## At A Glance

| Field | Value |
| --- | --- |
| Security boundary that fails | SECURITY_BOUNDARY |
| Minimum attacker position | REQUIRED_ATTACKER_ACCESS |
| User interaction required | YES_NO_AND_EXPLANATION |
| Primary impact | PRIMARY_IMPACT |
| Data or assets at risk | ASSETS_AT_RISK |
| Reproduce effort | LOW_MEDIUM_HIGH_WITH_SHORT_REASON |
| Exploit effort | LOW_MEDIUM_HIGH_WITH_SHORT_REASON |
| Patch effort | LOW_MEDIUM_HIGH_WITH_SHORT_REASON |

---

### Root Cause

<!-- 1 to 3 paragraphs explaining the root cause of the vulnerability -->
ROOT_CAUSE_EXPLAINED.

---

## System Context

<!-- Explain what the affected feature does in normal use, who uses it, and why the security boundary exists. -->

PLAIN_LANGUAGE_FEATURE_CONTEXT.

<!-- Define any project/component specific term or keywork that appears later. -->

PLAIN_LANGUAGE_DEFINITION_OF_REQUIRED_TERMS.

---

## Affected Conditions

### Vulnerable When

<!-- Provide information on the conditions or pre-conditions needed for the vulnerability to exist and be exploitable. Include any role, credential, network position, client control, external provider control, or user interaction the attacker needs. -->

- CONDITION_1_REQUIRED_FOR_THE_ISSUE_TO_APPLY.
- CONDITION_2_REQUIRED_FOR_THE_ISSUE_TO_APPLY.
- CONDITION_3_REQUIRED_FOR_THE_ISSUE_TO_APPLY.

### Not Affected When

<!-- Provide information on the conditions under which the vulnerability does not exist or is not applicable -->

- CONDITION_1_THAT_MAKES_THE_ISSUE_NOT_APPLICABLE.
- CONDITION_2_THAT_MAKES_THE_ISSUE_NOT_APPLICABLE.
- CONDITION_3_THAT_MAKES_THE_ISSUE_NOT_APPLICABLE.

---

## Threat Model And Risk

### Relevant Threat Actors

- THREAT_ACTOR_1_AND_WHY_THEY_CAN_REACH_THIS_PATH.
- THREAT_ACTOR_2_AND_WHY_THEY_CAN_REACH_THIS_PATH.

### Assets At Risk

- ASSET_1_AND_SECURITY_CONSEQUENCE.
- ASSET_2_AND_SECURITY_CONSEQUENCE.

### Attack Path

<!-- Describe the path from attacker position to impact in clear steps. Keep each step concrete and tie it to the affected feature. -->

1. ATTACKER_STARTING_POSITION.
2. ATTACKER_CONTROLLED_INPUT_OR_ACTION.
3. FAILED_SECURITY_CONTROL.
4. SECURITY_SENSITIVE_OPERATION_OR_SINK.
5. ATTACKER_OUTCOME_AND_IMPACT.

### Impact

<!-- Explain confidentiality, integrity, availability, authorization, audit, isolation, or operational impact. Include blast radius and whether impact stays inside one tenant, realm, user, or host. -->

DETAILED_IMPACT_AND_BLAST_RADIUS.

### Chaining And Severity Assessment

<!-- State whether the finding can realistically chain into a stronger outcome, what source-backed limits prevent overstatement, and whether the chain changes the severity. Distinguish confirmed escalation, deployment-dependent amplification, and rejected/speculative chains. -->

CHAINING_ANALYSIS_AND_SEVERITY_CALIBRATION.

### Likelihood And Exploitability

<!-- Explain why exploitation is easy or hard in practice, including required knowledge, special fixtures, default configuration, and detection difficulty. -->

LIKELIHOOD_AND_EXPLOITABILITY_ASSESSMENT.

---

## Technical Analysis

### Affected Components

| Component | File / Class / Function / Route | Role In The Failure |
| --- | --- | --- |
| COMPONENT_NAME | `PATH_OR_ROUTE` | HOW_THIS_COMPONENT_PARTICIPATES_IN_THE_ISSUE. |

### Code References

| Lines | File | Issue |
| --- | --- | --- |
| FROM_LINE-TO_LINE | `PATH_TO_FILE` | DESCRIBE_THE_ISSUE_IN_THE_CODE. |

### Trust Boundary

<!-- State the intended security boundary in one sentence and the reason it exists. -->

INTENDED_TRUST_BOUNDARY_AND_EXPECTED_CONTROL.

### Vulnerable Data Flow

<!-- Trace untrusted input from source to sink. Include validation, canonicalization, and authorization checks that are present, missing, or inconsistent. -->

1. Source: ATTACKER_CONTROLLED_SOURCE.
2. Parsing / transformation: HOW_THE_INPUT_IS_PARSED_OR_TRANSFORMED.
3. Validation / authorization: CONTROL_THAT_IS_MISSING_INCOMPLETE_OR_BYPASSED.
4. Sink: SECURITY_SENSITIVE_OPERATION.
5. Result: SECURITY_RELEVANT_OUTCOME.

### Vulnerable Code

<!-- Provide information on each affected / vulnerable code block associated grouped per file, and suggested patch / fix -->

#### ISSUE_TYPE in FILE_PATH:FUNCTION_NAME

File:
```
PATH_TO/AFFECTED_FILE.EXT:LINE_NUMBER
```

<!-- A summary with details on the issue, involved functions, variables etc. -->
SUMMARY_WITH_DETAILS

<!-- Cite exact lines of the affected code -->

Annotated source code:
```LANGUAGE
LINE_NUMBER RELEVANT_CODE
LINE_NUMBER RELEVANT_CODE // COMMENT_WITH_INFORMATION_ON_THE_ISSUE
...
LINE_NUMBER RELEVANT_CODE
LINE_NUMBER RELEVANT_CODE // COMMENT_WITH_INFORMATION_ON_THE_ISSUE
LINE_NUMBER RELEVANT_CODE
```

Suggested patch:
<!-- the source code of a patch to address the finding in patch format -->
```
--- a/PATH_TO_FILE
+++ b/PATH_TO_FILE
@@ -12,34 +23,45 @@
-CODE_TO_REMOVE
+CODE_TO_ADD
```

<!-- provide an explanation on what the patched version does to address the finding -->
EXPLANATION_OF_THE_PATCH

---

## Reproduction And Verification

### Prerequisites

<!-- List exact versions, feature flags, environment variables, fixtures, accounts, permissions, network setup, or generated files required before testing. -->

- PREREQUISITE_1.
- PREREQUISITE_2.
- PREREQUISITE_3.

### Bootstrap Assets Used

<!-- Name the users, clients, roles, groups, providers, mock services, files, or scripts created by bootstrap or setup helpers. State what each asset is used for. -->

- ASSET_NAME_1: PURPOSE.
- ASSET_NAME_2: PURPOSE.
- ASSET_NAME_3: PURPOSE.

### Automated Test

<!-- Provide the command from the repository root or PoC directory and explain what success, failure, unsupported, and not reproduced mean. -->

```bash
COMMAND_TO_RUN_THE_AUTOMATED_TEST
```

AUTOMATED_TEST_INTERPRETATION.

### Manual UI Or UI-Assisted Test

<!-- Give a numbered procedure that a system administrator can follow. Start with login identity and navigation. If an API call is required, explain why the UI alone is insufficient and provide the smallest browser-console or curl step needed. -->

1. MANUAL_STEP_1.
2. MANUAL_STEP_2.
3. MANUAL_STEP_3.
4. MANUAL_STEP_4.
5. MANUAL_STEP_5.

### Expected Vulnerable Result

EXPECTED_RESULT_WHEN_THE_ISSUE_IS_PRESENT.

### Expected Fixed Result

EXPECTED_RESULT_WHEN_THE_ISSUE_IS_FIXED.

### Expected Not Applicable Result

<!-- Explain what an operator should see when the required feature, provider, permission model, or configuration is absent. -->

EXPECTED_RESULT_WHEN_THE_DEPLOYMENT_IS_NOT_AFFECTED.

### Cleanup

- CLEANUP_STEP_1.
- CLEANUP_STEP_2.
- CLEANUP_STEP_3.

---

## How To Check Your Deployment

<!-- This section is for operators who are not running the PoC environment. Give a practical checklist that distinguishes affected, fixed, and not-applicable deployments. -->

1. IDENTIFY_RELEVANT_VERSION_FEATURE_PROVIDER_OR_CONFIGURATION.
2. CONFIRM_WHETHER_THE_ATTACKER_PRECONDITION_EXISTS_IN_THIS_DEPLOYMENT.
3. RUN_THE_MINIMUM_SAFE_VERIFICATION_STEP.
4. COMPARE_THE_RESULT_TO_THE_VULNERABLE_FIXED_AND_NOT_APPLICABLE_OUTCOMES_ABOVE.
5. RECORD_THE_RESULT_AND_ANY_ENVIRONMENT_DIFFERENCE_THAT_COULD_CHANGE_THE_CONCLUSION.

---

## Mitigations Until Patch

<!-- Recommend operational, configuration, permission, network, detection, or process controls that reduce risk before a code fix is deployed. State the tradeoff where the mitigation reduces functionality. -->

- MITIGATION_1_AND_TRADEOFF.
- MITIGATION_2_AND_TRADEOFF.
- MITIGATION_3_AND_TRADEOFF.

---

## Fix Guidance

### Quick Containment Fix

<!-- Describe the smallest safe patch or guard that blocks the demonstrated path. Be explicit about any compatibility or coverage limitations. -->

QUICK_FIX_RECOMMENDATION_AND_LIMITATIONS.

### Correct Long-Term Fix

<!-- Describe the design-level fix that preserves the intended security model across all equivalent entry points, providers, or code paths. -->

LONG_TERM_FIX_RECOMMENDATION.

### Regression Tests

- TEST_1_THAT_PROVES_THE_VULNERABLE_PATH_IS_BLOCKED.
- TEST_2_THAT_PROVES_THE_INTENDED_ALLOWED_PATH_STILL_WORKS.
- TEST_3_THAT_COVERS_VARIANTS_PROVIDERS_OR_EDGE_CASES.

### Migration And Compatibility Notes

<!-- State whether the fix changes API behaviour, admin permissions, feature configuration, external integrations, stored data, or upgrade behaviour. -->

MIGRATION_COMPATIBILITY_AND_ROLLOUT_NOTES.

---

## Detection And Monitoring

<!-- Explain what logs, audit events, metrics, network requests, or configuration changes can indicate attempted or successful abuse. -->

- DETECTION_OPPORTUNITY_1.
- DETECTION_OPPORTUNITY_2.
- DETECTION_OPPORTUNITY_3.

---

## Evidence

<!-- Include concise evidence that lets another engineer validate the conclusion without redoing the entire review. -->

| Evidence Type | Reference | What It Shows |
| --- | --- | --- |
| Source | `PATH_OR_FUNCTION` | SOURCE_BACKED_EVIDENCE. |
| Request / Response | `ARTIFACT_OR_LOG_REFERENCE` | RUNTIME_EVIDENCE. |
| PoC Asset | `SCRIPT_OR_REPORT_PATH` | HOW_TO_REPRODUCE_OR_VERIFY. |

---

## Framework Mapping

<!-- Include mappings that lets stakeholders understand impact and techniques. Do not force a mapping where it is weak or speculative. For each framework list all matching codes or ids, names etc. -->

| Framework | Mapping | Why It Applies |
| --- | --- | --- |
| CWE | CWE_ID_AND_NAME_1 | WHY_THIS_IS_THE_PRIMARY_WEAKNESS_CLASS. |
| CWE | CWE_ID_AND_NAME_2 | WHY_THIS_IS_THE_PRIMARY_WEAKNESS_CLASS. |
| OWASP | OWASP_CATEGORY_1 | WHY_THIS_CATEGORY_IS_RELEVANT. |
| OWASP | OWASP_CATEGORY_2 | WHY_THIS_CATEGORY_IS_RELEVANT. |
| CAPEC | MAPPING_1_OR_NONE | WHY_THIS_ATTACK_PATTERN_OR_BEHAVIOR_IS_RELEVANT. |
| CAPEC | MAPPING_2_OR_NONE | WHY_THIS_ATTACK_PATTERN_OR_BEHAVIOR_IS_RELEVANT. |
| MITRE ATT&CK | MAPPING_1_OR_NONE | WHY_THIS_ATTACK_PATTERN_OR_BEHAVIOR_IS_RELEVANT. |
| MITRE ATT&CK | MAPPING_2_OR_NONE | WHY_THIS_ATTACK_PATTERN_OR_BEHAVIOR_IS_RELEVANT. |

---

## Validation Status And Remaining Questions

<!-- State what was proven, what was not proven, and what additional fixture, version, provider, or test would close the remaining uncertainty. -->

VALIDATION_STATUS_CONFIDENCE_AND_OPEN_QUESTIONS.

---

## Appendix

### Raw Requests, Responses, Or Payloads

<!-- Include only material that helps reproduce or verify the issue. Redact secrets unless the values are disposable PoC fixtures. -->

```http
RAW_REQUEST_RESPONSE_OR_PAYLOAD_IF_NEEDED
```
