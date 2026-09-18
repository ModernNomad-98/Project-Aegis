from __future__ import annotations

import os
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from contextlib import redirect_stdout
from unittest.mock import patch

from tools.aegis_delivery_control.contracts import DispatchDenied
from tools.aegis_delivery_control.cli import ExpectedFreshnessOracle, main
from tools.aegis_delivery_control.storage import RepositoryWriterLock, default_state_root


class PlatformContractTests(unittest.TestCase):
    def test_freshness_requires_exact_repository_and_complete_run_vector(self) -> None:
        oracle = ExpectedFreshnessOracle(
            "repo-1", "catalog-1", {"run-1": "head-1", "run-2": "head-2"}
        )
        self.assertTrue(
            oracle.verify(
                "repo-1",
                "catalog-1",
                {"run-1": "head-1", "run-2": "head-2"},
            )
        )
        self.assertFalse(
            oracle.verify("repo-1", "catalog-1", {"run-1": "head-1"})
        )
        self.assertFalse(
            oracle.verify(
                "repo-2",
                "catalog-1",
                {"run-1": "head-1", "run-2": "head-2"},
            )
        )

    def test_cli_capabilities_disclose_unavailable_real_effects(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            result = main(["--repository-id", "repo-1", "capabilities"])
        self.assertEqual(result, 0)
        self.assertIn('"external_io": false', output.getvalue())
        self.assertIn('"real_adapters": false', output.getvalue())

    def test_cli_status_does_not_create_state(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            output = io.StringIO()
            with redirect_stdout(output):
                result = main(
                    [
                        "--repository-id",
                        "repo-1",
                        "status",
                    ]
                )
            self.assertEqual(result, 0)
            self.assertIn('"initialized": false', output.getvalue())
            self.assertEqual(list(root.iterdir()), [])

    def test_state_root_uses_repository_identity_not_checkout_name(self) -> None:
        if sys.platform == "win32":
            with patch.dict(os.environ, {"LOCALAPPDATA": r"C:\State"}):
                first = default_state_root("repository-a")
                second = default_state_root("repository-b")
        else:
            with patch.dict(os.environ, {"XDG_STATE_HOME": "/tmp/state"}):
                first = default_state_root("repository-a")
                second = default_state_root("repository-b")
        self.assertNotEqual(first, second)
        self.assertNotIn("repository-a", str(first))

    def test_t21_second_process_cannot_take_writer_lock(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            state_root = Path(temporary_directory)
            script = (
                "from pathlib import Path; "
                "from tools.aegis_delivery_control.storage import RepositoryWriterLock; "
                f"lock=RepositoryWriterLock(Path({str(state_root)!r})); "
                "lock.__enter__()"
            )
            with RepositoryWriterLock(state_root):
                result = subprocess.run(
                    [sys.executable, "-c", script],
                    cwd=Path(__file__).parents[3],
                    capture_output=True,
                    text=True,
                    check=False,
                )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("repository writer lock is unavailable", result.stderr)
            self.assertTrue((state_root / "writer.lock").exists())

    def test_lock_can_be_reacquired_without_deleting_lock_object(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            state_root = Path(temporary_directory)
            with RepositoryWriterLock(state_root):
                lock_path = state_root / "writer.lock"
                self.assertTrue(lock_path.exists())
            with RepositoryWriterLock(state_root):
                self.assertTrue(lock_path.exists())


if __name__ == "__main__":
    unittest.main()