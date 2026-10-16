# Stage A plan — Phase 4 readability re-read, lane A, batch 1 (PR #771)

**This file is the captured Stage A plan for PR #771.** It is captured as a tracked file committed on
its own branch, so its revision is immutable and a Stage B auditor can bind the exact text. The
branch, the capturing commit and **this file's blob SHA of the captured revision** are recorded in the
PR #771 body, together with the id of a fresh issue comment on that PR carrying the same text
verbatim (a file cannot contain its own content hash).

- **Planner:** DeepSeek-4.1-Flash (`deepseek-flash`), **Stage A only**. This planner is **not** the
  auditor of this plan and holds **no** Stage B, D, E, F or G on this change; it authored no keeper
  row, edited no file of the PR's diff, moved no head, and merged nothing.
- **Work item:** *Phase 4 readability full-page re-read — lane A, batch 1* — the work delivered by PR
  #771 (the eight keeper rows K-082..K-089 and the batch record they cite).
- **Head this plan plans against:** `0bd37e4dbb27ef108ca13ccbc0cbf4a673ef6b27` (40 hex, re-derived
  by `git rev-parse refs/pull/771/head`), head tree
  `7e74d05faaeeb2d64aea5808b3f63a0054c4f652`.
- **Base / merge base:** `e2a3e20b7c20ef8385b219b39c6405237163406f` (tree
  `effc72501297375d490705eaae686a0c181df2e6`); `git merge-base origin/main refs/pull/771/head`
  returns exactly it. This is also **the acceptance revision** — the revision every one of the eight
  keeper rows binds and at which the eight pages were read.
- **Stage context.** The PR's own skills table records that **Stage A (plan author) and Stage B (plan
  auditor) rows are owed — no plan-author or plan-auditor record was produced for this lane's pass at
  any head** (body L131). This file is that Stage A output. The PR is otherwise mid-repair: its three
  repair commits (`f6a4e418`, `7b010eea`, `0bd37e4d`) answer one Stage F REVISE, one Stage D REVISE
  and a coordinator ruling, and a **fresh Stage D is owed at this head**.

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

Every figure below was produced by a command in a fresh HTTPS clone by this planner on 2026-10-16
(`git clone -c http.sslBackend=openssl`; the shared clone was **not** used or cleaned; no worktree was
created). **Three places where what I measured differs from the brief I was given, or from the PR's
own bytes, are marked ⚠ and planned against as found.**

| # | Fact | Measured value |
| --- | --- | --- |
| 1 | Head | `0bd37e4dbb27ef108ca13ccbc0cbf4a673ef6b27` — `refs/pull/771/head` and `refs/heads/docs/readability-lane-a-batch-1-20261015` both resolve to it |
| 2 | Base = merge base | `e2a3e20b7c20ef8385b219b39c6405237163406f` (`git merge-base origin/main refs/pull/771/head`) |
| 3 | `main` at this reading | `38413563a843f030d3ac992b375b5db5528f2926` (advanced past the PR's base; the PR is CONFLICTING/DIRTY — not resolved here) |
| 4 | Commits in `base..head` | **4** (`09a7ee1c`, `f6a4e418`, `7b010eea`, `0bd37e4d`) |
| 5 | Files in `base..head` | **2**, both Markdown under `docs/` |
| 6 | `git diff --shortstat` | `2 files changed, 689 insertions(+)` — insert-only |
| 7 | `git diff --numstat` | `556 0` batch record, `133 0` ledger; `556+133 = 689` |
| 8 | Raw patch, hand-counted | **691** lines beginning `+` (= 689 added + 2 `+++` file headers), **2** beginning `-` (both `---` headers), **3** hunks |
| 9 | DCO over `origin/main..head` | exit 0 — `OK: 4 commit(s) checked, all signed off or exempt` |
| 10 | `git diff --check` | exit 0, no output |
| 11 | Check runs / workflow runs at the head | **0 / 0** (the PR is DIRTY against `main`, so no `pull_request` run can build a merge commit) |
| 12 | Record blob at head | `1c8ba69f648df11a027de7523d39fdaa380ba1a2` — 45,835 bytes, **556** newline-terminated lines |
| 13 | Ledger blob at head | `12c7c08c5afc95ce7e41617d03b460d4e7e64cf8` — 498,478 bytes, 5,369 lines; consolidated table = **109** data rows (K 89 + L 10 + T 10), 0 malformed, 0 duplicate IDs |
| 14 | Instrument at the base (`check_index.py --json --ref e2a3e20b`) | `653 / 57 / 4 / 586 / 0 / 0 / 6 / 596`; pending union (`586+4`) = **590**; quarters **148 / 148 / 148 / 146** |
| 15 | `build_index.py --ref 0bd37e4d --report` (full clone with `refs/pull/**`) | exit 0: `table_rows 109, events 109, full_page_acceptances 89, lost_commit_events 10, reader_pages_with_rows 76` |
| 16 | The eight pages' blob / lines / bytes at the base | all eight reproduce the record's and the body's figures **exactly** (table in §2) |
| 17 | PR body bound-field digest, recomputed from the live body by the body's own declared method | `4cd96b537eb398a1` (full `4cd96b537eb398a19bb8c2cd608b22f48c7695b29b21f74e30d4dc9580d748b0`), normalized lengths **1262 / 17182 / 40** — **exactly the published value** |

**⚠ Difference 1 — the "445" figure is in the RECORD, not in the body, and the body contradicts
itself as well.** The brief says the body "says '445 added' where the record and its own body row say
689". Measured: the **record** (a file this PR adds) says, at its **L508-509**:

> `**Diff scopes, counted by hand (not by regex).** \`base..head\` remains **insert-only**:`
> `**445 added / 0 deleted** over two file headers …`

and the record contains **no** occurrence of `689` at all. The **body** says **689** in two places
(L76 and validation row 16) **and** carries a stale row 4 whose two numbers (`334 0` + `111 0`)
**sum to 445**. So the contradiction exists in both artifacts, but the brief's attribution is
transposed: `445` is the record's figure (and the body's stale row 4), and `689` is the body's. Both
`445` readings are the `base..f6a4e418` scope, measured by me: `git diff --numstat e2a3e20b..f6a4e418`
= `334 0` + `111 0` = **445**; at the head the same command returns `556 0` + `133 0` = **689**. §14
binds both corrections with exact replacement text.

**⚠ Difference 2 — "its record is bound to `f6a4e418`" is not what the bytes show.** No keeper row,
and no part of the record, binds `f6a4e418`: all eight rows' **Acceptance revision** is
`e2a3e20b7c20ef8385b219b39c6405237163406f`, and `git grep -c f6a4e418 <head> -- docs/` returns exactly
one file — the record — with 4 mentions, none of them a row binding. What binds `f6a4e418` is the
**earlier Stage D REVISE** (issue comment 6209064290) and the record's own section-9 digest claim
(`b1acc2b2f5817fab` with payload lengths 1262 / 11819 / 40). The distinction matters because §14's
corrections must not be read as re-binding a row.

**⚠ Difference 3 — the record's next-batch list is not the first eight entries of the unread
sequence at the state its own section measures.** §7 derives it: the eight paths the record names sit
at lane-A sorted indices **8..15**, which lane A **batch 2 has already read**; under the read set the
record's own cross-check asserts (indices 0..39), the first eight unread are indices **40..47**. This
is a statement-vs-measurement defect of the same class as `445`, and §14 binds its correction.

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

**The two paths the PR's diff touches (the deliverable):**

| Path | Status | At head | In the diff, `base..head` |
| --- | --- | --- | --- |
| `docs/evidence/documentation/readability-lane-a-batch-1-2026-10-15.md` | new | blob `1c8ba69f…`, 45,835 bytes, 556 lines | `556 0` |
| `docs/roadmaps/aegis-documentation-readability-backlog.md` | modified | blob `12c7c08c…`, 498,478 bytes, 5,369 lines | `133 0` (the lane-A section inserted at L5114 and rows K-082..K-089 appended at L5361-5368) |

**Not touched — named so that it is not implicit.** This PR's diff contains **no** page text
correction; **no** change to any of the eight read pages under `.claude/`; **no** change to
`docs/delivery-workflow.md`, `AGENTS.md`, `CONTRIBUTING.md`, any `.claude/skills/**` file, any
`scripts/**` path, any `tools/**` path, any `.github/**` workflow, any test, any configuration, data
or lock file; **no** rebuild of `tools/readability_acceptance/acceptance-index.json` (no
`build_index.py --write`); **no** new keeper row and **no** withdrawal row authored by the three
repair commits; **no** merge, no rebase, no force-push; **no** other lane's branch, PR, clone or
worktree. **This plan adds nothing to that diff**: it is captured on its own branch whose parent is the
PR head, so the delivered diff stays two files and the head does not move.

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

**Blast radius.** Two files, **+689 / −0**, four commits, both paths Markdown under `docs/`:

```text
git diff --name-only  e2a3e20b7c20ef8385b219b39c6405237163406f..0bd37e4dbb27ef108ca13ccbc0cbf4a673ef6b27
  docs/evidence/documentation/readability-lane-a-batch-1-2026-10-15.md
  docs/roadmaps/aegis-documentation-readability-backlog.md
git diff --numstat  <same range>   ->  556 0  (record)   133 0  (ledger)
git diff --shortstat <same range>  ->  2 files changed, 689 insertions(+)
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
| `N+1` | 15 | 2.3% | at/above — convention |
| `MFA` | 10 | 1.5% | **below** — gap candidate |
| `AuthN` | 1 | 0.2% | **below** — gap candidate |
| `AuthZ` | 1 | 0.2% | **below** — gap candidate |

**The rule, stated so it is decidable:** a term used on **~12 or more** of the 653 reader pages is a
library-wide convention; an unglossed first use of it is recorded as an **OBSERVATION**, not a gap, and
**may not make a page fail**. A term below the threshold may be a gap, but a gap still needs the page's
own line cite.

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
| 1 | The diff `base..head` is exactly **two** Markdown paths under `docs/`, insert-only (`+689/−0`), and contains **no** code, script, workflow, test, config, data or lock file (the pure-docs condition). | `git diff --name-only` / `--numstat` / `--shortstat` / `--check` | **yes** — measured: 2 paths, `556 0`+`133 0`, exit 0 |
| 2 | The change classification **`docs-only`** is recorded **inside the plan** (element 3), not only in the PR's skills table. | §4 of this file + criterion 1's file list | **yes** |
| 3 | All eight pages are named **by path**, bound to the full 40-character acceptance revision, each with a disposition, and the six acceptance bullets are addressed per page. | the record's own bytes; `git rev-parse` / `git cat-file -s` per page | **yes** — measured: 8/8 paths, 8/8 blob SHAs and line/byte counts reproduce ▼ |
| 4 | The eight pages are **untouched** by the diff (the bytes read are the bytes merged), so no acceptance is voided by the merge of this head. | the two-path file list (§3) against the eight page paths | **yes** — measured: intersection is empty |
| 5 | The C-1 screen is stated with **measured prevalence for every term the record's gap list turns on** and applied: **YAML 32, API 204, MCP 28** of 653 — all at/above the threshold, so none may make P8 fail; no criterion in this plan treats them as gaps. | §5.1 (commands and numbers, re-runnable) | **yes** — measured in this plan's own run |
| 6 | **No page recorded PARTIAL carries an acceptance row, and no page recorded PARTIAL deserves its row** (the both-directions rule): at this head the record records **zero** partial pages among the eight and `check_index.py --path` reports each of the eight `full-page-acceptance`, `changed_lines 0`. | `build_index.py --report --ref <head>`; `check_index.py --json --path <page> --ref <head>` × 8 | **yes** — measured: `full_page_acceptances 89`, and all eight report an acceptance with 0 changed lines |
| 7 | The record's own appended evidence is machine-visible: the ledger's consolidated table holds **109** data rows, **0** malformed, **0** duplicate IDs, and the builder reports `table_rows 109, events 109, full_page_acceptances 89, lost_commit_events 10, reader_pages_with_rows 76` at this head. | `build_index.py --report --ref 0bd37e4d` in a clone holding `refs/pull/**` and `refs/remotes/**` | **yes** — measured exactly |
| 8 | Every load-bearing figure in the record that this plan re-derived **reproduces**: the eight line/byte counts, the eight blob SHAs, the instrument's eight summary figures, the pending union 590, the quarters 148/148/148/146. | §1 rows 13-16; §7 derivation | **yes** — measured |
| 9 | The diff-scope count the record publishes **matches the head it publishes it at**: `base..head` is **689 added / 0 deleted** (the record says 445 — see §14.1, a Stage C correction). | `git diff --numstat` at the head; §14.1 | **no at this head** — the record's bytes say 445; declared **N1** in §6 and bound in §14.1 |
| 10 | The PR body's validation table does not contradict itself: rows 1, 2, 4 and 13 are re-stated for the head (`rev-parse HEAD` = `0bd37e4d…`; 4 commits; `556 0`/`133 0`; DCO 4/4 signed). | the live body + `gh api`; §14.2 | **no at this head** — the live body says `f6a4e418`/`2 commits`/`334 0`+`111 0`/`3 commits`; declared **N2** and bound in §14.2 |
| 11 | The next-batch list is labelled by the state it was measured at, and the first eight **unread** pages at the acceptance revision are named by path: derived = lane-A indices **40..47** (§7), while the record names indices **8..15** (batch 2's pages). | §7's three-step derivation, re-runnable | **no at this head** — the record's bytes name indices 8..15 unlabelled; declared **N3** and bound in §14.3 |
| 12 | Every page path this PR **reads** is distinct from every path it **writes**: the eight read pages appear nowhere in the diff, and the two written paths are not among the 653 reader pages' acceptance rows authored here. | file list + `git grep` over the diff | **yes** — measured: empty intersection |
| 13 | The capture exists: this plan is a tracked file whose **blob SHA and capturing commit** are recorded in the PR #771 body **and** in a fresh issue comment holding the same text verbatim, with the earlier comments unedited. | the body text; the comment id and its extracted fenced block hashed against the committed bytes | **yes** — the capture receipt is in the PR body; the verbatim check is reproducible by extracting the fence and hashing (the fence-strip read differs from the committed bytes by exactly one trailing newline) |
| 14 | The capture edit **does not disturb the PR's bound fields**: the published bound-field digest still recomputes to `4cd96b537eb398a1` under the body's declared method. | the declared method, recomputed over the live body before and after the edit | **yes** — measured before the edit (reproduced exactly) and re-measured after |
| 15 | Branch hygiene: every commit on the plan's own branch is DCO-signed, `git diff --check` is clean, and the body's bound fields still parse. | `scripts/check_dco.py --range`; `git diff --check`; `scripts/ci/check_pr_body_skills.py --body-file` | **yes** — measured: body checker `PR body bound fields: OK` before the edit, re-run after |

▼ Criterion 3's page-level truth (that each bullet was judged *per page*) is only as strong as the
record's own text; the parts of it that no artifact can carry are declared in §6 (N4, N5).

## 6. Criteria declared not verifiable at this head, with reasons (element 5)

The workflow permits a criterion to be `UNRUN` at Stage D **only** if the plan at SD-A declared it
not verifiable at this head with its reason. These are so declared. None of them may be used to force
a disposition on this PR; each is excluded from §5.2's passing set.

- **N1 — the record's corrected diff-scope bytes ("689 added / 0 deleted").** The corrected bytes are
  a **Stage C commit's** to make; this planner holds Stage A only, and editing a file the PR itself
  adds would move the head and void every head-bound verdict (it is also outside a planner's stage).
  Reason: the criterion measures bytes that do not exist at this head. **What is decidable now:** that
  the record's present bytes say 445 while the head's diff is 689 — measured, and bound in §14.1.
- **N2 — the PR body's corrected validation rows.** The body is PR metadata, not a candidate file, so
  correcting it moves no head; but the correction is not this planner's to publish *as a result*, and
  the same rows' correctness depends on which head they are stated for. Reason: the corrected text
  does not exist in the live body at this head. **Decidable now:** that the live rows contradict the
  measured head (row 1 `f6a4e418` vs `0bd37e4d`; row 2 "2 commits" vs 4; row 4 `334 0`+`111 0` vs
  `556 0`+`133 0`; row 13 "three commits" vs 4) — measured, and bound in §14.2.
- **N3 — the corrected next-batch list.** Same reason as N1: the record's, the ledger's and the body's
  copies of the list are corrected by a later stage's commit, not by this plan. **Decidable now:** the
  derivation of §7 and the statement-vs-measurement defect it exposes.
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
   `refs/heads/docs/readability-lane-a-batch-1-20261015` `0bd37e4d` (blob `1c8ba69f`);
   `…batch-2-20261015` `8b0ba011`; `…batch-3-20261015` `7b0e9f60`; `…batch-4-20261015` `44d8f431`;
   `…batch-5-20261015` `864461c7` — the eight `| P# | path |` rows of each record.
3. **The next eight.** The first eight paths of (1), in repository-path order, that are not in (2) —
   **named by path**, never by index.

**My derivation, run at the acceptance revision (2026-10-16), reproduces the record's own
cross-check and falsifies its list:**

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

**The defect this exposes (⚠ Difference 3, §1).** The record names, as "the first eight entries of the
unread sequence at this base", the eight paths at lane-A sorted indices **8..15**
(`ab-test-designer` … `adr-sequencer`) — which are **exactly the eight pages lane A batch 2 has
already read** (measured: batch 2's record's eight `P#` rows are those paths, 8/8). They were the
first eight unread **at the moment batch 1 was the only lane-A record**; they are not the first eight
unread under the read set the same section asserts two paragraphs earlier ("lane A's own reads are
indices 0..39 with no gap"). The ledger's appended section and the PR body repeat the same list. The
rule's content is unaffected — the list must be re-measured at the next implementation base anyway —
but the record publishes a figure its own measurement contradicts, so §14.3 binds a labelling
correction.

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
   rides on it: the record publishes one figure (`445 added`) that is false of its own head (689) and
   another (the next-batch list) that its own measurement contradicts — defects that only a captured
   plan can bind without moving the head. *Routing: **cite*** — the PR's owed-stage record, §1's
   measurements and §14's bound corrections.
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
   Commit **one** Markdown plan file on its own branch whose parent is the PR head, and add one
   out-of-bound-field capture reference to the PR body plus one fresh comment. No page edited, no
   keeper row authored, no ledger byte changed by this planner, no tool, workflow, check, approval or
   index touched, no tier downgraded, no scope widened, **no bound field edited**, and **the head does
   not move**. *Routing: **smallest change***.
5. **Complexity justification — why is this machinery warranted, and what would be smaller?** The
   machinery is the workflow's own minimum: Stage B cannot audit what was never captured, and a plan
   may be small but never absent. Smaller alternatives and why they fail: **a plan paragraph in the PR
   body is not a capture** (the workflow says so explicitly, and three PRs in this programme were
   returned REVISE for exactly that); **a comment alone** is allowed by the workflow but weaker than a
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

## 10. The evidence the work will produce, and where it lives (element 9)

| Evidence | Where it lives |
| --- | --- |
| The eight dispositions, their six-bullet judgements, the purpose/normal-use restatements and the eight verbatim row-quote strings | `docs/evidence/documentation/readability-lane-a-batch-1-2026-10-15.md` at head `0bd37e4d` (blob `1c8ba69f…`, 556 lines) |
| The eight keeper rows K-082..K-089 (full-page-acceptance, bound to `e2a3e20b…` with the page's blob SHA in the row) | `docs/roadmaps/aegis-documentation-readability-backlog.md` L5361-5368 at head (blob `12c7c08c…`) |
| The lane-A section: derivation, keeper-independence defect and routing, count honesty, self-cost, next-batch rule | same ledger, L5114-L5253 |
| The pages' bytes at the acceptance revision and their blob SHAs / line / byte counts | the git objects at `e2a3e20b…` (§2's table, re-measurable by command) |
| The instrument's counts (`653 / 57 / 4 / 586 / 6 / 596`), the 590-path pending set and the 148-path lane-A quarter | `check_index.py --json --ref e2a3e20b…`; recorded in the record's §1 |
| The C-1 prevalence screen | §5.1 of this file — commands and per-term numbers, re-runnable |
| The next-batch derivation and its output at the base | §7 of this file — three steps, one output list, not a pinned range |
| **The capture of this plan** | this file's **blob SHA** and the **capturing commit**, published in the PR #771 body, plus the **fresh issue comment** on PR #771 carrying the same text and its id |
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
8. **It does not re-derive** the items declared not verifiable in §6 (N1-N8).
9. **It does not perform Stage C.** The corrections of §14 are the implementation stage's to commit —
   this planner holds Stage A only, and applying them would move the head deliberately and visibly at
   Stage C rather than as a side effect of the plan's own capture. **Applying §14 will move the head**;
   when it does, the criteria that measure the base-to-head diff (1, 3, 4, 8, 12) must be re-derived at
   the new head and this plan's head binding must be re-read as §13 states.
10. **It does not edit any bound field of the PR body.** Adding the Stage A skills row is an owed
    *governance-table* edit that moves the `skills` bound field and therefore the published digest —
    which the live Stage D verdict at this head (comment `6210951972`) has certified as
    `4cd96b537eb398a1`. This plan therefore **authors its own Stage A row and publishes its exact text
    outside the bound fields** (§14.2b) and routes its insertion, with the digest republication, to the
    PR editor / the stage that owns the next metadata edit, rather than moving a field a live verdict
    named.

## 12. Verification ledger — what was run, and what could not be verified

Run by this planner on 2026-10-16 in a fresh HTTPS clone (`git clone -c http.sslBackend=openssl`
https://github.com/ModernNomad-98/Project-Aegis.git; the shared clone was **not** used or cleaned; no
worktree was created; `git config user.name` was read **first** and is `Peter Nguyen`):

| Check | Result |
| --- | --- |
| `git rev-parse refs/pull/771/head` and the PR branch ref | both `0bd37e4dbb27ef108ca13ccbc0cbf4a673ef6b27` — **the head has not moved** |
| `git merge-base origin/main refs/pull/771/head` | `e2a3e20b7c20ef8385b219b39c6405237163406f` |
| Head tree / base tree | `7e74d05f…` / `effc7250…` |
| `git rev-list --count base..head` / `origin/main..head` | 4 / 4 |
| `git diff --name-only` / `--numstat` / `--shortstat` | 2 paths; `556 0` + `133 0`; `689 insertions(+)` |
| Raw-patch hand count | 691 `+` lines (689 + 2 headers), 2 `-` lines (headers), 3 hunks |
| `git diff --check` | exit 0 |
| `scripts/check_dco.py --range origin/main..0bd37e4d` | exit 0 — 4 commits, all SIGNED |
| `scripts/ci/check_pr_body_skills.py --body-file <live body>` | exit 0 — `PR body bound fields: OK` |
| Bound-field digest, recomputed from the live body by the declared method | `4cd96b537eb398a1`, lengths 1262 / 17182 / 40 — equals the published value |
| `check_index.py --json --ref e2a3e20b` | `653 / 57 / 4 / 586 / 0 / 0 / 6 / 596`; pending 590; quarters 148/148/148/146 |
| `build_index.py --report --ref 0bd37e4d` (full clone) | `109 / 109 / 89 / 10 / 76` |
| Ledger table scan | 109 data rows (K 89 + L 10 + T 10), 0 malformed, 0 duplicate IDs |
| The eight pages at the base | 8/8 blob SHAs, line counts and byte counts reproduce the record's and the body's figures |
| Term prevalence (§5.1) | 21 terms measured over the same 653 pages; `API` 204, `YAML` 32, `MCP` 28 — the record's own figures reproduce exactly |
| R2 derivation (§7) | pending 590 → lane A 148 → read set 40 pages at indices 0..39 contiguous → first eight unread at 40..47; the record's list is at 8..15 (batch 2's pages) |
| `main`'s ledger rows | 8 `K-08nW` withdrawals, 7 fresh rows (`K-098..K-104`), 0 rows `K-105`, 0 rows `K-082`/`K-089` |
| Check runs / workflow runs at the head | 0 / 0 |
| Naming check | `C-1`/`C-3`/`C-4` are not rulings anywhere on `main`; `page-resolves-it` is absent from `main`; the ledger on `main` carries none of the labels |

**Could not verify (stated, not waved through):** N1-N8 of §6 — in particular the record's corrected
diff-scope bytes and next-batch list (a Stage C commit's to make, so they do not exist at this head),
the body's corrected validation rows, the reading act, the model attributions, PR #781's patch in
full, the four non-GitHub CI suites and the Codex comment bodies. `build_index.py` refuses to run
without `refs/pull/**` and `refs/remotes/**` in the clone (measured: it raised `BuildError` before
those refs were fetched) — the clone used here fetched both, which is why its report could be run.

## 13. This plan's own revision and how it is captured

- **Path:** `docs/plans/readability-lane-a-batch-1-stage-a-plan-2026-10-16.md` (this file).
- **Capture method:** committed as a tracked file on a dedicated branch (`stage-a/lane-a-batch-1-plan-2026-10-16`)
  whose **parent is the PR head** `0bd37e4d…`, pushed to the repository, so the revision is
  immutable and the PR head does **not** move; **not** a PR-body-only plan, and not an edit of the PR
  branch.
- **The actual identifiers — the capturing branch, the capturing commit and this file's blob SHA — are
  recorded in the PR #771 body**, together with the id of the fresh issue comment on PR #771 that
  holds the same text **verbatim**. They are recorded there rather than here because a file cannot
  contain its own content hash.
- **Binding:** this plan binds head `0bd37e4dbb27ef108ca13ccbc0cbf4a673ef6b27` and acceptance
  revision `e2a3e20b7c20ef8385b219b39c6405237163406f`. **If either moves, this binding is void** and a
  Stage B auditor must audit the revision it can name, exactly as moving a head voids a head-bound
  verdict.
- **Editing this file after capture voids an ACCEPT that named the captured revision.**
- **Revision 1** is the only revision of this plan.

---

## 14. The corrections this plan binds for Stage C / the PR editor, with exact replacement text

**Why this section exists.** The record (a file this PR adds) publishes one figure that is false of
its own head, and its next-batch list contradicts its own measurement; the PR body carries stale
validation rows. This planner holds **Stage A only** and **must not** edit the files the PR itself
adds, because that would move the head and void every head-bound verdict downstream. The corrections
are therefore **bound here, with the exact replacement text**, so Stage C has no interpretation
latitude and Stage D can check the result mechanically at the commit that applies them. Everything in
§14.1, §14.3 and §14.4 is a **Stage C** commit; §14.2 is PR **metadata** and moves no head.

### 14.1 The record's diff-scope count — record L508-509

**Present bytes (measured, blob `1c8ba69f…`, L508-509):**

```text
**Diff scopes, counted by hand (not by regex).** `base..head` remains **insert-only**:
**445 added / 0 deleted** over two file headers, and with no deleted line at all, no deleted line
```

**Binding replacement:**

```text
**Diff scopes, counted by hand (not by regex).** `base..head` is **insert-only**:
**689 added / 0 deleted** over two file headers and three hunks, and with no deleted line at all, no
deleted line
```

and, immediately after the existing sentence about the intra-branch commit, insert the scope labels so
that no reader can mistake which state each figure belongs to:

```text
(`445 added / 0 deleted` is the **`base..f6a4e418`** figure — the scope before this pass's own two
commits; it is superseded by the head figure above and is not a count of this head.)
```

**What must not change in this edit:** the intra-branch figures already there
(`f6a4e418` vs `09a7ee1c` = **145 added / 51 deleted** — re-measured by me and correct), the
statement that no deleted line begins with `--`, and every other byte of section 9.

### 14.2 The PR body's stale validation rows (metadata; moves no head)

**Present (measured in the live body):** row 1 `git rev-parse HEAD` → `f6a4e418…`; row 2 "2 commits";
row 4 `git diff --numstat` → `334 0` / `111 0`; row 13 "SIGNED for all three commits … OK: 3
commit(s) checked". **Measured at the head:** HEAD = `0bd37e4d…`; 4 commits; `556 0` / `133 0`;
`OK: 4 commit(s) checked, all signed off or exempt`.

**Binding replacement text for each Result cell:**

- **Row 1:** `0bd37e4dbb27ef108ca13ccbc0cbf4a673ef6b27` (the head this row is read at).
- **Row 2:** `4 commits` — and keep the existing parenthetical that names them.
- **Row 4:** `556 0` (batch record) and `133 0` (ledger) — **the same command and the same head as row
  16; the earlier `334 0` / `111 0` reading is the `base..f6a4e418` scope and is superseded.**
- **Row 13:** `exit 0 at this head: SIGNED for all four commits, OK: 4 commit(s) checked, all signed
  off or exempt`.

**14.2b The Stage A skills row (authored here, published outside the bound fields).** This planner's
own self-authored row, in the table's exact four columns, for insertion by the PR editor **together
with the digest republication**, because inserting it changes the `skills` bound field:

```text
| `source-of-truth-reconciler`, `change-classification-gate` | Stage A / `readability-lane-a-stage-a-planner` (DeepSeek-4.1-Flash, deepseek-flash) | WHAT: re-derived every load-bearing figure from the repository instead of the brief — head, merge base, the two-path diff and its 689-line scope, the eight pages' blobs/lines/bytes, the instrument's buckets and the 590-path pending set, the ledger's 109 rows and the bound-field digest — then classified the change from the measured file set. WHY: the brief's figures and the record's own figures disagree in three places, and a plan that copies a stale number plans the wrong change. HOW: one fresh HTTPS clone; every number from a named command (section 12 of the plan). | The record's `445 added` is false of its head (689 is); the body's row 4 contradicts its row 16; the next-batch list names eight pages batch 2 already read. All three are bound as corrections with exact replacement text in the plan's section 14. **Limit:** this row is not an ACCEPT of anything; the plan's Stage B audit is owed and is not held by this agent. |
```

**The digest consequence, stated so it cannot surprise a later stage:** inserting this row moves the
published digest off `4cd96b537eb398a1`; the editor must therefore **recompute and republish** the
digest line (which sits outside all three fields) in the same edit. This plan does **not** make that
edit, because the live Stage D verdict at this head named the present value.

### 14.3 The next-batch list — record §6 (L325-335), the ledger's appended section (the same list), and the body (L267-276)

**Binding correction (text to add, not to replace, so the history stays legible):** label the list with
the state it belongs to, and add the measured first-eight-unread at the base:

```text
**Which state each list belongs to (2026-10-16 Stage A measurement).** The eight paths above are the
first eight **unread** entries of lane A's quarter **when batch 1 was lane A's only committed record**
(post-batch-1 frontier, sorted index 7). Lane A batch 2 has since read exactly those eight paths
(8/8 measured from that record's own bytes), so they are **not** unread at the later state this
section's cross-check measures. Under the read set this section's cross-check asserts (lane A's
reads = sorted indices 0..39, contiguous, from batch records 1-5), the first eight unread at the base
`e2a3e20b` are, by path:
`.claude/skills/ai-closeout-reporter/SKILL.md`,
`.claude/skills/ai-closeout-reporter/assets/closeout-template.md`,
`.claude/skills/ai-cost-guardrail-designer/SKILL.md`,
`.claude/skills/ai-cost-guardrail-designer/references/cost-guardrail-patterns.md`,
`.claude/skills/ai-evaluation-harness/SKILL.md`,
`.claude/skills/ai-evaluation-harness/references/eval-harness-design.md`,
`.claude/skills/ai-governance-risk-reviewer/SKILL.md`,
`.claude/skills/ai-governance-risk-reviewer/references/ai-governance-framework.md`.
Both lists are re-measurement **outputs at one base, not pinned ranges**: the next batch re-runs the
three-step derivation at its own base and only that run's output is binding.
```

**The same labelling goes to the ledger's appended lane-A section and to the PR body's "Next action"
list**, because all three carry the same unlabelled eight paths.

### 14.4 What must NOT change

The acceptance revision stays `e2a3e20b…`; the eight pages' bytes, blob SHAs, line and byte counts
stay as recorded; **no page under `.claude/` is edited** (that would reclassify the change out of
`docs-only`); no keeper row and no withdrawal row is authored by the corrections; the index is not
rebuilt; no tool, workflow, approval, script or test byte changes; the corrections touch only the two
paths already in this PR's diff (§14.1, §14.3) plus PR metadata (§14.2). **The three bound fields of
the PR body are not edited by §14.1-§14.3**, and §14.2b's insertion is the PR editor's, with the digest
republished.

### 14.5 When it becomes decidable

At this head only §14's **binding** is decidable (criteria 9, 10, 11 of §5.2 are declared not
verifiable at this head for this reason). The corrected files' own bytes become decidable at the Stage
C commit that applies them — which **moves the head**, which is exactly why this planner does not
apply them here.

*Prepared by a **DeepSeek-4.1-Flash** agent (`deepseek-flash`), Stage A only, under the owner account
as the repository's attribution rule requires.*
