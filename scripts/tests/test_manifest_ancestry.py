#!/usr/bin/env python3
"""Tests for scripts/check-manifest-ancestry.py.

These tests build throwaway Git repositories in the system temporary directory.
They are not wired into CI and no git hook is installed: the checker is a manual
pre-push check, and this file runs manually as well.

Run:
    python -P scripts/tests/test_manifest_ancestry.py

Git isolation: each repository gets its own user.name, user.email,
commit.gpgsign=false, GIT_CONFIG_NOSYSTEM=1 and an empty throwaway
GIT_CONFIG_GLOBAL. Every Git invocation passes -c safe.directory=<repo> because
Windows temporary directories can otherwise trigger Git's "dubious ownership"
check. If Git is missing, or ownership still cannot be satisfied, the affected
tests skip with the reason printed.
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "scripts" / "check-manifest-ancestry.py"


def load_checker():
    """Load the hyphenated script by path; it is not an importable module name."""
    spec = importlib.util.spec_from_file_location(
        "check_manifest_ancestry_under_test", SCRIPT_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CHECKER = load_checker()


def skip(reason):
    """Print the reason, then raise unittest's skip signal."""
    print(f"SKIP: {reason}", file=sys.stderr)
    raise unittest.SkipTest(reason)


def ownership_error(text):
    lowered = (text or "").lower()
    return (
        "dubious ownership" in lowered
        or "safe.directory" in lowered
        or "not owned by current user" in lowered
    )


def run_git(repo, *args, env, check=True):
    """Run Git against repo with the test's safe.directory and environment."""
    repo = Path(repo).resolve()
    command = ["git", "-c", f"safe.directory={repo}", "-C", str(repo), *args]
    try:
        proc = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            timeout=60,
            shell=False,
        )
    except FileNotFoundError:
        skip("git executable not found")
    except (subprocess.TimeoutExpired, OSError) as exc:
        skip(f"git could not be run: {exc}")
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip()
        if ownership_error(detail):
            skip(f"git ownership restriction: {detail}")
        if check:
            raise AssertionError(
                f"git {' '.join(args)} failed ({proc.returncode}): {detail}"
            )
    return proc


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
        "GIT_AUTHOR_NAME": "Manifest Ancestry Test",
        "GIT_AUTHOR_EMAIL": "manifest-ancestry@example.invalid",
        "GIT_COMMITTER_NAME": "Manifest Ancestry Test",
        "GIT_COMMITTER_EMAIL": "manifest-ancestry@example.invalid",
    })
    return env


def make_repo(tmp, name="repo"):
    """Initialise a repository with a local identity and signing disabled."""
    repo = (Path(tmp) / name).resolve()
    repo.mkdir(parents=True)
    env = git_env(tmp)
    run_git(repo, "init", "-q", "-b", "main", env=env)
    run_git(repo, "config", "user.name", "Manifest Ancestry Test", env=env)
    run_git(
        repo, "config", "user.email",
        "manifest-ancestry@example.invalid", env=env,
    )
    run_git(repo, "config", "commit.gpgsign", "false", env=env)
    run_git(repo, "config", "core.autocrlf", "false", env=env)
    return repo, env


def rev_parse(repo, revision, env):
    return run_git(repo, "rev-parse", revision, env=env).stdout.strip()


def commit_file(repo, env, name, content, message):
    path = Path(repo) / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    run_git(repo, "add", "--all", env=env)
    run_git(repo, "commit", "-q", "-m", message, env=env)
    return rev_parse(repo, "HEAD", env)


def write_manifest(repo, revision, schema=None):
    manifest = Path(repo) / "tools" / "skills-manifest.json"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    if schema is None:
        schema = CHECKER.MANIFEST_SCHEMA
    payload = {
        "schema": schema,
        "source_revision": revision,
        "skills": [],
    }
    manifest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return manifest


def make_temp_root():
    """Create a unique writable directory under the system temp root.

    tempfile.mkdtemp creates its directory with mode 0o700. On some Windows
    sandboxed hosts that ACL denies creating children inside it, so this uses
    os.makedirs with the normal inherited permissions instead. The name stays
    unique for this process and test.
    """
    base = Path(tempfile.gettempdir())
    for index in range(1000):
        candidate = base / f"aegis-manifest-ancestry-{os.getpid()}-{index}"
        try:
            candidate.mkdir()
        except FileExistsError:
            continue
        return candidate.resolve()
    raise RuntimeError("could not create a unique temporary directory")


class ManifestAncestryTests(unittest.TestCase):
    def setUp(self):
        if shutil.which("git") is None:
            skip("git executable not found")
        self.tmp = make_temp_root()
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.repo, self.env = make_repo(self.tmp)

    def assert_status(self, result, expected):
        """Assert the status and the result shape; never assert the wording."""
        if (result.get("status") != expected
                and ownership_error(str(result.get("reason", "")))):
            skip(f"git ownership restriction: {result.get('reason')}")
        self.assertEqual(
            {"status", "source_revision", "head", "reason"},
            set(result),
        )
        self.assertEqual(expected, result.get("status"), result)

    def test_pass_when_revision_is_head(self):
        revision = commit_file(
            self.repo, self.env, "a.txt", "one\n", "first"
        )
        write_manifest(self.repo, revision)
        result = CHECKER.check_manifest_ancestry(self.repo)
        self.assert_status(result, "PASS")
        self.assertEqual(revision, result["source_revision"])
        self.assertEqual(revision, result["head"])

    def test_pass_when_revision_is_ancestor(self):
        first = commit_file(
            self.repo, self.env, "a.txt", "one\n", "first"
        )
        second = commit_file(
            self.repo, self.env, "b.txt", "two\n", "second"
        )
        self.assertNotEqual(first, second)
        write_manifest(self.repo, first)
        result = CHECKER.check_manifest_ancestry(self.repo)
        self.assert_status(result, "PASS")
        self.assertEqual(first, result["source_revision"])
        self.assertEqual(second, result["head"])

    def test_fail_when_revision_is_on_unmerged_side_branch(self):
        commit_file(self.repo, self.env, "base.txt", "base\n", "base")
        run_git(self.repo, "checkout", "-q", "-b", "side", env=self.env)
        side = commit_file(
            self.repo, self.env, "side.txt", "side\n", "side"
        )
        run_git(self.repo, "checkout", "-q", "main", env=self.env)
        tip = commit_file(
            self.repo, self.env, "main.txt", "main\n", "main"
        )
        self.assertNotEqual(side, tip)
        write_manifest(self.repo, side)
        result = CHECKER.check_manifest_ancestry(self.repo)
        self.assert_status(result, "FAIL")
        self.assertEqual(side, result["source_revision"])
        self.assertEqual(tip, result["head"])

    def test_fail_when_revision_is_not_a_commit(self):
        commit_file(self.repo, self.env, "a.txt", "one\n", "first")
        missing = "0123456789abcdef" * 2 + "01234567"
        self.assertEqual(40, len(missing))
        write_manifest(self.repo, missing)
        result = CHECKER.check_manifest_ancestry(self.repo)
        self.assert_status(result, "FAIL")
        self.assertEqual(missing, result["source_revision"])

    def test_error_when_manifest_is_missing(self):
        commit_file(self.repo, self.env, "a.txt", "one\n", "first")
        result = CHECKER.check_manifest_ancestry(self.repo)
        self.assert_status(result, "ERROR")
        self.assertIsNone(result["source_revision"])

    def test_error_when_manifest_is_invalid_json(self):
        manifest = self.repo / "tools" / "skills-manifest.json"
        manifest.parent.mkdir(parents=True)
        manifest.write_text("{not json", encoding="utf-8")
        result = CHECKER.check_manifest_ancestry(self.repo)
        self.assert_status(result, "ERROR")

    def test_error_when_schema_is_wrong(self):
        revision = commit_file(
            self.repo, self.env, "a.txt", "one\n", "first"
        )
        write_manifest(self.repo, revision, schema="aegis.skills-manifest/2")
        result = CHECKER.check_manifest_ancestry(self.repo)
        self.assert_status(result, "ERROR")

    def test_error_for_malformed_source_revision(self):
        revision = commit_file(
            self.repo, self.env, "a.txt", "one\n", "first"
        )
        variants = {
            "short": revision[:39],
            "uppercase": revision.upper(),
            "non-hex": "z" * 40,
            "all-zero": CHECKER.ZERO_REVISION,
            "not-a-string": 123,
        }
        for label, value in variants.items():
            with self.subTest(label=label):
                write_manifest(self.repo, value)
                result = CHECKER.check_manifest_ancestry(self.repo)
                self.assert_status(result, "ERROR")

    def test_error_for_absolute_or_parent_manifest_path(self):
        revision = commit_file(
            self.repo, self.env, "a.txt", "one\n", "first"
        )
        write_manifest(self.repo, revision)
        absolute = str(
            (self.repo / "tools" / "skills-manifest.json").resolve()
        )
        self.assert_status(
            CHECKER.check_manifest_ancestry(self.repo, manifest=absolute),
            "ERROR",
        )
        self.assert_status(
            CHECKER.check_manifest_ancestry(
                self.repo, manifest="../tools/skills-manifest.json"
            ),
            "ERROR",
        )

    def test_error_for_shallow_clone(self):
        # A shallow clone's on-disk marker is .git/shallow. Writing that marker
        # creates the same repository state without a clone transport, which can
        # invoke a shell that restricted test hosts deny. The assertion below
        # proves Git itself reports the repository as shallow.
        first = commit_file(self.repo, self.env, "a.txt", "one\n", "first")
        second = commit_file(self.repo, self.env, "b.txt", "two\n", "second")
        (self.repo / ".git" / "shallow").write_text(
            first + "\n", encoding="utf-8"
        )
        shallow = run_git(
            self.repo, "rev-parse", "--is-shallow-repository", env=self.env
        ).stdout.strip()
        self.assertEqual("true", shallow)
        write_manifest(self.repo, second)
        result = CHECKER.check_manifest_ancestry(self.repo)
        self.assert_status(result, "ERROR")
        self.assertEqual(second, result["source_revision"])

    def test_error_for_non_repository_root(self):
        plain = (self.tmp / "not-a-repository").resolve()
        plain.mkdir()
        write_manifest(plain, "a" * 40)
        result = CHECKER.check_manifest_ancestry(plain)
        self.assert_status(result, "ERROR")

    def _run_json_cli(self):
        env = dict(self.env)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [
                sys.executable,
                "-B",
                "-P",
                str(SCRIPT_PATH),
                "--repo-root",
                str(self.repo),
                "--json",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            timeout=60,
            shell=False,
        )

    def test_json_cli_exit_codes_match_status(self):
        commit_file(self.repo, self.env, "base.txt", "base\n", "base")
        run_git(self.repo, "checkout", "-q", "-b", "side", env=self.env)
        side = commit_file(
            self.repo, self.env, "side.txt", "side\n", "side"
        )
        run_git(self.repo, "checkout", "-q", "main", env=self.env)
        tip = commit_file(
            self.repo, self.env, "main.txt", "main\n", "main"
        )

        write_manifest(self.repo, tip)
        proc = self._run_json_cli()
        if proc.returncode != 0 and ownership_error(proc.stderr + proc.stdout):
            skip(f"git ownership restriction: {proc.stderr.strip()}")
        self.assertEqual(0, proc.returncode, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual("PASS", payload["status"])
        self.assertEqual(tip, payload["head"])

        write_manifest(self.repo, side)
        proc = self._run_json_cli()
        if proc.returncode != 1 and ownership_error(proc.stderr + proc.stdout):
            skip(f"git ownership restriction: {proc.stderr.strip()}")
        self.assertEqual(1, proc.returncode, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual("FAIL", payload["status"])
        self.assertEqual(side, payload["source_revision"])

        write_manifest(self.repo, "not-a-revision")
        proc = self._run_json_cli()
        self.assertEqual(2, proc.returncode, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual("ERROR", payload["status"])

    def test_cli_argument_usage_exits_two(self):
        env = dict(self.env)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        proc = subprocess.run(
            [sys.executable, "-B", "-P", str(SCRIPT_PATH), "--no-such-option"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            timeout=60,
            shell=False,
        )
        self.assertEqual(2, proc.returncode)


if __name__ == "__main__":
    unittest.main(verbosity=2)
