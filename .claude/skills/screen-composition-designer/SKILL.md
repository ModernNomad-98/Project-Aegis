---
name: screen-composition-designer
description: 'Design the screen arrangement for a supplied brief and applicable design authority: name the primary task, what is prominent on entry and why, the order of content and actions on phone and desktop, what can be deferred, and one complete interaction with a return or recovery state, then explain the choice against the brief. Use when a brand, palette, spec or approved direction is supplied but the arrangement for a screen or flow is missing or unsettled. Do NOT use for a whole design pass (design-orchestrator), the iteration method''s offer or concept exploration (ux-design-iteration), a narrow layout or breakpoint defect in an existing screen (mobile-viewport-craft), non-happy-state matrices (edge-state-ux-designer), token governance (design-system-token-governor), implementation or browser execution (hand to the owning route), requirements/specification work, or approving a design.'
---

# Screen Composition Designer

Terms used below: **UX** means user experience; **UI** means user interface; **a11y** means accessibility; **composition** means the arrangement of a screen or flow (what is present, in what order, and with what prominence); **design authority** means the project's recorded source for a design decision plus the revision or snapshot actually consumed. This skill is read-only advice: it returns one arrangement in the conversation and writes nothing.

## Purpose

A brand, a palette, a design system or an approved visual direction can settle how a screen looks while the screen's workflow — its primary task, what is prominent on entry, the order of content and actions, and what can be deferred — is still undefined. The current design path hands that gap to whoever is implementing, so the arrangement gets decided by accident in code, or not at all.

This skill closes that gap with exactly one job: given a supplied brief and the applicable, recorded design authority, it returns ONE buildable screen arrangement and explains the choice against the brief. The deliverable is design advice in the conversation — a short ordered outline or annotated wireframe description naming the primary task, entry prominence and why, phone and desktop content and action order, what can be deferred, and one complete interaction with a return or recovery state. It is advice, not approval: it never implements, approves, launches a browser, writes product files or claims a rendered check passed. It preserves the iteration method's ownership (`ux-design-iteration`), the approved design system / UI lock, and mobile layout craft (`mobile-viewport-craft`).

## Use When

- Use when: a brief supplies a brand, palette, design system, spec or approved direction, and the primary task, entry prominence, or content and action order for a screen or flow is missing or unclear.
- Use when: the project's recorded design authority settles styling (or an approved composition covers a neighbouring screen) but the arrangement for this screen is a missing decision.
- Use when: a dashboard or overview question asks what should lead when monitoring is the job — several leading signals are allowed and often correct.
- Do NOT use when: the request is a whole design pass (`design-orchestrator`), the iteration method's one offer or concept exploration (`ux-design-iteration`), a narrow layout, breakpoint, touch-target or scroll defect in an existing screen (`mobile-viewport-craft`), a non-happy-state matrix (`edge-state-ux-designer`), token governance or the design system's one source of truth (`design-system-token-governor`), mapping an existing app before a change (`frontend-architecture-mapper`), designing the accessibility verification (`accessibility-test-harness`), whole-journey or stage routing (`project-orchestrator`), review of a technical design document (`design-review-facilitator`), requirements or specification writing, or anything that implements, browses, captures, files or approves.

## Inputs to Inspect

1. The supplied brief — quote it and name its source. The brief is the requirement; do not invent requirements beyond it.
2. The recorded design authority for each affected decision, with its revision or snapshot: a design file, wireframe, approved composition, design system or tokens, or the project's own state record. Cite what you consumed; never re-derive or invent an authority.
3. Which decisions the supplied material actually settles — styling only, layout only, or workflow. A palette settles colour and typography; it does not settle the workflow or the screen's order.
4. The target viewports and input methods named in the brief (phone and desktop; touch and keyboard). Where the brief is silent, state the assumption you use instead of silently choosing one.
5. The approved design system / UI lock and any component constraints that limit the arrangement — read-only; this skill proposes within them and does not change them.
6. The project's iteration status if present (Standard / Explore / declined / unanswered) — consumed as recorded, never re-offered and never converted into a new question by this skill.

If an input is missing or unreadable, say which one and stop rather than inventing it.

## Workflow

1. Confirm the request is in scope; if not, stop and name the exact neighbour owner from **Use When**.
2. List the known design decisions with their authority and revision, and mark which are already settled. An approved composition or wireframe is reused; this skill covers only the missing decision.
3. State the primary task in one sentence — the one job this screen does for its user.
4. Decide what is prominent on entry and why. Entry prominence must fit the job: an intentional welcome or overview screen is allowed when the brief makes it the job, and a monitoring dashboard may lead with several signals. There is no universal "one primary button first" rule.
5. Order content and actions for phone, then for desktop; separate primary, secondary and deferred; say what is deferred and why.
6. Walk one complete interaction with real-sized fictional sample content: entry → action(s) → result → return or recovery (back or cancel, failed save, empty or no results, retry). Invent no product data beyond a clearly fictional sample, and do not design a full state matrix — states appear only where the arrangement needs a return or recovery path.
7. Test the arrangement against the brief's job, audience and constraints. Record unresolved decisions and conflicts instead of guessing.
8. Re-check boundaries: if the request has turned into implementation, browsing, screenshot capture, file alteration, an approval request, multiple concepts or a direction choice, a narrow layout defect, a state matrix, token work or requirements work, stop and hand it to the owner named in **Use When**.
9. Return the arrangement in the conversation only, using **Output Format**; do not write files.

## Output Format

```
ARRANGEMENT — <screen/flow> @ <brief/authority revision>
- Primary task: <one sentence>
- Entry (phone): <first thing + why>; Entry (desktop): <first thing + why>
- Order (phone): 1 <content/action> [primary|secondary] ... (deferred marked)
- Order (desktop): 1 <content/action> [primary|secondary] ... (deferred marked)
- Deferred: <what and why>
- One interaction: entry → action → result → return/recovery, with sample content
- Why this fits the brief: <quoted brief fact → design consequence>
- Authority consumed: <path/source + revision/snapshot per decision accepted>
- Unresolved / open decisions: <items the project's design authority must decide, or none>
- Status: design advice only; not approved, not implemented; no rendered verification claimed (UNRUN where relevant)
- Handoff: the project's design authority for approval; implementation owner named by the project's own stage route
```

Keep it short enough to act on: an ordered outline or annotated wireframe description is sufficient. Mark any claim that would need a rendered run as UNRUN, never as passed.

## Validation Checklist

- [ ] One job only — an arrangement with rationale; no requirements, spec, code, tests, browser run or file write.
- [ ] Every settled decision is cited with its authority and revision and was not redrawn.
- [ ] Primary task stated in one sentence.
- [ ] Entry prominence stated with a reason that fits the job (an overview or welcome screen is allowed with a reason; no universal primary-button claim).
- [ ] Phone and desktop orders both given, with primary and secondary marked and deferral explicit.
- [ ] One complete interaction includes a return or recovery state, with clearly fictional sample content.
- [ ] Rationale ties quoted brief facts to design consequences.
- [ ] Unresolved decisions and authority conflicts surfaced, not guessed.
- [ ] Boundaries held: no implementation, browser, screenshot, file write, approval, concept exploration or layout-fix claim.
- [ ] Output returned in the conversation only; UNRUN labelled where relevant.

## Gotchas

- A brand, palette or design system is not an arrangement: it can settle styling while the workflow is still open. Do not let it skip the missing decision.
- A polished welcome screen is not automatically the primary task; justify entry prominence against the job.
- "Make it pretty" is styling (the design system), not composition; "make it usable" may be composition.
- A narrow bug report ("the save button hides under the keyboard", "tap targets overlap") is layout craft, not a composition brief — route it to `mobile-viewport-craft`.
- Multiple concepts or a direction choice are iteration work — `ux-design-iteration` owns its one offer; never repeat, reopen or pre-empt it.
- A dashboard's job can justify several leading signals; do not impose a universal primary-button rule.
- Citing an approved wireframe means preserving it, not redrawing or re-ranking it.
- Answering a request to implement, record or approve with "yes" is a boundary failure: those are other owners' acts.
- Static presence of an eval case is not evidence of behaviour; an UNRUN rendered check is never a pass.

## Stop Conditions

- Stop and hand off when the required design authority is missing, unreadable or stale — never invent one.
- Stop and refuse when the request is implementation, code or test writing, browser driving, screenshot capture or any file write; name the owning route and write nothing.
- Stop and refuse when the request asks this skill to approve its own arrangement or to record or write it as the approved design; name the project's design authority as the approver.
- Stop and hand off when the request is a whole design pass (`design-orchestrator`), the iteration offer or concepts (`ux-design-iteration`), a state matrix (`edge-state-ux-designer`), tokens or design system (`design-system-token-governor`), requirements or spec (`requirements-gathering-facilitator`, `product-spec-writer`), a narrow layout defect in an existing screen (`mobile-viewport-craft`), app mapping (`frontend-architecture-mapper`), an a11y verification design (`accessibility-test-harness`), a technical design-doc review (`design-review-facilitator`), or a whole journey and stage route (`project-orchestrator`).
- Stop when the brief and the authority conflict and the conflict cannot be resolved without a decision: name it for the project's design authority; do not pick a side.
- Stop when a supplied "approved composition" is claimed but cannot be read or verified: treat the authority as missing.

## Supporting Files

- `evals/evals.json` — the behaviour cases (happy path, edge, should-not-trigger, refusal) with observable assertions; static specification only, no runner executes them on a pull request.
- `evals/trigger-evals.json` — two-way trigger discrimination against the nine neighbouring skills.
- No `references/` file exists: the one job needs its boundaries, workflow and output shape on every call, and splitting a single-pass procedure would either restate this file or hide operative material from the call.
