"""Portable literal oracles for the local, non-authorizing reporting interface.

Copy unchanged beside fixtures/ with the module one directory above tests/.
The fixture's replay is sanitized supplied record evidence, not verified authority.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
MODULE = HERE.parent / "cnc_reporting.py"
CASES = json.loads((HERE / "fixtures" / "cnc-report-cases.json").read_text("utf-8"))
spec = importlib.util.spec_from_file_location("portable_cnc_reporting", MODULE)
cnc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cnc)


class ReportingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="cnc-portable-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.input = self.root / "input.json"
        self.profile = self.root / "profile.json"
        self.contract = self.root / "contract.json"
        self.contract.write_bytes(CASES["contract_utf8"].encode("utf-8"))
        self.profile.write_text(json.dumps(CASES["profile"]), encoding="utf-8")
        self.data = copy.deepcopy(CASES["input"])

    def report(self):
        self.input.write_text(json.dumps(self.data), encoding="utf-8")
        return cnc.report_from_paths(self.data["repository_id"], self.input,
                                     self.profile, self.contract)

    def cli(self, raw=None, extra=()):
        self.input.write_bytes(raw if raw is not None else json.dumps(self.data).encode())
        return subprocess.run([sys.executable, "-B", str(MODULE), "--repository-id",
                               self.data["repository_id"], "--input", str(self.input),
                               "--profile", str(self.profile), "--contract", str(self.contract),
                               *extra], capture_output=True)

    def refused(self, raw, code="INPUT_INVALID", exit_code=2):
        run = self.cli(raw)
        self.assertEqual(run.returncode, exit_code, run.stderr)
        self.assertEqual(run.stdout, b"")
        self.assertEqual(json.loads(run.stderr), {"error_code": code,
                         "message": cnc.ERRORS[code][1]})
        self.assertNotIn(b"\r", run.stderr)
        self.assertEqual(run.stderr.count(b"\n"), 1)
        self.assertNotIn(b"DO_NOT_LEAK", run.stderr)

    def test_sanitized_record_and_literal_oracles(self):
        report = self.report()
        self.assertEqual(report["report_status"], "RENDERED_NON_AUTHORIZING")
        self.assertEqual([x["progress"] for x in report["items"]], CASES["expected_progress"])
        self.assertEqual(report["items"][0]["dependencies_and_holds"], ["Real dispatch remains held"])
        self.assertEqual(report["items"][0]["next_action"], "Existing Lead reconciles retained record")
        self.assertEqual(report["native_record"], self.data["native_record"])
        self.assertEqual(report["input_sha256"], hashlib.sha256(self.input.read_bytes()).hexdigest())
        self.assertEqual(report["metrics"]["wall_seconds"], 10)
        self.assertEqual(report["metrics"]["wall_basis"], "explicit_review_wall_window")
        self.assertIsNone(report["metrics"]["active_effort_seconds"])
        self.assertEqual(report["collection"]["positions"], [665,666,667,668,669,670])
        self.assertFalse(report["collection"]["infer_deletions"])
        self.assertFalse(report["collection"]["overwrite_baseline"])

    def test_authority_literal_routes(self):
        item = self.data["items"][0]
        rendered = self.report()["items"][0]["native_routes"]["authority"]
        self.assertEqual(rendered["route"], "LOCATE_ORIGINAL_AUTHORITY")
        self.assertEqual(rendered["policy"],
                         CASES["profile"]["authority_policy_locator"])
        a = item["authority"]
        a.update(original_verified_reported=True, lifecycle="active",
                 conditions_satisfied_reported=True,
                 source_locator={"value":"record:original-owner", "unknown_reason":None})
        self.assertEqual(self.report()["items"][0]["native_routes"]["authority"]["route"],
                         "REUSE_VERIFIED_APPLICABLE_GRANT")
        # A missing original is a locating gap while the lifecycle is usable.
        a.update(original_verified_reported=False,
                 source_locator={"value": None, "unknown_reason": "not supplied"})
        self.assertEqual(self.report()["items"][0]["native_routes"]["authority"]["route"],
                         "LOCATE_ORIGINAL_AUTHORITY")
        # Expired, revoked and consumed are terminal before the missing check:
        # no reconciliation restores reuse, so only new authority can help.
        for lifecycle in ("consumed", "revoked", "expired"):
            a["lifecycle"] = lifecycle
            self.assertEqual(self.report()["items"][0]["native_routes"]["authority"]["route"],
                             "NON_REUSABLE_GRANT_NEW_AUTHORITY_REQUIRED")
        # An unknown lifecycle falls back to the locating gap.
        a["lifecycle"] = "unknown"
        self.assertEqual(self.report()["items"][0]["native_routes"]["authority"]["route"],
                         "LOCATE_ORIGINAL_AUTHORITY")
        # Restore a locatable grant for the remaining routes.
        a.update(original_verified_reported=True, lifecycle="active",
                 source_locator={"value": "record:original-owner",
                                 "unknown_reason": None})
        a["lifecycle"] = "unknown"
        self.assertEqual(self.report()["items"][0]["native_routes"]["authority"]["route"],
                         "RECONCILE_EXACT_SCOPE_OR_CONDITIONS")
        a["lifecycle"] = "active"
        a["repository"] = "foreign/repository"
        self.assertEqual(self.report()["items"][0]["native_routes"]["authority"]["route"],
                         "FOREIGN_GRANT_REJECTED")
        # Foreign is decided before missing: a foreign grant without a verified
        # original or locator is still foreign, not an authority to locate.
        a["original_verified_reported"] = False
        a["source_locator"] = {"value": None, "unknown_reason": "not supplied"}
        self.assertEqual(self.report()["items"][0]["native_routes"]["authority"]["route"],
                         "FOREIGN_GRANT_REJECTED")
        for rendered in self.report()["items"]:
            authority = rendered["native_routes"]["authority"]
            self.assertEqual(authority["policy"],
                             CASES["profile"]["authority_policy_locator"])
            self.assertFalse(authority["grantsNewExecutionAuthority"])
            self.assertIsNone(authority["ownerWithheld"])

    def test_retained_replay_does_not_invent_pending_progress(self):
        self.data = copy.deepcopy(CASES["retained_replay"])
        report = self.report()
        self.assertEqual([item["task"] for item in report["items"]], ["proof2-retained"])
        self.assertNotIn("source-995-record", [item["task"] for item in report["items"]])
        pending = CASES["replay_provenance"]["pending_facts_excluded_from_input"][0]
        self.assertEqual(pending["id"], "source-995-record")
        self.assertFalse(any(pending["progress"].values()))
        self.assertEqual(pending["hold"], "Native exact-head and bound-field conditions")
        self.assertEqual(pending["next"], "Existing holder supplies actual corrected publication and formal-stage disposition")
        proof = report["items"][0]
        self.assertEqual(proof["progress"], "accepted_completion")
        self.assertIsNone(proof["coordinator_answer"]["value"])
        self.assertEqual(proof["dependencies_and_holds"],
            ["Reported owner retention choice; source merge authority separate"])
        self.assertEqual(proof["evidence_label"], "Reported")
        self.assertEqual(proof["accepted_completion_scope"]["value"],
            "Reported operational consumer proof only; no source C&C rollout acceptance")
        self.assertIsNone(report["metrics"]["cost_savings"])
        self.assertIsNone(report["metrics"]["roi"])

    def test_changes_and_findings_are_native_advice(self):
        item = self.data["items"][0]
        self.assertEqual(self.report()["items"][0]["native_routes"]["change"]["route"],
                         "RECEIPT_READBACK_AND_NATIVE_RECEIPT_CHECKS")
        for key in ("changes_head", "changes_scope", "material_finding", "consumed_by_check"):
            item["change"][key] = True
            route = self.report()["items"][0]["native_routes"]["change"]
            self.assertEqual(route["route"], "NATIVE_POLICY_ASSESSMENT")
            self.assertFalse(route["automaticFullRerun"])
            self.assertFalse(route["clearsNativeGates"])
            item["change"][key] = False
        item["change"]["kind"] = "other"
        self.assertEqual(self.report()["items"][0]["native_routes"]["change"]["route"],
                         "IDENTIFY_CHANGED_INPUTS")
        item["finding"] = {"value":{"status":"accepted", "evidence":{"value":"record:review","unknown_reason":None},
            "primary":{"value":None,"unknown_reason":"not supplied"},
            "applicable_acceptance_verified_reported":True}, "unknown_reason":None}
        route = self.report()["items"][0]["native_routes"]["finding"]
        self.assertEqual(route["state"], "reported")
        self.assertEqual(route["route"], "NATIVE_DISPOSITION_POLICY")
        self.assertIsNone(route["evidenceGap"])
        self.assertFalse(route["closed"])

    def test_finding_states_are_explicit(self):
        item = self.data["items"][0]
        def route():
            return self.report()["items"][0]["native_routes"]["finding"]
        # A null finding is unknown, not proof that no finding exists.
        self.assertEqual(route()["state"], "unknown")
        self.assertEqual(route()["route"], "UNKNOWN_FINDING_NATIVE_DISPOSITION")
        self.assertTrue(route()["evidenceGap"])
        self.assertFalse(route()["closed"])
        self.assertTrue(any("Finding for event" in gap
                            for gap in self.report()["evidence_gaps"]))
        # A material finding flag without details is unresolved, never NO_FINDING.
        item["change"]["material_finding"] = True
        self.assertEqual(route()["state"], "unresolved_material")
        self.assertEqual(route()["route"], "UNRESOLVED_NATIVE_DISPOSITION")
        self.assertIn("material finding", route()["evidenceGap"])
        # Supplied details are a reported finding for native disposition.
        item["finding"] = {"value": {"status": "accepted",
            "evidence": {"value": "record:review", "unknown_reason": None},
            "primary": {"value": None, "unknown_reason": "not supplied"},
            "applicable_acceptance_verified_reported": True}, "unknown_reason": None}
        self.assertEqual(route()["state"], "reported")
        self.assertEqual(route()["route"], "NATIVE_DISPOSITION_POLICY")
        self.assertIsNone(route()["evidenceGap"])
        # A material finding needs a matching evidence or primary detail; a
        # "accepted" status alone is not detail.
        item["finding"] = {"value": {"status": "accepted",
            "evidence": {"value": None, "unknown_reason": "not supplied"},
            "primary": {"value": None, "unknown_reason": "not supplied"},
            "applicable_acceptance_verified_reported": True}, "unknown_reason": None}
        self.assertEqual(route()["state"], "unresolved_material")
        self.assertEqual(route()["route"], "UNRESOLVED_NATIVE_DISPOSITION")
        self.assertIn("evidence or primary detail", route()["evidenceGap"])
        self.assertTrue(any("Finding for event" in gap
                            for gap in self.report()["evidence_gaps"]))
        # Only a positive no-finding report routes NO_FINDING.
        item["change"]["material_finding"] = False
        item["finding"] = {"value": {"status": "none",
            "evidence": {"value": None, "unknown_reason": "not applicable"},
            "primary": {"value": None, "unknown_reason": "not applicable"},
            "applicable_acceptance_verified_reported": False}, "unknown_reason": None}
        self.assertEqual(route()["state"], "none")
        self.assertEqual(route()["route"], "NO_FINDING")
        self.assertIsNone(route()["evidenceGap"])
        # A no-finding record contradicted by the flag stays unresolved.
        item["change"]["material_finding"] = True
        self.assertEqual(route()["state"], "unresolved_material")
        self.assertEqual(route()["route"], "UNRESOLVED_NATIVE_DISPOSITION")

    def test_metrics_literal_formula_and_unknowns(self):
        m = self.data["metrics"]
        m["comparable_reported"] = True
        for key, value in {"baseline_elapsed_seconds":10,"current_elapsed_seconds":5,
                           "baseline_attributed_cost":10,"current_attributed_cost":8,
                           "attributable_benefit":12,"incremental_cost":4,
                           "cost_provenance":"record:synthetic-cost"}.items():
            m[key] = {"value":value,"unknown_reason":None}
        result = self.report()["metrics"]
        self.assertEqual([result[x] for x in ("speed_improvement","cost_savings","roi")], [.5,2,2])
        self.assertEqual(result["comparison_basis"], "reported_inputs")
        self.assertEqual(result["cost_provenance"], "record:synthetic-cost")
        m["baseline_elapsed_seconds"]["value"] = 0
        m["incremental_cost"]["value"] = 0
        m["explicit_finish"]["value"] = "2026-11-02T00:00:00Z"
        result = self.report()["metrics"]
        self.assertIsNone(result["wall_seconds"])
        self.assertIsNone(result["speed_improvement"])
        self.assertIsNone(result["roi"])
        self.assertTrue(result["reasons"])

    def test_cost_provenance_is_a_scalar_fact(self):
        metrics = self.report()["metrics"]
        self.assertIsNone(metrics["cost_provenance"])
        self.assertTrue(any(reason.startswith("Cost provenance unknown: ")
                            for reason in metrics["reasons"]))
        self.data["metrics"]["cost_provenance"] = {"value": "record:synthetic-cost",
                                                   "unknown_reason": None}
        metrics = self.report()["metrics"]
        self.assertEqual(metrics["cost_provenance"], "record:synthetic-cost")
        self.assertFalse(any("Cost provenance unknown" in reason
                             for reason in metrics["reasons"]))

    def test_no_side_effects(self):
        self.input.write_text(json.dumps(self.data), encoding="utf-8")
        before = {p.name:p.read_bytes() for p in self.root.iterdir()}
        import socket
        import sqlite3
        import os
        original_open = cnc.os.open
        def read_only(path, flags, *args, **kwargs):
            self.assertEqual(flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND), 0)
            return original_open(path, flags, *args, **kwargs)
        with patch.object(socket, "socket", side_effect=AssertionError("network")), \
             patch.object(sqlite3, "connect", side_effect=AssertionError("database")), \
             patch.object(subprocess, "Popen", side_effect=AssertionError("process")), \
             patch.object(cnc.os, "open", side_effect=read_only), \
             patch.object(Path, "write_bytes", side_effect=AssertionError("write")), \
             patch.object(Path, "write_text", side_effect=AssertionError("write")):
            cnc.report_from_paths(self.data["repository_id"], self.input, self.profile, self.contract)
        self.assertEqual(before, {p.name:p.read_bytes() for p in self.root.iterdir()})

    def test_raw_json_negative_oracles(self):
        good = json.dumps(self.data).encode()
        for raw in (b'{"schema_version":1,"schema_version":1}', b'{}{}', b'\xef\xbb\xbf'+good,
                    b'\xff', b'['*17+b'0'+b']'*17, b''):
            with self.subTest(raw=raw[:30]): self.refused(raw)
        for bad in ('NaN','Infinity','-Infinity','1e9999'):
            self.refused(good.replace(b'"schema_version": 1', ('"schema_version": '+bad).encode(),1))
        self.refused(good.replace(b'"paused": true', b'"paused": true,"paused": true',1))
        self.refused(good.replace(b'"schema_version": 1',b'"schema_version": 1e9999',1))

    def test_closed_schema_negative_oracles(self):
        mutations = [
            lambda d:d.update(schema_version=True),
            lambda d:d.update(password="DO_NOT_LEAK"),
            lambda d:d["items"][0].update(description="x"*4097),
            lambda d:d["items"][0].update(description="ghp_DO_NOT_LEAK_123"),
            lambda d:d["items"][0].update(description="https://u:DO_NOT_LEAK@example.invalid/"),
            lambda d:d["items"][0].update(event_id=d["items"][1]["event_id"]),
            lambda d:d["items"][0]["change"].update(changes_head=1),
            lambda d:d["items"][0]["change"].update(extra=False),
            lambda d:d["items"][0].pop("finding"),
            lambda d:d["items"][0].update(progress="accepted_completion"),
            lambda d:d["collection"].update(complete=True),
            lambda d:d["collection"].update(positions=[1,2,3,4,5,6]),
            lambda d:d["collection"]["inbox_total"].update(value=670.0),
            lambda d:d["metrics"]["active_effort_seconds"].update(value=True,unknown_reason=None),
            lambda d:d["metrics"]["active_effort_seconds"].update(value=-1,unknown_reason=None),
            lambda d:d["metrics"]["active_effort_seconds"].update(value=1000000000001,unknown_reason=None),
            lambda d:d["items"][0].update(retrieved_at="2026-02-30T00:00:00Z"),
            lambda d:d["items"][0].update(retrieved_at="2026-11-03T00:00:00+00:00"),
            lambda d:d["items"][0]["authority"].update(original_verified_reported="true"),
            lambda d:d["items"][0].update(event_id="x"*129),
            lambda d:d["items"][0].update(execution_evidence=["record:x"]*101),
            lambda d:d["items"][0].update(dependencies_and_holds=["held"]*1001),
        ]
        for mutate in mutations:
            d = copy.deepcopy(self.data); mutate(d)
            with self.subTest(mutation=mutate): self.refused(json.dumps(d).encode())
        for char in ("\x1b","\n","\x7f","\x85","\u202e","\u2066","\u200f","\u2028","\ud800"):
            d=copy.deepcopy(self.data); d["items"][0]["description"]="bad"+char
            self.refused(json.dumps(d).encode())

    def test_credentials_and_profile_schema_fail_closed(self):
        for secret in ("gho_DO_NOT_LEAK", "ghu_DO_NOT_LEAK", "ghs_DO_NOT_LEAK", "ghr_DO_NOT_LEAK",
                       "github_pat_DO_NOT_LEAK", "sk-proj-DO_NOT_LEAK", "sk-ant-DO_NOT_LEAK",
                       "AKIADO_NOT_LEAK", "ASIADO_NOT_LEAK", "Bearer DO_NOT_LEAK",
                       "-----BEGIN RSA PRIVATE KEY-----", "https://e.invalid/?token=DO_NOT_LEAK",
                       "https://e.invalid/?password=DO_NOT_LEAK", "https://e.invalid/?api_key=DO_NOT_LEAK"):
            d=copy.deepcopy(self.data); d["items"][0]["description"]=secret
            self.refused(json.dumps(d).encode())
        for mutation in (lambda p:p.update(extra=True),
                         lambda p:p["stage_labels"].append({"id":"H","label":"invented"}),
                         lambda p:p.update(schema_version=True)):
            profile=copy.deepcopy(CASES["profile"]); mutation(profile)
            self.profile.write_text(json.dumps(profile),encoding="utf-8")
            self.refused(json.dumps(self.data).encode(),"PROFILE_INVALID")

    def test_unknown_window_observation_span_and_validation_order(self):
        self.data["collection"]["inbox_total"]={"value":None,"unknown_reason":"unknown total"}
        self.data["collection"]["positions"]=[]
        metrics=self.data["metrics"]
        for key in ("explicit_start","explicit_finish"):
            metrics[key]={"value":None,"unknown_reason":"no explicit window"}
        metrics["first_observation"]={"value":"2026-11-02T22:22:28.765Z","unknown_reason":None}
        metrics["last_observation"]={"value":"2026-11-02T22:29:57.757Z","unknown_reason":None}
        report=self.report()
        self.assertEqual(report["metrics"]["wall_seconds"],448.992)
        self.assertEqual(report["metrics"]["wall_basis"],"observation_span_lower_bound")
        self.assertTrue(report["evidence_gaps"])
        self.profile.write_text("{}",encoding="utf-8")
        self.refused(b"{}","INPUT_INVALID")
        self.contract.write_bytes(b"{}")
        self.refused(json.dumps(self.data).encode(),"PROFILE_INVALID")

    def test_expected_repository_is_checked_before_projection(self):
        self.data["repository_id"] = "evil/repository"
        profile = copy.deepcopy(CASES["profile"])
        profile["repository"] = "evil/repository"
        self.profile.write_text(json.dumps(profile), encoding="utf-8")
        self.input.write_text(json.dumps(self.data), encoding="utf-8")
        with patch.object(cnc, "_routes",
                          side_effect=AssertionError("projection reached")):
            with self.assertRaises(cnc.ReportError) as caught:
                cnc.report_from_paths(
                    "evil/repository", self.input, self.profile, self.contract,
                    expected_repository_id="ModernNomad-98/Project-Aegis")
        self.assertEqual(caught.exception.code, "IDENTITY_MISMATCH")

    def test_cli_writes_lf_only_json(self):
        run = self.cli()
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stderr, b"")
        self.assertNotIn(b"\r", run.stdout)
        self.assertEqual(run.stdout.count(b"\n"), 1)
        self.assertEqual(json.loads(run.stdout)["report_status"],
                         "RENDERED_NON_AUTHORIZING")
        error = self.cli(extra=("--unknown", "DO_NOT_LEAK"))
        self.assertEqual(error.returncode, 2)
        self.assertEqual(error.stdout, b"")
        self.assertNotIn(b"\r", error.stderr)
        self.assertEqual(error.stderr.count(b"\n"), 1)
        self.assertEqual(json.loads(error.stderr)["error_code"], "CLI_INVALID")

    def test_cli_errors_and_identity(self):
        run = self.cli(extra=("--unknown", "DO_NOT_LEAK"))
        self.assertEqual(run.returncode,2); self.assertEqual(run.stdout,b"")
        self.assertEqual(json.loads(run.stderr)["error_code"], "CLI_INVALID")
        self.assertNotIn(b"DO_NOT_LEAK",run.stderr)
        self.profile.write_text(json.dumps({**CASES["profile"],"repository":"foreign/repo"}),encoding="utf-8")
        self.refused(json.dumps(self.data).encode(),"IDENTITY_MISMATCH")
        self.profile.write_text(json.dumps(CASES["profile"]),encoding="utf-8")
        self.contract.write_bytes(self.contract.read_bytes()+b" ")
        self.refused(json.dumps(self.data).encode(),"CONTRACT_INVALID")

    def test_availability_errors_name_the_document(self):
        self.input.write_text(json.dumps(self.data), encoding="utf-8")
        cases = ((self.root/"missing-input.json", self.profile, self.contract,
                  "INPUT_UNAVAILABLE"),
                 (self.input, self.root/"missing-profile.json", self.contract,
                  "PROFILE_UNAVAILABLE"),
                 (self.input, self.profile, self.root/"missing-contract.json",
                  "CONTRACT_UNAVAILABLE"))
        for input_path, profile_path, contract_path, code in cases:
            with self.subTest(code=code):
                with self.assertRaises(cnc.ReportError) as caught:
                    cnc.report_from_paths(self.data["repository_id"], input_path,
                                          profile_path, contract_path)
                self.assertEqual(caught.exception.code, code)
                self.assertEqual(cnc.ERRORS[code][0], 3)
        for profile_path, contract_path, code in (
                (self.root, self.contract, "PROFILE_UNAVAILABLE"),
                (self.profile, "-", "CONTRACT_UNAVAILABLE"),
                (self.profile, "https://example.invalid/contract.json",
                 "CONTRACT_UNAVAILABLE")):
            with self.subTest(code=code, path=str(profile_path)):
                with self.assertRaises(cnc.ReportError) as caught:
                    cnc.report_from_paths(self.data["repository_id"], self.input,
                                          profile_path, contract_path)
                self.assertEqual(caught.exception.code, code)

    def test_cli_availability_exit_codes(self):
        self.input.write_text(json.dumps(self.data), encoding="utf-8")
        base = [sys.executable, "-B", str(MODULE), "--repository-id",
                self.data["repository_id"], "--input", str(self.input)]
        for profile_path, contract_path, code in (
                (str(self.root/"missing-profile.json"), str(self.contract),
                 "PROFILE_UNAVAILABLE"),
                (str(self.profile), str(self.root/"missing-contract.json"),
                 "CONTRACT_UNAVAILABLE")):
            with self.subTest(code=code):
                run = subprocess.run(base + ["--profile", profile_path,
                                             "--contract", contract_path],
                                     capture_output=True)
                self.assertEqual(run.returncode, 3, run.stderr)
                self.assertEqual(run.stdout, b"")
                self.assertEqual(json.loads(run.stderr),
                                 {"error_code": code, "message": cnc.ERRORS[code][1]})

    def test_profile_identifiers_are_structural(self):
        for identifier in ("aegis", "waypoint", "opsflow", "consumer-product",
                           "consumer_product", "a"*64):
            profile = copy.deepcopy(CASES["profile"])
            profile["id"] = identifier
            if identifier != "aegis":
                profile["stage_labels"] = [{"id": "1", "label": "consumer stage"}]
            self.profile.write_text(json.dumps(profile), encoding="utf-8")
            with self.subTest(identifier=identifier):
                self.assertEqual(self.report()["report_status"],
                                 "RENDERED_NON_AUTHORIZING")
        for bad in ("Aegis", "with space", "", "1st", "a"*65, "aegis!", "caf\u00e9"):
            profile = copy.deepcopy(CASES["profile"])
            profile["id"] = bad
            self.profile.write_text(json.dumps(profile), encoding="utf-8")
            with self.subTest(identifier=bad):
                self.refused(json.dumps(self.data).encode(), "PROFILE_INVALID")
        # Only the aegis profile keeps the source stage labels A-G.
        profile = copy.deepcopy(CASES["profile"])
        profile["stage_labels"] = [{"id": "A", "label": "plan"}]
        self.profile.write_text(json.dumps(profile), encoding="utf-8")
        with self.subTest(identifier="aegis-stage-labels"):
            self.refused(json.dumps(self.data).encode(), "PROFILE_INVALID")

    def test_shipped_contract_bytes_stay_lf_and_match(self):
        # This test is the line-ending enforcement for the shipped contract:
        # every .gitattributes path is a gate-guard-protected surface, so the
        # byte pin lives in the suite rather than in a per-file attribute.
        candidates = (MODULE.parent/"cnc"/"cnc-evidence-contract-v2.json",
                      MODULE.parent/"cnc-evidence-contract-v2.json")
        shipped = next((path for path in candidates if path.is_file()), None)
        if shipped is None:
            self.skipTest("shipped contract is not beside the portable module")
        raw = shipped.read_bytes()
        self.assertNotIn(b"\r", raw)
        self.assertEqual(hashlib.sha256(raw).hexdigest(), cnc.CONTRACT_SHA256)
        self.assertEqual(raw, CASES["contract_utf8"].encode("utf-8"))
        copied = self.root/"copied-contract.json"
        shutil.copyfile(shipped, copied)
        self.assertEqual(hashlib.sha256(copied.read_bytes()).hexdigest(),
                         cnc.CONTRACT_SHA256)
        self.input.write_text(json.dumps(self.data), encoding="utf-8")
        report = cnc.report_from_paths(self.data["repository_id"], self.input,
                                       self.profile, copied)
        self.assertEqual(report["contract_sha256"], cnc.CONTRACT_SHA256)
        # A line-ending conversion is caught by the pinned byte hash.
        mangled = self.root/"crlf-contract.json"
        mangled.write_bytes(raw.replace(b"\n", b"\r\n"))
        with self.assertRaises(cnc.ReportError) as caught:
            cnc.report_from_paths(self.data["repository_id"], self.input,
                                  self.profile, mangled)
        self.assertEqual(caught.exception.code, "CONTRACT_INVALID")

    def test_utc_timestamps_require_ascii_digits(self):
        self.assertNotIn("\\d", cnc._TIMESTAMP.pattern)
        for text in ("\u0662\u0660\u0662\u0666-11-03T00:00:00Z",
                     "2026-\u0661\u0661-03T00:00:00Z",
                     "2026-11-0\u0663T00:00:00Z"):
            with self.subTest(text=text):
                self.assertIsNone(cnc._TIMESTAMP.fullmatch(text))
                with self.assertRaises(ValueError):
                    cnc._time(text)
        self.assertIsNotNone(
            cnc._TIMESTAMP.fullmatch("2026-11-03T00:00:00.123456Z"))
        self.data["items"][0]["retrieved_at"] = "\u0662\u0660\u0662\u0666-11-03T00:00:00Z"
        self.refused(json.dumps(self.data).encode())

    def test_boundaries_files_and_limits(self):
        for raw in (b" "*1048577,): self.refused(raw)
        with self.assertRaises(cnc.ReportError) as caught:
            cnc.report_from_paths(self.data["repository_id"],self.root/"DO_NOT_LEAK",self.profile,self.contract)
        self.assertEqual(caught.exception.code,"INPUT_UNAVAILABLE")
        for path in ("-","https://example.invalid/x","//host/file",r"\\host\file",str(self.root)):
            with self.assertRaises(cnc.ReportError) as caught:
                cnc.report_from_paths(self.data["repository_id"],path,self.profile,self.contract)
            self.assertEqual(caught.exception.code,"INPUT_UNAVAILABLE")
        if sys.platform != "win32":
            self.input.write_text(json.dumps(self.data),encoding="utf-8")
            link=self.root/"link.json"; link.symlink_to(self.input)
            with self.assertRaises(cnc.ReportError):
                cnc.report_from_paths(self.data["repository_id"],link,self.profile,self.contract)

    def test_unicode_and_distinct_events(self):
        self.data["items"][1]["task"] = self.data["items"][0]["task"]
        self.data["items"][0]["description"] = "café `<script>`"
        run=self.cli()
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertIn(b"caf\\u00e9",run.stdout)
        self.assertEqual(len(json.loads(run.stdout)["items"]),4)
        self.assertTrue(run.stdout.endswith(b"\n"))
        self.assertEqual(run.stderr,b"")


if __name__ == "__main__":
    unittest.main()
