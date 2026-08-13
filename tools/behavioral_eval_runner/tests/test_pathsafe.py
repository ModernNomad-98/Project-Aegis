"""Strict path-safety validator (shared by materialize + evidence)."""

from __future__ import annotations

import os
import tempfile
import unittest

from tools.behavioral_eval_runner.pathsafe import (
    UnsafePathError,
    normalize_relative_path,
    refuse_reparse_chain,
    safe_join,
)


class TestNormalizeRelativePath(unittest.TestCase):
    def test_accepts_ordinary_relative_paths(self) -> None:
        for path in ("a/b.txt", "SKILL.md", "references/guide.md", "a\\b\\c.md"):
            self.assertTrue(normalize_relative_path(path))

    def test_rejects_traversal_absolute_and_drive(self) -> None:
        for path in ("../x", "a/../../x", "/abs", "\\abs", "C:/x", "c:x"):
            with self.assertRaises(UnsafePathError, msg=path):
                normalize_relative_path(path)

    def test_rejects_alternate_data_stream_marker(self) -> None:
        with self.assertRaises(UnsafePathError):
            normalize_relative_path("notes:hidden")
        with self.assertRaises(UnsafePathError):
            normalize_relative_path("dir/file.txt:stream")

    def test_rejects_trailing_dot_or_space(self) -> None:
        for path in ("a ", "a.", "dir/file ", "dir/file."):
            with self.assertRaises(UnsafePathError, msg=path):
                normalize_relative_path(path)

    def test_rejects_windows_device_names(self) -> None:
        for path in ("nul", "CON", "com1", "LPT9.txt", "dir/aux"):
            with self.assertRaises(UnsafePathError, msg=path):
                normalize_relative_path(path)

    def test_rejects_empty(self) -> None:
        for path in ("", ".", "a/./b"):
            with self.assertRaises(UnsafePathError):
                normalize_relative_path(path)


class TestSafeJoin(unittest.TestCase):
    def test_join_stays_under_root(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            joined = safe_join(root, "a/b.txt")
            self.assertTrue(
                os.path.commonpath([os.path.realpath(root), joined])
                == os.path.realpath(root)
            )

    def test_join_refuses_escape(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(UnsafePathError):
                safe_join(root, "../escape.txt")


class TestReparseChain(unittest.TestCase):
    def test_clean_chain_passes(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            target = os.path.join(root, "sub", "file.txt")
            refuse_reparse_chain(target, root)  # no reparse point => no raise


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
