---
name: observability-operator
description: Operate the observability stack hands-on — instrument services (structured logs with correlation IDs, tenant context, and redaction; metrics; traces), wire health checks (liveness, readiness, dependency), create or edit dashboards and alert rules (every alert carries severity, owner, runbook link, and a threshold justified against real signal history), verify telemetry actually flows after a deploy by running real queries, and manage alert noise (deduplication, threshold tuning, silences only with owner + expiry). Implements the alerting DESIGN from slo-reliability-architect rather than re-deriving it, and keeps the audit trail's separation: audit events are audit-log-architect territory, telemetry is not an audit log. EDITS LIVE ALERT/DASHBOARD CONFIG AND EXECUTES OPERATIONAL QUERIES — manual invocation only. Use when asked to instrument a service, add or fix alerts/dashboards/health checks, verify observability after a change, silence or tune noisy alerts, or wire telemetry for a new surface. Do NOT use to design SLOs/SLIs/error budgets or decide what should page (slo-reliability-architect), design the audit trail (audit-log-architect), author incident procedures (incident-response-runbook), or debug a live production incident (systematic-debugger).
disable-model-invocation: true
---

# Observability Operator

## Purpose

Make a system's behavior visible and its alerts trustworthy by doing the
hands-on work: instrumentation with structured, correlated, redacted
telemetry; health checks that reflect real dependencies; dashboards and
alert rules implementing the reliability design; and post-change
verification by executing real queries against the telemetry backend. The
discipline is signal-over-inventory: every alert added must be worth waking
someone for (severity, owner, runbook link, justified threshold), every
noisy alert is a debt item with a tuning plan, and every instrumentation
claim is verified by observed data, not by the code compiling.

## Use When

- Use when: asked to instrument a service or feature — logs, metrics,
  traces, correlation IDs, tenant context.
- Use when: creating or editing alert rules, dashboards, or health checks
  (liveness/readiness/dependency).
- Use when: verifying telemetry after a deploy or migration — "is the new
  surface actually visible?"
- Use when: an alert is noisy and needs tuning, deduplication, or a
  silence — bounded, owned, expiring.
- Use when: implementing the alerting/dashboard spec produced by
  `slo-reliability-architect`.
- Do NOT use when: deciding WHAT the SLOs/SLIs are or what should page —
  `slo-reliability-architect` designs; this skill implements.
- Do NOT use when: designing the tenant-scoped audit trail —
  `audit-log-architect` (audit events have integrity/retention semantics
  telemetry does not).
- Do NOT use when: writing incident procedures — `incident-response-runbook`.
- Do NOT use when: diagnosing a live failure — `systematic-debugger`
  (this skill builds the visibility that debugging uses).

## Inputs to Inspect

1. The reliability design: `slo-reliability-architect` SLIs/SLOs, burn-rate
   alert spec, symptom-vs-cause alert routing — the contract being
   implemented.
2. The current observability stack: telemetry backend(s), dashboard/alert
   config (as code or console), existing instrumentation conventions
   (logger, metric names, trace propagation).
3. The log taxonomy if one exists: levels, event names, correlation-ID
   field, redaction rules — extend it, don't fork it.
4. The service's real signal history: current volumes, baseline values for
   any threshold being set (thresholds without history are guesses —
   labeled as such with a tuning date).
5. Tenant context propagation: how tenant IDs reach telemetry (and the
   redaction/access rules for tenant-identifying data in logs).
6. Alert inventory: what already pages/tickets, current noise level,
   existing silences and their ages.
7. On-call reality: who receives what, via which paging path.

## Workflow

1. **Instrument with structure**: logs as structured events (level, event
   name, correlation ID, tenant context where the taxonomy allows,
   duration/outcome fields), metrics for the service's RED/USE signals
   (rate, errors, duration / utilization, saturation), trace propagation
   across service boundaries. Redaction applied BEFORE emission — secrets,
   credentials, and PII never reach the backend on the promise of later
   filtering.
2. **Wire health checks that tell the truth**: liveness (process up),
   readiness (can serve: dependencies checked with timeouts), dependency
   checks distinguishing hard from soft dependencies — a health check that
   always returns 200 is instrumentation theater; one that checks a
   dependency without a timeout is an outage amplifier.
3. **Implement dashboards from the design**: the SLI panels
   `slo-reliability-architect` specified, deploy markers, per-tenant/top-N
   views where the design calls for them — named and organized so the
   3am responder finds them from the alert's runbook link.
4. **Create alert rules with full metadata**: every rule carries severity,
   owner, runbook link (`incident-response-runbook` artifact), and a
   threshold justified against signal history (or labeled provisional with
   a tuning date). Page-worthy vs ticket-worthy follows the design's
   symptom/cause split — this skill does not promote causes to pages on
   its own.
5. **Verify by querying**: after instrumenting or wiring, run real queries
   against the backend — events arriving with expected fields, metrics
   moving under induced/known load, traces stitching across the boundary,
   the alert firing in a controlled test (or its query returning truth
   against historical data). "The code emits it" is not verification;
   observed data is.
6. **Manage noise as debt**: for noisy alerts — classify (bad threshold,
   missing dedup, cause-alert that should be a ticket, genuinely flapping
   system), fix the classification's cause, and use silences only as
   bridges: owner + expiry + linked follow-up, never permanent mutes.
   Alert-noise patterns that indicate product instability route to
   `systematic-debugger` as product work, not to threshold inflation.
7. **Record what changed**: alert/dashboard config changes are
   config-as-code diffs where the stack supports it (reviewed like code
   per `reviewable-diff-discipline`); console-only stacks get the change
   log written into the report. Telemetry cost impact (new log volume,
   metric cardinality) is stated — cardinality explosions are billing
   incidents wearing observability clothes.

## Output Format

```
OBSERVABILITY CHANGES — <service/scope>
Instrumentation: <what was added/changed — events, metrics, traces,
  correlation/tenant fields — with redaction posture>
Health checks: <liveness/readiness/dependency — what each actually checks,
  timeouts>
Dashboards: <created/edited — panels mapped to designed SLIs — link/path>
Alert rules: <rule — severity — owner — runbook link — threshold + its
  justification (history vs provisional+tuning date) — page or ticket>
Verification (executed): <query/test run — observed result — pass/fail per
  claim; anything unverifiable named>
Noise actions: <alert — classification — fix — silences with owner+expiry>
Cost impact: <log volume / metric cardinality deltas, order of magnitude>
Config diffs: <files/paths changed, or console change log>
Handoffs: <design gaps → slo-reliability-architect; product instability →
  systematic-debugger; audit-grade events → audit-log-architect>
```

## Validation Checklist

- [ ] Every alert rule has severity, owner, runbook link, and a threshold
      justification — no orphan alerts.
- [ ] Redaction is applied at emission; no secret/PII fields ship to the
      backend "to be filtered later".
- [ ] Health checks check real dependencies with timeouts; none
      hardcode-pass.
- [ ] Every instrumentation claim was verified by an executed query with
      the observed result recorded — unverifiable items are named.
- [ ] Every silence has an owner, an expiry, and a linked follow-up.
- [ ] Page/ticket routing follows the `slo-reliability-architect` design;
      no cause-alert was promoted to paging unilaterally.
- [ ] Telemetry cost impact (volume, cardinality) is stated.
- [ ] Audit-grade events were routed to `audit-log-architect`, not logged
      as telemetry.

## Tenant Isolation Rules

- Tenant IDs in telemetry follow the taxonomy's redaction/access rules;
  tenant-identifying data in logs is access-controlled like the data it
  identifies.
- Per-tenant dashboards for internal use never become tenant-facing
  without scoping; a tenant sees only its own signals.
- Cross-tenant top-N views (noisy-neighbor hunting) are internal-only and
  access-controlled.

## Gotchas

- Metric cardinality is the classic self-inflicted outage: per-tenant or
  per-user label values on high-volume metrics multiply series counts —
  bound label sets deliberately, use exemplars/logs for the long tail.
- Readiness checks that cascade (A checks B checks C) turn one slow
  dependency into fleet-wide unreadiness; check direct dependencies only,
  with timeouts shorter than the caller's.
- Correlation IDs die at queue boundaries and scheduled jobs — propagate
  explicitly through message envelopes and job contexts or tracing stops
  at the first async hop.
- Deploy-time verification against a quiet service proves little: verify
  against induced load or known traffic, and say which.
- A dashboard nobody can find from the alert is decoration: the runbook
  link → dashboard path is part of the alert, not documentation garnish.
- Log-based alerts on unstructured strings break on the next reword;
  alert on structured fields/metrics, never on prose.

## Stop Conditions

- Invoked without explicit human request → do not run; this skill edits
  live alert/dashboard state and executes operational queries
  (`disable-model-invocation: true` is load-bearing).
- No alerting design exists and the request is "just add some alerts" →
  route to `slo-reliability-architect` first for anything page-worthy;
  ticket-level hygiene alerts may proceed with that gap named.
- Deleting or silencing an alert that guards a security or data-loss
  signal → `human-approval-boundary` with the alert's purpose and the
  compensating coverage.
- A verification query would run against production with material load/
  cost impact (full scans, high-volume test events) → state the impact
  and get approval before executing.
- Instrumentation would emit data whose redaction status is unclear
  (possible PII/secrets) → stop and resolve the classification before
  emission, not after.

## Supporting Files

- `references/instrumentation-checklist.md` — structured-event field
  standards, RED/USE metric sets, health-check patterns, alert-metadata
  requirements, noise-classification table.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the reliability
  cluster (`slo-reliability-architect`, `incident-response-runbook`) and
  against shipped `audit-log-architect` / `systematic-debugger`.
