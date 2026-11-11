"""Closed change-state schemas, canonicalization and provenance envelopes.

Every producer record is one JSON envelope:

    {"payload": {...record...},
     "provenance": {"source_ref", "as_of", "producer_role",
                    "producer_identity_ref", "declared_payload_sha256",
                    "declared_payload_bytes", "status"?}}

The declared payload hash covers the *canonical* serialization of the payload
(JCS-RFC8785-v1), so the binding is not circular and a consumer can always
re-derive it.  A declared hash is never trusted where bytes can be re-hashed.

The schemas here are closed: an unexpected field is
CANONICAL_FIELD_MISSING_OR_MISMATCH, a missing required field is
REQUIRED_INPUT_UNAVAILABLE.  The verdict field list is NOT restated here - the
merged checker's catalogue (tools/aegis_verdict_gate/catalogue.py) remains the
only in-code field list; these are the *input record* schemas the checker
consumes.

Standard library only; no network; no writes.
"""

from __future__ import annotations

import hashlib
import json
import math
import typing

from . import (
    FREEZE_SCHEMA_VERSION,
    HEAD_HISTORY_SCHEMA_VERSION,
    SCHEMA_VERSION,
    SETTLEMENT_SCHEMA_VERSION,
    SNAPSHOT_FLAGS,
    SNAPSHOT_FORMAT_VERSION,
    SNAPSHOT_METHOD,
    SNAPSHOT_SCHEMA_VERSION,
    STAGE_SCHEMA_VERSION,
)

# Blocker codes reused verbatim from the merged checker's contract vocabulary.
CODE_CANONICAL = "CANONICAL_FIELD_MISSING_OR_MISMATCH"
CODE_REQUIRED_INPUT = "REQUIRED_INPUT_UNAVAILABLE"
CODE_HEAD_MOVED = "HEAD_MOVED_OR_BASE_INVALIDATED"
CODE_STAGE = "STAGE_VERDICT_NOT_ACCEPTED"
CODE_MISSING_REVIEW = "MISSING_REQUIRED_REVIEW_OR_DISPOSITION"
CODE_TAMPER = "STATE_TAMPER_SUSPECTED"
CODE_AUTHORITY_ABSENT = "AUTHORITY_ABSENT"
CODE_BUDGET = "REVIEW_BUDGET_EXHAUSTED"
CODE_STALE = "VERDICT_STALE_OR_UNVERIFIED"

PRE_AUDIT_STATES = ("pass", "fail", "neutral", "unrun", "bypassed")
REVIEW_SOURCE_STATES = ("SETTLED", "PENDING", "UNAVAILABLE_DISPOSITIONED")
INPUT_STATUSES = ("VERIFIED", "UNVERIFIED", "ABSENT")
INDEPENDENCE_CLASSES = ("INDEPENDENT", "SELF", "UNKNOWN")
STAGE_VERDICTS = {"B": ("ACCEPT", "REVISE"), "D": ("ACCEPT", "REVISE"), "E": ("PASS", "FAIL")}
AFFIRMATIVE_STAGE = {"B": "ACCEPT", "D": "ACCEPT", "E": "PASS"}
STAGES = ("B", "D", "E")
HEAD_EVENT_KINDS = ("INITIAL", "BATCHED_BLOCKING_FIX", "FINAL_BLOCKING_FIX", "EXCEPTION", "RESYNC")
ASSURANCE_CLAIMS = ("NONE", "AUDITABLE")
COVERAGE_STATES = ("UNKNOWN",)

DISPOSITION_AUTHORITY_SCHEMA = "aegis.disposition-authority/v1"
DISPOSITION_DECISION = "UNAVAILABLE_REVIEW"
DISPOSITION_SCOPE_FIELDS = ("repo", "change_id", "head_sha", "merge_target_ref")


class SchemaError(ValueError):
    """The supplied document is not a change-state record at all (exit 2)."""


class Issue(typing.NamedTuple):
    """One finding, carrying the merged checker's blocker code where it maps."""

    code: str
    detail: str

    def as_dict(self) -> typing.Dict[str, str]:
        return {"code": self.code, "detail": self.detail}


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _encode_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _encode_number(value: typing.Union[int, float]) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if not math.isfinite(value):
        raise SchemaError("non-finite number is not representable in JCS")
    if value == int(value) and abs(value) < 1e21:
        return str(int(value))
    text = repr(value)
    if "e" in text or "E" in text:
        mantissa, _, exponent = text.partition("e")
        sign = "+" if not exponent.startswith("-") else "-"
        digits = exponent.lstrip("+-").lstrip("0") or "0"
        text = mantissa + "e" + sign + digits
    return text


def _encode(value: object) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int) or isinstance(value, float):
        return _encode_number(value)
    if isinstance(value, str):
        return _encode_string(value)
    if isinstance(value, (list, tuple)):
        return "[" + ",".join(_encode(item) for item in value) + "]"
    if isinstance(value, dict):
        for key in value:
            if not isinstance(key, str):
                raise SchemaError("object keys must be strings")
        items = sorted(value.items(), key=lambda pair: pair[0].encode("utf-16-be"))
        return "{" + ",".join(_encode_string(key) + ":" + _encode(item) for key, item in items) + "}"
    raise SchemaError("unsupported value type: %s" % type(value).__name__)


def dumps(value: object) -> str:
    """Serialize a value per JCS-RFC8785-v1."""

    return _encode(value)


def canonical_bytes(value: object) -> bytes:
    return dumps(value).encode("utf-8")


def digest(value: object) -> str:
    return sha256_hex(canonical_bytes(value))


def is_hex(value: object, length: int) -> bool:
    return (
        isinstance(value, str)
        and len(value) == length
        and not (set(value) - set("0123456789abcdef"))
    )


# ---------------------------------------------------------------------------
# Field tables (closed schemas)
# ---------------------------------------------------------------------------

# kind grammar: str|int|bool|list|dict|hex40|hex64|str?|hex64?|dict?|
#               =const | in:a,b,c
Field = typing.Tuple[str, str]

IMMUTABLE_INPUT_FIELDS: typing.Tuple[Field, ...] = (
    ("head_sha", "hex40"),
    ("tree_sha", "hex40"),
    ("base_sha", "hex40"),
    ("policy_sha256", "hex64"),
    ("plan_sha256", "hex64"),
    ("evidence_inputs_sha256", "hex64"),
)

MUTATION_EVENT_FIELDS: typing.Tuple[Field, ...] = (
    ("event_kind", "in:REFREEZE_ATTEMPT,BASE_MOVE,HEAD_MOVE,MUTATION"),
    ("at", "str"),
    ("evidence_ref", "str"),
)

FREEZE_FIELDS: typing.Tuple[Field, ...] = (
    ("schema_version", "=" + FREEZE_SCHEMA_VERSION),
    ("freeze_id", "str"),
    ("change_id", "str"),
    ("candidate_id", "str"),
    ("head_sha", "hex40"),
    ("tree_sha", "hex40"),
    ("base_sha", "hex40"),
    ("base_ref", "str"),
    ("frozen_at", "str"),
    ("frozen_by", "str"),
    ("immutable_inputs", "dict"),
    ("immutable_inputs_sha256", "hex64"),
    ("mutation_events", "list"),
    ("settlement_ref", "str"),
    ("valid", "bool"),
)

PRE_AUDIT_CHECK_FIELDS: typing.Tuple[Field, ...] = (
    ("check_id", "str"),
    ("state", "in:" + ",".join(PRE_AUDIT_STATES)),
    ("evidence_ref", "str"),
    ("note", "str?"),
)

REVIEW_SOURCE_FIELDS: typing.Tuple[Field, ...] = (
    ("source_id", "str"),
    ("role", "str"),
    ("required", "bool"),
    ("state", "in:" + ",".join(REVIEW_SOURCE_STATES)),
    ("evidence_ref", "str"),
    ("disposition_authority_ref", "str?"),
    ("disposition_authority_sha256", "hex64?"),
    ("disposition_authority_id", "str?"),
    ("disposition_scope", "dict?"),
    ("expires", "str?"),
)

SETTLEMENT_FIELDS: typing.Tuple[Field, ...] = (
    ("schema_version", "=" + SETTLEMENT_SCHEMA_VERSION),
    ("settlement_id", "str"),
    ("change_id", "str"),
    ("as_of", "str"),
    ("settled_by", "str"),
    ("pre_audit_checks", "list"),
    ("review_sources", "list"),
    ("settled", "bool"),
)

STAGE_DECLARATION_FIELDS: typing.Tuple[Field, ...] = (
    ("schema_version", "=" + STAGE_SCHEMA_VERSION),
    ("change_id", "str"),
    ("stage", "in:" + ",".join(STAGES)),
    ("record_id", "str"),
    ("record_path", "str"),
    ("bytes", "int"),
    ("sha256", "hex64"),
    ("head_sha", "hex40"),
    ("verdict", "str"),
    ("holder_identity_ref", "str"),
    ("independence_class", "in:" + ",".join(INDEPENDENCE_CLASSES)),
    ("snapshot_identity", "str"),
    ("completed_at", "str"),
    ("applicability", "in:REQUIRED,WAIVED"),
    ("waiver_ref", "str?"),
    ("replacement_of", "str?"),
)

STAGE_RECORD_BODY_FIELDS: typing.Tuple[Field, ...] = (
    ("stage", "in:" + ",".join(STAGES)),
    ("record_id", "str"),
    ("change_id", "str"),
    ("head_sha", "hex40"),
    ("verdict", "str"),
    ("reviewer_role", "str"),
    ("completed_at", "str"),
    ("notes", "str?"),
)

SNAPSHOT_MANIFEST_FIELDS: typing.Tuple[Field, ...] = (
    ("schema_version", "=" + SNAPSHOT_SCHEMA_VERSION),
    ("snapshot_id", "str"),
    ("change_id", "str"),
    ("method", "=" + SNAPSHOT_METHOD),
    ("format_version", "=" + SNAPSHOT_FORMAT_VERSION),
    ("commit", "hex40"),
    ("tree", "hex40"),
    ("base", "hex40"),
    ("archive_sha256", "hex64"),
    ("archive_bytes", "int"),
    ("file_count", "int"),
    ("flags", "list"),
    ("retention_ref", "str"),
    ("created_by", "str"),
    ("created_at", "str"),
)

HEAD_ENTRY_FIELDS: typing.Tuple[Field, ...] = (
    ("seq", "int"),
    ("head_sha", "hex40"),
    ("kind", "in:" + ",".join(HEAD_EVENT_KINDS)),
    ("exception_ref", "str?"),
    ("counted_at", "str"),
)

HEAD_HISTORY_FIELDS: typing.Tuple[Field, ...] = (
    ("schema_version", "=" + HEAD_HISTORY_SCHEMA_VERSION),
    ("change_id", "str"),
    ("candidate_head", "hex40"),
    ("heads", "list"),
    ("export_ref", "str"),
    ("exported_at", "str"),
)

LEDGER_EVENT_FIELDS: typing.Tuple[Field, ...] = (
    ("seq", "int"),
    ("head_sha", "hex40"),
    ("kind", "in:" + ",".join(HEAD_EVENT_KINDS)),
    ("exception_ref", "str?"),
    ("counted_at", "str"),
    ("recorded_by", "str"),
    ("prev_event_sha256", "hex64?"),
)

MANIFEST_FILE_FIELDS: typing.Tuple[Field, ...] = (
    ("path", "str"),
    ("kind", "str"),
    ("id", "str"),
    ("bytes", "int"),
    ("sha256", "hex64"),
    ("event_count", "int?"),
)

PROVENANCE_BINDING_FIELDS: typing.Tuple[Field, ...] = (
    ("authority_kind", "in:UNKNOWN,REGISTER_ENTRY,OWNER_LINE_RECORD"),
    ("authority_ref_id", "str?"),
    ("authority_ref_sha256", "hex64?"),
    ("holder_role", "str"),
    ("holder_identity_ref", "str?"),
    ("binding_status", "in:VERIFIED,UNVERIFIED,ABSENT"),
    ("unverified_reason", "str?"),
    ("binding_commit_or_pr", "str?"),
)

CHANGE_STATE_MANIFEST_FIELDS: typing.Tuple[Field, ...] = (
    ("schema_version", "=" + SCHEMA_VERSION),
    ("change_id", "str"),
    ("files", "list"),
    ("derived_counts_at_binding", "dict"),
    ("store_digest", "hex64"),
    ("assurance_claim", "str"),
    ("mounted_coverage", "str"),
    ("provenance_binding", "dict"),
)

PROVENANCE_FIELDS: typing.Tuple[Field, ...] = (
    ("source_ref", "str"),
    ("as_of", "str"),
    ("producer_role", "str"),
    ("producer_identity_ref", "str"),
    ("declared_payload_sha256", "hex64"),
    ("declared_payload_bytes", "int"),
    ("status", "in:" + ",".join(INPUT_STATUSES) + "?"),
)

SCHEMAS: typing.Dict[str, typing.Tuple[Field, ...]] = {
    "freeze": FREEZE_FIELDS,
    "settlement": SETTLEMENT_FIELDS,
    "stage": STAGE_DECLARATION_FIELDS,
    "stage_record": STAGE_RECORD_BODY_FIELDS,
    "snapshot": SNAPSHOT_MANIFEST_FIELDS,
    "head_history": HEAD_HISTORY_FIELDS,
    "ledger_event": LEDGER_EVENT_FIELDS,
    "manifest": CHANGE_STATE_MANIFEST_FIELDS,
}


def _check_value(value: object, kind: str) -> bool:
    if kind == "str":
        return isinstance(value, str) and bool(value)
    if kind == "int":
        return isinstance(value, int) and not isinstance(value, bool)
    if kind == "int?":
        return value is None or (isinstance(value, int) and not isinstance(value, bool))
    if kind == "bool":
        return isinstance(value, bool)
    if kind == "list":
        return isinstance(value, list)
    if kind == "dict":
        return isinstance(value, dict)
    if kind == "hex40":
        return is_hex(value, 40)
    if kind == "hex64":
        return is_hex(value, 64)
    if kind == "str?":
        return value is None or isinstance(value, str)
    if kind == "hex64?":
        return value is None or is_hex(value, 64)
    if kind == "dict?":
        return value is None or isinstance(value, dict)
    if kind.startswith("="):
        return value == kind[1:]
    if kind.startswith("in:"):
        return value in kind[3:].split(",")
    raise SchemaError("unknown field kind: %s" % kind)


def closed_schema_issues(
    payload: typing.Mapping[str, object],
    fields: typing.Sequence[Field],
    prefix: str = "",
    *,
    allow_optional_missing: bool = False,
) -> typing.List[Issue]:
    """Validate a closed field table against a payload: no extras, no gaps."""

    issues: typing.List[Issue] = []
    known = {name for name, _ in fields}
    for name, kind in fields:
        if name not in payload:
            if allow_optional_missing or kind.endswith("?"):
                continue
            issues.append(Issue(CODE_REQUIRED_INPUT, "%s%s is missing" % (prefix, name)))
            continue
        if not _check_value(payload[name], kind):
            issues.append(Issue(CODE_CANONICAL, "%s%s is not a valid %s" % (prefix, name, kind)))
    for name in sorted(payload):
        if name not in known:
            issues.append(Issue(CODE_CANONICAL, "%s%s is not a field of this closed schema" % (prefix, name)))
    return issues


def _object_list_issues(
    values: object, fields: typing.Sequence[Field], prefix: str
) -> typing.List[Issue]:
    if not isinstance(values, list):
        return [Issue(CODE_REQUIRED_INPUT, "%s is not a list" % prefix.rstrip("."))]
    issues: typing.List[Issue] = []
    for index, value in enumerate(values):
        if not isinstance(value, dict):
            issues.append(Issue(CODE_CANONICAL, "%s[%d] is not an object" % (prefix, index)))
            continue
        issues.extend(closed_schema_issues(value, fields, "%s[%d]." % (prefix, index)))
    return issues


def payload_issues(kind: str, payload: typing.Mapping[str, object]) -> typing.List[Issue]:
    """Validate one payload against its closed schema (and its nested rows)."""

    if kind not in SCHEMAS:
        raise SchemaError("unknown record kind: %s" % kind)
    issues = closed_schema_issues(payload, SCHEMAS[kind])
    if kind == "freeze":
        nested = payload.get("immutable_inputs")
        if isinstance(nested, dict):
            issues.extend(closed_schema_issues(nested, IMMUTABLE_INPUT_FIELDS, "immutable_inputs."))
        events = payload.get("mutation_events")
        if isinstance(events, list):
            issues.extend(_object_list_issues(events, MUTATION_EVENT_FIELDS, "mutation_events"))
    elif kind == "settlement":
        issues.extend(
            _object_list_issues(payload.get("pre_audit_checks"), PRE_AUDIT_CHECK_FIELDS, "pre_audit_checks")
        )
        issues.extend(_object_list_issues(payload.get("review_sources"), REVIEW_SOURCE_FIELDS, "review_sources"))
    elif kind == "snapshot":
        flags = payload.get("flags")
        if isinstance(flags, list) and list(flags) != list(SNAPSHOT_FLAGS):
            issues.append(
                Issue(CODE_CANONICAL, "snapshot flags are not the pinned %s" % (list(SNAPSHOT_FLAGS),))
            )
    elif kind == "head_history":
        issues.extend(_object_list_issues(payload.get("heads"), HEAD_ENTRY_FIELDS, "heads"))
    elif kind == "manifest":
        issues.extend(_object_list_issues(payload.get("files"), MANIFEST_FILE_FIELDS, "files"))
        binding = payload.get("provenance_binding")
        if isinstance(binding, dict):
            issues.extend(closed_schema_issues(binding, PROVENANCE_BINDING_FIELDS, "provenance_binding."))
    return issues


def build_envelope(
    payload: typing.Mapping[str, object],
    *,
    source_ref: str,
    as_of: str,
    producer_role: str,
    producer_identity_ref: str,
    status: typing.Optional[str] = None,
) -> typing.Dict[str, object]:
    """Build one provenance envelope.  Deterministic for identical inputs."""

    provenance: typing.Dict[str, object] = {
        "source_ref": source_ref,
        "as_of": as_of,
        "producer_role": producer_role,
        "producer_identity_ref": producer_identity_ref,
        "declared_payload_sha256": digest(payload),
        "declared_payload_bytes": len(canonical_bytes(payload)),
    }
    if status is not None:
        provenance["status"] = status
    return {"payload": dict(payload), "provenance": provenance}


def envelope_issues(document: object, label: str = "envelope") -> typing.List[Issue]:
    """Validate one envelope's structure and its declared payload binding."""

    issues: typing.List[Issue] = []
    if not isinstance(document, dict):
        return [Issue(CODE_CANONICAL, "%s is not a JSON object" % label)]
    for name in sorted(document):
        if name not in ("payload", "provenance"):
            issues.append(Issue(CODE_CANONICAL, "%s.%s is not an envelope field" % (label, name)))
    payload = document.get("payload")
    if not isinstance(payload, dict):
        issues.append(Issue(CODE_CANONICAL, "%s has no payload object" % label))
        return issues
    provenance = document.get("provenance")
    if not isinstance(provenance, dict):
        issues.append(Issue(CODE_REQUIRED_INPUT, "%s has no provenance block" % label))
        return issues
    issues.extend(closed_schema_issues(provenance, PROVENANCE_FIELDS, "%s.provenance." % label))
    if provenance.get("declared_payload_sha256") != digest(payload):
        issues.append(Issue(CODE_CANONICAL, "%s declared payload hash does not match the payload" % label))
    if provenance.get("declared_payload_bytes") != len(canonical_bytes(payload)):
        issues.append(Issue(CODE_CANONICAL, "%s declared payload bytes do not match the payload" % label))
    return issues


def stage_record_consistency_issues(
    declaration: typing.Mapping[str, object], body: typing.Mapping[str, object]
) -> typing.List[Issue]:
    """A declaration must not be repurposed: the record body has to agree."""

    issues: typing.List[Issue] = []
    if body.get("stage") != declaration.get("stage"):
        issues.append(
            Issue(
                CODE_STAGE,
                "stage declaration %s declares %r but its record body declares %r"
                % (declaration.get("record_id"), declaration.get("stage"), body.get("stage")),
            )
        )
    if body.get("record_id") != declaration.get("record_id"):
        issues.append(Issue(CODE_STAGE, "stage record body id disagrees with the declaration"))
    if body.get("head_sha") != declaration.get("head_sha"):
        issues.append(Issue(CODE_STAGE, "stage record body head disagrees with the declaration"))
    if body.get("verdict") != declaration.get("verdict"):
        issues.append(Issue(CODE_STAGE, "stage record body verdict disagrees with the declaration"))
    return issues


def immutable_inputs_digest(immutable_inputs: typing.Mapping[str, object]) -> str:
    """The merged checker's freeze re-derivation, over the same six terms."""

    return digest(
        {
            "head": immutable_inputs.get("head_sha"),
            "tree": immutable_inputs.get("tree_sha"),
            "base": immutable_inputs.get("base_sha"),
            "policy_sha256": immutable_inputs.get("policy_sha256"),
            "plan_sha256": immutable_inputs.get("plan_sha256"),
            "evidence_inputs_sha256": immutable_inputs.get("evidence_inputs_sha256"),
        }
    )


def load_json(path: object) -> object:
    """Read one UTF-8 JSON file; a parse failure is a fatal SchemaError."""

    from pathlib import Path

    file_path = Path(str(path))
    try:
        raw = file_path.read_bytes()
    except OSError as error:
        raise SchemaError("cannot read %s: %s" % (file_path, error))
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as error:
        raise SchemaError("%s is not valid UTF-8 JSON: %s" % (file_path, error))
