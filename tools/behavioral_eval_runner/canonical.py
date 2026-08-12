"""Canonical JSON encoding and hashing.

The canonical form is the single byte representation used for every identity
hash and manifest hash in the runner: UTF-8, sorted keys, minimal separators,
ASCII-escaped, NaN/Infinity rejected, string keys only. Two semantically equal
JSON documents always produce identical canonical bytes, so hashes are stable
under no-op serialization round-trips.
"""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any

from .errors import CanonicalizationError

_ALLOWED_SCALARS = (str, int, bool, type(None))


def _validate(obj: Any, path: str = "$") -> None:
    if isinstance(obj, dict):
        for key, value in obj.items():
            if not isinstance(key, str):
                raise CanonicalizationError(
                    f"non-string key {key!r} at {path} cannot be canonicalized"
                )
            _validate(value, f"{path}.{key}")
        return
    if isinstance(obj, (list, tuple)):
        for index, value in enumerate(obj):
            _validate(value, f"{path}[{index}]")
        return
    if isinstance(obj, bool) or obj is None or isinstance(obj, (str, int)):
        return
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            raise CanonicalizationError(f"non-finite float at {path}")
        return
    raise CanonicalizationError(
        f"type {type(obj).__name__} at {path} cannot be canonicalized"
    )


def canonical_json(obj: Any) -> str:
    """Return the canonical JSON text for ``obj`` (raises on unrepresentable input)."""
    _validate(obj)
    try:
        return json.dumps(
            obj,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:  # defense in depth after _validate
        raise CanonicalizationError(str(exc)) from exc


def canonical_bytes(obj: Any) -> bytes:
    return canonical_json(obj).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    if not isinstance(data, (bytes, bytearray)):
        raise CanonicalizationError(
            f"sha256_hex expects bytes, got {type(data).__name__}"
        )
    return hashlib.sha256(bytes(data)).hexdigest()


def sha256_hex_text(text: str) -> str:
    if not isinstance(text, str):
        raise CanonicalizationError(
            f"sha256_hex_text expects str, got {type(text).__name__}"
        )
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_of_obj(obj: Any) -> str:
    """SHA-256 of the canonical bytes of ``obj``."""
    return sha256_hex(canonical_bytes(obj))


def sha256_file(path: str, chunk_size: int = 1 << 20) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def is_roundtrip_stable(obj: Any) -> bool:
    """True when serialize→parse→serialize yields identical canonical bytes."""
    first = canonical_bytes(obj)
    reparsed = json.loads(first.decode("utf-8"))
    return canonical_bytes(reparsed) == first
