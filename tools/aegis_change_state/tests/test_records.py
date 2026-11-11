"""Append-only records, chain, manifest and git-prefix tests (C1.2 D1)."""

from __future__ import annotations

import json
import pathlib
import sys
import unittest

if str(pathlib.Path(__file__).resolve().parents[3]) not in sys.path:
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

import _fixtures  # noqa: E402
from tools.aegis_change_state import records, schema  # noqa: E402

EVENTS = [
    {
        "head_sha": "2a4c6e8f0b1d3f5a7c9e1b3d5f7a9c2e4b6d8f0a",
        "kind": "INITIAL",
        "exception_ref": None,
        "counted_at": "2026-11-10T18:00:00Z",
        "recorded_by": "fixture",
    },
    {
        "head_sha": "6f8e4d2c0b9a7f5e3d1c9b8a6f4e2d0c8b6a5f3e",
        "kind": "BATCHED_BLOCKING_FIX",
        "exception_ref": None,
        "counted_at": "2026-11-10T22:00:00Z",
        "recorded_by": "fixture",
    },
]


class LedgerChainTest(unittest.TestCase):
    def setUp(self):
        self.temporary = _fixtures.temporary_directory()
        self.addCleanup(lambda: __import__("shutil").rmtree(str(self.temporary), ignore_errors=True))
        self.path = self.temporary / "ledger.jsonl"
        records.write_ledger(self.path, EVENTS)

    def test_written_chain_validates(self):
        events, lines, issues = records.read_jsonl(self.path)
        self.assertEqual(issues, [])
        self.assertEqual(len(events), 2)
        self.assertEqual(records.validate_chain(events, lines), [])
        self.assertIsNone(events[0]["prev_event_sha256"])
        self.assertEqual(events[1]["prev_event_sha256"], schema.sha256_hex(lines[0]))

    def test_edited_line_is_tamper(self):
        lines = self.path.read_bytes().split(b"\n")
        lines[0] = lines[0].replace(b"fixture", b"rewritten")
        self.path.write_bytes(b"\n".join(lines))
        events, raw_lines, issues = records.read_jsonl(self.path)
        self.assertIn(schema.CODE_TAMPER, _fixtures.codes(issues + records.validate_chain(events, raw_lines)))

    def test_removed_line_is_tamper(self):
        lines = self.path.read_bytes().split(b"\n")
        self.path.write_bytes(b"\n".join(lines[1:]))
        events, raw_lines, _issues = records.read_jsonl(self.path)
        self.assertIn(schema.CODE_TAMPER, _fixtures.codes(records.validate_chain(events, raw_lines)))

    def test_decreased_sequence_is_tamper(self):
        lines = [json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines()]
        lines[1]["seq"] = 1
        events = lines
        raw = [schema.dumps(event).encode("utf-8") for event in events]
        self.assertIn(schema.CODE_TAMPER, _fixtures.codes(records.validate_chain(events, raw)))

    def test_non_canonical_line_is_tamper(self):
        raw = self.path.read_bytes()
        self.path.write_bytes(raw.replace(b'"kind":"INITIAL"', b'"kind": "INITIAL"'))
        _events, _lines, issues = records.read_jsonl(self.path)
        self.assertEqual(_fixtures.codes(issues), [schema.CODE_TAMPER])

    def test_append_keeps_the_chain_and_sequence(self):
        appended = records.append_event(
            self.path,
            {
                "head_sha": "8e0f2a4c6b8d0e1f3a5c7b9d2e4f6a8c0b1d3e5f",
                "kind": "FINAL_BLOCKING_FIX",
                "exception_ref": None,
                "counted_at": "2026-11-11T02:00:00Z",
                "recorded_by": "fixture",
            },
        )
        self.assertEqual(appended["seq"], 3)
        events, lines, issues = records.read_jsonl(self.path)
        self.assertEqual(records.validate_chain(events, lines), [])
        self.assertEqual(events[-1]["prev_event_sha256"], schema.sha256_hex(lines[-2]))


class ManifestTest(unittest.TestCase):
    def setUp(self):
        self.temporary = _fixtures.temporary_directory()
        self.addCleanup(lambda: __import__("shutil").rmtree(str(self.temporary), ignore_errors=True))
        self.root = self.temporary / "store"
        self.root.mkdir()
        records.write_ledger(self.root / "ledger.jsonl", EVENTS)
        (self.root / "freeze.json").write_text("{}\n", encoding="utf-8")
        self.files = [
            records.file_entry(self.root, "freeze.json", kind="freeze", record_id="freeze-1"),
            records.file_entry(self.root, "ledger.jsonl", kind="change_ledger", record_id="change-1", event_count=2),
        ]
        self.manifest = records.build_manifest("change-1", self.files, {"review_heads": {"used": 2}})

    def test_digest_is_deterministic_and_recomputable(self):
        same = records.build_manifest("change-1", list(reversed(self.files)), {"review_heads": {"used": 2}})
        self.assertEqual(self.manifest["store_digest"], same["store_digest"])
        self.assertEqual(records.validate_manifest(self.root, self.manifest), [])

    def test_no_volatile_or_generated_fields(self):
        text = json.dumps(self.manifest)
        self.assertNotIn("generated_at", text)
        self.assertNotIn("timestamp", text)

    def test_provenance_defaults_to_unverified(self):
        binding = self.manifest["provenance_binding"]
        self.assertEqual(binding["binding_status"], "UNVERIFIED")
        self.assertEqual(binding["authority_kind"], "UNKNOWN")
        self.assertIsNone(binding["authority_ref_id"])

    def test_tampered_file_is_detected(self):
        (self.root / "freeze.json").write_text('{"edited": true}\n', encoding="utf-8")
        self.assertIn(schema.CODE_TAMPER, _fixtures.codes(records.validate_manifest(self.root, self.manifest)))

    def test_digest_change_is_detected(self):
        manifest = dict(self.manifest)
        manifest["derived_counts_at_binding"] = {"review_heads": {"used": 1}}
        self.assertIn(schema.CODE_TAMPER, _fixtures.codes(records.validate_manifest(self.root, manifest)))

    def test_enforced_claim_and_verified_coverage_are_refused(self):
        manifest = dict(self.manifest)
        manifest["assurance_claim"] = "ENFORCED"
        manifest["mounted_coverage"] = "VERIFIED"
        manifest["store_digest"] = records.manifest_digest(manifest)
        codes = _fixtures.codes(records.validate_manifest(self.root, manifest))
        self.assertEqual(codes, [schema.CODE_CANONICAL])

    def test_fabricated_verified_binding_is_tamper(self):
        manifest = dict(self.manifest)
        manifest["provenance_binding"] = dict(manifest["provenance_binding"])
        manifest["provenance_binding"]["binding_status"] = "VERIFIED"
        manifest["provenance_binding"]["authority_kind"] = "UNKNOWN"
        manifest["store_digest"] = records.manifest_digest(manifest)
        self.assertIn(schema.CODE_TAMPER, _fixtures.codes(records.validate_manifest(self.root, manifest)))


class GitPrefixTest(unittest.TestCase):
    def setUp(self):
        self.temporary = _fixtures.temporary_directory()
        self.addCleanup(lambda: __import__("shutil").rmtree(str(self.temporary), ignore_errors=True))
        self.repo = _fixtures.make_repo(
            self.temporary / "repo",
            {"store/ledger.jsonl": '{"seq":1}\n{"seq":2}\n', "store/freeze.json": "{}\n"},
        )

    def test_new_and_prefixed_files_pass(self):
        with (self.repo / "store" / "ledger.jsonl").open("a", encoding="utf-8", newline="\n") as handle:
            handle.write('{"seq":3}\n')
        report = records.prefix_check(self.repo, ["store/ledger.jsonl", "store/new.json"], "origin/main")
        self.assertEqual(report["store/ledger.jsonl"], "PREFIX_OK")
        self.assertEqual(report["store/new.json"], "MISSING")
        self.assertEqual(report["__status__"], "CHECKED")

    def test_rewritten_base_line_is_a_prefix_violation(self):
        (self.repo / "store" / "ledger.jsonl").write_text('{"seq":9}\n{"seq":2}\n', encoding="utf-8")
        report = records.prefix_check(self.repo, ["store/ledger.jsonl"], "origin/main")
        self.assertEqual(report["store/ledger.jsonl"], "PREFIX_VIOLATION")

    def test_unresolved_base_is_reported_never_skipped(self):
        plain = self.temporary / "not-a-repo"
        plain.mkdir()
        (plain / "store").mkdir()
        (plain / "store" / "ledger.jsonl").write_text("{}\n", encoding="utf-8")
        report = records.prefix_check(plain, ["store/ledger.jsonl"], "origin/main")
        self.assertEqual(report["__status__"], "GIT_BASE_UNRESOLVED")
        self.assertEqual(report["store/ledger.jsonl"], "GIT_BASE_UNRESOLVED")


if __name__ == "__main__":
    unittest.main()
