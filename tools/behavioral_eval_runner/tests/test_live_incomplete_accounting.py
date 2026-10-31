"""Incomplete provider responses: fail closed, never graded, usage accounted.

The Pilot A run 41213647310 halted because a subject answer was truncated at the
output budget (provider status max_tokens). The harness correctly refused to
grade the partial answer, but it also threw away the provider usage telemetry on
the same response envelope, so the ledger recorded the call as unreconciled and
the run's accounting gate then required an owner attestation.

These tests pin the repair contract:
  * an incomplete / unusable response is never PASS or FAIL (the run still
    halts fail-closed with TRANSPORT_ERROR);
  * when the provider reported usage, the ledger records the ACTUAL cost and
    the call is reconciled, with an explicit ungraded/incomplete marker;
  * when no usage is available, the conservative reservation charge stays
    unreconciled (the pre-existing behaviour is preserved);
  * a complete response still takes the normal reconciled path.

No network call is made: every transport is the mock transport and the SDK-path
test injects a fake vendor module.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import types
import unittest
from unittest import mock

from tools.behavioral_eval_runner.live.cost_meter import CostMeter
from tools.behavioral_eval_runner.live.config import SUBJECT_PINS
from tools.behavioral_eval_runner.live.errors import (
    CostCeilingHaltError,
    ProviderTransportError,
)
from tools.behavioral_eval_runner.live.ledger_reconciliation import unreconciled_calls
from tools.behavioral_eval_runner.live.mock_transport import MockTransport
from tools.behavioral_eval_runner.live.pipeline import dry_run
from tools.behavioral_eval_runner.live.providers import complete_via_sdk
from tools.behavioral_eval_runner.live.transport import (
    ProviderRequest,
    ProviderResponse,
    ProviderUsage,
)
from tools.behavioral_eval_runner.tests import live_helpers as helpers


def _smoke_config() -> dict:
    """A single-attempt smoke-shaped synthetic config (mock dry run only)."""
    config = helpers.config_payload(ceiling=50, runs=1, max_out=512)
    config["subject_vendors"] = ["anthropic"]
    config["judge_allowlist"] = {
        "judge_models": [{"vendor": "openai", "model": "gpt-6-astra"}]
    }
    return config


def _smoke_paths(tmp: str):
    return helpers.make_paths(tmp, config=_smoke_config(), gate=helpers.gate_payload())


def _complete_subject(request: ProviderRequest) -> ProviderResponse:
    return ProviderResponse(
        response_id="mock-subject",
        served_model=request.model,
        text="A complete answer.",
        usage=ProviderUsage(input_tokens=120, output_tokens=40),
        stop_reason="end_turn",
    )


def _complete_judge(request: ProviderRequest) -> ProviderResponse:
    import json

    from tools.behavioral_eval_runner.canonical import canonical_json

    payload = json.loads(request.user_content)
    verdict = {
        "verdict": "PASS",
        "reason_code": "MEETS_RUBRIC",
        "failure_mode": None,
        "rubric_sha256": payload["rubric_sha256"],
        "response_sha256": payload["response_sha256"],
        "judge_model": payload["judge_model"],
        "evidence_refs": ["response"],
    }
    return ProviderResponse(
        response_id="mock-judge",
        served_model=request.model,
        text=canonical_json(verdict),
        usage=ProviderUsage(input_tokens=100, output_tokens=32),
        stop_reason="completed",
    )


def _truncated(request: ProviderRequest) -> ProviderResponse:
    """An unusable response envelope that still carries provider usage."""
    return ProviderResponse(
        response_id="truncated-response",
        served_model=request.model,
        text="A partial answer cut off at the output budget",
        usage=ProviderUsage(input_tokens=321, output_tokens=500),
        stop_reason="max_tokens",
    )


class IncompleteResponseAccountingTests(unittest.TestCase):
    def test_truncated_subject_is_ungraded_and_reconciled_at_actual_usage(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = _smoke_paths(tmp)
            subject = MockTransport(_truncated, name="truncated-subject")
            judge = MockTransport(_complete_judge, name="unused-judge")
            result = dry_run(
                paths,
                smoke=True,
                subject_transport_factory=lambda: subject,
                judge_transport_factory=lambda: judge,
            )

            # Fail closed: the run halts, the attempt is ERROR, never PASS/FAIL.
            self.assertEqual(result["status"], "HALTED")
            self.assertEqual(result["halt_reason_code"], "TRANSPORT_ERROR")
            self.assertEqual(result["dispatched_calls"], 1)
            self.assertEqual(subject.call_count, 1)
            self.assertEqual(judge.call_count, 0)
            states = [record["result_state"] for record in result["results"]]
            self.assertEqual(states, ["ERROR"])
            self.assertNotIn("PASS", states)
            self.assertNotIn("FAIL", states)

            ledger = result["cost_ledger"]
            self.assertEqual(ledger["call_count"], 1)
            self.assertEqual(ledger["unreconciled_count"], 0)
            self.assertEqual(unreconciled_calls(ledger), [])
            entry = ledger["calls"][0]
            self.assertTrue(entry["reconciled"])
            self.assertIsNotNone(entry["reason_code"])  # failure reason carried
            self.assertEqual(entry["reason_code"], "TRANSPORT_ERROR")
            self.assertEqual(entry["response_state"], "UNGRADED_INCOMPLETE")
            self.assertEqual(entry["stop_reason"], "max_tokens")
            self.assertEqual(entry["response_id"], "truncated-response")
            self.assertEqual(entry["served_model"], "claude-sonnet-5-5")
            self.assertEqual(
                entry["response_chars"],
                len("A partial answer cut off at the output budget"),
            )
            self.assertEqual(entry["input_tokens"], 321)
            self.assertEqual(entry["output_tokens"], 500)
            # Independently pinned integer cents: ceil((321*200 + 500*1000)/1e6)
            # = ceil(0.8463) = 1 (the production helper is not used to derive the
            # expected value, so this assertion is not tautological).
            self.assertEqual(entry["actual_cents"], 1)
            self.assertEqual(entry["cost_cents"], 1)
            self.assertEqual(entry["cost_cents"], entry["actual_cents"])
            self.assertGreaterEqual(entry["reserved_cents"], entry["actual_cents"])
            self.assertNotIn("text", entry)
            # The mock transport really received the capped, pinned request.
            self.assertEqual(subject.calls[0].vendor, "anthropic")
            self.assertEqual(subject.calls[0].model, "claude-sonnet-5-5")
            self.assertEqual(subject.calls[0].max_output_tokens, 512)
            self.assertEqual(subject.calls[0].timeout_seconds, 300)

    def test_truncated_judge_is_ungraded_and_reconciled_at_actual_usage(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = _smoke_paths(tmp)
            subject = MockTransport(_complete_subject, name="ok-subject")
            judge = MockTransport(_truncated, name="truncated-judge")
            result = dry_run(
                paths,
                smoke=True,
                subject_transport_factory=lambda: subject,
                judge_transport_factory=lambda: judge,
            )

            self.assertEqual(result["status"], "HALTED")
            self.assertEqual(result["halt_reason_code"], "TRANSPORT_ERROR")
            self.assertEqual(result["dispatched_calls"], 2)
            self.assertEqual(subject.call_count, 1)
            self.assertEqual(judge.call_count, 1)
            states = [record["result_state"] for record in result["results"]]
            self.assertEqual(states, ["ERROR"])

            ledger = result["cost_ledger"]
            self.assertEqual(ledger["call_count"], 2)
            self.assertEqual(ledger["unreconciled_count"], 0)
            self.assertEqual(unreconciled_calls(ledger), [])
            subject_entry = ledger["calls"][0]
            self.assertTrue(subject_entry["reconciled"])
            self.assertIsNone(subject_entry["reason_code"])
            judge_entry = ledger["calls"][1]
            self.assertTrue(judge_entry["reconciled"])
            self.assertEqual(judge_entry["response_state"], "UNGRADED_INCOMPLETE")
            self.assertEqual(judge_entry["stop_reason"], "max_tokens")
            self.assertEqual(judge_entry["call_ref"].split(":")[-2], "judge")
            self.assertEqual(judge_entry["response_id"], "truncated-response")
            self.assertEqual(judge_entry["served_model"], "gpt-6-astra")
            self.assertEqual(
                judge_entry["response_chars"],
                len("A partial answer cut off at the output budget"),
            )
            # The judge call was dispatched to the cross-vendor pinned judge with
            # the same configured output bound.
            self.assertEqual(judge.calls[0].vendor, "openai")
            self.assertEqual(judge.calls[0].model, "gpt-6-astra")
            self.assertEqual(judge.calls[0].max_output_tokens, 512)
            self.assertEqual(judge.calls[0].timeout_seconds, 300)

    def test_failure_without_usage_keeps_the_conservative_unreconciled_charge(self):
        def raise_without_usage(request):
            raise ProviderTransportError("simulated transport failure")

        with tempfile.TemporaryDirectory() as tmp:
            paths = _smoke_paths(tmp)
            subject = MockTransport(raise_without_usage, name="failing-subject")
            result = dry_run(
                paths,
                smoke=True,
                subject_transport_factory=lambda: subject,
                judge_transport_factory=lambda: MockTransport(_complete_judge),
            )

            self.assertEqual(result["status"], "HALTED")
            self.assertEqual(result["halt_reason_code"], "TRANSPORT_ERROR")
            ledger = result["cost_ledger"]
            self.assertEqual(ledger["unreconciled_count"], 1)
            entry = ledger["calls"][0]
            self.assertFalse(entry["reconciled"])
            self.assertIsNone(entry["actual_cents"])
            self.assertIsNone(entry["input_tokens"])
            self.assertIsNone(entry["output_tokens"])
            self.assertEqual(entry["cost_cents"], entry["reserved_cents"])
            self.assertEqual(entry["reason_code"], "TRANSPORT_ERROR")

    def test_usage_in_error_context_is_reconciled_without_a_response_object(self):
        # The SDK conversion path reports the error before any ProviderResponse
        # object escapes; the usage is carried in the error context instead.
        def raise_with_usage(request):
            raise ProviderTransportError(
                "the provider response is not clearly complete (status 'max_tokens')",
                context={
                    "vendor": request.vendor,
                    "stop_reason": "max_tokens",
                    "served_model": request.model,
                    "response_id": "resp-error-path",
                    "response_chars": 500,
                    "usage": {"input_tokens": 250, "output_tokens": 500},
                },
            )

        with tempfile.TemporaryDirectory() as tmp:
            paths = _smoke_paths(tmp)
            subject = MockTransport(raise_with_usage, name="sdk-shaped-failure")
            result = dry_run(
                paths,
                smoke=True,
                subject_transport_factory=lambda: subject,
                judge_transport_factory=lambda: MockTransport(_complete_judge),
            )

            ledger = result["cost_ledger"]
            self.assertEqual(ledger["unreconciled_count"], 0)
            entry = ledger["calls"][0]
            self.assertTrue(entry["reconciled"])
            self.assertEqual(entry["response_state"], "UNGRADED_INCOMPLETE")
            self.assertEqual(entry["stop_reason"], "max_tokens")
            self.assertEqual(entry["response_id"], "resp-error-path")
            self.assertEqual(entry["response_chars"], 500)
            # ceil((250*200 + 500*1000)/1e6) = ceil(0.55) = 1 cent, pinned literally.
            self.assertEqual(entry["actual_cents"], 1)


class ProviderEvidenceTests(unittest.TestCase):
    def test_validate_carries_usage_and_stop_reason_on_incomplete_response(self):
        response = ProviderResponse(
            response_id="resp-1",
            served_model="claude-sonnet-5-5",
            text="partial",
            usage=ProviderUsage(321, 500),
            stop_reason="max_tokens",
        )
        with self.assertRaises(ProviderTransportError) as caught:
            response.validate(require_model=False)
        context = caught.exception.context
        self.assertEqual(context["response_id"], "resp-1")
        self.assertEqual(context["served_model"], "claude-sonnet-5-5")
        self.assertEqual(context["stop_reason"], "max_tokens")
        self.assertEqual(context["response_chars"], 7)
        self.assertEqual(context["usage"], {"input_tokens": 321, "output_tokens": 500})
        self.assertTrue(context["response_incomplete"])

    def test_validate_carries_usage_on_empty_response_text(self):
        response = ProviderResponse(
            response_id="resp-2",
            served_model="claude-sonnet-5-5",
            text="   ",
            usage=ProviderUsage(10, 0),
            stop_reason="end_turn",
        )
        with self.assertRaises(ProviderTransportError) as caught:
            response.validate(require_model=False)
        self.assertEqual(caught.exception.context["usage"], {"input_tokens": 10, "output_tokens": 0})
        self.assertTrue(caught.exception.context["empty_response_text"])

    def test_complete_via_sdk_carries_usage_on_a_truncated_sdk_response(self):
        self.check_sdk_path(stop_reason="max_tokens", raises=True)

    def test_complete_via_sdk_returns_a_complete_response_with_usage(self):
        self.check_sdk_path(stop_reason="end_turn", raises=False)

    def check_sdk_path(self, *, stop_reason: str, raises: bool) -> None:
        fake = types.ModuleType("anthropic")

        # A plain instance (not a class body) so the test can parameterise the
        # terminal status: a class body cannot capture an enclosing local.
        fake_message = types.SimpleNamespace(
            id="msg-sdk",
            model="claude-sonnet-5-5",
            stop_reason=stop_reason,
            content=[types.SimpleNamespace(type="text", text="SDK path answer")],
            usage=types.SimpleNamespace(input_tokens=321, output_tokens=500),
        )

        class _FakeMessages:
            def create(self, **kwargs):
                self.kwargs = kwargs
                return fake_message

        class _FakeClient:
            def __init__(self, **kwargs):
                self.messages = _FakeMessages()

        fake.Anthropic = _FakeClient
        request = ProviderRequest(
            request_id="sdk-test",
            vendor="anthropic",
            model="claude-sonnet-5-5",
            system="system",
            user_content="user",
            max_output_tokens=512,
            timeout_seconds=30,
        )
        with mock.patch.dict(sys.modules, {"anthropic": fake}):
            with mock.patch.dict(os.environ, {}, clear=True):
                if raises:
                    with self.assertRaises(ProviderTransportError) as caught:
                        complete_via_sdk(request, "fake-key")
                    context = caught.exception.context
                    self.assertEqual(context["stop_reason"], "max_tokens")
                    self.assertEqual(context["served_model"], "claude-sonnet-5-5")
                    self.assertEqual(
                        context["usage"], {"input_tokens": 321, "output_tokens": 500}
                    )
                else:
                    response = complete_via_sdk(request, "fake-key")
                    self.assertEqual(response.stop_reason, "end_turn")
                    self.assertEqual(response.usage.to_dict(), {"input_tokens": 321, "output_tokens": 500})
                    self.assertEqual(response.text, "SDK path answer")

    def test_anthropic_missing_usage_keeps_termination_evidence_and_no_usage_key(self):
        # Symmetric to the openai missing-usage test: when the anthropic SDK
        # envelope carries no usage telemetry, the termination evidence must
        # still survive in the raised context and no usage key may be invented,
        # so accounting stays conservative.
        fake = types.ModuleType("anthropic")

        class _FakeMessage:
            id = "msg-missing-usage"
            model = "claude-sonnet-5-5"
            stop_reason = "max_tokens"
            content = [types.SimpleNamespace(type="text", text="partial answer")]
            # deliberately no usage attribute

        class _FakeMessages:
            def create(self, **kwargs):
                return _FakeMessage()

        class _FakeClient:
            def __init__(self, **kwargs):
                self.messages = _FakeMessages()

        fake.Anthropic = _FakeClient
        request = ProviderRequest(
            request_id="anthropic-missing-usage",
            vendor="anthropic",
            model="claude-sonnet-5-5",
            system="system",
            user_content="user",
            max_output_tokens=512,
            timeout_seconds=30,
        )
        with mock.patch.dict(sys.modules, {"anthropic": fake}):
            with mock.patch.dict(os.environ, {}, clear=True):
                with self.assertRaises(ProviderTransportError) as caught:
                    complete_via_sdk(request, "fake-key")
        context = caught.exception.context
        self.assertIn("no usage telemetry", str(caught.exception))
        self.assertNotIn("usage", context)  # accounting stays conservative
        self.assertEqual(context["response_id"], "msg-missing-usage")
        self.assertEqual(context["served_model"], "claude-sonnet-5-5")
        self.assertEqual(context["stop_reason"], "max_tokens")
        self.assertEqual(context["response_chars"], len("partial answer"))


class PerCallOutputBoundTests(unittest.TestCase):
    def test_reserve_uses_the_request_output_bound_and_reconciles(self):
        pin = SUBJECT_PINS["anthropic"]
        meter = CostMeter(1000, max_calls=10, max_output_tokens=4096)
        wide = meter.reserve(call_ref="wide", pin=pin, system_bytes=1000, user_bytes=1000)
        self.assertEqual(wide.reserved_output_tokens, 4096)
        self.assertEqual(wide.reserved_cents, 5)
        # The meter holds one reservation at a time (concurrency cap 1): reconcile
        # the first before opening the second.
        meter.reconcile(wide, input_tokens=500, output_tokens=100, served_model=pin.model)
        narrow = meter.reserve(
            call_ref="narrow",
            pin=pin,
            system_bytes=1000,
            user_bytes=1000,
            max_output_tokens=512,
        )
        self.assertEqual(narrow.reserved_output_tokens, 512)
        self.assertLess(narrow.reserved_cents, wide.reserved_cents)
        entry = meter.reconcile(
            narrow,
            input_tokens=500,
            output_tokens=100,
            served_model=pin.model,
        )
        self.assertTrue(entry["reconciled"])
        # ceil((500*200 + 100*1000)/1e6) = ceil(0.2) = 1 cent, pinned literally.
        self.assertEqual(entry["actual_cents"], 1)

    def test_reserve_refuses_a_malformed_output_bound(self):
        pin = SUBJECT_PINS["anthropic"]
        meter = CostMeter(1000, max_calls=10, max_output_tokens=4096)
        for bad in (0, -1, True, "many", None):
            with self.subTest(value=bad):
                if bad is None:
                    # None means "use the meter default", not malformed.
                    handle = meter.reserve(
                        call_ref="default", pin=pin, system_bytes=10, user_bytes=10
                    )
                    self.assertEqual(handle.reserved_output_tokens, 4096)
                    continue
                with self.assertRaises(ValueError):
                    meter.reserve(
                        call_ref="bad",
                        pin=pin,
                        system_bytes=10,
                        user_bytes=10,
                        max_output_tokens=bad,
                    )


class OpenAIBranchEvidenceTests(unittest.TestCase):
    """The openai responses-API branch must capture the same evidence."""

    @staticmethod
    def _fake_openai_module(*, status, output_text="SDK openai answer", with_usage=True):
        fake = types.ModuleType("openai")
        payload = {
            "id": "resp-openai-1",
            "model": "gpt-6-astra",
            "status": status,
            "output_text": output_text,
        }
        if with_usage:
            payload["usage"] = types.SimpleNamespace(
                input_tokens=111, output_tokens=222
            )
        response = types.SimpleNamespace(**payload)

        class _Responses:
            def create(self, **kwargs):
                self.kwargs = kwargs
                return response

        class _Client:
            def __init__(self, **kwargs):
                self.responses = _Responses()

        fake.OpenAI = _Client
        return fake

    @staticmethod
    def _request():
        return ProviderRequest(
            request_id="openai-sdk-test",
            vendor="openai",
            model="gpt-6-astra",
            system="system",
            user_content="user",
            max_output_tokens=512,
            timeout_seconds=30,
        )

    def test_incomplete_status_carries_usage_and_termination_evidence(self):
        fake = self._fake_openai_module(status="incomplete")
        with mock.patch.dict(sys.modules, {"openai": fake}):
            with mock.patch.dict(os.environ, {}, clear=True):
                with self.assertRaises(ProviderTransportError) as caught:
                    complete_via_sdk(self._request(), "fake-key")
        context = caught.exception.context
        self.assertIn("not clearly complete", str(caught.exception))
        self.assertEqual(context["stop_reason"], "incomplete")
        self.assertEqual(context["served_model"], "gpt-6-astra")
        self.assertEqual(
            context["usage"], {"input_tokens": 111, "output_tokens": 222}
        )
        self.assertEqual(context["response_chars"], len("SDK openai answer"))
        self.assertTrue(context["response_incomplete"])

    def test_complete_status_returns_usage_and_text(self):
        fake = self._fake_openai_module(status="completed")
        with mock.patch.dict(sys.modules, {"openai": fake}):
            with mock.patch.dict(os.environ, {}, clear=True):
                response = complete_via_sdk(self._request(), "fake-key")
        self.assertEqual(response.stop_reason, "completed")
        self.assertEqual(response.text, "SDK openai answer")
        self.assertEqual(
            response.usage.to_dict(), {"input_tokens": 111, "output_tokens": 222}
        )

    def test_missing_usage_keeps_termination_evidence_and_no_usage_key(self):
        fake = self._fake_openai_module(status="incomplete", with_usage=False)
        with mock.patch.dict(sys.modules, {"openai": fake}):
            with mock.patch.dict(os.environ, {}, clear=True):
                with self.assertRaises(ProviderTransportError) as caught:
                    complete_via_sdk(self._request(), "fake-key")
        context = caught.exception.context
        self.assertIn("no usage telemetry", str(caught.exception))
        self.assertNotIn("usage", context)  # accounting stays conservative
        self.assertEqual(context["stop_reason"], "incomplete")
        self.assertEqual(context["response_id"], "resp-openai-1")
        self.assertEqual(context["served_model"], "gpt-6-astra")
        self.assertEqual(context["response_chars"], len("SDK openai answer"))


class ForeignExceptionAndResumeTests(unittest.TestCase):
    def test_foreign_transport_exception_is_conservatively_unreconciled(self):
        def boom(request):
            raise RuntimeError("foreign transport failure")

        with tempfile.TemporaryDirectory() as tmp:
            paths = _smoke_paths(tmp)
            subject = MockTransport(boom, name="foreign-subject")
            judge = MockTransport(_complete_judge, name="unused-judge")
            result = dry_run(
                paths,
                smoke=True,
                subject_transport_factory=lambda: subject,
                judge_transport_factory=lambda: judge,
            )
            self.assertEqual(result["status"], "HALTED")
            self.assertEqual(result["halt_reason_code"], "TRANSPORT_ERROR")
            self.assertEqual(judge.call_count, 0)
            ledger = result["cost_ledger"]
            self.assertEqual(ledger["unreconciled_count"], 1)
            entry = ledger["calls"][0]
            self.assertFalse(entry["reconciled"])
            self.assertIsNone(entry["actual_cents"])
            self.assertEqual(entry["cost_cents"], entry["reserved_cents"])
            self.assertEqual(entry["reason_code"], "TRANSPORT_ERROR")
            self.assertIn("RuntimeError", entry["detail"])

    def test_ungraded_settlement_is_complete_in_the_atomic_snapshot(self):
        # An interrupted process must leave a self-consistent cost ledger: the
        # repaired accounting path snapshots the reconciled-ungraded entry right
        # after the call, so a resumed/restarted reader cannot double-charge it or
        # see a stale unreconciled block. Only the on-disk bytes are read here.
        pin = SUBJECT_PINS["anthropic"]
        with tempfile.TemporaryDirectory() as tmp:
            snapshot = os.path.join(tmp, "cost-ledger.json")
            meter = CostMeter(
                1000, max_calls=5, max_output_tokens=512, snapshot_path=snapshot
            )
            handle = meter.reserve(
                call_ref="resume:case:WITH_SKILL:run-1:subject:anthropic",
                pin=pin,
                system_bytes=100,
                user_bytes=200,
                max_output_tokens=512,
            )
            meter.reconcile_ungraded_response(
                handle,
                input_tokens=120,
                output_tokens=500,
                served_model=pin.model,
                reason_code="TRANSPORT_ERROR",
                detail="truncated at max_tokens",
                stop_reason="max_tokens",
                response_id="resp-snapshot",
                response_chars=44,
            )
            with open(snapshot, encoding="utf-8") as handle_in:
                persisted = json.load(handle_in)
            self.assertEqual(persisted["call_count"], 1)
            self.assertEqual(persisted["unreconciled_count"], 0)
            self.assertEqual(unreconciled_calls(persisted), [])
            entry = persisted["calls"][0]
            self.assertTrue(entry["reconciled"])
            self.assertEqual(entry["response_state"], "UNGRADED_INCOMPLETE")
            self.assertEqual(entry["stop_reason"], "max_tokens")
            self.assertEqual(entry["response_id"], "resp-snapshot")
            self.assertEqual(persisted["spent_cents"], entry["actual_cents"])
            # A resumed reader reproduces the same totals from the snapshot.
            self.assertEqual(meter.to_dict()["spent_cents"], persisted["spent_cents"])


class DriftBranchTests(unittest.TestCase):
    def test_usage_above_the_reservation_fails_closed_without_reconciling(self):
        # Deliberately inconsistent provider usage exercises the conservative
        # drift branch (same semantics as reconcile()): the call is recorded
        # unreconciled, charged max(actual, reserved) and the run halts. "Usage
        # present" therefore implies "reconciled" only when usage fits the
        # reservation (F9).
        pin = SUBJECT_PINS["anthropic"]
        meter = CostMeter(1000, max_calls=5, max_output_tokens=1)
        handle = meter.reserve(
            call_ref="drift", pin=pin, system_bytes=1, user_bytes=1
        )
        self.assertLessEqual(handle.reserved_cents, 2)
        with self.assertRaises(CostCeilingHaltError) as caught:
            meter.reconcile_ungraded_response(
                handle,
                input_tokens=10_000_000,
                output_tokens=0,
                served_model=pin.model,
                reason_code="TRANSPORT_ERROR",
                detail="impossible usage",
                stop_reason="max_tokens",
            )
        self.assertEqual(caught.exception.reason_code, "BUDGET_CAP")
        self.assertTrue(meter.halted)
        halt = meter.halt_record
        self.assertIsNotNone(halt)
        self.assertEqual(halt["reason_code"], "BUDGET_CAP")
        ledger = meter.to_dict()
        self.assertEqual(ledger["unreconciled_count"], 1)
        entry = ledger["calls"][0]
        self.assertFalse(entry["reconciled"])
        self.assertEqual(entry["reason_code"], "BUDGET_CAP")
        # 10,000,000 input tokens * 200 cents/Mtok = 2,000 cents (literal).
        self.assertEqual(entry["actual_cents"], 2000)
        self.assertEqual(entry["cost_cents"], max(2000, entry["reserved_cents"]))
