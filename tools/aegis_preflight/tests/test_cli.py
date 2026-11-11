"""End-to-end CLI tests for the C2.2 preflight fixture matrix."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import _fixtures as fixtures  # noqa: E402
from tools.aegis_preflight import checks  # noqa: E402


def run_cli(arguments):
    return subprocess.run(
        [sys.executable, "-m", "tools.aegis_preflight"] + arguments,
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


class PreflightCliTests(unittest.TestCase):
    def test_fixture_matrix(self) -> None:
        for name in fixtures.case_names():
            case = fixtures.load_case(name)
            with self.subTest(case=name), tempfile.TemporaryDirectory() as temporary:
                built = fixtures.build_case(case, temporary)
                completed = run_cli(
                    [
                        "check",
                        "--bundle",
                        str(built["bundle"]),
                        "--repo-root",
                        str(built["root"]),
                        "--fixture-mode",
                        "--supported-auth-method",
                        "provider-event-author",
                        "--json",
                    ]
                )
                self.assertIn(completed.returncode, (0, 1), completed.stderr)
                output = json.loads(completed.stdout)
                self.assertEqual(
                    completed.returncode,
                    case["expected"]["exit_code"],
                    "%s: %s" % (name, json.dumps({c["check_id"]: c["status"] for c in output["checks"]})),
                )
                statuses = {check["check_id"]: check["status"] for check in output["checks"]}
                for check_id, expected in case["expected"]["statuses"].items():
                    self.assertEqual(statuses.get(check_id), expected, "%s: %s" % (name, statuses))
                self.assertEqual(output["exit_code"], case["expected"]["exit_code"])
                if name == "clean-bundle":
                    self.assertEqual(set(statuses.values()), {"PASS"})
                    self.assertEqual(output["totals"], {"pass": 10, "fail": 0, "blocked": 0, "unrun": 0})

    def test_determinism_same_bundle(self) -> None:
        case = fixtures.load_case("clean-bundle")
        with tempfile.TemporaryDirectory() as temporary:
            built = fixtures.build_case(case, temporary)
            arguments = [
                "check",
                "--bundle",
                str(built["bundle"]),
                "--repo-root",
                str(built["root"]),
                "--fixture-mode",
                "--supported-auth-method",
                "provider-event-author",
                "--json",
            ]
            first = run_cli(arguments)
            second = run_cli(arguments)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)

    def test_production_mode_never_reports_ready(self) -> None:
        case = fixtures.load_case("clean-bundle")
        with tempfile.TemporaryDirectory() as temporary:
            built = fixtures.build_case(case, temporary)
            completed = run_cli(
                ["check", "--bundle", str(built["bundle"]), "--repo-root", str(built["root"]), "--json"]
            )
        self.assertEqual(completed.returncode, 1)
        output = json.loads(completed.stdout)
        statuses = {check["check_id"]: check["status"] for check in output["checks"]}
        self.assertEqual(statuses["PF-07"], "BLOCKED")
        self.assertEqual(output["assurance"]["mode"], "PRODUCTION")
        self.assertNotIn("readiness", output)

    def test_malformed_bundle_exit_2(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "bundle.json"
            path.write_text("{not json", encoding="utf-8")
            completed = run_cli(["check", "--bundle", str(path), "--json"])
        self.assertEqual(completed.returncode, 2)
        self.assertIn("invalid input", completed.stderr)

    def test_missing_bundle_exit_2(self) -> None:
        completed = run_cli(["check", "--bundle", "does-not-exist.json", "--json"])
        self.assertEqual(completed.returncode, 2)

    def test_missing_bundle_argument_exit_2(self) -> None:
        completed = run_cli(["check", "--json"])
        self.assertEqual(completed.returncode, 2)

    def test_self_test(self) -> None:
        completed = run_cli(["--self-test"])
        self.assertEqual(completed.returncode, 0, completed.stderr)
        report = json.loads(completed.stdout)
        self.assertTrue(report["ok"])
        self.assertEqual(len(report["check_ids"]), 10)

    def test_production_sources_have_no_network_or_write_path(self) -> None:
        self.assertEqual(checks.scan_source(Path(__file__).resolve().parents[1]), [])


if __name__ == "__main__":
    unittest.main()
