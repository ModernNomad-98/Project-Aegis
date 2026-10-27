"""Lifecycle tests: admission, replay, retention, deletion and expiry."""

import importlib.util
import json
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.aegis_usage import aggregate, local_report  # noqa: E402

S = local_report
A = aggregate
START = "2026-01-05"


def add_days(start, days):
    return (date.fromisoformat(start) + timedelta(days=days)).isoformat()


def prepare(start=START, issued=None, events=None):
    store = S.new_store()
    workflow = S.enable_capture(store, day=issued or start, start_day=start)
    for index, event in enumerate(events or [{"kind": "observation", "value": "ongoing", "effective_day": start}]):
        S.record_transition(
            store,
            workflow["workflow_ref"],
            kind=event["kind"],
            value=event["value"],
            effective_day=event["effective_day"],
            stage=event.get("stage"),
            event_ref="evt-" + format(index, "032x"),
        )
    notice = {
        "workflow_ref": workflow["workflow_ref"],
        "start_day": start,
        "applicable_stages": workflow["applicable_stages"],
        "criteria_frozen_before_work": True,
        "criteria_contract_ref": workflow["criteria_contract_ref"],
    }
    central = A.new_store()
    admission = A.issue_admission(central, notice, issued_day=issued or start)
    workflow["admission_ref"] = admission["admission_ref"]
    return store, central, workflow["workflow_ref"], admission


def payload_for(store, workflow_ref):
    return S.preview_export(store, workflow_ref)[0]


class AdmissionTests(unittest.TestCase):
    def test_import_without_an_admission_never_enrolls(self):
        store, central, workflow_ref, admission = prepare()
        payload = json.loads(payload_for(store, workflow_ref))
        payload["admission_ref"] = "adm-" + "9" * 32
        before = json.dumps(central, sort_keys=True)
        with self.assertRaises(S.ContractError) as caught:
            A.import_export(central, payload, capability=admission["capability"], receipt_day=add_days(START, 2))
        self.assertEqual(caught.exception.code, "unknown_admission")
        self.assertEqual(json.dumps(central, sort_keys=True), before)
        self.assertEqual(central["records"], {})
        self.assertEqual(len(central["admissions"]), 1)

    def test_admission_reference_alone_cannot_enroll(self):
        store, central, workflow_ref, admission = prepare()
        payload = payload_for(store, workflow_ref)
        fake = "adm-" + "b" * 32
        rewritten = json.loads(payload)
        rewritten["admission_ref"] = fake
        with self.assertRaises(S.ContractError) as caught:
            A.import_export(central, rewritten, capability=admission["capability"], receipt_day=add_days(START, 2))
        self.assertEqual(caught.exception.code, "unknown_admission")
        self.assertEqual(central["records"], {})

    def test_bad_capability_is_rejected(self):
        store, central, workflow_ref, admission = prepare()
        payload = payload_for(store, workflow_ref)
        with self.assertRaises(S.ContractError) as caught:
            A.import_export(central, payload, capability="0" * 64, receipt_day=add_days(START, 2))
        self.assertEqual(caught.exception.code, "bad_capability")
        self.assertEqual(central["records"], {})

    def test_admission_requires_a_prospective_start_within_seven_days(self):
        central = A.new_store()
        notice = {
            "workflow_ref": "wf-" + "c" * 32,
            "start_day": add_days(START, -8),
            "applicable_stages": list(S.STAGES),
            "criteria_frozen_before_work": True,
            "criteria_contract_ref": "crit-" + "c" * 32,
        }
        with self.assertRaises(S.ContractError) as caught:
            A.issue_admission(central, notice, issued_day=START)
        self.assertEqual(caught.exception.code, "start_outside_window")

    def test_pending_admission_expires_after_seven_days(self):
        store, central, workflow_ref, admission = prepare(issued=START)
        payload = payload_for(store, workflow_ref)
        with self.assertRaises(S.ContractError) as caught:
            A.import_export(central, payload, capability=admission["capability"], receipt_day=add_days(START, 8))
        self.assertEqual(caught.exception.code, "expired_admission")
        self.assertEqual(central["records"], {})

    def test_admission_cannot_be_issued_twice_for_the_same_workflow(self):
        store, central, workflow_ref, admission = prepare()
        notice = {
            "workflow_ref": workflow_ref,
            "start_day": START,
            "applicable_stages": list(S.STAGES),
            "criteria_frozen_before_work": True,
            "criteria_contract_ref": store["workflows"][workflow_ref]["criteria_contract_ref"],
        }
        with self.assertRaises(S.ContractError) as caught:
            A.issue_admission(central, notice, issued_day=add_days(START, 1))
        self.assertEqual(caught.exception.code, "admission_exists")


class WithdrawalTests(unittest.TestCase):
    def setUp(self):
        self.store, self.central, self.workflow_ref, self.admission = prepare()
        self.payload = payload_for(self.store, self.workflow_ref)
        A.import_export(
            self.central, self.payload, capability=self.admission["capability"], receipt_day=add_days(START, 2)
        )

    def test_withdrawal_deletes_admission_record_and_rejects_replay(self):
        result = A.withdraw(
            self.central,
            admission_ref=self.admission["admission_ref"],
            capability=self.admission["capability"],
            decision_day=add_days(START, 10),
        )
        self.assertEqual(result["deleted_records"], 1)
        self.assertEqual(result["raw_rows"], 0)
        self.assertEqual(self.central["records"], {})
        self.assertNotIn(self.admission["admission_ref"], self.central["admissions"])
        with self.assertRaises(S.ContractError) as caught:
            A.import_export(
                self.central, self.payload, capability=self.admission["capability"], receipt_day=add_days(START, 11)
            )
        self.assertEqual(caught.exception.code, "unknown_admission")
        self.assertEqual(self.central["records"], {})

    def test_withdrawal_leaves_no_linkable_tombstone(self):
        A.withdraw(
            self.central,
            admission_ref=self.admission["admission_ref"],
            capability=self.admission["capability"],
            decision_day=add_days(START, 10),
        )
        serialized = json.dumps(self.central, sort_keys=True)
        self.assertNotIn(self.workflow_ref, serialized)
        self.assertNotIn(self.admission["admission_ref"], serialized)
        self.assertEqual(len(self.central["deletion_receipts"]), 1)
        receipt = next(iter(self.central["deletion_receipts"].values()))
        self.assertEqual(receipt["deleted_day"], add_days(START, 10))
        self.assertEqual(receipt["expires_at"], add_days(START, 17))
        self.assertEqual(list(receipt), ["deleted_day", "expires_at"])

    def test_deletion_receipt_expires_within_seven_days(self):
        A.withdraw(
            self.central,
            admission_ref=self.admission["admission_ref"],
            capability=self.admission["capability"],
            decision_day=add_days(START, 10),
        )
        A.expire(self.central, today=add_days(START, 17))
        self.assertEqual(len(self.central["deletion_receipts"]), 1)
        A.expire(self.central, today=add_days(START, 18))
        self.assertEqual(self.central["deletion_receipts"], {})

    def test_a_fresh_admission_cannot_authenticate_the_old_envelope(self):
        A.withdraw(
            self.central,
            admission_ref=self.admission["admission_ref"],
            capability=self.admission["capability"],
            decision_day=add_days(START, 5),
        )
        notice = {
            "workflow_ref": self.workflow_ref,
            "start_day": START,
            "applicable_stages": list(S.STAGES),
            "criteria_frozen_before_work": True,
            "criteria_contract_ref": self.store["workflows"][self.workflow_ref]["criteria_contract_ref"],
        }
        fresh = A.issue_admission(self.central, notice, issued_day=add_days(START, 6))
        self.assertNotEqual(fresh["admission_ref"], self.admission["admission_ref"])
        with self.assertRaises(S.ContractError) as caught:
            A.import_export(
                self.central, self.payload, capability=fresh["capability"], receipt_day=add_days(START, 7)
            )
        self.assertEqual(caught.exception.code, "unknown_admission")
        self.assertEqual(self.central["records"], {})

    def test_a_fabricated_new_workflow_remains_a_stated_limitation(self):
        # Documented trust limit: an honest-participant replay guarantee cannot
        # detect a deliberately fabricated new workflow with a fresh admission.
        store, central, workflow_ref, admission = prepare(start=add_days(START, 20))
        payload = payload_for(store, workflow_ref)
        result = A.import_export(central, payload, capability=admission["capability"], receipt_day=add_days(START, 22))
        self.assertEqual(result["status"], "accepted")
        self.assertEqual(len(central["records"]), 1)


class RetentionTests(unittest.TestCase):
    def setUp(self):
        self.store, self.central, self.workflow_ref, self.admission = prepare()
        self.payload = payload_for(self.store, self.workflow_ref)
        A.import_export(
            self.central, self.payload, capability=self.admission["capability"], receipt_day=add_days(START, 2)
        )

    def test_expiry_day_is_inclusive_and_the_next_day_is_not(self):
        record = self.central["records"][self.workflow_ref]
        self.assertEqual(record["expires_at"], add_days(START, 92))
        S.record_transition(
            self.store, self.workflow_ref, kind="stage", value="complete", effective_day=add_days(START, 20), stage="build"
        )
        updated = payload_for(self.store, self.workflow_ref)
        result = A.import_export(
            self.central, updated, capability=self.admission["capability"], receipt_day=add_days(START, 92)
        )
        self.assertEqual(result["status"], "updated")
        with self.assertRaises(S.ContractError) as caught:
            A.import_export(
                self.central, updated, capability=self.admission["capability"], receipt_day=add_days(START, 93)
            )
        self.assertEqual(caught.exception.code, "expired_admission")

    def test_retries_do_not_extend_retention(self):
        expires_at = self.central["records"][self.workflow_ref]["expires_at"]
        S.record_transition(
            self.store, self.workflow_ref, kind="stage", value="complete", effective_day=add_days(START, 20), stage="build"
        )
        payload = payload_for(self.store, self.workflow_ref)
        result = A.import_export(
            self.central, payload, capability=self.admission["capability"], receipt_day=add_days(START, 80)
        )
        self.assertEqual(result["status"], "updated")
        self.assertEqual(self.central["records"][self.workflow_ref]["expires_at"], expires_at)
        self.assertEqual(self.central["records"][self.workflow_ref]["first_receipt_day"], add_days(START, 2))

    def test_natural_expiry_removes_the_admission_and_record(self):
        removed = A.expire(self.central, today=add_days(START, 93))
        self.assertEqual(removed["records"], 1)
        self.assertEqual(removed["admissions"], 1)
        with self.assertRaises(S.ContractError) as caught:
            A.import_export(
                self.central, self.payload, capability=self.admission["capability"], receipt_day=add_days(START, 94)
            )
        self.assertEqual(caught.exception.code, "unknown_admission")
        self.assertEqual(self.central["records"], {})
        self.assertEqual(self.central["admissions"], {})

    def test_replay_after_expiry_cannot_reset_first_receipt(self):
        A.expire(self.central, today=add_days(START, 93))
        for day in (94, 95):
            with self.assertRaises(S.ContractError):
                A.import_export(
                    self.central, self.payload, capability=self.admission["capability"], receipt_day=add_days(START, day)
                )
        self.assertEqual(self.central["records"], {})
        self.assertEqual(self.central["admissions"], {})
        self.assertFalse(any("first_receipt" in key for key in self.central.get("records", {})))

    def test_quarantine_expires_after_90_days(self):
        conflict = json.loads(self.payload)
        conflict["snapshot"]["revision"] = 1
        conflict["snapshot"]["export_ref"] = "exp-" + "f" * 32
        result = A.import_export(
            self.central, conflict, capability=self.admission["capability"], receipt_day=add_days(START, 3)
        )
        self.assertEqual(result["status"], "quarantined")
        self.assertEqual(len(self.central["quarantine"]), 1)
        A.expire(self.central, today=add_days(START, 94))
        self.assertEqual(self.central["quarantine"], [])

    def test_local_retention_is_sixty_days_from_capture(self):
        store = S.new_store()
        workflow = S.enable_capture(store, day=START, start_day=START)
        ref = workflow["workflow_ref"]
        self.assertEqual(S.prune_expired(store, add_days(START, 60)), 0)
        self.assertIn(ref, store["workflows"])
        self.assertEqual(S.prune_expired(store, add_days(START, 61)), 1)
        self.assertNotIn(ref, store["workflows"])


class MutantDetectionTests(unittest.TestCase):
    def load_mutant(self, replacements):
        source_path = REPO_ROOT / "tools" / "aegis_usage" / "aggregate.py"
        source = source_path.read_text(encoding="utf-8")
        for old, new in replacements:
            self.assertIn(old, source, "mutation anchor missing: " + old)
            source = source.replace(old, new, 1)
        folder = tempfile.mkdtemp(prefix="aegis-lifecycle-mutant-")
        target = Path(folder) / "mutant_aggregate.py"
        target.write_text(source, encoding="utf-8", newline="\n")
        spec = importlib.util.spec_from_file_location("lifecycle_mutant_aggregate_" + str(id(target)), target)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_expiry_check_mutant_accepts_a_replay_after_expiry(self):
        store, central, workflow_ref, admission = prepare()
        payload = payload_for(store, workflow_ref)
        A.import_export(central, payload, capability=admission["capability"], receipt_day=add_days(START, 2))
        with self.assertRaises(S.ContractError) as caught:
            A.import_export(central, payload, capability=admission["capability"], receipt_day=add_days(START, 93))
        self.assertEqual(caught.exception.code, "expired_admission")
        mutant = self.load_mutant([('if today > day(admission["expires_at"]):', "if False:")])
        result = mutant.import_export(central, payload, capability=admission["capability"], receipt_day=add_days(START, 93))
        self.assertEqual(result["status"], "duplicate")
        self.assertNotEqual("expired_admission", result["status"])


if __name__ == "__main__":
    unittest.main()
