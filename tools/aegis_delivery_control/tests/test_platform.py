from __future__ import annotations

import os
import io
import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from contextlib import closing, redirect_stderr, redirect_stdout
from types import SimpleNamespace
from unittest.mock import patch

import tools.aegis_delivery_control.owned_paths as owned_paths
from tools.aegis_delivery_control.adapters import (
    SyntheticExecutionAdapter,
    SyntheticValidatorAdapter,
)
from tools.aegis_delivery_control.contracts import DispatchDenied
from tools.aegis_delivery_control.cli import ExpectedFreshnessOracle, _status, main
from tools.aegis_delivery_control.owned_paths import (
    CheckedPathCapability,
    PathCapabilityUnavailable,
    connect_checked,
    prepare_owned_file,
    probe_owned_path_identity,
)
from tools.aegis_delivery_control.storage import (
    RepositoryWriterLock,
    SQLiteStateStore,
    default_state_root,
)


class PlatformContractTests(unittest.TestCase):
    def test_offline_owned_path_probe_denies_swap_and_hardlink(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            leaf = root / "synthetic.sqlite3"
            leaf.write_bytes(b"first")
            expected = prepare_owned_file(leaf, create=False, trusted_root=root)
            self.assertEqual(
                probe_owned_path_identity(leaf, expected=expected, trusted_root=root),
                expected,
            )
            leaf.rename(root / "old.sqlite3")
            leaf.write_bytes(b"second")
            with self.assertRaises(PathCapabilityUnavailable):
                probe_owned_path_identity(leaf, expected=expected, trusted_root=root)
            replacement_identity = prepare_owned_file(
                leaf, create=False, trusted_root=root
            )
            os.link(leaf, root / "alias.sqlite3")
            with self.assertRaisesRegex(PathCapabilityUnavailable, "single-link"):
                probe_owned_path_identity(
                    leaf,
                    expected=replacement_identity,
                    trusted_root=root,
                )

    def test_posix_traversal_requires_no_follow_and_directory_flags(self) -> None:
        for flag in ("O_NOFOLLOW", "O_DIRECTORY"):
            with self.subTest(flag=flag):
                with patch.object(owned_paths.os, flag, None, create=True):
                    with self.assertRaisesRegex(
                        PathCapabilityUnavailable,
                        "no-follow directory traversal",
                    ):
                        owned_paths._posix_open_flags()

    def test_posix_ancestor_policy_rejects_hostile_owner_and_sticky_child(self) -> None:
        with patch.object(owned_paths.os, "geteuid", return_value=1000, create=True):
            hostile = SimpleNamespace(st_mode=0o040755, st_uid=2000)
            with self.assertRaisesRegex(
                PathCapabilityUnavailable, "untrusted owner"
            ):
                owned_paths._validate_posix_ancestor(hostile, False)

            sticky = SimpleNamespace(st_mode=0o041777, st_uid=0)
            self.assertTrue(
                owned_paths._validate_posix_ancestor(sticky, False)
            )
            hostile_child = SimpleNamespace(st_mode=0o040700, st_uid=2000)
            with self.assertRaisesRegex(
                PathCapabilityUnavailable, "untrusted owner|owner-private"
            ):
                owned_paths._validate_posix_ancestor(hostile_child, True)
            private_child = SimpleNamespace(st_mode=0o040700, st_uid=1000)
            self.assertFalse(
                owned_paths._validate_posix_ancestor(private_child, True)
            )

    @unittest.skipUnless(sys.platform == "win32", "Windows contract")
    def test_windows_known_folder_ignores_localappdata_and_requires_fixed_drive(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            with patch.dict(
                os.environ, {"LOCALAPPDATA": temporary_directory}
            ):
                selected = owned_paths.known_local_state_base()
            self.assertNotEqual(
                os.path.normcase(str(selected)),
                os.path.normcase(temporary_directory),
            )
            path = Path(temporary_directory) / "state.sqlite3"
            path.write_bytes(b"database")
            with patch.object(
                owned_paths._kernel32, "GetDriveTypeW", return_value=2
            ):
                with self.assertRaisesRegex(
                    PathCapabilityUnavailable, "fixed Windows drive"
                ):
                    prepare_owned_file(path, create=False)

    @unittest.skipUnless(sys.platform == "win32", "Windows contract")
    def test_windows_known_folder_rejects_same_volume_path_rebound(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            database = root / "state.sqlite3"
            database.write_bytes(b"database")
            rebound = root.parent / f"{root.name}-rebound"
            rebound.mkdir()
            try:
                with patch.object(
                    owned_paths,
                    "_windows_final_path",
                    return_value=str(rebound),
                ):
                    with self.assertRaisesRegex(
                        PathCapabilityUnavailable, "path does not match"
                    ):
                        prepare_owned_file(
                            database,
                            create=False,
                            trusted_root=root,
                            os_known_root=True,
                        )
            finally:
                rebound.rmdir()

    @unittest.skipUnless(sys.platform == "win32", "Windows contract")
    def test_windows_owned_file_rejects_everyone_writable_acl_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            database = root / "state.sqlite3"
            database.write_bytes(b"database")
            grant = subprocess.run(
                [
                    "icacls",
                    str(database),
                    "/grant:r",
                    "*S-1-1-0:(F)",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(grant.returncode, 0, grant.stderr)
            before = {
                path.name: path.read_bytes()
                for path in root.iterdir()
                if path.is_file()
            }
            with self.assertRaisesRegex(
                PathCapabilityUnavailable, "unexpected principal"
            ):
                prepare_owned_file(database, create=False)
            after = {
                path.name: path.read_bytes()
                for path in root.iterdir()
                if path.is_file()
            }
            self.assertEqual(after, before)

    def test_owned_path_rejects_lexical_escape_and_windows_aliases(self) -> None:
        candidates = (
            Path("relative/state.sqlite3"),
            Path(r"\\server\share\state.sqlite3"),
            Path(r"C:\safe\..\state.sqlite3"),
            Path(r"C:\safe\state.sqlite3:stream"),
            Path(r"C:\safe\NUL.sqlite3"),
            Path(r"C:\safe\trailing.\state.sqlite3"),
        )
        for candidate in candidates:
            with self.subTest(path=str(candidate)):
                with self.assertRaises(PathCapabilityUnavailable):
                    CheckedPathCapability(
                        candidate, create=False, read_only=True
                    )

    def test_checked_leaf_prevents_or_detects_replacement(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            path = root / "state.sqlite3"
            path.write_bytes(b"original")
            replacement = root / "replacement.sqlite3"
            replacement.write_bytes(b"replacement")
            capability = CheckedPathCapability(
                path, create=False, read_only=False
            )
            try:
                if sys.platform == "win32":
                    with self.assertRaises(PermissionError):
                        os.replace(replacement, path)
                    self.assertEqual(path.read_bytes(), b"original")
                else:
                    os.replace(replacement, path)
                    with self.assertRaisesRegex(
                        PathCapabilityUnavailable, "identity"
                    ):
                        capability.assert_current()
                    self.assertEqual(path.read_bytes(), b"replacement")
            finally:
                capability.close()

    def test_checked_ancestor_prevents_or_detects_replacement(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            managed = root / "managed"
            parent = managed / "nested"
            parent.mkdir(parents=True)
            path = parent / "state.sqlite3"
            path.write_bytes(b"original")
            replacement = root / "replacement"
            replacement_parent = replacement / "nested"
            replacement_parent.mkdir(parents=True)
            (replacement_parent / "state.sqlite3").write_bytes(b"replacement")
            capability = CheckedPathCapability(
                path,
                create=False,
                read_only=False,
                trusted_root=root,
            )
            moved = root / "moved"
            try:
                if sys.platform == "win32":
                    with self.assertRaises(PermissionError):
                        os.replace(managed, moved)
                else:
                    os.replace(managed, moved)
                    os.replace(replacement, managed)
                    with self.assertRaisesRegex(
                        PathCapabilityUnavailable, "identity"
                    ):
                        capability.assert_current()
            finally:
                capability.close()

    def test_connect_failure_releases_checked_handles(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            database = root / "state.sqlite3"
            connection = sqlite3.connect(database)
            connection.close()
            identity = prepare_owned_file(database, create=False)
            failure = PathCapabilityUnavailable("synthetic post-connect failure")
            with patch.object(
                CheckedPathCapability,
                "assert_current",
                side_effect=[failure, None],
            ):
                with self.assertRaisesRegex(
                    PathCapabilityUnavailable, "synthetic post-connect"
                ):
                    connect_checked(database, expected=identity)
            replacement = root / "replacement.sqlite3"
            replacement.write_bytes(b"replacement")
            os.replace(replacement, database)
            self.assertEqual(database.read_bytes(), b"replacement")

    def test_adapter_ledgers_refuse_leaf_replacement(self) -> None:
        for adapter_type, filename in (
            (SyntheticExecutionAdapter, "effects.sqlite3"),
            (SyntheticValidatorAdapter, "validators.sqlite3"),
        ):
            with self.subTest(adapter=adapter_type.__name__):
                with tempfile.TemporaryDirectory() as temporary_directory:
                    root = Path(temporary_directory)
                    path = root / filename
                    adapter = adapter_type(path)
                    replacement = root / "replacement.sqlite3"
                    replacement.write_bytes(path.read_bytes())
                    os.replace(replacement, path)
                    with self.assertRaisesRegex(
                        PathCapabilityUnavailable, "identity changed"
                    ):
                        adapter.reconcile("missing-claim")

    def test_hardlinked_database_and_sqlite_wal_sidecar_are_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            original = root / "original.sqlite3"
            original.write_bytes(b"database")
            linked = root / "linked.sqlite3"
            os.link(original, linked)
            with self.assertRaisesRegex(
                PathCapabilityUnavailable, "single-link"
            ):
                prepare_owned_file(linked, create=False)

            safe = root / "safe.sqlite3"
            safe.write_bytes(b"database")
            wal = Path(str(safe) + "-wal")
            wal.write_bytes(b"unexpected")
            before = wal.read_bytes()
            with self.assertRaisesRegex(
                PathCapabilityUnavailable, "sidecar"
            ):
                prepare_owned_file(safe, create=False)
            self.assertEqual(wal.read_bytes(), before)
            wal.unlink()
            safe.unlink()

    def test_checked_connection_accepts_owned_crash_journal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            database = root / "state.sqlite3"
            connection = sqlite3.connect(database)
            try:
                connection.execute("CREATE TABLE values_table (value INTEGER)")
                connection.execute("INSERT INTO values_table VALUES (1)")
                connection.commit()
            finally:
                connection.close()
            database.chmod(0o600)
            crashed = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    (
                        "import os, sqlite3, sys; "
                        "connection = sqlite3.connect(sys.argv[1]); "
                        "connection.execute('PRAGMA journal_mode = DELETE'); "
                        "connection.execute('PRAGMA synchronous = FULL'); "
                        "connection.execute('BEGIN IMMEDIATE'); "
                        "connection.execute('UPDATE values_table SET value = 2'); "
                        "os._exit(0)"
                    ),
                    str(database),
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=5,
            )
            self.assertEqual(crashed.returncode, 0, crashed.stderr)
            journal = Path(str(database) + "-journal")
            self.assertTrue(journal.is_file())
            journal.chmod(0o600)
            identity = prepare_owned_file(database, create=False)
            with closing(connect_checked(database, expected=identity)) as checked:
                value = checked.execute(
                    "SELECT value FROM values_table"
                ).fetchone()[0]
            self.assertEqual(value, 1)

    def test_hardlinked_rollback_journal_is_refused_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            database = root / "state.sqlite3"
            database.write_bytes(b"database")
            source = root / "foreign-journal"
            source.write_bytes(b"journal")
            journal = Path(str(database) + "-journal")
            os.link(source, journal)
            before = {path.name: path.read_bytes() for path in root.iterdir()}
            with self.assertRaisesRegex(
                PathCapabilityUnavailable, "rollback journal"
            ):
                prepare_owned_file(database, create=False)
            after = {path.name: path.read_bytes() for path in root.iterdir()}
            self.assertEqual(after, before)

    def test_existing_state_without_stable_writer_lock_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            database = root / "state.sqlite3"
            SQLiteStateStore(database, ExpectedFreshnessOracle("repo-1", "x", {}), "repo-1")
            lock_path = root / "writer.lock"
            lock_path.unlink()
            before = database.read_bytes()
            with self.assertRaisesRegex(
                PathCapabilityUnavailable, "does not exist"
            ):
                SQLiteStateStore(
                    database,
                    ExpectedFreshnessOracle("repo-1", "x", {}),
                    "repo-1",
                )
            self.assertEqual(database.read_bytes(), before)
            self.assertFalse(lock_path.exists())

    def test_store_refuses_replaced_writer_lock_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            database = root / "state.sqlite3"
            store = SQLiteStateStore(
                database,
                ExpectedFreshnessOracle("repo-1", "x", {}),
                "repo-1",
            )
            lock_path = root / "writer.lock"
            original = lock_path.read_bytes()
            replacement = root / "replacement.lock"
            replacement.write_bytes(original)
            os.replace(replacement, lock_path)
            with self.assertRaisesRegex(
                PathCapabilityUnavailable, "identity changed"
            ):
                with store._writer_lock():
                    self.fail("replaced lock must never be acquired")

    def test_canonical_state_refuses_actual_redirect_before_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            selected_base = root / "selected"
            selected_base.mkdir()
            redirect_target = root / "redirect-target"
            redirect_target.mkdir()
            product = "ProjectAegis" if sys.platform == "win32" else "project-aegis"
            redirected_component = selected_base / product
            if sys.platform == "win32":
                result = subprocess.run(
                    [
                        "cmd", "/c", "mklink", "/J",
                        str(redirected_component), str(redirect_target),
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
            else:
                redirected_component.symlink_to(
                    redirect_target, target_is_directory=True
                )
            before = tuple(redirect_target.rglob("*"))
            try:
                with patch(
                    "tools.aegis_delivery_control.storage.known_local_state_base",
                    return_value=selected_base,
                ):
                    factories = (
                        lambda: SQLiteStateStore.open_canonical(
                            "repo-redirect",
                            ExpectedFreshnessOracle(
                                "repo-redirect", "catalog", {}
                            ),
                        ),
                        lambda: SyntheticExecutionAdapter.open_canonical(
                            "repo-redirect"
                        ),
                        lambda: SyntheticValidatorAdapter.open_canonical(
                            "repo-redirect"
                        ),
                    )
                    for factory in factories:
                        with self.subTest(factory=factory):
                            with self.assertRaisesRegex(
                                PathCapabilityUnavailable,
                                "reparse|redirect|symlink",
                            ):
                                factory()
                self.assertEqual(tuple(redirect_target.rglob("*")), before)
                self.assertFalse((selected_base / "writer.lock").exists())
            finally:
                if redirected_component.is_symlink():
                    redirected_component.unlink()
                elif redirected_component.exists():
                    os.rmdir(redirected_component)

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

    def test_cli_routes_handle_unavailable_canonical_root_without_traceback(self) -> None:
        unavailable = PathCapabilityUnavailable("known state root unavailable")
        with patch(
            "tools.aegis_delivery_control.storage.known_local_state_base",
            side_effect=unavailable,
        ):
            capabilities_output = io.StringIO()
            with redirect_stdout(capabilities_output):
                capabilities_result = main(
                    ["--repository-id", "repo-1", "capabilities"]
                )
            self.assertEqual(capabilities_result, 0)
            self.assertFalse(
                json.loads(capabilities_output.getvalue())["external_io"]
            )

            status_output = io.StringIO()
            with redirect_stdout(status_output):
                status_result = main(["--repository-id", "repo-1", "status"])
            status = json.loads(status_output.getvalue())
            self.assertEqual(status_result, 0)
            self.assertFalse(status["initialized"])
            self.assertFalse(status["verified"])
            self.assertEqual(status["path_capability"], "UNAVAILABLE")
            self.assertIsNone(status["database"])

            verify_error = io.StringIO()
            with redirect_stderr(verify_error):
                verify_result = main(
                    [
                        "--repository-id",
                        "repo-1",
                        "verify",
                        "--expected-vector",
                        "missing-vector.json",
                        "--authority-key-file",
                        "missing-authority.json",
                    ]
                )
            self.assertEqual(verify_result, 3)
            self.assertIn("verification failed", verify_error.getvalue())

    def test_explicit_store_does_not_discover_unrelated_canonical_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            database = Path(temporary_directory) / "state.sqlite3"
            with patch(
                "tools.aegis_delivery_control.storage.known_local_state_base",
                side_effect=PathCapabilityUnavailable(
                    "known state root unavailable"
                ),
            ):
                store = SQLiteStateStore(
                    database,
                    ExpectedFreshnessOracle("repo-1", "catalog-1", {}),
                    "repo-1",
                )
            self.assertFalse(store.is_canonical)
            self.assertTrue(database.is_file())

    def test_cli_status_does_not_create_state(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            output = io.StringIO()
            environment = {"XDG_STATE_HOME": str(root)}
            state_base = (
                patch(
                    "tools.aegis_delivery_control.storage.known_local_state_base",
                    return_value=root,
                )
                if sys.platform == "win32"
                else patch.dict(os.environ, environment)
            )
            with state_base, redirect_stdout(output):
                result = main(
                    ["--repository-id", "repo-1", "status"]
                )
            self.assertEqual(result, 0)
            self.assertIn('"initialized": false', output.getvalue())
            self.assertEqual(list(root.rglob("*")), [])

    def test_cli_status_reports_unsafe_path_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            original = root / "original.sqlite3"
            original.write_bytes(b"database")
            database = root / "state.sqlite3"
            os.link(original, database)
            before = {path.name: path.read_bytes() for path in root.iterdir()}
            result = _status(database)
            after = {path.name: path.read_bytes() for path in root.iterdir()}
            self.assertFalse(result["initialized"])
            self.assertFalse(result["verified"])
            self.assertEqual(result["path_capability"], "UNAVAILABLE")
            self.assertEqual(after, before)

    def test_cli_status_preserves_initialized_state_bytes_and_names(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            database = root / "state.sqlite3"
            SQLiteStateStore(
                database,
                ExpectedFreshnessOracle("repo-1", "catalog-1", {}),
                "repo-1",
            )
            before = {
                path.name: path.read_bytes()
                for path in root.iterdir()
                if path.is_file()
            }
            result = _status(database)
            after = {
                path.name: path.read_bytes()
                for path in root.iterdir()
                if path.is_file()
            }
            self.assertTrue(result["initialized"])
            self.assertEqual(result["path_capability"], "VERIFIED")
            self.assertEqual(after, before)

    def test_cli_capabilities_runs_as_module_in_isolated_environment(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            environment = os.environ.copy()
            state_variable = (
                "LOCALAPPDATA" if sys.platform == "win32" else "XDG_STATE_HOME"
            )
            environment[state_variable] = str(root)
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "tools.aegis_delivery_control",
                    "--repository-id",
                    "repo-1",
                    "capabilities",
                ],
                cwd=Path(__file__).parents[3],
                env=environment,
                capture_output=True,
                text=True,
                check=False,
                timeout=5,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stderr, "")
            capabilities = json.loads(result.stdout)
            self.assertFalse(capabilities["external_io"])
            self.assertFalse(capabilities["real_adapters"])
            self.assertEqual(list(root.rglob("*")), [])

    def test_state_root_uses_repository_identity_not_checkout_name(self) -> None:
        if sys.platform == "win32":
            with patch(
                "tools.aegis_delivery_control.storage.known_local_state_base",
                return_value=Path(r"C:\State"),
            ):
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
            with RepositoryWriterLock(state_root, allow_create=True):
                result = subprocess.run(
                    [sys.executable, "-c", script],
                    cwd=Path(__file__).parents[3],
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=5,
                )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("repository writer lock is unavailable", result.stderr)
            self.assertTrue((state_root / "writer.lock").exists())

    def test_lock_can_be_reacquired_without_deleting_lock_object(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            state_root = Path(temporary_directory)
            with RepositoryWriterLock(state_root, allow_create=True):
                lock_path = state_root / "writer.lock"
                self.assertTrue(lock_path.exists())
            with RepositoryWriterLock(state_root):
                self.assertTrue(lock_path.exists())


if __name__ == "__main__":
    unittest.main()
