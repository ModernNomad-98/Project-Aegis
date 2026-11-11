"""Canonicalization tests: Appendix A vector, projection and determinism (AC3)."""

from __future__ import annotations

import hashlib
import pathlib
import sys
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.aegis_verdict_gate import canonical, catalogue  # noqa: E402


class SelfTestVectorTest(unittest.TestCase):
    def test_vector_is_560_bytes_and_hashes(self):
        line = canonical.dumps(canonical.SELF_TEST_INPUT)
        encoded = line.encode("utf-8")
        self.assertEqual(len(encoded), 560)
        self.assertEqual(canonical.sha256_hex(encoded), canonical.SELF_TEST_SHA256)
        self.assertEqual(
            canonical.SELF_TEST_SHA256,
            "098ad54886568bbc7e9103839d5ceda9a573d01f7d234d58a8747913e331bd5d",
        )

    def test_vector_matches_the_recorded_line_byte_for_byte(self):
        self.assertEqual(canonical.dumps(canonical.SELF_TEST_INPUT), canonical.SELF_TEST_CANONICAL)
        self.assertEqual(
            hashlib.sha256(canonical.SELF_TEST_CANONICAL.encode("utf-8")).hexdigest(),
            canonical.SELF_TEST_SHA256,
        )

    def test_self_test_report(self):
        report = canonical.self_test()
        self.assertTrue(report["ok"])
        self.assertEqual(report["bytes"], 560)
        self.assertEqual(report["expected_bytes"], 560)
        self.assertTrue(report["serialization_matches"])


class SerializationTest(unittest.TestCase):
    def test_keys_sorted(self):
        self.assertEqual(canonical.dumps({"b": 1, "a": 2}), '{"a":2,"b":1}')

    def test_no_insignificant_whitespace(self):
        self.assertEqual(canonical.dumps({"a": [1, 2], "b": {"c": True}}), '{"a":[1,2],"b":{"c":true}}')

    def test_arrays_keep_given_order(self):
        self.assertEqual(canonical.dumps(["implementer", "pr-author"]), '["implementer","pr-author"]')

    def test_scalars(self):
        self.assertEqual(canonical.dumps(None), "null")
        self.assertEqual(canonical.dumps(True), "true")
        self.assertEqual(canonical.dumps(False), "false")
        self.assertEqual(canonical.dumps(42), "42")
        self.assertEqual(canonical.dumps(-7), "-7")
        self.assertEqual(canonical.dumps(0), "0")

    def test_strings_keep_utf8_and_escape_controls(self):
        self.assertEqual(canonical.dumps("example-org"), '"example-org"')
        self.assertEqual(canonical.dumps("a\"b"), '"a\\"b"')
        self.assertEqual(canonical.dumps("line\nfeed"), '"line\\nfeed"')
        self.assertEqual(canonical.dumps("caf\u00e9"), '"caf\u00e9"')
        self.assertEqual(len(canonical.canonical_bytes("caf\u00e9")), len('"caf\u00e9"'.encode("utf-8")))

    def test_nested_dotted_projection_round_trip(self):
        document = {}
        catalogue.set_path(document, "reviewer.independence.class", "INDEPENDENT")
        present, value = catalogue.get_path(document, "reviewer.independence.class")
        self.assertTrue(present)
        self.assertEqual(value, "INDEPENDENT")
        self.assertEqual(document, {"reviewer": {"independence": {"class": "INDEPENDENT"}}})

    def test_non_finite_numbers_are_refused(self):
        with self.assertRaises(canonical.CanonicalizationError):
            canonical.dumps(float("nan"))
        with self.assertRaises(canonical.CanonicalizationError):
            canonical.dumps(float("inf"))

    def test_digest_is_deterministic(self):
        self.assertEqual(canonical.digest({"a": 1}), canonical.digest({"a": 1}))
        self.assertNotEqual(canonical.digest({"a": 1}), canonical.digest({"a": 2}))


class ProjectionTest(unittest.TestCase):
    def test_projection_excludes_the_hash_and_the_gate_time_row(self):
        document = {
            "head_sha": "a" * 40,
            "bound_fields_sha256": "f" * 64,
            "owner_line": {"id": "APR-TEST", "effective_status_at_gate": "ACTIVE"},
            "record": {"body_text": "not hashed"},
            "not_a_catalogue_field": True,
        }
        projection = canonical.project_bound_fields(document)
        self.assertEqual(projection, {"head_sha": "a" * 40, "owner_line": {"id": "APR-TEST"}})

    def test_projection_keeps_present_optional_and_conditional_fields(self):
        document = {
            "parents": ["b" * 40],
            "plan": {"sha256": "c" * 64, "basis_ref": None},
            "conditionals_applied": [{"condition_id": "VB-C03", "applied": True, "basis_ref": "plan"}],
        }
        projection = canonical.project_bound_fields(document)
        self.assertIn("parents", projection)
        self.assertIn("conditionals_applied", projection)
        # A present conditional field with its explicit null is hashed as null.
        self.assertEqual(projection["plan"], {"sha256": "c" * 64, "basis_ref": None})

    def test_bound_hash_is_over_the_projection_not_the_record(self):
        document = {"head_sha": "a" * 40, "record": {"body_text": "one"}}
        changed = {"head_sha": "a" * 40, "record": {"body_text": "two"}}
        self.assertEqual(canonical.bound_fields_sha256(document), canonical.bound_fields_sha256(changed))

    def test_bound_hash_changes_with_a_canonical_field(self):
        document = {"head_sha": "a" * 40}
        changed = {"head_sha": "b" * 40}
        self.assertNotEqual(canonical.bound_fields_sha256(document), canonical.bound_fields_sha256(changed))


if __name__ == "__main__":
    unittest.main()
