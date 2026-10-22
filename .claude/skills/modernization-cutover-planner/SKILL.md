---
name: modernization-cutover-planner
description: 'Plan incremental modernization cutover: migration sequence, dual writes/backfill, cutover gates, rollback points and decommission.'
---

# Modernization Cutover Planner

Terms: **family 3** - core architecture & engineering (README roster family 3; docs/skills-catalog.md Phase 2 pack). **Advisory/design-only:** produces the named artifact and records; never edits code, runs commands, uses the network or grants production authority.

## Purpose

Plan strangler-fig replacement and monolith-to-service readiness: seams, adapters, routing, cutover gates, retirement, and ownership/data/ops/failure-mode readiness.

**Output artifact:** incremental cutover plan with gates, rollback points and decommission. The skill is auto-invocable and advisory: it composes the named neighbouring owners instead of duplicating them, and it returns the artifact plus open questions for the authorized implementer.

## Use When

- The request needs incremental cutover plan with gates, rollback points and decommission for a real system.
- The design is implicit/disputed or about to harden an assumption.
- A spec or review must record the artifact fields and boundaries explicitly.
- Implementation is about to start and the record it builds against is missing.

**Do not use when** the request belongs to a named neighbouring owner in Stop Conditions, or when the evidence needed for the artifact is unavailable.

## Inputs to Inspect

- Current and target states and the compatibility window
- Migration sequence and dependencies
- Dual-write/backfill/reconciliation strategy
- Feature flags and traffic stages
- Cutover gates and rollback points
- Data integrity checks and reconciliation

## Workflow

1. Define target state and the compatibility contract.
2. Sequence the migration into reversible phases.
3. Design dual-write/backfill with reconciliation.
4. Set measurable cutover gates per phase.
5. Define rollback triggers and owners.
6. Plan decommission and old-path cleanup.
7. Write the readiness checklist.

## Output Format

Return, in this order:

1. Scope, evidence inventory and what could not be inspected.
2. Incremental cutover plan with gates, rollback points and decommission, with the fields listed in Inputs to Inspect.
3. Edge/failure cases and the chosen handling.
4. Boundary/handoff note naming the neighbouring owners (including the eval-only list below).
5. Verified facts, assumptions, UNKNOWN/UNVERIFIED items and the validation/test plan.

## Validation Checklist

- Every phase has a gate and a rollback point
- Dual-write reconciliation is measurable
- Rollback is exercisable and owned
- Decommission has explicit criteria
- Cutover plan names the on-call decision maker

## Gotchas

- A big-bang cutover has no rollback point
- Backfill without reconciliation hides data loss
- Decommissioning too early turns a temporary bridge into permanent debt

## Stop Conditions

- architecture advisor requests route to `architecture-advisor`; this skill owns a different artifact.
- architecture designer requests route to `architecture-designer`; this skill owns a different artifact.
- schema evolution planner requests route to `schema-evolution-planner`; this skill owns a different artifact.
- The caller wants implementation, execution or approval: refuse; return the artifact for the authorized owner.
- Required evidence is unavailable: mark the artifact UNVERIFIED and state what is missing instead of inventing facts.
- **Eval-only discrimination set** (from `evals/trigger-evals.json` overlaps_with; eval-only, not a routing contract): `adr-writer`, `architecture-advisor`, `architecture-designer`, `change-classification-gate`, `code-reviewer`, `design-review-facilitator`, `feature-flag-rollout-strategist`, `human-approval-boundary`, `observability-by-design`, `release-readiness-reviewer`, `resilience-architecture-reviewer`, `rollback-runbook-author`, `schema-evolution-planner`, `tech-spec-writer`.

## Supporting Files

- [readiness-checklist](references/readiness-checklist.md) - the concrete incremental cutover plan with gates, rollback points and decommission fields, construction method, checks and a worked table.
- [evals/evals.json](evals/evals.json) - six domain-specific behaviour cases.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 22 trigger-discrimination cases (8 positive / 14 negative) against real manifest owners

**Source:** docs/skills-catalog.md Phase 2 core architecture & engineering pack (Batch 4/D112); coverage cat 01 rows #45, #46, #47. Description is trigger-first (capability front-loaded for truncated listings).
