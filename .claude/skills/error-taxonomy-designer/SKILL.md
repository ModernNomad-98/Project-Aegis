---
name: error-taxonomy-designer
description: Design the error model for an API or product surface — a finite, stable taxonomy of error categories with machine-readable codes, an error envelope (code, human message, field-level details, correlation id, retryable flag), an honest client-fault vs server-fault vs retryable split, actionable messages that say what to DO, ONE mapping boundary where exceptions become taxonomy errors, and a disclosure rule that keeps stack traces, internal identifiers, and PII out of what the caller sees. Owns the error MODEL and its wire/copy discipline; the endpoint contract carrying it is api-event-architect's, and rendering the error STATE in the UI is edge-state-ux-designer's. Use when designing or unifying error responses, error codes, or an error envelope, or when errors are inconsistent, leaky, or tell the user nothing they can act on. Do NOT use to design the API contract itself (api-event-architect) or the empty/loading/error UI (edge-state-ux-designer).
---

# Error Taxonomy Designer

## Purpose

Errors are the part of an API nobody designs and everybody hits. Left
ad-hoc, they become a mess: the same failure returns `400` on one route
and `500` on another, messages read `Error: undefined` or dump a stack
trace with a database DSN in it, clients string-match human copy because
there is no stable code, and nothing tells the user whether retrying
helps. This skill produces the error MODEL for a surface — a finite
taxonomy of categories with stable machine codes, one envelope shape,
an honest classification of whose fault each error is and whether it is
retryable, message discipline that is actionable without leaking
internals or PII, and a single boundary where raw exceptions are mapped
into the taxonomy. It owns the error model; carrying it over the wire is
`api-event-architect`'s contract, and painting the error on screen is
`edge-state-ux-designer`'s.

## Use When

- Use when: designing the error responses for a new API/surface, or
  defining error codes and an error envelope.
- Use when: errors are inconsistent across routes/surfaces (same failure,
  different status/shape), or messages are unactionable or leaky.
- Use when: clients are forced to string-match human message text because
  there is no stable machine-readable code to branch on.
- Use when: exceptions bubble to callers as `500`s with stack traces, or
  a failure's retryability is unclear.
- Do NOT use when: the task is the overall API contract — routes,
  versioning, idempotency, rate limits, webhook envelopes — that is
  `api-event-architect`; this skill designs the error model inside it.
- Do NOT use when: the task is how the UI RENDERS an error/empty/loading
  state (inline vs toast, retry affordance, copy placement) — that is
  `edge-state-ux-designer`, which consumes this taxonomy.
- Do NOT use when: the concern is broad sensitive-data disclosure policy
  beyond error messages — defer the general policy to the relevant
  disclosure/PII skill; this skill owns only what error responses expose.

## Inputs to Inspect

1. The current failure surface: how errors are produced and returned
   today across routes, background jobs, and any webhook/callback paths —
   status codes used, response shapes, message strings, from code and
   logs.
2. The consumers: who reads these errors (first-party UI, third-party
   integrators, internal callers) and how they branch on them — a stable
   contract matters more the more external the consumer.
3. Localization/i18n needs: whether human messages must be translated,
   which forces the machine-code / display-message separation.
4. Sensitive-data exposure: what internal detail currently leaks into
   messages (stack traces, SQL, hostnames, other users' data, PII) — the
   disclosure rule must close these.
5. Existing conventions to stay compatible with: any error codes clients
   already depend on (a live contract), the platform's status-code norms,
   and correlation-id / tracing setup (from `observability-operator`).

## Workflow

1. **Inventory and cluster today's failures.** Collect the distinct
   failure modes and how each is currently surfaced. Cluster them — most
   collapse into a small set of categories once the accidental variety is
   removed.
2. **Define the taxonomy.** A finite, stable set of categories, each with
   a machine-readable code (namespaced, e.g. `validation.field_required`)
   and a mapped transport status. Typical spine: invalid input /
   validation, unauthenticated, forbidden, not-found, conflict / invalid
   state, rate-limited, quota / entitlement exceeded, dependency
   unavailable, timeout, internal. Codes are additive-only once shipped —
   treat them as contract.
3. **Design the envelope.** One shape for every error: stable `code`,
   human `message`, optional structured `details` (e.g. per-field
   validation errors), a `correlationId` tying it to server logs, and an
   explicit `retryable` boolean (and where relevant a `retryAfter`).
   Field-level errors get their own sub-structure, not a concatenated
   string.
4. **Classify fault and retryability honestly.** Map each category to
   client-fault (4xx — the caller must change the request) vs server/
   dependency-fault (5xx). Mark which are safely retryable and under what
   condition (idempotency, backoff, `retryAfter`) — a validation error is
   never retryable as-is; a `503`/timeout usually is. State it per
   category, not per hunch.
5. **Set message discipline.** Human messages are actionable — they say
   what the caller can DO, in their language, keyed by the stable code
   (not the reverse). The message NEVER contains a stack trace, SQL,
   internal hostname/path, another subject's data, or PII. Unexpected/
   unmapped failures return a single generic internal error + correlation
   id; the real detail is logged server-side only.
6. **Pin the mapping boundary.** Exceptions are translated into the
   taxonomy at ONE layer (a middleware / error handler), not scattered
   `try/catch`es each inventing a response. Anything unmapped falls
   through to the generic internal error — never to a raw exception. This
   is what keeps consistency and disclosure guarantees enforceable.
7. **Enforce consistency across surfaces.** The same logical failure
   returns the same code/shape whether it happens on a sync request, a
   background job result, or a webhook payload. Note where transport
   differs (a job can't return an HTTP status) and how the code carries.
8. **Name the handoffs.** Rendering of each state → `edge-state-ux-designer`;
   the envelope's place in the wire contract and code versioning/
   deprecation → `api-event-architect`; correlation-id emission and
   redaction-before-logging → `observability-operator`.
9. **Deliver** the taxonomy, envelope, and retry/disclosure rules in the
   Output Format.

The category→status→retryable reference table, envelope schema, and
disclosure do/don't list:
[references/error-model-sheet.md](references/error-model-sheet.md).

## Output Format

```
ERROR MODEL — <surface/API>
Envelope:     { code, message, details?, correlationId, retryable, retryAfter? }
Taxonomy (per category):
  <category>: code=<namespace.slug> status=<4xx|5xx> fault=<client|server|dependency>
  retryable=<no|yes: condition> message-pattern="<actionable, code-keyed>"
Mapping boundary: <single layer that maps exceptions → taxonomy; unmapped → internal+corrId>
Disclosure rule: messages exclude <stack traces, SQL, hostnames, other-subject data, PII>;
                 detail logged server-side only, keyed by correlationId
Cross-surface: <how the same code carries on API / job / webhook>
Versioning:   codes additive-only; removals/renames → api-event-architect deprecation
Handoffs:     rendering → edge-state-ux-designer; wire contract → api-event-architect;
              correlation/redaction → observability-operator
```

## Validation Checklist

- [ ] The taxonomy is finite and each category has a stable, namespaced
      machine code distinct from the human message.
- [ ] One envelope shape covers every error; field-level errors are
      structured, not concatenated into one string.
- [ ] Every category is classified client vs server/dependency fault and
      marked retryable (with condition) or not — no unclassified errors.
- [ ] Messages are actionable and NEVER carry stack traces, SQL, internal
      hosts/paths, other subjects' data, or PII.
- [ ] Unmapped/unexpected failures return a single generic internal error
      plus a correlation id; detail is logged server-side only.
- [ ] Exceptions are mapped to the taxonomy at ONE boundary, not in
      scattered handlers.
- [ ] The same logical failure yields the same code across sync, job, and
      webhook surfaces.
- [ ] Rendering, wire-contract, and correlation/redaction concerns are
      handed to their owning skills, not redesigned here.

## Gotchas

- Human message text is not an API — but the moment clients branch on it,
  it becomes one, and every copy edit is a breaking change. Give clients
  a stable code to branch on and keep the message for humans.
- A leaked stack trace or SQL string in an error message is a security
  finding, not a cosmetic one: it hands an attacker your internals. The
  disclosure rule is a hard boundary, not a nicety.
- "Retryable" is a property of the failure, not the client's optimism.
  Marking a validation error retryable invites clients to hammer a
  request that can never succeed; marking a transient `503`
  non-retryable makes them give up on a blip.
- Scattering exception→response mapping across dozens of `catch` blocks
  guarantees drift: someone will return a bare `500` with the raw error.
  One boundary is what makes the guarantees enforceable.
- `4xx` vs `5xx` is a promise about whose fault it is; a `500` on bad
  input tells the caller to page an on-call for their own typo. Classify
  fault deliberately.
- A generic internal error with NO correlation id is undebuggable; one
  that dumps the exception is unsafe. The correlation id is the bridge —
  opaque to the caller, joinable in logs.
- Codes are contract. Renaming `auth.expired` to `authentication.token_expired`
  post-launch breaks every client switching on it — route removals/renames
  through `api-event-architect`'s deprecation window.

## Stop Conditions

- The request is really to design the whole API contract (routes,
  envelopes for success, versioning, rate limits) → route to
  `api-event-architect`; this skill designs only the error model within
  it.
- The request is how to render the error/empty/loading state in the UI
  (placement, retry affordance, copy tone) → route to
  `edge-state-ux-designer`; this skill produces the codes/messages it
  consumes.
- Changing an already-published error code would break live consumers →
  flag it as a contract-breaking change for `api-event-architect`'s
  deprecation process; do not silently rename or repurpose a code.
- A required message must include internal detail (e.g. "expose the
  failing downstream host to help partners debug") → surface the
  disclosure risk and offer the correlation-id + support-channel
  alternative to a human before weakening the rule.

## Supporting Files

- [references/error-model-sheet.md](references/error-model-sheet.md) —
  category→status→retryable reference table, the envelope schema, a
  field-error sub-structure, and the disclosure do/don't list.
- `evals/evals.json` — behavior cases including the unify-inconsistent-
  errors path, the retryability classification, and the leaked-internals
  refusal.
- `evals/trigger-evals.json` — discrimination against `api-event-architect`
  (the contract) and `edge-state-ux-designer` (rendering the state).
