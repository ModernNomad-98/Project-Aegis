---
name: mobile-journey-test-designer
description: 'Designs mobile-journey QA coverage: which critical journeys to verify on phone breakpoints, the touch interactions, dialogs, navigation, orientation, keyboard, and safe-area checks each journey needs, and how the pass is executed and evidenced. Produces the coverage design only — drives nothing; layout correctness stays with mobile-viewport-craft. Use when asked to design mobile/phone journey test coverage, verify critical journeys on mobile breakpoints, or plan mobile touch/dialog/navigation QA. Do NOT use for layout or viewport correctness design (mobile-viewport-craft), executing a live clickthrough (clickthrough-test-engineer), implementing permanent E2E specs (playwright-e2e-engineer), or a general per-change test plan (test-plan-designer).'
---

# Mobile Journey Test Designer

**Reading key:** QA is quality assurance; E2E is end-to-end; a breakpoint is a
viewport width at which a layout changes; the safe area is the screen region
not covered by notches, home indicators, or browser chrome. A journey is a
user path through the product (for example sign-up to first invoice), and a
pass is one execution of the planned checks.

## Purpose

Design mobile-journey QA coverage: which critical journeys to verify on
phone breakpoints, the touch interactions, dialogs, navigation, orientation,
keyboard, and safe-area checks each journey needs, and how the pass is
executed and evidenced. It is the mobile counterpart that
`mobile-viewport-craft` (layout) explicitly does not own; it drives nothing.
For list–detail journeys it also specifies the select → inspect detail → return
checks and the evidence that keeps the visible selected row, the accessible
selection state and the detail identity in agreement.

## Use When

- Use when: asked to design mobile or phone journey test coverage.
- Use when: asked to verify critical journeys on mobile breakpoints.
- Use when: asked to plan mobile touch, dialog, or navigation QA.
- Use when: desktop E2E exists and the team wants the mobile-specific gaps named and scoped.
- Use when: the journey includes a list → detail pattern where the selection, a
  focused row and the detail shown can disagree — adjacent or near-duplicate
  IDs, filtering, and the return to the list.
- Do NOT use when: the ask is layout or viewport correctness design (fitting the layout to phone screens) — that is `mobile-viewport-craft`.
- Do NOT use when: the ask is executing a live clickthrough — that is `clickthrough-test-engineer` *(manual-only)*.
- Do NOT use when: the ask is implementing permanent E2E specs — that is `playwright-e2e-engineer` *(manual-only)*.
- Do NOT use when: the ask is a general per-change test plan — that is `test-plan-designer`.

## Inputs to Inspect

1. The critical journeys and routes: which user paths the product cannot afford to break.
2. The responsive surfaces those journeys touch, and their breakpoints.
3. `mobile-viewport-craft`'s layout spec if present — what layout correctness it already assumes or proves.
4. Existing E2E and clickthrough coverage, so the design names gaps rather than duplicating.
5. Personas, devices, and breakpoints the product actually targets.
6. Network and offline considerations that hit mobile (flaky connections, offline states).

## Workflow

1. **Identify the critical journeys.** Name the journeys a mobile regression would break and why they are critical; rank them.
2. **Enumerate mobile-specific checks per journey.** Breakpoints, touch (tap targets, gestures, long-press), dialogs and toasts, navigation (back, tabs, deep links), orientation change, keyboard (on-screen, focus, dismissal), and safe-area behavior. These are the checks desktop E2E typically misses.
3. **Specify the list–detail interaction checks.** For every named journey that
   uses a list → detail pattern, specify: select → inspect detail → return,
   recording the visible selected row's identity, the detail's identity and the
   restored list position and focus at each step; where the list has search or
   filtering, filtering (the result-set identity, the retained filter/query,
   and the restored position and focus after return) and no results and
   recovery (the honest zero-match state distinguished from loading and from an
   error, and clearing or correcting the query restoring the previous result
   set and context) — a journey with no filtering feature records those checks
   as not applicable instead of inventing them; adjacent IDs selected by touch
   and keyboard (tap row n and row n+1, and use the keyboard arrows and Enter
   where the widget exposes them, checking the detail identity each time);
   and the agreement of the visible selected row, the accessible
   selection semantics where the widget exposes them, and the detail identity —
   for a list that is plain link navigation (activating a row navigates to a
   detail page rather than selecting in a composite widget), compare the
   activated link's identity and the return context instead of demanding
   persistent selection state; only a widget that models selection and exposes
   no selection state records that as a gap, not a pass. Distinguish focus from
   selection: a row with the keyboard focus ring is not necessarily the
   selected row, so include a correct control example (focus on one row while
   the selected row and the detail show the same identity) that a reviewer must
   accept, beside the seeded mismatch (the selected row's identity differs from
   the detail's) that must be flagged with visible evidence. State positioning
   and focus restoration explicitly, including what is not restored. Layout
   correctness stays with mobile-viewport-craft; the zero-match state design
   stays with edge-state-ux-designer; execution stays with the manual-only
   owners named in this skill's Use When section; step 5 specifies the handoff.
4. **Map journeys to a device/viewport + data matrix.** Which journey is checked on which device or viewport, with which persona and dataset.
5. **Specify pass execution and evidence.** How the pass is run (a manual clickthrough session or Playwright specs — named as handoffs, never executed here) and how evidence is captured, composing `screenshot-evidence-planner`'s naming and masking conventions.
6. **Emit the design** in the Output Format. State what was chosen, why, and the main rejected alternative.

## Output Format

Emit the design in the conversation (nothing is written to the repo):

```
MOBILE JOURNEY QA DESIGN — <app>
Critical journeys:
  <name> — why critical — <rank>
Mobile check matrix (per journey):
  breakpoints | touch | dialogs | navigation | orientation | keyboard | safe area
Device & data matrix:
  <journey> × <device/viewport> × <persona/data>
List-detail checks (per list-detail journey):
  select → inspect detail → return | filtering and no results and recovery
  only where the journey has a filter or search, else "n/a" | adjacent IDs by
  touch and keyboard | visible selected row = accessible selection = detail
  identity, or activated link identity = detail identity for plain link
  navigation | focus vs selection (correct control included)
Pass execution:
  <who runs the pass: manual clickthrough → clickthrough-test-engineer;
   permanent specs → playwright-e2e-engineer — named, not executed here>
Evidence:
  <capture rules follow screenshot-evidence-planner naming/masking/metadata>
Out of scope:
  layout correctness → mobile-viewport-craft; spec implementation → playwright-e2e-engineer;
  live execution → clickthrough-test-engineer; per-change plan → test-plan-designer
Chosen / why / rejected: <the key choices, the reason for each, and the main
  rejected alternative>
```

## Validation Checklist

- [ ] The named journeys are the critical ones, each with a why-critical reason.
- [ ] Mobile-specific checks (breakpoints, touch, dialogs, navigation, orientation, keyboard, safe area) are enumerated per journey.
- [ ] The device/viewport + data matrix is named.
- [ ] For each list-detail journey, select → inspect detail → return is
      specified with the visible selected row, the accessible selection
      semantics where the widget exposes them, and the detail identity required
      to agree; for plain link navigation the activated link identity is
      compared with the detail identity instead, and a gap is recorded only
      where a widget models selection and exposes none.
- [ ] Adjacent IDs are selected by touch and keyboard, and a correct control
      separates focus from selection so a reviewer cannot pass by flagging
      every focused row.
- [ ] Where the journey has a filter or search, filtering and no-results
      recovery are covered, with the restored result set, list position and
      focus checked; otherwise those checks are recorded not applicable.
- [ ] Evidence conventions follow `screenshot-evidence-planner`; no local naming rules invented.
- [ ] Out-of-scope list is present and names the owning skills.
- [ ] The design claims to drive no browser and execute no pass.

## Gotchas

- Journey QA is not layout correctness: touch, dialogs, and navigation checks are journey behavior; fitting the layout to a viewport is `mobile-viewport-craft`.
- Touch, dialog, orientation, and keyboard behavior are exactly what desktop E2E misses; a design that only lists breakpoints is incomplete.
- This skill must not execute: running the pass is `clickthrough-test-engineer` (live app) or `playwright-e2e-engineer` (permanent specs) — both manual-only.
- Evidence rules come from `screenshot-evidence-planner` (naming, masking, metadata); do not invent parallel conventions.
- A focus outline is not a selection bug: the correct control is focus on one
  row while a different selected row and a detail with the same identity are
  shown; a reviewer that flags every focused row fails the calibration.
- A highlighted row 43 with a detail showing 44 is the seeded mismatch; rows
  that look alike hide it unless the visible selected row, the accessible
  selection state and the detail identity are compared, which is why adjacent
  IDs are part of the check.
- A zero-match search is not loading and not an error: include it as its own
  state and check that clearing the query restores the list, position and
  focus rather than leaving a stale empty view.

## Stop Conditions

- No journey or route inventory is supplied or findable → stop and ask for it; a design cannot start from "mobile testing".
- The request becomes a layout redesign ("make the 100vh screen fit phones") → hand off to `mobile-viewport-craft`.
- The request becomes executing a pass on a device or driving a browser → hand off to `clickthrough-test-engineer` *(manual-only)* or `playwright-e2e-engineer` *(manual-only)*.
- The request involves destructive or live-state action → stop and refuse.

## Supporting Files

- `evals/evals.json` — trigger + behavior cases, including the list-detail
  interaction checks (select/inspect/return, filtering, no-results recovery,
  adjacent IDs, focus vs selection with a correct control).
- `evals/trigger-evals.json` — discrimination against `mobile-viewport-craft`,
  `clickthrough-test-engineer`, `playwright-e2e-engineer`, and
  `test-plan-designer`.
- `references/` — None: the design is self-contained.
