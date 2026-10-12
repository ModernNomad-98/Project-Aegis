"""Offline synthetic FAST SAVE checkpoint capture.

This capability is deliberately small and deliberately offline. One call writes
exactly ONE versioned JSON checkpoint file at the path the operator names on the
command line, using a temporary file plus flush and os.fsync and an atomic
replace, and only after a bounded readback of that TEMPORARY file has verified
its bytes, its integrity digest and its key set. Every FAILED return therefore
happens before os.replace, and a failed save leaves the previous checkpoint
byte-for-byte intact (protocol P7 rules 1, 2 and 3).

It reports statuses; it observes nothing. execution_status is the operator's
REPORTED state and never an observation: this tool holds no process handle,
starts no process, stops nothing, and verifies no authority. Authority
references are recorded verbatim and are explicitly not validated; evidence
references are recorded verbatim and never re-read. The module grants nothing
and enforces nothing: it cannot block, intercept or interrupt a prohibited
action, a passing fixture is not real authority, and no output of this module
may be read as evidence that any process ceased.

Durability honesty: this is atomic replace plus a file fsync. It is not a proof
of physical power-loss durability, matching the limit the package README already
draws for the kernel, and no directory fsync is attempted because it is not
portable on Windows.

The module imports only the closed standard-library allowlist documented in
ALLOWED_IMPORTS, has no module-level side effect (importing it opens no file,
starts no process and touches no network), and contains exactly one deletion
call SITE: os.unlink on the temporary file this module itself created, on the
failure paths inside write_checkpoint_atomically.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import tempfile
import time
from typing import Any, Mapping

CHECKPOINT_FORMAT = "aegis-fast-save-checkpoint"
CHECKPOINT_VERSION = 1
MAX_CHECKPOINT_BYTES = 65536
IDLE_TARGET_SECONDS = 60
EXECUTION_STATES = ("STOPPED", "ACTIVE", "UNKNOWN", "PAUSE INCOMPLETE")
DISPATCH_STATES = ("stopped", "not stopped", "unknown")
OPERATION_STATES = ("STOPPED", "ACTIVE", "UNKNOWN")
DISPATCH_STATE_SOURCE = "reported-by-operator"
EXECUTION_STATUS_SOURCE = "reported-by-operator"
CHANGED_FILES_SOURCE = "reported-by-operator; this tool runs no git command"
SAFE_STOPPED_NONE_NOTE = (
    "none: no tracked operation was reported STOPPED with an operator "
    "authorization to stop. The list is present and is never left blank, "
    "because a blank field cannot be distinguished from an omitted one."
)
# The closed import allowlist, recorded here as documentation: the AST allowlist
# scan in tests/test_fast_save.py asserts that this module's imported roots are a
# subset of it, and that no forbidden attribute call appears in the save path.
ALLOWED_IMPORTS = (
    "__future__",
    "dataclasses",
    "datetime",
    "hashlib",
    "json",
    "os",
    "pathlib",
    "tempfile",
    "time",
    "typing",
)
CREDENTIAL_KEY_NAMES = frozenset({
    "password", "passwd", "secret", "token", "api_key", "apikey", "private_key",
    "credential", "credentials", "client_secret", "access_token",
    "refresh_token", "session_token", "authorization_header", "bearer",
})
TOKEN_VALUE_PREFIXES = ("ghp_", "github_pat_", "gho_", "sk-", "AKIA", "-----BEGIN")

STATE_KEYS = frozenset({
    "item_id", "objective", "workstream_id", "repository_id", "current_stage",
    "holder", "completed_work", "remaining_work", "changed_files",
    "unfinished_files", "evidence_references", "failures_blockers", "gaps",
    "operations", "dispatch_state_reported", "pause_reported_complete",
    "pause_incomplete_reason", "authority_references", "one_line_resume",
    "next_safe_action",
})
OPERATION_KEYS = frozenset({
    "operation_id", "reported_state", "authorized_to_stop", "authorization_ref",
})
CHANGED_FILE_KEYS = frozenset({"path", "uncommitted"})
REQUIRED_CHECKPOINT_KEYS = frozenset({
    "checkpoint_format", "checkpoint_version", "checkpoint_sequence",
    "created_utc", "created_unix_seconds", "invocation_phrase",
    "invocation_phrase_note", "repository_id", "workstream_id", "item_id",
    "dispatch_state_reported", "dispatch_state_source", "objective",
    "current_stage", "holder", "completed_work", "remaining_work",
    "unfinished_files", "unfinished_files_preserved", "changed_files",
    "changed_files_source", "execution_status", "execution_status_source",
    "execution_status_note", "operations", "reported_state_conflicts",
    "checkpoint_status", "durable_location", "durable_location_approval",
    "bounded_readback", "one_line_resume", "next_safe_action",
    "previous_valid_checkpoint", "no_provider_call_attestation",
    "safe_stopped_operations", "safe_stopped_operations_source",
    "safe_stopped_operations_note", "operations_not_stopped",
    "no_credentials_tokens_secrets", "idle_measurement", "evidence_references",
    "evidence_references_note", "authority_references",
    "authority_references_note", "failures_blockers", "gaps", "gaps_note",
    "integrity",
})


class FastSaveRefused(Exception):
    """A refusal or a pre-replace failure. Nothing was written to the target."""

    def __init__(self, reason_code: str, reason: str) -> None:
        super().__init__(reason)
        self.reason_code = reason_code
        self.reason = reason


@dataclass(frozen=True)
class OperationReport:
    """One operator-reported operation. Never an observation."""

    operation_id: str
    reported_state: str
    authorized_to_stop: bool
    authorization_ref: str = ""


@dataclass(frozen=True)
class SaveRequest:
    """The strict-schema state document, as reported by the operator."""

    item_id: str
    objective: str
    workstream_id: str
    repository_id: str
    current_stage: str
    holder: str
    completed_work: tuple[str, ...]
    remaining_work: tuple[str, ...]
    changed_files: tuple[Mapping[str, Any], ...]
    unfinished_files: tuple[str, ...]
    evidence_references: tuple[str, ...]
    failures_blockers: tuple[str, ...]
    gaps: tuple[str, ...]
    operations: tuple[OperationReport, ...]
    dispatch_state_reported: str
    pause_reported_complete: bool
    pause_incomplete_reason: str
    authority_references: tuple[str, ...]
    one_line_resume: str
    next_safe_action: str


@dataclass(frozen=True)
class SaveResult:
    """The outcome of one capture. FAILED is returned, never written."""

    checkpoint_status: str
    reason_code: str
    reason: str
    document: Mapping[str, Any] | None
    checkpoint_path: str
    durable_location: str | None
    bounded_readback: Mapping[str, Any] | None
    one_line_resume: str | None


def _invalid(detail: str) -> FastSaveRefused:
    return FastSaveRefused("STATE_INVALID", detail)


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise _invalid(label + " must be a non-empty string")
    return value


def _require_text_list(value: object, label: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise _invalid(label + " must be a list of non-empty strings")
    return tuple(_require_text(item, label + " entry") for item in value)


def _scan_for_secrets(value: object, label: str) -> None:
    """Refuse credential-shaped keys and token-shaped values (never redact)."""
    if isinstance(value, Mapping):
        for key, item in value.items():
            if isinstance(key, str) and key.strip().lower() in CREDENTIAL_KEY_NAMES:
                raise FastSaveRefused(
                    "SECRET_DETECTED",
                    label + " carries the credential-shaped key " + repr(key) + "; "
                    "the save is refused and nothing is written rather than "
                    "redacting silently",
                )
            _scan_for_secrets(item, label)
        return
    if isinstance(value, (list, tuple)):
        for item in value:
            _scan_for_secrets(item, label)
        return
    if isinstance(value, str) and value.startswith(TOKEN_VALUE_PREFIXES):
        raise FastSaveRefused(
            "SECRET_DETECTED",
            label + " carries a token-shaped value; the save is refused and "
            "nothing is written rather than redacting silently",
        )


def load_state_document(path: Path) -> SaveRequest:
    """Load and strictly validate the operator's state document.

    The schema is exact: unknown or missing keys, empty required strings,
    unknown statuses and contradictory authorizations are refused as
    STATE_INVALID. Credential-shaped keys and token-shaped values are refused
    as SECRET_DETECTED before any other consideration.
    """
    try:
        raw = Path(path).read_bytes()
    except OSError as error:
        raise _invalid("the state document could not be read: " + str(error)) from error
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise _invalid("the state document must be readable JSON: " + str(error)) from error
    if not isinstance(value, dict):
        raise _invalid("the state document must be a JSON object")
    _scan_for_secrets(value, "the state document")
    unknown = sorted(set(value) - STATE_KEYS)
    missing = sorted(STATE_KEYS - set(value))
    if unknown or missing:
        raise _invalid(
            "the state document schema is exact; unknown key(s): "
            + str(unknown or "none") + "; missing key(s): " + str(missing or "none")
        )
    operations: list[OperationReport] = []
    seen: set[str] = set()
    for entry in value["operations"]:
        if not isinstance(entry, dict):
            raise _invalid("operations entries must be JSON objects")
        if set(entry) != OPERATION_KEYS:
            raise _invalid(
                "each operations entry needs exactly " + str(sorted(OPERATION_KEYS))
                + "; found " + str(sorted(entry))
            )
        operation_id = _require_text(entry["operation_id"], "operation_id")
        if operation_id in seen:
            raise _invalid("duplicate operation_id " + repr(operation_id))
        seen.add(operation_id)
        reported_state = _require_text(entry["reported_state"], "reported_state")
        if reported_state not in OPERATION_STATES:
            raise _invalid(
                "reported_state " + repr(reported_state) + " is not one of "
                + str(OPERATION_STATES)
            )
        authorized = entry["authorized_to_stop"]
        if not isinstance(authorized, bool):
            raise _invalid("authorized_to_stop must be true or false")
        reference = entry["authorization_ref"]
        if not isinstance(reference, str):
            raise _invalid("authorization_ref must be a string (empty when absent)")
        if authorized and not reference.strip():
            raise _invalid(
                "operation " + repr(operation_id) + " claims authorized_to_stop "
                "with an empty authorization_ref; an unknown authorization is refused"
            )
        if reference.strip() and not authorized:
            raise _invalid(
                "operation " + repr(operation_id) + " carries an authorization_ref "
                "without authorized_to_stop; the report is contradictory"
            )
        operations.append(OperationReport(operation_id, reported_state, authorized, reference))
    dispatch_state = _require_text(value["dispatch_state_reported"], "dispatch_state_reported")
    if dispatch_state not in DISPATCH_STATES:
        raise _invalid(
            "dispatch_state_reported " + repr(dispatch_state) + " is not one of "
            + str(DISPATCH_STATES)
        )
    pause_complete = value["pause_reported_complete"]
    if not isinstance(pause_complete, bool):
        raise _invalid("pause_reported_complete must be true or false")
    pause_reason = value["pause_incomplete_reason"]
    if not isinstance(pause_reason, str):
        raise _invalid("pause_incomplete_reason must be a string")
    if not pause_complete and not pause_reason.strip():
        raise _invalid(
            "pause_reported_complete is false, so pause_incomplete_reason must "
            "say why the pause did not complete"
        )
    one_line_resume = _require_text(value["one_line_resume"], "one_line_resume")
    if "\n" in one_line_resume or "\r" in one_line_resume:
        raise _invalid("one_line_resume must be a single line")
    changed_files: list[Mapping[str, Any]] = []
    for entry in value["changed_files"]:
        if not isinstance(entry, dict) or set(entry) != CHANGED_FILE_KEYS:
            raise _invalid(
                "each changed_files entry needs exactly "
                + str(sorted(CHANGED_FILE_KEYS))
                + " (the reported path and uncommitted flag)"
            )
        if not isinstance(entry["uncommitted"], bool):
            raise _invalid("changed_files entries need a true/false uncommitted flag")
        changed_files.append({
            "path": _require_text(entry["path"], "changed_files path"),
            "uncommitted": entry["uncommitted"],
        })
    return SaveRequest(
        item_id=_require_text(value["item_id"], "item_id"),
        objective=_require_text(value["objective"], "objective"),
        workstream_id=_require_text(value["workstream_id"], "workstream_id"),
        repository_id=_require_text(value["repository_id"], "repository_id"),
        current_stage=_require_text(value["current_stage"], "current_stage"),
        holder=_require_text(value["holder"], "holder"),
        completed_work=_require_text_list(value["completed_work"], "completed_work"),
        remaining_work=_require_text_list(value["remaining_work"], "remaining_work"),
        changed_files=tuple(changed_files),
        unfinished_files=_require_text_list(value["unfinished_files"], "unfinished_files"),
        evidence_references=_require_text_list(value["evidence_references"], "evidence_references"),
        failures_blockers=_require_text_list(value["failures_blockers"], "failures_blockers"),
        gaps=_require_text_list(value["gaps"], "gaps"),
        operations=tuple(operations),
        dispatch_state_reported=dispatch_state,
        pause_reported_complete=pause_complete,
        pause_incomplete_reason=pause_reason,
        authority_references=_require_text_list(value["authority_references"], "authority_references"),
        one_line_resume=one_line_resume,
        next_safe_action=_require_text(value["next_safe_action"], "next_safe_action"),
    )


def report_execution_state(request: SaveRequest) -> tuple[str, tuple[str, ...]]:
    """Derive the REPORTED execution status. Never inferred, never upgraded."""
    unknown = [op.operation_id for op in request.operations if op.reported_state == "UNKNOWN"]
    active = [op.operation_id for op in request.operations if op.reported_state == "ACTIVE"]
    if not request.pause_reported_complete:
        status = "PAUSE INCOMPLETE"
    elif unknown:
        status = "UNKNOWN"
    elif active:
        status = "ACTIVE"
    else:
        status = "STOPPED"
    conflicts: list[str] = []
    troubled = ", ".join(sorted(active + unknown))
    if request.dispatch_state_reported == "stopped" and (active or unknown):
        conflicts.append(
            "dispatch state is reported stopped while operation(s) " + troubled
            + " are reported ACTIVE or UNKNOWN; the contradiction is recorded, "
            "not resolved"
        )
    if request.pause_reported_complete and (active or unknown):
        conflicts.append(
            "the pause is reported complete while operation(s) " + troubled
            + " are reported ACTIVE or UNKNOWN; the contradiction is recorded, "
            "not resolved"
        )
    return status, tuple(conflicts)


def _authorized_stops(
    request: SaveRequest,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Split reported operations into authorized safe stops and everything else."""
    stopped: list[dict[str, Any]] = []
    not_stopped: list[dict[str, Any]] = []
    for operation in request.operations:
        if (
            operation.reported_state == "STOPPED"
            and operation.authorized_to_stop
            and operation.authorization_ref.strip()
        ):
            stopped.append({
                "operation_id": operation.operation_id,
                "reported_state": operation.reported_state,
                "authorization_ref": operation.authorization_ref,
                "source": "reported-by-operator",
            })
            continue
        if operation.reported_state == "STOPPED":
            reason = "authorization absent; the operation is not listed as a safe stop"
        elif operation.authorized_to_stop:
            reason = (
                "authorization present but the operation is reported "
                + operation.reported_state + ", so it was not stopped"
            )
        else:
            reason = "authorization absent; the operation is not listed as a safe stop"
        not_stopped.append({
            "operation_id": operation.operation_id,
            "reported_state": operation.reported_state,
            "reason": reason,
            "source": "reported-by-operator",
        })
    return stopped, not_stopped


def _content_digest(document: Mapping[str, Any]) -> str:
    body = {key: item for key, item in document.items() if key != "integrity"}
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _utc(now: datetime | None) -> datetime:
    if now is None:
        return datetime.now(timezone.utc)
    if now.tzinfo is None:
        return now.replace(tzinfo=timezone.utc)
    return now.astimezone(timezone.utc)


def _durable_location(path: Path) -> str:
    """Absolute and operator-named; never resolved through a symlink (A7)."""
    return os.path.abspath(os.fspath(path))


def build_checkpoint(
    request: SaveRequest,
    *,
    invocation_phrase: str,
    now: datetime | None = None,
    previous: Mapping[str, Any] | None = None,
    measured_seconds: float = 0.0,
    durable_location: str = "",
) -> dict[str, Any]:
    """Build the checkpoint document. Pure: it opens no file and writes none."""
    if not isinstance(invocation_phrase, str) or not invocation_phrase.strip():
        raise _invalid("the invocation phrase must be a non-empty string")
    moment = _utc(now)
    status, conflicts = report_execution_state(request)
    stopped, not_stopped = _authorized_stops(request)
    sequence = 1 if previous is None else int(previous["checkpoint_sequence"]) + 1
    document: dict[str, Any] = {
        "checkpoint_format": CHECKPOINT_FORMAT,
        "checkpoint_version": CHECKPOINT_VERSION,
        "checkpoint_sequence": sequence,
        "created_utc": moment.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "created_unix_seconds": int(moment.timestamp()),
        "invocation_phrase": invocation_phrase,
        "invocation_phrase_note": (
            "recorded verbatim; the invocation phrase is a trigger, not an authorization"
        ),
        "repository_id": request.repository_id,
        "workstream_id": request.workstream_id,
        "item_id": request.item_id,
        "dispatch_state_reported": request.dispatch_state_reported,
        "dispatch_state_source": DISPATCH_STATE_SOURCE,
        "objective": request.objective,
        "current_stage": request.current_stage,
        "holder": request.holder,
        "completed_work": list(request.completed_work),
        "remaining_work": list(request.remaining_work),
        "unfinished_files": list(request.unfinished_files),
        "unfinished_files_preserved": True,
        "changed_files": [dict(entry) for entry in request.changed_files],
        "changed_files_source": CHANGED_FILES_SOURCE,
        "execution_status": status,
        "execution_status_source": EXECUTION_STATUS_SOURCE,
        "execution_status_note": (
            "REPORTED state of the tracked operations: this tool observes no "
            "process and claims no cessation; UNKNOWN is never upgraded"
        ),
        "operations": [
            {
                "operation_id": operation.operation_id,
                "reported_state": operation.reported_state,
                "authorized_to_stop": operation.authorized_to_stop,
                "authorization_ref": operation.authorization_ref,
                "source": "reported-by-operator",
            }
            for operation in request.operations
        ],
        "reported_state_conflicts": list(conflicts),
        "checkpoint_status": "SAVED",
        "durable_location": durable_location,
        "durable_location_approval": (
            "operator-named at runtime; protocol gap G3 stays open and this tool "
            "invents no default location and creates no parent directory"
        ),
        "one_line_resume": request.one_line_resume,
        "next_safe_action": request.next_safe_action,
        "previous_valid_checkpoint": dict(previous) if previous is not None else None,
        "no_provider_call_attestation": {
            "provider_call_made": False,
            "basis": (
                "static AST allowlist scan of tools/aegis_delivery_control/"
                "fast_save.py (closed stdlib allowlist, zero forbidden attribute "
                "calls) plus a runtime audit-hook sentinel with a mandatory "
                "live-hook positive control"
            ),
        },
        "safe_stopped_operations": stopped,
        "safe_stopped_operations_source": "reported-by-operator",
        "safe_stopped_operations_note": (
            SAFE_STOPPED_NONE_NOTE
            if not stopped
            else (
                "each entry is operator-reported, requires authorized_to_stop "
                "and a non-empty authorization reference, and is recorded "
                "verbatim; this tool stops nothing and holds no process handle"
            )
        ),
        "operations_not_stopped": not_stopped,
        "no_credentials_tokens_secrets": {
            "checked": True,
            "finding": "none",
            "rule": (
                "credential-shaped keys and token-shaped values refuse the save "
                "with SECRET_DETECTED rather than being redacted silently"
            ),
        },
        "evidence_references": list(request.evidence_references),
        "evidence_references_note": (
            "recorded verbatim; never re-read and never revalidated (the "
            "prohibited action of revalidating references)"
        ),
        "authority_references": list(request.authority_references),
        "authority_references_note": (
            "recorded verbatim and explicitly NOT validated; this tool verifies "
            "no authority and grants nothing"
        ),
        "failures_blockers": list(request.failures_blockers),
        "gaps": list(request.gaps),
        "gaps_note": (
            "named as reported, never filled with invented content; this tool "
            "reads no inventory and no source bytes"
        ),
        "idle_measurement": {
            "measured_what": (
                "this tool's capture portion (state load, strict-schema "
                "validation, path guard, document build and serialization) up to "
                "the moment these bytes were built; the write, fsync and replace "
                "are excluded, and the end-to-end command-to-pause time is not "
                "observable here and is never inferred"
            ),
            "measured_when_utc": moment.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "measured_seconds": round(max(0.0, float(measured_seconds)), 6),
            "target_seconds": IDLE_TARGET_SECONDS,
            "within_target": float(measured_seconds) < IDLE_TARGET_SECONDS,
            "note": "measurement target only (protocol P6/S9): measured, never guaranteed",
        },
        "bounded_readback": {
            "performed": True,
            "subject": "temp-file-before-replace",
            "bytes_read": 0,
            "max_bytes": MAX_CHECKPOINT_BYTES,
            "complete": True,
            "missing_fields": [],
            "integrity_verified": True,
            "keyset_verified": True,
            "verified_before_replace": True,
            "note": (
                "these bytes exist only because this bounded readback and "
                "verification succeeded before os.replace; a failed readback "
                "leaves no checkpoint file, so no written document can carry a "
                "false claim here"
            ),
            "post_replace_confirmation": {
                "performed": False,
                "recorded_in": "the caller's SaveResult",
                "reason": (
                    "a document cannot record the outcome of a read performed "
                    "after it is written; the tool records it in the returned "
                    "result instead"
                ),
            },
        },
        "integrity": {
            "algorithm": "sha256",
            "canonicalization": (
                "json.dumps(document without this field, sort_keys=True, "
                "separators=(',', ':'), ensure_ascii=True)"
            ),
            "excludes": "this integrity field itself",
        },
    }
    document["integrity"]["content_sha256"] = _content_digest(document)
    return document


def _read_raw_bounded(path: Path) -> bytes:
    try:
        with open(path, "rb") as handle:
            data = handle.read(MAX_CHECKPOINT_BYTES + 1)
    except OSError as error:
        raise FastSaveRefused(
            "READBACK_FAILED", str(path) + " could not be read: " + str(error)
        ) from error
    if len(data) > MAX_CHECKPOINT_BYTES:
        raise FastSaveRefused(
            "READBACK_FAILED",
            str(path) + " exceeds the " + str(MAX_CHECKPOINT_BYTES) + "-byte "
            "checkpoint bound; the bounded readback refuses it rather than "
            "reading without limit",
        )
    return data


def read_checkpoint_bounded(path: Path) -> dict[str, Any]:
    """Public bounded reader: at most MAX_CHECKPOINT_BYTES, then verify.

    Used by the fresh-session fixture and by the write path's pre-replace check.
    """
    raw = _read_raw_bounded(Path(path))
    try:
        document = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise FastSaveRefused(
            "READBACK_FAILED", str(path) + " is not readable JSON: " + str(error)
        ) from error
    if not isinstance(document, dict):
        raise FastSaveRefused("READBACK_FAILED", str(path) + " is not a JSON object")
    missing = sorted(REQUIRED_CHECKPOINT_KEYS - set(document))
    unexpected = sorted(set(document) - REQUIRED_CHECKPOINT_KEYS)
    if missing or unexpected:
        raise FastSaveRefused(
            "READBACK_FAILED",
            str(path) + " key set does not match the checkpoint schema; missing: "
            + str(missing or "none") + "; unexpected: " + str(unexpected or "none"),
        )
    integrity = document.get("integrity")
    if not isinstance(integrity, dict):
        raise FastSaveRefused(
            "READBACK_FAILED", str(path) + " carries no integrity object"
        )
    if integrity.get("content_sha256") != _content_digest(document):
        raise FastSaveRefused(
            "READBACK_FAILED",
            str(path) + " integrity digest does not match its canonical bytes",
        )
    return document


def guard_target(path: Path) -> None:
    """Refuse an unsafe target before anything is written. No bypass exists.

    Order (lstat/islink FIRST): os.lstat and os.path.islink run on the
    operator-named path before any resolution. A link is refused and is NEVER
    followed - Path.resolve() and os.path.realpath() are not called on the
    target before that refusal. An existing target must then be a regular file
    that is recognizable in one clause: it parses as JSON and carries
    checkpoint_format equal to this format. A recognizable predecessor whose
    integrity digest fails is NOT refused; it is overwritten and recorded as not
    valid. A file that does not parse as JSON, or whose format tag differs, is
    refused and never overwritten. The parent directory must already exist; this
    module never creates one.

    Residual check-then-use window (recorded, not closed): the target is
    inspected here and os.replace runs later, with no directory-fd or no-follow
    confirmation at the moment of replacement, so a target swapped between the
    two steps is replaced rather than refused. The practical impact is small
    because os.replace does not follow a final-component symlink. Ownership,
    access-control lists and symlinked parent directories are outside this guard
    (reusing owned_paths.py was considered and rejected: it guards the kernel
    user-state root with ownership and ACL semantics, which would imply a
    guarantee this increment does not claim).
    """
    target = Path(path)
    try:
        os.lstat(target)
    except FileNotFoundError:
        exists = False
    except OSError as error:
        raise FastSaveRefused(
            "PATH_GUARD_DENIED", "the target could not be inspected: " + str(error)
        ) from error
    else:
        exists = True
    if os.path.islink(target):
        raise FastSaveRefused(
            "PATH_GUARD_DENIED",
            "the target is a symlink; the path guard refuses it and never "
            "follows it (lstat/islink first, no resolve)",
        )
    if exists:
        if not os.path.isfile(target):
            raise FastSaveRefused(
                "PATH_GUARD_DENIED",
                "the target exists and is not a regular file; nothing is written "
                "to a directory, device or other special file",
            )
        try:
            raw = _read_raw_bounded(target)
        except FastSaveRefused as error:
            raise FastSaveRefused(
                "PATH_GUARD_DENIED",
                "the existing target could not be recognized (" + error.reason
                + "); it is refused and never overwritten",
            ) from error
        try:
            document = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise FastSaveRefused(
                "PATH_GUARD_DENIED",
                "the target exists and does not parse as JSON; an unrelated file "
                "is never overwritten",
            ) from None
        if (
            not isinstance(document, dict)
            or document.get("checkpoint_format") != CHECKPOINT_FORMAT
        ):
            raise FastSaveRefused(
                "PATH_GUARD_DENIED",
                "the target exists and is not a checkpoint of this format; an "
                "unrelated file is never overwritten",
            )
    if not target.parent.is_dir():
        raise FastSaveRefused(
            "PATH_GUARD_DENIED",
            "the target's parent directory is absent or is not a directory; this "
            "tool never creates a parent directory",
        )


def _previous_valid_checkpoint(target: Path) -> dict[str, Any] | None:
    """Describe a recognizable predecessor, or None. Never invents one."""
    try:
        os.lstat(target)
    except FileNotFoundError:
        return None
    except OSError:
        return None
    try:
        document = read_checkpoint_bounded(target)
    except FastSaveRefused:
        return None
    sequence = document.get("checkpoint_sequence")
    integrity = document.get("integrity")
    if not isinstance(sequence, int) or not isinstance(integrity, dict):
        return None
    digest = integrity.get("content_sha256")
    if not isinstance(digest, str):
        return None
    return {
        "path": _durable_location(target),
        "checkpoint_sequence": sequence,
        "content_sha256": digest,
    }


def _discard_temp(temp_path: Path | None) -> str:
    """The module's single deletion call site. Never implies a clean rollback."""
    if temp_path is None:
        return ""
    try:
        os.unlink(temp_path)
    except FileNotFoundError:
        return ""
    except OSError as error:
        return " The temporary file " + str(temp_path) + " could not be removed: " + str(error)
    return ""


def write_checkpoint_atomically(path: Path, payload: bytes) -> bytes:
    """temp + flush + fsync + verify the TEMP file + os.replace.

    Every FAILED return is pre-replace: the previous checkpoint is byte-for-byte
    intact and the target is never opened for writing. If the temp-file removal
    itself fails, the reason names the temp path instead of implying a clean
    rollback.
    """
    target = Path(path)
    try:
        descriptor, temp_name = tempfile.mkstemp(
            dir=target.parent, prefix=target.name + ".fast-save-", suffix=".tmp"
        )
    except OSError as error:
        raise FastSaveRefused(
            "WRITE_FAILED",
            "no temporary file could be created in " + str(target.parent) + ": "
            + str(error),
        ) from error
    temp_path = Path(temp_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
    except OSError as error:
        raise FastSaveRefused(
            "WRITE_FAILED",
            "the temporary checkpoint write failed: " + str(error)
            + _discard_temp(temp_path),
        ) from error
    try:
        document = read_checkpoint_bounded(temp_path)
        missing = sorted(REQUIRED_CHECKPOINT_KEYS - set(document))
        if missing:
            raise FastSaveRefused(
                "READBACK_FAILED",
                "the temp-file readback is missing required key(s): " + ", ".join(missing),
            )
        if document["integrity"]["content_sha256"] != _content_digest(document):
            raise FastSaveRefused(
                "READBACK_FAILED",
                "the temp-file readback integrity digest does not match its "
                "canonical bytes",
            )
    except FastSaveRefused as error:
        raise FastSaveRefused(
            error.reason_code,
            error.reason + "; the previous checkpoint is untouched and the target "
            "was never opened for writing." + _discard_temp(temp_path),
        ) from error
    try:
        os.replace(temp_path, target)
    except OSError as error:
        raise FastSaveRefused(
            "REPLACE_FAILED",
            "the atomic replace failed before it took effect; the previous "
            "checkpoint is untouched: " + str(error) + _discard_temp(temp_path),
        ) from error
    return payload


def _confirm_after_replace(
    target: Path, verified: bytes, previous: Mapping[str, Any] | None
) -> dict[str, Any]:
    """The OPTIONAL post-replace confirmation, reported as a distinct fact."""
    try:
        confirmed = read_checkpoint_bounded(target)
    except FastSaveRefused as error:
        return {
            "performed": True,
            "subject": "target-after-replace",
            "complete": False,
            "integrity_verified": False,
            "reason": error.reason,
            "post_replace_fact": (
                "the target WAS replaced; the previous checkpoint is not "
                "recoverable in place. This is a post-replace fact and is never "
                "reported as a pre-replace FAILED."
            ),
            "pre_save_digest": None if previous is None else previous["content_sha256"],
        }
    verified_digest = json.loads(verified.decode("utf-8"))["integrity"]["content_sha256"]
    return {
        "performed": True,
        "subject": "target-after-replace",
        "complete": True,
        "integrity_verified": True,
        "bytes_read": len(verified),
        "max_bytes": MAX_CHECKPOINT_BYTES,
        "content_sha256": confirmed["integrity"]["content_sha256"],
        "matches_verified_bytes": confirmed["integrity"]["content_sha256"] == verified_digest,
        "note": (
            "confirmation only: the binding verification ran on the temp file "
            "before os.replace, so this outcome never converts a replaced "
            "checkpoint into a pre-replace FAILED"
        ),
    }


def capture(
    request: SaveRequest, checkpoint_path: Path, *, invocation_phrase: str
) -> SaveResult:
    """The single entry point: guard, build, serialize, verify, replace."""
    started = time.monotonic()
    target = Path(checkpoint_path)
    path_text = os.fspath(target)
    try:
        guard_target(target)
        previous = _previous_valid_checkpoint(target)
        document = build_checkpoint(
            request,
            invocation_phrase=invocation_phrase,
            now=datetime.now(timezone.utc),
            previous=previous,
            measured_seconds=time.monotonic() - started,
            durable_location=_durable_location(target),
        )
        _scan_for_secrets(document, "the checkpoint document")
        for _ in range(4):
            payload = json.dumps(
                document, sort_keys=True, indent=2, ensure_ascii=True
            ).encode("utf-8")
            if document["bounded_readback"]["bytes_read"] == len(payload):
                break
            document["bounded_readback"]["bytes_read"] = len(payload)
        # The bytes_read update is inside the digest's input, so the digest is
        # recomputed over the final document before it is written.
        document["integrity"]["content_sha256"] = _content_digest(document)
        payload = json.dumps(
            document, sort_keys=True, indent=2, ensure_ascii=True
        ).encode("utf-8")
        if len(payload) > MAX_CHECKPOINT_BYTES:
            raise FastSaveRefused(
                "CHECKPOINT_TOO_LARGE",
                "the serialized checkpoint is " + str(len(payload)) + " bytes, "
                "above the " + str(MAX_CHECKPOINT_BYTES) + "-byte bound; nothing "
                "is written",
            )
    except FastSaveRefused as error:
        return SaveResult(
            "FAILED", error.reason_code, error.reason, None, path_text, None, None, None
        )
    try:
        verified = write_checkpoint_atomically(target, payload)
    except FastSaveRefused as error:
        return SaveResult(
            "FAILED", error.reason_code, error.reason, None, path_text, None, None, None
        )
    readback = dict(document["bounded_readback"])
    readback["post_replace_confirmation"] = _confirm_after_replace(target, verified, previous)
    return SaveResult(
        "SAVED",
        "SAVED",
        "the checkpoint was verified before os.replace and is now in place",
        document,
        path_text,
        _durable_location(target),
        readback,
        request.one_line_resume,
    )
