"""Fail-closed containment interfaces and the mock/synthetic boundary
(design §15; prompt Phase 13).

The REAL Claude Code host containment capability remains UNAVAILABLE/UNKNOWN
in WP-2B-1 (R4 is INCOMPLETE/BLOCKED): no code here claims the real host is
contained, and the real-host implementation denies every operation. The mock
boundary exists ONLY for deterministic offline tests of the runner's own
control logic.
"""

from __future__ import annotations

import os
import stat
from dataclasses import dataclass, field
from typing import Any

from .enums import CapabilityState
from .errors import ContainmentUnavailableError, ContainmentViolationError, ReparsePointError


@dataclass(frozen=True, slots=True)
class EgressPolicy:
    """Deny-by-default network egress representation."""

    deny_all: bool = True
    loopback_fixture_allowlist: tuple[str, ...] = ()

    def is_allowed(self, target: str) -> bool:
        if self.deny_all:
            return False
        return target in self.loopback_fixture_allowlist


@dataclass(frozen=True, slots=True)
class CommandPolicy:
    """Allowlist-only command policy representation."""

    allowed_commands: tuple[str, ...] = ()

    def is_allowed(self, command: str) -> bool:
        return command in self.allowed_commands


class ContainmentBoundary:
    """Abstract fail-closed containment boundary."""

    def capability_report(self) -> dict[str, str]:  # pragma: no cover - interface
        raise NotImplementedError

    def validate_read(self, path: str) -> str:  # pragma: no cover - interface
        raise NotImplementedError

    def validate_write(self, path: str) -> str:  # pragma: no cover - interface
        raise NotImplementedError

    def check_egress(self, target: str) -> None:  # pragma: no cover - interface
        raise NotImplementedError

    def check_command(self, command: str) -> None:  # pragma: no cover - interface
        raise NotImplementedError


class RealHostContainment(ContainmentBoundary):
    """The real-host boundary in WP-2B-1: honestly UNAVAILABLE, fail closed.

    Per the WP-2B-0 Outcome B evidence state (R4 INCOMPLETE/BLOCKED) no
    OS/host-enforced boundary is proven. Every operation is therefore denied;
    nothing may proceed on an unproven boundary.
    """

    def capability_report(self) -> dict[str, str]:
        return {
            "os_host_isolation_boundary": CapabilityState.UNAVAILABLE.value,
            "per_tool_path_confinement": CapabilityState.UNKNOWN.value,
            "control_plane_inaccessibility": CapabilityState.UNKNOWN.value,
            "egress_enforcement": CapabilityState.UNKNOWN.value,
            "process_tree_kill_on_host": CapabilityState.UNKNOWN.value,
            "note": (
                "WP-2B-1 makes no real-host containment claim; R4 remains "
                "INCOMPLETE/BLOCKED (WP-2B-0 Outcome B)"
            ),
        }

    def _deny(self, operation: str) -> None:
        raise ContainmentUnavailableError(
            f"real-host containment is UNAVAILABLE/UNKNOWN in WP-2B-1; "
            f"{operation} is denied fail-closed"
        )

    def validate_read(self, path: str) -> str:
        self._deny(f"read of {path!r}")
        raise AssertionError("unreachable")  # pragma: no cover

    def validate_write(self, path: str) -> str:
        self._deny(f"write of {path!r}")
        raise AssertionError("unreachable")  # pragma: no cover

    def check_egress(self, target: str) -> None:
        self._deny(f"egress to {target!r}")

    def check_command(self, command: str) -> None:
        self._deny(f"command {command!r}")


def _refuse_reparse_chain(path: str, boundary_root: str) -> None:
    """Refuse reparse points between the boundary root and the target path."""
    probe = os.path.abspath(path)
    root = os.path.abspath(boundary_root)
    chain: list[str] = []
    while True:
        chain.append(probe)
        if os.path.normcase(probe) == os.path.normcase(root):
            break
        parent = os.path.dirname(probe)
        if parent == probe:
            break
        probe = parent
    for component in chain:
        if not os.path.exists(component):
            continue
        info = os.lstat(component)
        if stat.S_ISLNK(info.st_mode):
            raise ReparsePointError(f"symlink refused in containment path: {component}")
        windows_attrs = getattr(info, "st_file_attributes", 0)
        reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
        if windows_attrs & reparse_flag:
            raise ReparsePointError(
                f"reparse point refused in containment path: {component}"
            )


@dataclass(slots=True)
class MockContainment(ContainmentBoundary):
    """Deterministic mock/synthetic boundary used ONLY by offline tests.

    Logical rules it enforces (runner-side defense in depth — explicitly NOT a
    claim about any real host):

    - the read-only logical corpus boundary (reads allowed, writes refused);
    - the workspace-only logical write boundary;
    - caller-directory refusal (no read, no write);
    - control-plane roots inaccessible in both directions;
    - reparse-point refusal along validated chains;
    - deny-by-default egress; allowlist-only commands.
    """

    corpus_roots: tuple[str, ...]
    workspace_root: str
    control_plane_roots: tuple[str, ...] = ()
    caller_roots: tuple[str, ...] = ()
    egress_policy: EgressPolicy = field(default_factory=EgressPolicy)
    command_policy: CommandPolicy = field(default_factory=CommandPolicy)

    def capability_report(self) -> dict[str, str]:
        return {
            "boundary_kind": "mock_synthetic_offline_test_boundary",
            "os_host_isolation_boundary": CapabilityState.UNAVAILABLE.value,
            "logical_path_rules": CapabilityState.AVAILABLE.value,
            "egress_policy": "deny_by_default"
            if self.egress_policy.deny_all
            else "loopback_fixture_allowlist",
            "note": (
                "mock boundary for offline tests only; proves runner control "
                "logic, never real-host confinement"
            ),
        }

    def _contains(self, roots: tuple[str, ...], path: str) -> str | None:
        target = os.path.abspath(path)
        for root in roots:
            root_abs = os.path.abspath(root)
            try:
                if os.path.commonpath([root_abs, target]) == root_abs:
                    return root_abs
            except ValueError:  # different drives on Windows
                continue
        return None

    def validate_read(self, path: str) -> str:
        target = os.path.abspath(path)
        caller_root = self._contains(self.caller_roots, target)
        if caller_root is not None:
            raise ContainmentViolationError(
                f"caller-owned directory is inaccessible: {path!r}"
            )
        control_root = self._contains(self.control_plane_roots, target)
        if control_root is not None:
            raise ContainmentViolationError(
                f"control-plane corpus is inaccessible to the agent surface: {path!r}"
            )
        workspace_root = self._contains((self.workspace_root,), target)
        corpus_root = self._contains(self.corpus_roots, target)
        anchor = workspace_root or corpus_root
        if anchor is None:
            raise ContainmentViolationError(
                f"read outside every containment root refused: {path!r}"
            )
        _refuse_reparse_chain(target, anchor)
        return target

    def validate_write(self, path: str) -> str:
        target = os.path.abspath(path)
        if self._contains(self.caller_roots, target) is not None:
            raise ContainmentViolationError(
                f"caller-owned directory is never writable: {path!r}"
            )
        if self._contains(self.control_plane_roots, target) is not None:
            raise ContainmentViolationError(
                f"control-plane corpus is never writable: {path!r}"
            )
        if self._contains(self.corpus_roots, target) is not None:
            raise ContainmentViolationError(
                f"the corpus surface is read-only: {path!r}"
            )
        workspace_root = self._contains((self.workspace_root,), target)
        if workspace_root is None:
            raise ContainmentViolationError(
                f"write outside the owned workspace refused: {path!r}"
            )
        _refuse_reparse_chain(target, workspace_root)
        return target

    def check_egress(self, target: str) -> None:
        if not self.egress_policy.is_allowed(target):
            raise ContainmentViolationError(
                f"network egress denied (deny-by-default): {target!r}"
            )

    def check_command(self, command: str) -> None:
        if not self.command_policy.is_allowed(command):
            raise ContainmentViolationError(
                f"command outside the allowlist refused: {command!r}"
            )

    def to_capability_dict(self) -> dict[str, Any]:  # pragma: no cover - convenience
        return dict(self.capability_report())
