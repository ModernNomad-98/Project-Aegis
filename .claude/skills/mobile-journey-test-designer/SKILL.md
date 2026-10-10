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

## Use When

- Use when: asked to design mobile or phone journey test coverage.
- Use when: asked to verify critical journeys on mobile breakpoints.
- Use when: asked to plan mobile touch, dialog, or navigation QA.
- Use when: desktop E2E exists and the team wants the mobile-specific gaps named and scoped.
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
3. **Map journeys to a device/viewport + data matrix.** Which journey is checked on which device or viewport, with which persona and dataset.
4. **Specify pass execution and evidence.** How the pass is run (a manual clickthrough session or Playwright specs — named as handoffs, never executed here) and how evidence is captured, composing `screenshot-evidence-planner`'s naming and masking conventions.
5. **Emit the design** in the Output Format. State what was chosen, why, and the main rejected alternative.

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
- [ ] Evidence conventions follow `screenshot-evidence-planner`; no local naming rules invented.
- [ ] Out-of-scope list is present and names the owning skills.
- [ ] The design claims to drive no browser and execute no pass.

## Gotchas

- Journey QA is not layout correctness: touch, dialogs, and navigation checks are journey behavior; fitting the layout to a viewport is `mobile-viewport-craft`.
- Touch, dialog, orientation, and keyboard behavior are exactly what desktop E2E misses; a design that only lists breakpoints is incomplete.
- This skill must not execute: running the pass is `clickthrough-test-engineer` (live app) or `playwright-e2e-engineer` (permanent specs) — both manual-only.
- Evidence rules come from `screenshot-evidence-planner` (naming, masking, metadata); do not invent parallel conventions.

## Stop Conditions

- No journey or route inventory is supplied or findable → stop and ask for it; a design cannot start from "mobile testing".
- The request becomes a layout redesign ("make the 100vh screen fit phones") → hand off to `mobile-viewport-craft`.
- The request becomes executing a pass on a device or driving a browser → hand off to `clickthrough-test-engineer` *(manual-only)* or `playwright-e2e-engineer` *(manual-only)*.
- The request involves destructive or live-state action → stop and refuse.

## Supporting Files

- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `mobile-viewport-craft`, `clickthrough-test-engineer`, `playwright-e2e-engineer`, and `test-plan-designer`.
- `references/` — None: the design is self-contained.
