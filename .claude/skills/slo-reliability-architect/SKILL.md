---
name: slo-reliability-architect
description: Derive SLOs from user journeys, not from infrastructure — inventory the journeys users actually depend on, select symptom-based SLIs per journey (availability, latency percentiles, correctness, freshness measured where the user experiences them), set SLO targets with explicit error budgets, design burn-rate alerting where PAGES fire on symptoms/budget burn and causes (CPU, restarts, queue depth) go to tickets and dashboards, analyze failure modes and dependency chains against the targets, and define the error-budget policy (what happens to release velocity when the budget is spent) plus per-tenant/noisy-neighbor reliability views and a review cadence. Produces the SLO catalog, alert spec, and dashboard spec that observability-operator implements. Use when asked to define SLOs/SLIs/error budgets, decide what should page, set reliability targets for a product or journey, rationalize an alert inventory around symptoms, or negotiate reliability vs release velocity. Do NOT use to implement alerts/dashboards/instrumentation (observability-operator), author incident procedures (incident-response-runbook), design the availability SLA in customer contracts (commercial decision it informs), or debug current failures (systematic-debugger).
---

# SLO Reliability Architect

## Purpose

Produce a reliability design the business can reason about and on-call can
live with: user-journey-derived SLOs with error budgets, symptom-based SLIs
measured where users experience them, burn-rate alerting that pages only on
what threatens the budget, failure-mode analysis against the targets, and
the budget policy that converts reliability data into release decisions.
The discipline is journeys-before-infrastructure: users do not experience
CPU; they experience "checkout failed" — so checkout, not CPU, is what gets
a target, a budget, and a page.

## Use When

- Use when: asked to define SLOs, SLIs, or error budgets for a product,
  service, or user journey.
- Use when: deciding what should page vs ticket — or rationalizing a noisy
  alert inventory around symptoms.
- Use when: setting reliability targets for a new surface, or revisiting
  targets after incidents or architecture changes.
- Use when: reliability vs release-velocity tension needs a policy (the
  error budget is that policy).
- Use when: a multi-tenant product needs per-tenant reliability visibility
  (noisy neighbors, enterprise-tier commitments).
- Do NOT use when: implementing the resulting alerts, dashboards, or
  instrumentation — `observability-operator` (manual-only) executes this
  design.
- Do NOT use when: writing what on-call DOES when paged —
  `incident-response-runbook`.
- Do NOT use when: drafting contractual SLAs — this skill informs the
  commercial decision with achievable numbers; it does not own the
  contract.
- Do NOT use when: diagnosing an active reliability problem —
  `systematic-debugger`.

## Inputs to Inspect

1. The user journeys that matter: product flows, `qa-strategy-architect`
   risk inventory / `test-plan-designer` critical journeys if present —
   reliability targets attach to what users depend on.
2. Real traffic and failure history: request volumes, current
   availability/latency distributions, incident history — targets set
   without baseline data are aspirations, labeled as such.
3. The architecture and dependency chains (`architecture-designer` /
   provider-architect outputs): what each journey traverses, shared
   dependencies, single points of failure.
4. Current alert inventory and its noise profile (what pages today, what
   on-call ignores).
5. Commercial commitments: SLAs already sold, tier promises, enterprise
   contracts — the floor the SLOs must clear with margin.
6. Tenancy shape: pooled/siloed components, tenant size skew — whether one
   tenant's experience can diverge from the aggregate.
7. Deploy/release cadence and the team's appetite for a budget policy with
   teeth.

## Workflow

1. **Inventory the journeys**: enumerate the user journeys worth a
   reliability promise (login, core workflow, checkout/billing, data
   export, API integration paths), each with its user population, business
   impact of failure, and traffic volume. Rank; not everything gets an
   SLO — an SLO catalog nobody can recite protects nothing.
2. **Select symptom-based SLIs per journey**: availability (good events /
   valid events, with "good" and "valid" defined precisely — what counts,
   what is excluded, where measured), latency (percentile thresholds at
   the user-experienced edge, not the backend hop), correctness/freshness
   where the journey's value is data (exports complete, dashboards
   current). Measurement point stated per SLI: load balancer, client,
   synthetic — each with its blind spots named.
3. **Set targets with error budgets**: per SLI, a target justified by
   baseline data, commercial floor, and cost of the next nine — with the
   error budget stated in user-meaningful units (minutes of full outage
   per month, failed requests per million). Targets without baseline data
   are labeled provisional with a review date.
4. **Design burn-rate alerting**: pages fire on budget burn rates
   (fast-burn: page now; slow-burn: page/ticket on sustained burn), causes
   (CPU, GC, restarts, queue depth) go to tickets and dashboards as
   diagnostic context. Every page maps to a budget threat; every
   cause-alert that pages today is explicitly demoted or defended in the
   spec. Alert spec fields: SLI, burn threshold + window, severity,
   owner, runbook link placeholder — handed to `observability-operator`
   to implement and to `incident-response-runbook` for the procedures.
5. **Analyze failure modes against targets**: per journey, walk the
   dependency chain — shared dependencies whose failure burns multiple
   budgets, retry/timeout behavior that amplifies, saturation points,
   and the blast radius of each dependency's failure. Findings that
   require architectural change route to `architecture-designer`; this
   skill sizes the reliability impact.
6. **Define the error-budget policy**: what happens when a budget is
   spent — release freeze/slowdown criteria, who decides exceptions, how
   the budget resets, and what "budget spent on planned work vs incidents"
   means. A budget with no consequences is a chart, not a policy.
7. **Add the tenant dimension**: per-tenant SLI views where tenancy skew
   can hide misery in aggregates (one big tenant at 50% error rate inside
   a 99.9% aggregate), noisy-neighbor detection signals, and
   tier-differentiated targets where commercial commitments differ.
8. **Set the review cadence**: SLO review rhythm (post-incident, quarterly
   target review, alert-precision review — pages that led to action vs
   noise), and the staleness triggers (architecture change, traffic-shape
   change) that reopen the design.

## Output Format

```
RELIABILITY DESIGN — <product/scope>
Journey inventory: <journey — users — business impact — volume — ranked;
  explicitly not-covered journeys listed>
SLI definitions: <journey — SLI — good/valid definitions — measurement
  point + blind spots>
SLO targets & budgets: <SLI — target — budget in user-meaningful units —
  justification (baseline/commercial/cost) — provisional flags + review
  dates>
Alert spec (for observability-operator): <SLI — fast/slow burn thresholds
  + windows — severity — owner — page/ticket — runbook link placeholder>
Demotions: <today's cause-alerts that stop paging, each with rationale>
Failure-mode analysis: <journey — dependency chain — shared/single points
  — amplification risks — architectural findings routed>
Error-budget policy: <spent-budget consequences — decider — reset — 
  planned-work accounting>
Tenant dimension: <per-tenant views needed — noisy-neighbor signals —
  tier-differentiated targets>
Review cadence: <rhythms + staleness triggers>
Assumptions & open questions: <each with risk-if-wrong / who answers>
```

## Validation Checklist

- [ ] Every SLO traces to a user journey with named business impact — no
      SLO exists because a metric was available.
- [ ] Every SLI defines "good" and "valid" precisely and names its
      measurement point with blind spots.
- [ ] Every target carries a justification (baseline data, commercial
      floor, cost) or a provisional label with a review date.
- [ ] Error budgets are stated in user-meaningful units.
- [ ] Every page in the alert spec maps to budget burn; every currently
      paging cause-alert is explicitly demoted or defended.
- [ ] The budget policy has consequences and a decider.
- [ ] The tenant dimension is addressed (or explicitly n/a for
      single-tenant).
- [ ] Implementation was handed to `observability-operator`, procedures to
      `incident-response-runbook` — neither restated here.

## Gotchas

- Availability measured at the backend misses the CDN, DNS, and client —
  the user's 99.9% and the server's 99.99% differ by real outages; name
  the measurement point's blind spots.
- Percentile latency over a low-traffic window is noise: a p99 on 50
  requests pages on one slow request. Windows and minimum-volume guards
  are part of the SLI definition.
- 100%-minus-epsilon targets are budget-free zones: a 99.99% target on a
  monthly window is ~4 minutes of budget — no room to deploy. The next
  nine must be priced, not defaulted.
- Aggregate SLOs hide tenant misery in skewed populations; if one tenant
  is 40% of traffic, per-tenant views are not optional.
- Retries mask failures into latency: a journey "succeeding" after three
  retries burns latency budget invisibly and amplifies load at the worst
  time — count retried-success distinctly.
- Error budgets spent by planned maintenance vs incidents are different
  signals; a policy that cannot tell them apart freezes releases for the
  wrong reasons.

## Stop Conditions

- No baseline data exists and none can be gathered (new product) →
  provisional targets only, labeled, with instrumentation-first ordering
  (`observability-operator`) and a mandatory review date; refuse to
  present aspirations as commitments.
- The commercially promised SLA exceeds what the architecture can
  plausibly deliver → surface the gap to the human as a commercial/
  architecture decision (`human-approval-boundary` for the tradeoff);
  do not design SLOs that paper over it.
- Journey inventory cannot be established (nobody can say what users
  depend on) → stop; route to product/`qa-strategy-architect` risk
  inventory first. SLOs on infrastructure metrics alone are refused.
- The error-budget policy has no owner willing to enforce consequences →
  deliver the design with the policy gap named as its top risk.

## Supporting Files

- `references/slo-derivation.md` — SLI menu per journey type,
  burn-rate window/threshold patterns, budget-policy templates.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the reliability
  cluster (`observability-operator`, `incident-response-runbook`) and
  against shipped `qa-strategy-architect` / `saas-cost-architect`.
