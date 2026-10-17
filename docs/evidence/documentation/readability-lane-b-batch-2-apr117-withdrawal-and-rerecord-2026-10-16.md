# AEGIS-APR-117 withdrawal and re-record - Phase 4 re-read lane B, batch 2, 2026-10-16

Recorded by **DeepSeek-4.1-Flash (deepseek-flash)**, keeper identity
`deepseek-flash-apr117-keeper`, an agent that read none of the eight pages, wrote none of them, and
accepted none of them. The eight rows this act cancels were recorded by
`readability-lane-b-implementer-c`, the agent that also read the pages, so this keeper is a different agent
from each page's reader and from the accepting reviewer named in the cancelled rows -
the independence AEGIS-APR-101 requires.

## Why these rows exist

`readability-lane-b-implementer-c` recorded the eight lane-B batch-2 rows **K-197..K-204** - the same agent
that performed the reads in the batch record `docs/evidence/documentation/readability-lane-b-batch-2-2026-10-15.md`. AEGIS-APR-101 requires
the ledger keeper to be a **different agent** from the page's author and accepting
reviewer, and AEGIS-APR-101's Scope FORBIDDEN begins "No self-review". The remedy has
already been applied twice on this ledger - to lane A batch 2 (K-106..K-113 withdrawn as
K-106W..K-113W, re-recorded as K-114..K-121) and to lane D batch 2 (K-381..K-388
withdrawn as K-389W..K-397W, re-recorded as K-397..K-404) - and not to these eight.

AEGIS-APR-117 (withdrawal) is **WITHDRAWAL-ONLY**: a keeper may append a withdrawal row
cancelling a wrong row, bound to evidence, under normal review, and it **grants NO
re-record power - the recording act below belongs to AEGIS-APR-101**, whose scope lets
the keeper record an existing qualifying review decision bound to the exact reviewed
revision and its posted evidence while conferring no acceptance of its own. No page is
re-read and no acceptance is conferred: the reads stand, the bound revision is
unchanged, and only the recording authority changes.

The ledger is never rewritten. The withdrawn rows (K-197..K-204), the withdrawal rows
(K-197W..K-204W) and the fresh rows (K-205..K-212) all remain physically present in the
consolidated keeper table.

## The measured gap this act closes

- The eight superseded rows are **K-197..K-204**, all event kind
  `full-page-acceptance`, all 0 changed lines against `e2a3e20b7c20`, all sourced from
  `docs/evidence/documentation/readability-lane-b-batch-2-2026-10-15.md`.
- Their Reviewer cell is `readability-lane-b-implementer-c` - the same agent that read the pages.
- Their Acceptance revision is `e2a3e20b7c20ef8385b219b39c6405237163406f`.

## Stable-id derivation (by measurement, not by assumption)

Lane B's keeper band is **K-181..K-280**. Every id in that band was swept across **every
ref this clone can see** - 1574 refs in total: 798 `refs/pull/*/head` refs, 775
`refs/remotes/**` refs and `refs/heads/main`, fetched with the literal refspec
`+refs/pull/*/head:refs/pull/*/head`. Of those refs, 1373 carry `docs/roadmaps/aegis-documentation-readability-backlog.md`; 150 distinct
blobs of that file exist across the refs, and 19 of them carry a keeper table.

- **Highest existing id in the band, anywhere:** `K-204` (present at `main`). Inside
  the band, `main` holds K-181W..K-188W, K-189..K-196 and K-197..K-204, and
  `refs/pull/772/head` together with
  `refs/remotes/origin/docs/readability-lane-b-batch-1-20261015` additionally hold
  K-181..K-188. No ref holds any band id above K-204.
- **Withdrawal identifiers:** `K-197W..K-204W` - the band positions the withdrawn rows
  occupy, mirrored with a W suffix, which is this ledger's recorded rule for withdrawal
  ids (they mirror those positions with a W suffix, because a withdrawal must sort after
  the row it cancels and before the fresh row that replaces it).
- **Fresh identifiers:** `K-205..K-212` - the first free contiguous eight above every id
  claimed in the band at `main` or by any other ref.
- **Skipped candidates: NONE.** All sixteen identifiers were checked against every ref and
  are absent from all of them, so this withdrawal block is contiguous. The non-contiguous
  precedent was lane D batch 2, which had to skip `K-392W` because the already-merged
  row `K-392W` held it.

## Ordering property carried by the identifiers

The builder `build_index.py` selects a page's latest event by **string comparison of
the stable identifier** (`derive_reader_pages` replaces the current event only when the
candidate's stable_id is strictly greater as a string). Table order is irrelevant. For
every one of the eight pages the three identifiers order `withdrawn < withdrawal < fresh`
lexically:

| # | Page | Withdrawn | Withdrawal | Fresh | Lexical order |
| --- | --- | --- | --- | --- | --- |
| 1 | `.claude/skills/frontend-perf-engineer/references/frontend-metric-budget-sheet.md` | `K-197` | `K-197W` | `K-205` | `K-197 < K-197W < K-205` |
| 2 | `.claude/skills/full-codebase-auditor/SKILL.md` | `K-198` | `K-198W` | `K-206` | `K-198 < K-198W < K-206` |
| 3 | `.claude/skills/full-codebase-auditor/references/audit-inventory-checklist.md` | `K-199` | `K-199W` | `K-207` | `K-199 < K-199W < K-207` |
| 4 | `.claude/skills/funnel-definition-designer/SKILL.md` | `K-200` | `K-200W` | `K-208` | `K-200 < K-200W < K-208` |
| 5 | `.claude/skills/funnel-definition-designer/references/funnel-sheet.md` | `K-201` | `K-201W` | `K-209` | `K-201 < K-201W < K-209` |
| 6 | `.claude/skills/gated-deployment-prompt-template/SKILL.md` | `K-202` | `K-202W` | `K-210` | `K-202 < K-202W < K-210` |
| 7 | `.claude/skills/gated-deployment-prompt-template/references/deployment-prompt-template.md` | `K-203` | `K-203W` | `K-211` | `K-203 < K-203W < K-211` |
| 8 | `.claude/skills/hidden-context-exposure-reviewer/SKILL.md` | `K-204` | `K-204W` | `K-212` | `K-204 < K-204W < K-212` |

## Binding method

- **Acceptance revision:** every row binds the lane's reviewed head `e2a3e20b7c20ef8385b219b39c6405237163406f` - the same
  revision the withdrawn rows bind. The read is not repeated.
- **Blob IDs, recomputed this round, never transcribed:** every fresh and withdrawal row's
  `Blob ID` equals `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:<page>`. All eight were re-resolved this round
  and all eight match the withdrawn rows' cells.
- **Original quotes:** each *Original quote* line below is transcribed verbatim from the
  lane batch record `docs/evidence/documentation/readability-lane-b-batch-2-2026-10-15.md`, the evidence source of the withdrawn rows. The fresh
  rows cite **this** file as their evidence source, and every quote is bound here
  byte-for-byte, so the build-time checks in `build_index.py` - quote present verbatim,
  revision named, evidence source readable - hold at the built ref.
- **Withdrawal quotes:** each *Withdrawal row quote* line below is that row's own quote;
  the `WD-B2-<n>` prefix names the withdrawal and the row it cancels, so the
  cancellation stays robust to any later renumbering of the stable ids.
- **Authority:** AEGIS-APR-101 (the keeper role and its independence limits) for the
  recording, AEGIS-APR-117 (withdrawal-only) for the cancellations, and AEGIS-APR-100 with
  AEGIS-APR-039 for the commit, the branch push and the pull request.

## The eight pages (one block per withdrawn row; all eight end in a fresh acceptance row)

### WD-B2-1 - lane B batch 2, withdrawn row K-197, withdrawal row K-197W, fresh row K-205

- Page: .claude/skills/frontend-perf-engineer/references/frontend-metric-budget-sheet.md
- Original keeper (accepting reviewer agent): readability-lane-b-implementer-c
- Acceptance revision (the reviewed head; the read is not repeated): e2a3e20b7c20ef8385b219b39c6405237163406f
- Blob ID, recomputed this round with `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:.claude/skills/frontend-perf-engineer/references/frontend-metric-budget-sheet.md` (never transcribed): c6c8dd593de4c0ab48ae991166ee427101562502
- Original quote, transcribed verbatim from the lane batch record docs/evidence/documentation/readability-lane-b-batch-2-2026-10-15.md: B2-1 accepted: .claude/skills/frontend-perf-engineer/references/frontend-metric-budget-sheet.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Withdrawal row quote (AEGIS-APR-117): WD-B2-1 withdraws K-197 (readability-lane-b-implementer-c): B2-1 accepted: .claude/skills/frontend-perf-engineer/references/frontend-metric-budget-sheet.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Fresh row: K-205, event kind full-page-acceptance, same page, same revision,
  same blob, recorded by deepseek-flash-apr117-keeper

### WD-B2-2 - lane B batch 2, withdrawn row K-198, withdrawal row K-198W, fresh row K-206

- Page: .claude/skills/full-codebase-auditor/SKILL.md
- Original keeper (accepting reviewer agent): readability-lane-b-implementer-c
- Acceptance revision (the reviewed head; the read is not repeated): e2a3e20b7c20ef8385b219b39c6405237163406f
- Blob ID, recomputed this round with `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:.claude/skills/full-codebase-auditor/SKILL.md` (never transcribed): 87f49bbcc8524f707a60e16981020ab2fad2f400
- Original quote, transcribed verbatim from the lane batch record docs/evidence/documentation/readability-lane-b-batch-2-2026-10-15.md: B2-2 accepted: .claude/skills/full-codebase-auditor/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Withdrawal row quote (AEGIS-APR-117): WD-B2-2 withdraws K-198 (readability-lane-b-implementer-c): B2-2 accepted: .claude/skills/full-codebase-auditor/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Fresh row: K-206, event kind full-page-acceptance, same page, same revision,
  same blob, recorded by deepseek-flash-apr117-keeper

### WD-B2-3 - lane B batch 2, withdrawn row K-199, withdrawal row K-199W, fresh row K-207

- Page: .claude/skills/full-codebase-auditor/references/audit-inventory-checklist.md
- Original keeper (accepting reviewer agent): readability-lane-b-implementer-c
- Acceptance revision (the reviewed head; the read is not repeated): e2a3e20b7c20ef8385b219b39c6405237163406f
- Blob ID, recomputed this round with `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:.claude/skills/full-codebase-auditor/references/audit-inventory-checklist.md` (never transcribed): d68fda84cac40c09acf802d8282525686e51b629
- Original quote, transcribed verbatim from the lane batch record docs/evidence/documentation/readability-lane-b-batch-2-2026-10-15.md: B2-3 accepted: .claude/skills/full-codebase-auditor/references/audit-inventory-checklist.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Withdrawal row quote (AEGIS-APR-117): WD-B2-3 withdraws K-199 (readability-lane-b-implementer-c): B2-3 accepted: .claude/skills/full-codebase-auditor/references/audit-inventory-checklist.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Fresh row: K-207, event kind full-page-acceptance, same page, same revision,
  same blob, recorded by deepseek-flash-apr117-keeper

### WD-B2-4 - lane B batch 2, withdrawn row K-200, withdrawal row K-200W, fresh row K-208

- Page: .claude/skills/funnel-definition-designer/SKILL.md
- Original keeper (accepting reviewer agent): readability-lane-b-implementer-c
- Acceptance revision (the reviewed head; the read is not repeated): e2a3e20b7c20ef8385b219b39c6405237163406f
- Blob ID, recomputed this round with `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:.claude/skills/funnel-definition-designer/SKILL.md` (never transcribed): 34c3583d726c179d56ee3db65817a4e615ac65e4
- Original quote, transcribed verbatim from the lane batch record docs/evidence/documentation/readability-lane-b-batch-2-2026-10-15.md: B2-4 accepted: .claude/skills/funnel-definition-designer/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Withdrawal row quote (AEGIS-APR-117): WD-B2-4 withdraws K-200 (readability-lane-b-implementer-c): B2-4 accepted: .claude/skills/funnel-definition-designer/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Fresh row: K-208, event kind full-page-acceptance, same page, same revision,
  same blob, recorded by deepseek-flash-apr117-keeper

### WD-B2-5 - lane B batch 2, withdrawn row K-201, withdrawal row K-201W, fresh row K-209

- Page: .claude/skills/funnel-definition-designer/references/funnel-sheet.md
- Original keeper (accepting reviewer agent): readability-lane-b-implementer-c
- Acceptance revision (the reviewed head; the read is not repeated): e2a3e20b7c20ef8385b219b39c6405237163406f
- Blob ID, recomputed this round with `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:.claude/skills/funnel-definition-designer/references/funnel-sheet.md` (never transcribed): c7456559bfa7b31200232ff6631614c2daba39f2
- Original quote, transcribed verbatim from the lane batch record docs/evidence/documentation/readability-lane-b-batch-2-2026-10-15.md: B2-5 accepted: .claude/skills/funnel-definition-designer/references/funnel-sheet.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Withdrawal row quote (AEGIS-APR-117): WD-B2-5 withdraws K-201 (readability-lane-b-implementer-c): B2-5 accepted: .claude/skills/funnel-definition-designer/references/funnel-sheet.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Fresh row: K-209, event kind full-page-acceptance, same page, same revision,
  same blob, recorded by deepseek-flash-apr117-keeper

### WD-B2-6 - lane B batch 2, withdrawn row K-202, withdrawal row K-202W, fresh row K-210

- Page: .claude/skills/gated-deployment-prompt-template/SKILL.md
- Original keeper (accepting reviewer agent): readability-lane-b-implementer-c
- Acceptance revision (the reviewed head; the read is not repeated): e2a3e20b7c20ef8385b219b39c6405237163406f
- Blob ID, recomputed this round with `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:.claude/skills/gated-deployment-prompt-template/SKILL.md` (never transcribed): 0582c3a6d7b9e8137d9f9e767d2d904b73995429
- Original quote, transcribed verbatim from the lane batch record docs/evidence/documentation/readability-lane-b-batch-2-2026-10-15.md: B2-6 accepted: .claude/skills/gated-deployment-prompt-template/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Withdrawal row quote (AEGIS-APR-117): WD-B2-6 withdraws K-202 (readability-lane-b-implementer-c): B2-6 accepted: .claude/skills/gated-deployment-prompt-template/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Fresh row: K-210, event kind full-page-acceptance, same page, same revision,
  same blob, recorded by deepseek-flash-apr117-keeper

### WD-B2-7 - lane B batch 2, withdrawn row K-203, withdrawal row K-203W, fresh row K-211

- Page: .claude/skills/gated-deployment-prompt-template/references/deployment-prompt-template.md
- Original keeper (accepting reviewer agent): readability-lane-b-implementer-c
- Acceptance revision (the reviewed head; the read is not repeated): e2a3e20b7c20ef8385b219b39c6405237163406f
- Blob ID, recomputed this round with `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:.claude/skills/gated-deployment-prompt-template/references/deployment-prompt-template.md` (never transcribed): 59c065326306befe862aa8cd60b30d1f4c05b62b
- Original quote, transcribed verbatim from the lane batch record docs/evidence/documentation/readability-lane-b-batch-2-2026-10-15.md: B2-7 accepted: .claude/skills/gated-deployment-prompt-template/references/deployment-prompt-template.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Withdrawal row quote (AEGIS-APR-117): WD-B2-7 withdraws K-203 (readability-lane-b-implementer-c): B2-7 accepted: .claude/skills/gated-deployment-prompt-template/references/deployment-prompt-template.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Fresh row: K-211, event kind full-page-acceptance, same page, same revision,
  same blob, recorded by deepseek-flash-apr117-keeper

### WD-B2-8 - lane B batch 2, withdrawn row K-204, withdrawal row K-204W, fresh row K-212

- Page: .claude/skills/hidden-context-exposure-reviewer/SKILL.md
- Original keeper (accepting reviewer agent): readability-lane-b-implementer-c
- Acceptance revision (the reviewed head; the read is not repeated): e2a3e20b7c20ef8385b219b39c6405237163406f
- Blob ID, recomputed this round with `git rev-parse e2a3e20b7c20ef8385b219b39c6405237163406f:.claude/skills/hidden-context-exposure-reviewer/SKILL.md` (never transcribed): 43ba5d0990dc63c290866ad6b2239c0cff2e3c8f
- Original quote, transcribed verbatim from the lane batch record docs/evidence/documentation/readability-lane-b-batch-2-2026-10-15.md: B2-8 accepted: .claude/skills/hidden-context-exposure-reviewer/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Withdrawal row quote (AEGIS-APR-117): WD-B2-8 withdraws K-204 (readability-lane-b-implementer-c): B2-8 accepted: .claude/skills/hidden-context-exposure-reviewer/SKILL.md read whole at e2a3e20b7c20ef8385b219b39c6405237163406f
- Fresh row: K-212, event kind full-page-acceptance, same page, same revision,
  same blob, recorded by deepseek-flash-apr117-keeper

## What this round did not verify

- Whether the eight pages were truly read whole by the round-1 reader: that process claim
  is not checkable from the repository. This round verified the pages' blob IDs at the
  bound revision, the row bindings and the identifier ordering - not the act of reading.
- The merge of the pull request that carries these rows: **AEGIS-APR-101's Scope FORBIDDEN
  bars the keeper from merging what it recorded.** The merge must be performed by a
  different agent, after the required checks are green at the exact head.
- This file itself: it is a new reader page with no keeper row, so it counts pending, like
  every other evidence record before it.
