# Method record: edge function designer

Reference for the edge-function-designer skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Start from the question and the inspected evidence; mark UNKNOWN/UNVERIFIED explicitly.
- Produce the primary design/decision artifact before discussing options.
- Enumerate edge, failure and refusal cases with a chosen handling.
- Name the boundary owners and hand off their deliverables instead of duplicating them.

## 2. When this applies

- Design serverless/edge functions: auth, environment validation, timeouts, cold-start awareness, concurrency/retry semantics, event-source policy and logging.
- A review/spec needs the record and the boundaries, not an implementation.
- The team needs explicit assumptions/open questions before building.

## 3. Output and evidence rules

- Every claim names its evidence source or is labelled assumption/UNKNOWN/UNRUN.
- The artifact is complete enough for an authorized engineer to implement against.
- The validation/test plan is concrete and tied to the artifact.

## 4. Boundaries

- cloud architecture decider requests route to `cloud-architecture-decider`; this skill does not perform that owner work.
- aws saas architect requests route to `aws-saas-architect`; this skill does not perform that owner work.
- azure saas architect requests route to `azure-saas-architect`; this skill does not perform that owner work.
- background job orchestration architect requests route to `background-job-orchestration-architect`; this skill does not perform that owner work.
- Broader discrimination set from evals/trigger-evals.json: `adr-writer`, `api-event-architect`, `architecture-designer`, `aws-saas-architect`, `azure-saas-architect`, `background-job-orchestration-architect`, `caching-strategy-designer`, `cloud-architecture-decider`, `code-reviewer`, `design-review-facilitator`, `human-approval-boundary`, `latency-budget-architect`, `observability-by-design`, `tech-spec-writer` (neighbours, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Scope/inputs stated; assumptions separated from facts.
- Edge/failure cases enumerated with handling.
- Boundary owners named; no neighbouring deliverable taken over.
- No inspection/execution claimed that did not happen.
