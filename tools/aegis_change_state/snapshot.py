"""Per-head immutable snapshot manifests (git archive of the exact commit).

A snapshot identity is *not* a copy of the writer's working tree.  It is the
archive of one commit:

    git -C <repo> archive --format=tar <commit>

with the method, format version and flags pinned in the manifest.  The
manifest binds commit/tree/base + archive sha256/bytes/file count + a retention
ref, and reproducibility is the test: re-running the same command on the same
commit must reproduce the same archive bytes.  The archive itself is retained
outside the repository under the authority that authorises the run; this
package never commits a binary and never copies the archive anywhere.

A snapshot whose commit/tree/base does not equal the frozen head's is
HEAD_MOVED_OR_BASE_INVALIDATED.  No network, standard library only.
"""

from __future__ import annotations

import io
import tarfile
import typing
from pathlib import Path

from . import SNAPSHOT_FLAGS, SNAPSHOT_FORMAT_VERSION, SNAPSHOT_METHOD, SNAPSHOT_SCHEMA_VERSION
from .schema import (
    CODE_CANONICAL,
    CODE_HEAD_MOVED,
    CODE_REQUIRED_INPUT,
    CODE_TAMPER,
    Issue,
    payload_issues,
    sha256_hex,
)

ARCHIVE_FLAGS = list(SNAPSHOT_FLAGS)


class SnapshotError(RuntimeError):
    """A snapshot could not be produced or resolved (invalid input)."""


def _git(repo_root: typing.Union[str, Path], *args: str) -> typing.Tuple[int, bytes, str]:
    import subprocess

    completed = subprocess.run(
        ["git", "-C", str(repo_root)] + list(args),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=300,
    )
    return (completed.returncode, completed.stdout, completed.stderr.decode("utf-8", "replace"))


def resolve_commit(repo_root: typing.Union[str, Path], revision: str) -> str:
    code, out, err = _git(repo_root, "rev-parse", "--verify", revision + "^{commit}")
    if code != 0:
        raise SnapshotError("revision %r does not resolve: %s" % (revision, err.strip()))
    return out.decode("utf-8", "replace").strip()


def tree_of(repo_root: typing.Union[str, Path], commit: str) -> str:
    code, out, err = _git(repo_root, "rev-parse", "--verify", commit + "^{tree}")
    if code != 0:
        raise SnapshotError("tree of %r does not resolve: %s" % (commit, err.strip()))
    return out.decode("utf-8", "replace").strip()


def archive(repo_root: typing.Union[str, Path], commit: str) -> bytes:
    """The pinned git-archive tar bytes of one commit (never the worktree)."""

    code, out, err = _git(repo_root, "archive", *ARCHIVE_FLAGS, commit)
    if code != 0:
        raise SnapshotError("git archive failed for %r: %s" % (commit, err.strip()))
    if not out:
        raise SnapshotError("git archive produced no bytes for %r" % commit)
    return out


def archive_file_count(archive_bytes: bytes) -> int:
    """Count regular files in the tar (directories are not files)."""

    try:
        with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:") as handle:
            return sum(1 for member in handle.getmembers() if member.isfile())
    except tarfile.TarError as error:
        raise SnapshotError("the archive is not a readable tar: %s" % error)


def build_manifest(
    repo_root: typing.Union[str, Path],
    commit: str,
    *,
    change_id: str,
    base: str,
    retention_ref: str,
    created_by: str,
    created_at: str,
    snapshot_id: typing.Optional[str] = None,
) -> typing.Dict[str, object]:
    """Build one snapshot manifest from the exact commit (caller supplies the clock)."""

    resolved = resolve_commit(repo_root, commit)
    tree = tree_of(repo_root, resolved)
    data = archive(repo_root, resolved)
    manifest: typing.Dict[str, object] = {
        "schema_version": SNAPSHOT_SCHEMA_VERSION,
        "snapshot_id": snapshot_id or ("snapshot:%s" % resolved),
        "change_id": change_id,
        "method": SNAPSHOT_METHOD,
        "format_version": SNAPSHOT_FORMAT_VERSION,
        "commit": resolved,
        "tree": tree,
        "base": base,
        "archive_sha256": sha256_hex(data),
        "archive_bytes": len(data),
        "file_count": archive_file_count(data),
        "flags": list(ARCHIVE_FLAGS),
        "retention_ref": retention_ref,
        "created_by": created_by,
        "created_at": created_at,
    }
    return manifest


def verify_manifest(
    repo_root: typing.Union[str, Path],
    manifest: typing.Mapping[str, object],
) -> typing.List[Issue]:
    """Re-derive the snapshot identity from the commit and compare every term."""

    issues: typing.List[Issue] = payload_issues("snapshot", manifest)
    if issues:
        return issues
    commit = str(manifest.get("commit"))
    try:
        resolved = resolve_commit(repo_root, commit)
        tree = tree_of(repo_root, resolved)
        data = archive(repo_root, resolved)
        count = archive_file_count(data)
    except SnapshotError as error:
        return [Issue(CODE_REQUIRED_INPUT, str(error))]
    if resolved != commit:
        issues.append(Issue(CODE_CANONICAL, "snapshot commit does not resolve to itself"))
    if manifest.get("tree") != tree:
        issues.append(Issue(CODE_TAMPER, "snapshot tree does not resolve to the recorded tree"))
    if manifest.get("archive_sha256") != sha256_hex(data):
        issues.append(Issue(CODE_TAMPER, "snapshot archive sha256 does not reproduce from the commit"))
    if manifest.get("archive_bytes") != len(data):
        issues.append(Issue(CODE_TAMPER, "snapshot archive bytes do not reproduce from the commit"))
    if manifest.get("file_count") != count:
        issues.append(Issue(CODE_TAMPER, "snapshot file count does not reproduce from the archive"))
    return issues


def binding_issues(
    manifest: typing.Mapping[str, object],
    freeze: typing.Mapping[str, object],
) -> typing.List[Issue]:
    """A snapshot must resolve to the frozen commit/tree/base, not to a sibling."""

    issues: typing.List[Issue] = []
    for manifest_key, freeze_key in (("commit", "head_sha"), ("tree", "tree_sha"), ("base", "base_sha")):
        if manifest.get(manifest_key) != freeze.get(freeze_key):
            issues.append(
                Issue(
                    CODE_HEAD_MOVED,
                    "snapshot %s %r does not equal the frozen %s %r"
                    % (manifest_key, manifest.get(manifest_key), freeze_key, freeze.get(freeze_key)),
                )
            )
    if manifest.get("change_id") != freeze.get("change_id"):
        issues.append(Issue(CODE_HEAD_MOVED, "snapshot change_id does not equal the frozen change"))
    return issues


def retention_issues(manifest: typing.Mapping[str, object]) -> typing.List[Issue]:
    """The retention destination is an owner input; an unnamed one is not a pass."""

    issues: typing.List[Issue] = []
    retention = manifest.get("retention_ref")
    if not isinstance(retention, str) or not retention or retention in ("UNNAMED", "UNSET"):
        issues.append(
            Issue(
                CODE_REQUIRED_INPUT,
                "snapshot retention_ref is unnamed; owner input A8 names the evidence location before any "
                "real snapshot is captured",
            )
        )
    return issues
