"""Canonical evidence helpers for synthetic kernel records."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Mapping


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