"""Portable literal oracles for the local, non-authorizing reporting interface.

Copy unchanged beside fixtures/ with the module one directory above tests/.
The fixture's replay is sanitized supplied record evidence, not verified authority.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
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
        self.assertEqual(self.report()["items"][0]["native_routes"]["authority"]["route"],
                         "LOCATE_ORIGINAL_AUTHORITY")
        a = item["authority"]
        a.update(original_verified_reported=True, lifecycle="active",
                 conditions_satisfied_reported=True,
                 source_locator={"value":"record:original-owner", "unknown_reason":None})
        self.assertEqual(self.report()["items"][0]["native_routes"]["authority"]["route"],
                         "REUSE_VERIFIED_APPLICABLE_GRANT")
        for lifecycle in ("consumed", "revoked", "expired", "unknown"):
            a["lifecycle"] = lifecycle
            self.assertEqual(self.report()["items"][0]["native_routes"]["authority"]["route"],
                             "RECONCILE_EXACT_SCOPE_OR_CONDITIONS")
        a["lifecycle"] = "active"
        a["repository"] = "foreign/repository"
        self.assertEqual(self.report()["items"][0]["native_routes"]["authority"]["route"],
                         "FOREIGN_GRANT_REJECTED")
        for rendered in self.report()["items"]:
            self.assertFalse(rendered["native_routes"]["authority"]["grantsNewExecutionAuthority"])

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
        self.assertEqual(route["route"], "NATIVE_DISPOSITION_POLICY")
        self.assertFalse(route["closed"])

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
        m["baseline_elapsed_seconds"]["value"] = 0
        m["incremental_cost"]["value"] = 0
        m["explicit_finish"]["value"] = "2026-11-02T00:00:00Z"
        result = self.report()["metrics"]
        self.assertIsNone(result["wall_seconds"])
        self.assertIsNone(result["speed_improvement"])
        self.assertIsNone(result["roi"])
        self.assertTrue(result["reasons"])

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
