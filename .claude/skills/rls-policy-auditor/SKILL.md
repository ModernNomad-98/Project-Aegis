---
name: rls-policy-auditor
description: Audit and (where asked) author row-level-security policies for a tenant-scoped database — inspect SELECT/INSERT/UPDATE/DELETE policies per table for missing tenant scope, deny-by-default gaps, policy recursion, unsafe SECURITY DEFINER helpers, over-broad GRANTs, service-role/superuser leakage, and frontend-derived (client-supplied) tenant scope, and ALWAYS deliver a negative-test plan proving wrong-tenant/wrong-role/missing-auth access is denied per command. Use when asked to review, write, or fix RLS/tenant-scoping policies, when RLS is enabled but unverified, or before shipping a tenant table. Do NOT use for app/API-layer isolation tests (multi-tenant-security-tester), general migration review (secure-migration-reviewer), or non-database threat modeling (threat-modeler).
---

# RLS Policy Auditor

**Reading key:** RLS means row-level security; JWT means JSON Web Token;
SQL means Structured Query Language; DDL means data definition language.
`GRANT` assigns database privileges; `BYPASSRLS` lets a database role skip
row policies. PostgreSQL's [row-security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
and [policy](https://www.postgresql.org/docs/current/sql-createpolicy.html)
documentation define the effective behavior described here.

## Purpose

Produce a database-level verdict on whether row-level security actually
enforces tenant and role scope, plus the negative tests that prove it. This
skill absorbs both policy authoring and negative-test design (reconciliation
§3): it inspects each table's SELECT/INSERT/UPDATE/DELETE policies for the
classic failure modes, writes or corrects policies where asked, and ALWAYS
delivers a per-command negative-test plan. RLS enabled needs an effective
policy review: no applicable policy defaults to deny for a role subject to
RLS, while an over-broad permissive policy or client-supplied tenant scope
can expose rows. The deliverable is severity-ranked
findings with the offending policy quoted, remediation, and executable
negative tests as SQL/session sequences.

## Use When

- Use when: asked to review, audit, write, or fix RLS policies or tenant
  scoping at the database layer.
- Use when: RLS is enabled on tenant tables but nobody has verified the
  policies deny cross-tenant access.
- Use when: before shipping a new tenant-owned table, or after adding
  `SECURITY DEFINER` helpers or new GRANTs.
- Use when: converting an RLS finding into a permanent negative test.
- Do NOT use when: the isolation tests belong at the app/API layer across
  many surfaces — that is `multi-tenant-security-tester` (DB and app layers
  are complementary; hand off the non-DB surfaces).
- Do NOT use when: reviewing a whole migration for privilege/destructive
  changes beyond RLS — that is `secure-migration-reviewer` (route the RLS
  portion here).
- Do NOT use when: the ask is design-time threat enumeration —
  `threat-modeler`.
- Do NOT use when: tenant semantics are undefined — `tenant-modeler` first.

## Inputs to Inspect

1. The schema and migrations: `CREATE TABLE`, `ALTER TABLE … ENABLE ROW LEVEL
   SECURITY`, every `CREATE POLICY`, `CREATE FUNCTION`, and `GRANT`. No policy
   text or schema → Stop Conditions.
2. How tenant/user context reaches the database: session settings
   (`current_setting`), JWT claims, `auth.uid()`/`auth.jwt()` equivalents,
   connection roles — and whether that context is server-established or
   client-influenced.
3. The tenant model (`tenant-modeler`) and authorization matrix
   (`authorization-matrix-designer`) — policies are audited against THESE
   definitions of tenant and role, not re-derived here.
4. Roles and their GRANTs: application role, service/`service_role`, anon,
   and any role that BYPASSRLS or owns the tables.
5. Helper functions used inside policies: their `SECURITY` mode, `search_path`,
   and whether they re-query the same table (recursion risk).
6. Existing RLS tests, if any, and prior incidents.

## Workflow

1. **Confirm real policy text exists** and pin the tenant/role definitions
   being enforced. Undefined boundary → stop and route to `tenant-modeler`.
2. **Inventory tables** that hold tenant-owned data; for each, record whether
   RLS is ENABLED, whether it is FORCED (owners bypass otherwise), and which
   policies exist per command. RLS disabled on a tenant table is a finding.
   If RLS is not forced, determine whether the table-owner role can serve
   user-influenced requests; owner bypass is a risk only with a reachable path.
3. **Audit each command separately — SELECT, INSERT, UPDATE, DELETE** — using
   [references/rls-audit-checklist.md](references/rls-audit-checklist.md):
   - **SELECT/USING:** does every row require the caller's tenant scope?
   - **INSERT/effective check:** can a row be written with another tenant's
     id, or no tenant id? No applicable policy denies; an INSERT policy uses
     `WITH CHECK` to permit rows.
   - **UPDATE:** audit both existing-row `USING` and resulting-row checks.
     If `WITH CHECK` is omitted from an UPDATE/ALL policy, PostgreSQL uses
     its `USING` expression for the new row too; inspect the effective
     expression, not just whether the clause is written.
   - **DELETE/USING:** can a caller delete another tenant's rows?
4. **Hunt the classic failure modes:** missing tenant scope; deny-by-default
   gap (permissive policy that ORs open access); **recursion** (policy calls a
   function that selects the same table under RLS); unsafe **SECURITY DEFINER**
   (no fixed `search_path`, broader than needed, returns rows bypassing
   caller scope); over-broad **GRANT** (e.g. `GRANT ALL … TO anon`);
   **service-role leakage** (service role reachable from a client-influenced
   path, or BYPASSRLS role used in request handling); **frontend-derived
   scope** (tenant id taken from a client value the user controls rather than
   a server-established session/JWT claim).
5. **Rank findings.** A confirmed cross-tenant read or write via policy is
   CRITICAL; each needs the concrete path (which command, which caller, which
   client-controlled input). No demonstrable path → cap at medium and name
   the confirming test.
6. **Author/correct policies where asked** — deny-by-default, tenant scope
   from server context, explicit `WITH CHECK` where it makes the write rule
   clearer or different from `USING`, `SECURITY INVOKER`
   helpers with fixed `search_path` unless a DEFINER is justified and minimal.
   Present as a migration for `secure-migration-reviewer` to gate; do not
   apply to a live DB from this skill.
7. **Write the negative-test plan (mandatory)** per command and per failure
   mode: set the session to tenant A, attempt B's rows for SELECT/UPDATE/
   DELETE (expect zero rows / zero affected), attempt INSERT/UPDATE writing
   B's tenant id (expect rejection for the scoped app role), and include
   the positive control (A affects only A's rows). Test anonymous access
   against its intended policy. For service/owner/BYPASSRLS roles, verify
   they are unreachable from client-influenced paths and document any
   separately authorized privileged operation and expected access. Provide
   runnable SQL session sequences.
8. **Deliver** findings, corrected policies (if authored), and the negative
   tests, with an honest list of tables/commands not audited.

## Output Format

```
RLS AUDIT — <database/scope>
Enforced against: <tenant + role definitions (from tenant-modeler / authz matrix)>
Context source: <server session/JWT — or client-influenced (finding)>
Table inventory: <table — RLS enabled? forced? policies per command>
Findings (severity-ranked):
  [CRITICAL|HIGH|MEDIUM|LOW] <table.command> — <failure mode>
    Policy: <quoted policy or "absent">
    Path: <command + caller + client-controlled input → cross-tenant effect>
    Fix: <corrected policy / direction>
Authored/corrected policies (if requested): <SQL — as a migration, ungated>
Negative-test plan (per command):
  <id> — SET context = tenant A; <attempt on B> — EXPECT <0 rows / rejected>
         + positive control: <A on A's rows> — EXPECT allow
Not audited: <tables/commands + why>
Handoffs: <secure-migration-reviewer to gate the migration; multi-tenant-security-tester for app-layer>
```

## Validation Checklist

- [ ] Every tenant table's RLS enabled/forced status recorded; unprotected
      tables flagged.
- [ ] SELECT, INSERT, UPDATE, DELETE audited SEPARATELY per table.
- [ ] Effective INSERT and UPDATE new-row checks verified, including
      UPDATE/ALL implicit `USING` fallback when `WITH CHECK` is absent.
- [ ] Recursion, SECURITY DEFINER search_path, broad GRANTs, service-role
      leakage, and frontend-derived scope each explicitly checked.
- [ ] Every finding quotes the offending policy (or "absent") and states a
      concrete cross-tenant path; CRITICALs have a demonstrable path.
- [ ] Per-command negative tests and positive controls cover the scoped
      application and anonymous roles; privileged-role reachability and
      intended bypass are checked separately.
- [ ] Authored policies are deny-by-default and use server-derived scope;
      delivered as a migration, not applied live.
- [ ] Not-audited list present.

## Security Rules

- RLS enabled with no applicable policy defaults to deny for roles subject to
  RLS; this may block legitimate access but is not cross-tenant exposure.
  Audit the effective command/role policy: permissive policies OR together,
  restrictive policies AND with that grant, and bypass roles/owners may
  avoid RLS unless FORCE is used where applicable.
- Client-supplied / frontend-derived tenant scope in a policy is a finding
  regardless of demonstrated exploit — tenant scope must come from
  server-established session/JWT context.
- `SECURITY DEFINER` helpers without a pinned `search_path` are a finding
  (search-path hijacking); DEFINER is used only where justified and minimal.
- Service-role / BYPASSRLS credentials must not be reachable from request
  handling influenced by end users.
- No RLS finding is suppressed without written rationale via
  `human-approval-boundary`; every audit ships negative tests
  (master-prompt §6).

## Gotchas

- A correct SELECT policy does not prove INSERT safety: inspect the applicable
  INSERT check and role, and test writing another tenant's id.
- UPDATE requires safe existing-row and new-row checks. An omitted explicit
  `WITH CHECK` on UPDATE/ALL reuses `USING`; tenant hopping requires an
  effective check that permits the resulting wrong-tenant row.
- Policies calling a helper that selects the same table re-enter RLS and
  either recurse or silently return nothing under load — test, don't assume.
- `FORCE ROW LEVEL SECURITY` matters when owner-role requests must be
  constrained; without it the owner bypasses policies. Check whether that
  role is reachable from a user-influenced request path.
- PostgreSQL RLS with zero applicable policies denies all rows to roles
  subject to RLS. A permissive policy can grant rows, so read every policy
  and test with the actual application role.
- A DEFINER helper that returns rows to the caller can launder around the
  caller's own RLS — audit what the helper returns, not just that it exists.

## Stop Conditions

- No policy text, schema, or migration is available → stop; this skill does
  not audit RLS from a description.
- Tenant/role semantics are undefined or contested → stop; `tenant-modeler` /
  `source-of-truth-reconciler` first.
- A CRITICAL cross-tenant policy hole is confirmed in a live database → report
  the minimal reproduction immediately; containment is the human's call
  (`human-approval-boundary`) before continuing.
- Asked to APPLY authored policies to a live database → stop; deliver them as
  a migration for `secure-migration-reviewer` and human approval — this skill
  audits and authors text, it does not run DDL on live systems.

## Supporting Files

- [references/rls-audit-checklist.md](references/rls-audit-checklist.md) —
  per-command audit questions, the seven failure-mode catalog with detection
  and fix, and the negative-test session-sequence templates.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against
  `multi-tenant-security-tester`, `secure-migration-reviewer`, and the shipped
  `tenant-isolation-reviewer` (tenant security cluster).
