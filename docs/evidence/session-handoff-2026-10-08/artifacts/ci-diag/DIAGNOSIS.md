# Diagnosis: validate-skills failure on main, run 37713171379 at c060a7cb

Item: CI-failure diagnosis for the push-to-main run of PR #678's squash merge.
Started 2026-10-08T14:51:57Z. Finished 2026-10-08T15:19Z. Measured wall time is
about 27 minutes. Active time was not measured separately. No ETA was recorded
at the start, so the comparison against an ETA is unavailable.

## Skills used

- `ci-failure-classifier` (`.claude/skills/ci-failure-classifier/SKILL.md`) was
  used for the classification. It was applied only to logs saved on disk under
  `logs/`. The skill itself fetches and reruns nothing. The log downloads and
  the single re-run were separate steps, done under the coordinator's brief and
  the session permission system, and they are recorded below.
- `systematic-debugger` and `flaky-test-detective` are MANUAL-ONLY. Their
  frontmatter sets `disable-model-invocation: true`. The coordinator's brief is
  not the user naming them, so neither was invoked. The root-cause work below
  is ordinary reasoning: reproduce, isolate, then verify.

## Classification (ci-failure-classifier output format)

```
CI FAILURE CLASSIFICATION — validate-skills / run 37713171379 attempt 1 @ c060a7cb09758fa2f4f6b67ab00094f01d7c6a46
Evidence read: logs/run37713171379-attempt1-validate-skills-113103554440.log (1049 lines, complete, ends at
  "Cleaning up orphan processes") | Comparison run: 37709031628 (PR #678 merge 0f46051b, tree 0c5a2400),
  logs/run37709031628-attempt1-validate-skills-113090270682.log
Run verdict: RED (attempt 1). Attempt 2: validate-skills CLEAN for the log read. The other jobs were carried
  over from attempt 1, and their logs were not read.

| Job | Status | Duration / limit | Class | Deciding evidence | Next step → owner |
|---|---|---|---|---|---|
| validate-skills (attempt 1) | failure, step 9 "Check CI evidence and protected-path handling" | 20 s (01:29:23→01:29:43) / 15 min | TEST-BUG | "ERROR: test_each_enforcement_surface_requires_manual_merge ... (path='tools/behavioral_eval_runner/schemas/fixture.json')" / "line 149, in run_guard  with tempfile.TemporaryDirectory(prefix=\"aegis-ci-guard-\")" / "OSError: [Errno 39] Directory not empty: '/home/runner/work/_temp/aegis-ci-guard-y58nb11f/repo'" / "Ran 38 tests ... FAILED (errors=1, skipped=1)" | Test owner: fix the fixture isolation in scripts/tests/test_offline_ci.py (owner exception needed, see below) |
| changes, tools-tests-linux, tools-tests-windows, windows-offline-checks | success | 8 s / 2m37 / 3m44 / 2m19 | n/a | API conclusions only; logs not read | none |
| gate-guard | skipped | n/a | by design | `if: github.event_name == 'pull_request'` (D60) | none |

Green-run findings (attempt 2 validate-skills, job 113385585439): none beyond designed skips. ci-tests "Ran 38
  tests ... OK (skipped=1)", BER "OK (skipped=5)", equal to the comparison run (skipped=1 / skipped=5). The DCO step
  was skipped by design on push (`if: github.event_name == 'pull_request'`).
  "Cleaning up orphan processes" appears in both the failing and the passing log, so it does not tell them apart.
Indeterminate items: none.
Refused or out of scope: raising timeouts, adding retries, or setting ignore_cleanup_errors=True as "the fix".
  That would hide the race, so none is recommended.
```

TEST-BUG is a class, not a root cause. The mechanism is described next.

## Root cause

The test fixture deletes a Git repository while a background `git repack`, started
by Git itself, is still writing into it.

1. `ProtectedFileGuardTests.run_guard` (`scripts/tests/test_offline_ci.py:149-189`)
   creates a throwaway repository inside `tempfile.TemporaryDirectory`. It runs
   `git commit` twice, and then the gate-guard script runs `git fetch origin
   fixture-base`. When the `with` block exits, the tree is removed with
   `shutil.rmtree`.
2. Git 2.55.0 is on the runner (log line 60: "git version 2.55.0"). After `commit`
   and `fetch`, it runs `git maintenance run --auto --quiet --detach`. Detaching
   is the default (`maintenance.autoDetach` "Defaults to true", from
   Documentation/config/maintenance.adoc at v2.55.0, and run-command.c
   `prepare_auto_maintenance` pushes `--detach`). The maintenance process takes
   `.git/objects/maintenance.lock`, runs its foreground tasks, then calls
   `daemonize()` and runs its background tasks in a child process that outlives
   the git command (builtin/gc.c `maintenance_run_tasks`, lines 1785-1828).
3. Since Git 2.54 the default strategy is `geometric` (RelNotes 2.54.0:
   "git maintenance" starts using the "geometric" strategy by default). Its
   background `geometric-repack` task auto-fires when
   `too_many_loose_objects(100)` is true. The threshold is rounded up to 256.
   The count is estimated as the number of loose objects in `.git/objects/17/`
   times 256 (odb/source-loose.c, `ODB_COUNT_OBJECTS_APPROXIMATE`). So a fixture
   with **two loose objects whose IDs start with `17`** triggers a detached
   `git repack -d -l --cruft ... --write-midx`, even though the repository has
   fewer than ten objects. Under the old default (`gc` strategy, `gc.auto`
   6700), about 27 objects in that one directory were needed, which a fixture
   never reaches.
4. That detached repack writes `.git/objects/pack/.tmp-*`, `pack/tmp_idx_*` and
   `.git/info/refs`. Where the parent directories are already gone, it
   recreates them. It does this while `rmtree` is deleting the tree. `rmtree`
   lists a directory, deletes the entries, and then calls `rmdir`, which fails
   with ENOTEMPTY because new entries appeared in between. The failing
   directory depends on timing: `repo` (this run), `repo/.git/objects` (run
   36695924676), and `.git`, `.git/info` and `.git/objects/pack` (local runs).
5. Whether a fixture triggers the repack depends on the commit object IDs, which
   change with the commit timestamp. In every fixture of this file, none of the
   fixed objects (blobs and trees) has an ID starting with `17` (census below).
   A trigger therefore needs both commits to land in `17/`, a chance of 1 in
   65,536 per fixture. That explains why the failure is rare and hits a
   different subtest each time.

Python 3.14 is not the cause. Python 3.13's `shutil.rmtree` uses the same
fd-based stack implementation, and the race reproduced locally under Python
3.13.16 once Git 2.55.0 was used. The Git version is the deciding variable.

## Evidence

**PR #678 is not on the code path.**
- `git diff --stat 7d1d05e8 c060a7cb` lists six files, all under `docs/` (864
  insertions, 1 deletion).
- `git log -1 -- scripts/tests/test_offline_ci.py` gives 03c93c77 (PR #676).
  The file is unchanged by #678.
- The traceback line numbers 149 and 198 match `git show c060a7cb:scripts/tests/test_offline_ci.py`.

**The tree is the same as the passing PR run.**
- The PR run checked out merge commit `0f46051b` ("HEAD is now at 0f46051b
  Merge 3797739c... into 7d1d05e8", log line 767).
- `git merge-tree --write-tree 7d1d05e8 3797739c` gives `0c5a2400...`, and
  `git rev-parse c060a7cb^{tree}` gives `0c5a2400...`. They are identical.
- Both runs used CPython 3.14.7 and git 2.55.0.

**The same signature appears in one other run.** The search covered the last
500 completed runs of `validate-skills.yml`, from 2026-09-28T23:16Z to
2026-10-08T01:29Z (`runs-500.tsv`):
- Six failed runs in the latest 100 and 23 failed PR runs in runs 101–500. All
  of their failed-job logs were grepped for `Errno 39|Directory not empty`.
  The only hit was 37713171379.
- Two runs had a second attempt. Attempt 1 of **36695924676** (PR
  `docs/delivery-control-verify-wording`, 2026-09-30, git 2.55.0, CPython
  3.14.7) failed with the same error in the same test. The path was
  `'.GitHub/Dependabot.YML'`, and the message was "OSError: [Errno 39] Directory
  not empty: '/home/runner/work/_temp/aegis-ci-guard-nljvb8hl/repo/.git/objects'".
  That run went green on attempt 2.
- In total there are 2 occurrences in 500 runs. Both came from attempt 1 of a
  run, in the same helper, on different subtest paths.
- The other failures in the window were unrelated:
  - 37383161659 failed on `'needs' unexpectedly found` (the PR #676 branch
    before its fix).
  - 37268464341 failed on `SDK_VERSION_MISMATCH ... openai==3.0.0; found '3.23.0'`.
  - The gate-guard failures were on protected-path PRs.
- Sampled runs from 09-28 to 10-08 all show "git version 2.55.0", so the whole
  window ran under the exposed Git.

**Proof that the background process is detached** (`trace1/trace2.json`, `trace3/strace.txt`):
- GIT_TRACE2 shows `git maintenance run --auto --quiet --detach` started after
  each `commit` and after `fetch`, each entering region `maintenance detach`.
- strace of the fetch shows its maintenance parent (pid 24425) creating
  `.git/objects/maintenance.lock` and exiting. A child (pid 24426) calls
  `setsid()` and keeps reading `.git/objects/17` and commit objects. It only
  unlinks the lock after `fetch` has returned, while the guard's `git diff`
  is already running.
- With two loose objects in `17/` (`trace4`), the detached child enters region
  `maintenance geometric-repack` and starts `git repack -d -l --cruft
  --cruft-expiration=2.weeks.ago --quiet --write-midx` and `pack-objects`.

**Fixture census** (`repro/census`): the real `ProtectedFileGuardTests` were
run once with cleanup instrumented. That gave 88 fixtures, each with 2 commits.
The maximum number of non-commit loose objects in `17/` was 0 in every test
method. The expected number of natural repack triggers is 88/65536, about
0.00134 per test-file run, or about 1 per 745 runs.

## Local reproduction

The harness `scripts/stress.py` copies `run_guard` exactly and uses the real
guard from the workflow. All runs used a scratch TMPDIR and an empty global
git config, because the local global config has commit signing and CI does not.

| Setup | Result |
|---|---|
| Real test file, `python3 -B -P`, git 2.43.0, Python 3.13.16, 5 runs | 5/5 OK, 0 Errno 39 |
| Real test file, git 2.55.0 (built from the kernel.org tarball, sha256 457fdb04... matches sha256sums.asc), 20 runs | 20/20 OK, 0 Errno 39 |
| Harness, git 2.55.0, natural, 4 parallel workers × 600 | 0/2400 failures (matches the predicted rarity) |
| Harness, git 2.55.0, two loose objects in `17/` (natural trigger, no config override), 100 runs | **48/100 ENOTEMPTY** (`repo/.git` ×47, left behind: `info/refs`; `repo/.git/info` ×1) |
| Harness, git 2.55.0, `maintenance.geometric-repack.auto=-1`, 100 runs | **40/100 ENOTEMPTY** (`.git/objects/pack` ×36, left behind: `.tmp-*-pack-*.pack`; `.git/objects` ×4, left behind: `pack/tmp_idx_*`) |
| Harness, git 2.55.0, `maintenance.commit-graph.auto=-1`, 100 runs | 0/100 |
| Harness, git 2.43.0, two loose objects in `17/`, 100 runs | 0/100 (no detach and the old gc threshold) |

So the failure does **not** reproduce with the local default Git 2.43.0. It
reproduces at a high rate on Git 2.55.0 as soon as the background repack is
triggered, under Python 3.13.

## Re-run (one, as authorized by the brief)

- Before the re-run: run 37713171379 was `run_attempt 1, completed, failure`,
  and `git ls-remote origin refs/heads/main` returned `c060a7cb...`.
- At about 2026-10-08T15:13:10Z, `mcp__github__actions_run_trigger` was called
  with `rerun_failed_jobs`, run_id 37713171379. It returned "201 Created".
- Result: `run_attempt 2, completed, success` (updated 15:15:02Z).
  validate-skills job 113385585439 ran 15:13:17–15:15:00Z and all its steps
  succeeded (DCO skipped by design). ci-tests: "Ran 38 tests in 4.232s / OK
  (skipped=1)", "CHECK ci-tests: exit 0". Log:
  `logs/run37713171379-attempt2-validate-skills-113385585439.log`.
- Meaning: the same head and tree passed on re-run, consistent with a
  non-deterministic race in the test. The pass does not by itself prove the
  mechanism; the local experiments above do. Attempt 1 stays a failure in the
  run history, with this classification.
- Note: the brief said "the CI rules allow one re-run". No such rule was found
  in the repository. A grep of AGENTS.md, CONTRIBUTING.md,
  docs/delivery-workflow.md and the register found no matches. The only
  documented flake rule (`validate-skills.yml:64-65`) covers a different
  signature: "all jobs cancelled at the same instant". The re-run rests on the
  brief's explicit authorization and the session permission system.

## Proposed fix (not applied)

File: `proposed-fix.diff` (sha256 339e1f22...). It touches one file,
`scripts/tests/test_offline_ci.py`, and adds 10 lines.
`git apply --check` passes against c060a7cb.

```diff
--- a/scripts/tests/test_offline_ci.py
+++ b/scripts/tests/test_offline_ci.py
@@ -155,6 +155,16 @@
                                        "user.email=fixture@example.invalid", *args], cwd=repo,
                                       check=True, capture_output=True)
             git("init", "--quiet")
+            # Git runs auto-maintenance after `commit` and `fetch`, detached by
+            # default (maintenance.autoDetach), and since 2.54 its default
+            # geometric strategy can repack even this tiny repository. That
+            # detached `git repack` then writes into .git while
+            # TemporaryDirectory removes it, so cleanup fails with OSError
+            # ENOTEMPTY (runs 36695924676 and 37713171379). The fixture needs
+            # no maintenance: disable it in the fixture repository's own
+            # config, which the guard's `git fetch` reads as well.
+            git("config", "maintenance.auto", "false")
+            git("config", "gc.auto", "0")
             (repo / "README.md").write_text("fixture\n", encoding="utf-8")
             if rename:
                 old = repo / rename_from
```

Why this fix:
- `prepare_auto_maintenance` returns early when `maintenance.auto` is false, so
  no `commit` or `fetch` in the fixture starts any maintenance process. It
  also covers trigger paths this diagnosis did not observe.
- `gc.auto 0` covers older Git that still runs `gc --auto`.
- The setting is repository-local, so the guard script under test is
  unchanged and still reads the setting.
- The workflow and the real gate-guard job are unchanged.

Verification, using exported trees from `git archive c060a7cb` in `fixcheck/`
and running `ProtectedFileGuardTests`:

| Tree | Condition | Result |
|---|---|---|
| base | git 2.55, forced repack | 5/5 runs FAILED, 133 Errno 39 errors |
| patched | git 2.55, forced repack | 5/5 OK, 0 Errno 39 |
| patched | git 2.55, natural | 3/3 OK |
| patched | git 2.43 | 3/3 OK |

Not recommended: `TemporaryDirectory(ignore_cleanup_errors=True)`, a retry, or
a re-run policy. Each would hide the race and leave background repacks running
against deleted directories.

## Protected-path status

- `scripts/tests/test_offline_ci.py` matches the gate-guard `gate_pattern`.
  The live pattern was checked with bash `[[ =~ ]]` and nocasematch:
  "scripts/tests/test_offline_ci.py -> GATE (manual review and merge)". A fix
  PR therefore gets a red `gate-guard` and needs an owner exception, or a
  manual owner merge, that covers that exact head and scope (the MG1 rule in
  docs/delivery-workflow.md:291-300; the standing example is AEGIS-APR-047).
- `grep -n test_offline_ci docs/approvals/APPROVAL_REGISTER.md` found no
  existing grant for this file.
- CONTRIBUTING.md:238 lists `scripts/` as a security-relevant surface. The PR
  template's "Security-relevant surface?" must be answered "Yes: scripts/".
  Per AGENTS.md (2026-10-02), the extra security review applies to outside
  contributions only.
- CODEOWNERS: `* @ModernNomad-98`.

## Residual uncertainty

- The model predicts about 1 trigger per 745 runs. Even if every trigger
  caused a failure, that means about 0.67 expected failures in 500 runs; at
  the locally measured 40–50 % conversion, about 0.3. Two were observed
  (chance of 2 or more is about 3–15 %). So either this was chance, or CI has
  an extra trigger that could not be seen from here, for example runner
  system git config. The proposed fix disables all auto-maintenance in the
  fixture, so it does not depend on which trigger fired.
- The exact entry left in `repo` in run 37713171379 is unknown, because the
  runner's temp directory is gone. Locally, an equivalent `repo/.git`-level
  leftover was `.git/info/refs`, written by the repack's update-server-info.
- The local Git was built from source with NO_CURL, NO_OPENSSL and NO_PERL. The
  runner's packaged 2.55.0 may differ in build options. Those options do not
  affect the maintenance code paths cited.

## Files

- `logs/`: failing log (attempt 1), passing comparison, attempt-2 log,
  `other-failures/`, `older-failures/` (including run 36695924676 attempt 1)
- `runs-100.tsv`, `runs-101-500.tsv`, `runs-500.tsv`, `older-failures-grep.txt`
- `gitsrc/`: upstream git v2.55.0 sources and release notes cited above
- `trace1/`, `trace2/`, `trace3/`, `trace4/`: trace2 and strace evidence
- `scripts/`: `loop.sh`, `stress.py`, `ab.sh`, `census.py`, `census_sum.py`
- `repro/`: every local run's logs and summaries
- `fixcheck/`: base and patched exported trees
- `proposed-fix.diff`
