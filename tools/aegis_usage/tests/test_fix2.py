"""Fix-round regression tests for PR #950 (owner brief 6458014758, SD-F 6459004350).

Covers D2-m1 (per-event evidence), P1-2 (user-only files), P1-3 (withdrawal
after admission expiry), the receipt-chronology and disclosure findings, and the
CLI contract fixes. Synthetic data only.
"""

import json
import os
import stat
import subprocess
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
PYTHON = sys.executable


def add_days(start, days):
    return (date.fromisoformat(start) + timedelta(days=days)).isoformat()


def advance(days):
    return add_days(START, days)


def make_envelope(workflow_ref, criteria_ref, start, frozen, events, revision, admission_ref):
    transitions = [
        {
            "event_ref": "evt-" + format(index, "032x"),
            "kind": event["kind"],
            "effective_day": event["effective_day"],
            "value": event["value"],
            "stage": event.get("stage"),
        }
        for index, event in enumerate(events)
    ]
    last = max(event["effective_day"] for event in events)
    derived = S.derive_state(transitions, list(S.STAGES), S.parse_day(last, "last"))
    return {
        "schema": S.SCHEMA_NAME,
        "library_revision": S.SUPPORTED_LIBRARY_REVISIONS[0],
        "capture_tier": S.CAPTURE_TIER,
        "consent_policy_version": S.SUPPORTED_CONSENT_POLICIES[0],
        "reporting_window_days": S.REPORTING_WINDOW_DAYS,
        "admission_ref": admission_ref,
        "snapshot": {
            "workflow_ref": workflow_ref,
            "revision": revision,
            "export_ref": "exp-" + format(revision, "032x"),
            "start_day": start,
            "last_observed_day": last,
            "report_due_day": add_days(start, S.REPORTING_WINDOW_DAYS),
            "applicable_stages": list(S.STAGES),
            "criteria_frozen_before_work": frozen,
            "criteria_contract_ref": criteria_ref,
            "stage_status": derived["stage_status"],
            "status": derived["status"],
            "acceptance": derived["acceptance"],
            "acceptance_evidence": "none" if derived["acceptance"] == "not_assessed" else "local_review_record",
            "delivery_day": derived["delivery_day"],
            "acceptance_day": derived["acceptance_day"],
            "transitions": transitions,
        },
    }


def enrolled(stages=None):
    store = S.new_store()
    workflow = S.enable_capture(store, day=START, start_day=START, applicable_stages=stages)
    S.record_transition(store, workflow["workflow_ref"], kind="observation", value="ongoing", effective_day=START)
    return store, workflow


def admission_for(store, workflow, issued=START):
    notice = {
        "workflow_ref": workflow["workflow_ref"],
        "start_day": workflow["start_day"],
        "applicable_stages": workflow["applicable_stages"],
        "criteria_frozen_before_work": workflow["criteria_frozen_before_work"],
        "criteria_contract_ref": workflow["criteria_contract_ref"],
    }
    return A.issue_admission(A.new_store(), notice, issued_day=issued)


def run_cli(module, store, *args):
    command = [PYTHON, "-B", str(REPO_ROOT / "tools" / "aegis_usage" / module), "--store", str(store)]
    return subprocess.run(command + list(args), capture_output=True, text=True, encoding="utf-8")


class EvidenceBindingTests(unittest.TestCase):
    """D2-m1: evidence belongs to its own acceptance transition."""

    def test_out_of_order_acceptance_exports_the_winning_evidence_category(self):
        store, workflow = enrolled()
        ref = workflow["workflow_ref"]
        S.record_transition(
            store, ref, kind="status", value="delivered", effective_day=advance(10)
        )
        S.record_transition(
            store,
            ref,
            kind="acceptance",
            value="independent_attested_pass",
            effective_day=advance(20),
            evidence="local_review_record",
        )
        # Recorded later, but effective earlier: this must not overwrite the
        # category belonging to the acceptance that wins by effective day.
        S.record_transition(
            store,
            ref,
            kind="acceptance",
            value="self_reported_fail",
            effective_day=advance(10),
            evidence="local_checklist",
        )
        workflow["admission_ref"] = "adm-" + "a" * 32
        snapshot = S.build_envelope(store, ref)["snapshot"]
        self.assertEqual(snapshot["acceptance"], "independent_attested_pass")
        self.assertEqual(snapshot["acceptance_day"], advance(20))
        self.assertEqual(snapshot["acceptance_evidence"], "local_review_record")

    def test_each_acceptance_transition_keeps_its_own_category_locally(self):
        store, workflow = enrolled()
        ref = workflow["workflow_ref"]
        S.record_transition(store, ref, kind="acceptance", value="self_reported_fail", effective_day=advance(3), evidence="local_checklist")
        S.record_transition(store, ref, kind="acceptance", value="independent_attested_pass", effective_day=advance(4), evidence="local_test_record")
        categories = {
            event["effective_day"]: event["evidence"]
            for event in workflow["transitions"]
            if event["kind"] == "acceptance"
        }
        self.assertEqual(categories, {advance(3): "local_checklist", advance(4): "local_test_record"})
        self.assertEqual(workflow["acceptance_evidence"], "local_test_record")

    def test_evidence_is_not_added_to_the_exported_transition_schema(self):
        store, workflow = enrolled()
        S.record_transition(store, workflow["workflow_ref"], kind="acceptance", value="independent_attested_pass", effective_day=advance(2), evidence="local_review_record")
        workflow["admission_ref"] = "adm-" + "a" * 32
        envelope = S.build_envelope(store, workflow["workflow_ref"])
        for transition in envelope["snapshot"]["transitions"]:
            self.assertEqual(tuple(transition), S.TRANSITION_KEYS)

    def test_a_legacy_workflow_without_per_event_evidence_still_exports(self):
        store, workflow = enrolled()
        ref = workflow["workflow_ref"]
        S.record_transition(store, ref, kind="acceptance", value="independent_attested_pass", effective_day=advance(2), evidence="local_test_record")
        workflow["admission_ref"] = "adm-" + "a" * 32
        for event in workflow["transitions"]:
            event.pop("evidence", None)
        workflow["acceptance_evidence"] = "local_test_record"
        snapshot = S.build_envelope(store, ref)["snapshot"]
        self.assertEqual(snapshot["acceptance_evidence"], "local_test_record")

    def test_winning_acceptance_is_chosen_by_effective_day_not_event_reference(self):
        store, workflow = enrolled()
        ref = workflow["workflow_ref"]
        early = S.record_transition(store, ref, kind="acceptance", value="self_reported_pass", effective_day=advance(5), evidence="local_checklist")
        late = S.record_transition(store, ref, kind="acceptance", value="independent_attested_fail", effective_day=advance(6), evidence="local_test_record")
        winner = S.winning_acceptance(workflow["transitions"], S.parse_day(advance(6), "last"))
        self.assertEqual(winner["event_ref"], late["event_ref"])
        self.assertNotEqual(early["event_ref"], late["event_ref"])


class FilePermissionTests(unittest.TestCase):
    """P1-2: stores, exports and created parents are user-only."""

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)

    def assert_user_only_file(self, path):
        self.assertTrue(path.exists())
        if os.name == "posix":
            self.assertEqual(stat.S_IMODE(os.stat(path).st_mode), 0o600, str(path))
        else:
            # Windows has no POSIX mode bits; chmod only toggles the read-only
            # flag, so the guarantee is best effort and the ACL of the parent
            # directory governs access. Assert the file stays owner-usable.
            self.assertTrue(os.access(path, os.R_OK | os.W_OK))
            self.assertTrue(os.stat(path).st_mode & stat.S_IWRITE)

    def test_local_store_is_user_only_under_a_permissive_umask(self):
        previous = os.umask(0o022)
        try:
            path = self.root / "aegis" / "local.json"
            S.save_store(path, S.new_store())
        finally:
            os.umask(previous)
        self.assert_user_only_file(path)
        if os.name == "posix":
            self.assertEqual(stat.S_IMODE(os.stat(path.parent).st_mode), 0o700)

    def test_central_store_is_user_only_and_repairs_an_existing_mode(self):
        path = self.root / "central.json"
        path.write_text("{}", encoding="utf-8")
        if os.name == "posix":
            os.chmod(path, 0o644)
        A.save_store(path, A.new_store())
        self.assert_user_only_file(path)

    def test_export_is_user_only_and_writes_exact_bytes(self):
        store, workflow = enrolled()
        workflow["admission_ref"] = "adm-" + "a" * 32
        payload, digest = S.preview_export(store, workflow["workflow_ref"])
        target = self.root / "exports" / "export.json"
        S.export_snapshot(store, workflow["workflow_ref"], target, preview_sha256=digest, confirm=True)
        self.assert_user_only_file(target)
        self.assertEqual(target.read_bytes(), payload)
        if os.name == "posix":
            self.assertEqual(stat.S_IMODE(os.stat(target.parent).st_mode), 0o700)

    def test_export_and_store_paths_inside_the_repository_are_refused(self):
        target = REPO_ROOT / "forbidden-fix2-export.json"
        store, workflow = enrolled()
        workflow["admission_ref"] = "adm-" + "a" * 32
        _, digest = S.preview_export(store, workflow["workflow_ref"])
        with self.assertRaises(S.ContractError) as caught:
            S.export_snapshot(store, workflow["workflow_ref"], target, preview_sha256=digest, confirm=True)
        self.assertEqual(caught.exception.code, "export_path_in_repository")
        self.assertFalse(target.exists())
        with self.assertRaises(S.ContractError) as caught:
            S.save_store(REPO_ROOT / "forbidden-fix2-store.json", S.new_store())
        self.assertEqual(caught.exception.code, "store_path_in_repository")
        with self.assertRaises(S.ContractError) as caught:
            A.save_store(REPO_ROOT / "forbidden-fix2-central.json", A.new_store())
        self.assertEqual(caught.exception.code, "store_path_in_repository")
        self.assertFalse((REPO_ROOT / "forbidden-fix2-store.json").exists())
        self.assertFalse((REPO_ROOT / "forbidden-fix2-central.json").exists())


class WithdrawalAfterExpiryTests(unittest.TestCase):
    """P1-3: an expired admission must not block withdrawing retained data."""

    def build(self):
        store, workflow = enrolled()
        base = A.new_store()
        admission = admission_for(store, workflow)
        workflow["admission_ref"] = admission["admission_ref"]
        # Re-issue in the same store the withdrawal will use.
        notice = {
            "workflow_ref": workflow["workflow_ref"],
            "start_day": START,
            "applicable_stages": workflow["applicable_stages"],
            "criteria_frozen_before_work": True,
            "criteria_contract_ref": workflow["criteria_contract_ref"],
        }
        admission = A.issue_admission(base, notice, issued_day=START)
        workflow["admission_ref"] = admission["admission_ref"]
        payload = S.build_envelope(store, workflow["workflow_ref"])
        payload["snapshot"]["criteria_contract_ref"] = "crit-" + "e" * 32
        result = A.import_export(base, payload, capability=admission["capability"], receipt_day=advance(2))
        self.assertEqual(result["status"], "quarantined")
        return base, workflow, admission, payload

    def test_withdraw_works_on_day_eight_before_housekeeping(self):
        central, workflow, admission, payload = self.build()
        with self.assertRaises(S.ContractError) as caught:
            A.import_export(central, payload, capability=admission["capability"], receipt_day=advance(8))
        self.assertEqual(caught.exception.code, "expired_admission")
        result = A.withdraw(
            central,
            admission_ref=admission["admission_ref"],
            capability=admission["capability"],
            decision_day=advance(8),
        )
        self.assertEqual(result["deleted_records"], 0)
        self.assertEqual(central["quarantine"], [])
        self.assertEqual(central["admission_tombstones"], {})
        self.assertEqual(len(central["deletion_receipts"]), 1)

    def test_housekeeping_tombstone_permits_withdrawal_after_day_seven(self):
        central, workflow, admission, payload = self.build()
        removed = A.expire(central, today=advance(8))
        self.assertEqual(removed["admissions"], 1)
        self.assertIn(admission["admission_ref"], central["admission_tombstones"])
        tombstone = central["admission_tombstones"][admission["admission_ref"]]
        self.assertEqual(set(tombstone), {"workflow_ref", "verifier", "expired_day"})
        with self.assertRaises(S.ContractError) as caught:
            A.import_export(central, payload, capability=admission["capability"], receipt_day=advance(8))
        self.assertEqual(caught.exception.code, "unknown_admission")
        result = A.withdraw(
            central,
            admission_ref=admission["admission_ref"],
            capability=admission["capability"],
            decision_day=advance(8),
        )
        self.assertEqual(result["deleted_records"], 0)
        self.assertEqual(central["quarantine"], [])
        self.assertEqual(central["admission_tombstones"], {})
        self.assertEqual(len(central["deletion_receipts"]), 1)

    def test_wrong_capability_cannot_withdraw_retained_quarantine(self):
        central, workflow, admission, payload = self.build()
        A.expire(central, today=advance(8))
        with self.assertRaises(S.ContractError) as caught:
            A.withdraw(
                central,
                admission_ref=admission["admission_ref"],
                capability="0" * 64,
                decision_day=advance(8),
            )
        self.assertEqual(caught.exception.code, "bad_capability")
        self.assertEqual(len(central["quarantine"]), 1)
        self.assertIn(admission["admission_ref"], central["admission_tombstones"])

    def test_tombstone_is_purged_with_the_last_linked_payload(self):
        central, workflow, admission, payload = self.build()
        A.expire(central, today=advance(8))
        self.assertIn(admission["admission_ref"], central["admission_tombstones"])
        # Quarantine received on day 2 is retained through day 92 and purged on 93.
        A.expire(central, today=advance(93))
        self.assertEqual(central["quarantine"], [])
        self.assertEqual(central["admission_tombstones"], {})
        with self.assertRaises(S.ContractError) as caught:
            A.withdraw(
                central,
                admission_ref=admission["admission_ref"],
                capability=admission["capability"],
                decision_day=advance(93),
            )
        self.assertEqual(caught.exception.code, "unknown_admission")

    def test_accepted_record_retention_and_tombstone_stay_consistent(self):
        store, workflow = enrolled()
        central = A.new_store()
        notice = {
            "workflow_ref": workflow["workflow_ref"],
            "start_day": START,
            "applicable_stages": workflow["applicable_stages"],
            "criteria_frozen_before_work": True,
            "criteria_contract_ref": workflow["criteria_contract_ref"],
        }
        admission = A.issue_admission(central, notice, issued_day=START)
        workflow["admission_ref"] = admission["admission_ref"]
        payload = S.build_envelope(store, workflow["workflow_ref"])
        self.assertEqual(
            A.import_export(central, payload, capability=admission["capability"], receipt_day=advance(2))["status"],
            "accepted",
        )
        A.expire(central, today=advance(93))
        self.assertEqual(central["records"], {})
        self.assertEqual(central["admission_tombstones"], {})
        with self.assertRaises(S.ContractError) as caught:
            A.withdraw(
                central,
                admission_ref=admission["admission_ref"],
                capability=admission["capability"],
                decision_day=advance(93),
            )
        self.assertEqual(caught.exception.code, "unknown_admission")


class ReceiptChronologyTests(unittest.TestCase):
    """Codex aggregate.py:228 and the monotonic-receipt finding."""

    def setUp(self):
        self.store, self.workflow = enrolled()
        self.ref = self.workflow["workflow_ref"]
        self.central = A.new_store()
        notice = {
            "workflow_ref": self.ref,
            "start_day": START,
            "applicable_stages": self.workflow["applicable_stages"],
            "criteria_frozen_before_work": True,
            "criteria_contract_ref": self.workflow["criteria_contract_ref"],
        }
        self.admission = A.issue_admission(self.central, notice, issued_day=START)
        self.workflow["admission_ref"] = self.admission["admission_ref"]

    def test_an_event_effective_after_its_receipt_is_refused(self):
        events = [
            {"kind": "observation", "value": "ongoing", "effective_day": START},
            {"kind": "stage", "value": "complete", "effective_day": advance(9), "stage": "build"},
        ]
        payload = make_envelope(
            self.ref, self.workflow["criteria_contract_ref"], START, True, events, 2, self.admission["admission_ref"]
        )
        S.validate_envelope(payload)
        with self.assertRaises(S.ContractError) as caught:
            A.import_export(self.central, payload, capability=self.admission["capability"], receipt_day=advance(2))
        self.assertEqual(caught.exception.code, "event_after_receipt")
        self.assertEqual(self.central["records"], {})

    def test_a_receipt_before_the_admission_issue_is_refused(self):
        payload = S.build_envelope(self.store, self.ref)
        with self.assertRaises(S.ContractError) as caught:
            A.import_export(self.central, payload, capability=self.admission["capability"], receipt_day=advance(-1))
        self.assertEqual(caught.exception.code, "receipt_before_issue")

    def test_a_backdated_receipt_cannot_rewrite_the_last_receipt(self):
        payload = S.build_envelope(self.store, self.ref)
        A.import_export(self.central, payload, capability=self.admission["capability"], receipt_day=advance(2))
        with self.assertRaises(S.ContractError) as caught:
            A.import_export(self.central, payload, capability=self.admission["capability"], receipt_day=advance(1))
        self.assertEqual(caught.exception.code, "receipt_day_regression")
        self.assertEqual(self.central["records"][self.ref]["last_receipt_day"], advance(2))


class DisclosureTests(unittest.TestCase):
    """Suppression and cohort-completeness findings."""

    def cohort(self, month, counts, attested=None):
        n = sum(counts.values())
        return {
            "month": month,
            "closed_on": month + "-28",
            "n": n,
            "outcomes": dict(counts),
            "incomplete": False,
            "metrics": {
                "delivery_30d": {"numerator": counts["delivered"], "denominator": n, "rate": 0.0, "status": "available"},
                "follow_up_coverage": {"numerator": n, "denominator": n, "rate": 1.0, "status": "available"},
                "independently_attested_success": attested
                or {"numerator": 0, "denominator": n, "rate": 0.0, "status": "available"},
                "stage_reach": {},
            },
            "late_entries": 0,
            "late_events": 0,
        }

    def report(self, cohorts, open_cohorts=None, truncated=False):
        return {
            "report_version": A.REPORT_VERSION,
            "as_of": "2026-05-01",
            "cohorts": cohorts,
            "open_cohorts": open_cohorts or {},
            "incomplete_cohorts": {},
            "truncated": truncated,
            "withdrawals": 0,
            "limitations": [],
        }

    def test_a_truncated_store_refuses_the_publishable_view(self):
        report = self.report(
            {"2026-01": self.cohort("2026-01", {"delivered": 5, "failed": 5, "abandoned": 5, "ongoing": 5})},
            truncated=True,
        )
        with self.assertRaises(S.ContractError) as caught:
            A.publishable_report(report)
        self.assertEqual(caught.exception.code, "report_truncated")

    def test_a_month_still_open_is_withheld(self):
        report = self.report(
            {"2026-01": self.cohort("2026-01", {"delivered": 5, "failed": 5, "abandoned": 5, "ongoing": 5})},
            open_cohorts={"2026-01": 1},
        )
        view = A.publishable_report(report)
        self.assertEqual(view["cohorts"], [])
        self.assertEqual(view["suppressed_cohorts"], [{"month": "2026-01", "reason": "cohort_open"}])

    def test_a_sparse_attestation_numerator_is_withheld(self):
        report = self.report(
            {
                "2026-01": self.cohort(
                    "2026-01",
                    {"delivered": 5, "failed": 5, "abandoned": 5, "ongoing": 5, "unknown": 0},
                    attested={"numerator": 2, "denominator": 20, "rate": 0.1, "status": "available"},
                )
            }
        )
        view = A.publishable_report(report)
        self.assertEqual(len(view["cohorts"]), 1)
        self.assertEqual(
            view["cohorts"][0]["independently_attested_success"],
            {"status": "withheld", "reason": "sparse_attestation_cell"},
        )

    def test_an_expired_cohort_stays_incomplete_after_housekeeping(self):
        central = A.new_store()
        notice = {
            "workflow_ref": "wf-" + "c" * 32,
            "start_day": START,
            "applicable_stages": list(S.STAGES),
            "criteria_frozen_before_work": True,
            "criteria_contract_ref": "crit-" + "c" * 32,
        }
        admission = A.issue_admission(central, notice, issued_day=START)
        events = [{"kind": "observation", "value": "ongoing", "effective_day": START}]
        A.import_export(
            central,
            make_envelope("wf-" + "c" * 32, "crit-" + "c" * 32, START, True, events, 1, admission["admission_ref"]),
            capability=admission["capability"],
            receipt_day=advance(2),
        )
        before = A.compute_report(central, as_of=advance(100))
        self.assertEqual(before["expired_excluded"], 1)
        self.assertEqual(before["incomplete_cohorts"], {"2026-01": 1})
        A.expire(central, today=advance(93))
        after = A.compute_report(central, as_of=advance(100))
        self.assertEqual(after["expired_excluded"], 1)
        self.assertEqual(after["incomplete_cohorts"], {"2026-01": 1})
        self.assertEqual(after["cohorts"], {})
        # A later start for the same month cannot be published as a complete
        # cohort while the residual expiry marker exists.
        later = "2026-01-20"
        notice["workflow_ref"] = "wf-" + "d" * 32
        notice["start_day"] = later
        notice["criteria_contract_ref"] = "crit-" + "d" * 32
        second = A.issue_admission(central, notice, issued_day=later)
        later_events = [{"kind": "observation", "value": "ongoing", "effective_day": later}]
        A.import_export(
            central,
            make_envelope("wf-" + "d" * 32, "crit-" + "d" * 32, later, True, later_events, 1, second["admission_ref"]),
            capability=second["capability"],
            receipt_day=add_days(later, 2),
        )
        mixed = A.compute_report(central, as_of=advance(95))
        self.assertTrue(mixed["cohorts"]["2026-01"]["incomplete"])
        self.assertEqual(mixed["cohorts"]["2026-01"]["expired_excluded"], 1)
        view = A.publishable_report(mixed)
        self.assertEqual(view["cohorts"], [])
        self.assertEqual(view["suppressed_cohorts"], [{"month": "2026-01", "reason": "retention_incomplete"}])

    def test_only_a_claimed_frozen_criteria_invalidation_is_counted(self):
        central = A.new_store()
        notice = {
            "workflow_ref": "wf-" + "e" * 32,
            "start_day": START,
            "applicable_stages": list(S.STAGES),
            "criteria_frozen_before_work": False,
            "criteria_contract_ref": "crit-" + "e" * 32,
        }
        admission = A.issue_admission(central, notice, issued_day=START)
        first = [{"kind": "observation", "value": "ongoing", "effective_day": START}]
        second = first + [{"kind": "status", "value": "delivered", "effective_day": advance(10)}]
        A.import_export(
            central,
            make_envelope("wf-" + "e" * 32, "crit-" + "e" * 32, START, False, first, 1, admission["admission_ref"]),
            capability=admission["capability"],
            receipt_day=advance(2),
        )
        A.import_export(
            central,
            make_envelope("wf-" + "e" * 32, "crit-" + "e" * 32, START, False, second, 2, admission["admission_ref"]),
            capability=admission["capability"],
            receipt_day=advance(11),
        )
        report = A.compute_report(central, as_of=advance(40))
        january = report["cohorts"]["2026-01"]
        self.assertEqual(january["frozen_criteria_invalidated"], 0)
        self.assertEqual(january["metrics"]["independently_attested_success"]["numerator"], 0)


class InputContractTests(unittest.TestCase):
    """DeepSeek findings: duplicate event_ref, empty stages, read-only show."""

    def test_duplicate_event_ref_is_refused_before_the_store_is_mutated(self):
        store, workflow = enrolled()
        ref = workflow["workflow_ref"]
        S.record_transition(store, ref, kind="stage", value="complete", effective_day=advance(2), stage="build", event_ref="evt-" + "1" * 32)
        before = json.dumps(store, sort_keys=True)
        with self.assertRaises(S.ContractError) as caught:
            S.record_transition(store, ref, kind="stage", value="complete", effective_day=advance(3), stage="validate", event_ref="evt-" + "1" * 32)
        self.assertEqual(caught.exception.code, "duplicate_event_ref")
        self.assertEqual(json.dumps(store, sort_keys=True), before)
        self.assertEqual(workflow["revision"], 2)

    def test_an_explicitly_empty_stage_set_is_refused(self):
        with self.assertRaises(S.ContractError) as caught:
            S.enable_capture(S.new_store(), day=START, start_day=START, applicable_stages=[])
        self.assertEqual(caught.exception.code, "invalid_stages")
        with self.assertRaises(S.ContractError) as caught:
            A.issue_admission(
                A.new_store(),
                {
                    "workflow_ref": "wf-" + "a" * 32,
                    "start_day": START,
                    "applicable_stages": [],
                    "criteria_frozen_before_work": True,
                    "criteria_contract_ref": "crit-" + "a" * 32,
                },
                issued_day=START,
            )
        self.assertEqual(caught.exception.code, "invalid_stages")

    def test_show_still_reads_retained_history_after_opt_out(self):
        store, workflow = enrolled()
        S.disable_capture(store, workflow["workflow_ref"])
        with self.assertRaises(S.ContractError) as caught:
            S.record_transition(store, workflow["workflow_ref"], kind="stage", value="complete", effective_day=advance(2), stage="build")
        self.assertEqual(caught.exception.code, "capture_disabled")
        self.assertEqual(S.read_workflow(store, workflow["workflow_ref"])["revision"], 1)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "local.json"
            S.save_store(path, store)
            shown = run_cli("local_report.py", path, "show", "--workflow-ref", workflow["workflow_ref"])
            self.assertEqual(shown.returncode, 0, shown.stderr)
            self.assertEqual(json.loads(shown.stdout)["revision"], 1)


class CliContractTests(unittest.TestCase):
    """Stable CLI refusals and capability handling."""

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)

    def test_a_corrupt_local_store_is_a_stable_refusal_not_a_traceback(self):
        path = self.root / "local.json"
        path.write_text("{not json", encoding="utf-8")
        result = run_cli("local_report.py", path, "show", "--workflow-ref", "wf-" + "a" * 32)
        self.assertEqual(result.returncode, 2)
        self.assertIn("ERROR store_unreadable", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_a_corrupt_central_store_is_a_stable_refusal_not_a_traceback(self):
        path = self.root / "central.json"
        path.write_text("{not json", encoding="utf-8")
        result = run_cli("aggregate.py", path, "expire", "--day", advance(1))
        self.assertEqual(result.returncode, 2)
        self.assertIn("ERROR store_unreadable", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_a_store_inside_the_checkout_is_refused_by_the_cli(self):
        target = REPO_ROOT / "forbidden-fix2-cli.json"
        result = run_cli("aggregate.py", target, "expire", "--day", advance(1))
        self.assertEqual(result.returncode, 2)
        self.assertIn("ERROR store_path_in_repository", result.stderr)
        self.assertFalse(target.exists())

    def test_capability_file_is_accepted_and_argv_capability_warns(self):
        store, workflow = enrolled()
        central = A.new_store()
        notice = {
            "workflow_ref": workflow["workflow_ref"],
            "start_day": START,
            "applicable_stages": workflow["applicable_stages"],
            "criteria_frozen_before_work": True,
            "criteria_contract_ref": workflow["criteria_contract_ref"],
        }
        admission = A.issue_admission(central, notice, issued_day=START)
        workflow["admission_ref"] = admission["admission_ref"]
        payload = S.preview_export(store, workflow["workflow_ref"])[0]
        central_path = self.root / "central.json"
        A.save_store(central_path, central)
        payload_path = self.root / "payload.json"
        payload_path.write_bytes(payload)
        capability_path = self.root / "capability.txt"
        capability_path.write_text(admission["capability"] + "\n", encoding="utf-8")
        imported = run_cli(
            "aggregate.py", central_path, "import", "--payload", str(payload_path),
            "--capability-file", str(capability_path), "--day", advance(2),
        )
        self.assertEqual(imported.returncode, 0, imported.stderr)
        self.assertEqual(json.loads(imported.stdout)["status"], "accepted")
        self.assertNotIn("WARNING", imported.stderr)
        warned = run_cli(
            "aggregate.py", central_path, "import", "--payload", str(payload_path),
            "--capability", admission["capability"], "--day", advance(2),
        )
        self.assertEqual(warned.returncode, 0, warned.stderr)
        self.assertIn("WARNING capability_in_argv", warned.stderr)
        both = run_cli(
            "aggregate.py", central_path, "import", "--payload", str(payload_path),
            "--capability", admission["capability"], "--capability-file", str(capability_path), "--day", advance(2),
        )
        self.assertEqual(both.returncode, 2)
        self.assertIn("ERROR invalid_arguments", both.stderr)


if __name__ == "__main__":
    unittest.main()
