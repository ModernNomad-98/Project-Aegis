---
name: subscription-lifecycle-designer
description: 'Use when designing/reviewing a subscription lifecycle state machine: trials, upgrades, downgrades, cancellations, renewals, payment-failure grace and entitlement per state; the plan/entitlement matrix and cost modeling stay with plan-entitlement-architect and saas-cost-architect.'
---

# Subscription Lifecycle Designer

Terms: **family 4** - the discipline family in README.md and docs/skills-catalog.md; **read-only** means this skill inspects and returns guidance/records and never edits code or runs production actions.

## Purpose

Design a subscription lifecycle as an explicit state machine: every state, transition, entitlement posture, billing/proration rule, dunning/grace window and cancellation/reactivation path, with idempotent transitions and a rollback plan so a plan change never silently loses data or entitlement.

The skill is **advisory and auto-invocable**. It produces guidance, records and review structure only; it does not edit code, run commands, use the network or grant production authority. Any implementation, execution or approval is a delegated host/user action under existing authority. It composes the nearest owners rather than duplicating them.

## Use When

- A subscription model needs states and transitions defined before billing or access code is written.
- An upgrade, downgrade, cancellation or renewal path has ambiguous entitlement timing.
- Payment failure, dunning or grace handling is undefined or inconsistent with access.
- A lifecycle change must be reviewed for data-loss, grandfathering and rollback safety.

**Do not use when:** the request belongs to a named neighbouring owner (see Stop Conditions), or when inspection evidence is unavailable and the question would have to be answered by guessing.

## Inputs to Inspect

- Plan/entitlement model and the pricing rules the lifecycle must honour.
- Current subscription states, transitions and the records that carry them.
- Billing events available (invoice, payment failure, dunning) and their timing.
- Access-control and entitlement resolution points for each state.
- Existing grandfathering, trial and reactivation decisions.
- Billing-event ordering/retry behaviour (late, duplicate and out-of-order events) and any reconciliation job.

## Workflow

1. State the business model and enumerate subscription states with entry/exit conditions.
2. Build the transition matrix: trigger, actor, idempotency key, side effects, entitlement posture per state.
3. Define proration and timing rules for upgrades, downgrades, cancellations and renewals.
4. Define payment-failure, dunning and grace behaviour, including access during grace and hard-stop rules.
5. Define reactivation, grandfathering and cancellation-timing rules so reversibility is explicit.
6. Specify idempotent transition handling, duplicate-event suppression and rollback for failed transitions.
7. Return the state machine, transition matrix, edge cases and verification plan; do not implement billing code.
8. Define late/out-of-order billing-event handling: ordering keys, deterministic winner and duplicate suppression.
9. Use compensating transactions and reconciliation for external billing transitions that cannot be rolled back literally.

## Output Format

Return, in this order:

1. Subscription state model with entry/exit conditions.
2. Transition matrix (trigger, actor, idempotency, effects, entitlement per state).
3. Proration, dunning/grace, cancellation/reactivation and grandfathering rules.
4. Idempotency and rollback plan for transitions.
5. Edge cases, open questions and verification plan.

## Validation Checklist

- Every state and transition has an observable trigger and entitlement posture.
- Upgrade/downgrade proration and timing are explicit, with data-loss risk stated.
- Payment failure, dunning and grace access rules are defined, including hard stop.
- Cancellation timing, reactivation and grandfathering are explicit and reversible where claimed.
- Transitions are idempotent and duplicate events cannot double-apply.
- No billing implementation or entitlement enforcement is claimed as done.
- Out-of-order and duplicate events have a deterministic, idempotent outcome.
- Irreversible external transitions have a compensating/reconciliation path, not a literal rollback claim.

## Gotchas

- A lifecycle defined only by happy-path transitions hides entitlement drift during grace and dunning.
- Cancellation timing is a data question, not just a billing question; access and retention can diverge.
- Retries and webhook duplicates can double-apply a transition without an idempotency key.
- Grandfathering rules without an end date become permanent accidental entitlements.
- A literal rollback of an external billing charge is usually impossible; design compensation and reconciliation instead.

## Stop Conditions

- The request is the plan x entitlement matrix and one resolution point: route to `plan-entitlement-architect`.
- The request is tenant semantics and lifecycle state machine: route to `tenant-modeler`.
- The request is bill-grounded cost drivers and unit economics: route to `saas-cost-architect`.
- The trigger-evals file lists a broader 14-owner discrimination set; the three routes above are the primary Stop Conditions, and every tested owner is documented in the reference Boundaries section.
- The caller wants this skill to implement, provision or execute the design: refuse; return the design for the authorized host/user.
- Required evidence (state, data map, policy or configuration) is unavailable: state UNKNOWN and ask instead of inventing it.

## Supporting Files

- [subscription-state-matrix](references/subscription-state-matrix.md) - Subscription lifecycle state matrix and evidence rules.
- [evals/evals.json](evals/evals.json) - the 6 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 8 positive and 14 negative trigger-discrimination cases against the nearest owners.

**Source:** docs/skills-catalog.md - cat 02 #61 (Batch 2); coverage roadmap #61. The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
