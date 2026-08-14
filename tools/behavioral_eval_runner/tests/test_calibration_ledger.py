"""WP-2B-3 request/token/cost ledger (BER-DEC-008 decisions 17-20, 26).

Deterministic and offline: no network, no provider object, integer nano-USD
money math only.
"""

from __future__ import annotations

import os
import tempfile
import unittest

from tools.behavioral_eval_runner.judge import calibration_ledger as cl
from tools.behavioral_eval_runner.judge.calibration_errors import (
    CalibrationLedgerError,
    CalibrationReservationDenied,
    CalibrationStopError,
    CalibrationStopReason,
)

T0 = "2026-08-20T10:00:00+00:00"
T1 = "2026-08-20T10:00:07+00:00"


def _ledger(tmp: str) -> cl.CalibrationLedger:
    return cl.CalibrationLedger(os.path.join(tmp, "ledger.jsonl"))


def _usage(inp: int = 1000, out: int = 2000, reasoning: int = 1500,
           cached: int = 0) -> cl.ProviderUsage:
    return cl.ProviderUsage(
        input_tokens=inp, output_tokens=out, reasoning_tokens=reasoning,
        cached_input_tokens=cached,
    )


def _record_ok(ledger: cl.CalibrationLedger, reservation: cl.Reservation,
               usage: cl.ProviderUsage | None = None,
               outcome: str = "VERDICT_PASS") -> cl.LedgerEntry:
    return ledger.record(
        reservation,
        provider_response_id="resp-1",
        provider_request_trace_id="trace-1",
        requested_model="gpt-5.5-2026-04-23",
        returned_model="gpt-5.5-2026-04-23",
        request_timestamp_utc=T0,
        completion_timestamp_utc=T1,
        latency_ms=7000,
        response_status="completed",
        incomplete_details_reason=None,
        usage=usage if usage is not None else _usage(),
        outcome_kind=outcome,
    )


class TestCapsAndPricing(unittest.TestCase):
    def test_authorized_cap_constants(self) -> None:
        self.assertEqual(cl.MAX_JUDGMENT_ATTEMPTS, 200)
        self.assertEqual(cl.MAX_METADATA_REQUESTS, 1)
        self.assertEqual(cl.MAX_TOTAL_EXTERNAL_REQUESTS, 201)
        self.assertEqual(cl.MAX_TOTAL_SPEND_NANOUSD, 175_000_000_000)
        self.assertEqual(cl.MAX_SINGLE_DAY_SPEND_NANOUSD, 175_000_000_000)
        self.assertEqual(cl.INPUT_PRICE_NANOUSD_PER_TOKEN, 5000)
        self.assertEqual(cl.OUTPUT_PRICE_NANOUSD_PER_TOKEN, 30000)
        self.assertEqual(cl.CACHED_INPUT_PRICE_NANOUSD_PER_TOKEN, 500)

    def test_worst_permitted_token_path_is_158_usd(self) -> None:
        # 200 x (8,000 in + 25,000 out) at $5/$30 per 1M == $158 (BER-DEC-008).
        per_attempt = cl.worst_case_attempt_charge_nanousd()
        self.assertEqual(per_attempt, 790_000_000)
        self.assertEqual(200 * per_attempt, 158_000_000_000)

    def test_charge_calculation_is_integer_nanousd(self) -> None:
        charge = cl.calculate_charge_nanousd(_usage(inp=8000, out=25000))
        self.assertEqual(charge, 8000 * 5000 + 25000 * 30000)
        cached = cl.calculate_charge_nanousd(
            _usage(inp=1000, out=100, cached=400)
        )
        # cached tokens are billed at the cached rate, the rest at full rate
        self.assertEqual(cached, 600 * 5000 + 400 * 500 + 100 * 30000)


class TestReservationsAndCaps(unittest.TestCase):
    def test_reservation_then_record_appends_an_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = _ledger(tmp)
            reservation = ledger.reserve(
                kind=cl.RequestKind.JUDGMENT_ATTEMPT,
                logical_judgment_id="wp2b3-item-1",
                attempt_number=1,
                estimated_input_tokens=1000,
                max_output_tokens=25000,
                day="2026-08-20",
            )
            entry = _record_ok(ledger, reservation)
            self.assertEqual(entry.cumulative.attempts_total, 1)
            self.assertEqual(entry.cumulative.total_external_requests, 1)
            self.assertEqual(entry.calculated_charge_nanousd,
                             1000 * 5000 + 2000 * 30000)
            self.assertEqual(entry.internal_request_id, "wp2b3-req-000001")

    def test_attempt_cap_denies_the_201st_judgment_attempt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = _ledger(tmp)
            for n in range(200):
                reservation = ledger.reserve(
                    kind=cl.RequestKind.JUDGMENT_ATTEMPT,
                    logical_judgment_id=f"item-{n}",
                    attempt_number=1,
                    estimated_input_tokens=10,
                    max_output_tokens=8192,
                    day="2026-08-20",
                )
                _record_ok(ledger, reservation,
                           usage=_usage(inp=10, out=10, reasoning=0))
            with self.assertRaises(CalibrationReservationDenied):
                ledger.reserve(
                    kind=cl.RequestKind.JUDGMENT_ATTEMPT,
                    logical_judgment_id="item-overflow",
                    attempt_number=1,
                    estimated_input_tokens=10,
                    max_output_tokens=8192,
                    day="2026-08-20",
                )

    def test_metadata_cap_is_exactly_one(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = _ledger(tmp)
            reservation = ledger.reserve(
                kind=cl.RequestKind.METADATA,
                logical_judgment_id=None,
                attempt_number=1,
                estimated_input_tokens=0,
                max_output_tokens=0,
                day="2026-08-20",
            )
            ledger.record(
                reservation,
                provider_response_id=None,
                provider_request_trace_id=None,
                requested_model="gpt-5.5-2026-04-23",
                returned_model="gpt-5.5-2026-04-23",
                request_timestamp_utc=T0,
                completion_timestamp_utc=T1,
                latency_ms=100,
                response_status="200",
                incomplete_details_reason=None,
                usage=cl.ProviderUsage.zero(),
                outcome_kind="METADATA_OK",
            )
            with self.assertRaises(CalibrationReservationDenied):
                ledger.reserve(
                    kind=cl.RequestKind.METADATA,
                    logical_judgment_id=None,
                    attempt_number=1,
                    estimated_input_tokens=0,
                    max_output_tokens=0,
                    day="2026-08-20",
                )

    def test_spend_cap_stops_before_the_cap_not_after(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = _ledger(tmp)
            # Consume nearly the full budget with recorded actual charges.
            reservation = ledger.reserve(
                kind=cl.RequestKind.JUDGMENT_ATTEMPT,
                logical_judgment_id="big",
                attempt_number=1,
                estimated_input_tokens=8000,
                max_output_tokens=25000,
                day="2026-08-20",
            )
            big_usage = cl.ProviderUsage(
                input_tokens=8000,
                output_tokens=5_820_000,  # 5000*8000 + 30000*out ~= 174.64B nano
                reasoning_tokens=0,
                cached_input_tokens=0,
            )
            _record_ok(ledger, reservation, usage=big_usage)
            spent = ledger.cumulative().spend_nanousd_total
            self.assertLess(spent, cl.MAX_TOTAL_SPEND_NANOUSD)
            headroom = cl.MAX_TOTAL_SPEND_NANOUSD - spent
            self.assertLess(headroom, cl.worst_case_attempt_charge_nanousd())
            # The next worst-case reservation would cross the ceiling: denied
            # BEFORE dispatch, so the cap is never exceeded.
            with self.assertRaises(CalibrationReservationDenied):
                ledger.reserve(
                    kind=cl.RequestKind.JUDGMENT_ATTEMPT,
                    logical_judgment_id="overflow",
                    attempt_number=1,
                    estimated_input_tokens=8000,
                    max_output_tokens=25000,
                    day="2026-08-20",
                )

    def test_input_token_budget_denied_at_reservation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = _ledger(tmp)
            with self.assertRaises(CalibrationReservationDenied):
                ledger.reserve(
                    kind=cl.RequestKind.JUDGMENT_ATTEMPT,
                    logical_judgment_id="too-big",
                    attempt_number=1,
                    estimated_input_tokens=8001,
                    max_output_tokens=25000,
                    day="2026-08-20",
                )
            with self.assertRaises(CalibrationReservationDenied):
                ledger.reserve(
                    kind=cl.RequestKind.JUDGMENT_ATTEMPT,
                    logical_judgment_id="out-too-big",
                    attempt_number=1,
                    estimated_input_tokens=100,
                    max_output_tokens=25001,
                    day="2026-08-20",
                )

    def test_reservation_is_single_use(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = _ledger(tmp)
            reservation = ledger.reserve(
                kind=cl.RequestKind.JUDGMENT_ATTEMPT,
                logical_judgment_id="once",
                attempt_number=1,
                estimated_input_tokens=10,
                max_output_tokens=8192,
                day="2026-08-20",
            )
            _record_ok(ledger, reservation)
            with self.assertRaises(CalibrationLedgerError):
                _record_ok(ledger, reservation)


class TestTelemetryAndRetryLinkage(unittest.TestCase):
    def test_missing_monetary_telemetry_is_a_stop(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = _ledger(tmp)
            reservation = ledger.reserve(
                kind=cl.RequestKind.JUDGMENT_ATTEMPT,
                logical_judgment_id="no-usage",
                attempt_number=1,
                estimated_input_tokens=100,
                max_output_tokens=25000,
                day="2026-08-20",
            )
            with self.assertRaises(CalibrationStopError) as ctx:
                ledger.record(
                    reservation,
                    provider_response_id="resp-x",
                    provider_request_trace_id=None,
                    requested_model="gpt-5.5-2026-04-23",
                    returned_model="gpt-5.5-2026-04-23",
                    request_timestamp_utc=T0,
                    completion_timestamp_utc=T1,
                    latency_ms=10,
                    response_status="completed",
                    incomplete_details_reason=None,
                    usage=None,  # provider reported no usage/billing telemetry
                    outcome_kind="VERDICT_PASS",
                )
            self.assertIs(
                ctx.exception.stop_reason,
                CalibrationStopReason.BUDGET_TELEMETRY_UNAVAILABLE,
            )
            # The stop is still ACCOUNTED: an entry exists, charged worst-case.
            entries = ledger.entries()
            self.assertEqual(len(entries), 1)
            self.assertTrue(entries[-1].telemetry_missing)
            self.assertEqual(
                entries[-1].calculated_charge_nanousd,
                100 * 5000 + 25000 * 30000,
            )

    def test_retry_attempts_have_unique_ids_and_linkage(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = _ledger(tmp)
            first = ledger.reserve(
                kind=cl.RequestKind.JUDGMENT_ATTEMPT,
                logical_judgment_id="item-r",
                attempt_number=1,
                estimated_input_tokens=10,
                max_output_tokens=8192,
                day="2026-08-20",
            )
            entry1 = ledger.record(
                first,
                provider_response_id=None,
                provider_request_trace_id=None,
                requested_model="gpt-5.5-2026-04-23",
                returned_model=None,
                request_timestamp_utc=T0,
                completion_timestamp_utc=T1,
                latency_ms=15000,
                response_status="TIMEOUT",
                incomplete_details_reason=None,
                usage=cl.ProviderUsage.zero(),
                outcome_kind="TRANSPORT_TIMEOUT",
            )
            second = ledger.reserve(
                kind=cl.RequestKind.JUDGMENT_ATTEMPT,
                logical_judgment_id="item-r",
                attempt_number=2,
                estimated_input_tokens=10,
                max_output_tokens=8192,
                day="2026-08-20",
                retry_of_request_id=entry1.internal_request_id,
            )
            entry2 = _record_ok(ledger, second)
            self.assertNotEqual(entry1.internal_request_id,
                                entry2.internal_request_id)
            self.assertEqual(entry2.retry_of_request_id,
                             entry1.internal_request_id)
            self.assertEqual(entry2.attempt_number, 2)
            self.assertEqual(entry2.cumulative.attempts_total, 2)

    def test_third_attempt_for_one_judgment_is_denied(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = _ledger(tmp)
            for attempt in (1, 2):
                reservation = ledger.reserve(
                    kind=cl.RequestKind.JUDGMENT_ATTEMPT,
                    logical_judgment_id="item-x",
                    attempt_number=attempt,
                    estimated_input_tokens=10,
                    max_output_tokens=8192,
                    day="2026-08-20",
                )
                ledger.record(
                    reservation,
                    provider_response_id=None,
                    provider_request_trace_id=None,
                    requested_model="gpt-5.5-2026-04-23",
                    returned_model=None,
                    request_timestamp_utc=T0,
                    completion_timestamp_utc=T1,
                    latency_ms=1,
                    response_status="TIMEOUT",
                    incomplete_details_reason=None,
                    usage=cl.ProviderUsage.zero(),
                    outcome_kind="TRANSPORT_TIMEOUT",
                )
            with self.assertRaises(CalibrationReservationDenied):
                ledger.reserve(
                    kind=cl.RequestKind.JUDGMENT_ATTEMPT,
                    logical_judgment_id="item-x",
                    attempt_number=3,
                    estimated_input_tokens=10,
                    max_output_tokens=8192,
                    day="2026-08-20",
                )


class TestAppendOnlyIntegrity(unittest.TestCase):
    def test_ledger_file_is_append_only_jsonl_with_hash_chain(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "ledger.jsonl")
            ledger = cl.CalibrationLedger(path)
            r1 = ledger.reserve(
                kind=cl.RequestKind.JUDGMENT_ATTEMPT,
                logical_judgment_id="a", attempt_number=1,
                estimated_input_tokens=10, max_output_tokens=8192,
                day="2026-08-20",
            )
            _record_ok(ledger, r1)
            r2 = ledger.reserve(
                kind=cl.RequestKind.JUDGMENT_ATTEMPT,
                logical_judgment_id="b", attempt_number=1,
                estimated_input_tokens=10, max_output_tokens=8192,
                day="2026-08-20",
            )
            _record_ok(ledger, r2)
            with open(path, encoding="utf-8") as handle:
                lines = [line for line in handle.read().splitlines() if line]
            self.assertEqual(len(lines), 2)
            cl.verify_ledger_chain(path)  # no exception: chain intact
            with open(path, "a", encoding="utf-8") as handle:
                handle.write(lines[0] + "\n")  # naive duplicate append
            with self.assertRaises(CalibrationLedgerError):
                cl.verify_ledger_chain(path)


class TestCrossSegmentContinuity(unittest.TestCase):
    """B2 remediation: the BER-DEC-008 caps are WORK-PACKAGE totals — a new
    execution segment (mandated by the OWNER_WAIT design) must rehydrate
    prior verified ledgers, never reset the ceilings."""

    def _seed_segment(self, path: str, judgment_id: str = "j-1",
                      attempts: int = 1) -> None:
        ledger = cl.CalibrationLedger(path)
        for attempt in range(1, attempts + 1):
            reservation = ledger.reserve(
                kind=cl.RequestKind.JUDGMENT_ATTEMPT,
                logical_judgment_id=judgment_id,
                attempt_number=attempt,
                estimated_input_tokens=10,
                max_output_tokens=8192,
                day="2026-08-20",
            )
            _record_ok(ledger, reservation,
                       usage=_usage(inp=10, out=10, reasoning=0))

    def test_resumed_ledger_carries_prior_totals(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            seg1 = os.path.join(tmp, "seg1.jsonl")
            self._seed_segment(seg1, judgment_id="j-1", attempts=2)
            ledger = cl.CalibrationLedger(
                os.path.join(tmp, "seg2.jsonl"), prior_ledger_paths=(seg1,)
            )
            cumulative = ledger.cumulative()
            self.assertEqual(cumulative.attempts_total, 2)
            self.assertEqual(cumulative.total_external_requests, 2)
            self.assertEqual(cumulative.judgments_total, 1)
            self.assertGreater(cumulative.spend_nanousd_total, 0)

    def test_per_judgment_attempt_cap_survives_segments(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            seg1 = os.path.join(tmp, "seg1.jsonl")
            self._seed_segment(seg1, judgment_id="j-x", attempts=2)
            ledger = cl.CalibrationLedger(
                os.path.join(tmp, "seg2.jsonl"), prior_ledger_paths=(seg1,)
            )
            with self.assertRaises(CalibrationReservationDenied):
                ledger.reserve(
                    kind=cl.RequestKind.JUDGMENT_ATTEMPT,
                    logical_judgment_id="j-x",
                    attempt_number=2,
                    estimated_input_tokens=10,
                    max_output_tokens=8192,
                    day="2026-08-21",
                )

    def test_metadata_cap_survives_segments(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            seg1 = os.path.join(tmp, "seg1.jsonl")
            l1 = cl.CalibrationLedger(seg1)
            reservation = l1.reserve(
                kind=cl.RequestKind.METADATA, logical_judgment_id=None,
                attempt_number=1, estimated_input_tokens=0,
                max_output_tokens=0, day="2026-08-20",
            )
            l1.record(
                reservation, provider_response_id=None,
                provider_request_trace_id=None,
                requested_model="gpt-5.5-2026-04-23",
                returned_model="gpt-5.5-2026-04-23",
                request_timestamp_utc=T0, completion_timestamp_utc=T1,
                latency_ms=5, response_status="OK",
                incomplete_details_reason=None,
                usage=cl.ProviderUsage.zero(), outcome_kind="METADATA_OK",
            )
            l2 = cl.CalibrationLedger(
                os.path.join(tmp, "seg2.jsonl"), prior_ledger_paths=(seg1,)
            )
            with self.assertRaises(CalibrationReservationDenied):
                l2.reserve(
                    kind=cl.RequestKind.METADATA, logical_judgment_id=None,
                    attempt_number=1, estimated_input_tokens=0,
                    max_output_tokens=0, day="2026-08-21",
                )

    def test_spend_and_day_ceilings_survive_segments(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            seg1 = os.path.join(tmp, "seg1.jsonl")
            l1 = cl.CalibrationLedger(seg1)
            reservation = l1.reserve(
                kind=cl.RequestKind.JUDGMENT_ATTEMPT,
                logical_judgment_id="big", attempt_number=1,
                estimated_input_tokens=8000, max_output_tokens=25000,
                day="2026-08-20",
            )
            _record_ok(l1, reservation, usage=cl.ProviderUsage(
                input_tokens=8000, output_tokens=5_820_000,
                reasoning_tokens=0, cached_input_tokens=0,
            ))
            l2 = cl.CalibrationLedger(
                os.path.join(tmp, "seg2.jsonl"), prior_ledger_paths=(seg1,)
            )
            self.assertEqual(
                l2.cumulative().spend_nanousd_total, 174_640_000_000
            )
            # Total ceiling binds across segments even on a NEW day.
            with self.assertRaises(CalibrationReservationDenied):
                l2.reserve(
                    kind=cl.RequestKind.JUDGMENT_ATTEMPT,
                    logical_judgment_id="overflow", attempt_number=1,
                    estimated_input_tokens=8000, max_output_tokens=25000,
                    day="2026-08-21",
                )

    def test_tampered_prior_segment_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            seg1 = os.path.join(tmp, "seg1.jsonl")
            self._seed_segment(seg1)
            with open(seg1, encoding="utf-8") as fh:
                line = fh.readline()
            with open(seg1, "a", encoding="utf-8") as fh:
                fh.write(line)  # duplicate append breaks the chain
            with self.assertRaises(CalibrationLedgerError):
                cl.CalibrationLedger(
                    os.path.join(tmp, "seg2.jsonl"),
                    prior_ledger_paths=(seg1,),
                )

    def test_missing_prior_segment_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(CalibrationLedgerError):
                cl.CalibrationLedger(
                    os.path.join(tmp, "seg2.jsonl"),
                    prior_ledger_paths=(os.path.join(tmp, "absent.jsonl"),),
                )


class TestReportedInputTokenOvershoot(unittest.TestCase):
    def test_provider_reported_input_over_budget_is_recorded_stop(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = _ledger(tmp)
            reservation = ledger.reserve(
                kind=cl.RequestKind.JUDGMENT_ATTEMPT,
                logical_judgment_id="over", attempt_number=1,
                estimated_input_tokens=100, max_output_tokens=8192,
                day="2026-08-20",
            )
            with self.assertRaises(CalibrationStopError) as ctx:
                _record_ok(ledger, reservation, usage=cl.ProviderUsage(
                    input_tokens=9000, output_tokens=10,
                    reasoning_tokens=0, cached_input_tokens=0,
                ))
            self.assertIs(
                ctx.exception.stop_reason,
                CalibrationStopReason.CAP_WOULD_BE_EXCEEDED,
            )
            entries = ledger.entries()
            self.assertEqual(len(entries), 1)  # honestly accounted anyway


class TestDeadlines(unittest.TestCase):
    def test_authorized_deadline_constants(self) -> None:
        self.assertEqual(cl.DEV_STAGE_DEADLINE_SECONDS, 90 * 60)
        self.assertEqual(cl.HOLDOUT_STAGE_DEADLINE_SECONDS, 4 * 60 * 60)
        self.assertEqual(cl.TOTAL_RUN_DEADLINE_SECONDS, 6 * 60 * 60)

    def test_owner_wait_consumes_no_active_clock(self) -> None:
        clock = cl.ActiveExecutionClock()
        clock.begin_active_segment(at=1000.0)
        clock.end_active_segment(at=1600.0)  # 600s active
        # OWNER_WAIT gap 1600 -> 90000 does not count.
        clock.begin_active_segment(at=90_000.0)
        clock.end_active_segment(at=90_400.0)  # +400s
        self.assertEqual(clock.active_seconds(), 1000.0)

    def test_deadline_exceeded_stops_new_dispatch(self) -> None:
        clock = cl.ActiveExecutionClock()
        clock.begin_active_segment(at=0.0)
        clock.end_active_segment(at=cl.DEV_STAGE_DEADLINE_SECONDS + 1.0)
        with self.assertRaises(CalibrationStopError) as ctx:
            clock.check_stage_deadline(cl.DEV_STAGE_DEADLINE_SECONDS)
        self.assertIs(
            ctx.exception.stop_reason, CalibrationStopReason.DEADLINE_EXCEEDED
        )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
