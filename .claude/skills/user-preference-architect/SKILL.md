---
name: user-preference-architect
description: 'Use when users need settings overriding defaults: per-user preferences with precedence, tenant-policy ceilings, typed storage, migration and safe rollback without breaking tenant policy.'
---

# User Preference Architect

Terms: **family 4** - the discipline family in README.md and docs/skills-catalog.md; **read-only** means this skill inspects and returns guidance/records and never edits code or runs production actions.

## Purpose

Design a user-preference system with explicit ownership and precedence (user, tenant, global), tenant-policy ceilings that users cannot override, typed storage and schema with migration and rollback, so preferences never become entitlements or silently override tenant policy.

The skill is **advisory and auto-invocable**. It produces guidance, records and review structure only; it does not edit code, run commands, use the network or grant production authority. Any implementation, execution or approval is a delegated host/user action under existing authority. It composes the nearest owners rather than duplicating them.

## Use When

- Users need settings that override defaults but must not override tenant policy.
- The precedence between global, tenant and user settings is ambiguous.
- Settings storage, typing, migration or rollback is being designed or reviewed.
- A preference change risks crossing into entitlements or authorization decisions.

**Do not use when:** the request belongs to a named neighbouring owner (see Stop Conditions), or when inspection evidence is unavailable and the question would have to be answered by guessing.

## Inputs to Inspect

- Defaults, tenant policy and the role/permission model for the product.
- Current settings surfaces, storage and read paths.
- Which controls are tenant-mandated versus user-adjustable.
- Audit, privacy and migration requirements for settings.
- Known consumers of each preference and their fallback expectations.
- Legacy preference values that may now violate a tenant ceiling.

## Workflow

1. Build a preference taxonomy: scope (global/tenant/user), owner, type, default and allowed values.
2. Define the precedence table and the single resolution order (user -> tenant -> global) with per-key overrides only where stated.
3. Define tenant-policy ceilings and non-overridable controls; describe what a user sees when a setting is capped.
4. Choose typed storage and schema, including validation and unknown-key handling.
5. Specify migration from legacy settings and rollback, preserving tenant policy.
6. Define audit, privacy and access rules for preference data, plus cache invalidation on change.
7. Separate lookup precedence from policy enforcement: state exactly where a tenant ceiling wins, and whether an out-of-policy user value is clamped, rejected or disabled (and what the user sees).
8. Define detection of legacy out-of-policy values and the migration path.
9. Return the preference schema, precedence table, policy guards and migration plan; do not implement storage.

## Output Format

Return, in this order:

1. Preference taxonomy with scope, owner, type and default per key.
2. Precedence/resolution table with the single resolution point.
3. Tenant-policy ceilings and caps/non-overridable controls.
4. Typed storage/schema and unknown-key handling.
5. Migration, rollback and cache-invalidation plan.

## Validation Checklist

- Every preference has one owner, scope, type and default.
- Resolution order is single and explicit; no surface computes precedence differently.
- Tenant-policy ceilings are stated and users cannot override them.
- Storage is typed; unknown/invalid keys are handled deterministically.
- Migration and rollback preserve tenant policy; audit/privacy rules stated.
- No preference is treated as an entitlement or authorization decision.
- Lookup precedence and tenant-policy enforcement are distinct and both stated.
- Out-of-policy legacy values have a defined outcome and migration.

## Gotchas

- Preferences silently becoming entitlements is the classic failure: a user setting must never widen access.
- Two surfaces resolving precedence differently creates drift that looks like a bug.
- Uncapped user overrides can violate tenant policy in regulated tenants.
- Un-typed settings storage turns every typo into a support incident.
- Precedence is not policy: a user value must never outrank a tenant ceiling.

## Stop Conditions

- The request is tenant semantics and membership model: route to `tenant-modeler`.
- The request is the feature-flag system and evaluation placement: route to `feature-flag-architect`.
- The request is role/permission and object-level authorization: route to `authorization-matrix-designer`.
- The trigger-evals file lists a broader 14-owner discrimination set (all named in the reference Boundaries); the three routes above are the primary Stop Conditions and the broader set is discrimination guidance.
- The request is cache-key/invalidation policy or notification channel/template UX: route to caching-strategy-designer / notification-webhook-ux-designer.
- The caller wants this skill to implement, provision or execute the design: refuse; return the design for the authorized host/user.
- Required evidence (state, data map, policy or configuration) is unavailable: state UNKNOWN and ask instead of inventing it.

## Supporting Files

- [preference-precedence](references/preference-precedence.md) - Preference precedence, ceilings and migration rules.
- [evals/evals.json](evals/evals.json) - the 6 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 8 positive and 14 negative trigger-discrimination cases against the nearest owners.

**Source:** docs/skills-catalog.md - cat 02 #67 (Batch 2); coverage roadmap #67. The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
