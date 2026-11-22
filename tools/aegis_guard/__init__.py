"""Aegis Guard v1: fail-closed policy checks for coding-agent tool calls.

The package is standard library only. It reads a JSON policy and a repository
path, evaluates one proposed tool call or the repository's session files, and
prints a JSON decision. It never executes the proposed command, never starts a
shell, never opens a network connection and never writes to the repository.

Exit contract: 0 allow, 10 deny, 2 usage or argument error, 3 policy or
internal error. A decision is not an operating-system sandbox and is not an
enforcement claim. It is useful only when a host adapter calls this tool before
acting and maps 10, 3 and every other non-zero result to block.
"""

from __future__ import annotations

__version__ = "1.0.0"
TOOL_NAME = "aegis_guard"
POLICY_SCHEMA = "aegis.policy/1"
ADOPT_SCHEMA = "aegis.adopt/1"

__all__ = [
    "ADOPT_SCHEMA",
    "POLICY_SCHEMA",
    "TOOL_NAME",
    "__version__",
]
