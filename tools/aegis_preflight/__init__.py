"""Aegis C2 preflight (auditable tooling, not enforcement).

Package marker and version constants for the aegis.preflight/v1 bundle.  The
package is standard-library only and read-only: it composes the merged C1.1a
verdict checker (PF-07) and the C2.3 evidence-reuse validator (PF-08), and adds
deterministic completeness, reference, status, arithmetic, staleness and
truthfulness checks.  It is not a required context and changes no settings.

An exit 0 means "mechanical checks passed", never approval, readiness or merge
permission.
"""

from __future__ import annotations

__version__ = "1.0.0"
TOOL_NAME = "aegis-preflight"
SCHEMA_VERSION = "aegis.preflight/v1"
ASSURANCE_CLAIM = "AUDITABLE"
MOUNTED_COVERAGE = "UNKNOWN"

__all__ = [
    "ASSURANCE_CLAIM",
    "MOUNTED_COVERAGE",
    "SCHEMA_VERSION",
    "TOOL_NAME",
    "__version__",
]
