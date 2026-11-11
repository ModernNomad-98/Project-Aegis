"""Catalogue tests: 62 entries, group counts, v2.1 identity, one source (AC3)."""

from __future__ import annotations

import pathlib
import sys
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
SCRIPTS_DIR = pathlib.Path(__file__).resolve().parents[2]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from aegis_verdict_gate import catalogue  # noqa: E402

TOOL_DIR = pathlib.Path(__file__).resolve().parents[1]
SCAN_ROOTS = ("docs", "tools", "scripts", ".github")
SCAN_SUFFIXES = {".md", ".py", ".json", ".jsonl", ".yml", ".yaml", ".txt"}
SKIP_DIRS = {"evidence", "artifacts", ".git", "fixtures", "revision-state"}


class CatalogueTest(unittest.TestCase):
    def test_exactly_62_entries(self):
        self.assertEqual(len(catalogue.ENTRIES), 62)
        self.assertEqual(len(catalogue.ENTRIES_BY_ID), 62)
        self.assertEqual(len(catalogue.ENTRIES_BY_PATH), 62)

    def test_group_counts(self):
        counts = {}
        for entry in catalogue.ENTRIES:
            counts[entry.group] = counts.get(entry.group, 0) + 1
        self.assertEqual(counts, {"A": 12, "B": 4, "C": 9, "D": 3, "E": 4, "F": 15, "G": 3, "H": 11, "I": 1})
        self.assertEqual(catalogue.GROUP_COUNTS, counts)

    def test_entry_ids_are_contiguous_per_group(self):
        for group, count in catalogue.GROUP_COUNTS.items():
            entries = catalogue.entries_for_group(group)
            self.assertEqual(len(entries), count)
            expected = ["VB-%s%02d" % (group, index) for index in range(1, count + 1)]
            self.assertEqual([entry.entry_id for entry in entries], expected)

    def test_requiredness_vocabulary(self):
        seen = {entry.requiredness for entry in catalogue.ENTRIES}
        self.assertEqual(seen, {"R", "O", "C"})
        conditional = {entry.entry_id for entry in catalogue.conditional_entries()}
        self.assertEqual(conditional, {"VB-C03", "VB-C05", "VB-C08", "VB-D03", "VB-G03", "VB-H02"})

    def test_v2_1_identity_and_changed_entries(self):
        self.assertEqual(catalogue.BOUND_SET_ID, "aegis.verdict-bound/v2.1")
        self.assertEqual(catalogue.BOUND_SET_VERSION, "2.1")
        self.assertEqual(catalogue.CANONICALIZATION_VERSION, "JCS-RFC8785-v1")
        self.assertNotEqual(catalogue.BOUND_SET_ID, "aegis.verdict-bound/v2")
        self.assertEqual(len(catalogue.V2_1_CHANGED_ENTRIES), 7)
        for entry_id in catalogue.V2_1_CHANGED_ENTRIES:
            self.assertIn(entry_id, catalogue.ENTRIES_BY_ID)

    def test_hashed_projection_is_61_not_62(self):
        hashed = catalogue.hashed_entries()
        self.assertEqual(len(hashed), 61)
        self.assertNotIn("VB-I01", [entry.entry_id for entry in hashed])
        self.assertIn("VB-I01", catalogue.ENTRIES_BY_ID)
        self.assertNotIn("bound_fields_sha256", catalogue.hashed_paths())

    def test_gate_time_row_is_not_a_catalogue_entry(self):
        self.assertNotIn("owner_line.effective_status_at_gate", catalogue.ENTRIES_BY_PATH)
        self.assertIn("owner_line.effective_status_at_gate", catalogue.GATE_TIME_ONLY_PATHS)
        schema = catalogue.allowed_schema()
        self.assertEqual(set(schema["owner_line"]), {"id", "register_sha256"})

    def test_closed_schema_covers_every_top_level_group(self):
        schema = catalogue.allowed_schema()
        tops = {entry.path.split(".")[0] for entry in catalogue.ENTRIES}
        self.assertEqual(set(schema), tops)
        self.assertEqual(set(schema["reviewer"]), {"identity_ref", "role", "auth_method", "auth_verified", "independence"})
        self.assertEqual(set(schema["reviewer"]["independence"]), {"class", "distinct_from", "attestation_ref"})
        self.assertEqual(set(schema["plan"]), {"sha256", "revision_count", "basis_ref"})

    def test_one_source_rule_no_second_field_list(self):
        offenders = []
        for root_name in SCAN_ROOTS:
            root = REPO_ROOT / root_name
            if not root.is_dir():
                continue
            for path in root.rglob("*"):
                if not path.is_file() or path.suffix not in SCAN_SUFFIXES:
                    continue
                try:
                    relative = path.relative_to(REPO_ROOT)
                except ValueError:
                    continue
                if relative.parts and relative.parts[0] == "scripts" and relative.parts[1] == TOOL_DIR.name:
                    continue
                if any(part in SKIP_DIRS for part in relative.parts):
                    continue
                if path.stat().st_size > 400_000:
                    continue
                text = path.read_text(encoding="utf-8", errors="ignore")
                if "aegis.verdict-bound" in text or "VB-F09" in text:
                    offenders.append(str(relative))
        self.assertEqual(offenders, [], "a second canonical field list must not exist outside the tool")


if __name__ == "__main__":
    unittest.main()
