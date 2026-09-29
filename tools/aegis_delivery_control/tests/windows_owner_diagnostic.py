"""Print the Windows ownership facts that delivery-control fixtures depend on.

Run from the repository root::

    python -B -m tools.aegis_delivery_control.tests.windows_owner_diagnostic

It prints the process token's user SID, the default owner given to new
objects, whether the token is elevated, and the owner of ``RUNNER_TEMP``,
``TEMP`` and a fresh ``tempfile`` directory, before and after the
owner-private fixture defaults are applied. On a standard user the user and
default owner match. On an elevated token with User Account Control off (as
on GitHub's hosted Windows runners) the default owner is expected to be
``S-1-5-32-544`` (BUILTIN\\Administrators) until the fixture defaults apply.

The script only reads security information and creates then removes one
temporary directory per phase. It is not a test module and exits 0 on
non-Windows hosts.
"""

from __future__ import annotations

import os
import sys
import tempfile

from tools.aegis_delivery_control.tests import _owner_private_fixtures as fixtures


def _owner_or_error(path: str | None) -> str:
    if not path:
        return "(unset)"
    try:
        return fixtures.path_owner_sid(path)
    except OSError as error:
        return f"(unavailable: {error})"


def _fresh_directory_owner() -> str:
    directory = tempfile.mkdtemp(prefix="aegis-owner-diagnostic-")
    try:
        return fixtures.path_owner_sid(directory)
    finally:
        os.rmdir(directory)


def _report(phase: str) -> None:
    print(f"[{phase}]")
    print(f"  token user SID         : {fixtures.token_user_sid()}")
    print(f"  token default owner SID: {fixtures.token_default_owner_sid()}")
    print(f"  fresh tempfile dir     : {_fresh_directory_owner()}")


def main() -> int:
    if os.name != "nt":
        print("windows_owner_diagnostic: not Windows; nothing to report")
        return 0
    print(f"python                   : {sys.version.split()[0]}")
    print(f"token elevated           : {fixtures.token_is_elevated()}")
    runner_temp = os.environ.get("RUNNER_TEMP")
    print(f"RUNNER_TEMP              : {runner_temp or '(unset)'}")
    print(f"RUNNER_TEMP owner SID    : {_owner_or_error(runner_temp)}")
    print(f"tempfile.gettempdir()    : {tempfile.gettempdir()}")
    print(f"gettempdir() owner SID   : {_owner_or_error(tempfile.gettempdir())}")
    _report("process defaults")
    fixtures.enter()
    try:
        _report("owner-private fixture defaults")
    finally:
        fixtures.restore()
    _report("restored")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
