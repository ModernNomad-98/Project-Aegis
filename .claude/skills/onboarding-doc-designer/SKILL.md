---
name: onboarding-doc-designer
description: Design ONBOARDING documentation for someone JOINING a team/codebase — the first-day and first-week path, verified environment setup, an architecture/orientation tour (the mental model, not every detail), how-we-work (processes, tools, comms, rituals), key concepts and a glossary, a who-owns-what/who-to-ask map, a real first-task that produces an early win, and a plan to keep onboarding current (the docs that rot fastest). Audience is a new joiner ramping to productivity, not an external contributor or a README's evaluator. Use when designing onboarding for new hires/team members, when new joiners take too long to become productive, or when onboarding knowledge lives only in people's heads. Do NOT use to write the external CONTRIBUTING guide (contribution-guide-author), the README (readme-craftsman), or organize the whole docs corpus by type (diataxis-doc-organizer).
---

# Onboarding Doc Designer

## Purpose

A new engineer's first weeks are mostly spent reconstructing what the
team already knows: which repo, how to get it running, what the pieces
are called, who to ask, and how work actually flows here. When that
knowledge lives only in people's heads, every hire re-derives it by
interrupting others, and "ramp time" stretches for months. This skill
designs onboarding documentation that shortens the ramp — a first-day and
first-week path, verified setup, an architecture orientation that gives
the mental model without drowning the joiner in detail, the real
how-we-work, a concepts glossary, a who-to-ask map, and a first task that
produces an early win. Its audience is someone JOINING and becoming
productive — not an external contributor and not a README's evaluator —
and it's designed to stay current, because onboarding docs rot fastest.

## Use When

- Use when: designing onboarding docs for new hires or team members
  joining a codebase/team.
- Use when: new joiners take too long to become productive, or keep
  asking the same questions because the answers aren't written down.
- Use when: onboarding knowledge lives only in senior people's heads and
  needs capturing.
- Use when: a team is growing and ad-hoc onboarding no longer scales.
- Do NOT use when: the audience is an EXTERNAL contributor to an open/
  inner-source project (fork, PR, contribution process) — that is
  `contribution-guide-author`; different audience and journey.
- Do NOT use when: the task is the README front door for evaluators/users
  — that is `readme-craftsman`.
- Do NOT use when: the task is classifying the whole docs corpus by mode
  (tutorials/how-to/reference/explanation) — that is
  `diataxis-doc-organizer`; onboarding is an audience-defined journey that
  DRAWS ON those docs.

## Inputs to Inspect

1. The joiner and the ramp goal: the role, what "productive" means for it,
   the target timeline (day 1 / week 1 / month 1), and the prior knowledge
   the docs may assume.
2. The real setup path: the exact steps to get access, install, build,
   run, and test — and where new hires actually get stuck today.
3. The system's shape: the big pieces and how they fit, so the
   orientation can give a mental model (pointing at deeper reference/
   explanation, not reproducing it).
4. How the team actually works: branching, review, deploy, planning
   rituals, comms channels, and the unwritten norms newcomers trip over.
5. The tribal knowledge: the glossary of internal terms, the who-owns-what
   map, and the questions new hires ask most — the raw material to
   capture.

## Workflow

1. **Frame the ramp.** State who's joining, what productive looks like,
   and the day-1 / week-1 / month-1 milestones. Onboarding is a journey
   with a goal (first meaningful contribution), not a doc dump.
2. **Make day one work.** Access and accounts, verified environment setup,
   and a first successful build/run — the single biggest early blocker.
   Getting the system running on day one is worth more than any reading.
3. **Give the mental model, not the manual.** An architecture orientation
   that names the major pieces and how they connect — a map a newcomer can
   hold in their head — with links OUT to the detailed reference/
   explanation (`diataxis-doc-organizer`'s corpus). Resist reproducing the
   whole system; orientation is a sketch, not a survey.
4. **Write down how-we-work.** The real processes (branch → review →
   deploy), the tools, the comms channels, and the rituals and unwritten
   norms (how decisions get made, what "done" means here). This is the
   part that's never written and always needed.
5. **Capture concepts and a glossary.** The domain terms and internal
   jargon a newcomer won't know — the acronyms in every meeting. A glossary
   is one of the highest-value, lowest-effort onboarding artifacts.
6. **Map who owns what and who to ask.** An ownership map plus an explicit
   "when stuck on X, ask Y" — this removes the fear of asking and the
   guessing about whom to interrupt.
7. **Design a first task with an early win.** A real starter task that
   touches the actual workflow end-to-end and ships something small. Early
   success builds confidence and validates that setup and process docs
   work.
8. **Plan for currency.** Onboarding docs rot fastest — setup steps,
   tools, and people change constantly. Assign an owner and adopt the
   "each new hire fixes what tripped them" convention so the docs
   self-heal. Deliver in the Output Format.

The day-1/week-1/month-1 milestone template, the orientation-vs-detail
boundary, and the glossary/who-to-ask formats:
[references/onboarding-sheet.md](references/onboarding-sheet.md).

## Output Format

```
ONBOARDING PLAN — <team/codebase>, role=<...>
Ramp goal:     productive = <definition>; milestones day1 / week1 / month1
Day one:       access/accounts; VERIFIED setup; first successful build/run
Orientation:   mental model of the major pieces + how they connect (links OUT to detail)
How-we-work:   branch/review/deploy; tools; comms; rituals & unwritten norms
Glossary:      internal terms/acronyms a newcomer won't know
Who-to-ask:    ownership map + "stuck on X → ask Y"
First task:    real starter task, end-to-end, ships an early win
Maintenance:   owner; "each new hire fixes what tripped them"; rot-prone spots flagged
Boundaries:    external contributors → contribution-guide-author; README → readme-craftsman;
               corpus-by-mode → diataxis-doc-organizer (onboarding links into it)
```

## Validation Checklist

- [ ] The ramp is framed with a productivity definition and day1/week1/
      month1 milestones.
- [ ] Day-one setup is verified and results in a running system + first
      build/run.
- [ ] Orientation gives a mental model and links OUT to detail rather than
      reproducing the manual.
- [ ] How-we-work captures the real processes, tools, comms, AND unwritten
      norms.
- [ ] A glossary of internal terms and a who-to-ask/ownership map are
      present.
- [ ] A real first task with an early win is designed and touches the
      actual workflow.
- [ ] A currency plan (owner + self-heal convention) exists, because
      onboarding rots fastest.
- [ ] External-contributor, README, and corpus-organization concerns are
      handed to their owning skills.

## Gotchas

- The biggest day-one blocker is setup that doesn't work; a hire who can't
  run the system by end of day one starts demoralized. Verify setup like a
  quickstart and treat it as the top priority.
- Orientation that tries to explain the WHOLE system on day one buries the
  newcomer — they need a map they can hold in their head, not the
  territory. Sketch the major pieces; link to depth.
- The most valuable onboarding content is the unwritten how-we-work — the
  norms, the rituals, the "we don't do X here". If it's only in people's
  heads, capture it; that's the whole point.
- A glossary feels trivial and is one of the highest-leverage artifacts:
  new hires nod through meetings full of acronyms they don't know. Write
  them down.
- Without a who-to-ask map, new hires either interrupt the wrong people or
  suffer in silence. Naming who owns what removes both failure modes.
- Onboarding docs rot faster than any other docs because setup, tools, and
  people change constantly — and stale onboarding is actively harmful
  (sends the hire down dead ends). The "each hire fixes what tripped them"
  convention is what keeps it alive.
- Onboarding a new hire is not the external contribution process. A
  document that mixes internal ramp with external PR workflow serves
  neither.

## Stop Conditions

- The audience is an EXTERNAL contributor (fork, PR, contribution
  workflow) → route to `contribution-guide-author`.
- The task is the README front door for users/evaluators → route to
  `readme-craftsman`.
- The task is organizing the whole docs corpus by mode → route to
  `diataxis-doc-organizer` (onboarding links INTO that corpus).
- The onboarding gap is really a MISSING process (there is no defined
  how-we-work to document, only chaos) → surface that the team must
  establish the process; onboarding docs can capture a real process but
  can't invent one the team won't follow.

## Supporting Files

- [references/onboarding-sheet.md](references/onboarding-sheet.md) — the
  day-1/week-1/month-1 milestone template, the orientation-vs-detail
  boundary, and the glossary and who-to-ask formats.
- `evals/evals.json` — behavior cases including the ramp design, the
  orientation-not-manual discipline, and the currency/self-heal plan.
- `evals/trigger-evals.json` — discrimination against `contribution-guide-author`
  (new hire vs external contributor), `readme-craftsman`, and
  `diataxis-doc-organizer`.
