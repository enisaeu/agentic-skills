# Rating Rubrics

Use these labels consistently in candidate, finding, and aggregate artifacts. Explain each selection from demonstrated impact, prerequisites, and evidence.

## Finding Severity

| Label | General meaning |
| --- | --- |
| ⬛ Critical | Direct broad compromise, unauthenticated control, or equivalent impact with minimal barriers. |
| 🟥 High | A meaningful security boundary is crossed, sensitive data is exposed, or privilege materially increases. |
| 🟧 Medium | Material security impact requires additional access, a feature, configuration, or chaining. |
| 🟨 Low | Direct impact is limited, preconditions are narrow, or the weakness mainly improves attack reliability or information. |
| ⬜ Informational | No exploitable weakness is established; use for hardening or design observations. |

Assess severity from the strongest source-backed outcome that applies under stated conditions.
Do not use severity to encode uncertainty.

## Finding Confidence

| Label | General meaning |
| --- | --- |
| 🟩 High | The source-to-sink path, failed control, and outcome are directly evidenced with no material unresolved assumption. |
| 🟨 Medium | The static path is strong but one deployment, configuration, or runtime assumption remains. |
| 🟧 Low | A plausible boundary failure remains, but a material path segment or control behavior is unresolved. |

Suppress or defer a claim rather than using low confidence to preserve a disproved or non-actionable candidate.

## Effort

| Label | Reproduce effort | Exploit effort | Patch effort |
| --- | --- | --- | --- |
| 🟩 Low | Standard test setup and common tools, typically within one hour. | Little custom work for an attacker with the stated access. | Localized change with focused tests. |
| 🟨 Medium | Custom configuration or several manual steps, typically within half a day to two days. | Specific knowledge, a non-default feature, or a custom request or script. | Shared behavior, compatibility work, or several tests. |
| 🟥 High | Custom provider, external integration, signed fixture, unusual deployment, or extensive setup. | Rare access, significant preparation, or multiple chained conditions. | Design work, migration planning, or broad regression testing. |

Rate reproduce, exploit, and patch effort independently and include a concise rationale.
