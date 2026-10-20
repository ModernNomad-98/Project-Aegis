---
name: ux-design-iteration
description: 'Run optional, bounded design iteration before implementation - prototype the smallest interactive artifact, get an independent rendered-UI review, revise/retest, and hand off a reviewed direction. Use when the experience direction is unsettled, the user chooses option B, asks to compare flows, or wants an independent critique within an active iteration. Owns only the iteration method, records and readiness protocol; composes the nearest owners; design authority stays with the project. Advisory: it does not write project artefacts, run commands, launch browsers or use the network; records are returned to the host/user or the project''s state owner for persistence, and prototype/implementation are delegated host/user actions. Do NOT use for ordinary settled design/build, requirements elicitation (requirements-gathering-facilitator), spec authoring (product-spec-writer), design review facilitation (design-review-facilitator) or verification execution (accessibility-test-harness, visual-regression-test-designer).'
---

# UX Design Iteration

Terms: **UX** means user experience; **UI** means user interface; **A/B** means the two offered approaches (standard design/build versus
explore-and-refine) - not a measured experiment (that is ab-test-designer);
ship/deploy readiness is release-readiness-reviewer's, not this skill's;
**artifact** means the candidate prototype or rendered surface the reviewer
examines; **authority** means the project's recorded design and product
decision-making owner, not this skill.

## Purpose

Some features should not go straight from a requirement to a built screen. When
the experience direction is genuinely unsettled, cheap iterations before
implementation find a better flow than expensive rework after it. This skill
owns **only that iteration method**: the up-front choice, the bounded loop, the
record that makes each evaluation auditable, the readiness gate that prevents
false completion, and the reviewed handoff. It composes the existing Aegis
owners for requirements, states, accessibility, acceptance criteria, visual
evidence and handoff instead of duplicating them, and it never becomes a
second design system, release gate or orchestrator.

The skill is **advisory and auto-invocable**. It produces guidance, records and
review structure only. It does not write files, run commands, launch browsers,
use the network or create prototypes itself: a prototype, render or
implementation is a **delegated host or user action** under existing authority.
The records it produces are returned to the host/user or the project's state
owner for persistence; the skill does not write the project artefact itself.
The recorded mode is a method choice, not a blanket grant of tool or
production permission.

## Use When

- The experience direction is unsettled at the existing design entry (path step
  3) and the user wants to compare flows before building.
- The user chooses **B. Explore and refine first** at the offered choice, or
  asks for flow comparison, an interactive prototype, an independent critique,
  or a bounded iteration budget before implementation.
- The up-front choice itself needs to be presented or recorded (including an
  explicit **A** selection, which returns only the selection record and routes to
  the standard design/build path); an active iteration record also resumes here.
- A previous iteration record exists and must be resumed, reused, extended or
  handed off without losing its evidence or budget state.
- A prototype or rendered candidate exists and needs the independent review,
  disposition, retest and readiness structure this skill defines.
- The user changes the mode mid-task, wants to reopen a settled direction, or
  needs the readiness declaration before production work can start.

**Do not use when:** the request is a settled, ordinary implementation with no
active iteration record; the need is requirements elicitation, spec authoring,
design review facilitation, accessibility verification or visual regression
tooling (route to the named owners); or the user declined the optional iteration
path (standard design and build remains the default).

## Inputs to Inspect

- The user's existing request, brief, requirements or product spec, and any
  recorded design authority (design system, approved direction, revision).
- The existing step-3 design/state record or handoff artifact (project-state
  format, design doc, earlier iteration record), including the recorded mode,
  scope, instruction source, delivery endpoint, budget and offer count.
- Prior iteration evidence: brief, story, candidates, prototype scope,
  evaluation records, review findings, dispositions, retests, budget ledger and
  open items, bound to the candidate version/scenario/fixtures/baseline.
- The change class and validation depth from the classification step; the
  applicable Aegis owners for the states and evidence being iterated.
- Hard constraints: budget, deadline, platform/viewports, accessibility
  obligations, production boundary, and the host capabilities actually
  available for producing or rendering a candidate.
- The user's current choice (A, B, or a later change), and whether this feature
  already has a recorded choice that must be reused rather than re-offered.

## Workflow

1. **Offer the choice once, at the design entry.** If the experience direction
   is unsettled, ask once: "How would you like to approach this feature?"
   Present **A. Standard design and build** (the default) and **B. Explore and
   refine first** (flow comparison, interactive prototype, independent review,
   bounded budget; recommended when new or uncertain, with the extra effort
   explained and no invented time or price). Do not offer it for a generic
   build request, for a settled direction, on every turn, or through a
   settings/screen flow; the agent leads it as a method question. Before asking,
   explain in plain language what A and B mean, why each is offered, its benefits
   and drawbacks for this feature, and its known or unknown cost in money, setup
   time and ongoing effort (never invent a price or a time); recommend one with a
   reason tied to the user's context; if a deciding fact is missing, ask only for
   that fact this turn and ask no decision question; then ask one atomic question.
   If the direction is already settled or the request is an ordinary implementation,
   route it through change-classification-gate and docs/paths/design-and-build-ui.md
   and do not offer iteration.
2. **Decide the mode; return the record.** Return the exact selection record
   (mode, feature/task scope, instruction source, delivery endpoint, iteration
   budget, selection/offer count, record_location) to the host/user or the
   project's state owner
   for persistence; do not write the project artefact yourself. The choice is
   reused across turns, resumes, and tool or agent changes; a missing record is
   recovered from context, not treated as an opt-out, and a later user change is
   honored. The host/user or state owner performs any persistence; the skill
   only returns the exact content and may preview the intended location, never
   writing it.
3. **Brief.** Build an evidence-backed brief: concrete user/journey evidence,
   the problem and job, the current workaround, constraints and non-goals, and
   explicitly labeled UNKNOWNs. Never invent a requirement.
4. **Story.** Write the end-to-end experience story: start, success, failure
   and recovery, empty, permission-denied and timing states, each with its
   expected outcome and how the user continues.
5. **Flows.** Produce at least two meaningfully different, non-cosmetic
   candidate flows (default three, configurable); each states its hypothesis
   and what would make it right or wrong. Cosmetic variants do not count as
   alternatives.
6. **Prototype.** Declare the prototype scope: what is included, mocked or
   incomplete, which interaction it exercises, the fixtures used, and the
   smallest interactive artifact that can exercise the named interaction.
   Prototype creation is delegated to the host or user under existing
   authority; an isolated prototype is authorized scope only. Before any
   evaluation pass (including the first prototype review), declare the readiness
   criteria (scenarios/states/input methods/viewports, coverage or justified N/A,
   required checks and expected evidence) in the record.
7. **Independent review.** A reviewer other than the author inspects and
   exercises the candidate and records findings. Do not self-review or claim a
   review that did not happen. Rendered-UI review compares the candidate with
   the brief and the design system across hierarchy, layout, typography,
   spacing, labels, component consistency, responsive behavior, focus,
   keyboard and accessibility, with actual evidence per check.
8. **Return every evaluation record.** For each pass return the question/hypothesis,
   candidate version, scenario and conditions, observation, evidence, finding,
   disposition and uncertainty. Every pass counts, including an unchanged
   retest; never reset the counter, silently switch candidates, or lower a
   threshold.
9. **Disposition, retest and handoff.** Give every finding an explicit
   disposition. Before advancing, independently retest the changed or
   unchanged candidate; no manufactured change and no unearned PASS. The
   reviewed handoff preserves the selected flow, content, states, visual
   direction, authority, open items, evidence, budget state and next action, and
   composes
   the handoff owner rather than re-designing the protocol.
10. **Budget and readiness.** Defaults are **up to three concepts and up to
    three independent evaluation passes** (at least two non-cosmetic flows),
    configurable with a recorded reason; every pass counts; scale effort to the
    change. End by declaring readiness against the readiness rules in
    references/iteration-record-and-readiness.md. Budget expiry with unresolved
    work, an unrun or failed required check, a missing capability, or a
    manual-only check that was not run yields **NOT READY** with the smallest
    decision needed, never a silent PASS. The iteration itself needs no
    per-round owner approval; present the reviewed prototype on request; after
    readiness, full delivery continues only under existing authority and still
    verifies the integrated feature; merge/deploy/spending authority is
    unchanged.

## Output Format

Return, in this order:

1. **Selection record** - mode (A or B), feature/task scope, instruction
   source, delivery endpoint, iteration budget, selection/offer count, and
   where the record lives.

   **Mode A:** if mode A was selected, stop after the selection record and route
   to the standard design/build path; items 2-6 below apply only to mode B.

2. **Iteration record** - brief (with UNKNOWNs), story, at least two
   non-cosmetic flows with hypotheses, prototype scope/fixtures/incompleteness,
   per-evaluation records with all eight fields, findings and dispositions.
3. **Review record** - reviewer identity and independence, what was inspected
   or exercised, the rendered-UI check matrix with PASS/FAIL and evidence, and
   any limitations.
4. **Retest record** - candidate version retested, scenario/fixtures/baseline,
   result, and which earlier evidence the change invalidated.
5. **Readiness declaration** - READY or NOT READY, scenarios/states/input
   methods/viewports declared, coverage or justified N/A, every required check
   with observable outcome and evidence, blocking/unresolved items, production
   boundary, and the smallest decision if not ready.
6. **Reviewed handoff** - preserved flow, content, states, visual direction,
   authority, open items, evidence pointers, budget state and next action, in
   the form the project's existing handoff/state artifact expects, returned to
   the host/user or state owner for persistence (the skill does not write it).

The full record schema and readiness rules are in
[references/iteration-record-and-readiness.md](references/iteration-record-and-readiness.md).

## Validation Checklist

- The A/B choice was explained before asking: plain-language meanings, why each
  option is offered, its case-specific benefits and drawbacks, and its known or
  unknown cost in money, setup time and ongoing effort (no invented price or
  time); one option was recommended with a reason, a missing deciding fact was
  the only question that turn, and the final question was atomic.
- The choice was offered at most **once per feature/selection**, with the
  recorded mode returned for persistence and reused on resume; a generic build
  request did not select iteration; a missing record was recovered, not treated
  as an opt-out.
- The brief cites concrete evidence and labels every UNKNOWN; no requirement,
  persona, quote, timing, rate or result was fabricated.
- The story covers the defined start/success/failure/recovery/empty/permission/
  timing states with expected outcomes where the feature defines them.
- At least two candidate flows are meaningfully different beyond cosmetics and
  each has a hypothesis.
- Prototype scope lists included/mocked/incomplete parts and fixtures, and the
  artifact is the smallest that exercises the named interaction.
- The reviewer is independent of the author and actually inspected/exercised
  the artifact; rendered-UI checks have per-check evidence, not adjectives.
- Every evaluation record has all eight fields; every finding has a
  disposition; every advance has an independent retest, including unchanged
  candidates; the budget ledger counts every pass and never resets.
- The readiness declaration states scenarios/states/inputs/viewports before
  evaluation, records coverage or justified N/A, shows required checks PASS on
  the advanced candidate, has no unresolved blocking failure, binds evidence to
  the candidate/scenario/fixtures/baseline, and names the production boundary.
- Changes after evaluation start record the reason/decision/evidence and
  invalidate affected results until retested; no check was removed or
  redefined; no threshold was silently lowered.
- The handoff preserves flow, content, states, visual direction, authority,
  open items, evidence pointers, budget state and next action.
- Nothing claims unexercised interaction, human-user validation or a host
  capability that did not run; unavailable checks are reported UNRUN with
  their exact prerequisite.

## Gotchas

- A choice offered on every turn is not a choice; it is friction. Offer it
  once, record it, reuse it.
- A prototype is evidence, not product. Without an explicit production
  boundary, prototype success gets misread as production readiness.
- Independent review means another actor inspecting or exercising the
  artifact, not the author restating their intent. A review with no inspection
  evidence is not a review.
- An unchanged candidate can be retested and must still count as a pass; a
  fabricated one-line diff to look active is worse than an honest unchanged
  retest.
- Findings without dispositions become feel-good notes. Every finding must
  end fixed, accepted with a recorded limitation, re-scoped, or deferred with
  a named owner.
- "No evidence of failure" is not "verified". Empty checks, unrun checks and
  structural JSON are not runs.
- The mode selection is not permission to run tools, touch production, or
  override a manual-only skill or host permission. Permission to read a
  prototype is not permission to adopt it.
- Budgets exist to stop runaway exploration, not to force activity. Expiry
  yields NOT READY plus the smallest decision, never a manufactured pass.
- The nearest owners exist so this skill can compose them: requirements and
  spec craft belong to requirements-gathering-facilitator/product-spec-writer,
  state design to edge-state-ux-designer, responsive craft to
  mobile-viewport-craft, accessibility verification to
  accessibility-test-harness, visual evidence to
  visual-regression-test-designer/screenshot-evidence-planner, handoff to
  phased-work-handoff-designer, review facilitation to
  design-review-facilitator, criteria review to acceptance-criteria-reviewer,
  and lifecycle routing to project-orchestrator.

## Stop Conditions

- The user declines iteration or the direction is already settled: use the
  standard design/build path; do not re-offer.
- The request is requirements elicitation or spec authoring: route to
  requirements-gathering-facilitator / product-spec-writer.
- The request is state-matrix design, responsive/touch craft or accessibility
  verification: route to edge-state-ux-designer / mobile-viewport-craft /
  accessibility-test-harness.
- The request is acceptance-criteria review, screenshot planning,
  handoff-protocol design or design review facilitation: route to the named owner;
  this skill integrates the artifacts. For visual regression,
  visual-regression-test-designer designs coverage, while capture/execution is an
  authorized host action (for example Playwright or a clickthrough host session),
  never performed by this skill.
- The work would cross the production boundary (real app behavior, API/data/
  schema integration) before the criteria pass: stop, state NOT READY, and take
  the smallest decision back to the user under existing authority.
- A required host capability (prototype editor, renderer, interaction harness,
  independent reviewer session) is unavailable: preserve the work, report the
  check UNRUN with its exact prerequisite, and do not claim a pass.
- A manual-only skill or host permission is required for the next check: name
  it and stop for the human; do not invoke it silently.
- The iteration budget is exhausted with unresolved work: declare NOT READY and
  ask for the smallest decision (extend budget, accept a recorded limitation,
  change scope, or stop); never silently continue, reset or lower the criteria. If the final
  budgeted pass already establishes every required check, follow the readiness
  rules instead - the cap itself is not a blocker.
- Any instruction would require this skill itself to write files (including
  persisting the iteration record), run commands, launch browsers, use the
  network or create prototypes: stop and delegate to the host/user action under
  existing authority, returning the exact record/content for the host/user or
  state owner to persist. The host/user or state owner performs any persistence
  after receiving the returned content; the skill never writes it.
- The request is a measured A/B experiment (ab-test-designer) or a ship/deploy
  release-readiness gate (release-readiness-reviewer): route there; this skill's
  A/B names journey options and its readiness is design-progress readiness only.

## Supporting Files

- [references/iteration-record-and-readiness.md](references/iteration-record-and-readiness.md) -
  the full record schema fields, the 9 loop elements, readiness and
  false-completion rules, budget ledger, invalidation rules, accepted-with-
  disclosure guidance, and a worked template.
- [evals/evals.json](evals/evals.json) - the 13 behaviour cases (E1-E13) that
  exercise the choice, loop, records, readiness and budget.
- [evals/trigger-evals.json](evals/trigger-evals.json) - trigger
  discrimination against the nearest owners and the catalog-navigation case.
- **Normative copy / maintenance:** the reference is the detailed normative copy
  of the loop, readiness, ledger and acceptance rules; the workflow above is the
  summary - keep both in sync. The path step, owner names and A/B wording are
  pointers to docs/paths/design-and-build-ui.md and docs/skills-catalog.md;
  re-check them when those change.
