# L1 — CI, workflows and merge gates (OPT1-AUDIT)

Lane: L1. Repository: `/home/user/Project-Aegis`, detached at `7d1d05e8170254ae60e8deb175c74e244a284a80`
(`git rev-parse HEAD`). Role A (all four source-package landmarks present). Read-only: `git status --short | wc -l` → `0`
at the end of the audit. No `--write` run, no GitHub writes.

Start: `2026-10-07T20:34:45Z` (`date -u`). Finish: see the end of this file. I did not state an active-work ETA when I started,
so there is nothing to compare the elapsed time against.

## Skills used

| Skill | How it was applied |
| --- | --- |
| `risk-tiered-validation-selector` (`.claude/skills/risk-tiered-validation-selector/SKILL.md`) | Took each change class (harvester repair, index regeneration, ledger-only edit, CI wiring), read its changed paths, and mapped them through the live `changes` filter and `gate-guard` regex to the jobs that run. Took job costs from real run durations. Found a fail-open: a change to the workflow alone skips the advisory jobs. |
| `context-co-update-ci-gate` | Used its design checklist to judge the coordinator's possible "index check in CI to flag drift". Checks were important-path scope, a declared escape hatch, fail-closed on errors, interaction with the aggregate or required checks, and wiring as a handoff. Design assessment only; nothing was wired. |
| `ci-failure-classifier` | Duration-first reading of the runs for #675, #676 and #677 plus the push to main. Classified the cancelled jobs in #675 attempt 1 as INFRASTRUCTURE. Flagged that `check_index.py` always exits 0, so a CI step running it would always pass and decide nothing (the classifier's SKIPPED-RUNTIME class). |

I did not invoke `ci-pipeline-architect`, which is MANUAL-ONLY. The wiring options below are inputs for whoever owns that decision. They are not a pipeline design.

## Answers to the brief's questions

**(a) What the repair PR and the regeneration PRs trigger.** A PR that touches only `tools/readability_acceptance/**`, or that plus `docs/**`:

- It runs all six jobs: `changes`, `validate-skills`, `gate-guard`, `windows-offline-checks`, `tools-tests-linux` and `tools-tests-windows`.
- CI takes about 3.8–4 minutes of wall time per pushed head. A docs-only PR takes about 80 seconds.
- `gate-guard` stays **green**, so no owner exception is needed.
- None of those jobs exercises the readability tool. Its own tests are UNRUN in CI.

A ledger-only PR (C2) stays on the docs-only fast path: `changes`, `validate-skills` and `gate-guard`, about 80 seconds.

**(b) Adding the index check to CI.** It can work, but only under conditions the current tool and workflow do not meet:

- The job must use `fetch-depth: 0` and `--ref HEAD`.
- It cannot go in a gate job unless `tools/readability_acceptance/` becomes protected. That would push every regeneration PR through `gate-guard`.
- `check_index.py` cannot fail. `verify_ground_truth.py` fails permanently today.
- `build_index.py` is clone-dependent.
- Runtime is not the problem: about 9 seconds locally.
- Under MG1, a drift check that fails on threshold crossings would block most unrelated docs PRs.

**(c) Does anything in CI read the ledger's figures or the index?** **No.** CI reads the ledger only as one Markdown page in the link-check corpus.

**(d) What Option 2 costs in CI terms.** Zero added CI. It also gets no machine check, which is the same as today.

## Evidence base: real CI runs (GitHub MCP, read-only)

Durations are each job's `started_at` to `completed_at`, from `actions_list list_workflow_jobs`. Run wall time runs from the first job's start to the last job's completion.

| Run (event, PR) | What the PR touched | `changes` | `validate-skills` | `gate-guard` | `windows-offline-checks` | `tools-tests-linux` | `tools-tests-windows` | Run wall time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 37667969180 (PR #677, head `ccf3fc22`) | `docs/roadmaps/*` only (two ledger and forecast files) | 8s | **76s** | 7s ✅ | skipped | skipped | skipped | **80s** |
| 37397337142 (PR #676, head `4bfe819d`) | `.github/workflows/validate-skills.yml` and `scripts/tests/test_offline_ci.py` | 8s | 147s | 7s ❌ (by design) | **skipped** | **skipped** | **skipped** | 150s |
| 37367151729 attempt 1 (PR #675, head `e6892461`) | `tools/aegis_delivery_control/**` (before #676, so no `changes` job) | — | 125s (started about 10 minutes after creation) | cancelled | cancelled | cancelled | cancelled | — |
| 37367151729 attempt 2 (same head) | same | — | (kept from attempt 1) | 4s ✅ | **189s** | **124s** | **228s** | **231s** (21:59:29→22:03:20Z) |
| 37672991237 (push `7d1d05e8`, the merge of #677) | every flag forced true | 4s | 98s | skipped (runs on PRs only) | 250s | 98s | 211s | 294s |

PR metadata comes from `gh api repos/.../pulls/N`, a read-only GET:

| PR | Opened | Merged | Open to merge |
| --- | --- | --- | --- |
| #675 | 20:01:24Z | 22:26:48Z | 2h25m |
| #676 | 22:32:46Z | 01:29:57Z | 2h57m, merged while `gate-guard` was red |
| #677 | 18:35:11Z | 19:14:33Z | 39m |

Repository settings come from a read-only `gh api repos/ModernNomad-98/Project-Aegis` call:

```text
"visibility":"public","delete_branch_on_merge":false
```

Branch protection could not be read: `gh api .../branches/main/protection` returned `HTTP 403`. The required-check list
(`validate-skills`, `gate-guard`; `enforce_admins` false) is therefore taken from `docs/delivery-workflow.md:520-549` and
`.github/workflows/validate-skills.yml:3-5`. Its live state is **unverified**.

## Findings

Ratings follow the brief: BREAKS, SLOWS, RISK, NEUTRAL or HELPS. "New C#" marks a proposed new condition.

| # | Finding | Rating | Mitigated by |
| --- | --- | --- | --- |
| F1 | A harvester-repair PR or regeneration PR confined to `tools/readability_acceptance/**` and `docs/**` does **not** trip `gate-guard`. No owner exception is needed. | NEUTRAL | New **C7**: keep both inside those paths |
| F2 | Every `tools/` PR runs all five working jobs. CI wall time is about 3.8–4 minutes per pushed head, against about 80 seconds for docs-only. That adds about 2.5 minutes per head to the repair PR and to every C3 regeneration PR. Under MG1 the merge agent must wait for the advisory jobs as well. | SLOWS (minor) | — (or a narrower filter, F9) |
| F3 | The jobs a `tools/` PR runs exercise **none** of `tools/readability_acceptance`, and its 7 tests are not discovered by CI. The repair and regeneration PRs get about 4 minutes of CI with zero coverage of the changed tool. | RISK | **C5** must cite local test and run output; optional isolated job (F8) |
| F4 | `build_index.py` is **not clone-independent**. In any clone without `65bacc7` (every fresh clone, and CI), it drops 6 stated rows: they flip from recorded and unreachable to `unknown`, and `stated_candidates` falls from 19 to 13. A regeneration done from a fresh clone silently changes rows, and a reviewer re-running the build in another clone gets different bytes. The script also mixes `ls-tree <ref>` with reads from the working tree. | RISK (BREAKS for any "rebuild equals committed" check) | New **C6**: deterministic, clone-independent build plus a reproducibility check |
| F5 | Wired as-is, the README's reproduce commands give one step that is always red and one that is always green. `verify_ground_truth.py` exits **1** today by design (the `65bacc7` mismatch, which cannot be repaired because the commit is lost). `check_index.py` **always exits 0**. Under MG1, a red non-required job blocks every PR it runs on. | BREAKS (if wired naively) | New **C8**: any CI step fails only on tool errors or irreproducibility, and prints the bound as information |
| F6 | A drift check that **fails** when pages cross the threshold would be red on most docs PRs. 41 of the last 50 merges to main touched a reader `.md` page, and 36 of 50 changed some `.md` page by more than 10 lines. Under MG1 that blocks unrelated PRs. Placed under the existing `tools` filter, it would run on only 3 of 50 merges and miss nearly every PR that causes drift. | BREAKS (failing design) / ineffective (`tools` filter) | **C8**; give the job its own filter on `*.md` and `tools/readability_acceptance/**` |
| F7 | Gate jobs may execute only gate-guarded paths (`test_offline_ci.py:419-425`). Putting the check in `validate-skills`, or making it a required gate, means adding `tools/readability_acceptance/` to `gate_pattern`. Then **every C3 regeneration PR trips `gate-guard`** and needs a per-PR owner disposition and an administrator merge. | BREAKS C3's "normal stages" flow (if made a gate) | Keep it a non-gate, isolated, informational job |
| F8 | Any CI wiring edits `.github/workflows/validate-skills.yml` and `scripts/tests/test_offline_ci.py` (the exact-list assertion on `TOOLS_LABELS`). Both are protected, so it costs one PR with a red `gate-guard` and an owner exact-head exception. The precedent, #676, took 2h57m from open to merge; how much of that was the exception is unknown. | SLOWS (one-off) | — |
| F9 | The `changes` filter does not force the advisory jobs when only the workflow changes: in run 37397337142 all three were skipped. A PR that adds an index-check step to a tools job would not run that step at its own head unless it also touches `tools/`. The step would first run after merge. | RISK | Touch `tools/` in the same PR, or add `.github/workflows/` to the filter (fail-closed) |
| F10 | History depth is fine in the gate-style jobs (`fetch-depth: 0` fetches all 634 branches plus `pull/N/merge`). The `tools-tests-*` jobs check out shallow. In a shallow checkout an index check fails: either it cannot resolve `--ref origin/main` (exit 2) or every row becomes `cannot_decide`. The default `--ref origin/main` would also check the base branch, not the PR. Runtime is negligible. | NEUTRAL (works with `fetch-depth: 0` and `--ref HEAD`) | Design detail for whoever wires it |
| F11 | Tagging under **C4** does not help the tool. Both scripts count reachability only through `refs/remotes/`, never `refs/tags/`. After C1, keeper row `e6fc8d24` is reachable **only** through `origin/docs/readability-batch-b`. CI fetches it today; deleting that branch would flip the row to `cannot_decide`. | RISK | Amend **C4**: preserve under a remote branch ref, or teach the tool to read `refs/tags/` (and verify that CI fetches tags) |
| F12 | Nothing in CI reads the ledger's figures or the index. Switching the official source breaks no check. It also gains no CI protection unless one is added. | NEUTRAL | — |
| F13 | Three statements in the CI documentation are stale since #676. `docs/offline-ci.md:28` says "Pull requests have no path filter". `:12-15` says to wait for all five jobs. PR template `:33-34` asks for the Windows jobs to be checked. On ledger-only PRs, the Windows and tools jobs are skipped. | NEUTRAL (not specific to Option 1) | Separate documentation fix |
| F14 | Every `tools/` PR is exposed to infrastructure flakes in the Windows advisory jobs. In #675 attempt 1, four jobs were cancelled at the same instant (20:16:30Z, after 15m01s) with no runner and no steps. That is INFRASTRUCTURE and matches the documented flake signature (`validate-skills.yml:64-65`). The re-run came 1h43m later, for an unknown reason. Docs-only PRs are not exposed. | RISK (latency) | — |
| F15 | Option 2: zero added CI, and ledger PRs stay on the 80-second path. Advisory regenerations, if any are made, cost the same about 4 minutes. The figures still get no machine check. | NEUTRAL / opportunity cost | — |
| F16 | Option 1, once F4 and F5 are fixed, makes cheap machine checks possible. A clone-independent reproducibility rebuild takes about 3 seconds, and an informational pending summary about 9 seconds, in an isolated job alongside `validate-skills` (76–147s). That adds no wall time. Option 2's hand-stated figure cannot have such a check. | HELPS | Needs C6 and C8 first |
| F17 | The tool needs no lock or dependency change: it imports only the standard library, so `requirements*` and Dependabot are untouched. It has been run on Python 3.13 locally; CI pins 3.14 (`validate-skills.yml:131`, comment `:120-130`), and the tool has not been run on 3.14. | NEUTRAL / small RISK | **C5** reviewer runs on 3.14, or CI does |

## Evidence

**E1, the gate-guard regex against candidate paths (F1, F7, F8).**

- Script: `scratchpad/opt1-audit/l1_gate_test.sh`. It extracts the live `gate_pattern` from `validate-skills.yml:520` and uses `shopt -s nocasematch`.
- Output: `free` for these paths:
  - `tools/readability_acceptance/{build_index.py, check_index.py, acceptance-index.json, README.md, tests/test_verify_ground_truth.py, tests/test_build_index.py, __init__.py, tests/__init__.py}`
  - `docs/roadmaps/aegis-documentation-readability-backlog.md`
  - `docs/approvals/APPROVAL_REGISTER.md`
  - `requirements-ci.in`
- Output: `PROTECTED` for these paths:
  - `tools/__init__.py`
  - `.github/workflows/validate-skills.yml` and `.github/workflows/readability-index.yml`
  - `scripts/ci/check-readability-index.py`
  - `requirements-ci.txt` and `requirements.txt`
  - a root-level `check_index.py`
- The tool's README also says the directory is "deliberately outside the gate-guard protected set".

**E2, the path filter (F2, F6, F9).**

- `validate-skills.yml:91-100` sets `tools=true` only on `^tools/`, and `offline=true` on `^tools/` or `requirements-ci.(in|txt)`. A push to main forces both to true.
- Over the last 50 first-parent commits on main (2026-10-02 to 2026-10-07):
  - 41 touched a reader `.md` page (excluding `scripts/`).
  - 36 had at least one `.md` page with more than 10 changed lines (per-merge `git diff --numstat`; an upper-bound proxy).
  - 3 touched `tools/`.

**E3, no CI reader of the ledger or the index (F12).**

- `grep -rlE 'readability_acceptance|acceptance-index|readability-backlog|documentation-readability' .github scripts tools/behavioral_eval_runner tools/aegis_setup tools/aegis_delivery_control | wc -l` printed `0`.
- The ledger is path 551 of the 619 pages that the link-checker step derives (`validate-skills.yml:219-226`).

**E4, the tool's own tests are not in CI (F3).**

- The only test commands in the workflow are for `tools/behavioral_eval_runner/tests` (`:229-230`, `:327-328`), `tools/aegis_setup/tests` and `tools/aegis_delivery_control/tests` (`:395-400`, `:446-455`).
- The tool's README says ".github/ is outside this change, so CI does not discover this directory yet".
- Run locally, `python3 -B -m unittest discover -s tools/readability_acceptance/tests` printed `Ran 7 tests in 0.018s OK`.

**E5, local timings.** Measured on 4 cores with Python 3.13.16 and git 2.43.0. CI runs git 2.55.0 on ubuntu-latest, and CI timings are **unverified**.

| Command | Wall time | Result |
| --- | --- | --- |
| `check_index.py --json` (two runs) | 9.34s, 9.16s | exit 0. Summary: 602 indexed, 436 compared, `provably_pending` 212, `no_recorded_acceptance` 159, within-10-lines 224, `cannot_decide` 7 (all of them unreachable acceptance revisions) |
| `build_index.py` without `--write` (two runs) | 3.24s, 3.17s | exit 0 |
| `verify_ground_truth.py --ref refs/remotes/origin/main` | 0.82s | **exit 1**, mismatch: "…65bacc7d6b85 is contained by no remote-tracking ref…" |

**E6, `check_index.py` cannot fail on drift (F5).** Its `main()` returns 0 on both output paths (`check_index.py:246`, `:262`). It returns 2 only when `--ref` cannot be resolved (`:153-156`).

**E7, clone dependence (F4).**

- `git cat-file -t 65bacc7` gives `fatal: Not a valid object name`, and the same for `d3dcb62`.
- The local build printed `STATED DROPPED (revision unresolved)` six times, all for `cloud-security-baseline-reviewer` pages (from `build_index.py:484-488`).
- Committed row for `.claude/skills/cloud-security-baseline-reviewer/SKILL.md`: `last_acceptance_sha 65bacc7d6b85…, confidence recorded, acceptance_reachable False`.
- Fresh-build row for the same page: `last_acceptance_sha None, confidence unknown`.
- Committed counts: `stated_candidates 19, recorded 443` (built at `source_revision d6e48418`, 53 commits behind HEAD). The fresh build at HEAD gives `stated_candidates 13, recorded 437, reader_pages 609`.
- The page list is read from a ref (`build_index.py:145`). The tracker, evidence and stated files are read from the working tree (`:358`, `:411`, `:478`).

**E8, gate isolation (F7, F8).**

- `test_offline_ci.py:387-393` defines `GATE_JOBS` and the exact `TOOLS_LABELS`.
- `:419-425` asserts that every path a gate job runs matches `gate_pattern`.
- `:452-454` asserts that the tools-job labels equal `TOOLS_LABELS`.
- `docs/offline-ci.md:46-56` describes the same rule ("Gate isolation").

**E9, history in CI (F10, F11).**

- From the log of job 112951998421 (gate-guard, PR #677): 273 `[new branch]` lines in the last 400, including `docs/readability-batch-b -> origin/docs/readability-batch-b`, then `[new ref] 3e171c4c… -> pull/677/merge` and `HEAD is now at 3e171c4c Merge ccf3fc22… into 03c93c77…`.
- `git ls-remote --heads origin | wc -l` gives `634`, the same as the local `refs/remotes` count.
- The tools jobs set only `persist-credentials: false` (`:374`, `:424`), with no `fetch-depth`, so they get the action's default shallow checkout.
- In the committed index, 41 distinct acceptance SHAs cover 443 rows. 39 are ancestors of `origin/main`, 2 are missing (`65bacc7` on 6 rows, `d3dcb62` on 1), and 0 are reachable only from a side branch.
- `e6fc8d24ad78…` is not an ancestor of main. It is contained only by `refs/remotes/origin/docs/readability-batch-b`.
- Reachability uses only `refs/remotes/` (`check_index.py:59`, `:124-125`; `build_index.py:77`). `git for-each-ref refs/tags | wc -l` gives `0`, so whether CI fetches tags is **unverified**.

**E10, the flake (F14).**

- In run 37367151729 attempt 1, jobs 111954952544, …579, …704 and …736 have no `runner_name` and no steps. All were created at 20:01:29Z and completed at 20:16:30Z with conclusion `cancelled`.
- Attempt 2 re-ran only those jobs and kept `validate-skills` from attempt 1.
- Of the 30 most recent runs, 1 has `run_attempt` 2.

**E11, the docs-only run (F2, F13).** Run 37667969180 skipped `tools-tests-windows`, `windows-offline-checks` and `tools-tests-linux`. The stale lines are `docs/offline-ci.md:28` ("Pull requests have no path filter") and `pull_request_template.md:33-34`.

## Proposed condition changes, for the coordinator

- **New C6: reproducible regeneration.** `build_index.py` must produce byte-identical output for the same revision in any clone, annotating unresolved revisions instead of dropping them. It must also read every input from `--ref`, or refuse when the working tree is not at `--ref`. C5's review must include a fresh-clone rebuild that is equal to the committed bytes.
- **New C7: scope fence.** The repair PR and every regeneration PR touch only `tools/readability_acceptance/**` and `docs/**`. That keeps `gate-guard` green and avoids owner exceptions. Any CI wiring is a separate PR with an owner exact-head exception.
- **New C8: if CI is extended.** Use an isolated, non-gate, non-required job with `fetch-depth: 0` and `--ref HEAD`, and its own path filter on `*.md` and `tools/readability_acceptance/**`. It prints the bound and fails only on tool errors or irreproducibility. It never fails because a page crossed the threshold, and never runs `verify_ground_truth.py` while that script fails by design. Do not add `tools/readability_acceptance/` to `gate_pattern`.
- **Amend C4.** Preserve each acceptance commit under a remote **branch** ref, or change the tool to accept `refs/tags/` (and verify that CI fetches tags). Tags alone are invisible to both scripts.
- **Amend C5.** The reviewer cites a local run of the tool's tests, `check_index.py` and the fresh-clone rebuild on Python 3.14. CI provides no evidence for this tool today.

## What I did not check

- The live branch-protection settings (HTTP 403), including whether CODEOWNERS review is enforced. `.github/CODEOWNERS` is `* @ModernNomad-98`.
- CI runtime of the tool on ubuntu-latest. Only local timings exist.
- Whether `actions/checkout@v7.0.1` with `fetch-depth: 0` fetches tags. The repository has 0 tags.
- GitHub billing. The repository is public, and I am relying on GitHub's published policy that standard runners are free for public repositories; I did not verify it in this session.
- The harvester's correctness and its four blind spots (other lanes).
- The run durations of #675 at attempt 1 beyond the job metadata; I fetched no logs for those jobs.
- Why the #675 re-run came 1h43m after the cancellation.
- Job logs other than the gate-guard log of #677.
- The cost of the delivery stages themselves (process lanes).

Finish: `2026-10-07T20:43:54Z` (`date -u`, read after the draft was written; the tree was still clean, `git status --short | wc -l` → `0`). Measured elapsed wall time is 20:34:45Z to 20:43:54Z, 9m09s. Active time was not measured separately.
