# Test Data Patterns

Detail file for `test-data-architect`. Loaded on demand.

## Persona catalog template

| Persona | Tenant | Role | Stable identifier | Notes |
| --- | --- | --- | --- | --- |
| owner-t1 | tenant-1 | owner | owner@t1.test | billing-capable |
| admin-t1 | tenant-1 | admin | admin@t1.test | |
| member-t1 | tenant-1 | member | member@t1.test | least privilege |
| owner-t2 | tenant-2 | owner | owner@t2.test | cross-tenant counterpart |
| anon | — | — | — | unauthenticated |

Two tenants minimum keeps the catalog compatible with the A/B fixture recipe
`multi-tenant-security-tester` requires — its negative-test assertions stay
in that skill; this catalog just guarantees the world supports them.

For synthetic defaults, use reserved domains/names (`*.test`, `*.example`),
never real-looking customer identities. Any separately approved
de-identification path follows the owning skill's controls.

## Factory patterns

- **Single shape truth:** one factory definition per entity used by all
  layers; unit layer calls `build()` (in-memory), integration/E2E call
  `create()` (persisted through real paths).
- **Override-only variation:** `createInvoice({ status: 'overdue' })` —
  defaults are the simplest valid state; every override is visible at the
  call site.
- **Association discipline:** factories create their own parents by default
  but ACCEPT injected ones — tests composing scenarios stay explicit.
- **No raw-insert bypasses:** persistence goes through the app's write path
  or real migrations so constraints/defaults/hooks apply. Impossible states
  may be built ONLY for unit-level edge tests, in memory, labeled as such.

## Namespacing schemes (parallel isolation)

- Combine run ID, worker ID and test ID in the marker for every mutable
  tenant slug, email or resource name on shared environments, for example
  `r123-w2-invoice-overdue-`. A worker index or run ID alone can collide
  across tests or runs. Encode and bound each marker component before use.
- Baseline rows are READ-ONLY by convention AND (where possible) by
  role — the test user lacks permission to mutate catalog rows.

## Synthetic generation rules

- Names/emails/companies from fixed word lists with seeded selection —
  deterministic run-to-run.
- Realistic distributions only where behavior depends on them (long names
  for truncation tests are explicit fixtures, not lottery wins).
- Numbers/money: cover the boundary catalog (0, negative, max, precision)
  as named fixtures, not random draws.

## TTL & traceability

Every created record carries a marker (naming prefix or metadata column
where the schema allows): run ID + worker ID + test ID, plus its creation
time. An orphan sweep deletes only records proven to have been created by
that suite, after its time-to-live (TTL), within the authorized tenant and
environment. Do not delete by name wildcard alone on shared environments.
Local ephemeral DBs skip TTL — recreate instead.
