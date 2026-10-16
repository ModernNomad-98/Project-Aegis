# Readability Phase 4 re-read lane D — batch 3 record, 2026-10-15

- **Lane:** PHASE 4 RE-READ LANE D (full-page independent re-reads of the lane's fixed page range).
  **Stage:** C (IMPLEMENT). **Base:** `e2a3e20b7c20ef8385b219b39c6405237163406f` (`origin/main`, the
  PR #769 merge; equal to the lane's derivation base and equal to batches 1 and 2's base).
- **Plan applied:** the coordinator's lane-D brief of 2026-10-15 (batch 3), which carries the same
  derivation rule batches 1 and 2 applied ("run `check_index.py`, sort the pending paths, take
  your quarter; batch 3 = the next eight after batches 1 and 2"). No separate plan artifact exists for
  this lane; the brief's own derivation rule is the plan of record, and this record states every step
  it took from it.
- **What this page is.** The lane's tracked batch record: the **evidence record only**. Per the
  coordinator's batch-3 brief and AEGIS-APR-101 (the keeper-independence rule: the keeper must be a
  different agent from the page's author and from the accepting reviewer), **this batch authors NO
  keeper rows and writes NO ledger section** — earlier batches drew P1 findings because same-agent
  rows silently lower the official count. A separate eligible keeper records the rows from this
  evidence, under AEGIS-APR-117 (the keeper's targeted-review recording authority: withdraw and
  re-record by a different agent from the same evidence; no page needs re-reading). Section 10's
  quote strings are offered verbatim for that keeper's rows.
- **Acceptance revision named by this record:**
  `e2a3e20b7c20ef8385b219b39c6405237163406f`.
  That revision resolves to itself and is contained in `refs/remotes/origin/main`
  (`git merge-base --is-ancestor e2a3e20b7c20ef8385b219b39c6405237163406f refs/remotes/origin/main` exits 0).
- **The lane changed none of the eight read pages.** So the bytes this record read are the bytes the
  merge receives, and the acceptance is not voided by the merge.
- **Revision 2, 2026-10-16 — the first SD-D applied (findings F1-F5).** The Stage D audit of the
  first head (`99d46d752357c6cb127274944ce2ac2ff0b9b78e`) returned **REVISE**; the posted receipt is
  PR #784 issue comment `6209631818`. This revision re-records the five bullet-(b) PARTIAL pages as
  FULL under the standing C-1 ruling, with the measurement cited per term (sections 4 and 6(b));
  replaces section 10's false "cannot silently read as full" safeguard with the C-4 rule and its
  construction proof, and offers its strings for FULL pages only (all eight are FULL); corrects the
  ledger quotation (F3), the lost-commit phrase's source (F4) and the timing claim (F5, section 14);
  and adds section 15, what this round did not verify. Prepared by **DeepSeek-4.1-Flash
  (deepseek-flash)**, Stage C — a different agent from the record's first drafter
  (`deepseek-v4-pro`); the Stage D auditor also ran on DeepSeek-4.1-Flash (deepseek-flash).

## 1. The instrument's figures at the base, quoted

```text
python -P -B tools/readability_acceptance/check_index.py --json --ref origin/main
compared_ref e2a3e20b7c20ef8385b219b39c6405237163406f, reader_pages_in_tree 653,
accepted_on_recorded_review 57, provably_pending 4, no_recorded_acceptance 586,
recorded_acceptance_within_10_lines 0, within_10_not_covered_by_targeted_review 0,
cannot_decide 6, official_pending_count 596
exit 0
```

**This lane publishes no readability count of its own** (ledger L19-31, D84) and presents the figures
above as the instrument's, not as its own measurement. The run was made on a fresh clone of
`origin/main` at `e2a3e20b7c20ef8385b219b39c6405237163406f` (the same base batches 1 and 2 derived from;
origin/main had not moved when this batch derived).

## 2. The lane derivation, stated with its command

1. The pending set is the instrument's `no_recorded_acceptance` (586) plus `provably_pending` (4)
   buckets: **590 paths**, derived by replicating `check_index.py`'s own `classify_tree`
   (tracked `.md` at the ref, minus the `scripts/` fixtures except
   `scripts/tests/fixtures/README.md`, minus the one generated report) and subtracting the paths the
   committed `acceptance-index.json` carries rows for. The 4 provably-pending paths were taken from
   the same command's `pending` array. Command: `python -P -B tools/readability_acceptance/check_index.py
   --json --ref origin/main` plus a Python script over its output, saved with the lane
   (`_derive_laneD_b3.py`, `_laneD_b3_derivation.json`).
2. The 590 paths were **sorted**, then split into **four contiguous quarters by count**
   (148 / 148 / 148 / 146). **Lane D takes the last quarter: 146 pages, first**
   `docs/evidence/documentation/full-page-readability-batch-after-233-2026-09-24.md`, **last**
   `tools/behavioral_eval_runner/README.md` (sorted indices 444-589 of the 590, 0-based).
3. **Batch 1 = the first 8 of lane D** (sorted indices 444-451) — this derivation reproduces PR #774's
   eight pages boundary-for-boundary. **Batch 2 = the NEXT 8 (indices 452-459)** — reproduced
   boundary-for-boundary against PR #778's record. **Batch 3 = the NEXT 8 of lane D in sorted order
   (indices 460-467, 0-based; 1-based positions 461-468)**, re-checked against the instrument at the
   base immediately before reading: all eight sit in `no_recorded_acceptance` at `e2a3e20b` (each path
   verified absent from `acceptance-index.json`'s `reader_pages`), so none is already accepted and
   none is outside the lane's range. **The brief's gloss, read honestly:** the brief wrote "Lane D is
   quarter index 460 (0-based start), approximately paths 461 to 467 of the sorted pending list".
   460 is this batch's own 0-based start index (batches 1 and 2 took 444-459), and the true 1-based
   bound of this batch is 461-468; the lane's quarter itself is the last contiguous quarter, 444-589,
   exactly as batches 1 and 2 derived and PRs #774 and #778 confirm.
4. **No page outside lane D's quarter is read or recorded here**, and this batch's eight pages appear
   in no other lane's pushed rows (checked against the open lane PRs #771, #772, #774, #776, #777,
   #778, #779, #780 and the APR-117 re-record PR #781 path-by-path: zero overlap), so no page is read
   twice. The 6 `cannot_decide` (lost-commit) pages are in NO lane's list; this lane excludes them
   and states the exclusion here rather than picking them up silently:
   `.claude/skills/cloud-security-baseline-reviewer/references/aws-baseline.md`,
   `.claude/skills/cloud-security-baseline-reviewer/references/azure-baseline.md`,
   `.claude/skills/cloud-security-baseline-reviewer/references/gcp-baseline.md`,
   `.claude/skills/cloud-security-baseline-reviewer/references/supabase-baseline.md`,
   `.claude/skills/cloud-security-baseline-reviewer/references/vercel-baseline.md`,
   `.claude/skills/database-backup-verifier/SKILL.md`.

## 3. The roster, the independence posture, and what this batch does not do

One reader (`readability-phase4-lane-d-implementer-c3`, a different agent from batch 1's
`readability-phase4-lane-d-implementer-c` and batch 2's `readability-phase4-lane-d-implementer-c2`)
read all eight pages.

**Independence, stated plainly — no deviation to declare.** Per the coordinator's batch-3 brief: **the
reader does NOT author acceptance rows for pages it read** (AEGIS-APR-101), because earlier batches'
same-agent rows drew P1 findings — `build_index.py` reads row structure and cannot see the prose
that says a row is not green, so ineligible rows silently lower the official count. This batch
therefore: writes the evidence record only; authors no keeper row; edits no ledger section; claims no
row IDs; and leaves the row recording to a **separate eligible keeper under AEGIS-APR-117** (record
rows from the same evidence; no page needs re-reading). The first independence clause is satisfied by
construction — this lane wrote none of the eight pages (each is a dated record of a 2026-09-23,
2026-09-24, 2026-10-10 or 2026-10-12 batch authored by other agents) — and the second clause is the
future keeper's to satisfy, not this lane's.

## 4. Per-page dispositions — 8 whole-page re-reads; all eight FULL (revision 2 re-recorded the five former partials under C-1)

Every page below was read **whole** at `e2a3e20b7c20ef8385b219b39c6405237163406f`. None has a recorded
acceptance, so drift has no recorded acceptance revision to diff against (`not derivable`, the same
wording the after-713 record used for its no-recorded page).

| # | Page | Recorded acceptance | Drift | Disposition | Reader |
| --- | --- | --- | ---: | --- | --- |
| LD-17 | `docs/evidence/documentation/readability-maintainer-guides-2026-09-23.md` | none (no-recorded bucket) | not derivable | **accepted unchanged (full)** | `readability-phase4-lane-d-implementer-c3` |
| LD-18 | `docs/evidence/documentation/readability-reread-batches-2026-10-12.md` | none (no-recorded bucket) | not derivable | **accepted unchanged (full)** — observations, section 6(b) | `readability-phase4-lane-d-implementer-c3` |
| LD-19 | `docs/evidence/documentation/readability-technical-guides-2026-09-23.md` | none (no-recorded bucket) | not derivable | **accepted unchanged (full)** — observations, section 6(b) | `readability-phase4-lane-d-implementer-c3` |
| LD-20 | `docs/evidence/documentation/remaining-active-docs-readability-2026-09-23.md` | none (no-recorded bucket) | not derivable | **accepted unchanged (full)** — observations, section 6(b) | `readability-phase4-lane-d-implementer-c3` |
| LD-21 | `docs/evidence/documentation/roadmap-current-forecast-routes-2026-09-23.md` | none (no-recorded bucket) | not derivable | **accepted unchanged (full)** — observations, section 6(b) | `readability-phase4-lane-d-implementer-c3` |
| LD-22 | `docs/evidence/documentation/roadmap-deep-status-terms-2026-09-23.md` | none (no-recorded bucket) | not derivable | **accepted unchanged (full)** | `readability-phase4-lane-d-implementer-c3` |
| LD-23 | `docs/evidence/documentation/root-readme-workspace-routing-2026-09-23.md` | none (no-recorded bucket) | not derivable | **accepted unchanged (full)** — observations, section 6(b) | `readability-phase4-lane-d-implementer-c3` |
| LD-24 | `docs/evidence/documentation/root-status-docs-readability-2026-09-23.md` | none (no-recorded bucket) | not derivable | **accepted unchanged (full)** | `readability-phase4-lane-d-implementer-c3` |

**Revision 2 dispositions (SD-D F2).** The first head dispositioned five pages partial on
bullet-(b) grounds. The standing C-1 ruling makes those grounds **observations**: an unglossed term
that is a library-wide convention is not a per-page defect, and the stronger test is whether the
page itself resolves it. Measured here by command over the **653 reader pages at the base**
(`classify_tree` replicated: tracked `.md` at the ref, minus the `scripts/` fixtures except the one
README, minus the one generated report):

| Term | Reader pages containing it | Occurrences | C-1 treatment |
| --- | ---: | ---: | --- |
| `PR`/`PRs` | 291 | 4,153 | library-wide convention — observation (LD-18, LD-23) |
| `UTC` | 106 | 842 | library-wide convention — observation (LD-19) |
| `sha256` | 37 | 146 | library-wide convention — observation (LD-18) |
| `ETA` | 30 | 270 | library-wide convention — observation (LD-19) |
| `EVAL-004`, `AEGIS-060` | — | — | the page resolves it: first used L25-26, defined on-page L27-29 (LD-20) |
| `#186` | — | — | the page resolves it: used bare L3, expanded to "pull request #186" L23 (LD-21) |

The convention threshold is the one the **merged** lane A batch-5 record
(`docs/evidence/documentation/readability-lane-a-batch-5-2026-10-15.md`, section 5, present on
`main`) published and applied: at its bound revision `acceptor` on **12** reader pages is
"convention — observation", while `Phase 1.5` on **11** is "below convention — the one gap
recorded in this batch". All four terms above sit far above 12. The batch-3 brief's own rule ("an
undefined term used before its definition is not a full acceptance") conflicts with C-1 for LD-20
and LD-21; the standing C-1 ruling governs, as the SD-D states. **All five pages are accordingly
re-recorded FULL**, their observations named in section 6(b). No page needed a fix, so no page was
edited: the no-rewrite discipline forbids edits to dated records.

## 5. Depth records

**Every line of every page was read as prose, at the declared revision.** The eight pages are 43 +
319 + 48 + 63 + 33 + 30 + 55 + 37 = **628 lines** in total (largest page 319 lines), extracted from
the exact revision with `git show e2a3e20b:<page>` and read with line numbers. **No display elision
occurred and no range was skipped**: each page fit a single read pass, so the read depth is the
whole page for all eight.

**The mechanical pass** ran over the same exact-revision bytes. For each page it enumerated: every
Markdown link (local and external) and every in-page anchor target; every 40-character SHA; every
7-12 hex token inside backticks; and coded identifiers by the stated pattern
`\b(?:[A-Z]{2,8}-\d{1,4}|D\d{2,3}|PR\s*#\s*\d{1,4}|#\d{3,}|K-\d{3}|L-\d{3}|T-\d{3}|AC\d{1,2})\b`.

| Page | Local links resolved | External links (not fetched) | Broken links | Bad anchors | 40-hex SHAs | Unresolvable 40-hex | 7-12 hex backtick tokens | Not resolving | Coded identifiers |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| LD-17 | 4 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| LD-18 | 0 | 0 | 0 | 0 | 25 | 2 | 27 | 6 | 21 |
| LD-19 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| LD-20 | 8 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 3 |
| LD-21 | 5 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| LD-22 | 5 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| LD-23 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| LD-24 | 2 | 1 | 0 | 0 | 1 | 0 | 1 | 0 | 0 |

External links (github.com x2: PR #122 on LD-17, PR #176 on LD-24) were **not fetched**, matching the
2026-09-23 sample's own recorded practice ("external links were not fetched"). Every non-zero
residue in the table above was opened and dispositioned; none is a defect the page hides: the two
unresolvable 40-hex occurrences are LD-18's own D-1 row's `9644ef07…`, which the page discloses
as the unreachable grant revision it names follow-up 1; the six not-resolving backtick tokens are
LD-18's D-4 row's six named lost commits (`65bacc7`, `d3dcb62`, `3c44f4a`, `e9cce7d`,
`288d993`, `7f98950`), which the page itself explains as lost-commit events. The phrase "recorded, never bound,
never dropped" is the acceptance tool's own wording (`tools/readability_acceptance/build_index.py`
L15-16 and `tools/readability_acceptance/README.md` L58), carried by LD-18's D-4 row; D73 row 5
(`docs/reconciliation/step-0-reconciliation-v4.md` L3834) records the same six as counting as
pending until re-reviewed and says they are "never bound to another commit and never dropped
silently", not the quoted phrase (SD-D F4). The one 40-hex SHA on each of LD-20/LD-21/LD-22/LD-24 and
the two 7-hex tokens (LD-17 `b2c6db2`, LD-24 `02ff5f0`) all resolve in the local object store at
`e2a3e20b`.

## 6. The six acceptance bullets, addressed for each of the eight pages

**(a) Purpose and audience up front.** LD-17's banner names the merged PR #122 and glosses API
(L3-9), and its purpose paragraph addresses reviewers (L11-14); LD-18's header block names the lane,
stage, base, plan and what the page is (L3-19); LD-19's banner defines AI, JSON, YAML and SHA-256
(L3-9) and states the reviewer purpose (L11-14); LD-20's banner and dated header name what is
historical and the scope (L3-16); LD-21's banner names the live route (L3-7); LD-22's banner routes
to the live backlog and register (L3-8); LD-23's banner defines BER and UTC and routes to the live
README and ledger (L3-7); LD-24's banner names the merged PR #176 and defines UTC (L3-8). None of
the eight names an intended audience in so many words — the banner pages address "current reading"
to a generic reader. That is a property of the dated text, which this lane may not rewrite.

**(b) Abbreviations and coded identifiers — every term dispositioned; observations, not gaps (revision 2).**
- **LD-18 — observations:** `PR` is used unglossed on nine lines (L4, L136, L138, L195, L196, L200,
  L240, L244, L254) and `sha256` at L6 and L8; neither is expanded on-page. Both are library-wide
  conventions under C-1 (section 4: `PR`/`PRs` on 291 of the 653 reader pages at the base, `sha256`
  on 37 — both above the ≥12-page convention threshold the merged lane A batch-5 record published
  and applied). The remaining coded identifiers — SD-B ACCEPT (L7), the batch labels B1-B4 (L49-54),
  P1-P8 / W1-W10 (L74-93), F4/F5 (L57, L98), AC1/AC2/AC7/AC10 (L230, L233, L246, L263),
  D73/D84/D86/D87/D98 (L242, L259, L261-263, L266) and the L-citations (L229, L242, L258) — are the
  cited plan and ledger artifacts' identifiers, carried by design.
- **LD-19 — observations:** `UTC` (L47) and `ETA` (L43-45; four occurrences) are used without an
  on-page expansion. Both are library-wide conventions (section 4: 106 and 30 reader pages), above
  the ≥12 threshold. (The banner defines AI/JSON/YAML/SHA-256, L7-9, and the table spells out the
  other terms, L20.)
- **LD-20 — the page resolves it:** `EVAL-004` and `AEGIS-060` are first used at L25-26 and defined
  on the page at L27-29 ("EVAL-004 is the audit rule for named evaluation targets; AEGIS-060 is the
  identifier (ID) of the rejected proposed finding.") — two to three lines after first use, so the
  page itself resolves them (C-1's stronger test); observation, not a gap. (UTC L10, ID L28,
  AI/API/CQRS L48-49, PR L12 are each at first use.)
- **LD-21 — the page resolves it:** `#186` is used bare at L3 ("The #186-at-base … language") and
  expanded on the page at L23 ("at this base it names pull request #186") — the page itself
  resolves it; observation, not a gap. (UTC is defined L9; pull request is spelled out L11, L19,
  L23.)
- **LD-23 — observation:** `PR` is used unexpanded in "merged PRs #122, #126, #127, #128 and #133"
  (L47-48; one occurrence); a library-wide convention (section 4: 291 reader pages), above the ≥12
  threshold. (BER L6 and UTC L7 are defined before use.)
LD-17 (PR L3, API L7-8), LD-22 (pull request L16/L22/L24, work package L19, UTC L15, Behavioral Eval
Runner L5) and LD-24 (PR L3-4, UTC L7-8) define at first use. **Recorded, not repaired** — dated
records; every term above is dispositioned, so each of the eight pages is eligible for a full-page
acceptance row, and no page is offered a partial row.

**(c) Descriptive headings, lists or tables, and concrete examples.** LD-17 carries a three-row
problem/change table (L18-22) and verification bullets (L30-35); LD-18 headed sections 1-9, the
disposition table (L74-93), the mechanical table (L205-214) and worked stale/new/source rows C-1..C-3
and D-1..D-5; LD-19 a findings table (L18-21) and verification bullets (L29-39); LD-20 the scope
bullets (L20-35) and timestamped verification paragraphs (L42-63); LD-21 verification paragraphs
(L26-33); LD-22 plain headed paragraphs; LD-23 sections with verification bullets (L31-45); LD-24
check bullets (L26-31). Concrete worked content sits on all eight (LD-17's 33 passed tests and the
GitHub API check; LD-18's drift figures and the D-1/D-4 residues; LD-19's three corrected review
issues; LD-20's 25/25 links and 34 added lines; LD-21's 121 links / 23 anchors and 58-second freeze;
LD-22's base and grant SHAs; LD-23's new README heading; LD-24's 1m55s freeze).

**(d) Shipped behaviour separated from proposed or blocked behaviour.** LD-17: "An independent
reviewer and pull-request checks are still required before this batch is complete" (L34-35), and the
banner separates checkpoint requirements from current state (L5-6). LD-18 separates
accepted / needs-a-named-follow-up / withheld dispositions (L74-93) and withholds P4's row by design
(L98-106). LD-19: "Exact-head GitHub Actions remain required" (L36); the edits "do not grant
approval, change a schema, run an evaluation or deploy a control plane" (L23-25). LD-20: "No
approval or grant entry … was changed or accessed" (L37-38); "No files were committed or pushed in
this batch" (L61). LD-21: "Independent read-only review is pending at this draft freeze" (L32-33);
"These checks do not grant implementation or live execution authority" (L31-32). LD-22: "Pull
request #139 remains subject to a separate protected-file guard disposition" (L24-25); the change
"does not authorize real-host use or a provider request" (L25-26). LD-23: the edit "does not verify
host skill discovery or grant permission for product work" (L44-45) and "does not change a skill,
runtime, approval or deployment policy" (L22-23). LD-24: "Independent read-only review: pending on
this frozen draft" (L31); "No runtime behavior, skill criteria, approval, or private reporting
route is changed" (L21-22).

**(e) Navigation links current; every referenced file or command exists.** Section 5's mechanical
pass: 33 local links, zero broken paths, zero bad anchors across all eight pages; the named commands
(`python -B -m unittest …`, `python -B scripts/validate-skills.py`, `git diff --check`,
`python -B tools/readability_acceptance/check_index.py`, `build_index.py`) exist as git builtins or at the
named script paths at the base. The two external links were not fetched, matching the dated-note
practice. The 2026-09-23 pages' historical validation figures ("184 skills valid" on LD-19 L32,
"185 valid skills" on LD-20 L44/L57, LD-21 L30-31, LD-23 L37, LD-24 L26; LD-20's "25 links")
describe the batches at their own 2026-09-23 checkpoints, not today's tree — observation O-3.

**(f) The non-author review itself.** This record, with the independence posture in section 3: this
lane wrote none of the eight pages, and this batch authors no keeper rows — the rows are a separate
eligible keeper's work under AEGIS-APR-117, so the AEGIS-APR-101 keeper-independence condition stays
satisfiable. This record neither satisfies nor claims the keeper's independence.

## 7. Purpose and normal use restated from each page alone

- **LD-17** — *for:* recording the 2026-09-23 maintainer-guide readability batch (three guides,
  what each was missing, what the batch added) and its verification receipts. *Normal use:* read the
  banner for where the live guides are; the body is dated evidence of that batch.
- **LD-18** — *for:* the 2026-10-12 remaining-page re-read batches' Stage C record — which pages were
  accepted, which carry named follow-ups, which row was withheld and owed, and the offline
  re-verification table. *Normal use:* the evidence source those batches' keeper rows cite; read it
  with the plan it names.
- **LD-19** — *for:* the two technical guides' readability corrections (Behavioral Eval Runner schema
  compatibility policy and the Zero Trust discipline) and their verification. *Normal use:* read the
  banner for the delivered state; the estimates and 184-skill figure are the draft checkpoint's.
- **LD-20** — *for:* the reading keys for the remaining active docs (300-skill roadmap, catalog,
  audit baselines, VolunteerFlow handoff) and the scope/verification receipts of that correction.
  *Normal use:* read it before those pages to know what each pointer clarifies and what it does not
  establish.
- **LD-21** — *for:* the four-link forecast correction that re-pointed three roadmap pages to the
  stable "Start here — current reading" section. *Normal use:* read the banner for the live forecast
  route; the receipts are dated evidence.
- **LD-22** — *for:* the deeper-section status and terms correction on the Behavioral Eval Runner
  backlog and the historical skills roadmap. *Normal use:* read the banner for present gates; the
  body records what was clarified and what the clarification does not authorize.
- **LD-23** — *for:* the root README's two-workspace start-sequence clarification (product repos
  versus the source checkout) and its verification. *Normal use:* read the banner for the live
  README and ledger; the 503-page inventory figure is the original batch's.
- **LD-24** — *for:* the root status docs readability batch (changelog history mark and Claude
  startup routing wording). *Normal use:* read the banner for the merged state; the pending-review
  language is the frozen-draft checkpoint's.

## 8. Observations — read and dispositioned, none edited in place

Row shape: `stale:` the exact text as it stands at the declared revision; `new:` `unchanged`;
`source:` the artifact that settles it.

| # | stale | new | source |
| --- | --- | --- | --- |
| O-1 | LD-18's D-1 row (its L240) discloses `9644ef079db763802223180ae5b11af39919c781` as the unreachable grant revision and names it follow-up 1. At `e2a3e20b` the object still does not resolve (mechanical pass, two occurrences, both on LD-18). | **unchanged** — the page already discloses the non-resolution; nothing to repair. | `git cat-file -t 9644ef079db763802223180ae5b11af39919c781` exits non-zero at the base; LD-18's own D-1 row. |
| O-2 | LD-18's D-4 row names the six lost-commit tokens `65bacc7`, `d3dcb62`, `3c44f4a`, `e9cce7d`, `288d993`, `7f98950` and explains them as lost-commit events (the wording "recorded, never bound, never dropped" is `build_index.py` L15-16 and the tool README L58, carried by LD-18's own D-4 row; D73 row 5 is `docs/reconciliation/step-0-reconciliation-v4.md` L3834, which says these pages count as pending until re-reviewed). All six fail to resolve at the base. | **unchanged** — the page is correct as written; these are the program's known lost commits. | `git cat-file -t` over each token at the base; LD-18's own D-4 row. |
| O-3 | LD-19 L32 ("184 skills valid"), LD-20 L44/L57, LD-21 L30-31, LD-23 L37, LD-24 L26 ("185 valid skills") and LD-20's "25 links" describe the batches at their own 2026-09-23 checkpoints. At `e2a3e20b` the validator reports 205 skills, and the pages' present link counts are 4 / 0 / 4 / 8 / 5 / 5 / 5 / 2 local links (section 5). | **unchanged** — historical sentences about their own batches, not restated as today's. | mechanical pass (section 5); `python -B scripts/validate-skills.py` at the base reports 205 skills (run this session). |
| O-4 | LD-22 L21's link anchor `#aegis-apr-012-offline-behavioral-eval-runner-evidence-policy-proof` carries the identifier APR-012 without a prose gloss. The anchor resolves into the approval register's own APR-012 section, which is the identifier's definition site. | **unchanged** — the identifier's definition is the link's target, and the link resolves. | mechanical pass (no bad anchors); the register's own APR-012 section at the base. |

Zero rows above have an empty source.

## 9. Count honesty

- **This lane publishes no readability count of its own** and cites the instrument, as the D84 switch
  requires. The instrument classifies the **page tree at `--ref`** and reads the recorded
  acceptances from the **committed index JSON**; this batch appends no rows, so **nothing in the
  index moves because of it**. `build_index.py --write` is **not** run in-lane: a rebuild adds JSON
  under `tools/`, which is not Markdown, and would break this change's `docs-only` tier; the rebuild
  itself is the standing AEGIS-APR-115 rebuild pull request's own scope.
- **The only movement at this lane's head is this lane's own new reader page**, which enters
  `no_recorded_acceptance` and therefore the official pending count. The published head expectation
  is **654 / 57 / 4 / 587 / 0 / 0 / 6 / 597** — the base's 653 / 57 / 4 / 586 / 0 / 0 / 6 / 596 with
  **+1 reader page, +1 no_recorded_acceptance and +1 official pending count**, all three attributed
  to this page. **No post-rebuild count is predicted.**

## 10. The row-quote strings, verbatim (offered for the separate keeper) — FULL pages only

Each line below appears in this file byte-for-byte and is offered for the separate eligible keeper's
rows under AEGIS-APR-117 (this lane authors no rows and claims no row IDs). Every line contains the
full 40-character acceptance revision, and every line below belongs to a page dispositioned **FULL**
(section 4). **The C-4 rule, stated here where a keeper will read it: a page dispositioned PARTIAL
gets no acceptance row and no string of any kind and stays PENDING** — the ledger names only
`full-page-acceptance`, `targeted-review`, `withdrawal` and `lost-commit`, so there is no
partial-acceptance kind to record. A disclaimer inside a quote cannot prevent the flip:
`build_index.py` reads row structure only, and `check_index.py` buckets any zero-drift page carrying
any non-lost-commit row as **ACCEPTED**. Proved by construction in a throwaway local commit (never
pushed): one row appended for LD-18 quoting the first head's own "(partial; gap(s) section 6(b))"
string — `build_index.py --report` exited 0 (`table_rows` 101→102, `full_page_acceptances` 81→82,
`reader_pages_with_rows` 68→69) and `check_index.py --json` exited 0
(`accepted_on_recorded_review` 57→58, `no_recorded_acceptance` 587→586, `official_pending_count`
597→596), with LD-18 in the **accepted** bucket at `changed_lines: 0`. The mitigation is to offer no
string at all for a partial page. **All eight pages are dispositioned FULL in revision 2**, so all
eight strings below are offered; none is offered for a partial page.

```text
LD-17 accepted (full): docs/evidence/documentation/readability-maintainer-guides-2026-09-23.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
LD-18 accepted (full; C-1 observations, section 6(b)): docs/evidence/documentation/readability-reread-batches-2026-10-12.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
LD-19 accepted (full; C-1 observations, section 6(b)): docs/evidence/documentation/readability-technical-guides-2026-09-23.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
LD-20 accepted (full; the page resolves its terms, section 6(b)): docs/evidence/documentation/remaining-active-docs-readability-2026-09-23.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
LD-21 accepted (full; the page resolves its term, section 6(b)): docs/evidence/documentation/roadmap-current-forecast-routes-2026-09-23.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
LD-22 accepted (full): docs/evidence/documentation/roadmap-deep-status-terms-2026-09-23.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
LD-23 accepted (full; C-1 observation, section 6(b)): docs/evidence/documentation/root-readme-workspace-routing-2026-09-23.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
LD-24 accepted (full): docs/evidence/documentation/root-status-docs-readability-2026-09-23.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
```

## 11. Verification commands (run at the head; outputs in the pull-request body)

`check_index.py --json --ref <head>` and `check_index.py --ref <head> --quiet` (the head counts,
`build_index.py --ref <head> --report` (no row change vs the base), the changed-path Markdown link
check, `scripts/validate-skills.py`, `scripts/tests/test_validator.py`, `git diff --check`,
the numstat additions-only check, `scripts/check_dco.py --range origin/main..HEAD`, and
`python -P scripts/ci/check_pr_body_skills.py --body-file <f>`.

## 12. What this lane did not do

It edited none of the eight read pages (no-rewrite discipline); rewrote no dated snapshot;
**authored no keeper row and edited no ledger section** (the batch-3 brief's corrected AEGIS-APR-101
posture; the rows are a separate eligible keeper's work under AEGIS-APR-117); bound no acceptance
row to the lane's own unmerged head; ran no `build_index.py --write` and rebuilt no `tools/` artifact;
touched no page outside the lane's stated range; touched no other lane's branch, PR or clone (PRs
#771, #772, #774, #776, #777, #778, #779, #780 are the other lanes' holders and PR #781 is the
APR-117 re-record's holder); picked up none of the six `cannot_decide` lost-commit pages; and
claims no authority beyond recording under AEGIS-APR-101 and the standing backlog delivery grant
AEGIS-APR-039 (the owner's standing grant for backlog work, commits, pushes, PRs and merges, granted
2026-10-15 with the eight defaults). The batching procedure "is a work plan" and "does not mark
earlier screens as full-page acceptance or grant provider, private-input, real-host or deployment
authority" (ledger L3018-3020).

## 13. Skills used (this lane, Stage C)

`change-classification-gate` — classified the change `docs-only` (one new evidence record,
Markdown only) before writing, which is what keeps the lighter review path applicable and the diff
inside the no-code tier. `acceptance-criteria-reviewer` — the six acceptance bullets applied to
each of the eight pages, each bullet addressed with line cites rather than asserted; the bullet-(b)
gaps are named, never smoothed over. `source-of-truth-reconciler` — the observations resolved
against the repository (the self-disclosed unreachable revision, the six named lost commits, the
historical validation figures, the APR-012 anchor) instead of against the pages' own prose.
`scoped-approval-register` — established this change records under AEGIS-APR-101, performs backlog
work under AEGIS-APR-039, and consumes, extends and requests no grant; the index rebuild is
AEGIS-APR-115's separate scope, not this change's. `docs-retention-index` — consulted; no retention
entry or frontmatter mechanism exists for `docs/evidence/documentation/` pages (zero files there
carry `retention:` frontmatter at the base), so the new page follows the established shape and
creates no retention row; recorded as checked-and-not-applicable. `skill-usage-ledger` — the
six-field records in this section, bound to the skills-manifest hashes.

```text
skill@08d91a834460beebc9c66fa896b8b422f064bf1d7524f6e5b1512cda3afdc996 / reason: classify before writing, the class decides the tier and review path / applied: classified docs-only before any write / result: docs-only tier asserted in the PR body with the file set / incomplete: None / by: readability-phase4-lane-d-implementer-c3 (Stage C)
skill@c6e5d5649bf89658036cf38abba9c626701220e7b00831c2d843ceff94d81021 / reason: the acceptance contract's six bullets are criteria and were checked one by one / applied: each bullet per page with line cites in section 6 / result: 8 full — the five former bullet-(b) partials re-recorded FULL under C-1 in revision 2, observations in section 6(b) / incomplete: None / by: readability-phase4-lane-d-implementer-c3 (Stage C)
skill@b5fd9feda97235430259913aedd33447ab06e1c0ded281e9e131fa6bf9b78be2 / reason: four page items needed resolution against the repo, not the page's prose / applied: observations O-1..O-4 sourced to repo artifacts / result: all four dispositioned unchanged / incomplete: None / by: readability-phase4-lane-d-implementer-c3 (Stage C)
skill@a74d2a22579cf93f737725aa0c54197b5d496a9f33a291a93c2cf2073cd7d076 / reason: recording requires knowing which grant covers what / applied: read AEGIS-APR-039, -101, -115, -117, -118 at the base / result: recording-only under APR-101; no grant consumed, extended or requested / incomplete: None / by: readability-phase4-lane-d-implementer-c3 (Stage C)
skill@141b7036469f9f99ef6b8e152299619a6d0ab572656a5ba307062551d311d8a5 / reason: a new page may owe a retention entry / applied: checked for a retention registry and per-doc frontmatter practice / result: none exists for this directory; no retention change needed, recorded not skipped / incomplete: None / by: readability-phase4-lane-d-implementer-c3 (Stage C)
skill@6a27b5c8e690b605d7dca4b0e4c2ff1d67dfa6ac6c18469d5657b4ff093339a4 / reason: the repository requires the skills-used record where a reader can see it / applied: emitted this six-field block bound to the manifest hashes / result: record present in this file and mirrored in the PR body's skills field / incomplete: None / by: readability-phase4-lane-d-implementer-c3 (Stage C)
```

## 14. Timing

- Work item named **LaneD-Phase4-Batch3** (Phase 4 re-read, lane D, batch 3: eight whole-page
  re-reads of the lane's fixed page range, evidence record only), started
  **2026-10-15T13:44:57-07:00** (America/Los_Angeles; the turn-1 snapshot).
- **Finish: `2026-10-15T13:57:46-07:00`** — the first head commit's own committer timestamp
  (`git log -1 --format=%cI 99d46d752357c6cb127274944ce2ac2ff0b9b78e`), the last recorded write of
  this lane; the pull request itself was opened at `2026-10-15T21:00:51Z` (`14:00:51-07:00`).
  **Wall time ≈ 12m 49s** from the stated start to that timestamp. (Corrected in revision 2: the
  first head said the figures were "recorded in the pull-request body", which the body did not do —
  SD-D F5. The same figures are stated in the body's timing bullet.) Active time was **not
  instrumented**, so wall time is an imperfect comparison with the estimate rule's active-time
  requirement and no per-page active rate is claimed.

## 15. What revision 2 did not verify (recorded here, not only in a message)

- It did **not** re-perform the eight pages' whole-page prose reads. It re-verified by command what
  is artifact-checkable: the flagged terms' line cites, the C-1 prevalence counts (section 4), the
  eight line counts and blob IDs, the lane derivation and batch boundaries, the six acceptance
  bullets' cited lines, every quoted span it touched, and the citations' provenance.
- It did **not** re-fetch the two external links (PR #122 on LD-17, PR #176 on LD-24); the record's
  own "external links were not fetched" statement stands and their live status is unverified.
- It did **not** run `build_index.py --write` and predicts **no** post-rebuild bucket figure. The
  published head expectation (654 / 57 / 4 / 587 / 0 / 0 / 6 / 597) still holds: the repair changes
  the same one file, appends no page and no row, and was re-measured at the new head.
- It did **not** read any other lane's record or pull request in full; it re-checked only the eight
  page paths and the figures this record states.
- It did **not** verify the coordinator's batch-3 brief: no tracked artifact at any ref carries it,
  so the record's quotations of it remain **unverifiable, not false**.
- It did **not** merge, rebase or move the derivation base, and did **not** resolve any merge
  conflict (that is the merge holder's step).
- It did **not** run the CI workflows locally; it read the run and check-run APIs at the new head
  after the push.

---

*Prepared by a **DeepSeek agent** (`deepseek-v4-pro`) operating under the owner account, as the
repository's attribution rule (2026-10-13) requires. **Revision 2 (2026-10-16) prepared by a
DeepSeek agent (`DeepSeek-4.1-Flash`, `deepseek-flash`)** under the same rule; the Stage D audit that
returned REVISE also ran on DeepSeek-4.1-Flash (deepseek-flash).*
