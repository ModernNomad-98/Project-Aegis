---
name: design-orchestrator
description: 'One door for UX/UI design work that starts after the design path''s context, classification and design-authority steps: choose exactly one fixed play (design from scratch, improve existing screens, audit UI consistency, hand off a design-system change), name every skill in order before starting, route the design work to the existing UX/UI skills, hand requirements, specification, classification, design-authority recording and manual-only execution to their owners, and leave ONE plain-language design report. Use when asked to design or fix an app''s UI, audit UI consistency, hand off a design-system change, or run a whole UX/UI design pass end to end. Do NOT use for one already-scoped design skill (route straight to it), context verification or change classification, requirements/specification work, writing implementation or tests, QA passes (qa-orchestrator), security scans (security-scan-orchestrator), code review, or driving a browser.'
---

# Design Orchestrator (the design conductor)

Terms used below: **UX** means user experience; **UI** means user interface; **a11y** means accessibility; **play** is one fixed order of skills for one user goal. **Manual-only** means a skill a human must invoke by exact name (its description starts `MANUAL-ONLY; never auto-invoke.`); the consumer overrides it only through the manual-only policy, never here. `docs/paths/design-and-build-ui.md` is the design path guide; **guide steps 1-3** are its context/classification step, its requirements/specification step, and its recorded design-authority step.

## Purpose

A user who wants a UI designed or fixed should not have to know which of the many UX/UI skills to name. This skill is one plain door for that: it asks at most four questions, chooses exactly one of four fixed plays, names every skill it will use in order BEFORE starting, checks which are installed, hands the guide's context/classification, requirements/specification and design-authority steps to their owners rather than performing them, routes the design work to the existing UX/UI skills, and closes with ONE plain-language design report (plus, only when `docs/project-state.md` exists and a recording is authorized, one STATE SNAPSHOT row). It does not design or implement code itself, never drives a browser, never captures screenshots, never invokes a manual-only skill, and hands implementation to the owning stage route.

## Use When

- Use when: the user asks for a whole design pass in plain words — "help me design my app's UI", "fix this screen", "audit our UI for consistency", "hand off this design-system change", "does this design work?".
- Use when: the user is a non-developer who needs the design work chosen and sequenced for them (guided mode), or an engineer who wants one conductor for the same plays (direct mode).
- Use when: the request spans several design steps (for example "review these screens and tell me what to fix first").
- Do NOT use when: the request is exactly one already-scoped design skill ("write the state matrix for this view", "review this design doc", "map this frontend") — route straight to that skill; the conductor is for a user who does not know the next design step.
- Do NOT use when: the requested work is context verification, change classification or scope locking — those are guide step 1 and belong to `agent-startup-context-gate` then `change-classification-gate`.
- Do NOT use when: the request is requirements elicitation or specification writing — those are guide step 2 and belong to `requirements-gathering-facilitator` then `product-spec-writer` (or `tech-spec-writer` for a technical design document).
- Do NOT use when: the ask is implementation, writing code or tests, or driving a browser and capturing screenshots — hand those to the owning implementation/verification route; the conductor is a design door only.
- Do NOT use when: the ask is a QA pass (`qa-orchestrator`), a security scan (`security-scan-orchestrator`), or a code review (`code-reviewer` / `security-pr-reviewer`).

## Inputs to Inspect

1. `docs/project-state.md` if present — the recorded design authority for this change, its revision/snapshot, prior design entries and the project's stage; and the project's own existing design/architecture context when that is where authority lives.
2. The project's accepted specification and acceptance criteria for the affected screens, plus the change classification and approved file set from guide step 1.
3. What is installed: the skills present under the project's skill directory (never assume one is present).
4. The affected interface surface: the screens, routes, components, tokens, states and viewports actually in scope; the design file or screenshot only where one was supplied as the authority.
5. The consumer's evidence and recording conventions: where reports live, who reads the result (`project-orchestrator`, `release-readiness-reviewer`), and any recorded manual-only policy/trigger/override in the consumer's register.
6. The implementation owner named by the project's own stage route (not chosen here); the conductor names the handoff rather than performing it.

## Workflow

**0. Preconditions — guide steps 1-3 (never run, redo or paraphrase them here).** Before any play starts, the change must already carry (1) verified workspace role/context plus a classification with its scope lock; (2) requirements and specification satisfied for the affected screens; and (3) one recorded design authority per affected design decision, in the project's own existing context. If any is missing or unverifiable, STOP the play and hand the request to `project-orchestrator` (the stage-route and state-recording owner), naming the exact gates/owners that must run first: `agent-startup-context-gate` then `change-classification-gate` for step 1; `requirements-gathering-facilitator` then `product-spec-writer` (or `tech-spec-writer`) for step 2; the project's own recorded design authority for step 3. The conductor does not classify, lock scope, gather requirements, write a spec, invent a project file, fabricate a stage or record an authority. Each play's `references/play-orders.md` entry opens with its own "Before starting (guide steps 1-3)" block; the report states which branch was taken.

**1. Intake — at most four plain-language questions.** Ask only: (a) what the screen, flow or product is and where it runs; (b) what the user wants (design from scratch / improve existing screens / audit UI consistency / hand off a design-system change); (c) which existing authority applies (an accepted spec, a design system or file, or the recorded design context) — read it from the repo instead when readable; (d) how hands-on the user wants to be (guided or direct). Do not ask what you can read from the repository. In guided mode ask one at a time and confirm each answer; in direct mode accept a one-line scope and report tersely.

**2. Choose exactly one play and state the order BEFORE starting.** Print the play, every skill in it in order, which are installed, which steps are conditional and which are manual-only handoffs. The fixed orders are in `references/play-orders.md`:
- **Play A — Design from scratch (new screen/flow)**: `ux-design-iteration` **CONDITIONAL** (applies only when the experience direction is unsettled (a settled design is not iterated merely because no iteration choice is recorded); that skill owns the offer and the record, and the conductor neither offers nor re-offers it) -> `edge-state-ux-designer` -> `mobile-viewport-craft` **CONDITIONAL** (only when the interface runs in a web/browser-rendered target and small screens/responsive/touch are in scope; a native mobile/desktop app routes to its platform owner) -> `design-system-token-governor` **CONDITIONAL** (new tokens/components or an existing design system is the authority) -> `accessibility-test-harness` **CONDITIONAL** (interactive controls/forms or an a11y obligation exists) -> implementation handoff. `screenshot-evidence-planner` and `visual-regression-test-designer` are conditional companions only when evidence or visual-regression design is requested, and visual-regression only on a web/browser-rendered target. When the settled direction leaves no design-owning skill, the conductor says plainly that no Aegis skill owns the screen design and hands the actual screen design to the human design owner (or the implementation owner named by the project's own stage route); it never claims a screen was designed.
- **Play B — Improve existing screens**: `frontend-architecture-mapper` **CONDITIONAL** (an existing app with no current route/component/state map; if no surface inventory is findable, report its stop) -> `ux-design-iteration` **CONDITIONAL** (same direction condition) -> `edge-state-ux-designer` -> `mobile-viewport-craft` **CONDITIONAL** (only on a web/browser-rendered target; native apps route to their platform owner) -> `design-review-facilitator` **CONDITIONAL** (only when a reviewable technical design proposal exists — a tech spec/RFC/design doc with problem, proposal, alternatives and cross-cutting concerns; that skill prepares and circulates the pre-read and frames the decision, so a proposal not yet pre-read still applies; otherwise skip and record the condition; if it bounces an incomplete design to `tech-spec-writer`, record the bounce and hand the request to the project's spec route) -> conditional evidence companions (visual-regression only on a web/browser-rendered target) -> implementation handoff.
- **Play C — Audit UI consistency**: `design-system-token-governor` -> `edge-state-ux-designer` -> `mobile-viewport-craft` **CONDITIONAL** (only on a web/browser-rendered target; native apps route to their platform owner) -> `accessibility-test-harness` **CONDITIONAL** (a11y obligation or verification requested) -> `design-review-facilitator` **CONDITIONAL** (an audit of existing UI normally has no reviewable technical design proposal, so skip with the recorded condition unless the audit is turned into one; a bounce goes to the spec route as in Play B) -> conditional evidence companions (visual-regression only on a web/browser-rendered target) -> ONE prioritized consistency report.
- **Play D — Hand off a design-system change**: `design-system-token-governor` -> `design-review-facilitator` **CONDITIONAL** (only with a reviewable technical design proposal for the change (that skill prepares and circulates the pre-read; a proposal not yet pre-read still applies); otherwise skip and record the condition; a bounce goes to `tech-spec-writer`) -> `visual-regression-test-designer` **CONDITIONAL** (only when the interface runs in a web/browser-rendered target; a native mobile/desktop target routes to its appropriate non-web verification owner rather than this web-rendered-state designer) -> `screenshot-evidence-planner` **CONDITIONAL** (before/after evidence will be captured) -> handoff record to the project's own stage/handoff owner through `project-orchestrator`.

A goal that matches none of A-D gets ONE scoping question; never invent a fifth play.

**3. Installed-skill check.** List which play skills are present (check the project's skill directory at use time). The rule is one value, not a gate/advisory classification: **every step of the chosen play applies, except a step the play marks conditional, which applies only when its stated condition holds.** If a step applies and its skill is absent, STOP that play, name the exact skill, say it is not installed, give the selected-skills copy route (the README "Selected skills" allow-list section), and hand the copy and the extension DECISION to the human / `project-orchestrator` (that DECISION is owned by the starter's absent-skill rule and is not written by this conductor). Never invent a skill, substitute another, or call an applicable step n/a to get past it. A conditional step whose condition does not hold is skipped and named with its condition in the report; it is never claimed as passed.

**4. Manual-only handoff — never invoke or chain.** Every routed design step is model-invocable and design-only; only implementation/verification-execution owners may be manual-only (for example `playwright-e2e-engineer`, `clickthrough-test-engineer`, `vite-build-qa-engineer`). For any manual-only handoff, name the exact skill, state what it will do and its scope/limits, and hand it to the human — the conductor does not invoke, chain, simulate or claim it ran. The only delegation route is the consumer's recorded manual-only policy: one standing trigger-scoped override per project, tied to the named trigger in the consumer's recorded policy and naming each exact manual-only skill it covers, with per-run naming fallback (the human names and invokes the exact skill directly). The conductor creates no override and never writes an authorization record itself; when the consumer asks for a recording, it shows a draft entry for the human/`project-orchestrator` to record under existing authority, and never treats a business answer as permission to run a manual-only skill.

**5. Run the design pass once.** Execute the in-scope design steps through the named skills in order; for manual-only handoffs, give exact instructions and wait. Do not implement, write code or tests, edit the design system, drive a browser, capture screenshots or fix anything during the pass. Record what ran, what did not and why; the design authority consumed (with its revision/snapshot); each design output and gap; and any capability gap as UNKNOWN rather than a pass.

**6. Close with ONE report and (only when authorized) ONE record row.** Show the report path and content to the user first. Write the report file only when a current-session instruction explicitly authorizes creating/recording documentation or a content-specific single-use approval is given for that path and content; otherwise leave the report in the conversation and say that no file was written. Append exactly ONE **STATE SNAPSHOT** row to `docs/project-state.md` only when that file exists and a current-session instruction or content-specific single-use approval authorizes the recording; preserve the current stage, point at the report, and show the row before writing. If the file is absent, write the report only and say why no row was written; `project-orchestrator` owns creating it. Never create a second record location, never use a different entry type, and never transcribe an approval the human did not give. Then name the implementation handoff to the project's own stage route (owned by `project-orchestrator`) and stop; the conductor does not choose or perform that implementation.

## Output Format

```
DESIGN REPORT — <app / feature> @ <build|commit> — <date>
Mode: guided | direct        Play: A | B | C | D
Guide steps 1-3: <verified / handed off to which owner — reason>
Skills used (in order): <name — installed | conditional-skipped + condition | manual-only handed to human>
Not used / unavailable: <skill — why, and what is UNKNOWN as a result>
Design authority consumed: <path and revision/snapshot per affected decision>
Designed: <screens/flows/states/viewports covered, with what changed in the design>
Not designed: <what was not, and why — capability gap vs scope decision>
Findings / open decisions:
  [BLOCKING|RESIDUAL|NIT] <title — why — owner who must decide>
Next action: <the single most important next step>
Handoff: implementation owner via project-orchestrator | spec route | owner
```
Then, only if `docs/project-state.md` exists and recording is authorized, exactly one STATE SNAPSHOT row: | SS-<next unused number> | <date> | <current stage preserved> | design pass result + report path; single next action | — use the next unused `SS-*` identifier when the consumer uses the `project-orchestrator` snapshot contract, otherwise follow the consumer's existing snapshot schema; no second record, no invented stage or approval.

## Validation Checklist

- [ ] Guide steps 1-3 were verified as satisfied, or the request was stopped and handed to the exact owner; the conductor did not classify, write a spec or record an authority.
- [ ] At most four intake questions; each needed fact read from the repo instead when possible.
- [ ] Exactly one play chosen; every skill named in order BEFORE starting; conditional steps and their conditions and manual-only handoffs marked.
- [ ] Every step applies except a conditional step whose condition does not hold; an absent applying skill stopped the play and named the skill, the selected-skills copy route and the extension DECISION owner; no substitution and no n/a.
- [ ] No routed design step is treated as manual-only; every manual-only handoff is handed to the human and never invoked or chained.
- [ ] One design pass, one report; no implementation, code/test writing, browser driving, screenshot capture, design-system edit or fixes during the pass.
- [ ] Findings classified and each open decision has the owner who must decide it.
- [ ] Report shown before writing; at most ONE STATE SNAPSHOT row, only when the state file exists and recording is authorized; no second record location.
- [ ] Implementation handoff named through the project's own stage route; the conductor performs no implementation.
- [ ] No claim of browser/screenshot capability, executed evidence or a built design beyond what the evidence shows.

## Gotchas

- A goal that matches none of A-D is not a play: ask one scoping question; do not invent a fifth order.
- An absent applying skill is a stop, not an invitation to improvise: name it, give the selected-skills copy route, hand the extension DECISION to `project-orchestrator`.
- A manual-only skill named in the report is not authorization: the human invokes it directly; the conductor never runs it.
- Skipping a guide step silently is a false green: if steps 1-3 are not met, stop and hand off; do not paper over a missing spec or authority with a confident design.
- "Review this design" may not be the design-doc review: `design-review-facilitator` reviews a technical design proposal, not screens; a screen review is routed through the play steps.
- The report is the evidence and the state row is the pointer — never duplicate the report inside `docs/project-state.md`.
- A conditional step is skipped with its stated condition, never silently dropped and never claimed as passed.
- A design pass that could not verify a rendered result records the capability gap as UNKNOWN; no browser or screenshot support is assumed.

## Stop Conditions

- Guide step 1 (verified context/classification) is missing or unverifiable -> stop and hand the request to `project-orchestrator`, naming `agent-startup-context-gate` and `change-classification-gate`.
- Guide step 2 (requirements/specification) is missing for the affected screens -> stop and hand to `requirements-gathering-facilitator` / `product-spec-writer` (or `tech-spec-writer`) through `project-orchestrator`; never design against an invented requirement.
- Guide step 3 (one recorded design authority per affected decision) is missing -> stop and hand to `project-orchestrator`; never invent a project file, stage or authority.
- A play step applies and its skill is absent -> stop that hop, name the exact skill, give the selected-skills copy route and hand the extension DECISION to the human/`project-orchestrator`; never substitute or call the step n/a.
- A manual-only skill is needed -> name it and hand it to the human; the conductor never invokes, chains, simulates or records authorization for it; a business answer is not permission.
- The request needs implementation, code/test writing, browser driving or screenshot capture -> hand to the owning implementation/verification route and stop; the conductor designs only.
- The user asks for a ready design review of code/mockups with no reviewable technical design proposal -> route to the appropriate play step or to `tech-spec-writer`; do not run `design-review-facilitator` on something it cannot review.
- `design-review-facilitator` bounces an incomplete design to `tech-spec-writer` -> record the bounce, hand the request to the project's spec route through `project-orchestrator`, and stop.
- The requested change needs a design authority the project has not recorded, or the user asks the conductor to decide it -> stop and ask; design authority is the project's, not the conductor's.
- A second record location or a second report is requested -> refuse and keep ONE report plus at most ONE STATE SNAPSHOT row in the existing state file.

## Supporting Files

- `references/play-orders.md` — the four fixed plays, each opening with its "Before starting (guide steps 1-3)" block, plus conditional steps, manual-only handoffs and fallback/stop rules.
- `evals/evals.json` — behavior cases for the plays, guide-step handoffs, absent-skill recovery, manual-only handoff and the refusal paths (static specification only; evals do not run on pull requests).
- `evals/trigger-evals.json` — discrimination against `project-orchestrator` (journey vs design pass), `ux-design-iteration` (iteration offer vs whole pass), `edge-state-ux-designer` (state matrix vs full pass), `design-review-facilitator` (design-doc review vs pass), `design-system-token-governor` (token governance vs pass), `qa-orchestrator` (QA pass) and `security-scan-orchestrator` (security scan).
