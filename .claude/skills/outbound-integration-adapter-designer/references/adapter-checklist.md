# Method record: outbound integration adapter designer

Reference for the outbound-integration-adapter-designer skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Start from the question and the inspected evidence; mark UNKNOWN/UNVERIFIED explicitly.
- Produce the primary design/decision artifact before discussing options.
- Enumerate edge, failure and refusal cases with a chosen handling.
- Name the boundary owners and hand off their deliverables instead of duplicating them.

## 2. When this applies

- Design the wrapper for third-party calls: timeouts, retries, circuit breakers, logging, contract tests, version pinning.
- A review/spec needs the record and the boundaries, not an implementation.
- The team needs explicit assumptions/open questions before building.

## 3. Output and evidence rules

- Every claim names its evidence source or is labelled assumption/UNKNOWN/UNRUN.
- The artifact is complete enough for an authorized engineer to implement against.
- The validation/test plan is concrete and tied to the artifact.

## 4. Boundaries

- resilience architecture reviewer requests route to `resilience-architecture-reviewer`; this skill does not perform that owner work.
- latency budget architect requests route to `latency-budget-architect`; this skill does not perform that owner work.
- api contract test designer requests route to `api-contract-test-designer`; this skill does not perform that owner work.
- ai router architect requests route to `ai-router-architect`; this skill does not perform that owner work.
- Broader discrimination set from evals/trigger-evals.json: `adr-writer`, `ai-router-architect`, `api-contract-test-designer`, `api-event-architect`, `architecture-designer`, `background-job-orchestration-architect`, `code-reviewer`, `design-review-facilitator`, `error-taxonomy-designer`, `human-approval-boundary`, `interface-first-designer`, `latency-budget-architect`, `resilience-architecture-reviewer`, `tech-spec-writer` (neighbours, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Scope/inputs stated; assumptions separated from facts.
- Edge/failure cases enumerated with handling.
- Boundary owners named; no neighbouring deliverable taken over.
- No inspection/execution claimed that did not happen.
