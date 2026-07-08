---
name: prioritization-frame-picker
description: Pick and apply the RIGHT prioritization framework for a decision instead of defaulting to one — match the situation to a frame (RICE, WSJF/cost-of-delay, value-vs-effort/ICE, Kano, opportunity scoring, MoSCoW), surface the inputs each frame needs and how reliable they are, guard against false rigor (a precise RICE score built from guessed numbers), handle must-do and incomparable items OUTSIDE the score, and produce a ranked list with the frame's assumptions and sensitivity made explicit. Owns the RANKING method and its honest application; sequencing the ranked set over time is roadmap-under-uncertainty-planner's. Use when a backlog needs ranking, when stakeholders argue about priority, when a scoring model is being gamed or over-trusted, or when choosing a prioritization method. Do NOT use to sequence/communicate a roadmap over horizons (roadmap-under-uncertainty-planner), to spec one feature (product-spec-writer), or to elicit the underlying requirements (requirements-gathering-facilitator).
---

# Prioritization Frame Picker

## Purpose

Every team has a prioritization framework and most use the wrong one for
the decision in front of them — RICE-scoring a list of legal-compliance
must-dos, or eyeballing value-vs-effort for a portfolio where timing
dominates. Worse, the framework's numeric output gets treated as truth:
a RICE score of 42.7 built from three guesses and a made-up reach figure
outranks a strategic bet because the bet "didn't score well". This skill
picks the frame that fits the decision, names the inputs it needs and
how reliable they are, guards against the false rigor of precise scores
on soft data, pulls must-do and incomparable items out of the formula
where they belong, and produces a ranked list whose assumptions and
sensitivity are on the table. It owns the RANKING; sequencing the ranked
set over horizons is `roadmap-under-uncertainty-planner`'s.

## Use When

- Use when: a backlog or set of initiatives needs ranking and there's no
  agreed method, or the current one doesn't fit.
- Use when: stakeholders argue about priority and a shared, explicit
  frame would move the conversation from opinion to assumptions.
- Use when: an existing scoring model is being gamed, or its numbers are
  trusted far beyond the quality of their inputs.
- Use when: choosing which prioritization framework to adopt for a team
  or a specific decision.
- Do NOT use when: the items are already ranked and the task is to
  sequence/communicate them over time — that is
  `roadmap-under-uncertainty-planner`.
- Do NOT use when: the task is detailing ONE chosen item (problem, scope,
  acceptance criteria) — that is `product-spec-writer`.
- Do NOT use when: the real gap is not knowing what's needed or valuable
  yet — elicit first with `requirements-gathering-facilitator`;
  prioritizing unknowns produces confident nonsense.

## Inputs to Inspect

1. What's being prioritized: comparable features, a mixed portfolio,
   bugs, experiments, or whole initiatives — the object determines the
   frame.
2. The goal the ranking serves: growth, retention, revenue, risk
   reduction, flow/throughput — the frame's "value" must mean this.
3. The available inputs and their quality: is there real reach/usage data
   or are impact and reach guesses? Which numbers are evidence vs
   fiction?
4. Time sensitivity: whether cost-of-delay/timing dominates (favoring
   WSJF) or value/effort is roughly time-stable.
5. The non-negotiables: compliance, security, keep-the-lights-on, and
   contractual must-dos that shouldn't be forced through a value formula.

## Workflow

1. **Frame the decision before the framework.** State what's being
   ranked, toward what outcome, with what input quality and time horizon.
   The wrong frame applied rigorously is worse than the right frame
   applied roughly.
2. **Select the frame to fit.** Match, don't default: RICE for many
   comparable features where reach matters; WSJF / cost-of-delay when
   timing and flow dominate; value-vs-effort or ICE for a fast, coarse
   cut; Kano to classify basic vs performance vs delighter; opportunity
   scoring for importance-vs-satisfaction gaps; MoSCoW for release
   scoping. Name the chosen frame's fit AND its limits.
3. **Expose the inputs and their reliability.** List each input the frame
   needs and mark it evidence or guess. Use the confidence factor (RICE's
   confidence, or an explicit discount) to deflate scores built on
   guesses — that is what it's for.
4. **Refuse false rigor.** Score in ranges or buckets (t-shirt sizes),
   not false decimals; run a sensitivity check (does the ranking hold if
   a soft input is off by 2×?). If the order flips on a guess, the
   ranking is a coin flip wearing a spreadsheet.
5. **Handle items the formula can't.** Pull must-dos (compliance,
   security, reliability) into a protected lane rather than letting a low
   value score bury them. Flag strategic bets that score poorly but
   matter, and genuinely incomparable items, for explicit human judgment
   — the frame informs, it doesn't overrule.
6. **Produce the ranking honestly.** The ordered list, the inputs and
   their quality, the confidence, the sensitivity result, and the items
   handled outside the frame. Make the assumptions visible so the
   argument is about them, not about the number.
7. **Hand off.** State that sequencing the ranked set over horizons —
   with dependencies, capacity, and re-planning — is
   `roadmap-under-uncertainty-planner`'s job.

Framework selection guide, input-reliability discipline, and the
sensitivity-check method:
[references/prioritization-frames-sheet.md](references/prioritization-frames-sheet.md).

## Output Format

```
PRIORITIZATION — <what's being ranked>, toward <outcome>
Frame:        <RICE | WSJF | value/effort | ICE | Kano | opportunity | MoSCoW> — why it fits; limits
Inputs:       <inputs the frame needs, each marked [evidence] | [guess]>
Ranking:      <ordered list with scores in ranges/buckets, not false decimals>
Confidence:   <how much the input quality supports the order>
Sensitivity:  <does the order hold if a soft input is off 2×? which pairs flip?>
Outside the frame:
  Must-do lane: <compliance/security/keep-lights-on — protected, not value-scored>
  Strategic/incomparable: <flagged for human judgment>
Handoff:      sequencing over time → roadmap-under-uncertainty-planner
```

## Validation Checklist

- [ ] The decision is framed (object, outcome, input quality, time
      horizon) before a framework is chosen.
- [ ] The framework is matched to the situation with its fit AND limits
      stated — not defaulted.
- [ ] Every input is marked evidence or guess; guesses discount the
      score via a confidence factor.
- [ ] Scores are ranges/buckets, not false decimals; a sensitivity check
      is run and flips are reported.
- [ ] Must-dos are in a protected lane; strategic/incomparable items are
      flagged for human judgment, not buried by the formula.
- [ ] The ranking's assumptions are explicit so debate targets them, not
      the number.
- [ ] Sequencing over time is handed to `roadmap-under-uncertainty-planner`.

## Gotchas

- A precise score launders guesses into authority: 42.7 looks earned even
  when reach and impact were invented. Round to buckets so the precision
  matches the evidence.
- Defaulting to RICE (or whatever the org uses) for every decision
  mis-ranks whole classes of work — timing-dominated portfolios,
  must-dos, delighters. The frame is a choice, not a habit.
- The confidence factor exists precisely to punish confident guessing;
  teams that set it to 100% on everything have removed the one honest
  part of RICE.
- Forcing compliance and security must-dos through a value formula either
  games the inputs to make them "win" or buries genuinely required work.
  Put them in a lane above the score.
- A strategic bet that scores badly is often the point of the strategy —
  the formula optimizes for the measurable, and the measurable is
  short-term. Keep human judgment above the number for those.
- If the ranking flips when one soft input moves within its plausible
  range, you don't have a ranking — you have noise. Report that instead
  of a false order.
- Prioritizing before requirements are understood ranks fantasies. If the
  value of items is unknown, elicit first.

## Stop Conditions

- The items are already ranked and the task is to sequence/communicate
  them over time → route to `roadmap-under-uncertainty-planner`.
- The value/need of the items is genuinely unknown (no requirements yet)
  → route to `requirements-gathering-facilitator` first; ranking unknowns
  is confident nonsense.
- Stakeholders demand a single definitive number to end the debate when
  the inputs are guesses → surface the sensitivity and the assumptions,
  and route the real trade-off to a human decision rather than
  manufacturing a decisive score.
- A must-do (legal/security) is being value-scored to justify de-
  prioritizing it → halt and move it to the protected lane; do not
  produce a ranking that buries required work.

## Supporting Files

- [references/prioritization-frames-sheet.md](references/prioritization-frames-sheet.md)
  — the framework selection guide (fit/inputs/limits per frame), the
  input-reliability discipline, and the sensitivity-check method.
- `evals/evals.json` — behavior cases including frame selection, the
  false-rigor refusal, and the must-do-lane handling.
- `evals/trigger-evals.json` — discrimination against `roadmap-under-uncertainty-planner`
  (rank vs sequence), `product-spec-writer`, and `requirements-gathering-facilitator`.
