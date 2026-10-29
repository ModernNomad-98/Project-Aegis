# AUDIT SUMMARY v4 — Item 2 consumer plan, focused re-check of the two conditions

**Postable summary. One verdict, the evidence for it, and what it does not license.**
**Audit record:** ITEM2-STAGE-B-REAUDIT-v4.md (this directory). **Audited package:** item2-consumer-plan/v4/. **Auditor:** RV-1, fresh focused re-checker, 2026-10-28 16:19–16:26 PDT, approximately 6.5 minutes. No provider calls; local bytes only.

---

## Verdict

**C-1 CLOSED. C-2 CLOSED. D-3, D-4, D-5, D-6, D-7 applied.**

**The plan may be treated as ACCEPTED at plan level — all conditions discharged — for the content path already underway.** Three observations are recorded as non-blocking notes (below); none is a condition, and none touches a step, gate, stop rule, producer, evidence artifact, hash or authority row.

**Plan acceptance is not code acceptance.** There is no code. This verdict authorises content work only, creates no authority, and may not be cited as a case PASS.

## Why C-1 is closed

The v3 finding was that A1's summary table contradicted the operative sequence: section 13's U6 row said U6 blocks "CP-22, durable evidence, Item 2 closeout", and R11 said "Closeout … stay[s] blocked behind U6", although CP-22 is verdicted at S23 and U6 is asked at S24.

Both cells now read the opposite, in the same places:

- **A1 §13 U6 row:** "CP-22's **durable accessibility** (not its verdict) and the durable evidence export (S24, PR-13); the closeout written at S23 does not wait on it".
- **A1 §4.1 R11:** "The durable export — not the closeout — stays blocked behind U6 … The case verdict is not gated by U6, and RP-D-15 forbids the post-closeout acts from re-opening it."

The blocked set names two things and only two; the verdict and the closeout appear only in negatives. Counted over the bytes, the two old sentences have **0 occurrences in A1, A3 and A4**; they survive only inside the response's requirement quote and before/after block, and in the untouched v3 baseline. "blocked behind U6" now occurs **once** in A1 — the corrected R11, whose subject is the export.

The corrected rows now agree with the five sites that define the model: CP-22's coverage row (S23, export "cannot be a precondition"), S24's stop rule (refusal costs the export and PR-13, not the verdict), AU-18 (durable accessibility gated on U6, not the case), RP-D-15 (post-closeout acts never block a case) and the U7 row ("no CP row's verdict depends on it").

## Why C-2 is closed

The v3 defect was that AU-16 demanded a registry row for the RV-3 readiness record while only a decision (RP-D-14) and two steps existed. The repair takes the stronger of the two routes offered — it **adds the row**.

- **PR-16** now exists in A3 §6, with all six registry columns: RV-3 readiness review and record, captured before S9b/S15b, frozen before S9b/S15b, executed A at S9b and B at S15b, primary cases CP-15 and CP-16.
- The count is "**sixteen**" and no stale "fifteen procedure rows" claim survives anywhere.
- **AU-16** now names "the RV-3 readiness record (**PR-16**, whose fields and author are RP-D-14)" — an artifact that exists in the same document it cites.
- **A4 §5** now cites §6 (PR-16) and §12 (RP-D-14) rather than a decision alone.

## Why D-3 is closed

The record had to be hashed and in the repository before the ask that quotes it, and no step committed it. Now S9b and S15b "write, hash, commit and push" the record and its index.md entry, and each carries a stop rule: readiness not recorded, wrong candidate, **or the record not in the pushed commit → stop, no ask**. RP-D-14's row and detail, PR-03's precondition, the CP-15/CP-16 evidence cells and the §2.3 tree all name the commit, so no site still lets the R-A or R-B request quote a working-tree hash.

**D-4** to **D-7** are applied: the (pre-step) markers on S3a and S22a; the five missing paths in the evidence tree (startup-readback.md, routing-and-triggers.md, install-negative/, gate-fixtures/, firewall/); the R2-06 pointer, which now names A1's header Status line; and A1 §11's separation of the observer (RV-4, gates CP-15's observed leg) from the closeout reviewer (RV-5, writes CP-22).

## Invariants — unchanged

- **21/21 acceptance statements raw-identical** in A2 and in A4 (13 A + 5 B + 3 X); MUST appears five times across three statements, one of them a MUST NOT, and none is softened; A-13 still open at CP-06.
- **Denominator unchanged:** case_set_sha256 48a28ba1… over 4,934 canonical bytes; result_format_sha256 7f920ec7… over 2,153; 22 ordered IDs.
- **No new authority:** U6 OPEN — not asked; U7 OPEN — not granted; E19 NOT GRANTED; U4 per-turn; U5 five separate asks; E3 still inferred and confirmed in the R-A request; R-A still a separate ask quoting the pushed SHAs.
- **No producer after S23:** parsed 22/22 at or before, 21 strictly before, CP-22 at S23.
- **Non-circularity:** no v4 file contains its own hash or its own 8-character prefix; the index hashes four files and not itself; A4 hashes A1–A3 and points outside for its own.
- **Nothing claimed as run:** every step PLANNED, every case NOT-RUN, all sixteen procedure rows DRAFT/UNFROZEN.

## Files, measured from their bytes

| File | Bytes | LF | SHA-256 |
| --- | --- | --- | --- |
| CONSUMER-STAGE-0-v4.md | 41,024 | 329 | 4de970ee7b4f76055f10cde863a46516483c6ac978de0d54d4b4134ae30d0c26 |
| CONSUMER-RELEASE-PLAN-v4.md | 63,143 | 491 | 2bca5ad19b622d64d61128e4d5be3b9b7650a400dd67e8bda7349caa2552af8d |
| CONSUMER-PLAN-AUDIT-REQUEST-v4.md | 27,963 | 224 | b17bdc2808087c0632b0c1aa00edea8081c938d11fb06a58bfc6f26b46877b34 |
| FINDINGS-RESPONSE-v4.md | 25,282 | 153 | 6ffb954682ebf26c39a418b90165f389e20b335d03ef727f9a333b3334b406c5 |
| V4-INDEX.md | 9,967 | 121 | 8da88652be54057a4668f2381e7c97612e330b2617827ef4167bee6a4bc8f421 |
| ../v3/CONSUMER-REQUIREMENTS-AND-DECISIONS-v3.md (A2, unchanged) | 30,295 | 264 | 9471d18fb80c46e39bb768ddd48455a7778620071805fb673abc83a9a7732439 |
| ../v3/B-03-CLOSURE.md (unchanged) | 9,112 | 79 | 45a4171528461ed1b46c359ad472066edf0b381c156bde0f0c0051aab18da695 |

All five v4 files are UTF-8, no BOM, LF only (0 CR), trailing LF. All ten v1/v2 baselines and all seven v3 files reproduce their recorded hashes; the audited tree was not written to.

## Residual observations — recorded, not conditions

1. **S2 says "this v2 package"** (A3 line 254) — verbatim from v3, historically bounded by the phase table's "(v2 re-audit)". Cosmetic.
2. **E3's exclusion reads "evidence publication"** while A1 §10 allocates the repository's docs/evidence/ records to the content push. Under the reading "export = durable publication" (U6's own definition) the rows agree; worth sharpening when E3 is stated in the R-A request so the owner confirms the allocation with the SHAs. Pre-existing, not created by v4.
3. **S9's durable re-check now precedes S9b's commit and push** (which precede the ask). A content push cannot create a deployment or a Pages build, and S5 already pushes before S9, so the invariant stays measurable and true at S10. No action.

## UNRUN — all of it

Nothing has run. UNRUN: the install and S3a/S4; both builds; both deployments; both observations; both reversals; fresh-agent recovery; the CP-19 key and fixture batch; the firewall scan against real files; the readiness reviews, their two records and PR-16's own capture/freeze; the evidence export and U6; the U7 ask or an alternative disposition; R-EMPTY and the teardown primitive; and all 22 case verdicts at S23. Also UNRUN: **the full AU-01…AU-22 re-audit of the v4 text** — this re-check re-ran seven checks (AU-01, AU-02, AU-03, AU-08, AU-16, AU-18, AU-19) and examined the other fifteen only through a byte diff proving their sections untouched.

## Scope

Plan level only. No code, no pipeline run, no browser, no deployment, no rollback, no provider mutation of any kind (no GET, no HEAD), no case execution, no manual-only invocation, no examiner key, no fixture build. Contextual independence within one harness — not organisational separation; a human reviewer remains the anchor, and the five release decisions are the owner's.

Model: DeepSeek V4 Flash (deepseek-flash @ deepseek-account, DeepSeek Harness); serving model not observable.
