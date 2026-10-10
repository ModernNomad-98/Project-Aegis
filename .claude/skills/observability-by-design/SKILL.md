---
name: observability-by-design
description: 'Designs the telemetry contract for a system under construction: correlation IDs, structured logs, metrics, traces, and diagnostic context from the beginning, with log-redaction composition by reference to sensitive-disclosure-guard rules — never restating or weakening them. Produces the design only; instruments nothing. Use when asked to design telemetry or observability for a new or existing system, decide what to log, metric, or trace and where, or plan redaction-in-design. Do NOT use for hands-on instrumentation or stack operation (observability-operator), SLO targets or alerting policy (slo-reliability-architect), redaction-rule authorship (sensitive-disclosure-guard), synthetic-monitoring design (synthetic-monitoring-architect), or cloud-platform-specific infrastructure decisions (cloud-architecture-decider).'
---

# Observability By Design

**Reading key:** Telemetry is the data a system emits about itself: logs
(text records), metrics (numbers), and traces (end-to-end request paths). A
correlation ID is the shared identifier that ties one request's logs, metrics,
and traces together. Redaction is removing or masking sensitive values before
they are emitted; SLOs are service level objectives. PII is personally
identifiable information.

## Purpose

Produce the telemetry-contract design for a system under construction: which
components emit which logs, metrics, and traces; the correlation-ID scheme
that ties a request together; and the diagnostic context each component must
carry. Redaction is composed by reference to `sensitive-disclosure-guard`'s
rules — the design names that skill as the rule owner and never restates or
weakens its rules. It designs; it instruments nothing.

## Use When

- Use when: asked to design telemetry or observability for a new or existing system.
- Use when: asked to decide what to log, metric, or trace, and where.
- Use when: asked for a correlation-ID scheme or diagnostic-context plan.
- Use when: asked to plan redaction-in-design (which fields must never be emitted, per the owning skill's rules).
- Do NOT use when: the ask is hands-on instrumentation, running the stack, or editing dashboards/alerts — that is `observability-operator` *(manual-only)*.
- Do NOT use when: the ask is SLO targets, error budgets, or alerting policy — that is `slo-reliability-architect`.
- Do NOT use when: the ask is authoring or changing redaction RULES themselves — that is `sensitive-disclosure-guard`.
- Do NOT use when: the ask is synthetic-monitoring design (probes against the live app) — that is `synthetic-monitoring-architect`.
- Do NOT use when: the ask is cloud-platform-specific infrastructure or IaC choices — that is `cloud-architecture-decider`.

## Inputs to Inspect

1. The service architecture and data flows: components, call paths, queues, and where a request crosses a boundary.
2. `sensitive-disclosure-guard`'s redaction rules, when present — the design composes them by reference.
3. Existing observability stack notes (collector, storage, dashboard tooling) if any, to compose reality.
4. SLO and reliability documents, to align metric names with the targets `slo-reliability-architect` owns.
5. Prior incident notes or known failure modes the telemetry must make diagnosable.

## Workflow

1. **Map the system.** List the components and the flows between them, including async hops where correlation is lost without a carried ID.
2. **Write the telemetry contract per component.** For each component: which logs (with levels), which metrics (with labels), which spans; what each record must carry to be diagnosable.
3. **Define the correlation-ID scheme.** Where IDs are created, propagated, and logged across synchronous and asynchronous boundaries.
4. **Compose redaction by reference.** Name `sensitive-disclosure-guard` as the redaction-rule owner; mark the fields the contract must treat as sensitive and defer the rules to that skill — never restate or weaken them.
5. **Bound the metrics and traces.** Name the small set of metrics and spans that matter; reject over-instrumentation.
6. **Emit the design** in the Output Format, stating what was chosen, why, and the main rejected alternative.

## Output Format

Emit the design in the conversation (nothing is written to the repo):

```
TELEMETRY CONTRACT DESIGN — <system / service>
Components: <each component named, with its flows>
Per-component contract:
  <component> — logs <what, levels> — metrics <names + labels> — spans <what>
  — must carry <diagnostic context>
Correlation-ID scheme: <created at, propagated via, logged at each hop>
Redaction (composed, not restated):
  fields <list> — rules owned by sensitive-disclosure-guard — applied at <emit points>
Metrics & traces bound: <the kept set; what was rejected as over-instrumentation>
Out of scope:
  instrumentation / stack operation → observability-operator
  SLOs / alerting → slo-reliability-architect
  redaction-rule authorship → sensitive-disclosure-guard
  synthetic monitoring → synthetic-monitoring-architect
  platform IaC → cloud-architecture-decider
Chosen / why / rejected: <the key choices, the reason for each, and the main
  rejected alternative>
```

## Validation Checklist

- [ ] Every component has a telemetry contract; none assumed silent.
- [ ] The correlation-ID scheme covers synchronous AND asynchronous hops.
- [ ] Redaction is composed by reference to `sensitive-disclosure-guard`; no rule is restated or weakened.
- [ ] The metric/trace set is bounded, with the over-instrumentation rejects named.
- [ ] The design claims to instrument nothing.

## Gotchas

- Log bloat: a contract that logs everything logs nothing useful. Keep the set small and state what was rejected.
- PII in logs is the expensive failure: a field that is fine today becomes a breach tomorrow. Compose the redaction owner's rules; do not improvise local ones.
- Over-instrumentation burns cardinality and storage budgets; bounded metric sets are part of the design.
- Handing instrumentation or stack operation to this skill breaks the manual-only boundary — `observability-operator` runs and edits live systems; this skill designs only.
- Restating `sensitive-disclosure-guard`'s rules duplicates the owning skill and drifts when it changes; reference it.

## Stop Conditions

- No architecture or data-flow context is supplied or findable → stop and ask for it; a telemetry contract cannot start from "add observability".
- The request becomes hands-on instrumentation, stack operation, or dashboard/alert edits → hand off to `observability-operator` *(manual-only)*.
- The request becomes authoring redaction rules → hand off to `sensitive-disclosure-guard`.
- The request becomes SLO/alerting policy → hand off to `slo-reliability-architect`.
- The request involves destructive or live-state action → stop and refuse.

## Supporting Files

- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `observability-operator`, `slo-reliability-architect`, `sensitive-disclosure-guard`, `synthetic-monitoring-architect`, and `cloud-architecture-decider`.
- `references/` — None: the design is self-contained.
