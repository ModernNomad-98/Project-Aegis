# Readability F1-F5 re-read — Stage C batch record, 2026-10-12

- **Lane:** READABILITY F1-F5 RE-READ — the four named follow-ups (F1-F4) recorded at PR #754's
  merge, plus the withheld item-2 row (F5) that PR #754 carried forward. **Stage:** C (IMPLEMENT).
- **Declared revision — the revision every read below was made at, and the revision the appended
  row binds:** `0237f611f718ed833935e72a0d98dd42362388a0` (`origin/main`; the PR #755 merge, whose first parent
  `75d185e65c0c0ebb303e37e9b39c7f3c635cc664` is the PR #754 merge). At this revision this ledger is
  **4,941 lines** and its blob is `1e0190ee3faea7dbde5b01384fa2cbc56c9783d7` — measured, and identical to the blob at the PR #754
  merge commit.
- **Reader / author identity: `readability-f1f5-implementer-c`.** A **different agent** from
  `readability-batches-implementer-c` (the writer of the ledger section that changed the page, and
  the reader of all four #753 passes), from `readability-closeout-implementer-c` and from
  `readability-closeout-repairer-c2` (the two writers of the ledger sections this lane dispositions).
  That independence is the binding constraint the F1-F5 lane was opened for, and it holds for every
  row this commit appends.
- **Plan applied:** `evidence/docs-refresh-2026-10-12/READABILITY-CLOSEOUT-PLAN-rev2.md`, declared
  digest `743b060a9654f1a9bde04ef269eb9027e4215584c1edd05fa491e2bc903a3664` — **items 2 and 3's
  remaining procedures** — plus the F1-F5 deferrals recorded in the PR #754 body (its "Intentionally
  not done / omitted" section and its Stage C2 repair notes R3 and R4).
- **What this page is.** The lane's batch record and the **evidence source** cited by the row this
  commit appends to the ledger keeper table, so the row's `Quote` is a verbatim fragment of a
  tracked page and this file **names the bound acceptance revision verbatim** (40 characters) in its
  own bytes, which `tools/readability_acceptance/build_index.py` L264-278 requires at `--ref`.

## 1. The instrument figures at the declared revision, quoted

```text
python -B tools/readability_acceptance/build_index.py --ref 0237f611f718ed833935e72a0d98dd42362388a0 --report
{ "built_at_ref": "0237f611f718ed833935e72a0d98dd42362388a0", "table_rows": 95, "events": 95,
  "full_page_acceptances": 75, "lost_commit_events": 10, "reader_pages_with_rows": 68 }
exit 0
```

```text
python -B tools/readability_acceptance/check_index.py --ref 0237f611f718ed833935e72a0d98dd42362388a0 --quiet
{ "compared_ref": "0237f611f718ed833935e72a0d98dd42362388a0", "reader_pages_in_tree": 644,
  "accepted_on_recorded_review": 60, "provably_pending": 1, "no_recorded_acceptance": 577,
  "recorded_acceptance_within_10_lines": 0, "within_10_not_covered_by_targeted_review": 0,
  "cannot_decide": 6, "official_pending_count": 584 }
exit 0
```

**These are the instrument's figures, not this lane's.** This record publishes no readability count
of its own (D84; ledger L19-31, L4730-4741) and predicts **no** post-commit bucket figure. The
figures **at this commit's head** are published in the Stage C record `READABILITY-F1F5-SD-C.md` and
in the pull request body, never inside the commit that produces them.

## 2. The roster, the concurrency, and the declared deviations

| Batch | Theme | Pages | Read at | Reader |
| --- | --- | ---: | --- | --- |
| R1 | F5 + F3 — this ledger's own owed whole-page re-read (item 2), which is also the P4 remnant | 1 | `0237f611f718ed833935e72a0d98dd42362388a0` | `readability-f1f5-implementer-c` |

**Concurrency: one reader, inside the three-reader ceiling** — the ceiling is a maximum, and a single
reader satisfies it by construction.

**Declared deviations (read honestly, not silently). Two, both measured facts about this session:**

1. **The reader is the same agent that writes this record and the ledger keeper section it rests
   on.** The plan section 5 table asks, for item 3, that the reader also differ from the writer of the
   keeper section the row rests on. A single-agent lane cannot satisfy that second clause; it is
   **not satisfied**. The clause the row turns on — the reader differs from
   `readability-batches-implementer-c` — **is** satisfied by a different agent again.
2. **F1, F2 and F4 are not discharged by this session.** P1, P3 and P7 were **not** read whole; they
   keep their named follow-ups (section 7) and get **no row**. The plan allows exactly this (N = 0-6;
   a page the reader does not accept gets a named follow-up instead of a row), and no page is
   asserted accepted on the strength of a partial read.

## 3. Per-page dispositions

Drift is `git diff --numstat <recorded acceptance> <declared revision> -- <page>`, added plus
deleted, re-measured this session at the declared revision. The recorded acceptances are the ones the
keeper table itself carries for these paths at that revision.

| # | Page | Lines at 0237f611f718 | Recorded acceptance | Drift to the declared revision | Disposition |
| --- | --- | ---: | --- | ---: | --- |
| P1 | `docs/roadmaps/aegis-backlog-forecast.md` | 5,118 | `de56b736c25a` | 118 / 0 = 118 | **not read — named follow-up (F1)** |
| P3 | `docs/reconciliation/step-0-reconciliation-v4.md` | 4,879 | `e5dbfe8a05f4` | 624 / 0 = 624 | **not read — named follow-up (F2)** |
| P4 | `docs/roadmaps/aegis-documentation-readability-backlog.md` | 4,941 | `2c6b6fc634d1` | 512 / 0 = 512 | **read whole — accepted, row K-076 (discharges F3 and F5)** |
| P7 | `docs/approvals/APPROVAL_REGISTER.md` | 5,939 | `de56b736c25a` | 611 / 5 = 616 | **not read — named follow-up (F4)** |

**The P4 arithmetic, split exactly as the plan requires.**

```text
git diff --numstat 2c6b6fc634d1e4e256abb5472208a3053a98ec55 0237f611f718ed833935e72a0d98dd42362388a0 -- docs/roadmaps/aegis-documentation-readability-backlog.md
512	0	docs/roadmaps/aegis-documentation-readability-backlog.md
git diff --numstat 2c6b6fc634d1e4e256abb5472208a3053a98ec55 f5ac84445c78cc7b5fb87e39757a43dc22ad75d7 -- <same path>   ->  355  0
git diff --numstat f5ac84445c78cc7b5fb87e39757a43dc22ad75d7 79c5c5901cd69101a58a696e0f03f1f7dd2264db -- <same path>   ->   78  0
git diff --numstat 79c5c5901cd69101a58a696e0f03f1f7dd2264db 0237f611f718ed833935e72a0d98dd42362388a0 -- <same path>   ->   79  0
```

512 = 355 + 78 + 79. The 355 is the drift the #753 lane's reader read whole; the 78 is #753's own
appended rows and keeper note; the 79 is the close-out lane's own keeper section and two rows
(K-074/K-075). **All three tranches are inside the 512 that this session read line by line**, so no
part of the acceptance rests on an earlier read, and the excluded already-read set is stated as
read-again rather than skipped.

## 4. Depth records

### 4.1 R1 — this ledger, P4, read whole and accepted

Two passes were made, and each is stated as what it is:

1. **Every line, exhaustively and mechanically**, at 0237f611f718: every Markdown link target
   and in-page anchor, every 40-character SHA-shaped token, every 7-12 character backticked SHA
   token. The mechanical figures quoted here are the lane's own narrower classifier and are a
   **candidate list, never a defect list**; the repository's own instrument is the adjudicating one.
2. **Every line, line by line, as prose at 0237f611f718 — L1-4941, the whole page.** Seven
   contiguous slices covered the file (L1-800, 720-1419, 1420-2079, 2080-2739, 2740-3479, 3480-4219,
   4220-4941, overlapping at the slice joins), and the three tool-output elisions those slices
   produced (inside the first, sixth and seventh slices) were **re-read inside the next slice**, so
   **no line of the page is unread**. The page's line count at this revision, 4,941, is
   `(Get-Content <page> -Encoding UTF8).Count` — the plan's declared convention, and the same
   convention that gives 5,118 / 4,879 / 5,939 for P1 / P3 / P7.

**The six acceptance bullets, addressed for the accepted page.**

| Bullet | P4 `docs/roadmaps/aegis-documentation-readability-backlog.md` |
| --- | --- |
| Purpose and audience up front | **yes** — L1-3 "Start here — current reading" states what the page is and, at L5-17, what the current reading is; L19-31 states in its first sentence that "**The index is now the count**", names the instrument, and says the ledger "publishes no count of its own and cites the index" (D84), before any dated history begins. The dated rounds that follow are labelled as dated history, oldest first, and say no dated snapshot is rewritten (L9-10). |
| Abbreviations and coded identifiers defined at first use | **yes** — the term block at L156-168 defines pull request (PR), commit SHA, the acceptance index, `check_index.py`, "a bound", the ledger keeper and AEGIS-APR-101 before those short forms carry weight, and the later 2026-10-12 sections keep the same discipline (`D84`, `D98`, `K-074/K-075`, "CARRY-WITH-DEVIATION" are each glossed where they first appear in the section that uses them). Coded identifiers are resolved to their own records rather than left bare: AEGIS-APR-101/113-118 to the approval register, D73/D83/D84 to `step-0-reconciliation-v4.md#5-recorded-decisions`. |
| Descriptive headings, lists or tables, and at least one concrete example | **yes** — every dated round is its own descriptive heading, the counting rules are set out as headed rule paragraphs ("Targeted edits to accepted pages", the net-difference decision, the generated-report class, the manual-only-marker decision), each keeper round carries a table with the column contract, and the concrete examples are worked numbers rather than abstractions: the 2026-10-03 premises correction re-derives `674 − 1 − 65 = 608` from a named command, and this page's own count-honesty block quotes the instrument's printed summary instead of asserting a figure. |
| Shipped behaviour separated from proposed or blocked behaviour | **yes** — accepted, pending, generated-report and classified-fixture are distinct states with their own rules, "IN PROGRESS" is the stated status of the sweep, the estimates are labelled historical or planning projections ("Those are planning projections, not measurements", L99-100), and the page states repeatedly what it does **not** do: it "confers nothing", grants no provider, private-input, real-host or deployment authority (L3018-3020), and the D98 note records that it "accepts only the reviewed-revision CONTENT at `ab7182d8`". |
| Navigation links current and every referenced file or command existing | **yes, read as a candidate list and adjudicated on the page's own terms** — every local link target in the accepted span resolves to a tracked path at 0237f611f718, and the in-page anchors the page itself uses (`#acceptance-for-each-page`, `#remaining-page-review-in-larger-batches`, the keeper-recording and premises-correction anchors) each resolve to a heading that exists in this file at this revision. The page also records which anchors it knows to be stale instead of silently rewriting them: the D98 named follow-up 3 is exactly a stale evidence-source anchor (rows L-001 to L-006 cite L2574/L2575), and it is carried forward below rather than repaired. |
| The non-author review itself | **this record**, with the staffing deviation in section 2 declared in terms |

**Purpose and normal use restated from the page alone** (the acceptance contract's own non-author
test, ledger L2860-2862):

- **P4 — *for*:** the repository-wide documentation acceptance ledger — the record of which reader
  pages have had an independent full-page re-read, at which revision, by whom, and with what
  evidence, together with the counting rules in force and the dated history of how those
  determinations were reached. Its normal use is: read L1-31 for the live reading and the
  official-count switch (the count is the instrument's printed summary at a pinned ref, D84, not
  this page's own figure), then read the rules in force under "Remaining-page review in larger
  batches" and "Acceptance for each page" before recording or checking anything, and read the foot
  of the page — the schema sentinel, the column contract and the consolidated keeper table — as the
  machine-readable index that `build_index.py` consumes. The dated rounds in between are history:
  they are consulted for *what happened when*, never for the current count, and no dated snapshot is
  rewritten.

**Disputed lines: none.** No line of the page was disputed without change, and no line of it was
edited by this lane. Where the page's own recorded defects remain open (the D98 follow-up 3 stale
anchors at rows L-001 to L-006, and the two dated-prose defects D98 recorded in chunk 4), they are
restated as open follow-ups in section 7 rather than altered.

### 4.2 F1, F2 and F4 — the three pages not read this session

- **P1 `docs/roadmaps/aegis-backlog-forecast.md` (5,118 lines)** — not read this session. F1.
- **P3 `docs/reconciliation/step-0-reconciliation-v4.md` (4,879 lines)** — not read this session. F2.
- **P7 `docs/approvals/APPROVAL_REGISTER.md` (5,939 lines)** — not read this session. F4.

Each keeps the plan's exclusion rule unchanged: its recorded-acceptance drift (`de56b736c25a`,
118 / 0; `e5dbfe8a05f4`, 624 / 0; `de56b736c25a`, 611 / 5 = 616) was read in full by the #753 lane
and needs no second read; what those three pages still owe is the remainder, read whole, by a reader
who is a different agent from `readability-batches-implementer-c` **and** from this session's
reader. No row is appended for any of them.

## 5. Stale / new / source rows

**Every line this lane changes.** `git diff --numstat 0237f611f718` at this commit's head:

| Path | Added | Deleted | Source |
| --- | ---: | ---: | --- |
| `docs/evidence/documentation/readability-f1f5-reread-2026-10-12.md` | new file | 0 | this record |
| `docs/roadmaps/aegis-documentation-readability-backlog.md` | appends only | 0 | one keeper section before the schema marker, one keeper row at end of file |

**Nothing else is in the diff.** No code, no workflow, no script, no `tools/` artifact, no JSON, and
no protected path — the lane is Markdown-only by construction, which is why the pull request answers
the security question `No`.

**Source rows.** The row's `Quote` string appears in section 9 byte-for-byte and names the full
40-character acceptance revision `0237f611f718ed833935e72a0d98dd42362388a0` verbatim, which `build_index.py` L275-278 requires in the
evidence source at `--ref`; the row's `Blob ID` is `git rev-parse 0237f611f718ed833935e72a0d98dd42362388a0:<ledger>` =
`1e0190ee3faea7dbde5b01384fa2cbc56c9783d7`, which L258-263 requires.

## 6. Named follow-ups

**Staffing bound.** Every row still owed by this program — F1, F2 and F4 — must be bound by a
**different agent** from this session's reader, exactly as PR #754's R4 note required of this lane.

1. **F1 — P1 `docs/roadmaps/aegis-backlog-forecast.md` whole-page prose read.** Owner: the next
   reader of this lane (a different agent from this one). Reason: not read this session; 5,118
   lines, recorded drift 118 / 0. No row.
2. **F2 — P3 `docs/reconciliation/step-0-reconciliation-v4.md` whole-page prose read.** Owner: the
   next reader. Reason: not read this session; 4,879 lines, recorded drift 624 / 0, no new section.
   No row.
3. **F4 — P7 `docs/approvals/APPROVAL_REGISTER.md` whole-page prose read.** Owner: the next reader.
   Reason: not read this session; 5,939 lines, recorded drift 611 / 5 = 616. No row. Read-only when
   it is done: the register is an append-only approval record and no reader may edit it.
4. **F5 — DISCHARGED by this commit.** The item-2 owed row for this ledger is appended as **K-076**,
   bound to `0237f611f718ed833935e72a0d98dd42362388a0` with `Blob ID` `1e0190ee3faea7dbde5b01384fa2cbc56c9783d7`: a **main-contained revision whose ledger blob equals
   the blob at the merged tip**, which is exactly the resolver PR #754's R3 note recorded, and
   **never** `e6b99cee35a5de99a31deda38308deb244083516` (the pre-#754 base blob the lane's own
   writes had already moved). **The plan-versus-artifact contradiction R3 raised is resolved by
   this binding:** plan AC6 (plan L607) named `e6b99cee…` as the blob item 2's row must equal, and
   that text cannot be satisfied by any row appended after #754 — so this lane binds the blob the
   tool actually derives at the declared revision, `git rev-parse 0237f611f718ed833935e72a0d98dd42362388a0:<ledger>`, and records the
   plan text as superseded on this point rather than dropping the discrepancy.
5. **F3 — DISCHARGED by this commit.** P4's remnant whole-page read is the same read as F5's: the
   page's bytes at `0237f611f718ed833935e72a0d98dd42362388a0` were read whole, L1-4941, including the 512-line excluded range, and the
   single accepted-page row **K-076** is that read's record.
6. **F6 (carried, not this lane's) — the D98 follow-up 3 stale evidence-source anchors.** Rows L-001
   to L-006 in the consolidated keeper table cite `docs/roadmaps/aegis-documentation-readability-backlog.md:2574`
   and `:2575` as their evidence source; at the declared revision those lines hold other text, so the
   citation is stale and the tool's own quote check is what the rows actually pass through. Recorded
   by the D98 note; **re-verified as still open this session** and left untouched, because a dated
   record row is never edited in place. Owner: the ledger keeper, in a future keeper round.
7. **F7 (carried, not this lane's) — item 1, the index rebuild.** **Closed at this base**: PR #755
   merged as `0237f611`, the very revision this lane declares, and its diff over its first parent is
   the two `tools/readability_acceptance/` JSON artifacts only. Recorded here as closed so the lane's
   own record does not re-open it; **no `--write` was run by this lane**.

## 7. Count honesty

- **This lane publishes no readability count of its own** and cites the instrument (D84).
- The instrument classifies the page tree at `--ref` and reads the recorded acceptances from the
  **committed** `acceptance-index.json`. The row appended here **changes nothing until a further
  rebuild**, and a rebuild can only be run after the commit that carries the row, because
  `build_index.py` stamps its own `built_at_ref`; the two resolvers this ledger already names
  (L4671-4673) apply — a two-commit follow-up, or a merger-side rebuild at the merged tip (D73 row 8).
- The base figures in section 1 are the instrument's printed output at the declared revision,
  quoted **as the instrument's figures**, and **no post-commit bucket figure is predicted** anywhere
  in this record.

## 8. The row-quote string, verbatim

The line below appears in this file byte-for-byte and is copied verbatim into the ledger row **K-076**.
It also contains the full 40-character acceptance revision, the second binding rule the validator
enforces.

```text
K-076 accepted: docs/roadmaps/aegis-documentation-readability-backlog.md read whole at 0237f611f718ed833935e72a0d98dd42362388a0
```

## 9. What this lane did not do

It rewrote no dated snapshot; edited, reordered or deleted no existing keeper row; edited none of the
four named pages (the approval register among them is **read only** if it is ever read); appended no
acceptance row this record does not support; bound no row to this commit's own SHA; ran no
`build_index.py --write` and rebuilt no `tools/` artifact; touched no `.github/workflows/` path; and
claims no authority beyond recording. The batching procedure does not grant provider, private-input,
real-host or deployment authority (ledger L3018-3020).
