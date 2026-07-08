---
name: design-review-facilitator
description: Facilitate a technical DESIGN REVIEW — prepare it (circulate the design/spec ahead, state the decision the review must reach, invite the right reviewers including the skeptics and cross-cutting owners), structure the discussion (surface assumptions, probe the risky parts and cross-cutting concerns, weigh alternatives, keep it about the design not the person), actively elicit dissent and the strongest objection, drive to an EXPLICIT outcome (approved / approved-with-changes / needs-rework / blocked-on-X), and capture decisions and action items with owners — while avoiding rubber-stamp, bikeshedding, HiPPO-domination, and no-decision. Facilitates review of a design (often a tech-spec-writer doc); does not write it or make the decision. Use when running or improving a design review, RFC review, or architecture review. Do NOT use to WRITE the design doc (tech-spec-writer), review CODE/a diff (code-reviewer), or facilitate REQUIREMENTS elicitation (requirements-gathering-facilitator).
---

# Design Review Facilitator

## Purpose

A design review fails in one of four familiar ways: the rubber stamp (no
real scrutiny, approved because the author is senior), the bikeshed (an
hour on the button color while the data-loss risk goes unmentioned), the
HiPPO (the highest-paid opinion ends the discussion), and the no-decision
(a great conversation that decides nothing and reconvenes forever). This
skill facilitates the review so it actually does its job: the right
people pre-read the design, the discussion targets the assumptions and
risks that matter, dissent is actively drawn out, and the meeting ends
with an EXPLICIT outcome and captured decisions and owners. It
facilitates the review of a design — usually a `tech-spec-writer` doc; it
does not write the design or make the decision, though it drives the
group to one and hands the record to `adr-writer`.

## Use When

- Use when: running or improving a design review, RFC review, or
  architecture review meeting/process.
- Use when: design reviews at your org rubber-stamp, bikeshed, get
  dominated by the loudest voice, or end without a decision.
- Use when: a design needs structured scrutiny and an explicit approve/
  rework outcome before build.
- Use when: preparing a review — what to circulate, whom to invite, what
  decision it must reach.
- Do NOT use when: the task is WRITING the design doc/spec being reviewed
  — that is `tech-spec-writer`.
- Do NOT use when: the task is reviewing CODE or a diff (correctness,
  bugs, style) — that is `code-reviewer` / the PR-review skills; a design
  review is upstream of code.
- Do NOT use when: the task is facilitating REQUIREMENTS elicitation
  (what to build, from stakeholders) — that is
  `requirements-gathering-facilitator`; this facilitates review of a
  technical design.

## Inputs to Inspect

1. The design under review: the tech spec / RFC / design doc, and whether
   it's complete enough to review (problem, proposal, alternatives,
   cross-cutting).
2. The decision the review must reach: what "approved" means here and what
   the alternatives on the table are.
3. The reviewers: who should be in the room — domain owners, the
   skeptics, and the cross-cutting owners (security, data, ops) — and
   whether they've pre-read.
4. The stakes and reversibility: how costly the decision is to reverse,
   which sets how much scrutiny it warrants.
5. Past review dysfunction: whether this team rubber-stamps, bikesheds, or
   never decides — so the facilitation counters it.

## Workflow

1. **Prepare the review.** Circulate the design ahead with a required
   pre-read; state the review's PURPOSE and the decision it must reach;
   invite the right people — including the skeptics and the cross-cutting
   owners, not just allies. A review with no pre-read becomes a live
   reading, and quality collapses.
2. **Frame the decision at the start.** Name what's being decided, the
   options, and the bar for approval. The room should know from minute one
   whether it's here to approve a direction, choose between options, or
   pressure-test risks.
3. **Structure the discussion by importance.** Walk the design; spend time
   on the assumptions, the risky parts, and the cross-cutting concerns —
   not the trivia. Actively steer away from bikeshedding toward the
   decisions that matter and are expensive to reverse.
4. **Elicit dissent deliberately.** Ask for the strongest objection;
   invite the quietest domain expert; make disagreement safe and separate
   critique of the design from the author. The objection nobody voiced is
   the incident you'll have later.
5. **Counter the HiPPO.** Surface reasoning, not rank: ask "what's the
   argument?" not "what does the senior person think?". The best available
   argument decides, not the highest-paid opinion.
6. **Drive to an explicit outcome.** Approved / approved-with-changes
   (list them) / needs-rework (with what) / blocked-on-X (named). "Let's
   circle back" with no decision and no next step is the failure mode;
   force a concrete outcome or a concrete blocker.
7. **Capture decisions and actions.** Record the decisions (hand binding
   ones to `adr-writer`), the action items with owners and dates, and the
   open questions. A review whose outcome isn't written down didn't
   happen.
8. **Deliver** the review outcome record in the Output Format.

The review-preparation checklist, the anti-pattern countermeasures
(rubber-stamp/bikeshed/HiPPO/no-decision), and the outcome taxonomy:
[references/design-review-sheet.md](references/design-review-sheet.md).

## Output Format

```
DESIGN REVIEW OUTCOME — <design/effort>
Purpose:       <what this review had to decide>
Pre-read:      <design circulated? reviewers present + roles (skeptics, cross-cutting owners)>
Discussion:    <key assumptions probed; risks + cross-cutting concerns raised; alternatives weighed>
Dissent:       <strongest objections surfaced + how addressed>
OUTCOME:       approved | approved-with-changes (list) | needs-rework (what) | blocked-on-X
Decisions:     <decisions reached> (binding ones → adr-writer)
Action items:  <item — owner — date>
Open questions:<remaining, with owners>
Boundaries:    write the design → tech-spec-writer; code review → code-reviewer;
               requirements → requirements-gathering-facilitator
```

## Validation Checklist

- [ ] The design was circulated with a required pre-read; the right
      reviewers (incl. skeptics + cross-cutting owners) were present.
- [ ] The decision the review must reach was framed at the start.
- [ ] Discussion targeted assumptions, risks, and cross-cutting concerns —
      not bikeshed trivia.
- [ ] The strongest objection was actively elicited; dissent was safe and
      about the design, not the author.
- [ ] Reasoning decided, not rank (HiPPO countered).
- [ ] The review ended with an EXPLICIT outcome, not "circle back".
- [ ] Decisions (→ `adr-writer`), action items with owners/dates, and open
      questions were captured.
- [ ] Writing the design, code review, and requirements were not done here.

## Gotchas

- A review with no pre-read is a live reading of the doc — the scrutiny
  budget is spent parsing, and nothing gets pressure-tested. Require the
  pre-read or postpone.
- Bikeshedding is comfort behavior: people argue the trivial because it's
  safe and the hard parts are hard. The facilitator's job is to spend the
  time where reversal is expensive.
- The most dangerous review is the silent one — everyone nods, the one
  person who saw the flaw didn't feel safe saying it, and it ships.
  Eliciting the strongest objection is not optional.
- "What does the staff engineer think?" ends thought; "what's the
  argument for that?" continues it. Decide on reasoning, not rank.
- A review that ends without an explicit outcome has wasted everyone's
  time and will reconvene identically. Force approved / changes / rework /
  blocked — always one of them.
- Decisions not written down are decisions re-litigated next week. Capture
  them and route the binding ones to an ADR.
- Facilitating the review is not writing the design or making the call.
  If you find yourself authoring the spec or deciding the architecture,
  that's `tech-spec-writer` / `architecture-designer`.

## Stop Conditions

- The task is writing the design doc/spec → route to `tech-spec-writer`.
- The task is reviewing code/a diff → route to `code-reviewer` / the
  PR-review skills.
- The task is facilitating requirements elicitation → route to
  `requirements-gathering-facilitator`.
- The design under review is too incomplete to review meaningfully (no
  proposal, no alternatives, no cross-cutting) → send it back to
  `tech-spec-writer` rather than running a review that can only bikeshed.

## Supporting Files

- [references/design-review-sheet.md](references/design-review-sheet.md) —
  the preparation checklist, the anti-pattern countermeasures, the outcome
  taxonomy, and facilitation prompts for eliciting dissent.
- `evals/evals.json` — behavior cases including anti-bikeshed steering,
  dissent elicitation, and forcing an explicit outcome.
- `evals/trigger-evals.json` — discrimination against `tech-spec-writer`
  (write vs review), `code-reviewer` (code vs design), and
  `requirements-gathering-facilitator` (requirements vs design review).
