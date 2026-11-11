"""Provenance tests: store binding kinds, no fabricated id, fail-closed (AC17).

The seed store is UNVERIFIED by design (AUTH-STORE / T24 does not exist).  A
binding is only VERIFIED when the cited authority record re-checks at gate
time; missing, edited or absent evidence downgrades to UNVERIFIED and blocks
readiness instead of being hashed as if it were verified.
"""

from __future__ import annotations

import json
import pathlib
import sys
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import _fixtures  # noqa: E402
from tools.aegis_verdict_gate import canonical, gate, records  # noqa: E402


def evaluate(paths):
    return gate.evaluate(
        repo_root=paths["root"],
        verdict_path=paths["verdict"],
        freeze_path=paths["freeze"],
        settlement_path=paths["settlement"],
        head_history_path=paths["head_history"],
        stage_records_dir=paths["stage_records_dir"],
        supported_auth_methods=(_fixtures.FIXTURE_AUTH_METHOD,),
    )


def patch_binding(paths, binding):
    manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
    manifest["provenance_binding"] = binding
    paths["manifest"].write_text(json.dumps(manifest, sort_keys=True, indent=2) + "\n", encoding="utf-8")


class SeedStoreProvenanceTest(unittest.TestCase):
    def test_seed_manifest_is_unverified_and_has_no_fabricated_id(self):
        manifest = json.loads(
            (REPO_ROOT / "docs/approvals/revision-state/manifest.json").read_text(encoding="utf-8")
        )
        binding = manifest["provenance_binding"]
        self.assertEqual(binding["authority_kind"], "UNKNOWN")
        self.assertEqual(binding["binding_status"], "UNVERIFIED")
        self.assertIsNone(binding["authority_ref_id"])
        self.assertIsNone(binding["authority_ref_sha256"])
        self.assertIn("AUTH-STORE", binding["unverified_reason"])

    def test_seed_store_displays_as_unverified_not_as_a_verified_count(self):
        store = records.load_store(REPO_ROOT)
        self.assertEqual(store.binding_status, "UNVERIFIED")
        self.assertEqual(store.issues, [])
        self.assertRegex(store.recomputed_store_digest, "^[0-9a-f]{64}$")

    def test_seed_manifest_accepts_only_the_three_authority_kinds(self):
        manifest = json.loads(
            (REPO_ROOT / "docs/approvals/revision-state/manifest.json").read_text(encoding="utf-8")
        )
        self.assertIn(manifest["provenance_binding"]["authority_kind"], records.AUTHORITY_KINDS)
        self.assertEqual(records.AUTHORITY_KINDS, ("REGISTER_ENTRY", "OWNER_LINE_RECORD", "UNKNOWN"))


class BindingRecheckTest(unittest.TestCase):
    def setUp(self):
        bundle = _fixtures.load_bundle("valid-verdict")
        self.result, self.paths = _fixtures.run_bundle(bundle, keep=True)
        self.register = self.paths["root"] / records.REGISTER_RELATIVE_PATH

    def tearDown(self):
        _fixtures.cleanup(self.paths["root"])

    def test_fixture_binding_is_verified_and_ready(self):
        self.assertTrue(self.result.readiness)
        manifest = json.loads(self.paths["manifest"].read_text(encoding="utf-8"))
        self.assertEqual(manifest["provenance_binding"]["binding_status"], "VERIFIED")

    def test_unverified_binding_blocks_readiness(self):
        patch_binding(
            self.paths,
            {
                "authority_kind": "UNKNOWN",
                "authority_ref_id": None,
                "authority_ref_sha256": None,
                "holder_role": "programme-lead",
                "holder_identity_ref": None,
                "binding_commit_or_pr": "fixture",
                "binding_status": "UNVERIFIED",
                "unverified_reason": "no owner-authorised authority record yet (AUTH-STORE)",
            },
        )
        result = evaluate(self.paths)
        self.assertFalse(result.readiness)
        self.assertEqual(result.reason_codes, ["REQUIRED_INPUT_UNAVAILABLE"])
        self.assertRegex(result.store_digest, "^[0-9a-f]{64}$")

    def test_edited_register_downgrades_a_claimed_verified_binding(self):
        self.register.write_text(self.register.read_text(encoding="utf-8") + "\n| LATE | ACTIVE | x |\n", encoding="utf-8")
        result = evaluate(self.paths)
        self.assertFalse(result.readiness)
        self.assertEqual(result.reason_codes, ["STATE_TAMPER_SUSPECTED"])
        self.assertIn("does not re-check", result.blockers[0].detail)

    def test_absent_authority_record_downgrades_a_claimed_verified_binding(self):
        self.register.unlink()
        result = evaluate(self.paths)
        self.assertFalse(result.readiness)
        self.assertEqual(result.reason_codes, ["STATE_TAMPER_SUSPECTED"])

    def test_owner_line_record_path_route_verifies(self):
        register_sha = canonical.sha256_hex(self.register.read_bytes())
        patch_binding(
            self.paths,
            {
                "authority_kind": "OWNER_LINE_RECORD",
                "authority_ref_id": records.REGISTER_RELATIVE_PATH,
                "authority_ref_sha256": register_sha,
                "holder_role": "programme-lead",
                "holder_identity_ref": None,
                "binding_commit_or_pr": "fixture",
                "binding_status": "VERIFIED",
                "unverified_reason": None,
            },
        )
        result = evaluate(self.paths)
        self.assertTrue(result.readiness)

    def test_unknown_authority_cannot_claim_verified(self):
        patch_binding(
            self.paths,
            {
                "authority_kind": "UNKNOWN",
                "authority_ref_id": None,
                "authority_ref_sha256": None,
                "holder_role": "programme-lead",
                "holder_identity_ref": None,
                "binding_commit_or_pr": "fixture",
                "binding_status": "VERIFIED",
                "unverified_reason": None,
            },
        )
        result = evaluate(self.paths)
        self.assertFalse(result.readiness)
        self.assertEqual(result.reason_codes, ["STATE_TAMPER_SUSPECTED"])

    def test_register_entry_absent_from_the_register_is_tamper(self):
        register_sha = canonical.sha256_hex(self.register.read_bytes())
        patch_binding(
            self.paths,
            {
                "authority_kind": "REGISTER_ENTRY",
                "authority_ref_id": "APR-DOES-NOT-EXIST-9999",
                "authority_ref_sha256": register_sha,
                "holder_role": "programme-lead",
                "holder_identity_ref": None,
                "binding_commit_or_pr": "fixture",
                "binding_status": "VERIFIED",
                "unverified_reason": None,
            },
        )
        result = evaluate(self.paths)
        self.assertFalse(result.readiness)
        self.assertEqual(result.reason_codes, ["STATE_TAMPER_SUSPECTED"])

    def test_volatile_manifest_field_is_tamper(self):
        manifest = json.loads(self.paths["manifest"].read_text(encoding="utf-8"))
        manifest["generated_at"] = "2026-11-10T20:00:00Z"
        self.paths["manifest"].write_text(json.dumps(manifest, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        result = evaluate(self.paths)
        self.assertFalse(result.readiness)
        self.assertEqual(result.reason_codes, ["STATE_TAMPER_SUSPECTED"])
        self.assertIn("volatile", result.blockers[0].detail)

    def test_store_digest_is_independent_of_the_binding(self):
        before = evaluate(self.paths).store_digest
        patch_binding(
            self.paths,
            {
                "authority_kind": "UNKNOWN",
                "authority_ref_id": None,
                "authority_ref_sha256": None,
                "holder_role": "programme-lead",
                "holder_identity_ref": None,
                "binding_commit_or_pr": "fixture",
                "binding_status": "UNVERIFIED",
                "unverified_reason": "AUTH-STORE pending",
            },
        )
        after = evaluate(self.paths)
        self.assertEqual(before, after.store_digest)


if __name__ == "__main__":
    unittest.main()
