"""Evidence-preserving recovery of the failed Pilot A ledger point.

The fixture ledger is the REAL ledger artifact of failed Pilot A run
41145221349 (case pilot-a-01 attempt 1): one charged call, `reconciled: false`,
8 cents, halt reason TRANSPORT_ERROR because the provider response was truncated
at the 512-token cap (status max_tokens). No raw provider content is in a
ledger, so committing it as a test fixture adds no secret.

These tests prove the committed state and the transition it depends on:

* before reconciliation the summary guard sees 1 unreconciled entry and would
  refuse a further paid dispatch (this is the block raising max_tokens cannot
  clear);
* the committed record binds to the exact ledger and is ATTESTED by the owner
  (attestation 2026-10-30 21:02 PDT), so it reconciles the entry while
  preserving the ledger bytes, the charge (8 cents), the remaining ceiling
  (11,992 cents) and the attempt history: nothing is deleted, reset or
  repriced;
* a synthetic PENDING record that binds to the same ledger is still refused as
  NOT_ATTESTED - the guard is not weakened by the committed record becoming
  ATTESTED - and a synthetic ATTESTED record proves the same transition offline.
"""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from tools.behavioral_eval_runner.live.ledger_reconciliation import (
    STATUS_ATTESTED,
    STATUS_PENDING,
    LedgerReconciliationRefusedError,
    ledger_sha256,
    load_record,
    load_records,
    reconcile_ledger,
    remaining_unreconciled,
    unreconciled_calls,
    validate_record,
)
from tools.behavioral_eval_runner.tests.live_helpers import PACKAGE_ROOT, REPO_ROOT

FIXTURES = Path(PACKAGE_ROOT) / "tests" / "fixtures" / "live" / "reconciliation"
LEDGER_FIXTURE = FIXTURES / "ledger-pilot-a-41145221349-attempt1.json"
ATTESTED_FIXTURE = FIXTURES / "reconciliation-attested-41145221349.json"
COMMITTED_RECORD = (
    Path(PACKAGE_ROOT) / "live" / "reconciliation" / "pilot-a-41145221349-attempt1.json"
)
CALL_REF = (
    "pilot-a-01-agent-startup-context-gate:WITH_SKILL:run-1:subject:anthropic"
)


def _ledger():
    return json.loads(LEDGER_FIXTURE.read_text(encoding="utf-8"))


def _committed():
    return json.loads(COMMITTED_RECORD.read_text(encoding="utf-8"))


def _pending_record():
    """A synthetic PENDING record derived from the committed ATTESTED record.

    The committed record is now ATTESTED, but the fail-closed rule for an
    unattested record still has to be proven. This copy carries no attestation
    fields and an explicitly synthetic evidence_ref, so it can never be
    mistaken for the owner's attestation.
    """
    record = _committed()
    record["status"] = STATUS_PENDING
    record["attested_by"] = ""
    record["attested_on"] = ""
    record["attestation_ref"] = ""
    record["reconciles"][0]["evidence_ref"] = (
        "SYNTHETIC TEST RECORD ONLY: the committed ATTESTED record reversed to "
        "PENDING to prove the guard still refuses an unattested record"
    )
    return record


def _attested():
    return json.loads(ATTESTED_FIXTURE.read_text(encoding="utf-8"))


class FailedRunFixtureTests(unittest.TestCase):
    def test_the_fixture_is_the_real_failed_run_ledger_shape(self):
        ledger = _ledger()
        self.assertEqual(ledger["ledger_kind"], "ber-live-cost-ledger")
        self.assertEqual(ledger["spent_cents"], 8)
        self.assertEqual(ledger["ceiling_cents"], 12000)
        self.assertEqual(ledger["call_count"], 1)
        self.assertEqual(ledger["unreconciled_count"], 1)
        unreconciled = unreconciled_calls(ledger)
        self.assertEqual(len(unreconciled), 1)
        self.assertEqual(unreconciled[0]["call_ref"], CALL_REF)
        self.assertEqual(unreconciled[0]["reason_code"], "TRANSPORT_ERROR")
        self.assertIn("max_tokens", unreconciled[0]["detail"])
        self.assertEqual(ledger_sha256(LEDGER_FIXTURE.read_bytes()),
                         "d9390d5a98483e0ac7abb24bb959af9f3e6ad927b1a2a75e5eb1bfe73fb0c989")


class CommittedRecordTests(unittest.TestCase):
    def test_committed_record_is_attested_and_reconciles_preserving_spend(self):
        record = load_record(COMMITTED_RECORD)
        self.assertEqual(record["status"], STATUS_ATTESTED)
        self.assertTrue(record["attested_by"].strip())
        self.assertTrue(record["attested_on"].strip())
        self.assertTrue(record["attestation_ref"].strip())
        # The attestation names the run it settles and the preserved figures.
        self.assertIn("41145221349", record["attestation_ref"])
        self.assertIn("11,992", record["attestation_ref"])
        self.assertIn("no other paid dispatch", record["attestation_ref"])
        self.assertEqual(
            record["ledger_sha256"],
            ledger_sha256(LEDGER_FIXTURE.read_bytes()),
        )
        self.assertEqual(record["spent_cents_preserved"], 8)
        self.assertEqual(record["ceiling_cents_preserved"], 12000)
        self.assertEqual(record["budget_impact"]["charged_cents_preserved"], 8)
        self.assertEqual(
            record["budget_impact"]["remaining_ceiling_cents_preserved"], 11992
        )
        self.assertIs(record["budget_impact"]["cumulative_ceiling_cents_unchanged"], True)
        self.assertEqual(record["budget_impact"]["refunded_cents"], 0)
        self.assertEqual(record["reconciles"][0]["reserved_cents"], 8)
        self.assertEqual(record["reconciles"][0]["charged_cents"], 8)
        self.assertEqual(record["reconciles"][0]["disposition"], "PRESERVED_AND_ACCEPTED")

        ledger = _ledger()
        ledger_copy = copy.deepcopy(ledger)
        raw = LEDGER_FIXTURE.read_bytes()
        view = reconcile_ledger(ledger, record, ledger_bytes=raw)
        self.assertEqual(view["unreconciled_before"], 1)
        self.assertEqual(view["unreconciled_after"], 0)
        self.assertEqual(view["spent_cents_preserved"], 8)
        self.assertEqual(view["ceiling_cents_preserved"], 12000)
        self.assertEqual(view["remaining_ceiling_cents_preserved"], 11992)
        self.assertEqual(view["calls_preserved"], 1)
        self.assertEqual(view["reconciled_call_refs"], [CALL_REF])
        self.assertEqual(view["refunded_cents"], 0)
        self.assertEqual(view["deleted_entries"], 0)
        self.assertEqual(view["attested_by"], record["attested_by"])
        # Nothing is mutated or rewritten: the ledger dict and the file bytes
        # are unchanged after reconciliation, and the charge is counted once.
        self.assertEqual(ledger, ledger_copy)
        self.assertEqual(LEDGER_FIXTURE.read_bytes(), raw)
        self.assertEqual(
            sum(call["cost_cents"] for call in ledger["calls"]),
            view["spent_cents_preserved"],
        )
        self.assertEqual(remaining_unreconciled(ledger, record, ledger_bytes=raw), 0)

    def test_a_synthetic_pending_record_binds_to_the_ledger_and_is_refused(self):
        pending = _pending_record()
        self.assertEqual(validate_record(pending)["status"], STATUS_PENDING)
        self.assertEqual(
            pending["ledger_sha256"],
            ledger_sha256(LEDGER_FIXTURE.read_bytes()),
        )
        self.assertEqual(pending["spent_cents_preserved"], 8)
        self.assertEqual(
            pending["budget_impact"]["remaining_ceiling_cents_preserved"], 11992
        )
        with self.assertRaises(LedgerReconciliationRefusedError) as caught:
            reconcile_ledger(
                _ledger(), pending, ledger_bytes=LEDGER_FIXTURE.read_bytes()
            )
        self.assertEqual(
            caught.exception.reason_code, "RECONCILIATION_NOT_ATTESTED"
        )

    def test_a_pending_record_cannot_carry_attestation_fields(self):
        record = _pending_record()
        record["attested_by"] = "not allowed while pending"
        with self.assertRaises(LedgerReconciliationRefusedError) as caught:
            validate_record(record)
        self.assertEqual(caught.exception.reason_code, "RECONCILIATION_RECORD_INVALID")

    def test_no_record_means_the_guard_stays_blocked(self):
        ledger = _ledger()
        self.assertEqual(
            remaining_unreconciled(
                ledger, None, ledger_bytes=LEDGER_FIXTURE.read_bytes()
            ),
            1,
        )

    def test_committed_attested_record_is_the_only_record_for_that_ledger(self):
        records = load_records(Path(PACKAGE_ROOT) / "live" / "reconciliation")
        self.assertEqual(len(records), 1)
        committed = records[ledger_sha256(LEDGER_FIXTURE.read_bytes())]
        self.assertEqual(committed["status"], STATUS_ATTESTED)
        self.assertEqual(
            remaining_unreconciled(
                _ledger(), committed, ledger_bytes=LEDGER_FIXTURE.read_bytes()
            ),
            0,
        )


class AttestedTransitionTests(unittest.TestCase):
    def test_attested_reconciliation_preserves_spend_history_and_bytes(self):
        ledger = _ledger()
        ledger_copy = copy.deepcopy(ledger)
        raw = LEDGER_FIXTURE.read_bytes()
        view = reconcile_ledger(
            ledger, _attested(), ledger_bytes=raw
        )
        self.assertEqual(view["unreconciled_before"], 1)
        self.assertEqual(view["unreconciled_after"], 0)
        self.assertEqual(view["spent_cents_preserved"], 8)
        self.assertEqual(view["ceiling_cents_preserved"], 12000)
        self.assertEqual(view["remaining_ceiling_cents_preserved"], 11992)
        self.assertEqual(view["calls_preserved"], 1)
        self.assertEqual(view["reconciled_call_refs"], [CALL_REF])
        self.assertEqual(view["refunded_cents"], 0)
        self.assertEqual(view["deleted_entries"], 0)
        # Nothing is mutated or rewritten: the ledger dict and the file bytes
        # are the same objects/values after reconciliation.
        self.assertEqual(ledger, ledger_copy)
        self.assertEqual(LEDGER_FIXTURE.read_bytes(), raw)
        self.assertEqual(
            sum(call["cost_cents"] for call in ledger["calls"]),
            view["spent_cents_preserved"],
        )

    def test_guard_transitions_from_blocked_to_clear_on_attestation(self):
        ledger = _ledger()
        raw = LEDGER_FIXTURE.read_bytes()
        self.assertNotEqual(
            remaining_unreconciled(ledger, None, ledger_bytes=raw), 0
        )
        with self.assertRaises(LedgerReconciliationRefusedError) as caught:
            remaining_unreconciled(ledger, _pending_record(), ledger_bytes=raw)
        self.assertEqual(
            caught.exception.reason_code, "RECONCILIATION_NOT_ATTESTED"
        )
        self.assertEqual(
            remaining_unreconciled(ledger, _attested(), ledger_bytes=raw), 0
        )
        self.assertEqual(
            remaining_unreconciled(ledger, _committed(), ledger_bytes=raw), 0
        )


class FailClosedTests(unittest.TestCase):
    def _refused(self, record, *, ledger=None, raw=None, code=None):
        ledger = ledger if ledger is not None else _ledger()
        raw = raw if raw is not None else LEDGER_FIXTURE.read_bytes()
        with self.assertRaises(LedgerReconciliationRefusedError) as caught:
            reconcile_ledger(ledger, record, ledger_bytes=raw)
        if code is not None:
            self.assertEqual(caught.exception.reason_code, code)
        return caught.exception

    def test_ledger_bytes_that_do_not_match_the_record_are_refused(self):
        self._refused(
            _attested(),
            raw=LEDGER_FIXTURE.read_bytes() + b" ",
            code="RECONCILIATION_LEDGER_MISMATCH",
        )

    def test_a_repriced_charge_is_refused(self):
        record = _attested()
        record["reconciles"][0]["charged_cents"] = 7
        with self.assertRaises(LedgerReconciliationRefusedError) as caught:
            validate_record(record)
        self.assertEqual(caught.exception.reason_code, "RECONCILIATION_ENTRY_MISMATCH")

    def test_a_changed_reservation_is_refused(self):
        record = _attested()
        record["reconciles"][0]["reserved_cents"] = 9
        ledger = _ledger()
        record["reconciles"][0]["charged_cents"] = 9
        with self.assertRaises(LedgerReconciliationRefusedError) as caught:
            reconcile_ledger(ledger, record, ledger_bytes=LEDGER_FIXTURE.read_bytes())
        self.assertEqual(caught.exception.reason_code, "RECONCILIATION_ENTRY_MISMATCH")

    def test_a_record_covering_the_wrong_call_is_incomplete(self):
        record = _attested()
        record["reconciles"][0]["call_ref"] = "some-other-call"
        self._refused(record, code="RECONCILIATION_INCOMPLETE")

    def test_a_duplicate_claim_is_refused(self):
        record = _attested()
        record["unreconciled_before"] = 2
        record["reconciles"] = [record["reconciles"][0], dict(record["reconciles"][0])]
        with self.assertRaises(LedgerReconciliationRefusedError) as caught:
            validate_record(record)
        self.assertEqual(caught.exception.reason_code, "RECONCILIATION_DUPLICATE")

    def test_a_record_that_changes_the_preserved_spend_is_refused(self):
        record = _attested()
        record["spent_cents_preserved"] = 9
        record["budget_impact"]["charged_cents_preserved"] = 9
        self._refused(record, code="RECONCILIATION_BUDGET_MISMATCH")

    def test_a_record_with_a_wrong_remaining_ceiling_is_refused(self):
        record = _attested()
        record["budget_impact"]["remaining_ceiling_cents_preserved"] = 11991
        self._refused(record, code="RECONCILIATION_BUDGET_MISMATCH")

    def test_a_refund_is_never_accepted(self):
        record = _attested()
        record["budget_impact"]["refunded_cents"] = 8
        with self.assertRaises(LedgerReconciliationRefusedError) as caught:
            validate_record(record)
        self.assertEqual(caught.exception.reason_code, "RECONCILIATION_BUDGET_MISMATCH")

    def test_an_unknown_record_key_is_refused(self):
        record = _attested()
        record["delete_ledger"] = True
        with self.assertRaises(LedgerReconciliationRefusedError) as caught:
            validate_record(record)
        self.assertEqual(caught.exception.reason_code, "RECONCILIATION_RECORD_INVALID")

    def test_a_non_allowlisted_status_is_refused(self):
        record = _attested()
        record["status"] = "WAIVED"
        with self.assertRaises(LedgerReconciliationRefusedError) as caught:
            validate_record(record)
        self.assertEqual(caught.exception.reason_code, "RECONCILIATION_RECORD_INVALID")

    def test_an_attested_record_without_an_attestor_is_refused(self):
        record = _attested()
        record["attested_by"] = ""
        with self.assertRaises(LedgerReconciliationRefusedError) as caught:
            validate_record(record)
        self.assertEqual(caught.exception.reason_code, "RECONCILIATION_RECORD_INVALID")

    def test_two_records_claiming_one_ledger_are_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "a.json").write_text(
                json.dumps(_attested()), encoding="utf-8"
            )
            (target / "b.json").write_text(
                json.dumps(_attested()), encoding="utf-8"
            )
            with self.assertRaises(LedgerReconciliationRefusedError) as caught:
                load_records(target)
            self.assertEqual(caught.exception.reason_code, "RECONCILIATION_DUPLICATE")


if __name__ == "__main__":
    unittest.main()
