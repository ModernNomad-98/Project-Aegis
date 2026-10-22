# Method record: modernization cutover planner

Reference for the modernization-cutover-planner skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Start from the question and the inspected evidence; mark UNKNOWN/UNVERIFIED explicitly.
- Produce the primary design/decision artifact before discussing options.
- Enumerate edge, failure and refusal cases with a chosen handling.
- Name the boundary owners and hand off their deliverables instead of duplicating them.

## 2. When this applies

- Plan strangler-fig replacement and monolith-to-service readiness: seams, adapters, routing, cutover gates, retirement, and ownership/data/ops/failure-mode readiness.
- A review/spec needs the record and the boundaries, not an implementation.
- The team needs explicit assumptions/open questions before building.

## 3. Output and evidence rules

- Every claim names its evidence source or is labelled assumption/UNKNOWN/UNRUN.
- The artifact is complete enough for an authorized engineer to implement against.
- The validation/test plan is concrete and tied to the artifact.

## 4. Boundaries

- architecture advisor requests route to `architecture-advisor`; this skill does not perform that owner work.
- architecture designer requests route to `architecture-designer`; this skill does not perform that owner work.
- schema evolution planner requests route to `schema-evolution-planner`; this skill does not perform that owner work.
- feature flag rollout strategist requests route to `feature-flag-rollout-strategist`; this skill does not perform that owner work.
- Broader discrimination set from evals/trigger-evals.json: `adr-writer`, `architecture-advisor`, `architecture-designer`, `change-classification-gate`, `code-reviewer`, `design-review-facilitator`, `feature-flag-rollout-strategist`, `human-approval-boundary`, `observability-by-design`, `release-readiness-reviewer`, `resilience-architecture-reviewer`, `rollback-runbook-author`, `schema-evolution-planner`, `tech-spec-writer` (neighbours, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Scope/inputs stated; assumptions separated from facts.
- Edge/failure cases enumerated with handling.
- Boundary owners named; no neighbouring deliverable taken over.
- No inspection/execution claimed that did not happen.
