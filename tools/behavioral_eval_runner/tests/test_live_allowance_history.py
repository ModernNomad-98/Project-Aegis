"""Offline fake-GitHub tests for the shared allowance-history collector.

No network/provider/credential/paid action: gh is a fake callable and artifact
downloads are written under a temporary directory.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

REPO_ROOT = Path(__file__).resolve().parents[3]

from tools.behavioral_eval_runner.live.allowance_history import (
    ALLOWANCE_HISTORY_SCHEMA,
    collect_allowance_history,
    collect_smoke_proof_spends,
    list_run_artifacts,
    list_workflow_runs,
)
from tools.behavioral_eval_runner.live.cumulative import admit_paid_call, smoke_spend_total


class FakeGH:
    def __init__(self, run_pages, artifacts, payloads):
        self.run_pages = run_pages
        self.artifacts = artifacts
        self.payloads = payloads
        self.calls = []

    def __call__(self, args):
        self.calls.append(list(args))
        joined = " ".join(args)
        if args[:1] == ["api"]:
            if "eval-smoke.yml/runs" in joined:
                payload = self.run_pages["smoke"]
            elif "eval-run.yml/runs" in joined:
                payload = self.run_pages["trial"]
            elif "/artifacts" in joined:
                run_id = joined.split("/actions/runs/")[1].split("/artifacts")[0]
                payload = [{"total_count": len(self.artifacts[run_id]), "artifacts": self.artifacts[run_id]}]
            else:
                payload = []
            return SimpleNamespace(returncode=0, stdout=json.dumps(payload), stderr="")
        if args[:2] == ["run", "download"]:
            run_id = args[2]
            name = args[args.index("--name") + 1]
            out_dir = Path(args[args.index("--dir") + 1])
            out_dir.mkdir(parents=True, exist_ok=True)
            member, payload = self.payloads[(run_id, name)]
            (out_dir / member).write_text(json.dumps(payload), encoding="utf-8")
            return SimpleNamespace(returncode=0, stdout="", stderr="")
        return SimpleNamespace(returncode=1, stdout="", stderr="unexpected")


def run(run_id, attempt=1, conclusion="success"):
    return {"id": run_id, "run_attempt": attempt, "status": "completed", "conclusion": conclusion}


def page(items, total=None):
    return {"total_count": len(items) if total is None else total, "workflow_runs": items}


def artifact(name):
    return {"name": name}


class AllowanceHistoryTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_pagination_flattens_all_pages(self):
        fake = FakeGH({"smoke": [page([run(1)], total=2), page([run(2)], total=2)], "trial": [page([])]}, {}, {})
        runs = list_workflow_runs(fake, "o/r", "eval-smoke.yml")
        self.assertEqual([r["id"] for r in runs], [1, 2])

    def test_incomplete_run_listing_refuses(self):
        fake = FakeGH({"smoke": [page([run(1)], total=2)], "trial": [page([])]}, {}, {})
        with self.assertRaises(ValueError):
            list_workflow_runs(fake, "o/r", "eval-smoke.yml")

    def test_missing_artifact_is_unknown_not_zero(self):
        fake = FakeGH(
            {"smoke": [page([run(42)])], "trial": [page([])]},
            {"42": []}, {},
        )
        with self.assertRaises(ValueError) as caught:
            collect_smoke_proof_spends(gh=fake, repository="o/r", work_dir=self.tmp)
        self.assertIn("UNKNOWN", str(caught.exception))

    def test_unsupported_proof_schema_refuses(self):
        fake = FakeGH(
            {"smoke": [page([run(42)])], "trial": [page([])]},
            {"42": [artifact("ber-live-smoke-proof")]},
            {("42", "ber-live-smoke-proof"): ("smoke-proof.json",
              {"schema": "ber-live-smoke-proof/0.9.0", "spent_cents": 1})},
        )
        with self.assertRaises(ValueError):
            collect_smoke_proof_spends(gh=fake, repository="o/r", work_dir=self.tmp)

    def test_unicode_fixture_and_shared_history(self):
        fake = FakeGH(
            {"smoke": [page([run("smoke-☃", attempt=2)])],
             "trial": [page([run(900)])]},
            {"smoke-☃": [artifact("ber-live-smoke-proof")],
             "900": [artifact("ber-resume-manifest")]},
            {
                ("smoke-☃", "ber-live-smoke-proof"): (
                    "smoke-proof.json",
                    {"schema": "ber-live-smoke-proof/1.0.0", "spent_cents": 174,
                     "note": "smoke ☃ déjà vu"},
                ),
                ("900", "ber-resume-manifest"): (
                    "manifest.json",
                    {"schema": "ber-resume-manifest/1.2.0",
                     "totals": {"spent_cents": 2_000},
                     "smoke_spend": {"900": 50}},
                ),
            },
        )
        history = collect_allowance_history(gh=fake, repository="o/r", work_dir=self.tmp)
        self.assertEqual(history["schema"], ALLOWANCE_HISTORY_SCHEMA)
        self.assertEqual(history["ledger_spend_cents"], 1_950)
        self.assertEqual(history["smoke_spend_cents"], 242)

    def test_smoke_after_near_exhausted_trial_helper(self):
        fake = FakeGH(
            {"smoke": [page([run(42)])], "trial": [page([run(900)])]},
            {"42": [artifact("ber-live-smoke-proof")],
             "900": [artifact("ber-resume-manifest")]},
            {
                ("42", "ber-live-smoke-proof"): (
                    "smoke-proof.json",
                    {"schema": "ber-live-smoke-proof/1.0.0", "spent_cents": 174},
                ),
                ("900", "ber-resume-manifest"): (
                    "manifest.json",
                    {"schema": "ber-resume-manifest/1.2.0",
                     "totals": {"spent_cents": 11_874},
                     "smoke_spend": {"42": 174}},
                ),
            },
        )
        history = collect_allowance_history(gh=fake, repository="o/r", work_dir=self.tmp)
        admitted = admit_paid_call(
            ceiling_cents=12_000,
            prior_ledger_spend_cents=history["ledger_spend_cents"],
            prior_smoke_spend_records=history["smoke_spend"],
            reservation_cents=108,
        )
        denied = admit_paid_call(
            ceiling_cents=12_000,
            prior_ledger_spend_cents=history["ledger_spend_cents"],
            prior_smoke_spend_records=history["smoke_spend"],
            reservation_cents=109,
        )
        self.assertTrue(admitted["admitted"])
        self.assertFalse(denied["admitted"])

    def test_failed_run_proof_and_historical_are_not_skipped(self):
        fake = FakeGH(
            {"smoke": [page([run(42, conclusion="failure")])], "trial": [page([])]},
            {"42": [artifact("ber-live-smoke-proof")]},
            {("42", "ber-live-smoke-proof"): (
                "smoke-proof.json",
                {"schema": "ber-live-smoke-proof/1.0.0", "spent_cents": 150},
            )},
        )
        history = collect_allowance_history(gh=fake, repository="o/r", work_dir=self.tmp)
        self.assertEqual(history["ledger_spend_cents"], 222)
        self.assertEqual(history["smoke_spend_cents"], 168)

    def test_artifact_pagination_incomplete_refuses(self):
        from tools.behavioral_eval_runner.live import allowance_history
        fake = FakeGH({"smoke": [page([])], "trial": [page([])]}, {}, {})
        class Incomplete(FakeGH):
            def __call__(self, args):
                if "/artifacts" in " ".join(args):
                    return SimpleNamespace(returncode=0, stdout=json.dumps(
                        [{"total_count": 2, "artifacts": [{"name": "x"}]}]
                    ), stderr="")
                return super().__call__(args)
        with self.assertRaises(ValueError):
            allowance_history.list_run_artifacts(Incomplete({}, {}, {}), "o/r", 1)

    def test_old_resume_and_proof_schemas_fail_closed_explicitly(self):
        fake = FakeGH(
            {"smoke": [page([run(42)])], "trial": [page([run(900)])]},
            {"42": [artifact("ber-live-smoke-proof")],
             "900": [artifact("ber-resume-manifest")]},
            {
                ("42", "ber-live-smoke-proof"): (
                    "smoke-proof.json",
                    {"schema": "ber-live-smoke-proof/0.9.0", "spent_cents": 1},
                ),
                ("900", "ber-resume-manifest"): (
                    "manifest.json",
                    {"schema": "ber-resume-manifest/1.1.0", "totals": {"spent_cents": 1}},
                ),
            },
        )
        with self.assertRaises(ValueError) as caught:
            collect_allowance_history(gh=fake, repository="o/r", work_dir=self.tmp)
        self.assertIn("unsupported schema", str(caught.exception))

    def test_missing_trial_manifest_refuses(self):
        fake = FakeGH(
            {"smoke": [page([])], "trial": [page([run(900)])]},
            {"900": []}, {},
        )
        with self.assertRaises(ValueError):
            collect_allowance_history(gh=fake, repository="o/r", work_dir=self.tmp)

class WorkflowWiringTests(unittest.TestCase):
    def test_eval_smoke_admission_precedes_config_and_keys(self):
        text = (REPO_ROOT / ".github/workflows/eval-smoke.yml").read_text(encoding="utf-8")
        admission = text.index("Shared allowance admission preflight")
        config = text.index("Stage and verify the single-case smoke settings")
        keys = text.index("Run the single-case live smoke")
        self.assertLess(admission, config)
        self.assertLess(admission, keys)
        self.assertIn("collect_allowance_history", text)
        self.assertIn("admit_paid_call", text)

    def test_eval_run_merges_standalone_smoke_proofs(self):
        text = (REPO_ROOT / ".github/workflows/eval-run.yml").read_text(encoding="utf-8")
        self.assertIn("collect_smoke_proof_spends", text)
        self.assertIn("standalone smoke history is not restorable", text)
        self.assertIn("prior_smoke_manifests.append(standalone_smoke)", text)


if __name__ == "__main__":
    unittest.main()
