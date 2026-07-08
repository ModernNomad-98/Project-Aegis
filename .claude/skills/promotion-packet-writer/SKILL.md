---
name: promotion-packet-writer
description: Assemble a promotion case/packet for an engineer — evidence of impact ALREADY delivered, mapped to the target level's expectations. Inventory concrete accomplishments with measurable impact and scope of influence, map each to the leveling rubric's dimensions (scope, technical depth, leadership/influence, impact) so every dimension is covered, show the SUSTAINED pattern of operating at the level (not one heroic project), do an honest gap analysis against the target level, gather corroborating peer/manager evidence and artifacts, and write it in the committee's language (outcomes over activity). Use when preparing a promotion packet or self-assessment for leveling, or assessing readiness for the next level. Do NOT use to choose FUTURE high-leverage scope (staff-scope-selector), write one task/PR's closeout (ai-closeout-reporter), or carry evidence across stages of one effort (phased-work-handoff-designer).
---

# Promotion Packet Writer

## Purpose

Strong engineers lose promotion cycles to weak PACKETS: a list of
activities instead of impact, one impressive project instead of a
sustained pattern, coverage of the technical dimension but silence on
influence, and no corroborating evidence a committee that doesn't know
the person can trust. This skill assembles the case properly — concrete
accomplishments with measurable impact, mapped to every dimension the
target level's rubric requires, showing the person already operates AT
the level consistently, with an honest read of where the case is thin so
it's strengthened or delayed rather than sent up to fail. It documents
impact ALREADY delivered, in the committee's language. It does not choose
future scope, report a single task, or carry work across stages.

## Use When

- Use when: preparing a promotion packet, leveling case, or
  self-assessment for a target level.
- Use when: assessing whether an engineer is ready for the next level and
  where the evidence is strong vs thin.
- Use when: an engineer does level-appropriate work but their written case
  reads as activity, not impact.
- Do NOT use when: the task is choosing what high-leverage scope to work
  on NEXT — that is `staff-scope-selector` (future scope, not past
  evidence).
- Do NOT use when: the task is a single task/PR's closeout report — that
  is `ai-closeout-reporter`.
- Do NOT use when: the task is carrying decisions/evidence across STAGES
  of one effort for continuation — that is `phased-work-handoff-designer`.

## Inputs to Inspect

1. The target level and its rubric: the org's leveling expectations for
   the target level across scope, technical depth, leadership/influence,
   and impact — the criteria the case must satisfy.
2. The person's accomplishments: concrete work delivered over the review
   period, with outcomes and the scope of influence (self/team/org/
   company).
3. Measurable impact: metrics, before/after, and business/user outcomes
   attributable to the work — not just what was built.
4. Corroboration available: peer/manager/stakeholder testimony, artifacts
   (design docs, ADRs, dashboards), and cross-functional recognition.
5. The current draft (if any): whether it reads as activity vs impact and
   which rubric dimensions it under-covers.

## Workflow

1. **Anchor on the target level's rubric.** List the dimensions the target
   level requires (scope, technical, leadership/influence, impact). The
   packet's job is to show the person meets EACH — a case strong on one
   dimension and silent on another loses.
2. **Inventory accomplishments as impact, not activity.** For each,
   capture the outcome and its measurable impact and scope of influence.
   "Led the X migration" is activity; "led the X migration, cutting
   incident rate 40% and unblocking three teams" is impact.
3. **Map each accomplishment to rubric dimensions.** Show coverage across
   all dimensions; flag any dimension with thin evidence. This mapping is
   what turns a story into a case a committee can check.
4. **Demonstrate the sustained pattern.** Promotion is recognition that
   someone ALREADY operates at the level, consistently — not a reward for
   one heroic project. Show the pattern over time, across multiple pieces
   of work.
5. **Do an honest gap analysis.** Where is the case weak against the
   target level? Surface it — thin influence evidence, scope below the
   bar, missing corroboration. A packet sent up with hidden gaps wastes a
   cycle and damages credibility; naming gaps lets them be closed or the
   case timed better.
6. **Gather corroboration.** Attach peer/manager/stakeholder evidence and
   artifacts. A committee trusts corroborated impact over self-assertion.
7. **Write in the committee's language.** Frame in the rubric's terms,
   lead with outcomes, be concise and evidence-first. Cut activity that
   doesn't demonstrate a dimension.
8. **Deliver** the packet and the gap analysis in the Output Format —
   honestly, never inflating impact the evidence doesn't support.

The rubric-dimension map, the activity-to-impact rewrite guide, the
sustained-pattern test, and the gap-analysis format:
[references/promo-packet-sheet.md](references/promo-packet-sheet.md).

## Output Format

```
PROMOTION PACKET — <person> → <target level>
Rubric dimensions: scope · technical · leadership/influence · impact
Accomplishments (impact, not activity):
  <work> — outcome + MEASURABLE impact + scope of influence — maps to <dimension(s)>
Dimension coverage: <each dimension: strong | adequate | THIN>
Sustained pattern: <evidence the person already operates at the level, over time>
Corroboration:    <peer/manager/stakeholder evidence; artifacts>
GAP ANALYSIS:     <where the case is weak vs the target level — honest>
Recommendation:   ready | strengthen-then-submit | not-yet (with what's missing)
Boundaries:       future scope → staff-scope-selector; one task → ai-closeout-reporter;
                  cross-stage evidence → phased-work-handoff-designer
```

## Validation Checklist

- [ ] The target level's rubric dimensions are enumerated and the packet
      addresses EACH.
- [ ] Accomplishments are stated as impact (outcome + measurable effect +
      scope), not activity.
- [ ] Each accomplishment maps to rubric dimension(s); thin dimensions are
      flagged.
- [ ] A sustained pattern of operating at the level is demonstrated, not
      one project.
- [ ] An honest gap analysis names where the case is weak.
- [ ] Corroborating evidence and artifacts are gathered.
- [ ] Impact is not inflated beyond what the evidence supports.
- [ ] Future-scope, single-task, and cross-stage concerns are handed to
      their owning skills.

## Gotchas

- Activity is not impact. "Refactored the auth module" tells a committee
  nothing; "refactored auth, eliminating a class of outage and cutting
  onboarding time for new services in half" is a case. Rewrite every line
  to its outcome.
- One heroic project is not a promotion. Committees promote a sustained
  pattern of operating at the level; a single spike reads as a stretch,
  not the new baseline. Show the pattern.
- A packet strong on the technical dimension and silent on influence fails
  at levels where influence IS the level. Cover every dimension the rubric
  demands, or name the gap.
- Hiding a real gap doesn't close it — the committee finds it, and the
  credibility hit outlasts the cycle. Surface gaps and time or strengthen
  the case honestly.
- Uncorroborated self-assertion is discounted; the same claim with a
  peer's or stakeholder's confirmation lands. Gather the evidence.
- Inflating impact to fill a thin case is a short-term move with a
  long-term cost. Write the honest case; if it's not there yet, say what's
  missing.
- This documents PAST impact. If you're choosing what to work on next,
  that's `staff-scope-selector`.

## Stop Conditions

- The task is choosing future high-leverage scope → route to
  `staff-scope-selector`.
- The task is a single task/PR closeout, or carrying evidence across
  stages of one effort → route to `ai-closeout-reporter` or
  `phased-work-handoff-designer`.
- The gap analysis shows the person is not yet at the level → say so with
  what's missing; recommend strengthen-then-submit or not-yet rather than
  writing an inflated case that will fail.
- Impact claims can't be substantiated with evidence or corroboration →
  do not assert them; flag the missing evidence to gather rather than
  fabricating impact.

## Supporting Files

- [references/promo-packet-sheet.md](references/promo-packet-sheet.md) —
  the rubric-dimension map, the activity-to-impact rewrite guide, the
  sustained-pattern test, and the gap-analysis format.
- `evals/evals.json` — behavior cases including the activity-to-impact
  rewrite, the dimension-coverage check, and the honest not-yet gap.
- `evals/trigger-evals.json` — discrimination against `staff-scope-selector`
  (future scope vs past impact), `ai-closeout-reporter` (one task), and
  `phased-work-handoff-designer` (cross-stage evidence).
