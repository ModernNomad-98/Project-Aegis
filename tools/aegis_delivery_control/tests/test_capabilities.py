from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
import hashlib
import tempfile
import unittest
from pathlib import Path

from tools.aegis_delivery_control.capabilities import (
    Capability, CapabilityObservation, ContainmentProbe, Finding,
    FreshnessProof, SyntheticAccountingReceipt, SyntheticClaimSource,
    SyntheticLiabilityBook, require_real_dispatch, require_synthetic_dispatch,
    require_synthetic_validation, verify_containment,
    verify_freshness,
)
from tools.aegis_delivery_control.contracts import DispatchDenied
from tools.aegis_delivery_control.evidence import (
    canonical_bytes, verify_synthetic_evidence, write_new_evidence,
)


class CapabilityProofTests(unittest.TestCase):
    def test_manual_and_controller_race_one_source_token(self) -> None:
        source = SyntheticClaimSource("token-1", expires_at=100)
        with ThreadPoolExecutor(max_workers=2) as workers:
            results = list(workers.map(
                lambda consumer: source.claim("token-1", consumer, now=50),
                ("controller", "manual"),
            ))
        self.assertEqual(sum(results), 1)
        winner = ("controller", "manual")[results.index(True)]
        loser = "manual" if winner == "controller" else "controller"
        self.assertTrue(source.recover_acknowledgement("token-1", winner))
        self.assertTrue(source.authorize_contact("token-1", winner, now=51))
        self.assertFalse(source.recover_acknowledgement("token-1", loser))
        self.assertFalse(source.authorize_contact("token-1", loser, now=51))
        self.assertFalse(source.claim("token-1", winner, now=51))

    def test_source_revoke_expire_supersede_outage_and_distinct_copy(self) -> None:
        for change in ("revoke", "supersede"):
            with self.subTest(change=change):
                source = SyntheticClaimSource("token-1", expires_at=100)
                getattr(source, change)()
                self.assertFalse(source.claim("token-1", "controller", now=50))
        source = SyntheticClaimSource("token-1", expires_at=100)
        self.assertFalse(source.claim("token-1", "controller", now=100))
        source.available = False
        self.assertFalse(source.claim("token-1", "controller", now=50))
        for change in ("revoke", "supersede"):
            with self.subTest(contact_change=change):
                source = SyntheticClaimSource("token-1", expires_at=100)
                self.assertTrue(source.claim("token-1", "controller", now=50))
                getattr(source, change)()
                self.assertFalse(source.authorize_contact("token-1", "controller", now=51))
        source = SyntheticClaimSource("token-1", expires_at=100)
        self.assertTrue(source.claim("token-1", "controller", now=50))
        self.assertFalse(source.authorize_contact("token-1", "controller", now=100))
        # A local copied claim can succeed while the distinct source denies.
        source = SyntheticClaimSource("token-1", expires_at=100)
        source.available = False
        copy = SyntheticClaimSource("token-1", expires_at=100)
        self.assertTrue(copy.claim("token-1", "controller", now=50))
        self.assertFalse(source.recover_acknowledgement("token-1", "controller"))

    def test_rollback_after_later_effect_or_charge_is_denied(self) -> None:
        old = FreshnessProof(7, "head-before-effect")
        later = FreshnessProof(8, "head-after-charge")
        for keyword in ("independent_anchor", "current_source"):
            with self.subTest(keyword=keyword):
                with self.assertRaisesRegex(DispatchDenied, "stale"):
                    verify_freshness(old, **{keyword: later})
        with self.assertRaisesRegex(DispatchDenied, "unavailable"):
            verify_freshness(old)
        with self.assertRaisesRegex(DispatchDenied, "contradictory"):
            verify_freshness(later, independent_anchor=later, current_source=old)
        verify_freshness(later, independent_anchor=later, current_source=later)

    def test_containment_negative_matrix(self) -> None:
        good = ContainmentProbe(True, True, True, False, True, True, True)
        verify_containment(good)
        failures = {
            "host_supported": False,  # unsupported host
            "descendants_ceased": False,  # descendant escaped or child alive
            "leader_ceased": False,
            "timed_out": True,
            "fence_held": False,
            "path_identity_stable": False,  # swap/reparse/hardlink
            "owner_verified": False,  # ACL/ownership failure
        }
        for name, value in failures.items():
            with self.subTest(name=name), self.assertRaises(DispatchDenied):
                verify_containment(replace(good, **{name: value}))

    def test_evidence_original_bytes_binding_writer_stage_and_sensitive(self) -> None:
        record = {"version": 1, "binding": "run-1", "writer": "fixture-writer",
                  "stage": "observed", "payload": {"receipt": "synthetic"}}
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "proof.json"
            digest = write_new_evidence(path, record)
            original = path.read_bytes()
            self.assertEqual(digest, hashlib.sha256(original).hexdigest())
            arguments = dict(expected_hash=digest, expected_binding="run-1",
                             expected_writer="fixture-writer", expected_stage="observed")
            self.assertEqual(verify_synthetic_evidence(original, **arguments), record)
            cases = [
                (original + b" ", arguments),
                (original, {**arguments, "expected_hash": "0" * 64}),
                (original, {**arguments, "expected_binding": "run-2"}),
                (original, {**arguments, "expected_writer": "other"}),
                (original, {**arguments, "expected_stage": "applied"}),
                (canonical_bytes({**record, "version": 2}), arguments),
                (canonical_bytes({**record, "payload": {"token": "secret"}}), arguments),
                (canonical_bytes({**record, "payload": {"nested": [{"secret": "x"}]}}), arguments),
                (canonical_bytes({**record, "payload": {"password": "synthetic-secret"}}), arguments),
            ]
            for payload, kwargs in cases:
                with self.subTest(payload=payload, kwargs=kwargs):
                    with self.assertRaises(DispatchDenied):
                        verify_synthetic_evidence(payload, **kwargs)

    def test_unknown_billing_retains_worst_case_and_slot(self) -> None:
        book = SyntheticLiabilityBook("op1", cap=100, worst_case=100)
        unknown = SyntheticAccountingReceipt("r1", "op1", None, False)
        book.intake(unknown, cancelled=True)
        book.intake(unknown)  # identical replay
        book = SyntheticLiabilityBook.recover(
            "op1", 100, 100, book.checkpoint()
        )  # controller restart retains uncertain liability
        self.assertEqual(book.liability, 100)
        self.assertTrue(book.slot_held)
        with self.assertRaisesRegex(DispatchDenied, "contradictory"):
            book.intake(replace(unknown, amount=0))
        with self.assertRaises(DispatchDenied):
            book.intake(SyntheticAccountingReceipt("r2", "op1", 101, True))
        with self.assertRaises(DispatchDenied):
            book.intake(SyntheticAccountingReceipt("r2", "op2", 0, True))
        final = SyntheticAccountingReceipt("r3", "op1", 40, True)
        book.intake(final, cancelled=True)  # late but authoritative receipt
        self.assertEqual(book.liability, 40)
        self.assertFalse(book.slot_held)
        with self.assertRaisesRegex(DispatchDenied, "late"):
            book.intake(SyntheticAccountingReceipt("r4", "op1", 20, True))

    def test_offline_report_never_grants_real_dispatch(self) -> None:
        all_pass = tuple(CapabilityObservation(kind, Finding.SYNTHETIC_PROVEN, "fixture")
                         for kind in Capability)
        with self.assertRaisesRegex(DispatchDenied, "offline proofs"):
            require_real_dispatch(all_pass)
        with self.assertRaisesRegex(DispatchDenied, "unproven"):
            require_real_dispatch(all_pass[:-1])
        with self.assertRaisesRegex(DispatchDenied, "duplicate"):
            require_real_dispatch(all_pass + all_pass[:1])
        for gate in (require_synthetic_dispatch, require_synthetic_validation):
            with self.subTest(gate=gate.__name__), self.assertRaisesRegex(
                DispatchDenied, "synthetic"
            ):
                gate(object(), object())


if __name__ == "__main__":
    unittest.main()
