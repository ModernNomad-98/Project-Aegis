---
name: membership-invitation-designer
description: 'Designs the membership-invitation workflow on top of the tenant model''s invitation state machine: the invitation record and single-use token semantics (unguessable, expiring, one acceptance, revocation wins), identity binding at acceptance, seat checks against the plan''s seat pool, invite-spam limits, re-invite and bulk-invite paths, and audit hooks. Produces the design only — sends nothing, generates no tokens, executes nothing. Use when asked to design or repair invitation flows: invite-by-email, token/link acceptance, identity binding, expiry/revocation, seat limits, spam prevention, re-invites, bulk invites. Do NOT use for invitation state semantics (tenant-modeler), who-may-invite or role-grant rules (authorization-matrix-designer), plan seat limits (plan-entitlement-architect), the invitation email/notification UX (notification-webhook-ux-designer), token generation or storage hardening (secrets-identity-hardener), or executable cross-tenant negative suites (multi-tenant-security-tester).'
---

# Membership Invitation Designer

**Reading key:** SaaS is software as a service. An invitation is a scoped
offer to join a tenant: a record (invitee, role carried, expiry) plus a
single-use token that binds an identity to a membership on acceptance. A seat
is one membership slot the plan's entitlement pool allows. Identity binding is
the rule that decides which account an acceptance attaches to — email match,
existing-account handling, and the races that follow.

## Purpose

Produce the membership-invitation workflow design on top of
`tenant-modeler`'s invitation state machine (compose, never restate): the
invitation record and single-use token semantics, identity binding at
acceptance, seat checks against the plan's seat pool, invite-spam limits,
re-invite and bulk-invite paths, and audit hooks. It sends nothing, generates
no tokens, and executes nothing.

## Use When

- Use when: designing or repairing invite-by-email flows, token/link acceptance, or identity binding.
- Use when: expiry/revocation races, seat limits, or invite-spam prevention need a design.
- Use when: re-invite and bulk-invite paths need explicit semantics.
- Do NOT use when: the ask is invitation STATE semantics (states, transitions, who-may-invite) — that is `tenant-modeler` (compose its state machine).
- Do NOT use when: the ask is who-may-invite or role-grant rules — that is `authorization-matrix-designer` (compose, including the #59 extension's grant ceiling: an invitation carries a role grant, so the ceiling governs which role an inviter may put in an invite).
- Do NOT use when: the ask is plan seat limits themselves — that is `plan-entitlement-architect`.
- Do NOT use when: the ask is the invitation EMAIL/notification UX — that is `notification-webhook-ux-designer`.
- Do NOT use when: the ask is token generation or storage hardening — that is `secrets-identity-hardener` *(manual-only)*; this skill designs token SEMANTICS only.
- Do NOT use when: the ask is an executable cross-tenant negative suite — that is `multi-tenant-security-tester` *(manual-only)*; the design names the negative cases, the tester builds the suite.

## Inputs to Inspect

1. The tenant model and its invitation state machine (`tenant-modeler` output): states, transitions, who-may-invite, role-carried — the workflow rides on it.
2. The authorization matrix (`authorization-matrix-designer` output, including the #59 extension's grant-ceiling and custom-role rules): which role an inviter may grant in an invite — composed, never restated.
3. The entitlement/seat pool (`plan-entitlement-architect` output): how many seats the plan allows and what happens at the limit.
4. The rate-limit contract (`api-event-architect` output): per-inviter and per-tenant limits the spam controls compose.
5. Existing invite code paths and their de facto behavior.
6. The audit taxonomy (`audit-log-architect` output): invitation sent/accepted/revoked hooks.

## Workflow

1. **Map the invitation entry points.** Invite-by-email, resend, bulk invite, acceptance link — name each path the state machine serves.
2. **Design the record and token semantics.** Single-use, unguessable, expiring; one acceptance; the revocation-vs-acceptance race decided (revocation wins per the catalog's rule — cited, not restated). Token mechanics stay with `secrets-identity-hardener`.
3. **Name the identity-binding rules.** What binds the invitee to an account: email match rules, existing-account handling, and the acceptance race outcomes.
4. **Compose seat checks and spam limits.** Seat checks read the plan's seat pool (composed, not restated); behavior at the limit named (deny/queue/upgrade prompt). Spam limits compose the rate-limit contract per inviter and per tenant.
5. **Enumerate the negative cases.** Expired token, reused token, revoked-vs-acceptance race, cross-tenant acceptance, seat-limit race — each named with its expected denial.
6. **Emit the design** in the Output Format, stating what was chosen, why, and the main rejected alternative.

## Output Format

Emit the design in the conversation (nothing is written to the repo):

```
INVITATION DESIGN — <product>
Record: <invitee, role carried (composed ceiling), expiry, state per tenant-modeler>
Token semantics: <single-use, unguessable, expiry, one acceptance, revocation wins>
Identity binding: <email match rules, existing-account handling, race outcomes>
Seat checks: <composed plan seat pool; behavior at the limit (deny/queue/upgrade)>
Spam limits: <per-inviter / per-tenant composed rate limits>
Re-invite & bulk: <resend semantics; bulk path and its failure handling>
Negative cases: <expired | reused | revocation race | cross-tenant | seat race — expected denial>
Audit hooks: <sent/accepted/revoked composed from audit-log-architect>
Out of scope:
  state semantics → tenant-modeler; role grants → authorization-matrix-designer;
  seat pool → plan-entitlement-architect; email UX → notification-webhook-ux-designer;
  token hardening → secrets-identity-hardener; executable suites → multi-tenant-security-tester
Chosen / why / rejected: <the key choices, the reason for each, and the main
  rejected alternative>
```

## Validation Checklist

- [ ] The token is single-use, unguessable, and expiring, with the revocation-vs-acceptance race decided (revocation wins — cited from the catalog, not restated).
- [ ] Identity-binding rules are named: email match, existing-account handling, and each race outcome.
- [ ] Seat checks compose the entitlement matrix, never restate it; behavior at the limit is named.
- [ ] Spam limits compose the rate-limit contract per inviter and per tenant.
- [ ] Every negative case names its expected denial; no executable suite is claimed here.
- [ ] The design sends nothing, generates no tokens, and executes nothing.

## Gotchas

- Reusable links become standing credentials: a token that accepts twice, or never expires, is an open invitation to the tenant.
- Acceptance without identity binding opens account takeover: whoever holds the link becomes the member unless the binding rule decides otherwise.
- Seat checks enforced client-side only are theater; the seat decision must live where the membership is created.
- Invite spam is a tenant-exhaustion vector: unbounded invites let one inviter burn seats and rate budgets; the limits compose the shipped contract.
- Restating the state machine, the grant ceiling, or the seat pool duplicates their owners and drifts when they change — cite, never copy.

## Tenant Isolation Rules

- An invitation binds to exactly one tenant; acceptance never crosses tenants — an invitee of tenant A cannot accept into tenant B.
- Invitee data from another tenant is never enumerated (no "does this email exist in tenant B" oracle).
- Cross-tenant acceptance attempts are a named negative case with an expected denial.

## Stop Conditions

- No tenant model or invitation state machine exists or is findable → stop; `tenant-modeler` runs first.
- The ask becomes generating tokens, sending email, or implementing the flow → implementation is a separate task; this skill designs only.
- The ask involves live-state mutation or destructive action → stop and refuse.

## Supporting Files

- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `tenant-modeler`, `authorization-matrix-designer`, `plan-entitlement-architect`, `api-event-architect`, `notification-webhook-ux-designer`, `secrets-identity-hardener`, `audit-log-architect`, and `multi-tenant-security-tester`.
- `references/` — None: the design is self-contained.
