# Workspace-citation durability — Stage B independent plan audit

**Item:** "Workspace-citation durability — Stage B independent plan audit" — in plain words, *the independent re-derivation of the Stage A plan that decides whether that plan is fit to implement, performed by an agent that did not write it*.

**Agent:** `wcd-stage-b` — in plain words, *the Stage B auditor, a different agent from `wcd-stage-a` which wrote the plan*. No subagents were used; nothing was delegated. Read-only against the repository and GitHub; this file is my only write.

**Stage:** B — INDEPENDENT PLAN AUDIT, in the repository's seven-stage delivery workflow (`docs/delivery-workflow.md`): A PLAN → B INDEPENDENT PLAN AUDIT → C IMPLEMENT → D INDEPENDENT IMPLEMENTATION AUDIT → E VALIDATE → F FINAL INDEPENDENT PR CODE REVIEW → G MERGE.

**Audited object — the captured revision this verdict binds:** `_resume-2026-10-09/evidence/workspace-citation-durability-2026-10-13/PLAN.md` — in plain words, *the Stage A plan*, 566 lines, 63,393 bytes, LF only, final newline present.

- Whole-file sha256: `7a298545c53337d800343650dd6b2a9288ac49a037e66c13dbcdda75979f32a6` — in plain words, *the digest `Get-FileHash` reproduces from the file on disk, footer included*.
- The plan's own footer seal, recomputed by me: `578010377ca538e3454b48eb67aa854fb29b5dfe7127ae8019f44f83cf1e8d68` — in plain words, *the digest the plan claims for itself, over its bytes with the digest value replaced by the literal `{{SHA256}}`*. **MATCHES the claim.** Any later edit to the plan voids this audit.

**Verdict: `SD-B: REVISE`** — in plain words, *the plan's design is sound and I verified its load-bearing facts myself, but five of its own claims do not reproduce, and two acceptance criteria cannot pass or be measured by the commands the plan prescribes for them; those must be repaired before Stage C implements.* Detail in §2 and §3.

**Timing.** Start `2026-10-13T10:25:32-07:00` (the stamp sampled at this item's first action). Finish `2026-10-13T10:41:36-07:00`. Wall time `16 min` (harness clock, start to this write). ETA at start: **not stated** — my brief carried no estimated active-work duration, and none is invented here. Active time was not separately instrumented, so the ETA-versus-wall comparison is **IMPERFECT** and, with no ETA on record, **not applicable** rather than "met".

> **Independent-verdict marker.** `SD-B` is the plan-audit stage; `REVISE` is the workflow's own word for this disposition (`docs/delivery-workflow.md:178`). This file uses only the workflow's own verdict words for this stage - `ACCEPT` or `REVISE` - and no other.

---

## 1. Method — and the verifier validation this brief demanded

I created my own fresh HTTPS clone at `C:/src/Project Aegis/_resume-2026-10-09/_wcd-b-clone` (`git -c http.sslBackend=openssl clone --no-hardlinks https://github.com/ModernNomad-98/Project-Aegis.git`), which landed on `dbe2ee28559fef88950b2d8822cf72d3e595ba86`; `git status --porcelain` returned 0 lines, and `git -c http.sslBackend=openssl ls-remote origin refs/heads/main` returned the same commit. Every repository fact below is read from that clone at that revision; every archive fact is read from `C:/src/Project Aegis/_resume-2026-10-09/` on disk.

**The footer verifier was validated before it was used to accuse anything.** The two conventions in play here are different, and the brief warns that a false seal failure was asserted earlier in this session by skipping this step:

1. **The placeholder convention** — used by this lane's evidence files: replace the 64-hex value on the whole line beginning `sha256:` with the literal `{{SHA256}}`, then sha256 the UTF-8 bytes including the final newline, LF only.
2. **The `HASH-BOUNDARY` convention** — used by the older `evidence/p0/` artifacts: sha256 every byte *above* the line `<!-- HASH-BOUNDARY: ... -->`.

Both were validated against **known-good artifacts whose digests were already accepted**, before being pointed at anything:

```text
placeholder verifier:
  OF1-DISCHARGE-AUDIT-B.md      claimed a17f1ecdbe37465fa71830e2ea3c988e92c2249bf84e25e7d7af50741e5b626f  recomputed a17f1ecd...b626f  MATCH
  FU3-RECORD-FINAL-REVIEW-F.md  claimed 8f554598a04d91567fbb10e301d1a8bc1e0c2940b2a82fb8a5bac4be9258937b  recomputed same  MATCH
  FU3-RECORD-stage-g-summary.md claimed 059822aabffb13cb417adcd1714bb00a90244c0df040a457db7ba9ac895bb2d7  recomputed same  MATCH
HASH-BOUNDARY verifier:
  evidence/p0/P0A-A1-PLAN.md     claimed 4cdc03d5fe0d67e111f83ce4e6469fa0e136a650ccc284db821179f3e28b9a0b  recomputed same  MATCH
  evidence/p0/P0A-A1-AUDIT-B.md  claimed 1ab348270d0dc25cac71365e5f36b2142fecf0fbb446d9729fc741140ed4553e  recomputed same  MATCH
```

**This mattered immediately.** `docs/roadmaps/aegis-ci-baseline-2026-10-11.md` L43–L49 cites those two `p0` files by sha256, and a naive whole-file `Get-FileHash` on them returns `83f36c49...` and `6bb5b88f...` — a mismatch that would have produced two false accusations. Under the boundary convention the cited digests recompute exactly, so **the citations are correct and I report no defect there.**

---

## 2. Verdict

**`SD-B: REVISE`** (the workflow's vocabulary; `docs/delivery-workflow.md:178`).

**What is right — and it is most of the plan.** I re-derived the plan's load-bearing facts and they hold: the archive sits outside every git repository; the citation census (10 occurrences, 4 files, 9 distinct targets, all present, none tracked) is exact; the citations are accurate at the lines they name; the frozen O-F1 note hashes to `f29decc7…182d` over exactly L4149–L4190; the log's `L2672–L2675` rule says what the plan says it says; the evidence index's figure really does live at **three** live sites, not one; the table really does have 16 rows; the `gate_pattern` really does return NOMATCH on all eight declared paths; precedent `503c3b30` really did what the plan says; and the proposed governance-log anchor `#9---------the-carried-open-publication-item` (nine hyphens) really is in the repository's own checker's anchor set while the plan's first guess really is dead. §4 lists each with its command.

**Why REVISE nevertheless.** Two of the plan's ten acceptance criteria cannot pass or be measured by the commands the plan itself prescribes (D1, D2) — and a criterion that cannot be measured is the exact failure the workflow's `SD-D` rule turns on, because an `UNRUN` that Stage A did not declare forces `REVISE` downstream anyway. Three further claims do not reproduce against the artifact (D3, D4, D5), and two smaller precision items are recorded (D6, D7). None of the seven changes the change's scope, its class, its security answer, its anchor, or the frozen note's protection; all seven are repairs to the plan's text.

**None of the defects is a scope or authority defect.** The plan's three scope decisions — publish the four FU-3 records, supersede via a new appended entry, owe the other seven citations — I tested and found justified, correctly bounded, and safe (§6).

---

## 3. Defects

Severity is my own: **HIGH** would mean the change is unsafe or unjustified; **MEDIUM** means a claim or criterion fails its own test and must be repaired before the change can be validated; **LOW** means an inaccurate or imprecise statement with no downstream threshold; **INFO** is a precision note.

### D1 — MEDIUM — AC8's threshold cannot be met by AC8's own command

*Label:* `AC8` — in plain words, *the acceptance criterion that says the published pages carry no credential material*.

**The claim (plan §8, AC8):** "**exactly 3 hits** for the account-id-shaped pattern, each on a named benign line — a GitHub Actions job id, a provider price line, and a sha256 table row"; and §14 F16 repeats "**3 hits** across the 4 files … a provider price line (matched `token =`)".

**Command** (AC8's own pattern, applied to the four files it names):

```powershell
$pat='AKIA[0-9A-Z]{16}|BEGIN [A-Z ]*PRIVATE KEY|gh[pousr]_[A-Za-z0-9]{20,}|arn:aws|'
$pat+='[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+[.][A-Za-z]{2,}|password *[:=]|secret *[:=]|[0-9]{12}'
Get-ChildItem <archive>/evidence/docs-refresh-2026-10-12/*.md |
  Where-Object { $_.Name -in $four } | Select-String -Pattern $pat
```

**Observed output:**

```text
FU3-RECORD-FINAL-REVIEW-F.md:121: ... `validate-skills` job 115364466965 failed **step 20 `pr-body-skills-check`** ...
REVIEWPATH-FINAL-REVIEW-F.md:47: | `REVIEWPATH-VALIDATE-E.md` ... | `9dfc47f8...1c74887` | 25,115 / 164 | yes |
total hits = 2
```

Counting regex matches rather than lines gives the same answer — `[0-9]{12}` yields **2** matches in total (`115364466965`, and `013569599029` inside the sha256):

```text
BER-G3-FU3-EXECUTION.md : MATCHES = 0
FU3-RECORD-FINAL-REVIEW-F.md : MATCHES = 1   -> 115364466965
FU3-RECORD-stage-g-summary.md : MATCHES = 0
REVIEWPATH-FINAL-REVIEW-F.md : MATCHES = 1   -> 013569599029
TOTAL [0-9]{12} matches over the 4 files = 2
```

**The third named line cannot be produced by the prescribed pattern.** The "provider price line" is `BER-G3-FU3-EXECUTION.md:155` (`input \`5,000\` nano-USD/token = **$5.00 / 1M**`). It contains no twelve-digit run, and AC8's pattern has **no `token` alternative** — so the `token =` match the plan's F16 describes comes from a pattern AC8 does not prescribe. The other half of AC8 ("**0 hits** for AWS access keys, private keys, GitHub tokens, emails, `password=`/`secret=`") **is** reproducible: I measured 0.

**Impact.** AC8 as written cannot pass. A Stage D or E validator running AC8's own command gets 2 and must either record `NOT MET` — which forces `REVISE` at `SD-D` — or substitute a different count, which is the defect class the workflow names. The security substance (no credential material enters the repository) is **not** in doubt; the criterion's arithmetic is.

**Repair (local, no scope change):** set the threshold to the measured 2, or add the `token *[:=]` alternative and re-measure; and name the line each hit falls on.

### D2 — MEDIUM — AC10's threshold is not measured by AC10's own command

*Label:* `AC10` — in plain words, *the acceptance criterion that proves the change touches no protected path*.

**The claim (plan §8, AC10):** threshold "**0 of 8 planned paths match; 11 of 11 positive controls match; 0 control failures**". §3 states "11/11 documented positive controls matching and **12/12 negatives** not matching". §14 F15 repeats "11 of 11 positive controls". The plan names its 11 positives and 12 negatives **nowhere**.

**Command:** AC10's prescribed Python script, run verbatim at `dbe2ee28`.

**Observed output:**

```text
pattern_len 371
POS entries: 8  NEG entries: 6
positive failures []
planned-path matches []
extra planned-path matches []
ALL 8 declared paths matching = [] (count 0 of 8)
```

**The script enumerates 8 positives and 6 negatives, and prints no counts at all** — only two failure lists. It cannot produce "11 of 11", cannot produce "12/12 negatives", and its `NEG` list contains `docs/x.py`, which is not one of the eight declared paths, while four of the five new files are absent from it. The substantive result **is** confirmed: I extended the test to all eight declared paths (`docs/evidence/README.md`, `docs/README.md`, `docs/roadmaps/behavioral-eval-runner-backlog.md`, and all five under `docs/evidence/fu3-record-publication-2026-10-13/`) and measured **0 of 8 matching**, with all 8 enumerated positives matching and the pattern 371 characters long.

**Impact.** AC10 cannot be validated as stated. The criterion's number and its command disagree.

**Repair:** make the script print `len(POS)`, the match count and the NEG count, enumerate all eight declared paths and the full positive/negative control sets, and set the threshold to the numbers the script actually prints.

### D3 — MEDIUM — F11's archive figure does not reproduce from the method F11 states, and the stated cause of the gap is wrong

*Label:* `F11` — in plain words, *the plan's measurement of how many files the archive holds*.

**The claim (plan §14, F11; used in §2 and §5.1):** "**629,224 files** (30.7 s) … This stage's count used `.NET Directory.EnumerateFiles` with `IgnoreInaccessible=true`, so it is a **lower bound** if any subtree was unreadable." The plan contrasts this with the brief's 721,463 and says the difference is "stated, not reconciled silently".

**Command and observed output** (the stated method, and the same method with the hidden/`.git` filter made explicit):

```text
$opt=[System.IO.EnumerationOptions]::new(); $opt.IgnoreInaccessible=$true
$opt.RecurseSubdirectories=$true; $opt.AttributesToSkip=[System.IO.FileAttributes]::None
EnumerateFiles(root,'*',$opt)                          -> 737,158 files   (23.7 s)
same enumeration, counting paths matching \\.git\\    -> 107,795
same enumeration excluding those                      -> 629,363 files
```

**Reconciliation — which the plan says it could not make.** The plan's 629,224 is reproducible not as "the archive's size" but as **the archive's size excluding paths under a `.git` directory** (my re-derivation: 629,363; the ~139-file difference is growth between the two measurements, since agents are writing into the archive continuously). The brief's 721,463 and my 737,158 both count everything. **The gap is the `.git` subtrees, not inaccessible files** — the plan's explanation is unsupported, and the label "lower bound" is a mischaracterisation of what was actually counted (`EnumerationOptions` defaults to skipping hidden and system entries, which is what excludes `.git`; the plan does not say it set `AttributesToSkip`).

**Impact — and the part that is safe.** I checked every use of the figure: §5.1's rejected option ("publish the whole archive"), §9 Q5's comparison, and §2's statement. **No acceptance criterion and no scope decision depends on the exact value**, which is what makes the decision safe: 629,224 and 737,158 both make committing the archive non-viable, and the plan itself calls the number unsettled. But the figure as written is presented as a measurement with a command attached, and it is not reproducible from that command.

**Repair:** state the filter (`AttributesToSkip` = hidden/system, i.e. excluding `.git`), quote the number as "files excluding version-control internals", and record that the brief's larger figure counted the `.git` trees.

### D4 — LOW — §7.4 claims the rule is "used verbatim in all three places"; the plan's own §7.3 entry is a paraphrase

*Label:* `§7.4` — in plain words, *the section that says where the new citation-durability rule is stated*.

**The claim (§7.4, L247):** "The rule text is fixed once and **used verbatim in all three places**, so there is one rule and not three paraphrases:" — the three places listed include "**The section-13 entry of §7.3**".

**Observed:** the §7.4 block opens "A permanent record here — a governance log entry, a register entry, a dated evidence page or a roadmap fact — supports each claim …"; the §7.3 entry's rule bullet opens "a permanent repository record must support each claim …". Beyond the opening, the clause order differs, §7.4's second paragraph ("This is a documented rule, not a machine-enforced one …") appears in none of §7.3, and the §7.3 bullet adds a sentence §7.4 lacks ("… and it is never a substitute for publishing an artifact that could have been published"). **They are paraphrases of one another, not one text used in three places.**

**Impact.** Low: the *substance* — one rule — is preserved in all three, and no threshold or decision turns on the wording. But the sentence is a factual claim about the plan's own prescribed text, and it is false as written; a Stage D auditor testing "one rule, not three paraphrases" will find three.

**Repair:** either quote the §7.4 block inside the §7.3 entry verbatim, or change §7.4 to say the rule's *substance* is stated in three places, with the log entry's wording being the governance-log form.

### D5 — LOW — §9 Q5's byte figure contradicts the plan's own per-file counts

*Label:* `§9 Q5` — in plain words, *the plan's answer to the fifth necessity question, on why the machinery is warranted*.

**The claim (§9 Q5, L443):** "… it leaves the evidence permanently unretrievable when publishing it costs **105,860 bytes**".

**Command and observed output:**

```text
BER-G3-FU3-EXECUTION.md        = 25606
FU3-RECORD-FINAL-REVIEW-F.md   = 30777
FU3-RECORD-stage-g-summary.md  = 25454
REVIEWPATH-FINAL-REVIEW-F.md   = 21023
SUM = 102860   (plan section 9 Q5 says 105,860)
```

The plan's own §4.2 lists exactly these four byte counts, so the plan contradicts itself by 3,000 bytes. **Impact:** LOW — a justification figure, used by no threshold. **Repair:** 102,860.

### D6 — LOW — two dated records that state the evidence index's figure as 15 are not named among the excluded figure sites

*Label:* `§3 / F8` — in plain words, *the plan's list of places that state the evidence index's page count*.

**The claim (§3, L65 and §14 F8):** the figure lives at three live sites, and "Other `16`-bearing lines … are **dated measurements of a different set** and are not touched."

**Observed:** the three live sites are confirmed exactly (see V6). But two further lines state a figure for **the same artifact**, and neither is `16`-bearing, so the plan's stated reason does not cover them:

```text
docs/roadmaps/aegis-execution-metrics.md:2334:  The evidence index covers 15 selected records; the five follow-up reading
docs/roadmaps/aegis-documentation-readability-backlog.md:3188: | ... | Indexed 15 selected decision/delivery records and corrected ... |
```

Both sit inside **dated** entries (L2334 belongs to the PR #186 closeout measuring `d5b007b0`; L3188 is the PR #184 row in the readability ledger), so excluding them is the right call under this repository's convention that a dated record reports what was true at its date. **Impact:** LOW — no correction is needed. **Repair:** one sentence in §3 naming these two and saying they are dated records, so the exclusion reads as decided rather than missed.

### D7 — INFO — §7.2's "changing 2 lines" undercounts what the precedent changed

*Label:* `§7.2` — in plain words, *the section that copies the precedent's index shape*.

**The claim (§7.2, L191):** commit `503c3b30` "added exactly one row and moved the figure from 15 to 16, **changing 2 lines**".

**Observed:** `git show --stat 503c3b30` reports `docs/evidence/README.md | 5 +-`, and the diff is **3 insertions and 2 deletions** — one new table row plus two figure lines (L3 and the closing "these 15 pages" sentence). Under the reading "two *figure* lines" the sentence is accurate; as written it reads as the file's changed-line count. **Impact:** INFO, no threshold. **Repair:** "…and moved the figure from 15 to 16 on its two figure lines."

---

## 4. Claims I re-derived and found correct

Each row: the plan's claim, my command, and what I observed. These are the claims that carry the change.

| # | Plan claim | My command | Observed |
| --- | --- | --- | --- |
| V1 | The workspace root is not a repository; the archive is outside every repository | `Test-Path 'C:/src/Project Aegis/.git'`; `'C:/src/.git'`; `'C:/.git'` | `False`, `False`, `False`. The only repo nearby is the legacy checkout `Project-Aegis/`. The archive is **not gitignored — it is simply in no repository**, exactly as the plan says. |
| V2 | 10 citation occurrences, 4 files, 9 distinct paths, all present, none tracked | `git grep -n -I '_resume-2026-10-09'` | 10 lines: backlog 4, ci-baseline 3, SCIF page 2, approval register 1. 9 distinct paths; all 9 exist on disk; `git ls-files` membership = 0. |
| V3 | Precedent `503c3b30` created one new evidence page, added one index row and moved the figure 15 → 16 | `git show --stat 503c3b30`; `git show 503c3b30 -- docs/evidence/README.md` | `M docs/evidence/README.md`, `A docs/evidence/scif/scif-closeout-corrections-2026-10-11.md`, `M docs/reconciliation/step-0-reconciliation-v4.md`; README `-15 selected` → `+16 selected`, `these 15 pages` → `these 16 pages`, one row added. It did **not** publish the cited artifact. |
| V4 | The frozen O-F1 note is L4149–L4190 and hashes to `f29decc7…182d` | sha256 of those 42 lines, LF, trailing newline | 3,840 bytes, 42 lines, `f29decc72f1ee1b31d410ead380ce55c46081e2890d004947d9e4a43e00b182d` — **exact match**. |
| V5 | The log's rule L2672–L2675 forbids editing; the anchor is between L4191 and L4192 | `git show HEAD:docs/roadmaps/behavioral-eval-runner-backlog.md` | L2672–L2675 reads "entries are **never edited or deleted**; corrections append a superseding entry that names the entry it supersedes". Section 13 spans L2670–L4191; `## 14.` is at **L4192**; L4191 is blank. The anchor is right. |
| V6 | The figure `16` has **three** live sites, not one | `git grep -n -I -E '(^|[^0-9])16 (selected\|dated\|pages)'`; `git grep -n 'these 1[0-9] pages'` | Exactly three: `docs/evidence/README.md:3` (`16 selected`), `:49` (`these 16 pages`), `docs/README.md:59` (`routes to 16 dated decision and`). **No fourth live site.** (Two dated 15-figures are D6.) |
| V7 | The index table has 16 rows at base | AC5's own regex: `(Select-String docs/evidence/README.md -Pattern '^\| .*\]\(').Count` | `16`. So 17 after one row is added. |
| V8 | `gate_pattern` is 371 chars and NOMATCHes all 8 planned paths | AC10's script | `pattern_len 371`; `0 of 8` declared paths match; all 8 enumerated positives match; `positive failures []`. |
| V9 | The Stage G anchor is `#9---------the-carried-open-publication-item` (nine hyphens), and the first guess is dead | the repository's own `slugify`/`Document` and `scripts/ci/check-markdown-links.py` | The file's anchor set contains `9---------the-carried-open-publication-item` — **nine hyphens, counted**. A probe file carrying the entry's four links: `links checked: 4  anchors checked: 2  broken: 0  dead: 0`, **exit 0**. Replacing the fragment with the plan's first guess: `DEAD ANCHOR … #9-o-f1--the-carried-open-publication-item`, **exit 1**. |
| V10 | Three of the four published files carry self-digests that recompute; the fourth carries a body digest | validated `{{SHA256}}` verifier | `BER-G3-FU3-EXECUTION.md` `f5a6b9ca…` OK; `FU3-RECORD-FINAL-REVIEW-F.md` `8f554598…` OK; `FU3-RECORD-stage-g-summary.md` `059822aa…` OK; `REVIEWPATH-FINAL-REVIEW-F.md` has **no** whole-line `sha256:` footer (body-digest file), exactly as §7.1 says. |
| V11 | §10's Stage A row-block digest | sha256 of plan L456–L459 joined by LF + trailing LF | `08cb06e42db7ca83078c5d2d793f161e28c40862d07bbd896f64cc2d34a3051f` — **matches the plan's claim**, over the header row, separator row and the two authored rows (4 lines, the block the publisher must copy). |
| V12 | Corpus counts 714 / 658 / 56, CI floor 600 | `git ls-files '*.md'` with the workflow's own fixtures filter; workflow L230 | 714 tracked `.md`, 56 under `scripts/tests/fixtures/`, 658 checked; the workflow's floor is `-lt 600`. |
| V13 | Archive directory counts 476 and 88 | `os.walk` per directory | `evidence/docs-refresh-2026-10-12` = **476**; `evidence/p0` = **88**. Exact. |
| V14 | All 9 cited files are LF-only; `.gitattributes` is `* text=auto eol=lf` | byte scan for `\r\n`; `git show HEAD:.gitattributes` | 9 of 9 have **0** CRLF pairs; `.gitattributes` contains `* text=auto eol=lf`. |
| V15 | No tracked file cites a line ≥ L4192 in the backlog | `git grep -n -E 'behavioral-eval-runner-backlog\.md.*(L\|:)4[1-9][0-9][0-9]'` | Empty — the appended entry's shift is safe, as F9 claims. |
| V16 | No written rule mentions the archive; `.gitignore` has 6 patterns touching neither `docs/` nor `evidence/` | consequence of V2; `git show HEAD:.gitignore` | Only the 4 files at V2 match; `.gitignore` patterns are `.private-calibration-inputs/`, `__pycache__/`, `*.pyc`, `/.aegis-control-plane/`, `/.worktrees/`, `artifacts/tmp-*`. |
| V17 | §11(b) reflects the workflow's own words | `docs/delivery-workflow.md` L97–L103 | L97 "**No skill was found that owns writing a single change's plan**"; L98 the `acceptance-criteria-reviewer` partial fit and "never decides whether work is done"; L99 "**No skill was found that owns general implementation**" and `reviewable-diff-discipline` *(MANUAL-ONLY)*; L101 `risk-tiered-validation-selector` "**selects** a tier only". The plan's table is a faithful reading. |
| V18 | `reviewable-diff-discipline` is MANUAL-ONLY and must not be auto-applied | frontmatter `description:` of that `SKILL.md` | Contains the **MANUAL-ONLY** sentinel. `agent-authorization-matrix` likewise. `code-reviewer`, `change-classification-gate`, `docs-retention-index` are not manual-only. |
| V19 | F14: finding `4261109123` is real, P2, at backlog L4162, review `5506577448`, written at `e0a026e2…` | `gh api repos/ModernNomad-98/Project-Aegis/pulls/765/comments`; `.../reviews` | Read **live**: id `4261109123`, `path docs/roadmaps/behavioral-eval-runner-backlog.md`, `line 4162`, user `chatgpt-codex-connector[bot]`, `original_commit_id e0a026e2843e299d02180d31d7202a3598759a94`, created `2026-10-13T16:12:08Z`, title "Publish the evidence cited by the permanent log". The second finding `4261109109` is at L4188 and is "Do not close a mandatory Stage F failure by logging it". Review `5506577448`, state `COMMENTED`, submitted `2026-10-13T16:12:07Z`. Every field the plan states is exact. |
| V20 | Stage A wrote nothing to the repository | read-only `git -C _wcd-a-clone status --porcelain`, `git diff --cached --stat`, `git rev-parse HEAD` | HEAD `dbe2ee28…`, branch `main`, **0** porcelain lines, **0** staged lines. §4.1's claim holds. |

### On "staged bytes are the intended bytes"

At this revision there are **no staged bytes anywhere to verify**: Stage A's clone is clean at the base commit with an empty index, my own clone is clean (`git status --porcelain` → 0 lines), and Stage A made no repository write. The byte-identity obligation in this change is **AC1** — the four published copies must hash equal to their archive sources — and it can only be discharged after Stage C commits them. I record it as **not yet applicable at Stage B**, not as verified.

---

## 5. Acceptance-criteria review — skill `acceptance-criteria-reviewer`

*Label:* `acceptance-criteria-reviewer` — in plain words, *the Aegis skill that checks whether acceptance criteria can actually be verified: each must name an observable outcome, a pass/fail threshold and the evidence that proves it*. It is the skill I read in full and applied. Its verdicts are `TESTABLE`, `NEEDS-REWRITE` or `UNTESTABLE`, and by its own contract it never decides whether work is done — so it shapes the findings above and not the stage verdict.

| AC | What it asserts | Verdict | Why |
| --- | --- | --- | --- |
| AC1 | The four copies are byte-identical to their archive sources | **TESTABLE** | Outcome (per-file digest equality), threshold (4 of 4), command (paired `Get-FileHash`) all present; I confirmed the four source digests recompute. |
| AC2 | The copies' own integrity claims still hold | **TESTABLE** | Names three footers and the body digest, with a validated verifier and a negative control; I confirmed all three footers and the body-digest design against the real files. |
| AC3 | Every added link and heading fragment resolves | **TESTABLE** | Exit 0 / broken 0 / dead 0 / anchors ≥ 4 against the repository's own checker; I reproduced the checker's behaviour on the entry's links (V9). |
| AC4 | The corpus-wide CI link check is still green | **TESTABLE** | Batched command, exit-code threshold, count 663 against CI's floor 600; counts verified (V12). |
| AC5 | The stated count equals the measured row count at every site | **TESTABLE** | Four numbers must read 17; the base count verified at 16 with the criterion's own regex (V7). |
| AC6 | The log is append-only and the frozen range is byte-unchanged | **TESTABLE** | `--numstat` deletions 0, plus a byte-range comparison; the range arithmetic (L4149–L4190) is correct (V4). |
| AC7 | The diff is exactly the declared file set | **TESTABLE** | 5 A + 3 M = 8 paths, 3 deletions, each containing 17. |
| AC8 | No credential material enters the repository | **NEEDS-REWRITE** | Threshold says 3 hits; the prescribed pattern yields **2**, and one of its three named benign lines cannot match that pattern. **Defect D1.** |
| AC9 | A fresh checkout can retrieve the evidence | **TESTABLE** | Fresh clone, four digests, three anchors, zero `_resume-2026-10-09` references on the retrieval path. |
| AC10 | No protected path is touched, proven with controls | **NEEDS-REWRITE** | Threshold says 11 positives and 12 negatives; the prescribed script enumerates 8 and 6 and prints neither count. **Defect D2.** |

**Completeness classes the skill asks me to check.** Negative, boundary, permission and error classes: the plan covers the *negative* class well (a ninth path or an extra deletion forces reclassification; a dead anchor is probed for; a flipped-byte negative control on the verifier). *Boundary* is covered by the corpus count against CI's 600 floor. *Permission* and *error* are largely not applicable — the change grants no authority and adds no runtime behaviour — and the plan states that as a non-claim (§12) rather than leaving it implicit. I record no GAP.

---

## 6. The five necessity-and-reuse answers — per-question routing disposition (`SD-B` requires this)

*Label:* the five questions — in plain words, *the standing check that a change is necessary, reuses what exists, respects ownership, is the smallest safe action, and is not over-built*. `SD-B` must record one routing disposition per question before it may `ACCEPT`. My dispositions are recorded even though my verdict is `REVISE`, because they are what the next revision should preserve.

| Q | Plan's routing | My disposition | Evidence |
| --- | --- | --- | --- |
| 1 Necessity | satisfied → cite the proof | **cite** | The proof is real and I read it live: finding `4261109123`, P2, at backlog L4162, on review `5506577448` (V19). The wider census (V2) is exact. |
| 2 Reuse | owned elsewhere → preserve that ownership and cite it | **preserve** | All four reused mechanisms exist and are the right ones: the dated evidence directory shape (six precedents), the one-row + figure-correction precedent (`503c3b30`, V3), the repository's own link checker (exists, runs in CI, floor 600 — V8/V12), and the log's own `L2672–L2675` supersede rule (V5). |
| 3 Ownership | owned → proceed inside existing authority | **preserve** | `docs-only` is an approval-free class; no declared path is protected (V8) and none is on `CONTRIBUTING.md` L238–L249 (which I read: the list covers `scripts/`, `.github/`, `AGENTS.md`, `.claude/agents/`, Claude/Git config, the protected-file guard's paths, `tools/`, pinned dependency files, `docs/approvals/APPROVAL_REGISTER.md`, `docs/skill-generation-standard.md` §5 and skill frontmatter — none of the eight). The register is **not** edited. |
| 4 Minimum-safe action | smallest change | **smallest change** | Eight paths, five new pages, one appended entry, three replaced count lines. Publishing the 4 cited files rather than all 9, or all ~629k–737k archive files, is the same principle. I tested the bound: the four files total 102,860 bytes (D5 corrects the plan's figure). |
| 5 Complexity justification | bounded check first — done, not deferred | **bounded check** | The plan's own probes are real and I re-ran the decisive ones: the anchor probe (V9), the digest verifier with its negative control (§1), the gate regex with its controls (V8). Two of its bounded checks, however, are the two I could not make measure what they claim (D1, D2). |

**Non-claim I verified rather than assumed.** The plan does **not** re-decide `O-F1`. The second Codex finding `4261109109` (whether a dated note may close a mandatory Stage F failure) is named as out of subject in §2 and §12, and the proposed §7.3 entry carries the same non-claim in its own Scope bullet ("It decides nothing about the separate O-F1 closure question raised as P2 finding `4261109109` … re-opens no gate … **New authority: None.**"). Verified against the live finding text (V19).

---

## 7. Stage B skills rows — verbatim, for the Stage C publisher

*Label:* the skills row — in plain words, *the four-column table row that records which Aegis skill this stage read and how it used it; `docs/delivery-workflow.md:182` requires a row for every stage that ran, and an explicit absence row where a stage read none*.

The two rows below are **self-authored by `wcd-stage-b`**, are a retrievable fixed source in this file, and are **not** to be paraphrased, repaired or re-authored by the publisher (`docs/delivery-workflow.md` L642–L699).

**Fenced-block locator:** section 7 of this file, the fenced `markdown` block below.
**Row-block line range:** `L285-L288`.
**sha256 of those exact bytes** (the four lines inside that fence — header row, separator row and the two authored rows — joined by LF, plus one trailing LF): `fd60199d6bdeb94f0c58814f6e3987cfad720baa5804cf40f179be1999e41b6d`.

```markdown
| Skill | Stage / agent | How applied | Result / evidence |
| --- | --- | --- | --- |
| [acceptance-criteria-reviewer](.claude/skills/acceptance-criteria-reviewer/SKILL.md) | Stage B / `wcd-stage-b` | Read in full (234 lines) and applied to the plan's ten acceptance criteria: quoted each verbatim without merging or dropping one, then ran the skill's three-part testability check - observable outcome, pass/fail threshold, evidence that will prove it - and assigned one verdict per criterion (TESTABLE / NEEDS-REWRITE / UNTESTABLE). By the skill's own contract it never decides whether the work is done, so this row informs the criterion findings below, never the stage verdict. | AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC9 and AC10 are TESTABLE with their commands and thresholds named and reproducible. AC8 is NEEDS-REWRITE: its threshold requires "exactly 3 hits for the account-id-shaped pattern" but its own prescribed pattern yields 2 matches (`115364466965` and `013569599029`), and one of its three named benign lines is unreachable by that pattern. AC10 is NEEDS-REWRITE: its threshold states "11 of 11 positive controls" and "12/12 negatives" while the prescribed script enumerates 8 positives and 6 negatives and prints neither count. Findings D1 and D2 of this audit. |
| [source-of-truth-reconciler](.claude/skills/source-of-truth-reconciler/SKILL.md) | Stage B / `wcd-stage-b` | Read the frontmatter, purpose, use-when, inputs and the workflow's precedence order (L1-L70 of 153) and applied precedence rule 2 - for an IS-question (how many files does the archive hold?) actual repository state outranks a figure asserted in an instruction - to the two places where the brief's numbers and the plan's numbers disagreed, recording each conflict with its evidence anchor instead of silently picking a side. | The brief's 721,463 and the plan's 629,224 were both re-derived on disk: `.NET Directory.EnumerateFiles` with `AttributesToSkip=None` counts 737,158 files; the same enumeration excluding paths under a `.git` directory counts 629,363. The gap is the `.git` subtrees, not inaccessible files as the plan's F11 states. Finding D3 of this audit; the plan's scope decision is unaffected because no acceptance criterion depends on the exact figure. |
```

**Skills read but NOT claimed.** None. I read no other Aegis `SKILL.md`. The plan's §11(b) predicts an **ABSENCE row** for the plan-level `SD-B` verdict itself — *in plain words, the fact that no Aegis skill owns a plan-audit verdict* — and that prediction is correct: `docs/delivery-workflow.md:98` says so in the repository's own words (V17). The publisher should record that absence row for Stage B **in addition to** the two rows above, and this file is the source for it: *Stage B's plan-level `ACCEPT`/`REVISE` verdict has no owning skill; the two rows above record the skills that were read and applied.*

---

## 8. What I could NOT verify

Reported as gaps, not filled:

1. **That Stage A actually read `change-classification-gate`'s `SKILL.md` "in full" and ran steps 1–6.** Unverifiable from any artifact — there is no transcript. I verified what is checkable: the skill exists, its workflow steps 1–6 exist, and the plan's `CHANGE CLASSIFICATION` block carries the shape that skill requires (deliverables, one class per deliverable, governing class, approval path, validation plan, scope contract).
2. **F13's exact totals, "links 11, anchors 4".** I reproduced the decisive behaviour — the entry's four links and both fragments resolve (exit 0), and the plan's first anchor guess is dead (exit 1) — but I could not reconstruct the full 11-link/4-anchor set, because the publication record's exact link set (a file the plan says Stage C will author) is not specified in the plan. The counts are unverified; the behaviour is verified.
3. **F11's exact figure at the instant Stage A measured it.** The archive is being written to by other agents while this lane runs; every count I make is a point-in-time observation (737,158 total; 629,363 excluding `.git`). I cannot recover Stage A's instant, and I say so rather than asserting its number is simply wrong. What I can say is that its *method description* does not produce its number, and I have reconciled the gap (D3).
4. **Whether Stage C will reach the same `docs-only` classification.** Future work. The plan correctly locks scope and requires Stage C to re-run the gate.
5. **The archive's byte-level contents beyond the four published files.** I verified the four files' existence, digests and integrity footers; I did not audit the truth of what those records report, and neither does this change (plan §12).
6. **`gh`-hosted CI state at any future head.** Not applicable at Stage B; the plan's AC4 is the check that covers it.

---

## 9. Boundaries, independence and non-claims

- **Independence.** I am a different agent from `wcd-stage-a`, the plan's author; I created my own clone and re-derived every fact above from the repository and the archive rather than reading the plan and agreeing with it. I did not read Stage A's report as a substitute for any measurement.
- **Read-only.** No repository write, no commit, no push, no branch, no pull request, no comment, no label, no GitHub write of any kind. The only network calls were the clone, `ls-remote`, and two authenticated `gh api` GETs for the PR #765 comments and reviews. This file is my only write; the plan itself was not edited.
- **Boundaries respected.** `clone-pq1`, `clone-pq2`, the legacy checkout `C:/src/Project Aegis/Project-Aegis`, every `wt-*` worktree, the paused virtual machine and the WSL distro were not touched. The local-path clone route and the MSYS `sh`/`bash` route were avoided as instructed; the clone was made over HTTPS with `-c http.sslBackend=openssl`. No subagents were used and nothing was delegated.
- **This file grants nothing.** It is a stage verdict, not an approval, authorization or merge. **New authority: None.** It does not decide whether the change is done, ready to merge or ready to release — that is `SD-D`, `SD-E`, `SD-F` and `SD-G`.
- **Plain-English rule.** Every label, ID and identifier above carries a one-line plain-English description in the same item, per the owner's permanent reporting rule (`AGENTS.md`, 2026-10-13).

---

**(Audit ends. Written by `wcd-stage-b` — the Stage B independent plan auditor for the workspace-citation durability lane — on 2026-10-13.)**

<!-- sha256 footer: the hash below covers this file's bytes with the digest line's value replaced by the
     literal placeholder {{SHA256}}, so the digest is stable and independently reproducible.
     Verify by replacing the 64 hex characters on the line beginning "sha256:" with {{SHA256}}, then
     hashing the UTF-8 bytes including the final newline. Line endings are LF only. -->
sha256: 5dca29f2ef063b7a74c8658d0bca8066cecfe884379570ae747f86206e27308d
