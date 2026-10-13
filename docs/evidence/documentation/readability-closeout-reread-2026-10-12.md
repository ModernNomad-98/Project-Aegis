# Readability close-out follow-ups — Stage C batch record, 2026-10-12

- **Lane:** READABILITY CLOSE-OUT FOLLOW-UPS (the four OWED residuals recorded at PR #753 merge). **Stage:** C (IMPLEMENT). **Base = declared revision:**
  `79c5c5901cd69101a58a696e0f03f1f7dd2264db` (`origin/main`, the PR #753 merge; first parent
  `f5ac8444`, second parent `80d406b6`).
- **Plan applied:** `evidence/docs-refresh-2026-10-12/READABILITY-CLOSEOUT-PLAN-rev2.md`,
  declared digest `743b060a9654f1a9bde04ef269eb9027e4215584c1edd05fa491e2bc903a3664`, **re-verified this
  session over the bytes strictly above the footer `---` rule (lines 1-846 + LF)**. **Stage B:**
  **SD-B ACCEPT** (`READABILITY-CLOSEOUT-AUDIT-B-rev2.md`, declared digest
  `134618dbd7a0a4a8cde96bfdbb0ef0c1ec7ad440faed7b2c2600fc893cd08e3f`, **re-verified** the same way,
  over its own footer rule at line 418).
- **What this page is.** The lane lane batch record and the **evidence source** cited by every row this
  lane appends to the ledger keeper table, so each row Quote can be a verbatim fragment of a tracked
  page (ledger L4694-4695) and this file **names every row acceptance revision verbatim** (40
  characters) in its own bytes, which `build_index.py` L264-278 requires at `--ref`.

## 1. The instrument figures at the declared revision, quoted

```text
python -B tools/readability_acceptance/build_index.py --ref 79c5c5901cd69101a58a696e0f03f1f7dd2264db --report
{ "built_at_ref": "79c5c5901cd69101a58a696e0f03f1f7dd2264db", "table_rows": 93, "events": 93,
  "full_page_acceptances": 73, "lost_commit_events": 10, "reader_pages_with_rows": 68 }
exit 0
```

```text
python -B tools/readability_acceptance/check_index.py --ref 79c5c5901cd69101a58a696e0f03f1f7dd2264db --quiet
reader_pages_in_tree 643, accepted_on_recorded_review 43, provably_pending 8,
no_recorded_acceptance 576, recorded_acceptance_within_10_lines 10,
within_10_not_covered_by_targeted_review 10, cannot_decide 6, official_pending_count 600
exit 0
```

**These are the instrument figures, not this lane own.** This record publishes no readability count of
its own (D84; ledger L19-31, L4730-4741) and predicts **no** post-rebuild bucket count.

## 2. The roster, the concurrency, and the declared deviations

| Batch | Theme | Pages | Read at | Reader |
| --- | --- | ---: | --- | --- |
| R1 | the two shortest remnants (P2, P6) | 2 | `79c5c590` | `readability-closeout-implementer-c` |
| R2 | the ledger own owed whole-page re-read (item 2) | 1 | `80d406b6` = `79c5c590` bytes | `readability-closeout-implementer-c` |
| R3 | the four long remnants (P1, P3, P4 remainder, P7) | 4 | `79c5c590` | `readability-closeout-implementer-c` |

**Concurrency: one reader, well inside the three-reader ceiling** — the ceiling is a maximum, and a
single reader satisfies it by construction. **The reader is a different agent from
`readability-batches-implementer-c`**, the writer of the section that changed the ledger and the reader
of all four #753 passes: that is the eligibility clause items 2 and 3 both turn on, and it holds.

**Declared deviations (read honestly, not silently).** Three, and each is a measured fact about how
this lane was staffed and how far its read got — not a claim that the plan text was satisfied:

1. **The reader is the same agent that writes this lane keeper section and this record.** The plan
   section 5 table asks, for item 3, that the reader also differ from the writer of the keeper section
   the row rests on. This lane staffs one agent, so that second clause is **not satisfied**; AC7 and AC9
   are graded by Stage D against this sentence. The first clause (different from
   `readability-batches-implementer-c`) **is** satisfied.
2. **Item 2 whole-page re-read of the ledger is NOT complete** (see section 4.2 and follow-up F5).
   The owed acceptance row for `docs/roadmaps/aegis-documentation-readability-backlog.md` is therefore
   **not appended** by this commit. The plan formula `93 + 1 + N + M` carries that `+1` as **0 here**,
   and the measured instrument output in section 1 is the authority for the count.
3. **Item 3 accepted 2 of the 6 remnant pages** (P2 and P6). The other four (P1, P3, P4 remainder, P7)
   are recorded as **named follow-ups**, never as accepted pages, because their whole-page prose read
   was not completed in this session. The plan allows exactly this: N = 0-6, and a page the reader does
   not accept gets a named follow-up instead of a row (plan section 4.2 step 4).

**Coordinator decision, recorded 2026-10-12 and relayed to the Stage C2 repair: CARRY-WITH-DEVIATION
for the two appended rows.** Rows **K-074/K-075 stand**, with deviation 1 above declared rather than
hidden. The unmet second eligibility clause (reader ≠ this lane keeper-section writer) touches a
*disclosure* — this record states it in terms — not a false acceptance assertion, and the clause the two
rows turn on, **reader ≠ `readability-batches-implementer-c`**, **is** satisfied; that is the same
disposition the #753 lane's Stage D took on the identical second-clause failure — **"ACCEPT with the
deviation recorded"** (`READABILITY-BATCHES-AUDIT-D.md` F-A1) — and it is why the rows are carried rather
than withheld. **The remedy is staffing, not withdrawal: the ledger own owed row (F5) and any row for the
four unread pages (F1-F4) must be bound by a DIFFERENT agent from this session's reader.** AC7 and AC9
stay **NOT MET** as written either way.

## 3. Per-page dispositions

Drift is `git diff --numstat <recorded acceptance> <ref> -- <page>`, added plus deleted, re-measured at
`79c5c590` this session; every figure reproduces the plan section 4.1 table exactly.

| # | Page | Recorded acceptance | Drift at `f5ac8444` | Drift at `79c5c590` | New section | Disposition |
| --- | --- | --- | ---: | ---: | --- | --- |
| P1 | `docs/roadmaps/aegis-backlog-forecast.md` | `de56b736c25a` | 118 / 0 = 118 | 118 / 0 = 118 | yes | **needs a named follow-up (F1)** |
| P2 | `docs/roadmaps/behavioral-eval-runner-backlog.md` | `de56b736c25a` | 157 / 0 = 157 | 157 / 0 = 157 | yes | **accepted** (row K-074) |
| P3 | `docs/reconciliation/step-0-reconciliation-v4.md` | `e5dbfe8a05f4` | 624 / 0 = 624 | 624 / 0 = 624 | no | **needs a named follow-up (F2)** |
| P4 | `docs/roadmaps/aegis-documentation-readability-backlog.md` | `2c6b6fc634d1` | 355 / 0 = 355 | 433 / 0 = 433 | yes | **needs a named follow-up (F3)** |
| P6 | `docs/delivery-workflow.md` | `db49ca280c6f` | 158 / 6 = 164 | 158 / 6 = 164 | yes | **accepted** (row K-075) |
| P7 | `docs/approvals/APPROVAL_REGISTER.md` | `de56b736c25a` | 611 / 5 = 616 | 611 / 5 = 616 | yes | **needs a named follow-up (F4)** |

**The P4 arithmetic, split as the plan requires.** `2c6b6fc634d1..79c5c590` is **433 / 0**;
`2c6b6fc634d1..f5ac8444` is **355 / 0**; and `f5ac8444..79c5c590` is **78 / 0**, the only one of the six
paths that moved in that interval (the other five return no numstat row). 433 = 355 + 78. The 78 lines
are #753 own appended rows and keeper note; they lie inside the ledger blob `e6b99cee35a5de99a31deda38308deb244083516`
and are **excluded as already read** for P4 purposes.

**The instrument corroborates the decode.** `check_index.py --ref 79c5c590` lists P3 `624`, P7 `616`, P4
`433`, P6 `164`, P2 `157`, P1 `118` in its own added+del column — the record shorthand `+6` (P6) and `+5`
(P7) are the deleted columns, and the changed-line totals are 164 and 616, as the plan section 4.1 says.

## 4. Depth records

### 4.1 R1 — the two pages read whole, and accepted

Two complementary passes were made over each accepted page, and each is stated as what it is:

1. **Every line, exhaustively and mechanically**, at `79c5c590`: every Markdown link target and
   in-page anchor, every 40-character SHA-shaped token, every 7-12 character backticked SHA token,
   each resolved offline against the local Git object store at that revision. Figures in section 4.3.
2. **Every line, line by line, as prose at `79c5c590`** — the read this item exists to supply.
   - **P2, `docs/roadmaps/behavioral-eval-runner-backlog.md` (4,207 lines): L1-4207.** Eight contiguous
     slices covered the whole file. Two tool-output elisions inside the first slice (L328-349 and
     approximately L690-700) were **re-read** inside the second slice (L320-870), so no line of the
     page is unread. The excluded already-read set is the recorded drift `de56b736c25a..f5ac8444`,
     **157 / 0**, which #753 read in full; the P2 remainder is L1-4207 less those changed lines.
   - **P6, `docs/delivery-workflow.md` (1,141 lines): L1-1141**, in two slices, no elision anywhere.
     The excluded already-read set is the recorded drift `db49ca280c6f..f5ac8444`, **158 / 6 = 164**;
     the P6 remainder is the rest of the page, including its dated adoption history.

**Count convention (R1).** Both figures are `(Get-Content <page>).Count` at `79c5c590` — the plan's own
declared convention, and the plan's table gives the same two figures — and each equals the file's
newline count: **4,207** for P2 and **1,141** for P6.

**The six acceptance bullets, addressed for each accepted page.**

| Bullet | P2 (behavioral-eval-runner-backlog.md) | P6 (delivery-workflow.md) |
| --- | --- | --- |
| Purpose and audience up front | yes — L3-9 current-reading banner names maintainers and coding agents, and L13-33 expands BER, WP, BKL, BER-DEC, APR, PR, OD-1, R1-R5, CI, NON-LIVE, NON_BASELINE, POSIX, holdout, MCP, OS, DCO, SDK, API, JSON, YAML and UTC at first use | yes — L3-10 reading key defines PR, CI, head, SHA, Role A, Role B and MANUAL-ONLY before any use, and L12-18 states the page is the canonical normative rule and what it binds |
| Abbreviations and coded identifiers defined at first use | yes — the L13-33 key above, plus status vocabulary (L300-335) and priority vocabulary (L337-353), which spell out every status token a record can carry | yes — every stage token (SD-A..SD-G) and gate token (MG1..MG5) is defined once in its normative block and used elsewhere as an ID only |
| Descriptive headings, lists or tables, and at least one concrete example | yes — headed registers throughout, and a worked numeric example at L2389-2416 (one selected case that preflight excludes: selected_coverage 0.2, runnable_coverage 0.5, execution_coverage 0, with the aggregate re-derivation and the rejected PASS claim) | yes — headed sections plus tables, and concrete worked text: the MG4 verbatim quotation (L369-372), the two agreement-check greps (L984-985) and the per-marker divergence method (L318-341) |
| Shipped behaviour separated from proposed or blocked behaviour | yes — DONE / AUTHORIZED / BLOCKED / BACKLOG / PROHIBITED are distinct and each record states which; the simulated and mock scopes are labelled non-live | yes — procedural versus machine-enforced is its own section (L750-810), and the lighter docs-only path is bounded in its own section (L391-482) |
| Navigation links current and every referenced file or command existing | **P2: 107 links checked, 30 anchors checked, 0 broken, 0 dead** — the repository's own instrument, `python -B scripts/ci/check-markdown-links.py --json docs/roadmaps/behavioral-eval-runner-backlog.md`, prints `{"anchors": 30, "broken": 0, "checked": 107, "dead": 0, "external": 78, "files": 1, "skipped": 0}` at exit 0; `../../tools/behavioral_eval_runner/schemas/` is an existing directory, which that instrument's contract treats as a valid target | **P6: 10 links checked, 69 anchors checked, 0 broken, 0 dead** — `python -B scripts/ci/check-markdown-links.py --json docs/delivery-workflow.md` prints `{"anchors": 69, "broken": 0, "checked": 10, "dead": 0, "external": 0, "files": 1, "skipped": 0}` at exit 0; the cross-file anchor `reconciliation/step-0-reconciliation-v4.md#5-recorded-decisions` resolves on the linked page |
| The non-author review itself | this record, with the staffing deviation in section 2 | same |

**Purpose and normal use restated from each page alone** (the acceptance contract own non-author test, ledger L2860-2862):

- **P2** — *for:* the durable continuation and decision register for Behavioral Eval Runner maintainers
  and coding agents: what remains, under which recorded authorization, and what may not begin yet.
  *Normal use:* read the L3-9 current-reading banner and the L35-41 status map first, then the owning
  work-package record in section 7 before treating older conditional wording as today status; nothing
  in it authorizes a provider call, private input or live run.
- **P6** — *for:* the seven-stage rule that governs every change in this source repository, including
  the pure-docs lighter path, the bound PR-body fields and what CI does and does not enforce.
  *Normal use:* identify the stage the work is in, take the skill that owns that stage after checking
  its scope, and produce that stage stated evidence; read the MG block before merging.

### 4.2 R2 — item 2, the ledger own owed row: NOT completed, and why

The plan section 3.2 requires the row binder to re-read the ledger **whole** at the bound revision
exact bytes. This session read, at the bytes of blob `e6b99cee35a5de99a31deda38308deb244083516` (identical
at `80d406b6` and `79c5c590`, both measured):

- **in full: L1-3054 and L3130-3450, plus L4650-4780** — the live reading, the purpose and acceptance
  sections, the counting rules in force, the dated per-PR accounting, the D98 full-page re-read
  section, and the consolidated keeper table head and column contract;
- **not read: L3055-3129, L3451-4649 and L4781-4862** — **1,356** of the page's 4,862 lines
  (75 + 1,199 + 82; the read ranges total 3,506, and 3,506 + 1,356 = 4,862), overwhelmingly the long
  per-batch table rows and the dated keeper sections that follow them.

**Disposition: the whole-page read is NOT complete, so no acceptance row is claimed for this page.**
The item 2 row stays **owed**, exactly as #753 recorded it, and F5 names it. Writing the row anyway would
be the defect class this program exists to prevent: the ledger records repeatedly that a partial or
targeted read cannot confer full-page acceptance (L2943-2947, L4707-4712, L2492-2495).

### 4.3 R3 — the four long remnants: not read, and named as follow-ups

- **P1 `docs/roadmaps/aegis-backlog-forecast.md` (5,118 lines)** — not read this session. F1.
- **P3 `docs/reconciliation/step-0-reconciliation-v4.md` (4,879 lines)** — not read this session. F2.
- **P4 `docs/roadmaps/aegis-documentation-readability-backlog.md` (4,862 lines)** — read only to the
  extent recorded in section 4.2, which is not whole. F3.
- **P7 `docs/approvals/APPROVAL_REGISTER.md` (5,939 lines)** — not read this session. F4.

**The mechanical pass, by contrast, covered all six pages at 100 per cent of their lines.** Measured at
`79c5c590`:

| Page | Lines | Local links | Links resolved (lane classifier) | Anchors checked | Anchors resolved (same-page) | 40-hex tokens | 7-12 hex tokens |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P1 | 5,118 | 314 | 314 | 173 | 40 | 209 | 34 |
| P2 | 4,207 | 107 | 106 | 30 | 7 | 39 | 6 |
| P3 | 4,879 | 78 | 77 | 26 | 5 | 5 | 63 |
| P4 | 4,862 | 589 | 589 | 143 | 86 | 138 | 412 |
| P6 | 1,141 | 10 | 10 | 69 | 68 | 0 | 0 |
| P7 | 5,939 | 54 | 54 | 15 | 2 | 138 | 35 |

Object resolution over all 961 distinct 40-hex and 7-12-hex tokens found across the six pages: **896
resolve in the local object store, 65 do not** — the two known lost commits the keeper table records as
lost-commit events (`65bacc7d6b85…`, `d3dcb62a335d…`), the unreachable grant revision
`9644ef079db763802223180ae5b11af39919c781` that #753 named as follow-up 1, and historical
pre-rebase or abbreviated objects. The anchor column is deliberately read as a **candidate list, not a
defect list**: a cross-file anchor names a heading on the linked page, and only the counts for the two
accepted pages were adjudicated line by line (section 4.1). No page in this table is accepted on the
strength of the mechanical pass alone.

**The two accepted pages' link and anchor dispositions are read from the repository's own instrument,
not from this record's narrower classifier.** For P2 and P6 the adjudicating instrument is
`python -B scripts/ci/check-markdown-links.py --json <page>`: it reports **P2 `checked 107 / anchors 30 /
broken 0 / dead 0`** and **P6 `checked 10 / anchors 69 / broken 0 / dead 0`**, both at exit 0
(section 4.1). An existing directory is a valid target under that instrument's own contract, and the P6
cross-file anchor resolves on the linked page. The `Links resolved (lane classifier)` and
`Anchors resolved (same-page)` columns above are this record's own narrower mechanical classification —
a link counts only when its target is an existing **file**, an anchor only when it sits on the **same
page** — so they are a candidate list, never a defect list, and they carry **no** unresolved-link or
dead-anchor claim about any page.

## 5. Stale / new / source rows

**Every line this lane changes.** `git diff --numstat 79c5c590` at Stage C's commit head
(`c2916d29`; the Stage C2 repair's cumulative figures are in section 10):

| Path | Added | Deleted | Source |
| --- | ---: | ---: | --- |
| `docs/evidence/documentation/readability-closeout-reread-2026-10-12.md` | new file | 0 | this record |
| `docs/roadmaps/aegis-documentation-readability-backlog.md` | appends only | 0 | one keeper section before the schema marker, two keeper rows at end of file |
| `docs/offline-ci.md` | 2 | 2 | item 4, the artifact-pin correction |
| `docs/roadmaps/aegis-ci-baseline-2026-10-11.md` | appends only | 0 | item 4, the AC14 appended dated note |

**Every line a reader disputed without changing** — this lane disputes no line and edits no read page.
The four unread remnants are recorded as follow-ups, not as defects.

**Source rows.** Each accepted row Quote string appears in section 8 byte-for-byte and each names the
full 40-character acceptance revision `79c5c5901cd69101a58a696e0f03f1f7dd2264db` verbatim, which
`build_index.py` L275-278 requires in the evidence source at `--ref`.

## 6. Named follow-ups

**Staffing bound to the coordinator's decision (section 2):** every row this record still owes — F5's
ledger row and any row for the four pages named in F1-F4 — must be bound by a **different agent** from
this session's reader.

1. **F1 — P1 `docs/roadmaps/aegis-backlog-forecast.md` whole-page prose read.** Owner: the next reader
   of this lane (a different agent from this one). Reason: not read this session; the page is 5,118
   lines and its recorded drift is 118 / 0. No row is appended.
2. **F2 — P3 `docs/reconciliation/step-0-reconciliation-v4.md` whole-page prose read.** Owner: the next
   reader. Reason: not read this session; 4,879 lines, drift 624 / 0, no new section.
3. **F3 — P4 `docs/roadmaps/aegis-documentation-readability-backlog.md` remnant whole-page prose read.**
   Owner: the next reader. Reason: read only to the extent recorded in section 4.2 (L1-3054,
   L3130-3450, L4650-4780 of 4,862); the excluded already-read set is the full `2c6b6fc634d1..79c5c590`
   drift, 433 / 0, of which 78 / 0 is #753 own append.
4. **F4 — P7 `docs/approvals/APPROVAL_REGISTER.md` whole-page prose read.** Owner: the next reader.
   Reason: not read this session; 5,939 lines, drift 616 = 611 / 5.
5. **F5 — item 2, the ledger own acceptance row, still WITHHELD and OWED (1).** Owner: the coordinator
   or the merger at the merged tip. Reason: the whole-page re-read this row requires is not complete
   (section 4.2). **Resolver, corrected by the Stage C2 repair to be blob-bound:** a post-merge row
   bound to a main-contained revision **whose ledger blob equals the blob at the merged tip** — never
   `e6b99cee35a5de99a31deda38308deb244083516`, the *base* blob this lane own append has already moved
   (at `c2916d29` the ledger blob this commit reads is `529b91d39ac789f54b86133b46994f3f92f1246f`, and
   this repair commit moves it again, so at any later head the resolver is that head's blob, whatever
   it is) — or the merger-side rebuild practice (D73 row 8). **Plan-inherited contradiction, recorded
   for the coordinator and not dropped:** the plan AC6 text (plan L607) names `e6b99cee…` as the blob
   item 2's row must equal, so AC6 as written cannot be satisfied by any row appended after this
   commit; that plan-versus-artifact conflict is the coordinator's to resolve before the row is bound.
   Until the row exists the ledger stays inside the instrument provably-pending bucket.
6. **F6 — deleted by the Stage C2 repair (2026-10-12); recorded, not silently dropped.** The former F6
   named a P2 directory link and a P6 cross-file anchor as unresolved work. The repository's own
   instrument reports both accepted pages `broken: 0, dead: 0` (section 4.1), so there is nothing left
   to follow up. **F7 keeps its number** so every existing reference to it stays valid.
7. **F7 — item 1, the index rebuild.** Owner: the rebuild holder (never the coordinator, never a holder
   of another stage of that pull request; D73 row 9). Reason: the rows this commit appends are not
   machine-visible until `build_index.py --write --ref <the rebuild pull request base commit on the
   default branch>` runs at a ref that contains them. **No `--write` was run in this commit** (plan
   section 2.3), and the JSON artifacts are untouched.

## 7. Count honesty

- **This lane publishes no readability count of its own** and cites the instrument (D84).
- The instrument classifies the page tree at `--ref` and reads the recorded acceptances from the
  **committed** `acceptance-index.json`. So the rows appended here **change nothing until the rebuild**
  (F7); the only movement at this head is this lane own **new evidence page**, which enters
  `no_recorded_acceptance`.
- The measured figures at the base are section 1 exactly as the instrument printed them. **The figures
  at this commit head, and the head expectation, are published only as the commands own output** —
  they cannot be stated inside the commit that produces them (a commit cannot name its own SHA in its
  own bytes), so they are recorded in the Stage C record `READABILITY-CLOSEOUT-SD-C.md` and in the
  pull request body, not here.
- **No post-rebuild count is predicted** — the plan formula `93 + 1 + N + M` is arithmetic, not a
  measurement, and this lane publishes the measurement alone.

## 8. The row-quote strings, verbatim

Each line below appears in this file byte-for-byte and is copied verbatim into the ledger row whose
stable ID is prefixed by the same page label. Every line also contains the full 40-character
acceptance revision, the second binding rule the validator enforces.

```text
P2 accepted: docs/roadmaps/behavioral-eval-runner-backlog.md read whole at 79c5c5901cd69101a58a696e0f03f1f7dd2264db
P6 accepted: docs/delivery-workflow.md read whole at 79c5c5901cd69101a58a696e0f03f1f7dd2264db
```

## 9. What this lane did not do

It rewrote no dated snapshot; edited, reordered or deleted no existing keeper row; edited none of the
six remnant pages; appended no acceptance row this record does not support; bound no row to this
commit own SHA; ran no `build_index.py --write` and rebuilt no `tools/` artifact; touched no
`.github/workflows/` path; and claims no authority beyond recording. The batching procedure does not
grant provider, private-input, real-host or deployment authority (ledger L3018-3020).

## 10. The Stage C2 repair (2026-10-12), recorded

A second, different agent (`readability-closeout-repairer-c2`) discharged the Stage D `SD-D REVISE`
items R1-R4 in a second commit on this pull request, after this record was first published. (These
Stage D revision labels are distinct from the roster batches R1-R3 in section 2.):

- **R1** — the two accepted pages' line counts and read ranges are corrected in place to **4,207 /
  L1-4207** (P2) and **1,141 / L1-1141** (P6), and item 2's unread total to **1,356** lines
  (**L4781-4862**); the same figures are corrected in the ledger keeper section this pull request adds.
- **R2** — section 4.1's navigation bullet now carries the repository instrument's own disposition for
  both accepted pages, and the former F6, which rested on the narrower classifier, is deleted with its
  number tombstoned so F7's references stay valid.
- **R3** — F5's resolver is blob-bound: the owed row must bind the ledger blob at the merged tip, never
  the base blob `e6b99cee…`; the plan AC6 contradiction (plan L607 names `e6b99cee…`) is recorded for
  the coordinator rather than dropped.
- **R4** — the coordinator's CARRY-WITH-DEVIATION decision for rows K-074/K-075 is recorded in section 2
  above and in the ledger keeper section, with the staffing remedy that binds F1-F5's rows.

**The ledger path's cumulative figures over `79c5c590`, for the re-audit.** `git diff --numstat
79c5c590 -- docs/roadmaps/aegis-documentation-readability-backlog.md` prints **79 / 0** (the keeper
section plus the two rows, additions only); `git diff -U0` prints exactly two hunks,
`@@ -4747,0 +4748,77 @@` and `@@ -4862,0 +4940,2 @@`, with **0 deletion lines**; the ledger at the
repaired head is **4,941 lines**, blob `1e0190ee3faea7dbde5b01384fa2cbc56c9783d7`. The other two paths
keep Stage C's figures (`2 2` for `docs/offline-ci.md`, `23 0` for
`docs/roadmaps/aegis-ci-baseline-2026-10-11.md`). The pull request body's Stage C2 notes carry the same
four items and re-derive its 16-hex bound-field digest (placeholder convention). **The Stage D re-audit
this repair owes binds to the repaired head, not to the head this record was first written against.**
