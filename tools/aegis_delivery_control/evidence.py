"""Canonical evidence helpers for synthetic kernel records."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Mapping

from .contracts import DispatchDenied


def canonical_bytes(record: Mapping[str, object]) -> bytes:
    return json.dumps(
        record,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def write_new_evidence(path: Path, record: Mapping[str, object]) -> str:
    """Create one immutable synthetic evidence file and return its SHA-256."""
    payload = canonical_bytes(record)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(payload)
        stream.flush()
    return hashlib.sha256(payload).hexdigest()


def verify_synthetic_evidence(
    original: bytes, *, expected_hash: str, expected_binding: str,
    expected_writer: str, expected_stage: str,
) -> dict[str, object]:
    """Verify original bytes and the one closed synthetic fixture payload."""
    try:
        if any(type(value) is not str or not value.strip() for value in (
            expected_binding, expected_writer, expected_stage,
        )):
            raise ValueError("invalid synthetic evidence identity")
        record = json.loads(original.decode("ascii"))
        if not isinstance(record, dict) or canonical_bytes(record) != original:
            raise ValueError("noncanonical evidence")
        if (set(record) != {"version", "binding", "writer", "stage", "payload"}
                or type(record["version"]) is not int or record["version"] != 1
                or record["binding"] != expected_binding
                or record["writer"] != expected_writer
                or record["stage"] != expected_stage
                or record["payload"] != {"receipt": "synthetic"}):
            raise ValueError("unverifiable or sensitive evidence")
        if hashlib.sha256(original).hexdigest() != expected_hash:
            raise ValueError("evidence hash mismatch")
    except (UnicodeError, json.JSONDecodeError, TypeError, ValueError) as error:
        raise DispatchDenied("synthetic evidence verification failed") from error
    return record
