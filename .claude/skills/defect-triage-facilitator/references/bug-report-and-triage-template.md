# Method record: defect triage facilitator

Reference for the defect-triage-facilitator skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Start from the question and the inspected evidence; mark UNKNOWN/UNVERIFIED explicitly.
- Produce the primary design/decision artifact before discussing options.
- Enumerate edge, failure and refusal cases with a chosen handling.
- Name the boundary owners and hand off their deliverables instead of duplicating them.

## 2. When this applies

- Facilitate consistent defect reporting and triage: complete the bug report (repro steps, expected vs actual, environment, evidence, suspected area), rank defects by severity, frequency, customer impact, security and release risk with explicit rationale, assign one owner and next action per decision, and route security/release-risk findings; refuses invented facts and fixes.
- A review/spec needs the record and the boundaries, not an implementation.
- The team needs explicit assumptions/open questions before building.

## 3. Output and evidence rules

- Every claim names its evidence source or is labelled assumption/UNKNOWN/UNRUN.
- The artifact is complete enough for an authorized engineer to implement against.
- The validation/test plan is concrete and tied to the artifact.

## 4. Boundaries

- ci failure classifier requests route to `ci-failure-classifier`; this skill does not perform that owner work.
- systematic debugger requests route to `systematic-debugger`; this skill does not perform that owner work.
- regression suite curator requests route to `regression-suite-curator`; this skill does not perform that owner work.
- release readiness reviewer requests route to `release-readiness-reviewer`; this skill does not perform that owner work.
- Broader discrimination set from evals/trigger-evals.json: `acceptance-criteria-reviewer`, `ai-closeout-reporter`, `ci-failure-classifier`, `clickthrough-test-engineer`, `exploratory-charter-designer`, `flaky-test-detective`, `manual-test-case-creator`, `qa-strategy-architect`, `regression-suite-curator`, `release-readiness-reviewer`, `screenshot-evidence-planner`, `systematic-debugger`, `test-coverage-mapper`, `test-plan-designer` (neighbours, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Scope/inputs stated; assumptions separated from facts.
- Edge/failure cases enumerated with handling.
- Boundary owners named; no neighbouring deliverable taken over.
- No inspection/execution claimed that did not happen.
