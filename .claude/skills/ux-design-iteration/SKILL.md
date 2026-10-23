---
name: ux-design-iteration
description: 'Run optional, bounded design iteration before implementation - prototype the smallest interactive artifact, get an independent rendered-UI review, revise/retest, and hand off a reviewed direction. Use when the experience direction is unsettled, the user chooses option B, asks to compare flows, or wants an independent critique within an active iteration. Owns only the iteration method, records and readiness protocol; composes the nearest owners; design authority stays with the project. Advisory: it does not write project artifacts, run commands, launch browsers or use the network; records are returned to the host/user or the project''s state owner for persistence, and prototype/implementation are delegated host/user actions. Do NOT use for ordinary settled design/build, requirements elicitation (requirements-gathering-facilitator), spec authoring (product-spec-writer), design review facilitation (design-review-facilitator) or verification execution (accessibility-test-harness, visual-regression-test-designer).'
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
owner for persistence; the skill does not write the project artifact itself.
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

   **Design-entry questions and context inference (owner rev 2).** Existing A/B choices are unchanged. New choices (design direction 1.1a/b/c) are offered once, recorded in the selection record, and reused across turns, resumes and agent changes; the user can change them later. Infer what context settles and do not ask it: a provided Figma export or styleguide implies follow-my-existing-design (1c); a settled direction implies one mockup; an existing application implies UI consistency lock ON (1.5) without asking. At design entry ask at most TWO questions in total (the A/B method and, only when context does not settle it, the direction/mockup choice); before each question explain benefits, drawbacks and unknown costs plainly, never invent time or price, recommend one with a reason, and ask one atomic question. Ask the final-clickthrough question only after implementation (1.3) and the proof-set question only after that (section 5). Never ask a third design-entry question: if a decision is still unsettled, record it as an open item or UNKNOWN for later instead of asking. The cap excludes the post-implementation clickthrough question (1.3) and proof-set question (section 5). The cap covers design-entry choices only: later rule-enforcement requests for a missing fact, artifact or consent (for example the required second mockup under 1b, or missing pre-design details) are not design-entry questions and may be asked when their rule requires them. Each entry question is atomic (one decision); if the direction is still UNKNOWN after the cap, record it as an open item/UNKNOWN, never fabricate it, and do not claim readiness for work that depends on mockups until the direction is known.

2. **Decide the mode; return the record.** Return the exact selection record
   (mode, feature/task scope, instruction source, delivery endpoint, iteration
   budget, selection/offer count, record_location) to the host/user or the
   project's state owner
   for persistence; do not write the project artifact yourself. The choice is
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
5. **Concepts.** Produce up to four meaningfully different, non-cosmetic
   candidate flows by default, configurable with a recorded reason; each states
   its hypothesis and what would make it right or wrong. Cosmetic variants never
   count as alternatives; the mockup count and direction-conditional minimums
   are in 1.2.
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
10. **Budget and readiness.** Defaults are **up to four concepts and up to
    four mockups** (the direction-conditional minimums and four-mockup hard
    maximum are in 1.2) and **up to three independent evaluation passes**,
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

## Design direction, mockups, UI lock and live acceptance (owner rev 2)

These sections extend the iteration method; they do not replace the A/B choice or the readiness rules below. Section 1.2 mockup count (concepts/mockups) and the two-question entry cap (normative sentence in Workflow step 1) and the five pre-implementation fields are specified below; the clickthrough schema field (the sixth tracked field) and E30 are deferred to the next wave; section 1.4 (proof set) and section 5 (proof set and spoken demo, owner rev 2) are specified below; the ### 2/3/4 headings below and the owner H2 section ## 5 are the owner brief's section names, not Workflow step numbers. The skill stays strictly advisory: it writes no artifacts, runs no commands, launches no browser, uses no network, and delegates prototypes, mockups and proofs to the host/user under existing authority.

### 1.1 Design direction (choose one, once)

All three reuse the project's in-code design system and tokens as the authority (compose design-system-token-governor); none invents a parallel system.

- **(a) Guided premium - clarity first.** Reviewer-checkable heuristics: exactly one primary action per screen; one dominant element per view; spacing and type only from the token scale; at most one accent plus neutrals per view unless the design system defines more; system-native patterns; motion only on state change and only where it explains the state. Under UI lock (1.5), a heuristic the existing UI cannot meet with its current vocabulary yields to the lock and is recorded as a residual, not forced.
- **(b) Creative options.** Propose 2-4 distinct directions; each states its hypothesis and what would make it right or wrong. Cosmetic variants do not count as distinct. Under UI lock the directions must differ in experience (flow, structure, interaction, states), not in look.
- **(c) Follow my existing design.** Use the user-provided pre-design or guideline under the pre-design rules (3).

### 1.2 Mockup count (1-4)

Concepts are non-cosmetic candidate flows; mockups are exercisable artifacts of a chosen concept or direction; a prototype is the exercisable artifact used for acceptance/review of a chosen concept and may be the same artifact as a mockup - multiple prototypes of one concept do not count as multiple mockups. Concepts and mockups each have a hard maximum of four. Four is the hard maximum and is never exceeded; defaults are up to four concepts and up to four mockups, configurable only with a recorded reason. At least one concept is required whenever the iteration runs; zero concepts only when iteration is not-applicable/justified N/A with a recorded reason. Direction rules override the defaults: under guided premium (1a) and follow-my-existing-design (1c) exactly one mockup is permitted - one, never a second; under creative options (1b) at least two mockups are required, each for a distinct non-cosmetic concept or direction. A recorded reason may reduce counts within the direction's allowed range but never below a direction minimum, never above four, and never contrary to the direction rules. cosmetic variants never count as concepts or mockups. Every evaluation pass still counts.

### 1.3 Final clickthrough (offered, never required)

After implementation, offer an interactive clickthrough of the running app (compose clickthrough-test-engineer, MANUAL-ONLY: name it and stop; run it only on an explicit yes). Offer it immediately after implementation while the local stack is up. If declined or impossible, record a named UNRUN stating the defect classes that become unobservable - state hydration and transition bugs (for example a resume flow that opened the wrong step while every static suite was green). Readiness may still be declared; the record shows it was not run; clickthrough is never a pass. The post-implementation status is offered, declined or UNRUN; it is not part of the pre-implementation selection record.

### 1.4 Proof set (offered, never required)

After implementation and the clickthrough decision, offer the proof set once (specification in section 5). Declining it is recorded and is not a defect. The proof set is evidence of what was observed, never a substitute for a check, and never upgrades readiness; production-data-only input means a named UNRUN with that reason.

### 1.5 UI consistency lock (default by context, not a question)

Redesign the experience, keep the interface. UX (flow, step order, information architecture, what appears when, interaction within the existing component vocabulary, copy, state handling) may be redesigned. UI (components, tokens, colours, type scale, spacing scale, iconography, motion patterns, visual language) stays consistent with what is already in place. Default ON for an existing application or an in-code design system; OFF for greenfield. Do not ask it as a question: the user turns it off by asking for a visual refresh, and that override is recorded. An element/design conflict is recorded in authority_conflict (1c/3).

Permitted under the lock: new screens, steps, dialogs, sheets and layouts composed only from existing components and tokens; new copy; new states built from existing patterns. Not permitted: a new component not in the library; a new token, colour, type size or spacing value; new iconography; a new motion pattern. A genuinely needed new element becomes a **PROPOSED UI ADDITION** with a justification routed to the design-system owner as a separate decision; it does not enter the mockup as approved.

ENFORCEMENT: the independent reviewer produces an inventory diff composing frontend-architecture-mapper for components and design-system-token-governor for tokens. Every component, token, colour, type size, icon and motion in the mockup is mapped to an existing project element; any unmapped element is a finding; an unapproved unmapped element makes the mockup **NOT READY** with the element named. Under 1c, a pre-design conflicting with the lock follows rule 3: the in-code UI wins unless the user states otherwise for named elements. State the rationale generally: an experience can be redesigned within existing tokens and kit recipes without a design-system change, which is the point of the lock.

### 2. Prototype acceptance - live, not a picture

The reviewer enforces this; a failing artifact is **NOT READY**.

- **Exercisable:** the reviewer moves through the flow by clicking and typing; every transition named in the story is reachable.
- **Stateful:** state carries across steps and derived content updates from it - a count-carrying primary action reads the real count, with no hard-coded labels.
- **Non-happy states reachable:** for every state the story names in scope (empty, invalid input, permission-denied/viewer, loading, error, recovery), the prototype shows the state and how the user continues. Scope stays the named interaction; the prototype is not a parallel application.
- **Self-contained:** fixtures only, no backend, no network, no repository change. Real tokens come from the project or a bound pre-design; under UI lock, the project's only.
- **Responsive and keyboard-operable:** works at the declared viewports, is keyboard-operable with visible focus.

TEETH: a static image or non-interactive comp whose named transitions cannot be exercised is **NOT READY** with the unexercisable transitions named; screenshots are not evidence; the proof set does not upgrade it. Rationale: defects live in transitions.

### 3. Pre-design (1c)

A pre-design enters only as a user-provided artifact; this skill does not fetch, open URLs or launch a browser. Bind it by file name, version, byte size and sha256. Unspecified items are declared UNKNOWNs - never invent a token, spacing, state or interaction. An authority conflict is recorded, not guessed: the in-code design system keeps authority per docs/paths/design-and-build-ui.md unless the user states the pre-design supersedes it for named elements. Ask once, record the answer in the authority_conflict field (Output Format item 1), and reuse it without re-asking.

### 4. Retro rules

- **Failure triage:** when a check fails, classify it as a stale assertion, a product bug, or a wrong metric before fixing it; record which.
- **Scope discipline:** a defect outside the surface under change is named a residual, never fixed by loosening a test.
- **Mockup binding:** the approved mockup is bound by sha256 and byte size when the host provides it; the skill writes nothing.

## 5. Proof set and spoken demo (owner rev 2)

(Owner rev 2 H2 section; not a Workflow step number.)

Offer the proof set once, after the clickthrough decision. Declining it is recorded and is not a defect; a decline or an impossible run never changes readiness. The skill specifies the set, folder layout and manifest but delegates writing to the host/user or the project's state owner under existing authority. Compose screenshot-evidence-planner MANUAL-ONLY: name it and stop; run capture only on an explicit yes, never automatically; do not restate its policy.

A proof set may include the approved mockup (bound by sha256 and byte size), screenshots at named checkpoints, a recording of the clickthrough if it ran, and a short spoken-demo script keyed to those checkpoints (last, lowest priority; not evidence of a check). The manifest lists every file with its size and sha256 and records captured-over-expected. Folder layout: MANIFEST.json at the proof-set root, with mockup/, screenshots/<checkpoint>/, clickthrough/ and demo-script.md alongside it; the record names the delegated writer and the captured-over-expected differences.

Use test fixtures or a UAT project only - never production data. If only production data exists, record the proof set as **UNRUN** with that reason and capture nothing. A proof set is evidence of what was observed, never a substitute for a check, and never upgrades readiness; a production-data proof set and an unrun proof set are both never a pass. The manifest lists every artifact in the set with its size and sha256; the one exception is MANIFEST.json itself, which cannot contain its own hash, so files[] records every artifact except MANIFEST.json. proof_set status is offered, declined, UNRUN or collected: when declined, decline_reason is recorded, manifest_path is null and files is empty; when UNRUN, unrun_reason names the single blocking cause from production_data_only, no_local_stack, missing_tooling or failed_capture (a non-production impossible run is recorded the same way and is never a defect), manifest_path is null and files is empty; when collected, folder_layout and manifest_path are present. demo_script is skipped whenever proof_set is declined or UNRUN. Checkpoint keys are lowercase kebab-case with no path separators. Every files[].path, manifest_path and folder_layout is project-relative: no absolute paths, no .. traversal and no symlinks. Screenshots and recordings are fixtures/UAT only; redact secrets, credentials and personal data before capture and never capture production screens.

## Output Format

Return, in this order:

1. **Selection record** - mode (A or B), feature/task scope, instruction
   source, delivery endpoint, iteration budget, selection/offer count, and
   where the record lives.

   The selection record also carries the five pre-implementation fields: design_direction (1a, 1b, 1c, or not-applicable); mockup_budget (up to four concepts and up to four mockups by default; direction rules override: 1a/1c exactly one mockup, never a second; 1b at least two mockups, each a distinct non-cosmetic concept or direction; four hard maximum never exceeded; a recorded reason may reduce within the direction bounds but never contradict the direction rules); ui_lock (ON/OFF plus any visual-refresh override reason); pre_design_binding (name, version, byte size, sha256) when 1c; and authority_conflict (recorded source conflict and its resolution; in-code design system wins unless the user names elements the pre-design supersedes). pre_design_binding is always present: not-applicable when 1c is not used, and for 1c either the binding or a named UNKNOWN (not bindable). These five pre-implementation fields are the tracked selection fields; the clickthrough status remains post-implementation (1.3) and its dedicated schema field is deferred to the next wave.

   **Mode A:** if mode A was selected, stop after the selection record and route
   to the standard design/build path; items 2-6 below apply only to mode B.

2. **Iteration record** - brief (with UNKNOWNs), story, up to four non-cosmetic concepts (candidate flows)
   with hypotheses and the direction-conditional mockup count from 1.2,
   prototype scope/fixtures/incompleteness,
   per-evaluation records with all eight fields, findings and dispositions.
   After implementation, the iteration/post-implementation record also carries
    proof_set (offered,
    declined, UNRUN or collected) and demo_script (skipped, drafted or narrated)
    from the reference template; post-implementation status is never part of the
    pre-implementation selection record (1.3).
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
- Candidate concepts are meaningfully different beyond cosmetics and each has a hypothesis; the mockup count follows the 1.2 rule: at least one concept when iteration runs, 1a/1c at most one mockup (never a second), 1b at least two distinct concepts/directions and two mockups each distinct, four hard maximum never exceeded, and a recorded reason never reduces below a direction minimum.
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
- The design-entry questions followed the owner discipline: at most two questions at design entry, context inference used first (Figma export implies 1c, settled direction implies one mockup, existing application implies UI lock ON without asking), and no invented cost.
- The chosen design direction is one of 1a/1b/1c, or not-applicable when no direction is needed.
- Under guided premium, exactly one primary action per screen and one dominant element per view are checked; under UI lock, UI stays consistent and any inability to meet a heuristic is recorded as a residual, not forced.
- The UI-lock inventory diff maps every component/token/colour/type size/icon/motion to an existing project element; an unapproved unmapped element is NOT READY with the element named, and a needed new element is a PROPOSED UI ADDITION, not an approved mockup element.
- Prototype acceptance is live: transitions exercisable, state carries, real counts (no hard-coded labels), every named non-happy state reachable, fixtures only, declared viewports and keyboard focus; a static image or non-interactive comp whose transitions cannot be exercised is NOT READY with those transitions named.
- The clickthrough was offered after implementation; when declined or impossible it is a named UNRUN naming the unobservable state-hydration/transition defects, readiness is unchanged, and no pass is claimed.
- Pre-design is bound by name/version/byte size/sha256, gaps are UNKNOWNs, and an authority conflict is recorded (in-code wins unless the user names superseding elements).
- Retro failures were classified before fixing; out-of-scope defects are named residuals; the approved mockup is bound by sha256 and byte size when the host provides it; the skill writes nothing.

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
- A picture is not a prototype: a static image or non-interactive comp cannot exercise the transitions where defects live; it is NOT READY with the missing transitions named.
- Cosmetic variants are not creative directions: under creative options they must differ in flow/experience, and under UI lock they must differ in experience, not look.
- A new component under UI lock is not a mockup detail: it is a PROPOSED UI ADDITION routed to the design-system owner, and an unapproved unmapped element is a finding that makes the mockup NOT READY.
- Hard-coded labels and missing permission-denied states are acceptance failures, not polish: the count must come from state and every named non-happy state must show how the user continues.

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
- A requested acceptance is a static image or non-interactive comp: refuse it as evidence, declare NOT READY, and name the unexercisable transitions; do not treat a screenshot or the proof set as a pass.
- The next check is the clickthrough: name clickthrough-test-engineer (MANUAL-ONLY) and stop for the human; never run it silently. If declined/impossible, record the named UNRUN and keep readiness unchanged.
- UI lock blocks a needed element: propose a PROPOSED UI ADDITION to the design-system owner as a separate decision; never enter an unapproved new component/token into the mockup.
- A pre-design would need fetching, opening a URL or a browser to read: stop; only a user-provided artifact can enter, bound by name/version/byte size/sha256.

## Supporting Files

- [references/iteration-record-and-readiness.md](references/iteration-record-and-readiness.md) -
  the full record schema fields, the 9 loop elements, readiness and
  false-completion rules, budget ledger, invalidation rules, accepted-with-
  disclosure guidance, and a worked template.
  The SKILL carries the 1.1 direction rules, 1.2 mockup count, the two-question entry cap, 1.3 clickthrough status rule, 1.4 proof set, 1.5 UI consistency lock, 2 live-prototype acceptance teeth, 3 pre-design binding, 4 retro rules and 5 proof set/spoken demo (owner rev 2); the reference carries the matching record schema/fields and the template support; the proof-set rules themselves are normative in sections 1.4 and 5 and are not restated in the reference. E15-E19 and E25 are now in evals; only the remaining clickthrough-lifecycle detail and E30 (PR-2 reference-restatement issue) stay deferred to the next wave.
- [evals/evals.json](evals/evals.json) - the 31 behaviour cases (E1-E13, E14-E29 and PR-2 E31-E32) that exercise the choice, loop, records, readiness, budget and proof set; E30 is deferred to the next wave with the reference-restatement issue.
- [evals/trigger-evals.json](evals/trigger-evals.json) - trigger
  discrimination against the nearest owners and the catalog-navigation case.
- **Normative copy / maintenance:** the reference is the detailed normative copy
  of the loop, readiness, ledger and acceptance rules (exception: the proof-set
  rules are normative only in this SKILL, sections 1.4 and 5, and the reference
  records their schema/template support); the workflow above is the summary -
  keep both in sync. The path step, owner names and A/B wording are
  pointers to docs/paths/design-and-build-ui.md and docs/skills-catalog.md;
  re-check them when those change.
