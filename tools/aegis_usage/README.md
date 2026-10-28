# `tools/aegis_usage` — offline workflow-outcomes reporter and calculator

Two stdlib-only Python 3.14 programs that implement the contract in
[`docs/instrumentation/`](../../docs/instrumentation/README.md):

| File | Role |
| --- | --- |
| [`local_report.py`](local_report.py) | Participant side: per-workflow opt-in, bounded transition history, exact preview, local-only export. |
| [`aggregate.py`](aggregate.py) | Steward side: manual admissions, import with revision invariants, 90-day retention, deletion, cohort arithmetic and suppression. |
| [`tests/`](tests) | 205 behavioral tests, including mutant demonstrations, over synthetic fixtures only. |

**No network, no threads, no subprocesses, no third-party packages.** Capture is
off until a workflow is explicitly opted in. There is no background upload and
no reconnect retry: an export happens only after the exact bytes are previewed
and the preview SHA-256 is confirmed.

## Quick start (synthetic data only)

Run from the repository root. Use a store path outside the checkout; the tool
refuses to export reporting data under a Git working tree and, as defense in
depth, under the source tree that contains the tool (so an archive copy without
`.git` also fails closed for in-tree targets).

The flow is two-phase: a **start** snapshot is exported and imported within
seven days of the start, then the outcome snapshot is exported and imported
after the outcome. Importing the later export updates the earlier record.

```powershell
$py = "python -B tools/aegis_usage/local_report.py --store $env:TEMP\aegis-local.json"
$ag = "python -B tools/aegis_usage/aggregate.py --store $env:TEMP\aegis-central.json"

# 1. Opt in one synthetic workflow (nothing is captured before this).
Invoke-Expression "$py opt-in --day 2026-01-06 --start-day 2026-01-05"
# {"captured": true, "workflow_ref": "wf-c616d7eaa3cb4fa4211ef995e981d4a4"}

# 2. Record the start observation and start-phase stage.
Invoke-Expression "$py record --workflow-ref wf-c616... --kind observation --value ongoing --effective-day 2026-01-05"
Invoke-Expression "$py record --workflow-ref wf-c616... --kind stage --value complete --effective-day 2026-01-08 --stage discover"

# 3. Send the minimized start notice; the steward issues an admission.
#    Write JSON as UTF-8 without BOM: Windows PowerShell's default Set-Content
#    encoding can add a BOM, which the strict UTF-8 reader refuses.
[IO.File]::WriteAllText("$env:TEMP\start-notice.json", (Invoke-Expression "$py notice --workflow-ref wf-c616..."), [Text.UTF8Encoding]::new($false))
Invoke-Expression "$ag issue-admission --notice $env:TEMP\start-notice.json --day 2026-01-08"
# {"admission_ref": "adm-57ec...", "capability": "51eb...", "enrollment_fingerprint": "9a5c..."}

# 4. Attach it, export the start snapshot, and import it (accepted).
Invoke-Expression "$py attach-admission --workflow-ref wf-c616... --admission-ref adm-57ec..."
Invoke-Expression "$py preview --workflow-ref wf-c616..."   # prints preview-sha256 to stderr
Invoke-Expression "$py export --workflow-ref wf-c616... --out $env:TEMP\export-start.json --preview-sha256 04107c0a... --confirm"
# Keep the capability out of argv: write it to a user-only file once.
[IO.File]::WriteAllText("$env:TEMP\aegis-capability.txt", "51eb...", [Text.UTF8Encoding]::new($false))
Invoke-Expression "$ag import --payload $env:TEMP\export-start.json --capability-file $env:TEMP\aegis-capability.txt --day 2026-01-08"
# {"first_receipt": "2026-01-08", "prospective": true, "revision": 2, "status": "accepted"}

# 5. After the outcome, record it and its local evidence category.
Invoke-Expression "$py record --workflow-ref wf-c616... --kind status --value delivered --effective-day 2026-01-12"
Invoke-Expression "$py record --workflow-ref wf-c616... --kind acceptance --value independent_attested_pass --effective-day 2026-01-13 --evidence local_review_record"

# 6. Export the outcome snapshot and import the update (updated).
Invoke-Expression "$py preview --workflow-ref wf-c616..."
Invoke-Expression "$py export --workflow-ref wf-c616... --out $env:TEMP\export-outcome.json --preview-sha256 7c9e1b44... --confirm"
Invoke-Expression "$ag import --payload $env:TEMP\export-outcome.json --capability-file $env:TEMP\aegis-capability.txt --day 2026-01-15"
# {"first_receipt": "2026-01-08", "revision": 4, "status": "updated"}

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
| `record --workflow-ref W --kind K --value V --effective-day D [--stage S] [--evidence E]` | Append one bounded transition and bump the revision. `--evidence` names the local evidence category for that acceptance event (default `none`; independent attestation needs a non-`none` category). The category is stored with its own event, and the export carries the category of the acceptance that wins by effective day, so recording an earlier acceptance later cannot relabel a later one. |
| `show --workflow-ref W` | Summary only: revision, transition count, capture day, admission attached. Read-only, so it still works after `opt-out`. |
| `preview --workflow-ref W` | Print the exact export bytes; write nothing. |
| `export --workflow-ref W --out P --preview-sha256 H --confirm` | Write the previewed export to local disk. |
| `opt-out --workflow-ref W` | Stop capture immediately. There is no export queue: nothing is unsent or deleted, and retained history stays readable with `show`. |
| `delete-local --workflow-ref W --confirm` | Irreversibly delete one workflow's local history and opt-in. Local only; the store file remains if other workflows use it. Export files already written to disk are outside the store and are not removed. |
| `delete-local --all --confirm` | Irreversibly delete every local workflow and opt-in from the store file. |
| `purge-expired --day D` | Apply local 60-day retention. |

### Steward side

| Command | Purpose |
| --- | --- |
| `issue-admission --notice F --day D` | Issue a random admission and capability after a prospective-review check; the secret is returned once and only its verifier is stored. |
| `import --payload F (--capability-file C | --capability C) --day D` | Validate, dedupe and store one export. Never enrolls. Prefer `--capability-file`; `--capability` still works but prints a warning because argv is visible to other processes. |
| `withdraw --admission-ref A (--capability-file C | --capability C) --day D` | Delete every admission for the named admission's workflow and its linked raw data; returns an unlinkable receipt id. Works after the admission expires while linked data remains. |
| `expire --day D` | Apply central 90-day retention, quarantine expiry, admission tombstones and 7-day receipt expiry. |
| `report --as-of D [--publishable]` | Compute the restricted cohort report, or the suppressed rehearsal view. |

Exit codes: `0` success, `2` a contract refusal with `ERROR <code>: <message>`
on stderr, including a corrupt or incompatible store (`store_unreadable`,
`store_version`) and an unreadable input file. Stable codes include
`capture_disabled`, `missing_admission`, `confirmation_required`,
`preview_mismatch`, `unknown_admission`, `bad_capability`,
`expired_admission`, `enrollment_change`, `conflicting_revision`,
`history_rewrite`, `applicability_conflict`, `evidence_required`,
`duplicate_event_ref`, `conflicting_same_day_transition`,
`store_path_in_repository`, `store_path_symlink`, `export_path_symlink`,
`event_after_receipt`, `receipt_before_issue`,
`receipt_day_regression`, `capability_unreadable`, `notice_unreadable`,
`workflow_exists`, `invalid_nesting`, `report_truncated` and `oversize`.

An invalid payload's error path names contract fields only. A key outside the
fixed contract and forbidden vocabularies is reported as `<key>`, so an
attacker-chosen key name (for example an address) is never echoed.

One value per event kind (and per stage, for stage events) per effective day is
allowed. A second same-day value is refused as `conflicting_same_day_transition`
for correction rather than guessed from random event references. A terminal
status keeps its own same-day code, `conflicting_terminal_same_day`.

## What is stored where

- The participant store keeps the enrollment, the bounded transition history,
  each acceptance event's own evidence category and an opt-in flag. It never
  leaves the participant's machine by itself.
- `delete-local` removes the named workflow's history and opt-in, or every
  workflow with `--all`, and saves the store atomically. It is explicit
  (`--confirm`), local only and irreversible. The store file itself remains
  when other workflows still use it. Export files already written are not
  tracked and not deleted.
- The central-model store keeps issued admissions (verifier only), the
  minimized raw record with its first receipt and hard expiry, quarantine
  entries kept for correction, a non-linkable withdrawal counter and unlinkable
  deletion receipts. An expired admission leaves a verification-only tombstone
  (random admission reference, verifier hash, random workflow reference) while
  any linked record or quarantine payload survives, so the capability can still
  authorise withdrawal; it is deleted with the last linked datum. Withdrawal is
  workflow-level: a valid capability for any admission of a workflow revokes
  every admission for that workflow, so a sibling admission cannot later
  re-create the deleted records. A
  non-linkable count per start month records how many records retention
  deleted, so a completed month is never republished as complete.
- Stores, exports and directories this tool creates are user-only on POSIX
  (`0600` files, `0700` directories) regardless of the process umask, and an
  existing store is re-moded on save. Windows has no POSIX mode bits: the tool
  clears the read-only flag and relies on the ACL of the directory the operator
  chose, so keep stores and exports in a user-profile directory, not a shared
  one.
- Reporting data must stay outside project version control; both the exporter
  and the store writers refuse a path under a Git working tree and under the
  tool's own source tree, so a source archive without `.git` also fails closed
  for in-tree targets. The check walks the target path and its existing
  ancestors, so a target whose parent directory does not exist is still
  refused inside another checkout. A symlink anywhere in the path - the final
  component, a parent directory, or a dangling link whose target does not
  exist - is refused with `store_path_symlink` or `export_path_symlink`
  before any write; use a real directory path. Creating a symlink is denied to
  unprivileged Windows processes, so the symlink tests run on POSIX and are
  skipped on Windows.
- Read commands (`show`, `notice`, `preview`, `report`) do not re-check the
  path of an **existing** store, and `preview` cannot stop a shell redirect.
  The guard is a write-side control: keep stores outside version control.

## Tests

```text
python -B -m unittest discover -s tools/aegis_usage/tests -p "test_*.py" -v
```

The suites cover the contract and epochs, default-off and no-network behavior,
exact preview, nested forbidden fields, malformed and oversize payloads,
duplicate/conflicting/stale revisions, immutable enrollment, the day-30 and
day-31 horizon cases, stale-ongoing to unknown, scope-change invalidation, zero
denominators, stage applicability, local history deletion, acceptance evidence,
same-day conflict rejection, deletion and expiry replay, retention that a retry
cannot extend, cross-admission withdrawal, symlink-path refusal (POSIX),
suppression and differencing, and hand-calculated synthetic
expectations. Several tests load deliberately mutated copies of the modules and
assert that the mutation is detected.

Fixtures contain invented workflows only. Do not put real workflow data in this
repository.
