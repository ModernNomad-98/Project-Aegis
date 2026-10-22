# Method record: technical debt classifier

Reference for the technical-debt-classifier skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Start from the question and the inspected evidence; mark UNKNOWN/UNVERIFIED explicitly.
- Produce the primary design/decision artifact before discussing options.
- Enumerate edge, failure and refusal cases with a chosen handling.
- Name the boundary owners and hand off their deliverables instead of duplicating them.

## 2. When this applies

- Classify debt by risk, owner, impact, payoff and whether it blocks future architecture; produce a ledger, not a wish list.
- A review/spec needs the record and the boundaries, not an implementation.
- The team needs explicit assumptions/open questions before building.

## 3. Output and evidence rules

- Every claim names its evidence source or is labelled assumption/UNKNOWN/UNRUN.
- The artifact is complete enough for an authorized engineer to implement against.
- The validation/test plan is concrete and tied to the artifact.

## 4. Boundaries

- principal code analyst requests route to `principal-code-analyst`; this skill does not perform that owner work.
- full codebase auditor requests route to `full-codebase-auditor`; this skill does not perform that owner work.
- staff scope selector requests route to `staff-scope-selector`; this skill does not perform that owner work.
- prioritization frame picker requests route to `prioritization-frame-picker`; this skill does not perform that owner work.
- Broader discrimination set from evals/trigger-evals.json: `adr-writer`, `architecture-designer`, `change-classification-gate`, `code-reviewer`, `design-review-facilitator`, `full-codebase-auditor`, `human-approval-boundary`, `principal-code-analyst`, `prioritization-frame-picker`, `release-readiness-reviewer`, `roadmap-under-uncertainty-planner`, `rollback-runbook-author`, `staff-scope-selector`, `tech-spec-writer` (neighbours, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Scope/inputs stated; assumptions separated from facts.
- Edge/failure cases enumerated with handling.
- Boundary owners named; no neighbouring deliverable taken over.
- No inspection/execution claimed that did not happen.
