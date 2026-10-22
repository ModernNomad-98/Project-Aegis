# Method record: architecture fitness function designer

Reference for the architecture-fitness-function-designer skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Start from the question and the inspected evidence; mark UNKNOWN/UNVERIFIED explicitly.
- Produce the primary design/decision artifact before discussing options.
- Enumerate edge, failure and refusal cases with a chosen handling.
- Name the boundary owners and hand off their deliverables instead of duplicating them.

## 2. When this applies

- Define continuous checks that verify architectural constraints (dependency direction, layer rules, size/latency/coupling budgets) as CI gates with owned exception registers.
- A review/spec needs the record and the boundaries, not an implementation.
- The team needs explicit assumptions/open questions before building.

## 3. Output and evidence rules

- Every claim names its evidence source or is labelled assumption/UNKNOWN/UNRUN.
- The artifact is complete enough for an authorized engineer to implement against.
- The validation/test plan is concrete and tied to the artifact.

## 4. Boundaries

- dependency direction guard requests route to `dependency-direction-guard`; this skill does not perform that owner work.
- layered architecture enforcer requests route to `layered-architecture-enforcer`; this skill does not perform that owner work.
- n plus one detector requests route to `n-plus-one-detector`; this skill does not perform that owner work.
- performance test harness requests route to `performance-test-harness`; this skill does not perform that owner work.
- Broader discrimination set from evals/trigger-evals.json: `adr-writer`, `architecture-designer`, `change-classification-gate`, `code-reviewer`, `dependency-direction-guard`, `design-review-facilitator`, `frontend-perf-engineer`, `human-approval-boundary`, `layered-architecture-enforcer`, `n-plus-one-detector`, `observability-by-design`, `performance-test-harness`, `release-readiness-reviewer`, `tech-spec-writer` (neighbours, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Scope/inputs stated; assumptions separated from facts.
- Edge/failure cases enumerated with handling.
- Boundary owners named; no neighbouring deliverable taken over.
- No inspection/execution claimed that did not happen.
