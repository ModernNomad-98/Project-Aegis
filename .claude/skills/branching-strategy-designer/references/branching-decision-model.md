# Method record: branching strategy designer

Reference for the branching-strategy-designer skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Start from the question and the inspected evidence; mark UNKNOWN/UNVERIFIED explicitly.
- Produce the primary design/decision artifact before discussing options.
- Enumerate edge, failure and refusal cases with a chosen handling.
- Name the boundary owners and hand off their deliverables instead of duplicating them.

## 2. When this applies

- Design and record a repository branching and release flow: choose trunk-based or branch/release branching with alternatives and rejected options, define branch naming/protection/review rules, merge method and queue, release and hotfix flow, migrate from the current model with safe defaults and risks; refuses to change repository settings or invent team constraints.
- A review/spec needs the record and the boundaries, not an implementation.
- The team needs explicit assumptions/open questions before building.

## 3. Output and evidence rules

- Every claim names its evidence source or is labelled assumption/UNKNOWN/UNRUN.
- The artifact is complete enough for an authorized engineer to implement against.
- The validation/test plan is concrete and tied to the artifact.

## 4. Boundaries

- ci pipeline architect requests route to `ci-pipeline-architect`; this skill does not perform that owner work.
- contribution guide author requests route to `contribution-guide-author`; this skill does not perform that owner work.
- merge is deploy governance requests route to `merge-is-deploy-governance`; this skill does not perform that owner work.
- release readiness reviewer requests route to `release-readiness-reviewer`; this skill does not perform that owner work.
- Broader discrimination set from evals/trigger-evals.json: `ai-sdlc-operating-model`, `change-classification-gate`, `ci-pipeline-architect`, `code-reviewer`, `contribution-guide-author`, `environment-parity-reviewer`, `human-approval-boundary`, `local-ci-mirror-preflight`, `merge-is-deploy-governance`, `phased-work-handoff-designer`, `release-readiness-reviewer`, `reviewable-diff-discipline`, `rollback-runbook-author`, `scoped-approval-register` (neighbours, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Scope/inputs stated; assumptions separated from facts.
- Edge/failure cases enumerated with handling.
- Boundary owners named; no neighbouring deliverable taken over.
- No inspection/execution claimed that did not happen.
