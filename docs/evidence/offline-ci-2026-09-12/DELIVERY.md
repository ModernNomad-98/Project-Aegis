# Offline CI delivery — 2026-09-12

## 1. Summary

[PR #91](https://github.com/ModernNomad-98/Project-Aegis/pull/91) merged as
`0e95b29118fc27087ebaec2c5c9854a14d0cbeed` after the owner's explicit approval.
Its tree `05924592c4f297749822a286268e8795eb064580` matches the tested PR head
`69915fec415cddfce608eed7fd4f989d226af903`. Both verification jobs passed in
[main run 34677278437](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/34677278437).
The protected-file guard is PR-only and was correctly skipped on main.

The authorized PR #88 calibration-control engineering, PR #90 shared-contract
repairs, and PR #91 permanent offline CI are delivered. Their main verification
runs passed. The owner's subsequent standing administrator-merge instruction is
preserved as [AEGIS-APR-002](../../approvals/APPROVAL_REGISTER.md#aegis-apr-002-administrator-merges).

## 2. Intentionally not done / omitted

None from the authorized engineering delivery. Measured calibration, replacement
approved inputs, human labels, OD-1 and WP-2B-4 are separate, still-open work in
the [durable backlog](../../roadmaps/behavioral-eval-runner-backlog.md).

## 3. Files touched

The [PR #91 diff](https://github.com/ModernNomad-98/Project-Aegis/pull/91/files)
contains the complete file list. Principal changes:

- `.github/workflows/validate-skills.yml`, `.github/dependabot.yml`, `requirements-ci.txt`
- `scripts/ci/record-check.py`, `scripts/ci/check-environment.py`, `scripts/tests/test_offline_ci.py`
- `scripts/acceptance/Test-ScenarioAEvidence.ps1`
- `docs/offline-ci.md`, `CONTRIBUTING.md`, the backlog/audit checkpoints, and this evidence directory

The subsequent approval-record update adds `docs/approvals/APPROVAL_REGISTER.md`,
its source-library-only `AGENTS.md` pointer, and this delivery checkpoint.

## 4. Tests & validation run

The [hosted record](HOSTED.md) links the raw logs and observed counts.

| Command/check | Observed result |
| --- | --- |
| `python -m unittest discover -s tools/behavioral_eval_runner/tests -p 'test_*.py' -v` | 987 tests on each hosted OS; PASS, 5 Linux / 6 Windows capability skips |
| `Test-ScenarioAEvidence.ps1` | Linux Core 106, Windows Desktop 113, Windows Core 113; all PASS |
| Validator / contract-audit self-tests / BER self-check | PASS on both hosts; exact counts in HOSTED.md |
| CI helper/guard tests / DCO / actionlint | PASS |
| Main Actions run after merge | Both verification jobs SUCCESS; PR-only guard SKIPPED |
| Approval-record startup update: `python scripts/tests/test_validator.py` and `python scripts/validate-skills.py` | 91 assertions; 184 valid skills, 0 warnings; PASS |

The initial hosted Desktop run failed because: "The term 'Get-FileHash' is not
recognized as the name of a cmdlet, function, script file, or operable program."
The native Desktop shell correction resolved the inherited Core module-path
problem; the original acceptance checks then passed. The failed diagnostic log
is retained alongside successful evidence.

## 5. Evidence

- [Final PR run 34675774312](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/34675774312)
- [Post-merge main run 34677278437](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/34677278437)
- [Retained evidence hashes](SHA256SUMS.json): all 64 files independently verified against committed blobs
- [Hosted diagnosis and correction](HOSTED.md)
- [Owner approval register](../../approvals/APPROVAL_REGISTER.md)

## 6. Risks & known gaps

Observed host capability skips remain explicit. Offline tests do not establish
measured model calibration or sealed-holdout results. Windows is visible CI
coverage but is not a newly required branch-protection context; delivery waits
for it. GitHub branch settings were not changed.

## 7. Skipped validation

Local PowerShell Core was unavailable; hosted Linux and Windows Core runs covered
it before merge. Platform/capability-specific skipped cases are retained in raw
BER logs. No expected verification job was skipped for delivery.

## 8. Next actions / handoff

Continue from the durable backlog's approved-input and measured-calibration
requirements when that work is authorized. Future administrator merges in this
project use the owner's standing AEGIS-APR-002 grant without repeating the same
permission question; check later lifecycle events and the active task's scope.
