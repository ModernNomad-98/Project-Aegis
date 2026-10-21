# Tenant offboarding sequence, holds and evidence rules

Reference for the saas-offboarding-architect skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Every trigger has an actor and approval requirement.
- Access revocation precedes data operations and is verified.
- Retention/deletion/legal-hold rules are explicit and owner-approved.
- Reversible vs irreversible steps are distinguished; no destructive step is implicit.
- Billing close and ownership transfer are in the ordered flow.
- Every claim is backed by inspected evidence or labeled **assumption**, **UNKNOWN** or **UNRUN**; an empty check is never a PASS.

## 2. When this applies

- A user or tenant is leaving and the exit workflow must be designed.
- Offboarding risks leaving access, data or billing in an inconsistent state.
- Retention, deletion or legal-hold rules need an ordered sequence.
- Ownership transfer or tenant closure needs reversible/irreversible step definitions.

## 3. Output and evidence rules

1. Offboarding trigger/actor matrix.
2. Ordered step sequence with reversible/irreversible classification.
3. Retention/deletion/legal-hold exceptions with owners.
4. Billing-close and ownership-transfer steps.
5. Evidence plan and exception paths.

- Per-trigger branches: user leaves / tenant cancels / ownership change; state which steps apply.
- Last-owner authority: verify a successor or executor before revocation.
- Post-revocation export: authorized generator/deliverer, short-lived access, verification.
- Backups, derived copies and sub-processors: expiry, deletion verification, residual-risk evidence.

The returned record must name the evidence source for each decision, separate verified facts from assumptions, and list what could not be inspected. The skill does not edit files or execute commands; delegated actions go to the host/user or the existing implementation owner under existing authority.

## 4. Boundaries

- Inputs inspected: see the SKILL.md Inputs to Inspect section.
- Route tenant creation/provisioning and lifecycle handoff to `tenant-provisioning-designer`; this skill does not perform that owner's work.
- Route membership/invitation identity flows to `membership-invitation-designer`; this skill does not perform that owner's work.
- Route audit taxonomy and retention of records to `audit-log-architect`; this skill does not perform that owner's work.
- Broader discrimination set from evals/trigger-evals.json: the following owners' requests route away from this skill - `tenant-provisioning-designer`, `membership-invitation-designer`, `audit-log-architect`, `pii-lifecycle-designer`, `tenant-modeler`, `authorization-matrix-designer`, `plan-entitlement-architect`, `data-migration-runbook-author`, `secure-migration-reviewer`, `sensitive-disclosure-guard`, `admin-console-architect`, `incident-response-runbook`, `secrets-identity-hardener`, `saas-cost-architect` (discrimination neighbours, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Every trigger has an actor and approval requirement.
- Access revocation precedes data operations and is verified.
- Retention/deletion/legal-hold rules are explicit and owner-approved.
- Reversible vs irreversible steps are distinguished; no destructive step is implicit.
- Billing close and ownership transfer are in the ordered flow.
- Each step leaves audit evidence; exceptions are defined.
- Per-trigger branches state which steps apply (ownership transfer may skip deletion/closure).
- A successor/executor is verified before the last owner's authority is revoked.
- The post-revocation export delivery channel and verifier are defined.
- Backups, derived copies and sub-processor deletion evidence are covered.
