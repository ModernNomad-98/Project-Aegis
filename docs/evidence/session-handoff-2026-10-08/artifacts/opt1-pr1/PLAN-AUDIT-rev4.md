# OPT1-PR1 — PLAN AUDIT rev4 (Stage B, round 4)

- **Item:** OPT1-PR1, "Record the owner's Option 1 decision", now including the pause.
- **Stage:** B (INDEPENDENT PLAN AUDIT). I wrote no plan revision and hold no other stage of this change.
- **Audited text:** `opt1-pr1/PLAN-rev4.md`, **sha256 `7d4876f04683ce57a0c856dffb7ed01f61354ee3f378c6572b5e50653b26a733`**, verified at the start (2026-10-07T23:39:33Z) and at the end (see Timing). It is a delta on rev3 (`e3f1739f…0f44`) and rev2 (`40691fe1…bc58`); both hashes were re-checked, and both are unchanged.
- **Owner record:** `OWNER-EVIDENCE.md`, now sha256 `21a65916f2f80ea553aac7b722d9d265f033d7bc4c3656cf9a04c74a7bac8e68`.
  - **§1–§8 are unchanged.** The first 107 lines hash to `f6d8213b465ddcf33350f870b3ef059dfd3a3f7ec989aafee3e02201b2b00347`, the value rev4 cites. Earlier prefixes still reproduce: the first 69 lines give `622fc6c3…` and the first 90 give `08b0ec6d…`.
  - **§9** (appended 23:39:12Z, after rev4) labels §5's three option texts, in order, as "Parallel repair PRs", "High effort for low-risk" and "Raise rebuild fast path later". It also adds the "Ask open decisions now" option text.
- **Coordinator directions applied:** §5–§7 are recorded now, superseding "do not import §6"; only the tool's security classification is effective now; the §8 instruction is recorded.
- **Live state, re-derived this turn:**
  - `git ls-remote origin`: main `7d1d05e8…`; the branch and `refs/pull/678/head` are both at `18109931…`.
  - Open PRs: #678 only, at `18109931…`.
  - Local tree: `claude/sharp-lovelace-urgxpz` at `18109931…`, clean.
  - Disclosure: I ran `git fetch -q origin` (remote-tracking refs only).

## Disposition

**`SD-B: REVISE`** on `PLAN-rev4.md` sha256 `7d4876f0…a733`.

rev4 gets the substance right:

- B1–B3 are applied word for word.
- The B4 deviation is justified.
- Every owner quotation in the six register entries and the open-decisions rows matches §1–§8 mechanically.
- The start conditions come from the owner's words.
- AEGIS-APR-118 rests on the verified `CONTRIBUTING.md:243-245` wording.
- Revising D73 in place is legal.
- The 18-page over-count, the tool figures, the 675-file count and the floor of 40 all re-derive.
- The new ledger note passes the harvester's patterns.
- The backlog estimates are labelled and traceable.

Four defects remain. Each is a one-sentence change in text that becomes immutable at merge:

- two register statements that the now-current owner record, or the plan itself, contradicts;
- one ambiguous FORBIDDEN clause;
- one unverified claim in the "no longer stale" ledger text the owner asked for.

## Aegis skills used

| Skill | Why it applies now | What it inspected | Result |
| --- | --- | --- | --- |
| `scoped-approval-register` | rev4 writes AEGIS-APR-113–118 before they become immutable. | Verbatim scope; start conditions from the owner's words; no invented negatives; widening by a new grant (116, 117); POLICY DECISION versus GRANT (118); the citation rule. | Typing, start conditions and quotations are sound. B1, B3 and B4 are wording faults. N1 and N2 are precision nits. |
| `source-of-truth-reconciler` | rev4 states current-state facts and cross-references. | Each figure and claim against main `7d1d05e8`, VERIFY, the tool's output, the coordinator log and `OWNER-EVIDENCE.md` §1–§9. | B2 (an unverified "higher"), B1 (superseded by §9), N2–N5. |
| `adr-sequencer` | D73 is revised in place. | Whether D73 has merged. | Unmerged (`git grep D73 origin/main` → 0); the precedent is APR-105's "has never been merged and has no recorded history to preserve". Legal. |
| `acceptance-criteria-reviewer` (partial fit) | AC-16..AC-19 and K17..K19 are new. | Observable outcome, threshold and evidence for each. | All mechanical or read-checkable. K19 is too weak for its claim (N6); AC-6's 116 wording is muddled (N7). |

No MANUAL-ONLY skill was used. The plan-level verdict is procedural.

## Blocking findings

### B1 — APR-113 item 6, and two related rows, contradict the owner record as it now stands (§9)

rev4 4.1(c) item 6 reads: "The transcription gives no text for the first one; it was acted on, in that the questions in items 7 **and 8** were asked." §9 now gives that option's text: "I put the three questions the repair needs to you now (targeted reviews, security classification, unmeasurable changes), each explained with a recommendation." Those three questions are §6, which is item 7. Item 8, the repair variant (§7 Q1), was not one of them.

So once §9 is the record, both halves of the sentence are false:

- there is now a transcribed text;
- it was acted on by item 7 only.

The same error appears in two other places:

- rev4 §1's table: "chosen (no option text transcribed) … acted on: §6 and §7 were asked";
- the open-decisions "Speed-ups" row (4.8(b)): "They apply only if the program resumes". That is wrong for "Ask open decisions now", which is done; rev4's own §1 marks it "done". It is also wrong for "Raise rebuild fast path later", which §1 marks as an agenda item.

**Fix.**

- **Item 6:** "The first option's text, transcribed by the coordinator in its later clarification, reads:", followed by the §9 text in a one-line blockquote, then "It was acted on: the three questions in item 7 were asked."
- **Speed-ups row:** "'Ask open decisions now' was acted on (the three questions recorded as AEGIS-APR-116, AEGIS-APR-118 and the counting rule); 'Raise rebuild fast path later' is an item for the 2026-10-11 check-in; the other two apply only if the program resumes."
- **AC-5:** add the §9 text, compared against `OWNER-EVIDENCE.md` §9.

### B2 — The ledger note asserts a figure that cannot be derived: "The true figure is higher"

rev4 4.6 says: "Its records support at least 40 pending pages … **The true figure is higher**, because this ledger treats a page it does not list as reviewed, and the pages have not been re-measured one by one".

On main `7d1d05e8`, the reconciliation it cites says only that the 40 is a floor carried forward. The 2026-10-03 note says "a re-run could only raise the floor". The same rev4 note states that the over-count's "full size … is not derivable". "Higher" (strictly more than 40) is therefore an unverified claim. The repository's rule is "Report the gap, never fill it", and this is the "no longer stale" text the owner asked for.

**Fix.** "The true figure **may be** higher: this ledger treats a page it does not list as reviewed, and the pages have not been re-measured one by one against their last full-page review."

### B3 — APR-113's new relationship sentence points at the wrong items, and at a section that does not exist

rev4 4.1(f) says: "AEGIS-APR-116 to AEGIS-APR-118 record the later answers listed in items 7 and 8, and in §1 of D73's decision."

- Item 8 records only the repair-variant answer (§7 Q1). The withdrawal answer recorded as APR-117 (§7 Q3) is not listed in any APR-113 item, and the split-PR answer (§7 Q2) is in APR-114.
- D73 has no "§1".

**Fix.** "AEGIS-APR-116 and AEGIS-APR-118 record two of item 7's answers; AEGIS-APR-117 records the withdrawal answer, and AEGIS-APR-114 the split-PR answer, both from the question batch that included item 8's; D73's decision list summarises all of them."

### B4 — APR-114's new FORBIDDEN clause can be read as narrowing the grant

rev4 4.2(c) says: "As the split-PR answer states, **it** 'covers the repair PRs only': the decision record and the switch are not split under it."

The first "it" can be read as AEGIS-APR-114 itself. A later merge agent would then read the entry as covering repair PRs only, and drop the switch, which the owner's "Yes, same terms (Recommended)" covers. The option text ("Recorded in the approval register; covers the repair PRs only.") limits the **split**, not the grant. AC-6 builds the ambiguous phrase into a check.

**Fix.** "The split-PR answer's option text says it 'covers the repair PRs only': only the tool repair may be delivered as several pull requests; the decision record and the switch are each one pull request under this entry." Adjust AC-6 to match.

## Nits (non-blocking; fix in rev5 if cheap)

- **N1 — APR-116's table reference.** "the keeper's acceptance record table (D73 condition 2) exists on the default branch" can be confused with the keeper table that already exists in the first ledger-keeper recording (`| Page | Acceptance revision | Reviewer | Evidence source | Date |`, base `:3241`). Read that way, APR-116 would be ACTIVE now. Say "the fixed-format table with D73 condition 2's schema, including the event-kind column, which the paused tool repair adds", and label it as the recorder's reading of "in the table".
- **N2 — The 2026-10-11 check-in description and citation** (APR-113 item 8; the "Still open" row). The cited log, `origin/coord/idle-check-2026-10-04:.coord/coordinator-cadence.jsonl:72` at `4d05c62443c8…`, dated 2026-10-04T16:19:40-07:00, reads: "the owner said No, table it, check back in 7 days. A reminder is scheduled for 2026-10-11T16:15". Two changes:
  - say the owner asked to check back in 7 days and the coordinator scheduled 2026-10-11, rather than "the date the owner set";
  - cite the commit `4d05c624`, not only the branch, because a branch can be deleted and the register entry cannot change.
- **N3 — "Nothing still claims work is active."** The forecast row "Decision record (this change) | … | **In progress** … the actual **will** exceed the estimate" becomes false at merge, and "will" is a prediction. Use: "Delivered by this change; actual measured at closeout (four plan rounds suggest it may exceed the estimate)."
- **N4 — The forecast pointer over-states what it corrects.** "corrected on two points" is inaccurate: the forecast note above (base `:18-30`) never mentions blind spots (`grep -c -i 'blind spot'` → 0). Say "corrected on one point … and one finding is added".
- **N5 — D73 "Harder" is stale against this PR's own forecast.** It still cites option B's "About 16–32 agent-hours (estimate)" as the cost. The forecast row says the variant estimates (25–45 to 55–103, plus V1's re-review) supersede it. Add "later variant estimates are in the backlog item".
- **N6 — K19 is weaker than the claim it supports.** Equal counts (675 at both refs) do not prove that no Markdown file was added or removed. Use `git diff --name-status --diff-filter=ADR 03c93c77 <base> -- '*.md' | wc -l` = 0. I measured: 675 at `03c93c77`, 675 at `7d1d05e8`, and 0 added, deleted or renamed. The commits are `03c93c77` = "(#676)" and `7d1d05e8` = "(#677)" (`git log --oneline`).
- **N7 — AC-6's APR-116 clause is muddled.** It says "0 for 117, and for 116 only in FORBIDDEN's not-decided sentence", yet the grep runs over Scope allowed. Expected: 0 for both Scope allowed bullets.
- **N8 — Backlog bullet convention.** The page's existing item states its estimate as "outside the bounded selected subtotal", and the section intro says listing an item "does not authorize its implementation". Add "outside the bounded selected subtotal" to the bullet; the forecast already says it.

## What was verified and holds

- **B1–B3 from rev3: applied exactly.**
  - Row 8 carries B1's sentence word for word: "every acceptance commit that a keeper-table row records is held by a durable preservation mechanism that the repaired tool reads; commits already lost are governed by row 5, and no row binds them (row 4)".
  - Row 8 also carries B2's "content check" sentence. The "Easier" bullet and the r4212737366 reply are corrected, and that reply carries B1 as well.
  - B3: the prefix is ASCII `... `; AC-5 requires 0 U+2026 in added lines; rev4's §4 drafts contain no U+2026.
- **B4 deviation: justified.** Under the coordinator's new direction, rev4 records §6 Q1 as AEGIS-APR-116, so the rev3 fix text ("any later decision is recorded by a later pull request") would be false at merge. The reply now says exactly what the PR records: APR-116, its start condition, the pause, and that backfill transcription is not decided. That keeps the finding's principle.
- **Owner quotations: mechanical.** A whitespace-collapsed substring check against the first 107 lines (§1–§8), with `\"`→`"`, matched all of the following:
  - every blockquote and bold label in §4.1–4.5 (29 items, including §5's four labels and three texts, §6's three questions, labels and texts, §7's three questions, labels and texts, and §8);
  - every label in the new open-decisions rows (10 items);
  - 13 inline phrases ("covers the repair PRs only", "never its own judgment", "No extra step for your own or the agents' PRs", the §7 follow-up question, the non-chosen labels, and others).

  §9 confirms rev4's assumed order of the §5 option texts (P1 satisfied).
- **Register entries 113–118.**
  - **Typing:** 113 and 118 are POLICY DECISIONs that grant nothing. 114–117 are GRANTs, and 116 and 117 are new grants that widen the keeper's role without touching AEGIS-APR-101 ("widening is a new grant").
  - **Start conditions:**
    - 114 covers the repair and the switch "only if the owner resumes", from "Merge the decision record, then stop here and decide later …".
    - 115 and 117 are "ACTIVE only after the switch …", from "After the switch".
    - 116 waits for the table, from "in the table"; see N1.
    - 118 is ACTIVE on merge, as the coordinator directed.
  - Each Scope allowed restates only its question and option text, and each FORBIDDEN says "None additionally stated" or quotes the option ("never its own judgment").
  - **118's wording is verified:** `CONTRIBUTING.md` at `7d1d05e8`, lines 243–245, reads "the Behavioral Eval Runner and / approval/evidence tooling under / `tools/`". `CONTRIBUTING.md` is not in the PR. The option's "No extra step for your own or the agents' PRs" matches `MG5`'s outside-only scope and `CONTRIBUTING.md:253-258` (every PR answers the question; only outside contributions get the extra review).
  - **IDs are free:** `git grep -c -e 'AEGIS-APR-11[6-9]' -e 'AEGIS-APR-12[0-9]' -e 'D74'` → 0 files on main and at the head. The head has 115 headings. None of the 40 most recent remote branches claims 116–118.
- **D73 revised in place: legal.** D73 is absent from main. The APR-105 precedent permits revising an unmerged entry. The revised D73 is consistent with the register: the legend is widened per N4, rows 2, 5, 11 and 14 are updated, and "Not decided" lists three items.
- **Ledger and forecast facts (truthful at the head, except B2):**
  - **The floor of 40:** main's reconciliation says "at least 40 pending" at `03c93c77`, which is main after #676.
  - **675 files:** the counts and the diff check are under N6.
  - **Tool figures:** 602 / 436 / 212 / 159 / 224 / 7 and "NOT DERIVABLE" at `7d1d05e8` (`opt1-audit/l1_check_index.json`, `compared_ref` `7d1d05e8…`).
  - **At least 18:** I re-ran K17 for the 12 listed pages at base `7d1d05e8`. All 12 have ≤10 changed lines, 0 added `+#` lines and are in the tool's `pending` set. The lines are 0, 10, 0, 0, 2, 2, 2, 10, 0, 0, 0, 0, exactly as rev4 states. The ledger names each page's revision (for example, `:1042`–`1047` for `a56c60d` and `bd3219f`). None of the 12 overlaps PR #677's 6, so 6 + 12 = 18.
  - **The fifth blind spot (polarity):** VERIFY V2 shows L2634/2637/2638 binding pending text and L2569 binding "No acceptance was conferred".
  - **Clone dependence:** VERIFY V4 and V5.
  - **The 510–610 projection:** quoted from §7 Q1, labelled a projection, and consistent with `opt1-pr2/VARIANTS.md` (V0 ≈513, V1 609, V2 ≈541).
- **Harvester safety of the new ledger note.** Over the 90-line block, `ACCEPT_RE`, `RETENTION_RE`, backticked-SHA and bare-SHA checks all return 0. There are 0 table rows and 0 U+2026. The 12 backticked paths sit on lines with no verdict word. K11 still runs at Stage C.
- **The backlog item follows the page's convention:** a bold title, the source with its date, a description, recorded decisions, estimates, prerequisites, and a statement that implementation needs a decision. N8 is the one gap. Its estimates match `opt1-pr2/VARIANTS.md`'s comparison row (V0 55–103 over 10 PRs; V1 21–38 plus 90–365; V2 25–45; V3 47–85). They are labelled "agent estimates from the paused planning, unmeasured and low confidence", and V3 is correctly not presented as an option shown to the owner.
- **Forward-dated only:** every new note is "appended 2026-10-07". The `:148` prefix rule (AC-3) stands.
- **Nothing presents the repair or switch as started:**
  - APR-113's Status, Scope allowed item 9 and FORBIDDEN ("It does not resume the program");
  - D73's title, item 11 and "While paused" bullet;
  - the forecast's "not selected work";
  - the open-decisions row 1 status;
  - the conversion note.

  N3 is the one stale "In progress".
- **AC-16..AC-19 and K17..K19** are mechanical (grep or command with a stated expected value) or explicitly read-checks. Fixes for K19 and AC-6: N6 and N7.

## For rev5

Apply B1–B4 with the fix texts above, and N1–N8 if cheap. Recompute the sha256. The re-audit will check those sentences and the unchanged remainder.

## Not done / limits

- No repository edit, commit, push, PR edit, comment or thread resolution. GitHub was read only (`ls-remote`, the open-PR list). One `git fetch` updated remote-tracking refs.
- K11 was not re-run on rev4's full text. The new ledger note was checked against the harvester's patterns directly, and Stage C runs K11.
- I cannot read the owner's chat. `OWNER-EVIDENCE.md` is the owner record, and §9 is the coordinator's own clarification of the options it presented.
- Reserved scope was not touched.

## Timing

- **Item:** OPT1-PR1 Stage B round 4. **ETA used:** rev4's 20–30 min (`PLAN-rev4.md:789`). This subagent had no owner channel to announce it.
- **Start:** 2026-10-07T23:39:33Z (`date -u`).
- **Finish:** see the hand-off report (taken with `date -u` after this file's sha256).
