---
name: component-boundary-designer
description: 'Use when component ownership is unclear: decide page/container/feature/shared/primitive layers, contracts and dependency rules with one owner per concern.'
---

# Component Boundary Designer

Terms: **family 14** - the discipline family in README.md and docs/skills-catalog.md; **read-only** means this skill inspects and returns guidance/records and never edits code or runs production actions.

## Purpose

Design component boundaries with one owner per concern: the page/container/feature/shared/primitive layer taxonomy, props/events/context contracts, allowed dependency direction, abstraction-vs-duplication rules, violations and a migration path.

The skill is **advisory and auto-invocable**. It produces guidance, records and review structure only; it does not edit code, run commands, use the network or grant production authority. Any implementation, execution or approval is a delegated host/user action under existing authority. It composes the nearest owners rather than duplicating them.

## Use When

- Component ownership is unclear or duplicated across features.
- A component tree mixes page, container, feature and primitive responsibilities.
- Dependency direction or shared-component policy needs defining.
- Abstraction vs duplication decisions need an explicit rule.

**Do not use when:** the request belongs to a named neighbouring owner (see Stop Conditions), or when inspection evidence is unavailable and the question would have to be answered by guessing.

## Inputs to Inspect

- Component tree and current folder/ownership structure.
- Design-system/shared component inventory and usage.
- Feature responsibilities, data dependencies and route composition.
- Team ownership and review boundaries.
- Known duplication, prop-drilling and circular-import pain points.

## Workflow

1. State the layer taxonomy and what each layer may know (page/container/feature/shared/primitive).
2. Assign one owner per concern and list cross-cutting concerns explicitly.
3. Define contracts: props, events, slots/context and what is forbidden to pass across layers.
4. Define allowed dependency direction and how shared components may depend on primitives only.
5. Audit the current tree for violations: duplicated logic, page-level data in primitives, feature-to-feature imports.
6. Decide abstraction vs duplication with a stated rule and threshold; define the migration sequence.
7. Return the boundary record, layer rules, contracts, violations and migration plan; do not edit code.

## Output Format

Return, in this order:

1. Layer taxonomy with responsibilities and one owner per concern.
2. Component contracts (props/events/context/slots) and forbidden couplings.
3. Dependency-direction rules and shared-component policy.
4. Violation list with location and severity.
5. Abstraction-vs-duplication rule and migration plan.

## Validation Checklist

- Layer taxonomy and ownership are explicit and non-overlapping.
- Contracts name what each boundary accepts and forbids.
- Dependency direction is stated and shared components are constrained.
- Violations have locations and evidence, not adjectives.
- Abstraction-vs-duplication rule is stated; migration is ordered.
- No component was edited or refactor claimed.

## Gotchas

- A primitive that fetches data is a container in disguise; the boundary has already leaked.
- Shared folders become dumping grounds without an owner and a dependency rule.
- Duplicating a component is sometimes cheaper than the wrong abstraction; state the rule.
- Circular feature imports are a boundary violation, not just a build problem.

## Stop Conditions

- The request is telemetry contract and instrumentation design (real owner, not a sibling): route to `observability-by-design`.
- The request is actual-diff review: route to `code-reviewer`.
- The request is frontend architecture mapping (Batch-3 sibling seam): route to `component-boundary-designer`.
- The trigger-evals file lists a broader 14-owner discrimination set (all named in the reference Boundaries); the three routes above are the primary Stop Conditions.
- The caller wants this skill to implement, provision or execute the design: refuse; return the design for the authorized host/user.
- Required evidence (routes, state, cache config or policy) is unavailable: state UNKNOWN and ask instead of inventing it.

## Supporting Files

- [component-boundary-rules](references/component-boundary-rules.md) - Component boundary rules: layers, contracts and dependencies.
- [evals/evals.json](evals/evals.json) - the 6 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 8 positive and 14 negative trigger-discrimination cases against the nearest owners.

**Source:** docs/skills-catalog.md - D12.2 product engineering craft pack (Batch 3/D110); coverage roadmap #162. The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
