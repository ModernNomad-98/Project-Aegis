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
        self.assertEqual(payload["assurance"], {"claim": "AUDITABLE", "mounted_coverage": "UNKNOWN"})
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
            bundle["inputs"]["head_history"]["heads"] = heads_for(1)
            bundle["verdict"]["review_heads"] = {"used": 1, "exception_id": None}

        result, _ = variant(mutate)
        self.assertTrue(result.readiness)
        self.assertEqual(result.derived_counts["review_heads_used"], 1)

    def test_nv_d2_3_third_head(self):
        def mutate(bundle):
            bundle["inputs"]["head_history"]["heads"] = heads_for(2)
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
            bundle["inputs"]["head_history"]["heads"] = heads_for(2)
            bundle["verdict"]["review_heads"] = {"used": 2, "exception_id": "EXC-FIXTURE-0001"}

        result, _ = variant(mutate)
        self.assertFalse(result.readiness)
        self.assertEqual(result.reason_codes, ["STATE_TAMPER_SUSPECTED"])

    def test_nv_d2_7_decreased_reported_count_is_tamper(self):
        def mutate(bundle):
            bundle["inputs"]["head_history"]["heads"] = heads_for(2)
            bundle["verdict"]["review_heads"] = {"used": 1, "exception_id": None}

        result, _ = variant(mutate)
        self.assertFalse(result.readiness)
        self.assertEqual(result.reason_codes, ["STATE_TAMPER_SUSPECTED"])

    def test_nv_d2_8_resync_head_counts(self):
        def mutate(bundle):
            heads = heads_for(2)
            heads[1]["kind"] = "RESYNC"
            bundle["inputs"]["head_history"]["heads"] = heads
            bundle["verdict"]["review_heads"] = {"used": 2, "exception_id": None}

        result, _ = variant(mutate)
        self.assertTrue(result.readiness)
        self.assertEqual(result.derived_counts["review_heads_used"], 2)

    def test_rename_or_restart_never_resets_the_count(self):
        def mutate(bundle):
            heads = heads_for(3)
            heads[0]["kind"] = "RESYNC"
            bundle["inputs"]["head_history"]["heads"] = heads
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
        result, _ = _fixtures.run_bundle(bundle, supported_auth_methods=())
        self.assertFalse(result.readiness)
        self.assertEqual(result.reason_codes, ["VERDICT_STALE_OR_UNVERIFIED"])
        self.assertTrue(any("T6" in note for note in result.not_verifiable))

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
            )
            self.assertEqual(moved.reason_codes, ["HEAD_MOVED_OR_BASE_INVALIDATED"])
        finally:
            _fixtures.cleanup(paths["root"])


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
