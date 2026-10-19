#!/usr/bin/env python3
"""T1-T6 for the opt-in --blocks output of check_index.py (production item 4).

Coverage (plan AC1-AC6):
  T1  default output is byte-for-byte identical to the digest-pinned
      f110160a checker blob when --blocks is absent (human, --json, --quiet,
      --path; same ref/flags, stdout bytes and exit code compared).
  T2  blocks flatten back to the sorted remaining union; 0-based positions;
      ceil-quarter lanes; default size 8; final partial block; --block-size;
      --block-limit and blocks_total/blocks_emitted; empty-union helper edge.
  T3  page facts at --ref: blob, raw bytes, LF count and pin class
      (pinned-equal vs re-pin) at two refs, with totals summed from pages.
  T4  CLI --json schema/types, double-run byte-identical determinism, human
      header/rows/totals, and count consistency (union_size, blocks_total,
      blocks_emitted).
  T5  discovery contract: this module matches the test_*.py discovery pattern,
      all six T-methods exist, and the tests directory holds >= 50 methods
      (44 existing at the basis + the new ones).
  T6  hygiene/scope: exactly the two planned paths changed, no .github/README/
      index change, no new checker imports (AST allowlist equal to the pinned
      base blob), no network tokens, CLI input errors exit 2, and the suite
      writes no tracked data.

Runtime is bounded on purpose: full checker runs are expensive, so T1 compares
the human mode in full and the other three modes with --path; T4 uses
--block-limit 1. The pinned refs are historical commits available in the full
clone the readability suite already requires (CI uses fetch-depth: 0).

    python -B -m unittest discover -s tools/readability_acceptance/tests \
        -p "test_*.py" -v
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.readability_acceptance import check_index

ROOT = Path(__file__).resolve().parents[3]
CHECKER = ROOT / "tools" / "readability_acceptance" / "check_index.py"
TESTS_DIR = Path(__file__).resolve().parent

# The implementation base: the checker blob before this change. The blob sha1
# and the sha256 of its bytes are pinned so T1 cannot silently drift.
BASE_COMMIT = "f110160a12d54165ba99df60ac8e127f05283b8b"
BASE_CHECKER_BLOB = "041d681647473c91d6c2394b2fe05e789b08e651"
BASE_CHECKER_SHA256 = (
    "44c9f8cad3f7e80e7438d7c0c03a338be3e01f9a63b5ba5722fe338a96734a1d")

# A fixed historical ref: deterministic output and no dependence on today's
# origin/main. It is the item-1 merge commit (live main at plan time).
BASIS_REF = "61cacb2d5ace9aa91569351444a6da0b4cfcfc25"
# A page that exists in the tree and index at the basis; --path bounds runtime.
STABLE_PAGE = ".claude/skills/cloud-security-baseline-reviewer/SKILL.md"
PIN_DEFAULT = "2db1ffb7985ddc1c087c455740fd59e962967461"

PLANNED_PATHS = {
    "tools/readability_acceptance/check_index.py",
    "tools/readability_acceptance/tests/test_blocks.py",
}
ALLOWED_IMPORTS = {
    "__future__", "argparse", "json", "re", "subprocess", "sys", "pathlib",
    "build_index",
}


def _git(cwd, *args, binary=False):
    proc = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True)
    if proc.returncode != 0:
        raise AssertionError(
            "git " + " ".join(args) + " failed: "
            + proc.stderr.decode("utf-8", "replace")[:300])
    return proc.stdout if binary else proc.stdout.decode("utf-8", "replace")


def _run_checker(checker, argv):
    """Run one checker and return (returncode, stdout bytes, stderr bytes).

    PYTHONIOENCODING pins the child's stdout encoding so byte comparisons and
    human-output decoding are stable on every platform.
    """
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    proc = subprocess.run(
        [sys.executable, "-B", str(checker), "--repo", str(ROOT), *argv],
        cwd=str(ROOT), capture_output=True, env=env)
    return proc.returncode, proc.stdout, proc.stderr


def _materialize_base_checker(directory):
    """Extract the digest-verified pre-change checker beside build_index."""
    directory.mkdir(parents=True, exist_ok=True)
    blob = _git(ROOT, "cat-file", "blob", BASE_CHECKER_BLOB, binary=True)
    digest = hashlib.sha256(blob).hexdigest()
    if digest != BASE_CHECKER_SHA256:
        raise AssertionError(
            "base checker blob drifted: " + digest + " != " + BASE_CHECKER_SHA256)
    checker = directory / "check_index.py"
    checker.write_bytes(blob)
    shutil.copyfile(
        ROOT / "tools/readability_acceptance/build_index.py",
        directory / "build_index.py")
    return checker


def _write_fixture_repo(root):
    """A tiny git repo with one pin ref and one compared ref.

    Returns (pin_sha, ref_sha, union_paths). The union holds ten pages:
    docs/block-01.md and docs/block-02.md change at ref (re-pin), the other
    eight are identical at both refs (pinned-equal when --pin is pin_sha).
    docs/added-late.md exists only at ref (not in the union).
    """
    root.mkdir(parents=True, exist_ok=True)
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "blocks-test@example.com")
    _git(root, "config", "user.name", "blocks test")
    _git(root, "config", "core.autocrlf", "false")
    union = sorted("docs/block-{:02d}.md".format(index) for index in range(1, 11))
    for position, path in enumerate(union):
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(
            "# page {}\n\nfirst line\nsecond line\n".format(position)
            .encode("utf-8"))
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "pin")
    pin_sha = _git(root, "rev-parse", "HEAD").strip()
    for path in union[:2]:
        target = root / path
        target.write_bytes(target.read_bytes() + b"changed at ref\n")
    late = root / "docs/added-late.md"
    late.write_bytes(b"# late\n")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "ref")
    ref_sha = _git(root, "rev-parse", "HEAD").strip()
    return pin_sha, ref_sha, union


class T1DefaultOutputUnchanged(unittest.TestCase):
    """T1: --blocks absent => byte-identical to the pinned base checker."""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.base_checker = _materialize_base_checker(Path(cls._tmp.name))

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def _assert_identical(self, label, argv):
        base_code, base_out, base_err = _run_checker(self.base_checker, argv)
        new_code, new_out, new_err = _run_checker(CHECKER, argv)
        message = ("mode {}: returncode {} != {}\n--- base stderr ---\n{}"
                   "\n--- new stderr ---\n{}".format(
                       label, base_code, new_code,
                       base_err.decode("utf-8", "replace")[:800],
                       new_err.decode("utf-8", "replace")[:800]))
        self.assertEqual(base_code, new_code, message)
        self.assertEqual(base_out, new_out, message)
        self.assertEqual(base_err, new_err, message)

    def test_t1_default_output_matches_base_checker(self):
        self._assert_identical("human (full)", ["--ref", BASIS_REF])
        self._assert_identical(
            "json", ["--ref", BASIS_REF, "--json", "--path", STABLE_PAGE])
        self._assert_identical(
            "quiet", ["--ref", BASIS_REF, "--quiet", "--path", STABLE_PAGE])
        self._assert_identical(
            "path", ["--ref", BASIS_REF, "--path", STABLE_PAGE])

    def test_t1_base_blob_is_digest_pinned(self):
        blob = _git(ROOT, "cat-file", "blob", BASE_CHECKER_BLOB, binary=True)
        self.assertEqual(hashlib.sha256(blob).hexdigest(), BASE_CHECKER_SHA256)
        self.assertEqual(
            _git(ROOT, "rev-parse", BASE_COMMIT + ":"
                 "tools/readability_acceptance/check_index.py").strip(),
            BASE_CHECKER_BLOB)


class T2BlocksContract(unittest.TestCase):
    """T2: blocks partition the sorted union with positions/lanes/limits."""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.pin_sha, cls.ref_sha, cls.union = _write_fixture_repo(
            Path(cls._tmp.name) / "fixture")
        cls.payload = check_index.blocks_payload(
            Path(cls._tmp.name) / "fixture", cls.ref_sha, cls.pin_sha,
            cls.union, check_index.BLOCK_SIZE_DEFAULT, None)

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_t2_default_size_blocks(self):
        payload = self.payload
        self.assertEqual(payload["union_size"], 10)
        self.assertEqual(payload["block_size"], 8)
        self.assertIsNone(payload["block_limit"])
        self.assertEqual(payload["blocks_total"], 2)
        self.assertEqual(payload["blocks_emitted"], 2)
        first, second = payload["blocks"]
        self.assertEqual((first["start"], first["end"]), (0, 7))
        self.assertEqual((second["start"], second["end"]), (8, 9))
        self.assertFalse(first["partial"])
        self.assertTrue(second["partial"])
        self.assertEqual(first["index"], 0)
        self.assertEqual(second["index"], 1)

    def test_t2_flatten_is_the_sorted_union(self):
        pages = [page for block in self.payload["blocks"]
                 for page in block["pages"]]
        self.assertEqual([page["position"] for page in pages],
                         list(range(len(self.union))))
        self.assertEqual([page["path"] for page in pages], self.union)

    def test_t2_ceil_quarter_lanes(self):
        ceil, bounds = check_index.blocks_partition(10)
        self.assertEqual(ceil, 3)
        self.assertEqual(bounds, [(0, 2), (3, 5), (6, 8), (9, 9)])
        self.assertEqual(self.payload["blocks"][0]["lane"], "A")
        self.assertEqual(self.payload["blocks"][1]["lane"], "C")
        sized = check_index.blocks_payload(
            Path(self._tmp.name) / "fixture", self.ref_sha, self.pin_sha,
            self.union, 3, None)
        self.assertEqual([block["lane"] for block in sized["blocks"]],
                         ["A", "B", "C", "D"])
        self.assertEqual([block["start"] for block in sized["blocks"]],
                         [0, 3, 6, 9])
        self.assertTrue(sized["blocks"][-1]["partial"])
        self.assertEqual(sized["blocks_total"], 4)

    def test_t2_block_limit_and_totals(self):
        limited = check_index.blocks_payload(
            Path(self._tmp.name) / "fixture", self.ref_sha, self.pin_sha,
            self.union, 8, 1)
        self.assertEqual(limited["blocks_total"], 2)
        self.assertEqual(limited["blocks_emitted"], 1)
        self.assertEqual(len(limited["blocks"]), 1)
        over = check_index.blocks_payload(
            Path(self._tmp.name) / "fixture", self.ref_sha, self.pin_sha,
            self.union, 8, 99)
        self.assertEqual(over["blocks_emitted"], 2)
        first = self.payload["blocks"][0]
        self.assertEqual(first["totals"]["bytes"],
                         sum(page["bytes"] for page in first["pages"]))
        self.assertEqual(first["totals"]["lf"],
                         sum(page["lf"] for page in first["pages"]))
        self.assertEqual(first["totals"]["pinned_equal"]
                         + first["totals"]["repin"],
                         len(first["pages"]))

    def test_t2_empty_union_edge(self):
        self.assertEqual(check_index.blocks_partition(0),
                         (0, [(0, -1), (0, -1), (0, -1), (0, -1)]))
        payload = check_index.blocks_payload(
            Path(self._tmp.name) / "fixture", self.ref_sha, self.pin_sha,
            [], 8, None)
        self.assertEqual(payload["union_size"], 0)
        self.assertEqual(payload["blocks_total"], 0)
        self.assertEqual(payload["blocks_emitted"], 0)
        self.assertEqual(payload["blocks"], [])


class T3PageFacts(unittest.TestCase):
    """T3: blob/bytes/LF/pin class at --ref, at two refs."""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.fixture = Path(cls._tmp.name) / "fixture"
        cls.pin_sha, cls.ref_sha, cls.union = _write_fixture_repo(cls.fixture)

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_t3_page_facts_at_two_refs(self):
        unchanged = check_index.blocks_page_facts(
            self.fixture, self.ref_sha, self.pin_sha, "docs/block-03.md")
        expected = (self.fixture / "docs/block-03.md").read_bytes()
        self.assertEqual(unchanged["pin"], "pinned-equal")
        self.assertEqual(unchanged["bytes"], len(expected))
        self.assertEqual(unchanged["lf"], expected.count(b"\n"))
        self.assertEqual(
            unchanged["blob"],
            _git(self.fixture, "rev-parse",
                 self.ref_sha + ":docs/block-03.md").strip())
        changed = check_index.blocks_page_facts(
            self.fixture, self.ref_sha, self.pin_sha, "docs/block-01.md")
        self.assertEqual(changed["pin"], "re-pin")
        late = check_index.blocks_page_facts(
            self.fixture, self.ref_sha, self.pin_sha, "docs/added-late.md")
        self.assertEqual(late["pin"], "re-pin")
        at_pin = check_index.blocks_page_facts(
            self.fixture, self.pin_sha, self.pin_sha, "docs/block-03.md")
        self.assertEqual(at_pin["pin"], "pinned-equal")
        self.assertEqual(at_pin["blob"], unchanged["blob"])

    def test_t3_totals_sum_from_pages(self):
        payload = check_index.blocks_payload(
            self.fixture, self.ref_sha, self.pin_sha, self.union, 10, None)
        block = payload["blocks"][0]
        self.assertEqual(block["totals"]["bytes"],
                         sum(page["bytes"] for page in block["pages"]))
        self.assertEqual(block["totals"]["pinned_equal"], 8)
        self.assertEqual(block["totals"]["repin"], 2)


class T4CliJsonAndHuman(unittest.TestCase):
    """T4: JSON schema/types, double-run determinism, human rows/totals."""

    @classmethod
    def setUpClass(cls):
        cls.argv = ["--ref", BASIS_REF, "--blocks", "--block-limit", "1"]
        cls.code1, cls.out1, cls.err1 = _run_checker(
            CHECKER, cls.argv + ["--json"])
        cls.code2, cls.out2, cls.err2 = _run_checker(
            CHECKER, cls.argv + ["--json"])
        cls.human_code, cls.human_out, cls.human_err = _run_checker(
            CHECKER, cls.argv)

    def test_t4_json_schema_and_types(self):
        self.assertEqual(self.code1, 0, self.err1.decode("utf-8", "replace"))
        payload = json.loads(self.out1.decode("utf-8"))
        self.assertEqual(set(payload),
                         {"summary", "pending", "undecided", "small_drift",
                          "accepted", "withdrawn", "partial", "blocks"})
        blocks = payload["blocks"]
        self.assertEqual(
            set(blocks),
            {"block_size", "block_limit", "pin", "union_size",
             "blocks_total", "blocks_emitted", "blocks"})
        self.assertEqual(blocks["block_size"], 8)
        self.assertEqual(blocks["block_limit"], 1)
        self.assertEqual(blocks["pin"], PIN_DEFAULT)
        summary = payload["summary"]
        union_size = (summary["provably_pending"]
                      + summary["no_recorded_acceptance"])
        self.assertEqual(blocks["union_size"], union_size)
        self.assertEqual(blocks["blocks_total"], (union_size + 7) // 8)
        self.assertGreater(union_size, 8,
                           "T4 assumes a union larger than one 8-page block")
        self.assertEqual(blocks["blocks_emitted"], 1)
        self.assertEqual(len(blocks["blocks"]), 1)
        block = blocks["blocks"][0]
        self.assertEqual(
            set(block),
            {"index", "start", "end", "lane", "partial", "pages", "totals"})
        self.assertEqual(block["index"], 0)
        self.assertEqual(block["start"], 0)
        self.assertEqual(block["lane"], "A")
        self.assertEqual(len(block["pages"]), 8)
        self.assertEqual(block["partial"], len(block["pages"]) < 8)
        positions = [page["position"] for page in block["pages"]]
        self.assertEqual(positions, list(range(len(block["pages"]))))
        for page in block["pages"]:
            self.assertEqual(set(page),
                             {"position", "path", "blob", "bytes", "lf",
                              "pin"})
            self.assertRegex(page["blob"], r"^[0-9a-f]{40}$")
            self.assertIsInstance(page["bytes"], int)
            self.assertIsInstance(page["lf"], int)
            self.assertLessEqual(page["lf"], page["bytes"])
            self.assertIn(page["pin"], ("pinned-equal", "re-pin"))
        paths = [page["path"] for page in block["pages"]]
        self.assertEqual(paths, sorted(paths))
        self.assertEqual(block["totals"]["bytes"],
                         sum(page["bytes"] for page in block["pages"]))
        self.assertEqual(block["totals"]["lf"],
                         sum(page["lf"] for page in block["pages"]))

    def test_t4_json_determinism_double_run(self):
        self.assertEqual(self.code1, self.code2)
        self.assertEqual(self.out1, self.out2)
        self.assertEqual(self.err1, self.err2)

    def test_t4_human_blocks_output(self):
        self.assertEqual(self.human_code, 0,
                         self.human_err.decode("utf-8", "replace"))
        text = self.human_out.decode("utf-8")
        self.assertIn("BLOCKS — remaining pending union,", text)
        self.assertIn("block 0: positions 0-", text)
        self.assertIn("lane A", text)
        self.assertIn("pos  lane", text)
        self.assertIn("totals: bytes", text)
        self.assertIn("blocks total", text)
        payload = json.loads(self.out1.decode("utf-8"))
        summary_text = self.human_out.decode("utf-8").replace("\r\n", "\n")
        marker = summary_text.rfind('{\n  "compared_ref"')
        self.assertGreaterEqual(marker, 0)
        human_summary = json.loads(summary_text[marker:])
        self.assertEqual(human_summary["compared_ref"], BASIS_REF)
        self.assertEqual(human_summary["reader_pages_in_tree"],
                         payload["summary"]["reader_pages_in_tree"])


    def test_t4_quiet_still_prints_blocks(self):
        code, stdout, stderr = _run_checker(
            CHECKER, ["--ref", BASIS_REF, "--blocks", "--block-limit", "1",
                      "--quiet"])
        self.assertEqual(code, 0, stderr.decode("utf-8", "replace"))
        text = stdout.decode("utf-8")
        self.assertIn("BLOCKS — remaining pending union,", text)
        self.assertIn("block 0: positions 0-", text)
        self.assertIn("blocks total", text)
        self.assertNotIn("PROVABLY PENDING", text)


class T5DiscoveryContract(unittest.TestCase):
    """T5: the new module is discovered and the suite has >= 50 methods."""

    def test_t5_discovery_contract(self):
        module_names = sorted(
            path.name for path in TESTS_DIR.glob("test_*.py"))
        self.assertIn("test_blocks.py", module_names)
        self.assertTrue(Path(__file__).name.startswith("test_"))
        total = 0
        for path in TESTS_DIR.glob("test_*.py"):
            source = path.read_text(encoding="utf-8")
            total += len(re.findall(r"^    def test_", source, re.MULTILINE))
        self.assertGreaterEqual(total, 50)
        source = Path(__file__).read_text(encoding="utf-8")
        for name in ("test_t1_default_output_matches_base_checker",
                     "test_t2_flatten_is_the_sorted_union",
                     "test_t3_page_facts_at_two_refs",
                     "test_t4_json_schema_and_types",
                     "test_t5_discovery_contract",
                     "test_t6_scope_and_hygiene"):
            self.assertIn(name, source)


class T6ScopeAndHygiene(unittest.TestCase):
    """T6: scope, stdlib/no-network, exit-2 matrix, no tracked writes."""

    def _changed_paths(self):
        """The planned change set, from the merge-base to the WORKTREE.

        Reading the worktree (not only HEAD) keeps this check meaningful before
        the implementation commit exists locally, while a committed PR head
        yields the same two paths.
        """
        merge_base = _git(ROOT, "merge-base", "origin/main", "HEAD").strip()
        status = _git(ROOT, "diff", "--name-status", merge_base)
        entries = [line.split("\t") for line in status.splitlines() if line]
        untracked = _git(
            ROOT, "ls-files", "--others", "--exclude-standard").splitlines()
        for path in untracked:
            if path.startswith("tools/readability_acceptance/"):
                entries.append(["A", path])
        return entries

    def test_t6_only_the_two_planned_paths_changed(self):
        changes = self._changed_paths()
        if not changes:
            self.skipTest(
                "no base diff (e.g. running on main after merge); the exact-"
                "scope assertion applies to the implementing PR")
        paths = {entry[1] for entry in changes}
        self.assertEqual(paths, PLANNED_PATHS)
        statuses = {entry[1]: entry[0] for entry in changes}
        self.assertEqual(
            statuses["tools/readability_acceptance/tests/test_blocks.py"], "A")
        self.assertIn(
            statuses["tools/readability_acceptance/check_index.py"], ("M", "A"))
        for path in paths:
            self.assertFalse(path.startswith(".github/"), path)
            self.assertNotEqual(path, "tools/readability_acceptance/README.md")
            self.assertFalse(path.endswith("acceptance-index.json"), path)
            self.assertFalse(path.endswith("partial-dispositions.json"), path)

    def test_t6_no_new_imports_stdlib_only(self):
        tree = ast.parse(CHECKER.read_text(encoding="utf-8"))
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
        self.assertEqual(imports, ALLOWED_IMPORTS)
        base_tree = ast.parse(
            _git(ROOT, "cat-file", "blob", BASE_CHECKER_BLOB,
                 binary=True).decode("utf-8"))
        base_imports = set()
        for node in ast.walk(base_tree):
            if isinstance(node, ast.Import):
                base_imports.update(
                    alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                base_imports.add(node.module.split(".")[0])
        self.assertEqual(imports, base_imports)

    def test_t6_no_network_tokens(self):
        banned = ["sock" + "et", "ur" + "llib", "requ" + "ests",
                  "ht" + "tp"]
        for path in (CHECKER, Path(__file__)):
            source = path.read_text(encoding="utf-8")
            for token in banned:
                self.assertNotIn(token, source,
                                 path.name + " contains " + token)

    def test_t6_cli_input_errors_exit_2(self):
        cases = [
            ["--ref", BASIS_REF, "--blocks", "--path", STABLE_PAGE],
            ["--ref", BASIS_REF, "--blocks", "--block-size", "0"],
            ["--ref", BASIS_REF, "--blocks", "--block-limit", "0"],
            ["--ref", BASIS_REF, "--blocks", "--pin", "not-a-commit"],
            ["--ref", "not-a-ref", "--blocks"],
        ]
        for argv in cases:
            code, _stdout, _stderr = _run_checker(CHECKER, argv)
            self.assertEqual(code, 2, "argv {} returned {}".format(argv, code))

    def test_t6_suite_writes_no_tracked_data(self):
        status = _git(ROOT, "status", "--porcelain", "--",
                      "tools/readability_acceptance")
        allowed = {
            "tools/readability_acceptance/check_index.py",
            "tools/readability_acceptance/tests/test_blocks.py",
        }
        for line in status.splitlines():
            path = line[3:].strip()
            self.assertIn(path, allowed,
                          "unexpected worktree change: " + line)


if __name__ == "__main__":
    unittest.main()
