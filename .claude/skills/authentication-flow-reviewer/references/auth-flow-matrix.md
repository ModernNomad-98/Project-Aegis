# Method record: authentication flow reviewer

Reference for the authentication-flow-reviewer skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Start from the question and the inspected evidence; mark UNKNOWN/UNVERIFIED explicitly.
- Produce the primary design/decision artifact before discussing options.
- Enumerate edge, failure and refusal cases with a chosen handling.
- Name the boundary owners and hand off their deliverables instead of duplicating them.

## 2. When this applies

- Review authentication as one flow set rather than isolated endpoints: inventory flows and state map, token/session lifecycle and refresh semantics, logout/revocation and re-authentication paths, MFA enrollment/recovery edge cases, SSO/federation and account-linking boundaries, denial/error/audit expectations, and review-only findings with recovery/failure test plan.
- A review/spec needs the record and the boundaries, not an implementation.
- The team needs explicit assumptions/open questions before building.

## 3. Output and evidence rules

- Every claim names its evidence source or is labelled assumption/UNKNOWN/UNRUN.
- The artifact is complete enough for an authorized engineer to implement against.
- The validation/test plan is concrete and tied to the artifact.

## 4. Boundaries

- human agent trust reviewer requests route to `human-agent-trust-reviewer`; this skill does not perform that owner work.
- authority invalidation architect requests route to `authority-invalidation-architect`; this skill does not perform that owner work.
- secrets identity hardener requests route to `secrets-identity-hardener`; this skill does not perform that owner work.
- membership invitation designer requests route to `membership-invitation-designer`; this skill does not perform that owner work.
- Broader discrimination set from evals/trigger-evals.json: `agent-authorization-matrix`, `appsec-implementer`, `audit-log-architect`, `authority-invalidation-architect`, `authorization-matrix-designer`, `code-reviewer`, `human-agent-trust-reviewer`, `incident-response-runbook`, `membership-invitation-designer`, `multi-tenant-security-tester`, `rls-policy-auditor`, `secrets-identity-hardener`, `security-pr-reviewer`, `tenant-isolation-reviewer` (neighbours, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Scope/inputs stated; assumptions separated from facts.
- Edge/failure cases enumerated with handling.
- Boundary owners named; no neighbouring deliverable taken over.
- No inspection/execution claimed that did not happen.
