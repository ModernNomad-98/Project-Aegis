# Preference precedence, ceilings and migration rules

Reference for the user-preference-architect skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Every preference has one owner, scope, type and default.
- Resolution order is single and explicit; no surface computes precedence differently.
- Tenant-policy ceilings are stated and users cannot override them.
- Storage is typed; unknown/invalid keys are handled deterministically.
- Migration and rollback preserve tenant policy; audit/privacy rules stated.
- Every claim is backed by inspected evidence or labeled **assumption**, **UNKNOWN** or **UNRUN**; an empty check is never a PASS.

## 2. When this applies

- Users need settings that override defaults but must not override tenant policy.
- The precedence between global, tenant and user settings is ambiguous.
- Settings storage, typing, migration or rollback is being designed or reviewed.
- A preference change risks crossing into entitlements or authorization decisions.

## 3. Output and evidence rules

1. Preference taxonomy with scope, owner, type and default per key.
2. Precedence/resolution table with the single resolution point.
3. Tenant-policy ceilings and caps/non-overridable controls.
4. Typed storage/schema and unknown-key handling.
5. Migration, rollback and cache-invalidation plan.

The returned record must name the evidence source for each decision, separate verified facts from assumptions, and list what could not be inspected. The skill does not edit files or execute commands; delegated actions go to the host/user or the existing implementation owner under existing authority.

## 4. Boundaries

- Inputs inspected: see the SKILL.md Inputs to Inspect section.
- Tenant semantics and membership model routes to `tenant-modeler`; this skill does not perform that owner's work.
- The feature-flag system and evaluation placement routes to `feature-flag-architect`; this skill does not perform that owner's work.
- Role/permission and object-level authorization routes to `authorization-matrix-designer`; this skill does not perform that owner's work.
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Every preference has one owner, scope, type and default.
- Resolution order is single and explicit; no surface computes precedence differently.
- Tenant-policy ceilings are stated and users cannot override them.
- Storage is typed; unknown/invalid keys are handled deterministically.
- Migration and rollback preserve tenant policy; audit/privacy rules stated.
- No preference is treated as an entitlement or authorization decision.
