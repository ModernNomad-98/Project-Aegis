"""No network calls, no package-install path, no reachable dispatch path
(areas 38, 39, 40)."""

from __future__ import annotations

import os
import subprocess
import sys
import unittest

from tools.behavioral_eval_runner.cli import scan_package_sources
from tools.behavioral_eval_runner.tests.helpers import REPO_ROOT

PACKAGE_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
)

#: Every module in the package, imported by the no-network subprocess probe.
_IMPORT_PROBE = (
    "import sys\n"
    "import tools.behavioral_eval_runner as p\n"
    "import tools.behavioral_eval_runner.cli\n"
    "import tools.behavioral_eval_runner.census\n"
    "import tools.behavioral_eval_runner.materialize\n"
    "import tools.behavioral_eval_runner.budget\n"
    "import tools.behavioral_eval_runner.scheduler\n"
    "import tools.behavioral_eval_runner.aggregation\n"
    "import tools.behavioral_eval_runner.evidence\n"
    "import tools.behavioral_eval_runner.reporting\n"
    "import tools.behavioral_eval_runner.containment\n"
    "import tools.behavioral_eval_runner.process_control\n"
    "import tools.behavioral_eval_runner.execution_profile\n"
    "import tools.behavioral_eval_runner.preflight\n"
    "import tools.behavioral_eval_runner.adapters.claude_code\n"
    "loaded = [m for m in ('socket', 'urllib', 'urllib.request', 'http.client',"
    " 'ssl', 'ftplib', 'smtplib') if m in sys.modules]\n"
    "print(','.join(loaded) if loaded else 'CLEAN')\n"
)


class TestStaticSafety(unittest.TestCase):
    def test_no_forbidden_source_patterns(self) -> None:
        violations = scan_package_sources()
        self.assertEqual(violations, [])

    def test_importing_the_package_loads_no_network_module(self) -> None:
        completed = subprocess.run(
            [sys.executable, "-c", _IMPORT_PROBE],
            shell=False,
            capture_output=True,
            timeout=120,
            cwd=REPO_ROOT,
        )
        output = completed.stdout.decode("utf-8", "replace").strip()
        self.assertEqual(completed.returncode, 0, completed.stderr.decode("utf-8", "replace"))
        self.assertEqual(output.splitlines()[-1], "CLEAN")

    def test_no_dependency_or_install_files(self) -> None:
        for name in (
            "requirements.txt",
            "pyproject.toml",
            "setup.py",
            "setup.cfg",
            "Pipfile",
            "package.json",
        ):
            self.assertFalse(
                os.path.exists(os.path.join(PACKAGE_ROOT, name)),
                f"{name} must not exist: no dependency addition is authorized",
            )

    def test_no_live_provider_adapter_module(self) -> None:
        adapters_dir = os.path.join(PACKAGE_ROOT, "adapters")
        modules = sorted(
            name for name in os.listdir(adapters_dir) if name.endswith(".py")
        )
        self.assertEqual(modules, ["__init__.py", "base.py", "claude_code.py"])

    def test_no_dispatch_function_reachable(self) -> None:
        """The runtime package exposes no callable that could reach a provider."""
        forbidden_fragments = ("api.anthropic", "openai", "bedrock", "vertex")
        for directory, _dirs, files in os.walk(PACKAGE_ROOT):
            if os.path.basename(directory) == "tests":
                continue  # this very check lives here; the scan targets runtime code
            for name in files:
                if not name.endswith(".py"):
                    continue
                path = os.path.join(directory, name)
                with open(path, encoding="utf-8") as handle:
                    source = handle.read().lower()
                for fragment in forbidden_fragments:
                    self.assertNotIn(fragment, source, f"{name}: {fragment}")

    def test_subprocess_confined_to_allowlisted_modules(self) -> None:
        offenders: list[str] = []
        for directory, _dirs, files in os.walk(PACKAGE_ROOT):
            if os.path.basename(directory) == "tests":
                continue
            for name in files:
                if not name.endswith(".py"):
                    continue
                path = os.path.join(directory, name)
                with open(path, encoding="utf-8") as handle:
                    source = handle.read()
                if "import subprocess" in source and name not in (
                    "materialize.py",
                    "process_control.py",
                    "cli.py",  # holds the allowlist constant string only
                ):
                    offenders.append(name)
        self.assertEqual(offenders, [])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
