"""Phase 0/1 regressions. Synthetic evidence and fake transport only."""
import inspect
import argparse
import io
import json
import os
import tempfile
import time
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from tools.behavioral_eval_runner.errors import SchemaValidationError
from tools.behavioral_eval_runner.judge import calibration_dataset as cd
from tools.behavioral_eval_runner.judge import calibration_development_driver as drv
from tools.behavioral_eval_runner.judge import calibration_gates as cg
from tools.behavioral_eval_runner.judge import calibration_ledger as cl
from tools.behavioral_eval_runner.judge.calibration_errors import (
    CalibrationAuthorizationError, CalibrationStopError, HoldoutAccessError,
    CalibrationLedgerError,
)
from tools.behavioral_eval_runner.tests.test_calibration_development_driver import DriverCase
from tools.behavioral_eval_runner.tests.test_calibration_provider import FakeSdkClient, FAKE_EXCEPTIONS
from tools.behavioral_eval_runner.tests.test_calibration_provider import ProviderCase


class TestBoundaryCorrections(DriverCase):
    def test_competing_driver_process_makes_zero_transport_calls(self):
        from dataclasses import asdict
        driver = self._driver()
        code = '''import json, sys
from tools.behavioral_eval_runner.judge import calibration_development_driver as d
from tools.behavioral_eval_runner.judge.calibration_errors import CalibrationLedgerError
from tools.behavioral_eval_runner.tests.test_calibration_provider import FakeSdkClient, FAKE_EXCEPTIONS
config = json.loads(sys.argv[2])
sdk = FakeSdkClient([])
driver = d.Wp2b3DevelopmentDriver(verified_root=d.verify_evidence_root(sys.argv[1]),
    expected_artifacts=d.ApprovedArtifactIdentity(**config['identity']),
    audited_head_sha=config['head'], current_head_sha=config['head'],
    audited_tree_sha=config['tree'], current_tree_sha=config['tree'])
try:
    driver.execute_development(sdk_client=sdk, exception_types=FAKE_EXCEPTIONS,
        declare_first_segment=False, started_utc='2026-09-10T00:00:00Z')
except CalibrationLedgerError:
    print('BLOCKED', len(sdk.responses.calls))
'''
        config = json.dumps(dict(identity=asdict(driver.expected_artifacts),
                                 head=driver.audited_head_sha, tree=driver.audited_tree_sha))
        script = self._script_for_order(drv.development_run_order(self.dataset))
        first = script[0]
        def competing_process(kwargs):
            result = subprocess.run([sys.executable, '-B', '-c', code, self.root, config],
                                    capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), 'BLOCKED 0')
            return first
        script[0] = competing_process
        driver.execute_development(sdk_client=FakeSdkClient(script), exception_types=FAKE_EXCEPTIONS,
            declare_first_segment=True, started_utc='2026-09-10T00:00:00Z', owner_stop_after_items=1)
        cl.verify_ledger_chain(drv.canonical_ledger_path(driver.verified_root))

    def test_interrupted_manifest_commit_recovers_existing_genesis(self):
        driver = self._driver()
        driver.prepare()
        with patch.object(drv.os, 'replace', side_effect=OSError('injected rename failure')):
            with self.assertRaises(OSError):
                driver.create_genesis(started_utc='2026-09-10T00:00:00Z')
        resumed = self._driver()
        resumed.prepare()
        resumed.reopen()
        self.assertEqual(sum(e['event_kind'] == 'GENESIS' for e in self._ledger_events()), 1)

    def test_pending_manifest_cannot_reset_execution_history(self):
        driver = self._driver()
        driver.prepare()
        driver.create_genesis(started_utc='2026-09-10T00:00:00Z')
        driver.open_development_segment()
        manifest = drv.canonical_manifest_path(driver.verified_root)
        os.rename(manifest, manifest + '.pending')
        resumed = self._driver()
        resumed.prepare()
        with self.assertRaisesRegex(CalibrationLedgerError, 'execution evidence'):
            resumed.reopen()

    def test_frozen_dataset_membership_and_mutated_item(self):
        from dataclasses import replace
        from tools.behavioral_eval_runner.canonical import sha256_of_obj
        payload = cg.HoldoutFreezeArtifact.example_dict()
        payload['frozen_sha256']['dataset'] = self.dataset.dataset_sha256()
        payload['freeze_contract_sha256'] = cg.freeze_contract_sha256(payload)
        artifact = cg.HoldoutFreezeArtifact.from_dict(payload)
        with patch.object(cg, 'APPROVED_HOLDOUT_FREEZE_SHA256', sha256_of_obj(artifact.to_dict())):
            freeze = cg.authorize_holdout_access(freeze_artifact=artifact, dataset=self.dataset)
            items = cd.holdout_items(self.dataset, freeze)
            self.assertEqual(len(items), 120)
            cd.CalibrationItemContent.from_item(items[0], holdout_authorization=freeze)
            changed = replace(items[0], transcript=items[0].transcript + ' changed')
            with self.assertRaises(HoldoutAccessError):
                cd.CalibrationItemContent.from_item(changed, holdout_authorization=freeze)
        with self.assertRaises(HoldoutAccessError):
            cd.holdout_items(self.dataset, freeze)

    def test_direct_genesis_respects_execution_lock(self):
        from tools.behavioral_eval_runner.judge.calibration_io import exclusive_lock
        driver = self._driver()
        driver.prepare()
        with exclusive_lock(os.path.join(self.root, 'wp2b3-execution.lock')):
            with self.assertRaises(CalibrationLedgerError):
                driver.create_genesis(started_utc='2026-09-10T00:00:00Z')
        self.assertFalse(os.path.exists(drv.canonical_ledger_path(driver.verified_root)))

    def test_reservation_denial_records_cap_stop_and_closes_segment(self):
        driver = self._driver()
        from tools.behavioral_eval_runner.judge.calibration_errors import CalibrationReservationDenied
        with patch.object(cl, 'MAX_METADATA_REQUESTS', 0):
            with self.assertRaises(CalibrationReservationDenied):
                driver.execute_development(sdk_client=FakeSdkClient([]), exception_types=FAKE_EXCEPTIONS,
                    declare_first_segment=True, started_utc='2026-09-10T00:00:00Z')
        events = self._ledger_events()
        stop = next(e for e in events if e['event_kind'] == 'RUN_STATE_TRANSITION')
        self.assertEqual(stop['run_state'], cl.RUN_STATE_STOPPED)
        self.assertEqual(stop['reason'], 'CAP_WOULD_BE_EXCEEDED')
        self.assertEqual(events[-1]['event_kind'], 'ACTIVE_SEGMENT_END')
        self.assertEqual(driver.ledger.cumulative().total_external_requests, 0)

    def test_freeze_does_not_authorize_an_unbound_dataset(self):
        from tools.behavioral_eval_runner.canonical import sha256_of_obj
        artifact = cg.HoldoutFreezeArtifact.from_dict(cg.HoldoutFreezeArtifact.example_dict())
        with patch.object(cg, 'APPROVED_HOLDOUT_FREEZE_SHA256', sha256_of_obj(artifact.to_dict())):
            freeze = cg.authorize_holdout_access(freeze_artifact=artifact)
            with self.assertRaises(HoldoutAccessError):
                cd.holdout_items(self.dataset, freeze)

    def test_changed_freeze_is_rejected_after_issuance(self):
        from tools.behavioral_eval_runner.canonical import sha256_of_obj
        artifact = cg.HoldoutFreezeArtifact.from_dict(cg.HoldoutFreezeArtifact.example_dict())
        with patch.object(cg, 'APPROVED_HOLDOUT_FREEZE_SHA256', sha256_of_obj(artifact.to_dict())):
            freeze = cg.authorize_holdout_access(freeze_artifact=artifact)
            artifact.frozen_sha256['dataset'] = 'a' * 64
            with self.assertRaises((HoldoutAccessError, SchemaValidationError)):
                cd.holdout_items(self.dataset, freeze)

    def test_live_identity_mismatch_stops_before_evidence_access(self):
        with patch.object(drv, '_resolve_repo_identity', return_value=('c' * 40, 'd' * 40)), patch.object(drv, 'verify_evidence_root', side_effect=AssertionError('evidence touched')):
            with self.assertRaises(CalibrationAuthorizationError):
                drv.execute_development_live(audited_head_sha='a' * 40, audited_tree_sha='b' * 40, declare_first_segment=True)

    def test_competing_execution_process_cannot_enter(self):
        from tools.behavioral_eval_runner.judge.calibration_io import exclusive_lock
        path = drv._canonical_path(drv.verify_evidence_root(self.root), 'wp2b3-execution.lock')
        code = '''import sys
from tools.behavioral_eval_runner.judge.calibration_io import exclusive_lock
from tools.behavioral_eval_runner.judge.calibration_errors import CalibrationLedgerError
try:
    with exclusive_lock(sys.argv[1]):
        print('ENTERED')
except CalibrationLedgerError:
    print('BLOCKED')
'''
        with exclusive_lock(path):
            result = subprocess.run([sys.executable, '-B', '-c', code, path], capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), 'BLOCKED')

    def test_status_rejects_unrelated_approval(self):
        from tools.behavioral_eval_runner.cli import _cmd_calibration_status
        output = io.StringIO()
        with redirect_stdout(output):
            _cmd_calibration_status(argparse.Namespace(
                approval=os.path.join(self.root, *drv.APPROVAL_ARTIFACT_RELPATH.split('/'))))
        self.assertEqual(json.loads(output.getvalue())['owner_label_approval'], 'PENDING')

    def test_status_checks_each_identity_field_and_file_hash_independently(self):
        from dataclasses import replace
        from tools.behavioral_eval_runner.cli import _cmd_calibration_status

        cases = [("matching synthetic pin", self.identity, "APPROVED")]
        for field, value in (
            ("dataset_id", "unrelated-dataset"),
            ("dataset_version", "unrelated-version"),
            ("dataset_semantic_sha256", "0" * 64),
            ("split_map_sha256", "0" * 64),
            ("labeling_guide_sha256", "0" * 64),
            ("approval_artifact_sha256", "0" * 64),
        ):
            self.assertNotEqual(getattr(self.identity, field), value)
            cases.append((field, replace(self.identity, **{field: value}), "PENDING"))
        for name, expected, status in cases:
            with self.subTest(binding=name):
                output = io.StringIO()
                with patch.object(drv, "PRODUCTION_APPROVED_ARTIFACTS", expected), redirect_stdout(output):
                    _cmd_calibration_status(argparse.Namespace(
                        approval=os.path.join(self.root, *drv.APPROVAL_ARTIFACT_RELPATH.split("/"))))
                report = json.loads(output.getvalue())
                self.assertEqual(report["owner_label_approval"], status)
                self.assertFalse(report["provider_dispatch_allowed"])
                self.assertEqual(report["provider_calls_made_by_this_command"], 0)

    def test_interrupted_genesis_can_recover_without_reset(self):
        driver = self._driver()
        driver.prepare()
        with patch.object(drv, 'CalibrationLedger', side_effect=OSError('injected initialization crash')):
            with self.assertRaises(OSError):
                driver.create_genesis(started_utc='2026-09-10T00:00:00Z')
        resumed = self._driver()
        resumed.prepare()
        resumed.reopen()
        events = self._ledger_events()
        self.assertEqual(sum(e['event_kind'] == 'GENESIS' for e in events), 1)
        self.assertEqual(resumed.ledger.cumulative().total_external_requests, 0)

    def test_child_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as outside:
            link = os.path.join(self.root, 'runs')
            try:
                os.symlink(outside, link, target_is_directory=True)
            except OSError as exc:
                self.skipTest(f'symlink creation unavailable: {exc}')
            with self.assertRaises(CalibrationAuthorizationError):
                drv.canonical_ledger_path(drv.verify_evidence_root(self.root))

    def test_child_traversal_is_rejected(self):
        verified = drv.verify_evidence_root(self.root)
        with self.assertRaises(CalibrationAuthorizationError):
            drv._canonical_path(verified, '../outside.json')

    def test_dataset_rejects_non_boolean_values(self):
        payload = next(i for i in self.dataset.items if i.adversarial).to_dict()
        for value in ('false', 1, 0, None, [], {}):
            with self.subTest(value=value):
                payload['adversarial'] = value
                with self.assertRaisesRegex(SchemaValidationError, 'adversarial must be bool'):
                    cd.CandidateItem.from_dict(payload)

    def test_direct_judgments_require_metadata_success(self):
        driver = self._driver()
        driver.prepare()
        driver.create_genesis(started_utc='2026-09-10T00:00:00Z')
        driver.open_development_segment()
        sdk = FakeSdkClient(self._script_for_order(drv.development_run_order(self.dataset)))
        with self.assertRaisesRegex(CalibrationStopError, 'METADATA_OK'):
            driver.run_development_judgments(sdk_client=sdk, exception_types=FAKE_EXCEPTIONS)
        self.assertEqual(driver.ledger.cumulative().total_external_requests, 0)

    def test_invalid_stop_limit_has_no_side_effect(self):
        for limit in (0, -1, True, 1.5, '1'):
            with self.subTest(limit=limit):
                driver = self._driver()
                sdk = FakeSdkClient([])
                with patch.object(driver, 'prepare', side_effect=AssertionError('invalid limit reached prepare')), self.assertRaisesRegex(SchemaValidationError, 'owner_stop_after_items'):
                    driver.execute_development(
                        sdk_client=sdk, exception_types=FAKE_EXCEPTIONS,
                        declare_first_segment=True, started_utc='2026-09-10T00:00:00Z',
                        owner_stop_after_items=limit,
                    )
                self.assertFalse(os.path.exists(drv.canonical_manifest_path(driver.verified_root)))

    def test_live_signature_does_not_accept_asserted_current_identity_or_test_roots(self):
        parameters = inspect.signature(drv.execute_development_live).parameters
        for name in ('current_head_sha', 'current_tree_sha', 'repo_root',
                     '_root_override_for_offline_tests', '_expected_artifacts_override_for_offline_tests'):
            self.assertNotIn(name, parameters)

    def test_posix_stat_without_windows_attributes_is_supported(self):
        real_stat = os.lstat
        class PosixStat:
            def __init__(self, value):
                self.st_mode = value.st_mode
                self.st_dev = value.st_dev
                self.st_ino = value.st_ino
        with patch.object(drv.os, 'lstat', side_effect=lambda p: PosixStat(real_stat(p))):
            drv._refuse_reparse_ancestors(self.root)

    def test_example_freeze_cannot_authorize_holdout(self):
        artifact = cg.HoldoutFreezeArtifact.from_dict(cg.HoldoutFreezeArtifact.example_dict())
        with self.assertRaises(HoldoutAccessError):
            cg.authorize_holdout_access(freeze_artifact=artifact)


class TestDeadlineBoundaries(unittest.TestCase):
    def test_hardlinked_evidence_is_rejected(self):
        from tools.behavioral_eval_runner.judge.calibration_io import checked_open
        with tempfile.TemporaryDirectory() as root:
            path = os.path.join(root, 'evidence')
            alias = os.path.join(root, 'alias')
            with open(path, 'w') as handle:
                handle.write('original')
            os.link(path, alias)
            with self.assertRaises(CalibrationAuthorizationError):
                with checked_open(alias, 'w'):
                    self.fail('hardlink exposed')
            with open(path) as handle:
                self.assertEqual(handle.read(), 'original')

    def test_hash_consistent_invalid_genesis_and_sequence_are_rejected(self):
        from tools.behavioral_eval_runner.canonical import sha256_of_obj
        with tempfile.TemporaryDirectory() as root:
            path = os.path.join(root, 'ledger.jsonl')
            for kind, seq in [('SEGMENT_OPENED', 1), ('GENESIS', 2), ('GENESIS', True)]:
                with self.subTest(kind=kind, seq=seq):
                    event = dict(event_kind=kind, event_seq=seq, run_id='seg-test',
                                 prev_event_sha256='', work_package='wrong',
                                 authorization_id='wrong', declared_first_segment=True)
                    event['event_sha256'] = sha256_of_obj(event)
                    with open(path, 'w') as handle:
                        handle.write(json.dumps(event) + '\n')
                    with self.assertRaises(CalibrationLedgerError):
                        cl.verify_ledger_chain(path)

    def test_mount_component_is_rejected(self):
        from tools.behavioral_eval_runner.judge import calibration_io as cio
        with tempfile.TemporaryDirectory() as root:
            with patch.object(cio.os.path, 'ismount', side_effect=lambda p: p == root):
                with self.assertRaises(CalibrationAuthorizationError):
                    cio.check_path(os.path.join(root, 'evidence'))

    def test_rejected_open_does_not_truncate_existing_evidence(self):
        from tools.behavioral_eval_runner.judge import calibration_io as cio
        with tempfile.TemporaryDirectory() as root:
            path = os.path.join(root, 'evidence.txt')
            with open(path, 'w') as handle:
                handle.write('preserve evidence')
            with patch.object(cio, 'check_path', side_effect=[None, CalibrationAuthorizationError('changed target')]):
                with self.assertRaises(CalibrationAuthorizationError):
                    with cio.checked_open(path, 'w'):
                        self.fail('unsafe handle exposed')
            with open(path) as handle:
                self.assertEqual(handle.read(), 'preserve evidence')

    def test_stale_ledger_writer_cannot_reserve(self):
        with tempfile.TemporaryDirectory() as root:
            path = os.path.join(root, 'ledger.jsonl')
            first = cl.CalibrationLedger(path, declare_first_segment=True)
            second = cl.CalibrationLedger(path)
            with self.assertRaises(CalibrationLedgerError):
                first.reserve(kind=cl.RequestKind.METADATA, logical_judgment_id=None,
                              attempt_number=1, estimated_input_tokens=0,
                              max_output_tokens=0, day='2026-09-10',
                              dataset_sha256=None, stage='DEVELOPMENT')
            self.assertGreater(cl.verify_ledger_chain(path), 0)

    def test_stage_deadline_before_at_after(self):
        for elapsed in (5399, 5400, 5401):
            with self.subTest(elapsed=elapsed):
                ledger = cl.CalibrationLedger(None)
                ledger.begin_active_segment('DEVELOPMENT', 0)
                if elapsed < 5400:
                    ledger.check_deadlines('DEVELOPMENT', elapsed)
                else:
                    with self.assertRaises(CalibrationStopError):
                        ledger.check_deadlines('DEVELOPMENT', elapsed)

    def test_whole_run_exact_deadline(self):
        ledger = cl.CalibrationLedger(None)
        ledger.begin_active_segment('DEVELOPMENT', 0)
        ledger.end_active_segment(21600)
        with self.assertRaises(CalibrationStopError):
            ledger.check_deadlines('SEALED_HOLDOUT', 21600)


class TestDirectProviderBoundary(ProviderCase):
    SEED_METADATA = False
    def test_provider_cannot_bypass_metadata(self):
        from tools.behavioral_eval_runner.tests.test_calibration_provider import fake_response
        client = self._client([fake_response(self._valid_raw())])
        with self.assertRaisesRegex(CalibrationStopError, 'METADATA_OK'):
            client.dispatch(self.request, self.envelope_bytes)
        self.assertEqual(self.ledger.cumulative().attempts_total, 0)


class TestSharedProviderConcurrency(ProviderCase):
    def test_direct_provider_stop_is_durable_and_prevents_continuation(self):
        from tools.behavioral_eval_runner.tests.test_calibration_provider import FakeStatusError, fake_response
        client = self._client([FakeStatusError(401), fake_response(self._valid_raw())])
        with self.assertRaises(CalibrationStopError):
            client.dispatch(self.request, self.envelope_bytes)
        self.assertEqual(self.ledger.current_run_state(), cl.RUN_STATE_STOPPED)
        with self.assertRaises(CalibrationStopError):
            client.dispatch(self.request, self.envelope_bytes)
        self.assertEqual(len(client._sdk.responses.calls), 1)
        reopened = cl.CalibrationLedger(self.ledger_path)
        self.assertEqual(reopened.current_run_state(), cl.RUN_STATE_STOPPED)

    def test_terminal_run_states_block_direct_transport(self):
        from tools.behavioral_eval_runner.tests.test_calibration_provider import fake_response
        for state in (cl.RUN_STATE_STOPPED, cl.RUN_STATE_OWNER_WAIT):
            with self.subTest(state=state):
                ledger, path = self._durable_ledger()
                self.ledger = ledger
                ledger.record_run_state(state)
                client = self._client([fake_response(self._valid_raw())])
                with self.assertRaises(CalibrationStopError):
                    client.dispatch(self.request, self.envelope_bytes)
                self.assertEqual(client._sdk.responses.calls, [])

    def test_direct_transport_requires_open_active_segment(self):
        from tools.behavioral_eval_runner.tests.test_calibration_provider import fake_response
        # Close any fixture segment; a direct call must not escape accounting.
        if any(segment[2] is None for segment in self.ledger._segments):
            self.ledger.end_active_segment(time.time())
        client = self._client([fake_response(self._valid_raw())])
        with self.assertRaises(CalibrationStopError):
            client.dispatch(self.request, self.envelope_bytes)
        self.assertEqual(client._sdk.responses.calls, [])

    def test_two_clients_cannot_overlap_transport(self):
        from tools.behavioral_eval_runner.tests.test_calibration_provider import fake_response
        other = self._client([fake_response(self._valid_raw())])
        def attempt_overlap(kwargs):
            with self.assertRaises(CalibrationStopError):
                other.dispatch(self.request, self.envelope_bytes)
            return fake_response(self._valid_raw())
        client = self._client([attempt_overlap])
        client.dispatch(self.request, self.envelope_bytes)
        self.assertEqual(other._sdk.responses.calls, [])
