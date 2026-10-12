"""Command interface for the offline synthetic kernel.

capabilities, status and verify are read-only. fast-save is the single command
that writes: it writes exactly one JSON checkpoint file at the path the operator
names, and it opens no state database.
"""

from __future__ import annotations

import argparse
from contextlib import closing
import json
import sqlite3
import sys
from pathlib import Path
from typing import Mapping, Sequence

from . import ci_durations
from . import fast_save
from .authority import SyntheticAuthority
from .contracts import DispatchDenied, StorageIntegrityError
from .storage import SQLiteStateStore, default_state_root
from .owned_paths import (
    PathCapabilityUnavailable,
    connect_checked,
    nearest_existing_trusted_root,
    prepare_owned_file,
)


class ExpectedFreshnessOracle:
    """Synthetic CLI oracle requiring an independent complete head vector."""

    def __init__(
        self,
        repository_id: str,
        catalog_head: str,
        run_heads: Mapping[str, str],
    ) -> None:
        self._repository_id = repository_id
        self._catalog_head = catalog_head
        self._run_heads = dict(run_heads)

    def verify(
        self,
        repository_id: str,
        catalog_head: str,
        run_heads: Mapping[str, str],
    ) -> bool:
        return (
            bool(self._catalog_head)
            and repository_id == self._repository_id
            and catalog_head == self._catalog_head
            and dict(run_heads) == self._run_heads
        )


def _load_expected_vector(path: Path) -> tuple[str, str, dict[str, str]]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError("expected vector must be readable JSON") from error
    if not isinstance(value, dict) or set(value) != {
        "repository_id",
        "catalog_head",
        "run_heads",
    }:
        raise ValueError("expected vector has an invalid schema")
    repository_id = value["repository_id"]
    catalog_head = value["catalog_head"]
    run_heads = value["run_heads"]
    if (
        not isinstance(repository_id, str)
        or not repository_id
        or not isinstance(catalog_head, str)
        or not catalog_head
        or not isinstance(run_heads, dict)
        or any(
            not isinstance(run_id, str)
            or not run_id
            or not isinstance(head, str)
            or not head
            for run_id, head in run_heads.items()
        )
    ):
        raise ValueError("expected vector values must be non-empty strings")
    return repository_id, catalog_head, dict(run_heads)


def _load_authority(path: Path) -> SyntheticAuthority:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError("authority key file must be readable JSON") from error
    if not isinstance(value, dict) or set(value) != {
        "synthetic_issuer_key_hex"
    }:
        raise ValueError("authority key file has an invalid schema")
    key_hex = value["synthetic_issuer_key_hex"]
    if (
        not isinstance(key_hex, str)
        or len(key_hex) < 64
        or len(key_hex) % 2 != 0
        or any(character not in "0123456789abcdefABCDEF" for character in key_hex)
    ):
        raise ValueError("synthetic issuer key must be canonical hexadecimal")
    return SyntheticAuthority(bytes.fromhex(key_hex))


def _fast_save_report(result: fast_save.SaveResult) -> dict[str, object]:
    document = result.document
    return {
        "checkpoint_status": result.checkpoint_status,
        "reason_code": result.reason_code,
        "reason": result.reason,
        "execution_status": None if document is None else document["execution_status"],
        "execution_status_source": None
        if document is None
        else document["execution_status_source"],
        "durable_location": result.durable_location,
        "bounded_readback": result.bounded_readback,
        "one_line_resume": result.one_line_resume,
    }


def _fast_save_refusal(error: fast_save.FastSaveRefused) -> dict[str, object]:
    return {
        "checkpoint_status": "FAILED",
        "reason_code": error.reason_code,
        "reason": error.reason,
        "execution_status": None,
        "execution_status_source": None,
        "durable_location": None,
        "bounded_readback": None,
        "one_line_resume": None,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m tools.aegis_delivery_control",
        description=(
            "Read-only for capabilities, status and verify; fast-save is the "
            "single command that writes one checkpoint file at the path the "
            "operator names."
        ),
    )
    parser.add_argument("--repository-id", required=True)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("capabilities")
    subparsers.add_parser("status")
    verify = subparsers.add_parser("verify")
    verify.add_argument("--expected-vector", required=True, type=Path)
    verify.add_argument("--authority-key-file", required=True, type=Path)
    ci_durations.build_parser(subparsers)
    fast_save_parser = subparsers.add_parser("fast-save")
    fast_save_parser.add_argument("--state", required=True, type=Path)
    fast_save_parser.add_argument("--checkpoint", required=True, type=Path)
    fast_save_parser.add_argument("--invocation-phrase", default="fast save")
    return parser


def _database_path(arguments: argparse.Namespace) -> Path:
    return default_state_root(arguments.repository_id) / "state.sqlite3"


def _status(
    database_path: Path,
    *,
    trusted_root: Path | None = None,
    os_known_root: bool = False,
) -> dict[str, object]:
    trusted_root = trusted_root or nearest_existing_trusted_root(
        database_path.parent
    )
    try:
        identity = prepare_owned_file(
            database_path,
            create=False,
            trusted_root=trusted_root,
            os_known_root=os_known_root,
        )
        with closing(connect_checked(
            database_path,
            expected=identity,
            read_only=True,
            trusted_root=trusted_root,
            os_known_root=os_known_root,
        )) as connection:
            repository = connection.execute(
                "SELECT repository_id, catalog_head FROM repositories LIMIT 1"
            ).fetchone()
            slot = connection.execute(
                "SELECT run_id, logical_effect_id, attempt_id, generation "
                "FROM outstanding_slot"
            ).fetchone()
            fences = connection.execute(
                "SELECT COUNT(*) FROM dispatch_fences"
            ).fetchone()[0]
    except (PathCapabilityUnavailable, sqlite3.Error, OSError) as error:
        return {
            "initialized": False,
            "database": str(database_path),
            "path_capability": "UNAVAILABLE",
            "verified": False,
            "reason": str(error),
        }
    return {
        "initialized": True,
        "database": str(database_path),
        "path_capability": "VERIFIED",
        "repository_id": None if repository is None else repository[0],
        "catalog_head": None if repository is None else repository[1],
        "outstanding_slot": None
        if slot is None
        else {
            "run_id": slot[0],
            "logical_effect_id": slot[1],
            "attempt_id": slot[2],
            "generation": slot[3],
        },
        "dispatch_fence_count": fences,
    }


def main(argv: Sequence[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    if arguments.command == "fast-save":
        # Taken BEFORE the state document is loaded, so idle_measurement really
        # covers the state load and validation that measured_what names.
        command_started = fast_save.start_idle_measurement()
        try:
            request = fast_save.load_state_document(arguments.state)
            # The checkpoint is bound to this CLI identity: a state document from
            # another repository is refused here, before anything is written.
            fast_save.bind_repository_identity(request, arguments.repository_id)
        except fast_save.FastSaveRefused as error:
            print(json.dumps(_fast_save_refusal(error), sort_keys=True))
            return 4
        result = fast_save.capture(
            request,
            arguments.checkpoint,
            invocation_phrase=arguments.invocation_phrase,
            command_started_monotonic=command_started,
        )
        print(json.dumps(_fast_save_report(result), sort_keys=True))
        return 0 if result.checkpoint_status == "SAVED" else 4
    if arguments.command == "capabilities":
        print(
            json.dumps(
                {
                    "authority": "synthetic-only",
                    "external_io": False,
                    "git_mutation": False,
                    "lifecycle_cli_mutation": False,
                    "power_loss_durability_proven": False,
                    "process_crash_atomicity": "tested",
                    "real_adapters": False,
                },
                sort_keys=True,
            )
        )
        return 0
    if arguments.command == "ci-durations":
        # Read-only GitHub metadata read; it never opens a state database.
        return ci_durations.main(arguments)
    try:
        database_path = _database_path(arguments)
    except (PathCapabilityUnavailable, OSError) as error:
        if arguments.command == "status":
            print(json.dumps(
                {
                    "initialized": False,
                    "database": None,
                    "path_capability": "UNAVAILABLE",
                    "verified": False,
                    "reason": str(error),
                },
                sort_keys=True,
            ))
            return 0
        print(f"verification failed: {error}", file=sys.stderr)
        return 3
    if arguments.command == "status":
        print(json.dumps(
            _status(
                database_path,
                trusted_root=database_path.parents[3],
                os_known_root=sys.platform == "win32",
            ),
            sort_keys=True,
        ))
        return 0
    if not database_path.is_file():
        print("state database does not exist", file=sys.stderr)
        return 2
    try:
        expected_repository_id, expected_catalog_head, expected_run_heads = (
            _load_expected_vector(arguments.expected_vector)
        )
        authority = _load_authority(arguments.authority_key_file)
        store = SQLiteStateStore.open_canonical(
            arguments.repository_id,
            ExpectedFreshnessOracle(
                expected_repository_id,
                expected_catalog_head,
                expected_run_heads,
            ),
        )
        catalog_head, run_heads = store.load_verified(
            arguments.repository_id, authority=authority
        )
    except (
        DispatchDenied, StorageIntegrityError, ValueError, sqlite3.Error, OSError,
    ) as error:
        print(f"verification failed: {error}", file=sys.stderr)
        return 3
    print(
        json.dumps(
            {"catalog_head": catalog_head, "run_heads": run_heads, "verified": True},
            sort_keys=True,
        )
    )
    return 0
