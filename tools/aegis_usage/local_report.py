#!/usr/bin/env python3
"""Local, opt-in workflow-outcomes reporter for Project Aegis.

Offline by construction: this module imports no networking module, starts no
thread and no subprocess. It keeps minimized, allowlisted workflow-outcome
transitions in a local JSON store and writes an export only after the exact
bytes were previewed and the preview handle was confirmed. Capture is off by
default and enabled per workflow by explicit opt-in.

The contract is docs/instrumentation/workflow-outcomes-v1.schema.json. No
field may carry an identity, prompt, output, code, project/repository/path
name, content hash or free text; every string is an allowlisted enum, a
day-precision date or a random reference.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import secrets
import stat
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

SCHEMA_NAME = "workflow-outcomes-v1"
SUPPORTED_LIBRARY_REVISIONS = ("1.0.0",)
SUPPORTED_CONSENT_POLICIES = ("1",)
CAPTURE_TIER = "self_report"
REPORTING_WINDOW_DAYS = 30
LAG_DAYS = 7
MAX_SNAPSHOT_BYTES = 64 * 1024
MAX_TRANSITIONS = 256
LOCAL_RETENTION_DAYS = 60
STORE_VERSION = 1

STAGES = ("discover", "plan", "build", "validate", "deliver")
STAGE_STATUSES = ("not_started", "in_progress", "complete", "not_applicable", "unknown")
STATUSES = ("ongoing", "delivered", "failed", "abandoned", "unknown")
ACCEPTANCE = (
    "not_assessed",
    "self_reported_pass",
    "self_reported_fail",
    "independent_attested_pass",
    "independent_attested_fail",
)
ACCEPTANCE_EVIDENCE = ("none", "local_checklist", "local_test_record", "local_review_record")
EVENT_KINDS = ("status", "stage", "acceptance", "scope_change", "observation")
TERMINAL_STATUSES = ("delivered", "failed", "abandoned")
EVENT_VALUES = {
    "status": TERMINAL_STATUSES,
    "stage": STAGE_STATUSES,
    "acceptance": ACCEPTANCE,
    "scope_change": ("criteria_changed",),
    "observation": ("ongoing", "unknown"),
}
REF_PREFIXES = {
    "workflow_ref": "wf-",
    "export_ref": "exp-",
    "admission_ref": "adm-",
    "event_ref": "evt-",
    "criteria_contract_ref": "crit-",
}
REF_RE = re.compile(r"^(wf|exp|adm|evt|crit)-[0-9a-f]{32}$")
DAY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

TOP_KEYS = (
    "schema",
    "library_revision",
    "capture_tier",
    "consent_policy_version",
    "reporting_window_days",
    "admission_ref",
    "snapshot",
)
SNAPSHOT_KEYS = (
    "workflow_ref",
    "revision",
    "export_ref",
    "start_day",
    "last_observed_day",
    "report_due_day",
    "applicable_stages",
    "criteria_frozen_before_work",
    "criteria_contract_ref",
    "stage_status",
    "status",
    "acceptance",
    "acceptance_evidence",
    "delivery_day",
    "acceptance_day",
    "transitions",
)
TRANSITION_KEYS = ("event_ref", "kind", "effective_day", "value", "stage")

# The only key names the contract allows. An error path may echo these; any
# other key is attacker-chosen input and is replaced by "<key>" before it can
# reach a log line. FORBIDDEN_KEYS is itself a fixed vocabulary, so its
# canonical (lower-case) names are safe to report.
CONTRACT_KEY_NAMES = frozenset(TOP_KEYS + SNAPSHOT_KEYS + TRANSITION_KEYS + STAGES)

# Defense in depth: these keys are never part of the contract at any depth. A
# payload carrying one is rejected with its own error code so a leak is loud,
# not merely "unknown field".
FORBIDDEN_KEYS = frozenset(
    {
        "prompt",
        "prompts",
        "output",
        "outputs",
        "code",
        "source_code",
        "project",
        "project_name",
        "repository",
        "repo",
        "path",
        "file",
        "file_path",
        "filename",
        "url",
        "urls",
        "account",
        "account_id",
        "email",
        "name",
        "user",
        "user_id",
        "username",
        "host",
        "hostname",
        "device",
        "device_id",
        "machine",
        "ip",
        "ip_address",
        "content",
        "content_hash",
        "content_sha256",
        "sha256",
        "hash",
        "reason",
        "reasons",
        "notes",
        "note",
        "memo",
        "free_text",
        "text",
        "message",
        "description",
        "title",
        "comment",
        "comments",
        "ticket",
        "issue",
        "branch",
        "commit",
        "organization",
        "author",
        "reviewer",
    }
)


class ContractError(Exception):
    """A payload or local-state violation with a stable machine code."""

    def __init__(self, code: str, message: str, path: str = "") -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.path = path

    def as_dict(self) -> dict:
        result = {"code": self.code, "message": self.message}
        if self.path:
            result["path"] = self.path
        return result


def _fail(code: str, message: str, path: str = "") -> None:
    raise ContractError(code, message, path)


# --------------------------------------------------------------------------
# Date, reference and size helpers
# --------------------------------------------------------------------------


def parse_day(value: object, path: str) -> date:
    if not isinstance(value, str) or not DAY_RE.fullmatch(value):
        _fail("invalid_date", "expected a day-precision date YYYY-MM-DD", path)
    try:
        return date.fromisoformat(value)
    except ValueError:
        _fail("invalid_date", "not a real calendar day", path)
    raise AssertionError("unreachable")


def day_str(value: date) -> str:
    return value.isoformat()


def random_ref(prefix: str) -> str:
    return prefix + secrets.token_hex(16)


def parse_ref(value: object, path: str, prefix: str) -> str:
    if not isinstance(value, str) or not REF_RE.fullmatch(value) or not value.startswith(prefix):
        _fail("invalid_ref", "expected a random reference beginning " + prefix, path)
    return value


def canonical_bytes(payload: dict) -> bytes:
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return (text + "\n").encode("utf-8")


def bytes_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


FILE_MODE = 0o600
DIR_MODE = 0o700


def _repository_root(path: Path) -> Path | None:
    """Nearest ancestor with a .git entry, or None outside a working tree.

    A source archive has no .git; callers therefore also refuse a target
    inside the tool's own source tree, so an archive copy fails closed for
    in-tree targets instead of silently writing there.
    """
    for candidate in [path] + list(path.parents):
        if (candidate / ".git").exists():
            return candidate
    return None


def _tool_root() -> Path | None:
    resolved = Path(__file__).resolve()
    if resolved.parent.name == "aegis_usage":
        return resolved.parents[2]
    return None


def _inside_reporting_tree(resolved: Path, repo_root: Path | None = None) -> bool:
    """True when a resolved path sits inside version control or the tool tree.

    The repository root is looked up from the resolved target itself, walking
    its lexical ancestors, not from the current directory. A missing target
    parent must never move the check to the caller's working directory: that
    would let a path such as '<other-checkout>/missing_dir/export.json' be
    created inside another Git working tree.
    """
    root = repo_root if repo_root is not None else _repository_root(resolved)
    if root is not None and (resolved == root or root in resolved.parents):
        return True
    tool_root = _tool_root()
    return tool_root is not None and (resolved == tool_root or tool_root in resolved.parents)


def guard_store_path(path: Path) -> None:
    """Refuse a reporting store inside project version control."""
    if _inside_reporting_tree(Path(path).resolve()):
        _fail("store_path_in_repository", "reporting data must stay outside project version control", str(path))


def _ensure_private_dir(path: Path) -> None:
    """Create missing directories with user-only access, whatever the umask.

    Only directories this call creates are re-moded; an existing parent (a
    home directory or a system temp directory) is left as its owner set it.
    """
    missing: list[Path] = []
    current = path
    while not current.exists():
        missing.append(current)
        if current.parent == current:
            break
        current = current.parent
    for directory in reversed(missing):
        try:
            directory.mkdir(mode=DIR_MODE)
        except FileExistsError:
            continue
        if os.name == "posix":
            os.chmod(directory, DIR_MODE)


def _write_private_bytes(path: Path, data: bytes, *, exclusive: bool) -> None:
    """Create or replace one file readable only by its owner (POSIX 0600)."""
    flags = os.O_WRONLY | os.O_CREAT | (os.O_EXCL if exclusive else os.O_TRUNC)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags, FILE_MODE)
    try:
        if os.name == "posix":
            os.fchmod(descriptor, FILE_MODE)
        with os.fdopen(descriptor, "wb") as stream:
            descriptor = -1
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    if os.name == "posix":
        os.chmod(path, FILE_MODE)


def write_private_store(path: Path, text: str) -> None:
    """Atomically replace a store with a user-only file under private parents.

    The temporary file is created with an unpredictable name and O_EXCL by
    tempfile.mkstemp in the destination directory, so a pre-created
    store.tmp symlink (for example in a shared writable directory) is never
    followed. On Windows an existing read-only store is made writable
    immediately before the atomic replace, because the read-only attribute
    otherwise makes os.replace fail.
    """
    path = Path(path)
    guard_store_path(path)
    _ensure_private_dir(path.parent)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=path.name + ".", suffix=".tmp", dir=str(path.parent)
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            descriptor = -1
            if os.name == "posix":
                os.fchmod(stream.fileno(), FILE_MODE)
            stream.write(text.encode("utf-8"))
            stream.flush()
            os.fsync(stream.fileno())
        if os.name == "nt" and path.exists():
            os.chmod(path, stat.S_IWRITE)
        os.replace(temporary, path)
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        if temporary.exists():
            temporary.unlink()
    if os.name == "posix":
        os.chmod(path, FILE_MODE)


# --------------------------------------------------------------------------
# Contract validation
# --------------------------------------------------------------------------


MAX_NESTING_DEPTH = 64


def _assert_nesting(node: object) -> None:
    """Refuse a payload deeper than the contract bound without recursing."""
    stack = [(node, 0)]
    while stack:
        current, depth = stack.pop()
        if depth > MAX_NESTING_DEPTH:
            _fail("invalid_nesting", "the payload nesting is too deep", "")
        if isinstance(current, dict):
            stack.extend((value, depth + 1) for value in current.values())
        elif isinstance(current, list):
            stack.extend((value, depth + 1) for value in current)


def _reported_key(key: object) -> str:
    """Return a path segment that is safe to put in an error message.

    The walk runs before the key allowlist, so an ancestor key can be any
    attacker-chosen string (for example an email address). Only the contract's
    fixed names and the fixed forbidden vocabulary are echoed; every other key
    becomes the placeholder "<key>".
    """
    name = str(key)
    if name.lower() in FORBIDDEN_KEYS:
        return name.lower()
    return name if name in CONTRACT_KEY_NAMES else "<key>"


def _forbidden_walk(node: object, path: str, depth: int = 0) -> None:
    if depth > MAX_NESTING_DEPTH:
        _fail("invalid_nesting", "the payload nesting is too deep", path)
    if isinstance(node, dict):
        for key, value in node.items():
            segment = _reported_key(key)
            child = path + "." + segment if path else segment
            if str(key).lower() in FORBIDDEN_KEYS:
                _fail("forbidden_field", "field is never part of the contract", child)
            _forbidden_walk(value, child, depth + 1)
    elif isinstance(node, list):
        for index, item in enumerate(node):
            _forbidden_walk(item, path + "[" + str(index) + "]", depth + 1)


def _exact_keys(node: object, allowed: tuple, path: str) -> None:
    if not isinstance(node, dict):
        _fail("invalid_type", "expected a JSON object", path)
    extra = sorted(set(node) - set(allowed))
    if extra:
        # The key names are attacker-controlled input. Never echo them into
        # logs or a stable error message; the path names only the parent.
        _fail("unknown_field", "the object has field(s) outside the allowlist", path)
    missing = sorted(set(allowed) - set(node))
    if missing:
        _fail("missing_field", "missing field(s): " + ", ".join(missing), path)


def _unique_event_refs(transitions: list, path: str) -> None:
    seen: set = set()
    for index, event in enumerate(transitions):
        event_path = path + "[" + str(index) + "]"
        if not isinstance(event, dict):
            _fail("invalid_type", "expected a JSON object", event_path)
        ref = event.get("event_ref")
        if not isinstance(ref, str):
            _fail("invalid_ref", "event_ref is required", event_path + ".event_ref")
        if ref in seen:
            _fail("duplicate_event_ref", "event_ref repeats", event_path)
        seen.add(ref)


def _acceptance_events(transitions: list, as_of_day: date) -> list:
    """Acceptance transitions effective by the day, in deterministic order."""
    relevant = [
        event
        for event in transitions
        if event["kind"] == "acceptance" and parse_day(event["effective_day"], "effective_day") <= as_of_day
    ]
    relevant.sort(key=lambda event: (event["effective_day"], event["event_ref"]))
    return relevant


def winning_acceptance(transitions: list, as_of_day: date) -> dict | None:
    """The acceptance transition whose value and evidence the export carries."""
    events = _acceptance_events(transitions, as_of_day)
    return events[-1] if events else None


def derive_state(transitions: list, applicable_stages: list, as_of_day: date) -> dict:
    """Reconstruct the snapshot state at as_of_day from event history.

    Only events effective on or before the day are used; a later event can
    never settle an earlier day's state. Later stages never imply skipped
    stages: stage status is read from that stage's own events only.
    """
    relevant = [event for event in transitions if parse_day(event["effective_day"], "effective_day") <= as_of_day]
    relevant.sort(key=lambda event: (event["effective_day"], event["event_ref"]))

    terminal = [event for event in relevant if event["kind"] == "status"]
    if terminal:
        last_terminal = terminal[-1]
        status = last_terminal["value"]
        delivery_day = last_terminal["effective_day"] if status == "delivered" else None
    else:
        observations = [event for event in relevant if event["kind"] == "observation"]
        status = observations[-1]["value"] if observations else "unknown"
        delivery_day = None

    acceptance_events = _acceptance_events(transitions, as_of_day)
    if acceptance_events:
        acceptance = acceptance_events[-1]["value"]
        acceptance_day = acceptance_events[-1]["effective_day"]
    else:
        acceptance = "not_assessed"
        acceptance_day = None

    stage_status = {}
    for stage in STAGES:
        if stage not in applicable_stages:
            stage_status[stage] = "not_applicable"
            continue
        stage_events = [event for event in relevant if event["kind"] == "stage" and event.get("stage") == stage]
        stage_status[stage] = stage_events[-1]["value"] if stage_events else "not_started"

    return {
        "status": status,
        "delivery_day": delivery_day,
        "acceptance": acceptance,
        "acceptance_day": acceptance_day,
        "stage_status": stage_status,
    }


def validate_envelope(payload: object) -> dict:
    """Validate one export payload against the strict allowlist contract.

    Raises ContractError on the first violation; returns the payload unchanged.
    """
    if not isinstance(payload, dict):
        _fail("invalid_type", "the export must be a JSON object", "")
    _forbidden_walk(payload, "")
    _exact_keys(payload, TOP_KEYS, "")

    if payload["schema"] != SCHEMA_NAME:
        _fail("unsupported_schema", "unsupported schema epoch; fail closed", "schema")
    if payload["library_revision"] not in SUPPORTED_LIBRARY_REVISIONS:
        _fail("unknown_library_revision", "library revision is not a shipped value", "library_revision")
    if payload["capture_tier"] != CAPTURE_TIER:
        _fail("unsupported_capture_tier", "only self_report capture exists", "capture_tier")
    if payload["consent_policy_version"] not in SUPPORTED_CONSENT_POLICIES:
        _fail("unknown_consent_policy", "consent policy version is not known", "consent_policy_version")
    if payload["reporting_window_days"] != REPORTING_WINDOW_DAYS:
        _fail("invalid_horizon", "the reporting horizon is fixed at 30 days", "reporting_window_days")
    parse_ref(payload["admission_ref"], "admission_ref", "adm-")

    snapshot = payload["snapshot"]
    _exact_keys(snapshot, SNAPSHOT_KEYS, "snapshot")
    parse_ref(snapshot["workflow_ref"], "snapshot.workflow_ref", "wf-")
    parse_ref(snapshot["export_ref"], "snapshot.export_ref", "exp-")
    parse_ref(snapshot["criteria_contract_ref"], "snapshot.criteria_contract_ref", "crit-")

    revision = snapshot["revision"]
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 1:
        _fail("invalid_revision", "revision must be a positive integer", "snapshot.revision")

    start = parse_day(snapshot["start_day"], "snapshot.start_day")
    last = parse_day(snapshot["last_observed_day"], "snapshot.last_observed_day")
    due = parse_day(snapshot["report_due_day"], "snapshot.report_due_day")
    if due != start + timedelta(days=REPORTING_WINDOW_DAYS):
        _fail("invalid_report_due_day", "report_due_day must be start_day + 30 days", "snapshot.report_due_day")
    if last < start:
        _fail("invalid_last_observed_day", "last_observed_day precedes start_day", "snapshot.last_observed_day")

    if not isinstance(snapshot["criteria_frozen_before_work"], bool):
        _fail("invalid_type", "criteria_frozen_before_work must be boolean", "snapshot.criteria_frozen_before_work")

    stages = snapshot["applicable_stages"]
    if not isinstance(stages, list) or not stages or any(stage not in STAGES for stage in stages):
        _fail("invalid_stages", "applicable_stages must be a non-empty subset of the five stages", "snapshot.applicable_stages")
    if len(set(stages)) != len(stages):
        _fail("invalid_stages", "applicable_stages repeats a stage", "snapshot.applicable_stages")
    if [stage for stage in STAGES if stage in stages] != list(stages):
        _fail("invalid_stages", "applicable_stages must follow the fixed stage order", "snapshot.applicable_stages")

    stage_status = snapshot["stage_status"]
    _exact_keys(stage_status, STAGES, "snapshot.stage_status")
    for stage in STAGES:
        value = stage_status[stage]
        if value not in STAGE_STATUSES:
            _fail("invalid_enum", "stage status is not an allowlisted value", "snapshot.stage_status." + stage)
        if stage in stages and value == "not_applicable":
            _fail("applicability_conflict", "an applicable stage cannot be not_applicable", "snapshot.stage_status." + stage)
        if stage not in stages and value != "not_applicable":
            _fail("applicability_conflict", "an inapplicable stage must be not_applicable", "snapshot.stage_status." + stage)
    if snapshot["status"] not in STATUSES:
        _fail("invalid_enum", "status is not an allowlisted value", "snapshot.status")
    if snapshot["acceptance"] not in ACCEPTANCE:
        _fail("invalid_enum", "acceptance is not an allowlisted value", "snapshot.acceptance")
    if snapshot["acceptance_evidence"] not in ACCEPTANCE_EVIDENCE:
        _fail("invalid_enum", "acceptance_evidence is not an allowlisted value", "snapshot.acceptance_evidence")
    if snapshot["acceptance"] == "not_assessed" and snapshot["acceptance_evidence"] != "none":
        _fail("invalid_evidence", "an unassessed acceptance carries no evidence category", "snapshot.acceptance_evidence")
    if snapshot["acceptance"] in ("independent_attested_pass", "independent_attested_fail") and snapshot[
        "acceptance_evidence"
    ] == "none":
        _fail("evidence_required", "an independently attested acceptance needs a local evidence category", "snapshot.acceptance_evidence")
    for field in ("delivery_day", "acceptance_day"):
        value = snapshot[field]
        if value is not None:
            parse_day(value, "snapshot." + field)

    transitions = snapshot["transitions"]
    if not isinstance(transitions, list) or not transitions:
        _fail("invalid_transitions", "a snapshot needs at least one transition", "snapshot.transitions")
    if len(transitions) > MAX_TRANSITIONS:
        _fail("too_many_transitions", "at most 256 transitions per snapshot", "snapshot.transitions")
    _unique_event_refs(transitions, "snapshot.transitions")
    status_events: list = []
    same_day_values: dict = {}
    for index, event in enumerate(transitions):
        path = "snapshot.transitions[" + str(index) + "]"
        _exact_keys(event, TRANSITION_KEYS, path)
        parse_ref(event["event_ref"], path + ".event_ref", "evt-")
        kind = event["kind"]
        if kind not in EVENT_KINDS:
            _fail("invalid_enum", "event kind is not allowlisted", path + ".kind")
        effective = parse_day(event["effective_day"], path + ".effective_day")
        if effective < start:
            _fail("event_before_start", "an event cannot precede start_day", path + ".effective_day")
        if effective > last:
            _fail("event_after_last_observed", "an event cannot follow last_observed_day", path + ".effective_day")
        if event["value"] not in EVENT_VALUES[kind]:
            _fail("invalid_enum", "event value is not allowlisted for this kind", path + ".value")
        stage = event["stage"]
        if kind == "stage":
            if stage not in STAGES:
                _fail("invalid_stage", "a stage event needs an allowlisted stage", path + ".stage")
            if stage not in stages:
                _fail("stage_not_applicable", "a stage event names an inapplicable stage", path + ".stage")
            if event["value"] == "not_applicable":
                _fail("applicability_conflict", "an applicable stage cannot be not_applicable", path + ".value")
        elif stage is not None:
            _fail("unexpected_stage", "only a stage event carries a stage", path + ".stage")
        conflict_key = (kind, event["effective_day"], stage if kind == "stage" else None)
        if conflict_key in same_day_values and same_day_values[conflict_key] != event["value"]:
            if kind == "status":
                _fail("conflicting_terminal_same_day", "same-day terminal transitions conflict", path)
            _fail("conflicting_same_day_transition", "one value per kind or stage per day is allowed", path + ".value")
        same_day_values[conflict_key] = event["value"]
        if kind == "status":
            if status_events and status_events[0]["value"] != event["value"]:
                _fail("conflicting_terminal", "only one terminal status is permitted", path)
            status_events.append(event)
    terminal_days = [parse_day(item["effective_day"], "effective_day") for item in status_events]
    for index, event in enumerate(transitions):
        if event["kind"] != "observation":
            continue
        observed = parse_day(event["effective_day"], "effective_day")
        if any(observed > terminal for terminal in terminal_days):
            _fail("observation_after_terminal", "a terminal outcome needs no further observation", "snapshot.transitions[" + str(index) + "]")

    expected = derive_state(transitions, stages, last)
    for field in ("status", "delivery_day", "acceptance", "acceptance_day"):
        if snapshot[field] != expected[field]:
            _fail("derived_mismatch", "snapshot field disagrees with its transition history", "snapshot." + field)
    if dict(stage_status) != expected["stage_status"]:
        _fail("derived_mismatch", "stage_status disagrees with its transition history", "snapshot.stage_status")
    if snapshot["status"] == "delivered" and snapshot["delivery_day"] is None:
        _fail("derived_mismatch", "a delivered outcome needs a delivery day", "snapshot.delivery_day")

    size = len(canonical_bytes(payload))
    if size > MAX_SNAPSHOT_BYTES:
        _fail("oversize", "snapshot exceeds the 64 KiB bound", "")
    return payload


def loads_strict(raw: bytes) -> object:
    """Decode one UTF-8 JSON document, refusing duplicate keys and oversize input."""
    if len(raw) > MAX_SNAPSHOT_BYTES:
        _fail("oversize", "payload exceeds the 64 KiB bound", "")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        _fail("invalid_encoding", "payload is not UTF-8", "")

    def pairs(items):
        seen = set()
        result: dict = {}
        for key, value in items:
            if key in seen:
                _fail("duplicate_key", "a JSON object repeats a key", "")
            seen.add(key)
            result[key] = value
        return result

    try:
        parsed = json.loads(text, object_pairs_hook=pairs)
    except json.JSONDecodeError as exc:
        _fail("malformed_json", "payload is not valid JSON: " + exc.msg, "")
    except RecursionError:
        _fail("invalid_nesting", "the payload nesting is too deep", "")
    _assert_nesting(parsed)
    return parsed


# --------------------------------------------------------------------------
# Local store
# --------------------------------------------------------------------------


def new_store() -> dict:
    return {"store_version": STORE_VERSION, "opt_ins": {}, "workflows": {}}


def load_store(path: Path) -> dict:
    if not path.exists():
        return new_store()
    try:
        store = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        _fail("store_unreadable", "local store cannot be read: " + str(exc), str(path))
    if not isinstance(store, dict) or store.get("store_version") != STORE_VERSION:
        _fail("store_version", "local store version is not supported", str(path))
    if not isinstance(store.get("opt_ins", {}), dict) or not isinstance(store.get("workflows", {}), dict):
        _fail("store_unreadable", "local store has an unsupported shape", str(path))
    store.setdefault("opt_ins", {})
    store.setdefault("workflows", {})
    return store


def save_store(path: Path, store: dict) -> None:
    write_private_store(path, json.dumps(store, indent=2, sort_keys=True, ensure_ascii=True) + "\n")


def enable_capture(
    store: dict,
    *,
    day: str,
    start_day: str,
    applicable_stages: list | None = None,
    criteria_frozen_before_work: bool = True,
    workflow_ref: str | None = None,
    criteria_contract_ref: str | None = None,
    admission_ref: str | None = None,
) -> dict:
    """Explicit per-workflow opt-in. Nothing is captured before this call."""
    if not isinstance(criteria_frozen_before_work, bool):
        _fail("invalid_type", "criteria_frozen_before_work must be boolean", "criteria_frozen_before_work")
    start = parse_day(start_day, "start_day")
    captured = parse_day(day, "day")
    if start > captured or start < captured - timedelta(days=7):
        _fail("start_outside_window", "a start must be acknowledged within seven days", "start_day")
    requested = list(STAGES) if applicable_stages is None else list(applicable_stages)
    if not requested:
        _fail("invalid_stages", "applicable_stages needs at least one stage", "applicable_stages")
    if any(stage not in STAGES for stage in requested):
        _fail("invalid_stages", "applicable_stages contains a non-stage", "applicable_stages")
    if [stage for stage in STAGES if stage in requested] != list(requested):
        _fail("invalid_stages", "stages must follow the fixed order", "applicable_stages")
    stages = [stage for stage in STAGES if stage in requested]
    ref = workflow_ref or random_ref("wf-")
    parse_ref(ref, "workflow_ref", "wf-")
    if ref in store.get("workflows", {}):
        _fail("workflow_exists", "this workflow already has local enrollment; delete-local before re-enrolling", "workflow_ref")
    contract_ref = criteria_contract_ref or random_ref("crit-")
    parse_ref(contract_ref, "criteria_contract_ref", "crit-")
    if admission_ref is not None:
        parse_ref(admission_ref, "admission_ref", "adm-")
    workflow = {
        "workflow_ref": ref,
        "admission_ref": admission_ref,
        "captured_day": day_str(captured),
        "start_day": day_str(start),
        "applicable_stages": stages,
        "criteria_frozen_before_work": criteria_frozen_before_work,
        "criteria_contract_ref": contract_ref,
        "acceptance_evidence": "none",
        "revision": 0,
        "export_ref": None,
        "last_observed_day": None,
        "transitions": [],
    }
    store["workflows"][ref] = workflow
    store["opt_ins"][ref] = {"enabled": True, "opted_in_day": day_str(captured)}
    return workflow


def require_enabled(store: dict, workflow_ref: str) -> dict:
    parse_ref(workflow_ref, "workflow_ref", "wf-")
    opt_in = store.get("opt_ins", {}).get(workflow_ref)
    if not opt_in or not opt_in.get("enabled"):
        _fail("capture_disabled", "capture is off for this workflow; opt in first", workflow_ref)
    workflow = store.get("workflows", {}).get(workflow_ref)
    if not workflow:
        _fail("unknown_workflow", "no local enrollment for this workflow", workflow_ref)
    return workflow


def read_workflow(store: dict, workflow_ref: str) -> dict:
    """Read a retained workflow without requiring capture to be enabled."""
    parse_ref(workflow_ref, "workflow_ref", "wf-")
    workflow = store.get("workflows", {}).get(workflow_ref)
    if not workflow:
        _fail("unknown_workflow", "no local enrollment for this workflow", workflow_ref)
    return workflow


def disable_capture(store: dict, workflow_ref: str) -> dict:
    """Stop capture for this workflow; retained history stays readable."""
    parse_ref(workflow_ref, "workflow_ref", "wf-")
    opt_in = store.get("opt_ins", {}).get(workflow_ref)
    if not opt_in:
        _fail("unknown_workflow", "no opt-in for this workflow", workflow_ref)
    opt_in["enabled"] = False
    return opt_in


def delete_local(store: dict, *, workflow_ref: str | None = None, delete_all: bool = False, confirm: bool = False) -> dict:
    """Irreversibly delete locally retained reporting history.

    This is the "separately selectable" local deletion the plan requires. It
    removes the workflow history and its opt-in; it never contacts a steward or
    any network service. Deletion is explicit: without confirm nothing is
    changed. The store file remains when other workflows still use it, and the
    caller saves the mutated store atomically.
    """
    if not confirm:
        _fail("confirmation_required", "local deletion needs an explicit confirmation", "confirm")
    if delete_all == bool(workflow_ref):
        _fail("invalid_arguments", "name one workflow_ref or --all, not both or neither", "workflow_ref")
    if delete_all:
        removed_workflows = len(store.get("workflows", {}))
        removed_opt_ins = len(store.get("opt_ins", {}))
        store["workflows"] = {}
        store["opt_ins"] = {}
        return {
            "deleted_workflows": removed_workflows,
            "deleted_opt_ins": removed_opt_ins,
            "workflows_remaining": 0,
        }
    ref = parse_ref(workflow_ref, "workflow_ref", "wf-")
    workflow = store.get("workflows", {}).pop(ref, None)
    opt_in = store.get("opt_ins", {}).pop(ref, None)
    if workflow is None and opt_in is None:
        _fail("unknown_workflow", "no local history for this workflow", ref)
    return {
        "deleted_workflows": 1 if workflow is not None else 0,
        "deleted_opt_ins": 1 if opt_in is not None else 0,
        "workflows_remaining": len(store.get("workflows", {})),
    }


def record_transition(
    store: dict,
    workflow_ref: str,
    *,
    kind: str,
    value: str,
    effective_day: str,
    stage: str | None = None,
    event_ref: str | None = None,
    evidence: str | None = None,
) -> dict:
    workflow = require_enabled(store, workflow_ref)
    if kind not in EVENT_KINDS:
        _fail("invalid_enum", "event kind is not allowlisted", "kind")
    if value not in EVENT_VALUES[kind]:
        _fail("invalid_enum", "event value is not allowlisted for this kind", "value")
    effective = parse_day(effective_day, "effective_day")
    start = parse_day(workflow["start_day"], "start_day")
    if effective < start:
        _fail("event_before_start", "an event cannot precede start_day", "effective_day")
    if kind == "stage":
        if stage not in STAGES:
            _fail("invalid_stage", "a stage event needs an allowlisted stage", "stage")
        if stage not in workflow["applicable_stages"]:
            _fail("stage_not_applicable", "not-applicable stages are chosen at start", "stage")
        if value == "not_applicable":
            _fail("applicability_conflict", "an applicable stage cannot be not_applicable", "value")
    elif stage is not None:
        _fail("unexpected_stage", "only a stage event carries a stage", "stage")
    if kind == "acceptance":
        evidence = evidence or "none"
        if evidence not in ACCEPTANCE_EVIDENCE:
            _fail("invalid_enum", "acceptance evidence is not an allowlisted value", "evidence")
        if value == "not_assessed" and evidence != "none":
            _fail("invalid_evidence", "an unassessed acceptance carries no evidence category", "evidence")
        if value.startswith("independent_attested_") and evidence == "none":
            _fail("evidence_required", "an independently attested acceptance needs a local evidence category", "evidence")
    elif evidence is not None:
        _fail("unexpected_evidence", "only an acceptance event carries an evidence category", "evidence")
    if len(workflow["transitions"]) >= MAX_TRANSITIONS:
        _fail("too_many_transitions", "at most 256 transitions per snapshot", "transitions")
    if event_ref is not None:
        parse_ref(event_ref, "event_ref", "evt-")
        if any(other["event_ref"] == event_ref for other in workflow["transitions"]):
            _fail("duplicate_event_ref", "event_ref repeats", "event_ref")

    for other in workflow["transitions"]:
        if other["kind"] != kind or other["effective_day"] != day_str(effective) or other["value"] == value:
            continue
        if kind == "stage" and other["stage"] != stage:
            continue
        if kind == "status":
            _fail("conflicting_terminal_same_day", "same-day terminal transitions conflict", "value")
        _fail("conflicting_same_day_transition", "one value per kind or stage per day is allowed", "value")
    terminal = [event for event in workflow["transitions"] if event["kind"] == "status"]
    if kind == "status" and terminal:
        if (terminal[-1]["value"], terminal[-1]["effective_day"]) != (value, effective_day):
            _fail("conflicting_terminal", "a terminal outcome is already recorded", "value")
    if kind == "observation":
        # Chronology is decided by effective day, not by recording order: an
        # observation may be backfilled before a terminal already recorded.
        for other in terminal:
            if effective > parse_day(other["effective_day"], "effective_day"):
                _fail("observation_after_terminal", "a terminal outcome needs no further observation", "effective_day")
    if kind == "status":
        for other in workflow["transitions"]:
            if other["kind"] == "observation" and parse_day(other["effective_day"], "effective_day") > effective:
                _fail(
                    "observation_after_terminal",
                    "a terminal outcome cannot precede a recorded observation",
                    "effective_day",
                )

    event = {
        "event_ref": event_ref or random_ref("evt-"),
        "kind": kind,
        "effective_day": day_str(effective),
        "value": value,
        "stage": stage,
    }
    parse_ref(event["event_ref"], "event_ref", "evt-")
    if kind == "acceptance":
        # Evidence is bound to this transition, not to the workflow slot: an
        # acceptance recorded later with an earlier effective day must never
        # overwrite the category of the acceptance that wins by effective day.
        event["evidence"] = evidence
    workflow["transitions"].append(event)
    if kind == "acceptance":
        winner = max(
            (item for item in workflow["transitions"] if item["kind"] == "acceptance"),
            key=lambda item: (item["effective_day"], item["event_ref"]),
        )
        workflow["acceptance_evidence"] = winner.get("evidence", "none")
    workflow["revision"] += 1
    workflow["export_ref"] = random_ref("exp-")
    if workflow["last_observed_day"] is None or day_str(effective) > workflow["last_observed_day"]:
        workflow["last_observed_day"] = day_str(effective)
    return event


def build_envelope(store: dict, workflow_ref: str) -> dict:
    workflow = require_enabled(store, workflow_ref)
    if not workflow["transitions"]:
        _fail("empty_snapshot", "record at least one transition before export", workflow_ref)
    if not workflow.get("admission_ref"):
        _fail("missing_admission", "attach the steward-issued admission_ref before export", workflow_ref)
    last = parse_day(workflow["last_observed_day"], "last_observed_day")
    start = parse_day(workflow["start_day"], "start_day")
    derived = derive_state(workflow["transitions"], workflow["applicable_stages"], last)
    winner = winning_acceptance(workflow["transitions"], last)
    if derived["acceptance"] == "not_assessed" or winner is None:
        evidence = "none"
    else:
        evidence = winner.get("evidence")
        if evidence is None:  # a store written before evidence was per-event
            evidence = workflow.get("acceptance_evidence", "none")
    envelope = {
        "schema": SCHEMA_NAME,
        "library_revision": SUPPORTED_LIBRARY_REVISIONS[0],
        "capture_tier": CAPTURE_TIER,
        "consent_policy_version": SUPPORTED_CONSENT_POLICIES[0],
        "reporting_window_days": REPORTING_WINDOW_DAYS,
        "admission_ref": workflow["admission_ref"],
        "snapshot": {
            "workflow_ref": workflow["workflow_ref"],
            "revision": workflow["revision"],
            "export_ref": workflow["export_ref"],
            "start_day": day_str(start),
            "last_observed_day": day_str(last),
            "report_due_day": day_str(start + timedelta(days=REPORTING_WINDOW_DAYS)),
            "applicable_stages": list(workflow["applicable_stages"]),
            "criteria_frozen_before_work": workflow["criteria_frozen_before_work"],
            "criteria_contract_ref": workflow["criteria_contract_ref"],
            "stage_status": derived["stage_status"],
            "status": derived["status"],
            "acceptance": derived["acceptance"],
            "acceptance_evidence": evidence,
            "delivery_day": derived["delivery_day"],
            "acceptance_day": derived["acceptance_day"],
            "transitions": [
                {
                    "event_ref": event["event_ref"],
                    "kind": event["kind"],
                    "effective_day": event["effective_day"],
                    "value": event["value"],
                    "stage": event["stage"],
                }
                for event in workflow["transitions"]
            ],
        },
    }
    validate_envelope(envelope)
    return envelope


def preview_export(store: dict, workflow_ref: str) -> tuple[bytes, str]:
    payload = canonical_bytes(build_envelope(store, workflow_ref))
    return payload, bytes_sha256(payload)


def export_snapshot(
    store: dict,
    workflow_ref: str,
    out_path: Path,
    *,
    preview_sha256: str,
    confirm: bool,
    repo_root: Path | None = None,
) -> dict:
    """Write the export to local disk only, after exact preview confirmation."""
    payload, digest = preview_export(store, workflow_ref)
    if not confirm:
        _fail("confirmation_required", "export needs a fresh affirmative confirmation", "confirm")
    if not isinstance(preview_sha256, str) or preview_sha256.strip().lower() != digest:
        _fail("preview_mismatch", "the confirmed preview handle does not match these exact bytes", "preview_sha256")
    resolved = out_path.resolve()
    if _inside_reporting_tree(resolved, repo_root):
        _fail("export_path_in_repository", "reporting data must stay outside project version control", str(out_path))
    if resolved.exists():
        _fail("export_exists", "refusing to overwrite an existing export", str(out_path))
    _ensure_private_dir(resolved.parent)
    try:
        _write_private_bytes(resolved, payload, exclusive=True)
    except FileExistsError:
        _fail("export_exists", "refusing to overwrite an existing export", str(out_path))
    return {"path": str(resolved), "bytes": len(payload), "sha256": digest}


def prune_expired(store: dict, day: str) -> int:
    """Apply local 60-day retention from capture."""
    today = parse_day(day, "day")
    removed = 0
    for workflow_ref, workflow in list(store.get("workflows", {}).items()):
        captured = parse_day(workflow["captured_day"], "captured_day")
        if today > captured + timedelta(days=LOCAL_RETENTION_DAYS):
            del store["workflows"][workflow_ref]
            store.get("opt_ins", {}).pop(workflow_ref, None)
            removed += 1
    return removed


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Offline, opt-in workflow-outcomes reporter.")
    parser.add_argument("--store", required=True, help="path to the local reporting store (outside the repository)")
    sub = parser.add_subparsers(dest="command", required=True)

    opt_in = sub.add_parser("opt-in", help="enable capture for one workflow")
    opt_in.add_argument("--day", required=True)
    opt_in.add_argument("--start-day", required=True)
    opt_in.add_argument("--applicable-stages", default=",".join(STAGES))
    opt_in.add_argument("--criteria-frozen", dest="criteria_frozen", action="store_true", default=True)
    opt_in.add_argument("--criteria-not-frozen", dest="criteria_frozen", action="store_false")
    opt_in.add_argument("--admission-ref")

    attach = sub.add_parser("attach-admission", help="attach a steward-issued admission reference")
    attach.add_argument("--workflow-ref", required=True)
    attach.add_argument("--admission-ref", required=True)

    opt_out = sub.add_parser("opt-out", help="stop capture for one workflow")
    opt_out.add_argument("--workflow-ref", required=True)

    delete = sub.add_parser("delete-local", help="irreversibly delete locally retained history")
    target = delete.add_mutually_exclusive_group(required=True)
    target.add_argument("--workflow-ref")
    target.add_argument("--all", dest="delete_all", action="store_true", help="delete every local workflow")
    delete.add_argument("--confirm", action="store_true", help="required: deletion cannot be undone")

    record = sub.add_parser("record", help="record one bounded transition")
    record.add_argument("--workflow-ref", required=True)
    record.add_argument("--kind", required=True)
    record.add_argument("--value", required=True)
    record.add_argument("--effective-day", required=True)
    record.add_argument("--stage")
    record.add_argument("--evidence", choices=ACCEPTANCE_EVIDENCE, help="local evidence category for an acceptance event")

    show = sub.add_parser("show", help="show the local record summary")
    show.add_argument("--workflow-ref", required=True)

    notice = sub.add_parser("notice", help="print the minimized start notice for the steward")
    notice.add_argument("--workflow-ref", required=True)

    preview = sub.add_parser("preview", help="print the exact export bytes; writes nothing")
    preview.add_argument("--workflow-ref", required=True)

    export = sub.add_parser("export", help="write the previewed export to local disk")
    export.add_argument("--workflow-ref", required=True)
    export.add_argument("--out", required=True)
    export.add_argument("--preview-sha256", required=True)
    export.add_argument("--confirm", action="store_true")

    purge = sub.add_parser("purge-expired", help="apply local 60-day retention")
    purge.add_argument("--day", required=True)
    return parser


def main(argv: list | None = None) -> int:
    args = _parser().parse_args(argv)
    store_path = Path(args.store)
    try:
        store = load_store(store_path)
        if args.command == "opt-in":
            workflow = enable_capture(
                store,
                day=args.day,
                start_day=args.start_day,
                applicable_stages=[stage.strip() for stage in args.applicable_stages.split(",") if stage.strip()],
                criteria_frozen_before_work=args.criteria_frozen,
                admission_ref=args.admission_ref,
            )
            save_store(store_path, store)
            print(json.dumps({"workflow_ref": workflow["workflow_ref"], "captured": True}, sort_keys=True))
            return 0
        if args.command == "attach-admission":
            workflow = require_enabled(store, args.workflow_ref)
            parse_ref(args.admission_ref, "admission_ref", "adm-")
            if workflow.get("admission_ref") != args.admission_ref:
                # The admission reference is part of the exported envelope but
                # not of the snapshot. Rotate the revision and export handle so
                # the importer never sees two different payloads at one
                # revision (which it would quarantine as conflicting).
                workflow["admission_ref"] = args.admission_ref
                workflow["revision"] += 1
                workflow["export_ref"] = random_ref("exp-")
            save_store(store_path, store)
            print(json.dumps({"workflow_ref": workflow["workflow_ref"], "admission_attached": True}, sort_keys=True))
            return 0
        if args.command == "opt-out":
            disable_capture(store, args.workflow_ref)
            save_store(store_path, store)
            print(json.dumps({"workflow_ref": args.workflow_ref, "capture": "disabled"}, sort_keys=True))
            return 0
        if args.command == "delete-local":
            if not args.delete_all and not args.workflow_ref:
                _fail("invalid_arguments", "name one workflow_ref or --all", "workflow_ref")
            if args.delete_all and args.workflow_ref:
                _fail("invalid_arguments", "name one workflow_ref or --all, not both", "workflow_ref")
            result = delete_local(
                store,
                workflow_ref=args.workflow_ref,
                delete_all=args.delete_all,
                confirm=args.confirm,
            )
            save_store(store_path, store)
            print(json.dumps(result, sort_keys=True))
            return 0
        if args.command == "record":
            event = record_transition(
                store,
                args.workflow_ref,
                kind=args.kind,
                value=args.value,
                effective_day=args.effective_day,
                stage=args.stage,
                evidence=args.evidence,
            )
            save_store(store_path, store)
            print(json.dumps({"event_ref": event["event_ref"], "revision": store["workflows"][args.workflow_ref]["revision"]}, sort_keys=True))
            return 0
        if args.command == "show":
            workflow = read_workflow(store, args.workflow_ref)
            print(
                json.dumps(
                    {
                        "workflow_ref": workflow["workflow_ref"],
                        "revision": workflow["revision"],
                        "transitions": len(workflow["transitions"]),
                        "captured_day": workflow["captured_day"],
                        "admission_attached": bool(workflow.get("admission_ref")),
                    },
                    sort_keys=True,
                )
            )
            return 0
        if args.command == "notice":
            workflow = require_enabled(store, args.workflow_ref)
            print(
                json.dumps(
                    {
                        "workflow_ref": workflow["workflow_ref"],
                        "start_day": workflow["start_day"],
                        "applicable_stages": list(workflow["applicable_stages"]),
                        "criteria_frozen_before_work": workflow["criteria_frozen_before_work"],
                        "criteria_contract_ref": workflow["criteria_contract_ref"],
                    },
                    sort_keys=True,
                )
            )
            return 0
        if args.command == "preview":
            payload, digest = preview_export(store, args.workflow_ref)
            sys.stderr.write("preview-sha256 " + digest + "\n")
            sys.stderr.flush()
            sys.stdout.buffer.write(payload)
            sys.stdout.buffer.flush()
            return 0
        if args.command == "export":
            result = export_snapshot(
                store,
                args.workflow_ref,
                Path(args.out),
                preview_sha256=args.preview_sha256,
                confirm=args.confirm,
            )
            print(json.dumps(result, sort_keys=True))
            return 0
        if args.command == "purge-expired":
            removed = prune_expired(store, args.day)
            save_store(store_path, store)
            print(json.dumps({"removed": removed}, sort_keys=True))
            return 0
    except ContractError as exc:
        sys.stderr.write("ERROR " + exc.code + ": " + exc.message + (" [" + exc.path + "]" if exc.path else "") + "\n")
        return 2
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        # A corrupt store or an unreadable input is a stable refusal, never a
        # traceback: these are the failures that used to escape the handler.
        sys.stderr.write("ERROR store_unreadable: " + str(exc) + "\n")
        return 2
    except (TypeError, KeyError, AttributeError) as exc:
        # A structurally invalid nested store is still operator-readable input,
        # not a reason for a traceback.
        sys.stderr.write("ERROR store_unreadable: " + str(exc) + "\n")
        return 2
    return 2


if __name__ == "__main__":
    sys.exit(main())
