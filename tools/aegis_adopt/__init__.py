"""Aegis Adopt v1: make a repository's coding sessions aware of a local Aegis checkout.

The package is standard library only. It reads and writes the target repository
named on the command line, plus the Aegis checkout it is told to record. It
makes no network call and reads no credentials.

`adopt` writes the bootstrap files once and is idempotent: a second run
replaces only the marked blocks and rewrites the same bytes. `doctor` writes
nothing and exits 0 for PASS or 1 for FAIL. `unadopt` removes only the recorded
blocks and known `.aegis` files, restoring the original marker-file bytes. None
of the commands copies Aegis skills, installs a host, or proves that a host
reads startup files.
"""

from __future__ import annotations

__version__ = "1.0.0"
TOOL_NAME = "aegis_adopt"
PROJECT_SCHEMA = "aegis.adopt/1"
BLOCK_VERSION = "v1"

__all__ = [
    "BLOCK_VERSION",
    "PROJECT_SCHEMA",
    "TOOL_NAME",
    "__version__",
]
