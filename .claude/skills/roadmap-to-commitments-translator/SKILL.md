---
name: roadmap-to-commitments-translator
description: Translate a directional, uncertainty-aware roadmap into what a team can actually COMMIT to — the binding delivery promises stakeholders will hold you to. Separate commit-able (high-confidence, capacity-backed, dependency-clear) from aspirational, ground commitments in real capacity (velocity evidence minus maintenance/interrupts, with a buffer), fold in cross-team dependencies and risk, translate outcomes into concrete deliverables with honest date RANGES, and manage the gap explicitly (what's NOT committed, and why). The inverse of roadmap-under-uncertainty-planner, which keeps the roadmap honestly uncertain. Use when converting a roadmap into commitments, quarterly planning, or when stakeholders treat the whole roadmap as a promise. Do NOT use to build/sequence the roadmap itself (roadmap-under-uncertainty-planner), negotiate specific cross-team dependencies (cross-team-dependency-negotiator), or rank the backlog (prioritization-frame-picker).
---

# Roadmap to Commitments Translator

## Purpose

A roadmap is a set of bets; a commitment is a promise. The damage comes
from confusing them — presenting the whole directional roadmap to
stakeholders, who hear every item as a dated guarantee, and then missing
"commitments" the team never actually made. This skill translates the
roadmap into the subset the team can genuinely commit to: the
high-confidence, capacity-backed, dependency-clear items become firm
deliverables with honest date ranges, and everything else stays
explicitly directional. It grounds commitments in real velocity (not
aspiration), folds in dependencies and risk, and manages the gap out
loud so nobody mistakes a bet for a promise. It is the inverse of
`roadmap-under-uncertainty-planner`, which keeps the roadmap honestly
uncertain; this extracts the firm-promise slice from it.

## Use When

- Use when: converting a roadmap into delivery commitments for
  stakeholders (quarterly/OKR planning, a commitment review).
- Use when: stakeholders treat the entire roadmap as a set of promises and
  the committed subset needs separating out.
- Use when: deciding what a team can firmly commit to given real capacity,
  dependencies, and risk.
- Use when: under pressure to commit to more than capacity supports and
  the tradeoff must be made explicit.
- Do NOT use when: the task is BUILDING or sequencing the roadmap itself
  (horizons, confidence, learning-first order) — that is
  `roadmap-under-uncertainty-planner`; this consumes its output.
- Do NOT use when: the task is negotiating a SPECIFIC cross-team
  dependency (deliverable, date, owner) — that is
  `cross-team-dependency-negotiator` (an input here).
- Do NOT use when: the task is RANKING the backlog — that is
  `prioritization-frame-picker`.

## Inputs to Inspect

1. The roadmap (from `roadmap-under-uncertainty-planner` if present): the
   items, their horizons, and their stated confidence.
2. Real capacity evidence: velocity/throughput history, team size, and the
   maintenance/support/interrupt load that isn't available for new work.
3. Dependencies: cross-team dependencies (from
   `cross-team-dependency-negotiator`) and technical unknowns that gate or
   endanger delivery.
4. The stakeholders and the ask: who needs commitments, for what horizon,
   and what "committed" will mean to them (a promise they'll hold you to).
5. Prior commitment accuracy: how past commitments landed — chronic
   over-commitment is a signal to buffer harder.

## Workflow

1. **Separate commit-able from aspirational.** Only items that are
   high-confidence, capacity-backed, AND dependency-clear become
   commitments. Everything else stays directional. This split is the whole
   job; blurring it is how roadmaps become broken promises.
2. **Ground in real capacity.** Base commitments on velocity EVIDENCE, not
   the aspirational sprint. Subtract maintenance, support, and interrupt
   load — the capacity actually available for committed work is always
   less than headcount suggests. Leave a risk buffer.
3. **Fold in dependencies and risk.** A commitment that depends on another
   team's uncommitted deliverable isn't a commitment — route the
   dependency to `cross-team-dependency-negotiator` and only commit once
   it's secured (or de-risked). Technical unknowns either get a buffer or
   keep the item aspirational.
4. **Translate outcomes to concrete deliverables.** Roadmap themes/
   outcomes become specific deliverables the team can be held to, with
   honest date RANGES (not false-precise single dates). "Improve
   onboarding" is a theme; "ship the new onboarding flow, weeks 6–8" is a
   commitment.
5. **Manage the gap out loud.** State explicitly what's on the roadmap but
   NOT committed, and why (capacity, dependency, uncertainty). The
   unstated gap is where stakeholders invent promises you never made.
6. **Refuse over-commitment; surface the tradeoff.** When asked to commit
   beyond capacity, don't quietly pad estimates until it "fits" — present
   the tradeoff: commit to less, add capacity, or explicitly accept lower
   confidence. A padded commitment is a lie with a schedule.
7. **Deliver** the commitment set and the explicitly-not-committed set in
   the Output Format, with the capacity basis and dependencies shown.

The commit-able criteria, the capacity-math worksheet, the outcome-to-
deliverable translation, and the gap-communication format:
[references/commitments-sheet.md](references/commitments-sheet.md).

## Output Format

```
ROADMAP → COMMITMENTS — <team/horizon>
Capacity basis: velocity evidence; minus maintenance/interrupts; buffer   (not aspiration)
Committed:      <deliverable — date RANGE — capacity-backed, dependency-clear, high-confidence>
Dependencies:  <what each commitment needs> → cross-team-dependency-negotiator (secured?)
NOT committed (directional): <roadmap items excluded — and WHY (capacity/dependency/uncertainty)>
Over-commit tradeoff: <if asked for more: commit-less | add-capacity | accept-lower-confidence>
Boundaries:    build the roadmap → roadmap-under-uncertainty-planner; specific dep →
               cross-team-dependency-negotiator; ranking → prioritization-frame-picker
```

## Validation Checklist

- [ ] Commit-able items are separated from aspirational by confidence,
      capacity, AND dependency-clarity.
- [ ] Commitments are grounded in velocity evidence minus maintenance/
      interrupts, with a buffer — not aspiration.
- [ ] Dependencies are folded in; commitments gated on uncommitted
      external work are not treated as firm.
- [ ] Outcomes are translated into concrete deliverables with honest date
      RANGES, not false-precise dates.
- [ ] The not-committed gap is stated explicitly with reasons.
- [ ] Over-commitment pressure is met with an explicit tradeoff, not
      padded estimates.
- [ ] Roadmap-building, dependency-negotiation, and ranking are handed to
      their owning skills.

## Gotchas

- The whole roadmap presented as commitments is a promise machine: every
  directional bet gets heard as a dated guarantee. The committed subset
  must be visibly, explicitly smaller than the roadmap.
- Committing on aspirational velocity ("if everything goes right") is
  committing to the best case as if it's the expected case. Use the
  evidence, and subtract the work that always eats capacity.
- A commitment resting on another team's uncommitted deliverable is
  borrowed confidence. It's not committed until that dependency is
  secured.
- Padding estimates until an over-ask "fits" hides the over-commitment
  instead of resolving it — and the miss surfaces later, worse. Surface
  the tradeoff at planning, not at the deadline.
- False-precise dates ("March 14") on multi-week uncertain work invite the
  miss; ranges ("weeks 6–8") commit honestly to what's knowable.
- The silent gap between roadmap and commitments is where stakeholders
  invent promises. Naming what's NOT committed, and why, is as important
  as naming what is.
- Extracting commitments is not building the roadmap. If you're
  sequencing horizons and setting confidence, that's
  `roadmap-under-uncertainty-planner`.

## Stop Conditions

- The task is building/sequencing the roadmap itself → route to
  `roadmap-under-uncertainty-planner`.
- The task is negotiating a specific cross-team dependency → route to
  `cross-team-dependency-negotiator`.
- The task is ranking the backlog → route to `prioritization-frame-picker`.
- Leadership demands commitment to more than capacity supports and won't
  accept the tradeoff → surface the over-commitment risk explicitly and
  escalate the decision; do not manufacture a commitment by padding or
  by committing the best case.

## Supporting Files

- [references/commitments-sheet.md](references/commitments-sheet.md) — the
  commit-able criteria, the capacity-math worksheet, the outcome-to-
  deliverable translation, and the gap-communication format.
- `evals/evals.json` — behavior cases including the commit-able split, the
  capacity-grounding, and the over-commitment refusal.
- `evals/trigger-evals.json` — discrimination against `roadmap-under-uncertainty-planner`
  (build vs extract), `cross-team-dependency-negotiator`, and
  `prioritization-frame-picker`.
