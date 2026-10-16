# Workspace-citation durability — Stage D ROUND 3 independent implementation audit

**Item:** "Workspace-citation durability — Stage D ROUND 3" (shared task `task-21`).
**Agent:** `of1-stage-d` — in plain words, *the Stage D holder, auditing the third round of the same stage after the round-2 REVISE was repaired*. **No subagents were used.**
**Audited head (40 characters):** `c5f715544da64a43e0c900d33b298bce0957d504` — in plain words, *the third commit on the branch, which enumerates every index row the 2026-09-23 sweep does not reach and refreshes Stage C's own records*. Tree `dd75f7ce039855cc7bbbbc5b687af4ad20b3c6e7`.
**Rounds it supersedes:** `bd210954...` (round 1, ACCEPT) and `b591e0d9...` (round 2, REVISE on D-1 MEDIUM).
**Pinned base:** `dbe2ee28559fef88950b2d8822cf72d3e595ba86`.
**My clone:** `_resume-2026-10-09/_wcd-d-clone` — my own HTTPS clone, re-verified clean, detached at the audited head.

**Reading key — every label in plain English.**
- `P2` — *the middle severity band of the automated reviewer's findings; P2-and-higher is a floor that must be triaged.*
- `SD-D` — *the Stage D independent implementation audit verdict; this record.*
- `sweep` — *the 2026-09-23 commit that created this index and wrote its current-reading boundaries.*
- `AC7` — *the acceptance criterion that the cumulative diff deletes exactly three lines, all of them count lines.*
- `L694` / `L696-L699` — *the delivery-workflow rules that a D/E/F skills row for an older head or round cannot stand for a later one, and that superseded rows are marked in their source records with row text unchanged.*
- `frozen copies` — *the four archival files republished byte-identically under docs/evidence/fu3-record-publication-2026-10-13/.*
- `refreshed` / `superseded` — *the two ways a source record can be carried forward: its target and round updated for work actually re-run at the new head, or marked as no longer standing.*

---

## 1. Verdict

**VERDICT: `SD-D: ACCEPT`** — in plain words, *the workflow's word for an implementation audit that passes and can be built on by the next stage*.

Both round-3 repairs are genuinely done, and I verified them by re-applying **my own** method rather than reading Stage C's account of it:

- **Repair 1 (the round-2 defect D-1): fixed, and fixed completely.** I enumerated **every** row in the evidence index from the file's git history — not just the rows we knew about — and independently confirmed the sweep commit, the fifteen-of-seventeen split, and **exactly two** post-sweep rows. The new header names both, with their dates and adding commits, and excludes them from the sweep's claim. The claim is **true of every row the sweep does not reach**, which is the standard the round-2 verdict set.
- **Repair 2 (the Lead-upgraded INFO): fixed.** Stage C's three own source records now carry `round=3` and the operative head `c5f71554...` with an explicit refreshed clause; Stage D's and Stage E's round-1 records remain marked superseded. I judge the refresh choice correct and well-documented (section 4).

Every invariant that must not have moved has not moved: the four published copies are still byte-identical committed blobs, the frozen O-F1 note still hashes to `f29decc72f1ee1b31d410ead380ce55c46081e2890d004947d9e4a43e00b182d` under a pure append, and the cumulative diff still deletes exactly three lines, every one a count line.

**Skill applied:** `code-reviewer` (`.claude/skills/code-reviewer/SKILL.md`, sha256 CRLF-to-LF `6238b67b7b90fcbb26fcc45300562efa9e290a9d3870548e37bedaabbc76449a`). `reviewable-diff-discipline` was **not** applied: `MANUAL-ONLY`, and no human named it for this lane.

**Verifier validated before use.** My footer verifier reproduced three known-good artifacts (`c2d106af...`, `250cc3e8...`, `a17f1ecd...`) **3 of 3** before it was pointed at anything — the standing caution, honoured again.

---

## 2. What moved

```text
git diff --numstat b591e0d9 c5f71554
9       3       docs/evidence/README.md          <- the ONLY file that moved in round 3

git log --format='%H %ad %s' --date=iso dbe2ee28..c5f71554
c5f715544da64a43e0c900d33b298bce0957d504  2026-10-13 11:28:27 -0700  docs: enumerate every index row the 2026-09-23 sweep does not reach
b591e0d97dbc176a4bdc17128065e2bcf2daed35  2026-10-13 11:18:49 -0700  docs: narrow the citation rule's enforcement claim, scope its census, and date the new index row
bd21095427f584eaf97fa3218b942d1c502594c8  2026-10-13 10:55:55 -0700  docs: publish the FU-3 evidence the O-F1 note cites, and state the citation-durability rule
```
One file, three commits, all DCO-signed (`OK: 2 commit(s)` at round 2; round 3 adds a third, and the PR reports 8 changed files / +1,196 / -3 — unchanged in shape).

---

## 3. Repair 1 — every post-sweep row is now enumerated and the header is TRUE of all of them: **PASS**

### 3.1 My own enumeration, across all seventeen rows

I re-applied the round-2 method — establish a row's age from the file's **history**, never from its text — and ran it over **every** row, not only the two we knew about:

```text
for each link target in docs/evidence/README.md at c5f71554:
    git log --format=%H|%ad|%s --date=short -S <target> -- docs/evidence/README.md   (oldest hit = the adding commit)

rows with a link: 17
  backlog-status-reconciliation-2026-09-12.md              2026-09-23  9817037bf9  in sweep
  behavioral-eval-runner-wp-2b-0-summary.md                2026-09-23  9817037bf9  in sweep
  behavioral-eval-runner-wp-2b-1-summary.md                2026-09-23  9817037bf9  in sweep
  behavioral-eval-runner-wp-2b-2-summary.md                2026-09-23  9817037bf9  in sweep
  behavioral-eval-runner-wp-2b-3-summary.md                2026-09-23  9817037bf9  in sweep
  ber-bkl-007-schema-integrity.md                          2026-09-23  9817037bf9  in sweep
  ber-pr88-closeout-2026-09-12/README.md                   2026-09-23  9817037bf9  in sweep
  ber-pr88-closeout-2026-09-12/preflight/final-plan.md     2026-09-23  9817037bf9  in sweep
  ber-recovery-2026-09-11/README.md                        2026-09-23  9817037bf9  in sweep
  ber-recovery-2026-09-11/replacement-plan.md              2026-09-23  9817037bf9  in sweep
  ber-replacement-candidate-1-summary.md                   2026-09-23  9817037bf9  in sweep
  control-plane/cp-wp-001-review.md                        2026-09-23  9817037bf9  in sweep
  control-plane/cp-wp-003a-review.md                       2026-09-23  9817037bf9  in sweep
  setup/issue-101-package-2-review.md                      2026-09-23  9817037bf9  in sweep
  setup/issue-101-package-3-review.md                      2026-09-23  9817037bf9  in sweep
  scif/scif-closeout-corrections-2026-10-11.md             2026-10-11  503c3b3042  POST-SWEEP
  fu3-record-publication-2026-10-13/README.md              2026-10-13  bd21095427  POST-SWEEP

index file created by: 9817037bf9b270b7dd7d22f8b72a0539cbd2c731 | 2026-09-23 | docs: index decision evidence and date stale statuses
ROWS THE 2026-09-23 SWEEP DOES NOT REACH: 2
```
This reproduces Stage C's claim **exactly and independently**: the file was created by the sweep commit on 2026-09-23, fifteen rows date from it, and exactly two do not.

### 3.2 The header's claim, tested clause by clause against that enumeration

The round-2 sentence — "Rows added after that sweep state their own date and base revision in the row itself" — was false of the SCIF row and is **gone**. It is replaced by:

> This index was created that day and fifteen of its seventeen rows date from that sweep. **Exactly two rows post-date it and are therefore not covered by it:** the SCIF close-out corrections row, added 2026-10-11 by commit `503c3b30`, whose provenance is that commit's record; and the FU-3 record publication row, added 2026-10-13 by the workspace-citation-durability change against base `dbe2ee28`, which states its own date and base revision in the row itself. Neither row can name the commit that contains it — a page cannot cite its own commit, the convention `docs/roadmaps/aegis-ci-baseline-2026-10-11.md` L51-L52 states for itself.

```text
"This index was created that day"                          -> 9817037b, 2026-09-23            TRUE
"fifteen of its seventeen rows date from that sweep"       -> 15 added by 9817037b, 17 rows  TRUE
"Exactly two rows post-date it ... not covered by it"      -> exactly 2                     TRUE, and COMPLETE
"the SCIF ... row, added 2026-10-11 by commit 503c3b30"    -> 503c3b30, 2026-10-11          TRUE
"the FU-3 ... row, added 2026-10-13 ... against base dbe2ee28,
 which states its own date and base revision in the row"   -> row text says exactly that  TRUE
"Neither row can name the commit that contains it"         -> self-reference; convention exists  TRUE
```
**PASS.** This is the distinction the round-2 verdict turned on: a **complete enumeration that is accurate**, not a vague claim about an unbounded set and not a weakened claim that is still false. The two rows are excluded by name, so the header's 2026-09-23 sweep claim is now true of every row it still reaches.

**On Stage C's choice of scope-and-enumerate over annotating the SCIF row: I accept it, and the reasoning is sound.** Annotating that row would have replaced a **pre-existing** line, which would have broken this change's audited property that the cumulative diff deletes exactly three lines, all count lines — a property Stage E validates and Stage F will rely on. The row's provenance genuinely belongs to the change that added it. Naming both rows in the header fixes the impossibility without touching a byte of pre-existing text, and it is the smaller edit. A weakened-but-false sentence would have been a defect; this is neither weakened nor false.

---

## 4. Repair 2 — the body's own records: **PASS**

The Lead upgraded my round-2 INFO because the body treated its author's records differently from its auditors'. Round 3 fixes that:

```text
from the live body's skills bound field (16 Row source records):
  wcd-stage-c  stage=C  round=3  row=SC-1  target=c5f715544da6  refreshed=True   superseded=False
  wcd-stage-c  stage=C  round=3  row=SC-2  target=c5f715544da6  refreshed=True   superseded=False
  wcd-stage-c  stage=C  round=3  row=SC-3  target=c5f715544da6  refreshed=True   superseded=False
  of1-stage-d  stage=D  round=1  row=SDD-1 target=bd21095427f5  refreshed=False  superseded=True
  of1-stage-d  stage=D  round=1  row=SDD-2 target=bd21095427f5  refreshed=False  superseded=True
  of1-stage-e  stage=E  round=1  row=SDE-1 target=bd21095427f5  refreshed=False  superseded=True
  of1-stage-e  stage=E  round=1  row=SDE-2 target=bd21095427f5  refreshed=False  superseded=True
  wcd-stage-a  stage=A  round=2  (plan revision 2 seal, not head-bound)          superseded=False
  wcd-stage-b  stage=B  round=2  (re-audit record, not head-bound)               superseded=False
```
The refreshed clause is explicit, and it says what changed and what did not:

> ```refreshed at the operative head c5f71554; the row string is unchanged from round 1, and the work it records was re-performed at this head.```

The body states the rationale in its own voice too (L62–L63): *"My own three Row source records are refreshed, not superseded. Their rows are the author's own, their targets now name the operative head `c5f715544da64a43e0c900d33b298bce0957d504` and round 3, and each record says so; the row strings are unchanged from round 1."* And it credits the round-2 finding it is repairing at L47–L50.

**I judge REFRESH correct here, and I record the reasoning so a later reader can disagree with it explicitly rather than by silence.** `L694` binds **D/E/F** rows: an auditor's row for an older head or round cannot stand for a later one, because the audit's whole value is that it was performed against the revision being merged. Stage C is the **author**, and it genuinely re-performed its work at the new head; refreshing its own records is the accurate description of what happened, whereas superseding them would leave the operative implementation round with no standing record of the skills its author used. The refresh is not silent: the record says the row string is unchanged and the work was redone. Had the row text been edited to look like new work, that would have been a defect; it was not.

**Consistency now holds:** head-bound records for stages that re-ran at this head are refreshed (C), head-bound records for stages that did not are superseded (D, E), and records that are not head-bound at all (A's plan revision, B's re-audit record) are correctly neither. The body no longer treats its author differently from its auditors.

---

## 5. Invariants that must not have moved — re-verified at c5f71554

**The four published copies are still byte-identical committed blobs.** Committed blob at the audited head against the archive source file (not the worktree), and against their round-2 blobs:

```text
BER-G3-FU3-EXECUTION.md        25606 bytes  ea521f84c4d0d88f8e888f3588147a6a63c659f8773f7d41339d9eeca47b9915  blob==source=True
FU3-RECORD-FINAL-REVIEW-F.md   30777 bytes  c0b0c548fa6b8f2cc9b961814099e8e12e690729bfdaa16e6c4b96263d7dab8a  blob==source=True
FU3-RECORD-stage-g-summary.md  25454 bytes  d2ed1cfba306c12d993b5718b1d903de656409f1ff91af2e90c3ee1b178aa031  blob==source=True
REVIEWPATH-FINAL-REVIEW-F.md   21023 bytes  f367d36eda52c45289dee5d2cbdcde82c534db8c97786d23b78d51531491cd55  blob==source=True
```
**PASS 4 of 4.** Round 3 did not touch a byte of them.

**The frozen O-F1 note is untouched and the log is still append-only.**

```text
base index 4148 ; head index 4148
42-line block sha256 = f29decc72f1ee1b31d410ead380ce55c46081e2890d004947d9e4a43e00b182d
equals the bound digest: True ; byte-identical base vs head: True
backlog diff: hunks=1 deletions=0 additions=35
```
**PASS.**

**P2-1 is still literally true, and the checker it describes is unchanged.**

```text
LINK line 32 at this head: LINK = re.compile(r"\[([^\]\n]*)\]\(\s*(<[^<>\n]*>|[^()\n]*?)\s*\)")
no minimum-links / required-citation logic in the checker: True
the repaired sentence present in BOTH placements (whitespace-normalised): index True ; record True
```
**PASS.** The only file round 3 touched is the evidence index, and the sentence survives there unchanged; the publication record was not touched in round 3 and still carries it.

**P2-2's scope statement is still accurate and unchanged.** The publication record did not move this round; its heading still reads `## 3. Every archive path the pre-change records cite, and its disposition`, and the "for example" exclusion paragraph naming the two source-archive paths inside `BER-G3-FU3-EXECUTION.md` at L113–L114 and the row-source locator inside `FU3-RECORD-FINAL-REVIEW-F.md` at L222 is present. My round-2 count stands and still applies to the same bytes: **16 archive locators across the four copies** (BER 7, FINAL-REVIEW 4, stage-g 3, REVIEWPATH 2). **PASS.**

---

## 6. AC7 — the deletion count and, more importantly, the composition

```text
git diff -U0 dbe2ee28 c5f71554   -> deleted lines: 3
   '-- [Evidence reading guide](evidence/README.md): routes to 16 dated decision and'
   '-This index helps maintainers and reviewing agents find **16 selected decision'
   '-page has been reviewed or that these 16 pages cover the full repository.'
every deleted line contains '16': True

round2 -> round3 deleted lines: 3
   (the three lines round 2 had itself added: the header sentence and the row's redundant convention clause)
round-3 deletions that removed PRE-EXISTING text: 0
```
I tested the composition the only way that settles it: for each round-3 deletion I searched the **base** revision's copy of the file for that exact line. None was found, so none removed pre-existing text — they are round 2's own sentences being replaced by round 3's. **The cumulative count is still exactly 3, and all three are still count lines.** "Three deletions" means the same thing in round 3 as in rounds 1 and 2.

```text
base..round3 diff shape: 8 paths (5 added, 3 modified) ; added-file count 5 ; nothing under the archive prefix
base..round3 numstat: docs/README.md 1/1 ; docs/evidence/README.md 29/2 ; four copies 347/0, 274/0, 233/0, 107/0 ; record README 170/0 ; backlog 35/0
```
The index file's cumulative numstat grew from 23/2 to 29/2 across the three rounds — insertions only, the same two count-line deletions. **No archive dump.**

---

## 7. The live body at this head

```text
updated_at 2026-10-13T18:20:37Z  ->  superseded by the round-3 body revision
head_sha   c5f715544da64a43e0c900d33b298bce0957d504
body bytes 45,015 as fetched ; sha256 a6474d2209f26327dbcced94f79e64ca42ed7b6bd21ec837c116b792a6d5b2fa
three whole-line sentinel pairs: skills L96 (payload L97-L153), security L158 (payload L159-L162), witness L169 (payload L170-L181)
collapsed lengths: witness 1468, skills 29136, security 45 ; joined 30651
bound-field first-16 = eeb359259b517578
full                 = eeb359259b51757822f28ac313d69ab17fff41ab9ce03bfc282337b344adba95
matches the Lead's figure eeb359259b517578: True
security answer: '- [ ] Yes - surface(s) touched: none - [x] No'   -> No, correct
16 table rows / 16 Row source records (11 data rows + 5 explicit absence records)
```
**PASS.** No stage is omitted, the security answer is **No**, and the hash reproduces independently. *My round-2 rows are correctly NOT in this body* — they name a superseded head and cannot stand, which is the rule I am applying to Stage C in section 4; the Lead records that Stage C withheld them and Stage F's capture for the same reason. My round-3 rows are authored in section 9.

---

## 8. Observations — stated, not defects

**OBS-1 (INFO) — the header's "the commit that contains it" is slightly loose.** The phrase reads naturally as *the commit that added the row*, which is what the two named rows cannot self-cite; strictly, every later commit also "contains" the row. The sentence's own context ("added 2026-10-11 by commit `503c3b30`" / "added 2026-10-13 by the workspace-citation-durability change") fixes the reading, so this is ambiguity, not a falsehood.

**OBS-2 (INFO) — the header is now longer than the index's other preamble paragraphs.** It carries a six-line enumeration where the file's style is one or two lines. It is accurate and it discharges a real finding, so I do not grade it; if a later readability pass trims it, the enumeration must survive in some form, because it is what makes the sweep claim true.

**OBS-3 (INFO, method) — the text checks that must be whitespace-normalised.** The repaired rule sentence wraps to each placement's width, so a raw byte search returns false for text that is present. Both placements were verified on whitespace-flattened text.

---

## 9. Stage D ROUND-3 skills usage (authored here; to be published verbatim by the publisher)

**Copy-ready rows** — bound to the FINAL audited head `c5f715544da64a43e0c900d33b298bce0957d504`, per L694:

```text
| `code-reviewer` | Stage D round 3 / `of1-stage-d` | Re-applied the round-2 method to the round-3 repairs: enumerated EVERY row in docs/evidence/README.md from the file's git history (`git log -S <link target>`) rather than from its text, then tested the new header clause by clause against that enumeration; read the body's sixteen Row source records to check the author's records are now treated consistently with the auditors'; and re-ran the invariant battery (byte-fidelity, frozen note, AC7 count and composition, P2-1 against the checker, P2-2 against the enumerated locators) | verdict `SD-D: ACCEPT`: exactly two rows post-date the sweep (SCIF 2026-10-11 by 503c3b30; FU-3 2026-10-13 by bd210954) and the new header names both with dates and commits, so the sweep claim is TRUE of every row it reaches; Stage C's three records are refreshed to round 3 at this head while D's and E's remain superseded, which I judge correct and well-documented; four published blobs byte-identical; frozen note still f29decc7...182d with a pure append; cumulative deletions still 3, all count lines, 0 pre-existing lines removed in round 3. Recorded in `AUDIT-D-round3.md` |
| `skill-usage-ledger` | Stage D round 3 / `of1-stage-d` | Emitted this round's six-field usage records, resolving each name against `tools/skills-manifest.json` at the audited base and copying each digest from the manifest rather than remembering it | both names resolve and both digests recompute from `.claude/skills/<name>/SKILL.md` with CRLF-to-LF normalisation: `code-reviewer` = `6238b67b7b90fcbb26fcc45300562efa9e290a9d3870548e37bedaabbc76449a`, `skill-usage-ledger` = `6a27b5c8e690b605d7dca4b0e4c2ff1d67dfa6ac6c18469d5657b4ff093339a4`; manifest `tools/skills-manifest.json` sha256 `9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832`; the ledger is in section 9 of `AUDIT-D-round3.md` |
```

**Row source records** — for insertion inside the existing skills bound field, after the table:

```text
<!-- Row source: agent=of1-stage-d; stage=D; round=3; row=SDD3-1; target=c5f715544da64a43e0c900d33b298bce0957d504 (this pull request's candidate head); source=_resume-2026-10-09/evidence/workspace-citation-durability-2026-10-13/AUDIT-D-round3.md section 9 fenced block row 1 (the exact bytes hashed); binding=sha256 2f2e4c2bfccecf7a63510b24b4642f6f8bb735bb4004e38c0ab3b9788eb60902 over the fenced block's UTF-8 bytes including the final newline (the two Stage D round-3 row lines joined by LF plus one trailing LF, 1878 bytes); manifest=tools/skills-manifest.json sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832; limits=none. -->
<!-- Row source: agent=of1-stage-d; stage=D; round=3; row=SDD3-2; target=c5f715544da64a43e0c900d33b298bce0957d504 (this pull request's candidate head); source=_resume-2026-10-09/evidence/workspace-citation-durability-2026-10-13/AUDIT-D-round3.md section 9 fenced block row 2 (the exact bytes hashed); binding=sha256 2f2e4c2bfccecf7a63510b24b4642f6f8bb735bb4004e38c0ab3b9788eb60902 over the fenced block's UTF-8 bytes including the final newline (the two Stage D round-3 row lines joined by LF plus one trailing LF, 1878 bytes); manifest=tools/skills-manifest.json sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832; limits=none. -->
```

**Captured row-block digest — computed from these exact bytes:**
sha256 `2f2e4c2bfccecf7a63510b24b4642f6f8bb735bb4004e38c0ab3b9788eb60902` over the two row lines joined by LF plus one trailing LF (`1878` bytes), re-derived from the written file after sealing.

**Six-field ledger** (`skill@<manifest-sha256[:12]> / reason / applied / result / incomplete / by`):

```text
code-reviewer@6238b67b7b90 / reason: a Stage D round must test a repair against the artifact it describes and against the standard the previous round set, not against the repairer's account of it / applied: enumerated all seventeen index rows from git history, tested the new header clause by clause, read all sixteen Row source records in the live body, and re-ran the invariant battery including AC7's composition test against the BASE revision / result: SD-D ACCEPT with no defect; exactly two post-sweep rows, both named with dates and commits; refresh-vs-supersede consistency achieved; 4 of 4 published blobs byte-identical; frozen note f29decc7...182d under a 1-hunk 0-deletion append; cumulative deletions 3, all count lines, 0 pre-existing lines removed / incomplete: Stages E, F and G and the merge receipt are not mine to run; the body's bound-field hash will change again when these rows are inserted and Stage F must hash it as it then stands / by: of1-stage-d, Stage D, round 3
skill-usage-ledger@6a27b5c8e690 / reason: the workflow requires each stage round to record which skills it read, bound to the manifest hash so the exact instructions are pinned / applied: authored the two rows above and this ledger, resolving both names in tools/skills-manifest.json and recomputing both digests from .claude/skills/<name>/SKILL.md with CRLF-to-LF normalisation / result: both resolve and both recompute exactly - code-reviewer 6238b67b7b90fcbb26fcc45300562efa9e290a9d3870548e37bedaabbc76449a, skill-usage-ledger 6a27b5c8e690b605d7dca4b0e4c2ff1d67dfa6ac6c18469d5657b4ff093339a4; manifest sha256 9497950a61202aa28284a0ae5d3683ce398805bffa56c54917b96b0f708f6832 / incomplete: None / by: of1-stage-d, Stage D, round 3
```

**Limits.** This round read no other Aegis skill; `reviewable-diff-discipline` was refused as `MANUAL-ONLY` and unnamed by a human. Per L720–L721 these rows preclaim no other stage's verdict and embed no digest of themselves and no eventual body hash. Rounds 1 and 2 remain on disk unchanged.

---

## 10. Not verified, and the limits of this round

- **Stage C's stated reason for choosing scope-and-enumerate** is recorded in its commit message and the body; I verified the *consequence* it claims (that annotating the SCIF row would have replaced a pre-existing line, breaking AC7) by confirming that the row's line is present in the base revision and unchanged at this head. I did not audit Stage C's internal deliberation.
- **The two post-sweep rows' *boundary text* provenance** is established by the commit that added each row; I did not attempt to date the prose inside the target pages themselves.
- **The archive file count** remains method- and time-dependent; no criterion binds it.
- **The bound-field hash binds the body revision I hashed** (`updated_at 2026-10-13T18:20:37Z` at the time of fetch, head `c5f71554`). Inserting these round-3 rows changes it again; Stage F must hash the body as it then stands.
- **AC4 corpus-wide link check** was not re-derived this round: the only file round 3 touched is `docs/evidence/README.md`, and the same checker over the changed pages reports 0 broken and 0 dead, so the corpus result is unaffected.
- **Not reviewed:** the internal prose of the four frozen copies (verbatim by AC1), and hosted CI beyond the `gh pr checks` conclusions.
- **Environment limit, disclosed:** this host's sandbox blocks MSYS `sh.exe`, so the local-path clone route cannot run `git-upload-pack`; I clone over HTTPS and run `gh` directly. Python subprocess capture worked normally.

---

## 11. Timing

| | |
| --- | --- |
| **Item** | `Workspace-citation durability — Stage D ROUND 3` |
| **Start** | `2026-10-13T11:29:48-07:00` (America/Los_Angeles) — the stamp sampled at this item's first action |
| **ETA at start** | **not stated** in the brief, so no ETA-versus-actual comparison is claimed as met |
| **Finish** | `2026-10-13T11:33:38-07:00` — sampled in the same program run that performed this file's final write |
| **Measured wall time** | `3 minutes (230 seconds)` |
| **Active time** | **not separately instrumented**, so the comparison is **IMPERFECT and labelled as such**; the item was blocked on `task-20` for part of its wall time, so wall time overstates active audit work. |

---

## 12. Summary

| Check | Result |
| --- | --- |
| Repair 1 — every post-sweep row enumerated from git history | **PASS** — exactly 2 (SCIF 2026-10-11 / 503c3b30; FU-3 2026-10-13 / bd210954), matching Stage C independently |
| Repair 1 — the new header is TRUE of every row it reaches | **PASS** — clause-by-clause against my enumeration; complete, not vague, not weakened |
| Repair 2 — Stage C's records refreshed to round 3 at this head | **PASS** — with an explicit, honest refreshed clause |
| Repair 2 — the body treats author and auditors consistently | **PASS** — C refreshed, D/E superseded, A/B not head-bound |
| Refresh-vs-supersede judgment | **ACCEPTED** — reasoning recorded in section 4 so it can be disagreed with explicitly |
| Four published copies byte-identical committed blobs | **PASS — 4 of 4** |
| Frozen O-F1 note + append-only log | **PASS** — `f29decc7...182d`, 1 hunk, 0 deletions |
| P2-1 still literally true; checker unchanged | **PASS** |
| P2-2 scope statement still accurate | **PASS** — 16 locators, census not widened |
| AC7 count AND composition | **PASS** — 3 cumulative deletions, all count lines; 0 pre-existing lines removed in round 3 |
| Body bound-field hash | **PASS** — `eeb359259b517578` recomputed independently |
| Defects | **none** |

<!-- sha256 footer: the hash below covers this file's bytes with the digest line's value replaced by the
     literal placeholder {{SHA256}}, so the digest is stable and independently reproducible.
     Verify by replacing the 64 hex characters on the line beginning "sha256:" with {{SHA256}}, then
     hashing the UTF-8 bytes including the final newline. Line endings are LF only. -->
sha256: 3ead9a9a4e6d41a6221caabacc55c5c3f8189f67982e06056801acbd0347f9e4
