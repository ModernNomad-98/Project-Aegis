# Method record: configuration architect

Reference for the configuration-architect skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Start from the question and the inspected evidence; mark UNKNOWN/UNVERIFIED explicitly.
- Produce the primary design/decision artifact before discussing options.
- Enumerate edge, failure and refusal cases with a chosen handling.
- Name the boundary owners and hand off their deliverables instead of duplicating them.

## 2. When this applies

- Separate build-time config, runtime config, tenant settings, secrets, defaults and validation; define precedence and ownership; close the tenant-settings residual of #66.
- A review/spec needs the record and the boundaries, not an implementation.
- The team needs explicit assumptions/open questions before building.

## 3. Output and evidence rules

- Every claim names its evidence source or is labelled assumption/UNKNOWN/UNRUN.
- The artifact is complete enough for an authorized engineer to implement against.
- The validation/test plan is concrete and tied to the artifact.

## 4. Boundaries

- environment parity reviewer requests route to `environment-parity-reviewer`; this skill does not perform that owner work.
- secrets identity hardener requests route to `secrets-identity-hardener`; this skill does not perform that owner work.
- vite build qa engineer requests route to `vite-build-qa-engineer`; this skill does not perform that owner work.
- user preference architect requests route to `user-preference-architect`; this skill does not perform that owner work.
- Broader discrimination set from evals/trigger-evals.json: `adr-writer`, `architecture-designer`, `code-reviewer`, `design-review-facilitator`, `environment-parity-reviewer`, `feature-flag-architect`, `human-approval-boundary`, `observability-by-design`, `plan-entitlement-architect`, `secrets-identity-hardener`, `tech-spec-writer`, `tenant-modeler`, `user-preference-architect`, `vite-build-qa-engineer` (neighbours, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Scope/inputs stated; assumptions separated from facts.
- Edge/failure cases enumerated with handling.
- Boundary owners named; no neighbouring deliverable taken over.
- No inspection/execution claimed that did not happen.
