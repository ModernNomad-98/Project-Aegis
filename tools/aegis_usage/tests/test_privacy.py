"""Privacy tests: default off, allowlist minimization, bounds and offline behavior."""

import copy
import importlib.util
import json
import re
import socket
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.aegis_usage import aggregate, local_report  # noqa: E402

S = local_report
START = "2026-01-05"
ADMISSION = "adm-" + "a" * 32
DATE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
REF = re.compile(r"^(wf|exp|adm|evt|crit)-[0-9a-f]{32}$")


def enrolled_store(stages=None):
    store = S.new_store()
    workflow = S.enable_capture(store, day="2026-01-06", start_day=START, applicable_stages=stages)
    S.record_transition(store, workflow["workflow_ref"], kind="observation", value="ongoing", effective_day=START)
    workflow["admission_ref"] = ADMISSION
    return store, workflow["workflow_ref"]


class DefaultOffTests(unittest.TestCase):
    def test_nothing_is_captured_without_opt_in(self):
        store = S.new_store()
        with self.assertRaises(S.ContractError) as caught:
            S.record_transition(store, "wf-" + "1" * 32, kind="observation", value="ongoing", effective_day=START)
        self.assertEqual(caught.exception.code, "capture_disabled")
        self.assertEqual(store["workflows"], {})

    def test_consent_is_per_workflow(self):
        store = S.new_store()
        first = S.enable_capture(store, day="2026-01-06", start_day=START)
        second = S.enable_capture(store, day="2026-01-06", start_day=START)
        S.disable_capture(store, second["workflow_ref"])
        S.record_transition(store, first["workflow_ref"], kind="observation", value="ongoing", effective_day=START)
        with self.assertRaises(S.ContractError) as caught:
            S.record_transition(store, second["workflow_ref"], kind="observation", value="ongoing", effective_day=START)
        self.assertEqual(caught.exception.code, "capture_disabled")

    def test_opt_out_stops_capture(self):
        store, ref = enrolled_store()
        S.disable_capture(store, ref)
        with self.assertRaises(S.ContractError) as caught:
            S.record_transition(store, ref, kind="stage", value="complete", effective_day=START, stage="build")
        self.assertEqual(caught.exception.code, "capture_disabled")


class AllowlistTests(unittest.TestCase):
    def test_export_has_exactly_the_allowlisted_keys(self):
        store, ref = enrolled_store()
        envelope = S.build_envelope(store, ref)
        self.assertEqual(tuple(envelope), S.TOP_KEYS)
        self.assertEqual(tuple(envelope["snapshot"]), S.SNAPSHOT_KEYS)
        self.assertEqual(tuple(envelope["snapshot"]["transitions"][0]), S.TRANSITION_KEYS)
        self.assertEqual(tuple(envelope["snapshot"]["stage_status"]), S.STAGES)

    def test_every_string_is_an_enum_a_day_or_a_reference(self):
        store, ref = enrolled_store()
        S.record_transition(store, ref, kind="stage", value="complete", effective_day="2026-01-08", stage="build")
        envelope = S.build_envelope(store, ref)

        def walk(node, path=""):
            if isinstance(node, dict):
                for key, value in node.items():
                    walk(value, path + "." + key)
            elif isinstance(node, list):
                for index, item in enumerate(node):
                    walk(item, path + "[" + str(index) + "]")
            elif isinstance(node, str):
                allowed = (
                    DATE.fullmatch(node)
                    or REF.fullmatch(node)
                    or node in S.STAGES
                    or node in S.STAGE_STATUSES
                    or node in S.STATUSES
                    or node in S.ACCEPTANCE
                    or node in S.ACCEPTANCE_EVIDENCE
                    or node in S.EVENT_KINDS
                    or node in S.SUPPORTED_LIBRARY_REVISIONS
                    or node in S.SUPPORTED_CONSENT_POLICIES
                    or node == S.SCHEMA_NAME
                    or node == S.CAPTURE_TIER
                )
                self.assertTrue(allowed, "unexpected free text at " + path + ": " + node)

        walk(envelope)

    def test_nested_forbidden_fields_are_rejected_with_a_loud_code(self):
        store, ref = enrolled_store()
        baseline = S.build_envelope(store, ref)
        cases = [
            ("snapshot", "project_name"),
            ("snapshot", "repository"),
            ("snapshot", "prompt"),
            ("snapshot", "file_path"),
            ("snapshot", "content_sha256"),
            ("snapshot", "account_id"),
        ]
        for parent, field in cases:
            with self.subTest(field=field):
                payload = copy.deepcopy(baseline)
                payload[parent][field] = "leak"
                with self.assertRaises(S.ContractError) as caught:
                    S.validate_envelope(payload)
                self.assertEqual(caught.exception.code, "forbidden_field")
                self.assertIn(field, caught.exception.path)

    def test_forbidden_field_inside_a_transition_is_rejected(self):
        payload = S.build_envelope(*enrolled_store())
        payload["snapshot"]["transitions"][0]["user"] = "someone"
        with self.assertRaises(S.ContractError) as caught:
            S.validate_envelope(payload)
        self.assertEqual(caught.exception.code, "forbidden_field")

    def test_export_contains_no_identity_path_or_url_tokens(self):
        store, ref = enrolled_store()
        S.record_transition(store, ref, kind="stage", value="complete", effective_day="2026-01-08", stage="build")
        payload = S.preview_export(store, ref)[0].decode("utf-8")
        for token in ("@", "://", "C:\\", "/Users/", "http", "github", ".com", "sha256"):
            self.assertNotIn(token, payload)

    def test_references_are_random_pseudonyms_not_derived_from_the_start(self):
        first = S.enable_capture(S.new_store(), day="2026-01-06", start_day=START)
        second = S.enable_capture(S.new_store(), day="2026-01-06", start_day=START)
        self.assertNotEqual(first["workflow_ref"], second["workflow_ref"])
        self.assertNotEqual(first["criteria_contract_ref"], second["criteria_contract_ref"])
        for workflow in (first, second):
            self.assertRegex(workflow["workflow_ref"], REF)
            self.assertRegex(workflow["criteria_contract_ref"], REF)
            self.assertNotIn("2026", workflow["workflow_ref"])
            self.assertNotIn("2026", workflow["criteria_contract_ref"])

    def test_event_references_are_random(self):
        store, ref = enrolled_store()
        first = S.record_transition(store, ref, kind="stage", value="in_progress", effective_day="2026-01-06", stage="build")
        second = S.record_transition(store, ref, kind="stage", value="in_progress", effective_day="2026-01-06", stage="plan")
        self.assertNotEqual(first["event_ref"], second["event_ref"])
        self.assertRegex(first["event_ref"], REF)


class OfflineTests(unittest.TestCase):
    def test_modules_import_no_network_or_process_machinery(self):
        forbidden = ("import socket", "import urllib", "import http", "import requests", "import subprocess", "import threading", "from socket", "from urllib", "from http")
        for name in ("local_report.py", "aggregate.py"):
            source = (REPO_ROOT / "tools" / "aegis_usage" / name).read_text(encoding="utf-8")
            for token in forbidden:
                self.assertNotIn(token, source, name + " imports " + token)

    def test_no_network_call_is_made_during_preview_export_import_or_report(self):
        store, ref = enrolled_store()
        payload, digest = S.preview_export(store, ref)
        central = aggregate.new_store()
        notice = {
            "workflow_ref": ref,
            "start_day": START,
            "applicable_stages": list(S.STAGES),
            "criteria_frozen_before_work": True,
            "criteria_contract_ref": store["workflows"][ref]["criteria_contract_ref"],
        }
        admission = aggregate.issue_admission(central, notice, issued_day="2026-01-06")
        store["workflows"][ref]["admission_ref"] = admission["admission_ref"]
        payload = S.preview_export(store, ref)[0]
        with mock.patch.object(socket, "socket", side_effect=AssertionError("network use")):
            with mock.patch.object(socket, "create_connection", side_effect=AssertionError("network use")):
                with tempfile.TemporaryDirectory() as folder:
                    target = Path(folder) / "export.json"
                    digest = S.bytes_sha256(payload)
                    S.export_snapshot(store, ref, target, preview_sha256=digest, confirm=True)
                    aggregate.import_export(central, target.read_bytes(), capability=admission["capability"], receipt_day="2026-01-07")
                    aggregate.compute_report(central, as_of="2026-02-20")
                    aggregate.publishable_report(aggregate.compute_report(central, as_of="2026-02-20"))
        self.assertEqual(digest, S.bytes_sha256(payload))

    def test_preview_writes_nothing(self):
        store, ref = enrolled_store()
        with tempfile.TemporaryDirectory() as folder:
            before = set(Path(folder).iterdir())
            S.preview_export(store, ref)
            self.assertEqual(set(Path(folder).iterdir()), before)

    def test_size_bound_rejects_oversize_input(self):
        with self.assertRaises(S.ContractError) as caught:
            S.loads_strict(b'{"x":"' + b"y" * (S.MAX_SNAPSHOT_BYTES + 1) + b'"}')
        self.assertEqual(caught.exception.code, "oversize")
        self.assertEqual(S.MAX_SNAPSHOT_BYTES, 65536)


class MutantDetectionTests(unittest.TestCase):
    def load_mutant(self, source_name, replacements):
        source_path = REPO_ROOT / "tools" / "aegis_usage" / source_name
        source = source_path.read_text(encoding="utf-8")
        for old, new in replacements:
            self.assertIn(old, source, "mutation anchor missing: " + old)
            source = source.replace(old, new, 1)
        folder = tempfile.mkdtemp(prefix="aegis-privacy-mutant-")
        target = Path(folder) / ("mutant_" + source_name)
        target.write_text(source, encoding="utf-8", newline="\n")
        spec = importlib.util.spec_from_file_location(
            "privacy_mutant_" + source_name.replace(".py", "") + "_" + str(id(target)), target
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_mutant_without_the_allowlist_accepts_a_forbidden_nested_field(self):
        payload = S.build_envelope(*enrolled_store())
        payload["snapshot"]["project_name"] = "a consumer project"
        with self.assertRaises(S.ContractError) as caught:
            S.validate_envelope(payload)
        self.assertEqual(caught.exception.code, "forbidden_field")
        mutant = self.load_mutant(
            "local_report.py",
            [
                ("extra = sorted(set(node) - set(allowed))", "extra = []"),
                ('if str(key).lower() in FORBIDDEN_KEYS:', "if False:"),
            ],
        )
        self.assertIsNotNone(mutant.validate_envelope(payload))
        self.assertNotEqual(mutant.MAX_SNAPSHOT_BYTES, S.MAX_SNAPSHOT_BYTES * 2)

    def test_mutant_with_a_raised_size_bound_accepts_an_oversize_payload(self):
        oversized = b'{"x":"' + b"y" * (S.MAX_SNAPSHOT_BYTES + 1) + b'"}'
        with self.assertRaises(S.ContractError) as caught:
            S.loads_strict(oversized)
        self.assertEqual(caught.exception.code, "oversize")
        mutant = self.load_mutant(
            "local_report.py",
            [("MAX_SNAPSHOT_BYTES = 64 * 1024", "MAX_SNAPSHOT_BYTES = 64 * 1024 * 1024")],
        )
        self.assertIsNotNone(mutant.loads_strict(oversized))


if __name__ == "__main__":
    unittest.main()
