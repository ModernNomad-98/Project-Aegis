"""Canonical, globally unique identities (design §13, §20a-S25).

case_uid       = <target-owner>::<eval-file-kind>::<case-id>::<case-definition-hash>
assertion_uid  = <case_uid>::<assertion-index>::<assertion-content-hash>
attempt id     = (run_id, case_uid, repetition_number)

Bare case ids are never runner keys; identical assertion text in two cases
yields two distinct assertion_uids; editing a case changes its case_uid.
"""

from __future__ import annotations

from typing import Any, NamedTuple

from .canonical import canonical_bytes, sha256_hex, sha256_hex_text
from .enums import EvalFileKind
from .errors import IdentityError

SEPARATOR = "::"


def _require_component(name: str, value: str) -> str:
    if not isinstance(value, str) or not value:
        raise IdentityError(f"{name} must be a non-empty string, got {value!r}")
    if SEPARATOR in value:
        raise IdentityError(f"{name} must not contain {SEPARATOR!r}: {value!r}")
    return value


def case_definition_hash(case_definition: dict[str, Any]) -> str:
    """SHA-256 over the canonical representation of the authored case."""
    if not isinstance(case_definition, dict):
        raise IdentityError(
            f"case definition must be a dict, got {type(case_definition).__name__}"
        )
    return sha256_hex(canonical_bytes(case_definition))


def build_case_uid(
    target_owner: str,
    eval_file_kind: EvalFileKind | str,
    case_id: str,
    case_definition: dict[str, Any],
) -> str:
    owner = _require_component("target_owner", target_owner)
    kind = EvalFileKind.parse(eval_file_kind)
    cid = _require_component("case_id", case_id)
    return SEPARATOR.join(
        (owner, kind.value, cid, case_definition_hash(case_definition))
    )


def build_assertion_uid(case_uid: str, assertion_index: int, assertion_text: str) -> str:
    parse_case_uid(case_uid)  # validates shape
    if not isinstance(assertion_index, int) or isinstance(assertion_index, bool):
        raise IdentityError(f"assertion_index must be int, got {assertion_index!r}")
    if assertion_index < 0:
        raise IdentityError(f"assertion_index must be >= 0, got {assertion_index}")
    if not isinstance(assertion_text, str) or not assertion_text:
        raise IdentityError("assertion_text must be a non-empty string")
    return SEPARATOR.join(
        (case_uid, str(assertion_index), sha256_hex_text(assertion_text))
    )


class CaseUidParts(NamedTuple):
    target_owner: str
    eval_file_kind: EvalFileKind
    case_id: str
    definition_hash: str


def parse_case_uid(case_uid: str) -> CaseUidParts:
    if not isinstance(case_uid, str):
        raise IdentityError(f"case_uid must be str, got {type(case_uid).__name__}")
    parts = case_uid.split(SEPARATOR)
    if len(parts) != 4:
        raise IdentityError(f"case_uid must have 4 '::' components: {case_uid!r}")
    owner, kind_raw, case_id, definition_hash = parts
    _require_component("target_owner", owner)
    kind = EvalFileKind.parse(kind_raw)
    _require_component("case_id", case_id)
    if len(definition_hash) != 64 or any(
        c not in "0123456789abcdef" for c in definition_hash
    ):
        raise IdentityError(
            f"case-definition hash must be 64 lowercase hex chars: {definition_hash!r}"
        )
    return CaseUidParts(owner, kind, case_id, definition_hash)


class AttemptIdentity(NamedTuple):
    run_id: str
    case_uid: str
    repetition_number: int


def attempt_identity(run_id: str, case_uid: str, repetition_number: int) -> AttemptIdentity:
    if not isinstance(run_id, str) or not run_id:
        raise IdentityError("run_id must be a non-empty string")
    parse_case_uid(case_uid)
    if (
        not isinstance(repetition_number, int)
        or isinstance(repetition_number, bool)
        or repetition_number < 1
    ):
        raise IdentityError(
            f"repetition_number must be an int >= 1, got {repetition_number!r}"
        )
    return AttemptIdentity(run_id, case_uid, repetition_number)
