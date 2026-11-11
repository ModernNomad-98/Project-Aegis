"""Input tests: provenance, freeze, settlement, stage records, head history.

Covers AC9 and AC16: every required input is validated and re-derived, no
predicate term defaults to true, and an absent or unverifiable input fails
closed with REQUIRED_INPUT_UNAVAILABLE rather than passing.
"""

from __future__ import annotations

import json
import pathlib
import shutil
import sys
import tempfile
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.aegis_verdict_gate import canonical, inputs  # noqa: E402

HEAD = "a" * 40
TREE = "b" * 40
BASE = "c" * 40


def write_envelope(root, name, payload, *, status=None, tamper_hash=False, drop_provenance=False):
    provenance = {
        "source_ref": "fixture-%s" % name,
        "as_of": "2026-11-10T19:00:00Z",
        "producer_role": "fixture-holder",
        "producer_identity_ref": None,
        "declared_payload_sha256": canonical.digest(payload),
        "declared_payload_bytes": len(canonical.canonical_bytes(payload)),
    }
    if tamper_hash:
        provenance["declared_payload_sha256"] = "0" * 64
    if status:
        provenance["status"] = status
    document = {"payload": payload, "provenance": provenance}
    if drop_provenance:
        document = {"payload": payload}
    path = pathlib.Path(root) / name
    path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8", newline="\n")
    return path


def base_verdict():
    return {
        "repo": {"owner": "example-org", "name": "example-repo"},
        "change": {"type": "PR", "id": 42},
        "merge_target": {"ref": "refs/heads/main"},
        "candidate_id": "cand-fixture-0001",
        "head_sha": HEAD,
        "tree_sha": TREE,
        "base_sha": BASE,
        "policy_sha256": "d" * 64,
        "plan": {"sha256": "e" * 64},
        "evidence_inputs_sha256": "f" * 64,
    }


def base_freeze():
    verdict = base_verdict()
    return {
        "freeze_id": "frz-fixture-0001",
        "candidate_id": verdict["candidate_id"],
        "head_sha": HEAD,
        "tree_sha": TREE,
        "base_sha": BASE,
        "frozen_at": "2026-11-10T19:30:00Z",
        "immutable_inputs_sha256": canonical.digest(
            {
                "head": HEAD,
                "tree": TREE,
                "base": BASE,
                "policy_sha256": verdict["policy_sha256"],
                "plan_sha256": verdict["plan"]["sha256"],
                "evidence_inputs_sha256": verdict["evidence_inputs_sha256"],
            }
        ),
        "mutation_events": [],
        "settlement_ref": "set-fixture-0001",
    }


class EnvelopeTest(unittest.TestCase):
    def setUp(self):
        self.root = pathlib.Path(tempfile.mkdtemp(prefix="aegis-inputs-"))

    def tearDown(self):
        shutil.rmtree(str(self.root), ignore_errors=True)

    def test_valid_envelope_reports_file_identity(self):
        path = write_envelope(self.root, "freeze.json", base_freeze())
        envelope = inputs.load_envelope(path)
        self.assertEqual(envelope.file_sha256, canonical.sha256_hex(path.read_bytes()))
        self.assertEqual(envelope.file_bytes, path.stat().st_size)
        self.assertEqual(envelope.issues, [])

    def test_absent_input_is_a_gate_condition(self):
        with self.assertRaises(inputs.InputError) as caught:
            inputs.load_envelope(self.root / "absent.json")
        self.assertEqual(caught.exception.code, "REQUIRED_INPUT_UNAVAILABLE")
        self.assertFalse(caught.exception.fatal)

    def test_unparseable_input_is_fatal(self):
        path = self.root / "broken.json"
        path.write_text("{not json", encoding="utf-8")
        with self.assertRaises(inputs.InputError) as caught:
            inputs.load_envelope(path)
        self.assertTrue(caught.exception.fatal)
        self.assertEqual(caught.exception.code, "CANONICAL_FIELD_MISSING_OR_MISMATCH")

    def test_missing_provenance_is_required_input(self):
        path = write_envelope(self.root, "freeze.json", base_freeze(), drop_provenance=True)
        envelope = inputs.load_envelope(path)
        self.assertTrue(any(issue.code == "REQUIRED_INPUT_UNAVAILABLE" for issue in envelope.issues))

    def test_declared_hash_mismatch_is_canonical_mismatch(self):
        path = write_envelope(self.root, "freeze.json", base_freeze(), tamper_hash=True)
        envelope = inputs.load_envelope(path)
        self.assertTrue(any(issue.code == "CANONICAL_FIELD_MISSING_OR_MISMATCH" for issue in envelope.issues))


class FreezeDerivationTest(unittest.TestCase):
    def setUp(self):
        self.root = pathlib.Path(tempfile.mkdtemp(prefix="aegis-freeze-"))
        self.verdict = base_verdict()

    def tearDown(self):
        shutil.rmtree(str(self.root), ignore_errors=True)

    def derive(self, payload):
        path = write_envelope(self.root, "freeze.json", payload)
        return inputs.derive_freeze(inputs.load_envelope(path), self.verdict)

    def test_valid_freeze(self):
        result = self.derive(base_freeze())
        self.assertTrue(result.valid)
        self.assertEqual(result.issues, [])

    def test_head_mismatch_is_head_moved(self):
        freeze = base_freeze()
        freeze["head_sha"] = "9" * 40
        result = self.derive(freeze)
        self.assertFalse(result.valid)
        self.assertEqual(result.code, "HEAD_MOVED_OR_BASE_INVALIDATED")

    def test_mutation_events_are_head_moved(self):
        freeze = base_freeze()
        freeze["mutation_events"] = [{"event_id": "M-1", "at": "2026-11-10T19:40:00Z"}]
        result = self.derive(freeze)
        self.assertFalse(result.valid)
        self.assertEqual(result.code, "HEAD_MOVED_OR_BASE_INVALIDATED")

    def test_immutable_hash_mismatch_is_required_input(self):
        freeze = base_freeze()
        freeze["immutable_inputs_sha256"] = "0" * 64
        result = self.derive(freeze)
        self.assertFalse(result.valid)
        self.assertEqual(result.code, "REQUIRED_INPUT_UNAVAILABLE")

    def test_declared_false_freeze_is_never_valid(self):
        freeze = base_freeze()
        freeze["valid"] = False
        result = self.derive(freeze)
        self.assertFalse(result.valid)
        self.assertEqual(result.code, "REQUIRED_INPUT_UNAVAILABLE")


class SettlementDerivationTest(unittest.TestCase):
    def setUp(self):
        self.root = pathlib.Path(tempfile.mkdtemp(prefix="aegis-settlement-"))

    def tearDown(self):
        shutil.rmtree(str(self.root), ignore_errors=True)

    def payload(self, sources, settled):
        return {
            "settlement_id": "set-fixture-0001",
            "as_of": "2026-11-10T19:45:00Z",
            "pre_audit_checks": [{"check_id": "PA-1", "state": "pass", "evidence_ref": "EV-1"}],
            "review_sources": sources,
            "settled": settled,
        }

    def derive(self, payload, verdict=None, repo_root=None):
        path = write_envelope(self.root, "settlement.json", payload)
        return inputs.derive_settlement(inputs.load_envelope(path), verdict, repo_root)

    def authority_record(self, **overrides):
        document = {
            "schema_version": "aegis.disposition-authority/v1",
            "authority_id": "AUTH-DISP-0001",
            "status": "ACTIVE",
            "decision": "UNAVAILABLE_REVIEW",
            "holder_role": "owner",
            "holder_identity_ref": "owner",
            "scope": {
                "repo": "example-org/example-repo",
                "change_id": 42,
                "head_sha": HEAD,
                "merge_target_ref": "refs/heads/main",
            },
            "issued_at": "2026-11-10T19:00:00Z",
        }
        document.update(overrides)
        path = self.root / "authority" / "AUTH-DISP-0001.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8", newline="\n")
        return document, canonical.sha256_hex(path.read_bytes())

    def disposition_source(self, sha, head=HEAD):
        return {
            "source_id": "SR-1",
            "state": "UNAVAILABLE_DISPOSITIONED",
            "disposition_authority_ref": "authority/AUTH-DISP-0001.json",
            "disposition_authority_sha256": sha,
            "disposition_scope": {
                "repo": "example-org/example-repo",
                "change_id": 42,
                "head_sha": head,
                "merge_target_ref": "refs/heads/main",
            },
            "expires": None,
        }

    def test_settled(self):
        result = self.derive(self.payload([{"source_id": "SR-1", "state": "SETTLED"}], True))
        self.assertTrue(result.settled)
        self.assertEqual(result.issues, [])

    def test_pending_source_is_not_settled(self):
        result = self.derive(self.payload([{"source_id": "SR-1", "state": "PENDING"}], False))
        self.assertFalse(result.settled)
        self.assertTrue(any(issue.code == "MISSING_REQUIRED_REVIEW_OR_DISPOSITION" for issue in result.issues))

    def test_unavailable_disposition_requires_a_verified_authority(self):
        verdict = base_verdict()
        bare = self.derive(
            self.payload([{"source_id": "SR-1", "state": "UNAVAILABLE_DISPOSITIONED"}], False),
            verdict,
            self.root,
        )
        self.assertFalse(bare.settled)
        # Arbitrary strings are not an authority: a truthy ref plus a prose
        # scope used to be accepted; it is now blocked.
        arbitrary = self.derive(
            self.payload(
                [
                    {
                        "source_id": "SR-1",
                        "state": "UNAVAILABLE_DISPOSITIONED",
                        "disposition_authority_ref": "AUTH-1",
                        "disposition_scope": "this change",
                    }
                ],
                True,
            ),
            verdict,
            self.root,
        )
        self.assertFalse(arbitrary.settled)
        self.assertTrue(any("64-hex sha256" in issue.detail for issue in arbitrary.issues))

    def test_verified_disposition_authority_settles(self):
        verdict = base_verdict()
        _, sha = self.authority_record()
        result = self.derive(self.payload([self.disposition_source(sha)], True), verdict, self.root)
        self.assertTrue(result.settled)
        self.assertEqual(result.issues, [])

    def test_revoked_disposition_authority_blocks(self):
        verdict = base_verdict()
        _, sha = self.authority_record(status="REVOKED")
        result = self.derive(self.payload([self.disposition_source(sha)], True), verdict, self.root)
        self.assertFalse(result.settled)
        self.assertTrue(any("not ACTIVE" in issue.detail for issue in result.issues))

    def test_disposition_scope_must_cover_this_change(self):
        verdict = base_verdict()
        _, sha = self.authority_record()
        result = self.derive(
            self.payload([self.disposition_source(sha, head="9" * 40)], True), verdict, self.root
        )
        self.assertFalse(result.settled)
        self.assertTrue(any("scope" in issue.detail for issue in result.issues))

    def test_absent_disposition_authority_record_blocks(self):
        verdict = base_verdict()
        _, sha = self.authority_record()
        (self.root / "authority" / "AUTH-DISP-0001.json").unlink()
        result = self.derive(self.payload([self.disposition_source(sha)], True), verdict, self.root)
        self.assertFalse(result.settled)
        self.assertTrue(any("absent" in issue.detail for issue in result.issues))

    def test_edited_disposition_authority_record_blocks(self):
        verdict = base_verdict()
        _, sha = self.authority_record()
        path = self.root / "authority" / "AUTH-DISP-0001.json"
        path.write_text(path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        result = self.derive(self.payload([self.disposition_source(sha)], True), verdict, self.root)
        self.assertFalse(result.settled)
        self.assertTrue(any("do not match" in issue.detail for issue in result.issues))

    def test_time_bounded_disposition_authority_blocks(self):
        verdict = base_verdict()
        _, sha = self.authority_record()
        source = self.disposition_source(sha)
        source["expires"] = "2026-12-01T00:00:00Z"
        result = self.derive(self.payload([source], True), verdict, self.root)
        self.assertFalse(result.settled)
        self.assertTrue(any("time-bounded" in issue.detail for issue in result.issues))

    def test_declared_disagreement_is_invalid(self):
        result = self.derive(self.payload([{"source_id": "SR-1", "state": "SETTLED"}], False))
        self.assertFalse(result.settled)
        self.assertTrue(
            any("disagrees" in issue.detail for issue in result.issues)
        )

    def test_missing_check_outcome_is_invalid(self):
        payload = self.payload([{"source_id": "SR-1", "state": "SETTLED"}], True)
        payload["pre_audit_checks"] = [{"check_id": "PA-1", "evidence_ref": "EV-1"}]
        result = self.derive(payload)
        self.assertFalse(result.settled)
        self.assertTrue(any("recorded outcome" in issue.detail for issue in result.issues))


class StageRecordTest(unittest.TestCase):
    def setUp(self):
        self.root = pathlib.Path(tempfile.mkdtemp(prefix="aegis-stage-"))
        (self.root / "records").mkdir()

    def tearDown(self):
        shutil.rmtree(str(self.root), ignore_errors=True)

    def stage(self, stage, verdict, content=None):
        relative = "records/%s.md" % stage.lower()
        body = content if content is not None else "# STAGE %s\n" % stage
        path = self.root / relative
        path.write_text(body, encoding="utf-8", newline="\n")
        raw = path.read_bytes()
        return {
            "stage": stage,
            "record_id": "rec-%s-0001" % stage.lower(),
            "record_path": relative,
            "bytes": len(raw),
            "sha256": canonical.sha256_hex(raw),
            "head_sha": HEAD,
            "verdict": verdict,
            "holder_identity_ref": "reviewer-%s" % stage.lower(),
            "independence_class": "INDEPENDENT",
            "snapshot_identity": "snap-%s" % stage.lower(),
            "completed_at": "2026-11-10T19:10:00Z",
        }

    def test_all_required_records_affirmative(self):
        records_input = [self.stage("B", "ACCEPT"), self.stage("D", "ACCEPT"), self.stage("E", "PASS")]
        result = inputs.validate_stage_records(self.root, records_input, HEAD, True)
        self.assertEqual(result.issues, [])
        self.assertEqual(sorted(result.present_by_stage), ["B", "D", "E"])

    def test_bytes_mismatch(self):
        records_input = [self.stage("D", "ACCEPT"), self.stage("E", "PASS")]
        records_input[0]["bytes"] = records_input[0]["bytes"] + 7
        result = inputs.validate_stage_records(self.root, records_input, HEAD, True)
        self.assertTrue(any("bytes do not recompute" in issue.detail for issue in result.issues))

    def test_sha_mismatch(self):
        records_input = [self.stage("D", "ACCEPT"), self.stage("E", "PASS")]
        records_input[1]["sha256"] = "0" * 64
        result = inputs.validate_stage_records(self.root, records_input, HEAD, True)
        self.assertTrue(any("sha256 does not recompute" in issue.detail for issue in result.issues))

    def test_head_mismatch(self):
        records_input = [self.stage("D", "ACCEPT"), self.stage("E", "PASS")]
        records_input[0]["head_sha"] = "9" * 40
        result = inputs.validate_stage_records(self.root, records_input, HEAD, True)
        self.assertTrue(any(issue.code == "STAGE_VERDICT_NOT_ACCEPTED" for issue in result.issues))

    def test_implementer_independence_is_refused(self):
        records_input = [self.stage("D", "ACCEPT"), self.stage("E", "PASS")]
        records_input[0]["independence_class"] = "IMPLEMENTER"
        result = inputs.validate_stage_records(self.root, records_input, HEAD, True)
        self.assertTrue(any("not INDEPENDENT" in issue.detail for issue in result.issues))

    def test_missing_snapshot_identity_is_refused(self):
        records_input = [self.stage("D", "ACCEPT"), self.stage("E", "PASS")]
        records_input[1]["snapshot_identity"] = ""
        result = inputs.validate_stage_records(self.root, records_input, HEAD, True)
        self.assertTrue(any("snapshot_identity" in issue.detail for issue in result.issues))

    def test_missing_required_stage(self):
        records_input = [self.stage("E", "PASS")]
        result = inputs.validate_stage_records(self.root, records_input, HEAD, True)
        self.assertTrue(any("required D stage record" in issue.detail for issue in result.issues))
        self.assertTrue(any("required B stage record" in issue.detail for issue in result.issues))

    def test_non_affirmative_values(self):
        records_input = [self.stage("D", "REVISE"), self.stage("E", "FAIL")]
        result = inputs.validate_stage_records(self.root, records_input, HEAD, True)
        codes = {issue.code for issue in result.issues}
        self.assertIn("STAGE_VERDICT_NOT_ACCEPTED", codes)

    def test_duplicate_stage_is_refused(self):
        records_input = [self.stage("D", "ACCEPT"), self.stage("D", "ACCEPT"), self.stage("E", "PASS")]
        result = inputs.validate_stage_records(self.root, records_input, HEAD, True)
        self.assertTrue(any("more than one D" in issue.detail for issue in result.issues))


class HeadHistoryTest(unittest.TestCase):
    def setUp(self):
        self.root = pathlib.Path(tempfile.mkdtemp(prefix="aegis-history-"))

    def tearDown(self):
        shutil.rmtree(str(self.root), ignore_errors=True)

    def history(self, status, heads=None, verdict=None, drop=(), **extra):
        payload = {
            "change_id": 42,
            "candidate_head": HEAD,
            "heads": heads or [{"seq": 1, "head_sha": HEAD, "kind": "INITIAL"}],
        }
        payload.update(extra)
        for key in drop:
            payload.pop(key, None)
        path = write_envelope(self.root, "history.json", payload, status=status)
        return inputs.validate_head_history(inputs.load_envelope(path), verdict)

    def verdict(self, change_id=42, head=HEAD):
        return {"change": {"id": change_id}, "head_sha": head}

    def test_verified(self):
        result = self.history("VERIFIED")
        self.assertEqual(result.status, "VERIFIED")
        self.assertEqual(result.issues, [])

    def test_unverified_blocks(self):
        result = self.history("UNVERIFIED")
        self.assertEqual(result.status, "UNVERIFIED")
        self.assertTrue(any("not VERIFIED" in issue.detail for issue in result.issues))

    def test_missing_status_blocks(self):
        result = self.history(None)
        self.assertTrue(any("provenance.status" in issue.detail for issue in result.issues))

    def test_export_bound_to_the_evaluated_change_and_head(self):
        result = self.history("VERIFIED", verdict=self.verdict())
        self.assertEqual(result.issues, [])

    def test_foreign_change_export_is_refused(self):
        result = self.history("VERIFIED", verdict=self.verdict(), change_id=43)
        self.assertTrue(any("not the evaluated change" in issue.detail for issue in result.issues))

    def test_export_for_an_earlier_head_is_refused(self):
        result = self.history("VERIFIED", verdict=self.verdict(), candidate_head="9" * 40)
        self.assertTrue(any("not the evaluated head" in issue.detail for issue in result.issues))

    def test_export_without_change_identity_is_refused(self):
        result = self.history("VERIFIED", verdict=self.verdict(), drop=("change_id",))
        self.assertTrue(any("declares no change_id" in issue.detail for issue in result.issues))

    def test_export_without_candidate_head_is_refused(self):
        result = self.history("VERIFIED", verdict=self.verdict(), drop=("candidate_head",))
        self.assertTrue(any("declares no candidate_head" in issue.detail for issue in result.issues))


class EvidenceSetTest(unittest.TestCase):
    def test_evidence_hash_recomputes(self):
        evidence = [{"evidence_id": "EV-1", "sha256": "1" * 64, "head": HEAD}]
        verdict = {"evidence_inputs_sha256": canonical.digest(evidence)}
        self.assertEqual(inputs.check_evidence_set({"evidence_set": evidence}, verdict), [])
        verdict["evidence_inputs_sha256"] = "0" * 64
        issues = inputs.check_evidence_set({"evidence_set": evidence}, verdict)
        self.assertTrue(any(issue.code == "CANONICAL_FIELD_MISSING_OR_MISMATCH" for issue in issues))

    def test_missing_evidence_set_is_required_input(self):
        issues = inputs.check_evidence_set({}, {"evidence_inputs_sha256": "0" * 64})
        self.assertTrue(any(issue.code == "REQUIRED_INPUT_UNAVAILABLE" for issue in issues))


if __name__ == "__main__":
    unittest.main()
