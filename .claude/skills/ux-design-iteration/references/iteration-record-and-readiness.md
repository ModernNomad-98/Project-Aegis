# Iteration record, readiness rules and worked template

Reference for the `ux-design-iteration` skill. It defines the record the
skill produces, the readiness/false-completion rules the skill enforces, the
nine required loop elements, the budget ledger, evidence invalidation, the
accepted-with-disclosure rules, and a worked template. It is method and record
guidance only: it never directs the skill to write files, run commands, launch
browsers or use the network; records are returned to the host/user or project
state owner for persistence, and prototype and implementation work is a
delegated host or user action under existing authority. This reference is the
detailed normative copy of the loop/readiness/ledger; the SKILL workflow is the
summary - keep both in sync.

## 1. Selection record (recorded before iteration work)

| Field | Meaning | Example |
| --- | --- | --- |
| `mode` | The user's chosen approach. | `A - standard design and build` or `B - explore and refine first` |
| `scope` | Feature/task boundary the choice applies to. | `account settings screens: profile, notifications, save confirmation` |
| `instruction_source` | Where the choice came from (user turn, reused record, recovered context). | `user turn 2026-10-20, step-3 prompt` |
| `endpoint` | The delivery endpoint the iteration feeds. | `reviewed handoff to the build stage` |
| `budget` | Up to three concepts and up to three independent evaluation passes by default (at least two non-cosmetic flows); any override carries a recorded reason; every pass counts. | `up to 3 concepts / up to 3 passes` |
| `selection_offer_count` | How many times the choice was offered for this feature; at most once per feature/selection context. | `1` |
| `record_location` | Where the returned record will be persisted (host/user or the project state owner's existing artifact). | `docs/project-state.md decision log (owner to persist)` |
| design_direction | One of the three owner directions: 1a guided premium, 1b creative options, 1c follow my existing design; not-applicable only when no design direction is needed. | 1a |
| mockup_budget | Default 2; hard maximum 4; exactly one under 1a/1c; at least two under 1b; overrides carry a recorded reason. | 2 (max 4; one under 1c) |
| ui_lock | UI consistency lock state: ON for an existing application or in-code design system (default, not asked), OFF only when the user asks for a visual refresh and the override reason is recorded. | ON (existing app; no override) |
| pre_design_binding | For 1c: file name, version, byte size and sha256 of the user-provided pre-design; unspecified items are UNKNOWNs. | brand-kit.fig v4, 128,344 B, sha256 9f... |
| authority_conflict | Recorded source conflict and its resolution; the in-code design system keeps authority unless the user states the pre-design supersedes it for named elements. | in-code tokens win for all elements |
| clickthrough_offer_decision | Offered after implementation: offered, declined or UNRUN; a decline/UNRUN names the unobservable state-hydration/transition defect classes and never changes readiness to PASS. | declined; UNRUN (state hydration/transition) |

Return the record to the host/user or the project's state owner for persistence
in the project's existing step-3 design/state or handoff artifact (for example
its project-state format, design document or prior iteration record); do not
write the project artefact yourself; the host/user or state owner performs any
persistence after receiving the returned content. The record is task-level and survives turn,
session, resume and tool/agent changes. A missing record is recovered from the
surrounding evidence, not read as an opt-out; a later user change is recorded
and honored.

## 2. The nine required loop elements

1. **Evidence-backed brief** - concrete user/journey evidence; UNKNOWNs labeled;
   no invented requirement.
2. **End-to-end experience story** - start, success, failure/recovery, empty,
   permission-denied and timing states with expected outcomes where the feature
   defines them.
3. **Meaningfully different flows** - at least two non-cosmetic candidates
   (default three), each with a hypothesis and what would make it wrong.
4. **Prototype scope and smallest interactive artifact** - included, mocked and
   incomplete parts named; the artifact is the smallest that exercises the
   named interaction; fixtures listed.
5. **Independent reviewer** - a reviewer other than the author inspects and
   exercises the artifact; findings recorded; no self-review claim.
6. **Rendered-UI review** - compare the candidate with the brief and design
   system across hierarchy, layout, typography, spacing, labels, component
   consistency, responsive behavior, focus, keyboard and accessibility, with
   actual per-check evidence.
7. **Per-evaluation record** - question/hypothesis, candidate version, scenario
   and conditions, observation, evidence, finding, disposition, uncertainty.
8. **Disposition and independent retest** - every finding dispositioned; the
   changed or unchanged candidate independently retested before advancing; no
   manufactured change; the handoff preserves flow, content, states, visual
   direction, authority, open items, evidence, budget state and next action.
9. **Defaults, concepts and passes** - up to three concepts and up to three
   independent passes by default (at least two non-cosmetic flows), configurable
   with a recorded reason; every pass counts including unchanged retests; no
   reset on tool/agent switch, resume or rename; approved design preserved;
   effort scaled. The three-concept and three-pass limits are caps/defaults, not
   floors: a small feature may need fewer, with the reason recorded. The
   at-least-two non-cosmetic flows requirement is a minimum, not a cap.

## 3. Readiness and false-completion rules

Declare these **before** evaluation, not after:

- Scenarios, states, input methods and viewports the candidate will be judged
  against.
- Coverage or a justified N/A for negative, boundary, permission-denied,
  error-recovery and state-timing cases.
- Each required check's observable expected outcome, its pass/fail condition
  and the evidence that will establish it.
- The production boundary: whether the work is still an isolated prototype or
  starts real app behavior with API/data/schema integration.

A readiness declaration is **READY** only when:

- Required checks **PASS on the advanced candidate**; a FAIL or an UNRUN check
  cannot be hidden behind other results.
- No unresolved blocking experience failure remains; other findings have
  explicit dispositions.
- Evidence is bound to the candidate version, scenarios, fixtures and design
  baseline in the record.
- Changes made after evaluation started record their reason, decision and
  evidence, and all affected results were invalidated and retested.
- No check was removed, redefined or silently lowered; no threshold changed
  without a recorded decision.
- The declaration distinguishes verified requirements, observations and
  participant evidence; no fabricated personas, quotes, timing, rates or
  results appear; actual-user evaluation is stated if not run.
- The production boundary is respected: prototype work does not claim
  production readiness, and production work waits until the criteria pass.
- Prototype acceptance is live and enforced before READY: transitions named by the story are exercisable; state carries across steps with derived content and real counts; every named non-happy state (empty, invalid, permission-denied/viewer, loading, error, recovery) shows how the user continues; the artifact is fixtures-only with no backend/network/repo change; it is responsive at the declared viewports and keyboard-operable with visible focus. A static image, non-interactive comp or frame sequence whose transitions cannot be exercised is NOT READY with the unexercisable transitions named.
- UI-lock inventory diff: when ui_lock is ON, every component/token/colour/type size/icon/motion in the mockup maps to an existing project element (compose frontend-architecture-mapper and design-system-token-governor); any unmapped element is a finding; an unapproved unmapped element is NOT READY with the element named; a genuinely needed new element is a PROPOSED UI ADDITION routed as a separate design-system-owner decision, never an approved mockup element.

The iteration itself needs **no per-round owner approval**; present the reviewed
prototype on request; after readiness, full delivery continues only under
existing authority and still verifies the **integrated** feature; merge, deploy
and spending authority is unchanged. Otherwise declare **NOT READY**, list
every blocking/unresolved item, and name the **smallest decision** the user can
make (extend budget, accept a recorded limitation, change scope, or stop).
Never silently switch candidate, reset counters, lower criteria, or extend the
budget yourself.

## 4. Budget ledger and invalidation

- The ledger records concepts used and passes used for this feature/selection.
- Every evaluation pass increments the pass count, including an unchanged
  retest; retesting an unchanged candidate is legitimate and must not be
  disguised as a change.
- A tool/agent switch, resume, rename or handoff does not reset the ledger.
- A changed candidate, scenario, fixture or baseline invalidates the affected
  results; they stay invalid until retested. Unaffected results keep their
  binding and are reused, not re-run for ceremony.
- When a budget limit is reached with unresolved work, stop and present the
  smallest decision; if the final budgeted pass already establishes every
  required check, the readiness rules decide and the cap alone is not a blocker;
  never manufacture a pass or continue silently.
## 5a. Retro rules (failure triage, scope, mockup binding)

- When a check fails, classify it as a stale assertion, a product bug, or a wrong metric BEFORE fixing it; record the classification in the record.
- A defect outside the surface under change is a named residual; never fix it by loosening a test or lowering a threshold.
- The approved mockup is bound by sha256 and byte size; the implementation record states that the committed copy matches that binding.

## 5. Accepted-with-disclosure rules

A limitation can be accepted explicitly instead of fixed only when all of the
following are recorded: what is not fixed, why it is acceptable now, who
accepted it and on what evidence, what would reopen it, and the residual risk
visible in the readiness declaration. Accepted limitations never convert an
UNRUN or FAIL check into PASS, never remove a required check, and never claim
user validation that did not happen.

## 6. Worked record template

    feature: <feature/task scope>
    selection: {mode: A|B, design_direction: 1a|1b|1c|not-applicable, mockup_budget: ..., ui_lock: ON|OFF, pre_design_binding: {...}|null, authority_conflict: ..., clickthrough_offer_decision: offered|declined|UNRUN, instruction_source: ..., endpoint: ..., budget: ..., offer_count: 1, record_location: ...}
    brief:
      evidence: [<source, observation>]
      problem_job: ...
      unknowns: [...]
      non_goals: [...]
    story:
      start: ... ; success: ... ; failure_recovery: ... ; empty: ... ; permission: ... ; timing: ...
    candidates:
      - id: A1 ; hypothesis: ... ; would_be_wrong_if: ...
      - id: A2 ; hypothesis: ... ; would_be_wrong_if: ...
    prototype:
      scope_included: [...] ; mocked: [...] ; incomplete: [...] ; fixtures: [...] ; smallest_artifact: ...
    evaluations:
- id: E1 ; mockup_id: M1 ; question: ... ; candidate_version: ... ; scenario: ... ; observation: ... ;
      prototype_acceptance: {exercisable: ..., stateful: ..., non_happy_states: [...], fixtures_only: ..., viewports: [...], keyboard: ...} ;
      ui_lock_inventory_diff: [{element, mapped_to}] ; proposed_ui_additions: [...] ;
      retro_classification: [{check, class: stale_assertion|product_bug|wrong_metric}] ; clickthrough: {offered, decision, unrun_reason} ;
        evidence: ... ; finding: ... ; disposition: ... ; uncertainty: ...
    review:
      reviewer: <independent identity> ; exercised: ... ; checks: [{check, result, evidence}]
    retest:
      candidate_version: ... ; scenario: ... ; result: ... ; invalidated: [...]
    budget: {concepts_used: n, passes_used: m, limit: ...}
    readiness:
      status: READY | NOT READY ; declared_scenarios: [...] ; coverage_or_na: [...] ;
      required_checks: [{check, result, evidence}] ; blocking: [...] ; production_boundary: ... ;
      smallest_decision: ...
    handoff:
      flow: ... ; content: ... ; states: ... ; visual_direction: ... ; authority: ... ;
      open_items: [...] ; evidence_pointers: [...] ; budget_state: ... ; next_action: ...
