# Readability Phase 4 re-read lane C — Stage C batch record, batch 5, 2026-10-15

**Work item: "Phase 4 re-read, lane C, batch 5 — evidence record for eight whole-page re-reads".**
**Started** 2026-10-15T21:59:31-07:00 (this session's first clock sample, before the clone); **record
written** 2026-10-15 between the 22:21 and 22:31 clock samples of this session (the same session; wall
time to the pull request is reported in the pull-request body).

- **Lane:** PHASE 4 RE-READ LANE C. *Phase 4 re-read* is the fourth phase of the documentation
  readability backlog — a whole-page re-read of every page that has no recorded full-page acceptance;
  *lane C* is the third, by count, of the four count-based quarters of that sorted pending list, run
  concurrently with three other lanes that own the other three quarters.
- **Stage:** C (IMPLEMENT). *Stage C* is the implementation stage of the repository's delivery
  workflow; for this item it produces the evidence record and nothing else. **This batch authors no
  keeper row.**
- **Derivation base SHA:** `3b0d6cd54222442e2e0b1598829bd078c03a22d4`. *Derivation base* is the
  `origin/main` revision the pending set and the quarter bounds below were computed at (the merge of
  pull request #795, lane A batch 5); every added/deleted-line figure in this record is a diff against
  **this** revision, not against whatever `main` happens to be later, because main moves repeatedly and
  a diff against a newer main would show other pull requests' additions as this batch's deletions.
- **Acceptance revision bound by all eight reads:**
  `3b0d6cd54222442e2e0b1598829bd078c03a22d4`. *Acceptance revision* is the named 40-character revision
  a reader actually read; all eight pages are byte-identical at this revision and at the tip
  (`git diff --numstat 3b0d6cd5… refs/remotes/origin/main -- <page>` is empty for all eight, measured), so
  the bytes each reader read are the bytes the merge receives and the acceptance is not voided by it.
  `git merge-base --is-ancestor 3b0d6cd5… refs/remotes/origin/main` exits 0 (measured).
- **Agent / model attribution (the 2026-10-13 rule).** This record and every text this item publishes
  are drafted by **DeepSeek-4.1-Flash (deepseek-flash)**, an AI agent operating under the owner
  account, in a Stage C session. The 2026-10-13 rule is the owner's standing instruction that any text
  published under the owner account names the model that produced it.
- **Git identity used (checked before any git object was written).** This clone commits as
  `Peter Nguyen <263130032+ModernNomad-98@users.noreply.github.com>` with a matching DCO sign-off — the
  same explicit identity the two zero-rework sibling batches used (lane A batch 5, commit 864461c7;
  lane B batch 5, commits 39a3e5d0 / 4b830eb4 / 3a2546b4). The host's global identity was read first and
  was the stale placeholder `F reviewer <reviewer@example.invalid>`; it was **not** used, because a
  merge would inscribe it into `main`. The identity was set explicitly before this clone's first commit.
- **Stage C repair of this record, disclosed rather than hidden.** The implementation audit of this
  record (PR #797, comment `6209620458`; verdict `SD-D: REVISE`) recorded nine measured-claim findings
  (F1–F9) and ruled that none of them voids a disposition. This revision applies all nine to the record:
  four per-page counts (C5-5's link occurrences, and the named-skill counts and descriptors of C5-5,
  C5-6 and C5-7), the frontmatter numeral, the section 6.1 table size, four convention-table and
  below-norm figures plus the `n-a` substring artifact, two quotations, and the recording authority.
  The footer digest below is recomputed over the corrected bytes. No disposition, gap, page line,
  FULL/PARTIAL count, blob ID or per-page line/byte figure changed; no page, ledger line, index entry,
  register entry or workflow file is touched.
- **What this page is.** The batch's tracked evidence record. *Tracked* means committed to the
  repository rather than left in a working directory. It is the **evidence source** the separate keeper
  cites when it records this batch's pages: a *keeper row* is one row of the ledger's consolidated
  acceptance table, and the *ledger* is the documentation readability backlog, the tracked page that
  carries the acceptance record for every reader page.
- **This batch authors NO keeper rows and appends NOTHING to the ledger.** The diff against the base
  adds exactly this record file. Under **AEGIS-APR-101** — *AEGIS-APR-101* is the owner's register entry
  establishing the standing ledger-keeper role, whose first condition is that the keeper must be a
  different agent from the page's author **and** from the accepting reviewer — the rows for this batch's
  eligible pages are recorded later by a separate eligible keeper from this evidence. The **recording**
  authority is **AEGIS-APR-101** — its unchanged recording-only role, as the ledger states it at
  L5116-5117 ("The ledger keeper records under AEGIS-APR-101 (its unchanged recording-only role) and
  AEGIS-APR-117 (withdrawal rows)"). **AEGIS-APR-117** is the **withdrawal route only** and adds no
  recording power: *AEGIS-APR-117* is the owner's decision that a wrong or same-agent row is cancelled
  by an appended withdrawal row, bound to evidence, and the page becomes pending again. These seven
  pages carry no row at all, so there is nothing to withdraw: AEGIS-APR-117 covers nothing here, and
  **no page needs re-reading**.
- **AEGIS-APR-039** is the standing grant for authorized Project Aegis backlog work (commits, pushes,
  pull requests and merges); this batch uses the commit, push and pull-request part only and **does not
  merge**. **AEGIS-APR-137** is the owner's merged approval of the eight defaults this lane's brief
  cites. Both were read in the owner approval register at the derivation base.
- **Insert-only.** This change adds one new file and deletes nothing: the numstat against the base is
  **1 file, 0 deleted**, and the deleted-line count is taken by counting **every** line of the patch that
  begins with a single minus, rather than a regex over the patch text. The measured figure is in
  section 8 and the pull-request body.

### Labels used in this record, glossed (plain-English description beside every internal label)

- **lane C** — the third, by count, of the four contiguous quarters of the sorted pending page list;
  four lanes run concurrently and each owns a non-overlapping quarter.
- **pending set** — the set of reader pages that still count as not accepted: the instrument's
  `no_recorded_acceptance` bucket (no acceptance row at all) unioned with its `provably_pending` bucket
  (a row exists but the page has drifted past the rule).
- **reader page** — a tracked `.md` file that is documentation a person reads, after the instrument's own
  tree classification removes the `scripts/` test fixtures and the one generated report.
- **the instrument** — `tools/readability_acceptance/check_index.py`, the repository's official pending-count
  decision procedure; **the index** is `tools/readability_acceptance/acceptance-index.json`, the
  machine-readable table of recorded acceptances.
- **read frontier** — the highest sorted index of the pending list that any batch of this lane has
  already read. A page *behind* the frontier is passed over by every later batch that simply walks
  forward from it.
- **R1 / R2 / R3** — the three readings of "the next eight" this batch was asked to choose between.
  **R1** is the eight contiguous unread pages after the frontier; **R2** is the next eight unread pages in
  the **unread sequence** (not index-contiguous); **R3** is index arithmetic (quarter start plus 24).
  **This batch applies R2** (section 2).
- **unread sequence** — the pending set minus every page any lane's batch record has already read, taken
  in sorted order. Taking the next eight entries in it skips nothing at all, which is what coverage
  requires; adjacency is not the requirement.
- **FULL** — every one of the six acceptance bullets holds for the whole page. **PARTIAL** — at least one
  defect stands against the page at the bound revision and is named with its page line.
- **observation** — a measured library convention, or a term the page's own bytes resolve. An observation
  is **not** a defect and does not move a disposition; it is recorded so the measurement is visible
  rather than implied. A **gap** is a defect, and **a page with any recorded gap is PARTIAL**.
- **full-page-acceptance row** / **targeted-review row** — two of the four event kinds the ledger names;
  *full-page-acceptance* records that a named reader accepted the whole page at a named revision, and
  *targeted-review* records that a named reader reviewed only the drift since the last acceptance. The
  other two are *withdrawal* and *lost-commit*.
- **zero drift** — the page is byte-identical at the acceptance revision and at the compared ref, so
  nothing has changed since it was read.
- **no_recorded_acceptance** — a reader page with no acceptance row of any kind in the index.

## 1. The instrument's figures at the base, quoted

```text
python -P -B tools/readability_acceptance/check_index.py --quiet --ref 3b0d6cd54222442e2e0b1598829bd078c03a22d4
{
  "compared_ref": "3b0d6cd54222442e2e0b1598829bd078c03a22d4",
  "reader_pages_in_tree": 657,
  "accepted_on_recorded_review": 56,
  "provably_pending": 5,
  "no_recorded_acceptance": 590,
  "recorded_acceptance_within_10_lines": 0,
  "within_10_not_covered_by_targeted_review": 0,
  "cannot_decide": 6,
  "official_pending_count": 601,
  "official_pending_count_definition": "provably_pending + no_recorded_acceptance + cannot_decide + (recorded_acceptance_within_10_lines not covered by a recorded targeted-review row); computed at the pinned --ref"
}
exit 0
```

**This lane publishes no readability count of its own** (the owner's **D84** decision, which made this
instrument's summary the official count) and presents the figures above as the instrument's, not as its
own measurement. The official pending count is **601**; the **pending set** this lane's quarter is drawn
from is the two-bucket union **590 + 5 = 595**, which is the figure the lane's brief named and which this
batch re-derived by command rather than trusting.

## 2. Lane derivation, batch selection, and the frontier finding — by command

- **Pending set = 595 paths. Derived, not inherited.** `git ls-tree -r --name-only 3b0d6cd5…` returns **723**
  Markdown paths; the instrument's own classification removes **65** `scripts/` fixtures (all but the
  excepted `scripts/tests/fixtures/README.md`) and **1** generated report, leaving **657** reader pages. Those
  with no row in the index's `reader_pages` array (**68** rows at the base) are the **590**
  `no_recorded_acceptance` pages. Union with the instrument's **5** `provably_pending` paths
  (`docs/approvals/APPROVAL_REGISTER.md`, `docs/delivery-workflow.md`,
  `docs/roadmaps/aegis-backlog-forecast.md`, `docs/roadmaps/aegis-documentation-readability-backlog.md`,
  `docs/roadmaps/behavioral-eval-runner-backlog.md`) = **595**. Overlap between the two buckets is **0** and the
  union has **595** distinct paths, both measured. **The brief's 595 was checked, not trusted, and it is correct.**
- **Quarters.** Sorted by repository path, `ceil(595 / 4) = 149`, so the four contiguous count-based
  quarters are **149 / 149 / 149 / 148**: lane A indices **0–148**, lane B **149–297**, **lane C 298–446**,
  lane D **447–594**. Lane C's first path is `.claude/skills/skill-quality-reviewer/SKILL.md` and its last is
  `docs/evidence/documentation/full-page-readability-batch-after-234-2026-09-24.md`.
- **The six `cannot_decide` (lost-commit) pages are in NO lane.** *cannot_decide* means a lost-commit page:
  an acceptance whose commit was recorded, never bound and never dropped, so under decision **D73 row 5**
  it counts pending until re-reviewed. The six are
  `.claude/skills/cloud-security-baseline-reviewer/references/aws-baseline.md`, `…/azure-baseline.md`,
  `…/gcp-baseline.md`, `…/supabase-baseline.md`, `…/vercel-baseline.md` and
  `.claude/skills/database-backup-verifier/SKILL.md`. Their intersection with this batch's eight pages is
  **empty** (measured), and this batch does not pick them up.

### The reading used: R2 — and the frontier check, stated either way

**Every page lanes A–D read before this batch was extracted from the batch records themselves**, at their
branch heads, not from any summary: the 19 batch records (lane A batches 1–5, lane B batches 1–5, lane C
batches 1–4, lane D batches 1–5) were read at their own committed bytes and their read pages taken from
their disposition tables. Result: **19 batches × 8 pages = 152 read slots, 152 distinct pages** (every
batch read exactly eight, measured; no page was read twice). Each was mapped to its index in this base's
595-path pending set, and the whole range was re-measured before it was written down:

```text
lane A read indices in the 595-path pending set : 0 .. 39,   count 40, distinct 40, gaps: none
lane B read indices                              : 148 .. 187, count 40, distinct 40, gaps: none
lane C read indices (batches 1-4)                 : 296 .. 327, count 32, distinct 32, gaps: none
lane D read indices                              : 445 .. 486, count 40, distinct 40, gaps: 460, 461
read frontier (highest LANE C index read)        : 327  .claude/skills/supply-chain-security-reviewer/SKILL.md
UNREAD PAGES INSIDE LANE C'S QUARTER             : 117
UNREAD PAGES INSIDE LANE C'S QUARTER AT OR BELOW THE FRONTIER : 0
this batch (R2, next eight in the unread sequence): 328 329 330 331 332 333 334 335
```

**Finding: NO unread page sits behind this lane's frontier, at this base, in either sense.** Every pending
path that sorts below index 328 and inside lane C's quarter (298–327) is a page lane C batches 1–4 already
read; the only earlier-lane pages that sort *inside* lane C's quarter are two lane D batch-1 pages at
indices 445–446, which lane D already read. **Both readings were computed: R1 (the eight contiguous unread
pages after the frontier) also starts at 328, so here R1 and R2 select the same eight paths. R2 is recorded
as the rule because it is the one that cannot orphan a page when the pending set shifts — exactly what
happened to lane D batch 5, which had to read the unread page at index 456 first.**

- **Pages skipped as already read — named, not gestured at.** Four already-read pages now fall inside
  lane C's quarter by arithmetic, and this batch skipped all four:
  1. `docs/evidence/documentation/full-page-readability-batch-after-233-2026-09-24.md` (index **445**) — read by
     **lane D batch 1** as its LD-1.
  2. `docs/evidence/documentation/full-page-readability-batch-after-234-2026-09-24.md` (index **446**) — read by
     **lane D batch 1** as its LD-2.
  3. `.claude/skills/skill-deprecation-planner/SKILL.md` (index **296**) and
  4. `.claude/skills/skill-deprecation-planner/references/deprecation-stage-playbook.md` (index **297**) — read by
     **lane C batch 1** as its C1-1 and C1-2. These two have **moved out of lane C's quarter into lane B's**
     at this base and were skipped for the same reason: an earlier batch read them.
  Indices 298–327 — lane C batches 1–4's own 30 in-quarter pages — were skipped as the contiguous block
  they are. **No unread page was skipped.**
- **Cross-lane observation (recorded, not acted on).** The same measurement shows **two unread pages behind
  lane D's frontier, at indices 460 and 461**: `docs/evidence/documentation/readability-lane-a-batch-5-2026-10-15.md`
  and `docs/evidence/documentation/readability-lane-c-batch-3-2026-10-15.md`. Both are batch records of other
  lanes that reached `main` after lane D's batches ran, so lane D's forward walk passed over them. This
  lane **does not touch them** — they are lane D's quarter and lane D's decision — and the measurement is
  reported here only so the programme can route it. This is the same R1 trap this batch's own reading is
  chosen to avoid.
- **Continuity verified, not assumed.** The lane C batch-1…batch-4 records' eight paths were taken from
  their own committed bytes and compared one by one with sorted indices 296–327 of this base's pending
  set: **all 32 match exactly, in order, with no gap**. Lane A's 40 pages map to indices 0–39 and lane B's
  to 148–187 in the same check — which independently reproduces lane A batch 5's published claim that its
  own batch was indices 32–39 at its base, the strongest available check on this extraction method.
- **Next batch selection rule — pages named, no index pinned.** The next batch takes the next eight unread
  pages of lane C's unread sequence, re-measured at its own implementation base. At this base those pages
  are named (by path, never by number, because indices move as the pending set grows):
  `.claude/skills/tenant-isolation-reviewer/references/isolation-surface-checklist.md`,
  `.claude/skills/tenant-modeler/SKILL.md`, `.claude/skills/tenant-modeler/references/tenant-lifecycle-catalog.md`,
  `.claude/skills/test-coverage-mapper/SKILL.md`,
  `.claude/skills/test-coverage-mapper/references/coverage-mapping-method.md`,
  `.claude/skills/test-data-architect/SKILL.md`,
  `.claude/skills/test-data-architect/references/test-data-patterns.md` and
  `.claude/skills/test-plan-designer/SKILL.md`. They are a **measurement at this base, not an instruction**: the
  next batch must re-derive them and skip anything an earlier batch has read by then.
- **This batch is indices 328–335** — the next eight after batch 1's 296–303, batch 2's 304–311, batch 3's
  312–319 and batch 4's 320–327.

## 3. The roster and the role separation (stated, not hidden)

| Batch | Theme | Pages | Read at | Reader |
| --- | --- | ---: | --- | --- |
| C5 | eight `.claude/skills/` pages of the quarter: the `supply-chain-security-reviewer` checklist, the `synthetic-monitoring-architect` skill, the `systematic-debugger` skill and its isolation reference, the `tdd-engineer` skill, the `tech-spec-writer` skill and its sheet, and the `tenant-isolation-reviewer` skill | 8 | base `3b0d6cd5…` | this Stage C session (DeepSeek-4.1-Flash (deepseek-flash)) |

**Concurrency: one reader.** This item's brief directs a single agent to perform the batch, so the
three-reader ceiling (*three-reader ceiling*: the ledger's rule that up to three read-only agents may share a
batch when their page sets are disjoint) is satisfied by construction and is recorded here rather than
presented as multiple agents.

**Role separation — satisfied by construction.** This batch's agent is the accepting reader and the writer
of this evidence record only; it authors **no keeper rows** and appends nothing to the ledger. Both
AEGIS-APR-101 conditions hold for the rows a separate keeper will record from this evidence: the keeper will
differ from this accepting reviewer (a different agent) and from the page authors. The lane wrote none of the
eight read pages — the last commit touching each names another author
(`git log -1 --format="%h %an %s" -- <page>`, measured this session):

| # | Page | Last-touching commit / author |
| --- | --- | --- |
| C5-1 | `.claude/skills/supply-chain-security-reviewer/references/supply-chain-checklist.md` | `9c9a6692` Peter Nguyen ("feat: extend supply-chain-security-reviewer to promoted model artifacts") |
| C5-2 | `.claude/skills/synthetic-monitoring-architect/SKILL.md` | `67f577e2` Peter Nguyen ("docs: apply readability sweep batch 2 required edits") |
| C5-3 | `.claude/skills/systematic-debugger/SKILL.md` | `18e8a280` Peter Nguyen ("feat: add the ci-failure-classifier skill (186 to 187)") |
| C5-4 | `.claude/skills/systematic-debugger/references/isolation-tactics.md` | `a694b938` Peter Nguyen ("docs: review next forty skill references") |
| C5-5 | `.claude/skills/tdd-engineer/SKILL.md` | `cce5c378` Peter Nguyen ("docs: accept twenty more pages after PR 229") |
| C5-6 | `.claude/skills/tech-spec-writer/SKILL.md` | `67f577e2` Peter Nguyen ("docs: apply readability sweep batch 2 required edits") |
| C5-7 | `.claude/skills/tech-spec-writer/references/tech-spec-sheet.md` | `02e88b18` Peter Nguyen ("Explain owner choices in technical specifications") |
| C5-8 | `.claude/skills/tenant-isolation-reviewer/SKILL.md` | `8459ac73` Peter Nguyen ("docs: spell out artificial intelligence (AI) at first body use") |

**Honest disclosure about the shared identity string.** `git log --all --author="F reviewer"` returns
**11** commits in this clone — the count is measured, and an earlier draft of this record said 12, which was
wrong. All 11 sit on other Stage C/D lanes' branches or open pull requests: lane A batch 4 and its link
repair (`origin/docs/readability-lane-a-batch-4-20261015`), lane B batch 4 and its citation repair, lane C batch
3 and its repairs, the APR-117 withdrawal work, and a CI-label repair. **Zero** of those commits touch any of
the eight pages in this batch (checked per path by command: 0 commits for every page), and this session made
no other commit in this repository before this batch. The string is the host's stale global identity and is
disclosed here rather than used.

**One of those 11 is a live hazard and is reported, not amended.** Branch
`origin/docs/readability-lane-a-batch-4-20261015` (open pull request **#789**, lane A batch 4) carries **2**
commits authored `F reviewer <reviewer@example.invalid>` (head `de2bfe72`, base commit `e8c8a67c`), and a
merge would inscribe that placeholder identity into `main`. It is another lane's branch and pull request, so
this batch does not touch, amend or force-push it; the measurement is reported for the coordinator. (Sibling
lane A batch 5 made the same disclosure at its own head; it is still true here.)

**Keeper IDs — none allocated here.** This batch records evidence only and consumes no keeper-row identifier;
the separate keeper assigns the IDs when recording from this evidence.

## 4. Per-page dispositions — eight whole-page re-reads, zero edits

Every page was read **whole, line by line, as prose**, at the bound revision
`3b0d6cd54222442e2e0b1598829bd078c03a22d4` in this session, each page in one read with no display elision.
*Full-page re-read* means the reader judged **all six** acceptance bullets of the ledger's "Acceptance for each
page" contract against the whole page — not a sample and not a targeted diff. The bullets are referenced below
as **B1** open with what the page is for and who should read it; **B2** define an abbreviation or coded
identifier at first use; **B3** descriptive headings, short paragraphs, lists or tables, at least one concrete
example, and what a command accepts, produces, changes and refuses where safe use depends on it; **B4** state
shipped behavior separately from proposed or blocked behavior; **B5** keep navigation links current and check
that every referenced file or command exists, without removing a safety boundary; **B6** a read-only review by
someone who did not write the page.

**Verdict vocabulary, and the rule that keeps a gap and a FULL verdict from coexisting.** **FULL** means every
one of the six bullets holds for the whole page. **PARTIAL** means at least one defect stands against the page
at the bound revision and is named below with its page line number. **If a gap is recorded anywhere in this
record for a page, that page's disposition is PARTIAL** — no page in this batch carries a recorded gap
together with a FULL verdict, which is the laundering this record must not repeat. The ledger's own record
vocabulary is "accepted" and "needs a named follow-up"; this record's FULL maps to the first and its PARTIAL to
the second. An **observation** in this record is by construction **not** a gap: every observation below is
either a measured library convention or a term the page's own bytes resolve, and each carries its measurement
so a reviewer can check the call instead of trusting it.

| # | Pending index | Page | Lines / bytes at the bound revision | Disposition | Gap named (page line) | Edits |
| --- | ---: | --- | ---: | --- | --- | ---: |
| C5-1 | 328 | `.claude/skills/supply-chain-security-reviewer/references/supply-chain-checklist.md` | 215 / 12,979 | **FULL** | none | 0 |
| C5-2 | 329 | `.claude/skills/synthetic-monitoring-architect/SKILL.md` | 224 / 14,130 | **FULL** | none | 0 |
| C5-3 | 330 | `.claude/skills/systematic-debugger/SKILL.md` | 152 / 8,568 | **FULL** | none | 0 |
| C5-4 | 331 | `.claude/skills/systematic-debugger/references/isolation-tactics.md` | 61 / 3,777 | **FULL** | none | 0 |
| C5-5 | 332 | `.claude/skills/tdd-engineer/SKILL.md` | 151 / 8,111 | **FULL** | none | 0 |
| C5-6 | 333 | `.claude/skills/tech-spec-writer/SKILL.md` | 191 / 10,865 | **FULL** | none | 0 |
| C5-7 | 334 | `.claude/skills/tech-spec-writer/references/tech-spec-sheet.md` | 72 / 2,935 | **FULL** | none | 0 |
| C5-8 | 335 | `.claude/skills/tenant-isolation-reviewer/SKILL.md` | 173 / 9,852 | **PARTIAL** | **G-C5.1** — `authn` at **L36**, used as an abbreviation with no on-page definition and no companion that defines it | 0 |

**Counts: 7 FULL / 1 PARTIAL, one named gap.** The eight pages total **1,239 lines / 71,217 bytes** at the
bound revision (measured by command). Line and byte counts are `git show 3b0d6cd5…:<page>` measured in this
session, not transcribed. **Zero drift**: all eight pages are byte-identical at the base and at `origin/main`,
so no read is voided. **No page needed an edit and none was made**, so no page's net line change is anything
other than 0; this is an evidence-only change. The longest line across the eight pages is **1,003 bytes / 1,001
characters** (C5-2, its frontmatter description line).

**Eligibility for keeper rows — stated so a partial page cannot be laundered into an acceptance.** **Only
C5-1, C5-2, C5-3, C5-4, C5-5, C5-6 and C5-7 are eligible to receive a full-page-acceptance row from this
evidence. C5-8 is PARTIAL and stays pending.** *Stays pending* means the page continues to count in the
official pending total until a later eligible re-read clears it. This record deliberately does not repair
C5-8's defect: editing an instruction file under `.claude/skills/` would reclassify this change beyond the
docs-only class it is committed under (the change-classification gate's agent-instruction-file rule), so the
defect is recorded as a property of the bound text and left for its own authorized fix.

**Full 40-character blob IDs at the bound revision** (*blob ID* is git's content hash for one file revision),
computed by command in this session with `git rev-parse 3b0d6cd5…:<page>` × 8; each ID below is 40 hex characters:

| # | Page | Full blob ID (40 hex) |
| --- | --- | --- |
| C5-1 | `.claude/skills/supply-chain-security-reviewer/references/supply-chain-checklist.md` | `67a92a900964396b71fa34521d662994bbcc6567` |
| C5-2 | `.claude/skills/synthetic-monitoring-architect/SKILL.md` | `ba6d8a3941a1b48729c3d4beac0233519456a2d5` |
| C5-3 | `.claude/skills/systematic-debugger/SKILL.md` | `d36905334b762cb0e4bf0f92b680db3555b652ec` |
| C5-4 | `.claude/skills/systematic-debugger/references/isolation-tactics.md` | `6c9a09a19a90b21abfb951f9796d23c606b2d5b8` |
| C5-5 | `.claude/skills/tdd-engineer/SKILL.md` | `7ce8588b3af8b2b8644423c8c515c1f1c1415836` |
| C5-6 | `.claude/skills/tech-spec-writer/SKILL.md` | `dfb04a2c24a3a0bda1efa3ec9fd595f574aa3325` |
| C5-7 | `.claude/skills/tech-spec-writer/references/tech-spec-sheet.md` | `c04840c7ea8d9553c6ede5b21b8991d82358a457` |
| C5-8 | `.claude/skills/tenant-isolation-reviewer/SKILL.md` | `36aad49bb95373399c5200cee4b7c8f58916643f` |

## 5. Per-page read detail — ranges, the six bullets, purpose restatements, and every gap with its line

Every page below was read whole at `3b0d6cd54222442e2e0b1598829bd078c03a22d4`
against [Acceptance for each page](../../roadmaps/aegis-documentation-readability-backlog.md#acceptance-for-each-page).
None of the eight pages has a recorded acceptance at the base (each path is absent from both the index's
`reader_pages` and `events` arrays, verified by command), so there is no drift to measure; this record is
the first recorded read for each page.

### 5.1 C5-1 — `.claude/skills/supply-chain-security-reviewer/references/supply-chain-checklist.md`, read whole, FULL

1. **Ranges.** One slice: **L1-215** (the whole file at the bound revision). No elision; longest line 258
   bytes / 258 characters.
2. **Every line was read as prose** — the title and the use-with-the-parent line, the eleven-entry terms
   block, the reachability triage rubric, the CI/CD compromise-path catalog table, install/build execution
   review, dependency-specific risk, pinning and provenance checks, the AI/ML supply chain section, the
   promoted-model-artifact trace table, the agentic supply-chain section, the HIGH-severity gate, and handoffs.
3. **Links and named references** were checked mechanically (section 9): the page's one link occurrence
   (rendered text: Supply Chain Security Reviewer) resolves at the bound revision; **all 7** distinct
   backticked skill names on the page exist as skills at the bound revision.

**The six acceptance bullets, addressed.**

| Bullet | C5-1 `supply-chain-checklist.md` |
| --- | --- |
| Purpose and audience up front | **yes.** L1 names the file and its four subjects (CI/CD paths, triage, pinning, provenance); L3 states its Use with the parent skill; L5-7 states in one sentence what supply-chain assurance asks. |
| Abbreviations and coded identifiers defined at first use | **yes.** The terms block at L9-33 expands SLSA, CVE, CI/CD, PR, SHA, TP, SAST, RCE, AI, ML, RAG, OWASP, ASI04, ASI07, MCP, A2A, OS, authn, LLM04:2026, LLM, SBOM, AI-BOM and LoRA **before** the first body use in each case; `IaC` is written out in full at L155 and again at L211. Five further terms are below library norm and are recorded as **observations, not gaps**, in section 6, each with the page sentence that resolves it: `safetensors`, `Sigstore`, `transitive`, `postinstall`/`build.rs` and the named ecosystem tools. |
| Descriptive headings, lists or tables, and at least one concrete example | **yes.** Ten headed sections; two worked tables (the compromise-path catalog with Path/Signal/Remediation columns, and the seven-link promotion trace with Link/What to verify/Finding when columns); bulleted rubrics; concrete examples throughout (L76 `reqests`, `lodahs`; L70 `curl | sh`; L61 `uses: someorg/action@v3`). |
| Shipped behaviour separated from proposed or blocked behaviour | **yes.** The page is a review checklist and claims no shipped system behaviour; it instead states scope boundaries explicitly at L99 ("Scope: ACQUISITION"), L122-124, L166 ("Scope: ACQUISITION and update") and L162-167, and routes each neighbouring concern to its owning skill. |
| Navigation links current and every referenced file or command existing | **yes.** 1 Markdown link occurrence over 1 target — exists at the bound revision; no external links and no in-page anchors; **all 7** named skills exist; the commands and file names the page quotes are real (L87 `npm ci`, `--frozen-lockfile`; L88 `go.sum`; L102 `pickle.load`; L103 `torch.load(..., weights_only=False)`). |
| The non-author review itself | **this record** (page author: Peter Nguyen, last-touching commit `9c9a6692`) |

**Purpose and normal use restated from the page alone:** the triage and assurance checklist behind
`supply-chain-security-reviewer` — reachability triage of scanner output into four dispositions, the CI/CD
compromise-path catalog, install/build execution review, dependency-specific risk, pinning and provenance
checks, the AI/ML acquisition surface including promoted model artifacts, and the agentic (MCP/A2A)
acquisition surface. Its normal use is: open it beside the parent skill while reviewing a supply chain, sort each
flagged advisory by reachability, walk the compromise-path and promotion tables link by link, and hand every
out-of-scope concern to the skill the page names for it.

**Disputed lines: none. No gap recorded. No line of the page was edited by this lane.**
**Verdict: FULL, no edit. No defect recorded.**

### 5.2 C5-2 — `.claude/skills/synthetic-monitoring-architect/SKILL.md`, read whole, FULL

1. **Ranges.** One slice: **L1-224** (the whole file at the bound revision). No elision; longest line 1,003
   bytes / 1,001 characters (the frontmatter description), the longest line in the batch.
2. **Every line was read as prose** — the frontmatter description, the reading key, Purpose, Use When with its
   four Do-NOT-use counter-examples, Inputs to Inspect, the seven-step Workflow, the Output Format block, the
   Validation Checklist, Gotchas, Stop Conditions and Supporting Files.
3. **Links and named references** were checked mechanically (section 9): the page carries **zero** Markdown
   links, so there is no link to break; **all 7** distinct backticked skill names exist; and the page's own
   structural claims were verified: L223 says "No `references/`" and the directory listing confirms it (only
   `SKILL.md` and the two `evals/` files), and L216-222's description of both eval files matches their
   contents (all four named behaviour cases present in `evals.json`; all five named discriminating skills
   present in `trigger-evals.json`).

**The six acceptance bullets, addressed.**

| Bullet | C5-2 `synthetic-monitoring-architect/SKILL.md` |
| --- | --- |
| Purpose and audience up front | **yes.** The frontmatter description (L3) states the job, the trigger and the four Do-NOT-use neighbours; L8-10 is the reading key; L14-26 states the gap the skill fills and its boundary ("This skill DESIGNS the probes and their safety envelope — it does not execute them against production"); Use When addresses the reader directly with four Use-when and four Do-NOT-use cases. |
| Abbreviations and coded identifiers defined at first use | **yes.** The reading key at L8-10 expands SLI, SLO, RUM, E2E, CI and PII before the body; CDN and DNS are written out in full at L185; `heartbeat/canary` is defined by its own row at L78 ("a cheap liveness ping at high frequency"); `prod` is paired with `PRODUCTION` in full throughout. Four further terms are below library norm and are recorded as **observations, not gaps**, in section 6, each with the resolving sentence: `white-box`, `black-box`, `ring-fenced`, and the `prod` shorthand itself. |
| Descriptive headings, lists or tables, and at least one concrete example | **yes.** Eight headed sections; a seven-step workflow; a copyable Output Format block (L130-152) written as a filled-in guarantee card; a Validation Checklist; and concrete examples throughout (L176 "our uptime check signed up 50,000 fake users / emailed real customers", L185 "Up from us-east" is not "up"). |
| Shipped behaviour separated from proposed or blocked behaviour | **yes, and explicitly.** The Output Format's first line states "Posture: DESIGN ONLY — probes are not run against production here; execution requires an applicable human grant + a validated prod-safety contract" (L132-133), and Stop Conditions refuse execution without human approval and a validated contract (L197-205). |
| Navigation links current and every referenced file or command existing | **yes.** 0 Markdown links — nothing to resolve; no external links; no in-page anchors; **all 7** named skills exist at the bound revision; the page's two structural claims about its own directory were both verified true (section 9). |
| The non-author review itself | **this record** (page author: Peter Nguyen, last-touching commit `67f577e2`) |

**Purpose and normal use restated from the page alone:** designing black-box production monitoring — a probe
catalog selected by incident value (journey, dependency and heartbeat/canary probes), a prod-safety contract
that gates every probe (no mutation, no fixture leak, least privilege, fail safe), synthetic SLIs labelled as
such and feeding — never setting — the SLO targets, a scheduling design with its cost and load tradeoffs,
alerting that distinguishes a broken probe from a broken production, and result capture with redaction. Its
normal use is: write the prod-safety contract first, catalog the few journeys whose failure IS an incident,
define the synthetic SLIs, pick the schedule eyes-open, and route the alert to a runbook — designing probes,
never firing them at production.

**Disputed lines: none. No gap recorded. No line of the page was edited by this lane.**
**Verdict: FULL, no edit. No defect recorded.**

### 5.3 C5-3 — `.claude/skills/systematic-debugger/SKILL.md`, read whole, FULL

1. **Ranges.** One slice: **L1-152** (the whole file at the bound revision). No elision; longest line 804
   bytes / 792 characters (the frontmatter description).
2. **Every line was read as prose** — the frontmatter with its MANUAL-ONLY marker, Purpose, Use When with its
   four Do-NOT-use counter-examples, Inputs to Inspect, the Workflow preamble and its six numbered steps,
   the Output Format block, Validation Checklist, Gotchas, Stop Conditions and Supporting Files.
3. **Links and named references** were checked mechanically (section 9): the page's two link occurrences
   (rendered text: skill-generation standard, and references/isolation-tactics.md) resolve at the bound
   revision, and the one anchor the page cites was checked by the repository's own link checker (2 anchors
   checked, 0 broken); **all 7** distinct backticked skill names exist; the commands the page names are real
   (`git log`, `git bisect`).

**The six acceptance bullets, addressed.**

| Bullet | C5-3 `systematic-debugger/SKILL.md` |
| --- | --- |
| Purpose and audience up front | **yes.** L11-16 states what the skill replaces (guess-and-check debugging) with what (an evidence chain), names the six stages, and states the output ("a root cause the reader can check — not 'it works now.'"). Use When addresses the reader directly. |
| Abbreviations and coded identifiers defined at first use | **yes.** `TALI` is expanded at its first use as "Task-Authorized Local Implementation (TALI)" (L51-52) and then used; `PRODUCT-BUG` (L34) is below library norm and is recorded as an **observation, not a gap**, in section 6 with the page sentence that resolves it; `CI` (L32-33) and the MANUAL-ONLY marker (L3, L4) are library conventions, measured in section 6. |
| Descriptive headings, lists or tables, and at least one concrete example | **yes.** Seven headed sections; a six-step numbered workflow; a copyable Output Format block (L85-98) written as a filled-in debugging report; a Validation Checklist; and concrete examples (L105 "race in X when Y" not "timing issue"; L13 "if this is the cause, then X will happen when I do Y"). |
| Shipped behaviour separated from proposed or blocked behaviour | **yes.** L50-57 states the execution boundary explicitly — explicit human invocation selects the skill but "does not expand the allowed target or activate Task-Authorized Local Implementation (TALI)" — and Stop Conditions refuse automatic selection and any operation exceeding the applicable human grant. |
| Navigation links current and every referenced file or command existing | **yes.** 2 Markdown link occurrences over 2 targets, both existing at the bound revision; no external links; the one in-page anchor resolves (checked); **all 7** named skills exist; `git bisect` and `git log` are real commands, and the page's claim about a dirty-tree bisect (L118-119) is correct. |
| The non-author review itself | **this record** (page author: Peter Nguyen, last-touching commit `18e8a280`) |

**Purpose and normal use restated from the page alone:** driving an unknown-cause bug to a checkable root
cause through a fixed sequence — reproduce, reduce, isolate by tested prediction, fix exactly one thing, verify
against the original reproduction, and prevent the class from returning — with evidence recorded at every step
and disproofs kept as progress. Its normal use is: build the smallest reliable reproduction, shrink it, rank
hypotheses and test the top one against a stated prediction, change one variable, re-run the ORIGINAL
reproduction, and add the regression test that keeps the fix.

**Disputed lines: none. No gap recorded. No line of the page was edited by this lane.**
**Verdict: FULL, no edit. No defect recorded.**

### 5.4 C5-4 — `.claude/skills/systematic-debugger/references/isolation-tactics.md`, read whole, FULL

1. **Ranges.** One slice: **L1-61** (the whole file at the bound revision). No elision; longest line 293
   bytes / 291 characters.
2. **Every line was read as prose** — the use-with-the-parent line and reading key, the four bisection
   recipes, the intermittent-failure amplifier table, the reliability arithmetic, the environment-delta
   checklist, the instrumentation patterns, and the hypothesis-ranking heuristics.
3. **Links and named references** were checked mechanically (section 9): the page's one link occurrence
   (rendered text: Systematic Debugger) resolves at the bound revision; the page names no skill and no
   external file, so there is nothing else to resolve; the commands inside its code spans are real
   (`git bisect start`, `git bisect bad HEAD`, `git bisect good <last-known-good>`,
   `git bisect run <cmd>`).

**The six acceptance bullets, addressed.**

| Bullet | C5-4 `isolation-tactics.md` |
| --- | --- |
| Purpose and audience up front | **yes.** L1 is the title and L3 states both the owning skill and the reading mode ("Use these tactics with the Systematic Debugger. Read on demand."). |
| Abbreviations and coded identifiers defined at first use | **yes.** The reading key at L5-7 expands FD, DST, UTC, DNS and TLS before the body. Three further terms are below library norm and are recorded as **observations, not gaps**, in section 6 with the resolving sentence for each: `heisenbug`, `ulimits`, and `property-based`; `isolated disposable worktrees` is likewise recorded as an observation. |
| Descriptive headings, lists or tables, and at least one concrete example | **yes.** Five headed sections; a four-recipe bisection list; a five-row amplifier table mapping suspected class to concrete amplifier; a worked reliability calculation (L30-32: "if the bug fails 1-in-20 runs, a 20-run green streak after a fix is ~36% likely by luck alone … (for 1-in-20: ~90 runs)"); and a checkable instrumentation rule (L52-53). |
| Shipped behaviour separated from proposed or blocked behaviour | **yes.** The page is a tactic sheet for a manual-only owning skill and claims no shipped system behaviour; the tactics are instructions to the reader, and L14-16 states what to do when the preferred isolation is unavailable. |
| Navigation links current and every referenced file or command existing | **yes.** 1 Markdown link occurrence over 1 target — exists at the bound revision; no external links; no in-page anchors; exactly one backticked name on the page (`DBG-<ticket>`, a marker string, not a skill) and the page names no skill by path; the `git bisect` forms are real. |
| The non-author review itself | **this record** (page author: Peter Nguyen, last-touching commit `a694b938`) |

**Purpose and normal use restated from the page alone:** the owning skill's tactic sheet — bisection recipes
for change, dependency, data and config; amplifiers that turn an intermittent failure into a reproducible one;
the reliability arithmetic that says how many runs are enough; an ordered environment-delta checklist;
instrumentation patterns that do not perturb timing; and hypothesis-ranking heuristics. Its normal use is:
open it beside the parent skill mid-investigation, pick the bisection axis that fits, amplify the failure until
reproduction is statistically reliable, and instrument only the boundary between suspect and victim.

**Disputed lines: none. No gap recorded. No line of the page was edited by this lane.**
**Verdict: FULL, no edit. No defect recorded.**

### 5.5 C5-5 — `.claude/skills/tdd-engineer/SKILL.md`, read whole, FULL

1. **Ranges.** One slice: **L1-151** (the whole file at the bound revision). No elision; longest line 732
   bytes / 730 characters (the frontmatter description).
2. **Every line was read as prose** — the frontmatter with its MANUAL-ONLY marker, the reading key, Purpose,
   Use When with its three Do-NOT-use counter-examples, Inputs to Inspect, the Workflow preamble and its eight
   numbered steps, the Output Format block, Validation Checklist, Gotchas, Stop Conditions and Supporting Files.
3. **Links and named references** were checked mechanically (section 9): the page's one link occurrence
   (rendered text: skill-generation standard) resolves at the bound revision, with the one anchor it carries
   verified by the repository's link checker; **all 3** distinct backticked skill names exist; the page names
   no shell command that could be stale.

**The six acceptance bullets, addressed.**

| Bullet | C5-5 `tdd-engineer/SKILL.md` |
| --- | --- |
| Purpose and audience up front | **yes.** L14-16 defines the loop ("Test-driven development (TDD) uses a red-green-refactor loop") and L18-23 states what the skill delivers and why the load-bearing step is confirming the RED. Use When addresses the reader directly. |
| Abbreviations and coded identifiers defined at first use | **yes.** CI is expanded at L9-10 ("CI means continuous integration, the automated checks run for a change"); TDD at L14; TALI as "Task-Authorized Local Implementation (TALI)" at L55-56; RED, GREEN and REFACTOR are defined by the Purpose at L14-16 and by the workflow steps that name them (L70, L78, L80); `mid-batch` (L123) is a transparent two-word compound and is recorded as an observation in section 6. |
| Descriptive headings, lists or tables, and at least one concrete example | **yes.** Nine headed sections; an eight-step numbered workflow; a copyable Output Format block (L89-99) showing one iteration's RED/GREEN/REFACTOR lines; a Validation Checklist; and concrete failure examples (L71-73 "an import error, name error, fixture crash, or an unexpectedly passing test means the test is wrong — fix the test, not the code"). |
| Shipped behaviour separated from proposed or blocked behaviour | **yes.** L54-61 states the execution boundary in the same words the sibling skill uses (explicit human invocation "does not expand the allowed target or activate Task-Authorized Local Implementation (TALI)"), and Stop Conditions refuse the operation when authority is absent. |
| Navigation links current and every referenced file or command existing | **yes.** 1 Markdown link occurrence over 1 target — exists at the bound revision, with the page's one anchor resolving; no external links; **all 3** named skills exist. |
| The non-author review itself | **this record** (page author: Peter Nguyen, last-touching commit `cce5c378`) |

**Purpose and normal use restated from the page alone:** implementing a behavior change test-first — state the
contract as concrete cases, write the failing test, run it and confirm RED for the intended reason, implement
the minimal change, confirm GREEN plus the wider suite, refactor only under green, and report the loop
transcript with exact commands. Its normal use is: pick the smallest case that forces the change to exist, read
the actual failure output rather than the exit code, change one thing at a time, and keep the reproduction as
the regression test.

**Disputed lines: none. No gap recorded. No line of the page was edited by this lane.**
**Verdict: FULL, no edit. No defect recorded.**

### 5.6 C5-6 — `.claude/skills/tech-spec-writer/SKILL.md`, read whole, FULL

1. **Ranges.** One slice: **L1-191** (the whole file at the bound revision). No elision; longest line 992
   bytes / 990 characters (the frontmatter description).
2. **Every line was read as prose** — the frontmatter description, the reading key, Purpose, Use When with its
   four Do-NOT-use counter-examples, Inputs to Inspect, the eight-step Workflow with its owner-question
   discipline, the Output Format block, Validation Checklist, Gotchas, Stop Conditions and Supporting Files.
3. **Links and named references** were checked mechanically (section 9): the page's two link occurrences
   (rendered text: references/tech-spec-sheet.md, twice) resolve to the one existing target at the bound
   revision; no external links; no in-page anchors; **all 6** distinct backticked skill names exist.

**The six acceptance bullets, addressed.**

| Bullet | C5-6 `tech-spec-writer/SKILL.md` |
| --- | --- |
| Purpose and audience up front | **yes.** The frontmatter description (L3) states the artifact, its sections and its boundaries against ADR and product spec; L14-25 states the failure the artifact prevents and what the skill composes. Use When addresses the reader directly. |
| Abbreviations and coded identifiers defined at first use | **yes.** The reading key at L8-10 expands ADR, RFC, API and PII before the body; `hot paths` (L78) is below library norm and is recorded as an **observation, not a gap**, in section 6 with the resolving sentence; `cross-cutting concerns` is resolved by the page's own enumeration at L77-81; `observability` is a library convention, measured in section 6. |
| Descriptive headings, lists or tables, and at least one concrete example | **yes.** Eight headed sections; an eight-step workflow; a copyable Output Format block (L114-127) listing the spec's sections; a Validation Checklist; and concrete examples of the failure modes (L149-150 "A tech spec with no non-goals expands in review until it's a re-architecture"; L156-158 "Show the roads not taken"). |
| Shipped behaviour separated from proposed or blocked behaviour | **yes.** L144-145 requires known, assumed and open to be separated and forbids "confident fiction over unresolved design"; L84-97 states the owner-question discipline and that an answer "sets the design only and does not authorize starting the build". |
| Navigation links current and every referenced file or command existing | **yes.** 2 Markdown link occurrences over 1 target — exists at the bound revision; no external links; no in-page anchors; **all 6** named skills exist. |
| The non-author review itself | **this record** (page author: Peter Nguyen, last-touching commit `67f577e2`) |

**Purpose and normal use restated from the page alone:** writing the technical spec / design doc for a
substantial engineering change — problem and why now, goals and explicit non-goals, the proposed design with its
data model and interfaces, the alternatives weighed, the cross-cutting concerns designed up front, risks and
open questions with owners, and the review and sign-off path — while composing rather than duplicating the ADRs,
the architecture and the product spec. Its normal use is: frame the problem, present the design, show the
alternatives, design the concerns teams forget, state risks, define sign-off, and cite the owning artifacts for
the decisions inside it.

**Disputed lines: none. No gap recorded. No line of the page was edited by this lane.**
**Verdict: FULL, no edit. No defect recorded.**

### 5.7 C5-7 — `.claude/skills/tech-spec-writer/references/tech-spec-sheet.md`, read whole, FULL

1. **Ranges.** One slice: **L1-72** (the whole file at the bound revision). No elision; longest line 127
   bytes / 127 characters.
2. **Every line was read as prose** — the title and use-with-the-parent lines, the reading key, the tech-spec
   template block, the cross-cutting-concerns checklist, and the spec-versus-ADR-versus-product-spec
   discriminator table.
3. **Links and named references** were checked mechanically (section 9): the page's one link occurrence
   (rendered text: Tech Spec Writer) resolves at the bound revision; no external links; no in-page anchors;
   **1** distinct backticked skill name exists (`tech-spec-writer`), and the six further skill names the
   page gives in plain text — `adr-writer`, `architecture-designer`, `latency-budget-architect`,
   `observability-operator`, `pii-lifecycle-designer`, `product-spec-writer` — each resolve to a real
   skill at the bound revision.

**The six acceptance bullets, addressed.**

| Bullet | C5-7 `tech-spec-sheet.md` |
| --- | --- |
| Purpose and audience up front | **yes.** L1 is the title, L3 states the owning skill and the reading mode ("Use this reference with the Tech Spec Writer"), and L5 states it is detail to read on demand. |
| Abbreviations and coded identifiers defined at first use | **yes.** The reading key at L7-9 expands API, ADR, authn, authz, PII and E2E before the body. Two further coded items are below library norm and are recorded as **observations, not gaps**, in section 6 with the resolving sentence for each: `hot paths` and the `expand→migrate→contract` sequence; `blast radius` is a library convention, measured in section 6. |
| Descriptive headings, lists or tables, and at least one concrete example | **yes.** Three headed sections; the full tech-spec template as a copyable block (L13-46); an eight-item checklist (L50-57); and a four-row discriminator table comparing scope, question, content and relationship across tech spec, ADR and product spec — a worked comparison rather than an assertion. |
| Shipped behaviour separated from proposed or blocked behaviour | **yes.** The sheet is a template and a checklist and claims no shipped behaviour; the template's review-and-sign-off section (L44-45) and its risks section (L37-42) keep what is proposed separate from what is agreed. |
| Navigation links current and every referenced file or command existing | **yes.** 1 Markdown link occurrence over 1 target — exists at the bound revision; no external links; no in-page anchors; **1** backticked skill name and the **6** further plain-text skill names all exist. |
| The non-author review itself | **this record** (page author: Peter Nguyen, last-touching commit `02e88b18`) |

**Purpose and normal use restated from the page alone:** the owning skill's detail sheet — the fill-in
tech-spec template, the cross-cutting-concerns checklist covering security, privacy, performance,
observability, migration, rollout, testing and failure modes, and the discriminator that tells a tech spec from
an ADR from a product spec. Its normal use is: open it beside the parent skill, copy the template into the
spec, work the checklist item by item, and use the last row of the discriminator table to route anything that
belongs to a neighbouring artifact.

**Disputed lines: none. No gap recorded. No line of the page was edited by this lane.**
**Verdict: FULL, no edit. No defect recorded.**

### 5.8 C5-8 — `.claude/skills/tenant-isolation-reviewer/SKILL.md`, read whole, PARTIAL

1. **Ranges.** One slice: **L1-173** (the whole file at the bound revision). No elision; longest line 892
   bytes / 886 characters (the frontmatter description).
2. **Every line was read as prose** — the frontmatter description, the reading key, Purpose, Use When with its
   four Do-NOT-use counter-examples, Inputs to Inspect, the nine-step Workflow, the Output Format block,
   Validation Checklist, the Tenant Isolation Rules, the Security Rules, Gotchas, Stop Conditions and
   Supporting Files.
3. **Links and named references** were checked mechanically (section 9): the page's two link occurrences
   (rendered text: references/isolation-surface-checklist.md, twice) resolve to the one existing target at the
   bound revision; no external links; no in-page anchors; **all 6** distinct backticked skill names exist; and
   the page's own completeness claim was measured: L168-170 calls the companion "the fifteen-surface
   checklist", and the companion's table carries exactly **15** numbered surface rows (verified).

**The six acceptance bullets, addressed.**

| Bullet | C5-8 `tenant-isolation-reviewer/SKILL.md` |
| --- | --- |
| Purpose and audience up front | **yes.** The frontmatter description (L3) states the scope ("across EVERY surface — identity, data, API, storage, logs, analytics, support tooling, exports, imports, background jobs, search, AI retrieval, billing, feature flags, and audit — not just the database") and the deliverables; L14-20 states the verdict the skill produces and the honesty rule that a never-examined surface is reported as not-inspected. Use When addresses the reader directly. |
| Abbreviations and coded identifiers defined at first use | **PARTIAL — this is the batch's one gap.** The reading key at L8-10 expands RLS and IDOR, and AI is written out at L26, but `authn` is used unexpanded at **L36** ("the ask is a full security review beyond tenancy (authn, injection, secrets)") and is defined nowhere in the page; the page's own linked companion `references/isolation-surface-checklist.md` contains neither `authn` nor the word "authentication" (both measured). The measurements and the full reasoning are in section 6. |
| Descriptive headings, lists or tables, and at least one concrete example | **yes.** Nine headed sections; a nine-step numbered workflow; a copyable Output Format block (L89-101); two checklists; and concrete examples throughout (L74 "tenant A does X → sees tenant B's Y"; L144 "404-vs-403 responses and per-tenant error detail leak tenant existence"; L148-149 caches keyed without tenant context). |
| Shipped behaviour separated from proposed or blocked behaviour | **yes.** The page reviews and specifies; it states at L84-85 "Recommend fixes; do not implement them in this pass" and repeats it in the checklist at L116, and Stop Conditions route a confirmed live CRITICAL leak to immediate reporting and a separate, scoped fix rather than an in-pass edit (L160-164). |
| Navigation links current and every referenced file or command existing | **yes.** 2 Markdown link occurrences over 1 target — exists at the bound revision; no external links; no in-page anchors; **all 6** named skills exist; the page names no shell command. |
| The non-author review itself | **this record** (page author: Peter Nguyen, last-touching commit `8459ac73`) |

**Purpose and normal use restated from the page alone:** producing an evidence-based verdict on whether tenants
can reach each other's data across every surface a system exposes — severity-ranked findings each tied to
file:line evidence and a concrete tenant-A-reaches-tenant-B scenario, an isolation test matrix per surface, a
negative-test plan that observes denial, and an explicit not-inspected list. Its normal use is: confirm there is
a real artifact to review, pin the tenant boundary, enumerate and classify every surface before any finding,
trace each applicable surface from entry point to data access, probe the classic holes, and report confirmed
findings separately from suspected ones — recommending fixes, never implementing them in this pass.

**Disputed lines: none. The gap is a first-use-definition gap in the page's own bytes, named by line above; no
line of the page was edited by this lane.**
**Verdict: PARTIAL, no edit. Named gap G-C5.1: `authn` at L36, an abbreviation used at first use with no
on-page definition and no companion that defines it.**

## 6. The library-norm measurements taken before any gap was flagged — and the page-resolves-it test

**The rule this lane applied, in two halves.** *First, measure before flagging:* **an unglossed term that is a
library-wide convention is not a per-page defect** — it is recorded as an **observation with its count**, because
the library's shared vocabulary is not owed by any one page. *Second, and stronger:* **for every below-norm
term a page actually uses, check whether the page itself resolves it** — does its own sentence, or its own
linked companion, supply the meaning? If it does, the term is **an observation, not a gap**. A term becomes a
**gap** only when all three hold: its prevalence is well below the library norm, the page's own bytes and its own
linked companion both fail to supply the meaning, and the library's established practice is to gloss it — so this
page's silence departs from the norm rather than following it.

**How every number below was produced.** By command, in this session, over the **657 reader pages** at the
bound revision `3b0d6cd5…` — the instrument's own tree classification, loaded once with
`git ls-tree -r --name-only` and `git cat-file --batch` (10,366,770 bytes of Markdown). Single-word terms
are matched **on word boundaries**, coded or multi-word terms **literally**, which is the method the sibling
batch records used and therefore the only method whose numbers are comparable with theirs. Nothing below is
restated from memory or from the brief.

### 6.1 The convention table (measured; recorded as observations, never as gaps)

| Term | Reader pages containing it | Treatment |
| --- | ---: | --- |
| `PR` | 289 | convention |
| `gate` | 278 | convention |
| `CI` | 253 | convention |
| `tenant` | 255 | convention |
| `trigger-evals` | 239 | convention |
| `API` | 206 | convention |
| `manual-only` | 187 | convention |
| `repo` | 169 | convention |
| `runbook` | 147 | convention |
| `verdict` | 131 | convention |
| `fixture` | 117 | convention |
| `SHA` | 111 | convention |
| `UTC` | 107 | convention |
| `observability` | 107 | convention |
| `provenance` | 91 | convention |
| `auth` | 84 | convention |
| `RLS` | 73 | convention |
| `SaaS` | 65 | convention |
| `OWASP` | 62 | convention |
| `blast radius` | 61 | convention |
| `MANUAL-ONLY` (the frontmatter marker token) | 60 | convention |
| `org` | 58 | convention |
| `PII` | 58 | convention |
| `idempotency` | 56 | convention |
| `frontmatter` | 55 | convention |
| `DCO` | 54 | convention |
| `authz` | 53 | convention |
| `webhook` | 49 | convention |
| `idempotent` | 43 | convention |
| `lockfile` | 28 | convention |
| `attestation` | 35 | convention |
| `kill switch` | 38 | convention |
| `normative` | 32 | convention |
| `IaC` | 31 | convention |
| `RAG` | 31 | convention |
| `MCP` | 29 | convention |
| `spike` | 29 | convention |
| `TALI` | 27 | convention |
| `isolated worktree` | 27 | convention |
| `sink` | 23 | convention |

**These measurements corroborate the benchmark table this lane's brief supplied, at a corpus one page larger.**
The brief's figures were taken over ~656 reader pages; this base has **657**, because lane A batch 5's record
became a reader page when pull request #795 merged. Measured here against measured there: `PR` 289 / 289,
`CI` 253 / 252, `API` 206 / 205, `repo` 169 / 168, `verdict` 131 / 130, `SHA` 111 / 110,
`UTC` 107 / 106, `frontmatter` 55 / 54, `authz` 53 / 52, `normative` 32 / 31,
`idempotent` 43 / 42, `sink` 23 / 22-23, `manual-only` 187 / 186, `isolated worktree` 27 / 26,
`trigger-evals` 239 / 238, `org` 58 / 57, `PII` 58 / 57. The differences are the expected
one-page drift between measurement sites and are reported rather than smoothed.

### 6.2 The below-norm terms this batch's pages actually use — and how each page resolves them

Every term below is **below** the library norm (roughly 26 pages) and is used unexpanded by a page in this
batch. Each therefore had to pass the stronger test. **Seven of the eight pages are FULL, and this table is
where that is earned or lost:** a term is an observation only where the page's own bytes (or its own linked
companion) supply the meaning, and the justification is recorded per term rather than asserted in a block.

| Term (count over 657) | Page and line | Does the page itself resolve it? — the justification | Treatment |
| --- | --- | --- | --- |
| `safetensors` (**3**) | C5-1 L108, L141, L153 | **Yes, by C5-1's own sentence.** L141 states the defining property inside the promotion table: "Non-executable format (for example `safetensors`) or a verified restricted loader", against the same row's failing case "Pickle-based checkpoint promoted to production". L102-109 has already explained why an executable pickle is the hazard ("can execute arbitrary code from an untrusted artifact") and directs the reader to prefer it. A reader who does not know the format recovers what it is: the non-executable model format. | **observation** |
| `Sigstore` (**1**) | C5-1 L92 | **Yes, by C5-1's own sentence, and it is a named third-party tool.** L92 reads "Releases signed/attested (Sigstore/provenance) where the ecosystem supports it?", which places it as the mechanism of the signing/attestation the same sentence asks about; L140 then states exactly what a signature or attestation does ("ties the digest to the build job, source revision, base model, and data snapshot; verified at promotion AND at load"). The page treats every named tool this way — `PyTorch` (L104), `npm`/`cargo`/`python` (L68), `Dockerfile`/`Makefile` (L69) — none of which it expands either. | **observation** |
| `transitive` (**9**) | C5-1 L39 | **Yes, by C5-1's own sentence.** L39 asks "Is the vulnerable package a **direct** or **transitive** dependency?" and L40-41 tells the reader how to tell them apart ("Compare the lockfile with the resolved installed graph in the reviewed environment; a lockfile entry alone does not prove what was installed"). The direct/transitive contrast against the resolved installed graph supplies the meaning: pulled in indirectly rather than declared. | **observation** |
| `PRODUCT-BUG` (**3**) | C5-3 L34 | **Yes, by C5-3's own sentence.** L32-34 places it as one value of an enumerated classification: "the question is which jobs in a CI run failed and why, by cause class — `ci-failure-classifier` classifies first; it hands a `PRODUCT-BUG` with an unknown cause back here." The reader learns it is a cause class (as against the TEST-BUG class the page's audience is routing around) and that it means a failure attributed to the product's own behaviour — which is what the two ordinary words say. The label is not opaque the way a numbered phase label is, and the sentence names the skill that owns the classification. | **observation** |
| `heisenbug` (**1**) | C5-4 L46 | **Yes, by C5-4's own sentence — the phenomenon is stated in plain words before the label.** L44-46: "Instrument the BOUNDARY between suspect and victim … not the whole path; too many probes change timing and can hide races (heisenbug)." The parenthetical names a phenomenon the sentence has just described without jargon; a reader who does not know the word already knows what is meant. | **observation** |
| `ulimits` (**1**) | C5-4 L40 | **Yes, by C5-4's own sentence.** L40 reads "resource limits (memory, ulimits, container caps)" — the parent category is stated immediately before the term, so the reader recovers that a ulimit is a per-process resource limit, which is the only thing the checklist item asks them to compare. | **observation** |
| `property-based` (**8**) | C5-4 L28 | **Yes — the row states the operation, and the term is library vocabulary.** L28's amplifier row reads "Capture failing production payload shapes (sanitized); property-based fuzz around the boundary". The instruction is complete and actionable without the modifier (fuzz around the boundary of the captured failing shapes), and the library owns the technique as a first-class named skill (`property-based-test-designer`, in the skills catalog and the README), so the term is a name for something the library already documents rather than a loose coding. Recorded as a judgement with its reason, not as a measurement-only call. | **observation** |
| `ring-fenced` (**2**) | C5-2 L66, L84, L137, L159, L174, L202 | **Yes, by C5-2's own sentence.** L83-86 defines the property at the point of use: "it uses a ring-fenced synthetic account/tenant and a designated test path, and the write is isolated from real tenants and real billing/notifications." The isolating property is stated; L90-91 adds the least-privilege consequence. | **observation** |
| `white-box` (**4**) / `black-box` (**2**) | C5-2 L15, L18, L52, L61, L150 | **Yes, by C5-2's own sentences.** The two are characterised rather than named: L15 "internal white-box telemetry can look healthy", L50-52 "metrics, traces, logs from inside the app — that is `observability-operator` *(manual-only)*; synthetic monitoring is the external black-box complement", and L18-20 "scheduled probes that exercise the real critical journeys and dependencies from the outside, on the same path a user takes". Inside versus outside is exactly the distinction. | **observation** |
| `prod` (shorthand, **21**) | C5-2 L21, L46, L119, L165, L174, L180, L202 | **Yes, by C5-2's own sentences.** The page writes PRODUCTION in full at L18, L30, L56, L82, L96, L105, L115, L120, L133, L167 and L197-203, and pairs the shorthand with it in the same constructions ("a probe runs against PRODUCTION" / "prod-safety contract"; "distinguishes probe-broke from prod-broke"). | **observation** |
| `service-role` (**13**) | C5-8 L51, L70, L126 | **Yes, by C5-8's own sentence.** L51-52 reads "Privileged paths: support/admin tooling, service-role or superuser DB access, background jobs and their credentials" — the term is paired with the plain description "superuser DB access" under the heading "Privileged paths". | **observation** |
| `hot path` (**7**) | C5-6 L78; C5-7 L32, L52 | **Yes — a self-describing compound in the page's own list.** C5-6 L77-81 designs "performance (budgets, hot paths)" among the cross-cutting concerns, and C5-7 L32 and L52 repeat it inside the checklist item "Performance: latency/throughput budgets; hot paths." The two words carry the sense (the paths that run hot), and the same term is used by two other library skills (`code-reviewer`, `profiling-methodology-designer`), so it is vocabulary rather than a private code. | **observation** |
| `expand→migrate→contract` (**4**) | C5-7 L54 | **Yes — the item names its subject and the three ordinary verbs state the order.** C5-7 L54 reads "Migration: schema/data changes; expand→migrate→contract." The reader is told what it applies to (schema and data changes) and the sequence of three operations to plan (expand, migrate, contract). Recorded as a judgement: the *compatibility discipline* behind the sequence lives in the owning pages (`schema-evolution-planner`, `secure-migration-reviewer`, which this page does not link), so a reader recovers the operation order but not the per-stage compatibility rule. The checklist item, as written, is actionable. | **observation** |
| `env var` (**10**; `environment variable` **22**) | C5-4 L37 | **Yes, by C5-4's own heading and sentence.** The section is headed "Environment-delta checklist (fails only in env X)" (L34) and the item reads "env vars/secrets present and non-empty" (L37); the page's parent states the same list as "versions, env vars, data volume, permissions, concurrency" (C5-3 L45). The clipped form sits inside the full word's own heading. | **observation** |
| `mid-batch` (**1**) | C5-5 L123 | **Yes — a transparent two-word compound.** L122-123: "Writing all the tests up front, then all the code, is not TDD — it loses the design feedback and usually produces untestable interfaces mid-batch." "Mid" plus "batch" states its own meaning in a sentence that already names the batch (all the tests, then all the code). | **observation** |
| `n-a` (**3**; the literal substring matches **258** pages, a count that is an artifact of "non-author" — 20 pages — and other "non-a…" words) | C5-8 L92 | **Yes — a template token, and the page's own bytes resolve it.** It appears once, inside the Output Format block: "Surface inventory: <surface — applicable / n-a (why) / not-inspected (why)>" (L92). L61-63 tells the reader what to write there in words ("classify each as applicable, not-applicable (say why), or applicable-but-not-inspectable"), and L113-114 treats an empty not-inspected list as meaningful. It is **not** a library convention — only 3 of 657 reader pages carry the token — so this row rests on the page's own bytes, not on prevalence. This is the same class as the `r/w` template token lane A batch 5 and the `[SEV]` token lane B batch 5 recorded as observations rather than gaps. | **observation** |
| `pen test` / `pen-test` (**7** together; `penetration` **2**) | C5-8 L25, L53 | **Yes — and the library's own practice is the clipped form.** L25 places it among security-assurance triggers the reader already knows ("before an enterprise or regulated-customer onboarding, a security questionnaire, or a pen test") and L53 names its output as a review input ("Prior incidents, existing isolation tests, and pen-test reports if any"). Measured: of the **7** reader pages that use the clipped form, only **1** also writes "penetration" — so the library's established practice is to use the short form as vocabulary, and this page follows it rather than departing from it. The third condition of the gap test therefore fails. | **observation** |
| `authn` (**14**) | C5-8 L36 | **No — neither the page nor its own linked companion resolves it. THIS IS THE BATCH'S ONE GAP (G-C5.1).** L36 uses it at first use inside a parenthetical list: "the ask is a full security review beyond tenancy (authn, injection, secrets)". The page's reading key (L8-10) expands its two other abbreviations, RLS and IDOR, and does not expand this one; the page's own linked companion `references/isolation-surface-checklist.md` contains **neither** `authn` **nor** the word "authentication" (both measured by command). Measured practice: of the **14** reader pages that use `authn`, **11** also supply its expansion — so the library's established practice **is** to gloss it, and this page is one of the **3** that do not (`.claude/skills/security-pr-reviewer/SKILL.md`, this page, and `docs/prompts/phased-claude-skills-prompts.md`). All three conditions of the gap test hold. | **GAP — C5-8 is PARTIAL** |

**The distinction, stated so it is not left implicit.** What separates `authn` from every other row above is not
its count — `Sigstore` (1), `ulimits` (1) and `heisenbug` (1) are rarer still and are observations. It is
that those terms are resolved by the page's own bytes, and `authn` is not resolved by either the page or the
companion it links, **while the library's own practice is to resolve it**. A term the page defines, or that its own
sentence explains, is not a defect however rare it is; a term left bare when eleven of fourteen sibling pages
gloss it is.

**The frontmatter-position rule was also applied as a norm.** *Frontmatter position* is the observation that a
page's YAML metadata header may expand an acronym later than its first use in the body; the brief records that
about 60% of pages with a frontmatter description do this. Five pages in this batch carry frontmatter
(C5-2, C5-3, C5-5, C5-6, C5-8) and **no page in this batch is flagged for it** — it is a norm, not a defect.

### 6.3 Specific claims on the pages that were measured rather than accepted

The reading standard says not to over-assert completeness. Three pages make completeness or count claims about
their own companions, and each was measured:

- **C5-8's "fifteen-surface checklist" (L169)** — the companion's table carries exactly **15** numbered surface
  rows. **The page's claim is true.**
- **C5-2's "No `references/`" (L223)** — the skill directory contains only `SKILL.md`, `evals/evals.json` and
  `evals/trigger-evals.json`. **The page's claim is true.**
- **C5-2's description of its two eval files (L216-222)** — all four named behaviour cases are present in
  `evals.json`, and all five named discriminating neighbours are present in `trigger-evals.json`. **The claim is true.**

Everything else this batch says about a list is scoped: where a count is given above it is a measured count, and
where a line list is given it was produced by grep over the page's bytes and then confirmed by the whole-page
read — not asserted from memory.

## 7. The row-quote strings offered to the keeper — and the pages that get NO row

### 7.1 THE PARTIAL-PAGE RULE, stated explicitly (this is the C-4 rule)

**A page this record marks PARTIAL gets NO acceptance row of ANY kind. Not a full-page-acceptance row, and not
a targeted-review row. It stays PENDING.** This record states that rule here, in its own words, because the
ledger says it three ways and because the failure mode is mechanical rather than a matter of taste:

- The ledger names four event kinds — `full-page-acceptance`, `targeted-review`, `withdrawal` and
  `lost-commit` — and **has no partial-acceptance kind**. There is therefore no row shape that could honestly
  record a PARTIAL page, and a partial disposition must never be transcribed into a full acceptance.
- `check_index.py` buckets a page as **ACCEPTED** when a row exists, the row's revision is contained in
  `origin/main`, and the page has **zero drift** — and it does so while the page carries **ANY
  non-lost-commit row**. All eight pages in this batch have zero drift at this base (measured: the numstat
  against `origin/main` is empty for every one of them). **A targeted-review row authored for C5-8 would
  therefore silently move a PARTIAL page out of the pending set** — it would un-pend the page without anyone
  accepting it. That is exactly the laundering this rule exists to prevent, and it is why the prohibition covers
  *both* row kinds and not merely the full-page one.
- The rule is not a stylistic preference: **a gap and a FULL disposition must never coexist.** C5-8 has a
  recorded gap (G-C5.1), so its only honest disposition is PARTIAL, and a PARTIAL page keeps no row.

**Consequently the row-quote strings below are offered ONLY for the seven pages this record marked FULL.**
**There is deliberately no row-quote string for C5-8**, and the line that would have carried one instead says in
words that it gets none.

### 7.2 The exact sentence this lane gives any keeper about partial pages

> **The keeper records NO row of any kind for a page this evidence marks PARTIAL — no full-page-acceptance row
> and no targeted-review row. A partial page stays PENDING.** Of this batch's eight pages, **C5-1, C5-2, C5-3,
> C5-4, C5-5, C5-6 and C5-7 are the eligible seven**; **C5-8** (
> `.claude/skills/tenant-isolation-reviewer/SKILL.md`) is **PARTIAL** for the gap named at its **L36** and
> **must receive no row at all**. Offering it a targeted-review row because the drift happens to be zero would
> not be a lesser acceptance — it would be an un-pending, because this instrument counts a page as accepted
> while it carries any non-lost-commit row and has zero drift.

### 7.3 The verbatim quote lines (evidence, not rows)

Each line below appears in this file byte-for-byte, states the disposition honestly, and contains the full
40-character acceptance revision. **These are evidence lines for the separate eligible keeper to record from —
this lane authors no acceptance row and allocates no row ID.**

```text
C5-1 accepted: .claude/skills/supply-chain-security-reviewer/references/supply-chain-checklist.md read whole at 3b0d6cd54222442e2e0b1598829bd078c03a22d4
C5-2 accepted: .claude/skills/synthetic-monitoring-architect/SKILL.md read whole at 3b0d6cd54222442e2e0b1598829bd078c03a22d4
C5-3 accepted: .claude/skills/systematic-debugger/SKILL.md read whole at 3b0d6cd54222442e2e0b1598829bd078c03a22d4
C5-4 accepted: .claude/skills/systematic-debugger/references/isolation-tactics.md read whole at 3b0d6cd54222442e2e0b1598829bd078c03a22d4
C5-5 accepted: .claude/skills/tdd-engineer/SKILL.md read whole at 3b0d6cd54222442e2e0b1598829bd078c03a22d4
C5-6 accepted: .claude/skills/tech-spec-writer/SKILL.md read whole at 3b0d6cd54222442e2e0b1598829bd078c03a22d4
C5-7 accepted: .claude/skills/tech-spec-writer/references/tech-spec-sheet.md read whole at 3b0d6cd54222442e2e0b1598829bd078c03a22d4
C5-8 PARTIAL - NO ROW AND NO ACCEPTANCE OF ANY KIND: .claude/skills/tenant-isolation-reviewer/SKILL.md read whole at 3b0d6cd54222442e2e0b1598829bd078c03a22d4 - gap at L36 (authn used as an abbreviation with no on-page definition and no companion that defines it); this page stays pending
```

## 8. Count honesty, the expected diff, and the self-cost

- **This batch's honest count: 7 FULL / 1 PARTIAL of eight pages, one named gap.** A worse-looking honest
  number is the correct output. Nothing here is rounded toward more acceptances, and the seven FULL verdicts
  stand only because every candidate gap on them was rejected by measurement against the 657-page corpus
  (section 6), term by term, with the resolving sentence recorded for each.
- **This lane publishes no readability count of its own.** The owner's **D84** decision made the instrument
  the official pending count; the instrument's figures at the base are quoted in section 1 as the instrument's,
  and this record adds none. **No post-commit bucket figure is predicted anywhere in this record.**
- **The instrument reads recorded acceptances from the committed `acceptance-index.json`.** This record is
  itself a new reader page with no acceptance row, so it is **pending** and is not counted among accepted
  pages; the eight read pages do not move any bucket here because **no row is recorded by this lane**. The
  buckets move only when the separate keeper's rows are recorded and a rebuild runs at a ref containing them.
- **No `--write` was run by this lane**; every tool invocation in section 9 is a read-only report. No
  `build_index.py` run of any kind was made, and `tools/` is untouched by this change.
- **Expect diff — every line this lane changes.** Against the derivation base `3b0d6cd5…`:

| Path | Added | Deleted | Source |
| --- | ---: | ---: | --- |
| `docs/evidence/documentation/readability-lane-c-batch-5-2026-10-15.md` | new file | **0** | this record |

  **Nothing else is in the diff.** No code, no workflow, no script, no `tools/` artifact, no JSON, no ledger
  edit, no keeper row and no protected path — the lane is Markdown-only by construction, which is why the
  pull request answers the security question **No**. The eight read pages are **not** modified. The deleted-line
  count is **0**, taken by counting every patch line beginning with a single minus rather than by a regex over
  the patch text; the measured numstat is recorded in the pull-request body after the commit exists.
- **Self-cost.** This batch record is itself a new reader page with no acceptance row, so it is pending and is
  not counted among accepted pages — the self-cost every prior batch record states. At this record's head the
  instrument would read **658** reader pages rather than 657, the one added page being this record.

## 9. Validation actually run (commands and their real results)

| # | Command | Result |
| --- | --- | --- |
| 1 | `git rev-parse origin/main` at clone time | `3b0d6cd54222442e2e0b1598829bd078c03a22d4` (the derivation base; unchanged at every re-measure this session) |
| 2 | `python -P -B tools/readability_acceptance/check_index.py --quiet --ref 3b0d6cd5…` | exit 0; the summary quoted in section 1 |
| 3 | `git ls-tree -r --name-only 3b0d6cd5…` | 723 Markdown paths; 65 fixtures; 1 generated report; **657** reader pages |
| 4 | per-path check against the index's `reader_pages` **and** `events` arrays | all 8 paths absent from both (pending, as derived) |
| 5 | `git merge-base --is-ancestor 3b0d6cd5… refs/remotes/origin/main` | exit 0 (the acceptance revision is contained in main) |
| 6 | `git rev-parse 3b0d6cd5…:<page>` × 8 | the eight full 40-hex blob IDs in section 4 |
| 7 | `git show 3b0d6cd5…:<page>` × 8 | line/byte counts in section 4 reproduced; total **1,239 lines / 71,217 bytes**; longest line 1,003 bytes (C5-2) |
| 8 | `git diff --numstat 3b0d6cd5… refs/remotes/origin/main -- <page>` × 8 | empty for all eight — zero drift, so the reads are not voided |
| 9 | `python -B scripts/ci/check-markdown-links.py` over the 8 pages | exit 0: files **8**, links checked **10**, anchors checked **2**, broken **0**, dead **0**, external-skipped **0**, other-skipped **0** |
| 10 | `python -P scripts/validate-skills.py` | exit 0: `OK: 205 skill(s) valid, 0 warning(s)` |
| 11 | `python scripts/tests/test_validator.py` | exit 0: `OK: 181 gate self-test assertion(s) passed.` |
| 12 | link-target existence over the 8 pages | **10** link occurrences over **7** distinct resolved targets — all 7 exist at the bound revision |
| 13 | named-file and named-skill existence over the 8 pages | **32** distinct backticked names resolve to a real skill or agent; **0** hyphenated names unresolved; every claimed `evals` file exists and its contents match the page's description of it (C5-2, C5-3, C5-5, C5-6, C5-8) |
| 14 | page-claim measurement | C5-8's "fifteen-surface checklist" = **15** measured rows; C5-2's "No `references/`" = **true** |
| 15 | `git log -1 --format="%h %an %s" -- <page>` × 8 | other authors only (section 3 table) |
| 16 | `git log --all --author="F reviewer" --oneline -- <page>` × 8 | **0** commits for every page (the stale identity never touched them) |
| 17 | `git log --all --author="F reviewer" --oneline` | **11** commits, all on other lanes' branches or open pull requests; disclosed in section 3 |
| 18 | batch-record extraction and cross-check (19 records at their branch heads) | **152** read slots, **152** distinct pages; lane A→0–39, lane B→148–187, lane C→296–327, lane D→445–486 (gaps 460, 461); lane C's 32 match exactly, in order, no gap |
| 19 | library-norm measurement over the 657 reader pages (section 6) | 40-term convention table plus 17 below-norm terms measured with their page-resolves-it justification |
| 20 | `git diff --check` | exit 0 — no output |
| 21 | `python -P -B scripts/check_dco.py --range origin/main..HEAD` | recorded in the pull-request body after the commit (a commit cannot cite its own not-yet-made commit as a result) |
| 22 | `python -P scripts/ci/check_pr_body_skills.py --body-file <the posted body>` | exit 0 — `PR body bound fields: OK` (recorded in the pull-request body) |

The mechanical link output is a **candidate list, never a defect list**; the repository's own instrument is the
adjudicating one, and no page was edited in any case.

## 10. What this batch could not verify (stated, not hidden)

- **The page-claim verifications are bounded by what the repository can answer.** C5-1's statements about which
  loading mode a given PyTorch release defaults to, and C5-2's statements about third-party probe providers, are
  the pages' own dated research. This batch verified that the pages say where and what they checked — it did
  **not** re-test the vendors, and it did not fetch a single external URL. The link checker reports
  **external-skipped 0** for these eight pages because none of them carries an external hyperlink; the
  vendor claims are prose, not links, and are outside what this batch measured.
- **Continuous integration at this exact head is owed, never claimed.** The record's own commit is new, so no
  CI run result for it can be reported here; the offline checks in section 9 are the ones actually run. The
  pull-request body records the run once it exists.
- **The six `cannot_decide` (lost-commit) pages remain undecided.** This batch did not investigate whether
  their lost commits are recoverable; that is outside lane C's scope and no lane owns them.
- **C5-8's named gap is recorded, not fixed.** Whether the page's `authn` warrants a repair pull request,
  and in which change class, is a decision this batch does not make; editing an instruction file under
  `.claude/skills/` would move the change out of the docs-only class.
- **The two unread pages behind lane D's frontier (indices 460, 461) are reported, not routed.** This batch
  measured them and states them in section 2; whether and when lane D reads them is lane D's decision and the
  programme's, not this lane's.
- **Page authorship is read from git metadata only.** The claim that this lane did not write the eight pages
  rests on `git log` author fields, which are self-asserted; the last-touching commits name Peter Nguyen
  for all eight.
- **The bound-field digest and the footer digest are stated in the pull-request body and below**; both were
  calibrated against published values before being trusted, and neither is a substitute for re-measuring this
  record's own bytes after any later edit.

## 11. What this lane did not do

It rewrote no dated snapshot; edited, reordered or deleted no existing keeper row; authored no keeper row and
appended no ledger line; edited none of the eight read pages; added no new section to any page; bound no
acceptance row to the lane's own unmerged head; ran no `build_index.py --write` and rebuilt no `tools/`
artifact; re-read none of the six lost-commit pages of the `cannot_decide` bucket; touched no page outside lane
C's quarter (sorted indices 298–446 of the 595-path pending union) and no page of any sibling lane's quarter;
created no `wt-*` worktree and used no shared clone; and claims no authority beyond recording. The batching
procedure "does not grant provider, private-input, real-host or deployment authority" (ledger, batching
section). The reader is the DeepSeek-4.1-Flash (deepseek-flash) model, stated per the repository's
agent-attribution rule. **No Aegis skill matches this lane's unit of work** — the full-page readability
acceptance re-read is governed by the ledger's own "Acceptance for each page" contract, not by any
`.claude/skills/` entry; the lane-mechanics skills actually applied (`change-classification-gate`,
`acceptance-criteria-reviewer`, `source-of-truth-reconciler`, `scoped-approval-register`) are named and sourced in the
pull-request body's skills table, and the mechanical gates the repository's own instruments provide
(`scripts/validate-skills.py`, `scripts/ci/check-markdown-links.py`, `scripts/tests/test_validator.py`) were run and are
quoted in section 9.

## 12. Timing

- **Work item:** `LaneC-Phase4-Batch5` — Phase 4 re-read, lane C, batch 5: eight whole-page re-reads of
  the lane's next eight pages in the unread sequence, evidence record only.
- **Start:** 2026-10-15T21:59:31-07:00 (America/Los_Angeles), this session's first clock sample, taken before
  the clone.
- **Record written:** between the 22:21 and 22:31 clock samples of this session.
- **Wall time to the head push** is reported in the pull-request body (the commit's own committer time), since
  a commit cannot cite its own time from inside itself. **Active time is not instrumented**; wall time is
  reported as an imperfect comparison, per the repository's measurement rule.

---

## Footer

sha256: 2fbcd4d7875e9c839971071472b79c92a5c5e8d3a4983d2cca1378772295943a

This digest covers the batch record's bytes from the first line through the closing `---` rule line
and its terminating newline, encoded UTF-8 with LF line endings: exactly 90,939 bytes, byte offsets
0 through 90,938 inclusive, lines 1-912. It does not cover the blank separator line between that
rule and the `## Footer` heading, nor this footer. Any edit above the rule needs a fresh validation.
The method was calibrated before it was trusted: applying it to lane C batch 3's committed record reproduces
its published value `db9796c63ac8ab53022d8c4c237e62484cb4786ce19a261b81bbe36d9f58e2f8` exactly, and the same
collapse-and-hash method reproduces the four published bound-field digests this batch calibrated against
(pull requests #783 `3913683c686e6e71`, #787 `82ed906d2f228f0e`, #792 `88300e711714200a`
and #795 `5fabf87b2df899e9`). Drafted by **DeepSeek-4.1-Flash (deepseek-flash)**.
