"""Contract tests: versioned schema, strict allowlist, epochs, dedupe and revisions."""

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.aegis_usage import aggregate, local_report  # noqa: E402

S = local_report
START = "2026-01-05"
ADMISSION = "adm-" + "a" * 32


def enrolled_store(stages=None):
    store = S.new_store()
    workflow = S.enable_capture(store, day="2026-01-06", start_day=START, applicable_stages=stages)
    S.record_transition(store, workflow["workflow_ref"], kind="observation", value="ongoing", effective_day=START)
    workflow["admission_ref"] = ADMISSION
    return store, workflow["workflow_ref"]


def valid_envelope(stages=None):
    store, ref = enrolled_store(stages)
    return S.build_envelope(store, ref)


class ContractValidationTests(unittest.TestCase):
    def assertCode(self, payload, code):
        with self.assertRaises(S.ContractError) as caught:
            S.validate_envelope(payload)
        self.assertEqual(caught.exception.code, code, caught.exception.message)
        return caught.exception

    def test_default_store_captures_nothing(self):
        store = S.new_store()
        self.assertEqual(store["opt_ins"], {})
        with self.assertRaises(S.ContractError) as caught:
            S.record_transition(store, "wf-" + "0" * 32, kind="observation", value="ongoing", effective_day=START)
        self.assertEqual(caught.exception.code, "capture_disabled")

    def test_opt_in_then_record_and_export(self):
        store, ref = enrolled_store()
        envelope = S.build_envelope(store, ref)
        self.assertEqual(envelope["schema"], S.SCHEMA_NAME)
        self.assertEqual(envelope["snapshot"]["revision"], 1)
        self.assertEqual(envelope["snapshot"]["status"], "ongoing")

    def test_preview_is_exact_export_bytes(self):
        store, ref = enrolled_store()
        payload, digest = S.preview_export(store, ref)
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "export.json"
            result = S.export_snapshot(store, ref, target, preview_sha256=digest, confirm=True)
            self.assertEqual(target.read_bytes(), payload)
            self.assertEqual(result["sha256"], digest)
            self.assertEqual(S.bytes_sha256(target.read_bytes()), digest)

    def test_export_requires_fresh_confirmation(self):
        store, ref = enrolled_store()
        _, digest = S.preview_export(store, ref)
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "export.json"
            with self.assertRaises(S.ContractError) as caught:
                S.export_snapshot(store, ref, target, preview_sha256=digest, confirm=False)
            self.assertEqual(caught.exception.code, "confirmation_required")
            self.assertFalse(target.exists())

    def test_export_requires_matching_preview_handle(self):
        store, ref = enrolled_store()
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "export.json"
            with self.assertRaises(S.ContractError) as caught:
                S.export_snapshot(store, ref, target, preview_sha256="0" * 64, confirm=True)
            self.assertEqual(caught.exception.code, "preview_mismatch")
            self.assertFalse(target.exists())

    def test_export_refuses_repository_path(self):
        store, ref = enrolled_store()
        _, digest = S.preview_export(store, ref)
        target = REPO_ROOT / "tools" / "aegis_usage" / "would-be-export.json"
        with self.assertRaises(S.ContractError) as caught:
            S.export_snapshot(store, ref, target, preview_sha256=digest, confirm=True, repo_root=REPO_ROOT)
        self.assertEqual(caught.exception.code, "export_path_in_repository")
        self.assertFalse(target.exists())

    def test_export_refuses_tool_tree_even_without_a_git_marker(self):
        store, ref = enrolled_store()
        _, digest = S.preview_export(store, ref)
        target = REPO_ROOT / "tools" / "aegis_usage" / "would-be-archive-export.json"
        with self.assertRaises(S.ContractError) as caught:
            S.export_snapshot(
                store,
                ref,
                target,
                preview_sha256=digest,
                confirm=True,
                repo_root=Path(tempfile.gettempdir()) / "definitely-not-a-repository",
            )
        self.assertEqual(caught.exception.code, "export_path_in_repository")
        self.assertFalse(target.exists())

    def test_unknown_schema_epoch_rejected(self):
        payload = valid_envelope()
        payload["schema"] = "workflow-outcomes-v2"
        self.assertCode(payload, "unsupported_schema")

    def test_host_recorded_tier_rejected(self):
        payload = valid_envelope()
        payload["capture_tier"] = "host_recorded"
        self.assertCode(payload, "unsupported_capture_tier")

    def test_unknown_library_revision_rejected(self):
        payload = valid_envelope()
        payload["library_revision"] = "9.9.9"
        self.assertCode(payload, "unknown_library_revision")

    def test_unknown_consent_policy_rejected(self):
        payload = valid_envelope()
        payload["consent_policy_version"] = "2"
        self.assertCode(payload, "unknown_consent_policy")

    def test_horizon_is_fixed(self):
        payload = valid_envelope()
        payload["reporting_window_days"] = 60
        self.assertCode(payload, "invalid_horizon")

    def test_top_level_unknown_field_rejected(self):
        payload = valid_envelope()
        payload["extra"] = "x"
        self.assertCode(payload, "unknown_field")

    def test_nested_unknown_field_rejected(self):
        payload = valid_envelope()
        payload["snapshot"]["stage_status"]["build_notes"] = "unknown"
        self.assertCode(payload, "unknown_field")

    def test_transition_unknown_field_rejected(self):
        payload = valid_envelope()
        payload["snapshot"]["transitions"][0]["note"] = "x"
        self.assertCode(payload, "forbidden_field")

    def test_invalid_enum_rejected(self):
        payload = valid_envelope()
        payload["snapshot"]["status"] = "maybe"
        self.assertCode(payload, "invalid_enum")

    def test_invalid_date_and_due_day_rejected(self):
        payload = valid_envelope()
        payload["snapshot"]["start_day"] = "2026-13-01"
        self.assertCode(payload, "invalid_date")
        payload = valid_envelope()
        payload["snapshot"]["report_due_day"] = "2026-02-05"
        self.assertCode(payload, "invalid_report_due_day")

    def test_report_due_day_is_start_plus_30(self):
        payload = valid_envelope()
        self.assertEqual(payload["snapshot"]["report_due_day"], "2026-02-04")

    def test_missing_field_rejected(self):
        payload = valid_envelope()
        del payload["snapshot"]["export_ref"]
        self.assertCode(payload, "missing_field")

    def test_derived_snapshot_mismatch_rejected(self):
        payload = valid_envelope()
        payload["snapshot"]["status"] = "delivered"
        payload["snapshot"]["delivery_day"] = "2026-01-09"
        self.assertCode(payload, "derived_mismatch")

    def test_applicability_conflict_rejected(self):
        payload = valid_envelope()
        payload["snapshot"]["applicable_stages"] = ["discover", "plan", "build", "deliver"]
        self.assertCode(payload, "applicability_conflict")

    def test_stage_event_for_inapplicable_stage_rejected(self):
        store, ref = enrolled_store(stages=["discover", "plan", "build", "deliver"])
        payload = S.build_envelope(store, ref)
        payload["snapshot"]["transitions"].append(
            {"event_ref": "evt-" + "b" * 32, "kind": "stage", "effective_day": START, "value": "complete", "stage": "validate"}
        )
        self.assertCode(payload, "stage_not_applicable")

    def test_event_before_start_rejected(self):
        payload = valid_envelope()
        payload["snapshot"]["transitions"][0]["effective_day"] = "2026-01-01"
        self.assertCode(payload, "event_before_start")

    def test_same_day_conflicting_terminal_rejected(self):
        payload = valid_envelope()
        payload["snapshot"]["last_observed_day"] = "2026-01-09"
        payload["snapshot"]["transitions"].extend(
            [
                {"event_ref": "evt-" + "c" * 32, "kind": "status", "effective_day": "2026-01-09", "value": "delivered", "stage": None},
                {"event_ref": "evt-" + "d" * 32, "kind": "status", "effective_day": "2026-01-09", "value": "failed", "stage": None},
            ]
        )
        self.assertCode(payload, "conflicting_terminal_same_day")

    def test_duplicate_event_ref_rejected(self):
        payload = valid_envelope()
        payload["snapshot"]["transitions"].append(copy.deepcopy(payload["snapshot"]["transitions"][0]))
        self.assertCode(payload, "duplicate_event_ref")

    def test_transition_bound_rejected(self):
        payload = valid_envelope()
        events = [
            {"event_ref": "evt-" + format(index, "032x"), "kind": "observation", "effective_day": START, "value": "ongoing", "stage": None}
            for index in range(257)
        ]
        payload["snapshot"]["transitions"] = events
        self.assertCode(payload, "too_many_transitions")

    def test_oversize_input_rejected_before_parsing(self):
        oversized = b'{"schema":"' + b"x" * (S.MAX_SNAPSHOT_BYTES + 1) + b'"}'
        with self.assertRaises(S.ContractError) as caught:
            S.loads_strict(oversized)
        self.assertEqual(caught.exception.code, "oversize")
        with self.assertRaises(S.ContractError) as caught:
            aggregate.import_export(aggregate.new_store(), oversized, capability="x", receipt_day=START)
        self.assertEqual(caught.exception.code, "oversize")

    def test_duplicate_json_key_rejected(self):
        raw = b'{"schema":"workflow-outcomes-v1","schema":"workflow-outcomes-v1"}'
        with self.assertRaises(S.ContractError) as caught:
            S.loads_strict(raw)
        self.assertEqual(caught.exception.code, "duplicate_key")

    def test_malformed_json_rejected(self):
        with self.assertRaises(S.ContractError) as caught:
            S.loads_strict(b"{not json")
        self.assertEqual(caught.exception.code, "malformed_json")

    def test_non_utf8_rejected(self):
        with self.assertRaises(S.ContractError) as caught:
            S.loads_strict(b"\xff\xfe{}")
        self.assertEqual(caught.exception.code, "invalid_encoding")

    def test_same_day_conflicting_acceptance_rejected_in_both_orders(self):
        for order in (
            ("self_reported_fail", "self_reported_pass"),
            ("self_reported_pass", "self_reported_fail"),
        ):
            payload = valid_envelope()
            payload["snapshot"]["last_observed_day"] = "2026-01-09"
            for index, value in enumerate(order):
                payload["snapshot"]["transitions"].append(
                    {
                        "event_ref": "evt-" + (("e" if index == 0 else "f") * 32),
                        "kind": "acceptance",
                        "effective_day": "2026-01-09",
                        "value": value,
                        "stage": None,
                    }
                )
            self.assertCode(payload, "conflicting_same_day_transition")

    def test_same_day_conflicting_stage_value_rejected(self):
        payload = valid_envelope()
        payload["snapshot"]["last_observed_day"] = "2026-01-09"
        payload["snapshot"]["transitions"].extend(
            [
                {"event_ref": "evt-" + "1" * 32, "kind": "stage", "effective_day": "2026-01-09", "value": "complete", "stage": "build"},
                {"event_ref": "evt-" + "2" * 32, "kind": "stage", "effective_day": "2026-01-09", "value": "in_progress", "stage": "build"},
            ]
        )
        self.assertCode(payload, "conflicting_same_day_transition")

    def test_same_day_same_value_is_not_a_conflict(self):
        payload = valid_envelope()
        payload["snapshot"]["last_observed_day"] = "2026-01-09"
        payload["snapshot"]["stage_status"]["build"] = "complete"
        payload["snapshot"]["transitions"].extend(
            [
                {"event_ref": "evt-" + "3" * 32, "kind": "stage", "effective_day": "2026-01-09", "value": "complete", "stage": "build"},
                {"event_ref": "evt-" + "4" * 32, "kind": "stage", "effective_day": "2026-01-09", "value": "complete", "stage": "build"},
            ]
        )
        self.assertIs(S.validate_envelope(payload), payload)

    def test_acceptance_evidence_defaults_to_none(self):
        store, ref = enrolled_store()
        S.record_transition(store, ref, kind="acceptance", value="self_reported_fail", effective_day="2026-01-09")
        self.assertEqual(S.build_envelope(store, ref)["snapshot"]["acceptance_evidence"], "none")

    def test_each_acceptance_evidence_value_is_exported_unchanged(self):
        for evidence in S.ACCEPTANCE_EVIDENCE:
            store, ref = enrolled_store()
            S.record_transition(
                store,
                ref,
                kind="acceptance",
                value="self_reported_pass",
                effective_day="2026-01-09",
                evidence=evidence,
            )
            envelope = S.build_envelope(store, ref)
            self.assertEqual(envelope["snapshot"]["acceptance_evidence"], evidence)

    def test_independent_attestation_requires_a_local_evidence_category(self):
        store, ref = enrolled_store()
        with self.assertRaises(S.ContractError) as caught:
            S.record_transition(
                store, ref, kind="acceptance", value="independent_attested_pass", effective_day="2026-01-09"
            )
        self.assertEqual(caught.exception.code, "evidence_required")
        S.record_transition(
            store,
            ref,
            kind="acceptance",
            value="independent_attested_pass",
            effective_day="2026-01-09",
            evidence="local_review_record",
        )
        self.assertEqual(S.build_envelope(store, ref)["snapshot"]["acceptance_evidence"], "local_review_record")

    def test_independent_attestation_without_evidence_is_rejected_by_validation(self):
        payload = valid_envelope()
        payload["snapshot"]["acceptance"] = "independent_attested_pass"
        payload["snapshot"]["acceptance_evidence"] = "none"
        self.assertCode(payload, "evidence_required")

    def test_unassessed_acceptance_cannot_carry_evidence(self):
        payload = valid_envelope()
        payload["snapshot"]["acceptance_evidence"] = "local_checklist"
        self.assertCode(payload, "invalid_evidence")

    def test_recorder_rejects_same_day_conflicting_acceptance(self):
        store, ref = enrolled_store()
        S.record_transition(store, ref, kind="acceptance", value="self_reported_fail", effective_day="2026-01-09")
        with self.assertRaises(S.ContractError) as caught:
            S.record_transition(store, ref, kind="acceptance", value="self_reported_pass", effective_day="2026-01-09")
        self.assertEqual(caught.exception.code, "conflicting_same_day_transition")
        self.assertEqual(len(store["workflows"][ref]["transitions"]), 2)

    def test_recorder_rejects_not_applicable_for_an_applicable_stage(self):
        store, ref = enrolled_store()
        with self.assertRaises(S.ContractError) as caught:
            S.record_transition(
                store, ref, kind="stage", value="not_applicable", effective_day=START, stage="build"
            )
        self.assertEqual(caught.exception.code, "applicability_conflict")
        self.assertEqual(len(store["workflows"][ref]["transitions"]), 1)

class ImportRevisionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.central = aggregate.new_store()
        store, ref = enrolled_store()
        self.store, self.ref = store, ref
        self.notice = {
            "workflow_ref": ref,
            "start_day": START,
            "applicable_stages": list(S.STAGES),
            "criteria_frozen_before_work": True,
            "criteria_contract_ref": store["workflows"][ref]["criteria_contract_ref"],
        }
        self.admission = aggregate.issue_admission(self.central, self.notice, issued_day="2026-01-06")
        self.store["workflows"][ref]["admission_ref"] = self.admission["admission_ref"]

    def tearDown(self):
        self.tmp.cleanup()

    def export(self):
        payload, _ = S.preview_export(self.store, self.ref)
        return payload

    def test_import_accepts_valid_export(self):
        result = aggregate.import_export(
            self.central, self.export(), capability=self.admission["capability"], receipt_day="2026-01-07"
        )
        self.assertEqual(result["status"], "accepted")
        self.assertTrue(result["prospective"])
        self.assertIn(self.ref, self.central["records"])

    def test_identical_duplicate_is_a_no_op(self):
        aggregate.import_export(self.central, self.export(), capability=self.admission["capability"], receipt_day="2026-01-07")
        before = json.dumps(self.central, sort_keys=True)
        result = aggregate.import_export(
            self.central, self.export(), capability=self.admission["capability"], receipt_day="2026-01-08"
        )
        self.assertEqual(result["status"], "duplicate")
        after = json.loads(json.dumps(self.central, sort_keys=True))
        self.assertEqual(before, json.dumps(after, sort_keys=True))
        self.assertEqual(after["records"][self.ref]["first_receipt_day"], "2026-01-07")

    def test_conflicting_same_revision_is_quarantined(self):
        aggregate.import_export(self.central, self.export(), capability=self.admission["capability"], receipt_day="2026-01-07")
        payload = S.build_envelope(self.store, self.ref)
        payload["snapshot"]["export_ref"] = "exp-" + "f" * 32
        result = aggregate.import_export(
            self.central, payload, capability=self.admission["capability"], receipt_day="2026-01-08"
        )
        self.assertEqual(result["status"], "quarantined")
        self.assertEqual(result["code"], "conflicting_revision")
        self.assertEqual(self.central["records"][self.ref]["export_ref"], self.store["workflows"][self.ref]["export_ref"])
        self.assertEqual(len(self.central["quarantine"]), 1)

    def test_lower_revision_is_ignored(self):
        aggregate.import_export(self.central, self.export(), capability=self.admission["capability"], receipt_day="2026-01-07")
        S.record_transition(self.store, self.ref, kind="stage", value="complete", effective_day="2026-01-08", stage="build")
        aggregate.import_export(self.central, self.export(), capability=self.admission["capability"], receipt_day="2026-01-09")
        stale = S.build_envelope(self.store, self.ref)
        stale["snapshot"]["revision"] = 1
        result = aggregate.import_export(
            self.central, stale, capability=self.admission["capability"], receipt_day="2026-01-10"
        )
        self.assertEqual(result["status"], "ignored")
        self.assertEqual(self.central["records"][self.ref]["revision"], 2)
        self.assertEqual(self.central["ignored"], 1)

    def test_higher_revision_updates(self):
        aggregate.import_export(self.central, self.export(), capability=self.admission["capability"], receipt_day="2026-01-07")
        S.record_transition(self.store, self.ref, kind="stage", value="complete", effective_day="2026-01-08", stage="build")
        result = aggregate.import_export(
            self.central, self.export(), capability=self.admission["capability"], receipt_day="2026-01-09"
        )
        self.assertEqual(result["status"], "updated")
        self.assertEqual(self.central["records"][self.ref]["revision"], 2)
        self.assertEqual(len(self.central["records"][self.ref]["transitions"]), 2)

    def test_higher_revision_cannot_change_enrollment(self):
        aggregate.import_export(self.central, self.export(), capability=self.admission["capability"], receipt_day="2026-01-07")
        before = self.central["records"][self.ref]["enrollment_fingerprint"]
        S.record_transition(self.store, self.ref, kind="stage", value="complete", effective_day="2026-01-08", stage="build")
        payload = S.build_envelope(self.store, self.ref)
        payload["snapshot"]["start_day"] = "2026-01-04"
        payload["snapshot"]["report_due_day"] = "2026-02-03"
        result = aggregate.import_export(
            self.central, payload, capability=self.admission["capability"], receipt_day="2026-01-09"
        )
        self.assertEqual(result["status"], "quarantined")
        self.assertEqual(result["code"], "enrollment_change")
        self.assertEqual(self.central["records"][self.ref]["enrollment_fingerprint"], before)
        self.assertEqual(self.central["records"][self.ref]["revision"], 1)

    def test_higher_revision_cannot_remove_history(self):
        aggregate.import_export(self.central, self.export(), capability=self.admission["capability"], receipt_day="2026-01-07")
        S.record_transition(self.store, self.ref, kind="stage", value="complete", effective_day="2026-01-08", stage="build")
        aggregate.import_export(self.central, self.export(), capability=self.admission["capability"], receipt_day="2026-01-09")
        payload = S.build_envelope(self.store, self.ref)
        payload["snapshot"]["revision"] = 3
        payload["snapshot"]["transitions"] = payload["snapshot"]["transitions"][1:]
        payload["snapshot"]["status"] = "unknown"
        payload["snapshot"]["stage_status"] = {
            "discover": "not_started",
            "plan": "not_started",
            "build": "complete",
            "validate": "not_started",
            "deliver": "not_started",
        }
        S.validate_envelope(payload)
        result = aggregate.import_export(
            self.central, payload, capability=self.admission["capability"], receipt_day="2026-01-10"
        )
        self.assertEqual(result["status"], "quarantined")
        self.assertEqual(result["code"], "history_rewrite")
        self.assertEqual(len(self.central["records"][self.ref]["transitions"]), 2)


class SchemaFileTests(unittest.TestCase):
    def schema(self):
        path = REPO_ROOT / "docs" / "instrumentation" / "workflow-outcomes-v1.schema.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def walk(self, node, path=""):
        if isinstance(node, dict):
            if node.get("type") == "object":
                self.assertIs(node.get("additionalProperties"), False, "object schema without additionalProperties=false at " + path)
                for key in node.get("required", []):
                    self.assertIn(key, node.get("properties", {}), "required field not declared at " + path)
            strings = node.get("type") == "string"
            if strings:
                self.assertTrue(
                    any(key in node for key in ("enum", "const", "pattern", "format")),
                    "free-text string schema at " + path,
                )
            for key, value in node.items():
                self.walk(value, path + "/" + str(key))
        elif isinstance(node, list):
            for index, item in enumerate(node):
                self.walk(item, path + "/" + str(index))

    def test_schema_is_strict_and_fully_typed(self):
        self.walk(self.schema())

    def test_schema_enums_match_the_runtime_contract(self):
        schema = self.schema()
        self.assertEqual(schema["properties"]["schema"]["const"], S.SCHEMA_NAME)
        self.assertEqual(schema["properties"]["capture_tier"]["const"], S.CAPTURE_TIER)
        self.assertEqual(schema["properties"]["reporting_window_days"]["const"], S.REPORTING_WINDOW_DAYS)
        self.assertEqual(schema["properties"]["library_revision"]["enum"], list(S.SUPPORTED_LIBRARY_REVISIONS))
        snapshot = schema["properties"]["snapshot"]["properties"]
        self.assertEqual(snapshot["status"]["enum"], list(S.STATUSES))
        self.assertEqual(snapshot["acceptance"]["enum"], list(S.ACCEPTANCE))
        self.assertEqual(snapshot["acceptance_evidence"]["enum"], list(S.ACCEPTANCE_EVIDENCE))
        self.assertEqual(snapshot["applicable_stages"]["items"]["enum"], list(S.STAGES))
        self.assertEqual(snapshot["stage_status"]["properties"]["build"]["enum"], list(S.STAGE_STATUSES))
        transitions = snapshot["transitions"]
        self.assertEqual(transitions["maxItems"], S.MAX_TRANSITIONS)
        self.assertEqual(transitions["items"]["properties"]["kind"]["enum"], list(S.EVENT_KINDS))

    def test_schema_declares_the_same_top_level_fields(self):
        schema = self.schema()
        self.assertEqual(tuple(schema["required"]), S.TOP_KEYS)
        self.assertEqual(tuple(schema["properties"]["snapshot"]["required"]), S.SNAPSHOT_KEYS)


class CliTests(unittest.TestCase):
    def run_cli(self, *args, store):
        command = [sys.executable, "-B", str(REPO_ROOT / "tools" / "aegis_usage" / "local_report.py"), "--store", str(store)]
        return subprocess.run(command + list(args), capture_output=True, text=True, encoding="utf-8")

    def test_cli_opt_in_record_preview_export(self):
        with tempfile.TemporaryDirectory() as folder:
            store = Path(folder) / "local.json"
            result = self.run_cli("opt-in", "--day", "2026-01-06", "--start-day", START, store=store)
            self.assertEqual(result.returncode, 0, result.stderr)
            workflow_ref = json.loads(result.stdout)["workflow_ref"]
            self.assertTrue(store.exists())
            result = self.run_cli(
                "record", "--workflow-ref", workflow_ref, "--kind", "observation", "--value", "ongoing",
                "--effective-day", START, store=store,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            result = self.run_cli("preview", "--workflow-ref", workflow_ref, store=store)
            self.assertEqual(result.returncode, 2)
            self.assertIn("missing_admission", result.stderr)
            result = self.run_cli(
                "attach-admission", "--workflow-ref", workflow_ref, "--admission-ref", ADMISSION, store=store
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            result = self.run_cli("preview", "--workflow-ref", workflow_ref, store=store)
            self.assertEqual(result.returncode, 0, result.stderr)
            preview_bytes = result.stdout.encode("utf-8")
            digest = S.bytes_sha256(preview_bytes)
            self.assertIn(digest, result.stderr)
            target = Path(folder) / "out" / "export.json"
            result = self.run_cli(
                "export", "--workflow-ref", workflow_ref, "--out", str(target),
                "--preview-sha256", digest, "--confirm", store=store,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(target.read_bytes(), preview_bytes)

    def test_cli_reports_a_stable_error_code(self):
        with tempfile.TemporaryDirectory() as folder:
            store = Path(folder) / "local.json"
            result = self.run_cli(
                "record", "--workflow-ref", "wf-" + "0" * 32, "--kind", "observation",
                "--value", "ongoing", "--effective-day", START, store=store,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("ERROR capture_disabled", result.stderr)

    def test_cli_delete_local_requires_confirmation_and_deletes_one_workflow(self):
        with tempfile.TemporaryDirectory() as folder:
            store = Path(folder) / "local.json"
            first = json.loads(self.run_cli("opt-in", "--day", "2026-01-06", "--start-day", START, store=store).stdout)
            second = json.loads(self.run_cli("opt-in", "--day", "2026-01-06", "--start-day", START, store=store).stdout)
            refused = self.run_cli("delete-local", "--workflow-ref", first["workflow_ref"], store=store)
            self.assertEqual(refused.returncode, 2)
            self.assertIn("ERROR confirmation_required", refused.stderr)
            self.assertTrue(store.exists())
            deleted = self.run_cli(
                "delete-local", "--workflow-ref", first["workflow_ref"], "--confirm", store=store
            )
            self.assertEqual(deleted.returncode, 0, deleted.stderr)
            self.assertEqual(
                json.loads(deleted.stdout),
                {"deleted_opt_ins": 1, "deleted_workflows": 1, "workflows_remaining": 1},
            )
            after = json.loads(store.read_text(encoding="utf-8"))
            self.assertNotIn(first["workflow_ref"], after["workflows"])
            self.assertIn(second["workflow_ref"], after["workflows"])
            again = self.run_cli(
                "delete-local", "--workflow-ref", first["workflow_ref"], "--confirm", store=store
            )
            self.assertEqual(again.returncode, 2)
            self.assertIn("ERROR unknown_workflow", again.stderr)

    def test_cli_record_acceptance_evidence_defaults_and_explicit_values(self):
        with tempfile.TemporaryDirectory() as folder:
            store = Path(folder) / "local.json"
            ref = json.loads(self.run_cli("opt-in", "--day", "2026-01-06", "--start-day", START, store=store).stdout)[
                "workflow_ref"
            ]
            refused = self.run_cli(
                "record", "--workflow-ref", ref, "--kind", "acceptance",
                "--value", "independent_attested_pass", "--effective-day", "2026-01-09", store=store,
            )
            self.assertEqual(refused.returncode, 2)
            self.assertIn("ERROR evidence_required", refused.stderr)
            accepted = self.run_cli(
                "record", "--workflow-ref", ref, "--kind", "acceptance",
                "--value", "independent_attested_pass", "--effective-day", "2026-01-09",
                "--evidence", "local_test_record", store=store,
            )
            self.assertEqual(accepted.returncode, 0, accepted.stderr)
            self.run_cli(
                "attach-admission", "--workflow-ref", ref, "--admission-ref", ADMISSION, store=store
            )
            preview = self.run_cli("preview", "--workflow-ref", ref, store=store)
            self.assertEqual(preview.returncode, 0, preview.stderr)
            snapshot = json.loads(preview.stdout)["snapshot"]
            self.assertEqual(snapshot["acceptance"], "independent_attested_pass")
            self.assertEqual(snapshot["acceptance_evidence"], "local_test_record")


if __name__ == "__main__":
    unittest.main()
