---
name: product-analytics-instrumenter
description: 'Design the INSTRUMENTATION for product analytics — where/how the analytics events (defined by event-schema-architect) fire: client-side vs server-side capture and when server-side is more trustworthy, the capture points, identity/session, consent and privacy (opt-out, consent-gated capture, PII minimization at the source, regional rules), capture reliability, tracking QA (does the event fire with the right properties), avoiding double-counting, and the debug/verification workflow. This is USER-facing PRODUCT analytics — NOT system telemetry for engineers (observability-operator) and NOT the skill-library usage signal (skill-usage-instrumenter). Use when instrumenting product analytics events, deciding client vs server tracking, gating capture on consent, or QAing that tracking fires correctly. Do NOT use for system logs/metrics/traces and alerting (observability-operator), which library skills fire (skill-usage-instrumenter), or defining the event schema (event-schema-architect).'
---

# Product Analytics Instrumenter

**Reading key:** Personally identifiable information (PII) can identify a
person; quality assurance (QA) checks that tracking works; a software
development kit (SDK) is a provider's client library; user interface (UI)
means what a user interacts with; an internet protocol (IP) address can be
personal data. GDPR and CCPA refer to European Union and California privacy
laws; Do Not Track (DNT) is a browser preference whose handling must be
checked against the product's applicable policy and law.

## Purpose

A perfect tracking plan produces zero insight if the events don't fire,
fire twice, fire before consent, or fire from the ad-blocked client for a
number that has to be right. This skill designs the instrumentation that
turns a schema into trustworthy data: which events fire client-side vs
server-side and why, the capture points, identity and session handling at
the moment of capture, consent gating and PII minimization AT THE SOURCE,
reliability against data loss, de-duplication so nothing double-counts,
and a tracking-QA workflow that verifies events actually fire with the
right properties. It instruments USER behavior for product and growth
decisions — deliberately distinct from system telemetry for engineers
(`observability-operator`) and from the signal of which library skills
fire (`skill-usage-instrumenter`). Three different "instrumentation"
jobs; this one is the product-analytics slice.

## Use When

- Use when: instrumenting product analytics events — deciding where in
  the product/code each event fires and how.
- Use when: choosing client-side vs server-side tracking for accuracy,
  reliability, or ad-blocker resistance.
- Use when: gating analytics capture on consent, respecting opt-out/DNT,
  or minimizing PII at the point of capture for compliance.
- Use when: analytics numbers are wrong because events double-count, drop
  on navigation, or fire before identity is set — or when you need to QA
  that tracking matches the plan.
- Do NOT use when: the task is SYSTEM telemetry for engineers — service
  logs, metrics, traces, health checks, alerting — that is
  `observability-operator` (operating the observability stack, not
  product behavior).
- Do NOT use when: the task is measuring which SKILLS in THIS library
  fire in practice — that is `skill-usage-instrumenter` (the library's
  self-measurement, under strict minimization).
- Do NOT use when: the task is DEFINING the events/properties/taxonomy —
  that is `event-schema-architect`; this skill instruments against that
  schema, it doesn't design it.

## Inputs to Inspect

1. The tracking plan (from `event-schema-architect`): the events,
   properties, and identity model to instrument. If it doesn't exist,
   route there first — instrumenting undefined events bakes in the mess.
2. The surfaces and stack: web/mobile/backend, the frameworks, and where
   in the code user actions and state changes occur (the capture points).
3. Accuracy needs per event: which events must be exact (revenue, state
   changes → server-side candidates) vs which are UI interactions
   (client-side acceptable).
4. The consent/privacy regime: consent requirements (GDPR/CCPA and
   similar), opt-out/DNT handling, and the PII flags on the schema that
   constrain what may be captured.
5. Current instrumentation health: existing double-counts, drops, or
   fire-before-identify bugs, and whether any tracking QA exists today.

## Workflow

1. **Anchor on the schema.** Take the events/properties/identity model
   from the tracking plan as the target. A missing or fuzzy schema routes
   to `event-schema-architect` before any instrumentation.
2. **Choose capture location per event.** Compare three plain options:
   client capture sees UI-only actions but can be blocked, dropped on tab
   close, or repeated on re-render; server capture sees committed state and
   is more reliable for purchases or billing, but cannot see every UI
   interaction; both can connect intent to outcome but need a shared event
   key and a named authoritative count to reconcile duplicates and gaps.
   For each event, name what each location can actually observe, expected
   loss/retry behavior, and the source of truth for the reported metric.
   Estimate ingestion volume and compute cost, setup effort, and ongoing
   QA/monitoring upkeep for each viable option. Recommend client, server,
   or both in the event's context, explaining why its visibility and
   reliability justify those costs; do not call both automatically safer.
   Mark unknown costs as unknown and verify current prices if a precise
   spend choice depends on them. If a decisive context fact is missing,
   ask one discovery question before recommending; if the user must choose,
   ask one atomic decision question. That choice alone grants no capture
   or vendor-spend authority.
3. **Design the capture points and wrapper.** Route all tracking through
   one instrumentation layer/wrapper rather than scattered SDK calls, so
   naming/properties stay consistent and QA has one seam. Prefer
   declarative capture where the framework allows.
4. **Handle identity and session at capture.** Set anonymous/user/tenant
   ids and session per the identity model; call identify/alias at the
   right lifecycle moment so events attribute correctly and anonymous
   events later stitch. Firing before identity is set is a top cause of
   broken funnels.
5. **Gate on consent and minimize PII at the source.** Do NOT capture
   before consent where required; honor opt-out and Do-Not-Track;
   drop/redact any property the schema flagged sensitive AT capture, not
   later. Handle IP/geo and regional rules. This is a hard boundary, not
   a preference.
6. **Design for reliability.** Batch and flush on page unload/navigation
   so events aren't lost; retry on transient failure; handle offline;
   and if sampling is used, state its effect on the metrics (and never
   sample the events a funnel or experiment depends on without saying so).
7. **Prevent double-counting.** De-duplicate client retries and
   re-render double-fires (idempotency keys / fire-once guards); ensure
   one authoritative source per event (don't count the same purchase from
   both client and server). Double-counting silently inflates every
   metric.
8. **Build tracking QA.** A tracking-plan test: assert each event fires,
   with the right name and typed properties, at the right moment — in a
   debug/verification mode and in staging. A regression guard so a schema
   change or refactor that breaks tracking fails loudly, not silently.
9. **Name boundaries and deliver.** Schema → `event-schema-architect`;
   system telemetry → `observability-operator`; skill-library usage →
   `skill-usage-instrumenter`. Produce the instrumentation plan in the
   Output Format with a contextual capture recommendation, alternatives,
   reconciliation rule, and cost/upkeep assumptions.

The client-vs-server decision table, the consent-gating checklist,
de-dup patterns, and the tracking-QA workflow:
[references/instrumentation-sheet.md](references/instrumentation-sheet.md).

## Output Format

```
ANALYTICS INSTRUMENTATION PLAN — <product/surface>
Schema source: event-schema-architect tracking plan (target)
Per event:     capture=<client|server|both> — recommended option and context;
               client/server visibility and loss risks; authoritative metric source;
               capture point; properties set
Identity:      anon/user/tenant + session set at capture; identify/alias moment
Consent/PII:   capture gated on consent; opt-out/DNT honored; sensitive props dropped AT source;
               regional rules
Reliability:   batching/flush-on-unload; retry; offline; sampling (+ metric impact if any)
De-dup:        fire-once/idempotency; if both capture, shared key + reconciliation;
               one authoritative count per event
Tracking QA:   plan test (event fires, right name+typed props, right moment); staging + debug mode;
               regression guard
Choice costs:  per viable option, ingestion/compute money (estimate or
               explicit unknown), setup effort and monitoring/QA upkeep;
               assumptions and why recommendation wins
Owner decision: when needed, one atomic capture-choice question after the
               recommendation; if decisive context is missing, one discovery
               question first
Boundaries:    schema → event-schema-architect; system telemetry → observability-operator;
               skill usage → skill-usage-instrumenter
```

## Validation Checklist

- [ ] Instrumentation targets a defined tracking plan; a missing schema
      routes to `event-schema-architect`.
- [ ] Client, server and both were compared in plain terms for relevant
      visibility, loss/retry risk and authoritative counting; each event has
      a contextual recommendation. Accuracy-critical events use server
      authority; both has an explicit reconciliation key and rule.
- [ ] Viable capture options name ingestion/compute money as an estimate
      or explicit unknown, setup effort, ongoing monitoring/QA upkeep and
      the assumptions behind the choice; unknown prices are not invented.
- [ ] If owner choice is needed, the output asks one atomic decision
      question after the explanation, or one discovery question first when
      decisive context is missing; the choice grants no capture or spend.
- [ ] Tracking runs through one wrapper/layer, not scattered SDK calls.
- [ ] Identity/session is set at capture and identify/alias fires at the
      right moment (no fire-before-identify).
- [ ] Capture is consent-gated; opt-out/DNT honored; sensitive properties
      dropped AT the source; regional rules addressed.
- [ ] Reliability is designed (flush on unload, retry, offline); sampling
      impact on dependent metrics is stated.
- [ ] De-duplication prevents double-counting; each event has one
      authoritative source.
- [ ] A tracking-QA test verifies events fire correctly, with a
      regression guard.
- [ ] System-telemetry, skill-usage, and schema concerns are handed to
      their owning skills.

## Gotchas

- Three unrelated jobs are all called "instrumentation": product
  analytics (this skill — user behavior), system telemetry
  (`observability-operator` — engineer-facing logs/metrics/traces), and
  skill-library usage (`skill-usage-instrumenter`). They have different
  consumers, privacy stances, and owners; don't blur them.
- Tracking accuracy-critical events (purchases, upgrades) client-side is
  a slow-motion data loss: ad blockers, crashes, and closed tabs eat
  them, and the number is quietly low forever. Money moves server-side.
- Firing events before `identify` orphans them under an anonymous id that
  never joins the user — the funnel undercounts and no error is thrown.
  Order of capture vs identity matters.
- Capturing before consent (or ignoring opt-out/DNT) is a compliance
  violation, not a data-completeness win. Consent gates capture; minimize
  PII at the source, because scrubbing it downstream is unreliable and
  too late.
- Double-firing on React re-renders or client retries inflates every
  metric silently — a 2× conversion "improvement" that's really a
  double-count. Fire-once guards and one authoritative source per event
  are not optional.
- Events lost on navigation (fired but the page unloads before the
  request sends) are a classic silent gap. Flush on unload / use the
  beacon path for last-moment events.
- Instrumentation with no QA drifts the moment someone refactors the
  component; the tracking plan says one thing and the code fires another,
  and nobody notices until the metric looks wrong months later.

## Stop Conditions

- The task is SYSTEM telemetry — service logs, metrics, traces, health
  checks, alert/dashboard config → route to `observability-operator`.
- The task is measuring which LIBRARY SKILLS fire in practice → route to
  `skill-usage-instrumenter` (a different object under strict
  minimization).
- The event schema/tracking plan doesn't exist or is inconsistent →
  route to `event-schema-architect` first; instrumenting undefined events
  bakes in the inconsistency.
- Required analytics would capture personal data without a clear consent
  basis, or before consent → halt and get the consent/PII posture from
  `pii-lifecycle-designer` and a human; do not instrument capture that
  violates the consent regime.

## Supporting Files

- [references/instrumentation-sheet.md](references/instrumentation-sheet.md)
  — the client-vs-server decision table, consent-gating checklist,
  de-duplication patterns, reliability techniques, and the tracking-QA
  workflow.
- `evals/evals.json` — behavior cases including the server-side accuracy
  decision, the consent-gating refusal, and the double-counting fix.
- `evals/trigger-evals.json` — the THREE-way discrimination against
  `observability-operator` (system telemetry) and `skill-usage-instrumenter`
  (library usage), plus `event-schema-architect` (schema vs firing).
