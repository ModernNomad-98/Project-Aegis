# Play orders — the four fixed QA plays

These are the ONLY orders `qa-orchestrator` runs. Each was verified against the named skills' own "Use when"/"Do NOT use when"/handoff lines. Do not invent a fifth order; if a goal matches none, ask one scoping question.

## Play A — Find bugs now (a running app)

1. `production-safe-smoke-tester` — only when the running app is deployed production; read-only probes; names what is not exercised.
2. `exploratory-charter-designer` — optional, for a timeboxed mission when the goal is open-ended discovery; designs only, never executes.
3. `clickthrough-test-engineer` *(manual-only)* — route-by-route walkthrough of the running app; hands blockers to `systematic-debugger`/owner; fixes nothing.
4. `defect-triage-facilitator` — turns findings into consistent reports and severity/priority decisions.

Root cause is out of scope: `systematic-debugger` is manual-only and never run by the conductor.

## Play B — Plan tests for a feature or change

1. `acceptance-criteria-reviewer` — only when criteria already exist; reviews testability/completeness.
2. `test-plan-designer` — the concrete plan for THIS feature/change (layers, in/out of scope, exit criteria); hands implementation to engineer skills.
3. `manual-test-case-creator` — for the plan's manual items; full cases another tester can execute with no tribal knowledge.
4. Name (do not run) the engineer skills the plan maps to.

## Play C — Check before release

1. `risk-tiered-validation-selector` — machine-classifies the touched files into depth tiers; selects DEPTH only, never executes, fails closed.
2. `sharded-validation-with-resume` — only when a sharded test suite / CI exists; designs shard map + resume. In a no-CI consumer this is design-only and normally skipped — say why.
3. `clickthrough-test-engineer` *(manual-only)* — changed routes only.
4. `defect-triage-facilitator` — classifies and prioritizes findings.
5. `release-readiness-reviewer` — ship/no-ship gate on EVIDENCE; with no CI it must report the CI dimension MISSING and cannot claim a pass.

## Play D — Set up or improve automated tests

1. `test-coverage-mapper` — what existing tests cover, ranked uncovered critical paths.
2. `qa-strategy-architect` — product-wide strategy (risk inventory, layer split, manual-vs-automated).
3. `qa-automation-architect` — framework/tooling/parallelization design.
4. `test-data-architect` — deterministic test data per layer (no secrets; non-production only).
5. `vitest-unit-component-engineer` *(manual-only)* and `playwright-e2e-engineer` *(manual-only)* — implementation and runs.
6. `regression-suite-curator` — what belongs in the regression suite and at which tier.
7. `test-tenant-provisioner` *(manual-only)* — only if non-production test accounts must be created; never production or real customer tenants.

These are conductor-composed orders. Where two skills do not hand off to each other (notably `test-coverage-mapper` then `qa-strategy-architect`), the order is the conductor's choice, not a skill handoff.

## Fallback: no browser control (Play A or C)

`manual-test-case-creator` writes the cases → a person runs them → findings go to `defect-triage-facilitator`. Say explicitly that the browser route was unavailable and what is therefore UNKNOWN.

## Conditional companions (never required, never silently dropped)

- `production-safe-smoke-tester` — deployed-production safety only.
- `screenshot-evidence-planner` — evidence conventions when screenshots are captured; the skill's conventions govern naming/masking/storage.
- `systematic-debugger` *(manual-only)* — root cause, outside the conductor.
- `test-tenant-provisioner` *(manual-only)* — only with non-production test accounts.
