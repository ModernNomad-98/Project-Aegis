# OPT1-PR1 — PLAN rev7 (a short delta against rev6)

> **REVISION MARKER: rev7.**
>
> - **Effective plan:** rev2, then rev3, then rev4, then rev5, then rev6 (`27f541544e7e386b1fc2f0a8443d51bea009a08538355330fafeafe2ff112bd3`), then this file. Where rev7 is silent, the earlier revisions govern. None of them is modified.
> - **Why rev7:** rev6 received **`SD-B: REVISE`** in `PLAN-AUDIT-rev6.md` (sha256 `67915f71fcc8fc6c44b4dbedbf4784ff575ec1d53d1c0e50836ddbe288ae4dc7`). Blocking findings B1–B3 all sit in rev6's withdrawal and event mechanics in D73 row 2.
> - **Coordinator decision applied:** this PR records a **paused** program, so D73 row 2 states **requirements, not mechanics**. The exact schema, field list, validity rules and rejection list belong to the tool-repair plan and its independent plan audit, if the owner resumes.
> - **Live state, at 00:33Z:** `origin/main` = `7d1d05e8…`; `refs/pull/678/head` = `dbb4cd67…`; local tree clean. `OWNER-EVIDENCE.md` is unchanged (`21a65916…8e68`).

- **Planner:** the same PLAN-stage subagent. It made no repository edit, commit, push, PR comment or thread resolution.
- **rev7 start:** 2026-10-08T00:33:07Z (`date -u`).
- **Skills used:**
  - `scoped-approval-register`: the AEGIS-APR-117 reading is labelled as this record's reading, not as the owner's words; the AEGIS-APR-113 pointer.
  - `source-of-truth-reconciler`: rows 2, 4, 8 and 11 made consistent with each other.

  No MANUAL-ONLY skill was used.

## 1. What rev7 replaces in rev6

- **Superseded:** rev6 changes **3, 4, 5 and 6**, the detailed field lists, withdrawal mechanics and rejection rules for D73 row 2. Change 1 of §2 replaces all four with one requirements-level row.
- **Kept from rev6:**
  - change 1 (APR-113 pointer), with the audit's N1 applied;
  - change 2 (APR-115 full preamble sentence), with N6 applied;
  - change 7 (H1, row 3);
  - change 8 (the pinned rebuild ref), with N3 applied;
  - change 9 (H4, row 11), restated at requirements level;
  - changes 10 and 11 (backlog prerequisites; "What it is");
  - change 12 (H5), with N4 applied;
  - changes 13 and 14 (conversion note; M-1);
  - change 15 (N-4), with N7 applied;
  - changes 16 and 17 (the skills table; the self-cost recount);
  - K20.

**How the rev6-audit findings resolve:**

| Finding | Resolution |
| --- | --- |
| **B1** (withdrawal targets) | Resolved at requirements level. A withdrawal "identifies the specific earlier acceptance event of the same page that it cancels, and cannot cancel a later valid event". Whether a targeted-review row is an "acceptance row" that may be withdrawn under AEGIS-APR-117 is marked **Open**, following the audit's own option. The detailed rejection list is deferred. |
| **B2** ("affected page") | Applied: "as this record reads AEGIS-APR-117's 'The affected page becomes pending again.'". The mechanics sentence that B2 also corrected (re-recording under AEGIS-APR-101 or -116) is removed as mechanics, so that part has nothing left to apply to. |
| **B3** (opening sentence against listed fields) | Resolved. Row 2 now says the table "adds at least a blob ID, an event kind and a stable identifier for every event". There is no separate field list left to contradict it. |
| **N1** | Applied, in change 2 below. |
| **N2** | Applied: row 4 says "not written as an acceptance". |
| **N3** | Applied in row 8. |
| **N4** | Applied in backlog change 12. |
| **N5** | Applied in AC-6. |
| **N6** | Applied in AC-6 and in change 3 below. |
| **N7** | Applied in change 15. |

## 2. Exact text changes (to this PR's own added lines at `dbb4cd67`)

| # | Finding | Location at `dbb4cd67` | Old | New |
| --- | --- | --- | --- | --- |
| 1 | Coordinator; B1–B3 | D73 row 2 (`step-0…:3815`), the whole row. This replaces rev6 changes 3–6. | (the head row) | See the exact row text below this table. |
| 2 | r4213371781 + N1 | Register, AEGIS-APR-113 Event (`:4562-4564`) | "The owner's work and merge authority for this program are AEGIS-APR-114 and AEGIS-APR-115." | "The owner's grants for this program are two delivery grants and two keeper-role grants: AEGIS-APR-114, the program's pull requests; AEGIS-APR-115, routine rebuild pull requests after a switch; AEGIS-APR-116, targeted-review rows; and AEGIS-APR-117, withdrawal rows. None of them covers any work while the program is paused (Status below)." This replaces rev6 change 1. |
| 3 | N-1 + N6 | Register, AEGIS-APR-115 Scope allowed (`:4932-4933`) | "\"An action is covered only by an effectively ACTIVE human grant whose scope includes it.\"" | The full sentence, **kept on one line** under rev2 §7's one-line convention: `"An action is covered only by an effectively ACTIVE human grant whose scope includes it, after considering the full history and any actual limits."` This is rev6 change 2 with N6. |
| 4 | N2 | D73 row 4 | "A row that cannot be verified is not written, so its page counts as pending." | "A row that cannot be verified is not written as an acceptance, so its page counts as pending." |
| 5 | r4213371774 + N3 | D73 row 8 | (rev6 change 8's text) | rev6 change 8's text, with this sentence appended after "The reviewer rebuilds at that same ref and requires a zero diff.": "If the default branch has moved by merge time, the rebuild is redone at the new tip." |
| 6 | H4, restated at requirements level | D73 row 11, "carrying the reviewed revision, its blob ID, the retained full-page acceptance revision, the reviewer and the evidence pointer." | (that phrase) | "that identifies the reviewed revision and the retained full-page acceptance it builds on, by its identifier (exact fields: row 2). A targeted review covers the change from the retained acceptance up to its reviewed revision; a later change needs its own review, as the rule says of any unreviewed edit." This replaces rev6 change 9. |
| 7 | H5 + N4 | Open-decisions backlog bullet, the V2 clause | "It would narrow option B's backfill, so it needs the owner's confirmation;" | "It would narrow option B's backfill and partly change "Parallel repair PRs" (4 pull requests instead of 10), so it needs the owner's confirmation; V1 would drop that backfill and V3 would reverse "Parallel repair PRs", so each of them would need the owner's decision too;" This replaces rev6 change 12. |
| 8 | N-4 + N7 | Ledger note, second bullet | "out of 602 indexed pages." | "out of 602 indexed pages (the index lists no page added after it was built, which is 7 of the 609 reader pages on main after PR #677)." This replaces rev6 change 15 and is harvester-safe. |

**Change 1, the exact D73 row 2.** It is one table line in the file; it is wrapped here for reading. The lettered items run inline, separated by semicolons.

```markdown
    | 2 | The index reads only the keeper's table. This record states requirements for that table. The exact schema, field list, validity rules and rejection list are defined by the tool-repair plan and its independent plan audit, if the owner resumes the program. (a) The table keeps the existing keeper table's columns (Page, Acceptance revision, Reviewer, Evidence source, Date, in the first ledger-keeper recording) and adds at least a blob ID, an event kind and a stable identifier for every event. The event kinds include at least a full-page acceptance, a targeted review (AEGIS-APR-116) and a withdrawal (AEGIS-APR-117). (b) Every row carries an evidence pointer to the posted record it rests on: for a backfilled row, the ledger or evidence-record location and revision whose text the row quotes (row 4); for a withdrawal, the evidence that the cancelled event was wrong. The build runs offline, so the recording pull request's independent review checks that the pointer leads to a qualifying record bound to the recorded revision; AEGIS-APR-101 binds each recording "to the exact reviewed revision and its posted evidence". A pull-request comment can still be edited or deleted on GitHub; that residual is recorded, not solved. (c) A withdrawal identifies the specific earlier acceptance event of the same page that it cancels, and cannot cancel a later valid event. A page becomes pending again only when its status rested on the cancelled event, as this record reads AEGIS-APR-117's "The affected page becomes pending again." Whether a targeted-review row may be withdrawn as an "acceptance row" under AEGIS-APR-117 is Open. (d) A lost commit is recorded without binding it, in the backfill's reviewed report or as an event of its own kind, and never counts as an acceptance (rows 5 and 8). (e) The build rejects loudly, and does not count, any malformed or unverifiable row. (f) The index never reads the "Candidates examined and NOT recorded" table, `../` links resolve relative to the ledger, and `stated-acceptances.json` stops being an input. | Owner ("the index reads only that table"; AEGIS-APR-116; AEGIS-APR-117, as this record reads it); Existing rule (AEGIS-APR-101's evidence binding); Audit (the requirements); Open (withdrawing a targeted-review row) |
```

**Unchanged by rev7**, applied as rev6 states:

- change 7: row 3;
- change 8: row 8's pin, now with change 5's sentence appended;
- changes 10 and 11: the backlog bullet;
- change 13: the conversion note;
- change 14: M-1;
- change 16: N-3, the skills table;
- change 17: the self-cost recount.

## 3. Changes to checks and acceptance criteria

| Item | Change from rev6 §4 |
| --- | --- |
| **AC-6** (N1, N5, N6) | AEGIS-APR-113's Event names AEGIS-APR-114 to AEGIS-APR-117 with "two delivery grants and two keeper-role grants", and describes AEGIS-APR-115 as "routine rebuild pull requests after a switch". **N5:** rev2's `blob\|40-character\|tagg\|verifiable` grep runs over AEGIS-APR-113's **Scope allowed bullet** (expected 0), not the whole block; the whole block contains the verbatim label "V2: verifiable only (Recommended)". **N6:** AEGIS-APR-115's full preamble sentence sits on **one line**, so `grep -F 'whose scope includes it, after considering the full history and any actual limits.'` over the AEGIS-APR-115 block = 1. |
| **AC-14** (replaces rev6's row-2 items) | D73 row 2 contains:<br>• "defined by the tool-repair plan and its independent plan audit";<br>• "adds at least a blob ID, an event kind and a stable identifier for every event";<br>• "cannot cancel a later valid event";<br>• "as this record reads AEGIS-APR-117";<br>• "recorded without binding it";<br>• "rejects loudly".<br>Row 2 contains no per-kind field list and no enumerated rejection rules: by reading, and `grep -c 'whose withdrawal names'` over D73 = 0.<br>Row 4 contains "not written as an acceptance". Row 8 contains "never to the rebuild's own commit", "source_revision", "redone at the new tip" and B1's (rev3 audit) sentence verbatim. Row 11 contains "by its identifier (exact fields: row 2)". |
| AC-9, AC-18, AC-19, K4, K10, K11, K20 | As rev6 §4. AC-18 also checks "on main after PR #677" in the 602/609 clause. AC-19 also checks the V2 clause names "Parallel repair PRs". |

The chain rule is as in rev6: a new head, with Stages C–F re-run.

## 4. Codex replies (post after the fix head; do not resolve the threads)

- **r4213371765** (replaces rev6's text):
  > Adopted as a requirement in `<HEAD>`. D73 condition 2 now requires a stable identifier for every event, and requires that a withdrawal identify the specific earlier acceptance event of the same page that it cancels and cannot cancel a later valid event. A page becomes pending again only when its status rested on the cancelled event, as the record reads AEGIS-APR-117's "The affected page becomes pending again." The exact mechanics (schema, field list, validity rules and rejection list) are deferred to the tool-repair plan and its independent plan audit, because the program is paused (AEGIS-APR-113) and that plan only runs if the owner resumes it. Whether a targeted-review row may itself be withdrawn under AEGIS-APR-117 is left open.
- **r4213371781** (replaces rev6's text, with N1):
  > Adopted in `<HEAD>`. AEGIS-APR-113's Event line now names all four grants as two delivery grants and two keeper-role grants: AEGIS-APR-114, the program's pull requests; AEGIS-APR-115, routine rebuild pull requests after a switch; AEGIS-APR-116, targeted-review rows; and AEGIS-APR-117, withdrawal rows. It also says none of them covers any work while the program is paused, which matches the Status paragraph.
- **r4213371774** (rev6's text, plus N3):
  > Adopted in `<HEAD>`. Verified against `build_index.py`: `--ref` defaults to `HEAD`, and the resolved ref is written as `source_revision` into both generated files. D73 condition 8 now pins the build's `--ref` to the rebuild pull request's base commit on the default branch, named in the PR and never the rebuild's own commit, and the reviewer rebuilds at that same ref for the zero-diff check. If the default branch has moved by merge time, the rebuild is redone at the new tip. A repaired format without the self-reference remains acceptable if the tool-repair plan chooses it.
- **r4213371788** and **r4213371797:** rev6's texts, unchanged.

## Timing

- **rev7 start:** 2026-10-08T00:33:07Z (`date -u`). No ETA was announced, because this subagent has no owner channel.
- **rev7 finish:** see the hand-off report, taken with `date -u` after this file's sha256.
