# Subscription lifecycle state matrix and evidence rules

Reference for the subscription-lifecycle-designer skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Every state and transition has an observable trigger and entitlement posture.
- Upgrade/downgrade proration and timing are explicit, with data-loss risk stated.
- Payment failure, dunning and grace access rules are defined, including hard stop.
- Cancellation timing, reactivation and grandfathering are explicit and reversible where claimed.
- Transitions are idempotent and duplicate events cannot double-apply.
- Every claim is backed by inspected evidence or labeled **assumption**, **UNKNOWN** or **UNRUN**; an empty check is never a PASS.

## 2. When this applies

- A subscription model needs states and transitions defined before billing or access code is written.
- An upgrade, downgrade, cancellation or renewal path has ambiguous entitlement timing.
- Payment failure, dunning or grace handling is undefined or inconsistent with access.
- A lifecycle change must be reviewed for data-loss, grandfathering and rollback safety.

## 3. Output and evidence rules

1. Subscription state model with entry/exit conditions.
2. Transition matrix (trigger, actor, idempotency, effects, entitlement per state).
3. Proration, dunning/grace, cancellation/reactivation and grandfathering rules.
4. Idempotency and rollback plan for transitions.
5. Edge cases, open questions and verification plan.

- Late/out-of-order events: ordering key, deterministic winner, duplicate suppression.
- External transitions: compensating entry, reconciliation evidence, no literal rollback claim.

The returned record must name the evidence source for each decision, separate verified facts from assumptions, and list what could not be inspected. The skill does not edit files or execute commands; delegated actions go to the host/user or the existing implementation owner under existing authority.

## 4. Boundaries

- Inputs inspected: see the SKILL.md Inputs to Inspect section.
- Route the plan x entitlement matrix and one resolution point to `plan-entitlement-architect`; this skill does not perform that owner's work.
- Route tenant semantics and lifecycle state machine to `tenant-modeler`; this skill does not perform that owner's work.
- Route bill-grounded cost drivers and unit economics to `saas-cost-architect`; this skill does not perform that owner's work.
- Broader discrimination set from evals/trigger-evals.json: the following owners' requests route away from this skill - `plan-entitlement-architect`, `tenant-modeler`, `saas-cost-architect`, `api-event-architect`, `audit-log-architect`, `authorization-matrix-designer`, `admin-console-architect`, `notification-webhook-ux-designer`, `data-migration-runbook-author`, `release-readiness-reviewer`, `secure-migration-reviewer`, `feature-flag-architect`, `incident-response-runbook`, `observability-by-design` (discrimination neighbours, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Every state and transition has an observable trigger and entitlement posture.
- Upgrade/downgrade proration and timing are explicit, with data-loss risk stated.
- Payment failure, dunning and grace access rules are defined, including hard stop.
- Cancellation timing, reactivation and grandfathering are explicit and reversible where claimed.
- Transitions are idempotent and duplicate events cannot double-apply.
- No billing implementation or entitlement enforcement is claimed as done.
- Out-of-order and duplicate events have a deterministic, idempotent outcome.
- Irreversible external transitions have a compensating/reconciliation path, not a literal rollback claim.
