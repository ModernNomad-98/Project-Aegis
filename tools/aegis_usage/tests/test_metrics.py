"""Metric tests: hand-calculated cohorts, day-30 horizons, denominators and suppression."""

import hashlib
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
FIXTURE_PATH = Path(__file__).parent / "fixtures" / "synthetic.json"
FIXTURE = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def add_days(start, days):
    return (date.fromisoformat(start) + timedelta(days=days)).isoformat()


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


def build_case(central, key, start, exports, stages=None, frozen=True, issued=None):
    stages = list(stages or S.STAGES)
    workflow_ref = "wf-" + hashlib.sha256(("case:" + key).encode("utf-8")).hexdigest()[:32]
    criteria_ref = "crit-" + hashlib.sha256(("crit:" + key).encode("utf-8")).hexdigest()[:32]
    notice = {
        "workflow_ref": workflow_ref,
        "start_day": start,
        "applicable_stages": stages,
        "criteria_frozen_before_work": frozen,
        "criteria_contract_ref": criteria_ref,
    }
    admission = aggregate.issue_admission(central, notice, issued_day=issued or start)
    cumulative = []
    for revision, (receipt, events) in enumerate(exports, start=1):
        cumulative = cumulative + list(events)
        envelope = make_envelope(workflow_ref, criteria_ref, start, stages, frozen, cumulative, revision, admission["admission_ref"])
        aggregate.import_export(central, envelope, capability=admission["capability"], receipt_day=receipt)
    return workflow_ref, admission


def fixture_store():
    central = aggregate.new_store()
    capabilities = {}
    for workflow in FIXTURE["workflows"]:
        cumulative = []
        notice = {
            "workflow_ref": workflow["workflow_ref"],
            "start_day": workflow["start_day"],
            "applicable_stages": workflow["applicable_stages"],
            "criteria_frozen_before_work": workflow["criteria_frozen_before_work"],
            "criteria_contract_ref": workflow["criteria_contract_ref"],
        }
        admission = aggregate.issue_admission(central, notice, issued_day=workflow["issued_day"])
        for revision, export in enumerate(workflow["exports"], start=1):
            cumulative = cumulative + list(export["events"])
            envelope = make_envelope(
                workflow["workflow_ref"],
                workflow["criteria_contract_ref"],
                workflow["start_day"],
                workflow["applicable_stages"],
                workflow["criteria_frozen_before_work"],
                cumulative,
                revision,
                admission["admission_ref"],
            )
            aggregate.import_export(central, envelope, capability=admission["capability"], receipt_day=export["receipt_day"])
        capabilities[workflow["workflow_ref"]] = admission["capability"]
    return central, capabilities


def bulk_cohort(central, start, outcomes):
    refs = []
    for index, outcome in enumerate(outcomes):
        key = "bulk:" + start + ":" + str(index)
        workflow_ref = "wf-" + hashlib.sha256(key.encode("utf-8")).hexdigest()[:32]
        criteria_ref = "crit-" + hashlib.sha256(("crit:" + key).encode("utf-8")).hexdigest()[:32]
        notice = {
            "workflow_ref": workflow_ref,
            "start_day": start,
            "applicable_stages": list(S.STAGES),
            "criteria_frozen_before_work": True,
            "criteria_contract_ref": criteria_ref,
        }
        admission = aggregate.issue_admission(central, notice, issued_day=start)
        tail = []
        if outcome in ("delivered", "delivered_nobuild"):
            tail = [
                {"kind": "status", "value": "delivered", "effective_day": add_days(start, 10)},
                {"kind": "acceptance", "value": "independent_attested_pass", "effective_day": add_days(start, 12)},
            ]
            if outcome == "delivered":
                tail.insert(0, {"kind": "stage", "value": "complete", "effective_day": add_days(start, 5), "stage": "build"})
        elif outcome == "failed":
            tail = [{"kind": "status", "value": "failed", "effective_day": add_days(start, 10)}]
        elif outcome == "abandoned":
            tail = [{"kind": "status", "value": "abandoned", "effective_day": add_days(start, 10)}]
        elif outcome == "ongoing":
            tail = [{"kind": "observation", "value": "ongoing", "effective_day": add_days(start, 30)}]
        cumulative = [{"kind": "observation", "value": "ongoing", "effective_day": start}]
        first = make_envelope(workflow_ref, criteria_ref, start, S.STAGES, True, cumulative, 1, admission["admission_ref"])
        aggregate.import_export(central, first, capability=admission["capability"], receipt_day=add_days(start, 1))
        if tail:
            cumulative = cumulative + tail
            second = make_envelope(workflow_ref, criteria_ref, start, S.STAGES, True, cumulative, 2, admission["admission_ref"])
            aggregate.import_export(central, second, capability=admission["capability"], receipt_day=add_days(start, 31))
        refs.append(workflow_ref)
    return refs


def cell(report, month):
    return report["cohorts"][month]


class FixtureCohortTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.store, cls.capabilities = fixture_store()
        cls.report = aggregate.compute_report(cls.store, as_of=FIXTURE["report_as_of"])

    def test_fixture_n_and_outcomes_are_hand_calculated(self):
        for month, expected in FIXTURE["expectations"].items():
            with self.subTest(month=month):
                got = cell(self.report, month)
                self.assertEqual(got["n"], expected["n"])
                self.assertEqual(got["outcomes"], expected["outcomes"])
                self.assertEqual(got["closed_on"], expected["closed_on"])

    def test_fixture_rates_match_hand_calculation(self):
        for month, expected in FIXTURE["expectations"].items():
            got = cell(self.report, month)["metrics"]
            for name in ("delivery_30d", "follow_up_coverage", "unknown_share", "ongoing_share", "abandoned_share", "failed_share"):
                with self.subTest(month=month, metric=name):
                    self.assertEqual([got[name]["numerator"], got[name]["denominator"]], expected[name])

    def test_fixture_stage_reach_and_not_applicable(self):
        got = cell(self.report, "2026-01")["metrics"]["stage_reach"]
        for stage, expected in FIXTURE["expectations"]["2026-01"]["stage_reach"].items():
            with self.subTest(stage=stage):
                block = got[stage]
                self.assertEqual([block["numerator"], block["denominator"], block["not_applicable"]], expected)
        self.assertEqual(cell(self.report, "2026-02")["metrics"]["stage_reach"]["build"]["numerator"], 1)
        self.assertEqual(cell(self.report, "2026-02")["metrics"]["stage_reach"]["validate"]["denominator"], 1)

    def test_fixture_acceptance_strata_and_attested_success(self):
        january = cell(self.report, "2026-01")["metrics"]
        self.assertEqual(january["assessed_acceptance_self_report"]["status"], "unavailable")
        self.assertEqual(
            [january["assessed_acceptance_independent"]["numerator"], january["assessed_acceptance_independent"]["denominator"]],
            [1, 1],
        )
        self.assertEqual(
            [january["independently_attested_success"]["numerator"], january["independently_attested_success"]["denominator"]],
            [1, 6],
        )

    def test_fixture_evidence_flags(self):
        january = cell(self.report, "2026-01")
        self.assertEqual(january["late_entries"], 0)
        self.assertEqual(january["late_events"], 0)
        self.assertEqual(january["frozen_criteria_invalidated"], 0)
        self.assertEqual(cell(self.report, "2026-02")["frozen_criteria_invalidated"], 1)
        self.assertEqual(cell(self.report, "2026-02")["metrics"]["independently_attested_success"]["numerator"], 0)

    def test_publishable_view_withholds_every_small_cohort(self):
        view = aggregate.publishable_report(self.report)
        self.assertFalse(view["disclosure"]["public_release"])
        self.assertEqual(len(view["cohorts"]), FIXTURE["publishable"]["published_cohorts"])
        self.assertEqual(
            [(item["month"], item["reason"]) for item in view["suppressed_cohorts"]],
            [(item["month"], item["reason"]) for item in FIXTURE["publishable"]["suppressed"]],
        )

    def test_open_cohorts_are_separate(self):
        early = aggregate.compute_report(self.store, as_of="2026-02-01")
        self.assertEqual(early["open_cohorts"].get("2026-01"), 6)
        self.assertNotIn("2026-01", early["cohorts"])


class Day30HorizonTests(unittest.TestCase):
    def test_ongoing_at_cutoff_then_day31_failure_stays_ongoing(self):
        central = aggregate.new_store()
        start = "2026-01-05"
        build_case(
            central,
            "ongoing-then-fail",
            start,
            [
                (add_days(start, 2), [{"kind": "observation", "value": "ongoing", "effective_day": start}]),
                (
                    add_days(start, 33),
                    [
                        {"kind": "observation", "value": "ongoing", "effective_day": add_days(start, 30)},
                        {"kind": "status", "value": "failed", "effective_day": add_days(start, 31)},
                    ],
                ),
            ],
        )
        report = aggregate.compute_report(central, as_of=add_days(start, 40))
        outcomes = cell(report, start[:7])["outcomes"]
        self.assertEqual(outcomes, {"delivered": 0, "failed": 0, "abandoned": 0, "ongoing": 1, "unknown": 0})

    def test_missing_cutoff_observation_is_unknown(self):
        central = aggregate.new_store()
        start = "2026-01-05"
        build_case(
            central,
            "missing-cutoff",
            start,
            [
                (add_days(start, 2), [{"kind": "observation", "value": "ongoing", "effective_day": start}]),
                (add_days(start, 33), [{"kind": "status", "value": "failed", "effective_day": add_days(start, 31)}]),
            ],
        )
        report = aggregate.compute_report(central, as_of=add_days(start, 40))
        self.assertEqual(cell(report, start[:7])["outcomes"]["unknown"], 1)
        self.assertEqual(cell(report, start[:7])["outcomes"]["failed"], 0)

    def test_day30_failure_reported_day33_is_failed(self):
        central = aggregate.new_store()
        start = "2026-01-05"
        build_case(
            central,
            "day30-fail",
            start,
            [
                (add_days(start, 2), [{"kind": "observation", "value": "ongoing", "effective_day": start}]),
                (add_days(start, 33), [{"kind": "status", "value": "failed", "effective_day": add_days(start, 30)}]),
            ],
        )
        report = aggregate.compute_report(central, as_of=add_days(start, 40))
        self.assertEqual(cell(report, start[:7])["outcomes"]["failed"], 1)
        self.assertEqual(cell(report, start[:7])["outcomes"]["ongoing"], 0)

    def test_day31_abandonment_is_not_counted_at_day30(self):
        central = aggregate.new_store()
        start = "2026-01-05"
        build_case(
            central,
            "day31-abandon",
            start,
            [
                (add_days(start, 2), [{"kind": "observation", "value": "ongoing", "effective_day": start}]),
                (
                    add_days(start, 33),
                    [
                        {"kind": "observation", "value": "ongoing", "effective_day": add_days(start, 30)},
                        {"kind": "status", "value": "abandoned", "effective_day": add_days(start, 31)},
                    ],
                ),
            ],
        )
        report = aggregate.compute_report(central, as_of=add_days(start, 40))
        outcomes = cell(report, start[:7])["outcomes"]
        self.assertEqual((outcomes["abandoned"], outcomes["ongoing"]), (0, 1))

    def test_day30_abandonment_is_counted_at_day30(self):
        central = aggregate.new_store()
        start = "2026-01-05"
        build_case(
            central,
            "day30-abandon",
            start,
            [
                (add_days(start, 2), [{"kind": "observation", "value": "ongoing", "effective_day": start}]),
                (add_days(start, 33), [{"kind": "status", "value": "abandoned", "effective_day": add_days(start, 30)}]),
            ],
        )
        report = aggregate.compute_report(central, as_of=add_days(start, 40))
        self.assertEqual(cell(report, start[:7])["outcomes"]["abandoned"], 1)

    def test_stage_completion_day31_is_not_reached(self):
        central = aggregate.new_store()
        start = "2026-01-05"
        build_case(
            central,
            "stage-day31",
            start,
            [
                (add_days(start, 2), [{"kind": "observation", "value": "ongoing", "effective_day": start}]),
                (
                    add_days(start, 33),
                    [
                        {"kind": "observation", "value": "ongoing", "effective_day": add_days(start, 30)},
                        {"kind": "stage", "value": "complete", "effective_day": add_days(start, 31), "stage": "build"},
                    ],
                ),
            ],
        )
        report = aggregate.compute_report(central, as_of=add_days(start, 40))
        build = cell(report, start[:7])["metrics"]["stage_reach"]["build"]
        self.assertEqual((build["numerator"], build["denominator"]), (0, 1))

    def test_stage_completion_day30_is_reached(self):
        central = aggregate.new_store()
        start = "2026-01-05"
        build_case(
            central,
            "stage-day30",
            start,
            [
                (add_days(start, 2), [{"kind": "observation", "value": "ongoing", "effective_day": start}]),
                (
                    add_days(start, 33),
                    [
                        {"kind": "observation", "value": "ongoing", "effective_day": add_days(start, 30)},
                        {"kind": "stage", "value": "complete", "effective_day": add_days(start, 30), "stage": "build"},
                    ],
                ),
            ],
        )
        report = aggregate.compute_report(central, as_of=add_days(start, 40))
        build = cell(report, start[:7])["metrics"]["stage_reach"]["build"]
        self.assertEqual((build["numerator"], build["denominator"]), (1, 1))

    def test_delivery_does_not_imply_earlier_stage_completion(self):
        central = aggregate.new_store()
        start = "2026-01-05"
        build_case(
            central,
            "delivery-no-stages",
            start,
            [
                (add_days(start, 2), [{"kind": "observation", "value": "ongoing", "effective_day": start}]),
                (
                    add_days(start, 21),
                    [{"kind": "status", "value": "delivered", "effective_day": add_days(start, 20)}],
                ),
            ],
        )
        report = aggregate.compute_report(central, as_of=add_days(start, 40))
        reach = cell(report, start[:7])["metrics"]["stage_reach"]
        self.assertEqual(reach["deliver"]["numerator"], 0)
        self.assertEqual(cell(report, start[:7])["outcomes"]["delivered"], 1)


class DenominatorAndBiasTests(unittest.TestCase):
    def test_zero_denominator_is_unavailable(self):
        central = aggregate.new_store()
        start = "2026-01-05"
        build_case(
            central,
            "zero-denominator",
            start,
            [
                (add_days(start, 2), [{"kind": "observation", "value": "ongoing", "effective_day": start}]),
                (add_days(start, 33), [{"kind": "status", "value": "failed", "effective_day": add_days(start, 31)}]),
            ],
        )
        report = aggregate.compute_report(central, as_of=add_days(start, 40))
        metrics = cell(report, start[:7])["metrics"]
        for name in ("assessed_acceptance_self_report", "assessed_acceptance_independent"):
            self.assertEqual(metrics[name]["status"], "unavailable")
            self.assertIsNone(metrics[name]["rate"])
            self.assertEqual(metrics[name]["denominator"], 0)

    def test_report_after_retention_expiry_is_explicitly_incomplete(self):
        central = aggregate.new_store()
        start = "2026-01-05"
        workflow, _ = build_case(
            central,
            "expired-report",
            start,
            [
                (add_days(start, 2), [{"kind": "observation", "value": "ongoing", "effective_day": start}]),
                (add_days(start, 31), [{"kind": "observation", "value": "ongoing", "effective_day": add_days(start, 30)}]),
            ],
        )
        self.assertIn(workflow, central["records"])
        report = aggregate.compute_report(central, as_of=add_days(start, 100))
        self.assertEqual(report["expired_excluded"], 1)
        self.assertNotIn(start[:7], report["cohorts"])

    def test_retrospective_first_receipt_is_excluded_from_rates(self):
        central = aggregate.new_store()
        start = "2026-01-05"
        build_case(
            central,
            "retrospective",
            start,
            [(add_days(start, 9), [{"kind": "observation", "value": "ongoing", "effective_day": start}])],
            issued=add_days(start, 6),
        )
        report = aggregate.compute_report(central, as_of=add_days(start, 40))
        self.assertEqual(report["retrospective_excluded"], 1)
        self.assertNotIn(start[:7], report["cohorts"])

    def test_late_update_cannot_rewrite_day30(self):
        central = aggregate.new_store()
        start = "2026-01-05"
        build_case(
            central,
            "late-update",
            start,
            [
                (add_days(start, 2), [{"kind": "observation", "value": "ongoing", "effective_day": start}]),
                (add_days(start, 46), [{"kind": "status", "value": "delivered", "effective_day": add_days(start, 20)}]),
            ],
        )
        report = aggregate.compute_report(central, as_of=add_days(start, 60))
        january = cell(report, start[:7])
        self.assertEqual(january["outcomes"]["unknown"], 1)
        self.assertEqual(january["outcomes"]["delivered"], 0)
        self.assertEqual(january["late_entries"], 1)
        self.assertEqual(january["late_events"], 1)

    def test_scope_change_invalidates_frozen_criteria_success(self):
        store, _ = fixture_store()
        report = aggregate.compute_report(store, as_of=FIXTURE["report_as_of"])
        february = cell(report, "2026-02")
        self.assertEqual(february["outcomes"]["delivered"], 1)
        self.assertEqual(february["frozen_criteria_invalidated"], 1)
        self.assertEqual(february["metrics"]["independently_attested_success"]["numerator"], 0)
        self.assertEqual(february["metrics"]["assessed_acceptance_independent"]["numerator"], 1)


class ImmutableEnrollmentTests(unittest.TestCase):
    def admission_ref(self, store, workflow_ref):
        for ref, admission in store["admissions"].items():
            if admission["workflow_ref"] == workflow_ref:
                return ref
        raise AssertionError("no active admission for the workflow")

    def cumulative(self, workflow):
        events = []
        for export in workflow["exports"]:
            events = events + list(export["events"])
        return events

    def test_higher_revision_enrollment_change_is_rejected_and_rates_hold(self):
        store, capabilities = fixture_store()
        before = aggregate.compute_report(store, as_of=FIXTURE["report_as_of"])
        workflow = FIXTURE["workflows"][0]
        workflow_ref = workflow["workflow_ref"]
        stored_revision = store["records"][workflow_ref]["revision"]
        envelope = make_envelope(
            workflow_ref,
            workflow["criteria_contract_ref"],
            "2026-01-04",
            workflow["applicable_stages"],
            workflow["criteria_frozen_before_work"],
            self.cumulative(workflow),
            3,
            self.admission_ref(store, workflow_ref),
        )
        result = aggregate.import_export(store, envelope, capability=capabilities[workflow_ref], receipt_day="2026-01-23")
        self.assertEqual(result["status"], "quarantined")
        self.assertEqual(result["code"], "enrollment_change")
        after = aggregate.compute_report(store, as_of=FIXTURE["report_as_of"])
        self.assertEqual(after["cohorts"], before["cohorts"])
        self.assertEqual(store["records"][workflow_ref]["revision"], stored_revision)

    def test_applicability_change_is_rejected(self):
        store, capabilities = fixture_store()
        workflow = FIXTURE["workflows"][0]
        workflow_ref = workflow["workflow_ref"]
        envelope = make_envelope(
            workflow_ref,
            workflow["criteria_contract_ref"],
            workflow["start_day"],
            ["discover", "plan", "build", "deliver"],
            workflow["criteria_frozen_before_work"],
            [item for item in self.cumulative(workflow) if item.get("stage") != "validate"],
            3,
            self.admission_ref(store, workflow_ref),
        )
        result = aggregate.import_export(store, envelope, capability=capabilities[workflow_ref], receipt_day="2026-01-23")
        self.assertEqual(result["status"], "quarantined")
        self.assertEqual(result["code"], "enrollment_change")


class SuppressionTests(unittest.TestCase):
    def test_cohort_below_floor_is_withheld(self):
        central = aggregate.new_store()
        start = "2026-01-05"
        bulk_cohort(central, start, ["delivered"] * 19)
        report = aggregate.compute_report(central, as_of=add_days(start, 40))
        view = aggregate.publishable_report(report)
        self.assertEqual(view["cohorts"], [])
        self.assertEqual(view["suppressed_cohorts"][0]["reason"], "cohort_below_floor")

    def test_full_cells_are_published(self):
        central = aggregate.new_store()
        start = "2026-01-05"
        bulk_cohort(central, start, ["delivered"] * 5 + ["failed"] * 5 + ["abandoned"] * 5 + ["ongoing"] * 5)
        report = aggregate.compute_report(central, as_of=add_days(start, 40))
        view = aggregate.publishable_report(report)
        self.assertEqual(len(view["cohorts"]), 1)
        self.assertEqual(view["cohorts"][0]["n"], 20)
        self.assertEqual(view["cohorts"][0]["outcomes"]["delivered"], 5)

    def test_sparse_outcome_suppresses_cell_and_complementary_cell(self):
        central = aggregate.new_store()
        first = "2026-01-05"
        second = "2026-02-05"
        bulk_cohort(central, first, ["delivered"] * 6 + ["failed"] * 5 + ["abandoned"] * 5 + ["unknown"] * 4)
        bulk_cohort(central, second, ["delivered"] * 5 + ["failed"] * 5 + ["abandoned"] * 5 + ["ongoing"] * 5)
        report = aggregate.compute_report(central, as_of="2026-04-01")
        view = aggregate.publishable_report(report)
        reasons = {item["month"]: item["reason"] for item in view["suppressed_cohorts"]}
        self.assertEqual(reasons.get(first[:7]), "sparse_outcome")
        self.assertEqual(reasons.get(second[:7]), "complementary_suppression")
        self.assertEqual(view["cohorts"], [])

    def test_differencing_withholds_a_shifted_month(self):
        # Suppression is tested on a synthetic report so that the 90-day raw
        # retention, which cannot hold three closed monthly cohorts at once,
        # does not confound the disclosure arithmetic.
        def cell(month, counts):
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
                "late_entries": 0,
                "late_events": 0,
            }

        base = {"delivered": 5, "failed": 5, "abandoned": 5, "ongoing": 5, "unknown": 0}
        shifted = {"delivered": 9, "failed": 5, "abandoned": 5, "ongoing": 5, "unknown": 0}
        report = {
            "report_version": aggregate.REPORT_VERSION,
            "as_of": "2026-05-01",
            "cohorts": {"2026-01": cell("2026-01", base), "2026-02": cell("2026-02", shifted), "2026-03": cell("2026-03", base)},
            "withdrawals": 0,
            "limitations": [],
        }
        view = aggregate.publishable_report(report)
        published = [item["month"] for item in view["cohorts"]]
        reasons = {item["month"]: item["reason"] for item in view["suppressed_cohorts"]}
        self.assertEqual(published, ["2026-01", "2026-03"])
        self.assertEqual(reasons.get("2026-02"), "differencing_withheld")
        self.assertEqual(view["cohorts"][0]["outcomes"]["delivered"], 5)

    def test_stage_cell_with_small_numerator_is_withheld(self):
        central = aggregate.new_store()
        start = "2026-01-05"
        bulk_cohort(
            central,
            start,
            ["delivered"] * 2 + ["delivered_nobuild"] * 3 + ["failed"] * 5 + ["abandoned"] * 5 + ["ongoing"] * 5,
        )
        report = aggregate.compute_report(central, as_of=add_days(start, 40))
        view = aggregate.publishable_report(report)
        self.assertEqual(view["cohorts"][0]["outcomes"]["delivered"], 5)
        build = view["cohorts"][0]["stage_reach"]["build"]
        self.assertEqual(build, {"status": "withheld", "reason": "sparse_stage_cell"})


class MutantDetectionTests(unittest.TestCase):
    def load_mutant(self, source_name, replacements):
        source_path = REPO_ROOT / "tools" / "aegis_usage" / source_name
        source = source_path.read_text(encoding="utf-8")
        for old, new in replacements:
            self.assertIn(old, source, "mutation anchor missing: " + old)
            source = source.replace(old, new, 1)
        folder = tempfile.mkdtemp(prefix="aegis-mutant-")
        target = Path(folder) / ("mutant_" + source_name)
        target.write_text(source, encoding="utf-8", newline="\n")
        spec = importlib.util.spec_from_file_location("mutant_" + source_name.replace(".py", "") + "_" + str(id(target)), target)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_day30_filter_mutant_counts_a_day31_failure(self):
        central = aggregate.new_store()
        start = "2026-01-05"
        build_case(
            central,
            "mutant-day30",
            start,
            [
                (add_days(start, 2), [{"kind": "observation", "value": "ongoing", "effective_day": start}]),
                (
                    add_days(start, 33),
                    [
                        {"kind": "observation", "value": "ongoing", "effective_day": add_days(start, 30)},
                        {"kind": "status", "value": "failed", "effective_day": add_days(start, 31)},
                    ],
                ),
            ],
        )
        real = aggregate.compute_report(central, as_of=add_days(start, 40))["cohorts"][start[:7]]["outcomes"]
        self.assertEqual((real["ongoing"], real["failed"]), (1, 0))
        mutant = self.load_mutant(
            "aggregate.py",
            [('if event["effective_day"] <= cutoff and event["first_receipt_day"] <= close_day',
              'if event["effective_day"] <= close_day and event["first_receipt_day"] <= close_day')],
        )
        broken = mutant.compute_report(central, as_of=add_days(start, 40))["cohorts"][start[:7]]["outcomes"]
        self.assertEqual((broken["ongoing"], broken["failed"]), (0, 1))
        self.assertNotEqual(real, broken)

    def test_conflict_mutant_accepts_a_conflicting_revision(self):
        central = aggregate.new_store()
        start = "2026-01-05"
        key = "mutant-conflict"
        workflow_ref = "wf-" + hashlib.sha256(("case:" + key).encode("utf-8")).hexdigest()[:32]
        criteria_ref = "crit-" + hashlib.sha256(("crit:" + key).encode("utf-8")).hexdigest()[:32]
        _, admission = build_case(
            central,
            key,
            start,
            [(add_days(start, 2), [{"kind": "observation", "value": "ongoing", "effective_day": start}])],
        )
        tampered = make_envelope(
            workflow_ref,
            criteria_ref,
            start,
            S.STAGES,
            True,
            [{"kind": "observation", "value": "ongoing", "effective_day": start}],
            1,
            admission["admission_ref"],
        )
        tampered["snapshot"]["export_ref"] = "exp-" + "a" * 32
        real = aggregate.import_export(central, tampered, capability=admission["capability"], receipt_day=add_days(start, 3))
        self.assertEqual(real["status"], "quarantined")
        self.assertEqual(real["code"], "conflicting_revision")
        mutant = self.load_mutant("aggregate.py", [('if record["canonical_export"] == _canonical_text(envelope):', "if True:")])
        broken = mutant.import_export(central, tampered, capability=admission["capability"], receipt_day=add_days(start, 3))
        self.assertEqual(broken["status"], "duplicate")
        self.assertNotEqual(real["status"], broken["status"])


if __name__ == "__main__":
    unittest.main()
