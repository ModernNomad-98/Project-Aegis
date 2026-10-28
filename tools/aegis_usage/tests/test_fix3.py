"""FIX3 residual regression tests for PR #950 (SD-F 4c7add32, DeepSeek review 5677246919).

Covers R1 (repository guard for a missing parent), R2 (withdraw purges
same-workflow tombstones), R3 (Windows read-only store replacement), R4
(stage_reach uses the latest stage event), the material advisory findings that
were fixed in this round, and the documented residuals. It also carries the
FIX4 regressions for the two SD-F residuals: M4 (per-stage not_applicable is
floored with the whole stage cell) and M5 (a forbidden field under an
attacker-chosen key reports a redacted path). Synthetic data only.
"""

import contextlib
import hashlib
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
ADMISSION = "adm-" + "a" * 32


def add_days(start, days):
    return (date.fromisoformat(start) + timedelta(days=days)).isoformat()


def advance(days):
    return add_days(START, days)


def event_ref(workflow_ref, index):
    return "evt-" + hashlib.sha256((workflow_ref + ":" + str(index)).encode("utf-8")).hexdigest()[:32]


def export_ref(workflow_ref, revision):
    return "exp-" + hashlib.sha256((workflow_ref + ":export:" + str(revision)).encode("utf-8")).hexdigest()[:32]


def make_envelope(workflow_ref, criteria_ref, start, stages, frozen, events, revision, admission_ref):
    transitions = [
        {
            "event_ref": event_ref(workflow_ref, index),
            "kind": item["kind"],
            "effective_day": item["effective_day"],
            "value": item["value"],
            "stage": item.get("stage"),
        }
        for index, item in enumerate(events)
    ]
    last = max(item["effective_day"] for item in events)
    derived = S.derive_state(transitions, stages, S.parse_day(last, "last"))
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
            "export_ref": export_ref(workflow_ref, revision),
            "start_day": start,
            "last_observed_day": last,
            "report_due_day": add_days(start, S.REPORTING_WINDOW_DAYS),
            "applicable_stages": list(stages),
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


def notice_for(workflow_ref, start=START, stages=None, criteria_ref=None):
    return {
        "workflow_ref": workflow_ref,
        "start_day": start,
        "applicable_stages": list(S.STAGES if stages is None else stages),
        "criteria_frozen_before_work": True,
        "criteria_contract_ref": criteria_ref or ("crit-" + hashlib.sha256(workflow_ref.encode("utf-8")).hexdigest()[:32]),
    }


def build_case(central, key, start, exports, stages=None, issued=None):
    stages = list(stages or S.STAGES)
    workflow_ref = "wf-" + hashlib.sha256(("case:" + key).encode("utf-8")).hexdigest()[:32]
    notice = notice_for(workflow_ref, start, stages)
    admission = A.issue_admission(central, notice, issued_day=issued or start)
    cumulative = []
    for revision, (receipt, events) in enumerate(exports, start=1):
        cumulative = cumulative + list(events)
        envelope = make_envelope(
            workflow_ref, notice["criteria_contract_ref"], start, stages, True, cumulative, revision, admission["admission_ref"]
        )
        A.import_export(central, envelope, capability=admission["capability"], receipt_day=receipt)
    return workflow_ref, admission


def run_cli(module, store, *args):
    command = [PYTHON, "-B", str(REPO_ROOT / "tools" / "aegis_usage" / module), "--store", str(store)]
    return subprocess.run(command + list(args), capture_output=True, text=True, encoding="utf-8")


@contextlib.contextmanager
def working_directory(path):
    previous = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


def synthetic_cell(month, counts, late_entries=0, late_events=0):
    n = sum(counts.values())
    return {
        "month": month,
        "closed_on": month + "-28",
        "n": n,
        "outcomes": dict(counts),
        "metrics": {
            "delivery_30d": {"numerator": counts["delivered"], "denominator": n, "rate": 0.0, "status": "available"},
            "follow_up_coverage": {"numerator": n, "denominator": n, "rate": 1.0, "status": "available"},
            "independently_attested_success": {"numerator": 0, "denominator": n, "rate": 0.0, "status": "available"},
            "stage_reach": {
                stage: {"numerator": 0, "denominator": n, "rate": 0.0, "not_applicable": 0}
                for stage in S.STAGES
            },
        },
        "late_entries": late_entries,
        "late_events": late_events,
    }


class RepositoryPathGuardTests(unittest.TestCase):
    """R1: the nearest existing ancestor, not CWD, decides the guard."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="aegis-fix3-guard-")
        self.root = Path(self.temp.name)
        self.store = S.new_store()
        self.workflow = S.enable_capture(self.store, day=START, start_day=START)
        self.ref = self.workflow["workflow_ref"]
        S.record_transition(self.store, self.ref, kind="observation", value="ongoing", effective_day=START)
        self.workflow["admission_ref"] = ADMISSION
        self.payload, self.sha = S.preview_export(self.store, self.ref)

    def tearDown(self):
        self.temp.cleanup()

    def other_checkout(self):
        repo = self.root / "other-checkout"
        (repo / ".git").mkdir(parents=True, exist_ok=True)
        return repo

    def test_export_with_missing_parent_inside_another_checkout_is_refused(self):
        repo = self.other_checkout()
        out = repo / "missing" / "deeper" / "export.json"
        with working_directory(self.root):
            with self.assertRaises(S.ContractError) as caught:
                S.export_snapshot(
                    self.store, self.ref, out, preview_sha256=self.sha, confirm=True
                )
        self.assertEqual(caught.exception.code, "export_path_in_repository")
        self.assertFalse(out.exists())

    def test_store_with_missing_parent_inside_another_checkout_is_refused(self):
        repo = self.other_checkout()
        target = repo / "missing" / "deeper" / "local-store.json"
        with working_directory(self.root):
            with self.assertRaises(S.ContractError) as caught:
                S.save_store(target, S.new_store())
        self.assertEqual(caught.exception.code, "store_path_in_repository")
        self.assertFalse(target.exists())

    def test_export_with_an_existing_parent_inside_the_checkout_is_still_refused(self):
        repo = self.other_checkout()
        out = repo / "exports" / "export.json"
        out.parent.mkdir()
        with working_directory(self.root):
            with self.assertRaises(S.ContractError) as caught:
                S.export_snapshot(self.store, self.ref, out, preview_sha256=self.sha, confirm=True)
        self.assertEqual(caught.exception.code, "export_path_in_repository")

    def test_export_outside_version_control_with_a_missing_parent_is_allowed(self):
        out = self.root / "plain" / "deeper" / "export.json"
        with working_directory(self.root):
            result = S.export_snapshot(self.store, self.ref, out, preview_sha256=self.sha, confirm=True)
        self.assertTrue(out.exists())
        self.assertEqual(result["sha256"], self.sha)


class WithdrawTombstoneTests(unittest.TestCase):
    """R2: withdrawal leaves no same-workflow admission tombstone behind."""

    def quarantined_admission(self, central, workflow_ref):
        """An admission whose first import is quarantined keeps data linked."""
        admission = A.issue_admission(central, notice_for(workflow_ref), issued_day=START)
        envelope = make_envelope(
            workflow_ref,
            "crit-" + "9" * 32,
            START,
            S.STAGES,
            True,
            [{"kind": "observation", "value": "ongoing", "effective_day": START}],
            1,
            admission["admission_ref"],
        )
        result = A.import_export(
            central, envelope, capability=admission["capability"], receipt_day=advance(2)
        )
        self.assertEqual(result["status"], "quarantined")
        return admission

    def test_withdrawing_a_newer_admission_purges_the_older_same_workflow_tombstone(self):
        workflow_ref = "wf-" + "b" * 32
        central = A.new_store()
        first = self.quarantined_admission(central, workflow_ref)
        # The pending admission expires after seven days; the retained
        # quarantine payload keeps its capability-verification tombstone.
        A.expire(central, today=advance(8))
        self.assertEqual(len(central["admission_tombstones"]), 1)
        second = A.issue_admission(central, notice_for(workflow_ref), issued_day=advance(7))
        result = A.withdraw(
            central, admission_ref=second["admission_ref"], capability=second["capability"], decision_day=advance(8)
        )
        self.assertEqual(result["deleted_records"], 0)
        self.assertEqual(central["quarantine"], [])
        self.assertNotIn(first["admission_ref"], central["admission_tombstones"])
        self.assertEqual(central["admission_tombstones"], {})

    def test_withdraw_leaves_another_workflows_tombstone_alone(self):
        other_ref = "wf-" + "c" * 32
        central = A.new_store()
        other = self.quarantined_admission(central, other_ref)
        target = "wf-" + "d" * 32
        self.quarantined_admission(central, target)
        A.expire(central, today=advance(8))
        self.assertEqual(len(central["admission_tombstones"]), 2)
        newer = A.issue_admission(central, notice_for(target), issued_day=advance(7))
        A.withdraw(central, admission_ref=newer["admission_ref"], capability=newer["capability"], decision_day=advance(8))
        self.assertIn(other["admission_ref"], central["admission_tombstones"])


class ReadOnlyStoreTests(unittest.TestCase):
    """R3: a read-only store is replaced and left writable on Windows."""

    def test_a_read_only_store_can_be_replaced_and_is_left_writable(self):
        with tempfile.TemporaryDirectory(prefix="aegis-fix3-ro-") as folder:
            target = Path(folder) / "store.json"
            S.save_store(target, S.new_store())
            os.chmod(target, stat.S_IREAD | stat.S_IWRITE if os.name == "nt" else 0o400)
            if os.name == "nt":
                os.chmod(target, stat.S_IREAD)
            replacement = S.new_store()
            replacement["opt_ins"]["wf-" + "e" * 32] = {"enabled": True, "opted_in_day": START}
            S.save_store(target, replacement)
            saved = json.loads(target.read_text(encoding="utf-8"))
            self.assertIn("wf-" + "e" * 32, saved["opt_ins"])
            if os.name == "nt":
                self.assertTrue(os.stat(target).st_mode & stat.S_IWRITE)


class PredictableTempPathTests(unittest.TestCase):
    """The store writer no longer opens a predictable <store>.tmp path."""

    def test_a_preexisting_store_tmp_directory_does_not_block_the_save(self):
        with tempfile.TemporaryDirectory(prefix="aegis-fix3-tmp-") as folder:
            target = Path(folder) / "store.json"
            S.save_store(target, S.new_store())
            (Path(folder) / "store.json.tmp").mkdir()
            replacement = S.new_store()
            replacement["opt_ins"]["wf-" + "7" * 32] = {"enabled": True, "opted_in_day": START}
            S.save_store(target, replacement)
            saved = json.loads(target.read_text(encoding="utf-8"))
            self.assertIn("wf-" + "7" * 32, saved["opt_ins"])


class StageReachTests(unittest.TestCase):
    """R4: stage reach reads the latest stage event, not any historical one."""

    def test_a_stage_returned_to_in_progress_is_not_counted_as_reached(self):
        central = A.new_store()
        build_case(
            central,
            "stage-returned",
            START,
            [
                (advance(2), [{"kind": "observation", "value": "ongoing", "effective_day": START}]),
                (
                    advance(12),
                    [
                        {"kind": "stage", "value": "complete", "effective_day": advance(5), "stage": "build"},
                        {"kind": "stage", "value": "in_progress", "effective_day": advance(10), "stage": "build"},
                    ],
                ),
            ],
        )
        report = A.compute_report(central, as_of=advance(60))
        build = report["cohorts"]["2026-01"]["metrics"]["stage_reach"]["build"]
        self.assertEqual(build["numerator"], 0)
        self.assertEqual(build["denominator"], 1)

    def test_the_latest_stage_event_is_chosen_by_effective_day_not_recording_order(self):
        central = A.new_store()
        build_case(
            central,
            "stage-order",
            START,
            [
                (advance(2), [{"kind": "observation", "value": "ongoing", "effective_day": START}]),
                (
                    advance(12),
                    [
                        {"kind": "stage", "value": "in_progress", "effective_day": advance(5), "stage": "build"},
                        {"kind": "stage", "value": "complete", "effective_day": advance(10), "stage": "build"},
                    ],
                ),
            ],
        )
        report = A.compute_report(central, as_of=advance(60))
        build = report["cohorts"]["2026-01"]["metrics"]["stage_reach"]["build"]
        self.assertEqual(build["numerator"], 1)


class ImporterApplicabilityTests(unittest.TestCase):
    """High finding: the importer rejected an applicable not_applicable event."""

    def test_an_applicable_stage_cannot_carry_not_applicable_in_a_transition(self):
        workflow_ref = "wf-" + "f" * 32
        central = A.new_store()
        notice = notice_for(workflow_ref)
        admission = A.issue_admission(central, notice, issued_day=START)
        events = [
            {"kind": "observation", "value": "ongoing", "effective_day": START},
            {"kind": "stage", "value": "not_applicable", "effective_day": advance(5), "stage": "build"},
            {"kind": "stage", "value": "complete", "effective_day": advance(8), "stage": "build"},
        ]
        envelope = make_envelope(
            workflow_ref, notice["criteria_contract_ref"], START, S.STAGES, True, events, 1, admission["admission_ref"]
        )
        with self.assertRaises(S.ContractError) as caught:
            A.import_export(central, envelope, capability=admission["capability"], receipt_day=advance(10))
        self.assertEqual(caught.exception.code, "applicability_conflict")
        self.assertEqual(central["records"], {})


class ChronologyOrderTests(unittest.TestCase):
    """High finding: chronology must compare effective days, not list order."""

    def test_an_earlier_observation_can_be_backfilled_after_a_terminal(self):
        store = S.new_store()
        workflow = S.enable_capture(store, day=START, start_day=START)
        ref = workflow["workflow_ref"]
        S.record_transition(store, ref, kind="status", value="delivered", effective_day=advance(20))
        S.record_transition(store, ref, kind="observation", value="ongoing", effective_day=advance(10))
        workflow["admission_ref"] = ADMISSION
        snapshot = S.build_envelope(store, ref)["snapshot"]
        self.assertEqual(snapshot["status"], "delivered")

    def test_an_observation_effective_after_a_terminal_is_refused_on_record(self):
        store = S.new_store()
        workflow = S.enable_capture(store, day=START, start_day=START)
        ref = workflow["workflow_ref"]
        S.record_transition(store, ref, kind="observation", value="ongoing", effective_day=advance(10))
        with self.assertRaises(S.ContractError) as caught:
            S.record_transition(store, ref, kind="status", value="delivered", effective_day=advance(5))
        self.assertEqual(caught.exception.code, "observation_after_terminal")

    def test_validation_accepts_a_backfilled_earlier_observation(self):
        workflow_ref = "wf-" + "1" * 32
        events = [
            {"kind": "status", "value": "delivered", "effective_day": advance(20)},
            {"kind": "observation", "value": "ongoing", "effective_day": advance(10)},
        ]
        envelope = make_envelope(
            workflow_ref, "crit-" + "1" * 32, START, S.STAGES, True, events, 1, ADMISSION
        )
        S.validate_envelope(envelope)

    def test_validation_rejects_a_later_effective_observation(self):
        workflow_ref = "wf-" + "2" * 32
        events = [
            {"kind": "observation", "value": "ongoing", "effective_day": advance(20)},
            {"kind": "status", "value": "delivered", "effective_day": advance(5)},
        ]
        envelope = make_envelope(
            workflow_ref, "crit-" + "2" * 32, START, S.STAGES, True, events, 1, ADMISSION
        )
        with self.assertRaises(S.ContractError) as caught:
            S.validate_envelope(envelope)
        self.assertEqual(caught.exception.code, "observation_after_terminal")


class MalformedStoreTests(unittest.TestCase):
    """Medium finding: valid JSON with wrong shapes is a stable refusal."""

    def test_local_store_with_a_wrong_workflows_shape_is_refused(self):
        with tempfile.TemporaryDirectory(prefix="aegis-fix3-store-") as folder:
            path = Path(folder) / "local.json"
            path.write_text(json.dumps({"store_version": 1, "opt_ins": {}, "workflows": []}), encoding="utf-8")
            with self.assertRaises(S.ContractError) as caught:
                S.load_store(path)
        self.assertEqual(caught.exception.code, "store_unreadable")

    def test_central_store_with_a_wrong_records_shape_is_refused(self):
        with tempfile.TemporaryDirectory(prefix="aegis-fix3-store-") as folder:
            path = Path(folder) / "central.json"
            path.write_text(json.dumps({"store_version": 1, "records": []}), encoding="utf-8")
            with self.assertRaises(S.ContractError) as caught:
                A.load_store(path)
        self.assertEqual(caught.exception.code, "store_unreadable")

    def test_a_nested_malformed_store_is_a_stable_cli_refusal(self):
        with tempfile.TemporaryDirectory(prefix="aegis-fix3-store-") as folder:
            path = Path(folder) / "local.json"
            ref = "wf-" + "8" * 32
            path.write_text(
                json.dumps({"store_version": 1, "opt_ins": {}, "workflows": {ref: ["not-a-workflow"]}}), encoding="utf-8"
            )
            result = run_cli("local_report.py", path, "show", "--workflow-ref", ref)
        self.assertEqual(result.returncode, 2)
        self.assertIn("ERROR store_unreadable", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_a_notice_that_is_not_an_object_is_refused(self):
        with self.assertRaises(S.ContractError) as caught:
            A.issue_admission(A.new_store(), [], issued_day=START)
        self.assertEqual(caught.exception.code, "notice_unreadable")


class KeyEchoTests(unittest.TestCase):
    """Medium finding: invalid payloads do not echo attacker-chosen key names."""

    def test_an_unknown_top_level_key_is_not_echoed(self):
        workflow_ref = "wf-" + "3" * 32
        envelope = make_envelope(
            workflow_ref,
            "crit-" + "3" * 32,
            START,
            S.STAGES,
            True,
            [{"kind": "observation", "value": "ongoing", "effective_day": START}],
            1,
            ADMISSION,
        )
        envelope["alice@example.com"] = 1
        with self.assertRaises(S.ContractError) as caught:
            S.validate_envelope(envelope)
        self.assertEqual(caught.exception.code, "unknown_field")
        self.assertNotIn("alice@example.com", caught.exception.message)

    def test_a_duplicate_key_name_is_not_echoed(self):
        raw = b'{"alice@example.com": 1, "alice@example.com": 2}'
        with self.assertRaises(S.ContractError) as caught:
            S.loads_strict(raw)
        self.assertEqual(caught.exception.code, "duplicate_key")
        self.assertNotIn("alice@example.com", caught.exception.message)

    def test_a_forbidden_field_under_an_attacker_key_does_not_echo_the_key(self):
        # FIX4 / SD-F M5: the walk runs before the key allowlist, so an
        # arbitrary ancestor key must not reach the reported path.
        with self.assertRaises(S.ContractError) as caught:
            S.validate_envelope({"alice@example.com": {"email": 1}})
        self.assertEqual(caught.exception.code, "forbidden_field")
        self.assertEqual(caught.exception.path, "<key>.email")
        self.assertNotIn("alice@example.com", caught.exception.path)
        self.assertNotIn("alice@example.com", caught.exception.message)

    def test_the_cli_reports_a_redacted_path_for_an_attacker_key(self):
        with tempfile.TemporaryDirectory(prefix="aegis-fix4-echo-") as folder:
            payload = Path(folder) / "payload.json"
            payload.write_text(json.dumps({"alice@example.com": {"email": 1}}), encoding="utf-8")
            result = run_cli(
                "aggregate.py",
                Path(folder) / "central.json",
                "import",
                "--payload",
                str(payload),
                "--capability",
                "x",
                "--day",
                START,
            )
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("ERROR forbidden_field", result.stderr)
        self.assertIn("[<key>.email]", result.stderr)
        self.assertNotIn("alice@example.com", result.stderr)


class NestingTests(unittest.TestCase):
    """Medium finding: deep nesting is a contract refusal, not a traceback."""

    def test_deeply_nested_json_is_refused(self):
        raw = b"[" * 2000 + b"]" * 2000
        with self.assertRaises(S.ContractError) as caught:
            S.loads_strict(raw)
        self.assertIn(caught.exception.code, ("invalid_nesting", "malformed_json"))

    def test_deeply_nested_values_are_refused(self):
        nested = []
        for _ in range(2000):
            nested = [nested]
        with self.assertRaises(S.ContractError) as caught:
            S.validate_envelope({"deep": nested})
        self.assertEqual(caught.exception.code, "invalid_nesting")


class EnableCaptureTests(unittest.TestCase):
    """Medium finding: opt-in cannot overwrite history or coerce a flag."""

    def test_re_enrolling_the_same_workflow_is_refused(self):
        store = S.new_store()
        workflow = S.enable_capture(store, day=START, start_day=START)
        ref = workflow["workflow_ref"]
        S.record_transition(store, ref, kind="observation", value="ongoing", effective_day=START)
        with self.assertRaises(S.ContractError) as caught:
            S.enable_capture(store, day=START, start_day=START, workflow_ref=ref)
        self.assertEqual(caught.exception.code, "workflow_exists")
        self.assertEqual(len(store["workflows"][ref]["transitions"]), 1)

    def test_a_non_boolean_criteria_flag_is_refused(self):
        with self.assertRaises(S.ContractError) as caught:
            S.enable_capture(S.new_store(), day=START, start_day=START, criteria_frozen_before_work="yes")
        self.assertEqual(caught.exception.code, "invalid_type")


class AttachAdmissionTests(unittest.TestCase):
    """Low finding: changing the admission on an export bumps the revision."""

    def test_attach_admission_bumps_revision_and_rotates_export_ref(self):
        with tempfile.TemporaryDirectory(prefix="aegis-fix3-attach-") as folder:
            path = Path(folder) / "local.json"
            store = S.new_store()
            workflow = S.enable_capture(store, day=START, start_day=START)
            ref = workflow["workflow_ref"]
            S.record_transition(store, ref, kind="observation", value="ongoing", effective_day=START)
            S.save_store(path, store)
            before = S.load_store(path)["workflows"][ref]
            result = run_cli("local_report.py", path, "attach-admission", "--workflow-ref", ref, "--admission-ref", ADMISSION)
            self.assertEqual(result.returncode, 0, result.stderr)
            after = S.load_store(path)["workflows"][ref]
            self.assertEqual(after["admission_ref"], ADMISSION)
            self.assertEqual(after["revision"], before["revision"] + 1)
            self.assertNotEqual(after["export_ref"], before["export_ref"])

            second = run_cli("local_report.py", path, "attach-admission", "--workflow-ref", ref, "--admission-ref", ADMISSION)
            self.assertEqual(second.returncode, 0, second.stderr)
            unchanged = S.load_store(path)["workflows"][ref]
            self.assertEqual(unchanged["revision"], after["revision"])


class LateEventTests(unittest.TestCase):
    """Medium finding: a late event effective after day 30 is still late."""

    def test_an_event_effective_on_day_31_received_after_close_is_counted_late(self):
        central = A.new_store()
        build_case(
            central,
            "late-day-31",
            START,
            [
                (advance(2), [{"kind": "observation", "value": "ongoing", "effective_day": START}]),
                (advance(40), [{"kind": "status", "value": "delivered", "effective_day": advance(31)}]),
            ],
        )
        report = A.compute_report(central, as_of=advance(60))
        january = report["cohorts"]["2026-01"]
        self.assertEqual(january["outcomes"]["unknown"], 1)
        self.assertEqual(january["late_events"], 1)


class PublishableDisclosureTests(unittest.TestCase):
    """Medium finding: late cells are floored and incomplete months are listed."""

    def base_report(self, cohorts, late_entries=0, late_events=0):
        return {
            "report_version": A.REPORT_VERSION,
            "as_of": "2026-05-01",
            "cohorts": cohorts,
            "open_cohorts": {},
            "incomplete_cohorts": {},
            "withdrawals": 0,
            "limitations": [],
            "truncated": False,
        }

    def test_a_sparse_late_cell_is_withheld(self):
        counts = {"delivered": 5, "failed": 5, "abandoned": 5, "ongoing": 5, "unknown": 0}
        report = self.base_report(
            {"2026-01": synthetic_cell("2026-01", counts, late_entries=1, late_events=2)}
        )
        view = A.publishable_report(report)
        self.assertEqual(view["cohorts"][0]["late_entries"], {"status": "withheld", "reason": "sparse_late_cell"})
        self.assertEqual(view["cohorts"][0]["late_events"], {"status": "withheld", "reason": "sparse_late_cell"})

    def test_zero_late_cells_are_published_as_zero(self):
        counts = {"delivered": 5, "failed": 5, "abandoned": 5, "ongoing": 5, "unknown": 0}
        report = self.base_report({"2026-01": synthetic_cell("2026-01", counts)})
        view = A.publishable_report(report)
        self.assertEqual(view["cohorts"][0]["late_entries"], 0)
        self.assertEqual(view["cohorts"][0]["late_events"], 0)

    def test_a_sparse_not_applicable_count_withholds_the_stage_cell(self):
        # FIX4 / SD-F M4: n=21 with a stage denominator of 20 discloses one
        # not-applicable start, so the whole stage cell is withheld rather
        # than letting the count be recovered by subtraction.
        counts = {"delivered": 6, "failed": 5, "abandoned": 5, "ongoing": 5, "unknown": 0}
        cell = synthetic_cell("2026-01", counts)
        cell["metrics"]["stage_reach"]["build"] = {
            "numerator": 20,
            "denominator": 20,
            "rate": 1.0,
            "not_applicable": 1,
        }
        view = A.publishable_report(self.base_report({"2026-01": cell}))
        self.assertEqual(
            view["cohorts"][0]["stage_reach"]["build"],
            {"status": "withheld", "reason": "sparse_stage_cell"},
        )

    def test_a_not_applicable_count_at_the_cell_floor_is_published(self):
        counts = {"delivered": 8, "failed": 7, "abandoned": 5, "ongoing": 5, "unknown": 5}
        cell = synthetic_cell("2026-01", counts)
        cell["metrics"]["stage_reach"]["build"] = {
            "numerator": 25,
            "denominator": 25,
            "rate": 1.0,
            "not_applicable": 5,
        }
        view = A.publishable_report(self.base_report({"2026-01": cell}))
        published = view["cohorts"][0]["stage_reach"]["build"]
        self.assertEqual(published["not_applicable"], 5)
        self.assertEqual(published["denominator"], 25)
        self.assertEqual(published["numerator"], 25)

    def test_a_zero_not_applicable_count_is_published(self):
        counts = {"delivered": 5, "failed": 5, "abandoned": 5, "ongoing": 5, "unknown": 0}
        report = self.base_report({"2026-01": synthetic_cell("2026-01", counts)})
        view = A.publishable_report(report)
        build = view["cohorts"][0]["stage_reach"]["build"]
        self.assertEqual(build["not_applicable"], 0)
        self.assertEqual(build["denominator"], 20)

    def test_a_month_with_only_expired_records_is_listed_as_suppressed(self):
        report = self.base_report({})
        report["incomplete_cohorts"] = {"2026-01": 2}
        view = A.publishable_report(report)
        self.assertIn({"month": "2026-01", "reason": "retention_incomplete"}, view["suppressed_cohorts"])

    def test_an_incomplete_month_precedes_the_open_month_reason(self):
        counts = {"delivered": 5, "failed": 5, "abandoned": 5, "ongoing": 5, "unknown": 0}
        cell = synthetic_cell("2026-01", counts)
        cell["incomplete"] = True
        report = self.base_report({"2026-01": cell})
        report["open_cohorts"] = {"2026-01": 1}
        view = A.publishable_report(report)
        self.assertEqual(view["cohorts"], [])
        self.assertEqual(view["suppressed_cohorts"], [{"month": "2026-01", "reason": "retention_incomplete"}])

    def test_incomplete_only_month_withholds_the_next_publishable_month(self):
        # F3: an incomplete-only earlier month must not be silently absent
        # while the next publishable month is released.
        counts = {"delivered": 5, "failed": 5, "abandoned": 5, "ongoing": 5, "unknown": 0}
        report = self.base_report({"2026-02": synthetic_cell("2026-02", counts)})
        report["incomplete_cohorts"] = {"2026-01": 1}
        view = A.publishable_report(report)
        reasons = {item["month"]: item["reason"] for item in view["suppressed_cohorts"]}
        self.assertEqual(view["cohorts"], [])
        self.assertEqual(reasons.get("2026-01"), "retention_incomplete")
        self.assertEqual(reasons.get("2026-02"), "complementary_suppression")

    def test_open_only_month_is_listed_and_withholds_the_next_publishable_month(self):
        # F3: an open-only month previously vanished from suppressed_cohorts
        # and the next closed month published alone.
        counts = {"delivered": 5, "failed": 5, "abandoned": 5, "ongoing": 5, "unknown": 0}
        report = self.base_report({"2026-02": synthetic_cell("2026-02", counts)})
        report["open_cohorts"] = {"2026-01": 3}
        view = A.publishable_report(report)
        reasons = {item["month"]: item["reason"] for item in view["suppressed_cohorts"]}
        self.assertEqual(view["cohorts"], [])
        self.assertEqual(reasons.get("2026-01"), "cohort_open")
        self.assertEqual(reasons.get("2026-02"), "complementary_suppression")

    def test_two_retained_publishable_cohorts_are_both_published(self):
        # Control: complementary suppression must not withhold a pair of
        # publishable retained cohorts that have no suppressed earlier month.
        january = {"delivered": 10, "failed": 10, "abandoned": 0, "ongoing": 0, "unknown": 0}
        february = {"delivered": 5, "failed": 5, "abandoned": 5, "ongoing": 5, "unknown": 0}
        report = self.base_report(
            {
                "2026-01": synthetic_cell("2026-01", january),
                "2026-02": synthetic_cell("2026-02", february),
            }
        )
        view = A.publishable_report(report)
        self.assertEqual([item["month"] for item in view["cohorts"]], ["2026-01", "2026-02"])


class WithdrawalRevokesSiblingsTests(unittest.TestCase):
    """F1: withdrawing a workflow revokes every admission for that workflow."""

    def quarantined_admission(self, central, workflow_ref, issued=START):
        admission = A.issue_admission(central, notice_for(workflow_ref), issued_day=issued)
        envelope = make_envelope(
            workflow_ref,
            "crit-" + "9" * 32,
            START,
            S.STAGES,
            True,
            [{"kind": "observation", "value": "ongoing", "effective_day": START}],
            1,
            admission["admission_ref"],
        )
        result = A.import_export(central, envelope, capability=admission["capability"], receipt_day=advance(2))
        self.assertEqual(result["status"], "quarantined")
        return admission, envelope

    def sibling_state(self):
        workflow_ref = "wf-" + "f" * 32
        central = A.new_store()
        first, _ = self.quarantined_admission(central, workflow_ref)
        A.expire(central, today=advance(8))
        self.assertEqual(list(central["admission_tombstones"]), [first["admission_ref"]])
        second = A.issue_admission(central, notice_for(workflow_ref), issued_day=advance(7))
        self.assertIn(second["admission_ref"], central["admissions"])
        return central, workflow_ref, first, second

    def test_withdrawing_a_tombstoned_admission_revokes_a_sibling_active_admission(self):
        central, workflow_ref, first, second = self.sibling_state()
        result = A.withdraw(
            central,
            admission_ref=first["admission_ref"],
            capability=first["capability"],
            decision_day=advance(9),
        )
        self.assertEqual(result["deleted_records"], 0)
        self.assertEqual(central["admissions"], {})
        self.assertEqual(central["admission_tombstones"], {})
        self.assertEqual(central["quarantine"], [])

        # A later export naming the revoked sibling admission must not import
        # as accepted and re-create the record.
        notice = notice_for(workflow_ref)
        fresh = make_envelope(
            workflow_ref,
            notice["criteria_contract_ref"],
            START,
            S.STAGES,
            True,
            [{"kind": "observation", "value": "ongoing", "effective_day": START}],
            1,
            second["admission_ref"],
        )
        with self.assertRaises(S.ContractError) as caught:
            A.import_export(central, fresh, capability=second["capability"], receipt_day=advance(10))
        self.assertEqual(caught.exception.code, "unknown_admission")
        self.assertEqual(central["records"], {})

    def test_withdrawal_with_a_wrong_capability_revokes_nothing(self):
        central, workflow_ref, first, second = self.sibling_state()
        with self.assertRaises(S.ContractError) as caught:
            A.withdraw(
                central,
                admission_ref=first["admission_ref"],
                capability="00" * 32,
                decision_day=advance(9),
            )
        self.assertEqual(caught.exception.code, "bad_capability")
        self.assertIn(second["admission_ref"], central["admissions"])
        self.assertIn(first["admission_ref"], central["admission_tombstones"])
        self.assertEqual(len(central["quarantine"]), 1)

    def test_withdrawal_leaves_another_workflows_active_admission_alone(self):
        target = "wf-" + "1" * 32
        other = "wf-" + "2" * 32
        central = A.new_store()
        first, _ = self.quarantined_admission(central, target)
        A.expire(central, today=advance(8))
        A.issue_admission(central, notice_for(target), issued_day=advance(7))
        survivor = A.issue_admission(central, notice_for(other), issued_day=advance(7))
        A.withdraw(
            central,
            admission_ref=first["admission_ref"],
            capability=first["capability"],
            decision_day=advance(9),
        )
        self.assertIn(survivor["admission_ref"], central["admissions"])
        self.assertEqual(
            [ref for ref, admission in central["admissions"].items() if admission["workflow_ref"] == target],
            [],
        )


class SymlinkPathGuardTests(unittest.TestCase):
    """F2: every component of a store or export path must not be a symlink."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="aegis-fix5-symlink-")
        self.root = Path(self.temp.name)
        self.store = S.new_store()
        self.workflow = S.enable_capture(self.store, day=START, start_day=START)
        self.ref = self.workflow["workflow_ref"]
        S.record_transition(self.store, self.ref, kind="observation", value="ongoing", effective_day=START)
        self.workflow["admission_ref"] = ADMISSION
        self.payload, self.sha = S.preview_export(self.store, self.ref)

    def tearDown(self):
        self.temp.cleanup()

    def other_checkout(self):
        repo = self.root / "other-checkout"
        (repo / ".git").mkdir(parents=True, exist_ok=True)
        return repo

    def symlink(self, target, link, *, directory=False):
        try:
            os.symlink(target, link, target_is_directory=directory)
        except (OSError, NotImplementedError) as exc:
            self.skipTest("symlink creation unavailable on this host: " + str(exc))

    def test_store_with_a_final_symlink_inside_a_checkout_is_refused(self):
        repo = self.other_checkout()
        outside = self.root / "outside"
        outside.mkdir()
        target = outside / "store.json"
        link = repo / "store.json"
        self.symlink(target, link)
        with working_directory(self.root):
            with self.assertRaises(S.ContractError) as caught:
                S.save_store(link, S.new_store())
        self.assertEqual(caught.exception.code, "store_path_symlink")
        self.assertTrue(link.is_symlink())
        self.assertFalse(target.exists())

    def test_store_with_a_symlinked_parent_inside_a_checkout_is_refused(self):
        repo = self.other_checkout()
        outside = self.root / "outside"
        outside.mkdir()
        linked_dir = repo / "linked"
        self.symlink(outside, linked_dir, directory=True)
        target = linked_dir / "store.json"
        with working_directory(self.root):
            with self.assertRaises(S.ContractError) as caught:
                S.save_store(target, S.new_store())
        self.assertEqual(caught.exception.code, "store_path_symlink")
        self.assertFalse((outside / "store.json").exists())

    def test_store_with_a_dangling_symlink_is_refused(self):
        repo = self.other_checkout()
        target = self.root / "missing-store.json"
        link = repo / "store.json"
        self.symlink(target, link)
        with working_directory(self.root):
            with self.assertRaises(S.ContractError) as caught:
                S.save_store(link, S.new_store())
        self.assertEqual(caught.exception.code, "store_path_symlink")
        self.assertTrue(link.is_symlink())
        self.assertFalse(target.exists())

    def test_store_through_a_symlink_outside_version_control_is_refused(self):
        real = self.root / "real"
        real.mkdir()
        alias = self.root / "alias"
        self.symlink(real, alias, directory=True)
        with working_directory(self.root):
            with self.assertRaises(S.ContractError) as caught:
                S.save_store(alias / "store.json", S.new_store())
        self.assertEqual(caught.exception.code, "store_path_symlink")
        self.assertFalse((real / "store.json").exists())

    def test_export_with_a_final_symlink_is_refused(self):
        out = self.root / "export.json"
        target = self.root / "target.json"
        self.symlink(target, out)
        with working_directory(self.root):
            with self.assertRaises(S.ContractError) as caught:
                S.export_snapshot(self.store, self.ref, out, preview_sha256=self.sha, confirm=True)
        self.assertEqual(caught.exception.code, "export_path_symlink")
        self.assertTrue(out.is_symlink())
        self.assertFalse(target.exists())

    def test_export_with_a_dangling_symlink_is_refused(self):
        out = self.root / "export.json"
        target = self.root / "missing-export.json"
        self.symlink(target, out)
        with working_directory(self.root):
            with self.assertRaises(S.ContractError) as caught:
                S.export_snapshot(self.store, self.ref, out, preview_sha256=self.sha, confirm=True)
        self.assertEqual(caught.exception.code, "export_path_symlink")
        self.assertTrue(out.is_symlink())
        self.assertFalse(target.exists())

    def test_export_through_a_symlinked_parent_is_refused(self):
        real = self.root / "real"
        real.mkdir()
        alias = self.root / "alias"
        self.symlink(real, alias, directory=True)
        out = alias / "export.json"
        with working_directory(self.root):
            with self.assertRaises(S.ContractError) as caught:
                S.export_snapshot(self.store, self.ref, out, preview_sha256=self.sha, confirm=True)
        self.assertEqual(caught.exception.code, "export_path_symlink")
        self.assertFalse((real / "export.json").exists())

    def test_a_clean_path_still_writes_the_store_and_export(self):
        plain = self.root / "plain"
        store_path = plain / "store.json"
        S.save_store(store_path, self.store)
        self.assertTrue(store_path.exists())
        out = plain / "export.json"
        result = S.export_snapshot(self.store, self.ref, out, preview_sha256=self.sha, confirm=True)
        self.assertTrue(out.exists())
        self.assertEqual(result["sha256"], self.sha)


if __name__ == "__main__":
    unittest.main()
