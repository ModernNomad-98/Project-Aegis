---
name: model-routing-policy
description: 'Choose and assign models for a task by capability rather than model name: lightweight, balanced, advanced and independent-verification roles; runtime host capability inventory; least costly sufficient role; no hardcoded model, family, provider or version names; never lower verification quality to save cost; independent verification requires a different model and a separate agent or instance, and hosts with one model or no chooser must record and surface the limitation rather than claim separation. Use when dispatching or routing a task, choosing a model or reasoning effort, or deciding whether verification is independent. Do NOT use to select provider credentials or to claim model quality, cost savings or independence the host does not expose.'
---

# Model Routing Policy

**Reading key:** capability-based, model-agnostic decision contract for choosing and assigning models; no model names or versions, and no claim that Aegis can control the host's model selector.

## Purpose

This skill is the single authoritative routing policy for Aegis work: classify a task into a capability role, choose and record the model honestly, and never claim independence, quality or cost the host does not expose. Other skills cite this skill and do not restate it.

## Use When

- Use when: dispatching or routing a task, choosing a model or reasoning effort, or deciding whether verification will be independent.
- Do NOT use when: selecting provider credentials or configuration; claiming measured model quality, cost savings or independence the host does not expose; or substituting for the repository's approval and authority gates.

## Inputs to Inspect

- The task and its risk, plus whether independent verification is required.
- The host's available-model capability inventory as exposed at runtime.
- The host's effort controls and any opaque labels the host supplies.

## Workflow

Apply the policy stated in Purpose; this Workflow does not restate its scope. It is a decision contract for choosing models; it does not claim that Aegis can control the host's model selector.

Classify the task into one of four capability roles (roles, not model names):
- **Lightweight** - routine extraction, formatting, summarising, log scanning.
- **Balanced** - coding, debugging, implementation, tests, routine technical work.
- **Advanced** - architecture, planning, complex analysis, security, strategy.
- **Independent verification** - audit, adversarial review, code review, validation.

If a task spans roles, apply the highest-risk role and use independent verification for the verification step.

At dispatch:
1. Classify the task and note whether independent verification is required.
2. Obtain the host's available-model capability inventory at runtime. Do not hardcode model, family, provider or version names in this policy. A local capability map is data, not policy; store only opaque labels if a host supplies them, and never store secrets.
3. Choose the least costly role that is sufficient on demonstrated capability, reliability, latency and cost. Default advanced tasks to the host's medium effort setting (or its equivalent) - the host's medium effort is the default for advanced work, escalated when complexity or risk justifies it. Never accept lower verification quality to reduce cost.
4. For independent verification, use a model different from the implementer and a separate agent/instance. If the host exposes only one model, or cannot show the choice, do not claim independent verification: record the limitation and surface it. High-risk verification without a distinct model is an owner decision or a stop, never a silent pass.
5. If the host exposes no model chooser, state that plainly, continue only with the limits this creates, and do not fabricate separation.
6. Record in the existing turn/handoff/evidence: capability role, host-provided opaque label only if exposed, effort, rationale, and whether independence was available. Do not add a file, do not change the project-state schema, and do not store provider credentials or other secrets.
7. Model upgrades or replacements must not require policy changes; re-check the host inventory instead of editing this policy.
8. This policy is guidance, not a measurement or guarantee: do not claim model quality, cost savings, or independence beyond what the host actually exposes.

Examples (role-based, never names): routine log extraction -> lightweight; requirements work or implementation -> balanced; architecture/security/threat modelling -> advanced; validation, final review or audit -> independent verification.

## Output Format

- Record in the existing turn/handoff/evidence: the capability role, the host-provided opaque label only if exposed, the effort, the rationale, and whether independent verification was available (and the limitation when it was not).
- Do not add a file, do not change the project-state schema, and do not store provider credentials or other secrets.

## Validation Checklist

- A capability role is named and matches the task's risk.
- No model, family, provider or version name is hardcoded.
- The chosen role is the least costly one sufficient on demonstrated capability, reliability, latency and cost.
- Verification is called independent only when a different model and a separate agent/instance were actually used; otherwise the limitation is recorded and surfaced.
- High-risk verification without a distinct model is an owner decision or a stop, never a silent pass.
- No claim of model quality, cost savings or independence beyond what the host exposes.

## Gotchas

- Independent verification on the same model or a combined agent is not independent; record the limitation instead.
- A host with one model is not a failure by itself; pretending the verification was distinct is.
- A local capability map is data, not policy: store only opaque labels and never secrets.
- Upgrades or renames must re-read the host inventory, not edit this policy.

## Stop Conditions

- Stop unless the owner has explicitly decided to proceed with the limitation recorded.
- The host cannot show the model choice and the work would be reported as independently verified.
- The policy would need a hardcoded model, family, provider or version name.

## Supporting Files

- No references: this skill is self-contained, and `project-orchestrator/SKILL.md` points here as the single routing policy.
