"""Synthetic-only negative checks for the opt-in complete-bundle policy."""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.behavioral_eval_runner import RUNNER_VERSION, SCHEMA_VERSION
from tools.behavioral_eval_runner.canonical import canonical_bytes, sha256_hex
from tools.behavioral_eval_runner.enums import RedactionState, Sensitivity
from tools.behavioral_eval_runner.errors import EvidenceError, EvidenceIntegrityError
from tools.behavioral_eval_runner.evidence import (
    ArtifactMetadata, EvidenceArtifact, EvidenceWriter, FINAL_MANIFEST_NAME,
    FINAL_REPORT_NAME, INPUT_MANIFEST_NAME, MARKER_NAME, verify_final_bundle,
    verify_local_bundle,
)
from tools.behavioral_eval_runner.evidence_policy import (
    ClassifiedArtifact, ClassificationDecision, OfflinePolicyWriter,
    STAGE_A_POLICY, STAGE_B_POLICY, verify_policy_bundle,
    verify_policy_input,
)
from tools.behavioral_eval_runner import evidence_policy as policy_module

FIRST = "2030-01-31T23:00:00Z"
LATER = "2030-02-01T01:00:00Z"
DEADLINE = "2030-03-02T23:00:00Z"
RUN = "synthetic-policy-run"


def decision(name: str = "input") -> ClassificationDecision:
    return ClassificationDecision(
        Sensitivity.INTERNAL, RedactionState.UNREDACTED_INTERNAL_ONLY,
        "BER-DEC-011@v1", f"synthetic-review:{name}",
    )


def input_artifact() -> ClassifiedArtifact:
    return ClassifiedArtifact("inputs/one.txt", b"synthetic input", decision())


class PolicyCase(unittest.TestCase):
    def setUp(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = temp.name
        self.writer = OfflinePolicyWriter(self.root, RUN)

    def report(self, sha: str) -> dict:
        return {
            "report_kind": "behavioral_eval_run_report",
            "schema_version": SCHEMA_VERSION,
            "runner_version": RUNNER_VERSION,
            "run_id": RUN,
            "run_evidence_binding": {"input_evidence_manifest_sha256": sha},
            "attempts": [], "aggregates": [],
        }

    def stage_a(self) -> str:
        with patch("tools.behavioral_eval_runner.evidence_policy._now", return_value=FIRST), \
             patch("tools.behavioral_eval_runner.evidence._utc_now_iso", return_value=FIRST):
            return self.writer.finalize_input([input_artifact()]).input_evidence_manifest_sha256

    def complete(self) -> None:
        sha = self.stage_a()
        with patch("tools.behavioral_eval_runner.evidence_policy._now", return_value=LATER), \
             patch("tools.behavioral_eval_runner.evidence._utc_now_iso", return_value=LATER):
            self.writer.finalize_final(
                self.report(sha),
                [ClassifiedArtifact("outputs/one.txt", b"synthetic output", decision("output"))],
                decision("report"), "OFFLINE_DEMONSTRATION",
            )

    def read(self, name: str) -> dict:
        with open(os.path.join(self.root, *name.split("/")), encoding="utf-8") as handle:
            return json.load(handle)

    def write(self, name: str, value: dict) -> str:
        content = canonical_bytes(value)
        with open(os.path.join(self.root, *name.split("/")), "wb") as handle:
            handle.write(content)
        return sha256_hex(content)

    def verify_at(self, instant: str) -> dict[str, str]:
        with patch("tools.behavioral_eval_runner.evidence_policy._now", return_value=instant):
            return verify_policy_bundle(self.root)


class TestPolicy(PolicyCase):
    def test_stage_a_claim_uses_artifact_snapshot(self) -> None:
        artifacts = [input_artifact()]
        claim = policy_module._claim_policy_receipt
        def mutate_after_claim(root: str, path: str, content: bytes) -> None:
            claim(root, path, content)
            if path == STAGE_A_POLICY:
                artifacts[0] = ClassifiedArtifact("../invalid", b"changed", decision())
        with patch.object(policy_module, "_claim_policy_receipt", side_effect=mutate_after_claim), \
             patch("tools.behavioral_eval_runner.evidence_policy._now", return_value=FIRST), \
             patch("tools.behavioral_eval_runner.evidence._utc_now_iso", return_value=FIRST):
            self.writer.finalize_input(artifacts)
        self.assertEqual(Path(self.root, "inputs", "one.txt").read_bytes(), b"synthetic input")
        self.assertEqual(verify_policy_input(self.root)["bundle_review_at"], DEADLINE)

    def test_stage_a_path_conflicts_fail_before_claim_and_allow_retry(self) -> None:
        invalid_paths = (
            ("policy",),
            ("x", "x/y"),
            ("policy/stage-a.json/x",),
            ("input_evidence_manifest.json/x",),
        )
        for paths in invalid_paths:
            with self.subTest(paths=paths):
                artifacts = [ClassifiedArtifact(path, b"synthetic", decision()) for path in paths]
                with self.assertRaisesRegex(EvidenceError, "paths conflict"):
                    self.writer.finalize_input(artifacts)
                self.assertEqual(os.listdir(self.root), [])
        self.stage_a()
        self.assertEqual(verify_policy_input(self.root)["bundle_review_at"], DEADLINE)

    def test_invalid_report_preserves_stage_a_and_allows_corrected_retry(self) -> None:
        sha = self.stage_a()
        def tree() -> dict[str, bytes]:
            return {
                os.path.relpath(os.path.join(folder, name), self.root):
                Path(folder, name).read_bytes()
                for folder, _, names in os.walk(self.root) for name in names
            }
        before = tree()
        invalid = (
            ({**self.report(sha), "run_id": "another-run"}, "run_id"),
            ({**self.report(sha), "run_evidence_binding": {
                "input_evidence_manifest_sha256": "0" * 64}}, "stage A binding"),
            ({**self.report(sha), "run_evidence_binding": {
                "input_evidence_manifest_sha256": sha,
                "final_report_sha256": "0" * 64}}, "final_report_sha256"),
        )
        for report, reason in invalid:
            with self.subTest(reason=reason), self.assertRaisesRegex(EvidenceError, reason):
                self.writer.finalize_final(report, [], decision("report"), "INVALID")
            self.assertEqual(tree(), before)
        with patch("tools.behavioral_eval_runner.evidence_policy._now", return_value=LATER), \
             patch("tools.behavioral_eval_runner.evidence._utc_now_iso", return_value=LATER):
            self.writer.finalize_final(self.report(sha), [], decision("report"), "CORRECTED")
        self.assertEqual(self.read(MARKER_NAME)["final_status"], "CORRECTED")
        self.assertTrue(self.verify_at(LATER))

    def test_stage_b_path_conflict_preserves_stage_a_and_allows_retry(self) -> None:
        sha = self.stage_a()
        before = {
            os.path.relpath(os.path.join(folder, name), self.root): Path(folder, name).read_bytes()
            for folder, _, names in os.walk(self.root) for name in names
        }
        with self.assertRaisesRegex(EvidenceError, "paths conflict"):
            self.writer.finalize_final(
                self.report(sha),
                [ClassifiedArtifact("inputs", b"collision", decision("output"))],
                decision("report"), "INVALID",
            )
        after = {
            os.path.relpath(os.path.join(folder, name), self.root): Path(folder, name).read_bytes()
            for folder, _, names in os.walk(self.root) for name in names
        }
        self.assertEqual(after, before)
        with patch("tools.behavioral_eval_runner.evidence_policy._now", return_value=LATER), \
             patch("tools.behavioral_eval_runner.evidence._utc_now_iso", return_value=LATER):
            self.writer.finalize_final(self.report(sha), [], decision("report"), "CORRECTED")
        self.assertTrue(self.verify_at(LATER))

    def test_stage_b_report_version_and_status_fail_before_claim_then_retry(self) -> None:
        sha = self.stage_a()
        before = {
            os.path.relpath(os.path.join(folder, name), self.root): Path(folder, name).read_bytes()
            for folder, _, names in os.walk(self.root) for name in names
        }
        invalid_reports = (
            {**self.report(sha), "schema_version": "unsupported"},
            {key: value for key, value in self.report(sha).items() if key != "runner_version"},
            {**self.report(sha), "attempts": [{"schema_version": "unsupported"}]},
        )
        for report in invalid_reports:
            with self.subTest(report=report), self.assertRaises(EvidenceError):
                self.writer.finalize_final(report, [], decision("report"), "INVALID")
        for status in ({}, float("nan"), ""):
            with self.subTest(status=status), self.assertRaises(EvidenceError):
                self.writer.finalize_final(self.report(sha), [], decision("report"), status)
        after = {
            os.path.relpath(os.path.join(folder, name), self.root): Path(folder, name).read_bytes()
            for folder, _, names in os.walk(self.root) for name in names
        }
        self.assertEqual(after, before)
        with patch("tools.behavioral_eval_runner.evidence_policy._now", return_value=LATER), \
             patch("tools.behavioral_eval_runner.evidence._utc_now_iso", return_value=LATER):
            self.writer.finalize_final(self.report(sha), [], decision("report"), "CORRECTED")
        self.assertTrue(self.verify_at(LATER))

    def test_stage_b_claim_uses_artifact_snapshot(self) -> None:
        sha = self.stage_a()
        artifacts = [ClassifiedArtifact("outputs/one.txt", b"original", decision("output"))]
        claim = policy_module._claim_policy_receipt
        def mutate_after_claim(root: str, path: str, content: bytes) -> None:
            claim(root, path, content)
            if path == STAGE_B_POLICY:
                artifacts[0] = ClassifiedArtifact("../invalid", b"changed", decision("output"))
        with patch.object(policy_module, "_claim_policy_receipt", side_effect=mutate_after_claim), \
             patch("tools.behavioral_eval_runner.evidence_policy._now", return_value=LATER), \
             patch("tools.behavioral_eval_runner.evidence._utc_now_iso", return_value=LATER):
            self.writer.finalize_final(self.report(sha), artifacts, decision("report"), "SNAPSHOT")
        self.assertEqual(Path(self.root, "outputs", "one.txt").read_bytes(), b"original")
        self.assertTrue(self.verify_at(LATER))

    def test_report_mutation_during_receipt_claim_uses_validated_snapshot(self) -> None:
        sha = self.stage_a()
        report = self.report(sha)
        claim = policy_module._claim_policy_receipt
        def mutate_after_claim(root: str, path: str, content: bytes) -> None:
            claim(root, path, content)
            if path == STAGE_B_POLICY:
                report["run_id"] = "another-run"
                report["run_evidence_binding"]["input_evidence_manifest_sha256"] = "0" * 64
        with patch.object(policy_module, "_claim_policy_receipt", side_effect=mutate_after_claim), \
             patch("tools.behavioral_eval_runner.evidence_policy._now", return_value=LATER), \
             patch("tools.behavioral_eval_runner.evidence._utc_now_iso", return_value=LATER):
            self.writer.finalize_final(report, [], decision("report"), "SNAPSHOT")
        self.assertEqual(self.read(FINAL_REPORT_NAME)["run_id"], RUN)
        self.assertEqual(
            self.read(FINAL_REPORT_NAME)["run_evidence_binding"]["input_evidence_manifest_sha256"],
            sha,
        )
        self.assertTrue(self.verify_at(LATER))

    def test_report_snapshot_is_validated_instead_of_live_mapping_getters(self) -> None:
        sha = self.stage_a()
        class MisleadingReport(dict):
            def get(self, key, default=None):
                if key == "run_id":
                    return RUN
                if key == "run_evidence_binding":
                    return {"input_evidence_manifest_sha256": sha}
                return super().get(key, default)
        report = MisleadingReport(self.report(sha))
        report["run_id"] = "another-run"
        with self.assertRaisesRegex(EvidenceError, "run_id"):
            self.writer.finalize_final(report, [], decision("report"), "INVALID")
        self.assertFalse(os.path.exists(os.path.join(self.root, *STAGE_B_POLICY.split("/"))))

    def test_stage_b_policy_lookalike_cannot_pass_legacy_path(self) -> None:
        legacy = EvidenceWriter(self.root, RUN)
        sha = legacy.finalize_input_evidence([
            EvidenceArtifact("inputs/one.txt", b"synthetic input")
        ]).input_evidence_manifest_sha256
        with self.assertRaisesRegex(EvidenceError, "policy Stage B receipt"):
            legacy.finalize_final_bundle(
                self.report(sha), [EvidenceArtifact(STAGE_B_POLICY, b"{}")],
                sha, "OFFLINE_DEMONSTRATION",
            )
        self.assertFalse(os.path.exists(os.path.join(self.root, FINAL_REPORT_NAME)))

        # Simulate a pre-existing or externally forged bundle: keep the legacy
        # hashes valid while placing a policy-looking receipt in Stage B only.
        legacy.finalize_final_bundle(
            self.report(sha), [EvidenceArtifact("outputs/one.txt", b"{}")],
            sha, "OFFLINE_DEMONSTRATION",
        )
        source = os.path.join(self.root, "outputs", "one.txt")
        target = os.path.join(self.root, *STAGE_B_POLICY.split("/"))
        os.makedirs(os.path.dirname(target), exist_ok=True)
        os.replace(source, target)
        manifest = self.read(FINAL_MANIFEST_NAME)
        next(entry for entry in manifest["artifacts"]
             if entry["path"] == "outputs/one.txt")["path"] = STAGE_B_POLICY
        manifest_sha = self.write(FINAL_MANIFEST_NAME, manifest)
        marker = self.read(MARKER_NAME)
        marker["final_evidence_manifest_sha256"] = manifest_sha
        self.write(MARKER_NAME, marker)
        self.assertTrue(verify_final_bundle(self.root))
        with self.assertRaises(EvidenceIntegrityError):
            verify_local_bundle(self.root)
        os.remove(target)
        with self.assertRaises(EvidenceIntegrityError):
            verify_local_bundle(self.root)

    def test_prewritten_flag_cannot_replace_policy_stage_a_with_defaults(self) -> None:
        self.stage_a()
        manifest_path = os.path.join(self.root, INPUT_MANIFEST_NAME)
        with open(manifest_path, "rb") as handle:
            before = handle.read()
        receipt = canonical_bytes(self.read(STAGE_A_POLICY))
        with self.assertRaisesRegex(EvidenceError, "policy-bound Stage A"):
            self.writer.writer.finalize_input_evidence(
                [EvidenceArtifact(STAGE_A_POLICY, receipt)],
                _prewritten=frozenset({STAGE_A_POLICY}),
            )
        with open(manifest_path, "rb") as handle:
            self.assertEqual(handle.read(), before)
        self.assertEqual(verify_policy_input(self.root)["bundle_review_at"], DEADLINE)

    def test_boolean_policy_flag_cannot_finalize_with_default_report_metadata(self) -> None:
        sha = self.stage_a()
        stage_b_path = os.path.join(self.root, *STAGE_B_POLICY.split("/"))
        with open(stage_b_path, "wb") as handle:
            handle.write(b"{}")  # an interrupted, untrusted receipt claim
        with self.assertRaises(EvidenceError):
            self.writer.writer.finalize_final_bundle(
                self.report(sha), [], sha, "OFFLINE_DEMONSTRATION",
                report_metadata=ArtifactMetadata(),
                _prewritten=frozenset({STAGE_B_POLICY}),
                _policy_bound=True,
            )
        self.assertFalse(os.path.exists(os.path.join(self.root, FINAL_REPORT_NAME)))
        with open(stage_b_path, "rb") as handle:
            self.assertEqual(handle.read(), b"{}")

    def test_legacy_writer_cannot_downgrade_policy_stage_a(self) -> None:
        sha = self.stage_a()
        with self.assertRaisesRegex(EvidenceError, "policy-bound Stage A"):
            self.writer.writer.finalize_final_bundle(
                self.report(sha), [], sha, "OFFLINE_DEMONSTRATION",
            )
        self.assertFalse(os.path.exists(os.path.join(self.root, FINAL_REPORT_NAME)))
        os.remove(os.path.join(self.root, *STAGE_A_POLICY.split("/")))
        with self.assertRaisesRegex(EvidenceError, "policy-bound Stage A"):
            self.writer.writer.finalize_final_bundle(
                self.report(sha), [], sha, "OFFLINE_DEMONSTRATION",
            )
        with self.assertRaises(EvidenceIntegrityError):
            verify_local_bundle(self.root)
        self.assertFalse(os.path.exists(os.path.join(self.root, FINAL_REPORT_NAME)))

    def test_local_verifier_keeps_policy_semantics_and_explicit_requirement(self) -> None:
        self.complete()
        with patch("tools.behavioral_eval_runner.evidence_policy._now", return_value=LATER):
            self.assertEqual(verify_local_bundle(self.root)["bundle_review_at"], DEADLINE)
        self.assertTrue(verify_final_bundle(self.root))
        with patch("tools.behavioral_eval_runner.evidence_policy._now", return_value=DEADLINE):
            with self.assertRaises(EvidenceIntegrityError):
                verify_local_bundle(self.root)
        os.remove(os.path.join(self.root, *STAGE_A_POLICY.split("/")))
        with self.assertRaises(EvidenceIntegrityError):
            verify_local_bundle(self.root, require_policy=True)

    def test_backslash_paths_use_normalized_receipt_identity(self) -> None:
        with patch("tools.behavioral_eval_runner.evidence_policy._now", return_value=FIRST), \
             patch("tools.behavioral_eval_runner.evidence._utc_now_iso", return_value=FIRST):
            sha = self.writer.finalize_input([
                ClassifiedArtifact("inputs\\one.txt", b"synthetic input", decision())
            ]).input_evidence_manifest_sha256
        self.assertTrue(os.path.exists(os.path.join(self.root, "inputs", "one.txt")))
        with patch("tools.behavioral_eval_runner.evidence_policy._now", return_value=LATER), \
             patch("tools.behavioral_eval_runner.evidence._utc_now_iso", return_value=LATER):
            self.writer.finalize_final(self.report(sha), [
                ClassifiedArtifact("outputs\\one.txt", b"synthetic output", decision("output"))
            ], decision("report"), "OFFLINE_DEMONSTRATION")
        self.assertIn("outputs/one.txt", {a["path"] for a in self.read(FINAL_MANIFEST_NAME)["artifacts"]})

    def test_control_name_case_aliases_fail_before_first_write(self) -> None:
        for name in (INPUT_MANIFEST_NAME, FINAL_MANIFEST_NAME, MARKER_NAME):
            with self.subTest(name=name), self.assertRaises(EvidenceError):
                self.writer.finalize_input([ClassifiedArtifact(name.upper(), b"alias", decision())])
            self.assertEqual(os.listdir(self.root), [])

    def test_complete_deadline_and_detached_marker_binding(self) -> None:
        self.complete()
        result = self.verify_at("2030-03-02T22:59:59Z")
        self.assertEqual(result["first_created_at"], FIRST)
        self.assertEqual(result["bundle_review_at"], DEADLINE)
        self.assertIn("finalization_marker_sha256", result)
        manifest = self.read(FINAL_MANIFEST_NAME)
        self.assertIn(STAGE_B_POLICY, {entry["path"] for entry in manifest["artifacts"]})
        self.assertNotIn(MARKER_NAME, {entry["path"] for entry in manifest["artifacts"]})
        report = next(entry for entry in manifest["artifacts"] if entry["path"] == FINAL_REPORT_NAME)
        self.assertEqual(report["created_at"], LATER)
        self.assertNotEqual(report["expiration_at"], DEADLINE)  # legacy field stays per-artifact
        self.assertEqual(self.read(STAGE_B_POLICY)["bundle_review_at"], DEADLINE)

    def test_writer_normalizes_timezones_at_month_boundary(self) -> None:
        with patch("tools.behavioral_eval_runner.evidence_policy._now",
                   return_value="2030-02-01T04:00:00+05:00"), \
             patch("tools.behavioral_eval_runner.evidence._utc_now_iso", return_value=FIRST):
            self.writer.finalize_input([input_artifact()])
        self.assertEqual(verify_policy_input(self.root)["first_created_at"], FIRST)
        self.assertEqual(verify_policy_input(self.root)["bundle_review_at"], DEADLINE)

    def test_expired_bundle_is_preserved_and_refused(self) -> None:
        self.complete()
        for as_of in (DEADLINE, "2030-03-03T00:00:00+01:00"):
            with self.subTest(as_of=as_of), self.assertRaises(EvidenceIntegrityError):
                self.verify_at(as_of)
        self.assertTrue(os.path.exists(os.path.join(self.root, MARKER_NAME)))

    def test_empty_or_unclassified_stage_a_rejected_before_write(self) -> None:
        for items in ([], [EvidenceArtifact("x", b"raw")],
                      [ClassifiedArtifact("x", b"raw", None)]):
            with self.subTest(items=items), self.assertRaises(EvidenceError):
                self.writer.finalize_input(items)
        self.assertFalse(os.path.exists(os.path.join(self.root, INPUT_MANIFEST_NAME)))

    def test_receipt_only_stage_a_is_not_a_valid_input(self) -> None:
        self.stage_a()
        receipt = self.read(STAGE_A_POLICY)
        receipt["classification_decisions"] = []
        receipt_sha = self.write(STAGE_A_POLICY, receipt)
        manifest = self.read(INPUT_MANIFEST_NAME)
        manifest["artifacts"] = [
            entry for entry in manifest["artifacts"] if entry["path"] == STAGE_A_POLICY
        ]
        manifest["artifacts"][0]["sha256"] = receipt_sha
        manifest["artifacts"][0]["bytes"] = len(canonical_bytes(receipt))
        self.write(INPUT_MANIFEST_NAME, manifest)
        with self.assertRaises(EvidenceIntegrityError):
            verify_policy_input(self.root)

    def test_second_writer_cannot_reset_first_clock_or_overwrite(self) -> None:
        self.stage_a()
        before = self.read(STAGE_A_POLICY)
        with patch("tools.behavioral_eval_runner.evidence_policy._now", return_value=LATER):
            with self.assertRaises(EvidenceError):
                OfflinePolicyWriter(self.root, RUN).finalize_input([input_artifact()])
        self.assertEqual(self.read(STAGE_A_POLICY), before)
        self.assertEqual(verify_policy_input(self.root)["bundle_review_at"], DEADLINE)

    def test_interleaved_stage_a_claim_has_one_winner(self) -> None:
        winner = OfflinePolicyWriter(self.root, RUN)
        original = policy_module._claim_policy_receipt
        entered = False
        def interleave(root: str, path: str, content: bytes) -> None:
            nonlocal entered
            if path == STAGE_A_POLICY and not entered:
                entered = True
                with patch.object(policy_module, "_claim_policy_receipt", original):
                    winner.finalize_input([input_artifact()])
            original(root, path, content)
        with patch.object(policy_module, "_claim_policy_receipt", side_effect=interleave), \
             patch("tools.behavioral_eval_runner.evidence_policy._now", side_effect=[FIRST, LATER]), \
             patch("tools.behavioral_eval_runner.evidence._utc_now_iso", return_value=LATER):
            with self.assertRaises(EvidenceError):
                self.writer.finalize_input([input_artifact()])
        self.assertEqual(verify_policy_input(self.root)["first_created_at"], LATER)

    def test_interleaved_stage_b_claim_has_one_winner(self) -> None:
        sha = self.stage_a()
        winner = OfflinePolicyWriter(self.root, RUN)
        original = policy_module._claim_policy_receipt
        entered = False
        def interleave(root: str, path: str, content: bytes) -> None:
            nonlocal entered
            if path == STAGE_B_POLICY and not entered:
                entered = True
                with patch.object(policy_module, "_claim_policy_receipt", original):
                    winner.finalize_final(self.report(sha), [], decision("report"), "WINNER")
            original(root, path, content)
        with patch.object(policy_module, "_claim_policy_receipt", side_effect=interleave), \
             patch("tools.behavioral_eval_runner.evidence_policy._now", return_value=LATER), \
             patch("tools.behavioral_eval_runner.evidence._utc_now_iso", return_value=LATER):
            with self.assertRaises(EvidenceError):
                self.writer.finalize_final(self.report(sha), [], decision("report"), "LOSER")
        self.assertEqual(self.read(MARKER_NAME)["final_status"], "WINNER")
        self.assertTrue(self.verify_at(LATER))

    def test_windows_case_alias_cannot_overwrite_stage_a(self) -> None:
        sha = self.stage_a()
        target = os.path.join(self.root, "inputs", "one.txt")
        with open(target, "rb") as handle:
            original = handle.read()
        with self.assertRaises(EvidenceError):
            self.writer.finalize_final(
                self.report(sha),
                [ClassifiedArtifact("INPUTS/ONE.TXT", b"replacement", decision("output"))],
                decision("report"), "OFFLINE_DEMONSTRATION",
            )
        with open(target, "rb") as handle:
            self.assertEqual(handle.read(), original)
        self.assertFalse(os.path.exists(os.path.join(self.root, FINAL_REPORT_NAME)))

    def test_receipt_swap_after_stage_a_base_verification_fails(self) -> None:
        self.stage_a()
        original_load = policy_module._load_json_bytes
        def swap(root: str, name: str):
            if name == STAGE_A_POLICY:
                receipt = self.read(STAGE_A_POLICY)
                receipt["classification_decisions"][0]["decision_ref"] = "synthetic-review:substituted"
                self.write(STAGE_A_POLICY, receipt)
            return original_load(root, name)
        with patch.object(policy_module, "_load_json_bytes", side_effect=swap):
            with self.assertRaises(EvidenceIntegrityError):
                verify_policy_input(self.root)

    def test_receipt_swap_after_stage_b_base_verification_fails(self) -> None:
        self.complete()
        original_load = policy_module._load_json_bytes
        def swap(root: str, name: str):
            if name == STAGE_B_POLICY:
                receipt = self.read(STAGE_B_POLICY)
                receipt["classification_decisions"][0]["decision_ref"] = "synthetic-review:substituted"
                self.write(STAGE_B_POLICY, receipt)
            return original_load(root, name)
        with patch.object(policy_module, "_load_json_bytes", side_effect=swap):
            with self.assertRaises(EvidenceIntegrityError):
                self.verify_at(LATER)

    def test_report_swap_after_base_verification_fails(self) -> None:
        self.complete()
        original_load = policy_module._load_json_bytes
        def swap(root: str, name: str):
            if name == FINAL_REPORT_NAME:
                report = self.read(FINAL_REPORT_NAME)
                report["runner_version"] = "substituted"
                self.write(FINAL_REPORT_NAME, report)
            return original_load(root, name)
        with patch.object(policy_module, "_load_json_bytes", side_effect=swap):
            with self.assertRaises(EvidenceIntegrityError):
                self.verify_at(LATER)

    def test_invalid_classification_and_policy_ref_rejected(self) -> None:
        for bad in (
            ClassificationDecision(Sensitivity.INTERNAL, RedactionState.UNREDACTED_INTERNAL_ONLY,
                                   "BER-DEC-011", "synthetic-review:input"),
            ClassificationDecision(Sensitivity.INTERNAL, RedactionState.UNREDACTED_INTERNAL_ONLY,
                                   "BER-DEC-011@v1", ""),
            ClassificationDecision(None, RedactionState.UNREDACTED_INTERNAL_ONLY,
                                   "BER-DEC-011@v1", "synthetic-review:input"),
        ):
            with self.subTest(bad=bad), self.assertRaises(EvidenceError):
                self.writer.finalize_input([ClassifiedArtifact("x", b"raw", bad)])

    def test_legacy_caller_created_at_cannot_enter_policy(self) -> None:
        artifact = EvidenceArtifact("x", b"raw", ArtifactMetadata(created_at=FIRST))
        with self.assertRaises(EvidenceError):
            self.writer.finalize_input([artifact])

    def test_report_clock_overrides_rejected_before_write(self) -> None:
        sha = self.stage_a()
        for supplied in (
            {"report_metadata": ArtifactMetadata(created_at=FIRST)},
            {"report_metadata": ArtifactMetadata(), "finalized_at": LATER},
        ):
            with self.subTest(supplied=supplied), self.assertRaises(EvidenceError):
                self.writer.writer.finalize_final_bundle(
                    self.report(sha), [], sha, "OFFLINE_DEMONSTRATION", **supplied,
                )
            self.assertFalse(os.path.exists(os.path.join(self.root, FINAL_REPORT_NAME)))

    def test_missing_or_forged_first_time_fails_even_with_rehashed_manifest(self) -> None:
        for value in (None, "2030-02-01T23:00:00Z"):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as root:
                self.root = root
                self.writer = OfflinePolicyWriter(root, RUN)
                self.stage_a()
                receipt = self.read(STAGE_A_POLICY)
                if value is None:
                    receipt.pop("first_created_at")
                else:
                    receipt["first_created_at"] = value
                    receipt["bundle_review_at"] = "2030-03-03T23:00:00Z"
                new_sha = self.write(STAGE_A_POLICY, receipt)
                manifest = self.read(INPUT_MANIFEST_NAME)
                entry = next(e for e in manifest["artifacts"] if e["path"] == STAGE_A_POLICY)
                entry["sha256"] = new_sha
                entry["bytes"] = len(canonical_bytes(receipt))
                self.write(INPUT_MANIFEST_NAME, manifest)
                with self.assertRaises(EvidenceIntegrityError):
                    verify_policy_input(self.root)

    def test_rehashed_classification_forgery_fails(self) -> None:
        self.complete()
        receipt = self.read(STAGE_B_POLICY)
        receipt["classification_decisions"][0]["sha256"] = "0" * 64
        receipt_sha = self.write(STAGE_B_POLICY, receipt)
        manifest = self.read(FINAL_MANIFEST_NAME)
        entry = next(e for e in manifest["artifacts"] if e["path"] == STAGE_B_POLICY)
        entry["sha256"] = receipt_sha
        entry["bytes"] = len(canonical_bytes(receipt))
        manifest_sha = self.write(FINAL_MANIFEST_NAME, manifest)
        marker = self.read(MARKER_NAME)
        marker["final_evidence_manifest_sha256"] = manifest_sha
        self.write(MARKER_NAME, marker)
        self.assertTrue(verify_final_bundle(self.root))  # old hashes alone cannot spot the lie
        with self.assertRaises(EvidenceIntegrityError):
            self.verify_at(LATER)

    def test_invalid_matching_enum_metadata_fails(self) -> None:
        for field, value in (("sensitivity", None), ("redaction_state", "unknown")):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as root:
                self.root = root
                self.writer = OfflinePolicyWriter(root, RUN)
                self.stage_a()
                receipt = self.read(STAGE_A_POLICY)
                receipt["classification_decisions"][0][field] = value
                receipt_sha = self.write(STAGE_A_POLICY, receipt)
                manifest = self.read(INPUT_MANIFEST_NAME)
                for entry in manifest["artifacts"]:
                    if entry["path"] == "inputs/one.txt":
                        entry[field] = value
                    elif entry["path"] == STAGE_A_POLICY:
                        entry["sha256"] = receipt_sha
                        entry["bytes"] = len(canonical_bytes(receipt))
                self.write(INPUT_MANIFEST_NAME, manifest)
                with self.assertRaises(EvidenceIntegrityError):
                    verify_policy_input(self.root)

    def test_final_report_cannot_be_dropped_from_manifest_and_receipt(self) -> None:
        self.complete()
        receipt = self.read(STAGE_B_POLICY)
        receipt["classification_decisions"] = [
            item for item in receipt["classification_decisions"]
            if item["path"] != FINAL_REPORT_NAME
        ]
        receipt_sha = self.write(STAGE_B_POLICY, receipt)
        manifest = self.read(FINAL_MANIFEST_NAME)
        manifest["artifacts"] = [
            entry for entry in manifest["artifacts"] if entry["path"] != FINAL_REPORT_NAME
        ]
        entry = next(e for e in manifest["artifacts"] if e["path"] == STAGE_B_POLICY)
        entry["sha256"] = receipt_sha
        entry["bytes"] = len(canonical_bytes(receipt))
        manifest_sha = self.write(FINAL_MANIFEST_NAME, manifest)
        marker = self.read(MARKER_NAME)
        marker["final_evidence_manifest_sha256"] = manifest_sha
        self.write(MARKER_NAME, marker)
        self.assertTrue(verify_final_bundle(self.root))
        with self.assertRaises(EvidenceIntegrityError):
            self.verify_at(LATER)

    def test_marker_time_follows_all_artifacts_and_verifier_clock(self) -> None:
        sha = self.stage_a()
        times = iter((LATER, "2030-02-01T02:00:00Z", "2030-02-01T03:00:00Z"))
        with patch("tools.behavioral_eval_runner.evidence._utc_now_iso", side_effect=lambda: next(times)), \
             patch("tools.behavioral_eval_runner.evidence_policy._now",
                   side_effect=[LATER, "2030-02-01T05:00:00Z"]):
            self.writer.finalize_final(
                self.report(sha),
                [ClassifiedArtifact("outputs/one.txt", b"synthetic output", decision("output"))],
                decision("report"), "OFFLINE_DEMONSTRATION",
            )
        self.assertEqual(self.read(MARKER_NAME)["finalized_at"], "2030-02-01T03:00:00Z")
        self.assertTrue(self.verify_at("2030-02-01T05:00:00Z"))
        with self.assertRaises(EvidenceIntegrityError):
            self.verify_at("2000-01-01T00:00:00Z")
        marker = self.read(MARKER_NAME)
        marker["finalized_at"] = FIRST
        self.write(MARKER_NAME, marker)
        with self.assertRaises(EvidenceIntegrityError):
            self.verify_at("2030-02-01T05:00:00Z")

    def test_unbound_marker_and_noncanonical_policy_fail(self) -> None:
        self.complete()
        marker = self.read(MARKER_NAME)
        marker["final_evidence_manifest_sha256"] = "0" * 64
        self.write(MARKER_NAME, marker)
        with self.assertRaises(EvidenceIntegrityError):
            self.verify_at(LATER)
        with tempfile.TemporaryDirectory() as root:
            self.root = root
            self.writer = OfflinePolicyWriter(root, RUN)
            self.complete()
            path = os.path.join(self.root, *STAGE_B_POLICY.split("/"))
            with open(path, "ab") as handle:
                handle.write(b" ")
            with self.assertRaises(EvidenceIntegrityError):
                self.verify_at(LATER)

    def test_missing_marker_and_run_swap_fail(self) -> None:
        self.complete()
        os.remove(os.path.join(self.root, MARKER_NAME))
        with self.assertRaises(EvidenceIntegrityError):
            self.verify_at(LATER)
        with tempfile.TemporaryDirectory() as root:
            self.root = root
            self.writer = OfflinePolicyWriter(root, RUN)
            self.complete()
            marker = self.read(MARKER_NAME)
            marker["run_id"] = "other-run"
            self.write(MARKER_NAME, marker)
            with self.assertRaises(EvidenceIntegrityError):
                self.verify_at(LATER)

    def test_mixed_retention_and_incomplete_bundle_fail(self) -> None:
        self.stage_a()
        with self.assertRaises(EvidenceIntegrityError):
            self.verify_at(LATER)
        manifest = self.read(INPUT_MANIFEST_NAME)
        manifest["artifacts"][0]["retention_class"] = "days_90"
        self.write(INPUT_MANIFEST_NAME, manifest)
        with self.assertRaises(EvidenceIntegrityError):
            verify_policy_input(self.root)

    def test_missing_decision_fails_even_after_rehash(self) -> None:
        self.stage_a()
        receipt = self.read(STAGE_A_POLICY)
        receipt["classification_decisions"] = []
        receipt_sha = self.write(STAGE_A_POLICY, receipt)
        manifest = self.read(INPUT_MANIFEST_NAME)
        entry = next(e for e in manifest["artifacts"] if e["path"] == STAGE_A_POLICY)
        entry["sha256"] = receipt_sha
        entry["bytes"] = len(canonical_bytes(receipt))
        self.write(INPUT_MANIFEST_NAME, manifest)
        with self.assertRaises(EvidenceIntegrityError):
            verify_policy_input(self.root)


if __name__ == "__main__":
    unittest.main()
