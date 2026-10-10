---
name: exploratory-charter-designer
description: 'Designs a timeboxed exploratory-testing charter: a mission, the risks and open questions to probe, personas, test data, entry paths, and note/evidence conventions — so a tester runs one focused exploratory session and reports findings instead of wandering unguided. Produces the charter only; executes nothing. Use when asked to design an exploratory-testing charter, define a timeboxed exploratory mission, or turn "we need to explore X" into a scoped session. Do NOT use for a deterministic test plan (test-plan-designer), scripted manual cases (manual-test-case-creator), the product-wide QA strategy (qa-strategy-architect), or executing a live walkthrough (clickthrough-test-engineer).'
---

# Exploratory Charter Designer

**Reading key:** QA is quality assurance. Exploratory testing is a timeboxed,
investigation-driven session in which the tester designs and learns at the
same time, instead of following scripted steps. A charter is that session's
one-page contract: what to learn, where to start, and how to report.

## Purpose

Produce an exploratory-testing charter: a timeboxed mission, the risks and
open questions to probe, personas, test data, entry paths, and note/evidence
conventions — so a tester runs one focused exploratory session and reports
findings instead of wandering unguided. The charter scopes manual exploration
the way a plan scopes deterministic testing; this skill executes nothing.

## Use When

- Use when: asked to design an exploratory-testing charter for a feature or surface.
- Use when: asked to define a timeboxed exploratory mission ("what should we explore and how long?").
- Use when: asked to turn "we need to explore X" into a scoped, reportable session.
- Use when: a risky area has no scripted coverage yet and the team wants a focused manual probe first.
- Do NOT use when: the ask is a deterministic test plan with layers, data, and exit criteria — that is `test-plan-designer`.
- Do NOT use when: the ask is step-by-step scripted manual cases — that is `manual-test-case-creator`.
- Do NOT use when: the ask is the product-wide QA strategy (what to automate vs keep manual) — that is `qa-strategy-architect`.
- Do NOT use when: the ask is executing a live walkthrough of the app — that is `clickthrough-test-engineer` *(manual-only)*.

## Inputs to Inspect

1. The feature or surface to explore, and what the team hopes to learn.
2. Known risks: recent defects, untested changes, and areas the team already suspects.
3. Personas and roles that exist in the product, and which ones matter here.
4. Available test data: accounts, datasets, and fixtures the tester may use.
5. Prior defects and notes: bug history, support tickets, and earlier session reports for this surface.
6. The QA strategy's automation/manual split, so the charter probes what automation does NOT cover.
7. The timebox budget: how long the session may run.

## Workflow

1. **State the mission and the timebox.** One sentence on what the session must learn, and a hard time limit. A charter without a timebox is not bounded.
2. **Enumerate risks and open questions.** Rank the things to probe: what could be broken, what nobody has checked, what the team would regret missing.
3. **Name personas, data, and entry paths.** Which users explore, with which accounts and datasets, starting from which screens or routes.
4. **Bound the scope.** State explicitly what the session covers and what it deliberately skips (and why), and the defect-report and note/evidence conventions — including `screenshot-evidence-planner` naming/masking when evidence is captured.
5. **Emit the charter** in the Output Format. State what was chosen, why, and the main rejected alternative.

## Output Format

Emit the charter in the conversation (nothing is written to the repo):

```
EXPLORATORY CHARTER — <feature / surface>
Mission: <what the session must learn, in one sentence>
Timebox: <duration> — hard stop at <time or condition>
Risks & open questions: <ranked probes>
Personas: <who explores>
Data: <accounts, datasets, fixtures available to the tester>
Entry paths: <where the session starts>
Note & evidence conventions: <how findings are recorded and reported;
  screenshot naming/masking per screenshot-evidence-planner when evidence is captured>
Out of scope: <what the session deliberately skips and why>
Chosen / why / rejected: <the key choices, the reason for each, and the main
  rejected alternative>
```

## Validation Checklist

- [ ] Mission and timebox are both present and concrete.
- [ ] Every risk maps to at least one probe area; no unranked pile of guesses.
- [ ] Personas, data, and entry paths are concrete enough for a stranger to start.
- [ ] Scope is bounded: an out-of-scope list exists with rationale.
- [ ] The charter contains no scripted step-by-step cases with expected results.
- [ ] The charter claims to have executed nothing.

## Gotchas

- A charter is not a scripted case: no step-by-step expected results. If the request wants those, it is `manual-test-case-creator`'s job.
- The timebox is the discipline: without it, exploration expands until the session is abandoned; findings are scoped by what fits.
- The output is findings, not pass/fail verdicts; a charter that pre-commits to "all checks pass" has stopped being exploratory.
- Charter sessions often surface evidence needs; reference `screenshot-evidence-planner` for naming/masking instead of inventing local rules.
- This skill must not absorb `manual-test-case-creator` or `clickthrough-test-engineer` jobs: it designs the session, it does not script or run it.

## Stop Conditions

- The feature or scope is ambiguous ("explore the app") → stop and ask which feature or surface, before writing a charter.
- No risk or entry context exists (no changes, no suspects, no data) → ask what the team wants to learn; a charter cannot be invented from a feature name.
- The request becomes executing a live session → hand off to `clickthrough-test-engineer` *(manual-only)*; this skill designs only.
- The request becomes writing scripted step-by-step cases → hand off to `manual-test-case-creator`.
- The request involves destructive or live-state action (production data, payment, deletion) → stop and refuse.

## Supporting Files

- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `manual-test-case-creator`, `clickthrough-test-engineer`, `test-plan-designer`, and `qa-strategy-architect`.
- `references/` — None: the charter format is self-contained.
