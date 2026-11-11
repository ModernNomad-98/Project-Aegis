"""Synthetic fixture helpers for the C1.2-C1.4 change-state tests.

Every helper builds throw-away data in a temporary directory: no real PR,
identity, secret, approval, snapshot or host state is read or written.  The
only repository path these helpers touch is the package's own fixtures
directory (read-only).

The fixture JSON files are authored, complete records with mechanically
correct hashes.  Stage declarations additionally carry the record body they
point at (the "record" key); build_bundle materialises it, exactly as the
documented layout stores a real B/D/E record under stage-records/<change>/.
"""

from __future__ import annotations

import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.aegis_change_state import checks, records, schema, snapshot  # noqa: E402
from tools.aegis_change_state import __main__ as cli  # noqa: E402

FIXTURE_DIR = pathlib.Path(__file__).resolve().parent / "fixtures"
CHANGE_ID = "c1-2-c14-fixture-0001"
CANDIDATE_ID = "cand-c12c14-fixture-0001"
HEAD = "9f2c4d7e1a3b5c6d8e0f1a2b3c4d5e6f7a8b9c0d"
TREE = "4b8e2f6a9c0d1e3f5a7b9c2d4e6f8a0b1c3d5e7f"
BASE = "7c1d3e5f9a2b4c6d8e0f1a3b5c7d9e2f4a6b8c0d"
NEW_HEAD = "5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b"
SNAPSHOT_ID = "snapshot:" + HEAD
FIXTURE_NAMES = sorted(path.name for path in FIXTURE_DIR.glob("*.json"))

GIT_ENV = {
    "GIT_AUTHOR_NAME": "Fixture Builder",
    "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
    "GIT_COMMITTER_NAME": "Fixture Builder",
    "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
    "GIT_AUTHOR_DATE": "2026-11-11T12:00:00+0000",
    "GIT_COMMITTER_DATE": "2026-11-11T12:00:00+0000",
}


def load(name: str) -> dict:
    with (FIXTURE_DIR / name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def payload(name: str) -> dict:
    return load(name)["payload"]


def envelope(payload_document: dict, *, source: str = "fixture", role: str = "fixture", status=None) -> dict:
    return schema.build_envelope(
        payload_document,
        source_ref=source,
        as_of="2026-11-11T05:00:00Z",
        producer_role=role,
        producer_identity_ref=role,
        status=status,
    )


def temporary_directory(prefix: str = "aegis-change-state-test-") -> pathlib.Path:
    return pathlib.Path(tempfile.mkdtemp(prefix=prefix))


def build_bundle(directory) -> pathlib.Path:
    cli.build_bundle(directory, FIXTURE_DIR)
    return pathlib.Path(directory)


def copy_bundle(source) -> pathlib.Path:
    destination = temporary_directory("aegis-change-state-copy-")
    shutil.copytree(str(source), str(destination / "bundle"))
    return destination / "bundle"


def write_json(path, document) -> None:
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def replace_stage(bundle, stage: str, fixture_name: str) -> None:
    """Replace one stage declaration with a fixture's envelope (record key stripped)."""

    document = load(fixture_name)
    declaration = {"payload": document["payload"], "provenance": document["provenance"]}
    write_json(pathlib.Path(bundle) / "stage-records" / (stage + ".json"), declaration)
    body = document.get("record")
    if isinstance(body, dict):
        relative = declaration["payload"]["record_path"]
        raw = schema.dumps(body).encode("utf-8") + b"\n"
        target = pathlib.Path(bundle) / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)


def refresh_manifest(bundle) -> None:
    """Re-hash every listed file after an authorised append (holder refresh)."""

    path = pathlib.Path(bundle) / "manifest.json"
    manifest = schema.load_json(path)
    manifest["files"] = [
        records.file_entry(
            bundle,
            str(entry["path"]),
            kind=str(entry["kind"]),
            record_id=str(entry["id"]),
            event_count=entry.get("event_count"),
        )
        for entry in manifest["files"]
    ]
    manifest["store_digest"] = records.manifest_digest(manifest)
    write_json(path, manifest)


def git(root, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(root)] + list(args),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ, **GIT_ENV},
        check=False,
        timeout=120,
    )
    if completed.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (args, completed.stderr.decode("utf-8", "replace")))
    return completed.stdout.decode("utf-8", "replace")


def make_repo(directory, files: dict) -> pathlib.Path:
    """A real worktree with one deterministic commit on main and origin/main."""

    root = pathlib.Path(directory)
    root.mkdir(parents=True, exist_ok=True)
    git(root, "init", "-q", "-b", "main")
    git(root, "config", "user.email", "fixture@example.invalid")
    git(root, "config", "user.name", "Fixture Builder")
    git(root, "config", "core.autocrlf", "false")
    for relative, content in sorted(files.items()):
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "synthetic fixture base")
    git(root, "update-ref", "refs/remotes/origin/main", "HEAD")
    return root


def commit_of(root) -> str:
    return git(root, "rev-parse", "HEAD").strip()


def codes(issues) -> list:
    return sorted({issue.code for issue in issues})


def blockers_codes(report: dict) -> list:
    return sorted({blocker["code"] for blocker in report["blockers"]})


def merged_fixtures():
    """Load the merged checker's fixture builder read-only (or None if absent)."""

    path = REPO_ROOT / "tools" / "aegis_verdict_gate" / "tests" / "_fixtures.py"
    if not path.is_file():
        return None
    import importlib.util

    spec = importlib.util.spec_from_file_location("aegis_merged_gate_fixtures", str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
