"""JCS-RFC8785-v1 canonicalization, bound-fields projection and self-test.

The contract (C03-M1 delta section 2.5, corrected by the v2.1 errata) fixes
the canonicalization algorithm and a self-test vector.  This module is the
single implementation of both:

  * dumps() / digest() implement RFC 8785 JSON Canonicalization Scheme for the
    value shapes the catalogue uses (objects, arrays, strings, booleans, null,
    integers; floats are supported defensively but are not used by the set).
  * project_bound_fields() builds the hashed R/O/C projection of a supplied
    verdict record: every present catalogue field of groups A..H, plus
    conditionals_applied, and nothing else.  VB-I01 (the hash itself) cannot
    hash itself and the G gate-time row is not a catalogue entry; both are
    excluded, as the contract requires.
  * self_test() reproduces the recorded v2.1 vector byte-for-byte:
    560 UTF-8 bytes / sha256 098ad54886568bbc7e9103839d5ceda9a573d01f7d234d58a8747913e331bd5d

Standard library only; no network, no I/O.
"""

from __future__ import annotations

import hashlib
import json
import math
import typing

from . import catalogue

SELF_TEST_BYTES = 560
SELF_TEST_SHA256 = "098ad54886568bbc7e9103839d5ceda9a573d01f7d234d58a8747913e331bd5d"

SELF_TEST_INPUT: typing.Dict[str, object] = {
    "bound_set_id": catalogue.BOUND_SET_ID,
    "bound_set_version": catalogue.BOUND_SET_VERSION,
    "canonicalization_version": catalogue.CANONICALIZATION_VERSION,
    "change": {"id": 42, "type": "PR"},
    "head_sha": "1111111111111111111111111111111111111111",
    "merge_target": {"ref": "refs/heads/main"},
    "repo": {"name": "example-repo", "owner": "example-org"},
    "reviewer": {
        "auth_method": "provider-event-author",
        "auth_verified": True,
        "identity_ref": "role-f-example",
        "independence": {
            "class": "INDEPENDENT",
            "distinct_from": ["implementer", "pr-author"],
        },
    },
    "tree_sha": "2222222222222222222222222222222222222222",
    "verdict": {"value": "PASS"},
}

SELF_TEST_CANONICAL = (
    '{"bound_set_id":"aegis.verdict-bound/v2.1","bound_set_version":"2.1",'
    '"canonicalization_version":"JCS-RFC8785-v1","change":{"id":42,"type":"PR"},'
    '"head_sha":"1111111111111111111111111111111111111111",'
    '"merge_target":{"ref":"refs/heads/main"},'
    '"repo":{"name":"example-repo","owner":"example-org"},'
    '"reviewer":{"auth_method":"provider-event-author","auth_verified":true,'
    '"identity_ref":"role-f-example","independence":{"class":"INDEPENDENT",'
    '"distinct_from":["implementer","pr-author"]}},'
    '"tree_sha":"2222222222222222222222222222222222222222",'
    '"verdict":{"value":"PASS"}}'
)


class CanonicalizationError(ValueError):
    """Raised when a value cannot be serialized per JCS-RFC8785-v1."""


def _encode_string(value: str) -> str:
    # json.dumps with ensure_ascii=False matches RFC 8785 string serialization
    # for the escaping rules used here: quote, reverse solidus and the short
    # control escapes, with other control characters as lowercase \u00xx.
    return json.dumps(value, ensure_ascii=False)


def _encode_number(value: typing.Union[int, float]) -> str:
    if isinstance(value, bool):  # defensive: bools are handled before numbers
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if not math.isfinite(value):
        raise CanonicalizationError("non-finite number is not representable in JCS")
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
                raise CanonicalizationError("object keys must be strings")
        items = sorted(value.items(), key=lambda pair: pair[0].encode("utf-16-be"))
        return "{" + ",".join(_encode_string(key) + ":" + _encode(item) for key, item in items) + "}"
    raise CanonicalizationError("unsupported value type: %s" % type(value).__name__)


def dumps(value: object) -> str:
    """Serialize a value per JCS-RFC8785-v1 (UTF-8 bytes when encoded)."""

    return _encode(value)


def canonical_bytes(value: object) -> bytes:
    return dumps(value).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(value: object) -> str:
    """SHA-256 (lowercase hex) over the canonical UTF-8 serialization."""

    return sha256_hex(canonical_bytes(value))


def project_bound_fields(document: typing.Mapping[str, object]) -> typing.Dict[str, object]:
    """Return the hashed R/O/C projection of a supplied verdict record.

    Takes every present catalogue field in groups A..H (the R/O/C projection,
    61 entries minus VB-I01) and drops everything else, including the declared
    metadata envelope and VB-I01 itself.  Unknown keys never reach the hash;
    the closed-schema check in gate.py rejects them separately (AC3).
    """

    projection: typing.Dict[str, object] = {}
    for entry in catalogue.hashed_entries():
        present, value = catalogue.get_path(document, entry.path)
        if present:
            catalogue.set_path(projection, entry.path, value)
    return projection


def bound_fields_sha256(document: typing.Mapping[str, object]) -> str:
    """Recompute VB-I01 over the canonical R/O/C projection."""

    return digest(project_bound_fields(document))


def self_test() -> typing.Dict[str, object]:
    """Reproduce the recorded v2.1 canonicalization vector.

    Returns a deterministic report.  ok is true only when the serialization
    matches the recorded line byte-for-byte, is exactly 560 UTF-8 bytes and
    hashes to the recorded SHA-256.
    """

    serialized = dumps(SELF_TEST_INPUT)
    encoded = serialized.encode("utf-8")
    actual_sha = sha256_hex(encoded)
    return {
        "vector": "aegis.verdict-bound/v2.1 canonicalization self-test",
        "ok": (
            serialized == SELF_TEST_CANONICAL
            and len(encoded) == SELF_TEST_BYTES
            and actual_sha == SELF_TEST_SHA256
        ),
        "bytes": len(encoded),
        "expected_bytes": SELF_TEST_BYTES,
        "sha256": actual_sha,
        "expected_sha256": SELF_TEST_SHA256,
        "serialization_matches": serialized == SELF_TEST_CANONICAL,
    }
