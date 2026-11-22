"""Tests for Aegis Adopt v1 (standard-library unittest).

Every test works in a temporary directory and a synthetic Aegis checkout; none
reads the real checkout, the network or any credential.
"""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
import re
import stat
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.aegis_adopt import PROJECT_SCHEMA, __version__
from tools.aegis_adopt import cli
from tools.aegis_adopt.cli import BLOCK, BLOCK_BEGIN, BLOCK_END, main

SHA = re.compile(r"^[0-9a-f]{40}$")
WRITTEN = (
    ".aegis/project.json",
    ".aegis/START-HERE.md",
    ".aegis/bin/aegis-run",
    ".aegis/bin/aegis-run.cmd",
    "AGENTS.md",
    "CLAUDE.md",
)


def run_cli(*argv: str) -> tuple[int, str, str]:
    stdout, stderr = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        try:
            code = main(list(argv))
        except SystemExit as exc:
            code = int(exc.code or 0)
    return code, stdout.getvalue(), stderr.getvalue()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


class AdoptTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        self.repo = (self.root / "consumer repo").resolve()
        self.repo.mkdir()
        self.aegis = (self.root / "aegis checkout").resolve()
        run_module = self.aegis / "tools" / "aegis_run" / "__main__.py"
        run_module.parent.mkdir(parents=True)
        (run_module.parent / "__init__.py").write_text(
            '__version__ = "1.1.0"\n', encoding="utf-8"
        )
        run_module.write_text("print('aegis_run 1.1.0')\n", encoding="utf-8")

    # -- helpers --------------------------------------------------------

    def adopt(self, *extra: str) -> tuple[int, str, str]:
        return run_cli(
            "adopt",
            "--repo",
            str(self.repo),
            "--aegis-path",
            str(self.aegis),
            *extra,
        )

    def doctor(self) -> tuple[int, str, str]:
        return run_cli("doctor", "--repo", str(self.repo))

    def unadopt(self, *extra: str) -> tuple[int, str, str]:
        return run_cli("unadopt", "--repo", str(self.repo), *extra)

    def project(self) -> dict:
        return json.loads((self.repo / ".aegis/project.json").read_text(encoding="utf-8"))

    def read(self, relative: str) -> str:
        return (self.repo / relative).read_text(encoding="utf-8")

    def assert_no_traceback(self, *streams: str) -> None:
        for stream in streams:
            self.assertNotIn("Traceback (most recent call last)", stream)

    def _remove_link(self, path: Path) -> None:
        try:
            if path.is_symlink():
                path.unlink()
            elif getattr(path, "is_junction", lambda: False)():
                os.rmdir(path)
        except OSError:
            pass

    def _remove_file(self, path: Path) -> None:
        try:
            path.unlink()
        except OSError:
            pass

    # -- adopt ----------------------------------------------------------

    def test_fresh_adopt_creates_bootstrap_and_doctor_passes(self) -> None:
        code, out, err = self.adopt()
        self.assertEqual(code, 0, err)
        self.assertIn("adopted", out)
        for relative in WRITTEN:
            self.assertTrue((self.repo / relative).is_file(), relative)

        project = self.project()
        self.assertEqual(project["schema"], PROJECT_SCHEMA)
        self.assertTrue(project["adopted_at"].endswith("Z"))
        self.assertEqual(project["aegis_path"], str(self.aegis))
        self.assertTrue(Path(project["aegis_path"]).is_absolute())
        self.assertEqual(project["start_here"], ".aegis/START-HERE.md")
        self.assertEqual(
            project["hosts"], {"cursor": False, "copilot": False, "gemini": False}
        )
        self.assertIsNone(project["aegis_commit"])
        self.assertEqual(set(project["wrapper_sha256"]), {"sh", "cmd"})
        for key, relative in (
            ("sh", ".aegis/bin/aegis-run"),
            ("cmd", ".aegis/bin/aegis-run.cmd"),
        ):
            self.assertEqual(
                project["wrapper_sha256"][key],
                hashlib.sha256((self.repo / relative).read_bytes()).hexdigest(),
            )

        start_here = self.read(".aegis/START-HERE.md")
        self.assertIn("START HERE", start_here)
        self.assertIn(".aegis/bin/aegis-run", start_here)
        self.assertIn(r".aegis\bin\aegis-run.cmd", start_here)
        self.assertNotIn(chr(8), start_here)
        self.assertIn("confirmed project-state writes", start_here)

        for relative in ("AGENTS.md", "CLAUDE.md"):
            text = self.read(relative)
            self.assertIn("Aegis bootstrap", text)
            self.assertIn("before any task", text)
            self.assertIn("confirmed project-state writes", text)
            self.assertIn(".aegis/bin/aegis-run", text)
            self.assertEqual(text.count(BLOCK_BEGIN), 1)
            self.assertIn(BLOCK, text)
            self.assertIsNone(cli._block_problem(text))

        code, out, err = self.doctor()
        self.assertEqual(code, 0, err)
        self.assertIn("PASS", out)
        self.assertNotIn("FAIL", out)
        self.assertIn("module:", out)
        self.assertIn("printed aegis_run", out)

    def test_default_adopt_creates_zero_optional_host_files(self) -> None:
        code, _out, err = self.adopt()
        self.assertEqual(code, 0, err)
        self.assertFalse((self.repo / ".cursor").exists())
        self.assertFalse((self.repo / ".github").exists())
        self.assertFalse((self.repo / "GEMINI.md").exists())

    def test_second_adopt_is_byte_idempotent_and_has_no_duplicate_block(self) -> None:
        self.assertEqual(self.adopt()[0], 0)
        before = {relative: (self.repo / relative).read_bytes() for relative in WRITTEN}
        adopted_at = self.project()["adopted_at"]

        code, _out, err = self.adopt()
        self.assertEqual(code, 0, err)
        after = {relative: (self.repo / relative).read_bytes() for relative in WRITTEN}
        self.assertEqual(before, after)
        self.assertEqual(adopted_at, self.project()["adopted_at"])
        for relative in ("AGENTS.md", "CLAUDE.md"):
            self.assertEqual(self.read(relative).count(BLOCK_BEGIN), 1)
            self.assertEqual(self.read(relative).count(BLOCK_END), 1)

    def test_wrapper_sets_pythonpath_and_runs_python_p(self) -> None:
        self.assertEqual(self.adopt()[0], 0)
        sh = self.read(".aegis/bin/aegis-run")
        self.assertTrue(sh.startswith("#!/bin/sh"))
        self.assertIn("PYTHONPATH='%s'" % self.aegis.as_posix(), sh)
        self.assertIn(self.aegis.as_posix(), sh)
        self.assertIn("python -P -m tools.aegis_run", sh)
        self.assertIn('"$@"', sh)

        cmd = self.read(".aegis/bin/aegis-run.cmd")
        self.assertIn("PYTHONPATH=", cmd)
        self.assertIn(str(self.aegis), cmd)
        self.assertIn("python -P -m tools.aegis_run", cmd)
        self.assertIn("%*", cmd)

    def test_cursor_flag_creates_rule_and_records_it(self) -> None:
        code, _out, err = self.adopt("--cursor")
        self.assertEqual(code, 0, err)
        rule = self.repo / ".cursor/rules/aegis.mdc"
        self.assertTrue(rule.is_file())
        text = rule.read_text(encoding="utf-8")
        self.assertEqual(text.count(BLOCK_BEGIN), 1)
        self.assertIn(BLOCK, text)
        self.assertEqual(
            self.project()["hosts"], {"cursor": True, "copilot": False, "gemini": False}
        )
        self.assertFalse((self.repo / "GEMINI.md").exists())
        self.assertFalse((self.repo / ".github").exists())
        self.assertEqual(self.doctor()[0], 0)

    def test_copilot_and_gemini_flags_create_only_their_files(self) -> None:
        code, _out, err = self.adopt("--copilot", "--gemini")
        self.assertEqual(code, 0, err)
        self.assertTrue((self.repo / ".github/copilot-instructions.md").is_file())
        self.assertTrue((self.repo / "GEMINI.md").is_file())
        self.assertFalse((self.repo / ".cursor").exists())
        self.assertEqual(
            self.project()["hosts"], {"cursor": False, "copilot": True, "gemini": True}
        )
        self.assertEqual(self.doctor()[0], 0)

    def test_existing_agents_content_is_preserved_and_only_block_replaced(self) -> None:
        prefix = "# House rules\n\nKeep this byte-for-byte.\n"
        agents = self.repo / "AGENTS.md"
        write_text(agents, prefix)

        self.assertEqual(self.adopt()[0], 0)
        text = agents.read_text(encoding="utf-8")
        self.assertTrue(text.startswith(prefix))
        self.assertEqual(text.count(BLOCK_BEGIN), 1)

        tampered = text.replace("Keep the run record", "TAMPERED")
        tampered += "\nTAIL-MARKER\n"
        write_text(agents, tampered)
        self.assertEqual(self.adopt()[0], 0)

        after = agents.read_text(encoding="utf-8")
        self.assertTrue(after.startswith(prefix))
        self.assertNotIn("TAMPERED", after)
        self.assertTrue(after.endswith("TAIL-MARKER\n"))
        self.assertEqual(after.count(BLOCK_BEGIN), 1)
        self.assertIn(BLOCK, after)

    def test_crlf_agents_outside_block_is_preserved_and_block_uses_crlf(self) -> None:
        prefix = b"# House rules\r\n\r\nKeep CRLF.\r\nKeep mixed line.\n"
        agents = self.repo / "AGENTS.md"
        agents.write_bytes(prefix)

        self.assertEqual(self.adopt()[0], 0)
        data = agents.read_bytes()
        begin_marker = BLOCK_BEGIN.encode("utf-8")
        end_marker = BLOCK_END.encode("utf-8")
        begin = data.index(begin_marker)
        end = data.index(end_marker) + len(end_marker)
        block = data[begin:end]

        self.assertEqual(data[:begin], prefix)
        self.assertEqual(data[end:], b"\r\n")
        self.assertIn(b"\r\n", block)
        self.assertNotIn(b"\n", block.replace(b"\r\n", b""))
        self.assertNotIn(b"\r", block.replace(b"\r\n", b""))

        tail = b"\r\nTAIL\r\n"
        agents.write_bytes(data + tail)
        self.assertEqual(self.adopt()[0], 0)
        second = agents.read_bytes()
        self.assertEqual(second, data + tail)
        self.assertEqual(self.adopt()[0], 0)
        self.assertEqual(agents.read_bytes(), second)
        self.assertEqual(self.doctor()[0], 0)

    def test_crlf_block_replacement_preserves_surrounding_bytes(self) -> None:
        prefix = b"# Claude rules\r\n\r\n"
        suffix = b"\r\n\r\nTAIL\r\n"
        tampered = (
            BLOCK.replace("\n", "\r\n")
            .replace("Keep the run record", "TAMPERED")
            .encode("utf-8")
        )
        claude = self.repo / "CLAUDE.md"
        claude.write_bytes(prefix + tampered + suffix)

        self.assertEqual(self.adopt()[0], 0)
        data = claude.read_bytes()
        self.assertTrue(data.startswith(prefix))
        self.assertTrue(data.endswith(suffix))
        self.assertNotIn(b"TAMPERED", data)
        self.assertIn(BLOCK.replace("\n", "\r\n").encode("utf-8"), data)
        self.assertEqual(self.doctor()[0], 0)
        self.assertEqual(self.adopt()[0], 0)
        self.assertEqual(claude.read_bytes(), data)

    def test_adopt_rejects_non_utf8_agents_before_writing(self) -> None:
        original = b"\xff\xfe# title\n"
        agents = self.repo / "AGENTS.md"
        agents.write_bytes(original)

        code, _out, err = self.adopt()
        self.assertEqual(code, 1)
        self.assertIn("not valid UTF-8", err)
        self.assert_no_traceback(err)
        self.assertEqual(agents.read_bytes(), original)
        self.assertFalse((self.repo / ".aegis").exists())
        self.assertFalse((self.repo / "CLAUDE.md").exists())

    def test_adopt_rejects_non_utf8_host_file_before_writing(self) -> None:
        original = b"\xff\xfe# rule\n"
        rule = self.repo / ".cursor/rules/aegis.mdc"
        rule.parent.mkdir(parents=True)
        rule.write_bytes(original)

        code, _out, err = self.adopt("--cursor")
        self.assertEqual(code, 1)
        self.assertIn("not valid UTF-8", err)
        self.assert_no_traceback(err)
        self.assertEqual(rule.read_bytes(), original)
        self.assertFalse((self.repo / ".aegis").exists())

    def test_adopt_rejects_aegis_link_outside_repository(self) -> None:
        outside = (self.root / "outside-aegis").resolve()
        outside.mkdir()
        agents = self.repo / "AGENTS.md"
        original = b"# Keep these bytes\n"
        agents.write_bytes(original)
        link = self.repo / ".aegis"
        self.addCleanup(self._remove_link, link)

        if os.name == "nt":
            created = subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(link), str(outside)],
                capture_output=True,
                text=True,
            )
            if created.returncode != 0:
                self.skipTest(
                    "junction creation unavailable: %s" % created.stderr.strip()
                )
        else:
            try:
                link.symlink_to(outside, target_is_directory=True)
            except OSError as exc:
                self.skipTest("symlink creation unavailable: %s" % exc)

        code, _out, err = self.adopt()
        self.assertEqual(code, 1)
        self.assertIn("symbolic link or junction", err)
        self.assert_no_traceback(err)
        self.assertEqual(agents.read_bytes(), original)
        self.assertEqual(list(outside.iterdir()), [])

    def test_adopt_rejects_aegis_regular_file(self) -> None:
        agents = self.repo / "AGENTS.md"
        original = b"# Keep these bytes\n"
        agents.write_bytes(original)
        aegis = self.repo / ".aegis"
        aegis.write_bytes(b"not a directory\n")

        code, _out, err = self.adopt()
        self.assertEqual(code, 1)
        self.assertIn(".aegis", err)
        self.assertIn("not a directory", err)
        self.assert_no_traceback(err)
        self.assertEqual(aegis.read_bytes(), b"not a directory\n")
        self.assertEqual(agents.read_bytes(), original)

    def test_adopt_rejects_regular_file_at_host_directory(self) -> None:
        agents = self.repo / "AGENTS.md"
        original = b"# Keep these bytes\n"
        agents.write_bytes(original)

        for flag, parent in (("--cursor", ".cursor"), ("--copilot", ".github")):
            with self.subTest(flag=flag):
                blocker = self.repo / parent
                blocker.write_bytes(b"not a directory\n")
                code, _out, err = self.adopt(flag)
                self.assertEqual(code, 1)
                self.assertIn(parent, err)
                self.assertIn("not a directory", err)
                self.assert_no_traceback(err)
                self.assertFalse((self.repo / ".aegis").exists())
                self.assertEqual(agents.read_bytes(), original)
                blocker.unlink()

    def test_adopt_rejects_agents_link_outside_repository(self) -> None:
        outside = (self.root / "outside-agents").resolve()
        outside.mkdir()
        agents = self.repo / "AGENTS.md"
        self.addCleanup(self._remove_link, agents)

        if os.name == "nt":
            created = subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(agents), str(outside)],
                capture_output=True,
                text=True,
            )
            if created.returncode != 0:
                self.skipTest(
                    "junction creation unavailable: %s" % created.stderr.strip()
                )
        else:
            try:
                agents.symlink_to(outside, target_is_directory=True)
            except OSError as exc:
                self.skipTest("symlink creation unavailable: %s" % exc)

        code, _out, err = self.adopt()
        self.assertEqual(code, 1)
        self.assertIn("symbolic link or junction", err)
        self.assert_no_traceback(err)
        self.assertEqual(list(outside.iterdir()), [])
        self.assertFalse((self.repo / ".aegis").exists())

    def test_adopt_ignores_predictable_wrapper_tmp_link(self) -> None:
        outside = (self.root / "outside-temp-target.txt").resolve()
        outside.write_bytes(b"outside original\n")
        bin_dir = self.repo / ".aegis/bin"
        bin_dir.mkdir(parents=True)
        trap = bin_dir / "aegis-run.tmp"

        if os.name == "nt":
            try:
                os.link(outside, trap)
            except OSError as exc:
                self.skipTest("hardlink creation unavailable: %s" % exc)
        else:
            try:
                trap.symlink_to(outside)
            except OSError as exc:
                self.skipTest("symlink creation unavailable: %s" % exc)
        self.addCleanup(self._remove_file, trap)

        code, _out, err = self.adopt()
        self.assertEqual(code, 0, err)
        self.assertEqual(outside.read_bytes(), b"outside original\n")
        self.assertTrue(trap.exists())
        self.assertEqual(list(self.repo.rglob(".aegis-*.tmp")), [])
        self.assertEqual(self.doctor()[0], 0)

    def test_adopt_rolls_back_when_a_write_fails(self) -> None:
        agents = self.repo / "AGENTS.md"
        claude = self.repo / "CLAUDE.md"
        agents_original = b"# Agents original\r\nKeep.\r\n"
        claude_original = b"# Claude original\nKeep.\n"
        agents.write_bytes(agents_original)
        claude.write_bytes(claude_original)
        agents_mode = stat.S_IMODE(agents.stat().st_mode)
        claude_mode = stat.S_IMODE(claude.stat().st_mode)

        real_write = cli._atomic_write

        def fail_on_project(path, text, newline="\n", mode=0o644):
            if Path(path).name == "project.json":
                raise OSError("injected write failure")
            return real_write(path, text, newline, mode)

        with mock.patch.object(cli, "_atomic_write", side_effect=fail_on_project):
            code, _out, err = self.adopt()
        self.assertEqual(code, 1)
        self.assertIn("rolled back", err)
        self.assertIn("injected write failure", err)
        self.assert_no_traceback(err)
        self.assertFalse((self.repo / ".aegis").exists())
        self.assertEqual(agents.read_bytes(), agents_original)
        self.assertEqual(claude.read_bytes(), claude_original)
        self.assertEqual(stat.S_IMODE(agents.stat().st_mode), agents_mode)
        self.assertEqual(stat.S_IMODE(claude.stat().st_mode), claude_mode)

    def test_adopt_rolls_back_on_keyboard_interrupt(self) -> None:
        agents = self.repo / "AGENTS.md"
        claude = self.repo / "CLAUDE.md"
        agents_original = b"# Agents original\r\nKeep.\r\n"
        claude_original = b"# Claude original\nKeep.\n"
        agents.write_bytes(agents_original)
        claude.write_bytes(claude_original)
        agents_mode = stat.S_IMODE(agents.stat().st_mode)
        claude_mode = stat.S_IMODE(claude.stat().st_mode)

        real_write = cli._atomic_write

        def interrupt_on_project(path, text, newline="\n", mode=0o644):
            if Path(path).name == "project.json":
                raise KeyboardInterrupt()
            return real_write(path, text, newline, mode)

        with mock.patch.object(cli, "_atomic_write", side_effect=interrupt_on_project):
            with self.assertRaises(KeyboardInterrupt):
                self.adopt()

        self.assertFalse((self.repo / ".aegis").exists())
        self.assertEqual(agents.read_bytes(), agents_original)
        self.assertEqual(claude.read_bytes(), claude_original)
        self.assertEqual(stat.S_IMODE(agents.stat().st_mode), agents_mode)
        self.assertEqual(stat.S_IMODE(claude.stat().st_mode), claude_mode)

    def test_adopt_rejects_read_only_agents_before_writing(self) -> None:
        agents = self.repo / "AGENTS.md"
        original = b"# Read-only AGENTS\r\nKeep.\r\n"
        agents.write_bytes(original)
        original_mode = stat.S_IMODE(agents.stat().st_mode)
        os.chmod(agents, 0o444)
        self.addCleanup(os.chmod, agents, original_mode)

        code, _out, err = self.adopt()
        self.assertEqual(code, 1)
        self.assertIn("read-only", err)
        self.assert_no_traceback(err)
        self.assertFalse((self.repo / ".aegis").exists())
        self.assertEqual(agents.read_bytes(), original)
        self.assertEqual(stat.S_IMODE(agents.stat().st_mode), 0o444)

    def test_existing_agents_mode_is_preserved(self) -> None:
        agents = self.repo / "AGENTS.md"
        agents.write_bytes(b"# Agents original\n")
        os.chmod(agents, 0o644)
        before = stat.S_IMODE(agents.stat().st_mode)
        self.assertEqual(self.adopt()[0], 0)
        after = stat.S_IMODE(agents.stat().st_mode)
        self.assertEqual(after, before)
        if os.name != "nt":
            self.assertEqual(after, 0o644)

    def test_new_start_here_mode_is_0644(self) -> None:
        self.assertEqual(self.adopt()[0], 0)
        mode = stat.S_IMODE((self.repo / ".aegis/START-HERE.md").stat().st_mode)
        if os.name != "nt":
            self.assertEqual(mode, 0o644)
        else:
            # Windows represents writable files as 0o666; POSIX group/other bits
            # are not meaningful there.
            self.assertTrue(mode & 0o200)

    def test_sh_wrapper_mode_is_0755(self) -> None:
        self.assertEqual(self.adopt()[0], 0)
        wrapper = self.repo / ".aegis/bin/aegis-run"
        mode = stat.S_IMODE(wrapper.stat().st_mode)
        if os.name != "nt":
            self.assertEqual(mode, 0o755)
            self.assertTrue(mode & 0o111)
        else:
            # Windows has no POSIX execute bits; writable is the meaningful check.
            self.assertTrue(mode & 0o200)

    def test_second_adopt_preserves_modes(self) -> None:
        self.assertEqual(self.adopt()[0], 0)
        relatives = (
            "AGENTS.md",
            "CLAUDE.md",
            ".aegis/START-HERE.md",
            ".aegis/project.json",
            ".aegis/bin/aegis-run",
            ".aegis/bin/aegis-run.cmd",
        )
        before = {
            relative: stat.S_IMODE((self.repo / relative).stat().st_mode)
            for relative in relatives
        }
        self.assertEqual(self.adopt()[0], 0)
        after = {
            relative: stat.S_IMODE((self.repo / relative).stat().st_mode)
            for relative in relatives
        }
        self.assertEqual(after, before)

    def test_unadopt_restores_original_agents_bytes_exactly(self) -> None:
        agents_original = b"# Agents\r\n\r\nKeep no trailing newline"
        claude_original = b"# Claude\nKeep trailing\n"
        (self.repo / "AGENTS.md").write_bytes(agents_original)
        (self.repo / "CLAUDE.md").write_bytes(claude_original)
        self.assertEqual(self.adopt()[0], 0)
        self.assertIn(BLOCK_BEGIN.encode("utf-8"), (self.repo / "AGENTS.md").read_bytes())

        code, _out, err = self.unadopt()
        self.assertEqual(code, 0, err)
        self.assertEqual((self.repo / "AGENTS.md").read_bytes(), agents_original)
        self.assertEqual((self.repo / "CLAUDE.md").read_bytes(), claude_original)
        self.assertFalse((self.repo / ".aegis").exists())

    def test_unadopt_preserves_crlf_bytes(self) -> None:
        original = b"# CRLF rules\r\n\r\nKeep these bytes.\r\n"
        agents = self.repo / "AGENTS.md"
        agents.write_bytes(original)
        self.assertEqual(self.adopt()[0], 0)
        self.assertEqual(self.unadopt()[0], 0)
        self.assertEqual(agents.read_bytes(), original)
        self.assertIn(b"\r\n", agents.read_bytes())

    def test_second_unadopt_is_noop(self) -> None:
        agents = self.repo / "AGENTS.md"
        original = b"# Keep\n"
        agents.write_bytes(original)
        self.assertEqual(self.adopt()[0], 0)
        self.assertEqual(self.unadopt()[0], 0)
        before = agents.read_bytes()
        code, out, err = self.unadopt()
        self.assertEqual(code, 0, err)
        self.assertIn("already unadopted", out)
        self.assertEqual(agents.read_bytes(), before)
        self.assertFalse((self.repo / ".aegis").exists())

    def test_unadopt_refuses_unknown_aegis_file_unless_forced(self) -> None:
        agents = self.repo / "AGENTS.md"
        original = b"# Keep\n"
        agents.write_bytes(original)
        self.assertEqual(self.adopt()[0], 0)
        unknown = self.repo / ".aegis/unknown.txt"
        unknown.write_bytes(b"unknown\n")

        code, _out, err = self.unadopt()
        self.assertEqual(code, 1)
        self.assertIn("unknown", err)
        self.assertTrue((self.repo / ".aegis/project.json").exists())
        self.assertEqual(
            agents.read_bytes().count(BLOCK_BEGIN.encode("utf-8")), 1
        )

        code, out, err = self.unadopt("--force")
        self.assertEqual(code, 0, err)
        self.assertIn("unknown left", out)
        self.assertEqual(unknown.read_bytes(), b"unknown\n")
        self.assertFalse((self.repo / ".aegis/project.json").exists())
        self.assertEqual(agents.read_bytes().count(BLOCK_BEGIN.encode("utf-8")), 0)
        self.assertTrue((self.repo / ".aegis").is_dir())

    def test_unadopt_rejects_malformed_or_wrong_schema_project(self) -> None:
        agents = self.repo / "AGENTS.md"
        agents.write_bytes(b"# Keep\n")
        self.assertEqual(self.adopt()[0], 0)
        project_path = self.repo / ".aegis/project.json"
        original_project = project_path.read_bytes()
        with_block = agents.read_bytes()

        project_path.write_bytes(b"{not json")
        code, _out, err = self.unadopt()
        self.assertEqual(code, 1)
        self.assertIn("not valid JSON", err)
        self.assertEqual(agents.read_bytes(), with_block)

        data = json.loads(original_project)
        data["schema"] = "aegis.adopt/0"
        write_text(project_path, json.dumps(data, indent=2) + "\n")
        code, _out, err = self.unadopt()
        self.assertEqual(code, 1)
        self.assertIn("schema must be", err)
        self.assertEqual(agents.read_bytes(), with_block)

    def test_unadopt_force_with_missing_project_previews_and_removes_blocks(self) -> None:
        agents = self.repo / "AGENTS.md"
        agents.write_bytes(b"# Keep\n")
        self.assertEqual(self.adopt()[0], 0)
        (self.repo / ".aegis/project.json").unlink()
        with_block = agents.read_bytes()

        code, _out, err = self.unadopt()
        self.assertEqual(code, 1)
        self.assertIn("project.json is missing", err)
        self.assertEqual(agents.read_bytes(), with_block)

        code, out, err = self.unadopt("--force")
        self.assertEqual(code, 0, err)
        self.assertIn("preview:", out)
        self.assertEqual(agents.read_bytes().count(BLOCK_BEGIN.encode("utf-8")), 0)
        self.assertFalse((self.repo / ".aegis").exists())

    def test_unadopt_removes_recorded_optional_host_block(self) -> None:
        rule = self.repo / ".cursor/rules/aegis.mdc"
        original = b"# Cursor rule\nKeep.\n"
        rule.parent.mkdir(parents=True)
        rule.write_bytes(original)
        self.assertEqual(self.adopt("--cursor")[0], 0)
        self.assertIn(BLOCK_BEGIN.encode("utf-8"), rule.read_bytes())

        code, _out, err = self.unadopt()
        self.assertEqual(code, 0, err)
        self.assertEqual(rule.read_bytes(), original)
        self.assertFalse((self.repo / ".aegis").exists())

    def test_unadopt_removes_created_agents_and_claude(self) -> None:
        self.assertEqual(self.adopt()[0], 0)
        self.assertTrue((self.repo / "AGENTS.md").is_file())
        self.assertTrue((self.repo / "CLAUDE.md").is_file())

        code, _out, err = self.unadopt()
        self.assertEqual(code, 0, err)
        self.assertFalse((self.repo / "AGENTS.md").exists())
        self.assertFalse((self.repo / "CLAUDE.md").exists())
        self.assertFalse((self.repo / ".aegis").exists())

    def test_unadopt_removes_created_host_files_and_dirs(self) -> None:
        self.assertEqual(self.adopt("--cursor", "--copilot")[0], 0)
        self.assertTrue((self.repo / ".cursor/rules/aegis.mdc").is_file())
        self.assertTrue((self.repo / ".github/copilot-instructions.md").is_file())

        code, _out, err = self.unadopt()
        self.assertEqual(code, 0, err)
        self.assertFalse((self.repo / ".cursor/rules/aegis.mdc").exists())
        self.assertFalse((self.repo / ".github/copilot-instructions.md").exists())
        self.assertFalse((self.repo / ".cursor").exists())
        self.assertFalse((self.repo / ".github").exists())
        self.assertFalse((self.repo / ".aegis").exists())

    def test_unadopt_keeps_note_in_created_agents(self) -> None:
        agents = self.repo / "AGENTS.md"
        self.assertFalse(agents.exists())
        self.assertEqual(self.adopt()[0], 0)
        note = b"User note after adoption\n"
        agents.write_bytes(agents.read_bytes() + note)

        code, _out, err = self.unadopt()
        self.assertEqual(code, 0, err)
        self.assertTrue(agents.is_file())
        self.assertEqual(agents.read_bytes(), note)
        self.assertEqual(agents.read_bytes().count(BLOCK_BEGIN.encode("utf-8")), 0)
        self.assertFalse((self.repo / ".aegis").exists())

    def test_unadopt_keeps_note_after_existing_agents(self) -> None:
        agents = self.repo / "AGENTS.md"
        original = b"# Original\r\nKeep these bytes.\r\n"
        agents.write_bytes(original)
        self.assertEqual(self.adopt()[0], 0)
        note = b"User note after adoption\r\n"
        agents.write_bytes(agents.read_bytes() + note)

        code, _out, err = self.unadopt()
        self.assertEqual(code, 0, err)
        self.assertEqual(agents.read_bytes(), original + note)
        self.assertEqual(agents.read_bytes().count(BLOCK_BEGIN.encode("utf-8")), 0)
        self.assertFalse((self.repo / ".aegis").exists())

    # -- doctor failures -------------------------------------------------

    def test_doctor_fails_when_start_here_is_missing(self) -> None:
        self.assertEqual(self.adopt()[0], 0)
        (self.repo / ".aegis/START-HERE.md").unlink()
        code, out, err = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("FAIL", out)
        self.assertIn("START-HERE", out)
        self.assert_no_traceback(out, err)

    def test_doctor_fails_when_agents_block_is_missing(self) -> None:
        self.assertEqual(self.adopt()[0], 0)
        write_text(self.repo / "AGENTS.md", "# no block here\n")
        code, out, err = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("missing Aegis bootstrap block", out)
        self.assert_no_traceback(out, err)

    def test_doctor_fails_when_wrapper_is_missing(self) -> None:
        self.assertEqual(self.adopt()[0], 0)
        (self.repo / ".aegis/bin/aegis-run").unlink()
        code, out, err = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("missing .aegis/bin/aegis-run", out)
        self.assert_no_traceback(out, err)

    def test_doctor_fails_closed_on_missing_project(self) -> None:
        code, out, err = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("missing .aegis/project.json", out)
        self.assert_no_traceback(out, err)

    def test_doctor_fails_closed_on_malformed_or_non_utf8_project(self) -> None:
        self.assertEqual(self.adopt()[0], 0)
        project = self.repo / ".aegis/project.json"

        project.write_bytes(b"{not json")
        code, out, err = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("not valid JSON", out)
        self.assert_no_traceback(out, err)

        project.write_bytes(b"\xff\xfe\x00")
        code, out, err = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("UTF-8", out)
        self.assert_no_traceback(out, err)

    def test_doctor_fails_closed_on_bad_repository_arguments(self) -> None:
        code, _out, err = run_cli("doctor")
        self.assertEqual(code, 1)
        self.assertIn("required", err)
        self.assert_no_traceback(err)

        code, out, err = run_cli("doctor", "--repo", str(self.repo / "absent"))
        self.assertEqual(code, 1)
        self.assertIn("FAIL", out)
        self.assertIn("repository not found", out)
        self.assert_no_traceback(out, err)

        code, out, err = run_cli("doctor", "--repo", "")
        self.assertEqual(code, 1)
        self.assertIn("must not be empty", out)
        self.assert_no_traceback(out, err)

    def test_doctor_fails_when_project_is_a_directory(self) -> None:
        self.assertEqual(self.adopt()[0], 0)
        project = self.repo / ".aegis/project.json"
        project.unlink()
        project.mkdir()
        code, out, err = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("cannot read .aegis/project.json", out)
        self.assert_no_traceback(out, err)

    def test_doctor_fails_on_wrong_schema(self) -> None:
        self.assertEqual(self.adopt()[0], 0)
        data = self.project()
        data["schema"] = "aegis.adopt/0"
        write_text(
            self.repo / ".aegis/project.json",
            json.dumps(data, sort_keys=True, indent=2) + "\n",
        )
        code, out, err = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("schema must be aegis.adopt/1", out)
        self.assert_no_traceback(out, err)

    def test_doctor_fails_when_recorded_host_file_is_missing(self) -> None:
        self.assertEqual(self.adopt("--cursor")[0], 0)
        (self.repo / ".cursor/rules/aegis.mdc").unlink()
        code, out, err = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn(".cursor/rules/aegis.mdc", out)
        self.assert_no_traceback(out, err)

    def test_doctor_fails_when_wrapper_is_not_template(self) -> None:
        self.assertEqual(self.adopt()[0], 0)
        wrapper = self.repo / ".aegis/bin/aegis-run"
        write_text(
            wrapper,
            wrapper.read_text(encoding="utf-8").replace(
                "python -P -m tools.aegis_run", "python -m tools.aegis_run"
            ),
        )
        code, out, err = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("sha256", out)
        self.assert_no_traceback(out, err)

    def test_doctor_fails_on_edited_sh_wrapper(self) -> None:
        self.assertEqual(self.adopt()[0], 0)
        wrapper = self.repo / ".aegis/bin/aegis-run"
        text = wrapper.read_text(encoding="utf-8")
        text = text.replace(
            "PYTHONPATH='%s'" % self.aegis.as_posix(), "PYTHONPATH='/wrong'"
        )
        write_text(wrapper, text)
        code, out, err = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("sha256", out)
        self.assert_no_traceback(out, err)

    def test_doctor_fails_on_edited_cmd_wrapper(self) -> None:
        self.assertEqual(self.adopt()[0], 0)
        wrapper = self.repo / ".aegis/bin/aegis-run.cmd"
        text = wrapper.read_text(encoding="utf-8")
        text = text.replace(
            'set "PYTHONPATH=%AEGIS_PATH%"', 'set "PYTHONPATH=C:/wrong"'
        )
        write_text(wrapper, text)
        code, out, err = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("sha256", out)
        self.assert_no_traceback(out, err)

    def test_doctor_fails_on_noop_wrapper_with_exit_and_echo(self) -> None:
        self.assertEqual(self.adopt()[0], 0)
        write_text(
            self.repo / ".aegis/bin/aegis-run",
            "#!/bin/sh\nexit 0\necho aegis_run\n",
        )
        code, out, err = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("sha256", out)
        self.assert_no_traceback(out, err)

    def test_doctor_fails_on_extra_wrapper_line_without_side_effect(self) -> None:
        self.assertEqual(self.adopt()[0], 0)
        side_effect = self.repo / "side-effect.txt"
        sh_wrapper = self.repo / ".aegis/bin/aegis-run"
        cmd_wrapper = self.repo / ".aegis/bin/aegis-run.cmd"
        write_text(
            sh_wrapper,
            sh_wrapper.read_text(encoding="utf-8")
            + "\necho sideeffect > '%s'\n" % side_effect.as_posix(),
        )
        write_text(
            cmd_wrapper,
            cmd_wrapper.read_text(encoding="utf-8")
            + '\necho sideeffect > "%s"\n' % side_effect,
        )
        code, out, err = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("sha256", out)
        self.assertFalse(side_effect.exists())
        self.assert_no_traceback(out, err)

    def test_doctor_fails_when_required_strings_are_only_comments(self) -> None:
        self.assertEqual(self.adopt()[0], 0)
        posix = self.aegis.as_posix()
        native = str(self.aegis)
        write_text(
            self.repo / ".aegis/bin/aegis-run",
            f"""#!/bin/sh
# AEGIS_PATH={posix}
# PYTHONPATH={posix}
# exec python -P -m tools.aegis_run "$@"
exit 0
""",
        )
        write_text(
            self.repo / ".aegis/bin/aegis-run.cmd",
            f"""@echo off
rem set "AEGIS_PATH={native}"
rem set "PYTHONPATH=%AEGIS_PATH%"
rem python -P -m tools.aegis_run %*
exit /b 0
""",
        )
        code, out, err = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("sha256", out)
        self.assert_no_traceback(out, err)

    def test_doctor_fails_when_run_command_is_only_echoed(self) -> None:
        self.assertEqual(self.adopt()[0], 0)
        wrapper = self.repo / ".aegis/bin/aegis-run"
        text = wrapper.read_text(encoding="utf-8")
        text = text.replace(
            'exec python -P -m tools.aegis_run "$@"',
            'echo "python -P -m tools.aegis_run"',
        )
        write_text(wrapper, text)
        code, out, err = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("sha256", out)
        self.assert_no_traceback(out, err)

    def test_doctor_fails_when_recorded_checkout_module_is_missing(self) -> None:
        self.assertEqual(self.adopt()[0], 0)
        (self.aegis / "tools/aegis_run/__main__.py").unlink()
        code, out, err = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("no tools/aegis_run/__main__.py", out)
        self.assert_no_traceback(out, err)

    def test_doctor_fails_when_trusted_module_exits_nonzero(self) -> None:
        self.assertEqual(self.adopt()[0], 0)
        (self.aegis / "tools/aegis_run/__main__.py").write_text(
            "raise SystemExit(3)\n", encoding="utf-8"
        )
        code, out, err = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("--version exited 3", out)
        self.assert_no_traceback(out, err)

    def test_doctor_fails_when_trusted_module_prints_no_version(self) -> None:
        self.assertEqual(self.adopt()[0], 0)
        (self.aegis / "tools/aegis_run/__main__.py").write_text(
            "raise SystemExit(0)\n", encoding="utf-8"
        )
        code, out, err = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("did not print aegis_run", out)
        self.assert_no_traceback(out, err)

    def test_doctor_leaves_no_pycache(self) -> None:
        self.assertEqual(self.adopt()[0], 0)
        code, out, err = self.doctor()
        self.assertEqual(code, 0, err)
        self.assertFalse(list(self.aegis.rglob("__pycache__")))
        self.assertFalse(list(self.repo.rglob("__pycache__")))

    def test_doctor_fails_on_duplicate_markers(self) -> None:
        write_text(self.repo / "AGENTS.md", BLOCK + "\n\n" + BLOCK + "\n")
        code, out, err = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("duplicate Aegis bootstrap markers", out)
        self.assert_no_traceback(out, err)

    # -- adopt failures --------------------------------------------------

    def test_adopt_refuses_malformed_markers_and_writes_nothing(self) -> None:
        agents = self.repo / "AGENTS.md"
        original = (BLOCK_BEGIN + "\n## Aegis bootstrap\n").encode("utf-8")
        agents.write_bytes(original)
        code, _out, err = self.adopt()
        self.assertEqual(code, 1)
        self.assertIn("marker", err.lower())
        self.assert_no_traceback(err)
        self.assertEqual(agents.read_bytes(), original)
        self.assertFalse((self.repo / ".aegis/project.json").exists())

        code, out, err = self.doctor()
        self.assertEqual(code, 1)
        self.assertIn("FAIL", out)
        self.assertIn("marker", out.lower())
        self.assert_no_traceback(out, err)

    def test_adopt_refuses_duplicate_markers(self) -> None:
        agents = self.repo / "AGENTS.md"
        original = (BLOCK + "\n\n" + BLOCK + "\n").encode("utf-8")
        agents.write_bytes(original)
        code, _out, err = self.adopt()
        self.assertEqual(code, 1)
        self.assertIn("duplicate", err.lower())
        self.assertEqual(agents.read_bytes(), original)
        self.assertFalse((self.repo / ".aegis/project.json").exists())

    def test_adopt_rejects_aegis_path_without_run_module(self) -> None:
        empty = self.root / "empty aegis"
        empty.mkdir()
        code, _out, err = run_cli(
            "adopt", "--repo", str(self.repo), "--aegis-path", str(empty)
        )
        self.assertEqual(code, 1)
        self.assertIn("tools/aegis_run/__main__.py", err)
        self.assert_no_traceback(err)
        self.assertFalse((self.repo / ".aegis").exists())

    # -- safety ----------------------------------------------------------

    def test_version(self) -> None:
        code, out, err = run_cli("--version")
        self.assertEqual(code, 0)
        self.assertIn(__version__, out)
        self.assertEqual(err, "")

    def test_no_network_call(self) -> None:
        def blocked(*_args, **_kwargs):
            raise AssertionError("network access attempted")

        with (
            mock.patch("socket.socket", side_effect=blocked),
            mock.patch("socket.create_connection", side_effect=blocked),
            mock.patch("socket.getaddrinfo", side_effect=blocked),
        ):
            code, _out, err = self.adopt("--cursor")
            self.assertEqual(code, 0, err)
            code, out, err = self.doctor()
            self.assertEqual(code, 0, err)
            self.assertIn("PASS", out)

    @unittest.skipUnless(shutil.which("git"), "git is not installed")
    def test_aegis_commit_recorded_when_checkout_is_git(self) -> None:
        subprocess.run(
            ["git", "init", "-q", str(self.aegis)],
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(self.aegis),
                "-c",
                "user.name=Aegis Test",
                "-c",
                "user.email=test@example.invalid",
                "commit",
                "--allow-empty",
                "-q",
                "-m",
                "base",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        head = subprocess.run(
            ["git", "-C", str(self.aegis), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        self.assertTrue(SHA.match(head))
        self.assertEqual(self.adopt()[0], 0)
        self.assertEqual(self.project()["aegis_commit"], head)
        self.assertEqual(self.doctor()[0], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
