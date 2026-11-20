# Play orders — the four fixed QA plays

These are the ONLY orders `qa-orchestrator` runs. Do not invent a fifth order; if a goal matches none, ask one scoping question.

## Play A — Find bugs now (a running app)

1. `production-safe-smoke-tester` — only when the running app is deployed production; it DESIGNS read-only probes and names what is not exercised, but executes nothing and never claims live status: the human/operational owner executes the plan, and a live-status determination routes to the manual-only `observability-operator`. The conductor never executes production probes.
2. `exploratory-charter-designer` — optional, for a timeboxed mission when the goal is open-ended discovery; designs only, never executes.
3. `clickthrough-test-engineer` *(manual-only, CONDITIONAL)* — route-by-route walkthrough of the running app; hands blockers to `systematic-debugger`/owner; fixes nothing. Applies only when installed, authorized under the consumer's recorded manual-only policy, and the host can drive a browser; otherwise this step becomes the written-walkthrough route: `manual-test-case-creator` writes the cases -> a person runs the steps; the order's existing next step (`defect-triage-facilitator`) triages, single triage; not a substitution.
4. `defect-triage-facilitator` — turns findings into consistent reports and severity/priority decisions.

Root cause is out of scope: `systematic-debugger` is manual-only and never run by the conductor.

## Play B — Plan tests for a feature or change

1. `acceptance-criteria-reviewer` — only when criteria already exist; reviews testability/completeness.
2. `test-plan-designer` — the concrete plan for THIS feature/change (layers, in/out of scope, exit criteria); hands implementation to engineer skills.
3. `manual-test-case-creator` — for the plan's manual items; full cases another tester can execute with no tribal knowledge.
4. Name (do not run) the engineer skills the plan maps to.

## Play C — Check before release

1. `risk-tiered-validation-selector` — machine-classifies the touched files into depth tiers; selects DEPTH only, never executes, fails closed.
2. `sharded-validation-with-resume` — only when a sharded suite exists; designs the shard map/resume machinery and never executes it.
3. **Run the selected validation tier through the project's own execution owner.** When that route is the manual-only `local-ci-mirror-preflight`, list it as the EXECUTION OWNER and hand it to the human under the manual-only policy (never auto-run or chain it); otherwise use the project's documented validation command. With no CI evidence, record the CI dimension MISSING and do not claim a pass.
4. `clickthrough-test-engineer` *(manual-only, CONDITIONAL)* — changed routes only, same three conditions; otherwise the changed-routes step becomes the written-walkthrough route (cases -> person -> triage, single triage at the order's existing `defect-triage-facilitator` step), not a substitution.
5. `defect-triage-facilitator` — classifies and prioritizes findings; residual needs a recorded disposition + backlog id.
6. `release-readiness-reviewer` — ship/no-ship gate on EVIDENCE; with no CI it reports the CI dimension MISSING and cannot claim a pass. A direct "is this ready to ship?" request is that skill's own trigger and is routed there, not run as a conductor play.

## Play D — Set up or improve automated tests

With an existing test suite:

1. `test-coverage-mapper` — what the existing suite covers, ranked uncovered critical paths (requires a suite; with no suite this step is skipped).
2. `qa-strategy-architect` — product-wide strategy (risk inventory, layer split, manual-vs-automated).
3. `qa-automation-architect` — framework/tooling/parallelization design; its blueprint selects the tools and layers for THIS repo stack.
4. `test-data-architect` — deterministic test data per layer (no secrets; non-production only).
5. `test-tenant-provisioner` *(manual-only)* — ONLY when non-production test accounts are missing, drifted or hand-made, or need validation or repair (including stale auth fixtures); validate-only is the default; BEFORE any engineer run that needs them; if validation leaves any needed account BLOCKED, UNVERIFIED, MISSING or DRIFTED, STOP before the engineer step, hand the validation result to the human, and continue only after a clean re-validation.
6. The engineer skill(s) the blueprint SELECTS — for example `vitest-unit-component-engineer` *(manual-only)* and/or `playwright-e2e-engineer` *(manual-only)*, not automatically both; a stack with no browser layer names no browser engineer.
7. `regression-suite-curator` — ONLY when the suite has CI history and runtimes; otherwise name the curator as the next action once the suite has run in CI.

With NO test suite, Play D starts at `qa-strategy-architect`: `test-coverage-mapper` is skipped (nothing to map) and `regression-suite-curator` is named as the next action once the suite has run in CI.
## Written-walkthrough route (Play A and Play C changed routes)

When `clickthrough-test-engineer` is not installed, not authorized under the consumer's recorded manual-only policy, or the host cannot drive a browser, the play's route is the written-walkthrough route: `manual-test-case-creator` writes the cases -> a person runs the steps -> findings go to `defect-triage-facilitator`. State which route ran and what the human route could not cover; never mark the browser/clickthrough check passed and never substitute another executor.

## Conditional companions (never required, never silently dropped)

- `production-safe-smoke-tester` — deployed-production safety only.
- `screenshot-evidence-planner` — evidence conventions when screenshots are captured.
- `systematic-debugger` *(manual-only)* — root cause, outside the conductor.
- `test-tenant-provisioner` *(manual-only)* — only with non-production test accounts (creation, validation or repair; missing, drifted or hand-made accounts; stale auth fixtures; validate-only is the default).
- `local-ci-mirror-preflight` *(manual-only)* — the execution owner for Play C when the project's route is the local CI mirror; handed to the human, never auto-run.

These are conductor-composed orders. Where two skills do not hand off to each other (notably `test-coverage-mapper` then `qa-strategy-architect`), the order is the conductor's choice, not a skill handoff.
