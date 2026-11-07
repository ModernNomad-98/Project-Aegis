#!/usr/bin/env python3
"""Self-tests for the conformance catalog checker.

The suite runs the checker as a subprocess against synthetic temporary repositories: a positive
clean catalog, the accepted negative/adversarial cases, determinism, read-only behaviour and the
optional evidence binding. It needs no network, no credentials and no third-party packages.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import uuid
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
TOOL_DIR = TESTS_DIR.parent
REAL_REPO = TESTS_DIR.parents[2]
TOOL = TOOL_DIR / "check_catalog.py"
CATALOG_REL = "docs/conformance/requirements.v1.json"


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def make_temp_root():
    candidates = [Path(tempfile.gettempdir()), TOOL_DIR, Path.cwd()]
    for base in candidates:
        try:
            root = Path(base) / ("conformance-tests-" + uuid.uuid4().hex[:12])
            probe = root / "probe"
            probe.mkdir(parents=True)
            probe.rmdir()
            return root
        except OSError:
            continue
    raise RuntimeError("no writable temporary root available for conformance tests")


def fixture_sources(catalog):
    paths = set()
    for source in catalog.get("sources", []):
        paths.add(source["path"])
    for record in catalog.get("requirements", []):
        for ref in (record.get("mechanism") or {}).get("refs", []):
            if isinstance(ref, dict) and isinstance(ref.get("path"), str):
                paths.add(ref["path"])
    return sorted(paths)


def build_fixture(root):
    real_catalog = json.loads((REAL_REPO / CATALOG_REL).read_text(encoding="utf-8"))
    for rel in fixture_sources(real_catalog):
        src = REAL_REPO / rel
        dst = root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.is_file():
            shutil.copyfile(src, dst)
        else:
            raise AssertionError("fixture source is not a file: " + rel)
    catalog_path = root / CATALOG_REL
    catalog_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(REAL_REPO / CATALOG_REL, catalog_path)
    return root


class ConformanceCheckerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = make_temp_root()
        cls.fixture = build_fixture(cls.tmp / "fixture")
        cls.outdir = cls.tmp / "out"
        cls.outdir.mkdir()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def run_checker(self, *extra, root=None, outdir=None):
        root = Path(root or self.fixture)
        outdir = Path(outdir or self.outdir)
        stdout_path = outdir / ("stdout-" + uuid.uuid4().hex[:8] + ".txt")
        stderr_path = outdir / ("stderr-" + uuid.uuid4().hex[:8] + ".txt")
        with open(stdout_path, "w", encoding="utf-8") as stdout_handle, \
                open(stderr_path, "w", encoding="utf-8") as stderr_handle:
            proc = subprocess.run(
                [sys.executable, "-P", "-B", str(TOOL), "--catalog", CATALOG_REL, *extra],
                cwd=str(root), stdout=stdout_handle, stderr=stderr_handle, timeout=120)
        return proc.returncode, stdout_path.read_text(encoding="utf-8"), stderr_path.read_text(encoding="utf-8")

    def catalog(self):
        return json.loads((self.fixture / CATALOG_REL).read_text(encoding="utf-8"))

    def write_catalog(self, catalog, root=None):
        root = Path(root or self.fixture)
        (root / CATALOG_REL).write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")

    def fresh_fixture(self, label):
        dest = self.tmp / ("fixture-" + label)
        shutil.copytree(self.fixture, dest)
        return dest

    # ---------------------------------------------------------------- positive cases
    def test_clean_fixture_is_clean_and_report_is_observation_free(self):
        code, out, err = self.run_checker()
        self.assertEqual(code, 0, out + err)
        self.assertIn("SUMMARY: requirements=23 findings=0", out)
        self.assertIn("COMPLETENESS: declared_min=23 declared_max=27 observed_requirements=23 "
                      "expected_families=6 expected_requirements=23 in_declared_range=YES", out)
        self.assertIn("Structural checks do not establish semantic correctness", out)
        self.assertNotIn("PASS", out)

    def test_json_report_is_deterministic(self):
        code1, out1, _ = self.run_checker("--json")
        code2, out2, _ = self.run_checker("--json")
        self.assertEqual(code1, 0)
        self.assertEqual(code2, 0)
        self.assertEqual(out1, out2)
        report = json.loads(out1)
        self.assertEqual(report["summary"]["findings"], 0)
        self.assertEqual(len(report["requirements"]), 23)
        completeness = report["completeness"]
        self.assertEqual(completeness["declared_min"], 23)
        self.assertEqual(completeness["declared_max"], 27)
        self.assertEqual(completeness["observed_requirements"], 23)
        self.assertEqual(completeness["expected_families"], 6)
        self.assertEqual(completeness["expected_requirements"], 23)
        self.assertTrue(completeness["in_declared_range"])
        self.assertEqual(completeness["first_profile"], "source-library-change")
        self.assertEqual(completeness["missing_seed_ids"], [])
        self.assertEqual(report["summary"]["observed_requirements"], 23)
        self.assertEqual(completeness["families"]["F2"], {"expected": 5, "present": 5})
        self.assertNotIn("PASS", out1)

    def test_checker_is_read_only(self):
        before = {}
        for path in self.fixture.rglob("*"):
            if path.is_file():
                before[str(path.relative_to(self.fixture))] = sha256_bytes(path.read_bytes())
        self.run_checker()
        after = {}
        for path in self.fixture.rglob("*"):
            if path.is_file():
                after[str(path.relative_to(self.fixture))] = sha256_bytes(path.read_bytes())
        self.assertEqual(before, after)

    def test_out_inside_repository_is_refused(self):
        target = self.fixture / "report.json"
        code, _out, err = self.run_checker("--out", str(target))
        self.assertEqual(code, 2)
        self.assertIn("outside the repository root", err)
        self.assertFalse(target.exists())

    def test_profile_filter_and_unknown_profile(self):
        code, out, _ = self.run_checker("--profile", "source-library-change", "--json")
        self.assertEqual(code, 0)
        report = json.loads(out)
        self.assertEqual(report["profile"]["profile_id"], "source-library-change")
        self.assertEqual(len(report["requirements"]), 23)
        code, _out, err = self.run_checker("--profile", "does-not-exist")
        self.assertEqual(code, 2)
        self.assertIn("not found", err)

    # ---------------------------------------------------------------- structural negatives
    def test_missing_first_profile_is_finding_not_crash(self):
        fixture = self.fresh_fixture("no-first-profile")
        catalog = json.loads((fixture / CATALOG_REL).read_text(encoding="utf-8"))
        catalog["profiles"][0]["profile_id"] = "other-profile"
        self.write_catalog(catalog, fixture)
        code, out, _ = self.run_checker("--json", root=fixture)
        self.assertEqual(code, 1, out)
        report = json.loads(out)
        self.assertTrue(any(item["code"] == "COMPLETENESS-GAP" for item in report["findings"]))

    def test_malformed_containers_are_findings_not_crash(self):
        for field in ("mechanism", "verification", "evidence_requirement"):
            fixture = self.fresh_fixture("bad-" + field)
            catalog = json.loads((fixture / CATALOG_REL).read_text(encoding="utf-8"))
            catalog["requirements"][0][field] = ["malformed"]
            self.write_catalog(catalog, fixture)
            code, out, _ = self.run_checker("--json", root=fixture)
            self.assertEqual(code, 1, field + ": " + out)
            report = json.loads(out)
            self.assertTrue(report["findings"], field)

    def test_duplicate_requirement_id(self):
        fixture = self.fresh_fixture("dup-id")
        catalog = json.loads((fixture / CATALOG_REL).read_text(encoding="utf-8"))
        catalog["requirements"].append(dict(catalog["requirements"][0]))
        self.write_catalog(catalog, fixture)
        code, out, _ = self.run_checker(root=fixture)
        self.assertEqual(code, 1)
        self.assertIn("DUP-ID", out)

    def test_bad_and_unsupported_versions(self):
        fixture = self.fresh_fixture("versions")
        catalog = json.loads((fixture / CATALOG_REL).read_text(encoding="utf-8"))
        catalog["catalog_version"] = "1.0"
        self.write_catalog(catalog, fixture)
        code, out, _ = self.run_checker(root=fixture)
        self.assertEqual(code, 1)
        self.assertIn("BAD-VERSION", out)

        catalog["catalog_version"] = "99.0.0"
        self.write_catalog(catalog, fixture)
        code, _out, err = self.run_checker(root=fixture)
        self.assertEqual(code, 2)
        self.assertIn("UNSUPPORTED-MAJOR", err)

    def test_missing_source_file(self):
        fixture = self.fresh_fixture("missing-source")
        (fixture / "docs/delivery-workflow.md").unlink()
        code, out, _ = self.run_checker(root=fixture)
        self.assertEqual(code, 1)
        self.assertIn("MISSING-SOURCE", out)

    def test_stale_source_digest(self):
        fixture = self.fresh_fixture("stale-source")
        path = fixture / "docs/delivery-workflow.md"
        path.write_text(path.read_text(encoding="utf-8") + "\nappended\n", encoding="utf-8")
        code, out, _ = self.run_checker(root=fixture)
        self.assertEqual(code, 1)
        self.assertIn("STALE-SOURCE", out)

    def test_missing_anchor(self):
        fixture = self.fresh_fixture("missing-anchor")
        catalog = json.loads((fixture / CATALOG_REL).read_text(encoding="utf-8"))
        catalog["requirements"][0]["source_ref"]["anchor"] = "This Heading Does Not Exist"
        self.write_catalog(catalog, fixture)
        code, out, _ = self.run_checker(root=fixture)
        self.assertEqual(code, 1)
        self.assertIn("MISSING-ANCHOR", out)

    def test_bad_inapplicability(self):
        fixture = self.fresh_fixture("inapplicability")
        catalog = json.loads((fixture / CATALOG_REL).read_text(encoding="utf-8"))
        catalog["requirements"][0]["applicability"] = {
            "profiles": [],
            "inapplicability": [{"profile_id": "unknown-profile", "reason_code": "made-up",
                                 "justification": "short"}],
        }
        self.write_catalog(catalog, fixture)
        code, out, _ = self.run_checker(root=fixture)
        self.assertEqual(code, 1)
        self.assertIn("BAD-INAPPLICABILITY", out)

    def test_observation_like_field_is_rejected(self):
        fixture = self.fresh_fixture("observation")
        catalog = json.loads((fixture / CATALOG_REL).read_text(encoding="utf-8"))
        catalog["requirements"][0]["status"] = "observed"
        self.write_catalog(catalog, fixture)
        code, out, _ = self.run_checker(root=fixture)
        self.assertEqual(code, 1)
        self.assertIn("OBSERVATION-FIELD", out)

    def test_unsafe_and_absolute_paths_are_rejected(self):
        fixture = self.fresh_fixture("unsafe-path")
        catalog = json.loads((fixture / CATALOG_REL).read_text(encoding="utf-8"))
        catalog["sources"][0]["path"] = "../../outside.txt"
        self.write_catalog(catalog, fixture)
        code, out, _ = self.run_checker(root=fixture)
        self.assertEqual(code, 1)
        self.assertIn("UNSAFE-PATH", out)

    def test_completeness_gap_when_a_family_is_incomplete(self):
        fixture = self.fresh_fixture("completeness")
        catalog = json.loads((fixture / CATALOG_REL).read_text(encoding="utf-8"))
        catalog["requirements"] = [r for r in catalog["requirements"]
                                   if r["requirement_id"] != "MG5"]
        for profile in catalog["profiles"]:
            profile["mandatory_requirement_ids"] = [
                rid for rid in profile["mandatory_requirement_ids"] if rid != "MG5"]
        self.write_catalog(catalog, fixture)
        code, out, _ = self.run_checker(root=fixture, *("--json",))
        self.assertEqual(code, 1)
        self.assertIn("COMPLETENESS-GAP", out)
        self.assertIn("F2", out)
        report = json.loads(out)
        completeness = report["completeness"]
        self.assertEqual(completeness["declared_min"], 23)
        self.assertEqual(completeness["declared_max"], 27)
        self.assertEqual(completeness["observed_requirements"], 22)
        self.assertFalse(completeness["in_declared_range"])
        self.assertIn("MG5", completeness["missing_seed_ids"])
        self.assertEqual(completeness["families"]["F2"], {"expected": 5, "present": 4})

    def test_oversize_catalog_fails_closed(self):
        fixture = self.fresh_fixture("oversize")
        catalog = json.loads((fixture / CATALOG_REL).read_text(encoding="utf-8"))
        catalog["requirements"][0]["notes"] = "x" * (600 * 1024)
        self.write_catalog(catalog, fixture)
        code, _out, err = self.run_checker(root=fixture)
        self.assertEqual(code, 2)
        self.assertIn("INPUT-TOO-LARGE", err)

    def test_malicious_data_is_data_only(self):
        fixture = self.fresh_fixture("malicious")
        canary = self.tmp / "canary.txt"
        canary.write_text("untouched", encoding="utf-8")
        catalog = json.loads((fixture / CATALOG_REL).read_text(encoding="utf-8"))
        payload = ("$(touch " + str(canary) + ") " + chr(96) + "rm -rf /" + chr(96)
                   + " __import__('os').system('x') ;\u202e;\x01")
        catalog["requirements"][0]["notes"] = payload
        self.write_catalog(catalog, fixture)
        code, out, _err = self.run_checker(root=fixture)
        self.assertEqual(code, 1)
        self.assertIn("SUSPICIOUS-DATA", out)
        self.assertEqual(canary.read_text(encoding="utf-8"), "untouched")

    # ---------------------------------------------------------------- schema/ref negatives
    def test_circular_supersession(self):
        fixture = self.fresh_fixture("circular")
        catalog = json.loads((fixture / CATALOG_REL).read_text(encoding="utf-8"))
        by_id = {r["requirement_id"]: r for r in catalog["requirements"]}
        by_id["SD-A"]["superseded_by"] = ["SD-B"]
        by_id["SD-B"]["superseded_by"] = ["SD-A"]
        self.write_catalog(catalog, fixture)
        code, out, _ = self.run_checker(root=fixture)
        self.assertEqual(code, 1)
        self.assertIn("CIRCULAR-DEPENDENCY", out)

    def test_unknown_reference(self):
        fixture = self.fresh_fixture("unknown-ref")
        catalog = json.loads((fixture / CATALOG_REL).read_text(encoding="utf-8"))
        catalog["requirements"][0]["related"] = ["AEGIS-REQ-NOPE-99"]
        self.write_catalog(catalog, fixture)
        code, out, _ = self.run_checker(root=fixture)
        self.assertEqual(code, 1)
        self.assertIn("UNKNOWN-REF", out)

    # ---------------------------------------------------------------- evidence binding cases
    def make_evidence(self, label, mutate=None):
        binding_dir = self.tmp / ("evidence-" + label)
        binding_dir.mkdir(exist_ok=True)
        payload = binding_dir / "payload.txt"
        payload.write_text("validator output line\n", encoding="utf-8")
        catalog_bytes = (self.fixture / CATALOG_REL).read_bytes()
        catalog = json.loads(catalog_bytes.decode("utf-8"))
        binding = {
            "schema": "aegis.evidence-binding/1",
            "catalog": {"path": CATALOG_REL, "bytes": len(catalog_bytes),
                        "sha256": sha256_bytes(catalog_bytes)},
            "source_revision": catalog["source_baseline"]["revision"],
            "records": [
                {"evidence_id": "E-01", "requirement_ids": ["SD-A"], "classification": "EXECUTED",
                 "stdout_path": "payload.txt", "stdout_bytes": payload.stat().st_size,
                 "stdout_sha256": sha256_bytes(payload.read_bytes())},
                {"evidence_id": "E-02", "requirement_ids": ["SD-B", "MG2"],
                 "classification": "PLANNED-UNRUN"},
            ],
        }
        if mutate:
            mutate(binding, binding_dir)
        path = binding_dir / "binding.json"
        path.write_text(json.dumps(binding, indent=2) + "\n", encoding="utf-8")
        return path

    def test_valid_evidence_binding_counts_present_and_unrun(self):
        path = self.make_evidence("valid")
        code, out, _ = self.run_checker("--evidence", str(path), "--json")
        self.assertEqual(code, 0, out)
        report = json.loads(out)
        statuses = {row["requirement_id"]: row["evidence_status"] for row in report["requirements"]}
        self.assertEqual(statuses["SD-A"], "EVIDENCE-PRESENT")
        self.assertEqual(statuses["SD-B"], "UNRUN-LISTED")
        self.assertEqual(statuses["MG2"], "UNRUN-LISTED")
        self.assertGreaterEqual(report["summary"]["unrun_listed"], 2)

    def test_stale_evidence_binding(self):
        def mutate(binding, _dir):
            binding["catalog"]["sha256"] = "0" * 64
        path = self.make_evidence("stale", mutate)
        code, out, _ = self.run_checker("--evidence", str(path), "--json")
        self.assertEqual(code, 1)
        self.assertIn("STALE-BINDING", out)
        report = json.loads(out)
        self.assertEqual(report["summary"]["evidence_present"], 0)

    def test_unknown_evidence_outcome(self):
        def mutate(binding, _dir):
            binding["records"][0]["classification"] = "MAYBE"
        path = self.make_evidence("outcome", mutate)
        code, out, _ = self.run_checker("--evidence", str(path), "--json")
        self.assertEqual(code, 1)
        self.assertIn("UNKNOWN-OUTCOME", out)

    def test_evidence_payload_digest_mismatch(self):
        def mutate(binding, directory):
            (directory / "payload.txt").write_text("changed after binding\n", encoding="utf-8")
        path = self.make_evidence("payload", mutate)
        code, out, _ = self.run_checker("--evidence", str(path), "--json")
        self.assertEqual(code, 1)
        self.assertIn("EVIDENCE-PAYLOAD", out)
        report = json.loads(out)
        statuses = {row["requirement_id"]: row["evidence_status"] for row in report["requirements"]}
        self.assertNotEqual(statuses["SD-A"], "EVIDENCE-PRESENT")

    def test_circular_binding_self_field(self):
        def mutate(binding, _dir):
            binding["binding_sha256"] = "0" * 64
        path = self.make_evidence("circular", mutate)
        code, out, _ = self.run_checker("--evidence", str(path), "--json")
        self.assertEqual(code, 1)
        self.assertIn("CIRCULAR-BINDING", out)

    # ---------------------------------------------------------------- static hygiene
    def test_static_hygiene_of_checker(self):
        source = TOOL.read_text(encoding="utf-8")
        allowed_imports = {"__future__", "argparse", "hashlib", "json", "os", "re", "sys",
                           "tempfile", "pathlib"}
        imported = set()
        for line in source.splitlines():
            import re as re_module
            match = re_module.match(r"^(?:from\s+([A-Za-z0-9_.]+)\s+import|import\s+([A-Za-z0-9_., ]+))", line)
            if match:
                name = match.group(1) or match.group(2)
                for part in name.split(","):
                    imported.add(part.strip().split(".")[0])
        self.assertTrue(imported <= allowed_imports,
                        "unexpected imports: %s" % (imported - allowed_imports))
        forbidden = ["import socket", "import urllib", "import http", "import subprocess",
                     "import ssl", "import ctypes", "os.system", "os.popen", "subprocess.",
                     "socket.", "urlopen", "eval(", "exec(", "uninstall", "prune", "cleanup"]
        for token in forbidden:
            self.assertNotIn(token, source, "forbidden token in checker source: %r" % token)


    def test_completeness_rejects_record_omitted_from_mandatory(self):
        spec = importlib.util.spec_from_file_location("check_catalog_under_test", TOOL)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        catalog = json.loads((REAL_REPO / CATALOG_REL).read_text(encoding="utf-8"))
        extra = json.loads(json.dumps(catalog["requirements"][0]))
        extra["requirement_id"] = "AEGIS-EXTRA-99"
        catalog["requirements"].append(extra)
        findings = []
        module.check_completeness(catalog, findings)
        self.assertTrue(any(item["code"] == "COMPLETENESS-GAP"
                            and "omitted" in item["evidence"] for item in findings))

    def test_schema_constants_match_checker_structural_validation(self):
        """A-1 drift test: no JSON-Schema engine runs; selected schema constants must match the
        standard-library structural-validation constants in the checker."""
        schema = json.loads((REAL_REPO / "docs/conformance/requirements.v1.schema.json")
                            .read_text(encoding="utf-8"))
        spec = importlib.util.spec_from_file_location("check_catalog_under_test", TOOL)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(schema["$id"], module.CATALOG_SCHEMA)
        self.assertEqual(schema["properties"]["schema"]["const"], module.CATALOG_SCHEMA)
        self.assertEqual(schema["properties"]["requirements"]["minItems"],
                         module.DECLARED_COUNT_MIN)
        self.assertEqual(schema["properties"]["requirements"]["maxItems"],
                         module.MAX_REQUIREMENTS)
        self.assertEqual(schema["properties"]["catalog_version"]["pattern"],
                         r"^[0-9]+\.[0-9]+\.[0-9]+$")
        requirement = schema["properties"]["requirements"]["items"]["properties"]
        self.assertEqual(set(requirement["mechanism"]["properties"]["kind"]["enum"]),
                         module.MECH_KINDS)
        self.assertEqual(set(requirement["verification"]["properties"]["method"]["enum"]),
                         module.VERIF_METHODS)
        self.assertEqual(set(requirement["evidence_requirement"]["properties"]["kind"]["enum"]),
                         module.EVID_KINDS)
        inapplicability = requirement["applicability"]["properties"]["inapplicability"]["items"]
        self.assertEqual(set(inapplicability["properties"]["reason_code"]["enum"]),
                         module.REASON_CODES)
        self.assertEqual(set(requirement["id_kind"]["enum"]), module.ID_KINDS)
        self.assertIs(schema["properties"]["profiles"]["items"]
                      ["properties"]["maintains_full_catalog"]["const"], True)
        self.assertEqual(schema["properties"]["source_baseline"]["properties"]["revision"]["pattern"],
                         module.GIT_SHA_RE.pattern)
        self.assertEqual(schema["properties"]["sources"]["items"]["properties"]["sha256"]["pattern"],
                         module.SHA256_RE.pattern)


if __name__ == "__main__":
    unittest.main()
