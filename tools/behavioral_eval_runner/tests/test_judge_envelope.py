"""WP-2B-2: delimited untrusted-data envelope (prompt 11.C).

The envelope is built ONLY from stage-A input-manifest-verified artifacts
(through JudgeInputGate), separates policy identity from untrusted data,
encodes data so delimiter text cannot break framing, enforces the closed
least-context key set, and prevents expected-answer leakage."""

from __future__ import annotations

import base64
import json
import os
import tempfile
import unittest

from tools.behavioral_eval_runner.errors import (
    EvidenceIntegrityError,
    SchemaValidationError,
)
from tools.behavioral_eval_runner.evidence import (
    ArtifactMetadata,
    EvidenceArtifact,
    EvidenceWriter,
    JudgeInputGate,
)
from tools.behavioral_eval_runner.judge import policy as judge_policy
from tools.behavioral_eval_runner.judge import rubric as judge_rubric
from tools.behavioral_eval_runner.judge.envelope import (
    ALLOWED_EVIDENCE_KEYS,
    ENVELOPE_BEGIN,
    ENVELOPE_END,
    build_judge_envelope,
    envelope_sha256,
    extract_untrusted_data,
    render_envelope_text,
)

RUBRIC_REF = "rubric.scenario_a.coherent_topic.v1"


class EnvelopeTestBase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory(prefix="wp2b2-envelope-")
        self.addCleanup(self._tmp.cleanup)
        self.root = os.path.join(self._tmp.name, "bundle")
        writer = EvidenceWriter(self.root, run_id="run-envelope")
        self.transcript_text = "USER: one topic please.\nASSISTANT: one topic."
        writer.finalize_input_evidence(
            [
                EvidenceArtifact(
                    "transcript.txt",
                    self.transcript_text.encode("utf-8"),
                    ArtifactMetadata(),
                ),
                EvidenceArtifact(
                    "activation.json", b'{"nodes": []}', ArtifactMetadata()
                ),
            ]
        )
        self.gate = JudgeInputGate(self.root)

    def build(self, artifact_keys=None):
        self.gate.verify()
        return build_judge_envelope(
            rubric_ref=RUBRIC_REF,
            gate=self.gate,
            artifact_keys=artifact_keys
            or {"transcript": "transcript.txt"},
            control_id="SCENARIO_A_CONTROL_G",
        )


class EnvelopeConstructionTests(EnvelopeTestBase):
    def test_envelope_requires_verified_gate(self) -> None:
        with self.assertRaises(EvidenceIntegrityError):
            build_judge_envelope(
                rubric_ref=RUBRIC_REF,
                gate=self.gate,  # not verified
                artifact_keys={"transcript": "transcript.txt"},
                control_id="SCENARIO_A_CONTROL_G",
            )

    def test_envelope_reads_only_manifest_listed_artifacts(self) -> None:
        self.gate.verify()
        with self.assertRaises(EvidenceIntegrityError):
            build_judge_envelope(
                rubric_ref=RUBRIC_REF,
                gate=self.gate,
                artifact_keys={"transcript": "not-in-manifest.txt"},
                control_id="SCENARIO_A_CONTROL_G",
            )

    def test_envelope_shape_and_round_trip(self) -> None:
        envelope = self.build()
        self.assertEqual(envelope["envelope_kind"], "aegis_judge_envelope")
        self.assertEqual(envelope["policy_version"], judge_policy.JUDGE_POLICY_VERSION)
        self.assertEqual(envelope["policy_sha256"], judge_policy.policy_sha256())
        data = extract_untrusted_data(envelope)
        self.assertEqual(data["transcript"], self.transcript_text)

    def test_policy_text_never_inside_envelope(self) -> None:
        # The system policy is a SEPARATE layer: the envelope carries only its
        # version/hash identity, never the policy text itself.
        envelope = self.build()
        self.assertNotIn(
            judge_policy.JUDGE_SYSTEM_POLICY, json.dumps(envelope)
        )

    def test_unknown_evidence_key_rejected(self) -> None:
        self.gate.verify()
        with self.assertRaises(SchemaValidationError):
            build_judge_envelope(
                rubric_ref=RUBRIC_REF,
                gate=self.gate,
                artifact_keys={"surprise_channel": "transcript.txt"},
                control_id="SCENARIO_A_CONTROL_G",
            )

    def test_leakage_keys_are_not_representable(self) -> None:
        # The closed key set is least-context: no expected answer, answer
        # bank, or neighbor material can even be named.
        for forbidden in ("expected_answer", "answer_bank", "negative_neighbors"):
            self.assertNotIn(forbidden, ALLOWED_EVIDENCE_KEYS)

    def test_rubric_carries_minimum_contract_only(self) -> None:
        envelope = self.build()
        self.assertEqual(
            set(envelope["rubric"]),
            {
                "rubric_id",
                "rubric_version",
                "rubric_sha256",
                "question",
                "pass_criteria",
                "fail_criteria",
            },
        )

    def test_unknown_rubric_ref_rejected(self) -> None:
        self.gate.verify()
        with self.assertRaises(SchemaValidationError):
            build_judge_envelope(
                rubric_ref="rubric.invented.v1",
                gate=self.gate,
                artifact_keys={"transcript": "transcript.txt"},
                control_id="SCENARIO_A_CONTROL_G",
            )

    def test_deterministic_only_control_has_no_envelope(self) -> None:
        self.gate.verify()
        with self.assertRaises(SchemaValidationError):
            build_judge_envelope(
                rubric_ref=RUBRIC_REF,
                gate=self.gate,
                artifact_keys={"transcript": "transcript.txt"},
                control_id="SCENARIO_A_CONTROL_M",
            )

    def test_envelope_hash_deterministic(self) -> None:
        first = self.build()
        second = self.build()
        self.assertEqual(envelope_sha256(first), envelope_sha256(second))

    def test_duck_typed_gate_is_rejected(self) -> None:
        # The stage-A verification boundary cannot be satisfied by an
        # arbitrary object that quacks like a gate.
        class FakeGate:
            _verified_manifest_sha = "0" * 64

            def read_artifact(self, relative_path: str) -> bytes:
                return b"unverified bytes"

        with self.assertRaises(EvidenceIntegrityError):
            build_judge_envelope(
                rubric_ref=RUBRIC_REF,
                gate=FakeGate(),  # type: ignore[arg-type]
                artifact_keys={"transcript": "transcript.txt"},
                control_id="SCENARIO_A_CONTROL_G",
            )

    def test_extract_rejects_invalid_base64_entry(self) -> None:
        envelope = self.build()
        tampered = dict(envelope)
        tampered["untrusted_data"] = {
            "transcript": {"encoding": "utf-8", "content_b64": "!!!not-base64!!!"}
        }
        with self.assertRaises(SchemaValidationError):
            extract_untrusted_data(tampered)

    def test_extract_rejects_entry_without_content(self) -> None:
        envelope = self.build()
        tampered = dict(envelope)
        tampered["untrusted_data"] = {"transcript": {"encoding": "utf-8"}}
        with self.assertRaises(SchemaValidationError):
            extract_untrusted_data(tampered)


class EnvelopeRenderingTests(EnvelopeTestBase):
    def test_rendered_text_has_exactly_one_data_block(self) -> None:
        envelope = self.build()
        text = render_envelope_text(envelope)
        self.assertEqual(text.count(ENVELOPE_BEGIN), 1)
        self.assertEqual(text.count(ENVELOPE_END), 1)
        self.assertLess(text.index(ENVELOPE_BEGIN), text.index(ENVELOPE_END))

    def test_data_section_is_transport_encoded(self) -> None:
        envelope = self.build()
        text = render_envelope_text(envelope)
        begin = text.index(ENVELOPE_BEGIN) + len(ENVELOPE_BEGIN)
        end = text.index(ENVELOPE_END)
        payload = text[begin:end].strip()
        decoded = json.loads(base64.b64decode(payload).decode("utf-8"))
        self.assertIn("transcript", decoded)
        # The raw transcript text never appears un-encoded in the rendered form.
        self.assertNotIn(self.transcript_text, text)


if __name__ == "__main__":
    unittest.main()
