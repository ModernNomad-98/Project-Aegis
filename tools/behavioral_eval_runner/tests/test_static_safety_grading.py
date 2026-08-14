"""WP-2B-2: runtime no-network import probe for the grading stack.

The AST scan covers the whole package statically; this probe additionally
proves at RUNTIME that importing every grading-stack module loads no network
module (mirrors test_static_safety's probe for the WP-2B-1 core)."""

from __future__ import annotations

import subprocess
import sys
import unittest

from tools.behavioral_eval_runner.tests.helpers import REPO_ROOT

_IMPORT_PROBE = (
    "import sys\n"
    "import tools.behavioral_eval_runner.graders.contract\n"
    "import tools.behavioral_eval_runner.graders.records\n"
    "import tools.behavioral_eval_runner.graders.state_machine\n"
    "import tools.behavioral_eval_runner.graders.approval\n"
    "import tools.behavioral_eval_runner.graders.mutation\n"
    "import tools.behavioral_eval_runner.graders.append_only\n"
    "import tools.behavioral_eval_runner.graders.hashing\n"
    "import tools.behavioral_eval_runner.graders.activation\n"
    "import tools.behavioral_eval_runner.graders.controls\n"
    "import tools.behavioral_eval_runner.judge.interface\n"
    "import tools.behavioral_eval_runner.judge.policy\n"
    "import tools.behavioral_eval_runner.judge.rubric\n"
    "import tools.behavioral_eval_runner.judge.envelope\n"
    "import tools.behavioral_eval_runner.judge.mock\n"
    "import tools.behavioral_eval_runner.judge.verdict\n"
    "import tools.behavioral_eval_runner.judge.calibration\n"
    "loaded = [m for m in ('socket', 'urllib', 'urllib.request', 'http.client',"
    " 'ssl', 'ftplib', 'smtplib', 'subprocess') if m in sys.modules]\n"
    "print(','.join(loaded) if loaded else 'CLEAN')\n"
)


class TestGradingStackStaticSafety(unittest.TestCase):
    def test_importing_grading_stack_loads_no_network_module(self) -> None:
        completed = subprocess.run(
            [sys.executable, "-c", _IMPORT_PROBE],
            shell=False,
            capture_output=True,
            timeout=120,
            cwd=REPO_ROOT,
        )
        output = completed.stdout.decode("utf-8", "replace").strip()
        self.assertEqual(
            completed.returncode, 0, completed.stderr.decode("utf-8", "replace")
        )
        self.assertEqual(output.splitlines()[-1], "CLEAN")


if __name__ == "__main__":
    unittest.main()
