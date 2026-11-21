"""Parity between the validator's reachability gate and this tool.

The required `validate-skills` job must never execute `tools/` code, so the gate
carries a behaviour copy of measure_routed.py's scan instead of importing it.
This test is the drift detector for that copy. It loads the protected validator
BY PATH with importlib (no sys.path change, the same idiom
scripts/tests/test_validator.py uses for the hyphenated filename) and compares
the two on the real tree.

Run:
    python -P -m unittest discover -s tools/skill_reachability/tests -p 'test_*.py' -v
"""
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate-skills.py"
TOOL_PATH = REPO_ROOT / "tools" / "skill_reachability" / "measure_routed.py"
ALLOW_LIST_PATH = REPO_ROOT / "tools" / "skill_reachability" / "allow-list.json"
UNROUTED_ERROR = re.compile(
    r"^reachability: (\S+) is not routed from a front door and is not "
    r"on the allow-list \(tier: (handoff|none)\);")

_PATH_BEFORE = list(sys.path)
_spec = importlib.util.spec_from_file_location("aegis_validator", VALIDATOR_PATH)
if _spec is None or _spec.loader is None:  # pragma: no cover - broken checkout
    raise SystemExit("cannot load " + str(VALIDATOR_PATH))
validator = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validator)
_PATH_AFTER = list(sys.path)


def measure():
    """Run the tool with --json OUT (outside the repo) and return the payload."""
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "measure.json"
        proc = subprocess.run(
            [sys.executable, "-P", str(TOOL_PATH), str(REPO_ROOT),
             "--json", str(out)],
            capture_output=True, text=True)
        if proc.returncode != 0:
            raise AssertionError("measure_routed failed: %s\n%s"
                                 % (proc.stdout, proc.stderr))
        return json.loads(out.read_text(encoding="utf-8"))


def allow_list_names():
    payload = json.loads(ALLOW_LIST_PATH.read_text(encoding="utf-8"))
    return {row["name"] for row in payload["skills"]}


class ValidatorToolParityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.measured = measure()
        cls.tier = validator._reachability_tier_map(REPO_ROOT)

    def test_loader_leaves_sys_path_alone(self):
        # scripts/ must not enter sys.path: -P import isolation exists to keep
        # the gate from resolving unprotected modules.
        self.assertEqual(_PATH_AFTER, _PATH_BEFORE)

    def test_tier_map_matches_the_tool_on_the_real_tree(self):
        self.assertIsNotNone(self.tier)
        self.assertEqual(self.tier, self.measured["tier"])

    def test_verdict_matches_the_tool_on_the_real_tree(self):
        check = subprocess.run(
            [sys.executable, "-P", str(TOOL_PATH), str(REPO_ROOT),
             "--check-allow-list"], capture_output=True, text=True)
        if check.returncode != 0:
            # schema, expected_count and triage_row are the tool's job; the
            # gate only fails closed on the name set, dead rows and routed rows.
            self.skipTest("allow-list is not structurally valid; tool owns the "
                          "rest: " + check.stdout.strip())
        rep = validator.Report()
        validator.check_skill_reachability(rep, root=REPO_ROOT)
        listed = allow_list_names()
        expected = sorted(name for name, tier in self.measured["tier"].items()
                          if tier in ("handoff", "none") and name not in listed)
        got = sorted(match.group(1) for match in
                     (UNROUTED_ERROR.match(error) for error in rep.errors)
                     if match)
        self.assertEqual(got, expected)
        self.assertEqual(len(rep.errors), len(expected), rep.errors)
        self.assertEqual(rep.warnings, [])


if __name__ == "__main__":
    unittest.main()
