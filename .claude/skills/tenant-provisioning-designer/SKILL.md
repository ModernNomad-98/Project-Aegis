---
name: tenant-provisioning-designer
description: 'Designs the tenant-creation workflow for a multi-tenant SaaS: entry paths (signup, sales-led creation, import), the creation sequence (idempotent tenant creation, first-owner assignment, seed data, audit events), failure handling (partial-creation rollback, provisioning observability), and the lifecycle handoff. Produces the design only — creates, configures, and executes nothing. Use when asked to design or repair how tenants come into existence: signup flow, sales-led creation, first-owner assignment, seed defaults, failure and retry, or import. Do NOT use for tenant semantics or the lifecycle state machine (tenant-modeler), the platform deployment model (saas-platform-architect), role-grant rules (authorization-matrix-designer), plan selection (plan-entitlement-architect), pipeline mechanics (command-gateway-architect), making test tenants exist (test-tenant-provisioner), the operator console (admin-console-architect), or the audit record schema (audit-log-architect).'
---

# Tenant Provisioning Designer

**Reading key:** SaaS is software as a service. Provisioning is the act of
bringing a tenant into existence: creating the tenant row, assigning its first
owner, seeding its default configuration, and handing it to the lifecycle
model. A first owner is the initial human account that holds the tenant's
owner role; seed data is the default roles, workspaces, settings, and plan
selection a new tenant starts with. An idempotency key makes a creation safe
to retry without creating a second tenant.

## Purpose

Produce the tenant-creation workflow design: which entry paths exist
(self-serve signup, sales-led manual creation, org import/migration), the
creation sequence per path (idempotent tenant creation → first-owner
assignment → seed data → audit events), creation-failure handling
(partial-creation rollback, provisioning-state observability), and the
handoff into `tenant-modeler`'s lifecycle. It creates, configures, and
executes nothing.

## Use When

- Use when: designing or repairing how tenants come into existence — signup, sales-led creation, import.
- Use when: assigning the first owner and the default role/workspace/settings seed.
- Use when: creation can fail partway and needs rollback + observability.
- Use when: tenant import/migration needs a creation-path design.
- Do NOT use when: the ask is tenant semantics or the lifecycle state machine — that is `tenant-modeler` (compose its model).
- Do NOT use when: the ask is the platform deployment model (pooled/siloed/bridge) — that is `saas-platform-architect`.
- Do NOT use when: the ask is who may create/own or role-grant rules — that is `authorization-matrix-designer` (compose its matrix, including the #59 extension's grant ceilings and custom roles).
- Do NOT use when: the ask is plan/entitlement selection mechanics — that is `plan-entitlement-architect`.
- Do NOT use when: the ask is the write-path pipeline mechanics — that is `command-gateway-architect` (compose its idempotency contract, including the different-payload and in-flight policies).
- Do NOT use when: the ask is making TEST tenants exist in an environment — that is `test-tenant-provisioner` *(manual-only)*.
- Do NOT use when: the ask is the operator console surface — that is `admin-console-architect`.
- Do NOT use when: the ask is the audit record schema — that is `audit-log-architect`.

## Inputs to Inspect

1. The tenant model and its lifecycle catalog (`tenant-modeler` output): tenant definition, lifecycle states, and the Provisioning state's declared posture — the workflow hands off into it.
2. The platform deployment model (`saas-platform-architect` output): pooled/siloed/bridge — what "create a tenant" must allocate.
3. The authorization matrix (`authorization-matrix-designer` output, including the #59 extension's grant-ceiling and custom-role rules): who may create/own, and which roles the first owner holds — composed, never restated.
4. The entitlement matrix (`plan-entitlement-architect` output): plan selection and defaults at creation.
5. Existing signup/create code paths and their de facto behavior.
6. The write-path idempotency contract (`command-gateway-architect` output): key source, dedup store, different-payload and in-flight policies — composed, never restated.

## Workflow

1. **Inventory the entry paths.** Self-serve signup, sales-led manual creation, org import/migration — name every path a tenant can be born through.
2. **Design the creation sequence per path.** Idempotent tenant creation (composing `command-gateway-architect`'s contract), first-owner assignment (composing the matrix's grant rules), seed data (default roles/workspaces/settings/plan), and audit events (composing `audit-log-architect`'s taxonomy) — in that order, each step named.
3. **Handle creation failure.** Per step: what can fail, how a partial creation rolls back or resumes, and what the provisioning-state observability shows — no orphaned tenant rows.
4. **Hand off to the lifecycle.** State which lifecycle state the tenant enters after successful provisioning, per `tenant-modeler`'s model.
5. **Emit the design** in the Output Format, stating what was chosen, why, and the main rejected alternative.

## Output Format

Emit the design in the conversation (nothing is written to the repo):

```
PROVISIONING DESIGN — <product>
Entry paths: <self-serve | sales-led | import/migration — each named>
Creation sequence per path:
  <path> — idempotent create (composed gateway contract) → first-owner rule
  (composed matrix grant) → seed plan <roles/workspaces/settings/plan> →
  audit events <composed taxonomy>
Failure handling: <per step: failure mode → rollback/resume → observability>
Lifecycle handoff: <enters state X per tenant-modeler>
Out of scope:
  lifecycle semantics → tenant-modeler; deployment model → saas-platform-architect;
  role grants → authorization-matrix-designer; plan selection → plan-entitlement-architect;
  pipeline mechanics → command-gateway-architect; test tenants → test-tenant-provisioner;
  console surface → admin-console-architect; audit schema → audit-log-architect
Chosen / why / rejected: <the key choices, the reason for each, and the main
  rejected alternative>
```

## Validation Checklist

- [ ] Every entry path has a named creation sequence; none assumed single-path.
- [ ] First-owner assignment composes the authorization matrix (incl. grant ceilings), never restates it.
- [ ] Tenant creation is idempotent-composed (key, dedup, different-payload/in-flight policies), never redesigned.
- [ ] Partial-creation failure has a rollback/resume per step; no orphaned tenant rows.
- [ ] Seed data is enumerated and reviewed, not inherited by accident.
- [ ] The design claims to create, configure, or execute nothing.

## Gotchas

- Provisioning drift vs the lifecycle model: the workflow invents states the model does not have, or skips ones it does. Compose the model; do not extend it here.
- Seed data becomes de-facto defaults nobody reviews — every seeded role/workspace/setting needs an owner and a review point.
- Partial creation without rollback orphans tenant rows: the idempotency contract makes retries safe, but a half-seeded tenant still needs a resumable state.
- Conflating provisioning with suspension/offboarding: bringing a tenant into existence is not the same as pausing or deleting one — the lifecycle owns those.
- Creating test tenants in an environment is `test-tenant-provisioner`'s (manual-only) job — this skill designs the workflow, it makes nothing exist.

## Tenant Isolation Rules

- Creation is tenant-scoped by construction: a new tenant's seed data, defaults, and identifiers never reference another tenant's data.
- Seed data never seeds another tenant's identifiers, names, or configuration — it is generic or explicitly owned by the creating context.
- Provisioning-state observability reports state and failure without leaking one tenant's data to another (or to the operator console beyond its policy).

## Stop Conditions

- No tenant model exists or is findable → stop; `tenant-modeler` runs first — the workflow hands off into a model that must already exist.
- The ask becomes executing creations, writing pipeline code, or provisioning real tenants → implementation is a separate task; this skill designs only.
- The ask involves live-state mutation or destructive action → stop and refuse.

## Supporting Files

- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `tenant-modeler`, `saas-platform-architect`, `authorization-matrix-designer`, `plan-entitlement-architect`, `command-gateway-architect`, `admin-console-architect`, `test-tenant-provisioner`, and `audit-log-architect`.
- `references/` — None: the design is self-contained.
