# Product Spec Sheet

Detail for [product-spec-writer](../SKILL.md). Read on demand.
ADR means architecture decision record; UI is user interface; QA is quality
assurance; `p95` is the 95th-percentile observed value.

## Spec template

```
# <Feature> — Product Spec

## Problem & why now
<user problem, job-to-be-done, evidence it's real, why now>

## Goals
- <outcome, measurable where possible>

## Non-goals
- <explicitly out of scope>

## Users / roles
<who this is for; requester vs user>

## Scenarios & flows
- Happy path: <narrative>
- Alternate: <important variations>

## Functional requirements
- R1: <specific, testable statement>
  - Acceptance: <given/when/then or checklist>

## Edge cases & errors
<empty / invalid / forbidden / partial failure>
(error model → error-taxonomy-designer; UI states → edge-state-ux-designer)

## Dependencies
<cross-team / platform / sequencing / cited ADRs>

## Rollout intent
<staged? to whom? gated on what?>  (mechanics → feature-flag-rollout-strategist)

## Repeated-request outcomes

For every state-changing action, state the observable outcome on each
repeated-request case (the spec states outcomes only — the mechanism belongs
to `tech-spec-writer` and `command-gateway-architect`):

| Case | What the spec must state |
| --- | --- |
| Retry (same request after a timeout/error) | the result the user observes: same outcome returned, or a new attempt, per action |
| Double submit (one user, two quick submits) | one effect or two; how the second is recognized |
| Second tab (same session, parallel submit) | the result on the second tab |
| Stale request (an old request arrives after newer state) | rejected / ignored / applied — named per action |
| Duplicate events (webhook/notification repeats) | whether duplicates can reach the user, and what they see |

Template line for the Edge cases & errors section:

```
Repeated-request outcomes: <action> — retry: <outcome> — double-submit:
<outcome> — second-tab: <outcome> — stale-request: <outcome> —
duplicate-events: <possible? outcome>
```

## Success metrics & guardrails
<what proves the problem is solved; what must not regress>

## Open questions
<decisions needed; technical ones → adr-writer>
```

## Acceptance-criteria patterns

**Given/When/Then**
```
Given a user with 3 saved searches
When they save a 4th with a duplicate name
Then the save is rejected with a "name already used" message
```

**Checklist** (for simpler requirements)
```
- [ ] Empty query is rejected before submit
- [ ] Results are scoped to the current workspace
- [ ] A saved search persists across sessions
```

Rule: someone who wasn't in the room can verify it without asking you.

## Testable-requirement rewrites

| Vague | Testable |
|---|---|
| "Fast" | "Results render within the p95 latency budget (owner: latency-budget-architect)" |
| "Intuitive" | "A first-time user completes the core task without help in usability testing" |
| "Handles errors gracefully" | "On a failed save, the draft is preserved and an actionable error shows" |
| "Scales" | "Supports N concurrent users at the stated load (owner: load-test-planner)" |

Don't invent the number — name it as a requirement and cite the owner.

## Spec vs ADR discriminator

| | Product spec | ADR (adr-writer) |
|---|---|---|
| Question | What are we building for users, and how do we know it's done? | Which technical option did we choose, and why? |
| Audience | Product, design, eng, QA | Engineers, future maintainers |
| Core content | Problem, scope, scenarios, acceptance, metrics | Context, decision, alternatives, consequences, rollback |
| Example | "Saved searches feature" | "Use Postgres full-text vs a search engine" |
| Relationship | May CITE an ADR as a dependency | Records a decision a spec depends on |

If you're naming tables, services, or libraries and weighing their
trade-offs, you've crossed into ADR territory — route it.
