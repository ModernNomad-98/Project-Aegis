---
name: state-machine-modeler
description: 'Model state machines: states, events, guards, side effects, terminal states, retry/compensation edges and invalid-transition handling before code hardens the wrong lifecycle.'
---

# State Machine Modeler

Terms: **family 3** - core architecture & engineering (README roster family 3; docs/skills-catalog.md Phase 2 pack). **Advisory/design-only:** produces the named artifact and records; never edits code, runs commands, uses the network or grants production authority.

## Purpose

Model lifecycle states, legal transitions, terminal states, retries and invalid-transition handling for a domain object before code hardens the wrong lifecycle.

**Output artifact:** state/event/guard table plus transition matrix. The skill is auto-invocable and advisory: it composes the named neighbouring owners instead of duplicating them, and it returns the artifact plus open questions for the authorized implementer.

## Use When

- The request needs state/event/guard table plus transition matrix for a real system.
- The design is implicit/disputed or about to harden an assumption.
- A spec or review must record the artifact fields and boundaries explicitly.
- Implementation is about to start and the record it builds against is missing.

**Do not use when** the request belongs to a named neighbouring owner in Stop Conditions, or when the evidence needed for the artifact is unavailable.

## Inputs to Inspect

- Every state named, with owner and meaning
- Events/commands that trigger transitions
- Guards as explicit predicates
- Side effects per transition
- Terminal states and re-open rules
- Retry/compensation edges and their bounds

## Workflow

1. Inventory states from code, schema and incidents; mark inferred ones.
2. List events/commands and who may emit them.
3. Write guards as predicates over named evidence.
4. Attach side effects and failure handling per transition.
5. Mark terminal states and any re-open path.
6. Enumerate illegal moves and the expected refusal.
7. Review the matrix with the domain owner.

## Output Format

Return, in this order:

1. Scope, evidence inventory and what could not be inspected.
2. State/event/guard table plus transition matrix, with the fields listed in Inputs to Inspect.
3. Edge/failure cases and the chosen handling.
4. Boundary/handoff note naming the neighbouring owners (including the eval-only list below).
5. Verified facts, assumptions, UNKNOWN/UNVERIFIED items and the validation/test plan.

## Validation Checklist

- Every state reachable and every state has an exit or is terminal
- Every transition has trigger, guard and effect
- Retries bounded with a failure terminal
- Illegal transitions are refused not silently ignored
- Matrix covers the incidents/open questions that motivated it

## Gotchas

- A status column is not a state machine until guards and illegal moves are explicit
- Retries without a terminal failure can loop forever
- Terminal states that can silently re-open corrupt consumer assumptions

## Stop Conditions

- tenant modeler requests route to `tenant-modeler`; this skill owns a different artifact.
- subscription lifecycle designer requests route to `subscription-lifecycle-designer`; this skill owns a different artifact.
- domain modeler requests route to `domain-modeler`; this skill owns a different artifact.
- The caller wants implementation, execution or approval: refuse; return the artifact for the authorized owner.
- Required evidence is unavailable: mark the artifact UNVERIFIED and state what is missing instead of inventing facts.
- **Eval-only discrimination set** (from `evals/trigger-evals.json` overlaps_with; eval-only, not a routing contract): `adr-writer`, `architecture-designer`, `change-classification-gate`, `code-reviewer`, `design-review-facilitator`, `domain-modeler`, `human-approval-boundary`, `product-spec-writer`, `property-based-test-designer`, `release-readiness-reviewer`, `rollback-runbook-author`, `subscription-lifecycle-designer`, `tech-spec-writer`, `tenant-modeler`.

## Supporting Files

- [state-table-template](references/state-table-template.md) - the concrete state/event/guard table plus transition matrix fields, construction method, checks and a worked table.
- [evals/evals.json](evals/evals.json) - six domain-specific behaviour cases.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 22 trigger-discrimination cases (8 positive / 14 negative) against real manifest owners

**Source:** docs/skills-catalog.md Phase 2 core architecture & engineering pack (Batch 4/D112); coverage cat 01 rows #14. Description is trigger-first (capability front-loaded for truncated listings).
