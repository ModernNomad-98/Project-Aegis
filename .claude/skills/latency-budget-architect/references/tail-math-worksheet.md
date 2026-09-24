# Tail Math Worksheet

Composition math, overhead rows, cascade checks, and the review
template. The arithmetic here is the skill's spine — budgets that skip
it are fiction.

This is detail for the [latency-budget-architect](../SKILL.md). `p95` and
`p99` are 95th- and 99th-percentile latencies; `N` is branch count; TLS is
Transport Layer Security; PR is pull request; `ε` is explicit safety margin.

## Composition rules

| Shape | End-to-end latency | Budgeting consequence |
|---|---|---|
| Serial chain A→B→C | sum of the hops | per-hop budgets add to (target − headroom) |
| Parallel fan-out (join waits for all N) | max of the branches | the SLOWEST branch is the budget; tail exposure below |
| Parallel with partial join (first-K, hedged) | k-th fastest | hedging spends duplicate load — headroom-funded only |
| Async fire-and-forget | not on the user path | excluded from THIS budget; its own consumer budget elsewhere |

## Fan-out tail exposure

Probability at least one of N parallel branches exceeds its own p99
threshold, assuming independent branch tail events:

```
P(tail) = 1 - 0.99^N     N=3: 3.0%   N=10: 9.6%   N=30: 26%
```

Correlated branch tails change this probability. When independence is not
supported, use measured joint tails or state a conservative bound. For ten
independent branches, a p95 join target needs each branch's threshold near
p99.49 or stricter, before other path latency is counted. Worked example:

```
Target: 300ms p95 user-perceived
Shape: gateway → auth → [10 parallel shard reads] → assemble
Naive under independence: shard budget 100ms "p99" ⇒ ~9.6% of requests exceed it
Possible design: budget each shard at p99.5, or hedge at 60ms
       (duplicate cost funded from headroom), or reduce fan-out;
       verify the joint path distribution and overhead against the p95 target
```

## Overhead rows checklist (every budget includes them)

- [ ] Serialization/deserialization per fat payload boundary
- [ ] Connection establishment on the tail (pool miss, TLS) — or the
      promise explicitly excludes cold connections
- [ ] Queue wait AT TARGET LOAD for any async/queued hop
- [ ] Retry allowance: (retry count × hop budget + backoff), funded
      from a named allocation
- [ ] Middleware/filter chains (auth checks, logging interceptors)
- [ ] The frontend share when the target is user-perceived
      (render/hydration — frontend-perf-engineer's vocabulary)

## Timeout-cascade worksheet


```
Per hop: timeout(hop) = budget(hop) + tolerance (state tolerance, e.g. +20%)
Cascade check, leaf → root:
  timeout(upstream) ≥ critical-path downstream time + upstream work + ε
  critical path = sum of serial segments; max of parallel branch durations
  at each join; include allowed retries and backoff at their owning layer
Violations to hunt:
  - 30s defaults inside sub-second paths (bug by inheritance)
  - upstream < downstream×retries (abandons work that completes — waste + failure)
  - infinite/no timeout anywhere on a budgeted path (unbounded spend)
```

## Retry-spend accounting

```
retry_cost(hop) = P(retry) × (backoff + budget(hop))
Rules: idempotent hops only; ONE layer owns retries (innermost viable);
       hedging = deliberate duplicate spend, listed as its own row.
Two-layer retry compounding: layers L1×L2 retries ⇒ up to (1+r1)(1+r2)
attempts — the storm multiplier; the design names the single retry layer.
```

## Budget-claim review template (for PRs touching a budgeted path)

```
BUDGET CLAIM — <PR/design ref>
Path: <budgeted path>   Current headroom: <ms, owner>
New spend: <hop/dependency, estimated pXX ms, evidence for the estimate>
Funded by: headroom (path-owner sign-off) | reallocation from <hop> (that owner's sign-off)
           | RENEGOTIATE target (→ slo-reliability-architect loop)
Timeout/retry deltas: <derived numbers updated>
Attribution: <new span + budget annotation added>
```

Unfunded spend is a review block — the rule exists because paths decay
one unbudgeted dependency at a time.

## Attribution convention

Every budgeted hop = one span with a `latency.budget_ms` attribute (or
the tracing stack's equivalent). Violation query: spans where
`duration > budget_ms`, grouped by hop, windowed — the "who blew it"
answer becomes a query, not a meeting. Wiring: observability-operator.
Pre-release: performance-test-harness asserts hop budgets where gates
exist (budgets are its thresholds — one number vocabulary across both).
