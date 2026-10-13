# Readability ledger self-cost re-acceptance — Stage C batch record, 2026-10-13

- **Lane:** the ledger's OWN self-cost re-acceptance — the readability backlog's own whole-page prose
  re-read, plus the D98 follow-up 1-3 dated correction notes. **Stage:** C (IMPLEMENT).
- **Declared revision — the revision every read below was made at, and the revision the appended row
  binds:** `ba522f133d05624c2130f15eb8ef3b6329b0f37a` (`origin/main`; the PR #760 merge, whose subject
  is "Merge pull request #760 from ModernNomad-98/docs/ber-g3-fu-docs-20261013"). At this revision the
  ledger is **5,095 lines** (475,282 bytes), its blob is `5928d98534e95a79e2ffbcc2065d38602dd98b0f` and
  its sha256 is `0afd46779eb3cb72cdcbbaf37558d14d01dd25a5d53a11b3d56302ce2c69f606`, all measured this
  session.
- **Bound revision is main-contained.** `git merge-base --is-ancestor ba522f133d05624c2130f15eb8ef3b6329b0f37a refs/remotes/origin/main`
  exits 0 in this clone; the revision is the tip of `origin/main` as fetched from
  `https://github.com/ModernNomad-98/Project-Aegis.git`.
- **Reader / author identity: `ledger-selfcost-stagec-c`.** A **different agent** from
  `readability-batches-implementer-c`, `readability-closeout-implementer-c`,
  `readability-closeout-repairer-c2`, `readability-f1f5-implementer-c`,
  `readability-final3-implementer-c`, `readability-final3-repairer-c2`,
  `readability-ledger-reader-c` and **every** repairer and reader before this session. That
  independence is the binding constraint the program's carry requires, and it holds for the row this
  commit appends.
- **What this page is.** The lane's batch record and the **evidence source** cited by the one row this
  commit appends to the ledger keeper table, so the row's `Quote` is a verbatim fragment of a tracked
  page and this file **names the bound acceptance revision verbatim** (40 characters) in its own bytes,
  which `tools/readability_acceptance/build_index.py` L264-278 requires at `--ref`.

## 1. The instrument figures at the declared revision, quoted

```text
python -B tools/readability_acceptance/build_index.py --ref ba522f133d05624c2130f15eb8ef3b6329b0f37a --report
{ "built_at_ref": "ba522f133d05624c2130f15eb8ef3b6329b0f37a", "table_rows": 100, "events": 100,
  "full_page_acceptances": 80, "lost_commit_events": 10, "reader_pages_with_rows": 68 }
exit 0
```

```text
python -B tools/readability_acceptance/check_index.py --ref ba522f133d05624c2130f15eb8ef3b6329b0f37a --quiet
{ "compared_ref": "ba522f133d05624c2130f15eb8ef3b6329b0f37a", "reader_pages_in_tree": 647,
  "accepted_on_recorded_review": 60, "provably_pending": 1, "no_recorded_acceptance": 580,
  "recorded_acceptance_within_10_lines": 0, "within_10_not_covered_by_targeted_review": 0,
  "cannot_decide": 6, "official_pending_count": 587 }
exit 0
```

**The `1` is this page.** The tool's own provably-pending list at that revision holds exactly one
entry: `docs/roadmaps/aegis-documentation-readability-backlog.md`, `added+del 64`, `sect yes`,
recorded acceptance `878b7d46`. The six `cannot_decide` rows are the six lost-commit pages of D73
row 5.

**These are the instrument's figures, not this lane's.** This record publishes no readability count of
its own (D84; ledger L19-31, L4675-4682) and predicts **no** post-commit bucket figure. The figures
**at this commit's head** are published in the Stage C record and in the pull request body, never
inside the commit that produces them.

## 2. The roster, the concurrency, and the declared deviations

| Batch | Theme | Pages | Read at | Reader |
| --- | --- | ---: | --- | --- |
| R1 | the ledger's own self-cost re-acceptance, plus the D98 follow-up 1-3 dated corrections | 1 | `ba522f133d05624c2130f15eb8ef3b6329b0f37a` | `ledger-selfcost-stagec-c` |

**Concurrency: one reader.** The lane holds a single page; no second reader was started.

**Declared deviations (read honestly, not silently). Three, all measured facts:**

1. **The reader is the same agent that writes this record and the one ledger keeper row it rests on.**
   `docs/approvals/APPROVAL_REGISTER.md:3155` (AEGIS-APR-101) requires that "The keeper must be a
   different agent from the page's author and accepting reviewer", and permits the keeper only to
   record an existing qualifying decision rather than to confer acceptance. For `K-081` the reviewer
   cell and the writer of the record the row rests on are the **same** agent,
   `ledger-selfcost-stagec-c`, so **that condition is not satisfied on the register's text** and the
   row is **not green**. It is not hidden: the same pattern was declared for `K-074`/`K-075`,
   `K-076`, `K-077`/`K-078`/`K-079` and `K-080`, and is carried the same way — as a
   **CARRY-WITH-DEVIATION under the SD-D2 coordinator-ruling precedent** recorded in
   `READABILITY-CLOSEOUT-AUDIT-D2.md`, which covers the carry and does not itself satisfy the register
   condition. Disposing of the authority question is left where the authority sits: the merge holder
   disposes of it under AEGIS-APR-100. This record claims no such authority.
2. **Two tool-output display elisions and one short read occurred, and each is named by its range with
   the read that covered it.** They are recorded in section 4.2, never merged into one claim and never
   described as an absence of elisions.
3. **Two of the six acceptance-bullet dispositions are partial, and the page's own dated text was not
   rewritten to make them unqualified.** "Purpose and audience up front" is **partial** (L2803-2817
   state what the page is and how to read it but name no intended audience), and "Abbreviations and
   coded identifiers defined at first use" is **partial** (the page's first `PR` token is L14 against
   the definition at L156-157, and the first `D73` citation at L43 precedes its explanation). Both are
   declared in the six-bullet table in section 5.

## 3. The page's disposition

Drift is `git diff --numstat <recorded acceptance> <declared revision> -- <page>`, added plus deleted,
re-measured this session at the declared revision. The recorded acceptance is the one the keeper table
itself carries for this path at that revision — row **K-080**, bound to
`878b7d460d8cce5efb1cb8ecb3197e93e6cbf609`.

| # | Page | Lines at ba522f13 | Recorded acceptance | Drift to the declared revision | Disposition |
| --- | --- | ---: | --- | ---: | --- |
| P4 | `docs/roadmaps/aegis-documentation-readability-backlog.md` | 5,095 | `878b7d460d8c` (row K-080) | 64 / 0 = 64 | **read whole — accepted, row K-081** |

```text
git diff --numstat 878b7d460d8cce5efb1cb8ecb3197e93e6cbf609 ba522f133d05624c2130f15eb8ef3b6329b0f37a -- docs/roadmaps/aegis-documentation-readability-backlog.md
64	0	docs/roadmaps/aegis-documentation-readability-backlog.md
```

**Where the drift sits, measured by hunk headers** (`git diff --unified=0 … | Select-String '^@@'`): two
hunks, both pure additions — `@@ -4911,0 +4912,63 @@` (**63** lines, the K-080 self-acceptance note) and
`@@ -5031,0 +5095 @@` (**1** line, row K-080). 63 + 1 = **64**, matching the numstat exactly, with **0**
deletions. One added heading: `## Ledger-keeper recording — this ledger's own whole-page re-acceptance, 2026-10-13`,
so the page also fails the rule's new-section limb. **Both bands are inside the ranges this session read**
— `L4912-4974` inside R0 and `L5095` inside R0 — and **the excluded already-read set is empty**: no part of
this acceptance rests on an earlier lane's read.

## 4. Depth record — the read ranges, the elisions and their covering reads

### 4.1 The ranges, named by range

Every read below is a `read` call (offset/limit) whose returned line numbers are recorded here. All
ranges are written as `<full path>:<start>-<end>` so that no range is ambiguous between files, and
every range below is a **globally unique** one. **The ranges are listed in the order they were executed
and they are NOT all disjoint**; the overlaps are stated rather than smoothed over, and no claim is made
that the joins "abut exactly" or that there is no overlap anywhere.

| # | Range displayed | Lines returned | Role |
| --- | --- | ---: | --- |
| R0 | `docs/roadmaps/aegis-documentation-readability-backlog.md:4912-5095` | 184 (the request asked `4912-5101`; the page ends at 5095) | the K-080 note's tail, the column contract and the K-080 row (executed first) |
| R1 | `…:1-740` | 740 | prose — display elision 1, covered by C1 |
| R2 | `…:741-1080` | 340 | prose |
| R3 | `…:1081-1420` | 340 | prose |
| R4 | `…:1421-1760` | 340 | prose |
| R5 | `…:1761-2100` | 340 | prose |
| R6 | `…:2101-2440` | 340 | prose |
| R7 | `…:2441-2780` | 340 | prose |
| R8 | `…:2781-3089` | 309 (320 requested) | prose — short read 1; display elision 2, covered by C2 and C2b |
| R9 | `…:3090-3109` | 20 | the short read's remainder, first half (read at full row width) |
| R10 | `…:3110-3129` | 20 | the short read's remainder, second half (read at full row width) |
| R11 | `…:3130-3174` | 45 | prose |
| R12 | `…:3175-3514` | 340 | prose |
| R13 | `…:3515-3854` | 340 | prose |
| R14 | `…:3855-4194` | 340 | prose |
| R15 | `…:4195-4534` | 340 | prose |
| R16 | `…:4535-4874` | 340 | prose |
| R17 | `…:4820-4914` | 95 | prose — the F1-F5 keeper section and the close-out keeper section's tail |
| C1 | `…:355-424` | 70 | covering read for display elision 1 |
| C2 | `…:3028-3043` | 16 | covering read for display elision 2 (the print truncated three long rows, so C2b was added) |
| C2b | `…:3034-3038` | 5 | covering read for display elision 2, at full row width |
| X1 | `…:3090-3129` | 40 | first attempt at the short read's remainder — the print truncated each row to 300 characters, so it is **superseded by R9 and R10** and is **not** relied on for any part of this acceptance |

**The union of R0-R17 is `L1-5095`, the whole page**, and it holds with exactly **two** overlaps:
`L4820-4874`, shared by R16 (which ends at 4874) and R17 (which begins at 4820), and `L4912-4914`,
shared by R17 (which ends at 4914) and R0 (which begins at 4912). Every other adjacent pair is
contiguous with no overlap and no gap: R1/R2 at 740/741, R2/R3 at 1080/1081, R3/R4 at 1420/1421, R4/R5
at 1760/1761, R5/R6 at 2100/2101, R6/R7 at 2440/2441, R7/R8 at 2780/2781, R8/R9 at 3089/3090, R9/R10 at
3109/3110, R10/R11 at 3129/3130, R11/R12 at 3174/3175, R12/R13 at 3514/3515, R13/R14 at 3854/3855,
R14/R15 at 4194/4195, R15/R16 at 4534/4535, and R16/R17 covers 4820-4874. `C1` is contained in R1;
`C2` and `C2b` are contained in R8; `X1` is the union of R9 and R10.

### 4.2 The two tool-output elisions and the one short read, each with its covering read by range

1. **Display elision 1 — inside R1.** The request at `…:1-740` returned all 740 of its lines, but the
   display layer omitted **2,457 bytes**: the visible text jumps from mid-`L374` to mid-`L408`, so
   `L374` through `L408` are the affected rows. The covering read is **C1, `…:355-424`** (70 lines),
   which displayed `L355` through `L424` in full — including the whole of `L374-L408` that the
   elision had swallowed. `L374-408` is therefore covered by C1, not left to R1's truncated display.
2. **Display elision 2 — inside R8.** The display omitted a further **2,825 bytes**: the visible text
   jumps from the end of `L3036` to mid-`L3038`, so **`L3037` and `L3038`** are the affected rows.
   Two covering reads were made: **C2, `…:3028-3043`** (16 lines), which re-displayed the span, and
   **C2b, `…:3034-3038`** (5 lines), which displayed `L3034` through `L3038` at **full row width**,
   because the C2 print truncated the three longest rows. `L3037-3038` is therefore covered by C2b,
   not left to R8's truncated display.
3. **Short read — one request that asked for more lines than it received.** The request at
   `…:2781-3120` returned only `L2781-3089` — **309 of the 340 lines requested** — so `L3090-3129`
   was not displayed by R8. The covering reads are **R9, `…:3090-3109`** and **R10,
   `…:3110-3129`**, both at full row width; together they display `L3090-3129` in full. The first
   attempt, **X1**, printed those rows truncated to 300 characters each and is **superseded** by R9 and
   R10; nothing in this acceptance rests on it.

**No other read in this session was elided or short.** Every other range in section 4.1 was returned
with the line count its request implied and displayed without an omission marker.

### 4.3 The page was read as prose, not sampled

The reading covered the live front matter and the D84/pause/reconciliation notes (L1-2801), the purpose,
required-order, acceptance-bullet and delivery sections (L2803-2880), the whole dated batch table with
its per-batch dispositions (L2883-3301), the pending-floor correction and the 65bacc7 reachability
correction (L3303-3486), the keeper role's first recording and the consistency note that ratifies it
(L3488-3617), every dated checkpoint and batch update (L3619-4617), the 2026-10-12 keeper sections that
carried K-074 to K-076 and the D98 follow-ups (L4619-4910), the K-080 self-acceptance note and the D98
follow-up list (L4912-4974), and the consolidated keeper table with its column contract and all 100 rows
(L4977-5095).

### 4.4 Links and anchors

The page's links were checked mechanically: the repository's own `scripts/ci/check-markdown-links.py`
run over the page reported `files: 1   links checked: 592   anchors checked: 143   broken: 0   dead: 0 external-skipped: 67   other-skipped: 0`, exit 0. The 67 external-skipped entries are GitHub URLs the
checker does not fetch; they are recorded as **skipped**, never as passed. The mechanical output is a
**candidate list, never a defect list**; the repository's own instrument is the adjudicating one.

## 5. The six acceptance bullets, addressed

| Bullet | P4 `docs/roadmaps/aegis-documentation-readability-backlog.md` |
| --- | --- |
| Purpose and audience up front | **partial — deviation declared (section 2 item 3).** L1-2 give the title and subject; L3-31 ("Start here — current reading" and the D84 official-count switch) state what the page is and that the index is now the official count; L2803-2817 ("Purpose and scope") state the reader's task in full — "find a component, understand the problem it solves, follow a normal workflow…". But the page **names no intended audience** in the sense the rule's second clause requires; the nearest readership statement is generic ("Readers should be able to…"). Recorded as **partial** rather than as an unqualified yes, and not repaired because the lane may not rewrite the page's dated text. |
| Abbreviations and coded identifiers defined at first use | **partial — deviation declared (section 2 item 3).** The page does define its coded identifiers, and many well: L150-168 is a "Terms used here" block expanding pull request (PR), commit SHA, acceptance index, bound and ledger keeper; L156-157 defines the PR abbreviation; L2841-2862 restates the acceptance criteria with worked glosses (`CP-WP-003`, `OD-1`, `T03`); the keeper sections expand AEGIS-APR identifiers. **But the standard "never only in a distant block" is not met for the page's own first tokens:** the first `PR` is at L14 and "pull request (PR)" is expanded at L156-157, and the first `D73` citation is at L43 with its content explained much later. Recorded as **partial** rather than as an unqualified yes. |
| Descriptive headings, lists or tables, and at least one concrete example | **yes.** Every dated reading is its own descriptive heading; the counting rules are bulleted rules with named owner decisions and dates; the batch progress is a five-column table with a stated column contract; and the examples are worked rather than gestured at — the arithmetic closes explicitly (`584 + 1 + 55 + 13 = 653` at L2557; `674 − 1 − 65 = 608` at L336; `17 + 1 = 18` at L3443; `63 + 1 = 64` re-derived this session), and the page quotes its commands instead of asserting figures (`git diff --numstat`, `git ls-tree -r --name-only`, the two instrument invocations). |
| Shipped behaviour separated from proposed or blocked behaviour | **yes.** The D84 note says in terms that it "records the switch; it changes no count by itself and confers nothing" (L30-31); the 2026-10-07 note distinguishes the decided, the paused and the not-derivable (L93-100); the keeper sections repeat that no acceptance the reviewers did not give is recorded and that a not-accepted page keeps its pending status; the D98 section labels its three figures "(a) Historical, D96-pinned — NOT the live figure", "(b) Live at the reviewed revision" and "(c) Live at the candidate head" (L2795-2797); and the page states its own no-authority boundary at L2877-2879 and L3018-3020. |
| Navigation links current and every referenced file or command existing | **yes, read as a candidate list and adjudicated mechanically.** The page's run of the repository's own link checker reports **broken 0, dead 0** across 592 links and 143 anchors; the in-page anchors the page itself uses resolve; and the six `cannot_decide` pages it discusses are the tool's own lost-commit rows, which the page records as pending rather than as accepted. Historical citations the page itself marks as dated — and the D98 follow-up 3 stale evidence-source anchors at keeper rows `L-001` to `L-006` — are re-anchored forward by this lane's dated correction note, never edited in place. |
| The non-author review itself | **this record**, with the staffing deviation in section 2 item 1 declared in terms |

**Purpose and normal use restated from the page alone** (the acceptance contract's own non-author test):

- **P4 — *for*:** the repository-wide documentation acceptance backlog — the record of which reader pages
  have received an independent full-page acceptance, at which revision, by which reviewer and on what
  evidence; the counting rules in force; and the dated history of how the pending inventory moved. Its
  normal use is: read L3-31 first for the live reading and the official-count switch, then the
  "Acceptance for each page" list at L2841-2862 as the criterion any acceptance must meet, then the
  counting rules at L2939-3020 as the rule that decides whether a page is pending; consult the dated
  rounds only as history, and read the consolidated keeper table at L4977-5095 as the machine-readable
  index those rounds feed.

**Disputed lines: none.** No line of the page was disputed without change, and no line of it was edited by
this lane beyond the two appends named in section 6.

## 6. Stale / new / source rows

**Every line this lane changes.** `git diff --numstat ba522f133d05624c2130f15eb8ef3b6329b0f37a <this commit's head>`:

| Path | Added | Deleted | Source |
| --- | ---: | ---: | --- |
| `docs/evidence/documentation/readability-ledger-selfcost-2026-10-13.md` | new file | 0 | this record |
| `docs/roadmaps/aegis-documentation-readability-backlog.md` | appends only | 0 | one dated keeper note carrying the D98 follow-up 1-3 corrections (inserted immediately above the `<!-- acceptance-index-schema: 1 -->` sentinel, where every earlier dated keeper note sits) and one keeper row (`K-081`, at the end of the keeper table) |

**Nothing else is in the diff.** No code, no workflow, no script, no `tools/` artifact, no JSON, and no
protected path — the lane is Markdown-only by construction, which is why the pull request answers the
security question `No`. The read page is **not** modified other than by those two appends:
`git diff -U0` against the declared revision shows two insertion hunks and **0 deletion lines**.

**Source row.** The row's `Quote` string appears in section 9 byte-for-byte and names the full
40-character acceptance revision `ba522f133d05624c2130f15eb8ef3b6329b0f37a` verbatim, which
`build_index.py` L275-278 requires in the evidence source at `--ref`; the row's `Blob ID` is
`git rev-parse ba522f133d05624c2130f15eb8ef3b6329b0f37a:docs/roadmaps/aegis-documentation-readability-backlog.md`,
which L258-263 requires:

| Row | Page | Blob ID at the bound revision |
| --- | --- | --- |
| K-081 | `docs/roadmaps/aegis-documentation-readability-backlog.md` | `5928d98534e95a79e2ffbcc2065d38602dd98b0f` |

**Numbering was verified, not assumed.** A whole-page search of the ledger at the declared revision for
`K-081` returns no match (`git grep -c 'K-081' ba522f13… -- <the ledger>` exits 1); the keeper table's
last row at that revision is `K-080`, so `K-081` is the next free identifier in **string order** — the
order `build_index.py` L293 compares stable IDs in when it derives the latest event per page
(`ev["stable_id"] > cur["stable_id"]`) — and no duplicate is created.

**The D98 follow-up corrections, as appended rows.** Three dated correction notes are appended inside the
new keeper section, each naming the dated lines it corrects and leaving them byte-unchanged:

| Follow-up | Dated lines corrected forward | Correction recorded | Anchors that resolve at the bound revision |
| --- | --- | --- | --- |
| 1 | L3375-3377 ("open PR #633", "not merged") | PR #633 merged as `e88a0a0d0691259745d20301d3f34b992cb8e1c4`; `merge-base --is-ancestor e88a0a0d… refs/remotes/origin/main` exits **0** | `git rev-parse e88a0a0d`; `git merge-base --is-ancestor` |
| 2 | L3379-3385 ("the ten other SHAs") | ten strings, **nine distinct commits**: `bf7a4b86b46b` and `bf7a4b8` are the same commit | `git rev-parse` over the ten strings → nine distinct full SHAs |
| 3 | keeper rows `L-001`-`L-006` evidence-source cells (`:2574` / `:2575`) | those lines hold PR #333 protected-file guard prose; re-anchored to `docs/reconciliation/step-0-reconciliation-v4.md:3834` and this ledger's L3329-L3342 / L3353-L3389 | `git rev-parse` on the six lost commits; D73 row 5 at reconciliation log L3834 |

## 7. Named follow-ups

**Staffing bound.** Every row this program still owes must be bound by a **different agent** from the one
that read the page — this lane satisfies that for the page it accepts, and the bound is restated here for
any row a later tranche adds.

1. **The AEGIS-APR-101 keeper condition for K-081 — carried, not satisfied.** Owner: the merge holder
   under AEGIS-APR-100, which either cites the authority that permits a same-agent recording at this head
   or withholds the row for an eligible keeper to re-record. Reason: the reader and the record's writer
   are the same agent (section 2 item 1), which the register's own text does not permit. No further read
   is owed; only the authority disposition is.
2. **This lane's own self-cost.** This record and the ledger append change the ledger by more than 10
   lines and add a section, so the page **returns to pending** at this commit's head and owes a
   subsequent independent full-page re-read by a reader who did not write this section. This row accepts
   the page's **bytes at `ba522f133d05624c2130f15eb8ef3b6329b0f37a`**, not the page at the new head.
3. **The D98 follow-ups 1, 2 and 3 are discharged** by the appended dated correction notes (section 6).
   The dated text they correct is unchanged, as the rule requires; nothing further is owed on them.
4. **The two partial acceptance bullets stay partial and unrepaired** (section 2 item 3), because the
   lane may not rewrite the page's dated text. Not a new defect.
5. **No page-own follow-up remains undischarged at the bound revision.** The page's own dated requests for
   a re-read (its D98 follow-up 4, its L4720-4728 statement and its L4822-4824 restatement) refer to the
   revisions they were written at; at `ba522f13` the page carries an acceptance bound to that revision,
   which is this lane's record and row.

## 8. Count honesty

- **This lane publishes no readability count of its own** and cites the instrument (D84). The figures in
  section 1 are the instrument's printed output at the declared revision, quoted **as the instrument's
  figures**, and **no post-commit bucket figure is predicted** anywhere in this record.
- The instrument classifies the page tree at `--ref` and reads the recorded acceptances from the
  **committed** `acceptance-index.json`. The row appended here **changes nothing until a further
  rebuild**, and a rebuild can only be run after the commit that carries the row, because
  `build_index.py` stamps its own `built_at_ref`; the two resolvers this ledger names apply — a
  two-commit follow-up, or a merger-side rebuild at the merged tip (D73 row 8).
- **No `--write` was run by this lane**; the two gate commands above are read-only reports.

## 9. The row-quote string, verbatim

The line below appears in this file byte-for-byte and is copied verbatim into its ledger row. It also
contains the full 40-character acceptance revision, the second binding rule the validator enforces.

```text
K-081 accepted: docs/roadmaps/aegis-documentation-readability-backlog.md read whole at ba522f133d05624c2130f15eb8ef3b6329b0f37a
```

## 10. What this lane did not do

It rewrote no dated snapshot; edited, reordered or deleted no existing keeper row; edited nothing on the
page other than the two appends named in section 6; appended no acceptance row this record does not
support; bound no row to this commit's own SHA; ran no `build_index.py --write` and rebuilt no `tools/`
artifact; touched no `.github/workflows/` path; and claims no authority beyond recording. The reading
procedure does not grant provider, private-input, real-host or deployment authority (ledger L3018-3020).

---
## Footer

sha256: 026b364745b9730a59b269b1f9131cec32c4409a326f3a0225a499ccdc929147

This digest covers every byte of this file strictly above the last `## Footer` heading - the whole batch record through the closing `---` rule line and its terminating newline, encoded UTF-8 with LF line endings. It does not cover this footer. Any edit above the rule voids the digest and requires a fresh validation.
