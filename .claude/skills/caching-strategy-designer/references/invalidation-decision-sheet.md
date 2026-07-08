# Invalidation Decision Sheet

Layer, invalidation, key, and stampede tables backing the workflow.
Technology-agnostic — "distributed cache" is whatever fills that role in
your stack.

## Layer decision table

| Layer | Right for | Envelope it can honor | Hazards |
|---|---|---|---|
| Edge / shared HTTP-CDN | anonymous or coarsely-varied GET responses | TTL-bound; purge APIs where offered | `Vary` mistakes; personalized data in shared cache = incident; auth'd responses forbidden by default |
| In-process (per instance) | tiny, hot, slow-changing reference data | per-instance TTL; divergence across instances | users comparing across instances see different worlds; memory per instance |
| Distributed cache | shared keyed data, tenant-scoped items, session-adjacent | TTL + explicit purge + generations | network hop per hit; cluster failure semantics; the default for tenant data |
| DB materialization | data queried in shapes (filters/joins) a KV cache can't serve | refresh-interval | this is the splitter's territory when it's a workload move — check |

## Invalidation patterns — tradeoffs

| Pattern | Consistency bought | Price | Use with |
|---|---|---|---|
| TTL-only | staleness ≤ TTL, guaranteed | nothing fresher than TTL | tolerance-bounded data; TTL == envelope number, never a guess |
| Event-driven purge + backstop TTL | fresh-on-change when events flow | EVERY mutation path must emit; missed path = staleness hole until backstop | enumerated write topology; the backstop is mandatory |
| Write-through | read-your-write coherence | write-path latency + coupling | mutable values read immediately after write |
| Write-behind | write latency | WRITE LOSS on cache failure (by design) | never money-adjacent without human sign-off (Stop Condition) |
| Generation/version bump | family-wide atomic purge | full family recompute (stampede risk — pair with warming) | config/plan changes invalidating many keys |

## Key schema conventions

```
<namespace>:<schema-version>:<tenant-id>:<entity>:<discriminators...>
```

- `namespace`: the owning feature — enables targeted flush.
- `schema-version`: bump = generation purge of the family.
- `tenant-id`: MANDATORY for tenant-owned values (correctness boundary).
  Tenant-neutral reference data uses an explicit `shared` segment — the
  word appears, so review can see the claim.
- `discriminators`: everything that varies the value — role-visibility,
  locale, plan tier, feature flags that change the response.

**Under-keying check:** for each cached value, list what varies it; every
variance is in the key or the value is provably invariant to it.
**Over-keying check:** no request-unique noise (timestamps, cursors,
request ids) in keys — hit ratio target implies keys repeat.

## Stampede protection patterns

| Pattern | Mechanics | When |
|---|---|---|
| Single-flight / per-key lock | one recompute; others wait briefly or serve just-expired value | expensive misses, hot keys |
| TTL jitter | TTL ± random % per entry | families cached together (deploy-time fills) |
| Probabilistic early refresh | refresh before expiry with probability rising near TTL | steady-traffic hot keys — no cliff at all |
| Warming plan | ordered pre-fill of the hot set after flush/deploy | cold-start where the origin can't take the herd |

Cold-start sizing: estimate the miss storm (peak RPS × miss cost) and
state whether the origin absorbs it; if not, warming or staged rollout
is part of the design, not an ops improvisation.

## Negative caching

Cache "not found" only with: a SEPARATE, shorter TTL; a purge hook on
the create path (the 404-after-create window is user-visible); and never
for authorization denials (the deny must re-evaluate — see Safety Rules).

## Serve-stale-on-error policy shape

```
on origin error: serve stale up to MAX-STALE=<bound>
  exceeding bound ⇒ fail per item policy + ALERT (owner, not just log)
on cache down:   fail-open to origin with <shed policy if origin capacity < peak>
```

## Measurement rows (wired via observability-operator)

- hit ratio per cache (target + LOW trigger → removal review; an unhit
  cache is pure risk)
- staleness incidents (served-stale age histogram where measurable)
- eviction rate / memory pressure (early eviction breaks envelope math)
- invalidation-event lag (event emit → purge applied)
Latency before/after claims verify through performance-test-harness
gates where wired — the cache justifies itself with numbers or leaves.
