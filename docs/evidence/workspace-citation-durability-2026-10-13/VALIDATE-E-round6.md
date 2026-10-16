# WORKSPACE-CITATION DURABILITY — STAGE E ROUND 6: RE-BIND AT THE APPENDED-REPAIR HEAD

**Item:** "Stage E ROUND 6 — re-bound rows at head 35acbbe8" — in plain words, *the second re-binding of this stage's skills rows, produced as a new record rather than an edit, after the disclosure append moved the head again.*

**Agent:** `of1-stage-e` — the Stage E holder, a **different holder from** Stages A, B, C and D. **No subagents. Nothing was delegated.** **Skill dogfooded:** `acceptance-criteria-reviewer` — in plain words, *the Aegis skill that judges a criterion on an observable outcome, a threshold and the evidence* — applied here to the repair itself: whether the new log entry **actually discloses** what it claims to disclose. Secondary: `skill-usage-ledger` for this round's rows in section 7.

| | |
| --- | --- |
| **Head** | `35acbbe8bc5913a94988610ed77de9b8827d908f` — in plain words, *the tenth commit on the branch, which appends a section-13 entry recording an in-place log edit and the corrected counts.* **Linear move confirmed:** `c46d9057` is an ancestor (merge-base test rc=0) |
| **Pinned base** | `dbe2ee28559fef88950b2d8822cf72d3e595ba86` |
| **Body revision** | stored body **87,014 bytes**, `sha256 9651599790ce35c6ca2a419e3845239e528b5a99ccceabfbc3734fbb1ea22764`, 0 CRLF — recomputed here |
| **Bound-field hash** | first-16 **`04e1383bd03e971c`**, recomputed here — **unchanged across the move**, which is exactly why it cannot stand in for a re-read |
| **Outside the bound fields** | **25,755 of 87,014 bytes (29.6%)** by my own measure. The skills field spans **L152–L257** and **includes prose**, so any edit in that range moves the hash, and the hash moving does **not** imply the table changed |
| **Body census** | **34 data rows, 34 `Row source` records** — recomputed |
| **Writes** | exactly **one file** (this record). **No repository write, no commit, no push, no body edit, no comment, no label, no merge.** **`VALIDATE-E-round5.md` is left on disk unchanged** |

---

## 1. Why there is a round 6, and why round 5 is stale on arrival

**Round 5 was authored against `c46d9057`, which was the head when the Lead asked for it. The Lead then landed the section-13 disclosure append — `35acbbe8` — which is the head now.** The Lead has recorded the sequencing as their own error, and it is worth stating plainly in this record for the reason the Lead gave: **a row that names a superseded head is honest about the head it was authored against and honest that it no longer governs.** That is the correct handling, not a defect.

**The append exists because of a finding one stage over, and it traces back to my E-8.** Stage D found that the E-8 repair itself had **edited a section-13 entry in place**, which the log's own rule at **L2672–L2675** forbids, and that the edited entry's sentence *"no existing line of this file is edited"* was therefore **false of its own entry**; it also found the entry said the inventory was **seven** where the record carries **eight**. The Lead upheld both and repaired them by **appending**.

**Round 5 stays on disk unchanged.** It is a superseded binding, and a superseded binding has to stay checkable. Rounds 1–4 likewise.

---

## 2. The disclosure append, verified against its own text

I re-derived the delta myself: **`git diff c46d9057 35acbbe8` → one file, 34 added / 0 deleted** — the backlog only. The new entry is at **L4280**, immediately before `## 14.`, and I checked each of the four things a disclosure of this kind has to do:

| What it must do | Verified in the entry |
| --- | --- |
| Name the entry it addresses | **Yes** — *"the entry directly above (L4253-L4279, 'three corrections to the two entries above'), specifically its Correction 2 text at L4265-L4271"* — **by heading AND line range** |
| Disclose the deviation and the rule it broke | **Yes** — *"Commit `c46d9057` **edited that entry's Correction 2 in place** — a 1-line change at L4267 … **That departs from the rule at L2672-L2675**"*, and it records why the reasoning used was wrong (*"the entry merges with this pull request, and at merge it would have asserted something false about itself"*) |
| State that the superseded entry's own claim is no longer true | **Yes** — *"L4257-L4258 says the entry was 'Appended under this log's rule … no existing line of this file is edited.' After `c46d9057` that sentence is **false of its own entry**. No reader should rely on it."* |
| State the corrected facts, and not revive the retracted exception | **Yes** — **four** sites, **eight** inventory items; the fifth candidate (the searched-roots list) **deliberately retained** on **scope**; and explicitly *"**This entry does not revive the prior-publication exception**, which Correction 2 withdrew."* It also records that Correction 2's own line still reads seven and **does not edit that line** |
| Grant nothing | **Yes** — *"New Scope: … edits no existing line of this file, and grants no authority. It is insert-only. **New authority:** None."* |

**The repair is an append, not a revert**, and the entry says why: reverting would re-introduce the false claim the edit corrected. **My E-8 substance is untouched and remains repaired** — re-verified at this head: item 4 reads **"four sites"**, the token is **"the distro-side directory name"**, item 5 records the searched-roots list as **"NOT sanitized, deliberately"**, and the old false phrase is **absent**.

**One count convention differs, and I record it rather than reconcile it silently.** My method counts `^### ` between `## 13.` and `## 14.`: **24 → 25** entries across this move. Counting every `###` in the file gives **74 → 75**. The Lead and the publisher quote **75 → 76**. **The delta agrees in all three readings (+1 entry, the append); the absolute figure differs by counting convention** — the same class of difference as the earlier 14-versus-119 measurement, and the reason this lane now names methods beside counts.

---

## 3. The eleven criteria, re-measured at 35acbbe8

| # | Criterion | Verdict | Threshold | Observed at this head |
| --- | --- | --- | --- | --- |
| **AC1** | Three byte-identical copies + one labelled derivative | **PASS** | 3 of 3 + 1 labelled | **3 of 4** byte-identical (`c0b0c548…`, `d2ed1cfb…`, `f367d36e…`); `BER…` is the derivative (27,721 B / `89005849…`), unchanged by this move |
| **AC2** | The copies' integrity claims hold | **PASS** | 3 footers + body digest | Copies untouched by the delta; footers and `81884e0d…` still recompute |
| **AC3** | Added links resolve | **PASS** | rc 0, broken 0, dead 0, anchors >= 4 | rc=0; 4 files, 199 links, **33 anchors**, broken 0, dead 0 |
| **AC4** | Corpus link check green | **PASS** | all batches 0; 663 pages | **663 paths, 9 batches, 0 failed** |
| **AC5** | Stated page count = measured rows | **PASS** | 17 = 17 | 17 rows; `17 selected`, `these 17 pages` |
| **AC6** | Log append-only; frozen note unchanged | **PASS** | deletions 0; note identical | **backlog vs base: 122 added / 0 deleted** — insert-only, and this move added 34 of them with zero deletions. Frozen block still **`f29decc72f1ee1b31d410ead380ce55c46081e2890d004947d9e4a43e00b182d`** |
| **AC7** | Declared file set; exactly three lines replaced | **PASS** | 8 paths; deletions 3 | **8 paths**; cumulative deletions **3** |
| **AC8** | Pattern as printed, counting lines, three figures | **PASS** | 4 / 1 / 0 | **hits_on_copies = 4**; **hits_on_record = 1** (the record's own pattern quotation at **L216**); **substantive = 0** |
| **AC9** | Fresh checkout retrieves the evidence | **PASS** | 4 digests; archive_dependent 0 | Fresh clone at `35acbbe8`, **archive present: False**; `link_targets = 12`, **archive_dependent_targets = 0**, `map_occurrences = 12`, **occurrences_outside_map = 0** |
| **AC10** | No protected path, printed control counts | **PASS** | 371 / 11-11 / 0-4 / 0-8 / 0-12 / 0 | `pattern_len 371`; `POS 11/11`; `DOC_NEG 0/4`; `DECLARED 0/8`; `NEGATIVES_TOTAL 0/12`; `CONTROL_FAILURES 0` |
| **AC11** | The rule in all three placements | **PASS on threshold; O-4 carried** | PRESENT 3 of 3 | **PRESENT 3 of 3** normalised; raw contiguity False in all three |

**Tally: 11 PASS · 0 FAIL · 0 criterion-level UNRUN** — every value re-measured at this head, and **not one moved** from the previous measurement.

**Line anchors re-derived at this head:** README **L130 → BER L218** (STOP RECORD) OK; **L152 → BER L126/L127** OK; **L133 → REVIEWPATH L68** (F-F1) OK. **0 mismatches.**

---

## 4. Disposition

> ## **SD-E: INCOMPLETE — UNRUN LISTED**

**Written with its prefix**, per `docs/delivery-workflow.md` L56–L61, in the workflow's own vocabulary and no other token. **Affirmative** under L185–L188 — all three unrun checks satisfy (a). **Not PASS** because L193 says unrun coverage is never a pass. **Not FAIL** because nothing failed.

**Bound to head `35acbbe8…`.** The body measured is `96515997…` / `04e1383bd03e971c`. **All eleven criteria are properties of the repository at the head; none reads the pull-request body** — so the pending insertion of the staged rows moves the body binding and **cannot change any criterion**. **The head will not move**, and the Lead has declared the freeze.

---

## 5. UNRUN register, CI, and the repository's own checks

| # | Unrun check | Why it did not run here | Satisfies | What would resolve it |
| --- | --- | --- | --- | --- |
| **U-1** | `scripts/tests/test_validator.py` | the sandbox denies the `chmod` this suite performs on its own temporary directory, in `%TEMP%` and with `TEMP`/`TMP`/`TMPDIR` redirected into the workspace | L185–L188 **(a)**: run by the named `validate-skills` job at this exact head | A host without the sandbox limit, or acceptance of the CI evidence |
| **U-2** | `scripts/tests/test_markdown_links.py` | same denial | **(a)**: the same job's link-checker self-test step | As U-1 |
| **U-3** | `gate-guard` as the **actual bash step** | `bash` is denied in this session (`Bash/E_ACCESSDENIED`) | **(a)**: the `gate-guard` **check run is success** at this head, **plus** my own evaluator of the 371-character `gate_pattern` over all 8 changed paths and 11 positive controls | A host where `bash` runs |

**UNRUN is never PASS**; none of the three is absorbed, and **no criterion is UNRUN**.

**Re-run by me at this head:** `validate-skills` rc=0, `OK: 205 skill(s) valid, 0 warning(s)`; `check_dco.py --range origin/main..HEAD` rc=0 with **ten commits all signed** and a line beginning `OK: 10 commit(s) checked, all signed off or exempt.`; AC3 rc=0 (33 anchors); AC4 663 paths, 0 failed. Path-scoped jobs (`tools-tests-linux`, `tools-tests-windows`, `windows-offline-checks`) — **skipped by path condition, recorded as skipped, never as passed**.

---

## 6. Boundary

- **No repository write.** No commit, branch, push, tag or merge. **No pull-request write** — the rows in section 7 are authored and handed over.
- **No repair.** The append is the Lead's; I verified it and changed nothing. OBS-1, O-4 and O-6 remain carried and unedited.
- **`VALIDATE-E-round5.md` and rounds 1–4 are left on disk unchanged**, each bound to its own head and each still checkable.
- **No assumption** that any earlier disposition carries to this head — section 3 re-measures rather than inherits.
- **No touch** of `clone-pq1`, `clone-pq2`, the legacy checkout, any `wt-*` worktree, the paused VirtualBox VM or the WSL distro. **No subagents, no delegation.**

---

## 7. Skills this stage used — Stage E ROUND-6 rows, copy-ready for the publisher

**Author:** `of1-stage-e`, Stage E, **round 6**. **Target:** `35acbbe8bc5913a94988610ed77de9b8827d908f`. **Why new rows:** `docs/delivery-workflow.md` L693–L694. Rounds 1–5 are bound to `bd210954`, `c5f71554`, `95351dda`, `92437891` and `c46d9057`. Per L696–L699 older row **strings** stay unchanged and their source records are marked historical or superseded. **I did not insert these rows.**

**Exact captured row text** — the two lines inside the fence below, joined by LF plus one trailing LF, UTF-8, **1,718 bytes**:

```text
| [acceptance-criteria-reviewer](.claude/skills/acceptance-criteria-reviewer/SKILL.md) | Stage E round 6 / `of1-stage-e` | Re-bound to the appended-repair head, and used its outcome/threshold/evidence split to test the repair itself rather than describe it: whether the new section-13 entry actually discloses the in-place edit, whether it states the corrected counts, and whether the E-8 substance survived the move. All eleven criteria were re-measured at the new head rather than carried - the cumulative diffs, the three byte-identical copies, the AC8 figures and every line anchor re-derived identically - and one count convention was found to differ between my method and the lane's, which is recorded rather than reconciled silently. | `VALIDATE-E-round6.md` sections 2 and 3 - the eleven criteria re-measured at this head, and the disclosure-append verified against the entry's own text |
| [skill-usage-ledger](.claude/skills/skill-usage-ledger/SKILL.md) | Stage E round 6 / `of1-stage-e` | Used its workflow again for this round's own record: both skill names were re-resolved against `tools/skills-manifest.json` at the head under test and both digests recomputed from `.claude/skills/<name>/SKILL.md` with CRLF-to-LF normalisation, so the manifest is proven current rather than assumed. Its `incomplete` field names this round's unrun checks instead of asserting completeness. | `acceptance-criteria-reviewer` = `c6e5d5649bf89658036cf38abba9c626701220e7b00831c2d843ceff94d81021`, `skill-usage-ledger` = `6a27b5c8e690b605d7dca4b0e4c2ff1d67dfa6ac6c18469d5657b4ff093339a4`, both recomputed and matching; `tools/skills-manifest.json` sha256 `9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832` |
```

**`sha256` of that exact captured row text:**

`b9ad5aba780738e44e7a62e8b614386065ee6c6ca8200c3bf4eb89c0945565ed`

**`Row source` records for the two rows** — excluded from the digest above, so there is no self-reference:

```text
<!-- Row source: agent=of1-stage-e; stage=E; round=6; row=SDE6-1; target=35acbbe8bc5913a94988610ed77de9b8827d908f (this pull request's candidate head); source=_resume-2026-10-09/evidence/workspace-citation-durability-2026-10-13/VALIDATE-E-round6.md section 7 fenced block row 1 (the exact bytes hashed); binding=sha256 b9ad5aba780738e44e7a62e8b614386065ee6c6ca8200c3bf4eb89c0945565ed over the fenced block's UTF-8 bytes including the final newline (the two Stage E round-6 row lines joined by LF plus one trailing LF, 1,718 bytes); manifest=tools/skills-manifest.json sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832; limits=the row source is a session-workspace artifact and is not retrievable from this repository - see round 4 section 7 observation O-6. -->
<!-- Row source: agent=of1-stage-e; stage=E; round=6; row=SDE6-2; target=35acbbe8bc5913a94988610ed77de9b8827d908f (this pull request's candidate head); source=_resume-2026-10-09/evidence/workspace-citation-durability-2026-10-13/VALIDATE-E-round6.md section 7 fenced block row 2 (the exact bytes hashed); binding=sha256 b9ad5aba780738e44e7a62e8b614386065ee6c6ca8200c3bf4eb89c0945565ed over the fenced block's UTF-8 bytes including the final newline (the two Stage E round-6 row lines joined by LF plus one trailing LF, 1,718 bytes); manifest=tools/skills-manifest.json sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832; limits=the row source is a session-workspace artifact and is not retrievable from this repository - see round 4 section 7 observation O-6. -->
```

**Manifest provenance.** Both names resolve in `tools/skills-manifest.json` — itself `sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832` — and both digests were recomputed from `.claude/skills/<name>/SKILL.md` with CRLF→LF normalisation: `acceptance-criteria-reviewer` = `c6e5d5649bf89658036cf38abba9c626701220e7b00831c2d843ceff94d81021`, `skill-usage-ledger` = `6a27b5c8e690b605d7dca4b0e4c2ff1d67dfa6ac6c18469d5657b4ff093339a4` — both **match**.
**No preclaiming:** the row text contains neither its own digest nor any bound-field hash (checked against `04e1383b`, `96515997`, `35acbbe8`, `f29decc7`, `89005849`, `b109aeff` — all absent), per L720–L721.
**Sequencing:** this pair is inserted **with Stage D's fresh pair and Stage F's sixth capture in one edit**, after which the body is FINAL and Stage F hashes. Because the **skills field spans L152–L257 and includes prose**, a moved hash does not prove the table changed and an unmoved hash does not prove the insertion landed — **only a re-read of the payload settles it.**

---

## 8. Timing

| | |
| --- | --- |
| **Item** | *Stage E ROUND 6 — re-bound rows at head 35acbbe8* |
| **Start** | **`2026-10-13T13:42:08-07:00`** (America/Los_Angeles) — the modification stamp of the first file this round wrote, the earliest start I can **evidence**. No start stamp was issued for this re-bind; I have not invented one. |
| **Finish** | **`2026-10-13T13:43:26-07:00`** (America/Los_Angeles) — sampled in the same program run that performed this file's write |
| **Measured wall time** | **`1 minutes 17 seconds (77 seconds)`** — evidenced start to final write |
| **Active time** | **not separately instrumented.** Wall time is the honest measurement, so the ETA comparison is **IMPERFECT** and is labelled as such rather than presented as an active-time split. |

---

<!-- sha256 footer: the hash below covers this file's bytes with the digest line's value replaced by the
     literal placeholder {{SHA256}}, so the digest is stable and independently reproducible.
     Verify by replacing the 64 hex characters on the line beginning "sha256:" with {{SHA256}}, then
     hashing the UTF-8 bytes INCLUDING the final newline. Line endings are LF only. -->
sha256: acac866b2eac59a2149287900a4fdb69f3b6291141f5028b7958a4d5e1619f93
