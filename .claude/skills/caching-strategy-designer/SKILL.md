---
name: caching-strategy-designer
description: Decide what gets cached, where, and how it stays correct — candidate analysis first (read/write ratio, miss cost, staleness tolerance stated per item), layer choice (HTTP/CDN edge, in-process, distributed cache, DB materialization), invalidation designed BEFORE the cache ships (TTL, event-driven purge with backstop, write-through/behind — with the consistency envelope each buys), key design where tenant scoping is a correctness boundary (tenant-qualified keys; a NEW cache store's isolation defers to multi-tenant-data-architect), stampede protection, failure semantics (cold start, cache-down, stale-on-error), and measurement (hit ratio via observability-operator; gates via performance-test-harness). Authorization results are never cached by default. Use when adding or redesigning a cache, choosing TTLs/invalidation, or when stale-data bugs implicate a cache. Do NOT use to hide chatty patterns (n-plus-one-detector fixes those first) or for browser asset caching (frontend-perf-engineer).
---

# Caching Strategy Designer

## Purpose

There are only two hard things in computer science, and this skill owns
one of them: every cache is a standing bet that staleness within a stated
window is acceptable, and most caching bugs are that window never having
been stated. This skill designs caching as a correctness feature with a
performance benefit — candidates justified by evidence, the staleness
envelope written down per item, invalidation designed before the cache
ships (not after the first stale-data incident), keys that carry the
tenant boundary, stampede protection for the expiry cliff, and failure
semantics for the day the cache is down. A cache without an invalidation
story is a bug that hasn't fired yet; this skill exists to make sure it
never ships in that state.

## Use When

- Use when: adding a cache to a hot read path — API responses, computed
  aggregates, configuration/reference data, session-adjacent lookups.
- Use when: choosing or revisiting TTLs, invalidation triggers, or the
  cache layer (edge/HTTP vs application vs distributed vs database
  materialization) for a workload.
- Use when: stale-data bugs implicate an existing cache and its
  invalidation/consistency design needs an overhaul.
- Use when: a latency budget (`latency-budget-architect`) or split
  verdict (`operational-vs-analytical-splitter`) prescribes "cache" and
  the actual design now needs doing.
- Do NOT use when: the read path is chatty (N+1, per-row lookups) —
  `n-plus-one-detector` fixes the pattern FIRST; caching a storm hides
  it and every miss replays it.
- Do NOT use when: deciding the tenant-isolation posture of a NEW cache
  STORE (shared cluster vs per-tenant separation) —
  `multi-tenant-data-architect` owns where a new store gets its tenant
  scoping; this skill designs keys/invalidation WITHIN that decision.
- Do NOT use when: the caching is browser asset/bundle-level (cache
  headers for static assets, immutable bundle URLs, service-worker
  strategies) — `frontend-perf-engineer` owns the frontend asset path;
  this skill covers shared HTTP/CDN caching of API/page responses.
- Do NOT use when: the "cache" is really a materialized analytical
  workload moving off the primary — that placement decision is
  `operational-vs-analytical-splitter`.
- Do NOT use when: designing rate-limit counters, queues, or locks that
  happen to live in a cache technology — those are not caches (no
  source of truth to fall back to) and their design belongs to the
  owning feature's architecture.

## Inputs to Inspect

1. The candidate's evidence: read/write ratio, request rate, computation
   or query cost per miss (what a cache actually saves), result size
   and cardinality (what it costs to hold).
2. The staleness question, asked per candidate and answered by an
   owner: how old may this data be when served, in seconds/minutes,
   and what breaks (billing? authorization? a dashboard number?) when
   the window is exceeded.
3. Write topology: every path that mutates the underlying data —
   including background jobs, admin edits, and OTHER services —
   because each one is an invalidation trigger or a staleness hole.
4. The tenant model: cached data's tenant ownership, the established
   isolation posture for stores (from `multi-tenant-data-architect`
   output where it exists), and any cross-tenant shared/reference data
   that is legitimately tenant-neutral.
5. Existing cache infrastructure and its behavior: layers already in
   play (edge, app, distributed), their eviction policies, memory
   limits, and current hit ratios if measured.
6. Failure tolerance: what the system must do when the cache is cold,
   down, or partially evicted — and the origin's capacity to absorb a
   full miss storm (this bounds TTL/warming choices).

## Workflow

1. **Qualify the candidate — or reject it.** A cache earns its place
   with: high read/write ratio, meaningful miss cost, bounded result
   cardinality, and a stated staleness tolerance. Reject candidates
   that fail the interrogation: write-heavy data (invalidations exceed
   hits), unbounded key spaces (cache becomes a leak), zero staleness
   tolerance (see the authorization rule in Safety Rules), or a chatty
   pattern in disguise (→ `n-plus-one-detector` first).
2. **State the consistency envelope per item.** In writing, in the
   design: "served up to N seconds stale under normal operation, up to
   M during invalidation failure; never stale for <listed operations>".
   This sentence is the cache's contract; everything below implements
   it.
3. **Choose the layer.** Edge/HTTP-CDN for anonymous or coarsely-varied
   responses (careful: `Vary` and auth — a shared cache serving a
   personalized response is an incident); application-level in-process
   for tiny hot reference data (accepting per-instance divergence);
   distributed cache for shared, keyed, cross-instance data — the
   default for tenant-scoped items; database materialization when the
   data is queried in shapes a cache can't serve. State why the layer
   matches the envelope.
4. **Design the keys.** Explicit key schema: `<namespace>:<version>:
   <tenant-id>:<entity>:<discriminators>`. Tenant-qualified ALWAYS for
   tenant-owned data — key collisions across tenants are data leaks,
   not bugs. Version segment enables generation-based purge (bump the
   version = atomic invalidation of a family). Discriminators cover
   everything that varies the value (locale, role-visibility, plan) —
   under-keyed caches serve one user's view to another.
5. **Design invalidation BEFORE shipping.** Per item, choose and state:
   - *TTL-only:* honest for tolerance-bounded data; TTL = the envelope,
     not a guess.
   - *Event-driven purge:* mutation paths (ALL of them, from input 3)
     emit invalidation — precise but every missed path is a permanent
     staleness hole; pair with a backstop TTL always.
   - *Write-through / write-behind:* cache updated at write time —
     consistency at the cost of write-path coupling (write-behind adds
     loss risk; name it).
   - *Generation/version bump:* for families invalidated together.
   The backstop rule: every entry has a TTL even when event-driven —
   events fail, and the TTL caps the damage.
6. **Protect against stampedes.** For hot keys: single-flight/lock so
   one request recomputes while others wait or serve stale;
   probabilistic early refresh or TTL jitter so a family doesn't expire
   as one cliff; explicit cold-start/warming plan when a deploy or
   flush empties everything at once (the origin must survive the first
   minute — input 6 bounds this).
7. **Define failure semantics.** Cache down: fail-open to origin (with
   load shedding if the origin can't take it) or serve-stale-on-error
   (state the max-stale bound) — chosen per item's envelope; never
   fail-closed for availability-critical reads unless correctness
   demands it. Eviction pressure: what may be evicted early and what
   should be pinned/sized-for.
8. **Plan the measurement.** Hit ratio target per cache (and what a
   LOW ratio triggers — removal is a valid outcome; an unhit cache is
   pure risk), staleness-incident tracking, memory/eviction telemetry
   — wiring via `observability-operator`; latency effect verified
   through `performance-test-harness` gates where they exist.
9. **Deliver the design** in the Output Format, one card per cached
   item — the envelope, layer, keys, invalidation, stampede, failure,
   and measurement rows all filled; a cache card with an empty
   invalidation row does not ship.

Layer decision table, invalidation-pattern tradeoffs, key-schema
conventions, and stampede-protection patterns:
[references/invalidation-decision-sheet.md](references/invalidation-decision-sheet.md).

## Output Format

```
CACHING STRATEGY — <scope>
Rejected candidates: <item — why (write-heavy | unbounded keys | zero tolerance | chatty pattern → n-plus-one-detector)>
Per-item cache card:
  <item>: evidence=<read/write, miss cost, cardinality>
  ENVELOPE: "≤ <N>s stale normal / ≤ <M>s on invalidation failure; never stale for: <ops>"
  layer=<edge|app|distributed|materialized> (why it fits the envelope)
  keys=<namespace>:<ver>:<tenant-id>:<entity>:<discriminators> (under-keying check done)
  invalidation=<TTL|event+backstop-TTL|write-through|generation> — mutation paths covered: <list>
  stampede=<single-flight | jitter | early-refresh | warming plan>
  failure=<fail-open|serve-stale(max)|fail-closed(why)> ; eviction posture=<...>
  measurement=<hit-ratio target; removal trigger; staleness tracking> → observability-operator
Store-level isolation: <existing posture applied | NEW store → multi-tenant-data-architect>
Verification: <before/after latency via performance-test-harness where wired>
```

## Safety Rules

- **Authorization results are not cacheable by default.** Permission
  checks, entitlement lookups, and tenant-membership answers have
  effectively zero staleness tolerance in the deny direction (revoked
  access must revoke). Caching them requires an explicit human-approved
  envelope with a revocation-propagation bound — surface it, never
  default it.
- **Tenant-qualified keys are a correctness boundary**: any cached
  tenant-owned value whose key lacks the tenant id is a cross-tenant
  leak waiting for a collision. This rule has no exceptions for
  "internal" caches.
- **Personalized responses never enter shared HTTP caches** — auth'd
  responses carry cache-control that forbids shared storage unless the
  variance is fully keyed and reviewed.

## Validation Checklist

- [ ] Every cached item has a written consistency envelope with an
      owner-confirmed staleness number — no "we'll tune TTL later".
- [ ] Every card's invalidation row is filled; event-driven designs
      enumerate ALL mutation paths and carry a backstop TTL.
- [ ] Keys are tenant-qualified for tenant-owned data; discriminators
      cover everything that varies the value; a version segment exists.
- [ ] Rejected candidates are listed with reasons — the design shows
      what it declined to cache.
- [ ] Stampede protection exists for hot keys and the cold-start plan
      survives a full flush at peak.
- [ ] Failure semantics are stated per item (fail-open/serve-stale
      bounds), and the origin survives the miss storm.
- [ ] Hit-ratio targets and the removal trigger are defined; the
      measurement wiring is handed to observability-operator.
- [ ] No authorization/entitlement result is cached without the
      explicit approved envelope.

## Gotchas

- The second-hardest bug: an event-driven invalidation missing ONE
  mutation path (the admin bulk edit, the background reconciler) —
  staleness that only manifests for that path's changes. The
  mutation-path enumeration and backstop TTL exist for exactly this.
- Under-keying serves the wrong data, over-keying serves nothing:
  missing a discriminator (role, locale, plan) leaks one view to
  another audience; keying on request noise (timestamps, cursors)
  drives the hit ratio to zero. Both are key-schema review items.
- The expiry cliff: a popular family cached at deploy time with one
  TTL expires as one thundering herd. Jitter and early-refresh are
  cheap; the origin outage they prevent is not.
- Serve-stale-on-error without a bound quietly becomes
  serve-forever-on-error when the origin stays down — max-stale is
  part of the policy, and its exceedance is an alert, not a shrug.
- Write-behind loses writes on cache failure by design — it buys write
  latency at durability's expense; naming that tradeoff is mandatory,
  choosing it for money-adjacent data is a Stop Condition.
- In-process caches diverge per instance: N app instances = N
  independent staleness windows; fine for reference data, wrong for
  anything users compare across requests that land on different
  instances (sticky-session illusions).
- Negative caching cuts both ways: caching "not found" absorbs
  lookup storms for missing keys — and serves 404 for N seconds after
  the thing is created. State the negative TTL separately and shorter.
- Cache-aside recomputation races: two writers interleaving
  read-modify-write on the same key can resurrect stale data;
  single-flight plus compare-and-set (or versioned writes) where the
  value is mutable.

## Stop Conditions

- Asked to cache authorization/permission/entitlement results as an
  optimization → stop; apply the Safety Rule — explicit human approval
  with a revocation-propagation bound, or the answer is no.
- Asked to cache to hide a chatty pattern ("cache the page, it does
  400 queries") → refuse; route to `n-plus-one-detector` first, then
  revisit surviving candidates.
- No staleness tolerance can be stated for a candidate (the owner
  says "it must always be current") → the item is not cacheable as
  scoped; present read-path alternatives (query tuning →
  `query-plan-reader`; materialization → the splitter) instead of
  inventing a tolerance.
- The design would introduce a NEW cache store whose tenant-isolation
  posture is undecided → pause the store decision and route it to
  `multi-tenant-data-architect`; key design resumes after.
- Write-behind proposed on billing/financial or otherwise
  loss-intolerant data → halt for explicit human sign-off; write loss
  on cache failure is that choice's designed behavior.
- Asked to also flush/purge/edit a LIVE production cache → decline
  execution; operational cache actions follow the ops approval path.

## Supporting Files

- [references/invalidation-decision-sheet.md](references/invalidation-decision-sheet.md)
  — layer decision table, invalidation-pattern tradeoff rows,
  key-schema conventions with the under/over-keying checks, stampede
  patterns (single-flight, jitter, early refresh), negative-caching
  guidance.
- `evals/evals.json` — behavior cases including the
  missed-mutation-path edge and the cache-authorization refusal.
- `evals/trigger-evals.json` — discrimination against
  `n-plus-one-detector`, `multi-tenant-data-architect`,
  `frontend-perf-engineer`, and `operational-vs-analytical-splitter`.
