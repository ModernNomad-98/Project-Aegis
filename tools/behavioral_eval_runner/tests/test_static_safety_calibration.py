"""WP-2B-3 static-safety boundary (task section 13).

Proves the ONE narrow allowlist added for the calibration provider adapter
does not weaken the general policy: provider fragments appear ONLY in the
approved adapter modules, importing the calibration stack loads no network
module and does not import the SDK, and every general denial (AST scan,
DisabledJudgeProvider, dependency-file ban) still holds.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import unittest

from tools.behavioral_eval_runner.cli import scan_package_sources
from tools.behavioral_eval_runner.tests.helpers import REPO_ROOT

PACKAGE_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
)

#: The ONLY runtime modules permitted to reference the provider/SDK by name
#: (BER-DEC-008 decisions 1, 29; the narrow WP-2B-3 allowlist).
PROVIDER_FRAGMENT_ALLOWLIST = frozenset(
    {
        "judge/calibration_transport.py",
        "judge/calibration_provider.py",
        # Stage A2 (BER-DEC-008): the dedicated DEVELOPMENT driver composes
        # the two adapter modules and may therefore name the provider.
        "judge/calibration_development_driver.py",
    }
)

_IMPORT_PROBE = (
    "import sys\n"
    "import tools.behavioral_eval_runner.judge.calibration_errors\n"
    "import tools.behavioral_eval_runner.judge.calibration_credential\n"
    "import tools.behavioral_eval_runner.judge.calibration_transport\n"
    "import tools.behavioral_eval_runner.judge.calibration_ledger\n"
    "import tools.behavioral_eval_runner.judge.calibration_dataset\n"
    "import tools.behavioral_eval_runner.judge.calibration_envelope\n"
    "import tools.behavioral_eval_runner.judge.calibration_gates\n"
    "import tools.behavioral_eval_runner.judge.calibration_provider\n"
    "import tools.behavioral_eval_runner.judge."
    "calibration_development_driver\n"
    "loaded = [m for m in ('socket', 'urllib', 'urllib.request', 'http.client',"
    " 'ssl', 'ftplib', 'smtplib', 'subprocess', 'openai', 'httpx2', 'httpx')"
    " if m in sys.modules]\n"
    "print(','.join(loaded) if loaded else 'CLEAN')\n"
)


def _runtime_python_files() -> list[tuple[str, str]]:
    results: list[tuple[str, str]] = []
    for directory, _dirs, files in os.walk(PACKAGE_ROOT):
        if os.path.basename(directory) == "tests":
            continue
        for name in files:
            if not name.endswith(".py"):
                continue
            path = os.path.join(directory, name)
            relative = os.path.relpath(path, PACKAGE_ROOT).replace("\\", "/")
            with open(path, encoding="utf-8") as handle:
                results.append((relative, handle.read()))
    return results


class TestCalibrationStaticSafety(unittest.TestCase):
    def test_import_probe_is_clean_lazy_sdk_import_proven(self) -> None:
        completed = subprocess.run(
            [sys.executable, "-c", _IMPORT_PROBE],
            shell=False, capture_output=True, timeout=120, cwd=REPO_ROOT,
        )
        output = completed.stdout.decode("utf-8", "replace").strip()
        self.assertEqual(
            completed.returncode, 0,
            completed.stderr.decode("utf-8", "replace"),
        )
        self.assertEqual(output.splitlines()[-1], "CLEAN")

    def test_provider_fragments_confined_to_the_allowlist(self) -> None:
        offenders: list[str] = []
        allowlisted_present: set[str] = set()
        for relative, source in _runtime_python_files():
            lowered = source.lower()
            if "openai" in lowered:
                if relative in PROVIDER_FRAGMENT_ALLOWLIST:
                    allowlisted_present.add(relative)
                else:
                    offenders.append(relative)
        self.assertEqual(offenders, [])
        self.assertEqual(allowlisted_present, set(PROVIDER_FRAGMENT_ALLOWLIST))

    def test_other_provider_fragments_remain_banned_everywhere(self) -> None:
        for relative, source in _runtime_python_files():
            lowered = source.lower()
            for fragment in ("api.anthropic", "bedrock", "vertex"):
                self.assertNotIn(fragment, lowered, f"{relative}: {fragment}")

    def test_no_tls_or_verification_weakening_literals(self) -> None:
        for relative, source in _runtime_python_files():
            self.assertNotIn("verify=False", source, relative)
            self.assertNotIn("trust_env=True", source, relative)

    def test_no_credential_looking_literal_anywhere(self) -> None:
        pattern = re.compile(r"sk-[A-Za-z0-9]{16,}")
        for directory, _dirs, files in os.walk(PACKAGE_ROOT):
            for name in files:
                if not name.endswith((".py", ".json", ".md")):
                    continue
                path = os.path.join(directory, name)
                with open(path, encoding="utf-8") as handle:
                    source = handle.read()
                self.assertIsNone(pattern.search(source), path)

    def test_ast_scan_still_reports_zero_violations(self) -> None:
        self.assertEqual(scan_package_sources(), [])

    def test_no_dependency_files_added_by_wp2b3(self) -> None:
        for name in ("requirements.txt", "pyproject.toml", "setup.py",
                     "setup.cfg", "Pipfile", "package.json"):
            self.assertFalse(os.path.exists(os.path.join(PACKAGE_ROOT, name)))

    def test_calibration_modules_never_import_subprocess_or_ctypes(self) -> None:
        for relative, source in _runtime_python_files():
            if not relative.startswith("judge/calibration_"):
                continue
            self.assertNotIn("import subprocess", source, relative)
            self.assertNotIn("import ctypes", source, relative)

    def test_generic_live_denial_boundary_is_untouched(self) -> None:
        from tools.behavioral_eval_runner.errors import LiveDispatchDisabledError
        from tools.behavioral_eval_runner.judge.interface import (
            DisabledJudgeProvider,
        )

        provider = DisabledJudgeProvider()
        with self.assertRaises(LiveDispatchDisabledError):
            provider.dispatch(None, b"")
        self.assertEqual(provider.dispatch_count, 0)

    def test_adapters_directory_remains_frozen(self) -> None:
        adapters_dir = os.path.join(PACKAGE_ROOT, "adapters")
        modules = sorted(
            name for name in os.listdir(adapters_dir) if name.endswith(".py")
        )
        self.assertEqual(modules, ["__init__.py", "base.py", "claude_code.py"])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
