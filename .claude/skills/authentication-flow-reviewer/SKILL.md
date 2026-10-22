---
name: authentication-flow-reviewer
description: 'Use when authentication must be reviewed as one flow set: login, logout, reset, MFA enrollment and recovery, SSO/federation, account linking, session refresh, device trust and profile resolution, including failure and recovery paths. Do NOT use for agent-approval trust review (human-agent-trust-reviewer) or hands-on credential hardening (secrets-identity-hardener); this skill reviews auth flows and writes no code.'
---

# Authentication Flow Reviewer

Terms: **family 5** - Security, RLS & supply chain (README roster family 5; docs/skills-catalog.md Phase 4 security, RLS and supply-chain pack); **advisory/design-only** means this skill produces guidance and records and never edits code, runs commands or grants production authority.

## Purpose

Review authentication as one flow set rather than isolated endpoints: inventory flows and state map, token/session lifecycle and refresh semantics, logout/revocation and re-authentication paths, MFA enrollment/recovery edge cases, SSO/federation and account-linking boundaries, denial/error/audit expectations, and review-only findings with recovery/failure test plan.

The skill is **auto-invocable and advisory/design-only**. It produces the named artifact below with evidence and open questions; it does not edit code, run commands, use the network or grant production authority. Implementation and approval are delegated host/user actions. It composes the named neighbouring owners instead of duplicating them.

## Use When

- The request is to review authentication as one flow set rather than isolated endpoints: inventory flows and state map, token/session lifecycle and refresh semantics, logout/revocation and re-authentication paths, MFA enrollment/recovery edge cases, SSO/federation and account-linking boundaries, denial/error/audit expectations, and review-only findings with recovery/failure test plan..
- The named artifact is missing, disputed or about to be built against a wrong assumption.
- A review/spec must record the artifact, its edge cases and the boundary owners explicitly.
- An implementation is about to start and the ask is for the artifact it must build against.

**Do not use when:** the request belongs to a named neighbouring owner (the complete routing list is in Stop Conditions) or when no evidence exists and the answer would be invention.

## Inputs to Inspect

- Flow inventory: login, logout, password reset, MFA enroll/verify, SSO initiate/callback, account linking, session refresh and profile resolution, with entry points.
- Session/token configuration: lifetime, rotation, refresh strategy, storage location and revocation mechanism.
- Identity provider(s) and federation configuration (issuer, client, scopes, claims mapping) plus account-linking rules.
- Reset/MFA recovery policy and audit/error responses for each failure path.

## Workflow

1. Map every auth flow and its states, including failure, timeout, cancellation and re-entry paths.
2. Trace token/session lifecycle: issuance, refresh, rotation, revocation, logout and idle/absolute expiry.
3. Test the recovery paths on paper: reset, MFA loss, SSO linking conflict, device change and profile resolution failure.
4. Check denial/error/audit expectations for each flow, including enumeration and rate-limiting choices.
5. Produce the flow matrix with gaps and rank risks; separate what needs live testing (manual owner) from review findings.

## Output Format

Return, in this order:

1. Flow matrix: flow, entry, states, success/failure branch, revocation, evidence.
2. Token/session lifecycle table with rotation and expiry findings.
3. MFA/SSO/linking recovery edge table.
4. Risk-ranked findings with the recovery/failure test plan.

## Validation Checklist

- [ ] Every flow has an explicit state map including failure and recovery paths.
- [ ] Logout/revocation is verified as server-side effect, not only client redirect.
- [ ] Reset and MFA recovery paths are checked for identity-binding and rate limits.
- [ ] SSO/linking conflicts have a defined resolution and audit trail.
- [ ] Findings distinguish review evidence from live-test requirements.

## Gotchas

- Reviewing login only while reset and MFA recovery bypass the same controls.
- Treating a client-side token deletion as logout when the refresh token remains valid.
- Assuming SSO account linking is unique when the email claim is mutable.
- Claiming live login testing was run when no environment was supplied.

## Stop Conditions

Route a request to its real owner when it is that owner's deliverable (the complete expected-owner routing list exercised by trigger-evals):

- human-agent-trust-reviewer work -> `human-agent-trust-reviewer`.
- authority-invalidation-architect work -> `authority-invalidation-architect`.
- secrets-identity-hardener work -> `secrets-identity-hardener`.
- membership-invitation-designer work -> `membership-invitation-designer`.
- security-pr-reviewer work -> `security-pr-reviewer`.
- appsec-implementer work -> `appsec-implementer`.
- authorization-matrix-designer work -> `authorization-matrix-designer`.
- tenant-isolation-reviewer work -> `tenant-isolation-reviewer`.
- rls-policy-auditor work -> `rls-policy-auditor`.
- audit-log-architect work -> `audit-log-architect`.
- agent-authorization-matrix work -> `agent-authorization-matrix`.
- incident-response-runbook work -> `incident-response-runbook`.
- multi-tenant-security-tester work -> `multi-tenant-security-tester`.
- code-reviewer work -> `code-reviewer`.
- The caller wants this skill to implement, run or approve the change: refuse; return the artifact for the authorized owner.
- Required evidence is unavailable: state what is missing and mark the artifact UNVERIFIED instead of inventing facts.

## Supporting Files

- [auth-flow-matrix](references/auth-flow-matrix.md) - the named artifact, tables and completion checklist for this skill.
- [evals/evals.json](evals/evals.json) - the 6 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - the 22 trigger-discrimination cases (8 positive / 14 negative) against real manifest owners.

**Source:** docs/skills-catalog.md - Phase 4 security, RLS and supply-chain pack (Batch 5/D113); coverage: roadmap rows #108. The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
