"""C3.1: event catalogue/duplicate/order and bounded settlement.

Covers AC-C3.1-1, AC-C3.1-2 and AC-C3.1-4's blocked/checker behaviour.
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

from tools.aegis_ops import events, schema, settlement

import _fixtures


class EventCatalogueTests(unittest.TestCase):
    def test_valid_catalogue(self) -> None:
        result = events.validate(_fixtures.load("event-catalogue-valid.json"))
        self.assertTrue(result["valid"])
        self.assertFalse(result["blocked"])
        self.assertEqual(result["catalogue_rows"], 6)
        self.assertEqual(result["applied_actions"], ["NO_STAGE_ACTION", "START_STAGE_B"])

    def test_duplicate_delivery_is_noop(self) -> None:
        result = events.validate(_fixtures.load("duplicate-event-noop.json"))
        self.assertTrue(result["valid"])
        self.assertFalse(result["blocked"])
        self.assertEqual(result["duplicate_noops"], ["d-2"])
        self.assertEqual(len(result["results"]), 2)
        self.assertEqual(result["results"][1]["decision"], "DUPLICATE_NOOP")

    def test_out_of_order_is_refused(self) -> None:
        result = events.validate(_fixtures.load("out-of-order-event.json"))
        self.assertFalse(result["valid"])
        self.assertTrue(result["blocked"])
        self.assertIn("EVENT_OUT_OF_ORDER", result["issues"][0]["code"])

    def test_unknown_event_is_refused(self) -> None:
        document = _fixtures.load("event-catalogue-valid.json")
        document["events"][0]["event_name"] = "deployment_status"
        result = events.validate(document)
        self.assertFalse(result["valid"])
        self.assertIn("EVENT_UNKNOWN", [issue["code"] for issue in result["issues"]])

    def test_restart_not_allowed_duplicate_is_refused(self) -> None:
        document = _fixtures.load("duplicate-event-noop.json")
        document["events"][1]["action"] = "synchronize"
        document["events"][0]["action"] = "synchronize"
        # The second delivery is the same (event, action, head) as the first.
        result = events.validate(document)
        self.assertFalse(result["valid"])
        self.assertIn("refused", result)
        self.assertEqual(result["refused"], ["d-2"])


class SettlementTests(unittest.TestCase):
    def test_valid_settlement_is_settled_and_unblocked(self) -> None:
        result = settlement.settle(_fixtures.load("settlement-valid.json"))
        self.assertTrue(result["valid"])
        self.assertFalse(result["blocked"])
        self.assertTrue(result["settled"])
        self.assertEqual(result["blockers"], [])

    def test_pending_review_is_blocked(self) -> None:
        result = settlement.settle(_fixtures.load("settlement-pending-review.json"))
        self.assertTrue(result["valid"])
        self.assertTrue(result["blocked"])
        self.assertFalse(result["settled"])
        self.assertIn("REVIEW_SOURCE_PENDING:stage-D", result["blockers"])

    def test_deadline_and_unrun_are_named_blockers(self) -> None:
        result = settlement.settle(_fixtures.load("settlement-deadline-blocked.json"))
        self.assertTrue(result["valid"])
        self.assertTrue(result["blocked"])
        self.assertTrue(result["settled"])
        self.assertIn("BOUNDED_WAIT_EXHAUSTED:3/3", result["blockers"])
        self.assertIn("PRE_AUDIT_CHECK_NOT_PASSING:dco:unrun", result["blockers"])

    def test_unavailable_without_t7_is_blocked(self) -> None:
        result = settlement.settle(
            _fixtures.load("settlement-unavailable-no-authority.json")
        )
        self.assertTrue(result["valid"])
        self.assertTrue(result["blocked"])
        self.assertIn(
            "UNAVAILABLE_REVIEW_DISPOSITION_T7_OPEN:stage-D", result["blockers"]
        )

    def test_declared_mismatch_is_refused(self) -> None:
        document = _fixtures.load("settlement-pending-review.json")
        document["settled"] = True
        result = settlement.settle(document)
        self.assertFalse(result["valid"])
        self.assertIn(
            "DECLARED_SETTLED_MISMATCH", [issue["code"] for issue in result["issues"]]
        )
        self.assertNotIn("envelope", result)

    def test_envelope_hash_recomputes(self) -> None:
        result = settlement.settle(_fixtures.load("settlement-valid.json"))
        envelope = result["envelope"]
        payload = envelope["payload"]
        provenance = envelope["provenance"]
        self.assertEqual(provenance["declared_payload_sha256"], schema.digest(payload))
        self.assertEqual(
            provenance["declared_payload_bytes"], len(schema.canonical_bytes(payload))
        )
        self.assertEqual(payload["settled"], True)
        self.assertIn("pre_audit_checks", payload)

    def test_settlement_envelope_round_trips_through_merged_checker(self) -> None:
        """AC-C3.1-2: the output is the merged checker's own settlement input.

        The merged checker fixture builder supplies a real verdict/freeze/
        head-history bundle in a throw-away repository.  Our envelope replaces
        its settlement input; the checker must parse it and still exit 1 on
        T6/T24, with AUDITABLE assurance - never readiness true.
        """

        root = _fixtures.ROOT
        scripts = str(root / "scripts")
        if scripts not in sys.path:
            sys.path.insert(0, scripts)
        from aegis_verdict_gate.tests import _fixtures as checker_fixtures  # noqa: WPS433

        bundle = checker_fixtures.load_bundle("valid-verdict")
        temporary = pathlib.Path(tempfile.mkdtemp(prefix="c3c4-round-trip-"))
        paths = checker_fixtures.build(bundle, temporary)
        try:
            verdict_payload = json.loads(
                paths["verdict"].read_text(encoding="utf-8")
            )["payload"]
            checker_settlement = json.loads(
                paths["settlement"].read_text(encoding="utf-8")
            )["payload"]
            record = {
                "schema_version": schema.SCHEMA_SETTLEMENT,
                "change_id": str(verdict_payload["change"]["id"]),
                "candidate_head": verdict_payload["head_sha"],
                "source_ref": "fixture:round-trip",
                "as_of": checker_settlement["as_of"],
                "settled": checker_settlement["settled"],
                "pre_audit_checks": [
                    dict(check, deadline="2026-11-11T01:00:00Z")
                    for check in checker_settlement["pre_audit_checks"]
                ],
                "review_sources": checker_settlement["review_sources"],
                "bounded_wait": {
                    "deadline": "2026-11-11T01:00:00Z",
                    "max_attempts": 3,
                    "observed_attempts": 1,
                },
                "blockers": [],
            }
            result = settlement.settle(record)
            self.assertTrue(result["valid"], result["issues"])
            paths["settlement"].write_text(
                json.dumps(result["envelope"], sort_keys=True, indent=2) + "\n",
                encoding="utf-8",
            )
            completed = subprocess.run(
                [
                    sys.executable,
                    "-P",
                    str(root / "scripts" / "aegis_verdict_gate" / "run.py"),
                    "check",
                    "--repo-root",
                    str(temporary),
                    "--verdict",
                    str(paths["verdict"]),
                    "--freeze",
                    str(paths["freeze"]),
                    "--settlement",
                    str(paths["settlement"]),
                    "--head-history",
                    str(paths["head_history"]),
                    "--stage-records-dir",
                    str(paths["stage_records_dir"]),
                    "--records-dir",
                    "docs/approvals/revision-state",
                    "--json",
                ],
                capture_output=True,
                text=True,
                timeout=120,
            )
            self.assertEqual(completed.returncode, 1, completed.stderr)
            report = json.loads(completed.stdout)
            self.assertEqual(report["assurance"]["claim"], "AUDITABLE")
            self.assertEqual(report["assurance"]["mounted_coverage"], "UNKNOWN")
            self.assertFalse(report["readiness"])
            self.assertIn(
                "VERDICT_STALE_OR_UNVERIFIED",
                [blocker["code"] for blocker in report["blockers"]],
            )
        finally:
            checker_fixtures.cleanup(temporary)


if __name__ == "__main__":
    unittest.main()
