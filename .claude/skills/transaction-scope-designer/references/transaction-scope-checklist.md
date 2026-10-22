# Method record: transaction scope designer

Reference for the transaction-scope-designer skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Start from the question and the inspected evidence; mark UNKNOWN/UNVERIFIED explicitly.
- Produce the primary design/decision artifact before discussing options.
- Enumerate edge, failure and refusal cases with a chosen handling.
- Name the boundary owners and hand off their deliverables instead of duplicating them.

## 2. When this applies

- Decide which operations must be atomic vs staged; isolation level, lock ordering, long-transaction avoidance and cross-service compensation.
- A review/spec needs the record and the boundaries, not an implementation.
- The team needs explicit assumptions/open questions before building.

## 3. Output and evidence rules

- Every claim names its evidence source or is labelled assumption/UNKNOWN/UNRUN.
- The artifact is complete enough for an authorized engineer to implement against.
- The validation/test plan is concrete and tied to the artifact.

## 4. Boundaries

- concurrency race reviewer requests route to `concurrency-race-reviewer`; this skill does not perform that owner work.
- command gateway architect requests route to `command-gateway-architect`; this skill does not perform that owner work.
- validation boundary designer requests route to `validation-boundary-designer`; this skill does not perform that owner work.
- background job orchestration architect requests route to `background-job-orchestration-architect`; this skill does not perform that owner work.
- Broader discrimination set from evals/trigger-evals.json: `adr-writer`, `architecture-designer`, `background-job-orchestration-architect`, `code-reviewer`, `command-gateway-architect`, `concurrency-race-reviewer`, `data-migration-runbook-author`, `design-review-facilitator`, `human-approval-boundary`, `resilience-architecture-reviewer`, `schema-evolution-planner`, `secure-migration-reviewer`, `tech-spec-writer`, `validation-boundary-designer` (neighbours, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Scope/inputs stated; assumptions separated from facts.
- Edge/failure cases enumerated with handling.
- Boundary owners named; no neighbouring deliverable taken over.
- No inspection/execution claimed that did not happen.
