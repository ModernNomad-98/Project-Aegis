"""Two-stage, non-circular evidence finalization (design §13/§20a-S30; Phase 18).

Stage A (BEFORE any judge could read evidence): finalized input-evidence
artifacts + canonical input manifest with per-artifact SHA-256 + the manifest's
own SHA-256. Judge construction must verify the input manifest first — the
gate exists in WP-2B-1 even though no judge implementation does.

Stage B (after aggregation): the final report + final artifacts + canonical
final manifest + a DETACHED finalization marker. Rules enforced here:

- the final manifest excludes itself and the detached marker;
- the final report does not contain the final-manifest hash;
- the marker contains final-manifest and final-report hashes and no self-hash;
- no artifact directly or indirectly hashes itself;
- atomic replacement writes;
- corrupt, missing, truncated, circular, or mismatched evidence fails closed
  with ERROR / EVIDENCE_INTEGRITY_FAILURE;
- no unfinalized bundle is trusted. SHA-256 is tamper evidence only.
"""

from __future__ import annotations

import datetime as _dt
import os
from dataclasses import dataclass, field
from typing import Any, Mapping

from . import SCHEMA_VERSION
from .canonical import canonical_bytes, sha256_hex
from .enums import RedactionState, RetentionClass, Sensitivity
from .errors import CircularEvidenceError, EvidenceError, EvidenceIntegrityError
from .pathsafe import (
    UnsafePathError,
    normalize_relative_path,
    refuse_reparse_ancestors,
    refuse_reparse_chain,
)

INPUT_MANIFEST_NAME = "input_evidence_manifest.json"
FINAL_MANIFEST_NAME = "final_evidence_manifest.json"
FINAL_REPORT_NAME = "final_report.json"
MARKER_NAME = "finalization_marker.json"

_RETENTION_DAYS = {
    RetentionClass.DAYS_30: 30,
    RetentionClass.DAYS_90: 90,
    RetentionClass.DAYS_365: 365,
}


def _utc_now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _expiration_for(created_at: str, retention: RetentionClass) -> str:
    # D3: require a timezone-aware timestamp; convert to UTC before arithmetic
    # rather than silently assigning an unstated timezone to a naive value.
    try:
        created = _dt.datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise EvidenceError(f"created_at is not ISO-8601: {created_at!r}") from exc
    if created.tzinfo is None:
        raise EvidenceError(
            f"created_at {created_at!r} is timezone-naive; a timezone-aware "
            "timestamp is required"
        )
    created = created.astimezone(_dt.timezone.utc)
    expires = created + _dt.timedelta(days=_RETENTION_DAYS[retention])
    return expires.strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass(frozen=True, slots=True)
class ArtifactMetadata:
    sensitivity: Sensitivity = Sensitivity.INTERNAL
    redaction_state: RedactionState = RedactionState.SANITIZED_BY_CONSTRUCTION
    retention_class: RetentionClass = RetentionClass.DAYS_30
    access_policy_ref: str = "BER-DEC-006-build-evidence-handling"
    preserve_on_failure: bool = True
    created_at: str | None = None  # ISO-8601; defaults to now(UTC)


@dataclass(frozen=True, slots=True)
class EvidenceArtifact:
    relative_path: str
    content: bytes
    metadata: ArtifactMetadata = field(default_factory=ArtifactMetadata)


#: Names an artifact may never claim (manifests, marker, and the final report).
_RESERVED_ARTIFACT_NAMES = frozenset(
    {INPUT_MANIFEST_NAME, FINAL_MANIFEST_NAME, MARKER_NAME, FINAL_REPORT_NAME}
)


def _validate_artifact_path(relative_path: str, allow_final_report: bool = False) -> str:
    try:
        normalized = normalize_relative_path(relative_path)
    except UnsafePathError as exc:
        raise EvidenceError(str(exc)) from exc
    reserved = set(_RESERVED_ARTIFACT_NAMES)
    if allow_final_report:
        reserved.discard(FINAL_REPORT_NAME)
    if os.path.normcase(normalized) in {os.path.normcase(name) for name in reserved}:
        raise EvidenceError(f"artifact path {relative_path!r} is reserved")
    return normalized


def _atomic_write(root: str, relative_path: str, content: bytes) -> str:
    root_real = os.path.realpath(root)
    target = os.path.abspath(os.path.join(root_real, *relative_path.split("/")))
    if os.path.commonpath([root_real, target]) != root_real:
        raise EvidenceError(f"{relative_path!r} escapes evidence root {root!r}")
    parent = os.path.dirname(target) or root_real
    # D1: refuse a reparse point planted anywhere between the root and the
    # target before creating parents.
    try:
        refuse_reparse_chain(parent, root_real)
    except UnsafePathError as exc:
        raise EvidenceError(str(exc)) from exc
    os.makedirs(parent, exist_ok=True)
    import tempfile

    # Re-check after parent creation and immediately before os.replace.
    try:
        refuse_reparse_chain(parent, root_real)
    except UnsafePathError as exc:
        raise EvidenceError(str(exc)) from exc
    fd, temp = tempfile.mkstemp(dir=parent, prefix=".tmp-evidence-")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(content)
        try:
            refuse_reparse_chain(target, root_real)
        except UnsafePathError as exc:
            raise EvidenceError(str(exc)) from exc
        os.replace(temp, target)  # atomic replacement where the platform allows
    except BaseException:
        if os.path.exists(temp):  # pragma: no cover - cleanup guard
            os.remove(temp)
        raise
    return target


def _manifest_entry(artifact: EvidenceArtifact) -> dict[str, Any]:
    created_at = artifact.metadata.created_at or _utc_now_iso()
    return {
        "path": artifact.relative_path,
        "bytes": len(artifact.content),
        "sha256": sha256_hex(artifact.content),
        "sensitivity": artifact.metadata.sensitivity.value,
        "redaction_state": artifact.metadata.redaction_state.value,
        "retention_class": artifact.metadata.retention_class.value,
        "created_at": created_at,
        "expiration_at": _expiration_for(created_at, artifact.metadata.retention_class),
        "access_policy_ref": artifact.metadata.access_policy_ref,
        "preserve_on_failure": artifact.metadata.preserve_on_failure,
    }


def _check_no_self_hash(content: bytes, own_hash: str, label: str) -> None:
    if own_hash.encode("ascii") in content:
        raise CircularEvidenceError(
            f"{label} contains its own SHA-256; no artifact may hash itself"
        )


@dataclass(frozen=True, slots=True)
class InputEvidenceBundle:
    root: str
    manifest_path: str
    input_evidence_manifest_sha256: str
    artifact_count: int


@dataclass(frozen=True, slots=True)
class FinalEvidenceBundle:
    root: str
    final_report_path: str
    final_report_sha256: str
    final_manifest_path: str
    final_evidence_manifest_sha256: str
    marker_path: str
    finalization_marker_sha256: str


class EvidenceWriter:
    """Trusted control-plane evidence writer for one run's bundle root."""

    def __init__(self, root: str, run_id: str) -> None:
        if not run_id:
            raise EvidenceError("run_id required")
        self.root = os.path.abspath(root)
        self.run_id = run_id
        # D1: refuse a reparse point anywhere in the ancestor chain of the root.
        try:
            refuse_reparse_ancestors(self.root)
        except UnsafePathError as exc:
            raise EvidenceError(str(exc)) from exc
        os.makedirs(self.root, exist_ok=True)

    # ------------------------------------------------------------- stage A
    def finalize_input_evidence(
        self, artifacts: list[EvidenceArtifact]
    ) -> InputEvidenceBundle:
        entries: list[dict[str, Any]] = []
        seen: set[str] = set()
        for artifact in artifacts:
            path = _validate_artifact_path(artifact.relative_path)
            if path in seen:
                raise EvidenceError(f"duplicate artifact path {path!r}")
            seen.add(path)
            entry = _manifest_entry(artifact)
            _check_no_self_hash(artifact.content, entry["sha256"], path)
            _atomic_write(self.root, path, artifact.content)
            entries.append(entry)
        manifest = {
            "schema_version": SCHEMA_VERSION,
            "manifest_kind": "input_evidence",
            "run_id": self.run_id,
            "artifacts": sorted(entries, key=lambda e: e["path"]),
        }
        manifest_bytes = canonical_bytes(manifest)
        manifest_path = _atomic_write(self.root, INPUT_MANIFEST_NAME, manifest_bytes)
        return InputEvidenceBundle(
            root=self.root,
            manifest_path=manifest_path,
            input_evidence_manifest_sha256=sha256_hex(manifest_bytes),
            artifact_count=len(entries),
        )

    # ------------------------------------------------------------- stage B
    def finalize_final_bundle(
        self,
        final_report: Mapping[str, Any],
        artifacts: list[EvidenceArtifact],
        input_manifest_sha256: str,
        final_status: str,
        finalized_at: str | None = None,
    ) -> FinalEvidenceBundle:
        # D2: the report must belong to THIS run — a report for another run is
        # rejected at finalization.
        if final_report.get("run_id") != self.run_id:
            raise EvidenceError(
                f"final report run_id {final_report.get('run_id')!r} does not "
                f"match the writer's run_id {self.run_id!r}"
            )
        binding = final_report.get("run_evidence_binding")
        if (
            not isinstance(binding, Mapping)
            or binding.get("input_evidence_manifest_sha256") != input_manifest_sha256
        ):
            raise EvidenceError(
                "the final report must carry run_evidence_binding."
                "input_evidence_manifest_sha256 (stage A binding)"
            )
        for forbidden in ("final_evidence_manifest_sha256", "final_report_sha256"):
            if forbidden in binding:
                raise CircularEvidenceError(
                    f"the final report must not carry {forbidden}; those hashes "
                    "live only in the detached marker"
                )
        report_bytes = canonical_bytes(dict(final_report))
        report_sha = sha256_hex(report_bytes)
        report_path = _atomic_write(self.root, FINAL_REPORT_NAME, report_bytes)

        entries: list[dict[str, Any]] = []
        seen: set[str] = set()
        for artifact in artifacts:
            path = _validate_artifact_path(artifact.relative_path)
            if path in seen or path == FINAL_REPORT_NAME:
                raise EvidenceError(f"duplicate artifact path {path!r}")
            seen.add(path)
            entry = _manifest_entry(artifact)
            _check_no_self_hash(artifact.content, entry["sha256"], path)
            _atomic_write(self.root, path, artifact.content)
            entries.append(entry)
        report_created_at = finalized_at or _utc_now_iso()
        report_entry = {
            "path": FINAL_REPORT_NAME,
            "bytes": len(report_bytes),
            "sha256": report_sha,
            "sensitivity": Sensitivity.INTERNAL.value,
            "redaction_state": RedactionState.SANITIZED_BY_CONSTRUCTION.value,
            "retention_class": RetentionClass.DAYS_30.value,
            "created_at": report_created_at,
            "expiration_at": _expiration_for(report_created_at, RetentionClass.DAYS_30),
            "access_policy_ref": "BER-DEC-006-build-evidence-handling",
            "preserve_on_failure": True,
        }
        entries.append(report_entry)

        # The final manifest lists every final artifact INCLUDING the final
        # report, EXCLUDING itself and the detached marker.
        manifest = {
            "schema_version": SCHEMA_VERSION,
            "manifest_kind": "final_evidence",
            "run_id": self.run_id,
            "artifacts": sorted(entries, key=lambda e: e["path"]),
        }
        manifest_bytes = canonical_bytes(manifest)
        manifest_sha = sha256_hex(manifest_bytes)
        if manifest_sha.encode("ascii") in report_bytes:
            raise CircularEvidenceError(
                "the final report contains the final-manifest hash; "
                "a self-referential hash cannot verify"
            )
        manifest_path = _atomic_write(self.root, FINAL_MANIFEST_NAME, manifest_bytes)

        marker = {
            "schema_version": SCHEMA_VERSION,
            "marker_kind": "detached_finalization_marker",
            "run_id": self.run_id,
            "final_evidence_manifest_sha256": manifest_sha,
            "final_report_sha256": report_sha,
            "final_status": final_status,
            "finalized_at": report_created_at,
            "note": (
                "detached per the non-circular protocol: not listed in the "
                "manifest it names; contains no hash of itself; its own "
                "SHA-256 is recorded by the consuming index/rollup"
            ),
        }
        marker_bytes = canonical_bytes(marker)
        marker_path = _atomic_write(self.root, MARKER_NAME, marker_bytes)
        return FinalEvidenceBundle(
            root=self.root,
            final_report_path=report_path,
            final_report_sha256=report_sha,
            final_manifest_path=manifest_path,
            final_evidence_manifest_sha256=manifest_sha,
            marker_path=marker_path,
            finalization_marker_sha256=sha256_hex(marker_bytes),
        )


def _load_json_bytes(root: str, name: str) -> tuple[dict[str, Any], bytes]:
    import json

    path = os.path.join(root, *name.split("/"))
    if not os.path.exists(path):
        raise EvidenceIntegrityError(f"missing evidence artifact: {name}")
    with open(path, "rb") as handle:
        content = handle.read()
    try:
        parsed = json.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise EvidenceIntegrityError(f"corrupt evidence artifact {name}: {exc}") from exc
    if not isinstance(parsed, dict):
        raise EvidenceIntegrityError(f"evidence artifact {name} is not an object")
    return parsed, content


def _verify_manifest_artifacts(
    root: str, manifest: Mapping[str, Any], allow_final_report: bool = False
) -> dict[str, str]:
    """Verify every listed artifact; return the trusted {path: sha256} map."""
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        raise EvidenceIntegrityError("manifest has no artifact list")
    root_real = os.path.realpath(root)
    verified: dict[str, str] = {}
    for entry in artifacts:
        raw_path = entry.get("path", "")
        # Manifest paths are UNTRUSTED input: validate exactly as write paths
        # are, so a rewritten manifest cannot escape the bundle root or name a
        # manifest/marker artifact.
        try:
            path = _validate_artifact_path(raw_path, allow_final_report=allow_final_report)
        except EvidenceError as exc:
            raise EvidenceIntegrityError(
                f"manifest lists an unsafe artifact path {raw_path!r}: {exc}"
            ) from exc
        if path in verified:
            raise EvidenceIntegrityError(f"manifest lists {path!r} twice")
        target = os.path.realpath(os.path.join(root_real, *path.split("/")))
        if os.path.commonpath([root_real, target]) != root_real:
            raise EvidenceIntegrityError(
                f"manifest artifact {raw_path!r} resolves outside the bundle root"
            )
        if not os.path.exists(target):
            raise EvidenceIntegrityError(f"missing artifact {path!r}")
        with open(target, "rb") as handle:
            content = handle.read()
        if len(content) != entry.get("bytes"):
            raise EvidenceIntegrityError(
                f"truncated or padded artifact {path!r}: {len(content)} bytes, "
                f"manifest says {entry.get('bytes')}"
            )
        actual_sha = sha256_hex(content)
        if actual_sha != entry.get("sha256"):
            raise EvidenceIntegrityError(
                f"hash mismatch for {path!r}: manifest {entry.get('sha256')}, "
                f"actual {actual_sha}"
            )
        _check_no_self_hash(content, actual_sha, path)
        for meta_key in (
            "sensitivity",
            "redaction_state",
            "retention_class",
            "created_at",
            "expiration_at",
            "access_policy_ref",
        ):
            if meta_key not in entry:
                raise EvidenceIntegrityError(
                    f"artifact {path!r} missing metadata {meta_key!r}"
                )
        verified[path] = actual_sha
    return verified


def verify_input_evidence(root: str) -> str:
    """Verify stage A; returns the input manifest SHA-256. Fails closed."""
    return _verify_input_evidence_full(root)[0]


def _verify_input_evidence_full(root: str) -> tuple[str, dict[str, str]]:
    manifest, manifest_bytes = _load_json_bytes(root, INPUT_MANIFEST_NAME)
    if manifest.get("manifest_kind") != "input_evidence":
        raise EvidenceIntegrityError("wrong manifest kind for input evidence")
    verified = _verify_manifest_artifacts(root, manifest)
    return sha256_hex(manifest_bytes), verified


def verify_final_bundle(root: str) -> dict[str, str]:
    """Verify stage B, its detached-marker binding, AND its binding to the
    already-verified stage-A input manifest. Fails closed. D2: every artifact
    must carry the SAME non-empty run_id — a cross-run mixture is rejected even
    when all hashes are individually valid."""
    input_manifest, _ = _load_json_bytes(root, INPUT_MANIFEST_NAME)
    input_manifest_sha, _verified = _verify_input_evidence_full(root)
    run_id = input_manifest.get("run_id")
    if not run_id:
        raise EvidenceIntegrityError("input manifest has no run_id")

    manifest, manifest_bytes = _load_json_bytes(root, FINAL_MANIFEST_NAME)
    if manifest.get("manifest_kind") != "final_evidence":
        raise EvidenceIntegrityError("wrong manifest kind for final evidence")
    if manifest.get("run_id") != run_id:
        raise EvidenceIntegrityError("final manifest run_id differs (cross-run)")
    _verify_manifest_artifacts(root, manifest, allow_final_report=True)
    manifest_sha = sha256_hex(manifest_bytes)

    marker, marker_bytes = _load_json_bytes(root, MARKER_NAME)
    if marker.get("marker_kind") != "detached_finalization_marker":
        raise EvidenceIntegrityError("missing detached finalization marker")
    if marker.get("run_id") != run_id:
        raise EvidenceIntegrityError("marker run_id differs (cross-run)")
    if marker.get("final_evidence_manifest_sha256") != manifest_sha:
        raise EvidenceIntegrityError(
            "marker does not bind the final manifest (hash mismatch)"
        )
    marker_sha = sha256_hex(marker_bytes)
    _check_no_self_hash(marker_bytes, marker_sha, MARKER_NAME)

    report, report_bytes = _load_json_bytes(root, FINAL_REPORT_NAME)
    report_sha = sha256_hex(report_bytes)
    if marker.get("final_report_sha256") != report_sha:
        raise EvidenceIntegrityError(
            "marker does not bind the final report (hash mismatch)"
        )
    if manifest_sha.encode("ascii") in report_bytes:
        raise CircularEvidenceError(
            "final report contains the final-manifest hash (circular)"
        )
    if report.get("run_id") != run_id:
        raise EvidenceIntegrityError("final report run_id differs (cross-run)")
    binding = report.get("run_evidence_binding", {})
    bound_input_sha = binding.get("input_evidence_manifest_sha256")
    if not bound_input_sha:
        raise EvidenceIntegrityError(
            "final report lacks the stage-A input-evidence binding"
        )
    # The report's recorded stage-A hash MUST equal the freshly verified
    # stage-A manifest hash — a whole-cloth stage-A swap is caught here.
    if bound_input_sha != input_manifest_sha:
        raise EvidenceIntegrityError(
            "final report's input_evidence_manifest_sha256 does not match the "
            "verified stage-A input manifest (stage-A substitution)"
        )
    return {
        "input_evidence_manifest_sha256": input_manifest_sha,
        "final_evidence_manifest_sha256": manifest_sha,
        "final_report_sha256": report_sha,
        "finalization_marker_sha256": marker_sha,
    }


class JudgeInputGate:
    """The verification boundary a future judge constructor must pass.

    WP-2B-1 ships no judge; the gate still enforces that NOTHING reads
    stage-A evidence without verification (fail closed).
    """

    def __init__(self, root: str) -> None:
        self.root = os.path.realpath(root)
        self._verified_manifest_sha: str | None = None
        self._verified: dict[str, str] = {}

    def verify(self) -> str:
        manifest_sha, verified = _verify_input_evidence_full(self.root)
        self._verified_manifest_sha = manifest_sha
        self._verified = verified
        return manifest_sha

    @property
    def verified(self) -> bool:
        return self._verified_manifest_sha is not None

    def read_artifact(self, relative_path: str) -> bytes:
        if not self.verified:
            raise EvidenceIntegrityError(
                "input evidence must be verified before any read "
                "(judge constructors may consume only manifest-verified artifacts)"
            )
        path = _validate_artifact_path(relative_path)
        expected_sha = self._verified.get(path)
        if expected_sha is None:
            raise EvidenceIntegrityError(
                f"artifact {relative_path!r} is not in the verified input "
                "manifest; only manifest-listed artifacts may be read"
            )
        target = os.path.realpath(os.path.join(self.root, *path.split("/")))
        if os.path.commonpath([self.root, target]) != self.root:
            raise EvidenceIntegrityError(
                f"artifact {relative_path!r} resolves outside the bundle root"
            )
        if not os.path.exists(target):
            raise EvidenceIntegrityError(f"missing artifact {relative_path!r}")
        with open(target, "rb") as handle:
            content = handle.read()
        # Re-hash on read: a post-verify rewrite is caught before the bytes
        # reach any consumer.
        actual_sha = sha256_hex(content)
        if actual_sha != expected_sha:
            raise EvidenceIntegrityError(
                f"artifact {relative_path!r} changed since verification "
                "(hash mismatch on read)"
            )
        return content
