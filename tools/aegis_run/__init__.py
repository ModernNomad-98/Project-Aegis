"""Aegis Run Record v1: a portable, verifiable record of one Aegis app run.

The package is standard library only. It writes inside the run directory the
caller names, plus one named file outside it when the caller runs install-hook:
<repo>/.git/hooks/post-commit. It makes no network call and reads no
credentials.
An exit 0 from verify means the record structure and copied artifact hashes
are internally consistent at verification time. It is not certification,
approval, delivery or readiness, and it does not extend beyond the single run
and commit the record names.
"""

from __future__ import annotations

__version__ = "1.1.0"
TOOL_NAME = "aegis_run"
RECORD_SCHEMA = "aegis.run-record/1"
MANIFEST_SCHEMA = "aegis.run-manifest/1"

__all__ = [
    "MANIFEST_SCHEMA",
    "RECORD_SCHEMA",
    "TOOL_NAME",
    "__version__",
]
