"""Aegis C1.1a verdict/readiness checker (auditable tooling, not enforcement).

Package marker and version constants bound to aegis.verdict-bound/v2.1.

This package is a read-only, standard-library-only checker for supplied
authoritative records.  It is auditable gate tooling: it does not enforce,
does not register a required context, does not change settings, and never
claims a merge permission.  See README.md for the assurance statement, the
exit codes and the exact inputs.

Design consumed by reference: aegis.verdict-bound/v2.1 (C03-M1 delta plus the
v2.1 errata).  No second field list is defined here.
"""

from __future__ import annotations

from . import catalogue
from .catalogue import BOUND_SET_ID, BOUND_SET_VERSION, CANONICALIZATION_VERSION

__version__ = "1.0.0"
TOOL_NAME = "aegis-verdict-gate"

__all__ = [
    "BOUND_SET_ID",
    "BOUND_SET_VERSION",
    "CANONICALIZATION_VERSION",
    "TOOL_NAME",
    "__version__",
    "catalogue",
]
