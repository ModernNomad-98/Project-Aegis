---
name: production-safe-smoke-tester
description: 'Use when checking a deployed system safely: design smoke checks that are read-only probes, state exactly what is not exercised, and never mutate production; seeded-fixture probes are read-only against pre-seeded isolated or disposable tenants with no real customer data, and any write is not a smoke check (it needs separate explicit authorization, verified cleanup/rollback and no real customer data). Design/advisory only; execution is delegated to the host/user under production authority, and a live production-health determination is an operational action for the manual-only observability-operator, not this skill.'
---

# Production Safe Smoke Tester

Terms: **family 6** - the discipline family in README.md and docs/skills-catalog.md; **read-only** means this skill inspects and returns guidance/records and never edits code or runs production actions.

## Purpose

Design a production-safe smoke plan: enumerate safe and unsafe operations, choose read-only probes, dry-runs or seeded tenant checks, define stop conditions, and record exactly what the smoke did and did not exercise.

The skill is **advisory and auto-invocable**. It produces guidance, records and review structure only; it does not edit code, run commands, use the network or grant production authority. Any implementation, execution or approval is a delegated host/user action under existing authority. It composes the nearest owners rather than duplicating them.

## Use When

- A deploy needs a quick production check without writing unsafe data.
- You must decide which probes are read-only/reversible and which are forbidden.
- A smoke plan exists but does not state what it does not exercise.
- The user asks how to design or validate a safe smoke plan or checklist for a deploy (a live production-health determination is an operational action, not a design task).

**Do not use when:** the request belongs to a named neighbouring owner (see Stop Conditions), or when inspection evidence is unavailable and the question would have to be answered by guessing.

## Inputs to Inspect

- Deploy version, environment and the endpoints/operations to check.
- Permissions/credentials available (read-only preferred) and their authority.
- Data-safety rules: fixture-only routes, seeded tenants, irreversible operations.
- Rollback/monitoring signals and the acceptable blast radius.
- What cannot be checked from outside the host.

## Workflow

1. Enumerate candidate checks and classify each as read-only, seeded-fixture-only (read-only probes against pre-seeded isolated or disposable tenants with no real customer data), or unsafe/forbidden. The default is read-only; a write to a disposable tenant is not a smoke check and requires separate explicit authorization, verified cleanup/rollback and no real customer data.
2. Choose the smallest safe set that proves the deploy; prefer GET/health/version/read-only queries. Seeded-fixture probes are read-only; any write is not a smoke check and needs the separate authorization above, never a smoke convenience.
3. For each check define the probe, expected observable, evidence to record and stop condition.
4. State permissions and production authority explicitly; never smuggle write operations into a smoke plan.
5. Record what is not exercised (auth flows, payments, mutations, jobs) and the risk of that gap.
6. Define escalation/rollback if a check fails and who decides.
7. Return the plan; execution is a delegated host/user action, never performed by this skill.

## Output Format

Return, in this order:

1. Safe/unsafe operation inventory with classification.
2. Chosen probes with expected observables and evidence.
3. Stop conditions and escalation/rollback path.
4. Explicitly unexercised areas and residual risk.
5. Permissions/authority statement for the host/user.

## Validation Checklist

- Every probe classified as read-only, reversible, seeded-fixture or forbidden.
- No unsafe/destructive operation proposed as a smoke check.
- Expected observables and evidence defined per probe.
- Stop conditions, escalation and rollback owner stated.
- Unexercised areas and risk listed explicitly.
- Execution delegated; no production run claimed by the skill.

## Gotchas

- A smoke test that creates orders is a production transaction, not a smoke test; do not run write probes as smoke.
- Health endpoints can be cached or synthetic; state what each probe actually proves.
- Reading secrets or PII during smoke is an unsafe side effect.
- A green smoke does not prove background jobs or auth flows; list the gap.
- Production authority belongs to the host/user; advisory text does not grant it.

## Stop Conditions

- The request is monitoring/alert design: route to synthetic-monitoring-architect.
- The request is writing E2E tests: route to playwright-e2e-engineer.
- The request is a manual test case: route to manual-test-case-creator.
- The user asks for a live post-deploy health determination (current status, dashboard queries): this skill is design-only and must not claim live status - route the live determination to `observability-operator` (manual-only operational owner that runs real queries) and live-failure diagnosis to `systematic-debugger`.
- The caller asks this skill to execute production probes: refuse; return the plan for the authorized host/user.
- Any probe would mutate data: it is not a smoke check. Require separate explicit authorization, verified cleanup/rollback and no real customer data (disposable isolated tenant only); otherwise stop and propose a read-only alternative.

## Supporting Files

- [safe-smoke-checklist](references/safe-smoke-checklist.md) - Production-safe smoke checklist and evidence rules.
- [evals/evals.json](evals/evals.json) - the 6 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 8 positive and 14 negative trigger-discrimination cases against the nearest owners.

**Source:** docs/skills-catalog.md - cat 06 #188 (Production-Safe Smoke Testing); coverage roadmap #188. The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
