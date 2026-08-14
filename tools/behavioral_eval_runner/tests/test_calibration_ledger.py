"""WP-2B-3 durable request/token/cost ledger (BER-DEC-008 decisions 17-20,
25-26; PR #88 correction families 2-3 and the overshoot subcase).

Deterministic and offline: no network, no provider object, integer nano-USD
money math only. The ledger is EVENT-SOURCED and single-file: every future
external interaction leaves a durable write-ahead ATTEMPT_STARTED event
before any transport use, a separate append-only terminal event afterwards,
and the whole work package continues ONE verified hash chain across
execution segments.
"""

from __future__ import annotations

import json
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
DATASET_SHA = "f" * 64


def _ledger(tmp: str, name: str = "ledger.jsonl") -> cl.CalibrationLedger:
    return cl.CalibrationLedger(
        os.path.join(tmp, name), declare_first_segment=True
    )


def _usage(inp: int = 1000, out: int = 2000, reasoning: int = 1500,
           cached: int = 0) -> cl.ProviderUsage:
    return cl.ProviderUsage(
        input_tokens=inp, output_tokens=out, reasoning_tokens=reasoning,
        cached_input_tokens=cached,
    )


def _reserve(ledger: cl.CalibrationLedger, judgment_id: str = "wp2b3-item-1",
             attempt: int = 1, est: int = 1000, out: int = 25000,
             day: str = "2026-08-20",
             retry_of: str | None = None) -> cl.Reservation:
    return ledger.reserve(
        kind=cl.RequestKind.JUDGMENT_ATTEMPT,
        logical_judgment_id=judgment_id,
        attempt_number=attempt,
        estimated_input_tokens=est,
        max_output_tokens=out,
        day=day,
        dataset_sha256=DATASET_SHA,
        stage="DEVELOPMENT",
        retry_of_request_id=retry_of,
    )


def _record_ok(ledger: cl.CalibrationLedger, reservation: cl.Reservation,
               usage: cl.ProviderUsage | None = None,
               outcome: str = "OUTPUT_RECEIVED_UNVALIDATED") -> cl.LedgerEntry:
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


def _events(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


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
        per_attempt = cl.worst_case_attempt_charge_nanousd()
        self.assertEqual(per_attempt, 790_000_000)
        self.assertEqual(200 * per_attempt, 158_000_000_000)

    def test_charge_calculation_is_integer_nanousd(self) -> None:
        charge = cl.calculate_charge_nanousd(_usage(inp=8000, out=25000))
        self.assertEqual(charge, 8000 * 5000 + 25000 * 30000)
        cached = cl.calculate_charge_nanousd(
            _usage(inp=1000, out=100, cached=400)
        )
        self.assertEqual(cached, 600 * 5000 + 400 * 500 + 100 * 30000)


class TestDurableLifecycle(unittest.TestCase):
    """Family 2: write-ahead STARTED events, explicit genesis, in-memory
    ledgers demoted to unit-test-only status."""

    def test_in_memory_ledger_is_marked_non_durable(self) -> None:
        ledger = cl.CalibrationLedger(None)
        self.assertFalse(ledger.is_durable)
        with tempfile.TemporaryDirectory() as tmp:
            durable = _ledger(tmp)
            self.assertTrue(durable.is_durable)

    def test_fresh_file_requires_explicit_first_segment_declaration(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(CalibrationLedgerError):
                cl.CalibrationLedger(os.path.join(tmp, "seg.jsonl"))

    def test_genesis_and_segment_events_open_the_chain(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "wp.jsonl")
            ledger = cl.CalibrationLedger(path, declare_first_segment=True)
            events = _events(path)
            kinds = [e["event_kind"] for e in events]
            self.assertEqual(kinds[0], "GENESIS")
            self.assertEqual(kinds[1], "SEGMENT_OPENED")
            self.assertEqual(events[0]["work_package"], "WP-2B-3")
            self.assertEqual(events[0]["authorization_id"], "BER-DEC-008")
            self.assertTrue(events[1]["run_id"])
            self.assertEqual(events[1]["run_id"], ledger.run_id)

    def test_reserve_appends_a_durable_started_event_before_any_use(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "wp.jsonl")
            ledger = cl.CalibrationLedger(path, declare_first_segment=True)
            reservation = _reserve(ledger, est=123, out=8192)
            started = [
                e for e in _events(path)
                if e["event_kind"] == "ATTEMPT_STARTED"
            ]
            self.assertEqual(len(started), 1)
            event = started[0]
            self.assertEqual(event["attempt_id"], reservation.reservation_id)
            self.assertEqual(event["logical_judgment_id"], "wp2b3-item-1")
            self.assertEqual(event["attempt_number"], 1)
            self.assertEqual(event["request_kind"], "JUDGMENT_ATTEMPT")
            self.assertEqual(event["authorized_model"], "gpt-5.5-2026-04-23")
            self.assertEqual(event["dataset_sha256"], DATASET_SHA)
            self.assertEqual(event["stage"], "DEVELOPMENT")
            self.assertEqual(event["estimated_input_tokens"], 123)
            self.assertEqual(event["max_output_tokens"], 8192)
            self.assertEqual(
                event["worst_case_charge_nanousd"],
                123 * 5000 + 8192 * 30000,
            )
            self.assertTrue(event["reserved_utc"])
            self.assertEqual(event["run_id"], ledger.run_id)

    def test_terminal_event_is_separate_and_started_is_never_rewritten(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "wp.jsonl")
            ledger = cl.CalibrationLedger(path, declare_first_segment=True)
            reservation = _reserve(ledger)
            before = _events(path)
            _record_ok(ledger, reservation)
            after = _events(path)
            self.assertEqual(after[: len(before)], before)  # append-only
            self.assertEqual(after[-1]["event_kind"], "ATTEMPT_TERMINAL")
            self.assertEqual(
                after[-1]["internal_request_id"],
                reservation.reservation_id,
            )

    def test_verify_chain_covers_all_events(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "wp.jsonl")
            ledger = cl.CalibrationLedger(path, declare_first_segment=True)
            _record_ok(ledger, _reserve(ledger, judgment_id="a", out=8192))
            _record_ok(ledger, _reserve(ledger, judgment_id="b", out=8192))
            count = cl.verify_ledger_chain(path)
            self.assertEqual(count, 6)  # GENESIS + SEGMENT + 2x(STARTED+TERM)
            with open(path, encoding="utf-8") as fh:
                first = fh.readline()
            with open(path, "a", encoding="utf-8") as fh:
                fh.write(first)
            with self.assertRaises(CalibrationLedgerError):
                cl.verify_ledger_chain(path)


class TestReservationsAndCaps(unittest.TestCase):
    def test_reservation_then_record_appends_an_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = _ledger(tmp)
            reservation = _reserve(ledger)
            entry = _record_ok(ledger, reservation)
            self.assertEqual(entry.cumulative.attempts_total, 1)
            self.assertEqual(entry.cumulative.total_external_requests, 1)
            self.assertEqual(entry.calculated_charge_nanousd,
                             1000 * 5000 + 2000 * 30000)
            self.assertTrue(
                entry.internal_request_id.startswith(f"{ledger.run_id}-att-")
            )

    def test_attempt_cap_denies_the_201st_judgment_attempt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = _ledger(tmp)
            for n in range(200):
                reservation = _reserve(
                    ledger, judgment_id=f"item-{n}", est=10, out=8192
                )
                _record_ok(ledger, reservation,
                           usage=_usage(inp=10, out=10, reasoning=0))
            with self.assertRaises(CalibrationReservationDenied):
                _reserve(ledger, judgment_id="overflow", est=10, out=8192)

    def test_metadata_cap_is_exactly_one(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = _ledger(tmp)
            reservation = ledger.reserve(
                kind=cl.RequestKind.METADATA, logical_judgment_id=None,
                attempt_number=1, estimated_input_tokens=0,
                max_output_tokens=0, day="2026-08-20",
                dataset_sha256=None, stage="DEVELOPMENT",
            )
            ledger.record(
                reservation, provider_response_id=None,
                provider_request_trace_id=None,
                requested_model="gpt-5.5-2026-04-23",
                returned_model="gpt-5.5-2026-04-23",
                request_timestamp_utc=T0, completion_timestamp_utc=T1,
                latency_ms=100, response_status="OK",
                incomplete_details_reason=None,
                usage=cl.ProviderUsage.zero(), outcome_kind="METADATA_OK",
            )
            with self.assertRaises(CalibrationReservationDenied):
                ledger.reserve(
                    kind=cl.RequestKind.METADATA, logical_judgment_id=None,
                    attempt_number=1, estimated_input_tokens=0,
                    max_output_tokens=0, day="2026-08-20",
                    dataset_sha256=None, stage="DEVELOPMENT",
                )

    def test_spend_cap_stops_before_the_cap_not_after(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = _ledger(tmp)
            reservation = _reserve(ledger, judgment_id="big", est=8000,
                                   out=25000)
            big_usage = cl.ProviderUsage(
                input_tokens=8000, output_tokens=5_820_000,
                reasoning_tokens=0, cached_input_tokens=0,
            )
            # 5.82M output stays under the reserved... it does not; use a
            # raw record with matching reservation ceiling via metadata-free
            # path: reserve with out=25000 but record big output is an
            # overshoot stop now, so drive spend with many attempts instead.
            with self.assertRaises(CalibrationStopError):
                _record_ok(ledger, reservation, usage=big_usage)
            # The overshoot entry was honestly recorded and spend counted:
            spent = ledger.cumulative().spend_nanousd_total
            self.assertGreater(spent, 174_000_000_000)
            headroom = cl.MAX_TOTAL_SPEND_NANOUSD - spent
            self.assertLess(headroom, cl.worst_case_attempt_charge_nanousd())
            with self.assertRaises(CalibrationReservationDenied):
                _reserve(ledger, judgment_id="overflow", est=8000, out=25000)

    def test_input_token_budget_denied_at_reservation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = _ledger(tmp)
            with self.assertRaises(CalibrationReservationDenied):
                _reserve(ledger, judgment_id="too-big", est=8001, out=25000)
            with self.assertRaises(CalibrationReservationDenied):
                _reserve(ledger, judgment_id="out-too-big", est=100,
                         out=25001)

    def test_reservation_is_single_use(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = _ledger(tmp)
            reservation = _reserve(ledger, est=10, out=8192)
            _record_ok(ledger, reservation)
            with self.assertRaises(CalibrationLedgerError):
                _record_ok(ledger, reservation)


class TestTelemetryAndBillingUnknown(unittest.TestCase):
    def test_missing_monetary_telemetry_is_a_stop(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = _ledger(tmp)
            reservation = _reserve(ledger, judgment_id="no-usage", est=100,
                                   out=25000)
            with self.assertRaises(CalibrationStopError) as ctx:
                ledger.record(
                    reservation, provider_response_id="resp-x",
                    provider_request_trace_id=None,
                    requested_model="gpt-5.5-2026-04-23",
                    returned_model="gpt-5.5-2026-04-23",
                    request_timestamp_utc=T0, completion_timestamp_utc=T1,
                    latency_ms=10, response_status="completed",
                    incomplete_details_reason=None, usage=None,
                    outcome_kind="STOP_TELEMETRY_UNAVAILABLE",
                )
            self.assertIs(ctx.exception.stop_reason,
                          CalibrationStopReason.BUDGET_TELEMETRY_UNAVAILABLE)
            entries = ledger.entries()
            self.assertEqual(len(entries), 1)
            self.assertTrue(entries[-1].telemetry_missing)
            self.assertEqual(entries[-1].calculated_charge_nanousd,
                             100 * 5000 + 25000 * 30000)

    def test_billing_unknown_failure_charges_worst_case_without_stop(self) -> None:
        """Family 2 invariant 6: a boundary-uncertain failure is never
        recorded as known zero billing — it carries the reserved worst
        case, marked unknown, and (unlike missing success telemetry) the
        lawful runner retry may still proceed."""
        with tempfile.TemporaryDirectory() as tmp:
            ledger = _ledger(tmp)
            reservation = _reserve(ledger, judgment_id="t-1", est=100,
                                   out=8192)
            entry = ledger.record(
                reservation, provider_response_id=None,
                provider_request_trace_id=None,
                requested_model="gpt-5.5-2026-04-23", returned_model=None,
                request_timestamp_utc=T0, completion_timestamp_utc=T1,
                latency_ms=15000, response_status="TIMEOUT",
                incomplete_details_reason=None, usage=None,
                outcome_kind="TRANSPORT_TIMEOUT", billing_unknown=True,
            )
            self.assertTrue(entry.billing_unknown)
            self.assertEqual(entry.calculated_charge_nanousd,
                             100 * 5000 + 8192 * 30000)
            self.assertEqual(
                ledger.cumulative().spend_nanousd_total,
                entry.calculated_charge_nanousd,
            )

    def test_known_zero_requires_explicit_zero_usage(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = _ledger(tmp)
            reservation = _reserve(ledger, est=10, out=8192)
            entry = _record_ok(ledger, reservation,
                               usage=cl.ProviderUsage.zero(),
                               outcome="STOP_PROVIDER_AUTH_REJECTED")
            self.assertFalse(entry.billing_unknown)
            self.assertEqual(entry.calculated_charge_nanousd, 0)

    def test_retry_attempts_have_unique_ids_and_linkage(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = _ledger(tmp)
            first = _reserve(ledger, judgment_id="item-r", est=10, out=8192)
            entry1 = ledger.record(
                first, provider_response_id=None,
                provider_request_trace_id=None,
                requested_model="gpt-5.5-2026-04-23", returned_model=None,
                request_timestamp_utc=T0, completion_timestamp_utc=T1,
                latency_ms=15000, response_status="TIMEOUT",
                incomplete_details_reason=None, usage=None,
                outcome_kind="TRANSPORT_TIMEOUT", billing_unknown=True,
            )
            second = _reserve(ledger, judgment_id="item-r", attempt=2,
                              est=10, out=8192,
                              retry_of=entry1.internal_request_id)
            entry2 = _record_ok(ledger, second)
            self.assertNotEqual(entry1.internal_request_id,
                                entry2.internal_request_id)
            self.assertEqual(entry2.retry_of_request_id,
                             entry1.internal_request_id)
            self.assertEqual(entry2.cumulative.attempts_total, 2)

    def test_third_attempt_for_one_judgment_is_denied(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = _ledger(tmp)
            for attempt in (1, 2):
                reservation = _reserve(ledger, judgment_id="item-x",
                                       attempt=attempt, est=10, out=8192)
                ledger.record(
                    reservation, provider_response_id=None,
                    provider_request_trace_id=None,
                    requested_model="gpt-5.5-2026-04-23",
                    returned_model=None, request_timestamp_utc=T0,
                    completion_timestamp_utc=T1, latency_ms=1,
                    response_status="TIMEOUT",
                    incomplete_details_reason=None, usage=None,
                    outcome_kind="TRANSPORT_TIMEOUT", billing_unknown=True,
                )
            with self.assertRaises(CalibrationReservationDenied):
                _reserve(ledger, judgment_id="item-x", attempt=2, est=10,
                         out=8192)


class TestOvershootStops(unittest.TestCase):
    """Family 2 folded subcase: input, output, and actual-charge overshoot
    are honest recorded STOPs."""

    def test_provider_reported_input_over_budget_is_recorded_stop(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = _ledger(tmp)
            reservation = _reserve(ledger, judgment_id="over", est=100,
                                   out=8192)
            with self.assertRaises(CalibrationStopError) as ctx:
                _record_ok(ledger, reservation, usage=cl.ProviderUsage(
                    input_tokens=9000, output_tokens=10,
                    reasoning_tokens=0, cached_input_tokens=0,
                ))
            self.assertIs(ctx.exception.stop_reason,
                          CalibrationStopReason.CAP_WOULD_BE_EXCEEDED)
            self.assertEqual(len(ledger.entries()), 1)

    def test_output_tokens_above_reserved_ceiling_is_recorded_stop(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = _ledger(tmp)
            reservation = _reserve(ledger, judgment_id="out-over", est=100,
                                   out=8192)
            with self.assertRaises(CalibrationStopError) as ctx:
                _record_ok(ledger, reservation, usage=cl.ProviderUsage(
                    input_tokens=100, output_tokens=8193,
                    reasoning_tokens=0, cached_input_tokens=0,
                ))
            self.assertIs(ctx.exception.stop_reason,
                          CalibrationStopReason.CAP_WOULD_BE_EXCEEDED)
            entries = ledger.entries()
            self.assertEqual(len(entries), 1)  # honestly recorded first
            self.assertEqual(entries[0].output_tokens, 8193)

    def test_actual_charge_breaching_a_hard_ceiling_is_recorded_stop(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = _ledger(tmp)
            reservation = _reserve(ledger, judgment_id="charge-over",
                                   est=8000, out=25000)
            breach = cl.ProviderUsage(
                input_tokens=8000, output_tokens=5_840_000,
                reasoning_tokens=0, cached_input_tokens=0,
            )
            self.assertGreater(
                cl.calculate_charge_nanousd(breach),
                cl.MAX_TOTAL_SPEND_NANOUSD,
            )
            with self.assertRaises(CalibrationStopError) as ctx:
                _record_ok(ledger, reservation, usage=breach)
            self.assertIs(ctx.exception.stop_reason,
                          CalibrationStopReason.CAP_WOULD_BE_EXCEEDED)
            self.assertEqual(len(ledger.entries()), 1)


class TestCrashOrphanRecovery(unittest.TestCase):
    """Family 2 invariant 3: a STARTED attempt with no terminal event is an
    ORPHAN — never forgotten, never reissued, conservatively charged."""

    def _crash_after_started(self, tmp: str) -> str:
        path = os.path.join(tmp, "wp.jsonl")
        ledger = cl.CalibrationLedger(path, declare_first_segment=True)
        _reserve(ledger, judgment_id="orphaned-item", est=100, out=8192)
        return path  # simulated crash: no record() ever happens

    def test_restart_detects_the_orphan(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = self._crash_after_started(tmp)
            resumed = cl.CalibrationLedger(path)
            self.assertEqual(len(resumed.orphaned_attempt_ids), 1)

    def test_orphan_counts_against_every_ceiling(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = self._crash_after_started(tmp)
            resumed = cl.CalibrationLedger(path)
            cumulative = resumed.cumulative()
            self.assertEqual(cumulative.attempts_total, 1)
            self.assertEqual(cumulative.total_external_requests, 1)
            self.assertEqual(cumulative.spend_nanousd_total,
                             100 * 5000 + 8192 * 30000)

    def test_orphan_blocks_further_reservation_pending_review(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = self._crash_after_started(tmp)
            resumed = cl.CalibrationLedger(path)
            with self.assertRaises(CalibrationStopError) as ctx:
                _reserve(resumed, judgment_id="another")
            self.assertIs(ctx.exception.stop_reason,
                          CalibrationStopReason.BUDGET_TELEMETRY_UNAVAILABLE)

    def test_orphan_identity_is_never_reused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = self._crash_after_started(tmp)
            events = _events(path)
            orphan_id = [
                e for e in events if e["event_kind"] == "ATTEMPT_STARTED"
            ][0]["attempt_id"]
            resumed = cl.CalibrationLedger(path)
            self.assertIn(orphan_id, resumed.orphaned_attempt_ids)
            self.assertNotEqual(resumed.run_id, events[1]["run_id"])


class TestCrossSegmentContinuity(unittest.TestCase):
    """Family 2 invariant 4: ONE continuously appendable verified ledger —
    a later segment reopens the same file, verifies the complete chain, and
    can never silently reset the work-package totals."""

    def _seed(self, path: str, judgment_id: str = "j-1",
              attempts: int = 1) -> None:
        ledger = cl.CalibrationLedger(path, declare_first_segment=True)
        for attempt in range(1, attempts + 1):
            reservation = _reserve(ledger, judgment_id=judgment_id,
                                   attempt=attempt, est=10, out=8192)
            _record_ok(ledger, reservation,
                       usage=_usage(inp=10, out=10, reasoning=0))

    def test_reopening_carries_all_totals(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "wp.jsonl")
            self._seed(path, judgment_id="j-1", attempts=2)
            resumed = cl.CalibrationLedger(path)
            cumulative = resumed.cumulative()
            self.assertEqual(cumulative.attempts_total, 2)
            self.assertEqual(cumulative.total_external_requests, 2)
            self.assertEqual(cumulative.judgments_total, 1)
            self.assertGreater(cumulative.spend_nanousd_total, 0)

    def test_per_judgment_attempt_cap_survives_segments(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "wp.jsonl")
            self._seed(path, judgment_id="j-x", attempts=2)
            resumed = cl.CalibrationLedger(path)
            with self.assertRaises(CalibrationReservationDenied):
                _reserve(resumed, judgment_id="j-x", attempt=2, est=10,
                         out=8192, day="2026-08-21")

    def test_metadata_cap_survives_segments(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "wp.jsonl")
            ledger = cl.CalibrationLedger(path, declare_first_segment=True)
            reservation = ledger.reserve(
                kind=cl.RequestKind.METADATA, logical_judgment_id=None,
                attempt_number=1, estimated_input_tokens=0,
                max_output_tokens=0, day="2026-08-20",
                dataset_sha256=None, stage="DEVELOPMENT",
            )
            ledger.record(
                reservation, provider_response_id=None,
                provider_request_trace_id=None,
                requested_model="gpt-5.5-2026-04-23",
                returned_model="gpt-5.5-2026-04-23",
                request_timestamp_utc=T0, completion_timestamp_utc=T1,
                latency_ms=5, response_status="OK",
                incomplete_details_reason=None,
                usage=cl.ProviderUsage.zero(), outcome_kind="METADATA_OK",
            )
            resumed = cl.CalibrationLedger(path)
            with self.assertRaises(CalibrationReservationDenied):
                resumed.reserve(
                    kind=cl.RequestKind.METADATA, logical_judgment_id=None,
                    attempt_number=1, estimated_input_tokens=0,
                    max_output_tokens=0, day="2026-08-21",
                    dataset_sha256=None, stage="DEVELOPMENT",
                )

    def test_spend_ceiling_survives_segments_even_on_a_new_day(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "wp.jsonl")
            ledger = cl.CalibrationLedger(path, declare_first_segment=True)
            reservation = _reserve(ledger, judgment_id="big", est=8000,
                                   out=25000)
            near_cap = cl.ProviderUsage(
                input_tokens=8000, output_tokens=5_810_000,
                reasoning_tokens=0, cached_input_tokens=0,
            )
            with self.assertRaises(CalibrationStopError):
                # output ceiling overshoot records + stops; spend recorded
                _record_ok(ledger, reservation, usage=near_cap)
            resumed = cl.CalibrationLedger(path)
            self.assertEqual(
                resumed.cumulative().spend_nanousd_total,
                8000 * 5000 + 5_810_000 * 30_000,
            )
            with self.assertRaises(CalibrationReservationDenied):
                _reserve(resumed, judgment_id="overflow", est=8000,
                         out=25000, day="2026-08-21")

    def test_attempt_ids_do_not_collide_across_segments(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "wp.jsonl")
            self._seed(path, judgment_id="j-1", attempts=1)
            resumed = cl.CalibrationLedger(path)
            reservation = _reserve(resumed, judgment_id="j-2", est=10,
                                   out=8192)
            _record_ok(resumed, reservation,
                       usage=_usage(inp=10, out=10, reasoning=0))
            started_ids = [
                e["attempt_id"] for e in _events(path)
                if e["event_kind"] == "ATTEMPT_STARTED"
            ]
            self.assertEqual(len(started_ids), len(set(started_ids)))
            run_ids = {
                e["run_id"] for e in _events(path)
                if e["event_kind"] == "SEGMENT_OPENED"
            }
            self.assertEqual(len(run_ids), 2)

    def test_tampered_chain_is_rejected_on_reopen(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "wp.jsonl")
            self._seed(path)
            with open(path, encoding="utf-8") as fh:
                first = fh.readline()
            with open(path, "a", encoding="utf-8") as fh:
                fh.write(first)
            with self.assertRaises(CalibrationLedgerError):
                cl.CalibrationLedger(path)


class TestPersistentDeadlines(unittest.TestCase):
    """Family 3: active-execution deadlines live in the same durable chain
    and survive restarts; OWNER_WAIT contributes zero."""

    def test_authorized_deadline_constants(self) -> None:
        self.assertEqual(cl.DEV_STAGE_DEADLINE_SECONDS, 90 * 60)
        self.assertEqual(cl.HOLDOUT_STAGE_DEADLINE_SECONDS, 4 * 60 * 60)
        self.assertEqual(cl.TOTAL_RUN_DEADLINE_SECONDS, 6 * 60 * 60)

    def test_active_segments_are_durable_events(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "wp.jsonl")
            ledger = cl.CalibrationLedger(path, declare_first_segment=True)
            ledger.begin_active_segment("DEVELOPMENT", at=1000.0)
            ledger.end_active_segment(at=1600.0)
            kinds = [e["event_kind"] for e in _events(path)]
            self.assertIn("ACTIVE_SEGMENT_BEGIN", kinds)
            self.assertIn("ACTIVE_SEGMENT_END", kinds)

    def test_owner_wait_consumes_no_active_clock(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = _ledger(tmp)
            ledger.begin_active_segment("DEVELOPMENT", at=1000.0)
            ledger.end_active_segment(at=1600.0)  # 600 s active
            ledger.begin_active_segment("DEVELOPMENT", at=90_000.0)
            ledger.end_active_segment(at=90_400.0)  # +400 s
            self.assertEqual(ledger.active_seconds(), 1000.0)

    def test_restart_preserves_prior_active_time(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "wp.jsonl")
            ledger = cl.CalibrationLedger(path, declare_first_segment=True)
            ledger.begin_active_segment("DEVELOPMENT", at=0.0)
            ledger.end_active_segment(at=4000.0)
            resumed = cl.CalibrationLedger(path)
            self.assertEqual(resumed.active_seconds(), 4000.0)
            self.assertEqual(
                resumed.stage_active_seconds("DEVELOPMENT"), 4000.0
            )

    def test_stage_deadline_exceeded_stops_new_dispatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = _ledger(tmp)
            ledger.begin_active_segment("DEVELOPMENT", at=0.0)
            ledger.end_active_segment(
                at=cl.DEV_STAGE_DEADLINE_SECONDS + 1.0
            )
            with self.assertRaises(CalibrationStopError) as ctx:
                ledger.check_deadlines("DEVELOPMENT")
            self.assertIs(ctx.exception.stop_reason,
                          CalibrationStopReason.DEADLINE_EXCEEDED)

    def test_total_run_deadline_binds_while_stage_has_room(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = _ledger(tmp)
            # An over-run recorded development history: 5.5 hours active.
            ledger.begin_active_segment("DEVELOPMENT", at=0.0)
            ledger.end_active_segment(at=5.5 * 3600)
            # Holdout stage itself has room (1 h < 4 h)...
            ledger.begin_active_segment("SEALED_HOLDOUT", at=6.0 * 3600)
            ledger.end_active_segment(at=7.0 * 3600)
            self.assertLess(
                ledger.stage_active_seconds("SEALED_HOLDOUT"),
                cl.HOLDOUT_STAGE_DEADLINE_SECONDS,
            )
            # ...but the 6-hour WHOLE-RUN active limit is already breached.
            with self.assertRaises(CalibrationStopError) as ctx:
                ledger.check_deadlines("SEALED_HOLDOUT")
            self.assertIs(ctx.exception.stop_reason,
                          CalibrationStopReason.DEADLINE_EXCEEDED)

    def test_open_segment_counts_via_now_and_survives_crash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "wp.jsonl")
            ledger = cl.CalibrationLedger(path, declare_first_segment=True)
            ledger.begin_active_segment("DEVELOPMENT", at=100.0)
            self.assertEqual(ledger.active_seconds(now=700.0), 600.0)
            resumed = cl.CalibrationLedger(path)  # crash with open segment
            self.assertEqual(resumed.active_seconds(now=800.0), 700.0)

    def test_deadline_denial_appends_stop_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "wp.jsonl")
            ledger = cl.CalibrationLedger(path, declare_first_segment=True)
            ledger.begin_active_segment("DEVELOPMENT", at=0.0)
            ledger.end_active_segment(
                at=cl.DEV_STAGE_DEADLINE_SECONDS + 5.0
            )
            with self.assertRaises(CalibrationStopError):
                ledger.check_deadlines("DEVELOPMENT")
            kinds = [e["event_kind"] for e in _events(path)]
            self.assertIn("DEADLINE_STOP", kinds)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
