# Play orders — the four fixed design plays

These are the ONLY orders `design-orchestrator` runs. Each was verified against the named skills' own "Use when"/"Do NOT use when"/handoff statements at the implementation base. Do not invent a fifth order; if a goal matches none, ask one scoping question.

The design path guide is `docs/paths/design-and-build-ui.md`. Its **steps 1-3** are the precondition for every play below: step 1 verified context plus change classification/scope lock (`agent-startup-context-gate` then `change-classification-gate`); step 2 requirements/specification (`requirements-gathering-facilitator` then `product-spec-writer`, or `tech-spec-writer` where the artifact is a technical design doc); step 3 one recorded design authority per affected design decision in the project's own existing context. The conductor never runs, redoes or paraphrases those steps; when they are missing it stops and hands the request to `project-orchestrator` (the stage-route and state-recording owner) naming the exact owner that must run first.

## Play A — Design from scratch (new screen or flow)

**Before starting (guide steps 1-3):** step 1 must be verified; this is the guide's "started from a brief" case, so step 2 must be satisfied or handed off to the requirements/specification route first — if the brief already answers audience, the job, "done" and constraints, step 2 continues on the recorded authority and the play records that; step 3's design authority must be recorded. If any is missing, stop-and-hand-off as above; the play does not start.

1. `ux-design-iteration` — **CONDITIONAL**: applies only when the experience direction is unsettled or no recorded choice exists; that skill owns the one up-front offer and the record, and the conductor neither offers nor re-offers it.
2. `edge-state-ux-designer` — applies (the per-view state matrix for each new view).
3. `mobile-viewport-craft` — **CONDITIONAL** (the target includes small screens / responsive / touch).
4. `design-system-token-governor` — **CONDITIONAL** (new tokens/components or an existing design system is the authority; governance design only).
5. `accessibility-test-harness` — **CONDITIONAL** (interactive controls/forms, or an a11y obligation/request exists; otherwise skip with the recorded condition — no silent n/a).
6. Handoff: the implementation owner selected by the project's own stage route (owned by `project-orchestrator`); the conductor names it and stops. `screenshot-evidence-planner` and `visual-regression-test-designer` are **CONDITIONAL** companions only when evidence/visual-regression design is requested.

## Play B — Improve existing screens

**Before starting (guide steps 1-3):** step 1 must be verified; step 2 is normally satisfied by the existing accepted spec/design authority — if absent, stop-and-hand-off; step 3's design authority must be recorded. The play does not start otherwise.

1. `frontend-architecture-mapper` — **CONDITIONAL** (an existing app with no current route/component/state map; it requires a findable surface inventory and stops and asks when there is none — the conductor reports that stop rather than improvising one).
2. `ux-design-iteration` — **CONDITIONAL** (same condition as Play A: the experience direction is unsettled or no recorded choice exists; the skill owns the offer/record).
3. `edge-state-ux-designer` — applies.
4. `mobile-viewport-craft` — **CONDITIONAL** (responsive/touch surface is in scope).
5. `design-review-facilitator` — **CONDITIONAL**: applies only when a **reviewable technical design proposal** exists (a tech spec/RFC/design doc with problem, proposal, alternatives and cross-cutting concerns, per its Inputs) and its decision/pre-read are set; the facilitator reviews the design DOC, not screens. With no such proposal, skip it and record the condition. If it bounces an incomplete design to `tech-spec-writer`, the conductor records the bounce and hands the request to the project's spec route through `project-orchestrator` — it never runs `tech-spec-writer` itself.
6. `visual-regression-test-designer` — **CONDITIONAL** (rendered-UI baseline/regression coverage is in scope); `screenshot-evidence-planner` — **CONDITIONAL** (captures will be used).
7. Handoff to the implementation owner (never implemented here).

## Play C — Audit UI consistency

**Before starting (guide steps 1-3):** step 1 must be verified; step 2 is normally satisfied by the existing spec/design authority — if absent, stop-and-hand-off; step 3's design authority must be recorded. The play does not start otherwise.

1. `design-system-token-governor` — applies (token / one-source-of-truth drift; design only).
2. `edge-state-ux-designer` — applies (state coverage gaps).
3. `mobile-viewport-craft` — **CONDITIONAL** (responsive/touch surface in scope).
4. `accessibility-test-harness` — **CONDITIONAL** (an a11y obligation or verification is requested).
5. `design-review-facilitator` — **CONDITIONAL**: an audit of existing UI normally has no **reviewable technical design proposal**, so this step is normally skipped with the recorded condition; it applies only if the audit is turned into a reviewable proposal (spec/RFC/design doc with alternatives) before the step. A bounce to `tech-spec-writer` is recorded and handed to the spec route as in Play B.
6. `visual-regression-test-designer` — **CONDITIONAL**; `screenshot-evidence-planner` — **CONDITIONAL** (evidence will be captured).
7. ONE prioritized consistency report; no fixes applied during the pass.

## Play D — Hand off a design-system change

**Before starting (guide steps 1-3):** step 1 must be verified; step 2 is satisfied by the change proposal/specification or handed off; step 3's design authority must be recorded. The play does not start otherwise.

1. `design-system-token-governor` — applies (change governance and migration design).
2. `design-review-facilitator` — **CONDITIONAL**: applies only when the design-system change has a **reviewable technical design proposal** (design doc/RFC with proposal, alternatives and cross-cutting concerns); otherwise skip and record the condition. A bounce to `tech-spec-writer` is recorded and handed to the spec route; the conductor never runs it.
3. `visual-regression-test-designer` — applies (coverage for the change's rendered states).
4. `screenshot-evidence-planner` — **CONDITIONAL** (before/after evidence will be captured).
5. Handoff record to the project's own stage/handoff owner through `project-orchestrator`; the conductor states what is handed off and stops.

## Conditional-companion and manual-only rules

- A conditional step whose condition does not hold is skipped and named with its condition in the report; it is never claimed as passed and never silently dropped.
- No routed design skill is manual-only (all routed design steps above are model-invocable and design-only). Manual-only skills appear only as implementation/verification EXECUTION owners and are handed to the human: name the exact skill, state its scope/limits, and let the human invoke it. The conductor never invokes, chains, simulates or claims it ran; no new override authority is created.
- The consumer's recorded manual-only policy is the only delegation route: one standing trigger-scoped override per project naming each exact manual-only skill it covers, with per-run naming fallback (the human names and invokes the exact skill directly). A business answer is not permission.
- Fallback when a needed routed skill is absent: stop that hop, name the exact skill, give the selected-skills copy route and hand the extension DECISION to the human/`project-orchestrator`.
- The conductor records what ran, what was skipped conditionally and what remains UNKNOWN; it never claims a design was built, a browser was driven, a screenshot was captured or a manual-only skill ran.
