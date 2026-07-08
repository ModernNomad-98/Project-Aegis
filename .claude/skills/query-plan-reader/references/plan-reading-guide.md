# Plan Reading Guide

Operator interpretation, divergence causes, sargability, and index
worksheets. Store-agnostic: operator names vary by engine; the shapes and
diagnostics do not.

## Operator-reading table

| Plan shape | Healthy when | Suspect when |
|---|---|---|
| Full table scan | predicate serves a large fraction; tiny table; analytical shape | selective predicate exists; scan feeds a tiny result |
| Index seek/lookup | selective predicate; low loop count | looped millions of times (read the loops, not the name); followed by huge row-fetch back to the table |
| Nested-loop join | small outer × indexed inner | outer misestimated (est≪actual) — the planner thought "small" |
| Hash join | large unsorted inputs, enough memory | hash spills to disk (memory indicator); build side misestimated |
| Merge join | both inputs already ordered | explicit sorts feeding it that dominate cost |
| Sort | small input; top-N with limit | spill-to-disk markers; sort of millions to return 20 (missing ordered index) |
| Aggregate | after selective filtering | over the whole table per request — analytical shape on the operational path |

## Estimate-vs-actual divergence — causes in likelihood order

1. **Stale statistics** — refresh is the cheapest fix in the catalog;
   check the store's stats timestamp for the touched tables FIRST.
2. **Correlated predicates** — planner multiplies independent
   selectivities (`country='X' AND region='X-north'`); fixes: extended/
   multi-column statistics where supported, or rewrite.
3. **Skew** — histogram misses a dominant value (one tenant = 40% of
   rows); parameter-sensitive plans; consider tenant-aware indexing.
4. **Parameter sniffing / plan cache** — one cached plan serves all
   values; capture per symptomatic value; store-specific mitigations
   noted as verification items, not folklore.
5. **Expressions the planner can't see through** — functions/casts over
   columns (see sargability).

## Sargability catalog (rewrites that let indexes work)

| Anti-pattern | Rewrite |
|---|---|
| `WHERE fn(col) = v` | index the expression (computed/functional index) or rewrite to `col = inv(v)` |
| implicit cast (param type ≠ column type) | match the types — the invisible sargability killer |
| leading-wildcard match | trigram/text-search structures, or accept the scan honestly |
| `OR` across columns | union of two indexed branches, or composite redesign |
| `NOT IN (subquery)` with nulls | `NOT EXISTS` (semantics AND speed) |
| big `OFFSET` pagination | keyset: `WHERE (sort_key, id) > (last_seen...) ORDER BY ... LIMIT n` — offset degrades linearly by design |
| `SELECT *` feeding row-fetch cost | project needed columns; enables covering |

Every rewrite states: semantics preserved (same rows, same order where
promised) — verified, not assumed.

## Composite-index worksheet

```
Query predicates: equality=<cols> range=<cols> order-by=<cols> selected=<cols>
Proposed: (<equality cols...>, <range col>, [order-by respected]) INCLUDE/covering: <cols>
Tenant overlay: tenant key leads when the store's row-security/tenant predicate
                filters this table (policy-injected filters count as equality)
Price: write amplification = one more index maintained per INSERT/UPDATE on <table>
       (state the table's write rate); storage ≈ <estimate>; planner-choice risk low/med
Duplicates check: existing indexes on <table> — is one a prefix of the proposal?
                  (extend, don't stack near-duplicates)
Expected plan change: <node X: scan → seek; loops N→M; sort eliminated?>
```

## Re-verification protocol

1. Same query, SAME parameters, representative volume.
2. Plan shape changed as predicted (name the node-level change).
3. Timing at the calling surface improved (endpoint/job percentile —
   plan-node time alone can mislead); use `performance-test-harness`
   gates where wired.
4. No collateral regressions: the write path's cost (new index) and
   neighbor queries sharing the table checked.
5. Divergence rechecked: estimates now track actuals at the fixed nodes.

## Write-statement capture idiom (safety)

Analyze-style execution of INSERT/UPDATE/DELETE runs the write. Capture
inside an explicit transaction that rolls back (`BEGIN; EXPLAIN ANALYZE
<stmt>; ROLLBACK;` — your engine's equivalent), on non-production data
paths, or use estimate-only capture and say so in the verdict. Production
capture follows the repo's approval conventions — never a default.
