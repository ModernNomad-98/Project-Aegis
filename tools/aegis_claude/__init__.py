"""Aegis Claude adapter v1: repository-local Claude Code hooks for Aegis Guard.

The package is standard library only. It writes a policy file when asked to,
merges two hook entries into a repository's `.claude/settings.json`, and backs
up that file before changing it. The hook entry point reads one JSON event from
standard input and either checks the Aegis session files or asks Aegis Guard
about one proposed tool call.

This is a local, L2 policy adapter. It is not an operating-system sandbox, not
process containment, and not an enforcement claim. The hooks constrain a host
only when that host executes them and blocks on their exit code.
"""

from __future__ import annotations

__version__ = "1.0.0"
TOOL_NAME = "aegis_claude"
POLICY_SCHEMA = "aegis.policy/1"
HOOK_EVENTS = ("SessionStart", "PreToolUse")
HOOK_MODULE = "tools.aegis_claude.hook"
SETTINGS_REL = ".claude/settings.json"
BACKUP_DIR_REL = ".aegis/backup"

__all__ = [
    "BACKUP_DIR_REL",
    "HOOK_EVENTS",
    "HOOK_MODULE",
    "POLICY_SCHEMA",
    "SETTINGS_REL",
    "TOOL_NAME",
    "__version__",
]
