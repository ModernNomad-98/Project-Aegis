---
name: cqrs-read-model-designer
description: 'Design CQRS read models: split decision, projections, rebuild/backfill and the consistency contract between writes and reads.'
---

# CQRS Read Model Designer

Terms: **family 3** - core architecture & engineering (README roster family 3; docs/skills-catalog.md Phase 2 pack). **Advisory/design-only:** produces the named artifact and records; never edits code, runs commands, uses the network or grants production authority.

## Purpose

Decide when to separate mutation paths from optimized read models; design projections, their lifecycle and explicit consistency expectations.

**Output artifact:** read-model split decision, projection plan and consistency contract. The skill is auto-invocable and advisory: it composes the named neighbouring owners instead of duplicating them, and it returns the artifact plus open questions for the authorized implementer.

## Use When

- The request needs read-model split decision, projection plan and consistency contract for a real system.
- The design is implicit/disputed or about to harden an assumption.
- A spec or review must record the artifact fields and boundaries explicitly.
- Implementation is about to start and the record it builds against is missing.

**Do not use when** the request belongs to a named neighbouring owner in Stop Conditions, or when the evidence needed for the artifact is unavailable.

## Inputs to Inspect

- Split decision with write/read cost evidence
- Read models and their consumers
- Projection source and ordering guarantees
- Staleness/consistency contract per read model
- Rebuild and backfill procedure
- Failure/poison-event handling

## Workflow

1. Quantify the read vs write needs and the cost of the split.
2. Define each read model and its consumer contract.
3. Specify projection inputs, ordering and idempotency.
4. Write the consistency/staleness contract explicitly.
5. Design rebuild, backfill and replay.
6. Handle poison events and projection failures.
7. Plan the projection schema evolution.

## Output Format

Return, in this order:

1. Scope, evidence inventory and what could not be inspected.
2. Read-model split decision, projection plan and consistency contract, with the fields listed in Inputs to Inspect.
3. Edge/failure cases and the chosen handling.
4. Boundary/handoff note naming the neighbouring owners (including the eval-only list below).
5. Verified facts, assumptions, UNKNOWN/UNVERIFIED items and the validation/test plan.

## Validation Checklist

- Each read model has a consumer and a consistency contract
- Projections are idempotent and ordered
- Rebuild/backfill is documented and tested
- Staleness is measurable and alertable
- Failure of a projection does not corrupt the source of truth

## Gotchas

- CQRS without a staleness contract surprises consumers
- A rebuild that is not idempotent produces duplicate or lost rows
- Projections silently drifting from the write model go unnoticed without lag metrics

## Stop Conditions

- operational vs analytical splitter requests route to `operational-vs-analytical-splitter`; this skill owns a different artifact.
- command gateway architect requests route to `command-gateway-architect`; this skill owns a different artifact.
- caching strategy designer requests route to `caching-strategy-designer`; this skill owns a different artifact.
- The caller wants implementation, execution or approval: refuse; return the artifact for the authorized owner.
- Required evidence is unavailable: mark the artifact UNVERIFIED and state what is missing instead of inventing facts.
- **Eval-only discrimination set** (from `evals/trigger-evals.json` overlaps_with; eval-only, not a routing contract): `adr-writer`, `architecture-designer`, `caching-strategy-designer`, `change-classification-gate`, `code-reviewer`, `command-gateway-architect`, `data-flow-diagrammer`, `design-review-facilitator`, `human-approval-boundary`, `operational-vs-analytical-splitter`, `release-readiness-reviewer`, `schema-evolution-planner`, `streaming-event-architect`, `tech-spec-writer`.

## Supporting Files

- [read-model-projection-plan](references/read-model-projection-plan.md) - the concrete read-model split decision, projection plan and consistency contract fields, construction method, checks and a worked table.
- [evals/evals.json](evals/evals.json) - six domain-specific behaviour cases.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 8 positive and 14 negative trigger-discrimination cases against real manifest owners (including the reciprocal sibling case).

**Source:** docs/skills-catalog.md Phase 2 core architecture & engineering pack (Batch 4/D112); coverage cat 01 rows #20. Description is trigger-first (capability front-loaded for truncated listings).
