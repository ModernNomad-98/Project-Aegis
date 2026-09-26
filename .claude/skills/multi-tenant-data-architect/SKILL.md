---
name: multi-tenant-data-architect
description: Design the tenant-scoped data layer — choose a scoping strategy per store, define server-validated tenant-context propagation from request to query, map ownership and shared data, plan tenant indexing and migration with verification and rollback, and output an isolation test matrix. A client tenant selector may be used for an authorized multi-tenant principal only after server-side membership validation; data queries use the resulting trusted context. Use when designing multi-tenant storage, retrofitting tenant scoping, planning migration/re-sharding, or scoping a new store. Do NOT use to define tenant semantics (tenant-modeler), audit leaks (tenant-isolation-reviewer), or author/audit RLS policies.
---

# Multi-Tenant Data Architect

## Purpose

Produce a data-layer design where every byte of tenant data has a declared
scope, a declared owner, and a declared path for how tenant context reaches
the query that touches it. Deliverables: a per-store scoping decision with
tradeoffs, a tenant-context propagation contract, a data ownership map,
shared-data rules, a migration plan with verification and rollback, and a
data-layer isolation test matrix. The discipline: scoping is decided per
store, and tenant context is validated and bound server-side. A client
selector is permitted for a principal authorized in multiple tenants only
after membership and operation scope are checked; an unchecked selector is
a cross-tenant leak.

## Use When

- Use when: designing storage for a new multi-tenant product or feature.
- Use when: retrofitting tenant scoping onto existing single-tenant tables
  (the backfill-and-enforce problem).
- Use when: planning a tenant data migration — pooled→silo for a big tenant,
  re-shard, region move — or its rollback.
- Use when: a new store appears (cache, queue, search index, vector store,
  object storage) and needs its tenant-scoping decision.
- Do NOT use when: what a tenant IS remains undefined — `tenant-modeler`
  first; scoping an undefined boundary produces confident nonsense.
- Do NOT use when: auditing an existing system for cross-tenant leakage —
  `tenant-isolation-reviewer`.
- Do NOT use when: writing or auditing RLS policies themselves — that is the
  Phase 4 security pack's scope; this skill decides WHERE enforcement lives,
  not the policy SQL.
- Do NOT use when: the structural question has no tenancy axis — plain
  `architecture-designer`.
- Do NOT use when: the pressure is throughput/size distribution of a store —
  shard-key choice, range/hash partitioning, hot-key resharding are
  `data-partitioning-sharding-strategist` (a scale axis, not isolation); or
  adding a subordinate per-user scope BELOW tenant_id (site/region row-filter
  grants) — that is `intra-tenant-scope-architect`, layered on the tenant
  boundary this skill sets.

## Inputs to Inspect

1. The tenant model (tenant-modeler output): tenant definition, hierarchy,
   the level isolation is enforced at, lifecycle states with data postures.
2. Current stores and schemas: tables, indexes, existing tenant keys or their
   absence, ORMs/query layers in use.
3. Where tenant context currently lives in a request (session, token claim,
   middleware) and how queries are built (query builder, raw SQL, ORM
   default scopes).
4. Data volume facts: row counts by table, largest tenant's share, growth
   rate, retention requirements — skew drives partitioning and silo choices.
5. All secondary stores: caches, queues, search indexes, vector stores,
   object storage, analytics sinks — each needs a scoping decision, not just
   the primary database.
6. Compliance/residency constraints that force physical separation.

## Workflow

1. **Read the tenant model first.** Pin which level of the hierarchy is the
   scoping key. Undefined → stop, route to `tenant-modeler`.
2. **Inventory every store** — primary DB, caches, queues, indexes, vector
   stores, object storage, analytics sinks. The design covers all of them; a
   store without a scoping decision is a finding against the design.
3. **Choose the scoping strategy per store** using
   [references/scoping-strategy-tradeoffs.md](references/scoping-strategy-tradeoffs.md):
   pooled (tenant key + enforced scoping), schema-per-tenant,
   database-per-tenant, or mixed. Justify per store; a mixed answer is
   normal, an unjustified one is not.
4. **Define the tenant-context propagation contract**: derive allowed
   tenants from the authenticated principal; if the client selects one,
   validate membership and operation scope server-side. Bind the validated
   tenant once per request/job and carry that trusted context to every query
   via a named mechanism (middleware, scoped repository, ORM default scope,
   or session variable). Never trust a raw client-supplied tenant id.
5. **Map data ownership**: every table/store → one owning component; classify
   tables as tenant-owned (scoped), shared/reference (read-only to tenants),
   or platform (control-plane; no tenant business data). Flag anything that
   doesn't classify cleanly.
6. **Design indexes and partitioning around the tenant key** — tenant key
   leading in composite indexes on tenant-owned tables; partitioning only
   with a stated size/skew number driving it.
7. **Wire lifecycle hooks**: for each tenant lifecycle state (suspend,
   offboard, purge), state what happens in each store — frozen, exported,
   deleted — and which jobs do it. Purge must enumerate every store,
   including backups' retention window.
8. **Write the migration plan** (new scoping or re-shard): expand → backfill
   → verify (per-tenant row counts and checksums) → enforce → contract, each
   step shippable and reversible; rollback defined per step, and no step's
   rollback may require un-running a backfill (keep old columns/paths until
   the contract step).
9. **Emit the data-layer isolation test matrix**: per store × operation,
   the negative expectation (tenant A's context cannot read/write tenant B's
   rows/objects/entries), handed to `tenant-isolation-reviewer` and QA.
10. **Explain owner-facing choices before asking.** When scale, residency or
    isolation needs an owner decision, define terms such as pooled storage,
    schema per tenant and database per tenant, and explain why the choice
    affects this product. Compare viable options by money (including $0),
    migration/setup time, ongoing operations/maintenance cost, isolation
    benefits and drawbacks. Recommend one from measured volume, compliance
    needs and team capacity, with a reason. Resolve routine per-store design
    choices from evidence without asking the owner. Treat a choice already
    stated by the owner as settled; explain its implications without re-asking.
    State why each viable option could fit this case, mark unknown costs as
    unknown rather than guessing, then ask exactly one owner question; the
    answer does not authorize migration execution.

## Output Format

```
MULTI-TENANT DATA DESIGN — <scope>
Tenant scoping key: <which hierarchy level, from the tenant model>
Store inventory & scoping decisions:
  <store — pooled(mechanism)/schema/db/mixed — justification>
Tenant-context propagation contract: <derivation point → binding → query
  mechanism; client selector validation; raw client ids never trusted>
Data ownership map: <table/store → owner → tenant-owned/shared/platform>
Indexing & partitioning: <tenant-key-leading indexes; partitioning + the
  number driving it>
Lifecycle hooks: <state → per-store action → executing job>
Migration plan: <expand → backfill → verify → enforce → contract; rollback
  per step; verification = per-tenant counts/checksums>
Isolation test matrix (data layer): <store × operation × expected denial>
Assumptions & open questions: <each with risk-if-wrong / who answers>
Owner choice brief (only if needed): <terms; why now; options with money,
  setup/migration/maintenance costs, pros and cons; recommendation and fit>
```

## Validation Checklist

- [ ] Every store in the inventory has a scoping decision — including caches,
      indexes, vector stores, and object storage.
- [ ] The propagation contract derives tenant context server-side and names
      the concrete mechanism; no data path trusts a client-supplied tenant id.
- [ ] Every table/store classified tenant-owned / shared / platform; every
      one has exactly one owner.
- [ ] Purge enumerates every store where the tenant's data exists, backups
      included.
- [ ] Migration steps are individually shippable with per-step rollback and
      count/checksum verification; enforcement flips only after verification.
- [ ] The isolation test matrix covers every store, not just the primary DB.
- [ ] No RLS policy SQL authored; enforcement location decided, policy
      authoring deferred to the Phase 4 pack.
- [ ] Any owner-facing choice explains terms, each option's reason, costs or
      unknowns, pros and cons, and a reasoned recommendation before one
      owner question.

## Tenant Isolation Rules

- Every tenant-owned table/entry/object carries the tenant scope key; scoping
  by joins-through-ownership alone is declared and justified where used.
- Tenant context is derived from the authenticated principal and, when
  applicable, a server-validated tenant selector. Request bodies, query
  parameters and files never become trusted context without that check.
- Cross-tenant queries exist only in named, audited platform paths (support,
  billing aggregation, platform analytics), each listed in the design.
- Defense in depth is stated: application scoping plus database-level
  enforcement where available — the design names where each layer applies
  even though policy authoring is out of scope here.

## Gotchas

- The primary database gets all the attention while the cache serves tenant
  A's data to tenant B via an unscoped key — every store, every time.
- Backfilled tenant keys are wrong exactly where ownership was ambiguous;
  verify with per-tenant counts AND spot checksums before enforcing, not
  after.
- Tenant-key-last composite indexes make every scoped query a scan; the
  tenant key leads unless a measured query pattern says otherwise.
- Schema-per-tenant multiplies migrations by tenant count and drifts; it
  buys isolation optics, not automatic safety — the connection routing
  becomes the control.
- "Shared reference data" grows tenant-specific overrides within a quarter;
  design the override table now or inherit a fork later.
- Purge that forgets the search index, the vector store, or the analytics
  sink is a compliance incident with a delay timer.

## Stop Conditions

- Tenant model undefined or contested → stop; `tenant-modeler` (or
  `source-of-truth-reconciler`) first.
- Data volume/skew facts unknown AND they would flip pooled-vs-partitioned →
  ask for the numbers; do not design for imagined scale.
- The migration touches production data destructively (drops, rewrites) →
  draft the steps and safety gates under the task's design authority;
  `human-approval-boundary` applies before production execution unless an
  existing scoped grant already covers it.
- Residency/compliance requirements surface mid-design that force physical
  separation → re-run the scoping decision; do not bolt a region onto a
  pooled design.
- Asked to implement the migration in the same pass → separate, scoped task
  via `change-classification-gate`; this skill designs.

## Supporting Files

- [references/scoping-strategy-tradeoffs.md](references/scoping-strategy-tradeoffs.md) —
  pooled/schema/database tradeoff table, propagation mechanisms, and the
  expand→contract migration pattern with verification gates.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `tenant-modeler` and
  `tenant-isolation-reviewer` (tenant cluster).
