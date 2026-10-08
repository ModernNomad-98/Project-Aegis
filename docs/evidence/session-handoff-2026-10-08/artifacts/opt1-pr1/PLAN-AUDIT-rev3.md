# OPT1-PR1 — PLAN AUDIT rev3 (Stage B, round 3)

- **Item:** OPT1-PR1, "Record the owner's Option 1 decision".
- **Stage:** B (INDEPENDENT PLAN AUDIT), re-audit of a plan delta written after `SD-D`. I wrote no plan revision and hold no other stage of this change.
- **Audited text:** `opt1-pr1/PLAN-rev3.md`, **sha256 `e3f1739f0090ad74a503791938e82c98480de7543367ec34ef80d8a702230f44`**, verified with `sha256sum` at the start (2026-10-07T22:55:00Z) and at the end (see Timing). It is a delta against `PLAN-rev2.md` (`40691fe1…bc58`, unchanged), and only that delta was audited.
- **Inputs:**
  - `OWNER-EVIDENCE.md`, sha256 `08b0ec6dd7dabdb6a70c0f5dd72d308891f2cbf0ec8d73a10949ef45bdf73eb9` (§1–§6). Per the coordinator, rev3 may quote only §1–§4 and §5's "Parallel repair PRs", and §6 must not be imported.
  - `IMPL-AUDIT-1.md` (`827915bb…62b1ae`).
  - Codex review **5449260025** (`commit_id` `18109931a63f4542b976ea3c78918fe77dcb5124`, submitted 22:36:47Z) and its four threads, read with GitHub MCP `get_reviews` / `get_review_comments`. All four are unresolved and none is outdated.
  - PR #678 at head `18109931`. `git ls-remote` shows the branch and `refs/pull/678/head` both at `18109931…`, and main at `7d1d05e8…`.
- **Coordinator decision applied:** X1 is accepted (delete this PR's two "Still open" rows; relabel D73's legend).

## Disposition

**`SD-B: REVISE`** on `PLAN-rev3.md` sha256 `e3f1739f…0f44`.

Most of rev3 is correct:

- the APR-115 path pinning;
- the APR-114 split-PR coverage, quoted exactly from §5;
- D73 rows 2, 4, 10 and 11;
- the X1 implementation;
- the ledger bullets;
- the forecast edit;
- the new and changed checks.

Four defects fail the coordinator's explicit checks. Two are in the preservation wording (it must be "sound"). One concerns reply accuracy and §6 (the replies must be "accurate", and §6 must "not be imported"). One reverses a fix that was already accepted. Each is a one-sentence change, with exact replacement text given below, so a rev4 delta should be quick to re-audit. rev3's §2 is labelled "Exact text changes", so these cannot be left to Stage C to correct silently.

## Aegis skills used

| Skill | Why it applies now | What it inspected | Result |
| --- | --- | --- | --- |
| `scoped-approval-register` | rev3 changes AEGIS-APR-114 and -115 before they become immutable. | The APR-115 pin against "Nothing else is covered."; the APR-114 §5 quotation; no invented negatives; no §6 import. | The pin and §5 coverage are sound. N1 and N2 are labelling nits. |
| `source-of-truth-reconciler` | rev3 makes claims about the head text, the tool's code, VERIFY and the owner record. | Each claim was checked against `18109931` text, `check_index.py`, VERIFY V10/V11, `OWNER-EVIDENCE.md` §1–§6 and the Codex threads. | B1, B2 and B4 are claims that the artifacts contradict. |
| `acceptance-criteria-reviewer` (partial fit) | rev3 changes K4, AC-5 and AC-6 and adds AC-14 and AC-15. | Each item for an observable outcome, a threshold and evidence. | All are mechanical or read-checkable. AC-5's amendment hides B3 instead of catching it. |

No MANUAL-ONLY skill was used. The plan-level verdict is procedural (`delivery-workflow.md:97`).

## Blocking findings

### B1 — D73 row 8's preservation condition cannot be met as literally worded

rev3 2.4(e) reads: "before the switch, **every recorded acceptance commit** is held by a durable preservation mechanism". D73 row 5 at the head uses the same phrase for the six lost commits: "A page whose **recorded acceptance commit** no longer exists anywhere (`65bacc7`, …)". VERIFY V11 shows those six are absent even after all 676 `refs/pull/*/head` refs are fetched. Read literally, row 8 can never be satisfied, so the switch could never pass. That is an unsound condition in an append-only record. The same wording is in the reply for r4212737366.

**Fix.** In row 8 and in the reply, write: "every acceptance commit that a keeper-table row records is held by a durable preservation mechanism that the repaired tool reads; commits already lost are governed by row 5, and no row binds them (row 4)."

### B2 — The blob-ID rationale is technically wrong

rev3 makes the same claim in three places:

- row 8 (2.4(e)): "it lets the build measure a page's change against the default branch **when the reviewed commit is not an ancestor of it**";
- "Easier" (2.4(h)): "lets the build measure a page's change against the default branch after a squash merge";
- reply r4212737366: "a way to measure change against the default branch after a squash".

Measuring change needs the commit **object**, not ancestry. `check_index.py:69-79` runs `git diff --numstat <sha> <ref> -- <path>`, which works for any two commits. The tool already measures non-ancestor acceptances: it computes `rebased = not revision_reachable(sha, ref_sha, root)` and then calls `numstat` anyway (`main()`). A blob only adds a measurement path when the commit object is gone. Under row 5 (the owner's lost-commit rule), such a page is pending regardless. rev3's conclusion is still right: the blob ID is not preservation. Only the rationale is wrong.

**Fix.**
- Row 8: replace the sentence with "The blob ID is a content check: it binds the row to the page's exact bytes at the recorded revision (row 4 verifies it). It is not preservation: …", keeping the rest of the sentence.
- 2.4(h): "A blob ID lets the build and a reviewer check that a row matches the page's exact content at its recorded revision."
- Reply r4212737366: "reframed as a content check, not as preservation".

### B3 — rev3 2.3 reintroduces U+2026, reversing the accepted R2-N1 fix

2.3 prescribes prefixing blockquotes 2 and 3 with `… ` (U+2026). At the head, the added lines contain 0 U+2026 (`git diff 7d1d05e8 18109931 | grep '^+' | grep -c '…'` → 0). IMPL-AUDIT-1 AC-5 records R2-N1 as applied. APR-113's own legend at the head reads '("..." marks the transcription's own omissions)', and blockquotes 4 and 6 use ASCII "...", as does `OWNER-EVIDENCE.md` (no U+2026 present). Following 2.3 would put two different omission marks in an entry that is immutable once merged. rev3's AC-5 amendment ("the check is the text after the `… ` prefix") accommodates the defect instead of catching it.

**Fix.** Prefix with `... ` (ASCII). Restate AC-5's amendment as "the text after the `... ` prefix", and add "0 U+2026 in the added lines".

### B4 — Reply r4212737359 imports §6's outcome

The reply says the authority is left open "because **a later register entry records it**". That presupposes the §6 answer: `OWNER-EVIDENCE.md` §6, "Yes, explicit grant (Recommended)", whose option text is "Recorded as a new approval register entry". The coordinator ruled that §6 must not be imported. This PR's records say the authority is not decided by this record (D73 row 11, APR-113 "Not decided"), so the reply should say the same.

**Fix.** Write: "is deliberately left open: this record does not decide it, and any later decision is recorded by a later pull request."

## Nits (non-blocking; fix in rev4 if cheap)

- **N1 — 2.4(i) over-claims.** "Whether one program function may be delivered in more than one pull request is no longer open" is too broad. §5's "Parallel repair PRs" covers splitting **the tool repair** only, and APR-114 2.2(d) says so. Narrow it to: "… is no longer open for the tool repair".
- **N2 — Label the reading in APR-114.** In 2.2(a), "Each such pull request merges on the same terms." combines the Batch-1 "same terms" answer, which predates §5, with the §5 split. It is a sound reading, since the owner rejected "Ask me per PR" and then asked for the repair to be split, but it is the recorder's reading, not text from either answer. Label it, as rev2 did for the backfill mapping.
- **N3 — Row 2's event kind is a closed list.** "either a full-page acceptance or a targeted review" leaves no room for VERIFY C4a's proposed explicit `lost` rows. Row 5 requires lost-commit rows "never dropped silently", while row 4 says an unverifiable row "is not written". Either say "at least these two kinds", or state that the backfill's reviewed report (not a table row) is how lost acceptances stay visible. This is not a contradiction today, but it narrows PR2's design more than the audit did.
- **N4 — Row 8's source label against the legend.** The label is "Owner (the coordinator's summary: 'acceptance commits preserved')", but the legend says **Owner** means "the owner's words quoted in AEGIS-APR-113 to AEGIS-APR-115", and APR-113 calls that summary "not a quotation". Either widen the legend ("… or an owner-approved condition AEGIS-APR-113 records") or use "Owner (approved condition, in the coordinator's summary)". This also keeps AC-14's "only the legend's four labels" test meaningful.
- **N5 — The §5 option-text mapping is not labelled.** `OWNER-EVIDENCE.md` §5 lists four options but only three "Option texts", unlabelled. "Split the repair into small PRs …" belongs to "Parallel repair PRs" by content, and the coordinator says so. Have the coordinator label the mapping in `OWNER-EVIDENCE.md`, or confirm it in the Stage C brief, so AC-5 compares against a labelled source.

## Confirmed sound

- **Findings and threads.** rev3's four thread IDs match the live threads:
  - r4212737350: evidence, `step-0…:3797`;
  - r4212737359: targeted review, `:3806`;
  - r4212737366: durable refs, `:3803`;
  - r4212737371: pinned paths, register `:4814-4817`.

  Each Codex request is addressed: an evidence pointer validated before counting; an event kind plus the retained and targeted revisions; a durable mechanism before the switch; and pinning plus a new decision when outputs change. Every head citation rev3 uses was verified: ledger `:3286` header `| Page | Acceptance revision | Reviewer | Evidence source | Date |`; `:3395` "**Still separately unresolved, and still undecided.**"; register `:4657` "acceptance commits are preserved"; `:4802` "Nothing else is covered."; `git grep -c owner-decision-on-the-count 18109931 -- '*.md'` → 0 files.
- **The APR-115 pin matches "Nothing else is covered." without inventing a restriction.**
  - It names exactly the two files `build_index.py --write` writes (`INDEX_REL` / `STAGE1_REL`, `build_index.py:58-59, 669, 702`).
  - "No other path" agrees with the existing FORBIDDEN ("excludes a pull request that also changes … any other page").
  - "A rebuild that changes only one of them is covered" stays inside "rebuild PRs".
  - For any other output set it decides nothing and applies the register preamble's citation rule. The quoted sentence is an exact prefix of the preamble's: "An action is covered only by an effectively ACTIVE human grant whose scope includes it".
  - Row 10's switch-plan escalation means nothing is foreclosed: a changed output set is raised with the owner before APR-115 becomes active.
  - AC-6's checks are mechanical: "Today" occurs once in the APR-115 block at the head, in the bullet being replaced.
- **APR-114's §5 coverage quotes §5 exactly.** A whitespace-collapsed substring check against `OWNER-EVIDENCE.md` §5 passes for the question "Which speed-ups do you want? Pick any.", the label "Parallel repair PRs", the option text, "backfill batches" and the time "22:29:29Z". "The owner's other selections in that answer are outside this entry" describes the entry's scope and is not a prohibition.
- **No §6 import in rev3 §2 (the text Stage C applies).** A scan for §6's labels and option texts ("explicit grant", "security-relevant (Recommended)", "Keep last known status", "22:30:07Z") and for the other three §5 options returns 0. The one leak is in a reply (B4).
- **D73 rows 2, 4 and 11.**
  - Row 2 keeps the existing table's five columns, adds an event kind and a blob ID, and quotes APR-101's binding ("to the exact reviewed revision and its posted evidence", verified at `:3148`). It honestly states that the offline build cannot validate GitHub evidence.
  - Row 4's exclusion is correctly scoped to full-page rows from the prose backfill, and the targeted-review authority is left to row 11.
  - Row 11 measures the 10 lines from the retained full-page acceptance, which matches the ledger's net-difference rule ("the net difference between the page's accepted version and now"). The authority stays Open.
- **X1 is complete.** All three added references to the removed items are handled: the legend (head added line "**Open** means undecided."), D73's "Items 1 and 3 are listed under 'Still open …'" and the open-decisions row's "stay open (below)". The two deleted rows are this PR's own additions, so AC-2 and AC-3 against base `7d1d05e8` are unaffected. AEGIS-APR-113's "Not decided by this entry" stays true as worded.
- **Ledger bullets (2.5).** `ACCEPT_RE`, `RETENTION_RE`, backticked-SHA and bare-SHA checks over the block all return 0, and there are no table rows. Both anchors exist (head headings `:3268` and `:3378`). The quotations are verbatim, with case preserved (N-1 fixed).
- **Forecast (2.7)** changes no estimate.
- **Checks.**
  - K4: dropping "the new ledger heading" is correct, since nothing links to it.
  - K9–K12: unchanged in method.
  - AC-14: a read plus grep, specific enough to be mechanical.
  - AC-15: matches `MG3` (triage by reply; no thread resolution), and posting replies falls under AEGIS-APR-003 ("Project Aegis pull requests may be updated as needed").
- **Chain-rule statement (§4)** is correct: exact-head invalidation voids D, E and F at `18109931`, and Stage F re-hashes the bound fields.

## For rev4

Apply B1–B4 with the fix texts above, and N1–N5 if cheap. Recompute the sha256. The re-audit will check only those sentences, AC-5's ASCII rule and the unchanged remainder.

## Not done / limits

- No repository edit, commit, push, PR edit, comment or thread resolution. GitHub was read only (`get_reviews`, `get_review_comments`, `ls-remote`). No `git fetch` was run, and the head object was already local.
- I did not re-run K11 on rev3's text: the ledger bullets were checked directly against the harvester's regexes. The rev2 simulation method stands, and Stage C re-runs K11 at the new head.
- I cannot read the owner's chat. `OWNER-EVIDENCE.md` is the owner record.
- Reserved scope was not touched.

## Timing

- **Item:** OPT1-PR1 Stage B round 3. **ETA used:** rev3's 15–25 min (`PLAN-rev3.md:254`). This subagent had no owner channel to announce it.
- **Start:** 2026-10-07T22:55:00Z (`date -u`).
- **Finish:** see the hand-off report (taken with `date -u` after this file's sha256).
