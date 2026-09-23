# Hosted verification and Windows shell correction

> **Current reading, checked 2026-09-23:** This page records a specific
> pre-merge pull request (PR) #91 hosted run. Its overall protected-file guard
> failure and the then-unmerged status remain accurate for that run. PR #91
> later merged, and the [delivery record](DELIVERY.md) records passing
> main-branch checks. For current offline continuous integration (CI)
> commands and limits, use the [CI guide](../../offline-ci.md). Do not treat
> the earlier failed workflow as today's delivery status or erase its evidence.

[PR #91](https://github.com/ModernNomad-98/Project-Aegis/pull/91) implementation
`0444f46a459150b9fb2aeae168dc5d03b8135b96` passed both verification jobs in
[run 34675606660](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/34675606660).
The synthetic PR merge checkout was `67e3503dc3c0daf7d534c3530f3aa711176a0aac`.
All 19 recorded commands exited 0 and reported a clean checkout; DCO also passed.
The workflow's overall result is failure solely because `gate-guard` intentionally
requires manual review/merge for these enforcement changes. This checkpoint does
not claim that PR #91 is merged or that the required GitHub approval exists.

| Observed hosted check | Ubuntu | Windows |
| --- | --- | --- |
| Python / SDK | 3.14.7 / 3.0.0; precheck passed | 3.14.7 / 3.0.0; precheck passed |
| CI helper/guard tests | 8, no skips; PASS | 8, 4 Linux-only skips; PASS |
| Validator / skill validation | 91 assertions; 184 valid, 0 warnings | 91 assertions; 184 valid, 0 warnings |
| Contract-audit self-tests | 69 assertions; PASS | 70 assertions; PASS |
| BER self-check | 21 checks; PASS | 21 checks; PASS |
| Full BER suite | 987 tests, 5 skips; PASS | 987 tests, 6 skips; PASS |
| PowerShell Core acceptance | 106 checks; PASS | 113 checks; PASS |
| PowerShell Desktop 5.1 acceptance | Not applicable | 113 checks; PASS |

Both hosts executed the SDK-dependent cases. Actual capability records and skip
reasons remain in the raw artifacts: notably, the existing atomic-evidence-write
capability probe is false on both hosts, while POSIX no-follow materialization is
available on Ubuntu. Those branches are not reported as executed. Windows also
reported no distinct 8.3 alias on its temporary volume. This records the existing
capability limits; the CI change does not alter runtime containment guarantees.

## Failure, diagnosis and correction

The [initial run at e33df08](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/34675256416)
passed Linux and both full BER suites, but Desktop acceptance reported 109 passing
and 4 failing checks. The failed child replay preserved its work directory by
design. The assertions discarded child output, hiding the actual cause.

Commit `6d9d6dc` added child output to the three unexpected replay assertions,
without changing their conditions. Its
[diagnostic run](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/34675434033)
reproduced the failures and exposed `Get-FileHash` command discovery failure.
The recorded failing log and metadata are retained in `failure-34675434033/`.

The Desktop command ran through a Python recorder launched by the job's default
Core shell. Microsoft documents that this intermediate process inherits Core's
module paths, which can prevent Desktop from loading its Utility module. Commit
`0444f46` sets `shell: powershell` on that one Desktop step. The unchanged replay
and hashing code then passed all 113 checks; Core also passed all 113 Windows
checks. See the [module-path explanation](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_psmodulepath#starting-windows-powershell-from-powershell-7).

## Review and retained evidence

The automatic GitHub review completed at `e33df08` with no findings. Independent
read-only review approved the subsequent diagnostics and shell correction at
`0444f46`; it found no actionable issues. These are engineering review results,
not a GitHub `APPROVED` review or permission to bypass branch protection.

`hosted-34675606660/` contains both platforms' raw logs and command metadata,
run/job records, a summary, and the intentional guard failure log. The root
`SHA256SUMS.json` covers all 64 retained local, failure and hosted evidence files.
Later commits that only retain these documents/evidence do not change the tested
implementation. Their hosted check results are also visible on PR #91.

No measured calibration, approved inputs/labels, OD-1 or WP-2B-4 gate is closed by
these offline results. Final delivery still requires merge and a successful main
verification run.
