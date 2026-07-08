# Error Model Sheet

Detail tables for `error-taxonomy-designer`. Read on demand.

## Category → status → retryable reference

| Category | Example code | Status class | Fault | Retryable |
|---|---|---|---|---|
| Invalid input / validation | `validation.field_required` | 4xx (400/422) | client | No — fix the request |
| Unauthenticated | `auth.unauthenticated` | 401 | client | No — authenticate |
| Forbidden | `auth.forbidden` | 403 | client | No — lacks permission |
| Not found | `resource.not_found` | 404 | client | No |
| Conflict / invalid state | `state.conflict` | 409 | client | No — resolve conflict |
| Rate limited | `rate.limited` | 429 | client | Yes — after `retryAfter` |
| Quota / entitlement | `entitlement.exceeded` | 403/402 | client | No — until plan changes |
| Dependency unavailable | `dependency.unavailable` | 503 | dependency | Yes — backoff |
| Timeout | `dependency.timeout` | 504 | server/dependency | Yes — backoff, idempotent only |
| Internal | `internal.error` | 500 | server | Sometimes — treat as transient |

Codes are namespaced and additive-only once shipped. Status is the
transport mapping; the code is the stable contract clients branch on.

## Envelope schema

```json
{
  "code": "validation.field_required",
  "message": "Email is required.",
  "details": [
    { "field": "email", "code": "required", "message": "Email is required." }
  ],
  "correlationId": "01J...",
  "retryable": false,
  "retryAfter": null
}
```

- `code` — stable, machine-readable, namespaced. The contract.
- `message` — human, actionable, localizable, keyed by `code`.
- `details` — structured per-field (or per-item) errors; never a
  concatenated string.
- `correlationId` — opaque to the caller, joinable to server logs.
- `retryable` / `retryAfter` — a field to branch on, not prose.

## Disclosure do / don't

DO put in the caller-visible message:
- What went wrong in the caller's terms.
- What the caller can do about it.
- A stable code and a correlation id.

NEVER put in the caller-visible message:
- Stack traces or exception class names.
- SQL, query text, or ORM internals.
- Internal hostnames, file paths, IP addresses, service names.
- Another subject's data, or any PII not already the caller's own.
- Secrets, tokens, connection strings.

Unmapped/unexpected failures → single generic `internal.error` +
`correlationId`. The real detail is logged server-side only, after
redaction (`observability-operator` owns emission + redaction).

## Mapping boundary

One error-handling layer maps exceptions → taxonomy:

```
request → handler → (throws) → error middleware:
    known AppError      → map to its code + envelope
    validation error    → validation.* + field details
    unmapped exception   → internal.error + correlationId (log full detail)
```

No route or service invents its own error shape. This single funnel is
what makes the disclosure rule and cross-surface consistency enforceable.

## Cross-surface carry

| Surface | How the code carries |
|---|---|
| Sync HTTP | status + envelope in body |
| Background job | job result record: `{ code, message, correlationId }` |
| Webhook (outbound) | envelope in payload; delivery status separate (api-event-architect) |
| CLI / RPC | exit/status mapping documented once |

Same logical failure → same `code` everywhere; only the transport frame
differs.
