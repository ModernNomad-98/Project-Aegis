from __future__ import annotations

import os
import io
import json
import sqlite3
import stat
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
from tools.aegis_delivery_control.authority import SyntheticAuthority
from tools.aegis_delivery_control.contracts import DispatchDenied
from tools.aegis_delivery_control.cli import (
    ExpectedFreshnessOracle,
    _load_authority,
    _load_expected_vector,
    _status,
    main,
)
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
from tools.aegis_delivery_control.tests import _owner_private_fixtures


def setUpModule() -> None:
    _owner_private_fixtures.enter()


def tearDownModule() -> None:
    _owner_private_fixtures.restore()


class PlatformContractTests(unittest.TestCase):
    @unittest.skipUnless(os.name == "posix", "POSIX mode bits")
    def test_production_creates_owner_private_state_under_permissive_umask(self) -> None:
        # The module runs under an owner-private umask for its fixtures. This
        # test restores a permissive one so it proves production sets its own
        # modes rather than inheriting the fixture umask.
        previous = os.umask(0o022)
        try:
            with tempfile.TemporaryDirectory() as temporary_directory:
                root = Path(temporary_directory)
                database = root / "state.sqlite3"
                SQLiteStateStore(
                    database,
                    ExpectedFreshnessOracle("repo-1", "x", {}),
                    "repo-1",
                )
                effects = root / "effects.sqlite3"
                SyntheticExecutionAdapter(effects)
                for path in (database, root / "writer.lock", effects):
                    with self.subTest(path=path.name):
                        self.assertTrue(path.is_file())
                        self.assertEqual(
                            stat.S_IMODE(path.stat().st_mode) & 0o077, 0
                        )
        finally:
            os.umask(previous)

    @unittest.skipUnless(sys.platform == "win32", "Windows token default owner")
    def test_production_sets_explicit_owner_under_token_default_owner(self) -> None:
        # The module runs with the token's default owner set to the token
        # user for its fixtures. This test puts the process's original
        # default owner back while production creates state, so it proves
        # production sets O:<user> itself. It only discriminates where the
        # original default owner is someone else, such as an elevated
        # runner with User Account Control off (BUILTIN\Administrators).
        fixtures = _owner_private_fixtures
        user = fixtures.token_user_sid()
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            with fixtures.original_default_owner():
                probe = Path(tempfile.mkdtemp(dir=root))
                probe_owner = fixtures.path_owner_sid(probe)
                probe.rmdir()
                if probe_owner == user:
                    self.skipTest(
                        "default owner already equals the token user; "
                        "not discriminating on this host"
                    )
                database = root / "state.sqlite3"
                SQLiteStateStore(
                    database,
                    ExpectedFreshnessOracle("repo-1", "x", {}),
                    "repo-1",
                )
                effects = root / "effects.sqlite3"
                SyntheticExecutionAdapter(effects)
                managed_leaf = root / "managed" / "nested" / "leaf.sqlite3"
                prepare_owned_file(managed_leaf, create=True, trusted_root=root)
            created = [
                database,
                root / "writer.lock",
                effects,
                root / "managed",
                root / "managed" / "nested",
                managed_leaf,
            ]
            for path in created:
                with self.subTest(path=path.relative_to(root).as_posix()):
                    self.assertTrue(path.exists())
                    self.assertEqual(fixtures.path_owner_sid(path), user)

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


def _windows_local_rid500_sid() -> str:
    """Return this machine's built-in Administrator SID (RID 500).

    Derived independently of ``owned_paths``: look up the machine account
    domain SID by computer name and append RID 500.
    """
    import ctypes
    from ctypes import wintypes

    advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    sid = ctypes.create_string_buffer(68)
    sid_size = wintypes.DWORD(len(sid))
    domain = ctypes.create_unicode_buffer(256)
    domain_size = wintypes.DWORD(len(domain))
    use = wintypes.DWORD()
    if not advapi32.LookupAccountNameW(
        None, os.environ["COMPUTERNAME"], sid, ctypes.byref(sid_size),
        domain, ctypes.byref(domain_size), ctypes.byref(use),
    ):
        raise OSError(ctypes.get_last_error(), "LookupAccountNameW failed")
    text = ctypes.c_wchar_p()
    advapi32.ConvertSidToStringSidW.argtypes = [
        ctypes.c_void_p, ctypes.POINTER(ctypes.c_wchar_p)
    ]
    if not advapi32.ConvertSidToStringSidW(sid, ctypes.byref(text)):
        raise OSError(ctypes.get_last_error(), "ConvertSidToStringSidW failed")
    try:
        return f"{text.value}-500"
    finally:
        kernel32.LocalFree.argtypes = [ctypes.c_void_p]
        kernel32.LocalFree(text)


@unittest.skipUnless(sys.platform == "win32", "Windows DACL contract")
class WindowsAclPrincipalTests(unittest.TestCase):
    """The managed-path DACL check compares ACE trustees by SID value.

    SDDL rendering spells well-known SIDs as aliases. The machine's built-in
    Administrator account (RID 500), which GitHub's hosted Windows runner
    uses, is rendered ``LA``, so a text comparison refused production's own
    ``(A;OICI;FA;;;<user>)`` entry.
    """

    PRIVATE = "D:P(A;OICI;FA;;;{user})(A;OICI;FA;;;SY)(A;OICI;FA;;;BA)"

    def _verify(self, user: str, dacl: str, *, os_anchor: bool = False) -> None:
        with patch.object(owned_paths, "_windows_current_sid", return_value=user):
            owned_paths._verify_windows_acl_values(
                user, dacl, managed=not os_anchor, os_anchor=os_anchor
            )

    def test_rid500_user_rendered_as_la_alias_is_accepted(self) -> None:
        user = _windows_local_rid500_sid()
        for spelling in ("LA", user):
            with self.subTest(spelling=spelling):
                self._verify(user, self.PRIVATE.format(user=spelling))

    def test_allowed_principals_match_in_alias_and_full_forms(self) -> None:
        user = _windows_local_rid500_sid()
        self._verify(
            user,
            f"D:P(A;;FA;;;{user})(A;;FA;;;OW)(A;;FA;;;S-1-3-4)"
            "(A;;FA;;;SY)(A;;FA;;;S-1-5-18)(A;;FA;;;BA)(A;;FA;;;S-1-5-32-544)",
        )

    def test_unexpected_principal_is_still_refused(self) -> None:
        user = _windows_local_rid500_sid()
        for extra in ("BU", "AU", "WD", "S-1-5-32-545", "S-1-1-0", "CO", "LG"):
            with self.subTest(principal=extra):
                with self.assertRaisesRegex(
                    PathCapabilityUnavailable, "unexpected principal"
                ):
                    self._verify(
                        user,
                        self.PRIVATE.format(user=user) + f"(A;OICI;FA;;;{extra})",
                    )

    def test_la_is_refused_when_the_user_is_someone_else(self) -> None:
        other = "S-1-5-21-1-2-3-1001"
        with self.assertRaisesRegex(PathCapabilityUnavailable, "unexpected principal"):
            self._verify(other, self.PRIVATE.format(user=other) + "(A;;FA;;;LA)")

    def test_unresolvable_trustee_is_refused(self) -> None:
        user = _windows_local_rid500_sid()
        for bogus in ("NOT-A-SID", "S-1-", "ZZ", ""):
            for os_anchor in (False, True):
                with self.subTest(trustee=bogus, os_anchor=os_anchor):
                    with self.assertRaisesRegex(
                        PathCapabilityUnavailable, "unresolvable principal"
                    ):
                        self._verify(
                            user,
                            self.PRIVATE.format(user=user) + f"(A;;FR;;;{bogus})",
                            os_anchor=os_anchor,
                        )

    def test_os_anchor_still_allows_read_only_other_principals(self) -> None:
        user = _windows_local_rid500_sid()
        self._verify(
            user, self.PRIVATE.format(user=user) + "(A;OICI;FR;;;BU)", os_anchor=True
        )
        with self.assertRaisesRegex(PathCapabilityUnavailable, "unexpected principal"):
            self._verify(
                user, self.PRIVATE.format(user=user) + "(A;OICI;FA;;;BU)", os_anchor=True
            )


class CliInputFileTests(unittest.TestCase):
    """P3-15 and P3-19: CLI input files and OS errors on the verify path."""

    def _write(self, root: Path, name: str, value: object, *, bom: bool) -> Path:
        path = root / name
        text = json.dumps(value)
        path.write_bytes(("﻿" + text if bom else text).encode("utf-8"))
        return path

    def test_expected_vector_accepts_utf8_bom(self) -> None:
        # Windows PowerShell 5.1 Out-File writes a UTF-8 byte-order mark.
        vector = {
            "repository_id": "repo-1",
            "catalog_head": "catalog-1",
            "run_heads": {"run-1": "head-1"},
        }
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            for bom in (False, True):
                with self.subTest(bom=bom):
                    path = self._write(root, f"vector-{bom}.json", vector, bom=bom)
                    self.assertEqual(
                        _load_expected_vector(path),
                        ("repo-1", "catalog-1", {"run-1": "head-1"}),
                    )

    def test_authority_key_file_accepts_utf8_bom(self) -> None:
        key = {"synthetic_issuer_key_hex": "ab" * 32}
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            for bom in (False, True):
                with self.subTest(bom=bom):
                    path = self._write(root, f"key-{bom}.json", key, bom=bom)
                    self.assertEqual(
                        _load_authority(path).issuer_fingerprint,
                        SyntheticAuthority(bytes.fromhex("ab" * 32)).issuer_fingerprint,
                    )

    def test_verify_reports_os_error_as_exit_code_three(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            database = root / "state.sqlite3"
            database.write_bytes(b"")
            vector = self._write(
                root, "vector.json",
                {"repository_id": "repo-1", "catalog_head": "c", "run_heads": {}},
                bom=False,
            )
            key = self._write(
                root, "key.json", {"synthetic_issuer_key_hex": "ab" * 32},
                bom=False,
            )
            stderr = io.StringIO()
            with patch(
                "tools.aegis_delivery_control.cli._database_path",
                return_value=database,
            ), patch(
                "tools.aegis_delivery_control.cli.SQLiteStateStore.open_canonical",
                side_effect=OSError("synthetic disk error"),
            ), redirect_stderr(stderr):
                result = main([
                    "--repository-id", "repo-1", "verify",
                    "--expected-vector", str(vector),
                    "--authority-key-file", str(key),
                ])
            self.assertEqual(result, 3)
            self.assertIn("verification failed: synthetic disk error", stderr.getvalue())


class CheckedConnectionCommitTests(unittest.TestCase):
    """P3-18: the owned path is checked before and after a commit."""

    def _open(self, root: Path) -> tuple[Path, owned_paths.CheckedSQLiteConnection]:
        path = root / "owned.sqlite3"
        identity = prepare_owned_file(path, create=True, trusted_root=root)
        connection = connect_checked(path, expected=identity, trusted_root=root)
        connection.execute("CREATE TABLE facts (value TEXT NOT NULL)")
        return path, connection

    @staticmethod
    def _rows(path: Path) -> list[tuple[str]]:
        with closing(sqlite3.connect(path)) as reader:
            return reader.execute("SELECT value FROM facts").fetchall()

    def test_commit_refuses_to_write_when_owned_path_changed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path, connection = self._open(Path(temporary_directory))
            try:
                connection.execute("BEGIN IMMEDIATE")
                connection.execute("INSERT INTO facts VALUES ('pending')")
                capability = connection._owned_path_capability
                with patch.object(
                    capability, "assert_current",
                    side_effect=PathCapabilityUnavailable("owned path swapped"),
                ):
                    with self.assertRaisesRegex(
                        PathCapabilityUnavailable, "owned path swapped"
                    ) as raised:
                        connection.commit()
                self.assertNotIsInstance(
                    raised.exception, owned_paths.OwnedPathChangedAfterCommit
                )
                self.assertTrue(connection.in_transaction)
                connection.rollback()
            finally:
                connection.close()
            self.assertEqual(self._rows(path), [])

    def test_commit_reports_committed_write_when_path_changes_after(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path, connection = self._open(Path(temporary_directory))
            try:
                connection.execute("BEGIN IMMEDIATE")
                connection.execute("INSERT INTO facts VALUES ('durable')")
                capability = connection._owned_path_capability
                original = capability.assert_current
                calls = []

                def fail_after_commit() -> None:
                    calls.append(connection.in_transaction)
                    if not connection.in_transaction:
                        raise PathCapabilityUnavailable("owned path swapped")
                    original()

                with patch.object(
                    capability, "assert_current", side_effect=fail_after_commit
                ):
                    with self.assertRaisesRegex(
                        owned_paths.OwnedPathChangedAfterCommit, "committed"
                    ) as raised:
                        connection.commit()
                self.assertIsInstance(raised.exception, PathCapabilityUnavailable)
                self.assertEqual(calls, [True, False])
            finally:
                connection.close()
            self.assertEqual(self._rows(path), [("durable",)])

    def test_committed_signal_survives_production_rollback_pattern(self) -> None:
        # Production call sites do: try: commit() except BaseException:
        # rollback(); raise. The rollback must not replace the typed signal.
        with tempfile.TemporaryDirectory() as temporary_directory:
            path, connection = self._open(Path(temporary_directory))
            try:
                connection.execute("BEGIN IMMEDIATE")
                connection.execute("INSERT INTO facts VALUES ('durable')")
                capability = connection._owned_path_capability
                original = capability.assert_current

                def fail_after_commit() -> None:
                    if not connection.in_transaction:
                        raise PathCapabilityUnavailable("owned path swapped")
                    original()

                with patch.object(
                    capability, "assert_current", side_effect=fail_after_commit
                ):
                    with self.assertRaises(
                        owned_paths.OwnedPathChangedAfterCommit
                    ):
                        try:
                            connection.commit()
                        except BaseException:
                            connection.rollback()
                            raise
                # The marker is kept until close(): a later rollback with no
                # open transaction still reports the durable write.
                with self.assertRaises(owned_paths.OwnedPathChangedAfterCommit):
                    connection.rollback()
            finally:
                connection.close()
            self.assertEqual(self._rows(path), [("durable",)])

    def _persistent_swap(self, connection):
        """Swap the path during commit and keep it swapped through close()."""
        capability = connection._owned_path_capability
        original = capability.assert_current
        state = {"armed": False, "swapped": False}

        def check() -> None:
            if state["swapped"] or (state["armed"] and not connection.in_transaction):
                state["swapped"] = True
                raise PathCapabilityUnavailable("owned path swapped")
            original()

        return state, patch.object(capability, "assert_current", side_effect=check)

    def test_committed_signal_survives_closing_pattern(self) -> None:
        # storage.py and adapters.py: with closing(connect()) as connection.
        with tempfile.TemporaryDirectory() as temporary_directory:
            path, connection = self._open(Path(temporary_directory))
            state, swap = self._persistent_swap(connection)
            with swap:
                with self.assertRaises(
                    owned_paths.OwnedPathChangedAfterCommit
                ) as raised:
                    with closing(connection) as active:
                        active.execute("BEGIN IMMEDIATE")
                        active.execute("INSERT INTO facts VALUES ('durable')")
                        state["armed"] = True
                        try:
                            active.commit()
                        except BaseException:
                            active.rollback()
                            raise
            self.assertTrue(state["swapped"])
            self.assertIsInstance(raised.exception.__cause__, PathCapabilityUnavailable)
            self.assertIsNone(connection._owned_path_capability)
            self.assertEqual(self._rows(path), [("durable",)])

    def test_committed_signal_survives_finally_close_pattern(self) -> None:
        # authority.py: try: ... commit() except: rollback(); raise
        # finally: connection.close().
        with tempfile.TemporaryDirectory() as temporary_directory:
            path, connection = self._open(Path(temporary_directory))
            state, swap = self._persistent_swap(connection)
            with swap:
                with self.assertRaises(owned_paths.OwnedPathChangedAfterCommit):
                    try:
                        connection.execute("BEGIN IMMEDIATE")
                        connection.execute("INSERT INTO facts VALUES ('durable')")
                        state["armed"] = True
                        connection.commit()
                    except BaseException:
                        connection.rollback()
                        raise
                    finally:
                        connection.close()
            self.assertTrue(state["swapped"])
            self.assertIsNone(connection._owned_path_capability)
            self.assertEqual(self._rows(path), [("durable",)])

    def test_close_without_lost_commit_still_reports_plain_path_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            _, connection = self._open(Path(temporary_directory))
            capability = connection._owned_path_capability
            with patch.object(
                capability, "assert_current",
                side_effect=PathCapabilityUnavailable("owned path swapped"),
            ):
                with self.assertRaises(PathCapabilityUnavailable) as raised:
                    connection.close()
            self.assertNotIsInstance(
                raised.exception, owned_paths.OwnedPathChangedAfterCommit
            )
            self.assertIsNone(connection._owned_path_capability)


if __name__ == "__main__":
    unittest.main()
