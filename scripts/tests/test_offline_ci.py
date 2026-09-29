#!/usr/bin/env python3
"""Regression checks for evidence exit codes and the actual protected-file guard."""
from __future__ import annotations

import copy
import json
import os
import re
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml

REPO = Path(__file__).resolve().parents[2]
RECORDER = REPO / "scripts/ci/record-check.py"
WORKFLOW = REPO / ".github/workflows/validate-skills.yml"
VALIDATOR = REPO / "scripts/validate-skills.py"
# The only module runs that need the checkout root on sys.path; gate-guard
# protects every root-level importable name in their place.
# The diagnostic runs only in the isolated tools-tests-windows job.
ROOT_PATH_MODULES = {"tools.behavioral_eval_runner", "unittest",
                     "tools.aegis_delivery_control.tests.windows_owner_diagnostic"}
# A module placed beside a gate script: it loads the real module of the same
# name, then forces the interpreter to exit 0 whatever the script returns.
SHADOW_MODULE = """import atexit, importlib, os, sys
_here = os.path.dirname(os.path.abspath(__file__))
sys.path[:] = [p for p in sys.path if os.path.abspath(p or ".") != _here]
del sys.modules[__name__]
sys.modules[__name__] = importlib.import_module(__name__)
atexit.register(lambda: os._exit(0))
"""


def load_workflow():
    # BaseLoader preserves GitHub's literal `on` key instead of YAML 1.1 bools.
    return yaml.load(WORKFLOW.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)


class RecorderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="aegis-ci-recorder-")
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name) / "evidence"
        self.env = dict(os.environ, AEGIS_CI_EVIDENCE_DIR=str(self.output))

    def run_check(self, label, command):
        return subprocess.run([sys.executable, str(RECORDER), label, "--", *command],
                              cwd=REPO, env=self.env, capture_output=True)

    def test_failure_preserves_native_status_and_both_streams(self):
        result = self.run_check("failure", [sys.executable, "-c",
            "import sys; print('stdout evidence'); sys.stderr.write('stderr evidence\\n'); sys.exit(7)"])
        self.assertEqual(7, result.returncode, result.stdout + result.stderr)
        log = (self.output / "failure.log").read_bytes()
        self.assertIn(b"stdout evidence", log)
        self.assertIn(b"stderr evidence", log)
        report = json.loads((self.output / "failure.json").read_text(encoding="utf-8"))
        self.assertEqual(7, report["exit_code"])
        self.assertEqual(subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO,
                                                text=True).strip(), report["checkout_sha"])

    def test_missing_command_is_recorded_as_failure(self):
        result = self.run_check("missing", ["aegis-nonexistent-ci-command-3ba68f"])
        self.assertEqual(127, result.returncode)
        report = json.loads((self.output / "missing.json").read_text(encoding="utf-8"))
        self.assertEqual(127, report["exit_code"])
        self.assertIn(b"Cannot execute check", (self.output / "missing.log").read_bytes())

    def test_repeated_label_cannot_replace_prior_evidence(self):
        self.assertEqual(0, self.run_check("once", [sys.executable, "-c", "print('original')"]).returncode)
        before = {p.name: p.read_bytes() for p in self.output.iterdir()}
        self.assertNotEqual(0, self.run_check("once", [sys.executable, "-c", "print('replacement')"]).returncode)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.output.iterdir()})

    def test_label_cannot_escape_evidence_directory(self):
        self.assertNotEqual(0, self.run_check("../escape", [sys.executable, "-c", "pass"]).returncode)
        self.assertFalse(self.output.exists())


@unittest.skipUnless(os.name == "posix" and shutil.which("bash"), "the gate-guard job executes on Linux")
class ProtectedFileGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        workflow = load_workflow()
        cls.guard = next(step["run"] for step in workflow["jobs"]["gate-guard"]["steps"]
                         if "gate_pattern=" in step.get("run", ""))

    def run_guard(self, paths, *, rename=False, links=(),
                  rename_from=".github/workflows/previous.yml", rename_to="docs/previous.yml"):
        """`links` holds (path, target) pairs committed as git symlinks
        (mode 120000) through the index, so no real symlink is needed."""
        with tempfile.TemporaryDirectory(prefix="aegis-ci-guard-") as temporary:
            root = Path(temporary)
            repo = root / "repo"
            repo.mkdir()
            def git(*args):
                return subprocess.run(["git", "-c", "user.name=Fixture", "-c",
                                       "user.email=fixture@example.invalid", *args], cwd=repo,
                                      check=True, capture_output=True)
            git("init", "--quiet")
            (repo / "README.md").write_text("fixture\n", encoding="utf-8")
            if rename:
                old = repo / rename_from
                old.parent.mkdir(parents=True, exist_ok=True)
                old.write_text("protected fixture\n", encoding="utf-8")
            # --force: a user-level excludes file must not hide a fixture path
            # (Claude Code adds **/.claude/settings.local.json to one).
            git("add", "--force", ".")
            git("commit", "--quiet", "-m", "fixture base")
            git("branch", "fixture-base")
            git("remote", "add", "origin", str(repo))
            if rename:
                (repo / rename_to).parent.mkdir(parents=True, exist_ok=True)
                git("mv", rename_from, rename_to)
            else:
                for path in paths:
                    file = repo / path
                    file.parent.mkdir(parents=True, exist_ok=True)
                    file.write_text("changed fixture\n", encoding="utf-8")
            git("add", "--force", ".")
            for link, target in links:
                blob = subprocess.run(["git", "hash-object", "-w", "--stdin"], cwd=repo, check=True,
                                      input=target.encode("utf-8"), capture_output=True).stdout
                git("update-index", "--add", "--cacheinfo",
                    f"120000,{blob.decode('ascii').strip()},{link}")
            git("commit", "--quiet", "-m", "fixture change")
            return subprocess.run(["bash", "--noprofile", "--norc", "-eo", "pipefail", "-c", self.guard],
                                  cwd=repo, env=dict(os.environ, BASE_REF="fixture-base", RUNNER_TEMP=str(root)),
                                  capture_output=True, text=True)

    def test_each_enforcement_surface_requires_manual_merge(self):
        for path in (".github/workflows/check.yml", ".github/CODEOWNERS",
                     "scripts/validate-skills.py", "scripts/check_dco.py", "scripts/tests/fixture.py",
                     "scripts/ci/record-check.py", "scripts/audit-skill-contracts.py",
                     "scripts/acceptance/scenario-a-fixture/manifest.json", "tools.py", "tools/__init__.py",
                     "tools/behavioral_eval_runner/tests/fixture.py",
                     "tools/behavioral_eval_runner/schemas/fixture.json",
                     "tools/behavioral_eval_runner/graders/fixture.py", "requirements.txt", "requirements-ci.txt"):
            with self.subTest(path=path):
                result = self.run_guard([path])
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn("requires manual review and merge", result.stdout)

    def test_import_path_shadowing_locations_require_manual_merge(self):
        # scripts/ is first on sys.path for `python scripts/<gate>.py`; the
        # checkout root is first for the `python -m` gate commands.
        for path in ("scripts/yaml.py", "scripts/json.py", "scripts/new_helper.py",
                     "Scripts/yaml.py", "yaml.py", "unittest.py", "openai.py",
                     "sitecustomize.py", "usercustomize.py", "conftest.py", "YAML.PY",
                     "shadow.pth", "yaml.pyc", "yaml.pyw", "yaml.pyd",
                     "yaml.cpython-314-x86_64-linux-gnu.so", "yaml/__init__.py",
                     "unittest/__init__.pyc"):
            with self.subTest(path=path):
                result = self.run_guard([path])
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn("requires manual review and merge", result.stdout)

    def test_project_agent_files_require_manual_merge(self):
        # Claude Code honours `hooks`, `mcpServers` and `permissionMode` in
        # project agent files, so adding or editing one is a gate change.
        # Every .claude/agents/ up to the repository root is loaded, so nested
        # directories count too.
        for path in (".claude/agents/secure-saas-reviewer.md", ".claude/agents/new-agent.md",
                     ".claude/agents/nested/agent.md", ".Claude/Agents/new-agent.md",
                     ".CLAUDE/AGENTS/NEW-AGENT.MD", "docs/.claude/agents/example.md",
                     "a/b/.claude/agents/deep/agent.md", "docs/.Claude/Agents/agent.md"):
            with self.subTest(path=path):
                result = self.run_guard([path])
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn("requires manual review and merge", result.stdout)

    def test_root_executables_require_manual_merge(self):
        # Windows CreateProcess can resolve `git` or `python` from the checkout
        # root, the recorder's working directory.
        for path in ("git.exe", "python.exe", "PWSH.EXE", "powershell.com", "git.bat",
                     "python.cmd", "profile.ps1", "version.dll"):
            with self.subTest(path=path):
                result = self.run_guard([path])
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn("requires manual review and merge", result.stdout)

    def test_symlinked_claude_entries_require_manual_merge(self):
        # A nested `.claude` or `.claude/agents` symlink can point at a payload
        # directory whose own paths never contain `.claude/agents/`.
        for link in ("docs/.claude", "docs/.Claude", "docs/.claude/agents", ".claude"):
            with self.subTest(link=link):
                result = self.run_guard(["payload/agents/evil.md"], links=[(link, "../payload")])
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn("requires manual review and merge", result.stdout)
                self.assertIn(link, result.stdout.split("Gate files touched:")[-1])

    def test_symlinked_config_directories_require_manual_merge(self):
        # A commands, hooks or plugin directory entry that is itself a symlink
        # has no trailing slash in the diff, yet redirects what Claude Code loads.
        for link in ("docs/.claude/commands", ".claude/hooks", "docs/.claude-plugin",
                     ".claude/skills/x/.claude-plugin"):
            with self.subTest(link=link):
                result = self.run_guard(["payload/plugin.json"], links=[(link, "../payload")])
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(link, result.stdout.split("Gate files touched:")[-1])

    def test_claude_code_and_git_config_files_require_manual_merge(self):
        # Settings can define hooks, credential helpers and permissions;
        # .mcp.json starts server processes; commands carry skill-style
        # frontmatter; hooks/ holds hook scripts; .claude-plugin/ bundles hooks
        # and MCP servers; .gitattributes can hide diffs and change evidence
        # bytes. Claude Code and Git read nested copies, so every depth counts.
        for path in (".gitattributes", "docs/evidence/offline-ci-2026-09-12/.gitattributes",
                     "a/b/.GitAttributes", ".claude/settings.json", ".claude/settings.local.json",
                     ".Claude/Settings.JSON", "docs/.claude/settings.json",
                     "docs/.claude/settings.local.json", ".mcp.json", "docs/.mcp.json", ".MCP.JSON",
                     ".claude/commands/deploy.md", "docs/.claude/commands/deploy.md",
                     ".Claude/Commands/x.md", ".claude/hooks/check.sh", "a/.claude/hooks/check.sh",
                     ".claude-plugin/plugin.json", "docs/.claude-plugin/plugin.json",
                     "docs/.claude/commands", "docs/.claude/hooks", "a/.claude-plugin",
                     ".claude/skills/x/.claude-plugin/plugin.json", ".claude/skills/x/.mcp.json"):
            with self.subTest(path=path):
                result = self.run_guard([path])
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn("requires manual review and merge", result.stdout)

    def test_ordinary_skill_and_document_changes_pass(self):
        result = self.run_guard(["README.md", "docs/notes.md", ".claude/skills/example/SKILL.md",
                                 "docs/example.py", ".claude/skills/example/scripts/helper.py",
                                 "tools/aegis_setup/helper.py", "artifacts/scripts/yaml.py",
                                 ".claude/agents-notes.md", "docs/claude/agents/example.md",
                                 "docs/xclaude/agents/example.md", "docs/my.claude",
                                 ".claude/agentsX/example.md",
                                 # Near-misses of the Claude Code and Git config rules.
                                 ".claude/skills/example/references/settings.json",
                                 ".claude/settings.json.bak", ".claude/settings.jsonc",
                                 "docs/gitattributes.md", ".gitattributes.md", "x.gitattributes",
                                 "x.mcp.json", "docs/mcp.json", ".mcp.json.example",
                                 ".claude/commands-notes.md", "docs/claude/settings.json",
                                 ".claude/skills/example/hooks.md", "CLAUDE.md", "AGENTS.md",
                                 "docs/tool.exe", "tools/aegis_setup/run.ps1"])
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_renaming_a_protected_file_outside_the_set_is_still_guarded(self):
        for old, new in ((".github/workflows/previous.yml", "docs/previous.yml"),
                         (".gitattributes", "docs/old-gitattributes.txt"),
                         (".claude/settings.json", "docs/old-settings.json")):
            with self.subTest(old=old):
                result = self.run_guard([], rename=True, rename_from=old, rename_to=new)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn("requires manual review and merge", result.stdout)

    def test_unicode_and_newline_names_cannot_bypass_the_guard(self):
        result = self.run_guard([".github/workflows/\u2603\ncheck.yml"])
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("requires manual review and merge", result.stdout)


class ImportPathIsolationTests(unittest.TestCase):
    """A module a pull request adds cannot rewrite a gate script's exit status."""

    @classmethod
    def setUpClass(cls):
        cls.workflow = load_workflow()

    def python_calls(self):
        for job_name, job in self.workflow["jobs"].items():
            for step in job["steps"]:
                for line in step.get("run", "").splitlines():
                    words = shlex.split(line, comments=True)
                    for index, word in enumerate(words):
                        if word == "python":
                            yield job_name, step.get("name", ""), words[index + 1:]

    def test_every_gate_python_call_keeps_the_script_directory_off_sys_path(self):
        calls = list(self.python_calls())
        self.assertGreaterEqual(len(calls), 30)
        for job_name, step_name, args in calls:
            with self.subTest(job=job_name, step=step_name, args=args[:3]):
                if args[:1] == ["-m"] and args[1:2] and args[1] in ROOT_PATH_MODULES:
                    continue
                self.assertEqual("-P", args[0] if args else None)

    def validator_command(self, job_name):
        step = next(s for s in self.workflow["jobs"][job_name]["steps"]
                    if s.get("name") == "Run skill validator")
        words = shlex.split(step["run"])
        command = words[words.index("--") + 1:]
        self.assertEqual(["python", "-P", "scripts/validate-skills.py"], command)
        return [sys.executable, *command[1:]]

    def run_shadowed_validator(self, command):
        with tempfile.TemporaryDirectory(prefix="aegis-ci-shadow-") as temporary:
            root = Path(temporary)
            (root / "scripts").mkdir()
            shutil.copyfile(VALIDATOR, root / "scripts/validate-skills.py")
            (root / "scripts/yaml.py").write_text(SHADOW_MODULE, encoding="utf-8")
            skill = root / ".claude/skills/broken-skill"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "---\nname: not-the-directory-name\ndescription: Deliberately broken fixture.\n---\n\n# Broken\n",
                encoding="utf-8")
            env = dict(os.environ)
            env.pop("PYTHONSAFEPATH", None)
            return subprocess.run(command, cwd=root, env=env, capture_output=True, text=True)

    def test_shadow_module_cannot_turn_a_failing_validator_green(self):
        for job_name in ("validate-skills", "windows-offline-checks"):
            with self.subTest(job=job_name):
                result = self.run_shadowed_validator(self.validator_command(job_name))
                self.assertIn("FAILED:", result.stdout, result.stdout + result.stderr)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)

    def test_fixture_is_a_real_bypass_without_isolation(self):
        # Proves the shadow above is live: without -P the same failing run exits 0.
        command = [arg for arg in self.validator_command("validate-skills") if arg != "-P"]
        result = self.run_shadowed_validator(command)
        self.assertIn("FAILED:", result.stdout, result.stdout + result.stderr)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)


class GateJobIsolationTests(unittest.TestCase):
    """Gate jobs run only gate-guarded repository code; tools suites run apart.

    A step in a gate job can write $GITHUB_ENV or $GITHUB_PATH, or rewrite a
    gate script before it runs, so any pull-request-controlled code outside
    the gate-guard set must run in a separate job.
    """

    GATE_JOBS = ("validate-skills", "windows-offline-checks")
    TOOLS_JOBS = ("tools-tests-linux", "tools-tests-windows")
    TOOLS_LABELS = {
        "tools-tests-linux": ["setup-bridge", "setup-tests", "delivery-control"],
        "tools-tests-windows": ["setup-bridge", "setup-tests",
                                "delivery-control-diagnostic", "delivery-control"],
    }

    @classmethod
    def setUpClass(cls):
        cls.workflow = load_workflow()
        guard = next(step["run"] for step in cls.workflow["jobs"]["gate-guard"]["steps"]
                     if "gate_pattern=" in step.get("run", ""))
        cls.gate_pattern = re.compile(re.search(r"gate_pattern='([^']+)'", guard).group(1),
                                      re.IGNORECASE)

    def repo_paths(self, job_name):
        """Yield every repository path or module a job's steps execute or read."""
        for step in self.workflow["jobs"][job_name]["steps"]:
            if "working-directory" in step:
                yield step.get("name", ""), step["working-directory"].rstrip("/") + "/"
            for line in step.get("run", "").splitlines():
                words = shlex.split(line, comments=True, posix=True)
                for index, word in enumerate(words):
                    if index and words[index - 1] == "-m" and "." in word:
                        yield step.get("name", ""), word.replace(".", "/") + "/"
                    elif index and words[index - 1] == "-r":
                        yield step.get("name", ""), word
                    elif ("/" in word and "$" not in word and "://" not in word
                          and not word.startswith(("-", "origin/"))):
                        yield step.get("name", ""), word

    def test_gate_jobs_run_only_gate_guarded_repository_paths(self):
        for job_name in self.GATE_JOBS:
            paths = list(self.repo_paths(job_name))
            self.assertGreaterEqual(len(paths), 10, job_name)
            for step_name, path in paths:
                with self.subTest(job=job_name, step=step_name, path=path):
                    self.assertRegex(path, self.gate_pattern)

    def test_gate_jobs_run_no_node_or_tools_suites(self):
        for job_name in self.GATE_JOBS:
            job = self.workflow["jobs"][job_name]
            self.assertNotIn("needs", job)
            for step in job["steps"]:
                with self.subTest(job=job_name, step=step.get("name", step.get("uses"))):
                    self.assertNotIn("setup-node", step.get("uses", ""))
                    words = set(shlex.split(step.get("run", ""), comments=True))
                    self.assertFalse(words & {"node", "npm", "npx"}, words)
                    text = step.get("run", "") + step.get("working-directory", "")
                    for path in ("tools/aegis_setup", "tools/aegis_delivery_control"):
                        self.assertNotIn(path, text)

    def test_tools_jobs_run_every_suite_with_read_only_access(self):
        for job_name in self.TOOLS_JOBS:
            job = self.workflow["jobs"][job_name]
            with self.subTest(job=job_name):
                self.assertEqual({"contents": "read"}, job["permissions"])
                self.assertNotIn("needs", job)
                self.assertNotIn("secrets.", json.dumps(job))
                checkout = next(s for s in job["steps"]
                                if s.get("uses", "").startswith("actions/checkout@"))
                self.assertEqual("false", checkout["with"]["persist-credentials"])
                labels = [shlex.split(s["run"])[3] for s in job["steps"]
                          if "record-check.py" in s.get("run", "")]
                self.assertEqual(self.TOOLS_LABELS[job_name], labels)

    def test_gate_jobs_do_not_depend_on_tools_jobs(self):
        for job_name, job in self.workflow["jobs"].items():
            needs = job.get("needs", [])
            needs = [needs] if isinstance(needs, str) else needs
            with self.subTest(job=job_name):
                self.assertFalse(set(needs) & set(self.TOOLS_JOBS))

    # Environment variables that make an interpreter, shell or tool load code
    # or configuration from a chosen location. None belongs in a gate job.
    LOADER_VARIABLES = {
        "PATH", "PYTHONPATH", "PYTHONHOME", "PYTHONSTARTUP", "PYTHONUSERBASE",
        "PYTHONPLATLIBDIR", "PYTHONEXECUTABLE", "NODE_OPTIONS", "NODE_PATH",
        "PSMODULEPATH", "BASH_ENV", "ENV", "LD_PRELOAD", "LD_LIBRARY_PATH",
        "GIT_EXEC_PATH", "GIT_DIR", "GIT_WORK_TREE", "GIT_TEMPLATE_DIR",
    }
    # Any GIT_CONFIG* variable (COUNT, KEY_n, VALUE_n, GLOBAL, SYSTEM,
    # NOSYSTEM, PARAMETERS) can inject git configuration such as
    # core.fsmonitor, which `git status` in the recorder would execute.
    LOADER_VARIABLE_PREFIXES = ("GIT_CONFIG",)
    GATE_SHELLS = {"bash", "pwsh", "powershell"}

    def gate_violations(self, workflow):
        """Return every gate-isolation violation in a parsed workflow.

        Covers: action pins, step and job-default shells, job-default working
        directories, loader or git-config variables, and env or `with` values
        that climb (`..`) or name an unguarded path.
        """
        found = []

        def check_value(where, value):
            if "${{" in value:
                return
            if ".." in value:
                found.append(f"{where}: value climbs with '..': {value!r}")
            elif ("/" in value or "\\" in value) and not self.gate_pattern.search(
                    value.replace("\\", "/")):
                found.append(f"{where}: value names an unguarded path: {value!r}")

        def check_env(where, env):
            for key, value in (env or {}).items():
                upper = key.upper()
                if upper in self.LOADER_VARIABLES or upper.startswith(self.LOADER_VARIABLE_PREFIXES):
                    found.append(f"{where}: loader variable {key}")
                check_value(f"{where} {key}", value)

        check_env("workflow env", workflow.get("env"))
        for job_name in self.GATE_JOBS:
            job = workflow["jobs"][job_name]
            check_env(f"{job_name} env", job.get("env"))
            defaults = (job.get("defaults") or {}).get("run") or {}
            if defaults.get("shell", "bash") not in self.GATE_SHELLS:
                found.append(f"{job_name}: default shell {defaults['shell']!r}")
            if "working-directory" in defaults:
                found.append(
                    f"{job_name}: default working-directory {defaults['working-directory']!r}")
            for step in job["steps"]:
                where = f"{job_name}/{step.get('name', step.get('uses'))}"
                if "uses" in step and not re.fullmatch(
                        r"[\w.-]+/[\w.-]+@[0-9a-f]{40}", step["uses"]):
                    found.append(f"{where}: action is local or not SHA-pinned: {step['uses']!r}")
                if "shell" in step and step["shell"] not in self.GATE_SHELLS:
                    found.append(f"{where}: custom shell {step['shell']!r}")
                if ".." in step.get("working-directory", ""):
                    found.append(f"{where}: working-directory climbs with '..'")
                check_env(f"{where} env", step.get("env"))
                for key, value in (step.get("with") or {}).items():
                    check_value(f"{where} with {key}", value)
        return found

    def mutated(self, change):
        workflow = copy.deepcopy(self.workflow)
        change(workflow)
        return self.gate_violations(workflow)

    def first_step(self, workflow, job_name="validate-skills", name="Run skill validator"):
        return next(s for s in workflow["jobs"][job_name]["steps"] if s.get("name") == name)

    def assert_mutation_caught(self, change, fragment):
        violations = self.mutated(change)
        self.assertTrue(any(fragment in v for v in violations), violations)

    def test_current_workflow_has_no_gate_violations(self):
        self.assertEqual([], self.gate_violations(self.workflow))

    def test_mutation_local_or_unpinned_action_is_caught(self):
        for uses in ("./tools/aegis_setup/action", "docker://alpine", "actions/checkout@v4"):
            with self.subTest(uses=uses):
                self.assert_mutation_caught(
                    lambda w: w["jobs"]["validate-skills"]["steps"].append({"uses": uses}),
                    "not SHA-pinned")

    def test_mutation_custom_shell_is_caught(self):
        for job_name in self.GATE_JOBS:
            with self.subTest(job=job_name, where="step"):
                self.assert_mutation_caught(
                    lambda w: w["jobs"][job_name]["steps"][-1].__setitem__(
                        "shell", "python tools/aegis_setup/evil.py {0}"),
                    "custom shell")
            with self.subTest(job=job_name, where="job default"):
                self.assert_mutation_caught(
                    lambda w: w["jobs"][job_name]["defaults"]["run"].__setitem__(
                        "shell", "bash --rcfile tools/aegis_setup/rc -i {0}"),
                    "default shell")
            with self.subTest(job=job_name, where="job default directory"):
                self.assert_mutation_caught(
                    lambda w: w["jobs"][job_name]["defaults"]["run"].__setitem__(
                        "working-directory", "tools"),
                    "default working-directory")

    def test_mutation_loader_and_git_config_variables_are_caught(self):
        keys = ("PYTHONPATH", "Path", "GIT_CONFIG_COUNT", "GIT_CONFIG_KEY_0",
                "GIT_CONFIG_VALUE_0", "GIT_CONFIG_GLOBAL", "GIT_CONFIG_SYSTEM",
                "GIT_CONFIG_NOSYSTEM", "GIT_CONFIG_PARAMETERS", "GIT_DIR",
                "GIT_WORK_TREE", "GIT_TEMPLATE_DIR")
        scopes = {
            "workflow": lambda w: w.setdefault("env", {}),
            "job": lambda w: w["jobs"]["windows-offline-checks"].setdefault("env", {}),
            "step": lambda w: self.first_step(w).setdefault("env", {}),
        }
        for key in keys:
            for scope, env_of in scopes.items():
                with self.subTest(key=key, scope=scope):
                    self.assert_mutation_caught(
                        lambda w: env_of(w).__setitem__(key, "1"), f"loader variable {key}")

    def test_mutation_climbing_or_unguarded_value_is_caught(self):
        cases = (
            ("env", "HOOK", "scripts/../tools/aegis_setup/evil.sh", "climbs"),
            ("with", "path", "scripts/../tools", "climbs"),
            ("env", "HOOK", "tools/aegis_setup/evil.sh", "unguarded path"),
            ("with", "path", "tools\\aegis_setup", "unguarded path"),
        )
        for section, key, value, fragment in cases:
            with self.subTest(section=section, value=value):
                self.assert_mutation_caught(
                    lambda w: self.first_step(w).setdefault(section, {}).__setitem__(key, value),
                    fragment)

    def test_gate_pattern_protects_root_dll(self):
        # Belt and braces: the exe-search variable governs programs, not DLLs.
        for path in ("version.dll", "Git.DLL"):
            with self.subTest(path=path):
                self.assertRegex(path, self.gate_pattern)
        self.assertNotRegex("tools/aegis_setup/helper.dll", self.gate_pattern)

    def test_workflow_disables_windows_current_directory_executable_search(self):
        self.assertEqual("1", self.workflow["env"]["NoDefaultCurrentDirectoryInExePath"])

    @unittest.skipUnless(sys.platform == "win32", "Windows executable search order")
    def test_root_executable_cannot_replace_git_under_the_workflow_env(self):
        # CreateProcess searches the PARENT's current directory. The recorder
        # runs from the checkout root and starts `git`, so a stand-in git.exe
        # there (a copy of hostname.exe) must not run when the workflow's
        # variable is set. The parent below mimics the recorder.
        stand_in = Path(os.environ["SystemRoot"]) / "System32" / "hostname.exe"
        with tempfile.TemporaryDirectory(prefix="aegis-ci-exe-") as temporary:
            shutil.copyfile(stand_in, Path(temporary) / "git.exe")

            def run_git(search_current_directory):
                # Windows environment keys are case-insensitive and os.environ
                # upper-cases them, so drop the variable under any spelling.
                env = {key: value for key, value in os.environ.items()
                       if key.upper() != "NODEFAULTCURRENTDIRECTORYINEXEPATH"}
                if not search_current_directory:
                    env["NoDefaultCurrentDirectoryInExePath"] = (
                        self.workflow["env"]["NoDefaultCurrentDirectoryInExePath"])
                parent = ("import subprocess; "
                          "r = subprocess.run(['git', '--version'], capture_output=True, text=True); "
                          "print(r.stdout.strip())")
                return subprocess.run([sys.executable, "-c", parent], cwd=temporary, env=env,
                                      capture_output=True, text=True, timeout=60)

            protected = run_git(search_current_directory=False)
            self.assertEqual(0, protected.returncode, protected.stderr)
            self.assertTrue(protected.stdout.startswith("git version"), protected.stdout)
            # Proves the stand-in is live: without the variable, it runs instead.
            exposed = run_git(search_current_directory=True)
            self.assertFalse(exposed.stdout.startswith("git version"), exposed.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
