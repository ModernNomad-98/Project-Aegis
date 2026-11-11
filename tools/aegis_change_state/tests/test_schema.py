"""Closed-schema, canonicalization and envelope tests (C1.2 D1)."""

from __future__ import annotations

import json
import pathlib
import sys
import unittest

if str(pathlib.Path(__file__).resolve().parents[3]) not in sys.path:
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

import _fixtures  # noqa: E402
from tools.aegis_change_state import schema  # noqa: E402

JCS_VECTOR_VALUE = {"b": [True, None, "x"], "a": 1, "n": -0.0}
JCS_VECTOR_TEXT = '{"a":1,"b":[true,null,"x"],"n":0}'


class CanonicalizationTest(unittest.TestCase):
    def test_dumps_matches_the_pinned_jcs_shape(self):
        self.assertEqual(schema.dumps(JCS_VECTOR_VALUE), JCS_VECTOR_TEXT)
        self.assertEqual(schema.digest(JCS_VECTOR_VALUE), schema.sha256_hex(JCS_VECTOR_TEXT.encode("utf-8")))
        self.assertEqual(len(schema.canonical_bytes(JCS_VECTOR_VALUE)), len(JCS_VECTOR_TEXT))

    def test_unsupported_value_is_refused(self):
        with self.assertRaises(schema.SchemaError):
            schema.dumps({1: "non-string key"})

    def test_merged_checker_canonicalization_agrees(self):
        """The local JCS implementation must agree with the merged checker's."""

        try:
            from tools.aegis_verdict_gate import canonical as module
        except ImportError:
            self.skipTest("merged checker is absent at this head: A7 rebind required (UNRUN)")
        for value in (
            {"a": 1, "b": ["x", None, True]},
            {"z": {"y": [1, 2.5, -3]}, "a": "text"},
            _fixtures.load("valid-freeze.json")["payload"],
            _fixtures.load("valid-settlement.json")["payload"],
        ):
            self.assertEqual(schema.dumps(value), module.dumps(value))
            self.assertEqual(schema.digest(value), module.digest(value))


class EnvelopeTest(unittest.TestCase):
    def test_build_envelope_declares_the_payload_binding(self):
        document = _fixtures.envelope({"a": 1})
        self.assertEqual(document["provenance"]["declared_payload_sha256"], schema.digest({"a": 1}))
        self.assertEqual(document["provenance"]["declared_payload_bytes"], len(schema.canonical_bytes({"a": 1})))
        self.assertEqual(schema.envelope_issues(document), [])

    def test_tampered_declared_hash_is_refused(self):
        document = _fixtures.envelope({"a": 1})
        document["provenance"]["declared_payload_sha256"] = "0" * 64
        self.assertEqual(_fixtures.codes(schema.envelope_issues(document)), [schema.CODE_CANONICAL])

    def test_missing_provenance_is_refused(self):
        document = {"payload": {"a": 1}}
        self.assertEqual(_fixtures.codes(schema.envelope_issues(document)), [schema.CODE_REQUIRED_INPUT])

    def test_extra_top_level_field_is_refused(self):
        document = _fixtures.envelope({"a": 1})
        document["notes"] = "not an envelope field"
        self.assertEqual(_fixtures.codes(schema.envelope_issues(document)), [schema.CODE_CANONICAL])

    def test_provenance_requires_an_identity_ref(self):
        document = _fixtures.envelope({"a": 1})
        del document["provenance"]["producer_identity_ref"]
        self.assertEqual(_fixtures.codes(schema.envelope_issues(document)), [schema.CODE_REQUIRED_INPUT])

    def test_input_status_vocabulary_is_closed(self):
        document = _fixtures.envelope({"a": 1}, status="TRUSTED")
        self.assertEqual(_fixtures.codes(schema.envelope_issues(document)), [schema.CODE_CANONICAL])


class ClosedSchemaTest(unittest.TestCase):
    def test_every_fixture_payload_validates_against_its_closed_schema(self):
        mapping = {
            "valid-freeze.json": "freeze",
            "freeze-mutated-after-freeze.json": "freeze",
            "freeze-head-moved.json": "freeze",
            "valid-settlement.json": "settlement",
            "settlement-pending-review.json": "settlement",
            "settlement-unavailable-no-authority.json": "settlement",
            "stage-B.json": "stage",
            "stage-D.json": "stage",
            "stage-E.json": "stage",
            "stage-duplicate-lane.json": "stage",
            "stage-substitution.json": "stage",
            "head-history-valid.json": "head_history",
            "head-history-foreign-export.json": "head_history",
            "snapshot-manifest-valid.json": "snapshot",
            "snapshot-archive-mismatch.json": "snapshot",
        }
        for name, kind in sorted(mapping.items()):
            with self.subTest(fixture=name):
                self.assertEqual(schema.payload_issues(kind, _fixtures.payload(name)), [])

    def test_unknown_field_is_refused(self):
        payload = _fixtures.payload("valid-freeze.json")
        payload["confidence"] = "high"
        self.assertEqual(_fixtures.codes(schema.payload_issues("freeze", payload)), [schema.CODE_CANONICAL])

    def test_missing_required_field_is_refused(self):
        payload = _fixtures.payload("valid-freeze.json")
        del payload["settlement_ref"]
        self.assertEqual(_fixtures.codes(schema.payload_issues("freeze", payload)), [schema.CODE_REQUIRED_INPUT])

    def test_optional_fields_may_be_absent(self):
        payload = _fixtures.payload("stage-B.json")
        payload.pop("waiver_ref", None)
        payload.pop("replacement_of", None)
        self.assertEqual(schema.payload_issues("stage", payload), [])

    def test_hex_and_enum_values_are_checked(self):
        payload = _fixtures.payload("valid-freeze.json")
        payload["head_sha"] = "not-hex"
        payload["valid"] = "yes"
        self.assertEqual(len(schema.payload_issues("freeze", payload)), 2)

    def test_snapshot_flags_are_pinned(self):
        payload = _fixtures.payload("snapshot-manifest-valid.json")
        payload["flags"] = ["--format=tar", "--prefix=other/"]
        self.assertEqual(_fixtures.codes(schema.payload_issues("snapshot", payload)), [schema.CODE_CANONICAL])

    def test_stage_verdict_vocabulary(self):
        payload = _fixtures.payload("stage-D.json")
        payload["verdict"] = "PASS"
        self.assertEqual(schema.payload_issues("stage", payload), [])
        self.assertNotIn("PASS", schema.STAGE_VERDICTS["D"])

    def test_immutable_inputs_digest_uses_the_merged_six_terms(self):
        immutable = _fixtures.payload("valid-freeze.json")["immutable_inputs"]
        expected = schema.digest(
            {
                "head": immutable["head_sha"],
                "tree": immutable["tree_sha"],
                "base": immutable["base_sha"],
                "policy_sha256": immutable["policy_sha256"],
                "plan_sha256": immutable["plan_sha256"],
                "evidence_inputs_sha256": immutable["evidence_inputs_sha256"],
            }
        )
        self.assertEqual(schema.immutable_inputs_digest(immutable), expected)


if __name__ == "__main__":
    unittest.main()
