# Behavioral Eval Runner: resume on a new computer

Checkpoint: 2026-09-11. The old computer is lost. GitHub is the project's
continuation and backup location, as clarified by the owner. A separate copy of
the locally generated recovery ZIP is optional; it is not a prerequisite for
continuing. The owner states that this project contains no secret or personal
data. Read-only Project Aegis agents have standing owner approval.

## Current work and evidence

The implementation branch is `review/ber-phase01-corrections`. Three reviewed
source commits were pushed and verified at
`8f92e916f86bc0b9df618fb6a7887bd531df8fea`, tree
`499e7e96bd524fe024aec94ed69d11a17f783e13`:

- `40bfabc`: calibration execution boundaries.
- `c6822e1`: telemetry accounting and request deadlines.
- `8f92e91`: incomplete-response reason retained after a deadline.

The [independent review](phase01-independent-final-review.md) approved that exact
source revision. [Windows](windows-suite.log) and [POSIX](posix-suite.log) full
suites passed 961 tests at `c6822e1`, with 13 and 11 skips respectively. The final
follow-up passed 127 relevant tests without skips, as recorded in the
[source manifest](phase01-final-manifest.json). Later documentation commits do
not extend that exact-revision review to a new live-execution identity.

The [durable backlog](../../roadmaps/behavioral-eval-runner-backlog.md) remains
the continuation authority. WP-2B-3 is not DONE; OD-1 is OPEN and WP-2B-4 is
BLOCKED. This handoff does not authorize calibration, a budget reset or a merge.

## Restore the development environment

From PowerShell with Git and Windows x64 CPython 3.14 installed:

```powershell
git clone --branch review/ber-phase01-corrections https://github.com/ModernNomad-98/Project-Aegis.git
Set-Location Project-Aegis
py -3.14 -m venv ../aegis-venv
../aegis-venv/Scripts/python.exe -m pip --isolated install --index-url https://pypi.org/simple --only-binary=:all: --require-hashes -r docs/evidence/ber-recovery-2026-09-11/requirements-windows-py314.txt
../aegis-venv/Scripts/python.exe -m pip --isolated install --index-url https://pypi.org/simple -r requirements.txt
../aegis-venv/Scripts/python.exe -m pip check
../aegis-venv/Scripts/python.exe -B scripts/validate-skills.py
../aegis-venv/Scripts/python.exe -B -m tools.behavioral_eval_runner self-check
```

The hash-locked file records all 18 distributions from the verified SDK runtime,
including OpenAI SDK 3.0.0. The root requirements install the separately pinned
PyYAML 6.0.3 validator dependency. Downloads require those exact distributions to
remain available on PyPI; the GitHub checkout does not include wheel binaries or
a Python installer. Preserve hash mismatches as failures, rather than removing
the hashes or silently updating versions.

The earlier local archive restore passed offline installation, dependency/version
checks, [15 synthetic tests](restore-tests.log) and
[21 self-checks](restore-self-check.json). See the
[verification report](restore-verification.json) and
[independent preservation review](preservation-independent-review.md). These are
historical results from the local archive restore, not a claim that a fresh
network installation has just been tested on another computer.

## What is still missing

The [inventory](inventory.json) records four required original calibration inputs:

1. `wp2b3-owner-label-review-bundle-v2.zip`.
2. `dataset/wp2b3-candidate-dataset-v2.json`.
3. `dataset/wp2b3-labeling-guide-v2-copy.md`.
4. `approvals/wp2b3-owner-label-approval-v2.json`.

Their expected hashes survive; their bytes were not found in the
[repository scan](artifact-search.json) or authorized external root. The missing
original ZIP is different from the new backup ZIP created on this computer.
The original review conversation's attachment remains a recovery lead; access
has not been confirmed. The later approval JSON was not part of that original
ZIP. Supporting approval provenance is also missing but is not a driver gate
input itself.

Historical A2/A3 records say zero provider calls/spend and that the canonical
ledger and manifest had not been created. They are not established lost run
results. Later undocumented activity is unknown. No execution history or owner
approval should be recreated by assumption.

The [preflight](preflight.json) passed source and SDK integrity but stopped at
the missing evidence root. Host encryption was unverified. The original
execution controls remain unchanged by this documentation update; any intended
change belongs in the reviewed execution requirements. The current live client
supports development only, with no approved holdout freeze.

Next: recover the original attachments if available. If only some originals
survive, preserve them and identify the minimum new packaging or approval work.
If none survive, prepare replacement calibration material with new provenance
and explicit owner label approval. Then complete execution preflight against
the selected, reviewed source revision.

## Record interpretation and limits

This documentation update passed 91 validator self-test assertions and the skill
validator (184 skills, zero warnings), plus JSON parsing, handoff-link checks
and `git diff --check`. Runtime source was unchanged; the historical runtime
test results above were not rerun for these documentation additions.

The JSON and log files here preserve their historical contents, including old
machine paths and filenames. Those paths are evidence context, not instructions
to recreate the old machine. `inventory.json` points to the original scan path;
its preserved copy is `artifact-search.json` here. Its top-level user-folder
search was limited and does not establish that every cloud location was searched.
Source manifest hashes bind files at its recorded revision; use `git show` at
that revision to compare them after subsequent documentation changes.

The [source-backup record](source-backup-verification.json) documents the earlier
three-commit publication. The archive report's `off_device_copy_verified: false`
describes that ZIP at the time of verification. Neither implies that the source
or this committed handoff needs another storage destination.

Intentionally not included: redundant patches and Git bundles (the source
history is in Git), local virtual environments, wheel binaries and backup ZIPs.
They remain on the current computer. Missing calibration originals are still
unrecovered. No provider request, calibration run or merge was performed for
this documentation change.
