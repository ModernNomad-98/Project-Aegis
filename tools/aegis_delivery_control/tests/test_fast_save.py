"""Fixtures for the offline synthetic FAST SAVE capture module.

Scope: the module-level statements of the FAST SAVE contract that an offline
fixture can actually observe - AT-01, AT-02, AT-03, AT-05, AT-06, AT-08, AT-10,
AT-11, AT-12, AT-13 and AT-15 (as a negative control). AT-04, AT-07, AT-09 and
AT-14 stay UNRUN with the host-router resolver named in the plan: no fixture
here recreates a live process, a live network or a transfer surface, and a
written claim is not evidence (protocol P9 L251-254). AT-15 keeps its contract
verdict of acceptance FAILURE; this module only proves the attempted action
cannot originate in the save path.

This module deliberately does NOT call _owner_private_fixtures.enter(): it
exercises no owned-path or kernel trusted-root check and creates no kernel
fixture. tests/test_engine.py sets the same precedent, so the omission reads as
deliberate rather than forgotten.

Audit-hook lifetime (A4): CPython installs an audit hook permanently for the
process and offers no removal API. The sentinel below is therefore installed
exactly ONCE at import time, and it records nothing unless the enable flag is
set, which happens only inside a bounded window in one fixture.
"""

from __future__ import annotations

import argparse
import ast
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

from tools.aegis_delivery_control import cli
from tools.aegis_delivery_control import fast_save

REPO_ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = REPO_ROOT / "tools" / "aegis_delivery_control" / "fast_save.py"
CLI_PATH = REPO_ROOT / "tools" / "aegis_delivery_control" / "cli.py"

# AC8 is an ENUMERATED deny set derived from CPython's audit-event table, not a
# closed proof. Residual limit, stated here and in the README: a dynamically
# imported ctypes call raises no audit event, and the import allowlist (which
# excludes ctypes and pty) is what actually blocks that import. One recorded
# fact matters for reading the set: os.spawn* matches neither os.posix_spawn as
# a glob nor as a regex, which is why the process names are enumerated.
FORBIDDEN_IMPORT_ROOTS = frozenset({
    "subprocess", "socket", "urllib", "http", "requests", "shutil", "glob",
    "sqlite3", "asyncio", "multiprocessing", "ctypes", "pty",
})
FORBIDDEN_ATTRIBUTE_NAMES = frozenset({
    # inventory
    "walk", "scandir", "listdir", "glob", "rglob", "iterdir",
    # deletion
    "remove", "rmtree",
    # process and execution
    "system", "popen", "fork", "forkpty", "posix_spawn", "posix_spawnp",
    "startfile", "kill", "abort", "spawn", "spawnl", "spawnle", "spawnlp",
    "spawnlpe", "spawnv", "spawnve", "spawnvp", "spawnvpe", "execl", "execle",
    "execlp", "execlpe", "execv", "execve", "execvp", "execvpe", "spawn",
})
FORBIDDEN_EVENT_PATTERNS = (
    "socket.*", "subprocess.*", "urllib.*", "http.client.*", "os.system",
    "os.popen", "os.exec*", "os.spawn*", "os.fork", "os.forkpty",
    "os.posix_spawn", "os.posix_spawnp", "os.startfile", "os.kill",
    "os.abort", "pty.spawn", "shutil.rmtree",
)
# The new CLI entry branch may call only formatting and the module entry points.
CLI_BRANCH_CALL_ALLOWLIST = frozenset({
    "print", "json.dumps", "fast_save.load_state_document", "fast_save.capture",
    "_fast_save_refusal", "_fast_save_report",
    # Added at the Stage C2 repair: the branch binds the checkpoint to the CLI
    # repository identity (D2) and takes the idle-measurement start before it
    # loads the state document (D4). Both are module entry points, so the branch
    # still adds no import and calls nothing but formatting plus this module.
    "fast_save.bind_repository_identity", "fast_save.start_idle_measurement",
})

_SENTINEL_ENABLED = False
_SENTINEL_EVENTS: list[tuple[str, tuple]] = []


def _sentinel_hook(event: str, args: tuple) -> None:
    if _SENTINEL_ENABLED:
        _SENTINEL_EVENTS.append((event, args))


sys.addaudithook(_sentinel_hook)


class _SentinelWindow:
    """Enable the already-installed sentinel for one bounded window."""

    def __enter__(self) -> list[tuple[str, tuple]]:
        _SENTINEL_EVENTS.clear()
        globals()["_SENTINEL_ENABLED"] = True
        return _SENTINEL_EVENTS

    def __exit__(self, *exception: object) -> bool:
        globals()["_SENTINEL_ENABLED"] = False
        return False


def _state_document(**overrides: object) -> dict:
    document = {
        "item_id": "P0-B B2",
        "objective": "capture one offline FAST SAVE checkpoint",
        "workstream_id": "p0b",
        "repository_id": "example-project",
        "current_stage": "C",
        "holder": "p0b-implementer-c2",
        "completed_work": ["read the plan"],
        "remaining_work": ["stage the commit"],
        "changed_files": [],
        "unfinished_files": [],
        "evidence_references": [],
        "failures_blockers": [],
        "gaps": [],
        "operations": [],
        "dispatch_state_reported": "stopped",
        "pause_reported_complete": True,
        "pause_incomplete_reason": "",
        "authority_references": ["coordinator item brief"],
        "one_line_resume": "Resume B2 Stage C at the capture module and its fixtures",
        "next_safe_action": "run the focused fixture module",
    }
    document.update(overrides)
    return document


def _operation(
    operation_id: str, reported_state: str, authorized: bool = False, reference: str = ""
) -> dict:
    return {
        "operation_id": operation_id,
        "reported_state": reported_state,
        "authorized_to_stop": authorized,
        "authorization_ref": reference,
    }


def _dotted(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return _dotted(node.value) + "." + node.attr
    return ""


def _events_of(events: list[tuple[str, tuple]], patterns: tuple[str, ...]) -> list[str]:
    import fnmatch

    return [
        name for (name, _args) in events
        if any(fnmatch.fnmatchcase(name, pattern) for pattern in patterns)
    ]


class FastSaveTests(unittest.TestCase):
    def setUp(self) -> None:
        self._temp = tempfile.TemporaryDirectory()
        self.addCleanup(self._temp.cleanup)
        self.root = Path(self._temp.name)
        self.state_path = self.root / "state.json"
        self.checkpoint_path = self.root / "checkpoint.json"

    def _write_state(self, document: dict | None = None, name: str = "state.json") -> Path:
        path = self.root / name
        path.write_text(
            json.dumps(document if document is not None else _state_document()),
            encoding="utf-8",
        )
        return path

    def _save(
        self, document: dict | None = None, checkpoint: Path | None = None,
        phrase: str = "fast save",
    ) -> fast_save.SaveResult:
        state = self._write_state(document)
        request = fast_save.load_state_document(state)
        return fast_save.capture(
            request, checkpoint if checkpoint is not None else self.checkpoint_path,
            invocation_phrase=phrase,
        )

    def _run_cli(self, argv: list) -> tuple[int, str]:
        """Run the CLI with the state root patched to prove it is never opened."""
        stdout = io.StringIO()
        with mock.patch.object(
            cli, "default_state_root",
            side_effect=AssertionError("the state root was opened"),
        ), contextlib.redirect_stdout(stdout):
            exit_code = cli.main(argv)
        return exit_code, stdout.getvalue().strip()

    def _read_saved(self) -> dict:
        return fast_save.read_checkpoint_bounded(self.checkpoint_path)

    def _sha256(self, path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def _temp_leftovers(self, target: Path) -> list:
        return sorted(target.parent.glob(target.name + ".fast-save-*.tmp"))

    def test_at01_clean_idle_saves_and_reports_stopped(self) -> None:
        result = self._save()
        self.assertEqual(result.checkpoint_status, "SAVED")
        self.assertEqual(result.reason_code, "SAVED")
        self.assertEqual(result.one_line_resume, _state_document()["one_line_resume"])
        document = self._read_saved()
        self.assertEqual(document["execution_status"], "STOPPED")
        self.assertEqual(document["execution_status_source"], "reported-by-operator")
        self.assertEqual(document["operations"], [])
        self.assertEqual(document["reported_state_conflicts"], [])
        self.assertEqual(document["checkpoint_status"], "SAVED")
        self.assertEqual(document["safe_stopped_operations"], [])
        self.assertEqual(
            document["safe_stopped_operations_note"], fast_save.SAFE_STOPPED_NONE_NOTE
        )
        self.assertTrue(document["safe_stopped_operations_note"].strip())

    def test_at02_at03_reported_dirty_and_untracked_files_are_preserved(self) -> None:
        dirty = self.root / "dirty.txt"
        untracked = self.root / "untracked.txt"
        dirty.write_text("reported dirty\n", encoding="utf-8")
        untracked.write_text("reported untracked\n", encoding="utf-8")
        before = {path.name: self._sha256(path) for path in (dirty, untracked)}
        document = _state_document(
            changed_files=[
                {"path": str(dirty), "uncommitted": True},
                {"path": str(untracked), "uncommitted": True},
            ],
            unfinished_files=[str(untracked)],
        )
        result = self._save(document)
        self.assertEqual(result.checkpoint_status, "SAVED")
        written = self._read_saved()
        self.assertEqual(
            [entry["path"] for entry in written["changed_files"]],
            [str(dirty), str(untracked)],
        )
        self.assertTrue(all(entry["uncommitted"] is True for entry in written["changed_files"]))
        self.assertEqual(written["unfinished_files"], [str(untracked)])
        self.assertTrue(written["unfinished_files_preserved"])
        self.assertEqual(written["changed_files_source"], fast_save.CHANGED_FILES_SOURCE)
        self.assertIn("runs no git command", written["changed_files_source"])
        after = {path.name: self._sha256(path) for path in (dirty, untracked)}
        self.assertEqual(before, after, "the save changed a reported path")

    def test_at05_large_population_is_not_inventoried(self) -> None:
        for index in range(500):
            (self.root / ("population-%04d.txt" % index)).write_text("x", encoding="utf-8")
        reference = str(self.root / "population-0000.txt")
        result = self._save(_state_document(evidence_references=[reference]))
        self.assertEqual(result.checkpoint_status, "SAVED")
        document = self._read_saved()
        self.assertEqual(document["evidence_references"], [reference])
        self.assertIn("never re-read", document["evidence_references_note"])
        idle = document["idle_measurement"]
        self.assertIn("capture portion", idle["measured_what"])
        self.assertIn("never inferred", idle["measured_what"])
        self.assertEqual(idle["target_seconds"], 60)
        self.assertTrue(idle["within_target"])
        self.assertGreaterEqual(idle["measured_seconds"], 0.0)
        self.assertEqual(document["gaps"], [])
        self.assertIn("never filled", document["gaps_note"])
        self.assertFalse(document["no_provider_call_attestation"]["provider_call_made"])

    def test_at06_at15_negative_control_no_network_process_test_or_ci_action(self) -> None:
        source = MODULE_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source)
        imported_roots: set[str] = set()
        forbidden_calls: list[str] = []
        unlink_sites = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_roots.add(node.module.split(".")[0])
            elif isinstance(node, ast.Attribute):
                if node.attr in FORBIDDEN_ATTRIBUTE_NAMES:
                    forbidden_calls.append(_dotted(node))
                if _dotted(node) == "os.unlink":
                    unlink_sites += 1
        print("AC8 scanned file:", MODULE_PATH.relative_to(REPO_ROOT).as_posix())
        print("AC8 import allowlist observed:", sorted(imported_roots))
        print("AC8 forbidden attribute calls:", forbidden_calls)
        print("AC8 deletion call sites (os.unlink):", unlink_sites)
        self.assertLessEqual(imported_roots, set(fast_save.ALLOWED_IMPORTS))
        self.assertEqual(imported_roots & FORBIDDEN_IMPORT_ROOTS, set())
        self.assertEqual(forbidden_calls, [])
        self.assertEqual(unlink_sites, 1)
        print("AC8 residual limit: a dynamically imported ctypes call raises no")
        print("audit event; ctypes and pty are outside the import allowlist, and")
        print("the deny set is ENUMERATED, not closed.")

        # A3 (ii): the new CLI entry branch is scanned too - no new import, and
        # only formatting plus the two module entry points are called.
        branch_calls: list[str] = []
        branch_imports: list[str] = []
        for node in ast.walk(ast.parse(CLI_PATH.read_text(encoding="utf-8"))):
            if not isinstance(node, ast.If):
                continue
            literals = [
                child.value for child in ast.walk(node.test)
                if isinstance(child, ast.Constant) and isinstance(child.value, str)
            ]
            if "fast-save" not in literals:
                continue
            for inner in ast.walk(node):
                if isinstance(inner, (ast.Import, ast.ImportFrom)):
                    branch_imports.append(ast.dump(inner))
                elif isinstance(inner, ast.Call):
                    branch_calls.append(_dotted(inner.func))
        self.assertEqual(branch_imports, [], "the fast-save branch adds an import")
        self.assertTrue(branch_calls, "the fast-save branch was not found in cli.py")
        print("A3 cli.py fast-save branch calls:", sorted(set(branch_calls)))
        self.assertLessEqual(set(branch_calls), set(CLI_BRANCH_CALL_ALLOWLIST))
        self.assertNotIn("os.system", branch_calls)

        # The mandatory live-hook POSITIVE control: the sentinel is proven to
        # fire in this very process before its silence is believed.
        probe = self.root / "positive-control.txt"
        with _SentinelWindow() as events:
            probe.write_text("probe", encoding="utf-8")
        opened = [
            str(args[0]) for (name, args) in events
            if name == "open" and args and "positive-control" in str(args[0])
        ]
        self.assertTrue(opened, "the audit sentinel recorded no event for the probe")
        print("AC8 positive control: recorded open event for", sorted(set(opened)))

        # The measured window: one save plus one readback.
        state = self._write_state()
        request = fast_save.load_state_document(state)
        with _SentinelWindow() as events:
            result = fast_save.capture(request, self.checkpoint_path, invocation_phrase="fast save")
            fast_save.read_checkpoint_bounded(self.checkpoint_path)
        self.assertEqual(result.checkpoint_status, "SAVED")
        forbidden = _events_of(events, FORBIDDEN_EVENT_PATTERNS)
        print("AC8 forbidden events in the save window:", forbidden)
        print("AC8 extended deny set:", FORBIDDEN_EVENT_PATTERNS)
        self.assertEqual(forbidden, [])
        opened_paths = [
            str(args[0]) for (name, args) in events
            if name == "open" and isinstance(args[0], (str, bytes, os.PathLike))
        ]
        descriptors = [
            args[0] for (name, args) in events
            if name == "open" and isinstance(args[0], int)
        ]
        for raw in opened_paths:
            candidate = Path(raw)
            allowed = (
                candidate == state
                or candidate == self.checkpoint_path
                or candidate.name.startswith(self.checkpoint_path.name + ".fast-save-")
            )
            self.assertTrue(allowed, "an unexpected path was opened: " + raw)
        for descriptor in descriptors:
            self.assertIsInstance(descriptor, int)
        print("AC9 opened paths in the save window:", sorted({Path(p).name for p in opened_paths}))
        print("AC9 file-descriptor opens in the save window:", len(descriptors))

    def test_at08_active_operation_reports_state_and_only_authorized_stops_are_listed(
        self,
    ) -> None:
        operations = [
            _operation("op-active-authorized", "ACTIVE", True, "APR-100"),
            _operation("op-stopped-authorized", "STOPPED", True, "APR-100"),
            _operation("op-stopped-unauthorized", "STOPPED", False, ""),
        ]
        result = self._save(_state_document(operations=operations))
        self.assertEqual(result.checkpoint_status, "SAVED")
        document = self._read_saved()
        self.assertEqual(document["execution_status"], "ACTIVE")
        self.assertEqual(
            [entry["operation_id"] for entry in document["safe_stopped_operations"]],
            ["op-stopped-authorized"],
        )
        self.assertEqual(
            document["safe_stopped_operations"][0]["authorization_ref"], "APR-100"
        )
        self.assertEqual(
            document["safe_stopped_operations_source"], "reported-by-operator"
        )
        self.assertIn("stops nothing", document["safe_stopped_operations_note"])
        reasons = {
            entry["operation_id"]: entry["reason"]
            for entry in document["operations_not_stopped"]
        }
        self.assertEqual(
            sorted(reasons), ["op-active-authorized", "op-stopped-unauthorized"]
        )
        self.assertIn("reported ACTIVE", reasons["op-active-authorized"])
        self.assertIn("authorization absent", reasons["op-stopped-unauthorized"])

    def test_at10_interrupted_replace_leaves_previous_bytes_and_reports_failed(self) -> None:
        first = self._save()
        self.assertEqual(first.checkpoint_status, "SAVED")
        before = self._sha256(self.checkpoint_path)
        with mock.patch.object(
            fast_save.os, "replace", side_effect=OSError("simulated interruption")
        ):
            second = self._save()
        self.assertEqual(second.checkpoint_status, "FAILED")
        self.assertEqual(second.reason_code, "REPLACE_FAILED")
        self.assertIsNone(second.document)
        self.assertEqual(self._sha256(self.checkpoint_path), before)
        self.assertEqual(self._temp_leftovers(self.checkpoint_path), [])
        previous = self._read_saved()
        self.assertEqual(previous["checkpoint_sequence"], 1)
        self.assertIsNone(previous["previous_valid_checkpoint"])

    def test_at11_failed_persistence_preserves_the_previous_checkpoint(self) -> None:
        self.assertEqual(self._save().checkpoint_status, "SAVED")
        before = self._sha256(self.checkpoint_path)
        oversized = self._save(_state_document(gaps=["x" * 70000]))
        self.assertEqual(oversized.checkpoint_status, "FAILED")
        self.assertEqual(oversized.reason_code, "CHECKPOINT_TOO_LARGE")
        self.assertEqual(self._sha256(self.checkpoint_path), before)
        self.assertEqual(self._temp_leftovers(self.checkpoint_path), [])
        with mock.patch.object(
            fast_save.tempfile, "mkstemp", side_effect=OSError("simulated write failure")
        ):
            unwritable = self._save()
        self.assertEqual(unwritable.checkpoint_status, "FAILED")
        self.assertEqual(unwritable.reason_code, "WRITE_FAILED")
        self.assertEqual(self._sha256(self.checkpoint_path), before)
        self.assertEqual(self._temp_leftovers(self.checkpoint_path), [])
        self.assertEqual(self._read_saved()["checkpoint_sequence"], 1)

    def test_at12_bounded_readback_confirms_completeness(self) -> None:
        result = self._save()
        self.assertEqual(result.checkpoint_status, "SAVED")
        readback = result.bounded_readback
        self.assertEqual(readback["subject"], "temp-file-before-replace")
        self.assertTrue(readback["performed"])
        self.assertTrue(readback["complete"])
        self.assertTrue(readback["integrity_verified"])
        self.assertTrue(readback["keyset_verified"])
        self.assertTrue(readback["verified_before_replace"])
        self.assertEqual(readback["missing_fields"], [])
        self.assertLessEqual(readback["bytes_read"], fast_save.MAX_CHECKPOINT_BYTES)
        self.assertTrue(readback["post_replace_confirmation"]["performed"])
        self.assertTrue(readback["post_replace_confirmation"]["matches_verified_bytes"])
        document = self._read_saved()
        self.assertEqual(
            document["bounded_readback"]["bytes_read"], self.checkpoint_path.stat().st_size
        )
        self.assertEqual(
            document["integrity"]["content_sha256"],
            result.document["integrity"]["content_sha256"],
        )
        self.assertEqual(
            document["bounded_readback"]["post_replace_confirmation"]["performed"], False
        )
        self.assertEqual(
            document["bounded_readback"]["post_replace_confirmation"]["recorded_in"],
            "the caller's SaveResult",
        )
        # Readback-failure variant, first save: the target must stay ABSENT.
        fresh = self.root / "fresh.json"
        truncated = {
            "checkpoint_format": fast_save.CHECKPOINT_FORMAT,
            "checkpoint_status": "SAVED",
        }
        with mock.patch.object(
            fast_save, "read_checkpoint_bounded", return_value=dict(truncated)
        ):
            failed = self._save(checkpoint=fresh)
        self.assertEqual(failed.checkpoint_status, "FAILED")
        self.assertEqual(failed.reason_code, "READBACK_FAILED")
        self.assertFalse(fresh.exists(), "a failed readback left a target behind")
        self.assertEqual(self._temp_leftovers(fresh), [])
        # Readback-failure variant, second save: the previous bytes must survive.
        before = self._sha256(self.checkpoint_path)
        with mock.patch.object(
            fast_save, "read_checkpoint_bounded", return_value=dict(truncated)
        ):
            failed_again = self._save()
        self.assertEqual(failed_again.checkpoint_status, "FAILED")
        self.assertEqual(failed_again.reason_code, "READBACK_FAILED")
        self.assertEqual(self._sha256(self.checkpoint_path), before)
        self.assertEqual(self._temp_leftovers(self.checkpoint_path), [])

    def test_at13_fresh_session_resumes_from_the_checkpoint_alone(self) -> None:
        resume = "Resume B2 at the SD-C handoff; the checkpoint carries everything needed"
        result = self._save(
            _state_document(one_line_resume=resume, next_safe_action="open the PR")
        )
        self.assertEqual(result.checkpoint_status, "SAVED")
        document = fast_save.read_checkpoint_bounded(self.checkpoint_path)
        self.assertEqual(document["one_line_resume"], resume)
        self.assertNotIn("\n", document["one_line_resume"])
        self.assertEqual(document["next_safe_action"], "open the PR")
        self.assertEqual(document["execution_status"], "STOPPED")
        self.assertEqual(set(document), set(fast_save.REQUIRED_CHECKPOINT_KEYS))
        script = (
            "import json, sys;"
            "from tools.aegis_delivery_control.fast_save import read_checkpoint_bounded;"
            "d = read_checkpoint_bounded(sys.argv[1]);"
            "print(json.dumps({k: d[k] for k in"
            " ('one_line_resume', 'next_safe_action', 'execution_status')}, sort_keys=True))"
        )
        completed = subprocess.run(
            [sys.executable, "-B", "-c", script, str(self.checkpoint_path)],
            cwd=str(REPO_ROOT), capture_output=True, text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        fresh = json.loads(completed.stdout)
        self.assertEqual(fresh["one_line_resume"], resume)
        self.assertEqual(fresh["next_safe_action"], "open the PR")
        self.assertEqual(fresh["execution_status"], "STOPPED")

    def test_path_guard_refuses_unrelated_directory_and_symlink(self) -> None:
        unrelated = self.root / "unrelated.txt"
        unrelated.write_text("unrelated payload\n", encoding="utf-8")
        before = self._sha256(unrelated)
        refused = self._save(checkpoint=unrelated)
        self.assertEqual(refused.checkpoint_status, "FAILED")
        self.assertEqual(refused.reason_code, "PATH_GUARD_DENIED")
        self.assertEqual(self._sha256(unrelated), before)
        directory = self.root / "a-directory"
        directory.mkdir()
        refused = self._save(checkpoint=directory)
        self.assertEqual(refused.reason_code, "PATH_GUARD_DENIED")
        self.assertTrue(directory.is_dir())
        link = self.root / "link.json"
        try:
            os.symlink(unrelated, link)
        except (OSError, NotImplementedError) as error:
            # Real-symlink variant: UNRUN on this host, with its resolver. The
            # ordering below is still proven: with the link test forced true,
            # the guard refuses on that signal alone, before any read and
            # before any replace.
            print("AC6 real-symlink variant: UNRUN on this host:", error)
            print(
                "AC6 resolver for the real-link variant: a host holding "
                "SeCreateSymbolicLinkPrivilege (or Windows Developer Mode)"
            )
            with mock.patch.object(
                fast_save.os.path, "islink", return_value=True
            ), mock.patch.object(
                fast_save.os, "replace",
                side_effect=AssertionError("os.replace ran past the link refusal"),
            ):
                refused = self._save(checkpoint=unrelated)
            self.assertEqual(refused.reason_code, "PATH_GUARD_DENIED")
            self.assertIn("symlink", refused.reason)
            self.assertEqual(self._sha256(unrelated), before)
            self.assertFalse(link.exists())
        else:
            refused = self._save(checkpoint=link)
            self.assertEqual(refused.reason_code, "PATH_GUARD_DENIED")
            self.assertIn("symlink", refused.reason)
            self.assertTrue(os.path.islink(link))
            self.assertEqual(self._sha256(unrelated), before)
            self.assertTrue(link.exists())
        not_json = self.root / "not-json.json"
        not_json.write_text("this is not JSON\n", encoding="utf-8")
        refused = self._save(checkpoint=not_json)
        self.assertEqual(refused.reason_code, "PATH_GUARD_DENIED")
        self.assertEqual(not_json.read_text(encoding="utf-8"), "this is not JSON\n")
        wrong_format = self.root / "wrong-format.json"
        wrong_format.write_text(
            json.dumps({"checkpoint_format": "some-other-format"}), encoding="utf-8"
        )
        refused = self._save(checkpoint=wrong_format)
        self.assertEqual(refused.reason_code, "PATH_GUARD_DENIED")
        self.assertEqual(json.loads(wrong_format.read_text(encoding="utf-8")),
                         {"checkpoint_format": "some-other-format"})
        missing_parent = self.root / "absent" / "checkpoint.json"
        refused = self._save(checkpoint=missing_parent)
        self.assertEqual(refused.reason_code, "PATH_GUARD_DENIED")
        self.assertFalse(missing_parent.parent.exists(), "a parent directory was created")
        # A recognizable predecessor whose integrity digest fails IS overwritten
        # and recorded as not valid (F9).
        corrupt = self.root / "corrupt.json"
        self.assertEqual(self._save(checkpoint=corrupt).checkpoint_status, "SAVED")
        damaged = json.loads(corrupt.read_text(encoding="utf-8"))
        damaged["integrity"]["content_sha256"] = "0" * 64
        corrupt.write_text(json.dumps(damaged), encoding="utf-8")
        recovered = self._save(checkpoint=corrupt)
        self.assertEqual(recovered.checkpoint_status, "SAVED")
        written = fast_save.read_checkpoint_bounded(corrupt)
        self.assertIsNone(written["previous_valid_checkpoint"])
        self.assertEqual(written["checkpoint_sequence"], 1)
        # No bypass flag exists in the parser.
        subparsers = next(
            action for action in cli.build_parser()._actions
            if isinstance(action, argparse._SubParsersAction)
        )
        self.assertEqual(
            sorted(subparsers.choices),
            ["capabilities", "fast-save", "status", "verify"],
        )
        fast_save_parser = subparsers.choices["fast-save"]
        options = sorted({
            option for action in fast_save_parser._actions
            for option in action.option_strings if option not in ("-h", "--help")
        })
        self.assertEqual(options, ["--checkpoint", "--invocation-phrase", "--state"])
        with self.assertRaises(SystemExit):
            fast_save_parser.parse_args(
                ["--state", "s.json", "--checkpoint", "c.json", "--force"]
            )

    def test_status_never_upgrades_unknown_and_records_conflicts(self) -> None:
        unknown = _state_document(
            operations=[_operation("op-unknown", "UNKNOWN", True, "APR-100")]
        )
        self.assertEqual(self._save(unknown).checkpoint_status, "SAVED")
        written = self._read_saved()
        self.assertEqual(written["execution_status"], "UNKNOWN")
        self.assertEqual(written["execution_status_source"], "reported-by-operator")
        self.assertIn("observes no process", written["execution_status_note"])
        self.assertIn("claims no cessation", written["execution_status_note"])
        self.assertTrue(written["reported_state_conflicts"])
        self.assertIn("UNKNOWN", written["reported_state_conflicts"][0])
        self.assertEqual(
            [entry["operation_id"] for entry in written["safe_stopped_operations"]], []
        )
        incomplete = _state_document(
            operations=[_operation("op-unknown", "UNKNOWN", True, "APR-100")],
            pause_reported_complete=False,
            pause_incomplete_reason="the pause did not complete; one operation is uncertain",
        )
        self.assertEqual(self._save(incomplete).checkpoint_status, "SAVED")
        self.assertEqual(self._read_saved()["execution_status"], "PAUSE INCOMPLETE")
        active = _state_document(
            operations=[_operation("op-active", "ACTIVE", False, "")]
        )
        self.assertEqual(self._save(active).checkpoint_status, "SAVED")
        written = self._read_saved()
        self.assertEqual(written["execution_status"], "ACTIVE")
        self.assertTrue(
            any("pause is reported complete" in item
                for item in written["reported_state_conflicts"])
        )

    def test_secret_guard_refuses_credential_keys_and_token_shaped_values(self) -> None:
        credential_key = _state_document()
        credential_key["token"] = "not-a-real-token"
        with self.assertRaises(fast_save.FastSaveRefused) as caught:
            fast_save.load_state_document(self._write_state(credential_key))
        self.assertEqual(caught.exception.reason_code, "SECRET_DETECTED")
        with self.assertRaises(fast_save.FastSaveRefused) as refused:
            self._save(credential_key)
        self.assertEqual(refused.exception.reason_code, "SECRET_DETECTED")
        self.assertFalse(self.checkpoint_path.exists())
        token_value = _state_document(
            one_line_resume="ghp_exampleTokenValueNotReal"
        )
        with self.assertRaises(fast_save.FastSaveRefused) as refused:
            self._save(token_value)
        self.assertEqual(refused.exception.reason_code, "SECRET_DETECTED")
        self.assertFalse(self.checkpoint_path.exists())
        # The check runs on the serialized document, so it also covers lists.
        nested = _state_document(failures_blockers=["AKIAEXAMPLEKEYNOTREAL"])
        with self.assertRaises(fast_save.FastSaveRefused) as refused:
            self._save(nested)
        self.assertEqual(refused.exception.reason_code, "SECRET_DETECTED")
        self.assertFalse(self.checkpoint_path.exists())
        self.assertEqual(self._temp_leftovers(self.checkpoint_path), [])

    def test_cli_fast_save_end_to_end_and_state_root_isolation(self) -> None:
        state = self._write_state()
        stdout = io.StringIO()
        with mock.patch.object(
            cli, "default_state_root", side_effect=AssertionError("the state root was opened")
        ), contextlib.redirect_stdout(stdout):
            exit_code = cli.main([
                "--repository-id", "example-project", "fast-save",
                "--state", str(state), "--checkpoint", str(self.checkpoint_path),
                "--invocation-phrase", "fast save",
            ])
        self.assertEqual(exit_code, 0)
        line = json.loads(stdout.getvalue().strip())
        self.assertEqual(line["checkpoint_status"], "SAVED")
        self.assertEqual(line["execution_status"], "STOPPED")
        self.assertEqual(line["execution_status_source"], "reported-by-operator")
        self.assertEqual(line["durable_location"], str(self.checkpoint_path.absolute()))
        self.assertEqual(
            line["bounded_readback"]["subject"], "temp-file-before-replace"
        )
        self.assertTrue(line["one_line_resume"])
        self.assertEqual(set(line), {
            "checkpoint_status", "reason_code", "reason", "execution_status",
            "execution_status_source", "durable_location", "bounded_readback",
            "one_line_resume",
        })
        # The CLI entry branch runs inside the sentinel window too (A3 (i)).
        second = self.root / "cli-second.json"
        stdout = io.StringIO()
        with _SentinelWindow() as events, contextlib.redirect_stdout(stdout):
            exit_code = cli.main([
                "--repository-id", "example-project", "fast-save",
                "--state", str(state), "--checkpoint", str(second),
            ])
        self.assertEqual(exit_code, 0)
        self.assertEqual(_events_of(events, FORBIDDEN_EVENT_PATTERNS), [])
        for raw in [
            str(args[0]) for (name, args) in events
            if name == "open" and isinstance(args[0], (str, bytes, os.PathLike))
        ]:
            candidate = Path(raw)
            self.assertTrue(
                candidate == state
                or candidate == second
                or candidate.name.startswith(second.name + ".fast-save-"),
                "the CLI branch opened an unexpected path: " + raw,
            )
        # A refusal returns exit 4 with a FAILED line, and writes nothing.
        refused_path = self.root / "cli-refused.json"
        stdout = io.StringIO()
        with mock.patch.object(
            cli, "default_state_root", side_effect=AssertionError("the state root was opened")
        ), contextlib.redirect_stdout(stdout):
            exit_code = cli.main([
                "--repository-id", "example-project", "fast-save",
                "--state", str(self._write_state(
                    _state_document(one_line_resume="sk-notarealkey")
                )),
                "--checkpoint", str(refused_path),
            ])
        self.assertEqual(exit_code, 4)
        line = json.loads(stdout.getvalue().strip())
        self.assertEqual(line["checkpoint_status"], "FAILED")
        self.assertEqual(line["reason_code"], "SECRET_DETECTED")
        self.assertIsNone(line["execution_status"])
        self.assertIsNone(line["durable_location"])
        self.assertFalse(refused_path.exists())
        # The capabilities JSON is byte-identical to the base output.
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            exit_code = cli.main([
                "--repository-id", "example-project", "capabilities",
            ])
        self.assertEqual(exit_code, 0)
        self.assertEqual(
            stdout.getvalue().strip(),
            '{"authority": "synthetic-only", "external_io": false, '
            '"git_mutation": false, "lifecycle_cli_mutation": false, '
            '"power_loss_durability_proven": false, '
            '"process_crash_atomicity": "tested", "real_adapters": false}',
        )

    def test_checkpoint_field_completeness_against_the_scaffold(self) -> None:
        result = self._save()
        self.assertEqual(result.checkpoint_status, "SAVED")
        document = self._read_saved()
        self.assertEqual(set(document), set(fast_save.REQUIRED_CHECKPOINT_KEYS))
        scaffold = (
            "checkpoint_format", "checkpoint_version", "checkpoint_sequence",
            "created_utc", "created_unix_seconds", "invocation_phrase",
            "repository_id", "workstream_id", "item_id",
            "dispatch_state_reported", "dispatch_state_source", "objective",
            "current_stage", "holder", "completed_work", "remaining_work",
            "unfinished_files", "unfinished_files_preserved", "changed_files",
            "changed_files_source", "execution_status", "execution_status_source",
            "execution_status_note", "operations", "reported_state_conflicts",
            "checkpoint_status", "durable_location", "durable_location_approval",
            "bounded_readback", "one_line_resume", "previous_valid_checkpoint",
            "no_provider_call_attestation", "safe_stopped_operations",
            "safe_stopped_operations_source", "safe_stopped_operations_note",
            "operations_not_stopped", "no_credentials_tokens_secrets",
            "idle_measurement", "integrity",
        )
        for key in scaffold:
            self.assertIn(key, document, "the checkpoint is missing " + key)
        self.assertEqual(document["checkpoint_format"], fast_save.CHECKPOINT_FORMAT)
        self.assertEqual(document["checkpoint_version"], 1)
        self.assertEqual(document["checkpoint_sequence"], 1)
        self.assertEqual(document["invocation_phrase"], "fast save")
        self.assertIn("not an authorization", document["invocation_phrase_note"])
        self.assertEqual(document["no_credentials_tokens_secrets"]["checked"], True)
        self.assertEqual(document["no_credentials_tokens_secrets"]["finding"], "none")
        self.assertEqual(
            document["bounded_readback"]["max_bytes"], fast_save.MAX_CHECKPOINT_BYTES
        )
        self.assertEqual(document["safe_stopped_operations"], [])
        self.assertEqual(
            document["safe_stopped_operations_note"], fast_save.SAFE_STOPPED_NONE_NOTE
        )
        self.assertIn("G3", document["durable_location_approval"])
        self.assertIn("NOT validated", document["authority_references_note"])
        self.assertEqual(
            set(document) & fast_save.CREDENTIAL_KEY_NAMES, set()
        )
        # A second save over a valid predecessor increments the sequence and
        # records the predecessor reference.
        second = self._save()
        self.assertEqual(second.checkpoint_status, "SAVED")
        successor = self._read_saved()
        self.assertEqual(successor["checkpoint_sequence"], 2)
        self.assertEqual(
            successor["previous_valid_checkpoint"]["checkpoint_sequence"], 1
        )
        self.assertEqual(
            successor["previous_valid_checkpoint"]["content_sha256"],
            document["integrity"]["content_sha256"],
        )

    def test_d1_embedded_token_in_objective_refuses_and_keeps_the_previous_checkpoint(
        self,
    ) -> None:
        """D1: a token inside prose is refused, not saved under a 'none' attestation."""
        first = self._save()
        self.assertEqual(first.checkpoint_status, "SAVED")
        before = self._sha256(self.checkpoint_path)
        before_document = self._read_saved()
        embedded = _state_document(
            objective="resume the increment using ghp_exampleTokenValueNotReal now"
        )
        state = self._write_state(embedded)
        with self.assertRaises(fast_save.FastSaveRefused) as refused:
            fast_save.load_state_document(state)
        self.assertEqual(refused.exception.reason_code, "SECRET_DETECTED")
        # The refusal says WHERE the prefix was found (a non-zero offset, which is
        # what proves the scan is position-independent) and never repeats the
        # matched text back into the log.
        self.assertIn("at character offset", refused.exception.reason)
        offset = int(
            refused.exception.reason.split("at character offset ")[1].split(")")[0]
        )
        self.assertGreater(offset, 0)
        self.assertNotIn("ghp_exampleTokenValueNotReal", refused.exception.reason)
        # End to end: exit 4, a FAILED line, no traceback, and the PREVIOUS
        # checkpoint byte-for-byte intact.
        exit_code, line = self._run_cli([
            "--repository-id", "example-project", "fast-save",
            "--state", str(state), "--checkpoint", str(self.checkpoint_path),
        ])
        self.assertEqual(exit_code, 4)
        payload = json.loads(line)
        self.assertEqual(payload["checkpoint_status"], "FAILED")
        self.assertEqual(payload["reason_code"], "SECRET_DETECTED")
        self.assertIsNone(payload["execution_status"])
        self.assertEqual(self._sha256(self.checkpoint_path), before)
        self.assertEqual(self._read_saved(), before_document)
        self.assertEqual(
            self._read_saved()["no_credentials_tokens_secrets"]["finding"], "none"
        )
        self.assertEqual(self._temp_leftovers(self.checkpoint_path), [])

    def test_d1_token_scan_covers_every_position_and_keeps_ordinary_words_safe(
        self,
    ) -> None:
        """D1: any string position is scanned, and 'sk-' does not fire inside words."""
        # The two matchers cover the whole declared prefix list, so the README's
        # list and the code cannot drift apart silently.
        self.assertEqual(
            {prefix.lower() for prefix in fast_save.TOKEN_VALUE_PREFIXES},
            set(fast_save.TOKEN_VALUE_ANY_OFFSET_PREFIXES)
            | set(fast_save.TOKEN_VALUE_BOUNDARY_PREFIXES),
        )
        embedded_cases = {
            "objective_prose": _state_document(
                objective="see token (ghp_embeddedNotARealToken) for details"
            ),
            "list_entry": _state_document(
                failures_blockers=["blocked by github_pat_embeddedNotARealToken"]
            ),
            "changed_file_path": _state_document(
                changed_files=[
                    {"path": "tools/gho_embeddedNotARealToken.py", "uncommitted": True}
                ]
            ),
            "authorization_ref": _state_document(
                operations=[
                    _operation(
                        "op-embedded", "STOPPED", True,
                        "brief AKIAEMBEDDEDNOTAREALKEY",
                    )
                ]
            ),
            "trailing_sk_prefix": _state_document(
                next_safe_action="rotate sk-embeddedNotARealKey now"
            ),
            "begin_marker": _state_document(
                gaps=["-----BEGIN PRIVATE KEY----- material"]
            ),
        }
        for name, document in embedded_cases.items():
            with self.subTest(case=name):
                with self.assertRaises(fast_save.FastSaveRefused) as refused:
                    fast_save.load_state_document(self._write_state(document))
                self.assertEqual(refused.exception.reason_code, "SECRET_DETECTED")
                self.assertFalse(self.checkpoint_path.exists())
        # The strictest honest reading must not manufacture a refusal out of an
        # ordinary word that merely contains the two letters of "sk-".
        for safe_prose in (
            "update the task-list before the next stage",
            "risk-based ordering of the remaining work",
            "check disk-usage and desk-tidy notes",
        ):
            with self.subTest(safe=safe_prose):
                request = fast_save.load_state_document(
                    self._write_state(_state_document(objective=safe_prose))
                )
                self.assertEqual(request.objective, safe_prose)
        # ...while a leading or delimiter-preceded token is still refused.
        for token in ("sk-notARealKey", "(sk-notARealKey)"):
            with self.subTest(token=token):
                with self.assertRaises(fast_save.FastSaveRefused) as refused:
                    fast_save.load_state_document(
                        self._write_state(_state_document(one_line_resume=token))
                    )
                self.assertEqual(refused.exception.reason_code, "SECRET_DETECTED")

    def test_d2_repository_identity_mismatch_is_refused_as_state_invalid(self) -> None:
        """D2: the checkpoint is bound to the CLI identity, or it is refused."""
        first = self._save()
        self.assertEqual(first.checkpoint_status, "SAVED")
        before = self._sha256(self.checkpoint_path)
        state = self._write_state(_state_document(repository_id="other-repo"))
        request = fast_save.load_state_document(state)
        with self.assertRaises(fast_save.FastSaveRefused) as refused:
            fast_save.bind_repository_identity(request, "example-project")
        self.assertEqual(refused.exception.reason_code, "STATE_INVALID")
        self.assertIn("other-repo", refused.exception.reason)
        with self.assertRaises(fast_save.FastSaveRefused) as blank:
            fast_save.bind_repository_identity(request, "   ")
        self.assertEqual(blank.exception.reason_code, "STATE_INVALID")
        # End to end: exit 4 with STATE_INVALID, nothing written, the previous
        # checkpoint intact and still bound to its own repository.
        exit_code, line = self._run_cli([
            "--repository-id", "example-project", "fast-save",
            "--state", str(state), "--checkpoint", str(self.checkpoint_path),
        ])
        self.assertEqual(exit_code, 4)
        payload = json.loads(line)
        self.assertEqual(payload["checkpoint_status"], "FAILED")
        self.assertEqual(payload["reason_code"], "STATE_INVALID")
        self.assertIsNone(payload["execution_status"])
        self.assertIsNone(payload["durable_location"])
        self.assertEqual(self._sha256(self.checkpoint_path), before)
        self.assertEqual(self._read_saved()["repository_id"], "example-project")
        self.assertEqual(self._temp_leftovers(self.checkpoint_path), [])
        # Positive control: the matching identity still saves, so the refusal is
        # not a blanket refusal of every fast save.
        matching = self._write_state(
            _state_document(repository_id="example-project"), name="matching.json"
        )
        target = self.root / "matching-checkpoint.json"
        exit_code, line = self._run_cli([
            "--repository-id", "example-project", "fast-save",
            "--state", str(matching), "--checkpoint", str(target),
        ])
        self.assertEqual(exit_code, 0)
        self.assertEqual(json.loads(line)["checkpoint_status"], "SAVED")
        self.assertEqual(
            fast_save.read_checkpoint_bounded(target)["repository_id"],
            "example-project",
        )

    def test_d3_null_and_wrong_typed_collections_are_state_invalid(self) -> None:
        """D3: a null or wrong-typed collection is refused, never a traceback."""
        for field in ("operations", "changed_files"):
            for bad in (None, {}, "text", 7, True):
                with self.subTest(field=field, value=repr(bad)):
                    state = self._write_state(_state_document(**{field: bad}))
                    with self.assertRaises(fast_save.FastSaveRefused) as refused:
                        fast_save.load_state_document(state)
                    self.assertEqual(refused.exception.reason_code, "STATE_INVALID")
                    self.assertIn(field, refused.exception.reason)
                    self.assertIn(type(bad).__name__, refused.exception.reason)
        # The remaining list fields keep their own type check.
        for field in (
            "completed_work", "remaining_work", "unfinished_files",
            "evidence_references", "failures_blockers", "gaps",
            "authority_references",
        ):
            with self.subTest(field=field):
                state = self._write_state(_state_document(**{field: None}))
                with self.assertRaises(fast_save.FastSaveRefused) as refused:
                    fast_save.load_state_document(state)
                self.assertEqual(refused.exception.reason_code, "STATE_INVALID")
        # End to end: the documented STATE_INVALID JSON and exit 4 replace the
        # uncaught TypeError, and the previous checkpoint is untouched.
        self.assertEqual(self._save().checkpoint_status, "SAVED")
        before = self._sha256(self.checkpoint_path)
        for bad in (None, {}):
            with self.subTest(cli=repr(bad)):
                state = self._write_state(
                    _state_document(operations=bad), name="null-collection.json"
                )
                exit_code, line = self._run_cli([
                    "--repository-id", "example-project", "fast-save",
                    "--state", str(state), "--checkpoint", str(self.checkpoint_path),
                ])
                self.assertEqual(exit_code, 4)
                payload = json.loads(line)
                self.assertEqual(payload["checkpoint_status"], "FAILED")
                self.assertEqual(payload["reason_code"], "STATE_INVALID")
                self.assertIn("operations", payload["reason"])
        self.assertEqual(self._sha256(self.checkpoint_path), before)

    def test_d4_idle_measurement_covers_the_phases_it_names(self) -> None:
        """D4: the number covers the named phases, so a slow phase cannot hide."""
        real_build = fast_save.build_checkpoint

        def slow_build(*args: object, **kwargs: object) -> dict:
            time.sleep(2.0)
            return real_build(*args, **kwargs)

        # (a) capture() with no command start: the document claims the narrower
        # scope, says the state load is NOT included, and the slow build IS
        # visible in the number.
        state = self._write_state()
        request = fast_save.load_state_document(state)
        with mock.patch.object(fast_save, "build_checkpoint", side_effect=slow_build):
            result = fast_save.capture(
                request, self.checkpoint_path, invocation_phrase="fast save"
            )
        self.assertEqual(result.checkpoint_status, "SAVED")
        idle = fast_save.read_checkpoint_bounded(self.checkpoint_path)["idle_measurement"]
        self.assertGreaterEqual(idle["measured_seconds"], 2.0)
        self.assertIn("capture portion", idle["measured_what"])
        self.assertIn("NOT included", idle["measured_what"])
        self.assertIn("never inferred", idle["measured_what"])
        self.assertEqual(
            idle["within_target"],
            idle["measured_seconds"] < idle["target_seconds"],
        )
        # (b) the CLI path: the start instant is taken BEFORE the state load, so a
        # slow load is covered as well and measured_what names that scope.
        target = self.root / "cli-idle-checkpoint.json"
        real_load = fast_save.load_state_document

        def slow_load(path: Path) -> fast_save.SaveRequest:
            time.sleep(2.0)
            return real_load(path)

        with mock.patch.object(
            fast_save, "load_state_document", side_effect=slow_load
        ):
            exit_code, line = self._run_cli([
                "--repository-id", "example-project", "fast-save",
                "--state", str(state), "--checkpoint", str(target),
            ])
        self.assertEqual(exit_code, 0)
        self.assertEqual(json.loads(line)["checkpoint_status"], "SAVED")
        idle = fast_save.read_checkpoint_bounded(target)["idle_measurement"]
        self.assertGreaterEqual(idle["measured_seconds"], 2.0)
        self.assertIn("state-document load", idle["measured_what"])
        self.assertIn("fast-save CLI branch", idle["measured_what"])
        self.assertIn("never inferred", idle["measured_what"])
        self.assertTrue(idle["within_target"])
        self.assertEqual(
            idle["within_target"],
            idle["measured_seconds"] < idle["target_seconds"],
        )

    def test_module_import_has_no_side_effects(self) -> None:
        probe = self.root / "import-probe"
        probe.mkdir()
        script = (
            "import json, os, sys;"
            "before = set(os.listdir(sys.argv[1]));"
            "import tools.aegis_delivery_control.fast_save as fast_save;"
            "after = set(os.listdir(sys.argv[1]));"
            "print(json.dumps({'format': fast_save.CHECKPOINT_FORMAT,"
            " 'created': sorted(after - before), 'removed': sorted(before - after)},"
            " sort_keys=True))"
        )
        completed = subprocess.run(
            [sys.executable, "-B", "-c", script, str(probe)],
            cwd=str(REPO_ROOT), capture_output=True, text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stderr, "")
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["format"], fast_save.CHECKPOINT_FORMAT)
        self.assertEqual(payload["created"], [])
        self.assertEqual(payload["removed"], [])
        self.assertEqual(list(probe.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
