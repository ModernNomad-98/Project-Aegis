"""Consolidated workflow-runtime tests (annex-approved test path).

Preserves allowance-history, reservation/true-up, transport-spy and S3
budget-proof coverage; no assertions weakened.
"""

from __future__ import annotations

import ast
import hashlib
import itertools
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import yaml

"""Offline fake-GitHub tests for the shared allowance-history collector.

No network/provider/credential/paid action: gh is a fake callable and artifact
downloads are written under a temporary directory.
"""


import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

REPO_ROOT = Path(__file__).resolve().parents[3]

from tools.behavioral_eval_runner.live.workflow_runtime import (
    ALLOWANCE_HISTORY_SCHEMA,
    LEGACY_RESUME_MANIFEST_SCHEMA,
    PRESERVED_HISTORICAL_LEDGER_CENTS,
    PRESERVED_HISTORICAL_SMOKE_CENTS,
    REGISTERED_RESUME_MANIFEST_SCHEMAS,
    RESUME_MANIFEST_SCHEMA,
    SMOKE_PROOF_CONFIG_PINS,
    SMOKE_RUNS_WITHOUT_PROOF,
    SMOKE_RUNS_WITH_EXPIRED_PROOF,
    TRIAL_RUNS_WITHOUT_MANIFEST,
    collect_allowance_history,
    collect_latest_allowance_state,
    collect_latest_trial_spend,
    collect_smoke_proof_spends,
    list_run_artifacts,
    list_workflow_runs,
)
from tools.behavioral_eval_runner.live import workflow_runtime
from tools.behavioral_eval_runner.live.cumulative import admit_paid_call, smoke_spend_total


class FakeGH:
    def __init__(self, run_pages, artifacts, payloads):
        self.run_pages = run_pages
        self.artifacts = artifacts
        self.payloads = payloads
        self.calls = []
        self.download_requests = []

    def _run_attempt(self, run_id):
        for pages in self.run_pages.values():
            for page_entry in pages:
                for entry in page_entry.get("workflow_runs", []):
                    if str(entry.get("id")) == str(run_id):
                        return entry.get("run_attempt", 1)
        return 1

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
            records = [
                item for item in self.artifacts.get(run_id, [])
                if item.get("name") == name
            ]
            if len(records) != 1:
                # Name-only selection is only acceptable for a single record; fail
                # loudly here if production code ever guesses across duplicates.
                return SimpleNamespace(
                    returncode=1, stdout="", stderr="ambiguous artifact selection",
                )
            if records[0].get("expired") is True:
                # An expired record is never downloadable; fail loudly if requested.
                return SimpleNamespace(
                    returncode=1, stdout="", stderr="artifact expired (410)",
                )
            self.download_requests.append((run_id, name, records[0].get("id")))
            out_dir.mkdir(parents=True, exist_ok=True)
            member, payload = self.payloads[(run_id, name)]
            payload = dict(payload)
            if not payload.get("__no_defaults__"):
                if name == "ber-live-smoke-proof" and payload.get("schema") == "ber-live-smoke-proof/1.0.0":
                    payload.setdefault("status", "PASS")
                    payload.setdefault("workflow", "eval-smoke")
                    payload.setdefault("citability", "REAL_HOST")
                    payload.setdefault("head_sha", HEAD_SHA)
                    payload.setdefault("dataset_sha256", "b" * 64)
                    payload.setdefault("built_config_sha256", "c" * 64)
                    payload.setdefault("config_template_sha256", CURRENT_SMOKE_CONFIG_SHA256)
                    payload.setdefault("gate_id", "gate-1")
                    payload.setdefault("subject_vendor", "anthropic")
                    payload.setdefault("judge_vendor", "openai")
                    payload.setdefault("judge_model", "gpt-6-astra")
                    payload.setdefault("max_output_tokens", 16384)
                    payload.setdefault("planned_calls", 2)
                    payload.setdefault("dispatched_calls", 2)
                    payload.setdefault("workflow_run_id", str(run_id))
                    payload.setdefault("workflow_run_attempt", str(self._run_attempt(run_id)))
                    if "proof_sha256" not in payload:
                        import hashlib
                        payload["proof_sha256"] = hashlib.sha256(json.dumps(
                            {k: v for k, v in payload.items() if k != "proof_sha256"},
                            sort_keys=True, separators=(",", ":"),
                        ).encode("utf-8")).hexdigest()
                if name == "ber-resume-manifest" and payload.get("schema") in REGISTERED_RESUME_MANIFEST_SCHEMAS:
                    plan = payload.setdefault("plan", {})
                    plan.setdefault("dispatch_sha", HEAD_SHA)
                    plan.setdefault("config_sha256", "e" * 64)
                    plan.setdefault("dataset_sha256", "f" * 64)
                    plan.setdefault("gate_id", "gate-1")
                    plan.setdefault("subject_vendors", ["anthropic"])
                    # Only the current schema is pinned to 16,384. The legacy
                    # 1.1.0 artifacts recorded 4,096 or omitted the field, so a
                    # default here would mask a real-payload refusal.
                    if payload.get("schema") == RESUME_MANIFEST_SCHEMA:
                        plan.setdefault("max_output_tokens", 16384)
            payload.pop("__no_defaults__", None)
            (out_dir / member).write_text(json.dumps(payload), encoding="utf-8")
            return SimpleNamespace(returncode=0, stdout="", stderr="")
        return SimpleNamespace(returncode=1, stdout="", stderr="unexpected")


HEAD_SHA = "a" * 40

#: Config-template identity recorded by the producer for the current committed
#: smoke config (tools/behavioral_eval_runner/live/config/pilot-a-smoke-config.json).
CURRENT_SMOKE_CONFIG_SHA256 = "c484d8d9eff3f53cfdeaf05f86701351c498bb3a0dae442d5ddae66f7b76877e"

#: Config-template identity recorded in the two identified 2026-10-31 historical
#: proofs (legacy cap 4,096; see tests/fixtures/live/smoke-proof/README.md).
LEGACY_SMOKE_CONFIG_SHA256 = "a90ae2ce140e8dfb4beb60a4caef4782e4fbf07702dc60ab73fa4527d3c4e1d0"

#: Verbatim historical proof fixtures (eval-smoke runs 41213566873 / 41179846875).
SMOKE_PROOF_FIXTURE_DIR = (
    REPO_ROOT / "tools/behavioral_eval_runner/tests/fixtures/live/smoke-proof"
)
LEGACY_PROOF_HEADS = {
    "41213566873": "1bfdf4a96966a97059270e383b6d0b90e1d88fa0",
    "41179846875": "cef6e91cbae4af1114f182dce0f0d98ebc146b65",
}
#: Identified artifactless historical run (2026-10-30 judge-output-contract
#: failure; zero artifacts); only the retained head prefix is registered.
FAILED_NO_PROOF_RUN_ID = "41167546138"
FAILED_NO_PROOF_HEAD = "88fdec73" + "0" * 32
#: Incident admission-refused run (zero spend; no artifacts).
INCIDENT_RUN_ID = "42134872074"
INCIDENT_RUN_HEAD = "2cad63e57d3d215f62a9d5f22b1f2b23cbaf8abf"
#: Registered preflight-only eval-run: no provider call, zero spend, and no
#: resume manifest because no case ran (artifact preflight-only.json).
PREFLIGHT_ONLY_RUN_ID = "41145124808"
PREFLIGHT_ONLY_HEAD = "877d6a27a36923cbdeff88a324640ec8cd8a7783"
#: The two inspected legacy 1.1.0 manifests, older first.
LEGACY_TRIAL_RUN_OLD = "41145221349"
LEGACY_TRIAL_RUN_NEW = "41213647310"


def run(run_id, attempt=1, conclusion="success", created_at=None, head_sha=HEAD_SHA):
    entry = {"id": run_id, "run_attempt": attempt, "status": "completed", "conclusion": conclusion, "head_sha": head_sha}
    if created_at is not None:
        entry["created_at"] = created_at
    return entry


def page(items, total=None):
    return {"total_count": len(items) if total is None else total, "workflow_runs": items}


_ARTIFACT_ID_SEQ = itertools.count(1000)


def artifact(name, artifact_id=None):
    """One artifact-listing record, with the distinct id/URL the API provides."""
    if artifact_id is None:
        artifact_id = next(_ARTIFACT_ID_SEQ)
    return {
        "id": artifact_id,
        "name": name,
        "archive_download_url": (
            "https://api.github.com/repos/o/r/actions/artifacts/"
            + str(artifact_id) + "/zip"
        ),
    }


def expired_artifact(name, artifact_id=None):
    """An artifact-listing record GitHub can return after retention expiry but
    before the artifact is physically removed."""
    record = artifact(name, artifact_id)
    record["expired"] = True
    return record


def smoke_proof(**overrides):
    """A complete current-config-shaped smoke proof payload with a valid self-hash.

    Used by the compatibility tests for synthetic current / mismatched-identity
    proofs; the historical proofs are loaded verbatim from the committed fixtures.
    """
    payload = {
        "schema": "ber-live-smoke-proof/1.0.0",
        "status": "PASS",
        "workflow": "eval-smoke",
        "citability": "REAL_HOST",
        "head_sha": HEAD_SHA,
        "dataset_sha256": "b" * 64,
        "built_config_sha256": "c" * 64,
        "config_template_sha256": CURRENT_SMOKE_CONFIG_SHA256,
        "gate_id": "gate-1",
        "subject_vendor": "anthropic",
        "judge_vendor": "openai",
        "judge_model": "gpt-6-astra",
        "max_output_tokens": 16384,
        "planned_calls": 2,
        "dispatched_calls": 2,
        "workflow_run_id": "42",
        "workflow_run_attempt": "1",
        "spent_cents": 150,
    }
    payload.update(overrides)
    import hashlib
    if "proof_sha256" not in overrides:
        payload["proof_sha256"] = hashlib.sha256(json.dumps(
            {k: v for k, v in payload.items() if k != "proof_sha256"},
            sort_keys=True, separators=(",", ":"),
        ).encode("utf-8")).hexdigest()
    return payload


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
            {"smoke": [page([run(77, attempt=2)])],
             "trial": [page([run(900)])]},
            {"77": [artifact("ber-live-smoke-proof")],
             "900": [artifact("ber-resume-manifest")]},
            {
                ("77", "ber-live-smoke-proof"): (
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
        self.assertEqual(history["smoke_spend_cents"], 224)

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
            reservation_cents=126,
        )
        denied = admit_paid_call(
            ceiling_cents=12_000,
            prior_ledger_spend_cents=history["ledger_spend_cents"],
            prior_smoke_spend_records=history["smoke_spend"],
            reservation_cents=127,
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
        self.assertEqual(history["smoke_spend_cents"], 150)

    def test_job1_scoped_trial_manifest_is_consumed_on_resume(self):
        # S4: a two-job run that ended after job 1 published only the
        # job-1-scoped manifest. A later dispatch must count that spend, not
        # treat the run as a missing (UNKNOWN) record.
        plan = {
            "dispatch_sha": HEAD_SHA,
            "config_sha256": "e" * 64,
            "dataset_sha256": "f" * 64,
            "gate_id": "gate-1",
            "subject_vendors": ["anthropic"],
            "max_output_tokens": 16384,
        }
        fake = FakeGH(
            {"smoke": [page([])], "trial": [page([run(901, conclusion="failure")])]},
            {"901": [artifact("ber-resume-manifest-job-1")]},
            {("901", "ber-resume-manifest-job-1"): (
                "manifest.json",
                {
                    "schema": "ber-resume-manifest/1.2.0",
                    "plan": plan,
                    "totals": {"spent_cents": 3_940},
                    "smoke_spend": {},
                },
            )},
        )
        trial = collect_latest_trial_spend(
            gh=fake, repository="o/r", work_dir=self.tmp,
        )
        self.assertEqual(trial["ledger_spend_cents"], 3_940)
        history = collect_allowance_history(
            gh=fake, repository="o/r", work_dir=self.tmp,
        )
        self.assertEqual(history["ledger_spend_cents"], 3_940)

    def test_job1_scoped_allowance_state_is_consumed_for_outstanding(self):
        # S4: a run that ended after job 1 (job 2 never ran) may hold only the
        # job-1-scoped reservation state. Its outstanding exposure must be
        # counted before the next dispatch, never silently dropped.
        fake = FakeGH(
            {"smoke": [page([])], "trial": [page([run(902, conclusion="failure")])]},
            {
                "902": [artifact("ber-shared-allowance-state-job-1")],
                "other": [],
            },
            {("902", "ber-shared-allowance-state-job-1"): (
                "allowance-state.json",
                {
                    "schema": "ber-reservation-state/1.0.0",
                    "status": "CANCELLED",
                    "outstanding_reservations_cents": 126,
                    "ledger_spend_cents": 3940,
                    "smoke_spend_cents": 18,
                    "ceiling_cents": 12000,
                },
            )},
        )
        state = collect_latest_allowance_state(
            gh=fake, repository="o/r", work_dir=self.tmp,
        )
        self.assertIsNotNone(state)
        self.assertEqual(state["outstanding_reservations_cents"], 126)

    def test_artifact_pagination_incomplete_refuses(self):
        from tools.behavioral_eval_runner.live import workflow_runtime as allowance_history
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

    def test_old_smoke_proof_schema_fails_closed_explicitly(self):
        # The legacy resume-manifest path is registered (covered by the tests
        # below); an older SMOKE-PROOF schema is still unregistered and refuses
        # before any field is interpreted.
        fake = FakeGH(
            {"smoke": [page([run(42)])], "trial": [page([])]},
            {"42": [artifact("ber-live-smoke-proof")]},
            {
                ("42", "ber-live-smoke-proof"): (
                    "smoke-proof.json",
                    {"schema": "ber-live-smoke-proof/0.9.0", "spent_cents": 1},
                ),
            },
        )
        with self.assertRaises(ValueError) as caught:
            collect_allowance_history(gh=fake, repository="o/r", work_dir=self.tmp)
        self.assertIn("unsupported smoke proof schema", str(caught.exception))

    def _legacy_manifest(self, spent_cents, max_output_tokens=4_096, include_cap=True):
        payload = {
            "schema": LEGACY_RESUME_MANIFEST_SCHEMA,
            "totals": {"spent_cents": spent_cents},
        }
        if include_cap:
            # The real 2026-10-31 artifact records 4,096; the older one omits
            # the field (include_cap=False).
            payload["plan"] = {"max_output_tokens": max_output_tokens}
        return payload

    def _legacy_two_run_fake(self, older_spent, newer_spent, same_created_at=False):
        older_at = "2026-11-06T00:00:00Z"
        newer_at = older_at if same_created_at else "2026-11-08T00:00:00Z"
        return FakeGH(
            {"smoke": [page([])], "trial": [page([
                run(LEGACY_TRIAL_RUN_NEW, created_at=newer_at),
                run(LEGACY_TRIAL_RUN_OLD, created_at=older_at),
            ])]},
            {
                LEGACY_TRIAL_RUN_OLD: [artifact("ber-resume-manifest")],
                LEGACY_TRIAL_RUN_NEW: [artifact("ber-resume-manifest")],
            },
            {
                (LEGACY_TRIAL_RUN_OLD, "ber-resume-manifest"): (
                    "manifest.json", self._legacy_manifest(older_spent),
                ),
                (LEGACY_TRIAL_RUN_NEW, "ber-resume-manifest"): (
                    "manifest.json", self._legacy_manifest(newer_spent),
                ),
            },
        )

    def test_legacy_resume_manifest_is_accepted_and_its_totals_used(self):
        # (a) 1.1.0 is a registered reader path: its plan provenance is validated
        # by 1.2.0's checks except the recorded legacy output cap (absent or a
        # bounded positive int), its absent smoke_spend normalizes to {}, and its
        # totals.spent_cents is used as the cumulative trial total.
        fake = FakeGH(
            {"smoke": [page([])], "trial": [page([
                run(LEGACY_TRIAL_RUN_NEW, created_at="2026-11-08T12:00:00Z"),
            ])]},
            {LEGACY_TRIAL_RUN_NEW: [artifact("ber-resume-manifest")]},
            {(LEGACY_TRIAL_RUN_NEW, "ber-resume-manifest"): (
                "manifest.json", self._legacy_manifest(222),
            )},
        )
        trial = collect_latest_trial_spend(
            gh=fake, repository="o/r", work_dir=self.tmp,
        )
        # The collector's output schema stays current; the legacy manifest is
        # recorded as source provenance, never as an emitted output schema.
        self.assertEqual(trial["schema"], RESUME_MANIFEST_SCHEMA)
        self.assertEqual(trial["source_schema"], LEGACY_RESUME_MANIFEST_SCHEMA)
        self.assertEqual(trial["ledger_spend_cents"], 222)
        self.assertEqual(trial["smoke_spend"], {})
        history = collect_allowance_history(
            gh=fake, repository="o/r", work_dir=self.tmp,
        )
        self.assertEqual(history["ledger_spend_cents"], 222)
        self.assertEqual(history["source_schema"]["trial"], LEGACY_RESUME_MANIFEST_SCHEMA)
        self.assertEqual(history["smoke_spend_cents"], PRESERVED_HISTORICAL_SMOKE_CENTS)

    def _legacy_cap_fake(self, max_output_tokens=4_096, include_cap=True):
        payload = self._legacy_manifest(
            222,
            max_output_tokens=max_output_tokens,
            include_cap=include_cap,
        )
        return FakeGH(
            {"smoke": [page([])], "trial": [page([
                run(LEGACY_TRIAL_RUN_NEW, created_at="2026-11-08T12:00:00Z"),
            ])]},
            {LEGACY_TRIAL_RUN_NEW: [artifact("ber-resume-manifest")]},
            {(LEGACY_TRIAL_RUN_NEW, "ber-resume-manifest"): (
                "manifest.json", payload,
            )},
        )

    def test_real_legacy_manifest_fixtures_are_consumed(self):
        # The committed fixtures are byte-for-byte copies of the two published
        # 1.1.0 artifacts: run 41213647310 records cap 4,096 / totals 222 and
        # run 41145221349 omits the cap / records totals 8. Both must pass the
        # registered legacy reader, and the newest cumulative total is 222.
        fixture_dir = (
            REPO_ROOT
            / "tools/behavioral_eval_runner/tests/fixtures/live/legacy-resume-manifest"
        )
        older = json.loads(
            (fixture_dir / "ber-resume-manifest-run-41145221349.json").read_text(
                encoding="utf-8",
            )
        )
        newer = json.loads(
            (fixture_dir / "ber-resume-manifest-run-41213647310.json").read_text(
                encoding="utf-8",
            )
        )
        self.assertEqual(older["schema"], LEGACY_RESUME_MANIFEST_SCHEMA)
        self.assertEqual(older["totals"]["spent_cents"], 8)
        self.assertNotIn("max_output_tokens", older["plan"])
        self.assertEqual(newer["schema"], LEGACY_RESUME_MANIFEST_SCHEMA)
        self.assertEqual(newer["totals"]["spent_cents"], 222)
        self.assertEqual(newer["plan"]["max_output_tokens"], 4_096)
        fake = FakeGH(
            {"smoke": [page([])], "trial": [page([
                run(41213647310, created_at=newer["created_at"],
                    head_sha=newer["plan"]["dispatch_sha"]),
                run(41145221349, created_at=older["created_at"],
                    head_sha=older["plan"]["dispatch_sha"]),
            ])]},
            {
                "41213647310": [artifact("ber-resume-manifest")],
                "41145221349": [artifact("ber-resume-manifest")],
            },
            {
                ("41213647310", "ber-resume-manifest"): ("manifest.json", newer),
                ("41145221349", "ber-resume-manifest"): ("manifest.json", older),
            },
        )
        trial = collect_latest_trial_spend(
            gh=fake, repository="o/r", work_dir=self.tmp,
        )
        self.assertEqual(trial["schema"], RESUME_MANIFEST_SCHEMA)
        self.assertEqual(trial["source_schema"], LEGACY_RESUME_MANIFEST_SCHEMA)
        self.assertEqual(trial["ledger_spend_cents"], 222)
        self.assertEqual(trial["smoke_spend"], {})

    def test_legacy_recorded_output_cap_accepts_absent_or_bounded_positive_int(self):
        # The real legacy cap is absent (41145221349) or 4,096 (41213647310);
        # any positive int up to the pinned cap is the recorded legacy budget.
        for cap in (1, 4_096, 16_384):
            with self.subTest(cap=cap):
                trial = collect_latest_trial_spend(
                    gh=self._legacy_cap_fake(cap),
                    repository="o/r", work_dir=self.tmp,
                )
                self.assertEqual(trial["source_schema"], LEGACY_RESUME_MANIFEST_SCHEMA)
                self.assertEqual(trial["ledger_spend_cents"], 222)
        absent = collect_latest_trial_spend(
            gh=self._legacy_cap_fake(include_cap=False),
            repository="o/r", work_dir=self.tmp,
        )
        self.assertEqual(absent["source_schema"], LEGACY_RESUME_MANIFEST_SCHEMA)
        self.assertEqual(absent["ledger_spend_cents"], 222)

    def test_legacy_recorded_output_cap_negative_values_refuse(self):
        # Fail closed on every present value that is not a positive bounded int:
        # bool, non-int, null, zero, negative and above the pinned cap.
        for cap in (0, -1, True, 20_000, None, "4096", 4_096.0):
            with self.subTest(cap=cap):
                with self.assertRaises(ValueError) as caught:
                    collect_latest_trial_spend(
                        gh=self._legacy_cap_fake(cap),
                        repository="o/r", work_dir=self.tmp,
                    )
                self.assertIn(
                    "legacy trial plan output cap", str(caught.exception),
                )

    def test_current_schema_output_cap_must_stay_pinned(self):
        # 1.2.0 keeps the exact pinned cap: 4,096, zero, an over-cap value, a
        # bool/float and an absent field all refuse.
        for cap in (4_096, 0, 20_000, True, 16_384.0):
            with self.subTest(cap=cap):
                payload = {
                    "schema": RESUME_MANIFEST_SCHEMA,
                    "totals": {"spent_cents": 222},
                    "plan": {"max_output_tokens": cap},
                }
                fake = FakeGH(
                    {"smoke": [page([])], "trial": [page([
                        run(900, created_at="2026-11-08T12:00:00Z"),
                    ])]},
                    {"900": [artifact("ber-resume-manifest")]},
                    {("900", "ber-resume-manifest"): ("manifest.json", payload)},
                )
                with self.assertRaises(ValueError) as caught:
                    collect_latest_trial_spend(
                        gh=fake, repository="o/r", work_dir=self.tmp,
                    )
                self.assertIn(
                    "trial plan output cap is not the pinned 16384",
                    str(caught.exception),
                )
        absent = {
            "schema": RESUME_MANIFEST_SCHEMA,
            "totals": {"spent_cents": 222},
            "plan": {
                "dispatch_sha": HEAD_SHA,
                "config_sha256": "e" * 64,
                "dataset_sha256": "f" * 64,
                "gate_id": "gate-1",
                "subject_vendors": ["anthropic"],
            },
            "__no_defaults__": True,
        }
        fake = FakeGH(
            {"smoke": [page([])], "trial": [page([
                run(900, created_at="2026-11-08T12:00:00Z"),
            ])]},
            {"900": [artifact("ber-resume-manifest")]},
            {("900", "ber-resume-manifest"): ("manifest.json", absent)},
        )
        with self.assertRaises(ValueError) as caught:
            collect_latest_trial_spend(
                gh=fake, repository="o/r", work_dir=self.tmp,
            )
        self.assertIn(
            "trial plan output cap is not the pinned 16384", str(caught.exception),
        )

    def test_legacy_resume_manifest_plan_is_validated_like_current(self):
        # The legacy reader path is not a looser contract: the same plan fields
        # are checked, starting with the dispatch head bound to the run head.
        payload = self._legacy_manifest(222)
        payload["plan"] = {
            "dispatch_sha": "b" * 40,
            "config_sha256": "e" * 64,
            "dataset_sha256": "f" * 64,
            "gate_id": "gate-1",
            "subject_vendors": ["anthropic"],
            "max_output_tokens": 16384,
        }
        fake = FakeGH(
            {"smoke": [page([])], "trial": [page([
                run(LEGACY_TRIAL_RUN_NEW, created_at="2026-11-08T12:00:00Z"),
            ])]},
            {LEGACY_TRIAL_RUN_NEW: [artifact("ber-resume-manifest")]},
            {(LEGACY_TRIAL_RUN_NEW, "ber-resume-manifest"): (
                "manifest.json", payload,
            )},
        )
        with self.assertRaises(ValueError) as caught:
            collect_latest_trial_spend(
                gh=fake, repository="o/r", work_dir=self.tmp,
            )
        self.assertIn("dispatch head", str(caught.exception))

    def test_legacy_differing_totals_newest_wins_when_not_regressive(self):
        # (b) The two legacy manifests are sequential cumulative totals, not
        # independent deltas. The newest (created_at, tie-break run id) wins and
        # its total must be >= every older legacy total; totals are never summed.
        trial = collect_latest_trial_spend(
            gh=self._legacy_two_run_fake(8, 222), repository="o/r", work_dir=self.tmp,
        )
        self.assertEqual(trial["ledger_spend_cents"], 222)
        self.assertEqual(trial["schema"], RESUME_MANIFEST_SCHEMA)
        self.assertEqual(trial["source_schema"], LEGACY_RESUME_MANIFEST_SCHEMA)
        # Equal created_at: the higher run id is the newer record.
        tied = collect_latest_trial_spend(
            gh=self._legacy_two_run_fake(8, 222, same_created_at=True),
            repository="o/r", work_dir=self.tmp,
        )
        self.assertEqual(tied["ledger_spend_cents"], 222)

    def test_legacy_totals_regression_fails_closed(self):
        # (b, negative) A newest legacy total below an older legacy total is a
        # regression in a cumulative history; it refuses instead of being summed
        # or silently preferring the larger number.
        with self.assertRaises(ValueError) as caught:
            collect_latest_trial_spend(
                gh=self._legacy_two_run_fake(222, 8),
                repository="o/r", work_dir=self.tmp,
            )
        self.assertIn("regress", str(caught.exception))

    def test_legacy_manifest_without_created_at_fails_closed(self):
        # "Newest" is the authority rule, so an unorderable legacy record refuses
        # rather than being guessed from listing order.
        fake = FakeGH(
            {"smoke": [page([])], "trial": [page([run(LEGACY_TRIAL_RUN_NEW)])]},
            {LEGACY_TRIAL_RUN_NEW: [artifact("ber-resume-manifest")]},
            {(LEGACY_TRIAL_RUN_NEW, "ber-resume-manifest"): (
                "manifest.json", self._legacy_manifest(222),
            )},
        )
        with self.assertRaises(ValueError) as caught:
            collect_latest_trial_spend(
                gh=fake, repository="o/r", work_dir=self.tmp,
            )
        self.assertIn("created_at", str(caught.exception))

    def _preflight_only_fake(self, conclusion="success", head_sha=PREFLIGHT_ONLY_HEAD,
                             attempt=1):
        entry = {
            "id": PREFLIGHT_ONLY_RUN_ID,
            "run_attempt": attempt,
            "status": "completed",
            "conclusion": conclusion,
            "head_sha": head_sha,
            "created_at": "2026-11-05T00:00:00Z",
        }
        return FakeGH(
            {"smoke": [page([])], "trial": [page([entry])]},
            {PREFLIGHT_ONLY_RUN_ID: []}, {},
        )

    def test_registered_preflight_only_run_is_skipped_as_zero(self):
        # (c) The identified preflight-only run produced no resume manifest
        # because no case ran. Its exact registry entry makes it $0, not UNKNOWN.
        fake = self._preflight_only_fake()
        trial = collect_latest_trial_spend(
            gh=fake, repository="o/r", work_dir=self.tmp,
        )
        self.assertEqual(trial["ledger_spend_cents"], PRESERVED_HISTORICAL_LEDGER_CENTS)
        self.assertTrue(trial["preserved_historical"])
        self.assertEqual(fake.download_requests, [])
        history = collect_allowance_history(
            gh=fake, repository="o/r", work_dir=self.tmp,
        )
        self.assertEqual(history["ledger_spend_cents"], PRESERVED_HISTORICAL_LEDGER_CENTS)
        self.assertEqual(history["smoke_spend_cents"], PRESERVED_HISTORICAL_SMOKE_CENTS)

    def test_registered_preflight_only_run_metadata_mismatch_refuses(self):
        # (c, negative) Conclusion, head and attempt are all part of the
        # paid-attempt identity; a mismatch refuses instead of booking $0.
        cases = [
            ({"conclusion": "failure"}, "recorded conclusion"),
            ({"head_sha": "b" * 40}, "recorded head"),
            ({"attempt": 2}, "recorded attempt"),
        ]
        for overrides, expected in cases:
            with self.subTest(overrides=overrides):
                with self.assertRaises(ValueError) as caught:
                    collect_latest_trial_spend(
                        gh=self._preflight_only_fake(**overrides),
                        repository="o/r", work_dir=self.tmp,
                    )
                self.assertIn("registered preflight-only trial run", str(caught.exception))
                self.assertIn(expected, str(caught.exception))

    def test_unregistered_artifactless_trial_run_stays_unknown_not_zero(self):
        # (c, negative) The registry is exact-match only: any other artifactless
        # ended trial run remains UNKNOWN and keeps admission blocked.
        fake = FakeGH(
            {"smoke": [page([])], "trial": [page([run(999_000_001)])]},
            {"999000001": []}, {},
        )
        with self.assertRaises(ValueError) as caught:
            collect_latest_trial_spend(
                gh=fake, repository="o/r", work_dir=self.tmp,
            )
        self.assertIn("UNKNOWN", str(caught.exception))

    def test_unknown_resume_manifest_schema_still_fails_closed(self):
        # (d) Only the registered tuple is readable; an unknown schema refuses
        # before its fields are interpreted.
        fake = FakeGH(
            {"smoke": [page([])], "trial": [page([run(900)])]},
            {"900": [artifact("ber-resume-manifest")]},
            {("900", "ber-resume-manifest"): (
                "manifest.json",
                {"schema": "ber-resume-manifest/2.0.0",
                 "totals": {"spent_cents": 222}},
            )},
        )
        with self.assertRaises(ValueError) as caught:
            collect_latest_trial_spend(
                gh=fake, repository="o/r", work_dir=self.tmp,
            )
        self.assertIn("unsupported trial manifest schema", str(caught.exception))

    def test_legacy_compatibility_registries_are_exact_match_constants(self):
        self.assertEqual(
            REGISTERED_RESUME_MANIFEST_SCHEMAS,
            (RESUME_MANIFEST_SCHEMA, LEGACY_RESUME_MANIFEST_SCHEMA),
        )
        self.assertEqual(set(TRIAL_RUNS_WITHOUT_MANIFEST), {PREFLIGHT_ONLY_RUN_ID})
        registered = TRIAL_RUNS_WITHOUT_MANIFEST[PREFLIGHT_ONLY_RUN_ID]
        self.assertEqual(registered["spent_cents"], 0)
        self.assertEqual(registered["expected_conclusion"], "success")
        self.assertEqual(registered["head_sha"], PREFLIGHT_ONLY_HEAD)
        self.assertEqual(registered["expected_attempt"], 1)

    def _trial_history_fake(self, entries):
        """Build a fake trial history from explicit manifest records."""
        runs, artifacts, payloads = [], {}, {}
        for entry in entries:
            rid = str(entry["run_id"])
            runs.append(run(
                entry["run_id"],
                conclusion=entry.get("conclusion", "success"),
                created_at=entry.get("created_at"),
            ))
            artifacts[rid] = [artifact("ber-resume-manifest")]
            payload = {
                "schema": entry["schema"],
                "totals": {"spent_cents": entry["spent"]},
            }
            if "smoke_spend" in entry:
                payload["smoke_spend"] = entry["smoke_spend"]
            if "plan" in entry:
                payload["plan"] = entry["plan"]
            if entry.get("no_defaults"):
                payload["__no_defaults__"] = True
            payloads[(rid, "ber-resume-manifest")] = ("manifest.json", payload)
        return FakeGH({"smoke": [page([])], "trial": [page(runs)]}, artifacts, payloads)

    def test_modern_manifest_newer_than_legacy_is_authoritative(self):
        # Mixed history: a newer 1.2.0 record wins over an older 1.1.0 record.
        fake = self._trial_history_fake([
            {"run_id": LEGACY_TRIAL_RUN_NEW, "created_at": "2026-11-08T00:00:00Z",
             "schema": LEGACY_RESUME_MANIFEST_SCHEMA, "spent": 222},
            {"run_id": 900, "created_at": "2026-11-09T00:00:00Z",
             "schema": RESUME_MANIFEST_SCHEMA, "spent": 300},
        ])
        trial = collect_latest_trial_spend(
            gh=fake, repository="o/r", work_dir=self.tmp,
        )
        self.assertEqual(trial["schema"], RESUME_MANIFEST_SCHEMA)
        self.assertEqual(trial["ledger_spend_cents"], 300)

    def test_legacy_manifest_newer_than_modern_is_authoritative(self):
        # The legacy record is newest and non-regressive, so it wins.
        fake = self._trial_history_fake([
            {"run_id": 900, "created_at": "2026-11-06T00:00:00Z",
             "schema": RESUME_MANIFEST_SCHEMA, "spent": 200},
            {"run_id": LEGACY_TRIAL_RUN_NEW, "created_at": "2026-11-08T00:00:00Z",
             "schema": LEGACY_RESUME_MANIFEST_SCHEMA, "spent": 222},
        ])
        trial = collect_latest_trial_spend(
            gh=fake, repository="o/r", work_dir=self.tmp,
        )
        self.assertEqual(trial["schema"], RESUME_MANIFEST_SCHEMA)
        self.assertEqual(trial["source_schema"], LEGACY_RESUME_MANIFEST_SCHEMA)
        self.assertEqual(trial["ledger_spend_cents"], 222)

    def test_mixed_schema_regression_fails_closed(self):
        # Newest legacy total below an older modern total is a regression in a
        # cumulative history, whichever schema is newest.
        fake = self._trial_history_fake([
            {"run_id": 900, "created_at": "2026-11-06T00:00:00Z",
             "schema": RESUME_MANIFEST_SCHEMA, "spent": 300},
            {"run_id": LEGACY_TRIAL_RUN_NEW, "created_at": "2026-11-08T00:00:00Z",
             "schema": LEGACY_RESUME_MANIFEST_SCHEMA, "spent": 222},
        ])
        with self.assertRaises(ValueError) as caught:
            collect_latest_trial_spend(
                gh=fake, repository="o/r", work_dir=self.tmp,
            )
        self.assertIn("regress", str(caught.exception))

    def test_equal_modern_totals_choose_newest_modern_not_listing_order(self):
        # Multiple equal-total 1.2.0 manifests are valid (only DISTINCT totals
        # are ambiguous). The newest modern record must be selected by
        # (created_at, run id), not by listing order or by the first record.
        for listed in (
            ["modern_old", "legacy", "modern_new"],
            ["modern_new", "modern_old", "legacy"],
        ):
            with self.subTest(listing=listed):
                records = {
                    "modern_old": {
                        "run_id": 901, "created_at": "2026-11-07T00:00:00Z",
                        "schema": RESUME_MANIFEST_SCHEMA, "spent": 300,
                    },
                    "legacy": {
                        "run_id": LEGACY_TRIAL_RUN_NEW,
                        "created_at": "2026-11-08T00:00:00Z",
                        "schema": LEGACY_RESUME_MANIFEST_SCHEMA, "spent": 222,
                    },
                    "modern_new": {
                        "run_id": 902, "created_at": "2026-11-09T00:00:00Z",
                        "schema": RESUME_MANIFEST_SCHEMA, "spent": 300,
                        "smoke_spend": {"901": 50},
                    },
                }
                fake = self._trial_history_fake([records[name] for name in listed])
                trial = collect_latest_trial_spend(
                    gh=fake, repository="o/r", work_dir=self.tmp,
                )
                self.assertEqual(trial["schema"], RESUME_MANIFEST_SCHEMA)
                # 300 - 50 = 250, above the 222 preserved floor, so the chosen
                # record's smoke spend is observable.
                self.assertEqual(trial["ledger_spend_cents"], 250)

    def test_legacy_manifest_with_smoke_spend_is_still_validated(self):
        # A legacy record that DOES carry smoke_spend keeps the current
        # validation and ledger subtraction; absence is the only tolerant case.
        fake = self._trial_history_fake([
            {"run_id": LEGACY_TRIAL_RUN_NEW, "created_at": "2026-11-08T00:00:00Z",
             "schema": LEGACY_RESUME_MANIFEST_SCHEMA, "spent": 250,
             "smoke_spend": {"901": 20}},
        ])
        trial = collect_latest_trial_spend(
            gh=fake, repository="o/r", work_dir=self.tmp,
        )
        self.assertEqual(trial["ledger_spend_cents"], 230)

    def test_legacy_manifest_malformed_created_at_fails_closed(self):
        # A parseable-but-incomplete value (date only, or no timezone) could
        # silently change "newest" ordering, so it refuses like a bad string.
        for created_at in ("not-a-timestamp", "2026-11-08", "2026-11-08T00:00:00"):
            with self.subTest(created_at=created_at):
                fake = self._trial_history_fake([
                    {"run_id": LEGACY_TRIAL_RUN_NEW, "created_at": created_at,
                     "schema": LEGACY_RESUME_MANIFEST_SCHEMA, "spent": 222},
                ])
                with self.assertRaises(ValueError) as caught:
                    collect_latest_trial_spend(
                        gh=fake, repository="o/r", work_dir=self.tmp,
                    )
                self.assertIn("malformed created_at", str(caught.exception))

    def test_mixed_history_modern_without_created_at_fails_closed(self):
        # Recency decides cross-schema authority, so the modern candidate must
        # be orderable too in a mixed history; modern-only collection does not
        # require created_at.
        fake = self._trial_history_fake([
            {"run_id": LEGACY_TRIAL_RUN_NEW, "created_at": "2026-11-08T00:00:00Z",
             "schema": LEGACY_RESUME_MANIFEST_SCHEMA, "spent": 222},
            {"run_id": 900, "schema": RESUME_MANIFEST_SCHEMA, "spent": 300},
        ])
        with self.assertRaises(ValueError) as caught:
            collect_latest_trial_spend(
                gh=fake, repository="o/r", work_dir=self.tmp,
            )
        self.assertIn("created_at", str(caught.exception))

    def test_legacy_manifest_missing_config_sha_fails_closed(self):
        # The legacy path validates every plan field, not only dispatch_sha.
        plan = {
            "dispatch_sha": HEAD_SHA,
            "dataset_sha256": "f" * 64,
            "gate_id": "gate-1",
            "subject_vendors": ["anthropic"],
            "max_output_tokens": 16384,
        }
        fake = self._trial_history_fake([
            {"run_id": LEGACY_TRIAL_RUN_NEW, "created_at": "2026-11-08T00:00:00Z",
             "schema": LEGACY_RESUME_MANIFEST_SCHEMA, "spent": 222,
             "plan": plan, "no_defaults": True},
        ])
        with self.assertRaises(ValueError) as caught:
            collect_latest_trial_spend(
                gh=fake, repository="o/r", work_dir=self.tmp,
            )
        self.assertIn("config_sha256", str(caught.exception))

    def test_registered_preflight_only_nonzero_registry_spend_refuses(self):
        # A registry entry that claims spend cannot be skipped as $0.
        registered = dict(TRIAL_RUNS_WITHOUT_MANIFEST[PREFLIGHT_ONLY_RUN_ID])
        registered["spent_cents"] = 5
        with mock.patch.dict(
            workflow_runtime.TRIAL_RUNS_WITHOUT_MANIFEST,
            {PREFLIGHT_ONLY_RUN_ID: registered},
        ):
            with self.assertRaises(ValueError) as caught:
                collect_latest_trial_spend(
                    gh=self._preflight_only_fake(),
                    repository="o/r", work_dir=self.tmp,
                )
        self.assertIn("non-zero spend", str(caught.exception))

    def test_non_numeric_run_id_in_legacy_history_fails_closed(self):
        fake = self._trial_history_fake([
            {"run_id": "run-abc", "created_at": "2026-11-08T00:00:00Z",
             "schema": LEGACY_RESUME_MANIFEST_SCHEMA, "spent": 222},
        ])
        with self.assertRaises(ValueError) as caught:
            collect_latest_trial_spend(
                gh=fake, repository="o/r", work_dir=self.tmp,
            )
        self.assertIn("non-numeric run id", str(caught.exception))

    def test_multiple_trial_manifests_with_different_totals_fail_closed(self):
        fake = FakeGH(
            {"smoke": [page([])], "trial": [page([run(900), run(901)])]},
            {"900": [artifact("ber-resume-manifest")],
             "901": [artifact("ber-resume-manifest")]},
            {
                ("900", "ber-resume-manifest"): (
                    "manifest.json",
                    {"schema": "ber-resume-manifest/1.2.0",
                     "totals": {"spent_cents": 100}, "smoke_spend": {}},
                ),
                ("901", "ber-resume-manifest"): (
                    "manifest.json",
                    {"schema": "ber-resume-manifest/1.2.0",
                     "totals": {"spent_cents": 200}, "smoke_spend": {}},
                ),
            },
        )
        with self.assertRaises(ValueError) as caught:
            collect_allowance_history(gh=fake, repository="o/r", work_dir=self.tmp)
        # (e) The 1.2.0 different-totals ambiguity refusal is preserved.
        self.assertIn("different totals", str(caught.exception))

    def test_preserved_18c_not_doubled_when_history_present(self):
        fake = FakeGH(
            {"smoke": [page([run(42)])], "trial": [page([])]},
            {"42": [artifact("ber-live-smoke-proof")]},
            {("42", "ber-live-smoke-proof"): (
                "smoke-proof.json",
                {"schema": "ber-live-smoke-proof/1.0.0", "spent_cents": 150},
            )},
        )
        history = collect_allowance_history(gh=fake, repository="o/r", work_dir=self.tmp)
        self.assertEqual(history["smoke_spend_cents"], 150)
        empty = FakeGH({"smoke": [page([])], "trial": [page([])]}, {}, {})
        preserved = collect_allowance_history(gh=empty, repository="o/r", work_dir=self.tmp)
        self.assertEqual(preserved["smoke_spend_cents"], 18)

    def test_smoke_history_below_preserved_floor_fails_closed(self):
        fake = FakeGH(
            {"smoke": [page([run(42)])], "trial": [page([])]},
            {"42": [artifact("ber-live-smoke-proof")]},
            {("42", "ber-live-smoke-proof"): (
                "smoke-proof.json",
                {"schema": "ber-live-smoke-proof/1.0.0", "spent_cents": 10},
            )},
        )
        with self.assertRaises(ValueError):
            collect_allowance_history(gh=fake, repository="o/r", work_dir=self.tmp)

    def test_missing_trial_manifest_refuses(self):
        fake = FakeGH(
            {"smoke": [page([])], "trial": [page([run(900)])]},
            {"900": []}, {},
        )
        with self.assertRaises(ValueError):
            collect_allowance_history(gh=fake, repository="o/r", work_dir=self.tmp)

    def _proof_with(self, **overrides):
        # F-B1: both identity sites use the real current committed config
        # identity, and the self-hash is computed over the payload as the fake
        # download writes it (the test-only __no_defaults__ marker is excluded).
        # This keeps every existing negative test failing for the check it names
        # rather than for an incidental hash mismatch.
        payload = {
            "__no_defaults__": True,
            "schema": "ber-live-smoke-proof/1.0.0",
            "status": "PASS",
            "workflow": "eval-smoke",
            "citability": "REAL_HOST",
            "head_sha": HEAD_SHA,
            "dataset_sha256": "b" * 64,
            "built_config_sha256": "c" * 64,
            "config_template_sha256": CURRENT_SMOKE_CONFIG_SHA256,
            "gate_id": "gate-1",
            "subject_vendor": "anthropic",
            "judge_vendor": "openai",
            "judge_model": "gpt-6-astra",
            "max_output_tokens": 16384,
            "planned_calls": 2,
            "dispatched_calls": 2,
            "workflow_run_id": "42",
            "workflow_run_attempt": "1",
            "spent_cents": 150,
        }
        payload.update(overrides)
        import hashlib
        body = {k: v for k, v in payload.items() if k not in ("proof_sha256", "__no_defaults__")}
        if "proof_sha256" not in overrides:
            payload["proof_sha256"] = hashlib.sha256(json.dumps(
                body, sort_keys=True, separators=(",", ":"),
            ).encode("utf-8")).hexdigest()
        return payload

    def _history_with_proof(self, payload):
        return FakeGH(
            {"smoke": [page([run(42)])], "trial": [page([])]},
            {"42": [artifact("ber-live-smoke-proof")]},
            {("42", "ber-live-smoke-proof"): ("smoke-proof.json", payload)},
        )

    def test_provenance_required_fields_missing_reject(self):
        required = ["head_sha", "workflow", "dataset_sha256", "built_config_sha256",
                    "config_template_sha256", "gate_id", "subject_vendor", "judge_vendor",
                    "judge_model", "status", "citability",
                    "workflow_run_id", "workflow_run_attempt"]
        for key in required:
            payload = self._proof_with()
            del payload[key]
            with self.subTest(key=key):
                with self.assertRaises(ValueError):
                    collect_smoke_proof_spends(
                        gh=self._history_with_proof(payload), repository="o/r", work_dir=self.tmp
                    )

    def test_provenance_mismatch_and_untrusted_reject(self):
        cases = [
            {"head_sha": "f" * 40},
            {"workflow": "other-workflow"},
            {"citability": "SYNTHETIC"},
            {"status": "UNKNOWN"},
            {"judge_model": ""},
            {"judge_model": "evil-model"},
            {"subject_vendor": "evil"},
            {"judge_vendor": "evil"},
            {"proof_sha256": "0" * 64},
        ]
        for overrides in cases:
            payload = self._proof_with(**overrides)
            with self.subTest(overrides=overrides):
                with self.assertRaises(ValueError):
                    collect_smoke_proof_spends(
                        gh=self._history_with_proof(payload), repository="o/r", work_dir=self.tmp
                    )

class SmokeProofCompatibilityTests(unittest.TestCase):
    """Legacy smoke-proof compatibility, artifactless-run registry and preserved floor.

    Covers plan AC-01..AC-04, AC-10..AC-12 and NC-01..NC-14 for the shared
    allowance-history collector. Every test is offline: gh is FakeGH and the
    historical proofs are the committed verbatim fixture copies.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def _legacy_proof(self, run_id):
        path = SMOKE_PROOF_FIXTURE_DIR / ("smoke-proof-run-" + str(run_id) + ".json")
        return json.loads(path.read_text(encoding="utf-8"))

    def _run_with_head(self, run_id, head_sha, conclusion="success"):
        entry = run(run_id, conclusion=conclusion)
        entry["head_sha"] = head_sha
        return entry

    def _legacy_history_parts(self):
        runs = [
            self._run_with_head(41213566873, LEGACY_PROOF_HEADS["41213566873"]),
            self._run_with_head(41179846875, LEGACY_PROOF_HEADS["41179846875"]),
        ]
        artifacts = {
            "41213566873": [artifact("ber-live-smoke-proof")],
            "41179846875": [artifact("ber-live-smoke-proof")],
        }
        payloads = {
            ("41213566873", "ber-live-smoke-proof"): (
                "smoke-proof.json", self._legacy_proof("41213566873"),
            ),
            ("41179846875", "ber-live-smoke-proof"): (
                "smoke-proof.json", self._legacy_proof("41179846875"),
            ),
        }
        return runs, artifacts, payloads

    def _history(self, runs, artifacts, payloads, current_run_id="9999999999"):
        fake = FakeGH({"smoke": [page(runs)], "trial": [page([])]}, artifacts, payloads)
        return collect_allowance_history(
            gh=fake, repository="o/r", work_dir=self.tmp,
            current_run_id=current_run_id,
        )

    def _identified_history(self, current_run_id):
        runs, artifacts, payloads = self._legacy_history_parts()
        runs.append(self._run_with_head(
            FAILED_NO_PROOF_RUN_ID, FAILED_NO_PROOF_HEAD, conclusion="failure",
        ))
        runs.append(self._run_with_head(
            INCIDENT_RUN_ID, INCIDENT_RUN_HEAD, conclusion="failure",
        ))
        artifacts[FAILED_NO_PROOF_RUN_ID] = []
        artifacts[INCIDENT_RUN_ID] = []
        return self._history(runs, artifacts, payloads, current_run_id=current_run_id)

    def _admission(self, smoke_records, reservation_cents=200):
        return admit_paid_call(
            ceiling_cents=12_000,
            prior_ledger_spend_cents=222,
            prior_smoke_spend_records=smoke_records,
            reservation_cents=reservation_cents,
        )

    def _proof_fake(self, payload):
        return FakeGH(
            {"smoke": [page([run(42)])], "trial": [page([])]},
            {"42": [artifact("ber-live-smoke-proof")]},
            {("42", "ber-live-smoke-proof"): ("smoke-proof.json", payload)},
        )

    def test_legacy_smoke_proofs_are_accepted_by_recorded_config_identity(self):
        # AC-04: both identified legacy proofs are accepted through the recorded
        # config-identity registry and their recorded 6c each is counted. This uses
        # the per-run collector directly; the preserved-floor reconciliation is
        # covered by the full identified-history replay test below.
        runs, artifacts, payloads = self._legacy_history_parts()
        records = collect_smoke_proof_spends(
            gh=FakeGH({"smoke": [page(runs)], "trial": [page([])]}, artifacts, payloads),
            repository="o/r", work_dir=self.tmp,
        )
        self.assertEqual(len(records), 2)
        self.assertEqual(smoke_spend_total(records), 12)

    def test_current_smoke_proof_still_accepted(self):
        records = collect_smoke_proof_spends(
            gh=self._proof_fake(smoke_proof()), repository="o/r", work_dir=self.tmp,
        )
        self.assertEqual(len(records), 1)
        self.assertEqual(smoke_spend_total(records), 150)

    def test_identified_history_replays_to_preserved_totals_and_admission(self):
        # F-B2 incident-current view: the incident run is the in-flight run and is
        # excluded, so the preserved total comes from 3 records (two proofs + the
        # registered 6c artifactless run).
        history = self._identified_history(INCIDENT_RUN_ID)
        self.assertEqual(history["schema"], ALLOWANCE_HISTORY_SCHEMA)
        self.assertEqual(history["ledger_spend_cents"], 222)
        self.assertEqual(len(history["smoke_spend"]), 3)
        self.assertEqual(smoke_spend_total(history["smoke_spend"]), 18)
        admission = self._admission(history["smoke_spend"])
        self.assertTrue(admission["admitted"])
        self.assertEqual(admission["snapshot"]["combined_exposure_cents"], 440)
        self.assertEqual(admission["snapshot"]["remaining_cents"], 11_560)
        denied = self._admission(history["smoke_spend"], reservation_cents=11_761)
        self.assertFalse(denied["admitted"])

    def test_future_dispatch_view_counts_registered_zero_cent_run(self):
        # F-B2 future-dispatch view: when a later run is current, the incident
        # run is ended history and its registered 0c record is counted; totals and
        # admission stay invariant (4 records, smoke 18c, ledger 222c).
        history = self._identified_history("11111111111")
        self.assertEqual(history["ledger_spend_cents"], 222)
        self.assertEqual(len(history["smoke_spend"]), 4)
        self.assertEqual(smoke_spend_total(history["smoke_spend"]), 18)
        admission = self._admission(history["smoke_spend"])
        self.assertTrue(admission["admitted"])
        self.assertEqual(admission["snapshot"]["combined_exposure_cents"], 440)
        self.assertEqual(admission["snapshot"]["remaining_cents"], 11_560)

    def test_registered_artifactless_run_is_booked_and_unknown_run_still_refuses(self):
        failed = self._run_with_head(
            FAILED_NO_PROOF_RUN_ID, FAILED_NO_PROOF_HEAD, conclusion="failure",
        )
        fake = FakeGH(
            {"smoke": [page([failed])], "trial": [page([])]},
            {FAILED_NO_PROOF_RUN_ID: []}, {},
        )
        records = collect_smoke_proof_spends(gh=fake, repository="o/r", work_dir=self.tmp)
        self.assertEqual(len(records), 1)
        self.assertEqual(smoke_spend_total(records), 6)

        incident = self._run_with_head(
            INCIDENT_RUN_ID, INCIDENT_RUN_HEAD, conclusion="failure",
        )
        zero = FakeGH(
            {"smoke": [page([incident])], "trial": [page([])]},
            {INCIDENT_RUN_ID: []}, {},
        )
        zero_records = collect_smoke_proof_spends(
            gh=zero, repository="o/r", work_dir=self.tmp,
        )
        self.assertEqual(len(zero_records), 1)
        self.assertEqual(smoke_spend_total(zero_records), 0)

        unknown = FakeGH(
            {"smoke": [page([run(42, conclusion="failure")])], "trial": [page([])]},
            {"42": []}, {},
        )
        with self.assertRaises(ValueError) as caught:
            collect_smoke_proof_spends(gh=unknown, repository="o/r", work_dir=self.tmp)
        self.assertIn("UNKNOWN", str(caught.exception))

    def test_registered_artifactless_run_metadata_mismatch_refuses(self):
        cases = [
            self._run_with_head(FAILED_NO_PROOF_RUN_ID, FAILED_NO_PROOF_HEAD, conclusion="success"),
            self._run_with_head(FAILED_NO_PROOF_RUN_ID, "a" * 40, conclusion="failure"),
            self._run_with_head(INCIDENT_RUN_ID, "b" * 40, conclusion="failure"),
        ]
        for entry in cases:
            fake = FakeGH(
                {"smoke": [page([entry])], "trial": [page([])]},
                {str(entry["id"]): []}, {},
            )
            with self.subTest(run_id=entry["id"]):
                with self.assertRaises(ValueError):
                    collect_smoke_proof_spends(gh=fake, repository="o/r", work_dir=self.tmp)

    def _registered_fake(self, entry):
        return FakeGH(
            {"smoke": [page([entry])], "trial": [page([])]},
            {str(entry["id"]): []}, {},
        )

    def test_registered_artifactless_run_attempt_mismatch_refuses(self):
        # P2 (Codex 4501462748): the paid-attempt identity includes run_attempt.
        # A re-run keeps the run id/head and increments run_attempt, so a
        # non-original attempt must never receive the historical 6c/0c spend.
        cases = [
            (FAILED_NO_PROOF_RUN_ID, FAILED_NO_PROOF_HEAD, "6c"),
            (INCIDENT_RUN_ID, INCIDENT_RUN_HEAD, "0c"),
        ]
        for run_id, head_sha, label in cases:
            entry = self._run_with_head(run_id, head_sha, conclusion="failure")
            entry["run_attempt"] = 2
            with self.subTest(label=label):
                with self.assertRaises(ValueError) as caught:
                    collect_smoke_proof_spends(
                        gh=self._registered_fake(entry), repository="o/r", work_dir=self.tmp,
                    )
                self.assertIn("recorded attempt", str(caught.exception))

    def test_registered_artifactless_attempt_evidence_missing_fails_closed(self):
        # P2: missing attempt evidence is never guessed or defaulted. A missing
        # run attempt and a registry entry without a recorded attempt both refuse.
        entry = self._run_with_head(
            FAILED_NO_PROOF_RUN_ID, FAILED_NO_PROOF_HEAD, conclusion="failure",
        )
        del entry["run_attempt"]
        with self.assertRaises(ValueError) as caught:
            collect_smoke_proof_spends(
                gh=self._registered_fake(entry), repository="o/r", work_dir=self.tmp,
            )
        self.assertIn("readable attempt evidence", str(caught.exception))

        missing_recorded = {
            "spent_cents": 6,
            "expected_conclusion": "failure",
            "head_sha_prefix": "88fdec73",
        }
        entry = self._run_with_head(
            FAILED_NO_PROOF_RUN_ID, FAILED_NO_PROOF_HEAD, conclusion="failure",
        )
        with mock.patch.dict(
            workflow_runtime.SMOKE_RUNS_WITHOUT_PROOF,
            {FAILED_NO_PROOF_RUN_ID: missing_recorded},
            clear=False,
        ):
            with self.assertRaises(ValueError) as caught:
                collect_smoke_proof_spends(
                    gh=self._registered_fake(entry), repository="o/r", work_dir=self.tmp,
                )
            self.assertIn("no recorded attempt evidence", str(caught.exception))

        invalid_recorded = dict(missing_recorded)
        invalid_recorded["expected_attempt"] = "1"
        with mock.patch.dict(
            workflow_runtime.SMOKE_RUNS_WITHOUT_PROOF,
            {FAILED_NO_PROOF_RUN_ID: invalid_recorded},
            clear=False,
        ):
            with self.assertRaises(ValueError) as caught:
                collect_smoke_proof_spends(
                    gh=self._registered_fake(entry), repository="o/r", work_dir=self.tmp,
                )
            self.assertIn("no recorded attempt evidence", str(caught.exception))

    def test_registered_run_with_present_corrupt_artifact_refuses_without_booking(self):
        # F-B3/NC-12: artifact PRESENCE is checked before the registry, so a
        # present-but-corrupt proof for a registered run id hard-refuses and the
        # registered residual is never booked.
        failed = self._run_with_head(
            FAILED_NO_PROOF_RUN_ID, FAILED_NO_PROOF_HEAD, conclusion="failure",
        )
        fake = FakeGH(
            {"smoke": [page([failed])], "trial": [page([])]},
            {FAILED_NO_PROOF_RUN_ID: [artifact("ber-live-smoke-proof")]},
            {(FAILED_NO_PROOF_RUN_ID, "ber-live-smoke-proof"): (
                "smoke-proof.json", {"not": "a smoke proof"},
            )},
        )
        with self.assertRaises(ValueError) as caught:
            collect_smoke_proof_spends(gh=fake, repository="o/r", work_dir=self.tmp)
        self.assertIn("unsupported smoke proof schema", str(caught.exception))

    def _present_artifact_fake(self, entry, payload, artifact_names=None):
        names = artifact_names if artifact_names is not None else [
            artifact("ber-live-smoke-proof"),
        ]
        return FakeGH(
            {"smoke": [page([entry])], "trial": [page([])]},
            {str(entry["id"]): names},
            {(str(entry["id"]), "ber-live-smoke-proof"): (
                "smoke-proof.json", payload,
            )},
        )

    def test_present_artifact_attempt_mismatch_refuses(self):
        # P2 4501594132: a re-run API entry (attempt 2) must not accept the
        # retained attempt-1 artifact and record its 6c as attempt 2.
        cases = [
            (41213566873, LEGACY_PROOF_HEADS["41213566873"]),
            (41179846875, LEGACY_PROOF_HEADS["41179846875"]),
        ]
        for run_id, head_sha in cases:
            entry = self._run_with_head(run_id, head_sha)
            entry["run_attempt"] = 2
            fake = self._present_artifact_fake(entry, self._legacy_proof(str(run_id)))
            with self.subTest(run_id=run_id):
                with self.assertRaises(ValueError) as caught:
                    collect_smoke_proof_spends(gh=fake, repository="o/r", work_dir=self.tmp)
                self.assertIn("workflow run attempt does not match", str(caught.exception))

    def test_present_artifact_run_id_mismatch_refuses(self):
        fake = self._present_artifact_fake(run(42), smoke_proof(workflow_run_id="43"))
        with self.assertRaises(ValueError) as caught:
            collect_smoke_proof_spends(gh=fake, repository="o/r", work_dir=self.tmp)
        self.assertIn("workflow run id does not match", str(caught.exception))

    def test_present_artifact_missing_attempt_provenance_refuses(self):
        for key in ("workflow_run_id", "workflow_run_attempt"):
            payload = smoke_proof()
            del payload[key]
            payload["__no_defaults__"] = True
            with self.subTest(key=key):
                with self.assertRaises(ValueError) as caught:
                    collect_smoke_proof_spends(
                        gh=self._present_artifact_fake(run(42), payload),
                        repository="o/r", work_dir=self.tmp,
                    )
                self.assertIn(key, str(caught.exception))

    def test_present_artifact_missing_api_attempt_refuses(self):
        entry = run(42)
        del entry["run_attempt"]
        with self.assertRaises(ValueError) as caught:
            collect_smoke_proof_spends(
                gh=self._present_artifact_fake(entry, smoke_proof()),
                repository="o/r", work_dir=self.tmp,
            )
        self.assertIn("no readable attempt evidence", str(caught.exception))

    def test_duplicate_same_name_artifact_refuses(self):
        duplicate = [
            artifact("ber-live-smoke-proof"),
            artifact("ber-live-smoke-proof"),
        ]
        with self.assertRaises(ValueError) as caught:
            collect_smoke_proof_spends(
                gh=self._present_artifact_fake(run(42), smoke_proof(), duplicate),
                repository="o/r", work_dir=self.tmp,
            )
        self.assertIn("duplicate", str(caught.exception))
        self.assertIn("ambiguous selection", str(caught.exception))

    def test_present_artifact_matching_attempt_two_is_accepted(self):
        # The binding is not a blanket retry refusal: a re-run's own attempt-2
        # proof that matches the API attempt is accepted under the attempt-2 identity.
        entry = run(42, attempt=2)
        payload = smoke_proof(workflow_run_attempt="2")
        records = collect_smoke_proof_spends(
            gh=self._present_artifact_fake(entry, payload),
            repository="o/r", work_dir=self.tmp,
        )
        self.assertEqual(len(records), 1)
        self.assertEqual(smoke_spend_total(records), 150)
        self.assertIn("|42|2|smoke-proof", next(iter(records)))

    def test_present_artifact_attempt_one_binding_accepts(self):
        entry = self._run_with_head(41213566873, LEGACY_PROOF_HEADS["41213566873"])
        records = collect_smoke_proof_spends(
            gh=self._present_artifact_fake(entry, self._legacy_proof("41213566873")),
            repository="o/r", work_dir=self.tmp,
        )
        self.assertEqual(len(records), 1)
        self.assertEqual(smoke_spend_total(records), 6)
        self.assertIn("|41213566873|1|smoke-proof", next(iter(records)))

    def test_unknown_and_mismatched_smoke_config_identity_refuses(self):
        cases = [
            (smoke_proof(config_template_sha256="e" * 64), "config identity"),
            (
                smoke_proof(
                    config_template_sha256=CURRENT_SMOKE_CONFIG_SHA256,
                    max_output_tokens=4_096,
                ),
                "pinned value",
            ),
            (
                smoke_proof(
                    config_template_sha256=LEGACY_SMOKE_CONFIG_SHA256,
                    max_output_tokens=16_384,
                ),
                "pinned value",
            ),
        ]
        for payload, expected in cases:
            with self.subTest(
                config=payload["config_template_sha256"][:8],
                cap=payload["max_output_tokens"],
            ):
                with self.assertRaises(ValueError) as caught:
                    collect_smoke_proof_spends(
                        gh=self._proof_fake(payload), repository="o/r", work_dir=self.tmp,
                    )
                self.assertIn(expected, str(caught.exception))

    def test_legacy_proof_tamper_still_refused(self):
        payload = self._legacy_proof("41213566873")
        payload["spent_cents"] = payload["spent_cents"] + 1
        fake = FakeGH(
            {"smoke": [page([self._run_with_head(
                41213566873, LEGACY_PROOF_HEADS["41213566873"],
            )])], "trial": [page([])]},
            {"41213566873": [artifact("ber-live-smoke-proof")]},
            {("41213566873", "ber-live-smoke-proof"): (
                "smoke-proof.json", payload,
            )},
        )
        with self.assertRaises(ValueError) as caught:
            collect_smoke_proof_spends(gh=fake, repository="o/r", work_dir=self.tmp)
        self.assertIn("hash does not verify", str(caught.exception))

    def test_current_provenance_refusals_fire_for_their_named_reason(self):
        # F-B1: with the real current config identity in place, each existing
        # provenance refusal must still fire for the check it names.
        cases = [
            ({"head_sha": "f" * 40}, "head does not match"),
            ({"workflow": "other-workflow"}, "workflow is not eval-smoke"),
            ({"citability": "SYNTHETIC"}, "citability is not REAL_HOST"),
            ({"status": "UNKNOWN"}, "status is missing or untrusted"),
            ({"judge_model": ""}, "judge_model"),
            ({"judge_model": "evil-model"}, "judge model is not pinned"),
            ({"subject_vendor": "evil"}, "subject vendor is not pinned"),
            ({"judge_vendor": "evil"}, "judge vendor is not pinned"),
            ({"proof_sha256": "0" * 64}, "hash does not verify"),
        ]
        for overrides, expected in cases:
            payload = smoke_proof(**overrides)
            with self.subTest(expected=expected):
                with self.assertRaises(ValueError) as caught:
                    collect_smoke_proof_spends(
                        gh=self._proof_fake(payload), repository="o/r", work_dir=self.tmp,
                    )
                self.assertIn(expected, str(caught.exception))

    def test_compatibility_registries_are_exact_match_constants(self):
        # AC-05: the two registries are exact-match committed constants; repeated
        # collection must not mutate them, and there is no runtime/env override.
        self.assertEqual(
            dict(SMOKE_PROOF_CONFIG_PINS),
            {
                CURRENT_SMOKE_CONFIG_SHA256: 16_384,
                LEGACY_SMOKE_CONFIG_SHA256: 4_096,
            },
        )
        self.assertEqual(
            set(SMOKE_RUNS_WITHOUT_PROOF), {FAILED_NO_PROOF_RUN_ID, INCIDENT_RUN_ID},
        )
        failed = SMOKE_RUNS_WITHOUT_PROOF[FAILED_NO_PROOF_RUN_ID]
        self.assertEqual(failed["spent_cents"], 6)
        self.assertEqual(failed["expected_conclusion"], "failure")
        self.assertEqual(failed["expected_attempt"], 1)
        self.assertEqual(failed["head_sha_prefix"], "88fdec73")
        incident = SMOKE_RUNS_WITHOUT_PROOF[INCIDENT_RUN_ID]
        self.assertEqual(incident["spent_cents"], 0)
        self.assertEqual(incident["expected_conclusion"], "failure")
        self.assertEqual(incident["expected_attempt"], 1)
        self.assertEqual(incident["head_sha"], INCIDENT_RUN_HEAD)
        # AC-12/R3: the preserved floors are unchanged and not lowered.
        self.assertEqual(PRESERVED_HISTORICAL_SMOKE_CENTS, 18)
        self.assertEqual(PRESERVED_HISTORICAL_LEDGER_CENTS, 222)
        before = (
            dict(SMOKE_PROOF_CONFIG_PINS),
            {key: dict(value) for key, value in SMOKE_RUNS_WITHOUT_PROOF.items()},
        )
        self._identified_history(INCIDENT_RUN_ID)
        after = (
            dict(SMOKE_PROOF_CONFIG_PINS),
            {key: dict(value) for key, value in SMOKE_RUNS_WITHOUT_PROOF.items()},
        )
        self.assertEqual(before, after)

    def test_current_config_identity_matches_committed_template(self):
        # AC-07 drift guard: the registry current identity is the sha256 of the
        # committed smoke template and the mapped cap is its actual value; the
        # retained legacy proofs record exactly the registered legacy identity and
        # the unchanged committed gate identity; fixture bytes are pinned.
        config_bytes = (
            REPO_ROOT / "tools/behavioral_eval_runner/live/config/pilot-a-smoke-config.json"
        ).read_bytes()
        self.assertEqual(
            hashlib.sha256(config_bytes).hexdigest(), CURRENT_SMOKE_CONFIG_SHA256,
        )
        config = json.loads(config_bytes)
        self.assertEqual(
            config["max_output_tokens"],
            SMOKE_PROOF_CONFIG_PINS[CURRENT_SMOKE_CONFIG_SHA256],
        )
        gate_sha = hashlib.sha256((
            REPO_ROOT / "tools/behavioral_eval_runner/live/gates/pilot-a-apr161.json"
        ).read_bytes()).hexdigest()
        fixture_hashes = {
            "41213566873": "d1b18fe21bf8d56920b0551f9179c48a7b964f3572120b5dcee350e8935f8ade",
            "41179846875": "a202b4ac43a6ac20b4da518a1c0006ef5657efd6e6258a3a7809e223cac416f4",
        }
        for run_id, expected_hash in fixture_hashes.items():
            path = SMOKE_PROOF_FIXTURE_DIR / ("smoke-proof-run-" + run_id + ".json")
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected_hash)
            proof = self._legacy_proof(run_id)
            self.assertEqual(proof["config_template_sha256"], LEGACY_SMOKE_CONFIG_SHA256)
            self.assertEqual(
                SMOKE_PROOF_CONFIG_PINS[proof["config_template_sha256"]], 4_096,
            )
            self.assertEqual(proof["max_output_tokens"], 4_096)
            self.assertEqual(proof["gate_template_sha256"], gate_sha)


class _ArtifactListingFailureGH(FakeGH):
    """Fake gh whose per-run artifact listing command fails (unreadable)."""

    def __init__(self, runs):
        super().__init__({"smoke": [page(runs)], "trial": [page([])]}, {}, {})

    def __call__(self, args):
        if "/artifacts" in " ".join(args):
            return SimpleNamespace(returncode=1, stdout="", stderr="boom")
        return super().__call__(args)


class _IncompleteArtifactListingGH(FakeGH):
    """Fake gh whose artifact listing under-reports its immutable total."""

    def __init__(self, runs):
        super().__init__({"smoke": [page(runs)], "trial": [page([])]}, {}, {})

    def __call__(self, args):
        if "/artifacts" in " ".join(args):
            return SimpleNamespace(
                returncode=0,
                stdout=json.dumps([{"total_count": 2, "artifacts": []}]),
                stderr="",
            )
        return super().__call__(args)


class _UnderReportedArtifactListingGH(FakeGH):
    """Fake gh whose non-empty artifact page declares total_count=0."""

    def __init__(self, runs, artifacts):
        super().__init__(
            {"smoke": [page(runs)], "trial": [page([])]}, artifacts, {},
        )

    def __call__(self, args):
        joined = " ".join(args)
        if "/artifacts" in joined:
            run_id = joined.split("/actions/runs/")[1].split("/artifacts")[0]
            return SimpleNamespace(
                returncode=0,
                stdout=json.dumps([{
                    "total_count": 0,
                    "artifacts": self.artifacts.get(run_id, []),
                }]),
                stderr="",
            )
        return super().__call__(args)


class SmokeProofExpiryRegistryTests(unittest.TestCase):
    """Expiry-only recorded-hash classification for the two 2026-10-31 proofs.

    Adversarial matrix for the bounded exception that keeps shared-allowance
    history identical after GitHub retention deletes artifacts 13046737982 /
    13034581056 (eval-smoke.yml retention-days: 14; expected on/about
    2026-11-14). The exception is exact-match only: two committed run ids,
    recorded conclusion + full head SHA + run attempt, and the verbatim captured
    proof identities (2,253 B / a202b4ac... and 2,253 B / d1b18fe2...) committed
    as fixtures. Every test is offline: gh is FakeGH and no artifact is deleted.

    Positive: both runs booked at their recorded 6c when the artifact is absent,
    and history math/records equal the artifact-present behavior (incident view
    3 records / future view 4 records / smoke 18c / ledger 222c).

    Negative: unregistered artifactless runs stay UNKNOWN-not-zero; a registered
    run with mismatched conclusion/head/attempt (or no head) refuses; missing or
    invalid attempt evidence refuses and is never defaulted (repaired #997 paid-
    attempt identity); a present but malformed/tampered artifact refuses through
    the existing checks and never falls back to the registry; a readable artifact
    is validated by the repaired run id/attempt binding before the registry and
    books the artifact's own spend; unreadable/incomplete artifact listings
    refuse; a wrong or cross-bound recorded hash fails the drift guard;
    below-floor history still refuses.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    # -- helpers ---------------------------------------------------------

    def _legacy_proof(self, run_id):
        path = SMOKE_PROOF_FIXTURE_DIR / ("smoke-proof-run-" + str(run_id) + ".json")
        return json.loads(path.read_text(encoding="utf-8"))

    def _run_entry(self, run_id, head_sha, conclusion="success", attempt=1):
        entry = run(run_id, attempt=attempt, conclusion=conclusion)
        entry["head_sha"] = head_sha
        return entry

    def _expiry_runs(self):
        return [
            self._run_entry(41213566873, LEGACY_PROOF_HEADS["41213566873"]),
            self._run_entry(41179846875, LEGACY_PROOF_HEADS["41179846875"]),
        ]

    def _expired_history_parts(self):
        # Expiry scenario: GitHub retention deleted BOTH proof artifacts, so the
        # artifact listing is empty and no downloadable proof payload exists.
        artifacts = {"41213566873": [], "41179846875": []}
        return self._expiry_runs(), artifacts, {}

    def _present_history_parts(self):
        return (
            self._expiry_runs(),
            {
                "41213566873": [artifact("ber-live-smoke-proof")],
                "41179846875": [artifact("ber-live-smoke-proof")],
            },
            {
                ("41213566873", "ber-live-smoke-proof"): (
                    "smoke-proof.json", self._legacy_proof("41213566873"),
                ),
                ("41179846875", "ber-live-smoke-proof"): (
                    "smoke-proof.json", self._legacy_proof("41179846875"),
                ),
            },
        )

    def _identified_parts(self, expired):
        if expired:
            runs, artifacts, payloads = self._expired_history_parts()
        else:
            runs, artifacts, payloads = self._present_history_parts()
        runs.append(self._run_entry(
            FAILED_NO_PROOF_RUN_ID, FAILED_NO_PROOF_HEAD, conclusion="failure",
        ))
        runs.append(self._run_entry(
            INCIDENT_RUN_ID, INCIDENT_RUN_HEAD, conclusion="failure",
        ))
        artifacts[FAILED_NO_PROOF_RUN_ID] = []
        artifacts[INCIDENT_RUN_ID] = []
        return runs, artifacts, payloads

    def _history(self, runs, artifacts, payloads, current_run_id="9999999999"):
        fake = FakeGH({"smoke": [page(runs)], "trial": [page([])]}, artifacts, payloads)
        return collect_allowance_history(
            gh=fake, repository="o/r", work_dir=self.tmp,
            current_run_id=current_run_id,
        )

    def _identified_history(self, current_run_id, expired):
        return self._history(
            *self._identified_parts(expired), current_run_id=current_run_id,
        )

    def _smoke_records(self, runs, artifacts, payloads):
        fake = FakeGH({"smoke": [page(runs)], "trial": [page([])]}, artifacts, payloads)
        return collect_smoke_proof_spends(
            gh=fake, repository="o/r", work_dir=self.tmp,
        )

    def _admit(self, history, reservation_cents=200):
        return admit_paid_call(
            ceiling_cents=12_000,
            prior_ledger_spend_cents=history["ledger_spend_cents"],
            prior_smoke_spend_records=history["smoke_spend"],
            reservation_cents=reservation_cents,
        )

    # -- positive --------------------------------------------------------

    def test_both_expired_proofs_book_recorded_spend_exactly_as_artifact_path(self):
        expired_runs, expired_artifacts, no_payloads = self._expired_history_parts()
        expired_records = self._smoke_records(
            expired_runs, expired_artifacts, no_payloads,
        )
        self.assertEqual(len(expired_records), 2)
        self.assertEqual(smoke_spend_total(expired_records), 12)
        for run_id, registered in SMOKE_RUNS_WITH_EXPIRED_PROOF.items():
            matching = [
                key for key in expired_records
                if "|" + run_id + "|" in key
            ]
            self.assertEqual(len(matching), 1)
            self.assertEqual(expired_records[matching[0]], registered["spent_cents"])
            self.assertIn("|" + str(registered["expected_attempt"]) + "|", matching[0])
        present_records = self._smoke_records(*self._present_history_parts())
        self.assertEqual(expired_records, present_records)

    def test_expired_history_equals_artifact_present_history(self):
        for current_run_id in (INCIDENT_RUN_ID, "11111111111"):
            with self.subTest(current_run_id=current_run_id):
                expired = self._identified_history(current_run_id, expired=True)
                present = self._identified_history(current_run_id, expired=False)
                self.assertEqual(expired["schema"], present["schema"])
                self.assertEqual(expired["smoke_spend"], present["smoke_spend"])
                self.assertEqual(expired["smoke_spend_cents"], present["smoke_spend_cents"])
                self.assertEqual(expired["ledger_spend_cents"], present["ledger_spend_cents"])
                self.assertEqual(
                    expired["preserved_historical_ledger_cents"],
                    present["preserved_historical_ledger_cents"],
                )
                self.assertEqual(
                    expired["preserved_historical_smoke_cents"],
                    present["preserved_historical_smoke_cents"],
                )
                self.assertEqual(expired["source_schema"], present["source_schema"])
                self.assertEqual(self._admit(expired), self._admit(present))

    def test_expired_incident_and_future_views_keep_preserved_totals(self):
        incident = self._identified_history(INCIDENT_RUN_ID, expired=True)
        self.assertEqual(incident["ledger_spend_cents"], 222)
        self.assertEqual(len(incident["smoke_spend"]), 3)
        self.assertEqual(incident["smoke_spend_cents"], 18)
        incident_admission = self._admit(incident)
        self.assertTrue(incident_admission["admitted"])
        self.assertEqual(incident_admission["snapshot"]["combined_exposure_cents"], 440)
        self.assertEqual(incident_admission["snapshot"]["remaining_cents"], 11_560)
        denied = self._admit(incident, reservation_cents=11_761)
        self.assertFalse(denied["admitted"])

        future = self._identified_history("11111111111", expired=True)
        self.assertEqual(future["ledger_spend_cents"], 222)
        self.assertEqual(len(future["smoke_spend"]), 4)
        self.assertEqual(future["smoke_spend_cents"], 18)
        future_admission = self._admit(future)
        self.assertTrue(future_admission["admitted"])
        self.assertEqual(future_admission["snapshot"]["combined_exposure_cents"], 440)
        self.assertEqual(future_admission["snapshot"]["remaining_cents"], 11_560)

    def test_present_valid_artifact_is_validated_before_the_expiry_registry(self):
        # A readable artifact always wins: the registry must not substitute its
        # recorded 6c for the artifact's own recorded spend.
        run_id = "41213566873"
        # The repaired #997 binding requires the proof's own workflow_run_id and
        # workflow_run_attempt to match the API run entry, so this synthetic proof
        # is bound to the registered run id and attempt 1.
        fake = FakeGH(
            {"smoke": [page([self._run_entry(run_id, HEAD_SHA)])], "trial": [page([])]},
            {run_id: [artifact("ber-live-smoke-proof")]},
            {(run_id, "ber-live-smoke-proof"): (
                "smoke-proof.json",
                smoke_proof(workflow_run_id=run_id, workflow_run_attempt="1"),
            )},
        )
        records = collect_smoke_proof_spends(
            gh=fake, repository="o/r", work_dir=self.tmp,
        )
        self.assertEqual(smoke_spend_total(records), 150)
        self.assertNotEqual(smoke_spend_total(records), 6)

    def test_expired_listing_marker_is_treated_as_absent_for_the_registry(self):
        # GitHub can list the proof artifact with expired=true before it is
        # physically removed. That record is not a present/downloadable proof, so
        # treating it as absent lets the exact-match expiry registry book the
        # committed spend during the retention/cleanup window instead of failing
        # the download path.
        runs, _absent_artifacts, no_payloads = self._expired_history_parts()
        expired_artifacts = {
            "41213566873": [expired_artifact("ber-live-smoke-proof")],
            "41179846875": [expired_artifact("ber-live-smoke-proof")],
        }
        fake = FakeGH(
            {"smoke": [page(runs)], "trial": [page([])]},
            expired_artifacts, no_payloads,
        )
        expired_records = collect_smoke_proof_spends(
            gh=fake, repository="o/r", work_dir=self.tmp,
        )
        # An expired record is never requested: the registry path books directly.
        self.assertEqual(fake.download_requests, [])
        absent_records = self._smoke_records(*self._expired_history_parts())
        self.assertEqual(expired_records, absent_records)
        self.assertEqual(len(expired_records), 2)
        self.assertEqual(smoke_spend_total(expired_records), 12)

    def test_unregistered_expired_listing_stays_unknown_not_zero(self):
        # The expired record is treated as ABSENT, so the untouched rule applies:
        # an unregistered artifactless run stays UNKNOWN-not-zero and refuses.
        fake = FakeGH(
            {"smoke": [page([run(42, conclusion="failure")])], "trial": [page([])]},
            {"42": [expired_artifact("ber-live-smoke-proof")]}, {},
        )
        with self.assertRaises(ValueError) as caught:
            collect_smoke_proof_spends(gh=fake, repository="o/r", work_dir=self.tmp)
        self.assertIn("UNKNOWN", str(caught.exception))

    def test_mixed_expired_and_live_same_name_records_fail_closed_with_ids(self):
        # The available download is name-based and cannot be constrained to one
        # artifact id, so a run listing both an expired and a live same-name proof
        # has no single provable selection. Fail closed (never a name-only guess),
        # naming both records' distinct ids/URLs; the fake also refuses to download
        # an expired record, so any wrong selection would fail loudly.
        expired = expired_artifact("ber-live-smoke-proof")
        live = artifact("ber-live-smoke-proof")
        self.assertNotEqual(expired["id"], live["id"])
        self.assertNotEqual(
            expired["archive_download_url"], live["archive_download_url"],
        )
        fake = FakeGH(
            {"smoke": [page([run(42)])], "trial": [page([])]},
            {"42": [expired, live]},
            {("42", "ber-live-smoke-proof"): ("smoke-proof.json", smoke_proof())},
        )
        with self.assertRaises(ValueError) as caught:
            collect_smoke_proof_spends(gh=fake, repository="o/r", work_dir=self.tmp)
        message = str(caught.exception)
        self.assertIn("ambiguous", message)
        self.assertIn("name-only", message)
        self.assertIn(str(expired["id"]), message)
        self.assertIn(str(live["id"]), message)
        self.assertEqual(fake.download_requests, [])

    def test_live_single_artifact_selection_is_the_unique_record_id(self):
        # A single same-name record is unambiguous for the name-based download;
        # assert the downloaded record is that exact artifact id (not a guess).
        live = artifact("ber-live-smoke-proof")
        fake = FakeGH(
            {"smoke": [page([run(42)])], "trial": [page([])]},
            {"42": [live]},
            {("42", "ber-live-smoke-proof"): ("smoke-proof.json", smoke_proof())},
        )
        records = collect_smoke_proof_spends(
            gh=fake, repository="o/r", work_dir=self.tmp,
        )
        self.assertEqual(smoke_spend_total(records), 150)
        self.assertEqual(len(fake.download_requests), 1)
        self.assertEqual(fake.download_requests[0][2], live["id"])

    def test_non_boolean_expired_flag_fails_closed(self):
        # A truthy string is a malformed listing, not an expiry signal: the strict
        # boolean check refuses instead of treating it as live or expired.
        record = artifact("ber-live-smoke-proof")
        record["expired"] = "true"
        fake = FakeGH(
            {"smoke": [page([run(42)])], "trial": [page([])]},
            {"42": [record]}, {},
        )
        with self.assertRaises(ValueError) as caught:
            collect_smoke_proof_spends(gh=fake, repository="o/r", work_dir=self.tmp)
        self.assertIn("non-boolean expired", str(caught.exception))

    def test_under_reported_artifact_total_count_fails_closed(self):
        # A non-empty page that declares total_count=0 is lossy: the listing must
        # reconcile against its declared total before any expiry logic is applied.
        run_entry = self._run_entry(
            "41213566873", LEGACY_PROOF_HEADS["41213566873"],
        )
        fake = _UnderReportedArtifactListingGH(
            [run_entry],
            {"41213566873": [artifact("ber-live-smoke-proof")]},
        )
        with self.assertRaises(ValueError) as caught:
            collect_smoke_proof_spends(gh=fake, repository="o/r", work_dir=self.tmp)
        self.assertIn("artifact listing is incomplete", str(caught.exception))

    def test_head_sha_regex_is_anchored_to_exactly_40_lower_hex(self):
        # The full head must be exactly 40 lowercase hex characters; a prefixed,
        # suffixed, uppercase or overlong value never matches the registry path.
        for bad_head in (
            "a" * 40 + "x",
            "a" * 40 + " ",
            "A" * 40,
            "a" * 41,
        ):
            entry = self._run_entry(
                "41213566873", LEGACY_PROOF_HEADS["41213566873"],
            )
            entry["head_sha"] = bad_head
            fake = FakeGH(
                {"smoke": [page([entry])], "trial": [page([])]},
                {"41213566873": []}, {},
            )
            with self.subTest(head=bad_head):
                with self.assertRaises(ValueError) as caught:
                    collect_smoke_proof_spends(
                        gh=fake, repository="o/r", work_dir=self.tmp,
                    )
                self.assertIn("malformed provenance", str(caught.exception))

    # -- negative matrix -------------------------------------------------

    def test_unregistered_artifactless_run_stays_unknown_not_zero(self):
        # No wildcard/catch-all and no substring/superstring matching: only the
        # two exact committed run ids are eligible.
        for run_id in (42, "4121356687", 412135668730, 141213566873):
            fake = FakeGH(
                {"smoke": [page([run(run_id, conclusion="failure")])], "trial": [page([])]},
                {str(run_id): []}, {},
            )
            with self.subTest(run_id=run_id):
                with self.assertRaises(ValueError) as caught:
                    collect_smoke_proof_spends(
                        gh=fake, repository="o/r", work_dir=self.tmp,
                    )
                self.assertIn("UNKNOWN", str(caught.exception))
        # A non-proof artifact does not count as the proof artifact either.
        fake = FakeGH(
            {"smoke": [page([run(42, conclusion="failure")])], "trial": [page([])]},
            {"42": [artifact("ber-shared-allowance-state")]}, {},
        )
        with self.assertRaises(ValueError) as caught:
            collect_smoke_proof_spends(gh=fake, repository="o/r", work_dir=self.tmp)
        self.assertIn("UNKNOWN", str(caught.exception))

    def test_registered_expired_run_metadata_mismatch_refuses(self):
        for run_id, registered in SMOKE_RUNS_WITH_EXPIRED_PROOF.items():
            cases = [
                (
                    self._run_entry(run_id, registered["head_sha"], conclusion="failure"),
                    "recorded conclusion",
                ),
                (
                    self._run_entry(run_id, "a" * 40),
                    "recorded head",
                ),
                (
                    self._run_entry(run_id, registered["head_sha"], attempt=2),
                    "recorded attempt",
                ),
                (
                    {
                        key: value for key, value in
                        self._run_entry(run_id, registered["head_sha"]).items()
                        if key != "head_sha"
                    },
                    "run entry",
                ),
            ]
            for entry, expected in cases:
                fake = FakeGH(
                    {"smoke": [page([entry])], "trial": [page([])]},
                    {str(entry["id"]): []}, {},
                )
                with self.subTest(run_id=run_id, expected=expected):
                    with self.assertRaises(ValueError) as caught:
                        collect_smoke_proof_spends(
                            gh=fake, repository="o/r", work_dir=self.tmp,
                        )
                    self.assertIn(expected, str(caught.exception))

    def test_expired_registry_attempt_evidence_missing_fails_closed(self):
        # Repaired #997 convention: run_attempt is part of the paid-attempt
        # identity and is never guessed or defaulted. A missing API attempt, a
        # registry record without a recorded attempt, and an invalid recorded
        # attempt all refuse instead of booking the historical 6c.
        registered = SMOKE_RUNS_WITH_EXPIRED_PROOF["41213566873"]
        entry = self._run_entry("41213566873", registered["head_sha"])
        del entry["run_attempt"]
        with self.assertRaises(ValueError) as caught:
            collect_smoke_proof_spends(
                gh=FakeGH(
                    {"smoke": [page([entry])], "trial": [page([])]},
                    {"41213566873": []}, {},
                ),
                repository="o/r", work_dir=self.tmp,
            )
        self.assertIn("readable attempt evidence", str(caught.exception))

        recorded_without_attempt = {
            "spent_cents": 6,
            "expected_conclusion": "success",
            "head_sha": registered["head_sha"],
            "proof_bytes": 2_253,
            "proof_sha256": registered["proof_sha256"],
            "basis": registered["basis"],
        }
        entry = self._run_entry("41213566873", registered["head_sha"])

        def _attempt_evidence_fake():
            return FakeGH(
                {"smoke": [page([entry])], "trial": [page([])]},
                {"41213566873": []}, {},
            )

        with mock.patch.dict(
            workflow_runtime.SMOKE_RUNS_WITH_EXPIRED_PROOF,
            {"41213566873": recorded_without_attempt},
            clear=False,
        ):
            with self.assertRaises(ValueError) as caught:
                collect_smoke_proof_spends(
                    gh=_attempt_evidence_fake(), repository="o/r", work_dir=self.tmp,
                )
            self.assertIn("no recorded attempt evidence", str(caught.exception))

        invalid_recorded = dict(recorded_without_attempt)
        invalid_recorded["expected_attempt"] = "1"
        with mock.patch.dict(
            workflow_runtime.SMOKE_RUNS_WITH_EXPIRED_PROOF,
            {"41213566873": invalid_recorded},
            clear=False,
        ):
            with self.assertRaises(ValueError) as caught:
                collect_smoke_proof_spends(
                    gh=_attempt_evidence_fake(), repository="o/r", work_dir=self.tmp,
                )
            self.assertIn("no recorded attempt evidence", str(caught.exception))

    def test_expired_id_present_artifact_attempt_mismatch_refuses_via_repaired_binding(self):
        # A present artifact on a registered expiry id is always validated by the
        # repaired #997 binding first: a re-run API entry (attempt 2) with the
        # retained attempt-1 proof refuses and never falls back to the recorded 6c.
        for run_id, registered in SMOKE_RUNS_WITH_EXPIRED_PROOF.items():
            entry = self._run_entry(run_id, registered["head_sha"], attempt=2)
            fake = FakeGH(
                {"smoke": [page([entry])], "trial": [page([])]},
                {run_id: [artifact("ber-live-smoke-proof")]},
                {(run_id, "ber-live-smoke-proof"): (
                    "smoke-proof.json", self._legacy_proof(run_id),
                )},
            )
            with self.subTest(run_id=run_id):
                with self.assertRaises(ValueError) as caught:
                    collect_smoke_proof_spends(
                        gh=fake, repository="o/r", work_dir=self.tmp,
                    )
                self.assertIn(
                    "workflow run attempt does not match", str(caught.exception),
                )

    def test_present_but_tampered_artifact_refuses_without_registry_fallback(self):
        for run_id, registered in SMOKE_RUNS_WITH_EXPIRED_PROOF.items():
            run_entry = self._run_entry(run_id, registered["head_sha"])
            corrupt = FakeGH(
                {"smoke": [page([run_entry])], "trial": [page([])]},
                {run_id: [artifact("ber-live-smoke-proof")]},
                {(run_id, "ber-live-smoke-proof"): (
                    "smoke-proof.json", {"not": "a smoke proof"},
                )},
            )
            with self.subTest(run_id=run_id, mode="corrupt"):
                with self.assertRaises(ValueError) as caught:
                    collect_smoke_proof_spends(
                        gh=corrupt, repository="o/r", work_dir=self.tmp,
                    )
                self.assertIn("unsupported smoke proof schema", str(caught.exception))

            tampered = self._legacy_proof(run_id)
            tampered["spent_cents"] = tampered["spent_cents"] + 1
            tampered_fake = FakeGH(
                {"smoke": [page([run_entry])], "trial": [page([])]},
                {run_id: [artifact("ber-live-smoke-proof")]},
                {(run_id, "ber-live-smoke-proof"): ("smoke-proof.json", tampered)},
            )
            with self.subTest(run_id=run_id, mode="tampered"):
                with self.assertRaises(ValueError) as caught:
                    collect_smoke_proof_spends(
                        gh=tampered_fake, repository="o/r", work_dir=self.tmp,
                    )
                self.assertIn("hash does not verify", str(caught.exception))

    def test_unreadable_or_incomplete_artifact_listing_refuses(self):
        # A GitHub read failure or a lossy listing must refuse; the registry can
        # never be used as a fallback for an unreadable artifact inventory.
        run_entry = self._run_entry("41213566873", LEGACY_PROOF_HEADS["41213566873"])
        with self.assertRaises(ValueError) as caught:
            collect_smoke_proof_spends(
                gh=_ArtifactListingFailureGH([run_entry]),
                repository="o/r", work_dir=self.tmp,
            )
        self.assertIn("artifact listing failed", str(caught.exception))
        with self.assertRaises(ValueError) as caught:
            collect_smoke_proof_spends(
                gh=_IncompleteArtifactListingGH([run_entry]),
                repository="o/r", work_dir=self.tmp,
            )
        self.assertIn("artifact listing is incomplete", str(caught.exception))

    def test_single_expired_proof_below_preserved_floor_fails_closed(self):
        # Only one of the two expired proofs is in history: the unchanged
        # preserved-floor invariant still refuses rather than booking a short
        # (or fabricated) history. Artifact-present behavior is identical.
        run_entry = self._run_entry("41213566873", LEGACY_PROOF_HEADS["41213566873"])
        expired_fake = FakeGH(
            {"smoke": [page([run_entry])], "trial": [page([])]},
            {"41213566873": []}, {},
        )
        with self.assertRaises(ValueError) as caught:
            collect_allowance_history(
                gh=expired_fake, repository="o/r", work_dir=self.tmp,
                current_run_id="9999999999",
            )
        self.assertIn("below the preserved historical floor", str(caught.exception))

        present_fake = FakeGH(
            {"smoke": [page([run_entry])], "trial": [page([])]},
            {"41213566873": [artifact("ber-live-smoke-proof")]},
            {("41213566873", "ber-live-smoke-proof"): (
                "smoke-proof.json", self._legacy_proof("41213566873"),
            )},
        )
        with self.assertRaises(ValueError) as caught:
            collect_allowance_history(
                gh=present_fake, repository="o/r", work_dir=self.tmp,
                current_run_id="9999999999",
            )
        self.assertIn("below the preserved historical floor", str(caught.exception))

    def test_current_run_exclusion_precedes_the_expiry_registry(self):
        # The in-flight run is skipped before any artifact/bookkeeping logic, so a
        # current-run id never books its committed historical spend.
        run_entry = self._run_entry("41179846875", LEGACY_PROOF_HEADS["41179846875"])
        fake = FakeGH(
            {"smoke": [page([run_entry])], "trial": [page([])]},
            {"41179846875": []}, {},
        )
        records = collect_smoke_proof_spends(
            gh=fake, repository="o/r", work_dir=self.tmp,
            current_run_id="41179846875",
        )
        self.assertEqual(records, {})

    # -- recorded identities / registry invariants -----------------------

    def test_expired_registry_is_exact_match_committed_constant(self):
        self.assertEqual(
            set(SMOKE_RUNS_WITH_EXPIRED_PROOF),
            {"41213566873", "41179846875"},
        )
        self.assertTrue(
            set(SMOKE_RUNS_WITH_EXPIRED_PROOF).isdisjoint(SMOKE_RUNS_WITHOUT_PROOF)
        )
        expected_keys = {
            "spent_cents", "expected_conclusion", "head_sha", "expected_attempt",
            "proof_bytes", "proof_sha256", "basis",
        }
        for run_id, registered in SMOKE_RUNS_WITH_EXPIRED_PROOF.items():
            with self.subTest(run_id=run_id):
                self.assertEqual(set(registered), expected_keys)
                self.assertEqual(registered["spent_cents"], 6)
                self.assertEqual(registered["expected_conclusion"], "success")
                self.assertEqual(registered["expected_attempt"], 1)
                self.assertEqual(registered["proof_bytes"], 2_253)
                self.assertEqual(
                    registered["head_sha"], LEGACY_PROOF_HEADS[str(run_id)],
                )
                self.assertRegex(registered["head_sha"], "[0-9a-f]{40}")
                self.assertRegex(registered["proof_sha256"], "[0-9a-f]{64}")
                self.assertTrue(str(registered["basis"]).strip())
                self.assertIn("expires 2026-11-14", str(registered["basis"]))
                self.assertEqual(PRESERVED_HISTORICAL_SMOKE_CENTS, 18)
                self.assertEqual(PRESERVED_HISTORICAL_LEDGER_CENTS, 222)

    def test_recorded_proof_identities_match_captured_verbatim_fixtures(self):
        # The recorded proof identity is the whole-file SHA-256 of the verbatim
        # captured artifact member, committed byte-identically as the fixture; a
        # wrong recorded hash (or a changed fixture) fails here. The proof's own
        # recorded run/head/attempt/spend are the same identities the registry
        # binds at runtime, and its self-hash still verifies.
        for run_id, registered in SMOKE_RUNS_WITH_EXPIRED_PROOF.items():
            with self.subTest(run_id=run_id):
                raw = (
                    SMOKE_PROOF_FIXTURE_DIR / ("smoke-proof-run-" + run_id + ".json")
                ).read_bytes()
                self.assertEqual(len(raw), registered["proof_bytes"])
                self.assertEqual(
                    hashlib.sha256(raw).hexdigest(), registered["proof_sha256"],
                )
                proof = json.loads(raw)
                self.assertEqual(proof["workflow_run_id"], run_id)
                self.assertEqual(
                    proof["workflow_run_attempt"], str(registered["expected_attempt"]),
                )
                self.assertEqual(proof["head_sha"], registered["head_sha"])
                self.assertEqual(proof["spent_cents"], registered["spent_cents"])
                self.assertEqual(proof["status"], "PASS")
                self.assertEqual(proof["workflow"], "eval-smoke")
                recomputed = hashlib.sha256(json.dumps(
                    {k: v for k, v in proof.items() if k != "proof_sha256"},
                    sort_keys=True, separators=(",", ":"),
                ).encode("utf-8")).hexdigest()
                self.assertEqual(recomputed, proof["proof_sha256"])

    def test_recorded_proof_hash_is_bound_to_its_own_run_only(self):
        # Cross-binding or mutation must not match: each recorded hash equals its
        # own captured bytes, differs from the other run's bytes, and differs from
        # a tampered body (spent_cents 6 -> 7) of its own bytes.
        hashes = {}
        for run_id, registered in SMOKE_RUNS_WITH_EXPIRED_PROOF.items():
            raw = (
                SMOKE_PROOF_FIXTURE_DIR / ("smoke-proof-run-" + run_id + ".json")
            ).read_bytes()
            hashes[run_id] = hashlib.sha256(raw).hexdigest()
            self.assertEqual(hashes[run_id], registered["proof_sha256"])
            tampered = raw.replace(b'"spent_cents": 6', b'"spent_cents": 7')
            self.assertNotEqual(tampered, raw)
            self.assertNotEqual(
                hashlib.sha256(tampered).hexdigest(), registered["proof_sha256"],
            )
        for run_id, registered in SMOKE_RUNS_WITH_EXPIRED_PROOF.items():
            for other_id, other_hash in hashes.items():
                if other_id == run_id:
                    continue
                self.assertNotEqual(registered["proof_sha256"], other_hash)

    def test_repeated_expiry_collection_does_not_mutate_registry(self):
        # The name states the actual assertion: repeated collection is
        # deterministic and leaves the module mapping unchanged. True registry
        # immutability is P3-2, deferred as non-blocking (tests still patch the
        # mapping under mock.patch).
        before = {
            run_id: dict(registered)
            for run_id, registered in SMOKE_RUNS_WITH_EXPIRED_PROOF.items()
        }
        runs, artifacts, payloads = self._expired_history_parts()
        first = self._smoke_records(runs, artifacts, payloads)
        second = self._smoke_records(runs, artifacts, payloads)
        self.assertEqual(first, second)
        self.assertEqual(smoke_spend_total(first), 12)
        after = {
            run_id: dict(registered)
            for run_id, registered in SMOKE_RUNS_WITH_EXPIRED_PROOF.items()
        }
        self.assertEqual(before, after)


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


class TwoJobLayoutTests(unittest.TestCase):
    """S4 acceptance tests for the two sequential ten-case jobs (static).

    These tests are the offline, no-network proof that the reviewed workflow
    defines the accepted layout: one G3 dispatch, two sequential jobs, fixed
    first-ten/remaining-ten partitions represented separately from the full
    twenty-case count, durable state passed from job 1 to job 2, job 2 requiring
    job 1 success and mapping keys only in its gated run step, exactly 80
    planned calls at 300s per call, and unchanged timeouts/retry/dispatch shape.
    They do not run the workflow or a fake clock; S4 readiness still needs the
    workflow-wrapper and BER rehearsals.
    """

    @staticmethod
    def _workflow():
        path = REPO_ROOT / ".github/workflows/eval-run.yml"
        return path, yaml.safe_load(path.read_text(encoding="utf-8"))

    @staticmethod
    def _steps(job):
        return job.get("steps") or []

    def test_two_sequential_ten_case_jobs_and_shared_lock(self):
        path, workflow = self._workflow()
        self.assertEqual(
            list(workflow["jobs"]), ["eval-run-job-1", "eval-run-job-2"]
        )
        job1 = workflow["jobs"]["eval-run-job-1"]
        job2 = workflow["jobs"]["eval-run-job-2"]
        self.assertEqual(job2["needs"], ["eval-run-job-1"])
        self.assertNotIn("needs", job1)
        self.assertEqual(workflow["concurrency"]["group"], "pilot-a-shared-allowance")
        self.assertNotIn("concurrency", job1)
        self.assertNotIn("concurrency", job2)
        self.assertEqual(job1["timeout-minutes"], 360)
        self.assertEqual(job2["timeout-minutes"], 360)

    def test_job2_gates_on_job1_and_maps_keys_only_in_its_run_step(self):
        _path, workflow = self._workflow()
        job1 = workflow["jobs"]["eval-run-job-1"]
        job2 = workflow["jobs"]["eval-run-job-2"]
        self.assertIn("eval-run-job-1", str(job2.get("if")))
        self.assertIn("preflight_only", str(job2.get("if")))
        names = [step.get("name") for step in self._steps(job2)]
        verify_index = names.index(
            "Verify job 1, merge its durable state, and select the remaining cases"
        )
        run_index = names.index("Run the remaining cases as resumable per-case chunks")
        self.assertLess(verify_index, run_index)
        for step in self._steps(job2)[:run_index]:
            env = step.get("env") or {}
            self.assertNotIn("ANTHROPIC_API_KEY", env)
            self.assertNotIn("OPENAI_API_KEY", env)
        run_step = self._steps(job2)[run_index]
        self.assertIn("ANTHROPIC_API_KEY", run_step["env"])
        self.assertIn("OPENAI_API_KEY", run_step["env"])
        self.assertEqual(
            run_step["if"],
            "${{ steps.verify-job-1.outcome == 'success' }}",
        )

    def test_selected_sets_are_recorded_separately_from_the_full_count(self):
        text = self._workflow()[0].read_text(encoding="utf-8")
        for needle in (
            "ber-two-job-layout/1.0.0",
            "ber-job-case-selection/1.0.0",
            "fixed_selected_case_ids",
            "unexecuted_case_ids",
            "full_case_count",
            "full_planned_calls",
            "job_planned_calls_capacity",
            "per_call_timeout_seconds",
            "the trial must keep exactly 20 frozen cases",
            "the trial must be exactly 80 planned calls",
            "the trial must stay one subject vendor",
            "the per-call request timeout must stay 300s",
            "the two job selections are not a disjoint partition of the plan",
        ):
            self.assertIn(needle, text, needle)

    def test_durable_state_artifacts_and_job1_selection(self):
        text = self._workflow()[0].read_text(encoding="utf-8")
        for needle in (
            "ber-dispatch-context-job-1",
            "ber-resume-manifest-job-1",
            "ber-shared-allowance-state-job-1",
            "Select the ten cases for job 1",
            "Publish the dispatch context for the second job (no secrets)",
            "Upload resume manifest (always; completed cases survive a timeout)",
            "Upload reservation/true-up state (always)",
            "ber-resume-manifest",
            "ber-shared-allowance-state",
            "Build structured summary and publish directory",
        ):
            self.assertIn(needle, text, needle)
        self.assertGreaterEqual(text.count("ber-resume-manifest-job-1"), 2)
        self.assertGreaterEqual(text.count("ber-shared-allowance-state-job-1"), 2)

    def test_unchanged_timeouts_retry_and_dispatch_shape(self):
        text = self._workflow()[0].read_text(encoding="utf-8")
        for needle in (
            "timeout-minutes: 360",
            "timeout-minutes: 330",
            "PER_CASE_TIMEOUT_SECONDS = 1500",
            "timeout=120,",
            "re-runs are not resumed because the resume artifact is run-scoped",
            "no retry, no second",
        ):
            self.assertIn(needle, text, needle)

    def test_run_step_records_selection_skips_in_the_job_layout(self):
        # S4D2 execution proof found: when a resumed job has no case left to run
        # (or skips some of its fixed ten), the run step must record the
        # selection's already-completed ids in skipped_case_ids so the job
        # layout partitions its fixed ten ids and job 2's verification does not
        # refuse the resumed state.
        _path, workflow = self._workflow()
        job1 = workflow["jobs"]["eval-run-job-1"]
        run_step = next(
            step
            for step in self._steps(job1)
            if step.get("name") == "Run the remaining cases as resumable per-case chunks"
        )
        source = run_step["run"]
        self.assertIn(
            'skipped_cases = list(selection.get("already_completed_case_ids") or [])',
            source,
        )
        self.assertIn("if case_id not in skipped_cases:", source)

    def test_both_job_run_steps_are_byte_identical(self):
        # The run step is duplicated for the two jobs; keep the copies in sync
        # except for their gating condition, so a fix cannot land in one job
        # only. Both copies must contain the same case-selection contract.
        _path, workflow = self._workflow()
        job1 = workflow["jobs"]["eval-run-job-1"]
        job2 = workflow["jobs"]["eval-run-job-2"]
        def run_steps(job):
            return {
                step.get("name"): step
                for step in self._steps(job)
                if step.get("name") == "Run the remaining cases as resumable per-case chunks"
            }
        first = run_steps(job1)
        second = run_steps(job2)
        self.assertEqual(len(first), 1)
        self.assertEqual(len(second), 1)
        name = "Run the remaining cases as resumable per-case chunks"
        self.assertEqual(first[name]["timeout-minutes"], second[name]["timeout-minutes"])
        self.assertEqual(
            first[name]["env"], second[name]["env"],
        )
        self.assertEqual(
            first[name]["run"], second[name]["run"],
        )

    def test_embedded_python_compiles(self):
        _path, workflow = self._workflow()
        failures = []
        for job_name, job in workflow["jobs"].items():
            for step in self._steps(job):
                run = step.get("run")
                if not isinstance(run, str):
                    continue
                lines = run.split("\n")
                index = 0
                while index < len(lines):
                    if lines[index].strip() == "python -P - <<'PY'":
                        code = []
                        index += 1
                        while index < len(lines) and lines[index].strip() != "PY":
                            code.append(lines[index])
                            index += 1
                        try:
                            ast.parse("\n".join(code))
                        except SyntaxError as exc:
                            failures.append(f"{job_name}/{step.get('name')}: {exc}")
                    index += 1
        self.assertEqual(failures, [])


# ---- formerly test_live_reservations.py ----
"""Atomic reservation persistence and denied-path transport-spy tests (offline)."""


import json
import tempfile
import unittest
from pathlib import Path

from tools.behavioral_eval_runner.live.cumulative import admit_paid_call
from tools.behavioral_eval_runner.live.workflow_runtime import (
    dispatch_if_admitted,
    RESERVATION_STATE_SCHEMA,
    STATUS_CANCELLED,
    STATUS_TRUE_UP,
    cancel,
    load_state,
    reserve,
    true_up,
)
from tools.behavioral_eval_runner.live.transport import SubjectTransport
from tools.behavioral_eval_runner.live.subject import SubjectAdapter
from tools.behavioral_eval_runner.live.providers import SUBJECT_PINS
from tools.behavioral_eval_runner.live.config import OwnerAllowlist
from tools.behavioral_eval_runner.live.judge_adapter import JudgeAdapter


class SpyTransport(SubjectTransport):
    name = "spy"

    def __init__(self):
        self.calls = 0

    def complete(self, request):
        self.calls += 1
        raise AssertionError("transport must not be called when admission is denied")


class ReservationPersistenceTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.path = Path(self._tmp.name) / "allowance-state.json"

    def tearDown(self):
        self._tmp.cleanup()

    def test_reservation_survives_interruption_and_blocks_next_admission(self):
        reserve(
            self.path, allowance_id="pilot-a", workflow_run_id=123, identity="smoke",
            amount_cents=200, ledger_spend_cents=11_900, smoke_spend_cents=0,
            ceiling_cents=12_000,
        )
        restored = load_state(self.path)
        self.assertEqual(restored["schema"], RESERVATION_STATE_SCHEMA)
        self.assertEqual(restored["outstanding_reservations_cents"], 200)
        admission = admit_paid_call(
            ceiling_cents=12_000, prior_ledger_spend_cents=11_900,
            prior_smoke_spend_records={}, reservation_cents=0,
            outstanding_reservations_cents=restored["outstanding_reservations_cents"],
        )
        self.assertFalse(admission["admitted"])

    def test_true_up_clears_outstanding_atomically(self):
        reserve(self.path, allowance_id="pilot-a", workflow_run_id=123, identity="trial",
                amount_cents=7_880, ledger_spend_cents=222, smoke_spend_cents=18,
                ceiling_cents=12_000)
        state = true_up(self.path, spent_cents=500)
        self.assertEqual(state["status"], STATUS_TRUE_UP)
        self.assertEqual(state["outstanding_reservations_cents"], 0)
        self.assertEqual(state["ledger_spend_cents"], 722)
        json.loads(self.path.read_text(encoding="utf-8"))

    def test_cancellation_keeps_known_exposure(self):
        reserve(self.path, allowance_id="pilot-a", workflow_run_id=123, identity="trial",
                amount_cents=7_880, ledger_spend_cents=222, smoke_spend_cents=18,
                ceiling_cents=12_000)
        state = cancel(self.path)
        self.assertEqual(state["status"], STATUS_CANCELLED)
        self.assertEqual(state["outstanding_reservations_cents"], 7_880)

    def test_denied_admission_makes_zero_production_transport_calls(self):
        spy = SpyTransport()
        admission = admit_paid_call(
            ceiling_cents=12_000, prior_ledger_spend_cents=11_900,
            prior_smoke_spend_records={}, reservation_cents=200,
        )
        self.assertFalse(admission["admitted"])
        if admission["admitted"]:
            spy.complete(None)
        self.assertEqual(spy.calls, 0)

    def test_denied_admission_never_enters_production_dispatch(self):
        adapter = SubjectAdapter(SUBJECT_PINS["anthropic"], SpyTransport(), max_output_tokens=16_384, timeout_seconds=300)
        request = adapter.build_request(request_id="r", prompt="p", arm="BASELINE")
        admission = admit_paid_call(
            ceiling_cents=12_000, prior_ledger_spend_cents=11_900,
            prior_smoke_spend_records={}, reservation_cents=200,
        )
        self.assertFalse(admission["admitted"])
        result = dispatch_if_admitted(admission, adapter.dispatch, request)
        self.assertIsNone(result)
        self.assertEqual(adapter.transport.calls, 0)




# ---- formerly test_live_s3_budget_proof.py ----
"""S3 serialized provider request/token-budget proof tests (offline).

Uses the real SubjectAdapter/JudgeAdapter request builders and the shared
runtime reservation/admission functions. No provider call, network, credential,
tokenizer dependency or paid action occurs. Actual wire framing and actual
tokenizer counts remain UNKNOWN; the documented safe upper bound is used.
"""


import importlib.util
import json
import unittest
from pathlib import Path

from tools.behavioral_eval_runner.canonical import sha256_hex_text
from tools.behavioral_eval_runner.live.config import (
    MAX_JUDGE_REQUEST_BYTES,
    OWNER_PROVIDER_CAP_CENTS,
    SMOKE_CEILING_CENTS,
    OwnerAllowlist,
)
from tools.behavioral_eval_runner.live.cumulative import (
    actual_byte_reservation_cents,
    actual_byte_smoke_bounds,
    admit_paid_call,
)
from tools.behavioral_eval_runner.live.dataset import load_cases
from tools.behavioral_eval_runner.live.judge_adapter import JudgeAdapter
from tools.behavioral_eval_runner.live.providers import JUDGE_PINS, SUBJECT_PINS
from tools.behavioral_eval_runner.live.subject import SubjectAdapter, SubjectResult
from tools.behavioral_eval_runner.live.transport import ProviderUsage

OUTPUT_TOKENS = 16_384
FRAMING_OVERHEAD_BYTES = 1_024
SUBJECT_PIN = SUBJECT_PINS["anthropic"]
JUDGE_PIN = JUDGE_PINS[("anthropic", "claude-sonnet-5-5")]
ALLOWLIST = OwnerAllowlist((("openai", "gpt-6-astra"),))
HISTORICAL_LEDGER_CENTS = 222
HISTORICAL_SMOKE_CENTS = 18
HISTORICAL_TOTAL_CENTS = 240


def _subject_body_bytes(request) -> int:
    body = {
        "model": request.model,
        "max_tokens": request.max_output_tokens,
        "system": request.system,
        "messages": [{"role": "user", "content": request.user_content}],
    }
    return len(json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


def _judge_body_bytes(request) -> int:
    body = {
        "model": request.model,
        "max_output_tokens": request.max_output_tokens,
        "messages": [
            {"role": "system", "content": request.system},
            {"role": "user", "content": request.user_content},
        ],
    }
    return len(json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


def _cents(input_bytes: int, pin) -> int:
    return actual_byte_reservation_cents(
        input_bytes=input_bytes,
        input_cents_per_mtok=pin.input_cents_per_mtok,
        output_tokens=OUTPUT_TOKENS,
        output_cents_per_mtok=pin.output_cents_per_mtok,
    )


class S3SerializedBudgetProofTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        root = Path(__file__).resolve().parents[3]
        cls.cases = load_cases(str(root / "tools/behavioral_eval_runner/live/pilot-a/cases"))
        cls.result = SubjectResult(
            "r", "rid", "anthropic", SUBJECT_PIN.model, SUBJECT_PIN.model,
            sha256_hex_text("x"), 1, ProviderUsage(1, 1), "end_turn",
        )
        rows = []
        for case in cls.cases:
            for arm in ("WITH_SKILL", "BASELINE"):
                subject = SubjectAdapter(
                    SUBJECT_PIN, None,
                    max_output_tokens=OUTPUT_TOKENS, timeout_seconds=300,
                ).build_request(
                    request_id="s", prompt=case.prompt, arm=arm,
                    skill_instructions=case.skill_instructions if arm == "WITH_SKILL" else None,
                )
                judge = JudgeAdapter(
                    JUDGE_PIN, ALLOWLIST, None,
                    max_output_tokens=OUTPUT_TOKENS, timeout_seconds=300,
                ).build_request(
                    request_id="j", case=case, arm=arm, subject_vendor="anthropic",
                    subject_result=cls.result, subject_text="",
                )
                rows.append((_subject_body_bytes(subject), _judge_body_bytes(judge)))
        cls.rows = rows
        cls.subject_max = max(row[0] for row in rows)
        cls.judge_scaffold_max = max(row[1] for row in rows)
        cls.smoke_subject = _cents(rows[0][0] + FRAMING_OVERHEAD_BYTES, SUBJECT_PIN)
        cls.smoke_judge = _cents(MAX_JUDGE_REQUEST_BYTES + FRAMING_OVERHEAD_BYTES, JUDGE_PIN)
        cls.trial_subject = _cents(cls.subject_max + FRAMING_OVERHEAD_BYTES, SUBJECT_PIN)
        cls.trial_judge = cls.smoke_judge
        cls.trial_call = cls.trial_subject + cls.trial_judge
        cls.trial_total = 40 * cls.trial_call
        cls.full_total = 120 * cls.trial_call

    def test_standard_rates_and_caps_are_unchanged(self) -> None:
        self.assertEqual(SUBJECT_PIN.vendor, "anthropic")
        self.assertEqual(SUBJECT_PIN.price(), (200, 1000))
        self.assertEqual(JUDGE_PIN.vendor, "openai")
        self.assertEqual(JUDGE_PIN.price(), (1000, 5000))
        self.assertEqual(OUTPUT_TOKENS, 16_384)
        self.assertEqual(SMOKE_CEILING_CENTS, 200)
        self.assertEqual(OWNER_PROVIDER_CAP_CENTS, 12_000)
        self.assertEqual(MAX_JUDGE_REQUEST_BYTES, 90_000)
        # Only input/output billable categories are modelled; explicit standard
        # list price, no batch/cache/priority discount is applied.
        self.assertEqual(set(SUBJECT_PIN.to_dict()), {
            "vendor", "model", "credential_env_var",
            "input_cents_per_mtok", "output_cents_per_mtok",
        })

    def test_serialized_maxima_and_runtime_bounds(self) -> None:
        self.assertEqual(len(self.rows), 40)
        self.assertEqual(self.subject_max, 35_337)
        self.assertEqual(self.judge_scaffold_max, 5_556)
        smoke = actual_byte_smoke_bounds(
            subject_request_bytes=self.rows[0][0] + FRAMING_OVERHEAD_BYTES,
            max_judge_request_bytes=MAX_JUDGE_REQUEST_BYTES + FRAMING_OVERHEAD_BYTES,
            max_output_tokens=OUTPUT_TOKENS,
            subject_input_cents_per_mtok=SUBJECT_PIN.input_cents_per_mtok,
            subject_output_cents_per_mtok=SUBJECT_PIN.output_cents_per_mtok,
            judge_input_cents_per_mtok=JUDGE_PIN.input_cents_per_mtok,
            judge_output_cents_per_mtok=JUDGE_PIN.output_cents_per_mtok,
        )
        self.assertEqual(smoke["subject_cents"], 22)
        self.assertEqual(smoke["judge_cents"], 173)
        self.assertEqual(smoke["smoke_cents"], 195)
        self.assertLessEqual(smoke["smoke_cents"], SMOKE_CEILING_CENTS)
        self.assertLessEqual(HISTORICAL_TOTAL_CENTS + self.trial_total, OWNER_PROVIDER_CAP_CENTS)
        self.assertGreater(HISTORICAL_TOTAL_CENTS + self.full_total, OWNER_PROVIDER_CAP_CENTS)

    def test_full_pilot_rejected_pre_dispatch(self) -> None:
        historical_smoke = {"historical": HISTORICAL_SMOKE_CENTS}
        trial = admit_paid_call(
            ceiling_cents=OWNER_PROVIDER_CAP_CENTS,
            prior_ledger_spend_cents=HISTORICAL_LEDGER_CENTS,
            prior_smoke_spend_records=historical_smoke,
            reservation_cents=self.trial_total,
        )
        full = admit_paid_call(
            ceiling_cents=OWNER_PROVIDER_CAP_CENTS,
            prior_ledger_spend_cents=HISTORICAL_LEDGER_CENTS,
            prior_smoke_spend_records=historical_smoke,
            reservation_cents=self.full_total,
        )
        self.assertTrue(trial["admitted"])
        self.assertFalse(full["admitted"])
        self.assertLess(full["snapshot"]["remaining_cents"], 0)

    def test_safe_input_upper_bound_and_tokenizer_unavailable(self) -> None:
        self.assertIsNone(importlib.util.find_spec("tiktoken"))
        self.assertIsNone(importlib.util.find_spec("tokenizers"))
        # Documented safe upper bound: one input token cannot encode fewer than
        # one byte; output is capped exactly by max_output_tokens. Actual token
        # counts are UNKNOWN without a supported tokenizer.
        self.assertEqual(OUTPUT_TOKENS, 16_384)

    def _unicode_samples(self):
        return {
            "ascii": "plain ASCII text",
            "quotes": 'He said "hello" and \\ path',
            "newline": "line1\nline2\r\nline3\t",
            "c0": "\x00\x01\x02\x1f",
            "cjk": "漢字" * 100,
            "astral": "\U0001f600 \U0001f680 \U0001f4a9" * 100,
            "mixed": "A\"\n\x00漢\U0001f600" * 100,
        }

    def test_unicode_corpus_through_subject_then_judge(self) -> None:
        subject_adapter = SubjectAdapter(
            SUBJECT_PIN, None,
            max_output_tokens=OUTPUT_TOKENS, timeout_seconds=300,
        )
        judge_adapter = JudgeAdapter(
            JUDGE_PIN, ALLOWLIST, None,
            max_output_tokens=OUTPUT_TOKENS, timeout_seconds=300,
        )
        for label, sample in self._unicode_samples().items():
            subject_req = subject_adapter.build_request(
                request_id="u-" + label, prompt=sample, arm="WITH_SKILL",
                skill_instructions=self.cases[0].skill_instructions,
            )
            judge_req = judge_adapter.build_request(
                request_id="j-" + label, case=self.cases[0], arm="WITH_SKILL",
                subject_vendor="anthropic", subject_result=self.result,
                subject_text=sample,
            )
            self.assertGreater(_subject_body_bytes(subject_req), 0)
            self.assertGreater(_judge_body_bytes(judge_req), 0)
            raw = len(sample.encode("utf-8"))
            encoded = len(judge_req.user_content.encode("utf-8"))
            self.assertGreaterEqual(encoded, raw, label)
        huge = judge_adapter.build_request(
            request_id="j-huge", case=self.cases[0], arm="WITH_SKILL",
            subject_vendor="anthropic", subject_result=self.result,
            subject_text="漢" * 16_384,
        )
        huge_bytes = len(huge.system.encode("utf-8")) + len(huge.user_content.encode("utf-8"))
        self.assertGreater(huge_bytes, MAX_JUDGE_REQUEST_BYTES)
        # The encoded guard refuses AFTER a paid subject call: a partial
        # outcome, never a completion proof.
        self.assertGreater(_judge_body_bytes(huge), MAX_JUDGE_REQUEST_BYTES)




if __name__ == "__main__":
    unittest.main()
