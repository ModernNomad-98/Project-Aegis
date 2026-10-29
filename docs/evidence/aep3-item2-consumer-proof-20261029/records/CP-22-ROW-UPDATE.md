# CP-22 ROW UPDATE — VERDICT **PASS**

**Row:** CP-22, frozen case name `accessible independent closeout`.
**Acceptance sentence (E-03, unchanged):** Reviewer opens/hashes decisive evidence; exactly one final PASS for each required ID. Missing, duplicate or unknown final IDs and evidence-free PASS controls are rejected; retries remain separate history.

## The verdict

**CP-22 = PASS (observed, 2026-10-29T10:21:21-07:00).**

The owner's gate for this cycle: CP-22 is PASS if and only if the independent reviewer ACCEPTS all 22
records and all four rejection controls reject with the required message. The seventh independent review
(round 7) signed **SIGNED** with **22/22 ACCEPT, 0 REJECT**, the four required controls **and** the optional
hash-tamper control rejected (5/5), and a clean baseline exit 0. The gate is **MET**.

| Element of the acceptance sentence | Observation |
| --- | --- |
| "Reviewer opens/hashes decisive evidence" | the reviewer re-measured 261 path+sha256 citations and opened, per row, the decisive file (REVIEW-MATRIX.json `file_opened`); 0 missing, 0 mismatched |
| "exactly one final PASS for each required ID" | 22 unique frozen IDs, one final verdict each, checked by the reviewer's own checker |
| "Missing, duplicate or unknown final IDs ... are rejected" | C-MISSING, C-DUPLICATE, C-UNKNOWN all rejected with the required messages (exit 1) |
| "evidence-free PASS controls are rejected" | C-EVIDENCE-FREE rejected: `CP-11: PASS without hashed evidence` |
| "retries remain separate history" | CP-12, CP-19 and CP-09 carry `supersedes` and `attempt_history`; only the final attempt carries the row verdict |

## What the bundle row says, and why

The CP-22 record inside `RF1-DRAFT-v8.json` types the row **UNRUN** with `gap.next_need` = "the seventh
independent review (round 7) of revision 8". That was the accurate typing *before* the review existed, and
the round-7 reviewer accepted the row on exactly that basis (`claims no CP-22 verdict`). The bundle
bytes are **not** edited to PASS: editing signed bytes would void the signature (R7), and no revision beyond
8 is authorized. This record is the row's update, and the ledger and the U6 export take **PASS** from here,
with the review record as its evidence.

## Derived counts after the update

| Verdict | In revision-8 bytes | After this row update |
| --- | --- | --- |
| PASS | 7 | **8** (CP-04, 08, 10, 12, 13, 14, 16, **22**) |
| FAIL | 3 | 3 (CP-03, CP-09, CP-19) |
| UNRUN | 9 | **8** (CP-01, 02, 11, 15, 17, 18, 20, 21) |
| BLOCKED | 3 | 3 (CP-05, CP-06, CP-07) |
| non-PASS | 15 | **14** |
| open (UNRUN + BLOCKED) | 12 | **11** |

No other row changes. CP-19's rescore as RUN=FAIL (13/14, F2 failing) and CP-09's FAIL standing are already
in the counts and are not affected by this update.

## Evidence for the row

| Item | Path | Bytes | sha256 |
| --- | --- | --- | --- |
| Bundle reviewed | `_A/work-package-3/item2-cp22-final/RF1-DRAFT-v8.json` | 190645 | `9b595c241679f6bbb1da66dcc1a547cf53f0dc1f6ce1ca0b861edfd30d07aeb0` |
| Signature | `_A/work-package-3/item2-cp22-final/mount/REVIEW-OUT/signature-block.txt` | 1538 | `1cb3ad07faefe07265c792bb7ac83e0d8cfa89e7ae387e466e06fcfe9d8c1b42` |
| Matrix (22 rows) | `_A/work-package-3/item2-cp22-final/mount/REVIEW-OUT/REVIEW-MATRIX.json` | 13239 | `80db5c283103c6eef266995d89b764c3597d7986bf2713c8f86ad5879cfc4000` |
| Review narrative | `_A/work-package-3/item2-cp22-final/mount/REVIEW-OUT/REVIEW-ROUND7.md` | 10140 | `d8a5d1eaf3bb936d3216dc5318ffef98d057215880c991aa28e68a434c3379d2` |
| Cycle record | `_A/work-package-3/item2-cp22-final/FINAL-CYCLE-REVIEW.md` | 6921 | `0f14280bc626abb179d9020175577881522aeca8ee1621b1f9e43dcb64ea20eb` |

## Limits of this verdict

- It closes CP-22 only. The 11 remaining open rows stay open; FAIL and PASS rows below it are untouched.
- It does not approve the U6 export; that is the owner's act on the export's own conditions.
- It rests on an agent review, as the owner authorized (CP-22=B: agent review, different vendor), not on a
  human signature.
