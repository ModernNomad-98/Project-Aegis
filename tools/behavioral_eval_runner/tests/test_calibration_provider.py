"""WP-2B-3 calibration-only provider path (BER-DEC-008 decisions 1-4, 17,
21-22, 27; task sections 8, 9, 12, 17).

Every test uses fakes: NO real provider call, NO real credential, NO network.
"""

from __future__ import annotations

import json
import unittest

from tools.behavioral_eval_runner.canonical import canonical_bytes, sha256_hex
from tools.behavioral_eval_runner.judge import calibration_dataset as cd
from tools.behavioral_eval_runner.judge import calibration_envelope as ce
from tools.behavioral_eval_runner.judge import calibration_gates as cg
from tools.behavioral_eval_runner.judge import calibration_ledger as cl
from tools.behavioral_eval_runner.judge import calibration_provider as cp
from tools.behavioral_eval_runner.judge import calibration_transport as ct
from tools.behavioral_eval_runner.judge.calibration_errors import (
    CalibrationAuthorizationError,
    CalibrationStopError,
    CalibrationStopReason,
)
from tools.behavioral_eval_runner.judge.envelope import (
    envelope_sha256,
    validate_request_envelope_binding,
)
from tools.behavioral_eval_runner.judge.interface import (
    DisabledJudgeProvider,
    TransportOutcome,
)
from tools.behavioral_eval_runner.judge.verdict import parse_judge_output
from tools.behavioral_eval_runner.errors import LiveDispatchDisabledError
from tools.behavioral_eval_runner.tests.test_calibration_dataset import (
    build_conforming_dataset,
)


# --------------------------------------------------------------- fakes
class FakeTimeoutError(Exception):
    pass


class FakeConnectionError(Exception):
    pass


class FakeStatusError(Exception):
    def __init__(self, status_code: int) -> None:
        super().__init__(f"status {status_code}")
        self.status_code = status_code


FAKE_EXCEPTIONS = cp.TransportExceptionTypes(
    timeout=FakeTimeoutError,
    connection=FakeConnectionError,
    status=FakeStatusError,
)


class _Namespace:
    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)


def fake_usage(inp: int = 900, out: int = 1200, reasoning: int = 800,
               cached: int = 0) -> _Namespace:
    return _Namespace(
        input_tokens=inp,
        output_tokens=out,
        total_tokens=inp + out,
        output_tokens_details=_Namespace(reasoning_tokens=reasoning),
        input_tokens_details=_Namespace(cached_tokens=cached,
                                        cache_write_tokens=0),
    )


def fake_response(raw_output: str | None, *, model: str = "gpt-5.5-2026-04-23",
                  status: str = "completed", incomplete_reason: str | None = None,
                  usage: _Namespace | None = "default",
                  refusal: bool = False) -> _Namespace:
    output = []
    if refusal:
        content = [_Namespace(type="refusal", refusal="cannot comply")]
        output.append(_Namespace(type="message", content=content))
    elif raw_output is not None:
        content = [_Namespace(type="output_text", text=raw_output)]
        output.append(_Namespace(type="message", content=content))
    return _Namespace(
        id="resp-fake-1",
        model=model,
        status=status,
        incomplete_details=(
            _Namespace(reason=incomplete_reason) if incomplete_reason else None
        ),
        usage=fake_usage() if usage == "default" else usage,
        output=output,
        output_text="" if (refusal or raw_output is None) else raw_output,
    )


class FakeResponsesApi:
    def __init__(self, script) -> None:
        self._script = list(script)
        self.calls: list[dict] = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        action = self._script.pop(0)
        if isinstance(action, Exception):
            raise action
        return action


class FakeSdkClient:
    def __init__(self, script) -> None:
        self.responses = FakeResponsesApi(script)
        self.max_retries = 0
        self.base_url = "https://api.openai.com/v1/"
        self.timeout = _Namespace(connect=15.0, read=300.0)
        self.models = _Namespace(retrieve=self._retrieve)
        self.metadata_calls: list[str] = []

    def _retrieve(self, model: str):
        self.metadata_calls.append(model)
        return _Namespace(id=model)


# ----------------------------------------------------- shared fixtures
def _authorization(dataset: cd.CandidateDataset) -> cg.CalibrationDispatchAuthorization:
    identity = cg.DatasetIdentity(
        dataset_id=dataset.dataset_id,
        dataset_version=dataset.version,
        dataset_sha256=dataset.dataset_sha256(),
        split_map_sha256=cd.split_map_sha256(dataset),
        labeling_guide_sha256="c" * 64,
    )
    approval = cg.OwnerLabelApproval(
        status=cg.OwnerApprovalStatus.APPROVED,
        approved_by="Peter Nguyen (owner)",
        approval_statement="explicit owner approval (test fixture)",
        approval_date="2026-08-20",
        dataset_id=identity.dataset_id,
        dataset_version=identity.dataset_version,
        dataset_sha256=identity.dataset_sha256,
        split_map_sha256=identity.split_map_sha256,
        labeling_guide_sha256=identity.labeling_guide_sha256,
    )
    return cg.authorize_calibration_dispatch(
        approval=approval, dataset_identity=identity,
        dataset=dataset, stage=cg.ExecutionStage.DEVELOPMENT,
    )


class ProviderCase(unittest.TestCase):
    def setUp(self) -> None:
        self.dataset = build_conforming_dataset()
        self.authorization = _authorization(self.dataset)
        self.item = cd.development_items(self.dataset)[0]
        self.content = cd.CalibrationItemContent.from_item(self.item)
        self.envelope = ce.build_calibration_envelope(self.content)
        self.request = ce.build_calibration_judge_request(
            content=self.content,
            envelope=self.envelope,
            dataset_id=self.dataset.dataset_id,
            dataset_version=self.dataset.version,
            dataset_sha256=self.dataset.dataset_sha256(),
        )
        self.envelope_bytes = canonical_bytes(
            {k: self.envelope[k] for k in sorted(self.envelope)}
        )
        self.ledger = cl.CalibrationLedger(None)  # in-memory

    def _client(self, script) -> cp.OpenAICalibrationJudgeClient:
        return cp.OpenAICalibrationJudgeClient(
            authorization=self.authorization,
            ledger=self.ledger,
            sdk_client=FakeSdkClient(script),
            exception_types=FAKE_EXCEPTIONS,
        )

    def _valid_raw(self) -> str:
        return json.dumps({
            "verdict_id": "v-1",
            "request_id": self.request.request_id,
            "control_id": self.request.control_id,
            "verdict": "FAIL",
            "failure_mode": "OTHER_RUBRIC_VIOLATION",
            "offending_span": "offending words",
            "reason_code": "VIOLATES_RUBRIC",
            "evidence_refs": ["transcript"],
            "rubric_id": self.request.rubric_id,
            "rubric_version": self.request.rubric_version,
            "rubric_sha256": self.request.rubric_sha256,
            "judge_id": self.request.judge.judge_id,
            "judge_version": self.request.judge.judge_version,
            "input_manifest_sha256": self.request.input_manifest_sha256,
            "schema_version": "1.0.0-wp2b2",
        })


class TestCalibrationEnvelope(ProviderCase):
    def test_envelope_binds_through_the_existing_validator(self) -> None:
        validate_request_envelope_binding(self.request, self.envelope)
        self.assertEqual(self.request.envelope_sha256,
                         envelope_sha256(self.envelope))

    def test_envelope_carries_only_the_transcript_channel(self) -> None:
        self.assertEqual(set(self.envelope["untrusted_data"]), {"transcript"})

    def test_request_carries_the_calibration_dataset_identity(self) -> None:
        self.assertEqual(self.request.calibration_dataset_sha256,
                         self.dataset.dataset_sha256())


class TestExecutionSurfaceBoundary(ProviderCase):
    def test_provider_requires_a_gate_issued_authorization(self) -> None:
        with self.assertRaises(CalibrationAuthorizationError):
            cp.OpenAICalibrationJudgeClient(
                authorization=None, ledger=self.ledger,
                sdk_client=FakeSdkClient([]),
                exception_types=FAKE_EXCEPTIONS,
            )
        with self.assertRaises(CalibrationAuthorizationError):
            cp.OpenAICalibrationJudgeClient(
                authorization="forged", ledger=self.ledger,
                sdk_client=FakeSdkClient([]),
                exception_types=FAKE_EXCEPTIONS,
            )

    def test_provider_rejects_a_misconfigured_sdk_client(self) -> None:
        bad = FakeSdkClient([])
        bad.max_retries = 2
        with self.assertRaises(CalibrationStopError) as ctx:
            cp.OpenAICalibrationJudgeClient(
                authorization=self.authorization, ledger=self.ledger,
                sdk_client=bad, exception_types=FAKE_EXCEPTIONS,
            )
        self.assertIs(ctx.exception.stop_reason,
                      CalibrationStopReason.SDK_RETRY_CONFIG_INVALID)
        wrong_url = FakeSdkClient([])
        wrong_url.base_url = "https://api.other.example/v1/"
        with self.assertRaises(CalibrationStopError):
            cp.OpenAICalibrationJudgeClient(
                authorization=self.authorization, ledger=self.ledger,
                sdk_client=wrong_url, exception_types=FAKE_EXCEPTIONS,
            )

    def test_request_without_dataset_identity_is_refused(self) -> None:
        from tools.behavioral_eval_runner.judge.interface import JudgeRequest

        stripped = JudgeRequest.from_dict({
            **self.request.to_dict(),
            "calibration_dataset_id": None,
            "calibration_dataset_version": None,
            "calibration_dataset_sha256": None,
        })
        client = self._client([fake_response(self._valid_raw())])
        with self.assertRaises(CalibrationAuthorizationError):
            client.dispatch(stripped, self.envelope_bytes)

    def test_mismatched_envelope_bytes_never_reach_the_provider(self) -> None:
        fake = FakeSdkClient([fake_response(self._valid_raw())])
        client = cp.OpenAICalibrationJudgeClient(
            authorization=self.authorization, ledger=self.ledger,
            sdk_client=fake, exception_types=FAKE_EXCEPTIONS,
        )
        response = client.dispatch(self.request, b"not the envelope")
        self.assertIs(response.transport_outcome,
                      TransportOutcome.TRANSPORT_ERROR)
        self.assertEqual(fake.responses.calls, [])  # zero provider calls
        self.assertEqual(len(self.ledger.entries()), 0)

    def test_generic_disabled_provider_still_denies(self) -> None:
        with self.assertRaises(LiveDispatchDisabledError):
            DisabledJudgeProvider().dispatch(self.request, self.envelope_bytes)


class TestDispatchAndFailClosedMapping(ProviderCase):
    def test_successful_verdict_round_trip(self) -> None:
        client = self._client([fake_response(self._valid_raw())])
        outcome = cp.dispatch_calibration_judgment(
            client, self.request, self.envelope
        )
        self.assertTrue(outcome.is_verdict)
        self.assertEqual(outcome.verdict.verdict.value, "FAIL")
        entries = self.ledger.entries()
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertEqual(entry.requested_model, "gpt-5.5-2026-04-23")
        self.assertEqual(entry.returned_model, "gpt-5.5-2026-04-23")
        self.assertEqual(entry.outcome_kind, "VERDICT_FAIL")
        self.assertEqual(entry.reasoning_tokens, 800)
        self.assertTrue(entry.sdk_version and isinstance(entry.sdk_version, str))

    def test_request_kwargs_are_the_closed_authorized_set(self) -> None:
        fake = FakeSdkClient([fake_response(self._valid_raw())])
        client = cp.OpenAICalibrationJudgeClient(
            authorization=self.authorization, ledger=self.ledger,
            sdk_client=fake, exception_types=FAKE_EXCEPTIONS,
        )
        client.dispatch(self.request, self.envelope_bytes)
        self.assertEqual(len(fake.responses.calls), 1)
        kwargs = fake.responses.calls[0]
        self.assertEqual(set(kwargs), set(ct.REQUIRED_REQUEST_KEYS))
        self.assertEqual(kwargs["model"], "gpt-5.5-2026-04-23")
        self.assertIs(kwargs["store"], False)
        self.assertIs(kwargs["background"], False)
        self.assertNotIn("tools", kwargs)
        self.assertNotIn("previous_response_id", kwargs)
        self.assertIn("AEGIS BEHAVIORAL EVAL RUNNER", kwargs["instructions"])
        self.assertIn("UNTRUSTED DATA", kwargs["input"])

    def test_expected_label_never_appears_in_the_provider_request(self) -> None:
        fake = FakeSdkClient([fake_response(self._valid_raw())])
        client = cp.OpenAICalibrationJudgeClient(
            authorization=self.authorization, ledger=self.ledger,
            sdk_client=fake, exception_types=FAKE_EXCEPTIONS,
        )
        client.dispatch(self.request, self.envelope_bytes)
        rendered = json.dumps(fake.responses.calls[0], default=str)
        for leak in ("candidate_expected_label", "expected_label",
                     "proposed_gold_label", "candidate_rationale",
                     "owner_label_status"):
            self.assertNotIn(leak, rendered)

    def test_model_identity_mismatch_is_a_stop(self) -> None:
        client = self._client(
            [fake_response(self._valid_raw(), model="gpt-5.5")]
        )
        with self.assertRaises(CalibrationStopError) as ctx:
            client.dispatch(self.request, self.envelope_bytes)
        self.assertIs(ctx.exception.stop_reason,
                      CalibrationStopReason.MODEL_IDENTITY_MISMATCH)
        entries = self.ledger.entries()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].returned_model, "gpt-5.5")
        self.assertEqual(entries[0].outcome_kind,
                         "STOP_MODEL_IDENTITY_MISMATCH")

    def test_missing_usage_telemetry_is_a_stop(self) -> None:
        client = self._client([fake_response(self._valid_raw(), usage=None)])
        with self.assertRaises(CalibrationStopError) as ctx:
            client.dispatch(self.request, self.envelope_bytes)
        self.assertIs(ctx.exception.stop_reason,
                      CalibrationStopReason.BUDGET_TELEMETRY_UNAVAILABLE)

    def test_incomplete_output_is_judge_error_never_parsed(self) -> None:
        truncated = self._valid_raw()[:40]
        client = self._client([
            fake_response(truncated, status="incomplete",
                          incomplete_reason="max_output_tokens"),
        ])
        response = client.dispatch(self.request, self.envelope_bytes)
        self.assertIs(response.transport_outcome,
                      TransportOutcome.MALFORMED_OUTPUT)
        self.assertIsNone(response.raw_output)  # incomplete is never parsed
        outcome = parse_judge_output(response, self.request, self.envelope)
        self.assertFalse(outcome.is_verdict)
        entry = self.ledger.entries()[0]
        self.assertEqual(entry.response_status, "incomplete")
        self.assertEqual(entry.incomplete_details_reason, "max_output_tokens")
        self.assertEqual(entry.outcome_kind, "JUDGE_ERROR_INCOMPLETE")

    def test_malformed_output_is_judge_error_and_never_retried(self) -> None:
        client = self._client([fake_response("this is not json")])
        response = client.dispatch(self.request, self.envelope_bytes)
        outcome = parse_judge_output(response, self.request, self.envelope)
        self.assertFalse(outcome.is_verdict)
        self.assertEqual(outcome.judge_error_kind, "MALFORMED_JSON")
        self.assertEqual(len(self.ledger.entries()), 1)  # exactly one attempt

    def test_refusal_fails_closed_and_never_retries(self) -> None:
        client = self._client([fake_response(None, refusal=True)])
        response = client.dispatch(self.request, self.envelope_bytes)
        self.assertIs(response.transport_outcome, TransportOutcome.REFUSED)
        outcome = parse_judge_output(response, self.request, self.envelope)
        self.assertFalse(outcome.is_verdict)
        self.assertEqual(outcome.judge_error_kind, "REFUSED")
        self.assertEqual(len(self.ledger.entries()), 1)

    def test_semantic_fail_verdict_never_retries(self) -> None:
        fake = FakeSdkClient([fake_response(self._valid_raw())])
        client = cp.OpenAICalibrationJudgeClient(
            authorization=self.authorization, ledger=self.ledger,
            sdk_client=fake, exception_types=FAKE_EXCEPTIONS,
        )
        client.dispatch(self.request, self.envelope_bytes)
        self.assertEqual(len(fake.responses.calls), 1)


class TestRunnerOwnedRetry(ProviderCase):
    def test_timeout_then_success_uses_exactly_two_ledgered_attempts(self) -> None:
        fake = FakeSdkClient([
            FakeTimeoutError("connect timeout"),
            fake_response(self._valid_raw()),
        ])
        client = cp.OpenAICalibrationJudgeClient(
            authorization=self.authorization, ledger=self.ledger,
            sdk_client=fake, exception_types=FAKE_EXCEPTIONS,
        )
        response = client.dispatch(self.request, self.envelope_bytes)
        self.assertIs(response.transport_outcome, TransportOutcome.OK)
        entries = self.ledger.entries()
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0].outcome_kind, "TRANSPORT_TIMEOUT")
        self.assertEqual(entries[0].attempt_number, 1)
        self.assertEqual(entries[1].attempt_number, 2)
        self.assertEqual(entries[1].retry_of_request_id,
                         entries[0].internal_request_id)
        self.assertNotEqual(entries[0].internal_request_id,
                            entries[1].internal_request_id)

    def test_two_transport_failures_stop_at_two_attempts(self) -> None:
        fake = FakeSdkClient([
            FakeConnectionError("reset"), FakeConnectionError("reset"),
            fake_response(self._valid_raw()),  # must never be reached
        ])
        client = cp.OpenAICalibrationJudgeClient(
            authorization=self.authorization, ledger=self.ledger,
            sdk_client=fake, exception_types=FAKE_EXCEPTIONS,
        )
        response = client.dispatch(self.request, self.envelope_bytes)
        self.assertIs(response.transport_outcome,
                      TransportOutcome.TRANSPORT_ERROR)
        self.assertEqual(len(fake.responses.calls), 2)  # never a third
        self.assertEqual(len(self.ledger.entries()), 2)

    def test_retryable_status_codes_use_the_single_runner_retry(self) -> None:
        fake = FakeSdkClient([
            FakeStatusError(429), fake_response(self._valid_raw()),
        ])
        client = cp.OpenAICalibrationJudgeClient(
            authorization=self.authorization, ledger=self.ledger,
            sdk_client=fake, exception_types=FAKE_EXCEPTIONS,
        )
        response = client.dispatch(self.request, self.envelope_bytes)
        self.assertIs(response.transport_outcome, TransportOutcome.OK)
        self.assertEqual(len(self.ledger.entries()), 2)

    def test_auth_status_is_a_stop_not_a_retry(self) -> None:
        fake = FakeSdkClient([FakeStatusError(401)])
        client = cp.OpenAICalibrationJudgeClient(
            authorization=self.authorization, ledger=self.ledger,
            sdk_client=fake, exception_types=FAKE_EXCEPTIONS,
        )
        with self.assertRaises(CalibrationStopError) as ctx:
            client.dispatch(self.request, self.envelope_bytes)
        self.assertIs(ctx.exception.stop_reason,
                      CalibrationStopReason.PROVIDER_AUTH_REJECTED)
        self.assertEqual(len(fake.responses.calls), 1)

    def test_attempts_count_inside_the_200_ceiling(self) -> None:
        fake = FakeSdkClient([
            FakeTimeoutError("t"), fake_response(self._valid_raw()),
        ])
        client = cp.OpenAICalibrationJudgeClient(
            authorization=self.authorization, ledger=self.ledger,
            sdk_client=fake, exception_types=FAKE_EXCEPTIONS,
        )
        client.dispatch(self.request, self.envelope_bytes)
        cumulative = self.ledger.cumulative()
        self.assertEqual(cumulative.attempts_total, 2)
        self.assertEqual(cumulative.total_external_requests, 2)


class TestHoldoutDispatchBoundary(ProviderCase):
    """B1 remediation: a DEVELOPMENT authorization can never dispatch a
    sealed-holdout item — the provider enforces item membership."""

    def _holdout_request(self):
        artifact = cg.HoldoutFreezeArtifact.from_dict(
            cg.HoldoutFreezeArtifact.example_dict()
        )
        freeze = cg.authorize_holdout_access(freeze_artifact=artifact)
        holdout_item = next(
            item for item in self.dataset.items
            if item.split is cd.CandidateSplit.SEALED_HOLDOUT
        )
        content = cd.CalibrationItemContent.from_item(
            holdout_item, holdout_authorization=freeze
        )
        envelope = ce.build_calibration_envelope(content)
        request = ce.build_calibration_judge_request(
            content=content, envelope=envelope,
            dataset_id=self.dataset.dataset_id,
            dataset_version=self.dataset.version,
            dataset_sha256=self.dataset.dataset_sha256(),
        )
        return request, canonical_bytes(
            {k: envelope[k] for k in sorted(envelope)}
        )

    def test_direct_holdout_projection_is_refused_without_freeze(self) -> None:
        holdout_item = next(
            item for item in self.dataset.items
            if item.split is cd.CandidateSplit.SEALED_HOLDOUT
        )
        from tools.behavioral_eval_runner.judge.calibration_errors import (
            HoldoutAccessError,
        )

        with self.assertRaises(HoldoutAccessError):
            cd.CalibrationItemContent.from_item(holdout_item)

    def test_development_authorization_cannot_dispatch_holdout(self) -> None:
        request, envelope_bytes = self._holdout_request()
        fake = FakeSdkClient([fake_response(self._valid_raw())])
        client = cp.OpenAICalibrationJudgeClient(
            authorization=self.authorization, ledger=self.ledger,
            sdk_client=fake, exception_types=FAKE_EXCEPTIONS,
        )
        with self.assertRaises(CalibrationAuthorizationError):
            client.dispatch(request, envelope_bytes)
        self.assertEqual(fake.responses.calls, [])  # zero provider calls
        self.assertEqual(len(self.ledger.entries()), 0)  # zero attempts

    def test_authorization_covers_exactly_the_development_items(self) -> None:
        expected = {
            cd.calibration_request_id(item.item_id)
            for item in cd.development_items(self.dataset)
        }
        self.assertEqual(
            set(self.authorization.authorized_request_ids), expected
        )


class TestUnclassifiedTransportException(ProviderCase):
    def test_unknown_exception_is_recorded_and_stops(self) -> None:
        class WeirdError(Exception):
            pass

        fake = FakeSdkClient([WeirdError("surprise failure")])
        client = cp.OpenAICalibrationJudgeClient(
            authorization=self.authorization, ledger=self.ledger,
            sdk_client=fake, exception_types=FAKE_EXCEPTIONS,
        )
        with self.assertRaises(CalibrationStopError) as ctx:
            client.dispatch(self.request, self.envelope_bytes)
        self.assertIs(
            ctx.exception.stop_reason,
            CalibrationStopReason.UNCLASSIFIED_TRANSPORT_ERROR,
        )
        entries = self.ledger.entries()
        self.assertEqual(len(entries), 1)  # the attempt is still accounted
        self.assertEqual(entries[0].outcome_kind,
                         "STOP_UNCLASSIFIED_TRANSPORT_ERROR")


class TestMetadataRequestSurface(ProviderCase):
    def test_metadata_request_is_ledgered_and_capped_at_one(self) -> None:
        fake = FakeSdkClient([])
        client = cp.OpenAICalibrationJudgeClient(
            authorization=self.authorization, ledger=self.ledger,
            sdk_client=fake, exception_types=FAKE_EXCEPTIONS,
        )
        record = client.request_model_availability_metadata()
        self.assertEqual(fake.metadata_calls, ["gpt-5.5-2026-04-23"])
        self.assertEqual(record.request_kind, cl.RequestKind.METADATA.value)
        with self.assertRaises(Exception):
            client.request_model_availability_metadata()  # cap: exactly one

    def test_metadata_returned_model_mismatch_is_a_stop(self) -> None:
        fake = FakeSdkClient([])
        fake.models = _Namespace(
            retrieve=lambda model: _Namespace(id="gpt-5.5")
        )
        client = cp.OpenAICalibrationJudgeClient(
            authorization=self.authorization, ledger=self.ledger,
            sdk_client=fake, exception_types=FAKE_EXCEPTIONS,
        )
        with self.assertRaises(CalibrationStopError) as ctx:
            client.request_model_availability_metadata()
        self.assertIs(ctx.exception.stop_reason,
                      CalibrationStopReason.MODEL_IDENTITY_MISMATCH)
        entries = self.ledger.entries()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].returned_model, "gpt-5.5")
        self.assertEqual(entries[0].outcome_kind,
                         "STOP_MODEL_IDENTITY_MISMATCH")

    def test_metadata_transport_exception_is_recorded_and_stops(self) -> None:
        def _boom(model: str):
            raise RuntimeError("metadata transport surprise")

        fake = FakeSdkClient([])
        fake.models = _Namespace(retrieve=_boom)
        client = cp.OpenAICalibrationJudgeClient(
            authorization=self.authorization, ledger=self.ledger,
            sdk_client=fake, exception_types=FAKE_EXCEPTIONS,
        )
        with self.assertRaises(CalibrationStopError) as ctx:
            client.request_model_availability_metadata()
        self.assertIs(
            ctx.exception.stop_reason,
            CalibrationStopReason.UNCLASSIFIED_TRANSPORT_ERROR,
        )
        self.assertEqual(len(self.ledger.entries()), 1)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
