# Method record: browser boundary reviewer

Reference for the browser-boundary-reviewer skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Start from the question and the inspected evidence; mark UNKNOWN/UNVERIFIED explicitly.
- Produce the primary design/decision artifact before discussing options.
- Enumerate edge, failure and refusal cases with a chosen handling.
- Name the boundary owners and hand off their deliverables instead of duplicating them.

## 2. When this applies

- Review a web application browser/origin boundary and security-header policy as one review: inventory every mutating endpoint, form and auth callback; assess cookie attributes and SameSite posture; build the CSRF defense matrix (token, origin check, custom header, SameSite) with bypass paths; produce a header policy table with enforcement point (application vs CDN/proxy) and required values; rank findings with evidence and list what could not be verified.
- A review/spec needs the record and the boundaries, not an implementation.
- The team needs explicit assumptions/open questions before building.

## 3. Output and evidence rules

- Every claim names its evidence source or is labelled assumption/UNKNOWN/UNRUN.
- The artifact is complete enough for an authorized engineer to implement against.
- The validation/test plan is concrete and tied to the artifact.

## 4. Boundaries

- security pr reviewer requests route to `security-pr-reviewer`; this skill does not perform that owner work.
- appsec implementer requests route to `appsec-implementer`; this skill does not perform that owner work.
- cloud security baseline reviewer requests route to `cloud-security-baseline-reviewer`; this skill does not perform that owner work.
- vite build qa engineer requests route to `vite-build-qa-engineer`; this skill does not perform that owner work.
- Broader discrimination set from evals/trigger-evals.json: `appsec-implementer`, `authorization-matrix-designer`, `clickthrough-test-engineer`, `cloud-security-baseline-reviewer`, `code-reviewer`, `multi-tenant-security-tester`, `rls-policy-auditor`, `secrets-identity-hardener`, `secure-migration-reviewer`, `security-impact-note-author`, `security-pr-reviewer`, `security-regression-harness-designer`, `threat-modeler`, `vite-build-qa-engineer` (neighbours, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Scope/inputs stated; assumptions separated from facts.
- Edge/failure cases enumerated with handling.
- Boundary owners named; no neighbouring deliverable taken over.
- No inspection/execution claimed that did not happen.
