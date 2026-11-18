"""Local-only fixture tests for tools/skill_reachability/measure_routed.py.

Fixtures are built in temporary directories and removed; no fixture file is committed.
Run:
    python -P -m unittest discover -s tools/skill_reachability/tests -p 'test_*.py' -v
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPT = REPO_ROOT / "tools" / "skill_reachability" / "measure_routed.py"
REAL_ALLOW_LIST = REPO_ROOT / "tools" / "skill_reachability" / "allow-list.json"

SKILL_TEMPLATE = "---\nname: {name}\ndescription: fixture skill {name}\n---\n\n# {name}\n"


def write_skill(repo, name, extra=None):
    d = repo / ".claude" / "skills" / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(SKILL_TEMPLATE.format(name=name), encoding="utf-8")
    if extra:
        refs = d / "references"
        refs.mkdir(parents=True, exist_ok=True)
        (refs / "extra.md").write_text(extra, encoding="utf-8")


def add_landmarks(repo):
    """Add the source-library landmarks the tool role-checks (fixture, not the real files)."""
    (repo / "docs").mkdir(parents=True, exist_ok=True)
    (repo / "docs" / "skills-catalog.md").write_text("# fixture catalog", encoding="utf-8")
    (repo / "scripts").mkdir(parents=True, exist_ok=True)
    (repo / "scripts" / "validate-skills.py").write_text("# fixture validator", encoding="utf-8")
    audits = repo / "artifacts" / "audits"
    audits.mkdir(parents=True, exist_ok=True)
    (audits / "skill-contract-audit-baseline.json").write_text("{}", encoding="utf-8")


def make_repo(tmp, door_lines, guide_files=()):
    repo = Path(tmp)
    write_skill(repo, "project-orchestrator")
    readme = ["# Project Aegis", "", "### Start here: pick your path", ""] + list(door_lines) + ["", "## Later", "", "Text."]
    (repo / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")
    paths = repo / "docs" / "paths"
    paths.mkdir(parents=True, exist_ok=True)
    for rel in guide_files:
        (repo / rel).write_text("# guide\n", encoding="utf-8")
    add_landmarks(repo)
    return repo


def run_tool(repo, *args):
    cmd = [sys.executable, "-P", str(SCRIPT), str(repo)] + list(args)
    return subprocess.run(cmd, capture_output=True, text=True)


def measure(repo):
    with tempfile.TemporaryDirectory() as outdir:
        out = Path(outdir) / "measure.json"
        res = run_tool(repo, "--json", str(out))
        if res.returncode != 0:
            raise AssertionError("measure failed: %s %s" % (res.stdout, res.stderr))
        return json.loads(out.read_text(encoding="utf-8"))


class MeasureFixtureTests(unittest.TestCase):
    def test_conductor_is_not_invented(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = make_repo(tmp, ['- **"one path"** -> [guide](docs/paths/guide-one.md)'], ["docs/paths/guide-one.md"])
            write_skill(repo, "alpha-orchestrator")
            data = measure(repo)
            self.assertEqual(data["tier"].get("alpha-orchestrator"), "none")
            self.assertEqual(data["conductors"], [])

    def test_orphan_guide_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = make_repo(tmp, ['- **"one path"** -> [guide](docs/paths/guide-one.md)'], ["docs/paths/guide-one.md", "docs/paths/orphan.md"])
            data = measure(repo)
            self.assertIn("docs/paths/orphan.md", data["guides_not_linked_from_a_door"])

    def test_do_not_use_line_is_excluded(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = make_repo(tmp, ["- **x** names beta-skill but this line says do not use it"])
            write_skill(repo, "beta-skill")
            data = measure(repo)
            self.assertEqual(data["tier"].get("beta-skill"), "none")

    def test_reference_mention_is_not_a_route(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = make_repo(tmp, ['- **"one path"** names alpha-skill -> [guide](docs/paths/guide-one.md)'], ["docs/paths/guide-one.md"])
            write_skill(repo, "alpha-skill", extra="This reference mentions gamma-skill only.\n")
            write_skill(repo, "gamma-skill")
            data = measure(repo)
            self.assertEqual(data["tier"].get("gamma-skill"), "none")

    def test_new_unrouted_skill_require_exits_one(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = make_repo(tmp, [], [])
            write_skill(repo, "delta-skill")
            res = run_tool(repo, "--require", "delta-skill")
            self.assertEqual(res.returncode, 1)
            self.assertIn("--require: NOT routed: delta-skill", res.stdout)


class AllowListTests(unittest.TestCase):
    def _real_repo_run(self, *extra):
        return run_tool(REPO_ROOT, "--check-allow-list", *extra)

    def _copy_allow_list(self, tmp):
        out = Path(tmp) / "allow-list.json"
        out.write_text(REAL_ALLOW_LIST.read_text(encoding="utf-8"), encoding="utf-8")
        return out

    def test_real_allow_list_passes(self):
        res = self._real_repo_run()
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        self.assertIn("allow-list: OK", res.stdout)

    def _mutated(self, mutate):
        with tempfile.TemporaryDirectory() as tmp:
            allow_path = self._copy_allow_list(tmp)
            data = json.loads(allow_path.read_text(encoding="utf-8"))
            mutate(data)
            allow_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            return self._real_repo_run("--allow-list", str(allow_path))

    def test_routed_name_fails(self):
        def mutate(data):
            data["skills"][0]["name"] = "plan-of-record-author"
        res = self._mutated(mutate)
        self.assertEqual(res.returncode, 1)
        self.assertIn("plan-of-record-author is door", res.stdout)

    def test_duplicate_name_fails(self):
        def mutate(data):
            data["skills"][1]["name"] = data["skills"][0]["name"]
        res = self._mutated(mutate)
        self.assertEqual(res.returncode, 1)
        self.assertIn("duplicate name", res.stdout)

    def test_blank_reason_fails(self):
        def mutate(data):
            data["skills"][0]["reason"] = "   "
        res = self._mutated(mutate)
        self.assertEqual(res.returncode, 1)
        self.assertIn("blank reason", res.stdout)

    def test_missing_name_fails(self):
        def mutate(data):
            data["skills"][0]["name"] = "not-a-real-skill"
        res = self._mutated(mutate)
        self.assertEqual(res.returncode, 1)
        self.assertIn("not-a-real-skill", res.stdout)


    def test_substituted_name_fails(self):
        def mutate(data):
            data["skills"][0]["name"] = "membership-invitation-designer"
            data["skills"][0]["triage_row"] = 999
        res = self._mutated(mutate)
        self.assertEqual(res.returncode, 1)
        self.assertIn("membership-invitation-designer", res.stdout)
        self.assertIn("missing expected name", res.stdout)

    def test_wrong_triage_row_fails(self):
        def mutate(data):
            data["skills"][0]["triage_row"] = 999
        res = self._mutated(mutate)
        self.assertEqual(res.returncode, 1)
        self.assertIn("triage_row is 999, expected 9", res.stdout)


class OperandTests(unittest.TestCase):
    def test_missing_option_operand_is_usage_error(self):
        for flag in ("--json", "--require", "--allow-list"):
            res = run_tool(REPO_ROOT, flag)
            self.assertEqual(res.returncode, 2, flag + " -> " + res.stdout + res.stderr)
            self.assertIn("requires a value", res.stdout)
            self.assertNotIn("Traceback", res.stdout + res.stderr)


class RoleCheckTests(unittest.TestCase):
    def test_consumer_repository_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "foo-skill")
            (repo / "README.md").write_text("# Our product", encoding="utf-8")
            res = run_tool(repo)
            self.assertEqual(res.returncode, 2)
            self.assertIn("not the Project Aegis source library", res.stdout)
            self.assertNotIn("Traceback", res.stdout + res.stderr)


class JsonContainmentTests(unittest.TestCase):
    def test_json_out_inside_fixture_repo_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = make_repo(tmp, [], [])
            write_skill(repo, "inside-skill")
            marker = repo / "keep.txt"
            marker.write_text("keep", encoding="utf-8")
            inside = repo / "report.json"
            res = run_tool(repo, "--json", str(inside))
            self.assertEqual(res.returncode, 2)
            self.assertIn("outside the scanned repository", res.stdout)
            self.assertFalse(inside.exists())
            self.assertEqual(marker.read_text(encoding="utf-8"), "keep")


class UnknownOptionTests(unittest.TestCase):
    def test_unknown_option_and_unexpected_positional_exit_two(self):
        for extra in ("--check-allowlist", "--bogus-flag"):
            res = run_tool(REPO_ROOT, extra)
            self.assertEqual(res.returncode, 2, extra + " -> " + res.stdout + res.stderr)
            self.assertIn("unknown option", res.stdout)
        res = run_tool(REPO_ROOT, "extra-positional")
        self.assertEqual(res.returncode, 2)
        self.assertIn("unexpected argument", res.stdout)


class JsonWriteFailureTests(unittest.TestCase):
    def test_missing_parent_out_path_exits_two_with_message(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = make_repo(tmp, [], [])
            write_skill(repo, "write-skill")
            with tempfile.TemporaryDirectory() as outdir:
                out = Path(outdir) / "missing-dir" / "out.json"
                res = run_tool(repo, "--json", str(out))
                self.assertEqual(res.returncode, 2, res.stdout + res.stderr)
                self.assertIn("cannot write --json OUT", res.stdout)
                self.assertNotIn("Traceback", res.stdout + res.stderr)


class FragmentLinkTests(unittest.TestCase):
    def test_fragment_link_counts_as_linked(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = make_repo(tmp, ['- **"one path"** -> [guide](docs/paths/guide.md#start)'], ["docs/paths/guide.md"])
            data = measure(repo)
            self.assertEqual(data["guides_linked_from_doors"], ["docs/paths/guide.md"])
            self.assertNotIn("docs/paths/guide.md", data["guides_not_linked_from_a_door"])


class ManifestShapeTests(unittest.TestCase):
    def test_malformed_manifest_shapes_fail_cleanly(self):
        for shape in ("[]", '{"skills": "nope"}', '{"skills": [1, 2]}'):
            with tempfile.TemporaryDirectory() as tmp:
                make_repo(tmp, [], [])
                repo = Path(tmp)
                tools = repo / "tools"
                tools.mkdir(parents=True, exist_ok=True)
                (tools / "skills-manifest.json").write_text(shape, encoding="utf-8")
                allow = repo / "fixture-allow-list.json"
                allow.write_text(REAL_ALLOW_LIST.read_text(encoding="utf-8"), encoding="utf-8")
                res = run_tool(repo, "--check-allow-list", "--allow-list", str(allow))
                self.assertEqual(res.returncode, 1, shape + " -> " + res.stdout + res.stderr)
                self.assertIn("allow-list: FAIL", res.stdout)
                self.assertIn("malformed", res.stdout)
                self.assertNotIn("Traceback", res.stdout + res.stderr)


if __name__ == "__main__":
    unittest.main()
