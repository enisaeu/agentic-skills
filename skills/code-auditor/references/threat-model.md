# Source-Backed Threat Model

Build the model from the confirmed scope before candidate discovery. Cite exact paths and symbols for material claims, label inference, and record unknown deployment facts.

## Analyse

Document:

- product purpose, deployment shapes, privileged components, and external integrations;
- assets and required confidentiality, integrity, availability, authorization, isolation, and audit properties;
- unauthenticated, authenticated, delegated, administrative, tenant, supply-chain, and local attacker starting positions that the product makes relevant;
- externally reachable and cross-boundary entry points, including APIs, parsers, files, queues, callbacks, plugins, jobs, import/export paths, and administrative workflows;
- trust boundaries and the control expected at each crossing;
- authorization decisions, deserialisers, interpreters, process execution, filesystem access, network egress, secret access, and privileged state mutation;
- feature flags, providers, build modes, deployment topology, and configuration assumptions that materially change reachability or impact;
- observed root controls and high-risk surfaces that discovery must cover.

Use the four threat-model questions:

1. What is being built?
2. What can go wrong?
3. What controls address it?
4. Is the analysis adequate for the confirmed scope and available evidence?

## `ThreatModel.md` contract

Preserve these sections:

```markdown
# Threat Model — REVIEW_ID

## System And Deployment Context

## Assets And Security Properties

| Asset | Required Security Property | Consequence Of Failure |
| --- | --- | --- |

## Threat Actors And Starting Positions

| Actor | Starting Access | Relevant Goal |
| --- | --- | --- |

## Entry Points And Trust Boundaries

| Entry Point | Trust Boundary | Expected Control | Source Reference |
| --- | --- | --- | --- |

## High-Risk Sinks And Root Controls

## Feature And Configuration Assumptions

## Unknowns And Evidence Limits

## Coverage Priorities

## Adequacy Check

- **What is being built:** ...
- **What can go wrong:** ...
- **What is being done about it:** ...
- **Is the analysis adequate:** ...
```

Do not weaken or delete a section because information is unavailable. State the unknown and how it affects coverage or confidence.

## Exit gate

Close the phase only when all four adequacy questions have source-backed answers, material entry points and boundaries have citations, coverage priorities are actionable, and every placeholder is replaced. Otherwise mark the phase partial or blocked with the missing evidence.
