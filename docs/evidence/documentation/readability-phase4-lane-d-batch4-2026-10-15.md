# Readability Phase 4 re-read lane D — batch 4 record, 2026-10-15

- **Lane:** PHASE 4 RE-READ LANE D (the last quarter, by count, of the sorted pending page list;
  "re-read" means reading each page whole and judging it against the acceptance contract, not
  rewriting it). **Stage:** C (IMPLEMENT — the stage that does the work and records it).
  **Derivation base:** `f490c16f9ed23f3d489e42f7696323bffcce6fd3` (`origin/main`, the pull request
  (PR) #781 merge, "AEGIS-APR-117 withdrawals and fresh re-records"). **This batch's eight pages are
  unchanged between the lane's original batch base `e2a3e20b7c20ef8385b219b39c6405237163406f` and this base**
  (verified per path with `git diff --numstat`; all eight report no change).
- **Agent / model attribution (the repository's 2026-10-13 rule).** This record and every text this
  batch publishes are drafted by **DeepSeek-4.1-Flash (deepseek-flash)**, an AI agent operating under
  the owner account; the agent identity for this batch is
  `readability-phase4-lane-d-batch4-implementer`.
- **What this page is.** The lane's tracked batch record for its fourth batch. It is the
  **evidence source** a **separate eligible keeper** reads under AEGIS-APR-117 (the owner's
  approval-register item letting a different agent re-record rows from the same evidence when the
  original recorder's independence failed; no page needs re-reading for that). **That keeper records no
  row for any of these eight pages**: all eight are partial, and the ledger's PARTIAL rule
  (L5133-5137, L5149-5150 — **base-scoped** line numbers: at today's `main` (`71795e6e`) the same two
  passages are L5584-5588 and L5600-5601) gives a partial page no acceptance row — so the eight **stay
  pending**
  (section 10). **This batch authors no keeper rows and edits no ledger section** — see section 12.
- **Acceptance revision bound by the whole batch and named by every section 10 disposition line:**
  `f490c16f9ed23f3d489e42f7696323bffcce6fd3`. It resolves to itself and is contained in
  `refs/remotes/origin/main` (`git merge-base --is-ancestor f490c16f… refs/remotes/origin/main` exits 0,
  observed in this batch's fresh clone).
- **The batch changed none of the eight read pages**, so the bytes read are the bytes `main`
  carries, and the acceptance is not voided by the merge.
- **Bound-field digest — the commit repairs moved it, and a move voids the verdicts that quoted the
  old figure.** The PROC-04 digest over the three bound fields of this change's pull-request body
  (witness, skills, security, each collapsed to one line, joined in that order, `sha256` over the UTF-8
  bytes, first 16 hex) was **`1fcd0143e13198a3`** at the Stage C head `cac5c67d` — quoted as the first
  audit published it and **not reproduced from the live API** — because PR bodies are edited in
  place and the API serves only the current revision — and it **is** reproducible from the surviving
  saved snapshot of that revision, which this record names here so that the phrase cannot be read as
  "not reproducible": the Stage C batch's own saved body file `_laneD-batch4-scratch/pr_body.md`, **18,953 bytes / 18,881
  characters**, `sha256 8f2196d6684174ef2cf31fb50e5948b9c3066b7ff3887ce1c77091d994c61d72`, a byte-identical copy of which survives as the Stage D clone's `_sd-d-791-clone/_pr791_body.txt` (both
  reproduce **`1fcd0143e13198a3`** with payload lengths 1,175 / 5,152 / 567, re-measured here) — then **`54d5e1e9a06ccbbc`** at
  `d784c4dc` (payload lengths **1,175 / 5,197 / 567**) and **`605d99411a3a6bbe`** at the audited head `c4a55185` (payload lengths
  **1,331 / 5,280 / 567**), and **`4cc13e7e5dfb723a`** at the head `5e336ea2` (payload lengths **1,331 / 5,280 / 567** —
  *the same three lengths as the value before it*, which is the hazard stated next). **The security
  field, 567, did not move**; the movement is entirely the witness (1,175 → 1,331) and the skills
  field (5,197 → 5,280). **SAME LENGTHS, DIFFERENT BYTES, and that is a standing hazard: `605d99411a3a6bbe` moved
  to `4cc13e7e5dfb723a` with the payload lengths 1,331 / 5,280 / 567 on BOTH sides**, because the witness's
  candidate-head SHA and all six skills rows' `target=` SHAs are 40 hex characters replaced by 40 hex
  characters. **A guard that watches payload length alone passes while the digest moves.** **Any
  edit to a bound field voids that figure and requires a fresh one, exactly as a moved head does —
  so all three prior Stage D verdicts are void at the head this repair produces, and a fresh Stage
  D/F is owed there.** This repair's own body revision moves the figure again (its witness names the
  new head), so the post-repair value must be re-derived from the live body and is stated there,
  outside all three bound fields; **this record asserts no bound-field digest of its own and names
  no verdict as covering it.**

## Labels used in this record, glossed (plain-English description beside every internal label)

- **lane D** — the fourth and last of the four count-based quarters of the pending list; four lanes
  run concurrently and each owns a contiguous, non-overlapping quarter.
- **AEGIS-APR-039** — the owner's standing grant for backlog work, commits, pushes and PRs.
- **AEGIS-APR-101** — the keeper-independence rule: the agent that records an acceptance row must
  differ from the page's author **and** from the accepting reviewer.
- **AEGIS-APR-117** — the route that lets a different eligible agent re-record rows from the same
  evidence after a withdrawal; **no page needs re-reading** for it, and for the eight pages here it
  records **no** row, because all eight are partial and the ledger has no partial-acceptance kind
  (section 10).
- **AEGIS-APR-115** — the standing index-rebuild PR scope (it rebuilds `tools/` JSON; this batch
  does not run it).
- **AEGIS-APR-118** — the owner's classification of the readability acceptance tool as
  security-relevant.
- **keeper** / **keeper row** — the ledger's recorded acceptance entry for a page.
- **ledger** — `docs/roadmaps/aegis-documentation-readability-backlog.md`, the tracked
  documentation-readability backlog and acceptance record.
- **D73 / D84** — numbered owner decisions in the ledger: D73 governs the index/rebuild flow, D84
  fixes `check_index.py`'s summary as the official pending count.
- **cannot_decide** — the instrument's bucket for the six pages whose recorded acceptance was lost
  in a lost-commit event; they count pending and belong to **no lane** (section 2).
- **no_recorded_acceptance / provably_pending** — the instrument's two buckets that together form
  this batch's pending set: pages with no keeper row at all, and pages whose row is stale past the
  10-line/new-section rule.
- **PROC-04** — the repository's rule that a published figure names its method.
- **DCO** — Developer Certificate of Origin; the sign-off trailer every commit here carries.
- **LD-25 … LD-32** — this batch's eight row labels, continuing the lane's sequence (batch 1 =
  LD-1…LD-8, batch 2 = LD-9…LD-16, batch 3 = LD-17…LD-24).

## 0. Pre-flight (run before the first edit of this repair round)

The state this round edited, re-derived with the commands shown rather than carried from a brief. It is
a snapshot of one moment: it proves that these objects existed and read this way when measured, not
that any claim in this record is true, and not that any count is right.

| Item | Observed | Command |
| --- | --- | --- |
| Branch and head | `docs/readability-phase4-lane-d-batch4-20261015` at `61371fa5b3014c95922fb9f2b2a07f6a3f953fbe`; the API and `git rev-parse HEAD` in this round's fresh clone agree on the same 40 characters | `git rev-parse HEAD`; `gh api pulls/791` |
| Merge base | `f490c16f9ed23f3d489e42f7696323bffcce6fd3` (`git cat-file -t` = `commit`); the head is **not** an ancestor of `origin/main` (`merge-base --is-ancestor` exits 1), so the branch is unmerged | `git merge-base 61371fa5 origin/main` |
| Record at the head | blob `be2f7fc6ee5371343d2c601cd4843a38b13de314`, **66,015 bytes**, **689 LF / 0 CR** | `git rev-parse HEAD:<path>`; `git cat-file -s <blob>` |
| Record at the merge base | absent — `git cat-file -e f490c16f:<path>` exits 128, so the change is a pure addition | `git cat-file -e` |
| Live body before this round's edit | **56,046 UTF-8 bytes / 55,778 characters**, `sha256 b1ff423e6d58a8e24d7260dcc99afcfa728daca4840a1dab70eb8133356332b6`, last edited **2026-10-17T02:14:40Z** (the 11th of 11 edits) | `gh api pulls/791`; GraphQL `userContentEdits` |
| Required checks | `gate-guard` and `validate-skills` **success**, each having run at that head; `changes` success; the three tool jobs skipped by the docs-only path filter | `gh api commits/61371fa5/check-runs`; `branches/main/protection` |
| Branch state | `OPEN`, not draft, `MERGEABLE`, `mergeStateStatus BLOCKED`, `reviewDecision REVIEW_REQUIRED`, 0 approving reviews | `gh pr view 791 --json mergeable,mergeStateStatus,reviewDecision` |

**What this block does not prove.** It does not re-verify one acceptance count, disposition, gap, page
binding or digest before the edit; those are checked after it. The body row is dated to the revision
read here, and **this repair's own metadata write moves it again** — the record states no body digest.

## 1. The instrument's figures, quoted at both bases

```text
python -P -B tools/readability_acceptance/check_index.py --json --ref refs/remotes/origin/main
compared_ref f490c16f9ed23f3d489e42f7696323bffcce6fd3, reader_pages_in_tree 655,
accepted_on_recorded_review 56, provably_pending 5, no_recorded_acceptance 588,
recorded_acceptance_within_10_lines 0, within_10_not_covered_by_targeted_review 0,
cannot_decide 6, official_pending_count 599
exit 0
```

The same instrument at the lane's original batch base `e2a3e20b7c20ef8385b219b39c6405237163406f`
(run in this clone against that revision and that revision's own committed index JSON) reports
`653 / 57 / 4 / 586 / 0 / 0 / 6 / 596`, which reproduces the figure batch 1, 2 and 3 each published.

**This lane publishes no readability count of its own** (ledger L19-31, D84) and presents the
figures above as the instrument's, not as its own measurement.

## 2. The lane derivation, stated with its commands — and the boundary it moved

1. **The pending set at the derivation base.** The instrument's two pending buckets are
   `no_recorded_acceptance` (**588**) and `provably_pending` (**5**): **593 paths**. The
   `no_recorded_acceptance` figure was reproduced independently by replicating the instrument's own
   `classify_tree` (every tracked `.md` path at the ref, minus the `scripts/` fixtures except
   `scripts/tests/fixtures/README.md`, minus the one generated report) and subtracting the paths the
   committed `tools/readability_acceptance/acceptance-index.json` carries rows for; the five
   `provably_pending` paths were read from the same command's `pending` array.
2. **The quarters.** The 593 paths were **sorted**, then split into **four contiguous quarters by
   count**: `ceil(593 / 4) = 149` for the first three and the remainder for the last —
   **149 / 149 / 149 / 146**. **Lane D takes the last quarter: 146 pages, sorted indices 447-592
   (0-based) of the 593. First path**
   `docs/evidence/documentation/full-page-readability-batch-after-713-2026-10-10.md`, **last path**
   `tools/behavioral_eval_runner/README.md`. Lane C at this base is indices 298-446 and ends at
   `docs/evidence/documentation/full-page-readability-batch-after-234-2026-09-24.md`.
3. **The boundary moved, and this is stated rather than smoothed over.** At the lane's original
   batch base `e2a3e20b` the pending set was **590** (586 + 4), the quarters were
   `148 / 148 / 148 / 146`, and lane D began at index **444**. Three paths **entered** the pending
   set between the two bases and none left it: `docs/delivery-workflow.md`,
   `docs/evidence/documentation/readability-apr117-withdrawals-and-rerecord-2026-10-15.md` and
   `docs/roadmaps/OWNER-DECISIONS-2026-10-15.md`. **Two of the three are new files added to `origin/main` between the two bases — but by two different
   pull requests: the APR-117 withdrawal and re-record record by PR #781, and the owner-decisions
   page by PR #786.** *(Gloss: **PR #786** is the merge `cff725958c386592cd61a5d9acfcb16cd6c72c09`, "docs: publish the owner's 2026-10-15
   decisions as OWNER-DECISIONS-2026-10-15.md"; **PR #770** is the merge `7abb98eb`.)* Measured twice from
   two independent sources: `git log --first-parent --diff-filter=A f490c16f -- docs/roadmaps/OWNER-DECISIONS-2026-10-15.md` returns exactly `cff725958c386592cd61a5d9acfcb16cd6c72c09` — the **PR #786 merge** — and `git diff --name-only cff72595^1 cff72595` names that one
   path and nothing else, while `git diff --name-only f490c16f^1 f490c16f` names the APR-117 record and the ledger and **not** that path;
   the path is **absent** at `e2a3e20b`, at the **PR #770** merge `7abb98eb` and at the **PR #781 branch tip**
   `bfcf402a`, and **present** at `cff72595`; and the API agrees — `pulls/786/files` lists that one added file, `pulls/781/files` lists
   the APR-117 record (added) and the ledger (modified), and `commits?path=docs/roadmaps/OWNER-DECISIONS-2026-10-15.md` returns exactly one commit, `08856b64`.
   **This half of the claim was repaired only at the second attempt, and the round that narrowed it
   without fixing the surviving half is recorded here rather than smoothed over: the third repair
   round replaced the false "all three added to `origin/main` by PR #781" with "two of the three are new
   files that PR #781 added", which made the `docs/delivery-workflow.md` half true and re-asserted this surviving half as
   new text. A half-corrected attribution is worse than the original because it looks checked.**
   **The third, `docs/delivery-workflow.md`, is not new and PR #781 did not add it:** it already exists at `e2a3e20b` (blob `bff407a65a`;
   added to `origin/main` on 2026-10-03 by `c3527560`, PR #653), and it entered the pending set by **drifting out
   of its recorded acceptance** — **24 added and 0 deleted lines** against ledger row **K-075**
   (`last_acceptance_sha 79c5c590`, `blob_id bff407a65a`, reviewer `readability-closeout-implementer-c`), past the 10-line rule, its blob moving `bff407a65a → 9a2ea2bd`; the touching commit
   inside the window is **`7baf0b57`** (AEGIS-APR-137), which reached `origin/main` through the **PR #770** merge,
   not #781. **The set therefore grew by two new files plus one acceptance regression, not by three
   additions**, and the measured deltas agree: `accepted_on_recorded_review` fell **57 → 56** and `provably_pending` rose **4 → 5**, with
   that one page the only page in both deltas. The quarter start therefore moved **444 → 447 (+3)**,
   and two pages that were in lane D's quarter at the older base — `full-page-readability-batch-after-233` and `…-after-234` — now fall in
   **lane C's** quarter at this base while batches 1 and 2 of lane D already read them. **Reported
   to the coordinator, not decided here** (section 8, O-1): it is a cross-lane overlap created by
   the base moving, and this batch does not touch either page.
4. **"The first 24 paths" re-derived, not taken on trust.** Batches 1, 2 and 3 each derived at
   `e2a3e20b` and published their sorted indices. **The three lists were read from each batch's own
   tracked record at its pull-request branch head — not from either derivation ref, where none of the
   three exists.** All three paths are under `docs/evidence/documentation/`: batch 1's
   `readability-phase4-lane-d-batch1-2026-10-15.md` at `f380e92955be5f7896de6bf5a916466a31788277`
   (PR #774's branch), batch 2's `…-batch2-2026-10-15.md` at
   `5c462e1262cc205bca8d5a3194b50aff3452260a` (PR #778's branch) and batch 3's `…-batch3-2026-10-15.md`
   at `87c637dfb9dd646965d2dc43fff08887160c35f8` (PR #784's branch). Each record's eight `LD-n` rows
   carry a page path, and those eight paths are the list compared. This batch rebuilt the 590-path set
   at that base (the same replication as step 1, plus that revision's own `pending` array read with
   `--json`) and checked the three lists against it **boundary for boundary**: indices **444-451**,
   **452-459** and **460-467** are exactly batch 1's, batch 2's and batch 3's eight pages (**three
   comparisons, each true** — re-derived at this repair round, with zero paths differing either way).
   **Batch 4 is therefore indices 468-475 of that 590-path set — the next eight after the first 24,
   with nothing skipped and nothing re-read.**
5. **The same eight paths at this base.** The 590-set **is** a subset of the 593-set — re-deriving both
   pending sets with `check_index.py` at each ref against that ref's own committed index gives
   **586 + 4 = 590** at `e2a3e20b` and **588 + 5 = 593** at this base, with exactly **three paths
   entering and none leaving** (`docs/delivery-workflow.md`,
   `docs/evidence/documentation/readability-apr117-withdrawals-and-rerecord-2026-10-15.md`,
   `docs/roadmaps/OWNER-DECISIONS-2026-10-15.md` — **two new files, the APR-117 record added by PR
   #781 and the owner-decisions page added by PR #786, plus one acceptance regression**:
   `docs/delivery-workflow.md` drifting 24 lines past its recorded acceptance, row K-075,
   per step 3 above), and the index JSON
   is byte-identical at **all six refs read** — `e2a3e20b`, `f490c16f`, `988b5067` (main), `cac5c67d`,
   `d784c4dc` and this head — as blob `eeda4929cca872d626eb2ca6ca21583586335d11`: **88,316 bytes**,
   `sha256 b97e5fc9fbeb6b710d1ecbc449af80143156d9b24af512367a75b2c69295a0c3` over the tracked blob
   bytes, pure LF (**1,914 LF, 0 CR**). **The circulating `0b76b1a87db59019` / 90,230-byte pair is a
   CRLF re-encoding of the same file and is RETIRED here:** a PowerShell `Out-File` copy rewrites each
   of the 1,914 LF bytes as CRLF, so the arithmetic is exact — **88,316 + 1,914 = 90,230 bytes**, with
   `sha256 0b76b1a87db59019e735582db74a09f9d60a8f41a16f6d01c8028169ea1ee9a0`. **The real figure is
   88,316 bytes / `b97e5fc9fbeb6b71`**; 90,230 bytes names a different normalization of the same file,
   not a different file, and the file itself was never in doubt. Every one
   of the 24+8 pages batch 1 onward read survives in it: the eight of this batch sit at **indices
   470-477 of the 593**, i.e. **lane D positions 24-31** of 146 (1-based). The alternative literal
   reading — "the first 24 positions of the lane's quarter at this base, then the next 8" — would
   start at position 25 and **skip position 24** (`scenario-a-runbook-readability-2026-09-23.md`), a page
   no batch has read and that sits immediately after batch 3's last page in sorted order. **This
   batch reads it**; the reading that skips it is recorded here as the one *not* taken, with the
   reason.
6. **Membership checks.** Each of the eight pages was checked at the base against the committed
   index: **zero** carry an `acceptance-index.json` `reader_pages` row, and **zero** are touched by any
   `events` row (101 event rows at the base). All eight are in the
   `no_recorded_acceptance` bucket; none is in `provably_pending`, `small_drift` or `accepted`.

## 3. The roster, the concurrency, and the declared deviation

One reader (`readability-phase4-lane-d-batch4-implementer`, DeepSeek-4.1-Flash (deepseek-flash))
read all eight pages. **Declared deviation, carried by the lane since batch 1 and re-declared here:**
the AEGIS-APR-101 keeper-independence rule requires the keeper to differ from the page's author and
from the accepting reviewer. The **first** condition is satisfied — this batch wrote none of the
eight pages (each is a dated 2026-09-23 record whose last-touching commit is another author's; the
last-touching commits are named in section 5). The **second** is **not** claimed: this batch's
single agent is both the accepting reader and the writer of this record. **The rows are not this
batch's work**: this record authors no keeper row and edits no ledger section. The rows for these pages
are a separate eligible keeper's work under AEGIS-APR-117 — **and under the ledger's PARTIAL rule that
keeper records no row for any of the eight, because all eight are partial: the ledger's fixed-format
contract has "no partial-acceptance kind" (ledger L5133-5137 at the base; `main` L5584-5588) and
"a page a lane marked PARTIAL is never recorded as a full-page-acceptance" (L5149-5150 at the base;
`main` L5600-5601), so the eight get no acceptance row and stay pending.**
Section 10 carries the eight disposition lines verbatim as **evidence of the gaps, not as rows** — see
the explicit statement there. The authority question
stays with the merge holder; this batch records under AEGIS-APR-101 (recording only) and delivers
under AEGIS-APR-039.

## 4. Per-page dispositions — 0 full, 8 partial

Every page was read **whole, line by line, as prose**, at `f490c16f9ed23f3d489e42f7696323bffcce6fd3`.
The standard applied is stated in section 6; **every gap named there is reflected in the disposition
column here**, and no page carries a gap with a full disposition.

| # | Page | Read range | Lines | Disposition | Gaps (section 6) |
| --- | --- | --- | ---: | --- | --- |
| LD-25 | `docs/evidence/documentation/scenario-a-runbook-readability-2026-09-23.md` | L1-46 (whole) | 46 | **partial** | G-25.1 … G-25.4 |
| LD-26 | `docs/evidence/documentation/setup-routing-plan-readability-2026-09-23.md` | L1-67 (whole) | 67 | **partial** | G-26.1 … G-26.6 |
| LD-27 | `docs/evidence/documentation/skill-category-01-07-readability-2026-09-23.md` | L1-61 (whole) | 61 | **partial** | G-27.1 … G-27.3 |
| LD-28 | `docs/evidence/documentation/skill-category-map-readability-2026-09-23.md` | L1-52 (whole) | 52 | **partial** | G-28.1 … G-28.2 |
| LD-29 | `docs/evidence/documentation/skill-docs-eighth-20-readability-2026-09-23.md` | L1-64 (whole) | 64 | **partial** | G-29.1, G-29.4, G-29.5 |
| LD-30 | `docs/evidence/documentation/skill-docs-fifth-20-readability-2026-09-23.md` | L1-71 (whole) | 71 | **partial** | G-30.1, G-30.3, G-30.4 |
| LD-31 | `docs/evidence/documentation/skill-docs-final-screen-readability-2026-09-23.md` | L1-64 (whole) | 64 | **partial** | G-31.1, G-31.3 |
| LD-32 | `docs/evidence/documentation/skill-docs-first-20-readability-2026-09-23.md` | L1-63 (whole) | 63 | **partial** | G-32.1 … G-32.3 |

**Counts: 0 full / 8 partial. 26 named gaps, each with its page line numbers.** No page needed a fix,
so no page was edited: the no-rewrite discipline forbids edits to dated records, and every gap is
recorded here rather than repaired in place.

**Correction after the Stage D audit (2026-10-16) — the gap count was 28 and is now 30.** The audit's
read-not-grep check found this record's own `(b-plain)` term `isolated worktree` on two further pages
at their own lines — **G-26.6** (LD-26 L14) and **G-29.5** (LD-29 L21) — where the record had counted
the same term only on LD-27, LD-30, LD-31 and LD-32. Both gaps are added to the list below and to
their pages' rows above; the dispositions are **unchanged (0 full / 8 partial)**. The same repair
corrected three citations to the pages' verbatim wording (O-3's `185 skills valid`, the authority
sentence under "Explicitly not counted as gaps", and two `PR` tokens the committed text had mangled)
and re-issued the section 10 row-quote strings at the corrected ranges. No page, disposition, blob,
byte count, derivation figure or gate figure moved.

**Second correction, after the second Stage D audit (2026-10-16) — the gap count was 30 and is now 26.**
The re-audit measured every benchmark term over the **655 reader pages** at the base and applied the
owner's norm ruling: **an unglossed term that is a library-wide convention is not a per-page readability
defect — it is recorded as an observation about the library, with its count, not as a gap on the page.**
`manual-only` occurs on **206** of 655 pages and `frontmatter` on **53**, so the gaps that rest on them
are retired: **G-29.2** (`manual-only`), **G-31.2** (`MANUAL-ONLY`, the same convention — and its own
cite was wrong under the rule it applied: LD-31's first use is `manual-only` at **L36**, not
`MANUAL-ONLY` at L47) and **G-29.3** (`frontmatter`); the `frontmatter` clause of **G-31.3** and of
**G-32.2** is retired the same way, and both gaps remain on their `isolated worktree` clause.
**G-30.2** (`ASI07`) is retired as a false gap: LD-30 L47-48 gives the coded identifier its
plain-language name ("Insecure Inter-Agent Communication") at first use, which is what bullet (b) asks
for. **Both standards are stated, and the count under each: it was 30; on the record's own former
standard LD-30 would owe a frontmatter gap and the count would be 31; on the norm standard the three
pure-convention gaps fall away and the count is 27; with G-30.2 retired the count is 26.** The
**LD-30 / LD-29 asymmetry is resolved by applying one rule to both pages**: LD-29 L57-58 ("The four
frontmatter blocks …") and LD-30 L62-63 ("The four YAML (YAML Ain't Markup Language) frontmatter blocks
…") are the same sentence apart from the YAML expansion, both are the library convention, and **neither**
page owes a `frontmatter` gap — the former "does the page name the format?" test is withdrawn entirely
rather than applied unevenly. The four retired items are recorded as observations with their counts in
section 8 (O-6, O-7), and the chain is restated in section 9. `isolated worktree` (**26** of 655) stays
a per-page gap: it is the term this batch's own `(b-plain)` class measures, it is used unglossed on
**6 of these 8 pages**, and a page can remedy it in one clause — which a repository-wide convention
cannot, since a false `partial` keeps a page pending with no actionable remedy. The dispositions are
**unchanged (0 full / 8 partial)**, and no retained gap moved page or line.

## 5. Depth record and the mechanical pass

**Every line of every page was read as prose at the declared revision: 46 + 67 + 61 + 52 + 64 + 71 +
64 + 63 = 488 lines** (largest page 71 lines; mean 61). Each page fit a single read pass — **no
display elision occurred and no range was skipped**. The bytes were extracted with
`git cat-file blob f490c16f:<page>` and read with line numbers; the byte counts and blob IDs:

| # | Lines | Bytes | Blob ID at the acceptance revision | Last-touching commit (author) |
| --- | ---: | ---: | --- | --- |
| LD-25 | 46 | 2,564 | `78e865de87949b578ca5682d289cbbf709b4e194` | `93f61627` (Peter Nguyen) |
| LD-26 | 67 | 4,057 | `00cdb7dadcba4c56521390e25233b56307991b57` | `93f61627` (Peter Nguyen) |
| LD-27 | 61 | 3,692 | `acc445e3435875850538063b4a14ba2939219977` | `00504a3c` (Peter Nguyen) |
| LD-28 | 52 | 3,003 | `290c9bcee387521b13bbd6a7e49ed8ba4102a3d9` | `518a59d5` (Peter Nguyen) |
| LD-29 | 64 | 4,007 | `e2dafc86eb2088035142d6a05b9dd63db7b60aed` | `bf7a4b86` (Peter Nguyen) |
| LD-30 | 71 | 4,751 | `4e81cf73e17c38372497608bf46de0d2b8fec445` | `bf7a4b86` (Peter Nguyen) |
| LD-31 | 64 | 3,725 | `9bbfacc2034151028d6134ec8fb4ab6c7f5e00fc` | `bf7a4b86` (Peter Nguyen) |
| LD-32 | 63 | 3,915 | `145d7a112b6b04822be697f418293847ef15bd6f` | `bf7a4b86` (Peter Nguyen) |

**The mechanical pass** ran over the same exact-revision bytes. Per page it enumerated every
Markdown link (local and external), every in-page anchor target, every 40-character SHA, every 7-12
hex token in backticks, and coded identifiers by the pattern
`\b(?:[A-Z]{2,8}-\d{1,4}|D\d{2,3}|PR\s*#\s*\d{1,4}|#\d{3,}|K-\d{3}|L-\d{3}|T-\d{3}|AC\d{1,2})\b`.

| # | Local links resolved | External (not fetched) | Broken paths | Bad anchors | 40-hex SHAs (resolving) | 7-12 hex tokens (resolving) | Coded identifiers |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| LD-25 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| LD-26 | 4 | 0 | 0 | 0 | 0 | 0 | 1 (`PR #108`, expanded at L14) |
| LD-27 | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| LD-28 | 6 | 0 | 0 | 0 | 0 | 2 (`90f74c6`, `0c3d1c2` — both resolve) | 0 |
| LD-29 | 6 | 0 | 0 | 0 | 1 (resolves) | 0 | 0 |
| LD-30 | 7 | 5 | 0 | 0 | 1 (resolves) | 0 | 0 |
| LD-31 | 6 | 0 | 0 | 0 | 1 (resolves) | 0 | 0 |
| LD-32 | 4 | 0 | 0 | 0 | 1 (resolves) | 0 | 0 |

All 42 local links resolve at the base and no anchor is stale; the 5 external links (all on LD-30,
the OWASP, Agent2Agent, Model Context Protocol, W3C and HTML references) were **not fetched**,
matching the dated-note practice. The **four** 40-hex SHA occurrences in the table above (one each
on LD-29, LD-30, LD-31 and LD-32) are **three distinct values** — LD-29 and LD-31 both cite
`e900a0455c5ee3bb138b9292a6bcb71cbdfe7be8` — and each is the base or merge revision its note cites;
each resolves in the local object store at the base. The two 7-hex tokens on LD-28 are commit
abbreviations and both resolve. The named commands (`python -B
scripts/validate-skills.py`, `git diff --check`) exist at the named path or as git builtins
(checked with `git cat-file -e`).

## 6. The six acceptance bullets, and every gap with its page line

**The contract applied** is the ledger's "Acceptance for each page" (read at the base, ledger
L2841-2862): (a) open with what the page or component is for **and who should read it**; (b) define
an abbreviation or coded identifier at first use, and explain lifecycle/status codes in plain words
or link a glossary; (c) descriptive headings, short paragraphs, lists or tables, and at least one
concrete example, with what a function or command accepts, produces, changes and refuses explained
where safe use depends on it; (d) shipped behaviour separated from proposed or blocked behaviour;
(e) navigation links current and every referenced file or command existing; (f) a read-only review
by someone who did not write the page.

**The standard applied, stated so the dispositions can be audited.** A page is **partial** when this
record names at least one item in these classes, and **full** when it names none:

- **(b-def)** an abbreviation, coded identifier or status value is used without an on-page
  definition at or before its first use;
- **(b-plain)** a domain or repository shorthand term is used without the plain-words explanation
  bullet (b) asks for at first use;
- **(c-contract)** a named command or switch whose accept/change/refuse behaviour is load-bearing
  for safe use is left unexplained, or a verification claim names no revision a reader can check;
- **(d-unperformed)** the page states that a verification it presents was **not** performed;
- **(e-fail)** a link, anchor, referenced file, command or cited revision does not resolve — **none
  of the eight is in this class** (section 5);
- **(f-none)** no non-author read-only review is recorded — **none of the eight is in this class**;
- **the convention test (the owner's ruling of 2026-10-16), applied before any `(b-def)` or `(b-plain)`
  gap is recorded:** a term that is a **library-wide convention** is **not** a per-page readability
  defect. The term is measured first over the reader pages at the base (`manual-only` **206**/655,
  `frontmatter` **53**/655, `isolated worktree` **26**/655 — section 8, O-6) and, where the count shows
  a convention, it is recorded as an **observation about the library**, with its count, instead of as a
  gap on the page. **The cost is asymmetric:** a false `partial` keeps a page pending forever with no
  actionable remedy, and pending pages are exactly what the programme's exit condition counts.

**Explicitly not counted as gaps** (recorded so the classification is visible, not hidden): an
authority or scope boundary (the four skill-document pages' L7 sentence "This note does not grant
implementation or merge authority") — that is bullet (d) working correctly; the disclosure
"active-only time was not instrumented", which the repository's timing rule **requires** and no
acceptance bullet contradicts; and repository-wide work the page correctly says it does not close.
**Only the first of these three is listed per page where it appears** — section 6(d) cites the
authority sentence on all four skill-document pages. The timing disclosure and the repository-wide-sweep
class appear **only in this exclusion bullet and are not enumerated per page**; this sentence is
corrected so that a reader does not take it as a per-page listing for them.

**(a) Purpose and audience up front — 8 of 8 name the purpose, 0 of 8 name the reader.** Every page
opens by saying what it covers (LD-25 L1-18, LD-26 L1-21, LD-27 L1-14, LD-28 L1-13, LD-29…LD-32
L1-7 "This is dated delivery evidence…"). **None names an intended reader of the note itself**: the
only reader words are about the reviewed artifacts (LD-25 L16 "a maintainer arriving without the
earlier project conversation"; LD-26 L27-29 "tells maintainers … and points product users to the
manual setup skill"). That is the one clause of bullet (a) left unmet on every page, and **G-25.1 …
G-32.1** below.

**(b) First-use definitions, per page.** LD-25: clean (`ID` L7 and `PDT` L8 glossed at first
use) but jargon unmet (G-25.2). LD-26: **`Laya` and `Decider` (L31), `OpenJev` (L31-32) and the
`unselected` status value (L36) are used with no on-page definition** (G-26.2, G-26.3); `UTC` (L8)
and `PR` (L14) are correctly defined, but `isolated worktree` (L14) is used without plain words
(G-26.6). LD-27: clean (`PR` L7, `P0/P1/P2` L28-30, `IDs` L34,
`UTC` L48). LD-28: clean (`AI` L6, `P0/P1` L16-17, `UTC` L37, `ID` L40). LD-29:
`isolated worktree` (L21) is used without plain words (G-29.5); `UTC` is defined at L53; and
`manual-only` (L18) and `frontmatter` (L57-58) are **library conventions**, measured at 206/655 and
53/655 pages and recorded as observations with their counts (section 8, O-6) rather than as gaps. LD-30:
`ASI07` (L48) **carries its plain-language name at first use** — "Agentic Top 10's `ASI07 Insecure
Inter-Agent Communication category`" (L47-48) — so the former G-30.2 is withdrawn as a false gap and
the coded identifier is correctly defined under bullet (b) (section 8, O-7); the `frontmatter` at L62-63
is the library convention, recorded as an observation, and is **not** a gap, which is the same treatment
LD-29's identical sentence gets; `OWASP` L47-48, `W3C` L51, `HTML` L52, `YAML` L62, `IDs` L38 and
`UTC` L57 are correctly defined. LD-31: `MANUAL-ONLY` (L47) is the same library convention as `manual-only`, whose first use on this
page is at **L36** — recorded as an observation, not a gap (section 8, O-6); `frontmatter` (L48-49) is
the same convention, also an observation; `TDD` L9/L33, `TALI` L34,
`SAST`/`SARIF`/`CVE`/`TP`/`FP` L41-43 and `DCO` L63 are defined.
LD-32: the reading key (L9-16) covers WCAG, E2E, both `CI` senses, a11y, EN 301 549, ADA, ARIA,
SR, AT, VPAT and YAML; `PR` L28, `MDE` L35 and `SRM` L36 are defined; `frontmatter` (L14-15, and again
L44 and L56) is the library convention — the reading key at L14-15 in fact defines YAML as "the text
format used for skill frontmatter" — recorded as an observation, not a gap (section 8, O-6).

**(c) Descriptive headings, lists or tables, and concrete examples — satisfied on all eight.** Every
page uses headed sections and either a table or a list; each carries concrete worked content (LD-25
L33-37's 113 tests / nine versions / 185 skills; LD-26 L34-47's package-2 and package-3 findings;
LD-27 L34-37's 260 unchanged rows; LD-28 L30-36's 40 unchanged rows and commit names; LD-29 L30-47's
per-skill corrections; LD-30 L29-45's per-skill corrections; LD-31 L32-52's reader path and
corrections; LD-32 L35-46's reading key and corrections). **Two contract items were left unmet:**
LD-25 names `Invoke-ScenarioAEvidence.ps1` / `Test-ScenarioAEvidence.ps1` (L31-32) and the
`-KeepEvidence` switch (L34) without what they accept, change or refuse (G-25.3); LD-28's
verification claim compares against "the worktree base commit" (L31) without naming the revision, so
a reader cannot reproduce or check it (G-28.2).

**(d) Shipped behaviour separated from proposed or blocked behaviour — satisfied on all eight.**
Each page states what it did not do and denies authority it does not hold: LD-25 "does not change
runtime behavior or claim a fresh agent conversation has passed … does not grant implementation,
provider, or deployment authority" (L26-27); LD-26 "does not claim review of every plan-adjacent
document or skill" (L57-58); LD-27 "No skill file, runtime, permission, provider, deployment or
approval changed" (L36-37); LD-28 "does not install a skill, prove host behavior, change
authorization or mark either 20-item category fully delivered" (L22-23); LD-29-LD-32 "This note does
not grant implementation or merge authority" (L7) and "No private input, provider, credential, or
real host was accessed" (LD-29 L49, LD-30 L53, LD-32 L48).

**(e) Navigation links current and every referenced file or command existing.** Section 5's
mechanical pass: **all 42 local links resolve, zero broken paths, zero bad anchors**, every cited
40-hex SHA and 7-12 hex token resolves, and the named commands exist at the base. The five external
links were not fetched.

**(f) The non-author read-only review — recorded on all eight.** LD-25 L39-42; LD-26 L59-63;
LD-27 L48-56 (three rounds); LD-28 L37-43 (two rounds); LD-29 L61-62; LD-30 L67-69; LD-31 L62-63;
LD-32 L60-61. **On the pages whose review was narrower than the batch's own verification, the page
says so and this record counts it** (G-25.4 reviewer did not rerun the 113-test suite; G-26.5
reviewer did not re-fetch the live issue #101). **On three of the four skill-document pages the page
records that no live model evaluation was run** (LD-29 L60-61, LD-30 L65-66, LD-32 L59-60), which
this record also counts (G-29.4, G-30.4, G-32.3); **LD-31 records no such sentence anywhere** and so
carries no `(d-unperformed)` gap — the count of five pages is unchanged, the word "four" was wrong. **Closed, not counted:** LD-27 L48-51 (a first-use
gap the reviewer found and the batch corrected), LD-28 L40-41 (missing ID/AI/P0/P1/UTC explanations,
corrected) and LD-30 L68-69 (the note's own abbreviations expanded and its checks rerun) are
histories of corrections made **before** the bound revision; this batch verified the corrected text
directly (section 6(b)) rather than trusting the sentence.

### The gap list, one line per gap

- **G-25.1** (a) LD-25 L3-8, L12-18: purpose stated, intended reader of the note never named.
- **G-25.2** (b-plain) LD-25 L18 "behavioral acceptance gate", L25 "defect matrix" and "fresh-session gate" (again L41), L33 "negative suite": used without plain words.
- **G-25.3** (c-contract) LD-25 L31-32, L34: the two harness scripts and the `-KeepEvidence` switch are named without their accept/change/refuse contract.
- **G-25.4** (d-unperformed) LD-25 L41-42: "The reviewer did not rerun the 113-test suite."
- **G-26.1** (a) LD-26 L3-8, L10-21: purpose stated, intended reader never named.
- **G-26.2** (b-def) LD-26 L31-32: `Laya`, `Decider` and `OpenJev` are bare names with no on-page definition.
- **G-26.3** (b-def) LD-26 L36: the `unselected` status value is used without plain-words explanation.
- **G-26.4** (b-plain) LD-26 L45-46: "no-silent-online fallback boundary" (the phrase runs across the two lines) unglossed.
- **G-26.5** (d-unperformed) LD-26 L62-63: the reviewer "did not re-fetch the live issue" in its sandbox.
- **G-26.6** (b-plain) LD-26 L14: "isolated worktree" used without plain words.
- **G-27.1** (a) LD-27 L1-14: purpose stated, intended reader never named.
- **G-27.2** (b-plain) LD-27 L25-26: "the original conversion checklist" is named with no path or location, so it cannot be found.
- **G-27.3** (b-plain) LD-27 L7: "isolated worktree" used without plain words.
- **G-28.1** (a) LD-28 L1-13: purpose stated, intended reader never named.
- **G-28.2** (c-contract) LD-28 L31-32: the 40-row comparison names only "the worktree base commit", no revision, so the check is not reproducible from the page.
- **G-29.1** (a) LD-29 L3-7: purpose stated, intended reader never named.
- **G-29.4** (d-unperformed) LD-29 L60-61: "no live model evaluation was run for these wording changes."
- **G-29.5** (b-plain) LD-29 L21: "isolated worktree" used without plain words.
- **G-30.1** (a) LD-30 L3-7: purpose stated, intended reader never named.
- **G-30.3** (b-plain) LD-30 L20: "isolated worktree" used without plain words.
- **G-30.4** (d-unperformed) LD-30 L65-66: "no live model evaluation was run for these wording changes."
- **G-31.1** (a) LD-31 L3-7: purpose stated, intended reader never named.
- **G-31.3** (b-plain) LD-31 L21: "isolated worktree" used without plain words (the term is wholly on L21; the L48-49 `frontmatter` clause is retired to an observation, section 8 O-6).
- **G-32.1** (a) LD-32 L3-7: purpose stated, intended reader never named.
- **G-32.2** (b-plain) LD-32 L27: "isolated worktree" used without plain words (the L14-15 `frontmatter` clause is retired to an observation, section 8 O-6).
- **G-32.3** (d-unperformed) LD-32 L59-60: "no live model evaluation was run for this wording-only correction."

**Numbering, stated so the list can be counted:** the labels **G-29.2**, **G-29.3**, **G-30.2** and
**G-31.2** are **retired, not renumbered** — the retained gaps keep the labels and page lines the first
audit verified (in particular the two it added, **G-26.6** and **G-29.5**). Each retirement is
explained in section 4's second correction and in section 8 (O-6, O-7). **26 gaps remain**, one line
each: LD-25 four, LD-26 six, LD-27 three, LD-28 two, LD-29 three, LD-30 three, LD-31 two, LD-32 three.

## 7. Purpose and normal use restated from each page alone

- **LD-25** — *for:* recording the 2026-09-23 readability batch on the Scenario A acceptance
  runbook and its `docs/README.md` entry, with the 113-test and nine-version receipts. *Normal use:*
  read the current-reading banner for where the live runbook is; the body is the dated record.
- **LD-26** — *for:* the issue #101 setup-routing-plan readability batch: which plan sections were
  reviewed, what was labelled historical, and the package-2/3 rechecks. *Normal use:* read it as the
  dated evidence behind the plan's current package wording.
- **LD-27** — *for:* the seven original skill-category pages (01-07) and the correction that
  presented their candidate tables as historical rather than shipped. *Normal use:* dated evidence
  for that correction; the catalog is the live status reference it points to.
- **LD-28** — *for:* the two 20-row category maps (AI-era SDLC/agent ops and AI software
  engineering) and their historical-role clarification. *Normal use:* dated evidence; the catalog
  carries current availability.
- **LD-29** — *for:* the eighth 20-skill readability screen and the four skill files it corrected.
  *Normal use:* dated delivery evidence; the ledger and forecast carry current totals.
- **LD-30** — *for:* the fifth 20-skill readability screen and the four skill files it corrected,
  with the external terminology sources it checked against. *Normal use:* as above.
- **LD-31** — *for:* the final skill-documentation screen (26 entrypoints after
  `soc2-trust-criteria-mapper`) and the three skill files it corrected. *Normal use:* as above.
- **LD-32** — *for:* the first 20-skill screen and its reading key, plus the two skill files it
  corrected. *Normal use:* as above.

## 8. Observations — resolved against the repository, not the pages' prose

Row shape: `stale:` the item as it bears on this batch; `new:` the disposition this batch
records; `source:` the artifact that settles it. **Every row that names a page defect is
already reflected in that page's partial disposition in section 4** — none of these observations
carries a full disposition alongside it.

| # | stale | new | source |
| --- | --- | --- | --- |
| O-1 | The derivation base moved: `origin/main` gained three pending paths between `e2a3e20b` and `f490c16f` (two new files from two different merges — PR #781's own withdrawal-and-rerecord record and PR #786's `docs/roadmaps/OWNER-DECISIONS-2026-10-15.md` — plus `docs/delivery-workflow.md` by 24-line drift out of its recorded acceptance, row K-075; section 2 step 3), so lane D's quarter start moved 444 to 447 and two pages batches 1-2 read (`full-page-readability-batch-after-233`, `…-234`) now fall inside **lane C's** quarter at this base. | **unchanged — reported, not decided.** This batch touches neither page; the overlap is a cross-lane boundary question for the coordinator (a lane D batch-1/2 page and a lane C quarter can now name the same path). | `check_index.py --json` at both bases; the 590-set/593-set set-difference; `git ls-tree` counts. |
| O-2 | Batch 4's window under the moved boundary: the same eight pages are lane D positions **24-31** at this base, not 25-32; position 24 (`scenario-a-runbook-readability-2026-09-23.md`) was unread by batches 1-3 and would be skipped by a literal re-indexing. | **unchanged — the eight were selected by the lane's own sequence (indices 468-475 of the 590-set, verified boundary-for-boundary against batches 1-3), so nothing is skipped and nothing is re-read.** | `check_index.py --json` at `e2a3e20b` with that revision's index (the 590-set) and at the base (the 593-set); the three boundary comparisons. |
| O-3 | The 2026-09-23 pages' historical validation figures ("185 skills valid" on LD-25 L36 and LD-28 L33; "185 valid skills" on LD-26 L53, LD-27 L44, LD-29 L55-56, LD-30 L60-61, LD-31 L56 and LD-32 L54; link counts 23/25/4/11/9/6 on LD-26 to LD-32) describe those batches at their own checkpoints. **The six link-count values are stated on six of those seven pages, in page order, and LD-28 states no link count at all** — so read them 23 (LD-26 L54), 25 (LD-27 L45), 4 (LD-29 L56), 11 (LD-30 L61), 9 (LD-31 L57), 6 (LD-32 L55), and never shifted one page earlier. | **unchanged — historical sentences about their own batches, not restated as today's.** | The pages' own dates and base commits; the mechanical pass's per-page link counts (section 5). |
| O-4 | LD-28 L8 cites the commits `90f74c63a4d5e4ea9d4d7d59c871c07fbab95dd5` and `0c3d1c2763e1134c8355cd64242cd606befd8f04` (abbreviated on the page as `90f74c6` and `0c3d1c2`) as the two category maps' introduction commits; both resolve at the base. | **unchanged — resolved, no repair.** | `git cat-file -t 90f74c63a4d5e4ea9d4d7d59c871c07fbab95dd5` and `git cat-file -t 0c3d1c2763e1134c8355cd64242cd606befd8f04` at the base (both print `commit`). |
| O-5 | The six `cannot_decide` lost-commit pages (LD: `.claude/skills/cloud-security-baseline-reviewer/references/aws-baseline.md`, `…/azure-baseline.md`, `…/gcp-baseline.md`, `…/supabase-baseline.md`, `…/vercel-baseline.md` and `.claude/skills/database-backup-verifier/SKILL.md`) are in the instrument's `cannot_decide` bucket, not in the 593-path pending set, and therefore in **no lane**. | **unchanged — excluded, and stated.** This batch picked up none of them; they are also outside lane D's quarter at the base (checked: the intersection of the six with lane D's 146 paths is empty). | `check_index.py --json` `undecided` array at the base; the intersection check. |
| O-6 | Four gaps in this record's own `(b-def)`/`(b-plain)` classes rested on terms that are **library-wide conventions**, not page defects: `manual-only` / `MANUAL-ONLY` and `frontmatter`. Measured case-insensitively over the **655 reader pages** at the base they occur on **206** and **53** pages. | **unchanged as a library fact — recorded here as observations with their counts, and the gaps that rested on them are retired** (section 4's second correction; the count 30 → 26). | The eleven-term count over the 655 reader pages at `f490c16f`, per page, case-insensitive, over the page's own `git cat-file blob` bytes — the table below. |
| O-7 | LD-30 L47-48 gives the coded identifier `ASI07` its **plain-language name at first use** ("Agentic Top 10's `ASI07 Insecure Inter-Agent Communication category`"), so the former **G-30.2** recorded a page as defective for doing what bullet (b) asks. | **unchanged — G-30.2 is withdrawn as a false gap; the 30 → 26 correction includes it.** | The page's own L47-48 bytes at the base. |

**The eleven benchmark terms measured** (pages containing the term, case-insensitively, over the 655
reader pages at the base): `UTC` **222**, `manual-only` **206**, `verdict` **165**, `screen` **148**,
`PR #` **141**, `AEGIS-APR-` **88**, `receipt` **74**, `DCO` **71**, `frontmatter` **53**,
`authz` **52**, `isolated worktree` **26**. The convention test in section 6 is applied to the terms
this record had itself flagged; the seven more frequent terms are not gaps on these pages either, which
is the same standard applied to all eleven rather than to two. **Where the line is drawn is a judgement,
stated as one:** a term the repository uses as the naming convention for its own artifacts
(`manual-only` 206/655, `frontmatter` 53/655) is a library convention, while `isolated worktree`
(26/655, and 6 of these 8 pages) is a domain term a page can gloss in one clause — and both audits and
the standing brief treat it as a real per-page gap. The row above is the measurement; the
classification is this record's, and a later reader can re-draw it from the same numbers.
**Two reservations are recorded here so the coordinator can weigh them: (1) the criterion has no
numeric threshold, so it is not falsifiable from the numbers alone — the counts are evidence for the
judgement, not the judgement; and (2) keeping `isolated worktree` as a gap is load-bearing for this
record's own subordinate claim that "the fewest is two" (LD-28, LD-31 and LD-32), because retiring the
term would leave LD-31 with exactly one gap (G-31.1). Neither reservation changes an outcome: no page
would flip to full and no page would leave the pending set either way, so no acceptance outcome
depends on where the line is drawn.**

## 9. Count honesty

- **0 full / 8 partial.** That is the count this batch actually found; it is stated plainly rather
  than rounded toward a better-looking figure. The gaps are named per page with line numbers in
  section 6, and no page carries a gap with a full disposition.
- **The gap count was corrected after audit: 28 → 30.** The count first published at this record's
  audited head was **28**; the Stage D audit of 2026-10-16 found the two missing (b-plain)
  `isolated worktree` gaps (**G-26.6**, **G-29.5**), so the count in this record is **30**. Both
  figures are stated rather than the old one being quietly overwritten, and the two gaps carry
  their page lines in section 6.
- **The gap count was corrected again after the second audit: 30 → 26.** The second Stage D audit of
  2026-10-16 measured all eleven benchmark terms over the 655 reader pages and applied the owner's norm
  ruling. Four gaps are retired and the whole chain is stated rather than the old figure being quietly
  overwritten: **30** was the audited figure; on the record's own former standard LD-30 would owe a
  frontmatter gap and the figure would be **31**; on the norm standard the three pure-convention gaps
  fall away and the figure is **27**; with the false `ASI07` gap withdrawn the figure is **26**.
  **Retired:** **G-29.2** and **G-31.2** (`manual-only` / `MANUAL-ONLY`, 206 of 655 pages),
  **G-29.3** and the `frontmatter` clauses of G-31.3 and G-32.2 (53 of 655), and **G-30.2**
  (`ASI07`, given its plain-language name at LD-30 L47-48). **Kept:** every other gap, including the
  two the first audit added (**G-26.6**, **G-29.5**) and all six `isolated worktree` gaps (26 of
  655). The retired items are recorded as observations with their counts (section 8, O-6 and O-7), and
  the labels are retired rather than renumbered. **0 full / 8 partial is unchanged**, and every page
  still carries named gaps — the fewest is **two** (LD-28, LD-31 and LD-32), the most is **six**
  (LD-26), 26 in all.
- **This batch publishes no readability count of its own** (ledger L19-31, D84) and cites the
  instrument for every figure.
- **The instrument classifies the page tree at `--ref`** and reads recorded acceptances from the
  **committed index JSON**. **The two sides move on different clocks, and this record states which is
  which:** the page-count side is **immediate** — the page is in the tree at `--ref`, so the
  instrument's `classify_tree` counts it as a reader page, as `no_recorded_acceptance` and in the
  official pending count the moment the record lands — while **only the acceptance-row side awaits a
  rebuild**, because a row is read from the committed index JSON. **Codex finding #7, the P2 "Distinguish the immediate count change from a rebuild" (review comment `4290117780`, written against `cac5c67d`; the **seventh** of the eight findings reported on this change in the API's own `pulls/791/comments` array order — ascending comment id, which is creation order — and the one the second Stage D verdict's F1–F7 triage omitted), is SUSTAINED and corrected here.** The published head expectation
  after this record lands is **656 / 56 / 5 / 589 / 0 / 0 / 6 / 600** — the base's
  655 / 56 / 5 / 588 / 0 / 0 / 6 / 599 with **+1 reader page, +1 `no_recorded_acceptance` and +1
  official pending count**, all three attributed to this record. Those three effects are **already
  measured at this record's head, not predicted**; **no post-rebuild count is predicted.**
  `build_index.py --write` is not run in this batch: a rebuild adds JSON under `tools/`, which is not
  Markdown and would break this change's `docs-only` tier; the rebuild is the standing AEGIS-APR-115
  pull request's own scope (D73 row 8), and its effect when it runs is the **acceptance-row** side only.

## 10. The eight disposition lines, verbatim (evidence, NOT rows)

**No keeper may author an acceptance row for any of these eight pages, and not one of them leaves the
official pending count.** The ledger that governs the AEGIS-APR-117 keeper is the same file this record
cites, and it says the opposite of a row offer: the ledger's fixed-format contract "names four event
kinds — `full-page-acceptance`, `targeted-review`, `withdrawal` and `lost-commit` — and has **no
partial-acceptance kind**" (ledger L5133-5137 at the base; `main` L5584-5588), and the rule the ledger
made explicit after the last keeper draft is "**a page a lane marked PARTIAL is never recorded as a
full-page-acceptance**" (ledger L5149-5150 at the base; `main` L5600-5601). **All eight pages in this
batch are marked partial** (section 4), so under that
rule they get **no acceptance row** and **stay pending**. A keeper that read the lines below as a row
offer would record eight full-page acceptances and **drop eight pages out of the official pending
count**; the builder takes `event_kind` from the row, so nothing downstream would catch it. **This
batch authors no rows, claims no row IDs, and offers none.**

The lines below are **evidence, not rows**: each names its page, the full 40-character revision the page
was read at, its partial disposition and its gaps, so that a later reader can see what the reading
covered and what it did not. They are kept because they are the evidentiary record of the gaps — **they
are not a row template and nothing here may be pasted into the ledger's keeper block.** Every line
appears in this file byte-for-byte, and **every line states its partial disposition**, so that no reader
can mistake one for a full-page-acceptance.

```text
PAGE LD-25 partial, no acceptance row, stays pending; gaps G-25.1..G-25.4 (section 6); read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3: docs/evidence/documentation/scenario-a-runbook-readability-2026-09-23.md
PAGE LD-26 partial, no acceptance row, stays pending; gaps G-26.1..G-26.6 (section 6); read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3: docs/evidence/documentation/setup-routing-plan-readability-2026-09-23.md
PAGE LD-27 partial, no acceptance row, stays pending; gaps G-27.1..G-27.3 (section 6); read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3: docs/evidence/documentation/skill-category-01-07-readability-2026-09-23.md
PAGE LD-28 partial, no acceptance row, stays pending; gaps G-28.1..G-28.2 (section 6); read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3: docs/evidence/documentation/skill-category-map-readability-2026-09-23.md
PAGE LD-29 partial, no acceptance row, stays pending; gaps G-29.1, G-29.4, G-29.5 (section 6); read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3: docs/evidence/documentation/skill-docs-eighth-20-readability-2026-09-23.md
PAGE LD-30 partial, no acceptance row, stays pending; gaps G-30.1, G-30.3, G-30.4 (section 6); read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3: docs/evidence/documentation/skill-docs-fifth-20-readability-2026-09-23.md
PAGE LD-31 partial, no acceptance row, stays pending; gaps G-31.1, G-31.3 (section 6); read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3: docs/evidence/documentation/skill-docs-final-screen-readability-2026-09-23.md
PAGE LD-32 partial, no acceptance row, stays pending; gaps G-32.1..G-32.3 (section 6); read whole at f490c16f9ed23f3d489e42f7696323bffcce6fd3: docs/evidence/documentation/skill-docs-first-20-readability-2026-09-23.md
```

## 11. Verification commands (run at the head; outputs in the pull-request body)

`check_index.py --json --ref <head>` and `check_index.py --ref <head> --quiet` (the head counts),
`build_index.py --ref <head> --report` (no row change versus the base), the changed-path Markdown
link check, `scripts/validate-skills.py`, `scripts/tests/test_validator.py`,
`git diff --check`, the numstat check (the Stage C commit is insert-only against the derivation
base, 455 added / 0 deleted; the first Stage D repair commit adds 45 and deletes 19 of those lines;
the second adds 167 and deletes 56; the third adds 73 and deletes 20; the fourth adds 91 and deletes
47; **the fifth, `61371fa5`, adds 4 and deletes 4** — every figure counted over every `-` line
excluding the `---` headers, so **none of the five repairs is insert-only**, while the base-relative
figure is **752 added / 0 deleted** because the record file is new at the base — the file has
grown, and this record states the current figure rather than leaving the first repair's 481 standing.
**The third repair's 20 deleted lines sit at these sites (old-side line numbers at `c4a55185`):**
L97-98 (the false PR #781 provenance sentence), L115-119 (the second provenance clause and the
index-figure paragraph), L430 (O-1's provenance parenthetical), L477-478 and L480-483 (the "changes
nothing until a rebuild" sentence and its count sentences), L524-527 (this numstat sentence itself)
and L584-585 (the timing section's "two repair commits"); **none of its 20 deleted lines begins with
a second `-`**.
**The fourth repair's 47 deleted lines sit at these sites (old-side line numbers at `5e336ea2`):**
L31-40 (the whole bound-field-digest front-matter item, re-wrapped to the record's 100-column prose
style: the named snapshot that makes `1fcd0143e13198a3` reproducible, the new `4cc13e7e5dfb723a` entry,
and the same-lengths hazard), L111-126 (the whole of section 2 step 3, likewise re-wrapped: the false
attribution at site 1 and "the third is not new" clause around it), L139-140 (the step-5 clause, site
2), L461 (observation O-1's provenance parenthetical, site 3), L519-522 (the Codex finding's ordinal),
L569-580 (this numstat paragraph itself) and L637-638 (the timing section's repair count); **the
re-wrapped lines whose sentences are unchanged are deletions of line breaks, not of content, and none
of them begins with a second `-`** either, so the two-dash trap did not fire in that round.
**The fifth repair (`61371fa5`) rewrote section 12 item 3 in place — four lines added and four
deleted, old-side line numbers at `d1f02a0a`: L636-639** — replacing the "no snapshot survives …
unverified here" sentence with the measured sibling digests and the three surviving snapshots; the
record stayed at **689 lines** across that commit. **Five repair commits are therefore counted here,
and the branch carries a sixth after this round's commit** — that round's own figures are stated in the
pull-request body's head-pinned gate table and in the Stage C handoff, because a commit cannot measure
the bytes it is committing),
`scripts/check_dco.py --range
origin/main..HEAD`, and `python -P scripts/ci/check_pr_body_skills.py --body-file <f>`.

## 12. What this batch did not do

It **authored no keeper row and edited no ledger section** (AEGIS-APR-101's corrected posture; the
rows are a separate eligible keeper's work under AEGIS-APR-117) — and it states plainly that under the
ledger's PARTIAL rule (L5133-5137, "no partial-acceptance kind"; L5149-5150 — **base-scoped**: at `main`
`71795e6e` those passages are L5584-5588 and L5600-5601) the eight partial pages get
**no acceptance row** and stay **pending**, so no keeper authors one from this evidence; edited none of
the eight read pages
(no-rewrite discipline); rewrote no dated snapshot; bound no acceptance row to this batch's own
unmerged head; ran no `build_index.py --write` and rebuilt no `tools/` artifact; touched no page
outside lane D's quarter; touched no other lane's branch, PR or clone; picked up none of the six
`cannot_decide` lost-commit pages; skipped no page in the lane's sequence (the position-24 page a
literal re-indexing would have skipped is read here); and claims no authority beyond recording under
AEGIS-APR-101 and the standing backlog delivery grant AEGIS-APR-039. The batching procedure "does
not grant provider, private-input, real-host or deployment authority" (ledger L3018-3020).

### What the repair rounds did not verify

**The previous round's list of things it did not verify was published only in a message to the
coordinator — not in the record and not in the body, at this head or the previous one** (counted at the
previous head `5e336ea2`, in the 59,255-byte record and the posted body *as they stood there* — not in
this revision, which necessarily contains these words in this very item: "not verified", "unverified"
and "did not verify" each occur **0** times in that record and **0** times in that body, and "carried
over" 0 in both). An unpublished disclosure is not auditable, so this round carries its limits
here, in the record, and every future round does the same.

1. **The act of reading all 488 lines as prose** — a claim about the author's process. What is verified
   is each page's size, that the eight read ranges are whole and contiguous, and that all 488 lines are
   accounted for.
2. **The batches 1-3 boundary comparison** — that sorted indices 444-451, 452-459 and 460-467 of the
   590-path set are exactly lane D batches 1, 2 and 3's pages. **An earlier round of this item said
   those records "are in neither ref, so their published page lists cannot be read"; that conclusion
   was wrong, and section 2 step 4 now carries the corrected account.** They are in neither derivation
   ref, but each is retrievable at its own batch's pull-request branch head — `f380e929…`,
   `5c462e12…` and `87c637df…`, with their paths named in section 2 step 4 — and **the three
   comparisons were re-derived from exactly those files at this repair round: all three true, zero
   paths differing either way.** The position arithmetic and the set relations are verified
   independently by the instrument runs.
3. **The historical snapshot windows** — the batch did not read the body edit histories of the five
   pull requests this item names, so no digest movement is traced edit by edit. **Re-measured from the
   live bodies by API: four of the five still yield the digests recorded for them — PR #783 `3913683c686e6e71`
   (payload lengths 2,701 / 3,771 / 40), PR #792 `88300e711714200a` (1,565 / 3,824 / 40), PR #770 `75a3627ae62d0cb4` (1,989 / 4,567 / 165) and PR #766 `76e465ae8f2ba6e9` (1,468 / 111,039 / 45) — and only PR #774 has moved: its live body now yields `755e1656024f75f9` at payload lengths 2,543 / 5,792 / 738, its last body edit dated **2026-10-16T04:51:25Z**. `54d5e1e9a06ccbbc` at `d784c4dc` is reproduced, not carried: three snapshots of that body revision survive in this workspace and each re-derives it at payload lengths 1,175 / 5,197 / 567 — `_sc791-repair-20261015/_cal_791.txt` and `_pr791_body_live.txt` (both 22,605 bytes, content hash `sha256 7425ae896da0b8550b0f2930543106c27029c839f3bed23a2e9031e63e8ec33a`) and `_r791_live_791_body.md` (22,602 bytes, `sha256 a99e791956bba3b8666065372253aa2a9fd06c1523e28cf4aea8445739f13c4a`) — workspace files, not git objects, so those two values are content hashes of the file bytes and not git object ids.**

   **All five snapshots named in this record are untracked workspace files outside any repository
   — `_pr791_body_live.txt` and `_r791_live_791_body.md` sit at the workspace root, the others in
   their named directories — so they are not available to a clean checkout. What they establish is
   reproducibility of these values from these bytes on this host, not clean-checkout reproducibility.
   Tracking them is not done here (they are pull-request bodies, not repository content), so the
   durability gap is stated rather than closed.**
4. **Codex's security review** — its embedded state is
   `security_review {status: null, commit_sha: null, has_any_findings: null, has_unresolved_findings: null}`,
   so no security finding is retrievable either way. **That is unavailability, not a clean result.**

## 13. Skills used (this batch, Stage C)

`change-classification-gate` (the skill that classifies a change and fixes its validation tier)
— classified the change `docs-only` (one new evidence record, Markdown only) before writing.
`acceptance-criteria-reviewer` (the skill that reviews existing acceptance criteria for
testability and completeness) — the ledger's six acceptance bullets applied to each of the eight
pages, each bullet addressed with line cites rather than asserted; every gap named, never smoothed
over. `source-of-truth-reconciler` (the skill that resolves a claim against the artifact that
owns it rather than against prose) — the observations resolved against the repository (the moved
quarter boundary, the position-24 skip, the historical validation figures, the two category-map
commit abbreviations). `scoped-approval-register` (the skill that establishes which recorded
approval covers an action) — established this batch records under AEGIS-APR-101 and delivers under
AEGIS-APR-039, consumes, extends and requests no grant, and that the rows are the separate keeper's
AEGIS-APR-117 scope. `docs-retention-index` (the skill that decides whether a new page owes a
retention entry) — consulted; no retention entry or frontmatter mechanism exists for
`docs/evidence/documentation/` (zero files there carry `retention:` frontmatter at the base), so the
new page follows the established shape and creates no retention row; recorded as
checked-and-not-applicable. `skill-usage-ledger` (the skill that requires the six-field
skills-used record where a reader can see it) — the block below, bound to the skills-manifest hashes
at the base.

```text
skill@08d91a834460beebc9c66fa896b8b422f064bf1d7524f6e5b1512cda3afdc996 / reason: classify before writing, the class decides the tier and review path / applied: classified docs-only before any write / result: docs-only tier asserted in the PR body with the file set / incomplete: None / by: readability-phase4-lane-d-batch4-implementer (Stage C; DeepSeek-4.1-Flash (deepseek-flash))
skill@c6e5d5649bf89658036cf38abba9c626701220e7b00831c2d843ceff94d81021 / reason: the acceptance contract's six bullets are criteria and were checked one by one / applied: each bullet per page with line cites in section 6, every gap named with its page line / result: 0 full, 8 partial, 26 named gaps (28 → 30 → 26: two missing isolated worktree gaps added, then four convention/false gaps retired; sections 4 and 9) / incomplete: None / by: readability-phase4-lane-d-batch4-implementer (Stage C; DeepSeek-4.1-Flash (deepseek-flash))
skill@b5fd9feda97235430259913aedd33447ab06e1c0ded281e9e131fa6bf9b78be2 / reason: the moved quarter boundary and the items not resolvable from prose needed the artifacts that own them / applied: observations O-1..O-5 sourced to instrument runs and git objects / result: all five dispositioned, none repaired in place / incomplete: None / by: readability-phase4-lane-d-batch4-implementer (Stage C; DeepSeek-4.1-Flash (deepseek-flash))
skill@a74d2a22579cf93f737725aa0c54197b5d496a9f33a291a93c2cf2073cd7d076 / reason: recording requires knowing which grant covers what / applied: read AEGIS-APR-039, -101, -115, -117 and -118 at the base / result: recording-only under APR-101; no grant consumed, extended or requested / incomplete: None / by: readability-phase4-lane-d-batch4-implementer (Stage C; DeepSeek-4.1-Flash (deepseek-flash))
skill@141b7036469f9f99ef6b8e152299619a6d0ab572656a5ba307062551d311d8a5 / reason: a new page may owe a retention entry / applied: checked for a retention registry and per-doc frontmatter practice / result: none exists for this directory; no retention change needed, recorded not skipped / incomplete: None / by: readability-phase4-lane-d-batch4-implementer (Stage C; DeepSeek-4.1-Flash (deepseek-flash))
skill@6a27b5c8e690b605d7dca4b0e4c2ff1d67dfa6ac6c18469d5657b4ff093339a4 / reason: the repository requires the skills-used record where a reader can see it / applied: emitted this six-field block bound to the manifest hashes at the base / result: record present in this file and mirrored in the PR body's skills field / incomplete: None / by: readability-phase4-lane-d-batch4-implementer (Stage C; DeepSeek-4.1-Flash (deepseek-flash))
```

## 14. Timing

- Work item named **LaneD-Phase4-Batch4** (Phase 4 re-read, lane D, batch 4: eight whole-page
  re-reads of the lane's next eight pages, evidence record only), started
  **2026-10-15T18:30:31-07:00** (America/Los_Angeles; the first timestamp this batch recorded,
  taken after the turn-1 snapshot).
- Finish: the machine-recorded bound is the Stage C commit's own author date,
  **2026-10-16T01:43:17Z** (2026-10-15T18:43:17-07:00) — **12 minutes 46 seconds** after the recorded
  start. The pull-request body carries that figure and the first four repair rounds' own start/finish/wall
  times; **the fifth repair's start was not instrumented**, and its only machine-recorded time bound is
  its commit `61371fa5`'s author-and-committer date **2026-10-17T00:29:47Z** — which also bounds it
  above at **6 minutes 15 seconds**, because the sixth Stage D `REVISE` it answers was posted
  `2026-10-17T00:23:32Z`; that is a bound, not a measurement. **No separately instrumented finish time exists for the batch**:
  active time was **not** instrumented, so wall time is an imperfect comparison with the estimate
  rule's active-time requirement and no per-page active rate is claimed.

---

*Prepared by a **DeepSeek** agent (**DeepSeek-4.1-Flash (deepseek-flash)**) operating under the
owner account, as the repository's attribution rule (2026-10-13) requires.*
