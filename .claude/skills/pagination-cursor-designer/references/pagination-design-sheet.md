# Pagination Design Sheet

Detail tables for `pagination-cursor-designer`. Read on demand.

## Cursor (keyset) vs offset — decision table

| Dimension | Offset / limit | Cursor / keyset |
|---|---|---|
| Behavior under concurrent insert/delete | Drifts — rows duplicate/skip | Stable — resumes from a row key |
| Deep-page cost | O(offset) — scans skipped rows | O(page size) — seeks to key |
| Random access to page N | Native | Not native (needs page→cursor map) |
| Total "page X of Y" | Natural (but COUNT cost) | Awkward — usually omit total |
| Good for | Small, low-churn, human-browsed, admin tables | Large, high-churn, deep, feeds, exports, infinite scroll |

Default to keyset unless random page access is a hard requirement AND the
collection is small and low-churn.

## Total ordering & tiebreaker

Keyset paging requires a STRICT TOTAL order — every row comparable, no
ties. Compose the user-visible sort with a unique tiebreaker:

```
ORDER BY created_at DESC, id DESC     -- id breaks ties on equal timestamps
```

Without the `id` tiebreaker, all rows sharing one `created_at` (a bulk
import, a burst) straddle the page boundary and repeat or vanish. The
`WHERE` for "next page after (t, i)" mirrors the order:

```
WHERE (created_at, id) < (:last_created_at, :last_id)   -- row-value comparison
ORDER BY created_at DESC, id DESC
LIMIT :page_size
```

Descending needs `<`; ascending needs `>`. Composite/row-value comparison
keeps it index-friendly; the tenant/auth predicate is ANDed in
server-side, never taken from the cursor.

## Versioned cursor struct (opaque)

```
cursor = base64url(json({
  "v": 1,                 // bump when the shape changes
  "k": [<last_created_at>, <last_id>],  // ordering tuple only
  "d": "next"             // direction
}))
```

- Opaque so the shape can evolve; clients treat it as a token.
- Contains ordering keys + direction ONLY. No tenant id, no auth scope,
  no raw SQL offset, no total/position.
- On decode, validate `v`; reject unknown versions. Re-apply auth scope
  from the authenticated context, not from the cursor.

## Total-count strategies

| Need | Strategy | Cost |
|---|---|---|
| None | Omit total; show "load more" until next cursor is null | free |
| Rough | Cached/periodic estimate, or planner row estimate | low, approximate |
| Exact, small set | `COUNT(*)` once, not per page | moderate |
| Exact, huge/high-churn | Separate endpoint, or maintained counter table | high — escalate |

Never run an exact `COUNT(*)` on a large, high-churn table on every page
by default — it is a frequent latency dominator. Decide deliberately.

## Edge behaviors to specify

- **Sort/filter changed mid-traversal:** old cursor invalid → reset to
  first page; state this to the client.
- **Cursor points at a deleted row:** row-value comparison naturally
  resumes from the next row in order — verify, don't assume.
- **Empty result / first page:** next cursor absent; UI shows the empty
  state (hand rendering to `edge-state-ux-designer`).
- **Infinite scroll deep-link/back:** reflect cursor/position in URL
  state or users lose their place.
