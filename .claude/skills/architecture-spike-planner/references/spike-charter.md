# Method record: architecture spike planner

Reference for the architecture-spike-planner skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Start from the question and the inspected evidence; mark UNKNOWN/UNVERIFIED explicitly.
- Produce the primary design/decision artifact before discussing options.
- Enumerate edge, failure and refusal cases with a chosen handling.
- Name the boundary owners and hand off their deliverables instead of duplicating them.

## 2. When this applies

- Charter time-boxed spikes: hypothesis, success criteria, artifacts, decision output, and what is thrown away.
- A review/spec needs the record and the boundaries, not an implementation.
- The team needs explicit assumptions/open questions before building.

## 3. Output and evidence rules

- Every claim names its evidence source or is labelled assumption/UNKNOWN/UNRUN.
- The artifact is complete enough for an authorized engineer to implement against.
- The validation/test plan is concrete and tied to the artifact.

## 4. Boundaries

- roadmap under uncertainty planner requests route to `roadmap-under-uncertainty-planner`; this skill does not perform that owner work.
- ai task decomposer requests route to `ai-task-decomposer`; this skill does not perform that owner work.
- exploratory charter designer requests route to `exploratory-charter-designer`; this skill does not perform that owner work.
- architecture designer requests route to `architecture-designer`; this skill does not perform that owner work.
- Broader discrimination set from evals/trigger-evals.json: `adr-writer`, `ai-task-decomposer`, `architecture-designer`, `change-classification-gate`, `code-reviewer`, `design-review-facilitator`, `exploratory-charter-designer`, `human-approval-boundary`, `observability-by-design`, `release-readiness-reviewer`, `roadmap-under-uncertainty-planner`, `rollback-runbook-author`, `security-pr-reviewer`, `tech-spec-writer` (neighbours, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Scope/inputs stated; assumptions separated from facts.
- Edge/failure cases enumerated with handling.
- Boundary owners named; no neighbouring deliverable taken over.
- No inspection/execution claimed that did not happen.
