---
name: concurrency-race-reviewer
description: 'Use when creates, updates, approvals, imports, retries or jobs can interleave: identify races such as lost updates, double-create, check-then-act and retry duplicates, and propose serialization, idempotency, locking or transactional fixes with tests. Review-only; it does not classify flaky tests or design resilience strategy.'
---

# Concurrency Race Reviewer

Terms: **family 3** - the discipline family in README.md and docs/skills-catalog.md; **read-only** means this skill inspects and returns guidance/records and never edits code or runs production actions.

## Purpose

Review interleaving operations for races: model actors and interleavings, find lost updates, double-create, check-then-act and retry duplicates, then propose serialization, idempotency, locking or transactional fixes with targeted tests.

The skill is **advisory and auto-invocable**. It produces guidance, records and review structure only; it does not edit code, run commands, use the network or grant production authority. Any implementation, execution or approval is a delegated host/user action under existing authority. It composes the nearest owners rather than duplicating them.

## Use When

- Two requests, jobs or users can update or create the same record concurrently.
- Retries, imports or queue consumers can duplicate work.
- An approval/workflow action can race with another action.
- You need to reason about transactions, locks, idempotency keys or version checks before shipping.

**Do not use when:** the request belongs to a named neighbouring owner (see Stop Conditions), or when inspection evidence is unavailable and the question would have to be answered by guessing.

## Inputs to Inspect

- Code paths and data model for the interleaving operations.
- Transaction boundaries, isolation level, locking and retry policy.
- Job/queue semantics: at-least-once, ordering, dedupe keys.
- Concurrency assumptions and invariants the system must hold.
- Existing tests and failure reports that hint at races.

## Workflow

1. Model actors, operations and the interleavings that matter; state assumptions about isolation and job delivery.
2. Build a race matrix: operation pair, shared state, interleaving, bad outcome.
3. Identify lost updates, double-create, check-then-act, non-atomic multi-write and retry duplicates.
4. Propose fixes in order of least invasive: constraint, transaction boundary, optimistic version, lock, idempotency key, queue serialization.
5. Define tests: deterministic interleaving where possible, stress where not, and what evidence proves the fix.
6. Record residual races and operational controls (monitoring, alerts).
7. Return findings and fix options; do not edit code or claim a fix is verified.

## Output Format

Return, in this order:

1. Actors/interleavings model and stated assumptions.
2. Race matrix with bad outcomes and evidence.
3. Ranked fix options with trade-offs and residual risk.
4. Test plan for deterministic and stress cases.
5. Operational controls and unverified areas.

## Validation Checklist

- Concurrency assumptions (isolation, delivery, ordering) stated.
- Race matrix covers create/update/approval/import/retry pairs.
- Each finding names the interleaving and the bad outcome.
- Fixes are ordered by invasiveness and address atomicity/idempotency explicitly.
- Tests include a deterministic interleaving where feasible; residual races recorded.
- No claim of runtime verification without evidence.

## Gotchas

- A transaction around the write does not fix check-then-act across requests.
- Retries with at-least-once delivery require idempotency, not just unique indexes.
- Locks without timeout/deadlock policy create outages.
- Tests that never interleave prove nothing about races.
- Averaging away a rare race in stress runs is not a pass.

## Stop Conditions

- The request is classifying an existing flaky test: route to flaky-test-detective.
- The request is resilience/availability strategy: route to resilience-architecture-reviewer.
- The request is a general diff review: route to code-reviewer.
- The request is designing queue semantics/architecture (delivery, ordering, dead letters): route to background-job-orchestration-architect; consumer-race reviews stay with this skill.
- The request is a per-change test plan: route to test-plan-designer.
- The caller wants code edits: return fix options and delegate implementation.
- The data model/transaction boundaries are unknown: state assumptions and ask for evidence.

## Supporting Files

- [race-review-matrix](references/race-review-matrix.md) - Concurrency race matrix, fix ladder and test evidence.
- [evals/evals.json](evals/evals.json) - the 4 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 8 positive and 14 negative trigger-discrimination cases against the nearest owners.

**Source:** docs/skills-catalog.md - cat 04 #155 (Concurrency Race Review); coverage roadmap #155. The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
