# tools/aegis_adopt: package usage

`aegis_adopt` records one local Aegis checkout in a consumer repository so a
coding session that starts there can find Aegis. It writes the bootstrap files,
then `doctor` re-reads them. It is standard library only and Python 3.14, makes
no network call, reads no credentials, and writes only the files listed below
inside the repository named by `--repo`. The user guide is
[docs/aegis-adopt/README.md](../../docs/aegis-adopt/README.md).

## Invocation

Run from the Aegis checkout root:

```bash
python -m tools.aegis_adopt --version
python -m tools.aegis_adopt adopt --repo PATH --aegis-path PATH [--cursor] [--copilot] [--gemini]
python -m tools.aegis_adopt unadopt --repo PATH [--force]
python -m tools.aegis_adopt doctor --repo PATH
```

`--repo` is the consumer repository. `--aegis-path` is the Aegis checkout to
record; it must contain `tools/aegis_run/__main__.py`. Both are resolved to
absolute paths. `doctor` writes nothing and never executes a wrapper. It checks
the recorded wrapper hashes and runs the trusted Aegis module directly with
`python -B -P -m tools.aegis_run --version` (15-second timeout).

The wrappers that `adopt` writes run the recorded checkout with
`PYTHONPATH=<aegis-path>` and `python -P -m tools.aegis_run`, so a
repository-local `tools/` package cannot shadow Aegis.

## Files written by adopt

| File | Role |
| --- | --- |
| `.aegis/project.json` | Adoption metadata, schema `aegis.adopt/1`. |
| `.aegis/START-HERE.md` | The first file a session reads. |
| `.aegis/bin/aegis-run` | POSIX `sh` wrapper around the recorded checkout. |
| `.aegis/bin/aegis-run.cmd` | Windows `cmd` wrapper around the same checkout. |
| `AGENTS.md` | Whole file preserved; one marked Aegis bootstrap block. |
| `CLAUDE.md` | Whole file preserved; the same marked block. |
| host files | Only for hosts opted in by flag or recorded earlier. |

`project.json` records:

```json
{
  "schema": "aegis.adopt/1",
  "adopted_at": "2026-11-22T14:37:55Z",
  "aegis_path": "C:\\src\\Project Aegis\\aegis-batch34\\lane-adopt",
  "aegis_commit": null,
  "start_here": ".aegis/START-HERE.md",
  "hosts": {"cursor": true, "copilot": false, "gemini": false},
  "wrapper_sha256": {
    "sh": "<64 lowercase hex characters>",
    "cmd": "<64 lowercase hex characters>"
  }
}
```

`adopted_at` is preserved across runs. `aegis_path` is absolute.
`aegis_commit` is the checkout's `git rev-parse HEAD` when it is a git
repository, otherwise `null`; no network is used. `hosts` records every host
file this adoption owns, and host opt-ins are additive: a host recorded by an
earlier run stays recorded when a later run omits its flag.

`blocks` records, for each marker file, whether adopt created it and which
newline bytes adopt added around the block, so unadopt can restore the original
bytes exactly or remove a file adopt created. Unadopt removes only the block
from the current bytes; it never restores a pre-adopt snapshot over later edits.
`created_dirs` records the directories that did not exist before adoption.

`wrapper_sha256.sh` and `wrapper_sha256.cmd` are the SHA-256 of each wrapper
file as written. `doctor` recomputes them and also compares the wrapper bytes
with the current template for the recorded `aegis_path`. Any edited byte, a
no-op wrapper, an added command or an extra side-effect line fails the check.

## Markers and preservation

The block is identified by two lines, in this order:

```text
<!-- AEGIS-BOOTSTRAP:BEGIN v1 -->
...
<!-- AEGIS-BOOTSTRAP:END -->
```

| Existing file | adopt behavior |
| --- | --- |
| Absent | Creates the file containing the canonical block. |
| No markers | Appends the canonical block; existing bytes are unchanged. One line ending is added first only when the file does not already end with one. |
| Exactly one block | Replaces the text from BEGIN through END; prefix and suffix bytes are unchanged. |
| Duplicate markers | Exits 1 before writing anything, naming the file. |
| Missing one marker, or END before BEGIN | Exits 1 before writing anything, naming the file. |

AGENTS.md, CLAUDE.md and host files are read and written as bytes, but each
must decode as strict UTF-8: a non-UTF-8 file is rejected before any write.
Adopt picks the dominant line ending of the existing file (CRLF, LF, or CR) and
uses it for every line of the block; every byte outside the markers is copied
unchanged, including mixed line endings. A second successful run is
byte-identical for the same inputs.

Before the first write, adopt preflights every target path. `.aegis`,
`.aegis/bin`, the wrappers, AGENTS.md, CLAUDE.md and every enabled host path
must be ordinary paths inside the repository. A symbolic link or junction, a
resolved path outside the repository, a wrong file/directory type, a regular
file at `.cursor`/`.github` when that host is enabled, or an existing target
with no write bit (`mode & 0o222 == 0`, including a Windows read-only file) is
rejected before any file is written.

Every read and marker check also happens before the first write, so a malformed
file cannot leave a half-adopted repository.

Each write uses an unpredictable same-directory temporary file from
`tempfile.mkstemp` (prefix `.aegis-`, suffix `.tmp`), fsyncs the descriptor,
and calls `os.replace`. It never uses a predictable `<target>.tmp`, so a
symlink or hardlink planted at that name is left untouched.

New files are created with mode `0o644`, except the POSIX
`.aegis/bin/aegis-run` wrapper, which is `0o755`. An existing target keeps its
original mode. Windows represents only writable/read-only, not POSIX group or
execute bits.

Before the first write, adopt snapshots the existing bytes and permission bits of
every target and records which paths are new. If any write raises, it restores
the snapshots byte-for-byte, removes the new files and any directories it
created, and exits 1 with a rolled-back error. `KeyboardInterrupt` and
`SystemExit` are rolled back too and then re-raised unchanged.

## Optional host files

```bash
python -m tools.aegis_adopt adopt --repo PATH --aegis-path PATH --cursor
python -m tools.aegis_adopt adopt --repo PATH --aegis-path PATH --copilot
python -m tools.aegis_adopt adopt --repo PATH --aegis-path PATH --gemini
```

| Flag | File | Host convention |
| --- | --- | --- |
| `--cursor` | `.cursor/rules/aegis.mdc` | Cursor project rule. |
| `--copilot` | `.github/copilot-instructions.md` | GitHub Copilot repository instructions. |
| `--gemini` | `GEMINI.md` | Gemini CLI context file. |

With no flags and no earlier record, adopt creates none of these files and no
host directories. Each installed file carries the same marked block.

## What doctor checks

`doctor` writes nothing and prints one `FAIL: ...` line per finding:

- `.aegis/project.json` exists, parses as UTF-8 JSON, has schema
  `aegis.adopt/1`, a valid `adopted_at`, an absolute `aegis_path`, a
  `null` or 40-character `aegis_commit`, the expected `start_here`, a
  `hosts` object containing exactly the three boolean host flags, and a
  `wrapper_sha256` object with valid `sh` and `cmd` hashes.
- The recorded `aegis_path` contains `tools/aegis_run/__main__.py`.
- `.aegis/START-HERE.md` exists, is non-empty and names
  `.aegis/bin/aegis-run`.
- `AGENTS.md` and `CLAUDE.md` each contain exactly the canonical block.
- Both wrappers exist. Each file's SHA-256 must equal the value recorded in
  `project.json` `wrapper_sha256` (keys `sh` and `cmd`), and the bytes must
  match the exact `aegis.adopt/1` template for the recorded `aegis_path`.
  A no-op wrapper, an `exit`/`echo` replacement, an extra command or a
  side-effect line therefore fails without being run.
- The trusted module is run directly, never through a wrapper:
  `python -B -P -m tools.aegis_run --version` with
  `PYTHONPATH=<aegis_path>` and `PYTHONDONTWRITEBYTECODE=1`, with a
  15-second timeout. It must exit 0 and print `aegis_run`. Unavailable
  execution, a timeout, a nonzero exit or missing output is a finding. The
  `-B` flag and environment setting keep doctor from writing `__pycache__`.
- Every host file recorded as `true` exists and contains the canonical block.

It exits 0 with `PASS` only when there are no findings. Missing files,
unreadable or non-UTF-8 files, malformed JSON, malformed or duplicate markers,
missing wrappers, a missing recorded run module, a wrapper hash or template
mismatch, a failed trusted-module run and bad arguments all exit 1 with findings
and no traceback. Doctor never creates, repairs or deletes a file, never
executes a wrapper, and leaves no `__pycache__`.

## Reversible unadopt

```bash
python -m tools.aegis_adopt unadopt --repo PATH [--force]
```

`unadopt` requires `.aegis/project.json` with schema `aegis.adopt/1` and
refuses an unreadable file, invalid JSON, or any other schema. With a valid
project it:

- removes only the marked Aegis block from `AGENTS.md`, `CLAUDE.md`, and every
  optional host file recorded as enabled in `hosts`;
- uses the recorded `blocks` metadata to remove exactly the newline bytes adopt
  added, preserving every other byte and the file's newline style and mode;
- if `blocks[path].created` is true and the bytes remaining after block
  removal are empty, removes that marker file entirely; if user content
  remains, keeps the file with those current bytes;
- if `blocks[path].created` is false, keeps the file with every remaining
  current byte, including edits made after adoption; a pre-adopt snapshot is
  never written over later edits;
- removes the recorded `created_dirs` directories when they are empty;
- reports `already absent` for a marker file with no block;
- removes `.aegis/bin/aegis-run`, `.aegis/bin/aegis-run.cmd`,
  `.aegis/START-HERE.md`, and `.aegis/project.json`;
- removes `.aegis/bin` and `.aegis` only when they become empty;
- refuses when `.aegis` contains any other file or directory, naming it, unless
  `--force` is passed; with `--force` the unknown paths are left in place and
  reported.

If `.aegis/project.json` is missing, `--force` scans AGENTS.md, CLAUDE.md and
the known optional host paths, prints `preview: <count> AEGIS block(s)`, then
removes the blocks and any known `.aegis` files. Without `--force`, missing
project metadata is an error when any block or known `.aegis` file remains. A
repository with neither metadata nor blocks is already unadopted and exits 0.

Unadopt is transactional: it snapshots the bytes and modes of every file it will
change or remove and rolls back on failure, including interrupts. It makes no
network call, is idempotent, and removes only marked blocks, files adopt created,
known `.aegis` files, and empty directories adopt created.

## Exit codes

`0` success, doctor PASS, or an already-unadopted no-op; `1` adopt/unadopt
failure, doctor FAIL, or a usage error. This tool has no exit 2: its contract is
success 0 / failure 1, and a bad argument is reported as a clean one-line error.

## Tests

```bash
python -P -B tools/aegis_adopt/tests/test_aegis_adopt.py
```

The suite uses temporary consumer repositories and a synthetic, executable
Aegis checkout. It asserts that no optional host file appears by default,
blocks `socket` while adopt and doctor run, and covers wrapper hash mismatches
(a no-op `exit`/`echo` wrapper and an extra side-effect line), mixed/CRLF
content preserved byte-for-byte outside a CRLF block, non-UTF-8 marker-file
rejection before any write, preflight rejection of `.aegis`/AGENTS links and
regular files at host directories before any write, a read-only AGENTS target
rejected before any write, existing mode preservation, new `0o644` START-HERE,
new `0o755` sh wrapper, mode stability across a second adopt, a planted
predictable `<target>.tmp` link left untouched by atomic writes, rollback after
an injected write failure with originals restored, rollback on an injected
`KeyboardInterrupt` with the interrupt propagating, a missing recorded run
module, a trusted-module run that exits nonzero or prints no version, and a
check that doctor leaves no `__pycache__`. Unadopt tests cover exact AGENTS
restoration, CRLF preservation, host-file block removal, a no-op second run,
unknown `.aegis` refusal then `--force` leaving it, malformed/wrong-schema
project refusal, `--force` with missing project metadata, removal of
AGENTS/CLAUDE files adopt created, removal of created `.cursor`/`.github`
directories when empty, and preservation of user notes appended after adoption.

## Limits

Adoption copies no skills and installs no host. It cannot make a host that
ignores startup files read `AGENTS.md`, `CLAUDE.md` or a host rule. The
wrappers require Python on `PATH` and the recorded checkout at the absolute
`aegis_path`; if that checkout moves, rerun adopt. Doctor never executes a
wrapper, but it does run the recorded checkout's `tools.aegis_run` module
directly; run it only on a repository whose recorded path you trust. PASS proves
local file consistency, exact wrapper hashes and a successful
`aegis_run --version` only, not full checkout behavior, that a model read the
files, or that the application is correct, secure or delivered. Unadopt removes
only the recorded blocks, marker files adopt created, known `.aegis` files and
empty directories adopt created; unknown paths require `--force` and are left
in place.

## Provenance

Reference implementation authored by DeepSeek (DeepSeek Harness) for the Aegis
Maturity Package. Model: DeepSeek.
