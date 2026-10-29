# CP-19 rescore + CP-09 prevention line (owner decisions 2026-10-29 ~10:05-10:07 PDT)

**Source: Peter, typed directly in the Project Aegis DSH Web GUI Lead session at approximately 2026-10-29 10:05-10:07 PDT.**

## CP-19 — RESCORED RUN = FAIL
- Owner: "CP-19 is rescored RUN = FAIL (13/14, F2 failing). It ran; it produced a verdict. 'UNRUN' was wrong."
- Evidence: batch CP19C-22799eb0be91 executed 14 fixtures with 14 fresh Claude Code oracle sessions; **13 PASS / 1 FAIL** (F2-late-revocation: decision correct but required `authority_state=unresolved` absent; resolved chronology returned). Batch verdict FAIL; the case therefore RUN = FAIL. Owner decision CP-19=A (keep unresolved requirement; gap logged in #966 comment 6497612788) remains the disposition basis.
- Row update: CP-19 = **FAIL (run)**; no longer UNRUN. Residuals: unresolved F2 is a genuine negative-case finding, not a pass; no R2 revision.

## CP-09 — FAIL stands; future prevention line
- Owner: "CP-09: A. FAIL stands; final ledger records it. Add one line to the closeout naming the gap (plan-forbidden names/PR numbers and a personal name in public commit metadata) as a future prevention item - no retroactive exception, no history rewrite."
- Closeout line (for D121 and the program closeout): **Prevention item:** future consumer-repo commits must avoid plan-forbidden product names, PR numbers and personal names in public commit metadata (messages and added lines), since public history cannot be rewritten; this gap is recorded as CP-09 FAIL, not retroactively excepted.

## Ledger effect (to be applied in the final consolidated ledger)
- CP-19: UNRUN -> **RUN = FAIL** (13/14, F2 failing).
- CP-09: FAIL stands (public commit metadata breach; prevention item recorded).
- CP-22: pending final cycle (PASS or FAIL at the 60-min box; UNRUN not an outcome of a cycle that ran).
- CP-21: pending CP-21=B selector verdict (stale dispatch rejected after selector; served aggregate unchanged).
- Final ledger must show every non-browser row as PASS or FAIL; browser rows state UNRUN/result as of export; FAIL rows published as FAIL.

## U6 consequence (owner: condition (i) = C)
- U6 export proceeds only when CP-21(B) has its verdict, CP-22 has its verdict, and every non-browser row is PASS or FAIL. Browser rows state UNRUN or their result as of export time. FAIL rows published as FAIL.