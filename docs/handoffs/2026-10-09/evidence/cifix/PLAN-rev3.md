# CIFIX-1 — Stage A PLAN, revision 3

**Disposition: SD-A: COMPLETE.** This is a plan for P-FIX and its dependent P-REG, ready for an independent Stage B audit of these exact bytes. It is not an implementation, test result, audit, merge authorization, or Stage B verdict. No later stage may start on rev2.

**Item:** Fix the Errno 39 race in `scripts/tests/test_offline_ci.py`.
**Holder:** `/root/cifix_plan`, Stage A only. The coordinator supplied start `2026-10-08 18:46:08 UTC` and active-work ETA 25–40 minutes. Finish, measured wall time, and this file's SHA-256 are reported after the final write; active time is not separately measured.
**Read-only source clone:** `C:\src\Project Aegis\Project-Aegis`.
**Only file written by this stage:** `C:\src\Codex Projects\Project Aegis\cifix\PLAN-rev3.md`.
**Main pin:** `5228977920ee479e1fe1ec6b8d56f8fc24c14947` (M).
**Handoff pin:** `32f5ae25780c4802184a63d4063507fcf31b3a37` (S).
**Snapshot prefix:** `docs/evidence/session-handoff-2026-10-08/` (all snapshot paths below are relative to this prefix at S).

This revision supersedes rev2's plan, not its historical evidence. It applies RC11–RC16 and preserves RC1–RC10. The later owner answer closes OQ-C and overrides RC11(c)'s earlier request to leave it open. The snapshot branch remains unmerged and unedited; its statements are source records, not current policy. Current policy comes from M and current owner instructions.

## 1. Inputs, current observations, and evidence limits

Read from M: `AGENTS.md`, `CLAUDE.md`, `docs/delivery-workflow.md`, `CONTRIBUTING.md`, the approval-register preamble, relevant grants and their references across the full register, the complete target script, workflow path filters/guard, and the PR-body binding rules. Role A is corroborated by `# Project Aegis` at the README top and all three landmarks returned by `git ls-tree`: `docs/skills-catalog.md`, `scripts/validate-skills.py`, `artifacts/audits/skill-contract-audit-baseline.json`. `git remote -v` identifies `https://github.com/ModernNomad-98/Project-Aegis.git`.

| Captured input at S | SHA-256 of actual Git blob bytes |
| --- | --- |
| `HANDOFF.md` | `46cfef81a5f24b5d25b1f96623abf67ad18407720644f031c7c90a8cd2ddf16b` |
| `owner-messages.md` | `443f791038c41f7bffabc0bb6841b1aa9191f351bfc52c8e31b8f2ef7392b061` |
| `owner-askuserquestion-answers.md` | `a4c4524fe069e8a7347d180f24c2e9e2ebaf5b73982c26b034705a620e45b255` |
| `artifacts/cifix/BRIEF.md` | `682eb1cf401efda27a51c59ca006fa97812df13a259664ccd227653f13f37364` |
| `artifacts/cifix/PLAN-rev2.md` | `6ef9a2aee2ba612d842643ed7246734c544c736bc09554fb715eedc39127498c` |
| `artifacts/cifix/PLAN-AUDIT-rev2.md` | `4bd41cb236a2361afddbfbdfa9bdae255dec1104e857368d3682ce32963f1846` |
| `artifacts/cifix/owner-q2-q4-verbatim.json` | `74c8cd5a559b1398fe411d6d75f4da1be23fe788b0845cdb59dcfb09bc82f1c2` |
| `artifacts/ci-diag/DIAGNOSIS.md` | `522ea312e15f7d7f7b930f20e508c632b2fb54cfbf783c8734fe5d1710c09cfb` |

The RC11 historical BRIEF hash `31dec83bb660d843f2f3c96f372284b8f535354f4c3f1f185f74205bb847d2fb` preceded the later OQ-C section. It is not the saved brief's hash. The older plan/audit hashes inside the snapshot identify scratch originals; `REDACTIONS.md` explains changed copies and excluded raw logs/clones. This plan binds the available snapshot bytes above without claiming original and saved bytes are identical. The JSON's hash is unchanged. Its transcript fidelity is the previous coordinator's attestation, not independently reconstructed from unavailable transcripts. Its extraction has no supplied recording timestamp; none is invented.

| Observation in this planning turn | Command and relevant output |
| --- | --- |
| Local refs match both pins | `git rev-parse origin/main` → M; `git rev-parse origin/claude/sharp-lovelace-urgxpz` → S |
| Current remote main and open-PR count | Coordinator-provided current-turn evidence: `gh api repos/ModernNomad-98/Project-Aegis/commits/main --jq '.sha'` → M, exit 0; `gh api 'repos/ModernNomad-98/Project-Aegis/pulls?state=open&per_page=100' --jq 'length'` → `0`, exit 0; coordinator's fetch of main and handoff exited 0. These are relayed command results, not this planner's live calls. |
| Target at M | SHA-256 over `git show M:scripts/tests/test_offline_ci.py` bytes → `4fa62a8b03bf2d72ded776a73881dfbd18a1c6434e0ca4d9aef2e8de07d3a022`; `raw.count(b'\n')` → `750`; Python AST → 38 total test methods, 10 in `ProtectedFileGuardTests` |
| Scope unchanged since diagnosis base | `git diff --quiet c060a7cb origin/main -- scripts/tests/test_offline_ci.py .github/workflows/ scripts/ci/record-check.py scripts/validate-skills.py` → exit 0 |
| Register at M | Heading regex `^### AEGIS-APR-(\d+):` over the complete blob → 119 headings, maximum 119, zero duplicate IDs; SHA-256 `1a35c8c84de597319952a75d7ee5545a74829f0f07a7c12287e1fe43f6368970` |
| Protected paths | Extracted `gate_pattern` at M; case-insensitive regex matches test path (`True`) and excludes register path (`False`). Workflow `changes` selects neither advisory scope for either planned path. |
| Dirty source clone | `git status --porcelain` → `?? artifacts/recovery/` and `?? artifacts/reviews/`, plus inaccessible user-ignore warnings. Preserve these; no write, clean, reset, stash, checkout, or staging here. |
| Local live read limitation | Planner's `git ls-remote` and GitHub GETs for protection/rules/open PRs failed with restricted-network socket errors. No mutation occurred. Protection/rulesets and subsequent remote drift remain unverified here. |

The independently reported historical technical evidence in PLAN-AUDIT-rev2 §3 is a reason to pursue this fix, not proof of a future head: Git 2.55 forced base runs failed 3/3 with 49 Errno 39 lines; prototype passed 10/10; trace maintenance spawns fell 264→0; the new test flipped 5/5 each way on Git 2.55 and 2.43; full file reported 39 tests and `OK (skipped=1)`; natural stress passed 20/20. Raw stress logs, prototype and CIFIX harness files are not in this snapshot. No such test was run by this Stage A holder. Later holders must produce fresh evidence under §5–§6, rather than cite missing scratch paths as executable dependencies.

**Drift rule:** if M changes during this Stage A work, or current evidence conflicts, stop and report to the coordinator. Before implementation, refresh main in the isolated implementation clone; a base different from M returns to Stage A for reconciliation and a newly captured/audited plan. Once P-FIX exists, the planned register-only advance and later main checks follow §8, without silently rebasing P-FIX.

## 2. Skills and classification

| Aegis skill read from M | Applied part | Result |
| --- | --- | --- |
| `change-classification-gate` and `references/classification-matrix.md` | Classify actual paths, lock scope, preserve each validation floor | P-FIX bug-fix + qa-test-only; reproduce failure, prove the flip, add regression. P-REG documentary grant transcription on a security-relevant governance surface. |
| `human-approval-boundary` | Match one-time guard exception, recording vehicle, and changed-head response to exact owner words | Existing grants apply within scope; silence is not size approval; Q4 requires a new answer after a recorded exception's head moves. |
| `scoped-approval-register` and `references/register-format.md` | Preserve proposal, labels, option text, limits, lifecycle and evidence attribution | Fillable entry in §7; immutable merged records; consumption and expiry are distinct events. |
| `risk-tiered-validation-selector` | Map paths to required depth; selector does not execute | `scripts/` is never docs-only: P-FIX full repository tier plus focused race proof. P-REG register/link/append evidence plus its ordinary repository CI. No new classifier or skill is built. |

`ai-task-decomposer` was read and considered; this is one small fix plus its specifically authorized recording change, so it is not used to invent a larger task decomposition. No installed skill owns single-change Stage A, as the delivery workflow itself records: Stage A is procedurally enforced. No MANUAL-ONLY skill is invoked. Every subsequent stage must read its own matching skill, verify that it owns that scope, and report only its own actual use.

**P-FIX scope contract:** only `scripts/tests/test_offline_ci.py`, additions only. Security-relevant answer: Yes, `scripts/` and a protected guard-test path. Approval: owner one-time exception on an exact head, recorded by P-REG on main before merge. APR-047 excludes guard scripts/tests; it supplies no exception here.

**P-REG scope contract:** only `docs/approvals/APPROVAL_REGISTER.md`, one GRANT appended at EOF. Class: docs-only transcription, with security-relevant governance treatment; no permission/configuration behavior changes. Approval: owner's Q2 reply to the complete register-PR proposal. APR-100/048/050 support delivery mechanics and review waiting; they are not the work grant or a substitute for Q2. Security-relevant answer: Yes, owner approval register.

Both exclude `.github/`, other scripts, skills, instruction files, settings, guard patterns, branch protection, every new skill build, and reserved evaluation/rehearsal/VM/Stage4B/calibration/provider work. Do not copy reserved pins, fixtures, flags or budgets. Do not write the automated reviewer's trigger phrase. Ordinary existing hosted CI results may be observed; this plan authorizes no manual execution or repair of reserved packages.

**Declared limits under SD-A:**

- AC-F11 and AC-R6 are unavailable before each candidate is published; hosted checks are measured afterward. AC-R7 is a merge-time criterion, not something P-REG's Stage D can already prove. D may record these explicitly as UNRUN with this reason, and E/G must resolve them at their stated gates.
- A promise that the race can never recur is not verifiable at one head. Deterministic flip, trace evidence and bounded forced/natural runs are the acceptance tests instead.
- AC-F4–F8 require POSIX bash and the selected Git versions. Availability on the later execution host is unverified; Windows Python does not supply POSIX coverage because the entire guard class skips. Resolve the environment before SD-C: COMPLETE. If it is unavailable, report the specific gap to the coordinator; do not count skipped tests or historical prototypes as passing candidate evidence.
- Python 3.14 and pwsh were unavailable in the prior Linux session; that fact is historical. This machine has `C:\Python314\python.exe`; no suite has been run here. Later stages measure their own versions. Any local full-tier step outside the authorized scope or unavailable locally is named UNRUN with the exact CI job/step that covers it at H, or with what would resolve it. Nothing in the reserved scope is run manually to fill a local gap.
- `windows-offline-checks` is path-skipped for these PRs. It would run this changed module if selected. The new POSIX-only method will skip on Windows, though the standard-library `mock` import still executes. Post-merge push CI is Windows evidence; it does not prove the race fix on Windows or retroactively gate the earlier merge.

## 3. Intended behavior and technical choice

`ProtectedFileGuardTests.run_guard` creates a temporary Git repository, commits twice, and executes the workflow guard, which fetches from that fixture. The temporary repository currently receives no local auto-maintenance suppression. Add immediately after `git("init", "--quiet")`, before either commit:

```python
git("config", "maintenance.auto", "false")
git("config", "gc.auto", "0")
```

Include a short explanatory comment naming runs 36695924676 and 37713171379. No real guard command or workflow changes. The reported causal chain is detached auto-maintenance/repack writing `.git` while `TemporaryDirectory` removes it. The source inspection and independent reproduction in the prior audit cover the fixture's two commits and guard fetch. Other target-file fixtures use non-maintenance Git commands or the persistent checkout. This planning turn confirms the script is byte-identical across the relevant old/current scope; it does not independently rerun the causal experiment. The coordinator's separate read-only technical helper corroborated the three launch paths at target-file lines166/183 and workflow line493; it ran no tests and is not a Stage B reviewer. The exact leftover writer in the original hosted failure remains a historical inference: DIAGNOSIS lines268–273 acknowledge unavailable leftover/build evidence. Do not upgrade consistent mechanism evidence into a fresh proof of the old hosted process.

Keep repository-local config rather than injected high-precedence environment config: it reaches both fixture commits and the guard fetch, and the historical trace reported no residual maintenance spawn. Changing fetch would exceed the one-file scope. Sleeps, retries, cleanup-error suppression, timeouts, foreground maintenance and quarantine do not establish removal of the maintenance side effect.

**Self-scrutiny:** a runner's higher-precedence Git config or different build could defeat this setting. Conversely, inherited suppression could make an unfixed helper show no spawn despite a live trace. Static workflow environment checks inspect YAML and cannot establish the actual runner process environment. Build options remain unverified. Fresh isolated trace/flip tests must confirm the mechanism; the new regression also runs within `validate-skills` on H in the actual runner environment. A successful job alone is insufficient unless its log proves that the added test ran as part of the expected suite, and it does not replace AC-F5's unfixed negative control. A remaining spawn, absent trace-liveness proof, failure of that negative control, or conflicting source evidence changes this recommendation and returns to Stage A. The claimed old-Git benefit of `gc.auto=0` is unverified for versions not tested.

## 4. Regression design and size disclosure

Add `from unittest import mock` beside the existing `unittest` import and exactly one method, `ProtectedFileGuardTests.test_fixture_repository_starts_no_auto_maintenance`. It inherits the existing POSIX-only class condition. Inside a separate temporary trace directory, use `mock.patch.dict(os.environ, {"GIT_TRACE2_EVENT": <absolute trace path>})` around one `self.run_guard(["scripts/tests/fixture.py"])`. Read newline-delimited JSON events, assert guard return code 1, assert at least one `child_start` argv contains `upload-pack` (trace liveness), and assert there are no `child_start` records with an argv element `maintenance`, or both elements `gc` and `--auto`. Preserve all existing assertions and test methods.

This design is an additive change of about 28 lines in the prior prototype: two config lines, comment, import and one regression test. OQ-B is closed as a disclosure: BRIEF records at `2026-10-08T16:20:07Z` that the coordinator told the owner “about 28 lines.” The later brief explicitly calls this disclosure, not owner approval of the size. Authority rests on the chosen option's file scope and the authorized fix; lack of objection is not approval. Stage C reports actual `git diff --numstat` additions `a`; if `a != 28`, stop the P-REG Stage C handoff and tell the coordinator the exact size and reason. The coordinator resolves the disclosure/scope question before recording; this is not an invented 40-line allowance or automatic prohibition on another size. A scope expansion returns to Stage A and the applicable approval boundary.

Use a fresh isolated branch from M (suggested name `claude/sharp-lovelace-urgxpz-ci-fix`; verify it is unused). Keep the snapshot branch and dirty source clone untouched. Stage exactly the test file, verify branch identity before each commit/push/PR, and sign off every commit. One initial commit is preferred; subsequent authorized corrections may be additional signed commits rather than requiring an unnecessary history rewrite. Any head move invalidates all head-bound evidence and invokes §8 as applicable. Commit text names the root cause and both run IDs.

**Self-scrutiny:** the owner's question described two lines, so the added regression must be disclosed rather than hidden. The selected option scopes by file, the classification matrix requires a regression test for bug fixes, and the existing independent audit supports this design. Evidence that the owner limited the change to two total lines, that the test masks the guard, or that its size/scope expands materially changes the recommendation. Keep the regression only with the real size recorded and the non-vacuous flip proof.

## 5. Execution protocol for later holders (not run by Stage A)

All commands in this section are recipes for authorized Stage C/D/E holders. Bash recipes require a POSIX execution environment; do not paste them into PowerShell or assume Git Bash makes Windows Python POSIX. Assign variables explicitly and never use angle-bracket placeholders as shell arguments. Keep logs and harnesses under a coordinator-assigned scratch directory outside the candidate tree, with no credentials. Record versions, command, exit code, stdout/stderr, input SHAs, and harness SHA-256. Do not reuse missing historical `/tmp` paths.

1. Read current main and the five startup/policy sources; record M and source role. In a clean isolated clone at M, use full history and `core.autocrlf=false`. Record `B=M`, H after implementation, `git rev-parse "$H^{tree}"`, and `git merge-base "$B" "$H"` (must be B). Refresh and stop on unexpected base drift per §1.
2. Record `git --version`, `python3 --version`, `command -v bash`, and availability of Python 3.14 and pwsh. Select explicit Git 2.55.0 and Git 2.43.0 binaries in separate invocations; confirm each version before its run. If missing, resolve through the coordinator without substituting a skipped Windows class.
3. For each run, use a unique scratch TMPDIR/TEMP/TMP, `PYTHONDONTWRITEBYTECODE=1`, and `python3 -B -P`. Remove every inherited `GIT_CONFIG*` name from the child environment, then explicitly set `GIT_CONFIG_GLOBAL` to an empty scratch file and `GIT_CONFIG_NOSYSTEM=1`; only forced mode then adds the deliberate forced-trigger settings. This isolates inherited system/global/runtime suppression so the unfixed negative control is meaningful. Record only the safe scratch settings being deliberately supplied, not unknown inherited values. Never mutate real system/global Git config. Preserve the candidate regression's normal environment behavior; isolation belongs to the external validation invocation.
4. `T(B)` and `T(H)` mean clean exported trees using `git archive`; they may run only `ProtectedFileGuardTests` or its single method. **Every full-file test and repository check runs in a real isolated clone checked out at its exact revision, never an archive.** The prior audit measured archive false failures: recorder `git rev-parse` failed, full file had six failures/two errors, and validator/link tests also failed for missing Git metadata.
5. Run the repository baseline in the clone at B and repeat at H: `python3 -B -P scripts/validate-skills.py`; `python3 -B -P scripts/tests/test_validator.py`; `python3 -B -P scripts/tests/test_audit_skill_contracts.py`; `python3 -B -P scripts/tests/test_markdown_links.py`; `python3 -B -P scripts/tests/test_offline_ci.py`. Historical POSIX references are 195 valid/0 warnings, 181 gate assertions, 76 audit assertions, 23 link tests, and 38 offline tests with one skip; expected H adds one offline test. Measure rather than transplant the references.

For trace/forced runs, a later holder creates a small scratch driver with the following specified behavior: invoke the selected Python directly on the target file with selector `ProtectedFileGuardTests`; pass the selected Git's directory first on PATH; collect exit and both streams separately; set an absolute `GIT_TRACE2_EVENT` path outside TMPDIR. Parse each JSON line, count `child_start` maintenance or `gc --auto` argv and `start` maintenance processes, count `upload-pack` child starts for liveness, report Errno 39 occurrences and list TMPDIR contents after the process returns. For forced mode only, add `GIT_CONFIG_COUNT=1`, `GIT_CONFIG_KEY_0=maintenance.geometric-repack.auto`, `GIT_CONFIG_VALUE_0=-1`. Never enable force for the natural/flip runs. Hash and retain the driver; independent D checks its logic against these instructions before relying on its summary. Detailed commands below can also be executed directly without a driver.

To count fixtures without relying on an absent historical script, execute the following in each exported tree, with a unique TMPDIR and the same selected Git. This counts calls while retaining the original function and all test assertions:

```bash
python3 -I -B - "$TREE" <<'PY'
import pathlib, runpy, sys, unittest
ns = runpy.run_path(str(pathlib.Path(sys.argv[1]) / 'scripts/tests/test_offline_ci.py'))
cls = ns['ProtectedFileGuardTests']
original = cls.run_guard
calls = [0]
def counted(self, *args, **kwargs):
    calls[0] += 1
    return original(self, *args, **kwargs)
cls.run_guard = counted
result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
print('run_guard_fixtures=', calls[0], 'class_tests=', result.testsRun, 'skips=', len(result.skipped))
raise SystemExit(not result.wasSuccessful())
PY
```

This is a run recipe, not a claim it was executed or validated by this planner. Any recipe error is reported and corrected under the audited plan's intent, with changed harness bytes recorded. A change to an acceptance property requires plan re-audit.

## 6. Acceptance criteria

Set `R=ModernNomad-98/Project-Aegis`, `F=scripts/tests/test_offline_ci.py`, and `REG=docs/approvals/APPROVAL_REGISTER.md`. B/H are P-FIX base/head; BR/HR are P-REG base/head; PF/PR are their integer PR numbers; N is the allocated approval ID (candidate 120). Variables are assigned verified values before commands run. Every candidate check uses the same immutable head/tree/base.

### P-FIX

**AC-F1 — One additive file with disclosed size.** `git diff --numstat "$B...$H"` returns exactly `a 0 scripts/tests/test_offline_ci.py`; `git diff --name-only "$B...$H"` has that sole path. The numstat deletion column, including deleted blank lines, governs. Report a; 28 is the disclosed prototype size, not an upper bound. Apply §4's notification/hold if different. Review diff positions against §3–§4.

**AC-F2 — No weakening.** `git diff "$B...$H" -- "$F" | grep -inE '^\+.*(skip|expectedFailure|ignore_cleanup_errors|retry|sleep|timeout)'` has no output (grep exit 1); an independent diff read confirms no assertion change, removal, retry, quarantine or suppression. A match requires investigation, not an automatic removal of the check.

**AC-F3 — Exactly one regression and one fixture call added.** Run this in the clone; it reads Git blobs without checking out or importing candidate code:

```bash
python3 -I -B - "$B" "$H" "$F" <<'PY'
import ast, subprocess, sys
def names(rev):
    raw = subprocess.check_output(['git', 'show', rev + ':' + sys.argv[3]])
    return {c.name + '.' + m.name for c in ast.parse(raw).body if isinstance(c, ast.ClassDef)
            for m in c.body if isinstance(m, ast.FunctionDef) and m.name.startswith('test_')}
b, h = names(sys.argv[1]), names(sys.argv[2])
print('added:', sorted(h-b), 'removed:', sorted(b-h), 'base=', len(b), 'head=', len(h))
raise SystemExit(not (h-b == {'ProtectedFileGuardTests.test_fixture_repository_starts_no_auto_maintenance'} and not b-h and len(h) == len(b)+1))
PY
```

Expected counts 38→39 at M. Run §5's counter at B/H: fixture calls 88→89, class tests 10→11, no skipped guard tests. If measured baseline differs, stop for reconciliation rather than adjusting an expected value silently.

**AC-F4 — No maintenance spawn on any fixture path.** For each selected Git, in T(B) and T(H): `GIT_TRACE2_EVENT="$TRACE" python3 -B -P scripts/tests/test_offline_ci.py ProtectedFileGuardTests > "$LOG" 2>&1`, recording exit before parsing. Parse `child_start` and `start` events as §5 specifies; fresh base must exhibit maintenance and live upload-pack traces; H must show zero maintenance children, zero `gc --auto` children, zero maintenance starts, positive upload-pack count and 11 successful class tests. Historical base count 264 is corroboration, not a fabricated new observation. The regression owns its separate trace; the external class trace covers the other fixture calls and its own assertion covers its one call.

**AC-F5 — Deterministic flip.** Make a second exported H tree R0 and remove only the exact two config call lines using `sed -i '/git("config", "maintenance.auto", "false")/d; /git("config", "gc.auto", "0")/d' "$R0/$F"`. Raw newline count must drop exactly 2; diff must contain only those removals. In R0 then unmodified T(H), execute the new method five times per Git using `python3 -B -P scripts/tests/test_offline_ci.py ProtectedFileGuardTests.test_fixture_repository_starts_no_auto_maintenance`. R0 must show the assertion failing for maintenance argv five times; a secondary cleanup error does not replace that required assertion evidence. H must exit 0 five times with no skip. Retain every invocation log.

**AC-F6 — Forced reproduction and removal.** For Git 2.55.0 only, use the forced environment in §5 and run the guard class three times on B and ten on H. B: at least one failure with Errno 39 through `run_guard` cleanup; also record any second-commit exit 128. H: ten successes, zero Errno 39, zero leftover fixture/trace directories under each dedicated TMPDIR. This is a bounded stress test, never a retry-until-green merge strategy.

**AC-F7 — Natural stress.** In the real clone at H, without forced config, run `python3 -B -P scripts/tests/test_offline_ci.py` 20 times with Git 2.55.0. All 20 must exit 0, report 39 tests and `OK (skipped=1)` on POSIX, with zero Errno 39 and no fixture leftovers. Preserve failures; do not discard early failures and report only later passes.

**AC-F8 — Full target file on both Gits.** In the real clone at H, run `python3 -B -P scripts/tests/test_offline_ci.py` once per selected Git. Expected exit 0, 39 tests, `OK (skipped=1)` on POSIX. The one skip must be the Windows-specific test. A Windows run's different skip count cannot substitute.

**AC-F9 — Core repository checks.** In the real clone at H, run the first four §5 baseline commands; each exits 0 with the same baseline summary as B. The offline-file command is AC-F8; fixture counting is AC-F3. Never run these repository checks in T(H). Additional full-tier CI steps and any UNRUN local steps are recorded by E with exact coverage; do not invoke reserved execution scripts to fill a gap.

**AC-F10 — Scope and DCO.** `git diff --quiet "$B...$H" -- .github/` exits 0, as do equivalent unchanged-file checks for the other scope-lock paths. Enumerate `git rev-list "$B..$H"`; for each commit inspect `git show -s --format=%B "$commit"` for its valid `Signed-off-by:` trailer. Report commit count and sign-off evidence per commit. Do not require a force-push merely to force count 1.

**AC-F11 — Published checks/logs bind to H.** Retrieve and retain:

```bash
gh api --paginate "repos/$R/commits/$H/check-runs?per_page=100" --jq '.check_runs[] | {id,name,status,conclusion,head_sha,details_url}'
gh api "repos/$R/commits/$H/status" --jq '{state,statuses}'
gh api "repos/$R/actions/runs/$RUN" --jq '{id,head_sha,event,status,conclusion,run_attempt}'
gh api --paginate "repos/$R/actions/runs/$RUN/jobs?per_page=100" --jq '.jobs[] | {id,name,status,conclusion,steps}'
gh api "repos/$R/actions/jobs/$GG_JOB/logs" > "$OUT/gg.log"
gh api "repos/$R/actions/jobs/$VS_JOB/logs" > "$OUT/vs.log"
awk '/Z Gate files touched:\r?$/{f=1;next} /Z This PR modifies the merge gate/{f=0} f' "$OUT/gg.log" | sed -E 's/^[^ ]+ +//; s/\r$//'
grep -nE 'Z (Ran [0-9]+ tests|OK \(skipped=[0-9]+\)|CHECK ci-tests: exit)' "$OUT/vs.log"
```

Resolve RUN from the check details URL/API and job IDs from the run's jobs list; verify mapping instead of assuming ID equivalence. The prior audit observed check-run ID=job ID, but that is historical. Log fetch failure is unavailable evidence, not an empty successful check. The anchored guard extractor must return exactly `scripts/tests/test_offline_ci.py`; the `Z` anchor avoids the echoed shell source. Validator log must show the added method passing, `Ran 39 tests`, `OK (skipped=1)`, and `CHECK ci-tests: exit 0` together in that step. Other suite summaries such as the historical `OK (skipped=5)` are identified by step, not mistaken for ci-tests coverage.

Expected job conclusions: `changes`/`validate-skills` success; `gate-guard` failure solely for the one protected path; `windows-offline-checks`/`tools-tests-linux`/`tools-tests-windows` skipped due to the successful path filter's `tools=false`/`offline=false`. Save the changes job log/output evidence too. Inspect every check and legacy status at H, not just required checks; any unexpected failing/cancelled/incomplete actual check stops progression. A queued external suite with zero check runs is recorded as such, not a green job. Use run-level completion/conclusions to resolve the documented job-status stale `in_progress` case; do not classify an otherwise complete successful run as pending solely from that stale field. An unexpected shape is investigated, never waived by the expected table.

**AC-F12 — Isolation.** Record `git status --porcelain` before/after in the actual implementation clone and any source checkout observed. Clean implementation candidate expected; pre-existing dirty source output is preserved byte-for-byte, not forced empty. Each H run's dedicated TMPDIR must be empty (`find "$TMPDIR" -mindepth 1 -print` on POSIX). Retained logs outside it are intentional. Preserve failing B fixtures as evidence; they are not H leftovers. Any cleanup later uses verified absolute scratch paths in one native shell.

### P-REG

**AC-R1 — Pure EOF append.** `git diff --numstat "$BR...$HR"` names REG only, zero deletions. Execute:

```bash
python3 -I -B - "$BR" "$HR" "$REG" <<'PY'
import subprocess, sys
b, h = [subprocess.check_output(['git', 'show', rev + ':' + sys.argv[3]]) for rev in sys.argv[1:3]]
ok = h.startswith(b) and len(h) > len(b) and b.endswith(b'\n') and h.endswith(b'\n')
print('byte_prefix=', h.startswith(b), 'base_newlines=', b.count(b'\n'), 'appended_newlines=', h[len(b):].count(b'\n'), 'both_end_newline=', b.endswith(b'\n') and h.endswith(b'\n'))
raise SystemExit(not ok)
PY
git diff -U0 "$BR" "$HR" -- "$REG" | grep '^@@'
```

Expected prefix True, exit0, and exactly one hunk whose prefix is `@@ -L,0 +L+1,n @@`, where L is the base blob's newline count and n the appended newline count; allow Git's trailing context after the second `@@`. No earlier byte may change. The three-dot numstat and direct BR/HR proof must refer to the same ancestor base; verify BR is the merge base first.

**AC-R2 — Unique next ID, excluding this PR.** Re-run at writing and at P-REG G. First count headings and duplicate IDs from current main and HR; zero duplicates. Enumerate open PRs using the actual P-REG number (before creation, PR=0 excludes none):

```bash
gh api --paginate "repos/$R/pulls?state=open&per_page=100" --jq ".[] | select(.number != $PR) | .number"
```

For each returned number n, in P-REG's isolated clone: `git fetch origin "pull/$n/head:refs/cifix/approval-collision/$n"`; read that ref's REG blob and extract `^### AEGIS-APR-[0-9]+:` headings. A failed fetch or missing/unreadable register requires investigation, not treating its maximum as zero. Let K be the maximum ID across main and those other PRs. N must equal K+1, and HR contains N exactly once as the appended grant. Main at writing has maximum119 and the coordinator observed zero open PRs, so N=120 is a candidate, never reserved permanently. A collision returns to the coordinator for allocation and renewed head-bound stages.

**AC-R3 — Original option intact.** In the extracted new entry e.md, `grep -cF -- "$GRANT_OPTION" e.md` returns 1 for the exact 255-character string in §7. Quotation stays on a single physical line.

**AC-R4 — Measured binding.** Extract e.md by its exact heading `### AEGIS-APR-$N:` through the next `### AEGIS-APR-` heading, or EOF, excluding the following heading. Compare H, `git rev-parse "$H^{tree}"`, B/`git merge-base "$B" "$H"`, sole path and `+a/−0` with fresh Git/API results. Each fixed value has `grep -cF` count ≥1 in e.md. Entry also gives actual check-run/workflow-run IDs, conclusions, and D audit comment URL; no prefilled future F comment.

**AC-R5 — Repository/docs checks.** In the real clone at HR: `python3 -B -P scripts/validate-skills.py`; `python3 -B -P scripts/tests/test_validator.py`; `python3 -B -P scripts/ci/check-markdown-links.py docs/approvals/APPROVAL_REGISTER.md`. All exit0; links report broken0/dead0. Link counts may increase. Read the rendered Markdown to confirm owner paragraphs remain legible and one-line source strings were not wrapped or typographically rewritten.

**AC-R6 — Published HR checks.** Reuse AC-F11's paginated check/status/run retrieval at HR. `changes`, `validate-skills`, `gate-guard` success; advisory three skipped by verified path scope. Any actual additional check must pass if applicable; record other status honestly. No guard exception for P-REG is authorized or expected.

**AC-R7 — Settled P-FIX state before P-REG merge.** P-REG G obtains the immutable Stage F comment ID F_COMMENT from F's handoff, not search results, and retains its exact body/time:

```bash
gh api "repos/$R/issues/comments/$F_COMMENT" --jq '{id,created_at,updated_at,body}'
gh api --paginate "repos/$R/pulls/$PF/reviews?per_page=100" --jq '.[] | {id,user:.user.login,commit_id,submitted_at,state,body}'
gh api --paginate "repos/$R/pulls/$PF/comments?per_page=100" --jq '.[] | {id,original_commit_id,created_at,updated_at,body}'
gh api --paginate "repos/$R/issues/$PF/comments?per_page=100" --jq '.[] | {id,created_at,updated_at,body}'
gh api "repos/$R/pulls/$PF" --jq '{head:.head.sha,body,updated_at}'
```

Read that identified F verdict's actual disposition line: it must be `SD-F: ACCEPT`, name H and the current bound-field hash, with author identity independent and no later superseding REVISE. A text search merely containing the token is invalid; the prior audit found that token inside a REVISE comment. Verify MG3 from exact-head automated result or an explicit unavailable-for-H notice; relate P0–P2 findings by `original_commit_id`, and retain each triage comment/commit and timestamp. An issue comment can be the unavailability record. No result for an earlier head and no silence substitutes. Recompute bound fields and confirm live head=H. Store verification UTC plus evidence IDs and timestamps. After merge, `gh api "repos/$R/pulls/$PR" --jq '{merged,merged_at,merge_commit_sha,head:.head.sha}'` proves P-REG merged; its `merged_at` must be later than the relevant F, automated result/unavailability, final triage and premerge verification times. Check HR is the candidate actually merged. The live observations are repeated immediately before the merge; re-check PF after it as well and use §8 if it moved.

**AC-R8 — Every owner source string present.** In e.md use `grep -cF -- "$text" e.md` once for each: the 588-character grant question and 255-character grant option from BRIEF; all six JSON question/description strings (the three `questions[*].question` fields and three chosen `options[0].description` fields); all four selected labels (the grant label plus the three JSON `options[0].label` values); and the OQ-C question, label, and description from the later BRIEF. Each count ≥1. Obtain strings by JSON parsing/the one-line brief source, not retyping or whitespace-normalizing them. Preserve UTF-8 punctuation. If a source string is absent or wrapped, repair the unmerged entry; no fallback assertion of equivalent meaning. **Explicit RC13(c) count correction, confirmed by the coordinator in this planning turn:** the audit's eight-row quotation table comprises two BRIEF strings plus six JSON question/description strings; they are not eight JSON strings. Including the three JSON labels gives nine selected JSON fields. This enumeration corrects that label without dropping coverage. Text matching proves transcription only, not owner authority; the complete question/selection/provenance provides that context.

## 7. P-REG draft — only measured fields remain to be filled

`N`, PF, H, T, B, a, audit URL and check IDs below are future measured values. Every owner quotation is already supplied verbatim on one physical line. The new entry is appended only after §8's P-REG Stage C gate. The date of grant is the owner's original date; any later recording date is recorded separately and never backdated.

```markdown
### AEGIS-APR-<N>: PR #<PF> one-time gate-guard exception for the Errno 39 test fix

- **Event:** GRANT — one-time, bound to one exact head. Not a standing exception or a policy decision.
- **Status at recording:** ACTIVE and unspent as recorded. Consumed by one merge of PR #<PF> at the exact head named below, and by nothing else. This entry cannot authorize the merge of the pull request recording it. Consumption will be recorded in the next register pull request, as the owner selected below.
- **Date / Grantor:** 2026-10-08 / Peter Nguyen. Recorded <actual recording date/time> by <recording agent>.
- **Reason:** [PR #<PF>](https://github.com/ModernNomad-98/Project-Aegis/pull/<PF>) addresses the intermittent `OSError: [Errno 39] Directory not empty` from `ProtectedFileGuardTests.run_guard` in runs 36695924676 and 37713171379. Its fixture repository started detached Git auto-maintenance while temporary-directory cleanup removed it. The head adds two local config calls, an explanatory comment, one standard-library import and one regression test. It changes only `scripts/tests/test_offline_ci.py`, a protected path. AEGIS-APR-047 excludes guard scripts and tests from its four-file standing exception.
- **Owner decision and proposal context:** In the Project Aegis session on 2026-10-08, the owner was asked:

  > main's CI failure was a rare race in one CI test: Git 2.55 starts a background clean-up job in a throwaway test folder, and the test deletes the folder while that job is still writing. The one re-run passed, so main is green again, and the same race has happened once before (2026-09-30). The proposed fix adds two lines to scripts/tests/test_offline_ci.py telling Git not to run that background job in the test's folder. scripts/ is protected, so a fix PR's protected-file guard (gate-guard) will be red until you grant a one-time exception for that exact PR commit. Do you want the fix?

  The owner selected "Yes, one-time exception (Recommended)", whose option text was:

  > A third PR touching only that test file, on a third branch, through all seven stages. It merges once gate-guard's red is covered by your one-time exception for that exact commit, recorded in the register, with every other check green. Admin merge allowed.

  The separate register-PR question was:

  > The exception has to name the fix PR's exact commit, which only exists once the fix is written. The last one-time exception (AEGIS-APR-106) handled this with a separate small PR that changes only the approval register, merged just before the protected PR. That's a fourth PR your instruction didn't name. May the team open and merge it on the same terms (all seven stages, all checks green, admin merge allowed)?

  The owner selected "Yes, same terms (Recommended)", whose option text was:

  > Follows the precedent. The fix PR stays one file, and the exception is in the register, approved and pinned to the exact commit, before the fix merges. About 30–45 extra minutes.

  The consumption question was:

  > After the fix merges, the register should record that the one-time exception has been used up. Should that be its own small PR right after the merge (the AEGIS-APR-107 precedent), or wait for the next register PR?

  The owner selected "Batch it later (Recommended)", whose option text was:

  > Recorded in the next register PR, which will also record FU-2's grant as used up. One PR instead of two, with no loss of safety, since a one-time exception for an exact commit can't be reused anyway.

  The changed-head question was:

  > Suppose the fix PR's commit changes after the exception is recorded, for example because a reviewer asks for a change. The recorded exception would then name the wrong commit. What should happen?

  The owner selected "Ask me again (Recommended)", whose option text was:

  > Matches the AEGIS-APR-032→034 precedent. Each exception stays tied to a commit you approved. Costs a short wait for your answer if it happens, which is unlikely because the fix is small.

  The later clarification question was:

  > For the CI test fix, your answer says the exception must be "recorded in the register". I read that as: the register entry has to be merged on main (not just written in an open PR) before the fix can merge. Is that right?

  The owner selected "Yes, merged on main (Recommended)", whose option text was:

  > The safest reading. The register on main is what the repo treats as authority, so the exception only counts once that small register PR has merged.

  These are transcriptions of the owner's selections and the questions/options shown to the owner, relayed by the previous coordinating agent. They are not quotations of the owner typing the option prose into the register. The register preamble accepts current direct owner instructions before transcription. Recording does not create or enlarge authority.
- **Scope allowed:** One `gate-guard` exception and administrator merge of PR #<PF> at exact head `<H>` (tree `<T>`, base `<B>`), changing only `scripts/tests/test_offline_ci.py`, `+<a>/−0`. The real size includes the two config calls plus comment, import and regression test. At H, gate-guard check run <GG_CHECK> / workflow run <RUN> concluded FAILURE, and its job <GG_JOB> log named exactly that path under `Gate files touched:`. Changes and validate-skills concluded SUCCESS; windows-offline-checks, tools-tests-linux and tools-tests-windows were skipped by the verified path filter. The failure is recorded as **failed with an authorized disposition**, never green or waived. The owner requires every other applicable check green and all seven stages; skipped checks are recorded as skipped under the coordinator's procedural reading, not as passed.
- **Scope FORBIDDEN:** No other PR, head, path or failed check is covered by "only that test file", "for that exact commit", and "every other check green". This is one-time; it does not widen AEGIS-APR-047 or change any workflow, protected-path pattern, branch protection or repository setting. A moved head after this entry merges on main leaves this grant spendable on nothing. A replacement needs the owner's fresh answer to a question naming the replacement 40-character head, following the recorded Q4 choice.
- **Evidence:** Owner selection timestamps are preserved in `owner-askuserquestion-answers.md` at handoff commit `32f5ae25780c4802184a63d4063507fcf31b3a37`: grant `2026-10-08T15:26:38.922Z`; Q2–Q4 `2026-10-08T16:01:08.352Z`; later clarification `2026-10-08T17:51:48.809Z`. The coordinator's BRIEF relays the grant at 15:28:53Z, the full one-line question/option at 16:10:40Z, Q2–Q4 at 16:01:16Z, and the clarification at 17:52:07Z. The Q2–Q4 JSON is a session artifact, extracted programmatically from the session transcript's own AskUserQuestion call, SHA-256 `74c8cd5a559b1398fe411d6d75f4da1be23fe788b0845cdb59dcfb09bc82f1c2`; its extraction timestamp is not supplied. It is archived at `docs/evidence/session-handoff-2026-10-08/artifacts/cifix/owner-q2-q4-verbatim.json` in that unmerged handoff commit. BRIEF SHA-256 is `682eb1cf401efda27a51c59ca006fa97812df13a259664ccd227653f13f37364`. These are archival transcriptions, not independently authenticated owner signatures or new policy from the snapshot. BRIEF's 16:20:07Z coordinator record says the owner was told about 28 added lines; this is disclosure, not owner approval of size, and authority remains the selected file scope. The [Stage D audit](<actual comment URL>) at H and the [gate-guard job log](<actual job URL>) independently support the head, single path, and protected-path failure; they do not prove the owner's question or selections. Head/tree/base/numstat/check facts above were remeasured for this entry from Git and GitHub, not copied from the plan.
- **Expiry / use limit:** One use, one merge of PR #<PF> at H. No calendar expiry was stated. A later event records consumption or observed expiry without rewriting this entry.
```

P-REG Stage C may convert the archive path references into immutable `blob/S/...` links for retrievability, and must fill all measured placeholders before D. Preserve source text exactly and leave older merged entries byte-unchanged. P-FIX's Stage F link is deliberately not an entry dependency: F acceptance is checked at P-REG merge, not cited as if it existed at P-REG C.

## 8. Sequencing, exact-head exception and head movement

**Binding owner scrutiny rule**, direct owner text in `owner-messages.md` at `2026-10-08T16:23:20.186Z`, relayed in BRIEF at `17:10:06Z`:

> always audit and scrutinize your recommendations. Do not make any assumptions on your recommendation, if you are unsure, look for evidence or research it first.

The standing seven-stage sequence, distinct holders, SD-A–SD-G and MG1–MG5 remain unchanged. The parent coordinates and assigns; it does not perform implementation, audits, review or merging. Every stage has one holder; a supposedly dead lane is confirmed stopped before reassignment. No agent holds two stages of either change. A shared A plan and B plan-audit may explicitly cover both PRs; C–G still run separately for each.

Additional preserved separation: P-REG C is neither P-FIX C nor P-FIX G; **P-FIX G holds no stage of P-REG**, including its shared A/B. Prefer P-REG D/F holders who did not author the cited P-FIX D audit, so they are not reviewing their own evidence record. This last preference is a recommendation, not a new owner prohibition.

### 8.1 Concrete stage order

1. **A → independent B.** B captures this file's SHA-256 and returns SD-B ACCEPT/REVISE explicitly for both P-FIX/P-REG scope. This planner cannot hold B. A revision after B voids its acceptance until re-audited.
2. **P-FIX C.** Starts only after accepted plan. Reads main and scope; creates a clean isolated clone/branch; measures B; implements §3–§4; produces AC-F1–F10/F12 evidence, H/tree/B, size disclosure, exact-file signed commit(s), and opens P-FIX under its stage authorization. No unapproved reserved local execution. The branch head is recorded after publication. SD-C COMPLETE requires immutable H/tree/B; unsupported claims or unresolved required bug-fix proof keep C incomplete.
3. **P-FIX D.** A different agent checks each F criterion MET/NOT MET/UNRUN, including test liveness and flip behavior and unchanged guard. AC-F11 may remain UNRUN only under §2's declaration. D posts an exact-head ACCEPT or REVISE, with comment ID and evidence. Its result is not Stage F.
4. **P-FIX E → F.** E runs authorized checks at H and inventories every locally UNRUN full-tier step, its reason and named CI coverage or resolution. P-FIX's expected gate-guard failure remains failure with the granted disposition pending P-REG; it is never passed. E posts the applicable SD-E token under the canonical rule, not a bare INCOMPLETE. F starts only after an affirmative E disposition, reviews H and the actual evidence, accepts the UNRUN record where required, and posts SD-F with exact H and current bound-field hash. F does not merge.
5. **P-REG C may overlap P-FIX E/F, but only after both P-FIX SD-D ACCEPT at H and AC-F11's completed, explained check set.** C independently rechecks H, D comment and CI, resolves any size discrepancy, allocates N by AC-R2 and writes the fillable §7 entry with no F placeholder. P-REG branches independently from current main; if main has unexpected new changes, return to the coordinator before writing. It runs AC-R1–R5/R8 and publishes HR/tree/BR with exact-file sign-off.
6. **P-REG D → E → F.** Different holders audit all R criteria, validate HR and review HR. R6 is prepublication-unavailable; R7's eventual merge timing is declared UNRUN at D with its §2 reason and mandatory G resolution. P-REG D reviews the entry's quoting, source attribution, full-history grant interpretation, exact values and byte-prefix proof. E records its checks/UNRUN list. F checks the entry and PR bound fields, posts exact HR and hash. Each stage must meet the canonical predecessor rule.
7. **P-REG G waits for settled P-FIX F and MG3 at the same H.** Satisfy AC-R7; re-run AC-R2; rederive P-REG's own MG1–MG5, including automated review/triage on HR, all applicable checks green, bound fields and Q2 authority. Merge pinned to HR only. If the register's base or ID changes before merge, C revises the unmerged append in its own clone, then renewed D/E/F at the new HR; do not silently reuse old verdicts. Re-check P-FIX H after P-REG lands.
8. **P-FIX G runs only once the exception entry is merged on main.** The owner expressly confirmed this in OQ-C. It refreshes main/read-only evidence, reads the entire register history for N and the actual entry, verifies active exact H scope and unused status, rederives MG1–MG5, AC-F11, F comment/hash and MG3 triage, and performs the main-change scope check below. Merge is pinned to H. It posts a receipt keyed to MG IDs plus §9's facts; observes the merge-commit push CI through completion and reports honest outcome/remaining gaps.

P-REG is the separately authorized vehicle because a commit cannot include its own final SHA and P-FIX may touch only the test file. APR-106's statement “The PR cannot create that entry for itself” is a quotation of PR #661's Stage D audit, not a general owner grant. APR-106/107 are consumed historical examples, not CIFIX authority. APR-105's text says “Once merged, any further change to it is an append”; the different phrase “the append-only rule governs merged entries” is attributed only to #663's PR body in the historical audit.

**Self-scrutiny (vehicle/timing):** a second seven-stage PR adds work for a tiny fix. Q2 explicitly chooses that vehicle and its terms, and OQ-C explicitly requires its main merge. Avoid deadlock by citing D/CI in the entry and using F/MG3 as merge preconditions. A contrary later owner instruction or actual dependency cycle would change the sequence and require re-audit, not a silent bypass.

### 8.2 Exact-head merge mechanism and main advancement

At P-FIX G, let B remain its original recorded base, and M2 be refreshed main after P-REG lands. Execute `git diff --name-only "$B" origin/main`. Every changed path other than `docs/approvals/APPROVAL_REGISTER.md` must avoid the scope-lock set: `scripts/tests/test_offline_ci.py`, `.github/workflows/`, `scripts/ci/record-check.py`, `scripts/validate-skills.py`. Any intersection stops merge and returns to Stage A. Review other main changes for conflicts and full register lifecycle impact; do not assume unrelated means harmless. Confirm mergeability and record M2; recheck live main before the call to catch intervening movement.

**Never update, rebase, or merge main into P-FIX after P-REG merges.** That changes H and triggers Q4. A behind-main head is intentional in this sequence. Historical corroboration in PLAN-AUDIT-rev2: #661's bound head was three commits behind #663's register merge, then admin-squashed onto that main. That comparison has not been fetched anew here; APR-107 on M confirms the distinct reviewed head and squash commit and the head pin. Do not claim history guarantees present mergeability.

Choose an available **pinned** merge mechanism after its current schema/help is inspected:

- REST `PUT /repos/ModernNomad-98/Project-Aegis/pulls/<PF>/merge` with structured request `sha=H` and an explicitly chosen `merge_method`. [GitHub's REST merge documentation](https://docs.github.com/en/rest/pulls/pulls#merge-a-pull-request), read in this planning turn, specifies a head match and HTTP409 for a supplied SHA mismatch. The merge holder records request method, exact pin, response, and subsequent PR state.
- An available MCP `merge_pull_request` with `expectedHeadSha=H`, only after verifying that exact argument's current semantics. The RCF-1 receipt's historical `expectedHeadSha` is MCP evidence, not REST `sha` evidence. No MCP merge call or current schema verification was performed by this planner.

The prior session reported GraphQL `HTTP 403: GitHub GraphQL is not available from Claude Code sessions`; this is historical environment evidence and does not establish current Codex tool access. The previous audit also read branch protection with required `gate-guard`/`validate-skills`, `enforcement_level: non_admins`, and rulesets `[]`. Its inference of an admin REST/MCP bypass is **unverified in this session**, and that historical field interpretation is not proof of permission. APR-107 and #661's receipt corroborate a past pinned CLI administrator merge through failed gate-guard. Before any attempt, G retrieves current protection/rules/actor capability read-only and resolves unknowns with the coordinator; it never modifies them. No dry-run write is permitted to test authority.

**Fail closed:** if a pinned merge is refused for any reason, report SD-G NOT MERGED and return it to the coordinator. Never retry unpinned, weaken settings, arm auto-merge, or update the branch to get past refusal. If the response is ambiguous/connection lost, first read PR state to determine whether it merged; do not retry or spend the grant twice. A later authorized retry requires fresh exact-head gates and the same valid grant conditions.

**Self-scrutiny (mechanism):** REST may not bypass a failing required guard under current settings/actor permissions; MCP may be unavailable. The plan deliberately labels that ability unknown and leaves a refusal as a stop. Current documented tool semantics and read-only capability evidence can determine the mechanism; only the actual authorized pinned call proves that merge path succeeds. Neither a prior success nor an expired grant is authority to change protections.

### 8.3 Head movement and lifecycle events

- **Before P-REG merges:** under the now explicit OQ-C answer, the exception is not yet recorded on main. Coordinator routes P-FIX revisions back through C/D/E/F and fresh checks/MG3. P-REG C may rebuild its still-unmerged entry for H2 in place; every HR-bound verdict is void and retaken. P-REG C entry and G prerequisites repeat for H2. This does not rewrite a merged grant or authorize scope expansion. If the changed fix no longer fits the original option, halt for a new owner decision.
- **After P-REG merges:** if P-FIX moves from H to H2, its original N grant is spendable on nothing. P-FIX stays unmerged. Coordinator asks for **a fresh owner answer to a question that names H2's full 40-character head**, complete new diff/scope/check context and the one-time exception requested. The answer need not itself contain the SHA: APR-034 records “parooved” answering the immediately preceding message that named the head.
- Append an EXPIRED event targeting N for the observed unused head move, with effective movement time, recorded time, evidence, and no new authority, whether the owner approves a replacement, declines, or does not answer. APR-033 records this as a factual agent event. Timing/vehicle for that expiry is a coordinator decision within applicable recording authority, or an owner question if uncovered. **Q3 decides consumption timing only and must not be stretched to decide expiry timing.** This plan does not silently initiate an extra lifecycle PR.
- A replacement GRANT may be appended only after the fresh answer, with a fresh unique ID, complete question/reply provenance and H2 binding. Its register-only vehicle must have authority and run all seven stages; when the scope remains this authorized repair and Q2 vehicle, use those terms, and if it differs route to the owner. No agent rebinds N itself, revives N, or edits its merged bytes.

**Self-scrutiny (head move):** rebuilding an unmerged entry without another question could have been ambiguous before OQ-C. The owner's later explicit main-merge answer resolves that timing. A later owner instruction changing that boundary, uncertainty whether N already merged, or an unknown prior use forces a stop. Recording EXPIRED documents a fact and is not a substitute for the new head's approval.

## 9. Consumption, receipt and completion

There is no P-CONS task in CIFIX-1. The owner selected **Batch it later**: append N's CONSUMED event in the next register PR together with FU-2's APR-119 consumption. Recheck whether that later recording already occurred before adding it. Its entry ID is allocated then; no expected 121 or automatic extra PR is created here. APR-119's old ACTIVE wording does not make its one-use grant reusable; the snapshot reports its use by #679, and any executing recorder must verify that delivery fact anew.

P-FIX G's receipt must leave: PF; H/tree/B; N and main commit containing its entry; final F comment ID/hash; MG3 result/unavailability and finding dispositions; all check names/IDs/conclusions; Stage E UNRUN list; UTC merge time; merge method; full resulting merge SHA; pinned request mechanism/value and response; `git merge-base --is-ancestor "$H" "$MERGE"` exit and interpretation; post-merge push-run ID/head/result. Ancestry is measured, not assumed: a squash normally has a different non-descendant merge object while a merge commit preserves ancestry. The exception binds the act of merging the reviewed H, not a claim that the resulting main SHA equals H.

Record gate-guard as **failed with an authorized disposition (AEGIS-APR-N)**. Use the canonical MG-keyed status/pointer receipt without creating a new normative policy. A post-merge push normally selects all advisory jobs and skips the PR-only guard; observe actual results. If red, the owner's “diagnose and fix … try to merge again” instruction routes new code through its stages/authority; it does not authorize rerun-until-green, an unrelated repair or reserved execution. The record is incomplete until outstanding evidence and required follow-up are stated.

**Self-scrutiny:** delayed consumption transcription can mislead a reader skimming ACTIVE. The preamble's one-use rule and an exact merge receipt prevent reuse, and Q3 expressly selected batching. An ambiguous merge outcome or another attempted use would require immediate reconciliation; do not assume batching resolves uncertainty.

## 10. PR descriptions and per-stage evidence

Both use the current `.github/pull_request_template.md`. Keep all six whole-line sentinels; `## Reconciliation witness` has eight rows. Sites 1–5/8 use unchanged diff evidence for `docs/delivery-workflow.md`; site6 for `AGENTS.md`; site7 records the PR-body witness/skills/divergence state. No new governance rule is authored. State applicability of the divergence table honestly rather than inventing a rule change.

Each stage holder writes its own four-column skills row; nobody invents another agent's usage. Supply immutable accepted plan hash, exact head/tree/base, actual acceptance results and linked evidence. P-FIX security answer is Yes: protected `scripts/` test; P-REG is Yes: owner approval register. MG5 applies only to outside contributions, so these owner-assigned maintainer/agent PRs use its not-applicable scope clause if that provenance remains true. If contribution provenance changes, re-evaluate MG5 instead of assuming exemption.

F and G compute the canonical bound-field hash using whole-line sentinels, witness→skills→security order, whitespace-collapse/trim each payload, join with newline, UTF-8 SHA-256 first16. Missing/ambiguous sentinel pairs are errors, not empty fields. A change to a bound field voids F even without a head move and requires a new F verdict. G records its own skill use in the receipt; do not edit the bound table afterward and reuse F. Adding the real P-REG number/N in P-FIX “What & why” outside the bound fields does not alone change their hash; verify it really is outside before editing. Never add a file merely to carry stage rows or repair a body.

Stage D resolves every applicable criterion separately. Any new UNRUN criterion not declared at A forces REVISE under SD-D. Any true NOT MET is not carried as accepted. E uses PASS, INCOMPLETE — UNRUN LISTED, or FAIL according to the canonical SD-E definition; unavailable is never pass. F must explicitly accept the E unrun list when required, and G carries it. Stage-handoff blocks name retained decisions, files changed/not touched, actual commands/results, deviations and the next holder's entry evidence.

## 11. Estimates and recommendation scrutiny

These are **unverified estimates**, not delivery commitments or grounds for bypassing a gate. Active time is unmeasured in the historical session. The prior audit records round1 B wall time `15:52:33–16:07:03 UTC` (14m30s); round2 B `17:11:40–17:36:54 UTC` (25m14s). These are reported historical wall measurements and weak calibration for a new host/environment.

| Item | Unverified estimate | Basis and limits |
| --- | --- | --- |
| This Stage A | 25–40 active minutes, announced by coordinator | No measured active-time calibration; final wall time is only an imperfect comparison. |
| Independent B of rev3 | 15–30 active minutes | Historical B wall times above; different scope and missing harness artifacts limit comparison. |
| P-FIX C | 20–45 active minutes after environment ready | No measured same-host basis; runtime provisioning/recovery excluded and unknown. |
| P-FIX D, E, F | 20–35 active minutes each | No measured same-host basis. Avoid duplicated optional stress runs once the required independent evidence suffices; no gate is omitted. |
| CI at H/HR | Unknown | Neither head exists; queue/runner duration unverified. |
| P-REG C–F | Unknown; owner's option quoted “About 30–45 extra minutes” | That phrase is proposal text, not a measured or current estimate. Overlap follows gates, not predicted duration. |
| Each G including evidence | 10–25 active minutes plus CI/waits, unverified | No measured same-host basis; API availability/protection unknown. |

**Self-scrutiny:** the earlier plan underestimated audit iteration and assumed reusable scratch assets. The numeric ranges carry little predictive evidence; use measured start/finish times per assigned item to revise them. Environment readiness, audit findings or owner head-change decisions can dominate wall time. No unproven ETA is used to recommend merging earlier or running stages out of order.

## 12. Required-change preservation and open state

| Required change | Rev3 treatment |
| --- | --- |
| RC1 Q2 authority / current inputs | §§1,7,8: actual snapshot hashes, complete Q2, P-REG own authority and chain; supporting APRs not sole authority. |
| RC2 consumption / no P-CONS | §9: owner-selected batching, full receipt, no preallocated consumption ID. |
| RC3 moved head / recorded boundary | §8.3: explicit before/after main merge; OQ-C owner answer closes the old interpretation question. |
| RC4 P-REG C entry / no future F link | §§7,8.1: D ACCEPT + completed H checks; entry cites D/log; F checked at merge. |
| RC5 register merge after F/MG3 | AC-R7 and §8.1 with specific comment IDs, timestamps and head recheck. |
| RC6 source fidelity / proposal context | §7 has full question/options/labels; R3/R8 check exact strings and provenance. |
| RC7 append-only proof | AC-R1 byte prefix, one EOF hunk, raw newline and no deletions. |
| RC8 separation | §8: distinct stages, P-REG C independence, P-FIX G no P-REG stage. |
| RC9 fresh base / correct attribution | §1 current pin, actual bytes/counts, relayed live evidence; §8.1 correct APR-105/#663/Stage-D attribution. |
| RC10 concrete checks | F3 count recipe, F5 two-line flip, F12 dirty-root preservation, R2 enumerated PRs, R4 measured binding. |
| RC11 refreshed brief / OQ-A/B/C | §1 actual BRIEF including later OQ-C; §4 disclosure/size guard; §7 closed owner texts. Historical 31dec83b not mislabeled current. |
| RC12 fillable exact entry | §7 no owner-text placeholder; one-line labels; JSON hash/untimed extraction; disclosure and D/log evidence attribution correct. |
| RC13 runnable checks | R2 excludes itself; R7 uses identified verdicts; R8 corrects the source count explicitly with coordinator confirmation; F11 log commands; F9/§5 clone requirement. |
| RC14 mechanism / no update / fail closed | §8.2: official REST evidence, historical GraphQL/protection labelled, MCP pin distinct, refusal stop, behind-main preservation and scope-lock check. |
| RC15 exact Q4 / decline branch | §8.3: reply to SHA-naming question, factual EXPIRED with/without regrant, Q3 not extended to expiry. |
| RC16 scrutiny / estimates | §§3,4,8,9,11 provide strongest counterargument and evidence that would change each recommendation; ETA basis explicitly unverified. |

OQ-A is closed by the saved JSON; OQ-B by the coordinator's disclosure record only; OQ-C by the owner's later explicit choice. No new owner question is needed to audit this plan. Remaining execution unknowns are POSIX/Git runtime availability, current branch-protection/rules/actor capability, future H/HR/PR IDs/checks/reviews/mergeability, any main drift, and whether a later consumption-record PR already exists when that task is picked up. None is filled from old reports.

**Stage A handoff:** SD-A COMPLETE on the exact file hash reported alongside this artifact. SD-A–SD-G/MG1–MG5 and existing grants remain unchanged. Changes: this scratch plan only. Intentionally not done: implementation, prototype/harness execution, repository validation, independent plan audit, PR creation/commenting, commits, push, merge, settings changes, reserved execution and new skill builds. Text/AST/hash/ref reads listed in §1 are planning observations only. The initial historical-hash discrepancy and RC13 count clarification are disclosed above; no rule or owner scope was silently changed.

**Continuation:** coordinator gives the captured bytes/hash and both pins to an independent Stage B holder, including RC11–RC16 and the later OQ-C quote. The auditor must independently decide ACCEPT/REVISE; this plan's author supplies no audit verdict and holds no subsequent stage. Stage C waits for B's affirmative captured-revision verdict and any concrete environment/scope gaps to be resolved under the declared gates.
