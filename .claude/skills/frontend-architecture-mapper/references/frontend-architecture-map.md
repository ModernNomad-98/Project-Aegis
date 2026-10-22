# Frontend architecture map: routes, state and gate inventory

Reference for the frontend-architecture-mapper skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Scope and out-of-scope are stated; the map is built from code/config, not stale docs.
- Every route/layout/provider node has an evidence source or is marked unverified.
- State owners and data hooks are inventoried per concern.
- Gates name their enforcement source (client UX vs server truth).
- Shared-UI boundaries and cross-feature imports are mapped.
- Every claim is backed by inspected evidence or labeled **assumption**, **UNKNOWN** or **UNRUN**; an empty check is never a PASS.

## 2. When this applies

- A frontend change needs a map of routes, layouts, providers and state before design.
- Ownership of state, data fetching or gates is unclear across features.
- A migration or refactor needs a boundary inventory and dependency view.
- Onboarding or review needs a trustworthy frontend architecture summary.

## 3. Output and evidence rules

1. Scoped frontend architecture map (route/layout/provider tree).
2. State-owner and data-hook inventory.
3. Permission-gate map with enforcement source.
4. Shared-UI boundary and cross-feature dependency view.
5. Risks, assumptions, unverified elements and verification plan.

The returned record must name the evidence source for each decision, separate verified facts from assumptions, and list what could not be inspected. The skill does not edit files or execute commands; delegated actions go to the host/user or the existing implementation owner under existing authority.

## 4. Boundaries

- Inputs inspected: see the SKILL.md Inputs to Inspect section.
- Greenfield system/component design routes to `architecture-designer`; this skill does not perform that owner's work.
- Data-flow inventory and diagramming routes to `data-flow-diagrammer`; this skill does not perform that owner's work.
- Component layer/ownership decisions (batch-3 sibling) routes to `component-boundary-designer`; this skill does not perform that owner's work.
- Broader discrimination set from evals/trigger-evals.json: the following owners' requests route away from this skill - `accessibility-test-harness`, `api-event-architect`, `architecture-designer`, `code-reviewer`, `component-boundary-designer`, `data-flow-diagrammer`, `domain-modeler`, `full-codebase-auditor`, `mobile-viewport-craft`, `observability-by-design`, `principal-code-analyst`, `tech-spec-writer`, `ux-design-iteration`, `validation-boundary-designer`, `vite-build-qa-engineer` (discrimination neighbours, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Scope and out-of-scope are stated; the map is built from code/config, not stale docs.
- Every route/layout/provider node has an evidence source or is marked unverified.
- State owners and data hooks are inventoried per concern.
- Gates name their enforcement source (client UX vs server truth).
- Shared-UI boundaries and cross-feature imports are mapped.
- Risks/assumptions are separated from facts; no code edit is claimed.
