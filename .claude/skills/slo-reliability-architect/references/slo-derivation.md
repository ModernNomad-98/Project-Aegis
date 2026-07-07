# SLO Derivation Reference

Detail file for `slo-reliability-architect`. Loaded on demand.

## SLI menu per journey type

| Journey type | Primary SLIs | Definition notes |
| --- | --- | --- |
| Interactive request (login, page, API call) | availability = good/valid; latency pXX at the edge | exclude client aborts from valid? decide and write it down; percentiles need minimum-volume guards |
| Transactional flow (checkout, provisioning) | end-to-end success rate; time-to-complete | multi-step: define the success event, count retried-success distinctly |
| Async pipeline (exports, reports, ingestion) | freshness (age of newest complete result); completeness | "done within N" is the user promise, not queue depth |
| Data display (dashboards) | correctness/freshness | staleness the user can see is the symptom |
| Integration surface (webhooks, feeds) | delivery success within window; ordering where promised | consumer-observed, not send-attempted |

## Burn-rate alerting patterns

Budget burn rate = (error rate) / (1 − target). Standard two-window form:

| Alert | Burn rate | Long window | Short window (confirm) | Action |
| --- | --- | --- | --- | --- |
| Fast burn | high (budget gone in hours) | ~1h | ~5m | PAGE |
| Slow burn | moderate (budget gone in days) | ~6h | ~30m | page or high-priority ticket |
| Trickle | slow (budget at risk this window) | ~3d | ~6h | ticket |

Exact multipliers/windows are tuned to the SLO window and traffic shape —
the table is the pattern, not gospel. Both-windows-firing suppresses
deploy-blip false pages. Cause signals (CPU, GC, restarts, queue depth)
appear on the diagnostic dashboard the page links to — they do not page.

## Error-budget policy template

```
Budget: <SLI> — <X units per window>
When budget is spent:
  - <threshold, e.g., 100% spent> → <consequence: feature-release freeze;
    reliability work only> — decider: <role>
  - <75% spent> → <consequence: risky-change review tightens;
    release-readiness-reviewer gate required on all deploys>
Exceptions: <who may override, recorded where>
Reset: <rolling window / calendar window>
Accounting: planned maintenance vs incident burn tracked separately;
  planned burn requires pre-approval against remaining budget.
Review: post-incident always; quarterly target review; alert-precision
  review (pages that led to action / total pages).
```

## Target-setting heuristics

- Start from measured baseline; set the first target slightly better than
  the observed p50 month, not at the dream number.
- Price the next nine: each added nine multiplies infrastructure and
  process cost — name what it buys and what it costs.
- Internal SLO must clear the contractual SLA with real margin (the SLA is
  the floor with penalties; the SLO is the operating target).
- Tier-differentiated targets need tier-differentiated measurement —
  a premium-tier promise without per-tier SLIs is unenforceable.
