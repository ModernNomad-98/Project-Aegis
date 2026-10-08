# CIFIX-1 — Stage A PLAN, revision 1

**Item:** CIFIX-1, "Fix the Errno 39 race in `scripts/tests/test_offline_ci.py`".
**Stage held:** A (PLAN) only. This agent writes no repository file, commits nothing,
pushes nothing, opens no PR and merges nothing.
**Repository / role:** `/home/user/Project-Aegis`, Role A. The four source landmarks
are present (`head -3 README.md` → `# Project Aegis`; `ls` found
`docs/skills-catalog.md`, `scripts/validate-skills.py` and
`artifacts/audits/skill-contract-audit-baseline.json`).
**Base at planning time:** `origin/main` = `c060a7cb09758fa2f4f6b67ab00094f01d7c6a46`
(`git ls-remote origin refs/heads/main`, re-run at 2026-10-08T15:46:29Z). Stage C must
re-derive the base. Open PRs at that time: #679 `1d1a5096…` and #680 `33200aea…`.
Neither touches `scripts/tests/test_offline_ci.py`; their file lists come from
`gh api repos/ModernNomad-98/Project-Aegis/pulls/{679,680}/files`.
**Started:** 2026-10-08T15:29:52Z (`date -u`). The finish time is at the end of this file.
**Scratch root:** `S=/tmp/claude-0/-home-user-Project-Aegis/0168d1d5-9af4-5a74-a8dd-9a35339e53ab/scratchpad`.

Inputs that bind this plan, with their sha256 values from `sha256sum`:

| Input | sha256 |
| --- | --- |
| `$S/cifix/BRIEF.md` (the owner's verbatim instruction) | `041d76ab0ebfefb3c74751f3e5ba41fb9bfd56de525e44168b301c86c3cebb1c` |
| `$S/ci-diag/DIAGNOSIS.md` | `522ea312e15f7d7f7b930f20e508c632b2fb54cfbf783c8734fe5d1710c09cfb` |
| `$S/ci-diag/proposed-fix.diff` | `339e1f2257f78e10bae44ad9f93cddbcd769ecabdf1ff35c2c3a888d456e38fb` |
| `$S/rcf/BRIEF-COMMON.md` | read in full. Its binding rules 1–7 apply; the CIFIX brief overrides rule 5 for the register. |

---

## 0. Aegis skills read and applied (dogfood rule)

`docs/delivery-workflow.md:97` records that **no installed skill owns writing a
single change's plan**, so Stage A is enforced by procedure. I read and applied the
skills below to the parts of the plan they do own. MANUAL-ONLY skills were not used.
`systematic-debugger`, `flaky-test-detective` and `reviewable-diff-discipline` each
carry the `MANUAL-ONLY; never auto-invoke.` description prefix
(`grep -m1 '^description:'`).

| Skill | How applied | Result |
| --- | --- | --- |
| `change-classification-gate` (`.claude/skills/change-classification-gate/SKILL.md`) | Classified each deliverable from the files it will touch. Applied the class → floor matrix (`references/classification-matrix.md:22,24`), the highest-class rule and the scope lock. | §2. The `bug-fix` floor ("Reproduce the failure first; prove the fix flips it; regression test added") is why §4 adds one deterministic regression test. |
| `ci-failure-classifier` | Re-read the failing and passing logs on disk with the classifier's rules. Applied its "never mask a failure with a timeout or retry" rule and its "a skipped job is never counted as passed" rule. | Confirms TEST-BUG (§3.1). Sets the skipped-job wording in AC-F11 and in the Stage G notes. |
| `human-approval-boundary` | Matched each risky action against current instructions and the register's grants. | The fix PR's red `gate-guard` is covered only by the owner's 2026-10-08 one-time instruction, once it is recorded. AEGIS-APR-047 does not reach it (§6.1). |
| `scoped-approval-register` | Drafted the register entry. The owner's words are quoted verbatim, the one-time limit comes from the wording, no restriction is invented, and the consumption is a later appended event. | §6.4 draft entry. §6.6 consumption event. |
| `risk-tiered-validation-selector` | Applied its "never docs-only" list, which includes `scripts/`, and its max-tier aggregation. | Fix PR: **full** tier. Register PR: repository checks plus a link check of the register (§5, §7.2). |

`ai-task-decomposer` was considered and **not applied**. This item is one change plus
one dependent recording change, not a broad goal to split up.

---

## 1. What, why, blast radius, paths

**What.** `ProtectedFileGuardTests.run_guard` in `scripts/tests/test_offline_ci.py`
builds a throwaway Git repository. Right after its `git init`, two lines will turn off
that repository's Git auto-maintenance:
`git config maintenance.auto false` and `git config gc.auto 0`. One deterministic
regression test, in the same class and the same file, will prove that no
auto-maintenance process starts.

**Why.** Git 2.55 starts a **detached** `git maintenance run --auto` after every
`commit` and `fetch`. Under the geometric strategy, the default since Git 2.54, that
background process can start a `git repack`. The repack writes into `.git` while
`TemporaryDirectory` removes the tree, so cleanup intermittently fails with
`OSError: [Errno 39] Directory not empty`. This failed CI in runs 36695924676 and
37713171379. §3 verifies the cause independently.

**Blast radius.** The change touches one CI self-test file. The real `gate-guard`
script and the workflow are not changed. Production, skill and documentation content
are not changed. Behaviour changes only inside the throwaway fixture repositories:
they no longer start background maintenance. Every existing assertion stays as it is,
because no line is removed (AC-F1). Risk: low. The file is still a protected,
security-relevant surface, so `gate-guard` fails by construction and the merge needs
the recorded one-time owner exception (§6).

**Paths.**
- Fix PR (called **P-FIX** below): `scripts/tests/test_offline_ci.py` only.
- Register PR (**P-REG**): `docs/approvals/APPROVAL_REGISTER.md` only.
- Follow-up consumption PR (**P-CONS**, see Q3): `docs/approvals/APPROVAL_REGISTER.md` only.
- NOT touched, by any of them: `.github/` (including the workflow and `gate_pattern`),
  every other file under `scripts/`, `tools/`, `docs/delivery-workflow.md`,
  `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, the skills, and every reserved-scope
  item (evaluation package, VMs, Stage 4B, BER calibration, provider spend, the
  `[evaluation-source-pin]` source pin).

**Why two PRs and not one.** The owner's instruction (verbatim in §6.2) asks for "A
third PR touching only that test file" and an exception "for that exact commit,
recorded in the register". A commit cannot carry its own SHA. Adding the register entry
to P-FIX would add a second file and move the head the entry names. The register
precedent says the same thing: AEGIS-APR-106 states "The PR cannot create that entry
for itself." So the entry goes in a separate register-only PR. Q2 asks the coordinator
to confirm that reading.

---

## 2. Classification (`change-classification-gate`)

```
CHANGE CLASSIFICATION — P-FIX
Deliverables:    (1) disable auto-maintenance in run_guard's fixture repo; (2) one regression test
Classes:         (1) bug-fix (test bug); (2) qa-test-only
Governing class: bug-fix on a protected, security-relevant path (scripts/, gate_pattern match)
Approval path:   human-approval-boundary → the owner's one-time gate-guard exception (2026-10-08),
                 which must be recorded in the register before merge (§6); APR-047 does not reach it
Validation plan: bug-fix floor = reproduce before → prove the fix flips it → regression test added
                 (§5, AC-F4..F7); qa-test-only floor = run the suite and show the fixture change is
                 intended and masks nothing (AC-F1..F3, F8); risk-tiered tier = full (scripts/)
Scope contract:  scripts/tests/test_offline_ci.py only; additions only; no change to .github/ or guard

CHANGE CLASSIFICATION — P-REG
Deliverables:    one appended GRANT entry recording the owner's one-time exception for P-FIX's head
Classes:         docs-only by file type, but on a security-relevant governance surface
                 (CONTRIBUTING.md:246, "the owner approval register")
Governing class: governance record (treated above docs-only: verbatim-quote and immutability checks)
Approval path:   work authority = the owner's 2026-10-08 instruction ("recorded in the register");
                 merge mechanics = AEGIS-APR-100 / AEGIS-APR-048 once every check is green
                 (gate-guard is green here — the path is not protected, §6.3)
Validation plan: validator + validator self-tests + link check of the register; append-only proof
Scope contract:  docs/approvals/APPROVAL_REGISTER.md only; append-only
```

Two P-FIX criteria cannot be verified at the head before publication, and one is
probabilistic. All three are declared now, as `SD-A` requires:
- **AC-F11** (CI at the exact head) can be verified only after the push.
- **The race never recurs in CI** cannot be shown at any single head. The natural
  trigger is about 1 per 745 test-file runs (diagnosis census). A deterministic
  regression test (AC-F5) and a forced-trigger stress run (AC-F6) stand in for it.
- **Python 3.14** is UNRUN locally. Only 3.13.16 is installed (`python3 --version`,
  and `which python3.14` found nothing). The `validate-skills` job at the head
  covers 3.14.
- **`acceptance-core` (pwsh)** is UNRUN locally because `which pwsh` found nothing.
  The `validate-skills` job at the head covers it.

---

## 3. Independent verification of the root cause

### 3.1 CI evidence, re-read from the logs on disk

Attempt 1 log of run 37713171379,
`$S/ci-diag/logs/run37713171379-attempt1-validate-skills-113103554440.log`:
- line 60: `git version 2.55.0`
- line 949: `line 149, in run_guard`, called from line 947,
  `line 198, in test_each_enforcement_surface_requires_manual_merge`
- line 973: `OSError: [Errno 39] Directory not empty: '/home/runner/work/_temp/aegis-ci-guard-y58nb11f/repo'`
- lines 976–978: `Ran 38 tests in 3.520s` / `FAILED (errors=1, skipped=1)`

The log has 1049 lines (`wc -l`) and ends with `Cleaning up orphan processes`, so it is
not truncated. Run 36695924676, attempt 1
(`logs/older-failures/run36695924676-attempt1-109823746991.log:878`), shows
`OSError: [Errno 39] Directory not empty: '…/aegis-ci-guard-nljvb8hl/repo/.git/objects'`.
Classification: **TEST-BUG**, which agrees with the diagnosis.

There is also a relevant fact the diagnosis does not use. GitHub's own
`actions/checkout` runs the same mitigation on the CI checkout, at log line 87:
`[command]/usr/bin/git config --local gc.auto 0`. A gate-guard job log shows it too
(`logs/other-failures/run37159209057-111308911050.log:85`, Git 2.55.0). So the **real**
`gate-guard` job already runs with auto-maintenance off: under Git 2.55, `gc.auto 0`
disables it while `maintenance.auto` is unset (§3.2). The fixture is the one place
without that setting. The fix makes the fixture match the real job.

### 3.2 Git 2.55.0 source, from the scratch build `$S/git-build/src/git-2.55.0`

- `grep -rn 'run_auto_maintenance\|prepare_auto_maintenance' --include=*.c`. The only
  callers are `builtin/am.c:1942`, `builtin/receive-pack.c:2731`,
  `builtin/commit.c:1965`, `builtin/merge.c:509`, `builtin/fetch.c:2885` and
  `builtin/rebase.c:572`. The fixture and the guard run only `commit` and `fetch` from
  that list. `init`, `add`, `branch`, `remote`, `mv`, `hash-object`, `update-index`
  and `diff` never start maintenance.
- `run-command.c:1956-1967`, `prepare_auto_maintenance`: when `maintenance.auto` is
  set to false, the function returns 0 and no process starts. When `maintenance.auto`
  is unset, `gc.auto <= 0` disables it. Either setting alone is enough on 2.55.
  `gc.auto 0` also covers Git versions older than the `maintenance` command, which run
  `gc --auto` directly. That last point is not re-verified against old source here;
  it is labelled unverified.
- `run-command.c:1974-1976`: detaching defaults to true (`GIT_TEST_MAINT_AUTO_DETACH`,
  default true), unless `maintenance.autoDetach` or `gc.autoDetach` is set.
- `Documentation/config/maintenance.adoc` (`maintenance.auto`): "controls whether some
  commands run `git maintenance run --auto` after doing their normal work. Defaults to
  true."
- `builtin/fetch.c:2868` runs maintenance only if `enable_auto_gc`. That defaults to 1,
  and the `--no-auto-maintenance` flag (line 2580) clears it. The guard's
  `git fetch origin "$BASE_REF" --quiet` does not pass that flag.

### 3.3 Every temp-dir fixture and every git invocation in the file (read in full, 750 lines at `c060a7cb`)

| Fixture (line) | Git invocations, with cwd | Can it start a detached process inside the temp dir? |
| --- | --- | --- |
| `RecorderTests.setUp` `TemporaryDirectory("aegis-ci-recorder-")` (L47) | `git rev-parse HEAD` at L65 (cwd = REPO). The recorder `scripts/ci/record-check.py:63-64` runs `git rev-parse HEAD` and `git status --porcelain` with cwd = REPO. | No. These commands never start maintenance, and they run in the real checkout, which is never deleted. |
| `test_concurrent_local_runs…` `TemporaryDirectory("aegis-ci-fallback-")` (L90) | The same recorder git calls, cwd = REPO, with TMPDIR set to the temp dir | No, for the same reason. |
| **`ProtectedFileGuardTests.run_guard` `TemporaryDirectory("aegis-ci-guard-")` (L149)** | All with cwd = `repo`: `init` L157, `add` L165, **`commit` L166**, `branch` L167, `remote add origin <repo>` L168, `mv` L171 (rename case), `add` L177, `hash-object -w` L179 (symlink case; not through the helper), `update-index` L181, **`commit` L183**. The guard (L184, `bash -c self.guard`, cwd = repo) runs **`git fetch origin "$BASE_REF" --quiet`** and `git diff --no-renames --name-only -z …`. | **Yes. Three triggers per fixture: two commits and one fetch.** |
| `ImportPathIsolationTests.run_shadowed_validator` `TemporaryDirectory("aegis-ci-shadow-")` (L350) | `scripts/validate-skills.py:817,1084` runs `git ls-files` with cwd = the temp root, which is not a repository | No. `ls-files` never starts maintenance. |
| `test_root_executable_cannot_replace_git…` `TemporaryDirectory("aegis-ci-exe-")` (L631, Windows only) | `git --version` | No. |
| `GateJobIsolationTests`, `HashLockTests` | none | n/a |

### 3.4 Measured: auto-maintenance spawns per test-class run (trace2)

Script: `$S/cifix/scripts/trace_count.sh`, sha256 `56ebea49…`. It runs
`ProtectedFileGuardTests` once from an exported tree, with `GIT_TRACE2_EVENT` set to a
scratch directory, `GIT_CONFIG_GLOBAL=/dev/null`, a scratch `TMPDIR` and `python3 -B -P`.

| Tree | Git | Result line (verbatim) |
| --- | --- | --- |
| base (`git archive c060a7cb`) | 2.43.0 | `rc=0 OK Ran 10 tests … maintenance_child_start=264 gc_auto_child_start=0 maintenance_processes=264` |
| base | 2.55.0 | `rc=0 OK Ran 10 tests … maintenance_child_start=264 gc_auto_child_start=0 maintenance_processes=264` |
| base + `proposed-fix.diff` | 2.43.0 | `rc=0 OK Ran 10 tests … maintenance_child_start=0 gc_auto_child_start=0 maintenance_processes=0` |
| base + `proposed-fix.diff` | 2.55.0 | `rc=0 OK Ran 10 tests … maintenance_child_start=0 gc_auto_child_start=0 maintenance_processes=0` |

The base spawns break down by parent command as `{'fetch': 88, '-c': 176}`. Here `-c`
is the helper's `git -c user.name=…` commits, so the counts are 88 fixtures × (2
commits + 1 fetch). The example argv is
`['git', 'maintenance', 'run', '--auto', '--quiet', '--detach']`. The fixture count
comes from `$S/cifix/scripts/count_fixtures.py`:
`base: guard_tests=10 … run_guard_fixtures=88 test_methods_total=38`.

**Conclusion.** The proposed repository-local setting stops all three trigger paths.
That includes the guard's own `git fetch`, because the guard runs with cwd = repo and
reads `.git/config`. The guard script is not changed.

### 3.5 Measured: the race under a forced trigger, before and after

Script: `$S/cifix/scripts/ab_force.sh`, sha256 `149d3b3b…`. With force=1 it sets
`maintenance.geometric-repack.auto=-1` through `GIT_CONFIG_COUNT/KEY/VALUE`. That is
command-line-scope config, which the fixture's own config cannot override, so every
maintenance run repacks.

| Tree | Git | Result (verbatim) |
| --- | --- | --- |
| base | 2.55.0 | `base-force … force=1 runs=3 pass=0 fail=3 errno39_lines=82 leftover_tmp=82`. The runs report `FAILED (errors=24)`, `(errors=29)` and `(errors=29)`. The failing directories are `repo/.git/objects/pack` ×58, `repo/.git/objects` ×16, `repo/.git` ×7 and `repo/.git/info` ×1, all raised from `line 149, in run_guard`. |
| prototype (fix + regression test) | 2.55.0 | `full-force … force=1 runs=10 pass=10 fail=0 errno39_lines=0 leftover_tmp=0` |
| prototype | 2.55.0, natural | `full-natural … force=0 runs=10 pass=10 fail=0 errno39_lines=0 leftover_tmp=0` |

The local reproduction gives the same signature as CI: `OSError: [Errno 39]` at line
149, on the same directory family.

### 3.6 Is anything more robust needed? Decision: no. Use repository-local config only.

- **Environment `GIT_CONFIG_*` for the subprocesses** is rejected. It would have to be
  threaded into two separate environments: the helper's subprocess, which currently
  inherits `os.environ`, and the guard's `env=dict(os.environ, …)` at L185. It would
  also inject command-line-scope config into the guard under test, which the real CI
  job does not have. §3.4 shows the local setting already reaches 0 spawns on every
  path.
- **Both at once** is rejected as redundant, for the same evidence.
- **`--no-auto-maintenance` on the guard's fetch** is rejected. It would edit
  `.github/workflows/validate-skills.yml`, which is outside the owner's "only that
  test file".
- **`maintenance.autoDetach false`** is rejected. Maintenance would still run, now in
  the foreground: slower, and it still repacks.
- **`ignore_cleanup_errors=True`, retries, sleeps or a re-run policy** are rejected,
  as the classifier rule and the diagnosis also say. Each would hide the race and
  leave background repacks running.
- **Residual: command-line config.** A higher-precedence `git -c maintenance.auto=true`
  or `GIT_CONFIG_PARAMETERS` would override the repository-local setting. Neither
  exists in the test. The workflow's gate jobs are mechanically barred from
  `GIT_CONFIG*` environment variables by `test_current_workflow_has_no_gate_violations`
  (L557) and its mutation test (L585-599).
- **Residual: build options.** The runner's packaged Git 2.55 build options are
  unknown. They do not affect the cited code paths (unverified for that build). The
  diagnosis notes that the observed failure frequency is higher than its model
  predicts. The fix does not depend on which trigger fired, because it disables all
  auto-maintenance.

---

## 4. The change (P-FIX) — what Stage C writes

Stage C authors the commit. The reference prototype below is planning evidence, not
the implementation. Stage C may restyle it, provided every property P1–P7 holds and
every AC in §7.1 passes.

Reference prototype: `$S/cifix/prototype-reference.diff`, sha256
`a4ad6f9fdcd63446614b40216d82d94a473599e6344a837b0aa9f10e94c96a6f`. Measured against
`c060a7cb`: `git diff --numstat` gives `28	0	scripts/tests/test_offline_ci.py`, and
`git diff -U0 | grep -c '^-[^-]'` gives `0`.

**P1.** In `run_guard`, immediately after `git("init", "--quiet")` and before the first
`git("commit", …)`, add `git("config", "maintenance.auto", "false")` and
`git("config", "gc.auto", "0")`. Keep the explanatory comment. The diagnosis's
comment text in `proposed-fix.diff` is acceptable; it names runs 36695924676 and
37713171379.

**P2.** Add one test method to `ProtectedFileGuardTests`, so it inherits the
POSIX-only skip. It sets `GIT_TRACE2_EVENT` to a separate `TemporaryDirectory` (via
`unittest.mock.patch.dict(os.environ, …)`) around one `self.run_guard([...protected
path...])` call, and asserts three things:
- the guard result is 1 (protected path);
- the trace is live: some `child_start` argv contains `upload-pack`, the child the
  guard's fetch starts;
- no `child_start` argv contains the element `maintenance`, or both `gc` and `--auto`.

Prototype name: `test_fixture_repository_starts_no_auto_maintenance`.

**P3.** Add `from unittest import mock` beside `import unittest`, if P2 uses `mock`.

**P4.** Additions only. No existing line is modified or deleted.

**P5.** No `skip*`, `expectedFailure`, `ignore_cleanup_errors`, retry, `sleep` or
timeout change is added anywhere.

**P6.** One commit, signed off (`git commit -s`, required by DCO), on the new branch
`claude/sharp-lovelace-urgxpz-ci-fix`, created from the re-derived latest
`origin/main`. Stage exactly that one file (CONTRIBUTING rule 7) and run
`git branch --show-current` before commit and push.

**P7.** The commit message names the root cause and the two run IDs. It must not
contain the Codex trigger phrase (the word codex prefixed with the at sign).

The prototype regression test is deterministic. It was run 5 times per cell, with
`python3 -B -P scripts/tests/test_offline_ci.py ProtectedFileGuardTests.test_fixture_repository_starts_no_auto_maintenance`:

| Tree | Git 2.43.0 | Git 2.55.0 |
| --- | --- | --- |
| test added, **config lines absent** | `5 FAILED (failures=1)`; the assertion lists the 3 maintenance argvs | `5 FAILED (failures=1)` |
| test added, **config lines present** | `5 OK` | `5 OK` |

Full file at the prototype, in a scratch `git clone --shared` checked out at `c060a7cb`
with `GIT_CONFIG_GLOBAL=/dev/null`:

`git243 rc=0 Ran 39 tests in 5.255s OK (skipped=1) errno39=0`
`git255 rc=0 Ran 39 tests in 4.873s OK (skipped=1) errno39=0`

The prototype has `run_guard_fixtures=89` and `test_methods_total=39`
(`count_fixtures.py`).

---

## 5. How to prove it — the commands for Stages C, D and E

Everything runs from scratch. Exported trees go under `$S/cifix/`, with a scratch
`TMPDIR`, `PYTHONDONTWRITEBYTECODE=1`, `python3 -B` and `GIT_CONFIG_GLOBAL=/dev/null`.
The empty global config mirrors CI: the local global config enables
`commit.gpgsign` and CI does not. With the real global config the file still passes,
in 19.8 s against 5.4 s: `Ran 38 tests … OK (skipped=1)` either way
(`$S/cifix/verify/main-*.log`). Git 2.55.0 is
`$S/git-build/install/bin/git`, built from the kernel.org tarball; the diagnosis
verified its sha256. The system Git is 2.43.0.

1. **Before, reproduced** at the re-derived base. Export it with
   `git archive <base> | tar -x -C <dir>`. Run
   `trace_count.sh <base-tree> base-255 $S/git-build/install/bin`; expect
   `maintenance_child_start=264`. Run
   `ab_force.sh <base-tree> base-force 3 1 $S/git-build/install/bin`; expect `fail>=1`
   and `errno39_lines>0`.
2. **After, fixed**: the same scripts against the exported head tree; expectations in
   AC-F4 and AC-F6.
3. **Flip proof** for the regression test: copy the head tree, delete exactly the two
   `git("config", …)` lines, and run the single test 5×; expect FAILED. The unmodified
   head tree gives 5× OK, on both Git versions (AC-F5).
4. **Natural stress** at the head with Git 2.55: the whole test file 20× (AC-F7).
   This is a sanity check, not proof.
5. **The repository's own checks** at the head, from a scratch clone checked out at
   the head (AC-F8, AC-F9). The checks are the steps of the `validate-skills` job that
   can run locally: `test_offline_ci.py`, `test_validator.py`, `validate-skills.py`,
   `test_audit_skill_contracts.py`, `test_markdown_links.py`, and the BER self-check and
   suite, which is optional because the change cannot affect BER. Name pwsh acceptance
   and Python 3.14 as UNRUN, covered by the CI job at the head.

---

## 6. The one-time `gate-guard` exception: how and when it is recorded

### 6.1 Precedent read from the register (`grep -n '^###' docs/approvals/APPROVAL_REGISTER.md`)

- **The preamble, L8-13:** "Grant entries are immutable. Append later revocation,
  expiry, consumption or supersession events … An action is covered only by an
  effectively ACTIVE human grant whose scope includes it … Current direct user
  instructions are valid source evidence before transcription and do not need
  repeated consent." L64-66: "A gate-guard exception … usually one-time for one exact
  head, except the standing four-file exception in AEGIS-APR-047."
- **AEGIS-APR-047 (standing)** does **not** reach this file. Its Scope FORBIDDEN keeps
  "workflow/CI files, CODEOWNERS, the validator, Developer Certificate of Origin (DCO)
  check, guard scripts and tests, … for … separate one-time owner decisions"
  (`grep -n 'guard scripts and tests'` puts it at register line 1269).
- **One-time precedents.** There are 29 one-time `gate-guard` exception entries. The
  count comes from `grep -E '^### AEGIS-APR-[0-9]+: .*(guard exception|gate-guard exception|protected-path decision)' | grep -v -E 'Consumption|Standing' | wc -l`
  → `29`: APR-005, 010, 014, 016, 018, 020, 025, 029, 032, 034, 037, 041, 044, 055,
  061, 063, 071, 074, 077, 080, 082, 087, 089, 091, 093, 096, 103, 104 and 106. The
  register also has 44 "Consumption of …" or "… expired" headings. The three most
  recent precedents differ in timing:

  | Entries | PR | When recorded | Vehicle |
  | --- | --- | --- | --- |
  | **APR-103 / APR-104** | #648 / #649 | **after** the merge ("Recorded after the merge") | register-only PR #652 |
  | **APR-106** | #661 | **before** the merge | separate register-only PR **#663**, merged 2026-10-03T23:33:38Z |
  | APR-107 | #661 | consumption | PR #664, merged 23:46:03Z |

  PR #661 itself merged at 23:36:19Z (`git log --format='%h %ad %s' --date=iso-strict`
  and `gh api …/pulls/663`). `git merge-base --is-ancestor 5eb63bb8 cc8fd2cb` exits 0,
  so the register merge precedes the protected merge. #663's own body says it is a
  separate change because "The PR cannot create that entry for itself".
- **A moved head needs a new owner decision.** APR-032 was the original head. The head
  changed before merge, and APR-033 records it EXPIRED unused. APR-034 is a new GRANT
  for the replacement head, made on a fresh owner reply ("parooved").
- **CONTRIBUTING.md:45-49:** if `gate-guard` fails for the protected-path reason
  alone, "an independent review and an owner exception are required before an
  administrator merge". **MG4** (`docs/delivery-workflow.md:312-320`) has the merge
  agent confirm authority from "a register entry on the default branch that passes
  the preamble test below, or the owner's instruction quoted verbatim in its brief".
  The owner chose the register ("recorded in the register").

### 6.2 The owner's instruction (verbatim, from `$S/cifix/BRIEF.md`, joined to one line)

> A third PR touching only that test file, on a third branch, through all seven stages. It merges once gate-guard's red is covered by your one-time exception for that exact commit, recorded in the register, with every other check green. Admin merge allowed.

The label chosen was "Yes, one-time exception (Recommended)". The quote is 255
characters; the sha256 of the one-line text, first 16, is `95826ec00af9e24e`. The
coordinator recorded it at 2026-10-08T15:28:53Z, so the answer predates that time.

**Reading against precedent.** It matches APR-106 on four points: one-time, one exact
head, recorded **before** the merge ("It merges once … covered by … recorded in the
register"), and an administrator merge. It conflicts with no precedent. Four points
are flagged for the coordinator instead of being resolved here:
- Q1: "every other check green" against the three jobs the path filter skips.
- Q2: the separate register-only PR is a fourth PR the owner's text does not name.
- Q3: the consumption event.
- Q4: a head that moves after recording.

### 6.3 The vehicle and the timing

- **Vehicle: a separate register-only PR, P-REG.** It runs on a fourth branch, for
  example `claude/sharp-lovelace-urgxpz-ci-fix-register`; the coordinator chooses the
  name. It touches only `docs/approvals/APPROVAL_REGISTER.md` and appends one GRANT
  entry. The register path does **not** match `gate_pattern`: tested with bash
  `[[ =~ ]]` and `nocasematch` against the live pattern, it gives
  `docs/approvals/APPROVAL_REGISTER.md -> not gated`, while
  `scripts/tests/test_offline_ci.py -> GATE`. So `gate-guard` is green on P-REG, and
  P-REG merges on ordinary green checks.
- **This plan is the Stage A plan-of-record for P-REG as well** (§7.2). A Stage B
  ACCEPT on this captured revision covers both changes. P-REG still runs its own
  stages C to G, with distinct holders.
- **When:**
  1. P-REG's Stage C starts after P-FIX's head is fixed, at **SD-D ACCEPT**. That is
     the APR-106 / #663 timing.
  2. P-REG merges only **after P-FIX's SD-F ACCEPT at the same head the entry names**,
     and before P-FIX's Stage G.
  3. If P-FIX's head moves while P-REG is unmerged, P-REG's entry is rebuilt in place.
     That is permitted while the entry is unmerged; the #663 body and APR-105 Evidence
     both say "the append-only rule governs merged entries". P-REG's own verdicts are
     then void and re-taken.
  4. If P-FIX's head moves after P-REG merged, the entry is spendable on nothing, and
     Q4 applies.
- **Exact-head binding mechanism:**
  - (a) The entry names the PR number, the 40-character head, its tree
    (`git rev-parse <head>^{tree}`), its base, the single path with its `numstat`, and
    the `gate-guard` check-run and run IDs at that head. It also quotes the log's
    `Gate files touched:` line followed by the sole path.
  - (b) The merge is pinned to that head. With `gh pr merge --match-head-commit`, or
    over REST with `PUT /repos/ModernNomad-98/Project-Aegis/pulls/<n>/merge` and
    `"sha": "<head>"`, GitHub refuses the merge if the head moved. Note that
    `gh pr merge` may depend on GraphQL; `gh pr list` returned "HTTP 403: GitHub
    GraphQL is not available from Claude Code sessions" in this session, so Stage G
    should prefer REST.
  - (c) The merge is a squash, so the commit on `main` is a different object. The
    consumption record must say so (APR-107's lesson).
- **The ID.** On `main` there are 118 unique entries, max 118
  (`grep -o '^### AEGIS-APR-[0-9]*' … | sort -u | wc -l` → 118). PR #679's head adds
  119 (`git show <fetched refs/pull/679/head>:docs/approvals/APPROVAL_REGISTER.md | grep -o … | sort -n | tail -1` → 119). #680 adds none. **The next free ID
  at writing is `AEGIS-APR-120`.** P-REG's author re-derives it when writing, and the
  P-REG merge agent re-checks it at merge. #679 also appends at the end of the file
  (`@@ -5060,3 +5060,95 @@`), so whichever of #679 and P-REG merges second will have
  a textual conflict. Expect one rebase of the second one, which moves its head and
  voids its verdicts.

### 6.4 Draft register entry, to be written by P-REG's Stage C after P-FIX's SD-D ACCEPT

`<…>` marks a value Stage C fills in from live measurement. Each owner quotation stays
on one line, per `docs/delivery-workflow.md:813-825`, the line-wrap fragility rule.

```markdown
### AEGIS-APR-120: PR #<P-FIX> one-time gate-guard exception for the Errno 39 test fix

- **Event:** GRANT — one-time, bound to one exact head. Not a standing exception and
  not a policy decision.
- **Status at recording:** ACTIVE and **unspent** as recorded. It is consumed by the
  merge of PR #<P-FIX> at the exact head named below, and by nothing else. It cannot
  authorize the merge of the pull request that records it.
- **Date / Grantor:** 2026-10-08 / Peter Nguyen.
- **Reason:** [PR #<P-FIX>](https://github.com/ModernNomad-98/Project-Aegis/pull/<P-FIX>)
  stops the intermittent `OSError: [Errno 39] Directory not empty` raised by
  `ProtectedFileGuardTests.run_guard` (runs 36695924676 and 37713171379): a detached
  Git auto-maintenance repack wrote into the fixture repository while
  `TemporaryDirectory` removed it. The PR disables auto-maintenance in that fixture
  repository and adds a regression test. It changes only
  `scripts/tests/test_offline_ci.py`, which the protected-path pattern matches, so
  `gate-guard` fails by construction. AEGIS-APR-047 does not reach it: its Scope
  FORBIDDEN keeps "guard scripts and tests" for "separate one-time owner decisions".
- **Owner decision:** The owner selected, in the Project Aegis session on 2026-10-08,
  the option labelled "Yes, one-time exception (Recommended)". Its text, verbatim as
  relayed:

  > A third PR touching only that test file, on a third branch, through all seven stages. It merges once gate-guard's red is covered by your one-time exception for that exact commit, recorded in the register, with every other check green. Admin merge allowed.

  This is a transcription of a selection relayed through the coordinating agent, not
  the owner typing into this register. The preamble makes it valid source evidence —
  "Current direct user instructions are valid source evidence before transcription and
  do not need repeated consent" — and this entry does not claim a repository citation
  of the owner's own text.
- **Scope allowed:** One `gate-guard` exception and an administrator merge of
  PR #<P-FIX> at exact head `<40-hex head>` (tree `<40-hex tree>`, base
  `<40-hex base>`), and nothing else. The head changes one file,
  `scripts/tests/test_offline_ci.py`, `+<a>/−0`. At that head `gate-guard`
  (check run `<id>`, workflow run `<id>`) concluded FAILURE with `Gate files touched:`
  naming only `scripts/tests/test_offline_ci.py`; that failure is recorded here as
  **failed with an authorized disposition — not waived, and not a pass**. In the
  owner's words the merge also requires "every other check green" at that head and
  the PR to have gone "through all seven stages".
- **Scope FORBIDDEN:** No other pull request, head, path or failed check is covered
  ("only that test file", "for that exact commit", "every other check green"). It is
  one-time and is not a standing exception; it does not widen AEGIS-APR-047 and does
  not change `gate_pattern`, branch protection or any workflow. A moved head leaves it
  spendable on nothing.
- **Evidence:** The owner's selection, relayed through the coordinating agent and
  recorded by it at 2026-10-08T15:28:53Z (an upper bound); a session artifact, not a
  repository artifact. Repository artifacts that independently record the facts above:
  the Stage D audit <comment link>, the Stage F review <comment link>, and the
  `gate-guard` job log at the head. The head, tree, base, path and `+<a>/−0` were
  re-measured from `git` against `origin/main` for this entry, not taken from a brief.
- **Expiry / use limit:** One use: one merge of PR #<P-FIX> at the named head,
  consumed by that merge. No calendar expiry stated.
```

`scoped-approval-register` checks on this draft:
- The scope is the owner's verbatim wording.
- Every FORBIDDEN clause is derived from that wording ("only that test file", "that
  exact commit", "every other check green") or states a fact (no setting is changed).
  No restriction the owner did not state is invented.
- The one-time limit comes from "one-time exception for that exact commit".
- Consumption is a later appended event (§6.6).
- The entry contains no secret.

### 6.5 Authority for P-REG itself

- **Work:** the owner's instruction "recorded in the register" (§6.2), the recording
  step the owner prescribes.
- **Merge mechanics:** AEGIS-APR-100 ("all commits, push, and merges are pre-approved
  as long as they passed local tests and green on github actions") and AEGIS-APR-048
  (administrator merge once green), with AEGIS-APR-050 (wait for the automated
  review) and the seven stages.

BRIEF-COMMON rule 5's default ("do not edit … the approval register … unless the plan
explicitly justifies it AND the audit accepts it") is overridden here by the CIFIX
brief's explicit requirement and by §1's justification. Stage B must accept this
explicitly. Q2 asks the coordinator to confirm.

### 6.6 The consumption event (P-CONS), recommended, see Q3

After P-FIX merges, append `AEGIS-APR-<next>` (expected 121) as **Event: CONSUMED;
target grant AEGIS-APR-120**. Record:
- the effective time, which is P-FIX's merge time;
- the merged squash commit, with the statement that the bound head is not that commit
  (`git merge-base --is-ancestor <head> <merge>` exits non-zero);
- "New authority: None".

APR-107 is the template. The preamble (L33-35) allows a one-use grant to be "used up
even before a later event records that". So P-CONS does not gate P-FIX's merge. It
can run right after, or be batched into the next register PR (the coordinator
decides).

---

## 7. Acceptance criteria

Notation: `B` is the base P-FIX is against. `H` is P-FIX's 40-character head. `T(H)`
is `git archive H` exported to `$S/cifix/verify/head`. `G55` is
`$S/git-build/install/bin`. All local runs use a scratch `TMPDIR`,
`GIT_CONFIG_GLOBAL=/dev/null`, `PYTHONDONTWRITEBYTECODE=1` and `python3 -B`.

### 7.1 P-FIX

| # | Criterion | Command | Expected |
| --- | --- | --- | --- |
| AC-F1 | Exactly one file changes, additions only | `git diff --numstat B...H` ; `git diff -U0 B...H \| grep -c '^-[^-]'` | one line, `<a>	0	scripts/tests/test_offline_ci.py`, with `a` ≤ 40 (the prototype has 28) ; `0` |
| AC-F2 | No test weakened, skipped or retried | `git diff B...H \| grep -nE '^\+.*(skip\|expectedFailure\|ignore_cleanup_errors\|retry\|sleep\|timeout)'` | no output (exit 1) |
| AC-F3 | The method set is the base set plus exactly the one regression test; the fixture count goes up by exactly 1 | `python3 -I -B $S/cifix/scripts/count_fixtures.py <T(B)>` and `… <T(H)>`; compare the `test_` names with an `ast` listing of both files | B: `run_guard_fixtures=88 test_methods_total=38` (measured at `c060a7cb`; re-derive if B moved). H: `89` / `39`. The names differ by one, the P2 test. |
| AC-F4 | No auto-maintenance process starts from any fixture path | `trace_count.sh <T(H)> head-243` ; `trace_count.sh <T(H)> head-255 G55` | both: `OK Ran 11 tests` and `maintenance_child_start=0 gc_auto_child_start=0 maintenance_processes=0` (base: 264, AC-F4 before) |
| AC-F5 | The regression test flips deterministically | Copy `T(H)`, delete exactly the two `git("config", …)` lines, run `…ProtectedFileGuardTests.test_fixture_repository_starts_no_auto_maintenance` 5×, then 5× on `T(H)` unmodified, for both Git versions | without the lines: 5× `FAILED (failures=1)`; at H: 5× `OK`; both Git versions |
| AC-F6 | No race under a forced trigger; reproduced before | `ab_force.sh <T(B)> base-force 3 1 G55` ; `ab_force.sh <T(H)> head-force 10 1 G55` | B: `fail>=1 errno39_lines>0`; H: `pass=10 fail=0 errno39_lines=0 leftover_tmp=0` |
| AC-F7 | Natural stress at H with Git 2.55 | 20× `python3 -B -P scripts/tests/test_offline_ci.py` in a scratch clone at H with `PATH=G55:$PATH` | 20× `OK (skipped=1)`, 0 lines with `Errno 39` |
| AC-F8 | The full file passes at H, system Git and Git 2.55 | `python3 -B -P scripts/tests/test_offline_ci.py` in a scratch `git clone --shared` checked out at H | exit 0; `Ran 39 tests`; `OK (skipped=1)` |
| AC-F9 | Repository checks unchanged at H | `python3 -B -P scripts/validate-skills.py` ; `python3 -B -P scripts/tests/test_validator.py` ; `python3 -B -P scripts/tests/test_audit_skill_contracts.py` ; `python3 -B -P scripts/tests/test_markdown_links.py` | each exit 0, with the same summary line as at B. At `c060a7cb`: `OK: 195 skill(s) valid, 0 warning(s)` and `OK: 181 gate self-test assertion(s) passed.` Re-derive at B if B moved. |
| AC-F10 | The guard and the workflow are untouched; the commit is signed off | `git diff --quiet B...H -- .github/ ; echo $?` ; `git log --format=%B B..H \| grep -c '^Signed-off-by:'` ; `git rev-list --count B..H` | `0` ; equal to the commit count, expected `1` ; `1` |
| AC-F11 | CI at the exact head H. **Not verifiable before publication**, declared under SD-A. | `gh api repos/ModernNomad-98/Project-Aegis/commits/H/check-runs --jq '.check_runs[]\|"\(.name) \(.status) \(.conclusion)"'`, plus the job logs | `changes completed success`; `validate-skills completed success`, whose log has `Ran 39 tests` and `OK (skipped=1)` for ci-tests and `OK (skipped=5)` for BER. Those are the same skip counts as comparison run 37709031628, log lines 958 and 4538, and run 37713171379 attempt 2, lines 946 and 4526 (`grep -n 'OK (skipped='`); **`gate-guard completed failure`**, whose log has `Gate files touched:`, then exactly one path, `scripts/tests/test_offline_ci.py`, then `requires manual review and merge`; and **`windows-offline-checks`, `tools-tests-linux`, `tools-tests-windows`: `completed skipped`**, by the path filter (`changes` outputs `tools=false`, `offline=false`). Skipped is recorded as skipped, never as passed (see Q1). |
| AC-F12 | Hygiene | `git status --porcelain` in the real checkout after all local runs; `ls -A <TMPDIR>` after the H runs | empty; no leftover `aegis-ci-guard-*` |

### 7.2 P-REG

| # | Criterion | Command | Expected |
| --- | --- | --- | --- |
| AC-R1 | Exactly one file, append-only | `git diff --numstat Bʳ...Hʳ` ; `git diff -U0 Bʳ...Hʳ \| grep -c '^-[^-]'` | one line, `<n>	0	docs/approvals/APPROVAL_REGISTER.md` ; `0` |
| AC-R2 | The new ID is the next free one and unique | `git show Hʳ:docs/approvals/APPROVAL_REGISTER.md \| grep -o '^### AEGIS-APR-[0-9]*' \| sort \| uniq -d` ; the max ID on `origin/main` and on every open PR at writing | no duplicates; the ID is max+1 over main and open PRs (120 at planning) |
| AC-R3 | The owner quote is byte-exact and on one line | `grep -cF "<the 255-char quote of §6.2>" <file at Hʳ>` | `1` |
| AC-R4 | The entry names P-FIX's exact head, tree, base, path and numstat, and they match live git | `grep -c '<H>'` within the new entry; then recompute `git rev-parse H^{tree}`, the merge-base and the `numstat` | each value is present and equal to live git |
| AC-R5 | Repository checks | `validate-skills.py` ; `test_validator.py` ; `python3 -B -P scripts/ci/check-markdown-links.py docs/approvals/APPROVAL_REGISTER.md` | exit 0 each |
| AC-R6 | CI at Hʳ all green, including `gate-guard` | the check-runs command at Hʳ | `changes`, `validate-skills` and `gate-guard` succeed; the three path-scoped jobs are skipped |

### 7.3 P-CONS, if run (Q3)

Its AC-R1, AC-R2 and AC-R5 apply the same way. In addition, the entry names target
APR-120, the merge time, and the squash commit with its non-ancestry statement
(`git merge-base --is-ancestor H <merge>` exits 1).

---

## 8. PR body outlines

### 8.1 P-FIX body

The body follows `.github/pull_request_template.md` **as it is on `main` when the PR
is opened**. PR #680 adds sentinels to the template. If #680 has not merged, the body
must carry the sentinels anyway: `docs/delivery-workflow.md:643-671` defines the bound
fields by their sentinels, and a missing sentinel makes the hash undefined. Never
write the Codex trigger phrase.

1. **`## What & why`.** The plan in a few sentences: what, why, the blast radius, the
   path, and the AC list, either AC-F1..F12 or a link to this plan's captured revision.
   - **Audited plan revision:** the sha256 of the Stage B-accepted plan file.
   - Root cause, with the two run IDs and the Git 2.55 mechanism.
   - "Gate-guard will be red by design. It is covered only by the one-time owner
     exception AEGIS-APR-120 (recorded in a separate register PR, #<P-REG>), which
     names this exact head."
2. **`## Checklist`.** Tick the items that apply. Write the Windows jobs as "skipped by
   path scope", not as passed.
3. **`## Aegis skills used (required)`**, between the lines
   `<!-- bound-field: skills -->` and `<!-- bound-field: end -->`. The table has the
   four required columns, and each stage agent writes its own row.
4. **`## Security-relevant surface? (required)`**, between
   `<!-- bound-field: security -->` and `<!-- bound-field: end -->`. Text:
   `- [x] Yes — surface(s) touched: scripts/ (scripts/tests/test_offline_ci.py, a path the protected-file guard matches)`
   and `- [ ] No`. MG5 does not apply under its scope clause, because this is not an
   outside contribution (`docs/delivery-workflow.md:322-332`).
5. **`## Reconciliation witness (required)`**, between
   `<!-- bound-field: witness -->` and `<!-- bound-field: end -->`. Eight rows:
   - Sites 1–5 and 8: `unchanged-and-verified`, with
     `git diff --quiet B...H -- docs/delivery-workflow.md; echo $?` → `0`.
   - Site 6: `unchanged-and-verified`, with `git diff --quiet B...H -- AGENTS.md` → `0`.
   - Site 7: `unchanged-and-verified`. The body's only rule-bearing content is the
     witness, the skills table and the divergence table.
6. **`## Divergence table`.** "Not applicable: `AGENTS.md` and no `MG`/`SD` condition
   changed."
7. **Evidence section.** The before and after results for AC-F4..F7, with commands; the
   UNRUN list (pwsh acceptance, Python 3.14, both covered by `validate-skills` at H);
   the handoff block.
8. The closing attribution lines the session's commit and PR attribution reminder
   specifies.

### 8.2 P-REG body

The same template sections, with these differences:
- **What & why** says the PR records the owner's one-time exception for PR #<P-FIX> at
  `<H>`, and why it is a separate PR (§1).
- **Security answer:** `Yes — the owner approval register (docs/approvals/APPROVAL_REGISTER.md)`.
- The witness rows are the same as P-FIX's.
- The entry text is quoted in full in the body.
- An append-only proof (AC-R1).

---

## 9. Stage-specific notes

**All stages.**
- Re-derive every head, base, check result and register fact in the same turn.
- A moved head voids head-bound verdicts.
- `gate-guard` red on P-FIX is expected. It must be the **only non-success, non-skipped
  conclusion**, and it must be red **solely** for the protected-path match, with
  exactly the one path.
- Never write the Codex trigger phrase. Do not touch reserved scope.
- Separation: no agent holds two stages of the same change. In addition, the agent that
  authors P-REG's entry must be neither P-FIX's Stage C author nor P-FIX's merge agent,
  so that no agent records its own authority.

**Stage C (P-FIX).**
- Create `claude/sharp-lovelace-urgxpz-ci-fix` from the re-derived `origin/main`.
- Implement P1–P7. Run AC-F1..F10 and F12 locally before pushing.
- Record `H`, `git rev-parse H^{tree}` and `B` (SD-C).
- Open the PR with the §8.1 body. The B-accepted plan hash goes in "Audited plan
  revision". C does not write other stages' skills rows.

**Stage D (P-FIX).** `code-reviewer` fits, a CI test-code diff and not a skill-library
PR; verify its scope first.
- Check AC-F1..F10 and F12 one by one at `H`, each MET, NOT MET or UNRUN. AC-F11 is
  UNRUN until CI completes; that is declared in §2.
- Confirm P4/P5: no weakened assertion, no skip, no cleanup-error suppression.
- Confirm the regression test cannot pass vacuously, by the upload-pack liveness
  assertion and AC-F5.
- Confirm the config lines run before the first commit.
- Post the verdict naming `H`.
- An ACCEPT here is the trigger for P-REG's Stage C (§6.3).

**Stage E (P-FIX).**
- Run the §5 commands and the local `validate-skills` job steps at `H`.
- List pwsh `acceptance-core` and Python 3.14 as UNRUN, covered by the
  `validate-skills` job at `H`, with evidence.
- Collect AC-F11 from the live check-runs and logs. Read run-level state, not job
  `status` alone (AGENTS.md, run 37156376468).
- Confirm the three skips come from the path filter (`changes` outputs), not from a
  failure.
- Disposition: `SD-E: PASS` or `SD-E: INCOMPLETE — UNRUN LISTED`.

**Stage F (P-FIX).** `code-reviewer`.
- Give an independent verdict naming `H`.
- Check the "Aegis skills used" table against the work.
- Check that the security answer is "Yes: scripts/".
- Check that the witness has 8 rows.
- Compute the bound-field hash (sha256, first 16, by the whole-line sentinel method)
  and name it in the verdict.
- Accept the Stage E unrun list if E was INCOMPLETE.
- Note that P-REG must not merge until this ACCEPT exists for the head the entry names.

**P-REG stages C–G.**
- **C:** write the §6.4 entry with live values only. Run AC-R1..R5. Open the PR.
- **D and F:** `code-reviewer`, plus the `scoped-approval-register` validation
  checklist for the entry; verify each skill's scope. Check verbatim equality of the
  quote and the head values against live git, and that no prior entry changed.
- **E:** the checks plus CI.
- **G:**
  - Confirm authority: the owner instruction, plus AEGIS-APR-100/048/050. Every check
    is green, including `gate-guard`. The automated review has posted at `Hʳ`, or is
    confirmed unavailable, with P2+ findings triaged.
  - Confirm P-FIX's SD-F ACCEPT is posted for the head the entry names.
  - Merge pinned to `Hʳ`. Re-derive the ID against `main` and the open PRs first. If
    #679 merged in between, P-REG needs a rebase, a new `Hʳ`, and new D/E/F verdicts.

**Stage G (P-FIX), in the same turn, before merging.**
1. Read the PR head over the API: `gh api …/pulls/<P-FIX> --jq .head.sha`. It must
   equal the `H` the entry names.
2. Run `git fetch origin main`. The `AEGIS-APR-120` entry must be on
   `origin/main`:
   `git show origin/main:docs/approvals/APPROVAL_REGISTER.md | grep -n '<H>'` must
   find it inside that entry. Check the entry passes the preamble test: no later
   lifecycle event for it, and the scope covers this exact head and path.
3. MG1:
   - List the check-runs at `H`. `gate-guard` = failure, and its log shows only
     `scripts/tests/test_offline_ci.py` under `Gate files touched:`.
   - Every other run check = success: `changes` and `validate-skills`.
   - The three path-scoped jobs = skipped, recorded as skipped, not green (Q1).
   - Record `gate-guard` as "failed with an authorized disposition (AEGIS-APR-120)".
4. MG2: the SD-F ACCEPT names `H`. Recompute the bound-field hash from the live body;
   it must equal the verdict's hash.
5. MG3 / AEGIS-APR-050: the automated review has posted a result for `H` or is
   confirmed unavailable for `H`. Triage every P0–P2 finding. Use
   `original_commit_id`, not `commit_id`, to bind findings to heads (AGENTS.md,
   PR #657).
6. MG4: the register entry, plus the owner text quoted verbatim in the brief with its
   source. MG5: not applicable, by its scope clause.
7. Merge as an administrator ("Admin merge allowed"), squash, **pinned to `H`** (§6.3 b).
8. Post the receipt keyed by MG ID.
9. After the merge, observe the push-to-`main` run at the merge commit. A push runs
   every job with `tools=true, offline=true`, which gives Windows coverage of the
   merged file; `gate-guard` is skipped on a push. Record the result in the receipt.
   If it is red, the owner's failure-handling instruction applies (diagnose and fix;
   never re-run to green without a diagnosis).
10. Hand off to P-CONS (Q3).

---

## 10. Sequence and ETA

The ETAs are **estimates** of active work by this planner. They are not measurements;
the coordinator owns the official name/ETA announcement for each item.

| Step | Holder | ETA (estimate) |
| --- | --- | --- |
| B: audit this plan | auditor ≠ planner | 15–25 min |
| C: P-FIX implement + local AC + push + PR | implementer | 20–35 min |
| CI on H | GitHub | a few minutes. The diagnosis records validate-skills attempt 2 of run 37713171379 running 15:13:17–15:15:00Z. Unverified for H. |
| D: P-FIX audit | ≠ C | 20–30 min |
| E: P-FIX validate | ≠ C, D | 20–30 min |
| F: P-FIX final review | ≠ C, D, E, G | 20–30 min |
| P-REG C → G, starting at P-FIX SD-D and merging after P-FIX SD-F | distinct holders | 60–90 min, overlapping P-FIX's E and F |
| G: P-FIX merge + receipt + post-merge run | merge agent | 15–25 min |
| P-CONS (optional now) | distinct holders | 40–60 min |

---

## 11. Open questions for the coordinator

None of these is resolved by this plan.

- **Q1 — "every other check green" against path-scoped skips.** A PR that touches only
  `scripts/tests/test_offline_ci.py` will show `windows-offline-checks`,
  `tools-tests-linux` and `tools-tests-windows` as **skipped**. Their `if:` conditions
  need `tools/` or `requirements-ci.*` changes (`.github/workflows/validate-skills.yml`,
  `changes` job, PR #676). Precedent: PRs #677 and #678 merged with exactly those
  three skipped, under the owner's "merge once all checks are green" instruction
  (`gh api …/commits/<head>/check-runs`). The plan reads "every other check green" as
  every other check **that ran** concluding success, with the skips recorded as
  skipped and never as passed. The brief's phrase "gate-guard is the ONLY non-green
  check" also needs that reading. Please confirm it, or tell us to obtain the owner's
  view.
- **Q2 — the fourth PR.** The owner's text names "A third PR", and recording the
  exception "in the register" needs a separate register-only PR (§1, §6.3), as in the
  APR-106 / #663 precedent. The plan treats that recording PR as authorized by the
  owner's "recorded in the register", under AEGIS-APR-100/048 merge mechanics and its
  own seven stages. Please confirm that reading, which also lifts BRIEF-COMMON
  rule 5's register default.
- **Q3 — the consumption event (P-CONS).** Precedent APR-107 recorded consumption in
  its own register PR. The preamble does not require one before the grant is spent.
  Should P-CONS run right after the merge as part of CIFIX-1, or be batched into a
  later register PR?
- **Q4 — a head that moves after P-REG merged.** Precedent APR-032 → 033 → 034 took a
  **fresh owner reply** for a replacement head. The plan avoids this by merging P-REG
  only after P-FIX's SD-F ACCEPT. If it still happens, should the team ask the owner
  again, as the precedent did, or treat the owner's "for that exact commit" as
  re-bindable to the final head (an EXPIRED append and a new GRANT)? The planner's
  recommendation is to ask the owner, following the precedent.
- **Q5 — the regression test (scope).** The plan adds one deterministic regression
  test (P2) in the same file, to meet `change-classification-gate`'s bug-fix floor.
  The test adds about 18 lines to the 10-line fix. If the coordinator or Stage B
  prefers the config-only fix, drop P2/P3. AC-F3 then expects 88/38. Drop AC-F5, and
  AC-F4/F6/F7 remain the proof. The plan would then record a "regression test not
  added" shortfall against the floor.
- **Q6 — ID collision with #679.** P-REG takes `AEGIS-APR-120`. #679 holds 119 and also
  appends at the end of the register, so whichever merges second needs a rebase. Is
  there a preferred merge order? Merging #679 first avoids rebasing P-REG after its
  reviews.

---

## 12. Handoff block

1. **Decision IDs.**
   - Bound by: `SD-A`–`SD-G` and `MG1`–`MG5`, unchanged.
   - Relies on: AEGIS-APR-047, which does not cover this PR; AEGIS-APR-048, 050 and
     100; AEGIS-APR-106/107 as the precedent.
   - Changes no decision. The new entry AEGIS-APR-120 is proposed, not written.
2. **Changed files: none** (Stage A). Repository files written: none.
   `git status --porcelain | wc -l` returned `0` in the real checkout after all local
   runs, and it is re-read before handoff. Two local refs, `refs/remotes/pr/679` and
   `refs/remotes/pr/680`, came from a `git fetch` of the open PR heads, used for
   reading. Both were deleted afterwards with `git update-ref -d`, and
   `git for-each-ref refs/remotes/pr | wc -l` now returns `0`. The `git fetch origin main`
   also refreshed `origin/main`, which still equals `c060a7cb`. Scratch files written:
   this plan;
   `$S/cifix/scripts/{trace_count.sh,ab_force.sh,add_regtest.py,count_fixtures.py}`;
   `$S/cifix/prototype-reference.diff`; `$S/cifix/verify/**`.
   **NOT touched:** every repository path.
3. **Proven invocation:** every figure above carries its command and output.
   Unverified items are labelled: the branch-protection `strict` setting returned
   "403 Resource not accessible by integration"; the runner's Git build options; the
   CI duration for H; old-Git `gc --auto` coverage.
4. **Deviation flags.** One: the plan adds a regression test beyond the diagnosis's
   proposed diff (Q5). The diagnosis's mechanism and fix lines are adopted unchanged.
5. **Continuation line.** Stage B audits this file at its sha256 and returns ACCEPT or
   REVISE. On ACCEPT, Stage C implements §4 on `claude/sharp-lovelace-urgxpz-ci-fix`
   from the re-derived `origin/main`, runs §7.1 locally, records H/tree/base, and
   opens P-FIX with the §8.1 body. P-REG starts at P-FIX's SD-D ACCEPT (§6.3).

## 13. Evidence index (scratch)

| File | sha256 (first 16) |
| --- | --- |
| `$S/cifix/scripts/trace_count.sh` | `56ebea49c320effe` |
| `$S/cifix/scripts/ab_force.sh` | `149d3b3bff39a56b` |
| `$S/cifix/scripts/add_regtest.py` | `cceda7bf8c14dd99` |
| `$S/cifix/scripts/count_fixtures.py` | `e07d5bcf8e05c9a0` |
| `$S/cifix/prototype-reference.diff` | `a4ad6f9fdcd63446` |
| Run outputs | `$S/cifix/verify/{trace-*,ab-*,reg-*,fullfile-*,probe-*}/` |

**Finished:** see the coordinator handoff report. The finish timestamp is taken after
this file's hash, so that adding it does not change the hash.
