"""Negative and interruption cases for the consumer install/verify/repair/upgrade lifecycle.

Companion to `docs/design/consumer-install-verify-repair-v1.md` (plan row P-11,
closure CL-15). Cases N-1..N-10 and I-1/I-2 below are the executable forms of
that page's section 8 and section 9; the page states which cases remain UNRUN.

What these tests establish:

* no lifecycle verb (install, repair, upgrade, uninstall, prune, cleanup,
  approve) exists, and asking for one writes nothing;
* the read-only verifier reports drift and never repairs it;
* a verify run is the only lifecycle operation implemented, and it leaves a
  skill-bearing target byte-identical on clean, findings, refused and
  interrupted runs;
* a report write that is interrupted leaves either no report or the previous
  complete report, never a partial one;
* every refused attempt leaves the skill file set and every skill byte
  unchanged.

Fixtures are synthetic and live under `tests/fixtures/lifecycle/` in a neutral
`skills/` layout; each test materialises them into `.claude/skills/` inside its
own temporary directory. Nothing is installed, no repository file is written,
and no consumer install record is produced.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.distributed_payload import manifest as m  # noqa: E402
from tools.distributed_payload import verify as v  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "lifecycle"
PACKAGE = FIXTURES / "package"
SOURCE = FIXTURES / "source.json"
DESIGN_PAGE = REPO_ROOT / "docs" / "design" / "consumer-install-verify-repair-v1.md"
LIFECYCLE_VERBS = ("install", "repair", "upgrade", "uninstall", "prune", "cleanup", "approve")


def make_temp_dir(prefix: str) -> str:
    """Create a unique temporary directory with os.mkdir.

    `tempfile.mkdtemp()` requests mode 0o700; this repository's Windows test host
    runs under a restricted-token sandbox whose ACL handling denies child writes
    inside such directories. `os.mkdir()` without an explicit mode is portable,
    equally unique with a UUID suffix, and works on normal and restricted hosts.
    """
    import uuid
    base = Path(tempfile.gettempdir())
    base.mkdir(parents=True, exist_ok=True)
    for _ in range(20):
        candidate = base / (prefix + uuid.uuid4().hex)
        try:
            candidate.mkdir()
            return str(candidate)
        except FileExistsError:
            continue
    raise RuntimeError("could not create a unique temporary directory")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_fingerprint(root: Path) -> dict:
    """Relative path -> raw SHA-256 for every file under root."""
    entries = {}
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames.sort()
        for filename in sorted(filenames):
            path = Path(dirpath) / filename
            entries[path.relative_to(root).as_posix()] = sha256_file(path)
    return entries


def directory_fingerprint(root: Path) -> list:
    """Sorted relative directory paths, so a created directory is visible."""
    directories = []
    for dirpath, dirnames, _ in os.walk(root, followlinks=False):
        dirnames.sort()
        for dirname in dirnames:
            directories.append((Path(dirpath) / dirname).relative_to(root).as_posix())
    return sorted(directories)


def run_cli(arguments, cwd=REPO_ROOT):
    return subprocess.run(
        [sys.executable, "-m", "tools.distributed_payload", *arguments],
        cwd=str(cwd), capture_output=True, text=True, timeout=180)


def materialize_consumer_target(destination: Path) -> Path:
    """Copy the neutral fixture package into a consumer-shaped temporary target.

    The fixture keeps skills under `skills/`; a consumer repository carries them
    under `.claude/skills/`. Relocating only inside the temporary directory keeps
    the repository free of a nested `.claude/skills/` tree, which the skill
    validator treats as a hard error.
    """
    shutil.copytree(PACKAGE, destination)
    claude = destination / ".claude"
    claude.mkdir()
    (destination / "skills").rename(claude / "skills")
    return destination


def build_fixture_manifest(root: Path, out_path: Path, version: str = "1.0.0") -> dict:
    document = m.build_manifest(root, "lifecycle-fixture", version, m.load_source_identity(SOURCE))
    m.write_manifest_atomic(document, out_path)
    return document


class LifecycleTestCase(unittest.TestCase):
    def setUp(self):
        self._tmp = make_temp_dir("dp-lifecycle-test-")
        self.tmp = Path(self._tmp)
        self.addCleanup(shutil.rmtree, self._tmp, True)
        self.target = materialize_consumer_target(self.tmp / "target")
        self.manifest = self.tmp / "manifest.json"
        self.document = build_fixture_manifest(self.target, self.manifest)
        self.out_dir = self.tmp / "out"
        self.out_dir.mkdir()
        self.skill_root = self.target / ".claude" / "skills"


class DesignContractTests(LifecycleTestCase):
    def test_n01_design_page_states_the_lifecycle_contract(self):
        self.assertTrue(DESIGN_PAGE.is_file(),
                        "design page docs/design/consumer-install-verify-repair-v1.md must exist")
        text = DESIGN_PAGE.read_text(encoding="utf-8")
        lowered = text.lower()
        for term in ("accepted paths", "refused paths", "preservation invariant", "pi-1",
                     "interruption cases", "unrun", "consumer install record",
                     "no install target", "no skill loss is possible by construction",
                     "repair", "upgrade", "absent", "cl-15", "exit 2"):
            with self.subTest(term=term):
                self.assertIn(term, lowered,
                              msg=f"design page is missing required term: {term}")
        for heading in ("## 5. Accepted paths", "## 6. Refused paths", "## 7. Preservation invariants",
                        "## 8. Negative cases (executable)", "## 9. Interruption cases",
                        "## 11. Explicit non-claims and UNRUN register"):
            with self.subTest(heading=heading):
                self.assertIn(heading, text)


class AbsentVerbTests(LifecycleTestCase):
    def test_n02_lifecycle_verbs_are_absent_and_refuse_without_writing(self):
        from tools.distributed_payload.__main__ import build_parser
        parser = build_parser()
        subparsers = [action for action in parser._actions
                      if action.__class__.__name__ == "_SubParsersAction"][0]
        self.assertEqual({"build", "verify", "check-manifest"}, set(subparsers.choices))

        before_files = tree_fingerprint(self.target)
        before_dirs = directory_fingerprint(self.target)
        for verb in LIFECYCLE_VERBS:
            with self.subTest(verb=verb):
                completed = run_cli([verb, "--target", str(self.target),
                                     "--root", str(self.target),
                                     "--manifest", str(self.manifest)])
                self.assertEqual(2, completed.returncode, completed.stderr)
                self.assertIn("invalid choice", completed.stderr)
        self.assertEqual(before_files, tree_fingerprint(self.target),
                         "a refused lifecycle verb must not change a skill byte")
        self.assertEqual(before_dirs, directory_fingerprint(self.target),
                         "a refused lifecycle verb must not create a directory")
        record = self.target / "docs" / "consumer-install-record.md"
        self.assertFalse(record.exists(), "no consumer install record may be produced by this slice")


class VerifyOnlyLifecycleTests(LifecycleTestCase):
    def test_n03_verify_accepts_a_clean_consumer_package_read_only(self):
        before = tree_fingerprint(self.target)
        report, exit_code = v.verify_target(self.manifest, self.target)
        self.assertEqual(v.EXIT_CLEAN, exit_code)
        self.assertEqual([], report["findings"])
        self.assertEqual("read-only", report["mode"])
        self.assertFalse(report["repair_available"])
        self.assertEqual(3, len(self.document["entries"]))
        self.assertEqual(len(self.document["entries"]), report["summary"]["entries"])
        self.assertEqual(len(self.document["entries"]), report["summary"]["ok"])
        self.assertEqual(before, tree_fingerprint(self.target))

    def test_n04_drifted_skill_tree_reports_and_never_repairs(self):
        missing = self.skill_root / "alpha" / "references" / "notes.md"
        drifted = self.skill_root / "beta" / "SKILL.md"
        foreign = self.skill_root / "alpha" / "notes.md"
        missing.unlink()
        drifted.write_bytes(drifted.read_bytes() + b"drift line\n")
        foreign.write_bytes(b"consumer content that must survive\n")
        drifted_bytes = drifted.read_bytes()
        before = tree_fingerprint(self.target)

        report, exit_code = v.verify_target(self.manifest, self.target)
        self.assertEqual(v.EXIT_FINDINGS, exit_code)
        observed = {(finding["class"], finding["path"]) for finding in report["findings"]}
        self.assertEqual({
            ("ABSENT", ".claude/skills/alpha/references/notes.md"),
            ("CHANGED", ".claude/skills/beta/SKILL.md"),
            ("UNRECOGNIZED", ".claude/skills/alpha/notes.md"),
        }, observed)
        self.assertFalse(missing.exists(), "a missing skill file must not be repaired")
        self.assertEqual(drifted_bytes, drifted.read_bytes(), "drifted bytes must not be rewritten")
        self.assertEqual(b"consumer content that must survive\n", foreign.read_bytes(),
                         "unrecognized content must be preserved")
        self.assertEqual(before, tree_fingerprint(self.target),
                         "a findings run must leave the target byte-identical")

    def test_n05_upgrade_candidate_is_absent_and_never_materialised(self):
        v2_root = materialize_consumer_target(self.tmp / "v2-package")
        gamma_dir = v2_root / ".claude" / "skills" / "gamma"
        gamma_dir.mkdir()
        (gamma_dir / "SKILL.md").write_bytes(
            b"---\nname: gamma-fixture\ndescription: Synthetic gamma fixture.\n---\n\n# gamma\n")
        v2_manifest = self.tmp / "manifest-v2.json"
        v2_document = build_fixture_manifest(v2_root, v2_manifest, version="2.0.0")
        self.assertEqual(4, len(v2_document["entries"]))

        before_files = tree_fingerprint(self.target)
        before_dirs = directory_fingerprint(self.target)
        report, exit_code = v.verify_target(v2_manifest, self.target)
        self.assertEqual(v.EXIT_FINDINGS, exit_code)
        self.assertEqual([("ABSENT", ".claude/skills/gamma/SKILL.md")],
                         [(finding["class"], finding["path"]) for finding in report["findings"]],
                         "an upgrade is reported as ABSENT, never performed by verify")
        self.assertFalse((self.skill_root / "gamma").exists(),
                         "verify must not create the upgrade target directory")
        self.assertEqual(before_files, tree_fingerprint(self.target))
        self.assertEqual(before_dirs, directory_fingerprint(self.target))


class RefusalTests(LifecycleTestCase):
    def test_n06_report_destination_in_skill_tree_is_refused(self):
        skill_file = self.skill_root / "alpha" / "SKILL.md"
        before_bytes = skill_file.read_bytes()
        before = tree_fingerprint(self.target)
        with self.assertRaises(m.ManifestError) as context:
            v.verify_target(self.manifest, self.target, report_out=skill_file)
        self.assertEqual("unsafe_report_path", context.exception.code)
        completed = run_cli(["verify", "--manifest", str(self.manifest),
                             "--target", str(self.target), "--report-out", str(skill_file)])
        self.assertEqual(2, completed.returncode, completed.stderr)
        self.assertIn("unsafe_report_path", completed.stderr)
        self.assertEqual(before_bytes, skill_file.read_bytes(),
                         "a refused report destination must not overwrite a skill file")
        self.assertEqual(before, tree_fingerprint(self.target))

    def test_n07_invalid_manifest_refuses_before_touching_skills(self):
        broken = self.tmp / "broken-manifest.json"
        broken.write_text("{not valid json", encoding="utf-8")
        report_path = self.out_dir / "never-written.json"
        before = tree_fingerprint(self.target)
        with self.assertRaises(m.ManifestError) as context:
            v.verify_target(broken, self.target, report_out=report_path)
        self.assertEqual("manifest_invalid_json", context.exception.code)
        completed = run_cli(["verify", "--manifest", str(broken), "--target", str(self.target),
                             "--report-out", str(report_path)])
        self.assertEqual(2, completed.returncode, completed.stderr)
        self.assertFalse(report_path.exists(), "no report may be written for an invalid manifest")
        self.assertEqual(before, tree_fingerprint(self.target))

    def test_n08_missing_target_is_refused_without_creating_it(self):
        absent = self.tmp / "absent-target"
        with self.assertRaises(m.ManifestError) as context:
            v.verify_target(self.manifest, absent)
        self.assertEqual("target_missing", context.exception.code)
        self.assertFalse(absent.exists(), "a refused verify must not create its target")
        self.assertEqual([], [name for name in os.listdir(self.tmp)
                              if name.startswith(".verify")])

    def test_n09_report_destination_edge_cases_are_refused(self):
        cases = {
            "directory": self.out_dir,
            "manifest": self.manifest,
            "missing-parent": self.tmp / "missing" / "report.json",
            "inside-skill-tree": self.skill_root / "alpha" / "report.json",
        }
        for name, destination in cases.items():
            with self.subTest(case=name):
                with self.assertRaises(m.ManifestError) as context:
                    v.verify_target(self.manifest, self.target, report_out=destination)
                self.assertEqual("unsafe_report_path", context.exception.code)
                if name != "directory" and name != "manifest":
                    self.assertFalse(destination.exists())
        self.assertTrue(self.manifest.is_file(), "the manifest input must still exist")
        self.assertEqual([], sorted(p.name for p in self.out_dir.iterdir()))


class InterruptionTests(LifecycleTestCase):
    def test_i01_interrupted_report_write_leaves_no_partial_record(self):
        report_path = self.out_dir / "interrupted.json"
        before = tree_fingerprint(self.target)
        with mock.patch.object(v.os, "fsync", side_effect=KeyboardInterrupt("simulated interruption")):
            with self.assertRaises(KeyboardInterrupt):
                v.verify_target(self.manifest, self.target, report_out=report_path)
        self.assertFalse(report_path.exists(), "an interrupted write must not leave a report")
        leftovers = [p.name for p in self.out_dir.iterdir() if p.name.startswith(".verify-report-")]
        self.assertEqual([], leftovers, "the report temp file must be removed")
        self.assertEqual(before, tree_fingerprint(self.target))

    def test_i02_interrupted_report_rename_preserves_previous_record(self):
        report_path = self.out_dir / "previous.json"
        previous = b'{"previous": true}\n'
        report_path.write_bytes(previous)
        before = tree_fingerprint(self.target)
        with mock.patch("pathlib.Path.replace", side_effect=OSError("simulated interruption")):
            with self.assertRaises(OSError):
                v.verify_target(self.manifest, self.target, report_out=report_path)
        self.assertEqual(previous, report_path.read_bytes(),
                         "the previous complete report must survive a failed rename")
        leftovers = [p.name for p in self.out_dir.iterdir() if p.name.startswith(".verify-report-")]
        self.assertEqual([], leftovers, "the report temp file must be removed")
        self.assertEqual(before, tree_fingerprint(self.target))


class ConstructionInvariantTests(LifecycleTestCase):
    def test_n10_refused_attempts_cannot_lose_a_skill(self):
        before_files = tree_fingerprint(self.target)
        before_dirs = directory_fingerprint(self.target)
        skill_files = {path: digest for path, digest in before_files.items()
                       if path.startswith(".claude/skills/")}
        self.assertEqual(3, len(skill_files))

        broken = self.tmp / "broken-manifest.json"
        broken.write_text("{not valid json", encoding="utf-8")
        for verb in LIFECYCLE_VERBS:
            with self.subTest(verb=verb):
                run_cli([verb, "--target", str(self.target), "--root", str(self.target)])
        with self.assertRaises(m.ManifestError):
            v.verify_target(broken, self.target)
        with self.assertRaises(m.ManifestError):
            v.verify_target(self.manifest, self.target,
                            report_out=self.skill_root / "alpha" / "SKILL.md")
        with self.assertRaises(m.ManifestError):
            v.verify_target(self.manifest, self.tmp / "absent-target")

        self.assertEqual(before_files, tree_fingerprint(self.target),
                         "no refused attempt may change a skill byte")
        self.assertEqual(before_dirs, directory_fingerprint(self.target),
                         "no refused attempt may create or remove a directory")
        for relative, digest in skill_files.items():
            path = self.target / relative
            self.assertTrue(path.is_file(), f"skill file lost by a refused attempt: {relative}")
            self.assertEqual(digest, sha256_file(path), f"skill byte changed: {relative}")


if __name__ == "__main__":
    unittest.main()
