"""Unit tests for the distributed-payload manifest contract (stdlib unittest).

Covers the accepted plan's first-slice rows WP02-A01..A05, A09, A10, A11, A12
and the WP02-I03 static surface row. These are synthetic tests: no network, no
installation, no repository suite execution, and every fixture lives in a
temporary directory created by the test.
"""
from __future__ import annotations

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
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.distributed_payload import manifest as m  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"
PAYLOAD = FIXTURES / "payload"
SOURCE = FIXTURES / "source.json"


def run_cli(arguments, cwd=REPO_ROOT):
    return subprocess.run(
        [sys.executable, "-m", "tools.distributed_payload", *arguments],
        cwd=str(cwd), capture_output=True, text=True, timeout=120)


def write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


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


class ManifestTestCase(unittest.TestCase):
    def setUp(self):
        self._tmp = make_temp_dir("dp-manifest-test-")
        self.tmp = Path(self._tmp)
        self.addCleanup(shutil.rmtree, self._tmp, True)

    def build_fixture_manifest(self, payload=None, label=None):
        source = m.load_source_identity(SOURCE)
        return m.build_manifest(Path(payload or PAYLOAD), "example-fixture", "1.0.0", source, label=label)


class BuildTests(ManifestTestCase):
    def test_a01_build_manifest_contract_and_determinism(self):
        document = self.build_fixture_manifest()
        self.assertEqual(m.SCHEMA, document["schema"])
        self.assertEqual("example-fixture", document["package"]["profile_id"])
        self.assertEqual("1.0.0", document["package"]["profile_version"])
        self.assertEqual("example/aegis-payload-fixture", document["source"]["repository"])
        self.assertEqual(m.HASH_CONTRACT, document["hash_contract"])
        self.assertEqual({"tool": "aegis-distributed-payload", "version": "1.0.0"},
                         document["generator"])
        paths = [entry["path"] for entry in document["entries"]]
        self.assertEqual(sorted(paths), paths)
        self.assertEqual(["README.txt", "assets/notes.txt", "skills/example/SKILL.md"], paths)
        for entry in document["entries"]:
            self.assertEqual("file", entry["type"])
            self.assertIn("sha256_raw", entry)
            self.assertIn("sha256_normalized", entry)
            self.assertGreaterEqual(entry["lf"], 0)
        self.assertNotIn("manifest_identity", document)
        first = m.serialize_manifest(document)
        second = m.serialize_manifest(self.build_fixture_manifest())
        self.assertEqual(first, second)
        self.assertTrue(first.endswith(b"\n"))
        self.assertNotIn(b"\r\n", first)

    def test_a02_build_twice_via_cli_is_byte_identical(self):
        first = self.tmp / "m1.json"
        second = self.tmp / "m2.json"
        for output in (first, second):
            completed = run_cli(["build", "--root", str(PAYLOAD), "--package-id", "example-fixture",
                                 "--package-version", "1.0.0", "--source", str(SOURCE),
                                 "--out", str(output)])
            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertTrue(output.is_file())
        self.assertEqual(first.read_bytes(), second.read_bytes())
        identity = m.manifest_identity(first)
        self.assertEqual(hashlib.sha256(first.read_bytes()).hexdigest(), identity["sha256"])
        leftovers = [path.name for path in self.tmp.iterdir() if path.name.startswith(".manifest-")]
        self.assertEqual([], leftovers)

    def test_a03_raw_versus_normalized_identity_with_crlf_fixture(self):
        crlf_root = self.tmp / "crlf-payload"
        lf_root = self.tmp / "lf-payload"
        crlf_bytes = b"alpha\r\nbeta\r\n"
        lf_bytes = b"alpha\nbeta\n"
        write_bytes(crlf_root / "text.txt", crlf_bytes)
        write_bytes(lf_root / "text.txt", lf_bytes)
        crlf_manifest = self.build_fixture_manifest(crlf_root)
        lf_manifest = self.build_fixture_manifest(lf_root)
        crlf_entry = crlf_manifest["entries"][0]
        lf_entry = lf_manifest["entries"][0]
        self.assertEqual(len(crlf_bytes), crlf_entry["bytes"])
        self.assertEqual(2, crlf_entry["lf"])
        self.assertEqual(hashlib.sha256(crlf_bytes).hexdigest(), crlf_entry["sha256_raw"])
        self.assertEqual(hashlib.sha256(lf_bytes).hexdigest(), crlf_entry["sha256_normalized"])
        self.assertNotEqual(crlf_entry["sha256_raw"], lf_entry["sha256_raw"])
        self.assertEqual(crlf_entry["sha256_normalized"], lf_entry["sha256_normalized"])
        self.assertNotEqual(crlf_entry["bytes"], lf_entry["bytes"])

    def test_a04_path_rules_reject_unsafe_paths(self):
        unsafe = ["", "../escape.txt", "a/../b.txt", "a/./b.txt", "/absolute.txt",
                  "C:/windows.txt", "//server/share.txt", "back\\slash.txt",
                  "double//slash.txt", "control\x01.txt", "nul\x00.txt"]
        for path in unsafe:
            with self.subTest(path=path), self.assertRaises(m.ManifestError):
                m.validate_payload_path(path)
        document = self.build_fixture_manifest()
        duplicate = json.loads(json.dumps(document))
        duplicate["entries"] = [dict(duplicate["entries"][0]), dict(duplicate["entries"][0])]
        with self.assertRaises(m.ManifestError) as context:
            m.validate_manifest(duplicate)
        self.assertEqual("duplicate_path", context.exception.code)
        folded = json.loads(json.dumps(document))
        folded_entry = dict(folded["entries"][1])
        folded_entry["path"] = folded_entry["path"].upper()
        folded["entries"] = [dict(folded["entries"][1]), folded_entry]
        with self.assertRaises(m.ManifestError) as context:
            m.validate_manifest(folded)
        self.assertEqual("duplicate_path", context.exception.code)

    def test_a04_build_rejects_symlinked_payload_file(self):
        payload = self.tmp / "symlink-payload"
        payload.mkdir()
        target = self.tmp / "target.txt"
        target.write_text("target\n", encoding="utf-8")
        link = payload / "link.txt"
        try:
            os.symlink(target, link)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"host limitation: symlink creation unavailable ({exc}) - UNRUN")
        with self.assertRaises(m.ManifestError) as context:
            self.build_fixture_manifest(payload)
        self.assertIn(context.exception.code, {"symlink_payload", "reparse_point"})

    def test_a05_schema_digest_and_self_reference_rejected(self):
        document = self.build_fixture_manifest()
        unsupported = json.loads(json.dumps(document))
        unsupported["schema"] = "aegis.distributed-payload-manifest/2"
        with self.assertRaises(m.ManifestError) as context:
            m.validate_manifest(unsupported)
        self.assertEqual("schema_unsupported", context.exception.code)
        uppercase = json.loads(json.dumps(document))
        uppercase["entries"][0]["sha256_raw"] = uppercase["entries"][0]["sha256_raw"].upper()
        with self.assertRaises(m.ManifestError) as context:
            m.validate_manifest(uppercase)
        self.assertEqual("entry_digest", context.exception.code)
        short = json.loads(json.dumps(document))
        short["entries"][0]["sha256_normalized"] = "abc123"
        with self.assertRaises(m.ManifestError) as context:
            m.validate_manifest(short)
        self.assertEqual("entry_digest", context.exception.code)
        self_reference = json.loads(json.dumps(document))
        self_reference["manifest_identity"] = {"sha256": "0" * 64}
        with self.assertRaises(m.ManifestError) as context:
            m.validate_manifest(self_reference)
        self.assertEqual("manifest_self_reference", context.exception.code)
        unknown = json.loads(json.dumps(document))
        unknown["unexpected"] = True
        with self.assertRaises(m.ManifestError) as context:
            m.validate_manifest(unknown)
        self.assertEqual("manifest_unknown_field", context.exception.code)

    def test_a03_dependency_classes_validated(self):
        document = self.build_fixture_manifest()
        entries = [entry["path"] for entry in document["entries"]]
        valid = json.loads(json.dumps(document))
        valid["dependencies"] = [
            {"from": entries[0], "to": entries[1], "class": "required"},
            {"from": entries[1], "to": entries[2], "class": "optional"},
            {"from": entries[0], "to": entries[2], "class": "conditional",
             "rule": "only when the example journey is installed"},
            {"from": entries[0], "to": "maintainer-only:release-tooling",
             "class": "maintainer-only"},
        ]
        m.validate_manifest(valid)
        no_rule = json.loads(json.dumps(valid))
        no_rule["dependencies"][2].pop("rule")
        with self.assertRaises(m.ManifestError) as context:
            m.validate_manifest(no_rule)
        self.assertEqual("dependency_missing_rule", context.exception.code)
        bad_class = json.loads(json.dumps(valid))
        bad_class["dependencies"][0]["class"] = "inferred"
        with self.assertRaises(m.ManifestError) as context:
            m.validate_manifest(bad_class)
        self.assertEqual("dependency_class", context.exception.code)
        missing_target = json.loads(json.dumps(valid))
        missing_target["dependencies"][0]["to"] = "assets/missing.txt"
        with self.assertRaises(m.ManifestError) as context:
            m.validate_manifest(missing_target)
        self.assertEqual("dependency_target_missing", context.exception.code)
        unexpected_rule = json.loads(json.dumps(valid))
        unexpected_rule["dependencies"][0]["rule"] = "not allowed here"
        with self.assertRaises(m.ManifestError) as context:
            m.validate_manifest(unexpected_rule)
        self.assertEqual("dependency_unexpected_rule", context.exception.code)

    def test_a11_package_identity_namespace(self):
        source = m.load_source_identity(SOURCE)
        document = self.build_fixture_manifest(label="Example Fixture Package")
        self.assertEqual("Example Fixture Package", document["package"]["label"])
        with self.assertRaises(m.ManifestError):
            m.build_manifest(PAYLOAD, "BadProfile", "1.0.0", source)
        with self.assertRaises(m.ManifestError):
            m.build_manifest(PAYLOAD, "example-fixture", "1 0", source)
        invalid_label = json.loads(json.dumps(document))
        invalid_label["package"]["label"] = ""
        with self.assertRaises(m.ManifestError):
            m.validate_manifest(invalid_label)
        self.assertNotIn("release", document["package"])

    def test_a12_source_identity_recorded_as_claim(self):
        document = self.build_fixture_manifest()
        self.assertEqual(40, len(document["source"]["commit"]))
        bad_source = {"repository": "example/aegis-payload-fixture",
                      "commit": "A" * 40,
                      "tree": "b" * 40}
        with self.assertRaises(m.ManifestError) as context:
            m.build_manifest(PAYLOAD, "example-fixture", "1.0.0", bad_source)
        self.assertEqual("source_commit", context.exception.code)
        unknown_source = {"repository": "example/aegis-payload-fixture",
                          "commit": "a" * 40, "tree": "b" * 40, "extra": 1}
        with self.assertRaises(m.ManifestError) as context:
            m.build_manifest(PAYLOAD, "example-fixture", "1.0.0", unknown_source)
        self.assertEqual("source_unknown_field", context.exception.code)

    def test_a09_cli_exposes_only_three_verbs(self):
        from tools.distributed_payload.__main__ import build_parser
        parser = build_parser()
        subparsers_action = [action for action in parser._actions
                             if action.__class__.__name__ == "_SubParsersAction"][0]
        self.assertEqual({"build", "verify", "check-manifest"}, set(subparsers_action.choices))
        for forbidden in ("install", "repair", "upgrade", "uninstall", "prune", "cleanup", "remove", "approve"):
            with self.subTest(verb=forbidden):
                completed = run_cli([forbidden])
                self.assertEqual(2, completed.returncode)
                self.assertIn("invalid choice", completed.stderr)
        self.assertEqual(2, run_cli([]).returncode)

    def test_i03_no_removal_or_repair_operation_in_code(self):
        import ast as _ast
        package_dir = Path(m.__file__).resolve().parent
        forbidden = re.compile(r"(uninstall|prune|garbage|cleanup)", re.IGNORECASE)
        offenders = []
        for path in sorted(package_dir.glob("*.py")):
            tree = _ast.parse(path.read_text(encoding="utf-8"))
            for node in _ast.walk(tree):
                if isinstance(node, (_ast.FunctionDef, _ast.AsyncFunctionDef, _ast.ClassDef)):
                    if forbidden.search(node.name):
                        offenders.append(f"{path.name}: def/class {node.name}")
                elif isinstance(node, _ast.arg):
                    if forbidden.search(node.arg):
                        offenders.append(f"{path.name}: arg {node.arg}")
                elif isinstance(node, _ast.Attribute) and forbidden.search(node.attr):
                    offenders.append(f"{path.name}: attribute {node.attr}")
        self.assertEqual([], offenders)
        verify_source = package_dir.joinpath("verify.py").read_text(encoding="utf-8")
        for token in ("os.remove", "os.unlink", "os.rename", "os.chmod", "os.replace",
                      "shutil", "rmtree"):
            self.assertNotIn(token, verify_source)
        main_source = package_dir.joinpath("__main__.py").read_text(encoding="utf-8")
        self.assertNotIn("subprocess", main_source)

    def test_a10_design_page_documents_contract(self):
        design = REPO_ROOT / "docs" / "design" / "distributed-payload-manifest-v1.md"
        self.assertTrue(design.is_file(), "design page must exist")
        text = design.read_text(encoding="utf-8")
        for term in ("aegis.distributed-payload-manifest/1", "hash_contract", "sha256_raw",
                     "sha256_normalized", "dependencies", "read-only", "detached binding",
                     "never", "Path rules", "Exit codes"):
            self.assertIn(term, text, msg=f"design page is missing required term: {term}")

    def test_a08_atomic_manifest_write_leaves_no_partial_artifact(self):
        document = self.build_fixture_manifest()
        output = self.tmp / "manifest.json"
        with mock.patch("tools.distributed_payload.manifest.os.replace",
                        side_effect=OSError("simulated interruption")):
            with self.assertRaises(OSError):
                m.write_manifest_atomic(document, output)
        self.assertFalse(output.exists())
        leftovers = [path.name for path in self.tmp.iterdir() if path.name.startswith(".manifest-")]
        self.assertEqual([], leftovers)
        m.write_manifest_atomic(document, output)
        self.assertTrue(output.is_file())
        self.assertFalse(output.read_bytes().startswith(b"\xef\xbb\xbf"))

    def test_build_refuses_output_inside_payload_and_missing_parent(self):
        inside = PAYLOAD / "manifest.json"
        try:
            completed = run_cli(["build", "--root", str(PAYLOAD), "--package-id", "example-fixture",
                                 "--package-version", "1.0.0", "--source", str(SOURCE),
                                 "--out", str(inside)])
            self.assertEqual(2, completed.returncode)
            self.assertFalse(inside.exists())
        finally:
            if inside.exists():
                inside.unlink()
        missing_parent = self.tmp / "missing" / "manifest.json"
        completed = run_cli(["build", "--root", str(PAYLOAD), "--package-id", "example-fixture",
                             "--package-version", "1.0.0", "--source", str(SOURCE),
                             "--out", str(missing_parent)])
        self.assertEqual(2, completed.returncode)


if __name__ == "__main__":
    unittest.main()