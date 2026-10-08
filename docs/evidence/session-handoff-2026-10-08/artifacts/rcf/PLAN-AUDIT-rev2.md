# RCF-1 — Stage B INDEPENDENT PLAN AUDIT of PLAN rev2

- **Audited revision:** `PLAN-rev2.md`, sha256 `564da28340f1cf191860192723d02641c5bd82d9e712c54713b9ca9155eb7c65` (352 lines). I checked the hash at audit start (2026-10-07T18:18:38Z) and again at audit end (see "Timing"). I audited that exact text only. `PLAN-rev1.md` is unchanged (`dcd7dc9f…5be`).
- **Auditor:** the same Stage B agent that audited rev1 (`PLAN-AUDIT-rev1.md`, `SD-B: REVISE`). I did not write either plan, and I hold no other stage of this change.
- **Repository state re-observed this turn:**
  - `git rev-parse HEAD origin/main` → both `03c93c77a05e89d082f93c91b23dffabb332373c`.
  - `git status --porcelain | wc -l` → `0`, before and after every run.
  - No `tools/readability_acceptance/__pycache__` was created.
- **Brief re-read:** `BRIEF-COMMON.md`, sha256 `b894b171…a5cc`, 56 lines.
  - It already held the owner's merge and failure-handling instructions when I first read it for rev1. I found no newer edit (file time 17:37).
  - The disposition tokens come from `docs/delivery-workflow.md` "Stage dispositions": `SD-B` is **ACCEPT** or **REVISE**.
- **My raw outputs:** `…/scratchpad/rcf/audit-evidence/`. New this round:
  - `blindspot_probe.py` (the harvester's own functions run on the lines the plan cites)
  - `k14_ber_selfcheck.txt`, `k15_ber_suite.txt`, `check_env.txt`

## Disposition

**`SD-B: ACCEPT`**

- **B-1 and B-2 are resolved.** Every new figure I re-derived matches its command.
- **No new false premise affects a stated floor, ceiling or count.**
- **The acceptance-criteria set is still mechanical where it matters:** AC-1, AC-2, AC-3, AC-5, AC-6 and AC-8 fully; AC-4, AC-7 and AC-9 through grep-able parts plus reviewer reading.
- **Seven non-blocking nits (N-1 to N-7) are below.** They are instructions for Stage C, and Stage D should check them.
  - **Do not edit the plan to apply them.** Editing `PLAN-rev2.md` would void this ACCEPT (`docs/delivery-workflow.md`, Proportionality).
  - Each nit can be met inside the plan's existing wording intent and acceptance criteria.

---

## 1. B-1 and B-2: resolved?

**B-1 — resolved.**
- The "exactly one" premise is gone, and so is every bound derived from it: 211, 217, 218 as a bound, 228 and 391.
- AC-4 now lists those figures as **absent**, and AC-7 forbids 218, 391 and 228. Both are checks a command can run.
- 212 is attributed only to the tool, on its frozen harvest. Plan element 4 says plainly: *"212 is the tool's count on its own basis — not a floor or ceiling on this ledger's records."*
- The 2026-10-03 `unsure` is answered as "yes, at least 6, size not derivable". The 218 and "at most 390" are forward-noted as figures on the tool's basis, and no corrected tool-based bound is published (section 9 rules that out explicitly).
- The harvester's blind spots are recorded as owed `tools/` work, with the six pages as regression cases.
- The C3 verdict, C5 option (1) (no figure now), A2 and R3/R4 are all rewritten to match.
- I re-verified everything above in §2.

**B-2 — resolved.**
- The figure is now "the 2026-10-02 named set carried forward to `03c93c77`: 35 − 2 + 7 = **at least 40**", and the plan says explicitly that it is not a re-run.
- `docs/README.md` is the worked example. The plan says a re-run "could only raise the floor".
- "At least 40" is used in §2.5, C4, element 6, §6.2, AC-4 and AC-7.
- One wording imprecision remains in the plan's descriptor for the 44 paths; see N-1.

## 2. New figures re-derived (my commands, this turn)

| Plan claim | My command → output | Holds? |
| --- | --- | --- |
| Floor **at least 40** = 35 − 2 + 7 | `python3 -c "print(35-2+7)"` → `40`. The 35 comes from `LIMB_A/B/C`: union 35, verified in round 1. The −2 are the setup pages: empty numstat from `e6fc8d24`, re-verified in round 1. The +7 new pages: re-verified in round 1, all pages added after `d6e48418` (`git log --diff-filter=A`). | yes |
| Ceiling **at most 569** accepted (609 − 40), under the accepted-unless-pending convention | `print(609-40)` → `569`. 609 reader pages, re-verified. The convention is the one `check_index.py`'s own docstring states ("counts a tracked reader page as accepted unless it is listed pending"). 584 > 569, so the opening paragraph's 584 cannot be current. | yes |
| **44** Markdown paths changed or added since `d6e48418` | `git diff --numstat d6e48418 03c93c77 -- '*.md' \| wc -l` → `44`. Breakdown: `--name-status` gives 17 A and 27 M. 34 are reader pages; 10 are classified fixtures under `scripts/tests/fixtures/markdown-links/`. | figure yes; descriptor imprecise → **N-1** |
| `docs/README.md` 143 changed lines since `d6e48418`; the keeper row records 141 | `git diff --numstat d6e48418 03c93c77 -- docs/README.md` → `83 60`. Ledger line 3146 reads "changed 81 added / 60 deleted = 141 lines". | yes |
| No later recorded acceptance for the 33 carried pages | `git diff -U0 d6e48418 03c93c77 -- <ledger>`, added lines that contain acceptance words: only the keeper's two conferring rows, its "declines" / "not a full-page acceptance" rows, and quotations or rule text. My round-1 window probe found no named-set page apart from false positives and host feasibility. | yes (assumption A5 is correctly surfaced) |
| Six verified over-count pages, full revision prefixes | `git rev-parse` → `f5a6dabb7c8b`, `af328b512417`, `a56c60d8ad54`, `620b24595255`, `acdcdad4563b`. Empty numstat, 0 new headings, and still pending in the tool were all verified in round 1 (`overcount_verified.txt`). Host feasibility is not an ancestor of main and is reachable only via `origin/docs/readability-batch-b`. | yes |
| Other ledger rows the plan cites | Line 2800 (#410, after #397) is newer than line 2807 (#407): yes. Line 2769 is the #456 row "accepted both on `620b245`": yes. | yes |
| **Four harvester blind spots** | `python3 -I -B audit-evidence/blindspot_probe.py`, which runs `build_index.py`'s own `TRACKER_ROW_RE`, `sentence_split`, `verdict_in`, `clause_links`, `normalise_path` and `is_plausible_path` on the cited lines. The four results are listed after this table. | all four yes |
| Rebuild alone still binds `8ed59cd7` for host feasibility | `build_index.py --ref 03c93c77… --rows <host-feasibility>` (no `--write`) → `"last_acceptance_sha": "8ed59cd761d1…"`, evidence `…after-237-2026-09-24.md:142` | yes |
| Hazard examples (§2.6) | Same probe:<br>• `` `iac-reviewer/SKILL.md` was not accepted at `03c93c77`. `` → verdict `accepted`, path `.claude/skills/iac-reviewer/SKILL.md` (found through the `PATH_HINTS` prefixes).<br>• The same kind of sentence with a `](../evidence/…)` link → verdict but no path, so nothing is harvested.<br>• A backticked path with "recorded acceptance revision" → path but no verdict. | yes |
| **K14 baseline** | `python3 -B -m tools.behavioral_eval_runner self-check` (scratch `TMPDIR`) → exit 0, `"self_check": "PASS"` | yes |
| **K15 baseline** | `python3 -B -m unittest discover -s tools/behavioral_eval_runner/tests -p 'test_*.py'` (scratch `TMPDIR`) → exit 1, `Ran 1094 tests in 30.851s`, `FAILED (errors=2, skipped=13)`. The errors are exactly `test_process_control.TestProcessTreeKill.test_watchdog_kills_synthetic_child_tree` and `test_review_blockers.TestSupervisorDescendantCleanup.test_posix_background_child_terminated_after_leader_exit`, both `ProcessControlError: … pgid NNNN still has live members after 25 checks`. | yes |
| `check-environment.py` fails locally | `python3 -P -B scripts/ci/check-environment.py` → exit 1, `ModuleNotFoundError: No module named 'openai'`. It fails at its first import, before any check runs. | yes |
| No `pwsh` | `which pwsh` → no output, rc 1 | yes |
| `build_index` baseline file | `cmp plan-evidence/build_index_readonly_candidates.txt audit-evidence/build_index_candidates_base.txt` → identical. These are two separate runs with byte-identical output, not "the same run"; that does not matter. | yes |
| PR template field lines | `.github/pull_request_template.md` lines 18 ("Audited plan revision"), 41 (skills table), 62 (security question), 71 (reconciliation witness) | yes |
| Unchanged from round 1 (re-run there) | `check_index.py` at three refs (212 / 159 / 224 / 7; identical pending sets); `verify_ground_truth.py` (exit 1, one mismatch); the 675 / 65 / 1 / 609 inventory; 7 pages absent from the index; K1–K6 baselines; placement; gate-guard; security-relevant surface | yes |

**The four blind spots** (from `blindspot_probe.py`):
1. **Per physical line.**
   - Ledger lines 1989 and 1993: one line has the iac-reviewer path with no verdict, the other has "accepted" with no path.
   - Lines 1014 and 1015: the same split.
   - Line 921: a verdict with a path for `managed-platform-tier.md` but no commit SHA.
   - Lines 1510 and 1515: the same split.
2. **Per table cell.** Lines 2769, 2788 and 2800: the paths are in cell 1 and "accepted" is in cell 2.
3. **Unresolved names.**
   - `normalise_path('../../tools/behavioral_eval_runner/README.md')` → `None`.
   - `normalise_path('../evidence/setup/issue-101-package-4a-host-feasibility.md')` → `None`.
   - `is_plausible_path('source-of-truth-reconciler')` → `False`.
4. **No verdict word.** Keeper rows 3123 and 3124 → "no verdict, no path".

## 3. N-1 to N-10 dispositions from rev1: do they hold?

| rev1 nit | rev2 disposition | Holds? |
| --- | --- | --- |
| N-1 CI subset | K14/K15 added with verified baselines. The CI steps not run locally are pre-listed. Skipped advisory jobs are recorded as skipped, not green, for MG1. K7 is marked as extra. | yes — one vocabulary issue, see N-2 below |
| N-2 hazard example | Corrected, and verified with the harvester's own functions. AC-5 keeps the conservative superset. | yes |
| N-3 AC-5/AC-6 mechanics | AC-5(a) imports the harvester functions. AC-5(b) is the superset. AC-6/K10 compare the candidates as a sorted multiset with `:<line>` stripped. | yes |
| N-4 first-use rules | Element 1 requires plain-word definitions of PR, commit SHA, the index, `check_index.py`, bound, ledger keeper, and AEGIS-APR-101 with its register anchor. The forecast note must expand or avoid abbreviations. Both are in AC-4/AC-7. | yes |
| N-5 forecast purpose paragraph | S4b added. D2 element 2 covers it, and that paragraph's reserved-scope text must not be quoted. | yes |
| N-6 `e6fc8d24` caveat | Element 5 requires it; the facts were re-verified. | yes |
| N-7 issue #101 page | Wording constraint added. | yes |
| N-8 `tracker_line` | Added in §3 and element 10. Re-verified: `build_index.py:495` uses it only as an evidence label. | yes |
| N-9 PR-body obligations | In the continuation line, with template line numbers verified. | yes |
| N-10 shallow claims | Kept as planner-measured; the note omits the comparison. | yes |

## 4. Non-blocking nits for Stage C, checked at Stage D

- **N-1 — "44 Markdown paths … none re-measured" is imprecise.**
  - Where it appears: §2.5 ("44 Markdown paths changed or added, none re-measured here") and element 6.
  - The 44 break down as 34 reader pages plus 10 classified fixtures. The fixtures are not readability pages.
  - Of the 34 reader pages, 7 are the new pages already counted in the floor. Two, the setup pages, *were* measured: they have an empty numstat from `e6fc8d24`.
  - The 44 figure reproduces by its command, and "a re-run could only raise the floor" is true. But the note should not say that none of the 44 was measured.
  - Suggested note wording, which still satisfies AC-4's "44-path fact": *"`git diff --numstat d6e48418 03c93c77 -- '*.md'` lists 44 Markdown paths changed or added — 34 reader pages and 10 classified fixtures; apart from the two setup pages and the seven new pages, those reader pages were not re-measured against their last recorded acceptance."*
- **N-2 — Do not call K15's local errors "UNRUN".**
  - §7's pre-listed Stage E `UNRUN` items include "K15's two sandbox errors if they recur". An erroring test was run; it is a local failure, not an unrun check. `SD-E` keeps `UNRUN` and `FAIL` distinct, and "`UNRUN` is never `PASS`".
  - Stage E should record them as **failed locally, identically at base** (both names, with the `pgid … live members` cause), with the `validate-skills` CI run at the exact head as the governing result.
  - It must not convert them to `UNRUN`. Only `pip install`/`pip check`/`pip freeze`, `check-environment.py` and Scenario A in PowerShell are genuinely unrun here.
- **N-3 — Element 4's "i.e. it reflects the index's frozen harvest" claims more than the evidence shows.**
  - The pending set being identical at the three revisions shows two things: no page in the index crossed the rule's threshold in the index's terms since `d6e48418`, and the index's inputs are frozen at `d6e48418`.
  - Suggested wording: *"identical at `d6e48418`, `c3527560` and `03c93c77`: the index's acceptance rows are frozen at `d6e48418`, and no indexed page crossed the rule's threshold in its terms since"*.
- **N-4 — AC-4's absent-figure exception wording.** AC-4 says "218 (except when quoting the 2026-10-03 note)", but element 2 *names* that 218 as a dated figure rather than quoting it. Stage D should read the exception as "except where the note names the 2026-10-03 note's 218 as a dated tool-basis figure". The same applies to "at most 390", which is allowed: it is not in the absent list.
- **N-5 — K14/K15 and reserved scope (my judgment, for the coordinator).**
  - K14, K15 and `check-environment.py` run code under `tools/behavioral_eval_runner/`. They are the `validate-skills` job's own offline checks:
    - `run_self_check` is documented as "Offline invariants check".
    - `check-environment.py` prints "provider_requests: not part of this check; suites use mocked transports".
  - They are not BER calibration, and I ran them read-only with a scratch `TMPDIR`.
  - If the coordinator reads BRIEF-COMMON rule 5 more strictly, K14/K15 should move to the CI-covered list instead of being run locally. That changes nothing else in the plan.
- **N-6 — The rev2 header line overstates the brief change.** Line 9 says the owner instructions were "appended to the brief since rev1". By my observation the brief is unchanged since 17:37 and already held them during the rev1 audit. This is immaterial to scope and needs no action.
- **N-7 — Size.** The ledger note now carries 10 elements and a six-row table within ≤ 120 added lines (AC-2). If a draft exceeds the cap, trim the prose. Raising the cap or dropping an element would deviate from the accepted plan and needs a return to Stage A.

## 5. Per-criterion review (`acceptance-criteria-reviewer`)

| AC | Verdict | Evidence that will prove it |
| --- | --- | --- |
| AC-1 Scope | TESTABLE | `git diff --name-only`; `--diff-filter=ADR` empty |
| AC-2 Size, additions only | TESTABLE | `git diff --numstat` (deleted 0; ledger ≤ 120; forecast ≤ 18) |
| AC-3 Placement | TESTABLE | `grep -n` heading order; forecast line order. Placement verified correct in round 1. |
| AC-4 Ledger content | TESTABLE (mixed) | Absent-figure list and "exactly one" by grep; element presence and first-use definitions by reviewer reading; figures re-run by Stage D. Apply N-1, N-3, N-4. |
| AC-5 Wording | TESTABLE (mechanical) | Script output for (a) and (b), each → 0 |
| AC-6 Instrument invariance | TESTABLE (mechanical) | K8 summary and pending set; K10 counts plus sorted-multiset compare |
| AC-7 Forecast content | TESTABLE (mixed) | Figure whitelist by reading; absent 218/391/228 by grep; anchor resolves under K6 |
| AC-8 Checks | TESTABLE | K outputs. Record K15 per N-2. |
| AC-9 No rewrite / acceptance / C5 decision / exact count | TESTABLE (mixed) | AC-1, AC-2 and AC-5, plus reading |

**Gaps:** none blocking. "Criteria not verifiable at the implementation head: none" is acceptable for this local docs change.

## 6. Other checks that still hold

- **Classification and paths:**
  - docs-only, with exactly two files in scope.
  - Neither path matches gate-guard or CONTRIBUTING's security-relevant surface list.
  - No `.github/`, `docs/approvals/`, `scripts/` or `tools/` edit.
- **AEGIS-APR-101:** no acceptance conferred or recorded and no keeper act; the precedence question (C5) is held for the owner.
- **Reconciliation (`source-of-truth-reconciler`):**
  - C1–C4 are IS-questions resolved by precedence rule 2 (current repository state), with forward notes only.
  - C5 is a SHOULD-question held UNRESOLVED. The plan defines the terms, gives three options with pros, cons and cost, a recommendation, the evidence that would change it, and one question. Option (1) now names the known over-count instead of a figure.
  - Assumptions A1–A6 each carry a stated risk.
- **Dated-text discipline:** additions only; nothing rewritten; exact count "not derivable"; both edited pages stay pending, with the self-cost stated.

## 7. Skills used (dogfood rule)

| Skill | How applied | Result |
| --- | --- | --- |
| `source-of-truth-reconciler` (`.claude/skills/source-of-truth-reconciler/SKILL.md`) | Re-checked C1–C5, the precedence rules applied, assumptions A1–A6 with risk, and stale-source handling against the repository: re-ran the cited lines, numstats and SHAs. | C3 and C4 now rest on verified premises; C5 is correctly held. |
| `acceptance-criteria-reviewer` (`.claude/skills/acceptance-criteria-reviewer/SKILL.md`) | Per-criterion testability check of AC-1 to AC-9. It is a partial fit for Stage B by `docs/delivery-workflow.md`'s own map; the plan-level verdict is procedural. | All 9 TESTABLE, some mixed; no gaps that block. |

`design-review-facilitator` was read in round 1 and not applied; its scope is facilitating a review meeting.

## 8. Stage handoff

1. **Decision IDs:**
   - `SD-B: ACCEPT`, on sha256 `564da28340f1cf191860192723d02641c5bd82d9e712c54713b9ca9155eb7c65`.
   - This supersedes nothing: the rev1 `REVISE` stays recorded against `dcd7dc9f…5be`.
   - AEGIS-APR-101 still binds.
   - **Editing `PLAN-rev2.md` voids this ACCEPT.**
2. **Changed files:**
   - Nothing in the repository was changed.
   - Created only `…/scratchpad/rcf/PLAN-AUDIT-rev2.md` and new files under `…/audit-evidence/`.
   - No push, PR, GitHub write, `--write` run, fetch or reserved-scope action.
3. **Proven invocation:** the tables above, with raw files in `audit-evidence/`.
4. **Deviation flags:** none.
5. **Continuation:**
   - Stage C implements rev2 on base `03c93c77` (re-observe it first) and applies N-1 to N-4 and N-7 inside the existing acceptance criteria.
   - Stage D audits AC-1 to AC-9 per criterion and checks N-1 to N-4.
   - Stage E records K15 per N-2.
   - The coordinator decides N-5.
   - The PR body's "Audited plan revision" field takes `564da28340f1cf191860192723d02641c5bd82d9e712c54713b9ca9155eb7c65`.

## Timing

- Start: 2026-10-07T18:18:38Z (`date -u`, first command of this re-audit).
- Finish: 2026-10-07T18:24:56Z (`date -u`). Measured wall time: 6 min 18 s. Active time was not measured separately. No ETA was set for this re-audit item.
- Hash re-check at finish: `sha256sum PLAN-rev2.md` → `564da28340f1cf191860192723d02641c5bd82d9e712c54713b9ca9155eb7c65` (matches the audited revision).
- Repository at finish: `git rev-parse HEAD origin/main` → both `03c93c77…`; `git status --porcelain | wc -l` → `0`.
