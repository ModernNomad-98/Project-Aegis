# tools/aegis_run: package usage

`aegis_run` records one Aegis-assisted application run and exports a verifiable
record plus manifest. It is standard library only and Python 3.14, makes no
network call, reads no credentials, and writes the run directory named on the
command line. The one write outside that directory is
`<repo>/.git/hooks/post-commit`, and only when the caller runs `install-hook`. `verify` and `export` also read the checked-in
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

python -m tools.aegis_run sync --dir runs/demo --project-state docs/project-state.md [--dry-run]
python -m tools.aegis_run watch --dir runs/demo --project-state docs/project-state.md [--interval 30]
python -m tools.aegis_run install-hook --repo . --dir runs/demo --project-state docs/project-state.md --aegis-path . [--force]
python -m tools.aegis_run uninstall-hook --repo .
```

`--dir` may be relative or absolute. `artifact` defaults to copying the file to
`D/artifacts/<sha256-prefix>-<basename>` and recording a relative `path` and
`source`. `--external` stores a reference only; that record is nonportable and
`verify` reports it as EXTERNAL/UNVERIFIED and fails unless `--allow-external`
is passed.

## Automatic project-state sync

`sync` reads the `## State snapshots` table of a project-state file and imports
each row whose ID (for example `SS-003`) is not already recorded in the event
field `source_id`. The project-state file is only read; `sync` never writes it.

| Situation | Event written |
| --- | --- |
| First import, every row except the latest | `type: note`, `status: started`, note `historical snapshot SS-001 imported from project-state; not observed live` |
| First import, the latest row | `type: stage`, `status: started`, note `Imported from project-state; next: <next>` |
| A later sync, each new row | `type: stage`, `status: started`, same note |

A snapshot records the stage the project is in when the row is written. It is
not evidence that the stage passed, so `sync` writes only `status: started`,
never `passed`, and never infers one. Re-running `sync` reports `0 new`.
`--dry-run` prints the same lines and writes nothing.

`sync` takes an exclusive `D/sync.lock` (`O_CREAT|O_EXCL`, retried for about
5 seconds) and holds it across the record read and every append, so two syncs
cannot import the same row twice. Only one sync should write to a run directory
at a time. A lock older than 120 seconds is never deleted automatically: sync
fails, names the lock path, and asks you to remove it manually if no sync is
running. A missing file,
missing `## State snapshots` section, bad header, ragged row, duplicate-free
requirement or unparsable date/ID/stage is a clean error and exit 1, never a
traceback.

`watch` polls the project-state mtime (minimum 5 seconds, default 30) and runs
the same `sync` on change, printing one line per change. It is a foreground,
local process: Ctrl-C exits 0, nothing is daemonized, and it makes no network
call. Start it once per session, or use the hook below.

`install-hook` writes `<repo>/.git/hooks/post-commit` (POSIX `sh`, absolute
shell-quoted paths, no secrets). The hook body is:

```sh
cd '<aegis-path>' || exit 0
PYTHONPATH='<aegis-path>' python -P -m tools.aegis_run sync --dir '<D>' --project-state '<state>' || :
exit 0
```

The `cd` plus `-P` matter: git runs hooks from the repository root, where a
repository-local `tools/` package would otherwise shadow the checkout on
`sys.path` and the hook would run the wrong code. `-P` stops the working
directory being prepended, so `tools` resolves through `PYTHONPATH` to the
named Aegis checkout. The hook exits 0 even when sync reports nothing, so a
commit is never blocked. It refuses to replace a hook it did not write; with
`--force` it backs the old hook up to `post-commit.bak-<timestamp>`.
`uninstall-hook` removes only a hook carrying the marker and reports it; a hook
it did not write, or no hook at all, is a clean exit 1. Both commands act on
`<repo>/.git/hooks/post-commit`, which is outside the run directory.

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
| `cli.py` | argparse commands, atomic JSON writes, SHA-256 artifact copying, schema-lite enforcement, export and fail-closed verify, project-state sync and watch, post-commit hook management. |
| `tests/test_aegis_run.py` | Standard-library unittest coverage. |

## Exit codes

`0` success or verify PASS, `1` record failure, `SCHEMA_MISSING`/`SCHEMA_INVALID`,
verify FAIL (fail closed), an unreadable project-state file/table/row or a held
sync lock, `2` argparse usage failure.

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

The test suite creates temporary run directories, temporary git repositories
for the hook tests, and also verifies the synthetic example under
[`docs/aegis-run/example`](../../docs/aegis-run/example/README.md).
