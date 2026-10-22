# Auth-flow matrix: authentication-flow-reviewer artifact

## 1. Flow matrix

| Flow | Entry point | States/branches | Revocation on logout | Recovery path | Evidence |
| --- | --- | --- | --- | --- | --- |
| Login | /login (password) | pre-auth -> MFA-pending -> authenticated | session revoked | reset via email | <file:line> |
| Logout | /logout | authenticated -> revoked -> same-device | all tokens revoked? | re-login | ... |
| Password reset | /forgot | request -> token issued -> consumed/expired | sessions revoked after reset? | resend | ... |
| MFA enroll/verify | /mfa | unenrolled -> pending -> enrolled | removed on disable? | recovery codes | ... |
| SSO initiate/callback | /sso | discovery -> IdP -> callback -> linked | IdP session logout? | account linking | ... |
| Account linking | /link | unlinked -> pending -> linked/conflict | unlink path | admin/self-serve | ... |
| Session refresh | silent refresh | active -> rotated -> expired | refresh reuse detection? | re-auth | ... |

Every cell is evidence-cited or marked UNVERIFIED.

## 2. Token/session lifecycle

| Token | Storage | Lifetime | Rotation | Revocation | Finding |
| --- | --- | --- | --- | --- | --- |
| session cookie | HttpOnly cookie | <duration> | on privilege change? | server-side | <gap> |
| refresh token | <storage> | <duration> | rotation with reuse detection? | revoke family | ... |
| ID/access token | <storage> | <duration> | n/a | short expiry | ... |

## 3. Recovery edge cases

| Edge case | Expected behaviour | Observed | Finding |
| --- | --- | --- | --- |
| Password reset with active sessions | all sessions revoked | <obs> | <gap> |
| MFA lost, recovery code used | codes single-use, audit | <obs> | ... |
| SSO email changed at IdP | link conflict handled | <obs> | ... |
| Profile resolution failure | bounded error, no partial auth | <obs> | ... |

## 4. Completion checklist

- [ ] Every flow has a state map with failure/recovery branches.
- [ ] Revocation is server-side and verified.
- [ ] Recovery paths are identity-bound and rate-limited.
- [ ] Findings name whether live testing is required (manual owner) or review evidence suffices.
