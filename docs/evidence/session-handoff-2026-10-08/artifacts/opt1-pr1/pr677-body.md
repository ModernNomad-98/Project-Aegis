## What & why

**Plan (required).** Work item RCF-1, readability pending-count reconciliation, selected by the owner on 2026-10-07.

- **What.** This PR adds two forward-dated notes and nothing else (additions only, 0 deleted lines):
  1. `docs/roadmaps/aegis-documentation-readability-backlog.md`: a new `### Current-count reconciliation — appended 2026-10-07, measured at 03c93c77` subsection at the top of `## Start here — current reading`, before the 2026-10-03 premises correction.
  2. `docs/roadmaps/aegis-backlog-forecast.md`: one superseded-state blockquote directly after the "Current reading at the 2026-09-30 catch-up checkpoint after #554" block.
- **Why.** At `03c93c77` the repository's current-state surfaces disagree with its own acceptance tool and with each other:
  - The forecast's "Start here" still presents 656 / 584 / 1 / 55 / 16 (tip 657) as the ledger's live totals, plus "zero known pending" statements, with no pointer to the later corrections.
  - On the ledger's own records, the 2026-10-02 named set carried forward gives **at least 40** pending pages.
  - `check_index.py` counts **212** on its own frozen basis. That count over-counts relative to the ledger's records by **at least 6** verified pages; the full size of the over-count is not derivable.
  - The ledger note re-measures the inventory (`675 − 1 − 65 = 609` reader pages), answers the 2026-10-03 note's `unsure` with the six verified cases, and keeps the exact count **not derivable**.
  - The forecast note points to the ledger note.
- **Blast radius.** Two Markdown pages, both already pending. No code, CI, approval, skill or instruction file changes.
  - `build_index.py` harvests the ledger. The added text is worded so it harvests nothing (AC-5/AC-6 below).
  - Inserting near the top of the ledger shifts unvalidated line labels in the acceptance index. The note discloses this.
  - Rollback: revert the single commit.
- **Paths (scope lock):** exactly the two files above.
- **Not done, deliberately:**
  - No page accepted and no acceptance recorded (ledger-keeper acts are out of scope, AEGIS-APR-101).
  - No dated text rewritten.
  - No `tools/` change: the harvester repair and index rebuild are named as owed.
  - No decision on index precedence: this question is held for the owner.
  - No exact count claimed.
- **Acceptance criteria (from the audited plan):**
  - AC-1: scope is exactly two files, with no add, delete or rename.
  - AC-2: additions only; the ledger adds at most 120 lines and the forecast at most 18.
  - AC-3: placement as described above.
  - AC-4: the ledger content elements 1–10 are present, and the figures 211, 217, 228 and 391 and the phrase "exactly one" are absent.
  - AC-5: no added sentence or table cell reads as an acceptance to the harvester's own functions.
  - AC-6: the `check_index.py` summary, the pending set, the `build_index.py --candidates` counts and the tracker candidates are unchanged.
  - AC-7: the forecast content elements 1–5 are present.
  - AC-8: K1–K7, K11, K12, K14 as expected; K9 and K15 unchanged from base (K9 exit 1 with the one pre-existing mismatch; K15 the two sandbox process-control errors), and the Stage E `UNRUN` list carried as pre-listed.
  - AC-9: no dated text rewritten, no acceptance, no precedence decision, no exact count.
  - Criteria not verifiable at the implementation head: none.

**Audited plan revision.** `PLAN-rev2.md`, sha256 `564da28340f1cf191860192723d02641c5bd82d9e712c54713b9ca9155eb7c65`. It received `SD-B: ACCEPT` in an independent plan audit (`PLAN-AUDIT-rev2.md`, sha256 `5165f6d5dd299a1e0ef03769d9dba0fcead0231406f7a3d4ea9b59e73f113ba9`). Both files are session artifacts held by the coordinator.

**Implementation head (Stage C):**
- Head: `ccf3fc22001b277dd62d1185d939e23a7977e299`
- Tree: `6afd2ea75e40985cbba7985846b63f36580050b5`
- Base: `03c93c77a05e89d082f93c91b23dffabb332373c`
- `SD-C: COMPLETE`

## Checklist

- [x] `python scripts/tests/test_validator.py` passes locally (`OK: 181 gate self-test assertion(s) passed.`)
- [x] `python scripts/validate-skills.py` passes locally (`OK: 195 skill(s) valid, 0 warning(s)`, exit 0)
- [ ] Offline CI coverage and limits reviewed; both Ubuntu and Windows verification jobs checked. *Not ticked: hosted run `37667969180` at this head (`ccf3fc22`) completed with `conclusion: success` — `validate-skills`, `gate-guard` and `changes` succeeded; the three advisory jobs `windows-offline-checks`, `tools-tests-linux` and `tools-tests-windows` were skipped by the `changes` job's path filter, so no Windows job ran. Skipped is recorded as skipped, neither failed nor green.*
- [x] No skills added, renamed or removed (not applicable)
- [x] No README skill totals touched (not applicable)
- [x] Commits carry a DCO sign-off (`python -P scripts/check_dco.py --range "03c93c77..HEAD"` → `OK: 1 commit(s) checked, all signed off or exempt.`)

**Local checks at head `ccf3fc22` (Stage C)**

Python 3.13.16 locally; CI pins 3.14.

| # | Check | Result |
| --- | --- | --- |
| K1 | `validate-skills.py` | `OK: 195 skill(s) valid, 0 warning(s)` |
| K2 | `test_validator.py` | `OK: 181 …` |
| K3 | `test_audit_skill_contracts.py` | `OK: 76 …` |
| K4 | `test_markdown_links.py` | `OK` |
| K5 | `test_offline_ci.py` | `OK (skipped=1)` |
| K6 | CI page-set link check, 619 paths | `links checked: 3193 anchors checked: 843 broken: 0 dead: 0`. That is 839 at base plus the 4 anchor links added, counted by grep. |
| K7 | readability unit tests (extra; CI does not run it) | `Ran 7 tests … OK` |
| K8 | `check_index.py --ref HEAD` | 602 / 436 / 212 / 159 / 224 / 7. Only `compared_ref` differs from base; pending and undecided sets are equal to base. |
| K9 | `verify_ground_truth.py --ref HEAD` | exit 1, the same single pre-existing `cloud-security-baseline-reviewer` unreachable-revision mismatch as base |
| K10 | `build_index.py --ref HEAD --candidates` (no `--write`) | Counts block identical to base. The 56 tracker candidate lines are equal as a sorted multiset once the `:<line>` suffix is stripped and column padding is collapsed; the raw lines differ only in padding, because line numbers grew from 3 to 4 digits. |
| K11 | gate-guard regex over the changed files | 0 matches |
| K12 | DCO | exit 0 |
| K13 | `git diff --numstat 03c93c77 HEAD` | `15 0` forecast; `120 0` ledger |
| K14 | Behavioral Eval Runner (BER) offline self-check | `"self_check": "PASS"`, exit 0 |
| K15 | BER offline unit suite | `Ran 1094 tests`, `FAILED (errors=2, skipped=13)`. **Failed locally, identically at base**: `test_watchdog_kills_synthetic_child_tree` and `test_posix_background_child_terminated_after_leader_exit`, both "pgid … still has live members after 25 checks" (sandbox process-group cleanup). The `validate-skills` CI job at this head is the governing result. |
| AC-5 | harvester-function wording script | 158 scopes checked; (a) verdict plus resolved path: 0; (b) conservative superset: 0. A positive control on a known hazard sentence is detected. |

**Not run locally:**
- hash-locked `pip install` / `pip check` / `pip freeze`: CI dependencies are not installed here.
- `scripts/ci/check-environment.py`: exit 1 at its first import, `No module named 'openai'`, before any check runs.
- Scenario A in PowerShell Core: `which pwsh` returns nothing.

All three are covered by the `validate-skills` CI job at the PR head.

## Aegis skills used (required)

Each stage adds its own row. The rows for Stages A, B, D, E and F (round 1) are transcribed from those agents' own reports, with their source named. They are not Stage C's claims.

<!-- bound-field: skills -->

| Skill | Stage / agent | How applied | Result / evidence |
| --- | --- | --- | --- |
| [`source-of-truth-reconciler`](https://github.com/ModernNomad-98/Project-Aegis/blob/main/.claude/skills/source-of-truth-reconciler/SKILL.md) | A PLAN rev2 / RCF-1 planner (self-reported, `PLAN-rev2.md` §12) | Enumerated the stated claims with anchors; tagged each conflict IS or SHOULD; applied precedence rule 2 over rule 5; surfaced assumptions with their risk; held the SHOULD conflict for the owner | C1–C4 resolved by forward notes; C5 (index precedence) held UNRESOLVED |
| [`change-classification-gate`](https://github.com/ModernNomad-98/Project-Aegis/blob/main/.claude/skills/change-classification-gate/SKILL.md) | A PLAN rev2 / RCF-1 planner (self-reported, `PLAN-rev2.md` §12) | Classified the change against the two-file scope | docs-only; no approval class; two-file scope lock |
| [`source-of-truth-reconciler`](https://github.com/ModernNomad-98/Project-Aegis/blob/main/.claude/skills/source-of-truth-reconciler/SKILL.md) | B PLAN AUDIT / RCF-1 plan auditor (self-reported, `PLAN-AUDIT-rev2.md` §7) | Re-ran the cited lines, numstats and SHAs; re-checked C1–C5 and assumptions A1–A6 | C3 and C4 rest on verified premises; C5 correctly held; `SD-B: ACCEPT` |
| [`acceptance-criteria-reviewer`](https://github.com/ModernNomad-98/Project-Aegis/blob/main/.claude/skills/acceptance-criteria-reviewer/SKILL.md) | B PLAN AUDIT / RCF-1 plan auditor (self-reported, `PLAN-AUDIT-rev2.md` §7) | Checked AC-1 to AC-9 for testability (a partial fit for Stage B) | All nine TESTABLE, some mixed |
| [`change-classification-gate`](https://github.com/ModernNomad-98/Project-Aegis/blob/main/.claude/skills/change-classification-gate/SKILL.md) | C IMPLEMENT / RCF-1 implementer | Applied the scope lock at commit time: inspected the actual changed files against the contract; checked the docs-only floor (links resolve under K6) | `git diff --name-only` shows exactly the two contracted paths; `--diff-filter=ADR` is empty; K6 reports 0 broken links. No reclassification was needed. |
| [`ai-closeout-reporter`](https://github.com/ModernNomad-98/Project-Aegis/blob/main/.claude/skills/ai-closeout-reporter/SKILL.md) | C IMPLEMENT / RCF-1 implementer | Wrote the Stage C handoff: an explicit not-done list; files taken from git; every check given with its command and actual result; K15 failures reported verbatim; skips broken down by reason | Stage C handoff block (coordinator-held `IMPL-HANDOFF.md`); this PR body's check table |
| No owning skill | C IMPLEMENT | `docs/delivery-workflow.md` records that no installed skill owns general implementation. `reviewable-diff-discipline` is MANUAL-ONLY and was not named by the owner. | Stage C is procedurally enforced |
| [code-reviewer](https://github.com/ModernNomad-98/Project-Aegis/blob/main/.claude/skills/code-reviewer/SKILL.md) | D IMPL AUDIT / RCF-1 implementation auditor (self-reported, implementation-audit comment on this PR) | Reviewed the obtained diff 03c93c77..ccf3fc22 against the plan; correctness pass re-deriving every figure; machine-reader (harvester) invariance, link, gate-guard and DCO checks; severity-ranked findings | SD-D: ACCEPT, AC-1–AC-9 MET (implementation-audit comment on this PR) |
| [`risk-tiered-validation-selector`](https://github.com/ModernNomad-98/Project-Aegis/blob/main/.claude/skills/risk-tiered-validation-selector/SKILL.md) | E VALIDATE / RCF-1 validator (self-reported, validate comment 6044706387) | Selection only, as its contract requires: from `git diff --name-status 03c93c77 ccf3fc22` (two `M` files, neither on its never-docs-only list) | Tier docs-only; all runnable repository checks still run (execution is procedural) |
| [`ci-failure-classifier`](https://github.com/ModernNomad-98/Project-Aegis/blob/main/.claude/skills/ci-failure-classifier/SKILL.md) | E VALIDATE / RCF-1 validator (self-reported, validate comment 6044706387) | Applied to the downloaded hosted logs of run 37667969180 and to the local K15 failures | Hosted run CLEAN; local K15 INFRASTRUCTURE (sandbox process-group cleanup); `SD-E: INCOMPLETE — UNRUN LISTED` |
| [`code-reviewer`](https://github.com/ModernNomad-98/Project-Aegis/blob/main/.claude/skills/code-reviewer/SKILL.md) | F FINAL REVIEW round 1 / RCF-1 final reviewer (self-reported, final-review comment 6044893720) | Applied: real diff obtained; correctness (decisive figures recomputed), security, reliability (harvester invariance), validation-integrity and maintainability passes; severity-ranked findings. `library-diff-reviewer` read, not applied (no `.claude/` path changed); `security-pr-reviewer` read, not applied (documentation only) | Round 1 `SD-F: REVISE` (B-1, m-1; nits N-1 to N-5); security answer `No` confirmed |

<!-- bound-field: end -->

## Security-relevant surface? (required)

<!-- bound-field: security -->

- [ ] Yes
- [x] No. Both changed paths are under `docs/roadmaps/`. Neither is in `CONTRIBUTING.md`'s security-relevant surface list, and neither matches the `gate-guard` pattern (K11: 0 matches).

<!-- bound-field: end -->

## Reconciliation witness (required)

The change edits neither `docs/delivery-workflow.md` nor `AGENTS.md`. `git diff --name-only 03c93c77 HEAD -- docs/delivery-workflow.md AGENTS.md | wc -l` → `0`.

<!-- bound-field: witness -->

| # | Site | Status | Evidence (command and output) |
| --- | --- | --- | --- |
| 1 | The `MG` block | unchanged-and-verified | `git rev-parse <ref>:docs/delivery-workflow.md` → `720a858083f6…` at both `03c93c77` and `ccf3fc22` |
| 2 | The `SD` block | unchanged-and-verified | same blob at base and head, as row 1 |
| 3 | The dependency block | unchanged-and-verified | same blob at base and head, as row 1 |
| 4 | The handoff block | unchanged-and-verified | same blob at base and head, as row 1 |
| 5 | The pointer-shaped sites | unchanged-and-verified | `grep -c 'MG[1-5]'` → 33 and `grep -c 'SD-[A-G]'` → 46 on `docs/delivery-workflow.md`, the same at base and head |
| 6 | The `AGENTS.md` summary | unchanged-and-verified | `git rev-parse <ref>:AGENTS.md` → `116450fd754c…` at both base and head |
| 7 | The PR body | unchanged-and-verified | This body carries no rule text beyond this witness and the skills table. No divergence table is needed, because no `AGENTS.md` or condition changed. |
| 8 | The stage table's exit-disposition column | unchanged-and-verified | same blob at base and head, as row 1 |

<!-- bound-field: end -->

## Readability (CONTRIBUTING rule 6)

**Pages edited, both still pending:**
- `docs/roadmaps/aegis-documentation-readability-backlog.md`
- `docs/roadmaps/aegis-backlog-forecast.md`

This PR confers no acceptance. Each page still owes an independent full-page re-read against the ledger's "Acceptance for each page" criteria, by a reader who did not write it. The repository-wide sweep's pending set is otherwise unchanged by this PR (K8).

## Divergence table (required when `AGENTS.md` or a condition changed)

Not applicable: neither `AGENTS.md` nor any condition changed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01KVt4UFM9to3vScP5k33f1q

---
_Generated by [Claude Code](https://claude.ai/code/session_01KVt4UFM9to3vScP5k33f1q)_
