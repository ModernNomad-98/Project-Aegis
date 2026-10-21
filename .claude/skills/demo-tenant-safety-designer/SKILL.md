---
name: demo-tenant-safety-designer
description: 'Use when demos use tenant-like environments: design demo tenants that cannot create unsafe records, leak real data, bypass security assumptions or become production accidentally.'
---

# Demo Tenant Safety Designer

Terms: **family 4** - the discipline family in README.md and docs/skills-catalog.md; **read-only** means this skill inspects and returns guidance/records and never edits code or runs production actions.

## Purpose

Design demo-tenant posture and guardrails: keep demo environments clearly non-production, seed only synthetic data, bound mutations, limit roles and access, reset/expire reliably, monitor misuse, and define the rules for converting a demo tenant into a real one.

The skill is **advisory and auto-invocable**. It produces guidance, records and review structure only; it does not edit code, run commands, use the network or grant production authority. Any implementation, execution or approval is a delegated host/user action under existing authority. It composes the nearest owners rather than duplicating them.

## Use When

- Sales or product demos need tenant-like environments.
- A demo environment might contain or leak real customer data.
- Demo tenants need reset, expiry or mutation guardrails.
- A demo tenant could be mistaken for production or be converted accidentally.

**Do not use when:** the request belongs to a named neighbouring owner (see Stop Conditions), or when inspection evidence is unavailable and the question would have to be answered by guessing.

## Inputs to Inspect

- Demo purpose, audience and the journeys the demo must show.
- Data sources available and whether they contain real customer data.
- Environment model and identity/secret separation between demo and production.
- Access paths and role assumptions for demo users.
- Reset/expiry and conversion-to-real requirements.
- Monitoring/alerting ownership for demo-environment misuse.

## Workflow

1. Separate demo identity, data, secrets and infrastructure from production in the design.
2. Define the synthetic seed policy: fixtures, generators and a hard rule against real customer data.
3. Define mutation guardrails: what demos may create, rate limits, resettable-only writes and sandbox boundaries.
4. Define access and role limits for demo users, including support/broker access rules.
5. Design reset and expiry: schedule, idempotent reseeding, teardown and evidence.
6. Define monitoring for misuse/leak signals and the conversion-to-real rules and approvals.
7. Define concrete misuse signals: production DB or secret access, outbound email/payment/webhook attempts, data-volume anomalies, role escalation, export attempts, and the alert owner/escalation path.
8. Return the demo-tenant design, isolation controls, reset/seed plan and safety checks; do not provision anything.

## Output Format

Return, in this order:

1. Demo vs production separation model (identity, data, secrets, infrastructure).
2. Synthetic seed policy and generation rules.
3. Mutation guardrails and sandbox boundaries.
4. Access/role limits and reset/expiry plan.
5. Monitoring signals, residual realism limits and the conversion-to-real approval path.

## Validation Checklist

- Demo and production are separated in identity, data, secrets and infrastructure.
- Seed data is synthetic; no real customer data path exists.
- Mutations are bounded and resettable; guardrails are stated.
- Demo roles/access are limited and audited.
- Reset/expiry is reliable and evidenced; conversion-to-real needs explicit approval.
- No provisioning or live environment mutation is performed by the design.
- Concrete misuse signals and their alert owner/escalation path are defined.

## Gotchas

- A demo tenant with copied production data is a data-leak and compliance incident waiting to happen.
- Reusing production secrets in a demo environment removes the isolation boundary.
- Without an expiry/reset owner, demo tenants silently accumulate and become production-like.
- A demo that can send real emails, payments or webhooks creates real side effects; guard the outbound boundary explicitly.

## Stop Conditions

- The request is cross-tenant leakage review of a real system: route to `tenant-isolation-reviewer`.
- The request is tenant-creation workflow and seeding: route to `tenant-provisioning-designer`.
- The request is executing non-production test-tenant creation: route to `test-tenant-provisioner`.
- The trigger-evals file lists a broader 14-owner discrimination set (all named in the reference Boundaries); the three routes above are the primary Stop Conditions and the broader set is discrimination guidance.
- The caller wants this skill to implement, provision or execute the design: refuse; return the design for the authorized host/user.
- Required evidence (state, data map, policy or configuration) is unavailable: state UNKNOWN and ask instead of inventing it.

## Supporting Files

- [demo-tenant-safety](references/demo-tenant-safety.md) - Demo tenant safety, seeding and reset rules.
- [evals/evals.json](evals/evals.json) - the 6 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 8 positive and 14 negative trigger-discrimination cases against the nearest owners.

**Source:** docs/skills-catalog.md - cat 02 #80 (Batch 2); coverage roadmap #80. The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
