"""WP-2B-2: injection-defense tests over recorded synthetic fixtures
(prompt 11.F). No actual model call occurs anywhere in this module."""

from __future__ import annotations

import base64
import json
import os
import tempfile
import unittest

from tools.behavioral_eval_runner.evidence import (
    ArtifactMetadata,
    EvidenceArtifact,
    EvidenceWriter,
    JudgeInputGate,
)
from tools.behavioral_eval_runner.judge import policy as judge_policy
from tools.behavioral_eval_runner.judge import rubric as judge_rubric
from tools.behavioral_eval_runner.judge.envelope import (
    ENVELOPE_BEGIN,
    ENVELOPE_END,
    build_judge_envelope,
    envelope_sha256,
    extract_untrusted_data,
    render_envelope_text,
)
from tools.behavioral_eval_runner.judge.interface import (
    JudgeIdentity,
    JudgeRequest,
    JudgeResponse,
    TransportOutcome,
)
from tools.behavioral_eval_runner.judge.verdict import parse_judge_output
from tools.behavioral_eval_runner.tests.grading_helpers import load_fixture

RUBRIC_REF = "rubric.scenario_a.coherent_topic.v1"


def _attack_payloads() -> dict[str, str]:
    fixture = load_fixture("injection_suite.json")
    attacks = dict(fixture["attacks"])
    attacks["overlong_content"] = attacks["overlong_content"] * int(
        fixture["overlong_repeat"]
    )
    return attacks


def _request_for(envelope: dict, request_id: str = "req-inj") -> JudgeRequest:
    rubric = judge_rubric.get_rubric(RUBRIC_REF)
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
        control_id="SCENARIO_A_CONTROL_G",
        judge=identity,
        rubric_id=rubric["rubric_id"],
        rubric_version=rubric["rubric_version"],
        rubric_sha256=judge_rubric.rubric_sha256(rubric),
        envelope_sha256=envelope_sha256(envelope),
        # The request's stage-A binding is the envelope's verified manifest.
        input_manifest_sha256=envelope["input_manifest_sha256"],
    )


class InjectionEnvelopeTests(unittest.TestCase):
    """Every attack payload stays inert data inside the envelope."""

    def _envelope_for(self, payload: str):
        tmp = tempfile.TemporaryDirectory(prefix="wp2b2-injection-")
        self.addCleanup(tmp.cleanup)
        root = os.path.join(tmp.name, "bundle")
        writer = EvidenceWriter(root, run_id="run-injection")
        writer.finalize_input_evidence(
            [
                EvidenceArtifact(
                    "transcript.txt", payload.encode("utf-8"), ArtifactMetadata()
                )
            ]
        )
        gate = JudgeInputGate(root)
        gate.verify()
        return build_judge_envelope(
            rubric_ref=RUBRIC_REF,
            gate=gate,
            artifact_keys={"transcript": "transcript.txt"},
            control_id="SCENARIO_A_CONTROL_G",
        )

    def test_every_attack_round_trips_as_inert_data(self) -> None:
        for name, payload in _attack_payloads().items():
            with self.subTest(attack=name):
                envelope = self._envelope_for(payload)
                # Policy identity is untouched by transcript content.
                self.assertEqual(
                    envelope["policy_sha256"], judge_policy.policy_sha256()
                )
                # The payload survives byte-exact as DATA.
                self.assertEqual(
                    extract_untrusted_data(envelope)["transcript"], payload
                )
                # The rubric stays the pinned rubric.
                self.assertEqual(envelope["rubric"]["rubric_id"], RUBRIC_REF)

    def test_delimiter_injection_cannot_break_framing(self) -> None:
        payload = _attack_payloads()["delimiter_injection"]
        envelope = self._envelope_for(payload)
        text = render_envelope_text(envelope)
        self.assertEqual(text.count(ENVELOPE_BEGIN), 1)
        self.assertEqual(text.count(ENVELOPE_END), 1)
        # The raw delimiter text from the attack never appears in the
        # rendered envelope (content is transport-encoded).
        begin = text.index(ENVELOPE_BEGIN) + len(ENVELOPE_BEGIN)
        end = text.index(ENVELOPE_END)
        block = text[begin:end]
        decoded = json.loads(base64.b64decode(block.strip()).decode("utf-8"))
        self.assertEqual(decoded["transcript"], payload)

    def test_hidden_policy_request_gets_no_policy_text(self) -> None:
        payload = _attack_payloads()["hidden_policy_request"]
        envelope = self._envelope_for(payload)
        self.assertNotIn(judge_policy.JUDGE_SYSTEM_POLICY, json.dumps(envelope))
        self.assertNotIn(
            judge_policy.JUDGE_SYSTEM_POLICY, render_envelope_text(envelope)
        )


class InjectionVerdictTests(unittest.TestCase):
    """Malformed / spoofed / contradictory mock outputs are JUDGE_ERROR."""

    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory(prefix="wp2b2-injection-verdict-")
        self.addCleanup(tmp.cleanup)
        root = os.path.join(tmp.name, "bundle")
        writer = EvidenceWriter(root, run_id="run-injection-verdict")
        writer.finalize_input_evidence(
            [EvidenceArtifact("transcript.txt", b"turn", ArtifactMetadata())]
        )
        gate = JudgeInputGate(root)
        gate.verify()
        self.envelope = build_judge_envelope(
            rubric_ref=RUBRIC_REF,
            gate=gate,
            artifact_keys={"transcript": "transcript.txt"},
            control_id="SCENARIO_A_CONTROL_G",
        )
        self.request = _request_for(self.envelope)
        self.fixture = load_fixture("mock_verdicts.json")

    def _fill(self, payload: dict) -> dict:
        substitutions = {
            "__REQUEST_ID__": self.request.request_id,
            "__CONTROL_ID__": self.request.control_id,
            "__RUBRIC_SHA256__": self.request.rubric_sha256,
            "__JUDGE_ID__": self.request.judge.judge_id,
            "__JUDGE_VERSION__": self.request.judge.judge_version,
            "__INPUT_MANIFEST_SHA256__": self.request.input_manifest_sha256,
        }
        filled = {}
        for key, value in payload.items():
            filled[key] = substitutions.get(value, value) if isinstance(value, str) else value
        return filled

    def _materialize(self, spec) -> str:
        if isinstance(spec, str):
            return spec
        base = self._fill(dict(self.fixture["well_formed"][spec["template"]]))
        for key in spec.get("remove", []):
            base.pop(key, None)
        base.update(spec.get("add", {}))
        base.update({k: v for k, v in spec.get("set", {}).items()})
        if "set_overlong_span" in spec:
            base["offending_span"] = "x" * int(spec["set_overlong_span"])
        return json.dumps(base)

    def test_well_formed_mock_verdicts_parse(self) -> None:
        for name, payload in self.fixture["well_formed"].items():
            with self.subTest(case=name):
                response = JudgeResponse(
                    request_id=self.request.request_id,
                    response_id=f"resp-{name}",
                    transport_outcome=TransportOutcome.OK,
                    raw_output=json.dumps(self._fill(dict(payload))),
                )
                result = parse_judge_output(
                    response, self.request, self.envelope
                )
                self.assertTrue(result.is_verdict, name)

    def test_every_malformed_mock_output_is_judge_error(self) -> None:
        for name, spec in self.fixture["malformed"].items():
            with self.subTest(case=name):
                response = JudgeResponse(
                    request_id=self.request.request_id,
                    response_id=f"resp-{name}",
                    transport_outcome=TransportOutcome.OK,
                    raw_output=self._materialize(spec),
                )
                result = parse_judge_output(
                    response, self.request, self.envelope
                )
                self.assertFalse(result.is_verdict, name)
                self.assertIsNone(result.verdict, name)

    def test_refusal_timeout_transport_are_judge_error(self) -> None:
        for outcome in (
            TransportOutcome.REFUSED,
            TransportOutcome.TIMEOUT,
            TransportOutcome.TRANSPORT_ERROR,
        ):
            with self.subTest(outcome=outcome):
                response = JudgeResponse(
                    request_id=self.request.request_id,
                    response_id="resp-x",
                    transport_outcome=outcome,
                    raw_output=None,
                )
                result = parse_judge_output(
                    response, self.request, self.envelope
                )
                self.assertFalse(result.is_verdict)


if __name__ == "__main__":
    unittest.main()
