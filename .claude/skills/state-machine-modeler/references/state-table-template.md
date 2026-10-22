# Method record: state machine modeler

Reference for the state-machine-modeler skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Start from the question and the inspected evidence; mark UNKNOWN/UNVERIFIED explicitly.
- Produce the primary design/decision artifact before discussing options.
- Enumerate edge, failure and refusal cases with a chosen handling.
- Name the boundary owners and hand off their deliverables instead of duplicating them.

## 2. When this applies

- Model lifecycle states, legal transitions, terminal states, retries and invalid-transition handling for a domain object before code hardens the wrong lifecycle.
- A review/spec needs the record and the boundaries, not an implementation.
- The team needs explicit assumptions/open questions before building.

## 3. Output and evidence rules

- Every claim names its evidence source or is labelled assumption/UNKNOWN/UNRUN.
- The artifact is complete enough for an authorized engineer to implement against.
- The validation/test plan is concrete and tied to the artifact.

## 4. Boundaries

- tenant modeler requests route to `tenant-modeler`; this skill does not perform that owner work.
- subscription lifecycle designer requests route to `subscription-lifecycle-designer`; this skill does not perform that owner work.
- domain modeler requests route to `domain-modeler`; this skill does not perform that owner work.
- property based test designer requests route to `property-based-test-designer`; this skill does not perform that owner work.
- Broader discrimination set from evals/trigger-evals.json: `adr-writer`, `architecture-designer`, `change-classification-gate`, `code-reviewer`, `design-review-facilitator`, `domain-modeler`, `human-approval-boundary`, `product-spec-writer`, `property-based-test-designer`, `release-readiness-reviewer`, `rollback-runbook-author`, `subscription-lifecycle-designer`, `tech-spec-writer`, `tenant-modeler` (neighbours, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Scope/inputs stated; assumptions separated from facts.
- Edge/failure cases enumerated with handling.
- Boundary owners named; no neighbouring deliverable taken over.
- No inspection/execution claimed that did not happen.
