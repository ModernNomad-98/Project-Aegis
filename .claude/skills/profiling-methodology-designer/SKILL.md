---
name: profiling-methodology-designer
description: Design the profiling methodology that answers "where does the time (or memory) actually go" — profiler class per layer (sampling vs instrumenting CPU, allocation/heap, off-CPU/blocking-IO, distributed trace for cross-service attribution), measurement conditions that make results meaningful (warm vs cold, representative load and data volume, stated profiler overhead budget), the hypothesis-driven narrowing loop from symptom to attributed code path, baseline-profile conventions for differential diffing, and the handoff map — a blamed query to query-plan-reader, chatty access to n-plus-one-detector, browser time to frontend-perf-engineer. Produces methodology + attribution report design; never runs profilers against production (approval-gated) and fixes nothing. Use when asked how to profile or why something is slow with no evidenced suspect. Do NOT use for functional defects (systematic-debugger) or standing telemetry (observability-operator).
---

# Profiling Methodology Designer

## Purpose

Guessing is the dominant performance methodology in the wild: someone
"knows" it's the database, three weeks of tuning later p99 hasn't moved,
because the time was in serialization all along. This skill designs the
investigation that replaces guessing — which profiler class attaches to
which layer, under what load and data conditions the measurement is
valid, what overhead the act of measuring may add, and the narrowing loop
that walks from symptom to attributed code path with evidence at each
step. The deliverable is a methodology and its attribution-report format:
who measures what, in what order, and what verdict lets the fix work
begin. It attributes; the fixing belongs to the layer-owning skills the
handoff map names.

## Use When

- Use when: something is slow (or memory-hungry) and there is no
  evidenced suspect — the ask is "find where it goes", not "fix this
  query".
- Use when: asked to design a profiling approach, choose profiler types,
  or set up a performance investigation for a service, job, or request
  path.
- Use when: a `performance-test-harness` regression gate caught a
  degradation and the number needs attributing to a component before
  anyone tunes anything.
- Use when: cross-service latency needs decomposing (trace-based
  attribution) to find which hop consumes an end-to-end budget.
- Do NOT use when: the defect is functional (wrong output, crash,
  intermittent error) — evidence-driven root-cause of BEHAVIOR is
  `systematic-debugger`; this skill owns resource/time attribution.
- Do NOT use when: the suspect is already evidenced — one slow query
  goes straight to `query-plan-reader`; a request issuing hundreds of
  queries goes to `n-plus-one-detector`; browser-side slowness goes to
  `frontend-perf-engineer`. Profiling first would be ceremony.
- Do NOT use when: designing continuous production telemetry (metrics,
  dashboards, alerts) — `observability-operator` implements standing
  instrumentation; profiling here is a targeted, bounded investigation.
- Do NOT use when: building the MEASUREMENT harness that gates releases
  — `performance-test-harness` owns pass/fail measurement; this skill
  begins where its red result needs explaining.

## Inputs to Inspect

1. The symptom's evidence: which surface is slow/heavy, by how much,
   since when, at which percentile, under what load — from harness
   results, telemetry, or user reports. "Slow" without a number gets a
   number first.
2. The runtime topology of the suspect path: services touched, runtime
   platforms (this decides which profiler classes exist), async
   boundaries, queues — a request path map or its absence.
3. Existing instrumentation: traces (and their span coverage gaps),
   metrics granularity, any prior profiles or flame graphs to diff
   against.
4. Environment options: where a profiler may attach — local
   reproduction, staging with representative data, production (approval
   and overhead constraints apply) — and how representative each is of
   the symptom's conditions.
5. Data-volume reality: whether staging data volumes reproduce the
   symptom (an empty-table staging profile attributes nothing).
6. The load source available for reproduction: `load-test-planner`
   scenarios or harness workloads that can hold the system at the
   symptomatic load level while profiling.

## Workflow

1. **Pin the symptom quantitatively.** Surface, metric, percentile,
   magnitude, conditions (load level, data shape, cold/warm), and
   blast radius. A symptom that cannot be stated as a number under
   conditions cannot be attributed — get the number first (one-off
   measurement, not standing telemetry).
2. **Choose the attribution level first, profiler second.**
   Cross-service: distributed trace decomposition (which hop).
   Single service: CPU sampling (where on-CPU time goes) vs off-CPU
   analysis (where waiting happens — locks, IO, pool exhaustion) vs
   allocation profiling (what churns memory). Wrong-level profiling is
   the classic waste: a CPU flame graph of a service that is 90%
   waiting attributes the wrong 10%.
3. **Design measurement conditions.** Warm-up policy (JIT/cache-warm
   states measured separately from cold start — both matter, never
   blended), load held at the symptomatic level via the named load
   source, data volume representative of the symptom (state the
   fixture source), duration/sample count for stable percentiles, and
   the profiler's own overhead budget (sampling rates chosen so the
   measurement doesn't become the workload; instrumenting profilers
   confined to non-production or narrow scopes).
4. **Define the narrowing loop.** Hypothesis → cheapest discriminating
   measurement → evidence → narrower hypothesis, with a stop rule:
   attribution ends when a component/code path owns a stated share of
   the symptom (e.g., ≥60%) or when two loops fail to narrow (then the
   symptom is plural — split it and attribute each part separately).
   Each loop iteration records what was ruled OUT with its evidence —
   ruled-out suspects staying ruled out is what makes the loop converge.
5. **Set baseline-profile conventions.** Profiles/flame graphs captured
   under stated conditions are artifacts: named, dated,
   condition-stamped, stored with the investigation, so the next
   regression diffs against evidence instead of memory. Differential
   profiling (before/after under identical conditions) is the default
   comparison method.
6. **Map the handoffs.** The attribution verdict routes: dominant query
   → `query-plan-reader`; query-count explosion →
   `n-plus-one-detector`; browser/frontend share →
   `frontend-perf-engineer`; a hop blowing its budget →
   `latency-budget-architect`'s attribution + the owning service; cache
   candidates → `caching-strategy-designer`; systemic capacity →
   `operational-vs-analytical-splitter` or architecture surfaces. The
   methodology's job ends at an evidenced verdict + handoff.
7. **Specify the attribution report.** The Output Format below: every
   claim carries its measurement evidence and conditions; unattributed
   remainder is stated as a percentage, not rounded away.
8. **State the production posture.** If production profiling is
   required (symptom absent elsewhere): sampling-only, overhead budget
   stated, scoped window, and explicit human approval BEFORE any
   attach — this is a Stop Condition, not a footnote.

Profiler-class selection table, measurement-conditions checklist,
narrowing-loop worksheet, and the attribution-report template:
[references/profiler-selection-guide.md](references/profiler-selection-guide.md).

## Output Format

```
PROFILING METHODOLOGY — <symptom>
Symptom (pinned): <surface, metric@percentile, magnitude, conditions>
Attribution level: cross-service (trace) | on-CPU | off-CPU | allocation — why
Environment:     <where profilers attach; representativeness statement;
                  production attach: NOT without approval — posture stated>
Conditions:      warm/cold policy; load=<source, level>; data=<volume/fixture>;
                 duration/samples; profiler overhead budget=<n%>
Narrowing loop:  <hypothesis 1..n → discriminating measurement → stop rule;
                  ruled-out register>
Baselines:       <artifact naming, condition stamps, differential method>
ATTRIBUTION REPORT (on completion):
  <component/path>: <share of symptom> — evidence: <profile/trace artifact>
  unattributed remainder: <n%>
  Handoff: <query-plan-reader | n-plus-one-detector | frontend-perf-engineer |
            latency-budget-architect | caching-strategy-designer | owning team>
Not this skill:  fixes (handed off); standing telemetry (observability-operator)
```

## Validation Checklist

- [ ] The symptom is a number under stated conditions, not an adjective.
- [ ] Attribution level was chosen before profiler tooling; off-CPU was
      considered (waiting is the majority of most latency).
- [ ] Warm and cold are measured separately; neither is discarded as
      "noise" without a decision.
- [ ] Load and data volume during measurement are stated and
      representative of the symptom; the load source is named.
- [ ] Profiler overhead budget is stated; the measurement cannot
      plausibly be the workload.
- [ ] The narrowing loop has a stop rule and a ruled-out register.
- [ ] Every attribution claim carries an artifact; the unattributed
      remainder is stated.
- [ ] Handoffs are named per finding class; the methodology fixes
      nothing itself.
- [ ] Production profiling, if proposed, is sampling-only, scoped, and
      explicitly approval-gated.

## Gotchas

- Profiling the wrong state: cold-start cost profiled warm (invisible)
  or steady-state profiled cold (all JIT/cache noise). The warm/cold
  policy exists because the two have different owners and fixes.
- CPU flame graphs of waiting systems: the classic misattribution — a
  service at 15% CPU that is slow is waiting, and its flame graph
  attributes the wrong sliver. Off-CPU/blocking analysis first when
  utilization is low.
- The observer effect at scale: instrumenting profilers and verbose
  spans can double a hot path's cost; the overhead budget and
  sampling-first posture exist so the diagnosis doesn't cause the
  disease.
- Empty-staging attribution: a profile over 100 rows attributes
  nothing about production's 100 million — data volume is a
  measurement condition, not an afterthought.
- Averages hide the symptom: profiling at mean load when the complaint
  is p99 under peak attributes the wrong regime. Hold the system at the
  symptomatic percentile's conditions.
- Trace gaps masquerade as service time: a missing span makes its
  parent look slow; span-coverage audit precedes trust in trace
  decomposition.
- One profile, one conclusion: single captures are anecdotes — stable
  attribution needs repeated captures under fixed conditions
  (variance stated), especially before accusing someone's code.
- Plural symptoms resist narrowing: when two loops fail to narrow, it
  is usually two problems sharing a metric — split the symptom rather
  than forcing one culprit.

## Stop Conditions

- Asked to attach a profiler (or enable heavy instrumentation) on
  PRODUCTION → stop; produce the sampling-only, scoped, overhead-
  budgeted proposal and require explicit human approval before any
  attach. This skill never executes it.
- The symptom cannot be reproduced under any available conditions and
  production capture is denied → halt with the honest statement: the
  investigation is blocked on either reproduction fidelity or an
  approved capture; do not attribute from vibes.
- Evidence already names the suspect (one query, N+1 pattern, a
  frontend bundle) → skip methodology ceremony and route directly to
  the owning skill; profiling exists for the unattributed case.
- The "performance problem" is functional under load (errors,
  timeouts producing retries) → route to `systematic-debugger` /
  the reliability surfaces; attributing time in a failing system
  measures the failure, not the performance.
- Attribution requires reading production data content (not shapes/
  timings) → stop; profiling attributes time and allocation, never
  business data. Escalate if the investigation seems to need it.

## Supporting Files

- [references/profiler-selection-guide.md](references/profiler-selection-guide.md)
  — profiler-class selection table per layer/runtime, measurement-
  conditions checklist, narrowing-loop worksheet with the ruled-out
  register, attribution-report template.
- `evals/evals.json` — behavior cases including the off-CPU
  misattribution edge and the production-attach refusal.
- `evals/trigger-evals.json` — discrimination against
  `systematic-debugger`, `query-plan-reader`, `n-plus-one-detector`,
  `observability-operator`, and `performance-test-harness`.
