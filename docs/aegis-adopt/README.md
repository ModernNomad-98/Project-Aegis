# Aegis Adopt v1

Aegis Adopt makes a repository's sessions aware that the repository uses
Project Aegis. One command records a local Aegis checkout in the consumer
repository, writes a short startup file, installs wrappers around the checkout,
and inserts one marked block into the files a coding host reads first. A second
command, `doctor`, re-checks those local files. Adoption copies no skills,
installs no host, and makes no network call.

The implementation is standard library only and Python 3.14, at
[`tools/aegis_adopt/cli.py`](../../tools/aegis_adopt/cli.py); package usage is in
[the package README](../../tools/aegis_adopt/README.md). The Aegis run-record
tool that the wrappers call is documented in
[`docs/aegis-run`](../aegis-run/README.md).

## Quickstart

Run these from the Aegis checkout root. Replace the example paths. Arguments
shown on one line may be split freely.

```bash
python -m tools.aegis_adopt adopt --repo C:/work/my-app --aegis-path C:/src/Project-Aegis
python -m tools.aegis_adopt doctor --repo C:/work/my-app
python -m tools.aegis_adopt unadopt --repo C:/work/my-app
```

To opt in to a host file, add exactly the flag for that host:

```bash
python -m tools.aegis_adopt adopt --repo C:/work/my-app --aegis-path C:/src/Project-Aegis --cursor
python -m tools.aegis_adopt adopt --repo C:/work/my-app --aegis-path C:/src/Project-Aegis --copilot
python -m tools.aegis_adopt adopt --repo C:/work/my-app --aegis-path C:/src/Project-Aegis --gemini
```

`adopt` is idempotent. Rerun it after the Aegis checkout moves or after a new
host flag is needed; it replaces only the marked blocks and rewrites the same
bytes for the same inputs. `doctor` writes nothing and never executes a
wrapper; it checks the recorded wrapper hashes and runs the trusted Aegis
module with `--version`. `unadopt` reverses an adoption, removing only the
marked blocks and known `.aegis` files. `--version` prints the tool version.

## What a session reads

A session that starts in the adopted repository is expected to read, in this
order:

1. `.aegis/START-HERE.md` — the adoption summary, the wrapper commands and the
   session rules.
2. The marked **Aegis bootstrap** block in `AGENTS.md` and `CLAUDE.md` — the
   same block in both files, so either host sees the same instruction.
3. `.aegis/project.json` — the machine-readable record of which checkout the
   repository uses.
4. `.aegis/bin/aegis-run` (POSIX) or `.aegis/bin/aegis-run.cmd` (Windows) — the
   wrapper that runs that checkout.

The block says to read `.aegis/START-HERE.md` before any task, to keep the run
record in sync after confirmed project-state writes, and to use the wrapper.
Text outside the block belongs to the repository and is never rewritten.

## What adopt writes

| File | Contents |
| --- | --- |
| `.aegis/project.json` | Schema `aegis.adopt/1`, `adopted_at`, absolute `aegis_path`, `aegis_commit` or `null`, `start_here`, the three boolean `hosts` flags, `wrapper_sha256` for both wrappers, and `blocks` metadata for exact unadopt. |
| `.aegis/START-HERE.md` | Startup summary and rules, including the wrapper paths. |
| `.aegis/bin/aegis-run` | POSIX `sh` wrapper: sets `PYTHONPATH` to the recorded checkout and runs `python -P -m tools.aegis_run "$@"`. |
| `.aegis/bin/aegis-run.cmd` | Windows wrapper with the same checkout, `PYTHONPATH` and `python -P -m tools.aegis_run %*`. |
| `AGENTS.md` | Created when absent; otherwise one marked block is appended or replaced. |
| `CLAUDE.md` | Same rule as `AGENTS.md`, with the same block. |
| host files | Only when the matching flag is passed or the host was recorded earlier. |

`adopted_at` is preserved on later runs. `aegis_commit` is the checkout's
current `git rev-parse HEAD` when it is a git repository and `null` otherwise;
the lookup is local. Host opt-ins are additive: once a host is recorded, a later
run that omits the flag still checks and refreshes that host file.

`wrapper_sha256.sh` and `wrapper_sha256.cmd` are the SHA-256 of each wrapper
file as adopt wrote it. `doctor` recomputes the hashes and also compares the
bytes with the current wrapper template for the recorded `aegis_path`. Any edit (a no-op `exit`/`echo` wrapper, an extra
command or a side-effect line) makes the check fail. Doctor never runs a
wrapper.

### The marked block

```text
<!-- AEGIS-BOOTSTRAP:BEGIN v1 -->
...
<!-- AEGIS-BOOTSTRAP:END -->
```

The block is the only part of `AGENTS.md`, `CLAUDE.md` or an optional host file
that adopt edits. Existing files without markers are kept byte-for-byte and the
block is appended after them. Existing files with exactly one block keep every
byte before BEGIN and after END. Duplicate markers, a missing marker, or END
before BEGIN make adopt exit 1 before writing anything, so it never guesses
which copy to replace.

Adopt reads these files as bytes and requires strict UTF-8; a non-UTF-8
`AGENTS.md`, `CLAUDE.md` or optional host file is rejected before any write.
It chooses the dominant line ending (CRLF, LF, or CR) for the inserted block.
Bytes outside the markers are copied unchanged, including mixed line endings; a
second adoption is byte-identical. If an appended file does not already end with
a line ending, exactly one is added before the block.

Before writing, adopt preflights every target path. It refuses symbolic links,
junctions, paths that resolve outside the repository, wrong file/directory
types, a regular file at `.cursor` or `.github` when that host is enabled, and
existing targets with no write bit (`mode & 0o222 == 0`, including Windows
read-only files). A preflight failure writes nothing.

Writes use an unpredictable same-directory `tempfile.mkstemp` file, fsync and
atomic replace. A predictable `<target>.tmp` path is never used, so a symlink
or hardlink planted there is ignored and left untouched. New files are `0o644`
except the POSIX sh wrapper at `0o755`; existing modes are preserved. On
Windows, only writable/read-only is representable, not POSIX group or execute
bits.

Before writing, adopt snapshots every target's bytes and permission bits. If a
write fails, it restores existing files byte-for-byte, removes new files and
directories it created, and exits 1 with a rolled-back error. An interrupt or
`SystemExit` is rolled back the same way and then re-raised.

### Optional host files

| Flag | File |
| --- | --- |
| `--cursor` | `.cursor/rules/aegis.mdc` |
| `--copilot` | `.github/copilot-instructions.md` |
| `--gemini` | `GEMINI.md` |

With no flags, a fresh adoption creates none of these files and no host
directories. Each installed file carries the same marked block.

### The wrappers

The wrapper does not copy Aegis into the consumer repository. It sets
`PYTHONPATH` to the recorded `aegis_path` and runs
`python -P -m tools.aegis_run` with the caller's arguments. The `-P` flag stops
Python from prepending the current directory, so a repository-local `tools/`
package cannot shadow the recorded checkout; `PYTHONPATH` is what makes
`tools.aegis_run` importable. The wrapper exits 1 with a short message when the
recorded checkout no longer has `tools/aegis_run/__main__.py`.

## What doctor checks

```bash
python -m tools.aegis_adopt doctor --repo PATH
```

`doctor` writes nothing. It exits 0 and prints `PASS` only when all of these
hold:

- `.aegis/project.json` exists, is valid UTF-8 JSON, has schema
  `aegis.adopt/1`, a valid UTC `adopted_at`, an absolute `aegis_path`, a
  `null` or 40-character lowercase `aegis_commit`, the expected `start_here`,
  and `hosts` with exactly the three boolean flags. The recorded
  `aegis_path` must contain `tools/aegis_run/__main__.py`.
- `.aegis/START-HERE.md` exists, is non-empty and names the wrapper.
- `AGENTS.md` and `CLAUDE.md` each contain exactly one canonical block.
- Both wrappers exist. Each file's SHA-256 must equal the recorded
  `wrapper_sha256`, and its bytes must match the exact wrapper template for the
  recorded `aegis_path`. A no-op `exit`/`echo` wrapper, an added command or
  a side-effect line fails by hash; the wrapper is never run.
- The trusted module is run directly, never through a wrapper:
  `python -B -P -m tools.aegis_run --version` with
  `PYTHONPATH=<aegis_path>` and `PYTHONDONTWRITEBYTECODE=1`, with a
  15-second timeout. It must exit 0 and print `aegis_run`. Unavailable
  execution, a timeout, a nonzero exit or missing output fails. The `-B` flag
  and environment setting prevent `__pycache__` writes.
- Every host flag recorded as `true` has its file with the canonical block.

Any other result exits 1 and prints one `FAIL: ...` line per finding, a finding
count, and the scope. Missing files, non-UTF-8 or unreadable files, malformed
JSON, malformed or duplicate markers, missing wrappers, a missing recorded run
module, a wrapper hash or template mismatch, a failed trusted-module run and
bad arguments all exit 1 without a traceback. Doctor does not repair anything;
rerun adopt for that.

PASS covers local file consistency, exact wrapper hashes and a successful
`aegis_run --version` run only. It does not prove full checkout behavior, that
a model read the files, that a host honors them, or that the application is
correct, secure or delivered.

## Unadopt (reversible)

```bash
python -m tools.aegis_adopt unadopt --repo PATH [--force]
```

`unadopt` requires `.aegis/project.json` with schema `aegis.adopt/1`; an
unreadable file, invalid JSON or another schema is refused. With valid metadata
it removes only the marked Aegis block from `AGENTS.md`, `CLAUDE.md` and each
optional host file recorded as enabled, using the stored `blocks` metadata to
remove exactly the newline bytes adopt added. Every other byte, the newline
style and the file mode are preserved. A marker file with no block is reported
as `already absent`. If `blocks[path].created` is true and the bytes remaining
after block removal are empty, unadopt removes the marker file entirely; if
user content remains, it keeps the file with those current bytes. If
`created` is false, unadopt keeps the file with every remaining current byte,
including edits made after adoption. It never restores a pre-adopt snapshot
over later edits. Matching `created_dirs` directories are removed when empty.

It then removes `.aegis/bin/aegis-run`, `.aegis/bin/aegis-run.cmd`,
`.aegis/START-HERE.md` and `.aegis/project.json`; `.aegis/bin` and `.aegis`
are removed only when empty. Any other path under `.aegis` is unknown: without
`--force` unadopt refuses and names it; with `--force` it leaves the unknown
path in place and reports it.

If `.aegis/project.json` is missing, `--force` scans AGENTS.md, CLAUDE.md and
the known optional host paths, prints `preview: <count> AEGIS block(s)`, then
removes the blocks and any known `.aegis` files. Without `--force`, missing
project metadata is an error when a block or known `.aegis` file remains. A
repository with neither metadata nor blocks is already unadopted and exits 0.
A second unadopt is a no-op.

Unadopt snapshots bytes and modes before changing or removing a file and rolls
back on failure, including interrupts. It makes no network call and never
removes a path it does not recognise without `--force`.

## Adopt/unadopt contract

| Guarantee | Behavior |
| --- | --- |
| Local only | No network, credentials, provider calls or telemetry. |
| Adopt idempotent | A second adopt with the same inputs writes the same bytes and keeps the original `adopted_at`. |
| Preservation | Bytes outside the marked block, file modes and newline styles are preserved; new files are `0o644` except the POSIX sh wrapper at `0o755`. |
| Exact block removal | Unadopt removes the marked block from the current bytes; it never restores a pre-adopt snapshot over later edits. A created file is removed only when nothing remains. |
| Known removals only | Unadopt removes the four known `.aegis` files, empty adopt-created marker files, and empty directories adopt created; unknown paths require `--force` and are left in place. |
| Transactional | Adopt and unadopt snapshot target bytes/modes and roll back on failure. |
| Schema gate | Normal unadopt requires `aegis.adopt/1`; `--force` is limited to missing project metadata with leftover blocks/known files. |

## Limits

- **No skills are copied.** Adoption points at the checkout; it does not copy
  `.claude/skills`, `docs`, or any other Aegis content into the repository.
- **A host can ignore startup files.** Writing `AGENTS.md`, `CLAUDE.md`,
  `.cursor/rules/aegis.mdc`, `.github/copilot-instructions.md` or `GEMINI.md`
  cannot force a host that does not read that file. Adoption also does not
  configure, install or authenticate any host.
- **The wrapper depends on the recorded absolute path.** If the checkout moves,
  rerun adopt. The wrapper also needs Python on `PATH`.
- **Doctor runs the trusted module, not the wrapper.** The `--version` check
  runs `tools.aegis_run` from the recorded checkout. Run doctor only on a
  repository whose recorded path you trust, and note that a successful version
  check does not prove the rest of the checkout works.
- **Host flags are recorded, not discovered.** A host file that exists without
  being recorded is not checked; doctor checks the flags in `project.json`.
- **Unadopt removes only what it knows.** It removes marked blocks from current
  bytes, created marker files only when empty, the four known `.aegis` files,
  and empty directories adopt created. Unknown `.aegis` paths require
  `--force` and are left in place; unadopt never guesses or deletes them.
- **Local only.** No network, credentials, provider calls or telemetry. The
  local process calls are `git rev-parse HEAD` when recording the checkout
  commit and the trusted `tools.aegis_run --version` check.
- **Not an approval.** PASS is not certification, readiness, delivery or merge
  permission, and it says nothing about any particular run record.

## Privacy

The metadata stores an absolute local checkout path, and the wrappers repeat it.
That path may reveal local directory names; review it before publishing an
adopted repository. Adoption writes nothing outside the repository named by
`--repo`. It reads that repository, the recorded checkout's
`tools/aegis_run/__main__.py`, and its local git HEAD. Doctor additionally runs
the recorded checkout's `tools.aegis_run` module with `--version`, but never a
wrapper. No secrets are read or written.

## Tests

```bash
python -P -B tools/aegis_adopt/tests/test_aegis_adopt.py
```

The tests use temporary consumer repositories and synthetic Aegis checkouts.
They cover a fresh adoption, a byte-identical second run, doctor PASS, missing
START-HERE, preserved `AGENTS.md` content, wrapper hashes, the cursor flag,
malformed and duplicate markers, fail-closed doctor cases, a no-op wrapper, an
extra side-effect wrapper line that is never run, mixed/CRLF content kept
byte-for-byte outside a CRLF block, non-UTF-8 marker-file rejection before any
write, preflight rejection of `.aegis`/AGENTS links and regular files at host
directories before any write, a read-only AGENTS target rejected before any
write, existing mode preservation, new `0o644` START-HERE, new `0o755` sh
wrapper, mode stability across a second adopt, a planted predictable
`<target>.tmp` link left untouched by atomic writes, rollback after an injected
write failure with originals restored, rollback on an injected
`KeyboardInterrupt` with the interrupt propagating, a missing recorded run
module, a trusted-module run that exits nonzero or prints nothing, no
`__pycache__` left behind, and a blocked `socket` during adopt and doctor.
Unadopt tests cover exact AGENTS restoration, CRLF preservation, optional host
block removal, a no-op second run, unknown `.aegis` refusal then `--force`
leaving it, malformed/wrong-schema project refusal, and `--force` with missing
project metadata, removal of empty AGENTS/CLAUDE files adopt created, removal
of created `.cursor`/`.github` directories when empty, and preservation of
user notes appended after adoption.

## Provenance

Reference implementation authored by DeepSeek (DeepSeek Harness) for the Aegis
Maturity Package. Model: DeepSeek.
