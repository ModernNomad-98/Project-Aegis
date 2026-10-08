# RCF-1 — Readability pending-count reconciliation — PLAN rev2 (Stage A)

**Revision marker:** `rev2`. Supersedes `PLAN-rev1.md` (sha256 `dcd7dc9f8b125b48a5c3926da18425bd92ce6dc2107e9ce0e02e34fe95cdf5be`, left unmodified), in response to `PLAN-AUDIT-rev1.md` (sha256 `15797c75a3c5af314808f9fd7052d308863501afecf65d153eddbd4bde4a23e1`, verdict `SD-B: REVISE`). The rev1 ACCEPT/REVISE verdict does not carry over; rev2 needs its own Stage B audit bound to its own hash.

- **Work item:** RCF-1, selected by the owner (Peter Nguyen) on 2026-10-07 (current-turn chat instruction, per BRIEF-COMMON.md).
- **Stage:** A PLAN only (docs/delivery-workflow.md). This plan edits nothing in the repository.
- **Base:** `origin/main` = `03c93c77a05e89d082f93c91b23dffabb332373c` (re-observed at rev2 start: `git rev-parse HEAD origin/main` → both `03c93c77…`; `git status --porcelain | wc -l` → `0`; `git rev-parse --is-shallow-repository` → `false`).
- **Workspace role:** Role A (landmarks present: `README.md` opens `# Project Aegis`; `docs/skills-catalog.md`, `scripts/validate-skills.py`, `artifacts/audits/skill-contract-audit-baseline.json` exist).
- **Owner instructions appended to the brief since rev1 (read, binding on later stages, not on this plan's content):** merge authority for RCF-1's PR "once all checks are green. Including admin merge"; and "if a check fails, diagnose and fix the issue and try to merge again". Neither changes this plan's scope; both are carried in the continuation line (section 13).

## Changes from rev1

| Finding | Severity | How rev2 resolves it | Where |
| --- | --- | --- | --- |
| **B-1** "tool over-counts by exactly one" is false; ≥ 218, ≤ 391, ≥ 217, 211 and 228 unsupported | blocking | **Dropped** the premise and every bound derived from it. 212 stays strictly the tool's own count on its frozen harvest (pending set re-verified identical at `d6e48418`, `c3527560`, `03c93c77`). The 2026-10-03 `unsure` is answered: **yes, the tool over-counts relative to this ledger's records, by at least 6 verified pages; the magnitude is not derivable** without a harvester repair and an index rebuild. I re-verified all five of the auditor's extra cases independently (section 2.4). The 2026-10-03 note's 218 and "at most 390" are forward-noted as tool-basis figures, not a floor or ceiling on the ledger's records (no "correction to 217"). The harvester blind spots and the six verified cases are recorded as owed `tools/` work. C3, C5 option (1) (no figure), A2 and R3 rewritten. | §1, §2.4–2.6, §5, §6.1 el. 4–7, §6.2, AC-4, AC-7 |
| **B-2** "40" mislabelled as the 2026-10-02 method re-applied, stated as a value | blocking | Renamed to "**the 2026-10-02 named set carried forward to `03c93c77`: 35 − 2 + 7 = at least 40**", explicitly **not** a re-run; pages edited since `d6e48418` (44 Markdown paths) were not re-measured, with `docs/README.md` as the example. "At least 40" used everywhere. It is now the only floor stated on the ledger's records; a derived ceiling "at most 569 accepted" (609 − 40) replaces the dropped 391. | §2.5, §5 C4, §6.1 el. 6, §6.2, AC-4, AC-7 |
| N-1 K-checks are a subset of CI | nit | **Applied.** Renamed "local subset"; added K14 (BER self-check, runs locally: PASS) and K15 (BER suite: base result recorded, 2 sandbox process-control errors); pre-listed Stage E UNRUN items covered by the `validate-skills` CI job at the PR head; noted skipped advisory jobs are skipped, not failed, for `MG1`; K7 marked as extra (CI does not run it). | §7 |
| N-2 hazard example imprecise | nit | **Applied.** Re-verified by calling the harvester's own functions: a `../`-relative link is **not** harvested; a backticked repo path (`docs/…md`) or a short path resolvable through `PATH_HINTS` (`iac-reviewer/SKILL.md`) **is**, including negated forms and "keeps no acceptance". Example corrected; AC-5 keeps the conservative superset. | §2.6, §6.1 constraints |
| N-3 AC-5/AC-6 mechanics | nit | **Applied.** AC-5 imports `TRACKER_ROW_RE`, `sentence_split`, `verdict_in`, `clause_links` from `build_index.py`; AC-6 compares tracker candidates as a sorted multiset with `:<line>` stripped; baseline file named. | §7 K10, §8 AC-5, AC-6 |
| N-4 CONTRIBUTING new-reader rules apply to edits | nit | **Applied.** First-use definitions required in both notes (PR, commit SHA, the index, `check_index.py`, `build_index.py`, bound, ledger keeper, AEGIS-APR-101); added to AC-4/AC-7. | §6.1 el. 1, §6.2, AC-4, AC-7 |
| N-5 forecast purpose paragraph also carries readability figures | nit | **Applied.** D2 element 2 now covers the whole section's readability figures, including the PR-dated page totals and "zero known pending" statements (`aegis-backlog-forecast.md:46-52`), without quoting or touching that paragraph's reserved-scope text. §2.1 corrected. | §2.1, §6.2 |
| N-6 `e6fc8d24` reachability caveat | nit | **Applied.** Re-verified: `git merge-base --is-ancestor e6fc8d24 03c93c77` → exit 1; contained only by `refs/remotes/origin/docs/readability-batch-b`. The note must say so. | §2.4, §6.1 el. 5 |
| N-7 issue #101 page named | nit | **Applied.** Naming the host feasibility path as a readability-count item is not reserved-scope work; the note must not describe its content or host findings. | §6.1 constraints |
| N-8 `stated-acceptances.json` line refs displaced | nit | **Applied.** Re-verified 19 `tracker_line` fields; `build_index.py` uses them only as an evidence label (`evidence=f"{data['source_file']}:{row['tracker_line']}"`). One clause added. | §3, §6.1 el. 10 |
| N-9 PR-body obligations | nit | **Applied** in the continuation line (PR template fields verified at `.github/pull_request_template.md:18`, `:41`, `:62`, `:71`). | §13 |
| N-10 shallow-clone claims not re-derivable | nit | **Applied.** Kept in this plan as planner-measured with the saved files; the note omits the unshallow comparison and states only the re-derivable fact (both undecidable revisions are in no remote-tracking ref). | §2.2, §6.1 el. 4 |

---

## 1. What and why

**What.** Add two short, forward-dated notes, nothing else:

1. **Ledger** `docs/roadmaps/aegis-documentation-readability-backlog.md` — a new `###` subsection at the top of `## Start here — current reading`, between the opening (dated 2026-09-30) paragraph and `### Premises correction — appended 2026-10-03, measured at c3527560`. It re-measures the readability position at `03c93c77`, states which stated figures are dated, answers the 2026-10-03 note's `unsure` with verified cases, carries the 2026-10-02 named set forward as a floor, and keeps the exact count **not derivable**.
2. **Forecast** `docs/roadmaps/aegis-backlog-forecast.md` — a short dated blockquote directly **after** the "Current reading at the 2026-09-30 catch-up checkpoint after #554" block, stating that this section's readability figures are dated and pointing to the ledger note.

**Why.** At `03c93c77` the repository's current-state surfaces disagree with its own instrument and with each other:

- The forecast's "Start here — current reading" tells a reader that *"the ledger's live totals have since moved to 656 / 584 / 1 / 55 / 16"* (tip 657), and its purpose paragraph still says "zero known pending" for PR-dated totals (`aegis-backlog-forecast.md:15`, `:46-52`). Nothing on that page points to the 2026-10-02 floor correction or the 2026-10-03 premises correction. **This is a false current-state statement**: on the ledger's own records at least 40 pages are pending at `03c93c77` (section 2.5), and the tool counts 212 on its own basis.
- The ledger's opening paragraph (`…backlog.md:3-17`) gives 16 as the latest figure. It is honestly dated and the 2026-10-03 premises note sits beneath it, so this is a **navigation gap, not a falsehood**. But the premises note's own figures are pinned to `c3527560`, its "(3) … at least 218" and "at most 390" are tool-basis figures presented next to the word "floor", and its recorded `unsure` ("Whether the tool over-counts … is `unsure` here") can now be answered: **yes, by at least six verified pages** (section 2.4).
- The 2026-10-02 named floor (35, measured at `d6e48418`) is no longer current: two of its pages have since had recorded acceptances (ledger keeper, ratified by AEGIS-APR-101) and seven reader pages were added after `d6e48418`.
- The opening paragraph's "584 accepted" is impossible at `03c93c77`: 609 reader pages less at least 40 pending leaves at most 569 under the ledger's accepted-unless-pending convention.

**Is "no change needed" right?** No (section 4, option C).

---

## 2. Evidence (commands and observed output)

Raw outputs: `…/scratchpad/rcf/plan-evidence/` (rev1 and rev2 runs). All commands read-only.

### 2.1 Stated figures (verbatim, with anchors)

| ID | Source | Verbatim claim |
| --- | --- | --- |
| S1 | `docs/roadmaps/aegis-documentation-readability-backlog.md:11-17` (`grep -n -F 'files and **16** pending'` → 13) | "giving **656** tracked Markdown files and **16** pending … the tip count is now **657** …" (dated 2026-09-30). The same paragraph states "584 accepted reader pages". |
| S2 | same file `:2927` | "**The floor is 35 named pages, not 13 or 16**" — measured at `d6e48418`. |
| S3 | same file, premises note (own text `:19-186`) | "(3) … the floor rises from 35 to at least 218"; "**But that bound is the TOOL'S … not this ledger's floor**"; "**212 is not guaranteed to be a floor.** Whether the tool over-counts for that reason, and by how much, is **`unsure` here**"; "at least `212 + 6 = 218`"; "**at most 390**". |
| S4 | `docs/roadmaps/aegis-backlog-forecast.md:15` | "the ledger's live totals have since moved to 656 / 584 / 1 / 55 / 16" + appended note (tip 657). |
| S4b | same file `:46-52` (purpose paragraph) | "**599 pages: 555 accepted readers and 44 classified fixtures**, with zero known pending pages in the [readability ledger](…)" and "**600 pages: 556 accepted readers …**, with zero known pending." (PR-dated; partly present tense.) The same paragraph carries reserved-scope text that must not be touched or quoted. |
| S5 | `docs/approvals/APPROVAL_REGISTER.md:3150` (AEGIS-APR-101, Scope FORBIDDEN) | "No approval of the charter's proposed canonical index, its precedence, or changed counting rules." One hit for `AEGIS-APR-101` (`:3142`): no later lifecycle event. |

Other count statements are in dated records only (`docs/evidence/session-continuation-2026-09-30*.md`, execution metrics, session checkpoints, forecast checkpoint sections). `docs/README.md:58-60`, `README.md`, `CONTRIBUTING.md`, `AGENTS.md` state no pending/accepted count.

### 2.2 The instrument

`python3 -I -B tools/readability_acceptance/check_index.py --json --ref <ref>` (exit 0 at each):

| `--ref` | provably_pending | no_recorded_acceptance | within_10_lines | cannot_decide | pending path set vs `03c93c77` |
| --- | ---: | ---: | ---: | ---: | --- |
| `d6e484189cc3…` | 212 | 159 | 224 | 7 | identical (`True`) |
| `c3527560fb7e…` | 212 | 159 | 224 | 7 | identical (`True`) |
| `03c93c77a05e…` | 212 | 159 | 224 | 7 | — |

At `03c93c77`: `reader_pages_in_index 602`, `recorded_pages_compared 436`, `exact_pending_count "NOT DERIVABLE from this procedure"`. All 7 undecidable rows are `unreachable-acceptance`: `65bacc7d6b85…` (6 `cloud-security-baseline-reviewer` rows), `d3dcb62a335d…` (1 `database-backup-verifier` row); `git cat-file -t <sha>` → "could not get object info"; `git for-each-ref --contains <sha> refs/remotes | wc -l` → `0` for both. *Planner-measured, not re-derivable now (N-10):* before `git fetch --unshallow origin`, the same command gave the same counts and path sets; only `rebased_acceptance` differed (`true` on 436 rows while shallow) — `plan-evidence/check_index_shallow.json` vs `check_index_unshallow.json`.

`verify_ground_truth.py --ref refs/remotes/origin/main` → exit **1**, sole mismatch the pre-existing `cloud-security-baseline-reviewer` unreachable revision; two `PASS` lines; `658 - 1 - 55 = 602`; limbs `19/19`, `5/5`, `11/11`. Readability unit tests (`python3 -B -m unittest discover -s tools/readability_acceptance/tests -p 'test_*.py' -v`, no `-I`) → `Ran 7 tests … OK`.

### 2.3 Inventory at `03c93c77`

Method: `git ls-tree -r --name-only <ref>`, paths ending `.md`, one per emitted path.

| Figure | `d6e48418` | `c3527560` | `03c93c77` |
| --- | ---: | ---: | ---: |
| tracked Markdown | 658 | 674 | **675** |
| `.md` under `scripts/` | 56 | 66 | **66** |
| classified fixtures (less `scripts/tests/fixtures/README.md`) | 55 | 65 | **65** |
| generated reports | 1 | 1 | **1** |
| reader pages | 602 | 608 | **609** |

`git diff --name-status --diff-filter=A c3527560 03c93c77 -- '*.md'` → only `.coord/proc08-sweep-2026-10-03.md` (PR #656); `D`/`R` empty. Reader pages absent from the index → **7** (6 at `c3527560`); index paths no longer reader pages → **0**: `.coord/proc08-sweep-2026-10-03.md`, `docs/delivery-workflow.md`, `docs/evidence/documentation/acceptance-conversion-process-2026-10-02.md`, `docs/evidence/documentation/process-issues-and-prevention-2026-10-02.md`, `docs/evidence/documentation/stale-checkout-instruction-divergence-2026-10-02.md`, `docs/roadmaps/aegis-coordinator-figures.md`, `tools/readability_acceptance/README.md`. None has a recorded full-page acceptance (ledger mentions are the 2026-10-03 "added" list, the keeper's "not a full-page acceptance … remains pending" row, links; `aegis-coordinator-figures.md` §7 item 6 self-declares "starts `pending`").

### 2.4 The tool over-counts relative to the ledger's records — at least 6 verified pages

Test applied to each page (my own commands, rev2): the ledger records a later full-page acceptance at revision R; R resolves; `git diff --numstat R 03c93c77 -- <path>` is **empty**; `git diff R 03c93c77 -- <path> | grep -cE '^\+#{1,6} '` → `0`; yet `check_index.py --ref 03c93c77…` lists the page under `pending`.

| Page | Ledger record of the later acceptance (verified by reading) | R | ancestor of `03c93c77` | numstat | new headings | Tool row at `03c93c77` |
| --- | --- | --- | --- | --- | --- | --- |
| `.claude/skills/iac-reviewer/SKILL.md` | `:1982-1995` "Full-page re-reads done and accepted in this range" — full-page re-read on `8ccc5ee` (FIX-FIRST, I1–I3), then the confined re-read on `f5a6dab`, "its new acceptance point" (PR #521) | `f5a6dabb7c8b…` | yes | empty | 0 | pending, index rev `694333c0b7`, 47 lines |
| `.claude/skills/llm-output-safety-reviewer/SKILL.md` | `:1014-1015` "#424: `llm-output-safety-reviewer/SKILL.md` … accepted on `af328b5`"; table row `:2788` (newer than the `:2797` row that made it pending) | `af328b512417…` | yes | empty | 0 | pending, index rev `dbad6c25c1`, 107 lines |
| `.claude/skills/multi-tenant-data-architect/SKILL.md` | `:918-922` "Accepted after full-page re-reads (16 pages). #410: … accepted on #410's branch head (`a56c60d`)"; row `:2800` newer than `:2807` | `a56c60d8ad54…` | yes | empty | 0 | pending, index rev `1ec01bfb7f`, 23 lines |
| `.claude/skills/source-of-truth-reconciler/SKILL.md` | `:1281-1284` "#456, `tenant-modeler` (13) and `source-of-truth-reconciler` (10), **accepted** on `620b245`"; row `:2769` | `620b24595255…` | yes | empty | 0 | pending, index rev `0bc4a8fcae`, 55 lines |
| `tools/behavioral_eval_runner/README.md` | `:1510-1515` "re-read the page in full and posted **ACCEPT** on `acdcdad`. Pending to accepted." (PR #475) | `acdcdad4563b…` | yes | empty | 0 | pending, index rev `8ed59cd761`, 137 lines |
| `docs/evidence/setup/issue-101-package-4a-host-feasibility.md` | keeper row `:3123` (PR #635, ratified by AEGIS-APR-101) | `e6fc8d24ad78…` | **no** — reachable only via `refs/remotes/origin/docs/readability-batch-b` (`git for-each-ref --contains`) | empty | 0 | pending, index rev `8ed59cd761`, 244 lines |

Each page's ledger mentions were listed (`grep -n <name>`) and the later ones read: no later record returns any of them to pending, and none could by drift since each `numstat` is empty.

**Why the harvester misses them** — verified by calling `build_index.py`'s own functions (`TRACKER_ROW_RE`, `sentence_split`, `verdict_in`, `clause_links`) on the cited ledger lines, read-only, `-I -B`, no `__pycache__` written, tree clean afterwards:

| Blind spot | Observed on |
| --- | --- |
| **Per physical line:** `harvest_tracker` iterates `text.splitlines()`, so a statement wrapped across lines separates the page from its verdict | `:1989` path / `:1993` verdict (iac-reviewer); `:1014` / `:1015` (llm-output-safety-reviewer); `:919` path / `:921` verdict / `:922` revision (multi-tenant-data-architect — line 921 instead yields a verdict without a revision for `managed-platform-tier.md`); `:1510` / `:1515` (BER guide) |
| **Table rows scoped per cell:** page in one cell, verdict in another | `:2769` (source-of-truth-reconciler: paths in cell 2, "accepted" in cell 3); keeper rows `:3123-3124` |
| **Unresolved names:** a short name without `.md` fails `is_plausible_path`; a `../`-relative link fails `normalise_path` | `:1283` `` `source-of-truth-reconciler` ``; `:2788` `` `llm-output-safety-reviewer` ``; `:1510` `](../../tools/behavioral_eval_runner/README.md)`; keeper rows `](../evidence/setup/…)` (`normalise_path('../../tools/behavioral_eval_runner/README.md')` → `None`) |
| **No verdict word:** the keeper rows carry the acceptance revision but no `ACCEPT_RE` match | `:3123-3124` |

A rebuild alone does not fix this: `build_index.py --ref 03c93c77… --rows docs/evidence/setup/issue-101-package-4a-host-feasibility.md` (no `--write`) still binds `8ed59cd7…`. **Conclusion:** the tool over-counts relative to this ledger's records by **at least 6**; the true over-count is **not derivable** without repairing the harvester and rebuilding the index (the auditor's heuristic probe flagged more candidates but also produced false positives, so no figure beyond 6 is stated). 212 therefore stays the tool's own count on its own frozen basis, neither a floor nor a ceiling on this ledger's records.

### 2.5 What can be stated on the ledger's records at `03c93c77`

| Statement | Composition | Value |
| --- | --- | ---: |
| **Floor:** the 2026-10-02 named set carried forward | 35 (`verify_ground_truth.py` `LIMB_A` 19 + `LIMB_B` 5 + `LIMB_C` 11, union 35 — the tool's encoding of the 2026-10-02 derivation) − 2 (both setup pages in `LIMB_C`: later recorded acceptance at `e6fc8d24`, empty `numstat`) + 7 (reader pages added after `d6e48418`, pending under the new-page rule, none with a recorded full-page acceptance) | **at least 40** |
| **Ceiling on accepted** | 609 reader pages − at least 40 pending, under the ledger's accepted-unless-pending convention | **at most 569** |
| Exact pending count | — | **not derivable** |

- **Not a re-run of the 2026-10-02 audit.** The carried-forward set does not re-apply the >10-line limb to pages edited since `d6e48418`: `git diff --numstat d6e48418 03c93c77 -- '*.md' | wc -l` → **44** Markdown paths changed or added, none re-measured here. Example: `docs/README.md` → `83 60` since `d6e48418`, and the ledger's own keeper row (`:3146`) already records "`docs/README.md` changed 81 added / 60 deleted = 141 lines, far past 10" with no acceptance conferred. A genuine re-run could only raise the floor.
- **No later recorded acceptance for the 33 carried pages:** the ledger's added lines since `d6e48418` (`git diff d6e48418 03c93c77 -- <ledger> | grep '^+'`) record acceptance only for the two setup pages; the rest are "declines", the 2026-10-03 note's quotations, or rule text. `docs/evidence/documentation/` gained only three process notes; `stated-acceptances.json` and `acceptance-index.json` each have one commit, `1cb61f3a` (PR #629).
- **One carried page cannot be re-measured in a fresh clone:** `cloud-security-baseline-reviewer/SKILL.md` is carried on the ledger's 2026-10-02 determination (its correction section keeps all ten rows) although the tool reports it `cannot_decide`.
- **Not nested with the tool:** 10 of the 33 carried index pages are outside the tool's 212 (9 with no recorded index acceptance, 1 undecidable). The two bases answer different questions and are not to be added, subtracted or merged in the note.

### 2.6 Effect of the planned edits on the instrument; the wording hazard

- Both edited pages are `null` rows in `acceptance-index.json` (`no_recorded_acceptance` bucket), so editing them cannot change `check_index.py`'s summary or pending set.
- `build_index.py --ref 03c93c77… --candidates` (no `--write`; working tree at base) prints counts `675 / 1 / 65 / 609 / 609 / 437 / 172 / 3 / 489 / 433 / 43 / 13` (`tracked_markdown … stated_candidates`); saved as `plan-evidence/build_index_readonly_candidates.txt` (the auditor's `audit-evidence/build_index_candidates_base.txt` is the same run). `harvest_tracker` reads the tracker from the **working tree**.
- **Hazard (re-verified with the harvester's own functions):** `ACCEPT_RE` and `RETENTION_RE` match per sentence or per table cell with no negation handling. Harvested: `` `docs/delivery-workflow.md` is not accepted at `03c93c77`. `` → (`accepted`, `docs/delivery-workflow.md`, `03c93c77…`); `` It keeps no acceptance for `docs/roadmaps/aegis-backlog-forecast.md` at `03c93c77`. `` → (`keeps no acceptance`, forecast); `` `iac-reviewer/SKILL.md` was not accepted at `03c93c77`. `` → resolves through `PATH_HINTS` to `.claude/skills/iac-reviewer/SKILL.md`. **Not** harvested: the same sentence with a `](../evidence/…)` link (does not resolve), and a sentence with a backticked path and "recorded acceptance revision" (no verdict match: "acceptance" does not match `accept\b`). A harvested sentence would act, on the next rebuild, as a recording of acceptance — a ledger-keeper-only act under AEGIS-APR-101.

### 2.7 Protected paths, CI scope and baselines

- `gate-guard` pattern (`.github/workflows/validate-skills.yml`, job `gate-guard`) matches neither `docs/roadmaps/…` path. `CONTRIBUTING.md:238-251` security-relevant surfaces include none of them. Security-relevant surface for a later PR: **No**; `MG5` not applicable on its own scope clause.
- No test or script guards these pages specifically (`git grep -n -E 'roadmaps/|readability' -- scripts/*.py scripts/ci scripts/tests/*.py` → no hits); the CI link-check step covers them.
- **CI on a docs-only PR** (`.github/workflows/validate-skills.yml`): `validate-skills` and `gate-guard` always run; `windows-offline-checks` (`if: … needs.changes.outputs.offline == 'true'`) and `tools-tests-linux`/`-windows` (`… tools == 'true'`) are skipped because no path is under `tools/` or a pip lock file. The `validate-skills` job runs, besides the K-checks: hash-locked `pip install`/`pip check`/`pip freeze`, `scripts/ci/check-environment.py`, BER self-check, the full offline BER suite, Scenario A in PowerShell Core, DCO.
- **Local baselines at `03c93c77`** (Python 3.13.16; CI pins 3.14): `validate-skills.py` → `OK: 195 skill(s) valid, 0 warning(s)`; `test_validator.py` → `OK: 181 …`; `test_audit_skill_contracts.py` → `OK: 76 …`; `test_markdown_links.py` → `OK`; `test_offline_ci.py` (scratch `TMPDIR`) → `OK (skipped=1)`; CI page-set link check → `checked paths: 619`, `files: 619 links checked: 3191 anchors checked: 839 broken: 0 dead: 0 external-skipped: 1809`; BER self-check `python3 -B -m tools.behavioral_eval_runner self-check` → `"self_check": "PASS"`, exit 0; BER suite `python3 -B -m unittest discover -s tools/behavioral_eval_runner/tests -p 'test_*.py'` → `Ran 1094 tests`, `FAILED (errors=2, skipped=13)` — both errors are sandbox process-control cleanup (`test_process_control…test_watchdog_kills_synthetic_child_tree`, `test_review_blockers…test_posix_background_child_terminated_after_leader_exit`: "pgid … still has live members after 25 checks"), present at the unchanged base; `check-environment.py` → exit 1 `ModuleNotFoundError: No module named 'openai'` (hash-locked CI dependencies not installed locally); `which pwsh` → nothing.

---

## 3. Classification, blast radius, paths

```
CHANGE CLASSIFICATION (change-classification-gate)
Deliverables:    D1 ledger forward-dated note; D2 forecast forward-dated note
Classes:         D1 docs-only; D2 docs-only (Markdown prose, not agent-instruction files)
Governing class: docs-only
Approval path:   none (no approval class). Merge authority is Stage G's own MG4 check (the owner's
                 2026-10-07 merge instruction is recorded in BRIEF-COMMON.md for that agent to verify).
Validation plan: docs-only floor (links/paths resolve + independent review) PLUS instrument-invariance
                 checks AC-5/AC-6 (the ledger is build_index.py's harvest source) PLUS the local subset
                 of the CI checks in section 7, with the rest pre-listed for Stage E.
Scope contract:  exactly two files: docs/roadmaps/aegis-documentation-readability-backlog.md,
                 docs/roadmaps/aegis-backlog-forecast.md. Any other path → stop, return to Stage A.
```

**Blast radius.** Two Markdown pages, both already **pending** (ledger and forecast are in `LIMB_C`; both `null` in the index). No code, CI, approval, skill or instruction file. Readers: maintainers and agents reading either "Start here". Machine readers: `build_index.py` harvests the ledger (guarded by AC-5/AC-6). Inserting lines near the top of the ledger displaces two sets of recorded line references, neither of which is validated: `acceptance-index.json` `rules` ranges (the 2026-10-03 note measured 0 of 11 still resolving; `verify_rule_lines` checks only `end ≤ len(lines)`) and the 19 `tracker_line` fields of `stated-acceptances.json` (used only as an evidence label, `build_index.py:495`). New anchor added; no existing anchor changes. Rollback: revert the single commit.

**Exact files and sections (additions only — 0 deleted lines):**

| File | Insertion point at base (blob `4ac2c264…` / `703b8f8b…`) | Section |
| --- | --- | --- |
| `docs/roadmaps/aegis-documentation-readability-backlog.md` | After line 17 ("…as the dated snapshot it is.)"), before line 19 `### Premises correction — appended 2026-10-03, measured at c3527560`. | New `### Current-count reconciliation — appended <YYYY-MM-DD>, measured at 03c93c77` (anchor `#current-count-reconciliation--appended-<YYYY-MM-DD>-measured-at-03c93c77`). |
| `docs/roadmaps/aegis-backlog-forecast.md` | After line 15 (paragraph ending "See the [catch-up checkpoint after #554](…)."), before line 17 `**Earlier reading at the 2026-09-28 catch-up checkpoint after #491:**`. **Not** between lines 11 and 13 (would retarget the 2026-10-01 note's "the block immediately below"). | One blockquote paragraph, bold lead `**Readability figures — superseded-state note appended <YYYY-MM-DD>.**` |

`<YYYY-MM-DD>` = implementer's `date -u +%F` on the day of the edit.

---

## 4. Alternatives considered

| Option | Why viable | Drawback | Verdict |
| --- | --- | --- | --- |
| A. Two notes (this plan) | Removes the false forecast statement; makes the ledger's top reading current; answers the `unsure` with verified cases; states only figures supported on the ledger's records. | ~90–120 ledger lines; both pages stay pending (already pending). | **Recommended.** |
| B. Forecast-only pointer to the 2026-10-03 note | Smallest diff. | Points readers to a note whose 218/390 are tool-basis figures beside the word "floor", and whose `unsure` is now answerable. | Fallback if Stage B judges A out of proportion. |
| C. No change | The ledger already quotes 212 and "not derivable". | The forecast states stale figures as current with no pointer. | Rejected. |
| D. Repair the harvester / rebuild the index / add `stated-acceptances.json` rows | Would let the tool see the six cases and the seven new pages. | Writes under `tools/` (approval/evidence tooling is a CONTRIBUTING security-relevant surface); adding acceptance rows is a recording act (keeper only); needs its own plan and review. | Out of scope; recorded as owed. |

---

## 5. Reconciliation (`source-of-truth-reconciler`)

```
RECONCILIATION REPORT
Conflicts:
  C1: S4/S4b forecast "live totals … 16", "zero known pending"  vs  ledger S2/S3 and the carried-forward floor (≥40)
      Type: IS. Verdict: repo state wins — precedence rule 2 (actual repo state, re-measured now) over rule 5
      (superseded dated text). Annotate forward.
  C2: S1 ledger "16 pending", "584 accepted" (dated 2026-09-30)  vs  ≥40 pending / ≤569 accepted at 03c93c77
      Type: IS. Verdict: as C1; S1 is honestly dated — forward pointer, no rewrite.
  C3: S3 "212 is not guaranteed to be a floor … unsure"  vs  six verified pages the tool counts pending whose later
      recorded acceptance has empty numstat
      Type: IS. Verdict: measurement answers the unsure — the tool over-counts relative to the ledger's records by at
      least 6; magnitude not derivable without harvester repair + rebuild. S3's 218 and "at most 390" are tool-basis
      figures, not a floor/ceiling on the ledger's records. Forward-note; no corrected tool-based bound is published.
  C4: S2 "floor is 35 named pages" (d6e48418)  vs  two later recorded acceptances in that set + seven later pages
      Type: IS. Verdict: the named set carried forward gives at least 40 at 03c93c77 — explicitly not a re-run of the
      2026-10-02 audit (44 Markdown paths changed since d6e48418 were not re-measured). Forward-note.
  C5: Should the ledger's pending floor follow the index's decision procedure (index precedence)?
      Type: SHOULD. Verdict: NONE — owner decision; S5 forbids approving it under AEGIS-APR-101. Held UNRESOLVED;
      the note reports the ledger-record floor and the tool count separately, each attributed.
Assumptions surfaced:
  A1: The keeper's two rows (ratified by AEGIS-APR-101) are valid recorded acceptances. Risk if wrong: the floor
      rises to at least 42 and the verified over-count falls to at least 5.
  A2: The limiting assumption is the harvester's coverage, before and after d6e48418 — not the post-d6e48418 search.
      The six verified cases are a lower bound on the over-count; the remainder is unknown. Risk: none to the
      statements as worded ("at least 6", "not derivable").
  A3: .coord/proc08-sweep-2026-10-03.md is a reader page under the ledger's class rule (tracked .md less the
      generated report less scripts/ fixtures). Risk if wrong: the floor is at least 39.
  A4: verify_ground_truth.py LIMB_A/B/C faithfully encodes the 2026-10-02 35-page set (union = 35; the ledger's
      keeper section confirms both setup pages were pending, "PR #542 returned both to pending"). Risk if wrong:
      the carried-forward figure changes.
  A5: The 33 carried pages have no later recorded acceptance (section 2.5 check). Risk if wrong: floor falls by
      the number found.
  A6: Acceptances existing only in pull-request comments never recorded in git are invisible; by the ledger's
      convention they are not recorded acceptances. Risk: none to statements made "on the ledger's records".
Stale sources to fix: forecast :15 and :46-52 (forward note D2); ledger :3-17 (forward pointer D1); S3's 218/390/unsure
  (forward-noted inside D1).
Blocked: C5 only — owner question below; not blocking for RCF-1.
```

**Owner choice for C5 (for the coordinator to relay; RCF-1 does not need the answer).** Terms: the *index* is `tools/readability_acceptance/acceptance-index.json` plus `check_index.py`, the machine-run form of the ledger's >10-lines-or-new-section rule; *precedence* means which artifact the ledger's floor follows when they differ. Options: (1) **adopt the tool's determinations into the ledger's floor once repaired** — pro: one figure from a command; con: today's harvester misses at least six recorded acceptances (multi-line statements, per-cell table rows, short names and `../` links, keeper rows), so adopting it now would publish a known over-count; cost: a `tools/` harvester fix, a rebuild and their own review. (2) **keep the ledger's named-set floor as the ledger's figure** — pro: no new authority; con: "at least 40" understates the likely workload and needs a manual re-run to tighten. (3) **hold UNRESOLVED**, both reported and attributed — what this plan does; pro: truthful now, no authority taken; con: two figures for readers. **Recommendation: hold UNRESOLVED until the harvester is repaired and the index rebuilt.** Evidence that would change it: a rebuilt index whose harvester records the multi-line, per-cell, short-name/relative-link and keeper acceptances — so that the six pages in section 2.4 leave its pending list — and whose `verify_ground_truth.py` passes. **One question:** *"Once the acceptance index's harvester is repaired and the index rebuilt, should the readability ledger's pending floor follow the index's decision procedure — yes, no, or decide later?"* No answer by itself authorizes any edit.

---

## 6. Exact wording intent

### 6.1 Ledger note (D1) — required elements, in this order

1. **Scope line and first-use definitions (CONTRIBUTING "Write documentation for a new reader", rule 2).** Bold first sentence: the note re-measures the readability position at commit `03c93c77a05e89d082f93c91b23dffabb332373c` and points to the current reading; it adds no page, confers or records no acceptance, changes no counting rule, approves nothing about the index's precedence, and rewrites no dated text. Define in plain words at first use: *pull request (PR)*; *commit SHA* (the 40-character Git object ID; short forms are its leading characters); *the acceptance index* (`tools/readability_acceptance/acceptance-index.json`, a per-page record of the revision at which each page was last accepted full-page, harvested by `build_index.py` from this ledger and the evidence records); `check_index.py` (the read-only script that applies this ledger's >10-lines-or-new-section rule to the index); *bound* (a provable minimum or maximum, not an exact count); *ledger keeper* (the recording-only role the owner ratified); *AEGIS-APR-101* (the owner approval register entry that ratified the keeper role and expressly did not approve the index's precedence or any changed counting rule — link the register anchor).
2. **Dated, not current:** the 16 (and the 13, 17, 18, 656/657 and 584 figures) in the paragraph above; the 35 of `## Correction to the pending floor — 2026-10-02` (measured at `d6e48418`); the 608/674, 218 and "at most 390" of the 2026-10-03 premises note (measured at `c3527560`). Link both later sections by anchor.
3. **Inventory at `03c93c77`** with the method named and the arithmetic closing `675 − 1 − 65 = 609`; the one page added since `c3527560` named (`.coord/proc08-sweep-2026-10-03.md`, PR #656).
4. **The tool, strictly attributed:** the exact command with `--ref` pinned to the 40-character SHA; its summary quoted (602 / 436 / 212 / 159 / 224 / 7; "NOT DERIVABLE from this procedure"); the 212-page set is identical at `d6e48418`, `c3527560` and `03c93c77`, i.e. it reflects the index's frozen harvest; the 7 undecidable rows name two revisions no remote-tracking ref contains. **212 is the tool's count on its own basis — not a floor or ceiling on this ledger's records.** (Do not mention the shallow/unshallow comparison.)
5. **The 2026-10-03 `unsure`, answered:** yes — relative to this ledger's records the tool over-counts. Name the six verified pages with their recorded acceptance revision and PR, and the command test (`git diff --numstat <R> 03c93c77 -- <path>` empty; no added heading; listed pending by the tool). For the host feasibility page add that `e6fc8d24` is not an ancestor of the default branch and is reachable only through `origin/docs/readability-batch-b`. State that the over-count is **at least 6** and its size **not derivable** without repairing the harvester and rebuilding the index; therefore the 2026-10-03 note's 218 and "at most 390" are figures on the tool's basis, **not** a floor or ceiling on this ledger's records. Cite ledger evidence by PR and revision, not by line number (line numbers shift with this insertion).
6. **What this ledger's records support at `03c93c77`:** "the 2026-10-02 named set carried forward: 35 − 2 + 7 = **at least 40** pending" — say where the 35-set membership was read, why the two setup pages leave it, that the seven are new pages; that this is **not a re-run** of the 2026-10-02 audit (44 Markdown paths changed or added since `d6e48418` were not re-measured; `docs/README.md` as the example — 143 changed lines since `d6e48418`, and the keeper section already records 141 with no acceptance — so a re-run could only raise it); that one carried page (`cloud-security-baseline-reviewer/SKILL.md`) is carried on the 2026-10-02 determination although its drift cannot be re-measured in a fresh clone. Then **at most 569** accepted (609 − 40) under the accepted-unless-pending convention, so the paragraph above's 584 cannot be current. Say the floor and the tool's 212 are **different bases, not nested** (10 carried pages are outside the tool's set), and are not to be combined.
7. **Exact count:** "**not derivable**; this note asserts no exact count."
8. **Owner question held:** whether this ledger's floor should follow the index once repaired is the owner's decision, not this note's (quote AEGIS-APR-101's Scope FORBIDDEN sentence).
9. **Owed, not done here (`tools/` work needing its own plan and review):** the `build_index.py` re-run already named owed in the 2026-10-03 note; and the harvester's blind spots — statements wrapped across lines, page and verdict in different table cells, short names without `.md` and `../`-relative links, and keeper rows that carry no verdict word — with the six pages as the regression cases.
10. **Self-cost and side effects:** the note's own `git diff --numstat` (added, deleted 0) on this already-pending ledger; no acceptance conferred; the ledger stays **pending** its independent full-page re-read. One clause: like the 2026-10-03 note, the insertion moves the index's recorded rule line ranges and `stated-acceptances.json`'s `tracker_line` labels further (neither is validated; repaired only by the owed rebuild).

**Wording constraints (mechanically checked by AC-5):**
- No sentence and no table cell may contain `accepted`, `accepts`, `accept` (whole word, any case), `re-accepted`/`reaccepted`, or "keep/keeps/keeping … acceptance" **together with** a Markdown link to a `.md` file or a backticked `.md` path (including short paths such as `` `iac-reviewer/SKILL.md` ``, which the harvester resolves through `PATH_HINTS`). Use "recorded acceptance", "acceptance revision", "full-page acceptance". Do not quote the ledger's own verdict sentences next to a path; cite PR and revision instead.
- Every figure carries its revision and the command or named method that produced it; tool figures are attributed to the tool (CONTRIBUTING rule 7; delivery-workflow PROC-04).
- Plain language; descriptive heading; short paragraphs or a small table for the six pages; no new coded identifiers.
- **Reserved scope:** naming `docs/evidence/setup/issue-101-package-4a-host-feasibility.md` as a readability-count item is not reserved-scope work; the note must not describe that page's content, host findings or issue #101 status. No mention of, or figure from, the paused evaluation, rehearsal package, VMs/ISO, Stage 4B, BER calibration or provider spend. `03c93c77` appears only as the measured revision.

### 6.2 Forecast note (D2) — required elements

One blockquote paragraph, ≤ 18 wrapped lines: (1) dated bold lead; (2) the readability figures in this "Start here" section — the current-reading block's 656 / 584 / 1 / 55 / 16 and its appended note's tip 657, and the purpose paragraph's PR-dated page totals and "zero known pending" statements — are dated snapshots, not the current position (do not quote or touch the purpose paragraph's other content); (3) the current position is in the ledger's new subsection (link with anchor): exact pending count **not derivable**; on the ledger's records **at least 40** pages pending at `03c93c77`; the ledger's acceptance tool counts 212 on its own frozen basis, which over-counts relative to the ledger's records by at least 6 pages, amount not derivable; how the two relate is an open owner question; (4) this note re-estimates no hours, closes no five-merge window and changes no dated text; (5) it confers no acceptance and this page remains pending. First use in the note: expand any abbreviation it uses (or avoid "PR"/"SHA"; "revision `03c93c77`" suffices). No other figures. Same harvest-safe phrasing.

---

## 7. Checks the implementer must run (local subset of CI; record command + tell-tale output)

Run from the repository root at the implementation head; record base, head and `git rev-parse HEAD^{tree}`; record the Python version.

| # | Command | Expected |
| --- | --- | --- |
| K1 | `python -P -B scripts/validate-skills.py` | `OK: 195 skill(s) valid, 0 warning(s)` |
| K2 | `python -P -B scripts/tests/test_validator.py` | `OK: 181 gate self-test assertion(s) passed.` |
| K3 | `python -P -B scripts/tests/test_audit_skill_contracts.py` | `OK: 76 contract-audit self-test assertion(s) passed.` |
| K4 | `python -P -B scripts/tests/test_markdown_links.py` | `OK` |
| K5 | `python -P -B scripts/tests/test_offline_ci.py` (scratch `TMPDIR`) | `OK (skipped=1)` |
| K6 | `mapfile -t pages < <(git ls-files \| grep -v scripts/tests/fixtures/ \| grep '[.]md$'); python -P -B scripts/ci/check-markdown-links.py "${pages[@]}"` | `checked paths: 619`; `broken: 0 dead: 0`; anchors checked = 839 + the number of `#…` links the two notes add (count with a command) |
| K7 | `python -B -m unittest discover -s tools/readability_acceptance/tests -p 'test_*.py' -v` (no `-I`) — **extra: CI does not run it** | `Ran 7 tests … OK` |
| K8 | `python -I -B tools/readability_acceptance/check_index.py --json --ref HEAD` | 602 / 436 / 212 / 159 / 224 / 7 / 7; pending path set equal to base |
| K9 | `python -I -B tools/readability_acceptance/verify_ground_truth.py --ref HEAD` (baseline: `--ref refs/remotes/origin/main` = `03c93c77`) | exit 1, exactly the one pre-existing `cloud-security-baseline-reviewer` mismatch |
| K10 | `python -I -B tools/readability_acceptance/build_index.py --ref HEAD --candidates` (**no `--write`**) in the implementation worktree | counts block identical to `plan-evidence/build_index_readonly_candidates.txt`; `tracker-*` candidate lines equal **as a sorted multiset** after stripping the `:<line>` suffix of `evidence_source` |
| K11 | gate-guard regex (copied verbatim, `nocasematch`) over `git diff --no-renames --name-only -z 03c93c77...HEAD` | no match |
| K12 | `python -P scripts/check_dco.py --range "03c93c77..HEAD"` | exit 0 (`git commit -s`) |
| K13 | `git diff --numstat 03c93c77 HEAD` | two lines, deleted `0` on both |
| K14 | `python -B -m tools.behavioral_eval_runner self-check` | `"self_check": "PASS"`, exit 0 |
| K15 | `python -B -m unittest discover -s tools/behavioral_eval_runner/tests -p 'test_*.py'` (scratch `TMPDIR`) | same as base: `Ran 1094 tests`, at most the two named sandbox process-control errors; any other failure is a finding |

**Pre-listed Stage E `UNRUN` items (not runnable here; covered by the `validate-skills` CI job at the PR head):** hash-locked `pip install`/`pip check`/`pip freeze` (dependencies not installed locally); `scripts/ci/check-environment.py` (local exit 1, `No module named 'openai'`); Scenario A in PowerShell Core (`which pwsh` → nothing); K15's two sandbox errors if they recur. **For Stage G (`MG1`):** on a docs-only PR the `windows-offline-checks` and `tools-tests-*` jobs are *skipped* by the `changes` job's path filter — skipped is not failed, and not green either; record them as skipped by that filter.

---

## 8. Acceptance criteria

- **AC-1 Scope.** `git diff --name-only 03c93c77 HEAD` lists exactly `docs/roadmaps/aegis-backlog-forecast.md` and `docs/roadmaps/aegis-documentation-readability-backlog.md`; `git diff --name-status --diff-filter=ADR 03c93c77 HEAD` prints nothing.
- **AC-2 Additions only, proportionate size.** K13: deleted = 0 on both; ledger added ≤ 120 lines; forecast added ≤ 18 lines.
- **AC-3 Placement.** The new ledger heading is the first `###` after `## Start here — current reading` and precedes `### Premises correction — appended 2026-10-03…`. The forecast blockquote sits between the paragraph ending "See the [catch-up checkpoint after #554](…)." and `**Earlier reading at the 2026-09-28 catch-up checkpoint after #491:**`; nothing is inserted between the 2026-10-01 purpose note and the `**Current reading at the 2026-09-30…**` block.
- **AC-4 Ledger content.** Elements 1–10 of section 6.1 are present, including every first-use definition in element 1. Figures stated: 675 / 65 / 1 / 609; the pinned check_index command and 602 / 436 / 212 / 159 / 224 / 7; set identity at the three revisions; the six verified pages with revision, PR and the empty-numstat test (host feasibility with its reachability caveat); "at least 6", size not derivable; 218 and "at most 390" forward-noted as tool-basis; "at least 40" labelled as the named set carried forward and not a re-run, with the 44-path and `docs/README.md` facts; "at most 569"; "not derivable"; the C5 question left to the owner with AEGIS-APR-101 quoted; the four harvester blind spots as owed work. **Absent:** any figure 211, 217, 218 (except when quoting the 2026-10-03 note), 228 or 391; any "exactly one". Every figure reproduces by its stated command or method (the auditor re-runs them).
- **AC-5 No acceptance recorded, by wording.** A script imports `TRACKER_ROW_RE`, `sentence_split`, `verdict_in` and `clause_links` from `tools/readability_acceptance/build_index.py` (`-I -B`, `sys.path` insert, no `__pycache__`), takes the `+` lines of `git diff -U0 03c93c77 HEAD` for each file (excluding `+++`), scopes each line as `harvest_tracker` does (per cell for `TRACKER_ROW_RE` rows, else per sentence), and reports (a) scopes with a verdict **and** a resolved tracked path → **0**; (b) the conservative superset — scopes matching `(?i)\b(re-?accepted|accepted|accepts|accept)\b` or `RETENTION_RE` **and** containing a `.md` link or backticked `.md` path → **0**. Script and output saved.
- **AC-6 Instrument invariance.** K8 summary and pending set equal base (only `compared_ref` differs); K10 counts block identical and tracker candidates equal as a sorted multiset with `:<line>` stripped.
- **AC-7 Forecast content.** Elements 1–5 of section 6.2 present; the scope covers the current-reading block, its appended note and the purpose paragraph's readability figures; links to the ledger anchor (resolves under K6); figures limited to the dated ones it names, "at least 40", 212 (attributed), "at least 6", and the revision; no 218/391/228; first-use rule met; the purpose paragraph's reserved-scope text not quoted.
- **AC-8 Checks.** K1–K7, K11, K12, K14 as expected; K9 and K15 unchanged from base; Stage E `UNRUN` list carried as pre-listed in section 7.
- **AC-9 No dated text rewritten, no acceptance, no C5 decision, no exact count.** Mechanical part via AC-1/AC-2/AC-5; the rest by reviewer reading.

**Criteria not verifiable at the implementation head:** none. Hosted CI at a PR head is Stage E/G evidence (`MG1`), not an AC of this local item.

---

## 9. Explicitly out of scope

- Accepting, re-reading or recording acceptance for any page (including the ledger's and forecast's owed full-page re-reads); acting as ledger keeper; adding rows to `stated-acceptances.json`.
- Deciding C5 (owner only; AEGIS-APR-101 forbids approving it under that entry).
- Any `tools/` change: harvester repair, `build_index.py --write`, index rebuild, the two unreachable revisions.
- Publishing any corrected tool-based bound (e.g. a "212 − k" figure) or the auditor's heuristic probe count.
- A re-run of the 2026-10-02 >10-line audit over the 44 paths changed since `d6e48418`.
- Rewriting any dated text: the ledger's opening paragraph, the 2026-10-02 and 2026-10-03 notes (including the latter's heading-versus-body tension), forecast checkpoints and its purpose paragraph, session-continuation evidence, execution metrics, session checkpoints.
- Forecast re-estimation or the missed five-merge windows since #554.
- Edits to `docs/README.md`, `README.md`, `CONTRIBUTING.md`, `AGENTS.md`, `CLAUDE.md`, `docs/delivery-workflow.md`, `docs/approvals/`, `.github/`, `scripts/`.
- The PROC-01 / open PR #633 citation in the ledger.
- Reserved scope (paused evaluation, rehearsal package, VMs/ISO, Stage 4B, issue #101 execution, BER calibration, provider spend, execution flags); the evaluation's source pin is not changed.
- For this local item: push, PR creation, merge, any GitHub write (later stages act under the owner instructions recorded in BRIEF-COMMON.md).

---

## 10. Risks

| Risk | Likelihood / impact | Mitigation |
| --- | --- | --- |
| R1 A note sentence is harvested as an acceptance on a future rebuild (keeper-only act) | Medium / high — the note must name six pages next to acceptance revisions | §6.1 constraints; AC-5 (harvester functions + conservative superset); AC-6. |
| R2 `origin/main` moves before implementation and changes an input | Medium / medium | Re-observe; if moved, re-run sections 2.2–2.5. Same figures → re-pin with a deviation flag. Any changed figure, new acceptance record or new over-count case that changes a stated figure → stop, return to Stage A. |
| R3 Readers combine "at least 40" and 212, or read either as exact | Medium / medium | Elements 4–8: different bases, not nested, not combined, exact count not derivable; 212 never called a floor. |
| R4 The over-count list is read as complete | Medium / low | "at least 6", "size not derivable" stated with the reason (harvester blind spots). |
| R5 Line insertion displaces unvalidated line references | Certain / low | Disclosed (element 10, §3); repaired only by the owed rebuild. |
| R6 Over-proportion | Medium / low | AC-2 caps; option B fallback. |
| R7 Separation of duty | Low / high | Planner holds A only; implementer, auditors, validator, reviewer and merger are each different agents; no keeper act occurs. |

---

## 11. Active-work ETA

- **Stage C:** 1.5–2.5 agent active hours (estimate, not a measurement): re-derive section 2, write both notes within the wording constraints, write the AC-5 script, run K1–K15.
- **This rev2:** start 2026-10-07T18:10:10Z; finish recorded in the hand-off report.

---

## 12. Skills (dogfood rule)

| Skill | Stage / agent | How applied | Result |
| --- | --- | --- | --- |
| `source-of-truth-reconciler` (`.claude/skills/source-of-truth-reconciler/SKILL.md`) | A PLAN rev2 / RCF-1 planner | Re-enumerated claims with anchors (added S4b); re-tested the auditor's counterexamples against the repository rather than accepting them; IS/SHOULD tags; precedence rule 2 over rule 5; assumptions with risk (A1–A6 rewritten); stale-source fixes as follow-up (this plan); SHOULD conflict held for the owner with a taught choice and one question. | C1–C4 IS verdicts revised (C3, C4 per B-1/B-2); C5 held UNRESOLVED. |
| `change-classification-gate` (`.claude/skills/change-classification-gate/SKILL.md`) | A PLAN rev2 / RCF-1 planner | Re-checked the class against the unchanged two-file scope; validation plan widened to the CI-subset list. | docs-only; no approval class; two-file scope lock. |
| Considered, not used | — | `reviewable-diff-discipline` (MANUAL-ONLY, not named by the owner); `ai-task-decomposer`, `chat-backlog-reconciliation`, `risk-tiered-validation-selector` (out of this stage's scope). No installed skill owns writing a plan; Stage A is procedural. | — |

## 13. Stage handoff

1. **Decision IDs:** binds `SD-A` (rev2 seeks COMPLETE: what, why, blast radius, paths, ACs, classification, not-verifiable declaration "none"). `SD-B: REVISE` on rev1 (`dcd7dc9f…5be`) is the input; rev2 changes no `MG`/`SD` decision. AEGIS-APR-101 binds.
2. **Changed files:** none in the repository. Created only under `…/scratchpad/rcf/`: `PLAN-rev2.md` and new `plan-evidence/` files (`check_index_d6e48418.json`, `ber_selfcheck.base.txt`, `ber_suite.base.txt`, `check_env.base.txt`). `PLAN-rev1.md` not modified. Working tree clean (`git status --porcelain | wc -l` → `0` after every run).
3. **Proven invocation:** section 2 and `plan-evidence/`.
4. **Deviation flags:** none from the brief. The brief's token "APPROVE" for `SD-B` is not a defined token; `ACCEPT`/`REVISE` apply (coordinator confirmed).
5. **Continuation:** Stage B audits this exact file by its sha256. Stage C starts at sections 3 and 6 on base `03c93c77` (re-observe first) and records base, head and tree. **For the PR stages (not this local item):** the PR body owes the "Audited plan revision" field (the sha256 of the revision that received `SD-B: ACCEPT`, `.github/pull_request_template.md:18`), the "Aegis skills used" table with a row per stage (`:41`), the Security-relevant surface answer **No** (`:62`; both paths outside `gate-guard` and `CONTRIBUTING.md:238-251`), the `## Reconciliation witness` with all 8 numbered sites `unchanged-and-verified` (`:71`; no `docs/delivery-workflow.md` or `AGENTS.md` edit), and CONTRIBUTING rule 6 (both edited pages named as still pending). Stage E carries the pre-listed `UNRUN` items in section 7. Stage G verifies its own authority (`MG4`) against the owner's verbatim merge instruction recorded in BRIEF-COMMON.md, and treats skipped advisory jobs as skipped, not green. A failing check routes back through C → D → E → F at the new head per the owner's failure-handling instruction; it never authorizes skipping or waiving a check.
