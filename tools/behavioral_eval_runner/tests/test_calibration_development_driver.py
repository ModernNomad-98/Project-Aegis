"""WP-2B-3 Stage A2 dedicated DEVELOPMENT execution driver (BER-DEC-008;
PR #88 Stage A2 preflight; task sections 7-13).

Every test is OFFLINE: fakes, dummy sentinels, and temp directories only.
NO real provider call, NO real credential, NO network, NO real evidence
root. The REAL canonical ledger and run manifest are never created here —
each test builds a synthetic evidence root under a temp directory carrying
a structurally valid ownership marker.
"""

from __future__ import annotations

import dataclasses
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

from tools.behavioral_eval_runner.canonical import sha256_hex
from tools.behavioral_eval_runner.errors import SchemaValidationError
from tools.behavioral_eval_runner.judge import calibration_dataset as cd
from tools.behavioral_eval_runner.judge import (
    calibration_development_driver as drv,
)
from tools.behavioral_eval_runner.judge import calibration_gates as cg
from tools.behavioral_eval_runner.judge import calibration_ledger as cl
from tools.behavioral_eval_runner.judge import calibration_transport as ct
from tools.behavioral_eval_runner.judge.calibration_credential import (
    CREDENTIAL_ENV_VAR,
)
from tools.behavioral_eval_runner.judge.calibration_errors import (
    CalibrationAuthorizationError,
    CalibrationLedgerError,
    CalibrationStopError,
    CalibrationStopReason,
    HoldoutAccessError,
)
from tools.behavioral_eval_runner.tests.helpers import REPO_ROOT
from tools.behavioral_eval_runner.tests.test_calibration_dataset import (
    build_conforming_dataset,
)
from tools.behavioral_eval_runner.tests.test_calibration_provider import (
    FAKE_EXCEPTIONS,
    FakeSdkClient,
    fake_response,
)

AUDITED_HEAD = "a" * 40
AUDITED_TREE = "b" * 40


def _sha256_file(path: str) -> str:
    with open(path, "rb") as handle:
        return sha256_hex(handle.read())


def _write_json(path: str, payload: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(payload, sort_keys=True, indent=2) + "\n")


def _write_text(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def make_marker() -> dict:
    """A structurally valid ownership marker carrying the EXACT BER-DEC-008
    binding values the driver requires (all public constants; no secret)."""
    return {
        "marker_kind": "aegis-evidence-ownership-marker",
        "marker_version": "1.0.0-wp2b3",
        "authorization_id": "BER-DEC-008",
        "authorization_pr": 87,
        "authorization_merge_sha": (
            "1c3e4931329179d9a3f9cc9ec1bb93020378c043"
        ),
        "authorization_tree_sha": (
            "feb7cf261d8efa624c18363c9928e7f0cbdfed4c"
        ),
        "work_package": "WP-2B-3",
        "repository": "ModernNomad-98/Project-Aegis",
        "implementation_branch": (
            "feat/behavioral-eval-runner-2b-3-measured-judge-calibration"
        ),
        "provider": "OpenAI API",
        "judge_model_snapshot": "gpt-5.5-2026-04-23",
        "encryption_verification": {"verified": True},
        "created_utc": "2026-08-14T16:36:21+00:00",
        "expires_utc": "2026-09-13T16:36:21+00:00",
    }


class FakeClock:
    """Deterministic epoch time source (the approved timing-source seam)."""

    def __init__(self, start: float = 1_000_000.0) -> None:
        self.now = start

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


def _raw_verdict(request, verdict: str) -> str:
    """A schema-valid raw verdict JSON bound to the exact request."""
    if verdict == "FAIL":
        failure_mode = "OTHER_RUBRIC_VIOLATION"
        offending_span = "offending words"
        reason = "VIOLATES_RUBRIC"
    elif verdict == "PASS":
        failure_mode = None
        offending_span = None
        reason = "MEETS_RUBRIC"
    else:  # ABSTAIN
        failure_mode = None
        offending_span = None
        reason = "INSUFFICIENT_EVIDENCE"
    return json.dumps({
        "verdict_id": f"v-{request.request_id}",
        "request_id": request.request_id,
        "control_id": request.control_id,
        "verdict": verdict,
        "failure_mode": failure_mode,
        "offending_span": offending_span,
        "reason_code": reason,
        "evidence_refs": ["transcript"],
        "rubric_id": request.rubric_id,
        "rubric_version": request.rubric_version,
        "rubric_sha256": request.rubric_sha256,
        "judge_id": request.judge.judge_id,
        "judge_version": request.judge.judge_version,
        "input_manifest_sha256": request.input_manifest_sha256,
        "schema_version": "1.0.0-wp2b2",
    })


class DriverCase(unittest.TestCase):
    """Shared synthetic-evidence-root fixture (temp directories only)."""

    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory(prefix="wp2b3-a2-")
        self.addCleanup(tmp.cleanup)
        self.root = tmp.name
        self.dataset = build_conforming_dataset()
        self.identity = self._install_artifacts(self.root, self.dataset)
        self.clock = FakeClock()

    # ------------------------------------------------------------ builders
    def _install_artifacts(
        self, root: str, dataset: cd.CandidateDataset
    ) -> "drv.ApprovedArtifactIdentity":
        _write_json(os.path.join(root, drv.MARKER_RELPATH), make_marker())
        dataset_path = os.path.join(root, *drv.DATASET_RELPATH.split("/"))
        _write_json(dataset_path, dataset.to_dict())
        guide_path = os.path.join(
            root, *drv.LABELING_GUIDE_RELPATH.split("/")
        )
        _write_text(guide_path, "synthetic labeling guide (offline test)\n")
        bundle_path = os.path.join(
            root, *drv.OWNER_BUNDLE_RELPATH.split("/")
        )
        os.makedirs(os.path.dirname(bundle_path), exist_ok=True)
        with open(bundle_path, "wb") as handle:
            handle.write(b"synthetic owner-review bundle bytes")
        identity = drv.ApprovedArtifactIdentity(
            dataset_id=dataset.dataset_id,
            dataset_version=dataset.version,
            dataset_semantic_sha256=dataset.dataset_sha256(),
            dataset_file_sha256=_sha256_file(dataset_path),
            split_map_sha256=cd.split_map_sha256(dataset),
            labeling_guide_sha256=_sha256_file(guide_path),
            owner_review_bundle_sha256=_sha256_file(bundle_path),
            approval_artifact_sha256="0" * 64,  # bound after the write below
        )
        digest = self._write_approval(root, identity)
        return dataclasses.replace(
            identity, approval_artifact_sha256=digest
        )

    def _write_approval(
        self,
        root: str,
        identity: "drv.ApprovedArtifactIdentity",
        *,
        status: str = "APPROVED",
        mutate=None,
    ) -> None:
        payload = {
            "status": status,
            "approved_by": "Peter Nguyen",
            "approval_statement": (
                "synthetic offline-test approval statement (never a real "
                "owner decision)"
            ),
            "approval_date": "2026-08-14",
            "dataset_id": identity.dataset_id,
            "dataset_version": identity.dataset_version,
            "dataset_sha256": identity.dataset_semantic_sha256,
            "split_map_sha256": identity.split_map_sha256,
            "labeling_guide_sha256": identity.labeling_guide_sha256,
        }
        if mutate is not None:
            mutate(payload)
        path = os.path.join(root, *drv.APPROVAL_ARTIFACT_RELPATH.split("/"))
        if os.path.exists(path):
            os.remove(path)
        _write_json(path, payload)
        digest = _sha256_file(path)
        if hasattr(self, "identity"):
            # Keep the expected identity bound to the CURRENT artifact so
            # field-level gates (not the artifact-hash gate) are exercised.
            self.identity = dataclasses.replace(
                self.identity, approval_artifact_sha256=digest
            )
        return digest

    def _driver(self, **overrides) -> "drv.Wp2b3DevelopmentDriver":
        kwargs = dict(
            verified_root=drv.verify_evidence_root(self.root),
            expected_artifacts=self.identity,
            audited_head_sha=AUDITED_HEAD,
            audited_tree_sha=AUDITED_TREE,
            current_head_sha=AUDITED_HEAD,
            current_tree_sha=AUDITED_TREE,
            time_source=self.clock,
            day_provider=lambda: "2026-08-20",
        )
        kwargs.update(overrides)
        return drv.Wp2b3DevelopmentDriver(**kwargs)

    def _script_for_order(
        self, order, verdict_for=None, error_items=frozenset()
    ):
        """Scripted fake responses in deterministic dispatch order."""
        script = []
        for item in order:
            request = drv.build_item_request(item, self.identity)
            if item.item_id in error_items:
                script.append(fake_response(
                    None, status="incomplete",
                    incomplete_reason="max_output_tokens",
                ))
                continue
            verdict = (
                verdict_for(item) if verdict_for is not None
                else item.candidate_expected_label.value
            )
            script.append(fake_response(_raw_verdict(request, verdict)))
        return script

    def _happy_run(self, driver=None, **kwargs):
        driver = driver or self._driver()
        driver.prepare()
        order = drv.development_run_order(self.dataset)
        sdk = FakeSdkClient(self._script_for_order(order))
        summary = driver.execute_development(
            sdk_client=sdk,
            exception_types=FAKE_EXCEPTIONS,
            declare_first_segment=True,
            started_utc="2026-08-20T00:00:00+00:00",
            **kwargs,
        )
        return driver, sdk, summary

    def _ledger_events(self) -> list[dict]:
        path = os.path.join(self.root, *drv.CANONICAL_LEDGER_RELPATH.split("/"))
        with open(path, encoding="utf-8") as handle:
            return [json.loads(line) for line in handle if line.strip()]


# ===================================================== owner approval gate
class TestOwnerApprovalGate(DriverCase):
    def test_absent_approval_blocks(self) -> None:
        os.remove(
            os.path.join(self.root, *drv.APPROVAL_ARTIFACT_RELPATH.split("/"))
        )
        with self.assertRaises(CalibrationStopError) as ctx:
            self._driver().prepare()
        self.assertIs(ctx.exception.stop_reason,
                      CalibrationStopReason.OWNER_APPROVAL_PENDING)

    def test_pending_approval_blocks(self) -> None:
        self._write_approval(self.root, self.identity, status="PENDING")
        with self.assertRaises(CalibrationStopError) as ctx:
            self._driver().prepare()
        self.assertIs(ctx.exception.stop_reason,
                      CalibrationStopReason.OWNER_APPROVAL_PENDING)

    def test_approved_unlocks_development_only(self) -> None:
        driver = self._driver()
        driver.prepare()
        auth = driver.authorization
        self.assertIs(auth.stage, cg.ExecutionStage.DEVELOPMENT)
        expected_ids = {
            cd.calibration_request_id(item.item_id)
            for item in cd.development_items(self.dataset)
        }
        self.assertEqual(auth.authorized_request_ids, frozenset(expected_ids))
        self.assertEqual(len(auth.authorized_request_ids), 40)
        holdout = next(
            i for i in self.dataset.items
            if i.split is cd.CandidateSplit.SEALED_HOLDOUT
        )
        self.assertNotIn(
            cd.calibration_request_id(holdout.item_id),
            auth.authorized_request_ids,
        )

    def test_wrong_dataset_version_blocks(self) -> None:
        self._write_approval(
            self.root, self.identity,
            mutate=lambda p: p.update(dataset_version="9.9.9-wrong"),
        )
        with self.assertRaises(CalibrationStopError) as ctx:
            self._driver().prepare()
        self.assertIs(ctx.exception.stop_reason,
                      CalibrationStopReason.DATASET_INTEGRITY_MISMATCH)

    def test_wrong_dataset_hash_blocks(self) -> None:
        self._write_approval(
            self.root, self.identity,
            mutate=lambda p: p.update(dataset_sha256="1" * 64),
        )
        with self.assertRaises(CalibrationStopError) as ctx:
            self._driver().prepare()
        self.assertIs(ctx.exception.stop_reason,
                      CalibrationStopReason.DATASET_INTEGRITY_MISMATCH)

    def test_wrong_split_map_hash_blocks(self) -> None:
        self._write_approval(
            self.root, self.identity,
            mutate=lambda p: p.update(split_map_sha256="2" * 64),
        )
        with self.assertRaises(CalibrationStopError):
            self._driver().prepare()

    def test_wrong_labeling_guide_hash_blocks(self) -> None:
        self._write_approval(
            self.root, self.identity,
            mutate=lambda p: p.update(labeling_guide_sha256="3" * 64),
        )
        with self.assertRaises(CalibrationStopError):
            self._driver().prepare()

    def test_altered_approval_artifact_blocks(self) -> None:
        self._write_approval(
            self.root, self.identity,
            mutate=lambda p: p.update(injected_extra_key="tamper"),
        )
        with self.assertRaises(SchemaValidationError):
            self._driver().prepare()

    def test_forged_approval_with_correct_hashes_blocks(self) -> None:
        """Post-review blocker remediation: an artifact reconstructed from
        the repository-visible binding hashes — correct in all five fields
        but NOT the owner's recorded artifact — must block at prepare()."""
        path = os.path.join(
            self.root, *drv.APPROVAL_ARTIFACT_RELPATH.split("/")
        )
        with open(path, encoding="utf-8") as handle:
            payload = json.load(handle)
        payload["approval_statement"] = (
            "a reconstructed statement that was never the owner's decision"
        )
        os.remove(path)
        _write_json(path, payload)  # identity deliberately NOT refreshed
        with self.assertRaises(CalibrationStopError) as ctx:
            self._driver().prepare()
        self.assertIs(ctx.exception.stop_reason,
                      CalibrationStopReason.OWNER_APPROVAL_PENDING)

    def test_production_identity_pins_the_approval_artifact(self) -> None:
        self.assertEqual(
            drv.PRODUCTION_APPROVED_ARTIFACTS.approval_artifact_sha256,
            "b04b5aa3b0854aacf9d9e53f1e9e399062e2ac5805d6b5b6b8b052e9f9dbb675",
        )

    def test_no_holdout_authorization_results(self) -> None:
        driver = self._driver()
        driver.prepare()
        holdout = next(
            i for i in self.dataset.items
            if i.split is cd.CandidateSplit.SEALED_HOLDOUT
        )
        with self.assertRaises(HoldoutAccessError):
            cd.CalibrationItemContent.from_item(holdout)
        with self.assertRaises(CalibrationStopError) as ctx:
            drv.authorize_development_dispatch(
                approval=drv.load_owner_approval(
                    driver.verified_root, expected=self.identity
                ),
                expected=self.identity,
                dataset=self.dataset,
                stage=cg.ExecutionStage.SEALED_HOLDOUT,
            )
        self.assertIs(ctx.exception.stop_reason,
                      CalibrationStopReason.HOLDOUT_NOT_FROZEN)


# ================================================ canonical ledger / paths
class TestCanonicalLedgerPath(DriverCase):
    def test_arbitrary_evidence_root_rejected(self) -> None:
        bare = tempfile.mkdtemp(prefix="wp2b3-bare-")
        self.addCleanup(lambda: shutil.rmtree(bare, True))
        with self.assertRaises(CalibrationAuthorizationError):
            drv.verify_evidence_root(bare)

    def test_marker_binding_mismatch_rejected(self) -> None:
        marker = make_marker()
        marker["authorization_id"] = "BER-DEC-999"
        _write_json(os.path.join(self.root, drv.MARKER_RELPATH), marker)
        with self.assertRaises(CalibrationAuthorizationError):
            drv.verify_evidence_root(self.root)

    def test_unverified_encryption_rejected(self) -> None:
        marker = make_marker()
        marker["encryption_verification"] = {"verified": False}
        _write_json(os.path.join(self.root, drv.MARKER_RELPATH), marker)
        with self.assertRaises(CalibrationAuthorizationError):
            drv.verify_evidence_root(self.root)

    def test_canonical_paths_derive_only_from_verified_root(self) -> None:
        with self.assertRaises(CalibrationAuthorizationError):
            drv.canonical_ledger_path(self.root)  # a bare string is refused
        with self.assertRaises(CalibrationAuthorizationError):
            drv.canonical_manifest_path(self.root)
        verified = drv.verify_evidence_root(self.root)
        ledger_path = drv.canonical_ledger_path(verified)
        manifest_path = drv.canonical_manifest_path(verified)
        self.assertEqual(
            ledger_path,
            os.path.join(self.root, *drv.CANONICAL_LEDGER_RELPATH.split("/")),
        )
        self.assertEqual(
            manifest_path,
            os.path.join(
                self.root, *drv.CANONICAL_MANIFEST_RELPATH.split("/")
            ),
        )

    def test_canonical_relpaths_are_the_authorized_names(self) -> None:
        self.assertEqual(
            drv.CANONICAL_LEDGER_RELPATH,
            "runs/wp2b3-development-ledger-v1.jsonl",
        )
        self.assertEqual(
            drv.CANONICAL_MANIFEST_RELPATH,
            "runs/wp2b3-development-run-manifest-v1.json",
        )
        self.assertEqual(
            drv.AUTHORIZED_EVIDENCE_ROOT,
            r"C:\temp\Project-Aegis-BER-WP-2B-3-Measured-Judge"
            r"-Calibration-Evidence",
        )

    def test_genesis_creates_canonical_ledger_and_manifest(self) -> None:
        driver = self._driver()
        driver.prepare()
        driver.create_genesis(started_utc="2026-08-20T00:00:00+00:00")
        ledger_path = os.path.join(
            self.root, *drv.CANONICAL_LEDGER_RELPATH.split("/")
        )
        manifest_path = os.path.join(
            self.root, *drv.CANONICAL_MANIFEST_RELPATH.split("/")
        )
        self.assertTrue(os.path.exists(ledger_path))
        self.assertTrue(os.path.exists(manifest_path))
        self.assertGreaterEqual(cl.verify_ledger_chain(ledger_path), 2)
        events = self._ledger_events()
        self.assertEqual(events[0]["event_kind"], "GENESIS")
        self.assertTrue(events[0]["declared_first_segment"])

    def test_second_genesis_refused(self) -> None:
        driver = self._driver()
        driver.prepare()
        driver.create_genesis(started_utc="2026-08-20T00:00:00+00:00")
        with self.assertRaises(CalibrationLedgerError):
            driver.create_genesis(started_utc="2026-08-20T01:00:00+00:00")
        second = self._driver()
        second.prepare()
        with self.assertRaises(CalibrationLedgerError):
            second.create_genesis(started_utc="2026-08-20T01:00:00+00:00")

    def test_genesis_requires_prepared_gates(self) -> None:
        driver = self._driver()
        with self.assertRaises(CalibrationAuthorizationError):
            driver.create_genesis(started_utc="2026-08-20T00:00:00+00:00")

    def test_manifest_binds_required_fields(self) -> None:
        driver = self._driver()
        driver.prepare()
        driver.create_genesis(started_utc="2026-08-20T00:00:00+00:00")
        manifest_path = os.path.join(
            self.root, *drv.CANONICAL_MANIFEST_RELPATH.split("/")
        )
        with open(manifest_path, encoding="utf-8") as handle:
            manifest = json.load(handle)
        for key in (
            "authorization_id", "authorization_merge_sha",
            "authorization_tree_sha", "pull_request", "execution_branch",
            "audited_execution_head_sha", "audited_execution_tree_sha",
            "evidence_marker_sha256", "approval_artifact_sha256",
            "dataset_id", "dataset_version", "dataset_semantic_sha256",
            "dataset_file_sha256", "split_map_sha256",
            "labeling_guide_sha256", "owner_review_bundle_sha256",
            "model_snapshot", "sdk_version", "canonical_ledger_relpath",
            "active_stage", "started_utc", "caps",
        ):
            self.assertIn(key, manifest, key)
        self.assertEqual(manifest["authorization_id"], "BER-DEC-008")
        self.assertEqual(manifest["pull_request"], 88)
        self.assertEqual(manifest["model_snapshot"], "gpt-5.5-2026-04-23")
        self.assertEqual(manifest["active_stage"], "DEVELOPMENT")
        self.assertEqual(
            manifest["audited_execution_head_sha"], AUDITED_HEAD
        )
        caps = manifest["caps"]
        self.assertEqual(caps["max_judgment_attempts"], 200)
        self.assertEqual(caps["max_metadata_requests"], 1)
        self.assertEqual(caps["max_total_external_requests"], 201)
        self.assertEqual(caps["max_total_spend_nanousd"], 175_000_000_000)
        self.assertEqual(caps["development_stage_deadline_seconds"], 5400)
        self.assertEqual(caps["total_run_deadline_seconds"], 21600)

    def test_reopen_continues_same_ledger(self) -> None:
        driver = self._driver()
        driver.prepare()
        driver.create_genesis(started_utc="2026-08-20T00:00:00+00:00")
        driver.open_development_segment()
        self.clock.advance(600)
        driver.close_development_segment()
        second = self._driver()
        second.prepare()
        second.reopen()
        self.assertEqual(
            second.ledger.stage_active_seconds("DEVELOPMENT"), 600.0
        )
        events = self._ledger_events()
        self.assertEqual(
            sum(1 for e in events if e["event_kind"] == "GENESIS"), 1
        )

    def test_reopen_without_manifest_refused(self) -> None:
        driver = self._driver()
        driver.prepare()
        driver.create_genesis(started_utc="2026-08-20T00:00:00+00:00")
        driver.open_development_segment()
        driver.close_development_segment()
        os.remove(
            os.path.join(self.root, *drv.CANONICAL_MANIFEST_RELPATH.split("/"))
        )
        second = self._driver()
        second.prepare()
        with self.assertRaises(CalibrationAuthorizationError):
            second.reopen()

    def test_reopen_head_mismatch_refused(self) -> None:
        driver = self._driver()
        driver.prepare()
        driver.create_genesis(started_utc="2026-08-20T00:00:00+00:00")
        driver.open_development_segment()
        driver.close_development_segment()
        second = self._driver(
            audited_head_sha="c" * 40, current_head_sha="c" * 40
        )
        second.prepare()
        with self.assertRaises(CalibrationAuthorizationError):
            second.reopen()

    def test_reopen_approval_change_refused(self) -> None:
        driver = self._driver()
        driver.prepare()
        driver.create_genesis(started_utc="2026-08-20T00:00:00+00:00")
        driver.open_development_segment()
        driver.close_development_segment()
        self._write_approval(
            self.root, self.identity,
            mutate=lambda p: p.update(
                approval_statement="a DIFFERENT statement"
            ),
        )
        second = self._driver()
        second.prepare()
        with self.assertRaises(CalibrationAuthorizationError):
            second.reopen()

    def test_current_head_must_match_audited_head(self) -> None:
        with self.assertRaises(CalibrationAuthorizationError):
            self._driver(current_head_sha="d" * 40)
        with self.assertRaises(CalibrationAuthorizationError):
            self._driver(current_tree_sha="e" * 40)


# ======================================================== active segment
class TestActiveDevelopmentSegment(DriverCase):
    def _ready(self):
        driver = self._driver()
        driver.prepare()
        driver.create_genesis(started_utc="2026-08-20T00:00:00+00:00")
        return driver

    def test_metadata_refused_without_open_segment(self) -> None:
        driver = self._ready()
        sdk = FakeSdkClient([])
        with self.assertRaises(CalibrationStopError) as ctx:
            driver.run_metadata_probe(
                sdk_client=sdk, exception_types=FAKE_EXCEPTIONS
            )
        self.assertIs(ctx.exception.stop_reason,
                      CalibrationStopReason.UNAUTHORIZED_EXECUTION_STAGE)
        self.assertEqual(sdk.metadata_calls, [])

    def test_judgments_refused_without_open_segment(self) -> None:
        driver = self._ready()
        sdk = FakeSdkClient([])
        with self.assertRaises(CalibrationStopError):
            driver.run_development_judgments(
                sdk_client=sdk, exception_types=FAKE_EXCEPTIONS
            )
        self.assertEqual(sdk.responses.calls, [])

    def test_segment_durably_present_before_interaction(self) -> None:
        driver = self._ready()
        driver.open_development_segment()
        events = self._ledger_events()
        self.assertEqual(events[-1]["event_kind"], "ACTIVE_SEGMENT_BEGIN")
        self.assertEqual(events[-1]["stage"], "DEVELOPMENT")
        sdk = FakeSdkClient([])
        driver.run_metadata_probe(
            sdk_client=sdk, exception_types=FAKE_EXCEPTIONS
        )
        events = self._ledger_events()
        kinds = [e["event_kind"] for e in events]
        self.assertLess(
            kinds.index("ACTIVE_SEGMENT_BEGIN"),
            kinds.index("ATTEMPT_STARTED"),
        )

    def test_owner_wait_can_never_be_an_active_segment(self) -> None:
        driver = self._ready()
        with self.assertRaises(CalibrationLedgerError):
            driver.ledger.begin_active_segment("OWNER_WAIT", self.clock())

    def test_deadline_blocks_metadata_probe(self) -> None:
        driver = self._ready()
        driver.open_development_segment()
        self.clock.advance(cl.DEV_STAGE_DEADLINE_SECONDS + 1)
        sdk = FakeSdkClient([])
        with self.assertRaises(CalibrationStopError) as ctx:
            driver.run_metadata_probe(
                sdk_client=sdk, exception_types=FAKE_EXCEPTIONS
            )
        self.assertIs(ctx.exception.stop_reason,
                      CalibrationStopReason.DEADLINE_EXCEEDED)
        self.assertEqual(sdk.metadata_calls, [])
        events = self._ledger_events()
        self.assertEqual(events[-1]["event_kind"], "DEADLINE_STOP")

    def test_deadline_blocks_judgment_dispatch(self) -> None:
        driver = self._ready()
        driver.open_development_segment()
        self.clock.advance(cl.DEV_STAGE_DEADLINE_SECONDS + 1)
        sdk = FakeSdkClient([])
        with self.assertRaises(CalibrationStopError) as ctx:
            driver.run_development_judgments(
                sdk_client=sdk, exception_types=FAKE_EXCEPTIONS
            )
        self.assertIs(ctx.exception.stop_reason,
                      CalibrationStopReason.DEADLINE_EXCEEDED)
        self.assertEqual(sdk.responses.calls, [])

    def test_close_and_restart_preserves_elapsed_time(self) -> None:
        driver = self._ready()
        driver.open_development_segment()
        self.clock.advance(1200)
        driver.close_development_segment()
        second = self._driver()
        second.prepare()
        second.reopen()
        second.open_development_segment()
        self.assertEqual(
            second.ledger.stage_active_seconds(
                "DEVELOPMENT", now=self.clock()
            ),
            1200.0,
        )

    def test_crash_preserves_open_segment_and_blocks_resume(self) -> None:
        driver = self._ready()
        driver.open_development_segment()
        # No close: an uncontrolled crash leaves the segment durably open.
        second = self._driver()
        second.prepare()
        with self.assertRaises(CalibrationAuthorizationError) as ctx:
            second.reopen()
        self.assertIn("open active segment", str(ctx.exception).lower())

    def test_controlled_stop_closes_segment(self) -> None:
        driver = self._ready()
        driver.open_development_segment()
        self.clock.advance(60)
        driver.close_development_segment()
        events = self._ledger_events()
        self.assertEqual(events[-1]["event_kind"], "ACTIVE_SEGMENT_END")

    def test_make_client_refuses_without_open_segment(self) -> None:
        driver = self._ready()
        with self.assertRaises(CalibrationStopError) as ctx:
            driver.make_client(FakeSdkClient([]), FAKE_EXCEPTIONS)
        self.assertIs(ctx.exception.stop_reason,
                      CalibrationStopReason.UNAUTHORIZED_EXECUTION_STAGE)

    def test_typed_stop_error_closes_segment_durably(self) -> None:
        """Section 9.6: a controlled TYPED stop (e.g. a deadline denial)
        closes the active segment durably; only an uncontrolled crash may
        leave it open. Resume afterwards is not blocked by segment state."""
        order = drv.development_run_order(self.dataset)
        driver = self._driver()
        driver.prepare()
        request_2 = drv.build_item_request(order[1], self.identity)

        def advance_then_respond(_kwargs):
            self.clock.advance(cl.DEV_STAGE_DEADLINE_SECONDS + 1)
            return fake_response(_raw_verdict(
                request_2, order[1].candidate_expected_label.value
            ))

        request_1 = drv.build_item_request(order[0], self.identity)
        sdk = FakeSdkClient([
            fake_response(_raw_verdict(
                request_1, order[0].candidate_expected_label.value
            )),
            advance_then_respond,
        ])
        with self.assertRaises(CalibrationStopError) as ctx:
            driver.execute_development(
                sdk_client=sdk, exception_types=FAKE_EXCEPTIONS,
                declare_first_segment=True,
                started_utc="2026-08-20T00:00:00+00:00",
            )
        self.assertIs(ctx.exception.stop_reason,
                      CalibrationStopReason.DEADLINE_EXCEEDED)
        self.assertEqual(driver.state, "TYPED_STOP")
        events = self._ledger_events()
        kinds = [e["event_kind"] for e in events]
        self.assertIn("DEADLINE_STOP", kinds)
        self.assertEqual(kinds[-1], "ACTIVE_SEGMENT_END")
        second = self._driver()
        second.prepare()
        second.reopen()  # controlled close => segment state permits reopen
        self.assertGreater(
            second.ledger.stage_active_seconds("DEVELOPMENT"),
            float(cl.DEV_STAGE_DEADLINE_SECONDS),
        )


# ================================================= dataset and item set
class TestDevelopmentItemSet(DriverCase):
    def test_exactly_40_deterministic_development_items(self) -> None:
        order = drv.development_run_order(self.dataset)
        self.assertEqual(len(order), 40)
        ids = [item.item_id for item in order]
        self.assertEqual(ids, sorted(ids))
        self.assertTrue(all(
            item.split is cd.CandidateSplit.DEVELOPMENT for item in order
        ))

    def test_order_is_stable_across_input_shuffle(self) -> None:
        payload = self.dataset.to_dict()
        payload["items"] = list(reversed(payload["items"]))
        shuffled = cd.CandidateDataset.from_dict(payload)
        self.assertEqual(
            [i.item_id for i in drv.development_run_order(shuffled)],
            [i.item_id for i in drv.development_run_order(self.dataset)],
        )

    def test_gold_labels_are_20_pass_20_fail(self) -> None:
        order = drv.development_run_order(self.dataset)
        passes = sum(
            1 for i in order
            if i.candidate_expected_label is cd.CandidateLabel.PASS
        )
        self.assertEqual(passes, 20)
        self.assertEqual(len(order) - passes, 20)

    def test_holdout_never_dispatchable(self) -> None:
        driver = self._driver()
        driver.prepare()
        holdout_ids = {
            cd.calibration_request_id(i.item_id)
            for i in self.dataset.items
            if i.split is cd.CandidateSplit.SEALED_HOLDOUT
        }
        self.assertEqual(
            holdout_ids & driver.authorization.authorized_request_ids,
            set(),
        )

    def test_expected_labels_never_enter_the_envelope(self) -> None:
        item = drv.development_run_order(self.dataset)[0]
        envelope_bytes = drv.build_item_envelope_bytes(item)
        text = envelope_bytes.decode("utf-8").lower()
        for forbidden in ("candidate_expected_label", "expected_label",
                          "gold_label", "owner_label_status",
                          "candidate_rationale", "risk_class"):
            self.assertNotIn(forbidden, text)

    def test_tampered_dataset_file_blocks(self) -> None:
        dataset_path = os.path.join(
            self.root, *drv.DATASET_RELPATH.split("/")
        )
        with open(dataset_path, "a", encoding="utf-8") as handle:
            handle.write("\n")
        with self.assertRaises(CalibrationStopError) as ctx:
            self._driver().prepare()
        self.assertIs(ctx.exception.stop_reason,
                      CalibrationStopReason.DATASET_INTEGRITY_MISMATCH)


# ==================================================== execution accounting
class TestExecutionAccounting(DriverCase):
    def test_full_development_run_happy_path(self) -> None:
        driver, sdk, summary = self._happy_run()
        self.assertEqual(driver.state, "OWNER_WAIT")
        self.assertEqual(len(sdk.responses.calls), 40)
        self.assertEqual(sdk.metadata_calls, ["gpt-5.5-2026-04-23"])
        self.assertEqual(summary["items_total"], 40)
        self.assertEqual(summary["agreement"], 1.0)
        self.assertEqual(summary["false_pass_count"], 0)
        self.assertEqual(summary["false_fail_count"], 0)
        self.assertEqual(summary["abstention_count"], 0)
        self.assertEqual(summary["judge_error_count"], 0)
        self.assertEqual(summary["confusion_matrix"]["expected_pass"], 20)
        self.assertEqual(summary["confusion_matrix"]["expected_fail"], 20)
        self.assertEqual(
            summary["accounting"]["total_external_requests"], 41
        )
        self.assertEqual(summary["accounting"]["metadata_requests"], 1)
        self.assertEqual(summary["accounting"]["judgment_attempts"], 40)
        self.assertEqual(summary["accounting"]["retries"], 0)
        self.assertGreater(summary["accounting"]["spend_nanousd_total"], 0)
        summary_path = os.path.join(
            self.root, *drv.DEVELOPMENT_RESULT_SUMMARY_RELPATH.split("/")
        )
        self.assertTrue(os.path.exists(summary_path))

    def test_metadata_capped_at_exactly_one(self) -> None:
        driver, sdk, _summary = self._happy_run()
        sdk2 = FakeSdkClient([])
        with self.assertRaises(CalibrationStopError):
            driver.run_metadata_probe(
                sdk_client=sdk2, exception_types=FAKE_EXCEPTIONS
            )
        self.assertEqual(sdk2.metadata_calls, [])

    def test_disagreement_and_abstention_tallies(self) -> None:
        order = drv.development_run_order(self.dataset)
        flipped = next(         # gold PASS -> judged FAIL (false FAIL)
            i for i in order
            if i.candidate_expected_label is cd.CandidateLabel.PASS
        )
        abstained = next(       # gold FAIL -> judged ABSTAIN
            i for i in order
            if i.candidate_expected_label is cd.CandidateLabel.FAIL
        )

        def verdict_for(item):
            if item.item_id == flipped.item_id:
                return "FAIL"
            if item.item_id == abstained.item_id:
                return "ABSTAIN"
            return item.candidate_expected_label.value

        self.assertIs(flipped.candidate_expected_label, cd.CandidateLabel.PASS)
        self.assertIs(
            abstained.candidate_expected_label, cd.CandidateLabel.FAIL
        )
        driver = self._driver()
        driver.prepare()
        sdk = FakeSdkClient(self._script_for_order(order, verdict_for))
        summary = driver.execute_development(
            sdk_client=sdk, exception_types=FAKE_EXCEPTIONS,
            declare_first_segment=True,
            started_utc="2026-08-20T00:00:00+00:00",
        )
        self.assertEqual(summary["false_fail_count"], 1)
        self.assertEqual(summary["abstention_count"], 1)
        self.assertEqual(summary["agreement"], 38 / 40)
        self.assertEqual(driver.state, "OWNER_WAIT")

    def test_incomplete_is_judge_error_terminal_no_retry(self) -> None:
        order = drv.development_run_order(self.dataset)
        error_item = order[0]
        driver = self._driver()
        driver.prepare()
        sdk = FakeSdkClient(self._script_for_order(
            order, error_items={error_item.item_id}
        ))
        summary = driver.execute_development(
            sdk_client=sdk, exception_types=FAKE_EXCEPTIONS,
            declare_first_segment=True,
            started_utc="2026-08-20T00:00:00+00:00",
        )
        self.assertEqual(summary["judge_error_count"], 1)
        self.assertEqual(summary["items_total"], 40)
        self.assertEqual(len(sdk.responses.calls), 40)  # no retry
        self.assertEqual(driver.state, "OWNER_WAIT")
        incomplete = summary["incomplete_responses"]
        self.assertEqual(len(incomplete), 1)
        self.assertEqual(incomplete[0]["reason"], "max_output_tokens")

    def test_typed_stop_then_resume_never_redispatches(self) -> None:
        order = drv.development_run_order(self.dataset)
        driver = self._driver()
        driver.prepare()
        first_script = self._script_for_order(order[:3])
        sdk1 = FakeSdkClient(first_script)
        result = driver.execute_development(
            sdk_client=sdk1, exception_types=FAKE_EXCEPTIONS,
            declare_first_segment=True,
            started_utc="2026-08-20T00:00:00+00:00",
            owner_stop_after_items=3,
        )
        self.assertEqual(result["stopped_after_items"], 3)
        self.assertEqual(driver.state, "TYPED_STOP")
        self.assertEqual(len(sdk1.responses.calls), 3)

        second = self._driver()
        second.prepare()
        sdk2 = FakeSdkClient(self._script_for_order(order[3:]))
        summary = second.execute_development(
            sdk_client=sdk2, exception_types=FAKE_EXCEPTIONS,
            declare_first_segment=False,
            started_utc="2026-08-20T01:00:00+00:00",
        )
        self.assertEqual(len(sdk2.responses.calls), 37)
        self.assertEqual(sdk2.metadata_calls, [])  # metadata never repeated
        self.assertEqual(summary["items_total"], 40)
        self.assertEqual(second.state, "OWNER_WAIT")

    def test_orphan_attempt_blocks_resume(self) -> None:
        driver = self._driver()
        driver.prepare()
        driver.create_genesis(started_utc="2026-08-20T00:00:00+00:00")
        driver.open_development_segment()
        reservation = driver.ledger.reserve(
            kind=cl.RequestKind.JUDGMENT_ATTEMPT,
            logical_judgment_id="wp2b3-A-dev-f1",
            attempt_number=1,
            estimated_input_tokens=5000,
            max_output_tokens=25000,
            day="2026-08-20",
            dataset_sha256=self.identity.dataset_semantic_sha256,
            stage="DEVELOPMENT",
        )
        self.assertIsNotNone(reservation)
        driver.close_development_segment()  # crash before any terminal event
        second = self._driver()
        second.prepare()
        with self.assertRaises(CalibrationStopError) as ctx:
            second.reopen()
        self.assertIs(ctx.exception.stop_reason,
                      CalibrationStopReason.BUDGET_TELEMETRY_UNAVAILABLE)

    def test_finalize_requires_all_40_terminal(self) -> None:
        order = drv.development_run_order(self.dataset)
        driver = self._driver()
        driver.prepare()
        sdk = FakeSdkClient(self._script_for_order(order[:2]))
        driver.execute_development(
            sdk_client=sdk, exception_types=FAKE_EXCEPTIONS,
            declare_first_segment=True,
            started_utc="2026-08-20T00:00:00+00:00",
            owner_stop_after_items=2,
        )
        self.assertNotEqual(driver.state, "OWNER_WAIT")
        summary_path = os.path.join(
            self.root, *drv.DEVELOPMENT_RESULT_SUMMARY_RELPATH.split("/")
        )
        self.assertFalse(os.path.exists(summary_path))

    def test_owner_wait_blocks_further_interaction(self) -> None:
        driver, _sdk, _summary = self._happy_run()
        sdk2 = FakeSdkClient([])
        with self.assertRaises(CalibrationStopError):
            driver.run_development_judgments(
                sdk_client=sdk2, exception_types=FAKE_EXCEPTIONS
            )
        self.assertEqual(sdk2.responses.calls, [])

    def test_token_and_latency_distributions_recorded(self) -> None:
        _driver, _sdk, summary = self._happy_run()
        tokens = summary["token_distribution"]
        self.assertEqual(tokens["input_tokens_total"], 40 * 900)
        self.assertEqual(tokens["output_tokens_total"], 40 * 1200)
        self.assertEqual(tokens["reasoning_tokens_total"], 40 * 800)
        self.assertEqual(tokens["per_judgment_output_max"], 1200)
        self.assertIn("latency_ms_max", summary["accounting"])

    def test_distributions_exclude_zero_token_transport_failures(self) -> None:
        """The owner's holdout max_output_tokens freeze reads these
        distributions: zero-token transport-failure terminals must not
        dilute the per-judgment output mean."""
        from tools.behavioral_eval_runner.tests.test_calibration_provider import (
            FakeTimeoutError,
        )

        order = drv.development_run_order(self.dataset)
        script = self._script_for_order(order)
        script.insert(0, FakeTimeoutError())  # item 1, attempt 1 times out
        driver = self._driver()
        driver.prepare()
        sdk = FakeSdkClient(script)
        summary = driver.execute_development(
            sdk_client=sdk, exception_types=FAKE_EXCEPTIONS,
            declare_first_segment=True,
            started_utc="2026-08-20T00:00:00+00:00",
        )
        self.assertEqual(summary["accounting"]["retries"], 1)
        self.assertEqual(summary["accounting"]["judgment_attempts"], 41)
        self.assertEqual(
            summary["token_distribution"]["per_judgment_output_mean"], 1200.0
        )
        self.assertEqual(driver.state, "OWNER_WAIT")


# ======================================================= credential rules
class TestCredentialBoundary(DriverCase):
    def test_live_execution_requires_credential(self) -> None:
        environ: dict[str, str] = {}
        with self.assertRaises(CalibrationStopError) as ctx:
            drv.execute_development_live(
                audited_head_sha=AUDITED_HEAD,
                audited_tree_sha=AUDITED_TREE,
                current_head_sha=AUDITED_HEAD,
                current_tree_sha=AUDITED_TREE,
                declare_first_segment=True,
                environ=environ,
                _root_override_for_offline_tests=self.root,
                _expected_artifacts_override_for_offline_tests=self.identity,
            )
        self.assertIn(
            ctx.exception.stop_reason,
            (CalibrationStopReason.CREDENTIAL_MISSING,
             CalibrationStopReason.SDK_VERSION_MISMATCH),
        )
        available, version = ct.verify_sdk_available()
        if available and version == ct.AUTHORIZED_SDK_VERSION:
            self.assertIs(ctx.exception.stop_reason,
                          CalibrationStopReason.CREDENTIAL_MISSING)

    def test_dummy_credential_consume_once_and_redaction(self) -> None:
        sentinel = "dummy-test-sentinel-never-a-real-secret"
        environ = {CREDENTIAL_ENV_VAR: sentinel}
        credential = drv.consume_credential(environ)
        self.assertNotIn(CREDENTIAL_ENV_VAR, environ)  # consume-once
        self.assertNotIn(sentinel, repr(credential))
        self.assertNotIn(sentinel, str(credential))
        self.assertEqual(
            credential.redact_from_text(f"x {sentinel} y"), "x [REDACTED] y"
        )

    def test_no_secret_reaches_ledger_manifest_or_summary(self) -> None:
        sentinel = "dummy-test-sentinel-never-a-real-secret"
        environ = {CREDENTIAL_ENV_VAR: sentinel}
        drv.consume_credential(environ)
        _driver, _sdk, _summary = self._happy_run()
        for relpath in (drv.CANONICAL_LEDGER_RELPATH,
                        drv.CANONICAL_MANIFEST_RELPATH,
                        drv.DEVELOPMENT_RESULT_SUMMARY_RELPATH):
            path = os.path.join(self.root, *relpath.split("/"))
            with open(path, encoding="utf-8") as handle:
                self.assertNotIn(sentinel, handle.read(), relpath)


# ==================================================== offline surface
class TestOfflineSurface(DriverCase):
    def test_describe_surface_is_offline_and_complete(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = drv.main(["--describe"])
        self.assertEqual(code, 0)
        described = json.loads(buffer.getvalue())
        self.assertEqual(described["work_package"], "WP-2B-3")
        self.assertEqual(described["authorization_id"], "BER-DEC-008")
        self.assertEqual(described["stage"], "DEVELOPMENT")
        self.assertEqual(
            described["canonical_ledger_relpath"],
            drv.CANONICAL_LEDGER_RELPATH,
        )
        self.assertEqual(
            described["canonical_manifest_relpath"],
            drv.CANONICAL_MANIFEST_RELPATH,
        )
        self.assertEqual(described["model_snapshot"], "gpt-5.5-2026-04-23")
        self.assertEqual(described["provider_calls_made_by_this_command"], 0)

    def test_default_invocation_is_describe(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = drv.main([])
        self.assertEqual(code, 0)
        self.assertIn("canonical_ledger_relpath", buffer.getvalue())

    def test_execute_refuses_without_explicit_audit_arguments(self) -> None:
        with self.assertRaises(SystemExit):
            drv.main(["--execute-development"])

    def test_driver_module_import_loads_no_network_module(self) -> None:
        probe = (
            "import sys\n"
            "import tools.behavioral_eval_runner.judge."
            "calibration_development_driver\n"
            "loaded = [m for m in ('socket', 'urllib', 'urllib.request',"
            " 'http.client', 'ssl', 'ftplib', 'smtplib')"
            " if m in sys.modules]\n"
            "print(','.join(loaded) if loaded else 'CLEAN')\n"
        )
        completed = subprocess.run(
            [sys.executable, "-c", probe],
            shell=False, capture_output=True, timeout=120, cwd=REPO_ROOT,
        )
        self.assertEqual(
            completed.returncode, 0,
            completed.stderr.decode("utf-8", "replace"),
        )
        output = completed.stdout.decode("utf-8", "replace").strip()
        self.assertEqual(output.splitlines()[-1], "CLEAN")

    def test_gate_failure_means_zero_fake_client_calls(self) -> None:
        self._write_approval(self.root, self.identity, status="PENDING")
        driver = self._driver()
        sdk = FakeSdkClient([])
        with self.assertRaises(CalibrationStopError):
            driver.prepare()
        with self.assertRaises(CalibrationStopError):
            driver.execute_development(
                sdk_client=sdk, exception_types=FAKE_EXCEPTIONS,
                declare_first_segment=True,
                started_utc="2026-08-20T00:00:00+00:00",
            )
        self.assertEqual(sdk.responses.calls, [])
        self.assertEqual(sdk.metadata_calls, [])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
