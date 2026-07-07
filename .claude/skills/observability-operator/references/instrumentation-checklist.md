# Instrumentation Checklist Reference

Detail file for `observability-operator`. Loaded on demand.

## Structured event field standard (minimum)

| Field | Rule |
| --- | --- |
| level | from the taxonomy; ERROR reserved for actionable failures |
| event | stable snake_case name — alert/query key, never reworded casually |
| correlation_id | present on every request-scoped event; propagated through queues/jobs via envelopes |
| tenant | per taxonomy + redaction rules; access-controlled downstream |
| duration_ms / outcome | on operation-complete events |
| redaction | applied BEFORE emission — no secrets/PII ever, no "filter later" |

## Default metric sets

- **Services (RED):** request rate, error rate (by class), duration
  (histogram/percentiles) — per endpoint/operation, bounded label sets.
- **Resources (USE):** utilization, saturation (queue depth, pool wait),
  errors — per resource.
- **Jobs/queues:** processed rate, failure rate, lag/age of oldest item,
  dead-letter depth.
- Cardinality rule: label values must be bounded sets (endpoint, status
  class, region). Unbounded values (user id, tenant id on high-volume
  metrics, request id) go to logs/traces/exemplars instead.

## Health-check patterns

| Check | Answers | Rules |
| --- | --- | --- |
| Liveness | is the process alive | no dependency calls; cheap; restarts on fail |
| Readiness | can it serve now | direct hard dependencies only, each with a timeout shorter than the caller's; soft deps degrade, not fail |
| Dependency | is X reachable/healthy | reported per dependency for dashboards; never cascaded transitively |

## Alert rule metadata (all four required)

1. **Severity** — page vs ticket per the `slo-reliability-architect`
   symptom/cause split.
2. **Owner** — a team/rotation, not a person's name.
3. **Runbook link** — resolvable, pointing at the relevant
   `incident-response-runbook` section.
4. **Threshold justification** — derived from N days/weeks of signal
   history, or labeled `provisional — tune by <date>`.

## Noise classification table

| Pattern | Classification | Fix |
| --- | --- | --- |
| Fires on deploys, self-resolves | bad threshold / missing deploy-awareness | widen window, deploy markers, burn-rate form |
| Fires in bursts for one cause | missing dedup/grouping | group by root label; inhibition rules |
| Cause-alert paging (CPU, GC, pod restart) | should be ticket/dashboard | demote per design; symptom alert covers paging |
| Fires nightly at backup/cron | predictable saturation | schedule-aware threshold or fix the contention (product work) |
| Genuinely intermittent product failure | NOT alert noise | route to `systematic-debugger` — do not tune away real signal |

Silences: owner + expiry + linked follow-up, always. A silence without an
expiry is a deleted alert wearing a maintenance costume.

## Verification query patterns

- New event: query for it filtered to the deployed version/window; confirm
  expected fields non-null.
- New metric: confirm series exist AND move under known/induced load; note
  which load.
- Trace: confirm spans stitch across the changed boundary (one trace id,
  parent-child intact).
- Alert: fire it in a controlled test or replay its query over a
  historical window that should have fired; record the result.
