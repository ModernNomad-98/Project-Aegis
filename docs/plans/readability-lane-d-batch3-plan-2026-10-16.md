# Stage A plan — Phase 4 readability lane D, batch 3 (PR #784) — revision 3

**Plan revision 3**, 2026-10-16 — it re-captures plan revision 2 because a Stage C repair moved the
head and made two of revision 2's own criteria false; it also carries revision 1's corrections
(§11). **Stage: A (PLAN).** **Role A**
is this repository, the Project Aegis source library (Role B is a consumer or product repository that
copied the Aegis files).
**Planner:** agent `readability-phase4-lane-d-planner-a1`, model **DeepSeek-4.1-Flash
(`deepseek-flash`)** — a holder that did not draft, repair, read, audit or merge the diff, and holds
**Stage A only**. **SD-B**, the independent plan audit, is a different agent's stage; this planner must
not hold it (and does not hold C, D, E, F or G on this change either).

**Reading key — every internal label used below, in plain words.**
`SD-A`…`SD-G` are the delivery workflow's verdict tokens for its seven stages (A PLAN, B PLAN AUDIT,
C IMPLEMENT, D IMPLEMENTATION AUDIT, E VALIDATE, F FINAL REVIEW, G MERGE). **C-1** is the standing
ruling that an unglossed term which is a library-wide convention is an **observation**, not a
per-page defect; the stronger test is whether the page itself resolves it. **C-3** is this plan's
label for the batch-selection rule — the next batch means the next eight **unread** pages, selected
from the unread sequence and named **by path**, never by index and never by index arithmetic. **That
label is not a tracked ruling in this tree (§6)**; the rule rests on its own derivation, not on the
name. **C-4** is the standing ruling
that a page dispositioned **PARTIAL** gets no acceptance row of any kind and stays pending. The
**keeper** is the agent that records a page's acceptance row in the consolidated ledger table; a
**keeper row** is one such row. A **reader page** is a tracked `.md` file other than the `scripts/`
fixtures (except `scripts/tests/fixtures/README.md`) and the one generated report
`docs/audits/skill-contract-audit-baseline.md` — this is the instrument's own `classify_tree` rule.
The **unread sequence** is the reader pages that carry no recorded acceptance at the measured
revision: the instrument's `no_recorded_acceptance` bucket plus its `provably_pending` bucket. A
**blob SHA** is Git's content hash of a file's exact bytes. **PROC-04** is the repository's
body-digest normalization rule (three bound fields, whitespace collapsed, joined with newlines,
sha256). `AEGIS-APR-nnn` are entries in `docs/approvals/APPROVAL_REGISTER.md`. **Lane D** is one of
four disjoint quarters of the unread sequence used by the Phase 4 re-read programme. **Docs-only** is
the change class whose validation floor is links/rendering sanity plus review, with no human approval
required.

---

## 1. The work item and its exact scope

**Work item: `LaneD-Phase4-Batch3`** — the Phase 4 whole-page independent re-read of lane D's
batch 3, recorded as evidence only.

**In scope, by path (the change under this plan):**

- `docs/evidence/documentation/readability-phase4-lane-d-batch3-2026-10-15.md` — **one new file**, the
  lane's tracked batch record (the primary artifact). At the head it is blob
  `cc460c0cd9fae1846046df65ffc36c6c5efe6157`, 446 lines, 38,937 bytes,
  sha256 `6f02d168d47482bbad80dfbe71445052eec5ad0bc53bd06af0640ab6358c6c1a`.

**In scope, by path (the eight pages the record dispositions — read, never edited):**

| ID | Path (all under `docs/evidence/documentation/`) | Blob at the acceptance revision `e2a3e20b…` |
| --- | --- | --- |
| LD-17 | `readability-maintainer-guides-2026-09-23.md` | `c185737776cc30eb01d6835185c0a32eba8f99a3` |
| LD-18 | `readability-reread-batches-2026-10-12.md` | `cf399891b27a81b1bf269ad6e990e22197ddb3f8` |
| LD-19 | `readability-technical-guides-2026-09-23.md` | `21df1e2b6a982aea6510981925eced9fa4ac613b` |
| LD-20 | `remaining-active-docs-readability-2026-09-23.md` | `2f646d3e4ba4e43a57634f6e09e8ee6b4c1dcd69` |
| LD-21 | `roadmap-current-forecast-routes-2026-09-23.md` | `3061a07d3663028248acccff69fdf52c54d06dd3` |
| LD-22 | `roadmap-deep-status-terms-2026-09-23.md` | `7d689fb2eed5babf152d5b34e8e94fe3fcfdc00a` |
| LD-23 | `root-readme-workspace-routing-2026-09-23.md` | `6e12a60bc4a22f63896cd3808da947062307e51f` |
| LD-24 | `root-status-docs-readability-2026-09-23.md` | `336934fcd552cb31b4f7a40d547d88b51e9886fa` |

**Out of scope — named, not left implicit.** No edit to any of the eight pages (they are dated records;
the no-rewrite discipline forbids it). No keeper row, no ledger edit. No index rebuild
(`build_index.py --write`) — that is AEGIS-APR-115's own pull request. No second batch, no other lane's
range, no merge, no rebase, no head move.

**The revision this plan is written against.** The head is
`87c637dfb9dd646965d2dc43fff08887160c35f8` (40 hex, re-derived here — see §11). **The dispatch that
requested revision 1 named `1aa632f7e66a865c5206b6361d8ebf512120e8c4`; that 40-hex object does not
exist in the repository** (`git cat-file -t` fails; `git ls-tree` answers "not a tree object"). The
two strings differ only in the last three bytes, transposed (`…1208e64` is real; `…120e8c4` is not).
The API field `head.sha`, `git rev-parse refs/pull/784/head` and `refs/remotes/pr/784/head` all
return `87c637df…` at this capture. **The head HAS moved since revision 2**, and that move is the
whole reason for this revision: `87c637df…` is the first head
`99d46d752357c6cb127274944ce2ac2ff0b9b78e` plus repair commit `1aa632f7…` (repair round 1) plus
repair commit `87c637df…` (repair round 2, Stage C's fix of SD-E's rendering FAIL) — **three
commits**, one more than the two revision 2 was written against. Revision 2's AC-15 asserted the head
was still `1aa632f7…`; it is not. Revision 2's AC-1 asserted `+449/−0`; it is `+446/−0`. **Both are
corrected here rather than excused by a Stage D exception**, following this plan's own precedent —
revision 1 → 2 was the same repair, after the first SD-D moved the head. §13 carries the full sweep.

## 2. What the change is, why it exists, and the blast radius

- **What.** One new Markdown evidence record. It states the lane derivation, the eight-page roster with
  per-page **FULL** dispositions, the read-depth record (628 lines), the six acceptance bullets
  addressed per page, four observations, the C-4 rule with its construction proof, and eight verbatim
  row-quote strings offered to a separate keeper.
- **Why.** The readability programme's standing batching procedure (ledger L3018-3020, quoted in the
  record's §12) requires a tracked batch record per batch, and AEGIS-APR-101 requires the reader not to
  author its own acceptance rows. The record is the evidence the separate eligible keeper will record
  from, and the artifact the programme's count honesty depends on.
- **Blast radius.** Exactly **one path, added**, against the merge base
  `e2a3e20b7c20ef8385b219b39c6405237163406f` (which is also the API `base.sha` and the **first**
  commit's only parent — **not** the head's: the head `87c637df…`'s only parent is `1aa632f7…`,
  whose own only parent is that first commit, `99d46d752357c6cb127274944ce2ac2ff0b9b78e`): `446`
  added, `0` deleted, one `A` entry in
  `--name-status`, 0 other paths. **No code,
  script, workflow, test, configuration, data or lock file is added, modified or deleted** — the diff
  is Markdown only, so the change is not code-bearing (workflow blob `bff407a6…` L400-403) and the
  lighter pure-docs path applies. The repair commits alone are **+133/−45** (repair round 1,
  `99d46d75…` → `1aa632f7…`) and **+1/−4** (repair round 2, `1aa632f7…` → `87c637df…`) inside
  the same file; no path is touched in either scope.
- **Governance text is not touched**: the diff adds a new file only; no rule, register entry, skill,
  script or workflow is edited.

## 3. Recorded change classification (change-classification-gate, applied before Stage A)

`change-classification-gate` was read at the head
(`.claude/skills/change-classification-gate/SKILL.md`, sha256 `08d91a83…` in
`tools/skills-manifest.json`) and applied to the file set above. Its own output shape:

```text
CHANGE CLASSIFICATION
Deliverables:    one new tracked evidence record, docs/evidence/documentation/readability-phase4-lane-d-batch3-2026-10-15.md
Classes:         docs-only (the single deliverable)
Governing class: docs-only
Approval path:   none (docs-only requires no human approval)
Validation plan: docs-only floor = links/rendering sanity + review. Applied: the changed path's Markdown
                 link check, the repository's skill validator and gate self-test, the readability
                 instrument at base and head, and the structural PR-body check.
Scope contract:  exactly one path: docs/evidence/documentation/readability-phase4-lane-d-batch3-2026-10-15.md
```

**The classification is `docs-only`, recorded here in the plan as the workflow requires
(blob `bff407a6…` L397-398).** Scope growth into a code-bearing class would force reclassification and
would move the change off this path; no such growth is authorised by this plan.

## 4. Proportionate acceptance criteria (each decidable; C-1 screened)

Every criterion states its decision procedure and whether it is verifiable at the implementation head
(`87c637df…`). The C-1 screen is applied to every criterion that could fail a page for an unglossed
term: **the term must first be shown not to be a library-wide convention, measured over the reader
pages at the measured revision.** The convention threshold used is the one the merged lane A batch-5
record published and applied (`docs/evidence/documentation/readability-lane-a-batch-5-2026-10-15.md`,
blob `a1f537a9…` at `origin/main`; its section 5 table: `acceptor` on **12** reader pages =
"convention — observation"; `Phase 1.5` on **11** = "below convention — the one gap recorded in this
batch"). **So ≥12 reader pages = a convention, and an unglossed use of it is an observation, not a
gap.** The lane A record is cited from `origin/main`; it is **absent at this change's base and head**
(recorded in §12).

**The C-1 measurements this plan took**, at the base `e2a3e20b…` over the **653 reader pages** (the
instrument's own `classify_tree` rule; method and reproducibility in §4.1):

| Term | Reader pages containing it | Occurrences | C-1 treatment at the ≥12 threshold |
| --- | ---: | ---: | --- |
| `PR` / `PRs` | **291** | 4,152 | convention — observation (LD-18, LD-23) |
| `UTC` | **106** | 842 | convention — observation (LD-19) |
| `sha256` | **37** | 146 | convention — observation (LD-18) |
| `ETA` | **30** | 270 | convention — observation (LD-19) |
| `AEGIS-060` | 17 | 80 | below the threshold, but the page resolves it (LD-20 defines it at L27-29) — observation |
| `#186` | 7 | 45 | below the threshold, but the page resolves it (LD-21 expands it at L23) — observation |
| `EVAL-004` | 2 | 17 | below the threshold, but the page resolves it (LD-20 defines it at L27-29) — observation |
| `API` (benchmark) | 204 | 720 | convention — corroborates the threshold's stability |
| `CI` (benchmark) | 250 | 1,574 | convention — corroborates the threshold's stability |

At the head the same measurement over the **654** reader pages gives 292 / 107 / 38 / 31 for the four
convention terms — the +1 in each case is this change's own new record, which itself uses the terms.
**No criterion below fails a page for any of these terms.**

**AC-1 — scope and blast radius.** The change under this plan is exactly one added file,
`docs/evidence/documentation/readability-phase4-lane-d-batch3-2026-10-15.md`, `+446/−0` against
`e2a3e20b…`, and no code, script, workflow, test, configuration, data or lock file is added, modified
or deleted.
*Decide by:* `git diff --numstat e2a3e20b… <head>` (one line, `446  0  <path>`) and
`git diff --name-status` (one `A`). **Verifiable at the implementation head: yes.**
> **Corrected in revision 3.** Revision 2 stated `+449/−0` and `449  0`. Stage C's repair round 2
> joined four wrapped source lines into one (record old L308-L311 → new L308), removing three LF
> lines and so three added lines: the numstat at `87c637df…` is `446  0`, and the record's own LF
> count is 446 (it was 449). **The byte count is unchanged at 38,937** — three removed newlines equal
> three inserted spaces — so only AC-1's line figure moves, never its byte figure.

**AC-2 — classification recorded.** The plan records `docs-only` as the change's class in §3, and the
diff carries no skill frontmatter, security rules or stop conditions.
*Decide by:* this plan's §3 and `git diff --name-only`. **Verifiable at the head: yes.**

**AC-3 — the record names its work item and its acceptance revision, and that revision is reachable.**
The record names `LaneD-Phase4-Batch3`, the lane, Stage C, the base and the acceptance revision
`e2a3e20b…`, and `git merge-base --is-ancestor e2a3e20b… refs/remotes/origin/main` exits 0.
*Decide by:* record L3-24 and the `merge-base` command. **Verifiable at the head: yes.**

**AC-4 — the eight pages are named by path, with their base bytes fixed.** The record's §4 table names
exactly the eight paths in §1, each dispositioned `accepted unchanged (full)`; each path's blob at
`e2a3e20b…` equals the value in §1.
*Decide by:* extract the §4 table; `git rev-parse e2a3e20b…:<path>` for each. **Verifiable at the
head: yes.**

**AC-5 — the C-1 screen holds for every term observation.** Every unglossed-term observation in the
record is either (a) a term measured on **≥12** reader pages at the base (291 / 106 / 37 / 30 — the
table above) or (b) resolved by the page itself (LD-20 defines `EVAL-004` and `AEGIS-060` at L27-29;
LD-21 expands `#186` at L23). No page is denied acceptance on an unglossed-term ground.
*Decide by:* re-run the §4.1 measurement; read record §4 and §6(b). **Verifiable at the head: yes.**

**AC-6 — the C-4 rule holds and no partial-page string is offered.** Record §4 contains **0** PARTIAL
dispositions; §10 offers exactly **8** strings, each for a page dispositioned FULL, and states the C-4
rule with its construction proof (a throwaway row quoting a `(partial; gap(s) section 6(b))` string
made `build_index.py --report` exit 0 with `table_rows` 101→102 and `check_index.py --json` exit 0
with `official_pending_count` 597→596, then was reverted and never pushed).
*Decide by:* count the dispositions and strings in §4/§10; confirm the diff adds no row.
**Verifiable at the head: yes.**

**AC-7 — no keeper row and no ledger edit.** The diff adds no `| K-` row; the ledger blob and the
index blob are byte-identical at base and head (`aa6acddf031054646c538d9b3ff9522278ca7ddd` and
`eeda4929cca872d626eb2ca6ca21583586335d11`).
*Decide by:* `git rev-parse <ref>:<path>` at both refs; grep the diff. **Verifiable at the head: yes.**

**AC-8 — the instrument's figures reproduce.** `check_index.py --json --ref <head>` exits 0 with
`654 / 57 / 4 / 587 / 0 / 0 / 6 / 597`; `--quiet` exits 0; `build_index.py --report` exits 0 at the
head **and** the base with the identical block `table_rows 101, events 101, full_page_acceptances 81,
lost_commit_events 10, reader_pages_with_rows 68` — no row change.
*Decide by:* run the three commands (this plan ran them; outputs in §9). **Verifiable at the head:
yes.**

**AC-9 — count honesty.** The record publishes **no** readability count of its own; it attributes the
+1 reader page, the +1 `no_recorded_acceptance` and the +1 official pending count to its own new
page; it predicts **no** post-rebuild figure.
*Decide by:* record §9; the base/head instrument runs in §9. **Verifiable at the head: yes.**

**AC-10 — the C-3 selection rule for the next batch is stated, path-anchored, and index-free.** §6 of
this plan states the rule and names the next eight pages **by path**; the rule contains no index, no
index arithmetic and no pinned range. The frozen record still carries index arithmetic in its §2 (the
SD-B finding); this plan names that as a **declared observation carried at the frozen head** — it is
not rewritten here, because rewriting it would move the head and void every head-bound verdict.
*Decide by:* read this plan §6 and the record §2. **Verifiable at the head: yes** (the criterion is
about the plan's text and the record's frozen state, both readable at the head).

**AC-11 — the non-author test is stated and this PR authors no rows.** §8 of this plan states
AEGIS-APR-101's two-clause test and the AEGIS-APR-117 route, records that this change authors no rows
and edits no ledger section, and names who will record the rows (a separate eligible keeper — not the
page's author, not its accepting reviewer, not any stage of this PR, not the coordinator).
*Decide by:* read this plan §8; AC-7's blob comparison. **Verifiable at the head: yes** for the
statement and the no-rows fact; the keeper's own act is AC-14.

**AC-12 — the offered strings are complete and machine-usable.** Each of the eight §10 strings contains
the page path and the **full 40-character** acceptance revision `e2a3e20b7c20ef8385b219b39c6405237163406f`,
and each string's page matches a FULL row in §4 (8/8).
*Decide by:* extract the §10 block; compare. **Verifiable at the head: yes.**

**AC-13 — DECLARED NOT VERIFIABLE AT THIS HEAD: the read-depth prose claim.** The record asserts every
one of the 628 lines was "read as prose" with no range skipped. The **line counts are** checkable
(43+319+48+63+33+30+55+37 = 628), but "read as prose" is a statement about a reading process that
leaves no artifact evidence; no command can decide it. **Reason recorded here as L180 requires**, so a
Stage D `UNRUN` on this criterion is permitted.
*Decide by:* not decidable at this head; the line-count component is decidable.

**AC-14 — DECLARED NOT VERIFIABLE AT THIS HEAD: the eight pages' acceptance rows.** The rows are
recorded by a separate eligible keeper, from this evidence, in a **separate change** under
AEGIS-APR-117 — they do not exist at this head and **must not** exist in this diff (C-4 and the SD-D's
F1: any row in this diff would be the same agent recording its own read). **Reason recorded here as
L180 requires**; a Stage D `UNRUN` is permitted. The sub-facts that *are* verifiable at this head are
AC-7 (no row exists here) and the eligibility conditions in §8.

**AC-15 — the plan is captured, and the PR head is named as it stands.** This plan's exact text is
captured at a named immutable revision: a tracked file at
`docs/plans/readability-lane-d-batch3-plan-2026-10-16.md` on branch
`stage-a/lane-d-batch3-plan-2026-10-16` (commit and blob SHA named in the PR body and in the posted
comment), and posted verbatim as a PR issue comment whose id the PR body names. The PR head is
`87c637dfb9dd646965d2dc43fff08887160c35f8`, and **this plan does not move it** — the plan's own
commit is on the side branch, and no commit of the PR branch is touched by this capture. **Stated
exactly, because the topology is not what a reader would guess:** the plan branch was cut from
`1aa632f7…`, which is the current head's only parent and **not** the head, so `87c637df…` is **not** an
ancestor of the plan branch (`git merge-base --is-ancestor 87c637df… HEAD` exits 1). §11 says why the
branch is deliberately not rebased onto the new head.
*Decide by:* `git rev-parse origin/stage-a/lane-d-batch3-plan-2026-10-16:docs/plans/…`;
`gh pr view 784 --json headRefOid`; read the named comment. **Verifiable: yes** (at those refs, not
inside the frozen PR diff — see §11 for why the plan is deliberately not in the PR diff).
> **Corrected in revision 3.** Revision 2 said "the head has not moved" and "The PR head is still
> `1aa632f7…`". Both were true when revision 2 was captured, and both became false at
> `2026-10-16T04:03:49-07:00`, when Stage C's repair round 2 committed `87c637df…`. The criterion is
> restated above as a *checkable* claim about a named revision plus a claim about **this plan's own
> act**: the head's movement is Stage C's, and no plan can promise that a head will never move.

### 4.1 The C-1 measurement, reproducible

The reader-page universe is the instrument's own rule: `git ls-tree -r --name-only <ref>` filtered to
`.md`, minus `scripts/` except `scripts/tests/fixtures/README.md`, minus
`docs/audits/skill-contract-audit-baseline.md` (653 paths at `e2a3e20b…`, 654 at the head). Prevalence
is then `git grep -o -E <regex> <ref> -- '*.md'` restricted to those paths, counting matching files
and matches per file. Regexes used: `\bPRs?\b`, `\bUTC\b`, `sha256`, `\bETA\b`,
`\bAPI\b`, `\bCI\b`, `AEGIS-060`, `EVAL-004`, `#186`. **One honest difference from the record:**
the record publishes 4,153 `PR`/PRs occurrences; this plan's regex counts **4,152**. The page counts
agree exactly (291 / 106 / 37 / 30). The one-occurrence difference is a regex artefact at a word
boundary, not a defect; the threshold decision is unaffected either way.

## 5. Criteria declared not verifiable at this head (the L180 list)

Two criteria, both with their reasons recorded above, are declared not verifiable at this head:
**AC-13** (the prose-read claim — a process statement with no artifact) and **AC-14** (the keeper's
rows — a future, separate change that must not appear in this diff). Everything else in §4 is
decidable at the head by the command named. This is the plan's own `SD-A` obligation under the
workflow's `SD-D` row (blob `bff407a6…` L180): an `UNRUN` at audit time is permitted **only** for a
criterion declared here with its reason.


**Re-checked in revision 3, after the repair.** Stage C's repair round 2 changed the *record's* bytes
(joining four wrapped source lines) and nothing else, so **it did not change what AC-13 or AC-14 can
decide.** AC-13's decidable component is the eight **pages'** line counts — 43+319+48+63+33+30+55+37
= **628**, re-counted here at the acceptance revision `e2a3e20b…` (the eight pages are untouched by the
repair) — and AC-14's decidable component is that no keeper row exists in this diff, which is still
true: the ledger blob is `aa6acddf…` at the base and at `87c637df…`, the index blob is `eeda4929…` at both,
and the diff remains one added `docs/` path. **Neither declaration is stale and neither is widened.** One
adjacent fact the repair *did* change is **verifiable** and was previously false — the record's §8
observations table now renders one `tr` per source row (asked directly of GitHub's own GFM renderer,
`POST /markdown` with `mode=gfm`: **5** `tr` elements where the same section produced **8** at
`1aa632f7…`) — and this plan records that in §13 rather than adding a sixteenth criterion, because §4's
criterion set is the set Stage B and Stage D have audited, and a re-capture is not the place to widen
it.
## 6. The C-3 / next-batch selection rule (path-anchored; never an index)

**The rule for the next batch (batch 4), stated so it cannot be misread:**

> **Batch 4 is the next eight UNREAD pages in the lane's unread sequence, re-measured at the next
> implementation base and named BY PATH.** The starting point is the last page the batch-3 record
> names: `docs/evidence/documentation/root-status-docs-readability-2026-09-23.md` (LD-24). Batch 4 is
> the first eight paths that sort **after that path** in the unread sequence at that base, in the
> lane's own committed order. **No index, no index arithmetic and no pinned range appear in the rule**;
> a page that has since acquired a recorded acceptance is skipped as READ and the next unread path is
> taken, so the batch stays eight whole-page re-reads.

**How it is derived from the lane records' own committed bytes** (the instrument cannot compute a
frontier, so the rule is anchored on the records' own text):

1. Read the lane's committed records and take the page list each one names in order: batch 1 =
   `docs/evidence/documentation/readability-phase4-lane-d-batch1-2026-10-15.md` (blob `7a479f86…` at
   `origin/main`; LD-1…LD-8), batch 2 =
   `docs/evidence/documentation/readability-phase4-lane-d-batch2-2026-10-15.md` (blob `706bf4aa…` at
   `refs/pull/778/head`, whose head is `e5d327ca…`; **not merged** — PR #778 is still open), batch 3 =
   this change's record (blob `cc460c0c…`; LD-17…LD-24).
2. Re-measure the unread sequence at the next base with the instrument: reader pages minus the paths
   the committed `acceptance-index.json` carries rows for (`no_recorded_acceptance`) plus the paths
   whose recorded acceptance has drifted past the rule (`provably_pending`), sorted. At
   `e2a3e20b…` that is **586 + 4 = 590** paths; at this head **587 + 4 = 591**.
3. Take the eight paths immediately following LD-24's path. **As of this base and head, those eight
   are:**

| # | Path (all under `docs/evidence/documentation/`) | Blob at `e2a3e20b…` |
| --- | --- | --- |
| 1 | `scenario-a-runbook-readability-2026-09-23.md` | `78e865de87949b578ca5682d289cbbf709b4e194` |
| 2 | `setup-routing-plan-readability-2026-09-23.md` | `00cdb7dadcba4c56521390e25233b56307991b57` |
| 3 | `skill-category-01-07-readability-2026-09-23.md` | `acc445e3435875850538063b4a14ba2939219977` |
| 4 | `skill-category-map-readability-2026-09-23.md` | `290c9bcee387521b13bbd6a7e49ed8ba4102a3d9` |
| 5 | `skill-docs-eighth-20-readability-2026-09-23.md` | `e2dafc86eb2088035142d6a05b9dd63db7b60aed` |
| 6 | `skill-docs-fifth-20-readability-2026-09-23.md` | `4e81cf73e17c38372497608bf46de0d2b8fec445` |
| 7 | `skill-docs-final-screen-readability-2026-09-23.md` | `9bbfacc2034151028d6134ec8fb4ab6c7f5e00fc` |
| 8 | `skill-docs-first-20-readability-2026-09-23.md` | `145d7a112b6b04822be697f418293847ef15bd6f` |

4. **Re-check at the next base, not now.** The eight above are the derivation *at this base*; the rule
   binds the **next** batch to a **fresh measurement** at its own base, so a page that gains a row in
   the meantime drops out and the next unread path takes its place. Re-check disjointness the way the
   batch-3 record does — path-by-path against the other lanes' records — before reading. (At this base
   all eight are in the unread sequence by construction; they are *cited* as background in the older
   2026-09-24 `full-page-readability-batch-after-218/219` records, but **none carries an acceptance
   row**, which is exactly why they are still unread.)

**Why the rule is written this way, in the record's own numbers.** The same eight paths come out at the
base and at the head, but the anchor path's **0-based position in the unread sequence moves from 467
(base) to 468 (head)** purely because this change's own new record sorts before it. An index-based
rule would therefore have to be re-derived at every ref and could silently select a different page; a
path-anchored rule is stable. This is C-3's point, demonstrated on this change's own data.

**One honest note on the two labels, "C-3" and "R2".** The dispatch that requested this plan calls
this "the C-3 / R2 selection rule". **Neither label is a tracked ruling in this tree, and neither is
offered here as the rule's authority.** A search of the tracked tree at the head finds no readability
standing ruling named `R2` — the `R2` hits are the Behavioral Eval Runner's judge-calibration item
and unrelated re-read range labels — and none named `C-3`: the only two `C-3` hits at the head are
unrelated change-site IDs (a worked `C-1..C-3` row range inside the batch-3 record, and a table row
ID in `docs/evidence/documentation/readability-reread-batches-2026-10-12.md`). "R2" is a **reading**
defined in the merged lane A batch-5 record
(`docs/evidence/documentation/readability-lane-a-batch-5-2026-10-15.md`, blob `a1f537a9…` at
`origin/main`, its section "The reading used: R2") — a record, not a ruling. **The rule above is the
rule this plan binds the next batch to; it rests on its own derivation from the lane records'
committed bytes and the instrument, not on either name.** This plan keeps the label `C-3` for
continuity with the dispatch, with this caveat stated; if a ruling by either name exists elsewhere,
this plan could not verify it (§12).

## 7. The five-question necessity and reuse answers, with routing

**1. Necessity — what need, and the evidence it exists.**
*Answer:* The delivery workflow's Stage B entry condition (blob `bff407a6…` L28) requires the plan's
exact text bound to a captured revision, and Stage B has posted **`SD-B: REVISE`** on this PR for the
absence of exactly that (issue comment `6211504777`, 2026-10-16T08:35:04Z). Under the workflow's
`REVISE` routing (L48-49) the work returns to Stage A, and L572 states "A plan is always required, but
its size is proportional to the change."
*Routing disposition:* **satisfied — cite the proof** (the posted verdict; the workflow lines).

**2. Reuse — what existing mechanism already does this.**
*Answer:* The **method** is reused, not reinvented: the ledger's standing batching procedure (L3018-3020)
supplies the batch shape, the four lane records supply the page-selection precedent, and the workflow's
own intake condition for a diff that already exists supplies the plan-of-record shape (L493-497). The
one thing that does **not** exist is a captured plan: `docs/plans/` contains **0** files at the head,
and a repository-wide search of the head tree finds no plan artifact and no issue/PR carrying the
coordinator's batch-3 brief (the SD-B's own finding, confirmed by this plan's re-derivation of the
head).
*Routing disposition:* **nothing suitable → the smallest new thing** (one new Markdown file plus its
capture), with the existing method cited rather than copied.

**3. Ownership — who holds the authority and responsibility for this surface, at this revision.**
*Answer:* The **Stage A holder** (this planner) writes the plan-of-record and holds Stage A only
(L493-497: "This actor holds Stage A only — it is the *planning* agent, not the adopting one, and it
must not also take Stage C"). The **merge** decision stays with the owner and Stage G. The **keeper**
role for the acceptance rows is AEGIS-APR-101's, not this plan's, and this change requests no grant
(it proceeds under the owner's standing backlog grant AEGIS-APR-039, which the record cites and this
plan does not extend). The **index rebuild** is AEGIS-APR-115's separate scope.
*Routing disposition:* **owned → proceed inside the existing authority; do not re-ask.**

**4. Minimum-safe action — the smallest action that satisfies the need without weakening a control.**
*Answer:* Write **one** plan file, capture it (one pushed commit on a new branch, one posted comment),
and name both in the PR body. **No** row is authored, **no** ledger section is edited, **no** page is
edited, **no** script or workflow is added, **no** check is removed or downgraded, **no** validation
tier is lowered, **no** scope is widened, and **the head does not move** — the diff stays exactly what
Stage B will audit.
*Routing disposition:* **smallest change.**

**5. Complexity justification — why the machinery is warranted, and what would be smaller.**
*Answer:* The alternative already failed: a plan living only in a PR body is not a captured plan
(L587-592), and this PR has now had that fail once. What is added is one Markdown page and one comment
— no new tooling, no new script, no new gate. A smaller unit (a comment alone) would satisfy the
"immutable comment" half of the rule but not give a tracked path and blob SHA; a larger unit (a head
move to carry the plan into the PR) would cost every head-bound verdict and is not needed.
*Routing disposition:* **bounded check already performed** (the SD-B finding) — no new machinery, no
time-boxed investigation owed.

## 8. The non-author test (AEGIS-APR-101 and AEGIS-APR-117)

**This change authors no keeper rows and edits no ledger section — by design, and that fact is
verifiable (AC-7).** The rows for the eight pages are a **separate eligible keeper's** work, recorded
from this evidence.

- **AEGIS-APR-101** (register L3149-3159) sets the test: "The keeper must be a different agent from
  the page's author and accepting reviewer. The coordinator may not hold this role" (L3155), and its
  "Scope FORBIDDEN" clause (L3157) bars self-review, overriding review findings, merging by the keeper,
  and **waiver of existing review and delivery requirements**. **There is no waiver provision at
  L3155-3157.**
- **AEGIS-APR-117** (register L5016-5042) is the keeper's **withdrawal-and-re-record** route: "the
  ledger keeper may append a withdrawal row that cancels a recorded acceptance row that turns out to
  be wrong … The ledger is never rewritten" (L5038-5042). It is **withdrawal-only**; it is not an
  authority to record a fresh acceptance in place of a missing one.
- **The owner declined to ratify a carry-with-deviation on 2026-10-15.** Decision 3 of
  `docs/roadmaps/OWNER-DECISIONS-2026-10-15.md` (blob `f2010a75…` at `origin/main`) is headed
  "NO ratification; use the AEGIS-APR-117 route": the same-agent rows are to be **withdrawn and
  re-recorded by a different, eligible keeper**, not carried with a declared deviation. That file is
  **absent at this change's base and head** (§12); it is cited from `origin/main` by blob.

**Who will record the rows, stated plainly:** a separate **eligible keeper** — one that is **not** any
page's author, **not** its accepting reviewer, **not** any stage of this change (not this Stage A
planner, not the Stage C reader/implementer, not the Stage B, D, E, F or G holder) and **not the
coordinator**. This plan **allocates no row ID and names no keeper identity**; the eligibility test is
satisfied (or not) at recording time, by the keeper's own row metadata. For orientation only: the
merged AEGIS-APR-117 re-record PR #781 recorded this lane's batch-1 rows (K-389…K-396) under an
eligible keeper identity — the same identity is a natural candidate for batch 3's rows, **subject to
the same test at recording time**, and this plan does not bind it. Recording happens in the keeper's
own change, not here; the strings it records from are the record's §10 block, each carrying the full
40-character acceptance revision (AC-12).

## 9. The evidence this work produces, and where it lives

| Evidence | Where it lives |
| --- | --- |
| The batch-3 evidence record (the change itself) | `docs/evidence/documentation/readability-phase4-lane-d-batch3-2026-10-15.md`, blob `cc460c0c…`, at the PR head |
| This plan, captured | `docs/plans/readability-lane-d-batch3-plan-2026-10-16.md` on branch `stage-a/lane-d-batch3-plan-2026-10-16` (blob SHA and commit named in the PR body), and posted verbatim as a PR comment (id named in the PR body) |
| The instrument's figures at three refs | reproducible by command: `python -P -B tools/readability_acceptance/check_index.py --json --ref <ref>`; base `e2a3e20b…` `653 / 57 / 4 / 586 / 0 / 0 / 6 / 596`, superseded head `1aa632f7…` and head `87c637df…` both `654 / 57 / 4 / 587 / 0 / 0 / 6 / 597`, all exit 0; `--quiet` exits 0 at each; `build_index.py --report` gives the identical block `101 / 101 / 81 / 10 / 68`, exit 0, at **base, `1aa632f7…` and `87c637df…` alike**. All were run in this planning session; **the head move changed none of them** |
| The C-1 prevalence table | this plan §4, reproducible by the command in §4.1 |
| The row-quote strings for the keeper | record §10 (8 strings, FULL pages only) |
| The stage receipts (SD-A…SD-G) | the PR conversation: SD-B **REVISE** `6211504777` and SD-B **REVISE** `6212915586` (both against revision 1); SD-D **REVISE** `6209631818`; then SD-D **ACCEPT** `6213714837` and SD-E **FAIL** `6213965761`. **Those last two are bound to `1aa632f7…` and are therefore void at `87c637df…`** — a fresh SD-D and a fresh SD-E are owed at this head |
| The keeper's rows | the consolidated keeper table in `docs/roadmaps/aegis-documentation-readability-backlog.md`, appended by the separate keeper's own change — **not** by this PR |

## 10. What this plan does NOT decide

Named rather than left implicit:

1. **It does not move the head and does not authorise any edit to the record or the eight pages.** The
   head is `87c637dfb9dd646965d2dc43fff08887160c35f8` and **this plan leaves it there**: the plan's
   own commit lands on the side branch `stage-a/lane-d-batch3-plan-2026-10-16`, never on the PR
   branch, so no head-bound verdict can be moved by this capture. (The head *did* move at
   `2026-10-16T04:03:49-07:00` by Stage C's repair round 2 — that is Stage C's act, and the reason
   this revision exists; see §13.) In particular this plan does **not** rewrite the record's §2
   index-arithmetic wording or its L6-10 "Plan applied" sentence (which says no separate plan artifact
   exists — **superseded by fact** once this plan is captured, and named here and in §6 as a declared
   observation carried at the frozen head). A later head-moving repair may align that sentence; that
   decision is not taken here.
2. **It does not record, withdraw or re-record any keeper row**, does not allocate row IDs, and does
   not name or bind the keeper. It does not claim the keeper's independence (AEGIS-APR-101's second
   clause is the keeper's to satisfy).
3. **It does not accept the pages.** Acceptance is Stage D/E/F's per the workflow, and the pages'
   eligibility for a full-page row is the keeper's determination bound to the evidence.
4. **It does not authorise the index rebuild** (`build_index.py --write`) and predicts **no**
   post-rebuild count; the rebuild is AEGIS-APR-115's separate pull request. Any rebuild is
   code-bearing and off this path.
5. **It does not re-open or re-decide C-1, C-3 or C-4**, the ≥12-page convention threshold, or the
   owner's 2026-10-15 no-ratification decision. It applies them.
6. **It does not execute the next batch** — §6 states the selection rule and the current derivation;
   the next batch's own base, roster and record are its own Stage A's work.
7. **It does not decide the Stage B verdict**, and it is not the plan audit. It also does not decide
   whether "R2" names a separate ruling (§6) — that could not be verified here.
8. **It does not classify or plan any other change**, lane, or pull request, and it does not touch any
   other lane's branch, clone or record.

## 11. The plan's own revision, and how it is captured

**Revision 3** of this plan — it re-captures revision 2 after a Stage C repair moved the PR head, and
it carries revision 1's corrections. Capture, so that Stage B has an exact text to bind (the
requirement is the workflow's own: blob `bff407a6…` L587-592 at this head — at `origin/main`'s newer
blob `9a2ea2bd…` the same paragraph sits at L612-616, which is the numbering the dispatch quoted as
"L613-616"):

- **Why a third revision, stated first.** Revision 2 was captured against the head `1aa632f7…` and
  asserted `+449/−0`. At `2026-10-16T04:03:49-07:00` Stage C committed `87c637df…` (repair round 2,
  the fix of SD-E's rendering FAIL: record old L308-L311 joined onto new L308). That moved the head
  and changed the record's LF line count 449 → 446, so **two of revision 2's own criteria were false
  at the new head** — AC-1 (`+449/−0`) and AC-15 ("the PR head is still `1aa632f7…`"). A Stage D run at
  the new head would have returned `REVISE` on a plan that was accurate when captured. **The remedy is a
  re-capture, not a Stage D exception** — this plan's own precedent, since revision 1 → 2 was the same
  repair after the first SD-D moved the head. **§13 carries the full before → after sweep**, including
  the items beyond AC-1 and AC-15 that the dispatch did not name.
- **What revision 3 changes, and nothing else.** (a) AC-1's line figures and §1's and §2's line and
  numstat counts: `449` → `446`. (b) Every head reference: `1aa632f7…` → `87c637df…`, and the
  commit count two → three. (c) The record's blob and sha256 in §1, §6 and §9: `af7a8502…` →
  `cc460c0c…`, sha256 `705ebf14…` → `6f02d168…` (bytes unchanged, 38,937). (d) The stage receipts in
  §9. (e) §12's Codex note, corrected to name the commit the Codex state block actually binds.
  (f) §5: an explicit re-check that AC-13 and AC-14 are not stale. (g) §14 (new): the bound-field
  digest and the Stage A row block this revision does not insert. (h) §13 (new): the head-move sweep.
  (i) §15 (timing, renumbered from §13) with revision 2's measured finish stated directly.
  **Every other element is revision 2's text, unchanged**: the scope and the eight paths, the what/why
  and blast radius, the `docs-only` classification, the fifteen criteria with the C-1 screen and the two
  declared-not-verifiable criteria, the path-anchored selection rule and its eight paths, the five
  answers with their routings, the non-author test, the evidence inventory and the non-decisions.
- **Superseded captures.** Revision 1 was captured at commit
  `491bad103254d561054d631294d43a09db20493d` (blob `dbc244c3793fd05cdeded3f9383a906799bdd87f`,
  sha256 `8beb89caed02974d8b30c452f535c87d49be689facc66eec71b6f3f901020b8a`, posted verbatim as issue
  comment `6212482822`). Revision 2 was captured at commit
  `b8f91cfe504a11119cb23c642db373fb8b55df83` (blob `2b16f53f6b85a2d30eee81174b0a0f9d71611949`,
  sha256 `967df6b9e336acc03ab678e0a4cf977c75adc0672986112b6894c32b61241fd9`, posted verbatim as issue
  comment `6213082533`). **Both blobs are superseded by this revision's blob**, which the PR body and the
  fresh capture comment both name; **both earlier comments stay posted and unedited**, each as its own
  revision's record. The plan branch is not the PR branch, so **no head moves** with this supersession.
- **Tracked file:** `docs/plans/readability-lane-d-batch3-plan-2026-10-16.md`, committed on branch
  `stage-a/lane-d-batch3-plan-2026-10-16`. **The branch's topology is stated exactly rather than
  assumed**, because it is not what a reader would guess: the chain below this revision's capturing
  commit runs `b8f91cfe…` → `491bad10…` → `1aa632f7…` → `99d46d75…` → `e2a3e20b…` (the merge base), so
  **the branch was cut from `1aa632f7…`** — the head as it stood when revision 1 was captured, which is
  now the **parent** of the current head, not the head. Therefore **the current head `87c637df…` is not
  in this branch's history** (`git merge-base --is-ancestor 87c637df… HEAD` exits 1): the branch
  predates the repair that moved the head. The plan still sits beside the change in the same lineage,
  but the two refs have diverged by one commit. **It is deliberately not rebased onto the new head**: a
  rebase would rewrite the revision-1 and revision-2 capture commits whose SHAs are already published
  in the PR body and its comments, and re-pointing a published capture is exactly what this plan's own
  rule forbids. **The capturing commit's own SHA, the blob SHA of the plan's bytes at it and the file's
  sha256 are recorded in the PR body** and re-derivable with
  `git rev-parse origin/stage-a/lane-d-batch3-plan-2026-10-16:docs/plans/readability-lane-d-batch3-plan-2026-10-16.md`.
- **Immutable posted copy:** the same text posted verbatim as a PR issue comment; **the comment id is
  recorded in the PR body**. The copy is proved byte-exact by extraction and hash, not asserted: the
  declared extraction method is in §14, and **a prior revision of this plan's sibling claimed a
  verbatim copy that did not exist, while a later one dropped the final newline** — so the method and
  the byte-exact comparison are both named. The result is stated in the PR body and the fresh comment,
  because the comment is posted after this plan's bytes are fixed.
- **Deliberately not in the PR diff.** Adding the plan to the PR branch would move the head and void
  every head-bound verdict (workflow L48-49 and the exact-head rule). The plan therefore lives beside
  the change, not inside it, and the PR body carries the capture reference so Stage B can bind it
  without the head moving.
- **Editing this plan after capture voids the ACCEPT** on it, exactly as moving a head voids a
  head-bound verdict.

## 12. What this plan could not verify

- **The dispatch's head string (revision 1's dispatch).** `1aa632f7e66a865c5206b6361d8ebf512120e8c4`
  is not an object in the repository. The string it transposes is
  `1aa632f7e66a865c5206b6361d8ebf512120e8c4`'s real neighbour
  `1aa632f7e66a865c5206b6361d8ebf5121208e64` — the head that revisions 1 and 2 were written against,
  and now the **second** of this branch's three commits (the head is `87c637df…`). Which string the
  dispatch intended cannot be verified from the repository — only that the former does not exist and
  the latter is real.
- **The order of the head move and the dispatch.** This revision was requested *because* Stage C's
  repair round 2 moved the head; the repository shows that commit at `2026-10-16T04:03:49-07:00` and this
  session's first snapshot at `2026-10-16T04:07:51-07:00`, but what the coordinator read, and when, is
  not a tracked artifact.
- **"R2" as a standing ruling.** No tracked artifact at the head defines a readability ruling by that
  name (§6). **Re-measured at `87c637df…`: 78 `\bR2\b` hits, none of them a readability standing
  ruling, and 2 `\bC-3\b` hits, both unrelated change-site IDs — the same counts as at `1aa632f7…`**, so the
  head move changed nothing here.
- **The coordinator's batch-3 brief.** No tracked artifact at any ref carries it; the record itself
  says its quotations of it are "unverifiable, not false" (its §15), and the SD-B found the same.
- **Artifacts cited from `origin/main`, absent at this base and head:** the lane A batch-5 record
  (`a1f537a9…`, the ≥12 convention threshold), the batch-1 record (`7a479f86…`) and
  `OWNER-DECISIONS-2026-10-15.md` (`f2010a75…`). All three are cited by blob at `origin/main`
  (`38413563a8…`, **35** commits ahead of the merge base), not from the frozen tree. A re-measurement at
  a future base re-reads them there.
- **The two external links** on LD-17 (PR #122) and LD-24 (PR #176): not fetched, matching the dated
  records' own practice.
- **Any Codex P1 content.** The Codex state block reports `"has_unresolved_findings": true` with
  `code_review.commit_sha` = `99d46d752357c6cb127274944ce2ac2ff0b9b78e` — the **first** head, not
  `1aa632f7…` and not `87c637df…` — and the PR has 0 submitted reviews and 0 review comments, so no
  finding text is retrievable at any of the three heads. The bot's second comment is a usage-limit
  notice. **Revision 2 said this block reported "at this head"; it never did, and the claim is
  corrected here rather than carried.**
- **The fresh capture comment's byte-exactness.** The extraction method is declared in §14, but the
  comment is posted **after** this plan's bytes are fixed, so the plan cannot carry its own
  verification result; that result is stated in the PR body and in the fresh comment.
- **Any post-rebuild figure**, which this plan does not predict (§10.4).

## 13. The head move: every figure and identifier it invalidated, before → after

The dispatch named two criteria (AC-1, AC-15) as the reason for this revision. **They were not the
only two false figures.** This section is the whole sweep: every count, head reference, line count,
blob id and "at this head" claim in revision 2, re-derived at `87c637df…` by command. Items 1-14 are
statements in this plan that were false at the new head and are corrected above; items 15-17 are
adjacent facts the same move changed, published alongside the plan and recorded here because they
would otherwise stay wrong in the PR body.

| # | Item (revision 2's text) | Before | After | How re-derived |
| --- | --- | --- | --- | --- |
| 1 | AC-1 blast radius | `+449/−0` | **`+446/−0`** | `git diff --numstat e2a3e20b… 87c637df…` → one line, `446  0` |
| 2 | AC-1 decision command's expected output | `449  0  <path>` | **`446  0  <path>`** | the same command |
| 3 | AC-15 head binding | "the PR head is still `1aa632f7…`" | **the head is `87c637df…`; this plan does not move it** | `gh pr view 784 --json headRefOid`, `git rev-parse refs/pull/784/head` |
| 4 | §1 "the head is `1aa632f7…`" | `1aa632f7…` | **`87c637df…`** | `git cat-file -p 87c637df…` |
| 5 | §1 "The head has not moved … two commits" | 2 commits | **3 commits: `99d46d75…`, `1aa632f7…`, `87c637df…`** | `git rev-list --count e2a3e20b…87c637df…` → 3 |
| 6 | §2 "the head `1aa632f7…`'s only parent" | the head's parent = `99d46d75…` | **the head `87c637df…`'s only parent is `1aa632f7…`; `1aa632f7…`'s only parent is `99d46d75…`; the merge base is still `e2a3e20b…`** | `git cat-file -p` on each; `git merge-base 87c637df… origin/main` → `e2a3e20b…` |
| 7 | §1, §6 and §9, the record's blob | `af7a8502d2aed730da9befd45920fd0a08b9f06a` | **`cc460c0cd9fae1846046df65ffc36c6c5efe6157`** | `git rev-parse 87c637df…:<path>` |
| 8 | §1 the record's line count | 449 lines | **446 lines** | LF count of the blob: 446, CRLF 0 |
| 9 | §1 the record's sha256 | `705ebf145372c5f8653e690a59a67a1abb6245e7d0095602cd385fb204587fae` | **`6f02d168d47482bbad80dfbe71445052eec5ad0bc53bd06af0640ab6358c6c1a`** | sha256 over the blob's bytes |
| 10 | §1 the record's byte count | 38,937 | **38,937 — unchanged** | `git cat-file -s`: three removed newlines equal three inserted spaces |
| 11 | §4 "verifiable at the implementation head (`1aa632f7…`)" | `1aa632f7…` | **`87c637df…`** | this plan's own text |
| 12 | §9 stage receipts | "SD-B `6211504777`; SD-D `6209631818`; the rest owed" | **SD-D `ACCEPT` `6213714837` and SD-E `FAIL` `6213965761` are posted, both bound to `1aa632f7…` and therefore void at this head; a fresh SD-D and a fresh SD-E are owed** | the PR conversation, via the API |
| 13 | §12 Codex state block | `"has_unresolved_findings": true` **"at this head"** | **the block's `code_review.commit_sha` is `99d46d75…`** — the *first* head — so "at this head" was already imprecise; no Codex review has run at `1aa632f7…` or `87c637df…` (the bot posted a usage-limit notice) | the bot comment's embedded JSON, via the API |
| 14 | §10.1 "The head stays `1aa632f7…`" | "the head stays" | **the head moved at Stage C's repair round 2; this plan does not move it further** | the commit's committer timestamp |
| 15 | The record's own section line numbers (published alongside this plan) | §9 L317, §10 L331, §11 L361, §12 L369, §13 L384, §14 L410, §15 L424 | **§9 L314, §10 L328, §11 L358, §12 L366, §13 L381, §14 L407, §15 L421** | heading line numbers of the blob at each head. Headings §1-§8 are unchanged, because the join is inside §8's table at L308. **The plan cites the record by section number, not by line**, and its only line-level citations of the record are L3-24 (AC-3) and L6-10 (§10.1) — both above L308, so neither breaks |
| 16 | The PR body's structural-gate block | "all at the head `1aa632f7…`"; numstat `449 added, 0 deleted`; DCO "2 checked"; CI run `38872542401` | **head `87c637df…`; `446 added, 0 deleted`; DCO "3 checked, all signed off"; CI run `38891331698`** (created `2026-10-16T11:04:08Z`, conclusion success) | the API, and the commands in that block |
| 17 | The PR body's witness bound field | "Candidate head `1aa632f7…` … any move of it voids this record" | **text unchanged, and therefore now void on its own terms.** This plan does **not** edit it (§14) | the field's own sentence |

**What the sweep found beyond the two named criteria, stated plainly:** the record's blob and sha256
(items 7 and 9), the record's line count as a property of the change under plan (item 8), the commit
count and the parent chain (items 5 and 6), the stage receipts (item 12), the Codex block's actual
binding (item 13), the record's shifted section line numbers (item 15), and the PR body's gate block
(item 16).

**What the head move did *not* invalidate — re-measured here, not assumed.** The C-1 prevalence table
(at `87c637df…`: 292 / 107 / 38 / 31 over 654 reader pages; at the base: 291 / 106 / 37 / 30 over 653
— identical to revision 2's figures); the instrument's summary at the head
(`654 / 57 / 4 / 587 / 0 / 0 / 6 / 597`) and at the base (`653 / 57 / 4 / 586 / 0 / 0 / 6 / 596`), both
exit 0, with `--quiet` also exit 0 at each; `build_index.py --report`'s identical block
`101 / 101 / 81 / 10 / 68` at exit 0 for the base, `1aa632f7…` and `87c637df…` alike; the unread
sequence (**591** at the head, **590** at the base); the anchor path's 0-based position in it (**468**
at the head, **467** at the base); the eight next-batch paths, unchanged and in the same order; the
ledger blob `aa6acddf…` and the index blob `eeda4929…` (identical at the base, `1aa632f7…` and
`87c637df…`); the register blob `7947260b…`; the workflow blob `bff407a6…`; the skills-manifest blob
`d60fa564…`; and all sixteen page blobs in §1 and §6. **None of them moved.**

## 14. The bound fields, the PROC-04 digest, and the Stage A row this revision does not insert

**The published digest, re-derived.** The PR body states a PROC-04 digest over its three
sentinel-delimited bound fields: `77a6db9c7a5c31d0` (full
`77a6db9c7a5c31d0438afdf01aab5970ba741ea005431fc471a5927633c828e1`). Re-computed here from the live body
with the method `docs/delivery-workflow.md` L875-898 fixes — sentinels resolved by **whole-line equality**,
not by substring search; each field's payload taken strictly between its opening sentinel and the next
`end` sentinel, sentinels excluded; every run of whitespace collapsed to a single space and each field
trimmed; the three joined witness → skills → security with single newlines; `sha256` over the UTF-8
string with no trailing newline; first 16 hex published — **it reproduces exactly**, field for field
(witness 1,298 characters, skills 8,191, security 567). The repair round's earlier value
`e0d31bd3c7a7e796` does **not** reproduce against the live body, correctly: the body itself records it
as void once the Stage A rows were added to the skills field.

**What the digest binds, and the tension this revision must handle rather than ignore.** The `skills`
bound field's last four records are the Stage A `Row source` lines, each carrying
`target=captured plan revision 491bad103254d561054d631294d43a09db20493d` — the **revision-1** capture
those rows were produced against. The coordinator's ruling that the field stays was made **for
revision 2**, and this revision may not carry it over unexamined.

**Does a Stage A row for this revision belong? Yes — and it still must not be inserted here.** The
distinction is between *re-pointing* and *adding*. Re-pointing the four revision-1 rows at a later
revision would assert a skill application that did not occur — which is exactly why the field was left
alone for revision 2. **Adding** a row block for this revision asserts a skill application that **did**
occur: this planning session applied the same four Stage A skills to the moved head, so the
`skill-usage-ledger` obligation is not discharged for revision 3 without it. But the block belongs
**inside** the `skills` bound field, and the workflow is explicit that any change to a bound field
voids the verdict over it (L919-925). **So this revision does not edit the field.** The exact text is
authored below and the edit is left to whoever will republish the digest; both digest values are
stated.

**Old digest (published; reproduced above):** `77a6db9c7a5c31d0`.

**New digest if the row block below is appended to the `skills` field, immediately before its closing
`end` sentinel:** `f15e3d128da4cd52` — computed with the same normalization (PROC-04, named) over the
same three fields with only that block added.

**The exact row block to append** — four records, one per Stage A skill, mirroring the revision-1
block. The four skill sha256 values were re-read from `tools/skills-manifest.json` at `87c637df…`, whose
manifest blob `d60fa564…` is identical at the base, at `1aa632f7…` and at `87c637df…`:

<!-- ROWBLOCK-START -->
```text
<!-- Row source: agent=readability-phase4-lane-d-planner-a1 (DeepSeek-4.1-Flash (deepseek-flash)); stage=A; round=2; row=SA-5; target=captured plan revision 3, this revision's capturing commit and blob named in the PR body and the fresh capture comment; source=.claude/skills/change-classification-gate/SKILL.md, applied to re-classify this change docs-only before re-planning at the moved head 87c637df; binding=sha256 08d91a834460beebc9c66fa896b8b422f064bf1d7524f6e5b1512cda3afdc996 of that skill's SKILL.md bytes from tools/skills-manifest.json at 87c637df -->
<!-- Row source: agent=readability-phase4-lane-d-planner-a1 (DeepSeek-4.1-Flash (deepseek-flash)); stage=A; round=2; row=SA-6; target=captured plan revision 3, this revision's capturing commit and blob named in the PR body and the fresh capture comment; source=.claude/skills/acceptance-criteria-reviewer/SKILL.md, applied to re-check AC-1 to AC-15 against the moved head and correct the two criteria the head move falsified; binding=sha256 c6e5d5649bf89658036cf38abba9c626701220e7b00831c2d843ceff94d81021 of that skill's SKILL.md bytes from tools/skills-manifest.json at 87c637df -->
<!-- Row source: agent=readability-phase4-lane-d-planner-a1 (DeepSeek-4.1-Flash (deepseek-flash)); stage=A; round=2; row=SA-7; target=captured plan revision 3, this revision's capturing commit and blob named in the PR body and the fresh capture comment; source=.claude/skills/scoped-approval-register/SKILL.md, applied to re-read AEGIS-APR-101 and AEGIS-APR-117 at the moved head and restate the non-author test; binding=sha256 a74d2a22579cf93f737725aa0c54197b5d496a9f33a291a93c2cf2073cd7d076 of that skill's SKILL.md bytes from tools/skills-manifest.json at 87c637df -->
<!-- Row source: agent=readability-phase4-lane-d-planner-a1 (DeepSeek-4.1-Flash (deepseek-flash)); stage=A; round=2; row=SA-8; target=captured plan revision 3, this revision's capturing commit and blob named in the PR body and the fresh capture comment; source=.claude/skills/skill-usage-ledger/SKILL.md, applied to emit this revision's six-field skills record and state the row block this revision does not insert; binding=sha256 6a27b5c8e690b605d7dca4b0e4c2ff1d67dfa6ac6c18469d5657b4ff093339a4 of that skill's SKILL.md bytes from tools/skills-manifest.json at 87c637df -->
```
<!-- ROWBLOCK-END -->

**Two notes the inserter needs, so the block is not inserted blind.**

- **The `target=` value is exact as written, and is deliberately not a literal 40-hex.** The natural
  literal is this revision's capturing commit — and **this plan is inside that commit**, so the value
  cannot be known when the plan's bytes are fixed. The record therefore names the revision and the two
  publication sites that carry the commit and blob SHA, exactly as this plan's own capture reference
  does (§11). If the inserter prefers a literal SHA, substituting it **changes the digest again** and
  the value above becomes void: recompute with the same method and publish the new value.
- **`round=2`** is this Stage A capture's ordinal among the rounds that publish `Row source` records:
  revision 1 published the four `round=1` rows, revision 2 published none (the coordinator's ruling), and
  this revision is the second such round. The token is stated so the inserter can re-check it against
  the repository's convention rather than guess.

**Verbatim copy of this plan: the extraction method, declared.** The fresh capture comment holds the
plan inside a fenced code block **opened by a line of four backticks followed by the info string
`text`, and closed by a line of four backticks.** **Four, not three, and that is load-bearing:** this
plan's own bytes contain two three-backtick fences (its §3 classification block and its §14 row block),
so a three-backtick outer fence would close early and the "copy" would silently be a prefix — the exact
class of error this verification exists to catch. The declared method: **take the comment body; find
the line that is exactly ````text and the next line that is exactly ````; take the lines strictly
between them; join those lines with a single LF after each and terminate the result with one LF; then
`git hash-object -t blob --path docs/plans/readability-lane-d-batch3-plan-2026-10-16.md <extract>` must
return this plan's blob SHA itself.** A method that matches the fence by substring, that uses a
three-backtick fence, or that normalises the final newline is **not** this method and its result is not
comparable — the rule that a republished figure names its method applies here too (PROC-04). This
plan's bytes end with exactly one LF, so the extract that matches is the one that keeps it. **This is
stated rather than assumed because a prior revision of this plan's sibling claimed a verbatim copy that
did not exist, and a later one dropped the final newline.** The result is stated in the PR body and the
fresh comment, since the comment is posted after this plan's bytes are fixed.

## 15. Timing

- **Start (plan revision 1):** 2026-10-16T02:14:37-07:00 (America/Los_Angeles; the turn-1 snapshot of
  that planning session).
- **Finish (plan revision 1):** 2026-10-16T02:29:57-07:00 — the creation time of the verbatim capture
  comment `6212482822` (`2026-10-16T09:29:57Z`), the last publication act of that capture. The
  capturing commit `491bad103254d561054d631294d43a09db20493d` is a few seconds earlier, at
  `2026-10-16T02:29:26-07:00` by its own committer timestamp; both instants are stated because both are
  finish instants of the same capture — commit first, comment second.
- **Wall time (plan revision 1):** **15m 20s** from the stated start `02:14:37` to the finish
  `02:29:57`; **14m 49s** from the start to the capturing commit `02:29:26`. Both are **measured
  wall time**; **active time is not instrumented**, so wall time is an imperfect comparison and no
  active-time split is claimed. *Derivation — the values are stated here and are re-derivable, not a
  pointer to somewhere else:* the start is that session's own turn-1 snapshot, recorded in revision 1
  of this plan; the two finish instants are read from the repository and the API —
  `git log -1 --format=%cI 491bad103254d561054d631294d43a09db20493d` → `2026-10-16T02:29:26-07:00`,
  and `gh api repos/ModernNomad-98/Project-Aegis/issues/comments/6212482822 --jq .created_at` →
  `2026-10-16T09:29:57Z`.
- **Start (plan revision 2):** 2026-10-16T02:59:36-07:00 (the turn-1 snapshot of that session).
- **Finish (plan revision 2):** 2026-10-16T03:04:26-07:00 — the creation time of the verbatim capture
  comment `6213082533` (`2026-10-16T10:04:26Z`). Its capturing commit
  `b8f91cfe504a11119cb23c642db373fb8b55df83` is earlier, at `2026-10-16T03:03:38-07:00` by its own
  committer timestamp.
- **Wall time (plan revision 2):** **4m 50s** from `02:59:36` to `03:04:26`; **4m 2s** to the capturing
  commit `03:03:38`. Measured the same way as above. **These are stated directly here**, because
  revision 2 left its own figures to the comment and the PR body, and the rule finding **B-2**
  established for revision 1 — that a revision's timing is stated in the plan, not pointed at —
  applies to every revision of it.
- **Start (plan revision 3, this text):** 2026-10-16T04:07:51-07:00 (the turn-1 snapshot of this
  session).
- **Finish and wall time (plan revision 3):** these necessarily fall **after** this commit exists, so
  they are stated in the fresh capture comment and in the PR body's capture section, which carry the
  comment's creation time, the capturing commit's own committer timestamp and both wall figures. The
  reason they cannot appear in these bytes is stated rather than hidden: **the plan is inside the
  commit that would supply its own finish instant.** They are re-derivable from
  `git log -1 --format=%cI <capturing commit>` and
  `gh api repos/ModernNomad-98/Project-Aegis/issues/comments/<fresh comment id> --jq .created_at`.
- **Identity and environment:** written on a fresh HTTPS clone
  (`git clone -c http.sslBackend=openssl`) outside the shared clone, with `git config user.name` =
  Peter Nguyen; no `wt-*` worktree created; nothing merged.

---

*Prepared by a **DeepSeek agent** (**DeepSeek-4.1-Flash**, `deepseek-flash`) operating under the owner
account, as the repository's attribution rule (2026-10-13) requires, holding **Stage A only**.*
