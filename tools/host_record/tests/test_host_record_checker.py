"""Stdlib synthetic-fixture self-tests for the host-record checker.

Contract (pinned by Stage C readiness A3, extended by delivery prep R-1 and the
Stage-F correction pass of 2026-11-08): 38 unittest items = 8
positive/structural + 30 negative/adversarial/refusal/deterministic-negative.
The harness copies the checker and fixture set into a temporary repository and
drives the checker as a black-box subprocess; that is harness behaviour only,
not a capability of the shipped checker (the checker itself spawns no process).
"""
import ast
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import unittest
import uuid
from pathlib import Path

VALID_ONE = "docs/host-record/fixtures/valid/host-record.synthetic-windows-11-python-314.json"
VALID_TWO = "docs/host-record/fixtures/valid/host-record.synthetic-unknown-gap.json"
INVALID_AGGREGATE = "docs/host-record/fixtures/invalid/host-record.aggregate-boolean.json"
INVALID_UNKNOWN = "docs/host-record/fixtures/invalid/host-record.unknown-field.json"
INVALID_DISPOSITION = "docs/host-record/fixtures/invalid/host-record.missing-disposition.json"
INVALID_UNSAFE = "docs/host-record/fixtures/invalid/host-record.unsafe-secret-field.json"
MANIFEST = "docs/host-record/fixtures/FIXTURE-MANIFEST.v1.json"
EXPECTED = "docs/host-record/fixtures/expected-findings.v1.json"
FORBIDDEN_REPORT_KEYS = {
    "pass",
    "qualified",
    "approved",
    "authorized",
    "authority",
    "status",
    "host_qualified",
    "consumer_qualified",
}


def sha256_path(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def tree_digest(root):
    items = []
    for path in sorted(Path(root).rglob("*")):
        if path.is_file():
            relative = path.relative_to(root).as_posix()
            items.append(relative + ":" + sha256_path(path))
    return hashlib.sha256("\n".join(items).encode("utf-8")).hexdigest()


def load_checker_module(path):
    spec = importlib.util.spec_from_file_location("check_host_record_under_test", str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_directory_link(target, link):
    """Create a directory link; return False when this host refuses one.

    Symlink creation needs a privilege on Windows, so the test falls back to a
    directory junction (mklink /J), which needs none; the caller skips with an
    explicit UNRUN note when both are unavailable.
    """
    try:
        Path(link).symlink_to(target, target_is_directory=True)
        return True
    except (OSError, NotImplementedError):
        pass
    if sys.platform.startswith("win"):
        completed = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link), str(target)],
            capture_output=True, text=True)
        return completed.returncode == 0 and Path(link).exists()
    return False


class HostRecordCheckerTests(unittest.TestCase):
    def setUp(self):
        self.real_repo = Path(__file__).resolve().parents[3]
        self.checker_source = self.real_repo / "tools" / "host_record" / "check_host_record.py"
        self.fixture_source = self.real_repo / "docs" / "host-record" / "fixtures"
        self.temp_dirs = []
        self.repo = self.make_repo()

    def tearDown(self):
        for path in self.temp_dirs:
            shutil.rmtree(path, ignore_errors=True)

    def make_repo(self):
        temp_root = Path(__file__).resolve().parents[4] / "_host-record-test-tmp"
        temp_root.mkdir(parents=True, exist_ok=True)
        temp = temp_root / ("repo-" + uuid.uuid4().hex[:12])
        temp.mkdir()
        self.temp_dirs.append(temp)
        repo = Path(temp)
        (repo / "tools" / "host_record").mkdir(parents=True)
        shutil.copyfile(self.checker_source, repo / "tools" / "host_record" / "check_host_record.py")
        shutil.copytree(self.fixture_source, repo / "docs" / "host-record" / "fixtures")
        return repo

    def run_checker(self, *args):
        command = [sys.executable, "-P", "-B", str(self.repo / "tools" / "host_record" / "check_host_record.py")] + list(args)
        return subprocess.run(command, cwd=str(self.repo), capture_output=True, text=True)

    def report(self, process):
        return json.loads(process.stdout)

    def codes(self, process):
        return [finding["code"] for finding in self.report(process)["findings"]]

    def load_fixture(self, relative):
        return json.loads((self.repo / relative).read_text(encoding="utf-8"))

    def write_fixture(self, relative, document):
        (self.repo / relative).write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")

    def make_valid_copy(self, relative):
        document = self.load_fixture(VALID_ONE)
        self.write_fixture(relative, document)
        return document

    # ---------------- positive / structural (7) ----------------
    def test_valid_fixture_one_clean(self):
        process = self.run_checker("--record", VALID_ONE, "--json")
        self.assertEqual(process.returncode, 0)
        report = self.report(process)
        self.assertEqual(report["findings"], [])
        self.assertEqual(report["checked_record"]["path"], VALID_ONE)

    def test_valid_fixture_two_clean(self):
        process = self.run_checker("--record", VALID_TWO, "--json")
        self.assertEqual(process.returncode, 0)
        self.assertEqual(self.report(process)["findings"], [])

    def test_deterministic_report_byte_identical(self):
        first = self.run_checker("--fixtures", "docs/host-record/fixtures", "--json")
        second = self.run_checker("--fixtures", "docs/host-record/fixtures", "--json")
        self.assertEqual(first.returncode, 0)
        self.assertEqual(second.returncode, 0)
        self.assertEqual(first.stdout, second.stdout)

    def test_read_only_fixture_tree_unchanged(self):
        before = tree_digest(self.repo)
        process = self.run_checker("--fixtures", "docs/host-record/fixtures", "--json")
        self.assertEqual(process.returncode, 0)
        self.assertEqual(before, tree_digest(self.repo))

    def test_static_stdlib_only_no_forbidden_imports(self):
        source = self.checker_source.read_text(encoding="utf-8")
        module = ast.parse(source)
        allowed = {"__future__", "argparse", "hashlib", "json", "re", "sys", "pathlib"}
        imported = set()
        for node in ast.walk(module):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        self.assertTrue(imported.issubset(allowed), imported - allowed)
        for token in ("subprocess", "urllib", "network", "os.system", "eval(", "exec("):
            self.assertNotIn(token, source)

    def test_report_has_no_authority_or_pass_fields(self):
        process = self.run_checker("--fixtures", "docs/host-record/fixtures", "--json")
        report = self.report(process)

        def walk(value):
            if isinstance(value, dict):
                for key, child in value.items():
                    self.assertNotIn(str(key).lower(), FORBIDDEN_REPORT_KEYS)
                    walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)
            elif isinstance(value, str):
                self.assertNotEqual(value.strip().upper(), "PASS")

        walk(report)
        self.assertNotIn("status", report)

    def test_manifest_dot_segments_canonicalised_clean(self):
        manifest = self.load_fixture(MANIFEST)
        for entry in manifest["entries"]:
            if entry["path"] == VALID_ONE:
                entry["path"] = "docs/host-record/fixtures/valid/./host-record.synthetic-windows-11-python-314.json"
        self.write_fixture(MANIFEST, manifest)
        process = self.run_checker("--fixtures", "docs/host-record/fixtures", "--json")
        self.assertEqual(process.returncode, 0, process.stdout)
        self.assertEqual(self.report(process)["findings"], [])

    def test_report_fields_sorted_deterministic_json(self):
        process = self.run_checker("--fixtures", "docs/host-record/fixtures", "--json")
        report = self.report(process)
        self.assertEqual(list(report.keys()), sorted(report.keys()))
        pairs = [(finding["code"], finding["path"], finding["evidence"]) for finding in report["findings"]]
        self.assertEqual(pairs, sorted(pairs))

    # ---------------- negatives / adversarial (19) ----------------
    def test_refused_out_inside_repository(self):
        out_path = self.repo / "docs" / "host-record" / "fixtures" / "report.json"
        process = self.run_checker("--fixtures", "docs/host-record/fixtures", "--json", "--out", str(out_path))
        self.assertEqual(process.returncode, 2)
        self.assertFalse(out_path.exists())

    def test_aggregate_boolean_rejected(self):
        process = self.run_checker("--record", INVALID_AGGREGATE, "--json")
        self.assertEqual(process.returncode, 1)
        self.assertEqual(self.codes(process), ["AGGREGATE-CAPABILITY"])

    def test_unknown_field_and_missing_binding_rejected(self):
        process = self.run_checker("--record", INVALID_UNKNOWN, "--json")
        self.assertEqual(process.returncode, 1)
        self.assertEqual(sorted(self.codes(process)), ["MISSING-FIELD", "UNKNOWN-FIELD"])

    def test_missing_disposition_rejected(self):
        process = self.run_checker("--record", INVALID_DISPOSITION, "--json")
        self.assertEqual(process.returncode, 1)
        self.assertEqual(self.codes(process), ["MISSING-DISPOSITION"])

    def test_verified_without_evidence_rejected(self):
        relative = "docs/host-record/fixtures/valid/mutated-verified.json"
        document = self.make_valid_copy(relative)
        document["capabilities"][0]["evidence_refs"] = []
        self.write_fixture(relative, document)
        process = self.run_checker("--record", relative, "--json")
        self.assertEqual(process.returncode, 1)
        self.assertIn("VERIFIED-WITHOUT-EVIDENCE", self.codes(process))

    def test_unknown_without_reason_rejected(self):
        relative = "docs/host-record/fixtures/valid/mutated-unknown.json"
        document = self.load_fixture(VALID_TWO)
        for capability in document["capabilities"]:
            if capability["disposition"] == "UNKNOWN":
                capability["reason"] = ""
                capability["remaining_action"] = ""
                break
        self.write_fixture(relative, document)
        process = self.run_checker("--record", relative, "--json")
        self.assertEqual(process.returncode, 1)
        self.assertIn("UNKNOWN-WITHOUT-REASON", self.codes(process))

    def test_duplicate_capability_rejected(self):
        relative = "docs/host-record/fixtures/valid/mutated-duplicate.json"
        document = self.make_valid_copy(relative)
        document["capabilities"].append(json.loads(json.dumps(document["capabilities"][0])))
        self.write_fixture(relative, document)
        process = self.run_checker("--record", relative, "--json")
        self.assertEqual(process.returncode, 1)
        self.assertIn("DUPLICATE-CAPABILITY", self.codes(process))

    def test_below_minimum_capability_and_source_counts_rejected(self):
        relative = "docs/host-record/fixtures/valid/mutated-too-few-capabilities.json"
        document = self.make_valid_copy(relative)
        document["capabilities"] = document["capabilities"][:3]
        self.write_fixture(relative, document)
        process = self.run_checker("--record", relative, "--json")
        self.assertEqual(process.returncode, 1)
        self.assertEqual(self.codes(process), ["CAPABILITY-COUNT"])
        empty = "docs/host-record/fixtures/valid/mutated-no-source-evidence.json"
        document = self.make_valid_copy(empty)
        document["source_evidence"] = []
        self.write_fixture(empty, document)
        empty_process = self.run_checker("--record", empty, "--json")
        self.assertEqual(empty_process.returncode, 1)
        self.assertEqual(self.codes(empty_process), ["SOURCE-EVIDENCE-EMPTY"])

    def test_secret_like_field_rejected(self):
        relative = "docs/host-record/fixtures/valid/mutated-secret.json"
        document = self.make_valid_copy(relative)
        document["api_key"] = "REDACTED-NOT-A-SECRET"
        self.write_fixture(relative, document)
        process = self.run_checker("--record", relative, "--json")
        self.assertEqual(process.returncode, 1)
        self.assertIn("SECRET-LIKE-FIELD", self.codes(process))

    def test_personal_data_field_rejected(self):
        relative = "docs/host-record/fixtures/valid/mutated-personal.json"
        document = self.make_valid_copy(relative)
        document["owner_email"] = "redacted-invalid-fixture"
        self.write_fixture(relative, document)
        process = self.run_checker("--record", relative, "--json")
        self.assertEqual(process.returncode, 1)
        self.assertIn("PERSONAL-DATA-FIELD", self.codes(process))

    def test_bad_config_digest_rejected(self):
        relative = "docs/host-record/fixtures/valid/mutated-digest.json"
        document = self.make_valid_copy(relative)
        document["config_digest"]["digest"] = "0" * 64
        self.write_fixture(relative, document)
        process = self.run_checker("--record", relative, "--json")
        self.assertEqual(process.returncode, 1)
        self.assertIn("BAD-CONFIG-DIGEST", self.codes(process))

    def test_bad_package_binding_rejected(self):
        relative = "docs/host-record/fixtures/valid/mutated-binding.json"
        document = self.make_valid_copy(relative)
        document["package_binding"]["package_manifest_sha256"] = "not-a-sha256"
        self.write_fixture(relative, document)
        process = self.run_checker("--record", relative, "--json")
        self.assertEqual(process.returncode, 1)
        self.assertIn("BAD-PACKAGE-BINDING", self.codes(process))

    def test_bad_record_id_rejected(self):
        relative = "docs/host-record/fixtures/valid/mutated-id.json"
        document = self.make_valid_copy(relative)
        document["record_id"] = "not a valid id"
        self.write_fixture(relative, document)
        process = self.run_checker("--record", relative, "--json")
        self.assertEqual(process.returncode, 1)
        self.assertIn("BAD-RECORD-ID", self.codes(process))

    def test_unsynthetic_real_claim_rejected(self):
        relative = "docs/host-record/fixtures/valid/mutated-real.json"
        document = self.make_valid_copy(relative)
        document["synthetic"] = False
        document["preparation_only"] = False
        self.write_fixture(relative, document)
        process = self.run_checker("--record", relative, "--json")
        self.assertEqual(process.returncode, 1)
        self.assertIn("UNSYNTHETIC-REAL-CLAIM", self.codes(process))

    def test_manifest_missing_fixture_rejected(self):
        (self.repo / VALID_TWO).unlink()
        process = self.run_checker("--fixtures", "docs/host-record/fixtures", "--json")
        self.assertEqual(process.returncode, 1)
        self.assertIn("MANIFEST-MISSING-FIXTURE", self.codes(process))

    def test_manifest_stale_version_rejected(self):
        manifest = self.load_fixture(MANIFEST)
        manifest["fixture_version"] = "v0"
        self.write_fixture(MANIFEST, manifest)
        process = self.run_checker("--fixtures", "docs/host-record/fixtures", "--json")
        self.assertEqual(process.returncode, 1)
        self.assertIn("MANIFEST-STALE", self.codes(process))

    def test_manifest_byte_mismatch_rejected(self):
        target = self.repo / VALID_ONE
        target.write_bytes(target.read_bytes() + b" ")
        process = self.run_checker("--fixtures", "docs/host-record/fixtures", "--json")
        self.assertEqual(process.returncode, 1)
        self.assertIn("MANIFEST-BYTE-MISMATCH", self.codes(process))

    def test_expected_findings_mismatch_rejected(self):
        expected = self.load_fixture(EXPECTED)
        expected["entries"][0]["expected_findings"] = ["SCHEMA"]
        self.write_fixture(EXPECTED, expected)
        process = self.run_checker("--fixtures", "docs/host-record/fixtures", "--json")
        self.assertEqual(process.returncode, 1)
        self.assertIn("EXPECTED-FINDINGS-MISMATCH", self.codes(process))

    def test_unsafe_path_rejected(self):
        relative = "docs/host-record/fixtures/valid/mutated-unsafe-path.json"
        document = self.make_valid_copy(relative)
        document["source_evidence"][0]["path"] = "../escape.json"
        self.write_fixture(relative, document)
        process = self.run_checker("--record", relative, "--json")
        self.assertEqual(process.returncode, 1)
        self.assertIn("UNSAFE-PATH", self.codes(process))

    def test_fail_closed_input_class(self):
        bad_json = self.repo / "docs" / "host-record" / "fixtures" / "valid" / "malformed.json"
        bad_json.write_text("{ this is not json", encoding="utf-8")
        malformed = self.run_checker("--record", "docs/host-record/fixtures/valid/malformed.json", "--json")
        self.assertEqual(malformed.returncode, 2)
        unknown = self.make_valid_copy("docs/host-record/fixtures/valid/unknown-schema.json")
        unknown["schema"] = "unknown.schema/1"
        self.write_fixture("docs/host-record/fixtures/valid/unknown-schema.json", unknown)
        unknown_schema = self.run_checker("--record", "docs/host-record/fixtures/valid/unknown-schema.json", "--json")
        self.assertEqual(unknown_schema.returncode, 2)
        oversize = self.repo / "docs" / "host-record" / "fixtures" / "valid" / "oversize.json"
        oversize.write_text(json.dumps({"padding": "x" * 70000}), encoding="utf-8")
        oversize_run = self.run_checker("--record", "docs/host-record/fixtures/valid/oversize.json", "--json")
        self.assertEqual(oversize_run.returncode, 2)

    # ---------------- Stage-F correction pass (2026-11-08) ----------------
    def test_required_container_types_rejected(self):
        mutations = {
            "host": "not-an-object",
            "config_digest": [],
            "package_binding": None,
            "source_evidence": {},
        }
        for name, value in mutations.items():
            relative = "docs/host-record/fixtures/valid/mutated-type-" + name + ".json"
            document = self.make_valid_copy(relative)
            document[name] = value
            self.write_fixture(relative, document)
            process = self.run_checker("--record", relative, "--json")
            self.assertEqual(process.returncode, 1, name)
            pairs = {(finding["code"], finding["path"]) for finding in self.report(process)["findings"]}
            self.assertIn(("SCHEMA", name), pairs, name)

    def test_self_citation_dot_segments_rejected(self):
        relative = "docs/host-record/fixtures/valid/mutated-selfcite.json"
        document = self.make_valid_copy(relative)
        document["source_evidence"][0]["path"] = "docs/host-record/fixtures/valid/./mutated-selfcite.json"
        self.write_fixture(relative, document)
        process = self.run_checker("--record", relative, "--json")
        self.assertEqual(process.returncode, 1)
        self.assertIn("UNSAFE-PATH", self.codes(process))

    def test_source_evidence_entry_rules_rejected(self):
        relative = "docs/host-record/fixtures/valid/mutated-source-evidence.json"
        document = self.make_valid_copy(relative)
        document["source_evidence"][0]["extra"] = "unknown-field"
        document["source_evidence"][0]["bytes"] = "6230"
        document["source_evidence"][0]["note"] = "x"
        self.write_fixture(relative, document)
        process = self.run_checker("--record", relative, "--json")
        self.assertEqual(process.returncode, 1)
        codes = self.codes(process)
        self.assertIn("UNKNOWN-FIELD", codes)
        self.assertIn("SCHEMA", codes)
        pairs = {(finding["code"], finding["path"]) for finding in self.report(process)["findings"]}
        self.assertIn(("SCHEMA", "source_evidence[0]/bytes"), pairs)
        self.assertIn(("SCHEMA", "source_evidence[0]/note"), pairs)

    def test_capability_and_list_rules_rejected(self):
        relative = "docs/host-record/fixtures/valid/mutated-list-rules.json"
        document = self.make_valid_copy(relative)
        document["capabilities"][0]["reason"] = "x"
        document["capabilities"][0]["evidence_refs"] = "docs/host-record/README.md"
        document["limits"][0] = 5
        document["non_claims"] = ["not host/consumer qualification", "not a portability claim"]
        self.write_fixture(relative, document)
        process = self.run_checker("--record", relative, "--json")
        self.assertEqual(process.returncode, 1)
        codes = self.codes(process)
        self.assertIn("SCHEMA", codes)
        pairs = {(finding["code"], finding["path"]) for finding in self.report(process)["findings"]}
        self.assertIn(("SCHEMA", "capabilities[0]/reason"), pairs)
        self.assertIn(("SCHEMA", "capabilities[0]/evidence_refs"), pairs)
        self.assertIn(("SCHEMA", "limits[0]"), pairs)
        self.assertIn(("SCHEMA", "non_claims"), pairs)

    def test_fixture_record_count_must_be_exactly_six(self):
        manifest = self.load_fixture(MANIFEST)
        entry = next(item for item in manifest["entries"] if item["kind"] == "record")
        for _ in range(58):
            manifest["entries"].append(json.loads(json.dumps(entry)))
        self.write_fixture(MANIFEST, manifest)
        process = self.run_checker("--fixtures", "docs/host-record/fixtures", "--json")
        self.assertEqual(process.returncode, 1)
        self.assertIn("MANIFEST-STALE", self.codes(process))

    def test_record_count_cap_refused(self):
        manifest = self.load_fixture(MANIFEST)
        entry = next(item for item in manifest["entries"] if item["kind"] == "record")
        for _ in range(59):
            manifest["entries"].append(json.loads(json.dumps(entry)))
        self.write_fixture(MANIFEST, manifest)
        process = self.run_checker("--fixtures", "docs/host-record/fixtures", "--json")
        self.assertEqual(process.returncode, 2)
        self.assertEqual(process.stdout, "")

    def test_string_cap_refused(self):
        relative = "docs/host-record/fixtures/valid/mutated-long-string.json"
        document = self.make_valid_copy(relative)
        document["capabilities"][0]["reason"] = "x" * 2001
        self.write_fixture(relative, document)
        process = self.run_checker("--record", relative, "--json")
        self.assertEqual(process.returncode, 2)
        self.assertEqual(process.stdout, "")

    def test_capability_cap_refused(self):
        relative = "docs/host-record/fixtures/valid/mutated-many-capabilities.json"
        document = self.make_valid_copy(relative)
        for _ in range(44):
            document["capabilities"].append(json.loads(json.dumps(document["capabilities"][0])))
        self.write_fixture(relative, document)
        process = self.run_checker("--record", relative, "--json")
        self.assertEqual(process.returncode, 2)
        self.assertEqual(process.stdout, "")

    def test_containment_helper_refuses_escapes(self):
        module = load_checker_module(self.checker_source)
        with self.assertRaises(module.UsageError):
            module.resolve_under_repo(self.repo, "../escape.json")
        with self.assertRaises(module.UsageError):
            module.resolve_under_repo(self.repo, "C:/Windows/win.ini")
        findings = []
        self.assertIsNone(module.resolve_manifest_entry(self.repo, "../outside.json", findings))
        self.assertEqual([finding["code"] for finding in findings], ["UNSAFE-PATH"])
        inside = module.resolve_manifest_entry(self.repo, "docs/host-record/fixtures/expected-findings.v1.json", [])
        self.assertIsNotNone(inside)
        self.assertTrue(str(inside).startswith(str(self.repo.resolve())))

    def test_manifest_entry_escape_link_rejected(self):
        outside = Path(self.repo).parent / ("outside-" + uuid.uuid4().hex[:10])
        outside.mkdir()
        self.temp_dirs.append(outside)
        outside_record = outside / "outside-record.json"
        shutil.copyfile(self.repo / VALID_TWO, outside_record)
        link = self.repo / "docs" / "host-record" / "fixtures" / "escape-link"
        if not make_directory_link(outside, link):
            self.skipTest("UNRUN: this host refused both a symlink and a directory junction")
        manifest = self.load_fixture(MANIFEST)
        manifest["entries"].append({
            "bytes": outside_record.stat().st_size,
            "expected_exit": 1,
            "kind": "record",
            "path": "docs/host-record/fixtures/escape-link/outside-record.json",
            "sha256": sha256_path(outside_record),
        })
        self.write_fixture(MANIFEST, manifest)
        process = self.run_checker("--fixtures", "docs/host-record/fixtures", "--json")
        self.assertEqual(process.returncode, 1, process.stdout + process.stderr)
        self.assertIn("UNSAFE-PATH", self.codes(process))


if __name__ == "__main__":
    unittest.main(verbosity=2)
