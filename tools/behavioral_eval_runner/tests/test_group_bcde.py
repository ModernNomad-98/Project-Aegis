"""Groups B–E regression tests (preflight completeness, materialization/census,
evidence binding, budget/scheduler/deadlines/process control)."""

from __future__ import annotations

import json
import math
import os
import tempfile
import unittest

from tools.behavioral_eval_runner.budget import BudgetCaps, BudgetLedger
from tools.behavioral_eval_runner.enums import (
    AggregateBlocker,
    AggregateVerdict,
    ClaimScope,
    MaterializationProfile,
    PreflightOutcome,
    ReasonCode,
    WorkspaceRole,
)
from tools.behavioral_eval_runner.errors import (
    BudgetError,
    ControlPlaneLeakageError,
    EvidenceError,
    EvidenceIntegrityError,
    LedgerIntegrityError,
    MaterializationError,
    ProcessControlError,
    ReservationDeniedError,
)
from tools.behavioral_eval_runner.evidence import (
    EvidenceArtifact,
    EvidenceWriter,
    verify_final_bundle,
)
from tools.behavioral_eval_runner.materialize import (
    FixtureDefinition,
    MaterializationRequest,
    SyntheticSnapshot,
    materialize,
    verify_materialization_manifests,
)
from tools.behavioral_eval_runner.preflight import PreflightEnvironment, evaluate_case
from tools.behavioral_eval_runner.process_control import TimeoutController
from tools.behavioral_eval_runner.runtime_surface import classify_skill_file
from tools.behavioral_eval_runner.enums import RuntimeClassification
from tools.behavioral_eval_runner.scheduler import (
    SchedulingPolicy,
    SelectionItem,
    schedule_with_reservation,
)
from tools.behavioral_eval_runner.enums import InclusionReason, SchedulingPriority
from tools.behavioral_eval_runner.tests.helpers import (
    make_case,
    make_case_uid,
    synthetic_corpus_files,
)


# =================================================================== Group B
class TestPreflightCompleteness(unittest.TestCase):
    def test_missing_required_file_excluded(self) -> None:
        from tools.behavioral_eval_runner.models import CaseManifestRecord

        payload = make_case(case_id="needs-file").to_dict()
        payload["required_files"] = ["services/report_builder.py"]
        case = CaseManifestRecord.from_dict(payload)
        result = evaluate_case(case, PreflightEnvironment())
        self.assertIs(result.outcome, PreflightOutcome.PRECHECK_EXCLUDED)
        self.assertIs(result.reason_code, ReasonCode.MISSING_PREREQUISITE)
        self.assertTrue(result.findings)

    def test_present_required_file_runnable(self) -> None:
        from tools.behavioral_eval_runner.models import CaseManifestRecord

        payload = make_case(case_id="has-file").to_dict()
        payload["required_files"] = ["services/report_builder.py"]
        case = CaseManifestRecord.from_dict(payload)
        env = PreflightEnvironment(
            available_fixture_files=frozenset({"services/report_builder.py"})
        )
        self.assertIs(evaluate_case(case, env).outcome, PreflightOutcome.RUNNABLE)

    def test_missing_tool_permission_excluded(self) -> None:
        from tools.behavioral_eval_runner.models import CaseManifestRecord

        payload = make_case(case_id="needs-perm").to_dict()
        payload["required_tool_permissions"] = ["Edit"]
        case = CaseManifestRecord.from_dict(payload)
        result = evaluate_case(case, PreflightEnvironment())
        self.assertIs(result.outcome, PreflightOutcome.PRECHECK_EXCLUDED)
        self.assertIs(result.reason_code, ReasonCode.MISSING_PREREQUISITE)

    def test_unsafe_required_file_path_excluded(self) -> None:
        from tools.behavioral_eval_runner.models import CaseManifestRecord

        payload = make_case(case_id="evil").to_dict()
        payload["required_files"] = ["../escape.py"]
        case = CaseManifestRecord.from_dict(payload)
        result = evaluate_case(case, PreflightEnvironment())
        self.assertIs(result.outcome, PreflightOutcome.PRECHECK_EXCLUDED)


# =================================================================== Group C
def _full_request(dest, **kwargs):
    return MaterializationRequest(
        snapshot=SyntheticSnapshot(synthetic_corpus_files()),
        profile=MaterializationProfile.CONSUMER_SKILLS_ONLY,
        workspace_role=WorkspaceRole.CONSUMER,
        claim_scope=ClaimScope.FULL_LIBRARY,
        destination_root=dest,
        **kwargs,
    )


class TestMaterializationCensus(unittest.TestCase):
    def test_manifests_persisted_and_verifiable(self) -> None:
        with tempfile.TemporaryDirectory() as dest:
            record = materialize(
                _full_request(
                    dest,
                    fixture=FixtureDefinition(
                        fixture_id="fx", files={"app/x.txt": b"fixture"}
                    ),
                )
            )
            for name in (
                "control_plane_manifest.json",
                "runtime_surface_manifest.json",
                "product_fixture_manifest.json",
            ):
                self.assertIn(name, record.manifest_paths)
                self.assertTrue(os.path.exists(record.manifest_paths[name]))
            result = verify_materialization_manifests(dest, record)
            self.assertTrue(result["verified"])

    def test_manifest_verification_fails_on_tamper(self) -> None:
        with tempfile.TemporaryDirectory() as dest:
            record = materialize(_full_request(dest))
            # Tamper a materialized runtime file after manifest write.
            skill_md = os.path.join(
                dest, "runtime_surface", ".claude", "skills", "skill-a", "SKILL.md"
            )
            with open(skill_md, "ab") as fh:
                fh.write(b" TAMPERED")
            with self.assertRaises(MaterializationError):
                verify_materialization_manifests(dest, record)

    def test_control_plane_manifest_not_under_runtime_root(self) -> None:
        with tempfile.TemporaryDirectory() as dest:
            record = materialize(_full_request(dest))
            runtime_root = os.path.realpath(os.path.join(dest, "runtime_surface"))
            for path in record.manifest_paths.values():
                self.assertNotEqual(
                    os.path.commonpath([runtime_root, os.path.realpath(path)]),
                    runtime_root,
                )

    def test_skill_dir_without_entry_point_is_not_shipped(self) -> None:
        files = synthetic_corpus_files()
        # A directory with only a supporting file (no SKILL.md).
        del files[".claude/skills/skill-c/SKILL.md"]
        files[".claude/skills/skill-c/references/x.md"] = b"orphan"
        with tempfile.TemporaryDirectory() as dest:
            record = materialize(
                MaterializationRequest(
                    snapshot=SyntheticSnapshot(files),
                    profile=MaterializationProfile.CONSUMER_SKILLS_ONLY,
                    workspace_role=WorkspaceRole.CONSUMER,
                    claim_scope=ClaimScope.FULL_LIBRARY,
                    destination_root=dest,
                )
            )
            # skill-c no longer counts as a shipped skill (no entry point).
            self.assertEqual(record.shipped_skill_count, 2)

    def test_control_plane_path_fragment_classified(self) -> None:
        for path in (
            "references/rubric/criteria.md",
            "references/answer-bank/examples.json",
            "assets/case-manifest/data.json",
        ):
            self.assertIs(
                classify_skill_file(path).classification,
                RuntimeClassification.CONTROL_PLANE_ONLY,
                path,
            )

    def test_snapshot_files_are_immutable_view(self) -> None:
        snap = SyntheticSnapshot(synthetic_corpus_files())
        files = snap.files()
        with self.assertRaises(TypeError):
            files["injected"] = b"x"  # type: ignore[index]


# =================================================================== Group D
class TestEvidenceBinding(unittest.TestCase):
    def _bundle(self, root, run_id):
        writer = EvidenceWriter(root, run_id)
        stage_a = writer.finalize_input_evidence(
            [EvidenceArtifact("t/a.txt", b"bytes")]
        )
        return writer, stage_a

    def test_cross_run_report_rejected_at_finalize(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            writer, stage_a = self._bundle(root, "run-A")
            report = {
                "report_kind": "behavioral_eval_run_report",
                "run_id": "run-B",  # wrong run
                "run_evidence_binding": {
                    "input_evidence_manifest_sha256": stage_a.input_evidence_manifest_sha256
                },
                "aggregates": [],
            }
            with self.assertRaises(EvidenceError):
                writer.finalize_final_bundle(
                    report, [], stage_a.input_evidence_manifest_sha256, "X"
                )

    def test_cross_run_mixture_rejected_at_verify(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            writer, stage_a = self._bundle(root, "run-A")
            report = {
                "report_kind": "behavioral_eval_run_report",
                "run_id": "run-A",
                "run_evidence_binding": {
                    "input_evidence_manifest_sha256": stage_a.input_evidence_manifest_sha256
                },
                "aggregates": [],
            }
            writer.finalize_final_bundle(
                report, [], stage_a.input_evidence_manifest_sha256, "X"
            )
            # Corrupt the marker's run_id to simulate a cross-run mixture.
            from tools.behavioral_eval_runner.evidence import MARKER_NAME

            marker_path = os.path.join(root, MARKER_NAME)
            with open(marker_path, encoding="utf-8") as fh:
                marker = json.load(fh)
            marker["run_id"] = "run-Z"
            with open(marker_path, "w", encoding="utf-8") as fh:
                json.dump(marker, fh)
            with self.assertRaises(EvidenceIntegrityError):
                verify_final_bundle(root)

    def test_naive_timestamp_rejected(self) -> None:
        from tools.behavioral_eval_runner.evidence import ArtifactMetadata

        with tempfile.TemporaryDirectory() as root:
            writer = EvidenceWriter(root, "run-tz")
            with self.assertRaises(EvidenceError):
                writer.finalize_input_evidence(
                    [
                        EvidenceArtifact(
                            "t/a.txt",
                            b"x",
                            ArtifactMetadata(created_at="2026-08-12T00:00:00"),
                        )
                    ]
                )


# =================================================================== Group E
class TestBudgetDeadlineAndDrift(unittest.TestCase):
    def test_deadline_denies_after_expiry(self) -> None:
        clock = {"t": 1000.0}
        caps = BudgetCaps(limits={"calls": 100}, wall_clock_deadline_seconds=10)
        ledger = BudgetLedger(caps, clock=lambda: clock["t"])
        ledger.reserve("c1", {"calls": 1})  # before deadline
        clock["t"] = 1011.0  # past deadline
        with self.assertRaises(ReservationDeniedError):
            ledger.reserve("c2", {"calls": 1})
        self.assertTrue(ledger.kill_switch_engaged)

    def test_deadline_survives_reload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = os.path.join(tmp, "l.jsonl")
            clock = {"t": 5000.0}
            caps = BudgetCaps(limits={"calls": 100}, wall_clock_deadline_seconds=10)
            BudgetLedger(caps, store_path=store, clock=lambda: clock["t"])
            clock["t"] = 5020.0  # deadline passed before reload
            resumed = BudgetLedger.load(store, caps, clock=lambda: clock["t"])
            with self.assertRaises(ReservationDeniedError):
                resumed.reserve("c1", {"calls": 1})

    def test_drift_preserves_reservation_and_engages_kill(self) -> None:
        ledger = BudgetLedger(BudgetCaps(limits={"calls": 10}))
        reservation = ledger.reserve("c1", {"calls": 2})
        with self.assertRaises(BudgetError):
            ledger.reconcile(reservation, {"calls": 5})  # overrun
        self.assertTrue(ledger.kill_switch_engaged)
        # Reservation preserved (still in flight).
        self.assertEqual(ledger.totals()["inflight_count"], 1)
        with self.assertRaises(ReservationDeniedError):
            ledger.reserve("c2", {"calls": 1})

    def test_empty_reservation_denied(self) -> None:
        ledger = BudgetLedger(BudgetCaps(limits={"calls": 10}))
        with self.assertRaises(ReservationDeniedError):
            ledger.reserve("c1", {})
        with self.assertRaises(ReservationDeniedError):
            ledger.reserve("c2", {"calls": 0})

    def test_checkpoint_required_on_load(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = os.path.join(tmp, "l.jsonl")
            caps = BudgetCaps(limits={"calls": 5})
            BudgetLedger(caps, store_path=store)
            os.remove(store + ".checkpoint.json")
            with self.assertRaises(LedgerIntegrityError):
                BudgetLedger.load(store, caps)

    def test_checkpoint_rollback_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = os.path.join(tmp, "l.jsonl")
            caps = BudgetCaps(limits={"calls": 5})
            ledger = BudgetLedger(caps, store_path=store)
            # Snapshot the early checkpoint, then advance the ledger.
            with open(store + ".checkpoint.json", encoding="utf-8") as fh:
                stale = fh.read()
            r = ledger.reserve("c1", {"calls": 1})
            ledger.reconcile(r, {"calls": 1})
            # Roll the checkpoint back to the stale one (mismatch with ledger).
            with open(store + ".checkpoint.json", "w", encoding="utf-8") as fh:
                fh.write(stale)
            with self.assertRaises(LedgerIntegrityError):
                BudgetLedger.load(store, caps)


class TestSchedulerPrefix(unittest.TestCase):
    def _item(self, cid, priority, calls=1):
        return SelectionItem(
            case_uid=make_case_uid(case_id=cid),
            priority=priority,
            inclusion_reason=InclusionReason.CADENCE_SLOT,
            reservation_request={"calls": calls},
        )

    def test_no_lower_priority_after_prefix_exhaustion(self) -> None:
        selection = [
            self._item("crit", SchedulingPriority.CRITICAL_SAFETY, calls=2),
            self._item("std-a", SchedulingPriority.STANDARD_CHANGED_SCOPE, calls=2),
            self._item("std-b", SchedulingPriority.STANDARD_CHANGED_SCOPE, calls=2),
        ]
        ledger = BudgetLedger(BudgetCaps(limits={"calls": 3}))
        evidence = schedule_with_reservation(SchedulingPolicy(), selection, ledger)
        reserved = [d for d in evidence.decisions if d.reservation_result == "reserved"]
        denied = [d for d in evidence.decisions if d.reservation_result == "denied"]
        # Only the critical prefix (2 calls) fits; the rest are prefix-exhausted.
        self.assertEqual(len(reserved), 1)
        self.assertEqual(reserved[0].case_uid, make_case_uid(case_id="crit"))
        for d in denied:
            self.assertEqual(d.unrun_reason_code, "BUDGET_CAP")

    def test_empty_reservation_item_denied_not_reserved(self) -> None:
        item = self._item("empty", SchedulingPriority.STANDARD_CHANGED_SCOPE, calls=0)
        ledger = BudgetLedger(BudgetCaps(limits={"calls": 10}))
        evidence = schedule_with_reservation(SchedulingPolicy(), [item], ledger)
        self.assertEqual(evidence.decisions[0].reservation_result, "denied")


class TestTimeoutFinite(unittest.TestCase):
    def test_rejects_nonfinite_and_bool(self) -> None:
        for bad in (True, False, math.nan, math.inf, -math.inf, 0, -1):
            with self.assertRaises(ProcessControlError):
                TimeoutController(bad)  # type: ignore[arg-type]


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
