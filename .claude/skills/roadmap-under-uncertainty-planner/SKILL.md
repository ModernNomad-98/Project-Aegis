---
name: roadmap-under-uncertainty-planner
description: Plan a product roadmap when the future is genuinely uncertain — organize by horizon (now/next/later, or committed/planned/exploratory) instead of a false-precision Gantt of dated features, let confidence decay with distance, sequence by dependency AND by learning (retire the most uncertainty first), frame around outcomes/themes not a feature checklist, reconcile ambition against real capacity with slack, and communicate without over-promising. Produces a horizon-based roadmap with confidence levels, an uncertainty-reduction sequence, and a re-planning cadence. Consumes a prioritization (the ranking of WHAT) from prioritization-frame-picker; owns sequencing and communication over TIME. Use when building or resetting a roadmap, planning under shifting priorities, or when a dated roadmap keeps being wrong. Do NOT use to pick/apply a prioritization framework (prioritization-frame-picker), write one feature's spec (product-spec-writer), or plan one feature's flag rollout (feature-flag-rollout-strategist).
---

# Roadmap Under Uncertainty Planner

## Purpose

The classic roadmap is a lie told in good faith: a tidy Gantt chart of
dated features stretching four quarters out, every bar precise, none of
it true past the first month. Reality delivers changed priorities, a
discovery that reshapes the plan, and a dependency that slips — and the
dated chart becomes a stick to beat the team with. This skill plans the
roadmap for that reality: horizons instead of dates, confidence that
honestly decays with distance, sequencing that front-loads the work
which RETIRES uncertainty, outcomes and themes rather than a feature
checklist, capacity reconciled with slack for the unknown, and a
re-planning cadence baked in. It owns sequencing and communication over
TIME; it consumes the ranking of WHAT to do from
`prioritization-frame-picker`.

## Use When

- Use when: building, resetting, or communicating a product roadmap,
  especially one spanning multiple quarters of genuine uncertainty.
- Use when: a dated roadmap keeps being wrong and getting used as a
  contract, and you need horizons and confidence instead.
- Use when: priorities shift often and the plan needs to sequence for
  learning (do the uncertainty-reducing bets first) rather than for a
  fixed order.
- Use when: ambition exceeds capacity and the roadmap must show the
  trade-off honestly instead of promising everything.
- Do NOT use when: the task is to RANK or score the backlog items — pick
  and apply a prioritization framework — that is
  `prioritization-frame-picker`; this skill consumes that ranking.
- Do NOT use when: the task is one feature's specification (problem,
  scope, acceptance criteria) — that is `product-spec-writer`.
- Do NOT use when: the task is one feature's flag-gated rollout plan
  (progressive %s, guardrails) — that is `feature-flag-rollout-strategist`;
  a roadmap sequences features, it doesn't roll one out.

## Inputs to Inspect

1. The strategic goals/outcomes the roadmap must serve — what the
   business is trying to achieve, not just a wish list of features.
2. The prioritized backlog (from `prioritization-frame-picker` if
   present): the ranking of candidate work and the assumptions behind it.
3. Real capacity: team size, velocity evidence, and how much is already
   committed to maintenance/support/reliability (rarely zero).
4. Dependencies and sequencing constraints: what must precede what,
   cross-team hand-offs, and external deadlines that are genuinely fixed.
5. The biggest unknowns: the assumptions whose being wrong would most
   change the plan — the candidates for uncertainty-reducing bets.

## Workflow

1. **Anchor on outcomes, not features.** Restate the roadmap's purpose as
   the outcomes it should produce. Each candidate becomes a hypothesized
   path to an outcome, not a guaranteed deliverable — this reframing is
   what lets the plan flex without "failing".
2. **Choose the horizon model.** now/next/later or committed/planned/
   exploratory. Assign granularity per horizon: near-term items are
   specific and confident; far-term items are themes and directions, not
   dated features. State the model so readers calibrate.
3. **Let confidence decay with distance.** Near horizon: high confidence,
   specific, possibly date-ranged. Middle: directional, quarter-grained.
   Far: thematic, explicitly "we intend to explore". Never attach a
   precise date to a low-confidence item — that's the false precision
   that makes roadmaps wrong.
4. **Sequence by dependency AND by learning.** Beyond "what unblocks
   what", identify the bets whose outcome would most reshape the plan and
   front-load cheap uncertainty-reducers (spikes, prototypes,
   experiments) so later commitments rest on evidence, not hope.
5. **Reconcile with capacity honestly.** Do not fill 100% — reserve slack
   for the unknown, interrupts, and maintenance. If ambition exceeds
   capacity, show the trade-off (what moves to a later horizon) rather
   than compressing everything into a fantasy.
6. **Build in re-planning.** State the cadence at which the roadmap is
   revisited, what events trigger an off-cadence re-plan, and how changes
   are communicated. A roadmap without a re-plan rhythm silently becomes
   a stale promise.
7. **Communicate without over-promising.** Label each item's confidence
   and horizon; distinguish committed from directional from exploratory;
   avoid presenting the whole thing as a dated contract. State the
   assumptions the plan rests on so a changed assumption visibly changes
   the plan.
8. **Deliver** the horizon roadmap in the Output Format, with confidence,
   the uncertainty-reduction sequence, and the re-plan cadence explicit.

Horizon models, the confidence-labeling scheme, and the outcome-vs-
feature reframing patterns:
[references/roadmap-uncertainty-sheet.md](references/roadmap-uncertainty-sheet.md).

## Output Format

```
ROADMAP (uncertainty-aware) — <product/team>, horizon model=<now/next/later | ...>
Outcomes:      <the outcomes this roadmap serves>
Now (committed):    <specific items, high confidence, date-range if any>
Next (planned):     <directional, quarter-grained, medium confidence>
Later (exploratory):<themes/directions, low confidence, "intend to explore">
Per item:      outcome=<...> confidence=<high|med|low> depends-on=<...>
Uncertainty bets: <cheap experiments/spikes front-loaded to retire the biggest unknowns>
Capacity:      <committed vs slack vs maintenance; trade-offs if over capacity>
Assumptions:   <what the plan rests on — changing these changes the plan>
Re-plan:       <cadence + off-cadence triggers + how changes are communicated>
Boundaries:    ranking → prioritization-frame-picker; one spec → product-spec-writer;
               one rollout → feature-flag-rollout-strategist
```

## Validation Checklist

- [ ] The roadmap is organized by horizon, not as a dated Gantt of
      features across all quarters.
- [ ] Items tie to outcomes; far-horizon entries are themes/directions,
      not dated features.
- [ ] Confidence is labeled per item and decays with distance; no precise
      date sits on a low-confidence item.
- [ ] Sequencing front-loads uncertainty-reducing bets, not just
      dependency order.
- [ ] Capacity includes slack and maintenance; over-ambition is shown as
      a trade-off, not compressed away.
- [ ] A re-planning cadence and its triggers are stated.
- [ ] The plan's load-bearing assumptions are explicit.
- [ ] Ranking, single-spec, and single-rollout concerns are handed to
      their owning skills.

## Gotchas

- A dated four-quarter Gantt reads as a commitment no matter how many
  "subject to change" disclaimers surround it. If you don't want it
  treated as a contract, don't draw it as one — use horizons.
- Precision and confidence are different axes; the failure is attaching
  high precision (an exact date) to low confidence (a far-out idea).
  Match the grain to the certainty.
- Sequencing purely by dependency ignores the cheapest wins: a two-day
  spike that could invalidate a quarter of planned work should come
  first. Sequence to learn, not just to unblock.
- A roadmap filled to 100% capacity has no room for the interrupts,
  bugs, and discoveries that always come — it's over by definition.
  Slack is a feature.
- Outcome-free roadmaps ("ship features A–H") can't absorb change: when
  A turns out not to matter, the plan has no way to say so. Tie work to
  outcomes so a dead hypothesis can be dropped without the plan
  "failing".
- No re-plan cadence means the roadmap is only honest on the day it's
  published; by the next sprint it's fiction nobody updated.
- A roadmap is not a stack rank and not a spec. If you're scoring items
  or detailing one feature's requirements, you've stepped into another
  skill's job.

## Stop Conditions

- The task is actually to RANK/score the backlog (choose RICE vs
  value/effort, apply it) → route to `prioritization-frame-picker`; this
  skill sequences an already-prioritized set.
- The task is one feature's spec or one feature's rollout → route to
  `product-spec-writer` or `feature-flag-rollout-strategist`
  respectively.
- A "fixed" external deadline is presented as immovable but the scope to
  hit it is undefined → surface the scope-vs-date trade-off for a human
  decision rather than encoding a date the plan can't support.
- Leadership demands precise dates across all horizons as commitments →
  flag the false-precision risk and offer the confidence-labeled
  alternative; do not manufacture certainty the evidence doesn't
  support.

## Supporting Files

- [references/roadmap-uncertainty-sheet.md](references/roadmap-uncertainty-sheet.md)
  — horizon models, the confidence-labeling scheme, uncertainty-bet
  patterns, and the outcome-vs-feature reframing guide.
- `evals/evals.json` — behavior cases including the dated-Gantt reset,
  learning-first sequencing, and the false-precision refusal.
- `evals/trigger-evals.json` — discrimination against `prioritization-frame-picker`
  (rank vs sequence), `product-spec-writer`, and `feature-flag-rollout-strategist`.
