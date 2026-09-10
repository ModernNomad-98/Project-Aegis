"""Fail-closed local evidence I/O and nonblocking process locks."""
from contextlib import contextmanager
import os
import stat

from .calibration_errors import CalibrationAuthorizationError, CalibrationLockError


def check_path(path):
    """Inspect every existing component; never follow links or reparse points."""
    current = os.path.abspath(path)
    leaf = current
    while True:
        try:
            info = os.lstat(current)
        except FileNotFoundError:
            info = None
        if info is not None:
            if os.path.dirname(current) != current and os.path.ismount(current):
                raise CalibrationAuthorizationError('unsafe evidence path: mount crossing')
            if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0):
                raise CalibrationAuthorizationError('unsafe evidence path: link/reparse point')
            if current == leaf and stat.S_ISREG(info.st_mode) and info.st_nlink != 1:
                raise CalibrationAuthorizationError('unsafe evidence path: multiply linked file')
        parent = os.path.dirname(current)
        if current == parent:
            return
        current = parent


@contextmanager
def checked_open(path, mode='r', **kwargs):
    check_path(path)
    # O_NOFOLLOW also protects the final component on supporting hosts.
    def opener(name, flags):
        # Opening must not destroy evidence before the post-open identity
        # checks. Apply truncation to the verified descriptor only.
        return os.open(name, (flags & ~os.O_TRUNC) | getattr(os, 'O_NOFOLLOW', 0), 0o600)
    with open(path, mode, opener=opener, **kwargs) as handle:
        check_path(path)
        actual = os.fstat(handle.fileno())
        named = os.stat(path, follow_symlinks=False)
        if not stat.S_ISREG(actual.st_mode) or (actual.st_dev, actual.st_ino) != (named.st_dev, named.st_ino):
            raise CalibrationAuthorizationError('evidence target changed during open')
        if 'w' in mode:
            handle.truncate(0)
        yield handle


@contextmanager
def exclusive_lock(path):
    """Keep the sidecar: unlinking a lock would permit competing inodes."""
    with checked_open(path, 'a+b') as handle:
        if os.name == 'nt':
            import msvcrt
            handle.seek(0)
            try:
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError as exc:
                raise CalibrationLockError('canonical ledger is locked by another execution') from exc
            try:
                yield
            finally:
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl
            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError as exc:
                raise CalibrationLockError('canonical ledger is locked by another execution') from exc
            try:
                yield
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
