OWNER DECISION BATCH — 9 open items, one comment

Read one block at a time; answer once. IDs match the STATUS gate list. No new work starts from this comment; fail-closed defaults are already in force and remain until you answer.

---

ID: I5
QUESTION: For the 78-file consumer-readiness evidence export, which publication treatment do you choose for the 148 lines that contain the Windows short-name alias (the relayed reply 6486405242 already authorized removing the local username line but did not cover this second identifier), and who is the separate reviewer?
OPTIONS:
- A — Option 2 (extend the authorized redaction): publish a derivative with the 148 alias lines masked/removed, README states the derivative and why, Apache-2.0 attribution kept, path `docs/evidence/consumer-readiness/exports/item5-20261028/`, reviewer named by you.
- B — Option 1 (publish literally as authorized): same path, alias lines left intact, README states the artifact contains a local Windows account alias.
- C — Hold: no publication; I5 closes as not-published and the export stays workspace-local.
FAIL-CLOSED DEFAULT: C (hold). If you never answer, nothing is published; the export remains workspace-local and I5 never closes.
YOUR RECOMMENDATION: A — data-minimization and your earlier relay already accepted a redacted version without the local username line; only you can widen that redaction scope and name the reviewer. Evidence: `_A/work-package-3/item5-publication/PUBLICATION-RECORD.md` (12,372 B), REDACTION-DIFF, FILE-LIST; relayed reply 6486405242 in #910.
BLOCKS: AEP3-I5 publication and U6 export (U6 is pre-granted only after all non-browser CP rows are RUN and the Item 2 closeout is written); the named reviewer is required before any commit.

---

ID: APR-156
QUESTION: Grant the exact-scope gate-guard exception for AEP#3 Item 8? The exact ask text follows inline (no file link).

> # OWNER ASK — AEP#3 Item 8 exact-scope gate-guard exception
>
> **One-line answer requested.**
>
> ## Exact file
> `.github/workflows/validate-skills.yml` (protected by gate-guard via the `^\.github/workflows/` pattern).
>
> ## Exact one-line predicate change (line 95, PR "Compute changed paths" step)
> From:
> ```sh
> if grep -Eq '^tools/' "$RUNNER_TEMP/aegis-changed-paths"; then
> ```
> To:
> ```sh
> if grep -Eq '^(tools/|docs/instrumentation/workflow-outcomes-v1\.schema\.json$)' "$RUNNER_TEMP/aegis-changed-paths"; then
> ```
>
> ## Effect
> A PR that changes only `docs/instrumentation/workflow-outcomes-v1.schema.json` selects the existing Linux and Windows tool-test jobs (and the usage contract suite already wired there), matching the existing `tools/` trigger; all other routing predicates and the push-event behavior are unchanged (push sets tools=true unconditionally at line 86-89 and is untouched). Bounded routing fixture matrix will cover exact schema path, ordinary tools path, mixed change, unrelated docs, similar-but-different filename, and push behavior; the invalid-schema control must fail the suite and restored bytes must pass.
>
> ## Grant requested (new, exact-scope only)
> AEGIS-APR-156: a gate-guard exception for exactly one file `.github/workflows/validate-skills.yml`, for exactly the one-line predicate change above, bound to the exact schema path and the candidate head; **no general waiver**, no change to CODEOWNERS/branch protection/required checks, and the standard fresh-merger + APR receipt path still applies. This is a protected-workflow merge decision for the owner, not a settings change.
>
> ## Why it is needed
> APR-140 is scripts-only; APR-151/APR-153 were consumed by APR-155 at #951. Without a new grant, Item 8 delivery is blocked (fail-closed hold), while all other AEP#3 items can proceed.
>
> ## Answer format
> "APR-156: YES" or "APR-156: NO" (or a different scope you specify). Source class: owner instruction in the DSH Web GUI session; recorded with timestamp and wording.

OPTIONS: A — "APR-156: YES" as written; B — "APR-156: NO" (Item 8 closes as not-authorized); C — narrower/different scope you specify in one line.
FAIL-CLOSED DEFAULT: B (no grant). If you never answer, Item 8 stays HOLD, no workflow change is made or pushed.
YOUR RECOMMENDATION: A — it is one line in one file, exact-scope, fixture-covered, and leaves push behavior/required checks untouched; the alternative is Item 8 never closing. Evidence: `_A/work-package-3/ITEM8-OWNER-ASK.md` (1,988 B / sha256 5c9a5e1e… ask recorded verbatim above); APR-140/151/153/155 history in `docs/approvals/APPROVAL_REGISTER.md`.
BLOCKS: AEP3-I8 only; nothing else in AEP#3 depends on it.

---

ID: CP-02
QUESTION: Which record is the authoritative **E3 allocation**, so the effect-to-grant reconciliation can be scored against one source?
OPTIONS:
- A — E3 = plan A1 §12 as written (the accepted plan is canonical).
- B — E3 = the consumer-record description (consumer documents are canonical).
- C — You restate E3 in one line and that line becomes authoritative.
FAIL-CLOSED DEFAULT: no E3 allocation confirmed -> CP-02 stays UNRUN.
YOUR RECOMMENDATION: A — the plan is the document you accepted; the consumer records are downstream copies. Evidence: `_A/work-package-3/item2-cp-ledger/CP-LEDGER.md` line 59 (CP-02 row: target/URL/exposure observed; frozen row requires every planned effect reconciled to a grant or marked NOT GRANTED/INFERRED; no independent reconciliation exists yet).
BLOCKS: CP-02 and the AEP3-I2 acceptance closeout (D121) that carries it.

---

ID: CP-05
QUESTION: U8 is recorded (YES-with-conditions) and the vendoring/startup-readback was already re-run — the remaining blocker is only the plan sentence: accept CP-05 as a plan defect, or authorize a revised sentence?
OPTIONS:
- A — Accept as plan defect: CP-05 recorded as UNRUN-permanently with a plan-defect note (no plan edit; the row cannot pass by construction).
- B — Authorize revised CP-05 sentence: "fresh-session startup readback on the current consumer repo, Stage-0 clause removed"; re-run then scores PASS/UNRUN (ETA 20-30 min).
- C — Drop CP-05 from the acceptance claim with a written rationale.
FAIL-CLOSED DEFAULT: A (row stays UNRUN; no plan edit).
YOUR RECOMMENDATION: B — the meaningful startup behavior was already observed (a genuinely new session reported Role B correctly, no inherited source authority, no sibling redirect); only the Stage-0 clause is unsatisfiable because the repo is no longer Stage-0-shaped. Evidence: `_A/work-package-3/item2-cp-replication/CP-REPLICATION-RECORD.md` and `evidence/cp05-startup-readback.md`; U8 record `_A/work-package-3/OWNER-DECISION-RA-A13-U8-2026-10-28.md`.
BLOCKS: CP-05 and the AEP3-I2 closeout; U6 pre-grant conditions include all non-browser CP rows RUN.

---

ID: CP-06
QUESTION: A-13 is already recorded (three-seed spec), so only the **four Stage 2 owner outcomes** remain — do you answer them now, or point me to a record to transcribe?
OPTIONS:
- A — You answer the four Stage 2 owner outcomes now (one line each).
- B — You point to an existing record containing them and authorize transcription; I then score CP-06 against it.
- C — Defer CP-06 (stays BLOCKED).
FAIL-CLOSED DEFAULT: C (BLOCKED).
YOUR RECOMMENDATION: B if such a record exists; otherwise A — CP-06 requires the four real outcomes in required order, and no such answers exist in the workspace (the plan says they are answered by you, not derived by agents). Evidence: `_A/work-package-3/item2-cp-ledger/CP-LEDGER.md` line 63 and `REMAINING-ROWS.md` (CP-06 needs A-13 ratified — now recorded — plus the four Stage 2 owner outcomes).
BLOCKS: CP-06 and the AEP3-I2 closeout.

---

ID: CP-12
QUESTION: The directory-symlink finding is real (main accepts `site -> site.real`); a reviewed bounded guard exists on consumer branch `aep3-i2/cp12-guard` @ `8ac4f73` (independent review PASS, `59223fed…`). Should it be merged to the consumer repo main?
OPTIONS:
- A — Authorize a content commit of the guard to consumer main + a merged-main S0-S3 re-run (ETA 20-30 min); CP-12 can then PASS.
- B — Keep the guard on its branch only; CP-12 stays UNRUN.
- C — Reject the guard and record the finding as accepted risk.
FAIL-CLOSED DEFAULT: B (branch only; CP-12 UNRUN).
YOUR RECOMMENDATION: A — the finding is reproduced (S3 accepted on main), the guard is one-file +20 lines with unchanged allowlist/manifest/build job, and one build-only dispatch already passed; consumer-main merges are owner-only per SDP-1 item 6. Evidence: `_A/work-package-3/item2-cp12-guard/CP12-RECORD.md` (`511da819…`), `GATE-DIFF.md` (`fecd9e99…`), review `item2-cp12-review/CP12-REVIEW.md`.
BLOCKS: CP-12 and CP-12.6/.7 sub-cases; does not block other rows.

---

ID: CP-19
QUESTION: The corrected CP-19 batch is 13/14 PASS; the one failure (F2 late-revocation) resolves the impossible chronology instead of reporting `authority_state=unresolved`. Keep that requirement, or pre-register an R2 revision accepting a resolved chronology?
OPTIONS:
- A — Keep the unresolved requirement: CP-19 stays UNRUN; F2 recorded as a genuine negative-case finding (consumer gap remains open).
- B — Pre-register R2 revision: accept a resolved chronology for late-revocation; re-score (14/14) -> CP-19 PASS.
- C — Drop CP-19 from the acceptance claim with a written rationale.
FAIL-CLOSED DEFAULT: A (UNRUN; the fixture semantics are frozen without your revision).
YOUR RECOMMENDATION: A — resolving an impossible chronology silently is exactly the authority-state gap CP-19 exists to catch; B would turn a known gap into a pass. Evidence: `_A/work-package-3/item2-cp19-fix/CP19-FIX-RECORD.md`, `evidence/CP-19-ROW.md`, `SCORING.md` (13 PASS / 1 FAIL, F2).
BLOCKS: CP-19 and the AEP3-I2 closeout.

---

ID: CP-22
QUESTION: The 22 RF-1 records are prepared (7 PASS / 12 UNRUN / 3 BLOCKED) but CP-22 needs an independent non-implementing reviewer and the four rejection controls run. Who reviews?
OPTIONS:
- A — You name a human reviewer (person) not in the build chain.
- B — You designate a fresh independent agent session (recorded as agent review, not human) named by you.
- C — Leave CP-22 UNRUN.
FAIL-CLOSED DEFAULT: C (UNRUN).
YOUR RECOMMENDATION: B — fastest route that preserves independence as a documented agent review; the brief and controls are ready. Evidence: `_A/work-package-3/item2-cp22-prep/REVIEWER-BRIEF.md` (`152dd909…`), `RF1-DRAFT.json` (`042396d5…`), `CP22-RECORDS.md` (`62fb7e0d…`). Note: U6 gates only the S24 export, not CP-22.
BLOCKS: CP-22 and the AEP3-I2 closeout.

---

ID: browser rows
QUESTION: CP-11, CP-15, CP-17 and CP-20 have visible/browser halves that cannot run without a browser session. Do you supply one, or do those halves close as UNRUN?
OPTIONS:
- A — You supply a browser session (or run the visible checks yourself and return results); ETA 30-60 min.
- B — Accept the visible halves as UNRUN permanently and record that in the closeout.
- C — Supply screenshots/video instead of a live session (partial evidence; not a pass).
FAIL-CLOSED DEFAULT: B (UNRUN; already the recorded state).
YOUR RECOMMENDATION: B for closure — everything that can be observed without a browser is already PASS/UNRUN honestly; a browser session is the only way to convert these, but it is not required for the non-browser closeout. Evidence: `_A/work-package-3/item2-cp-ledger/BROWSER-PLAN.md`, CP-CLOSEOUT-RECORD).
BLOCKS: only the browser halves of those four rows; the AEP3-I2 closeout can state them UNRUN.

---

END OF BATCH. One answer is enough; anything left unanswered keeps its fail-closed default. Nothing above authorizes a deployment, settings change, publication or merge by itself.
