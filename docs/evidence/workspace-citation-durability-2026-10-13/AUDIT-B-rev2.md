# Workspace-citation durability — Stage B RE-AUDIT after the revision

**Item:** "Workspace-citation durability — Stage B re-audit" — in plain words, *the independent check that the repairs Stage A made in response to my REVISE verdict are real, performed by re-running the plan's own commands rather than by reading its claims of repair*.

**Agent:** `wcd-stage-b` — in plain words, *the same independent auditor that posted the REVISE; the re-audit is the mandatory second half of the repair-and-re-audit cycle, not a fresh opinion*. No subagents were used; nothing was delegated. Read-only against the repository and GitHub; this file is my only write.

**Stage:** B — INDEPENDENT PLAN AUDIT (re-audit round), under `docs/delivery-workflow.md`. The workflow's `SD-B` disposition is `ACCEPT` or `REVISE`.

**Audited object — the captured revision this acceptance binds:** `_resume-2026-10-09/evidence/workspace-citation-durability-2026-10-13/PLAN.md`, **revision 2**, 700 lines, 77,404 bytes, LF only, final newline present, zero CR bytes.

- **Footer seal, recomputed by me under the placeholder convention: `2dfe2f5fa682861e1110891d4345486d8f1926668cccd0dba1a232ada7702e0a`** — in plain words, *the plan's own self-digest, over its bytes with the 64-hex value on the whole line beginning `sha256:` replaced by the literal `{{SHA256}}`, UTF-8 including the final newline*. **MATCHES the claim; this is the revision I accept.**
- Whole-file sha256: `d02022bcfeef11278feee0048f8ed259c6560e673cfabf7b1313af16a1cf05ee` — in plain words, *the digest `Get-FileHash` reproduces from the bytes on disk, footer included*.
- Exactly **one** whole-line `sha256:` prefix exists, so the placeholder substitution is unambiguous.
- Superseded revision 1, seal `578010377ca538e3454b48eb67aa854fb29b5dfe7127ae8019f44f83cf1e8d68`, in plain words, *the revision I returned REVISE on*, is quoted **exactly once** in the body and labelled "superseded, not overwritten". Nothing was silently overwritten.

**Verdict: `SD-B: ACCEPT` — the revision is `2dfe2f5fa682861e1110891d4345486d8f1926668cccd0dba1a232ada7702e0a`.**

**This acceptance is bound to that digest, not to the path.** Any later edit to the plan voids it; Stage C is held to exactly this revision. All seven of my defects (D1–D7) plus the Lead-added AC9 repair are **verified repaired by running the plan's own commands**, and the new AC11 is checkable with the right method. Four INFO observations are recorded in §4; none affects a decision, a threshold or satisfiability, and none blocks this ACCEPT.

**Timing.** This round's first action was claiming `task-16`; I did not stamp that claim myself, and the nearest observed harness stamp is `2026-10-13T10:49:38-07:00`. Finish `2026-10-13T10:54:16-07:00`. Wall is therefore reported as **approximately 6–8 minutes**, labelled **IMPERFECT** because the start is a neighbouring observation rather than a recorded claim stamp. ETA at start: not stated in task-16; active time was not instrumented.

> **Verdict marker.** `SD-B` is the plan-audit stage. `ACCEPT` and `REVISE` are the workflow's own words (`docs/delivery-workflow.md:178`); this file uses only those.

---

## 1. Method — re-derive, do not accept a claim of repair

I claimed `task-16` at its exact revision, then for each defect **ran the command the plan itself prescribes** and compared the number it produced with the number the plan states. The verifier used for the footer is the same placeholder-convention verifier I validated in the first audit against three known-good artifacts (`OF1-DISCHARGE-AUDIT-B.md`, `FU3-RECORD-FINAL-REVIEW-F.md`, `FU3-RECORD-stage-g-summary.md`) — it was re-validated at the start of this round and reproduced all three.

Repository state at audit time: my own clone `_wcd-b-clone` at `dbe2ee28559fef88950b2d8822cf72d3e595ba86`, `git status --porcelain` empty; live `origin/main` unchanged.

---

## 2. Per-defect verification

### D1 — REPAIRED. AC8's threshold now equals what AC8's command prints.

**What the plan now claims:** the pattern gains the `token *[:=]` alternative and prints **3**, landing on `BER-G3-FU3-EXECUTION.md:155`, `FU3-RECORD-FINAL-REVIEW-F.md:121` and `REVIEWPATH-FINAL-REVIEW-F.md:47`; `hits_on_record = 0`.

**Command:** AC8's own `$pat` (extracted verbatim from the plan's fenced block at L424–L432), applied with `re` to the four byte-identical source files that AC1 proves the copies must equal.

```text
extracted pattern len : 174        (was 162 in revision 1)
adds token alternative: True
hits_on_copies = 3
   BER-G3-FU3-EXECUTION.md:155
   FU3-RECORD-FINAL-REVIEW-F.md:121
   REVIEWPATH-FINAL-REVIEW-F.md:47
plan names exactly these three: True
```

The three named lines really do carry the matches: L155 is the provider price line (`input \`5,000\` nano-USD/token = **$5.00 / 1M**`), L121 the GitHub Actions job id in the CI table, L47 the sha256 inside a table row. **Revision 1 printed 2; revision 2 prints 3 and names each hit.**

*Residual I checked rather than assumed:* `hits_on_record = 0` is satisfiable — I hashed all four sources and **none** of their digests contains a twelve-consecutive-digit run, so a record that prints those digests cannot trip the `[0-9]{12}` alternative. See INFO-4.

### D2 — REPAIRED. AC10's script is now the measurement, and its output matches the plan's stated block line-for-line.

**Command:** the plan's fenced Python block at L466–L520, extracted verbatim and executed from the clone root.

```text
--- ACTUAL OUTPUT ---            --- PLAN'S STATED BLOCK (L524-L529) ---
pattern_len = 371                 pattern_len = 371
POS = 11 matched = 11             POS = 11 matched = 11
DOCUMENTED_NEGATIVES = 4 matched = 0   DOCUMENTED_NEGATIVES = 4 matched = 0
DECLARED_PATHS = 8 matched = 0    DECLARED_PATHS = 8 matched = 0
NEGATIVES_TOTAL = 12 matched = 0  NEGATIVES_TOTAL = 12 matched = 0
CONTROL_FAILURES = 0              CONTROL_FAILURES = 0
exit: 0
OUTPUT MATCHES THE STATED BLOCK EXACTLY: True
```

The script **enumerates** 11 positive controls, 4 documented negatives and all 8 declared paths (12 negatives in total) and **prints every count** — the two things revision 1 did not do. The prose threshold is now those printed numbers, not asserted ones.

### D3 — REPAIRED. F11 states the filter, presents the figure as a timestamped snapshot, and withdraws the wrong cause.

**What the plan now claims (F11, L668):** `737,179 files including version-control internals; 629,280 excluding them` — *a snapshot taken at `2026-10-13T10:44:43-07:00`*, the filter being `System.IO.EnumerationOptions` with `AttributesToSkip = Hidden \| System`; the gap is the `.git` trees, "**not** unreadable files"; revision 1's `IgnoreInaccessible` attribution is **withdrawn**; and "**No acceptance criterion depends on this number, and none may be written to depend on it.**"

**Command and observed output — the stated method, both ways, in one run:**

```text
AttributesToSkip = None               -> 737,195 files
AttributesToSkip = Hidden -bor System -> 629,295 files
difference                            -> 107,900
files under a .git dir (mode A)       -> 107,797
 ```

**Reconciliation of the stated snapshot with my re-measurement.** The plan's `737,179 / 629,280` and my `737,195 / 629,295` are the **same pair of counts, +16 files each**, measured later — the archive is being written to throughout the session, which is exactly why the plan now calls it a snapshot. The mechanism the plan states is **confirmed**: the entire gap comes from the hidden/system filter, and 107,797 of the 107,900 (99.9%) are `.git` files. Revision 1's cause ("inaccessible subtrees") is indeed wrong and is withdrawn. **No acceptance criterion references the figure** — I searched AC1–AC11 and found none.

The revision also records the three disagreeing same-turn measurements (733,980 the Lead, 737,158 mine, 737,179 Stage A) rather than picking one, which is the honest form of a moving number.

### D4 — REPAIRED. §7.4's claim is now true of the plan's own text, and the log entry's wording is settled.

**What the plan now says (§7.4, L294):** the block is "quoted **byte-for-byte** in the two prose placements"; "**the entry does not quote this block verbatim**"; and the entry's wording "is **final in this revision**, settled here so that no byte of the permanent, un-editable log is written twice". The revision note (L43–L49) repeats that Stage C "appends exactly those bytes, and no later repair round re-opens the entry's wording".

**Command:** `grep -n 'verbatim'` over the revision, then reading each hit.

```text
the only occurrence of "verbatim in all three" is at L37 -- the revision note's D4 row,
which QUOTES the withdrawn revision-1 claim in order to describe the defect.
§7.4 itself no longer makes that claim; §7.3's entry is declared a paraphrase by design.
```

I checked this by **reading**, not by substring match — a naive pattern test flags L37 as a live claim, and it is not. The settlement Stage C depends on is unambiguous: the entry at §7.3 is quoted in full (L251–L285), is declared final, and is **not** required to be a verbatim copy of the §7.4 block. The claim that was false in revision 1 is now true.

### D5 — REPAIRED. The byte total matches the plan's own per-file counts.

```text
105,860 present anywhere : False
102,860 occurrences      : 2
measured per-file sum    : 102,860   (25,606 + 30,777 + 25,454 + 21,023)
plan states 102,860      : True
```

### D6 — REPAIRED. Both dated fifteen-figure sites are named with their reason.

§3 now carries a second exclusion class: "**(a) Dated statements about a past index size:** `docs/roadmaps/aegis-execution-metrics.md:2334` … and `docs/roadmaps/aegis-documentation-readability-backlog.md:3188` … state what was true when written; moving a dated record's figure to chase a live count would falsify the record." Both line numbers and both quotations are correct — I read both lines and both say what the plan says they say. The exclusion is now *decided and stated*, which was the whole of D6.

### D7 — REPAIRED. The precedent's count is now the measured one.

**Command:** `git show --numstat 503c3b30 -- docs/evidence/README.md`

```text
3	2	docs/evidence/README.md
```

and the full commit: `3 2 docs/evidence/README.md`, `222 0 scif-closeout-corrections-2026-10-11.md`, `35 0 step-0-reconciliation-v4.md`. §7.2 now reads "made a **3-insertion / 2-deletion** change to that file (`git show --numstat 503c3b30 -- docs/evidence/README.md`)" — exactly right, with the command attached.

### AC9 (Lead-added repair) — REPAIRED. It measures the retrieval path, and the map count is reported, not thresholded.

**What the plan now says (L435–L439):** the record *must* name the archive path, because its old-path → new-path map is required by the scope contract; occurrences **inside** that map are "expected: they are counted and reported, never suppressed". The threshold is "`archive_dependent_targets = 0`; `occurrences_outside_map = 0`; and `map_occurrences` is reported at whatever value it measures — **no threshold is pinned to it**, because Stage C authors the record."

**I re-derived the contradiction it repairs, from the revision-1 bytes** (re-observed this turn, not recalled): revision 1's L384 demanded "0 references to `_resume-2026-10-09`" while its L392 command ran a whole-file `Select-String` over the very record that L94's scope contract requires to carry the old-path → new-path map. **Unsatisfiable as worded — the Lead is right, and this is a defect my first audit missed** (I rated AC9 TESTABLE; that rating was wrong and I withdraw it). The revised criterion is satisfiable: its command computes link targets, archive-dependent targets, map occurrences and occurrences-outside-map, and degrades safely to zero counts when a list is empty. The residual judgement — whether each backtick-or-pipe line really belongs to the map — is stated rather than implied and routed to Stage D.

**No criterion remains that its own command cannot satisfy.** I checked AC1–AC11 individually: each now names an observable outcome, a threshold the command prints, and the command.

### AC11 (new) — CHECKABLE, and the whitespace-normalised comparison is the right method.

**What the plan claims:** the check "run against this plan … finds **3 occurrences** — §7.3's entry, §7.4's block … and this criterion's own command text"; and "a byte-search therefore fails on text that is correct".

**Command:** the plan's own sentence, normalised with `re.sub(r'\s+', ' ', text)`, counted against the revision; then the same sentence counted as a raw byte string.

```text
occurrences of the normalised sentence in the PLAN: 3
  (~L272 the 7.3 entry, ~L304 the 7.4 block, ~L535 AC11's own command text)
raw byte occurrences of the sentence            : 1
```

**The reasoning holds and I verified it both ways:** the sentence is present three times when whitespace is normalised and only **once** as contiguous bytes, because each placement wraps to its own width (the §7.4 block breaks it inside the clause "A digest pins / identity"). A byte-search would therefore report MISSING for two placements that are correct — the method is right, and the plan states the limitation instead of asserting a byte identity that does not hold. That is the D4 lesson applied.

### Row-block locator (the Lead's correction) — CONFIRMED, and the old locator was genuinely stale.

```text
plan L590-L593 -> 08cb06e42db7ca83078c5d2d793f161e28c40862d07bbd896f64cc2d34a3051f   (matches)
plan L456-L459 -> 352e1419574950dff8ca09bc79581fb042eb41c3b769903c17112707ab432b15   (moved text)
```

The row-block **digest** is unchanged; only the locator moved, exactly as reported. `L456-L459` now holds AC9's map-check commands, so a row that still cited that range would have pointed at the wrong text — the defect class this lane exists to fix. **My own rows' locator is in `AUDIT-B.md`, a sealed file that has not changed, so `L285-L288` there remains correct.**

---

## 3. Revision transparency, and scope invariance

**Transparent, not overwritten.** A dated revision note opens the file (L19–L62) and states "This is revision 2 of this plan. Revision 1 is **superseded, not overwritten**"; it quotes revision 1's seal in full, its line and byte counts, and a per-defect disposition table. Revision 1's seal occurs **exactly once** in the body. Anyone holding my first audit can identify exactly what it audited.

**No scope decision changed.** Verified line by line against revision 1:

| Invariant | Status |
| --- | --- |
| Same 8 paths (5 added + 3 modified) | unchanged |
| Same class — `Governing class: docs-only`, `Approval path: none` | unchanged |
| Same four published FU-3 files | unchanged |
| Same 7 owed citations (O1), each by file and line | unchanged |
| Same anchor — inserted between L4191 and L4192 | unchanged |
| Same three live `16` sites | unchanged |
| Frozen O-F1 note still protected | unchanged |
| O-F1 closure question still not re-decided (`4261109109` non-claim retained in both the plan and the §7.3 entry) | unchanged |

**Load-bearing facts re-confirmed at this revision** (my clone at `dbe2ee28`, clean):

```text
three live "16" sites : docs/evidence/README.md:3, docs/evidence/README.md:49, docs/README.md:59  (no fourth)
frozen O-F1 note      : L4149-L4190 -> f29decc72f1ee1b31d410ead380ce55c46081e2890d004947d9e4a43e00b182d  MATCH
citation census       : 10 occurrences in 4 files (backlog 4, ci-baseline 3, SCIF 2, register 1)
anchor                : L4191 blank, L4192 = "## 14. Continuation instructions for a brand-new session"
Stage G fragment      : "9---------the-carried-open-publication-item" is in the checker's own anchor set
gate_pattern          : 371 chars; 0 of 8 declared paths match; 11/11 positive controls match
```

---

## 4. New observations

Four INFO observations from this round. None affects a decision, a threshold or satisfiability; none blocks the ACCEPT. Each carries its command so Stage D or E can re-derive it.

**INFO-1 — F11's "the whole gap" is 99.9% of the gap, not 100%.** F11 says the hidden/system filter "skips hidden and system entries, which on Windows is the `.git` trees — that, and **not** unreadable files, is **the whole gap** between the two counts". Measured: the gap is 107,900 files, of which 107,797 are under a `.git` directory; the remaining **103** are other hidden or system entries outside `.git`. The substantive correction is **verified** — the gap is the filter, not inaccessible files — and only the word "whole" is a touch absolute. *Suggested, not required:* "essentially all of it the `.git` trees (107,797 of 107,900 in Stage B's re-measurement)".

**INFO-2 — the §3 command returns 15 lines and the enumeration accounts for 14.** §3 attaches `git grep -n -E '(^|[^0-9])1[56] (selected|dated|pages)'` as the proof of its exclusion classes. Running it returns **15** lines; the plan accounts for 3 live sites, 2 class-(a) and 9 class-(b) = **14**. The fifteenth is `docs/roadmaps/aegis-documentation-readability-backlog.md:1704` — `D15 pages that went past 10 and were accepted again within this range change` — which is a **false positive of the pattern** (`D15` is a decision identifier matched by `[^0-9]1[56]`, not a page count). It is not a figure site and needs no correction. *Suggested, not required:* one clause naming it, so that every line the command prints is accounted for and an unaccounted line cannot later be mistaken for a missed site.

**INFO-3 — AC9's "3 of 3 cited anchors resolve" is informal.** The §7.3 entry carries three citation links, of which **two** carry heading fragments; the prescribed command proves resolution as `broken 0 / dead 0`. The criterion is satisfiable and the command is the right one; only the phrase "3 of 3 anchors" reads as though three fragments are checked. *Suggested, not required:* "the three citation links resolve, `broken 0`, `dead 0`".

**INFO-4 — AC8's `hits_on_record = 0` is satisfiable, with one content obligation on Stage C.** I hashed all four sources and **no** digest contains a twelve-consecutive-digit run (`ea521f84…`, `c0b0c548…`, `d2ed1cfb…`, `f367d36e…` — all clean), so printing them cannot trip the `[0-9]{12}` alternative. The residual is that Stage C must not write any bare twelve-digit-or-longer number into the record. Given the record's numbers are byte counts and line anchors, that is easy to meet — but it is a content obligation, not a formality, and it is recorded here so Stage C is not surprised by AC8's second count.

---

## 5. What I could not verify

1. **The three placement files do not exist yet.** AC11 is a **requirement on the implementation** — the plan says so explicitly. What I verified is that the check works and that the method is right (3 normalised occurrences against 1 raw, §2). Whether Stage C's three files contain the sentence is a Stage D/E question.
2. **Whether Stage C will keep `occurrences_outside_map = 0` and `hits_on_record = 0`.** Both are content obligations on bytes that do not exist at plan time (INFO-3, INFO-4). The criteria are satisfiable; satisfaction is not yet demonstrated and cannot be.
3. **F11's exact snapshot values at `2026-10-13T10:44:43-07:00`.** The archive is being written to continuously; my re-measurement is later by construction and reads `737,195 / 629,295`. I verified the **method and the mechanism**, not the historical digits — which is precisely how the revised F11 now presents itself.
4. **That Stage A read `change-classification-gate` in full**, unchanged from my first audit — there is no transcript; I verified the artifact's shape only.

---

## 6. Stage B skills row — re-audit round, verbatim for the publisher

*Label:* the skills row — in plain words, *the four-column table row recording which Aegis skill this stage read and how it used it*. A row bound to an older round cannot stand for a later one, so the re-audit round authors its own: this row binds **revision 2** (seal `2dfe2f5f…`). The two rows in `AUDIT-B.md` §7 remain the record for the round that bound revision 1 (seal `578010377…`).

**Fenced-block locator:** section 6 of this file, the fenced `markdown` block below.
**Row-block line range:** `L223-L226`.
**sha256 of those exact bytes** (the four lines inside that fence — header row, separator row and the two authored rows — joined by LF, plus one trailing LF): `11c68ae30094de95be57b006bbe221dee46f11b9023f75aa10bba4a184901485`.

```markdown
| Skill | Stage / agent | How applied | Result / evidence |
| --- | --- | --- | --- |
| [acceptance-criteria-reviewer](.claude/skills/acceptance-criteria-reviewer/SKILL.md) | Stage B re-audit / `wcd-stage-b` | Re-applied the three-part testability check to the revised criteria and - the point of this round - re-RAN each repaired criterion's own command instead of accepting a claim of repair: executed AC8's pattern over the four source files, executed AC10's fenced script verbatim, executed AC11's whitespace-normalised comparison against the revision, and re-measured the archive under the method F11 now states. No criterion was accepted on its prose. | AC1-AC11 each name an outcome, a threshold their own command prints, and that command; all seven defects D1-D7 plus the Lead-added AC9 repair confirmed repaired. AC8 prints 3 at exactly the three named lines; AC10's actual output matches its stated block line-for-line (pattern_len 371, POS 11/11, NEGATIVES_TOTAL 12 matched 0, CONTROL_FAILURES 0); AC11 finds 3 normalised occurrences against 1 raw, confirming its method; F11's filter measured at 737,195 / 629,295, a 99.9%-`.git` gap. Four INFO observations, no blocking defect. Evidence in AUDIT-B-rev2.md. |
| [source-of-truth-reconciler](.claude/skills/source-of-truth-reconciler/SKILL.md) | Stage B re-audit / `wcd-stage-b` | Its precedence discipline was applied again in this round - for the IS-question "how many files does the archive hold?" the disk outranks every stated figure - but its SKILL.md was **not re-read** in this round, so this row claims the previous round's reading (AUDIT-B.md, L1-L70) and the application, not a fresh read. Stated so the row is not an over-claim. | The plan's snapshot 737,179 / 629,280 and my later 737,195 / 629,295 are the same pair of counts, +16 files each; the mechanism the plan states (the hidden/system filter) is confirmed at 107,797 of a 107,900 gap. INFO-1. |
```

**No other Aegis `SKILL.md` was read in this round.** As in the first audit, the plan-level `SD-B` verdict itself has **no owning skill** — `docs/delivery-workflow.md:98` says so in the repository's own words — so the publisher records that **ABSENCE row** for Stage B alongside these rows.

---

## 7. Boundaries and non-claims

- **Independence.** I am the different agent that wrote the REVISE; this round tests my own defects against the revision, which is the cycle's design. Nothing was accepted on Stage A's word.
- **Read-only.** No repository write, commit, push, branch, pull request, comment, label or other GitHub write. Network use was limited to the clone and read-only `git` / `gh` reads inherited from the first audit; this round added no network call. This file is my only write.
- **Boundaries respected.** `clone-pq1`, `clone-pq2`, the legacy checkout `C:/src/Project Aegis/Project-Aegis`, every `wt-*` worktree, the paused virtual machine and the WSL distro were not touched. No subagents; nothing delegated.
- **This file grants nothing.** It is a stage verdict, not an approval, authorization or merge. **New authority: None.** It does not decide whether the change is done, ready to merge or ready to release.
- **Plain-English rule.** Every label, ID and identifier above carries a one-line plain-English description in the same item, per the owner's permanent reporting rule (`AGENTS.md`, 2026-10-13).

---

**(Re-audit ends. Written by `wcd-stage-b` — the Stage B independent plan auditor for the workspace-citation durability lane — on 2026-10-13. It accepts revision 2 of the plan at seal `2dfe2f5fa682861e1110891d4345486d8f1926668cccd0dba1a232ada7702e0a`.)**

<!-- sha256 footer: the hash below covers this file's bytes with the digest line's value replaced by the
     literal placeholder {{SHA256}}, so the digest is stable and independently reproducible.
     Verify by replacing the 64 hex characters on the line beginning "sha256:" with {{SHA256}}, then
     hashing the UTF-8 bytes including the final newline. Line endings are LF only. -->
sha256: 03e7be7c85ac159bb1e2fbcd0c1f0262f3feaf95967290ba066560a9b86acdb8
