# Permanent offline CI — prepared follow-up

> Historical prepared plan. This work shipped in
> [PR #91](../offline-ci-2026-09-12/DELIVERY.md), including the Windows native-shell
> correction and successful main verification. Use the
> [current CI guide](../../offline-ci.md) for commands and coverage. Original
> proposals and estimates below are retained for provenance.

Scope already authorized in the audited plan; implementation/merge follows shared
contracts. Estimate: 2–4 active hours plus required external review/merge waits.
Prepared using Aegis qa-automation-architect against the current repository checks.

Keep unittest, the validator/audit self-tests and the existing Scenario A PowerShell
acceptance harness. A new runner or browser/database suite adds no coverage needed
for this source library. Tests retain isolated synthetic temporary repositories,
fake provider transports and zero real credentials/provider calls.

Proposed change to the existing protected workflow:

- Preserve the required `validate-skills` and `gate-guard` job names and the guard's
  protected paths. Add contract-audit tests, runner self-check and BER tests inside
  the existing required Linux validation job, so those failures gate normal merge
  without changing branch-protection settings.
- Add a Windows verification job for BER and Scenario A acceptance under both
  `powershell` (Desktop 5.1) and `pwsh` (Core). This additional job is initially
  advisory under the current two required check names; root's closeout must wait
  for it as well. Do not claim it is a registered required check.
- Run Scenario A under Linux `pwsh` as well, so its POSIX symlink cases execute.
  Keep matrix fail-fast disabled so all platform evidence completes.
- Reuse the repository's pinned checkout/setup-python actions and Python 3.14.
  Install pinned PyYAML from requirements.txt and the already authorized pinned
  OpenAI SDK 3.0.0 for its mocked configuration cases; install steps may fetch
  packages, test execution must not call a provider. Record actual dependency
  versions and all platform/dependency skips. Consider a dedicated CI requirements
  file rather than adding the optional SDK to the validator runtime dependency.
- Require an SDK import/version precheck before mocked SDK tests; an import-error
  skip must not silently remove the intended configuration coverage. Record the
  tested commit, Python and shell versions and set PYTHONDONTWRITEBYTECODE=1.
- Keep one Python command per PowerShell step, or check LASTEXITCODE immediately
  after each native command, so a later success cannot hide an earlier failure.
- Run on PRs targeting main and pushes to main. Avoid path filters that could
  leave required checks pending. Main runs detect regressions after merge.
- No retries or silent quarantine. Failures retain native logs and exact commit;
  investigate and repair them before merge. Existing local evidence is not a
  substitute for the hosted result. Use job timeouts (Linux 15 minutes, Windows
  20 minutes) and preserve failure artifacts with bounded retention if adding
  an upload action; pin any new action to a verified commit.
- Review the protected set under D60 as the enforced surface grows: BER tests,
  self-check, contract-audit code, acceptance checks and CI dependencies can now
  affect a gate. Account for these explicitly while preserving existing paths;
  do not add new enforcement that can silently disarm itself through an unguarded
  change. Preserve branch-protection settings.

GitHub documents the explicit Desktop/Core shell selectors and native exit-code
handling in its [workflow syntax reference](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idstepsshell).

Verification: parse the YAML without YAML-1.1 `on` coercion, review trigger/job/
permissions/timeout/gate semantics, run the exact commands locally, publish the
separately reviewed workflow PR, inspect every hosted job, fix failures and rerun.
The workflow change intentionally trips gate-guard and needs the explicit manual
merge route for its concrete revision; PR #88's administrator authorization does
not carry forward automatically.
