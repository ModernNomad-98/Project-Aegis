# OPT1-PR1 — PLAN AUDIT rev6 (Stage B, round 6)

- **Item:** OPT1-PR1. **Stage:** B (INDEPENDENT PLAN AUDIT). I wrote no plan revision and hold no other stage of this change.
- **Audited text:** `opt1-pr1/PLAN-rev6.md`, **sha256 `27f541544e7e386b1fc2f0a8443d51bea009a08538355330fafeafe2ff112bd3`** (109 lines), verified at the start (2026-10-08T00:27:57Z) and at the end (see Timing). It is a delta on rev5 (`8e853967…4e85`), rev4 (`7d4876f0…a733`), rev3 and rev2. All were re-hashed and are unchanged.
- **Inputs:**
  - `OWNER-EVIDENCE.md` sha256 `21a65916…8e68`, unchanged.
  - `IMPL-AUDIT-2.md` sha256 `df70cb72…4075` (`SD-D: ACCEPT` at `dbb4cd67`, with M-1 and N-1 to N-4).
  - Codex review **5449970404** at head `dbb4cd6793cd583bc407f7152bb275f14945d56f`. I read its five new threads with GitHub MCP `get_review_comments`: r4213371765 (P1), r4213371774 (P2), r4213371781 (P2), r4213371788 (P2) and r4213371797 (P2). All five are unresolved and none is outdated. The four round-1 threads are now outdated and carry the round-1 replies.
- **Live state:**
  - `git ls-remote origin`: main `7d1d05e8…`; the branch and `refs/pull/678/head` are both at `dbb4cd67…`.
  - Open PRs: #678 only, at `dbb4cd67…`.
  - Local tree: clean at `dbb4cd67` on `claude/sharp-lovelace-urgxpz`.

## Disposition

**`SD-B: REVISE`** on `PLAN-rev6.md` sha256 `27f54154…2bd3`.

All nine responses to the review findings are correct against the head text and against `build_index.py`, and the five reply texts are accurate. My hostile pass found three defects in rev6's own rewrite of **D73 row 2**: the withdrawal mechanics added by change 3 and changes 4 and 6. They are the same class of defect Codex has found each round, and they would very likely draw the next Codex P1/P2. Each fix is one or two sentences, given below. Everything else is non-blocking.

## Aegis skills used

| Skill | Why it applies now | What it inspected | Result |
| --- | --- | --- | --- |
| `scoped-approval-register` | The APR-113 Event pointer and the APR-115 quotation change, and D73 interprets APR-117's owner text. | Fidelity of each owner quotation, and any reading that narrows or extends an owner sentence. | B2 (the "affected page" reading must be labelled) and N1. |
| `source-of-truth-reconciler` | rev6 makes claims about the head, `build_index.py`, `VARIANTS.md` and the owner record. | Every line citation at `dbb4cd67`, every `build_index.py` line, every VARIANTS claim, every quotation. | All cited facts verified. B1, B3, N2 and N4 are internal inconsistencies. |
| `acceptance-criteria-reviewer` (partial fit) | The checks AC-6, -9, -14, -18 and -19 and the new K20 change. | Observable outcome, threshold and evidence. | Mechanical. N5 and N6 are wording notes. |

No MANUAL-ONLY skill was used. The plan-level verdict is procedural.

## Verification of rev6's findings table (§1) against the head and the tool

| Item | Head or tool fact | Verified |
| --- | --- | --- |
| r4213371765 | D73 row 2 at `step-0…:3815` lists "a withdrawal (AEGIS-APR-117)" with no target field | Yes. The row starts at `:3815`. |
| r4213371781 | Register `:4562-4564`: "The owner's work and merge authority for this program are AEGIS-APR-114 and AEGIS-APR-115." | Yes |
| r4213371788 | Open-decisions `:314-315` lists the lighter path under "Prerequisites on resume" | Yes |
| r4213371774 / K20 | `build_index.py:631` `ap.add_argument("--ref", default="HEAD")`; `:672` `"source_revision": git("rev-parse", args.ref, …)`; `:696` `"source_revision": payload["source_revision"]` | Yes, all three lines (`grep -n 'default="HEAD"\|"source_revision"'`). The self-reference argument is correct: a rebuild committed at its parent records the parent, and a re-run at the candidate head records the candidate. |
| r4213371797 | Conversion note `:450`: "**Nothing is in effect:** …" | Yes |
| M-1 | Ledger `:25-26`: "will one day give" | Yes |
| N-1 | Register `:4932-4933` cut at "…whose scope includes it." The preamble's full sentence, "An action is covered only by an effectively ACTIVE human grant whose scope includes it, after considering the full history and any actual limits.", is found verbatim in the first 20 lines of the main register. | Yes |
| N-4 | 609 − 602 = 7. Main's reconciliation says "The seven are reader pages added after `d6e48418`". | Yes |
| D73 row lines | rows 2, 3, 8 and 11 at `:3815`, `:3816`, `:3821` and `:3824` | Yes |

**Quotations.** "The affected page becomes pending again." is exactly the end of APR-117's option text in `OWNER-EVIDENCE.md` §7 (whitespace-collapsed substring). "AEGIS-APR-101 unchanged", "Parallel repair PRs" and "Nothing else is covered." also match. rev6's §2 new text contains no U+2026; the two in §2 are in a location description, which is plan text. No new owner attribution appears, except the reading in B2.

**The five reply texts are accurate** to rev6's changes. r4213371774's "`--ref` defaults to `HEAD`, and the resolved ref is written as `source_revision` into both generated files" matches the tool. B1–B3 require small edits to the r4213371765 reply; see the fixes.

## Blocking findings

All three are in D73 row 2 as rev6 rewrites it (changes 3, 4 and 6).

### B1 — A withdrawal may name any event, of any page, and the build does not reject that

Change 3 reads: "A withdrawal names, by identifier, the event it cancels". Change 6 rejects only a withdrawal "that names no earlier event". So the schema lets a withdrawal name:

- another **withdrawal**. Under change 4 ("A cancelled event stops counting from the withdrawal on"), that would leave it undefined whether the first withdrawal's target counts again. It also contradicts change 4's own rule that "A mistaken withdrawal is corrected by recording the qualifying review again as a new event";
- a **lost-kind event**, which "never counts as an acceptance", so there is nothing to cancel;
- an event of a **different page** from the page the withdrawal records.

AEGIS-APR-117's Scope allowed covers only a withdrawal "that cancels a recorded acceptance row that turns out to be wrong". So the schema also permits keeper actions the grant does not cover.

**Fix (change 3 and change 6):**

- "A withdrawal names, by identifier, the earlier full-page-acceptance or targeted-review event **of the same page** that it cancels; it cannot cancel a withdrawal or a lost-kind event."
- Add to the rejection list: "whose withdrawal names no earlier full-page-acceptance or targeted-review event of the same page".
- APR-117 says "acceptance row". Either state as this record's reading that a targeted-review row, which records that a page stays accepted, is such a row, or mark withdrawing a targeted-review row as **Open**.

### B2 — The "affected page" rule is presented as the owner's sentence, but it is a conditional reading of it

Change 4 reads: "A page whose status rested on the cancelled event becomes pending again (AEGIS-APR-117: \"The affected page becomes pending again.\"), and a later valid event for the same page is not cancelled."

The owner's sentence is unconditional. D73's rule is conditional: in Codex's A-then-B case, the page does **not** become pending. That reading is sound and is what Codex asked for. But citing the owner's sentence as if it said the conditional rule turns D73's Audit reading into the owner's words. The `scoped-approval-register` gotcha is "Paraphrase drift … is a fabricated widening".

**Fix:** "A page is *affected*, as this record reads AEGIS-APR-117's \"The affected page becomes pending again.\", when its status rested on the cancelled event; such a page becomes pending again, and a later valid event for the same page is not cancelled."

Also make two related corrections:

- the next sentence's "recording the qualifying review again as a new event under AEGIS-APR-101" becomes "… under AEGIS-APR-101, or AEGIS-APR-116 for a targeted review";
- the r4213371765 reply's "matching AEGIS-APR-117's …" becomes "as D73 reads AEGIS-APR-117's …".

### B3 — Row 2's opening schema sentence now contradicts the fields it lists

Row 2 keeps (it is not replaced by change 3): "The table keeps the information in the existing keeper table's columns (…) **and adds an event kind and a blob ID.**" rev6 then adds more fields:

- a stable identifier on every event;
- the retained full-page acceptance's identifier, on a targeted review;
- the cancelled event's identifier, on a withdrawal.

The opening sentence still says only two are added. That is the same kind of inconsistency between "pinned schema" and listed fields that Codex raised in r4212737350 and r4212737359.

**Fix:** "… and adds an event kind, a blob ID, a stable identifier for every event, and the identifier of the event a targeted review builds on or a withdrawal cancels."

## Non-blocking findings (fix in rev7 if cheap)

- **N1 — APR-113's new Event pointer describes AEGIS-APR-115 loosely** (change 1). It reads "AEGIS-APR-114 and AEGIS-APR-115, the delivery grants (work and merge authority **for the program's pull requests**)". AEGIS-APR-115 covers routine **rebuild** pull requests **after a switch**, not the decision record, repair or switch. Write "(AEGIS-APR-114: the program's pull requests; AEGIS-APR-115: routine rebuild pull requests after a switch)". The r4213371781 reply follows the same text.
- **N2 — Row 4 against change 5.** Row 4 says "A row that cannot be verified is not written, so its page counts as pending". Change 5 allows a lost acceptance to be recorded "as an event of its own kind that records the lost revision". Say "is not written **as an acceptance**" in row 4, or keep change 5's backfill-report option only.
- **N3 — The pinned base can lag the default branch at merge** (change 8). If a keeper recording merges while a rebuild PR is open, the rebuild, pinned to its older base, merges an index that omits that recording. Row 7's "after each keeper recording" schedule limits this to a transient lag, since another rebuild follows, and `source_revision` shows the base. A one-line requirement would remove the next likely Codex finding: "if the default branch has moved by merge time, the rebuild is redone at the new tip".
- **N4 — Change 12 is still incomplete.** `opt1-pr2/VARIANTS.md:108` says V2 also changes "Parallel repair PRs" in part: "4 PRs instead of 10, with one backfill PR instead of batches". Add "and partly changes 'Parallel repair PRs'" to the V2 clause.
- **N5 — IMPL-AUDIT-2 N-2 is unaddressed.** rev2's AC-6 grep (`blob|40-character|tagg|verifiable`) returns 1 over the whole APR-113 block, because of the verbatim label "V2: verifiable only (Recommended)". Restate it as being over APR-113's Scope allowed bullet, where it returns 0.
- **N6 — AC-6's new `grep -F` needs the phrase on one line.** At the head, the APR-115 quotation is wrapped across two lines (`:4932-4933`), and the longer full sentence will wrap too unless kept on one line. Name the rev2 §7 one-line convention in AC-6 so that the grep is not a false fail.
- **N7 — Change 15's "today's 609"** should be "the 609 reader pages on main after PR #677", so that the dated note does not depend on the reading date.

## What holds

- **Changes 1, 2, 7, 9–17**, and changes 5 and 8 apart from N2 and N3, are correct against the head text and introduce no new owner attribution:
  - **H1, row 3:** AEGIS-APR-101 unchanged is the owner's option text; 116 and 117 are the owner's grants.
  - **H4, row 11:** "covers the change from the retained acceptance up to its reviewed revision; a later change needs its own review" matches the ledger rule: "Either review must cover every changed line …", with net difference measured from the accepted version.
  - **H5:** V1 dropping, and V3 reversing, "Parallel repair PRs" matches `VARIANTS.md:71, :135`; N4 is the V2 gap.
  - **Change 8:** the self-reference is real (K20); pinning to the PR's base fixes the zero-diff check.
  - **Change 13:** APR-113 and APR-118 are the two policies in effect at merge.
  - **Change 10:** removes the fast path from the prerequisites, consistent with APR-113 item 8 and D73 row 9.
- **Harvester safety** of changes 14 and 15 (ledger) and 13 (conversion note): no accept-verb, no *keep … acceptance*, no SHA, no table row. K11 remains required at Stage C.
- **New and extended checks:** AC-9, AC-14, AC-18, AC-19 and K20 are mechanical, with stated expected values. AC-6 is mechanical subject to N5 and N6.
- **Hostile pass, no further defect:**
  - APR-113's Scope allowed items 1–9 and FORBIDDEN;
  - APR-114: the split-PR FORBIDDEN, the expiry, and the consumption recorded by the switch;
  - APR-115: the pinned files and the full preamble sentence (after change 2);
  - APR-116: the table defined, labelled as the recorder's reading;
  - APR-118: confirms `CONTRIBUTING.md:243-245`;
  - D73 rows 4–7 and 9–11 (row 4 apart from N2);
  - the backlog item after changes 10–12 (N4 apart).

## For rev7

Apply B1–B3 with the fix texts above, update the r4213371765 reply to match, and apply N1–N7 if cheap. Recompute the sha256. The re-audit will check row 2, the reply, and that nothing else changed.

## Not done / limits

- No repository edit, commit, push, PR edit, comment or thread resolution. GitHub was read only (`get_review_comments`, `ls-remote`, the open-PR list). No `git fetch` was needed: the head object was already local.
- K11 was not re-run. The new ledger and conversion-note text was checked against the harvester's patterns.
- I cannot read the owner's chat. `OWNER-EVIDENCE.md` is the owner record.
- Reserved scope was not touched.

## Timing

- **Item:** OPT1-PR1 Stage B round 6. **ETA:** none was stated for this round. This subagent had no owner channel.
- **Start:** 2026-10-08T00:27:57Z (`date -u`).
- **Finish:** see the hand-off report (taken with `date -u` after this file's sha256).
