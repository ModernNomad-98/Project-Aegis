"""WP-2B-2: offline grading CLI and self-check extension (prompt 15).

No CLI command calls a provider, opens a live session, runs live Scenario A,
runs the generic corpus, mutates skills/evals, modifies workflows, or
deploys — the verbs do not exist. Self-check verifies the grading-stack
invariants."""

from __future__ import annotations

import contextlib
import io
import json
import os
import tempfile
import unittest

from tools.behavioral_eval_runner.cli import COMMANDS, main, run_self_check
from tools.behavioral_eval_runner.evidence import (
    ArtifactMetadata,
    EvidenceArtifact,
    EvidenceWriter,
)
from tools.behavioral_eval_runner.tests.grading_helpers import (
    load_fixture,
    zero_commit_evidence,
)


def _run_cli(argv: list[str]) -> tuple[int, dict]:
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        code = main(argv)
    text = stdout.getvalue()
    return code, json.loads(text) if text.strip() else {}


class CommandSurfaceTests(unittest.TestCase):
    def test_new_commands_registered(self) -> None:
        for command in (
            "validate-grading-contract",
            "grade-fixture",
            "build-judge-envelope",
            "validate-judge-verdict",
            "mock-calibration",
            "grading-capabilities",
        ):
            self.assertIn(command, COMMANDS)

    def test_no_live_verbs_exist(self) -> None:
        for command in COMMANDS:
            for banned in ("run", "live", "dispatch", "session", "deploy"):
                self.assertNotIn(banned, command)


class ValidateContractCommandTests(unittest.TestCase):
    def test_contract_validates_and_reports_census(self) -> None:
        code, payload = _run_cli(["validate-grading-contract"])
        self.assertEqual(code, 0)
        self.assertEqual(payload["control_count"], 17)
        self.assertEqual(len(payload["contract_sha256"]), 64)
        self.assertEqual(
            payload["control_ids"][0], "SCENARIO_A_CONTROL_A"
        )
        self.assertEqual(payload["control_ids"][-1], "SCENARIO_A_CONTROL_Q")


class GradeFixtureCommandTests(unittest.TestCase):
    def test_grades_recorded_fixture(self) -> None:
        evidence = zero_commit_evidence("good_zero")
        with tempfile.TemporaryDirectory(prefix="wp2b2-cli-") as tmp:
            path = os.path.join(tmp, "evidence.json")
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(evidence, handle)
            code, payload = _run_cli(
                ["grade-fixture", "--grader", "zero_commit", "--evidence", path]
            )
        self.assertEqual(code, 0)
        self.assertEqual(payload["result"]["result_state"], "PASS")
        self.assertEqual(len(payload["result"]["output_sha256"]), 64)

    def test_unknown_grader_rejected(self) -> None:
        code, payload = _run_cli(
            ["grade-fixture", "--grader", "nope", "--evidence", "x.json"]
        )
        self.assertEqual(code, 2)
        self.assertIn("error", payload)


class JudgeEnvelopeCommandTests(unittest.TestCase):
    def test_builds_envelope_without_dispatch(self) -> None:
        with tempfile.TemporaryDirectory(prefix="wp2b2-cli-env-") as tmp:
            root = os.path.join(tmp, "bundle")
            writer = EvidenceWriter(root, run_id="run-cli")
            writer.finalize_input_evidence(
                [EvidenceArtifact("transcript.txt", b"one topic", ArtifactMetadata())]
            )
            code, payload = _run_cli(
                [
                    "build-judge-envelope",
                    "--root",
                    root,
                    "--rubric",
                    "rubric.scenario_a.coherent_topic.v1",
                    "--map",
                    "transcript=transcript.txt",
                ]
            )
        self.assertEqual(code, 0)
        self.assertEqual(payload["envelope"]["envelope_kind"], "aegis_judge_envelope")
        self.assertEqual(len(payload["envelope_sha256"]), 64)
        self.assertEqual(payload["dispatched"], False)


class ValidateVerdictCommandTests(unittest.TestCase):
    def _write_verdict(self, tmp: str, mutate=None) -> str:
        from tools.behavioral_eval_runner.tests.test_judge_scaffold import (
            VerdictSchemaTests,
        )

        payload = VerdictSchemaTests()._verdict_payload()
        if mutate:
            mutate(payload)
        path = os.path.join(tmp, "verdict.json")
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle)
        return path

    def test_valid_mock_verdict(self) -> None:
        with tempfile.TemporaryDirectory(prefix="wp2b2-cli-v-") as tmp:
            code, payload = _run_cli(
                ["validate-judge-verdict", "--file", self._write_verdict(tmp)]
            )
        self.assertEqual(code, 0)
        self.assertTrue(payload["valid"])
        self.assertEqual(payload["verdict"], "PASS")

    def test_malformed_mock_verdict_is_rejected(self) -> None:
        def mutate(p):
            p["confidence"] = 0.9

        with tempfile.TemporaryDirectory(prefix="wp2b2-cli-v-") as tmp:
            code, payload = _run_cli(
                [
                    "validate-judge-verdict",
                    "--file",
                    self._write_verdict(tmp, mutate),
                ]
            )
        self.assertEqual(code, 2)
        self.assertIn("error", payload)


class MockCalibrationCommandTests(unittest.TestCase):
    def _paths(self, tmp: str, observed_name: str, thresholds: bool):
        fixture = load_fixture("calibration_mock.json")
        dataset_path = os.path.join(tmp, "dataset.json")
        with open(dataset_path, "w", encoding="utf-8") as handle:
            json.dump(fixture["dataset"], handle)
        observed_path = os.path.join(tmp, "observed.json")
        with open(observed_path, "w", encoding="utf-8") as handle:
            json.dump(fixture["observed_sets"][observed_name], handle)
        argv = [
            "mock-calibration",
            "--dataset",
            dataset_path,
            "--observed",
            observed_path,
        ]
        if thresholds:
            thresholds_path = os.path.join(tmp, "thresholds.json")
            with open(thresholds_path, "w", encoding="utf-8") as handle:
                json.dump(fixture["mock_thresholds"], handle)
            argv += ["--thresholds", thresholds_path]
        return argv

    def test_metrics_and_under_threshold_rejection(self) -> None:
        with tempfile.TemporaryDirectory(prefix="wp2b2-cli-cal-") as tmp:
            code, payload = _run_cli(self._paths(tmp, "mixed", thresholds=True))
        self.assertEqual(code, 0)
        self.assertEqual(payload["report"]["metrics"]["agreement_rate"], 0.6)
        self.assertEqual(
            payload["threshold_evaluation"]["outcome"], "REJECTED_UNDER_THRESHOLD"
        )
        self.assertFalse(payload["threshold_evaluation"]["baseline_eligible"])

    def test_missing_thresholds_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="wp2b2-cli-cal-") as tmp:
            code, payload = _run_cli(self._paths(tmp, "perfect", thresholds=False))
        self.assertEqual(code, 0)
        self.assertEqual(
            payload["threshold_evaluation"]["outcome"], "REJECTED_NO_THRESHOLDS"
        )
        self.assertFalse(payload["threshold_evaluation"]["baseline_eligible"])


class GradingCapabilitiesCommandTests(unittest.TestCase):
    def test_truthful_grading_capabilities(self) -> None:
        code, payload = _run_cli(["grading-capabilities"])
        self.assertEqual(code, 0)
        self.assertEqual(payload["authorization"]["authorization_id"], "BER-DEC-007")
        self.assertEqual(payload["judge_dispatch"], "DISABLED")
        self.assertEqual(payload["actual_judge_provider_calls"], 0)
        self.assertIn("OD-1 OPEN", payload["measured_calibration"])
        self.assertEqual(payload["live_scenario_a"], "NOT_AUTHORIZED")
        self.assertEqual(payload["generic_corpus"], "NOT_AUTHORIZED")
        self.assertEqual(
            payload["coherent_topic_rule"],
            "ONE COHERENT DISCOVERY TOPIC PER TURN.\n"
            "Related supporting details within that topic are allowed.",
        )


class SelfCheckExtensionTests(unittest.TestCase):
    def test_self_check_passes_with_grading_checks(self) -> None:
        result = run_self_check()
        self.assertEqual(result["self_check"], "PASS")
        names = {check["name"] for check in result["checks"]}
        for required in (
            "grading_enum_sets_closed",
            "grading_schemas_match_code_enums",
            "grading_contract_complete",
            "grading_fixture_reproducible",
            "judge_provider_absent_or_denied",
            "judge_envelope_security_invariants",
            "mock_calibration_threshold_behavior",
            "no_forbidden_source_patterns",
        ):
            self.assertIn(required, names)


if __name__ == "__main__":
    unittest.main()
