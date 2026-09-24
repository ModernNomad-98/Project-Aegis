# RLS Audit Checklist — per command, failure modes, negative tests

Use this [RLS policy auditor](../SKILL.md) checklist to inspect each table's
four commands and design wrong-tenant negative tests. **RLS** means row-level
security; **JWT** means JSON Web Token; **API** means application programming
interface. This is Postgres-oriented, but the reasoning transfers to any
policy-based row security. RLS enabled is not RLS enforced.

## Per-command audit questions

### SELECT (`USING`)
- Does the predicate require the caller's tenant scope on EVERY row?
- Is the scope from server context (`current_setting('request.jwt.claims')`,
  `auth.uid()`, session var set by the app) — not a client-passed column value?
- Any permissive policy that ORs in broader access (e.g. `USING (true)` for a
  role that end users can reach)?

### INSERT (`WITH CHECK`)
- Is there an applicable INSERT/ALL policy and what is its effective
  new-row check? No applicable policy defaults to deny; an INSERT policy
  needs `WITH CHECK`, while an ALL policy may reuse `USING`.
- Does the effective check force `tenant_id = <server-derived caller tenant>`?
- Can the client supply `tenant_id`/`owner_id` and have it honored?

### UPDATE (`USING` AND `WITH CHECK`)
- `USING` restricts WHICH rows can be updated (caller's tenant only)?
- Does the effective new-row check restrict the RESULTING row? For an
  UPDATE/ALL policy, omitted `WITH CHECK` reuses `USING`; an unsafe
  effective expression, not mere omission, permits tenant hopping.

### DELETE (`USING`)
- Can the caller delete only their tenant's rows? Any role with unrestricted
  delete?

## Seven failure modes (detect → fix)

1. **Missing tenant scope** — policy predicate omits tenant. *Fix:* add
   `tenant_id = <server ctx>` to USING/WITH CHECK.
2. **Deny-by-default gap** — RLS enabled but a permissive policy reopens
   access, or a role has BYPASSRLS. *Fix:* restrictive policies; remove
   BYPASSRLS from request-path roles.
3. **Policy recursion** — policy calls a function that SELECTs the same table
   under RLS. *Fix:* mark helper `SECURITY DEFINER` with a pinned
   `search_path` and query a non-recursive source, or restructure.
4. **Unsafe SECURITY DEFINER** — DEFINER helper without `SET search_path`,
   broader than needed, or returning rows that bypass caller scope. *Fix:*
   pin `search_path`, least privilege, return only caller-scoped rows; prefer
   `SECURITY INVOKER` unless DEFINER is justified.
5. **Over-broad GRANT** — `GRANT ALL`/`GRANT … TO anon`/public. *Fix:* grant
   least privilege per role; anon gets only what's intentionally public.
6. **Service-role leakage** — `service_role`/superuser/BYPASSRLS reachable
   from user-influenced request handling, or its key exposed to the client.
   *Fix:* confine service role to trusted server jobs; never in client path.
7. **Frontend-derived scope** — tenant/user id taken from a client-controlled
   value. *Fix:* derive scope from verified session/JWT claims server-side.

## Negative-test session sequences (mandatory deliverable)

Express each as a session that sets the caller context, then attempts a
forbidden action, with the expected result. Include a positive control.
The SQL below is an illustrative plan for **synthetic fixtures in an isolated,
disposable non-production database**. It includes write statements to expose
policy failures. Do not paste it into a live or customer database. Run each
adapted case in a separate transaction or savepoint that is rolled back, and verify the fixture is
unchanged afterward. Skip execution if triggers or external effects cannot be
isolated or reversed. This skill delivers the plan, not live execution.

Run these checks as the application's actual restricted database role with
verified synthetic session claims. A claim setting by itself does not switch
database roles, and the owner, superuser and `BYPASSRLS` roles can bypass
row-level security. Expected statement errors abort a PostgreSQL transaction
until it is rolled back to a savepoint or restarted.

```sql
-- SELECT isolation
-- Connect as the restricted member role used by the application.
SET request.jwt.claims = '{"tenant_id":"A", "role":"member"}';
SELECT count(*) FROM invoices WHERE tenant_id = 'B';   -- EXPECT 0
SELECT count(*) FROM invoices WHERE tenant_id = 'A';   -- positive control: > 0

-- INSERT write-side
-- Use a separate transaction/savepoint; roll back after the expected error.
SET request.jwt.claims = '{"tenant_id":"A"}';
INSERT INTO invoices (tenant_id, amount) VALUES ('B', 100);  -- EXPECT rejected

-- UPDATE tenant hop
UPDATE invoices SET tenant_id = 'B' WHERE id = '<A-row>';     -- EXPECT rejected/0

-- DELETE cross-tenant
DELETE FROM invoices WHERE tenant_id = 'B';                   -- EXPECT 0 affected

-- Reconnect or SET ROLE as the actual restricted anonymous role.
RESET request.jwt.claims;  -- clears claims; does not itself change DB role
SELECT count(*) FROM invoices;                               -- EXPECT 0 (or only public)
```

Adapt the context-setting mechanism to the project (Supabase JWT claims,
`SET LOCAL app.tenant_id`, connection role, etc.). Every table × command that
matters gets a row; the not-audited list captures the rest. Audit separately
whether owner, service and BYPASSRLS roles can be reached from a
client-influenced path; do not expect their intended privileged operations
to be denied by row policies that they bypass.

## Handoffs

- Authored/corrected policies → deliver as a migration for
  `secure-migration-reviewer` + human approval; never apply live from here.
- App/API/cross-surface isolation tests → `multi-tenant-security-tester`.
