"""Regression tests for the self-review remediations (review findings).

Covers: evidence verification bypasses, scheduler dedup, materializer empty
destination and subagent fail-closed, budget uncapped-dimension denial and
ledger tamper detection, aggregation unmapped-reason fail-closed, and the
AST-based static-safety scan.
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest

from tools.behavioral_eval_runner.aggregation import AttemptSet, aggregate_case
from tools.behavioral_eval_runner.budget import BudgetCaps, BudgetLedger
from tools.behavioral_eval_runner.cli import scan_package_sources
from tools.behavioral_eval_runner.enums import (
    AttemptState,
    ClaimScope,
    InclusionReason,
    MaterializationProfile,
    ReasonCode,
    SchedulingPriority,
    WorkspaceRole,
)
from tools.behavioral_eval_runner.errors import (
    AggregationError,
    EvidenceIntegrityError,
    LedgerIntegrityError,
    MaterializationError,
    ReservationDeniedError,
    SchedulerError,
)
from tools.behavioral_eval_runner.evidence import (
    ArtifactMetadata,
    EvidenceArtifact,
    EvidenceWriter,
    INPUT_MANIFEST_NAME,
    JudgeInputGate,
    verify_final_bundle,
)
from tools.behavioral_eval_runner.materialize import (
    FixtureDefinition,
    MaterializationRequest,
    SyntheticSnapshot,
    materialize,
)
from tools.behavioral_eval_runner.models import AttemptRecord, planned_unrun_attempt
from tools.behavioral_eval_runner.scheduler import (
    SchedulingPolicy,
    SelectionItem,
    schedule_with_reservation,
)
from tools.behavioral_eval_runner.tests.helpers import make_case_uid, synthetic_corpus_files

RUN = "run-harden"


class TestEvidenceGateHardening(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = self._tmp.name
        writer = EvidenceWriter(self.root, RUN)
        self.bundle = writer.finalize_input_evidence(
            [EvidenceArtifact("t/a.txt", b"trusted bytes")]
        )

    def test_gate_refuses_unlisted_path(self) -> None:
        gate = JudgeInputGate(self.root)
        gate.verify()
        # An empty-manifest bundle would still fail here; a real bundle also
        # refuses any path not present in the verified manifest.
        with open(os.path.join(self.root, "planted.txt"), "wb") as fh:
            fh.write(b"planted")
        with self.assertRaises(EvidenceIntegrityError):
            gate.read_artifact("planted.txt")

    def test_gate_rehashes_on_read_catching_post_verify_tamper(self) -> None:
        gate = JudgeInputGate(self.root)
        gate.verify()
        with open(os.path.join(self.root, "t", "a.txt"), "wb") as fh:
            fh.write(b"tampered after verify")
        with self.assertRaises(EvidenceIntegrityError):
            gate.read_artifact("t/a.txt")

    def test_manifest_path_traversal_refused(self) -> None:
        manifest_path = os.path.join(self.root, INPUT_MANIFEST_NAME)
        with open(manifest_path, encoding="utf-8") as fh:
            manifest = json.load(fh)
        manifest["artifacts"][0]["path"] = "../escape.txt"
        with open(manifest_path, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh)
        gate = JudgeInputGate(self.root)
        with self.assertRaises(EvidenceIntegrityError):
            gate.verify()

    def test_stage_a_substitution_detected_by_final_verify(self) -> None:
        writer = EvidenceWriter(self.root, RUN)
        report = {
            "report_kind": "behavioral_eval_run_report",
            "run_id": RUN,
            "run_evidence_binding": {
                "input_evidence_manifest_sha256": self.bundle.input_evidence_manifest_sha256
            },
            "aggregates": [],
        }
        writer.finalize_final_bundle(
            report, [], self.bundle.input_evidence_manifest_sha256, "OFFLINE"
        )
        # Swap stage A wholesale (self-consistent new manifest); the final
        # report still records the ORIGINAL input hash -> mismatch caught.
        writer2 = EvidenceWriter(self.root, RUN)
        writer2.finalize_input_evidence(
            [EvidenceArtifact("t/a.txt", b"substituted stage A bytes")]
        )
        with self.assertRaises(EvidenceIntegrityError):
            verify_final_bundle(self.root)

    def test_stage_a_artifact_cannot_be_named_final_report(self) -> None:
        writer = EvidenceWriter(self.root + "_2", RUN)
        with self.assertRaises(Exception):
            writer.finalize_input_evidence(
                [EvidenceArtifact("final_report.json", b"x")]
            )


class TestSchedulerDedup(unittest.TestCase):
    def test_duplicate_selection_refused_at_reservation_entry(self) -> None:
        uid = make_case_uid(case_id="dup")
        item_a = SelectionItem(
            case_uid=uid,
            priority=SchedulingPriority.STANDARD_CHANGED_SCOPE,
            inclusion_reason=InclusionReason.OWN_CASE,
            reservation_request={"calls": 1},
        )
        item_b = SelectionItem(
            case_uid=uid,
            priority=SchedulingPriority.CRITICAL_SAFETY,
            inclusion_reason=InclusionReason.OWN_CASE,
            reservation_request={"calls": 5},
        )
        ledger = BudgetLedger(BudgetCaps(limits={"calls": 10}))
        with self.assertRaises(SchedulerError):
            schedule_with_reservation(SchedulingPolicy(), [item_a, item_b], ledger)


class TestMaterializeHardening(unittest.TestCase):
    def _request(self, dest: str, **kwargs) -> MaterializationRequest:
        return MaterializationRequest(
            snapshot=SyntheticSnapshot(synthetic_corpus_files()),
            profile=MaterializationProfile.CONSUMER_SKILLS_ONLY,
            workspace_role=WorkspaceRole.CONSUMER,
            claim_scope=ClaimScope.FULL_LIBRARY,
            destination_root=dest,
            **kwargs,
        )

    def test_non_empty_destination_refused(self) -> None:
        with tempfile.TemporaryDirectory() as dest:
            with open(os.path.join(dest, "stale.txt"), "w", encoding="utf-8") as fh:
                fh.write("prior run")
            with self.assertRaises(MaterializationError):
                materialize(self._request(dest))

    def test_required_subagent_missing_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as dest:
            request = MaterializationRequest(
                snapshot=SyntheticSnapshot(synthetic_corpus_files()),
                profile=MaterializationProfile.CONSUMER_WITH_SUBAGENTS,
                workspace_role=WorkspaceRole.CONSUMER,
                claim_scope=ClaimScope.FULL_LIBRARY,
                destination_root=dest,
                required_subagents=("does-not-exist",),
            )
            with self.assertRaises(MaterializationError):
                materialize(request)

    def test_required_subagent_under_wrong_profile_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as dest:
            request = MaterializationRequest(
                snapshot=SyntheticSnapshot(synthetic_corpus_files()),
                profile=MaterializationProfile.CONSUMER_SKILLS_ONLY,
                workspace_role=WorkspaceRole.CONSUMER,
                claim_scope=ClaimScope.FULL_LIBRARY,
                destination_root=dest,
                required_subagents=("reviewer-agent",),
            )
            with self.assertRaises(MaterializationError):
                materialize(request)


class TestBudgetHardening(unittest.TestCase):
    def test_uncapped_dimension_denied_by_default(self) -> None:
        ledger = BudgetLedger(BudgetCaps(limits={"calls": 10}))
        with self.assertRaises(ReservationDeniedError):
            ledger.reserve("case-1", {"input_tokens": 1})  # no cap for input_tokens

    def test_zero_request_for_uncapped_dimension_allowed(self) -> None:
        ledger = BudgetLedger(BudgetCaps(limits={"calls": 10}))
        reservation = ledger.reserve("case-1", {"calls": 1, "input_tokens": 0})
        ledger.reconcile(reservation, {"calls": 1, "input_tokens": 0})

    def test_deleted_ledger_line_breaks_chain_on_load(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = os.path.join(tmp, "ledger.jsonl")
            ledger = BudgetLedger(BudgetCaps(limits={"calls": 5}), store_path=store)
            r1 = ledger.reserve("case-1", {"calls": 2})
            ledger.reconcile(r1, {"calls": 2})
            r2 = ledger.reserve("case-2", {"calls": 2})
            ledger.reconcile(r2, {"calls": 2})
            with open(store, encoding="utf-8") as fh:
                lines = fh.read().splitlines()
            # Drop a RESERVE line to try to restore headroom.
            del lines[1]
            with open(store, "w", encoding="utf-8", newline="\n") as fh:
                fh.write("\n".join(lines) + "\n")
            with self.assertRaises(LedgerIntegrityError):
                BudgetLedger.load(store, BudgetCaps(limits={"calls": 5}))

    def test_corrupt_ledger_line_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = os.path.join(tmp, "ledger.jsonl")
            BudgetLedger(BudgetCaps(limits={"calls": 5}), store_path=store)
            with open(store, "a", encoding="utf-8", newline="\n") as fh:
                fh.write("{not valid json\n")
            with self.assertRaises(LedgerIntegrityError):
                BudgetLedger.load(store, BudgetCaps(limits={"calls": 5}))


class TestAggregationUnmappedReason(unittest.TestCase):
    def test_unmapped_unrun_reason_fails_closed(self) -> None:
        uid = make_case_uid(case_id="unmapped")
        attempt_set = AttemptSet(RUN, uid, 3)
        for rep in (1, 2, 3):
            attempt_set.add(
                planned_unrun_attempt(RUN, uid, rep, ReasonCode.LIVE_DISPATCH_DISABLED)
            )
        with self.assertRaises(AggregationError):
            aggregate_case(attempt_set)


class TestStaticScanCannotBeBypassedByComment(unittest.TestCase):
    def test_scan_is_ast_based_not_substring(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            # A file that names the old escape marker in a comment AND imports a
            # network module must still be flagged.
            with open(os.path.join(root, "sneaky.py"), "w", encoding="utf-8") as fh:
                fh.write(
                    "# FORBIDDEN_SOURCE_PATTERNS reviewed\n"
                    "import socket  # noqa\n"
                )
            violations = scan_package_sources(root)
            self.assertTrue(
                any(v["kind"] == "forbidden-import" for v in violations), violations
            )

    def test_shell_true_flagged(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            with open(os.path.join(root, "s.py"), "w", encoding="utf-8") as fh:
                fh.write("import subprocess\nsubprocess.run(['x'], shell=True)\n")
            violations = scan_package_sources(root)
            self.assertTrue(any(v["kind"] == "shell-true" for v in violations))

    def test_dynamic_exec_flagged(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            with open(os.path.join(root, "d.py"), "w", encoding="utf-8") as fh:
                fh.write("import os\nos.system('echo hi')\n")
            violations = scan_package_sources(root)
            self.assertTrue(
                any(v["kind"] == "dynamic-or-shell-exec" for v in violations)
            )

    def test_extended_dynamic_exec_forms_flagged(self) -> None:
        # eval/exec/compile and the os.execl*/os.spawn* families are covered.
        snippets = (
            "eval('1+1')\n",
            "exec('x=1')\n",
            "compile('1', '<s>', 'eval')\n",
            "import os\nos.execlp('x', 'x')\n",
            "import os\nos.spawnv(os.P_WAIT, 'x', ['x'])\n",
        )
        for i, src in enumerate(snippets):
            with tempfile.TemporaryDirectory() as root:
                with open(os.path.join(root, f"m{i}.py"), "w", encoding="utf-8") as fh:
                    fh.write(src)
                violations = scan_package_sources(root)
                self.assertTrue(
                    any(v["kind"] == "dynamic-or-shell-exec" for v in violations),
                    src,
                )

    def test_real_package_is_clean(self) -> None:
        self.assertEqual(scan_package_sources(), [])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
