# Readability Phase 4 re-read lane D — batch 1 record, 2026-10-15

- **Lane:** PHASE 4 RE-READ LANE D (full-page independent re-reads of the lane's fixed page range).
  **Stage:** C (IMPLEMENT). **Base:** `e2a3e20b7c20ef8385b219b39c6405237163406f` (`origin/main`, the
  PR #769 merge; equal to the lane's derivation base).
- **Plan applied:** the coordinator's lane-D brief of 2026-10-15. No separate plan artifact exists for
  this lane; the brief's own derivation rule ("take the pending set from `check_index.py`, sort the
  paths, take your quarter") is the plan of record, and this record states every step it took from it.
- **What this page is.** The lane's tracked batch record. It is the **evidence source** every keeper
  row this lane appends to the ledger's consolidated keeper table cites, so the ledger's `Quote`
  column can hold a verbatim fragment of a tracked page, and it **names every row's full 40-character
  acceptance revision verbatim** in its own bytes (section 10).
- **Acceptance revision bound by all eight rows of this batch:**
  `e2a3e20b7c20ef8385b219b39c6405237163406f`
  That revision resolves to itself and is contained in `refs/remotes/origin/main`
  (`git merge-base --is-ancestor e2a3e20b7c20ef8385b219b39c6405237163406f refs/remotes/origin/main` exits 0).
- **The lane changed none of the eight read pages.** So the bytes this record read are the bytes the
  merge receives, and the acceptance is not voided by the merge.

## 1. The instrument's figures at the base, quoted

```text
python -P tools/readability_acceptance/check_index.py --json --ref refs/remotes/origin/main
compared_ref e2a3e20b7c20ef8385b219b39c6405237163406f, reader_pages_in_tree 653,
accepted_on_recorded_review 57, provably_pending 4, no_recorded_acceptance 586,
recorded_acceptance_within_10_lines 0, within_10_not_covered_by_targeted_review 0,
cannot_decide 6, official_pending_count 596
exit 0
```

**This lane publishes no readability count of its own** (ledger L19-31; decision D84 — the
official count is the instrument's computed figure, not the ledger's own) and presents the figures
above as the instrument's, not as its own measurement.

## 2. The lane derivation, stated with its command

1. The pending set is the instrument's `no_recorded_acceptance` (586) plus `provably_pending` (4)
   buckets: **590 paths**, derived by replicating `check_index.py`'s own `classify_tree`
   (tracked `.md` at the ref, minus the `scripts/` fixtures except
   `scripts/tests/fixtures/README.md`, minus the one generated report) and subtracting the paths the
   committed `acceptance-index.json` carries rows for. The 4 provably-pending paths were taken from
   the same command's `pending` array. Command: `python -P tools/readability_acceptance/check_index.py
   --json --ref refs/remotes/origin/main` plus a Python script over its output, saved with the lane.
2. The 590 paths were **sorted**, then split into **four contiguous quarters by count**
   (148 / 148 / 148 / 146). **Lane D takes the last quarter: 146 pages, first**
   `docs/evidence/documentation/full-page-readability-batch-after-233-2026-09-24.md`, **last**
   `tools/behavioral_eval_runner/README.md`.
3. **Declared divergence from the brief's gloss, read honestly.** The brief describes lane D as "the
   pages whose path sorts T through Z". That letter-based reading is not the quarter the brief's own
   rule produces: only **3** of the 590 pending paths sort at or after "t" (all under `tools/`), while
   the last quarter is 146 paths. The operative rule in the same sentence is "sort the paths, and take
   your quarter", so **the last contiguous quarter is taken**, and its first and last path are stated
   here and in the pull-request body so the other three lanes can hold disjoint contiguous quarters.
4. **Batch 1 = the first 8 of lane D in sorted order** (the ledger's representative-batch guidance of
   eight to ten pages), re-checked against the instrument at the base immediately before writing: all
   eight sit in `no_recorded_acceptance` at `e2a3e20b`, so none is already accepted and none is
   outside the lane's range.

## 3. The roster, the concurrency, and the declared deviation

One reader (`readability-phase4-lane-d-implementer-c`) read all eight pages. **Declared deviation,
reported not hidden:** the ledger's 2026-10-12 remaining-page batch already recorded that its single
agent performed all reader passes *and* wrote the lane's ledger section, with the first
reader-independence clause satisfied (the lane wrote none of the read pages) and the second not. This
lane has the same structure and records the same fact: the first clause **is** satisfied — this lane
wrote none of the eight pages (each is a dated record of a 2026-09-23, 2026-09-24 or 2026-10-10 batch
authored by other agents) — and the second is **not**, because the same agent writes this lane's
ledger section and appends the keeper rows. Carried into the pull-request body.

## 4. Per-page dispositions — eight full-page re-reads, zero edits (seven accepted unchanged, one partial)

Every page below was read **whole** at `e2a3e20b`. None has a recorded acceptance, so drift has no
recorded acceptance revision to diff against (`not derivable`, the same wording the after-713 record
used for its no-recorded page).

| # | Page | Recorded acceptance | Drift | Disposition | Reader |
| --- | --- | --- | ---: | --- | --- |
| LD-1 | `docs/evidence/documentation/full-page-readability-batch-after-233-2026-09-24.md` | none (no-recorded bucket) | not derivable | **accepted unchanged** | `readability-phase4-lane-d-implementer-c` |
| LD-2 | `docs/evidence/documentation/full-page-readability-batch-after-234-2026-09-24.md` | none (no-recorded bucket) | not derivable | **accepted unchanged** | `readability-phase4-lane-d-implementer-c` |
| LD-3 | `docs/evidence/documentation/full-page-readability-batch-after-713-2026-10-10.md` | none (no-recorded bucket) | not derivable | **accepted unchanged** | `readability-phase4-lane-d-implementer-c` |
| LD-4 | `docs/evidence/documentation/full-page-readability-sample-2026-09-23.md` | none (no-recorded bucket) | not derivable | **partial** — `D9` at page L30 unglossed (acceptance bullet 2) | `readability-phase4-lane-d-implementer-c` |
| LD-5 | `docs/evidence/documentation/governance-poisoning-routing-correction-2026-09-23.md` | none (no-recorded bucket) | not derivable | **accepted unchanged** | `readability-phase4-lane-d-implementer-c` |
| LD-6 | `docs/evidence/documentation/historical-evidence-reading-2026-09-23.md` | none (no-recorded bucket) | not derivable | **accepted unchanged** | `readability-phase4-lane-d-implementer-c` |
| LD-7 | `docs/evidence/documentation/legacy-prompts-current-reading-2026-09-23.md` | none (no-recorded bucket) | not derivable | **accepted unchanged** | `readability-phase4-lane-d-implementer-c` |
| LD-8 | `docs/evidence/documentation/legacy-roadmap-ber-design-readability-2026-09-23.md` | none (no-recorded bucket) | not derivable | **accepted unchanged** | `readability-phase4-lane-d-implementer-c` |

No page needed a fix, so no page was edited: the no-rewrite discipline forbids edits to dated records,
and the four observations below (section 8) are recorded rather than rewritten in place.

LD-4's verdict is **partial**, not accepted unchanged: acceptance bullet 2 (abbreviations and coded
identifiers defined at first use) fails — the coded identifier `D9` (owner decision 9) appears at
page L30 with no on-page gloss (observation O-2), verified with `git show
e2a3e20b:docs/evidence/documentation/full-page-readability-sample-2026-09-23.md` (`D9` occurs exactly
once, at L30). LD-4 is recorded honestly as a **partial** acceptance, and the full-page-acceptance
keeper row K-093 (this lane's keeper-table row for LD-4) **does not stand as authored** — PR #787
(the open AEGIS-APR-117 withdrawal pull request, head
`1419d480e0c2f90ccb62cd4f491ae2b8c4aa676d`, verified with `git fetch origin refs/pull/787/head`)
appends withdrawal row K-392W on its branch and records LD-4 PARTIAL, leaving it pending; on main,
K-093's lineage is already cancelled by withdrawal row K-384W (merged PR #781). The eight rows stay
in the keeper table as authored so the main-side withdrawal lineage stays aligned — the same shape
PR #771 used for its P8/K-089 partial page. Section 18 records the commands behind this.

## 5. Depth records

**Every line of every page was read as prose, at the declared revision.** The eight pages are 71 + 44
+ 56 + 54 + 63 + 24 + 41 + 38 = **391 lines** in total (largest page 71 lines), extracted from the
exact revision with `git show e2a3e20b:<page>` and read with line numbers. **No display elision
occurred and no range was skipped**: each page fit a single read pass, so the read depth is the whole
page for all eight — there is no unchanged remainder limit to state here, unlike the 2026-10-12
batch's large pages.

**The mechanical pass** ran over the same exact-revision bytes. For each page it enumerated: every
Markdown link (local and external) and every in-page anchor target; every 40-character SHA; every
7-12 hex token inside backticks; and coded identifiers by the stated pattern
`\b(?:[A-Z]{2,8}-\d{1,4}|D\d{2,3}|PR\s*#\s*\d{1,4}|#\d{3,}|K-\d{3}|L-\d{3}|T-\d{3}|AC\d{1,2})\b`.

| Page | Local links resolved | External links (not fetched) | Broken links | Bad anchors | 40-hex SHAs | Unresolvable 40-hex | 7-12 hex backtick tokens | Not resolving | Coded identifiers |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| LD-1 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| LD-2 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| LD-3 | 1 | 0 | 0 | 0 | 1 | 0 | 3 | 0 | 0 |
| LD-4 | 12 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| LD-5 | 6 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LD-6 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LD-7 | 4 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| LD-8 | 2 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |

External links (git-scm.com x2 on LD-5, github.com x1 on LD-6) were **not fetched**, matching the
2026-09-23 sample's own recorded practice ("external links were not fetched"). The six forty-hex
SHAs are the base/merge revisions each note cites, and every one resolves in the local object store
at `e2a3e20b`; the six merge SHAs were additionally verified against their pull-request subjects:
`b545d075` = "Merge pull request #233 from ModernNomad-98/docs/checkpoint-after-232",
`5c46c7b3` = "Merge pull request #234 from ModernNomad-98/docs/skill-references-after-233-readable",
`2c6b6fc6` = "Merge pull request #713 from ModernNomad-98/docs/readability-tenth-batch-20261010",
`6051ab0a` = "Merge pull request #205 from ModernNomad-98/docs/evidence-reading-clarity",
`e6148322` = "Merge pull request #173 from ModernNomad-98/docs/skill-references-final-16-readable",
`a8b81d49` = "Merge pull request #190 from ModernNomad-98/docs/agent-contributor-docs-readable". LD-3's three backtick tokens are
`2c6b6fc6`, `518b0b38` (twice) and all resolve.

## 6. The six acceptance bullets, addressed for each of the eight pages

**(a) Purpose and audience up front.** LD-1/LD-2/LD-3 open with the batch title and its exact base
merge (L1-4); LD-4 and LD-5 carry an explicit "Current reading" banner routing to the live artifacts
(LD-4 L3-8, LD-5 L3-9) and LD-4 names the maintainer audience (L10-11); LD-6 opens "This note helps
maintainers read..." (L3-4); LD-7 and LD-8 open with the current-reading route (LD-7 L3-6) and the
reading-keys purpose (LD-8 L1). **(b) Abbreviations and coded identifiers defined at first use.**
"pull request (PR)" is expanded at first use on LD-1 L3, LD-2 L3, LD-3 L3; "Coordinated Universal
Time (UTC)" on LD-4 L12, LD-5 L25, LD-6 L6-7, LD-7 L6, LD-8 L3; LD-6 and LD-7 spell out "Pull
request" in full (LD-6 L10, LD-7 L9). The one identifier not glossed on its page is LD-4's `D9` at page L30
(observation O-2 below) — a failure of acceptance bullet 2, so LD-4's disposition is **partial**
(section 4), recorded not repaired. **(c) Descriptive headings, lists or tables, and concrete examples.** LD-1,
LD-2, LD-3 and LD-4 are headed records with disposition tables; LD-5, LD-7 and LD-8 use headed
sections and lists; concrete worked content sits on LD-5 (the `git revert` and `A..B`
explanations, L31-49) — a dated evidence note's concrete content is its recorded work, not an
abstract component. **(d) Shipped behaviour separated from proposed or blocked behaviour.** LD-1
closes with "Exact-head Actions and merge remain outstanding." (L68); LD-2 closes with
"Exact-head GitHub Actions and merge remain delivery gates." (L41); LD-3 states no page was edited and
the acceptance binds to the reviewed head (L45-47); LD-4 states the batch "does not accept the other
tracked Markdown files... or grant execution authority" (L50-53); LD-5 states "This note does not
claim that any revert or live incident operation was run" (L49-50); LD-6 "The edits clarify historical
evidence. They do not change test results, skill contracts, owner grants, live-execution gates or the
current backlog" (L23-24); LD-7 "A historical page supplies no implementation, provider, private-input,
host or approval authority" (L29-30); LD-8 "No runtime, provider, private-input, approval,
design-schema or skill contract change is made" (L23-24). **(e) Navigation links current; every
referenced file or command exists.** Section 5's mechanical pass: 30 local links, zero broken paths,
zero bad anchors across all eight pages; named commands (`git revert`,
`python scripts/validate-skills.py`, `git diff --check`) exist as git builtins or at the named
script path at the base. **(f) The non-author review itself.** This record, with the deviation
declared in section 3: this lane wrote none of the eight pages.

## 7. Purpose and normal use restated from each page alone

- **LD-1** — *for:* recording which of 40 skill reference pages the after-#233 batch corrected and
  why. *Normal use:* read it as a dated disposition table of that batch; the live acceptance state is
  the documentation ledger it links.
- **LD-2** — *for:* the same for the 18 pages of the after-#234 batch. *Normal use:* dated
  disposition table; follow its checklist link for the live rule.
- **LD-3** — *for:* the two-page eleventh sweep batch (the after-712 record and the ledger's own
  re-pend), including its derivation. *Normal use:* dated batch evidence; its tracker line anchors are
  dated (observation O-1).
- **LD-4** — *for:* the representative nine-page acceptance sample and its measured intervals.
  *Normal use:* historical measurement sample for the estimate rule; its "current reading" banner
  routes to the live forecast and ledger.
- **LD-5** — *for:* the revert-routing and live-incident-routing correction of two governance skills.
  *Normal use:* read the banner for where the live instructions live; the body is retained evidence.
- **LD-6** — *for:* how to read the 2026-09-12 shared-contract and BER recovery evidence. *Normal
  use:* a maintainer reads it before those records to know what the corrections clarify.
- **LD-7** — *for:* the legacy skill-plans current-reading notes. *Normal use:* explains the
  historical status of seven legacy pages and where their live successors are.
- **LD-8** — *for:* the historical roadmap and BER v1 design reading keys. *Normal use:* explains
  what the dated design and roadmap pages are, and routes current status to the owning backlog.

## 8. Observations — read and dispositioned, none edited in place

Row shape: `stale:` the exact text as it stands at the declared revision; `new:` `unchanged`;
`source:` the artifact that settles it.

| # | stale | new | source |
| --- | --- | --- | --- |
| O-1 | LD-3 L25-26 and L28-29 cite "tracker L2941–2947" and "tracker L2801" for the up-to-three structure and the non-author rule. At `e2a3e20b` L2941-2947 holds the denominator paragraph and L2801 the self-cost note; the cited texts sit at L3002 (paragraph L3000-3006) and L2860-2862. | **unchanged** — a dated 2026-10-10 record is a snapshot and is never rewritten (the 2026-10-12 close-out's disposition row D-5: stale anchors in dated records stay unchanged, never rewritten). | `git show e2a3e20b:docs/roadmaps/aegis-documentation-readability-backlog.md` lines read at those anchors. |
| O-2 | LD-4 L30 "Reconciled the 30-day evidence-policy choice, schema-shape and D9 decisions" uses `D9` without a gloss. `D9` is owner decision 9, recorded in the decisions log. | **unchanged** — the code resolves in `docs/reconciliation/step-0-reconciliation-v4.md` L941 ("D9 (2026-07-06) — A Compliance & Governance batch"), and the page is a dated record. The unglossed `D9` fails acceptance bullet 2, so LD-4's disposition is **partial** (section 4), recorded not repaired — the gap is stated, never filled silently. | `step-0-reconciliation-v4.md` L941, read at the base. |
| O-3 | LD-3 L6-7 name the plan artifacts `PLAN-first-batch.md 4eeaf8aa…`, `AUDIT-B ca7e3b9f…`, `STAGE0 8cbd113f…`. The three 8-hex prefixes do not resolve in the local object store. | **unchanged** — they name the 2026-10-10 sweep's plan artifacts outside the tree, the same shape the 2026-10-12 record used for its plan evidence sha256 (outside git). | `git cat-file -t 4eeaf8aa` / `ca7e3b9f` / `8cbd113f` each exit non-zero at the base. |
| O-4 | LD-5 L59 "all **seven local links** resolved" is the note's own 2026-09-23 figure; the page at `e2a3e20b` carries six local links. | **unchanged** — the historical sentence describes the page at its own revision; today's six links all resolve (section 5). | `git show e2a3e20b:<LD-5>`; the mechanical pass's link count. |

Zero rows above have an empty source.

## 9. Count honesty

- **This lane publishes no readability count of its own** and cites the instrument, as the D84 switch
  requires. The instrument classifies the **page tree at `--ref`** and reads the recorded
  acceptances from the **committed index JSON**, so **the eight appended rows change nothing until a
  rebuild**, and the builder can only be rebuilt after the commit that carries the rows because it
  stamps its own `built_at_ref`. The two resolvers the ledger already names apply: a two-commit
  follow-up, or a merger-side rebuild at the merged tip (decision D73 row 8 — the recorded
  practice for a moved main). `build_index.py --write` is
  **not** run in-lane: a rebuild adds JSON under `tools/`, which is not Markdown, and would break
  this change's `docs-only` tier; the rebuild itself is the standing AEGIS-APR-115 (the register
  grant for routine index-rebuild pull requests) rebuild pull request's own scope.
- **The only movement at this lane's head is this lane's own new reader page**, which enters
  `no_recorded_acceptance` and therefore the official pending count. The published head expectation
  is **654 / 57 / 4 / 587 / 0 / 0 / 6 / 597** — the base's 653 / 57 / 4 / 586 / 0 / 0 / 6 / 596 with
  **+1 reader page, +1 no_recorded_acceptance and +1 official pending count**, all three attributed to
  this page. **No post-rebuild count is predicted.**

## 10. The row-quote strings, verbatim

Each line below appears in this file byte-for-byte and is copied verbatim into the ledger row whose
stable ID shares the same label. Every line contains the full 40-character acceptance revision.

```text
LD-1 accepted: docs/evidence/documentation/full-page-readability-batch-after-233-2026-09-24.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
LD-2 accepted: docs/evidence/documentation/full-page-readability-batch-after-234-2026-09-24.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
LD-3 accepted: docs/evidence/documentation/full-page-readability-batch-after-713-2026-10-10.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
LD-4 accepted: docs/evidence/documentation/full-page-readability-sample-2026-09-23.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
LD-5 accepted: docs/evidence/documentation/governance-poisoning-routing-correction-2026-09-23.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
LD-6 accepted: docs/evidence/documentation/historical-evidence-reading-2026-09-23.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
LD-7 accepted: docs/evidence/documentation/legacy-prompts-current-reading-2026-09-23.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
LD-8 accepted: docs/evidence/documentation/legacy-roadmap-ber-design-readability-2026-09-23.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
```

The LD-4 line's row K-093 (full-page-acceptance) does not stand as authored — LD-4's disposition is
**partial** (section 4), and on main the row lineage is cancelled by withdrawal row K-384W (merged
PR #781) with the re-record withdrawn by PR #787's K-392W (section 18). The line is kept
byte-identical because the row remains in the keeper table as authored until that main-side
withdrawal lineage completes — the same shape PR #771 used for its P8/K-089 partial page.

## 11. Verification commands (run at the head; outputs in the pull-request body)

`build_index.py --ref <head> --report`, `check_index.py --ref <head> --quiet`, the changed-path
Markdown link check, `scripts/validate-skills.py`, `scripts/tests/test_validator.py`,
`git diff --check`, the ledger numstat additions-only check, the per-row checks (revision resolves
to itself and is main-contained, quote verbatim in this evidence source and names the revision
verbatim, blob ID equals `git rev-parse <revision>:<page>`, path tracked), and
`scripts/check_dco.py --range origin/main..HEAD`.

## 12. What this lane did not do

It edited none of the eight read pages (no-rewrite discipline); rewrote no dated snapshot; edited,
reordered or deleted no existing keeper row; bound no acceptance row to the lane's own unmerged head;
ran no `build_index.py --write` and rebuilt no `tools/` artifact; touched no page outside the
lane's stated range; and claims no authority beyond recording under AEGIS-APR-101 (the ledger-
keeper recording role) and the standing backlog delivery grant AEGIS-APR-039. The batching
procedure does "not mark earlier screens as full-page acceptance or grant provider, private-input,
real-host or deployment authority" (ledger L3018-3020).

## 13. Skills used (this lane, Stage C)

`change-classification-gate` — classified the change `docs-only` (evidence record + ledger
additions, Markdown only) before writing, which is what keeps the lighter review path applicable and
the diff inside the no-code tier. `acceptance-criteria-reviewer` — used inside its contract: the
ledger's six acceptance bullets are criteria, and each is addressed with line cites rather than
asserted (section 6). That skill returns one verdict per criterion and states that it "never decides
whether work is done", so the accept/partial dispositions are the lane's own recorded decision
(section 4), not this skill's output.
`source-of-truth-reconciler` — the four observations resolved against the repository (stale anchors,
the `D9` decision, the non-resolving plan tokens, the historical link count) instead of against the
pages' own prose. `scoped-approval-register` — established this change records under
AEGIS-APR-101 (the ledger-keeper recording role), performs backlog work under AEGIS-APR-039 (the
standing backlog delivery grant), and consumes, extends and requests no grant; the index rebuild
is AEGIS-APR-115's separate scope (the register grant for routine index-rebuild pull requests),
not this change's. `docs-retention-index`
— consulted; no retention entry or frontmatter mechanism exists for
`docs/evidence/documentation/` pages (zero files there carry `retention:` frontmatter at the
base), so the new page follows the established shape and creates no retention row; recorded as
checked-and-not-applicable. `skill-usage-ledger` — the six-field records in this section, bound to
the skills-manifest hashes.

```text
skill@08d91a834460beebc9c66fa896b8b422f064bf1d7524f6e5b1512cda3afdc996 / reason: classify before writing, the class decides the tier and review path / applied: classified docs-only before any write / result: docs-only tier asserted in the PR body with the file set / incomplete: None / by: readability-phase4-lane-d-implementer-c (Stage C)
skill@c6e5d5649bf89658036cf38abba9c626701220e7b00831c2d843ceff94d81021 / reason: the acceptance contract's six bullets are criteria and were checked one by one / applied: each bullet per page with line cites in section 6 / result: the six bullets checked as criteria; this skill issued no acceptance verdict — its contract states it "never decides whether work is done" — so the 7/8 accepted unchanged, 1/8 partial dispositions are the lane's own recorded decision (section 4) / incomplete: None / by: readability-phase4-lane-d-implementer-c (Stage C)
skill@b5fd9feda97235430259913aedd33447ab06e1c0ded281e9e131fa6bf9b78be2 / reason: four page items needed resolution against the repo, not the page's prose / applied: observations O-1..O-4 sourced to repo artifacts / result: all four dispositioned unchanged / incomplete: None / by: readability-phase4-lane-d-implementer-c (Stage C)
skill@a74d2a22579cf93f737725aa0c54197b5d496a9f33a291a93c2cf2073cd7d076 / reason: recording requires knowing which grant covers what / applied: read AEGIS-APR-039, -101, -113..-118, -125, -129 at the base (register entries; one-line descriptions in section 17) / result: recording-only under APR-101; no grant consumed, extended or requested / incomplete: None / by: readability-phase4-lane-d-implementer-c (Stage C)
skill@141b7036469f9f99ef6b8e152299619a6d0ab572656a5ba307062551d311d8a5 / reason: a new page may owe a retention entry / applied: checked for a retention registry and per-doc frontmatter practice / result: none exists for this directory; no retention change needed, recorded not skipped / incomplete: None / by: readability-phase4-lane-d-implementer-c (Stage C)
skill@6a27b5c8e690b605d7dca4b0e4c2ff1d67dfa6ac6c18469d5657b4ff093339a4 / reason: the repository requires the skills-used record where a reader can see it / applied: emitted this six-field block bound to the manifest hashes / result: record present in this file and mirrored in the PR body's skills field / incomplete: None / by: readability-phase4-lane-d-implementer-c (Stage C)
```

## 14. Timing

- Lane ETA given to the owner: 8-12 hours for the whole lane. Batch-1 work start recorded at
  **2026-10-15T11:12:42-07:00** (the lane's start timestamp).
- The eight page reads ran after the lane derivation, beginning 2026-10-15T11:16-07:00
  (approximate, from the recorded step timestamps) and finished 2026-10-15T11:22-07:00
  (approximate); active time was **not instrumented**, so wall time is an imperfect comparison with
  the estimate rule's active-time requirement and no per-page active rate is claimed.
- Batch-1 finish and full wall time were **not recorded** — the lane's session record carried neither, and this record does not invent them (gap stated, not filled). The fourth-round repair item's own start, finish and wall time are recorded in section 18 and in the pull-request body.

## 15. Stage D repair note (2026-10-15)

The Stage D audit returned **REVISE** on this pull request with two P3 factual citation errors inside
this record. Both are repaired in place at this lane's second head (the record is unmerged, so in-place
repair is allowed; after merge a dated record can only be superseded). **The two corrections, with the
commands behind them:**

1. **Section 5 count word.** The record said "the four merge SHAs" and then listed six. All six facts
   are correct — `git show -s --format=%s b545d075 5c46c7b3 2c6b6fc6 6051ab0a e6148322 a8b81d49` prints
   "Merge pull request #233 from ModernNomad-98/docs/checkpoint-after-232",
   "Merge pull request #234 from ModernNomad-98/docs/skill-references-after-233-readable",
   "Merge pull request #713 from ModernNomad-98/docs/readability-tenth-batch-20261010",
   "Merge pull request #205 from ModernNomad-98/docs/evidence-reading-clarity",
   "Merge pull request #173 from ModernNomad-98/docs/skill-references-final-16-readable",
   "Merge pull request #190 from ModernNomad-98/docs/agent-contributor-docs-readable" — so the count word now says
   **six**, matching the six listed subjects.
2. **Observation O-1 anchor.** The record said the cited texts sit at "L2900-2905 and L2860-2862".
   L2860-2862 is correct. L2900-2905 is wrong: at `e2a3e20b` it holds the 61-requests measurement-gap
   paragraph, while the up-to-three-read-only-agents text sits at **L3002** (paragraph L3000-3006),
   verified with `git show e2a3e20b:docs/roadmaps/aegis-documentation-readability-backlog.md` and a grep
   for the phrase. The row's quoted tracker range is now byte-verbatim too: the page prints an en dash
   ("tracker L2941–2947", LD-3 L25), where the row had quoted a hyphen.
3. Every other figure in this record was re-verified against the artifact at the bound revision
   `e2a3e20b` — the section 1 instrument figures (653 / 57 / 4 / 586 / 0 / 0 / 6 / 596), the 590-path
   lane derivation (586 + 4, split 148 / 148 / 148 / 146, lane D first and last path, "3 of 590 sort at
   or after t"), the per-page depth and mechanical table (391 lines, 30 local links, 6 resolving 40-hex
   SHAs, 3 external links not fetched), the six merge-SHA subjects, the section 10 quote strings
   (verbatim in the eight appended ledger rows), and the eight row blob IDs (each 40 hex, each equal to
   `git rev-parse e2a3e20b:<page>`) — all unchanged and correct, so nothing else was edited in the
   first round. **Narrowed by the Stage D REVISE (second round):** that re-verification missed two
   quotations — the section 6(d) LD-1/LD-2 closing-phrase quotation and the section 12
   batching-procedure quotation — which the second round found wrong; both are corrected at the
   lane's third head in the second-round note below, and nothing else was edited there either.

**Keeper rows.** This repair authors no keeper row and withdraws none. The withdrawal of the same-agent
rows K-090..K-097 (the keeper-table row IDs this lane appended) and their re-recording by a separate
eligible keeper is **PR #781**'s scope (its record is
`docs/evidence/documentation/readability-apr117-withdrawals-and-rerecord-2026-10-15.md`, the
AEGIS-APR-117 route (the grant that lets the ledger keeper append withdrawal rows) the owner
directed on 2026-10-15).

*Repair drafted by **DeepSeek v4 Pro** (`deepseek-v4-pro`), the Stage D repairing agent, under the owner
account, as the repository's 2026-10-13 attribution rule requires.*

## 16. Stage D REVISE repair note, second round (2026-10-15)

The Stage D audit's second round returned **REVISE** on this pull request with three further P3
citation/gloss errors inside this record. All three are repaired in place at this lane's third head
(the record is still unmerged, so in-place repair remains allowed). **The three corrections, with
the commands behind them:**

1. **Section 6(d) closing-phrase quotation.** The record said LD-1/LD-2 close with "Exact-head
   Actions and merge remain delivery gates". That string is verbatim on neither page, verified with
   `git show e2a3e20b:<page>` and substring checks: LD-1 L68 closes "Exact-head Actions and merge
   remain outstanding." and the phrase "delivery gates" occurs nowhere in LD-1, while LD-2 L41
   closes "Exact-head GitHub Actions and merge remain delivery gates." — the record had omitted the
   word GitHub. Section 6(d) now quotes each page's actual closing phrase separately, each with its
   own line cite (LD-1 L68, LD-2 L41).
2. **Section 12 batching-procedure quotation.** The record quoted "does not grant provider,
   private-input, real-host or deployment authority" (ledger L3018-3020), eliding material without
   an ellipsis. At `e2a3e20b` L3018-3020 reads "This batching procedure is a work plan. It does not
   mark earlier screens as full-page acceptance or grant provider, private-input, real-host or
   deployment authority." — verified with `git show
   e2a3e20b:docs/roadmaps/aegis-documentation-readability-backlog.md`. The record now quotes the
   contiguous fragment "not mark earlier screens as full-page acceptance or grant provider,
   private-input, real-host or deployment authority". The ledger's own pre-existing dated sections
   (L4746, L4910) quote the elided form identically; they are dated sections the no-rewrite
   discipline protects, and they are **not** edited.
3. **The AEGIS-APR-117 label.** The keeper-rows paragraph named "the AEGIS-APR-117 route" without a
   plain-English description. It now reads AEGIS-APR-117 (the grant that lets the ledger keeper
   append withdrawal rows) — the same gloss the pull-request body carries and the register's own
   heading states ("The ledger keeper may append withdrawal rows after the switch",
   `docs/approvals/APPROVAL_REGISTER.md` L5016 at the base).
4. **Base note (recorded, not repaired):** `origin/main` has moved since the lane's derivation
   base `e2a3e20b` (the PR #769 merge). It is now `7abb98eb88ec3253521ab4ff5418d225413bd193`
   (the PR #770 merge, "docs/apr-137-phase1-transcription"). The lane's base binding and every
   figure in this record are unchanged, and the branch's own two files stay insert-only against the
   base (`git diff --numstat e2a3e20b HEAD`: 316/0 record, 59/0 ledger, 0 deleted lines). Against
   the moved main the same diff carries 190 deleted lines in three files
   (APPROVAL_REGISTER.md 137, delivery-workflow.md 24, open-decisions 29) — all of them main-side
   additions from PR #770, none written by this lane; reconciling that divergence is the merger's
   decision, not this repair's.

**Keeper rows.** This second-round repair authors no keeper row and withdraws none — the same
statement the first-round note makes, restated for the third head: the withdrawal of K-090..K-097
and their re-recording by a separate eligible keeper remain **PR #781**'s scope.

*Repair drafted by **DeepSeek v4 Pro** (`deepseek-v4-pro`), the Stage D repairing agent (second
round), under the owner account, as the repository's 2026-10-13 attribution rule requires.*

## 17. Stage D REVISE repair note, third round (2026-10-15)

The Stage D audit's third round returned **REVISE** on this pull request with two P3 findings in the
citation/gloss class — one against the pull-request body, one inside this record. Both are repaired
at this lane's fourth head (the record is still unmerged, so in-place repair remains allowed). **The
corrections, with the commands behind them:**

1. **Stale sibling-lane attribution (body).** The pull-request body said at three sites that lanes A
   and B had "already pushed their first batches with rows K-082..K-089 (PR #771 and PR #772)". That
   was stale: lane B (PR #772) renumbered its rows from K-082..K-089 into the lane-B band
   **K-181..K-188** at commit `a94dc5ea2f996f47cdaeb10f8995d8f68e232950` (2026-10-15 13:53:52 -0700,
   "docs(readability): renumber PR 772 keeper rows into lane B band K-181..K-188"), before this body
   was last revised. Measured by command, not memory:
   `git show refs/pull/772/head:docs/roadmaps/aegis-documentation-readability-backlog.md` — lane B's
   file now carries the eight rows K-181..K-188 and holds no K-082..K-089 rows; lane A (PR #771, head
   `f6a4e4189ecfbe874f97ec9b6b09bf8fe14f49ad`, 2026-10-15 13:53:50 -0700) still holds K-082..K-089.
   This lane's own band **K-090..K-097** was re-checked against both sibling heads with the same
   command at 2026-10-15T15:07:40-07:00 and collides with neither (no K-090..K-097 row in either
   sibling file). All three body sites were corrected, and the body now carries a frozen
   sibling-PR observation note (the facts, the revision each was true at, and the observation time)
   instead of a live claim.
2. **Bare register ID (body and record).** The body's moved-main note named "(the PR #770 merge,
   APR-137)" without a plain-English gloss; the body now carries the register's gloss beside the ID:
   "AEGIS-APR-137: Readability index program — resume ratified, historical backfill approved, and
   the sweep reaffirmed to zero pending" (the register's heading at main
   `7abb98eb88ec3253521ab4ff5418d225413bd193` and at the current main
   `f490c16f9ed23f3d489e42f7696323bffcce6fd3`, both verified with `git show
   <ref>:docs/approvals/APPROVAL_REGISTER.md` — the heading prints an em dash; the fourth round
   restored the dash here and in the body). This record's `scoped-approval-register` ledger row
   named the register entries AEGIS-APR-039, -101, -113..-118, -125, -129 with no descriptions; they
   are register entries read at the base, and their one-line register headings (each read from
   `docs/approvals/APPROVAL_REGISTER.md` at `e2a3e20b`) are:
   - **AEGIS-APR-039:** Reaffirmation of ongoing backlog delivery approval
   - **AEGIS-APR-101:** Ledger keeper role and two historical recording acts
   - **AEGIS-APR-113:** Readability pending-count authority (Option 1)
   - **AEGIS-APR-114:** Work and merge terms for the readability count program
   - **AEGIS-APR-115:** Standing approval for index-rebuild pull requests after the switch
   - **AEGIS-APR-116:** The ledger keeper may record targeted reviews in the acceptance record table
   - **AEGIS-APR-117:** The ledger keeper may append withdrawal rows after the switch
   - **AEGIS-APR-118:** Security classification of the readability acceptance tool
   - **AEGIS-APR-125:** AEGIS-APR-114 CONSUMED — the index-repair switch merged
   - **AEGIS-APR-129:** The lighter review path for pure-docs pull requests (2026-10-12)
3. **Bound-field digest (body).** The body's witness bound field is corrected (one of the three
   corrected body sites sits inside it), so the bound-field digest changed: the published figure was
   `1b72bdbbee456702` and the new figure over the corrected three fields is stated in the body's
   digest line (which sits outside all three bound fields, so stating it changes nothing). A digest
   change with a stated reason is correct; one without is the failure mode.
4. **Systemic note (body).** The body now states which sibling-PR facts it asserts, the revision at
   which each was true, and that they may have moved since — frozen with the observation time, the
   same treatment this body already gives a moved main.

**Keeper rows.** This third-round repair authors no keeper row and withdraws none — the same
statement the first two rounds make, restated for the fourth head: the withdrawal of K-090..K-097
and their re-recording by a separate eligible keeper remain **PR #781**'s scope.

*Repair drafted by **DeepSeek v4 Pro** (`deepseek-v4-pro`), the Stage D repairing agent (third
round), under the owner account, as the repository's 2026-10-13 attribution rule requires.*

## 18. Stage D REVISE repair note, fourth round (2026-10-15)

The Stage D audit's fourth round returned **REVISE** on this pull request with five findings — one
P2 (a must-fix review finding) and four P3 (citation/gloss defects) — posted on the pull request as
comment 6204472704. All five are repaired in place at this lane's fifth head (the record is still
unmerged, so in-place repair remains allowed). **The corrections, with the commands behind them:**

1. **F1 (P2) — LD-4 partial, not full.** The record's section 4 recorded LD-4 "accepted unchanged"
   and keeper row K-093 full-page-acceptance, while section 6(b)/O-2 acknowledged that LD-4's `D9`
   (owner decision 9) is unglossed at page L30 — a failure of acceptance bullet 2 (abbreviations and
   coded identifiers defined at first use). Verified by command: `git show
   e2a3e20b:docs/evidence/documentation/full-page-readability-sample-2026-09-23.md` — `D9` occurs
   exactly once, at L30, unglossed. LD-4's disposition is now **partial** in section 4 (table,
   heading and the note after the table), section 6(b), O-2, the section 10 note under the row-quote
   block, the skills ledger's acceptance row, the ledger section and the pull-request body; K-093
   **does not stand as authored**. The withdrawal is **PR #787**'s work, not re-done here: verified
   by command `git fetch origin refs/pull/787/head` → head
   `1419d480e0c2f90ccb62cd4f491ae2b8c4aa676d` (PR open), which appends withdrawal row K-392W
   ("WD-D4-r1 withdraws K-392 (deepseek-v4-pro-apr117-keeper): LD-4 accepted: docs/evidence/documentation/full-page-readability-sample-2026-09-23.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f")
   and records LD-4 PARTIAL, left pending; K-093's own lineage is cancelled on main by K-384W
   ("WD-D4 withdraws K-093 (readability-phase4-lane-d-implementer-c): LD-4 accepted: docs/evidence/documentation/full-page-readability-sample-2026-09-23.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f",
   merged PR #781). The eight rows stay in the keeper table as authored so the main-side withdrawals
   stay aligned — the same shape PR #771 used for its P8/K-089 partial page.
2. **F2 (P3) — bare register IDs in the body.** The security-surface bullet and the security bound
   field named AEGIS-APR-118 (the register entry "Security classification of the readability
   acceptance tool") without a gloss, and the skills bound field's AEGIS-APR list was bare. Each now
   carries its one-line register heading (section 17; each heading verified verbatim at `e2a3e20b`
   with `git show e2a3e20b:docs/approvals/APPROVAL_REGISTER.md`).
3. **F3 (P3) — the AEGIS-APR-137 heading quote.** The body and this record's section 17 printed a
   hyphen where the register prints an em dash. Verified at the current main: `git show
   f490c16f9ed23f3d489e42f7696323bffcce6fd3:docs/approvals/APPROVAL_REGISTER.md` prints
   "### AEGIS-APR-137: Readability index program — resume ratified, historical backfill approved,
   and the sweep reaffirmed to zero pending" (the same at `7abb98eb88ec3253521ab4ff5418d225413bd193`);
   both copies (body and record) now print the em dash.
4. **F4 (P3) — the elided splice quote in the new ledger section.** The ledger section still quoted
   "does not grant provider, private-input, real-host or deployment authority" (L3018-3020) — the
   elided splice this record's section 12 and the body's residual list already fixed. The ledger
   section now quotes the contiguous fragment "not mark earlier screens as full-page acceptance or
   grant provider, private-input, real-host or deployment authority" (`git show
   e2a3e20b:docs/roadmaps/aegis-documentation-readability-backlog.md` L3018-3020). The four
   pre-existing dated sections that quote the elided form (L4746, L4819, L4909, L5111 — counted by
   command over the whole file, two more than the second round's note named) are no-rewrite-protected
   and untouched.
5. **F5 (P3) — the promised finish/wall time.** Section 14 promised a batch finish timestamp and wall
   time "recorded in the pull-request body"; neither was ever recorded anywhere. The promise is
   corrected (the figures are recorded as not recorded — stated, not filled), and this repair item's
   own start, finish and wall time are recorded here and in the body.

**The whole-diff quotation sweep (F4's second half).** Every quotation this branch's diff reproduces
was re-checked against its source at `e2a3e20b` by command, in every copy — this record, the ledger
section and the pull-request body. Results, all verbatim: the LD-1/LD-2 closing phrases (LD-1 L68
"Exact-head Actions and merge remain outstanding.", LD-2 L41 "Exact-head GitHub Actions and merge
remain delivery gates."); the section 6(d) LD-4..LD-8 fragments (each spans a page line break and
joins verbatim; LD-4's is elision-marked with "..."); O-1's "tracker L2941–2947" (en dash) and
"tracker L2801"; O-2's "Reconciled the 30-day evidence-policy choice, schema-shape and D9 decisions"
(LD-4 L30) and "D9 (2026-07-06) — A Compliance & Governance batch" (step-0-reconciliation-v4.md
L941); O-3's `PLAN-first-batch.md 4eeaf8aa…`, `AUDIT-B ca7e3b9f…`, `STAGE0 8cbd113f…` (LD-3
L6-7); O-4's "all **seven local links** resolved" (LD-5 L59 — the bold markers are now quoted too);
the six merge subjects (full subjects now quoted, `git show -s --format=%s b545d075 5c46c7b3
2c6b6fc6 6051ab0a e6148322 a8b81d49`); the batching-procedure fragment (record section 12, body
residual item 6, ledger section — the three copies now agree); the ten register headings in section
17 (each verbatim at `e2a3e20b`, with AEGIS-APR-125's em dash); the AEGIS-APR-117 heading ("The
ledger keeper may append withdrawal rows after the switch", register L5016 at the base); and the
AEGIS-APR-137 heading (em dash, above).

**Keeper rows.** This fourth-round repair authors no keeper row and withdraws none — the same
statement the first three rounds make, restated for the fifth head: the withdrawal of K-090..K-097
and their re-recording by a separate eligible keeper were PR #781's scope (merged as
`f490c16f9ed23f3d489e42f7696323bffcce6fd3`), and the withdrawal of LD-4's re-record K-392 as
K-392W, with LD-4 recorded PARTIAL and left pending, is PR #787's scope (open at head
`1419d480e0c2f90ccb62cd4f491ae2b8c4aa676d`).

**Timing (the name-and-time rule).** Item: PR #774 fourth-round repair — five Stage D findings,
one P2 and four P3. Start: 2026-10-15T17:14:30-07:00 (harness-sampled at the first work step). ETA:
none was given in the coordinator's brief — recorded as unavailable, not invented. Finish
(edit phase, through this commit): 2026-10-15T17:28:29-07:00 (measured by command immediately
before the commit). Wall time (edit phase): 13 minutes 59.7 seconds. Active time was not
instrumented, so the wall time is an imperfect comparison with the estimate rule's active-time
requirement. Post-commit verification and the pull-request-body publication continue after this
commit; their total wall time is reported to the owner at completion.

*Repair drafted by **DeepSeek V4** (`deepseek-v4-pro`, DeepSeek Harness), the Stage C repairing
agent (fourth round), under the owner account, as the repository's 2026-10-13 attribution rule
requires.*

## 19. Pre-merge Codex-triage repair note (2026-10-15; 2026-10-16 UTC)

**This is the pre-merge triage AEGIS-APR-050 requires** (the register entry "Merges wait for the
automated Codex review": wait for the Codex review, then triage every P1 and P2 finding before
merging — fix it, or record in the pull request why it is not a defect). The pull request carries
**1** Codex review and **3** review comments (`gh api
repos/ModernNomad-98/Project-Aegis/pulls/774/reviews` prints one object; `.../pulls/774/comments`
three; all `chatgpt-codex-connector[bot]`, all `original_commit_id` =
`370bc8db75faf251b28ad0e328e559cbcd320866`). **Three findings, three recorded dispositions**, in the
pull-request body's triage section. Two are answered without a change here: the separate-keeper
finding is answered on main by merged PR #781 (rows K-381W..K-388W withdraw K-090..K-097 and rows
K-389..K-396 re-record them, keeper `deepseek-v4-pro-apr117-keeper`, a different agent from the
accepting reviewer), and the `D9` finding is answered by LD-4's **partial** disposition and K-093's
declared non-standing (section 4). **One is fixed here:** the third finding (P1) reads the skills
record as crediting `acceptance-criteria-reviewer` with the acceptance verdict, so section 13 and
its six-field row now describe what that skill's contract permits — one verdict per criterion, since
it "never decides whether work is done"
(`.claude/skills/acceptance-criteria-reviewer/SKILL.md` L25-33; `docs/delivery-workflow.md` L98
records it as a partial fit only) — and state that the accept/partial dispositions are the lane's own
recorded decision (section 4).

**The second correction is a quotation with no source.** Section 5's two quotation marks around
`unchanged remainder` are **removed**: the 2026-10-12 batch record states its limit as "the
*unchanged* remainder of each large page was covered by pass 1"
(`docs/evidence/documentation/readability-reread-batches-2026-10-12.md` L126), so the quoted
two-word form is verbatim nowhere in the tree, and a quotation with no source is the defect class
this branch has been repairing. No keeper row, no withdrawal row, no row-quote string (section 10),
no date-stamped page and no protected ledger section was touched — this repair edits this record only.

**Timing (the name-and-time rule).** Item: the pre-merge Codex triage of PR #774 under AEGIS-APR-050
and this record's two wording corrections. Start 2026-10-15T18:28:46-07:00 (2026-10-16T01:28:46Z,
harness-sampled at the first work step). ETA: none was given in the coordinator's brief — recorded as
unavailable, not invented. Finish (edit phase, through this commit):
2026-10-15T18:35:48.7476998-07:00 (2026-10-16T01:35:48.7476998Z, measured by command immediately
before the commit). Wall time (edit phase): 7 minutes 2.7 seconds.

*Repair drafted by **DeepSeek-4.1-Flash** (`deepseek-flash`, DeepSeek Harness), the Stage C repairing
agent, under the owner account, as the repository's 2026-10-13 attribution rule requires.*

---

*Prepared by a **DeepSeek agent** (`deepseek-v4-pro`) operating under the owner account, as the
repository's attribution rule (2026-10-13) requires; fourth-round repair (section 18) drafted by
**DeepSeek V4** (`deepseek-v4-pro`, DeepSeek Harness), the Stage C repairing agent.*
