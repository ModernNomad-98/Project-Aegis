---
name: saas-offboarding-architect
description: 'Use when a user or tenant leaves: design access revocation, data export/retention/deletion, billing close, ownership transfer and audit evidence in one ordered flow.'
---

# SaaS Offboarding Architect

Terms: **family 4** - the discipline family in README.md and docs/skills-catalog.md; **read-only** means this skill inspects and returns guidance/records and never edits code or runs production actions.

## Purpose

Design an ordered offboarding flow for users and tenants: trigger events and actors, immediate access revocation, data export/retention/deletion sequence, billing closure, ownership transfer, legal holds, reversible vs irreversible steps and the audit evidence each step must leave.

The skill is **advisory and auto-invocable**. It produces guidance, records and review structure only; it does not edit code, run commands, use the network or grant production authority. Any implementation, execution or approval is a delegated host/user action under existing authority. It composes the nearest owners rather than duplicating them.

## Use When

- A user or tenant is leaving and the exit workflow must be designed.
- Offboarding risks leaving access, data or billing in an inconsistent state.
- Retention, deletion or legal-hold rules need an ordered sequence.
- Ownership transfer or tenant closure needs reversible/irreversible step definitions.

**Do not use when:** the request belongs to a named neighbouring owner (see Stop Conditions), or when inspection evidence is unavailable and the question would have to be answered by guessing.

## Inputs to Inspect

- Tenant/user state, contracts and retention/legal-hold policy.
- Data map for what must be exported, retained or deleted.
- Billing model and the rules for final invoice/closure.
- Ownership/transfer model and who may approve each step.
- Audit requirements and evidence retention for offboarding.
- Backup expiry, derived-copy inventory and sub-processor deletion evidence.

## Workflow

1. Enumerate trigger events (user leaves, tenant cancels, contract ends) and their actors/approvals.
2. Order the flow: access revocation first, then export, retention, deletion, billing close and ownership transfer.
3. Define what is reversible vs irreversible at each step and who decides.
4. Define legal-hold and retention exceptions with owners and expiry.
5. Specify the records each step must leave and where they are retained.
6. Define exception paths: partial offboarding, cancelled offboarding, failed deletion and idle tenants.
7. Return the offboarding state machine, ordered checklist, evidence plan and exception paths; do not execute deletes.
8. Define per-trigger branches (single user leaves / tenant cancels / merger-ownership change): which steps apply and which are skipped.
9. For a sole-owner departure or ownership change, establish and verify a successor or separately authorized executor BEFORE revoking the last owner's authority; still revoke non-owner access promptly.
10. Define the secure export delivery channel after revocation: who generates/delivers it, the short-lived access method and how it is verified.
11. Cover backups, derived copies and sub-processor deletion verification with residual-risk evidence.

## Output Format

Return, in this order:

1. Offboarding trigger/actor matrix.
2. Ordered step sequence with reversible/irreversible classification.
3. Retention/deletion/legal-hold exceptions with owners.
4. Billing-close and ownership-transfer steps.
5. Evidence plan and exception paths.

## Validation Checklist

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

## Gotchas

- Revoking access after deleting data leaves no owner able to verify the deletion.
- Legal holds silently lost during dev work create compliance exposure.
- A single 'delete tenant' action hides irreversible steps that need explicit approval.
- Offboarding without billing close leaves invoices for a tenant that no longer exists.
- Revoking the last owner before a successor is verified leaves nobody able to authorize the export or complete the transfer.
- Derived copies, backups and sub-processors mean deletion is not complete until their evidence is recorded.

## Stop Conditions

- The request is tenant creation/provisioning and lifecycle handoff: route to `tenant-provisioning-designer`.
- The request is membership/invitation identity flows: route to `membership-invitation-designer`.
- The request is audit taxonomy and retention of records: route to `audit-log-architect`.
- The trigger-evals file lists a broader 14-owner discrimination set; the three routes above are the primary Stop Conditions, and every tested owner is documented in the reference Boundaries section.
- The caller wants this skill to implement, provision or execute the design: refuse; return the design for the authorized host/user.
- Required evidence (state, data map, policy or configuration) is unavailable: state UNKNOWN and ask instead of inventing it.

## Supporting Files

- [offboarding-checklist](references/offboarding-checklist.md) - Tenant offboarding sequence, holds and evidence rules.
- [evals/evals.json](evals/evals.json) - the 6 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 8 positive and 14 negative trigger-discrimination cases against the nearest owners.

**Source:** docs/skills-catalog.md - cat 02 #83 (Batch 2); coverage roadmap #83. The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
