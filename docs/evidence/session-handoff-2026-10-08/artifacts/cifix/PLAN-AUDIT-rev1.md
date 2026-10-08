# CIFIX-1 — Stage B INDEPENDENT PLAN AUDIT of PLAN-rev1

**Disposition: `SD-B: REVISE`** on the captured revision below. The required changes are numbered in §3.

- **Audited revision:** `$S/cifix/PLAN-rev1.md`, sha256
  `634f3f0fbcc48592f8e8d4abfdaf4b42f16130f4eaa52128f125f018195110c8`. Checked with `sha256sum` at the start
  (2026-10-08T15:52:33Z) and again after the coordinator's mid-audit update; the value was the same both times.
- **Stage held:** B only. I did not write the plan. I will not implement, audit the implementation, validate,
  review or merge either change. Repository files written: none. GitHub writes: none.
- **Role:** A. The four landmarks are present: `head -3 README.md` shows `# Project Aegis`, and `ls` found
  `docs/skills-catalog.md`, `scripts/validate-skills.py` and `artifacts/audits/skill-contract-audit-baseline.json`.
- **Scratch root:** `S=/tmp/claude-0/-home-user-Project-Aegis/0168d1d5-9af4-5a74-a8dd-9a35339e53ab/scratchpad`.
  My own evidence is under `$S/cifix/b-audit/`.
- **Inputs read in full:** `AGENTS.md`, `CLAUDE.md`, `docs/delivery-workflow.md` (all 894 lines: Stage B, SD-B,
  MG1–MG5, proportionality, bound fields), `CONTRIBUTING.md` (all 276 lines), and the register: the preamble
  L1-80, AEGIS-APR-032/033/034, 047, 048, 049, 050, 100, 103, 104, 105, 106 and 107. I also read
  `$S/rcf/BRIEF-COMMON.md`, `$S/cifix/BRIEF.md` (both versions; see below), `$S/ci-diag/DIAGNOSIS.md`, the plan,
  `$S/cifix/prototype-reference.diff` and the planner's four scripts. `scripts/tests/test_offline_ci.py` was read
  in full: 750 lines at `c060a7cb` (`wc -l`).
- **The brief changed during the audit.** The coordinator appended the owner's answers to Q2, Q3 and Q4,
  recorded at 2026-10-08T16:01:16Z. `sha256sum $S/cifix/BRIEF.md` now gives `5419a0dacaf8e092…`. The plan's
  input table names `041d76ab0ebfefb3…`, the earlier version. This audit applies the owner's answers. RC1–RC3
  cite them.

## 0. Aegis skills used (dogfood rule)

`docs/delivery-workflow.md:98` records that **no installed skill owns a plan-level ACCEPT/REVISE audit**, so the
verdict and the revision binding are procedural. I applied the skills below to the parts they do own. Each one's
frontmatter was checked, and none is MANUAL-ONLY (`grep -m1 '^description:'`). The MANUAL-ONLY skills
`systematic-debugger`, `flaky-test-detective` and `reviewable-diff-discipline` were not used.

| Skill | How applied | Result |
| --- | --- | --- |
| `acceptance-criteria-reviewer` (partial fit, per delivery-workflow:98) | Gave each of AC-F1..F12 and AC-R1..R6 a TESTABLE, NEEDS-REWRITE or UNTESTABLE verdict, checking that each has an observable outcome, a threshold and evidence. Listed the gaps. Wrote nothing into the plan. | §5. 13 TESTABLE, 5 NEEDS-REWRITE, 0 UNTESTABLE, 3 gaps. This skill "never decides whether work is done". The plan-level verdict is mine and is procedural. |
| `scoped-approval-register` | Ran its validation checklist against the §6.4 draft entry. Checked the verbatim quote, FORBIDDEN clauses derived from the wording, one-use limit from the wording, proposal context, lifecycle by appended events, and no secrets. | The quote is byte-exact (§2.4). Nothing is invented. The proposal context is missing and the owner's Q2/Q4 answers are absent (RC6). |
| `human-approval-boundary` | Matched each risky action against the current owner instructions (BRIEF.md, both parts) and the register's grants. The actions were: P-FIX's admin merge past a red `gate-guard`, P-REG's register edit and merge, and the response to a moved head. | P-FIX is covered only by the owner's one-time grant once it is recorded. AEGIS-APR-047 does not reach it (register L1269-1271). P-REG is covered by the owner's Q2 answer. A head moved after recording needs a fresh owner decision (Q4). |
| `change-classification-gate` | Re-checked the plan's §2 classification and floors against `references/classification-matrix.md` L24 (bug-fix) and L22 (qa-test-only). | Agrees: bug-fix plus qa-test-only, on a protected path. The bug-fix floor "reproduce → flip → regression test" is met by the prototype, which I reproduced (§2.1–2.2). |

## 1. Summary

The technical core is sound, and I re-verified it independently.
- **Root cause.** A detached Git auto-maintenance `git repack` races the `TemporaryDirectory` cleanup.
- **Fix.** Repository-local `maintenance.auto false` and `gc.auto 0`, set after `git init`. It reaches every
  trigger path: two commits and the guard's fetch per fixture.
- **Regression test.** The trace2 test is deterministic, flips cleanly and is POSIX-only by inheritance. It is
  portable because the class skips on Windows.
- **Scope.** P-FIX stays one file, additions only.

The revision is needed for four reasons:
- the owner's Q2/Q3/Q4 answers must replace three open questions and the parts of the plan that depend on them;
- the P-REG schedule contradicts its own draft entry (Stage F evidence is cited before Stage F can exist);
- the P-REG append-only criterion does not prove that prior entries are unchanged;
- several facts have gone stale since the plan was written (#679 merged, and the base moved).

## 2. Findings by audit area

### 2.1 Root cause and fix — re-verified independently

All runs used my own harnesses, not the planner's: `$S/cifix/b-audit/scripts/force_run.sh` (sha256 first 16:
`fd7cca218a151144`) and `trace_spawns.sh` (`649791b52878900d`). Each ran under a scratch `TMPDIR`,
`GIT_CONFIG_GLOBAL=/dev/null`, `PYTHONDONTWRITEBYTECODE=1` and `python3 -B -P`. The trees are
`git archive c060a7cb… | tar -x` (base), base plus `git apply prototype-reference.diff` (proto, which applied
cleanly), and proto with the two `git("config", …)` lines removed by `sed` (reverted). Git 2.55.0 is
`$S/git-build/install/bin` (`git --version` → `git version 2.55.0`). System Git is 2.43.0.

**Git source (2.55.0, `$S/git-build/src/git-2.55.0`):**
- `run-command.c:1956` `prepare_auto_maintenance`. At L1961, `repo_config_get_bool(r, "maintenance.auto", …)`
  returns non-zero only when the key is **absent**. In that case `gc.auto` decides, with `enabled = gc_threshold > 0`.
  When `!enabled`, the function returns 0 and no process starts.
- L1976 sets detach to default true (`GIT_TEST_MAINT_AUTO_DETACH`). L1980 builds the argv
  `"maintenance", "run", "--auto"`.
- The plan says either setting alone suffices on 2.55. **Confirmed.**
- Callers, from `grep -rn 'run_auto_maintenance\|prepare_auto_maintenance' --include=*.c`: am.c:1942,
  receive-pack.c:2731, commit.c:1965, merge.c:509, fetch.c:2885 and rebase.c:572. **This matches the plan exactly.**
  The fixture and the guard reach only `commit` and `fetch`.
- `builtin/gc.c:1632-1637`: `maintenance.geometric-repack.auto` `< 0` → `return 1`. `maintenance.adoc` says "A
  negative value will force the task to run every time". So the planner's forced trigger is a valid forcing method.

**Spawn census (trace2, `trace_spawns.sh`):**

```
base-255  git=2.55.0 rc=0 Ran 10 tests OK auto_maint_spawns=264 by_parent={'commit': 176, 'fetch': 88} upload_pack_children=88
base-243  git=2.43.0 rc=0 Ran 10 tests OK auto_maint_spawns=264 by_parent={'fetch': 88, 'commit': 176} upload_pack_children=88
proto-255 git=2.55.0 rc=0 Ran 11 tests OK auto_maint_spawns=0 by_parent={} upload_pack_children=88
proto-243 git=2.43.0 rc=0 Ran 11 tests OK auto_maint_spawns=0 by_parent={} upload_pack_children=88
```

This matches the plan's §3.4 (264 → 0). It also confirms that the guard's `git fetch` reads the fixture's
`.git/config`: the fetch-parented spawns go from 88 to 0. In proto, 88 upload-pack children remain because the
regression test traces its own fixture into its own directory: 89 fixtures, minus that one.

**Forced trigger, before and after (`force_run.sh`, force=1, Git 2.55):**

```
base-force-255  runs=3 ok=0 bad=3 errno39=100 leftover=100 results=[FAILED (errors=30); FAILED (errors=35); FAILED (errors=36)]
proto-force-255 runs=5 ok=5 bad=0 errno39=0  leftover=0   results=[5 OK]
```

- The base signature matches CI: 100 tracebacks `line 149, in run_guard`. The failing directories are
  `repo/.git/objects/pack` ×88, `repo/.git/objects` ×10 and `repo/.git` ×2.
- **A second symptom of the same race, not in the plan:** one base error is
  `CalledProcessError … 'commit' … 'fixture change' … exit status 128` at `line 183, in run_guard`
  (`out/base-force-255/r2.log:830-843`). The detached repack started by the first commit raced the second
  commit. The fix removes it as well (proto: 0 errors). This strengthens the case; see N1.

**Full file in a scratch `git clone --shared`, with the prototype committed on `c060a7cb`.** The commit is
`b53a5bd3…`, tree `5b3e136e…`, and `git diff --numstat` gives `28 0 scripts/tests/test_offline_ci.py`:
`fullfile-proto-255 runs=3 ok=3 … results=[3 OK (skipped=1)]`, `fullfile-proto-243 runs=2 ok=2 … [2 OK (skipped=1)]`,
`Ran 39 tests`. The skip is `test_root_executable_cannot_replace_git_under_the_workflow_env`, which is Windows-only.

**CI facts in the plan, re-read from the logs:**
- `run37713171379-attempt1…log`: L60 `git version 2.55.0`; L87 `[command]/usr/bin/git config --local gc.auto 0`;
  L949 `line 149, in run_guard`; L973 `OSError: [Errno 39] … /repo'`; L976-978 `Ran 38 tests` / `FAILED (errors=1, skipped=1)`.
  `wc -l` gives 1049 and the last line is `Cleaning up orphan processes`.
- `other-failures/run37159209057…log:85` shows the same `gc.auto 0` line, with Git 2.55.0 at L58.
- So the plan's §3.1 point stands: the real `gate-guard` checkout already runs with `gc.auto 0`. **Verified.**

**Coverage of the other fixtures (plan §3.3).** I read every `TemporaryDirectory` in the file: L47, L90, L149,
L350 and L631. The plan's table is correct. Only `run_guard` runs `commit` or `fetch` inside a temp repository.

**Residual (agree with the plan).** The diagnosis reports more CI failures than its model predicts (2 in 500
runs, against about 0.3 expected). The fix does not depend on which trigger fired. Disabling auto-maintenance
removes every path that `prepare_auto_maintenance` gates, and the source grep shows that is the only automatic
spawn path from these commands. The runner's packaged Git build options remain **unverified**.

### 2.2 The regression test (P2) — robust, deterministic, portable, minimal

- **Flip proof, my runs (5 each), `ProtectedFileGuardTests.test_fixture_repository_starts_no_auto_maintenance`:**
  - `flip-reverted-255 ok=0 bad=5 [5 FAILED (failures=1)]` · `flip-proto-255 ok=5 [5 OK]`
  - `flip-reverted-243 ok=0 bad=5 [5 FAILED (failures=1)]` · `flip-proto-243 ok=5 [5 OK]`
  - The assertion lists the maintenance argvs:
    `AssertionError: Lists differ: [] != [['git', 'maintenance', 'run', '--auto', …]]` / "Second list contains 3
    additional elements".
- **Why it is deterministic.** Without the config, `prepare_auto_maintenance` *always* spawns after `commit` and
  `fetch`; the loose-object trigger is irrelevant to the spawn. So the test fails on every run without the fix
  and passes on every run with it. It tests the mechanism, not the timing of the race.
- **No vacuous pass.** The `upload-pack` liveness assertion fails closed if trace2 is not honoured, or if the
  fixture stops fetching. The `"maintenance" in argv` element match is correct: trace2 prepends `git` for a
  `git_cmd` child, and the argv observed is `['git','maintenance','run','--auto',…]`.
- **Not itself racy when fixed.** The trace directory is a separate `TemporaryDirectory`. Every traced process
  is synchronous once no maintenance spawns. My runs left `leftover=0` in TMPDIR.
- **Portability.**
  - The test sits in `ProtectedFileGuardTests`, which carries
    `@unittest.skipUnless(os.name == "posix" and shutil.which("bash"), …)` (test file L137). On Windows,
    `os.name == "nt"`, so the whole class, including the new test, is skipped.
  - `from unittest import mock` is standard library.
  - `windows-offline-checks` runs this file (`validate-skills.yml:310`), but only when
    `github.event_name == 'push' || needs.changes.outputs.offline == 'true'` (L275). `offline` needs `^tools/` or
    `requirements-ci.(in|txt)` (L99). A PR touching only this file therefore skips the Windows job; the
    post-merge push run covers it.
  - **Windows is UNRUN here** (no Windows host). The portability claim rests on that reading.
- **Minimal.** 17 added lines, with one assertion of each kind. It cannot tell the two config lines apart
  (either alone disables maintenance on 2.55); that is by design, and `gc.auto 0` is for older Git.
- **Verdict on Q5: keep it.** It stays inside the one permitted file, meets the bug-fix floor, and is proven
  deterministic.

### 2.3 Single-file scope of P-FIX

- The plan's P-FIX touches only `scripts/tests/test_offline_ci.py`: §1 Paths, P4, P6, AC-F1 and AC-F10.
- On my scratch commit:
  - `git diff --numstat` → `28	0	scripts/tests/test_offline_ci.py`;
  - `git diff -U0 … | grep -c '^-[^-]'` → `0`;
  - `git diff --quiet … -- .github/; echo $?` → `0`.
- Moving the register entry to a separate PR keeps P-FIX at one file, as the owner's text requires. The owner's
  Q2 answer now explicitly approves that fourth PR. **No conflict remains.**

### 2.4 Exception-recording design

**What holds.**
- **Vehicle and timing match precedent.** APR-106 was recorded in the separate register-only PR #663, which
  merged at 2026-10-03T23:33:38Z, before PR #661 merged at 23:36:19Z (`gh api …/pulls/663`, `…/pulls/661`).
  `git merge-base --is-ancestor 5eb63bb8… cc8fd2cb…` → rc 0.
- **The owner's text requires recording before the merge.** "It merges once … covered by … recorded in the
  register". So the APR-103/104 recorded-after pattern is excluded, and the plan correctly follows APR-106.
- **The owner's Q2 option text confirms it:** "merged just before the protected PR … before the fix merges".
- **Binding a head-less owner decision to an exact head is precedented.** APR-106's owner selection named no
  SHA (register L3481-3496), and the entry bound it to `4a9e09dd…`.
- **Admin-merge pinning.** REST `PUT …/pulls/{n}/merge` with `sha` is correct. `gh pr list` returned
  `HTTP 403: GitHub GraphQL is not available from Claude Code sessions`, re-run by me, so the plan's advice to
  prefer REST is right. RCF-1's receipt records the merge "used `expectedHeadSha` pinned"
  (`$S/rcf/MERGE-RECEIPT.md:7`).
- **The ID.**
  - `git ls-remote origin refs/heads/main` → `c1acc075…`. PR #679 merged at 2026-10-08T15:55:22Z as `c1acc075`.
  - On `origin/main`, the register's highest ID is 119, with no duplicates (`sort | uniq -d | wc -l` → 0).
    `### AEGIS-APR-119` is at L5064.
  - The only open PR is #680, and its file list has no register file (`gh api …/pulls/680/files`).
  - **The next free ID is AEGIS-APR-120. The plan is right, but its #679 conflict reasoning is now moot (RC9).**
- **The verbatim quote.** I rebuilt the owner's text from the brief by joining its wrapped lines with single
  spaces. The result is 255 characters, with sha256 first 16 `95826ec00af9e24e`. It is byte-equal to both
  `> A third PR…` lines in the plan (Python comparison → `True`, twice).
- **No invention.** Each FORBIDDEN clause is derived from the wording ("only that test file", "that exact
  commit", "every other check green") or states a fact. The one-use limit comes from "one-time … for that exact
  commit".
- **AEGIS-APR-047 does not reach this file.** Its quoted phrase "guard scripts and tests … keep separate
  one-time owner decisions" is at register L1269-1271, and its scope is four BER files.

**What must change.**
- **Contradiction in schedule versus evidence (RC4).**
  - P-REG's Stage C starts at P-FIX's SD-D ACCEPT (§6.3 step 1), but the draft's Evidence cites "the Stage F
    review <comment link>" (§6.4). That comment cannot exist then.
  - Adding the link later moves P-REG's head and voids its D/E/F verdicts.
  - The entry also records the `gate-guard` check-run and run IDs and the failure conclusion at H. AC-F11
    (P-FIX CI) is declared possibly UNRUN at Stage D, so those values may not exist at the trigger either.
- **Ordering gap (RC5).**
  - P-REG may merge after P-FIX's SD-F, but before P-FIX's MG3 automated review has posted at H and been
    triaged.
  - A P1/P2 finding fixed after that point moves H. APR-120 is then unspendable and, under the owner's Q4
    answer, needs a fresh owner decision.
  - Merging P-REG only once MG3 is settled leaves Stage G as the only step after recording.
- **Owner answers not yet in the design (RC1–RC3, RC6).**
  - Q2 now authorizes P-REG "on the same terms (all seven stages, all checks green, admin merge allowed)".
  - Q3 defers consumption to the next register PR.
  - Q4 requires a fresh owner decision if the head moves after recording.
- **Proposal context (RC6).** The draft quotes the chosen option but not the question it answered. The
  `scoped-approval-register` checklist asks for a "dated verbatim current-session record with its proposal
  context". The Q2 question text, now in the brief, is the proposal context for the vehicle and timing. The
  original exception question text is not in the brief, so it must be obtained or declared absent.
- **Wrapped-line reconstruction.** The brief wraps the option text at about 120 columns, so the "verbatim"
  one-line form is a reconstruction: line breaks were joined with single spaces. That is likely right, but it is
  **unverified** until the coordinator confirms it (RC6c).
- **Self-authority separation (RC8).** The plan bars the P-REG entry author from being P-FIX's implementer or
  merge agent. It does not bar P-FIX's merge agent from holding P-REG's merge, which is the agent that lands the
  authority it later spends.
- **Two attribution errors (RC9b, c).**
  - The phrase "the append-only rule governs merged entries" appears in #663's body (body line 62, found by
    `gh api …/pulls/663 --jq .body | grep -n`), but **not** in APR-105. `grep -n 'append-only rule governs'` on
    the register → no match. APR-105 says "Once merged, any further change to it is an append".
  - "The PR cannot create that entry for itself" is APR-106's quotation of the Stage D audit (L3463-3464), not
    APR-106's own statement.

### 2.5 Acceptance criteria — runnable commands and concrete outputs

The per-criterion table is in §5. I ran these criteria against my scratch prototype commit and they produced
the plan's expected values:
- **AC-F1:** `28 0 …`, `0`.
- **AC-F2:** no output, rc 1. I also ran it case-insensitive: rc 1.
- **AC-F3:** `count_fixtures.py` gives base `run_guard_fixtures=88 test_methods_total=38` and proto `89` / `39`.
  My own `ast` listing gives 38 → 39, added `ProtectedFileGuardTests.test_fixture_repository_starts_no_auto_maintenance`,
  removed none.
- **AC-F4, F5, F6, F8:** as in §2.1–2.2.
- **AC-F10:** `0`, `1`, `1`.
- **AC-R5:** `check-markdown-links.py docs/approvals/APPROVAL_REGISTER.md` gives rc 0, with
  `files: 1 … broken: 0 dead: 0`. The script takes `paths` with `nargs="*"` (L375).
- **AC-F11 skip counts:** comparison log L958 `OK (skipped=1)` and L4538 `OK (skipped=5)`; attempt-2 log L946
  and L4526, the same values.

Criteria that need a concrete command are listed under RC7 and RC10.

### 2.6 Open questions Q1–Q6: who decides, and is any blocking?

| Q | Kind | Status now | Blocks the plan? |
| --- | --- | --- | --- |
| Q1 "every other check green" against path-scoped skips | **Coordinator procedural reading, with precedent** | **Precedent verified.** The heads of #677 (`ccf3fc22`) and #678 (`3797739c`) both show `tools-tests-linux`, `tools-tests-windows` and `windows-offline-checks` as `completed skipped`, with the other three `success` (`gh api …/commits/<h>/check-runs`). MG1 requires "Every **applicable** check" green. A stricter reading cannot be met inside "touching only that test file", because it would need a workflow change. The coordinator's position (skips recorded as skipped, never as passed) is consistent with all of this. | No |
| Q2 the fourth, register-only PR | **Owner decision** | **Answered:** "Yes, same terms (Recommended)" (BRIEF.md, 16:01:16Z) | No (RC1 applies it) |
| Q3 the consumption record | Procedural by the preamble ("A one-use grant can be used up even before a later event records that"), but the **owner has now decided it** | **Answered:** "Batch it later (Recommended)", meaning the next register PR together with FU-2's APR-119 consumption | No (RC2 applies it) |
| Q4 a head that moves after recording | **Owner decision** | **Answered:** "Ask me again (Recommended)", the APR-032→034 precedent | No (RC3 applies it) |
| Q5 keep the regression test | **Plan or coordinator procedural.** Stage B weighs in. | Coordinator's position is to keep it. **Auditor: keep it** (§2.2). | No |
| Q6 merge order with #679 | **Coordinator procedural** | **Moot.** #679 merged at 2026-10-08T15:55:22Z, and the next free ID is 120. | No |

With RC1–RC10 applied, the plan needs no further owner input. Only a contingency would need it: a head moving
after P-REG merges triggers the Q4 procedure.

BRIEF-COMMON rule 5 (do not touch the register by default) is **explicitly accepted as overridden** for P-REG.
The CIFIX brief requires the record, the owner's text says "recorded in the register", and the owner's Q2
answer approves the separate register PR. The register file is not a protected path. I extracted the live `gate_pattern` from `validate-skills.yml:528`
and matched it with bash `[[ =~ ]]` under nocasematch: `docs/approvals/APPROVAL_REGISTER.md -> not gated`,
`scripts/tests/test_offline_ci.py -> GATE`. That agrees with the plan's result.

## 3. Required changes (for PLAN-rev2)

1. **RC1 — Apply the owner's Q2 answer.**
   - Update the input table to BRIEF.md sha256 `5419a0dacaf8e092521c739cb09b6d73f0ebe5a967f5484f6d95d629701159c6`.
   - Close Q2 as owner-decided. In §6.5, rest P-REG's authority on the owner's Q2 answer, quoted verbatim:
     the question, the label "Yes, same terms (Recommended)" and its option text, recorded by the coordinator at
     2026-10-08T16:01:16Z.
   - State its terms as worded: "all seven stages, all checks green, admin merge allowed". Apply the Q1 reading
     to P-REG's skipped jobs too.
   - AEGIS-APR-100/048/050 may stay as supporting mechanics, not as the sole authority.
   - Remove the "Q2 asks the coordinator to confirm" dependencies in §1 and §6.5.
2. **RC2 — Apply the owner's Q3 answer.**
   - Remove P-CONS from CIFIX-1: §1 Paths, §6.6, §7.3, §9 Stage G step 10 and the §10 ETA row.
   - The consumption of APR-120 goes into **the next register PR, together with FU-2's APR-119 consumption**.
     Drop "expected 121": the ID is re-derived when that PR is written.
   - P-FIX's merge receipt must carry what that later entry needs: the merge time, the squash commit, and the
     non-ancestry result of `git merge-base --is-ancestor H <merge>`. Keep APR-107 as the template.
3. **RC3 — Apply the owner's Q4 answer as a fixed procedure, not an open question.**
   - **Head moves after P-REG has merged:** APR-120 is spent on nothing, and P-FIX is not merged on it. The
     coordinator asks the owner again, following APR-032→033→034. Only after a fresh owner answer naming the new
     head, one register-only PR (same terms) appends an EXPIRED event for APR-120 and a new GRANT for that head.
   - **Head moves before P-REG has merged:** the plan's existing in-place rebuild of the unmerged entry (§6.3
     step 3) applies, with P-REG's verdicts voided.
   - State the reading this rests on: "recorded" means **merged on the default branch**, which is where MG4 reads
     it. Flag that reading to the coordinator, because the owner's Q4 text says "after the exception is recorded".
4. **RC4 — Fix the contradiction between P-REG's trigger and its evidence.**
   - Remove "the Stage F review <comment link>" from the §6.4 Evidence. APR-106's precedent cites only the Stage D
     audit. Keep P-FIX's SD-F ACCEPT at H as a **P-REG merge precondition** only.
   - Make P-REG's Stage C entry condition: P-FIX's `SD-D: ACCEPT` at H, **and** every check run at H completed,
     with `gate-guard` concluding failure and its log naming only `scripts/tests/test_offline_ci.py`,
     `changes` and `validate-skills` concluding success, and the three path-scoped jobs skipped. The entry
     records those IDs and conclusions, so they must exist when it is written.
5. **RC5 — Tighten when P-REG may merge.**
   - P-REG merges only after P-FIX's `SD-F: ACCEPT` at H **and** P-FIX's MG3 condition is met at H: the automated
     review has posted for H, or is confirmed unavailable for H, and every P0–P2 finding is triaged with no head
     move.
   - Then the only step left after recording is P-FIX's Stage G. This honours the Q2 option text "merged just
     before the protected PR" and makes RC3's re-ask unlikely.
6. **RC6 — Changes to the draft entry (§6.4).**
   - (a) Add the Q2 question and answer verbatim as the owner's approval of the recording vehicle and its timing.
     Add the Q4 answer verbatim to Scope FORBIDDEN or Expiry: a moved head needs a fresh owner decision. Mention
     Q3's timing in the Status line if wanted.
   - (b) Add the **proposal context** for the original grant: the verbatim AskUserQuestion text the owner answered
     with "Yes, one-time exception (Recommended)", obtained from the coordinator by P-REG's Stage C. If it was
     not relayed, the entry must say so explicitly.
   - (c) Have the coordinator confirm the one-line form of the 255-character option text. The brief wraps it, and
     the plan joins the lines with single spaces. Record that confirmation in the entry's Evidence.
   - (d) RC4's removal of the Stage F link.
7. **RC7 — Make AC-R1 a real append-only proof.**
   - `numstat` deletions `0` does not prove that prior entries are unchanged: a line inserted *inside* an existing
     entry also shows 0 deletions.
   - Add a prefix check: the base blob must be a byte prefix of the head blob. For example:
     `git show Bʳ:docs/approvals/APPROVAL_REGISTER.md > b; git show Hʳ:docs/approvals/APPROVAL_REGISTER.md > h; cmp -n "$(stat -c %s b)" b h; echo $?`
     → `0`, with a single `git diff -U0` hunk that starts after the base's last line.
   - State the trailing-newline check (CONTRIBUTING documentation rule 7).
8. **RC8 — Add to the stage-separation rule in §9.**
   - **P-FIX's Stage G holder holds no stage of P-REG**, so the agent that spends APR-120 neither authored,
     audited, reviewed nor merged it.
   - Keep the existing rule that P-REG's entry author is neither P-FIX's Stage C author nor its merge agent.
9. **RC9 — Correct the stale and misattributed facts.**
   - (a) **Base moved.**
     - `origin/main` = `c1acc075910ea1e849401e18cdb60df31c09ef30`. PR #679 merged at 2026-10-08T15:55:22Z.
     - The register maximum on main is 119, so the next free ID is 120. The §6.3 #679-conflict paragraph and Q6
       are moot.
     - `git diff --quiet c060a7cb origin/main -- scripts/tests/test_offline_ci.py .github/` → rc 0, so the
       prototype and its line numbers still apply.
     - #679 changed `artifacts/audits/*.json` and the register (`git diff --name-only`, 7 files), so AC-F9's and
       AC-F3's base values must be re-derived at `c1acc075`. The plan already says to re-derive; the figures
       must be updated.
   - (b) §6.3 step 3: the "append-only rule governs merged entries" wording is from #663's body only, not APR-105.
     APR-105 says "Once merged, any further change to it is an append".
   - (c) §1: "The PR cannot create that entry for itself" is APR-106 *quoting the Stage D audit* of #661.
10. **RC10 — Make five acceptance criteria concrete** (each NEEDS-REWRITE, §5).
    - **AC-F3:** give the `ast` name-listing command, for example the four-line snippet in §2.5's evidence.
      Expected: "added: [the P2 test], removed: []".
    - **AC-F5:** give the exact deletion command,
      `sed -i '/git("config", "maintenance.auto", "false")/d; /git("config", "gc.auto", "0")/d'`, and how each Git
      is selected (`PATH=G55:$PATH` against the system PATH). Expected: `FAILED (failures=1)`, and the assertion
      lists `['git', 'maintenance', 'run', '--auto', …]` argvs.
    - **AC-F12:** expect `ls -A <TMPDIR>` to be **empty**. That also covers `aegis-ci-trace-*`.
    - **AC-R2:** give the open-PR enumeration, for example `gh api 'repos/…/pulls?state=open'` and, for each,
      `git fetch origin pull/<n>/head` plus the `grep -o '^### AEGIS-APR-[0-9]*'` maximum.
    - **AC-R4:** define how the new entry is extracted, for example `awk '/^### AEGIS-APR-120:/,0'` on the file at
      Hʳ, before the `grep -c '<H>'`.

## 4. Non-blocking notes (carry into the PR evidence; no plan change required)

- **N1.** Under the forced trigger, base also fails with `CalledProcessError … exit status 128` on the second
  commit (`line 183, in run_guard`). The same race causes it, and the fix removes it. Worth one line in P-FIX's
  evidence.
- **N2.** AC-F1's `grep -c '^-[^-]'` does not count a removed blank line. The `numstat` deletions column is the
  governing measure.
- **N3.** Stage E's unrun list should name Windows explicitly. `windows-offline-checks` is skipped at H by the
  path filter. `ProtectedFileGuardTests` would also skip on Windows by its class decorator. The post-merge push
  run is the Windows evidence.
- **N4.** In the reverted tree, a detached maintenance child can, rarely, add a cleanup error next to the
  assertion failure. I observed 0 of 10. Read AC-F5 as "the assertion failure is present".
- **N5.** I saw `gh pr list` refused with GraphQL 403 in this session, which supports §6.3(b).

## 5. Acceptance-criteria review (`acceptance-criteria-reviewer`, condensed)

| AC | Verdict | Evidence that proves it, or the gap |
| --- | --- | --- |
| F1 | TESTABLE | `numstat` line plus `0`. Reproduced: `28 0 …`. See N2. |
| F2 | TESTABLE | grep exits 1. Reproduced, case-sensitive and insensitive. |
| F3 | NEEDS-REWRITE | The `ast` listing has no command (RC10). The base and head values must be re-derived (RC9a). |
| F4 | TESTABLE | trace counts 264 → 0. Reproduced with my own counter. |
| F5 | NEEDS-REWRITE | The deletion command and Git selection are implicit (RC10). The flip itself was reproduced 5/5 on each Git. |
| F6 | TESTABLE | Base `fail>=1, errno39>0`; head `10/10, 0, 0`. Reproduced: base 3/3 failed, 100 lines; proto 5/5 OK. |
| F7 | TESTABLE | 20× `OK (skipped=1)`, 0 `Errno 39`. |
| F8 | TESTABLE | `Ran 39 tests`, `OK (skipped=1)`. Reproduced on both Gits. |
| F9 | TESTABLE | "Same summary as at B". The B values must be re-derived at `c1acc075` (RC9a). |
| F10 | TESTABLE | `0`, `1`, `1`. Reproduced. |
| F11 | TESTABLE after publication | Declared not verifiable at the head before push, as SD-A requires. The expected six check runs match the workflow's six jobs (`validate-skills.yml` is the only workflow: `ls .github/workflows/`). |
| F12 | NEEDS-REWRITE | The expected value names only `aegis-ci-guard-*`; it should be "empty" (RC10). |
| R1 | NEEDS-REWRITE | Zero deletions does not prove an append (RC7). |
| R2 | NEEDS-REWRITE | The open-PR maximum has no command (RC10). |
| R3 | TESTABLE | `grep -cF` → `1`. The quote was verified byte-equal. |
| R4 | TESTABLE once extraction is defined | "Within the new entry" needs the extraction step (RC10). Counted as TESTABLE with RC10 applied. |
| R5 | TESTABLE | Link checker rc 0 on the register at `c060a7cb`, reproduced. |
| R6 | TESTABLE | All green including `gate-guard`; three jobs skipped. |

Summary: 13 TESTABLE, 5 NEEDS-REWRITE, 0 UNTESTABLE.

Gaps (not requirements; the planner and coordinator decide):
- **GAP1, error class.** No criterion checks that P-REG's entry carries the owner's Q2/Q4 answers. RC6 would
  add one, for example a `grep -cF` for each answer label.
- **GAP2, ordering.** P-REG's merge preconditions (RC4/RC5) live only in §9 prose. Consider an AC-R7: "P-FIX's
  SD-F ACCEPT and MG3 settled at H before Hʳ merges".
- **GAP3, boundary.** No criterion covers a second register PR landing between P-REG's authoring and its merge.
  AC-R2's re-check at merge covers it, provided RC10's enumeration is used.

## 6. Handoff block

1. **Decision IDs.** Bound by `SD-A`–`SD-G` and `MG1`–`MG5`, unchanged. Relies on AEGIS-APR-047 (does not cover
   this change), 048, 050, 100 and 106/107 (precedent), and on the owner's 2026-10-08 answers to Q2/Q3/Q4. This
   audit changes no decision.
2. **Changed files:** none in the repository.
   - `git status --porcelain | wc -l` → `0`; `git rev-parse HEAD` → `c060a7cb…` (detached, unchanged).
   - Local metadata touched by reads, **disclosed**:
     - `git fetch origin main` refreshed `refs/remotes/origin/main` to `c1acc075…`.
     - `git fetch origin pull/680/head` wrote `.git/FETCH_HEAD`.
     - No branch, index or working-tree change; `git for-each-ref refs/remotes/pr | wc -l` → `0`.
   - Scratch written: this file; `$S/cifix/b-audit/scripts/{force_run.sh,trace_spawns.sh}`;
     `$S/cifix/b-audit/trees/{base,proto,reverted}`; `$S/cifix/b-audit/clone` (a `git clone --shared` with one
     local scratch commit `b53a5bd3…`, never pushed); `$S/cifix/b-audit/out/**`.
   - **NOT touched:** every repository path, `.github/`, the register, GitHub (reads only: `gh api` GETs and
     `gh pr list`, which was refused), and reserved scope.
3. **Proven invocation.** Every figure above carries its command and output.
   - **Unverified:** the runner's Git build options; the one-line form of the owner's option text (RC6c).
   - **UNRUN:** Windows behaviour; Python 3.14.
4. **Deviation flags.**
   - **Plan deviations found:** the schedule/evidence contradiction (RC4) and the stale facts (RC9).
   - **Own deviations:** none. I used my own harnesses. The planner's `count_fixtures.py` was re-run only as an
     instrument, and its result was cross-checked by an independent `ast` count.
5. **Continuation.** The planner, as Stage A holder, produces PLAN-rev2 applying RC1–RC10. Stage B re-audits it
   at its new sha256, by a different agent from the planner. This audit's holder may re-audit, because it is the
   same stage of the same change. Stage C must not start on rev1.

**Timing.**
- Started: 2026-10-08T15:52:33Z (`date -u`).
- Text completed: 2026-10-08T16:07:03Z (`date -u`). The finish timestamp and the file hash are reported in the
  handoff, because adding them here would change the hash.
- ETA: none was given to me at the start, so no comparison is possible. Active time was not measured separately.
