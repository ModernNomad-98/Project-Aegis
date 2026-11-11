"""Gate tests: 26 fixtures, D1/D2/D3 negative vectors, determinism, exit codes.

Covers AC4-AC8, AC10, AC12: affirmative verdicts cannot be bypassed, the
exclusive review-head budget is enforced at 3/4 heads, the security flag has
no exception path, output is deterministic and the CLI exit codes are 0/1/2/3.
"""

from __future__ import annotations

import contextlib
import copy
import io
import json
import pathlib
import sys
import unittest
from unittest import mock

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import _fixtures  # noqa: E402
from tools.aegis_verdict_gate import __main__ as cli  # noqa: E402
from tools.aegis_verdict_gate import gate, records  # noqa: E402

HEAD = "a" * 40

CONTRACT_CODES = {
    "VERDICT_NOT_AFFIRMATIVE",
    "STAGE_VERDICT_NOT_ACCEPTED",
    "SECURITY_FLAG_SET",
    "VERDICT_STALE_OR_UNVERIFIED",
    "CANONICAL_FIELD_MISSING_OR_MISMATCH",
    "HEAD_MOVED_OR_BASE_INVALIDATED",
    "EVIDENCE_REUSE_INVALID",
    "AUTHORITY_ABSENT",
    "STATE_TAMPER_SUSPECTED",
    "OWNER_DECISION_BLOCKING",
    "POST_F_BLOCKER",
    "REQUIRED_INPUT_UNAVAILABLE",
    "OPEN_BLOCKING_FINDING",
    "MISSING_INDEPENDENT_APPROVAL",
    "MISSING_REQUIRED_REVIEW_OR_DISPOSITION",
    "REVIEW_BUDGET_EXHAUSTED",
}


def variant(mutator, supported=(_fixtures.FIXTURE_AUTH_METHOD,), source="valid-verdict"):
    bundle = copy.deepcopy(_fixtures.load_bundle(source))
    mutator(bundle)
    result, _ = _fixtures.run_bundle(bundle, supported_auth_methods=supported)
    return result, bundle


def heads_for(previous, candidate=HEAD):
    heads = [
        {"seq": index + 1, "head_sha": str(index + 1) * 40, "kind": "INITIAL"}
        for index in range(previous)
    ]
    heads.append({"seq": previous + 1, "head_sha": candidate, "kind": "INITIAL"})
    return heads


def ledger_for(heads):
    """The change-ledger mirror the A10 rule requires for a given export."""

    return [
        {
            "head_sha": head["head_sha"],
            "kind": head["kind"],
            "exception_ref": None,
            "counted_at": head.get("published_at", "2026-11-10T18:00:00Z"),
            "authority_ref": {
                "authority_kind": "REGISTER_ENTRY",
                "authority_ref_id": "APR-FIXTURE-C11A-0001",
                "holder_role": "programme-lead",
                "holder_identity_ref": None,
            },
        }
        for head in heads
        if head["head_sha"] != HEAD
    ]


def set_heads(bundle, heads):
    bundle["inputs"]["head_history"]["heads"] = heads
    bundle["inputs"]["revision_state"]["change_ledger"] = ledger_for(heads)


def rewrite_envelope(path, mutate):
    """Rewrite one input envelope after mutating its payload (hashes recomputed)."""

    document = json.loads(path.read_text(encoding="utf-8"))
    mutate(document["payload"])
    _fixtures._write_envelope(path, document["payload"], document["provenance"])


class FixtureBundleTest(unittest.TestCase):
    def test_exactly_26_named_bundles(self):
        names = _fixtures.fixture_names()
        self.assertEqual(len(names), 26)
        self.assertIn("valid-verdict", names)
        self.assertIn("canonical-field-missing", names)
        for name in names:
            bundle = _fixtures.load_bundle(name)
            self.assertEqual(bundle["case_id"], name)
            for key in ("case_id", "notes", "verdict", "inputs", "expected"):
                self.assertIn(key, bundle)
            for key in ("freeze", "settlement", "revision_state", "stage_records", "head_history"):
                self.assertIn(key, bundle["inputs"])
            self.assertEqual(sorted(bundle["expected"]), ["blocker_codes", "readiness"])

    def test_every_bundle_matches_its_expected_result(self):
        for name in _fixtures.fixture_names():
            bundle = _fixtures.load_bundle(name)
            result, _ = _fixtures.run_bundle(bundle)
            self.assertEqual(
                result.readiness,
                bundle["expected"]["readiness"],
                "%s readiness" % name,
            )
            self.assertEqual(
                sorted(result.reason_codes),
                sorted(bundle["expected"]["blocker_codes"]),
                "%s blocker codes: %s" % (name, [(blocker.code, blocker.detail) for blocker in result.blockers]),
            )

    def test_every_contract_blocker_code_is_exercised(self):
        covered = set()
        for name in _fixtures.fixture_names():
            covered.update(_fixtures.load_bundle(name)["expected"]["blocker_codes"])
        self.assertEqual(CONTRACT_CODES - covered, set())

    def test_output_schema_and_assurance(self):
        bundle = _fixtures.load_bundle("valid-verdict")
        result, _ = _fixtures.run_bundle(bundle)
        payload = result.as_dict()
        for key in (
            "schema_version",
            "bound_set_id",
            "bound_set_version",
            "readiness",
            "blockers",
            "reason_codes",
            "derived_counts",
            "revision_state_sha256",
            "store_digest",
            "inputs_sha256",
            "permitted_next_action",
            "assurance",
        ):
            self.assertIn(key, payload)
        self.assertEqual(payload["bound_set_id"], "aegis.verdict-bound/v2.1")
        self.assertEqual(
            payload["assurance"],
            {"claim": "AUDITABLE", "mounted_coverage": "UNKNOWN", "mode": "FIXTURE"},
        )
        self.assertEqual(payload["schema_version"], "aegis.verdict-gate-output/v1")
        self.assertTrue(payload["readiness"])
        self.assertEqual(payload["permitted_next_action"]["action"], "PROCEED_TO_STAGE_G_MERGE_AUTHORITY")
        self.assertEqual(result.reason_codes, [])


class AffirmativeVerdictVectorsTest(unittest.TestCase):
    """NV-D1-1..8 from the v2.1 errata."""

    def assert_blocked(self, result, code):
        self.assertFalse(result.readiness)
        self.assertIn(code, result.reason_codes)

    def test_nv_d1_1_f_revise(self):
        result, _ = _fixtures.run_bundle(_fixtures.load_bundle("f-revise"))
        self.assert_blocked(result, "VERDICT_NOT_AFFIRMATIVE")

    def test_nv_d1_2_f_blocked(self):
        result, _ = _fixtures.run_bundle(_fixtures.load_bundle("f-blocked"))
        self.assert_blocked(result, "VERDICT_NOT_AFFIRMATIVE")

    def test_nv_d1_3_f_value_missing(self):
        result, _ = _fixtures.run_bundle(_fixtures.load_bundle("f-missing-value"))
        self.assert_blocked(result, "CANONICAL_FIELD_MISSING_OR_MISMATCH")
        self.assert_blocked(result, "VERDICT_STALE_OR_UNVERIFIED")

    def test_nv_d1_4_d_revise(self):
        result, _ = _fixtures.run_bundle(_fixtures.load_bundle("d-revise"))
        self.assert_blocked(result, "STAGE_VERDICT_NOT_ACCEPTED")

    def test_nv_d1_5_e_fail(self):
        result, _ = _fixtures.run_bundle(_fixtures.load_bundle("e-fail"))
        self.assert_blocked(result, "STAGE_VERDICT_NOT_ACCEPTED")

    def test_nv_d1_6_b_revise(self):
        result, _ = _fixtures.run_bundle(_fixtures.load_bundle("b-revise"))
        self.assert_blocked(result, "STAGE_VERDICT_NOT_ACCEPTED")

    def test_nv_d1_7_duplicate_active_f(self):
        result, _ = _fixtures.run_bundle(_fixtures.load_bundle("duplicate-f-active"))
        self.assert_blocked(result, "VERDICT_NOT_AFFIRMATIVE")

    def test_nv_d1_8_positive_control(self):
        result, _ = _fixtures.run_bundle(_fixtures.load_bundle("valid-verdict"))
        self.assertTrue(result.readiness)
        self.assertEqual(result.blockers, [])

    def test_a_later_pass_cannot_erase_an_active_revise(self):
        def mutate(bundle):
            bundle["verdict"]["record"]["verdict_records"] = [
                {"record_id": "rec-f-0001", "head_sha": HEAD, "value": "REVISE", "active": True},
                {"record_id": "rec-f-0002", "head_sha": HEAD, "value": "PASS", "active": True},
            ]

        result, _ = variant(mutate)
        self.assert_blocked(result, "VERDICT_NOT_AFFIRMATIVE")


class ReviewerIndependenceVectorsTest(unittest.TestCase):
    """B13: VB-F06 requires PR author, implementer and declared commit authors."""

    def test_missing_pr_author_distinct_is_not_ready(self):
        def mutate(bundle):
            bundle["verdict"]["reviewer"]["identity_ref"] = "pr-author"
            bundle["verdict"]["reviewer"]["independence"]["distinct_from"] = ["implementer"]

        result, _ = variant(mutate)
        self.assertFalse(result.readiness)
        self.assertIn("MISSING_INDEPENDENT_APPROVAL", result.reason_codes)
        self.assertTrue(any("pr-author" in issue.detail for issue in result.blockers))

class ReviewBudgetVectorsTest(unittest.TestCase):
    """NV-D2-1..8 from the v2.1 errata: exclusive head count."""

    def test_nv_d2_1_initial_head(self):
        def mutate(bundle):
            bundle["inputs"]["head_history"]["heads"] = heads_for(0)
            bundle["verdict"]["review_heads"] = {"used": 0, "exception_id": None}

        result, _ = variant(mutate)
        self.assertTrue(result.readiness)
        self.assertEqual(result.derived_counts["review_heads_used"], 0)
        self.assertEqual(result.derived_counts["derived_ordinal"], 1)

    def test_nv_d2_2_second_head(self):
        def mutate(bundle):
            set_heads(bundle, heads_for(1))
            bundle["verdict"]["review_heads"] = {"used": 1, "exception_id": None}

        result, _ = variant(mutate)
        self.assertTrue(result.readiness)
        self.assertEqual(result.derived_counts["review_heads_used"], 1)

    def test_nv_d2_3_third_head(self):
        def mutate(bundle):
            set_heads(bundle, heads_for(2))
            bundle["verdict"]["review_heads"] = {"used": 2, "exception_id": None}

        result, _ = variant(mutate)
        self.assertTrue(result.readiness)
        self.assertEqual(result.derived_counts["review_heads_used"], 2)

    def test_nv_d2_4_fourth_head_without_exception(self):
        result, _ = _fixtures.run_bundle(_fixtures.load_bundle("fourth-head-no-exception"))
        self.assertFalse(result.readiness)
        self.assertEqual(result.reason_codes, ["REVIEW_BUDGET_EXHAUSTED"])
        self.assertEqual(result.blockers[0].classification, "LIMIT")

    def test_nv_d2_5_fourth_head_with_active_exception(self):
        result, _ = _fixtures.run_bundle(_fixtures.load_bundle("fourth-head-active-exception"))
        self.assertTrue(result.readiness)
        self.assertEqual(result.derived_counts["review_heads_used"], 3)

    def test_nv_d2_6_unnecessary_exception_is_invalid(self):
        def mutate(bundle):
            set_heads(bundle, heads_for(2))
            bundle["verdict"]["review_heads"] = {"used": 2, "exception_id": "EXC-FIXTURE-0001"}

        result, _ = variant(mutate)
        self.assertFalse(result.readiness)
        self.assertEqual(result.reason_codes, ["STATE_TAMPER_SUSPECTED"])

    def test_nv_d2_7_decreased_reported_count_is_tamper(self):
        def mutate(bundle):
            set_heads(bundle, heads_for(2))
            bundle["verdict"]["review_heads"] = {"used": 1, "exception_id": None}

        result, _ = variant(mutate)
        self.assertFalse(result.readiness)
        self.assertEqual(result.reason_codes, ["STATE_TAMPER_SUSPECTED"])

    def test_nv_d2_8_resync_head_counts(self):
        def mutate(bundle):
            heads = heads_for(2)
            heads[1]["kind"] = "RESYNC"
            set_heads(bundle, heads)
            bundle["verdict"]["review_heads"] = {"used": 2, "exception_id": None}

        result, _ = variant(mutate)
        self.assertTrue(result.readiness)
        self.assertEqual(result.derived_counts["review_heads_used"], 2)

    def test_rename_or_restart_never_resets_the_count(self):
        def mutate(bundle):
            heads = heads_for(3)
            heads[0]["kind"] = "RESYNC"
            set_heads(bundle, heads)
            bundle["verdict"]["review_heads"] = {"used": 0, "exception_id": None}

        result, _ = variant(mutate)
        self.assertFalse(result.readiness)
        self.assertIn("STATE_TAMPER_SUSPECTED", result.reason_codes)


class SecurityFlagVectorsTest(unittest.TestCase):
    """NV-D3-1..4 from the v2.1 errata: no exception path."""

    def test_nv_d3_1_true_fails(self):
        result, _ = _fixtures.run_bundle(_fixtures.load_bundle("secret-flag-true"))
        self.assertFalse(result.readiness)
        self.assertEqual(result.reason_codes, ["SECURITY_FLAG_SET"])

    def test_nv_d3_2_purported_exception_is_only_a_bypass(self):
        bundle = _fixtures.load_bundle("secret-flag-true")
        self.assertEqual(bundle["verdict"]["record"]["bypasses"][0]["bypass_id"], "BYP-FIXTURE-0001")
        result, _ = _fixtures.run_bundle(bundle)
        self.assertFalse(result.readiness)
        self.assertEqual(result.reason_codes, ["SECURITY_FLAG_SET"])
        self.assertEqual(result.blockers[0].classification, "MANDATORY")

    def test_nv_d3_3_all_else_affirmative_is_insufficient(self):
        def mutate(bundle):
            bundle["verdict"]["security"]["secret_read_or_logged"] = True
            bundle["verdict"]["verdict"]["value"] = "PASS"

        result, _ = variant(mutate)
        self.assertFalse(result.readiness)
        self.assertEqual(result.reason_codes, ["SECURITY_FLAG_SET"])

    def test_nv_d3_4_false_passes(self):
        result, _ = _fixtures.run_bundle(_fixtures.load_bundle("valid-verdict"))
        self.assertTrue(result.readiness)


class FailClosedTest(unittest.TestCase):
    def test_production_mode_has_no_path_to_readiness(self):
        bundle = _fixtures.load_bundle("valid-verdict")
        _, paths = _fixtures.run_bundle(bundle, keep=True)
        try:
            result = gate.evaluate(
                repo_root=paths["root"],
                verdict_path=paths["verdict"],
                freeze_path=paths["freeze"],
                settlement_path=paths["settlement"],
                head_history_path=paths["head_history"],
                stage_records_dir=paths["stage_records_dir"],
            )
            self.assertFalse(result.readiness)
            self.assertEqual(result.reason_codes, ["VERDICT_STALE_OR_UNVERIFIED"])
            self.assertTrue(any("T6" in note for note in result.not_verifiable))
        finally:
            _fixtures.cleanup(paths["root"])

    def test_unexpected_top_level_field_is_invalid(self):
        def mutate(bundle):
            bundle["verdict"]["surprise"] = 1

        result, _ = variant(mutate)
        self.assertEqual(result.reason_codes, ["CANONICAL_FIELD_MISSING_OR_MISMATCH"])

    def test_unexpected_nested_field_is_invalid(self):
        def mutate(bundle):
            bundle["verdict"]["reviewer"]["surprise"] = "x"

        result, _ = variant(mutate)
        self.assertEqual(result.reason_codes, ["CANONICAL_FIELD_MISSING_OR_MISMATCH"])

    def test_v2_or_lower_record_is_invalid_for_a_v2_1_gate(self):
        def mutate(bundle):
            bundle["verdict"]["bound_set_id"] = "aegis.verdict-bound/v2"
            bundle["verdict"]["bound_set_version"] = "2"

        result, _ = variant(mutate)
        self.assertFalse(result.readiness)
        self.assertEqual(result.reason_codes, ["CANONICAL_FIELD_MISSING_OR_MISMATCH"])

    def test_bound_hash_mismatch_is_invalid(self):
        def mutate(bundle):
            bundle["overrides"] = {"bound_fields_sha256": "0" * 64}

        result, _ = variant(mutate)
        self.assertEqual(result.reason_codes, ["CANONICAL_FIELD_MISSING_OR_MISMATCH"])

    def test_checks_run_in_order_and_stop_at_the_first_failure(self):
        def mutate(bundle):
            bundle["verdict"]["verdict"]["value"] = "REVISE"
            bundle["verdict"]["record"]["verdict_records"][0]["value"] = "REVISE"
            bundle["inputs"]["stage_records"][1]["verdict"] = "REVISE"
            bundle["verdict"]["security"]["secret_read_or_logged"] = True

        result, _ = variant(mutate)
        self.assertEqual(result.reason_codes, ["VERDICT_NOT_AFFIRMATIVE"])
        failed = [check for check in result.checks if check["status"] == "FAIL"]
        self.assertEqual(len(failed), 1)
        self.assertEqual(failed[0]["check"], "C3")

    def test_declared_head_must_match_the_candidate_head(self):
        bundle = _fixtures.load_bundle("valid-verdict")
        result, paths = _fixtures.run_bundle(bundle, keep=True)
        try:
            moved = gate.evaluate(
                repo_root=paths["root"],
                verdict_path=paths["verdict"],
                freeze_path=paths["freeze"],
                settlement_path=paths["settlement"],
                head_history_path=paths["head_history"],
                stage_records_dir=paths["stage_records_dir"],
                supported_auth_methods=(_fixtures.FIXTURE_AUTH_METHOD,),
                candidate_head="9" * 40,
                fixture_mode=True,
            )
            self.assertEqual(moved.reason_codes, ["HEAD_MOVED_OR_BASE_INVALIDATED"])
        finally:
            _fixtures.cleanup(paths["root"])


class FixtureModeGuardTest(unittest.TestCase):
    """B1: production mode has no path to readiness=true while T6 is undecided."""

    def test_gate_refuses_supported_methods_outside_fixture_mode(self):
        bundle = _fixtures.load_bundle("valid-verdict")
        self.assertTrue(_fixtures.run_bundle(bundle)[0].readiness)
        result, paths = _fixtures.run_bundle(bundle, keep=True)
        try:
            refused = gate.evaluate(
                repo_root=paths["root"],
                verdict_path=paths["verdict"],
                freeze_path=paths["freeze"],
                settlement_path=paths["settlement"],
                head_history_path=paths["head_history"],
                stage_records_dir=paths["stage_records_dir"],
                supported_auth_methods=(_fixtures.FIXTURE_AUTH_METHOD,),
            )
            self.assertFalse(refused.readiness)
            self.assertEqual(refused.reason_codes, ["VERDICT_STALE_OR_UNVERIFIED"])
            self.assertIn("fixture mode", refused.blockers[0].detail)
            self.assertEqual(refused.assurance["mode"], "PRODUCTION")
        finally:
            _fixtures.cleanup(paths["root"])

    def test_production_run_with_no_method_is_still_blocked(self):
        bundle = _fixtures.load_bundle("valid-verdict")
        result, paths = _fixtures.run_bundle(bundle, keep=True)
        try:
            blocked = gate.evaluate(
                repo_root=paths["root"],
                verdict_path=paths["verdict"],
                freeze_path=paths["freeze"],
                settlement_path=paths["settlement"],
                head_history_path=paths["head_history"],
                stage_records_dir=paths["stage_records_dir"],
            )
            self.assertFalse(blocked.readiness)
            self.assertEqual(blocked.reason_codes, ["VERDICT_STALE_OR_UNVERIFIED"])
            self.assertEqual(blocked.assurance["mode"], "PRODUCTION")
        finally:
            _fixtures.cleanup(paths["root"])

    def test_cli_refuses_a_supported_method_without_fixture_mode(self):
        bundle = _fixtures.load_bundle("valid-verdict")
        _, paths = _fixtures.run_bundle(bundle, keep=True)
        argv = [
            "check",
            "--repo-root",
            str(paths["root"]),
            "--verdict",
            str(paths["verdict"]),
            "--freeze",
            str(paths["freeze"]),
            "--settlement",
            str(paths["settlement"]),
            "--head-history",
            str(paths["head_history"]),
            "--stage-records-dir",
            str(paths["stage_records_dir"]),
            "--supported-auth-method",
            _fixtures.FIXTURE_AUTH_METHOD,
        ]
        stderr = io.StringIO()
        try:
            with contextlib.redirect_stderr(stderr):
                with self.assertRaises(SystemExit) as caught:
                    cli.main(argv)
            self.assertEqual(caught.exception.code, 2)
            self.assertIn("--fixture-mode", stderr.getvalue())
        finally:
            _fixtures.cleanup(paths["root"])


class AppendOnlyFailClosedTest(unittest.TestCase):
    """B2: an unresolvable git base is a required-input blocker, not a skip."""

    def test_unresolvable_git_base_blocks_readiness(self):
        bundle = _fixtures.load_bundle("valid-verdict")
        result, paths = _fixtures.run_bundle(bundle, keep=True)
        try:
            self.assertTrue(result.readiness)
            # A bad base ref is the documented way to make the base
            # unresolvable without touching the worktree.
            blocked = gate.evaluate(
                repo_root=paths["root"],
                verdict_path=paths["verdict"],
                freeze_path=paths["freeze"],
                settlement_path=paths["settlement"],
                head_history_path=paths["head_history"],
                stage_records_dir=paths["stage_records_dir"],
                supported_auth_methods=(_fixtures.FIXTURE_AUTH_METHOD,),
                fixture_mode=True,
                base_ref="refs/heads/does-not-exist",
            )
            self.assertFalse(blocked.readiness)
            self.assertEqual(blocked.reason_codes, ["REQUIRED_INPUT_UNAVAILABLE"])
            self.assertIn("no git base", blocked.blockers[0].detail)
            self.assertEqual(blocked.inputs_sha256["store"]["prefix_checks"]["__status__"], "GIT_BASE_UNRESOLVED")
        finally:
            _fixtures.cleanup(paths["root"])


class StageDeclarationsFailClosedTest(unittest.TestCase):
    """B7: --stage-records-dir is required and never silently skipped."""

    def evaluate(self, paths):
        return gate.evaluate(
            repo_root=paths["root"],
            verdict_path=paths["verdict"],
            freeze_path=paths["freeze"],
            settlement_path=paths["settlement"],
            head_history_path=paths["head_history"],
            stage_records_dir=paths["stage_records_dir"],
            supported_auth_methods=(_fixtures.FIXTURE_AUTH_METHOD,),
            fixture_mode=True,
        )

    def bundle_paths(self):
        bundle = _fixtures.load_bundle("valid-verdict")
        return _fixtures.run_bundle(bundle, keep=True)

    def test_absent_directory_is_required_input(self):
        import shutil

        _, paths = self.bundle_paths()
        try:
            shutil.rmtree(paths["stage_records_dir"])  # noqa: F821 - local import above
            result = self.evaluate(paths)
            self.assertFalse(result.readiness)
            self.assertEqual(result.reason_codes, ["REQUIRED_INPUT_UNAVAILABLE"])
            self.assertIn("--stage-records-dir", result.blockers[0].detail)
        finally:
            _fixtures.cleanup(paths["root"])

    def test_malformed_envelope_is_a_finding(self):
        _, paths = self.bundle_paths()
        try:
            (paths["stage_records_dir"] / "extra.json").write_text("{not json", encoding="utf-8")
            result = self.evaluate(paths)
            self.assertFalse(result.readiness)
            self.assertEqual(result.reason_codes, ["CANONICAL_FIELD_MISSING_OR_MISMATCH"])
            self.assertIn("extra.json", result.blockers[0].detail)
        finally:
            _fixtures.cleanup(paths["root"])

    def test_duplicate_stage_envelope_is_a_finding(self):
        _, paths = self.bundle_paths()
        try:
            (paths["stage_records_dir"] / "duplicate-b.json").write_text(
                (paths["stage_records_dir"] / "b.json").read_text(encoding="utf-8"), encoding="utf-8"
            )
            result = self.evaluate(paths)
            self.assertFalse(result.readiness)
            self.assertEqual(result.reason_codes, ["CANONICAL_FIELD_MISSING_OR_MISMATCH"])
            self.assertIn("more than one B", result.blockers[0].detail)
        finally:
            _fixtures.cleanup(paths["root"])

    def test_non_stage_envelope_is_a_finding(self):
        _, paths = self.bundle_paths()
        try:
            rewrite_envelope(paths["stage_records_dir"] / "b.json", lambda payload: payload.__setitem__("stage", "F"))
            result = self.evaluate(paths)
            self.assertFalse(result.readiness)
            self.assertEqual(result.reason_codes, ["CANONICAL_FIELD_MISSING_OR_MISMATCH"])
            self.assertIn("no B/D/E stage", result.blockers[0].detail)
        finally:
            _fixtures.cleanup(paths["root"])

    def test_missing_declaration_is_required_input(self):
        _, paths = self.bundle_paths()
        try:
            (paths["stage_records_dir"] / "d.json").unlink()
            result = self.evaluate(paths)
            self.assertFalse(result.readiness)
            self.assertEqual(result.reason_codes, ["REQUIRED_INPUT_UNAVAILABLE"])
            self.assertIn("missing required stage declaration", result.blockers[0].detail)
        finally:
            _fixtures.cleanup(paths["root"])


class HeadHistoryBindingTest(unittest.TestCase):
    """B8: the head-history export must be bound to the evaluated change/head."""

    def evaluate(self, paths):
        return gate.evaluate(
            repo_root=paths["root"],
            verdict_path=paths["verdict"],
            freeze_path=paths["freeze"],
            settlement_path=paths["settlement"],
            head_history_path=paths["head_history"],
            stage_records_dir=paths["stage_records_dir"],
            supported_auth_methods=(_fixtures.FIXTURE_AUTH_METHOD,),
            fixture_mode=True,
        )

    def bundle_paths(self):
        bundle = _fixtures.load_bundle("valid-verdict")
        return _fixtures.run_bundle(bundle, keep=True)

    def test_foreign_change_export_is_not_authoritative(self):
        _, paths = self.bundle_paths()
        try:
            rewrite_envelope(paths["head_history"], lambda payload: payload.__setitem__("change_id", 43))
            result = self.evaluate(paths)
            self.assertFalse(result.readiness)
            self.assertEqual(result.reason_codes, ["REQUIRED_INPUT_UNAVAILABLE"])
            self.assertIn("not the evaluated change", result.blockers[0].detail)
        finally:
            _fixtures.cleanup(paths["root"])

    def test_export_for_an_earlier_head_is_not_authoritative(self):
        _, paths = self.bundle_paths()
        try:
            rewrite_envelope(
                paths["head_history"], lambda payload: payload.__setitem__("candidate_head", "9" * 40)
            )
            result = self.evaluate(paths)
            self.assertFalse(result.readiness)
            self.assertEqual(result.reason_codes, ["REQUIRED_INPUT_UNAVAILABLE"])
            self.assertIn("not the evaluated head", result.blockers[0].detail)
        finally:
            _fixtures.cleanup(paths["root"])

    def test_export_without_change_identity_is_not_authoritative(self):
        _, paths = self.bundle_paths()
        try:
            rewrite_envelope(paths["head_history"], lambda payload: payload.pop("change_id", None))
            result = self.evaluate(paths)
            self.assertFalse(result.readiness)
            self.assertEqual(result.reason_codes, ["REQUIRED_INPUT_UNAVAILABLE"])
            self.assertIn("declares no change_id", result.blockers[0].detail)
        finally:
            _fixtures.cleanup(paths["root"])


class OwnerLineAndExceptionResolutionTest(unittest.TestCase):
    """B5: the G group and the budget exception resolve in the register."""

    def test_revoked_owner_line_entry_is_authority_absent(self):
        def mutate(bundle):
            text = bundle["inputs"]["revision_state"]["register_text"]
            bundle["inputs"]["revision_state"]["register_text"] = text.replace(
                "| APR-FIXTURE-C11A-0001 | ACTIVE |", "| APR-FIXTURE-C11A-0001 | REVOKED |"
            )

        result, _ = variant(mutate)
        self.assertFalse(result.readiness)
        self.assertEqual(result.reason_codes, ["AUTHORITY_ABSENT"])
        self.assertIn("not ACTIVE", result.blockers[0].detail)

    def test_absent_owner_line_entry_is_authority_absent(self):
        def mutate(bundle):
            text = bundle["inputs"]["revision_state"]["register_text"]
            bundle["inputs"]["revision_state"]["register_text"] = (
                "\n".join(line for line in text.splitlines() if "APR-FIXTURE-C11A-0001" not in line) + "\n"
            )

        result, _ = variant(mutate)
        self.assertFalse(result.readiness)
        self.assertEqual(result.reason_codes, ["AUTHORITY_ABSENT"])

    def test_register_entry_without_a_gate_scope_is_authority_absent(self):
        def mutate(bundle):
            text = bundle["inputs"]["revision_state"]["register_text"]
            bundle["inputs"]["revision_state"]["register_text"] = text.replace(
                "| APR-FIXTURE-C11A-0001 | ACTIVE | repo=example-org/example-repo; change_id=42; "
                "head_sha=" + "a" * 40 + "; merge_target_ref=refs/heads/main |",
                "| APR-FIXTURE-C11A-0001 | ACTIVE | fixture repo/change/head only |",
            )

        result, _ = variant(mutate)
        self.assertFalse(result.readiness)
        self.assertEqual(result.reason_codes, ["AUTHORITY_ABSENT"])
        self.assertIn("no machine-checkable gate scope", result.blockers[0].detail)

    def test_forged_covering_scope_is_tamper(self):
        def mutate(bundle):
            bundle["verdict"]["record"]["owner_line_resolution"]["scope"]["head_sha"] = "f" * 40

        result, _ = variant(mutate)
        self.assertFalse(result.readiness)
        self.assertEqual(result.reason_codes, ["STATE_TAMPER_SUSPECTED"])
        self.assertIn("register says", result.blockers[0].detail)

    def test_forged_effective_status_is_tamper(self):
        def mutate(bundle):
            bundle["verdict"]["record"]["owner_line_resolution"]["effective_status"] = "REVOKED"

        result, _ = variant(mutate)
        self.assertFalse(result.readiness)
        self.assertEqual(result.reason_codes, ["STATE_TAMPER_SUSPECTED"])

    def test_exception_absent_from_the_register_exhausts_the_budget(self):
        def mutate(bundle):
            text = bundle["inputs"]["revision_state"]["register_text"]
            bundle["inputs"]["revision_state"]["register_text"] = (
                "\n".join(line for line in text.splitlines() if "EXC-FIXTURE-0001" not in line) + "\n"
            )

        result, _ = variant(mutate, source="fourth-head-active-exception")
        self.assertFalse(result.readiness)
        self.assertEqual(result.reason_codes, ["REVIEW_BUDGET_EXHAUSTED"])
        self.assertEqual(result.blockers[0].classification, "LIMIT")

    def test_revoked_exception_entry_exhausts_the_budget(self):
        def mutate(bundle):
            text = bundle["inputs"]["revision_state"]["register_text"]
            bundle["inputs"]["revision_state"]["register_text"] = text.replace(
                "| EXC-FIXTURE-0001 | ACTIVE |", "| EXC-FIXTURE-0001 | REVOKED |"
            )

        result, _ = variant(mutate, source="fourth-head-active-exception")
        self.assertFalse(result.readiness)
        self.assertEqual(result.reason_codes, ["REVIEW_BUDGET_EXHAUSTED"])

    def test_forged_exception_scope_is_tamper(self):
        def mutate(bundle):
            bundle["verdict"]["record"]["review_head_exception"]["scope"]["head_sha"] = "f" * 40

        result, _ = variant(mutate, source="fourth-head-active-exception")
        self.assertFalse(result.readiness)
        self.assertEqual(result.reason_codes, ["STATE_TAMPER_SUSPECTED"])


class BlockerClassTotalsTest(unittest.TestCase):
    """D1: 19 codes = 15 MANDATORY + 1 LIMIT + 3 WAIT (not 16 MANDATORY)."""

    def test_totals(self):
        counts = {}
        for klass in gate.BLOCKER_CLASSES.values():
            counts[klass] = counts.get(klass, 0) + 1
        self.assertEqual(counts, {"MANDATORY": 15, "LIMIT": 1, "WAIT": 3})
        self.assertEqual(len(gate.BLOCKER_CLASSES), 19)

    def test_every_code_has_a_permitted_action(self):
        self.assertEqual(set(gate.PERMITTED_ACTION), set(gate.BLOCKER_CLASSES))


class StaticHygieneTest(unittest.TestCase):
    """AC10: standard library only, no network, no shell, read-only git only."""

    MODULES = (
        "__init__.py",
        "__main__.py",
        "catalogue.py",
        "canonical.py",
        "records.py",
        "inputs.py",
        "gate.py",
    )
    STDLIB = {
        "__future__",
        "argparse",
        "dataclasses",
        "hashlib",
        "json",
        "math",
        "pathlib",
        "re",
        "subprocess",
        "sys",
        "traceback",
        "typing",
    }
    BANNED = (
        "import socket",
        "import urllib",
        "import requests",
        "import httpx",
        "import http.client",
        "os.system",
        "shell=True",
        "urlopen",
        "popen",
    )

    def test_imports_are_stdlib_or_local(self):
        import ast

        tool_dir = pathlib.Path(__file__).resolve().parents[1]
        for name in self.MODULES:
            source = (tool_dir / name).read_text(encoding="utf-8")
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        top = alias.name.split(".")[0]
                        self.assertIn(top, self.STDLIB, "%s imports %s" % (name, alias.name))
                elif isinstance(node, ast.ImportFrom):
                    if node.level:
                        continue
                    top = (node.module or "").split(".")[0]
                    self.assertIn(top, self.STDLIB, "%s imports %s" % (name, node.module))

    def test_no_network_or_shell_tokens(self):
        tool_dir = pathlib.Path(__file__).resolve().parents[1]
        for name in self.MODULES:
            source = (tool_dir / name).read_text(encoding="utf-8")
            for token in self.BANNED:
                self.assertNotIn(token, source, "%s contains %r" % (name, token))

    def test_subprocess_is_confined_to_read_only_git_plumbing(self):
        tool_dir = pathlib.Path(__file__).resolve().parents[1]
        for name in self.MODULES:
            source = (tool_dir / name).read_text(encoding="utf-8")
            if name != "records.py":
                self.assertNotIn("subprocess", source, "%s must not spawn processes" % name)
        self.assertEqual(
            records.ALLOWED_GIT_SUBCOMMANDS, ("rev-parse", "cat-file", "log", "merge-base")
        )

    def test_readme_states_the_assurance_boundary(self):
        readme = (pathlib.Path(__file__).resolve().parents[1] / "README.md").read_text(encoding="utf-8")
        self.assertIn("AUDITABLE TOOLING, NOT ENFORCEMENT", readme)
        self.assertIn("098ad54886568bbc7e9103839d5ceda9a573d01f7d234d58a8747913e331bd5d", readme)
        self.assertIn("T6", readme)


class DeterminismTest(unittest.TestCase):
    def test_same_inputs_produce_identical_json(self):
        bundle = _fixtures.load_bundle("fourth-head-active-exception")
        result, paths = _fixtures.run_bundle(bundle, keep=True)
        try:
            def evaluate():
                return gate.evaluate(
                    repo_root=paths["root"],
                    verdict_path=paths["verdict"],
                    freeze_path=paths["freeze"],
                    settlement_path=paths["settlement"],
                    head_history_path=paths["head_history"],
                    stage_records_dir=paths["stage_records_dir"],
                    supported_auth_methods=(_fixtures.FIXTURE_AUTH_METHOD,),
                    fixture_mode=True,
                )

            first = json.dumps(evaluate().as_dict(), sort_keys=True)
            second = json.dumps(evaluate().as_dict(), sort_keys=True)
            self.assertEqual(first, second)
            self.assertNotIn("generated_at", first)
            self.assertNotIn(str(paths["root"]), first)
        finally:
            _fixtures.cleanup(paths["root"])

    def test_store_digest_is_reported_and_stable(self):
        bundle = _fixtures.load_bundle("valid-verdict")
        first, paths = _fixtures.run_bundle(bundle, keep=True)
        try:
            second = gate.evaluate(
                repo_root=paths["root"],
                verdict_path=paths["verdict"],
                freeze_path=paths["freeze"],
                settlement_path=paths["settlement"],
                head_history_path=paths["head_history"],
                stage_records_dir=paths["stage_records_dir"],
                supported_auth_methods=(_fixtures.FIXTURE_AUTH_METHOD,),
                fixture_mode=True,
            )
            self.assertEqual(first.store_digest, second.store_digest)
            self.assertRegex(first.store_digest, "^[0-9a-f]{64}$")
            self.assertRegex(first.revision_state_sha256, "^[0-9a-f]{64}$")
            self.assertIn("verdict", first.inputs_sha256)
            self.assertIn("store", first.inputs_sha256)
        finally:
            _fixtures.cleanup(paths["root"])


class CliExitCodeTest(unittest.TestCase):
    def run_cli(self, argv):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = cli.main(argv)
        return code, stdout.getvalue(), stderr.getvalue()

    def arguments(self, paths, *extra):
        return [
            "check",
            "--repo-root",
            str(paths["root"]),
            "--verdict",
            str(paths["verdict"]),
            "--freeze",
            str(paths["freeze"]),
            "--settlement",
            str(paths["settlement"]),
            "--head-history",
            str(paths["head_history"]),
            "--stage-records-dir",
            str(paths["stage_records_dir"]),
            "--fixture-mode",
        ] + list(extra)

    def test_self_test_exit_zero(self):
        code, stdout, _ = self.run_cli(["--self-test"])
        self.assertEqual(code, 0)
        self.assertIn("098ad54886568bbc7e9103839d5ceda9a573d01f7d234d58a8747913e331bd5d", stdout)

    def test_exit_zero_when_ready(self):
        bundle = _fixtures.load_bundle("valid-verdict")
        result, paths = _fixtures.run_bundle(bundle, keep=True)
        try:
            code, stdout, _ = self.run_cli(
                self.arguments(paths, "--supported-auth-method", _fixtures.FIXTURE_AUTH_METHOD, "--json")
            )
            self.assertEqual(code, 0)
            self.assertTrue(json.loads(stdout)["readiness"])
        finally:
            _fixtures.cleanup(paths["root"])

    def test_exit_one_when_blocked(self):
        bundle = _fixtures.load_bundle("f-revise")
        result, paths = _fixtures.run_bundle(bundle, keep=True)
        try:
            code, stdout, _ = self.run_cli(
                self.arguments(paths, "--supported-auth-method", _fixtures.FIXTURE_AUTH_METHOD, "--json")
            )
            self.assertEqual(code, 1)
            payload = json.loads(stdout)
            self.assertFalse(payload["readiness"])
            self.assertEqual(payload["reason_codes"], ["VERDICT_NOT_AFFIRMATIVE"])
        finally:
            _fixtures.cleanup(paths["root"])

    def test_exit_two_on_unparseable_input(self):
        bundle = _fixtures.load_bundle("valid-verdict")
        result, paths = _fixtures.run_bundle(bundle, keep=True)
        try:
            paths["verdict"].write_text("{not json", encoding="utf-8")
            code, _, stderr = self.run_cli(
                self.arguments(paths, "--supported-auth-method", _fixtures.FIXTURE_AUTH_METHOD)
            )
            self.assertEqual(code, 2)
            self.assertIn("invalid input", stderr)
        finally:
            _fixtures.cleanup(paths["root"])

    def test_exit_three_on_internal_error(self):
        bundle = _fixtures.load_bundle("valid-verdict")
        result, paths = _fixtures.run_bundle(bundle, keep=True)
        try:
            with mock.patch.object(gate, "evaluate", side_effect=RuntimeError("boom")):
                code, _, stderr = self.run_cli(self.arguments(paths))
            self.assertEqual(code, 3)
            self.assertIn("internal error", stderr)
        finally:
            _fixtures.cleanup(paths["root"])


if __name__ == "__main__":
    unittest.main()
