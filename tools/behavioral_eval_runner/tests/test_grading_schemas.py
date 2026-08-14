"""WP-2B-2: schema/code agreement for the grading-stack schemas.

The JSON Schemas are the portable specification; the dataclass validators
are the runtime contract. These tests pin their agreement: enum sets match
the closed code enums exactly, additionalProperties is false everywhere,
and record serializations carry exactly the schema's property keys."""

from __future__ import annotations

import unittest

from tools.behavioral_eval_runner import GRADING_SCHEMA_VERSION
from tools.behavioral_eval_runner.cli import load_schema
from tools.behavioral_eval_runner.graders.contract import (
    ComponentStatus,
    ControlDisposition,
    load_contract,
)
from tools.behavioral_eval_runner.graders.records import (
    GraderResultState,
    GradingReasonCode,
)
from tools.behavioral_eval_runner.judge.calibration import (
    CalibrationLabel,
    CalibrationProvenance,
    ObservedOutcome,
    SplitFold,
)
from tools.behavioral_eval_runner.judge.verdict import (
    OFFENDING_SPAN_MAX_CHARS,
    FailureMode,
    JudgeVerdictReason,
    JudgeVerdictState,
)
from tools.behavioral_eval_runner.enums import RiskClass

NEW_SCHEMAS = (
    "grader-result.schema.json",
    "judge-request.schema.json",
    "judge-verdict.schema.json",
    "calibration-dataset.schema.json",
    "calibration-report.schema.json",
    "scenario-a-grading-contract.schema.json",
    "scenario-a-grading-plan.schema.json",
)


class SchemaHygieneTests(unittest.TestCase):
    def test_all_schemas_load_and_are_closed(self) -> None:
        for name in NEW_SCHEMAS:
            with self.subTest(schema=name):
                schema = load_schema(name)
                self.assertEqual(schema["type"], "object")
                self.assertFalse(schema["additionalProperties"])
                self.assertIn(GRADING_SCHEMA_VERSION, schema["$id"])
                self.assertEqual(
                    schema["properties"]["schema_version"]["const"]
                    if "schema_version" in schema["properties"]
                    else GRADING_SCHEMA_VERSION,
                    GRADING_SCHEMA_VERSION,
                )


class EnumAgreementTests(unittest.TestCase):
    def test_grader_result_enums_match_code(self) -> None:
        schema = load_schema("grader-result.schema.json")
        self.assertEqual(
            sorted(schema["properties"]["result_state"]["enum"]),
            sorted(GraderResultState.values()),
        )
        reason_enum = schema["properties"]["reason_code"]["anyOf"][1]["enum"]
        self.assertEqual(sorted(reason_enum), sorted(GradingReasonCode.values()))

    def test_judge_verdict_enums_match_code(self) -> None:
        schema = load_schema("judge-verdict.schema.json")
        self.assertEqual(
            sorted(schema["properties"]["verdict"]["enum"]),
            sorted(JudgeVerdictState.values()),
        )
        failure_enum = schema["properties"]["failure_mode"]["anyOf"][1]["enum"]
        self.assertEqual(sorted(failure_enum), sorted(FailureMode.values()))
        self.assertEqual(
            sorted(schema["properties"]["reason_code"]["enum"]),
            sorted(JudgeVerdictReason.values()),
        )
        self.assertEqual(
            schema["properties"]["offending_span"]["anyOf"][1]["maxLength"],
            OFFENDING_SPAN_MAX_CHARS,
        )

    def test_calibration_dataset_enums_match_code(self) -> None:
        schema = load_schema("calibration-dataset.schema.json")
        self.assertEqual(
            sorted(schema["properties"]["provenance"]["enum"]),
            sorted(CalibrationProvenance.values()),
        )
        entry = schema["properties"]["entries"]["items"]
        self.assertFalse(entry["additionalProperties"])
        self.assertEqual(
            sorted(entry["properties"]["risk_class"]["enum"]),
            sorted(RiskClass.values()),
        )
        self.assertEqual(
            sorted(entry["properties"]["expected_label"]["enum"]),
            sorted(CalibrationLabel.values()),
        )
        self.assertEqual(
            sorted(entry["properties"]["split"]["enum"]),
            sorted(SplitFold.values()),
        )

    def test_calibration_report_observed_counts_match_code(self) -> None:
        schema = load_schema("calibration-report.schema.json")
        counts = schema["definitions"]["observed_counts"]
        self.assertEqual(
            sorted(counts["required"]), sorted(ObservedOutcome.values())
        )

    def test_contract_schema_enums_match_code(self) -> None:
        schema = load_schema("scenario-a-grading-contract.schema.json")
        control = schema["properties"]["controls"]["items"]
        self.assertEqual(
            sorted(control["properties"]["classification"]["enum"]),
            sorted(ControlDisposition.values()),
        )
        self.assertEqual(
            sorted(control["properties"]["deterministic_status"]["enum"]),
            sorted(ComponentStatus.values()),
        )


class InstanceKeyAgreementTests(unittest.TestCase):
    def test_contract_instance_matches_schema_keys(self) -> None:
        schema = load_schema("scenario-a-grading-contract.schema.json")
        payload = load_contract().to_dict()
        self.assertEqual(set(payload), set(schema["properties"]))
        control_props = set(
            schema["properties"]["controls"]["items"]["properties"]
        )
        for control in payload["controls"]:
            self.assertEqual(set(control), control_props)
        self.assertEqual(len(payload["controls"]), 17)


if __name__ == "__main__":
    unittest.main()
