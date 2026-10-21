---
name: interface-first-designer
description: 'Use when implementation should start from stable interfaces: elicit callers and constraints, design contracts, adapters, command shapes, compatibility and rollback before internals change. Design-only; it stops before implementation and does not replace system-boundary or whole-system design.'
---

# Interface First Designer

Terms: **family 3** - the discipline family in README.md and docs/skills-catalog.md; **read-only** means this skill inspects and returns guidance/records and never edits code or runs production actions.

## Purpose

Design the contract before internals: identify callers and constraints, specify interfaces/adapters and command shapes, pin compatibility/versioning, test doubles and migration order, and stop before implementation.

The skill is **advisory and auto-invocable**. It produces guidance, records and review structure only; it does not edit code, run commands, use the network or grant production authority. Any implementation, execution or approval is a delegated host/user action under existing authority. It composes the nearest owners rather than duplicating them.

## Use When

- Multiple callers or teams will depend on a new or changing interface.
- Internals are unsettled but the external contract must be stable first.
- A change risks breaking callers, stored commands/messages, or compatibility guarantees.
- You need the seam for test doubles and an ordered migration before coding.

**Do not use when:** the request belongs to a named neighbouring owner (see Stop Conditions), or when inspection evidence is unavailable and the question would have to be answered by guessing.

## Inputs to Inspect

- Call sites, consumers and teams that will use the interface.
- Current API/data/message shapes, versioning and compatibility promises.
- Domain constraints and invariants the contract must preserve.
- Test strategy and the seams needed for doubles/fakes.
- Rollout, rollback and migration constraints.

## Workflow

1. Inventory callers and their expectations; state who is not yet known as UNKNOWN.
2. Derive the contract from use cases, not from the current implementation.
3. Specify interface/adapters, command/query shapes, error semantics and invariants.
4. Define compatibility rules, versioning and deprecation, including stored-data/message impact.
5. List test doubles and the ordered migration/rollback plan.
6. Identify the smallest first slice that proves the contract.
7. Stop before implementation; hand the contract and plan to the implementation owner.

## Output Format

Return, in this order:

1. Contract specification: operations, inputs/outputs, errors and invariants.
2. Adapter plan distinguishing ports from implementations.
3. Compatibility/versioning and migration/rollback plan.
4. Test-double plan and contract-test strategy.
5. Open questions and the smallest proving slice.

## Validation Checklist

- Callers and constraints inventoried; unknown callers labeled.
- Contract derived from use cases and invariants, not current internals.
- Error semantics, compatibility and versioning explicit.
- Adapters and test doubles specified without implementation.
- Migration order and rollback recorded.
- No implementation was performed or claimed.

## Gotchas

- Designing the interface from today's implementation bakes in accidental coupling.
- Ignoring stored commands/messages breaks replay and rollback even when types compile.
- An interface with no callers or no adapter plan is speculation, not design.
- Compatibility promises need a versioning and deprecation rule, not a note.
- Stopping before code is the feature; continuing to implement is a boundary violation.

## Stop Conditions

- The question is a system-boundary/API event contract owned end-to-end: route to api-event-architect.
- The request is whole-system architecture: route to architecture-designer.
- The concepts themselves are contested: route to domain-modeler first.
- The caller wants implementation: hand off the contract and stop.
- Callers cannot be identified: state the gap and ask, rather than inventing a contract.

## Supporting Files

- [interface-contract-template](references/interface-contract-template.md) - Interface contract template, compatibility and migration.
- [evals/evals.json](evals/evals.json) - the 6 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 8 positive and 14 negative trigger-discrimination cases against the nearest owners.

**Source:** docs/skills-catalog.md - cat 01 #8 (Interface-First Engineering); coverage roadmap #8. The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
