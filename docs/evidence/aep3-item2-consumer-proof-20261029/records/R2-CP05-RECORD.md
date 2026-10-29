# R2 — change-control record for the revised CP-05 acceptance text

| field | value |
| --- | --- |
| **Revision ID** | **R2** (freeze-level revision), entry **R2-CP05** |
| Scope | **CP-05 only.** The other 21 acceptance texts, the result format, the roll-up rules and the denominator are untouched. R1 remains the revision for everything except CP-05's acceptance. |
| Supersedes | **R1** for the CP-05 acceptance text only |
| Date | **2026-10-29** (owner decision ~06:20–06:21 PDT; this R2 recorded 06:41–06:44 PDT) |
| Trigger | `TWENTY-TWO-CASE-FREEZE.md` §4 — a rewording of an acceptance after a result exists requires (1) a disclosed new revision, (2) independent review by a non-author, (3) new digests before further execution, (4) retained results for the superseded revision. A CP-05 result existed (UNRUN at `338ba82`). |
| Owner source | `_A/work-package-3/OWNER-DECISION-BATCH-ANSWERS-2026-10-29.md` lines 14–15 — **CP-05 = B** |
| Original text | `cases.json` `.cases[CP-05].acceptance` (R1): `Correct consumer Role B and Stage 0 in the intended repository; no redirect to a sibling app or inherited source authority.` |
| Revised text | `Correct consumer Role B in the intended repository; no redirect to a sibling app or inherited source authority.` |
| Frozen set reference | `case_set_sha256` R1 **48a28ba14e0d589757d6be1269202631ca15fa6631677ca4ed1175ed473c1de9** (unchanged, recomputed); **R2 c39360cf62e79b97301444e8d48385418e9c960f8d941e65fe7be199007ddec8** (new) |
| Reviewer | AEP3-I2 RV-1 / R2 reviewer (this session), independent of the revision author |
| Status | **RECORDED — independent review complete.** `cases.json`, the plan and the freeze prose are **not edited** by this record. |

---

## 1. Authority for the revision

`OWNER-DECISION-BATCH-ANSWERS-2026-10-29.md`, lines 14–15, verbatim:

> **CP-05: B**
> Revised sentence authorized: "fresh-session startup readback on the current consumer repo,
> Stage-0 clause removed." Record the original sentence, the revision, and the rationale (repo
> is no longer Stage-0-shaped) as a dated plan-revision entry; score the row as PASS or UNRUN
> against the revised sentence and label it "revised criterion."

Source class (the file's own line 3): Peter, typed directly in the Project Aegis DSH Web GUI Lead
session, approximately **2026-10-29 06:20–06:21 PDT**. The question it answers is
`OWNER-DECISION-BATCH-2026-10-29.md` lines 70–78 (question CP-05; option B; fail-closed default A).

`PLAN-REVISION-CP05.md` (84d62bc4…, 12,073 B) records this as plan-level revision **R-CP05-1** and
states in its §5 that it is **not** the R2 the freeze requires. This record is that R2.

---

## 2. The exact diff

### 2.1 Frozen acceptance text (what `case_set_sha256` hashes)

| | Text | SHA-256 |
| --- | --- | --- |
| **R1** | `Correct consumer Role B and Stage 0 in the intended repository; no redirect to a sibling app or inherited source authority.` | **66d245e70e9b5c5ac9342b40a595d0ce5af53a8e93dbc6434ab89069aa159d8b** |
| **R2** | `Correct consumer Role B in the intended repository; no redirect to a sibling app or inherited source authority.` | **6a96e07ce7b44d7d7441d6729326c2ec92279d940708f897538cea4d07291232** |

**Diff: delete " and Stage 0"; nothing else changes** — not the actor, not "in the intended
repository", not the sibling-app clause, not the inherited-authority clause, not the punctuation.

### 2.2 Plan row sentence (what the row is scored against)

| | Text | SHA-256 |
| --- | --- | --- |
| **R1** (plan line 299) | `A new session given only the repository location and a resume request reports consumer Role B and Stage 0, with no sibling-app redirect and no inherited source authority` | **a6671a14c58556f7e67aec079a5b59140cacf14936d052b76b373a6f5296ea53** |
| **R2** | `On the current consumer repository, a new session given only the repository location and a resume request reports consumer Role B, with no sibling-app redirect and no inherited source authority.` | **5b77a1affca1618f17e25f0b73db9b3314ef9197059a26b9760f0acfe85bf2cb** |

**Diff:** delete "and Stage 0"; add the owner's locality qualifier "On the current consumer
repository," at the head. Every other clause is R1's wording, unchanged.

### 2.3 Why the revision has to touch the frozen text, not only the plan row

`case_set_sha256` hashes `.cases`, whose `acceptance` field carries the freeze's **O-2** wording
("Correct consumer Role B and Stage 0 in the intended repository; …"), not the plan row's **O-1**
wording. `PLAN-REVISION-CP05.md` §2.2 derives only O-1′ and calls the plan row "the operative one".
That is right for scoring the row, but it is incomplete for change control: an R2 that hashed only
O-1′ would leave the text the frozen digest actually covers unrevised. **R2 therefore records both
forms** — O-2′ (frozen acceptance, one deletion) and O-1′ (row sentence, deletion + locality
qualifier) — and computes the new case-set digest over O-2′. This completes the revision; it does
not contradict it. Both forms carry the same decisive change and the same remaining clauses.

The divergence is not special to CP-05: measured against the plan's rows, **all 22** frozen acceptance texts
differ from the plan cells (they are condensed paraphrases, not verbatim copies, despite the freeze's §2
sentence). CP-05 is simply the case whose text is being revised — and an R2 that touched only the plan row
would have revised a sentence the digest does not cover.

---

## 3. Minimum edit, and what "not a broadening" means here

| Clause | R1 (row form) | R2 | Change |
| --- | --- | --- | --- |
| Locality | "given only the repository location and a resume request" | "**On the current consumer repository,** a new session given only the repository location and a resume request" | qualifier added, from the owner's own "on the current consumer repo" |
| Role | "reports consumer Role B" | "reports consumer Role B" | unchanged |
| Stage | "Role B **and Stage 0**" | "Role B" | **removed — the authorised change** |
| Redirect | "with no sibling-app redirect" | "with no sibling-app redirect" | unchanged |
| Authority | "and no inherited source authority" | "and no inherited source authority" | unchanged |

The qualifier adds **no observation**: it names where the readback is taken and is satisfied by the
same session on the same repository. It does not widen the target set (it says *the* current consumer
repository, not "any repository"), does not change the actor, the prompt rule, the disqualifiers in
plan line 258, the producer (S4a), the evidence standard, the case ID or the denominator.

The revision is therefore a **minimum edit implementing exactly the authorised change**, not a
broadening of scope or permission. It *is* a deliberate relaxation of one required observation —
removing a clause a repository can no longer satisfy — and that relaxation is precisely what the owner
authorised. Say it plainly rather than pretending the criterion is unchanged.

---

## 4. New digests

Canonicalization is the freeze's own: for text, SHA-256 over the UTF-8 bytes of the exact sentence
with no trailing newline; for the case set, SHA-256 over
`json.dumps(.cases, sort_keys=True, separators=(',',':'), ensure_ascii=False).encode('utf-8')`, array
order preserved. Reproduce with `evidence/r2_digests.py` (output: `evidence/R2-DIGESTS.json`).

| Digest | Value | What it covers |
| --- | --- | --- |
| `cp05_acceptance_sha256_R1` | `66d245e70e9b5c5ac9342b40a595d0ce5af53a8e93dbc6434ab89069aa159d8b` | frozen acceptance, R1 |
| `cp05_acceptance_sha256_R2` | `6a96e07ce7b44d7d7441d6729326c2ec92279d940708f897538cea4d07291232` | **revised criterion text** |
| `cp05_row_sentence_sha256_R1` | `a6671a14c58556f7e67aec079a5b59140cacf14936d052b76b373a6f5296ea53` | plan row sentence, R1 |
| `cp05_row_sentence_sha256_R2` | `5b77a1affca1618f17e25f0b73db9b3314ef9197059a26b9760f0acfe85bf2cb` | revised row sentence |
| `case_set_sha256_R1` | `48a28ba14e0d589757d6be1269202631ca15fa6631677ca4ed1175ed473c1de9` | **case-set reference** (recomputed; matches the freeze) |
| `case_set_sha256_R2` | `c39360cf62e79b97301444e8d48385418e9c960f8d941e65fe7be199007ddec8` | **new case-set digest**: `.cases` with only CP-05's `acceptance` replaced by R2 text |
| `owner_authorization_sha256` | `f848672ab03ca62b75fc67fc833f3047af754db2a1fd6f600918c0c62ebb31e0` | lines 14–15 of the answers record, newline-joined |
| `r2_binding_sha256` | `4c93aea9899de5bd6155d917762309f8f604087ed7a482c1c471596a362e42a0` | canonical JSON binding the revision id, both case-set digests, both text pairs and the owner-authorization hash |

`case_set_sha256_R2` is a **derived** identity, not a digest of any file on disk: `cases.json` is
unchanged (9,442 B, SHA-256 `5908f1e2b5519bb14984a074bcb9b6d11ecc84926b19a8b8a8871c853855bdce`,
still carrying the R1 text). A reviewer reproduces the R2 digest by applying the single substitution
documented in §2.1; no edit is required, and none was made.

**Pre-execution requirement.** Freeze §4(3) says the new digests are recorded **before** any further
execution. From this record forward, every CP-05 execution or roll-up must quote `c39360cf62e79b97301444e8d48385418e9c960f8d941e65fe7be199007ddec8`.
See R2-1 for the sequencing deviation already incurred.

---

## 5. Independent review statement

I am the RV-1 / R2 reviewer for this leg. I did not write `PLAN-REVISION-CP05.md`,
`CP-05-ROW-UPDATE.md`, the currency addendum, the CP-02 package, or either CP-05 observation; I ran no
session for CP-05; I made no provider call and no consumer write.

**What I checked, and what I found:**

1. **Original text — verified at three places.** `CONSUMER-RELEASE-PLAN-v4.md` line 299 (2bca5ad1…)
   reads exactly as quoted; `TWENTY-TWO-CASE-FREEZE.md` line 62 (85c773fb…) reads "Correct consumer
   Role B and Stage 0 in the intended repository; no redirect to a sibling app or inherited source
   authority."; `cases.json` `.acceptance` is byte-equal to the freeze line. **Confirmed.**
2. **Owner authorisation — verified verbatim and dated.** Lines 14–15 read as quoted; the file's own
   source-class line dates the answer to ~06:20–06:21 PDT 2026-10-29; the question record's option B
   matches the authorised revision. The answers file is a live append-only capture, and lines 14–15
   sit inside the first 4,843 bytes, whose digest still equals the `f5bdd0f5…` captured by the
   revision turn — so the operative words have not moved since 06:24. **Confirmed.**
3. **Diff — verified clause by clause.** One deletion and one qualifier in the row form; one deletion
   in the frozen form. No other clause, actor, target or standard changes. **Minimum edit, not a
   scope broadening** (§3). **Confirmed.**
4. **Observation at `338ba82` — verified in the retained transcript.** It reports Role B ("this is
   your product repository, not the Aegis source library… The Aegis skills here are copied tools"),
   proposes no sibling app, claims no source authority, writes nothing, and never reports Stage 0.
   Under R1 that is UNRUN; under R2 the four remaining clauses are all observed. **Confirmed.**
5. **Observation at `3998af1` — verified in the currency transcript.** A genuinely new `claude -p`
   session (74-byte prompt, fresh clone, new process) reports Role B, absence of the source-library
   landmarks, no sibling redirect, no inherited authority, no writes; it refuses to guess live
   provider state. **Confirmed**, and it is the re-run the owner's option contemplated.
6. **Labelling.** The row is marked "**PASS — revised criterion**" and carries L2 ("must not be counted
   against `case_set_sha256 48a28ba1…` until that step is recorded"). **Confirmed.**
7. **Identity of the evidence.** The readback record (7,998 B / `9270fdb4…`), the session stream
   (94,306 B / `db26f39b…`), the ordered reads (4,046 B / `5c50d621…`), the prompt (74 B /
   `3896883c…`) and the currency transcript (2,966 B / 2,961 chars / `802ea101…`) all recompute
   exactly. **Confirmed.** (The addendum's "2,959 chars" bullet is two characters off; its own
   Artifacts bullet and the bytes are right.)

**Two findings that change what the closeout should do:**

- **F1 — the revision package revised only the plan-row form.** R2 supplies the frozen-form edit and
  the case-set digest over it (§2.3). Without this, the digest would have covered the wrong text.
- **F2 — sequencing.** The `3998af1` re-run was executed at ~06:29 PDT, before this R2 existed
  (06:41+). Freeze §4(3) asks for digests before further execution. The observation itself is
  read-only, reproducible and admissible; the deviation is recorded, and from here on the rule binds.

**Reviewer verdict:** the revision is **authorised, minimum, correctly dated and correctly labelled**;
the R2 record is **complete** (revision id, both text forms with hashes, owner source, reviewer
statement, new digests over the revised text and the case-set reference). **Accepted for CP-05 only.**

---

## 6. Labelling and counting rules (exact strings for the ledger / STATUS)

- Row label: **`PASS — revised criterion`**.
- Roll-up string: **`CP-05 PASS (revised criterion; R2-CP05; case_set_sha256_R2 c39360cf62e79b97301444e8d48385418e9c960f8d941e65fe7be199007ddec8; R1 48a28ba14e0d589757d6be1269202631ca15fa6631677ca4ed1175ed473c1de9 retained as history)`**.
- **Never** count the CP-05 PASS against `case_set_sha256_R1 48a28ba14e0d589757d6be1269202631ca15fa6631677ca4ed1175ed473c1de9`. A matrix that
  quotes R1 while counting CP-05 as PASS overstates what the frozen set measured.
- **The R1 result is retained, not relabelled.** `cp05-startup-readback.md` line 12 records
  **UNRUN** under R1 and stays that way; the PASS is an R2-era result over the same observation plus
  the `3998af1` re-run.
- The R2 digest is quoted **together with** the R1 digest wherever a total includes CP-05, so a reader
  can see which text produced which verdict.

---

## 7. What R2 does not do

- It does not edit `cases.json`, the plan, the freeze prose, the ledger or the closeout.
- It does not change any case other than CP-05, and does not change the denominator (22) or the
  NOT-APPLICABLE rule (0).
- It does not re-run CP-05, start a session, dispatch, deploy or publish.
- It does not take the owner's remaining decisions (U6 publication, CP-06 questions, browser rows).
- It does not decide whether the plan file or `cases.json` should eventually be edited to carry the
  revised text; that is an owner/Lead choice, and the R2 digest is designed to work without it.

---

## 8. Residuals

| # | Residual | Disposition |
| --- | --- | --- |
| **R2-1** | **Sequencing:** the `3998af1` re-run preceded this R2. Freeze §4(3) was not satisfied for that run | Recorded; the observation is read-only and admissible. The rule binds all future CP-05 execution |
| **R2-2** | **Evidence location:** the plan's CP-05 artifact (`docs/evidence/closeout/startup-readback.md`) does not exist in the consumer repository; the observation lives in the planning workspace (row update L3) | Carried; one content commit would close it if the closeout requires the artifact in-repo |
| **R2-3** | **Currency:** both observations are on install branches (`aep3-i2/startup-readback` `338ba82`, `aep3-i2/next-action-record` `3998af1`), **never on `main`**, which carries no install | Disclosed in the row (L1) and the addendum. The revised sentence says "the current consumer repository", so this is within its terms, but a reader must not read it as a `main` readback |
| **R2-4** | **One session, one model, one run per observation** (`claude-sonnet-5-5`); not a human session | Disclosed (L6) and unchanged by R2 |
| **R2-5** | **Two renderings exist** — the operative O-1′ in `PLAN-REVISION-CP05.md` §2.2 / `CP-05-ROW-UPDATE.md` §1 (identical), and a summary-table paraphrase in the row update that puts the locality qualifier at the end | The paraphrase is non-operative and semantically identical; the R2 text in §2.2 governs. A future edit should align the summary cell |
| **R2-6** | **Freeze §2's provenance claim is inaccurate for all 22 texts**, CP-05 included: the frozen field is a condensation, not a verbatim copy of the plan's observation cell | R2 works from the frozen field the digest actually hashes, so the revision is unaffected. The freeze's §2 sentence should be corrected once by the owner/Lead |

Model: DeepSeek V4 Flash (deepseek-flash @ deepseek-account, DeepSeek Harness); serving model not observable.
