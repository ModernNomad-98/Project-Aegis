"""Two-stage evidence finalization: verification, detached marker,
circularity and corruption rejection (areas 31–34)."""

from __future__ import annotations

import json
import os
import tempfile
import unittest

from tools.behavioral_eval_runner.canonical import sha256_hex
from tools.behavioral_eval_runner.errors import CircularEvidenceError, EvidenceError, EvidenceIntegrityError
from tools.behavioral_eval_runner.evidence import (
    EvidenceArtifact,
    EvidenceWriter,
    FINAL_MANIFEST_NAME,
    FINAL_REPORT_NAME,
    INPUT_MANIFEST_NAME,
    JudgeInputGate,
    MARKER_NAME,
    verify_final_bundle,
    verify_input_evidence,
)

RUN = "run-ev"


def _artifacts() -> list[EvidenceArtifact]:
    return [
        EvidenceArtifact("transcripts/attempt-1.txt", b"synthetic transcript"),
        EvidenceArtifact("audit/sandbox-log.txt", b"synthetic audit log"),
    ]


class _BundleCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = self._tmp.name
        self.writer = EvidenceWriter(self.root, RUN)

    def _report(self, input_sha: str) -> dict:
        return {
            "report_kind": "behavioral_eval_run_report",
            "run_id": RUN,
            "run_evidence_binding": {"input_evidence_manifest_sha256": input_sha},
            "aggregates": [],
        }

    def _full_bundle(self):
        stage_a = self.writer.finalize_input_evidence(_artifacts())
        stage_b = self.writer.finalize_final_bundle(
            final_report=self._report(stage_a.input_evidence_manifest_sha256),
            artifacts=[EvidenceArtifact("judge/none.txt", b"no judge in WP-2B-1")],
            input_manifest_sha256=stage_a.input_evidence_manifest_sha256,
            final_status="OFFLINE_DEMONSTRATION",
        )
        return stage_a, stage_b


class TestStageA(_BundleCase):
    def test_finalize_and_verify(self) -> None:
        bundle = self.writer.finalize_input_evidence(_artifacts())
        self.assertEqual(bundle.artifact_count, 2)
        self.assertEqual(
            verify_input_evidence(self.root), bundle.input_evidence_manifest_sha256
        )

    def test_manifest_excludes_itself(self) -> None:
        self.writer.finalize_input_evidence(_artifacts())
        with open(os.path.join(self.root, INPUT_MANIFEST_NAME), encoding="utf-8") as fh:
            manifest = json.load(fh)
        paths = [entry["path"] for entry in manifest["artifacts"]]
        self.assertNotIn(INPUT_MANIFEST_NAME, paths)

    def test_metadata_on_every_artifact(self) -> None:
        self.writer.finalize_input_evidence(_artifacts())
        with open(os.path.join(self.root, INPUT_MANIFEST_NAME), encoding="utf-8") as fh:
            manifest = json.load(fh)
        for entry in manifest["artifacts"]:
            for key in (
                "retention_class",
                "sensitivity",
                "redaction_state",
                "created_at",
                "expiration_at",
                "access_policy_ref",
                "preserve_on_failure",
            ):
                self.assertIn(key, entry)

    def test_corrupted_artifact_fails_closed(self) -> None:
        self.writer.finalize_input_evidence(_artifacts())
        target = os.path.join(self.root, "transcripts", "attempt-1.txt")
        with open(target, "ab") as fh:
            fh.write(b" TAMPERED")
        with self.assertRaises(EvidenceIntegrityError) as ctx:
            verify_input_evidence(self.root)
        self.assertEqual(ctx.exception.reason_code, "EVIDENCE_INTEGRITY_FAILURE")

    def test_truncated_artifact_fails_closed(self) -> None:
        self.writer.finalize_input_evidence(_artifacts())
        target = os.path.join(self.root, "audit", "sandbox-log.txt")
        with open(target, "rb") as fh:
            content = fh.read()
        with open(target, "wb") as fh:
            fh.write(content[:-3])
        with self.assertRaises(EvidenceIntegrityError):
            verify_input_evidence(self.root)

    def test_missing_artifact_fails_closed(self) -> None:
        self.writer.finalize_input_evidence(_artifacts())
        os.remove(os.path.join(self.root, "transcripts", "attempt-1.txt"))
        with self.assertRaises(EvidenceIntegrityError):
            verify_input_evidence(self.root)

    def test_judge_gate_requires_verification_first(self) -> None:
        self.writer.finalize_input_evidence(_artifacts())
        gate = JudgeInputGate(self.root)
        with self.assertRaises(EvidenceIntegrityError):
            gate.read_artifact("transcripts/attempt-1.txt")
        gate.verify()
        self.assertEqual(
            gate.read_artifact("transcripts/attempt-1.txt"), b"synthetic transcript"
        )

    def test_judge_gate_fails_closed_on_tamper(self) -> None:
        self.writer.finalize_input_evidence(_artifacts())
        with open(
            os.path.join(self.root, "transcripts", "attempt-1.txt"), "ab"
        ) as fh:
            fh.write(b"x")
        gate = JudgeInputGate(self.root)
        with self.assertRaises(EvidenceIntegrityError):
            gate.verify()
        self.assertFalse(gate.verified)

    def test_reserved_and_traversal_paths_refused(self) -> None:
        for path in (INPUT_MANIFEST_NAME, MARKER_NAME, "../escape.txt", "a/../b"):
            with self.assertRaises(EvidenceError):
                self.writer.finalize_input_evidence(
                    [EvidenceArtifact(path, b"x")]
                )


class TestStageB(_BundleCase):
    def test_detached_marker_binds_report_and_manifest(self) -> None:
        _stage_a, stage_b = self._full_bundle()
        result = verify_final_bundle(self.root)
        self.assertEqual(
            result["final_evidence_manifest_sha256"],
            stage_b.final_evidence_manifest_sha256,
        )
        self.assertEqual(result["final_report_sha256"], stage_b.final_report_sha256)

    def test_final_manifest_excludes_itself_and_marker(self) -> None:
        self._full_bundle()
        with open(os.path.join(self.root, FINAL_MANIFEST_NAME), encoding="utf-8") as fh:
            manifest = json.load(fh)
        paths = [entry["path"] for entry in manifest["artifacts"]]
        self.assertNotIn(FINAL_MANIFEST_NAME, paths)
        self.assertNotIn(MARKER_NAME, paths)
        self.assertIn(FINAL_REPORT_NAME, paths)

    def test_report_carries_input_hash_never_final_hash(self) -> None:
        stage_a, stage_b = self._full_bundle()
        with open(os.path.join(self.root, FINAL_REPORT_NAME), "rb") as fh:
            report_bytes = fh.read()
        self.assertIn(
            stage_a.input_evidence_manifest_sha256.encode("ascii"), report_bytes
        )
        self.assertNotIn(
            stage_b.final_evidence_manifest_sha256.encode("ascii"), report_bytes
        )

    def test_marker_contains_no_self_hash(self) -> None:
        _stage_a, stage_b = self._full_bundle()
        with open(os.path.join(self.root, MARKER_NAME), "rb") as fh:
            marker_bytes = fh.read()
        self.assertNotIn(
            stage_b.finalization_marker_sha256.encode("ascii"), marker_bytes
        )

    def test_report_with_final_hash_field_refused(self) -> None:
        stage_a = self.writer.finalize_input_evidence(_artifacts())
        report = self._report(stage_a.input_evidence_manifest_sha256)
        report["run_evidence_binding"]["final_report_sha256"] = "0" * 64
        with self.assertRaises(CircularEvidenceError):
            self.writer.finalize_final_bundle(
                report,
                [],
                stage_a.input_evidence_manifest_sha256,
                "X",
            )

    def test_report_without_binding_refused(self) -> None:
        stage_a = self.writer.finalize_input_evidence(_artifacts())
        with self.assertRaises(EvidenceError):
            self.writer.finalize_final_bundle(
                {"report_kind": "x"}, [], stage_a.input_evidence_manifest_sha256, "X"
            )

    def test_tampered_final_report_fails_closed(self) -> None:
        self._full_bundle()
        target = os.path.join(self.root, FINAL_REPORT_NAME)
        with open(target, "ab") as fh:
            fh.write(b" ")
        with self.assertRaises(EvidenceIntegrityError):
            verify_final_bundle(self.root)

    def test_missing_marker_never_trusted(self) -> None:
        self._full_bundle()
        os.remove(os.path.join(self.root, MARKER_NAME))
        with self.assertRaises(EvidenceIntegrityError):
            verify_final_bundle(self.root)

    def test_marker_manifest_mismatch_fails_closed(self) -> None:
        self._full_bundle()
        marker_path = os.path.join(self.root, MARKER_NAME)
        with open(marker_path, encoding="utf-8") as fh:
            marker = json.load(fh)
        marker["final_evidence_manifest_sha256"] = "f" * 64
        with open(marker_path, "w", encoding="utf-8") as fh:
            json.dump(marker, fh)
        with self.assertRaises(EvidenceIntegrityError):
            verify_final_bundle(self.root)

    def test_manifest_listing_marker_is_circular(self) -> None:
        self._full_bundle()
        manifest_path = os.path.join(self.root, FINAL_MANIFEST_NAME)
        with open(manifest_path, encoding="utf-8") as fh:
            manifest = json.load(fh)
        with open(os.path.join(self.root, MARKER_NAME), "rb") as fh:
            marker_bytes = fh.read()
        manifest["artifacts"].append(
            {
                "path": MARKER_NAME,
                "bytes": len(marker_bytes),
                "sha256": sha256_hex(marker_bytes),
                "sensitivity": "INTERNAL",
                "redaction_state": "sanitized_by_construction",
                "retention_class": "days_30",
                "created_at": "2026-08-12T00:00:00Z",
                "expiration_at": "2026-09-11T00:00:00Z",
                "access_policy_ref": "x",
                "preserve_on_failure": True,
            }
        )
        with open(manifest_path, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh)
        with self.assertRaises(EvidenceIntegrityError):
            verify_final_bundle(self.root)

    def test_unfinalized_bundle_never_trusted(self) -> None:
        # Stage A only — no final manifest, no marker: rollups must refuse.
        self.writer.finalize_input_evidence(_artifacts())
        with self.assertRaises(EvidenceIntegrityError):
            verify_final_bundle(self.root)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
