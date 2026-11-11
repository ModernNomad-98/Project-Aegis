"""Unit and negative-control tests for PF-01..PF-10."""

from __future__ import annotations

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
from tools.aegis_preflight import checks, models  # noqa: E402


def load_document(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def make_context(built, document=None, checker_result=None):
    return checks.Context(
        bundle=models.Bundle(
            path=Path(built["bundle"]),
            document=document if document is not None else load_document(Path(built["bundle"])),
        ),
        repo_root=Path(built["root"]),
        fixture_mode=True,
        code_root=REPO_ROOT,
        checker_result=checker_result,
    )


def statuses(results):
    return {item["check_id"]: item["status"] for item in results}


class PreflightCheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._temporary = tempfile.TemporaryDirectory()
        cls.clean = fixtures.build_case(fixtures.load_case("clean-bundle"), cls._temporary.name)

    @classmethod
    def tearDownClass(cls) -> None:
        cls._temporary.cleanup()

    def test_clean_all_pass_in_fixture_mode(self) -> None:
        results = checks.run_all(
            models.load_bundle(Path(self.clean["bundle"])),
            Path(self.clean["root"]),
            fixture_mode=True,
            supported_auth_methods=("provider-event-author",),
        )
        self.assertEqual(set(statuses(results).values()), {"PASS"})

    def test_pf07_input_hash_mismatch_is_refused(self) -> None:
        real_run = checks._run

        def tampering_runner(command, cwd):
            exit_code, stdout, stderr = real_run(command, cwd=cwd)
            document = json.loads(stdout)
            document["inputs_sha256"]["verdict"]["sha256"] = "0" * 64
            return exit_code, json.dumps(document), stderr

        results = checks.run_all(
            models.load_bundle(Path(self.clean["bundle"])),
            Path(self.clean["root"]),
            fixture_mode=True,
            supported_auth_methods=("provider-event-author",),
            checker_runner=tampering_runner,
        )
        by_id = {item["check_id"]: item for item in results}
        self.assertEqual(by_id["PF-07"]["status"], "FAIL")
        self.assertEqual(by_id["PF-07"]["reason_code"], "PF07_INPUT_HASH_MISMATCH")

    def test_pf07_blocked_checker_is_never_converted(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            built = fixtures.build_case(fixtures.load_case("checker-blocked-consistent"), temporary)
            results = checks.run_all(
                models.load_bundle(Path(built["bundle"])),
                Path(built["root"]),
                fixture_mode=True,
                supported_auth_methods=("provider-event-author",),
            )
        self.assertEqual(statuses(results)["PF-07"], "BLOCKED")

    def test_pf10_rejects_network_import(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "source"
            source.mkdir()
            (source / "bad.py").write_text("import socket\n", encoding="utf-8")
            context = make_context(self.clean)
            result = checks.check_pf10(context, source_root=source)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["reason_code"], "PF10_SELF_AUDIT_FAILED")

    def test_pf10_rejects_write_call(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "source"
            source.mkdir()
            (source / "bad.py").write_text(
                'from pathlib import Path\nPath("x").write_text("y")\n', encoding="utf-8"
            )
            context = make_context(self.clean)
            result = checks.check_pf10(context, source_root=source)
        self.assertEqual(result["status"], "FAIL")

    def test_pf03_gate_green_is_refused(self) -> None:
        document = load_document(Path(self.clean["bundle"]))
        document["inputs"]["gate_status"]["MG2"] = "green"
        context = make_context(self.clean, document=document)
        result = checks.check_pf03(context)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["reason_code"], "PF03_INVALID_STATUS")

    def test_pf05_unnamed_unrun_is_refused(self) -> None:
        document = load_document(Path(self.clean["bundle"]))
        document["inputs"]["evidence"][0]["result"] = "UNRUN"
        context = make_context(self.clean, document=document)
        result = checks.check_pf05(context)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["reason_code"], "PF05_EVIDENCE_INCOMPLETE")

    def test_pf09_bypass_displayed_green_is_refused(self) -> None:
        envelope_path = Path(self.clean["paths"]["verdict"])
        original = envelope_path.read_text(encoding="utf-8")
        try:
            document = json.loads(original)
            document["payload"]["record"]["bypasses"] = [
                {"bypass_id": "BYPASS-1", "displayed_as": "GREEN", "status": "GREEN"}
            ]
            envelope_path.write_text(json.dumps(document, indent=2), encoding="utf-8")
            context = make_context(self.clean, document=load_document(Path(self.clean["bundle"])))
            result = checks.check_pf09(context)
        finally:
            envelope_path.write_text(original, encoding="utf-8")
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["reason_code"], "PF09_UNTRUTHFUL_OUTPUT")

    def test_pf01_provenance_tamper_is_refused(self) -> None:
        document = load_document(Path(self.clean["bundle"]))
        document["provenance"]["declared_payload_sha256"] = "0" * 64
        context = make_context(self.clean, document=document)
        result = checks.check_pf01(context)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["reason_code"], "PF01_REQUIRED_FIELD")

    def test_pf04_open_blocking_mismatch_is_refused(self) -> None:
        document = load_document(Path(self.clean["bundle"]))
        document["inputs"]["triage"]["open_blocking"] = 1
        context = make_context(self.clean, document=document)
        result = checks.check_pf04(context)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["reason_code"], "PF04_ARITHMETIC_MISMATCH")

    def test_pf02_unresolved_evidence_is_refused(self) -> None:
        document = load_document(Path(self.clean["bundle"]))
        document["inputs"]["triage"]["findings"].append(
            {
                "finding_id": "F-404",
                "class": "NIT",
                "disposition": "NIT_ACCEPTED",
                "candidate_head": "a" * 40,
                "evidence_ref": "EV-404",
                "decided_by": {"role": "F", "identity_ref": "role-f-fixture"},
            }
        )
        context = make_context(self.clean, document=document)
        result = checks.check_pf02(context)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["reason_code"], "PF02_UNRESOLVED_REFERENCE")

    def test_pf06_stale_store_digest_is_refused(self) -> None:
        document = load_document(Path(self.clean["bundle"]))
        context = make_context(self.clean, document=document, checker_result={"store_digest": "0" * 64})
        result = checks.check_pf06(context)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["reason_code"], "PF06_STALE_GENERATED_RECORD")

    def test_pf08_invalid_reuse_decision_blocks(self) -> None:
        document = load_document(Path(self.clean["bundle"]))
        record_path = Path(self.clean["root"]) / "preflight" / "reuse" / "REUSE-INVALID.json"
        source = Path(self.clean["root"]) / "preflight" / "reuse" / "REUSE-CLEAN-0001.json"
        record = load_document(source)
        record["decision"] = "INVALID"
        record["provenance"]["declared_payload_sha256"] = models.digest(
            {key: value for key, value in record.items() if key != "provenance"}
        )
        record["provenance"]["declared_payload_bytes"] = len(
            models.canonical_bytes({key: value for key, value in record.items() if key != "provenance"})
        )
        record_path.write_text(json.dumps(record, indent=2), encoding="utf-8")
        document["inputs"]["reuse_decisions"] = ["reuse/REUSE-INVALID.json"]
        context = make_context(self.clean, document=document)
        result = checks.check_pf08(context)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["reason_code"], "PF08_REUSE_NOT_VALID")

    def test_self_test_ok(self) -> None:
        report = checks.self_test()
        self.assertTrue(report["ok"])
        self.assertEqual(report["source_scan_findings"], [])


if __name__ == "__main__":
    unittest.main()
