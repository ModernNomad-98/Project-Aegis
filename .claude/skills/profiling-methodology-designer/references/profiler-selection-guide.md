# Profiler Selection Guide

Selection tables and worksheets backing the methodology. Tool-agnostic:
"sampling CPU profiler" means whatever fills that class on your runtime.

## Attribution-level decision (before any tool)

| Symptom shape | Level | Instrument class |
|---|---|---|
| End-to-end latency across services | cross-service | distributed trace decomposition (audit span coverage first) |
| One service slow, CPU utilization HIGH | on-CPU | sampling CPU profiler → flame graph |
| One service slow, CPU utilization LOW | off-CPU | off-CPU/blocking profiler; lock/pool/IO wait analysis |
| Memory growth / GC pressure / OOM | allocation | allocation/heap profiler; retention snapshots diffed |
| Slow only at high concurrency | off-CPU first | contention analysis (locks, pools, queues), then on-CPU |
| Batch/job wall-clock | phase timing first | coarse phase stamps, then the dominant phase gets the above |

Low utilization + slow = waiting. The single most common misattribution
is an on-CPU flame graph of a system that is waiting.

## Profiler-class properties

| Class | Overhead | Prod-viable | Blind spots |
|---|---|---|---|
| Sampling CPU | very low (rate-bound) | yes, with approval + stated rate | off-CPU time entirely; very short spikes under the sample rate |
| Instrumenting/tracing CPU | high (can 2× hot paths) | no — non-prod only | its own overhead distorts ranking |
| Off-CPU / blocking | low–medium | sometimes (platform-dependent) | attributing WHICH wait needs symbolized stacks |
| Allocation/heap | medium; snapshots pause | snapshots with care | allocation site ≠ retention cause; needs dominator/retention view |
| Distributed trace | per-span cost; sampling policy | yes (already standing) | span gaps read as parent time; clock skew across hosts |

## Measurement-conditions checklist

- [ ] Warm-up: N discarded iterations stated; cold-start measured as its
      OWN experiment when startup is part of the symptom.
- [ ] Load: held at symptomatic level by a named source
      (load-test-planner scenario / harness workload) for the full
      capture window.
- [ ] Data: volume + shape representative (named fixture/dataset);
      never an empty store.
- [ ] Duration/samples: enough for stable percentiles (state the
      variance across repeated captures; ≥3 captures before accusing a
      component).
- [ ] Overhead budget: profiler cost ≤ <n>% of the measured path,
      stated and checked (compare a profiled vs unprofiled run).
- [ ] Environment stamp: build/version, config, instance size — on the
      artifact.

## Narrowing-loop worksheet

```
LOOP <n>
Hypothesis:     <component/path suspected, and WHY (prior evidence)>
Discriminator:  <cheapest measurement that splits hypothesis true/false>
Result:         <evidence artifact>
Verdict:        narrowed to <X> | RULED OUT <X> (→ register) | no narrowing
RULED-OUT REGISTER: <suspect — evidence — conditions> (append-only)
STOP RULE: attributed ≥<share>% to one component/path ⇒ report & hand off;
two consecutive no-narrowing loops ⇒ split the symptom (it is plural).
```

## Baseline & differential conventions

- Artifact naming: `<surface>-<condition>-<date>-<build>` (e.g.
  `checkout-warm-p99load-<date>-<build>`), stored with the
  investigation record.
- Differential profiling: identical conditions, before/after builds;
  compare SHARES not absolute samples; a new bar in the flame graph
  outranks a taller one.
- Regressions from `performance-test-harness` diff against the
  baseline captured at the harness's own conditions — one conditions
  vocabulary across both skills.

## Attribution-report template

```
ATTRIBUTION — <symptom> (<date>)
Conditions: <load, data, warm/cold, environment, captures=N, variance>
Findings:
  1. <component/path> — <share>% of <metric> — artifact: <name>
  2. ...
Unattributed remainder: <n>% (stated, not rounded away)
Ruled out: <register summary>
Handoffs: <finding → owning skill/team>
Production capture used: none | approved <ref, scope, overhead observed>
```
