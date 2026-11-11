"""Tests for the aegis.evidence-reuse/1 validator (RU-01..RU-12)."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import _fixtures as fixtures  # noqa: E402
from tools.aegis_evidence_reuse import schema, validate  # noqa: E402


class ReuseValidationTests(unittest.TestCase):
    def validate_case(self, name: str, **overrides) -> dict:
        case = fixtures.load_case(name)
        record = fixtures.build_record(case)
        for key, value in overrides.items():
            if value is None:
                record.pop(key, None)
            else:
                record[key] = value
        return validate.validate_record(
            record,
            target_head=case["target_head"],
            change_id=42,
            evidence_records=case["evidence"],
            requirement_ids={"MG1"},
        )

    def assert_rule(self, result: dict, rule_id: str) -> None:
        rules = {item["rule_id"] for item in result["violations"]}
        self.assertIn(rule_id, rules, result["violations"])

    def test_valid_docs_only(self) -> None:
        result = self.validate_case("valid-docs-only")
        self.assertTrue(result["valid"], result["violations"])
        self.assertEqual(result["effective_decision"], "VALID")
        self.assertTrue(all(check["status"] == "PASS" for check in result["checks"]))

    def test_docstring_only_with_ast(self) -> None:
        result = self.validate_case("docstring-only-with-ast")
        self.assertTrue(result["valid"], result["violations"])
        self.assertEqual(result["effective_decision"], "VALID")
        rule = {check["rule_id"]: check for check in result["checks"]}["RU-06"]
        self.assertEqual(rule["status"], "PASS")
        self.assertTrue(rule["applicable"])

    def test_test_change_refused(self) -> None:
        result = self.validate_case("test-change-no-reuse")
        self.assertFalse(result["valid"])
        self.assert_rule(result, "RU-07")

    def test_config_change_refused(self) -> None:
        result = self.validate_case("config-change-no-reuse")
        self.assertFalse(result["valid"])
        self.assert_rule(result, "RU-08")

    def test_behavior_change_refused(self) -> None:
        result = self.validate_case("behavior-change-no-reuse")
        self.assertFalse(result["valid"])
        self.assert_rule(result, "RU-09")

    def test_copied_pass_refused(self) -> None:
        result = self.validate_case("copied-pass-invalid")
        self.assertFalse(result["valid"])
        self.assert_rule(result, "RU-10")

    def test_stale_target(self) -> None:
        result = self.validate_case("stale-target-invalid")
        self.assertEqual(result["effective_decision"], "STALE")
        self.assert_rule(result, "RU-04")

    def test_ast_only_code_claim_refused(self) -> None:
        result = self.validate_case("ast-only-code-invalid")
        self.assertFalse(result["valid"])
        self.assert_rule(result, "RU-06")

    def test_unknown_field_refused(self) -> None:
        case = fixtures.load_case("valid-docs-only")
        record = fixtures.build_record(case)
        record["unexpected"] = True
        result = validate.validate_record(
            record, target_head=case["target_head"], evidence_records=case["evidence"], requirement_ids={"MG1"}
        )
        self.assertFalse(result["valid"])
        self.assert_rule(result, "RU-01")

    def test_malformed_head_refused(self) -> None:
        case = fixtures.load_case("valid-docs-only")
        record = fixtures.build_record(case)
        record["target"]["target_head"] = "not-a-head"
        result = validate.validate_record(
            record, target_head="d" * 40, evidence_records=case["evidence"], requirement_ids={"MG1"}
        )
        self.assertFalse(result["valid"])
        self.assert_rule(result, "RU-02")

    def test_missing_evidence_refused(self) -> None:
        case = fixtures.load_case("valid-docs-only")
        record = fixtures.build_record(case)
        result = validate.validate_record(
            record, target_head=case["target_head"], evidence_records=[], requirement_ids={"MG1"}
        )
        self.assertFalse(result["valid"])
        self.assert_rule(result, "RU-03")

    def test_provenance_tamper_refused(self) -> None:
        case = fixtures.load_case("valid-docs-only")
        record = fixtures.build_record(case)
        record["provenance"]["declared_payload_sha256"] = "0" * 64
        result = validate.validate_record(
            record, target_head=case["target_head"], evidence_records=case["evidence"], requirement_ids={"MG1"}
        )
        self.assertFalse(result["valid"])
        self.assert_rule(result, "RU-12")

    def mutated_case(self, name: str, mutate) -> dict:
        case = fixtures.load_case(name)
        record = fixtures.build_record(case)
        mutate(record)
        record["provenance"]["declared_payload_sha256"] = schema.payload_digest(record)
        record["provenance"]["declared_payload_bytes"] = schema.payload_bytes(record)
        return validate.validate_record(
            record,
            target_head=case["target_head"],
            change_id=42,
            evidence_records=case["evidence"],
            requirement_ids={"MG1"},
        )

    def test_required_ci_unrun_refused(self) -> None:
        def mutate(record: dict) -> None:
            record["target_delta_checks"][0]["result"] = "UNRUN"

        result = self.mutated_case("valid-docs-only", mutate)
        self.assertFalse(result["valid"])
        self.assert_rule(result, "RU-05")
        self.assert_rule(result, "RU-11")

    def test_missing_excluded_claim_refused(self) -> None:
        def mutate(record: dict) -> None:
            record["excluded_claims"] = ["APPROVAL"]

        result = self.mutated_case("valid-docs-only", mutate)
        self.assertFalse(result["valid"])
        self.assert_rule(result, "RU-10")

    def test_unknown_decision_authority_refused(self) -> None:
        def mutate(record: dict) -> None:
            record["decision_authority"] = {
                "authority_kind": "UNKNOWN",
                "authority_ref_id": None,
                "authority_ref_sha256": None,
            }

        result = self.mutated_case("valid-docs-only", mutate)
        self.assertFalse(result["valid"])
        self.assert_rule(result, "RU-10")

    def test_determinism(self) -> None:
        first = self.validate_case("valid-docs-only")
        second = self.validate_case("valid-docs-only")
        self.assertEqual(json.dumps(first, sort_keys=True), json.dumps(second, sort_keys=True))

    def test_schema_file_matches_code(self) -> None:
        path = REPO_ROOT / "docs" / "conformance" / "evidence-reuse-v1.schema.json"
        document = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(set(document["properties"]), set(schema.TOP_LEVEL_FIELDS))
        self.assertEqual(set(document["required"]), set(schema.TOP_LEVEL_FIELDS))
        self.assertFalse(document["additionalProperties"])
        properties = document["properties"]
        self.assertEqual(properties["delta_class"]["enum"], list(schema.DELTA_CLASSES))
        self.assertEqual(properties["decision"]["enum"], list(schema.DECISIONS))
        self.assertEqual(
            properties["decision_authority"]["properties"]["authority_kind"]["enum"],
            list(schema.AUTHORITY_KINDS),
        )
        self.assertEqual(
            properties["excluded_claims"]["items"]["enum"], list(schema.EXCLUDED_CLAIMS)
        )
        self.assertEqual(
            properties["target_delta_checks"]["items"]["properties"]["kind"]["enum"],
            list(schema.CHECK_KINDS),
        )
        self.assertEqual(
            properties["target_delta_checks"]["items"]["properties"]["result"]["enum"],
            list(schema.CHECK_RESULTS),
        )
        self.assertEqual(properties["invalid_after"]["items"]["enum"], list(schema.INVALIDATION_EVENTS))
        self.assertEqual(set(properties["source"]["required"]), set(schema.SOURCE_FIELDS))
        self.assertFalse(properties["source"]["additionalProperties"])

    def test_schema_self_test(self) -> None:
        report = schema.self_test()
        self.assertTrue(report["ok"])
        self.assertEqual(report["violations"], [])


class ReuseCliTests(unittest.TestCase):
    def run_cli(self, arguments, *, stdin=None):
        return subprocess.run(
            [sys.executable, "-m", "tools.aegis_evidence_reuse"] + arguments,
            cwd=str(REPO_ROOT),
            input=stdin,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

    def write_case(self, directory: Path, name: str):
        case = fixtures.load_case(name)
        record = fixtures.build_record(case)
        record_path = directory / (name + ".json")
        record_path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
        evidence_path = directory / "evidence.json"
        evidence_path.write_text(json.dumps(case["evidence"], indent=2), encoding="utf-8")
        return case, record_path, evidence_path

    def test_cli_valid_exit_0(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            case, record_path, evidence_path = self.write_case(Path(temporary), "valid-docs-only")
            completed = self.run_cli(
                ["validate", "--record", str(record_path), "--target-head", case["target_head"],
                 "--evidence", str(evidence_path), "--json"]
            )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertTrue(json.loads(completed.stdout)["valid"])

    def test_cli_stale_exit_1(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            case, record_path, evidence_path = self.write_case(Path(temporary), "stale-target-invalid")
            completed = self.run_cli(
                ["validate", "--record", str(record_path), "--target-head", case["target_head"],
                 "--evidence", str(evidence_path), "--json"]
            )
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(json.loads(completed.stdout)["effective_decision"], "STALE")

    def test_cli_malformed_record_exit_2(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "record.json"
            path.write_text("{not json", encoding="utf-8")
            completed = self.run_cli(["validate", "--record", str(path), "--target-head", "d" * 40])
        self.assertEqual(completed.returncode, 2)
        self.assertEqual(completed.stdout, "")

    def test_cli_self_test(self) -> None:
        completed = self.run_cli(["--self-test"])
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertTrue(json.loads(completed.stdout)["ok"])

    def test_cli_stdin_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            case = fixtures.load_case("valid-docs-only")
            record = fixtures.build_record(case)
            path = Path(temporary) / "record.json"
            path.write_text(json.dumps(record), encoding="utf-8")
            completed = self.run_cli(
                ["validate", "--record", str(path), "--target-head", case["target_head"],
                 "--evidence", "-", "--json"],
                stdin=json.dumps(case["evidence"]),
            )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertTrue(json.loads(completed.stdout)["valid"])


if __name__ == "__main__":
    unittest.main()
