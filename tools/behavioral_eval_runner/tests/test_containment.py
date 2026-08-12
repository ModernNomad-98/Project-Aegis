"""Containment interfaces: fail-closed real host, mock boundary semantics,
reparse refusal (areas 18, 19, 20)."""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
import unittest

from tools.behavioral_eval_runner.containment import (
    CommandPolicy,
    EgressPolicy,
    MockContainment,
    RealHostContainment,
)
from tools.behavioral_eval_runner.errors import ContainmentUnavailableError, ContainmentViolationError, ReparsePointError


class TestRealHostContainment(unittest.TestCase):
    def test_capability_report_is_honest(self) -> None:
        report = RealHostContainment().capability_report()
        self.assertEqual(report["os_host_isolation_boundary"], "UNAVAILABLE")
        self.assertIn("no real-host containment claim", report["note"])

    def test_every_operation_denied_fail_closed(self) -> None:
        boundary = RealHostContainment()
        with self.assertRaises(ContainmentUnavailableError):
            boundary.validate_read("C:/anything")
        with self.assertRaises(ContainmentUnavailableError):
            boundary.validate_write("C:/anything")
        with self.assertRaises(ContainmentUnavailableError):
            boundary.check_egress("example.invalid")
        with self.assertRaises(ContainmentUnavailableError):
            boundary.check_command("echo hi")


class TestMockContainment(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        root = self._tmp.name
        self.corpus = os.path.join(root, "corpus")
        self.workspace = os.path.join(root, "workspace")
        self.control = os.path.join(root, "control_plane")
        self.caller = os.path.join(root, "caller_home")
        for directory in (self.corpus, self.workspace, self.control, self.caller):
            os.makedirs(directory, exist_ok=True)
        with open(os.path.join(self.corpus, "SKILL.md"), "w", encoding="utf-8") as fh:
            fh.write("skill")
        with open(os.path.join(self.control, "evals.json"), "w", encoding="utf-8") as fh:
            fh.write("{}")
        self.boundary = MockContainment(
            corpus_roots=(self.corpus,),
            workspace_root=self.workspace,
            control_plane_roots=(self.control,),
            caller_roots=(self.caller,),
        )

    def test_corpus_readable_but_read_only(self) -> None:
        target = os.path.join(self.corpus, "SKILL.md")
        self.assertEqual(self.boundary.validate_read(target), os.path.abspath(target))
        with self.assertRaises(ContainmentViolationError):
            self.boundary.validate_write(target)

    def test_workspace_is_the_only_writable_area(self) -> None:
        inside = os.path.join(self.workspace, "app", "file.txt")
        self.assertEqual(self.boundary.validate_write(inside), os.path.abspath(inside))
        outside = os.path.join(self._tmp.name, "elsewhere.txt")
        with self.assertRaises(ContainmentViolationError):
            self.boundary.validate_write(outside)

    def test_caller_directories_inaccessible_both_directions(self) -> None:
        target = os.path.join(self.caller, "private.txt")
        with self.assertRaises(ContainmentViolationError):
            self.boundary.validate_read(target)
        with self.assertRaises(ContainmentViolationError):
            self.boundary.validate_write(target)

    def test_control_plane_inaccessible_both_directions(self) -> None:
        target = os.path.join(self.control, "evals.json")
        with self.assertRaises(ContainmentViolationError):
            self.boundary.validate_read(target)
        with self.assertRaises(ContainmentViolationError):
            self.boundary.validate_write(target)

    def test_path_escape_via_dotdot_refused(self) -> None:
        sneaky = os.path.join(self.workspace, "..", "control_plane", "evals.json")
        with self.assertRaises(ContainmentViolationError):
            self.boundary.validate_write(sneaky)

    def test_egress_denied_by_default(self) -> None:
        with self.assertRaises(ContainmentViolationError):
            self.boundary.check_egress("127.0.0.1:8080")
        allowing = MockContainment(
            corpus_roots=(self.corpus,),
            workspace_root=self.workspace,
            egress_policy=EgressPolicy(
                deny_all=False, loopback_fixture_allowlist=("127.0.0.1:9999",)
            ),
        )
        allowing.check_egress("127.0.0.1:9999")
        with self.assertRaises(ContainmentViolationError):
            allowing.check_egress("127.0.0.1:1")

    def test_commands_allowlist_only(self) -> None:
        with self.assertRaises(ContainmentViolationError):
            self.boundary.check_command("python -c pass")
        allowing = MockContainment(
            corpus_roots=(self.corpus,),
            workspace_root=self.workspace,
            command_policy=CommandPolicy(allowed_commands=("git status",)),
        )
        allowing.check_command("git status")
        with self.assertRaises(ContainmentViolationError):
            allowing.check_command("git push")

    def test_capability_report_never_claims_real_host(self) -> None:
        report = self.boundary.capability_report()
        self.assertEqual(report["os_host_isolation_boundary"], "UNAVAILABLE")
        self.assertIn("offline tests only", report["note"])

    def test_reparse_point_refused(self) -> None:
        link_parent = os.path.join(self.workspace, "linked")
        real_target = os.path.join(self._tmp.name, "outside_dir")
        os.makedirs(real_target, exist_ok=True)
        created = False
        try:
            os.symlink(real_target, link_parent, target_is_directory=True)
            created = True
        except OSError:
            if sys.platform == "win32":
                # `cmd /c mklink` re-parses under cmd rules; guard both
                # interpolated paths to a safe charset so no path segment can
                # inject a second command via the shell.
                safe = re.compile(r"^[A-Za-z0-9_:\\.\- ]+$")
                self.assertRegex(link_parent, safe)
                self.assertRegex(real_target, safe)
                completed = subprocess.run(  # junctions need no privilege
                    ["cmd", "/c", "mklink", "/J", link_parent, real_target],
                    shell=False,
                    capture_output=True,
                    timeout=30,
                )
                created = completed.returncode == 0
        if not created:
            self.skipTest(
                "cannot create a symlink or junction in this environment "
                "(privilege-restricted); reparse refusal is still enforced "
                "by _refuse_reparse_chain, which this environment cannot "
                "exercise with a real reparse point"
            )
        with self.assertRaises(ReparsePointError):
            self.boundary.validate_write(os.path.join(link_parent, "escape.txt"))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
