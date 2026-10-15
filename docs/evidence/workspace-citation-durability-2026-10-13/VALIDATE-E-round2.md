# WORKSPACE-CITATION DURABILITY — STAGE E ROUND 2: VALIDATION AT THE CORRECTED HEAD

**Item:** "Workspace-citation durability — Stage E ROUND 2 at the corrected head" (shared task `task-17`) — in plain words, *the second run of the validation stage for this change, required because three verified review findings moved the head after round 1 finished.*

**Agent:** `of1-stage-e` — the Stage E holder, and a **different holder from** Stage A (`wcd-stage-a`), Stage B (`wcd-stage-b`), Stage C (`wcd-stage-c`) and Stage D (`of1-stage-d`). **No subagents. Nothing was delegated.**

**Skill dogfooded:** `acceptance-criteria-reviewer` — in plain words, *the Aegis skill that judges whether a criterion names an observable outcome, a pass-or-fail threshold and the evidence that will prove it, and returns one verdict per criterion.* Secondary: `skill-usage-ledger` — in plain words, *the Aegis skill that produces the record of which skills a task used, bound to the skills manifest* — used for this round's rows in section 7. Both were read in full from `.claude/skills/` at the head under test.

**Reading key — every label in this record, in plain words (the owner's permanent reporting rule).**
- `P2-1` — *the verified finding that the rule text claimed the link checker enforces something it cannot.*
- `P2-2` — *the verified finding that the archive-path inventory heading promised more coverage than its table delivered.*
- `P2-3` — *the verified finding that the index header gave a newly added row impossible verification provenance.*
- `O-F1` — *observation F1 from the FU-3 record lane, whose frozen note this change makes retrievable.*
- `FU-3` — *the Behavioral Eval Runner provider-usage reconciliation attempt whose record lane merged as pull request #764.*
- `gate_pattern` — *the regular expression read from the skills-validation workflow that decides which changed paths are protected and force a manual merge.*
- `DCO` — *the Developer Certificate of Origin sign-off trailer every commit in the range must carry.*
- `bound fields` — *the three pull-request-body fields the process acts on: the reconciliation witness, the Aegis skills table and the security answer.*
- `Row source` — *the provenance record inside the skills bound field binding each published row to its authoring agent, stage, round, target and source.*
- `UNRUN` — *a check that did not run. Unrun coverage is never a pass.*

---

## 1. What was validated, and at exactly which revision

| | |
| --- | --- |
| **Repository** | `ModernNomad-98/Project-Aegis` |
| **Pinned base** | `dbe2ee28559fef88950b2d8822cf72d3e595ba86` — in plain words, *the tip of main this change targets.* |
| **Head validated (40 characters)** | `c5f715544da64a43e0c900d33b298bce0957d504` — in plain words, *the third commit on the branch, which enumerates every index row the 2026-09-23 sweep does not reach.* The branch is **three commits** on the pinned base: `bd210954` (round 1), `b591e0d9` (round 2), `c5f71554` (round 3). |
| **Pull request** | #766, `docs/workspace-citation-durability-20261013` |
| **Body revision** | **stored body 45,014 bytes**, `sha256 4cc5171f75009e6c5c50caf96261ca7ac57bafc86531a5b334b96111bb733cf1`, 0 CRLF |
| **Bound-field hash** | first-16 **`eeb359259b517578`**, recomputed here (full `sha256 eeb359259b51757822f28ac313d69ab17fff41ab9ce03bfc282337b344adba95`) — matches the value supplied to this round exactly |
| **Byte-count convention, named** | Every body figure in this record is the **stored body**: the JSON `.body` value written back byte-for-byte, 45,014 bytes, 0 CRLF. A `gh … --jq .body` redirect appends one trailing byte, which is why the same revision can otherwise read 45,015. **The hash is convention-independent**, because the protocol collapses every whitespace run; the hash, not the byte count, is what binds. |
| **Superseded bindings** | Round 1 of this stage was bound to head `bd210954` and body `6f36dda81cf9f3cd`. The head has moved twice since, so **that disposition is void** and this record replaces it. The body names `f879e2e7f77d73dc` and `6f36dda81cf9f3cd` as not standing. |
| **My own clones** | `_wcd-e-clone` (working clone, HTTPS) and `_wcd-e-scratch/fresh-wcd-r2` (a single-branch clone of the candidate branch for AC9, with the session archive **verified absent** inside it). No other stage's clone was used. |
| **Writes made by this round** | exactly **one file** (this record) plus that throwaway clone. **No repository write, no commit, no push, no body edit, no comment, no label, no merge.** |

**Verifier discipline.** Both verifiers were validated before use, as this lane requires: the **footer verifier** reproduced three known-good seals (`250cc3e8…`, `73254f26…`, `c2d106af…`) 3 of 3; the **body-digest verifier** was, in round 1, caught disagreeing with `REVIEWPATH-FINAL-REVIEW-F.md`'s body digest until I adopted that file's own stated method — this round it was reused only after reproducing the same known-good value again. **No seal was accused without a validated verifier.**

---

## 2. Disposition

> ## **SD-E: INCOMPLETE — UNRUN LISTED**

**Written with its prefix**, per `docs/delivery-workflow.md` L56–L61, in the workflow's own vocabulary for `SD-E` and no other token.

**All eleven acceptance criteria PASS at this head**, each re-derived from the repository, the live pull request or the archive — never inherited from round 1, whose head has been superseded.

**Why this token and not PASS.** L193: *"UNRUN is never PASS."* Three session-level checks genuinely could not run in this session (section 5): two repository self-test suites and the `gate-guard` bash step. **Why it is affirmative:** per L185–L188 the disposition is affirmative when every unrun check is either (a) run by a named CI job at that exact head, evidenced, or (b) listed with what would resolve it — and all three satisfy (a) at head `c5f71554`. Per L190–L193, **SD-F must accept this list as part of its review and SD-G's receipt must record it.**

**Why not FAIL.** Nothing failed. The one finding that touches a criterion (observation O-4, the plan's §7.4 byte-identity clause) is a consequence of a **mandated repair**, not a defect in the implementation, and it is recorded rather than buried.

**Bound to what.** Head `c5f71554…` **and** body `4cc5171f…` / `eeb359259b517578`. **The body will move once more** — it carries Stage E's round-1 rows, which are bound to `bd210954` and cannot stand for this head (L693), so section 7 authors this round's rows for the publisher. When they land the body binding moves again; the head, the diff and the eleven criteria do not.

---

## 3. The eleven-criterion verdict table

| # | Criterion | Verdict | Threshold | Observed |
| --- | --- | --- | --- | --- |
| **AC1** | The four cited records are published byte-identically | **PASS** | **4 of 4 IDENTICAL** | From the **committed blobs** at `c5f71554`, each copy's size and digest equal its archive source's: `ea521f84…` (25,606 B), `c0b0c548…` (30,777 B), `d2ed1cfb…` (25,454 B), `f367d36e…` (21,023 B). **The repairs did not touch the frozen copies** |
| **AC2** | The published copies' own integrity claims still hold | **PASS** | **3 of 3 footers OK** + body digest `81884e0d…` | `f5a6b9ca…`, `8f554598…`, `059822aa…` all recompute; `REVIEWPATH-FINAL-REVIEW-F.md`'s body digest recomputes to `81884e0d49cb117c7f7884350ce23adcfac6788891c0a9bc8828dc19461abcc8` over 20,338 bytes / 102 lines under that file's own stated method |
| **AC3** | Every link the change adds resolves, including heading fragments | **PASS** | exit 0, broken 0, dead 0, **anchors >= 4** | `{"files": 4, "checked": 198, "anchors": 32, "broken": 0, "dead": 0, "skipped": 0}`, rc=0 — **32 anchors** |
| **AC4** | The corpus-wide link check CI runs is still green | **PASS** | every batch exits 0; broken 0; dead 0; **page count 663** | **checked paths: 663**, **9 batches, 0 failed**, every batch `broken 0, dead 0` |
| **AC5** | The stated evidence-page count equals the measured row count, at every site | **PASS** | **17 = 17 = 17 = 17**; stale figures gone; **the header's provenance sentences TRUE** | `17 selected` x1, `these 17 pages` x1, `routes to 17 dated` x1, table rows **17**; the three stale figures all **0**. **The header's enumeration was verified against git history, not accepted**: fifteen rows were introduced 2026-09-23 by commit `9817037b` (the sweep), and **exactly two** post-date it — the SCIF row (2026-10-11, commit `503c3b30`) and the FU-3 publication row (2026-10-13, commit `bd210954`). The header names exactly those two and the same commits. **True** |
| **AC6** | The governance log is append-only; the frozen O-F1 note is byte-unchanged | **PASS** | **deletions = 0**; L4149–L4190 identical at base and head | backlog **35 added / 0 deleted**; the 42-line block still hashes to **`f29decc72f1ee1b31d410ead380ce55c46081e2890d004947d9e4a43e00b182d`**; base L1–L4190 and head L1–L4190 are **byte-identical** |
| **AC7** | The diff is exactly the declared file set, and exactly three lines are replaced | **PASS**, with both deletion tests reproduced | **5 A + 3 M = 8 paths; total deletions 3**; no deletion but the count figures | **8 paths: 5 added, 3 modified, 0 deleted.** Cumulative **deletions = 3**, and all three are pre-existing **base** count lines. Separately, the **round-3** deletions (3, from `c5f71554`) are **not in the base at all** — they are round-2 text replaced in round 3 — which is the distinction Stage D drew |
| **AC8** | No credential material; every broad-pattern hit is named and read | **PASS** | **hits_on_copies = 3**, **hits_on_record = 0**, on the three named lines | **3 and 0.** The hits are `BER-G3-FU3-EXECUTION.md:155` (`nano-USD/token = …`), `FU3-RECORD-FINAL-REVIEW-F.md:121` (Actions job id `115364466965`) and `REVIEWPATH-FINAL-REVIEW-F.md:47` (a sha256 with a 12-digit run). No other hit |
| **AC9** | A fresh checkout can retrieve the evidence; nothing on the retrieval path needs the archive | **PASS** | **4 of 4 digests; 3 of 3 anchors; archive_dependent_targets = 0; occurrences_outside_map = 0**; `map_occurrences` reported with no threshold | Fresh single-branch clone HEAD = `c5f71554`; **archive present inside it: False**; **4 of 4** digests reproduce; `link_targets = 9`, **`archive_dependent_targets = 0`**, **`occurrences_outside_map = 0`**, **`map_occurrences = 10`**; link checker over the record and the log rc=0 |
| **AC10** | No protected path is touched, proven with a controlled test that prints its own counts | **PASS** | `pattern_len = 371`, `POS = 11 matched = 11`, `DOCUMENTED_NEGATIVES = 4 matched = 0`, `DECLARED_PATHS = 8 matched = 0`, `NEGATIVES_TOTAL = 12 matched = 0`, `CONTROL_FAILURES = 0` | Exactly those six numbers. Independently, the extracted pattern returns `nomatch` on **all 8** changed paths |
| **AC11** | The rule is present in all three placements, and the log entry's wording is the settled one | **PASS on its threshold and command — with observation O-4** | the command prints **PRESENT for 3 of 3 files** | **PRESENT 3 of 3** after whitespace normalisation; raw byte-contiguity is **False in all three**, so the normalisation is genuinely required. The two prose placements are **byte-identical to each other** (1,360 bytes each) — one rule, not two paraphrases — and the log entry states the rule in its bullet voice *without* the overstatement P2-1 removed. **O-4:** the criterion's Outcome also claims the placements carry the plan's §7.4 block byte-for-byte; that sub-claim is **no longer true**, because the mandated P2-1 repair rewrote the enforcement paragraph in both placements while the plan still carries the pre-repair text. See section 6 |

**Tally: 11 PASS · 0 FAIL · 0 criterion-level UNRUN.** Three session-level UNRUN checks are carried in section 5 and are part of the disposition.

---

## 4. The three verified P2 findings, and how each repair was checked

The findings are Codex review comments, all with `original_commit_id = bd210954…` — the head round 1 validated. Each repair moved the head, which is why this round exists.

### 4.1 P2-1 — the rule text overstated what the link checker enforces

**Finding (comment 4262291570, `docs/evidence/README.md` L65).** The checker validates only Markdown links authors already supplied, so a record can cite a path as plain text — or omit its evidence entirely — and the job stays green. That overstates the enforcement behind the claimed prevention.

**I verified the mechanism myself rather than accepting the finding.** `scripts/ci/check-markdown-links.py` compiles `LINK = re.compile(r"\[([^\]\n]*)\]\(\s*(<[^<>\n]*>|[^()\n]*?)\s*\)")` at L32 and scans **per line** with `LINK.finditer` at L322. A line containing no `](` is never examined. So the checker tests the **resolution of links an author wrote**; it cannot require a citation to exist. **The finding is correct.**

**Repair verified at the head.** The old clause — *"which goes red when a cited path or heading stops resolving"* — is **gone** (byte search returns False). The replacement is literally true:

```text
the "Run Markdown link checker over the repository's own pages" step of validate-skills validates the
links a record already contains - it goes red when a written link stops resolving - and it does
not require a record to contain a durable citation at all. A record can cite an out-of-tree path as
plain text, or omit its evidence entirely, and that step stays green. Supplying the citation this rule
requires is therefore a documentation obligation that nothing machine-checks; the digest half is
checked by nothing either, and a record that relies on it says so.
```

That is exactly the remedy Codex offered — *"narrow this text to say the job validates only existing links"* — and it matches the code. **The log entry's own rule bullet is also accurate**: it says a path *"cited as a Markdown link so the repository's own link checker proves it resolves"*, which claims resolution of a written link, not enforcement of its existence. No placement still carries the overstatement.

### 4.2 P2-2 — the inventory heading promised more than the census delivered

**Finding (comment 4262291580, publication `README.md` L77).** The heading promised every archive path a tracked record cites, while the newly published records themselves cite further archive locators the nine-row table omits — for example the two source-tar paths in `BER-G3-FU3-EXECUTION.md:113-114` and a row source in `FU3-RECORD-FINAL-REVIEW-F.md:222`.

**Repair verified.** The heading is now scoped: `## 3. Every archive path the pre-change records cite, and its disposition`. The census states *"Ten citation occurrences across the **four pre-change tracked records** … name **nine distinct** archive paths. Four are published here; **five are owed**"* — and the table has exactly nine rows, four PUBLISHED and five OWED. A scope paragraph follows, added *"because the heading promises it"*: the census was taken over the tracked tree **at the base revision, before this change**; the four published copies are frozen re-publications that *"carry their own out-of-tree references internally"*; **those internal references "are **not** counted above and are **not** repaired by this change"**, because rewriting them would falsify the copies' own integrity claims and widening the census would breach the audited scope.

**I checked the scope statement's two specific line claims and they are exact:** `BER-G3-FU3-EXECUTION.md` L113 and L114 really are the two `ber-source-*.tar` paths, and `FU3-RECORD-FINAL-REVIEW-F.md` L222 really is a `Row source` locator. My own count of the archive string inside the four copies is **17 occurrences over 14 lines**, a different measure from Stage D's 16 — but the statement says *"for example"* and claims no total, so **no count is asserted that I could falsify**, and the heading's promise is now true of the set it names.

### 4.3 P2-3 — the index header gave a new row impossible provenance

**Finding (comment 4262291601, `docs/evidence/README.md` L46).** The header said every boundary below was checked 2026-09-23 against `e2145b1`, while the newly added row describes a 2026-10-13 page — impossible provenance.

**Repair verified, and the harder question asked.** The header now adds: *"This index was created that day and fifteen of its seventeen rows date from that sweep. **Exactly two rows post-date it and are therefore not covered by it:**"* — the SCIF row (2026-10-11, commit `503c3b30`) and the FU-3 publication row (2026-10-13, against base `dbe2ee28`), noting that a page cannot cite its own commit.

**I did not accept that enumeration — I reproduced it across all seventeen rows** using `git log -S` on each row's own text: **fifteen rows were introduced 2026-09-23 by commit `9817037b`**, and **exactly two** post-date the sweep — row 16 (2026-10-11, `503c3b30`) and row 17 (2026-10-13, `bd210954`). The header names those two and those commits. **The enumeration is true.** This is also why the first repair (annotating only this change's own row) was insufficient: the SCIF row was the second post-sweep row and had to be named.

### 4.4 The repairs were confined to the prose — the frozen material did not move

| Check | Result |
| --- | --- |
| The four published copies | **still copy-identical to their archive sources**; the same four digests as round 1 (`ea521f84`, `c0b0c548`, `d2ed1cfb`, `f367d36e`) |
| Their internal integrity claims | 3 of 3 footers and the body digest still recompute (AC2) |
| The frozen O-F1 note | still `f29decc72f1ee1b31d410ead380ce55c46081e2890d004947d9e4a43e00b182d`; the log diff is **35 added / 0 deleted** |
| The declared file set | still exactly 8 paths (5 A + 3 M); **no new file**, so no archive dump |
| Cumulative deletions | still exactly **3**, all count lines |

---

## 5. UNRUN register — every check that did not run, with what would resolve it

| # | Unrun check | Why it did not run here | Satisfies | What would resolve it |
| --- | --- | --- | --- | --- |
| **U-1** | `scripts/tests/test_validator.py` | The sandbox denies the `chmod` this suite performs on its own temporary directory, in `%TEMP%` and with `TEMP`/`TMP`/`TMPDIR` redirected into this workspace | L185–L188 **(a)**: run by a named CI job at this exact head — `validate-skills` run 38447153822, job 115468416716, **step 11 success** | A host without the sandbox limit, or acceptance of the CI evidence |
| **U-2** | `scripts/tests/test_markdown_links.py` | Same sandbox temp-directory denial | **(a)**: **same job, step 14 success** | As U-1 |
| **U-3** | `gate-guard` as the **actual bash step** | `bash` is denied in this session (`Bash/E_ACCESSDENIED`), the limitation the lane brief names for this host | **(a)**: the `gate-guard` **check run is success** at this exact head, **plus** my own evaluator of the extracted 371-character `gate_pattern` over all 8 changed paths and 11 positive controls (AC10) | A host where `bash` runs, or acceptance of the check run as the authoritative object |

**UNRUN is never PASS.** None of the three is absorbed into the eleven verdicts. **No criterion is UNRUN** — every one of AC1–AC11 was measured at this head by me.

**CI at the head, read not assumed.** Run **38447153822** (`validate-skills`, run #2082): `head_sha = c5f715544da64a43e0c900d33b298bce0957d504`, `status: completed`, `conclusion: success`. Job 115468416716 steps **10, 11, 12, 14, 15, 19 and 20 all success**. Check runs at the head: `changes`, `gate-guard`, `validate-skills` **success**; `tools-tests-linux`, `tools-tests-windows`, `windows-offline-checks` **skipped by path condition — recorded as skipped, never as passed**.

**Repository checks re-run by me at the head.** `python -P scripts/validate-skills.py` → rc=0, `OK: 205 skill(s) valid, 0 warning(s)`. `python -P scripts/check_dco.py --range origin/main..HEAD` → rc=0, three commits all `SIGNED`, line begins **`OK: 3 commit(s) checked, all signed off or exempt.`**. `python -P scripts/ci/check_pr_body_skills.py --body-file <body> --author ModernNomad-98` → rc=0, `PR body bound fields: OK`.

**The body as a bound field.** Three whole-line sentinel pairs, no duplicates, **zero** non-sentinel substring occurrences; security `[x] No`; bound-field hash first-16 **`eeb359259b517578`**; **16 data rows and 16 `Row source` records** — A(2), B re-audit(2), C(3), D(2), E round 1(2), plus **5 explicit absence rows** for the A–E shapes where no matching skill exists. **Stage E's rows in the body are round-1 rows bound to `bd210954`**, which is why section 7 authors this round's replacement.

---

## 6. Defects and observations

### 6.1 Defects

**None found in the implementation, the diff, the frozen material or the three repairs.** Every criterion measured PASS at this head; both plan-command defects from round 1 (SDC-1's `$P`/`$p` collision, SDC-2's `^-[^-]` counter) remain defects of the **plan's** commands and were already reported in round 1's record — they do not recur here because this round used corrected commands and reproduced both behaviours.

### 6.2 Observations

| # | Severity | Observation | My assessment |
| --- | --- | --- | --- |
| **O-4** | **LOW (criterion drift — a consequence of a mandated repair, not a defect)** | **AC11's Outcome clause about byte-identity no longer holds.** AC11's Outcome says *"the two prose placements carry the §7.4 block byte-for-byte"*. At this head they do **not**: both placements were rewritten by P2-1's repair and are now 1,360 bytes each, identical to each other, while the plan's §7.4 block is 1,046 bytes and still contains the **pre-repair** enforcement paragraph. | **PASS stands.** AC11's stated **threshold and command** — PRESENT for 3 of 3 under whitespace normalisation — is met, and it is the criterion's operative test. The byte-identity clause described text that a later **verified** finding required to be corrected; a criterion cannot demand reproduction of wording that was false. The substance is **stronger** at this head than the plan text it was written against: one rule, stated identically in both prose placements, and the log entry's version accurate. Recorded so Stage F does not read the Outcome literally and conclude the change drifted. |
| **O-5** | **INFO** | **Stage D's round-3 artifact, and which revision I read.** `AUDIT-D-round3.md` — **28,776 bytes, raw `sha256 1f67140863d84783fe561f9f08d1707ebb17c56a3ec9ac3ff8f9bdba30acb8d6`**, agent `of1-stage-d`, audited head `c5f71554`, naming the rounds it supersedes. I read **this** revision. Its count of 16 internal locators in the frozen copies differs from my own measure (17 occurrences over 14 lines) — a difference of **measure, not of fact**, and no criterion or claim in the artifact depends on the figure, as P2-2's repaired statement says *"for example"* rather than asserting a total. | No action needed; recorded so the two figures are not later mistaken for a contradiction. |
| **O-6** | **MEDIUM (named residual, carried from round 1 — still open)** | **The skills `Row source` records for Stages A–E cite session-workspace artifacts** (`PLAN.md`, `AUDIT-B-rev2.md`, `AUDIT-D`, `VALIDATE-E` under `_resume-2026-10-09/`), which a fresh checkout cannot retrieve. | **Unchanged from round 1 and still correctly handled**: this change's own rule's second branch — digest, locator, and a plain statement that the artifact is not retrievable — is satisfied, and the non-retrievability is named inside the skills bound field. The judgement I still decline to make silently: those text files **could** have been published, but publishing them is outside the audited 8-path scope, so it is a **scope decision for the owner or Stage F**, not something Stage E may decide or repair. **My own rows in section 7 carry the same shape and say so in their `limits=` field.** |

**Every label above carries its plain-English description in the same item**, per the owner's permanent reporting rule.

---

## 7. Skills this stage used — Stage E ROUND-2 rows, copy-ready for the publisher

**Author:** `of1-stage-e`, Stage E, **round 2**. **Target:** `c5f715544da64a43e0c900d33b298bce0957d504`. **Why new rows and not the round-1 text:** `docs/delivery-workflow.md` L693–L694 — *"A D/E/F row for an older head or round cannot stand for a later one."* The two Stage E rows now in the body are bound to `bd210954`; this round ran at `c5f71554`. Per L696–L699 the older row **strings** stay unchanged and their source records are marked historical or superseded. **I did not insert these rows** — I am the validator, not the publisher.

**Exact captured row text** — the two lines inside the fence below, joined by LF plus one trailing LF, UTF-8, **1,760 bytes**:

```text
| [acceptance-criteria-reviewer](.claude/skills/acceptance-criteria-reviewer/SKILL.md) | Stage E round 2 / `of1-stage-e` | Re-applied its three-part test at the corrected head after three verified Codex P2 findings moved it: all eleven criteria were re-derived from scratch rather than carried forward, and the three repairs were each checked against the mechanism they correct - the narrowed enforcement sentence read against the link checker's own LINK/`finditer` behaviour, the census scope statement read against an independent count of the frozen copies' internal locators, and the index provenance sentence read against a git-history enumeration of all seventeen rows. Its discipline is what caught that the plan's section 7.4 block is no longer byte-present in either prose placement, because the P2-1 repair legitimately rewrote it. | The eleven-row verdict table and the UNRUN register in `VALIDATE-E-round2.md` sections 3 and 5 |
| [skill-usage-ledger](.claude/skills/skill-usage-ledger/SKILL.md) | Stage E round 2 / `of1-stage-e` | Used its workflow again for this round's own record: both skill names were re-resolved against `tools/skills-manifest.json` at the corrected head and both digests recomputed from `.claude/skills/<name>/SKILL.md` with CRLF-to-LF normalisation, so the manifest is proven current rather than assumed. Its `incomplete` field names this round's unrun checks instead of asserting completeness. | `acceptance-criteria-reviewer` = `c6e5d5649bf89658036cf38abba9c626701220e7b00831c2d843ceff94d81021`, `skill-usage-ledger` = `6a27b5c8e690b605d7dca4b0e4c2ff1d67dfa6ac6c18469d5657b4ff093339a4`, both recomputed and matching; `tools/skills-manifest.json` sha256 `9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832` |
```

**`sha256` of that exact captured row text:**

`1ff5e868c39201a9ac6884744f7dc8a9191d8786caf0571033dd3f4260a87206`

**`Row source` records for the two rows** — excluded from the digest above, so there is no self-reference:

```text
<!-- Row source: agent=of1-stage-e; stage=E; round=2; row=SDE2-1; target=c5f715544da64a43e0c900d33b298bce0957d504 (this pull request's candidate head); source=_resume-2026-10-09/evidence/workspace-citation-durability-2026-10-13/VALIDATE-E-round2.md section 7 fenced block row 1 (the exact bytes hashed); binding=sha256 1ff5e868c39201a9ac6884744f7dc8a9191d8786caf0571033dd3f4260a87206 over the fenced block's UTF-8 bytes including the final newline (the two Stage E round-2 row lines joined by LF plus one trailing LF, 1,760 bytes); manifest=tools/skills-manifest.json sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832; limits=the row source is a session-workspace artifact and is not retrievable from this repository - see section 6 observation O-6. -->
<!-- Row source: agent=of1-stage-e; stage=E; round=2; row=SDE2-2; target=c5f715544da64a43e0c900d33b298bce0957d504 (this pull request's candidate head); source=_resume-2026-10-09/evidence/workspace-citation-durability-2026-10-13/VALIDATE-E-round2.md section 7 fenced block row 2 (the exact bytes hashed); binding=sha256 1ff5e868c39201a9ac6884744f7dc8a9191d8786caf0571033dd3f4260a87206 over the fenced block's UTF-8 bytes including the final newline (the two Stage E round-2 row lines joined by LF plus one trailing LF, 1,760 bytes); manifest=tools/skills-manifest.json sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832; limits=the row source is a session-workspace artifact and is not retrievable from this repository - see section 6 observation O-6. -->
```

**Manifest provenance, recomputable by any reader.** Both names resolve in `tools/skills-manifest.json` — itself `sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832` — and both digests were recomputed this round from `.claude/skills/<name>/SKILL.md` with CRLF→LF normalisation: `acceptance-criteria-reviewer` = `c6e5d5649bf89658036cf38abba9c626701220e7b00831c2d843ceff94d81021`, `skill-usage-ledger` = `6a27b5c8e690b605d7dca4b0e4c2ff1d67dfa6ac6c18469d5657b4ff093339a4` — both **match**.
**No preclaiming:** the row text contains neither its own digest nor any bound-field hash (checked against `eeb35925`, `4cc5171f`, `c5f71554`, `f29decc7`, `2dfe2f5f`, `d08418e5` — all absent), per L720–L721.
**One sequencing note for the publisher.** These rows must be inserted **together with Stage D round 3's rows and Stage F's re-authored rows, in one edit, before Stage F computes its hash** — so the body is stable at the moment the verdict binds it. If only some of the sets land, the hash will bind a payload that is about to change.

---

## 8. Boundary — what this round did not do

- **No repository write.** No commit, branch, push, tag or merge. My working tree was detached at the head to run the checkers; nothing was committed from it.
- **No pull-request write.** No body edit, comment, review, label or reaction. The rows in section 7 are **authored and handed over**.
- **No repair of any defect or observation.** O-4, O-5 and O-6 are reported with their commands and left as found. In particular I did **not** edit the plan's §7.4, did **not** publish the plan or the audits, and did **not** touch the three repaired passages.
- **No adjudication** of the scope question in O-6 — that belongs to the owner or Stage F.
- **No touch** of `clone-pq1`, `clone-pq2`, the legacy checkout, any `wt-*` worktree, the paused VirtualBox VM or the WSL distro.
- **No subagents, no delegation.**
- **Round 1 is preserved, not overwritten** — `VALIDATE-E.md` stays on disk bound to `bd210954`.
- **A verdict is bound to what it measured.** Head `c5f71554…` and body `4cc5171f…` / `eeb359259b517578`.

---

## 9. Timing — *Workspace-citation durability — Stage E ROUND 2*

| | |
| --- | --- |
| **Item** | *Workspace-citation durability — Stage E ROUND 2 at the corrected head* (shared task `task-17`) |
| **Start** | **`2026-10-13T11:34:55-07:00`** (America/Los_Angeles) — the modification stamp of the first file this round wrote (its byte-exact capture of the pull-request body), the earliest start I can **evidence** rather than assert. No separate start stamp was issued to me; I have not invented one. |
| **Finish** | **`2026-10-13T11:41:19-07:00`** (America/Los_Angeles) — sampled in the same program run that performed this file's write |
| **Measured wall time** | **`6 minutes 24 seconds (384 seconds)`** — from the evidenced start to the final write |
| **Active time** | **not separately instrumented.** Wall time is the honest measurement, so the ETA comparison is **IMPERFECT** and is labelled as such rather than presented as an active-time split. |

---

<!-- sha256 footer: the hash below covers this file's bytes with the digest line's value replaced by the
     literal placeholder {{SHA256}}, so the digest is stable and independently reproducible.
     Verify by replacing the 64 hex characters on the line beginning "sha256:" with {{SHA256}}, then
     hashing the UTF-8 bytes INCLUDING the final newline. Line endings are LF only. -->
sha256: 57e54b375f5f4345f47ad456f4af946eef989505fb4ba6003759dff38a0ff203
