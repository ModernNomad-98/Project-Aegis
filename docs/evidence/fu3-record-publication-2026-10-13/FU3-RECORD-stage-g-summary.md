# BER-G3 FU-3 RECORD LANE — STAGE G MERGE RECORD

**Item:** "FU-3 reconciliation record lane Stage G merge" — the merge of the three append-only governance records stating that the historical provider-usage reconciliation was **attempted and NOT completed**, so headroom against the BER-DEC-008 lifetime maxima is **UNVERIFIABLE — not zero and not positive** — and the standing zero-residual posture is unchanged.
**Agent:** `fu3-record-merger-g` — a different agent from every Stage A, B, C, D, E and F holder of this lane. **No subagents were used.**
**Writes made by this pass:** (1) the merge itself, (2) the MERGE RECEIPT comment **6149285129** on pull request #764, and (3) this record. A private clone (`_resume-2026-10-09/_fu3rec-g-merger-clone-g`) and a private scratch directory (`_resume-2026-10-09/fu3rec-g-merger-scratch`) were created outside the repository. The repository's working tree, the pull request **body** and every other lane artefact were **read, never written**; `clone-pq1`, `clone-pq2`, the legacy root and every `wt-*` worktree were neither written nor fetched.
**PR:** **#764** — now **closed and merged**; one commit, three changed files, 54 insertions, 1 deletion.
**Head merged (head-bound):** `c7350242ad0b4728d44871bc24a18d85a1bd7fdc` — tree `fc8cc35c96efbf3a2b6e15e8271d66984213ff74`, single parent `ba522f133d05624c2130f15eb8ef3b6329b0f37a`.
**Merge commit:** `05e93f499c827c4749b12cef09d2bbb7989121c4` — parents `ac731607124f1f849257f8db260f41451c533da7` + `c7350242ad0b4728d44871bc24a18d85a1bd7fdc`, tree `1a0dd7a5c7ff96ebddc364a2275cba93b9fe774a`, committer date **2026-10-13T15:36:39Z**; `main` now reads `05e93f49…`.
**Bound-field digest of record (recorded, never filled into the body):** **`482ee760bc99ca36`** — full `482ee760bc99ca36de51313d1ff2cf39051bf15f6a4852556b7de86936426e86`.
**Verdict:** **MERGED** — on the exact 40-character head above, with the digest above, after every merge gate in §4 was either met or recorded with its exact disposition. **The pull request body was not edited by this stage — not one byte.**

**Reading aid (the owner's permanent reporting rule — every label and id carries a one-line plain-English description).**

| Label / id | What it is, in plain English |
| --- | --- |
| **FU-3** | Follow-up item 3 of the BER-G3 reconciliation accounting: recover the historical provider usage and state the remaining allowance. |
| **BER-G3** | The third owner-approved gate of the BER measurement package — the remaining-allowance gate; "BER" is the Behavioral Eval Runner this project is building. |
| **BER-DEC-008** | The backlog decision entry that sets the lifetime maxima (attempts, metadata requests, tokens, dollars) the reconciliation would have measured against. |
| **register** | `docs/approvals/APPROVAL_REGISTER.md` — the append-only owner approval register recording who was allowed to do what. |
| **backlog** | `docs/roadmaps/behavioral-eval-runner-backlog.md` — the BER decision register; its **section 13** is the append-only governance log. |
| **open-decisions** | `docs/roadmaps/aegis-open-decisions-2026-09-23.md` — the open-question tracker whose WP-2B-3 posture row carries the standing "assume zero residual allowance" instruction. |
| **AEGIS-APR-136** | The register entry this change appends: one numbered lifecycle record that grants nothing. |
| **DCO** | Developer Certificate of Origin — the per-commit `Signed-off-by:` trailer continuous integration checks. |
| **`gate_pattern` / `gate-guard`** | The protected-path regular expression inside the CI workflow, and the continuous-integration check that fails when a pull request changes one of those paths. |
| **Codex / AEGIS-APR-050** | The automated reviewer GitHub runs on pull requests, and the standing owner grant that makes merges wait for its review **or** a recorded "Codex unavailable". |
| **MG1–MG5** | The five merge-entry gates: green checks at the exact head; a posted final review naming that head; the Codex review or its confirmed unavailability for that head; the merger's own authority; the outside-contribution security question. |
| **MG3** | The gate this record spends the most words on: a Codex **result for the exact head**, or confirmed unavailability for it. |
| **Bound field** | One of three pull-request-body fields — the reconciliation witness, the Aegis skills table, the security answer — delimited by hidden sentinel lines and bound by a content hash. |
| **`482ee760bc99ca36`** | The bound-field digest of record: the first 16 hex characters of the sha256 over the body's three bound payloads in their published order. |
| **`PLACEHOLDER16`** | The literal text the body's digest line carries where the final value is recorded; it stays, because the body is frozen at the merged head. |
| **O-F1** | Stage F's one non-blocking observation: the body's skills table carries Stage A and Stage C rows only, with no Stage D, E or F row. |
| **F-F1** | The precedent that the same situation was recorded and accepted as INFO in an earlier lane's final review. |
| **AC1–AC16** | The audited plan's sixteen acceptance criteria — each an observable outcome, a threshold and the command producing its evidence. |
| **Tier `docs-only`** | The change class for a documentation-only diff (zero code), which may use the lighter review path of AEGIS-APR-129. |
| **Exact-head rule** | Every verdict and gate in this lane binds one 40-character commit SHA; a result at any other commit does not count. |

---

## 0. Verdict in one screen

| # | What was checked | Measured result in this pass | Disposition |
| --- | --- | --- | --- |
| 1 | The head never moved | `pulls/764.head.sha` re-read at **15:36:36Z**, three seconds before the merge call, with an explicit guard comparison; branch ref, pull head and the fresh checkout all `c7350242…` | **PASS** |
| 2 | `main` has drifted, and it does not matter | `origin/main` = `ac731607…` — **three integrations** (#761, #762, #763; seven commits) after `ba522f13…`; **merge base still `ba522f13…`**; three-dot diff unchanged `28/0`, `1/1`, `25/0` | **PASS** |
| 3 | No conflict | `git merge-tree --write-tree origin/main HEAD` → exit **0**, tree `1a0dd7a5…`, **identical** to the real merge commit's tree | **PASS** |
| 4 | Continuous integration at the head | **four** runs, all `head_sha c7350242…`: 2066 **failure** (the self-caught pre-repair body), 2067 / 2069 / 2070 **success**; run **2070** latest and certifies the repaired body; 24 check runs; the three path-scoped jobs **skipped by name**, never passed | **PASS** |
| 5 | The bound-field digest | re-derived **twice** (pre- and post-merge) from the byte-exact live body with the canonical script: `first16 482ee760bc99ca36`; full sha256 `482ee760…e86` | **PASS** |
| 6 | The repository's own body checker | `PR body bound fields: OK`, exit **0**, before and after the merge | **PASS** |
| 7 | `MG3` (Codex under AEGIS-APR-050) | **zero** reviews, zero inline findings, zero P1/P2; usage-limit notice **6148352811** recorded verbatim; **confirmed-unavailability branch in substance, bound by timing only — never a green** | **PRESENT (never a green)** |
| 8 | The merge | `gh api -X PUT …/pulls/764/merge -f merge_method=merge -f sha=c7350242…` → `{"sha":"05e93f499c827c4749b12cef09d2bbb7989121c4","merged":true,…}`, exit **0**; **no bypass** | **PASS** |
| 9 | `O-F1` (the skills table carries A + C rows only) | carried as an **open publication item** in the receipt — recorded, not repaired, not waived; the body stays frozen so the digest stays valid; owed to a different agent in a later change | **CARRIED** |
| 10 | The A–G chain | six prior-stage self-digests re-derived from disk — plan rev2 `3052b84b…`, AUDIT-B-rev2 `fb418436…`, SD-C `07879e38…`, SD-D `9d2013f0…`, SD-E `4af4e95f…`, SD-F `8f554598…` — **all MATCH** | **PASS** |

---

## 1. Verification basis

**Clone (fresh, this pass).** `git clone --no-hardlinks` from `clone-pq2` used only as a read-only source; `origin` re-pointed at `https://github.com/ModernNomad-98/Project-Aegis.git`; the branch ref fetched with `-c http.sslBackend=openssl` and checked out as `fu3rec-g-merger`; `main` fetched afterwards. `git status --porcelain` empty. Clone log: `_resume-2026-10-09/_fu3rec-g-merger-clone-g.log` (start 08:34:19-07:00, done 08:34:26-07:00).

**Tools.** `git` 2.55.0.windows.5 (local clone, `merge-tree`), the repository's own `scripts/check_dco.py` and `scripts/ci/check_pr_body_skills.py`, the lane's canonical digest script `evidence/docs-refresh-2026-10-12/_stagec-digest.py`, `gh` API calls, and Python for byte-exact body handling. No other network write.

**The commit.** `c7350242ad0b4728d44871bc24a18d85a1bd7fdc`, parent `ba522f133d05624c2130f15eb8ef3b6329b0f37a`, tree `fc8cc35c96efbf3a2b6e15e8271d66984213ff74`, subject `docs(approvals): record the FU-3 reconciliation attempt (AEGIS-APR-136)`, `Signed-off-by` present, `parents=1`.

---

## 2. The merge, exactly

| # | Fact | Observed |
| --- | --- | --- |
| 1 | Head at the PUT | `c7350242ad0b4728d44871bc24a18d85a1bd7fdc` — re-read at **15:36:36Z** with an explicit guard; unmoved at every read of this stage |
| 2 | Base at the PUT | `origin/main` = `ac731607124f1f849257f8db260f41451c533da7`; GitHub's `base.sha` still reads `dbf60c33…` (main's tip when the PR opened) — the merge used `ac731607…` as first parent, not that stale value |
| 3 | Shape | `commits=1`, `changed_files=3`, `additions=54`, `deletions=1`; paths: register `28/0`, open-decisions `1/1`, backlog `25/0` |
| 4 | No conflict, two ways | local `merge-tree` exit 0, tree `1a0dd7a5c7ff96ebddc364a2275cba93b9fe774a` = the merge commit's own tree |
| 5 | DCO | `scripts/check_dco.py --range ba522f13..c7350242` → `SIGNED c7350242ad0b`, `OK: 1 commit(s) checked`, exit 0 |
| 6 | The call | `gh api -X PUT repos/ModernNomad-98/Project-Aegis/pulls/764/merge -f merge_method=merge -f sha=c7350242ad0b4728d44871bc24a18d85a1bd7fdc` → `{"sha":"05e93f499c827c4749b12cef09d2bbb7989121c4","merged":true,"message":"Pull Request successfully merged"}`, exit 0, PUT stamped **15:36:39Z**. **No bypass**: no `--admin`, no protection or ruleset edit, no label, no fabricated review, no check re-run, no auto-merge, no force-push, no body edit |
| 7 | Merge commit | `05e93f499c827c4749b12cef09d2bbb7989121c4` — parents `ac731607…` + `c7350242…`, tree `1a0dd7a5…`, committer date 15:36:39Z, message `Merge pull request #764 from ModernNomad-98/docs/ber-g3-fu3-reconciliation-record-20261013` |
| 8 | Post-merge reads | `state=closed`, `merged=true`, `merged_at=2026-10-13T15:36:40Z`, `merged_by=ModernNomad-98`, `merge_commit_sha=05e93f49…`; `git/ref/heads/main` = `05e93f49…`; fetch moved `ac731607..05e93f49`; `--numstat 05e93f49^1 05e93f49` → the same three `docs/` paths |
| 9 | The records on `main` | `### AEGIS-APR-136:` exactly once; `## 14.` exactly once; the three appends are default-branch content |

---

## 3. The bound-field digest of record

**`482ee760bc99ca36`** — the first 16 hex characters of `sha256 482ee760bc99ca36de51313d1ff2cf39051bf15f6a4852556b7de86936426e86`.

Method, exactly as the body's own digest line and plan §7.3 state it: the three payloads in the order **witness → skills → security**; each field's whitespace runs collapsed to single spaces and trimmed; the three joined with single newlines; `sha256` over the UTF-8 string with **no trailing newline**; first 16 hex characters.

| Field | Normalised length | sha256 first 16 |
| --- | ---: | --- |
| witness | 1,870 chars | `561ef0e5413e47db` |
| skills | 11,924 chars | `841311d2e6440dd0` |
| security | 78 chars | `d4f2e46ef53eebf4` |
| **joined (witness · skills · security)** | | **`482ee760bc99ca36`** |

**Two reads, one value.** Re-derived from the byte-exact live body **before** the merge (15:36Z) and **again after** it (15:37Z) with the canonical script `_stagec-digest.py` — `witness chars 1870  skills chars 11924  security chars 78` then `first16 482ee760bc99ca36`, exit 0 each time.

**The live body:** **27,661 bytes**, `sha256 12969a19c5a79d4b9e665a75bed6787e53a138a269efc14a82294341def68d52` — **byte-identical to the bytes Stage F bound**, and identical before and after the merge. `PLACEHOLDER16` occurs **exactly once** and was **not** edited; a later edit to any bound field voids the Stage F verdict even though the head has not moved.

**Repository's own checker:** `python -B scripts/ci/check_pr_body_skills.py --body-file <live body> --author ModernNomad-98` → `PR body bound fields: OK`, exit **0** (pre- and post-merge). The checker is **structural only** — its own docstring says no hash equality, no content grading — so it corroborates the fields' shape and is **not** evidence for the digest; the digest is this stage's own computation.

---

## 4. The merge gates at the exact head `c7350242…`

| Gate | Condition | Status at this exact head |
| --- | --- | --- |
| **`MG1`** | every applicable check green at that exact head | **met** — four runs at this head; latest **2070** success; required `gate-guard` and `validate-skills` green; three path-scoped jobs **skipped by name, never passed** (§5) |
| **`MG2`** | final PR review posted, accepted, naming that exact head | **met** — `SD-F ACCEPT`, comment **6149151592** (2026-10-13T15:32:14Z), head-bound to `c7350242…` and to this digest; evidence `FU3-RECORD-FINAL-REVIEW-F.md` sha256 `8f554598…` re-derived **MATCH** |
| **`MG3`** | a Codex **result for that exact head**, or confirmed unavailability for it | **present on the confirmed-unavailability branch — bound by timing only, never a green** (§6) |
| **`MG4`** | the merge agent confirmed **its own** authority | **met** — `AEGIS-APR-100` re-read on `main` (`APPROVAL_REGISTER.md:3075`: GRANT, ACTIVE, grantor Peter Nguyen, standing and forward-only) plus `AEGIS-APR-050/049/002/013/048`; branch protection read live: `contexts=[gate-guard, validate-skills]`, `strict=false`, `required_approving_review_count=1`, `enforce_admins=false` → `mergeable_state=blocked` was the **review requirement, not a conflict**; no protection, ruleset or setting was changed |
| **`MG5`** | outside-contribution additional security review | **not applicable** — a maintainer/agent PR, not an outside contribution; the bound security field answers **Yes** and names `docs/approvals/APPROVAL_REGISTER.md`, which is recorded |

---

## 5. Continuous integration at the head — four runs

| Run | Id | Created → finished (UTC) | Conclusion | Note |
| --- | --- | --- | --- | --- |
| **2066** | `38417138626` | 14:52:35 → 14:54:26 | **failure** | the self-caught pre-repair body: `pr-body-skills-check` failed on skills rows without a `Row source` record; the lane's own gate caught its own defect |
| **2067** | `38417565079` | 14:55:30 → 14:57:39 | success | repaired body |
| **2069** | `38419969798` | 15:11:56 → 15:13:56 | success | repaired body |
| **2070** | `38420055605` | 15:12:32 → 15:14:12 | **success (latest)** | **certifies the repaired body**; its checker step printed `OK` and its DCO step printed `OK: 1 commit(s) checked` |

**24 check runs** (6 jobs × 4 runs) attach to the head. `windows-offline-checks`, `tools-tests-linux` and `tools-tests-windows` are **completed / skipped** in every run — *named skipped, never passed*. All four runs carry the same `head_sha`, so every repair was a **body edit**, never a force-push. Required contexts on `main`: `gate-guard` and `validate-skills`; both green on the latest run. No check was removed, loosened, re-run by hand or waived.

---

## 6. `MG3` — the Codex disposition, verbatim and never a green

```text
GET /pulls/764/reviews   -> 0 objects
GET /pulls/764/comments  -> 0 inline findings (review_comments = 0)
timeline                 -> one Codex event only: "commented" 2026-10-13T14:52:38Z
issue comments           -> 3: 6148352811 (Codex notice), 6148473581 (Stage C record),
                            6149151592 (Stage F verdict)
```

The recorded unavailability, **byte-verbatim** — issue comment **6148352811**, `chatgpt-codex-connector[bot]`, `2026-10-13T14:52:38Z` (`created == updated`):

> You have reached your Codex usage limits for code reviews. You can see your limits in the [Codex usage dashboard](https://chatgpt.com/codex/cloud/settings/usage).

**Disposition.** `AEGIS-APR-050` names *"a usage-limit notice"* as its own example of confirmed unavailability, so the branch is right **in substance**, and **zero P1/P2 findings exist, so nothing is owed to triage**. Stated honestly: the notice is a **pull-request-level** comment that names **no head** — it was posted at 14:52:38Z, after this head's commit existed (14:50:46Z), and the head never moved — so it is bound to `c7350242…` **by timing only**, not by a per-head statement from Codex. **It is never a green**: no artefact records Codex as having reviewed, approved or passed this change. A later Codex review must be re-checked at the then-current head; a result at a superseded head would not satisfy `MG3`.

---

## 7. Acceptance-criteria routing at the merged head (restated, never upgraded)

| AC | Disposition | Basis |
| --- | --- | --- |
| **AC10** exactly three files, all Markdown under `docs/` | **MET** — re-measured this stage | `--numstat` against the parent, against the moved `origin/main` (three-dot) and on the merge commit vs its first parent all return the same three `docs/` paths (`28/0`, `1/1`, `25/0`) |
| **AC12** DCO on every commit | **MET** — re-run this stage | `check_dco.py` exit 0, `OK: 1 commit(s) checked` |
| **AC13** the body carries the three bound fields correctly | **MET** — re-derived this stage, with **O-F1 carried** | byte-exact body; 3 sentinel pairs; 12 skills data rows (6 A + 6 C) + 12 `Row source` records + Stage B absence record; security **Yes** naming the register; checker exit 0; digest `482ee760bc99ca36` named |
| **AC14** the automated review under `AEGIS-APR-050` is recorded | **MET on the record, never a green** | §6 |
| **AC1–AC9, AC11, AC15, AC16** | **as recorded by Stages C, D, E and F at this head — not re-graded, not upgraded here** | measured at `c7350242…` by those stages; this stage re-verified the union the merge rests on and re-derived the six prior-stage self-digests (§8) |

No criterion is re-opened by the merge and none is upgraded by it. `SD-D` and `SD-E` were plain `ACCEPT`s, so no unrun list is carried forward.

---

## 8. The A–G chain (self-digests re-derived in this stage)

| Stage | Verdict / artifact | Identifier |
| --- | --- | --- |
| A — PLAN | `FU3-RECORD-PLAN-rev2.md` | sha256 **`3052b84b746ce05f06d3c9a4b7ae85c0ce2dfaa6bc9af3ddf891a9787c279bd4`** — MATCH |
| B — plan audit | **`SD-B ACCEPT`** — `FU3-RECORD-AUDIT-B-rev2.md` | sha256 **`fb418436af2463a111608a0f997919db84857294f77df6e2ebb283b49d60fdf8`** — MATCH |
| C — IMPLEMENT | `fu3-record-implementer-c` — `FU3-RECORD-SD-C.md` | sha256 **`07879e382f1fb244e88cc9714040f1c80098750b93d322f1d554cb239be2a81d`** — MATCH |
| D — independent implementation audit | **`SD-D ACCEPT`** — `FU3-RECORD-AUDIT-D.md` | sha256 **`9d2013f0eb8204db86b990e54f7fbecb3fb260a98df5c75fcc70008cf15a7ce9`** — MATCH |
| E — VALIDATE | **`SD-E ACCEPT`** — `FU3-RECORD-VALIDATE-E.md` | sha256 **`4af4e95f22e4a96e8d6fd17a77b6b0a0bd75891de3666eb0e21613d60fcea80d`** — MATCH |
| F — final independent PR review | **`SD-F ACCEPT`** — comment **6149151592**; `FU3-RECORD-FINAL-REVIEW-F.md` | sha256 **`8f554598a04d91567fbb10e301d1a8bc1e0c2940b2a82fb8a5bac4be9258937b`** — MATCH |
| G — MERGE | **this record** — receipt comment **6149285129**; merge commit **`05e93f499c827c4749b12cef09d2bbb7989121c4`** | this file, with its own sha256 footer |

Convention: replace the 64 hex characters on the line beginning `sha256:` with the literal `{{SHA256}}`, then hash the UTF-8 bytes including the final newline, LF only — byte-exact replacement, not a whitespace-tolerant pattern.

---

## 9. `O-F1` — the carried open publication item

**Recorded as an open publication item, exactly as the coordinator directed and as the `F-F1` precedent supports.** The body's skills payload publishes **12** data rows — 6 Stage A (`fu3-record-planner-a-rev2`) and 6 Stage C (`fu3-record-implementer-c`) — plus the explicit Stage B absence record; there is **no Stage D, E or F row**, and **no stage read a skill** (Stages D and E name no Aegis skill, and Stage F's rows were authored inside its own evidence file §11 and never inserted into the body). `docs/delivery-workflow.md:182` words the `SD-F` condition as a table "with a row for every stage that ran".

**Disposition:** a known, declared gap — **not** a satisfied check and **not** a defect found by this stage; **non-blocking**, because no acceptance criterion's threshold depends on it (AC13's threshold is met either way).

**Why carried and not repaired:** inserting a D/E/F row edits the **skills** bound field and would **void `482ee760bc99ca36`** — the digest Stage F's verdict named and this receipt records. The authorized repair is a **new change** by the authorized publisher (Stage F captured its own row text and binding in its §11), which voids the digest and returns through a **fresh `SD-F`** at its own head. The body was not edited by this stage, so the recorded digest remains valid for the merged head. **Owed to:** a different agent, in a later change. **Severity:** INFO/Low.

---

## 10. Timing — *FU-3 reconciliation record lane Stage G merge*

| | |
| --- | --- |
| **Item** | `FU-3 reconciliation record lane Stage G merge` |
| **Start** | **2026-10-13T08:33:38-07:00** (= `2026-10-13T15:33:38Z`, America/Los_Angeles) — the stamp at which the brief was received and the ETA was stated in the first action |
| **ETA at start** | **~20 minutes** of wall time |
| **Merge instant** | **2026-10-13T15:36:39Z** (PUT, head pinned) / **15:36:40Z** (`merged_at`) |
| **Receipt posted** | **2026-10-13T15:39:06Z** — comment **6149285129** |
| **Finish** | **2026-10-13T08:39:05-07:00** (= `2026-10-13T15:39:05Z`) — the stamp this record's receipt was stamped with at post time |
| **Wall** | **5m 28s** |
| **ETA vs wall** | inside the stated ~20-minute ETA: 5m 28s of elapsed wall time (ETA ~20 min vs wall 5m 28s — ahead of the estimate) |
| **Active time** | not separately instrumented; wall time is the honest measurement, so the ETA comparison is imperfect and is labelled as such |

---

## 11. Boundary — what this stage did not do

- **No repository, branch, commit, tag, label or body write.** The only GitHub writes are the merge PUT and the receipt comment.
- **The pull request body was not edited — not one byte.** `PLACEHOLDER16` remains; the digest of record is **recorded**, never filled in. (The instruction "do NOT edit the PR body" was honoured exactly.)
- **No reconciliation was performed and no usage figure is asserted either way** — headroom against the BER-DEC-008 lifetime maxima remains **UNVERIFIABLE, not zero and not positive**; the standing zero-residual posture is unchanged.
- **Nothing was bypassed:** no protection or ruleset edit, no review fabricated or dismissed, no check re-run or waived, no force-push, no auto-merge.
- **Not re-graded here, by design:** the correctness of the historical search inside the records, the Stage A/B plan and audit texts, and the three integrations `main` gained after `ba522f13`. No subagents were used.

---

## 12. Verification commands (reproducible at `c7350242ad0b4728d44871bc24a18d85a1bd7fdc`)

```text
git -C <clone> rev-parse HEAD HEAD^ HEAD^{tree}                  -> c7350242…, ba522f13…, fc8cc35c…
git -C <clone> merge-base HEAD origin/main                       -> ba522f133d05624c2130f15eb8ef3b6329b0f37a
git -C <clone> rev-list --count --merges ba522f13..origin/main   -> 3 integrations (7 commits) to ac731607…
git -C <clone> diff --numstat origin/main...HEAD                 -> 28/0 register, 1/1 open-decisions, 25/0 backlog
git -C <clone> merge-tree --write-tree origin/main HEAD          -> exit 0, tree 1a0dd7a5c7ff96ebddc364a2275cba93b9fe774a
python -B scripts/check_dco.py --range ba522f13..c7350242        -> exit 0, "OK: 1 commit(s) checked"
python -B scripts/ci/check_pr_body_skills.py --body-file <body> --author ModernNomad-98 -> "PR body bound fields: OK", exit 0
python -B _stagec-digest.py <byte-exact live body>               -> first16 482ee760bc99ca36
gh api -X PUT repos/ModernNomad-98/Project-Aegis/pulls/764/merge -f merge_method=merge -f sha=c7350242… -> merged=true, 05e93f49…
gh api repos/ModernNomad-98/Project-Aegis/pulls/764/reviews      -> []
gh api repos/ModernNomad-98/Project-Aegis/issues/comments/6148352811 --jq .body -> the usage-limit notice, verbatim
gh api 'repos/…/commits/c7350242…/check-runs?per_page=100'       -> 24 check runs (6 jobs x 4 runs)
```

<!-- sha256 footer: the hash below covers this file's bytes with the digest line's value replaced by the
     literal placeholder {{SHA256}}, so the digest is stable and independently reproducible.
     Verify by replacing the 64 hex characters on the line beginning "sha256:" with {{SHA256}}, then
     hashing the UTF-8 bytes including the final newline. Line endings are LF only. -->
sha256: 059822aabffb13cb417adcd1714bb00a90244c0df040a457db7ba9ac895bb2d7
