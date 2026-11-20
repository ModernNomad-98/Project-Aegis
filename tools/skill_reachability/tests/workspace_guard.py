#!/usr/bin/env python3
"""Workspace-mutation guard for the local-only skill-reachability tests (#1140).

Issue #1140 is a T-13 residual: a review round found that a test had deleted a
pre-existing repository file inside the checkout, and nothing then failed if
test code reintroduced a workspace deletion. This guard closes that gap: it
snapshots the working tree, runs a command (by default this tool's local test
suite), snapshots again, and fails when anything was added, removed or
modified.

The snapshot covers every file and directory under the tree, so it includes
tracked and untracked paths alike. The top-level .git entry is the only
exclusion: that is repository metadata rather than a workspace file, and a test
run must not be expected to re-hash it. The separate cleanliness check that the
checkout is unchanged is still a plain "git status".

The guarded command always runs with PYTHONDONTWRITEBYTECODE=1, so interpreter
bytecode caches written inside the tree are not misreported as test-run
mutations. A deleted, added or edited workspace file is reported and the guard
exits 1.

Standard library only. The guard itself writes nothing; the supplied command is
responsible for its own writes.

Usage:
    python -P tools/skill_reachability/tests/workspace_guard.py
    python -P tools/skill_reachability/tests/workspace_guard.py --tree REPO -- COMMAND ...
    python -P tools/skill_reachability/tests/workspace_guard.py -- COMMAND ...

Exit codes:
    0  the command exited 0 and the tree is unchanged
    1  the tree changed, or the guarded command exited non-zero
    2  usage error (bad option, missing or unreadable tree, empty command)
"""
from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TREE = os.path.dirname(os.path.dirname(os.path.dirname(TESTS_DIR)))
DEFAULT_COMMAND = [sys.executable, "-P", "-m", "unittest", "discover",
                   "-s", TESTS_DIR, "-p", "test_*.py"]
SKIPPED_TOP_LEVEL = frozenset({".git"})
PREFIX = "workspace-guard:"
CHUNK_BYTES = 1 << 20


def file_digest(path):
    """Return the sha256 hex digest of a file's bytes."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(CHUNK_BYTES)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def snapshot_tree(root):
    """Return {relative posix path: entry tuple} for every entry under root.

    Directories, regular files and symlinks are recorded and the top-level .git
    entry is skipped. Tuple shapes: ("dir",), ("file", size, sha256),
    ("symlink", target), ("other",).
    """
    entries = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        filenames.sort()
        relative_dir = os.path.relpath(dirpath, root)
        at_root = relative_dir == "."
        if at_root:
            dirnames[:] = [name for name in dirnames if name not in SKIPPED_TOP_LEVEL]
            relative_dir = ""
        else:
            relative_dir = relative_dir.replace(os.sep, "/")
        for name in dirnames:
            relative = name if at_root else relative_dir + "/" + name
            full = os.path.join(dirpath, name)
            if os.path.islink(full):
                entries[relative] = ("symlink", os.readlink(full))
            else:
                entries[relative] = ("dir",)
        for name in filenames:
            if at_root and name in SKIPPED_TOP_LEVEL:
                continue
            relative = name if at_root else relative_dir + "/" + name
            full = os.path.join(dirpath, name)
            if os.path.islink(full):
                entries[relative] = ("symlink", os.readlink(full))
            elif os.path.isfile(full):
                entries[relative] = ("file", os.path.getsize(full), file_digest(full))
            else:
                entries[relative] = ("other",)
    return entries


def compare_snapshots(before, after):
    """Return sorted (kind, relative path) changes between two snapshots."""
    changes = []
    for relative in sorted(set(before) | set(after)):
        old = before.get(relative)
        new = after.get(relative)
        if old == new:
            continue
        if new is None:
            changes.append(("REMOVED", relative))
        elif old is None:
            changes.append(("ADDED", relative))
        else:
            changes.append(("MODIFIED", relative))
    return changes


def count_kind(entries, kind):
    return sum(1 for entry in entries.values() if entry[0] == kind)


def parse_arguments(argv):
    parser = argparse.ArgumentParser(
        prog="workspace_guard.py",
        description="Run a command and fail if it changes the workspace tree.")
    parser.add_argument("--tree", default=DEFAULT_TREE,
                        help="tree to snapshot (default: this checkout root)")
    parser.add_argument("command", nargs=argparse.REMAINDER,
                        help="command to run; everything after -- is passed verbatim")
    arguments = parser.parse_args(argv)
    raw_command = list(arguments.command)
    if raw_command and raw_command[0] == "--":
        raw_command = raw_command[1:]
    if raw_command:
        command = raw_command
    elif arguments.command:
        parser.error("no command after --")
    else:
        command = list(DEFAULT_COMMAND)
    return arguments.tree, command


def main(argv=None):
    tree, command = parse_arguments(argv)
    tree = os.path.abspath(tree)
    if not os.path.isdir(tree):
        print("%s ERROR tree is not a directory: %s" % (PREFIX, tree), file=sys.stderr)
        return 2
    before = snapshot_tree(tree)
    print("%s snapshot tree=%s entries=%d files=%d dirs=%d"
          % (PREFIX, tree, len(before), count_kind(before, "file"),
             count_kind(before, "dir")))
    print("%s running: %s" % (PREFIX, " ".join(command)))
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        completed = subprocess.run(command, cwd=tree, env=environment)
    except OSError as error:
        print("%s ERROR cannot run command: %s" % (PREFIX, error), file=sys.stderr)
        return 2
    after = snapshot_tree(tree)
    changes = compare_snapshots(before, after)
    for kind, relative in changes:
        print("CHANGE %s %s" % (kind, relative))
    ok = completed.returncode == 0 and not changes
    print("%s %s tree=%s files=%d dirs=%d changes=%d command_exit=%d"
          % (PREFIX, "PASS" if ok else "FAIL", tree, count_kind(after, "file"),
             count_kind(after, "dir"), len(changes), completed.returncode))
    if changes:
        print("%s the run changed the working tree; this is the issue #1140 guard failing"
              % PREFIX)
    if completed.returncode != 0:
        print("%s the guarded command exited %d" % (PREFIX, completed.returncode))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
