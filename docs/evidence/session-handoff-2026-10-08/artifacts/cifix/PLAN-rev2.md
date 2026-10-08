# CIFIX-1: Stage A PLAN, revision 2

**Item:** CIFIX-1, "Fix the Errno 39 race in `scripts/tests/test_offline_ci.py`".
**Stage held:** Stage A (PLAN) only. No repository file is written, nothing is
committed, pushed, opened as a pull request or merged.
**Supersedes:** PLAN-rev1 (sha256 `634f3f0fbcc48592f8e8d4abfdaf4b42f16130f4eaa52128f125f018195110c8`),
which received `SD-B: REVISE`. Rev1 is left unedited. §12 maps each required change
(RC1–RC10) to the place where this revision addresses it.

**Repository and role:** `/home/user/Project-Aegis`, Role A. The four source landmarks
are present: `head -3 README.md` shows `# Project Aegis`, and `ls` found
`docs/skills-catalog.md`, `scripts/validate-skills.py` and
`artifacts/audits/skill-contract-audit-baseline.json`.

**Base at writing:**
- `origin/main` = `5228977920ee479e1fe1ec6b8d56f8fc24c14947`, from
  `git ls-remote origin refs/heads/main` at 2026-10-08T16:13:29Z.
- PR #679 merged at 15:55:22Z as `c1acc075` (a merge commit).
- PR #680 merged at 16:13:04Z as `52289779` (a squash).
- Open pull requests: **0**, from `gh api 'repos/…/pulls?state=open' --jq length`.
- **Stage C re-measures every baseline at whatever `main` is when it starts (§5.0).**
  The figures here are reference values only.

**Revision 2 started:** 2026-10-08T16:10:57Z (`date -u`). Revision 1 was written
15:29:52Z–15:51:44Z.

**Scratch root:** `S=/tmp/claude-0/-home-user-Project-Aegis/0168d1d5-9af4-5a74-a8dd-9a35339e53ab/scratchpad`.

| Input | sha256 |
| --- | --- |
| `$S/cifix/BRIEF.md`, read in full: the owner's instruction, the owner's Q2/Q3/Q4 answers (recorded 16:01:16Z), the original question and the one-line option text, and the coordinator's RC3 reading (recorded 16:10:40Z) | `5729b3914ebafd4798e110f38e9a57c004b2ee8fa769a3cbf33a5faabe713aa6` |
| `$S/cifix/PLAN-AUDIT-rev1.md` (Stage B, `SD-B: REVISE`) | `26609843ae2940c42cb93dc7813703b3397ff27a3e497926f0df62264c6941e0` |
| `$S/ci-diag/DIAGNOSIS.md` | `522ea312e15f7d7f7b930f20e508c632b2fb54cfbf783c8734fe5d1710c09cfb` |
| `$S/ci-diag/proposed-fix.diff` | `339e1f2257f78e10bae44ad9f93cddbcd769ecabdf1ff35c2c3a888d456e38fb` |

The audit cites the brief's intermediate hash, `5419a0da…`. The current brief,
`5729b391…`, adds the section "Answers to Stage B RC6 / RC3".

`$S/rcf/BRIEF-COMMON.md` binding rules 1–7 apply. The CIFIX brief and the owner's Q2
answer override rule 5's default against touching the register; see §6.5.

---

## 0. Aegis skills read and applied (dogfood rule)

`docs/delivery-workflow.md:97` says no installed skill owns writing a single change's
plan, so Stage A is enforced by procedure. The skills below were applied to the parts
of the plan they do own. No MANUAL-ONLY skill was used. `systematic-debugger`,
`flaky-test-detective` and `reviewable-diff-discipline` all carry the
`MANUAL-ONLY; never auto-invoke.` description prefix.

| Skill | How applied | Result |
| --- | --- | --- |
| `change-classification-gate` (`.claude/skills/change-classification-gate/SKILL.md`) | Classified each deliverable from the files it touches. Applied the class→floor matrix (`references/classification-matrix.md:22,24`), the rule that the highest class governs, and the scope lock. | §2. The bug-fix floor ("Reproduce the failure first; prove the fix flips it; regression test added") is why §4 includes the regression test. Stage B agreed (audit §2.2). |
| `ci-failure-classifier` | Re-read the failing and passing logs on disk. Applied the rules "never mask a failure with timeout or retry" and "a required job that was skipped is never counted as passed". | TEST-BUG (§3.1). Skipped jobs are recorded as skipped (AC-F11, AC-R6, §9). |
| `human-approval-boundary` | Matched each risky action against the owner's instructions and the register's grants: P-FIX's administrator merge past a red `gate-guard`, P-REG's register edit and merge, and the response to a moved head. | P-FIX is covered by the owner's one-time grant once it is merged on `main`. P-REG is covered by the owner's Q2 answer. A head that moves after recording needs a fresh owner decision (Q4 answer). AEGIS-APR-047 does not reach this change (§6.1). |
| `scoped-approval-register` | Drafted the entry with the verbatim scope and its proposal context (RC6). The one-time limit comes from the wording, nothing is invented, and lifecycle changes are appended as events. Consumption timing follows the owner's Q3 answer. | §6.4 draft and §6.6. |
| `risk-tiered-validation-selector` | Applied its "never docs-only" list, which includes `scripts/`, and max aggregation across the files touched. | P-FIX gets the **full** tier. P-REG gets the repository checks plus a link check of the register and the append-only proof (§7.2). |

`ai-task-decomposer` was considered and not applied: this is one change plus one
dependent recording change.

---

## 1. What, why, blast radius, paths

**What.** `ProtectedFileGuardTests.run_guard` in `scripts/tests/test_offline_ci.py`
gets two lines immediately after its `git init`:

```
git config maintenance.auto false
git config gc.auto 0
```

They turn off Git auto-maintenance in the throwaway fixture repository. The same
class, in the same file, also gets one deterministic regression test proving that no
auto-maintenance process starts.

**Why.** Git 2.55 starts a **detached** `git maintenance run --auto` after every
`commit` and `fetch`. Under the default geometric strategy (the default since Git
2.54), that process can run `git repack`, which writes into `.git` while
`TemporaryDirectory` is deleting the tree. Cleanup then fails intermittently with
`OSError: [Errno 39] Directory not empty`, as in runs 36695924676 and 37713171379.
The same race also shows up as a failed second `git commit` (exit status 128) under
a forced trigger (audit N1; §3.5). §3 verifies the cause independently.

**Blast radius.** One CI self-test file. Nothing else changes:
- the real `gate-guard` script and the workflow are unchanged (AC-F10);
- no production, skill or documentation content changes;
- the only behaviour change is that the fixture repositories stop starting background
  maintenance;
- every existing assertion is kept, because the change only adds lines (AC-F1).

The risk is low. The file is still a protected, security-relevant surface, so
`gate-guard` fails by construction. The merge needs the owner's one-time exception,
recorded and merged on `main` first (§6).

**Paths.**
- **P-FIX**, the fix pull request: `scripts/tests/test_offline_ci.py` only.
- **P-REG**, the register pull request: `docs/approvals/APPROVAL_REGISTER.md` only,
  as one appended GRANT entry.
- **Out of CIFIX-1:** the consumption event for that entry goes into **the next
  register pull request, together with FU-2's AEGIS-APR-119 consumption**. This
  follows the owner's Q3 answer (§6.6). CIFIX-1 only has to leave the facts that
  event needs in P-FIX's merge receipt.
- **Not touched by either pull request:**
  - `.github/`, including the workflow, `gate_pattern` and the PR template;
  - every other file under `scripts/`;
  - `tools/`;
  - `docs/delivery-workflow.md`, `AGENTS.md`, `CLAUDE.md` and `CONTRIBUTING.md`;
  - the skills;
  - all reserved scope: the evaluation package, VMs, Stage 4B, BER calibration,
    provider spend and the `[evaluation-source-pin]` source pin.

**Why two pull requests.** The owner's option text asks for "A third PR touching only
that test file", plus an exception "for that exact commit, recorded in the register".
A commit cannot carry its own SHA. Putting the entry inside P-FIX would add a second
file and move the head the entry names. AEGIS-APR-106 records the same point by
quoting the Stage D audit of PR #661: *"The PR cannot create that entry for itself"*
(register L3463-3464). The owner approved this separate pull request in the Q2 answer,
"Yes, same terms (Recommended)", quoted in §6.2.

---

## 2. Classification (`change-classification-gate`)

```
CHANGE CLASSIFICATION — P-FIX
Deliverables:    (1) disable auto-maintenance in run_guard's fixture repo; (2) one regression test
Classes:         (1) bug-fix (test bug); (2) qa-test-only
Governing class: bug-fix on a protected, security-relevant path (scripts/, gate_pattern match)
Approval path:   human-approval-boundary → the owner's one-time gate-guard exception (2026-10-08), which
                 must be merged on main (P-REG) before P-FIX merges (§6); AEGIS-APR-047 does not reach it
Validation plan: bug-fix floor = reproduce before → prove the fix flips it → regression test added
                 (AC-F4..F7); qa-test-only floor = run the suite and show nothing is masked
                 (AC-F1..F3, F8); risk-tiered tier = full (scripts/)
Scope contract:  scripts/tests/test_offline_ci.py only; additions only; nothing under .github/

CHANGE CLASSIFICATION — P-REG
Deliverables:    one appended GRANT entry recording the owner's one-time exception for P-FIX's head
Classes:         docs-only by file type, on a security-relevant governance surface (CONTRIBUTING.md:246)
Governing class: governance record (verbatim-quote, proposal-context and append-only proofs required)
Approval path:   owner's Q2 answer ("Yes, same terms (Recommended)": all seven stages, all checks
                 green, admin merge allowed); AEGIS-APR-100/048/050 as supporting mechanics
Validation plan: validator + validator self-tests + link check of the register + byte-prefix append proof
Scope contract:  docs/approvals/APPROVAL_REGISTER.md only; append-only at end of file
```

**Criteria declared not verifiable at P-FIX's head before publication, or
probabilistic** (required by `SD-A`):

1. **AC-F11, CI at the exact head H.** It can only be checked after the push. It is
   also a precondition for P-REG's Stage C (RC4), so P-REG cannot start before it is
   known.
2. **"The race never recurs in CI."** No single head can show this. The natural
   trigger rate is about 1 in 745 test-file runs (diagnosis census). The
   deterministic regression test (AC-F5) and the forced-trigger stress run (AC-F6)
   stand in for it.
3. **Python 3.14** is UNRUN locally. Only 3.13.16 is installed (`python3 --version`),
   and `which python3.14` found nothing. The `validate-skills` job at H covers it.
4. **`acceptance-core` (pwsh)** is UNRUN locally, because `which pwsh` found nothing.
   The `validate-skills` job at H covers it.
5. **Windows** is UNRUN at H.
   - `windows-offline-checks` is skipped by the path filter (`changes` outputs
     `offline=false`).
   - `ProtectedFileGuardTests` skips on Windows anyway, by its class decorator
     (test file L137).
   - The post-merge push run is the Windows evidence (audit N3).

---

## 3. Independent verification of the root cause

All of the following is unchanged from rev1 except where noted. Stage B reproduced it
with its own harnesses (audit §2.1–2.2).

**The base moved; the code under test did not.** Comparing `c060a7cb` with `52289779`:

```
git diff --quiet c060a7cb origin/main -- scripts/tests/test_offline_ci.py .github/workflows/ scripts/ci/record-check.py scripts/validate-skills.py
```

returns rc 0 at `origin/main` = `52289779`. The prototype still applies there:
`git apply --check $S/cifix/prototype-reference.diff`, run in a scratch clone at
`52289779`, prints "prototype applies at 52289779". So every line number and finding
below still holds.

### 3.1 CI evidence, re-read from the logs on disk

`$S/ci-diag/logs/run37713171379-attempt1-validate-skills-113103554440.log`:
- L60: `git version 2.55.0`
- L947/949: `line 198, in test_each_enforcement_surface_requires_manual_merge` → `line 149, in run_guard`
- L973: `OSError: [Errno 39] Directory not empty: '/home/runner/work/_temp/aegis-ci-guard-y58nb11f/repo'`
- L976-978: `Ran 38 tests in 3.520s` / `FAILED (errors=1, skipped=1)`
- 1049 lines in total (`wc -l`), the last being `Cleaning up orphan processes`.

Run 36695924676, attempt 1 (`logs/older-failures/run36695924676-attempt1-109823746991.log:878`):
`… aegis-ci-guard-nljvb8hl/repo/.git/objects'`.

The class is **TEST-BUG**.

`actions/checkout` runs `[command]/usr/bin/git config --local gc.auto 0` on the CI
checkout (L87). It does the same in a `gate-guard` job log
(`logs/other-failures/run37159209057-111308911050.log:85`, Git 2.55.0 at L58). So
the real guard job already runs with auto-maintenance off, and the fix makes the
fixture match it.

### 3.2 Git 2.55.0 source (`$S/git-build/src/git-2.55.0`)

- **Call sites.** `grep -rn 'run_auto_maintenance\|prepare_auto_maintenance' --include=*.c`
  finds callers only in `builtin/am.c:1942`, `receive-pack.c:2731`, `commit.c:1965`,
  `merge.c:509`, `fetch.c:2885` and `rebase.c:572`. The fixture and the guard reach
  only `commit` and `fetch`.
- **Off switch.** `run-command.c:1956-1967`: if `maintenance.auto` is false, the
  function returns 0. If it is absent, `gc.auto <= 0` disables maintenance instead.
  Either setting alone is enough on 2.55; Stage B confirmed this. `gc.auto 0` also
  covers older Git that runs `gc --auto` directly, but that claim is **not
  re-verified against old source**, so it stays labelled unverified.
- **Detach default.** `run-command.c:1974-1976`: maintenance detaches by default.
- **Fetch.** `builtin/fetch.c:2868` runs maintenance only if `enable_auto_gc` is set.
  It defaults to on, and only `--no-auto-maintenance` (L2580) turns it off. The
  guard's `git fetch origin "$BASE_REF" --quiet` does not pass that flag.

### 3.3 Every temp-dir fixture and git invocation in the file

The file was read in full: 750 lines, unchanged at `52289779`.

| Fixture (line) | Git invocations (cwd) | Can a detached process start inside the temp dir? |
| --- | --- | --- |
| `RecorderTests.setUp` `TemporaryDirectory("aegis-ci-recorder-")` (L47) | `git rev-parse HEAD` at L65, and the recorder's `git rev-parse HEAD` / `git status --porcelain` (`scripts/ci/record-check.py:63-64`); cwd = REPO | No. These commands never start maintenance, and REPO is never deleted. |
| `test_concurrent_local_runs…` `TemporaryDirectory("aegis-ci-fallback-")` (L90) | the same recorder calls, cwd = REPO | No |
| **`run_guard` `TemporaryDirectory("aegis-ci-guard-")` (L149)** | cwd = repo: `init` L157, `add` L165, **`commit` L166**, `branch` L167, `remote add` L168, `mv` L171, `add` L177, `hash-object -w` L179, `update-index` L181, **`commit` L183**. The guard (L184, cwd = repo) runs **`git fetch origin "$BASE_REF" --quiet`** and `git diff --no-renames --name-only -z …` | **Yes: three triggers per fixture** |
| `run_shadowed_validator` `TemporaryDirectory("aegis-ci-shadow-")` (L350) | `scripts/validate-skills.py:817,1084` runs `git ls-files` (not a repository) | No |
| `test_root_executable_cannot_replace_git…` `TemporaryDirectory("aegis-ci-exe-")` (L631, Windows only) | `git --version` | No |
| `GateJobIsolationTests`, `HashLockTests` | none | n/a |

### 3.4 Trace2 spawn census (`$S/cifix/scripts/trace_count.sh`, sha256 first 16 `56ebea49c320effe`)

| Tree | Git | Result |
| --- | --- | --- |
| base `c060a7cb` | 2.43.0 / 2.55.0 | `maintenance_child_start=264 … maintenance_processes=264` (both) |
| base + proposed fix | 2.43.0 / 2.55.0 | `maintenance_child_start=0 gc_auto_child_start=0 maintenance_processes=0` (both) |

By parent process: `{'fetch': 88, '-c': 176}`, which is 88 fixtures × (2 commits +
1 fetch). Stage B reproduced `264 → 0` with its own counter (`by_parent={'commit': 176,
'fetch': 88}`). **The local setting reaches every path, including the guard's own
`git fetch`.**

### 3.5 Forced trigger (`$S/cifix/scripts/ab_force.sh`, sha256 first 16 `149d3b3bff39a56b`)

The trigger is `GIT_CONFIG_COUNT/KEY/VALUE` with `maintenance.geometric-repack.auto=-1`.
A negative value forces the task every time (`builtin/gc.c:1632-1637`, confirmed by
Stage B).

- base, Git 2.55: `runs=3 pass=0 fail=3 errno39_lines=82 leftover_tmp=82`. All errors
  come from `line 149, in run_guard`, across `repo/.git/objects/pack`,
  `repo/.git/objects`, `repo/.git` and `repo/.git/info`.
- Stage B also saw a `CalledProcessError … 'commit' … exit status 128` at
  `line 183, in run_guard`: the detached repack started by the first commit racing
  the second commit (audit N1). That is the same root cause.
- prototype, Git 2.55: forced `runs=10 pass=10 fail=0 errno39_lines=0 leftover_tmp=0`;
  natural `runs=10 pass=10 … 0 … 0`.

### 3.6 Alternatives (decision unchanged: repository-local config only)

Rejected:
- **Passing `GIT_CONFIG_*` through the environment**, alone or together with the
  repository config. It would have to be threaded into two environments, it would
  inject command-line-scope config into the guard under test, and §3.4 already shows
  0 spawns without it.
- **`--no-auto-maintenance` on the guard's fetch.** That edits the workflow, which is
  outside "only that test file".
- **`maintenance.autoDetach false`.** Maintenance would still run in the foreground
  and still repack.
- **`ignore_cleanup_errors`, a retry, a sleep or a re-run policy.** Each one hides
  the race.

Residuals:
- **Command-line config precedence.** A higher-precedence `-c` or
  `GIT_CONFIG_PARAMETERS` would win over the repository config. Neither exists in the
  test, and gate jobs are barred from `GIT_CONFIG*` by
  `test_current_workflow_has_no_gate_violations` (L557) and its mutation test
  (L585-599).
- **The runner's packaged Git build options** are unverified.

---

## 4. The change (P-FIX), written by Stage C

The reference prototype is planning evidence, not the implementation.

- **File:** `$S/cifix/prototype-reference.diff`, sha256 `a4ad6f9fdcd63446614b40216d82d94a473599e6344a837b0aa9f10e94c96a6f`.
- **Size:** `git diff --numstat` reports `28	0	scripts/tests/test_offline_ci.py`.
- **It applies at `52289779`.**

Stage C may restyle it, but every property P1–P7 must hold and every criterion in
§7.1 must pass.

- **P1.** In `run_guard`, immediately after `git("init", "--quiet")` and before the
  first `git("commit", …)`, add:
  - `git("config", "maintenance.auto", "false")`
  - `git("config", "gc.auto", "0")`

  Keep an explanatory comment that names runs 36695924676 and 37713171379.
- **P2.** Add one test method to `ProtectedFileGuardTests`, so it inherits the
  POSIX-only skip. It sets `GIT_TRACE2_EVENT` to a separate `TemporaryDirectory`
  around one `self.run_guard([<protected path>])`, using
  `unittest.mock.patch.dict(os.environ, …)`. It asserts:
  - the guard returns 1;
  - the trace is live: some `child_start` argv contains `upload-pack`;
  - no `child_start` argv contains the element `maintenance`, or both `gc` and
    `--auto`.

  The prototype names it `test_fixture_repository_starts_no_auto_maintenance`.
- **P3.** `from unittest import mock` goes beside `import unittest`.
- **P4.** Additions only.
- **P5.** No `skip*`, `expectedFailure`, `ignore_cleanup_errors`, retry, `sleep` or
  timeout change anywhere.
- **P6.** Exactly one commit, signed off (`git commit -s`), on the new branch
  `claude/sharp-lovelace-urgxpz-ci-fix`. Create the branch from `origin/main` as
  re-measured in §5.0. Stage exactly the one file, and run
  `git branch --show-current` before the commit and before the push.
- **P7.** The commit message names the root cause and both run IDs. It never contains
  the Codex trigger phrase, the word codex prefixed with the at sign.

**Measured on the prototype.**

The flip test ran 5× per cell, on both Git 2.43.0 and 2.55.0:

| Configuration | Result |
| --- | --- |
| Test present, config lines absent | `5 FAILED (failures=1)` |
| Test present, config lines present | `5 OK` |

The rev2 re-check used the AC-F5 deletion command (it removed 2 lines) and gave
`FAILED (failures=1)` ×2 on each Git. The assertion message reads
`AssertionError: Lists differ: [] != [['git', 'maintenance', 'run', '--auto', …`.

The full file, run in a scratch clone with `GIT_CONFIG_GLOBAL=/dev/null`, gives
`Ran 39 tests … OK (skipped=1)` on both Git versions.

`count_fixtures.py` reports `run_guard_fixtures=89 test_methods_total=39`.

**Open point OQ-B, flagged and not resolved.** The proposal the owner answered said
"The proposed fix adds two lines to scripts/tests/test_offline_ci.py" (§6.2). The plan
adds those two lines plus the regression test: 28 lines in all, still in the one
file. The owner's chosen option scopes the change by file ("touching only that test
file"), not by line count. The coordinator's position on Q5 is to keep the test, and
Stage B agrees. The entry draft states the real `+<a>/−0` and the test's presence
(§6.4), so the record does not overstate how closely the head matches the "two
lines" description. See §11.

---

## 5. How to prove it

### 5.0 Baseline re-measurement: Stage C runs this first, at the `main` it branches from

```bash
git fetch origin main && B=$(git rev-parse origin/main)       # record B (40 hex)
git diff --quiet 52289779 "$B" -- scripts/tests/test_offline_ci.py .github/workflows/ scripts/ci/record-check.py scripts/validate-skills.py; echo $?
# scratch clone at B, with TMPDIR=<scratch> GIT_CONFIG_GLOBAL=/dev/null PYTHONDONTWRITEBYTECODE=1:
python3 -B -P scripts/validate-skills.py                  # reference at 52289779: OK: 195 skill(s) valid, 0 warning(s)
python3 -B -P scripts/tests/test_validator.py             # reference: OK: 181 gate self-test assertion(s) passed.
python3 -B -P scripts/tests/test_audit_skill_contracts.py # reference: OK: 76 contract-audit self-test assertion(s) passed.
python3 -B -P scripts/tests/test_markdown_links.py        # reference: Ran 23 tests … OK
python3 -B -P scripts/tests/test_offline_ci.py            # reference: Ran 38 tests … OK (skipped=1)
python3 -I -B $S/cifix/scripts/count_fixtures.py <clone>  # reference: run_guard_fixtures=88 test_methods_total=38
```

All six reference values were measured at `52289779` at about 16:13–16:14Z on
2026-10-08. The values at `c060a7cb` and `c1acc075` were identical.

- **Scope-lock rule.** If the `git diff --quiet` check returns non-zero (the test
  file, workflow, recorder or validator changed since `52289779`), **stop and return
  to Stage A.** The prototype and its line numbers would no longer be proven.
- **Otherwise,** B's re-measured values become the "at B" expectations in §7.1.
  Record them in the handoff.

### 5.1 Before, after, flip and stress

All of these run from scratch. Exported trees come from
`git archive <rev> | tar -x -C <dir>`. Every run uses a scratch `TMPDIR`,
`GIT_CONFIG_GLOBAL=/dev/null` and `PYTHONDONTWRITEBYTECODE=1`, plus `python3 -B -P`.
The empty global config is needed because the local global config enables
`commit.gpgsign` and CI does not; the file still passes with the real config, just
more slowly.

Git selection:
- **G55** is `$S/git-build/install/bin`, Git 2.55.0. Select it with
  `PATH=G55:$PATH`.
- The system Git, 2.43.0, is selected by leaving `PATH` unchanged.

The runs:
1. **Before, on `T(B)`.** `trace_count.sh` should show 264 spawns.
   `ab_force.sh … 3 1 G55` should report `fail>=1 errno39_lines>0`.
2. **After, on `T(H)`.** AC-F4 and AC-F6.
3. **Flip.** AC-F5.
4. **Natural stress.** AC-F7.
5. **Repository checks.** AC-F8 and AC-F9.

---

## 6. The one-time `gate-guard` exception: how and when it is recorded

### 6.1 Precedent (`grep -n '^###' docs/approvals/APPROVAL_REGISTER.md`)

**The preamble.**
- L8-13: "Grant entries are immutable. Append later revocation, expiry, consumption or
  supersession events … Current direct user instructions are valid source evidence
  before transcription and do not need repeated consent."
- L33-35: "A one-use grant can be used up even before a later event records that".
- L63-66: "usually one-time for one exact head, except the standing four-file
  exception in AEGIS-APR-047."

**AEGIS-APR-047 does not reach this change.** Its Scope FORBIDDEN keeps "guard scripts
and tests" for "separate one-time owner decisions" (register L1269-1271).

**29 one-time exception entries exist.** The count is
`grep -E '^### AEGIS-APR-[0-9]+: .*(guard exception|gate-guard exception|protected-path decision)' | grep -v -E 'Consumption|Standing' | wc -l`
→ `29`. The ones that set the pattern for this change:

| Entry | Pull request | Recorded | Vehicle |
| --- | --- | --- | --- |
| APR-103/104 | #648/#649 | after merge | register PR #652 |
| **APR-106** | #661 | **before merge** | separate register-only PR **#663**, merged 23:33:38Z; #661 merged 23:36:19Z |
| APR-107 | #661 consumption | after | PR #664 |
| APR-032 → 033 → 034 | #281 | head moved → EXPIRED unused → new GRANT on a **fresh owner reply** | — |

On #661 specifically: APR-106 bound an owner selection that named no SHA to an exact
head (L3481-3496). Its "PR cannot create that entry for itself" is a quotation of
#661's Stage D audit (L3463-3464).

**Two attribution corrections from rev1 (RC9b, RC9c).**
- The phrase "the append-only rule governs merged entries" appears **only in #663's PR
  body** (body line 62, per the audit).
- APR-105 says instead: "Once merged, any further change to it is an append".

**Merge methods vary.** PR #661 and PR #680 were squashed. PR #679 was merged with a
merge commit (`git log --oneline -4 origin/main` shows `c1acc075 Merge pull request
#679 …`). P-FIX's receipt therefore records which method was used and the ancestry
result (§6.6).

### 6.2 The owner's words (from `$S/cifix/BRIEF.md`, sha256 `5729b391…`)

**The proposal context for the grant.** The coordinator relayed this verbatim, from
the session's own AskUserQuestion call, header "CI test fix":

> main's CI failure was a rare race in one CI test: Git 2.55 starts a background clean-up job in a throwaway test folder, and the test deletes the folder while that job is still writing. The one re-run passed, so main is green again, and the same race has happened once before (2026-09-30). The proposed fix adds two lines to scripts/tests/test_offline_ci.py telling Git not to run that background job in the test's folder. scripts/ is protected, so a fix PR's protected-file guard (gate-guard) will be red until you grant a one-time exception for that exact PR commit. Do you want the fix?

That text is 588 characters, sha256 first 16 `87eee772606974b1`. The two options the
owner did not choose were:
- "Yes, but ask me before merging" — "Same PR. It waits for you to look at the exact
  commit before the exception is used."
- "Not now, backlog it" — "Leave it as a known intermittent failure (about 1 in 750
  runs by the diagnosis) and record it as a backlog item."

**The grant.** The owner chose the label "Yes, one-time exception (Recommended)".
Its option text, **confirmed by the coordinator as the one-line form the owner saw**,
is:

> A third PR touching only that test file, on a third branch, through all seven stages. It merges once gate-guard's red is covered by your one-time exception for that exact commit, recorded in the register, with every other check green. Admin merge allowed.

It is 255 characters, sha256 first 16 `95826ec00af9e24e`. A Python comparison shows it
is byte-equal to the brief's wrapped text joined with single spaces (`EQUAL: True`).
This closes RC6c.

**Q2, the vehicle and its terms.** Question:

> The exception has to name the fix PR's exact commit, which only exists once the fix is written. The last one-time exception (AEGIS-APR-106) handled this with a separate small PR that changes only the approval register, merged just before the protected PR. That's a fourth PR your instruction didn't name. May the team open and merge it on the same terms (all seven stages, all checks green, admin merge allowed)?

The owner answered **"Yes, same terms (Recommended)"**. Option text:

> Follows the precedent. The fix PR stays one file, and the exception is in the register, approved and pinned to the exact commit, before the fix merges. About 30–45 extra minutes.

**Q3, consumption.** The owner answered **"Batch it later (Recommended)"**. Option
text:

> Recorded in the next register PR, which will also record FU-2's grant as used up. One PR instead of two, with no loss of safety, since a one-time exception for an exact commit can't be reused anyway.

**Q4, a head that moves after the exception is recorded.** The owner answered **"Ask
me again (Recommended)"**. Option text:

> Matches the AEGIS-APR-032→034 precedent. Each exception stays tied to a commit you approved. Costs a short wait for your answer if it happens, which is unlikely because the fix is small.

All three answers were recorded by the coordinator at 16:01:16Z.

**Caveat on the Q2–Q4 one-line forms.** They are **reconstructions**: the brief wraps
them, with indented continuation lines, and they were joined with single spaces. Only
the 255-character option text has the coordinator's one-line confirmation. The brief
also gives no verbatim question text for Q3 or Q4, only the coordinator's labels
"(consumption record)" and "(fix head moves after the exception is recorded)". See
OQ-A.

**Coordinator's reading (RC3), recorded 16:10:40Z.** "recorded in the register" is
read as **merged on main**, because the register on the default branch is the
authority (AGENTS.md; MG4 at `docs/delivery-workflow.md:312-320`). The coordinator is
telling the owner about this reading, and this plan follows it.

### 6.3 Vehicle, entry condition, merge condition, head-move procedure

**Vehicle.** A separate register-only pull request, **P-REG**, on a fourth branch. A
suggested name is `claude/sharp-lovelace-urgxpz-ci-fix-register`; the coordinator
chooses. It touches only `docs/approvals/APPROVAL_REGISTER.md` and appends exactly one
GRANT entry at the end of the file. That path is not protected: against the live
`gate_pattern`, `docs/approvals/APPROVAL_REGISTER.md -> not gated` and
`scripts/tests/test_offline_ci.py -> GATE`. Stage B reproduced this from
`validate-skills.yml:528`. So `gate-guard` should be green on P-REG. This plan is
P-REG's Stage A plan of record too (§7.2). P-REG runs its own stages C–G with distinct
holders (§9).

**When P-REG's Stage C may start (RC4).** Both of these must hold at P-FIX's head H:
- (a) P-FIX has a posted `SD-D: ACCEPT` naming H.
- (b) Every check run at H has `status completed`, with these conclusions:
  - `gate-guard` = failure, and its log shows `Gate files touched:` followed by
    exactly `scripts/tests/test_offline_ci.py`;
  - `changes` and `validate-skills` = success;
  - `windows-offline-checks`, `tools-tests-linux` and `tools-tests-windows` =
    skipped.

  Read the run-level state, not a job's `status` alone (AGENTS.md, run 37156376468).

The entry records those check-run and run IDs and their conclusions, so they must
exist before it is written.

**When P-REG may merge (RC5).** All of the following must hold:
- (a) P-FIX has a posted `SD-F: ACCEPT` naming the **same** H the entry names.
- (b) P-FIX's MG3 condition is met at H: the automated review has posted a result for
  H, or is confirmed unavailable for H, and every P0–P2 finding is triaged.
- (c) P-FIX's head is still H: `gh api …/pulls/<P-FIX> --jq .head.sha` equals the
  entry's H.
- (d) P-REG's own MG1–MG5 hold at its head Hʳ, on the owner's Q2 terms ("all seven
  stages, all checks green, admin merge allowed").

After that, the only step left is P-FIX's Stage G. This honours "merged just before
the protected PR" in the Q2 question.

**If the head moves (RC3, applying the owner's Q4 answer as a fixed procedure).**
- **Before P-REG has merged.** The entry is not yet "recorded" under the coordinator's
  reading. P-REG's unmerged entry is rebuilt in place for the new head. That is
  allowed, on the ground #663's body states and APR-105 applies to unmerged entries.
  Every P-REG verdict is void and is taken again. P-REG's Stage C entry condition and
  the merge conditions are re-applied at the new head.
- **After P-REG has merged.**
  - AEGIS-APR-120 is spendable on nothing, and **P-FIX is not merged.**
  - The coordinator **asks the owner again**, per the Q4 answer and the
    APR-032→033→034 precedent.
  - Only after a fresh owner answer that names the new head does one register-only
    pull request, on the Q2 terms, append an EXPIRED event for APR-120 and a new
    GRANT for that head.
  - No agent re-binds the exception on its own.
- **Dependency, flagged.** The "before P-REG has merged" branch needs no owner
  question only because of the coordinator's reading that "recorded" means "merged on
  main". If the owner rejects that reading, that branch also becomes an owner
  question.

**Exact-head binding.**
- (a) The entry names: the pull request number; the 40-character head H; its tree
  (`git rev-parse H^{tree}`); its base B; the single path with its `numstat`; the
  `gate-guard` check-run and workflow-run IDs at H; and the `Gate files touched:` log
  line followed by the sole path.
- (b) P-FIX's merge is pinned to H, using REST `PUT
  /repos/ModernNomad-98/Project-Aegis/pulls/<n>/merge` with `"sha": "<H>"`. GitHub
  refuses that request if the head has moved. Prefer REST, because
  `gh pr list` returned "HTTP 403: GitHub GraphQL is not available from Claude Code
  sessions". RCF-1's receipt records an `expectedHeadSha` pin.
- (c) The merge method is the merge agent's choice within repository practice: #661
  and #680 were squashed, #679 used a merge commit. If squashed, H is not an ancestor
  of the merge commit (APR-107's lesson). With a merge commit it is. The receipt
  records the method and the result of `git merge-base --is-ancestor H <merge>`.

**The ID.**
- On `origin/main` = `52289779` there are 119 unique entries, maximum 119, and
  `sort | uniq -d | wc -l` → `0`.
- There are no open pull requests, so the open-PR enumeration printed nothing.
- **The next free ID is `AEGIS-APR-120`.**
- P-REG's author re-derives it when writing, and P-REG's merge agent re-derives it
  again at merge (AC-R2).
- The #679 conflict concern (rev1 Q6) is **moot**.

### 6.4 Draft entry, written by P-REG's Stage C once the §6.3 entry condition holds

`<…>` marks a value filled from live measurement. Each owner quotation stays on one
line (`docs/delivery-workflow.md:813-825`). The Q2/Q4 quotations depend on OQ-A.

```markdown
### AEGIS-APR-120: PR #<P-FIX> one-time gate-guard exception for the Errno 39 test fix

- **Event:** GRANT — one-time, bound to one exact head. Not a standing exception and
  not a policy decision.
- **Status at recording:** ACTIVE and **unspent** as recorded. It is consumed by the
  merge of PR #<P-FIX> at the exact head named below, and by nothing else. It cannot
  authorize the merge of the pull request that records it. Its consumption will be
  recorded in the next register pull request, as the owner chose (Q3 below).
- **Date / Grantor:** 2026-10-08 / Peter Nguyen.
- **Reason:** [PR #<P-FIX>](https://github.com/ModernNomad-98/Project-Aegis/pull/<P-FIX>)
  stops the intermittent `OSError: [Errno 39] Directory not empty` raised by
  `ProtectedFileGuardTests.run_guard` (runs 36695924676 and 37713171379): a detached
  Git auto-maintenance repack wrote into the fixture repository while
  `TemporaryDirectory` removed it. The PR adds the two lines that disable
  auto-maintenance in that fixture repository and one regression test proving no
  auto-maintenance process starts. It changes only `scripts/tests/test_offline_ci.py`,
  which the protected-path pattern matches, so `gate-guard` fails by construction.
  AEGIS-APR-047 does not reach it: its Scope FORBIDDEN keeps "guard scripts and tests"
  for "separate one-time owner decisions".
- **Owner decision:** In the Project Aegis session on 2026-10-08 the owner was asked,
  verbatim:

  > main's CI failure was a rare race in one CI test: Git 2.55 starts a background clean-up job in a throwaway test folder, and the test deletes the folder while that job is still writing. The one re-run passed, so main is green again, and the same race has happened once before (2026-09-30). The proposed fix adds two lines to scripts/tests/test_offline_ci.py telling Git not to run that background job in the test's folder. scripts/ is protected, so a fix PR's protected-file guard (gate-guard) will be red until you grant a one-time exception for that exact PR commit. Do you want the fix?

  and selected "Yes, one-time exception (Recommended)", whose option text reads:

  > A third PR touching only that test file, on a third branch, through all seven stages. It merges once gate-guard's red is covered by your one-time exception for that exact commit, recorded in the register, with every other check green. Admin merge allowed.

  Asked whether this register pull request may be opened and merged — verbatim:

  > <Q2 question, one line, as confirmed under OQ-A>

  the owner chose "Yes, same terms (Recommended)": "<Q2 option text, as confirmed>".
  For a head that moves after recording, the owner chose "Ask me again
  (Recommended)": "<Q4 option text, as confirmed>". For the consumption record, the
  owner chose "Batch it later (Recommended)": "<Q3 option text, as confirmed>".
  <If OQ-A leaves the Q3/Q4 question texts unrelayed: "The Q3 and Q4 question texts
  were not relayed verbatim; only the coordinator's labels '(consumption record)' and
  '(fix head moves after the exception is recorded)' were.">

  These are transcriptions of selections relayed through the coordinating agent, not
  the owner typing into this register. The preamble makes them valid source evidence
  — "Current direct user instructions are valid source evidence before transcription
  and do not need repeated consent" — and this entry does not claim a repository
  citation of the owner's own text.
- **Scope allowed:** One `gate-guard` exception and an administrator merge of
  PR #<P-FIX> at exact head `<H>` (tree `<T>`, base `<B>`), and nothing else. The head
  changes one file, `scripts/tests/test_offline_ci.py`, `+<a>/−0`: the two
  configuration lines the question described, plus their comment, one `mock` import
  and one regression test. At that head `gate-guard` (check run `<id>`, workflow run
  `<id>`) concluded FAILURE with `Gate files touched:` naming only
  `scripts/tests/test_offline_ci.py`; `changes` and `validate-skills` concluded
  SUCCESS; `windows-offline-checks`, `tools-tests-linux` and `tools-tests-windows` were
  skipped by the workflow's path filter. The `gate-guard` failure is recorded here as
  **failed with an authorized disposition — not waived, and not a pass**. In the
  owner's words the merge also requires "every other check green" at that head and the
  PR to have gone "through all seven stages".
- **Scope FORBIDDEN:** No other pull request, head, path or failed check is covered
  ("only that test file", "for that exact commit", "every other check green"). It is
  one-time and not a standing exception; it does not widen AEGIS-APR-047 and changes
  no `gate_pattern`, branch protection or workflow. If the head moves after this entry
  is on the default branch, it is spendable on nothing, and a new exception needs the
  owner's fresh answer ("Ask me again", above), following AEGIS-APR-032→033→034.
- **Evidence:** The owner's question and selections above, relayed through the
  coordinating agent and recorded by it at 2026-10-08T15:28:53Z (grant), 16:01:16Z
  (Q2–Q4) and 16:10:40Z (question text and the one-line option text, which the
  coordinator confirmed as the form the owner saw); session artifacts, not repository
  artifacts. Repository artifacts that independently record the facts above: the
  Stage D audit of PR #<P-FIX> <comment link> and the `gate-guard` job log at the head.
  The head, tree, base, path, `+<a>/−0` and check conclusions were re-measured from
  `git` and the GitHub API for this entry, not taken from a brief.
- **Expiry / use limit:** One use: one merge of PR #<P-FIX> at the named head,
  consumed by that merge. No calendar expiry stated.
```

**`scoped-approval-register` checks on this draft.**
- The scope is verbatim.
- The proposal context is present (RC6b).
- Every FORBIDDEN clause comes from the owner's wording or from the owner's Q4
  answer, or states a fact. Nothing is invented.
- The one-use limit comes from "one-time … for that exact commit".
- Consumption is a later appended event, timed by Q3.
- The draft contains no secret.
- The Stage F link is gone (RC4/RC6d). P-FIX's `SD-F: ACCEPT` is a merge precondition
  only (§6.3).

### 6.5 Authority for P-REG

- **Work and merge authority:** the owner's Q2 answer, quoted in full in §6.2: "Yes,
  same terms (Recommended)", on the terms "all seven stages, all checks green, admin
  merge allowed". The coordinator recorded it at 16:01:16Z.
- **Supporting mechanics, not the sole authority:** AEGIS-APR-100, AEGIS-APR-048, and
  AEGIS-APR-050 (wait for the automated review).
- **Skipped jobs.** The coordinator's Q1 reading also applies to P-REG. On a
  register-only change the three path-scoped jobs are skipped by design. They are
  recorded as skipped, never as green.
- **BRIEF-COMMON rule 5's register default** is overridden by the CIFIX brief, the
  owner's "recorded in the register" and the owner's Q2 answer. Stage B explicitly
  accepted this override (audit §2.6).

### 6.6 Consumption (owner Q3: "Batch it later")

**Not in CIFIX-1.** The CONSUMED event for AEGIS-APR-120 is appended in **the next
register pull request, which also records FU-2's AEGIS-APR-119 as used up.** Its ID is
re-derived when that pull request is written. Rev1's "expected 121" is dropped. The
template is APR-107.

**What CIFIX-1 must leave behind.** P-FIX's Stage G merge receipt records everything
that later entry needs:

| Fact | Content |
| --- | --- |
| Merge time | UTC |
| Merge method | squash or merge commit |
| Merge commit SHA | 40 characters |
| Ancestry result | `git merge-base --is-ancestor <H> <merge>`: exit 0 (merge commit) or 1 (squash), with the sentence that the bound head is H, not the merge commit |
| Exact-head pin | the evidence used (REST `sha`) |
| `gate-guard` disposition | "failed with an authorized disposition (AEGIS-APR-120)" |
| Post-merge push run | its result |

---

## 7. Acceptance criteria

**Notation.**
- `B`: P-FIX's base, as re-measured in §5.0.
- `H`: P-FIX's 40-character head.
- `T(x)`: `git archive x | tar -x -C $S/cifix/verify/<name>`.
- `G55`: `$S/git-build/install/bin`.

Every local run uses a scratch `TMPDIR`, `GIT_CONFIG_GLOBAL=/dev/null`,
`PYTHONDONTWRITEBYTECODE=1` and `python3 -B -P`.

Git is selected per run: Git 2.55 with `PATH=G55:$PATH`; the system Git 2.43.0 by
leaving `PATH` as it is.

### 7.1 P-FIX

**AC-F1 — One file changes, and only by additions.**
- Commands: `git diff --numstat B...H` and `git diff -U0 B...H | grep -c '^-[^-]'`.
- Expected: one line, `<a>	0	scripts/tests/test_offline_ci.py`, with `a` ≤ 40 (the
  prototype has 28), and `0`.
- The `numstat` deletions column governs. The grep alone does not count a removed
  blank line (audit N2).

**AC-F2 — No test is weakened, skipped or retried.**
- Command: `git diff B...H | grep -inE '^\+.*(skip|expectedFailure|ignore_cleanup_errors|retry|sleep|timeout)'`.
- Expected: no output, exit 1.

**AC-F3 — Exactly one test method is added and none is removed (RC10).**
- Commands:
  - `python3 -I $S/cifix/scripts/test_names.py <T(B)>/scripts/tests/test_offline_ci.py <T(H)>/scripts/tests/test_offline_ci.py`
    (sha256 first 16 `8564d05454f8ef48`).
  - `python3 -I -B $S/cifix/scripts/count_fixtures.py <T(B)>` and the same for `<T(H)>`.
- Expected:
  - `added: ['ProtectedFileGuardTests.test_fixture_repository_starts_no_auto_maintenance'] removed: [] base=<n> head=<n+1>`.
    At `52289779` this was `base=38 head=39`.
  - `count_fixtures.py` gives fixtures and methods B: 88/38 → H: 89/39, using the
    re-measured B values.

**AC-F4 — No auto-maintenance process starts on any fixture path.**
- Commands: `trace_count.sh <T(H)> head-243` and `trace_count.sh <T(H)> head-255 G55`.
- Expected, for both: `OK Ran 11 tests` and
  `maintenance_child_start=0 gc_auto_child_start=0 maintenance_processes=0`.
- On `T(B)` the same commands give 264.

**AC-F5 — The regression test flips deterministically (RC10).**
- Commands:
  1. `cp -r <T(H)> <R>`.
  2. `sed -i '/git("config", "maintenance.auto", "false")/d; /git("config", "gc.auto", "0")/d' <R>/scripts/tests/test_offline_ci.py`.
     Check that `wc -l` drops by exactly 2.
  3. In `<R>` and then in `<T(H)>`, run
     `python3 -B -P scripts/tests/test_offline_ci.py ProtectedFileGuardTests.test_fixture_repository_starts_no_auto_maintenance`
     5× each, once with `PATH=G55:$PATH` and once with the system `PATH`.
- Expected:
  - `<R>`: 5× `FAILED (failures=1)` on each Git, and the log contains
    `AssertionError: Lists differ: [] != [['git', 'maintenance', 'run', '--auto', …`.
    Read this as "the assertion failure is present"; a rare extra cleanup error is
    allowed (audit N4).
  - `<T(H)>`: 5× `OK` on each Git.

**AC-F6 — There is no race under a forced trigger, and the race reproduces before the
fix.**
- Commands: `ab_force.sh <T(B)> base-force 3 1 G55` and
  `ab_force.sh <T(H)> head-force 10 1 G55`.
- Expected:
  - B: `fail>=1 errno39_lines>0`.
  - H: `pass=10 fail=0 errno39_lines=0 leftover_tmp=0`.

**AC-F7 — Natural stress at H passes on Git 2.55.**
- Command: 20× `python3 -B -P scripts/tests/test_offline_ci.py` in a scratch
  `git clone --shared` at H, with `PATH=G55:$PATH`.
- Expected: 20× `OK (skipped=1)`, and 0 lines contain `Errno 39`.

**AC-F8 — The full file passes at H on both Git versions.**
- Command: the same file in the same clone, once per Git.
- Expected: exit 0, `Ran <n+1> tests`, `OK (skipped=1)`. At `52289779` this was
  39 tests.

**AC-F9 — The repository checks are unchanged at H.**
- Commands: the five §5.0 commands other than `test_offline_ci.py`, run at H.
- Expected: each exits 0 with the **same summary line as at B**. At `52289779` the
  lines were 195 / 181 / 76 / `Ran 23 tests … OK`.

**AC-F10 — The guard and workflow are untouched, and the commit is signed off.**
- Commands: `git diff --quiet B...H -- .github/ ; echo $?`,
  `git log --format=%B B..H | grep -c '^Signed-off-by:'` and
  `git rev-list --count B..H`.
- Expected: `0` ; `1` ; `1`.

**AC-F11 — CI at the exact head is as designed.** Not verifiable before publication
(declared in §2).
- Command:
  `gh api repos/ModernNomad-98/Project-Aegis/commits/H/check-runs --jq '.check_runs[]|"\(.name) \(.status) \(.conclusion)"'`,
  plus the job logs.
- Expected:
  - `changes completed success`.
  - `validate-skills completed success`. Its log shows `Ran <n+1> tests` and
    `OK (skipped=1)` for ci-tests, and `OK (skipped=5)` for BER. Those skip counts
    match comparison run 37709031628 (lines 958 and 4538) and run 37713171379
    attempt 2 (lines 946 and 4526).
  - **`gate-guard completed failure`**, with the log lines `Gate files touched:`, then
    exactly `scripts/tests/test_offline_ci.py`, then
    `… requires manual review and merge.`
  - **`windows-offline-checks`, `tools-tests-linux` and `tools-tests-windows`:
    `completed skipped`**, with `changes` outputs `tools=false` and `offline=false`.
    These are recorded as skipped, never as passed.

**AC-F12 — The local runs leave nothing behind (RC10).**
- Commands: `git status --porcelain` in the real checkout after all local runs, and
  `ls -A <TMPDIR>` after the H runs.
- Expected: both outputs are empty. An empty TMPDIR means no `aegis-ci-guard-*`,
  `aegis-ci-trace-*` or any other leftover.

### 7.2 P-REG

Notation: `Bʳ` is P-REG's base and `Hʳ` its head. Set `f=docs/approvals/APPROVAL_REGISTER.md`.

**AC-R1 — The change is an append-only, end-of-file addition (RC7).**
- Commands:
  - `git diff --numstat Bʳ...Hʳ`
  - `git show Bʳ:$f > b.md; git show Hʳ:$f > h.md; cmp -n "$(stat -c %s b.md)" b.md h.md; echo $?`
  - `git diff -U0 Bʳ Hʳ -- $f | grep '^@@'`
  - `wc -l < b.md`
  - `tail -c1 h.md | od -An -c`
- Expected:
  - one line, `<n>	0	$f`;
  - `0`, meaning the base blob is a byte prefix of the head blob, so no prior byte
    changed;
  - exactly one hunk, `@@ -<L>,0 +<L+1>,<n> @@`, where `L` is the `wc -l` count;
  - a trailing `\n`.
- These commands were validated on a scratch simulation at `c1acc075`: `cmp rc=0` and
  `@@ -5154,0 +5155,4 @@` with `L=5154`. The base ends in `\n`, per
  `git show origin/main:$f | tail -c 1 | od -c`.

**AC-R2 — The new ID is the next free one and unique (RC10, GAP3).**
- Commands:
  - `git show Hʳ:$f | grep -o '^### AEGIS-APR-[0-9]*' | sort | uniq -d | wc -l`.
  - `git show origin/main:$f | grep -o '^### AEGIS-APR-[0-9]*' | sed 's/.*-//' | sort -n | tail -1`.
  - For every open pull request except P-REG itself:
    `gh api 'repos/ModernNomad-98/Project-Aegis/pulls?state=open&per_page=100' --jq '.[].number' | while read n; do git fetch -q origin "pull/$n/head" && echo "PR$n $(git show FETCH_HEAD:$f | grep -o '^### AEGIS-APR-[0-9]*' | sed 's/.*-//' | sort -n | tail -1)"; done`.
- Expected: `0`, and the new ID is greater than every printed maximum. At writing the
  main maximum was 119 and there were no open pull requests, so the ID is 120.
- Run this when writing and again **at P-REG's merge**.

**AC-R3 — The owner's option text is byte-exact and on one line.**
- Command: `grep -cF "<the 255-char option text of §6.2>" h.md`.
- Expected: `1`.

**AC-R4 — The new entry names P-FIX's head, tree, base, path and numstat, matching
live git (RC10).**
- Commands:
  - `awk '/^### AEGIS-APR-120:/,0' h.md > e.md`
  - `grep -c '<H>' e.md`, and the same for `<T>`, `<B>`, `scripts/tests/test_offline_ci.py` and `+<a>/−0`
  - recompute `git rev-parse H^{tree}`, the merge base and the `numstat`.
- Expected: each count ≥ 1, and each value equals live git.

**AC-R5 — The repository checks pass.**
- Commands: `validate-skills.py` ; `test_validator.py` ;
  `python3 -B -P scripts/ci/check-markdown-links.py $f`.
- Expected: exit 0 for each. The reference link check at `52289779` was
  `files: 1 links checked: 49 anchors checked: 11 broken: 0 dead: 0`. The new entry
  may raise the links count, but broken and dead must stay at 0.

**AC-R6 — CI at Hʳ is green.**
- Command: the check-runs command at Hʳ.
- Expected: `changes`, `validate-skills` and **`gate-guard`** conclude success. The
  three path-scoped jobs are skipped and recorded as skipped.

**AC-R7 — P-REG's merge comes after P-FIX's settled review state, and no head moved
(GAP2).** Checked by P-REG's merge agent in the same turn as the merge.
- Expected, before the merge:
  - P-FIX `SD-F: ACCEPT` is posted, naming the entry's H.
  - P-FIX's MG3 is settled at H.
  - `gh api …/pulls/<P-FIX> --jq .head.sha` equals H.
- Expected after the merge: the `merged_at` of Hʳ is later than both events above.

**AC-R8 — The entry carries the owner's proposal context and the Q2/Q3/Q4 answers
(GAP1, RC6).**
- Command: `grep -cF` on `e.md` for each of:
  - the 588-character question text;
  - `Yes, one-time exception (Recommended)`;
  - `Yes, same terms (Recommended)`;
  - `Ask me again (Recommended)`;
  - `Batch it later (Recommended)`.
- Expected: `1` or more for each.
- The confirmed Q2/Q4 option texts are checked as well, once OQ-A is answered.

---

## 8. PR body outlines

### 8.1 P-FIX body

The body follows `.github/pull_request_template.md` on `main`. At `52289779` (after
#680) the template already carries the sentinels: `grep -n 'bound-field'` finds them
at L64/70, L78/83 and L93/106. Keep every sentinel line exactly as it is, and never
write the Codex trigger phrase.

1. **`## What & why`.** The plan in a few sentences: what, why, blast radius, path,
   and the acceptance-criteria list (AC-F1..F12 or a link to the audited plan
   revision). Then:
   - **Audited plan revision:** the sha256 of the plan file Stage B accepted.
   - The root cause, the two run IDs and the Git 2.55 mechanism.
   - N1: under a forced trigger the race also fails the second commit.
   - The sentence: "gate-guard will be red by design; it is covered only by the
     one-time owner exception AEGIS-APR-120, recorded in a separate register PR
     (#<P-REG>, opened after this PR's Stage D audit and merged before this PR),
     which names this exact head."
2. **`## Checklist`.** Mark the Windows and tools jobs as "skipped by path scope".
3. **The skills table**, between `<!-- bound-field: skills -->` and
   `<!-- bound-field: end -->`. It has four columns, and each stage agent writes its
   own row.
4. **The security answer**, between `<!-- bound-field: security -->` and
   `<!-- bound-field: end -->`:
   `- [x] Yes — surface(s) touched: scripts/ (scripts/tests/test_offline_ci.py, a path the protected-file guard matches)`
   / `- [ ] No`. MG5 is not applicable under its scope clause (not an outside
   contribution).
5. **The witness**, between `<!-- bound-field: witness -->` and
   `<!-- bound-field: end -->`, with eight rows:
   - sites 1–5 and 8: `unchanged-and-verified`, evidence
     `git diff --quiet B...H -- docs/delivery-workflow.md; echo $?` → `0`;
   - site 6: `git diff --quiet B...H -- AGENTS.md` → `0`;
   - site 7: the body's only rule-bearing content is the witness, the skills table
     and the divergence table.
6. **Divergence table.** "Not applicable: AGENTS.md and no MG/SD condition changed."
7. **Evidence.**
   - Before and after results for AC-F4..F7.
   - The UNRUN list: pwsh acceptance and Python 3.14 (covered by `validate-skills`
     at H), and Windows (the path filter skips `windows-offline-checks`; the class
     skips on Windows; the post-merge push run covers it).
   - The handoff block.
8. **Attribution.** The closing lines that the session's PR attribution reminder
   specifies.

### 8.2 P-REG body

The same template sections and sentinels, with these differences:
- **What & why:** records the owner's one-time exception for PR #<P-FIX> at `<H>`,
  why it is a separate pull request (§1), and the Q2 answer as its authority.
- **Security answer:** `Yes — the owner approval register (docs/approvals/APPROVAL_REGISTER.md)`.
- **Witness:** as in P-FIX.
- **Evidence:** the full entry text, plus the outputs of AC-R1, AC-R2, AC-R3, AC-R4
  and AC-R8.

---

## 9. Stage-specific notes

### All stages

- Re-derive every head, base, check result and register fact in the same turn as the
  action that relies on it.
- A moved head voids every verdict bound to it.
- `gate-guard` red on P-FIX is expected. It must be the **only conclusion that is
  neither success nor skipped**, and it must be red **only** for the protected-path
  match, with exactly one path.
- Never write the Codex trigger phrase. No reserved scope.

**Separation, beyond "no agent holds two stages of one change" (RC8):**
- (i) P-REG's entry author (its Stage C) is neither P-FIX's Stage C author nor P-FIX's
  Stage G merge agent.
- (ii) **P-FIX's Stage G holder holds no stage of P-REG.** The agent that spends
  AEGIS-APR-120 did not author, audit, validate, review or merge it.

### P-FIX Stage C

1. Run §5.0 and apply its scope-lock rule.
2. Create `claude/sharp-lovelace-urgxpz-ci-fix` from B.
3. Implement P1–P7.
4. Run AC-F1..F10 and AC-F12 locally.
5. Push, and record H, `git rev-parse H^{tree}` and B (SD-C).
6. Open the pull request with the §8.1 body and the accepted plan hash.

### P-FIX Stage D

Use `code-reviewer`: this is a CI test-code diff, not a skill-library pull request.
Verify the skill's scope before relying on it.
1. Check AC-F1..F10 and AC-F12 one by one at H, recording MET, NOT MET or UNRUN.
   AC-F11 may be UNRUN until CI completes, as declared in §2.
2. Confirm P4/P5, and that the config lines come before the first commit.
3. Confirm the liveness assertion and AC-F5, so the test cannot pass vacuously.
4. Post the verdict naming H.
5. Your ACCEPT, together with AC-F11's completed check set, is P-REG's Stage C entry
   condition (§6.3).

### P-FIX Stage E

1. Run §5 at H, and the local `validate-skills` job steps.
2. List as UNRUN, each with its coverage:
   - pwsh `acceptance-core` and Python 3.14, covered by `validate-skills` at H;
   - Windows (N3).
3. Collect AC-F11 from the run-level state. Confirm the three skips come from
   `changes` outputs.
4. Disposition: `SD-E: PASS` or `SD-E: INCOMPLETE — UNRUN LISTED`.

### P-FIX Stage F

Use `code-reviewer`.
1. The verdict names H.
2. Check the skills table against the work.
3. Check the security answer is "Yes: scripts/" and the witness has eight rows.
4. Compute the bound-field hash (sha256, first 16, whole-line sentinels) and name it.
5. Accept the Stage E unrun list.
6. Your ACCEPT is one of P-REG's merge preconditions (§6.3, AC-R7).

### P-REG stages C–G

Holders must be distinct from each other and satisfy (i) and (ii).
- **C:** start only when §6.3's entry condition holds.
  1. Obtain the OQ-A confirmations from the coordinator.
  2. Write the §6.4 entry from live values.
  3. Run AC-R1..R5 and AC-R8.
  4. Open the pull request.
- **D/F:** use `code-reviewer` and the `scoped-approval-register` validation
  checklist; verify each skill's scope. Check:
  - the verbatim quotes, against `$S/cifix/BRIEF.md` and the coordinator's
    confirmations;
  - the head values, against live git;
  - append-only, by AC-R1;
  - no invented restriction.
- **E:** the checks plus CI (AC-R6).
- **G:**
  1. Confirm authority: the owner's Q2 answer quoted verbatim in the brief with its
     source, and AEGIS-APR-100/048/050.
  2. Confirm every check is green, including `gate-guard`. Skips are recorded as
     skipped.
  3. Confirm the automated review has posted at Hʳ or is confirmed unavailable, and
     triage P0–P2 findings.
  4. Check **AC-R7** and re-run **AC-R2**.
  5. Merge, pinned to Hʳ.
  6. If a new register entry lands on `main` first, rebase. That moves Hʳ, so D/E/F
     must be taken again.

### P-FIX Stage G

Do all of these in one turn, before merging.
1. `gh api …/pulls/<P-FIX> --jq .head.sha` must equal the H that AEGIS-APR-120 names.
2. Run `git fetch origin main`, then
   `git show origin/main:docs/approvals/APPROVAL_REGISTER.md | awk '/^### AEGIS-APR-120:/,/^### AEGIS-APR-121:/'`.
   The entry must name H and pass the preamble test. That means no later lifecycle
   event for APR-120 (`grep -n 'AEGIS-APR-120'` across the file), and a scope that
   covers this head and path.
3. **MG1.**
   - `gate-guard` is failure, and its log shows only `scripts/tests/test_offline_ci.py`
     under `Gate files touched:`.
   - `changes` and `validate-skills` are success.
   - The three path-scoped jobs are skipped and recorded as skipped (coordinator Q1
     reading).
   - Record `gate-guard` as "failed with an authorized disposition (AEGIS-APR-120)".
4. **MG2.** The `SD-F: ACCEPT` names H. Recompute the bound-field hash from the live
   body; it must equal the verdict's hash.
5. **MG3 / AEGIS-APR-050.** The automated review result is for H, or the review is
   confirmed unavailable for H. P0–P2 findings are triaged. Bind findings with
   `original_commit_id`.
6. **MG4.** The register entry on `main`, plus the owner's option text quoted verbatim
   in the brief with its source.
7. **MG5.** Not applicable, by its scope clause.
8. **Head move.** If the head moved at any point after APR-120 merged, **do not
   merge.** Return the work to the coordinator for the owner question (§6.3).
9. **Merge.** Administrator merge ("Admin merge allowed"), **pinned to H** (§6.3 b).
10. **Receipt.** Post it keyed by MG ID, including **every §6.6 fact** for the
    batched consumption event.
11. **Post-merge.** Observe the push-to-`main` run at the merge commit. A push runs
    all jobs, which is the Windows evidence; `gate-guard` is skipped on push. Record
    the result. If the run is red, the owner's failure-handling instruction applies:
    diagnose and fix, never re-run to green without a diagnosis.

There is no P-CONS step in CIFIX-1 (owner Q3).

---

## 10. Sequence and ETA

The durations are estimates; none is measured. The coordinator owns the official
per-item announcements.

| Step | Gate to start | ETA (estimate) |
| --- | --- | --- |
| B re-audit of rev2 | this file's sha256 | 10–20 min |
| P-FIX C, including §5.0 | `SD-B: ACCEPT` | 20–35 min |
| CI on H | push | a few minutes (unverified for H) |
| P-FIX D | SD-C COMPLETE | 20–30 min |
| P-REG C → F | P-FIX `SD-D: ACCEPT` + AC-F11 completed | overlaps P-FIX E/F; the owner's Q2 option text estimates "About 30–45 extra minutes" |
| P-FIX E, F | chain | 20–30 min each |
| P-REG G | AC-R7 (P-FIX SD-F + MG3 settled, head unchanged) | 10–15 min |
| P-FIX G + receipt + post-merge run | AEGIS-APR-120 on `main` | 15–25 min |

---

## 11. Open questions for the coordinator

### Closed, recorded for traceability

| Q | Closed by |
| --- | --- |
| Q1 skipped jobs vs. "every other check green" | Coordinator procedural position: recorded as skipped, as in #677/#678. Stage B verified that precedent. Applied in AC-F11, AC-R6 and §9. |
| Q2 the fourth pull request | Owner: "Yes, same terms (Recommended)" (§6.2, §6.5) |
| Q3 consumption | Owner: "Batch it later (Recommended)" (§6.6) |
| Q4 head moves after recording | Owner: "Ask me again (Recommended)" (§6.3) |
| Q5 the regression test | Coordinator: keep it. Stage B: keep it. |
| Q6 the #679 collision | Moot: #679 merged at 15:55:22Z |

### Remaining

None of these blocks Stage B. OQ-A blocks P-REG's Stage C text only.

- **OQ-A: one-line forms and missing question texts for Q2–Q4.**
  - The brief wraps the Q2 question and the Q2, Q3 and Q4 option texts across indented
    lines. This plan joined them with single spaces, so the forms are
    reconstructions. The audit's RC6c logic applies to them as well; only the
    255-character grant option has the coordinator's one-line confirmation.
  - The brief carries no verbatim question text for Q3 or Q4, only the labels
    "(consumption record)" and "(fix head moves after the exception is recorded)".
  - **Request:** the coordinator relays the one-line forms of the Q2 question and the
    three option texts, and the verbatim Q3/Q4 questions, before P-REG's Stage C. If
    the Q3/Q4 questions are unavailable, the entry says so explicitly; the §6.4
    placeholder already allows for this.
- **OQ-B: "adds two lines" versus the regression test.**
  - The question the owner answered said "The proposed fix adds two lines to
    scripts/tests/test_offline_ci.py". The head will add those two lines plus a
    17-line regression test, an import and a comment: +28/−0 in the prototype.
  - The grant's own scope is the option text, "touching only that test file", which
    the head satisfies. The coordinator's Q5 position is to keep the test.
  - **Request:** confirm whether the owner should be told that the head is larger
    than "two lines" before the exception is spent. The entry states the real size
    either way (§6.4 Scope allowed). The planner does not resolve this.
- **OQ-C: dependence on the "recorded = merged on main" reading.** The coordinator is
  telling the owner about this reading. If the owner rejects it, a head move *before*
  P-REG merges also requires an owner question (§6.3). No action is needed unless the
  owner objects.

---

## 12. RC1–RC10: where each is addressed

| RC | Requirement | Addressed in |
| --- | --- | --- |
| RC1 | Apply the owner's Q2 answer; update the brief hash; Q2 as authority for P-REG, stated as worded; the Q1 reading applies to P-REG; APR-100/048/050 as support; remove the "confirm" dependencies | Header input table (`5729b391…`, superseding the audit's `5419a0da…`); §1 "Why two pull requests"; §2 P-REG approval path; §6.2 (Q2 verbatim); §6.5; §11 closed table |
| RC2 | Apply Q3; remove P-CONS; the receipt carries what the later entry needs | §1 Paths ("Out of CIFIX-1"); §6.6 (no "expected 121"; receipt facts, APR-107 template); §7 (no §7.3); §9 P-FIX G steps 10 and closing line; §10 (no P-CONS row) |
| RC3 | Apply Q4 as a procedure; state the "recorded = merged" reading and flag it | §6.2 (coordinator's reading, 16:10:40Z); §6.3 "If the head moves" (before or after P-REG merged, EXPIRED + new GRANT only after a fresh owner answer); §9 P-FIX G step 8; §11 OQ-C |
| RC4 | Remove the Stage F link from the entry; the P-REG Stage C entry condition = P-FIX `SD-D: ACCEPT` + completed CI with the expected conclusions | §6.3 "When P-REG's Stage C may start"; §6.4 Evidence (Stage D only); §6.4 checks; §9 P-FIX D step 5 |
| RC5 | P-REG merges only after P-FIX `SD-F: ACCEPT` and MG3 at H, with no head move | §6.3 "When P-REG may merge" (a)–(d); AC-R7; §9 P-REG G, P-FIX F step 6 |
| RC6 | (a) Q2/Q4 (and Q3) verbatim in the entry; (b) proposal context; (c) one-line confirmation; (d) no Stage F link | §6.2 (all texts, hashes, `EQUAL: True` for the confirmed option text); §6.4 Owner decision / Status / Scope FORBIDDEN / Evidence; AC-R3, AC-R8; residual reconstruction caveat as OQ-A |
| RC7 | A real append-only proof: byte prefix, single trailing hunk, trailing newline | AC-R1 (commands validated on a scratch simulation: `cmp rc=0`, `@@ -5154,0 +5155,4 @@`, base ends with `\n`) |
| RC8 | P-FIX's Stage G holder holds no P-REG stage; keep the author rule | §9 "All stages", separation (i) and (ii) |
| RC9 | (a) the base moved: re-derive figures, Q6 moot; (b) the "append-only rule governs merged entries" attribution; (c) "The PR cannot create that entry…" attribution | (a) Header base `52289779`, §3 "The base moved" (rc 0), §5.0 re-measure block with values at `52289779`, §6.3 ID (119 → 120, no open pull requests), §11 Q6; (b) §6.1 corrections and §6.3 "Before P-REG has merged"; (c) §1 "Why two pull requests" and §6.1 |
| RC10 | Concrete AC-F3, F5, F12, R2, R4 | AC-F3 (`test_names.py`, run output shown); AC-F5 (exact `sed`, Git selection, expected assertion); AC-F12 (TMPDIR empty); AC-R2 (open-pull-request enumeration loop, run at writing); AC-R4 (`awk` extraction) |

Audit notes N1–N5 are carried as follows:
- N1: §1 and §3.5.
- N2: AC-F1.
- N3: §2 item 5, §8.1 item 7 and §9 Stage E.
- N4: AC-F5.
- N5: §6.3(b).

Gaps GAP1–GAP3 are covered by AC-R8, AC-R7 and AC-R2 respectively.

---

## 13. Handoff block

1. **Decision IDs.**
   - Still binding: `SD-A`–`SD-G` and `MG1`–`MG5`, unchanged.
   - Relied on: AEGIS-APR-047 (does not cover this change), 048, 050, 100, 106/107,
     and the precedents 032/033/034.
   - Owner decisions used: 2026-10-08, grant + Q2/Q3/Q4.
   - The proposed new entry, AEGIS-APR-120, is drafted, not written.
2. **Changed files: none.**
   - Real checkout: `git status --porcelain | wc -l` → `0`;
     `git rev-parse HEAD` → `c060a7cb…` (detached, unchanged);
     `git for-each-ref refs/remotes/pr | wc -l` → `0`.
   - Read-side metadata: `git fetch origin main` refreshed `origin/main` to
     `52289779`, and `git fetch origin pull/680/head` wrote `.git/FETCH_HEAD`.
   - Scratch files written:
     - this file;
     - `$S/cifix/scripts/test_names.py`;
     - `$S/cifix/verify2/**`, including a scratch `git clone --shared` with one
       never-pushed simulation commit made to validate AC-R1. The clone was left
       checked out at `52289779`.
   - **Not touched:** every repository path; GitHub (reads only).
3. **Proven invocation.** Every figure carries its command and output. These remain
   unverified:
   - the runner's Git build options;
   - old-Git `gc --auto` coverage;
   - the one-line forms of the Q2–Q4 texts (OQ-A);
   - the CI duration for H;
   - branch-protection `strict`, which returned 403.
4. **Deviation flags.**
   - The plan adds a regression test beyond the diagnosis diff. Q5 kept it, and it
     raises OQ-B.
   - The figures moved from `c060a7cb` to `52289779`. The values are identical.
5. **Continuation.** Stage B re-audits this file at its sha256. On `SD-B: ACCEPT`,
   P-FIX Stage C begins at §5.0. P-REG Stage C begins when §6.3's entry condition
   holds, after the coordinator answers OQ-A.

## 14. Evidence index (scratch)

| File | sha256 first 16 |
| --- | --- |
| `$S/cifix/scripts/trace_count.sh` | `56ebea49c320effe` |
| `$S/cifix/scripts/ab_force.sh` | `149d3b3bff39a56b` |
| `$S/cifix/scripts/add_regtest.py` | `cceda7bf8c14dd99` |
| `$S/cifix/scripts/count_fixtures.py` | `e07d5bcf8e05c9a0` |
| `$S/cifix/scripts/test_names.py` | `8564d05454f8ef48` |
| `$S/cifix/prototype-reference.diff` | `a4ad6f9fdcd63446` |
| Run outputs | rev1 runs in `$S/cifix/verify/**`; rev2 baselines, flip re-check and AC-R1 simulation in `$S/cifix/verify2/**` |

**Finish:** the finish timestamp is reported in the handoff message, after this file's
hash was taken, so that recording it does not change the hash.
