---
name: application-layer-pattern-advisor
description: 'Decide application-layer patterns: when adapters, facades, repositories, service objects or use-case layers earn their cost, and where they belong.'
---

# Application Layer Pattern Advisor

Terms: **family 3** - core architecture & engineering (README roster family 3; docs/skills-catalog.md Phase 2 pack). **Advisory/design-only:** produces the named artifact and records; never edits code, runs commands, uses the network or grants production authority.

## Purpose

Decide when adapters, facades, repositories, service objects and explicit use-case layers earn their cost; give placement and refactor guidance without hiding side effects.

**Output artifact:** pattern decision table with placement and side-effect visibility. The skill is auto-invocable and advisory: it composes the named neighbouring owners instead of duplicating them, and it returns the artifact plus open questions for the authorized implementer.

## Use When

- The request needs pattern decision table with placement and side-effect visibility for a real system.
- The design is implicit/disputed or about to harden an assumption.
- A spec or review must record the artifact fields and boundaries explicitly.
- Implementation is about to start and the record it builds against is missing.

**Do not use when** the request belongs to a named neighbouring owner in Stop Conditions, or when the evidence needed for the artifact is unavailable.

## Inputs to Inspect

- Patterns considered: adapter, facade, repository, service object, use-case layer
- Cost and benefit per pattern
- Placement and allowed dependencies
- Side-effect visibility and transaction boundary
- Introduction/removal/refactor path
- Over-abstraction stop rules

## Workflow

1. State the actual change pressure and coupling evidence.
2. List candidate patterns with cost/benefit.
3. Decide placement per layer and dependency direction.
4. Make side effects and transaction boundaries visible.
5. Define introduction or removal steps.
6. Set the stop rules for over-abstraction.
7. Yield external-provider adapter contracts to outbound-integration-adapter-designer.

## Output Format

Return, in this order:

1. Scope, evidence inventory and what could not be inspected.
2. Pattern decision table with placement and side-effect visibility, with the fields listed in Inputs to Inspect.
3. Edge/failure cases and the chosen handling.
4. Boundary/handoff note naming the neighbouring owners (including the eval-only list below).
5. Verified facts, assumptions, UNKNOWN/UNVERIFIED items and the validation/test plan.

## Validation Checklist

- Each pattern has a concrete cost and benefit
- Placement respects dependency direction
- Side effects are visible at the application boundary
- Removal/introduction path is incremental
- External provider adapter details are not stolen from the sibling owner

## Gotchas

- An abstraction that only forwards calls is cost without benefit
- Hiding side effects behind a facade makes retries unsafe
- Pattern advice and external adapter design are different decisions

## Stop Conditions

- layered architecture enforcer requests route to `layered-architecture-enforcer`; this skill owns a different artifact.
- interface first designer requests route to `interface-first-designer`; this skill owns a different artifact.
- code simplifier requests route to `code-simplifier`; this skill owns a different artifact.
- Pattern/placement decisions inside the application layer yield to `application-layer-pattern-advisor`; external-provider adapter contracts (timeouts, retries, idempotency, signing) yield to `outbound-integration-adapter-designer`.
- The caller wants implementation, execution or approval: refuse; return the artifact for the authorized owner.
- Required evidence is unavailable: mark the artifact UNVERIFIED and state what is missing instead of inventing facts.
- **Eval-only discrimination set** (from `evals/trigger-evals.json` overlaps_with; eval-only, not a routing contract): `adr-writer`, `architecture-designer`, `change-classification-gate`, `code-reviewer`, `code-simplifier`, `command-gateway-architect`, `dependency-direction-guard`, `design-review-facilitator`, `domain-modeler`, `human-approval-boundary`, `interface-first-designer`, `layered-architecture-enforcer`, `release-readiness-reviewer`, `tech-spec-writer`.

## Supporting Files

- [pattern-decision-table](references/pattern-decision-table.md) - the concrete pattern decision table with placement and side-effect visibility fields, construction method, checks and a worked table.
- [evals/evals.json](evals/evals.json) - six domain-specific behaviour cases.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 8 positive and 14 negative trigger-discrimination cases against real manifest owners (including the reciprocal sibling case).

**Source:** docs/skills-catalog.md Phase 2 core architecture & engineering pack (Batch 4/D112); coverage cat 01 rows #31, #32, #33, #34, #35. Description is trigger-first (capability front-loaded for truncated listings).
