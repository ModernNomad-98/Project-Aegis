"""Immutable Git-object workspace materializer (design §5a; prompt Phase 10).

Materialization always starts from EXACT Git objects (``git archive`` of a
pinned commit), never uncontrolled working-tree bytes. It builds three
separated surfaces:

- a trusted CONTROL-PLANE staging surface (surface A — eval files and other
  control-plane classified content; never agent-visible);
- a SANITIZED agent-visible runtime surface (surface B — profile-scoped);
- a PRODUCT-FIXTURE overlay (the only writable logical area).

Each surface gets its own canonical manifest with per-file SHA-256. The
materializer fails closed on hash/tree mismatch, ambiguous runtime files,
path escapes, reparse points, role mismatch, and any partial surface used
for a full-library claim. No model or agent is launched.

Platform reparse/TOCTOU posture (Finding C — corrected in Round 2). A leaf-only
``O_NOFOLLOW`` protects ONLY the final component; a symlink swapped into a PARENT
component between the check and the open is still followed. That is why the
earlier "real POSIX no-follow guarantee" wording was an overstatement, now
withdrawn. Every write still routes through ``_write_file``, which then splits by
platform capability:

- POSIX with ``dir_fd`` + ``O_DIRECTORY`` + ``O_NOFOLLOW`` (``_POSIX_NOFOLLOW_WRITE``):
  writes route through ``_write_file_dirfd``, which creates and reopens EVERY
  path component under the destination with ``O_NOFOLLOW`` relative to a directory
  descriptor. No symlink planted in any component — parent OR leaf — can be
  traversed, closing the parent-chain TOCTOU window. This path is IMPLEMENTED BUT
  UNRUN in the WP-2B-1 evidence environment (POSIX is not executed here); it is
  reported ``IMPLEMENTED_BUT_UNRUN`` via ``reparse_write_capability()``, never
  proven.
- Windows / hosts without dir-fd no-follow: writes fall back to a leaf-only
  ``O_NOFOLLOW`` (absent on Windows, so ``0``) plus pre/post reparse-chain checks.
  These DETECT a reparse point already present in the chain, but cannot PREVENT a
  reparse point planted mid-operation (the create->open window, or a parent swap).
  An atomic no-reparse write on Windows needs native no-follow handles
  (``CreateFileW``/ctypes), OUT of WP-2B-1's stdlib-only scope. The Windows atomic
  no-reparse write is therefore reported UNAVAILABLE / NON-BASELINE, is NOT claimed
  solved, and remains an OPEN owner decision in the implementation summary.
"""

from __future__ import annotations

import io
import os
import shutil
import subprocess
import tarfile
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from . import SCHEMA_VERSION
from .canonical import canonical_bytes, sha256_hex
from .pathsafe import (
    UnsafePathError,
    normalize_relative_path,
    refuse_reparse_ancestors,
    refuse_reparse_chain,
    safe_join,
)
from .enums import (
    ClaimScope,
    MaterializationProfile,
    RuntimeClassification,
    WorkspaceRole,
)
from .errors import (
    ControlPlaneLeakageError,
    MaterializationError,
    PathEscapeError,
    PartialSurfaceViolationError,
    ReparsePointError,
    RoleMismatchError,
    SnapshotVerificationError,
)
from .runtime_surface import classify_skill_file

SKILLS_PREFIX = ".claude/skills/"
AGENTS_PREFIX = ".claude/agents/"
TEMPLATE_SKILL = "_template"
STARTUP_FILES = ("AGENTS.md", "CLAUDE.md")

#: The four source-library landmarks (AGENTS.md role rules). Consumer-shaped
#: workspaces must exclude ALL of them so role detection resolves to consumer.
SOURCE_LANDMARKS = (
    "README.md",
    "docs/skills-catalog.md",
    "scripts/validate-skills.py",
    "artifacts/audits/skill-contract-audit-baseline.json",
)

_PROFILE_INCLUDES_STARTUP = {
    MaterializationProfile.CONSUMER_SKILLS_ONLY: False,
    MaterializationProfile.CONSUMER_WITH_STARTUP_ROUTING: True,
    MaterializationProfile.CONSUMER_WITH_SUBAGENTS: True,
    MaterializationProfile.SOURCE_LIBRARY: True,
    MaterializationProfile.CONSUMER_PARTIAL_INSTALL: False,
}

_PROFILE_INCLUDES_SUBAGENTS = {
    MaterializationProfile.CONSUMER_SKILLS_ONLY: False,
    MaterializationProfile.CONSUMER_WITH_STARTUP_ROUTING: False,
    MaterializationProfile.CONSUMER_WITH_SUBAGENTS: True,
    MaterializationProfile.SOURCE_LIBRARY: True,
    MaterializationProfile.CONSUMER_PARTIAL_INSTALL: False,
}


_HEX40 = frozenset("0123456789abcdef")
_HEX64 = frozenset("0123456789abcdef")

#: True only on POSIX hosts whose stdlib can do descriptor-relative no-follow
#: traversal (openat-style). When True, ``_write_file`` PREVENTS parent-chain
#: reparse traversal; when False (Windows, and POSIX without dir_fd/O_NOFOLLOW)
#: it can only DETECT a pre-existing reparse and is NON-BASELINE for the
#: mid-operation swap (Finding C).
_POSIX_NOFOLLOW_WRITE = (
    os.name == "posix"
    and hasattr(os, "O_DIRECTORY")
    and hasattr(os, "O_NOFOLLOW")
    and os.open in getattr(os, "supports_dir_fd", frozenset())
    and os.mkdir in getattr(os, "supports_dir_fd", frozenset())
)


def reparse_write_capability() -> Mapping[str, str]:
    """Honest capability report for the reparse-safe materialization write path.

    POSIX with dir-fd no-follow → parent-chain TOCTOU is PREVENTED but the path is
    UNRUN in this Windows evidence environment. Otherwise the mid-operation parent
    swap is UNAVAILABLE to prevent in stdlib and reported NON-BASELINE (Finding C).
    """
    if _POSIX_NOFOLLOW_WRITE:
        return MappingProxyType(
            {
                "platform": "posix",
                "mechanism": "descriptor-relative no-follow traversal "
                "(O_NOFOLLOW per component via dir_fd)",
                "parent_component_toctou": "PREVENTED",
                "baseline_status": "IMPLEMENTED_BUT_UNRUN",
            }
        )
    return MappingProxyType(
        {
            "platform": os.name,
            "mechanism": "leaf O_NOFOLLOW where available + pre/post reparse-chain "
            "checks (detection, not prevention)",
            "parent_component_toctou": "UNAVAILABLE",
            "baseline_status": "NON_BASELINE",
        }
    )


def is_full_sha(value: str) -> bool:
    """True only for a 40-char lowercase hex SHA (not merely 40 chars)."""
    return (
        isinstance(value, str)
        and len(value) == 40
        and all(c in _HEX40 for c in value)
    )


def _resolve_git() -> str:
    """Resolve the git binary via PATH to avoid CWD binary planting on Windows."""
    resolved = shutil.which("git")
    if resolved is None:
        raise SnapshotVerificationError("git executable not found on PATH")
    return resolved


def _git_env() -> dict[str, str]:
    """Minimal git environment: no system config, no prompts, no remote helpers.

    Starts from the current environment (git needs SystemRoot/HOME on some
    platforms) but strips every GIT_* variable that could redirect behavior,
    then re-adds only the safe pins.
    """
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    return env


def _run_git(repo_path: str, args: list[str]) -> bytes:
    """Run a read-only git command with shell=False; fail closed on error.

    Every invocation disables remote protocols and system/global config, and
    callers pass only validated SHAs (never operator-supplied option-shaped
    strings), so no ``git archive --remote=`` / ``--output=`` injection is
    reachable.
    """
    command = [
        _resolve_git(),
        "-c",
        "protocol.allow=never",
        "-C",
        repo_path,
        *args,
    ]
    try:
        completed = subprocess.run(  # noqa: S603 - resolved path, fixed argv, shell=False
            command,
            shell=False,
            capture_output=True,
            timeout=300,
            env=_git_env(),
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise SnapshotVerificationError(f"git invocation failed: {exc}") from exc
    if completed.returncode != 0:
        raise SnapshotVerificationError(
            f"git {' '.join(args[:2])} failed with exit {completed.returncode}: "
            f"{completed.stderr.decode('utf-8', 'replace').strip()[:400]}"
        )
    return completed.stdout


class SnapshotSource:
    """Abstract immutable snapshot: mapping of repo-relative path -> bytes."""

    source_commit: str
    source_tree: str

    def files(self) -> dict[str, bytes]:  # pragma: no cover - interface
        raise NotImplementedError


class GitSnapshot(SnapshotSource):
    """Snapshot exported from exact Git objects at a pinned commit."""

    def __init__(self, repo_path: str, source_commit: str, expected_tree: str) -> None:
        if not is_full_sha(source_commit):
            raise SnapshotVerificationError(
                f"source commit must be a full 40-char lowercase hex SHA: "
                f"{source_commit!r}"
            )
        if not is_full_sha(expected_tree):
            raise SnapshotVerificationError(
                f"expected tree must be a full 40-char lowercase hex SHA: "
                f"{expected_tree!r}"
            )
        actual_tree = (
            _run_git(
                repo_path,
                ["rev-parse", "--verify", "--end-of-options", f"{source_commit}^{{tree}}"],
            )
            .decode("ascii")
            .strip()
        )
        if actual_tree != expected_tree:
            raise SnapshotVerificationError(
                f"tree mismatch for {source_commit}: expected {expected_tree}, "
                f"got {actual_tree}"
            )
        self.repo_path = repo_path
        self.source_commit = source_commit
        self.source_tree = actual_tree
        self._files: dict[str, bytes] | None = None

    def files(self) -> dict[str, bytes]:
        if self._files is None:
            tar_bytes = _run_git(
                self.repo_path,
                ["archive", "--format=tar", "--end-of-options", self.source_commit],
            )
            extracted: dict[str, bytes] = {}
            with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:") as archive:
                for member in archive.getmembers():
                    if member.issym() or member.islnk():
                        raise ReparsePointError(
                            f"snapshot contains a link entry: {member.name!r}"
                        )
                    if not member.isfile():
                        continue
                    handle = archive.extractfile(member)
                    if handle is None:  # pragma: no cover - tarfile guarantees
                        continue
                    extracted[member.name] = handle.read()
            self._files = extracted
        return MappingProxyType(self._files)


class SyntheticSnapshot(SnapshotSource):
    """In-memory snapshot for deterministic offline tests (clearly synthetic)."""

    def __init__(
        self,
        files: Mapping[str, bytes],
        source_commit: str = "0" * 40,
        source_tree: str = "1" * 40,
    ) -> None:
        self._files = {path: bytes(content) for path, content in files.items()}
        self.source_commit = source_commit
        self.source_tree = source_tree

    def files(self) -> Mapping[str, bytes]:
        return MappingProxyType(self._files)


@dataclass(frozen=True, slots=True)
class FixtureDefinition:
    """Product-fixture overlay: the only writable logical area."""

    fixture_id: str = "empty-consumer"
    fixture_version: str = "1"
    files: Mapping[str, bytes] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.fixture_id:
            raise MaterializationError("fixture_id required")
        for path in self.files:
            _validate_relative_path(path)


@dataclass(frozen=True, slots=True)
class MaterializationRequest:
    snapshot: SnapshotSource
    profile: MaterializationProfile
    workspace_role: WorkspaceRole
    claim_scope: ClaimScope
    destination_root: str
    fixture: FixtureDefinition = field(default_factory=FixtureDefinition)
    partial_skill_subset: tuple[str, ...] = ()
    required_subagents: tuple[str, ...] = ()


def _validate_relative_path(path: str) -> str:
    try:
        return normalize_relative_path(path)
    except UnsafePathError as exc:
        raise PathEscapeError(str(exc)) from exc


def _refuse_reparse_points(root: str) -> None:
    """Refuse a destination whose ANCESTOR components include reparse points."""
    try:
        refuse_reparse_ancestors(root)
    except UnsafePathError as exc:
        raise ReparsePointError(str(exc)) from exc


def _safe_join(root: str, relative_path: str) -> str:
    try:
        return safe_join(root, relative_path)
    except UnsafePathError as exc:
        raise PathEscapeError(str(exc)) from exc


def _refuse_read_reparse(path: str, boundary_root: str) -> None:
    """Refuse a reparse point immediately before a verification read."""
    try:
        refuse_reparse_chain(path, boundary_root)
    except UnsafePathError as exc:
        raise ReparsePointError(str(exc)) from exc


def _write_file_dirfd(root_real: str, relative_path: str, content: bytes) -> None:
    """POSIX descriptor-relative no-follow write (Finding C).

    Creates and reopens every path component under ``root_real`` with
    ``O_NOFOLLOW`` relative to a directory descriptor, so a symlink planted in
    ANY component — parent or leaf — cannot be traversed. This closes the
    parent-chain TOCTOU window a leaf-only ``O_NOFOLLOW`` leaves open. Only
    invoked when ``_POSIX_NOFOLLOW_WRITE`` is True; UNRUN on Windows.
    """
    parts = [component for component in relative_path.split("/") if component not in ("", ".")]
    if not parts or any(component == ".." for component in parts):
        # Callers pass a pre-validated relative path, but self-guard anyway so
        # this fail-closed primitive never traverses upward.
        raise MaterializationError(f"unsafe relative path {relative_path!r}")
    *directories, leaf = parts
    open_dirs: list[int] = []
    open_dirs.append(os.open(root_real, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW))
    try:
        current = open_dirs[0]
        for component in directories:
            try:
                os.mkdir(component, 0o700, dir_fd=current)
            except FileExistsError:
                pass
            try:
                child = os.open(
                    component,
                    os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                    dir_fd=current,
                )
            except OSError as exc:
                raise ReparsePointError(
                    f"path component {component!r} under {relative_path!r} is not a "
                    f"real directory (no-follow open refused): {exc}"
                ) from exc
            open_dirs.append(child)
            current = child
        try:
            leaf_fd = os.open(
                leaf,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                0o600,
                dir_fd=current,
            )
        except FileExistsError as exc:
            raise MaterializationError(
                f"refusing to overwrite an existing target {relative_path!r}"
            ) from exc
        except OSError as exc:
            raise ReparsePointError(
                f"could not create {relative_path!r} no-follow: {exc}"
            ) from exc
        try:
            handle = os.fdopen(leaf_fd, "wb")
        except OSError:
            os.close(leaf_fd)  # fdopen failed to take ownership; close the raw fd
            raise
        with handle:
            handle.write(content)
    finally:
        for fd in reversed(open_dirs):
            try:
                os.close(fd)
            except OSError:
                pass


def _write_file(root: str, relative_path: str, content: bytes) -> None:
    root_real = os.path.realpath(root)
    target = _safe_join(root, relative_path)
    # Refuse a reparse point already present in the chain BEFORE any create.
    # On all platforms this DETECTS a pre-existing reparse; on POSIX the dir-fd
    # path below additionally PREVENTS mid-operation parent-swap traversal.
    try:
        refuse_reparse_chain(target, root_real)
    except UnsafePathError as exc:
        raise ReparsePointError(str(exc)) from exc

    if _POSIX_NOFOLLOW_WRITE:
        _write_file_dirfd(root_real, _validate_relative_path(relative_path), content)
        return

    # Fallback (Windows, and POSIX without dir_fd/O_NOFOLLOW): leaf-only
    # O_NOFOLLOW (absent on Windows -> 0) plus a pre/post reparse-chain recheck.
    # This DETECTS a reparse in the chain but cannot PREVENT a reparse planted
    # mid-operation (create->open window or a parent swap) — a documented
    # NON-BASELINE residual (Finding C; see reparse_write_capability()).
    parent = os.path.dirname(target)
    os.makedirs(parent, exist_ok=True)
    try:
        refuse_reparse_chain(parent, root_real)
    except UnsafePathError as exc:
        raise ReparsePointError(str(exc)) from exc
    open_flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    binary = getattr(os, "O_BINARY", 0)
    try:
        fd = os.open(target, open_flags | binary, 0o600)
    except FileExistsError as exc:
        raise MaterializationError(
            f"refusing to overwrite an existing target {relative_path!r}"
        ) from exc
    except OSError as exc:
        raise ReparsePointError(
            f"could not open {relative_path!r} no-follow: {exc}"
        ) from exc
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(content)
    finally:
        # Post-write containment recheck: detect a race that redirected the path
        # and fail closed rather than trusting the write silently.
        try:
            refuse_reparse_chain(target, root_real)
        except UnsafePathError as exc:
            raise ReparsePointError(
                f"reparse detected after writing {relative_path!r}: {exc}"
            ) from exc
    if os.path.commonpath([root_real, os.path.realpath(target)]) != root_real:
        raise ReparsePointError(
            f"{relative_path!r} resolved outside the destination after write"
        )


def _manifest(
    kind: str,
    snapshot: SnapshotSource,
    profile: MaterializationProfile,
    entries: dict[str, bytes],
) -> dict[str, Any]:
    files = [
        {"path": path, "bytes": len(content), "sha256": sha256_hex(content)}
        for path, content in sorted(entries.items())
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "manifest_kind": kind,
        "source_commit": snapshot.source_commit,
        "source_tree": snapshot.source_tree,
        "materialization_profile": profile.value,
        "file_count": len(files),
        "files": files,
    }


def discover_shipped_skills(snapshot_files: Mapping[str, bytes]) -> list[str]:
    """Every shipped skill at the snapshot, ``_template`` excluded."""
    names: set[str] = set()
    for path in snapshot_files:
        if path.startswith(SKILLS_PREFIX):
            remainder = path[len(SKILLS_PREFIX) :]
            skill, _, inner = remainder.partition("/")
            if skill and skill != TEMPLATE_SKILL and inner == "SKILL.md":
                names.add(skill)
    return sorted(names)


_PARTIAL_INSTALL_INELIGIBILITY_REASON = (
    "partial_install results are ineligible for baseline, stability, "
    "full-corpus coverage, and promotion accounting (design §5a)"
)


def _ineligibility_reasons(
    partial_install: bool, ambiguous_excluded: "tuple[str, ...] | list[str]"
) -> list[str]:
    """Single source of truth for baseline-ineligibility reasons.

    Both ``materialize()`` and ``verify_materialization_manifests()`` derive the
    reason list from here so a persisted record's reasons can be recomputed and
    compared EXACTLY (Round 2 §4). The partial_install reason is fully bound
    (claim_scope is bound to the manifest profile); the ambiguity reason TEXT is
    a function of the record's own ``ambiguous_excluded`` list, which is itself
    NOT bindable from the three include-only manifests — see the verifier, which
    classifies the ambiguity inventory UNVERIFIED rather than certifying it.
    """
    reasons: list[str] = []
    if partial_install:
        reasons.append(_PARTIAL_INSTALL_INELIGIBILITY_REASON)
    ambiguous = sorted(ambiguous_excluded)
    if ambiguous:
        reasons.append(
            "ambiguous_needs_owner_review files were excluded from the runtime "
            f"surface: {ambiguous[:5]}"
            f"{'...' if len(ambiguous) > 5 else ''}"
        )
    return reasons


@dataclass(frozen=True, slots=True)
class MaterializationRecord:
    """The three-manifest materialization evidence record."""

    source_commit: str
    source_tree: str
    profile: MaterializationProfile
    workspace_role: WorkspaceRole
    claim_scope: ClaimScope
    shipped_skill_count: int
    materialized_skill_count: int
    subagent_count: int
    ambiguous_excluded: tuple[str, ...]
    control_plane_manifest: Mapping[str, Any]
    runtime_surface_manifest: Mapping[str, Any]
    product_fixture_manifest: Mapping[str, Any]
    control_plane_manifest_sha256: str
    runtime_surface_manifest_sha256: str
    product_fixture_manifest_sha256: str
    baseline_eligible: bool
    baseline_ineligibility_reasons: tuple[str, ...]
    manifest_paths: Mapping[str, str] = field(default_factory=dict)
    schema_version: str = SCHEMA_VERSION

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "source_commit": self.source_commit,
            "source_tree": self.source_tree,
            "materialization_profile": self.profile.value,
            "workspace_role": self.workspace_role.value,
            "claim_scope": self.claim_scope.value,
            "shipped_skill_count": self.shipped_skill_count,
            "materialized_skill_count": self.materialized_skill_count,
            "subagent_count": self.subagent_count,
            "ambiguous_excluded": list(self.ambiguous_excluded),
            "control_plane_manifest_sha256": self.control_plane_manifest_sha256,
            "runtime_surface_manifest_sha256": self.runtime_surface_manifest_sha256,
            "product_fixture_manifest_sha256": self.product_fixture_manifest_sha256,
            "baseline_eligible": self.baseline_eligible,
            "baseline_ineligibility_reasons": list(self.baseline_ineligibility_reasons),
            # Finding F: `manifest_paths` holds operator-local ABSOLUTE paths.
            # It is deliberately kept OUT of the schema-governed portable record
            # (materialization.schema.json is additionalProperties:false) so no
            # operator-private path leaks into committed/portable evidence. The
            # paths remain available as an in-memory attribute for the verifier.
        }


_MANIFEST_SPECS = {
    "control_plane_manifest.json": (
        "authored_eval_corpus",
        "control_plane",
        "control_plane_manifest_sha256",
        "control_plane_manifest",
    ),
    "runtime_surface_manifest.json": (
        "sanitized_runtime_surface",
        "runtime_surface",
        "runtime_surface_manifest_sha256",
        "runtime_surface_manifest",
    ),
    "product_fixture_manifest.json": (
        "product_fixture",
        "product_fixture",
        "product_fixture_manifest_sha256",
        "product_fixture_manifest",
    ),
}


def _enumerate_materialized_files(
    area_root: str, destination_real: str
) -> set[str]:
    """Return the exact regular-file set, refusing every reparse component."""
    _refuse_read_reparse(area_root, destination_real)
    if not os.path.isdir(area_root):
        raise MaterializationError(f"missing materialized area {area_root!r}")

    def _walk_failed(error: OSError) -> None:
        # Finding D: an unreadable/undirable subtree must FAIL CLOSED, never be
        # silently skipped — otherwise an extra unlisted subtree could be
        # omitted from the on-disk comparison while verification reports the
        # file set complete.
        raise MaterializationError(
            f"cannot enumerate materialized subtree "
            f"{getattr(error, 'filename', area_root)!r}: {error}"
        )

    found: set[str] = set()
    for current, directories, files in os.walk(
        area_root, topdown=True, onerror=_walk_failed, followlinks=False
    ):
        _refuse_read_reparse(current, destination_real)
        for name in list(directories):
            _refuse_read_reparse(os.path.join(current, name), destination_real)
        for name in files:
            target = os.path.join(current, name)
            _refuse_read_reparse(target, destination_real)
            if not os.path.isfile(target):
                raise MaterializationError(
                    f"non-regular materialized file {target!r}"
                )
            relative = os.path.relpath(target, area_root).replace("\\", "/")
            relative = _validate_relative_path(relative)
            if relative in found:
                raise MaterializationError(
                    f"duplicate on-disk materialized path {relative!r}"
                )
            found.add(relative)
    return found


def verify_materialization_manifests(
    destination_root: str, expected_record: MaterializationRecord
) -> dict[str, Any]:
    """Verify persisted manifests against the expected materialization record.

    Verification is not self-certifying: every manifest body is bound to the
    immutable hash carried by ``expected_record``; identity fields and paths
    must match the record; listed paths must be unique; ``file_count`` must be
    exact; and the listed file set must equal the complete on-disk file set.
    Every manifest and materialized-file read is reparse-checked immediately
    before opening.
    """
    import json

    if not isinstance(expected_record, MaterializationRecord):
        raise MaterializationError("expected MaterializationRecord required")
    _refuse_reparse_points(destination_root)
    destination_real = os.path.realpath(destination_root)
    manifest_dir = _safe_join(destination_real, "materialization_manifests")
    _refuse_read_reparse(manifest_dir, destination_real)
    runtime_root = _safe_join(destination_real, "runtime_surface")
    result: dict[str, Any] = {"manifests": {}, "verified": True}

    for name, (
        expected_kind,
        area,
        hash_attribute,
        manifest_attribute,
    ) in _MANIFEST_SPECS.items():
        path = _safe_join(manifest_dir, name)
        _refuse_read_reparse(path, destination_real)
        if not os.path.isfile(path):
            raise MaterializationError(f"missing persisted manifest {name!r}")
        recorded_path = expected_record.manifest_paths.get(name)
        if recorded_path is None:
            raise MaterializationError(
                f"expected record missing manifest path {name!r}"
            )
        if os.path.normcase(os.path.abspath(recorded_path)) != os.path.normcase(
            os.path.abspath(path)
        ):
            raise MaterializationError(f"manifest path mismatch for {name!r}")
        if os.path.commonpath(
            [os.path.realpath(runtime_root), os.path.realpath(path)]
        ) == os.path.realpath(runtime_root):
            raise ControlPlaneLeakageError(
                f"manifest {name!r} resides in the agent-visible runtime root"
            )

        _refuse_read_reparse(path, destination_real)
        with open(path, "rb") as handle:
            body_bytes = handle.read()
        expected_hash = getattr(expected_record, hash_attribute)
        if sha256_hex(body_bytes) != expected_hash:
            raise MaterializationError(
                f"manifest {name!r} hash does not match MaterializationRecord"
            )
        try:
            manifest = json.loads(body_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise MaterializationError(
                f"invalid persisted manifest {name!r}"
            ) from exc
        if not isinstance(manifest, dict) or canonical_bytes(manifest) != body_bytes:
            raise MaterializationError(f"manifest {name!r} is not canonical")
        expected_manifest = getattr(expected_record, manifest_attribute)
        if manifest != dict(expected_manifest):
            raise MaterializationError(
                f"manifest {name!r} body does not match MaterializationRecord"
            )

        expected_identity = {
            "schema_version": expected_record.schema_version,
            "manifest_kind": expected_kind,
            "source_commit": expected_record.source_commit,
            "source_tree": expected_record.source_tree,
            "materialization_profile": expected_record.profile.value,
        }
        for key, expected_value in expected_identity.items():
            if manifest.get(key) != expected_value:
                raise MaterializationError(
                    f"manifest {name!r} {key} mismatch: expected "
                    f"{expected_value!r}, got {manifest.get(key)!r}"
                )

        entries = manifest.get("files")
        if not isinstance(entries, list):
            raise MaterializationError(f"manifest {name!r} files must be a list")
        file_count = manifest.get("file_count")
        if (
            isinstance(file_count, bool)
            or not isinstance(file_count, int)
            or file_count != len(entries)
        ):
            raise MaterializationError(f"manifest {name!r} file_count mismatch")

        listed: dict[str, tuple[int, str]] = {}
        for entry in entries:
            if not isinstance(entry, dict) or set(entry) != {
                "path",
                "bytes",
                "sha256",
            }:
                raise MaterializationError(
                    f"manifest {name!r} contains a malformed file entry"
                )
            relative = _validate_relative_path(entry["path"])
            if relative in listed:
                raise MaterializationError(
                    f"manifest {name!r} contains duplicate path {relative!r}"
                )
            byte_count = entry["bytes"]
            digest = entry["sha256"]
            if (
                isinstance(byte_count, bool)
                or not isinstance(byte_count, int)
                or byte_count < 0
            ):
                raise MaterializationError(
                    f"manifest {name!r} has invalid byte count for {relative!r}"
                )
            if (
                not isinstance(digest, str)
                or len(digest) != 64
                or any(character not in _HEX64 for character in digest)
            ):
                raise MaterializationError(
                    f"manifest {name!r} has invalid sha256 for {relative!r}"
                )
            listed[relative] = (byte_count, digest)

        area_root = _safe_join(destination_real, area)
        on_disk = _enumerate_materialized_files(area_root, destination_real)
        if on_disk != set(listed):
            raise MaterializationError(
                f"manifest {name!r} file-set mismatch: "
                f"missing={sorted(set(listed) - on_disk)}, "
                f"extra={sorted(on_disk - set(listed))}"
            )
        for relative, (byte_count, digest) in listed.items():
            target = _safe_join(area_root, relative)
            _refuse_read_reparse(target, destination_real)
            with open(target, "rb") as handle:
                content = handle.read()
            if len(content) != byte_count or sha256_hex(content) != digest:
                raise MaterializationError(
                    f"manifest {name!r} file {relative!r} failed byte/hash "
                    "verification"
                )
        result["manifests"][name] = {
            "sha256": expected_hash,
            "files_verified": len(listed),
        }

    # Finding B: recompute the record's DERIVABLE claims from the verified
    # runtime-surface file set and enforce the cross-field invariants, so a
    # caller-supplied record cannot publish a false workspace_role / claim_scope
    # / count / ambiguity / baseline_eligible through a self-consistent bundle.
    runtime_files = [
        entry["path"]
        for entry in expected_record.runtime_surface_manifest.get("files", [])
    ]
    materialized_skills = {
        path[len(SKILLS_PREFIX):].split("/", 1)[0]
        for path in runtime_files
        if path.startswith(SKILLS_PREFIX)
        and path[len(SKILLS_PREFIX):].partition("/")[2] == "SKILL.md"
    }
    subagents = {
        path[len(AGENTS_PREFIX):].removesuffix(".md")
        for path in runtime_files
        if path.startswith(AGENTS_PREFIX) and path.endswith(".md")
    }
    if expected_record.materialized_skill_count != len(materialized_skills):
        raise MaterializationError(
            f"record materialized_skill_count "
            f"{expected_record.materialized_skill_count} != recomputed "
            f"{len(materialized_skills)} from the verified runtime surface"
        )
    if expected_record.subagent_count != len(subagents):
        raise MaterializationError(
            f"record subagent_count {expected_record.subagent_count} != "
            f"recomputed {len(subagents)} from the verified runtime surface"
        )
    # claim_scope <-> profile invariant.
    partial = expected_record.claim_scope is ClaimScope.PARTIAL_INSTALL
    if partial != (
        expected_record.profile is MaterializationProfile.CONSUMER_PARTIAL_INSTALL
    ):
        raise MaterializationError(
            "record claim_scope and materialization profile are inconsistent"
        )
    # workspace_role <-> profile invariant.
    source_role = expected_record.workspace_role is WorkspaceRole.SOURCE_LIBRARY
    if source_role != (
        expected_record.profile is MaterializationProfile.SOURCE_LIBRARY
    ):
        raise MaterializationError(
            "record workspace_role and materialization profile are inconsistent"
        )
    # shipped_skill_count binding. The verifier has NO access to the source
    # library — it reads only the persisted destination — so it can prove INTERNAL
    # consistency against the materialized surface, NOT the true shipped total. A
    # FULL_LIBRARY run materializes every shipped skill's entry point, so shipped
    # MUST EQUAL materialized (the previous >= floor let an inflated 999 through);
    # a partial_install keeps the >= floor. Either way the shipped TOTAL against
    # the real library is not verifiable here and is classified UNVERIFIED below.
    full_library = expected_record.claim_scope is ClaimScope.FULL_LIBRARY
    if full_library:
        if (
            expected_record.shipped_skill_count
            != expected_record.materialized_skill_count
        ):
            raise MaterializationError(
                "full-library record shipped_skill_count must equal the "
                f"materialized skill count; got "
                f"{expected_record.shipped_skill_count} != "
                f"{expected_record.materialized_skill_count}"
            )
    elif (
        expected_record.shipped_skill_count
        < expected_record.materialized_skill_count
    ):
        raise MaterializationError(
            "record shipped_skill_count is below materialized_skill_count"
        )
    # baseline_eligible invariant: ineligible iff partial_install OR any ambiguity.
    derived_baseline_eligible = not (partial or bool(expected_record.ambiguous_excluded))
    if expected_record.baseline_eligible != derived_baseline_eligible:
        raise MaterializationError(
            f"record baseline_eligible {expected_record.baseline_eligible} != "
            f"derived {derived_baseline_eligible} (partial_install or ambiguity "
            "makes a run baseline-ineligible)"
        )
    # baseline_ineligibility_reasons must be a list of strings, structurally
    # consistent with baseline_eligible, and EXACTLY equal to the reasons
    # recomputed from the bound partial flag and the record's ambiguity list.
    recorded_reasons = expected_record.baseline_ineligibility_reasons
    if not all(isinstance(reason, str) for reason in recorded_reasons):
        raise MaterializationError(
            "record baseline_ineligibility_reasons must all be strings"
        )
    if expected_record.baseline_eligible and recorded_reasons:
        raise MaterializationError(
            "a baseline_eligible record must carry no ineligibility reasons"
        )
    if not expected_record.baseline_eligible and not recorded_reasons:
        raise MaterializationError(
            "a baseline-ineligible record must state at least one reason"
        )
    expected_reasons = _ineligibility_reasons(
        partial, expected_record.ambiguous_excluded
    )
    if list(recorded_reasons) != expected_reasons:
        raise MaterializationError(
            "record baseline_ineligibility_reasons do not match the reasons "
            "recomputed from claim_scope and the ambiguity inventory"
        )
    # Honest claim classification. The verifier reads only the persisted
    # destination, never the source library, and the three manifests list
    # INCLUDED files only. So the EXCLUDED ambiguity inventory and the shipped
    # TOTAL against the real library cannot be bound here — they are disclosed
    # UNVERIFIED, never certified. `full_library_shipped_equals_materialized` is
    # the one shipped-related claim actually proven: the enforced `shipped ==
    # materialized` invariant, a necessary consistency check, not completeness.
    # Binding the rest would require a fourth hashed manifest or a manifest-schema
    # change (an OPEN owner decision), out of WP-2B-1 scope.
    unverifiable: list[str] = [
        "ambiguous_excluded_inventory",
        "shipped_skill_count_total",
    ]
    if expected_record.ambiguous_excluded:
        unverifiable.append("ambiguity_derived_ineligibility_reason_text")
    result["record_claims"] = {
        "materialized_skill_count": "verified",
        "subagent_count": "verified",
        "claim_scope_profile_invariant": "verified",
        "workspace_role_profile_invariant": "verified",
        "baseline_eligible_invariant": "verified",
        "baseline_ineligibility_reasons": "verified",
        "full_library_shipped_equals_materialized": (
            "verified" if full_library else "n/a"
        ),
        "shipped_skill_count_total": (
            "unverified: the verifier does not read the source library; equality "
            "to the materialized count is a necessary consistency check, not proof "
            "of completeness"
        ),
        "ambiguous_excluded_inventory": (
            "unverified: excluded files are absent from all three manifests"
        ),
    }
    result["record_claims_unverifiable"] = unverifiable
    # Reaching here means every BINDABLE claim held (any failure raised above).
    result["record_derivable_claims_verified"] = True
    # The overall flag is True only when NOTHING is left unverifiable; while the
    # ambiguity inventory stays unbindable it is False (honest, not an overclaim).
    result["record_claims_verified"] = not unverifiable
    return result


def _check_role_profile(request: MaterializationRequest) -> None:
    if request.profile is MaterializationProfile.SOURCE_LIBRARY:
        if request.workspace_role is not WorkspaceRole.SOURCE_LIBRARY:
            raise RoleMismatchError(
                "source_library profile requires workspace_role source_library"
            )
    else:
        if request.workspace_role is not WorkspaceRole.CONSUMER:
            raise RoleMismatchError(
                f"profile {request.profile.value} requires workspace_role consumer"
            )
    partial_profile = request.profile is MaterializationProfile.CONSUMER_PARTIAL_INSTALL
    partial_claim = request.claim_scope is ClaimScope.PARTIAL_INSTALL
    if partial_profile != partial_claim:
        raise PartialSurfaceViolationError(
            "consumer_partial_install and claim_scope partial_install must be "
            "declared together; a reduced surface is never a full-library claim"
        )
    if request.partial_skill_subset and not partial_profile:
        raise PartialSurfaceViolationError(
            "a skill subset is only permitted under consumer_partial_install "
            "with claim_scope partial_install (design §5a binding rule)"
        )
    if partial_profile and not request.partial_skill_subset:
        raise PartialSurfaceViolationError(
            "consumer_partial_install requires an explicitly declared skill subset"
        )


def materialize(request: MaterializationRequest) -> MaterializationRecord:
    """Materialize the two surfaces + fixture overlay; fail closed on violations."""
    _check_role_profile(request)
    request.fixture.validate()
    _refuse_reparse_points(request.destination_root)
    if os.path.exists(request.destination_root) and os.listdir(
        request.destination_root
    ):
        raise MaterializationError(
            f"destination {request.destination_root!r} is not empty; "
            "materialization requires a fresh destination so the written "
            "surfaces exactly match the returned manifests"
        )

    snapshot_files = request.snapshot.files()
    shipped_skills = discover_shipped_skills(snapshot_files)
    if not shipped_skills:
        raise MaterializationError("snapshot contains no shipped skills")

    if request.profile is MaterializationProfile.CONSUMER_PARTIAL_INSTALL:
        unknown = sorted(set(request.partial_skill_subset) - set(shipped_skills))
        if unknown:
            raise MaterializationError(
                f"partial subset names unknown skills: {unknown}"
            )
        selected_skills = sorted(set(request.partial_skill_subset))
    else:
        selected_skills = shipped_skills

    include_startup = _PROFILE_INCLUDES_STARTUP[request.profile]
    include_subagents = _PROFILE_INCLUDES_SUBAGENTS[request.profile]
    include_landmarks = request.profile is MaterializationProfile.SOURCE_LIBRARY

    control_plane: dict[str, bytes] = {}
    runtime_surface: dict[str, bytes] = {}
    ambiguous_excluded: list[str] = []
    subagent_names: set[str] = set()

    for path, content in sorted(snapshot_files.items()):
        if path.startswith(SKILLS_PREFIX):
            remainder = path[len(SKILLS_PREFIX) :]
            skill, _, inner = remainder.partition("/")
            if not inner:
                continue
            if skill == TEMPLATE_SKILL:
                classified = classify_skill_file(inner)
                if classified.classification is RuntimeClassification.CONTROL_PLANE_ONLY:
                    control_plane[path] = content
                continue
            if skill not in selected_skills:
                classified = classify_skill_file(inner)
                if classified.classification is RuntimeClassification.CONTROL_PLANE_ONLY:
                    control_plane[path] = content
                continue
            classified = classify_skill_file(inner)
            if classified.classification is RuntimeClassification.CONTROL_PLANE_ONLY:
                control_plane[path] = content
            elif classified.classification is RuntimeClassification.RUNTIME_REQUIRED:
                runtime_surface[path] = content
            else:
                ambiguous_excluded.append(path)
            continue
        if path.startswith(AGENTS_PREFIX):
            if include_subagents:
                name = path[len(AGENTS_PREFIX) :]
                if request.required_subagents and (
                    name.removesuffix(".md") not in request.required_subagents
                ):
                    continue
                runtime_surface[path] = content
                subagent_names.add(name.removesuffix(".md"))
            continue
        if path in STARTUP_FILES:
            if include_startup:
                runtime_surface[path] = content
            continue
        if path in SOURCE_LANDMARKS:
            if include_landmarks:
                runtime_surface[path] = content
            continue

    if request.required_subagents:
        if not include_subagents:
            raise MaterializationError(
                f"required subagents {sorted(request.required_subagents)} but "
                f"profile {request.profile.value} carries no subagents"
            )
        missing_subagents = sorted(set(request.required_subagents) - subagent_names)
        if missing_subagents:
            raise MaterializationError(
                f"required subagents absent from the snapshot: {missing_subagents}"
            )

    leaked = sorted(set(runtime_surface) & set(control_plane))
    if leaked:
        raise ControlPlaneLeakageError(f"control-plane files in runtime surface: {leaked}")
    for path in runtime_surface:
        if path.startswith(SKILLS_PREFIX):
            inner = path[len(SKILLS_PREFIX) :].partition("/")[2]
            if (
                classify_skill_file(inner).classification
                is not RuntimeClassification.RUNTIME_REQUIRED
            ):
                raise ControlPlaneLeakageError(
                    f"non-runtime file classified into runtime surface: {path}"
                )

    skills_with_entry_point = {
        path[len(SKILLS_PREFIX) :].split("/", 1)[0]
        for path in runtime_surface
        if path.startswith(SKILLS_PREFIX)
        and path[len(SKILLS_PREFIX) :].partition("/")[2] == "SKILL.md"
    }
    if request.claim_scope is ClaimScope.FULL_LIBRARY:
        missing = sorted(set(shipped_skills) - skills_with_entry_point)
        if missing:
            raise PartialSurfaceViolationError(
                f"full-library claim but skill entry point(s) missing from the "
                f"runtime surface: {missing[:5]}{'...' if len(missing) > 5 else ''}"
            )

    control_root = os.path.join(request.destination_root, "control_plane")
    runtime_root = os.path.join(request.destination_root, "runtime_surface")
    fixture_root = os.path.join(request.destination_root, "product_fixture")
    for area_root, entries in (
        (control_root, control_plane),
        (runtime_root, runtime_surface),
        (fixture_root, dict(request.fixture.files)),
    ):
        os.makedirs(area_root, exist_ok=True)
        for path, content in sorted(entries.items()):
            _write_file(area_root, path, content)

    control_manifest = _manifest(
        "authored_eval_corpus", request.snapshot, request.profile, control_plane
    )
    runtime_manifest = _manifest(
        "sanitized_runtime_surface", request.snapshot, request.profile, runtime_surface
    )
    fixture_manifest = _manifest(
        "product_fixture",
        request.snapshot,
        request.profile,
        dict(request.fixture.files),
    )
    fixture_manifest["fixture_id"] = request.fixture.fixture_id
    fixture_manifest["fixture_version"] = request.fixture.fixture_version

    manifest_files = {
        "control_plane_manifest.json": control_manifest,
        "runtime_surface_manifest.json": runtime_manifest,
        "product_fixture_manifest.json": fixture_manifest,
    }
    manifest_paths: dict[str, str] = {}
    for name, body in manifest_files.items():
        # Finding C: the persisted-manifest writes route through the SAME
        # reparse-checked write path as every surface write — no raw open().
        relative = f"materialization_manifests/{name}"
        _write_file(request.destination_root, relative, canonical_bytes(body))
        manifest_paths[name] = _safe_join(request.destination_root, relative)

    ineligibility = _ineligibility_reasons(
        request.claim_scope is ClaimScope.PARTIAL_INSTALL, ambiguous_excluded
    )

    return MaterializationRecord(
        source_commit=request.snapshot.source_commit,
        source_tree=request.snapshot.source_tree,
        profile=request.profile,
        workspace_role=request.workspace_role,
        claim_scope=request.claim_scope,
        shipped_skill_count=len(shipped_skills),
        materialized_skill_count=len(skills_with_entry_point),
        subagent_count=len(subagent_names),
        ambiguous_excluded=tuple(sorted(ambiguous_excluded)),
        control_plane_manifest=control_manifest,
        runtime_surface_manifest=runtime_manifest,
        product_fixture_manifest=fixture_manifest,
        control_plane_manifest_sha256=sha256_hex(canonical_bytes(control_manifest)),
        runtime_surface_manifest_sha256=sha256_hex(canonical_bytes(runtime_manifest)),
        product_fixture_manifest_sha256=sha256_hex(canonical_bytes(fixture_manifest)),
        baseline_eligible=not ineligibility,
        baseline_ineligibility_reasons=tuple(ineligibility),
        manifest_paths=manifest_paths,
    )
