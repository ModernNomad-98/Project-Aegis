# Stage A plan — Phase 4 readability re-read, lane A, batch 1 (PR #771)

**This file is the captured Stage A plan for PR #771.** It is captured as a tracked file committed on
its own branch, so its revision is immutable and a Stage B auditor can bind the exact text. The
branch, the capturing commit and **this file's blob SHA of the captured revision** are recorded in the
PR #771 body, together with the id of a fresh issue comment on that PR carrying the same text
verbatim (a file cannot contain its own content hash).

**Revision 5 (2026-10-16) supersedes revisions 1, 2, 3 and 4 of this plan.** Superseded, immutable and
**not to be bound**: revision 1 is blob `ea048399f14dd13ed91c13ab6d1123dabe9c774b` (58,466 bytes, 727
lines) at capturing commit `462d786bf8803d5794c21a6cb0486ff03f5829d8`, held as issue comment
`6213972798`; revision 2 is blob `6d579cdca95663f0851ade204adc625d5f315658` (61,173 bytes, 747 lines)
at capturing commit `e3a4a19c0d048ece8b1121a0437613105bf19771`, held as comment `6214016914`; revision 3
is blob `c47b7d908e2beb75ce23940d5ccf19a2595571c2` (63,853 bytes, 775 lines) at capturing commit
`5f3384df0d9b58a78d1aac3bcbaf89c12689594b`, held as comment `6214392977`; revision 4 is blob
`324564cd03c589cc92b2d2f7f790b8317b69ac3b` (91,724 bytes, 1,122 newline-terminated lines) at capturing
commit `0cce5b33aada3a979795be915148ada0863b00c5`, parent `5f3384df`, held as comment `6215856084`.
**Stage B must bind the revision its own verdict names.**

**Why revision 4 exists.** The independent plan audit at comment `6215231275` (**SD-B**, the post-audit
verdict — plain English: the independent audit of this plan and the disposition it posted) returned
**REVISE** on revision 3, on a finding this revision fixes: revision 3's §14 bound head-stamped values
that the act of applying them falsifies — because the commit that writes them is the commit that moves
the head. Applied verbatim, as Stage C correctly did, the record publishes `689 added / 0 deleted`
where the head that publishes it measures **727**, and the PR body's validation rows 1, 2, 4, 13 and 16
state a superseded head, four commits where there are five, and `556 0` / `133 0` where the head
measures `576 0` / `151 0`. Revision 4 therefore: re-reads this plan's head binding to
`2e523622…`; restates §14 so that the head, the `base..head` diff scope, the commit count and the
sign-off count are bound as **a duty re-derived at the head the head-moving corrections produce** and
stated in **a final metadata pass that contains no further head-moving commit** (§14.0); binds the
§14.2b skills-row **insertion point** and a **recomputable post-insertion digest**; and corrects the
descriptive line ranges and the ref/commit/blob citations that the head movement made stale (§7, §10).
It re-verifies, at the new head, every figure the earlier audits accepted, and it records what it could
not verify (§12).

**Why revision 5 exists.** The independent plan audit at comment `6216259175` (**SD-B** — plain English:
the independent audit of this plan, and the disposition it posted) returned **REVISE** on revision 4:
one false re-measured value stated twice, and two further count corrections. All three are fixed here,
and each is **measured by command rather than carried** from the audit or from the brief (§12). (1) §12
called the ledger's consolidated keeper table "every row 8 columns" (L683) and "their 8-column shape"
(L707); it is **9 columns**, and §1 row 13, §5.2 criterion 7 and §12 now state that with the command
that measured it. (2) The record was called "576 newline-terminated lines" and the ledger "5,387
lines"; under this plan's own declared **newline-count** method they are **575** and **5,386**, because
the record's last line carries no LF and the ledger's does (§1 rows 12-13, §2, §10, §12). (3) §9's
residual inventory named two sentences; the sharp form sits at **six** sites across the record, the
ledger and this PR's body, with two further recording-act sites listed for completeness — **every site
enumerated** in §9. Revision 5 re-verifies at the unchanged head every figure the earlier audits
accepted, and it carries one change of its own that moves a bound field's digest: the §14.2b skills row
names **revision 5**, so that digest becomes `b78221cc2ae8f394` where revision 4 bound
`e6d9809812112231` — both values, and the single token that moved, are stated in §14.2b.

- **Planner:** DeepSeek-4.1-Flash (`deepseek-flash`), **Stage A only**. This planner is **not** the
  auditor of this plan and holds **no** Stage B, D, E, F or G on this change; it authored no keeper
  row, edited no file of the PR's diff, moved no head, and merged nothing.
- **Work item:** *Phase 4 readability full-page re-read — lane A, batch 1* — the work delivered by PR
  #771 (the eight keeper rows K-082..K-089 and the batch record they cite).
- **Head this plan plans against:** `2e5236222080dc6064df0b493ab83a8a94441176` (40 hex, re-derived
  by `git rev-parse refs/pull/771/head` at 2026-10-16T05:30-07:00), head tree
  `5758d7c95571d5dc33679a9c492b75fda77861fe`.
- **Base / merge base:** `e2a3e20b7c20ef8385b219b39c6405237163406f` (tree
  `effc72501297375d490705eaae686a0c181df2e6`); `git merge-base origin/main refs/pull/771/head`
  returns exactly it. This is also **the acceptance revision** — the revision every one of the eight
  keeper rows binds and at which the eight pages were read.
- **Stage context.** The PR's own skills table still records that **Stage A (plan author) and Stage B
  (plan auditor) rows are owed — no plan-author or plan-auditor record was produced for this lane's pass
  at any head** (body L131 at `2e523622`). This file is that Stage A output; its row is authored in
  §14.2b and is inserted, with the digest republication, by the final metadata pass. The PR is
  otherwise mid-repair: its four repair commits (`f6a4e418`, `7b010eea`, `0bd37e4d`, `2e523622`)
  answer one Stage F REVISE, one Stage D REVISE and a coordinator ruling, its Stage C corrections have
  landed, and a **fresh Stage B on this revision and a fresh Stage D at the head this revision's
  corrections produce** are owed.

## Glosses for the internal labels used below (one line each)

- **Stage A / SD-A** — the PLAN stage and its exit disposition: a written plan carrying what, why,
  blast radius, the paths, proportionate acceptance criteria, the change classification and the
  five-question answers.
- **Stage B / SD-B** — the INDEPENDENT PLAN AUDIT: a different agent audits this plan's captured text
  and records a per-question routing disposition before ACCEPT.
- **Stage C / D / E / F / G** — IMPLEMENT / INDEPENDENT IMPLEMENTATION AUDIT / VALIDATE / FINAL
  INDEPENDENT PR REVIEW / MERGE, each held by a different agent; this planner holds none of them.
- **Captured revision** — the immutable identity of a plan's exact text: a content hash taken as the
  text is captured, or an immutable comment holding it; editing the text afterwards voids an ACCEPT
  that named it.
- **Blob SHA** — git's content hash of one file's bytes; one changed byte changes it.
- **Bound field** — one of the three sentinel-delimited payloads in the PR #771 body (witness, skills,
  security) over which the body publishes a digest; text outside them is not covered by that digest.
- **Acceptance revision** — the 40-character revision a reader read and a keeper row binds.
- **Keeper row / ledger keeper** — one row of the ledger's consolidated acceptance table, and the
  distinct agent AEGIS-APR-101 permits to record it (a different agent from the page's author **and**
  its accepting reviewer).
- **AEGIS-APR-*nnn*** — an entry in `docs/approvals/APPROVAL_REGISTER.md`.
- **The convention screen (called "C-1" below)** — *a term used on about 12 or more of the 653 reader
  pages is a library-wide convention, so an unglossed first use of it is an OBSERVATION, not a gap, and
  may not make a page fail.* The label is only a label: **no tracked document in this tree defines a
  ruling named `C-1`** (measured in §7); the screen is authoritative here only by its content.
- **The next-batch rule (called "R2" below)** — a *different* rule: *the next batch is the next eight
  UNREAD pages in the unread sequence, re-measured at that batch's own implementation base and named
  by path — never a pinned index, never index arithmetic, never a pinned range.* Also a label only.
- **P1..P8** — this batch's eight read pages, in the record's own numbering.
- **Reader-page set** — the pages `check_index.py`'s own `classify_tree()` returns at a pinned ref:
  every tracked `.md` path except `scripts/**` (one fixture README excepted) and one generated audit
  report. At `e2a3e20b` it is **653** pages (measured: 719 `.md` − 65 fixtures − 1 report).
- **SD-D** — the Stage D implementation-audit verdict; **DCO** — the Developer Certificate of Origin
  commit sign-off; **PARTIAL / FULL** — a page accepted with a named gap / accepted unchanged.

---

## 1. The PR's state as re-derived by this planner (against the brief, not from it)

Every figure below was produced by a command in a fresh HTTPS clone by this planner on 2026-10-16,
between 05:30 and 05:45 America/Los_Angeles (`git clone -c http.sslBackend=openssl`; the shared clone
was **not** used or cleaned; no worktree was created; `git config user.name` was read first and is
`Peter Nguyen`). **Every count here is a measurement at the head named beside it and is re-runnable by
the command given; none is carried forward as a standing fact.** **Three places where what I measured
differs from the brief I was given, or from the PR's own bytes, are marked ⚠ and planned against as
found; all three were re-measured at revision 4's head and again at revision 5's (the head has not
moved between them), and two of them have changed since revision 3 because the Stage C commit landed.**

| # | Fact | Measured value |
| --- | --- | --- |
| 1 | Head | `2e5236222080dc6064df0b493ab83a8a94441176` — `refs/pull/771/head` and `refs/heads/docs/readability-lane-a-batch-1-20261015` both resolve to it (measured 2026-10-16T05:30-07:00) |
| 2 | Base = merge base | `e2a3e20b7c20ef8385b219b39c6405237163406f` (`git merge-base origin/main refs/pull/771/head`) |
| 3 | `main` at this reading | `38413563a843f030d3ac992b375b5db5528f2926` (advanced past the PR's base; the PR is CONFLICTING/DIRTY — not resolved here) |
| 4 | Commits in `base..head` | **5** (`09a7ee1c`, `f6a4e418`, `7b010eea`, `0bd37e4d`, `2e523622` — `git rev-list --count e2a3e20b..2e523622`) |
| 5 | Files in `base..head` | **2**, both Markdown under `docs/` |
| 6 | `git diff --shortstat` | `2 files changed, 727 insertions(+)` — insert-only |
| 7 | `git diff --numstat` | `576 0` batch record, `151 0` ledger; `576+151 = 727` |
| 8 | Raw patch, hand-counted | **729** lines beginning `+` (= 727 added + 2 `+++` file headers), **2** beginning `-` (both `---` headers), **3** hunks |
| 9 | DCO over `origin/main..head` | exit 0 — `OK: 5 commit(s) checked, all signed off or exempt` |
| 10 | `git diff --check` | exit 0, no output |
| 11 | Check runs / workflow runs at the head | **0 / 0** (the PR is DIRTY against `main`, so no `pull_request` run can build a merge commit) |
| 12 | Record blob at head | `49d677a9255925e9f3a91492996d81032c62e81c` — 47,345 bytes, **575** newline-terminated lines (**576** lines by splitting on LF: the last line ends `.` and carries no LF) |
| 13 | Ledger blob at head | `d27eada876c7a0ed61e7166e21c722d3fe29b7b0` — 499,791 bytes, **5,386** newline-terminated lines (the file ends with LF); consolidated table = **109** data rows (K 89 + L 10 + T 10), **9 columns per row**, 0 malformed, 0 duplicate IDs |
| 14 | Instrument at the base (`check_index.py --json --ref e2a3e20b`) | `653 / 57 / 4 / 586 / 0 / 0 / 6 / 596`; pending union (`586+4`) = **590**; quarters **148 / 148 / 148 / 146** |
| 15 | `build_index.py --ref 2e523622 --report` (full clone with `refs/pull/**`) | exit 0: `table_rows 109, events 109, full_page_acceptances 89, lost_commit_events 10, reader_pages_with_rows 76` |
| 16 | The eight pages' blob / lines / bytes at the base | all eight reproduce the record's and the body's figures **exactly** (table in §2) |
| 17 | PR body bound-field digest, recomputed from the live body by the body's own declared method | `4cd96b537eb398a1` (full `4cd96b537eb398a19bb8c2cd608b22f48c7695b29b21f74e30d4dc9580d748b0`), normalized lengths **1262 / 17182 / 40** — **exactly the published value**; the four sibling calibrations (`#783 3913683c686e6e71`, `#787 82ed906d2f228f0e`, `#792 88300e711714200a`, `#795 5fabf87b2df899e9`) reproduce exactly, each from its **own live body**, with line endings normalised after fetch |

**⚠ Difference 1 — the record's own diff-scope figure is false of the head that publishes it, and the
body's rows contradict each other.** Measured at `2e523622…` (2026-10-16, this planner): the **record**
(a file this PR adds) says, at its **L526-528**:

> `**Diff scopes, counted by hand (not by regex).** \`base..head\` is **insert-only**:`
> `**689 added / 0 deleted** over two file headers and three hunks …`

and the record contains **no** occurrence of `727`, `576` or `151` at all. The **body** carries the
same stale reading in its Paths paragraph (L76) and validation row 16, and its row 4 now repeats
`556 0` / `133 0` while naming the wrong head. The three scopes are all measured by command —
`git diff --numstat` at each range: `e2a3e20b..f6a4e418` = `334 0` + `111 0` = **445**;
`e2a3e20b..0bd37e4d` = `556 0` + `133 0` = **689**; `e2a3e20b..2e523622` = `576 0` + `151 0` =
**727**. So `689` is the figure for the **previous** head, and the record publishes it at a head that
measures **727** — the same statement-vs-measurement defect the Stage C repair existed to close, now
carrying a different wrong number. §14 binds the correction, and it binds it **as a duty**, because the
commit that applies it is the commit that moves the head (§14.0).

**⚠ Difference 2 — "its record is bound to `f6a4e418`" is not what the bytes show.** No keeper row,
and no part of the record, binds `f6a4e418`: all eight rows' **Acceptance revision** is
`e2a3e20b7c20ef8385b219b39c6405237163406f`, and `git grep -c f6a4e418 2e523622 -- docs/` (measured
2026-10-16) returns exactly one file — the record — with **5** mentions, none of them a row binding.
What binds `f6a4e418` is the **earlier Stage D REVISE** (issue comment 6209064290) and the record's own
section-9 digest claim (`b1acc2b2f5817fab` with payload lengths 1262 / 11819 / 40). The distinction
matters because §14's corrections must not be read as re-binding a row.

**⚠ Difference 3 — the record's next-batch list was not the first eight entries of the unread sequence
at the state its own section measures; that defect is corrected at the head this plan is written at.**
§7 re-derives it at `2e523622`: the eight paths the record named originally sit at lane-A sorted
indices **8..15**, which lane A **batch 2 has already read**; under the read set the record's own
cross-check asserts (indices 0..39), the first eight unread are indices **40..47**. Revision 3 bound a
labelling correction; the Stage C commit `2e523622` **applied it** in all three places (record
L339-355, ledger L5221-L5237, body L278-294), so the statement-vs-measurement defect is closed at this
head and §14.3 binds nothing further.

## 2. The work item and the exact scope, by path (element 1)

**The work item** is the Phase 4 full-page re-read of **lane A, batch 1**: eight reader pages read
whole at the acceptance revision, the eight full-page-acceptance keeper rows K-082..K-089 recorded for
them in the ledger, and one new tracked batch record holding the evidence those rows cite. The work is
**already implemented at this head**; what this plan adds is the Stage A artifact the workflow owed,
plus the corrections §14 binds for Stage C.

**The eight pages in scope (read-only — none may be edited by this PR), measured at the acceptance
revision `e2a3e20b` by `git cat-file -s` / newline count / `git rev-parse`:**

| # | Page (path) | Lines | Bytes | Blob SHA at the acceptance revision |
| --- | --- | ---: | ---: | --- |
| P1 | `.claude/agents/ai-security-red-team-reviewer.md` | 33 | 2,055 | `447d20b2083b5f07113061a7cbe6a1092e121357` |
| P2 | `.claude/agents/full-codebase-auditor.md` | 30 | 1,611 | `e15ffa02533e8e63a76bb5c1248e28d53b6f3a70` |
| P3 | `.claude/agents/principal-architecture-reviewer.md` | 31 | 1,739 | `86ffeb6fd2ceac7e1b66068f3ee5373172a92846` |
| P4 | `.claude/agents/qa-automation-lead.md` | 31 | 1,691 | `34cd8c0e73cc89eb04d507b0039394831aee656f` |
| P5 | `.claude/agents/release-readiness-reviewer.md` | 31 | 1,765 | `b54a9f5efc139b16578014a9b804c801b6132941` |
| P6 | `.claude/agents/secure-saas-reviewer.md` | 34 | 1,908 | `490b57942a156f896457897a1aa45750594c8309` |
| P7 | `.claude/agents/senior-troubleshooting-lead.md` | 30 | 1,651 | `6ae09b38b11ac0565384bdc864dcac6e19a82df7` |
| P8 | `.claude/skills/_template/SKILL.md` | 119 | 7,081 | `de6d954b6040fff33122377b2f47b8b48106166b` |

**How those numbers were taken, and what the same method returns for the two changed files.** The
declared method is the **newline count** — the number of LF bytes in the blob — with `git cat-file -s`
for the bytes and `git rev-parse <rev>:<path>` for the blob SHA. **All eight pages above end with LF**,
so for each of them the newline count and the line count are the same number, and the eight reproduce
exactly at `e2a3e20b` (33 / 30 / 31 / 31 / 31 / 34 / 30 / 119 — 8/8, measured 2026-10-16 from the
blobs). The two paths the PR changes do **not** have that property, so **both** figures are stated for
each and neither is called "newline-terminated" without saying which it is: the **record** is 47,345
bytes with **575** newlines and **576** lines (its last line ends `.` and carries no LF), and the
**ledger** is 499,791 bytes with **5,386** newlines and 5,386 lines (it ends with LF).

**The two paths the PR's diff touches (the deliverable):**

| Path | Status | At head | In the diff, `base..head` |
| --- | --- | --- | --- |
| `docs/evidence/documentation/readability-lane-a-batch-1-2026-10-15.md` | new | blob `49d677a9…`, 47,345 bytes, **575 newline-terminated lines / 576 lines** | `576 0` |
| `docs/roadmaps/aegis-documentation-readability-backlog.md` | modified | blob `d27eada8…`, 499,791 bytes, **5,386 newline-terminated lines** | `151 0` — the lane-A section now occupies **L5114-L5255** (with its single trailing blank insertion line at L5256, shifted +18 by the inserted labelling block) and rows K-082..K-089 sit at **L5379-L5386** (shifted +18 the same way) |

**Not touched — named so that it is not implicit.** This PR's diff contains **no** page text
correction; **no** change to any of the eight read pages under `.claude/`; **no** change to
`docs/delivery-workflow.md`, `AGENTS.md`, `CONTRIBUTING.md`, any `.claude/skills/**` file, any
`scripts/**` path, any `tools/**` path, any `.github/**` workflow, any test, any configuration, data
or lock file; **no** rebuild of `tools/readability_acceptance/acceptance-index.json` (no
`build_index.py --write`); **no** new keeper row and **no** withdrawal row authored by the four
repair commits; **no** merge, no rebase, no force-push; **no** other lane's branch, PR, clone or
worktree. **This plan adds nothing to that diff**: it is captured as a new revision on the plan's own
branch, with its parent revision 4's commit `0cce5b33` — whose chain runs back through `5f3384df` to
`0bd37e4d`, the head current when revision 1 was captured — so the delivered diff stays two files and
the **PR head does not move** (`git diff --name-status 0cce5b33 <this revision's commit>` is one line,
`M` on this file).

## 3. What and why, and the blast radius (element 2)

**What.** Two Markdown paths under `docs/`: (a) one new batch record that names the eight pages by
path and by acceptance revision, records one disposition per page against the ledger's six
"Acceptance for each page" bullets, states the first-use observations it found and offers one verbatim
row-quote string per accepted page; and (b) one appended lane-A section in the ledger that states the
lane derivation, the keeper-independence defect and its routing, the count-honesty note, the
self-cost, the next-batch rule and the eight keeper rows K-082..K-089.

**Why — the need, with its evidence.** A page leaves the readability pending set only when an
acceptance exists on record for it. Measured at the acceptance revision by the programme's own
instrument: **653 reader pages, 57 accepted on recorded review, 4 provably pending, 586 with no
recorded acceptance, 6 cannot decide, official pending count 596**; the lane works the
`no_recorded_acceptance + provably_pending` union of **590** paths, of which lane A is the first
**148**. This batch supplies the read, the disposition and the citable evidence for eight of them. The
count itself is the instrument's (the official-count rule keeps the ledger from publishing one of its
own).

**Blast radius.** Two files, **+727 / −0**, five commits, both paths Markdown under `docs/` — measured
at `2e523622` on 2026-10-16 by this planner; the same commands are **re-run at the head §14.1
produces**, and the values they return there are what the final metadata pass publishes (§14.0):

```text
git diff --name-only  e2a3e20b7c20ef8385b219b39c6405237163406f..2e5236222080dc6064df0b493ab83a8a94441176
  docs/evidence/documentation/readability-lane-a-batch-1-2026-10-15.md
  docs/roadmaps/aegis-documentation-readability-backlog.md
git diff --numstat  <same range>   ->  576 0  (record)   151 0  (ledger)
git diff --shortstat <same range>  ->  2 files changed, 727 insertions(+)
git diff --check    <same range>   ->  exit 0
```

**No code, script, workflow, test, configuration, data or lock file is involved.** Both paths end
`.md` and begin `docs/`; the file list is measured, not described, and no path outside those two is
in the diff. The pure-docs condition therefore holds and the pure-docs path applies. It is lighter,
**not exempt**: all seven stages still run in order with a different holder per stage, and every
`MG1`–`MG5` condition still applies.

## 4. The change classification, recorded in the plan (element 3)

**Classification: `docs-only`** — taken from the `change-classification-gate` skill and re-applied by
this planner against the measured file set (the skill classifies from the files, never from the
wording). Recorded here because the workflow requires the classification **in the plan**, not only in
the PR's skills table.

- **Deliverables:** (1) the batch record; (2) the appended lane-A ledger section and eight keeper rows.
- **Classes:** `docs-only` for both.
- **Governing class:** `docs-only` (no higher-risk class is present in the diff).
- **Approval path:** **none** — `docs-only`'s row in the skill's class table requires no human
  approval. The keeper rows' *recording authority* is a separate question, and it is answered in §9:
  AEGIS-APR-101's independence condition is **not** met by the rows as authored, and the owner declined
  to ratify the deviation.
- **Validation floor for `docs-only`:** links/rendering sanity + review — met by the link checker on
  the record's links, the validator run and the review stages; §6 records which are run at this head.
- **Scope contract (locked file set):** exactly the two paths above. **Any edit to a third path, and in
  particular to any file under `.claude/` or `scripts/` or `.github/`, forces reclassification** — which
  is exactly why the record's flagged terms on P8 were recorded as an observation instead of being
  "fixed" by editing the page (editing a `.claude/skills/` instruction file is not `docs-only`).

## 5. Proportionate acceptance criteria, each decidable (element 4)

Each criterion states the command that decides it and whether it is **verifiable at this head**. The
C-1 screen of §5.1 is applied to **every** criterion: no criterion may fail a page for an unglossed
term that the screen classifies as a library-wide convention.

### 5.1 The C-1 screen, measured — prevalence per term, over the reader-page set

**Method (two steps, both run by this planner at the acceptance revision; neither is copied from the
record or the audit):**

```text
python -P -B tools/readability_acceptance/check_index.py --json --ref e2a3e20b7c20ef8385b219b39c6405237163406f
#   -> reader_pages_in_tree 653; the SET is check_index.py's own classify_tree("e2a3e20b...")["reader"]
#      (719 .md paths - 65 scripts/ fixtures - 1 generated report = 653), reproduced here independently
git grep -l -E '\\b<TERM>\\b' e2a3e20b7c20ef8385b219b39c6405237163406f -- '*.md'
#   -> "<tree-ish>:<path>" lines; strip the "<tree-ish>:" prefix, then intersect the paths with the
#      653-path reader set. Without the prefix strip the intersection is empty and every term reads 0.
```

**Measured (my own run, 2026-10-16):**

| Term | Reader pages of 653 | % | The screen's classification |
| --- | ---: | ---: | --- |
| `CI` | 250 | 38.3% | at/above ~12 — convention (OBSERVATION, not a gap) |
| `API` | **204** | 31.2% | at/above — convention |
| `AI` | 149 | 22.8% | at/above — convention |
| `JSON` | 85 | 13.0% | at/above — convention |
| `QA` | 83 | 12.7% | at/above — convention |
| `SaaS` | 63 | 9.6% | at/above — convention |
| `MANUAL-ONLY` | 59 | 9.0% | at/above — convention |
| `LLM` | 58 | 8.9% | at/above — convention |
| `PII` | 56 | 8.6% | at/above — convention |
| `DCO` | 53 | 8.1% | at/above — convention |
| `SQL` | 47 | 7.2% | at/above — convention |
| `YAML` | **32** | 4.9% | at/above — convention |
| `MCP` | **28** | 4.3% | at/above — convention |
| `TALI` | 27 | 4.1% | at/above — convention |
| `SAST` | 24 | 3.7% | at/above — convention |
| `IDOR` | 20 | 3.1% | at/above — convention |
| `SSRF` | 17 | 2.6% | at/above — convention |
| `N+1` | 15 | 2.3% | at/above — convention (measured with the literal string; see the method note below) |
| `MFA` | 10 | 1.5% | **below** — gap candidate |
| `AuthN` | 1 | 0.2% | **below** — gap candidate |
| `AuthZ` | 1 | 0.2% | **below** — gap candidate |

**The rule, stated so it is decidable:** a term used on **~12 or more** of the 653 reader pages is a
library-wide convention; an unglossed first use of it is recorded as an **OBSERVATION**, not a gap, and
**may not make a page fail**. A term below the threshold may be a gap, but a gap still needs the page's
own line cite.

**Method note for the one row the declared template does not reproduce (measured 2026-10-16).** The
declared command template `git grep -l -E '\b<TERM>\b'` returns **1** for `N+1`, because `+` is a
regex quantifier applied to the `N`; the literal string occurs on **15** reader pages
(`git grep -l -F 'N+1' e2a3e20b -- '*.md'`, tree-ish prefix stripped, intersected with the 653-path
reader set). The figure **15** is therefore right and the template is imprecise for a term containing
a metacharacter. This is recorded, not hidden: **20 of 21 rows reproduce under the declared template
exactly; `N+1` is the one exception, and it is not decision-bearing** — no criterion below fails a
page on it. Every other row was re-measured at `2e523622` and reproduces.

**The screen applied to the terms this PR's record turns on.** The record's only first-use flag is on
**P8**, for **YAML / API / MCP** — measured here at **32 / 204 / 28** of 653, i.e. **all three at or
above the threshold**, so the screen classifies all three as conventions and the record's disposition
("observation, not a gap", P8 **accepted**) is **screen-consistent**, not merely asserted. The three
below-threshold terms in the table (`MFA`, `AuthN`, `AuthZ`) are on **P6**, whose record entry states
they are glossed at first use; nothing in this PR records them as gaps, and no criterion below fails
any page for them.

### 5.2 The criteria

| # | Criterion (decidable) | Decided by | Verifiable at this head? |
| --- | --- | --- | --- |
| 1 | The diff `base..head` is exactly **two** Markdown paths under `docs/`, insert-only, and contains **no** code, script, workflow, test, config, data or lock file (the pure-docs condition). | `git diff --name-only` / `--numstat` / `--shortstat` / `--check` | **yes** — measured at `2e523622` (2026-10-16): 2 paths, `576 0`+`151 0`, exit 0; after §14.1's head-moving correction the same commands are **re-run at the head it produces** and their output is what the final metadata pass publishes (§14.0) |
| 2 | The change classification **`docs-only`** is recorded **inside the plan** (element 3), not only in the PR's skills table. | §4 of this file + criterion 1's file list | **yes** |
| 3 | All eight pages are named **by path**, bound to the full 40-character acceptance revision, each with a disposition, and the six acceptance bullets are addressed per page. | the record's own bytes; `git rev-parse` / `git cat-file -s` per page | **yes** — re-measured at `2e523622` (2026-10-16): 8/8 paths, 8/8 blob SHAs and line/byte counts reproduce ▼ |
| 4 | The eight pages are **untouched** by the diff (the bytes read are the bytes merged), so no acceptance is voided by the merge of this head. | the two-path file list (§3) against the eight page paths | **yes** — measured: intersection is empty |
| 5 | The C-1 screen is stated with **measured prevalence for every term the record's gap list turns on** and applied: **YAML 32, API 204, MCP 28** of 653 — all at/above the threshold, so none may make P8 fail; no criterion in this plan treats them as gaps. | §5.1 (commands and numbers, re-runnable) | **yes** — measured in this plan's own run |
| 6 | **No page recorded PARTIAL carries an acceptance row, and no page recorded PARTIAL deserves its row** (the both-directions rule): the record's own disposition table (L120-127) has **8 rows, all `**accepted**`, zero partial** — the only two `**partial**` strings in the record (L443, L444 at `2e523622`) sit inside section 9's *Before:* quotation of the text that pass superseded — and the ledger at this head holds exactly **8 rows for the eight paths, all `full-page-acceptance`, all bound to `e2a3e20b…`**, so no acceptance row exists for a page recorded partial. | the record's own bytes (rows counted by verdict); `git grep '^\| K-08[2-9] \|'` over the ledger at the head | **yes** — measured: 8/8 accepted dispositions; 8/8 ledger rows `full-page-acceptance` on the acceptance revision. **The index-level form of this check** (rebuild with `build_index.py --write`, then `check_index.py --path` per page, as the PR body's validation row 20 states it) is **not** reproduced by this planner — declared **N9**; the read-only `--report` form is criterion 7 |
| 7 | The record's own appended evidence is machine-visible: the ledger's consolidated table holds **109** data rows, **9 columns per row**, **0** malformed, **0** duplicate IDs, and the builder reports `table_rows 109, events 109, full_page_acceptances 89, lost_commit_events 10, reader_pages_with_rows 76` at this head. | `build_index.py --report --ref 2e523622` in a clone holding `refs/pull/**` and `refs/remotes/**`; the column count also by that tool's own `find_table(root, '2e523622')` (109 rows, 9 keys each) and by counting the 109 row lines' cells | **yes** — re-measured at `2e523622` (2026-10-16, 796 `refs/pull/*/head` fetched) |
| 8 | Every load-bearing figure in the record that this plan re-derived **reproduces**: the eight line/byte counts, the eight blob SHAs, the instrument's eight summary figures, the pending union 590, the quarters 148/148/148/146. | §1 rows 13-16; §7 derivation | **yes** — re-measured at `2e523622` (2026-10-16); the derivation was re-run from the five batch records' own bytes |
| 9 | The record publishes **no `base..head` count that a head move can falsify**: it states the insert-only facts and binds the added-line count as a **re-derivation at the head that publishes it** (`git diff --numstat e2a3e20b..HEAD`), and the literal for the head it is read at is stated in the PR body's validation rows 4 and 16 by the final metadata pass. | `git diff --numstat` at the head read; §14.0-§14.2 | **no at this head** — the record's bytes at L526-528 say `689` where the head measures **727**; declared **N1** in §6 and bound as a duty in §14.1 |
| 10 | The PR body's validation table does not contradict itself **at the head it is read at**: after the final metadata pass — which contains no head-moving commit — rows 1, 2, 4, 13 and 16 and the narrative state the values re-derived at that pass's head `H` (`git rev-parse refs/pull/771/head`, `git rev-list --count origin/main..H`, `check_dco.py --range origin/main..H`, `git diff --numstat e2a3e20b..H`). | the live body + `gh api`; §14.2 | **no at this head** — rows 1/2/4/13 say `0bd37e4d` / 4 commits / `556 0`+`133 0`, and row 16 says `556 0`+`133 0` = 689, where the head measures `2e523622` / 5 commits / `576 0`+`151 0` / **727**; declared **N2** and bound as the final metadata pass in §14.2 |
| 11 | The next-batch list is labelled by the state it was measured at, and the first eight **unread** pages at the acceptance revision are named by path: derived = lane-A indices **40..47** (§7), and the labelling block is present in the record, the ledger and the body. | §7's three-step derivation, re-runnable | **yes at this head** — applied by the Stage C commit `2e523622` (record L339-355, ledger L5221-L5237, body L278-294) and re-verified by this planner: the derived eight paths are 8/8 the inserted ones (N3 discharged) |
| 12 | Every page path this PR **reads** is distinct from every path it **writes**: the eight read pages appear nowhere in the diff, and the two written paths are not among the 653 reader pages' acceptance rows authored here. | file list + `git grep` over the diff | **yes** — measured: empty intersection |
| 13 | The capture exists: this plan is a tracked file whose **blob SHA and capturing commit** are recorded in the PR #771 body **and** in a fresh issue comment holding the same text verbatim, with the earlier comments unedited, and with every superseded revision named. | the body text; the comment id and its extracted fenced block hashed against the committed bytes | **yes** — the revision-5 capture receipt is in the PR body; the verbatim check is reproducible by extracting the fence and hashing (the fence-strip read differs from the committed bytes by exactly one trailing newline); revisions 1, 2, 3 and 4 remain immutable and are named in §13 |
| 14 | The capture edit **does not disturb the PR's bound fields**: the published bound-field digest still recomputes to `4cd96b537eb398a1` under the body's declared method. The **owed** §14.2b edit moves it **once**, to the value §14.2b binds and the final metadata pass republishes. | the declared method, recomputed over the live body before and after the edit | **yes** — measured before the edit (reproduced exactly, with the four sibling calibrations) and re-measured after; §14.2b states the post-insertion value `b78221cc2ae8f394` and the precondition under which it holds |
| 15 | Branch hygiene: every commit on the plan's own branch is DCO-signed, `git diff --check` is clean, and the body's bound fields still parse. | `scripts/check_dco.py --range`; `git diff --check`; `scripts/ci/check_pr_body_skills.py --body-file` | **yes** — measured for revision 5 (2026-10-16): the plan commit is DCO-signed (`check_dco.py` over `origin/main..<capture commit>`), `git diff --check` exit 0, and the body checker returns `PR body bound fields: OK` before and after this revision's receipt is appended (revision 4 was measured the same way) |

▼ Criterion 3's page-level truth (that each bullet was judged *per page*) is only as strong as the
record's own text; the parts of it that no artifact can carry are declared in §6 (N4, N5).

## 6. Criteria declared not verifiable at this head, with reasons (element 5)

The workflow permits a criterion to be `UNRUN` at Stage D **only** if the plan at SD-A declared it
not verifiable at this head with its reason. These are so declared. None of them may be used to force
a disposition on this PR; each is excluded from §5.2's passing set.

- **N1 — the record's corrected diff-scope bytes.** The corrected bytes are a **Stage C commit's** to
  make; this planner holds Stage A only, and editing a file the PR itself adds would move the head and
  void every head-bound verdict (it is also outside a planner's stage). Reason: the criterion measures
  bytes that do not exist at this head. **What is decidable now:** that the record's present bytes at
  L526-528 say `689` while the head's diff measures **727** — measured, and bound as a duty in §14.1.
  The **value** for the head the correction produces is not bound here at all: it is re-derived and
  published in the final metadata pass (§14.2), because a number inside a head-moving file is falsified
  by the commit that writes it (§14.0).
- **N2 — the PR body's corrected validation rows, and the republished digest.** The body is PR
  metadata, not a candidate file, so correcting it moves no head; but the correction is not this
  planner's to publish *as a result*, and the rows' correctness depends on which head they are stated
  for. Reason: the corrected text does not exist in the live body at this head. **Decidable now:** that
  the live rows contradict the measured head (row 1 `0bd37e4d` vs `2e523622`; row 2 "4 commits" vs 5;
  row 4 and row 16 `556 0`+`133 0` = 689 vs `576 0`+`151 0` = 727; row 13 "4 commit(s)" vs 5) —
  measured, and bound as the final metadata pass in §14.2.
- **N3 — the corrected next-batch list — DISCHARGED at `2e523622`.** The labelling block was applied by
  the Stage C commit in all three places (record L339-355, ledger L5221-L5237, body L278-294); this
  planner re-verified it against its own derivation: the eight paths it names are 8/8 the first eight
  unread (indices 40..47) at the base. It stays listed so that the earlier revision's declaration is not
  silently dropped; nothing further is bound (§14.3).
- **N4 — that the reader actually read each page whole, line by line, as prose.** No instrument records
  a reading act; the only evidence is the reader's own record. Reading is an act, not an artifact, and
  the repository has no read-tracking mechanism.
- **N5 — the model attribution of the reader and the repairers** (`deepseek-v4-pro`,
  `deepseek-flash`). The repository's attribution rule requires the naming; nothing verifies which
  model produced bytes. Every commit in this repository is made under the owner account, so git's
  author field cannot distinguish agents — which is why §9 states the independence test in its
  falsifiable form rather than as a git query.
- **N6 — PR #781's patch in full.** Its content is measured here only through `main`'s ledger rows
  (8 withdrawal rows `K-082W..K-089W`, 7 fresh rows `K-098..K-104`, `K-105` unused — measured by
  command) and its merge commit `f490c16f`; its whole diff was not re-read.
- **N7 — the four non-GitHub CI suites** (supabase / vercel / claude / cursor) and the Codex
  review-comment bodies: no runs exist at this head for the former, and the latter are not
  retrievable here. Reason: the evidence is not in the repository.
- **N8 — this head's merge with `main`.** The PR is CONFLICTING/DIRTY against `main`
  (`38413563…`); reconciling the appended rows with `main`'s is the merge holder's step. Reason: a
  rebase or a merge would move the head and void every head-bound verdict, so this plan does not
  perform it and cannot decide it.
- **N9 — the index-level both-directions check as the PR body's validation row 20 states it**
  (`build_index.py --write --ref HEAD` followed by `check_index.py --json --path <each of the eight>`,
  "all eight pages ACCEPTED, event_kind full-page-acceptance, changed_lines 0", with the two generated
  JSON files then restored byte-identically). Reason: it requires writing the generated index into a
  working tree; this planner ran only the read-only `--report` form and does not reproduce a
  write-then-restore inside a capture run. **Decidable now:** both directions at the record and ledger
  level (criterion 6) and the report's counts (criterion 7); the write-based form is Stage D/E's to
  reproduce.

## 7. The next-batch selection rule, stated by content, and how its frontier is derived (element 6)

**The naming caveat — no label in this plan is offered as authority.** The labels used here (`C-1`,
`C-3`, `R2`, `C-4`) are **not tracked rulings in this tree**; every rule is stated by **content**, and
a reader who relies on a rule must rely on its content and its measurements, never on a label.
Measured by command (2026-10-16):

- `git grep -l -E 'C-[134]' origin/main -- docs/` returns 6 files, **none of them the ledger**, the
  delivery workflow, or an approval entry; the one `C-1` hit in
  `docs/evidence/documentation/readability-reread-batches-2026-10-12.md` (L229) is a **change-site ID**
  in a change-site table, not a ruling.
- `git grep -n -E 'page-resolves-it' origin/main -- docs/` returns **nothing**: the phrase this PR's
  record uses to explain its P8 disposition is not on `main` at all.
- `git grep -c -E 'C-[134]' origin/main -- docs/roadmaps/aegis-documentation-readability-backlog.md`
  returns **0**: the ledger on `main` does not carry these labels.
- The reading named `R2` **is** recorded in a lane's batch record (lane A batch 5, on `main`), but a
  reading recorded inside one lane's record is a practice, not a ruling.

**The rule, stated in full.** *The next batch is the **next eight unread pages in the unread
sequence**, re-measured at that batch's **own implementation base**, and **named by path**.* It is
never a pinned index, never index arithmetic, never a pinned range. The unread sequence is the sorted
list of pages that no lane's batch record has yet read. The rule exists because the two rejected
readings fail: *the eight contiguous pages after the frontier* can orphan a page behind the frontier,
and *index arithmetic* silently couples a batch to a shifting pending set.

**How the frontier is derived from the lane records' own committed bytes** (the instrument cannot
compute it: `check_index.py` sorts pages into buckets and does not know which lane read what):

1. **The pending set at the batch's own base.** `python -P -B tools/readability_acceptance/check_index.py
   --json --ref <base>` gives the two buckets `no_recorded_acceptance` (586) + `provably_pending` (4)
   = **590** paths, sorted by repository path. Lane A is the first `ceil(590/4) = 148` of them.
2. **The read set.** The union of the page paths that **lane A's committed batch records** name as
   read, each record cited by the **ref and commit that hold its bytes** (never by a PR's status):
   `refs/heads/docs/readability-lane-a-batch-1-20261015` `2e523622` (blob `49d677a9`) — batch 1's
   branch **is** the PR branch, so its tip moved with the head; the eight `P#` rows are identical at
   `0bd37e4d` and at `2e523622` (both measured 2026-10-16, 8/8), so the citation names the tip;
   `…batch-2-20261015` `8b0ba011`; `…batch-3-20261015` `7b0e9f60`; `…batch-4-20261015` `0c994d77`
   (the previously cited immutable object `44d8f431` still resolves, and its extracted `P#` row set is
   identical to the tip's, so the frontier is unaffected — the tip is named because a citation must
   resolve as a ref/commit/blob triple); `…batch-5-20261015` `864461c7` — the eight `| P# | path |`
   rows of each record, extracted by path pattern from that record's own committed bytes.
3. **The next eight.** The first eight paths of (1), in repository-path order, that are not in (2) —
   **named by path**, never by index.

**My derivation, re-run at the acceptance revision on 2026-10-16 (`check_index.py`'s own
`classify_tree`, then the five records' bytes), reproduces the record's own cross-check and the
labelling block the Stage C commit inserted:**

```text
pending set at e2a3e20b                  : 590   (586 no_recorded_acceptance + 4 provably_pending)
quarters                                 : 148 / 148 / 148 / 146
lane A                                   : 148 paths
  first .claude/agents/ai-security-red-team-reviewer.md
  last  .claude/skills/feature-flag-rollout-strategist/references/flag-rollout-sheet.md
lane A read set (batches 1-5, 8 pages each) : 40 pages, sorted indices 0..39, CONTIGUOUS, no gap
lane A read frontier after batch 1        : sorted index 7  .claude/skills/_template/SKILL.md
UNREAD PAGES BEHIND THE FRONTIER          : 0
first eight UNREAD at this base           : sorted indices 40..47
```

**The eight unread pages at that base, named by path (a re-measurement output at that base, NOT a
pinned range):**

1. `.claude/skills/ai-closeout-reporter/SKILL.md`
2. `.claude/skills/ai-closeout-reporter/assets/closeout-template.md`
3. `.claude/skills/ai-cost-guardrail-designer/SKILL.md`
4. `.claude/skills/ai-cost-guardrail-designer/references/cost-guardrail-patterns.md`
5. `.claude/skills/ai-evaluation-harness/SKILL.md`
6. `.claude/skills/ai-evaluation-harness/references/eval-harness-design.md`
7. `.claude/skills/ai-governance-risk-reviewer/SKILL.md`
8. `.claude/skills/ai-governance-risk-reviewer/references/ai-governance-framework.md`

**The defect this exposed (⚠ Difference 3, §1) — corrected at this head.** The record named, as "the
first eight entries of the unread sequence at this base", the eight paths at lane-A sorted indices
**8..15** (`ab-test-designer` … `adr-sequencer`) — which are **exactly the eight pages lane A batch 2
has already read** (measured: batch 2's record's eight `P#` rows are those paths, 8/8). They were the
first eight unread **at the moment batch 1 was the only lane-A record**; they are not the first eight
unread under the read set the same section asserts ("lane A's own reads are indices 0..39 with no
gap"). The ledger's appended section and the PR body repeated the same list. The labelling block that
names each list's state is now present in all three places (record L339-355, ledger L5221-L5237, body
L278-294, applied by `2e523622`), so the record no longer publishes a figure its own measurement
contradicts; the rule's content is unaffected, because the list must be re-measured at the next
implementation base in any case.

**Fail-closed.** If any lane-A batch record is not retrievable from a fetched ref at derivation time,
or the acceptance index in hand is not the one at the pinned base, the derivation **stops and
escalates**. It must not fall back to index arithmetic and must not guess a frontier. The derivation
above was validated the same way lane B's was: it reproduces the record's frontier claim (index 7,
zero unread behind it) and the cross-check (indices 0..39 contiguous) from the records' own bytes.

## 8. The five-question necessity and reuse answers, with per-question routing (element 7)

Each answer names the evidence that settles it and the routing disposition Stage B is to record
(**cite** / **preserve** / **smallest change** / **bounded check**).

1. **Necessity — what need does this serve, and what evidence shows the need exists?** The need is a
   **captured Stage A plan for PR #771**, which has never existed: the PR's own skills table records
   that Stage A and Stage B rows are owed at every head, and the workflow makes a captured plan
   Stage B's entry evidence and an affirmative SD-B a Stage C entry condition. A second, measured need
   rides on it: the record publishes `689 added / 0 deleted` at L526-528, false of the head that
   publishes it (**727**), and the body's rows 1, 2, 4, 13 and 16 state a superseded head, four commits
   where there are five, and `556 0` / `133 0` where the head measures `576 0` / `151 0` — defects that
   only a captured plan can bind without moving the head, and that must be bound as a duty rather than
   as literals because the correction is itself a commit. *Routing: **cite*** — the PR's owed-stage
   record, §1's measurements and §14's bound corrections.
2. **Reuse — what existing mechanism, skill, script, document or decision already does this?** The
   lane's tracked batch-record pattern (already used by five lane-A batches); the ledger's six
   "Acceptance for each page" bullets as the acceptance criteria; the committed instrument
   `check_index.py` for the pending set and `build_index.py` for the table arithmetic; the
   AEGIS-APR-101 keeper role for recording; the consolidation of the PR body's three bound fields
   checked by `scripts/ci/check_pr_body_skills.py`; and the `docs/plans/` capture pattern two sibling
   PRs already use. **The only new artifact is this plan file.** *Routing: **preserve*** — every
   mechanism keeps its existing owner; nothing is re-implemented, and no tool, workflow or index is
   touched.
3. **Ownership — who holds authority and responsibility for this surface, at this revision?** The
   recording role and its independence limit: **AEGIS-APR-101** (register L3149-3159 at both this head
   and `main`; "The keeper must be a different agent from the page's author and accepting reviewer",
   L3155, with **no waiver** — L3157 forbids "waiver of existing review and delivery requirements").
   Withdrawal rows: **AEGIS-APR-117** (register L5038-5042), which is **WITHDRAWAL-ONLY** — it lets the
   keeper *cancel* a wrong row, and it grants **no** authority to record a fresh acceptance. Standing
   backlog delivery: AEGIS-APR-039. Merge: Stage G, not this PR. *Routing: **preserve*** — proceed
   inside that authority and do not re-ask; §9 records what that authority does and does not permit
   for the rows this PR carries.
4. **Minimum-safe action — the smallest action that satisfies the need without weakening a control?**
   Commit **one** Markdown plan file as a new revision on the plan's own branch — this revision's
   parent is revision 4's commit `0cce5b33`, whose chain runs back through `5f3384df` to `0bd37e4d` (the
   head at revision 1's capture), so the revision adds **no path other than the plan file** and moves **no** head — and add
   one out-of-bound-field capture reference to the PR body plus one fresh comment. No page edited, no
   keeper row authored, no ledger byte changed by this planner, no tool, workflow, check, approval or
   index touched, no tier downgraded, no scope widened, **no bound field edited**, and **the PR head
   does not move**. *Routing: **smallest change***.
5. **Complexity justification — why is this machinery warranted, and what would be smaller?** The
   machinery is the workflow's own minimum: Stage B cannot audit what was never captured, and a plan
   may be small but never absent. Smaller alternatives and why they fail: **a plan paragraph in the PR
   body is not a capture as the workflow uses that word**, and the workflow's own sentence is weaker than
   that phrasing, so the plan states the sentence's own terms: a plan that lives only in a PR body *is
   not exempt from exact-revision binding merely because it is not a file*
   (`docs/delivery-workflow.md` cited by **ref and blob**: at the PR head `2e523622…` the file is blob
   `bff407a65ade2fc7f07871e9d57bf0dc20a55516` and the rule sits at its **L587-592**; at `main`
   (`38413563…`) the same rule is blob `9a2ea2bd3557740373cce1285b9f31736b7fe1ec` at **L611-616** —
   both verified 2026-10-16, and the line number is never carried from one ref to another). The consequence is the
   one that matters and it is measured, not asserted: the three Stage B verdicts in this programme that
   turned on exactly that were PR #784 (comment `6211504777`, SD-B REVISE, "no captured plan exists for
   this PR, so Stage B has nothing to bind"), PR #785 (comment `6211647547`, SD-B REVISE, no captured
   plan revision) and PR #789 (comment `6211547391`, SD-B REVISE, no captured plan revision; that one was
   later discharged by the ACCEPT at comment `6212640376`, which names it as superseded and discharged)
   -- each read this pass and each bound to its own head; **a comment alone** is allowed by the workflow
   but weaker than a
   tracked file and it would still have to hold the text; **widening the plan into a design document**
   is disproportionate for a two-file docs change. *Routing: **cite*** — the requirement is textual,
   so no bounded check is needed.

## 9. The non-author test (element 8)

**This PR records eight acceptance rows and they are NOT keeper-independent.** The ledger's
consolidated table at this head carries **K-082..K-089**, appended by this PR's first commit
(`09a7ee1c`), for the eight pages. Their `Reviewer` cell is `readability-lane-a-implementer-c` — the
same agent identity that judged the pages accepted. **AEGIS-APR-101 requires the keeper to be a
different agent from the page's author *and* its accepting reviewer** (L3155), and **no waiver is
available** (L3157 forbids "waiver of existing review and delivery requirements"). The owner
**declined on 2026-10-15 to ratify** the carry-with-deviation and directed the withdrawal route
instead.

**Who may record, and who may not.** For any page this PR covers, an acceptance row may be recorded
only by a keeper that is **not** the page's author, **not** its accepting reviewer (so
`readability-lane-a-implementer-c` is excluded for all eight), and **not any other stage of this PR**
(so the two repairer identities and this planner are excluded too). That keeper records under
**AEGIS-APR-101**'s recording limb, bound to the acceptance revision `e2a3e20b…` and to this
evidence. **AEGIS-APR-117 is withdrawal-only** and supplies **no** authority to record a fresh
acceptance — it is the instrument that cancels the eight non-independent rows, not a substitute for
the independence test.

**What has already been recorded elsewhere, measured on `main` (not this head):** the merged PR #781
appends the **8 withdrawal rows `K-082W..K-089W`** and **7 fresh rows `K-098..K-104`** recorded by a
different keeper (`deepseek-v4-pro-apr117-keeper`); **`K-105` has no row** — it was left unused
because #781 was written while P8 was still recorded partial. Measured on `main` by command: 8 rows
`K-08nW`, 2 rows `K-098/K-099`, 5 rows `K-100..K-104`, **0 rows `K-105`**, and **0 rows
`K-082`/`K-089`** (those exist only in this branch). So:

- **P1-P7** have a fresh, independent acceptance on `main` (K-098..K-104);
- **P8's fresh full-page-acceptance row is still owed**, on the withdrawal-and-re-record route, from
  the same evidence and without re-reading the page;
- **this PR's own eight rows stay as authored** — its three repair commits author no keeper row and no
  withdrawal row, and reconciling the two row sets is the **merge holder's** step.

**What is testable, and what is not.** Whether the pages' *authors* are different agents from the
reader is **not** decidable from git: every commit is made under the owner account. What this plan
therefore requires is the falsifiable form: (i) the diff contains no page, index or tool file, so no
acceptance this PR records can be silently "made true" by editing the reviewed bytes —
**measured, §5.2 criterion 4**; (ii) the recording agent's identity must be named as a *different*
agent in the keeper's own artifact — where the independence claim has to be made and checked; (iii)
the six bullets' independent-read bullet is satisfied only to the extent that the reader is a
different agent from the page authors, and **a keeper must not re-derive that from the record's commit
list**, which cannot distinguish agents.

**A residual weakened pairing on the two changed files and on this PR's body — recorded, not bound
here, and routed to Stage D.** *Gloss for this paragraph: **the owner's compound** is the owner's own
hyphenated term `re-record` for the recording act; the approval register contains it **nowhere**
(measured 2026-10-16 at `2e523622` and on `main` across fourteen spellings — the ASCII hyphen, seven
further dash code points, the closed form `rerecord`, and the inflected forms — **0 hits at both refs**;
the apparent hits for the spaced form are substring noise inside ordinary words such as "are recorded").*
The sharp test this plan applies to itself and to the two changed files is: **does any text attach the
owner's compound, or any recording act, to a citation of the register's withdrawal grant?** Swept over
the whole plan, the record and the ledger at `2e523622`, and the live PR body, the answer is **six sharp
sites, two route-form sites and two recording-act sites — every one enumerated below, none inferred from
another**. The compound is named once here and referred to as *the owner's compound* below **so that this
inventory does not itself place the word beside the citation it is inventorying**; a reader who wants the
literal sweep has the command at the end of this paragraph.

*Sharp form — the owner's compound in the same construction as a citation of `AEGIS-APR-117`:*

| # | Site | The citation it carries | The construction |
| --- | --- | --- | --- |
| 1 | record **L71-L72** | `AEGIS-APR-117` | the owner's compound inside the "withdrawal-and-… route" phrase the owner directed |
| 2 | record **L385** (the disposition table's row 1) | `AEGIS-APR-117` | "remedy routed to …", then "and directed withdrawal-and-…" carrying the owner's compound |
| 3 | ledger **L5165-L5166** | `AEGIS-APR-117` | the same "withdrawal-and-… route" phrase |
| 4 | PR body **L28** | `AEGIS-APR-117` | the same phrase, in the body's diff-scope narrative |
| 5 | PR body **L120** — inside the `skills` bound field | `AEGIS-APR-117` | the round-1 `scoped-approval-register` row's Result cell: "directed the … route" |
| 6 | PR body **L129** — inside the `skills` bound field | `AEGIS-APR-117` | the round-3 `scoped-approval-register` row's WHAT cell: "use the … route" |

*Route form — a fresh acceptance row attached to the withdrawal grant's route rather than to its scope:*

| # | Site | The citation it carries | The construction |
| --- | --- | --- | --- |
| 7 | record **L404-L409** | `AEGIS-APR-117` | "its keeper-independence defect … is routed through [it]" and "the fresh full-page-acceptance row for P8 is owed on that route" |
| 8 | ledger **L5249** | `AEGIS-APR-117` | "carries K-082W..K-089W and fresh rows K-098..K-104" |

*Recording acts that sit in a passage citing the register's withdrawal grant on an adjacent line, with
the compound not beside the citation — listed so the inventory is exhaustive rather than representative:*
record **L81** ("cancelled by withdrawal rows and re-recorded by a different, eligible keeper", in the
paragraph whose L71 cites the grant) and PR body **L261** ("the eight rows are withdrawn and re-recorded
on `main`", the merge-holder sentence, which cites no grant on its own line).

A route is not a grant, and none of these sentences says "recorded under APR-117"; several also name
AEGIS-APR-101 as the recording authority (record L102). But the register's own words are that
AEGIS-APR-117 "does not supersede or rewrite AEGIS-APR-101" (L5018-L5019) and that "AEGIS-APR-101's
limits continue" (L5043-L5044), so a sentence that puts fresh acceptance rows under a heading naming the
withdrawal grant is exactly the reading the register forbids. **This plan binds no correction for it**:
it is a Stage D item on the two changed files and a PR-metadata item on the body, not a Stage B
condition, and §14.4 keeps the correction set to the documented defects. It is recorded here so that it
is not discovered a further time. **The plan's own text is clean under the same test**: its one
occurrence of the owner's compound outside this paragraph sits in a sentence that cites no grant, and
§12 names its line. The sweep, run 2026-10-16 at `2e523622`:

```text
git grep -n -I -E 're[-‐‑‒–—―−⁃]?record' 2e523622 -- docs/evidence/documentation/readability-lane-a-batch-1-2026-10-15.md docs/roadmaps/aegis-documentation-readability-backlog.md
  -> exit 0, 4 hits: record L72, record L81, record L385, ledger L5166   (each named above)
git grep -n -I -E 're[-‐‑‒–—―−⁃]?record' <ref> -- docs/approvals/APPROVAL_REGISTER.md
  -> 0 hits at 2e523622 and 0 at origin/main (exit 1 each)
```

The body is not a tracked file, so `git grep` cannot reach it: the live body was fetched with
`gh api repos/ModernNomad-98/Project-Aegis/pulls/771 --jq .body` and swept with the same regular
expression, returning **four** lines — L28, L120, L129 and L261.

## 10. The evidence the work will produce, and where it lives (element 9)

| Evidence | Where it lives |
| --- | --- |
| The eight dispositions, their six-bullet judgements, the purpose/normal-use restatements and the eight verbatim row-quote strings | `docs/evidence/documentation/readability-lane-a-batch-1-2026-10-15.md` at head `2e523622` (blob `49d677a9…`, **575 newline-terminated lines / 576 lines**) |
| The eight keeper rows K-082..K-089 (full-page-acceptance, bound to `e2a3e20b…` with the page's blob SHA in the row) | `docs/roadmaps/aegis-documentation-readability-backlog.md` **L5379-L5386** at head `2e523622` (blob `d27eada8…`, 499,791 bytes, **5,386 newline-terminated lines**) — verified row by row 2026-10-16 |
| The lane-A section: derivation, keeper-independence defect and routing, count honesty, self-cost, next-batch rule | same ledger, **L5114-L5255** (the insertion carries one trailing blank line at L5256; the 17-line labelling block sits at L5221-L5237) |
| The pages' bytes at the acceptance revision and their blob SHAs / line / byte counts | the git objects at `e2a3e20b…` (§2's table, re-measurable by command) |
| The instrument's counts (`653 / 57 / 4 / 586 / 6 / 596`), the 590-path pending set and the 148-path lane-A quarter | `check_index.py --json --ref e2a3e20b…`; recorded in the record's §1 |
| The C-1 prevalence screen | §5.1 of this file — commands and per-term numbers, re-runnable |
| The next-batch derivation and its output at the base | §7 of this file — three steps, one output list, not a pinned range |
| **The capture of this plan** | this file's **blob SHA** and the **capturing commit**, published in the PR #771 body, plus the **fresh issue comment** on PR #771 carrying the same text and its id; every superseded revision (1-3) named there and here (§13) |
| The rows still owed (P8's fresh row; any future batch's rows) | a separate eligible keeper's artifact under AEGIS-APR-101 — **not** this PR and **not** this plan |

**What the plan does NOT decide** is stated in full in §11. **The plan's own capture** is recorded in
the PR body and the fresh comment rather than in this file, because a file cannot contain its own
content hash; §13 states the binding and what voids it.

## 11. What this plan does NOT decide

1. **It does not decide that the record's dispositions are correct.** It plans, states the criteria and
   declares what is not verifiable; the independent implementation audit (Stage D) is the decider, and
   a fresh one is owed at this head.
2. **It does not reclassify any page of its own motion.** P8's `accepted` disposition rests on the
   coordinator's 2026-10-15 ruling and is *screen-consistent* under §5.1's measurement; this plan
   applies it rather than re-litigating it, and it does not extend it to any other page.
3. **It does not decide the keeper IDs, the keeper's identity or the row types.** Those belong to the
   allocation and to a separate eligible keeper (§9); P8's fresh row is owed on that route.
4. **It does not decide whether or when the index is rebuilt**, and it runs no
   `build_index.py --write` (the instrument's `--report` only).
5. **It does not adjudicate the six `cannot_decide` (lost-commit) pages' lane routing**, which remains
   a coordinator call outside this record.
6. **It does not resolve this head's conflict with `main`**, rebase the branch, or merge anything
   (Stage G, a separate holder; the head is frozen by this plan's binding).
7. **It does not hold or post Stage B, D, E, F or G** on this change, and it states no verdict on the
   implementation that already exists at this head.
8. **It does not re-derive** the items declared not verifiable in §6 (N1-N9).
9. **It does not perform Stage C.** The corrections of §14 are the implementation stage's to commit —
   this planner holds Stage A only, and applying them would move the head deliberately and visibly at
   Stage C rather than as a side effect of the plan's own capture. **Applying §14.1 will move the
   head**; when it does, the criteria that measure the base-to-head diff (1, 3, 4, 8, 12) must be
   re-derived at the new head and this plan's head binding must be re-read as §13 states. **The four
   head-stamped quantities are never bound as final values here**: §14.0 states the rule by content and
   §14.2 places their literals in a final metadata pass that moves no head.
10. **It does not edit any bound field of the PR body — and it does not justify that by a head-bound
    verdict.** Adding the Stage A skills row is an owed *governance-table* edit that moves the
    `skills` bound field and therefore the published digest. §14.2b therefore binds **the insertion
    point, the exact row text, the head-invariant replacement for the two stale head-stamps inside the
    field, and the recomputable post-insertion digest `b78221cc2ae8f394`**, and routes the edit to the
    PR editor in the **final metadata pass** after the last head-moving commit. The reason is not that
    a live verdict names the present digest — revision 3's justification, which expired when the head
    moved — but that a bound field may only be edited where its digest can be recomputed and
    republished in the same edit.

## 12. Verification ledger — what was run, and what could not be verified

Run by this planner on 2026-10-16 in a fresh HTTPS clone (`git clone -c http.sslBackend=openssl`
https://github.com/ModernNomad-98/Project-Aegis.git; the shared clone was **not** used or cleaned; no
worktree was created; `git config user.name` was read **first** and is `Peter Nguyen`):

| Check | Result |
| --- | --- |
| `git rev-parse refs/pull/771/head` and the PR branch ref | both `2e5236222080dc6064df0b493ab83a8a94441176` — **the head has not moved**, re-checked after this revision's capture commit (the capture is on the plan branch, which is not the PR branch) |
| `git merge-base origin/main refs/pull/771/head` | `e2a3e20b7c20ef8385b219b39c6405237163406f` |
| Head tree / base tree | `5758d7c95571d5dc33679a9c492b75fda77861fe` / `effc72501297375d490705eaae686a0c181df2e6` |
| `origin/main` at this reading | `38413563a843f030d3ac992b375b5db5528f2926`; the PR is `CONFLICTING` / `DIRTY` (`gh pr view 771 --json mergeable,mergeStateStatus`) |
| `git rev-list --count base..head` | **5** |
| `git diff --name-only` / `--numstat` / `--shortstat` | 2 paths; `576 0` + `151 0`; `2 files changed, 727 insertions(+)` |
| Raw-patch hand count | 729 `+` lines (727 + 2 file headers), 2 `-` lines (both `---` headers), 3 hunks |
| `git diff --check` | exit 0 |
| `python -B scripts/check_dco.py --range origin/main..2e523622` | exit 0 — 5 commits, all SIGNED: `OK: 5 commit(s) checked, all signed off or exempt` |
| Bound-field digest, recomputed from the live body by the declared method | `4cd96b537eb398a1`, lengths 1262 / 17182 / 40 — equals the published value; the four sibling calibrations reproduce exactly from their own live bodies: `#783 3913683c686e6e71`, `#787 82ed906d2f228f0e`, `#792 88300e711714200a`, `#795 5fabf87b2df899e9` |
| §14.2b post-insertion digest, computed by the same method over the three bound in-field edits | `b78221cc2ae8f394`, lengths 1262 / 19172 / 40 — bound as a recomputable value in §14.2b |
| `check_index.py --json --ref e2a3e20b` | `653 / 57 / 4 / 586 / 0 / 0 / 6 / 596`; pending union 590; quarters 148/148/148/146 |
| `build_index.py --report --ref 2e523622` (full clone, 796 `refs/pull/*/head` fetched) | `table_rows 109, events 109, full_page_acceptances 89, lost_commit_events 10, reader_pages_with_rows 76` |
| Ledger keeper-table scan | 109 data rows (K 89 + L 10 + T 10), **every row 9 columns**, **0 duplicate IDs** — measured 2026-10-16 at `2e523622` by `python -B tools/readability_acceptance/build_index.py --report --ref 2e523622` (exit 0) and by that tool's own `find_table(root, '2e523622')`, which returns 109 rows whose key set is 9 names (`stable_id`, `path`, `event_kind`, `revision`, `blob_id`, `quote`, `reviewer`, `evidence_source`, `date`); the table's header at ledger L5276 names the same nine (`Stable ID`, `Page`, `Event kind`, `Acceptance revision`, `Blob ID`, `Quote`, `Reviewer`, `Evidence source`, `Date`), all 109 data rows carry 9 non-empty cells (histogram `{9 cells: 109}`, each row line carrying ten pipe characters, 0 rows with an empty last cell); the builder's own docstring says "the nine schema columns" and its parser raises `malformed keeper row (expected 9 columns, got ...)`; and `git grep -E '8 columns'` and `git grep -E 'eight columns'` over `docs/` and `tools/` at `2e523622` return **nothing** (exit 1 each) |
| Line counts, by this plan's own declared newline-count method (LF bytes in the blob, read from `git cat-file blob <rev>:<path>`) | record `49d677a9…`: **575** newlines, **576** lines, last line unterminated (ends `.`); ledger `d27eada8…`: **5,386** newlines and 5,386 lines (ends with LF); the eight pages at `e2a3e20b`: **33 / 30 / 31 / 31 / 31 / 34 / 30 / 119**, the same number as each page's line count because each ends with LF — **8/8 reproduced under this method** (2026-10-16) |
| Record's disposition table / ledger rows for the eight paths | 8/8 `**accepted**`, 0 partial (record L120-L127); 8/8 ledger rows `full-page-acceptance` bound to `e2a3e20b…` at ledger L5379-L5386 |
| The appended lane-A ledger section's extent | **L5114-L5255** + one blank insertion line at L5256 |
| The record's location facts at this head | two `**partial**` strings at **L443/L444**; the diff-scope paragraph at **L526-528**; the labelling block at **L339-L355**; `689` at L527, `445` at L531; `git grep -n -E '727|576|151'` over the record returns **nothing** |
| The eight pages at the base | 8/8 blob SHAs, line counts and byte counts reproduce the record's and the body's figures (re-measured page by page at `e2a3e20b`) |
| Term prevalence (§5.1) | 21 terms over the same 653 pages; `API` 204, `YAML` 32, `MCP` 28 reproduce exactly; **20 of 21 rows reproduce under the declared template — `N+1` is the one exception, now carrying its method note in §5.1** |
| The next-batch derivation (§7) | pending 590 → lane A 148 → the five records' 40 read pages at sorted indices 0..39, **contiguous** → first eight unread at **40..47**; the record's original list is at **8..15** and is **8/8** batch 2's rows |
| Stability of the §7 citations | batch 1's eight `P#` rows are identical at `0bd37e4d` and `2e523622`; batch 4's `P#` row set is identical at `44d8f431` and the tip `0c994d77` |
| Register cites | `AEGIS-APR-101` heading L3149, independence condition L3155, no-waiver L3157; `AEGIS-APR-117` heading L5016, scope-allowed L5038-L5042, "AEGIS-APR-101's limits continue" L5043-L5044 — identical at `2e523622` and `main` |
| APR-117 sweep of this plan | every `APR-117` occurrence read in context; the plan states **withdrawal-only, no recording power** by content, and offers no label as authority (§8.3, §9); the owner's compound occurs **once** in this file outside §9's inventory, at **its own L608**, in a sentence that cites no register entry — the near-miss §9 records, and the reason §9's inventory refers to "the owner's compound" rather than reproducing it beside a citation |
| Check runs / workflow runs at the head | **0 / 0** (`gh api .../commits/2e523622.../check-runs` and the Actions runs query for the same SHA) |
| Naming check | `C-1`/`C-3`/`C-4` are not rulings anywhere on `main`; `page-resolves-it` is absent from `main`; the ledger on `main` carries none of the labels |
| Capture verification (this revision, revision 5) | blob SHA from `git hash-object` on the committed file; the holding comment's fenced block extracted by the declared method (fence run N, first run of N or longer closes it) + **one trailing LF** reproduces the blob byte-for-byte and is byte-identical to the committed blob; the fence run is longer than any backtick run inside the plan; **zero unsubstituted generator tokens** in the posted body and comment |

**Could not verify (stated, not waved through):** the items of §6 — in particular the record's
corrected diff-scope bytes (a Stage C commit's to make, so they do not exist at this head), the body's
corrected validation rows and the republished digest, the reading act, the model attributions, PR
#781's patch in full, the four non-GitHub CI suites and the Codex comment bodies. `build_index.py`
refuses to run without `refs/pull/**` and `refs/remotes/**` in the clone (measured: it raised
`BuildError` twice before both ref sets were fetched) — the clone used here fetched both (796 PR refs),
which is why its report could be run. Also not reproduced by this planner: **N9** — the index-level
both-directions check that the PR body's validation row 20 states, which requires a `--write` rebuild
in a working tree. **And one earlier claim is carried rather than re-derived:** the `0 malformed`
half of the keeper-table property is the builder's own parse (109 rows read as 109 events); this
revision re-measured the 109 rows, their **9-column** shape and 0 duplicate IDs **directly from the
ledger's own bytes**, but did not independently re-scan for malformed rows, and states that rather than
implying a fresh measurement.

## 13. This plan's own revision and how it is captured

- **Path:** `docs/plans/readability-lane-a-batch-1-stage-a-plan-2026-10-16.md` (this file).
- **Capture method:** committed as a tracked file on the plan's dedicated branch
  (`stage-a/lane-a-batch-1-plan-2026-10-16`) as a **new revision whose parent is revision 4's commit
  `0cce5b33…`** — whose chain runs back through `5f3384df…` to `0bd37e4d…`, the head current when
  revision 1 was captured — and pushed to the repository, so the revision is immutable and the **PR head
  `2e523622…` does not move**; **not** a PR-body-only plan, and not an edit of the PR branch.
  `git diff --name-status 0cce5b33 <this revision's commit>` returns **one line, `M` on this file**:
  the revision adds no other path and changes no other file, so the delivered diff stays the two
  `docs/` paths it already is.
- **The actual identifiers — the capturing branch, the capturing commit and this file's blob SHA — are
  recorded in the PR #771 body**, together with the id of the fresh issue comment on PR #771 that
  holds the same text **verbatim**. They are recorded there rather than here because a file cannot
  contain its own content hash.
- **Binding:** this plan binds head `2e5236222080dc6064df0b493ab83a8a94441176` and acceptance
  revision `e2a3e20b7c20ef8385b219b39c6405237163406f`. **If either moves, this binding is void** and a
  Stage B auditor must audit the revision it can name, exactly as moving a head voids a head-bound
  verdict. The head is expected to move **once** more, when the §14.1 correction lands; that move is
  why §14's four quantities are bound as duties and not as literals (§14.0), and a fresh Stage B on
  this revision and a fresh Stage D at the resulting head are then owed.
- **Editing this file after capture voids an ACCEPT that named the captured revision.**
- **This plan has more than one revision, and this file is not the register of all of them.** Each
  revision was captured separately on the branch above and held by its own immutable comment on PR
  #771, each naming its own file blob and capturing commit; no later revision rewrites an earlier one
  and **no earlier comment is edited**. Stage B must bind the revision its own verdict names.
  Revision 1 is blob `ea048399f14dd13ed91c13ab6d1123dabe9c774b` (58,466 bytes, 727 lines) at capturing
  commit `462d786bf8803d5794c21a6cb0486ff03f5829d8`, held as comment `6213972798`; revision 2 is blob
  `6d579cdca95663f0851ade204adc625d5f315658` (61,173 bytes, 747 lines) at capturing commit
  `e3a4a19c0d048ece8b1121a0437613105bf19771`, held as comment `6214016914`; revision 3 is blob
  `c47b7d908e2beb75ce23940d5ccf19a2595571c2` (63,853 bytes, 775 lines) at capturing commit
  `5f3384df0d9b58a78d1aac3bcbaf89c12689594b`, held as comment `6214392977`; revision 4 is blob
  `324564cd03c589cc92b2d2f7f790b8317b69ac3b` (91,724 bytes, 1,122 newline-terminated lines) at capturing
  commit `0cce5b33aada3a979795be915148ada0863b00c5`, held as comment `6215856084`. **Revision 5 — this
  one — is the revision whose identifiers are recorded in the PR #771 body, for the reason given above;
  it supersedes revisions 1, 2, 3 and 4, and they must not be bound.**
- **How the verbatim claim is verified (method declared, because the newline variant decides the hash).**
  The holding comment wraps the plan in a fence **longer than any backtick run inside the plan**, so
  the plan's own three-backtick fences cannot close it and a reader cannot find the block by taking
  the first three-backtick fence. The declared method here is: take the comment body's first fence
  line, read its backtick run length N, and take every line up to the next line whose backtick run is
  N or longer. That block is the file's bytes **minus the single final trailing newline**, which the
  closing fence line replaces: the normalized variant that matches the blob is **LF with exactly one
  trailing LF appended** (line endings are LF, with no CR anywhere — the repository's `eol=lf`
  policy; PowerShell redirection CRLF-ifies and must not be used to compare the two), and
  `git hash-object` on that byte string returns the blob SHA. The CRLF variants do **not** match, and
  neither does the block as extracted without its trailing newline. The same method was run against
  revision 4 before this revision was written (reproducing `324564cd…` exactly) and against revision 3
  (reproducing `c47b7d90…` exactly), and it is applied to the comment that holds this revision.

---

## 14. The corrections this plan binds, and the sequencing that keeps them true

**Why this section exists.** The record (a file this PR adds) publishes a `base..head` count that is
false of the head it publishes at, and the PR body's validation table states a superseded head, the
wrong commit count and the wrong diff scope. This planner holds **Stage A only** and **must not** edit
the files the PR itself adds, because that would move the head and void every head-bound verdict
downstream. The corrections are therefore **bound here**: with exact replacement text wherever the text
is invariant to the head, and with **derived slots** wherever it is not, so Stage C and the PR editor
have no interpretation latitude and Stage D can check the result mechanically.

### 14.0 The rule this section applies (stated by content, because no label is authority here)

The independent plan audit at comment `6215231275` states the rule revision 4 applied and revision 5
continues to apply, and this plan adopts it **by its content**, not by any label:

> *A plan may not bind, in the same correction round as a head-moving commit, any text that asserts the
> head, the `base..head` diff scope, the commit count or the sign-off count as a final value. Where the
> correction is itself a commit on the PR branch, those quantities are superseded the instant the
> carrying commit lands, because the commit that states them is the commit that changes them. They must
> be bound as a duty to re-derive at the head the head-moving corrections produce, and stated in a
> final metadata pass that contains no further head-moving commit; or they must be expressed in terms
> that are invariant to the move.*

Applied here, the rule produces three bindings:

1. **The record's diff-scope paragraph carries no count a head move can falsify** (§14.1): it states
   the insert-only facts that are true at every head and binds the added-line count as a
   **re-derivation** at the head that publishes it.
2. **The body's four quantities are written only in the final metadata pass** (§14.2), after the last
   head-moving commit, re-derived there by the named commands — never carried from this plan.
3. **The one literal this plan binds inside a bound field is the post-insertion digest** (§14.2b) —
   and it can be a literal precisely because every byte it hashes is invariant to the move: the two
   stale head-stamps inside the field are replaced by re-derivations, not by fresh stamps.

**A worked prediction, stated as a prediction and not as a bound value.** The §14.1 replacement is
exactly **3 lines for the 3 lines it replaces** (below), and it is the only head-moving correction this
plan binds; the ledger is not edited. The head the correction produces is therefore expected to measure
`git diff --numstat e2a3e20b..HEAD` = `576 0` + `151 0` = **727** and `--shortstat` `2 files changed,
727 insertions(+)` — the same figures as at `2e523622` (measured 2026-10-16 by this planner). The
implementer **verifies** this by running the commands at the new head; if any number differs, the bound
text is still sound (it carries no count) and the numbers the final metadata pass publishes are
whatever the commands return.

### 14.1 The head-moving correction — the record's diff-scope paragraph (blob `49d677a9…`, L526-528)

**Present bytes (measured 2026-10-16 at `2e523622`, blob
`49d677a9255925e9f3a91492996d81032c62e81c`, L526-528):**

```text
**Diff scopes, counted by hand (not by regex).** `base..head` is **insert-only**:
**689 added / 0 deleted** over two file headers and three hunks, and with no deleted line at all, no
deleted line
```

(The paragraph continues at L529 with `begins with two dashes. …`, so the replacement's last line must
end where the continuation still reads: its third line ends `… no deleted line`.)

**Binding replacement — exactly three lines, in place of L526-528 (this is the text Stage C commits):**

```text
**Diff scopes, counted by hand (not by regex).** `base..head` is **insert-only** — it adds no
deleted line at all, over two file headers and three hunks — and its added-line count is **re-derived
at the head that publishes this record** (`git diff --numstat e2a3e20b..HEAD`), never carried; no deleted line
```

**One same-line edit in the same paragraph**, so that the surviving historic reference to `445` no
longer points at a removed "head figure above" and the paragraph reads continuously. Both the old and
the new text are inside **L532** (one line, so the file's line count does not change):

The edit is a **substring replacement inside L532 only** — L531, which ends `…this pass's own two`, is
unchanged, and the tail of L532, ` This pass's own`, is unchanged — so the record's line count does not
move. Present substring (the head of L532):

```text
commits; it is superseded by the head figure above and is not a count of this head.)
```

Binding substring:

```text
commits, fixed by immutable commits and not a count of the head that publishes this record — what this record binds is the re-derivation above, and the value for the head it is read at is stated in the PR body's validation rows 4 and 16.)
```

**Why this satisfies the criterion the earlier binding failed.** §5.2 criterion 9 requires that the
record not publish a count false of the head it publishes it at. After this edit the record publishes
**no count for a moving head at all** — it publishes the invariant facts (zero deleted lines, two file
headers, three hunks) and the command that re-derives the count at whatever head reads it. The literal
is published where it can stay true: the PR body's validation rows, written by the final metadata pass
after the last head-moving commit, which moves no head. That is §14.0's rule applied, not evaded: a
number inside a head-moving file is falsified by the next head move, including by the very commit that
writes it — which is exactly what happened to `689`.

**What must not change in this edit:** the intra-branch figures already there (`f6a4e418` vs
`09a7ee1c` = **145 added / 51 deleted** — immutable, between two fixed commits, re-measured and
correct), the `445` historic reference and its `base..f6a4e418` label, the statement that no deleted
line begins with `--`, and every other byte of section 9. **The replacement is line-neutral (3 lines
for 3 lines) and the L532 edit is inside one line**, so this correction adds no line to the diff.

### 14.2 The final metadata pass — the PR body's stale rows and narrative (metadata; moves no head)

**What it is.** One body edit, run **after** the §14.1 commit lands and after any other head-moving
correction is complete, containing **no head-moving commit**. It re-derives the four quantities at the
head it runs at and writes them there. Below, `H` means exactly that head:
`git rev-parse refs/pull/771/head`, re-read in the pass and verified equal to the §14.1 commit.

**Values the pass must derive (commands, all at `H`):**

```text
H      = git rev-parse refs/pull/771/head
n      = git rev-list --count origin/main..H
r / l  = git diff --numstat e2a3e20b..H                      (record / ledger)
r+l    = git diff --shortstat e2a3e20b..H                    ("2 files changed, <r+l> insertions(+)")
dco    = python -B scripts/check_dco.py --range origin/main..H
```

**Binding replacement for each site.** The present text below is quoted from the live body at
`2e523622`; every `<…>` is a value derived at `H`, never a carried one. **Each present and binding
string is given as a fenced block, so no markdown escape character (a backslash before a backtick) is
part of any string: copy the block text exactly, character for character.** Where a binding says
`<H>`, it means the 40-hex head re-derived at the pass, not the digits.

**Row 1 (live body L211).** Present (the Result cell):

```text
0bd37e4dbb27ef108ca13ccbc0cbf4a673ef6b27
```

Binding:

```text
<H>
```

**Row 2 (L212).** Present:

```text
4 commits (the record commit and this repair commit, both DCO-signed)
```

Binding:

```text
<n> commits (the record commit 09a7ee1c9beefbb16d7fab0a608fa3a155879d5a, the Stage F repair f6a4e4189ecfbe874f97ec9b6b09bf8fe14f49ad, the Stage C repair 7b010eeab20901c1ce5450dd5db0e5cb955189ea and its citation correction 0bd37e4dbb27ef108ca13ccbc0cbf4a673ef6b27, and this correction commit <H> - all DCO-signed)
```

**Row 4 (L214).** Present:

```text
`556 0` (batch record) and `133 0` (ledger) — **the same command and the same head as row 16; the earlier `334 0` / `111 0` reading is the `base..f6a4e418` scope and is superseded.**
```

Binding (`<r>` and `<l>` are the numstat pair at `H`):

```text
`<r> 0` (batch record) and `<l> 0` (ledger) — **the same command and the same head as row 16; the earlier `334 0` / `111 0` reading is the `base..f6a4e418` scope, and the `556 0` / `133 0` reading is the `base..0bd37e4d` scope; both are superseded.**
```

**Row 13 (L223).** Present:

```text
exit 0 at this head: `SIGNED` for all four commits, `OK: 4 commit(s) checked, all signed off or exempt`
```

Binding:

```text
exit 0 at this head: `SIGNED` for all <n> commits, `OK: <n> commit(s) checked, all signed off or exempt`
```

**Row 16 (L226).** Present:

```text
`556 0` (batch record) and `133 0` (ledger): base..head is **insert-only — 689 added / 0 deleted**, counted from the raw patch by hand, not by regex; no deleted line begins with `--`
```

Binding:

```text
`<r> 0` (batch record) and `<l> 0` (ledger): base..head is **insert-only — <r+l> added / 0 deleted**, counted from the raw patch by hand (<r+l+2> `+` lines minus the 2 file headers), not by regex; no deleted line begins with `--`
```

**Row 16 must not be left behind again:** the earlier binding updated rows 1, 2, 4 and 13 and left row 16
stale, which is half of the defect this revision exists to close.

**Row 19 (L229).** Present command cell:

```text
`python tools/readability_acceptance/build_index.py --repo . --ref 0bd37e4dbb27ef108ca13ccbc0cbf4a673ef6b27 --report`
```

Binding: the same command with `--ref <H>`, and the figures it returns (re-measured at `2e523622`:
`table_rows 109, events 109, full_page_acceptances 89, lost_commit_events 10, reader_pages_with_rows 76`).

**Paths paragraph (L75-77).** Present:

```text
numstat `556 0` (batch record) and `133 0` (ledger) — insert-only at this head, 689 added / 0 deleted counted from the raw patch by hand, and no deleted line begins with `--`.
```

Binding:

```text
numstat `<r> 0` (batch record) and `<l> 0` (ledger) — insert-only at this head, <r+l> added / 0 deleted counted from the raw patch by hand, and no deleted line begins with `--`.
```

**Acceptance-criteria paragraph (L84).** Present:

```text
AC6 (DCO over `origin/main..HEAD`) SIGNED — 4 commits at this head.
```

Binding:

```text
AC6 (DCO over `origin/main..HEAD`) SIGNED — <n> commits at this head.
```

**Known skips (L237, L250) and Next action (L260) — a rule, not three literals.** Every `0bd37e4d…`
in the body that names the head at which a stage or a record is **owed** becomes `<H>`. The Row source
comments inside the skills field and the historic pass-1/pass-2/pass-3 statements are **provenance**
(the head each row was authored at) and stay as they are.

**Attribution (L12).** Present:

```text
`0bd37e4dbb27ef108ca13ccbc0cbf4a673ef6b27` (the new head, DCO-signed)
```

Binding:

```text
`0bd37e4d…` (the head when this repair landed, DCO-signed)
```

**Revision-1 receipt narrative (L323-326).** Present:

```text
(1) The **record** (not this body) prints `445 added / 0 deleted` at its L508-509 — that is the `base..f6a4e418` scope, and it is false of this head, where `base..head` is **689 added / 0 deleted** (`556 0` record + `133 0` ledger; 691 `+` lines in the raw patch minus 2 file headers; 0 deleted lines; 2 `-` header lines; 3 hunks).
```

Binding (time-qualified, so the sentence is true whenever it is read):

```text
(1) As measured at the head this receipt was written for (`0bd37e4d…`), the **record** (not this body) printed `445 added / 0 deleted` at its then-L508-509 — that is the `base..f6a4e418` scope, and it was false of that head, where `base..head` measured **689 added / 0 deleted** (`556 0` record + `133 0` ledger; 691 `+` lines in the raw patch minus 2 file headers; 0 deleted lines; 2 `-` header lines; 3 hunks). At the head this text is read at, the record's diff-scope paragraph sits at L526-528 and the live figures are the validation rows' own, re-derived in the final metadata pass.
```

**Digest line (L192-205) and validation row 21 (L231).** Present value `4cd96b537eb398a1` with
normalized lengths `1262 / 17182 / 40`. Binding: `b78221cc2ae8f394` with lengths `1262 / 19172 / 40`
— the value §14.2b produces — and the paragraph records the head `H` the pass ran at and the moment,
so that the "when" of every number is recorded **outside** the bound fields, where it cannot go stale
inside a hashed payload.

**The pass publishes its own receipt** — `H`, the moment, and the derived values — in the digest line's
paragraph and in the validation table, so that the "when" of every number is recorded **outside** the
bound fields, where it cannot go stale inside a hashed payload.

### 14.2b The Stage A skills row — insertion point, exact text, head-invariant stamps, and the recomputable digest

**Insertion point (exact).** In the `skills` bound field (sentinels at body L114 and L146 at
`2e523622`), **immediately after the last data row** — the round-3 `scoped-approval-register` row
whose Result cell ends `… the merge holder reconciles the two row sets. |` — and **before the blank line
that precedes the owed-records note**: the new row becomes the table's **13th data row**, directly under
the 12th. (The earlier revision bound the row's text but not its place; seven candidate places give
seven different digests, which is why the place is bound here.)

**The exact row text (four columns, one line):**

```text
| `source-of-truth-reconciler`, `change-classification-gate` | Stage A / `readability-lane-a-stage-a-planner` (DeepSeek-4.1-Flash, deepseek-flash), plan revision 5 | WHAT: re-derived this PR's correction state at head `2e5236222080dc6064df0b493ab83a8a94441176` from the repository rather than from revision 3 — the two-path diff (`576 0` record + `151 0` ledger = 727 added / 0 deleted), the five commits and the DCO count, the record's false `689` at its L526-528, the two `**partial**` strings at L443/L444, the ledger section at L5114-L5255 with rows K-082..K-089 at L5379-L5386, the five lane-A batch records' 40 read pages (sorted indices 0..39) and the first eight unread (40..47), and the bound-field digest `4cd96b537eb398a1` reproduced from the live body after four sibling calibrations. WHY: revision 3's section 14 bound head-stamped values that applying them falsified — the record publishes `689` where its own head measures 727, and the body's rows 1, 2, 4, 13 and 16 state a superseded head, four commits where there are five, and `556 0` / `133 0` where the head measures `576 0` / `151 0`. HOW: one fresh HTTPS clone; every number from a named command (plan section 12). | The four head-stamped quantities (the head, the `base..head` scope, the commit count and the sign-off count) are bound as a duty re-derived at the head the head-moving corrections produce and stated in a final metadata pass that contains no further head-moving commit (plan section 14); the skills-row insertion point and the post-insertion digest are bound in plan section 14.2b. **Limit:** this row is not an ACCEPT of anything; the plan's Stage B audit is owed and is not held by this agent. |
```

**Two further in-field edits that must go in the same edit**, because the digest hashes all three
payloads and a later in-field edit would invalidate a digest published earlier:

1. **L127 (row 10's Result cell), its last sentence.** Present substring:

   ```text
   Stage D/E/F are owed at `0bd37e4d…`.
   ```

   Binding substring:

   ```text
   Stage D/E/F are owed for the head this row is read at (re-derived with `git rev-parse refs/pull/771/head`; never carried in this field).
   ```

2. **L131, the whole owed-records note** — replace the present line

   ```text
   Stage A (plan author) and Stage B (plan auditor) rows are owed - no plan-author or plan-auditor skills records were produced for this lane's pass at any head, and Stage D, Stage E and Stage F rows are owed for the new head 0bd37e4dbb27ef108ca13ccbc0cbf4a673ef6b27 (every stage re-runs after the head moves). No plan-author or plan-auditor record exists at any head, so the owed note is unchanged in substance.
   ```

   with

   ```text
   Stage A (plan author) is recorded: the row inserted above is this plan's Stage A skills record, and the plan's captured blob SHA, capturing commit and holding comment id are published in this body's "Captured Stage A plan" section, outside the bound fields. Stage B (plan auditor) is owed — no plan-auditor skills record was produced for this lane's pass at any head. Stage D, Stage E and Stage F rows are owed for the head this note is read at: every stage re-runs after the head moves, so the operative head is re-derived at reading time with `git rev-parse refs/pull/771/head` and never carried in this field.
   ```

   The replacement names **no head at all**: the rows that remain owed are owed for **the head the note
   is read at**, re-derived by command. That is §14.0's "invariant to the move" limb, and it is why the
   digest below can be a literal.

**The recomputable value.** Applying exactly those three edits to the body at `2e523622` — whose
three-field digest is `4cd96b537eb398a1` with normalized lengths 1262 / 17182 / 40 — produces:

- **digest `b78221cc2ae8f394`** (full SHA-256
  `b78221cc2ae8f394c34c26ad1dace7a722c6e4ec456faf61057f6b03c8b5ef4d`), normalized payload lengths
  **1262 / 19172 / 40** (witness / skills / security).

**The one token that moved, and the value it moved from.** Revision 4 bound this same guard with the
digest **`e6d9809812112231`** (full
`e6d980981211223149af641308e93485b86a3407abeeb4bd6d72057dfa0426e9`, the same lengths) over a row text
identical to the one above **except for one token**: revision 4's row named `plan revision 4` in its
stage cell, and this one names `plan revision 5`. That token sits inside a bound payload, so the digest
moves with it. **The input that changed is named, and both values are computable** from the live body
at `2e523622` by the method above: nothing else in the three payloads, and no other bound edit, differs
between them. A reader confirms it by computing either value from the row text in this section plus the
two `L127` / `L131` bindings above — the revision-4 row text is byte-identical to this one apart from
that token, and it is preserved in revision 4's own committed blob `324564cd…` (§13).

The method is the body's own declared one, unchanged: extract each sentinel-delimited payload in the
published order **witness, skills, security**, collapse each payload's whitespace runs to single
spaces, trim, join the three with single newlines, SHA-256 over the UTF-8 string, take the first 16
hex. This planner recomputed the baseline value and the four sibling calibrations before computing this
one (`#783 3913683c686e6e71`, `#787 82ed906d2f228f0e`, `#792 88300e711714200a`,
`#795 5fabf87b2df899e9`, each from its own live body, with line endings normalised after fetch —
PowerShell redirection CRLF-ifies and would make a correct method falsely read 0/4).

**Obligation, and the one way this literal can be wrong.** The pass **recomputes** this digest from the
live body after the three edits and **publishes what it computes**; the value above holds when the
three payloads differ from the `2e523622` reading by exactly these three edits and nothing else. If any
other byte inside the three payloads has changed between this plan's capture and the pass, the literal
is superseded: the pass publishes the recomputed value, states that the precondition failed, and names
the differing bytes. It must **not** publish `b78221cc2ae8f394` on a body it did not compute it from —
that is the receipt defect this programme has already seen six times (five receipts, and this plan's
own revision 4, whose digest moved when its Stage A row's revision token changed).

**What the pass must not do to the fields.** It edits nothing else inside the three payloads: not the
Row source comments (L133-L144), which are provenance and state the head each row was authored at; not
the witness or security payloads; not the gloss paragraph above the witness field.

### 14.3 The next-batch labelling — already applied at `2e523622`; nothing further is bound

The 17-line labelling block is present in all three places (record L339-355, ledger L5221-L5237, body
L278-294), inserted by the Stage C commit `2e523622`; this planner re-derived its output independently
(`check_index.py`'s own `classify_tree`, then the five records' own bytes: 8/8 the eight paths at
sorted indices 40..47). **No further correction is bound here.** The three copies remain as applied.

### 14.4 What must NOT change

The acceptance revision stays `e2a3e20b…`; the eight pages' bytes, blob SHAs, line and byte counts stay
as recorded; **no page under `.claude/` is edited** (that would reclassify the change out of
`docs-only`); no keeper row and no withdrawal row is authored by the corrections; the index is not
rebuilt; no tool, workflow, approval, script or test byte changes; the corrections touch only the two
paths already in this PR's diff (§14.1) plus PR metadata (§14.2, §14.2b). **The three bound fields are
edited only by §14.2b, in the final metadata pass, with the digest recomputed and republished**. **No
further head-moving commit may follow the §14.1 commit**, or the pass's numbers are superseded and the
pass must be re-run at the new head.

### 14.5 When it becomes decidable, and the two-phase order

At this head only §14's **binding** is decidable (criteria 9 and 10 of §5.2 are declared not verifiable
at this head for this reason — N1 and N2; criterion 11 is now verifiable and is checked). The corrected
record's bytes become decidable at the §14.1 commit; the body's rows and the republished digest become
decidable at the final metadata pass; the pass's own state — that it contained no head-moving commit —
is decidable by comparing `git rev-parse refs/pull/771/head` before and after it. **Order: (1) the
§14.1 commit; (2) the final metadata pass, body only, containing §14.2 and §14.2b; (3) a fresh Stage B
on this plan's revision and a fresh Stage D at the head those two steps produce.** The correction moves
the head deliberately and visibly at Stage C rather than as a side effect of this plan's own capture,
which is exactly why this planner does not apply them here.

*Prepared by a **DeepSeek-4.1-Flash** agent (`deepseek-flash`), Stage A only, under the owner account
as the repository's attribution rule requires. Revision 5 (2026-10-16) — re-captured on the **SD-B**
REVISE at comment `6216259175` (the independent plan audit of revision 4), which found the ledger's
keeper table called "8 columns" where it is **9**, two line counts stated under a method that returns a
different number, and a residual inventory narrower than the defect it describes. All three are fixed
here, each measured by command; nothing the earlier audits accepted was undone. This plan holds no
Stage B, D, E, F or G on this change; it audited nothing, edited no file of the PR's diff, moved no head
and merged nothing.*
