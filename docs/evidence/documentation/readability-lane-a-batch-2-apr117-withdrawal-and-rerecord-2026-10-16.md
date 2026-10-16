# AEGIS-APR-117 withdrawal and re-record — Phase 4 re-read lane A, batch 2, 2026-10-16

Recorded by **DeepSeek-4.1-Flash (deepseek-flash)**, keeper identity
`deepseek-flash-apr117-keeper`, an agent that ran none of the eight reads, wrote none of the
eight pages, and holds no other stage of this pull request (PR) #777. This is a Stage C repair
round answering the Stage D verdict `SD-D: REVISE` posted on PR #777 at head
`05ad76072d12070164aaf9135223e49e28a296ae`.

## Why these rows exist

AEGIS-APR-101 (the register entry defining the ledger-keeper role) requires the keeper to be a
**different agent** from the page's author and accepting reviewer. Lane A's second batch recorded
its eight rows (K-090…K-097) with **one agent both reading the pages and writing the keeper
rows** — `readability-lane-a-implementer-c` — and declared that deviation in its batch record.
**Owner decision 3 of 2026-10-15 declined to ratify the carry** (the K-074..K-081
carry-with-deviation precedent is not extended) and directed the **AEGIS-APR-117 route** instead:
append withdrawal rows that cancel the same-agent rows, then append fresh keeper rows for the same
pages **from the same evidence**, recorded by a different, eligible keeper. **No page is re-read;
the reads stand; only the recording authority changes.** All eight pages carry no partial verdict,
so all eight end in a fresh full-page-acceptance row. The ledger is never rewritten: the withdrawn
rows (K-090…K-097), the withdrawal rows (K-090W…K-097W) and the fresh rows (K-106…K-113) all
remain physically present in the consolidated keeper table.

## Binding method

- **Acceptance revision:** every row binds the lane's reviewed head
  `e2a3e20b7c20ef8385b219b39c6405237163406f` (the same revision the withdrawn rows bind; the
  read is not repeated).
- **Blob IDs, recomputed this round, never transcribed:** every fresh and withdrawal row's
  `Blob ID` equals `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:<page>`. All eight
  were re-resolved this round and **all eight match the withdrawn rows' cells**.
- **Original quotes:** each block's *Original quote* line is transcribed verbatim from the lane
  batch record `docs/evidence/documentation/readability-lane-a-batch-2-2026-10-15.md` (the
  evidence source of the withdrawn rows). The fresh rows cite **this** file as their evidence
  source, and each transcribed quote is bound here byte-for-byte, so the build-time quote check
  (`build_index.py`) finds both the quote and the revision at the built ref.
- **Withdrawal quotes:** each *Withdrawal row quote* line below is the row's own quote; the
  `WD-A2-<n>` prefix names the withdrawal and the row it cancels, so the cancellation stays
  robust to any later renumbering of the stable ids.
- **Build check:** `python -B tools/readability_acceptance/build_index.py --report --ref <the
  repair head>` exits 0 with the row arithmetic stated in the batch record section 8
  (109 + 8 withdrawals + 8 fresh = 125 rows; full-page acceptances 89 + 8 = 97).

## Stable-id choice — audited against every open pull request

The fresh rows take the contiguous block **K-106…K-113** in lane A's allocated band
(K-082–K-180, per the published allocation page `docs/roadmaps/KEEPER-ID-ALLOCATION-2026-10-15.md`;
the bare filename `KEEPER-ID-ALLOCATION.md` resolves to no repository path). The choice follows
the standing rule — **new keeper ids must be checked against every OPEN pull request, not just
`main`, and new batches take ids above the highest id any open pull request claims**:

- **Highest id claimed in lane A's band:** `main` holds K-098…K-104 (the merged PR #781 fresh
  rows); this pull request holds K-090…K-097; open PR #771 holds K-082…K-089. The highest is
  **K-104**, so K-106…K-113 is above every claimed id.
- **K-105 is skipped deliberately, not by arithmetic:** the merged PR #781 record and the
  published allocation page record K-105 as **withheld and never authored** under the PARTIAL rule
  (it is the fresh id lane A's P8 would have used; that page carries a partial verdict and gets no
  fresh row). No rule requires the lowest free id when a recorded withholding exists, and the band
  has ample room.
- **Absence measured, not assumed:** the ids K-106…K-113 and K-090W…K-097W occur in **no** table
  row at `main` `50241ba5036e36ec9bcd1ce7a4b93ffa23a0392b` and in **none** of the 19 open
  pull-request heads measured this round (#771, #772, #773, #774, #775, #776, #777, #778, #779,
  #780, #782, #784, #785, #787, #788, #789, #790, #791, #792, #793, #794, #796, #797 — the open set
  at measurement). The audit command and its output are in the batch record section 8.

## The eight pages (one block per withdrawn row; all eight end in a fresh acceptance row)

### WD-A2-1 — lane A batch 2, withdrawn row K-090, fresh row K-106

- Page: .claude/skills/ab-test-designer/SKILL.md
- Original keeper (accepting reviewer agent): readability-lane-a-implementer-c
- Acceptance revision (the reviewed head; the read is not repeated): e2a3e20b7c20ef8385b219b39c6405237163406f
- Blob ID, recomputed this round with `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:.claude/skills/ab-test-designer/SKILL.md` (never transcribed): 775b774fde08e5d7ac1df462bef78de148b07a8a
- Original quote, transcribed verbatim from the lane batch record docs/evidence/documentation/readability-lane-a-batch-2-2026-10-15.md: P1 accepted: .claude/skills/ab-test-designer/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Withdrawal row quote (AEGIS-APR-117): WD-A2-1 withdraws K-090 (readability-lane-a-implementer-c): P1 accepted: .claude/skills/ab-test-designer/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Fresh row: K-106, event kind full-page-acceptance, same page, same revision, same blob, recorded by deepseek-flash-apr117-keeper

### WD-A2-2 — lane A batch 2, withdrawn row K-091, fresh row K-107

- Page: .claude/skills/ab-test-designer/references/ab-test-sheet.md
- Original keeper (accepting reviewer agent): readability-lane-a-implementer-c
- Acceptance revision (the reviewed head; the read is not repeated): e2a3e20b7c20ef8385b219b39c6405237163406f
- Blob ID, recomputed this round with `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:.claude/skills/ab-test-designer/references/ab-test-sheet.md` (never transcribed): 28e206977eacb05084844fcbc7d5aff7f90f1ed1
- Original quote, transcribed verbatim from the lane batch record docs/evidence/documentation/readability-lane-a-batch-2-2026-10-15.md: P2 accepted: .claude/skills/ab-test-designer/references/ab-test-sheet.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Withdrawal row quote (AEGIS-APR-117): WD-A2-2 withdraws K-091 (readability-lane-a-implementer-c): P2 accepted: .claude/skills/ab-test-designer/references/ab-test-sheet.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Fresh row: K-107, event kind full-page-acceptance, same page, same revision, same blob, recorded by deepseek-flash-apr117-keeper

### WD-A2-3 — lane A batch 2, withdrawn row K-092, fresh row K-108

- Page: .claude/skills/acceptance-criteria-reviewer/SKILL.md
- Original keeper (accepting reviewer agent): readability-lane-a-implementer-c
- Acceptance revision (the reviewed head; the read is not repeated): e2a3e20b7c20ef8385b219b39c6405237163406f
- Blob ID, recomputed this round with `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:.claude/skills/acceptance-criteria-reviewer/SKILL.md` (never transcribed): 56899580a8a30b194a1ba5cf63ab810984426604
- Original quote, transcribed verbatim from the lane batch record docs/evidence/documentation/readability-lane-a-batch-2-2026-10-15.md: P3 accepted: .claude/skills/acceptance-criteria-reviewer/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Withdrawal row quote (AEGIS-APR-117): WD-A2-3 withdraws K-092 (readability-lane-a-implementer-c): P3 accepted: .claude/skills/acceptance-criteria-reviewer/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Fresh row: K-108, event kind full-page-acceptance, same page, same revision, same blob, recorded by deepseek-flash-apr117-keeper

### WD-A2-4 — lane A batch 2, withdrawn row K-093, fresh row K-109

- Page: .claude/skills/acceptance-criteria-reviewer/references/criteria-review-sheet.md
- Original keeper (accepting reviewer agent): readability-lane-a-implementer-c
- Acceptance revision (the reviewed head; the read is not repeated): e2a3e20b7c20ef8385b219b39c6405237163406f
- Blob ID, recomputed this round with `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:.claude/skills/acceptance-criteria-reviewer/references/criteria-review-sheet.md` (never transcribed): bf44030a2928081b1720396233d3208938d9e85c
- Original quote, transcribed verbatim from the lane batch record docs/evidence/documentation/readability-lane-a-batch-2-2026-10-15.md: P4 accepted: .claude/skills/acceptance-criteria-reviewer/references/criteria-review-sheet.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Withdrawal row quote (AEGIS-APR-117): WD-A2-4 withdraws K-093 (readability-lane-a-implementer-c): P4 accepted: .claude/skills/acceptance-criteria-reviewer/references/criteria-review-sheet.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Fresh row: K-109, event kind full-page-acceptance, same page, same revision, same blob, recorded by deepseek-flash-apr117-keeper

### WD-A2-5 — lane A batch 2, withdrawn row K-094, fresh row K-110

- Page: .claude/skills/accessibility-test-harness/SKILL.md
- Original keeper (accepting reviewer agent): readability-lane-a-implementer-c
- Acceptance revision (the reviewed head; the read is not repeated): e2a3e20b7c20ef8385b219b39c6405237163406f
- Blob ID, recomputed this round with `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:.claude/skills/accessibility-test-harness/SKILL.md` (never transcribed): 61a36e4f3acbc2aa25bf743a804add2e32492786
- Original quote, transcribed verbatim from the lane batch record docs/evidence/documentation/readability-lane-a-batch-2-2026-10-15.md: P5 accepted: .claude/skills/accessibility-test-harness/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Withdrawal row quote (AEGIS-APR-117): WD-A2-5 withdraws K-094 (readability-lane-a-implementer-c): P5 accepted: .claude/skills/accessibility-test-harness/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Fresh row: K-110, event kind full-page-acceptance, same page, same revision, same blob, recorded by deepseek-flash-apr117-keeper

### WD-A2-6 — lane A batch 2, withdrawn row K-095, fresh row K-111

- Page: .claude/skills/accessibility-test-harness/references/a11y-checklists.md
- Original keeper (accepting reviewer agent): readability-lane-a-implementer-c
- Acceptance revision (the reviewed head; the read is not repeated): e2a3e20b7c20ef8385b219b39c6405237163406f
- Blob ID, recomputed this round with `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:.claude/skills/accessibility-test-harness/references/a11y-checklists.md` (never transcribed): 0be76bc052efba600c5f7296aa1d0f8421fb725f
- Original quote, transcribed verbatim from the lane batch record docs/evidence/documentation/readability-lane-a-batch-2-2026-10-15.md: P6 accepted: .claude/skills/accessibility-test-harness/references/a11y-checklists.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Withdrawal row quote (AEGIS-APR-117): WD-A2-6 withdraws K-095 (readability-lane-a-implementer-c): P6 accepted: .claude/skills/accessibility-test-harness/references/a11y-checklists.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Fresh row: K-111, event kind full-page-acceptance, same page, same revision, same blob, recorded by deepseek-flash-apr117-keeper

### WD-A2-7 — lane A batch 2, withdrawn row K-096, fresh row K-112

- Page: .claude/skills/admin-console-architect/SKILL.md
- Original keeper (accepting reviewer agent): readability-lane-a-implementer-c
- Acceptance revision (the reviewed head; the read is not repeated): e2a3e20b7c20ef8385b219b39c6405237163406f
- Blob ID, recomputed this round with `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:.claude/skills/admin-console-architect/SKILL.md` (never transcribed): d9500b3bde91301cef76dc76ac659712d4e93e91
- Original quote, transcribed verbatim from the lane batch record docs/evidence/documentation/readability-lane-a-batch-2-2026-10-15.md: P7 accepted: .claude/skills/admin-console-architect/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Withdrawal row quote (AEGIS-APR-117): WD-A2-7 withdraws K-096 (readability-lane-a-implementer-c): P7 accepted: .claude/skills/admin-console-architect/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Fresh row: K-112, event kind full-page-acceptance, same page, same revision, same blob, recorded by deepseek-flash-apr117-keeper

### WD-A2-8 — lane A batch 2, withdrawn row K-097, fresh row K-113

- Page: .claude/skills/adr-sequencer/references/adr-corpus-sheet.md
- Original keeper (accepting reviewer agent): readability-lane-a-implementer-c
- Acceptance revision (the reviewed head; the read is not repeated): e2a3e20b7c20ef8385b219b39c6405237163406f
- Blob ID, recomputed this round with `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:.claude/skills/adr-sequencer/references/adr-corpus-sheet.md` (never transcribed): 84ed16cabe2e7390ea95825c173382900ee4430e
- Original quote, transcribed verbatim from the lane batch record docs/evidence/documentation/readability-lane-a-batch-2-2026-10-15.md: P8 accepted: .claude/skills/adr-sequencer/references/adr-corpus-sheet.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Withdrawal row quote (AEGIS-APR-117): WD-A2-8 withdraws K-097 (readability-lane-a-implementer-c): P8 accepted: .claude/skills/adr-sequencer/references/adr-corpus-sheet.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Fresh row: K-113, event kind full-page-acceptance, same page, same revision, same blob, recorded by deepseek-flash-apr117-keeper

## The C-1 measurement the re-record rests on

The keeper does not confer acceptance and does not re-read; before re-recording it re-measured the
two terms the round-1 record called "partial", on the pages themselves at the bound revision and
across the reader-page library. The full per-term analysis is in the batch record section 8; the
measurements are:

| Term | Occurrences on the page at `e2a3e20b…` | How the page (or its own linked companion) resolves it |
| --- | --- | --- |
| `p<0.05` (P1) | 1 (L178) | P1's own L176-177 ("the false-positive rate climbs far past 5%") and its own linked companion `references/ab-test-sheet.md` L13 ("**Significance level (α):** typically 0.05"). |
| `p-hacking` (P1) | 1 (L183) | Defined by apposition on the page: "Slicing until something is significant is p-hacking with extra steps." |
| `Overall Evaluation Criterion` (P1) | 1 (L82) | Glossed in apposition: "One metric decides the test (an Overall Evaluation Criterion)"; it is not an abbreviation or coded identifier. |
| `authz` (P7) | **2 (L143, L160)**, both inside the one Output Format block | P7 spells "authorization" **20 times**, including L25 ("that ENFORCES the authorization policy") which L143 mirrors as "enforces the authz policy", and names `authorization-matrix-designer` at L146/L160. |

**Prevalence under C-1 (measured 2026-10-16 at `origin/main`
`50241ba5036e36ec9bcd1ce7a4b93ffa23a0392b`):** 658 reader pages; **54** use `authz`; **47 of
those 54** also spell the word out; **7** use it without a spelled-out form anywhere (P7 is not
one of the seven); 125 occurrences in total. The C-1 convention threshold in use is about 12+
pages, so a short form is a library-wide convention and not a per-page defect — and P7 resolves
its own term in any case. At the Stage D auditor's own `origin/main` the same measurement read
657 / 53 / 46 / 7 / 119; main has moved by one page since, which changes no conclusion.

## Codex at the audited head — CONFIRMED UNAVAILABILITY, not clean

- **The state block binds THIS head:** `codex-review-state:v1
  {"code_review":{"commit_sha":"05ad76072d12070164aaf9135223e49e28a296ae","has_any_findings":true,"has_unresolved_findings":true,"status":"failed"},...}`
  — `05ad76072d12070164aaf9135223e49e28a296ae`, not a superseded one.
- **The cause is the bot's own next comment**, posted two seconds later at
  `2026-10-15T19:03:46Z`: "You have reached your Codex usage limits for code reviews."
- **This round's own counts at 2026-10-16:** `GET /pulls/777/reviews` = **0 reviews**;
  `GET /pulls/777/comments` = **0 review comments**; `GET /issues/777/comments` = **6 issue
  comments**, of which **2** are from `chatgpt-codex-connector[bot]`. There is no review body and
  no inline finding anywhere on this pull request, so **no substantive finding content exists to
  triage** — and **0 reviews is not "clean"**: it is **CONFIRMED UNAVAILABILITY**. A P1 is never
  left untriaged; here there is no P1, but the merge holder records the unavailability or re-runs
  Codex before merge.

## What this repair round did not verify

- Whether the eight pages were truly read "whole, line by line, as prose" — the round-1 reader's
  process claim is not checkable from the repository. This round verified the pages' bytes, the
  conservative re-measurement above, and the row bindings, not the act of reading.
- Whether a fresh Stage F is owed: it is **not verified here** — this round is a repair (a new
  commit, a moved head and an edited bound field in the PR body), so the head being merged will not
  be `05ad76072d12070164aaf9135223e49e28a296ae` and the verdicts that named it do not cover the
  repaired head. Re-audit at the new head is owed.
- This file itself: it is a new reader page with no keeper row, so it counts pending, like every
  other evidence record before it.
