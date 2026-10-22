# Header and origin checklist: browser-boundary-reviewer artifact

Use this checklist to produce the review. Every row records evidence (file/config line) or UNVERIFIED.

## 1. Header policy table

| Header | Required value for this app | Enforcement point | Observed | Status | Evidence |
| --- | --- | --- | --- | --- | --- |
| Content-Security-Policy | default-src 'self'; frame-ancestors 'none'; object-src 'none' (tighten per asset inventory) | app middleware or CDN | <observed> | PASS/GAP/UNVERIFIED | <file:line> |
| Strict-Transport-Security | baseline max-age >= 15552000; includeSubDomains; preload requires max-age >= 31536000 + includeSubDomains + submission, only after audit | edge/CDN | <observed> | ... | ... |
| X-Frame-Options / frame-ancestors | DENY or none (frame-ancestors preferred) | app or edge | <observed> | ... | ... |
| Referrer-Policy | strict-origin-when-cross-origin or stricter | app or edge | <observed> | ... | ... |
| Permissions-Policy | camera/microphone/geolocation disabled unless needed | app or edge | <observed> | ... | ... |
| X-Content-Type-Options | nosniff | app or edge | <observed> | ... | ... |

Conflicting enforcement points (app sets one value, CDN another) are a finding, not a pass.

## 2. CSRF defense matrix

| Mutating endpoint | Method | Auth mechanism | Token | Origin/Referer check | Custom header | SameSite | Bypass paths noted |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <form/route> | POST | session cookie | yes/no | yes/no | yes/no | Lax/Strict/None | <e.g. top-level GET form, JSON content-type, Origin absent> |

Every row with no defense is a finding. Token must be bound to the session, single-use where appropriate, and checked server-side.

## 3. Cookie/session posture

| Cookie | Purpose | HttpOnly | Secure | SameSite | Domain/Path | Lifetime | Finding |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <name> | session | yes/no | yes/no | Lax/Strict/None | <scope> | <duration> | <none/gap> |

## 4. Review completion

- [ ] Every mutating endpoint, form and auth callback appears in sections 1-3 or is UNVERIFIED with the reason.
- [ ] Header conflicts between app and CDN are called out with both sources.
- [ ] Findings ranked by exploitability; unverified list is explicit.
- [ ] No code changes are made by this review; implementation goes to the manual-only owner.
