---
name: browser-boundary-reviewer
description: 'Use when a web app''s browser/origin boundary or security-header policy needs review: mutation paths, cookies/SameSite, origins/CORS, CSRF defenses and CSP/HSTS/frame/referrer/permissions/content-type headers, especially after an auth or cookie change. Do NOT use for a per-PR security diff review (security-pr-reviewer) or hands-on control implementation (appsec-implementer); this skill reviews the whole origin/header surface and writes no code.'
---

# Browser Boundary Reviewer

Terms: **family 5** - Security, RLS & supply chain (README roster family 5; docs/skills-catalog.md Phase 4 security, RLS and supply-chain pack); **advisory/design-only** means this skill produces guidance and records and never edits code, runs commands or grants production authority.

## Purpose

Review a web application browser/origin boundary and security-header policy as one review: inventory every mutating endpoint, form and auth callback; assess cookie attributes and SameSite posture; build the CSRF defense matrix (token, origin check, custom header, SameSite) with bypass paths; produce a header policy table with enforcement point (application vs CDN/proxy) and required values; rank findings with evidence and list what could not be verified.

The skill is **auto-invocable and advisory/design-only**. It produces the named artifact below with evidence and open questions; it does not edit code, run commands, use the network or grant production authority. Implementation and approval are delegated host/user actions. It composes the named neighbouring owners instead of duplicating them.

## Use When

- A concrete request like: Review our web app browser boundary and security headers before we ship the new login flow.
- The named artifact is missing, disputed or about to be built against a wrong assumption.
- A review/spec must record the artifact, its edge cases and the boundary owners explicitly.
- An implementation is about to start and the ask is for the artifact it must build against.

**Do not use when:** the request belongs to a named neighbouring owner (the complete routing list is in Stop Conditions) or when no evidence exists and the answer would be invention.

## Inputs to Inspect

- Route table, forms and mutation endpoints (method, path, auth requirement, CSRF mechanism) from the app router and server handlers.
- Cookie configuration (names, attributes, SameSite, domain/path, secure, lifetime) and session storage location.
- Header configuration at each enforcement point (app middleware, CDN/proxy, framework defaults) for CSP, HSTS, frame-ancestors, referrer-policy, permissions-policy and content-type.
- CORS configuration (allowed origins, credentials, methods, headers) and auth callbacks/redirect allowlists.

## Workflow

1. Inventory every mutating endpoint, form and auth callback; mark same-origin vs cross-origin and state-changing vs read-only.
2. Assess cookies and session boundary: SameSite posture, secure/domain scope, and where session state lives.
3. Build the CSRF defense matrix (token, origin check, custom header, SameSite) per mutating endpoint and list bypass paths.
4. Build the header policy table per enforcement point and flag conflicting or missing headers (CSP as defense-in-depth, not the CSRF fix).
5. Rank findings by exploitability and evidence strength; list what could not be verified (CDN config not supplied, etc.).

## Output Format

Return, in this order:

1. Origin/boundary inventory: every mutating endpoint, form and callback with its CSRF defense(s).
2. Cookie/SameSite posture table with violations.
3. CSRF defense matrix with bypass paths per endpoint.
4. Header policy table (header, required value, enforcement point, status, evidence).
5. Ranked findings with file/config evidence and unverified list.

## Validation Checklist

- [ ] Every mutating endpoint is in the origin inventory and has a CSRF defense named.
- [ ] Cookie attributes and SameSite posture are assessed against the session boundary, not assumed.
- [ ] Header table names the enforcement point (app vs CDN) and flags conflicts.
- [ ] CSP claims are defense-in-depth, not asserted as the CSRF control.
- [ ] Unverified items (e.g. CDN config not supplied) are labelled, never guessed.

## Gotchas

- Treating a CSP presence as CSRF protection: browsers do not block form posts to same-origin endpoints on CSP alone.
- Reviewing only the framework default config while the CDN/proxy rewrites or strips headers.
- Assuming SameSite=Lax covers cross-site POSTs from embedded or top-level navigation cases.
- Reading cookie flags without checking which host actually sets the cookie.

## Stop Conditions

Route a request to its real owner when it is that owner's deliverable (the complete expected-owner routing list exercised by trigger-evals):

- security-pr-reviewer work -> `security-pr-reviewer`.
- appsec-implementer work -> `appsec-implementer`.
- cloud-security-baseline-reviewer work -> `cloud-security-baseline-reviewer`.
- vite-build-qa-engineer work -> `vite-build-qa-engineer`.
- secrets-identity-hardener work -> `secrets-identity-hardener`.
- authorization-matrix-designer work -> `authorization-matrix-designer`.
- clickthrough-test-engineer work -> `clickthrough-test-engineer`.
- multi-tenant-security-tester work -> `multi-tenant-security-tester`.
- rls-policy-auditor work -> `rls-policy-auditor`.
- threat-modeler work -> `threat-modeler`.
- security-impact-note-author work -> `security-impact-note-author`.
- security-regression-harness-designer work -> `security-regression-harness-designer`.
- secure-migration-reviewer work -> `secure-migration-reviewer`.
- code-reviewer work -> `code-reviewer`.
- The caller wants this skill to implement, run or approve the change: refuse; return the artifact for the authorized owner.
- Required evidence is unavailable: state what is missing and mark the artifact UNVERIFIED instead of inventing facts.

## Supporting Files

- [header-and-origin-checklist](references/header-and-origin-checklist.md) - the named artifact, tables and completion checklist for this skill.
- [evals/evals.json](evals/evals.json) - the 6 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - the 22 trigger-discrimination cases (8 positive / 14 negative) against real manifest owners.

**Source:** docs/skills-catalog.md - Phase 4 security, RLS and supply-chain pack (Batch 5/D113); coverage: roadmap rows #110, #120. The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
