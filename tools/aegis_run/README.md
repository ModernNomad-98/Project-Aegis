# tools/aegis_run: package usage

`aegis_run` records one Aegis-assisted application run and exports a verifiable
record plus manifest. It is standard library only and Python 3.14, makes no
network call, reads no credentials, and writes only the run directory named on
the command line. `verify` and `export` also read the checked-in
`docs/aegis-run/schema.json`. The public field contract is in
[`docs/aegis-run/run-record-v1.md`](../../docs/aegis-run/run-record-v1.md); user
quickstart is in [`docs/aegis-run/README.md`](../../docs/aegis-run/README.md).

## Invocation

From the repository root:

```bash
python -m tools.aegis_run --version
python -m tools.aegis_run init --dir runs/demo --app demo-app --aegis-commit <sha> --host <host> [--model M] [--owner O]
python -m tools.aegis_run event --dir runs/demo --type stage --stage 1 --status started [--note TEXT] [--actor A]
python -m tools.aegis_run artifact --dir runs/demo --path <file> [--kind log|screenshot|report|note|dataset|other] [--external]
python -m tools.aegis_run finish --dir runs/demo --outcome delivered --limitation TEXT
python -m tools.aegis_run export --dir runs/demo
python -m tools.aegis_run verify --dir runs/demo [--allow-external]
```

`--dir` may be relative or absolute. `artifact` defaults to copying the file to
`D/artifacts/<sha256-prefix>-<basename>` and recording a relative `path` and
`source`. `--external` stores a reference only; that record is nonportable and
`verify` reports it as EXTERNAL/UNVERIFIED and fails unless `--allow-external`
is passed.

## Schema enforcement

`verify` and `export` load `docs/aegis-run/schema.json` on every invocation and
enforce it with a standard-library schema-lite validator (no `jsonschema`
dependency). The checks include required fields, `additionalProperties: false`,
enums, RFC3339 UTC `Z` timestamps, SHA-256 patterns, artifact kind values,
at least one event and non-empty limitations for export/verify, a final
outcome, and `path` null only when `external` is true. A missing schema fails closed with `SCHEMA_MISSING` and
exit 1; an unparsable schema fails with `SCHEMA_INVALID`.

## Layout

| Module | Role |
| --- | --- |
| `__init__.py` | Version and schema identifiers (`aegis.run-record/1`, `aegis.run-manifest/1`). |
| `__main__.py` | Calls `cli.main` for `python -m tools.aegis_run`. |
| `cli.py` | argparse commands, atomic JSON writes, SHA-256 artifact copying, schema-lite enforcement, export and fail-closed verify. |
| `tests/test_aegis_run.py` | Standard-library unittest coverage. |

## Exit codes

`0` success or verify PASS, `1` record failure, `SCHEMA_MISSING`/`SCHEMA_INVALID`
or verify FAIL (fail closed), `2` argparse usage failure.

## Verify scope

`verify` prints:

```text
VERIFIED: record structure and copied artifact hashes only. NOT PROVEN: host/model identity, app correctness, security, delivery, universal support.
```

Exit 0 applies only to that scope. Passing verification is not certification,
approval, readiness, delivery or merge permission, and it covers only the
single run and asserted commit in the record.

## Tests

```bash
python -P -B tools/aegis_run/tests/test_aegis_run.py
```

The test suite creates temporary run directories and also verifies the synthetic
example under [`docs/aegis-run/example`](../../docs/aegis-run/example/README.md).
