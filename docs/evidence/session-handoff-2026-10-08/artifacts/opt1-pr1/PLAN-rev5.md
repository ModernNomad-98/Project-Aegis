# OPT1-PR1 — PLAN rev5 (a short delta against rev4)

> **REVISION MARKER: rev5.**
>
> - **Effective plan:** rev2 (`40691fe1…bc58`), then rev3 (`e3f1739f…0f44`), then rev4 (`7d4876f04683ce57a0c856dffb7ed01f61354ee3f378c6572b5e50653b26a733`), then this file. Where rev5 is silent, the earlier revisions govern. None of them is modified.
> - **Why rev5:** rev4 received **`SD-B: REVISE`** in `PLAN-AUDIT-rev4.md` (sha256 `1f74dd6ef16a709378f7d891f6e376c01acfd50839458d510bb29a5a83928e42`).
> - **What rev5 changes:** it applies blocking findings B1–B4 with the audit's exact fix wording, and nits N1–N8. **Nothing else changes.**
> - **Owner record:** `OWNER-EVIDENCE.md` is now sha256 `21a65916f2f80ea553aac7b722d9d265f033d7bc4c3656cf9a04c74a7bac8e68`. §9 was appended at 23:39:12Z, and §1–§8 are unchanged (the audit verified that the first 107 lines hash to `f6d8213b…`). §9 answers rev4's precondition P1, so P1 is satisfied.

- **Planner:** the same PLAN-stage subagent. It made no repository edit, commit, push, PR comment or thread resolution.
- **rev5 start:** 2026-10-07T23:46:54Z (`date -u`).
- **Skill used:** `scoped-approval-register`, for the wording of AEGIS-APR-113, -114 and -116 before they become immutable. No MANUAL-ONLY skill was used.

## Changes

| # | Finding | rev4 location | Old text | New text |
| --- | --- | --- | --- | --- |
| 1 | **B1** | 4.1(c), AEGIS-APR-113 item 6 | "The transcription gives no text for the first one; it was acted on, in that the questions in items 7 and 8 were asked." | "The first option's text, transcribed by the coordinator in its later clarification, reads:" + the blank line, the one-line blockquote `> I put the three questions the repair needs to you now (targeted reviews, security classification, unmeasurable changes), each explained with a recommendation.` and a blank line + "It was acted on: the three questions in item 7 were asked." The sentence that follows ("The other three option texts read, in order:") stays. |
| 2 | **B1** | 4.8(b), the open-decisions "Speed-ups" row | "They apply only if the program resumes." | "'Ask open decisions now' was acted on (the three questions recorded as AEGIS-APR-116, AEGIS-APR-118 and the counting rule); 'Raise rebuild fast path later' is an item for the 2026-10-11 check-in; the other two apply only if the program resumes." |
| 3 | **B1** | rev4 §1 table, the "Ask open decisions now" row (plan text, not repository text) | "chosen (no option text transcribed) … acted on: §6 and §7 were asked" | "chosen; option text in §9 … acted on: the three §6 questions were asked" |
| 4 | **B1** | §5, AC-5 | (the list) | Add the §9 text "I put the three questions the repair needs to you now (targeted reviews, security classification, unmeasurable changes), each explained with a recommendation.", compared against `OWNER-EVIDENCE.md` §9. |
| 5 | **B2** | 4.6, the ledger note, first bullet | "The true figure is higher, because this ledger treats a page it does not list as reviewed, and the pages have not been re-measured one by one against their last full-page review." | "The true figure may be higher: this ledger treats a page it does not list as reviewed, and the pages have not been re-measured one by one against their last full-page review." This is harvester-safe: it adds no accept-verb, no *keep … acceptance* and no SHA. |
| 6 | **B3** | 4.1(f), AEGIS-APR-113 "Relationship" | "AEGIS-APR-116 to AEGIS-APR-118 record the later answers listed in items 7 and 8, and in §1 of D73's decision." | "AEGIS-APR-116 and AEGIS-APR-118 record two of item 7's answers; AEGIS-APR-117 records the withdrawal answer, and AEGIS-APR-114 the split-PR answer, both from the question batch that included item 8's; D73's decision list summarises all of them." |
| 7 | **B4** | 4.2(c), AEGIS-APR-114 Scope FORBIDDEN | "As the split-PR answer states, it \"covers the repair PRs only\": the decision record and the switch are not split under it." | "The split-PR answer's option text says it \"covers the repair PRs only\": only the tool repair may be delivered as several pull requests; the decision record and the switch are each one pull request under this entry." |
| 8 | **B4** | §5, AC-6 | "AEGIS-APR-114's FORBIDDEN quotes \"covers the repair PRs only\"." | "AEGIS-APR-114's FORBIDDEN quotes \"covers the repair PRs only\" and states that only the tool repair may be delivered as several pull requests, the decision record and the switch each being one pull request under the entry. Its Scope allowed still covers the switch, so it is not narrowed to repair PRs." |
| 9 | **N1** | 4.5, AEGIS-APR-116 Status at recording | "Owner approved; ACTIVE only once the keeper's acceptance record table (D73 condition 2) exists on the default branch. The tool repair that adds that table is paused (AEGIS-APR-113), so until the owner resumes the program this entry covers nothing." | "Owner approved; ACTIVE only once the fixed-format table with D73 condition 2's schema, including the event-kind column, which the paused tool repair adds, exists on the default branch. This is the recorder's reading of the question's \"in the table\". It is not the keeper table already in the ledger's first ledger-keeper recording. Until the owner resumes the program, this entry covers nothing." |
| 10 | **N1** (consistency) | 4.5, AEGIS-APR-116 Scope allowed; 4.4 Decision item 9; 4.4 row 11; 4.8(b) the targeted-reviews row; §6 reply r4212737359 | "as a row of the ledger's acceptance record table" / "once the table exists" / "ACTIVE only once the keeper's table exists" | "as a row of that fixed-format table" / "once the fixed-format table exists" / "ACTIVE only once the paused repair adds the fixed-format table" (in the reply: "only once the paused tool repair adds the fixed-format table") |
| 11 | **N2** | 4.1(d), AEGIS-APR-113 Scope item 8; 4.8(c), the "Still open" row | "That check-in is the date the owner set on 2026-10-04 to revisit a proposal to cap review rounds, which the owner tabled. It is recorded in a coordinator log on the branch `coord/idle-check-2026-10-04`, not on the default branch." (and the row's equivalent sentence) | "On 2026-10-04 the owner tabled a proposal to cap review rounds and asked to check back in 7 days; the coordinator scheduled that check-in for 2026-10-11. This is recorded only in a coordinator log, `.coord/coordinator-cadence.jsonl` line 72 at commit `4d05c624`, which only the branch `coord/idle-check-2026-10-04` holds; it is not on the default branch." |
| 12 | **N3** | 4.7(b), forecast row "Decision record (this change)", Status cell | "In progress. It has needed four plan rounds, so the actual will exceed the estimate; it is measured at closeout." | "Delivered by this change; actual measured at closeout (five plan rounds suggest it may exceed the estimate)." |
| 13 | **N4** | 4.7(a), the forecast pointer note | "The note above is corrected on two points: the acceptance tool over-counts" | "The note above is corrected on one point, and one finding is added: the acceptance tool over-counts". The rest of the sentence is unchanged. |
| 14 | **N5** | D73 Consequences, "Harder" (the rev2 text, unchanged by rev3 and rev4) | "(option B was shown to the owner at \"About 16–32 agent-hours (estimate)\")" | "(option B was shown to the owner at \"About 16–32 agent-hours (estimate)\"; later variant estimates are in the backlog item)" |
| 15 | **N6** | §5, K19 | "`git ls-tree -r --name-only <base> \| grep -c '\.md$'` = 675 …" | "`git diff --name-status --diff-filter=ADR 03c93c77 <base> -- '*.md' \| wc -l` = **0** (no Markdown file added, deleted or renamed since main after PR #676). Supporting count: 675 at both refs." The planner re-measured at `7d1d05e8`: **0**. |
| 16 | **N7** | §5, AC-6 | "… 0 for 117, and for 116 only in FORBIDDEN's not-decided sentence." | "… over the Scope allowed bullets of AEGIS-APR-116 and AEGIS-APR-117: expected **0** for both." |
| 17 | **N8** | 4.8(d), the backlog bullet's "Repair options" line | "agent estimates from the paused planning, unmeasured and low confidence:" | "agent estimates from the paused planning, unmeasured and low confidence, outside the bounded selected subtotal:" |

## Notes on the changes

**Row 12 deviates from the audit's wording by one word.** The audit's N3 text says "four plan rounds", which was correct for rev4. This delta is the fifth plan revision, so the factual count is now five. The coordinator may prefer "several plan rounds", which needs no update if a further round occurs.

**Row 11's citation was verified this turn:**

- `git rev-parse origin/coord/idle-check-2026-10-04` → `4d05c62443c82db903f2ee3133b96046230cfdd4`.
- Line 72 of `.coord/coordinator-cadence.jsonl` at that commit contains "the owner said No, table it, check back in 7 days. A reminder is scheduled for 2026-10-11T16:15 America/Los_Angeles". The line was first written in `eb568329` at 2026-10-04T16:19:41-07:00.
- `git merge-base --is-ancestor 4d05c624 origin/main` exits 1, and `git for-each-ref --contains` lists only that branch. That is why the new text says only that branch holds it.

**Row 15 was verified this turn:** `git diff --name-status --diff-filter=ADR 03c93c77 7d1d05e8 -- '*.md' | wc -l` → `0`.

**Other effects of §9:**

- P1 is satisfied.
- rev4 §8 P3's `OWNER-EVIDENCE.md` citation for the PR body becomes `21a65916…8e68`, because §9 is now quoted.
- AC-5's quotation source is `OWNER-EVIDENCE.md` §1–§9.

**Unchanged:** files (six), `gate-guard` (0 matches), the security answer ("Yes — the owner approval register"), IDs (AEGIS-APR-113 to 118, D73), every other K and AC, the chain rule and the ETA.

## Timing

- **rev5 start:** 2026-10-07T23:46:54Z (`date -u`). No ETA was announced, because this subagent has no owner channel.
- **rev5 finish:** see the hand-off report, taken with `date -u` after this file's sha256.
