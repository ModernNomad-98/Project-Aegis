---
name: frontend-architecture-mapper
description: 'Use when a frontend app must be mapped before change: routes, layouts, providers, state, data hooks, permission gates, shared-UI boundaries.'
---

# Frontend Architecture Mapper

Terms: **family 14** - the discipline family in README.md and docs/skills-catalog.md; **read-only** means this skill inspects and returns guidance/records and never edits code or runs production actions.

## Purpose

Produce a trustworthy map of an existing frontend application before any change: the route/layout/provider tree, state owners, data-fetch hooks, permission gates and shared-UI boundaries, with risks, assumptions and a verification plan.

The skill is **advisory and auto-invocable**. It produces guidance, records and review structure only; it does not edit code, run commands, use the network or grant production authority. Any implementation, execution or approval is a delegated host/user action under existing authority. It composes the nearest owners rather than duplicating them.

## Use When

- A frontend change needs a map of routes, layouts, providers and state before design.
- Ownership of state, data fetching or gates is unclear across features.
- A migration or refactor needs a boundary inventory and dependency view.
- Onboarding or review needs a trustworthy frontend architecture summary.

**Do not use when:** the request belongs to a named neighbouring owner (see Stop Conditions), or when inspection evidence is unavailable and the question would have to be answered by guessing.

## Inputs to Inspect

- Route configuration, layout tree and provider composition.
- State stores, data hooks/fetchers and cache configuration.
- Auth/permission model and where gates are enforced.
- Shared UI/design-system boundaries and feature folders.
- Known incidents, stale diagrams and risks to verify.

## Workflow

1. State the question and scope of the map; list what will not be inspected.
2. Build the route/layout/provider tree from configuration and code, not from docs.
3. Inventory state owners per concern (local/shared/URL/server-cache/persistent) and the data hooks that feed them.
4. Map permission gates and where identity/role decisions are consumed (client UX vs server truth).
5. Map shared-UI boundaries and cross-feature imports; flag duplicate or overlapping ownership.
6. Record risks, assumptions and unverified elements distinctly, then define a verification plan.
7. Return the map, boundary inventory, dependency view and risks; do not change code.

## Output Format

Return, in this order:

1. Scoped frontend architecture map (route/layout/provider tree).
2. State-owner and data-hook inventory.
3. Permission-gate map with enforcement source.
4. Shared-UI boundary and cross-feature dependency view.
5. Risks, assumptions, unverified elements and verification plan.

## Validation Checklist

- Scope and out-of-scope are stated; the map is built from code/config, not stale docs.
- Every route/layout/provider node has an evidence source or is marked unverified.
- State owners and data hooks are inventoried per concern.
- Gates name their enforcement source (client UX vs server truth).
- Shared-UI boundaries and cross-feature imports are mapped.
- Risks/assumptions are separated from facts; no code edit is claimed.

## Gotchas

- Mapping from an old diagram instead of the route tree produces a confident but wrong map.
- Client route guards are frequently mistaken for security boundaries; name the server enforcement.
- A provider that wraps the app often hides global state ownership; trace both provider and store.
- Unmarked assumptions in an architecture map turn into design inputs.

## Stop Conditions

- The request is greenfield system/component design: route to `architecture-designer`.
- The request is data-flow inventory and diagramming: route to `data-flow-diagrammer`.
- The request is component layer/ownership decisions (Batch-3 sibling): route to `component-boundary-designer`.
- The trigger-evals file lists a broader 14-owner discrimination set (all named in the reference Boundaries); the routes above are the primary Stop Conditions.
- The caller wants this skill to implement, provision or execute the design: refuse; return the design for the authorized host/user.
- Required evidence (routes, state, cache config or policy) is unavailable: state UNKNOWN and ask instead of inventing it.

## Supporting Files

- [frontend-architecture-map](references/frontend-architecture-map.md) - Frontend architecture map: routes, state and gate inventory.
- [evals/evals.json](evals/evals.json) - the 6 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 8 positive and 14 negative trigger-discrimination cases against the nearest owners.

**Source:** docs/skills-catalog.md - D12.2 product engineering craft pack (Batch 3/D110); coverage roadmap #161. The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
