---
name: pagination-cursor-designer
description: Design pagination for list endpoints and their UIs — cursor (keyset) vs offset chosen with drift and deep-page costs stated, the opaque cursor's contents defined (sort key + deterministic tiebreaker + direction) with a stability contract, a total ordering mandated so rows never repeat or vanish under concurrent writes, default and max page sizes set, end-of-results signaled honestly (null next cursor, no guessed total), the tenant/permission predicate kept INSIDE the cursor so paging cannot cross a boundary, and a surface pattern (load-more, numbered, infinite scroll) chosen with tradeoffs. Owns the pagination MECHANISM inside a contract whose routes, versioning, and rate limits are api-event-architect's. Use when designing or fixing pagination, cursors, or "load more", or when a list skips or repeats rows as data changes. Do NOT use to design the API contract itself (api-event-architect) or tune one slow query's plan (query-plan-reader).
---

# Pagination Cursor Designer

## Purpose

Pagination breaks in ways a single request never shows: a row is
inserted while a user reads page two, and page three now repeats a row
or skips one; someone deep-links to `?page=900` and the database scans
nine hundred pages to serve one; a client stores `nextCursor` and it
silently starts returning another tenant's rows because the tenant
filter lived outside the cursor. This skill produces the pagination
design for a list surface — the cursor's contents and stability
contract, the total ordering that makes "next" deterministic, page-size
bounds, honest end-of-results signaling, and the tenant/permission
predicate carried INSIDE the traversal — plus the surface pattern
(load-more, numbered pages, infinite scroll) with its tradeoffs. It owns
the pagination MECHANISM; the route shape, versioning, and rate limits
of the endpoint it rides on belong to `api-event-architect`.

## Use When

- Use when: designing pagination for a new list/collection endpoint or
  its UI, or choosing between cursor and offset paging.
- Use when: a list skips, repeats, or reorders rows as underlying data
  changes (the classic offset-drift bug), or deep pagination is slow.
- Use when: adding "load more", infinite scroll, or numbered pages and
  the traversal semantics (stability, end signaling) need pinning.
- Use when: an existing cursor leaks internal ids/offsets, breaks when
  the sort changes, or lets a client page across a tenant boundary.
- Do NOT use when: the task is the API contract itself — resource
  routes, versioning/deprecation, envelopes, rate limits — that is
  `api-event-architect`; this skill designs the pagination inside it.
- Do NOT use when: one specific query is slow and needs plan analysis
  (index/sargability) — that is `query-plan-reader`; this skill decides
  the pagination model, then hands the keyset query to it if needed.
- Do NOT use when: the question is whether to cache list responses —
  that is `caching-strategy-designer` (a paginated list's cache key
  must include the cursor, which this skill defines).

## Inputs to Inspect

1. The list's access pattern: expected result-set sizes, how deep users
   actually page (most stop at page 1–2; some export everything), and
   whether the client needs random access to page N or only sequential.
2. Write concurrency on the collection: insert/delete rate relative to
   read, which determines how badly offset paging drifts.
3. The sort/filter surface: every sortable column and filter the client
   can set — the cursor must encode enough to resume any of them, and
   changing the sort invalidates an existing cursor.
4. The tenant/authorization model (from `multi-tenant-data-architect` /
   `authorization-matrix-designer` outputs if present): the predicate
   that scopes rows to the caller, which MUST be part of the query, not
   reconstructed from a client-supplied cursor.
5. Any existing pagination in the codebase and its bugs: offset drift
   reports, `page`/`limit` params, cursor formats already exposed to
   clients (a live contract that constrains changes).

## Workflow

1. **Choose the model against the access pattern.** Offset/limit is
   acceptable ONLY for small, low-churn, human-browsed lists where
   random page access matters and drift is tolerable — state that
   ceiling. Default to cursor (keyset) paging for anything large,
   high-churn, or deep: it is drift-free and O(page size), not O(offset).
   Record why, per surface.
2. **Define the total ordering.** Keyset paging requires a strict, total
   order — pick the sort column(s) PLUS a deterministic tiebreaker
   (commonly the primary key) so no two rows compare equal. Without the
   tiebreaker, rows sharing a sort value straddle a page edge and
   repeat/vanish. State the exact ORDER BY.
3. **Specify the cursor contents and encoding.** The cursor carries the
   last row's ordering tuple (sort value(s) + tiebreaker) and the
   direction — nothing the client should not depend on. Make it opaque
   (base64 of a versioned struct) so its shape can evolve; NEVER expose a
   raw offset or internal row id the client can forge or that leaks
   count/position. Version the cursor payload.
4. **Bind tenant/permission scope into the query, not the cursor.** The
   authorization predicate is applied server-side on every page from
   trusted context (session/token), never trusted from cursor contents.
   A tampered or stale cursor must at worst return the caller's own rows
   or an error — never another scope's. This is a correctness boundary.
5. **Bound page size.** Set a sane default and a hard maximum; reject or
   clamp over-max requests. Unbounded `limit` is a denial-of-wallet and
   memory risk — cross-reference `ai-cost-guardrail-designer` /
   rate-limit policy only as the enforcement home, not the value.
6. **Signal boundaries honestly.** Return the next cursor (null/absent at
   the end) and, for bidirectional UIs, a previous cursor. Do NOT return
   a total count unless it is cheap and correct — an approximate or
   expensive `COUNT(*)` on every page is a common performance trap; if a
   total is truly needed, price it and consider a separate estimate.
7. **Handle sort/filter changes and edge cases.** Define behavior when
   the client changes sort or filter mid-traversal (the old cursor is
   invalid — reset to first page, state this), when a cursor points at a
   now-deleted row (resume from the next row in order), and empty/first/
   last pages.
8. **Pick the surface pattern.** Map the model to UX: "load more"/
   infinite scroll pairs naturally with cursors; numbered pages imply
   offsets or a page→cursor map and random access (call out the cost);
   pick per surface and state the tradeoff. Note deep-link/back-button
   behavior for infinite scroll.
9. **Deliver** the design in the Output Format with the exact ordering,
   cursor schema, size bounds, and the tenant-scope guarantee.

Decision tables (cursor vs offset, tiebreaker selection, total-count
strategies) and a worked keyset query with a versioned cursor struct:
[references/pagination-design-sheet.md](references/pagination-design-sheet.md).

## Output Format

```
PAGINATION DESIGN — <surface/endpoint>
Model:        cursor (keyset) | offset  — rationale + access pattern
Ordering:     ORDER BY <sort cols>, <tiebreaker> <dir>   (strict total order)
Cursor:       opaque base64 of { v, keys[], dir }  — contents listed; what it must NOT expose
Page size:    default=<n> max=<n>  (over-max: clamp|reject)
Scope:        auth/tenant predicate applied server-side every page (NOT from cursor)
End signal:   nextCursor null at end; prevCursor=<...>; total=<none|estimate|exact+cost>
Sort change:  cursor invalidated → reset to first page (stated to client)
Deleted-row:  resume from next row in order
Surface:      load-more | infinite | numbered — tradeoff noted
Boundaries:   contract/routes/rate-limits → api-event-architect; keyset query tuning → query-plan-reader
```

## Validation Checklist

- [ ] The ORDER BY is a strict total order — a deterministic tiebreaker
      is present, so no two rows tie.
- [ ] The cursor is opaque and versioned; it exposes no raw offset,
      internal id, or position/count a client could depend on or forge.
- [ ] The tenant/authorization predicate is applied server-side on every
      page from trusted context — a tampered cursor cannot cross scope.
- [ ] Page size has a default AND an enforced maximum.
- [ ] End-of-results is signaled by an absent/null next cursor; any total
      count is justified as cheap-and-correct or omitted.
- [ ] Behavior is defined for sort/filter change mid-traversal and for a
      cursor pointing at a deleted row.
- [ ] The surface pattern is chosen with its random-access/deep-link
      tradeoff stated.
- [ ] Endpoint contract concerns are handed to `api-event-architect`, not
      redesigned here.

## Gotchas

- Offset paging over changing data is not "mostly fine" — a single
  insert above the current offset shifts every subsequent row by one,
  duplicating one and hiding one on the next page. It is a correctness
  bug, not a nicety.
- A cursor without a tiebreaker breaks precisely on the rows users care
  about — the burst created at the same second, the batch imported with
  one timestamp. Equal sort values MUST be broken by the primary key.
- `COUNT(*)` for "page X of Y" is often the most expensive part of a
  list endpoint and gets re-run on every page. Decide the total-count
  cost deliberately; frequently the honest answer is "no total".
- Trusting scope from the cursor is a tenant-isolation hole: if the
  cursor says `tenant=7` and the server believes it, a forged cursor
  reads tenant 7. Scope always comes from the authenticated context.
- Encoding a raw SQL offset or internal id in a "opaque" cursor makes it
  a contract the moment a client decodes and depends on it — keep the
  payload versioned and genuinely opaque.
- Infinite scroll destroys deep-linking and the back button unless the
  cursor/position is reflected in URL state — design that, or users lose
  their place.
- Changing the default sort silently invalidates every stored cursor
  clients hold; treat cursor format and default ordering as part of the
  endpoint's compatibility surface (coordinate with `api-event-architect`).

## Stop Conditions

- The authorization/tenant predicate that scopes the list is undefined
  or ambiguous → stop and obtain it from `authorization-matrix-designer`
  / `multi-tenant-data-architect` outputs or a human before fixing the
  cursor; guessing here builds a cross-tenant paging hole.
- The request is really to design the endpoint contract (routes,
  versioning, envelope, rate limits) → route to `api-event-architect`;
  this skill designs only the pagination inside that contract.
- A required exact total count on a huge, high-churn collection is
  mandated despite its cost → surface the performance tradeoff and the
  alternatives (estimate, separate count endpoint) to a human rather
  than baking an expensive `COUNT(*)` into every page.
- Changing an already-published cursor format would break live clients →
  flag it as a contract-breaking change for `api-event-architect`'s
  versioning/deprecation process; do not silently alter the format.

## Supporting Files

- [references/pagination-design-sheet.md](references/pagination-design-sheet.md)
  — cursor-vs-offset decision table, tiebreaker selection, total-count
  strategies, and a worked keyset query with a versioned cursor struct.
- `evals/evals.json` — behavior cases including offset-drift diagnosis,
  the tenant-scope-in-cursor refusal, and the total-count trap.
- `evals/trigger-evals.json` — discrimination against `api-event-architect`
  (the contract), `query-plan-reader`, and `caching-strategy-designer`.
