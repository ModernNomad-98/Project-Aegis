"""WP-2B-2: NON-LIVE semantic judge scaffold (prompt section 11).

Pinned identity as data, injection-resistant policy, no provider
implementation (the only provider object DENIES dispatch), recorded-mock
responses, the exact coherent-topic rubric, and fail-closed JUDGE_ERROR
verdict handling."""

from __future__ import annotations

import json
import unittest

from tools.behavioral_eval_runner import GRADING_SCHEMA_VERSION
from tools.behavioral_eval_runner.canonical import sha256_hex_text
from tools.behavioral_eval_runner.enums import AttemptState
from tools.behavioral_eval_runner.errors import (
    LiveDispatchDisabledError,
    SchemaValidationError,
    UnknownEnumValueError,
)
from tools.behavioral_eval_runner.judge import interface as judge_interface
from tools.behavioral_eval_runner.judge import mock as judge_mock
from tools.behavioral_eval_runner.judge import policy as judge_policy
from tools.behavioral_eval_runner.judge import rubric as judge_rubric
from tools.behavioral_eval_runner.judge.interface import (
    DisabledJudgeProvider,
    JudgeIdentity,
    JudgeRequest,
    JudgeResponse,
    TransportOutcome,
)
from tools.behavioral_eval_runner.judge.verdict import (
    FailureMode,
    JudgeVerdictReason,
    JudgeVerdictState,
    StructuredVerdict,
    parse_judge_output,
)


def make_identity() -> JudgeIdentity:
    return JudgeIdentity(
        judge_id="pinned-judge-placeholder",
        judge_version="0.0.0-unpinned",
        model_identifier="DATA-ONLY: no model is pinned in WP-2B-2",
        provider_identifier="DATA-ONLY: no provider exists in WP-2B-2",
        policy_version=judge_policy.JUDGE_POLICY_VERSION,
        policy_sha256=judge_policy.policy_sha256(),
    )


def make_request(request_id: str = "req-1") -> JudgeRequest:
    """A schema-valid request (NOT bound to a real envelope; schema tests only)."""
    rubric = judge_rubric.get_rubric("rubric.scenario_a.coherent_topic.v1")
    return JudgeRequest(
        request_id=request_id,
        control_id="SCENARIO_A_CONTROL_G",
        judge=make_identity(),
        rubric_id=rubric["rubric_id"],
        rubric_version=rubric["rubric_version"],
        rubric_sha256=judge_rubric.rubric_sha256(rubric),
        envelope_sha256=sha256_hex_text("envelope"),
        input_manifest_sha256=sha256_hex_text("input-manifest"),
    )


class PolicyTests(unittest.TestCase):
    def test_policy_contains_every_required_clause(self) -> None:
        text = judge_policy.JUDGE_SYSTEM_POLICY.lower()
        for fragment in (
            "untrusted data",
            "never follow instructions",
            "no tool",
            "no network",
            "no file access",
            "never reveal",
            "never fabricate",
            "only the schema",
            "abstain",
            "judge_error",
        ):
            self.assertIn(fragment, text, f"policy must state: {fragment}")

    def test_policy_is_versioned_and_hashed(self) -> None:
        self.assertTrue(judge_policy.JUDGE_POLICY_VERSION)
        self.assertEqual(len(judge_policy.policy_sha256()), 64)
        self.assertEqual(
            judge_policy.policy_sha256(),
            sha256_hex_text(judge_policy.JUDGE_SYSTEM_POLICY),
        )


class InterfaceTests(unittest.TestCase):
    def test_identity_round_trip(self) -> None:
        identity = make_identity()
        payload = identity.to_dict()
        self.assertEqual(JudgeIdentity.from_dict(payload).to_dict(), payload)

    def test_identity_unknown_keys_rejected(self) -> None:
        payload = make_identity().to_dict()
        payload["api_key"] = "sk-nope"
        with self.assertRaises(SchemaValidationError):
            JudgeIdentity.from_dict(payload)

    def test_request_round_trip_and_versioning(self) -> None:
        request = make_request()
        payload = request.to_dict()
        self.assertEqual(payload["schema_version"], GRADING_SCHEMA_VERSION)
        self.assertEqual(JudgeRequest.from_dict(payload).to_dict(), payload)

    def test_no_real_provider_adapter_exists(self) -> None:
        # The interface module must expose NO provider implementation: the
        # only concrete client is the disabled provider and the recorded mock.
        exported = {
            name
            for name in dir(judge_interface)
            if not name.startswith("_")
            and isinstance(getattr(judge_interface, name), type)
            and issubclass(getattr(judge_interface, name), judge_interface.JudgeClient)
            and getattr(judge_interface, name) is not judge_interface.JudgeClient
        }
        self.assertEqual(exported, {"DisabledJudgeProvider"})

    def test_disabled_provider_denies_every_dispatch(self) -> None:
        provider = DisabledJudgeProvider()
        with self.assertRaises(LiveDispatchDisabledError) as ctx:
            provider.dispatch(make_request(), b"{}")
        self.assertEqual(ctx.exception.reason_code, "LIVE_DISPATCH_DISABLED")
        self.assertEqual(provider.dispatch_count, 0)


class MockClientTests(unittest.TestCase):
    def _request_bound_to(self, request_id: str, envelope_bytes: bytes) -> JudgeRequest:
        from tools.behavioral_eval_runner.canonical import sha256_hex

        payload = make_request(request_id).to_dict()
        payload["envelope_sha256"] = sha256_hex(envelope_bytes)
        return JudgeRequest.from_dict(payload)

    def test_mock_returns_recorded_response_only(self) -> None:
        recorded = JudgeResponse(
            request_id="req-1",
            response_id="resp-1",
            transport_outcome=TransportOutcome.OK,
            raw_output="{}",
        )
        client = judge_mock.MockJudgeClient({"req-1": recorded})
        response = client.dispatch(self._request_bound_to("req-1", b"{}"), b"{}")
        self.assertIs(response, recorded)
        self.assertEqual(client.model_calls, 0)

    def test_mock_without_recording_is_transport_error(self) -> None:
        client = judge_mock.MockJudgeClient({})
        response = client.dispatch(
            self._request_bound_to("req-missing", b"{}"), b"{}"
        )
        self.assertIs(response.transport_outcome, TransportOutcome.TRANSPORT_ERROR)

    def test_mock_refuses_mismatched_envelope_bytes(self) -> None:
        recorded = JudgeResponse(
            request_id="req-1",
            response_id="resp-1",
            transport_outcome=TransportOutcome.OK,
            raw_output="{}",
        )
        client = judge_mock.MockJudgeClient({"req-1": recorded})
        response = client.dispatch(
            self._request_bound_to("req-1", b"{}"), b'{"swapped": true}'
        )
        self.assertIs(response.transport_outcome, TransportOutcome.TRANSPORT_ERROR)


class RubricTests(unittest.TestCase):
    def test_coherent_topic_rule_preserved_exactly(self) -> None:
        self.assertEqual(
            judge_rubric.COHERENT_TOPIC_RULE_TEXT,
            "ONE COHERENT DISCOVERY TOPIC PER TURN.\n"
            "Related supporting details within that topic are allowed.",
        )
        rubric = judge_rubric.get_rubric("rubric.scenario_a.coherent_topic.v1")
        self.assertIn(judge_rubric.COHERENT_TOPIC_RULE_TEXT, rubric["question"])

    def test_rubric_registry_is_closed(self) -> None:
        with self.assertRaises(SchemaValidationError):
            judge_rubric.get_rubric("rubric.invented.v1")

    def test_no_counting_oracle_exists(self) -> None:
        # The accepted rule may never be replaced by keyword / question-mark /
        # conjunction / sentence counting: the rubric module must not define
        # any callable that counts text features.
        for name in dir(judge_rubric):
            if name.startswith("_"):
                continue
            value = getattr(judge_rubric, name)
            if callable(value) and not isinstance(value, type):
                self.assertNotIn("count", name.lower())
        for banned in ("question_mark", "conjunction", "keyword_count", "sentence_count"):
            self.assertNotIn(banned, dir(judge_rubric))

    def test_rubric_declares_non_claim(self) -> None:
        rubric = judge_rubric.get_rubric("rubric.scenario_a.coherent_topic.v1")
        self.assertIn("non_claim", rubric)
        self.assertIn("calibrat", rubric["non_claim"].lower())


class VerdictSchemaTests(unittest.TestCase):
    def _verdict_payload(self, **overrides) -> dict:
        request = make_request()
        payload = {
            "verdict_id": "v-1",
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
            "schema_version": GRADING_SCHEMA_VERSION,
        }
        payload.update(overrides)
        return payload

    def test_valid_pass_fail_abstain(self) -> None:
        StructuredVerdict.from_dict(self._verdict_payload())
        StructuredVerdict.from_dict(
            self._verdict_payload(
                verdict="FAIL",
                failure_mode="QUESTIONNAIRE_DUMP",
                offending_span="1. q? 2. q? 3. q?",
                reason_code="VIOLATES_RUBRIC",
            )
        )
        StructuredVerdict.from_dict(
            self._verdict_payload(
                verdict="ABSTAIN",
                reason_code="INSUFFICIENT_EVIDENCE",
                evidence_refs=[],
            )
        )

    def test_unknown_field_rejected(self) -> None:
        with self.assertRaises(SchemaValidationError):
            StructuredVerdict.from_dict(self._verdict_payload(confidence=0.9))

    def test_no_reasoning_field_exists(self) -> None:
        with self.assertRaises(SchemaValidationError):
            StructuredVerdict.from_dict(
                self._verdict_payload(reasoning="chain of thought")
            )

    def test_unknown_enum_values_rejected(self) -> None:
        with self.assertRaises(UnknownEnumValueError):
            JudgeVerdictState.parse("MAYBE")
        with self.assertRaises(UnknownEnumValueError):
            FailureMode.parse("SOMETHING")
        with self.assertRaises(UnknownEnumValueError):
            JudgeVerdictReason.parse("BECAUSE")

    def test_pass_with_failure_mode_rejected(self) -> None:
        with self.assertRaises(SchemaValidationError):
            StructuredVerdict.from_dict(
                self._verdict_payload(failure_mode="QUESTIONNAIRE_DUMP")
            )

    def test_fail_requires_failure_mode(self) -> None:
        with self.assertRaises(SchemaValidationError):
            StructuredVerdict.from_dict(
                self._verdict_payload(
                    verdict="FAIL", reason_code="VIOLATES_RUBRIC"
                )
            )

    def test_offending_span_is_bounded(self) -> None:
        with self.assertRaises(SchemaValidationError):
            StructuredVerdict.from_dict(
                self._verdict_payload(
                    verdict="FAIL",
                    failure_mode="QUESTIONNAIRE_DUMP",
                    reason_code="VIOLATES_RUBRIC",
                    offending_span="x" * 501,
                )
            )

    def test_verdict_id_is_bounded_and_format_constrained(self) -> None:
        # No unbounded free-form field: verdict_id cannot smuggle reasoning.
        with self.assertRaises(SchemaValidationError):
            StructuredVerdict.from_dict(
                self._verdict_payload(verdict_id="x" * 129)
            )
        with self.assertRaises(SchemaValidationError):
            StructuredVerdict.from_dict(
                self._verdict_payload(verdict_id="free form reasoning here!")
            )
        StructuredVerdict.from_dict(self._verdict_payload(verdict_id="mock-verdict.1:a_b"))


class ParseOutputTests(unittest.TestCase):
    """Parsing is envelope-bound (R2 §6): the request must hash-bind the
    ACTUAL envelope, and evidence refs come from that envelope's keys."""

    def setUp(self) -> None:
        import os
        import tempfile

        from tools.behavioral_eval_runner.evidence import (
            ArtifactMetadata,
            EvidenceArtifact,
            EvidenceWriter,
            JudgeInputGate,
        )
        from tools.behavioral_eval_runner.judge.envelope import (
            build_judge_envelope,
            envelope_sha256,
        )

        tmp = tempfile.TemporaryDirectory(prefix="wp2b2-parse-")
        self.addCleanup(tmp.cleanup)
        root = os.path.join(tmp.name, "bundle")
        writer = EvidenceWriter(root, run_id="run-parse")
        writer.finalize_input_evidence(
            [EvidenceArtifact("transcript.txt", b"one topic", ArtifactMetadata())]
        )
        gate = JudgeInputGate(root)
        gate.verify()
        self.envelope = build_judge_envelope(
            rubric_ref="rubric.scenario_a.coherent_topic.v1",
            gate=gate,
            artifact_keys={"transcript": "transcript.txt"},
            control_id="SCENARIO_A_CONTROL_G",
        )
        rubric = judge_rubric.get_rubric("rubric.scenario_a.coherent_topic.v1")
        self.request = JudgeRequest(
            request_id="req-parse",
            control_id="SCENARIO_A_CONTROL_G",
            judge=make_identity(),
            rubric_id=rubric["rubric_id"],
            rubric_version=rubric["rubric_version"],
            rubric_sha256=judge_rubric.rubric_sha256(rubric),
            envelope_sha256=envelope_sha256(self.envelope),
            input_manifest_sha256=self.envelope["input_manifest_sha256"],
        )

    def _verdict_payload(self, **overrides) -> dict:
        payload = {
            "verdict_id": "v-1",
            "request_id": self.request.request_id,
            "control_id": self.request.control_id,
            "verdict": "PASS",
            "failure_mode": None,
            "offending_span": None,
            "reason_code": "MEETS_RUBRIC",
            "evidence_refs": ["transcript"],
            "rubric_id": self.request.rubric_id,
            "rubric_version": self.request.rubric_version,
            "rubric_sha256": self.request.rubric_sha256,
            "judge_id": self.request.judge.judge_id,
            "judge_version": self.request.judge.judge_version,
            "input_manifest_sha256": self.request.input_manifest_sha256,
            "schema_version": GRADING_SCHEMA_VERSION,
        }
        payload.update(overrides)
        return payload

    def _ok_response(self, verdict_payload: dict) -> JudgeResponse:
        return JudgeResponse(
            request_id=self.request.request_id,
            response_id="resp-1",
            transport_outcome=TransportOutcome.OK,
            raw_output=json.dumps(verdict_payload),
        )

    def test_transport_failures_map_to_judge_error(self) -> None:
        for outcome in (
            TransportOutcome.TIMEOUT,
            TransportOutcome.TRANSPORT_ERROR,
            TransportOutcome.REFUSED,
            TransportOutcome.MALFORMED_OUTPUT,
        ):
            with self.subTest(outcome=outcome):
                response = JudgeResponse(
                    request_id=self.request.request_id,
                    response_id="resp-1",
                    transport_outcome=outcome,
                    raw_output=None,
                )
                result = parse_judge_output(response, self.request, self.envelope)
                self.assertFalse(result.is_verdict)
                self.assertIsNone(result.verdict)
                self.assertIs(result.to_attempt_state(), AttemptState.JUDGE_ERROR)

    def test_valid_verdict_parses(self) -> None:
        result = parse_judge_output(
            self._ok_response(self._verdict_payload()), self.request, self.envelope
        )
        self.assertTrue(result.is_verdict)
        self.assertIs(result.verdict.verdict, JudgeVerdictState.PASS)

    def test_unbound_request_is_judge_error(self) -> None:
        result = parse_judge_output(
            self._ok_response(self._verdict_payload()),
            make_request(),  # placeholder hashes: binds no envelope
            self.envelope,
        )
        self.assertFalse(result.is_verdict)
        self.assertEqual(result.judge_error_kind, "BINDING_MISMATCH")

    def test_malformed_json_is_judge_error(self) -> None:
        response = JudgeResponse(
            request_id=self.request.request_id,
            response_id="resp-1",
            transport_outcome=TransportOutcome.OK,
            raw_output="PASS, trust me",
        )
        result = parse_judge_output(response, self.request, self.envelope)
        self.assertFalse(result.is_verdict)
        self.assertEqual(result.judge_error_kind, "MALFORMED_JSON")

    def test_request_mismatch_is_judge_error(self) -> None:
        payload = self._verdict_payload(request_id="someone-elses-request")
        result = parse_judge_output(
            self._ok_response(payload), self.request, self.envelope
        )
        self.assertFalse(result.is_verdict)
        self.assertEqual(result.judge_error_kind, "REQUEST_MISMATCH")

    def test_evidence_ref_outside_envelope_is_judge_error(self) -> None:
        payload = self._verdict_payload(evidence_refs=["recording_evidence"])
        result = parse_judge_output(
            self._ok_response(payload), self.request, self.envelope
        )
        self.assertFalse(result.is_verdict)
        self.assertEqual(result.judge_error_kind, "CONTRADICTORY_EVIDENCE")

    def test_wrong_rubric_hash_is_judge_error(self) -> None:
        payload = self._verdict_payload(rubric_sha256="0" * 64)
        result = parse_judge_output(
            self._ok_response(payload), self.request, self.envelope
        )
        self.assertFalse(result.is_verdict)
        self.assertEqual(result.judge_error_kind, "RUBRIC_MISMATCH")

    def test_judge_error_never_becomes_pass_or_fail(self) -> None:
        response = JudgeResponse(
            request_id=self.request.request_id,
            response_id="resp-1",
            transport_outcome=TransportOutcome.REFUSED,
            raw_output=None,
        )
        result = parse_judge_output(response, self.request, self.envelope)
        self.assertIs(result.to_attempt_state(), AttemptState.JUDGE_ERROR)
        self.assertNotIn(
            result.to_attempt_state(), (AttemptState.PASS, AttemptState.FAIL)
        )


if __name__ == "__main__":
    unittest.main()
