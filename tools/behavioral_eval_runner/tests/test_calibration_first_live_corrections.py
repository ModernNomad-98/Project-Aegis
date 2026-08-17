"""WP-2B-3 first-live execution-gate corrections (BER-DEC-008; the four
consolidated blocker families of the independent exact-head audit of
ca19b919…).

Family A: real-model response binding + label-opaque request IDs.
Family B: crash-durable ledger event persistence (flush + fsync barrier).
Family C: persistent metadata / RUN_STOPPED / RUN_PAUSED / OWNER_WAIT state.
Family D: complete owner-freeze token distributions.

Every test is OFFLINE: fakes, dummy sentinels, and temp directories only.
NO provider call, NO real credential, NO network, NO real evidence root.
"""

from __future__ import annotations

import json
import re
import unittest

from tools.behavioral_eval_runner.judge import calibration_dataset as cd
from tools.behavioral_eval_runner.judge import (
    calibration_development_driver as drv,
)
from tools.behavioral_eval_runner.judge import calibration_ledger as cl
from tools.behavioral_eval_runner.judge import calibration_transport as ct
from tools.behavioral_eval_runner.judge.calibration_errors import (
    CalibrationLedgerError,
    CalibrationStopError,
    CalibrationStopReason,
)
from tools.behavioral_eval_runner.judge.envelope import render_envelope_text
from tools.behavioral_eval_runner.judge.policy import JUDGE_SYSTEM_POLICY
from tools.behavioral_eval_runner.tests.test_calibration_development_driver import (
    DriverCase,
    _raw_verdict,
)
from tools.behavioral_eval_runner.tests.test_calibration_provider import (
    FAKE_EXCEPTIONS,
    FakeSdkClient,
    fake_response,
)

OPAQUE_ID_PATTERN = re.compile(r"^wp2b3-r-[0-9a-f]{32}$")

#: Substrings whose presence in any provider-visible surface would leak the
#: gold label, the split, or the raw item identity (audit family A).
LABEL_CODED_SUBSTRINGS = ("-dev-p", "-dev-f", "-h-p", "-h-f")

#: The nine trusted binding fields the request-specific schema must pin to
#: exactly one value each (audit family A).
PINNED_BINDING_FIELDS = (
    "request_id",
    "control_id",
    "rubric_id",
    "rubric_version",
    "rubric_sha256",
    "judge_id",
    "judge_version",
    "input_manifest_sha256",
    "schema_version",
)


def payload_from_schema_only(schema: dict) -> dict:
    """Build a verdict payload using ONLY the provider-visible response
    schema — the exact information a real model receives. Single-value
    enums supply every trusted binding; the model-chosen fields use plain
    schema-legal choices (a PASS verdict here)."""
    properties = schema["properties"]
    payload: dict = {}
    for name, prop in properties.items():
        enum = prop.get("enum")
        if isinstance(enum, list) and len(enum) == 1:
            payload[name] = enum[0]
    payload["verdict_id"] = "model-chosen-verdict-1"
    payload["verdict"] = "PASS"
    payload["failure_mode"] = None
    payload["offending_span"] = None
    payload["reason_code"] = "MEETS_RUBRIC"
    refs_enum = properties["evidence_refs"]["items"].get("enum")
    payload["evidence_refs"] = [refs_enum[0]]
    missing = set(properties) - set(payload)
    assert not missing, f"schema fields left unfilled: {sorted(missing)}"
    return payload


class TestFamilyARealModelBinding(DriverCase):
    """A real model must be able to produce a completely binding-valid
    verdict using ONLY provider-visible request content, and nothing
    provider-visible may leak item identity, split, or gold label."""

    def test_request_ids_are_opaque_deterministic_and_collision_free(self) -> None:
        dataset_sha = self.dataset.dataset_sha256()
        ids = []
        for item in self.dataset.items:  # all 160 approved-composition items
            rid = cd.calibration_request_id(item.item_id, dataset_sha)
            self.assertRegex(rid, OPAQUE_ID_PATTERN)
            self.assertNotIn(item.item_id, rid)
            for banned in LABEL_CODED_SUBSTRINGS:
                self.assertNotIn(banned, rid)
            self.assertEqual(
                rid, cd.calibration_request_id(item.item_id, dataset_sha)
            )
            ids.append(rid)
        self.assertEqual(len(set(ids)), 160)  # collision-free, all distinct

    def test_request_builder_uses_the_opaque_derivation(self) -> None:
        item = drv.development_run_order(self.dataset)[0]
        request = drv.build_item_request(item, self.identity)
        self.assertEqual(
            request.request_id,
            cd.calibration_request_id(
                item.item_id, self.identity.dataset_semantic_sha256
            ),
        )
        self.assertRegex(request.request_id, OPAQUE_ID_PATTERN)

    def test_schema_pins_every_trusted_binding_to_one_value(self) -> None:
        item = drv.development_run_order(self.dataset)[0]
        request = drv.build_item_request(item, self.identity)
        schema = ct.structured_verdict_output_schema(
            request=request, evidence_keys=("transcript",)
        )
        expected = {
            "request_id": request.request_id,
            "control_id": request.control_id,
            "rubric_id": request.rubric_id,
            "rubric_version": request.rubric_version,
            "rubric_sha256": request.rubric_sha256,
            "judge_id": request.judge.judge_id,
            "judge_version": request.judge.judge_version,
            "input_manifest_sha256": request.input_manifest_sha256,
            "schema_version": request.schema_version,
        }
        for field in PINNED_BINDING_FIELDS:
            enum = schema["properties"][field].get("enum")
            self.assertEqual(
                enum, [expected[field]],
                f"{field} must be pinned to exactly the trusted value",
            )
        self.assertEqual(
            schema["properties"]["evidence_refs"]["items"].get("enum"),
            ["transcript"],
        )

    def test_dispatch_kwargs_carry_request_specific_schema(self) -> None:
        driver, sdk, _summary = self._happy_run()
        self.assertEqual(driver.state, "OWNER_WAIT")
        first_kwargs = sdk.responses.calls[0]
        schema = first_kwargs["text"]["format"]["schema"]
        enum = schema["properties"]["request_id"].get("enum")
        self.assertIsInstance(enum, list)
        self.assertEqual(len(enum), 1)
        self.assertRegex(enum[0], OPAQUE_ID_PATTERN)

    def test_provider_kwargs_expose_no_item_identity_or_labels(self) -> None:
        driver, sdk, _summary = self._happy_run()
        del driver
        item_ids = {item.item_id for item in self.dataset.items}
        for kwargs in sdk.responses.calls:
            rendered = json.dumps(kwargs, sort_keys=True, default=str)
            for banned in LABEL_CODED_SUBSTRINGS:
                self.assertNotIn(banned, rendered)
            for item_id in item_ids:
                self.assertNotIn(item_id, rendered)
            for forbidden_key in ("candidate_expected_label",
                                  "candidate_rationale", "risk_class",
                                  "split", "owner_label_status"):
                self.assertNotIn(forbidden_key, rendered)

    def test_real_model_shaped_output_validates_from_schema_alone(self) -> None:
        """The decisive family-A regression: a fake that reads ONLY the
        provider-visible kwargs (as a real model would) must produce a
        verdict the runtime accepts as fully bound."""
        order = drv.development_run_order(self.dataset)
        gold_pass_item = next(
            i for i in order
            if i.candidate_expected_label is cd.CandidateLabel.PASS
        )

        def model_from_schema(kwargs):
            payload = payload_from_schema_only(
                kwargs["text"]["format"]["schema"]
            )
            return fake_response(json.dumps(payload))

        driver = self._driver()
        driver.prepare()
        script = []
        for item in order:
            if item.item_id == gold_pass_item.item_id:
                script.append(model_from_schema)
            else:
                request = drv.build_item_request(item, self.identity)
                script.append(fake_response(_raw_verdict(
                    request, item.candidate_expected_label.value
                )))
        sdk = FakeSdkClient(script)
        summary = driver.execute_development(
            sdk_client=sdk, exception_types=FAKE_EXCEPTIONS,
            declare_first_segment=True,
            started_utc="2026-08-20T00:00:00+00:00",
        )
        self.assertEqual(summary["judge_error_count"], 0)
        self.assertEqual(summary["agreement"], 1.0)
        row = next(
            r for r in summary["per_item_outcomes"]
            if r["item_id"] == gold_pass_item.item_id
        )
        self.assertEqual(row["outcome"], "VALIDATED_PASS")

    def test_wrong_binding_fields_remain_judge_error(self) -> None:
        order = drv.development_run_order(self.dataset)
        target = order[0]

        def corrupted_model(kwargs):
            payload = payload_from_schema_only(
                kwargs["text"]["format"]["schema"]
            )
            payload["rubric_sha256"] = "0" * 64  # off-schema AND off-binding
            return fake_response(json.dumps(payload))

        driver = self._driver()
        driver.prepare()
        script = []
        for item in order:
            if item.item_id == target.item_id:
                script.append(corrupted_model)
            else:
                request = drv.build_item_request(item, self.identity)
                script.append(fake_response(_raw_verdict(
                    request, item.candidate_expected_label.value
                )))
        sdk = FakeSdkClient(script)
        summary = driver.execute_development(
            sdk_client=sdk, exception_types=FAKE_EXCEPTIONS,
            declare_first_segment=True,
            started_utc="2026-08-20T00:00:00+00:00",
        )
        self.assertEqual(summary["judge_error_count"], 1)  # never a verdict

    def test_all_40_request_bounds_stay_within_the_ceiling(self) -> None:
        for item in drv.development_run_order(self.dataset):
            content = cd.CalibrationItemContent.from_item(item)
            from tools.behavioral_eval_runner.judge.calibration_envelope import (
                build_calibration_envelope,
            )
            envelope = build_calibration_envelope(content)
            request = drv.build_item_request(item, self.identity)
            kwargs = ct.build_responses_request_kwargs(
                instructions=JUDGE_SYSTEM_POLICY,
                input_text=render_envelope_text(envelope),
                max_output_tokens=ct.DEV_MAX_OUTPUT_TOKENS,
                request=request,
                evidence_keys=tuple(sorted(envelope["untrusted_data"])),
            )
            bound = ct.enforce_proven_input_budget(kwargs)
            self.assertLessEqual(bound, ct.MAX_INPUT_TOKENS_PER_JUDGMENT)


class TestFamilyBFsyncDurability(unittest.TestCase):
    """Every durable ledger event must be written, flushed, AND fsynced
    before control returns — ATTEMPT_STARTED is the write-ahead authority
    before any transport use."""

    def setUp(self) -> None:
        import os as os_module
        import tempfile

        self._os = os_module
        self._real_fsync = os_module.fsync
        self.fsync_calls = 0

        def counting_fsync(fd):
            self.fsync_calls += 1
            return self._real_fsync(fd)

        os_module.fsync = counting_fsync
        self.addCleanup(self._restore_fsync)
        tmp = tempfile.TemporaryDirectory(prefix="wp2b3-fsync-")
        self.addCleanup(tmp.cleanup)
        self.tmp = tmp.name

        from tools.behavioral_eval_runner.judge import (
            calibration_envelope as ce,
        )
        from tools.behavioral_eval_runner.judge import (
            calibration_ledger as cl,
        )
        from tools.behavioral_eval_runner.judge import (
            calibration_provider as cp,
        )
        from tools.behavioral_eval_runner.tests.test_calibration_dataset import (
            build_conforming_dataset,
        )
        from tools.behavioral_eval_runner.tests.test_calibration_provider import (
            _authorization,
        )

        self.cl = cl
        self.cp = cp
        self.dataset = build_conforming_dataset()
        self.authorization = _authorization(self.dataset)
        item = cd.development_items(self.dataset)[0]
        content = cd.CalibrationItemContent.from_item(item)
        self.envelope = ce.build_calibration_envelope(content)
        self.request = ce.build_calibration_judge_request(
            content=content,
            envelope=self.envelope,
            dataset_id=self.dataset.dataset_id,
            dataset_version=self.dataset.version,
            dataset_sha256=self.dataset.dataset_sha256(),
        )
        import os as _os

        self.ledger_path = _os.path.join(self.tmp, "fsync-ledger.jsonl")

    def _restore_fsync(self) -> None:
        self._os.fsync = self._real_fsync

    def test_fsync_called_for_every_durable_event_append(self) -> None:
        before = self.fsync_calls
        self.cl.CalibrationLedger(
            self.ledger_path, declare_first_segment=True
        )  # GENESIS + SEGMENT_OPENED = two durable appends
        self.assertGreaterEqual(self.fsync_calls - before, 2)

    def test_started_event_is_fsynced_before_transport(self) -> None:
        ledger = self.cl.CalibrationLedger(
            self.ledger_path, declare_first_segment=True
        )
        observed: dict = {}

        def transport_hook(kwargs):
            observed["fsync_calls_at_dispatch"] = self.fsync_calls
            with open(self.ledger_path, encoding="utf-8") as handle:
                lines = [json.loads(l) for l in handle if l.strip()]
            observed["tail_kind"] = lines[-1]["event_kind"]
            payload = payload_from_schema_only(
                kwargs["text"]["format"]["schema"]
            )
            return fake_response(json.dumps(payload))

        client = self.cp.OpenAICalibrationJudgeClient(
            authorization=self.authorization,
            ledger=ledger,
            sdk_client=FakeSdkClient([transport_hook]),
            exception_types=FAKE_EXCEPTIONS,
        )
        before = self.fsync_calls
        outcome = self.cp.dispatch_calibration_judgment(
            client, self.request, self.envelope
        )
        self.assertTrue(outcome.is_verdict)
        self.assertGreater(observed["fsync_calls_at_dispatch"], before)
        self.assertEqual(observed["tail_kind"], "ATTEMPT_STARTED")

    def test_fsync_failure_prevents_transport(self) -> None:
        ledger = self.cl.CalibrationLedger(
            self.ledger_path, declare_first_segment=True
        )

        def broken_fsync(_fd):
            raise OSError("simulated stable-storage failure")

        self._os.fsync = broken_fsync
        sdk = FakeSdkClient([])
        client = self.cp.OpenAICalibrationJudgeClient(
            authorization=self.authorization,
            ledger=ledger,
            sdk_client=sdk,
            exception_types=FAKE_EXCEPTIONS,
        )
        with self.assertRaises(OSError):
            client.dispatch(
                self.request,
                drv.build_item_envelope_bytes(
                    cd.development_items(self.dataset)[0]
                ),
            )
        self.assertEqual(sdk.responses.calls, [])  # transport never reached

    def test_partial_event_fails_chain_verification(self) -> None:
        self.cl.CalibrationLedger(
            self.ledger_path, declare_first_segment=True
        )
        with open(self.ledger_path, "a", encoding="utf-8") as handle:
            handle.write('{"event_kind": "ATTEMPT_STARTED", "trunc')
        with self.assertRaises(self.cl.CalibrationLedgerError):
            self.cl.verify_ledger_chain(self.ledger_path)

    def test_in_memory_unit_test_ledger_unaffected(self) -> None:
        def broken_fsync(_fd):
            raise OSError("simulated failure")

        self._os.fsync = broken_fsync
        ledger = self.cl.CalibrationLedger(None)  # in-memory: no file, no fsync
        reservation = ledger.reserve(
            kind=self.cl.RequestKind.JUDGMENT_ATTEMPT,
            logical_judgment_id="unit-test-judgment",
            attempt_number=1,
            estimated_input_tokens=100,
            max_output_tokens=100,
            day="2026-08-20",
            dataset_sha256="a" * 64,
            stage="DEVELOPMENT",
        )
        self.assertIsNotNone(reservation)


class _Obj:
    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)


class TestFamilyCPersistentRunState(DriverCase):
    """Durable RUN_PAUSED / RUN_STOPPED / OWNER_WAIT states; metadata
    SUCCESS (never a bare count) gates judgments; failure states cannot be
    silently resumed after restart."""

    def _events(self):
        import os

        path = os.path.join(
            self.root, *drv.CANONICAL_LEDGER_RELPATH.split("/")
        )
        with open(path, encoding="utf-8") as handle:
            return [json.loads(l) for l in handle if l.strip()]

    def _run_states(self):
        return [
            (e.get("run_state"), e.get("reason"))
            for e in self._events()
            if e.get("event_kind") == "RUN_STATE_TRANSITION"
        ]

    def _execute(self, driver, sdk, **kwargs):
        return driver.execute_development(
            sdk_client=sdk, exception_types=FAKE_EXCEPTIONS,
            declare_first_segment=kwargs.pop("declare_first_segment", True),
            started_utc="2026-08-20T00:00:00+00:00", **kwargs,
        )

    def test_failed_metadata_blocks_judgments_across_restart(self) -> None:
        from tools.behavioral_eval_runner.judge.calibration_errors import (
            CalibrationStopError,
        )

        driver = self._driver()
        driver.prepare()
        sdk = FakeSdkClient([])

        def exploding_retrieve(_model):
            raise RuntimeError("simulated metadata transport explosion")

        sdk.models.retrieve = exploding_retrieve
        with self.assertRaises(CalibrationStopError):
            self._execute(driver, sdk)
        self.assertEqual(driver.state, "RUN_STOPPED")
        self.assertEqual(sdk.responses.calls, [])  # no judgment dispatched
        states = self._run_states()
        self.assertEqual(states[-1][0], "RUN_STOPPED")

        second = self._driver()
        second.prepare()
        sdk2 = FakeSdkClient([])
        with self.assertRaises(CalibrationStopError):
            second.reopen()
        self.assertEqual(sdk2.responses.calls, [])
        self.assertEqual(sdk2.metadata_calls, [])

    def test_metadata_model_mismatch_blocks_across_restart(self) -> None:
        driver = self._driver()
        driver.prepare()
        sdk = FakeSdkClient([])
        sdk.models.retrieve = lambda _m: _Obj(id="gpt-not-the-snapshot")
        with self.assertRaises(CalibrationStopError) as ctx:
            self._execute(driver, sdk)
        self.assertIs(ctx.exception.stop_reason,
                      CalibrationStopReason.MODEL_IDENTITY_MISMATCH)
        self.assertEqual(self._run_states()[-1][0], "RUN_STOPPED")
        second = self._driver()
        second.prepare()
        with self.assertRaises(CalibrationStopError):
            second.reopen()

    def test_metadata_exception_records_billing_unknown(self) -> None:
        driver = self._driver()
        driver.prepare()
        sdk = FakeSdkClient([])

        def exploding_retrieve(_model):
            raise RuntimeError("boundary-uncertain metadata failure")

        sdk.models.retrieve = exploding_retrieve
        with self.assertRaises(CalibrationStopError):
            self._execute(driver, sdk)
        metadata_terminals = [
            e for e in self._events()
            if e.get("event_kind") == "ATTEMPT_TERMINAL"
            and e.get("request_kind") == "METADATA"
        ]
        self.assertEqual(len(metadata_terminals), 1)
        self.assertTrue(metadata_terminals[0]["billing_unknown"])

    def test_consumed_metadata_without_success_never_suffices(self) -> None:
        driver = self._driver()
        driver.prepare()
        driver.create_genesis(started_utc="2026-08-20T00:00:00+00:00")
        driver.open_development_segment()
        # Simulate a historical failed metadata terminal (count == 1, no
        # METADATA_OK) written by an earlier segment.
        reservation = driver.ledger.reserve(
            kind=cl.RequestKind.METADATA,
            logical_judgment_id=None,
            attempt_number=1,
            estimated_input_tokens=0,
            max_output_tokens=0,
            day="2026-08-20",
            dataset_sha256=self.identity.dataset_semantic_sha256,
            stage="DEVELOPMENT",
        )
        driver.ledger.record(
            reservation,
            provider_response_id=None,
            provider_request_trace_id=None,
            requested_model="gpt-5.5-2026-04-23",
            returned_model=None,
            request_timestamp_utc="t0",
            completion_timestamp_utc="t1",
            latency_ms=1,
            response_status="500",
            incomplete_details_reason=None,
            usage=None,
            outcome_kind="TRANSPORT_STATUS_500",
            billing_unknown=True,
        )
        driver.close_development_segment()

        second = self._driver()
        second.prepare()
        sdk = FakeSdkClient([])
        with self.assertRaises(CalibrationStopError):
            self._execute(second, sdk, declare_first_segment=False)
        self.assertEqual(sdk.metadata_calls, [])   # never re-probed (cap)
        self.assertEqual(sdk.responses.calls, [])  # never a judgment
        self.assertEqual(second.state, "RUN_STOPPED")

    def _stop_scenario(self, first_response) -> None:
        order = drv.development_run_order(self.dataset)
        driver = self._driver()
        driver.prepare()
        script = [first_response]  # item 1 hits the stop; rest never run
        sdk = FakeSdkClient(script)
        with self.assertRaises(CalibrationStopError):
            self._execute(driver, sdk)
        self.assertEqual(driver.state, "RUN_STOPPED")
        self.assertEqual(self._run_states()[-1][0], "RUN_STOPPED")
        second = self._driver()
        second.prepare()
        with self.assertRaises(CalibrationStopError):
            second.reopen()
        del order

    def test_model_mismatch_judgment_persists_run_stopped(self) -> None:
        self._stop_scenario(fake_response(
            '{"never": "parsed"}', model="gpt-not-the-snapshot"
        ))

    def test_auth_rejection_persists_run_stopped(self) -> None:
        from tools.behavioral_eval_runner.tests.test_calibration_provider import (
            FakeStatusError,
        )

        self._stop_scenario(FakeStatusError(401))

    def test_telemetry_failure_persists_run_stopped(self) -> None:
        order = drv.development_run_order(self.dataset)
        request = drv.build_item_request(order[0], self.identity)
        self._stop_scenario(fake_response(
            _raw_verdict(request, order[0].candidate_expected_label.value),
            usage=None,
        ))

    def test_cap_breach_persists_run_stopped(self) -> None:
        from tools.behavioral_eval_runner.tests.test_calibration_provider import (
            fake_usage,
        )

        order = drv.development_run_order(self.dataset)
        request = drv.build_item_request(order[0], self.identity)
        self._stop_scenario(fake_response(
            _raw_verdict(request, order[0].candidate_expected_label.value),
            usage=fake_usage(out=25001),
        ))

    def test_run_paused_is_durable_and_resumes_lawfully(self) -> None:
        order = drv.development_run_order(self.dataset)
        driver = self._driver()
        driver.prepare()
        sdk1 = FakeSdkClient(self._script_for_order(order[:3]))
        result = self._execute(driver, sdk1, owner_stop_after_items=3)
        self.assertEqual(result["state"], "RUN_PAUSED")
        self.assertEqual(driver.state, "RUN_PAUSED")
        states = self._run_states()
        self.assertEqual(states[-1][0], "RUN_PAUSED")
        second = self._driver()
        second.prepare()
        sdk2 = FakeSdkClient(self._script_for_order(order[3:]))
        summary = self._execute(second, sdk2, declare_first_segment=False)
        self.assertEqual(sdk2.metadata_calls, [])  # metadata never repeats
        self.assertEqual(len(sdk2.responses.calls), 37)
        self.assertEqual(summary["items_total"], 40)
        self.assertEqual(self._run_states()[-1][0], "OWNER_WAIT")

    def test_owner_wait_survives_restart_and_permits_zero_calls(self) -> None:
        _driver, _sdk, _summary = self._happy_run()
        self.assertEqual(self._run_states()[-1][0], "OWNER_WAIT")
        second = self._driver()
        second.prepare()
        sdk2 = FakeSdkClient([])
        with self.assertRaises(CalibrationStopError):
            second.reopen()
        self.assertEqual(sdk2.responses.calls, [])
        self.assertEqual(sdk2.metadata_calls, [])

    def test_summary_cannot_be_overwritten_or_bypassed(self) -> None:
        import os

        driver, _sdk, _summary = self._happy_run()
        with self.assertRaises(CalibrationLedgerError):
            driver.finalize()  # the summary is written exactly once
        summary_path = os.path.join(
            self.root, *drv.DEVELOPMENT_RESULT_SUMMARY_RELPATH.split("/")
        )
        os.remove(summary_path)  # deleting the file must NOT reopen the run
        second = self._driver()
        second.prepare()
        with self.assertRaises(CalibrationStopError):
            second.reopen()  # the durable OWNER_WAIT state still blocks


class TestFamilyDTokenDistributions(DriverCase):
    """The development summary must give Peter complete per-judgment
    input/output/reasoning distributions (count, min, max, mean, median,
    deterministic p95, sorted values) for the holdout max_output_tokens
    freeze; transport failures without telemetry stay excluded from the
    distributions but counted in attempts/retries/spend."""

    def test_percentile_definition_is_deterministic(self) -> None:
        self.assertEqual(
            drv.nearest_rank_percentile(list(range(1, 21)), 95), 19
        )
        self.assertEqual(drv.nearest_rank_percentile([10], 95), 10)
        self.assertEqual(
            drv.nearest_rank_percentile(list(range(1, 101)), 95), 95
        )
        self.assertEqual(
            drv.nearest_rank_percentile([5, 1, 9, 3], 50), 3
        )

    def _varied_run(self):
        from tools.behavioral_eval_runner.tests.test_calibration_provider import (
            fake_usage,
        )

        order = drv.development_run_order(self.dataset)
        driver = self._driver()
        driver.prepare()
        script = []
        expected = {"input": [], "output": [], "reasoning": []}
        for index, item in enumerate(order):
            request = drv.build_item_request(item, self.identity)
            usage = fake_usage(
                inp=900 + index, out=1000 + 10 * index,
                reasoning=500 + 5 * index,
            )
            expected["input"].append(900 + index)
            expected["output"].append(1000 + 10 * index)
            expected["reasoning"].append(500 + 5 * index)
            script.append(fake_response(
                _raw_verdict(request, item.candidate_expected_label.value),
                usage=usage,
            ))
        sdk = FakeSdkClient(script)
        summary = driver.execute_development(
            sdk_client=sdk, exception_types=FAKE_EXCEPTIONS,
            declare_first_segment=True,
            started_utc="2026-08-20T00:00:00+00:00",
        )
        return summary, expected

    def test_summary_contains_complete_distributions(self) -> None:
        summary, expected = self._varied_run()
        distributions = summary["distributions"]
        for name, values in (("input_tokens", expected["input"]),
                             ("output_tokens", expected["output"]),
                             ("reasoning_tokens", expected["reasoning"])):
            dist = distributions[name]
            ordered = sorted(values)
            self.assertEqual(dist["sample_count"], 40, name)
            self.assertEqual(dist["minimum"], ordered[0], name)
            self.assertEqual(dist["maximum"], ordered[-1], name)
            self.assertEqual(dist["mean"], sum(ordered) / 40, name)
            self.assertEqual(
                dist["median"],
                (ordered[19] + ordered[20]) / 2, name,
            )
            self.assertEqual(
                dist["p95"], drv.nearest_rank_percentile(ordered, 95), name
            )
            self.assertEqual(dist["values_sorted"], ordered, name)
            self.assertIn("nearest-rank", dist["percentile_definition"])

    def test_transport_failures_excluded_but_fully_counted(self) -> None:
        from tools.behavioral_eval_runner.tests.test_calibration_provider import (
            FakeTimeoutError,
        )

        order = drv.development_run_order(self.dataset)
        script = self._script_for_order(order)
        script.insert(0, FakeTimeoutError())  # item 1 attempt 1 times out
        driver = self._driver()
        driver.prepare()
        sdk = FakeSdkClient(script)
        summary = driver.execute_development(
            sdk_client=sdk, exception_types=FAKE_EXCEPTIONS,
            declare_first_segment=True,
            started_utc="2026-08-20T00:00:00+00:00",
        )
        for name in ("input_tokens", "output_tokens", "reasoning_tokens"):
            self.assertEqual(
                summary["distributions"][name]["sample_count"], 40, name
            )
        self.assertEqual(summary["accounting"]["judgment_attempts"], 41)
        self.assertEqual(summary["accounting"]["retries"], 1)
        self.assertGreater(summary["accounting"]["spend_nanousd_total"], 0)

    def test_incomplete_responses_stay_in_distributions_and_details(self) -> None:
        order = drv.development_run_order(self.dataset)
        error_item = order[0]
        driver = self._driver()
        driver.prepare()
        sdk = FakeSdkClient(self._script_for_order(
            order, error_items={error_item.item_id}
        ))
        summary = driver.execute_development(
            sdk_client=sdk, exception_types=FAKE_EXCEPTIONS,
            declare_first_segment=True,
            started_utc="2026-08-20T00:00:00+00:00",
        )
        self.assertEqual(summary["judge_error_count"], 1)
        self.assertEqual(
            summary["distributions"]["output_tokens"]["sample_count"], 40
        )
        self.assertEqual(len(summary["incomplete_responses"]), 1)
        self.assertEqual(
            summary["incomplete_responses"][0]["reason"],
            "max_output_tokens",
        )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
