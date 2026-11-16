# OWNER DECISION TABLE ADDENDUM — E3 item-2 corrected status (2026-11-10)

Basis: E3-ITEM2-OPEN-CASES-ANALYSIS-2026-11-10.md — 40063 B / a04c673ebef42d7dd1098a9994a152202d216b9913d9fbb6b1a57948f83fb366 (task-14; read-only; no repair).

## Corrected facts
- Ledger v5 (5,775 B / a9508664...): 18 PASS / 3 FAIL (CP-03, CP-09, CP-19) / 1 UNRUN (CP-17) / 0 BLOCKED, denominator 22; case_set_sha256 48a28ba1... .
- CP-22 PASS is matrix/closeout integrity, NOT item-2 22/22 acceptance. The current attempt is NOT accepted; E3.2 remains open.
- CP-09 is irreparable for this attempt (public commit metadata breach; owner CP-09=A keeps FAIL; prevention only). Structural ceiling: even closing CP-03/19/17 gives 21/22; only a NEW consumer-proof attempt can reach 22/22.
- CP-03: owner/acceptance decision on criterion-vs-documented-behaviour conflict (no explicit owner CP-03 line found; E0 refusal-to-waive is REPORTED).
- CP-19: repairable observation gap (fresh F2 session allowed by CP19-FIX-RECORD; no design change).
- CP-17: repairable observation gap (second-engine browser journey UNRUN; controls/HTTP PASS are supporting only).

## Tabled decisions added
| # | Decision | Known facts | Recommended option |
| --- | --- | --- | --- |
| T15 | E3 item-2 programme outcome | 18/3/1; CP-09 permanent; only new attempt can reach 22/22 | Option A now: publish bounded proof with no repair; do not claim item-2 acceptance |
| T16 | CP-03 disposition | criterion-vs-documented-behaviour conflict; owner CP03 line absent | Owner decision: keep FAIL / authorize R2 clarification / different control / behaviour change |
| T17 | CP-09 disposition | irreparable for this attempt; owner CP-09=A recorded | Confirm permanent FAIL + prevention; authorize a new attempt only if 22/22 is required |
| T18 | CP-19 disposition | repairable with fresh F2 session | Authorize fresh F2 (name oracle/model + examiner-key holder) or accept FAIL |
| T19 | CP-17 disposition | repairable second-engine run | Authorize second-engine/external-client run + durable evidence or accept UNRUN |
| T20 | E3.2 estimate for a new attempt | not reissued; new attempt needs its own bounded plan/estimate | Defer until T15 direction; no invented date |

## Effect
E3.2 remains open; no repair, ledger edit, acceptance or closure occurred. The bounded-proof/no-repair path (Option A) requires no new implementation authority and is the recommended immediate outcome; all others are owner-gated. No plan revision created.

Recorded by: Lead (DeepSeek Harness; route deepseek-flash). Local record only.