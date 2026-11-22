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
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
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
ARTIFACT_KINDS = ("log", "screenshot", "report", "note", "dataset", "other")
MANIFEST_ARTIFACT_FIELDS = ("path", "source", "bytes", "sha256", "portable", "external")
SCOPE = (
    "VERIFIED: record structure and copied artifact hashes only. "
    "NOT PROVEN: host/model identity, app correctness, security, delivery, "
    "universal support."
)
RFC3339_Z = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")

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
    line = json.dumps(event, sort_keys=True, ensure_ascii=False)
    with open(directory / EVENTS_NAME, "a", encoding="utf-8", newline="\n") as handle:
        handle.write(line + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    record["events"].append(event)
    _save_record(directory, record)
    print(
        "event %d: %s %s/%s"
        % (len(record["events"]), event["type"], event["stage"], event["status"])
    )
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
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except CliError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return EXIT_FAIL
