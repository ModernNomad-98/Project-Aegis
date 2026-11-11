"""Aegis C2 evidence-reuse validator (auditable tooling, not enforcement).

Package marker and version constants for the closed aegis.evidence-reuse/1
record.  The package is standard-library only and read-only: it validates a
supplied reuse record against the closed schema and RU-01..RU-12 and writes
nothing.  A VALID result is a record decision, never an approval, a CI waiver
or a merge permission.
"""

from __future__ import annotations

__version__ = "1.0.0"
TOOL_NAME = "aegis-evidence-reuse"
SCHEMA_VERSION = "aegis.evidence-reuse/1"
ASSURANCE_CLAIM = "AUDITABLE"
MOUNTED_COVERAGE = "UNKNOWN"

__all__ = [
    "ASSURANCE_CLAIM",
    "MOUNTED_COVERAGE",
    "SCHEMA_VERSION",
    "TOOL_NAME",
    "__version__",
]
