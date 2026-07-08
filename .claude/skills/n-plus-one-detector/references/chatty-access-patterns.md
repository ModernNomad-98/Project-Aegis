# Chatty Access Patterns — Catalog & Guards

Pattern classes, fix templates, instrumentation options, and assertion
patterns. ORM-agnostic: idioms are named by shape; map to your data
layer's spelling.

## Pattern classes and signatures

| Class | Evidence signature | Typical injection site |
|---|---|---|
| Classic N+1 | 1 parent query + N children differing only in key | lazy relation in loop/serializer/template |
| Resolver N+1 | N identical-shape queries per FIELD across one response | per-field resolver fetching independently |
| Repeated identical | same statement, same params, ≥2× per request | helper called per component without request memoization |
| Serial await | wall-clock ≈ N × round-trip; queries serialized in time | awaited call inside a loop |
| Over-fetch | SELECT of wide rows feeding ≤3 fields | default select-all + narrow projection downstream |
| Per-row aggregate | N COUNT/SUM statements keyed per row | count badge per list item |

## Fix templates (by class)

- **Classic N+1** → eager/preload on the parent query, scoped to the
  paths that render the relation. Anti-template: enabling global eager
  loading (fixes one page, bloats twelve).
- **Resolver N+1** → batched loader per entity type: collect keys
  during the resolution tick, issue ONE `WHERE key IN (...)` query,
  memoize per request. Loader cache lifecycle = the request, never the
  process (tenant-leak hazard otherwise).
- **Repeated identical** → per-request memoization at the accessor
  (request-scoped cache or loader reuse). Not a TTL cache — the scope
  is one request, correctness-bounded.
- **Serial await** → batch keys into one call where the interface
  exists; else bounded-concurrency fan-out (state the bound) as the
  lesser fix + route the batch-interface need to the contract owner.
- **Per-row aggregate** → one grouped query
  (`SELECT key, count(*) ... GROUP BY key`) joined back in memory.
- **Over-fetch** → project the used fields; pairs with covering-index
  effects (see query-plan-reader's worksheet when the projection
  enables one).
- **One-to-many composition** → prefer two batched queries (parents;
  children by parent-key IN) over a row-exploding join when children
  per parent is large; join is fine when it's ≤ a few.

## IN-list chunking

Large key sets need chunking (per-statement parameter limits and plan
quality): chunk at a stated size, issue chunks concurrently with a
bound, and sanity-check the chunked query's plan at worst-case volume —
the batched query becoming the new hotspot is the classic
overcorrection (route to query-plan-reader if heavy).

## Counter instrumentation options

| Option | Where it counts | Notes |
|---|---|---|
| ORM instrumentation hook / event | per statement, in-process | the standard test-time counter |
| Driver/pool-level counter | everything incl. raw SQL | catches escapes from the ORM |
| APM span count per request | production evidence | the discovery tool; too coarse for assertions |
| Query log diff (dev) | ad-hoc reproduction | fine for the evidence table, not for guards |

## Query-budget assertion patterns

```
# exact — stable seeding, deterministic rendering
assert_query_count(operation, expected=3)

# bounded — fixture-count varies; catch storms, not seed drift
assert_query_budget(operation, max=6)

# shape-aware — budget per statement shape (strongest signal)
assert_no_statement_repeated_more_than(operation, times=1, ignore=[<setup shapes>])
```

Guard placement: the integration layer that owns cross-component
behavior (per the repo's test-layer split). Budgets live on endpoints
with history or high traffic — a budget on everything is alarm fatigue
in test form. On failure the assertion should print the statement
shapes and counts (the evidence table), not just "budget exceeded".

## Review-time static cues (cheap catches before evidence)

- Relation/association access inside `for`/`map`/render loops.
- `await` inside loops over collections.
- Serializer/template touching relations the parent query didn't
  preload.
- Any per-row helper that "just fetches one thing".

Static cues justify capturing the evidence table; they do not replace
it — framework internals (identity maps, implicit batching) make
code-reading alone unreliable in both directions.
