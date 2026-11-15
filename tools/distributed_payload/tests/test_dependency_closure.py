"""T-DEP acceptance tests for read-only dependency consumption (P0-GOV C1).

Covers plan section 10 cases 02/04/24 and the FS-R3 packaging feasibility rows
re-executed at the implementation head with the real governance payload. All
fixtures are synthetic temporary directories; the repository payload is only
read. Nothing here is an approval, a gate or a live-host claim.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import uuid
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.distributed_payload import manifest as m  # noqa: E402
from tools.distributed_payload import verify as v  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"
GOVERNANCE_FIXTURES = REPO_ROOT / "tools" / "aegis_preflight" / "tests" / "fixtures" / "governance"
GOVERNANCE_PAYLOAD = REPO_ROOT / "docs" / "governance" / "payload"
GOVERNANCE_SOURCE = REPO_ROOT / "docs" / "governance" / "governance-payload.source.json"
GOVERNANCE_DEPENDENCIES = REPO_ROOT / "docs" / "governance" / "governance-payload.dependencies.json"
GOVERNANCE_MANIFEST = REPO_ROOT / "docs" / "governance" / "governance-payload.manifest.json"


def make_temp_dir(prefix: str) -> str:
    base = Path(tempfile.gettempdir())
    for _ in range(20):
        candidate = base / (prefix + uuid.uuid4().hex)
        try:
            candidate.mkdir()
            return str(candidate)
        except FileExistsError:
            continue
    raise RuntimeError("could not create a unique temporary directory")


def run_cli(arguments, cwd=REPO_ROOT):
    return subprocess.run(
        [sys.executable, "-m", "tools.distributed_payload", *arguments],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        timeout=180,
    )


def write_small_payload(root: Path, names=("alpha.json", "beta.json", "gamma.json")) -> None:
    root.mkdir(parents=True, exist_ok=True)
    for index, name in enumerate(sorted(names)):
        (root / name).write_bytes(('{"synthetic": true, "index": %d}\n' % index).encode("utf-8"))


class DependencyClosureTests(unittest.TestCase):
    def setUp(self) -> None:
        self._temporary = make_temp_dir("dp-deps-")
        self.tmp = Path(self._temporary)
        self.addCleanup(shutil.rmtree, self._temporary, True)
        self.source = self.tmp / "source.json"
        self.source.write_text(
            json.dumps(
                {
                    "repository": "example/synthetic",
                    "commit": "a" * 40,
                    "tree": "b" * 40,
                }
            ),
            encoding="utf-8",
        )

    def build_payload(self, dependencies_file: Path, out: Path | None = None):
        payload = self.tmp / "payload"
        if not payload.exists():
            write_small_payload(payload)
        out = out or (self.tmp / "manifest.json")
        document = m.build_manifest(
            payload, "synthetic-package", "1.0.0", m.load_source_identity(self.source),
            dependencies=json.loads(Path(dependencies_file).read_text(encoding="utf-8")),
        )
        m.write_manifest_atomic(document, out)
        return payload, out, document

    # --- CASE 02 (S): packaging closure over the governance payload (T-DEP-04).
    def test_tdep04_governance_payload_closure(self) -> None:
        out = self.tmp / "governance-manifest.json"
        built = run_cli(
            [
                "build",
                "--root",
                str(GOVERNANCE_PAYLOAD),
                "--package-id",
                "aegis.required-governance",
                "--package-version",
                "1.0.0",
                "--source",
                str(GOVERNANCE_SOURCE),
                "--dependencies",
                str(GOVERNANCE_DEPENDENCIES),
                "--out",
                str(out),
            ]
        )
        self.assertEqual(built.returncode, 0, built.stderr)
        self.assertEqual(out.read_bytes(), GOVERNANCE_MANIFEST.read_bytes())
        verified = run_cli(["verify", "--manifest", str(out), "--target", str(GOVERNANCE_PAYLOAD), "--json"])
        self.assertEqual(verified.returncode, 0, verified.stdout + verified.stderr)
        report = json.loads(verified.stdout)
        self.assertEqual(report["summary"]["entries"], 6)
        self.assertEqual(report["summary"]["findings"], 0)
        dependency = run_cli(
            [
                "verify",
                "--manifest",
                str(GOVERNANCE_MANIFEST),
                "--target",
                str(GOVERNANCE_PAYLOAD),
                "--check-dependencies",
                "--json",
            ]
        )
        self.assertEqual(dependency.returncode, 0, dependency.stdout + dependency.stderr)
        dependency_report = json.loads(dependency.stdout)["dependencies"]
        self.assertEqual(dependency_report["edges"], 5)
        self.assertEqual(dependency_report["summary"]["findings"], 0)
        self.assertEqual(dependency_report["classes"]["required"], 5)
        self.assertEqual(dependency_report["mode"], "read-only")

    # --- CASE 04 (S): a standalone export missing a required governance edge is rejected.
    def test_tdep05_standalone_export_missing_dependency_rejected(self) -> None:
        payload = self.tmp / "export"
        write_small_payload(payload, names=("alpha.json",))
        out = self.tmp / "export-manifest.json"
        refused = run_cli(
            [
                "build",
                "--root",
                str(payload),
                "--package-id",
                "synthetic-export",
                "--package-version",
                "1.0.0",
                "--source",
                str(self.source),
                "--dependencies",
                str(GOVERNANCE_FIXTURES / "packaging" / "dependencies-missing-target.json"),
                "--out",
                str(out),
            ]
        )
        self.assertEqual(refused.returncode, 2, refused.stdout + refused.stderr)
        self.assertIn("dependency_target_missing", refused.stderr)
        self.assertFalse(out.exists(), "a refused build must not write a partial package")
        # C1 consumption: a required dependency target absent from the target tree is a finding.
        payload, manifest_path, _ = self.build_payload(GOVERNANCE_FIXTURES / "packaging" / "dependencies-required.json")
        target = self.tmp / "export-target"
        shutil.copytree(payload, target)
        (target / "beta.json").unlink()
        verified = run_cli(
            ["verify", "--manifest", str(manifest_path), "--target", str(target), "--check-dependencies", "--json"]
        )
        self.assertEqual(verified.returncode, 1, verified.stdout + verified.stderr)
        report = json.loads(verified.stdout)
        classes = {finding["class"] for finding in report["dependencies"]["findings"]}
        self.assertIn("DEPENDENCY_TARGET_ABSENT", classes)
        # C1 consumption: a maintainer-only edge naming a distributed entry is out of scope.
        scope_payload, scope_manifest, _ = self.build_payload(
            GOVERNANCE_FIXTURES / "packaging" / "dependencies-scope.json", out=self.tmp / "scope-manifest.json"
        )
        scope = run_cli(
            ["verify", "--manifest", str(scope_manifest), "--target", str(scope_payload),
             "--check-dependencies", "--json"]
        )
        self.assertEqual(scope.returncode, 1, scope.stdout + scope.stderr)
        scope_classes = {finding["class"] for finding in json.loads(scope.stdout)["dependencies"]["findings"]}
        self.assertIn("DEPENDENCY_SCOPE", scope_classes)

    # --- CASE 24 (S): cyclic/duplicate packaging graphs produce deterministic findings.
    def test_tdep06_packaging_graph_cycle_and_duplicate(self) -> None:
        for name, expected in (
            ("dependencies-cycle.json", "DEPENDENCY_CYCLE"),
            ("dependencies-duplicate.json", "DEPENDENCY_DUPLICATE"),
        ):
            with self.subTest(fixture=name):
                payload, manifest_path, _ = self.build_payload(GOVERNANCE_FIXTURES / "packaging" / name)
                first = run_cli(
                    ["verify", "--manifest", str(manifest_path), "--target", str(payload),
                     "--check-dependencies", "--json"]
                )
                second = run_cli(
                    ["verify", "--manifest", str(manifest_path), "--target", str(payload),
                     "--check-dependencies", "--json"]
                )
                self.assertEqual(first.returncode, 1, first.stdout + first.stderr)
                self.assertEqual(first.stdout, second.stdout, "the dependency report must be deterministic")
                classes = {finding["class"] for finding in json.loads(first.stdout)["dependencies"]["findings"]}
                self.assertIn(expected, classes)

    # --- FS-R3-02/03: unchanged build+determinism over the real payload.
    def test_fs_r3_build_determinism(self) -> None:
        out_a = self.tmp / "manifest.a.json"
        out_b = self.tmp / "manifest.b.json"
        for out in (out_a, out_b):
            completed = run_cli(
                [
                    "build",
                    "--root",
                    str(GOVERNANCE_PAYLOAD),
                    "--package-id",
                    "aegis.required-governance",
                    "--package-version",
                    "1.0.0",
                    "--source",
                    str(GOVERNANCE_SOURCE),
                    "--dependencies",
                    str(GOVERNANCE_DEPENDENCIES),
                    "--out",
                    str(out),
                ]
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(out_a.read_bytes(), out_b.read_bytes())
        self.assertEqual(out_a.read_bytes(), GOVERNANCE_MANIFEST.read_bytes())

    # --- FS-R3-04/05/08: verify, check-manifest and fail-on-change over the real payload.
    def test_fs_r3_verify_check_and_fail_on_change(self) -> None:
        identity = run_cli(["check-manifest", "--manifest", str(GOVERNANCE_MANIFEST)])
        self.assertEqual(identity.returncode, 0, identity.stderr)
        parsed = json.loads(identity.stdout)
        self.assertEqual(parsed["bytes"], len(GOVERNANCE_MANIFEST.read_bytes()))
        self.assertEqual(parsed["sha256"], m.sha256_raw(GOVERNANCE_MANIFEST.read_bytes()))
        target = self.tmp / "payload-copy"
        shutil.copytree(GOVERNANCE_PAYLOAD, target)
        clean_report, clean_exit = v.verify_target(GOVERNANCE_MANIFEST, target)
        self.assertEqual(clean_exit, 0)
        self.assertEqual(clean_report["summary"]["findings"], 0)
        changed = target / "required-governance-contract.v1.json"
        changed.write_bytes(changed.read_bytes() + b" ")
        dirty_report, dirty_exit = v.verify_target(GOVERNANCE_MANIFEST, target)
        self.assertEqual(dirty_exit, v.EXIT_FINDINGS)
        self.assertGreater(dirty_report["summary"]["changed"], 0)
        self.assertEqual(v.verify_target(GOVERNANCE_MANIFEST, target)[0]["summary"]["findings"], dirty_report["summary"]["findings"])
        # verify is read-only: the changed byte is reported, never repaired.
        self.assertTrue(changed.read_bytes().endswith(b" "))
        changed.write_bytes(changed.read_bytes()[:-1])
        restored_report, restored_exit = v.verify_target(GOVERNANCE_MANIFEST, target)
        self.assertEqual(restored_exit, 0)
        self.assertEqual(restored_report["summary"]["findings"], 0)

    # --- FS-R3-06/07: unchanged tool refusals (out inside root; missing dependency target).
    def test_fs_r3_refusals(self) -> None:
        payload = self.tmp / "payload"
        write_small_payload(payload)
        inside = payload / "bad-manifest.json"
        refused = run_cli(
            [
                "build",
                "--root",
                str(payload),
                "--package-id",
                "synthetic-package",
                "--package-version",
                "1.0.0",
                "--source",
                str(self.source),
                "--out",
                str(inside),
            ]
        )
        self.assertEqual(refused.returncode, 2)
        self.assertIn("out_inside_payload", refused.stderr)
        self.assertFalse(inside.exists())

    # --- T-DEP-06 duplicate-class detection is deterministic.
    def test_dependency_report_is_byte_deterministic(self) -> None:
        payload, manifest_path, _ = self.build_payload(GOVERNANCE_FIXTURES / "packaging" / "dependencies-duplicate.json")
        document, _ = v.load_manifest_document(manifest_path)
        first = v.dependency_report(document, payload)
        second = v.dependency_report(document, payload)
        self.assertEqual(json.dumps(first, sort_keys=True), json.dumps(second, sort_keys=True))
        self.assertGreater(first["summary"]["duplicates"], 0)


if __name__ == "__main__":
    unittest.main()
