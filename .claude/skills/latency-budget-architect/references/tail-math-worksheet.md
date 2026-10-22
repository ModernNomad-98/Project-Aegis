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
Cascade check, leaf to root:
  timeout(upstream) > own work(upstream) + downstream critical-path budget +
  recorded epsilon
  own work = what the hop itself spends (processing, serialization, queue and
  connection waits it owns); downstream critical-path budget = serial
  downstream hops + the longest parallel branch at each join, including the
  initial attempt, retry spend defined in the retry-spend accounting section. Epsilon is recorded
  once.

## Retry-spend accounting

```
total_expected_hop_cost(hop) = own attempt work(hop) + wait_0
                               + downstream critical-path budget(hop)
                               + retry_overhead(hop)
retry_overhead(hop) = the sum over k=1..K of
                      P(k-th retry) × (attempt work(hop) + wait_k)
Definitions: wait_0 is the pre-initial-attempt wait this hop owns (queue/dispatch
before the first attempt; 0 when none); p is the per-attempt retry probability (P(k-th
retry) = p^k under independent retries, or record a measured cumulative value and state
that assumption); wait_k is the wait before the k-th retry from the recorded per-attempt
backoff (base × 2^(k-1)), not aggregate backoff_total; K is the permitted retries for
this hop. The initial attempt is counted exactly once (first line) and is NOT inside
retry_overhead. retry_overhead is LOCAL retry work only (attempt work + wait_k).
downstream critical-path budget(hop) covers downstream hops' initial work and retry spend
once; it excludes this hop's own initial attempt/retry spend. If this hop's retry
re-invokes downstream work, add that re-executed downstream cost to the retry term (or
explicitly limit the formula to local-only retry work and state the limitation). Record p,
wait_0, the independence/one-retry-layer assumption, and which layer owns retries. Use
total_expected_hop_cost for budget claims; retry_overhead is reported separately.
Worked example: p=0.1, K=4, attempt work=40ms, wait_0=0ms, downstream
critical-path budget=200ms, base backoff=10ms so the PER-ATTEMPT waits are
10/20/40/80ms (wait_k = 10·2^(k-1); these are per-attempt waits, NOT cumulative
time-to-attempt - cumulative time to attempt k would be base·(2^k - 1) and is not used
here): retry_overhead = 0.1·(40+10) + 0.01·(40+20) + 0.001·(40+40) + 0.0001·(40+80)
= 5.0 + 0.6 + 0.08 + 0.012 = 5.692ms.
total_expected_hop_cost = own attempt work 40 + wait_0 0 + downstream budget 200 +
retry_overhead 5.692 = 245.692ms.
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
