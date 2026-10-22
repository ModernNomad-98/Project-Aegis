# Method record: graphql boundary reviewer

Reference for the graphql-boundary-reviewer skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Start from the question and the inspected evidence; mark UNKNOWN/UNVERIFIED explicitly.
- Produce the primary design/decision artifact before discussing options.
- Enumerate edge, failure and refusal cases with a chosen handling.
- Name the boundary owners and hand off their deliverables instead of duplicating them.

## 2. When this applies

- Review GraphQL schema, resolver authorization, field-level access, N+1, depth/complexity/cost limits and batching.
- A review/spec needs the record and the boundaries, not an implementation.
- The team needs explicit assumptions/open questions before building.

## 3. Output and evidence rules

- Every claim names its evidence source or is labelled assumption/UNKNOWN/UNRUN.
- The artifact is complete enough for an authorized engineer to implement against.
- The validation/test plan is concrete and tied to the artifact.

## 4. Boundaries

- n plus one detector requests route to `n-plus-one-detector`; this skill does not perform that owner work.
- authorization matrix designer requests route to `authorization-matrix-designer`; this skill does not perform that owner work.
- api contract test designer requests route to `api-contract-test-designer`; this skill does not perform that owner work.
- api event architect requests route to `api-event-architect`; this skill does not perform that owner work.
- Broader discrimination set from evals/trigger-evals.json: `adr-writer`, `api-contract-test-designer`, `api-event-architect`, `architecture-designer`, `authorization-matrix-designer`, `caching-strategy-designer`, `code-reviewer`, `design-review-facilitator`, `human-approval-boundary`, `n-plus-one-detector`, `observability-by-design`, `query-plan-reader`, `security-pr-reviewer`, `tech-spec-writer` (neighbours, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Scope/inputs stated; assumptions separated from facts.
- Edge/failure cases enumerated with handling.
- Boundary owners named; no neighbouring deliverable taken over.
- No inspection/execution claimed that did not happen.
