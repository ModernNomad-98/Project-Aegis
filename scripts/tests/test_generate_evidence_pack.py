#!/usr/bin/env python3
"""Tests for scripts/generate-evidence-pack.py.

These tests build throwaway Git repositories in the system temporary directory.
They run in the advisory path-filtered local-tool-tests job when scripts/ or
tools/ changes; the pack stays a local/PR aid, and this file also runs by hand.

Run:
    python -B -P scripts/tests/test_generate_evidence_pack.py

Git isolation: each repository gets its own user.name, user.email,
commit.gpgsign=false, GIT_CONFIG_NOSYSTEM=1 and an empty throwaway
GIT_CONFIG_GLOBAL. Every Git invocation passes -c safe.directory=<repo>, and
the generator subprocess also receives safe.directory through GIT_CONFIG_COUNT,
because Windows temporary directories can otherwise trigger Git's "dubious
ownership" check. If Git is missing, or ownership/ACL still blocks the temp
root, the affected tests skip with the reason printed.

The tab-containing path is committed through Git's own tree plumbing
(hash-object, mktree, commit-tree, update-ref): Windows file-name rules reject
a tab in a real file name, and git update-index rejects it too, but a tree
object carries the bytes and the three-dot diff reports them. That exercises
the NUL-separated parsing exactly as on a POSIX host. A symlink/typechange
entry is committed the same way, so the generator's null content-fact rule for
mode 120000 is tested without needing OS symlink privilege.
"""
from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "scripts" / "generate-evidence-pack.py"

GUIDE = "# Guide\n\nOne.\n"
ALPHA_A = "def alpha():\n    return 1\n"
ALPHA_B = "def alpha():\n    return 2\n\ndef beta():\n    return 3\n"
GAMMA = "GAMMA = True\n"
BINARY = b"\x00\x01PNG\r\n\x1a\n\xff\xfe"
TAB_NAME = "tab\tna\u00efve-\u0394.md"
TAB_PATH = "docs/" + TAB_NAME
TAB_CONTENT = b"tabbed\n"


def load_generator():
    """Load the hyphenated script by path; it is not an importable name."""
    spec = importlib.util.spec_from_file_location(
        "generate_evidence_pack_under_test", SCRIPT_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GENERATOR = load_generator()


def skip(reason):
    """Print the reason, then raise unittest's skip signal."""
    print(f"SKIP: {reason}", file=sys.stderr)
    raise unittest.SkipTest(reason)


def environment_error(text):
    lowered = (text or "").lower()
    return (
        "dubious ownership" in lowered
        or "safe.directory" in lowered
        or "not owned by current user" in lowered
        or "permission denied" in lowered
        or "access is denied" in lowered
        or "unable to create" in lowered
    )


def git_env(tmp):
    """Build an isolated environment: no system config, no inherited GIT_*."""
    env = {key: value for key, value in os.environ.items()
           if not key.startswith("GIT_")}
    global_config = Path(tmp) / "gitconfig-global"
    global_config.write_text("", encoding="utf-8")
    env.update({
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": str(global_config),
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_AUTHOR_NAME": "Evidence Pack Test",
        "GIT_AUTHOR_EMAIL": "evidence-pack@example.invalid",
        "GIT_COMMITTER_NAME": "Evidence Pack Test",
        "GIT_COMMITTER_EMAIL": "evidence-pack@example.invalid",
    })
    return env


def git_base(repo):
    return ["git", "-c", f"safe.directory={repo}", "-C", str(repo)]


def run_git_bytes(repo, *args, env, input_bytes=None):
    """Run Git and return raw stdout bytes."""
    command = [*git_base(repo), *args]
    try:
        proc = subprocess.run(
            command,
            input=input_bytes,
            capture_output=True,
            env=env,
            timeout=60,
            shell=False,
        )
    except FileNotFoundError:
        skip("git executable not found")
    except (subprocess.TimeoutExpired, OSError) as exc:
        skip(f"git could not be run: {exc}")
    if proc.returncode != 0:
        detail = (proc.stderr or b"").decode("utf-8", "replace").strip()
        if environment_error(detail):
            skip(f"git environment restriction: {detail}")
        raise AssertionError(
            f"git {' '.join(args)} failed ({proc.returncode}): {detail}"
        )
    return proc.stdout


def run_git(repo, *args, env):
    return run_git_bytes(repo, *args, env=env).decode("utf-8", "replace")


def rev_parse(repo, revision, env):
    return run_git(repo, "rev-parse", revision, env=env).strip()


def write_text(repo, name, text):
    path = Path(repo) / name
    path.parent.mkdir(parents=True, exist_ok=True)
    # newline="" keeps LF as one byte on Windows, so blob assertions match
    # the constants' UTF-8 bytes on every host.
    path.write_text(text, encoding="utf-8", newline="")


def blob_id(repo, env, data):
    return run_git_bytes(
        repo, "hash-object", "-w", "--stdin", env=env, input_bytes=data
    ).decode("ascii").strip()


def make_tree(repo, env, entries):
    payload = b"".join(entry + b"\0" for entry in entries)
    return run_git_bytes(
        repo, "mktree", "-z", env=env, input_bytes=payload
    ).decode("ascii").strip()


def list_tree(repo, env, revision):
    raw = run_git_bytes(repo, "ls-tree", "-z", revision, env=env)
    return [entry for entry in raw.split(b"\0") if entry]


def make_commit(repo, env, tree, parents, message):
    args = ["commit-tree", tree]
    for parent in parents:
        args.extend(["-p", parent])
    args.extend(["-m", message])
    return run_git(repo, *args, env=env).strip()


def make_repo(tmp):
    """Initialise a repository with a local identity and signing disabled."""
    repo = (Path(tmp) / "repo").resolve()
    repo.mkdir(parents=True)
    env = git_env(tmp)
    env["GIT_CONFIG_COUNT"] = "1"
    env["GIT_CONFIG_KEY_0"] = "safe.directory"
    env["GIT_CONFIG_VALUE_0"] = str(repo)
    try:
        run_git(repo, "init", "-q", "-b", "main", env=env)
        run_git(repo, "config", "user.name", "Evidence Pack Test", env=env)
        run_git(repo, "config", "user.email",
                "evidence-pack@example.invalid", env=env)
        run_git(repo, "config", "commit.gpgsign", "false", env=env)
        run_git(repo, "config", "core.autocrlf", "false", env=env)
    except OSError as exc:
        skip(f"temporary repository could not be created: {exc}")
    return repo, env


def write_manifest(repo, revision):
    manifest = Path(repo) / "tools" / "skills-manifest.json"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "aegis.skills-manifest/1",
        "source_revision": revision,
        "skills": [],
    }
    manifest.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline=""
    )
    return manifest


def build_change_repo(tmp):
    """Build commit A, a side commit, then commit B with the required change.

    B modifies one file, adds one, deletes one, adds a binary, and adds a
    path with a tab and non-ASCII characters. B's tree is assembled with
    plumbing so the tab path can exist on Windows.
    """
    repo, env = make_repo(tmp)
    write_text(repo, "scripts/alpha.py", ALPHA_A)
    write_text(repo, "docs/guide.md", GUIDE)
    write_text(repo, "old.txt", "remove me\n")
    run_git(repo, "add", "--all", env=env)
    run_git(repo, "commit", "-q", "-m", "A", env=env)
    commit_a = rev_parse(repo, "HEAD", env)

    side = make_commit(repo, env, rev_parse(repo, "HEAD^{tree}", env),
                       [commit_a], "side")
    run_git(repo, "update-ref", "refs/heads/side", side, env=env)

    write_text(repo, "scripts/alpha.py", ALPHA_B)
    write_text(repo, "scripts/gamma.py", GAMMA)
    (Path(repo) / "old.txt").unlink()
    assets = Path(repo) / "assets"
    assets.mkdir()
    (assets / "logo.bin").write_bytes(BINARY)
    run_git(repo, "add", "--all", env=env)
    staged_tree = run_git(repo, "write-tree", env=env).strip()

    tab_entry = (
        b"100644 blob " + blob_id(repo, env, TAB_CONTENT).encode("ascii")
        + b"\t" + TAB_NAME.encode("utf-8")
    )
    docs_entries = list_tree(repo, env, f"{staged_tree}:docs") + [tab_entry]
    docs_tree = make_tree(repo, env, docs_entries)

    root_entries = []
    for entry in list_tree(repo, env, staged_tree):
        if entry.split(b"\t", 1)[1] == b"docs":
            root_entries.append(
                b"040000 tree " + docs_tree.encode("ascii") + b"\tdocs"
            )
        else:
            root_entries.append(entry)
    root_tree = make_tree(repo, env, root_entries)
    commit_b = make_commit(repo, env, root_tree, [commit_a], "B")
    run_git(repo, "update-ref", "refs/heads/main", commit_b, env=env)
    if rev_parse(repo, "HEAD", env) != commit_b:
        raise AssertionError("HEAD did not move to the constructed commit B")

    manifest = write_manifest(repo, commit_a)
    return repo, env, commit_a, commit_b, side, manifest


def make_temp_root():
    """Create a unique writable directory under the system temp root."""
    base = Path(tempfile.gettempdir())
    for index in range(1000):
        candidate = base / f"aegis-evidence-pack-{os.getpid()}-{index}"
        try:
            candidate.mkdir()
        except FileExistsError:
            continue
        return candidate.resolve()
    raise RuntimeError("could not create a unique temporary directory")


class EvidencePackTests(unittest.TestCase):
    def setUp(self):
        if shutil.which("git") is None:
            skip("git executable not found")
        self.tmp = make_temp_root()
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        (self.repo, self.env, self.a, self.b, self.side,
         self.manifest) = build_change_repo(self.tmp)

    def output_dir(self):
        directory = Path(self.tmp) / "out"
        directory.mkdir(exist_ok=True)
        return directory

    def run_pack(self, *args, out=None, repo_root=None, base=None):
        directory = self.output_dir()
        if out is None:
            out = directory / f"pack-{len(list(directory.iterdir()))}.json"
        command = [
            sys.executable, "-B", str(SCRIPT_PATH),
            "--repo-root", str(repo_root or self.repo),
            "--base", base or self.a,
            "--out", str(out),
            *args,
        ]
        proc = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=self.env,
            cwd=str(self.repo),
            timeout=120,
            shell=False,
        )
        return proc, Path(out)

    def run_ok(self, *args, out=None, base=None):
        proc, target = self.run_pack(*args, out=out, base=base)
        self.assertEqual(0, proc.returncode, proc.stderr)
        self.assertEqual("", proc.stderr, proc.stderr)
        self.assertTrue(target.is_file(), "pack was not written")
        return json.loads(target.read_text(encoding="utf-8")), target

    def test_pack_records_expected_facts(self):
        pack, target = self.run_ok(
            "--manifest", "tools/skills-manifest.json",
            "--plan", "docs/guide.md",
            "--gate-pattern", "^scripts/",
            "--gate-pattern", "^docs/",
        )
        self.assertEqual("aegis.evidence-pack/1", pack["schema"])
        self.assertEqual("OK", pack["status"])
        self.assertEqual(self.a, pack["base"])
        self.assertEqual(self.b, pack["head"])
        self.assertEqual(self.a, pack["merge_base"])
        self.assertEqual(
            ["base", "changed", "gate", "head", "manifest", "merge_base",
             "plan", "schema", "status"],
            sorted(pack),
        )

        changed = {entry["path"]: entry for entry in pack["changed"]}
        self.assertEqual(
            {"scripts/alpha.py", "scripts/gamma.py", "old.txt",
             "assets/logo.bin", TAB_PATH},
            set(changed),
        )
        self.assertEqual(
            ["assets/logo.bin", TAB_PATH, "old.txt", "scripts/alpha.py",
             "scripts/gamma.py"],
            [entry["path"] for entry in pack["changed"]],
            "changed files must be sorted by path",
        )

        alpha = changed["scripts/alpha.py"]
        self.assertEqual("M", alpha["status"])
        self.assertEqual("100644", alpha["mode"])
        self.assertEqual(4, alpha["additions"])
        self.assertEqual(1, alpha["deletions"])
        alpha_bytes = ALPHA_B.encode("utf-8")
        self.assertEqual(hashlib.sha256(alpha_bytes).hexdigest(),
                         alpha["sha256"])
        self.assertEqual(len(alpha_bytes), alpha["bytes"])
        self.assertEqual(5, alpha["lines"])

        gamma = changed["scripts/gamma.py"]
        self.assertEqual("A", gamma["status"])
        self.assertEqual(1, gamma["additions"])
        self.assertEqual(0, gamma["deletions"])
        self.assertEqual(hashlib.sha256(GAMMA.encode()).hexdigest(),
                         gamma["sha256"])
        self.assertEqual(1, gamma["lines"])

        deleted = changed["old.txt"]
        self.assertEqual("D", deleted["status"])
        self.assertIsNone(deleted["sha256"])
        self.assertIsNone(deleted["bytes"])
        self.assertIsNone(deleted["lines"])
        self.assertEqual(0, deleted["additions"])
        self.assertEqual(1, deleted["deletions"])

        binary = changed["assets/logo.bin"]
        self.assertEqual("A", binary["status"])
        self.assertIsNone(binary["additions"], "binary numstat is '-'")
        self.assertIsNone(binary["deletions"], "binary numstat is '-'")
        self.assertEqual(hashlib.sha256(BINARY).hexdigest(), binary["sha256"])
        self.assertEqual(len(BINARY), binary["bytes"])

        tab = changed[TAB_PATH]
        self.assertEqual("A", tab["status"])
        self.assertEqual("100644", tab["mode"])
        self.assertEqual(hashlib.sha256(TAB_CONTENT).hexdigest(), tab["sha256"])
        self.assertEqual(len(TAB_CONTENT), tab["bytes"])
        self.assertEqual(1, tab["lines"])

        ancestry = pack["manifest"]["ancestry"]
        self.assertEqual("PASS", ancestry["status"])
        self.assertEqual(self.a, ancestry["source_revision"])
        self.assertEqual(self.b, ancestry["head"])
        manifest_bytes = self.manifest.read_bytes()
        self.assertEqual(hashlib.sha256(manifest_bytes).hexdigest(),
                         pack["manifest"]["sha256"])
        self.assertEqual(len(manifest_bytes), pack["manifest"]["bytes"])

        self.assertEqual(["^scripts/", "^docs/"], pack["gate"]["patterns"])
        self.assertEqual(
            [
                {"path": TAB_PATH, "pattern": "^docs/"},
                {"path": "scripts/alpha.py", "pattern": "^scripts/"},
                {"path": "scripts/gamma.py", "pattern": "^scripts/"},
            ],
            pack["gate"]["matches"],
        )

        guide_bytes = GUIDE.encode("utf-8")
        self.assertEqual(
            {
                "path": "docs/guide.md",
                "sha256": hashlib.sha256(guide_bytes).hexdigest(),
                "bytes": len(guide_bytes),
                "lines": 3,
            },
            pack["plan"],
        )

        text = target.read_text(encoding="utf-8")
        self.assertNotIn(str(self.repo), text, "pack must not record an "
                                               "absolute repository path")
        self.assertNotIn(str(self.tmp), text)

    def test_two_runs_are_byte_identical(self):
        first, first_path = self.run_ok(
            "--gate-pattern", "^scripts/",
            "--plan", "docs/guide.md",
        )
        second, second_path = self.run_ok(
            "--gate-pattern", "^scripts/",
            "--plan", "docs/guide.md",
            out=Path(self.tmp) / "out" / "pack-second.json",
        )
        self.assertEqual(first, second)
        self.assertEqual(first_path.read_bytes(), second_path.read_bytes())

    def test_missing_base_is_a_generation_error(self):
        proc, target = self.run_pack(base="refs/heads/does-not-exist")
        self.assertEqual(2, proc.returncode)
        self.assertIn("ERROR", proc.stderr)
        self.assertFalse(target.exists())

    def test_invalid_gate_pattern_is_a_generation_error(self):
        proc, target = self.run_pack("--gate-pattern", "[")
        self.assertEqual(2, proc.returncode)
        self.assertIn("invalid gate pattern", proc.stderr)
        self.assertFalse(target.exists())

    def test_output_inside_repository_is_refused(self):
        proc, target = self.run_pack(
            out=Path(self.repo) / "evidence-pack.json"
        )
        self.assertEqual(2, proc.returncode)
        self.assertIn("outside the repository", proc.stderr)
        self.assertFalse(target.exists())

    def test_missing_manifest_is_a_generation_error(self):
        self.manifest.unlink()
        proc, target = self.run_pack()
        self.assertEqual(2, proc.returncode)
        self.assertIn("manifest", proc.stderr.lower())
        self.assertFalse(target.exists())

    def test_manifest_path_must_be_repository_relative(self):
        for bad in (str(self.manifest.resolve()),
                    "../tools/skills-manifest.json"):
            with self.subTest(path=bad):
                proc, target = self.run_pack("--manifest", bad)
                self.assertEqual(2, proc.returncode)
                self.assertIn("manifest path", proc.stderr)
                self.assertNotIn("Traceback", proc.stderr)
                self.assertFalse(target.exists())

    def test_absolute_plan_is_recorded_relative(self):
        absolute = (Path(self.repo) / "docs" / "guide.md").resolve()
        pack, _target = self.run_ok("--plan", str(absolute))
        guide_bytes = GUIDE.encode("utf-8")
        self.assertEqual("docs/guide.md", pack["plan"]["path"])
        self.assertEqual(hashlib.sha256(guide_bytes).hexdigest(),
                         pack["plan"]["sha256"])
        self.assertEqual(len(guide_bytes), pack["plan"]["bytes"])

    def test_head_must_match_worktree_head(self):
        write_text(self.repo, "later.txt", "later\n")
        run_git(self.repo, "add", "--all", env=self.env)
        run_git(self.repo, "commit", "-q", "-m", "C", env=self.env)
        later = rev_parse(self.repo, "HEAD", self.env)
        self.assertNotEqual(self.b, later)
        proc, target = self.run_pack("--head", self.b)
        self.assertEqual(2, proc.returncode)
        self.assertIn("does not match --head", proc.stderr)
        self.assertFalse(target.exists())

    def test_no_common_ancestor_is_a_generation_error(self):
        empty_tree = make_tree(self.repo, self.env, [])
        unrelated = make_commit(
            self.repo, self.env, empty_tree, [], "unrelated root"
        )
        run_git(self.repo, "update-ref", "refs/heads/unrelated",
                unrelated, env=self.env)
        proc, target = self.run_pack(base=unrelated)
        self.assertEqual(2, proc.returncode)
        self.assertIn("ERROR", proc.stderr)
        self.assertFalse(target.exists())

    def test_ancestry_fail_still_writes_the_pack(self):
        write_manifest(self.repo, self.side)
        pack, _target = self.run_ok("--manifest", "tools/skills-manifest.json")
        ancestry = pack["manifest"]["ancestry"]
        self.assertEqual("FAIL", ancestry["status"])
        self.assertEqual(self.side, ancestry["source_revision"])
        self.assertEqual(self.b, ancestry["head"])
        self.assertEqual("OK", pack["status"])

    def test_ancestry_error_still_writes_the_pack(self):
        shallow = Path(self.repo) / ".git" / "shallow"
        shallow.write_text(self.a + "\n", encoding="utf-8")
        self.assertEqual(
            "true",
            run_git(self.repo, "rev-parse", "--is-shallow-repository",
                    env=self.env).strip(),
        )
        pack, _target = self.run_ok()
        ancestry = pack["manifest"]["ancestry"]
        self.assertEqual("ERROR", ancestry["status"])
        self.assertIn("shallow", ancestry["reason"])
        self.assertEqual(self.a, ancestry["source_revision"])
        self.assertEqual("OK", pack["status"])

    def test_typechange_to_symlink_has_null_content_facts(self):
        head_tree = rev_parse(self.repo, "HEAD^{tree}", self.env)
        link_blob = blob_id(self.repo, self.env, b"guide.md")
        docs_entries = []
        for entry in list_tree(self.repo, self.env, f"{head_tree}:docs"):
            if entry.split(b"\t", 1)[1] == b"guide.md":
                docs_entries.append(
                    b"120000 blob " + link_blob.encode("ascii")
                    + b"\tguide.md"
                )
            else:
                docs_entries.append(entry)
        docs_tree = make_tree(self.repo, self.env, docs_entries)
        root_entries = []
        for entry in list_tree(self.repo, self.env, head_tree):
            if entry.split(b"\t", 1)[1] == b"docs":
                root_entries.append(
                    b"040000 tree " + docs_tree.encode("ascii") + b"\tdocs"
                )
            else:
                root_entries.append(entry)
        typechange = make_commit(
            self.repo, self.env,
            make_tree(self.repo, self.env, root_entries),
            [self.b], "typechange",
        )
        run_git(self.repo, "update-ref", "refs/heads/main", typechange,
                env=self.env)

        pack, _target = self.run_ok(base=self.b)
        self.assertEqual(1, len(pack["changed"]))
        entry = pack["changed"][0]
        self.assertEqual("docs/guide.md", entry["path"])
        self.assertEqual("T", entry["status"])
        self.assertEqual("120000", entry["mode"])
        self.assertIsNone(entry["sha256"])
        self.assertIsNone(entry["bytes"])
        self.assertIsNone(entry["lines"])

    def test_unexpected_exception_exits_2_without_traceback(self):
        original = GENERATOR.build_pack

        def explode(_args):
            raise RuntimeError("boom\non two lines")

        GENERATOR.build_pack = explode
        try:
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                code = GENERATOR.main([
                    "--repo-root", str(self.repo),
                    "--base", self.a,
                    "--out", str(Path(self.tmp) / "out" / "never.json"),
                ])
        finally:
            GENERATOR.build_pack = original
        text = stderr.getvalue()
        self.assertEqual(2, code)
        self.assertNotIn("Traceback", text)
        self.assertEqual(1, len(text.strip().splitlines()))
        self.assertIn("RuntimeError", text)
        self.assertIn("boom on two lines", text)

    def test_existing_output_requires_force(self):
        first, target = self.run_ok()
        proc, _ = self.run_pack(out=target)
        self.assertEqual(2, proc.returncode)
        self.assertIn("--force", proc.stderr)
        self.assertEqual(first, json.loads(target.read_text(encoding="utf-8")))
        forced, forced_target = self.run_ok("--force", out=target)
        self.assertEqual(first, forced)
        self.assertEqual(target, forced_target)

    def test_missing_output_parent_is_a_generation_error(self):
        missing = Path(self.tmp) / "no-such-directory" / "pack.json"
        proc, target = self.run_pack(out=missing)
        self.assertEqual(2, proc.returncode)
        self.assertIn("output directory does not exist", proc.stderr)
        self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
