"""Append-only change-state records: JSONL hash chain, manifest and git prefix.

The discipline is the merged C1.1a revision-state store's
(docs/approvals/revision-state/README.md), applied to a *separate* change-state
area - one store per concern, no second ledger for the same concern:

  * JSONL, one event per line, canonical (JCS) bytes, LF, append-only;
  * every line carries prev_event_sha256 = SHA-256 of the exact previous line
    bytes (null for the first event) and seq is contiguous from 1;
  * the current file must be an append-only prefix of its git base version;
    an edit, a removal, a decrease or a rename/restart reset is
    STATE_TAMPER_SUSPECTED, never accepted as drift;
  * manifest.json carries a deterministic store_digest and a provenance
    binding that defaults to UNKNOWN/UNVERIFIED (T24).  No generated_at and
    no other volatile field is written.

Writers take an explicit caller-supplied path and never write into the
repository by themselves.  No network, standard library only.
"""

from __future__ import annotations

import json
import subprocess
import typing
from pathlib import Path

from . import ASSURANCE, PROVENANCE_BINDING_STATUS, SCHEMA_VERSION
from .schema import (
    ASSURANCE_CLAIMS,
    CODE_CANONICAL,
    CODE_REQUIRED_INPUT,
    CODE_TAMPER,
    COVERAGE_STATES,
    Issue,
    canonical_bytes,
    digest,
    dumps,
    payload_issues,
    sha256_hex,
)

LEDGER_KINDS = ("INITIAL", "BATCHED_BLOCKING_FIX", "FINAL_BLOCKING_FIX", "EXCEPTION", "RESYNC")
UNVERIFIED_REASON = (
    "no owner-authorised change-state authority record yet (AUTH-STORE / owner decision T24 unresolved)"
)


def read_jsonl(path: typing.Union[str, Path]) -> typing.Tuple[typing.List[typing.Dict[str, object]], typing.List[bytes], typing.List[Issue]]:
    """Read one SQL-free JSONL ledger into events, raw line bytes and issues."""

    file_path = Path(path)
    issues: typing.List[Issue] = []
    try:
        raw = file_path.read_bytes()
    except OSError as error:
        return ([], [], [Issue(CODE_REQUIRED_INPUT, "ledger is absent: %s (%s)" % (file_path, error))])
    if raw and not raw.endswith(b"\n"):
        issues.append(Issue(CODE_CANONICAL, "ledger does not end with a newline: %s" % file_path))
    lines = [line for line in raw.split(b"\n")]
    if lines and lines[-1] == b"":
        lines = lines[:-1]
    events: typing.List[typing.Dict[str, object]] = []
    for index, line in enumerate(lines):
        try:
            document = json.loads(line.decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            issues.append(Issue(CODE_CANONICAL, "ledger line %d is not UTF-8 JSON" % (index + 1)))
            continue
        if not isinstance(document, dict):
            issues.append(Issue(CODE_CANONICAL, "ledger line %d is not an object" % (index + 1)))
            continue
        if line != dumps(document).encode("utf-8"):
            issues.append(
                Issue(CODE_TAMPER, "ledger line %d is not canonical (rewritten outside the producer)" % (index + 1))
            )
        events.append(typing.cast(typing.Dict[str, object], document))
    return (events, lines, issues)


def event_bytes(event: typing.Mapping[str, object]) -> bytes:
    """The exact bytes one event occupies (without the terminating LF)."""

    return dumps(event).encode("utf-8")


def validate_chain(
    events: typing.Sequence[typing.Mapping[str, object]],
    lines: typing.Sequence[bytes],
) -> typing.List[Issue]:
    """Re-derive seq/prev-event chain over the exact line bytes."""

    issues: typing.List[Issue] = []
    seqs = [event.get("seq") for event in events]
    if seqs != list(range(1, len(seqs) + 1)):
        issues.append(Issue(CODE_TAMPER, "ledger seq values are not contiguous from 1"))
    for index, event in enumerate(events):
        expected_prev = None if index == 0 else sha256_hex(lines[index - 1])
        if event.get("prev_event_sha256") != expected_prev:
            issues.append(
                Issue(CODE_TAMPER, "ledger line %d does not chain to the previous line" % (index + 1))
            )
        issues.extend(payload_issues("ledger_event", event))
    return issues


def write_ledger(path: typing.Union[str, Path], events: typing.Sequence[typing.Mapping[str, object]]) -> None:
    """Write a complete ledger to a caller-supplied path (deterministic bytes)."""

    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    chunks: typing.List[bytes] = []
    previous: typing.Optional[bytes] = None
    for index, event in enumerate(events):
        document = dict(event)
        document["seq"] = index + 1
        document["prev_event_sha256"] = None if previous is None else sha256_hex(previous)
        previous = event_bytes(document)
        chunks.append(previous + b"\n")
    file_path.write_bytes(b"".join(chunks))


def append_event(path: typing.Union[str, Path], event: typing.Mapping[str, object]) -> typing.Dict[str, object]:
    """Append one event to a caller-supplied ledger, chaining it to the last line."""

    file_path = Path(path)
    events, lines, issues = read_jsonl(file_path)
    if issues:
        raise ValueError("refusing to append to a ledger that does not validate: %s" % issues[0].detail)
    document = dict(event)
    document["seq"] = len(events) + 1
    document["prev_event_sha256"] = None if not lines else sha256_hex(lines[-1])
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("ab") as handle:
        handle.write(event_bytes(document) + b"\n")
    return document


def derived_review_heads(events: typing.Sequence[typing.Mapping[str, object]]) -> int:
    """used = published heads recorded in this change's ledger (candidate excluded)."""

    return sum(1 for event in events if event.get("head_sha"))


# ---------------------------------------------------------------------------
# Manifest and deterministic digest
# ---------------------------------------------------------------------------


def file_entry(
    root: typing.Union[str, Path],
    relative_path: str,
    *,
    kind: str,
    record_id: str,
    event_count: typing.Optional[int] = None,
) -> typing.Dict[str, object]:
    """Describe one stored file by re-hashing it (never by a declared value)."""

    raw = (Path(root) / relative_path).read_bytes()
    entry: typing.Dict[str, object] = {
        "path": relative_path,
        "kind": kind,
        "id": record_id,
        "bytes": len(raw),
        "sha256": sha256_hex(raw),
    }
    if event_count is not None:
        entry["event_count"] = event_count
    return entry


def manifest_digest(manifest: typing.Mapping[str, object]) -> str:
    """The deterministic store_digest projection (no timestamps, no binding)."""

    files = manifest.get("files") if isinstance(manifest.get("files"), list) else []
    projection = []
    for entry in sorted(files, key=lambda item: str(item.get("path"))):
        projection.append(
            {
                "path": entry.get("path"),
                "bytes": entry.get("bytes"),
                "sha256": entry.get("sha256"),
                "event_count": entry.get("event_count"),
                "id": entry.get("id"),
                "kind": entry.get("kind"),
            }
        )
    return digest(
        {
            "schema_version": SCHEMA_VERSION,
            "files": projection,
            "derived_counts_at_binding": manifest.get("derived_counts_at_binding", {}),
        }
    )


def build_manifest(
    change_id: str,
    files: typing.Sequence[typing.Mapping[str, object]],
    derived_counts_at_binding: typing.Mapping[str, object],
    *,
    assurance_claim: str = "AUDITABLE",
    mounted_coverage: str = "UNKNOWN",
) -> typing.Dict[str, object]:
    """Build a closed change-state manifest with an UNVERIFIED provenance binding."""

    manifest: typing.Dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "change_id": change_id,
        "files": [dict(entry) for entry in files],
        "derived_counts_at_binding": dict(derived_counts_at_binding),
        "store_digest": "",
        "assurance_claim": assurance_claim,
        "mounted_coverage": mounted_coverage,
        "provenance_binding": {
            "authority_kind": "UNKNOWN",
            "authority_ref_id": None,
            "authority_ref_sha256": None,
            "holder_role": "change-state-producer",
            "holder_identity_ref": None,
            "binding_status": PROVENANCE_BINDING_STATUS,
            "unverified_reason": UNVERIFIED_REASON,
            "binding_commit_or_pr": None,
        },
    }
    manifest["store_digest"] = manifest_digest(manifest)
    return manifest


def validate_manifest(
    root: typing.Union[str, Path],
    manifest: typing.Mapping[str, object],
) -> typing.List[Issue]:
    """Re-hash every stored file and re-derive the manifest digest."""

    issues: typing.List[Issue] = payload_issues("manifest", manifest)
    if manifest.get("assurance_claim") not in ASSURANCE_CLAIMS:
        issues.append(
            Issue(
                CODE_CANONICAL,
                "assurance claim %r is not NONE/AUDITABLE (no ENFORCED claim is possible in this slice)"
                % (manifest.get("assurance_claim"),),
            )
        )
    if manifest.get("mounted_coverage") not in COVERAGE_STATES:
        issues.append(
            Issue(
                CODE_CANONICAL,
                "mounted coverage %r is claimed without a T5 export; it must stay UNKNOWN"
                % (manifest.get("mounted_coverage"),),
            )
        )
    binding = manifest.get("provenance_binding")
    if isinstance(binding, dict):
        if binding.get("binding_status") == "VERIFIED" and binding.get("authority_kind") == "UNKNOWN":
            issues.append(Issue(CODE_TAMPER, "a VERIFIED binding with authority_kind UNKNOWN is fabricated"))
        if binding.get("authority_kind") == "UNKNOWN" and binding.get("authority_ref_id") is not None:
            issues.append(Issue(CODE_TAMPER, "an authority_ref_id is cited with authority_kind UNKNOWN"))
    files = manifest.get("files")
    if isinstance(files, list):
        for entry in files:
            if not isinstance(entry, dict):
                continue
            relative = entry.get("path")
            if not isinstance(relative, str):
                continue
            path = Path(root) / relative
            if not path.is_file():
                issues.append(Issue(CODE_REQUIRED_INPUT, "manifest file is absent: %s" % relative))
                continue
            raw = path.read_bytes()
            if entry.get("bytes") != len(raw):
                issues.append(Issue(CODE_TAMPER, "manifest bytes do not recompute: %s" % relative))
            if entry.get("sha256") != sha256_hex(raw):
                issues.append(Issue(CODE_TAMPER, "manifest sha256 does not recompute: %s" % relative))
            if relative.endswith(".jsonl") and isinstance(entry.get("event_count"), int):
                events, _lines, _issues = read_jsonl(path)
                if entry.get("event_count") != len(events):
                    issues.append(Issue(CODE_TAMPER, "manifest event_count does not recompute: %s" % relative))
    if manifest.get("store_digest") != manifest_digest(manifest):
        issues.append(Issue(CODE_TAMPER, "manifest store_digest does not recompute"))
    return issues


# ---------------------------------------------------------------------------
# Read-only git plumbing (base resolution and the append-only prefix check)
# ---------------------------------------------------------------------------


def _git(root: typing.Union[str, Path], *args: str) -> typing.Tuple[int, bytes]:
    """Run one read-only git command; never raises on a non-zero exit."""

    completed = subprocess.run(
        ["git", "-C", str(root)] + list(args),
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
        timeout=120,
    )
    return (completed.returncode, completed.stdout)


def resolve_base(root: typing.Union[str, Path], base_ref: str) -> typing.Optional[str]:
    code, out = _git(root, "rev-parse", "--verify", base_ref + "^{commit}")
    if code != 0:
        return None
    value = out.decode("utf-8", "replace").strip()
    return value or None


def _base_bytes(root: typing.Union[str, Path], base: str, relative_path: str) -> typing.Optional[bytes]:
    code, out = _git(root, "cat-file", "-p", "%s:%s" % (base, relative_path))
    if code != 0:
        return None
    return out


def prefix_check(
    root: typing.Union[str, Path],
    relative_paths: typing.Sequence[str],
    base_ref: str = "origin/main",
) -> typing.Dict[str, str]:
    """Check that every stored file is an append-only prefix of its git base.

    A file that does not exist in the base is NEW_FILE (trivially append-only).
    A base that does not resolve is GIT_BASE_UNRESOLVED: the check is never
    skipped and never reported as passed.
    """

    base = resolve_base(root, base_ref)
    report: typing.Dict[str, str] = {}
    if base is None:
        for relative in relative_paths:
            report[str(relative)] = "GIT_BASE_UNRESOLVED"
        report["__status__"] = "GIT_BASE_UNRESOLVED"
        return report
    for relative in relative_paths:
        current_path = Path(root) / str(relative)
        if not current_path.is_file():
            report[str(relative)] = "MISSING"
            continue
        base_bytes = _base_bytes(root, base, str(relative))
        if base_bytes is None:
            report[str(relative)] = "NEW_FILE"
            continue
        current = current_path.read_bytes()
        report[str(relative)] = "PREFIX_OK" if current.startswith(base_bytes) else "PREFIX_VIOLATION"
    report["__status__"] = "CHECKED"
    return report


# ---------------------------------------------------------------------------
# Bundle discovery (documented layout, or the flat fixture layout)
# ---------------------------------------------------------------------------

RECORD_DIRS: typing.Dict[str, str] = {
    "freeze": "freeze",
    "settlement": "settlement",
    "head-history": "head-history",
    "stage-records": "stage-records",
    "snapshots": "snapshots",
    "ledger": "ledger",
}


def discover_bundle(root: typing.Union[str, Path]) -> typing.Dict[str, typing.List[str]]:
    """Find the change-state files of one bundle.

    Documented layout: freeze/<change-id>.json, settlement/<change-id>.json,
    stage-records/<change-id>/{B,D,E}.json, snapshots/<change-id>/<head>.json,
    head-history/<change-id>.json, ledger/<change-id>.jsonl, manifest.json.
    The flat layout (freeze.json, settlement.json, stage-records/*.json, ...)
    is accepted for the synthetic fixtures.
    """

    base = Path(root)
    found: typing.Dict[str, typing.List[str]] = {key: [] for key in RECORD_DIRS}
    found["manifest"] = []
    for key, directory in RECORD_DIRS.items():
        folder = base / directory
        pattern = "*.jsonl" if key == "ledger" else "*.json"
        if folder.is_dir():
            found[key] = [str(path) for path in sorted(folder.rglob(pattern))]
        else:
            found[key] = [str(path) for path in sorted(base.glob(directory + "*.json"))] + [
                str(path) for path in sorted(base.glob(directory + "*.jsonl"))
            ]
    manifest = base / "manifest.json"
    if manifest.is_file():
        found["manifest"] = [str(manifest)]
    return found


def write_json(path: typing.Union[str, Path], document: object) -> None:
    """Write one deterministic JSON document to a caller-supplied path."""

    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(document, indent=2, ensure_ascii=False) + "\n"
    file_path.write_text(text, encoding="utf-8", newline="\n")
