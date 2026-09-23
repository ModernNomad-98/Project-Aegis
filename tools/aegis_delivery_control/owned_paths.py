"""Checked, owner-controlled filesystem paths for the offline kernel.

The capability is deliberately local and standard-library only.  It protects
against path redirection by a different OS principal; a compromised process
running as the owning principal remains inside the documented state-trust
boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
import ctypes
from ctypes import wintypes
import errno
import os
from pathlib import Path, PureWindowsPath
import re
import sqlite3
import stat
import sys
from typing import Iterable

from .contracts import StorageIntegrityError


_REPARSE_FLAG = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
_WINDOWS_DEVICES = frozenset(
    {"con", "prn", "aux", "nul", *(f"com{i}" for i in range(1, 10)),
     *(f"lpt{i}" for i in range(1, 10))}
)


class PathCapabilityUnavailable(StorageIntegrityError):
    """The host cannot prove the required owned-path guarantee."""


@dataclass(frozen=True)
class PathIdentity:
    platform: str
    components: tuple[tuple[int, int], ...]
    leaf: tuple[int, int]
    canonical_path: str


def _validate_absolute_path(path: Path) -> Path:
    raw = os.fspath(path)
    if not isinstance(raw, str) or not raw or "\x00" in raw:
        raise PathCapabilityUnavailable("owned path is invalid")
    if sys.platform == "win32":
        pure = PureWindowsPath(raw)
        if not pure.is_absolute() or raw.startswith(("\\\\", "//")):
            raise PathCapabilityUnavailable("owned path must use a local absolute drive")
        parts = pure.parts
        segments = parts[1:]
    else:
        if not raw.startswith("/"):
            raise PathCapabilityUnavailable("owned path must be absolute")
        parts = Path(raw).parts
        segments = parts[1:]
    for segment in segments:
        if segment in {"", ".", ".."} or segment != segment.rstrip(" ."):
            raise PathCapabilityUnavailable("owned path contains an unsafe segment")
        if ":" in segment:
            raise PathCapabilityUnavailable("owned path contains an alternate stream")
        if segment.split(".", 1)[0].casefold() in _WINDOWS_DEVICES:
            raise PathCapabilityUnavailable("owned path contains a device name")
    result = Path(raw)
    if sys.platform == "win32":
        probe = Path(result.anchor)
        for part in result.parts[1:-1]:
            probe = probe / part
            if probe.exists() or probe.is_symlink():
                info = os.lstat(probe)
                if (
                    stat.S_ISLNK(info.st_mode)
                    or getattr(info, "st_file_attributes", 0) & _REPARSE_FLAG
                ):
                    raise PathCapabilityUnavailable(
                        "reparse point refused in owned path"
                    )
    return result


def _relative_parts(path: Path, root: Path) -> tuple[str, ...]:
    if sys.platform == "win32":
        path_parts = tuple(part.casefold() for part in path.parts)
        root_parts = tuple(part.casefold() for part in root.parts)
        if path_parts[:len(root_parts)] != root_parts:
            raise PathCapabilityUnavailable(
                "owned path escapes its trusted root"
            )
        return tuple(path.parts[len(root.parts):])
    try:
        return path.relative_to(root).parts
    except ValueError as error:
        raise PathCapabilityUnavailable(
            "owned path escapes its trusted root"
        ) from error


def nearest_existing_trusted_root(path: Path) -> Path:
    """Select the closest existing ancestor for noncanonical checked paths."""
    current = _validate_absolute_path(path)
    while not current.exists() and not current.is_symlink():
        parent = current.parent
        if parent == current:
            raise PathCapabilityUnavailable(
                "owned path has no existing trusted root"
            )
        current = parent
    return current


def known_local_state_base() -> Path:
    """Use the OS-known Windows folder; POSIX honors XDG_STATE_HOME."""
    if sys.platform != "win32":
        selected = os.environ.get("XDG_STATE_HOME")
        if selected:
            return _validate_absolute_path(Path(selected))
        return _validate_absolute_path(Path.home() / ".local" / "state")
    shell32 = ctypes.WinDLL("shell32", use_last_error=True)
    ole32 = ctypes.WinDLL("ole32", use_last_error=True)

    class GUID(ctypes.Structure):
        _fields_ = [
            ("Data1", wintypes.DWORD), ("Data2", wintypes.WORD),
            ("Data3", wintypes.WORD), ("Data4", ctypes.c_ubyte * 8),
        ]

    folder = GUID(
        0xF1B32785, 0x6FBA, 0x4FCF,
        (ctypes.c_ubyte * 8)(0x9D, 0x55, 0x7B, 0x8E, 0x7F, 0x15, 0x70, 0x91),
    )
    value = ctypes.c_wchar_p()
    shell32.SHGetKnownFolderPath.argtypes = [
        ctypes.POINTER(GUID), wintypes.DWORD, wintypes.HANDLE,
        ctypes.POINTER(ctypes.c_wchar_p),
    ]
    result = shell32.SHGetKnownFolderPath(
        ctypes.byref(folder), 0, None, ctypes.byref(value)
    )
    if result != 0 or not value.value:
        raise PathCapabilityUnavailable("Windows local-state known folder is unavailable")
    try:
        selected = _validate_absolute_path(Path(value.value))
        if _kernel32.GetDriveTypeW(selected.anchor) != 3:
            raise PathCapabilityUnavailable(
                "Windows local-state known folder is not on a fixed drive"
            )
        return selected
    finally:
        ole32.CoTaskMemFree(value)


if sys.platform == "win32":
    _kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    _advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)
    _INVALID_HANDLE = wintypes.HANDLE(-1).value
    _FILE_SHARE_READ = 1
    _FILE_SHARE_WRITE = 2
    _FILE_SHARE_DELETE = 4
    _OPEN_EXISTING = 3
    _OPEN_ALWAYS = 4
    _CREATE_NEW = 1
    _FILE_FLAG_BACKUP_SEMANTICS = 0x02000000
    _FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000

    class _BY_HANDLE_FILE_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("dwFileAttributes", wintypes.DWORD),
            ("ftCreationTime", wintypes.FILETIME),
            ("ftLastAccessTime", wintypes.FILETIME),
            ("ftLastWriteTime", wintypes.FILETIME),
            ("dwVolumeSerialNumber", wintypes.DWORD),
            ("nFileSizeHigh", wintypes.DWORD), ("nFileSizeLow", wintypes.DWORD),
            ("nNumberOfLinks", wintypes.DWORD),
            ("nFileIndexHigh", wintypes.DWORD), ("nFileIndexLow", wintypes.DWORD),
        ]

    class _SECURITY_ATTRIBUTES(ctypes.Structure):
        _fields_ = [
            ("nLength", wintypes.DWORD),
            ("lpSecurityDescriptor", ctypes.c_void_p),
            ("bInheritHandle", wintypes.BOOL),
        ]

    _kernel32.CreateFileW.restype = wintypes.HANDLE
    _kernel32.CreateFileW.argtypes = [
        wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.c_void_p,
        wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE,
    ]
    _kernel32.GetCurrentProcess.restype = wintypes.HANDLE
    _kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    _kernel32.CloseHandle.restype = wintypes.BOOL
    _kernel32.GetFileInformationByHandle.argtypes = [
        wintypes.HANDLE, ctypes.POINTER(_BY_HANDLE_FILE_INFORMATION)
    ]
    _kernel32.GetFileInformationByHandle.restype = wintypes.BOOL
    _kernel32.GetDriveTypeW.argtypes = [wintypes.LPCWSTR]
    _kernel32.GetDriveTypeW.restype = wintypes.UINT
    _kernel32.GetFinalPathNameByHandleW.argtypes = [
        wintypes.HANDLE, wintypes.LPWSTR, wintypes.DWORD, wintypes.DWORD,
    ]
    _kernel32.GetFinalPathNameByHandleW.restype = wintypes.DWORD
    _kernel32.GetShortPathNameW.argtypes = [
        wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD,
    ]
    _kernel32.GetShortPathNameW.restype = wintypes.DWORD
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
    _advapi32.ConvertSidToStringSidW.argtypes = [
        ctypes.c_void_p, ctypes.POINTER(ctypes.c_wchar_p)
    ]
    _advapi32.ConvertSidToStringSidW.restype = wintypes.BOOL
    _advapi32.GetNamedSecurityInfoW.argtypes = [
        wintypes.LPWSTR, ctypes.c_int, wintypes.DWORD,
        ctypes.POINTER(ctypes.c_void_p), ctypes.c_void_p, ctypes.c_void_p,
        ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p),
    ]
    _advapi32.GetNamedSecurityInfoW.restype = wintypes.DWORD
    _advapi32.GetSecurityInfo.argtypes = [
        wintypes.HANDLE, ctypes.c_int, wintypes.DWORD,
        ctypes.POINTER(ctypes.c_void_p), ctypes.c_void_p, ctypes.c_void_p,
        ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p),
    ]
    _advapi32.GetSecurityInfo.restype = wintypes.DWORD
    _advapi32.ConvertSecurityDescriptorToStringSecurityDescriptorW.argtypes = [
        ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD,
        ctypes.POINTER(ctypes.c_wchar_p), ctypes.POINTER(wintypes.DWORD),
    ]
    _advapi32.ConvertSecurityDescriptorToStringSecurityDescriptorW.restype = wintypes.BOOL
    _advapi32.ConvertStringSecurityDescriptorToSecurityDescriptorW.argtypes = [
        wintypes.LPCWSTR, wintypes.DWORD,
        ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(wintypes.DWORD),
    ]
    _advapi32.ConvertStringSecurityDescriptorToSecurityDescriptorW.restype = wintypes.BOOL
    _kernel32.CreateDirectoryW.argtypes = [
        wintypes.LPCWSTR, ctypes.POINTER(_SECURITY_ATTRIBUTES)
    ]
    _kernel32.CreateDirectoryW.restype = wintypes.BOOL


def _windows_handle(
    path: Path, *, directory: bool = False, protect_delete: bool = True,
    open_reparse: bool = True, desired_access: int = 0x00020000,
) -> int:
    flags = _FILE_FLAG_OPEN_REPARSE_POINT if open_reparse else 0
    if directory:
        flags |= _FILE_FLAG_BACKUP_SEMANTICS
    handle = _kernel32.CreateFileW(
        str(path), desired_access,
        _FILE_SHARE_READ | _FILE_SHARE_WRITE
        | (0 if protect_delete else _FILE_SHARE_DELETE),
        None, _OPEN_EXISTING, flags, None,
    )
    if handle == _INVALID_HANDLE:
        raise PathCapabilityUnavailable(
            f"checked Windows path handle is unavailable: {path} "
            f"(winerror={ctypes.get_last_error()})"
        )
    return int(handle)


def _windows_info(handle: int) -> tuple[tuple[int, int], int, int]:
    info = _BY_HANDLE_FILE_INFORMATION()
    if not _kernel32.GetFileInformationByHandle(handle, ctypes.byref(info)):
        raise PathCapabilityUnavailable("Windows path identity is unavailable")
    if info.dwFileAttributes & _REPARSE_FLAG:
        raise PathCapabilityUnavailable("reparse point refused in owned path")
    identity = (
        int(info.dwVolumeSerialNumber),
        (int(info.nFileIndexHigh) << 32) | int(info.nFileIndexLow),
    )
    return identity, int(info.nNumberOfLinks), int(info.dwFileAttributes)


def _windows_final_path(handle: int) -> str:
    size = _kernel32.GetFinalPathNameByHandleW(handle, None, 0, 0)
    if size == 0:
        raise PathCapabilityUnavailable("Windows final path is unavailable")
    buffer = ctypes.create_unicode_buffer(size + 1)
    written = _kernel32.GetFinalPathNameByHandleW(handle, buffer, len(buffer), 0)
    if written == 0 or written >= len(buffer):
        raise PathCapabilityUnavailable("Windows final path is unavailable")
    value = buffer.value
    if value.startswith("\\\\?\\UNC\\"):
        value = "\\\\" + value[8:]
    elif value.startswith("\\\\?\\"):
        value = value[4:]
    return value


def _windows_normalized_path(path: Path | str) -> str:
    """Normalize one existing local path, including supported 8.3 aliases."""
    value = str(path)
    size = _kernel32.GetShortPathNameW(value, None, 0)
    if size == 0:
        raise PathCapabilityUnavailable(
            "Windows path normalization is unavailable"
        )
    buffer = ctypes.create_unicode_buffer(size + 1)
    written = _kernel32.GetShortPathNameW(value, buffer, len(buffer))
    if written == 0 or written >= len(buffer):
        raise PathCapabilityUnavailable(
            "Windows path normalization is unavailable"
        )
    return os.path.normcase(os.path.normpath(buffer.value))


def _close_windows(handles: Iterable[int]) -> None:
    for handle in handles:
        _kernel32.CloseHandle(handle)


def _windows_current_sid() -> str:
    token = wintypes.HANDLE()
    if not _advapi32.OpenProcessToken(
        _kernel32.GetCurrentProcess(), 0x0008, ctypes.byref(token)
    ):
        raise PathCapabilityUnavailable("Windows process token is unavailable")
    try:
        needed = wintypes.DWORD()
        _advapi32.GetTokenInformation(token, 1, None, 0, ctypes.byref(needed))
        buffer = ctypes.create_string_buffer(needed.value)
        if not _advapi32.GetTokenInformation(
            token, 1, buffer, needed, ctypes.byref(needed)
        ):
            raise PathCapabilityUnavailable("Windows owner SID is unavailable")
        sid_pointer = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_void_p))[0]
        text = ctypes.c_wchar_p()
        if not _advapi32.ConvertSidToStringSidW(sid_pointer, ctypes.byref(text)):
            raise PathCapabilityUnavailable("Windows owner SID is unavailable")
        try:
            return str(text.value)
        finally:
            _kernel32.LocalFree(text)
    finally:
        _kernel32.CloseHandle(token)


def _windows_sddl(path: Path) -> tuple[str, str]:
    owner = ctypes.c_void_p()
    descriptor = ctypes.c_void_p()
    result = _advapi32.GetNamedSecurityInfoW(
        str(path), 1, 0x00000001 | 0x00000004,
        ctypes.byref(owner), None, None, None, ctypes.byref(descriptor),
    )
    if result != 0:
        raise PathCapabilityUnavailable("Windows path security is unavailable")
    try:
        owner_text = ctypes.c_wchar_p()
        if not _advapi32.ConvertSidToStringSidW(owner, ctypes.byref(owner_text)):
            raise PathCapabilityUnavailable("Windows path owner is unavailable")
        try:
            owner_sid = str(owner_text.value)
        finally:
            _kernel32.LocalFree(owner_text)
        sddl = ctypes.c_wchar_p()
        length = wintypes.DWORD()
        if not _advapi32.ConvertSecurityDescriptorToStringSecurityDescriptorW(
            descriptor, 1, 0x00000004, ctypes.byref(sddl), ctypes.byref(length)
        ):
            raise PathCapabilityUnavailable("Windows path DACL is unavailable")
        try:
            return owner_sid, str(sddl.value)
        finally:
            _kernel32.LocalFree(sddl)
    finally:
        _kernel32.LocalFree(descriptor)


def _windows_handle_sddl(handle: int) -> tuple[str, str]:
    owner = ctypes.c_void_p()
    descriptor = ctypes.c_void_p()
    result = _advapi32.GetSecurityInfo(
        handle, 1, 0x00000001 | 0x00000004,
        ctypes.byref(owner), None, None, None, ctypes.byref(descriptor),
    )
    if result != 0:
        raise PathCapabilityUnavailable("Windows handle security is unavailable")
    try:
        owner_text = ctypes.c_wchar_p()
        if not _advapi32.ConvertSidToStringSidW(owner, ctypes.byref(owner_text)):
            raise PathCapabilityUnavailable("Windows handle owner is unavailable")
        try:
            owner_sid = str(owner_text.value)
        finally:
            _kernel32.LocalFree(owner_text)
        sddl = ctypes.c_wchar_p()
        length = wintypes.DWORD()
        if not _advapi32.ConvertSecurityDescriptorToStringSecurityDescriptorW(
            descriptor, 1, 0x00000004, ctypes.byref(sddl), ctypes.byref(length)
        ):
            raise PathCapabilityUnavailable("Windows handle DACL is unavailable")
        try:
            return owner_sid, str(sddl.value)
        finally:
            _kernel32.LocalFree(sddl)
    finally:
        _kernel32.LocalFree(descriptor)


def _windows_security_attributes() -> tuple[_SECURITY_ATTRIBUTES, ctypes.c_void_p]:
    owner = _windows_current_sid()
    descriptor = ctypes.c_void_p()
    size = wintypes.DWORD()
    sddl = (
        f"O:{owner}G:{owner}D:P"
        f"(A;OICI;FA;;;{owner})(A;OICI;FA;;;SY)(A;OICI;FA;;;BA)"
    )
    if not _advapi32.ConvertStringSecurityDescriptorToSecurityDescriptorW(
        sddl, 1, ctypes.byref(descriptor), ctypes.byref(size)
    ):
        raise PathCapabilityUnavailable(
            "restrictive Windows security descriptor is unavailable"
        )
    attributes = _SECURITY_ATTRIBUTES(
        ctypes.sizeof(_SECURITY_ATTRIBUTES), descriptor, False
    )
    return attributes, descriptor


def _windows_create_directory(path: Path) -> None:
    attributes, descriptor = _windows_security_attributes()
    try:
        if not _kernel32.CreateDirectoryW(str(path), ctypes.byref(attributes)):
            error = ctypes.get_last_error()
            if error != 183:
                raise PathCapabilityUnavailable(
                    f"restrictive Windows directory creation failed ({error})"
                )
    finally:
        _kernel32.LocalFree(descriptor)
    _verify_windows_acl(path, managed=True)


def _windows_rights_are_read_only(rights: str) -> bool:
    if rights in {"FR", "GR", "GX", "GRGX"}:
        return True
    if not rights.lower().startswith("0x"):
        return False
    try:
        mask = int(rights, 16)
    except ValueError:
        return False
    write_or_delete = (
        0x00000002 | 0x00000004 | 0x00000010 | 0x00000040
        | 0x00000100 | 0x00010000 | 0x00040000 | 0x00080000
        | 0x10000000 | 0x40000000
    )
    return mask & write_or_delete == 0


def _verify_windows_acl_values(
    owner: str,
    dacl: str,
    *,
    managed: bool,
    os_anchor: bool = False,
) -> None:
    current = _windows_current_sid()
    if (managed or os_anchor) and owner != current:
        raise PathCapabilityUnavailable("managed path is not owned by this principal")
    if "D:NO_ACCESS_CONTROL" in dacl:
        raise PathCapabilityUnavailable("owned path has an unprotected DACL")
    if managed or os_anchor:
        allowed = {
            current, "OW", "SY", "BA", "S-1-5-18", "S-1-5-32-544"
        }
        aces = re.findall(r"\(([^)]*)\)", dacl)
        if not aces:
            raise PathCapabilityUnavailable("managed path DACL is empty")
        for ace in aces:
            fields = ace.split(";")
            if len(fields) < 6:
                raise PathCapabilityUnavailable("managed path DACL is malformed")
            if fields[0] == "D":
                continue
            if fields[0] != "A":
                raise PathCapabilityUnavailable("managed path DACL has an unsupported ACE")
            if fields[5] not in allowed and not (
                os_anchor and _windows_rights_are_read_only(fields[2])
            ):
                raise PathCapabilityUnavailable("managed path DACL grants an unexpected principal")


def _verify_windows_acl(path: Path, *, managed: bool) -> None:
    _verify_windows_acl_values(*_windows_sddl(path), managed=managed)


def _verify_windows_handle_acl(
    handle: int, *, managed: bool, os_anchor: bool = False
) -> None:
    _verify_windows_acl_values(
        *_windows_handle_sddl(handle),
        managed=managed,
        os_anchor=os_anchor,
    )


def _validate_posix_ancestor(info: os.stat_result, require_private_child: bool) -> bool:
    mode = stat.S_IMODE(info.st_mode)
    owner = info.st_uid
    if owner not in {0, os.geteuid()}:
        raise PathCapabilityUnavailable(
            "owned path ancestor has an untrusted owner"
        )
    if require_private_child and (
        owner != os.geteuid() or mode & 0o077
    ):
        raise PathCapabilityUnavailable(
            "sticky path child is not owner-private"
        )
    if mode & 0o022:
        if not mode & stat.S_ISVTX:
            raise PathCapabilityUnavailable(
                "owned path ancestor is writable by another principal"
            )
        return True
    return False


def _posix_open_flags() -> tuple[int, int]:
    directory = getattr(os, "O_DIRECTORY", None)
    no_follow = getattr(os, "O_NOFOLLOW", None)
    if not isinstance(directory, int) or not isinstance(no_follow, int):
        raise PathCapabilityUnavailable(
            "host lacks required no-follow directory traversal"
        )
    return directory, no_follow


class CheckedPathCapability:
    """Pinned component and leaf identities for one connection/lock scope."""

    def __init__(
        self, path: Path, *, create: bool, read_only: bool,
        expected: PathIdentity | None = None,
        trusted_root: Path | None = None,
        os_known_root: bool = False,
    ) -> None:
        self.path = _validate_absolute_path(path)
        self._trusted_root = _validate_absolute_path(
            trusted_root
            if trusted_root is not None
            else nearest_existing_trusted_root(self.path.parent)
        )
        self._os_known_root = os_known_root
        _relative_parts(self.path, self._trusted_root)
        self._handles: list[int] = []
        self._fds: list[int] = []
        self._closed = False
        self._read_only = read_only
        try:
            self._prepare_parent(create=create and not read_only)
            if not self.path.exists() and not self.path.is_symlink():
                if not create or read_only:
                    raise PathCapabilityUnavailable("owned path does not exist")
                self._create_leaf()
            self.identity = self._pin_leaf()
            if expected is not None and self.identity != expected:
                raise PathCapabilityUnavailable("owned path identity changed")
            self.check_sidecars()
        except BaseException:
            self.close()
            raise

    def _prepare_parent(self, *, create: bool) -> None:
        parent = self.path.parent
        if sys.platform == "win32":
            if _kernel32.GetDriveTypeW(self.path.anchor) != 3:
                raise PathCapabilityUnavailable(
                    "owned path is not on a fixed Windows drive"
                )
            volume_root = Path(self.path.anchor)
            root_handle = _windows_handle(
                volume_root,
                directory=True,
                protect_delete=False,
                open_reparse=True,
            )
            self._handles.append(root_handle)
            volume_identity, _, _ = _windows_info(root_handle)
            _verify_windows_handle_acl(root_handle, managed=False)

            trusted_root = self._trusted_root
            trusted_handle = _windows_handle(
                trusted_root,
                directory=True,
                protect_delete=True,
                open_reparse=True,
            )
            self._handles.append(trusted_handle)
            trusted_identity, _, _ = _windows_info(trusted_handle)
            _verify_windows_handle_acl(
                trusted_handle,
                managed=not self._os_known_root,
                os_anchor=self._os_known_root,
            )
            if self._os_known_root:
                final_path = _validate_absolute_path(Path(
                    _windows_final_path(trusted_handle)
                ))
                if _windows_normalized_path(
                    final_path
                ) != _windows_normalized_path(trusted_root):
                    raise PathCapabilityUnavailable(
                        "Windows known-folder handle path does not match"
                    )
                comparison_handle = _windows_handle(
                    trusted_root,
                    directory=True,
                    protect_delete=False,
                    open_reparse=True,
                )
                try:
                    comparison_identity, _, _ = _windows_info(comparison_handle)
                finally:
                    _kernel32.CloseHandle(comparison_handle)
                if comparison_identity != trusted_identity:
                    raise PathCapabilityUnavailable(
                        "Windows known-folder handle identity does not match"
                    )
            if trusted_identity[0] != volume_identity[0]:
                raise PathCapabilityUnavailable(
                    "owned path crosses a volume boundary"
                )

            current = trusted_root
            component_ids = [volume_identity, trusted_identity]
            descendant_parts = _relative_parts(parent, trusted_root)
            for part in descendant_parts:
                current = current / part
                if not current.exists():
                    if not create:
                        raise PathCapabilityUnavailable(
                            "owned path ancestor is missing"
                        )
                    _windows_create_directory(current)
                handle = _windows_handle(
                    current,
                    directory=True,
                    protect_delete=True,
                    open_reparse=True,
                )
                self._handles.append(handle)
                identity, _, _ = _windows_info(handle)
                _verify_windows_handle_acl(handle, managed=True)
                if identity[0] != volume_identity[0]:
                    raise PathCapabilityUnavailable("owned path crosses a volume boundary")
                component_ids.append(identity)
            self._component_ids = tuple(component_ids)
            return
        directory_flag, no_follow_flag = _posix_open_flags()
        fd = os.open("/", os.O_RDONLY | directory_flag)
        self._fds.append(fd)
        root_stat = os.fstat(fd)
        device = root_stat.st_dev
        component_ids: list[tuple[int, int]] = []
        require_private_child = False
        for part in self.path.parts[1:-1]:
            if create:
                try:
                    os.mkdir(part, 0o700, dir_fd=fd)
                except FileExistsError:
                    pass
            try:
                next_fd = os.open(
                    part,
                    os.O_RDONLY | directory_flag | no_follow_flag,
                    dir_fd=fd,
                )
            except FileNotFoundError as error:
                raise PathCapabilityUnavailable(
                    "owned path ancestor is missing"
                ) from error
            except OSError as error:
                if error.errno in {errno.ELOOP, errno.ENOTDIR}:
                    raise PathCapabilityUnavailable(
                        "symlink or redirected ancestor refused in owned path"
                    ) from error
                raise
            self._fds.append(next_fd)
            info = os.fstat(next_fd)
            if info.st_dev != device:
                raise PathCapabilityUnavailable("owned path crosses a mount boundary")
            if not stat.S_ISDIR(info.st_mode):
                raise PathCapabilityUnavailable("owned path ancestor is not a directory")
            require_private_child = _validate_posix_ancestor(
                info, require_private_child
            )
            fd = next_fd
            component_ids.append((info.st_dev, info.st_ino))
        parent_info = os.fstat(fd)
        if parent_info.st_uid != os.geteuid() or stat.S_IMODE(parent_info.st_mode) & 0o077:
            raise PathCapabilityUnavailable("managed path parent is not owner-private")
        self._component_ids = tuple(component_ids)

    def _create_leaf(self) -> None:
        if sys.platform == "win32":
            attributes, security_descriptor = _windows_security_attributes()
            try:
                handle = _kernel32.CreateFileW(
                    str(self.path), 0x80000000 | 0x40000000,
                    _FILE_SHARE_READ | _FILE_SHARE_WRITE,
                    ctypes.byref(attributes), _CREATE_NEW,
                    _FILE_FLAG_OPEN_REPARSE_POINT, None,
                )
                if handle == _INVALID_HANDLE:
                    raise PathCapabilityUnavailable(
                        "restrictive Windows file creation failed"
                    )
                _kernel32.CloseHandle(handle)
            finally:
                _kernel32.LocalFree(security_descriptor)
            _verify_windows_acl(self.path, managed=True)
            return
        _, no_follow_flag = _posix_open_flags()
        descriptor = os.open(
            self.path.name,
            os.O_RDWR | os.O_CREAT | os.O_EXCL | no_follow_flag,
            0o600,
            dir_fd=self._fds[-1],
        )
        os.close(descriptor)

    def _pin_leaf(self) -> PathIdentity:
        if sys.platform == "win32":
            handle = _windows_handle(self.path)
            self._handles.append(handle)
            identity, links, attributes = _windows_info(handle)
            if attributes & 0x10 or links != 1:
                raise PathCapabilityUnavailable("owned database leaf is not a single-link file")
            _verify_windows_handle_acl(handle, managed=True)
            return PathIdentity("win32", self._component_ids, identity, str(self.path))
        _, no_follow_flag = _posix_open_flags()
        descriptor = os.open(
            self.path.name,
            (os.O_RDONLY if self._read_only else os.O_RDWR)
            | no_follow_flag,
            dir_fd=self._fds[-1],
        )
        self._fds.append(descriptor)
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode):
            raise PathCapabilityUnavailable(
                "owned database leaf is not a regular file"
            )
        if info.st_nlink != 1:
            raise PathCapabilityUnavailable(
                "owned database leaf is not a single-link file"
            )
        if info.st_uid != os.geteuid() or stat.S_IMODE(info.st_mode) & 0o077:
            raise PathCapabilityUnavailable("owned database leaf is not owner-private")
        return PathIdentity(
            "posix", self._component_ids, (info.st_dev, info.st_ino), str(self.path)
        )

    def assert_current(self) -> None:
        if self._closed:
            raise PathCapabilityUnavailable("owned path capability is closed")
        probe = os.lstat(self.path)
        if stat.S_ISLNK(probe.st_mode) or getattr(probe, "st_file_attributes", 0) & _REPARSE_FLAG:
            raise PathCapabilityUnavailable("owned database leaf was redirected")
        if sys.platform == "win32":
            current_handle = _windows_handle(
                self.path, protect_delete=False, open_reparse=True
            )
            try:
                current, links, _ = _windows_info(current_handle)
                _verify_windows_handle_acl(current_handle, managed=True)
            finally:
                _kernel32.CloseHandle(current_handle)
            if links != 1:
                raise PathCapabilityUnavailable(
                    "owned database leaf is not a single-link file"
                )
        else:
            current = (int(probe.st_dev), int(probe.st_ino))
            if (
                not stat.S_ISREG(probe.st_mode)
                or probe.st_uid != os.geteuid()
                or stat.S_IMODE(probe.st_mode) & 0o077
                or probe.st_nlink != 1
            ):
                raise PathCapabilityUnavailable(
                    "owned database leaf is not owner-private"
                )
        if current != self.identity.leaf:
            raise PathCapabilityUnavailable("owned database leaf identity changed")

    def check_sidecars(self) -> None:
        for suffix in ("-wal", "-shm"):
            candidate = Path(str(self.path) + suffix)
            if candidate.exists() or candidate.is_symlink():
                raise PathCapabilityUnavailable("unexpected SQLite sidecar is present")
        journal = Path(str(self.path) + "-journal")
        if not journal.exists() and not journal.is_symlink():
            return
        probe = os.lstat(journal)
        if (
            stat.S_ISLNK(probe.st_mode)
            or getattr(probe, "st_file_attributes", 0) & _REPARSE_FLAG
            or not stat.S_ISREG(probe.st_mode)
            or probe.st_nlink != 1
        ):
            raise PathCapabilityUnavailable("unsafe SQLite rollback journal is present")
        if sys.platform == "win32":
            handle = _windows_handle(journal)
            try:
                _windows_info(handle)
                _verify_windows_handle_acl(handle, managed=True)
            finally:
                _kernel32.CloseHandle(handle)
        elif probe.st_uid != os.geteuid() or stat.S_IMODE(probe.st_mode) & 0o077:
            raise PathCapabilityUnavailable("SQLite rollback journal is not owner-private")

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        if sys.platform == "win32":
            _close_windows(reversed(self._handles))
        else:
            for descriptor in reversed(self._fds):
                os.close(descriptor)
        self._handles.clear()
        self._fds.clear()


class CheckedSQLiteConnection(sqlite3.Connection):
    _owned_path_capability: CheckedPathCapability | None = None

    def _check_owned_path(self) -> None:
        if self._owned_path_capability is not None:
            self._owned_path_capability.assert_current()
            self._owned_path_capability.check_sidecars()

    def commit(self) -> None:
        super().commit()
        self._check_owned_path()

    def rollback(self) -> None:
        super().rollback()
        self._check_owned_path()

    def close(self) -> None:
        capability = self._owned_path_capability
        try:
            super().close()
            if capability is not None:
                capability.assert_current()
                capability.check_sidecars()
        finally:
            if capability is not None:
                capability.close()
                self._owned_path_capability = None


def connect_checked(
    path: Path,
    *,
    expected: PathIdentity,
    read_only: bool = False,
    trusted_root: Path | None = None,
    os_known_root: bool = False,
) -> CheckedSQLiteConnection:
    capability = CheckedPathCapability(
        path,
        create=False,
        read_only=read_only,
        expected=expected,
        trusted_root=trusted_root,
        os_known_root=os_known_root,
    )
    connection: CheckedSQLiteConnection | None = None
    try:
        target = (
            f"{path.as_uri()}?mode=ro"
            if read_only
            else os.fspath(path)
        )
        connection = sqlite3.connect(
            target,
            uri=read_only,
            isolation_level=None,
            factory=CheckedSQLiteConnection,
        )
        connection._owned_path_capability = capability
        capability.assert_current()
        capability.check_sidecars()
        return connection
    except BaseException:
        if connection is not None:
            connection.close()
        capability.close()
        raise


def prepare_owned_file(
    path: Path,
    *,
    create: bool,
    trusted_root: Path | None = None,
    os_known_root: bool = False,
) -> PathIdentity:
    capability = CheckedPathCapability(
        path,
        create=create,
        read_only=not create,
        trusted_root=trusted_root,
        os_known_root=os_known_root,
    )
    try:
        return capability.identity
    finally:
        capability.close()


def probe_owned_path_identity(
    path: Path, *, expected: PathIdentity, trusted_root: Path,
) -> PathIdentity:
    """Read-only offline identity probe; not an open-time real-I/O guarantee."""
    capability = CheckedPathCapability(
        path, create=False, read_only=True, expected=expected,
        trusted_root=trusted_root,
    )
    try:
        capability.assert_current()
        return capability.identity
    finally:
        capability.close()
