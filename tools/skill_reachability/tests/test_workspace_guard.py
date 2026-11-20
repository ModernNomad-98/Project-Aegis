"""Fixture tests for the issue #1140 workspace-mutation guard.

Every fixture tree is built under a temporary directory and never inside the
repository; the planted deleting test deletes a file inside its own temporary
workspace, which is the proof issue #1140 requires: the guard must fail when a
test run deletes a workspace file.

Run:
    python -P -m unittest discover -s tools/skill_reachability/tests -p 'test_*.py' -v
"""
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
GUARD = REPO_ROOT / "tools" / "skill_reachability" / "tests" / "workspace_guard.py"


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def make_workspace(root):
    """Build a temporary workspace with a tracked-like and an untracked file."""
    write(root / "fixture" / "tracked.txt", "keep me\n")
    write(root / "untracked-notes.md", "untracked but present\n")


def plant(test_root, name, body):
    """Write a planted test/command script under the temporary test root."""
    return write(test_root / name, "import pathlib\nimport sys\n\n" + body)


class GuardCliTests(unittest.TestCase):
    def run_guard(self, test_root, *arguments):
        return subprocess.run(
            [sys.executable, "-P", str(GUARD)] + list(arguments),
            capture_output=True, text=True,
            env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))

    def test_planted_deleting_test_is_caught(self):
        """Issue #1140 proof: a test deleting a workspace file must fail."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            make_workspace(workspace)
            planted = plant(
                root, "planted_deleting_test.py",
                "root = pathlib.Path(sys.argv[1])\n"
                "(root / 'fixture' / 'tracked.txt').unlink()\n")
            result = self.run_guard(tmp, "--tree", str(workspace), "--",
                                    sys.executable, "-P", str(planted), str(workspace))
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("CHANGE REMOVED fixture/tracked.txt", result.stdout)
            self.assertIn("workspace-guard: FAIL", result.stdout)

    def test_clean_run_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            make_workspace(workspace)
            result = self.run_guard(tmp, "--tree", str(workspace), "--",
                                    sys.executable, "-P", "-c", "print('noop')")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("workspace-guard: PASS", result.stdout)
            self.assertIn("changes=0", result.stdout)

    def test_untracked_workspace_file_deletion_is_caught(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            make_workspace(workspace)
            planted = plant(
                root, "delete_untracked.py",
                "root = pathlib.Path(sys.argv[1])\n"
                "(root / 'untracked-notes.md').unlink()\n")
            result = self.run_guard(tmp, "--tree", str(workspace), "--",
                                    sys.executable, "-P", str(planted), str(workspace))
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("CHANGE REMOVED untracked-notes.md", result.stdout)

    def test_added_workspace_file_is_caught(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            make_workspace(workspace)
            planted = plant(
                root, "add_file.py",
                "root = pathlib.Path(sys.argv[1])\n"
                "(root / 'added.txt').write_text('new', encoding='utf-8')\n")
            result = self.run_guard(tmp, "--tree", str(workspace), "--",
                                    sys.executable, "-P", str(planted), str(workspace))
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("CHANGE ADDED added.txt", result.stdout)

    def test_modified_workspace_file_is_caught(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            make_workspace(workspace)
            planted = plant(
                root, "modify_file.py",
                "root = pathlib.Path(sys.argv[1])\n"
                "path = root / 'fixture' / 'tracked.txt'\n"
                "path.write_text(path.read_text(encoding='utf-8') + 'x', encoding='utf-8')\n")
            result = self.run_guard(tmp, "--tree", str(workspace), "--",
                                    sys.executable, "-P", str(planted), str(workspace))
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("CHANGE MODIFIED fixture/tracked.txt", result.stdout)

    def test_non_zero_command_fails_with_unchanged_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            make_workspace(workspace)
            result = self.run_guard(tmp, "--tree", str(workspace), "--",
                                    sys.executable, "-P", "-c", "raise SystemExit(3)")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("changes=0", result.stdout)
            self.assertIn("command_exit=3", result.stdout)

    def test_git_metadata_is_the_only_excluded_entry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            make_workspace(workspace)
            write(workspace / ".git" / "HEAD", "ref: refs/heads/main\n")
            planted = plant(
                root, "touch_git_metadata.py",
                "root = pathlib.Path(sys.argv[1])\n"
                "(root / '.git' / 'HEAD').write_text('ref: refs/heads/other\\n', encoding='utf-8')\n")
            result = self.run_guard(tmp, "--tree", str(workspace), "--",
                                    sys.executable, "-P", str(planted), str(workspace))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("workspace-guard: PASS", result.stdout)

    def test_missing_tree_is_a_usage_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "not-a-tree"
            result = self.run_guard(tmp, "--tree", str(missing))
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("tree is not a directory", result.stderr)

    def test_empty_command_after_separator_is_a_usage_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            make_workspace(workspace)
            result = self.run_guard(tmp, "--tree", str(workspace), "--")
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("no command after --", result.stderr)

    def test_default_tree_is_the_checkout_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_guard(tmp, "--",
                                    sys.executable, "-P", "-c", "print('noop')")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("tree=" + str(REPO_ROOT), result.stdout)
            self.assertIn("changes=0", result.stdout)


if __name__ == "__main__":
    unittest.main()
