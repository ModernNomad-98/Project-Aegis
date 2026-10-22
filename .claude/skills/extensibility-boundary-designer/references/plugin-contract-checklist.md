# Method record: extensibility boundary designer

Reference for the extensibility-boundary-designer skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Start from the question and the inspected evidence; mark UNKNOWN/UNVERIFIED explicitly.
- Produce the primary design/decision artifact before discussing options.
- Enumerate edge, failure and refusal cases with a chosen handling.
- Name the boundary owners and hand off their deliverables instead of duplicating them.

## 2. When this applies

- Design extension points and plugin contracts: isolation, permissions, versioning, compatibility and safe lifecycle without exposing unstable internals.
- A review/spec needs the record and the boundaries, not an implementation.
- The team needs explicit assumptions/open questions before building.

## 3. Output and evidence rules

- Every claim names its evidence source or is labelled assumption/UNKNOWN/UNRUN.
- The artifact is complete enough for an authorized engineer to implement against.
- The validation/test plan is concrete and tied to the artifact.

## 4. Boundaries

- interface first designer requests route to `interface-first-designer`; this skill does not perform that owner work.
- supply chain security reviewer requests route to `supply-chain-security-reviewer`; this skill does not perform that owner work.
- api event architect requests route to `api-event-architect`; this skill does not perform that owner work.
- authorization matrix designer requests route to `authorization-matrix-designer`; this skill does not perform that owner work.
- Broader discrimination set from evals/trigger-evals.json: `adr-writer`, `api-event-architect`, `architecture-designer`, `authorization-matrix-designer`, `change-classification-gate`, `code-reviewer`, `design-review-facilitator`, `human-approval-boundary`, `interface-first-designer`, `layered-architecture-enforcer`, `release-readiness-reviewer`, `security-pr-reviewer`, `supply-chain-security-reviewer`, `tech-spec-writer` (neighbours, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Scope/inputs stated; assumptions separated from facts.
- Edge/failure cases enumerated with handling.
- Boundary owners named; no neighbouring deliverable taken over.
- No inspection/execution claimed that did not happen.
