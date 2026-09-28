---
name: test-tenant-provisioner
description: 'MANUAL-ONLY; never auto-invoke. Provision and verify repeatable test tenants and users in a named NON-PRODUCTION environment for auth, row-level-security (RLS), integration and end-to-end (E2E) runs. Every created row carries a test marker and unmarked rows are never mutated; validate-only mode (the default) reports drift against the persona catalog, apply mode creates or repairs only marked tenants, users and memberships; credentials are referenced by environment-variable NAME only; capability grants are backup-gated with an inline rollback; a static lint flags test automation that could reach production. WRITES to an environment, so manual invocation only. Use when test tenants or users are missing, drifted or hand-made, or runs fail on stale auth fixtures. Do NOT use to design the persona and data catalog (test-data-architect), write cross-tenant security tests (multi-tenant-security-tester), define the tenant model (tenant-modeler), or store or rotate secrets (secrets-identity-hardener).'
disable-model-invocation: true
---

# Test Tenant Provisioner

**Reading key:** RLS is row-level security (database rules that limit which
rows each tenant can read or write); E2E is end-to-end; CI is continuous
integration; API is application programming interface. A **tenant** is one
customer account in a multi-tenant product. A **persona** is a named test
user with a fixed tenant and role (for example "tenant A owner"). The
**persona catalog** is the written list of test tenants, personas, roles and
their stable identifiers. A **test marker** is a field or tag on a row that
says "this row was created for testing by this tool".

## Purpose

Make the test accounts that auth, RLS, integration and E2E runs depend on
actually exist, in a named non-production environment, exactly as the persona
catalog describes them, and prove they still match. The deliverable is a
provisioning report: a drift table (missing, drifted, orphaned, blocked)
from a read-only validation, and, only when a human explicitly asks for apply
mode and approves the exact plan, a record of the marked rows created or
repaired, each capability grant's backup reference and rollback step, and a
re-validation showing what still differs. It also reports a static lint of
test configuration that could point automation at production. Hand-made test
accounts drift silently; this skill replaces them with one repeatable,
checkable procedure. Built under owner decision D68 (roadmap row #198, as
broadened by D10).

## Use When

- Use when: a human explicitly invokes this skill to check whether the test
  tenants, users, roles and memberships in a named test or staging
  environment still match the persona catalog (validate-only, the default).
- Use when: a human explicitly invokes it to create or repair missing or
  drifted test accounts in a named non-production environment (apply mode).
- Use when: auth, RLS, integration or E2E runs fail because a persona's
  account is missing, has the wrong role, or was hand-edited.
- Use when: test accounts were made by hand and need to be brought under a
  marker convention and a repeatable manifest.
- Use when: someone needs proof that test automation configuration cannot
  reach the production environment (the production-reach lint).
- Do NOT use when: the persona catalog, seeds or factories need DESIGNING —
  that is `test-data-architect`. This skill consumes its catalog; it never
  invents personas.
- Do NOT use when: the ask is to write cross-tenant or authorization negative
  TESTS — `multi-tenant-security-tester` owns the two-tenant fixture's
  required shape and the denial assertions; this skill only makes those
  accounts exist.
- Do NOT use when: the question is what a tenant IS, or how real customer
  tenants are provisioned in the product — `tenant-modeler`.
- Do NOT use when: credentials must be stored, issued or rotated —
  `secrets-identity-hardener`. This skill refers to them by variable name only.
- Do NOT use when: the work is browser auth-state files or Playwright
  fixtures that log these accounts in — `playwright-e2e-engineer`.
- Do NOT use when: the question is whether the RLS policies the accounts
  exercise are correct — `rls-policy-auditor`.
- Do NOT use when: the target is production, or a real customer tenant, for
  any reason. That is refused, not routed (see Stop Conditions).

## Inputs to Inspect

1. **The persona catalog** (`test-data-architect` output): tenants, personas,
   roles, memberships, capability grants and stable identifiers. Missing
   catalog → Stop Conditions.
2. **The target environment declaration:** its name, its host names, its
   database or project identifier, and the declared list of PRODUCTION hosts
   and identifiers to compare against. An environment is non-production only
   on positive evidence, never by its name alone.
3. **The tenant, user, role and membership model** in the product
   (`tenant-modeler` output or the schema): which tables or identity-provider
   objects hold each, and which API or admin path is the supported way to
   create them.
4. **The marker convention:** the field, tag or metadata key that marks a
   test-created row, and its value format. None yet → propose one (see
   [references/provisioning-manifest.md](references/provisioning-manifest.md))
   before any write.
5. **Credential references:** the environment-variable NAMES that hold each
   persona's password, token or key. Never read or print the values.
6. **The backup mechanism** for capability grants (for example an export of
   the current grant rows, a snapshot identifier, or an audit-log reference).
7. **Test automation configuration** for the lint: E2E base URLs, CI job
   environment blocks, seed-script connection settings, `.env.example` or
   environment templates, and test runner configuration files.
8. **The existing current state:** read-only listing of tenants, users,
   memberships and grants in the target environment, if a read path exists.

## Workflow

Explicit human invocation selects this execution-capable skill; it does not
expand the allowed target or activate Task-Authorized Local Implementation
(TALI). TALI is a separate route requiring its own classification and
activation under the [skill-generation standard](../../../docs/skill-generation-standard.md#5-least-privilege--side-effects).
Use applicable existing user grants without repeated consent. Before a
state-changing command, confirm its actual files, environment and effects fit
those grants; if authority is absent, propose the operation and obtain it
before proceeding.

1. **Confirm the catalog.** Load the persona catalog. If none exists, or it
   names personas without stable identifiers, stop and hand off to
   `test-data-architect`. Never invent a persona, role or tenant.
2. **Pin the environment.** Record the target environment's name, hosts and
   database or project identifier. Compare each against the declared
   production list. Classify it NON-PRODUCTION only when every identifier is
   positively different from production; anything unknown or shared is
   treated as production and the run stops.
3. **Build the desired-state manifest.** From the catalog, list every tenant,
   user, role, membership and capability grant with its stable identifier,
   its marker value and, for credentials, the environment-variable NAME that
   holds the secret. Format:
   [references/provisioning-manifest.md](references/provisioning-manifest.md).
4. **Validate (default mode, read-only).** Read the current state and compare
   it with the manifest. Classify every row as one of: OK; MISSING; DRIFTED
   (marked row with a wrong role, membership, tenant or grant); ORPHANED
   (marked row not in the catalog); BLOCKED (an UNMARKED row that collides
   with a catalog identity, such as the same email or tenant slug). Change
   nothing. If no read path exists, say so and mark the state UNVERIFIED.
5. **Run the production-reach lint (static, read-only).** Scan test
   configuration for any base URL, host, connection setting or default value
   that matches a declared production host or identifier, and for
   environment variables whose fallback default points at production. Report
   each hit with file and line. The lint compares declared values; it does
   not resolve names over the network unless that call is separately
   authorized.
6. **Stop here unless apply mode was explicitly requested.** Deliver the
   validation report. Apply mode needs all of: an explicit human request for
   apply, the named non-production environment from step 2, and approval of
   the exact change plan in step 7.
7. **Present the apply plan and obtain approval.** List each create or
   repair with its target row, its marker, and the supported path used (API,
   admin command or migration-safe seed). For each capability grant (a role,
   permission or elevated flag), show the backup reference that will be
   taken first and the inline rollback step beside it. BLOCKED rows are
   listed as untouched with the reason. Deleting ORPHANED marked rows is
   included only when the human asks for it. Wait for approval of this exact
   plan; a changed plan needs fresh approval.
8. **Apply, idempotently, marked rows only.** Create missing rows with the
   marker set at creation. Repair drifted rows only when the marker is
   present. Take each backup before its grant; if the backup fails, skip that
   grant and report it. Never change or delete an unmarked row. Refer to
   credentials by variable name only; if a value would appear in output,
   stop.
9. **Re-validate.** Run step 4 again and report residual drift. Apply is not
   done until the re-validation is shown.
10. **Report** in the Output Format, including what was not done and why.

When provisioning mechanisms are a real choice (for example the product's
admin API versus a database seed script), first define the terms; explain
each option's reason, setup and maintenance cost (or state that it is
unknown), and case-specific pros and cons; recommend one with a reason tied
to the user's context; then ask one question. If a deciding fact is missing,
ask only for that one fact first. A chosen option is not approval to write.

## Output Format

```
TEST TENANT PROVISIONING REPORT — <environment name>
Mode: validate-only | apply (plan approved: <quote + time>)
Environment evidence: <hosts / project id> vs production <list> → NON-PRODUCTION
Catalog: <source path + version>; manifest rows: <n tenants, n users, n memberships, n grants>
Marker convention: <field = value format>
Drift table:
  <row id> | <tenant/user/membership/grant> | OK | MISSING | DRIFTED (<what>) | ORPHANED | BLOCKED (unmarked collision)
Production-reach lint: <file:line — value — matched production identifier> | none found (<files scanned>)
Apply record (apply mode only):
  <row id> — created | repaired | skipped (<why>) — via <path>
  Grant <id> — backup <reference> — rollback: <exact inline step>
Credentials: referenced by variable name only — <VAR_NAME list>
Re-validation: <residual drift or "matches catalog">
Not done: <blocked rows, skipped grants, unverified reads, deletions not requested>
Handoffs: <test-data-architect | multi-tenant-security-tester | secrets-identity-hardener | playwright-e2e-engineer>
```

## Validation Checklist

- [ ] The persona catalog came from `test-data-architect` output; no persona,
      role or tenant was invented.
- [ ] The environment was classified non-production on positive evidence,
      and the evidence is in the report.
- [ ] Validate-only was the default; apply ran only after an explicit request
      and approval of the exact plan.
- [ ] Every created row carries the marker; no unmarked row was changed or
      deleted; BLOCKED rows are listed.
- [ ] Every capability grant has a backup reference and an inline rollback
      step, or is reported as skipped.
- [ ] No credential value appears anywhere in output, manifest or logs; only
      variable names.
- [ ] The production-reach lint ran and lists its scanned files.
- [ ] Re-validation after apply is shown; UNVERIFIED states are named.
- [ ] Any provisioning-mechanism choice explained terms, costs, pros and
      cons, and a recommendation before one question.

## Safety Rules

- Production is never a target. A request, a variable or a configuration
  default that points at production stops the run; no approval converts it.
- The marker is the only permission to touch a row. An unmarked row is
  someone else's data, even when its email or slug matches a persona.
- Credential values are never read into the conversation, written into the
  manifest, or echoed in logs. Missing variables are reported by name.
- Capability grants change who can do what; each one is backup-first with its
  rollback written beside it, so one step reverses it.
- Deletion is never implied by "repair". Removing marked orphans needs its
  own explicit request.

## Gotchas

- A staging database restored from a production backup contains real
  customer rows. They are unmarked, so the marker rule protects them, but
  it also means the environment evidence must check data origin, not only
  the host name.
- Identity providers often key users by email: a hand-made account with a
  persona's email is a BLOCKED collision, not a row to adopt silently.
- Creating users through raw database inserts can skip the identity
  provider, hooks and default memberships, producing accounts the product
  itself could never create. Prefer the product's supported admin path.
- A shared environment used by several teams may hold other teams' marked
  rows; scope the marker value (for example by suite or owner) so ORPHANED
  does not mean "someone else's".
- An E2E failure on a persona login can be the account (this skill) or the
  auth-state fixture (`playwright-e2e-engineer`); validate the account first
  so the two are not confused.
- `.env` defaults are the usual production-reach leak: a variable that falls
  back to the production URL when unset passes every local check.

## Stop Conditions

- The skill was selected automatically rather than explicitly invoked by the
  human: do not execute it. An agent may recommend the named manual skill.
- A write, Git/network operation, database command or test side effect exceeds
  the applicable human grant: stop that operation and obtain the missing scope.
  Existing authorized operations do not need the same permission again.

- The target is production, a real customer tenant, or an environment whose
  identifiers cannot be proven different from production → refuse the write
  and report why; do not offer a workaround.
- No persona catalog exists, or it lacks stable identifiers → stop and hand
  off to `test-data-architect`.
- Apply mode would change or delete an UNMARKED row → do not touch it; report
  it as BLOCKED and ask the human how the collision should be resolved.
- A capability grant's backup cannot be taken, or its rollback step cannot be
  written → skip that grant and report it; never grant without both.
- A credential value would be printed, stored or committed, or is missing →
  stop and report the variable name; custody goes to
  `secrets-identity-hardener`.
- The production-reach lint finds a hit → report it; do not apply against an
  environment whose test configuration can reach production until a human
  decides.
- The apply plan changed after approval → stop and obtain approval for the
  new plan. Creating, repairing, granting or deleting rows is the
  irreversible step this skill guards.

## Supporting Files

- [references/provisioning-manifest.md](references/provisioning-manifest.md)
  — desired-state manifest format, marker conventions, drift classes,
  capability-grant backup and rollback pattern, and production-reach lint
  rules.
- `evals/evals.json` — behavior cases: validate-only drift report, apply with
  backup and rollback, production refusal, unmarked-row block, missing
  catalog, lint hit, credential refusal, and manual-only silence.
- `evals/trigger-evals.json` — discrimination against `test-data-architect`,
  `multi-tenant-security-tester`, `tenant-modeler`, `playwright-e2e-engineer`
  and `secrets-identity-hardener`.
