---
name: authorization-matrix-designer
description: Design authorization for multi-tenant software as a service (SaaS) as an explicit roles × permissions × resources matrix. Include object-level rules, enforcement points, deny-by-default behavior, brokered support access, negative tests, and a safe migration and rollback plan. Use when roles or permissions need design or repair. Do NOT use for plan entitlements (plan-entitlement-architect), audit records (audit-log-architect), or row-level security (RLS) policy review (rls-policy-auditor).
---

# Authorization Matrix Designer

Here, **RBAC** means role-based access control, **UI** means user interface,
**API** means application programming interface, **SQL** means Structured
Query Language, **IDOR** means insecure direct object reference, and **QA**
means quality assurance. **SOC 2** means System and Organization Controls 2;
**ISO/IEC 27001** is the information-security management standard published
by the International Organization for Standardization and International
Electrotechnical Commission.

## Purpose

Produce an authorization model where every allow is written down and
everything else is denied: a roles × permissions × resources matrix, the
object-level rules that stop cross-tenant and cross-user reach-through, a map
of exactly where each check is enforced, brokered rules for support and
impersonation, and negative tests for the denials that matter. The discipline:
authorization is a designed matrix with enforcement points, not an
accumulation of `if (user.isAdmin)` checks discovered later by a pen test.

## Use When

- Use when: designing roles and permissions for a new product or feature
  area, or overhauling a grown-wild permission system.
- Use when: authorization decisions are scattered — some in UI, some in
  handlers, some in SQL — and behave inconsistently across surfaces.
- Use when: adding a sensitive capability (billing changes, data export, member
  removal, API keys) that needs an explicit permission and a denial test.
- Use when: support/admin staff need access to tenant data and the rules for
  it don't exist yet.
- Do NOT use when: the gate is commercial — "is feature X in the Pro plan" is
  `plan-entitlement-architect`. A request may need both; keep the axes
  separate: role says CAN, plan says INCLUDED.
- Do NOT use when: designing the audit record of actions taken — that is
  `audit-log-architect` (this skill only requires that high-privilege grants
  emit audit events).
- Do NOT use when: tenant semantics/membership are undefined — run
  `tenant-modeler` first; roles attach to memberships.
- Do NOT use when: the task is the operator CONSOLE that enforces policy
  (tiers, break-glass, impersonation mechanics) — that is
  `admin-console-architect`, which enforces the matrix this skill authors;
  a subordinate per-user row-FILTER scope axis below tenant_id
  (`intra-tenant-scope-architect`, a filter a role carries, not a
  permission); or anyone-with-the-link bearer access for NON-members
  (`share-link-access-architect`, a capability, not member RBAC).

## Inputs to Inspect

1. The tenant model — especially the membership model, since roles attach to
   memberships (tenant-modeler output).
2. Existing authorization code: role enums/tables, permission checks in
   middleware/handlers/UI, ad-hoc `isAdmin`/`isOwner` conditionals.
3. The resource inventory: every tenant-owned resource type and the sensitive
   actions on each (export, delete, share, invite, billing, keys).
4. Every enforcement surface that exists: UI, API routes, service layer,
   background jobs, integrations/webhooks, admin console.
5. Current support/staff access practice — what actually happens today when
   support needs to see tenant data.
6. Compliance requirements naming access control (SOC 2, ISO/IEC 27001, customer
   contracts demanding least privilege or access reviews).

## Workflow

When a sensitive permission policy needs an owner choice, define the roles,
resource, and action; compare viable grants and restrictions by reason, user
benefit, security drawback, and money/setup/upkeep cost or uncertainty.
Recommend the least-privilege fit with context before one decision question;
the answer does not authorize widening access or implementing the matrix.

1. **Inventory resources and actions.** Every tenant-owned resource type ×
   its actions, flagging the sensitive ones. This is the matrix's column
   space; an action not in the inventory cannot be secured.
2. **Inventory actors.** Tenant roles (owner, admin, member, guest — per the
   tenant model), platform/staff roles, service accounts, API keys/machine
   actors. Platform roles that can cross tenant boundaries get enumerated
   individually — they are the dangerous ones.
3. **Build the matrix**: role × permission × resource, deny-by-default —
   cells are explicit allows; absent means denied. Use the template in
   [references/authorization-matrix-template.md](references/authorization-matrix-template.md).
   Keep permissions named as verb-resource pairs, not role names.
4. **Write the object-level rules.** Role checks answer "may this role do
   this action"; object rules answer "on THIS resource" — membership in the
   owning tenant, ownership of the object, sharing grants. Every tenant-owned
   resource gets an object rule; endpoint-level checks alone are an IDOR
   design.
5. **Map enforcement points.** For each surface (UI, API, service, jobs,
   integrations): where the check runs and which layer is authoritative. UI
   hides, API enforces — write that down. Jobs and integrations enforce the
   same matrix; they are not exempt.
6. **Design brokered access**: support/impersonation is explicit-grant,
   scoped to a tenant, time-boxed, visible to the tenant where promised, and
   every use emits an audit event. Raw production access is not a support
   role.
7. **Define the negative-test plan**: for each sensitive permission and each
   privileged role boundary, a test where the disallowed actor attempts the
   action and the expected result is denial — including revoked-membership,
   cross-tenant, and expired-impersonation cases (catalog in references).
8. **Plan migration and rollback** for role changes: introduce new
   permissions additively, dual-check (old and new logic in shadow
   comparison) before cutover. A revert flag is usable only if the old
   check still passes deny-by-default and cross-tenant negative tests;
   otherwise halt and obtain an approved safer rollback. Never widen a
   role's reach silently — widening is a change the human approves.

## Output Format

```
AUTHORIZATION DESIGN — <scope>
Actor inventory: <tenant roles / platform roles (cross-tenant ones flagged) /
  machine actors>
Resource-action inventory: <resource × actions; sensitive actions flagged>
Matrix: role × permission × resource (explicit allows; deny by default)
Object-level rules: <resource → rule (membership/ownership/grant)>
Enforcement-point map: <surface → where the check runs → authoritative layer>
Brokered access rules: <grant, scope, time-box, visibility, audit event>
Negative-test plan: <actor — attempted action — expected denial>
Migration & rollback: <additive introduction → shadow dual-check → cutover →
  tested safe revert or halt; widenings requiring approval listed>
Assumptions & open questions: <each with risk-if-wrong / who answers>
Owner choice (if needed): <terms, viable permission options, costs/unknowns, pros/cons, recommendation + why>
```

## Validation Checklist

- [ ] Any owner-facing permission choice is explained with costs and tradeoffs
      before one question; the answer is not treated as implementation approval.

- [ ] Deny-by-default stated and structural: the matrix contains allows only;
      nothing is "allowed unless".
- [ ] Every tenant-owned resource has an object-level rule, not just an
      endpoint/role check.
- [ ] Every surface — including background jobs and integrations — appears in
      the enforcement-point map with an authoritative layer.
- [ ] Cross-tenant-capable platform roles are individually enumerated with
      audit requirements.
- [ ] Support/impersonation is grant-based, scoped, time-boxed, and audited.
- [ ] Every sensitive permission has at least one negative test; revoked and
      cross-tenant cases are covered.
- [ ] Role migrations are additive with shadow dual-check; any revert path
      passes denial and cross-tenant tests; silent widenings: none.
- [ ] Authorization (role CAN) is not conflated with entitlement (plan
      INCLUDES) anywhere in the matrix.

## Security Rules

- Deny by default; an unlisted permission is a denied permission.
- UI hiding is never authorization; the authoritative check lives at or below
  the API/service layer, and the map says where.
- Object-level authorization is required for every tenant-owned resource —
  the IDOR class is designed out, not patched out.
- Every high-privilege grant, escalation, and impersonation use emits an
  audit event (schema via `audit-log-architect`).
- Negative tests are part of the design deliverable, not a QA afterthought.

## Tenant Isolation Rules

- Tenant roles never grant reach outside their tenant; role checks compose
  with tenant scoping (from `multi-tenant-data-architect`) — they do not
  replace it.
- Roles attach to memberships, so a user's power in tenant A says nothing
  about tenant B; revoking the membership revokes the role's effect
  everywhere, including active sessions and tokens (state the mechanism).
- Platform roles that cross tenants are the exception, enumerated and
  audited; "platform admin can do everything silently" is a finding.

## Gotchas

- Permission checks copy-pasted per handler drift within months; the matrix
  is only real if enforcement flows through a shared decision point.
- Role explosion ("billing-admin-readonly-eu") signals entitlement or scoping
  concerns leaking into roles — factor them back out to the right axis.
- Machine actors (API keys, service accounts) inheriting a human's role
  outlive the human's departure; they get their own rows in the matrix.
- Revocation is the forgotten path: removing a role/membership must be tested
  against live sessions, cached permissions, and issued tokens.
- The admin console tends to grow checks of its own that bypass the shared
  decision point — it is a surface in the map like any other.

## Stop Conditions

- Tenant/membership model undefined → stop; `tenant-modeler` first — roles
  have nothing to attach to.
- A requested role or rule would cross the tenant boundary or widen an
  existing role's reach → `human-approval-boundary` with the blast radius
  before it enters the matrix.
- Business ambiguity about who should hold a sensitive permission → present
  the explained options and a least-privilege recommendation; do not assign
  sensitive defaults silently.
- Asked to implement the permission system in the same pass → separate,
  scoped implementation task; this skill delivers the design and tests plan.

## Supporting Files

- [references/authorization-matrix-template.md](references/authorization-matrix-template.md) —
  matrix and enforcement-map templates, permission naming convention, and the
  negative-test catalog (IDOR probes, revocation, impersonation expiry).
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `audit-log-architect`,
  `api-event-architect` (access & events cluster) and the entitlement axis
  (`plan-entitlement-architect`).
