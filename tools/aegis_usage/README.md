# `tools/aegis_usage` — offline workflow-outcomes reporter and calculator

Two stdlib-only Python 3.14 programs that implement the contract in
[`docs/instrumentation/`](../../docs/instrumentation/README.md):

| File | Role |
| --- | --- |
| [`local_report.py`](local_report.py) | Participant side: per-workflow opt-in, bounded transition history, exact preview, local-only export. |
| [`aggregate.py`](aggregate.py) | Steward side: manual admissions, import with revision invariants, 90-day retention, deletion, cohort arithmetic and suppression. |
| [`tests/`](tests) | 104 behavioral tests, including mutant demonstrations, over synthetic fixtures only. |

**No network, no threads, no subprocesses, no third-party packages.** Capture is
off until a workflow is explicitly opted in. There is no background upload and
no reconnect retry: an export happens only after the exact bytes are previewed
and the preview SHA-256 is confirmed.

## Quick start (synthetic data only)

Run from the repository root. Use a store path outside the checkout; the tool
refuses to export reporting data under a Git working tree.

```powershell
$py = "python -B tools/aegis_usage/local_report.py --store $env:TEMP\aegis-local.json"
$ag = "python -B tools/aegis_usage/aggregate.py --store $env:TEMP\aegis-central.json"

# 1. Opt in one synthetic workflow (nothing is captured before this).
Invoke-Expression "$py opt-in --day 2026-01-06 --start-day 2026-01-05"
# {"captured": true, "workflow_ref": "wf-c616d7eaa3cb4fa4211ef995e981d4a4"}

# 2. Record bounded transitions.
Invoke-Expression "$py record --workflow-ref wf-c616... --kind observation --value ongoing --effective-day 2026-01-05"
Invoke-Expression "$py record --workflow-ref wf-c616... --kind stage --value complete --effective-day 2026-01-08 --stage discover"
Invoke-Expression "$py record --workflow-ref wf-c616... --kind status --value delivered --effective-day 2026-01-12"

# 3. Print the minimized start notice for the steward.
Invoke-Expression "$py notice --workflow-ref wf-c616..."

# 4. The steward issues a fresh admission after prospective review.
Invoke-Expression "$ag issue-admission --notice .\start-notice.json --day 2026-01-06"
# {"admission_ref": "adm-57ec...", "capability": "51eb...", "enrollment_fingerprint": "9a5c..."}

# 5. Attach it, preview the exact bytes, then export with the printed hash.
Invoke-Expression "$py attach-admission --workflow-ref wf-c616... --admission-ref adm-57ec..."
Invoke-Expression "$py preview --workflow-ref wf-c616..."   # prints preview-sha256 to stderr
Invoke-Expression "$py export --workflow-ref wf-c616... --out $env:TEMP\export.json --preview-sha256 04107c0a... --confirm"

# 6. Import with the capability secret. Importing never creates an enrollment.
Invoke-Expression "$ag import --payload $env:TEMP\export.json --capability 51eb... --day 2026-01-08"
# {"first_receipt": "2026-01-08", "prospective": true, "revision": 4, "status": "accepted"}

# 7. Compute the restricted report and the suppressed rehearsal view.
Invoke-Expression "$ag report --as-of 2026-03-01"
Invoke-Expression "$ag report --as-of 2026-03-01 --publishable"
```

`preview` writes nothing: stdout is the byte-exact export and stderr carries
`preview-sha256 <hex>`. `export` refuses to write without `--confirm` and a
matching hash, and refuses to overwrite an existing file.

## Commands

### Participant side

| Command | Purpose |
| --- | --- |
| `opt-in --day D --start-day D [--applicable-stages a,b] [--admission-ref R]` | Enable capture for one workflow and fix its immutable enrollment. |
| `notice --workflow-ref W` | Print the exact minimized start notice for the steward. |
| `attach-admission --workflow-ref W --admission-ref R` | Attach the steward-issued admission reference. |
| `record --workflow-ref W --kind K --value V --effective-day D [--stage S]` | Append one bounded transition and bump the revision. |
| `show --workflow-ref W` | Summary only: revision, transition count, capture day, admission attached. |
| `preview --workflow-ref W` | Print the exact export bytes; write nothing. |
| `export --workflow-ref W --out P --preview-sha256 H --confirm` | Write the previewed export to local disk. |
| `opt-out --workflow-ref W` | Stop capture and drop the unsent export queue. |
| `purge-expired --day D` | Apply local 60-day retention. |

### Steward side

| Command | Purpose |
| --- | --- |
| `issue-admission --notice F --day D` | Issue a random admission and capability after a prospective-review check; the secret is returned once and only its verifier is stored. |
| `import --payload F --capability C --day D` | Validate, dedupe and store one export. Never enrolls. |
| `withdraw --admission-ref A --capability C --day D` | Delete the admission and linked raw data; returns an unlinkable receipt id. |
| `expire --day D` | Apply central 90-day retention, quarantine expiry and 7-day receipt expiry. |
| `report --as-of D [--publishable]` | Compute the restricted cohort report, or the suppressed rehearsal view. |

Exit codes: `0` success, `2` a contract refusal with `ERROR <code>: <message>`
on stderr. Stable codes include `capture_disabled`, `missing_admission`,
`confirmation_required`, `preview_mismatch`, `unknown_admission`,
`bad_capability`, `expired_admission`, `enrollment_change`,
`conflicting_revision`, `history_rewrite` and `oversize`.

## What is stored where

- The participant store keeps the enrollment, the bounded transition history
  and an opt-in flag. It never leaves the participant's machine by itself.
- The central-model store keeps issued admissions (verifier only), the
  minimized raw record with its first receipt and hard expiry, quarantine
  entries kept for correction, a non-linkable withdrawal counter and unlinkable
  deletion receipts.
- Reporting data must stay outside project version control; the exporter
  refuses a target under a Git working tree.

## Tests

```text
python -B -m unittest discover -s tools/aegis_usage/tests -p "test_*.py" -v
```

The suites cover the contract and epochs, default-off and no-network behavior,
exact preview, nested forbidden fields, malformed and oversize payloads,
duplicate/conflicting/stale revisions, immutable enrollment, the day-30 and
day-31 horizon cases, stale-ongoing to unknown, scope-change invalidation, zero
denominators, stage applicability, deletion and expiry replay, retention that a
retry cannot extend, suppression and differencing, and hand-calculated
synthetic expectations. Several tests load deliberately mutated copies of the
modules and assert that the mutation is detected.

Fixtures contain invented workflows only. Do not put real workflow data in this
repository.
