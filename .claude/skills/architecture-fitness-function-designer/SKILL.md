---
name: architecture-fitness-function-designer
description: 'Design architecture fitness functions: measurable rules for dependency direction, coupling, layering and latency with budgets and owners.'
---

# Architecture Fitness Function Designer

Terms: **family 3** - core architecture & engineering (README roster family 3; docs/skills-catalog.md Phase 2 pack). **Advisory/design-only:** produces the named artifact and records; never edits code, runs commands, uses the network or grants production authority.

## Purpose

Define continuous checks that verify architectural constraints (dependency direction, layer rules, size/latency/coupling budgets) as CI gates with owned exception registers.

**Output artifact:** fitness-function catalog with metrics, budgets, owners and failure actions. The skill is auto-invocable and advisory: it composes the named neighbouring owners instead of duplicating them, and it returns the artifact plus open questions for the authorized implementer.

## Use When

- The request needs fitness-function catalog with metrics, budgets, owners and failure actions for a real system.
- The design is implicit/disputed or about to harden an assumption.
- A spec or review must record the artifact fields and boundaries explicitly.
- Implementation is about to start and the record it builds against is missing.

**Do not use when** the request belongs to a named neighbouring owner in Stop Conditions, or when the evidence needed for the artifact is unavailable.

## Inputs to Inspect

- Architecture characteristics to protect
- Fitness function per characteristic
- Metric definition and collection point
- Threshold/budget and trend rule
- Owner and escalation path
- Failure action (block/warn/report)

## Workflow

1. Select the characteristics that actually matter.
2. Define a measurable function per characteristic.
3. Set budgets from evidence, not aspiration.
4. Choose failure actions and ownership.
5. Decide collection point and frequency.
6. Design the trend/ratchet rule.
7. Plan exemptions and reviews.

## Output Format

Return, in this order:

1. Scope, evidence inventory and what could not be inspected.
2. Fitness-function catalog with metrics, budgets, owners and failure actions, with the fields listed in Inputs to Inspect.
3. Edge/failure cases and the chosen handling.
4. Boundary/handoff note naming the neighbouring owners (including the eval-only list below).
5. Verified facts, assumptions, UNKNOWN/UNVERIFIED items and the validation/test plan.

## Validation Checklist

- Each function maps to one characteristic
- Metric is observable and stable
- Budget is justified by evidence
- Owner and failure action are explicit
- Flaky checks have a quarantine rule

## Gotchas

- A fitness function nobody owns becomes a flaky gate
- Budgets set by aspiration fail on day one
- Measurements without trend rules do not prevent drift

## Stop Conditions

- dependency direction guard requests route to `dependency-direction-guard`; this skill owns a different artifact.
- layered architecture enforcer requests route to `layered-architecture-enforcer`; this skill owns a different artifact.
- n plus one detector requests route to `n-plus-one-detector`; this skill owns a different artifact.
- The caller wants implementation, execution or approval: refuse; return the artifact for the authorized owner.
- Required evidence is unavailable: mark the artifact UNVERIFIED and state what is missing instead of inventing facts.
- **Eval-only discrimination set** (from `evals/trigger-evals.json` overlaps_with; eval-only, not a routing contract): `adr-writer`, `architecture-designer`, `change-classification-gate`, `code-reviewer`, `dependency-direction-guard`, `design-review-facilitator`, `frontend-perf-engineer`, `human-approval-boundary`, `layered-architecture-enforcer`, `n-plus-one-detector`, `observability-by-design`, `performance-test-harness`, `release-readiness-reviewer`, `tech-spec-writer`.

## Supporting Files

- [fitness-function-catalog](references/fitness-function-catalog.md) - the concrete fitness-function catalog with metrics, budgets, owners and failure actions fields, construction method, checks and a worked table.
- [evals/evals.json](evals/evals.json) - six domain-specific behaviour cases.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 22 trigger-discrimination cases (8 positive / 14 negative) against real manifest owners

**Source:** docs/skills-catalog.md Phase 2 core architecture & engineering pack (Batch 4/D112); coverage cat 01 rows #50. Description is trigger-first (capability front-loaded for truncated listings).
