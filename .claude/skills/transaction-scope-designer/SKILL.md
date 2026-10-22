---
name: transaction-scope-designer
description: 'Design transaction scope across tables and services: atomic vs staged writes, isolation, lock order, retries, idempotency and compensation.'
---

# Transaction Scope Designer

Terms: **family 3** - core architecture & engineering (README roster family 3; docs/skills-catalog.md Phase 2 pack). **Advisory/design-only:** produces the named artifact and records; never edits code, runs commands, uses the network or grants production authority.

## Purpose

Decide which operations must be atomic vs staged; isolation level, lock ordering, long-transaction avoidance and cross-service compensation.

**Output artifact:** transaction scope matrix plus compensation plan. The skill is auto-invocable and advisory: it composes the named neighbouring owners instead of duplicating them, and it returns the artifact plus open questions for the authorized implementer.

## Use When

- The request needs transaction scope matrix plus compensation plan for a real system.
- The design is implicit/disputed or about to harden an assumption.
- A spec or review must record the artifact fields and boundaries explicitly.
- Implementation is about to start and the record it builds against is missing.

**Do not use when** the request belongs to a named neighbouring owner in Stop Conditions, or when the evidence needed for the artifact is unavailable.

## Inputs to Inspect

- Write paths and the invariants they must preserve
- Atomic vs staged decision per path
- Isolation level and its anomaly budget
- Lock order and deadlock avoidance
- Idempotency key and acknowledgement handling
- Compensation/rollback per staged step

## Workflow

1. Map every write path and its invariant.
2. Decide atomic vs staged with a failure-cost argument.
3. Choose isolation level and name the anomaly it permits.
4. Define a global lock order or an optimistic strategy.
5. Design idempotency and lost-acknowledgement behaviour.
6. Write the compensation sequence for partial failure.
7. Plan the concurrency tests that prove the bounds.

## Output Format

Return, in this order:

1. Scope, evidence inventory and what could not be inspected.
2. Transaction scope matrix plus compensation plan, with the fields listed in Inputs to Inspect.
3. Edge/failure cases and the chosen handling.
4. Boundary/handoff note naming the neighbouring owners (including the eval-only list below).
5. Verified facts, assumptions, UNKNOWN/UNVERIFIED items and the validation/test plan.

## Validation Checklist

- Every write path has a decision and rationale
- Lock order is global and documented
- Retries are idempotent or deduplicated
- Compensation leaves no partial invariant
- Anomaly budget matches the isolation level

## Gotchas

- A long transaction holding locks is a latency incident waiting to happen
- Idempotency added after the fact rarely covers replays
- Compensation without reconciliation leaves silent partial state

## Stop Conditions

- concurrency race reviewer requests route to `concurrency-race-reviewer`; this skill owns a different artifact.
- command gateway architect requests route to `command-gateway-architect`; this skill owns a different artifact.
- validation boundary designer requests route to `validation-boundary-designer`; this skill owns a different artifact.
- The caller wants implementation, execution or approval: refuse; return the artifact for the authorized owner.
- Required evidence is unavailable: mark the artifact UNVERIFIED and state what is missing instead of inventing facts.
- **Eval-only discrimination set** (from `evals/trigger-evals.json` overlaps_with; eval-only, not a routing contract): `adr-writer`, `architecture-designer`, `background-job-orchestration-architect`, `code-reviewer`, `command-gateway-architect`, `concurrency-race-reviewer`, `data-migration-runbook-author`, `design-review-facilitator`, `human-approval-boundary`, `resilience-architecture-reviewer`, `schema-evolution-planner`, `secure-migration-reviewer`, `tech-spec-writer`, `validation-boundary-designer`.

## Supporting Files

- [transaction-scope-checklist](references/transaction-scope-checklist.md) - the concrete transaction scope matrix plus compensation plan fields, construction method, checks and a worked table.
- [evals/evals.json](evals/evals.json) - six domain-specific behaviour cases.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 8 positive and 14 negative trigger-discrimination cases against real manifest owners (including the reciprocal sibling case).

**Source:** docs/skills-catalog.md Phase 2 core architecture & engineering pack (Batch 4/D112); coverage cat 01, 04 rows #19, #156. Description is trigger-first (capability front-loaded for truncated listings).
