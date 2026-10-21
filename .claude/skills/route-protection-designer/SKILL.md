---
name: route-protection-designer
description: 'Use when routes need gates: design auth, role, onboarding and admin protection consistently, server enforcement as source of truth, explicit redirect/denied/deep-link behavior.'
---

# Route Protection Designer

Terms: **family 14** - the discipline family in README.md and docs/skills-catalog.md; **read-only** means this skill inspects and returns guidance/records and never edits code or runs production actions.

## Purpose

Design route protection consistently: a per-route gate taxonomy (auth/role/onboarding/admin), server enforcement as the source of truth, explicit redirect/denied/deep-link flows, client checks as UX-only, and the negative tests that prove denials.

The skill is **advisory and auto-invocable**. It produces guidance, records and review structure only; it does not edit code, run commands, use the network or grant production authority. Any implementation, execution or approval is a delegated host/user action under existing authority. It composes the nearest owners rather than duplicating them.

## Use When

- Routes need auth, role, onboarding or admin gates and behavior is inconsistent.
- A deep link or redirect flow can bypass or break a gate.
- Client route guards are being treated as a security boundary.
- Denied/redirect/onboarding flows need explicit behavior per route.

**Do not use when:** the request belongs to a named neighbouring owner (see Stop Conditions), or when inspection evidence is unavailable and the question would have to be answered by guessing.

## Inputs to Inspect

- Route table and the protected capability per route.
- Auth/role model and server enforcement facts (middleware, RLS, API checks).
- Onboarding states and what each gated route requires.
- Current redirect/deep-link behavior and known bypass reports.
- Negative-test expectations for unauthorized access.

## Workflow

1. Build the route x gate matrix: auth, role, onboarding, admin, and the required capability per route.
2. Name the server enforcement for each gate and mark enforcement gaps explicitly.
3. Define denied/redirect behavior: 401/403 vs onboarding redirect vs not-found hiding, per route class.
4. Define deep-link return behavior so a gated link returns the user to the requested destination after auth.
5. Confirm client guards are UX-only and cannot be the sole enforcement.
6. Define negative tests for unauthorized/under-privileged access per gate class.
7. Return the gate matrix, denial flows, trust-boundary note and test plan; do not implement routes.

## Output Format

Return, in this order:

1. Route x gate matrix with required capability and enforcement source.
2. Redirect/denied/onboarding behavior per route class.
3. Deep-link return contract.
4. Trust-boundary note (client UX vs server truth).
5. Negative-test plan and enforcement gaps.

## Validation Checklist

- Every gated route names its capability and server enforcement source.
- Denied/redirect/onboarding behavior is explicit per route class.
- Deep-link return is defined and cannot bypass the gate.
- Client guards are labeled UX-only; enforcement gaps are named.
- Negative tests cover unauthorized and under-privileged access.
- No route or server code was edited or enforcement claimed.

## Gotchas

- A client route guard that hides UI is not authorization; treat it as UX and name the server check.
- A deep link that redirects to a generic home page loses the user's destination; define the return contract.
- Onboarding gates and role gates can conflict; state the precedence per route.
- Hiding a route versus returning 403 is a product decision; make it explicit.

## Stop Conditions

- The request is roles/permissions/object-level authorization matrix: route to `authorization-matrix-designer`.
- The request is cross-tenant leakage review: route to `tenant-isolation-reviewer`.
- The request is security review of an actual diff: route to `security-pr-reviewer`.
- The trigger-evals file lists a broader 14-owner discrimination set (all named in the reference Boundaries); the three routes above are the primary Stop Conditions.
- The caller wants this skill to implement, provision or execute the design: refuse; return the design for the authorized host/user.
- Required evidence (routes, state, cache config or policy) is unavailable: state UNKNOWN and ask instead of inventing it.

## Supporting Files

- [route-protection-matrix](references/route-protection-matrix.md) - Route protection matrix: gates, denials and negative tests.
- [evals/evals.json](evals/evals.json) - the 6 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 8 positive and 14 negative trigger-discrimination cases against the nearest owners.

**Source:** docs/skills-catalog.md - D12.2 product engineering craft pack (Batch 3/D110); coverage roadmap #164. The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
