# WORKSPACE-CITATION DURABILITY — STAGE E ROUND 3: VALIDATION AT THE FINAL HEAD

**Item:** "Workspace-citation durability — Stage E ROUND 3 — validate at head 95351dda" (shared task `task-26`) — in plain words, *the third run of the validation stage for this change, required because five further review findings and a superseding log entry moved the head after round 2 finished.*

**Agent:** `of1-stage-e` — the Stage E holder, and a **different holder from** Stage A (`wcd-stage-a`), Stage B (`wcd-stage-b`), Stage C (`wcd-stage-c`) and Stage D (`of1-stage-d`). **No subagents. Nothing was delegated.**

**Skill dogfooded:** `acceptance-criteria-reviewer` — in plain words, *the Aegis skill that judges whether a criterion names an observable outcome, a pass-or-fail threshold and the evidence that will prove it, and returns one verdict per criterion.* Secondary: `skill-usage-ledger` — in plain words, *the Aegis skill that produces the record of which skills a task used, bound to the skills manifest* — for this round's rows in section 7. Both read in full from `.claude/skills/` at the head under test.

**Reading key — every label in this record, in plain words (the owner's permanent reporting rule).**
- `P2-1` … `P2-5` — *the five Codex review findings raised at the round-2 head, each of which Stage C repaired.*
- `P2-6` — *the superseding section-13 entry, which corrects one word of the publication entry after the Lead ruled it false.*
- `sanitized derivative` — *a published copy whose bytes differ from its archive source because private identifiers were removed and three wrong claims corrected, with every difference enumerated.*
- `O-F1` — *observation F1 from the FU-3 record lane, whose frozen note this change makes retrievable.*
- `gate_pattern` — *the regular expression read from the skills-validation workflow that decides which changed paths are protected.*
- `DCO` — *the Developer Certificate of Origin sign-off trailer every commit must carry.*
- `bound fields` — *the three pull-request-body fields the process acts on: the reconciliation witness, the Aegis skills table and the security answer.*
- `Row source` — *the provenance record inside the skills bound field binding each published row to its author, stage, round, target and source.*
- `UNRUN` — *a check that did not run. Unrun coverage is never a pass.*

---

## 1. What was validated, and at exactly which revision

| | |
| --- | --- |
| **Pinned base** | `dbe2ee28559fef88950b2d8822cf72d3e595ba86` |
| **Head validated (40 characters)** | `95351dda27210f4b5707aa067cd138bf37710bd5` — in plain words, *the fifth commit on the branch, which supersedes one word of the publication entry.* Five commits on the base: `bd210954`, `b591e0d9`, `c5f71554`, `61e73442`, `95351dda` |
| **Body revision** | **stored body 58,462 bytes**, `sha256 b1b88d120104e6c4a3cbfd1ef4e1f9604ad82bb9d53485fadd7cfb2947b70b7c`, 0 CRLF |
| **Bound-field hash** | first-16 **`9114b83bcfbd2cdb`**, recomputed here (full `sha256 9114b83bcfbd2cdb680646abca86fa85fd5a0a0e9d07fab8206eaac37ea10883`) |
| **The hash is unchanged; the body is not** | The hash carried over from the previous revision while the **body text changed** (58,462 vs the round-2 body). This is not a contradiction and it is the reason this round exists: **the hash covers only the three bound fields**, and `20,748 of the body's 58,462 bytes (35.5%)` lie **outside** them, by my byte measure. A change anywhere outside the sentinels leaves the hash identical. **The hash is not a body checksum and must never be read as one.** (Stage D measured 20,749; the one-byte difference is the body's terminating newline convention. The figure, not the byte, is the point.) |
| **Byte-count convention, named** | Every body figure here is the **stored body** — the JSON `.body` value written back byte-for-byte. A `gh … --jq .body` redirect appends one trailing byte, which is why the same revision also reads 58,463. The hash is convention-independent. |
| **Superseded bindings** | Round 1 was bound to `bd210954` / `6f36dda8…`; round 2 to `c5f71554` / `eeb359259b517578`. Both heads have moved, so both dispositions are void and this record replaces them. |
| **Writes** | exactly **one file** (this record) plus a throwaway single-branch clone for AC9. **No repository write, no commit, no push, no body edit, no comment, no label, no merge.** |

**Verifier discipline.** Both verifiers were validated before use. The **footer verifier** reproduced three known-good seals (`250cc3e8…`, `73254f26…`, `c2d106af…`). The **body-digest verifier** was re-validated against `REVIEWPATH-FINAL-REVIEW-F.md`'s own stated method before being used on anything else — the method I had to adopt in round 1 after my first approach disagreed with that file. **No seal was accused without a validated verifier.**

---

## 2. Disposition

> ## **SD-E: INCOMPLETE — UNRUN LISTED**

**Written with its prefix**, per `docs/delivery-workflow.md` L56–L61, in the workflow's own vocabulary and no other token.

**All eleven acceptance criteria PASS at this head**, every one re-derived rather than inherited.

**Why not PASS.** L193: *"UNRUN is never PASS."* Three session-level checks could not run in this session (section 5). **Why affirmative:** per L185–L188 the disposition is affirmative when every unrun check is either (a) run by a named CI job at that exact head, evidenced, or (b) listed with what would resolve it — all three satisfy (a) at `95351dda`. Per L190–L193, **SD-F must accept this list and SD-G's receipt must record it.**

**Why not FAIL.** Nothing failed. Two observations are **carried**, both on the Lead's ruling and both recorded rather than repaired: **OBS-1** (the retained finding text's length label uses a UTF-16 code-unit count) and **O-4** (AC11's Outcome clause drifted because a mandated repair rewrote the prose it described). Neither is a defect and neither is a criterion failure.

**Bound to what.** Head `95351dda…` **and** body `b1b88d12…` / `9114b83bcfbd2cdb`. **The body will move once more** — it carries Stage E's round-2 rows, which are bound to `c5f71554` and cannot stand for this head (L693), so section 7 authors this round's rows. When they land the body binding moves again; the head, the diff and the eleven criteria do not.

---

## 3. The eleven-criterion verdict table

| # | Criterion | Verdict | Threshold | Observed |
| --- | --- | --- | --- | --- |
| **AC1** | The cited records are published — **AMENDED: three byte-identical copies plus one explicitly labelled SANITIZED DERIVATIVE** | **PASS** | **3 byte-identical of 3, plus 1 labelled derivative** (supersedes "4 of 4") | The three are byte-identical to their archive sources: `c0b0c548…` (30,777 B), `d2ed1cfb…` (25,454 B), `f367d36e…` (21,023 B). `BER-G3-FU3-EXECUTION.md` is a **labelled sanitized derivative**: source 25,606 B / `ea521f84…` → committed 26,345 B / `cc183e45…`, with **both sides given in the table** and every difference enumerated in section 1.1. **The body states the amendment explicitly, not silently** — at L6, at L58-L59, in the table's own wording, and in the superseding log entry |
| **AC2** | The published copies' own integrity claims still hold | **PASS** | 3 of 3 footers + the body digest | The derivative's footer was **recomputed over the derivative** (`3a4d32645e0e2189…`, MATCH); `8f554598…` and `059822aa…` unchanged and MATCH; `REVIEWPATH-FINAL-REVIEW-F.md`'s body digest `81884e0d…` recomputes over 20,338 bytes / 102 lines |
| **AC3** | Every link the change adds resolves, including heading fragments | **PASS** | exit 0, broken 0, dead 0, anchors >= 4 | `{"files": 4, "checked": 199, "anchors": 33, "broken": 0, "dead": 0}`, rc=0. **The superseding entry's section 1.1 anchor was probed specifically**: rc=0, `dead: 0` — it resolves |
| **AC4** | The corpus-wide link check is still green | **PASS** | every batch exits 0; broken 0; dead 0; **663 pages** | **663 checked paths, 9 batches, 0 failed**; every batch `broken 0, dead 0` |
| **AC5** | The stated evidence-page count equals the measured row count | **PASS** | **17 = 17 = 17 = 17**; stale figures gone | `17 selected`, `these 17 pages`, `routes to 17 dated` each x1; table rows **17**; the three stale figures all **0** |
| **AC6** | The governance log is append-only; the frozen O-F1 note is byte-unchanged | **PASS** | **deletions = 0**; **60 added**; L4149–L4190 identical | The backlog diff is **one hunk, `@@ -4191,0 +4192,60 @@`, 60 added / 0 deleted** — insert-only, exactly as ruled. The 42-line block still hashes to **`f29decc72f1ee1b31d410ead380ce55c46081e2890d004947d9e4a43e00b182d`**; base L1–L4190 and head L1–L4190 are **byte-identical**. The new entry is at L4228 and names its predecessor by **heading and line range (L4192–L4226)** |
| **AC7** | The diff is the declared file set, and exactly three lines are replaced | **PASS** | **5 A + 3 M = 8 paths; deletions 3**; no other deletion | **8 paths: 5 added, 3 modified, 0 deleted.** Cumulative **deletions = 3**, and all three are pre-existing **base** count lines (each confirmed present in the base revision) |
| **AC8** | No credential material; every broad-pattern hit is named and read | **PASS** | hits_on_copies = 3, hits_on_record = 0 | **3 and 0** — `BER-G3-FU3-EXECUTION.md:158` (`nano-USD/token = …`), `FU3-RECORD-FINAL-REVIEW-F.md:121` (Actions job id), `REVIEWPATH-FINAL-REVIEW-F.md:47` (sha256 with a 12-digit run). No other hit |
| **AC9** | A fresh checkout can retrieve the evidence; nothing on the retrieval path needs the archive | **PASS** | 4 of 4 digests; archive_dependent_targets = 0; occurrences_outside_map = 0; `map_occurrences` reported with no threshold | Fresh single-branch clone at `95351dda`; **archive present inside it: False**; **4 of 4** digests reproduce (including the derivative's `cc183e45…`); `link_targets = 12`, **`archive_dependent_targets = 0`**, **`occurrences_outside_map = 0`**, **`map_occurrences = 12`**; link rc=0 |
| **AC10** | No protected path is touched, proven with a controlled test that prints its counts | **PASS** | `pattern_len 371`; `POS 11/11`; `DOCUMENTED_NEGATIVES 0/4`; `DECLARED_PATHS 0/8`; `NEGATIVES_TOTAL 0/12`; `CONTROL_FAILURES 0` | Exactly those six numbers |
| **AC11** | The rule is present in all three placements; the log entry's wording is the settled one | **PASS on its threshold and command — O-4 carried** | PRESENT for **3 of 3** files | **PRESENT 3 of 3** after whitespace normalisation; raw byte-contiguity **False in all three**. O-4 (carried, not a defect): the Outcome's byte-identity clause drifted because the P2-1 repair rewrote the prose — see section 6 |

**Tally: 11 PASS · 0 FAIL · 0 criterion-level UNRUN.**

---

## 4. The five repairs and the superseding entry — each checked against the artifact it corrects

The five findings are Codex review **5508772323**, all with `original_commit_id = c5f71554…` (the head round 2 validated). Stage C repaired all five at `61e73442`; the Lead then ruled one word of the publication entry false, and `95351dda` supersedes it.

### 4.1 Sanitization of the fourth copy — verified by its own inventory

**Finding (P2, comment 4262995845).** Publishing the frozen record verbatim would place a username-bound WSL path, the user's home, the shell-history filename and the searched local drives into Git, against the evidence-retention rule at `docs/roadmaps/behavioral-eval-runner-backlog.md` L4021-L4025. Remedy: a **sanitized derivative**, with the original retained and digest-pinned externally.

**Verified independently, in both directions.**

| Probe on the published copy | Occurrences |
| --- | --- |
| the shell-history filename | **0** |
| the dotless shell-history filename | **0** |
| `Get-PSDrive`, `Get-Volume`, `Get-ChildItem -Path` (the drive enumeration) | **0** |
| the shell-history size result ("16 bytes") | **2** — the evidentiary substance survives |

The derivative's own section 1.1 enumerates **five** differences: two privacy sanitizations (the shell-history artefact's filename; the drive-enumeration command's host-specific root list) and three corrections of wrong claims (the arithmetic, a `Test-Path` result stated as proof of historical absence, and the copy's own self-digest footer, recomputed over the derivative). **Nothing else differs**, and the original is named with its digest and an explicit statement that it **is not retrievable from this repository**.

### 4.2 The retained review finding — digest recomputed

**Finding (P2, comment 4262995838).** The record quoted finding `4261109123` but retained no capture, so a fresh checkout could not verify it — a violation of the rule this very change introduces.

**Verified.** The publication record now carries the finding with a **locator** (the PR #765 review-comment permalink, with the plain statement that a comment can be edited or deleted and that the **digest**, not the URL, pins the text) and the **text retained verbatim**. I recomputed the digest over the retained text: **`be0e3aab224a7384c0aedb734c3d1bffa65407b836b6b0a0dfa257bcdb266ecb` — exact match.** I also checked it against the live comment: **retained text + one LF is byte-identical to the live comment body**, so the capture is faithful and not a paraphrase.

### 4.3 The $158.00 arithmetic — verified against the ledger's own assertion

**Finding (P2, comment 4262995856).** The 201-request ceiling is at most 200 judgment attempts **plus one metadata request**, and the metadata reservation carries a worst-case charge of **zero** — so the permitted path stays **$158.00**, not $158.79.

**Verified from the repository itself, twice over.**
- `tools/behavioral_eval_runner/judge/calibration_ledger.py` **L706-L712**: the `METADATA` branch raises if more than one is requested, then sets **`worst_case = 0`** — the finding's premise, confirmed in code.
- `tools/behavioral_eval_runner/cli.py` **L1115-L1117** asserts `200 * worst_case_attempt_charge_nanousd() == 158_000_000_000` — the repository's **own authority gate** for the $158 figure.
- The published copy now reads: 200 judgment attempts at the worst case `= 158,000,000,000 nano-USD = USD $158.00`, plus at most one zero-charge metadata request, worst case on the permitted 201-request path `= USD $158.00`. **That is arithmetically correct**: the per-judgment worst case is $0.79 (`40,000,000 + 750,000,000 nano-USD`), and 200 x $0.79 = $158.00 exactly.

### 4.4 The other two corrections

| Finding | What it required | Verified |
| --- | --- | --- |
| **4262995850** — do not infer historical absence from current state | the `Test-Path == False` result must be stated as absence **when searched**, with historical existence labelled unknown | The derivative's difference 4 records exactly that reframing |
| **4262995828** — preserve source hashes before claiming byte identity | retain independently recorded pre-copy source hashes, or label identity unverified | The table now gives **both sides for all four files** (source-side and committed-side digests, two per row), and the derivative is labelled rather than claimed identical. My check: **2 hashes present in every one of the four rows**, and the BER row's two values **differ** (`ea521f84…` vs `cc183e45…`) exactly as a labelled derivative requires |

### 4.5 The superseding section-13 entry

The Lead ruled that the earlier entry's word **"byte-identical"** had become false for the fourth file. The repair is a **new entry at L4228**, appended under the log's own rule at L2672–L2675:

- it names the entry it supersedes **by heading AND by line range** ("L4192–L4226"), and quotes the sentence it corrects;
- it states the correction — *"three byte-identical copies and one sanitized derivative"* — names the two sanitized identifiers, cites the retention rule at **L4021–L4025**, names the three corrected claims, and records **both the source-side and committed-side digest** of the derivative;
- it states that the original remains in the session archive with its digest and **"is not retrievable from this repository"**;
- it edits no existing byte and grants nothing (**"New authority: None"**).
- **Its link to the publication record's section 1.1 resolves**: the anchor probe returned rc=0 with `dead: 0`.

### 4.6 The three pre-existing identifiers were not altered

The derivative deliberately **keeps** the identifiers it already shares with the base revision, on the stated ground that removing them would change the copy for no privacy gain. I checked rather than accepted: the distro release (the distro-release token, raw value withheld) and the WSL references present in the derivative are **already present in tracked files at the base revision** — confirmed by search. So the retained identifiers are not new disclosures, and the sanitization was confined to what was new to Git.

---

## 5. UNRUN register, CI, and the body at this revision

| # | Unrun check | Why it did not run here | Satisfies | What would resolve it |
| --- | --- | --- | --- | --- |
| **U-1** | `scripts/tests/test_validator.py` | the sandbox denies the `chmod` this suite performs on its own temporary directory, in `%TEMP%` and with `TEMP`/`TMP`/`TMPDIR` redirected into the workspace | L185–L188 **(a)**: run by a named CI job at this exact head — `validate-skills` run **38454963608**, success, and its steps include *Run validator self-tests* | A host without the sandbox limit, or acceptance of the CI evidence |
| **U-2** | `scripts/tests/test_markdown_links.py` | same sandbox temp-directory denial | **(a)**: same job, the *Run Markdown link-checker self-tests* step success | As U-1 |
| **U-3** | `gate-guard` as the **actual bash step** | `bash` is denied in this session (`Bash/E_ACCESSDENIED`), the limitation the lane brief names for this host | **(a)**: the `gate-guard` **check run is success** at this exact head, **plus** my own evaluator of the extracted 371-character `gate_pattern` over all 8 changed paths and 11 positive controls (AC10) | A host where `bash` runs, or acceptance of the check run as the authoritative object |

**UNRUN is never PASS.** None of the three is absorbed into the eleven verdicts; **no criterion is UNRUN** — every one of AC1–AC11 was measured at this head by me.

**CI and the repository's own checks at the head.** Runs **38454963608** (#2088) and **38454941592** (#2087) both succeeded at `head_sha = 95351dda…`. Check runs: `changes`, `gate-guard`, `validate-skills` **success**; `tools-tests-linux`, `tools-tests-windows`, `windows-offline-checks` **skipped by path condition — recorded as skipped, never as passed**. Re-run by me: `python -P scripts/validate-skills.py` → rc=0, `OK: 205 skill(s) valid, 0 warning(s)`; `python -P scripts/check_dco.py --range origin/main..HEAD` → rc=0 with **five commits all SIGNED** and a line beginning **`OK: 5 commit(s) checked, all signed off or exempt.`**; `python -P scripts/ci/check_pr_body_skills.py --body-file <body> --author ModernNomad-98` → rc=0, `PR body bound fields: OK`.

**The body as a bound field.** Three whole-line sentinel pairs, no duplicates, **zero** non-sentinel substring occurrences; security `[x] No`; bound-field first-16 **`9114b83bcfbd2cdb`**; **22 data rows and 22 `Row source` records** — A(2), B re-audit(2), C(3), D(2), D round 3(2), E round 1(2), E round 2(2), F(3), plus **5 absence rows**. The Stage E rows present are round 1 and round 2; both are bound to superseded heads, which is why section 7 authors round 3.

---

## 6. Defects and observations

### 6.1 Defects

**None found in the implementation, the diff, the frozen material, the five repairs or the superseding entry.** Every criterion measured PASS at this head.

### 6.2 Observations — carried, not repaired, on the Lead's ruling

| # | Severity | Observation | My independent measurement and assessment |
| --- | --- | --- | --- |
| **OBS-1** | **LOW — carried** | The retained finding text's length is labelled **"913 characters"**. | I measured the retained text three ways: **911 Unicode code points**, **918 UTF-8 bytes**, **913 UTF-16 code units**. The label matches the **UTF-16 code-unit** count, so it is a **different counting convention, not a false statement** — and the digest that actually protects the text (**`be0e3aab…`**) recomputes exactly over the 911 code points. **I agree with the ruling to carry it**: correcting the label would change the retained bytes and invalidate the digest that does the protecting — the label is descriptive, the digest is the mechanism. Recorded, not fixed |
| **O-4** | **LOW — carried (criterion-text drift)** | AC11's Outcome claims the two prose placements carry the plan's §7.4 block byte-for-byte. | Still **not** true, for the same reason as round 2: the P2-1 repair legitimately rewrote the enforcement paragraph in both placements, while the plan keeps the pre-repair text. AC11's **operative threshold and command** (PRESENT 3 of 3, normalised) are met, so PASS stands. This is drift in the *criterion's description*, caused by a **mandated** repair — **not a defect, and not a reason to re-edit**, which is what the Lead ruled and what the evidence supports |
| **O-6** | **MEDIUM — carried residual** | The skills `Row source` records for Stages A–F cite session-workspace artifacts that a fresh checkout cannot retrieve. | Unchanged and still handled by the change's own rule's second branch (digest, locator, plain non-retrievability). The judgement I continue to decline silently: those text files **could** have been published, but that is outside the audited 8-path scope — a **scope decision for the owner or Stage F**, not for Stage E. My own rows carry the same shape and say so in their `limits=` field |

### 6.3 One thing this round adds to the record, because it explains the whole re-validation cycle

**The bound-field hash is not a body checksum.** `20,748 of the body's 58,462 bytes (35.5%)` lie outside the three bound fields, so the hash can be **identical while the body changes** — which is exactly what happened between the previous revision and this one. Anyone reading a bound-field hash as evidence that the body is unchanged would be wrong, and this record states the measurement rather than the assumption.

---

## 7. Skills this stage used — Stage E ROUND-3 rows, copy-ready for the publisher

**Author:** `of1-stage-e`, Stage E, **round 3**. **Target:** `95351dda27210f4b5707aa067cd138bf37710bd5`. **Why new rows:** `docs/delivery-workflow.md` L693–L694 — *"A D/E/F row for an older head or round cannot stand for a later one."* The Stage E rows now in the body are bound to `bd210954` and `c5f71554`. Per L696–L699 the older row **strings** stay unchanged and their source records are marked historical or superseded. **I did not insert these rows** — I am the validator, not the publisher.

**Exact captured row text** — the two lines inside the fence below, joined by LF plus one trailing LF, UTF-8, **1,547 bytes**:

```text
| [acceptance-criteria-reviewer](.claude/skills/acceptance-criteria-reviewer/SKILL.md) | Stage E round 3 / `of1-stage-e` | Re-applied its three-part test a third time at the final head, after five further Codex P2 findings and a superseding log entry moved it twice: all eleven criteria were re-derived rather than carried, and each of the five repairs was checked against the artifact it corrects - the sanitized derivative read against the frozen copy's own byte inventory, the retained finding text read against the live review comment, and the $158.00 arithmetic read against the ledger's own assertion at `cli.py` L1115-L1117. | The eleven-row verdict table and the UNRUN register in `VALIDATE-E-round3.md` sections 3 and 5 |
| [skill-usage-ledger](.claude/skills/skill-usage-ledger/SKILL.md) | Stage E round 3 / `of1-stage-e` | Used its workflow again for this round's own record: both skill names were re-resolved against `tools/skills-manifest.json` at the final head and both digests recomputed from `.claude/skills/<name>/SKILL.md` with CRLF-to-LF normalisation, so the manifest is proven current rather than assumed. Its `incomplete` field names this round's unrun checks instead of asserting completeness. | `acceptance-criteria-reviewer` = `c6e5d5649bf89658036cf38abba9c626701220e7b00831c2d843ceff94d81021`, `skill-usage-ledger` = `6a27b5c8e690b605d7dca4b0e4c2ff1d67dfa6ac6c18469d5657b4ff093339a4`, both recomputed and matching; `tools/skills-manifest.json` sha256 `9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832` |
```

**`sha256` of that exact captured row text:**

`cb7bca1674b18713aebb21858174defc2d3e6b679eafb1d5c606d8a4ac0d414b`

**`Row source` records for the two rows** — excluded from the digest above, so there is no self-reference:

```text
<!-- Row source: agent=of1-stage-e; stage=E; round=3; row=SDE3-1; target=95351dda27210f4b5707aa067cd138bf37710bd5 (this pull request's candidate head); source=_resume-2026-10-09/evidence/workspace-citation-durability-2026-10-13/VALIDATE-E-round3.md section 7 fenced block row 1 (the exact bytes hashed); binding=sha256 cb7bca1674b18713aebb21858174defc2d3e6b679eafb1d5c606d8a4ac0d414b over the fenced block's UTF-8 bytes including the final newline (the two Stage E round-3 row lines joined by LF plus one trailing LF, 1,547 bytes); manifest=tools/skills-manifest.json sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832; limits=the row source is a session-workspace artifact and is not retrievable from this repository - see section 6 observation O-6. -->
<!-- Row source: agent=of1-stage-e; stage=E; round=3; row=SDE3-2; target=95351dda27210f4b5707aa067cd138bf37710bd5 (this pull request's candidate head); source=_resume-2026-10-09/evidence/workspace-citation-durability-2026-10-13/VALIDATE-E-round3.md section 7 fenced block row 2 (the exact bytes hashed); binding=sha256 cb7bca1674b18713aebb21858174defc2d3e6b679eafb1d5c606d8a4ac0d414b over the fenced block's UTF-8 bytes including the final newline (the two Stage E round-3 row lines joined by LF plus one trailing LF, 1,547 bytes); manifest=tools/skills-manifest.json sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832; limits=the row source is a session-workspace artifact and is not retrievable from this repository - see section 6 observation O-6. -->
```

**Manifest provenance.** Both names resolve in `tools/skills-manifest.json` — itself `sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832` — and both digests were recomputed this round from `.claude/skills/<name>/SKILL.md` with CRLF→LF normalisation: `acceptance-criteria-reviewer` = `c6e5d5649bf89658036cf38abba9c626701220e7b00831c2d843ceff94d81021`, `skill-usage-ledger` = `6a27b5c8e690b605d7dca4b0e4c2ff1d67dfa6ac6c18469d5657b4ff093339a4` — both **match**.
**No preclaiming:** the row text contains neither its own digest nor any bound-field hash (checked against `9114b83b`, `b1b88d12`, `95351dda`, `f29decc7`, `cc183e45`, `be0e3aab` — all absent), per L720–L721.
**Sequencing note for the publisher.** Insert these rows **together with Stage F's re-authored rows in ONE edit, before Stage F computes its bound-field hash**, so the body is stable when the verdict binds it.

---

## 8. Boundary — what this round did not do

- **No repository write.** No commit, branch, push, tag or merge.
- **No pull-request write.** No body edit, comment, review, label or reaction. The rows in section 7 are **authored and handed over**.
- **No repair.** OBS-1, O-4 and O-6 are recorded with their measurements and left as found. In particular I did **not** correct the length label (which would have invalidated the digest that protects the text), did **not** edit the plan's §7.4, and did **not** touch the derivative, the retained capture or the superseding entry.
- **No adjudication** of the scope question in O-6.
- **No touch** of `clone-pq1`, `clone-pq2`, the legacy checkout, any `wt-*` worktree, the paused VirtualBox VM or the WSL distro.
- **No subagents, no delegation.**
- **Rounds 1 and 2 are preserved, not overwritten** — `VALIDATE-E.md` and `VALIDATE-E-round2.md` stay on disk bound to their own heads.

---

## 9. Timing — *Workspace-citation durability — Stage E ROUND 3*

| | |
| --- | --- |
| **Item** | *Workspace-citation durability — Stage E ROUND 3 — validate at head 95351dda* (shared task `task-26`) |
| **Start** | **`2026-10-13T12:32:59-07:00`** (America/Los_Angeles) — the modification stamp of the first file this round wrote (its byte-exact capture of the pull-request body), the earliest start I can **evidence**. No start stamp was issued to me; I have not invented one. |
| **Finish** | **`2026-10-13T12:37:32-07:00`** (America/Los_Angeles) — sampled in the same program run that performed this file's write |
| **Measured wall time** | **`4 minutes 33 seconds (273 seconds)`** — evidenced start to final write |
| **Active time** | **not separately instrumented.** Wall time is the honest measurement, so the ETA comparison is **IMPERFECT** and is labelled as such rather than presented as an active-time split. |

---

<!-- sha256 footer: the hash below covers this file's bytes with the digest line's value replaced by the
     literal placeholder {{SHA256}}, so the digest is stable and independently reproducible.
     Verify by replacing the 64 hex characters on the line beginning "sha256:" with {{SHA256}}, then
     hashing the UTF-8 bytes INCLUDING the final newline. Line endings are LF only. -->
sha256: a199e8318bfa5d8cdbd189195f0e3289e557b73498de4e054934623db5ff63d4
