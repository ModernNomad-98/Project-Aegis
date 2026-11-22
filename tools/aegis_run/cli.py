"""Command-line interface for Aegis Run Record v1.

Local only: standard library, no network, no credentials, no provider calls.
It records one Aegis-assisted application run in D/aegis-run.json, mirrors
events into the append-only D/events.jsonl, copies artifacts into D/artifacts/
and hashes them, and exports D/aegis-run.json plus D/manifest.json for offline
verification.

Copied artifacts are the verification target and are always stored under
relative paths. --external references a file without copying it: such an entry
is nonportable and verify reports it as EXTERNAL/UNVERIFIED, failing unless
--allow-external is passed.

verify and export load docs/aegis-run/schema.json from the repository root and
enforce it with a standard-library schema-lite validator. A missing schema
fails closed as SCHEMA_MISSING. Exit codes: 0 success/PASS, 1 record failure or
verify FAIL (fail closed), 2 argument/usage failure.

Automatic project-state sync: sync imports unseen rows of the
"## State snapshots" table in a project-state file, keyed by the row ID in
source_id. On a first import every row except the latest becomes a type=note
event, and only the latest becomes type=stage, status=started; later rows become
type=stage, status=started. It never infers a passed stage. Sync holds an
exclusive lock file in the run directory, so concurrent runs cannot duplicate an
import. watch polls that file locally and repeats the same sync on change.
install-hook and uninstall-hook manage a local post-commit hook that calls sync.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import re
import shutil
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

from . import MANIFEST_SCHEMA, RECORD_SCHEMA, __version__

RECORD_NAME = "aegis-run.json"
MANIFEST_NAME = "manifest.json"
EVENTS_NAME = "events.jsonl"
ARTIFACTS_DIR = "artifacts"
SCHEMA_PATH = Path(__file__).resolve().parents[2] / "docs" / "aegis-run" / "schema.json"
EVENT_TYPES = ("stage", "approval", "note")
EVENT_STATUSES = ("started", "passed", "failed", "skipped")
OUTCOMES = ("delivered", "stopped", "failed")
SYNC_ACTOR = "project-state-sync"
SNAPSHOT_HEADING = "State snapshots"
MIN_WATCH_INTERVAL = 5
HOOK_NAME = "post-commit"
HOOK_MARKER = "AEGIS_RUN_HOOK_MARKER: aegis_run post-commit v1"
LOCK_NAME = "sync.lock"
LOCK_TIMEOUT_SECONDS = 5.0
LOCK_STALE_SECONDS = 120.0
ARTIFACT_KINDS = ("log", "screenshot", "report", "note", "dataset", "other")
MANIFEST_ARTIFACT_FIELDS = ("path", "source", "bytes", "sha256", "portable", "external")
SCOPE = (
    "VERIFIED: record structure and copied artifact hashes only. "
    "NOT PROVEN: host/model identity, app correctness, security, delivery, "
    "universal support."
)
RFC3339_Z = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")
SNAPSHOT_ID = re.compile(r"^SS-[0-9]{3,}$")

EXIT_OK = 0
EXIT_FAIL = 1


class CliError(Exception):
    """A local, user-facing failure. The CLI reports it and exits nonzero."""


class SchemaError(Exception):
    """The record schema could not be loaded or parsed."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False) + "\n"


def _atomic_write(path: Path, text: str) -> None:
    """Write text atomically: same-directory temp file, fsync, os.replace."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)


def _digest(path: Path) -> tuple[str, int]:
    hasher = hashlib.sha256()
    size = 0
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
            size += len(chunk)
    return hasher.hexdigest(), size


def _require_text(value: str, label: str) -> str:
    if not value or not value.strip():
        raise CliError("%s must not be empty" % label)
    return value


def _run_dir(value: str) -> Path:
    path = Path(value).expanduser().resolve()
    if not path.is_dir():
        raise CliError("run directory not found: %s" % path)
    return path


def _read_record(directory: Path) -> dict[str, Any]:
    path = directory / RECORD_NAME
    if not path.is_file():
        raise CliError("run record not found (run init first): %s" % path)
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CliError("run record is not valid UTF-8 JSON: %s" % exc) from exc
    if not isinstance(record, dict):
        raise CliError("run record must be a JSON object")
    return record


def _save_record(directory: Path, record: dict[str, Any]) -> None:
    _atomic_write(directory / RECORD_NAME, _canonical(record))


def _load_schema() -> dict[str, Any]:
    """Load the checked-in v1 schema; a missing or unreadable file fails closed."""
    try:
        raw = SCHEMA_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        raise SchemaError("SCHEMA_MISSING: %s (%s)" % (SCHEMA_PATH, exc)) from exc
    except UnicodeDecodeError as exc:
        raise SchemaError("SCHEMA_INVALID: %s (%s)" % (SCHEMA_PATH, exc)) from exc
    try:
        schema = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SchemaError("SCHEMA_INVALID: %s (%s)" % (SCHEMA_PATH, exc)) from exc
    if not isinstance(schema, dict):
        raise SchemaError("SCHEMA_INVALID: %s is not a JSON object" % SCHEMA_PATH)
    return schema


def _is_rfc3339_z(value: str) -> bool:
    if not RFC3339_Z.match(value):
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def _json_equal(left: Any, right: Any) -> bool:
    if isinstance(left, bool) != isinstance(right, bool):
        return False
    return left == right


def _matches_type(value: Any, name: str) -> bool:
    if name == "object":
        return isinstance(value, dict)
    if name == "array":
        return isinstance(value, list)
    if name == "string":
        return isinstance(value, str)
    if name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if name == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if name == "boolean":
        return isinstance(value, bool)
    if name == "null":
        return value is None
    return False


def _type_ok(value: Any, spec: Any) -> bool:
    names = spec if isinstance(spec, list) else [spec]
    return any(_matches_type(value, name) for name in names)


def _resolve_ref(root: dict[str, Any], reference: str) -> Any:
    if not isinstance(reference, str) or not reference.startswith("#/"):
        return None
    node: Any = root
    for part in reference[2:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


def _join(path: str, key: str) -> str:
    return "%s/%s" % (path, key) if path else key


def _validate_node(
    root: dict[str, Any],
    node: Any,
    value: Any,
    path: str,
    findings: list[str],
) -> None:
    """Validate one value against the subset of JSON Schema used by schema.json."""
    if not isinstance(node, dict):
        return
    if "$ref" in node:
        resolved = _resolve_ref(root, node["$ref"])
        if resolved is None:
            findings.append("schema: unresolved reference %r" % node["$ref"])
            return
        _validate_node(root, resolved, value, path, findings)
        return
    label = path or "record"
    if "const" in node and not _json_equal(value, node["const"]):
        findings.append("schema: %s must equal %r" % (label, node["const"]))
    if "enum" in node and not any(_json_equal(value, item) for item in node["enum"]):
        findings.append(
            "schema: %s must be one of %s" % (label, json.dumps(node["enum"], sort_keys=True))
        )
    if "type" in node and not _type_ok(value, node["type"]):
        findings.append("schema: %s must be of type %s" % (label, node["type"]))
        return
    if isinstance(value, str):
        if "minLength" in node and len(value) < node["minLength"]:
            findings.append(
                "schema: %s must be at least %d character(s)" % (label, node["minLength"])
            )
        if "pattern" in node:
            try:
                matched = re.search(node["pattern"], value)
            except re.error:
                matched = None
            if matched is None:
                findings.append("schema: %s must match pattern %s" % (label, node["pattern"]))
        if node.get("format") == "date-time" and not _is_rfc3339_z(value):
            findings.append("schema: %s must be an RFC3339 UTC timestamp ending Z" % label)
        elif node.get("format") == "uuid":
            try:
                uuid.UUID(value)
            except (ValueError, AttributeError, TypeError):
                findings.append("schema: %s must be a UUID" % label)
    if isinstance(value, int) and not isinstance(value, bool) and "minimum" in node:
        if value < node["minimum"]:
            findings.append("schema: %s must be >= %d" % (label, node["minimum"]))
    if isinstance(value, list):
        if "minItems" in node and len(value) < node["minItems"]:
            findings.append(
                "schema: %s must contain at least %d item(s)" % (label, node["minItems"])
            )
        if isinstance(node.get("items"), dict):
            for index, item in enumerate(value):
                _validate_node(root, node["items"], item, _join(path, str(index)), findings)
    if isinstance(value, dict):
        for key in node.get("required", []):
            if key not in value:
                findings.append("schema: missing required field: %s" % _join(path, key))
        properties = node.get("properties", {})
        for key, subschema in properties.items():
            if key in value:
                _validate_node(root, subschema, value[key], _join(path, key), findings)
        extra = node.get("additionalProperties", True)
        if extra is False:
            for key in value:
                if key not in properties:
                    findings.append("schema: unexpected property: %s" % _join(path, key))
        elif isinstance(extra, dict):
            for key in value:
                if key not in properties:
                    _validate_node(root, extra, value[key], _join(path, key), findings)


def _schema_findings(schema: dict[str, Any], record: dict[str, Any]) -> list[str]:
    """Apply schema.json plus the record-level rules the schema cannot express."""
    findings: list[str] = []
    _validate_node(schema, schema, record, "", findings)
    events = record.get("events")
    if isinstance(events, list) and not events:
        findings.append("schema: events must contain at least one entry")
    if isinstance(events, list):
        for index, event in enumerate(events):
            if not isinstance(event, dict) or "source_id" not in event:
                continue
            if event.get("actor") != SYNC_ACTOR:
                findings.append(
                    "schema: events/%d/source_id is only allowed on %s events"
                    % (index, SYNC_ACTOR)
                )
            value = event.get("source_id")
            if not isinstance(value, str) or not value.strip():
                findings.append(
                    "schema: events/%d/source_id must be a non-empty "
                    "string matching ^SS-[0-9]{3,}$" % index
                )
    limitations = record.get("limitations")
    if not isinstance(limitations, list) or not limitations:
        findings.append("schema: limitations must contain at least one entry")
    if record.get("outcome") is None:
        findings.append("schema: outcome must be delivered, stopped or failed")
    artifacts = record.get("artifacts")
    if isinstance(artifacts, list):
        for index, entry in enumerate(artifacts):
            if not isinstance(entry, dict):
                continue
            external = entry.get("external")
            portable = entry.get("portable")
            path = entry.get("path")
            if external is True:
                if path is not None:
                    findings.append(
                        "schema: artifacts/%d/path must be null when external is true" % index
                    )
                if portable is True:
                    findings.append(
                        "schema: artifacts/%d/portable must be false for an external reference"
                        % index
                    )
            elif external is False:
                if not isinstance(path, str) or not path:
                    findings.append(
                        "schema: artifacts/%d/path is required when external is false" % index
                    )
                if portable is not True:
                    findings.append(
                        "schema: artifacts/%d/portable must be true for a copied artifact" % index
                    )
    return findings


def _source_reference(directory: Path, target: Path) -> str:
    """Return a relative, slash-normalized reference to the original file.

    No absolute path is ever stored. Files outside the run directory are
    expressed relative to it, so the reference can begin with ../. When no
    relative path exists (for example another Windows volume), the file name
    alone is kept.
    """
    try:
        relative = target.relative_to(directory)
    except ValueError:
        try:
            relative = Path(os.path.relpath(target, directory))
        except ValueError:
            return target.name
    return relative.as_posix()


def _safe_name(name: str) -> str:
    cleaned = "".join(
        char if (char.isprintable() and char not in '/\\:*?"<>|') else "_"
        for char in name
    )
    cleaned = cleaned.strip(" .") or "artifact"
    return cleaned[:120]


def _copy_into_run(directory: Path, target: Path, sha256: str) -> Path:
    dest_dir = directory / ARTIFACTS_DIR
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / ("%s-%s" % (sha256[:12], _safe_name(target.name)))
    if dest.is_file():
        existing, _size = _digest(dest)
        if existing == sha256:
            return dest
    tmp = dest.with_name(dest.name + ".tmp")
    shutil.copyfile(target, tmp)
    os.replace(tmp, dest)
    return dest


def _artifact_entry(directory: Path, target: Path, kind: str | None, external: bool) -> dict[str, Any]:
    sha256, size = _digest(target)
    source = _source_reference(directory, target)
    if external:
        return {
            "path": None,
            "source": source,
            "bytes": size,
            "sha256": sha256,
            "portable": False,
            "external": True,
            "kind": kind,
        }
    copied = _copy_into_run(directory, target, sha256)
    relative = copied.relative_to(directory)
    return {
        "path": relative.as_posix(),
        "source": source,
        "bytes": size,
        "sha256": sha256,
        "portable": True,
        "external": False,
        "kind": kind,
    }


def cmd_init(args: argparse.Namespace) -> int:
    app = _require_text(args.app, "--app")
    commit = _require_text(args.aegis_commit, "--aegis-commit")
    host = _require_text(args.host, "--host")
    directory = Path(args.dir).expanduser().resolve()
    if directory.exists() and not directory.is_dir():
        raise CliError("run directory path is not a directory: %s" % directory)
    record_path = directory / RECORD_NAME
    if record_path.exists():
        raise CliError("refusing to overwrite existing record: %s" % record_path)
    try:
        directory.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise CliError("cannot create run directory %s: %s" % (directory, exc)) from exc
    record = {
        "schema": RECORD_SCHEMA,
        "run_id": str(uuid.uuid4()),
        "created_at": _now(),
        "app": app,
        "aegis_commit": commit,
        "host": host,
        "model": args.model or None,
        "owner": args.owner or None,
        "events": [],
        "artifacts": [],
        "limitations": [],
        "outcome": None,
    }
    _save_record(directory, record)
    _atomic_write(directory / EVENTS_NAME, "")
    print("initialized run %s in %s" % (record["run_id"], directory))
    return EXIT_OK


def _append_event(directory: Path, record: dict[str, Any], event: dict[str, Any]) -> None:
    """Append one event to events.jsonl, then mirror it into the record."""
    line = json.dumps(event, sort_keys=True, ensure_ascii=False)
    with open(directory / EVENTS_NAME, "a", encoding="utf-8", newline="\n") as handle:
        handle.write(line + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    record["events"].append(event)
    _save_record(directory, record)


def cmd_event(args: argparse.Namespace) -> int:
    directory = _run_dir(args.dir)
    record = _read_record(directory)
    stage = _require_text(args.stage, "--stage")
    event = {
        "ts": _now(),
        "type": args.type,
        "stage": stage,
        "status": args.status,
        "note": args.note,
        "actor": args.actor,
    }
    _append_event(directory, record, event)
    print(
        "event %d: %s %s/%s"
        % (len(record["events"]), event["type"], event["stage"], event["status"])
    )
    return EXIT_OK


# -- project-state sync and watch --------------------------------------


def _read_text(path: Path, label: str) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise CliError("%s is not valid UTF-8: %s" % (label, exc)) from exc
    except OSError as exc:
        raise CliError("cannot read %s %s: %s" % (label, path, exc)) from exc


def _project_state_file(value: str) -> Path:
    path = Path(value).expanduser().resolve()
    if not path.is_file():
        raise CliError("project-state file not found: %s" % path)
    return path


def _snapshot_section(text: str) -> list[str]:
    """Return the lines of the first '## State snapshots ...' section."""
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if not line.startswith("## "):
            continue
        title = line[3:].strip()
        if title == SNAPSHOT_HEADING or title.startswith(SNAPSHOT_HEADING + " "):
            start = index + 1
            break
    if start is None:
        raise CliError("project-state has no '## %s' section" % SNAPSHOT_HEADING)
    for index in range(start, len(lines)):
        if lines[index].startswith("## "):
            return lines[start:index]
    return lines[start:]


def _row_cells(line: str) -> list[str]:
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [cell.strip() for cell in body.split("|")]


_PLACEHOLDER_CELLS = {"", "-", "\u2014", "(none yet)", "(none recorded)"}


def _valid_snapshot_date(value: str) -> bool:
    token = value.split()[0] if value.split() else ""
    try:
        datetime.strptime(token, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def _parse_snapshots(text: str) -> list[dict[str, str]]:
    """Parse the State snapshots table; a structural problem is a CliError."""
    rows = [line for line in _snapshot_section(text) if line.strip().startswith("|")]
    if not rows:
        raise CliError("project-state has no State snapshots table")
    header = _row_cells(rows[0])
    if (
        len(header) != 4
        or header[0].lower() != "id"
        or "date" not in header[1].lower()
        or "stage" not in header[2].lower()
        or "next" not in header[3].lower()
    ):
        raise CliError(
            "project-state State snapshots header must be "
            "'| ID | Date | Current stage | Next recommended action |'"
        )
    if len(rows) < 2 or not all(
        re.fullmatch(r":?-{2,}:?", cell) for cell in _row_cells(rows[1])
    ):
        raise CliError("project-state State snapshots table has no header separator row")
    snapshots: list[dict[str, str]] = []
    for line in rows[2:]:
        cells = _row_cells(line)
        if all(cell in _PLACEHOLDER_CELLS for cell in cells):
            continue
        if len(cells) != 4:
            raise CliError(
                "malformed State snapshots row (expected 4 columns): %s" % line.strip()
            )
        snapshot_id, date, stage, next_action = cells
        if snapshot_id in _PLACEHOLDER_CELLS:
            raise CliError(
                "malformed State snapshots row (missing ID): %s" % line.strip()
            )
        if not SNAPSHOT_ID.match(snapshot_id):
            raise CliError(
                "malformed State snapshots row (ID must match SS- followed by at "
                "least three digits): %s" % line.strip()
            )
        if not _valid_snapshot_date(date):
            raise CliError(
                "malformed State snapshots row %s (missing or invalid date)" % snapshot_id
            )
        if not stage:
            raise CliError("malformed State snapshots row %s (missing stage)" % snapshot_id)
        if not next_action:
            raise CliError(
                "malformed State snapshots row %s (missing next action)" % snapshot_id
            )
        snapshots.append(
            {"id": snapshot_id, "date": date, "stage": stage, "next": next_action}
        )
    return snapshots


def _historical_event(snapshot: dict[str, str]) -> dict[str, Any]:
    """An older snapshot from the first import: history, never a live claim."""
    return {
        "ts": _now(),
        "type": "note",
        "stage": snapshot["stage"],
        "status": "started",
        "note": "historical snapshot %s imported from project-state; not observed live"
        % snapshot["id"],
        "actor": SYNC_ACTOR,
        "source_id": snapshot["id"],
    }


def _current_event(snapshot: dict[str, str]) -> dict[str, Any]:
    """The latest snapshot: the current stage, started, never passed."""
    return {
        "ts": _now(),
        "type": "stage",
        "stage": snapshot["stage"],
        "status": "started",
        "note": "Imported from project-state; next: %s" % snapshot["next"],
        "actor": SYNC_ACTOR,
        "source_id": snapshot["id"],
    }


def _imported_snapshot_ids(events: Any) -> set[str]:
    if not isinstance(events, list):
        return set()
    return {
        event["source_id"]
        for event in events
        if isinstance(event, dict) and isinstance(event.get("source_id"), str)
    }


def _lock_is_stale(path: Path) -> bool:
    try:
        return (time.time() - path.stat().st_mtime) > LOCK_STALE_SECONDS
    except OSError:
        return False


@contextlib.contextmanager
def _sync_lock(directory: Path):
    """Exclusive single-writer lock in the run directory; always released."""
    path = directory / LOCK_NAME
    deadline = time.monotonic() + LOCK_TIMEOUT_SECONDS
    while True:
        try:
            handle = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            if _lock_is_stale(path):
                raise CliError(
                    "stale sync lock older than %ds: %s "
                    "(remove it manually if no sync is running)"
                    % (LOCK_STALE_SECONDS, path)
                )
            if time.monotonic() >= deadline:
                raise CliError(
                    "sync lock is held (another sync is running?): %s" % path
                )
            time.sleep(0.05)
            continue
        except OSError as exc:
            raise CliError("cannot create sync lock %s: %s" % (path, exc)) from exc
        try:
            os.write(handle, ("%d\n" % os.getpid()).encode("ascii"))
        finally:
            os.close(handle)
        break
    try:
        yield
    finally:
        try:
            path.unlink()
        except OSError:
            pass


def _pending_snapshots(
    record: dict[str, Any], snapshots: list[dict[str, str]]
) -> tuple[list[dict[str, str]], bool]:
    """Return unseen snapshots and whether this is the first import."""
    seen = _imported_snapshot_ids(record.get("events"))
    first_import = not seen
    pending: list[dict[str, str]] = []
    for snapshot in snapshots:
        if snapshot["id"] in seen:
            continue
        seen.add(snapshot["id"])
        pending.append(snapshot)
    return pending, first_import


def _apply_sync(
    directory: Path,
    record: dict[str, Any],
    snapshots: list[dict[str, str]],
    dry_run: bool,
) -> tuple[int, int]:
    pending, first_import = _pending_snapshots(record, snapshots)
    for index, snapshot in enumerate(pending):
        historical = first_import and index < len(pending) - 1
        kind = "note" if historical else "stage"
        if dry_run:
            print(
                "dry-run: would append %s type=%s status=started stage=%s"
                % (snapshot["id"], kind, snapshot["stage"])
            )
            continue
        event = _historical_event(snapshot) if historical else _current_event(snapshot)
        _append_event(directory, record, event)
        print(
            "appended %s type=%s status=started stage=%s"
            % (snapshot["id"], event["type"], snapshot["stage"])
        )
    return len(pending), len(snapshots) - len(pending)


def cmd_sync(args: argparse.Namespace) -> int:
    directory = _run_dir(args.dir)
    state = _project_state_file(args.project_state)
    snapshots = _parse_snapshots(_read_text(state, "project-state"))
    if getattr(args, "dry_run", False):
        pending, already = _apply_sync(directory, _read_record(directory), snapshots, True)
        print(
            "sync: dry-run, %d would append, %d already imported, 0 written"
            % (pending, already)
        )
        return EXIT_OK
    with _sync_lock(directory):
        pending, already = _apply_sync(directory, _read_record(directory), snapshots, False)
    print("sync: %d new, %d already imported" % (pending, already))
    return EXIT_OK


def _watch_interval(value: float) -> float:
    if value < MIN_WATCH_INTERVAL:
        print(
            "note: --interval %g is below the %ds minimum; using %ds"
            % (value, MIN_WATCH_INTERVAL, MIN_WATCH_INTERVAL),
            file=sys.stderr,
        )
        return float(MIN_WATCH_INTERVAL)
    return float(value)


def _mtime(path: Path) -> float | None:
    try:
        return path.stat().st_mtime
    except OSError:
        return None


def _watch_once(args: argparse.Namespace, last: float | None) -> tuple[float | None, bool]:
    """Poll the mtime once and run the same sync on change. Not a loop."""
    state = Path(args.project_state).expanduser().resolve()
    current = _mtime(state)
    if current is None:
        if last is not None:
            print("warning: project-state is not readable: %s" % state, file=sys.stderr)
        return current, False
    if last is not None and current == last:
        return last, False
    print("changed: %s" % state)
    cmd_sync(args)
    return current, True


def cmd_watch(args: argparse.Namespace) -> int:
    interval = _watch_interval(args.interval)
    state = _project_state_file(args.project_state)
    _run_dir(args.dir)
    print("watching %s every %gs (Ctrl-C to stop); local only" % (state, interval))
    last = _mtime(state)
    try:
        while True:
            time.sleep(interval)
            try:
                last, _ran = _watch_once(args, last)
            except CliError as exc:
                print("error: %s" % exc, file=sys.stderr)
    except KeyboardInterrupt:
        print("")
        print("watch stopped")
        return EXIT_OK


# -- post-commit hook --------------------------------------------------


def _sh_quote(value: object) -> str:
    """Quote one value for POSIX sh; single quotes, safely escaped."""
    return "'" + str(value).replace("'", "'\\''") + "'"


def _hook_path(path: Path) -> str:
    """Absolute path with forward slashes, so a POSIX sh hook reads it literally."""
    return Path(path).as_posix()


def _hook_script(directory: Path, state: Path, aegis_path: Path) -> str:
    lines = [
        "#!/bin/sh",
        "# %s" % HOOK_MARKER,
        "# Installed by 'python -m tools.aegis_run install-hook'; local files only.",
        "# Remove with 'python -m tools.aegis_run uninstall-hook --repo <repo>'.",
        "cd %s || exit 0" % _sh_quote(_hook_path(aegis_path)),
        "PYTHONPATH=%s" % _sh_quote(_hook_path(aegis_path)),
        "export PYTHONPATH",
        "python -P -m tools.aegis_run sync --dir %s --project-state %s || :"
        % (_sh_quote(_hook_path(directory)), _sh_quote(_hook_path(state))),
        "printf '%s\\n' 'aegis_run: project-state sync after commit (local only;"
        " the commit is never blocked)'",
        "exit 0",
        "",
    ]
    return "\n".join(lines)


def _hook_owns(path: Path) -> bool:
    try:
        return HOOK_MARKER in _read_text(path, "hook")
    except CliError:
        return False


def _git_repo(value: str) -> Path:
    repo = Path(value).expanduser().resolve()
    if not repo.is_dir():
        raise CliError("repository not found: %s" % repo)
    if not (repo / ".git").exists():
        raise CliError("not a git repository (no .git): %s" % repo)
    return repo


def cmd_install_hook(args: argparse.Namespace) -> int:
    repo = _git_repo(args.repo)
    directory = _run_dir(args.dir)
    state = _project_state_file(args.project_state)
    aegis_path = Path(args.aegis_path).expanduser().resolve()
    if not aegis_path.is_dir():
        raise CliError("Aegis checkout not found: %s" % aegis_path)
    hooks = repo / ".git" / "hooks"
    try:
        hooks.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise CliError("cannot create hooks directory %s: %s" % (hooks, exc)) from exc
    hook = hooks / HOOK_NAME
    if hook.exists() and not _hook_owns(hook):
        if not args.force:
            raise CliError(
                "refusing to replace a post-commit hook aegis_run did not write: %s "
                "(rerun with --force to back it up)" % hook
            )
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        backup = hook.with_name("%s.bak-%s" % (HOOK_NAME, stamp))
        try:
            os.replace(hook, backup)
        except OSError as exc:
            raise CliError("cannot back up existing hook %s: %s" % (hook, exc)) from exc
        print("backed up existing hook: %s" % backup)
    _atomic_write(hook, _hook_script(directory, state, aegis_path))
    try:
        os.chmod(hook, 0o755)
    except OSError as exc:
        raise CliError("hook written but not made executable: %s (%s)" % (hook, exc)) from exc
    print("installed post-commit hook: %s" % hook)
    return EXIT_OK


def cmd_uninstall_hook(args: argparse.Namespace) -> int:
    repo = _git_repo(args.repo)
    hook = repo / ".git" / "hooks" / HOOK_NAME
    if not hook.exists():
        raise CliError("no post-commit hook installed: %s" % hook)
    if not _hook_owns(hook):
        raise CliError(
            "refusing to remove a post-commit hook aegis_run did not write: %s" % hook
        )
    try:
        hook.unlink()
    except OSError as exc:
        raise CliError("cannot remove hook %s: %s" % (hook, exc)) from exc
    print("removed post-commit hook: %s" % hook)
    return EXIT_OK


def cmd_artifact(args: argparse.Namespace) -> int:
    directory = _run_dir(args.dir)
    record = _read_record(directory)
    target = Path(args.path).expanduser()
    if not target.is_absolute():
        target = Path.cwd() / target
    target = target.resolve()
    if not target.is_file():
        raise CliError("artifact not found: %s" % target)
    reserved = {
        directory / RECORD_NAME,
        directory / MANIFEST_NAME,
        directory / EVENTS_NAME,
    }
    if target in reserved:
        raise CliError("refusing to record a run-record file as an artifact: %s" % target.name)
    entry = _artifact_entry(directory, target, args.kind, args.external)
    artifacts = [item for item in record["artifacts"] if item.get("source") != entry["source"]]
    artifacts.append(entry)
    record["artifacts"] = artifacts
    _save_record(directory, record)
    print(
        "artifact source=%s path=%s bytes=%d sha256=%s portable=%s external=%s"
        % (
            entry["source"],
            entry["path"],
            entry["bytes"],
            entry["sha256"],
            str(entry["portable"]).lower(),
            str(entry["external"]).lower(),
        )
    )
    return EXIT_OK


def cmd_finish(args: argparse.Namespace) -> int:
    directory = _run_dir(args.dir)
    record = _read_record(directory)
    if record.get("outcome") is not None:
        raise CliError("run already finished with outcome %r" % record.get("outcome"))
    limitations = [value.strip() for value in args.limitation if value.strip()]
    if not limitations:
        raise CliError("--limitation must contain at least one non-empty value")
    record["outcome"] = args.outcome
    record["limitations"] = limitations
    _save_record(directory, record)
    print("finished: %s (%d limitation(s))" % (args.outcome, len(limitations)))
    return EXIT_OK


def cmd_export(args: argparse.Namespace) -> int:
    try:
        schema = _load_schema()
    except SchemaError as exc:
        raise CliError(str(exc)) from exc
    directory = _run_dir(args.dir)
    record = _read_record(directory)
    if record.get("outcome") is None:
        raise CliError("export requires a finished run; run finish first")
    problems = _schema_findings(schema, record)
    if problems:
        raise CliError(
            "record does not satisfy %s:\n  %s" % (RECORD_SCHEMA, "\n  ".join(problems))
        )
    for entry in record["artifacts"]:
        if entry.get("external"):
            print(
                "warning: external artifact %s is not copied; this record is not portable"
                % entry.get("source"),
                file=sys.stderr,
            )
    record_text = _canonical(record)
    record_path = directory / RECORD_NAME
    _atomic_write(record_path, record_text)
    record_sha256 = hashlib.sha256(record_text.encode("utf-8")).hexdigest()
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "record": RECORD_NAME,
        "record_sha256": record_sha256,
        "artifacts": [
            {field: item[field] for field in MANIFEST_ARTIFACT_FIELDS}
            for item in record["artifacts"]
        ],
    }
    manifest_path = directory / MANIFEST_NAME
    _atomic_write(manifest_path, _canonical(manifest))
    print(record_path)
    print(manifest_path)
    return EXIT_OK


def _has_symlink_component(directory: Path, relative: Path) -> bool:
    current = directory
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            return True
    return False


def _check_artifact(
    directory: Path, entry: Any, findings: list[str], allow_external: bool
) -> int:
    """Check copied artifact path safety and bytes; return accepted external count."""
    if not isinstance(entry, dict):
        return 0
    source = entry.get("source")
    if isinstance(source, str) and Path(source).is_absolute():
        findings.append("artifact source must not be an absolute path: %s" % source)
    if entry.get("external") is True:
        if not allow_external:
            findings.append(
                "EXTERNAL artifact %s is UNVERIFIED (not copied; "
                "rerun verify with --allow-external to accept)" % source
            )
            return 0
        return 1
    label = entry.get("path")
    if not isinstance(label, str) or not label:
        return 0
    path = Path(label)
    if path.is_absolute():
        findings.append("artifact copied path must not be absolute: %s" % label)
        return 0
    if ".." in path.parts:
        findings.append("artifact copied path escapes the run directory: %s" % label)
        return 0
    if _has_symlink_component(directory, path):
        findings.append("artifact copied path uses a symbolic link: %s" % label)
        return 0
    target = (directory / path).resolve()
    try:
        target.relative_to(directory)
    except ValueError:
        findings.append("artifact copied path escapes the run directory: %s" % label)
        return 0
    if not target.is_file():
        findings.append("artifact missing: %s" % label)
        return 0
    actual_sha256, actual_size = _digest(target)
    if actual_sha256 != entry.get("sha256"):
        findings.append(
            "artifact sha256 mismatch: %s (recorded %s, actual %s)"
            % (label, entry.get("sha256"), actual_sha256)
        )
    if actual_size != entry.get("bytes"):
        findings.append(
            "artifact byte-size mismatch: %s (recorded %r, actual %d)"
            % (label, entry.get("bytes"), actual_size)
        )
    return 0


def _check_mirror(directory: Path, events: list[Any], findings: list[str]) -> None:
    path = directory / EVENTS_NAME
    if not path.is_file():
        if events:
            findings.append("missing event log: %s" % EVENTS_NAME)
        return
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        findings.append("event log is not valid UTF-8: %s" % EVENTS_NAME)
        return
    except OSError as exc:
        findings.append("event log is unreadable: %s" % exc)
        return
    appended = []
    for number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            appended.append(json.loads(line))
        except json.JSONDecodeError:
            findings.append("event log line %d is not valid JSON" % number)
            return
    if appended != events:
        findings.append("event state does not mirror %s" % EVENTS_NAME)


def cmd_verify(args: argparse.Namespace) -> int:
    directory = Path(args.dir).expanduser().resolve()
    try:
        schema = _load_schema()
    except SchemaError as exc:
        return _report([str(exc)])
    findings: list[str] = []
    record_path = directory / RECORD_NAME
    manifest_path = directory / MANIFEST_NAME
    record: Any = None
    if not record_path.is_file():
        findings.append("missing record: %s" % RECORD_NAME)
    if not manifest_path.is_file():
        findings.append("missing manifest: %s" % MANIFEST_NAME)
    if findings:
        return _report(findings)
    raw = record_path.read_bytes()
    try:
        record = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        findings.append("record is not valid UTF-8 JSON: %s" % exc)
        return _report(findings)
    if not isinstance(record, dict):
        findings.append("record must be a JSON object")
        return _report(findings)
    findings.extend(_schema_findings(schema, record))
    events = record.get("events")
    if isinstance(events, list):
        _check_mirror(directory, events, findings)
    artifacts = record.get("artifacts")
    accepted_external = 0
    if isinstance(artifacts, list):
        for entry in artifacts:
            accepted_external += _check_artifact(
                directory, entry, findings, bool(args.allow_external)
            )
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        findings.append("manifest is not valid UTF-8 JSON: %s" % exc)
        manifest = None
    if manifest is not None:
        if not isinstance(manifest, dict):
            findings.append("manifest must be a JSON object")
        else:
            if manifest.get("schema") != MANIFEST_SCHEMA:
                findings.append(
                    "manifest schema must be %s, got %r"
                    % (MANIFEST_SCHEMA, manifest.get("schema"))
                )
            if manifest.get("record") != RECORD_NAME:
                findings.append("manifest record must be %r" % RECORD_NAME)
            expected = hashlib.sha256(raw).hexdigest()
            if manifest.get("record_sha256") != expected:
                findings.append(
                    "record_sha256 mismatch (manifest %r, actual %s)"
                    % (manifest.get("record_sha256"), expected)
                )
            if isinstance(manifest.get("artifacts"), list) and isinstance(artifacts, list):
                projected = [
                    {field: item.get(field) for field in MANIFEST_ARTIFACT_FIELDS}
                    for item in artifacts
                    if isinstance(item, dict)
                ]
                if manifest["artifacts"] != projected:
                    findings.append("manifest artifacts do not match the record artifacts")
            else:
                findings.append("manifest artifacts must be a list")
    if findings:
        return _report(findings)
    print("PASS")
    print(SCOPE)
    if accepted_external:
        print(
            "EXTERNAL: %d reference(s) accepted via --allow-external and remain UNVERIFIED."
            % accepted_external
        )
    return EXIT_OK


def _report(findings: list[str]) -> int:
    for finding in findings:
        print("FAIL: %s" % finding)
    print("FAIL: %d finding(s)" % len(findings))
    print(SCOPE)
    return EXIT_FAIL


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aegis_run",
        description=(
            "Record one Aegis-assisted application run, copy and hash its artifacts, "
            "and export a verifiable record plus manifest. Local files only."
        ),
    )
    parser.add_argument("--version", action="version", version="aegis_run %s" % __version__)
    subparsers = parser.add_subparsers(dest="command", required=True, metavar="COMMAND")

    init = subparsers.add_parser("init", help="create a run directory and record")
    init.add_argument("--dir", required=True, metavar="D")
    init.add_argument("--app", required=True, metavar="NAME")
    init.add_argument("--aegis-commit", required=True, metavar="SHA")
    init.add_argument("--host", required=True, metavar="HOST")
    init.add_argument("--model", default=None, metavar="M")
    init.add_argument("--owner", default=None, metavar="O")
    init.set_defaults(func=cmd_init)

    event = subparsers.add_parser("event", help="append an event to the run")
    event.add_argument("--dir", required=True, metavar="D")
    event.add_argument("--type", required=True, choices=EVENT_TYPES)
    event.add_argument("--stage", required=True, metavar="N")
    event.add_argument("--status", required=True, choices=EVENT_STATUSES)
    event.add_argument("--note", default=None, metavar="TEXT")
    event.add_argument("--actor", default=None, metavar="A")
    event.set_defaults(func=cmd_event)

    artifact = subparsers.add_parser("artifact", help="copy and hash a file into the record")
    artifact.add_argument("--dir", required=True, metavar="D")
    artifact.add_argument("--path", required=True, metavar="FILE")
    artifact.add_argument("--kind", default=None, choices=ARTIFACT_KINDS, metavar="KIND")
    artifact.add_argument(
        "--external",
        action="store_true",
        help="reference without copying; makes the record nonportable",
    )
    artifact.set_defaults(func=cmd_artifact)

    finish = subparsers.add_parser("finish", help="record the outcome and limitations")
    finish.add_argument("--dir", required=True, metavar="D")
    finish.add_argument("--outcome", required=True, choices=OUTCOMES)
    finish.add_argument("--limitation", required=True, action="append", metavar="TEXT")
    finish.set_defaults(func=cmd_finish)

    export = subparsers.add_parser("export", help="write aegis-run.json and manifest.json")
    export.add_argument("--dir", required=True, metavar="D")
    export.set_defaults(func=cmd_export)

    verify = subparsers.add_parser("verify", help="recompute hashes and fail closed")
    verify.add_argument("--dir", required=True, metavar="D")
    verify.add_argument(
        "--allow-external",
        action="store_true",
        help="accept EXTERNAL/UNVERIFIED references instead of failing",
    )
    verify.set_defaults(func=cmd_verify)

    sync = subparsers.add_parser(
        "sync", help="import new project-state snapshots as started stage events"
    )
    sync.add_argument("--dir", required=True, metavar="D")
    sync.add_argument("--project-state", required=True, metavar="PATH")
    sync.add_argument(
        "--dry-run",
        action="store_true",
        help="print what would append and write nothing",
    )
    sync.set_defaults(func=cmd_sync)

    watch = subparsers.add_parser(
        "watch", help="poll project-state and run sync on change (Ctrl-C stops)"
    )
    watch.add_argument("--dir", required=True, metavar="D")
    watch.add_argument("--project-state", required=True, metavar="PATH")
    watch.add_argument(
        "--interval",
        type=float,
        default=30.0,
        metavar="SECONDS",
        help="poll interval in seconds (minimum 5)",
    )
    watch.set_defaults(func=cmd_watch)

    install = subparsers.add_parser(
        "install-hook", help="install a post-commit hook that runs sync"
    )
    install.add_argument("--repo", required=True, metavar="PATH")
    install.add_argument("--dir", required=True, metavar="D")
    install.add_argument("--project-state", required=True, metavar="PATH")
    install.add_argument("--aegis-path", required=True, metavar="PATH")
    install.add_argument(
        "--force",
        action="store_true",
        help="back up and replace an existing post-commit hook",
    )
    install.set_defaults(func=cmd_install_hook)

    uninstall = subparsers.add_parser(
        "uninstall-hook", help="remove the post-commit hook aegis_run installed"
    )
    uninstall.add_argument("--repo", required=True, metavar="PATH")
    uninstall.set_defaults(func=cmd_uninstall_hook)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except CliError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return EXIT_FAIL
