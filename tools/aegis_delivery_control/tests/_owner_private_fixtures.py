"""Owner-private defaults for delivery-control test fixtures.

Production refuses any trusted root, managed parent, owned database, writer
lock or sidecar that another principal could control (``owned_paths.py``).
Test fixtures build those paths with plain ``tempfile``, ``mkdir``,
``write_bytes`` or ``sqlite3.connect``, so they inherit the test process's
creation defaults. When those defaults are not owner-private, production
refuses the fixture before the check a test actually targets (identity
change, single link, unexpected principal, schema drift, freshness) runs.

Test modules call :func:`enter` from ``setUpModule`` and :func:`restore` from
``tearDownModule``. Each call changes only this test process's defaults:

* POSIX: the umask becomes ``077``. Under the common umask ``022`` fixtures
  would come out ``0644``/``0755`` and be refused as "not owner-private".
* Windows: the process token's default owner (``TokenOwner``) becomes the
  token user (``TokenUser``). GitHub's hosted Windows runners run elevated
  with User Account Control off, so the default owner there is
  ``BUILTIN\\Administrators``. Every fixture directory or file created with a
  default security descriptor would then be owned by Administrators and
  refused as "managed path is not owned by this principal". Setting the
  default owner to the token's own user needs no privilege and changes no
  system setting. It matches a standard (non-elevated) user, where the two
  SIDs are already equal and this call changes nothing.

Production is unaffected: it passes explicit ``0o600``/``0o700`` modes on
POSIX and an explicit ``O:<user>`` security descriptor on Windows, and it
still refuses any path whose owner is not the current user.
``test_platform.test_production_creates_owner_private_state_under_permissive_umask``
proves the POSIX half under a permissive umask.

:func:`enter` checks its own result on Windows: a fresh ``tempfile``
directory must be owned by the token user, or it raises with the SIDs it saw.
"""

from __future__ import annotations

import contextlib
import os
import tempfile
from typing import Iterator

OWNER_PRIVATE_UMASK = 0o077

_saved_umasks: list[int] = []
_saved_owners: list[object] = []


if os.name == "nt":
    import ctypes
    from ctypes import wintypes

    _kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    _advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)

    _TOKEN_QUERY = 0x0008
    _TOKEN_ADJUST_DEFAULT = 0x0080
    _TOKEN_USER = 1
    _TOKEN_OWNER = 4
    _TOKEN_ELEVATION = 20
    _SE_FILE_OBJECT = 1
    _OWNER_SECURITY_INFORMATION = 0x00000001

    _kernel32.GetCurrentProcess.restype = wintypes.HANDLE
    _kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    _kernel32.CloseHandle.restype = wintypes.BOOL
    _kernel32.LocalFree.argtypes = [ctypes.c_void_p]
    _kernel32.LocalFree.restype = ctypes.c_void_p
    _advapi32.OpenProcessToken.argtypes = [
        wintypes.HANDLE, wintypes.DWORD, ctypes.POINTER(wintypes.HANDLE)
    ]
    _advapi32.OpenProcessToken.restype = wintypes.BOOL
    _advapi32.GetTokenInformation.argtypes = [
        wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
    ]
    _advapi32.GetTokenInformation.restype = wintypes.BOOL
    _advapi32.SetTokenInformation.argtypes = [
        wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD,
    ]
    _advapi32.SetTokenInformation.restype = wintypes.BOOL
    _advapi32.ConvertSidToStringSidW.argtypes = [
        ctypes.c_void_p, ctypes.POINTER(ctypes.c_wchar_p)
    ]
    _advapi32.ConvertSidToStringSidW.restype = wintypes.BOOL
    _advapi32.GetNamedSecurityInfoW.argtypes = [
        wintypes.LPCWSTR, ctypes.c_int, wintypes.DWORD,
        ctypes.POINTER(ctypes.c_void_p), ctypes.c_void_p, ctypes.c_void_p,
        ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p),
    ]
    _advapi32.GetNamedSecurityInfoW.restype = wintypes.DWORD

    def _open_token(access: int) -> wintypes.HANDLE:
        token = wintypes.HANDLE()
        if not _advapi32.OpenProcessToken(
            _kernel32.GetCurrentProcess(), access, ctypes.byref(token)
        ):
            raise OSError(ctypes.get_last_error(), "OpenProcessToken failed")
        return token

    def _token_information(token: wintypes.HANDLE, info_class: int) -> ctypes.Array:
        needed = wintypes.DWORD()
        _advapi32.GetTokenInformation(token, info_class, None, 0, ctypes.byref(needed))
        buffer = ctypes.create_string_buffer(needed.value)
        if not _advapi32.GetTokenInformation(
            token, info_class, buffer, needed, ctypes.byref(needed)
        ):
            raise OSError(ctypes.get_last_error(), "GetTokenInformation failed")
        return buffer

    def _sid_text(sid_pointer: int | ctypes.c_void_p) -> str:
        text = ctypes.c_wchar_p()
        if not _advapi32.ConvertSidToStringSidW(sid_pointer, ctypes.byref(text)):
            raise OSError(ctypes.get_last_error(), "ConvertSidToStringSidW failed")
        try:
            return str(text.value)
        finally:
            _kernel32.LocalFree(text)

    def _first_pointer(buffer: ctypes.Array) -> int:
        return ctypes.cast(buffer, ctypes.POINTER(ctypes.c_void_p))[0]

    def token_user_sid() -> str:
        """Return the process token's user SID (``TokenUser``)."""
        token = _open_token(_TOKEN_QUERY)
        try:
            return _sid_text(_first_pointer(_token_information(token, _TOKEN_USER)))
        finally:
            _kernel32.CloseHandle(token)

    def token_default_owner_sid() -> str:
        """Return the owner given to new objects created with no explicit owner."""
        token = _open_token(_TOKEN_QUERY)
        try:
            return _sid_text(_first_pointer(_token_information(token, _TOKEN_OWNER)))
        finally:
            _kernel32.CloseHandle(token)

    def token_is_elevated() -> bool:
        token = _open_token(_TOKEN_QUERY)
        try:
            buffer = _token_information(token, _TOKEN_ELEVATION)
            return bool(ctypes.cast(buffer, ctypes.POINTER(wintypes.DWORD))[0])
        finally:
            _kernel32.CloseHandle(token)

    def path_owner_sid(path: str | os.PathLike[str]) -> str:
        """Return the owner SID recorded on an existing file or directory."""
        owner = ctypes.c_void_p()
        descriptor = ctypes.c_void_p()
        result = _advapi32.GetNamedSecurityInfoW(
            os.fspath(path), _SE_FILE_OBJECT, _OWNER_SECURITY_INFORMATION,
            ctypes.byref(owner), None, None, None, ctypes.byref(descriptor),
        )
        if result != 0:
            raise OSError(result, "GetNamedSecurityInfoW failed")
        try:
            return _sid_text(owner)
        finally:
            _kernel32.LocalFree(descriptor)

    def _set_default_owner(token_owner: ctypes.Array) -> None:
        token = _open_token(_TOKEN_QUERY | _TOKEN_ADJUST_DEFAULT)
        try:
            if not _advapi32.SetTokenInformation(
                token, _TOKEN_OWNER, token_owner, ctypes.sizeof(token_owner)
            ):
                raise OSError(
                    ctypes.get_last_error(), "SetTokenInformation(TokenOwner) failed"
                )
        finally:
            _kernel32.CloseHandle(token)

    def _enter_windows() -> None:
        token = _open_token(_TOKEN_QUERY)
        try:
            saved_owner = _token_information(token, _TOKEN_OWNER)
            user = _token_information(token, _TOKEN_USER)
        finally:
            _kernel32.CloseHandle(token)
        # TOKEN_USER starts with the user SID pointer, so its first pointer is
        # a valid TOKEN_OWNER naming the same SID. ``user`` stays alive for the
        # call; the kernel copies the SID into the token.
        owner_record = (ctypes.c_void_p * 1)(_first_pointer(user))
        _set_default_owner(owner_record)  # type: ignore[arg-type]
        _saved_owners.append(saved_owner)
        try:
            _verify_fresh_temporary_directory_owner()
        except BaseException:
            # A failing setUpModule never reaches tearDownModule, so undo the
            # token change here rather than leave it for later modules.
            _set_default_owner(_saved_owners.pop())  # type: ignore[arg-type]
            raise

    @contextlib.contextmanager
    def original_default_owner() -> Iterator[None]:
        """Temporarily put back the default owner saved by the first :func:`enter`.

        Guard tests use this to create production state under the process's
        real default owner (``BUILTIN\\Administrators`` on an elevated runner),
        so they prove production sets its own owner explicitly instead of
        inheriting the fixture default.
        """
        if not _saved_owners:
            raise RuntimeError("original_default_owner() needs an active enter()")
        token = _open_token(_TOKEN_QUERY)
        try:
            current = _token_information(token, _TOKEN_OWNER)
        finally:
            _kernel32.CloseHandle(token)
        _set_default_owner(_saved_owners[0])  # type: ignore[arg-type]
        try:
            yield
        finally:
            _set_default_owner(current)  # type: ignore[arg-type]

    def _restore_windows() -> None:
        if _saved_owners:
            _set_default_owner(_saved_owners.pop())  # type: ignore[arg-type]

    def _verify_fresh_temporary_directory_owner() -> None:
        expected = token_user_sid()
        directory = tempfile.mkdtemp(prefix="aegis-owner-check-")
        try:
            actual = path_owner_sid(directory)
        finally:
            os.rmdir(directory)
        if actual != expected:
            raise RuntimeError(
                "owner-private fixture defaults did not take effect: a fresh "
                f"temporary directory is owned by {actual}, expected the token "
                f"user {expected} (default owner {token_default_owner_sid()}, "
                f"elevated={token_is_elevated()})"
            )


def enter() -> None:
    """Make fixture paths this process creates owner-private by default."""
    if os.name == "posix":
        _saved_umasks.append(os.umask(OWNER_PRIVATE_UMASK))
    elif os.name == "nt":
        _enter_windows()


def restore() -> None:
    """Undo the most recent :func:`enter`."""
    if os.name == "posix":
        if _saved_umasks:
            os.umask(_saved_umasks.pop())
    elif os.name == "nt":
        _restore_windows()
