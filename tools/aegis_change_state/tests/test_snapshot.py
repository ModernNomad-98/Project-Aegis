"""Per-head snapshot manifest and reproducibility tests (C1.2 D1)."""

from __future__ import annotations

import pathlib
import sys
import unittest

if str(pathlib.Path(__file__).resolve().parents[3]) not in sys.path:
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

import _fixtures  # noqa: E402
from tools.aegis_change_state import records, schema, snapshot  # noqa: E402

FILES = {
    "README.md": "synthetic fixture tree\n",
    "package/one.py": "VALUE = 1\n",
    "package/nested/two.py": "VALUE = 2\n",
}


class SnapshotManifestTest(unittest.TestCase):
    def setUp(self):
        self.temporary = _fixtures.temporary_directory()
        self.addCleanup(lambda: __import__("shutil").rmtree(str(self.temporary), ignore_errors=True))
        self.repo = _fixtures.make_repo(self.temporary / "repo", FILES)
        self.commit = _fixtures.commit_of(self.repo)
        self.tree = snapshot.tree_of(self.repo, self.commit)
        self.manifest = snapshot.build_manifest(
            self.repo,
            self.commit,
            change_id="change-1",
            base="7c1d3e5f9a2b4c6d8e0f1a3b5c7d9e2f4a6b8c0d",
            retention_ref="PROGRAMME-EXECUTION-2026-11-10/snapshots/",
            created_by="snapshot-producer",
            created_at="2026-11-11T05:25:00Z",
        )

    def test_manifest_binds_commit_tree_base_and_archive(self):
        self.assertEqual(self.manifest["commit"], self.commit)
        self.assertEqual(self.manifest["tree"], self.tree)
        self.assertEqual(self.manifest["method"], "git-archive")
        self.assertEqual(self.manifest["flags"], ["--format=tar"])
        self.assertGreater(self.manifest["archive_bytes"], 0)
        self.assertGreater(self.manifest["file_count"], 0)
        self.assertEqual(schema.payload_issues("snapshot", self.manifest), [])

    def test_manifest_reproduces_byte_for_byte(self):
        again = snapshot.build_manifest(
            self.repo,
            self.commit,
            change_id="change-1",
            base=self.manifest["base"],
            retention_ref=self.manifest["retention_ref"],
            created_by=self.manifest["created_by"],
            created_at=self.manifest["created_at"],
        )
        self.assertEqual(again, self.manifest)
        self.assertEqual(snapshot.verify_manifest(self.repo, self.manifest), [])

    def test_archive_mismatch_is_detected(self):
        tampered = dict(self.manifest)
        tampered["archive_sha256"] = "0" * 64
        self.assertIn(schema.CODE_TAMPER, _fixtures.codes(snapshot.verify_manifest(self.repo, tampered)))

    def test_file_count_mismatch_is_detected(self):
        tampered = dict(self.manifest)
        tampered["file_count"] = 999
        self.assertIn(schema.CODE_TAMPER, _fixtures.codes(snapshot.verify_manifest(self.repo, tampered)))

    def test_tree_mismatch_is_detected(self):
        tampered = dict(self.manifest)
        tampered["tree"] = "4b8e2f6a9c0d1e3f5a7b9c2d4e6f8a0b1c3d5e7f"
        self.assertIn(schema.CODE_TAMPER, _fixtures.codes(snapshot.verify_manifest(self.repo, tampered)))

    def test_working_tree_edits_do_not_change_the_snapshot(self):
        (self.repo / "README.md").write_text("edited but never committed\n", encoding="utf-8", newline="\n")
        (self.repo / "package" / "untracked.py").write_text("UNTRACKED = True\n", encoding="utf-8", newline="\n")
        again = snapshot.build_manifest(
            self.repo,
            self.commit,
            change_id="change-1",
            base=self.manifest["base"],
            retention_ref=self.manifest["retention_ref"],
            created_by=self.manifest["created_by"],
            created_at=self.manifest["created_at"],
        )
        self.assertEqual(again["archive_sha256"], self.manifest["archive_sha256"])
        self.assertEqual(again["file_count"], self.manifest["file_count"])

    def test_binding_to_the_frozen_head(self):
        freeze = _fixtures.payload("valid-freeze.json")
        issues = snapshot.binding_issues(self.manifest, freeze)
        self.assertEqual(len(issues), 3)
        self.assertEqual(_fixtures.codes(issues), [schema.CODE_HEAD_MOVED])
        matching = dict(freeze)
        matching.update({"head_sha": self.commit, "tree_sha": self.tree, "base_sha": self.manifest["base"], "change_id": "change-1"})
        self.assertEqual(snapshot.binding_issues(self.manifest, matching), [])

    def test_unnamed_retention_is_not_a_pass(self):
        manifest = dict(self.manifest)
        manifest["retention_ref"] = "UNNAMED"
        self.assertEqual(_fixtures.codes(snapshot.retention_issues(manifest)), [schema.CODE_REQUIRED_INPUT])

    def test_no_archive_or_binary_is_written(self):
        self.assertEqual([path for path in self.temporary.rglob("*.tar")], [])
        self.assertEqual([path for path in self.temporary.rglob("*.tar.gz")], [])

    def test_unknown_manifest_field_is_refused(self):
        manifest = dict(self.manifest)
        manifest["mounted_coverage"] = "VERIFIED"
        self.assertEqual(_fixtures.codes(schema.payload_issues("snapshot", manifest)), [schema.CODE_CANONICAL])

    def test_cli_writes_only_the_requested_manifest(self):
        out = self.temporary / "out" / "manifest.json"
        buffer = __import__("io").StringIO()
        with __import__("contextlib").redirect_stdout(buffer):
            code = _fixtures.cli.main(
                [
                    "snapshot-manifest",
                    "--repo",
                    str(self.repo),
                    "--commit",
                    self.commit,
                    "--change-id",
                    "change-1",
                    "--base",
                    self.manifest["base"],
                    "--retention-ref",
                    self.manifest["retention_ref"],
                    "--created-by",
                    "snapshot-producer",
                    "--created-at",
                    "2026-11-11T05:25:00Z",
                    "--out",
                    str(out),
                ]
            )
        self.assertEqual(code, 0)
        written = schema.load_json(out)
        self.assertEqual(written, self.manifest)
        self.assertEqual(sorted(path.name for path in (self.temporary / "out").iterdir()), ["manifest.json"])


if __name__ == "__main__":
    unittest.main()
