# Aegis Run Record v1

Aegis Run Record records one Aegis-assisted application run, copies its
artifacts into the run directory, hashes them, and exports a portable pair of
files: the full record and a manifest binding that record and every copied
artifact by SHA-256. `verify` re-checks the pair offline and fails closed. Both
`verify` and `export` load [schema.json](schema.json) from the repository root
and enforce it with a standard-library schema-lite validator; if that file is
missing they fail closed with `SCHEMA_MISSING`. This is auditing tooling, not
enforcement, and it certifies nothing.

The implementation is standard library only and Python 3.14, at
[`tools/aegis_run/cli.py`](../../tools/aegis_run/cli.py); package usage is in
[the package README](../../tools/aegis_run/README.md). The field contract is
[run-record-v1.md](run-record-v1.md), the machine-readable record shape is
[schema.json](schema.json), and a synthetic illustration is in
[example/](example/README.md).

## Quickstart

Run these from the repository root. Replace the example values. Arguments shown
on one line may be split freely.

```bash
python -m tools.aegis_run init --dir runs/demo --app demo-app --aegis-commit 0123456789abcdef0123456789abcdef01234567 --host windows-11 --model DeepSeek --owner owner-name

python -m tools.aegis_run event --dir runs/demo --type stage --stage 1 --status started --note "requirements captured" --actor builder
python -m tools.aegis_run event --dir runs/demo --type approval --stage 1 --status passed --note "owner approved scope" --actor owner
python -m tools.aegis_run event --dir runs/demo --type stage --stage 2 --status passed --note "tests green" --actor builder

python -m tools.aegis_run artifact --dir runs/demo --path runs/demo/evidence/build.log --kind log
python -m tools.aegis_run artifact --dir runs/demo --path C:/temp/screenshot.png --kind screenshot

python -m tools.aegis_run finish --dir runs/demo --outcome delivered --limitation "one host only" --limitation "no live provider run"
python -m tools.aegis_run export --dir runs/demo
python -m tools.aegis_run verify --dir runs/demo
```

Both artifact commands copy the file into `runs/demo/artifacts/` as
`<sha256-prefix>-<basename>` and record the original reference under
`source`. `verify` prints `PASS` plus a scope block and exits 0, or prints
every `FAIL` finding and exits 1. `export` prints the absolute paths of
`runs/demo/aegis-run.json` and `runs/demo/manifest.json`. Use `--version` for
the tool version.

## Commands

| Command | What it does | Rules |
| --- | --- | --- |
| `init --dir D --app NAME --aegis-commit SHA --host HOST [--model M] [--owner O]` | Creates `D`, `D/aegis-run.json` and an empty `D/events.jsonl`. | Runs once per directory; refuses to overwrite an existing record. |
| `event --dir D --type stage\|approval\|note --stage N --status started\|passed\|failed\|skipped [--note TEXT] [--actor A]` | Appends one UTC-timestamped event to `D/events.jsonl` and mirrors it in the record. | `events.jsonl` is append-only; `verify` checks the mirror. |
| `artifact --dir D --path FILE [--kind log\|screenshot\|report\|note\|dataset\|other] [--external]` | Hashes one existing file (SHA-256 and byte size). By default it also copies the file to `D/artifacts/<sha256-prefix>-<basename>`. | Default entries are `portable: true` with relative `path` and `source`; never absolute. `--external` stores a reference without copying: `external: true`, `portable: false`, `path: null`. Re-recording the same `source` replaces its entry. `kind` is optional and must be one of the listed values. |
| `finish --dir D --outcome delivered\|stopped\|failed --limitation TEXT` | Records the outcome and at least one limitation; repeat `--limitation`. | Once per run; blank limitations are rejected; export requires it. |
| `export --dir D` | Loads `schema.json`, validates the record against it, then atomically writes the canonical record and `manifest.json` with `record_sha256` and the artifact projection. | Requires a finished run with a non-empty `limitations` list and a final outcome. A missing schema fails as `SCHEMA_MISSING`; schema violations fail before any file is written. Deterministic JSON: sorted keys, UTF-8, LF. |
| `verify --dir D [--allow-external]` | Loads `schema.json` and enforces it: required fields, enums, RFC3339 UTC `Z` timestamps, SHA-256 patterns, artifact kind enum, unknown-property rejection, non-empty limitations, final outcome and the `path`/`external` rule. It then recomputes every copied artifact hash and size, recomputes `record_sha256`, and checks the event mirror, manifest projection, traversal and symlink escape. | Fail closed: a missing schema is `SCHEMA_MISSING` and any finding exits 1. External entries are `EXTERNAL/UNVERIFIED` and fail verification unless `--allow-external` is explicit. |

Exit codes: `0` success or PASS, `1` record/verify failure, `2` argument or
usage failure.

## Files in a run directory

| File | Role |
| --- | --- |
| `aegis-run.json` | Full record for the single run. Rewritten canonically by `export`. |
| `events.jsonl` | Append-only event log, one compact JSON object per line; mirrors `events` in the record. |
| `artifacts/` | Copied artifact bytes, named `<sha256-prefix>-<basename>`. These are the files `verify` re-hashes. |
| `manifest.json` | `schema: aegis.run-manifest/1`, `record: "aegis-run.json"`, `record_sha256`, and `artifacts` entries of `path`, `source`, `bytes`, `sha256`, `portable`, `external`. Written by `export`. |

## Schema enforcement

`verify` and `export` read [schema.json](schema.json) from the repository root
and run a standard-library schema-lite validator: `required`,
`additionalProperties: false`, `const`, `enum`, `type`, `pattern`, `format`,
`minLength`, `minItems`, `minimum`, `items` and `$ref`. In practical terms:

- `schema` must be `aegis.run-record/1`; unknown root, event or artifact
  properties are rejected.
- `created_at` and every event `ts` must be RFC3339 UTC timestamps ending `Z`.
- `run_id` is a UUID; `app`, `aegis_commit`, `host` and a supplied `model` are
  non-empty strings; `model` may be `null` when omitted.
- Event `type` and `status` use their fixed v1 enums; `note` and `actor` are
  string or null; unknown event properties are rejected. The schema permits an
  empty `events` list only for a just-initialized run; `export` and `verify`
  require at least one event, so a publishable run needs at least one recorded
  event.
- Artifacts require `path`, `source`, `bytes`, `sha256`, `portable`, `external`
  and `kind`; `path` is null only when `external` is true; `kind` is one of
  `log`, `screenshot`, `report`, `note`, `dataset`, `other` or null; `bytes` is
  a non-negative integer; `sha256` is 64 lowercase hex characters.
- `limitations` is an array of non-empty strings. It may be empty only before
  finish; `finish` and `export` require at least one entry, and `verify`
  rejects an exported record with none.
- `outcome` is `delivered`, `stopped` or `failed`; `null` is allowed only
  before finish, so `export` and `verify` require a final value.

If `schema.json` is missing or unreadable, `verify` and `export` stop with
`SCHEMA_MISSING` and exit 1; they never fall back to a looser shape.

## The example

[example/](example/README.md) is a synthetic run generated by this CLI and
labelled EXAMPLE, NOT A REAL APP PROOF. It exists to show the file layout and
the verify output, not to support any claim about an application.

## What PASS proves, and what it does not

`verify` prints this scope block:

```text
VERIFIED: record structure and copied artifact hashes only. NOT PROVEN: host/model identity, app correctness, security, delivery, universal support.
```

PASS proves internal consistency at verification time: the record parses, the
loaded schema accepts it, and it has the required v1 fields, including at least
one event, non-empty `limitations` and a final `outcome`; the manifest's
`record_sha256` equals the SHA-256 of the record file as it exists then; every
copied artifact is a regular file inside the run directory, free of traversal and
symbolic links, with the recorded size and hash; the event log is valid UTF-8 and
mirrors the record; and the manifest's artifact list matches the record's. Any
byte change, missing file, absolute path, traversal attempt, non-UTF-8 event log,
empty event list or missing field fails.

PASS does not prove who produced the record, that its events are complete or
truthful, that the host or model values are accurate, that the application works
or is secure, or that the files will stay unchanged. SHA-256 gives integrity,
not identity or authorship; the record is not signed. Timestamps come from the
local clock and are not trusted time.

## Privacy and limits

- Local files only: no network, no credentials, no provider calls, no
  telemetry. `verify` reads `D`, the copied artifacts inside it, and the
  checked-in `docs/aegis-run/schema.json`.
- Copying is deliberate: artifact bytes are duplicated into `D/artifacts/`, so
  a run directory can contain secrets, customer data or personal data that was
  in the source file. Never record a file you would not publish.
- The record never stores an absolute path. `source` is relative to `D` and can
  begin with `../`, which may reveal nearby directory names but not the volume
  root. Keep publishable artifacts inside `D` where `source` is fully internal.
- `--external` records a hash without copying. Such a run is not portable and
  `verify` reports `EXTERNAL/UNVERIFIED` and fails unless `--allow-external` is
  passed; even then the external file is not re-hashed and no PASS claim covers
  it.
- Notes, limitations, app, host, model and owner are exported verbatim. Never
  put tokens or personal data in them; there is no redaction step.
- The scope is one run at one asserted Aegis commit on the recorded host. It
  makes no universal claim about Aegis or any application, is not a
  certification, and is not approval, readiness, delivery or merge permission.

## CI wiring: UNRUN

No workflow was added or edited. Wiring `verify` into CI would require a
protected workflow change and its own review; as delivered, CI wiring is
**UNRUN** and this tool claims no CI enforcement.

## Tests

```bash
python -P -B tools/aegis_run/tests/test_aegis_run.py
```

## Provenance

Reference implementation authored by DeepSeek (DeepSeek Harness) for the Aegis
Maturity Package. Model: DeepSeek.
