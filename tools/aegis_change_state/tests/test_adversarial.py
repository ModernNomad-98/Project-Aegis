"""C1.3 adversarial matrix: thirteen rows, fail-closed evidence, named UNRUNs.

Rows 1-12 are exercised against the C1.2 producers and, where the contract
term belongs to the merged checker, against the merged checker's own fixture
bundles read-only by path.  Row 13 needs a real authorised host and is
recorded as UNRUN with the exact missing authority; it is never reported as a
pass and nothing here simulates host behaviour.

Concurrency is modelled by ordered record sequences (two freezes, a second
holder, a truncated ledger), never by real race timing.
"""

from __future__ import annotations

import json
import pathlib
import shutil
import sys
import unittest

if str(pathlib.Path(__file__).resolve().parents[3]) not in sys.path:
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

import _fixtures  # noqa: E402
from tools.aegis_change_state import checks, records, schema  # noqa: E402

MATRIX = (
    {
        "row": 1,
        "scenario": "same-tree / in-flight head movement",
        "expected": ["HEAD_MOVED_OR_BASE_INVALIDATED"],
        "evidence": "fixture:adversarial-same-tree-head-move.json",
        "status": "RUN",
    },
    {
        "row": 2,
        "scenario": "duplicate lanes: two active D holders for one candidate",
        "expected": ["CANONICAL_FIELD_MISSING_OR_MISMATCH"],
        "evidence": "fixture:stage-duplicate-lane.json",
        "status": "RUN",
    },
    {
        "row": 3,
        "scenario": "stage substitution: an E record offered as D",
        "expected": ["STAGE_VERDICT_NOT_ACCEPTED"],
        "evidence": "fixture:stage-substitution.json",
        "status": "RUN",
    },
    {
        "row": 4,
        "scenario": "stale evidence: a foreign/earlier export and an older-head freeze",
        "expected": ["REQUIRED_INPUT_UNAVAILABLE", "HEAD_MOVED_OR_BASE_INVALIDATED"],
        "evidence": "fixture:head-history-foreign-export.json",
        "status": "RUN",
    },
    {
        "row": 5,
        "scenario": "freeze races: two freezes and a settlement before the checks finish",
        "expected": ["STATE_TAMPER_SUSPECTED", "MISSING_REQUIRED_REVIEW_OR_DISPOSITION"],
        "evidence": "fixture:adversarial-freeze-race.json",
        "status": "RUN",
    },
    {
        "row": 6,
        "scenario": "concurrent attempts: a stale auditor finishing after a head move",
        "expected": ["HEAD_MOVED_OR_BASE_INVALIDATED", "STATE_TAMPER_SUSPECTED"],
        "evidence": "fixture:adversarial-same-tree-head-move.json + freeze set",
        "status": "RUN",
    },
    {
        "row": 7,
        "scenario": "replacement agents and renamed items: explicit replacement, no count reset",
        "expected": ["NO_DUPLICATE_LANE_WHEN_REPLACEMENT_IS_RECORDED"],
        "evidence": "producer:replacement_of + ledger restart",
        "status": "RUN",
    },
    {
        "row": 8,
        "scenario": "stale authority: a fabricated VERIFIED binding",
        "expected": ["STATE_TAMPER_SUSPECTED"],
        "evidence": "producer:manifest provenance binding",
        "status": "RUN",
    },
    {
        "row": 9,
        "scenario": "state tampering: edited/removed ledger line, mismatched digest",
        "expected": ["STATE_TAMPER_SUSPECTED"],
        "evidence": "producer:ledger + manifest",
        "status": "RUN",
    },
    {
        "row": 10,
        "scenario": "unauthorized exceptions: a self-written fourth-head exception",
        "expected": ["AUTHORITY_ABSENT", "REVIEW_BUDGET_EXHAUSTED"],
        "evidence": "fixture:adversarial-unauthorized-exception.json",
        "status": "RUN",
    },
    {
        "row": 11,
        "scenario": "non-affirmative, security, auth and budget rules",
        "expected": [
            "VERDICT_NOT_AFFIRMATIVE",
            "STAGE_VERDICT_NOT_ACCEPTED",
            "SECURITY_FLAG_SET",
            "REVIEW_BUDGET_EXHAUSTED",
            "VERDICT_STALE_OR_UNVERIFIED",
        ],
        "evidence": "merged-checker fixtures: f-revise, d-revise, secret-flag-true, "
        "fourth-head-no-exception, unverified-auth",
        "status": "RUN",
    },
    {
        "row": 12,
        "scenario": "overclaim: a bypass displayed as green and coverage claimed without T5",
        "expected": ["CANONICAL_FIELD_MISSING_OR_MISMATCH"],
        "evidence": "fixture:adversarial-overclaim-bypass.json",
        "status": "RUN",
    },
    {
        "row": 13,
        "scenario": "host-side adversarial (denied call then retry, config edit/restart, "
        "custom executor/ACP/terminal routes, counter-store editability)",
        "expected": ["NOT_COVERED_OR_UNKNOWN"],
        "evidence": "UNRUN",
        "status": "UNRUN",
        "missing_authority": ["T5 mounted-coverage export", "T4 settings/identity", "T9 host authority"],
    },
)


def _rewrite_declaration(bundle, stage: str, mutate) -> None:
    path = pathlib.Path(bundle) / "stage-records" / (stage + ".json")
    document = schema.load_json(path)
    payload = dict(document["payload"])
    mutate(payload)
    provenance = document["provenance"]
    rebuilt = schema.build_envelope(
        payload,
        source_ref=str(provenance["source_ref"]),
        as_of=str(provenance["as_of"]),
        producer_role=str(provenance["producer_role"]),
        producer_identity_ref=str(provenance["producer_identity_ref"]),
    )
    _fixtures.write_json(path, rebuilt)


class AdversarialMatrixShapeTest(unittest.TestCase):
    def test_all_thirteen_rows_are_present_and_ordered(self):
        self.assertEqual([row["row"] for row in MATRIX], list(range(1, 14)))

    def test_every_row_states_an_expected_fail_closed_outcome(self):
        for row in MATRIX:
            with self.subTest(row=row["row"]):
                self.assertTrue(row["expected"])
                self.assertTrue(row["evidence"])

    def test_host_side_row_is_unrun_with_named_authority(self):
        row = MATRIX[12]
        self.assertEqual(row["status"], "UNRUN")
        self.assertIn("T5 mounted-coverage export", row["missing_authority"])
        self.assertNotIn("PASS", row["expected"])


class AdversarialRowsOneToSixTest(unittest.TestCase):
    def setUp(self):
        self.temporary = _fixtures.temporary_directory()
        self.addCleanup(lambda: shutil.rmtree(str(self.temporary), ignore_errors=True))
        self.bundle = _fixtures.build_bundle(self.temporary / "bundle")

    def test_row_1_same_tree_head_move(self):
        document = _fixtures.load("adversarial-same-tree-head-move.json")
        self.assertTrue(document["tree_preserved"])
        issues, derived = checks.freeze_issues(document["freeze"], identity=document["identity"])
        self.assertIn(schema.CODE_HEAD_MOVED, _fixtures.codes(issues))
        self.assertFalse(derived["valid"])

    def test_row_2_duplicate_lanes(self):
        _fixtures.replace_stage(self.bundle, "D2", "stage-duplicate-lane.json")
        report = checks.validate_bundle(self.bundle)
        self.assertFalse(report["ok"])
        self.assertIn(schema.CODE_CANONICAL, _fixtures.blockers_codes(report))
        self.assertEqual(report["derived"]["stage_records"]["stages"]["D"], "ACCEPT")

    def test_row_3_stage_substitution(self):
        _fixtures.replace_stage(self.bundle, "D", "stage-substitution.json")
        report = checks.validate_bundle(self.bundle)
        self.assertFalse(report["ok"])
        self.assertIn(schema.CODE_STAGE, _fixtures.blockers_codes(report))
        details = " ".join(blocker["detail"] for blocker in report["blockers"])
        self.assertIn("not in the stage vocabulary", details)
        self.assertIn("record body declares 'E'", details)

    def test_row_4_stale_evidence(self):
        foreign = _fixtures.load("head-history-foreign-export.json")
        issues, _derived = checks.head_history_issues(
            foreign, change_id=_fixtures.CHANGE_ID, candidate_head=_fixtures.HEAD
        )
        self.assertEqual(_fixtures.codes(issues), [schema.CODE_REQUIRED_INPUT])
        freeze = _fixtures.load("adversarial-same-tree-head-move.json")["freeze"]
        stale_issues, _ = checks.freeze_issues(freeze, identity={"head_sha": _fixtures.HEAD})
        self.assertIn(schema.CODE_HEAD_MOVED, _fixtures.codes(stale_issues))

    def test_row_5_freeze_race(self):
        document = _fixtures.load("adversarial-freeze-race.json")
        set_issues, payloads = checks.freeze_set_issues(document["freezes"])
        self.assertEqual(_fixtures.codes(set_issues), [schema.CODE_TAMPER])
        self.assertEqual(len(payloads), 2)
        settlement_issues, derived = checks.settlement_issues(document["settlement"])
        self.assertIn(schema.CODE_MISSING_REVIEW, _fixtures.codes(settlement_issues))
        self.assertFalse(derived["settled"])

    def test_row_6_concurrent_attempts(self):
        document = _fixtures.load("adversarial-same-tree-head-move.json")
        stale, _ = checks.freeze_issues(document["freeze"], identity={"head_sha": _fixtures.HEAD, "tree_sha": _fixtures.TREE})
        self.assertIn(schema.CODE_HEAD_MOVED, _fixtures.codes(stale))
        race = _fixtures.load("adversarial-freeze-race.json")
        set_issues, _payloads = checks.freeze_set_issues(race["freezes"])
        self.assertIn(schema.CODE_TAMPER, _fixtures.codes(set_issues))


class AdversarialRowsSevenToTwelveTest(unittest.TestCase):
    def setUp(self):
        self.temporary = _fixtures.temporary_directory()
        self.addCleanup(lambda: shutil.rmtree(str(self.temporary), ignore_errors=True))
        self.bundle = _fixtures.build_bundle(self.temporary / "bundle")

    def test_row_7_replacement_is_explicit_and_counters_survive_restart(self):
        _rewrite_declaration(
            self.bundle,
            "D",
            lambda payload: payload.update({"replacement_of": "stage-D-c12c14-0000"}),
        )
        _fixtures.refresh_manifest(self.bundle)
        report = checks.validate_bundle(self.bundle)
        self.assertTrue(report["ok"], report["blockers"])
        ledger = self.bundle / "ledger" / (_fixtures.CHANGE_ID + ".jsonl")
        before, lines, issues = records.read_jsonl(ledger)
        self.assertEqual(issues, [])
        appended = records.append_event(
            ledger,
            {
                "head_sha": "8e0f2a4c6b8d0e1f3a5c7b9d2e4f6a8c0b1d3e5f",
                "kind": "FINAL_BLOCKING_FIX",
                "exception_ref": None,
                "counted_at": "2026-11-11T06:00:00Z",
                "recorded_by": "fixture",
            },
        )
        self.assertEqual(appended["seq"], len(before) + 1)
        reloaded, raw_lines, _ = records.read_jsonl(ledger)
        self.assertEqual(records.validate_chain(reloaded, raw_lines), [])

    def test_row_7_a_waived_stage_without_a_waiver_is_refused(self):
        _rewrite_declaration(self.bundle, "B", lambda payload: payload.update({"applicability": "WAIVED"}))
        _fixtures.refresh_manifest(self.bundle)
        report = checks.validate_bundle(self.bundle)
        self.assertIn("waiver_ref", " ".join(blocker["detail"] for blocker in report["blockers"]))
        self.assertIn(schema.CODE_STAGE, _fixtures.blockers_codes(report))

    def test_row_8_fabricated_verified_authority_is_tamper(self):
        manifest = records.build_manifest(_fixtures.CHANGE_ID, [], {})
        manifest["provenance_binding"] = dict(manifest["provenance_binding"])
        manifest["provenance_binding"]["binding_status"] = "VERIFIED"
        manifest["store_digest"] = records.manifest_digest(manifest)
        self.assertIn(schema.CODE_TAMPER, _fixtures.codes(records.validate_manifest(self.bundle, manifest)))
        report = checks.validate_bundle(self.bundle)
        self.assertEqual(report["derived"]["review_heads"]["used"], 2)
        self.assertEqual(report["readiness"], "NOT_COMPUTED")

    def test_row_9_state_tampering(self):
        ledger = self.bundle / "ledger" / (_fixtures.CHANGE_ID + ".jsonl")
        lines = ledger.read_bytes().split(b"\n")
        lines[0] = lines[0].replace(b'"kind":"INITIAL"', b'"kind":"RESYNC"')
        ledger.write_bytes(b"\n".join(lines))
        report = checks.validate_bundle(self.bundle)
        self.assertFalse(report["ok"])
        self.assertIn(schema.CODE_TAMPER, _fixtures.blockers_codes(report))

    def test_row_9_removed_ledger_line_is_tamper(self):
        ledger = self.bundle / "ledger" / (_fixtures.CHANGE_ID + ".jsonl")
        lines = ledger.read_bytes().split(b"\n")
        ledger.write_bytes(b"\n".join(lines[1:]))
        report = checks.validate_bundle(self.bundle)
        self.assertIn(schema.CODE_TAMPER, _fixtures.blockers_codes(report))

    def test_row_10_unauthorized_exception(self):
        document = _fixtures.load("adversarial-unauthorized-exception.json")
        issues, derived = checks.head_history_issues(
            document["head_history"], change_id=_fixtures.CHANGE_ID, candidate_head=_fixtures.HEAD
        )
        self.assertIn(schema.CODE_AUTHORITY_ABSENT, _fixtures.codes(issues))
        self.assertTrue(derived["exception_required"])
        self.assertEqual(derived["used"], 3)

    def test_row_10_a_fourth_head_without_any_exception_is_a_limit_block(self):
        payload = dict(_fixtures.load("adversarial-unauthorized-exception.json")["head_history"]["payload"])
        for head in payload["heads"]:
            head["exception_ref"] = None
        envelope = _fixtures.envelope(payload, status="VERIFIED")
        issues, derived = checks.head_history_issues(
            envelope, change_id=_fixtures.CHANGE_ID, candidate_head=_fixtures.HEAD
        )
        self.assertIn(schema.CODE_BUDGET, _fixtures.codes(issues))
        self.assertTrue(derived["exception_required"])

    def test_row_12_overclaim_is_refused_and_never_displayed_green(self):
        document = _fixtures.load("adversarial-overclaim-bypass.json")
        issues = checks.assurance_issues(document["manifest"])
        self.assertEqual(_fixtures.codes(issues), [schema.CODE_CANONICAL])
        self.assertEqual(len(issues), 2)
        report = checks.validate_bundle(self.bundle)
        self.assertEqual(report["assurance"]["claim"], "AUDITABLE")
        self.assertEqual(report["assurance"]["mounted_coverage"], "UNKNOWN")
        self.assertEqual(report["assurance"]["enforced"], "BLOCKED")
        rendered = json.dumps(report)
        self.assertNotIn("ENFORCED", rendered)
        self.assertNotIn('"GREEN"', rendered)


class MergedCheckerRowsTest(unittest.TestCase):
    """Rows 9-12 that belong to contract terms are exercised through the merged
    checker's own synthetic bundles, read-only by path."""

    def _run(self, name: str):
        module = _fixtures.merged_fixtures()
        if module is None:
            self.skipTest("merged checker fixtures are absent at this head: A7 rebind required (UNRUN)")
        result, _paths = module.run_bundle(module.load_bundle(name))
        return result

    def test_row_11_non_affirmative_verdict(self):
        result = self._run("f-revise")
        self.assertFalse(result.readiness)
        self.assertIn("VERDICT_NOT_AFFIRMATIVE", [blocker.code for blocker in result.blockers])

    def test_row_11_non_affirmative_stage(self):
        for name, expected in (("d-revise", "STAGE_VERDICT_NOT_ACCEPTED"), ("e-fail", "STAGE_VERDICT_NOT_ACCEPTED")):
            with self.subTest(fixture=name):
                result = self._run(name)
                self.assertFalse(result.readiness)
                self.assertIn(expected, [blocker.code for blocker in result.blockers])

    def test_row_11_security_flag(self):
        result = self._run("secret-flag-true")
        self.assertFalse(result.readiness)
        self.assertIn("SECURITY_FLAG_SET", [blocker.code for blocker in result.blockers])

    def test_row_11_budget_without_exception(self):
        result = self._run("fourth-head-no-exception")
        self.assertFalse(result.readiness)
        self.assertIn("REVIEW_BUDGET_EXHAUSTED", [blocker.code for blocker in result.blockers])

    def test_row_11_unverified_auth(self):
        result = self._run("unverified-auth")
        self.assertFalse(result.readiness)
        self.assertIn("VERDICT_STALE_OR_UNVERIFIED", [blocker.code for blocker in result.blockers])

    def test_row_10_a_fixture_exception_is_fixture_mode_only(self):
        result = self._run("fourth-head-active-exception")
        self.assertEqual(result.assurance["mode"], "FIXTURE")
        self.assertEqual(result.assurance["claim"], "AUDITABLE")
        self.assertEqual(result.assurance["mounted_coverage"], "UNKNOWN")

    def test_row_9_store_tamper(self):
        result = self._run("store-manifest-tamper")
        self.assertFalse(result.readiness)
        self.assertIn("STATE_TAMPER_SUSPECTED", [blocker.code for blocker in result.blockers])


class UnrunHostRowsTest(unittest.TestCase):
    """Row 13 needs a real host; it is recorded, never simulated."""

    UNRUN = (
        {
            "row": 13,
            "probe": "denied tool call then retry",
            "missing_authority": "T5 mounted-coverage export + T9 host authority",
        },
        {
            "row": 13,
            "probe": "config/profile edit and restart re-read",
            "missing_authority": "T4 settings/identity + T9 host authority",
        },
        {
            "row": 13,
            "probe": "custom executor / ACP / terminal or remote route",
            "missing_authority": "T5 coverage export + T9 host authority",
        },
        {
            "row": 13,
            "probe": "host-side counter-store editability",
            "missing_authority": "T7 authority + T24 store custody",
        },
    )

    def test_host_rows_are_unrun_and_named(self):
        for item in self.UNRUN:
            with self.subTest(probe=item["probe"]):
                self.assertTrue(item["probe"])
                self.assertRegex(item["missing_authority"], "T[0-9]+")

    def test_no_host_assertion_exists_in_this_suite(self):
        source = pathlib.Path(__file__).read_text(encoding="utf-8")
        tokens = (
            "mounted_" + "coverage_verified",
            "host_" + "containment_proved",
            "ENFORCED_" + "HOST",
            "assertTrue(" + "result.readiness)",
        )
        for token in tokens:
            self.assertEqual(source.count(token), 0, "forbidden pass token present: %s" % token)
