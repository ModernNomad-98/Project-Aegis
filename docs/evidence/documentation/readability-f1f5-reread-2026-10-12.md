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

**Declared deviations (read honestly, not silently). Three, all measured facts:**

1. **The reader is the same agent that writes this record and the ledger keeper section it rests
   on.** The plan section 5 table asks, for item 3, that the reader also differ from the writer of the
   keeper section the row rests on. A single-agent lane cannot satisfy that second clause; it is
   **not satisfied**. The clause the row turns on — the reader differs from
   `readability-batches-implementer-c` — **is** satisfied by a different agent again.
   **Restated as an exposure against the register's own text (carried exposure E-3).**
   `docs/approvals/APPROVAL_REGISTER.md:3155` (AEGIS-APR-101, at the bound revision
   `0237f611f718`) requires that "the keeper must be a different agent from the page's author and
   accepting reviewer", and permits the keeper only to record an existing qualifying decision rather
   than to confer acceptance. For **K-076** the reviewer cell and the writer of the keeper section the
   row rests on are the **same** agent, `readability-f1f5-implementer-c`, so **that condition is not
   satisfied on the register's text** and this row is **not green**. It is also not hidden: the same
   pattern was declared for `K-074`/`K-075` and carried by the coordinator ruling recorded in
   `READABILITY-CLOSEOUT-AUDIT-D2.md` (*AC7/AC9 "declared deviation, coordinator ruling (a)
   CARRY-WITH-DEVIATION; remedy is staffing"*), and this lane is carried the same way — as a
   **CARRY-WITH-DEVIATION under that SD-D2 coordinator-ruling precedent**, which covers the *carry* and
   does not itself satisfy the register condition. Disposing of the **authority question** is left where
   the authority sits: the merge holder disposes of it under AEGIS-APR-100 (the standing commit, push
   and merge pre-approval), by either citing the authority that permits a same-agent recording at this
   head or withholding the row for an eligible keeper to re-record. This record claims no such
   authority.
2. **F1, F2 and F4 are not discharged by this session.** P1, P3 and P7 were **not** read whole; they
   keep their named follow-ups (section 7) and get **no row**. The plan allows exactly this (N = 0-6;
   a page the reader does not accept gets a named follow-up instead of a row), and no page is
   asserted accepted on the strength of a partial read.
3. **Two of the six acceptance-bullet dispositions for the accepted page are partial, and the page's
   own text was not rewritten to make them unqualified.** The "purpose and audience up front" bullet
   and the "abbreviation or coded identifier at first use" bullet are recorded as **partial —
   deviation declared** in the six-bullet table at the end of section 4.1, with the facts each turns
   on (L1-17 names no intended audience; the page's first `PR` token is L14 against the definition at
   L156). Both are properties of the page's text at the bound revision, which this lane may not
   rewrite, so they are declared as deviations rather than repaired; item 2 of section 4.1 states them
   in full.

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

Four numbered items follow, and each is stated as what it is: item 1 records the coverage corrections
this lane has made (the Stage C2 round's and this Stage C3 round's), and item 2's two partial bullet
dispositions are declared in section 2 deviation 3.

1. **The coverage sentence in section 4.1 item 4 needed correction, and it is corrected there — twice.**
   The item asserted that three tool-output elisions were "re-read inside the next slice", that the
   slices overlapped at their joins, and it concluded "no line of the page is unread".
   The Stage C2 round replaced the mechanism sentence and named three elisions; the Stage E2 verdict
   (`READABILITY-F1F5-VALIDATE-E2.md`, item R-1) then showed that (a) the join-overlap clause
   survived at L138 and is false — only the L720-800 join overlaps — (b) the seventh slice's elided
   L4845-4895 cannot have been displayed by the call at L4896-4941, and (c) a **fourth, larger**
   elision, **L3058-3479 (422 lines)**, was named by no read at all, so the coverage sentence was
   false by 422 lines. Item 4 now states all **four** capped slices by their exact line ranges with
   the read that displayed each, and both the "next slice" and the join-overlap wording are gone.
   This Stage C3 round read **L3058-3479** directly at the bound revision, which is what closes that
   band. Declared here because the Stage E item E-1 and its re-validation item R-1 rest on the
   correction.
2. **Two of the six acceptance-bullet dispositions are partial, not unqualified.** See the six-bullet table at the end of section 4.1:
   the "purpose and audience up front" bullet is **partial** (no intended audience is named in L1-17)
   and the "abbreviation or coded identifier at first use" bullet is **partial** (the page's first `PR`
   token is at L14; the definition is at L156).
3. **Every line, exhaustively and mechanically**, at 0237f611f718: every Markdown link target
   and in-page anchor, every 40-character SHA-shaped token, every 7-12 character backticked SHA
   token. The mechanical figures quoted here are the lane's own narrower classifier and are a
   **candidate list, never a defect list**; the repository's own instrument is the adjudicating one.
4. **Every line, line by line, as prose at 0237f611f718 — L1-4941, the whole page.** Seven
   contiguous slices covered the file (L1-800, 720-1419, 1420-2079, 2080-2739, 2740-3479, 3480-4219,
   4220-4941); only the 1-to-2 join overlaps (at L720-800) and the other five joins abut exactly, so
   the slices' union is L1-4941 and no join hides a line — the earlier claim that the slices
   overlapped at their joins was false for five of the six joins and is deleted here. **Four of the seven slices
   were capped**, and the four elisions they produced are named below by exact range, each with the
   read that displayed it — never merged into one claim:
   **first slice (L1-800): L786-800** — 15 lines; the read stopped at L785 under a per-call output
   cap, and these 15 lines were displayed by the reader's own subsequent read call at L720-1419.
   **fifth slice (L2740-3479): L3058-3479** — **422 lines, the largest of the four**; the read stopped
   at L3057 with "Use offset=3058 to continue", and no read in the reader's session **and no read in
   the Stage C2 round** displayed them — established by the Stage E2 verdict
   (`READABILITY-F1F5-VALIDATE-E2.md` section 3.3) on three independent observations (the cap marker
   and its offset, the absence of any covering call in that session, and the absence of twelve
   distinctive probes drawn from the band across that session's whole transcript and all eleven of its
   spill files). This record's earlier "three elisions" accounting omitted that band, so its "no line
   of the page is left unread" sentence was **false by 422 lines** as it stood. **The Stage C3 repair
   round (this one) read the band directly:** this round extracted the page's bytes at `0237f611f718`
   (`git show`, 4,941 lines, `git hash-object` = `1e0190ee3faea7dbde5b01384fa2cbc56c9783d7`) and
   displayed **L3058-3479** in its own read calls, in eleven chunks (L3058-3107, 3108-3157, 3158-3197,
   3198-3237, 3238-3277, 3278-3317, 3318-3357, 3358-3397, 3398-3437, 3438-3477, 3478-3479). The first
   attempt to display the whole band in one step was itself capped by that session's own output limit
   (1,216 bytes omitted and spilled to a file), which is why the band is recorded as eleven displayed
   chunks rather than one; the omitted bytes were re-read inside those chunks.
   **sixth slice (L3480-4219): L4171-4219** — 49 lines; the read stopped at L4170 and the next slice
   starts at L4220, so this elision splits: **L4196-4219** was displayed by the reader's own fill read
   at L4196-4221, while **L4171-4195 (25 lines)** was displayed by no read call in the reader's
   session — carried as a residual against that session's evidence and then displayed by the **Stage
   C2 repair round's read of L4166-4225**.
   **seventh slice (L4220-4941): L4845-4895** — 51 lines; the read stopped at L4844, and these 51
   lines were displayed by the **Stage C2 repair round's read of L4840-4899** — *not* by the reader's
   later call at L4896-4941, which begins after the elision and displays L4896-4941 only; the earlier
   attribution of this elision to that call was wrong and is corrected here.
   **The honest total, by covering read.** The reader's own session displayed L1-785, L720-1419,
   1420-2079, 2080-2739, 2740-3057, 3480-4170 and 4220-4844, plus L4196-4221 and L4896-4941 in its
   two fill reads. The Stage C2 round displayed L780-804, L4166-4225 and L4840-4899. The Stage C3
   round (this one) displayed L3058-3479. **Every one of the page's 4,941 lines is displayed by one of
   those named reads**: the seven slices cover L1-4941, and each of the four capped bands is supplied
   by the read named for it — L786-800 by the reader's own L720-1419 call, **L3058-3479 by this
   round's read**, L4171-4195 by the Stage C2 round's L4166-4225 read (with L4196-4219 from the
   reader's own L4196-4221 fill read), and L4845-4895 by the Stage C2 round's L4840-4899 read. The
   coverage therefore rests on the reader's slices, the Stage C2 round's three reads and this round's
   L3058-3479 read, in that order, and this record says which read covered which range rather than
   merging them into one claim. The page's line count at this revision, 4,941, is
   `(Get-Content <page> -Encoding UTF8).Count` — the plan's declared convention, and the same
   convention that gives 5,118 / 4,879 / 5,939 for P1 / P3 / P7.
   **One carried inconsistency, disclosed rather than hidden, and now historical.** That disclosure
   described the C2/C3-era state of the ledger's appended keeper section, which then carried the old
   coverage sentence — the seven slices said to overlap at their joins and the three capped outputs
   said to be re-read inside the following slice, concluding that no line is unread — and the older
   **two**-item declared-deviation list. The Stage C4 round corrected that section to the record's
   coverage wording: it names all **four** elisions by exact range, each with the read that displayed
   it, and carries the **three**-item deviation list, at L4826-4911 of this head. The section is a
   dated recording and is bound to no acceptance either way: row **K-076** binds the page's blob at
   `0237f611f718`, where no such section exists. This record states the correction as history rather
   than as head state, so that no reader carries away a sentence this head has already replaced, and
   it is named here so no reader takes that superseded sentence for the accounting the row rests on,
   which is the one in this item.

**The six acceptance bullets, addressed for the accepted page.**

| Bullet | P4 `docs/roadmaps/aegis-documentation-readability-backlog.md` |
| --- | --- |
| Purpose and audience up front | **partial — deviation declared.** L1-3 "Start here — current reading" states what the page is and, at L5-17, what the current reading is; L1-17 names **no intended audience** — the rule's second clause ("and who should read it", ledger L2843) is not met anywhere in the page's opening, and the nearest statement of readership (the **Purpose and normal use** restatement heading at L2773, the `## Purpose and scope` section at L2803 — its reader statement at L2805-2809 — through L2835) is not an opening and addresses the reader generically. The record states that as a partial rather than as an unqualified `yes`; L19-31 states in its first sentence that "**The index is now the count**", names the instrument, and says the ledger "publishes no count of its own and cites the index" (D84), before any dated history begins. The dated rounds that follow are labelled as dated history, oldest first, and say no dated snapshot is rewritten (L9-10). |
| Abbreviations and coded identifiers defined at first use | **partial — deviation declared.** The term block at L156-168 defines pull request (PR), commit SHA, the acceptance index, `check_index.py`, "a bound", the ledger keeper and AEGIS-APR-101, and it is the definition the page's own rule turns on. The rule says *at first use*, and the page's **first `PR` token is at L14** ("A later merge, PR #577, adds one further tracked page"), **142 lines before the definition at L156** — the one place the page breaks its own rule, and the record now states it instead of reading the term block as if it preceded every use. The later 2026-10-12 sections keep the discipline (`D84`, `D98`, `K-074/K-075`, "CARRY-WITH-DEVIATION" are each glossed where they first appear in the section that uses them), and coded identifiers are resolved to their own records rather than left bare: AEGIS-APR-101/113-118 to the approval register, D73/D83/D84 to `step-0-reconciliation-v4.md#5-recorded-decisions`. |
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

**Source rows.** The row's `Quote` string appears in section 8 byte-for-byte and names the full
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
   page's bytes at `0237f611f718ed833935e72a0d98dd42362388a0` were read whole, L1-4941, including the 512-line excluded range (the coverage is the reader's seven slices plus the Stage C2 round's three reads plus this Stage C3 round's L3058-3479 read, each named in section 4.1 item 4), and the
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
---
## Footer

sha256: 260321d50e8badc55b0ec93f4cbbfb304a9cde9e1269889e24971626a23cff3a

This digest covers every byte of this file strictly above the last `## Footer` heading — the whole
batch record through the closing `---` rule line and its terminating newline, encoded UTF-8 with LF line
endings. It does not cover this footer. Any edit above the rule voids the digest and requires a fresh
validation.
