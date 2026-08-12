"""Group A — record/identity/aggregation/report integrity (A1–A10)."""

from __future__ import annotations

import math
import unittest

from tools.behavioral_eval_runner.enums import (
    AggregateBlocker,
    AggregateVerdict,
    AttemptState,
    CaseType,
    ClaimScope,
    EvalFileKind,
    InvocationMode,
    MaterializationProfile,
    QuarantineStatus,
    ReasonCode,
    RiskClass,
    TargetKind,
    WorkspaceRole,
)
from tools.behavioral_eval_runner.errors import DishonestReportError, SchemaValidationError
from tools.behavioral_eval_runner.canonical import sha256_hex_text
from tools.behavioral_eval_runner.identity import build_assertion_uid, build_case_uid
from tools.behavioral_eval_runner.models import (
    AggregateRecord,
    AssertionRecord,
    AttemptRecord,
    CaseManifestRecord,
    CostUsage,
    CoverageMetrics,
    TypedTarget,
    planned_unrun_attempt,
)
from tools.behavioral_eval_runner.reporting import build_run_report, compute_coverage
from tools.behavioral_eval_runner.tests.helpers import make_case, make_case_uid

RUN = "run-a"


# ---------------------------------------------------------------- A1 quorum
class TestQuorumReDerivation(unittest.TestCase):
    def _agg(self, verdict, wins, planned, run, derived=True):
        return AggregateRecord(
            case_uid=make_case_uid(),
            aggregate_verdict=verdict,
            aggregate_blocker=AggregateBlocker.NONE,
            derived_from_executed_quorum=derived,
            wins=wins,
            attempts_planned=planned,
            attempts_run=run,
        )

    def test_one_of_three_pass_rejected(self) -> None:
        with self.assertRaises(SchemaValidationError):
            self._agg(AggregateVerdict.PASS, wins=1, planned=3, run=3).validate()

    def test_boolean_cannot_manufacture_quorum(self) -> None:
        # wins below quorum, but derived flag set true — still rejected.
        with self.assertRaises(SchemaValidationError):
            self._agg(AggregateVerdict.PASS, wins=1, planned=3, run=2).validate()

    def test_valid_quorum_accepted(self) -> None:
        self._agg(AggregateVerdict.PASS, wins=2, planned=3, run=3).validate()
        self._agg(AggregateVerdict.FAIL, wins=3, planned=5, run=5).validate()

    def test_inconclusive_must_not_claim_quorum(self) -> None:
        with self.assertRaises(SchemaValidationError):
            AggregateRecord(
                case_uid=make_case_uid(),
                aggregate_verdict=AggregateVerdict.INCONCLUSIVE,
                aggregate_blocker=AggregateBlocker.ERROR,
                derived_from_executed_quorum=True,
            ).validate()

    def test_inconclusive_wins_must_be_zero(self) -> None:
        with self.assertRaises(SchemaValidationError):
            AggregateRecord(
                case_uid=make_case_uid(),
                aggregate_verdict=AggregateVerdict.INCONCLUSIVE,
                aggregate_blocker=AggregateBlocker.ERROR,
                wins=5,
            ).validate()

    def test_from_dict_one_of_three_rejected(self) -> None:
        payload = self._agg(AggregateVerdict.PASS, 2, 3, 3).to_dict()
        payload["wins"] = 1
        with self.assertRaises(SchemaValidationError):
            AggregateRecord.from_dict(payload)


# ------------------------------------------------------- A2/A3 report integrity
class TestReportIntegrity(unittest.TestCase):
    def _empty_coverage(self, authored=10):
        return compute_coverage(
            authored_units_total=authored,
            selected_case_uids=[],
            preflight_results=[],
            attempts=[],
            aggregates=[],
            assertions_selected_total=0,
            assertions_accounted_total=0,
            assertions_actually_graded_total=0,
        )

    def test_cross_run_attempt_rejected(self) -> None:
        uid = make_case_uid(case_id="x")
        agg = AggregateRecord(
            case_uid=uid,
            aggregate_verdict=AggregateVerdict.INCONCLUSIVE,
            aggregate_blocker=AggregateBlocker.NOT_SELECTED,
            reason_code=ReasonCode.NOT_SELECTED,
            attempts_planned=1,
        )
        foreign = planned_unrun_attempt("OTHER-RUN", uid, 1, ReasonCode.NOT_SELECTED)
        with self.assertRaises(DishonestReportError):
            build_run_report(
                run_id=RUN,
                baseline_identity={},
                run_provenance={},
                input_evidence_manifest_sha256=None,
                attempts=[foreign],
                aggregates=[agg],
                coverage=self._empty_coverage(),
            )

    def test_duplicate_repetition_rejected(self) -> None:
        uid = make_case_uid(case_id="d")
        agg = AggregateRecord(
            case_uid=uid,
            aggregate_verdict=AggregateVerdict.INCONCLUSIVE,
            aggregate_blocker=AggregateBlocker.NOT_SELECTED,
            reason_code=ReasonCode.NOT_SELECTED,
            attempts_planned=2,
        )
        a1 = planned_unrun_attempt(RUN, uid, 1, ReasonCode.NOT_SELECTED)
        a1b = planned_unrun_attempt(RUN, uid, 1, ReasonCode.NOT_SELECTED)
        with self.assertRaises(DishonestReportError):
            build_run_report(
                run_id=RUN,
                baseline_identity={},
                run_provenance={},
                input_evidence_manifest_sha256=None,
                attempts=[a1, a1b],
                aggregates=[agg],
                coverage=self._empty_coverage(),
            )

    def test_attempt_without_aggregate_rejected(self) -> None:
        uid = make_case_uid(case_id="no-agg")
        a1 = planned_unrun_attempt(RUN, uid, 1, ReasonCode.NOT_SELECTED)
        with self.assertRaises(DishonestReportError):
            build_run_report(
                run_id=RUN,
                baseline_identity={},
                run_provenance={},
                input_evidence_manifest_sha256=None,
                attempts=[a1],
                aggregates=[],
                coverage=self._empty_coverage(),
            )

    def test_aggregate_missing_planned_attempts_rejected(self) -> None:
        uid = make_case_uid(case_id="short")
        agg = AggregateRecord(
            case_uid=uid,
            aggregate_verdict=AggregateVerdict.INCONCLUSIVE,
            aggregate_blocker=AggregateBlocker.NOT_SELECTED,
            reason_code=ReasonCode.NOT_SELECTED,
            attempts_planned=3,
        )
        only_one = planned_unrun_attempt(RUN, uid, 1, ReasonCode.NOT_SELECTED)
        with self.assertRaises(DishonestReportError):
            build_run_report(
                run_id=RUN,
                baseline_identity={},
                run_provenance={},
                input_evidence_manifest_sha256=None,
                attempts=[only_one],
                aggregates=[agg],
                coverage=self._empty_coverage(),
            )

    def test_duplicate_aggregate_rejected(self) -> None:
        uid = make_case_uid(case_id="dupagg")
        agg = AggregateRecord(
            case_uid=uid,
            aggregate_verdict=AggregateVerdict.INCONCLUSIVE,
            aggregate_blocker=AggregateBlocker.NOT_SELECTED,
            reason_code=ReasonCode.NOT_SELECTED,
            attempts_planned=0,
        )
        with self.assertRaises(DishonestReportError):
            build_run_report(
                run_id=RUN,
                baseline_identity={},
                run_provenance={},
                input_evidence_manifest_sha256=None,
                attempts=[],
                aggregates=[agg, agg],
                coverage=self._empty_coverage(),
            )

    def test_fabricated_full_coverage_on_empty_run_rejected(self) -> None:
        fabricated = CoverageMetrics(
            authored_units_total=100,
            selected_units_total=100,
            preflight_accounted_total=100,
            runnable_units_total=100,
            attempted_units_total=100,
            completed_units_total=100,
            assertions_selected_total=10,
            assertions_accounted_total=10,
            assertions_actually_graded_total=10,
        )
        with self.assertRaises(DishonestReportError):
            build_run_report(
                run_id=RUN,
                baseline_identity={},
                run_provenance={},
                input_evidence_manifest_sha256=None,
                attempts=[],
                aggregates=[],
                coverage=fabricated,
            )


# --------------------------------------------------------- A4/A5 identity binds
class TestManifestIdentityBinding(unittest.TestCase):
    def test_tampered_assertion_uid_rejected(self) -> None:
        case = make_case(assertions=("real assertion",))
        bad = AssertionRecord(
            assertion_uid="wrong::wrong::wrong::wrong::0::" + "0" * 64,
            index=0,
            text="real assertion",
        )
        payload = case.to_dict()
        payload["assertions"] = [bad.to_dict()]
        with self.assertRaises(SchemaValidationError):
            CaseManifestRecord.from_dict(payload)

    def test_duplicate_assertion_index_rejected(self) -> None:
        case = make_case(assertions=("a", "b"))
        uid = case.case_uid
        payload = case.to_dict()
        payload["assertions"] = [
            {"assertion_uid": build_assertion_uid(uid, 0, "a"), "index": 0, "text": "a"},
            {"assertion_uid": build_assertion_uid(uid, 0, "b"), "index": 0, "text": "b"},
        ]
        with self.assertRaises(SchemaValidationError):
            CaseManifestRecord.from_dict(payload)

    def test_case_uid_owner_mismatch_rejected(self) -> None:
        case = make_case(owner="skill-a", case_id="c1")
        payload = case.to_dict()
        payload["owner"] = "skill-b"  # case_uid still encodes skill-a
        with self.assertRaises(SchemaValidationError):
            CaseManifestRecord.from_dict(payload)

    def test_case_uid_caseid_mismatch_rejected(self) -> None:
        case = make_case(owner="skill-a", case_id="c1")
        payload = case.to_dict()
        payload["case_id"] = "c2"
        with self.assertRaises(SchemaValidationError):
            CaseManifestRecord.from_dict(payload)


# ------------------------------------------------------------- A6 subagent
class TestSubagentCrossField(unittest.TestCase):
    def _subagent_case(self, mode, profile, annotation="(subagent)"):
        uid = build_case_uid("owner", EvalFileKind.TRIGGER_EVAL, "sub", {"id": "sub"})
        return CaseManifestRecord(
            case_uid=uid,
            case_id="sub",
            owner="owner",
            eval_file_kind=EvalFileKind.TRIGGER_EVAL,
            case_type=CaseType.DISCRIMINATION,
            prompt_sha256=sha256_hex_text("p"),
            target=TypedTarget(TargetKind.SUBAGENT, "reviewer-agent", annotation),
            risk_class=RiskClass.STANDARD,
            risk_class_ratified=False,
            claim_scope=ClaimScope.FULL_LIBRARY,
            workspace_role=WorkspaceRole.CONSUMER,
            materialization_profile_id=profile,
            activation_mode_expected=mode,
        )

    def test_subagent_requires_delegated_mode(self) -> None:
        with self.assertRaises(SchemaValidationError):
            self._subagent_case(
                InvocationMode.MODEL_SELECTED,
                MaterializationProfile.CONSUMER_WITH_SUBAGENTS,
            ).validate()

    def test_subagent_requires_subagent_profile(self) -> None:
        with self.assertRaises(SchemaValidationError):
            self._subagent_case(
                InvocationMode.DELEGATED_SUBAGENT,
                MaterializationProfile.CONSUMER_SKILLS_ONLY,
            ).validate()

    def test_subagent_requires_annotation(self) -> None:
        with self.assertRaises(SchemaValidationError):
            self._subagent_case(
                InvocationMode.DELEGATED_SUBAGENT,
                MaterializationProfile.CONSUMER_WITH_SUBAGENTS,
                annotation=None,
            ).validate()

    def test_valid_subagent_accepted(self) -> None:
        self._subagent_case(
            InvocationMode.DELEGATED_SUBAGENT,
            MaterializationProfile.CONSUMER_WITH_SUBAGENTS,
        ).validate()

    def test_skill_may_not_use_delegated_mode(self) -> None:
        # make_case validates on construction, so the violation surfaces there.
        with self.assertRaises(SchemaValidationError):
            make_case(activation_mode=InvocationMode.DELEGATED_SUBAGENT)


# -------------------------------------------------------------- A7 strict bool
class TestStrictScalars(unittest.TestCase):
    def test_truthy_int_rejected_for_bool_field(self) -> None:
        payload = make_case().to_dict()
        payload["manual_only_target"] = 1  # truthy int, not a bool
        with self.assertRaises(SchemaValidationError):
            CaseManifestRecord.from_dict(payload)

    def test_string_rejected_for_bool_field(self) -> None:
        agg = AggregateRecord(
            case_uid=make_case_uid(),
            aggregate_verdict=AggregateVerdict.PASS,
            aggregate_blocker=AggregateBlocker.NONE,
            derived_from_executed_quorum=True,
            wins=2,
            attempts_planned=3,
            attempts_run=3,
        )
        payload = agg.to_dict()
        payload["execution_degraded"] = "false"
        with self.assertRaises(SchemaValidationError):
            AggregateRecord.from_dict(payload)


# ------------------------------------------------------------- A8 immutability
class TestDeepImmutability(unittest.TestCase):
    def test_cost_usage_source_mutation_has_no_effect(self) -> None:
        source = {"calls": 2}
        usage = CostUsage(reserved_max=source)
        before = usage.to_dict()
        source["calls"] = 999
        source["extra"] = 1
        self.assertEqual(usage.to_dict(), before)

    def test_budget_caps_source_mutation_has_no_effect(self) -> None:
        from tools.behavioral_eval_runner.budget import BudgetCaps

        source = {"calls": 5}
        caps = BudgetCaps(limits=source)
        before = caps.to_dict()
        source["calls"] = 9999
        self.assertEqual(caps.to_dict(), before)

    def test_attempt_activation_evidence_frozen(self) -> None:
        source = {"tier": 1, "nested": {"x": 1}}
        attempt = AttemptRecord(
            run_id=RUN,
            case_uid=make_case_uid(),
            repetition_number=1,
            attempt_state=AttemptState.PASS,
            activation_evidence=source,
        )
        before = attempt.to_dict()
        source["tier"] = 99
        source["nested"]["x"] = 99
        self.assertEqual(attempt.to_dict(), before)

    def test_coverage_bucket_source_mutation_has_no_effect(self) -> None:
        source = {"BUDGET_CAP": 1}
        metrics = CoverageMetrics(
            authored_units_total=1,
            selected_units_total=0,
            preflight_accounted_total=0,
            runnable_units_total=0,
            attempted_units_total=0,
            completed_units_total=0,
            assertions_selected_total=0,
            assertions_accounted_total=0,
            assertions_actually_graded_total=0,
            unrun_totals_by_reason=source,
        )
        before = metrics.to_dict()
        source["BUDGET_CAP"] = 42
        self.assertEqual(metrics.to_dict(), before)


# --------------------------------------------------------- A9 quarantine
class TestQuarantineConsistency(unittest.TestCase):
    def test_latest_must_match_current(self) -> None:
        with self.assertRaises(SchemaValidationError):
            AggregateRecord(
                case_uid=make_case_uid(),
                aggregate_verdict=AggregateVerdict.FAIL,
                aggregate_blocker=AggregateBlocker.NONE,
                derived_from_executed_quorum=True,
                wins=2,
                attempts_planned=3,
                attempts_run=3,
                quarantine_status=QuarantineStatus.ACTIVE,
                quarantine_reason="osc",
                quarantine_since="2026-08-01",
                latest_aggregate_verdict=AggregateVerdict.PASS,  # mismatch
                latest_aggregate_blocker=AggregateBlocker.NONE,
            ).validate()

    def test_consistent_quarantine_accepted(self) -> None:
        AggregateRecord(
            case_uid=make_case_uid(),
            aggregate_verdict=AggregateVerdict.FAIL,
            aggregate_blocker=AggregateBlocker.NONE,
            derived_from_executed_quorum=True,
            wins=2,
            attempts_planned=3,
            attempts_run=3,
            quarantine_status=QuarantineStatus.ACTIVE,
            quarantine_reason="osc",
            quarantine_since="2026-08-01",
            latest_aggregate_verdict=AggregateVerdict.FAIL,
            latest_aggregate_blocker=AggregateBlocker.NONE,
        ).validate()


# ------------------------------------------------------------- A10 finite
class TestFiniteNumerics(unittest.TestCase):
    def test_nan_duration_rejected(self) -> None:
        with self.assertRaises(SchemaValidationError):
            AttemptRecord(
                run_id=RUN,
                case_uid=make_case_uid(),
                repetition_number=1,
                attempt_state=AttemptState.PASS,
                duration_seconds=math.nan,
            ).validate()

    def test_inf_duration_rejected(self) -> None:
        with self.assertRaises(SchemaValidationError):
            AttemptRecord(
                run_id=RUN,
                case_uid=make_case_uid(),
                repetition_number=1,
                attempt_state=AttemptState.PASS,
                duration_seconds=math.inf,
            ).validate()

    def test_finite_duration_accepted(self) -> None:
        AttemptRecord(
            run_id=RUN,
            case_uid=make_case_uid(),
            repetition_number=1,
            attempt_state=AttemptState.PASS,
            duration_seconds=1.5,
        ).validate()


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
