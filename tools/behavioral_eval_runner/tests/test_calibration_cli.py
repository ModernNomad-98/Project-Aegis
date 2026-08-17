"""WP-2B-3 offline calibration CLI surfaces (task section 20).

Repository-safe output only: the commands emit hashes, counts, and statuses —
never item transcripts, candidate labels, rationales, or credentials. No live
verb exists.
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import tempfile
import unittest

from tools.behavioral_eval_runner.cli import COMMANDS, main, run_self_check
from tools.behavioral_eval_runner.judge import calibration_dataset as cd
from tools.behavioral_eval_runner.judge import calibration_gates as cg
from tools.behavioral_eval_runner.tests.test_calibration_dataset import (
    build_conforming_dataset,
)


def _run_cli(argv: list[str]) -> tuple[int, dict, str]:
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        code = main(argv)
    text = stdout.getvalue()
    return code, (json.loads(text) if text.strip() else {}), text


class CommandSurfaceTests(unittest.TestCase):
    def test_wp2b3_commands_registered(self) -> None:
        self.assertIn("validate-calibration-dataset", COMMANDS)
        self.assertIn("calibration-status", COMMANDS)

    def test_still_no_live_verbs(self) -> None:
        for command in COMMANDS:
            for banned in ("run", "live", "dispatch", "session", "deploy"):
                self.assertNotIn(banned, command)


class ValidateCalibrationDatasetTests(unittest.TestCase):
    def test_conforming_dataset_reports_repository_safe_metadata(self) -> None:
        dataset = build_conforming_dataset()
        with tempfile.TemporaryDirectory(prefix="wp2b3-cli-") as tmp:
            path = os.path.join(tmp, "candidate-dataset.json")
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(dataset.to_dict(), handle)
            code, payload, text = _run_cli(
                ["validate-calibration-dataset", "--dataset", path]
            )
        self.assertEqual(code, 0)
        self.assertEqual(payload["total_items"], 160)
        self.assertEqual(payload["owner_label_status"], "PENDING")
        self.assertEqual(payload["dataset_sha256"], dataset.dataset_sha256())
        self.assertEqual(payload["split_map_sha256"],
                         cd.split_map_sha256(dataset))
        self.assertEqual(payload["composition"], "PASS")
        self.assertEqual(payload["holdout_critical_expected_fail"], 40)
        self.assertEqual(payload["holdout_adversarial_total"], 40)
        self.assertEqual(payload["critical_adversarial_overlap"], 10)
        # Repository-safe: no transcript, rationale, or per-item label output.
        first = dataset.items[0]
        self.assertNotIn(first.transcript, text)
        self.assertNotIn(first.candidate_rationale, text)
        self.assertNotIn("candidate_expected_label", text)

    def test_nonconforming_dataset_fails_with_nonzero_exit(self) -> None:
        dataset = build_conforming_dataset()
        payload = dataset.to_dict()
        payload["items"] = payload["items"][:-1]  # 159 items
        with tempfile.TemporaryDirectory(prefix="wp2b3-cli-") as tmp:
            path = os.path.join(tmp, "broken.json")
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(payload, handle)
            code, _payload, _text = _run_cli(
                ["validate-calibration-dataset", "--dataset", path]
            )
        self.assertNotEqual(code, 0)


class CalibrationStatusTests(unittest.TestCase):
    def test_default_status_is_pending_and_blocked(self) -> None:
        code, payload, text = _run_cli(["calibration-status"])
        self.assertEqual(code, 0)
        self.assertEqual(payload["owner_label_approval"], "PENDING")
        self.assertIs(payload["provider_dispatch_allowed"], False)
        self.assertEqual(payload["provider_calls_made_by_this_command"], 0)
        self.assertEqual(payload["od1_status"], "OPEN")
        self.assertEqual(payload["wp2b4_status"], "BLOCKED")

    def test_status_with_approval_artifact_still_reports_gates(self) -> None:
        dataset = build_conforming_dataset()
        approval = cg.OwnerLabelApproval.pending(cg.DatasetIdentity(
            dataset_id=dataset.dataset_id,
            dataset_version=dataset.version,
            dataset_sha256=dataset.dataset_sha256(),
            split_map_sha256=cd.split_map_sha256(dataset),
            labeling_guide_sha256="c" * 64,
        ))
        with tempfile.TemporaryDirectory(prefix="wp2b3-cli-") as tmp:
            path = os.path.join(tmp, "approval.json")
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(approval.to_dict(), handle)
            code, payload, _text = _run_cli(
                ["calibration-status", "--approval", path]
            )
        self.assertEqual(code, 0)
        self.assertEqual(payload["owner_label_approval"], "PENDING")
        self.assertIs(payload["provider_dispatch_allowed"], False)


class SelfCheckExtensionTests(unittest.TestCase):
    def test_self_check_covers_wp2b3_gates_and_passes(self) -> None:
        report = run_self_check()
        names = {check["name"] for check in report["checks"]}
        for required in (
            "calibration_gates_fail_closed",
            "calibration_request_settings_closed",
            "calibration_caps_and_pricing_exact",
            "calibration_dataset_contract_enforced",
            "calibration_provider_fragments_allowlisted",
            "calibration_schemas_match_code_enums",
        ):
            self.assertIn(required, names)
        self.assertEqual(report["self_check"], "PASS")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
