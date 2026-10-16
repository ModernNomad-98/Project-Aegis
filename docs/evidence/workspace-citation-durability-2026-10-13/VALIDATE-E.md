# WORKSPACE-CITATION DURABILITY — STAGE E: VALIDATION OF ALL ELEVEN ACCEPTANCE CRITERIA

**Item:** "Workspace-citation durability — Stage E: validate acceptance criteria" (shared task `task-12`) — in plain words, *the fifth stage of the seven-stage delivery chain, whose job is to re-run and re-derive every acceptance criterion the plan stated, at the exact head and body under review, and to say plainly which ones pass, which fail and which could not be run.*

**Agent:** `of1-stage-e` — the Stage E validator, and a **different holder from** Stage A (`wcd-stage-a`), Stage B (`wcd-stage-b`), Stage C (`wcd-stage-c`) and Stage D (`of1-stage-d`). **No subagents. Nothing was delegated.**

**Skill dogfooded:** `acceptance-criteria-reviewer` — in plain words, *the Aegis skill that judges whether a criterion names an observable outcome, a pass-or-fail threshold and the evidence that will prove it, and returns one verdict per criterion.* Its three-part test was applied to **validation**: every criterion got an outcome, the plan's own threshold, the exact command, and one verdict. Secondary: `skill-usage-ledger` — in plain words, *the Aegis skill that produces the record of which skills a task used, bound to the skills manifest* — used to author this stage's rows in section 7. Both files were read in full from `.claude/skills/` at the head under test.

**Reading key — every label in this record, in plain words (the owner's permanent reporting rule).**
- `first11` — the plan's acceptance criteria AC1–AC11: *the eleven measurable conditions this change must meet.*
- `O-F1` — *observation F1 from the FU-3 record lane: a governance note that cited evidence only a session workspace held.*
- `FU-3` — *the Behavioral Eval Runner provider-usage reconciliation attempt whose record lane merged as pull request #764.*
- `AEGIS-APR-050` — *the owner rule that a merge waits for the automated Codex review and that every P1/P2 finding is triaged first.*
- `gate_pattern` — *the regular expression read from the skills-validation workflow that decides which changed paths are protected and force a manual merge.*
- `DCO` — *the Developer Certificate of Origin sign-off trailer every commit in the pull-request range must carry.*
- `bound fields` — *the three pull-request-body fields the process acts on: the reconciliation witness, the Aegis skills table and the security answer.*
- `Row source` — *the provenance record inside the skills bound field that binds each published table row to its authoring agent, stage, round, target and source.*
- `UNRUN` — *a check that did not run. Unrun coverage is never a pass.*

---

## 1. What was validated, and at exactly which revision

| | |
| --- | --- |
| **Repository** | `ModernNomad-98/Project-Aegis` |
| **Pinned base** | `dbe2ee28559fef88950b2d8822cf72d3e595ba86` — in plain words, *the tip of main this change targets, being the merge commit of pull request #765.* |
| **Head validated (40 characters)** | `bd21095427f584eaf97fa3218b942d1c502594c8` — in plain words, *the single commit of pull request #766.* |
| **Pull request** | #766, `docs/workspace-citation-durability-20261013` |
| **Body revision** | stored body **30,374 bytes**, `sha256 52491e9388924f51b3292d19ff39cca85af593161ad14612be70d3bcc92ab6ff`, 0 CRLF |
| **Bound-field hash** | first-16 **`6f36dda81cf9f3cd`**, recomputed here by the documented method (full `sha256 6f36dda81cf9f3cd9cf0ea960dd017a4e761124781bb378d90d006a2a46c27ee`) |
| **My own private clone** | `_resume-2026-10-09/_wcd-e-clone`, made **fresh over HTTPS** from `https://github.com/ModernNomad-98/Project-Aegis.git`. The local-path clone route and the MSYS shell route are sandbox-blocked on this host, so the HTTPS route was used with `-c http.sslBackend=openssl`. |
| **A second, independent clone** | `_wcd-e-scratch/fresh-wcd` — a single-branch clone of the candidate branch, used for AC9, with the session archive **verified absent** inside it. |
| **Writes made by this stage** | exactly **one file** (this record) plus my two throwaway clones. **No repository write, no commit, no push, no body edit, no comment, no label, no merge.** |

**Verifiers validated before use — this lane's own rule, applied to me.** Three false seal accusations already occurred in this lane, so before accusing anything I validated both of my verifiers against known-good artifacts:
- **footer verifier** — re-sealed three artifacts whose seals were already established independently: `OF1-DISCHARGE-PLAN.md` (`250cc3e8…`), `OF1-DISCHARGE-VALIDATE-E-ROUND2.md` (`73254f26…`) and `OF1-DISCHARGE-AUDIT-D.md` (`c2d106af…`). All three reproduced; **3 of 3 PASS**.
- **body-digest verifier** — the plan's AC2 concerned `REVIEWPATH-FINAL-REVIEW-F.md`'s body digest. My first method (raw byte slice above the heading) produced `5719fda8…` and **disagreed** with the claimed `81884e0d…`. Rather than accuse, I read that file's own statement of its method (L41, L107: *LF-normalised, cut immediately before the whole-line heading, joined with LF, one trailing LF*), applied it, and reproduced **`81884e0d49cb117c7f7884350ce23adcfac6788891c0a9bc8828dc19461abcc8`** exactly over 20,338 bytes / 102 lines — and a **negative control** (one flipped byte) correctly FAILED. **My first method was wrong; the artifact was right.** Recorded because it is the exact failure mode this lane exists to remove.

---

## 2. Disposition

> ## **SD-E: INCOMPLETE — UNRUN LISTED**

**Written with its prefix**, per `docs/delivery-workflow.md` L56–L61. The token is the workflow's own vocabulary for `SD-E`; no other token is used and no bare disposition is written.

**All eleven acceptance criteria PASS at this head — measured, not ratified.** Every one of AC1–AC11 was re-derived from the repository, the live pull request or the archive, with the command recorded in section 4.

**Why this token and not PASS.** L193: *"UNRUN is never PASS. A check that did not run is named, not absorbed."* Three checks genuinely could not be executed in this session (section 5) — two repository self-test suites and the `gate-guard` bash step. Reporting PASS while those are unrun would be exactly the dishonesty this lane exists to remove. **Why it is affirmative:** per L185–L188 this disposition is affirmative when every unrun check is either (a) run by a named CI job at that exact head, evidenced, or (b) listed with what would resolve it — and all three satisfy (a). Per L190–L193, **SD-F must accept this list as part of its review and SD-G's receipt must record it — because E said so, not as a condition of E being affirmative.**

**Why not FAIL.** Nothing failed. The two defects found are defects in the **plan's own prescribed commands**, not in the implementation (section 6): each plan command fails to produce its own threshold while the underlying substance is correct, and I reproduced both exactly.

**Bound to what.** This disposition is bound to head `bd210954…` **and** to body revision `52491e93…`, whose bound-field hash is `6f36dda81cf9f3cd`. **The body will change once more before Stage F hashes** — it carries no Stage D, E or F skills row, which is expected because those stages had not run when Stage C published. My own Stage E row is authored in section 7 for the publisher to insert verbatim; when it lands, the body revision moves and **this record's body binding must be re-confirmed**. The head, the diff and the eleven criteria are unaffected by a body edit, because the body is not in the tree.

**No repair from here.** This stage reports. It does not edit the change, the body, the plan or the workflow.

---

## 3. The eleven-criterion verdict table

| # | Criterion | Verdict | Threshold | Exact command | Observed |
| --- | --- | --- | --- | --- | --- |
| **AC1** | The four cited records are published byte-identically | **PASS** | **4 of 4 IDENTICAL** | the plan's AC1 snippet, corrected for its own `$P`/`$p` collision (SDC-1); independently, `git show <head>:<path>` vs the archive source | **4 of 4 IDENTICAL** — `ea521f84…` (25,606 B), `c0b0c548…` (30,777 B), `d2ed1cfb…` (25,454 B), `f367d36e…` (21,023 B); each copy's size and digest equal its source's |
| **AC2** | The published copies' own integrity claims still hold | **PASS** | **3 of 3 footers OK** + body digest `81884e0d…` | the plan's AC2 verifier, at the head; validated against three known-good artifacts and a negative control | **3 of 3 footers recompute**: `f5a6b9ca…`, `8f554598…`, `059822aa…`. Body digest **`81884e0d49cb117c7f7884350ce23adcfac6788891c0a9bc8828dc19461abcc8`** over 20,338 bytes / 102 lines — **exact match** |
| **AC3** | Every link the change adds resolves, including heading fragments | **PASS** | exit 0, broken 0, dead 0, **anchors checked >= 4** | `python -P scripts/ci/check-markdown-links.py docs/README.md docs/evidence/README.md docs/evidence/fu3-record-publication-2026-10-13/README.md docs/roadmaps/behavioral-eval-runner-backlog.md` | rc=0; `{"files": 4, "checked": 198, "anchors": 32, "broken": 0, "dead": 0, "skipped": 0}` — **32 anchors >= 4** |
| **AC4** | The corpus-wide link check CI runs is still green | **PASS** | every batch exits 0; broken 0; dead 0; **page count 663** | `git ls-files '*.md'` minus `scripts/tests/fixtures/`, batched 80 per call through the same checker | **checked paths: 663** (matches 658 base + 5 new); **9 batches, 0 failed**; every batch `broken 0, dead 0` |
| **AC5** | The stated evidence-page count equals the measured row count, at every site | **PASS** | **17 = 17 = 17 = 17**; the three stale figures gone | `Select-String` on the three stated figures + count of `^\| .*\]\(` rows | `17 selected` x1, `these 17 pages` x1, `routes to 17 dated` x1, table rows **17**; `16 selected` / `these 16 pages` / `16 dated` all **0** |
| **AC6** | The governance log is append-only; the frozen O-F1 note is byte-unchanged | **PASS** | **deletions = 0** for the log; L4149–L4190 identical at base and head | `git diff --numstat dbe2ee28..HEAD -- <log>`; sha256 of head L4149–L4190; base/head prefix comparison | backlog **35 added / 0 deleted**; the 42-line block hashes to **`f29decc72f1ee1b31d410ead380ce55c46081e2890d004947d9e4a43e00b182d`** — the frozen value; base L1–L4190 and head L1–L4190 are **byte-identical** |
| **AC7** | The diff is exactly the declared file set, and exactly three lines are replaced | **PASS (substance), with plan-command defect SDC-2 confirmed** | **5 A + 3 M = 8 paths; total deletions 3**; no deletion but the count figures | `git diff --name-status`; `git diff --numstat`; `git diff \| Select-String '^-[^-]'` | exactly **8 paths: 5 added, 3 modified, 0 deleted**; numstat matches the plan's declared shape line for line; **deletion sum = 3** and all three deleted lines are count lines (listed in section 4). The plan's `^-[^-]` counter prints **2**, because one deleted line is a Markdown list item beginning `--` — **the plan's own predicted defect, reproduced exactly** |
| **AC8** | No credential material enters the repository; every broad-pattern hit is named and read | **PASS** | **hits_on_copies = 3**, **hits_on_record = 0**, on exactly the three named lines | the plan's revised AC8 snippet, with the `token *[:=]` alternative | **hits_on_copies = 3**, **hits_on_record = 0**. The three hits land exactly where the plan says: `BER-G3-FU3-EXECUTION.md:155` (a provider price line, `nano-USD/token = …`), `FU3-RECORD-FINAL-REVIEW-F.md:121` (a GitHub Actions job id `115364466965`) and `REVIEWPATH-FINAL-REVIEW-F.md:47` (a sha256 containing a 12-digit run). **No other hit.** Without the `token` alternative my own first run returned 2 — confirming the plan's D1 repair was necessary and is now correct |
| **AC9** | A fresh checkout can retrieve the evidence; nothing on the retrieval path needs the archive | **PASS** | **4 of 4 digests reproduce; 3 of 3 cited anchors resolve; archive_dependent_targets = 0; occurrences_outside_map = 0**; map_occurrences reported with **no threshold** | a single-branch clone of the candidate branch, then the plan's AC9 snippet inside it | fresh clone HEAD = `bd210954…`; **archive present inside it: False**; **4 of 4** digests reproduce exactly; `link_targets = 9`, **`archive_dependent_targets = 0`**, **`occurrences_outside_map = 0`**, **`map_occurrences = 10`** (reported, no threshold pinned); the link checker over the record and the log exits **0** |
| **AC10** | The change touches no protected path, proven with a controlled test that prints its own counts | **PASS** | `pattern_len = 371`, `POS = 11 matched = 11`, `DOCUMENTED_NEGATIVES = 4 matched = 0`, `DECLARED_PATHS = 8 matched = 0`, `NEGATIVES_TOTAL = 12 matched = 0`, `CONTROL_FAILURES = 0` | the plan's AC10 script, and independently my own evaluator over all 8 changed paths plus expanded control lists | `pattern_len = 371`; **POS 11/11**; **DOC_NEG 0/4**; **DECLARED 0/8**; **NEGATIVES_TOTAL 0/12**; **CONTROL_FAILURES = 0**. Independently: the extracted pattern returns `nomatch` on all **8** changed paths and `MATCH` on every positive control |
| **AC11** | The rule is present in all three placements, and the log entry's wording is the settled one | **PASS** | **PRESENT for 3 of 3 files** | the plan's AC11 normalised sentence check, plus a raw-contiguity probe and a byte comparison of the two prose placements against the plan's §7.4 block | **PRESENT 3 of 3** — `docs/evidence/README.md`, the publication record, and the log entry. **Raw byte-contiguity is False in all three**, so the normalisation is genuinely required rather than a workaround. The two prose placements carry §7.4's block **byte-for-byte** (1,070 bytes), i.e. one fixed text used verbatim, **not text re-wrapped to satisfy a grep**. The log entry states the rule in its bullet voice at L4192 |

**Tally: 11 PASS · 0 FAIL · 0 criterion-level UNRUN.** Three session-level UNRUN checks are carried in section 5 and are part of the disposition.

---

## 4. Per-criterion evidence — the commands and their raw outputs

Every command below was run by me, in my own clone at `bd210954…`, or in the fresh single-branch clone for AC9. Only the relevant excerpts are quoted.

**AC1 — byte identity.** The plan's own snippet is defective (SDC-1, section 6) so I ran it, recorded its failure, and then ran the check correctly. The corrected comparison, per file, printed source and copy side by side:

```text
BER-G3-FU3-EXECUTION.md       source 25606 B ea521f84c4d0d88f8e888f3588147a6a63c659f8773f7d41339d9eeca47b9915
                              copy   25606 B ea521f84c4d0d88f8e888f3588147a6a63c659f8773f7d41339d9eeca47b9915   IDENTICAL=True
FU3-RECORD-FINAL-REVIEW-F.md  source 30777 B c0b0c548fa6b8f2cc9b961814099e8e12e690729bfdaa16e6c4b96263d7dab8a
                              copy   30777 B c0b0c548fa6b8f2cc9b961814099e8e12e690729bfdaa16e6c4b96263d7dab8a   IDENTICAL=True
FU3-RECORD-stage-g-summary.md source 25454 B d2ed1cfba306c12d993b5718b1d903de656409f1ff91af2e90c3ee1b178aa031
                              copy   25454 B d2ed1cfba306c12d993b5718b1d903de656409f1ff91af2e90c3ee1b178aa031   IDENTICAL=True
REVIEWPATH-FINAL-REVIEW-F.md  source 21023 B f367d36eda52c45289dee5d2cbdcde82c534db8c97786d23b78d51531491cd55
                              copy   21023 B f367d36eda52c45289dee5d2cbdcde82c534db8c97786d23b78d51531491cd55   IDENTICAL=True
RESULT: 4 of 4 IDENTICAL (threshold 4 of 4)
```

Read from the **committed blobs** (`git show <head>:<path>`), not the working tree, so the comparison is against what a fresh checkout receives.

**AC6 — the frozen note.** The 42-line block at head L4149–L4190 hashes to `f29decc72f1ee1b31d410ead380ce55c46081e2890d004947d9e4a43e00b182d`. The base's L4149–L4190 hashes to the same value, and the whole base prefix L1–L4190 is byte-identical to the head prefix. The log's own diff is `35 added / 0 deleted`. **The note was not touched.**

**AC7 — the three deleted lines, listed in full.** This is the substance the plan's counter under-reports:

```text
-- [Evidence reading guide](evidence/README.md): routes to 16 dated decision and delivery records.
-This index helps maintainers and reviewing agents find **16 selected decision
-page has been reviewed or that these 16 pages cover the full repository.
```

Three deletions; every one is a count line; the first begins `--` because it is a Markdown list item, which is exactly why `Select-String '^-[^-]'` prints **2** while `--numstat` sums to **3**. The two figures measure different things and the plan's threshold names the numstat one.

**AC8 — the three hits, with their lines.** `hits_on_copies = 3`, `hits_on_record = 0`. Each hit is a named, read, benign line: a provider price line (`nano-USD/token = **$5.00 / 1M**`), a GitHub Actions job id in a CI results table, and a sha256 inside a table row. No key, private key, GitHub token, ARN, email, `password=` or `secret=` appears in the published pages.

**AC9 — the retrieval path, in the fresh clone.** `link_targets = 9`; `archive_dependent_targets = 0` — **not one link target in the publication record depends on the archive**. `map_occurrences = 10` and `occurrences_outside_map = 0`: the record names the archive only inside its old-path → new-path map, which the plan's own §4.2 row 1 requires it to carry. The archive directory **does not exist** inside the fresh clone, so its absence is proven by the clone itself rather than asserted.

**AC10 — the control test is not vacuous.** All eleven positive controls fire, and all twelve negatives (four documented plus the eight declared paths) do not. I also ran my own evaluator independently over the eight changed paths, with a different control list, and got the same answer.

**AC11 — why normalisation, and why it is not a workaround.** The normative sentence is `An out-of-tree path alone is not acceptable support. A digest pins identity; it never makes an absent artifact retrievable.` It is PRESENT in all three files only after whitespace normalisation, and raw byte-contiguity is **False in all three** — each placement wraps to its own width. Crucially, the two prose placements are **byte-identical to the plan's §7.4 block** (1,070 bytes), a text authored before any check existed; so the wrapping was not introduced to satisfy a grep. That is the difference between a normalised check and a fraudulent one, and I checked it rather than assuming it.

**Repository's own checks at this head.**

| Check | Command | Result |
| --- | --- | --- |
| Skill validator | `python -P scripts/validate-skills.py` | **rc=0** — `OK: 205 skill(s) valid, 0 warning(s)` |
| `DCO` | `python -P scripts/check_dco.py --range origin/main..HEAD` | **rc=0**, with a line beginning **`OK: 1 commit(s) checked, all signed off or exempt.`** |
| PR-body bound-field checker (CI step `pr-body-skills-check`) | `python -P scripts/ci/check_pr_body_skills.py --body-file <body> --author ModernNomad-98` | **rc=0** — `PR body bound fields: OK` |
| PR-body checker self-tests | `python -P scripts/tests/test_pr_body_skills_check.py` | **rc=0** — `Ran 38 tests … OK` |
| CI at the exact head | run **38443072080** (`validate-skills`, run #2078) | `head_sha = bd210954…`, `conclusion: success`; job 115454349937 completed **all 21 steps success** |
| CI check runs at the head | `gh api …/commits/<head>/check-runs` | `changes` **success**, `gate-guard` **success**, `validate-skills` **success**; `windows-offline-checks`, `tools-tests-linux`, `tools-tests-windows` **SKIPPED** by path condition — recorded as **skipped**, **never as passed** |

**The pull-request body, checked as a bound field.** Three whole-line sentinel pairs (skills, security, witness), each opening sentinel alone on its line, each closed by its own `end`; **zero** substring occurrences that are not sentinels; **no duplicates**. Security answer `[x] No` ticked and `[ ] Yes` unticked. Bound-field hash first-16 **`6f36dda81cf9f3cd`**, computed here. **Skills table: 10 data rows, 10 `Row source` records**, covering the stages that have run — Stage A (2 rows), Stage B re-audit (2 rows), Stage C (3 rows) — plus **3 explicit absence rows** naming the A, B and C shapes where no matching skill exists. Each row carries its own record with agent, stage, round, target, source and binding populated. **No Stage D, E or F row exists yet**, which is expected: those stages had not run when Stage C published. The publisher inserts them before Stage F hashes.

---

## 5. UNRUN register — every check that did not run, with what would resolve it

| # | Unrun check | Why it did not run here | Satisfies | What would resolve it |
| --- | --- | --- | --- | --- |
| **U-1** | `scripts/tests/test_validator.py` (validator self-tests) | The sandbox denies the `chmod` this suite performs on its own temporary directory, both in `%TEMP%` and with `TEMP`/`TMP`/`TMPDIR` redirected into this workspace | L185–L188 **(a)**: run by a named CI job at this exact head — `validate-skills` job 115454349937, **step 11 success** | A host without the sandbox limit, or acceptance of the CI evidence |
| **U-2** | `scripts/tests/test_markdown_links.py` (link-checker self-tests) | Same sandbox temp-directory denial | L185–L188 **(a)**: **same job, step 14 success** | As U-1 |
| **U-3** | `gate-guard` as the **actual bash step** | `bash` is denied in this session (`Bash/E_ACCESSDENIED`) — the same limitation the task-12 brief names for this host | L185–L188 **(a)**: the `gate-guard` **check run is success** at this exact head, **plus** my own evaluator of the extracted 371-character `gate_pattern` over all eight changed paths and 11 positive controls | A host where `bash` runs, or acceptance of the check run as the authoritative object |

**UNRUN is never PASS.** None of these three is absorbed into the eleven PASS verdicts; they are carried by the disposition, and per L190–L193 Stage F must accept this list and Stage G must record it.

**No criterion is UNRUN.** Every one of AC1–AC11 was measured at this head by me. The three items above are session-level checks, and for each the *substance* is independently covered — by the CI job that ran it at this head, or by my own re-implementation.

---

## 6. Defects and observations

### 6.1 Defects — both in the PLAN's prescribed commands, not in the implementation

| # | Severity | Defect | Reproduction and evidence |
| --- | --- | --- | --- |
| **SDC-1** | **MEDIUM (plan-command)** | **AC1's snippet cannot verify files 2–4.** It assigns `$P='docs/evidence/fu3-record-publication-2026-10-13'` and then, inside the loop, `$p=(Get-FileHash …)`. PowerShell variable names are **case-insensitive**, so `$P` and `$p` are **the same variable**: the first iteration overwrites the path with a hash, and every later `Join-Path $P $f` fails. | Reproduced verbatim. `$P -eq $p` → **True** after assigning to lowercase `$p`. The snippet printed `IDENTICAL BER-G3-FU3-EXECUTION.md` then `DIFFERS` for the other three, with `Get-FileHash: Cannot find path '…\EA521F84…\FU3-RECORD-FINAL-REVIEW-F.md'`. **The implementation is unaffected**: my corrected AC1 check returns 4 of 4 IDENTICAL. Stage C reported this same defect (SDC-1) — **independently confirmed**. |
| **SDC-2** | **LOW (plan-command)** | **AC7's counter under-reports its own threshold.** `git diff \| Select-String '^-[^-]'` prints **2**, while the threshold is "total deletions 3". | Reproduced verbatim: `Select-String '^-[^-]' count = 2` and `numstat deletion sum = 3`. The third deleted line begins `--` (a Markdown list item in `docs/README.md`), which `^-[^-]` excludes by construction. **The substance holds**: I listed all three deletions and each is a count line. Stage C reported this same defect — **independently confirmed**. |

### 6.2 Observations — reported, not defects in the change

| # | Severity | Observation | My assessment |
| --- | --- | --- | --- |
| **O-1** | **INFO (record provenance, corrected)** | **AUDIT-D.md author mislabel.** The Stage D artifact was produced by `of1-stage-d` but originally named `wcd-stage-d` — two agents were spawned for one task. | **I read the CORRECTED revision:** `AUDIT-D.md` is **36,252 bytes**, raw `sha256 ddfbc5fc79b0ee3c0f42fbeee3e018da5290ed22d4ec68599b57ce6b2d7d9808`, 0 CRLF, with an **ERRATUM at L9** and `of1-stage-d` at L4. The pre-correction revision the Lead quoted (35,637 bytes / `354ef62b…`) is **superseded**; I did not read it. This is a record-provenance correction and **does not touch any of AC1–AC11** — none of my eleven verdicts rests on Stage D's authorship, and I re-derived every fact myself. |
| **O-2** | **LOW (labelling)** | **The Stage A Row source records say `round=1` while their target is `the accepted plan revision 2`.** Stage A ran twice in this lane: the original plan and the revision made in response to `SD-B: REVISE`. | The **binding** is correct and points at the operative record: I recomputed `PLAN.md`'s footer digest and it equals the rows' target `2dfe2f5f…` exactly, and the row text was authored in that revision's §10 table. So the row stands for the **operative** revision, which is what the rule protects. Only the `round` integer reads 1 where a reader might expect 2. **Not a criterion failure** — the criterion requires a row per stage bound to its own captured self-authored source, which holds — but recorded so Stage F can rule on the label. |
| **O-3** | **MEDIUM (named residual — my own view, as asked)** | **The skills Row source records for Stages A, B and C cite session-workspace artifacts** (`PLAN.md`, `AUDIT-B-rev2.md`, `AUDIT-D.md` under `_resume-2026-10-09/`), which a fresh checkout cannot retrieve. | **I judge this correctly handled, and I say why rather than rubber-stamping it.** This change's **own rule** has two branches: publish, *or* — where the artifact cannot be published — carry its digest, name its locator, and **state plainly that it is not retrievable from this repository**. The Row source records do exactly that: each carries a recomputing digest, a locator, and the body states the non-retrievability in a **named residual** inside the skills bound field. So the change **applies its own rule to itself** rather than exempting itself, which is the honest outcome. **The residual judgement I will not make silently:** the rule also says a digest *"is never a substitute for publishing an artifact that could have been published"*, and these three are ordinary text files that **could** have been published — but publishing them is **outside the 8-path scope** that Stage A declared and Stage B audited and accepted, so widening it here would breach the audited contract. The lawful resolution is a scope decision for the owner or Stage F (a later pure-docs change can carry them), **not** something Stage E may decide or repair. Recorded as an open item with that reasoning. |

**Every label above carries its plain-English description in the same item**, per the owner's permanent reporting rule.

---

## 7. Skills this stage used — the Stage E row, copy-ready for the publisher

**Author:** `of1-stage-e`, Stage E, round 1. **Target:** `bd21095427f584eaf97fa3218b942d1c502594c8` (this pull request's candidate head). **An authorized publisher copies this text verbatim**; the publisher does not author, summarise or repair it, and **I did not insert it into the body** — I am the validator, not the publisher.

**Exact captured row text** — the two lines inside the fence below, joined by LF plus one trailing LF, UTF-8, **1,569 bytes**:

```text
| [acceptance-criteria-reviewer](.claude/skills/acceptance-criteria-reviewer/SKILL.md) | Stage E / `of1-stage-e` | Read in full and applied its three-part test as the validation method: each of the plan's eleven acceptance criteria was re-derived at the exact candidate head with an observable outcome, the plan's own stated threshold and the exact command that produces the evidence, then exactly one verdict of PASS, FAIL or UNRUN. Its discipline is what separated criteria that are genuinely measured from checks this session could not run, and it is why two defects were reported against the PLAN's own prescribed commands rather than against the implementation. | The eleven-row verdict table and the UNRUN register in `VALIDATE-E.md` sections 3 and 5 |
| [skill-usage-ledger](.claude/skills/skill-usage-ledger/SKILL.md) | Stage E / `of1-stage-e` | Used its workflow to author this stage's own record: both skill names were resolved against `tools/skills-manifest.json` at the head under test and both digests recomputed from `.claude/skills/<name>/SKILL.md` with CRLF-to-LF normalisation, so the manifest is proven current rather than assumed. Its `incomplete` field names this stage's unrun checks instead of asserting completeness. | `acceptance-criteria-reviewer` = `c6e5d5649bf89658036cf38abba9c626701220e7b00831c2d843ceff94d81021`, `skill-usage-ledger` = `6a27b5c8e690b605d7dca4b0e4c2ff1d67dfa6ac6c18469d5657b4ff093339a4`, both recomputed and matching; `tools/skills-manifest.json` sha256 `9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832` |
```

**`sha256` of that exact captured row text:**

`d08418e5f7a1eeee3c10ed17eafa288ee4720b41f6729448dae5300032a15c5b`

**`Row source` records for the two rows** — excluded from the digest above, so there is no self-reference:

```text
<!-- Row source: agent=of1-stage-e; stage=E; round=1; row=SDE-1; target=bd21095427f584eaf97fa3218b942d1c502594c8 (this pull request's candidate head); source=_resume-2026-10-09/evidence/workspace-citation-durability-2026-10-13/VALIDATE-E.md section 7 fenced block row 1 (the exact bytes hashed); binding=sha256 d08418e5f7a1eeee3c10ed17eafa288ee4720b41f6729448dae5300032a15c5b over the fenced block's UTF-8 bytes including the final newline (the two Stage E row lines joined by LF plus one trailing LF, 1,569 bytes); manifest=tools/skills-manifest.json sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832; limits=the row source is a session-workspace artifact and is not retrievable from this repository - see section 6 observation O-3. -->
<!-- Row source: agent=of1-stage-e; stage=E; round=1; row=SDE-2; target=bd21095427f584eaf97fa3218b942d1c502594c8 (this pull request's candidate head); source=_resume-2026-10-09/evidence/workspace-citation-durability-2026-10-13/VALIDATE-E.md section 7 fenced block row 2 (the exact bytes hashed); binding=sha256 d08418e5f7a1eeee3c10ed17eafa288ee4720b41f6729448dae5300032a15c5b over the fenced block's UTF-8 bytes including the final newline (the two Stage E row lines joined by LF plus one trailing LF, 1,569 bytes); manifest=tools/skills-manifest.json sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832; limits=the row source is a session-workspace artifact and is not retrievable from this repository - see section 6 observation O-3. -->
```

**Manifest provenance, recomputable by any reader.** Both names resolve in `tools/skills-manifest.json` — itself `sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832` — and both digests were recomputed this round from `.claude/skills/<name>/SKILL.md` with CRLF→LF normalisation: `acceptance-criteria-reviewer` = `c6e5d5649bf89658036cf38abba9c626701220e7b00831c2d843ceff94d81021`, `skill-usage-ledger` = `6a27b5c8e690b605d7dca4b0e4c2ff1d67dfa6ac6c18469d5657b4ff093339a4` — both **match**.
**No preclaiming:** the row text contains neither its own digest nor any bound-field hash (checked against `6f36dda8`, `52491e93`, `bd210954`, `f29decc7`, `2dfe2f5f` — all absent), per `docs/delivery-workflow.md` L720–L721.
**A note on this block's own durability, and it is deliberately pointed:** the Row source records I author here cite **this record** under `_resume-2026-10-09/evidence/` — the very shape this change exists to correct. That is **not** an oversight: this stage's artifact is a session-workspace artifact by construction (Stage A's plan and Stage B's audit are too), and publishing them is outside the audited 8-path scope. Observation **O-3** records the same residual for the other stages' row sources, with the honest statement that they are not retrievable from the repository — and that the "could have been published" half is a scope decision for the owner, not for me.

---

## 8. Boundary — what this validation did not do

- **No repository write.** No commit, branch, push, tag or merge. My working tree was detached at the head to run the checkers and nothing was committed from it.
- **No pull-request write.** No body edit, comment, review, label or reaction. The Stage E row above is **authored and handed over**.
- **No repair of any defect.** SDC-1, SDC-2, O-1, O-2 and O-3 are reported with their commands and left as found. In particular I did **not** renumber the Stage A row's `round`, did **not** publish the plan or audits, and did **not** touch the plan's prose.
- **No adjudication** of the scope question in O-3 — that is the owner's or Stage F's.
- **No touch** of `clone-pq1`, `clone-pq2`, the legacy checkout, any `wt-*` worktree, the paused VirtualBox VM or the WSL distro.
- **No subagents, no delegation.**
- **A verdict is bound to what it measured.** This disposition is bound to head `bd210954…` and body revision `52491e93…`. The body **will** move once more (the Stage D/E/F rows), which changes the body binding only — not the head, the diff, or any of the eleven verdicts.

---

## 9. Timing — *Workspace-citation durability — Stage E*

| | |
| --- | --- |
| **Item** | *Workspace-citation durability — Stage E: validate acceptance criteria* (shared task `task-12`) |
| **Start** | **`2026-10-13T11:12:47-07:00`** (America/Los_Angeles) — the modification stamp of the first file this stage wrote (its byte-exact capture of the pull-request body), the earliest start I can **evidence** rather than assert. No separate start stamp was issued to me for this task; I have not invented one. |
| **Finish** | **`2026-10-13T11:16:08-07:00`** (America/Los_Angeles) — sampled in the same program run that performed this file's write |
| **Measured wall time** | **`3 minutes 21 seconds (201 seconds)`** — from the evidenced start to the final write |
| **Active time** | **not separately instrumented.** Wall time is the honest measurement, so the ETA comparison is **IMPERFECT** and is labelled as such rather than presented as an active-time split. A substantial part of the wall time was **waiting on the delivery chain** (Stage A → re-audit → Stage C → Stage D), not working: reconnaissance, harness-building and verifier validation ran while blocked, and the eleven criteria were measured only after `task-11` completed, as the brief required. |

---

<!-- sha256 footer: the hash below covers this file's bytes with the digest line's value replaced by the
     literal placeholder {{SHA256}}, so the digest is stable and independently reproducible.
     Verify by replacing the 64 hex characters on the line beginning "sha256:" with {{SHA256}}, then
     hashing the UTF-8 bytes INCLUDING the final newline. Line endings are LF only. -->
sha256: 9d5d6125f9ac02ec36d968f691faf7ec3275968393289275834e81fac1ec3c85
