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
- [ ] Retry spend funded from a named allocation and priced with the
      canonical R8-CONV-2 model (probability-weighted expected retry_overhead;
      hard-mode retry_allowance_bound where bounds are recorded)
- [ ] Middleware/filter chains (auth checks, logging interceptors)
- [ ] The frontend share when the target is user-perceived
      (render/hydration — frontend-perf-engineer's vocabulary)

## Timeout-cascade worksheet


```
Cascade check, leaf to root:
  timeout(upstream) > own work(upstream) + downstream critical-path budget +
  recorded epsilon
  own work = what the hop itself spends (processing, serialization, queue and
  connection waits it owns); downstream critical-path budget = serial
  downstream hops + the longest parallel branch at each join, priced with the
  canonical R8-CONV-2 expected/hard cascade terms (downstream_expected_critical_path
  with expected_maximum_at_joins in expected mode; hard-mode
  downstream_hard_bound). Epsilon is recorded once.
```

## Retry-spend accounting

Retry spend is owned by the canonical R8-CONV-2 model
([docs/semantics/canonical-semantics.md](../../../../docs/semantics/canonical-semantics.md),
section R8-CONV-2): probability-weighted retry_overhead in expected mode and
retry_allowance_bound in hard mode; nested or correlated retry layers require
a recorded joint expectation or conservative bound, never marginal
multiplication treated as exact. Rules kept here: idempotent hops only; ONE
named layer owns retries (innermost viable); hedging is deliberate duplicate
spend listed as its own row.

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
## Canonical composition and hard-mode formulas (R8-CONV-2)

The canonical formulas are defined once, in
[docs/semantics/canonical-semantics.md](../../../../docs/semantics/canonical-semantics.md)
section R8-CONV-2, and restated for this skill only in the
[SKILL.md canonical section](../SKILL.md#canonical-retry-spend-and-hard-mode-formulas-r8-conv-2).
Cite them; do not copy, extend or re-derive the formulas here.
