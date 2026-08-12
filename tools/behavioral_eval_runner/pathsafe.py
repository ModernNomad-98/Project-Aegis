"""Strict, cross-platform relative-path validation and reparse-safe joins.

Shared by the materializer and the evidence writer so both fail closed on the
same class of unsafe paths: traversal (``..``), absolute paths, drive letters,
NTFS alternate-data-stream markers (``:``), trailing dots/spaces, Windows
reserved device names, and reparse points anywhere along a resolved chain.
"""

from __future__ import annotations

import os
import stat

_WINDOWS_DEVICE_NAMES = frozenset(
    {
        "con",
        "prn",
        "aux",
        "nul",
        *(f"com{i}" for i in range(1, 10)),
        *(f"lpt{i}" for i in range(1, 10)),
    }
)

_REPARSE_FLAG = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)


class UnsafePathError(ValueError):
    """A relative path is unsafe for materialization or evidence writing."""


def normalize_relative_path(relative_path: str) -> str:
    """Validate a repo-relative path and return it with forward slashes.

    Raises UnsafePathError on any traversal/absolute/drive/ADS/device/trailing
    unsafe segment. Never touches the filesystem.
    """
    if not isinstance(relative_path, str) or not relative_path:
        raise UnsafePathError(f"invalid path: {relative_path!r}")
    normalized = relative_path.replace("\\", "/")
    if normalized.startswith("/"):
        raise UnsafePathError(f"absolute path refused: {relative_path!r}")
    parts = normalized.split("/")
    for part in parts:
        if part in ("", ".", ".."):
            raise UnsafePathError(f"path traversal refused: {relative_path!r}")
        if ":" in part:
            raise UnsafePathError(
                f"drive letter or alternate-data-stream marker refused: "
                f"{relative_path!r}"
            )
        if part != part.rstrip(" ."):
            raise UnsafePathError(
                f"trailing dot/space segment refused: {relative_path!r}"
            )
        stem = part.split(".", 1)[0].lower()
        if stem in _WINDOWS_DEVICE_NAMES:
            raise UnsafePathError(
                f"Windows reserved device name refused: {relative_path!r}"
            )
    return normalized


def refuse_reparse_chain(path: str, boundary_root: str) -> None:
    """Refuse reparse points from ``boundary_root`` down through ``path``.

    lstats every existing component between the (inclusive) boundary root and
    the target so a symlink/junction/mount planted below the root cannot
    redirect a read or write outside it. Fail closed.
    """
    probe = os.path.abspath(path)
    root = os.path.abspath(boundary_root)
    chain: list[str] = []
    while True:
        chain.append(probe)
        if os.path.normcase(probe) == os.path.normcase(root):
            break
        parent = os.path.dirname(probe)
        if parent == probe:
            break
        probe = parent
    for component in chain:
        if not os.path.exists(component) and not os.path.islink(component):
            continue
        info = os.lstat(component)
        if stat.S_ISLNK(info.st_mode):
            raise UnsafePathError(f"symlink refused in path chain: {component}")
        if getattr(info, "st_file_attributes", 0) & _REPARSE_FLAG:
            raise UnsafePathError(f"reparse point refused in path chain: {component}")


def refuse_reparse_ancestors(root: str) -> None:
    """Refuse reparse points from the volume root up to (and incl.) ``root``."""
    probe = os.path.abspath(root)
    chain: list[str] = []
    while True:
        chain.append(probe)
        parent = os.path.dirname(probe)
        if parent == probe:
            break
        probe = parent
    for component in chain:
        if not os.path.exists(component) and not os.path.islink(component):
            continue
        info = os.lstat(component)
        if stat.S_ISLNK(info.st_mode):
            raise UnsafePathError(f"symlink in ancestor chain: {component}")
        if getattr(info, "st_file_attributes", 0) & _REPARSE_FLAG:
            raise UnsafePathError(f"reparse point in ancestor chain: {component}")


def safe_join(root: str, relative_path: str) -> str:
    """Join ``relative_path`` under ``root``, refusing any escape or reparse.

    Uses realpath on the root so a reparse-pointed root resolves once; the
    per-component reparse check then covers anything planted below it.
    """
    relative = normalize_relative_path(relative_path)
    root_real = os.path.realpath(root)
    joined = os.path.abspath(os.path.join(root_real, *relative.split("/")))
    if os.path.commonpath([root_real, joined]) != root_real:
        raise UnsafePathError(f"{relative_path!r} escapes {root!r}")
    return joined
