# Method record: security drift detector

Reference for the security-drift-detector skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Start from the question and the inspected evidence; mark UNKNOWN/UNVERIFIED explicitly.
- Produce the primary design/decision artifact before discussing options.
- Enumerate edge, failure and refusal cases with a chosen handling.
- Name the boundary owners and hand off their deliverables instead of duplicating them.

## 2. When this applies

- Detect security drift against a recorded baseline: select and record the baseline, compare control by control, classify weakening (removed, narrowed, default-changed, unowned), detect undocumented changes and expiry/staleness, attach evidence and an owner/action per finding, and recommend re-baselining; read-only, no live probing.
- A review/spec needs the record and the boundaries, not an implementation.
- The team needs explicit assumptions/open questions before building.

## 3. Output and evidence rules

- Every claim names its evidence source or is labelled assumption/UNKNOWN/UNRUN.
- The artifact is complete enough for an authorized engineer to implement against.
- The validation/test plan is concrete and tied to the artifact.

## 4. Boundaries

- security pr reviewer requests route to `security-pr-reviewer`; this skill does not perform that owner work.
- rls policy auditor requests route to `rls-policy-auditor`; this skill does not perform that owner work.
- agent governance audit requests route to `agent-governance-audit`; this skill does not perform that owner work.
- compliance evidence collector requests route to `compliance-evidence-collector`; this skill does not perform that owner work.
- Broader discrimination set from evals/trigger-evals.json: `agent-governance-audit`, `agent-memory-governance`, `audit-log-architect`, `change-classification-gate`, `cloud-security-baseline-reviewer`, `code-reviewer`, `compliance-evidence-collector`, `iac-reviewer`, `local-ci-mirror-preflight`, `rls-policy-auditor`, `secure-migration-reviewer`, `security-pr-reviewer`, `source-of-truth-reconciler`, `threat-modeler` (neighbours, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Scope/inputs stated; assumptions separated from facts.
- Edge/failure cases enumerated with handling.
- Boundary owners named; no neighbouring deliverable taken over.
- No inspection/execution claimed that did not happen.
