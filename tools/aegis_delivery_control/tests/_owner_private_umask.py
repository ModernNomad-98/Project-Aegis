"""Owner-private umask for delivery-control test fixtures.

Production refuses any owned database, writer lock, sidecar or managed
parent that is group- or world-accessible (``owned_paths.py``). Fixtures that
build those files with plain ``write_bytes``, ``sqlite3.connect`` or
``mkdir`` inherit the process umask. Under the common POSIX umask ``022``
they come out ``0644``/``0755`` and are refused as "not owner-private"
before the check a test actually targets (identity change, single link,
schema drift, freshness) ever runs.

Test modules that build such fixtures call :func:`enter` from
``setUpModule`` and :func:`restore` from ``tearDownModule``. This changes
only the test process's fixture defaults; production still passes explicit
``0o600``/``0o700`` modes, which
``test_platform.test_production_creates_owner_private_state_under_permissive_umask``
proves under a permissive umask. Windows has no POSIX mode bits here, so the
helpers are no-ops there.
"""

from __future__ import annotations

import os

OWNER_PRIVATE_UMASK = 0o077

_saved: list[int] = []


def enter() -> None:
    if os.name == "posix":
        _saved.append(os.umask(OWNER_PRIVATE_UMASK))


def restore() -> None:
    if _saved:
        os.umask(_saved.pop())
