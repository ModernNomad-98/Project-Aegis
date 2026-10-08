# OPT1-PR1 — PLAN rev3 (a delta against rev2)

> **REVISION MARKER: rev3.** This file is a delta. The effective plan is `PLAN-rev2.md` (sha256 `40691fe15546d9458ea8c6728e7c31efb88701a88c0217fd3bbbcb333647bc58`, unmodified) with the changes below applied. Where the two disagree, rev3 governs. Every section of rev2 not named here stands.
>
> **Why rev3 exists.** Two reviews of PR #678 at head `18109931a63f4542b976ea3c78918fe77dcb5124` found defects in conditions the plan recorded:
>
> - the Codex automated review **5449260025** (22:36:47Z) raised four threads;
> - the Stage D audit `IMPL-AUDIT-1.md` (sha256 `827915bb…62b1ae`; `SD-D: ACCEPT`, comment 6048419441) independently raised C-1 to C-4 and N-1 to N-4.
>
> rev3 also takes in one coordinator-directed owner item: the "Parallel repair PRs" option of `OWNER-EVIDENCE.md` §5. That file now has sha256 `08b0ec6dd7dabdb6a70c0f5dd72d308891f2cbf0ec8d73a10949ef45bdf73eb9`; rev2 cited `622fc6c3…`, which reproduces as its first 69 lines.
>
> **Out of scope, by the coordinator's direction:** every §6 item and every other §5 item.

- **Planner:** the same PLAN-stage subagent as rev1 and rev2. It made no repository edit, commit, push, PR, comment or thread resolution. It read refs only: `git fetch origin` updated remote-tracking refs, and `git status --short | wc -l` printed 0 before and after.
- **rev3 start:** 2026-10-07T22:47:16Z (`date -u`).
- **Skills used:**
  - `scoped-approval-register`: AEGIS-APR-114 and -115 are tightened without invented negatives, and §5 is added verbatim.
  - `source-of-truth-reconciler`: each finding is weighed against the head text, AEGIS-APR-101, the ledger and VERIFY.
  - `acceptance-criteria-reviewer` (partial fit): the new and changed criteria are checked for testability.

  No MANUAL-ONLY skill was used.

## 1. Each finding, checked against the head text

| Finding | What I checked at `18109931` | Verdict |
| --- | --- | --- |
| **Codex r4212737371** (P1) and **IMPL C-4**: pin AEGIS-APR-115's output paths | Register `:4814-4817`: "regenerates the files the repaired tool's build writes, using the tool as it stands on the default branch. Today `build_index.py --write` writes [two files]". The set is defined by a reference that changes when the tool does. The selected option says "Nothing else is covered." (`:4802`). The register's preamble says "An action is covered only by an effectively ACTIVE human grant whose scope includes it." | **ADOPT.** Name the two files. Make no claim that a future output is covered: until the owner decides, it is not. That follows the preamble's citation rule, so it is not an invented negative. This must be fixed now, because a register entry is immutable once merged (IMPL C-4). |
| **Codex r4212737350** (P1) and **IMPL C-1** (MAJOR): the keeper-row schema drops the evidence | D73 row 2 (`step-0…:3797`) pins only "page, full 40-character acceptance commit, blob ID". The existing keeper table at ledger head `:3286` (base `:3241`) is `Page \| Acceptance revision \| Reviewer \| Evidence source \| Date`. VERIFY §5 kept "reviewer, evidence link, date". AEGIS-APR-101 (`:3148`) binds a recording "to the exact reviewed revision and its posted evidence". Row 2 also says `stated-acceptances.json` stops being an input, so no other channel carries the evidence. | **ADOPT, with one qualification.** Keep the reviewer, evidence and date columns, and require the build to reject (not count) a row whose evidence pointer is missing or malformed. The build runs offline and cannot read GitHub, so it cannot confirm that a pointer leads to a qualifying review; that check stays with the recording PR's independent review. rev3 says so rather than claiming machine validation. |
| **Codex r4212737359** (P1) and **IMPL C-2**: no way to represent a targeted review | Row 11 (`:3806`) says "the table needs a way to record targeted reviews". Row 2's pinned schema has no field for one, and row 4 says "targeted-only … text never yields a row". Read alone, row 4 would forbid such rows everywhere, although it belongs to the backfill. | **ADOPT, scoped as the coordinator directs.** Add an event kind to row 2, plus, for a targeted review, the retained full-page acceptance revision beside the reviewed revision. Narrow row 4's exclusion to *full-page* rows the **backfill from prose** creates. Leave the authority to record targeted-review rows not decided (it belongs to `OWNER-EVIDENCE.md` §6, a later PR); the schema only provides for such rows, so it forecloses nothing. |
| **Codex r4212737366** (P2) and **IMPL C-3**: discovery is not preservation | Row 8 (`:3803`) requires fetching `refs/remotes/**` and `refs/pull/*/head`. AEGIS-APR-113 (`:4657`) lists "acceptance commits are preserved". Fetching finds an object only while a ref holds it. VERIFY V11 shows six acceptance commits already lost. **Reconciling with the blob ID:** D73 row 5 and AEGIS-APR-113 item 3 make a page whose commit "no longer exists anywhere" pending until it is re-reviewed, and that rule does not depend on whether the page's blob survives. So the blob column cannot by itself keep a page counted, and preservation must come from a durable reference. D73 never says which rows meet "acceptance commits are preserved" (C-3). | **ADOPT.** Row 8 adds an Audit condition: before the switch, every recorded acceptance commit is held by a durable mechanism that the repaired tool reads. The tool-repair plan names the mechanism, and a new ref, tag or merge-method convention needs the owner's decision first. The blob ID is reframed as a content check and a change measure, not as preservation. Rows 2, 5 and 8 together are stated to deliver the condition. |
| **IMPL N-1**: case changed inside a quotation | The ledger note quotes "still separately unresolved"; the source, at head `:3395`, reads "**Still separately unresolved, and still undecided.**" | **ADOPT** (cheap): quote "Still separately unresolved". |
| **IMPL N-2**: the elision marks between recommendation blockquotes are not shown | The `OWNER-EVIDENCE.md` §1(a) transcription has "..." before "1. No CI gate" and before "Rebuild the index". Blockquotes 2 and 3 do not show them. | **ADOPT** (cheap): prefix those two blockquotes with "… ". |
| **IMPL N-3**: the label "coordinator default" is not in the legend | Row 8's source label | **ADOPT**: the label becomes Audit (row 8 is rewritten anyway). |
| **IMPL N-4**: "What it answers" is one sentence of about 12 lines | Ledger note at head `:34-43` | **ADOPT** (cheap): three bullets. This is also needed because the column list in that sentence changes (X3). |
| **Coordinator: §5 "Parallel repair PRs"** | `OWNER-EVIDENCE.md` §5. The question was "Which speed-ups do you want? Pick any."; the chosen options included "Parallel repair PRs", with the option text "Split the repair into small PRs held by separate agents and run in parallel: guards and tests, the table reader, and backfill batches." It was answered before 22:29:29Z. AEGIS-APR-114's expiry at head says "does not say whether one function delivered in more than one pull request is covered". | **ADOPT**: AEGIS-APR-114 covers the tool repair in one PR or several and cites §5 verbatim. It also turns the recorder's reading about the backfill into an owner-supported one, because the option text names "backfill batches". The D73 "Not decided" item 4 is resolved. |
| **Stage E: no link points to the new ledger heading** | `git grep "owner-decision-on-the-count" 18109931 -- '*.md'` → 0 | **Intended, and not a defect.** The note sits directly under "Start here — current reading", where every reader of the ledger starts, and the register, D73 and the forecast link to the authoritative records rather than to the note. **rev2's K4 list was wrong** to name "the new ledger heading" as an anchor that must resolve; rev3 removes it (§4). |

No finding is rejected. The qualifications above (the offline build cannot validate GitHub evidence; the targeted-review authority stays undecided) are stated in the replies (§5).

## 2. Exact text changes (Stage C applies these to the PR's own added lines; nothing on main is touched)

Line references are at head `18109931`. Every change replaces text this PR added, so AC-2 and AC-3 against base `7d1d05e8` stay as specified.

### 2.1 AEGIS-APR-115 (`APPROVAL_REGISTER.md`, Scope allowed, `:4810-4817`). Codex r4212737371 / C-4

**Replace** the whole `Scope allowed` bullet with:

```markdown
- **Scope allowed:** Work and merge authority for routine index-rebuild pull
  requests after the switch, merged on the question's terms (all stages
  passed, all checks green, administrator merge allowed, fix and retry)
  without asking the owner each time. A rebuild pull request regenerates, with
  the tool as it stands on the default branch, these two generated files and
  no other path:
  - `tools/readability_acceptance/acceptance-index.json`
  - `tools/readability_acceptance/acceptance-verdicts-stage-1.json`

  These are the files `build_index.py --write` writes at this recording; a
  rebuild that changes only one of them is covered. Whether a pull request
  that writes any other path is a rebuild pull request is not decided by this
  entry. Until the owner decides, such a pull request is not covered: under
  this register's preamble, "An action is covered only by an effectively
  ACTIVE human grant whose scope includes it."
```

`Scope FORBIDDEN`, Status, Evidence and Expiry stay as at head.

### 2.2 AEGIS-APR-114 (`APPROVAL_REGISTER.md`). Coordinator §5 item

The Scope allowed, Evidence and Expiry bullets change as follows.

**(a)** Replace the sentence "The covered pull requests are the three the question names: the decision record, the tool repair and the switch." with:

```markdown
  The covered pull requests are those the question names: the decision
  record, the tool repair and the switch. The tool repair may be delivered in
  one pull request or several. Asked "Which speed-ups do you want? Pick any."
  (answered before 2026-10-07T22:29:29Z, an upper bound), the owner's
  selections included **"Parallel repair PRs"**, whose option text reads:

  > Split the repair into small PRs held by separate agents and run in parallel: guards and tests, the table reader, and backfill batches.

  Each such pull request merges on the same terms. The owner's other
  selections in that answer are outside this entry.
```

**(b)** Replace the **Recorder's reading** paragraph with:

```markdown
  **The backfill is part of the tool repair.** The "Parallel repair PRs"
  option text names "backfill batches" among the repair's pull requests, and
  option B's text bundles the backfill with the repair ("after a one-time
  reviewed backfill. About 16–32 agent-hours (estimate).").
```

**(c)** In **Evidence**, append: "The speed-up selection was answered before 22:29:29Z."

**(d)** Replace the whole **Expiry / use limit** bullet with:

```markdown
- **Expiry / use limit:** The pull requests the question names, with the tool
  repair delivered in one or several pull requests. The grant is exhausted
  once the decision record, every tool-repair pull request and the switch
  have merged.
```

The "Recording of its consumption" bullet stays.

### 2.3 AEGIS-APR-113 (`APPROVAL_REGISTER.md`, Owner decisions item 1). IMPL N-2 only

Prefix the second and third recommendation blockquotes with `… `:

- `> … 1. No CI gate. The index should be the official count, but it should not become a required CI check that every PR must pass.`
- `> … Rebuild the index in its own small PR when you want a fresh count. Optionally add a separate, non-blocking CI job later.`

**No other APR-113 change.** Its item 1 already names "acceptance commits are preserved" and sends the method to D73. Its "Not decided by this entry" items stay literally true: this entry does not decide them.

### 2.4 D73 (`step-0-reconciliation-v4.md`)

**(a) The Decision paragraph** (`:3749-3753`). Replace "and answered six follow-up questions, recorded verbatim in" with "answered six follow-up questions and, among later speed-up options, chose "Parallel repair PRs"; all are recorded verbatim in". Append a list item after item 7:

```markdown
    8. the tool repair may be split into several pull requests run in
       parallel.
```

**(b) The legend** (consistency item X1). Replace "**Open** means undecided." with "**Open** means not decided by this record."

**(c) Row 2.** Codex r4212737350 and r4212737359; C-1. Replace the row with:

```markdown
    | 2 | The index reads only the keeper's table. The table keeps the information in the existing keeper table's columns (Page, Acceptance revision, Reviewer, Evidence source, Date, in the first ledger-keeper recording) and adds an event kind and a blob ID. Each row records: the page; the event kind, either a full-page acceptance or a targeted review; the recorded revision, the full 40-character commit the review read; the page's blob ID at that revision; for a targeted review, also the retained full-page acceptance revision it builds on; the reviewer; the evidence pointer; and the date. The evidence pointer is a link to the posted review record carrying its numeric ID (the repository's established form is a pull-request comment) or, for a backfilled row, the ledger or evidence-record location and revision whose text the row quotes (row 4). The build rejects, and does not count, a row whose evidence pointer is missing or malformed. The build runs offline, so the recording pull request's independent review checks that the pointer leads to a qualifying review bound to the recorded revision; AEGIS-APR-101 binds each recording "to the exact reviewed revision and its posted evidence". A pull-request comment can still be edited or deleted on GitHub; that residual is recorded, not solved. The index never reads the "Candidates examined and NOT recorded" table, and `../` links resolve relative to the ledger. `stated-acceptances.json` stops being an input. | Owner ("the index reads only that table"); Existing rule (AEGIS-APR-101's evidence binding); Audit (schema and validation) |
```

**(d) Row 4.** Codex r4212737359, scoping the backfill. Replace the row with:

```markdown
    | 4 | Backfill verification. Each backfilled row's quoted text is found verbatim in the cited ledger or evidence record at a stated revision, and that location is the row's evidence pointer. The full commit resolves, and the blob ID equals `git rev-parse <commit>:<path>`. In the backfill from ledger prose, retention, negated, targeted-only and "becomes pending" text never yields a full-page acceptance row. Whether the backfill may transcribe a historical targeted review as a targeted-review row depends on the authority in row 11, which this record does not decide. A row that cannot be verified is not written, so its page counts as pending. An independent reviewer checks every row, and the build rejects a malformed row loudly. | Owner ("one-time reviewed backfill"); Audit (the verifiable quote and all checks) |
```

**(e) Row 8.** Codex r4212737366; C-3; N-3. Replace the row with:

```markdown
    | 8 | Discovery and preservation. Rebuilds run only in a full clone that has fetched `refs/remotes/**` and `refs/pull/*/head`, and the reviewer rebuilds and requires a zero diff. Fetching finds a commit only while some reference still holds it; it does not preserve it. So before the switch, every recorded acceptance commit is held by a durable preservation mechanism that the repaired tool reads, and the tool-repair plan names that mechanism. A new reference namespace, a tag convention or a merge-method rule needs the owner's decision first. The blob ID is a content check, and it lets the build measure a page's change against the default branch when the reviewed commit is not an ancestor of it. It is not preservation: under row 5, a page whose commit is lost counts as pending even when its blob survives. Rows 2, 5 and 8 together are how "acceptance commits are preserved" (AEGIS-APR-113) is met. | Owner (the coordinator's summary: "acceptance commits preserved"); Audit (the mechanism) |
```

**(f) Row 10**, for consistency with 2.1. Append to the condition cell: " If the repaired build writes any path other than the two files AEGIS-APR-115 names, the switch plan raises it with the owner before relying on AEGIS-APR-115." Change the source cell to "Audit; Owner ("Nothing else is covered.")".

**(g) Row 11.** Codex r4212737359. Replace the row with:

```markdown
    | 11 | The targeted-edit rule applies as written: "A small edit keeps acceptance only if an independent reviewer checked it". For the index to see that check, it must be recorded as a targeted-review row (row 2's event kind), carrying the reviewed revision, its blob ID, the retained full-page acceptance revision, the reviewer and the evidence pointer. The 10-line net difference is still measured from the retained full-page acceptance (the ledger rule). The switch states the resulting count before it takes effect. **Open:** the authority for recording targeted-review rows. The schema provides for them, so recording that authority later needs no schema change. Context: the conversion process's (b)2 says a targeted review "never qualifies", while its (b)3 counts "a qualifying ≤10-line retained edit". | Existing rule; Audit (the recording need and schema); Open (authority) |
```

**(h) Consequences, "Easier"**, for consistency with (e). Replace "A blob ID keeps an acceptance verifiable after a squash merge." with "A blob ID lets the build measure a page's change against the default branch after a squash merge."

**(i) "Not decided here"**, the list and the paragraph under it. Replace both with:

```markdown
  - **Not decided here:**
    1. the unmeasurable cases other than lost commits (condition 5);
    2. the authority for recording targeted-review rows (condition 11);
    3. the tool's security classification (condition 14).

    This record does not decide these three. Whether one program function may
    be delivered in more than one pull request is no longer open: AEGIS-APR-114
    records the owner's "Parallel repair PRs" choice for the tool repair.
```

If the coordinator vetoes X1 (§3), keep instead the head's sentence "Items 1 and 3 are listed under "Still open for the owner" …", with "Items 2 and 4" changed to "Item 2" and "(item 2 is flagged for the tool repair)" kept.

### 2.5 Ledger note (`aegis-documentation-readability-backlog.md`, `:34-43` and the self-cost line). N-1, N-4, X3

Replace the "What it answers" paragraph with the block below. It is harvester-safe: it contains no accept-verb, no *keep … acceptance*, no SHA and no table.

```markdown
**What it answers:**

- the "Held for the owner" question in the current-count reconciliation that
  directly follows this note;
- "Both deserve an owner ruling before the convention is relied on again" in
  the [first ledger-keeper recording](#first-ledger-keeper-recording--owner-ratified-role-2026-10-02):
  future records go into one fixed-format table in this ledger, whose columns
  D73 sets as an audit condition; the repair pull request adds the table, and
  this note does not;
- the precedence and counting rules that the
  [keeper consistency note](#consistency-note--the-ledger-keeper-entry-2026-10-02-local--recorded-2026-10-03-utc)
  calls "Still separately unresolved".
```

**X3, the self-cost line.** Recount the note with `git diff --numstat 7d1d05e8 HEAD -- <ledger>` at the new head and update "adds 45 lines" to the measured figure. Do not assume a value.

### 2.6 Open-decisions (`aegis-open-decisions-2026-09-23.md`). Consistency for §5, plus X1

- **Row "Merges of the program's pull requests":** after the label, insert "With the owner's later "Parallel repair PRs" choice, the tool repair may be several pull requests." The link to AEGIS-APR-114 stays.
- **Row "Pages whose recorded acceptance commit no longer exists anywhere"**, under X1: replace "other cases where a page's change cannot be measured stay open (below)." with "other cases where a page's change cannot be measured are not decided by this record."
- **X1:** delete the two rows this PR appended to "Still open for the owner" ("Readability count: changes that cannot be measured …" and "Security classification of the readability acceptance tool …"). They are this PR's own additions, so deleting them changes nothing that is on main.

### 2.7 Forecast (`aegis-backlog-forecast.md`, the new section). X2, consistency with §5

- Replace "It adds an owner-selected program of three pull requests, outside the" with "It adds an owner-selected program — the decision record, the tool repair (one or several pull requests) and the switch — outside the".
- In the table row "Tool repair with the one-time backfill", append " (one or several pull requests)" to the first cell. **No estimate changes.**

## 3. Consistency items

**X1, recommended; the coordinator may veto it in the Stage C brief.** `OWNER-EVIDENCE.md` §6 (before 22:30:07Z) records owner answers to three items this head presents as open:

- two "Still open for the owner" rows, which assert "Each item below needs an owner choice or read";
- D73's legend, "**Open** means undecided".

At merge, those statements would be known to be false. The coordinator has directed that §6 is **not** recorded here, and IMPL O-1 agrees that a later PR owes the forward corrections. X1 brings in nothing from §6. It only stops this PR from adding text that is false at merge:

- it deletes the PR's own two "Still open" rows;
- it changes the legend to "not decided by this record", which is true whatever §6 says.

AEGIS-APR-113's "Not decided by this entry" is already true as worded, so it is left alone. If X1 is vetoed, the later §6 PR must forward-correct those rows (IMPL O-1), and rev3's 2.4(i) fallback applies.

**X2:** the forecast's "three pull requests" (2.7). **X3:** the ledger self-cost count (2.5). Both follow mechanically from the changes above.

## 4. Changes to checks and acceptance criteria

| Item | Change |
| --- | --- |
| **K4** | Remove "the new ledger heading" from the list of anchors that must resolve: no link targets it, by design (§1). The rest of K4 is unchanged; the run must still give `broken: 0 dead: 0` at the new head. |
| **K9 / AC-2 / AC-3** | Re-run at the new head. Expected numstat: 0 deletions everywhere except open-decisions, which stays at exactly 1 deleted line (the `:148` row). Under X1, open-decisions' added count falls by 2. Every change in §2 edits this PR's own added lines, so base lines stay byte-identical. |
| **K10, K11 / AC-10, AC-11** | Re-run at the new head, unchanged in method and expectation: summary 602/436/212/159/224/7; K11 (a) identical, (b) identical after normalisation, (c) 0. The rewritten ledger bullets fall inside the added-line range. |
| **K12 / AC-4** | Unchanged: 115 headings, 1..115. |
| **AC-5** (extended) | Add three items, each `grep -F`-checked on one line: `Parallel repair PRs`; `Split the repair into small PRs held by separate agents and run in parallel: guards and tests, the table reader, and backfill batches.`; `Which speed-ups do you want? Pick any.`. The existing items still hold; for the two recommendation blockquotes, the check is the text after the `… ` prefix. |
| **AC-6** (extended) | AEGIS-APR-115's Scope allowed names exactly the two paths, contains no "Today", and contains the sentence "Until the owner decides, such a pull request is not covered". Check: `grep -c 'Today' <115 block>` = 0, and both `tools/readability_acceptance/…json` paths are present. AEGIS-APR-114's Expiry no longer contains "does not say whether one function". |
| **AC-14** (new) | **D73 schema and preservation.** The check is a read plus a grep over the D73 block.<br>• Row 2 names: page, event kind, recorded revision, blob ID, retained full-page acceptance revision for targeted reviews, reviewer, evidence pointer and date. It states that the build rejects a row without a well-formed pointer, and that the offline build does not verify GitHub content.<br>• Row 4's exclusion reads "never yields a full-page acceptance row" and is scoped to "the backfill from ledger prose".<br>• Row 8 contains "it does not preserve it" and the owner-decision requirement for a new ref, tag or merge-method convention.<br>• Row 11 marks the targeted-review authority **Open**.<br>• No D73 text decides that authority: grep the D73 block for "grant", "may record targeted" and "authorized to record" and read each hit.<br>• No source label outside the legend's four (Owner, Existing rule, Audit, Open) remains: `grep -c 'coordinator default'` = 0. |
| **AC-15** (new) | **Codex triage (`MG3`) at the new head.** Each of the four threads has a reply naming the fix head and the change (§5). Stage E confirms that an automated result for the new head exists, or that Codex is confirmed unavailable, and that any new P0–P2 finding is triaged. The plan does not resolve threads; replying records the triage, which is what `MG3` requires. |

**Chain rule.** rev3 is a plan revision after `SD-D`. It therefore goes to Stage B for re-audit. After that come Stage C (new head), D, E and F at that head, then G. The verdicts bound to `18109931` are void for the new head (exact-head invalidation). The PR body's skills table and bound fields change, so Stage F re-hashes them. The body's `OWNER-EVIDENCE.md` citation should name `08b0ec6d…`, now that §5 is quoted (IMPL O-3).

## 5. Thread replies for the implementer

Post one reply on each Codex thread **after** the fix head is pushed, with `<HEAD>` replaced by the new 40-character head. These are PR comment replies, covered by the standing PR-update grant (AEGIS-APR-003). Do not resolve the threads.

- **r4212737371** (AEGIS-APR-115 output paths):
  > Adopted in `<HEAD>`. AEGIS-APR-115's Scope allowed now names exactly `tools/readability_acceptance/acceptance-index.json` and `tools/readability_acceptance/acceptance-verdicts-stage-1.json` (a rebuild that changes only one of them is covered). It says that whether a pull request writing any other path is a rebuild PR is not decided by the entry, and is not covered until the owner decides, citing the register preamble's coverage rule. D73 condition 10 adds that the switch plan raises any different output set with the owner before relying on AEGIS-APR-115. That matches the selected option's "Nothing else is covered." without adding a restriction the owner did not state.
- **r4212737350** (evidence pointer):
  > Adopted in `<HEAD>`. D73 condition 2 now keeps the existing keeper table's Reviewer, Evidence source and Date information and adds an event kind and the blob ID. The evidence pointer is a link to the posted review record with its numeric ID, or, for backfilled rows, the ledger or evidence-record location and revision whose text the row quotes. The build rejects, and does not count, a row whose pointer is missing or malformed. One qualification: the build runs offline and cannot read GitHub, so checking that the pointer leads to a qualifying review bound to the recorded revision stays with the recording PR's independent review (AEGIS-APR-101's "posted evidence" binding). The entry says so rather than claiming machine validation.
- **r4212737359** (targeted-review representation):
  > Adopted in `<HEAD>`. D73 condition 2 adds an event kind (full-page acceptance or targeted review) and, for targeted-review rows, the retained full-page acceptance revision beside the reviewed revision. Condition 11 describes the targeted-review row and keeps the 10-line baseline at the retained full-page acceptance. Condition 4's exclusion is narrowed to full-page rows created by the backfill from ledger prose, so it no longer reads as forbidding targeted-review rows. The authority to record targeted-review rows is deliberately left open here, because a later register entry records it. The schema provides for those rows so that no schema change is needed then.
- **r4212737366** (durable references):
  > Adopted in `<HEAD>`. D73 condition 8 now separates discovery from preservation. It requires that, before the switch, every recorded acceptance commit is held by a durable preservation mechanism that the repaired tool reads, named by the tool-repair plan, with any new ref, tag or merge-method convention needing the owner's decision first. On reconciling with the blob ID: under condition 5 (the owner's lost-commit rule), a page whose commit no longer exists counts as pending even when its blob survives. So the blob ID is reframed as a content check and a way to measure change against the default branch after a squash, not as preservation. Conditions 2, 5 and 8 are now stated to be how "acceptance commits are preserved" is met.

## 6. ETA for this rework

Agent estimates; unmeasured; low confidence.

| Stage | Estimate |
| --- | --- |
| B re-audit of rev3 | 15–25 min |
| C | 30–50 min |
| D | 20–35 min |
| E | 15–25 min, plus about 2 min CI and the Codex wait |
| F | 25–45 min |
| G | 10–20 min |
| **Total remaining** | about 2–3.3 active hours |

The forecast row "Decision record … 3–5" stays within range and is not edited.

## Timing

- **rev3 start:** 2026-10-07T22:47:16Z (`date -u`). No ETA was announced, because this subagent has no owner channel.
- **rev3 finish:** see the hand-off report, taken with `date -u` after this file's sha256.
