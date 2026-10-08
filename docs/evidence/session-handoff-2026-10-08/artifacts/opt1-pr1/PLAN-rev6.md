# OPT1-PR1 — PLAN rev6 (a short delta against rev5)

> **REVISION MARKER: rev6.**
>
> - **Effective plan:** rev2, then rev3, then rev4, then rev5 (`8e8539679de094d0f1cdd8c06a8991fb3fef407e79b79f157d887947fba94e85`), then this file. Where rev6 is silent, the earlier revisions govern. None of them is modified.
> - **Why rev6:** two reviews of PR #678 at head **`dbb4cd6793cd583bc407f7152bb275f14945d56f`**:
>   - Codex review **5449970404** raised five new threads;
>   - the Stage D round-2 audit `IMPL-AUDIT-2.md` (sha256 `df70cb724760e459367170978ccfe378db59820e1b6cf8c6237544259bc84075`) raised M-1, N-1, N-3 and N-4.
> - **Hostile re-read:** at the coordinator's request, I re-read D73 conditions 2–11 and the backlog item as a hostile reviewer would. §3 lists what that changed.
> - **Live state, re-derived at 00:23Z:** `origin/main` = `7d1d05e8…` (unchanged); `refs/pull/678/head` = `dbb4cd67…`; local tree clean at `dbb4cd67`. I ran `git fetch` for remote-tracking refs only.

- **Planner:** the same PLAN-stage subagent. It made no repository edit, commit, push, PR comment or thread resolution. GitHub was read only (`get_review_comments`).
- **rev6 start:** 2026-10-08T00:23:47Z (`date -u`).
- **Skills used:**
  - `scoped-approval-register`: the AEGIS-APR-113 pointer and the AEGIS-APR-115 quotation, before both become immutable;
  - `source-of-truth-reconciler`: each finding checked against the head text and `build_index.py`;
  - `acceptance-criteria-reviewer` (partial fit): the new checks.

  No MANUAL-ONLY skill was used.

## 1. Findings verified against the head (`dbb4cd67`)

| Finding | Verified | Verdict |
| --- | --- | --- |
| **Codex r4213371765** (P1): withdrawal rows need a target | D73 row 2 (`step-0…:3815`) lists "a withdrawal (AEGIS-APR-117)" as an event kind, but no row field names which event a withdrawal cancels, and no event has an identifier. Codex's case (accepted at A, later accepted at B, then A withdrawn) has no unambiguous outcome. | **ADOPT.** Row 2 gives every event a stable identifier, and a withdrawal names the event it cancels. The resolution keeps the owner's "The affected page becomes pending again": the page goes pending when its status rested on the cancelled event, and a later valid event is not cancelled. |
| **Codex r4213371781** (P2): APR-113's authority pointer | Register `:4562-4564`: "The owner's work and merge authority for this program are AEGIS-APR-114 and AEGIS-APR-115." Its own Status two paragraphs below names "AEGIS-APR-114 to AEGIS-APR-117". | **ADOPT.** The Event line names all four and separates delivery grants (114, 115) from keeper-role grants (116, 117). |
| **Codex r4213371788** (P2): optional fast path listed as a prerequisite | Open-decisions `:314-315` lists "the lighter rebuild review path …" under "Prerequisites on resume". APR-113 item 8 says "This entry does not decide that review path", and D73 row 9 keeps the seven stages. | **ADOPT.** It moves to an "Optional follow-up" line, which says the normal seven-stage path is enough without it. |
| **Codex r4213371774** (P2): the zero-diff rebuild check is self-referential | `build_index.py:631` gives `--ref` the default `"HEAD"`. `:672` writes `"source_revision": git("rev-parse", args.ref …)` into the index, and `:696` copies it into the stage-1 file. Both committed files carry `source_revision` today (`d6e48418…`). A rebuild made before its commit records the parent; re-running it at the candidate head records the candidate, so the diff is never zero. | **ADOPT**, by pinning the input ref. Row 8 pins `--ref` to the rebuild PR's base commit on the default branch, named in the PR, and the reviewer rebuilds at that same ref. The alternative Codex offers — a format with no self-reference — is left open to the tool-repair plan. |
| **Codex r4213371797** (P2): conversion note says "Nothing is in effect" | Conversion note `:450`, "**Nothing is in effect:** …". AEGIS-APR-113 is "ACTIVE as policy once this entry is on the default branch", and AEGIS-APR-118 "takes effect then, independent of the paused program". | **ADOPT.** The claim is limited to the repair, the switch and the changed count, and the two policies in effect are named. |
| **IMPL-2 M-1:** "will one day give" overstates the decision | Ledger `:25-26`. The owner's pause text is "decide later whether the repair is worth it". | **ADOPT**: "would give … after a gated repair". |
| **IMPL-2 N-1:** the APR-115 quotation is cut mid-sentence | Register `:4932-4933` ends "…whose scope includes it." The preamble at `APPROVAL_REGISTER.md:10-11` continues ", after considering the full history and any actual limits." | **ADOPT**: quote the full sentence exactly. |
| **IMPL-2 N-3:** the skills table's Stage D round-1 row | PR body bound field (`IMPL-AUDIT-1.md` also applied `scoped-approval-register`) | **ADOPT**: add `scoped-approval-register` to that row. This is a PR-body change; Stage F re-hashes the bound fields. |
| **IMPL-2 N-4:** 602 and 609 appear side by side unexplained | Ledger note bullet 2. 609 − 602 = 7; VERIFY V33 found 7 reader pages added after the index's `source_revision` `d6e48418`. | **ADOPT**: one clause. |

None is rejected.

## 2. Exact text changes (to this PR's own added lines; base lines untouched)

**Harvester safety.** Changes to the ledger and the conversion note follow the K11 wording rules:

- no *accept*, *accepts*, *accepted* or *re-accepted*;
- no *keep*, *keeps* or *keeping* within 40 characters of *acceptance*;
- no hex SHA;
- no table rows.

| # | Finding | File: location at `dbb4cd67` | Old | New |
| --- | --- | --- | --- | --- |
| 1 | r4213371781 | Register, AEGIS-APR-113 Event (`:4562-4564`) | "The owner's work and merge authority for this program are AEGIS-APR-114 and AEGIS-APR-115." | "The owner's grants for this program are AEGIS-APR-114 and AEGIS-APR-115, the delivery grants (work and merge authority for the program's pull requests), and AEGIS-APR-116 and AEGIS-APR-117, the keeper-role grants (targeted-review rows and withdrawal rows). None of them covers any work while the program is paused (Status below)." |
| 2 | N-1 | Register, AEGIS-APR-115 Scope allowed (`:4932-4933`) | "\"An action is covered only by an effectively ACTIVE human grant whose scope includes it.\"" | "\"An action is covered only by an effectively ACTIVE human grant whose scope includes it, after considering the full history and any actual limits.\"" |
| 3 | r4213371765 + §3 H2/H3 | D73 row 2 (`:3815`), the "Each row records: …" sentence through "… and the date." | (the head sentence) | "Every row is an event. Every event has a stable identifier, unique within the table and never reused or changed, and records the page, the event kind, the evidence pointer and the date. The event kinds include at least: a full-page acceptance; a targeted review (AEGIS-APR-116); and a withdrawal (AEGIS-APR-117). A full-page acceptance and a targeted review also record the reviewed revision (the full 40-character commit the review read), the page's blob ID at that revision and the reviewer. A targeted review also names the retained full-page acceptance of the same page by its identifier and revision. A withdrawal names, by identifier, the event it cancels; it records no reviewed revision or blob ID." |
| 4 | r4213371765 | D73 row 2, after the evidence-pointer sentence | — | Insert: "For a withdrawal, the evidence pointer leads to the evidence that shows the cancelled event was wrong. A cancelled event stops counting from the withdrawal on, and the page's status is decided from its remaining events. A page whose status rested on the cancelled event becomes pending again (AEGIS-APR-117: \"The affected page becomes pending again.\"), and a later valid event for the same page is not cancelled. A targeted review whose retained acceptance is cancelled stops counting too. A mistaken withdrawal is corrected by recording the qualifying review again as a new event under AEGIS-APR-101; nothing is rewritten." |
| 5 | §3 H3 | D73 row 2, the sentence "A lost acceptance is never dropped silently: it is listed in the backfill's reviewed report or as a row of its own kind (row 5)." | (that sentence) | "A lost acceptance is never dropped silently. It is listed in the backfill's reviewed report, or as an event of its own kind that records the lost revision without binding it; such an event never counts as an acceptance (rows 5 and 8)." |
| 6 | §3 H2 | D73 row 2, the sentence "The build rejects, and does not count, a row whose evidence pointer is missing or malformed." | (that sentence) | "The build rejects loudly, and does not count, any row whose evidence pointer is missing or malformed, whose identifier is missing or duplicated, whose withdrawal names no earlier event, or whose targeted review names a retained event that is not a full-page acceptance of the same page." |
| 7 | §3 H1 | D73 row 3 | "The keeper keeps recording in the ledger under AEGIS-APR-101, unchanged except for the table's format." | "The keeper keeps recording in the ledger under AEGIS-APR-101, unchanged except for the table's format. Two separate grants add to the keeper's role: targeted-review rows once the fixed-format table exists (AEGIS-APR-116), and withdrawal rows after a switch (AEGIS-APR-117). Neither changes AEGIS-APR-101." Source cell: "Owner (AEGIS-APR-101 unchanged; AEGIS-APR-116 and AEGIS-APR-117)". |
| 8 | r4213371774 | D73 row 8 (`:3821`), the sentence "Rebuilds run only in a full clone that has fetched `refs/remotes/**` and `refs/pull/*/head`, and the reviewer rebuilds and requires a zero diff." | (that sentence) | "Rebuilds run only in a full clone that has fetched `refs/remotes/**` and `refs/pull/*/head`. The build's `--ref` is pinned to the rebuild pull request's base commit on the default branch, named in the pull request, and never to the rebuild's own commit. The reason is that the build records its input ref as `source_revision` in both generated files (`tools/readability_acceptance/build_index.py`), so a run at the candidate head would always differ. The reviewer rebuilds at that same ref and requires a zero diff. A repaired format that records no self-reference is also acceptable, if the tool-repair plan chooses it (row 6)." |
| 9 | §3 H4 | D73 row 11, "carrying the reviewed revision, its blob ID, the retained full-page acceptance revision, the reviewer and the evidence pointer." | (that phrase) | "carrying the reviewed revision, its blob ID, the retained full-page acceptance (its identifier and revision), the reviewer and the evidence pointer. A targeted review covers the change from the retained acceptance up to its reviewed revision; a later change needs its own review, as the rule says of any unreviewed edit." |
| 10 | r4213371788 | Open-decisions backlog bullet, "Prerequisites on resume" (`:314-315`) | "- the lighter rebuild review path, which the owner chose to raise at the 2026-10-11 review-cap check-in." | Delete it from the prerequisites list. Add after that list, before "**Resume trigger:**": "- **Optional follow-up, not a prerequisite:** a lighter review path for machine-checked rebuild pull requests, which the owner chose to raise at the 2026-10-11 review-cap check-in. Without it, rebuilds use the normal seven-stage path." |
| 11 | §3 H5 | Open-decisions backlog bullet, "What it is" | "seed that table once, then make the acceptance index the official pending count" | "seed that table once by the one-time reviewed backfill of option B, then make the acceptance index the official pending count" |
| 12 | §3 H5 | Open-decisions backlog bullet, the V2 item's last sentence | "It would narrow option B's backfill, so it needs the owner's confirmation;" | "It would narrow option B's backfill, so it needs the owner's confirmation; V1 would drop that backfill and V3 would reverse "Parallel repair PRs", so each of them would need the owner's decision too;" Move that clause to after the V3 item if it reads better there; the content is unchanged. |
| 13 | r4213371797 | Conversion note (`:450`) | "**Nothing is in effect:** the owner paused the program after this decision record, and a switch happens only if the owner resumes it." | "**The repair, the switch and any changed count are not in effect:** the owner paused the program after this decision record, and a switch happens only if the owner resumes it. Two policies are in effect: AEGIS-APR-113, as policy, and AEGIS-APR-118's security classification of the tool." |
| 14 | M-1 | Ledger note (`:25-26`) | "the owner decided that the acceptance index will one day give the official readability pending count," | "the owner decided that the acceptance index would give the official readability pending count after a gated repair," |
| 15 | N-4 | Ledger note, second bullet | "out of 602 indexed pages." | "out of 602 indexed pages (the index lists no page added after it was built, which is 7 of today's 609 reader pages)." |
| 16 | N-3 | PR body skills table (a bound field), Stage D round-1 row | "`code-reviewer`" | "`code-reviewer`, `scoped-approval-register`" |
| 17 | consistency (rev3 X3: ledger self-cost) | Ledger note, "Self-cost" | "This note adds N lines" | Re-measure at the new head (rev3 X3). |

## 3. Hostile re-read of D73 rows 2–11 and the backlog item: what else changed, and why

| # | Finding | Why it would have drawn another round | Fix |
| --- | --- | --- | --- |
| **H1** | Row 3 says the keeper is "unchanged except for the table's format", while AEGIS-APR-116 and -117 add keeper powers. | A direct contradiction inside D73, of the same kind as Codex r4213371781. | Change 7 |
| **H2** | Row 2's per-row fields are written for review events only. A withdrawal has no reviewed revision or blob ID, and the build's rejection rule does not cover a missing or duplicate identifier, a withdrawal naming nothing, or a targeted review resting on the wrong kind of event. | An underspecified schema point, of the same kind as Codex r4212737359 and r4213371765. | Changes 3 and 6 |
| **H3** | Row 2's "a row of its own kind" for lost acceptances, read against row 8's "no row binds them (row 4)". | An ambiguity: is a lost-kind row a binding? | Change 5: a lost-kind event "records the lost revision without binding it" and "never counts as an acceptance". This keeps row 8's exact B1 wording. |
| **H4** | Row 11 names the retained acceptance by revision only, and does not say what a targeted review covers. | Two events can share a revision (for example, a re-recording after a withdrawal), and a later edit would look covered. | Change 9: name it by identifier and revision, and limit coverage to the change up to its reviewed revision, which is the written rule's own logic. |
| **H5** | Backlog "What it is" says "seed that table once" while V1 has no backfill. Only V2 is flagged as needing owner confirmation, but `opt1-pr2/VARIANTS.md` says V1 drops option B's backfill and V3 reverses "Parallel repair PRs". | An internal contradiction, and an incomplete prerequisite of the same kind as r4213371788. | Changes 11 and 12 |
| — | Rows 4–7 and 9–10 | Re-read with no contradiction found. Row 6 ("inputs are read at `--ref`") and row 7 (page set at `--ref`) agree with change 8's pinned ref. Row 10's scope fence fits a rebuild that writes only the two named files. Row 5's "A commit still held by a pull-request head is not lost (row 8)" agrees with row 8's discovery-versus-preservation split. | none |

## 4. Changes to checks and acceptance criteria

| Item | Change |
| --- | --- |
| **AC-6** (extended) | AEGIS-APR-113's Event names AEGIS-APR-114 to AEGIS-APR-117, with "delivery grants" and "keeper-role grants". AEGIS-APR-115 contains the preamble sentence in full: check that `grep -F 'whose scope includes it, after considering the full history and any actual limits.'` over the AEGIS-APR-115 block returns 1. |
| **AC-9** (extended) | `grep -c 'Nothing is in effect'` over the added lines = 0. The conversion note names AEGIS-APR-113 and AEGIS-APR-118 as in effect. |
| **AC-14** (extended) | The read and grep over D73:<br>• Row 2 contains "stable identifier", and the withdrawal "names, by identifier, the event it cancels".<br>• Row 2's rejection list includes duplicated identifiers.<br>• Row 2's lost-acceptance sentence contains "without binding it".<br>• Row 3 names AEGIS-APR-116 and AEGIS-APR-117.<br>• Row 8 contains "never to the rebuild's own commit" and "source_revision".<br>• Row 11 contains "its identifier and revision".<br>• Row 8 still carries B1's sentence verbatim. |
| **AC-18** (extended) | `grep -c 'will one day'` over the added lines = 0. The ledger note contains "after a gated repair" and the 602/609 clause. |
| **AC-19** (extended) | In the backlog bullet, the "Prerequisites on resume" list contains no "lighter" (grep within that list = 0). An "Optional follow-up, not a prerequisite" line contains it together with "normal seven-stage path". The bullet names V1 and V3 as needing the owner's decision. |
| **K4, K10, K11** | Re-run at the new head with the same expectations: K4 `broken: 0 dead: 0`; K10 summary unchanged; K11 (a) identical, (b) identical after normalisation, (c) 0. The ledger and conversion-note text changed, so K11 is required. |
| **K20** (new) | Verify the self-reference fact cited in row 8: `grep -n 'default="HEAD"\|"source_revision"' tools/readability_acceptance/build_index.py` shows the `--ref` default and both writes. At the base this is `:631`, `:672` and `:696`. |

The declared not-verifiable items, the chain rule and the IDs are unchanged. The head moves, so the `SD-C` to `SD-F` verdicts bound to `dbb4cd67` become void and Stages C to F re-run, and Stage F re-hashes the bound fields (change 16).

## 5. Replies for the five new Codex threads

Post these after the fix head is pushed, replacing `<HEAD>`. Do not resolve the threads.

- **r4213371765** (withdrawal target):
  > Adopted in `<HEAD>`. D73 condition 2 now gives every event a stable identifier, unique within the table and never reused, and a withdrawal names by identifier the event it cancels. A cancelled event stops counting from the withdrawal on, and the page's status is decided from its remaining events. A page whose status rested on the cancelled event becomes pending again, matching AEGIS-APR-117's "The affected page becomes pending again.", while a later valid event for the same page (your A-then-B case) is not cancelled. A targeted review whose retained acceptance is cancelled stops counting too. The build rejects duplicate identifiers and withdrawals that name no earlier event. The program is paused (AEGIS-APR-113), so this is a condition on any future switch.
- **r4213371781** (authority pointer):
  > Adopted in `<HEAD>`. AEGIS-APR-113's Event line now names all four grants and distinguishes them: AEGIS-APR-114 and AEGIS-APR-115 are the delivery grants (work and merge authority for the program's pull requests), and AEGIS-APR-116 and AEGIS-APR-117 are the keeper-role grants (targeted-review and withdrawal rows). It also says none of them covers any work while the program is paused, which matches the Status paragraph.
- **r4213371788** (fast path as prerequisite):
  > Adopted in `<HEAD>`. The lighter review path is removed from "Prerequisites on resume" and listed as an "Optional follow-up, not a prerequisite", which the owner chose to raise at the 2026-10-11 review-cap check-in. The bullet says that without it, rebuilds use the normal seven-stage path.
- **r4213371774** (self-referential rebuild):
  > Adopted in `<HEAD>`. Verified against `build_index.py`: `--ref` defaults to `HEAD`, and the resolved ref is written as `source_revision` into both generated files. D73 condition 8 now pins the build's `--ref` to the rebuild pull request's base commit on the default branch, named in the PR and never the rebuild's own commit, and the reviewer rebuilds at that same ref for the zero-diff check. A repaired format without the self-reference remains acceptable if the tool-repair plan chooses it.
- **r4213371797** (conversion note scope):
  > Adopted in `<HEAD>`. The conversion note now says only that the repair, the switch and any changed count are not in effect, and it names the two policies that are: AEGIS-APR-113, as policy, and AEGIS-APR-118's security classification of the tool.

## Timing

- **rev6 start:** 2026-10-08T00:23:47Z (`date -u`). No ETA was announced, because this subagent has no owner channel.
- **rev6 finish:** see the hand-off report, taken with `date -u` after this file's sha256.
