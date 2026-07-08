# Onboarding Sheet

Detail for `onboarding-doc-designer`. Read on demand.

## Day-1 / Week-1 / Month-1 milestone template

| Milestone | Target |
|---|---|
| End of day 1 | Access sorted; environment set up; system builds and runs |
| End of week 1 | Understands the mental model; shipped a tiny first change; knows who to ask |
| End of month 1 | Working through real tasks independently; contributing to reviews |

Define "productive" for the role, then work backward to these.

## Orientation vs detail boundary

Onboarding gives a MAP, not the territory:

| Onboarding provides | Links OUT to |
|---|---|
| The major pieces and how they connect | Detailed architecture reference/explanation |
| The mental model to hold in your head | Deep-dive docs per component |
| "This talks to that via X" | The full API/interface reference |

Reproducing the whole system on day one buries the newcomer. Sketch;
link to depth (the corpus `diataxis-doc-organizer` organizes).

## Day-one essentials (top priority)

- Accounts/access/permissions.
- Environment setup — VERIFIED on a clean machine.
- First successful build + run + test.
- The one starter task queued up.

A hire who can't run the system by end of day one starts demoralized.

## How-we-work (the usually-unwritten part)

- Branch → review → deploy flow (the real one).
- Tools and where things live.
- Comms channels + norms (where to ask what).
- Rituals: standups, planning, decision-making, what "done" means.
- Unwritten norms ("we don't do X here").

## Glossary & who-to-ask

**Glossary** — internal terms/acronyms with plain definitions. Highest
leverage per line of effort.

**Who-to-ask** —
```
| Area | Owner | Ask when… |
|------|-------|-----------|
| <area> | <role/team> | stuck on <X> |
```
Removes the fear of asking and the wrong-person interrupt.

## First task with an early win

- Real, small, end-to-end (touches setup → change → checks → PR → merge).
- Ships something visible; builds confidence.
- Doubles as a test that setup/process docs actually work.

## Currency (onboarding rots fastest)

- Assign a maintenance owner.
- Convention: **each new hire fixes what tripped them** on the way through
  — the docs self-heal.
- Flag rot-prone spots: setup commands, tool versions, people/ownership.
