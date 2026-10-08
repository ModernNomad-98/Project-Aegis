## Stage E VALIDATE — RCF-1, PR #677

**Disposition: `SD-E: INCOMPLETE — UNRUN LISTED`**. This disposition is **affirmative**: each of the 3 checks not run here was run by the named CI job `validate-skills` at this exact head, with evidence (condition (a) of `SD-E` in `docs/delivery-workflow.md`). It is not `PASS`, because those 3 checks did not run here. `UNRUN` is never `PASS`.

- **Head:** `ccf3fc22001b277dd62d1185d939e23a7977e299`
- **Tree:** `6afd2ea75e40985cbba7985846b63f36580050b5`
- **Base:** `03c93c77a05e89d082f93c91b23dffabb332373c`
- **Head checks:** `git rev-parse HEAD HEAD^{tree}` gave the values above at 18:51:26Z and again at 18:55:12Z. GitHub `pulls/677` `head.sha` = `ccf3fc22…7e299`. `git ls-remote` shows that `refs/pull/677/head` and the branch both equal `ccf3fc22…` at the end. The working tree is clean (`git status --porcelain | wc -l` → `0`).
- **Validator:** RCF-1 Stage E agent. I did not plan, audit or implement this change.
- **Predecessor:** `SD-D: ACCEPT` on this head (`IMPL-AUDIT-1.md`).
- **Local environment:** Python 3.13.16. CI uses 3.14 (the hosted run used 3.14.8).

### Skills used

| Skill | How it was applied |
| --- | --- |
| `risk-tiered-validation-selector` | **Selection only, as its contract requires.** Input was `git diff --name-status 03c93c77 ccf3fc22`: `M docs/roadmaps/aegis-backlog-forecast.md` and `M docs/roadmaps/aegis-documentation-readability-backlog.md`. Neither file is on its "never docs-only" list, so the tier is **docs-only**. The selector does not run checks. I still ran every repository check that can run here, because the plan's K1–K15 and the `validate-skills` gate job are not reduced by tier. Running the checks is procedural (`docs/delivery-workflow.md`, Stage E row of the skill map). |
| `ci-failure-classifier` | Applied to the hosted logs after downloading them to disk, and to the local K15 failures. Hosted run verdict: **CLEAN**, with notes below. Local K15: **INFRASTRUCTURE**, meaning the sandbox's process-group cleanup. The classifier fetches nothing itself; I downloaded the logs as Stage E evidence. |

### Local checks at `ccf3fc22`

Evidence for each check (the command, its full output and exit status) is in `…/rcf/validate-evidence/`.

| # | Check | Result | Verdict |
| --- | --- | --- | --- |
| K1 | `python -P -B scripts/validate-skills.py` | `OK: 195 skill(s) valid, 0 warning(s)`, exit 0 | PASS |
| K2 | `scripts/tests/test_validator.py` | `OK: 181 gate self-test assertion(s) passed.` | PASS |
| K3 | `scripts/tests/test_audit_skill_contracts.py` | `OK: 76 contract-audit self-test assertion(s) passed.` | PASS |
| K4 | `scripts/tests/test_markdown_links.py` | `Ran 23 tests` `OK` | PASS |
| K5 | `scripts/tests/test_offline_ci.py` (scratch `TMPDIR`) | `Ran 38 tests` `OK (skipped=1)` | PASS |
| K6 | CI page-set link check, run as the CI step does | `checked paths: 619`; `links checked: 3193 anchors checked: 843 broken: 0 dead: 0` | PASS |
| K7 | readability tool tests (`tools/readability_acceptance/tests`; CI does not run these) | `Ran 7 tests` `OK` | PASS |
| K8 | `check_index.py --json --ref HEAD` | 602 / 436 / 212 / 159 / 224 / 7 / 7; `exact_pending_count` "NOT DERIVABLE". Compared with a base run, only `compared_ref` differs in the summary; the 212 pending rows are equal. | PASS (equal to base) |
| K9 | `verify_ground_truth.py --ref HEAD` | exit 1, with one mismatch: `cloud-security-baseline-reviewer` revision `65bacc7d6b85` is "contained by no remote-tracking ref" | **FAIL locally, identical to base**: the base run gives exit 1, and 50 vs 50 output lines with 0 differing. Pre-existing; the plan expected this result. |
| K10 | `build_index.py --ref HEAD --candidates`, without `--write` | The counts block is identical to base (675 / 1 / 65 / 609 / 437 / 172 / 3 / 489 / 433 / 43 / 13). 550 vs 550 lines. The lines are equal as a sorted multiset once `:<line>` is stripped and whitespace collapsed; they differ in raw order and padding, as the plan expected. | PASS |
| K11 | gate-guard regex, read verbatim from the workflow, `nocasematch`, over `03c93c77...ccf3fc22` | `files=2 matches=0`. Controls: `scripts/x.py` and `.github/workflows/a.yml` both MATCH; `docs/x.md` does not. | PASS |
| K12 | `scripts/check_dco.py --range 03c93c77..ccf3fc22` | `OK: 1 commit(s) checked, all signed off or exempt.` | PASS |
| K13 | `git diff --numstat` | `15 0` forecast; `120 0` ledger. `--name-status` shows `M` on both files only. | PASS |
| K14 | `python -B -m tools.behavioral_eval_runner self-check` | `"self_check": "PASS"`, exit 0 | PASS |
| K15 | BER offline suite (BER is the Behavioral Eval Runner; scratch `TMPDIR`) | `Ran 1094 tests` `FAILED (errors=2, skipped=13)`. Both errors are "pgid N still has live members after 25 checks": `test_process_control…test_watchdog_kills_synthetic_child_tree` and `test_review_blockers…test_posix_background_child_terminated_after_leader_exit`. | **FAIL locally, identical to base**: the base run gives the same two tests, the same cause, and `FAILED (errors=2, skipped=13)`. This is a local failure, **not** `UNRUN` (plan-audit N-2). Classified as **INFRASTRUCTURE** (the sandbox's process-group cleanup), because `git diff --name-only 03c93c77 ccf3fc22 -- tools scripts .github requirements*.txt` → `0` and both tests print `... ok` in the hosted run on the same tree. The governing result is hosted `CHECK ber: exit 0`. |

**Base comparison.** I created a temporary detached worktree at `03c93c77` (tree `6cd7de29…`) under the scratch folder, ran K8, K9, K10 and K15 there, then removed it with `git worktree remove --force` and `git worktree prune`. `git worktree list` now shows only the main checkout.

### UNRUN here (Stage E unrun record), each covered by CI at this exact head

| Check | Why it was not run here | What resolves it: CI evidence at `ccf3fc22` |
| --- | --- | --- |
| Hash-locked `pip install` / `pip check` / `pip freeze` | The CI lock is not installed here, and installing it would change the host environment. The interpreter is 3.13 and CI pins 3.14. | `validate-skills` job: the install step succeeded; `No broken requirements found.`; `CHECK dependencies: exit 0` |
| `scripts/ci/check-environment.py` | It exits 1 at import with `ModuleNotFoundError: No module named 'openai'`, before any check runs. | `CHECK environment: exit 0` |
| Scenario A acceptance in PowerShell Core | `which pwsh powershell` finds nothing (exit 1). | `PASS - all 106 test(s) passed (host: /opt/microsoft/powershell/7/pwsh)`; `CHECK acceptance-core: exit 0` |

**Forward duty, from the `SD-E` definition:** `SD-F` must accept this unrun list as part of its review, and `SD-G`'s receipt must record it.

### Hosted CI: run `37667969180` (workflow `validate-skills`, event `pull_request`, attempt 1)

**Run-level state:** `status: completed`, `conclusion: success`, `head_sha: ccf3fc22001b277dd62d1185d939e23a7977e299`. I read this from `actions/runs/37667969180` itself, not from job status alone.

**What CI tested:** the run's checkout SHA is the synthetic merge commit `3e171c4c1c07…`. Its parents are `03c93c77…` and `ccf3fc22…`, and its tree is `6afd2ea7…`, the **same tree as the head**. So CI tested exactly the head's content.

`get_check_runs` on the head returns 6 check runs, all from this run. The head has 0 commit statuses.

| Job | Status | Conclusion |
| --- | --- | --- |
| `validate-skills` (required) | completed | **success**. Every step succeeded, including DCO (`OK: 1 commit(s) checked`). |
| `gate-guard` (required) | completed | **success**: "No merge-gate or enforcement-surface files modified." It lists the same 2 files as K11. |
| `changes` | completed | **success** |
| `windows-offline-checks` | completed | **skipped** |
| `tools-tests-linux` | completed | **skipped** |
| `tools-tests-windows` | completed | **skipped** |

**The 3 skipped jobs.** They are skipped by the `changes` path filter: they run only when the change touches `tools/` or the requirements lock, and K11/K13 show only 2 `docs/roadmaps/` files changed. I did not read the filter's output values in the log, so the link between the filter and these skips is inferred from the `if:` conditions and the file list. **Skipped is neither failed nor green.** Stage G should record them as skipped under this filter (plan §7, `MG1`).

**The `validate-skills` job log, step by step** (downloaded with `gh api …/jobs/112951998232/logs`; 4783 lines):

- `CHECK ci-tests` exit 0 (`Ran 38` `OK (skipped=1)`)
- `validator-tests`: 181 OK
- `skills`: 195 OK
- `contract-audit-tests`: 76 OK
- `markdown-links`: 23 OK
- `markdown-link-corpus`: 619 paths, `broken: 0 dead: 0`
- `ber-self-check` PASS
- `ber`: `Ran 1094 tests` `OK (skipped=5)`
- `acceptance-core`: 106 PASS

**Classifier scan of the green run: CLEAN.**

- **6 skip messages** (1 ci-tests, 5 BER). Each is platform-scoped, for example "Windows-only" or "Windows 8.3 aliases only". None hides this host's result, so none is `SKIPPED-RUNTIME`.
- **Scenario A has one Windows-only case** reported as `[SKIPPED] … explicitly NOT counted as a pass`.
- **`test_posix_background_child…` prints a `ResourceWarning`** and then `ok`. It is a warning, not a failure.
- **No `Traceback`, `ERROR:` or `FAIL:` lines** matched in the log.

**Not investigated:** local K15 reports skipped=13, while CI reports skipped=5. The plan's K15 command is not verbose, so the local skip reasons are not in the evidence. The difference is environment-dependent and recorded here. The governing result is the hosted run.

### Not done

- No file edits in the repository, no push, no approvals, no merge.
- No `build_index.py --write`.
- No reserved-scope work.
- One GitHub write: this comment.

---
_Generated by [Claude Code](https://claude.ai/code)_
