# CP-22 FINAL CYCLE — REVIEW RECORD AND VERDICT

**Cycle:** AEP3-I2 CP-22 final cycle, opened 2026-10-29T10:05:42-07:00 under the owner decision of
2026-10-29 10:05-10:07 PDT (one reviewer cycle, hard 60-minute box, PASS or FAIL at the box).
**Producer:** AEP3-I2 CP-22 FINAL-CYCLE (DeepSeek Harness, model deepseek-flash), one session.

## Verdict

**CP-22 = PASS.** The seventh independent review signed **SIGNED** with **22 of 22 records ACCEPTED**,
**0 REJECTED**, the four required rejection controls **and** the optional hash-tamper control all rejected
(5/5), and a **clean baseline exit 0**. Under decision CP-22=B that is the gate: **MET**.

| Field | Value |
| --- | --- |
| Bundle reviewed | RF1-DRAFT-v8.json, revision 8, 190645 bytes, sha256 `9b595c241679f6bbb1da66dcc1a547cf53f0dc1f6ce1ca0b861edfd30d07aeb0` |
| Records | 22; ACCEPT 22, REJECT 0 |
| Controls | C-MISSING, C-DUPLICATE, C-UNKNOWN, C-EVIDENCE-FREE rejected; C-HASH-TAMPER rejected |
| Clean baseline | exit 0, admissible, 7 disclosed warnings (reviewer null on the 7 PASS rows) |
| Case set (T1) | `48a28ba14e0d589757d6be1269202631ca15fa6631677ca4ed1175ed473c1de9`, 22 IDs, matches |
| Evidence re-measurement (T2) | 261 citations by the reviewer's sweep, 0 missing, 0 mismatched |
| Clocks (T5) | accepted as documented deviation |
| Reviewer | fresh Claude Agent SDK session `9bcd0382-3738-4ff4-b28e-269a7221b8dd`, Anthropic claude-opus-5-5, one session, no resume/fork |
| Signed at | 2026-10-29T10:17:46-07:00 (2026-10-29T17:17:47Z) |
| Verdict recorded | 2026-10-29T10:21:21-07:00 — 15 min 39 s after the box opened, inside 60 minutes |

## What was reviewed

Revision 7 was rejected by round 6 on exactly two text defects: one CP-09 sentence that said the scanned
clone's checkout moved between attempts, and CP-22's stale self-reference to revision 6 / round 5.
Revision 8 fixes those two and changes nothing else. The owner's 10:05 corrections (CP-19 rescored
RUN=FAIL at 13/14 with F2 failing; CP-09 FAIL stands) are carried as a bundle-level `owner_decisions` block,
because both touch records round 6 accepted and the instruction was to keep those 20 records byte-identical.

| Claim | How it was checked | Result |
| --- | --- | --- |
| Only CP-09 and CP-22 changed | canonical per-record sha256 plus serialised-text comparison, revision 7 vs 8 | 20 of 22 byte-identical; CP-09 and CP-22 changed; 0 other record leaves |
| No verdict changed | counts recomputed from the 22 records | 7 PASS / 3 FAIL / 9 UNRUN / 3 BLOCKED before and after; 15 non-PASS, 12 open |
| CP-09's replacement sentence is supported | producer re-read the three sources; the reviewer re-opened them independently | attempt 1 read `rb-prereq-work/consumer` (CP-CLOSEOUT-RECORD.md:14, CP19-FIX-RECORD.md:7); the scanned clone was a fresh post-merge clone at 4f31293 (MERGED-MAIN-MATRIX.md:22-23); 390363f is 4f31293's first parent |
| CP-22 now describes revision 8 / round 7 | reviewer re-read setup, observed_outcome, gap, prep_review | accepted; the row claims no CP-22 verdict |
| The bundle did not change during review | hash re-measured before and after the session | `9b595c241679f6bbb1da66dcc1a547cf53f0dc1f6ce1ca0b861edfd30d07aeb0` at build, at signing, and after |

## The reviewer's decisions

**T4 — 22 ACCEPT, 0 REJECT.** The seven PASS rows were opened and their observations found; the three FAIL
rows (CP-03, CP-09, CP-19) are supported by their evidence and name the failed clause; the twelve open rows
are accurately typed and none types an executed failure as unrun. No row was converted to PASS on prose.

**T5 — clocks accepted as documented deviation.** started_at/ended_at are null on 21 records; every null
record carries a time_basis citing a source the reviewer opened; no verdict depends on the record clocks.

**T6 — CP-22 = PASS.** The signature states it does not approve an export and that the 12 open rows stay open.

## Producer defects the reviewer found, non-blocking

These did not meet the pre-committed rejection criteria and did not change any row decision. They are
recorded because they are true, and none was fixed after the signature: editing the signed bytes would void
the signature (R7), and no revision beyond 8 is authorized.

1. **Brief defect (producer).** Section 7 of the brief still said the signature block belongs "inside
   REVIEW-ROUND6.md" — a leftover from the round-6 brief. The reviewer treated it as a typo and wrote
   REVIEW-ROUND7.md. Recorded as such; it affected no decision.
2. **Stale bundle-level prose.** `schema.deviations_disclosed` still says the round-6 review supplies the
   reviewer. It is bundle metadata, not a record, and revision 8 left it unchanged.
3. **CP-09 record-level correction ledger** (`correction.fields_with_revision`) was not extended to revision 8; the
   revision-8 change is recorded in the bundle-level `corrections` array instead. Incomplete ledger, no
   run misstated.
4. **CP-22 attributes.** The row's actor, run_id and time_basis are the closeout session's while its tally is
   the revision-8 prep's; the row is unexecuted, so no run is falsely attributed.
5. **CP19C scoring.json** carries `cp19_verdict: UNRUN` internally; the owner's rescore supersedes it and the
   record follows the rescore.

## What this verdict does and does not do

- It makes CP-22 **PASS** on the owner's gate for the final cycle. It does not close CP-01, CP-02, CP-05,
  CP-06, CP-07, CP-11, CP-15, CP-17, CP-18, CP-20 or CP-21, and it does not change CP-03, CP-09 or CP-19
  (FAIL), nor CP-04/08/10/12/13/14/16 (PASS). The 12 open rows stay open.
- It does not approve the U6 export. That is the owner's act, and the export proceeds on its own conditions.
- CP-09 remains FAIL and CP-19 remains FAIL (owner rescore). Neither is re-typed by this cycle.
- No extra revision was built: revision 8 is the only revision of this cycle.

## Time box

| Mark | Time (PDT) |
| --- | --- |
| Box opened | 2026-10-29T10:05:42-07:00 |
| Revision 8 built | 2026-10-29T10:08:18-07:00 |
| Review root packed | 2026-10-29T10:12:41-07:00 |
| Reviewer launched (launch 2 of record) | 2026-10-29T10:12:49-07:00 |
| Reviewer signed | 2026-10-29T10:17:46-07:00 |
| Verdict recorded | 2026-10-29T10:21:21-07:00 |
| Hard box | 2026-10-29T11:05:42-07:00 (60 minutes) |
| Elapsed at verdict | **15 min 39 s** |

One aborted launch preceded the reviewer of record: launch 1 ran from about 10:10:30 and was terminated at
about 10:12:00, after T1, because the mounted brief still carried a stale section-8 signature block naming
round 6 and revision 7 and the owner-decision file had a stale name. Its stream and partial outputs are
preserved under `session/aborted-launch-round7/`; it produced no adjudication and signed nothing.
Launch 2 used the corrected root. This is disclosed rather than hidden because an aborted launch that read a
defective brief is part of the cycle's history.
