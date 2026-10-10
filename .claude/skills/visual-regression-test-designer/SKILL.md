---
name: visual-regression-test-designer
description: 'Designs visual/pixel-regression test coverage for a web UI: which UI states are stable enough to capture, the deterministic baseline and diff/compare mechanics, the positive snapshot-selection rule with explicit update review, and the deterministic state-rendering slice for fixture/render surfaces. Produces the coverage design only — captures and compares nothing. Use when asked to design visual regression coverage, decide which screens or states to snapshot, define a baseline/diff workflow, or govern snapshot selection and updates. Do NOT use for the evidence naming/masking/storage policy (screenshot-evidence-planner), a per-change test plan (test-plan-designer), automation tooling design (qa-automation-architect), curation of existing tests (regression-suite-curator), or writing Playwright specs (playwright-e2e-engineer).'
---

# Visual Regression Test Designer

**Reading key:** UI is user interface; CI is continuous integration. A baseline
is the approved set of reference snapshots; a diff is the pixel-level
comparison of a fresh capture against that baseline. Snapshot selection means
choosing which states earn a capture; update review means a human examines and
approves a baseline change before it becomes the new baseline.

## Purpose

Produce the visual/pixel-regression coverage DESIGN for a web UI: which states
are stable enough to capture, the deterministic baseline + diff/compare
mechanics, the positive snapshot-selection rule with explicit update review,
and the deterministic state-rendering slice for fixture/render surfaces. The
deliverable tells a later engineer what to capture, how to compare it, and
what to do when a diff appears; this skill captures and compares nothing.

## Use When

- Use when: asked to design visual or pixel-regression coverage for a web UI.
- Use when: asked which screens or UI states should be snapshotted.
- Use when: asked to define a baseline capture, diff/compare, or baseline-update workflow.
- Use when: asked to govern snapshot selection or snapshot updates for an existing visual suite.
- Do NOT use when: the ask is the evidence naming, masking, metadata, or storage policy — that is `screenshot-evidence-planner`.
- Do NOT use when: the ask is a per-change test plan across layers — that is `test-plan-designer`.
- Do NOT use when: the ask is automation tooling or framework design (which runner, how fixtures are structured, CI tiers) — that is `qa-automation-architect`.
- Do NOT use when: the ask is promoting, retaining, demoting, or retiring existing tests — that is `regression-suite-curator`.
- Do NOT use when: the ask is writing or running Playwright/E2E specs — that is `playwright-e2e-engineer` *(manual-only)*.

## Inputs to Inspect

1. The UI surface or route inventory: screens, routes, dialogs, and the user-visible states that matter.
2. The existing evidence policy (`screenshot-evidence-planner` output if present) — the naming, masking, and storage rules any capture plan must compose.
3. Existing snapshot tooling and suites in the repo, if any, and what they already cover.
4. Stable vs dynamic data sources: which content is seeded or fixtured, which is live (clocks, tickers, feeds, external images).
5. CI configuration: where suites can run and how often.
6. Risk-critical states: what a regression here would cost, to rank capture priority.

## Workflow

1. **Inventory the critical states.** List the screens, routes, dialogs, and states whose appearance a regression would break; rank them by risk.
2. **Classify each state's stability.** For each state, name its data source and rendering inputs: fixed fixtures vs live clock/locale/animation-driven content. Unstable content cannot be snapshotted as-is.
3. **Select positive snapshot candidates.** Apply the positive rule: snapshots are reserved for stable, meaningful outputs. Each candidate must state what a diff on it would prove. Meaningless or unstable captures are excluded, never weakened.
4. **Specify the deterministic state-rendering slice.** For each selected state, name the fixture/render surface that makes it deterministic: test-only or local routes, seeded data, fixed viewport, fixed timezone and locale, frozen animation. This is the design, not the implementation.
5. **Define the baseline + diff mechanics.** State where the baseline lives, how captures compare (thresholds, ignored regions, anti-aliasing if the repo tooling supports them), and the explicit update-review gate: any baseline change is reviewed and approved by a named human before it becomes the new baseline — never a blanket update-all.
6. **Place the CI gates.** Name which suites run on pull request, merge, or schedule, and which are release-blocking.
7. **Emit the design** in the Output Format. State what was chosen, why, and the main rejected alternative.

## Output Format

Emit the design in the conversation (nothing is written to the repo):

```
VISUAL REGRESSION COVERAGE DESIGN — <app / surface>
Stable states to capture:
  <name> — data <fixture source> — viewport <fixed size> — why a diff here matters
Baseline & diff mechanics:
  baseline <location / how captured> — compare <tool, thresholds, regions> —
  update review <named human gate; never update-all>
Snapshot selection rule:
  <positive rule applied: stable + meaningful; what each kept capture proves>
  Rejected: <candidates excluded and why>
Deterministic rendering:
  <test-only routes, seeded data, fixed timezone/locale, frozen animation per state>
CI placement:
  <suite → PR / merge / schedule tier; which are release-blocking>
Out of scope:
  evidence policy → screenshot-evidence-planner; tooling design → qa-automation-architect;
  spec implementation → playwright-e2e-engineer; suite curation → regression-suite-curator
Chosen / why / rejected: <the key choices, the reason for each, and the main
  rejected alternative>
```

## Validation Checklist

- [ ] Every named state carries its determinism: data source and viewport are named.
- [ ] Snapshots are restricted to stable + meaningful outputs; unstable or meaningless captures are excluded with a reason.
- [ ] The baseline update review is explicit (a named human gate); no blanket update-all.
- [ ] Deterministic rendering is specified per state (routes, fixtures, timezone/locale, animation).
- [ ] CI placement is named per suite.
- [ ] Out-of-scope list is present and names the owning skills.
- [ ] The design claims to capture, compare, or run nothing.

## Gotchas

- Unstable content (clocks, tickers, feeds, external images) flaked into snapshots is the classic failure: every run diffs, nobody reads the diffs anymore.
- Timezone, locale, font-rendering, and animation drift produce diffs that look like regressions; freeze or fixture them, or exclude the state.
- Baseline drift: updating the baseline whenever a diff appears turns the suite into a recording of the current bugs. The update-review gate keeps a diff meaningful.
- "Update all baselines" after any UI change masks the one real regression; it must require explicit review.
- This skill must not reproduce `screenshot-evidence-planner`'s policy — naming, masking, metadata, and storage are that skill's job; reference it, never rewrite it.

## Stop Conditions

- No UI surface or route inventory is supplied or findable → stop and ask for it; a coverage design cannot start from "our app".
- The request is ambiguous about which states are "critical" → ask for the risk context instead of guessing.
- The request drifts into executing captures, driving a browser, or writing specs → stop and hand off to `playwright-e2e-engineer` *(manual-only)* or `clickthrough-test-engineer` *(manual-only)*; this skill designs only.
- The request is to write the evidence naming/masking/storage policy → hand off to `screenshot-evidence-planner`.
- The request involves destructive or live-state action (deleting baselines, mutating production data to force a state) → stop and refuse.

## Supporting Files

- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `screenshot-evidence-planner`, `test-plan-designer`, `qa-automation-architect`, `regression-suite-curator`, and the `playwright-e2e-engineer` execution seam.
- `references/` — None: the design is self-contained.
