# Security baseline checklist: security-drift-detector artifact

## 1. Baseline record

| Item | Value |
| --- | --- |
| Baseline source | <audit/review/config snapshot path + hash> |
| Baseline date | <YYYY-MM-DD> |
| Scope | <areas and controls covered> |
| Out of scope | <explicitly not covered; becomes UNVERIFIED> |
| Baseline authority | <owner who can re-baseline> |

## 2. Control comparison

| Control | Expected (baseline) | Current (evidence) | Classification | Criticality | Owner/action |
| --- | --- | --- | --- | --- | --- |
| Password KDF cost | Argon2id cost params recorded | <observed config/code> | SAME / REMOVED / NARROWED / DEFAULT-CHANGED / UNDOCUMENTED / EXPIRED | H/M/L | <owner + action> |
| RLS tenant predicate | policy present on all tenant tables | <observed> | ... | ... | ... |
| Auth session revocation | server-side revocation | <observed> | ... | ... | ... |
| CI security job | SAST blocking on changed code | <observed> | ... | ... | ... |

Rules: cite evidence for both columns; never mark SAME without current evidence; planned change must cite its change record.

## 3. Weakening classes

| Class | Definition | Example |
| --- | --- | --- |
| REMOVED | control no longer exists | security job deleted |
| NARROWED | control applies to fewer cases | RLS predicate missing on new table |
| DEFAULT-CHANGED | framework/plan default weakened | debug mode enabled |
| UNDOCUMENTED | change without a change record | policy edited silently |
| EXPIRED | evidence or control past its review date | stale audit baseline |

## 4. Completion checklist

- [ ] Baseline recorded with source/date/scope.
- [ ] Every difference has both-sides evidence.
- [ ] Planned changes cite their change record.
- [ ] Unowned/expired controls are surfaced with owner/action.
- [ ] Re-baseline recommendation is stated; no live probing performed.
