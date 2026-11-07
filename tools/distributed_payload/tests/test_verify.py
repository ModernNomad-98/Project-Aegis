"""Unit tests for the read-only distributed-payload verifier (stdlib unittest).

Covers the accepted plan's first-slice rows WP02-A06..A08 (read-only/atomic),
A13..A18, A20..A22 and the WP02-I04 no-mutation row. Synthetic fixtures only:
no network, no installation and no repository suite execution; every target and
manifest lives in a temporary directory created by the test.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.distributed_payload import manifest as m  # noqa: E402
from tools.distributed_payload import verify as v  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"
PAYLOAD = FIXTURES / "payload"
SOURCE = FIXTURES / "source.json"
ALLOWED_IMPORTS = {"__future__", "argparse", "hashlib", "json", "os", "pathlib", "re", "sys", "tempfile"}
FORBIDDEN_IMPORTS = {"socket", "urllib", "http", "requests", "ftplib", "smtplib", "ssl",
                     "asyncio", "ctypes", "subprocess"}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_fingerprint(root: Path) -> dict:
    entries = {}
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames.sort()
        for filename in sorted(filenames):
            path = Path(dirpath) / filename
            entries[path.relative_to(root).as_posix()] = sha256_file(path)
    return entries


def run_cli(arguments, cwd=REPO_ROOT):
    return subprocess.run(
        [sys.executable, "-m", "tools.distributed_payload", *arguments],
        cwd=str(cwd), capture_output=True, text=True, timeout=180)


def make_temp_dir(prefix: str) -> str:
    """Create a unique temporary directory with os.mkdir.

    tempfile.mkdtemp() requests mode 0o700; this repository's Windows test host
    runs under a restricted-token sandbox whose ACL handling denies child writes
    inside such directories. os.mkdir() without an explicit mode is portable,
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


class VerifyTestCase(unittest.TestCase):
    def setUp(self):
        self._tmp = make_temp_dir("dp-verify-test-")
        self.tmp = Path(self._tmp)
        self.addCleanup(shutil.rmtree, self._tmp, True)
        source = m.load_source_identity(SOURCE)
        self.manifest = self.tmp / "manifest.json"
        document = m.build_manifest(PAYLOAD, "example-fixture", "1.0.0", source)
        m.write_manifest_atomic(document, self.manifest)
        self.target = self.tmp / "target"
        shutil.copytree(PAYLOAD, self.target)
        self.out_dir = self.tmp / "out"
        self.out_dir.mkdir()

    def write_manifest_json(self, document, name="bad-manifest.json") -> Path:
        path = self.tmp / name
        path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return path


class ReadOnlyVerifyTests(VerifyTestCase):
    def test_a06_clean_verify_is_read_only(self):
        before = tree_fingerprint(self.target)
        report, exit_code = v.verify_target(self.manifest, self.target)
        self.assertEqual(v.EXIT_CLEAN, exit_code)
        self.assertEqual(0, len(report["findings"]))
        self.assertEqual(3, report["summary"]["ok"])
        self.assertEqual(3, report["summary"]["entries"])
        self.assertEqual("read-only", report["mode"])
        self.assertFalse(report["repair_available"])
        self.assertEqual(before, tree_fingerprint(self.target))

    def test_a13_missing_file_reported_absent_never_repaired(self):
        missing = self.target / "assets" / "notes.txt"
        missing.unlink()
        before = tree_fingerprint(self.target)
        report, exit_code = v.verify_target(self.manifest, self.target)
        self.assertEqual(v.EXIT_FINDINGS, exit_code)
        self.assertEqual([{"class": "ABSENT", "path": "assets/notes.txt"}], report["findings"])
        self.assertFalse(missing.exists(), "verifier must not repair a missing file")
        self.assertEqual(before, tree_fingerprint(self.target))

    def test_a14_changed_byte_same_length_diagnosed(self):
        path = self.target / "assets" / "notes.txt"
        original = path.read_bytes()
        path.write_bytes(b"X" * len(original))
        before = tree_fingerprint(self.target)
        report, exit_code = v.verify_target(self.manifest, self.target)
        self.assertEqual(v.EXIT_FINDINGS, exit_code)
        self.assertEqual(1, len(report["findings"]))
        finding = report["findings"][0]
        self.assertEqual("CHANGED", finding["class"])
        self.assertEqual("assets/notes.txt", finding["path"])
        self.assertIn("sha256_raw", finding["fields"])
        self.assertIn("sha256_normalized", finding["fields"])
        self.assertNotIn("bytes", finding["fields"])
        self.assertIn("expected", finding["fields"]["sha256_raw"])
        self.assertEqual(before, tree_fingerprint(self.target))

    def test_a03_crlf_target_reports_changed_raw_not_clean(self):
        payload = self.tmp / "lf-payload"
        target = self.tmp / "crlf-target"
        payload.mkdir()
        target.mkdir()
        (payload / "text.txt").write_bytes(b"alpha\nbeta\n")
        (target / "text.txt").write_bytes(b"alpha\r\nbeta\r\n")
        manifest_path = self.tmp / "lf-manifest.json"
        document = m.build_manifest(payload, "crlf-fixture", "1.0.0", m.load_source_identity(SOURCE))
        m.write_manifest_atomic(document, manifest_path)
        report, exit_code = v.verify_target(manifest_path, target)
        self.assertEqual(v.EXIT_FINDINGS, exit_code)
        finding = report["findings"][0]
        self.assertEqual("CHANGED", finding["class"])
        self.assertIn("bytes", finding["fields"])
        self.assertIn("sha256_raw", finding["fields"])
        self.assertNotIn("sha256_normalized", finding["fields"],
                         "normalized digests are equal for CRLF-vs-LF; the raw difference must still be CHANGED")

    def test_a15_unrecognized_content_preserved_never_uploaded(self):
        extra = self.target / "skills" / "extra.txt"
        extra.write_bytes(b"user content that must survive\n")
        before = tree_fingerprint(self.target)
        report, exit_code = v.verify_target(self.manifest, self.target)
        self.assertEqual(v.EXIT_FINDINGS, exit_code)
        classes = {finding["class"] for finding in report["findings"]}
        self.assertEqual({"UNRECOGNIZED"}, classes)
        self.assertEqual("skills/extra.txt", report["findings"][0]["path"])
        self.assertEqual(b"user content that must survive\n", extra.read_bytes())
        self.assertEqual(before, tree_fingerprint(self.target))

    def test_a16_foreign_content_outside_scope_ignored(self):
        foreign = self.target / "user-notes.txt"
        foreign.write_text("not ours\n", encoding="utf-8")
        report, exit_code = v.verify_target(self.manifest, self.target)
        self.assertEqual(v.EXIT_CLEAN, exit_code)
        self.assertEqual([], report["findings"])
        self.assertEqual("not ours\n", foreign.read_text(encoding="utf-8"))

    def test_a17_invalid_manifest_exit2_and_target_untouched(self):
        before = tree_fingerprint(self.target)
        broken = self.tmp / "broken.json"
        broken.write_text("{not valid json", encoding="utf-8")
        with self.assertRaises(m.ManifestError) as context:
            v.verify_target(broken, self.target)
        self.assertEqual("manifest_invalid_json", context.exception.code)
        completed = run_cli(["verify", "--manifest", str(broken), "--target", str(self.target)])
        self.assertEqual(2, completed.returncode)
        document = json.loads(self.manifest.read_text(encoding="utf-8"))
        document["schema"] = "aegis.distributed-payload-manifest/99"
        unsupported = self.write_manifest_json(document)
        completed = run_cli(["verify", "--manifest", str(unsupported), "--target", str(self.target)])
        self.assertEqual(2, completed.returncode)
        self.assertEqual(before, tree_fingerprint(self.target))

    def test_a18_unsafe_report_destinations_refused(self):
        inside = self.target / "assets" / "report.json"
        with self.assertRaises(m.ManifestError) as context:
            v.verify_target(self.manifest, self.target, report_out=inside)
        self.assertEqual("unsafe_report_path", context.exception.code)
        self.assertFalse(inside.exists())
        output_path = self.target / "assets" / "notes.txt"
        with self.assertRaises(m.ManifestError):
            v.verify_target(self.manifest, self.target, report_out=output_path)
        directory_destination = self.tmp / "a-directory"
        directory_destination.mkdir()
        with self.assertRaises(m.ManifestError):
            v.verify_target(self.manifest, self.target, report_out=directory_destination)
        missing_parent = self.tmp / "missing" / "report.json"
        with self.assertRaises(m.ManifestError):
            v.verify_target(self.manifest, self.target, report_out=missing_parent)
        self.assertFalse(missing_parent.exists())
        good = self.out_dir / "report.json"
        report, exit_code = v.verify_target(self.manifest, self.target, report_out=good)
        self.assertEqual(v.EXIT_CLEAN, exit_code)
        self.assertTrue(good.is_file())
        parsed = json.loads(good.read_text(encoding="utf-8"))
        self.assertEqual(report, parsed)

    def test_a19_symlinked_target_entry_host_limited(self):
        target_file = self.target / "assets" / "file.txt"
        outside = self.tmp / "outside.txt"
        outside.write_text("outside\n", encoding="utf-8")
        try:
            os.symlink(outside, target_file)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"host limitation: symlink creation unavailable ({exc}) - UNRUN")
        report, exit_code = v.verify_target(self.manifest, self.target)
        self.assertEqual(v.EXIT_FINDINGS, exit_code)
        finding = [item for item in report["findings"] if item["path"] == "assets/file.txt"][0]
        self.assertIn(finding["class"], {"UNRECOGNIZED", "CHANGED_TYPE"})
        self.assertTrue(target_file.is_symlink())
        self.assertEqual("outside\n", outside.read_text(encoding="utf-8"))

    def test_i04_no_mutation_for_clean_and_findings_runs(self):
        clean_before = tree_fingerprint(self.target)
        v.verify_target(self.manifest, self.target)
        self.assertEqual(clean_before, tree_fingerprint(self.target))
        (self.target / "assets" / "notes.txt").write_bytes(b"changed\n")
        (self.target / "skills" / "unexpected.txt").write_bytes(b"extra\n")
        findings_before = tree_fingerprint(self.target)
        report, exit_code = v.verify_target(self.manifest, self.target)
        self.assertEqual(v.EXIT_FINDINGS, exit_code)
        self.assertEqual(findings_before, tree_fingerprint(self.target))
        self.assertEqual([], [name for name in os.listdir(self.target)
                               if name.startswith(".verify") or name.endswith(".tmp")])

    def test_a22_no_authority_artifact_in_output(self):
        report, _ = v.verify_target(self.manifest, self.target)
        forbidden = ("approved", "qualified", "verdict", "accept")
        keys = set()

        def collect(node):
            if isinstance(node, dict):
                for key, value in node.items():
                    keys.add(key.lower())
                    collect(value)
            elif isinstance(node, list):
                for item in node:
                    collect(item)

        collect(report)
        for key in keys:
            for word in forbidden:
                self.assertNotIn(word, key, f"authority-like field in verify output: {key}")
        completed = run_cli(["verify", "--manifest", str(self.manifest),
                             "--target", str(self.target), "--json"])
        self.assertEqual(0, completed.returncode)
        parsed = json.loads(completed.stdout)
        self.assertNotIn("approved", completed.stdout.lower())
        self.assertNotIn("qualified", completed.stdout.lower())
        self.assertIn("source_note", parsed)
        self.assertIn("declared claim", parsed["source_note"])


class HygieneTests(VerifyTestCase):
    def test_a21_imports_are_stdlib_allowlist_only(self):
        package_dir = Path(m.__file__).resolve().parent
        offenders = []
        imported = set()
        for path in sorted(package_dir.glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imported.add(alias.name.split(".")[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.level:
                        continue  # package-relative import
                    if node.module:
                        imported.add(node.module.split(".")[0])
        offenders = sorted(imported & FORBIDDEN_IMPORTS)
        self.assertEqual([], offenders, f"forbidden imports found: {offenders}")
        self.assertEqual(set(), imported - ALLOWED_IMPORTS - {"tools"},
                         f"imports outside the stdlib allowlist: {sorted(imported - ALLOWED_IMPORTS)}")

    def test_a08_interrupted_verify_leaves_no_corruption(self):
        payload = self.tmp / "many-file-payload"
        payload.mkdir()
        for index in range(300):
            (payload / f"file-{index:03d}.txt").write_bytes(f"payload {index}\n".encode("utf-8"))
        manifest_path = self.tmp / "many-manifest.json"
        document = m.build_manifest(payload, "many-files", "1.0.0", m.load_source_identity(SOURCE))
        m.write_manifest_atomic(document, manifest_path)
        target = self.tmp / "many-target"
        shutil.copytree(payload, target)
        before = tree_fingerprint(target)
        report_path = self.out_dir / "interrupted-report.json"
        process = subprocess.Popen(
            [sys.executable, "-m", "tools.distributed_payload", "verify",
             "--manifest", str(manifest_path), "--target", str(target),
             "--report-out", str(report_path)],
            cwd=str(REPO_ROOT), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(0.05)
        if process.poll() is None:
            process.terminate()
        process.wait(timeout=30)
        self.assertEqual(before, tree_fingerprint(target),
                         "an interrupted verify must not mutate the target")
        if report_path.exists():
            json.loads(report_path.read_text(encoding="utf-8"))
        report, exit_code = v.verify_target(manifest_path, target, report_out=self.out_dir / "rerun.json")
        self.assertEqual(v.EXIT_CLEAN, exit_code)
        self.assertEqual(0, len(report["findings"]))
        first = (self.out_dir / "rerun.json").read_bytes()
        v.verify_target(manifest_path, target, report_out=self.out_dir / "rerun2.json")
        self.assertEqual(first, (self.out_dir / "rerun2.json").read_bytes())

    def test_deterministic_verify_reports(self):
        first = self.out_dir / "det-1.json"
        second = self.out_dir / "det-2.json"
        v.verify_target(self.manifest, self.target, report_out=first)
        v.verify_target(self.manifest, self.target, report_out=second)
        self.assertEqual(first.read_bytes(), second.read_bytes())
        report = json.loads(first.read_text(encoding="utf-8"))
        self.assertEqual(".", report["target"])
        self.assertNotIn(":\\", first.read_text(encoding="utf-8"))
        self.assertNotIn(REPO_ROOT.as_posix(), first.read_text(encoding="utf-8"))

    def test_a12b_optional_untrusted_notes_are_not_emitted(self):
        source = dict(m.load_source_identity(SOURCE))
        source["note"] = "C:\\Users\\host-owner\\payload\\notes.txt 2026-11-07T00:00:00Z"
        document = m.build_manifest(PAYLOAD, "example-fixture", "1.0.0", source,
                                    label="host label C:\\Users\\host-owner")
        m.write_manifest_atomic(document, self.manifest)
        report, exit_code = v.verify_target(self.manifest, self.target)
        self.assertEqual(v.EXIT_CLEAN, exit_code)
        serialized = json.dumps(report, sort_keys=True)
        self.assertNotIn("host-owner", serialized)
        self.assertNotIn("2026-11-07T00:00:00Z", serialized)
        self.assertEqual({"repository", "commit", "tree"}, set(report["source"]))
        identity = v.check_manifest(self.manifest)
        identity_serialized = json.dumps(identity, sort_keys=True)
        self.assertNotIn("host-owner", identity_serialized)
        self.assertEqual({"profile_id", "profile_version"}, set(identity["package"]))
        self.assertEqual({"repository", "commit", "tree"}, set(identity["source"]))


class CliExitCodeTests(VerifyTestCase):
    def test_exit_codes_and_check_manifest(self):
        clean = run_cli(["verify", "--manifest", str(self.manifest), "--target", str(self.target)])
        self.assertEqual(0, clean.returncode, clean.stderr)
        (self.target / "README.txt").write_bytes(b"changed\n")
        findings = run_cli(["verify", "--manifest", str(self.manifest), "--target", str(self.target)])
        self.assertEqual(1, findings.returncode, findings.stderr)
        missing_arguments = run_cli(["verify"])
        self.assertEqual(2, missing_arguments.returncode)
        identity = run_cli(["check-manifest", "--manifest", str(self.manifest)])
        self.assertEqual(0, identity.returncode, identity.stderr)
        parsed = json.loads(identity.stdout)
        self.assertEqual(sha256_file(self.manifest), parsed["sha256"])
        self.assertIn("not an approval", parsed["note"])
        document = json.loads(self.manifest.read_text(encoding="utf-8"))
        document["entries"][0]["sha256_raw"] = "A" * 64
        tampered = self.write_manifest_json(document, "tampered-manifest.json")
        tampered_result = run_cli(["check-manifest", "--manifest", str(tampered)])
        self.assertEqual(2, tampered_result.returncode)


if __name__ == "__main__":
    unittest.main()