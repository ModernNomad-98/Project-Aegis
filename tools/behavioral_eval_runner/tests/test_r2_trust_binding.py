"""R2 correction pass (PR85-WP2B2-TRUST-AND-EVIDENCE-BINDING-CORRECTION):
regressions for the independently proven defects at head f3f82ece.

P1-A  Trusted grading plans are separated from observed evidence: no
      observation can redefine the criteria it is graded against.
P1-B  grade_control enforces the complete required deterministic oracle set.
P1-C  Judge request / envelope / control context / mock response are bound.
P1-D  The CLI emits repository-safe envelope metadata only.
P2-E  Strict runtime parsers and closed control IDs.

Each test asserts the CORRECTED contract; at f3f82ece these fail (RED)."""

from __future__ import annotations

import contextlib
import io
import json
import os
import tempfile
import unittest

from tools.behavioral_eval_runner.canonical import canonical_bytes, sha256_of_obj
from tools.behavioral_eval_runner.errors import (
    EvidenceIntegrityError,
    RunnerError,
    SchemaValidationError,
)
from tools.behavioral_eval_runner.evidence import (
    ArtifactMetadata,
    EvidenceArtifact,
    EvidenceWriter,
    JudgeInputGate,
)
from tools.behavioral_eval_runner.graders.activation import grade_activation
from tools.behavioral_eval_runner.graders.append_only import grade_version_sequence
from tools.behavioral_eval_runner.graders.approval import grade_approval_boundary
from tools.behavioral_eval_runner.graders.contract import load_contract
from tools.behavioral_eval_runner.graders.controls import (
    ControlOutcomeState,
    grade_control,
    grade_workspace_role,
)
from tools.behavioral_eval_runner.graders.mutation import (
    grade_mutations,
    grade_zero_commit_evidence,
)
from tools.behavioral_eval_runner.graders.records import (
    GraderResult,
    GraderResultState,
    GradingReasonCode,
)
from tools.behavioral_eval_runner.graders.state_machine import grade_transitions
from tools.behavioral_eval_runner.judge import policy as judge_policy
from tools.behavioral_eval_runner.judge import rubric as judge_rubric
from tools.behavioral_eval_runner.judge.envelope import (
    build_judge_envelope,
    envelope_sha256,
    render_envelope_text,
)
from tools.behavioral_eval_runner.judge.interface import (
    JudgeIdentity,
    JudgeRequest,
    JudgeResponse,
    TransportOutcome,
)
from tools.behavioral_eval_runner.judge.mock import MockJudgeClient
from tools.behavioral_eval_runner.judge.verdict import (
    StructuredVerdict,
    dispatch_mock_judgment,
    parse_judge_output,
)
from tools.behavioral_eval_runner.tests import grading_helpers as gh

RUBRIC_G = "rubric.scenario_a.coherent_topic.v1"


# --------------------------------------------------------------------------
# P1-A: trusted plan vs observed evidence
# --------------------------------------------------------------------------
class TrustedPlanSeparationTests(unittest.TestCase):
    """The eight manufactured-PASS vectors must be impossible or fail closed."""

    def test_observed_answer_id_cannot_be_added_to_the_bank(self) -> None:
        # Vector 1: the answer bank is trusted-plan data; the observation
        # mapping cannot name a bank at all.
        plan, evidence = gh.transitions_case("bad_unknown_answer")
        evidence["answer_bank_ids"] = list(plan.answer_bank["answer_ids"]) + [
            "ANS-NOT-IN-BANK"
        ]
        result = grade_transitions(plan, evidence)
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)

    def test_required_start_cannot_be_disabled_by_observation(self) -> None:
        # Vector 2.
        plan, evidence = gh.transitions_case("bad_repeated_loop_strict_start")
        evidence["required_start"] = False
        result = grade_transitions(plan, evidence)
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)

    def test_loop_threshold_cannot_be_raised_by_observation(self) -> None:
        # Vector 3.
        plan, evidence = gh.transitions_case("bad_repeated_loop")
        evidence["loop_threshold"] = 99
        result = grade_transitions(plan, evidence)
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)

    def test_owner_gate_ids_cannot_be_emptied_by_observation(self) -> None:
        # Vector 4.
        plan, evidence = gh.approval_case("bad_silent_stage_advance")
        evidence["required_gate_ids"] = []
        result = grade_approval_boundary(plan, evidence)
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)

    def test_semantic_gates_cannot_be_weakened_by_observation(self) -> None:
        # Vector 5.
        plan, evidence = gh.append_only_case("bad_forbidden_snapshot")
        evidence["semantics"] = {
            "spec_acceptance_id": "PS-006",
            "spec_owner_completion_id": "PS-007",
            "stage2_owner_ids": ["PS-007"],
            "stage3_snapshot_id": "SS-002",
            "forbidden_snapshot_ids": [],
        }
        result = grade_version_sequence(plan, evidence)
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)

    def test_activation_expectation_is_plan_data(self) -> None:
        # Vector 6.
        plan, evidence = gh.activation_case("bad_wrong_mode")
        evidence["expectation"] = {
            "target_kind": "skill",
            "target_name": "requirements-gathering-facilitator",
            "invocation_mode": "explicit_skill_invocation",
        }
        result = grade_activation(plan, evidence)
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)

    def test_expected_role_is_plan_data_not_observation(self) -> None:
        # Vector 7: the trusted expected role comes from the plan; an
        # observed claim that merely matches itself cannot manufacture PASS.
        plan, evidence = gh.workspace_role_case("bad_consumer_called_library")
        result = grade_workspace_role(plan, evidence)
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.WORKSPACE_ROLE_MISMATCH)
        evidence["expected_workspace_role"] = "source_library"
        result = grade_workspace_role(plan, evidence)
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)

    def test_plan_only_keys_inside_observed_evidence_fail_closed(self) -> None:
        # Vector 8 (generic): any plan-only key in the observation mapping is
        # malformed evidence for every grader.
        plan, evidence = gh.append_only_case("good_sequence")
        evidence["expected_final_ids"] = {"Approvals": ["(none yet)"]}
        result = grade_version_sequence(plan, evidence)
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertIs(result.reason_code, GradingReasonCode.EVIDENCE_MALFORMED)

    def test_grader_results_bind_plan_and_evidence_hashes_separately(self) -> None:
        plan, evidence = gh.transitions_case("good_linear")
        result = grade_transitions(plan, evidence)
        self.assertIs(result.result_state, GraderResultState.PASS)
        hashes = result.input_sha256s
        self.assertEqual(
            set(hashes), {"trusted_grading_plan", "observed_evidence"}
        )
        self.assertEqual(hashes["trusted_grading_plan"], plan.plan_sha256)
        self.assertNotEqual(
            hashes["trusted_grading_plan"], hashes["observed_evidence"]
        )

    def test_plan_is_typed_not_a_mapping(self) -> None:
        # A raw dict cannot impersonate the trusted plan.
        plan, evidence = gh.transitions_case("good_linear")
        with self.assertRaises((SchemaValidationError, TypeError, AttributeError)):
            grade_transitions(plan.to_dict(), evidence)  # type: ignore[arg-type]

    def test_plan_binds_the_current_contract_hash(self) -> None:
        plan, _evidence = gh.transitions_case("good_linear")
        payload = plan.to_dict()
        payload["contract_sha256"] = "0" * 64
        from tools.behavioral_eval_runner.graders.plan import TrustedGradingPlan

        with self.assertRaises(SchemaValidationError):
            TrustedGradingPlan.from_dict(payload)


class ApprovalTargetBindingTests(unittest.TestCase):
    def test_approval_for_target_a_cannot_authorize_target_b(self) -> None:
        # Approval A-REQ-1 is granted for target A; the append reuses the
        # approval ID against target B. Target B WAS previewed, so only the
        # approval-target binding can catch the reuse.
        plan, evidence = gh.approval_case("good_preview_approve_append")
        target_a = "docs/project-state.md#PS-001"
        target_b = "docs/OTHER-FILE.md#PS-999"
        evidence["events"] = [
            {"seq": 1, "kind": "PREVIEW_SHOWN", "target": target_a},
            {"seq": 2, "kind": "APPROVAL_REQUESTED", "target": target_a,
             "approval_id": "A-REQ-1"},
            {"seq": 3, "kind": "APPROVAL_GRANTED", "target": target_a,
             "approval_id": "A-REQ-1", "approver_identity": "user"},
            {"seq": 4, "kind": "PREVIEW_SHOWN", "target": target_b},
            {"seq": 5, "kind": "RECORD_APPENDED", "target": target_b,
             "approval_id": "A-REQ-1"},
        ]
        result = grade_approval_boundary(plan, evidence)
        self.assertIs(result.result_state, GraderResultState.FAIL)
        self.assertIs(result.reason_code, GradingReasonCode.APPROVAL_MISSING)


# --------------------------------------------------------------------------
# P1-B: complete required oracle sets
# --------------------------------------------------------------------------
class OracleCompletenessTests(unittest.TestCase):
    def test_contract_carries_structured_required_oracle_ids(self) -> None:
        contract = load_contract()
        for control in contract.controls:
            if control.deterministic_oracle is not None:
                self.assertTrue(
                    control.required_oracle_ids,
                    f"{control.control_id} must declare required_oracle_ids",
                )
                for oracle_id in control.required_oracle_ids:
                    self.assertNotIn(";", oracle_id)
            else:
                self.assertEqual(control.required_oracle_ids, ())

    def test_results_carry_exact_oracle_identity(self) -> None:
        plan, evidence = gh.zero_commit_case("good_zero")
        result = grade_zero_commit_evidence(plan, evidence)
        self.assertEqual(result.oracle_id, "oracle.mutation.zero_commit")
        plan, evidence = gh.mutation_case("good_clean", "SCENARIO_A_CONTROL_M")
        result = grade_mutations(plan, evidence)
        self.assertEqual(result.oracle_id, "oracle.mutation.category_scan")

    def test_control_m_requires_both_oracles(self) -> None:
        plan_m, ev_m = gh.mutation_case("good_clean", "SCENARIO_A_CONTROL_M")
        plan_z, ev_z = gh.zero_commit_case("good_zero")
        only_mutation = grade_control(
            "SCENARIO_A_CONTROL_M", [grade_mutations(plan_m, ev_m)]
        )
        self.assertIs(only_mutation.state, ControlOutcomeState.ERROR)
        only_zero = grade_control(
            "SCENARIO_A_CONTROL_M", [grade_zero_commit_evidence(plan_z, ev_z)]
        )
        self.assertIs(only_zero.state, ControlOutcomeState.ERROR)
        both = grade_control(
            "SCENARIO_A_CONTROL_M",
            [grade_mutations(plan_m, ev_m), grade_zero_commit_evidence(plan_z, ev_z)],
        )
        self.assertIs(both.state, ControlOutcomeState.PASS)

    def test_control_o_requires_both_oracles(self) -> None:
        # ONE shared trusted plan for control O feeds both of its oracles.
        shared_plan = gh.scenario_o_plan()
        _, ev_a = gh.append_only_case("good_sequence", plan=shared_plan)
        _, ev_t = gh.transitions_case("good_linear", plan=shared_plan)
        append_only = grade_control(
            "SCENARIO_A_CONTROL_O", [grade_version_sequence(shared_plan, ev_a)]
        )
        self.assertIs(append_only.state, ControlOutcomeState.ERROR)
        transitions_only = grade_control(
            "SCENARIO_A_CONTROL_O", [grade_transitions(shared_plan, ev_t)]
        )
        self.assertIs(transitions_only.state, ControlOutcomeState.ERROR)
        none_at_all = grade_control("SCENARIO_A_CONTROL_O", [])
        self.assertIs(none_at_all.state, ControlOutcomeState.ERROR)
        both = grade_control(
            "SCENARIO_A_CONTROL_O",
            [
                grade_version_sequence(shared_plan, ev_a),
                grade_transitions(shared_plan, ev_t),
            ],
        )
        self.assertIs(both.state, ControlOutcomeState.SEMANTIC_PENDING)

    def test_fabricated_oracle_results_are_unrepresentable(self) -> None:
        plan, evidence = gh.zero_commit_case("good_zero")
        genuine = grade_zero_commit_evidence(plan, evidence)
        # An invented oracle identity cannot be represented at all.
        payload = genuine.to_dict()
        payload["oracle_id"] = "oracle.invented.fake"
        payload["output_sha256"] = sha256_of_obj(
            {k: v for k, v in payload.items() if k != "output_sha256"}
        )
        with self.assertRaises(SchemaValidationError):
            GraderResult.from_dict(payload)
        # Relabeling a genuine result's oracle without recomputing its
        # content-bound hash is tamper-detected on parse.
        payload = genuine.to_dict()
        payload["oracle_id"] = "oracle.mutation.category_scan"
        with self.assertRaises(SchemaValidationError):
            GraderResult.from_dict(payload)

    def test_duplicate_oracle_is_error(self) -> None:
        plan, evidence = gh.zero_commit_case("good_zero")
        first = grade_zero_commit_evidence(plan, evidence)
        second = grade_zero_commit_evidence(plan, evidence)
        plan_m, ev_m = gh.mutation_case("good_clean", "SCENARIO_A_CONTROL_M")
        outcome = grade_control(
            "SCENARIO_A_CONTROL_M",
            [first, second, grade_mutations(plan_m, ev_m)],
        )
        self.assertIs(outcome.state, ControlOutcomeState.ERROR)

    def test_extra_unexpected_oracle_is_error(self) -> None:
        plan_p, ev_p = gh.evidence_capture_case("good_bundle")
        from tools.behavioral_eval_runner.graders.controls import (
            grade_evidence_capture,
        )

        result_p = grade_evidence_capture(plan_p, ev_p)
        plan_q, ev_q = gh.metadata_capture_case("good_metadata")
        from tools.behavioral_eval_runner.graders.controls import (
            grade_metadata_capture,
        )

        result_q_payload = grade_metadata_capture(plan_q, ev_q).to_dict()
        # Relabel the Q result as control P so the dispatcher sees an extra,
        # unexpected oracle for P.
        result_q_payload["control_id"] = "SCENARIO_A_CONTROL_P"
        result_q_payload["output_sha256"] = sha256_of_obj(
            {k: v for k, v in result_q_payload.items() if k != "output_sha256"}
        )
        outcome = grade_control(
            "SCENARIO_A_CONTROL_P",
            [result_p, GraderResult.from_dict(result_q_payload)],
        )
        self.assertIs(outcome.state, ControlOutcomeState.ERROR)

    def test_mixed_case_uids_are_error(self) -> None:
        plan_a, ev_a = gh.zero_commit_case("good_zero")
        plan_b, ev_b = gh.zero_commit_case("good_zero", case_id="other-case")
        plan_m, ev_m = gh.mutation_case("good_clean", "SCENARIO_A_CONTROL_M")
        outcome = grade_control(
            "SCENARIO_A_CONTROL_M",
            [
                grade_zero_commit_evidence(plan_a, ev_a),
                grade_mutations(plan_b, ev_m_with_case(plan_b, ev_m)),
            ],
        )
        self.assertIs(outcome.state, ControlOutcomeState.ERROR)

    def test_semantic_only_control_rejects_fabricated_deterministic_result(
        self,
    ) -> None:
        pending = grade_control("SCENARIO_A_CONTROL_G", [])
        self.assertIs(pending.state, ControlOutcomeState.SEMANTIC_PENDING)
        plan, evidence = gh.zero_commit_case("good_zero")
        genuine = grade_zero_commit_evidence(plan, evidence)
        payload = genuine.to_dict()
        payload["control_id"] = "SCENARIO_A_CONTROL_G"
        payload["output_sha256"] = sha256_of_obj(
            {k: v for k, v in payload.items() if k != "output_sha256"}
        )
        outcome = grade_control(
            "SCENARIO_A_CONTROL_G", [GraderResult.from_dict(payload)]
        )
        self.assertIs(outcome.state, ControlOutcomeState.ERROR)

    def test_outcome_carries_contract_and_plan_hashes(self) -> None:
        plan, evidence = gh.evidence_capture_case("good_bundle")
        from tools.behavioral_eval_runner.graders.controls import (
            grade_evidence_capture,
        )

        outcome = grade_control(
            "SCENARIO_A_CONTROL_P", [grade_evidence_capture(plan, evidence)]
        )
        self.assertIs(outcome.state, ControlOutcomeState.PASS)
        self.assertEqual(outcome.contract_sha256, load_contract().contract_hash())
        self.assertEqual(outcome.trusted_grading_plan_sha256, plan.plan_sha256)


def ev_m_with_case(plan, evidence):
    """Helper: mutation evidence is case-free; the plan carries the case."""
    return evidence


# --------------------------------------------------------------------------
# P1-C: judge request / envelope / control context / mock binding
# --------------------------------------------------------------------------
class JudgeBindingTestBase(unittest.TestCase):
    CONTROL = "SCENARIO_A_CONTROL_G"

    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory(prefix="wp2b2-r2-bind-")
        self.addCleanup(tmp.cleanup)
        self.root = os.path.join(tmp.name, "bundle")
        writer = EvidenceWriter(self.root, run_id="run-r2")
        writer.finalize_input_evidence(
            [EvidenceArtifact("transcript.txt", b"one topic", ArtifactMetadata())]
        )
        self.gate = JudgeInputGate(self.root)
        self.gate.verify()
        self.envelope = build_judge_envelope(
            rubric_ref=RUBRIC_G,
            gate=self.gate,
            artifact_keys={"transcript": "transcript.txt"},
            control_id=self.CONTROL,
        )

    def request_for(self, envelope, request_id: str = "req-r2") -> JudgeRequest:
        rubric = judge_rubric.get_rubric(RUBRIC_G)
        identity = JudgeIdentity(
            judge_id="pinned-judge-placeholder",
            judge_version="0.0.0-unpinned",
            model_identifier="DATA-ONLY",
            provider_identifier="DATA-ONLY",
            policy_version=judge_policy.JUDGE_POLICY_VERSION,
            policy_sha256=judge_policy.policy_sha256(),
        )
        return JudgeRequest(
            request_id=request_id,
            control_id=self.CONTROL,
            judge=identity,
            rubric_id=rubric["rubric_id"],
            rubric_version=rubric["rubric_version"],
            rubric_sha256=judge_rubric.rubric_sha256(rubric),
            envelope_sha256=envelope_sha256(envelope),
            input_manifest_sha256=envelope["input_manifest_sha256"],
        )

    def good_verdict_response(self, request: JudgeRequest) -> JudgeResponse:
        payload = {
            "verdict_id": "r2-verdict-1",
            "request_id": request.request_id,
            "control_id": request.control_id,
            "verdict": "PASS",
            "failure_mode": None,
            "offending_span": None,
            "reason_code": "MEETS_RUBRIC",
            "evidence_refs": ["transcript"],
            "rubric_id": request.rubric_id,
            "rubric_version": request.rubric_version,
            "rubric_sha256": request.rubric_sha256,
            "judge_id": request.judge.judge_id,
            "judge_version": request.judge.judge_version,
            "input_manifest_sha256": request.input_manifest_sha256,
            "schema_version": request.schema_version,
        }
        return JudgeResponse(
            request_id=request.request_id,
            response_id="r2-resp-1",
            transport_outcome=TransportOutcome.OK,
            raw_output=json.dumps(payload),
        )


class JudgeBindingTests(JudgeBindingTestBase):
    def test_envelope_carries_trusted_control_context(self) -> None:
        context = self.envelope["control_context"]
        contract = load_contract()
        control = next(
            c for c in contract.controls if c.control_id == self.CONTROL
        )
        self.assertEqual(context["control_id"], self.CONTROL)
        self.assertEqual(context["requirement"], control.requirement)
        self.assertEqual(context["classification"], control.classification.value)
        self.assertEqual(context["semantic_rubric_ref"], control.semantic_rubric_ref)
        self.assertEqual(context["contract_sha256"], contract.contract_hash())
        self.assertEqual(context["d9_signoff_state"], "PENDING_OWNER_DECISION")

    def test_rubric_must_match_the_controls_contract_rubric(self) -> None:
        with self.assertRaises(SchemaValidationError):
            build_judge_envelope(
                rubric_ref="rubric.scenario_a.control_semantics.v1",
                gate=self.gate,
                artifact_keys={"transcript": "transcript.txt"},
                control_id=self.CONTROL,
            )

    def test_rendered_envelope_includes_requirement_and_criteria(self) -> None:
        text = render_envelope_text(self.envelope)
        rubric = judge_rubric.get_rubric(RUBRIC_G)
        control = next(
            c for c in load_contract().controls if c.control_id == self.CONTROL
        )
        self.assertIn(control.requirement, text)
        for criterion in rubric["pass_criteria"]:
            self.assertIn(criterion, text)
        for criterion in rubric["fail_criteria"]:
            self.assertIn(criterion, text)

    def test_mock_dispatch_requires_matching_envelope_bytes(self) -> None:
        request = self.request_for(self.envelope)
        client = MockJudgeClient(
            {request.request_id: self.good_verdict_response(request)}
        )
        other_envelope = dict(self.envelope)
        other_envelope["untrusted_data"] = {
            "transcript": {
                "encoding": "utf-8",
                "content_b64": "c3dhcHBlZA==",
            }
        }
        response = client.dispatch(request, canonical_bytes(other_envelope))
        self.assertIsNot(response.transport_outcome, TransportOutcome.OK)

    def test_dispatch_mock_judgment_binds_before_lookup(self) -> None:
        request = self.request_for(self.envelope)
        client = MockJudgeClient(
            {request.request_id: self.good_verdict_response(request)}
        )
        good = dispatch_mock_judgment(client, request, self.envelope)
        self.assertTrue(good.is_verdict)

        tampered = dict(self.envelope)
        tampered["policy_sha256"] = "0" * 64
        outcome = dispatch_mock_judgment(client, request, tampered)
        self.assertFalse(outcome.is_verdict)

    def test_request_manifest_mismatch_fails_closed(self) -> None:
        request = self.request_for(self.envelope)
        payload = request.to_dict()
        payload["input_manifest_sha256"] = "1" * 64
        bad_request = JudgeRequest.from_dict(payload)
        client = MockJudgeClient(
            {bad_request.request_id: self.good_verdict_response(bad_request)}
        )
        outcome = dispatch_mock_judgment(client, bad_request, self.envelope)
        self.assertFalse(outcome.is_verdict)

    def test_rubric_mismatch_fails_closed(self) -> None:
        request = self.request_for(self.envelope)
        payload = request.to_dict()
        payload["rubric_sha256"] = "2" * 64
        bad_request = JudgeRequest.from_dict(payload)
        client = MockJudgeClient(
            {bad_request.request_id: self.good_verdict_response(bad_request)}
        )
        outcome = dispatch_mock_judgment(client, bad_request, self.envelope)
        self.assertFalse(outcome.is_verdict)

    def test_control_id_mismatch_fails_closed(self) -> None:
        request = self.request_for(self.envelope)
        payload = request.to_dict()
        payload["control_id"] = "SCENARIO_A_CONTROL_I"
        bad_request = JudgeRequest.from_dict(payload)
        client = MockJudgeClient(
            {bad_request.request_id: self.good_verdict_response(bad_request)}
        )
        outcome = dispatch_mock_judgment(client, bad_request, self.envelope)
        self.assertFalse(outcome.is_verdict)

    def test_contract_hash_mismatch_fails_closed(self) -> None:
        request = self.request_for(self.envelope)
        tampered = dict(self.envelope)
        tampered_context = dict(tampered["control_context"])
        tampered_context["contract_sha256"] = "3" * 64
        tampered["control_context"] = tampered_context
        client = MockJudgeClient(
            {request.request_id: self.good_verdict_response(request)}
        )
        outcome = dispatch_mock_judgment(client, request, tampered)
        self.assertFalse(outcome.is_verdict)

    def test_two_envelopes_one_request_id_cannot_both_bind(self) -> None:
        request = self.request_for(self.envelope)
        writer_root = os.path.join(os.path.dirname(self.root), "bundle2")
        writer = EvidenceWriter(writer_root, run_id="run-r2b")
        writer.finalize_input_evidence(
            [EvidenceArtifact("transcript.txt", b"different", ArtifactMetadata())]
        )
        gate2 = JudgeInputGate(writer_root)
        gate2.verify()
        envelope2 = build_judge_envelope(
            rubric_ref=RUBRIC_G,
            gate=gate2,
            artifact_keys={"transcript": "transcript.txt"},
            control_id=self.CONTROL,
        )
        client = MockJudgeClient(
            {request.request_id: self.good_verdict_response(request)}
        )
        outcome = dispatch_mock_judgment(client, request, envelope2)
        self.assertFalse(outcome.is_verdict)

    def test_binding_rejects_tampered_control_context_content(self) -> None:
        # Review F2: the binding validator re-derives the control context and
        # rubric body from the trusted sources — a hand-built envelope with a
        # substituted requirement or criteria cannot bind, even with the
        # correct contract hash.
        # The attacker controls BOTH the hand-built envelope and its request,
        # so the request hash-binds the tampered envelope; only content
        # re-derivation from the trusted sources can reject it.
        tampered = dict(self.envelope)
        context = dict(tampered["control_context"])
        context["requirement"] = "Substituted requirement the judge never saw."
        tampered["control_context"] = context
        request = self.request_for(tampered)
        client = MockJudgeClient(
            {request.request_id: self.good_verdict_response(request)}
        )
        outcome = dispatch_mock_judgment(client, request, tampered)
        self.assertFalse(outcome.is_verdict)

        tampered = dict(self.envelope)
        rubric = dict(tampered["rubric"])
        rubric["fail_criteria"] = ["anything at all"]
        tampered["rubric"] = rubric
        request = self.request_for(tampered)
        client = MockJudgeClient(
            {request.request_id: self.good_verdict_response(request)}
        )
        outcome = dispatch_mock_judgment(client, request, tampered)
        self.assertFalse(outcome.is_verdict)

    def test_verdict_evidence_refs_come_from_the_actual_envelope(self) -> None:
        request = self.request_for(self.envelope)
        response = self.good_verdict_response(request)
        payload = json.loads(response.raw_output)
        payload["evidence_refs"] = ["recording_evidence"]  # not in this envelope
        response = JudgeResponse(
            request_id=request.request_id,
            response_id="r2-resp-2",
            transport_outcome=TransportOutcome.OK,
            raw_output=json.dumps(payload),
        )
        outcome = parse_judge_output(response, request, self.envelope)
        self.assertFalse(outcome.is_verdict)


# --------------------------------------------------------------------------
# P1-D: CLI evidence boundary
# --------------------------------------------------------------------------
class CliEnvelopeBoundaryTests(unittest.TestCase):
    def _run_cli(self, argv):
        from tools.behavioral_eval_runner.cli import main

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = main(argv)
        return code, stdout.getvalue()

    def test_cli_emits_metadata_only(self) -> None:
        secret = "SECRET-TRANSCRIPT-CONTENT one topic"
        with tempfile.TemporaryDirectory(prefix="wp2b2-r2-cli-") as tmp:
            root = os.path.join(tmp, "bundle")
            writer = EvidenceWriter(root, run_id="run-r2-cli")
            writer.finalize_input_evidence(
                [
                    EvidenceArtifact(
                        "transcript.txt", secret.encode("utf-8"), ArtifactMetadata()
                    )
                ]
            )
            code, output = self._run_cli(
                [
                    "build-judge-envelope",
                    "--root",
                    root,
                    "--rubric",
                    RUBRIC_G,
                    "--control",
                    "SCENARIO_A_CONTROL_G",
                    "--map",
                    "transcript=transcript.txt",
                ]
            )
        self.assertEqual(code, 0)
        self.assertNotIn(secret, output)
        self.assertNotIn("content_b64", output)
        import base64

        self.assertNotIn(
            base64.b64encode(secret.encode("utf-8")).decode("ascii"), output
        )
        payload = json.loads(output)
        self.assertEqual(len(payload["envelope_sha256"]), 64)
        self.assertEqual(payload["evidence_keys"], ["transcript"])
        self.assertFalse(payload["dispatched"])
        self.assertIn("contract_sha256", payload)

    def test_arbitrary_out_path_no_longer_exists(self) -> None:
        from tools.behavioral_eval_runner.cli import main

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            with self.assertRaises(SystemExit):
                main(
                    [
                        "build-judge-envelope",
                        "--root",
                        "irrelevant",
                        "--rubric",
                        RUBRIC_G,
                        "--control",
                        "SCENARIO_A_CONTROL_G",
                        "--map",
                        "transcript=transcript.txt",
                        "--out",
                        "C:\\anywhere\\envelope.json",
                    ]
                )
        self.assertIn("--out", stderr.getvalue())


# --------------------------------------------------------------------------
# P2-E: strict parsers and closed control IDs
# --------------------------------------------------------------------------
class StrictParserTests(unittest.TestCase):
    def _verdict_payload(self, **overrides):
        from tools.behavioral_eval_runner import GRADING_SCHEMA_VERSION

        payload = {
            "verdict_id": "r2-v-1",
            "request_id": "req-1",
            "control_id": "SCENARIO_A_CONTROL_G",
            "verdict": "PASS",
            "failure_mode": None,
            "offending_span": None,
            "reason_code": "MEETS_RUBRIC",
            "evidence_refs": ["transcript"],
            "rubric_id": "rubric.scenario_a.coherent_topic.v1",
            "rubric_version": "1.0.0-wp2b2",
            "rubric_sha256": "a" * 64,
            "judge_id": "j",
            "judge_version": "1",
            "input_manifest_sha256": "b" * 64,
            "schema_version": GRADING_SCHEMA_VERSION,
        }
        payload.update(overrides)
        return payload

    def test_string_never_becomes_a_tuple_of_characters(self) -> None:
        with self.assertRaises(SchemaValidationError):
            StructuredVerdict.from_dict(
                self._verdict_payload(evidence_refs="transcript")
            )
        plan, evidence = gh.zero_commit_case("good_zero")
        payload = grade_zero_commit_evidence(plan, evidence).to_dict()
        payload["evidence_pointers"] = "fixture:pointer"
        with self.assertRaises(SchemaValidationError):
            GraderResult.from_dict(payload)
        from tools.behavioral_eval_runner.judge.calibration import CalibrationEntry

        with self.assertRaises(SchemaValidationError):
            CalibrationEntry.from_dict(
                {
                    "entry_id": "e1",
                    "control_id": "SCENARIO_A_CONTROL_G",
                    "risk_class": "STANDARD",
                    "expected_label": "PASS",
                    "input_artifact_refs": "transcript",
                    "split": "TRAIN",
                    "assertion_uid": None,
                }
            )
        from tools.behavioral_eval_runner.graders.contract import ScenarioAControl

        control_payload = load_contract().controls[0].to_dict()
        control_payload["required_evidence"] = "recorded evidence"
        with self.assertRaises(SchemaValidationError):
            ScenarioAControl.from_dict(control_payload)

    def test_control_ids_are_closed_everywhere(self) -> None:
        with self.assertRaises(SchemaValidationError):
            StructuredVerdict.from_dict(
                self._verdict_payload(control_id="CONTROL_Z")
            )
        from tools.behavioral_eval_runner.judge.calibration import CalibrationEntry

        with self.assertRaises(SchemaValidationError):
            CalibrationEntry.from_dict(
                {
                    "entry_id": "e1",
                    "control_id": "NOT_A_CONTROL",
                    "risk_class": "STANDARD",
                    "expected_label": "PASS",
                    "input_artifact_refs": ["transcript"],
                    "split": "TRAIN",
                    "assertion_uid": None,
                }
            )
        identity = JudgeIdentity(
            judge_id="j",
            judge_version="1",
            model_identifier="DATA-ONLY",
            provider_identifier="DATA-ONLY",
            policy_version=judge_policy.JUDGE_POLICY_VERSION,
            policy_sha256=judge_policy.policy_sha256(),
        )
        with self.assertRaises(SchemaValidationError):
            JudgeRequest(
                request_id="r",
                control_id="CONTROL_Z",
                judge=identity,
                rubric_id="rubric.scenario_a.coherent_topic.v1",
                rubric_version="1.0.0-wp2b2",
                rubric_sha256="a" * 64,
                envelope_sha256="b" * 64,
                input_manifest_sha256="c" * 64,
            ).validate()

    def test_schemas_carry_cross_field_rules(self) -> None:
        from tools.behavioral_eval_runner.cli import load_schema

        result_schema = load_schema("grader-result.schema.json")
        self.assertIn("allOf", result_schema)
        verdict_schema = load_schema("judge-verdict.schema.json")
        self.assertIn("allOf", verdict_schema)
        request_schema = load_schema("judge-request.schema.json")
        self.assertIn("allOf", request_schema)
        self.assertIn(
            "^SCENARIO_A_CONTROL_[A-Q]$",
            json.dumps(request_schema) + json.dumps(verdict_schema),
        )
        # Review F3: calibration entries carry the closed control pattern too.
        dataset_schema = load_schema("calibration-dataset.schema.json")
        self.assertEqual(
            dataset_schema["properties"]["entries"]["items"]["properties"][
                "control_id"
            ]["pattern"],
            "^SCENARIO_A_CONTROL_[A-Q]$",
        )
        # Review F5: the FAIL/ERROR branch REQUIRES reason_code to be present
        # (draft-07 `properties` alone does not apply to absent members).
        fail_clause = result_schema["allOf"][1]["then"]
        self.assertIn("reason_code", fail_clause.get("required", []))
        for clause in request_schema["allOf"]:
            self.assertTrue(clause["then"].get("required"))

    def test_plan_schema_is_bound_and_key_complete(self) -> None:
        # Review F4: the plan schema is loaded, key-complete against the
        # runtime record, and closes expected_final_ids to the ID sections.
        from tools.behavioral_eval_runner.cli import load_schema
        from tools.behavioral_eval_runner.graders.plan import TrustedGradingPlan

        schema = load_schema("scenario-a-grading-plan.schema.json")
        self.assertEqual(set(schema["properties"]), set(TrustedGradingPlan._KEYS))
        final_ids = schema["properties"]["expected_final_ids"]["anyOf"][1]
        self.assertFalse(final_ids["additionalProperties"])
        self.assertEqual(
            set(final_ids["properties"]),
            {"State snapshots", "Decision log", "Approvals"},
        )

    def test_malformed_evidence_detail_never_echoes_content(self) -> None:
        # Review F6: fail-closed diagnostics report the key and TYPE of a
        # malformed value, never its content (no transcript echo channel).
        plan, evidence = gh.questionnaire_case("good_single_question")
        evidence["turn_text"] = ["SECRET transcript line"]
        from tools.behavioral_eval_runner.graders.controls import (
            grade_questionnaire_dump,
        )

        result = grade_questionnaire_dump(plan, evidence)
        self.assertIs(result.result_state, GraderResultState.ERROR)
        self.assertNotIn("SECRET", json.dumps(result.to_dict()))


if __name__ == "__main__":
    unittest.main()
