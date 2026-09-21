from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
import json
import multiprocessing
import sqlite3
import shutil
import tempfile
import threading
import unittest
from unittest.mock import patch
from pathlib import Path
from typing import Mapping

from tools.aegis_delivery_control.authority import (
    SyntheticAuthority,
    SyntheticAuthorityLifecycleEvidence,
    SyntheticGrant,
    SyntheticOperatorGrant,
    SyntheticSettlementProof,
    SyntheticValidatorGrant,
)
from tools.aegis_delivery_control.adapters import (
    SyntheticValidatorAdapter,
    SyntheticValidatorRequest,
)
from tools.aegis_delivery_control.contracts import (
    AuthorityFactKind,
    AuthorityLifecycleFactRequest,
    BindingMismatchKind,
    BindingMismatchRequest,
    BudgetDisposition,
    BudgetSettlementRequest as BudgetSettlementContract,
    DispatchDenied,
    EffectObservationRequest,
    FinalizeOperationRequest,
    InjectedFailure,
    IntentRequest,
    LifecycleState,
    GovernedOrder,
    PauseBeforeDispatchRequest,
    PlanAcceptanceRequest as PlanAcceptanceContract,
    ReadinessEvaluationRequest,
    StopMode,
    StopEscalationRequest,
    StopEscalationSettlement,
    StopRequest,
    StorageIntegrityError,
    TerminalValidationSettlementRequest,
    ValidationApplicationRequest,
    ValidationRecoveryRequest,
    ValidatorCessationRequest,
    ValidatorIntentRequest,
    ValidatorObservationRequest,
)
from tools.aegis_delivery_control.engine import TRANSITIONS, TransitionEngine
from tools.aegis_delivery_control.storage import SQLiteStateStore, raise_at


def BudgetSettlementRequest(*args, **kwargs):
    kwargs.setdefault("repository_id", "repo-1")
    kwargs.setdefault("run_id", "run-1")
    kwargs.setdefault("item_id", "item-1")
    kwargs.setdefault("logical_effect_id", "effect-1")
    reservation_id = kwargs.get("reservation_id")
    if reservation_id is None and len(args) > 1:
        reservation_id = args[1]
    if isinstance(reservation_id, str) and reservation_id.startswith(
        "validator-reservation-"
    ):
        kwargs.setdefault(
            "attempt_id",
            reservation_id.replace("validator-reservation-", "validator-attempt-", 1),
        )
    else:
        kwargs.setdefault("attempt_id", "attempt-1")
    return BudgetSettlementContract(*args, **kwargs)


def PlanAcceptanceRequest(*args, **kwargs):
    """Build a newly accepted synthetic plan with explicit immutable pins."""
    kwargs.setdefault("source_tree_digest", "source-tree-1")
    kwargs.setdefault("item_definition_digest", "item-definition-1")
    kwargs.setdefault("plan_schema_version", "plan-schema-1")
    kwargs.setdefault("reducer_version", "reducer-1")
    return PlanAcceptanceContract(*args, **kwargs)


class MutableFreshnessOracle:
    def __init__(self) -> None:
        self.allowed_head = ""

    def verify(
        self,
        repository_id: str,
        catalog_head: str,
        run_heads: Mapping[str, str],
    ) -> bool:
        return repository_id == "repo-1" and catalog_head == self.allowed_head


def _settle_until_terminated(
    database_path,
    issuer_key,
    allowed_head,
    request,
    stop_stage,
    ready,
):
    oracle = MutableFreshnessOracle()
    oracle.allowed_head = allowed_head
    store = SQLiteStateStore(Path(database_path), oracle, "repo-1")
    authority = SyntheticAuthority(issuer_key)
    store._bind_classification_authority(authority)

    def hold(stage):
        if stage == stop_stage:
            ready.set()
            threading.Event().wait()

    store._settle_budget(
        request,
        authority.issue_settlement_proof("process-proof", request),
        authority,
        failure_hook=hold,
    )


class SQLiteStateStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        database_path = Path(self.temporary_directory.name) / "state.sqlite3"
        self.database_path = database_path
        self.oracle = MutableFreshnessOracle()
        self.store = SQLiteStateStore(
            database_path,
            self.oracle,
            "repo-1",
            utc_now=lambda: datetime(2026, 9, 21, tzinfo=timezone.utc),
        )
        self.authority = SyntheticAuthority()
        self.store._bind_classification_authority(self.authority)
        self.authority.register(
            SyntheticGrant(
                "grant-1", "repo-1", "effect-1", "attempt-1", "scope-1"
            )
        )
        self.capability = self.authority.claim(
            "grant-1", "repo-1", "effect-1", "attempt-1", "scope-1"
        )

    @staticmethod
    def request() -> IntentRequest:
        return IntentRequest(
            repository_id="repo-1",
            run_id="run-1",
            item_id="item-1",
            command_id="command-1",
            event_id="event-1",
            logical_effect_id="effect-1",
            effect_descriptor_digest="descriptor-digest",
            attempt_id="attempt-1",
            permission_use_id="permission-use-1",
            reservation_id="reservation-1",
            budget_policy_digest="budget-policy-digest",
            reserved_units=3,
            worst_case_units=5,
            cap_units=10,
        )

    def _commit_planned_intent(
        self,
        request: IntentRequest,
        capability,
        authority: SyntheticAuthority,
        *,
        expected_head: str,
        writer_epoch: int,
        failure_hook=None,
    ):
        connection = sqlite3.connect(self.database_path)
        try:
            accepted = connection.execute(
                "SELECT event_hash FROM validation_plans WHERE run_id = ?",
                (request.run_id,),
            ).fetchone()
        finally:
            connection.close()
        if accepted is None:
            plan = self.store.accept_plan(
                PlanAcceptanceRequest(
                    f"plan:{request.run_id}",
                    f"plan:{request.command_id}",
                    f"plan:{request.event_id}",
                    request.repository_id,
                    request.run_id,
                    request.item_id,
                    request.logical_effect_id,
                    "revision-1",
                    request.effect_descriptor_digest,
                    capability.scope_digest,
                    request.budget_policy_digest,
                    ("check-1",),
                ),
                expected_head=expected_head,
                writer_epoch=writer_epoch,
            )
            self.oracle.allowed_head = plan.event_hash
            expected_head = plan.event_hash
            writer_epoch += 1
        return self.store.commit_intent(
            request,
            capability,
            authority,
            expected_head=expected_head,
            writer_epoch=writer_epoch,
            failure_hook=failure_hook,
        )

    def _rewrite_application_tail(self, body: dict[str, object]) -> str:
        event_hash = self.store._event_hash(body)
        body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? "
                "WHERE event_id = ?",
                (event_hash, body_json, body["event_id"]),
            )
            connection.execute(
                "UPDATE validation_applications SET event_hash = ?, "
                "resulting_state = ?, continuation_cursor = ?, body_json = ? "
                "WHERE application_id = ?",
                (
                    event_hash, body["lifecycle_to"],
                    body["continuation_cursor"], body_json,
                    body["application_id"],
                ),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                (event_hash, body["command_id"]),
            )
            connection.execute(
                "UPDATE runs SET lifecycle_state = ?, continuation_cursor = ?, "
                "head_hash = ? WHERE run_id = ?",
                (
                    body["lifecycle_to"], body["continuation_cursor"],
                    event_hash, body["run_id"],
                ),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, body["repository_id"]),
            )
            connection.commit()
        finally:
            connection.close()
        return event_hash

    def test_c01_failure_before_commit_leaves_no_authoritative_state(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="",
            writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            before_failure = tuple(connection.iterdump())
        finally:
            connection.close()
        with self.assertRaises(InjectedFailure):
            self.store.commit_intent(
                self.request(),
                self.capability,
                self.authority,
                expected_head=plan.event_hash,
                writer_epoch=2,
                failure_hook=raise_at("after_intent_writes_before_commit"),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            after_failure = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_failure, before_failure)

    def test_t01_denies_plan_without_bound_classification_issuer(self) -> None:
        unbound_path = Path(self.temporary_directory.name) / "unbound.sqlite3"
        unbound_store = SQLiteStateStore(unbound_path, self.oracle, "repo-1")
        with self.assertRaisesRegex(DispatchDenied, "classification authority"):
            unbound_store.accept_plan(
                PlanAcceptanceRequest(
                    "plan-unbound", "command-unbound", "event-unbound",
                    "repo-1", "run-unbound", "item-unbound", "effect-unbound",
                    "revision-unbound", "descriptor-unbound", "scope-unbound",
                    "budget-unbound", ("check-unbound",),
                ),
                expected_head="",
                writer_epoch=1,
            )
        self.assertEqual(unbound_store.table_counts()["validation_plans"], 0)

        self.assertEqual(
            self.store.table_counts(),
            {
                "repositories": 0,
                "runs": 0,
                "validation_plans": 0,
                "validation_requirements": 0,
                "readiness_evaluations": 0,
                "events": 0,
                "command_outcomes": 0,
                "effects": 0,
                "permission_uses": 0,
                "capability_redemptions": 0,
                "budget_reservations": 0,
                "budget_settlements": 0,
                "effect_observations": 0,
                "validator_intents": 0,
                "validator_observations": 0,
                "validator_cessations": 0,
                "validation_applications": 0,
                "validation_recoveries": 0,
                "terminal_validation_settlements": 0,
                "operation_finalizations": 0,
                "operation_launches": 0,
                "control_actions": 0,
                "stop_actions": 0,
                "stop_escalations": 0,
                "operator_redemptions": 0,
                "outstanding_slot": 0,
                "dispatch_fences": 0,
                "binding_mismatches": 0,
            },
        )

    def test_t15_new_plan_requires_explicit_immutable_binding_pins(self) -> None:
        with self.assertRaisesRegex(ValueError, "immutable binding pins"):
            self.store.accept_plan(
                PlanAcceptanceContract(
                    "plan-unpinned", "command-unpinned", "event-unpinned",
                    "repo-1", "run-unpinned", "item-unpinned", "effect-unpinned",
                    "revision-unpinned", "descriptor-unpinned", "scope-unpinned",
                    "budget-unpinned", ("check-unpinned",),
                ),
                expected_head="",
                writer_epoch=1,
            )
        with self.assertRaisesRegex(ValueError, "immutable binding pins"):
            PlanAcceptanceContract(
                "plan-partial", "command-partial", "event-partial",
                "repo-1", "run-partial", "item-partial", "effect-partial",
                "revision-partial", "descriptor-partial", "scope-partial",
                "budget-partial", ("check-partial",),
                source_tree_digest="only-one-pin",
            ).validate()
        with self.assertRaisesRegex(ValueError, "must differ"):
            BindingMismatchRequest(
                "mismatch-equal", "observation-equal", "command-equal",
                "event-equal", "repo-1", "run-1", "item-1", "effect-1",
                BindingMismatchKind.SOURCE, "same", "same", "head",
                "BINDING_MISMATCH_SOURCE",
            ).validate()

    def test_t15_persists_semantic_and_complete_policy_bindings(self) -> None:
        receipt = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-pinned", "command-pinned", "event-pinned",
                "repo-1", "run-pinned", "item-pinned", "effect-pinned",
                "revision-pinned", "descriptor-pinned", "scope-pinned",
                "budget-pinned", ("check-b", "check-a"), ("gate-b", "gate-a"),
                source_tree_digest="source-pinned",
                item_definition_digest="item-definition-pinned",
                plan_schema_version="schema-pinned",
                reducer_version="reducer-pinned",
            ),
            expected_head="",
            writer_epoch=1,
        )
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            columns = {
                row["name"]
                for row in connection.execute("PRAGMA table_info(validation_plans)")
            }
            row = connection.execute(
                "SELECT * FROM validation_plans WHERE plan_id = 'plan-pinned'"
            ).fetchone()
            body = json.loads(row["body_json"])
        finally:
            connection.close()
        expected_columns = {
            "source_tree_digest", "item_definition_digest",
            "plan_schema_version", "reducer_version",
            "accepted_plan_semantic_digest", "complete_policy_digest",
        }
        self.assertTrue(expected_columns.issubset(columns))
        self.assertEqual(row["source_tree_digest"], "source-pinned")
        self.assertEqual(row["item_definition_digest"], "item-definition-pinned")
        self.assertTrue(row["accepted_plan_semantic_digest"])
        self.assertTrue(row["complete_policy_digest"])
        self.assertEqual(body["failure_policy_id"], "failure-policy")
        self.assertEqual(body["failure_policy_version"], "1")
        self.oracle.allowed_head = receipt.event_hash
        catalog_head, run_heads = self.store.load_verified("repo-1")
        self.assertEqual(catalog_head, receipt.event_hash)
        self.assertEqual(run_heads["run-pinned"], receipt.event_hash)

    def test_t15_source_mismatch_atomically_fences_and_blocks_idle_run(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="",
            writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        request = BindingMismatchRequest(
            "mismatch-1", "observation-1", "mismatch-command-1",
            "mismatch-event-1", "repo-1", "run-1", "item-1", "effect-1",
            BindingMismatchKind.SOURCE, "source-tree-1", "source-tree-2",
            plan.event_hash, "BINDING_MISMATCH_SOURCE",
        )
        receipt = self.store.record_binding_mismatch(
            request,
            self.authority.issue_binding_observation(request),
            self.authority,
            expected_head=plan.event_hash,
            writer_epoch=2,
        )
        self.assertEqual(receipt.resulting_state, LifecycleState.BLOCKED)
        connection = sqlite3.connect(self.database_path)
        try:
            mismatch = connection.execute(
                "SELECT mismatch_kind, fence_id FROM binding_mismatches"
            ).fetchone()
            fences = connection.execute(
                "SELECT reason_code FROM dispatch_fences"
            ).fetchall()
        finally:
            connection.close()
        self.assertEqual(mismatch[0], BindingMismatchKind.SOURCE.value)
        self.assertTrue(mismatch[1].startswith("binding:"))
        self.assertEqual(fences, [("BINDING_MISMATCH_SOURCE",)])
        self.oracle.allowed_head = receipt.event_hash
        catalog_head, run_heads = self.store.load_verified(
            "repo-1", authority=self.authority
        )
        self.assertEqual(catalog_head, receipt.event_hash)
        self.assertEqual(run_heads["run-1"], receipt.event_hash)
        readiness = self.store.evaluate_readiness(
            ReadinessEvaluationRequest(
                "readiness-after-t15", "readiness-command-after-t15",
                "readiness-event-after-t15", "repo-1", "run-1", "item-1",
                "plan-1", "revision-1", receipt.event_hash, None,
                "inputs-after-t15", True,
            )
        )
        self.assertEqual(readiness.resulting_state, LifecycleState.BLOCKED)
        self.oracle.allowed_head = readiness.event_hash
        self.store.load_verified("repo-1", authority=self.authority)

    def test_t15_exact_kind_mapping_recovery_and_observation_freshness(self) -> None:
        head = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        ).event_hash
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            plan = connection.execute(
                "SELECT * FROM validation_plans WHERE plan_id = 'plan-1'"
            ).fetchone()
            expected_by_kind = {
                BindingMismatchKind.SOURCE: plan["source_tree_digest"],
                BindingMismatchKind.ITEM: plan["item_definition_digest"],
                BindingMismatchKind.PLAN: plan["accepted_plan_semantic_digest"],
                BindingMismatchKind.POLICY: plan["complete_policy_digest"],
            }
        finally:
            connection.close()
        first_request = None
        for index, (kind, expected) in enumerate(expected_by_kind.items(), start=2):
            self.oracle.allowed_head = head
            request = BindingMismatchRequest(
                f"mismatch-{index}", f"observation-{index}",
                f"mismatch-command-{index}", f"mismatch-event-{index}",
                "repo-1", "run-1", "item-1", "effect-1", kind,
                str(expected), f"observed-{kind.value.lower()}", head,
                f"BINDING_MISMATCH_{kind.value}",
            )
            receipt = self.store.record_binding_mismatch(
                request, self.authority.issue_binding_observation(request),
                self.authority, expected_head=head, writer_epoch=index,
            )
            self.assertEqual(receipt.resulting_state, LifecycleState.BLOCKED)
            head = receipt.event_hash
            if first_request is None:
                first_request = request
        self.oracle.allowed_head = head
        self.store.load_verified("repo-1", authority=self.authority)
        connection = sqlite3.connect(self.database_path)
        try:
            recorded_kinds = {
                row[0]
                for row in connection.execute(
                    "SELECT mismatch_kind FROM binding_mismatches"
                )
            }
        finally:
            connection.close()
        self.assertEqual(
            recorded_kinds, {kind.value for kind in BindingMismatchKind}
        )
        assert first_request is not None
        replayed_observation = replace(
            first_request,
            mismatch_id="mismatch-rebound",
            command_id="mismatch-command-rebound",
            event_id="mismatch-event-rebound",
            evidence_head=head,
        )
        with self.assertRaisesRegex(StorageIntegrityError, "identity was rebound"):
            self.store.record_binding_mismatch(
                replayed_observation,
                self.authority.issue_binding_observation(replayed_observation),
                self.authority,
                expected_head=head,
                writer_epoch=6,
            )

    def test_t15_rejects_forged_stale_and_store_unverified_mismatch(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        valid = BindingMismatchRequest(
            "mismatch-1", "observation-1", "mismatch-command-1",
            "mismatch-event-1", "repo-1", "run-1", "item-1", "effect-1",
            BindingMismatchKind.SOURCE, "source-tree-1", "source-tree-2",
            plan.event_hash, "BINDING_MISMATCH_SOURCE",
        )
        connection = sqlite3.connect(self.database_path)
        try:
            before = tuple(connection.iterdump())
        finally:
            connection.close()
        forged = replace(
            self.authority.issue_binding_observation(valid), issuer_mac="0" * 64
        )
        with self.assertRaisesRegex(DispatchDenied, "not issued here"):
            self.store.record_binding_mismatch(
                valid, forged, self.authority,
                expected_head=plan.event_hash, writer_epoch=2,
            )
        cross_bound = replace(
            valid, mismatch_id="mismatch-cross", command_id="command-cross",
            event_id="event-cross", observed_digest="source-tree-cross",
        )
        with self.assertRaisesRegex(DispatchDenied, "not issued here"):
            self.store.record_binding_mismatch(
                cross_bound,
                self.authority.issue_binding_observation(valid),
                self.authority,
                expected_head=plan.event_hash,
                writer_epoch=2,
            )
        wrong_expected = replace(
            valid, mismatch_id="mismatch-2", observation_id="observation-2",
            command_id="mismatch-command-2", event_id="mismatch-event-2",
            expected_digest="caller-invented-binding",
        )
        with self.assertRaisesRegex(DispatchDenied, "accepted binding"):
            self.store.record_binding_mismatch(
                wrong_expected,
                self.authority.issue_binding_observation(wrong_expected),
                self.authority,
                expected_head=plan.event_hash, writer_epoch=2,
            )
        stale = replace(
            valid, mismatch_id="mismatch-3", observation_id="observation-3",
            command_id="mismatch-command-3", event_id="mismatch-event-3",
            evidence_head="stale-head",
        )
        with self.assertRaisesRegex(DispatchDenied, "evidence head is stale"):
            self.store.record_binding_mismatch(
                stale, self.authority.issue_binding_observation(stale),
                self.authority,
                expected_head="stale-head", writer_epoch=2,
            )
        foreign_item = replace(
            valid, mismatch_id="mismatch-foreign",
            observation_id="observation-foreign",
            command_id="command-foreign", event_id="event-foreign",
            item_id="item-foreign",
        )
        with self.assertRaisesRegex(DispatchDenied, "accepted plan"):
            self.store.record_binding_mismatch(
                foreign_item,
                self.authority.issue_binding_observation(foreign_item),
                self.authority,
                expected_head=plan.event_hash,
                writer_epoch=2,
            )
        connection = sqlite3.connect(self.database_path)
        try:
            after = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after, before)

    def test_t15_recovery_rejects_rehashed_forged_observation(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        request = BindingMismatchRequest(
            "mismatch-1", "observation-1", "mismatch-command-1",
            "mismatch-event-1", "repo-1", "run-1", "item-1", "effect-1",
            BindingMismatchKind.SOURCE, "source-tree-1", "source-tree-2",
            plan.event_hash, "BINDING_MISMATCH_SOURCE",
        )
        receipt = self.store.record_binding_mismatch(
            request, self.authority.issue_binding_observation(request),
            self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    (request.event_id,),
                ).fetchone()[0]
            )
            body["observation_issuer_mac"] = "0" * 64
            body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
            forged_hash = self.store._event_hash(body)
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (forged_hash, body_json, request.event_id),
            )
            connection.execute(
                "UPDATE binding_mismatches SET issuer_mac = ?, event_hash = ?, "
                "body_json = ? WHERE mismatch_id = ?",
                ("0" * 64, forged_hash, body_json, request.mismatch_id),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                (forged_hash, request.command_id),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = ?",
                (forged_hash, request.run_id),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (forged_hash, request.repository_id),
            )
            connection.commit()
        finally:
            connection.close()
        self.assertNotEqual(forged_hash, receipt.event_hash)
        self.oracle.allowed_head = forged_hash
        with self.assertRaisesRegex(
            StorageIntegrityError, "binding mismatch proof or schema"
        ):
            self.store.load_verified("repo-1", authority=self.authority)

    def test_t15_recovery_rederives_plan_and_policy_digests(self) -> None:
        receipt = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            plan = connection.execute(
                "SELECT * FROM validation_plans WHERE plan_id = 'plan-1'"
            ).fetchone()
            original_body_json = plan["body_json"]
            original_body = json.loads(original_body_json)
            original_values = {
                "accepted_plan_semantic_digest": plan[
                    "accepted_plan_semantic_digest"
                ],
                "complete_policy_digest": plan["complete_policy_digest"],
            }
        finally:
            connection.close()
        for field in original_values:
            with self.subTest(field=field):
                forged_body = dict(original_body)
                forged_body[field] = f"forged-{field}"
                forged_body_json = json.dumps(
                    forged_body, sort_keys=True, separators=(",", ":")
                )
                forged_hash = self.store._event_hash(forged_body)
                connection = sqlite3.connect(self.database_path)
                try:
                    connection.execute(
                        "UPDATE events SET event_hash = ?, body_json = ? "
                        "WHERE event_id = 'plan-event-1'",
                        (forged_hash, forged_body_json),
                    )
                    connection.execute(
                        f"UPDATE validation_plans SET {field} = ?, "
                        "event_hash = ?, body_json = ? WHERE plan_id = 'plan-1'",
                        (forged_body[field], forged_hash, forged_body_json),
                    )
                    connection.execute(
                        "UPDATE command_outcomes SET event_hash = ? "
                        "WHERE command_id = 'plan-command-1'",
                        (forged_hash,),
                    )
                    connection.execute(
                        "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                        (forged_hash,),
                    )
                    connection.execute(
                        "UPDATE repositories SET catalog_head = ? "
                        "WHERE repository_id = 'repo-1'",
                        (forged_hash,),
                    )
                    connection.commit()
                finally:
                    connection.close()
                self.oracle.allowed_head = forged_hash
                with self.assertRaisesRegex(
                    StorageIntegrityError,
                    "plan (semantic|policy) digest diverges",
                ):
                    self.store.load_verified("repo-1", authority=self.authority)
                connection = sqlite3.connect(self.database_path)
                try:
                    connection.execute(
                        "UPDATE events SET event_hash = ?, body_json = ? "
                        "WHERE event_id = 'plan-event-1'",
                        (receipt.event_hash, original_body_json),
                    )
                    connection.execute(
                        f"UPDATE validation_plans SET {field} = ?, "
                        "event_hash = ?, body_json = ? WHERE plan_id = 'plan-1'",
                        (
                            original_values[field], receipt.event_hash,
                            original_body_json,
                        ),
                    )
                    connection.execute(
                        "UPDATE command_outcomes SET event_hash = ? "
                        "WHERE command_id = 'plan-command-1'",
                        (receipt.event_hash,),
                    )
                    connection.execute(
                        "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                        (receipt.event_hash,),
                    )
                    connection.execute(
                        "UPDATE repositories SET catalog_head = ? "
                        "WHERE repository_id = 'repo-1'",
                        (receipt.event_hash,),
                    )
                    connection.commit()
                finally:
                    connection.close()
                self.oracle.allowed_head = receipt.event_hash
                self.store.load_verified("repo-1", authority=self.authority)

    def test_t15_crash_replay_is_atomic_and_preserves_effect_identity(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        request = BindingMismatchRequest(
            "mismatch-1", "observation-1", "mismatch-command-1",
            "mismatch-event-1", "repo-1", "run-1", "item-1", "effect-1",
            BindingMismatchKind.ITEM, "item-definition-1", "item-definition-2",
            plan.event_hash, "BINDING_MISMATCH_ITEM",
        )
        observation = self.authority.issue_binding_observation(request)
        connection = sqlite3.connect(self.database_path)
        try:
            immutable_before = {
                table: tuple(connection.execute(f"SELECT * FROM {table}"))
                for table in (
                    "validation_plans", "validation_requirements", "effects",
                    "permission_uses", "budget_reservations", "outstanding_slot",
                )
            }
            database_before = tuple(connection.iterdump())
        finally:
            connection.close()
        with self.assertRaises(InjectedFailure):
            self.store.record_binding_mismatch(
                request, observation, self.authority,
                expected_head=plan.event_hash, writer_epoch=2,
                failure_hook=raise_at(
                    "after_binding_mismatch_writes_before_commit"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            self.assertEqual(tuple(connection.iterdump()), database_before)
        finally:
            connection.close()
        with self.assertRaises(InjectedFailure):
            self.store.record_binding_mismatch(
                request, observation, self.authority,
                expected_head=plan.event_hash, writer_epoch=2,
                failure_hook=raise_at(
                    "after_binding_mismatch_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            committed_head = connection.execute(
                "SELECT head_hash FROM runs WHERE run_id = 'run-1'"
            ).fetchone()[0]
            immutable_after = {
                table: tuple(connection.execute(f"SELECT * FROM {table}"))
                for table in immutable_before
            }
        finally:
            connection.close()
        self.assertEqual(immutable_after, immutable_before)
        self.oracle.allowed_head = committed_head
        replay = self.store.record_binding_mismatch(
            request, observation, self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        self.assertTrue(replay.replayed)
        self.assertEqual(replay.event_hash, committed_head)
        with self.assertRaisesRegex(DispatchDenied, "durable PLANNED state"):
            self.store.commit_intent(
                self.request(), self.capability, self.authority,
                expected_head=committed_head, writer_epoch=3,
            )

    def test_t15_partial_plan_binding_schema_is_rejected_without_completion(self) -> None:
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "ALTER TABLE validation_plans DROP COLUMN complete_policy_digest"
            )
            connection.commit()
            before_columns = tuple(
                row[1]
                for row in connection.execute(
                    "PRAGMA table_info(validation_plans)"
                )
            )
        finally:
            connection.close()
        with self.assertRaisesRegex(StorageIntegrityError, "partially migrated"):
            SQLiteStateStore(self.database_path, self.oracle, "repo-1")
        connection = sqlite3.connect(self.database_path)
        try:
            after_columns = tuple(
                row[1]
                for row in connection.execute(
                    "PRAGMA table_info(validation_plans)"
                )
            )
        finally:
            connection.close()
        self.assertEqual(after_columns, before_columns)

    def test_t15_active_mismatch_reconciles_without_changing_effect_or_slot(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            effects_before = tuple(connection.execute("SELECT * FROM effects"))
            slot_before = tuple(
                connection.execute("SELECT * FROM outstanding_slot")
            )
            plan_before = tuple(
                connection.execute("SELECT * FROM validation_plans")
            )
        finally:
            connection.close()
        request = BindingMismatchRequest(
            "mismatch-active", "observation-active", "command-active",
            "event-active", "repo-1", "run-1", "item-1", "effect-1",
            BindingMismatchKind.SOURCE, "source-tree-1", "source-tree-2",
            committed.event_hash, "BINDING_MISMATCH_SOURCE",
        )
        receipt = self.store.record_binding_mismatch(
            request, self.authority.issue_binding_observation(request),
            self.authority,
            expected_head=committed.event_hash, writer_epoch=3,
        )
        self.assertEqual(
            receipt.resulting_state, LifecycleState.RECONCILIATION_REQUIRED
        )
        connection = sqlite3.connect(self.database_path)
        try:
            self.assertEqual(
                tuple(connection.execute("SELECT * FROM effects")),
                effects_before,
            )
            self.assertEqual(
                tuple(connection.execute("SELECT * FROM outstanding_slot")),
                slot_before,
            )
            self.assertEqual(
                tuple(connection.execute("SELECT * FROM validation_plans")),
                plan_before,
            )
        finally:
            connection.close()

    def test_t15_lifecycle_route_is_closed_and_preserves_paused(self) -> None:
        expected = {
            LifecycleState.PLANNED: LifecycleState.BLOCKED,
            LifecycleState.BLOCKED: LifecycleState.BLOCKED,
            LifecycleState.PAUSED: LifecycleState.PAUSED,
            LifecycleState.RUNNING: LifecycleState.RECONCILIATION_REQUIRED,
            LifecycleState.PAUSING: LifecycleState.RECONCILIATION_REQUIRED,
            LifecycleState.VALIDATING: LifecycleState.RECONCILIATION_REQUIRED,
            LifecycleState.RECONCILIATION_REQUIRED: (
                LifecycleState.RECONCILIATION_REQUIRED
            ),
        }
        for current, resulting in expected.items():
            with self.subTest(current=current):
                self.assertEqual(
                    self.store._binding_mismatch_route(
                        current, active_or_uncertain=False
                    ),
                    resulting,
                )
        self.assertEqual(
            self.store._binding_mismatch_route(
                LifecycleState.BLOCKED, active_or_uncertain=True
            ),
            LifecycleState.RECONCILIATION_REQUIRED,
        )
        for terminal in (
            LifecycleState.COMPLETED,
            LifecycleState.FAILED_FINAL,
            LifecycleState.STOPPED,
        ):
            with self.subTest(terminal=terminal):
                with self.assertRaisesRegex(DispatchDenied, "nonterminal"):
                    self.store._binding_mismatch_route(
                        terminal, active_or_uncertain=False
                    )

    def test_t15_blocked_owned_slot_routes_to_reconciliation(self) -> None:
        self._prepare_finalization()
        connection = sqlite3.connect(self.database_path)
        try:
            state_before = connection.execute(
                "SELECT lifecycle_state, continuation_cursor, head_hash "
                "FROM runs WHERE run_id = 'run-1'"
            ).fetchone()
            writer_epoch = connection.execute(
                "SELECT MAX(writer_epoch) + 1 FROM events"
            ).fetchone()[0]
            slot_before = tuple(
                connection.execute("SELECT * FROM outstanding_slot")
            )
        finally:
            connection.close()
        self.assertEqual(state_before[:2], ("BLOCKED", "FINALIZING"))
        self.assertEqual(len(slot_before), 1)
        request = BindingMismatchRequest(
            "mismatch-blocked", "observation-blocked", "command-blocked",
            "event-blocked", "repo-1", "run-1", "item-1", "effect-1",
            BindingMismatchKind.SOURCE, "source-tree-1", "source-tree-2",
            state_before[2], "BINDING_MISMATCH_SOURCE",
        )
        observation = self.authority.issue_binding_observation(request)
        with self.assertRaises(InjectedFailure):
            self.store.record_binding_mismatch(
                request, observation, self.authority,
                expected_head=state_before[2], writer_epoch=writer_epoch,
                failure_hook=raise_at(
                    "after_binding_mismatch_writes_before_commit"
                ),
            )
        self.assertEqual(
            self.store.load_run_lifecycle("run-1"), LifecycleState.BLOCKED
        )
        receipt = self.store.record_binding_mismatch(
            request, observation, self.authority,
            expected_head=state_before[2], writer_epoch=writer_epoch,
        )
        self.assertEqual(
            receipt.resulting_state, LifecycleState.RECONCILIATION_REQUIRED
        )
        connection = sqlite3.connect(self.database_path)
        try:
            state_after = connection.execute(
                "SELECT lifecycle_state, continuation_cursor FROM runs "
                "WHERE run_id = 'run-1'"
            ).fetchone()
            slot_after = tuple(
                connection.execute("SELECT * FROM outstanding_slot")
            )
        finally:
            connection.close()
        self.assertEqual(
            state_after, ("RECONCILIATION_REQUIRED", "FINALIZING")
        )
        self.assertEqual(slot_after, slot_before)
        self.oracle.allowed_head = receipt.event_hash
        self.store.load_verified("repo-1", authority=self.authority)

    def test_t15_paused_run_retains_pause_and_terminal_run_rejects(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        paused = self.store.pause_before_dispatch(
            self._pause_request("t15"), self._pause_capability("t15"),
            self.authority,
        )
        self.oracle.allowed_head = paused.event_hash
        request = BindingMismatchRequest(
            "mismatch-paused", "observation-paused", "command-paused",
            "event-paused", "repo-1", "run-1", "item-1", "effect-1",
            BindingMismatchKind.SOURCE, "source-tree-1", "source-tree-2",
            paused.event_hash, "BINDING_MISMATCH_SOURCE",
        )
        mismatch = self.store.record_binding_mismatch(
            request, self.authority.issue_binding_observation(request),
            self.authority,
            expected_head=paused.event_hash, writer_epoch=3,
        )
        self.assertEqual(mismatch.resulting_state, LifecycleState.PAUSED)
        self.oracle.allowed_head = mismatch.event_hash
        stopped = self.store.stop(
            self._stop_request(StopMode.IMMEDIATE, "t15"),
            self._stop_capability(StopMode.IMMEDIATE, "t15"),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            policy_digest = connection.execute(
                "SELECT complete_policy_digest FROM validation_plans "
                "WHERE plan_id = 'plan-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        terminal_request = BindingMismatchRequest(
            "mismatch-terminal", "observation-terminal", "command-terminal",
            "event-terminal", "repo-1", "run-1", "item-1", "effect-1",
            BindingMismatchKind.POLICY,
            policy_digest,
            "changed-policy", stopped.event_hash, "BINDING_MISMATCH_POLICY",
        )
        connection = sqlite3.connect(self.database_path)
        try:
            before = tuple(connection.iterdump())
        finally:
            connection.close()
        with self.assertRaisesRegex(DispatchDenied, "nonterminal"):
            self.store.record_binding_mismatch(
                terminal_request,
                self.authority.issue_binding_observation(terminal_request),
                self.authority,
                expected_head=stopped.event_hash,
                writer_epoch=5,
            )
        connection = sqlite3.connect(self.database_path)
        try:
            after = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after, before)

    def test_t03_requires_exact_accepted_plan_and_rejects_run_substitution(self) -> None:
        connection = sqlite3.connect(self.database_path)
        try:
            empty_state = tuple(connection.iterdump())
        finally:
            connection.close()
        with self.assertRaisesRegex(DispatchDenied, "accepted plan"):
            self.store.commit_intent(
                self.request(), self.capability, self.authority,
                expected_head="", writer_epoch=1,
            )
        connection = sqlite3.connect(self.database_path)
        try:
            after_missing_plan = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_missing_plan, empty_state)

        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        alternate_grant = SyntheticGrant(
            "grant-plan-scope", "repo-1", "effect-1", "attempt-1", "scope-2"
        )
        self.authority.register(alternate_grant)
        alternate_capability = self.authority.claim(
            *alternate_grant.__dict__.values()
        )
        for changed_request, changed_capability in (
            (
                replace(
                    self.request(), effect_descriptor_digest="descriptor-revision-2"
                ),
                self.capability,
            ),
            (
                replace(self.request(), budget_policy_digest="budget-revision-2"),
                self.capability,
            ),
            (self.request(), alternate_capability),
        ):
            connection = sqlite3.connect(self.database_path)
            try:
                before_pin_denial = tuple(connection.iterdump())
            finally:
                connection.close()
            with self.assertRaisesRegex(DispatchDenied, "execution pins"):
                self.store.commit_intent(
                    changed_request, changed_capability, self.authority,
                    expected_head=plan.event_hash, writer_epoch=2,
                )
            connection = sqlite3.connect(self.database_path)
            try:
                after_pin_denial = tuple(connection.iterdump())
            finally:
                connection.close()
            self.assertEqual(after_pin_denial, before_pin_denial)

        substituted = replace(
            self.request(), run_id="run-2", item_id="item-2",
            command_id="command-2", event_id="event-2",
        )
        connection = sqlite3.connect(self.database_path)
        try:
            before_substitution = tuple(connection.iterdump())
        finally:
            connection.close()
        with self.assertRaisesRegex(DispatchDenied, "accepted plan"):
            self.store.commit_intent(
                substituted, self.capability, self.authority,
                expected_head=plan.event_hash, writer_epoch=2,
            )
        connection = sqlite3.connect(self.database_path)
        try:
            after_substitution = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_substitution, before_substitution)

        committed = self.store.commit_intent(
            self.request(), self.capability, self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = 'event-1'"
                ).fetchone()[0]
            )
        finally:
            connection.close()
        self.assertEqual(body["plan_id"], "plan-1")
        self.assertEqual(body["revision_digest"], "revision-1")
        self.assertEqual(committed.sequence, 2)

    def test_intent_commit_is_atomic_and_replay_is_idempotent(self) -> None:
        first = self._commit_planned_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = first.event_hash
        replay = self._commit_planned_intent(
            self.request(), self.capability, self.authority, expected_head=first.event_hash, writer_epoch=2
        )

        self.assertFalse(first.replayed)
        self.assertTrue(replay.replayed)
        self.assertEqual(replay.event_hash, first.event_hash)
        self.assertEqual(
            self.store.table_counts(),
            {
                "repositories": 1,
                "runs": 1,
                "validation_plans": 1,
                "validation_requirements": 1,
                "readiness_evaluations": 0,
                "events": 2,
                "command_outcomes": 2,
                "effects": 1,
                "permission_uses": 1,
                "capability_redemptions": 1,
                "budget_reservations": 1,
                "budget_settlements": 0,
                "effect_observations": 0,
                "validator_intents": 0,
                "validator_observations": 0,
                "validator_cessations": 0,
                "validation_applications": 0,
                "validation_recoveries": 0,
                "terminal_validation_settlements": 0,
                "operation_finalizations": 0,
                "operation_launches": 0,
                "control_actions": 0,
                "stop_actions": 0,
                "stop_escalations": 0,
                "operator_redemptions": 0,
                "outstanding_slot": 1,
                "dispatch_fences": 0,
                "binding_mismatches": 0,
            },
        )

    def test_recovery_rejects_tampered_operation_launch_projection(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            before_rebound = tuple(connection.iterdump())
        finally:
            connection.close()
        with self.assertRaisesRegex(DispatchDenied, "changed the durable intent"):
            self.store.claim_operation_launch(
                replace(self.request(), item_id="item-2"), committed
            )
        connection = sqlite3.connect(self.database_path)
        try:
            after_rebound = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_rebound, before_rebound)
        launched = self.store.claim_operation_launch(self.request(), committed)
        self.oracle.allowed_head = launched.event_hash
        baseline_path = (
            Path(self.temporary_directory.name) / "launch-baseline.sqlite3"
        )
        shutil.copy2(self.database_path, baseline_path)
        tamper_cases = (
            (
                "delete",
                "DELETE FROM operation_launches WHERE launch_id = ?",
                (launched.launch_id,),
            ),
            (
                "body",
                "UPDATE operation_launches SET body_json = '{}' "
                "WHERE launch_id = ?",
                (launched.launch_id,),
            ),
            (
                "event-link",
                "UPDATE operation_launches SET intent_event_id = 'other-event' "
                "WHERE launch_id = ?",
                (launched.launch_id,),
            ),
            (
                "cross-run",
                "UPDATE operation_launches SET run_id = 'other-run' "
                "WHERE launch_id = ?",
                (launched.launch_id,),
            ),
            (
                "extra-row",
                "INSERT INTO operation_launches SELECT launch_id || ':extra', "
                "event_id || ':extra', repository_id, run_id, item_id, "
                "logical_effect_id || ':extra', attempt_id || ':extra', "
                "capability_claim_id || ':extra', "
                "intent_event_id, intent_event_hash, 'extra-hash', '{}' "
                "FROM operation_launches WHERE launch_id = ?",
                (launched.launch_id,),
            ),
        )
        for name, statement, parameters in tamper_cases:
            with self.subTest(name=name):
                test_path = (
                    Path(self.temporary_directory.name)
                    / f"launch-tamper-{name}.sqlite3"
                )
                shutil.copy2(baseline_path, test_path)
                connection = sqlite3.connect(test_path)
                try:
                    connection.execute(statement, parameters)
                    connection.commit()
                finally:
                    connection.close()
                with self.assertRaisesRegex(
                    StorageIntegrityError, "operation-launch projection"
                ):
                    SQLiteStateStore(
                        test_path, self.oracle, "repo-1"
                    ).load_verified("repo-1")

    def test_contact_claim_without_target_receipt_denies_redispatch(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        launch = self.store.claim_operation_launch(self.request(), committed)
        self.oracle.allowed_head = launch.event_hash

        self.store._contact_claimed_operation(
            self.request(), self.capability, committed, launch,
            self.store._adapter_target_digest("repo-1", "EFFECT"),
        )
        connection = sqlite3.connect(self.database_path)
        try:
            contact_count, contact_head = connection.execute(
                "SELECT COUNT(*), MAX(event_hash) FROM adapter_contacts"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(contact_count, 1)
        self.oracle.allowed_head = contact_head
        with self.assertRaisesRegex(DispatchDenied, "already claimed"):
            self.store._contact_claimed_operation(
                self.request(), self.capability, committed, launch,
                self.store._adapter_target_digest("repo-1", "EFFECT"),
            )
        self.store.load_verified("repo-1")
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute("DELETE FROM adapter_contacts")
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(StorageIntegrityError, "contact projection"):
            self.store.load_verified("repo-1")

    def test_f04_unknown_usage_charges_worst_case_and_retains_slot(self) -> None:
        committed = self._commit_planned_intent(self.request(), self.capability, self.authority, expected_head="", writer_epoch=1)
        self.oracle.allowed_head = committed.event_hash
        request = BudgetSettlementRequest(
                settlement_event_id="settlement-1",
                reservation_id="reservation-1",
                expected_previous_hash="",
                disposition=BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED,
                actual_units=None,
                evidence_digest="missing-telemetry",
                reason_code="USAGE_UNKNOWN",
                release_slot=False,
            )
        proof = self.authority.issue_settlement_proof(
            "proof-1",
            request,
        )
        receipt = self.store._settle_budget(request, proof, self.authority)
        self.assertEqual(receipt.charged_units, 5)
        self.assertTrue(receipt.uncertainty)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

    def test_recovery_derives_settlement_charges_instead_of_trusting_event(
        self,
    ) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        request = BudgetSettlementRequest(
            "settlement-1", "reservation-1", "",
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "missing-telemetry", "USAGE_UNKNOWN",
        )
        receipt = self.store._settle_budget(
            request,
            self.authority.issue_settlement_proof("proof-1", request),
            self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM budget_settlements WHERE "
                    "settlement_event_id = 'settlement-1'"
                ).fetchone()["body_json"]
            )
            body["charged_units"] = 1
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE budget_settlements SET charged_units = 1, "
                "settlement_hash = ?, body_json = ? WHERE "
                "settlement_event_id = 'settlement-1'",
                (event_hash, body_json),
            )
            connection.execute(
                "UPDATE budget_reservations SET charged_units = 1, "
                "settlement_head_hash = ? WHERE reservation_id = 'reservation-1'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                "event_id = 'settlement-1'",
                (event_hash, body_json),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE "
                "repository_id = 'repo-1'",
                (event_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(
            StorageIntegrityError, "settlement accounting semantics"
        ):
            self.store.load_verified("repo-1")

    def test_recovery_derives_effect_receipt_lifecycle_routing(self) -> None:
        observation = self._record_effect_observation()
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM effect_observations WHERE "
                    "observation_id = 'observation-1'"
                ).fetchone()["body_json"]
            )
            body["lifecycle_to"] = LifecycleState.COMPLETED.value
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE effect_observations SET resulting_state = 'COMPLETED', "
                "event_hash = ?, body_json = ? WHERE observation_id = "
                "'observation-1'",
                (event_hash, body_json),
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                "event_id = 'observation-event-1'",
                (event_hash, body_json),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE "
                "command_id = 'observe-command-1'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE runs SET lifecycle_state = 'COMPLETED', head_hash = ? "
                "WHERE run_id = 'run-1'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE "
                "repository_id = 'repo-1'",
                (event_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(
            StorageIntegrityError, "effect observation semantics"
        ):
            self.store.load_verified("repo-1")

    def test_recovery_derives_contradiction_fence_from_prior_evidence(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        request = BudgetSettlementRequest(
            "settlement-1", "reservation-1", "",
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "missing-telemetry", "USAGE_UNKNOWN",
        )
        self.store._settle_budget(
            request,
            self.authority.issue_settlement_proof("proof-1", request),
            self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM budget_settlements WHERE "
                    "settlement_event_id = 'settlement-1'"
                ).fetchone()["body_json"]
            )
            body["contradiction"] = True
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE budget_settlements SET settlement_hash = ?, "
                "body_json = ? WHERE settlement_event_id = 'settlement-1'",
                (event_hash, body_json),
            )
            connection.execute(
                "UPDATE budget_reservations SET settlement_head_hash = ? "
                "WHERE reservation_id = 'reservation-1'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                "event_id = 'settlement-1'",
                (event_hash, body_json),
            )
            connection.execute(
                "INSERT INTO dispatch_fences VALUES (?, ?, ?, ?, ?, ?)",
                (
                    "nonexecution-contradiction:settlement-1", "repo-1",
                    "item-1", "effect-1", "NONEXECUTION_CONTRADICTION",
                    "settlement-1",
                ),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE "
                "repository_id = 'repo-1'",
                (event_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(
            StorageIntegrityError, "settlement contradiction semantics"
        ):
            self.store.load_verified("repo-1")

    def test_settlement_proof_rejects_cross_domain_delimiter_collision(self) -> None:
        authority = SyntheticAuthority(b"a" * 32)
        grant = SyntheticGrant(
            "grant-1", "repo-1", "1", "1", "1"
        )
        authority.register(grant)
        capability = authority.claim(*grant.__dict__.values())
        forged = SyntheticSettlementProof(
            capability.claim_id,
            "grant-1\0repo-1",
            True,
            True,
            True,
            capability.issuer_mac,
            capability.issuer_mac,
        )

        with self.assertRaisesRegex(DispatchDenied, "was not issued here"):
            authority.verify_settlement_proof(
                forged,
                BudgetSettlementRequest(
                    "settlement-1", "reservation-1", "",
                    BudgetDisposition.CONSUMED, 1, "evidence-1", "USAGE_REPORTED",
                ),
            )

    def test_settlement_proof_rejects_altered_request(self) -> None:
        request = BudgetSettlementRequest(
            "settlement-1", "reservation-1", "",
            BudgetDisposition.CONSUMED, 1, "evidence-1", "USAGE_REPORTED",
        )
        proof = self.authority.issue_settlement_proof("proof-1", request)
        altered = BudgetSettlementRequest(
            **{**request.__dict__, "actual_units": 2}
        )

        with self.assertRaisesRegex(DispatchDenied, "was not issued here"):
            self.authority.verify_settlement_proof(proof, altered)

    def test_settlement_proof_binds_every_request_field_without_state_change(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        request = BudgetSettlementRequest(
            "settlement-1", "reservation-1", "",
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "evidence-1", "USAGE_UNKNOWN",
        )
        proof = self.authority.issue_settlement_proof("proof-1", request)
        mutations = {
            "settlement_event_id": "settlement-2",
            "reservation_id": "reservation-2",
            "expected_previous_hash": "predecessor-2",
            "disposition": BudgetDisposition.CONSUMED,
            "actual_units": 1,
            "evidence_digest": "evidence-2",
            "reason_code": "OTHER_REASON",
            "non_dispatch_proven": True,
            "zero_liability_proven": True,
            "release_slot": True,
            "all_obligations_settled": True,
            "additional_liability": True,
            "repository_id": "repo-2",
            "run_id": "run-2",
            "item_id": "item-2",
            "logical_effect_id": "effect-2",
            "attempt_id": "attempt-2",
            "nonexecution_seal_id": "nonexecution-seal-1",
        }
        connection = sqlite3.connect(self.database_path)
        try:
            unchanged = tuple(connection.iterdump())
        finally:
            connection.close()

        self.assertEqual(
            set(mutations), set(BudgetSettlementContract.__dataclass_fields__)
        )
        for field, value in mutations.items():
            with self.subTest(field=field), self.assertRaisesRegex(
                DispatchDenied, "was not issued here"
            ):
                self.store._settle_budget(
                    replace(request, **{field: value}), proof, self.authority
                )
            connection = sqlite3.connect(self.database_path)
            try:
                after_denial = tuple(connection.iterdump())
            finally:
                connection.close()
            self.assertEqual(after_denial, unchanged)

    def test_settlement_rejects_non_boolean_control_flags_before_state_change(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        request = BudgetSettlementRequest(
            "settlement-1", "reservation-1", "",
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "evidence-1", "USAGE_UNKNOWN",
        )
        connection = sqlite3.connect(self.database_path)
        try:
            unchanged = tuple(connection.iterdump())
        finally:
            connection.close()

        for field in (
            "non_dispatch_proven",
            "zero_liability_proven",
            "release_slot",
            "all_obligations_settled",
            "additional_liability",
        ):
            malformed = replace(request, **{field: "false"})
            with self.subTest(field=field), self.assertRaisesRegex(
                ValueError, "must be booleans"
            ):
                self.store._settle_budget(
                    malformed,
                    SyntheticSettlementProof(
                        "proof", "reservation-1", False, False, False,
                        "digest", "mac",
                    ),
                    self.authority,
                )
            connection = sqlite3.connect(self.database_path)
            try:
                after_denial = tuple(connection.iterdump())
            finally:
                connection.close()
            self.assertEqual(after_denial, unchanged)

    def test_f04_release_requires_both_proofs_and_releases_slot_once(self) -> None:
        committed = self._commit_planned_intent(self.request(), self.capability, self.authority, expected_head="", writer_epoch=1)
        self.oracle.allowed_head = committed.event_hash
        incomplete = BudgetSettlementRequest(
            settlement_event_id="settlement-1",
            reservation_id="reservation-1",
            expected_previous_hash="",
            disposition=BudgetDisposition.RELEASED,
            actual_units=None,
            evidence_digest="proof-1",
            reason_code="NONDISPATCH",
            non_dispatch_proven=True,
            zero_liability_proven=False,
            release_slot=True,
            all_obligations_settled=True,
        )
        with self.assertRaisesRegex(DispatchDenied, "zero-liability"):
            proof = self.authority.issue_settlement_proof(
                "proof-incomplete",
                incomplete,
            )
            self.store._settle_budget(incomplete, proof, self.authority)

        attacker = SyntheticAuthority(b"x" * 32)
        reopened = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        )
        forged_release = replace(incomplete, zero_liability_proven=True)
        forged_proof = attacker.issue_settlement_proof(
            "attacker-proof", forged_release
        )
        connection = sqlite3.connect(self.database_path)
        try:
            before_forged_release = tuple(connection.iterdump())
        finally:
            connection.close()
        with self.assertRaisesRegex(DispatchDenied, "accepted plan"):
            reopened._settle_budget(
                forged_release, forged_proof, attacker
            )
        connection = sqlite3.connect(self.database_path)
        try:
            after_forged_release = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_forged_release, before_forged_release)

        rebound = replace(incomplete, item_id="item-2")
        with self.assertRaisesRegex(DispatchDenied, "was not issued here"):
            self.authority.verify_settlement_proof(proof, rebound)

        complete = BudgetSettlementRequest(
            **{**incomplete.__dict__, "zero_liability_proven": True}
        )
        proof = self.authority.issue_settlement_proof(
            "proof-complete",
            complete,
        )
        receipt = reopened._settle_budget(complete, proof, self.authority)
        self.oracle.allowed_head = receipt.settlement_hash
        replay = self.store._settle_budget(complete, proof, self.authority)
        self.assertTrue(receipt.slot_released)
        self.assertTrue(replay.replayed)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.assertEqual(self.store.load_run_lifecycle("run-1"), LifecycleState.BLOCKED)
        recovered = SQLiteStateStore(self.database_path, self.oracle, "repo-1")
        recovered._bind_classification_authority(self.authority)
        recovered.load_verified("repo-1")
        self.assertEqual(
            recovered.load_run_lifecycle("run-1"), LifecycleState.BLOCKED
        )

    def test_restart_rejects_replacement_issuer_before_settlement_or_replay(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        attacker = SyntheticAuthority(b"x" * 32)
        reopened = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        )

        connection = sqlite3.connect(self.database_path)
        try:
            before_bind = tuple(connection.iterdump())
        finally:
            connection.close()
        with self.assertRaisesRegex(DispatchDenied, "accepted plan"):
            reopened._bind_classification_authority(attacker)
        connection = sqlite3.connect(self.database_path)
        try:
            after_bind = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_bind, before_bind)

        receipt = EffectObservationRequest(
            "attacker-observation", "attacker-observe-command",
            "attacker-observation-event", "repo-1", "run-1", "item-1",
            "effect-1", "attempt-1", "attacker-receipt",
            self.capability.claim_id, "descriptor-digest", 2,
            "attacker-settlement", "",
        )
        with self.assertRaisesRegex(DispatchDenied, "authority is not bound"):
            reopened._record_effect_observation(receipt)
        connection = sqlite3.connect(self.database_path)
        try:
            after_receipt = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_receipt, before_bind)

        settlement_request = BudgetSettlementRequest(
            "settlement-1", "reservation-1", "",
            BudgetDisposition.CONSUMED, 2, "receipt-1", "USAGE_REPORTED",
        )
        settlement = self.store._settle_budget(
            settlement_request,
            self.authority.issue_settlement_proof(
                "proof-1", settlement_request
            ),
            self.authority,
        )
        self.oracle.allowed_head = settlement.settlement_hash
        connection = sqlite3.connect(self.database_path)
        try:
            before_replay = tuple(connection.iterdump())
        finally:
            connection.close()
        with self.assertRaisesRegex(DispatchDenied, "accepted plan"):
            reopened._settle_budget(
                settlement_request,
                attacker.issue_settlement_proof(
                    "attacker-replay-proof", settlement_request
                ),
                attacker,
            )
        connection = sqlite3.connect(self.database_path)
        try:
            after_replay = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_replay, before_replay)

    def test_known_usage_cannot_be_rewritten_as_release_or_unknown(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        consumed = BudgetSettlementRequest(
            "settlement-1", "reservation-1", "",
            BudgetDisposition.CONSUMED, 2, "receipt-1", "USAGE_REPORTED",
        )
        consumed_receipt = self.store._settle_budget(
            consumed,
            self.authority.issue_settlement_proof("proof-1", consumed),
            self.authority,
        )
        self.oracle.allowed_head = consumed_receipt.settlement_hash

        for disposition, actual_units in (
            (BudgetDisposition.RELEASED, None),
            (BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None),
        ):
            request = BudgetSettlementRequest(
                f"settlement-{disposition.value}", "reservation-1",
                consumed_receipt.settlement_hash, disposition, actual_units,
                "contradictory-evidence", "CONTRADICTORY_SETTLEMENT",
                non_dispatch_proven=disposition is BudgetDisposition.RELEASED,
                zero_liability_proven=disposition is BudgetDisposition.RELEASED,
            )
            proof = self.authority.issue_settlement_proof(
                f"proof-{disposition.value}", request
            )
            with self.subTest(disposition=disposition), self.assertRaisesRegex(
                DispatchDenied,
                "illegal budget settlement transition|cannot downgrade known usage",
            ):
                self.store._settle_budget(request, proof, self.authority)

        self.assertEqual(self.store.table_counts()["budget_settlements"], 1)
        self.assertEqual(self.store.table_counts()["dispatch_fences"], 0)

    def test_additional_unknown_liability_preserves_known_charge_and_fences(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        consumed = BudgetSettlementRequest(
            "settlement-1", "reservation-1", "",
            BudgetDisposition.CONSUMED, 2, "receipt-1", "USAGE_REPORTED",
        )
        consumed_receipt = self.store._settle_budget(
            consumed,
            self.authority.issue_settlement_proof("proof-1", consumed),
            self.authority,
        )
        self.oracle.allowed_head = consumed_receipt.settlement_hash
        additional = BudgetSettlementRequest(
            "settlement-2", "reservation-1",
            consumed_receipt.settlement_hash,
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "additional-exposure-1", "ADDITIONAL_LIABILITY_UNKNOWN",
            additional_liability=True,
        )

        under_bound = replace(additional, additional_liability=False)
        under_bound_proof = self.authority.issue_settlement_proof(
            "proof-under-bound", under_bound
        )
        connection = sqlite3.connect(self.database_path)
        try:
            before_rebind = tuple(connection.iterdump())
        finally:
            connection.close()
        with self.assertRaisesRegex(DispatchDenied, "was not issued here"):
            self.store._settle_budget(
                additional, under_bound_proof, self.authority
            )
        connection = sqlite3.connect(self.database_path)
        try:
            after_rebind = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_rebind, before_rebind)

        receipt = self.store._settle_budget(
            additional,
            self.authority.issue_settlement_proof("proof-2", additional),
            self.authority,
        )
        self.oracle.allowed_head = receipt.settlement_hash

        self.assertEqual(receipt.charged_units, 7)
        self.assertTrue(receipt.uncertainty)
        self.assertEqual(self.store.table_counts()["dispatch_fences"], 1)
        self.store.load_verified("repo-1")

    def test_f05_recovery_requires_independent_current_head(self) -> None:
        oracle = MutableFreshnessOracle()
        database_path = Path(self.temporary_directory.name) / "freshness.sqlite3"
        store = SQLiteStateStore(database_path, oracle, "repo-1")
        authority = SyntheticAuthority()
        store._bind_classification_authority(authority)
        authority.register(SyntheticGrant("grant-2", "repo-1", "effect-1", "attempt-1", "scope-1"))
        capability = authority.claim("grant-2", "repo-1", "effect-1", "attempt-1", "scope-1")
        plan = store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        oracle.allowed_head = plan.event_hash
        committed = store.commit_intent(
            self.request(), capability, authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        with self.assertRaisesRegex(DispatchDenied, "freshness"):
            store.load_verified("repo-1")
        oracle.allowed_head = committed.event_hash
        catalog_head, run_heads = store.load_verified("repo-1")
        self.assertEqual(catalog_head, committed.event_hash)
        self.assertEqual(run_heads, {"run-1": committed.event_hash})

    def test_database_rejects_another_repository_identity(self) -> None:
        database_path = Path(self.temporary_directory.name) / "bound.sqlite3"
        SQLiteStateStore(database_path, MutableFreshnessOracle(), "repo-1")
        with self.assertRaisesRegex(Exception, "another repository"):
            SQLiteStateStore(database_path, MutableFreshnessOracle(), "repo-2")

    def test_recovery_rejects_deleted_slot_projection(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = committed.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute("DELETE FROM outstanding_slot")
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(Exception, "slot projection"):
            self.store.load_verified("repo-1")

    def test_recovery_rejects_tampered_run_head_sequence(self) -> None:
        receipt = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = receipt.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE runs SET head_sequence = head_sequence + 1 "
                "WHERE run_id = 'run-1'"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(StorageIntegrityError, "head sequence"):
            self.store.load_verified("repo-1")

    def test_recovery_rejects_tampered_slot_run_and_generation(self) -> None:
        for column, value in (
            ("run_id", "other-run"),
            ("logical_effect_id", "other-effect"),
            ("attempt_id", "other-attempt"),
            ("generation", 2),
        ):
            with self.subTest(column=column):
                self.oracle.allowed_head = ""
                test_path = (
                    Path(self.temporary_directory.name) / f"slot-{column}.sqlite3"
                )
                store = SQLiteStateStore(test_path, self.oracle, "repo-1")
                authority = SyntheticAuthority()
                store._bind_classification_authority(authority)
                grant = SyntheticGrant(
                    f"grant-{column}", "repo-1", "effect-1", "attempt-1",
                    "scope-1",
                )
                authority.register(grant)
                capability = authority.claim(*grant.__dict__.values())
                plan = store.accept_plan(
                    PlanAcceptanceRequest(
                        "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                        "run-1", "item-1", "effect-1", "revision-1",
                        "descriptor-digest", "scope-1", "budget-policy-digest",
                        ("check-1",),
                    ),
                    expected_head="", writer_epoch=1,
                )
                self.oracle.allowed_head = plan.event_hash
                receipt = store.commit_intent(
                    self.request(), capability, authority,
                    expected_head=plan.event_hash, writer_epoch=2,
                )
                self.oracle.allowed_head = receipt.event_hash
                connection = sqlite3.connect(test_path)
                try:
                    connection.execute(
                        f"UPDATE outstanding_slot SET {column} = ?", (value,)
                    )
                    connection.commit()
                finally:
                    connection.close()
                with self.assertRaisesRegex(StorageIntegrityError, "slot projection"):
                    store.load_verified("repo-1")

    def test_recovery_rejects_tampered_command_and_redemption_projections(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = committed.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE command_outcomes SET event_hash = 'forged' WHERE command_id = 'command-1'"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(Exception, "command-outcome projection"):
            self.store.load_verified("repo-1")

        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = 'command-1'",
                (committed.event_hash,),
            )
            connection.execute("DELETE FROM capability_redemptions")
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(Exception, "capability-redemption projection"):
            self.store.load_verified("repo-1")

    def test_recovery_rejects_tampered_lifecycle_projection(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = committed.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE runs SET lifecycle_state = 'PLANNED' WHERE run_id = 'run-1'"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(Exception, "lifecycle projection"):
            self.store.load_verified("repo-1")

    def test_recovery_reconstructs_settlement_accounting_and_fences(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = committed.event_hash
        settlement = BudgetSettlementRequest(
            settlement_event_id="settlement-1",
            reservation_id="reservation-1",
            expected_previous_hash="",
            disposition=BudgetDisposition.CONSUMED,
            actual_units=11,
            evidence_digest="usage-evidence",
            reason_code="USAGE_REPORTED",
        )
        proof = self.authority.issue_settlement_proof(
            "proof-1",
            settlement,
        )
        self.store._settle_budget(settlement, proof, self.authority)

        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE budget_reservations SET charged_units = 1 WHERE reservation_id = 'reservation-1'"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(Exception, "accounting projection"):
            self.store.load_verified("repo-1")

        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE budget_reservations SET charged_units = 11 WHERE reservation_id = 'reservation-1'"
            )
            connection.execute("DELETE FROM dispatch_fences")
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(Exception, "dispatch-fence projection"):
            self.store.load_verified("repo-1")

    def test_settlement_requires_verified_fresh_state(self) -> None:
        self._commit_planned_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        request = BudgetSettlementRequest(
            "settlement-1",
            "reservation-1",
            "",
            BudgetDisposition.CONSUMED,
            1,
            "usage-evidence",
            "USAGE_REPORTED",
        )
        proof = self.authority.issue_settlement_proof(
            "proof-1",
            request,
        )
        with self.assertRaisesRegex(DispatchDenied, "freshness"):
            self.store._settle_budget(request, proof, self.authority)
        self.assertEqual(self.store.table_counts()["budget_settlements"], 0)

    def test_c09_failure_before_settlement_commit_preserves_reservation_and_slot(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = committed.event_hash
        request = BudgetSettlementRequest(
            "settlement-1",
            "reservation-1",
            "",
            BudgetDisposition.RELEASED,
            None,
            "usage-evidence",
            "NONDISPATCH_PROVEN",
            non_dispatch_proven=True,
            zero_liability_proven=True,
            release_slot=True,
            all_obligations_settled=True,
        )
        proof = self.authority.issue_settlement_proof(
            "proof-1",
            request,
        )

        with self.assertRaises(InjectedFailure):
            self.store._settle_budget(
                request,
                proof,
                self.authority,
                failure_hook=raise_at("after_settlement_writes_before_commit"),
            )

        self.assertEqual(self.store.table_counts()["budget_settlements"], 0)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        catalog_head, run_heads = self.store.load_verified("repo-1")
        self.assertEqual(catalog_head, committed.event_hash)
        self.assertEqual(run_heads, {"run-1": committed.event_hash})

        receipt = self.store._settle_budget(request, proof, self.authority)
        self.oracle.allowed_head = receipt.settlement_hash
        self.assertFalse(receipt.replayed)
        self.assertEqual(receipt.held_units, 0)
        self.assertEqual(receipt.charged_units, 0)
        self.assertFalse(receipt.uncertainty)
        self.assertTrue(receipt.slot_released)
        self.assertEqual(self.store.table_counts()["events"], 3)
        self.assertEqual(self.store.table_counts()["budget_reservations"], 1)
        self.assertEqual(self.store.table_counts()["budget_settlements"], 1)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.store.load_verified("repo-1")

    def test_c09_failure_after_settlement_commit_replays_without_duplicate_release(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = committed.event_hash
        request = BudgetSettlementRequest(
            "settlement-1",
            "reservation-1",
            "",
            BudgetDisposition.RELEASED,
            None,
            "usage-evidence",
            "NONDISPATCH_PROVEN",
            non_dispatch_proven=True,
            zero_liability_proven=True,
            release_slot=True,
            all_obligations_settled=True,
        )
        proof = self.authority.issue_settlement_proof(
            "proof-1",
            request,
        )

        with self.assertRaises(InjectedFailure):
            self.store._settle_budget(
                request,
                proof,
                self.authority,
                failure_hook=raise_at(
                    "after_settlement_commit_before_acknowledgement"
                ),
            )

        connection = sqlite3.connect(self.database_path)
        try:
            settlement_hash = connection.execute(
                "SELECT settlement_hash FROM budget_settlements WHERE settlement_event_id = 'settlement-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = settlement_hash
        replay = self.store._settle_budget(request, proof, self.authority)

        self.assertTrue(replay.replayed)
        self.assertEqual(replay.settlement_hash, settlement_hash)
        self.assertEqual(replay.held_units, 0)
        self.assertEqual(replay.charged_units, 0)
        self.assertFalse(replay.uncertainty)
        self.assertTrue(replay.slot_released)
        connection = sqlite3.connect(self.database_path)
        try:
            reservation = connection.execute(
                "SELECT held_units, charged_units, uncertainty FROM budget_reservations WHERE reservation_id = 'reservation-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(reservation, (0, 0, 0))
        self.assertEqual(self.store.table_counts()["events"], 3)
        self.assertEqual(self.store.table_counts()["budget_reservations"], 1)
        self.assertEqual(self.store.table_counts()["budget_settlements"], 1)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.store.load_verified("repo-1")

    def test_c04_observation_intake_survives_crash_without_duplicate_or_slot_release(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = committed.event_hash
        settlement_request = BudgetSettlementRequest(
            "settlement-1",
            "reservation-1",
            "",
            BudgetDisposition.CONSUMED,
            2,
            "receipt-1",
            "USAGE_REPORTED",
        )
        proof = self.authority.issue_settlement_proof(
            "proof-1",
            settlement_request,
        )
        settlement = self.store._settle_budget(
            settlement_request, proof, self.authority
        )
        self.oracle.allowed_head = settlement.settlement_hash
        observation = EffectObservationRequest(
            observation_id="observation-1",
            command_id="observe-command-1",
            event_id="observation-event-1",
            repository_id="repo-1",
            run_id="run-1",
            item_id="item-1",
            logical_effect_id="effect-1",
            attempt_id="attempt-1",
            source_receipt_id="receipt-1",
            source_claim_id=self.capability.claim_id,
            payload_digest="descriptor-digest",
            usage_units=2,
            settlement_event_id="settlement-1",
            settlement_hash=settlement.settlement_hash,
        )

        with self.assertRaises(InjectedFailure):
            self.store._record_effect_observation(
                observation,
                failure_hook=raise_at("after_observation_writes_before_commit"),
            )
        self.assertEqual(self.store.table_counts()["effect_observations"], 0)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        with self.assertRaises(InjectedFailure):
            self.store._record_effect_observation(
                observation,
                failure_hook=raise_at(
                    "after_observation_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            observation_hash = connection.execute(
                "SELECT event_hash FROM effect_observations WHERE observation_id = 'observation-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = observation_hash
        replay = self.store._record_effect_observation(observation)

        self.assertTrue(replay.replayed)
        self.assertEqual(replay.event_hash, observation_hash)
        self.assertEqual(replay.resulting_state.value, "VALIDATING")


    def test_t25_recovery_derives_lifecycle_instead_of_trusting_event(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        request = BudgetSettlementRequest(
            "settlement-1", "reservation-1", "",
            BudgetDisposition.RELEASED, None, "usage-evidence",
            "NONDISPATCH_PROVEN", non_dispatch_proven=True,
            zero_liability_proven=True, release_slot=True,
            all_obligations_settled=True,
        )
        receipt = self.store._settle_budget(
            request,
            self.authority.issue_settlement_proof("proof-1", request),
            self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM budget_settlements WHERE "
                    "settlement_event_id = 'settlement-1'"
                ).fetchone()["body_json"]
            )
            body["lifecycle_to"] = LifecycleState.COMPLETED.value
            body["continuation_cursor"] = None
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE budget_settlements SET settlement_hash = ?, "
                "body_json = ? WHERE settlement_event_id = 'settlement-1'",
                (event_hash, body_json),
            )
            connection.execute(
                "UPDATE budget_reservations SET settlement_head_hash = ? "
                "WHERE reservation_id = 'reservation-1'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                "event_id = 'settlement-1'",
                (event_hash, body_json),
            )
            connection.execute(
                "UPDATE runs SET lifecycle_state = 'COMPLETED', "
                "continuation_cursor = NULL, head_hash = ? WHERE run_id = 'run-1'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE "
                "repository_id = 'repo-1'",
                (event_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(
            StorageIntegrityError, "T25 lifecycle semantics"
        ):
            self.store.load_verified("repo-1")

    def test_t25_historical_slot_requires_prior_exact_intent(self) -> None:
        self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            reservation = connection.execute(
                "SELECT * FROM budget_reservations WHERE reservation_id = ?",
                ("reservation-1",),
            ).fetchone()
            intent_sequence = connection.execute(
                "SELECT sequence FROM events WHERE event_kind = ?",
                ("INTENT_COMMITTED",),
            ).fetchone()["sequence"]
            self.assertFalse(
                self.store._operation_slot_current_before(
                    connection, reservation, int(intent_sequence)
                )
            )
            self.assertTrue(
                self.store._operation_slot_current_before(
                    connection, reservation, int(intent_sequence) + 1
                )
            )
            self.assertFalse(
                self.store._operation_slot_current_before(
                    connection, reservation, int(intent_sequence) + 1,
                    expected_generation=2,
                )
            )
        finally:
            connection.close()

    def test_historical_slot_ignores_release_fields_on_budget_event(self) -> None:
        self._record_effect_observation(check_ids=("check-1",))
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            settlement = connection.execute(
                "SELECT settlement_event_id, body_json FROM budget_settlements "
                "WHERE reservation_id = ?",
                ("reservation-1",),
            ).fetchone()
            body = json.loads(settlement["body_json"])
            body.update(
                {
                    "slot_released": True,
                    "slot_attempt_id": "attempt-1",
                    "slot_generation": 1,
                }
            )
            connection.execute(
                "UPDATE events SET body_json = ? WHERE event_id = ?",
                (
                    json.dumps(body, sort_keys=True, separators=(",", ":")),
                    settlement["settlement_event_id"],
                ),
            )
            reservation = connection.execute(
                "SELECT * FROM budget_reservations WHERE reservation_id = ?",
                ("reservation-1",),
            ).fetchone()
            self.assertTrue(
                self.store._operation_slot_current_before(
                    connection, reservation, 100
                )
            )
        finally:
            connection.close()

    def test_recovery_rejects_settlement_moved_to_another_run(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        settlement_request = BudgetSettlementRequest(
            "settlement-1", "reservation-1", "",
            BudgetDisposition.CONSUMED, 2, "usage-evidence", "USAGE_REPORTED",
        )
        settlement = self.store._settle_budget(
            settlement_request,
            self.authority.issue_settlement_proof(
                "settlement-proof-1", settlement_request
            ),
            self.authority,
        )
        self.oracle.allowed_head = settlement.settlement_hash
        second_plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-2", "plan-command-2", "plan-event-2", "repo-1",
                "run-2", "item-2", "effect-2", "revision-2",
                "descriptor-2", "scope-2", "budget-policy-2", ("check-2",),
            ),
            expected_head=settlement.settlement_hash,
            writer_epoch=4,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM budget_settlements WHERE "
                    "settlement_event_id = ?",
                    ("settlement-1",),
                ).fetchone()[0]
            )
            body.update(
                {
                    "run_id": "run-2",
                    "item_id": "item-2",
                    "sequence": 2,
                    "previous_event_hash": second_plan.event_hash,
                }
            )
            payload_keys = (
                "actual_units", "additional_liability",
                "all_obligations_settled", "disposition", "evidence_digest",
                "expected_previous_hash", "non_dispatch_proven", "reason_code",
                "release_slot", "reservation_id", "settlement_event_id",
                "zero_liability_proven", "repository_id", "run_id", "item_id",
                "logical_effect_id", "attempt_id", "nonexecution_seal_id",
                "settlement_binding_version",
            )
            payload_digest = self.store._event_hash(
                {key: body[key] for key in payload_keys}
            )
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE budget_settlements SET settlement_hash = ?, "
                "payload_digest = ?, body_json = ? WHERE settlement_event_id = ?",
                (event_hash, payload_digest, body_json, "settlement-1"),
            )
            connection.execute(
                "UPDATE budget_reservations SET settlement_head_hash = ? "
                "WHERE reservation_id = ?",
                (event_hash, "reservation-1"),
            )
            connection.execute(
                "UPDATE events SET run_id = ?, item_id = ?, sequence = 2, "
                "previous_event_hash = ?, event_hash = ?, body_json = ? "
                "WHERE event_id = ?",
                (
                    "run-2", "item-2", second_plan.event_hash, event_hash,
                    body_json, "settlement-1",
                ),
            )
            connection.execute(
                "UPDATE runs SET head_sequence = 2, head_hash = ? WHERE run_id = ?",
                (event_hash, "run-2"),
            )
            connection.execute(
                "UPDATE runs SET head_sequence = 2, head_hash = ? WHERE run_id = ?",
                (committed.event_hash, "run-1"),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, "repo-1"),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(
            StorageIntegrityError,
            "writer epoch|settlement scope binding",
        ):
            self.store.load_verified("repo-1")

    def test_recovery_rejects_surplus_settlement_key(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        settlement_request = BudgetSettlementRequest(
            "surplus-settlement", "reservation-1", "",
            BudgetDisposition.CONSUMED, 2, "usage-evidence", "USAGE_REPORTED",
        )
        settlement = self.store._settle_budget(
            settlement_request,
            self.authority.issue_settlement_proof(
                "surplus-settlement-proof", settlement_request
            ),
            self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM budget_settlements WHERE "
                    "settlement_event_id = ?",
                    ("surplus-settlement",),
                ).fetchone()[0]
            )
            body["surplus_authority_claim"] = True
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE budget_settlements SET settlement_hash = ?, "
                "body_json = ? WHERE settlement_event_id = ?",
                (event_hash, body_json, "surplus-settlement"),
            )
            connection.execute(
                "UPDATE budget_reservations SET settlement_head_hash = ? "
                "WHERE reservation_id = ?",
                (event_hash, "reservation-1"),
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (event_hash, body_json, "surplus-settlement"),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = ?",
                (event_hash, "run-1"),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, "repo-1"),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(StorageIntegrityError, "settlement schema"):
            self.store.load_verified("repo-1")

    def test_recovery_rejects_settlement_bool_for_integer(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        settlement_request = BudgetSettlementRequest(
            "typed-settlement", "reservation-1", "",
            BudgetDisposition.CONSUMED, 0, "usage-evidence", "USAGE_REPORTED",
        )
        settlement = self.store._settle_budget(
            settlement_request,
            self.authority.issue_settlement_proof(
                "typed-settlement-proof", settlement_request
            ),
            self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM budget_settlements WHERE "
                    "settlement_event_id = ?",
                    ("typed-settlement",),
                ).fetchone()[0]
            )
            body["charged_units"] = False
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE budget_settlements SET settlement_hash = ?, "
                "body_json = ? WHERE settlement_event_id = ?",
                (event_hash, body_json, "typed-settlement"),
            )
            connection.execute(
                "UPDATE budget_reservations SET settlement_head_hash = ? "
                "WHERE reservation_id = ?",
                (event_hash, "reservation-1"),
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (event_hash, body_json, "typed-settlement"),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = ?",
                (event_hash, "run-1"),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, "repo-1"),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(StorageIntegrityError, "settlement schema"):
            self.store.load_verified("repo-1")

    def test_recovery_rejects_ordinary_receipt_slot_release_forgery(self) -> None:
        recorded = self._record_effect_observation(check_ids=("check-1",))
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    (recorded.event_id,),
                ).fetchone()[0]
            )
            self.assertFalse(body["slot_released"])
            body["slot_released"] = True
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (event_hash, body_json, recorded.event_id),
            )
            connection.execute(
                "UPDATE effect_observations SET event_hash = ?, body_json = ? "
                "WHERE observation_id = ?",
                (event_hash, body_json, recorded.observation_id),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                (event_hash, recorded.command_id),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = ?",
                (event_hash, "run-1"),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, "repo-1"),
            )
            connection.execute("DELETE FROM outstanding_slot")
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(
            StorageIntegrityError, "effect observation semantics"
        ):
            self.store.load_verified("repo-1")

    def test_observation_requests_reject_boolean_usage(self) -> None:
        with self.assertRaisesRegex(ValueError, "usage"):
            EffectObservationRequest(
                "observation-bool", "observe-command-bool",
                "observation-event-bool", "repo-1", "run-1", "item-1",
                "effect-1", "attempt-1", "receipt-bool", "claim-bool",
                "descriptor-digest", True, "settlement-bool", "",
            ).validate()
        with self.assertRaisesRegex(ValueError, "usage"):
            ValidatorObservationRequest(
                "validator-observation-bool", "validator-command-bool",
                "validator-event-bool", "repo-1", "run-1", "item-1",
                "effect-1", "validator-intent-bool",
                "validator-attempt-bool", "validator-result-bool",
                "claim-bool", "revision-1", "check-1", "input-1",
                "result-bool", "PASS", True, "validator-settlement-bool",
                "validator-settlement-hash-bool",
            ).validate()

    def test_c04_unknown_receipt_usage_is_recorded_for_reconciliation(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = committed.event_hash
        settlement_request = BudgetSettlementRequest(
            "settlement-1", "reservation-1", "",
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "receipt-unknown-1", "USAGE_UNKNOWN",
        )
        proof = self.authority.issue_settlement_proof(
            "proof-1", settlement_request
        )
        settlement = self.store._settle_budget(
            settlement_request,
            proof,
            self.authority,
        )
        self.oracle.allowed_head = settlement.settlement_hash

        recorded = self.store._record_effect_observation(
            EffectObservationRequest(
                "observation-unknown-1", "observe-unknown-command-1",
                "observation-unknown-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "attempt-1", "receipt-unknown-1",
                self.capability.claim_id, "descriptor-digest", None,
                "settlement-1", settlement.settlement_hash,
            )
        )
        self.oracle.allowed_head = recorded.event_hash

        self.assertEqual(recorded.resulting_state.value, "RECONCILIATION_REQUIRED")
        self.assertEqual(self.store.table_counts()["effect_observations"], 1)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

        release = BudgetSettlementRequest(
            "settlement-release-1", "reservation-1",
            settlement.settlement_hash, BudgetDisposition.RELEASED, None,
            "non-dispatch-proof", "NONDISPATCH",
            non_dispatch_proven=True, zero_liability_proven=True,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            before_denial = tuple(connection.iterdump())
        finally:
            connection.close()
        with self.assertRaisesRegex(
            DispatchDenied, "cannot release liability"
        ):
            self.store._settle_budget(
                release,
                self.authority.issue_settlement_proof(
                    "proof-release-1", release
                ),
                self.authority,
            )
        connection = sqlite3.connect(self.database_path)
        try:
            after_denial = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_denial, before_denial)

    def test_c04_conflicting_durable_identities_fail_closed(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        base = EffectObservationRequest(
            "observation-1", "observe-command-1", "observation-event-1",
            "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
            "receipt-1", self.capability.claim_id, "descriptor-digest", 2,
            "settlement-1", "",
        )
        recorded = self.store._record_effect_observation(base)
        self.assertFalse(recorded.replayed)
        self.oracle.allowed_head = recorded.event_hash
        for conflicting in (
            EffectObservationRequest(
                *(
                    "observation-1", "observe-command-2", "observation-event-2",
                    "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
                    "receipt-2", self.capability.claim_id, "descriptor-digest", 2,
                    "settlement-2", "",
                )
            ),
            EffectObservationRequest(
                *(
                    "observation-2", "observe-command-2", "event-1",
                    "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
                    "receipt-2", self.capability.claim_id, "descriptor-digest", 2,
                    "settlement-2", "",
                )
            ),
            EffectObservationRequest(
                *(
                    "observation-2", "observe-command-2", "observation-event-2",
                    "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
                    "receipt-2", self.capability.claim_id, "descriptor-digest", 2,
                    "event-1", "",
                )
            ),
        ):
            with self.subTest(conflicting=conflicting), self.assertRaises(
                StorageIntegrityError
            ):
                self.store._record_effect_observation(conflicting)
            self.assertEqual(self.store.table_counts()["budget_settlements"], 1)
            self.assertEqual(self.store.table_counts()["effect_observations"], 1)

    def test_c04_recovery_rejects_tampered_observation_projection(self) -> None:
        observation = self._record_effect_observation(check_ids=("check-1",))
        self.oracle.allowed_head = observation.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE effect_observations SET source_claim_id = 'tampered' "
                "WHERE observation_id = 'observation-1'"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(
            StorageIntegrityError, "effect-observation projection"
        ):
            SQLiteStateStore(
                self.database_path, self.oracle, "repo-1"
            ).load_verified("repo-1")

    def _record_effect_observation(
        self,
        check_ids=("check-1", "check-2"),
        aggregate_gate_ids=None,
    ):
        if aggregate_gate_ids is None:
            aggregate_gate_ids = check_ids
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                check_ids, aggregate_gate_ids,
            ),
            expected_head="",
            writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        committed = self.store.commit_intent(
            self.request(), self.capability, self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        self.oracle.allowed_head = committed.event_hash
        settlement_request = BudgetSettlementRequest(
            "settlement-1",
            "reservation-1",
            "",
            BudgetDisposition.CONSUMED,
            2,
            "receipt-1",
            "USAGE_REPORTED",
        )
        proof = self.authority.issue_settlement_proof(
            "proof-1",
            settlement_request,
        )
        settlement = self.store._settle_budget(
            settlement_request, proof, self.authority
        )
        self.oracle.allowed_head = settlement.settlement_hash
        receipt = self.store._record_effect_observation(
            EffectObservationRequest(
                "observation-1",
                "observe-command-1",
                "observation-event-1",
                "repo-1",
                "run-1",
                "item-1",
                "effect-1",
                "attempt-1",
                "receipt-1",
                self.capability.claim_id,
                "descriptor-digest",
                2,
                "settlement-1",
                settlement.settlement_hash,
            )
        )
        self.oracle.allowed_head = receipt.event_hash
        return receipt

    def test_t01_plan_acceptance_replays_and_rejects_empty_or_tampered_checks(self) -> None:
        request = PlanAcceptanceRequest(
            "plan-1", "plan-command-1", "plan-event-1", "repo-1", "run-1",
            "item-1", "effect-1", "revision-1", "descriptor-digest",
            "scope-1", "budget-policy-digest", ("check-2", "check-1"),
        )
        first = self.store.accept_plan(
            request, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = first.event_hash
        replay = self.store.accept_plan(
            request, expected_head=first.event_hash, writer_epoch=2
        )
        self.assertTrue(replay.replayed)
        with self.assertRaisesRegex(ValueError, "at least one"):
            self.store.accept_plan(
                PlanAcceptanceRequest(
                    "plan-2", "plan-command-2", "plan-event-2", "repo-1",
                    "run-2", "item-2", "effect-2", "revision-2",
                    "descriptor-2", "scope-2", "budget-2", (),
                ),
                expected_head=first.event_hash,
                writer_epoch=2,
            )
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "DELETE FROM validation_requirements WHERE plan_id = 'plan-1' AND check_id = 'check-2'"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(StorageIntegrityError, "validation-requirement"):
            self.store.load_verified("repo-1")

    def test_t01_plan_acceptance_is_atomic_across_acknowledgement_loss(self) -> None:
        request = PlanAcceptanceRequest(
            "plan-1", "plan-command-1", "plan-event-1", "repo-1", "run-1",
            "item-1", "effect-1", "revision-1", "descriptor-digest",
            "scope-1", "budget-policy-digest", ("check-1",),
        )
        with self.assertRaises(InjectedFailure):
            self.store.accept_plan(
                request,
                expected_head="",
                writer_epoch=1,
                failure_hook=raise_at("after_plan_writes_before_commit"),
            )
        self.assertEqual(self.store.table_counts()["validation_plans"], 0)
        with self.assertRaises(InjectedFailure):
            self.store.accept_plan(
                request,
                expected_head="",
                writer_epoch=1,
                failure_hook=raise_at("after_plan_commit_before_acknowledgement"),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            event_hash = connection.execute(
                "SELECT event_hash FROM validation_plans WHERE plan_id = 'plan-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash
        replay = self.store.accept_plan(
            request, expected_head=event_hash, writer_epoch=2
        )
        self.assertTrue(replay.replayed)
        self.store.load_verified("repo-1")

    def test_t01_recovery_rejects_self_consistent_terminal_entry(self) -> None:
        accepted = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="",
            writer_epoch=1,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    ("plan-event-1",),
                ).fetchone()[0]
            )
            body["lifecycle_to"] = LifecycleState.COMPLETED.value
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (event_hash, body_json, "plan-event-1"),
            )
            connection.execute(
                "UPDATE validation_plans SET event_hash = ?, body_json = ? "
                "WHERE plan_id = ?",
                (event_hash, body_json, "plan-1"),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                (event_hash, "plan-command-1"),
            )
            connection.execute(
                "UPDATE runs SET lifecycle_state = ?, head_hash = ? WHERE run_id = ?",
                (LifecycleState.COMPLETED.value, event_hash, "run-1"),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, "repo-1"),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(StorageIntegrityError, "lifecycle route"):
            self.store.load_verified("repo-1")

    def test_t01_recovery_rejects_missing_lifecycle_key(self) -> None:
        self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="",
            writer_epoch=1,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    ("plan-event-1",),
                ).fetchone()[0]
            )
            del body["lifecycle_from"]
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (event_hash, body_json, "plan-event-1"),
            )
            connection.execute(
                "UPDATE validation_plans SET event_hash = ?, body_json = ? "
                "WHERE plan_id = ?",
                (event_hash, body_json, "plan-1"),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                (event_hash, "plan-command-1"),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = ?",
                (event_hash, "run-1"),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, "repo-1"),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(StorageIntegrityError, "lifecycle schema"):
            self.store.load_verified("repo-1")

    def test_t02_readiness_is_atomic_replay_safe_and_reversible(self) -> None:
        accepted = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = accepted.event_hash
        blocked_request = ReadinessEvaluationRequest(
            "readiness-1", "readiness-command-1", "readiness-event-1",
            "repo-1", "run-1", "item-1", "plan-1", "revision-1",
            accepted.event_hash, None, "inputs-evidence-1", False,
        )
        with self.assertRaises(InjectedFailure):
            self.store.evaluate_readiness(
                blocked_request,
                failure_hook=raise_at("after_readiness_writes_before_commit"),
            )
        self.assertEqual(self.store.table_counts()["readiness_evaluations"], 0)
        blocked = self.store.evaluate_readiness(blocked_request)
        self.oracle.allowed_head = blocked.event_hash
        self.assertEqual(blocked.resulting_state, LifecycleState.BLOCKED)
        replay = self.store.evaluate_readiness(blocked_request)
        self.assertTrue(replay.replayed)
        ready_request = ReadinessEvaluationRequest(
            "readiness-2", "readiness-command-2", "readiness-event-2",
            "repo-1", "run-1", "item-1", "plan-1", "revision-1",
            blocked.event_hash, None, "inputs-evidence-2", True,
        )
        ready = self.store.evaluate_readiness(ready_request)
        self.oracle.allowed_head = ready.event_hash
        self.assertEqual(ready.resulting_state, LifecycleState.PLANNED)
        self.store.load_verified("repo-1")

    def test_t02_cannot_clear_t16_recovery_blocker(self) -> None:
        _, failed = self._prepare_recoverable_application()
        request = ReadinessEvaluationRequest(
            "readiness-1", "readiness-command-1", "readiness-event-1",
            "repo-1", "run-1", "item-1", "plan-1", "revision-1",
            failed.event_hash, LifecycleState.VALIDATING.value,
            "inputs-evidence-1", True,
        )
        evaluated = self.store.evaluate_readiness(request)
        self.oracle.allowed_head = evaluated.event_hash

        self.assertEqual(evaluated.resulting_state, LifecycleState.BLOCKED)
        connection = sqlite3.connect(self.database_path)
        try:
            state, cursor = connection.execute(
                "SELECT lifecycle_state, continuation_cursor FROM runs "
                "WHERE run_id = 'run-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(state, LifecycleState.BLOCKED.value)
        self.assertEqual(cursor, LifecycleState.VALIDATING.value)
        self.store.load_verified("repo-1")

    def test_t02_unknown_cursor_fails_closed_before_append(self) -> None:
        accepted = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = accepted.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE runs SET lifecycle_state = 'BLOCKED', "
                "continuation_cursor = 'unknown:obligation' WHERE run_id = 'run-1'"
            )
            connection.commit()
        finally:
            connection.close()

        with self.assertRaisesRegex(StorageIntegrityError, "lifecycle|cursor"):
            self.store.evaluate_readiness(
                ReadinessEvaluationRequest(
                    "readiness-1", "readiness-command-1", "readiness-event-1",
                    "repo-1", "run-1", "item-1", "plan-1", "revision-1",
                    accepted.event_hash, "unknown:obligation",
                    "inputs-evidence-1", True,
                )
            )
        self.assertEqual(self.store.table_counts()["readiness_evaluations"], 0)

    def test_t02_repository_slot_in_another_run_blocks_readiness(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        accepted = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-2", "plan-command-2", "plan-event-2", "repo-1",
                "run-2", "item-2", "effect-2", "revision-2",
                "descriptor-2", "scope-2", "budget-policy-2", ("check-2",),
            ),
            expected_head=committed.event_hash, writer_epoch=3,
        )
        self.oracle.allowed_head = accepted.event_hash

        evaluated = self.store.evaluate_readiness(
            ReadinessEvaluationRequest(
                "readiness-2", "readiness-command-2", "readiness-event-2",
                "repo-1", "run-2", "item-2", "plan-2", "revision-2",
                accepted.event_hash, None, "inputs-evidence-2", True,
            )
        )

        self.assertEqual(evaluated.resulting_state, LifecycleState.BLOCKED)
        connection = sqlite3.connect(self.database_path)
        try:
            blocker_codes = json.loads(
                connection.execute(
                    "SELECT body_json FROM readiness_evaluations WHERE "
                    "readiness_id = 'readiness-2'"
                ).fetchone()[0]
            )["blocker_codes"]
        finally:
            connection.close()
        self.assertIn("OPERATION_SLOT_OCCUPIED", blocker_codes)

    def test_t02_historical_cross_run_fence_survives_later_clearance(self) -> None:
        request, attestation = self._prepare_finalization()
        finalized = self.store._finalize_operation(
            request, attestation, self.authority
        )
        self.oracle.allowed_head = finalized.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            previous_hash = connection.execute(
                "SELECT settlement_head_hash FROM budget_reservations "
                "WHERE reservation_id = 'reservation-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        unknown = BudgetSettlementRequest(
            "late-unknown", "reservation-1", previous_hash,
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "late-unknown-evidence", "ADDITIONAL_LIABILITY_UNKNOWN",
            additional_liability=True,
        )
        unknown_receipt = self.store._settle_budget(
            unknown,
            self.authority.issue_settlement_proof("late-unknown-proof", unknown),
            self.authority,
        )
        self.oracle.allowed_head = unknown_receipt.settlement_hash
        accepted = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-2", "plan-command-2", "plan-event-2", "repo-1",
                "run-2", "item-2", "effect-2", "revision-2",
                "descriptor-2", "scope-2", "budget-policy-2", ("check-2",),
            ),
            expected_head=unknown_receipt.settlement_hash, writer_epoch=100,
        )
        self.oracle.allowed_head = accepted.event_hash
        evaluated = self.store.evaluate_readiness(
            ReadinessEvaluationRequest(
                "readiness-2", "readiness-command-2", "readiness-event-2",
                "repo-1", "run-2", "item-2", "plan-2", "revision-2",
                accepted.event_hash, None, "inputs-evidence-2", True,
            )
        )
        self.assertEqual(evaluated.resulting_state, LifecycleState.BLOCKED)

        self.oracle.allowed_head = evaluated.event_hash
        correction = BudgetSettlementRequest(
            "late-correction", "reservation-1",
            unknown_receipt.settlement_hash, BudgetDisposition.ADJUSTED, 3,
            "late-authoritative-evidence", "AUTHORITATIVE_CORRECTION",
        )
        corrected = self.store._settle_budget(
            correction,
            self.authority.issue_settlement_proof(
                "late-correction-proof", correction
            ),
            self.authority,
        )
        self.oracle.allowed_head = corrected.settlement_hash
        self.assertEqual(self.store.table_counts()["dispatch_fences"], 0)
        self.store.load_verified("repo-1")

    def test_t02_missing_slot_reservation_fails_closed(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        accepted = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-2", "plan-command-2", "plan-event-2", "repo-1",
                "run-2", "item-2", "effect-2", "revision-2",
                "descriptor-2", "scope-2", "budget-policy-2", ("check-2",),
            ),
            expected_head=committed.event_hash, writer_epoch=3,
        )
        self.oracle.allowed_head = accepted.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "DELETE FROM budget_reservations WHERE reservation_id = "
                "'reservation-1'"
            )
            connection.commit()
        finally:
            connection.close()

        with self.assertRaisesRegex(StorageIntegrityError, "budget projection"):
            self.store.evaluate_readiness(
                ReadinessEvaluationRequest(
                    "readiness-2", "readiness-command-2", "readiness-event-2",
                    "repo-1", "run-2", "item-2", "plan-2", "revision-2",
                    accepted.event_hash, None, "inputs-evidence-2", True,
                )
            )
        self.assertEqual(self.store.table_counts()["readiness_evaluations"], 0)

    def test_repository_writer_epoch_must_advance(self) -> None:
        accepted = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = accepted.event_hash
        with self.assertRaisesRegex(DispatchDenied, "writer epoch"):
            self.store.accept_plan(
                PlanAcceptanceRequest(
                    "plan-2", "plan-command-2", "plan-event-2", "repo-1",
                    "run-2", "item-2", "effect-2", "revision-2",
                    "descriptor-2", "scope-2", "budget-policy-2", ("check-2",),
                ),
                expected_head=accepted.event_hash, writer_epoch=1,
            )

        with self.assertRaisesRegex(DispatchDenied, "writer epoch"):
            self.store.commit_intent(
                self.request(), self.capability, self.authority,
                expected_head=accepted.event_hash, writer_epoch=1,
            )
        self.assertEqual(self.store.table_counts()["events"], 1)

    def test_recovery_rejects_reused_repository_writer_epoch(self) -> None:
        first = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-1", "scope-1", "budget-policy-1", ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = first.event_hash
        second = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-2", "plan-command-2", "plan-event-2", "repo-1",
                "run-2", "item-2", "effect-2", "revision-2",
                "descriptor-2", "scope-2", "budget-policy-2", ("check-2",),
            ),
            expected_head=first.event_hash, writer_epoch=2,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = 'plan-event-2'"
                ).fetchone()[0]
            )
            body["writer_epoch"] = 1
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET writer_epoch = 1, event_hash = ?, "
                "body_json = ? WHERE event_id = 'plan-event-2'",
                (event_hash, body_json),
            )
            connection.execute(
                "UPDATE validation_plans SET event_hash = ?, body_json = ? "
                "WHERE plan_id = 'plan-2'",
                (event_hash, body_json),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE "
                "command_id = 'plan-command-2'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-2'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE "
                "repository_id = 'repo-1'",
                (event_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(StorageIntegrityError, "writer epoch"):
            self.store.load_verified("repo-1")

    def test_t16_schema_migrates_populated_pre_t16_plan_fail_closed(self) -> None:
        accepted = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="",
            writer_epoch=1,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = 'plan-event-1'"
                ).fetchone()[0]
            )
            for key in (
                "effect_descriptor_digest", "permission_scope_digest",
                "budget_policy_digest",
                "aggregate_gate_ids", "gate_set_digest",
                "finalization_policy_id", "finalization_policy_version",
                "finalization_issuer_fingerprint",
                "failure_policy_id", "failure_policy_version",
                "source_tree_digest", "item_definition_digest",
                "plan_schema_version", "reducer_version",
                "accepted_plan_semantic_digest", "complete_policy_digest",
            ):
                body.pop(key)
            body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
            event_hash = self.store._event_hash(body)
            payload_digest = self.store._event_hash(
                {
                    key: body[key]
                    for key in PlanAcceptanceContract.__dataclass_fields__
                    if key in body
                }
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (event_hash, body_json, "plan-event-1"),
            )
            connection.execute(
                "UPDATE validation_plans SET payload_digest = ?, event_hash = ?, "
                "body_json = ? WHERE plan_id = 'plan-1'",
                (payload_digest, event_hash, body_json),
            )
            connection.execute(
                "UPDATE command_outcomes SET payload_digest = ?, event_hash = ? "
                "WHERE command_id = 'plan-command-1'",
                (payload_digest, event_hash),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = 'repo-1'",
                (event_hash,),
            )
            connection.execute("PRAGMA foreign_keys = OFF")
            connection.execute("DROP TABLE operation_finalizations")
            connection.execute("ALTER TABLE runs DROP COLUMN continuation_cursor")
            for column_name in (
                "effect_descriptor_digest", "permission_scope_digest",
                "budget_policy_digest",
                "aggregate_gate_ids_json", "gate_set_digest",
                "finalization_policy_id", "finalization_policy_version",
                "finalization_issuer_fingerprint",
                "source_tree_digest", "item_definition_digest",
                "plan_schema_version", "reducer_version",
                "accepted_plan_semantic_digest", "complete_policy_digest",
            ):
                connection.execute(
                    f"ALTER TABLE validation_plans DROP COLUMN {column_name}"
                )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash
        migrated = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        )
        migrated._bind_classification_authority(self.authority)
        migrated.load_verified("repo-1")
        connection = sqlite3.connect(self.database_path)
        try:
            run_columns = {
                row[1] for row in connection.execute("PRAGMA table_info(runs)")
            }
            plan_columns = {
                row[1]
                for row in connection.execute(
                    "PRAGMA table_info(validation_plans)"
                )
            }
            gate_json = connection.execute(
                "SELECT aggregate_gate_ids_json FROM validation_plans"
            ).fetchone()[0]
            migrated_bindings = connection.execute(
                "SELECT source_tree_digest, item_definition_digest, "
                "plan_schema_version, reducer_version, "
                "accepted_plan_semantic_digest, complete_policy_digest "
                "FROM validation_plans"
            ).fetchone()
        finally:
            connection.close()
        self.assertIn("continuation_cursor", run_columns)
        self.assertIn("finalization_issuer_fingerprint", plan_columns)
        self.assertIsNone(gate_json)
        self.assertEqual(migrated_bindings, (None,) * 6)
        self.assertNotEqual(accepted.event_hash, event_hash)
        connection = sqlite3.connect(self.database_path)
        try:
            before_denial = tuple(connection.iterdump())
        finally:
            connection.close()
        with self.assertRaisesRegex(
            StorageIntegrityError, "command ID was reused with a different payload"
        ):
            migrated.accept_plan(
                PlanAcceptanceRequest(
                    "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                    "run-1", "item-1", "effect-1", "revision-1",
                    "descriptor-digest", "scope-1", "budget-policy-digest",
                    ("check-1",),
                ),
                expected_head=event_hash,
                writer_epoch=2,
            )
        with self.assertRaisesRegex(
            DispatchDenied, "predates required finalization pins"
        ):
            migrated.commit_intent(
                self.request(), self.capability, self.authority,
                expected_head=event_hash, writer_epoch=2,
            )
        connection = sqlite3.connect(self.database_path)
        try:
            after_denial = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_denial, before_denial)

    def _pause_capability(self, suffix: str = "1"):
        grant = SyntheticOperatorGrant(
            f"operator-grant-{suffix}", "repo-1", "run-1", "PAUSE",
            f"operator-scope-{suffix}",
        )
        self.authority.register_operator(grant)
        return self.authority.claim_operator(
            grant.grant_id, grant.repository_id, grant.run_id, grant.action,
            grant.scope_digest,
        )

    @staticmethod
    def _pause_request(suffix: str = "1") -> PauseBeforeDispatchRequest:
        return PauseBeforeDispatchRequest(
            f"pause-{suffix}", f"pause-command-{suffix}",
            f"pause-request-event-{suffix}", f"pause-settled-event-{suffix}",
            f"pause-fence-{suffix}", "repo-1", "run-1", "item-1",
            "OPERATOR_PAUSE", f"cursor-{suffix}",
        )

    def _stop_capability(self, mode: StopMode, suffix: str = "1"):
        action = (
            "STOP_GRACEFUL"
            if mode is StopMode.GRACEFUL
            else "STOP_IMMEDIATE"
        )
        grant = SyntheticOperatorGrant(
            f"stop-grant-{suffix}", "repo-1", "run-1", action,
            f"stop-scope-{suffix}",
        )
        self.authority.register_operator(grant)
        return self.authority.claim_operator(
            grant.grant_id, grant.repository_id, grant.run_id, grant.action,
            grant.scope_digest,
        )

    def test_t13_pre_action_revocation_blocks_matching_effect_grant(self) -> None:
        request = self.request()
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-t13", "plan-command-t13", "plan-event-t13",
                request.repository_id, request.run_id, request.item_id,
                request.logical_effect_id, "revision-1",
                request.effect_descriptor_digest, self.capability.scope_digest,
                request.budget_policy_digest, ("check-1",),
            ),
            expected_head="",
            writer_epoch=1,
        )
        fact = AuthorityLifecycleFactRequest(
            "fact-t13", "fact-command-t13", "fact-event-t13",
            request.repository_id, request.run_id, request.item_id,
            request.logical_effect_id, "EFFECT", self.capability.grant_id,
            "EXECUTE_EFFECT", self.capability.scope_digest,
            AuthorityFactKind.REVOKED, GovernedOrder.BEFORE, "NO_ACTION",
            None, None,
        )
        evidence: SyntheticAuthorityLifecycleEvidence = (
            self.authority.issue_authority_lifecycle_evidence("proof-t13", fact)
        )
        self.oracle.allowed_head = plan.event_hash

        recorded = self.store.record_authority_fact(
            fact,
            evidence,
            self.authority,
            expected_head=plan.event_hash,
            writer_epoch=2,
        )

        self.assertEqual(recorded.resulting_state, LifecycleState.BLOCKED)
        self.oracle.allowed_head = recorded.event_hash
        with self.assertRaisesRegex(DispatchDenied, "authority"):
            self.store.commit_intent(
                request,
                self.capability,
                self.authority,
                expected_head=recorded.event_hash,
                writer_epoch=3,
            )

    def test_t13_after_action_expiry_is_future_only(self) -> None:
        intent = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = intent.event_hash
        fact = AuthorityLifecycleFactRequest(
            "fact-after", "fact-command-after", "fact-event-after",
            "repo-1", "run-1", "item-1", "effect-1", "EFFECT",
            "grant-1", "EXECUTE_EFFECT", "scope-1",
            AuthorityFactKind.EXPIRED, GovernedOrder.AFTER, "INTENT",
            intent.event_id, intent.event_hash,
        )
        recorded = self.store.record_authority_fact(
            fact,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-after", fact
            ),
            self.authority,
            expected_head=intent.event_hash,
            writer_epoch=3,
        )
        self.assertEqual(recorded.resulting_state, LifecycleState.RUNNING)
        connection = self.store._connect()
        try:
            self.assertEqual(
                connection.execute(
                    "SELECT COUNT(*) FROM effective_authority"
                ).fetchone()[0],
                1,
            )
            self.assertEqual(
                connection.execute(
                    "SELECT COUNT(*) FROM dispatch_fences"
                ).fetchone()[0],
                0,
            )
        finally:
            connection.close()
        self.oracle.allowed_head = recorded.event_hash
        self.store.load_verified("repo-1")

    def test_t13_unknown_claim_status_retains_slot_and_disputes_history(self) -> None:
        intent = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = intent.event_hash
        fact = AuthorityLifecycleFactRequest(
            "fact-unknown", "fact-command-unknown", "fact-event-unknown",
            "repo-1", "run-1", "item-1", "effect-1", "EFFECT",
            "grant-1", "EXECUTE_EFFECT", "scope-1",
            AuthorityFactKind.CLAIM_STATUS_UNKNOWN, GovernedOrder.UNKNOWN,
            "INTENT", intent.event_id, intent.event_hash,
        )
        recorded = self.store.record_authority_fact(
            fact,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-unknown", fact
            ),
            self.authority,
            expected_head=intent.event_hash,
            writer_epoch=3,
        )
        self.assertEqual(
            recorded.resulting_state, LifecycleState.RECONCILIATION_REQUIRED
        )
        connection = sqlite3.connect(self.database_path)
        try:
            self.assertEqual(
                connection.execute(
                    "SELECT status FROM effective_authority"
                ).fetchone()[0],
                "UNKNOWN",
            )
            self.assertEqual(
                connection.execute(
                    "SELECT COUNT(*) FROM outstanding_slot"
                ).fetchone()[0],
                1,
            )
        finally:
            connection.close()

    def test_t13_own_consumption_is_nonbreaching_and_mismatch_rejects(self) -> None:
        intent = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = intent.event_hash
        fact = AuthorityLifecycleFactRequest(
            "fact-own", "fact-command-own", "fact-event-own", "repo-1",
            "run-1", "item-1", "effect-1", "EFFECT", "grant-1",
            "EXECUTE_EFFECT", "scope-1", AuthorityFactKind.OWN_CONSUMED,
            GovernedOrder.DURING, "INTENT", intent.event_id, intent.event_hash,
        )
        recorded = self.store.record_authority_fact(
            fact,
            self.authority.issue_authority_lifecycle_evidence("proof-own", fact),
            self.authority,
            expected_head=intent.event_hash,
            writer_epoch=3,
        )
        self.assertEqual(recorded.resulting_state, LifecycleState.RUNNING)
        connection = sqlite3.connect(self.database_path)
        try:
            self.assertEqual(
                connection.execute(
                    "SELECT COUNT(*) FROM effective_authority"
                ).fetchone()[0],
                1,
            )
            self.assertEqual(
                connection.execute(
                    "SELECT COUNT(*) FROM dispatch_fences"
                ).fetchone()[0],
                0,
            )
        finally:
            connection.close()
        self.oracle.allowed_head = recorded.event_hash
        launch = self.store.claim_operation_launch(self.request(), intent)
        self.oracle.allowed_head = launch.event_hash
        self.store._contact_claimed_operation(
            self.request(), self.capability, intent, launch,
            self.store._adapter_target_digest("repo-1", "EFFECT"),
        )
        connection = self.store._connect()
        try:
            contact_head = connection.execute(
                "SELECT catalog_head FROM repositories WHERE repository_id = 'repo-1'"
            ).fetchone()[0]
            with self.assertRaisesRegex(DispatchDenied, "authority"):
                self.store._require_effective_authority(
                    connection, self.authority.issuer_fingerprint, "EFFECT",
                    "grant-1", "EXECUTE_EFFECT", "scope-1",
                    continuing_event_id="different-intent",
                    continuing_event_hash="different-hash",
                )
        finally:
            connection.close()
        self.oracle.allowed_head = contact_head
        self.store.load_verified("repo-1")
        mismatched = replace(
            fact,
            fact_id="fact-own-bad",
            command_id="fact-command-own-bad",
            event_id="fact-event-own-bad",
            governed_event_hash="0" * 64,
        )
        self.oracle.allowed_head = contact_head
        with self.assertRaisesRegex(DispatchDenied, "boundary"):
            self.store.record_authority_fact(
                mismatched,
                self.authority.issue_authority_lifecycle_evidence(
                    "proof-own-bad", mismatched
                ),
                self.authority,
                expected_head=contact_head,
                writer_epoch=6,
            )

    def test_t13_exact_correction_clears_only_its_effective_generation(self) -> None:
        request = self.request()
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-correct", "plan-command-correct", "plan-event-correct",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                request.effect_descriptor_digest, "scope-1",
                request.budget_policy_digest, ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        denied = AuthorityLifecycleFactRequest(
            "fact-denied", "fact-command-denied", "fact-event-denied",
            "repo-1", "run-1", "item-1", "effect-1", "EFFECT",
            "grant-1", "EXECUTE_EFFECT", "scope-1",
            AuthorityFactKind.REVOKED, GovernedOrder.BEFORE, "NO_ACTION",
            None, None,
        )
        denial = self.store.record_authority_fact(
            denied,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-denied", denied
            ),
            self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        self.oracle.allowed_head = denial.event_hash
        correction = AuthorityLifecycleFactRequest(
            "fact-correct", "fact-command-correct", "fact-event-correct",
            "repo-1", "run-1", "item-1", "effect-1", "EFFECT",
            "grant-1", "EXECUTE_EFFECT", "scope-1",
            AuthorityFactKind.CORRECTION, GovernedOrder.BEFORE, "NO_ACTION",
            None, None, corrected_fact_id=denied.fact_id,
            corrected_event_hash=denial.event_hash,
        )
        corrected = self.store.record_authority_fact(
            correction,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-correct", correction
            ),
            self.authority,
            expected_head=denial.event_hash, writer_epoch=3,
        )
        self.assertEqual(corrected.resulting_state, LifecycleState.BLOCKED)
        connection = sqlite3.connect(self.database_path)
        try:
            self.assertEqual(
                connection.execute(
                    "SELECT COUNT(*) FROM effective_authority"
                ).fetchone()[0],
                0,
            )
            self.assertEqual(
                connection.execute(
                    "SELECT COUNT(*) FROM dispatch_fences"
                ).fetchone()[0],
                0,
            )
        finally:
            connection.close()
        self.oracle.allowed_head = corrected.event_hash
        self.store.load_verified("repo-1")

    def test_t13_correction_restores_older_uncorrected_denial(self) -> None:
        request = self.request()
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-stack", "plan-command-stack", "plan-event-stack",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                request.effect_descriptor_digest, "scope-1",
                request.budget_policy_digest, ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        first = AuthorityLifecycleFactRequest(
            "fact-stack-1", "fact-command-stack-1", "fact-event-stack-1",
            "repo-1", "run-1", "item-1", "effect-1", "EFFECT",
            "grant-1", "EXECUTE_EFFECT", "scope-1",
            AuthorityFactKind.REVOKED, GovernedOrder.BEFORE, "NO_ACTION",
            None, None,
        )
        first_receipt = self.store.record_authority_fact(
            first,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-stack-1", first
            ),
            self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        self.oracle.allowed_head = first_receipt.event_hash
        second = replace(
            first,
            fact_id="fact-stack-2", command_id="fact-command-stack-2",
            event_id="fact-event-stack-2",
            fact_kind=AuthorityFactKind.SOURCE_UNAVAILABLE,
            governed_order=GovernedOrder.UNKNOWN,
        )
        second_receipt = self.store.record_authority_fact(
            second,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-stack-2", second
            ),
            self.authority,
            expected_head=first_receipt.event_hash, writer_epoch=3,
        )
        self.oracle.allowed_head = second_receipt.event_hash
        correction = replace(
            first,
            fact_id="fact-stack-correction",
            command_id="fact-command-stack-correction",
            event_id="fact-event-stack-correction",
            fact_kind=AuthorityFactKind.CORRECTION,
            corrected_fact_id=second.fact_id,
            corrected_event_hash=second_receipt.event_hash,
        )
        corrected = self.store.record_authority_fact(
            correction,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-stack-correction", correction
            ),
            self.authority,
            expected_head=second_receipt.event_hash, writer_epoch=4,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            effective = connection.execute(
                "SELECT originating_fact_id FROM effective_authority"
            ).fetchone()[0]
            fences = {
                row[0] for row in connection.execute(
                    "SELECT fence_id FROM dispatch_fences"
                )
            }
        finally:
            connection.close()
        self.assertEqual(effective, first.fact_id)
        self.assertEqual(fences, {f"authority:{first.fact_id}"})
        self.oracle.allowed_head = corrected.event_hash
        self.store.load_verified("repo-1")
        with self.assertRaisesRegex(DispatchDenied, "authority"):
            self.store.commit_intent(
                request, self.capability, self.authority,
                expected_head=corrected.event_hash, writer_epoch=5,
            )

    def test_t13_fact_write_is_atomic_replay_safe_and_tamper_evident(self) -> None:
        request = self.request()
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-atomic", "plan-command-atomic", "plan-event-atomic",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                request.effect_descriptor_digest, "scope-1",
                request.budget_policy_digest, ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        fact = AuthorityLifecycleFactRequest(
            "fact-atomic", "fact-command-atomic", "fact-event-atomic",
            "repo-1", "run-1", "item-1", "effect-1", "EFFECT",
            "grant-1", "EXECUTE_EFFECT", "scope-1",
            AuthorityFactKind.SOURCE_UNAVAILABLE, GovernedOrder.UNKNOWN,
            "NO_ACTION", None, None,
        )
        evidence = self.authority.issue_authority_lifecycle_evidence(
            "proof-atomic", fact
        )
        with self.assertRaises(InjectedFailure):
            self.store.record_authority_fact(
                fact, evidence, self.authority,
                expected_head=plan.event_hash, writer_epoch=2,
                failure_hook=raise_at("after_authority_fact_writes_before_commit"),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            self.assertEqual(
                connection.execute(
                    "SELECT COUNT(*) FROM authority_facts"
                ).fetchone()[0],
                0,
            )
        finally:
            connection.close()
        recorded = self.store.record_authority_fact(
            fact, evidence, self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        self.oracle.allowed_head = recorded.event_hash
        replay = self.store.record_authority_fact(
            fact, evidence, self.authority,
            expected_head=recorded.event_hash, writer_epoch=3,
        )
        self.assertTrue(replay.replayed)
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE effective_authority SET generation = 99"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(StorageIntegrityError, "effective-authority"):
            self.store.load_verified("repo-1")

    def test_t13_lifecycle_decision_table(self) -> None:
        terminal = {
            LifecycleState.COMPLETED,
            LifecycleState.FAILED_FINAL,
            LifecycleState.STOPPED,
        }
        for state in LifecycleState:
            with self.subTest(state=state):
                expected = (
                    state
                    if state in terminal
                    or state in {
                        LifecycleState.PAUSED,
                        LifecycleState.PAUSING,
                        LifecycleState.RECONCILIATION_REQUIRED,
                    }
                    else LifecycleState.RECONCILIATION_REQUIRED
                    if state in {LifecycleState.RUNNING, LifecycleState.VALIDATING}
                    else LifecycleState.BLOCKED
                )
                self.assertEqual(
                    self.store._authority_fact_route(
                        state, AuthorityFactKind.REVOKED, GovernedOrder.BEFORE
                    ),
                    expected,
                )
                self.assertEqual(
                    self.store._authority_fact_route(
                        state, AuthorityFactKind.EXPIRED, GovernedOrder.AFTER
                    ),
                    state,
                )

    def test_t13_future_denial_is_rechecked_before_adapter_contact(self) -> None:
        request = self.request()
        intent = self._commit_planned_intent(
            request, self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = intent.event_hash
        fact = AuthorityLifecycleFactRequest(
            "fact-contact", "fact-command-contact", "fact-event-contact",
            "repo-1", "run-1", "item-1", "effect-1", "EFFECT",
            "grant-1", "EXECUTE_EFFECT", "scope-1",
            AuthorityFactKind.REVOKED, GovernedOrder.AFTER, "INTENT",
            intent.event_id, intent.event_hash,
        )
        recorded = self.store.record_authority_fact(
            fact,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-contact", fact
            ),
            self.authority,
            expected_head=intent.event_hash, writer_epoch=3,
        )
        self.oracle.allowed_head = recorded.event_hash
        with self.assertRaisesRegex(DispatchDenied, "authority"):
            self.store.claim_operation_launch(request, intent)

    def test_t13_operator_consumer_uses_grant_wide_effective_index(self) -> None:
        request = self.request()
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-operator", "plan-command-operator",
                "plan-event-operator", "repo-1", "run-1", "item-1",
                "effect-1", "revision-1", request.effect_descriptor_digest,
                "scope-1", request.budget_policy_digest, ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        capability = self._pause_capability("t13")
        self.oracle.allowed_head = plan.event_hash
        fact = AuthorityLifecycleFactRequest(
            "fact-operator", "fact-command-operator", "fact-event-operator",
            "repo-1", "run-1", "item-1", "effect-1", "OPERATOR",
            capability.grant_id, "PAUSE", capability.scope_digest,
            AuthorityFactKind.REVOKED, GovernedOrder.BEFORE, "NO_ACTION",
            None, None,
        )
        recorded = self.store.record_authority_fact(
            fact,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-operator", fact
            ),
            self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        self.oracle.allowed_head = recorded.event_hash
        with self.assertRaisesRegex(DispatchDenied, "authority"):
            self.store.pause_before_dispatch(
                self._pause_request("t13"), capability, self.authority
            )

    def test_t13_unknown_operator_claim_binds_exact_operator_redemption(self) -> None:
        request = self.request()
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-operator-unknown", "plan-command-operator-unknown",
                "plan-event-operator-unknown", "repo-1", "run-1", "item-1",
                "effect-1", "revision-1", request.effect_descriptor_digest,
                "scope-1", request.budget_policy_digest, ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        capability = self._pause_capability("unknown")
        paused = self.store.pause_before_dispatch(
            self._pause_request("unknown"), capability, self.authority
        )
        self.oracle.allowed_head = paused.event_hash
        fact = AuthorityLifecycleFactRequest(
            "fact-operator-unknown", "fact-command-operator-unknown",
            "fact-event-operator-unknown", "repo-1", "run-1", "item-1",
            "effect-1", "OPERATOR", capability.grant_id, "PAUSE",
            capability.scope_digest, AuthorityFactKind.CLAIM_STATUS_UNKNOWN,
            GovernedOrder.UNKNOWN, "REDEMPTION", paused.event_id,
            paused.event_hash,
        )
        recorded = self.store.record_authority_fact(
            fact,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-operator-unknown", fact
            ),
            self.authority,
            expected_head=paused.event_hash, writer_epoch=4,
        )
        self.assertEqual(recorded.resulting_state, LifecycleState.PAUSED)

    def test_t13_unknown_claim_rejects_cross_kind_grant_id_collision(self) -> None:
        request = self.request()
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-collision", "plan-command-collision",
                "plan-event-collision", "repo-1", "run-1", "item-1",
                "effect-1", "revision-1", request.effect_descriptor_digest,
                "scope-1", request.budget_policy_digest, ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        operator_grant = SyntheticOperatorGrant(
            "grant-1", "repo-1", "run-1", "PAUSE", "scope-1"
        )
        self.authority.register_operator(operator_grant)
        operator_capability = self.authority.claim_operator(
            *operator_grant.__dict__.values()
        )
        paused = self.store.pause_before_dispatch(
            self._pause_request("collision"), operator_capability, self.authority
        )
        self.oracle.allowed_head = paused.event_hash
        fact = AuthorityLifecycleFactRequest(
            "fact-collision", "fact-command-collision", "fact-event-collision",
            "repo-1", "run-1", "item-1", "effect-1", "EFFECT", "grant-1",
            "EXECUTE_EFFECT", "scope-1",
            AuthorityFactKind.CLAIM_STATUS_UNKNOWN, GovernedOrder.UNKNOWN,
            "REDEMPTION", paused.event_id, paused.event_hash,
        )
        with self.assertRaisesRegex(DispatchDenied, "local use"):
            self.store.record_authority_fact(
                fact,
                self.authority.issue_authority_lifecycle_evidence(
                    "proof-collision", fact
                ),
                self.authority,
                expected_head=paused.event_hash, writer_epoch=4,
            )

    def test_t13_unknown_validator_claim_binds_exact_validator_redemption(self) -> None:
        observation = self._record_effect_observation(check_ids=("check-1",))
        validator_request, capability = self._validator_intent(observation)
        intent = self.store.commit_validator_intent(
            validator_request, capability, self.authority
        )
        self.oracle.allowed_head = intent.event_hash
        fact = AuthorityLifecycleFactRequest(
            "fact-validator-unknown", "fact-command-validator-unknown",
            "fact-event-validator-unknown", "repo-1", "run-1", "item-1",
            "effect-1", "VALIDATOR", capability.grant_id, "RUN_VALIDATOR",
            capability.scope_digest, AuthorityFactKind.CLAIM_STATUS_UNKNOWN,
            GovernedOrder.UNKNOWN, "INTENT", intent.event_id,
            intent.event_hash,
        )
        recorded = self.store.record_authority_fact(
            fact,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-validator-unknown", fact
            ),
            self.authority,
            expected_head=intent.event_hash, writer_epoch=6,
        )
        self.assertEqual(
            recorded.resulting_state, LifecycleState.RECONCILIATION_REQUIRED
        )

    def test_t13_own_validator_consumption_allows_exact_contact(self) -> None:
        observation = self._record_effect_observation(check_ids=("check-1",))
        validator_request, capability = self._validator_intent(observation)
        intent = self.store.commit_validator_intent(
            validator_request, capability, self.authority
        )
        self.oracle.allowed_head = intent.event_hash
        fact = AuthorityLifecycleFactRequest(
            "fact-validator-own", "fact-command-validator-own",
            "fact-event-validator-own", "repo-1", "run-1", "item-1",
            "effect-1", "VALIDATOR", capability.grant_id, "RUN_VALIDATOR",
            capability.scope_digest, AuthorityFactKind.OWN_CONSUMED,
            GovernedOrder.DURING, "INTENT", intent.event_id,
            intent.event_hash,
        )
        recorded = self.store.record_authority_fact(
            fact,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-validator-own", fact
            ),
            self.authority,
            expected_head=intent.event_hash, writer_epoch=6,
        )
        self.oracle.allowed_head = recorded.event_hash
        self.store._contact_committed_validator(
            validator_request, capability, intent,
            self.store._adapter_target_digest("repo-1", "VALIDATOR"),
            self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            contact_head = connection.execute(
                "SELECT catalog_head FROM repositories WHERE repository_id = 'repo-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = contact_head
        self.store.load_verified("repo-1")

    def test_t13_supersession_rejects_cycles_and_never_revives_predecessor(
        self,
    ) -> None:
        request = self.request()
        successor = SyntheticGrant(
            "grant-successor", "repo-1", "effect-1", "attempt-1", "scope-1"
        )
        self.authority.register(successor)
        final_successor = SyntheticGrant(
            "grant-final", "repo-1", "effect-1", "attempt-1", "scope-1"
        )
        self.authority.register(final_successor)
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-super", "plan-command-super", "plan-event-super",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                request.effect_descriptor_digest, "scope-1",
                request.budget_policy_digest, ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        superseded = AuthorityLifecycleFactRequest(
            "fact-super", "fact-command-super", "fact-event-super",
            "repo-1", "run-1", "item-1", "effect-1", "EFFECT",
            "grant-1", "EXECUTE_EFFECT", "scope-1",
            AuthorityFactKind.SUPERSEDED, GovernedOrder.BEFORE, "NO_ACTION",
            None, None, successor_grant_id="grant-successor",
        )
        recorded = self.store.record_authority_fact(
            superseded,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-super", superseded
            ),
            self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        self.oracle.allowed_head = recorded.event_hash
        chain = replace(
            superseded,
            fact_id="fact-chain", command_id="fact-command-chain",
            event_id="fact-event-chain", grant_id="grant-successor",
            successor_grant_id="grant-final",
        )
        chained = self.store.record_authority_fact(
            chain,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-chain", chain
            ),
            self.authority,
            expected_head=recorded.event_hash, writer_epoch=3,
        )
        self.oracle.allowed_head = chained.event_hash
        conflict = replace(
            superseded,
            fact_id="fact-conflict", command_id="fact-command-conflict",
            event_id="fact-event-conflict", successor_grant_id="grant-final",
        )
        with self.assertRaisesRegex(DispatchDenied, "conflicts"):
            self.store.record_authority_fact(
                conflict,
                self.authority.issue_authority_lifecycle_evidence(
                    "proof-conflict", conflict
                ),
                self.authority,
                expected_head=chained.event_hash, writer_epoch=4,
            )
        cycle = replace(
            superseded,
            fact_id="fact-cycle", command_id="fact-command-cycle",
            event_id="fact-event-cycle", grant_id="grant-final",
            successor_grant_id="grant-1",
        )
        with self.assertRaisesRegex(DispatchDenied, "cyclic"):
            self.store.record_authority_fact(
                cycle,
                self.authority.issue_authority_lifecycle_evidence(
                    "proof-cycle", cycle
                ),
                self.authority,
                expected_head=chained.event_hash, writer_epoch=4,
            )
        correction = replace(
            chain,
            fact_id="fact-chain-correction",
            command_id="fact-command-chain-correction",
            event_id="fact-event-chain-correction",
            fact_kind=AuthorityFactKind.CORRECTION,
            successor_grant_id=None,
            corrected_fact_id=chain.fact_id,
            corrected_event_hash=chained.event_hash,
        )
        corrected = self.store.record_authority_fact(
            correction,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-chain-correction", correction
            ),
            self.authority,
            expected_head=chained.event_hash, writer_epoch=4,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            self.assertEqual(
                connection.execute(
                    "SELECT status FROM effective_authority WHERE grant_id = 'grant-1'"
                ).fetchone()[0],
                "DENIED",
            )
            self.assertEqual(
                connection.execute(
                    "SELECT COUNT(*) FROM authority_supersessions"
                ).fetchone()[0],
                1,
            )
        finally:
            connection.close()
        self.oracle.allowed_head = corrected.event_hash
        self.store.load_verified("repo-1")

    def test_t13_supersession_graph_is_namespaced_by_full_typed_binding(self) -> None:
        request = self.request()
        self.authority.register(
            SyntheticGrant(
                "grant-successor", "repo-1", "effect-1", "attempt-1",
                "scope-1",
            )
        )
        for grant_id in ("grant-1", "grant-successor"):
            self.authority.register_validator(
                SyntheticValidatorGrant(
                    grant_id, "repo-1", "effect-1", "revision-1", "check-1",
                    "input-1", "validator-attempt-1", "validator-scope-1",
                )
            )
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-typed", "plan-command-typed", "plan-event-typed",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                request.effect_descriptor_digest, "scope-1",
                request.budget_policy_digest, ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        effect_fact = AuthorityLifecycleFactRequest(
            "fact-effect-typed", "fact-command-effect-typed",
            "fact-event-effect-typed", "repo-1", "run-1", "item-1",
            "effect-1", "EFFECT", "grant-1", "EXECUTE_EFFECT", "scope-1",
            AuthorityFactKind.SUPERSEDED, GovernedOrder.BEFORE, "NO_ACTION",
            None, None, successor_grant_id="grant-successor",
        )
        effect_recorded = self.store.record_authority_fact(
            effect_fact,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-effect-typed", effect_fact
            ),
            self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        self.oracle.allowed_head = effect_recorded.event_hash
        validator_fact = replace(
            effect_fact,
            fact_id="fact-validator-typed",
            command_id="fact-command-validator-typed",
            event_id="fact-event-validator-typed",
            grant_kind="VALIDATOR",
            action="RUN_VALIDATOR",
            scope_digest="validator-scope-1",
        )
        validator_recorded = self.store.record_authority_fact(
            validator_fact,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-validator-typed", validator_fact
            ),
            self.authority,
            expected_head=effect_recorded.event_hash, writer_epoch=3,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            self.assertEqual(
                connection.execute(
                    "SELECT COUNT(*) FROM authority_supersessions"
                ).fetchone()[0],
                2,
            )
        finally:
            connection.close()
        self.oracle.allowed_head = validator_recorded.event_hash
        self.store.load_verified("repo-1")

    def _stop_escalation_capability(self, suffix: str = "1"):
        grant = SyntheticOperatorGrant(
            f"escalation-grant-{suffix}", "repo-1", "run-1",
            "STOP_ESCALATE", f"escalation-scope-{suffix}",
        )
        self.authority.register_operator(grant)
        return self.authority.claim_operator(*grant.__dict__.values())

    @staticmethod
    def _stop_request(
        mode: StopMode = StopMode.IMMEDIATE, suffix: str = "1"
    ) -> StopRequest:
        return StopRequest(
            f"stop-{suffix}", f"stop-command-{suffix}",
            f"stop-event-{suffix}", "repo-1", "run-1", mode,
            "OPERATOR_STOP",
            "2030-01-01T00:00:00Z" if mode is StopMode.GRACEFUL else None,
        )

    def test_t19_immediate_stop_is_atomic_before_fence(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        capability = self._stop_capability(StopMode.IMMEDIATE)
        request = self._stop_request()

        with self.assertRaises(InjectedFailure):
            self.store.stop(
                request, capability, self.authority,
                failure_hook=raise_at("after_stop_recorded_before_fence"),
            )
        counts = self.store.table_counts()
        self.assertEqual(counts["events"], 1)
        self.assertEqual(counts["stop_actions"], 0)
        self.assertEqual(counts["operator_redemptions"], 0)
        self.assertEqual(counts["dispatch_fences"], 0)
        self.assertEqual(
            self.store.load_run_lifecycle("run-1"), LifecycleState.PLANNED
        )

        with self.assertRaises(InjectedFailure):
            self.store.stop(
                request, capability, self.authority,
                failure_hook=raise_at(
                    "after_stop_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            committed_hash = connection.execute(
                "SELECT event_hash FROM stop_actions WHERE stop_id = 'stop-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = committed_hash
        replay = self.store.stop(request, capability, self.authority)
        self.assertEqual(replay.resulting_state, LifecycleState.STOPPED)
        self.assertEqual(self.store.table_counts()["stop_actions"], 1)
        self.assertEqual(self.store.table_counts()["dispatch_fences"], 1)
        self.assertTrue(replay.replayed)
        self.assertEqual(replay.event_hash, committed_hash)
        with self.assertRaisesRegex(StorageIntegrityError, "different payload"):
            self.store.stop(
                replace(request, reason_code="DIFFERENT_REASON"),
                capability,
                self.authority,
            )
        with self.assertRaises(DispatchDenied):
            self.store.stop(
                self._stop_request(StopMode.IMMEDIATE, "2"),
                self._stop_capability(StopMode.IMMEDIATE, "2"),
                self.authority,
            )
        self.store.load_verified("repo-1")

    def test_t19_alternate_identity_replay_authenticates_capability(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        request = self._stop_request()
        capability = self._stop_capability(StopMode.IMMEDIATE)
        stopped = self.store.stop(request, capability, self.authority)
        self.oracle.allowed_head = stopped.event_hash

        forged = replace(capability, issuer_mac="forged-issuer-mac")
        with self.assertRaisesRegex(DispatchDenied, "was not issued here"):
            self.store.stop(
                replace(
                    request,
                    command_id="alternate-stop-command",
                    event_id="alternate-stop-event",
                ),
                forged,
                self.authority,
            )

    def test_t19_operator_issuer_and_grant_identity_survive_restart(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        request = self._stop_request()
        stopped = self.store.stop(
            request,
            self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash

        replacement = SyntheticAuthority(b"r" * 32)
        replay_grant = SyntheticOperatorGrant(
            "stop-grant-1", "repo-1", "run-1", "STOP_IMMEDIATE",
            "stop-scope-1",
        )
        replacement.register_operator(replay_grant)
        replay_capability = replacement.claim_operator(
            *replay_grant.__dict__.values()
        )
        with self.assertRaisesRegex(DispatchDenied, "issuer"):
            self.store.stop(request, replay_capability, replacement)

        plan_2 = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-2", "plan-command-2", "plan-event-2", "repo-1",
                "run-2", "item-2", "effect-2", "revision-2",
                "descriptor-digest", "operator-scope-2",
                "budget-policy-digest", ("check-2",),
            ),
            expected_head=stopped.event_hash, writer_epoch=3,
        )
        self.oracle.allowed_head = plan_2.event_hash
        rebound = SyntheticAuthority(b"b" * 32)
        rebound_grant = SyntheticOperatorGrant(
            "stop-grant-1", "repo-1", "run-2", "STOP_IMMEDIATE",
            "stop-scope-2",
        )
        rebound.register_operator(rebound_grant)
        rebound_capability = rebound.claim_operator(
            *rebound_grant.__dict__.values()
        )
        with self.assertRaisesRegex(DispatchDenied, "grant was already redeemed"):
            self.store.stop(
                replace(
                    self._stop_request(StopMode.IMMEDIATE, "2"),
                    run_id="run-2",
                ),
                rebound_capability,
                rebound,
            )

    def test_t19_legacy_stop_event_has_typed_compatibility_rejection(
        self,
    ) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        stopped = self.store.stop(
            self._stop_request(),
            self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            row = connection.execute(
                "SELECT body_json FROM stop_actions WHERE stop_id = 'stop-1'"
            ).fetchone()
            body = json.loads(row["body_json"])
            del body["mode"]
            legacy_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                "event_id = 'stop-event-1'",
                (legacy_hash, body_json),
            )
            connection.execute(
                "UPDATE stop_actions SET event_hash = ?, body_json = ? WHERE "
                "stop_id = 'stop-1'",
                (legacy_hash, body_json),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE "
                "command_id = 'stop-command-1'",
                (legacy_hash,),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (legacy_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE "
                "repository_id = 'repo-1'",
                (legacy_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = legacy_hash

        with self.assertRaisesRegex(
            StorageIntegrityError, "unsupported STOP_RECORDED event schema"
        ):
            self.store.load_verified("repo-1")

    def test_t19_stop_event_decoder_rejects_extensions_and_mode_mismatch(
        self,
    ) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        stopped = self.store.stop(
            self._stop_request(),
            self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM stop_actions WHERE stop_id = 'stop-1'"
                ).fetchone()["body_json"]
            )
        finally:
            connection.close()

        with self.assertRaisesRegex(
            StorageIntegrityError, "unsupported STOP_RECORDED event schema"
        ):
            self.store._validate_stop_event_body(body | {"extension": True})
        with self.assertRaisesRegex(
            StorageIntegrityError, "STOP_RECORDED event semantics are invalid"
        ):
            self.store._validate_stop_event_body(
                body | {"action": "STOP_GRACEFUL"}
            )
        with self.assertRaisesRegex(
            StorageIntegrityError, "STOP_RECORDED event semantics are invalid"
        ):
            self.store._validate_stop_event_body(body | {"sequence": "2"})

    def test_t19_recovery_rejects_forged_stop_predecessor_state_and_cursor(
        self,
    ) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        committed = self.store.commit_intent(
            self.request(), self.capability, self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        self.oracle.allowed_head = committed.event_hash
        stopped = self._stop_run()

        for suffix, changes in (
            ("state", {"lifecycle_from": LifecycleState.PLANNED.value}),
            ("cursor", {"retained_continuation_cursor": "forged-cursor"}),
        ):
            tampered_path = self.database_path.with_name(
                f"tampered-stop-{suffix}.sqlite3"
            )
            shutil.copy2(self.database_path, tampered_path)
            connection = sqlite3.connect(tampered_path)
            connection.row_factory = sqlite3.Row
            try:
                body = json.loads(
                    connection.execute(
                        "SELECT body_json FROM stop_actions WHERE stop_id = 'stop-1'"
                    ).fetchone()["body_json"]
                ) | changes
                event_hash = self.store._event_hash(body)
                body_json = json.dumps(
                    body, sort_keys=True, separators=(",", ":")
                )
                connection.execute(
                    "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                    "event_id = 'stop-event-1'",
                    (event_hash, body_json),
                )
                connection.execute(
                    "UPDATE stop_actions SET retained_continuation_cursor = ?, "
                    "event_hash = ?, body_json = ? WHERE stop_id = 'stop-1'",
                    (
                        body["retained_continuation_cursor"], event_hash,
                        body_json,
                    ),
                )
                connection.execute(
                    "UPDATE command_outcomes SET event_hash = ? WHERE "
                    "command_id = 'stop-command-1'",
                    (event_hash,),
                )
                connection.execute(
                    "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                    (event_hash,),
                )
                connection.execute(
                    "UPDATE repositories SET catalog_head = ? WHERE "
                    "repository_id = 'repo-1'",
                    (event_hash,),
                )
                connection.commit()
            finally:
                connection.close()
            oracle = MutableFreshnessOracle()
            oracle.allowed_head = event_hash
            with self.subTest(suffix=suffix), self.assertRaisesRegex(
                StorageIntegrityError, "(event lifecycle|stop predecessor)"
            ):
                SQLiteStateStore(
                    tampered_path, oracle, "repo-1"
                ).load_verified("repo-1")

    def test_t19_recovery_rejects_stop_fence_retargeted_from_plan(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        stopped = self._stop_run()
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM stop_actions WHERE stop_id = 'stop-1'"
                ).fetchone()["body_json"]
            )
            body["item_id"] = "forged-item"
            body["logical_effect_id"] = "forged-effect"
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET item_id = 'forged-item', event_hash = ?, "
                "body_json = ? WHERE event_id = 'stop-event-1'",
                (event_hash, body_json),
            )
            connection.execute(
                "UPDATE stop_actions SET item_id = 'forged-item', "
                "logical_effect_id = 'forged-effect', event_hash = ?, "
                "body_json = ? WHERE stop_id = 'stop-1'",
                (event_hash, body_json),
            )
            connection.execute(
                "UPDATE dispatch_fences SET item_id = 'forged-item', "
                "logical_effect_id = 'forged-effect' WHERE fence_id = ?",
                (body["fence_id"],),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE "
                "command_id = 'stop-command-1'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE "
                "repository_id = 'repo-1'",
                (event_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(
            StorageIntegrityError, "stop plan binding"
        ):
            self.store.load_verified("repo-1")

    def test_t18_graceful_stop_persists_deadline_and_rejects_mode_mismatch(
        self,
    ) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        request = self._stop_request(StopMode.GRACEFUL)
        stopped = self.store.stop(
            request,
            self._stop_capability(StopMode.GRACEFUL),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            persisted = connection.execute(
                "SELECT mode, drain_deadline_utc FROM stop_actions "
                "WHERE stop_id = 'stop-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(persisted, ("GRACEFUL", "2030-01-01T00:00:00Z"))
        with self.assertRaisesRegex(ValueError, "cannot carry"):
            replace(
                self._stop_request(StopMode.IMMEDIATE, "2"),
                drain_deadline_utc="2030-01-01T00:00:00Z",
            ).validate()
        with self.assertRaisesRegex(ValueError, "requires"):
            replace(request, drain_deadline_utc=None).validate()
        self.store.load_verified("repo-1")

    def test_t19_active_stop_retains_slot_and_admits_late_receipt(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        stopped = self.store.stop(
            self._stop_request(),
            self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        with self.assertRaisesRegex(DispatchDenied, "requires RUNNING"):
            self.store.claim_operation_launch(self.request(), committed)
        self.assertEqual(self.store.table_counts()["operation_launches"], 0)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        connection = sqlite3.connect(self.database_path)
        try:
            reservation_before = connection.execute(
                "SELECT held_units, charged_units, uncertainty, disposition "
                "FROM budget_reservations WHERE reservation_id = 'reservation-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(reservation_before, (3, 0, 0, "RESERVED"))

        late = self.store._record_effect_observation(
            EffectObservationRequest(
                "late-observation-1", "late-observe-command-1",
                "late-observation-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "attempt-1", "late-receipt-1",
                self.capability.claim_id, "descriptor-digest", 2,
                "late-settlement-1", "",
            )
        )
        self.oracle.allowed_head = late.event_hash
        self.assertEqual(late.resulting_state, LifecycleState.STOPPED)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        connection = sqlite3.connect(self.database_path)
        try:
            event_kind = connection.execute(
                "SELECT event_kind FROM events WHERE event_id = ?",
                (late.event_id,),
            ).fetchone()[0]
            reservation_after = connection.execute(
                "SELECT held_units, charged_units, uncertainty, disposition "
                "FROM budget_reservations WHERE reservation_id = 'reservation-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(event_kind, "LATE_RECEIPT_RECORDED")
        self.assertEqual(reservation_after, (0, 2, 0, "CONSUMED"))
        self.store.load_verified("repo-1")

    def test_t23_late_receipt_from_validating_preserves_evidence(self) -> None:
        self._record_effect_observation(check_ids=("check-1",))
        late = self.store._record_effect_observation(
            EffectObservationRequest(
                "observation-2", "observe-command-2", "observation-event-2",
                "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
                "receipt-2", self.capability.claim_id, "descriptor-digest",
                3, "settlement-event-2", "",
            )
        )
        self.oracle.allowed_head = late.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            event_kind = connection.execute(
                "SELECT event_kind FROM events WHERE event_id = ?",
                (late.event_id,),
            ).fetchone()[0]
            accounting = connection.execute(
                "SELECT charged_units, disposition FROM budget_reservations "
                "WHERE reservation_id = 'reservation-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(event_kind, "LATE_RECEIPT_RECORDED")
        self.assertEqual(
            late.resulting_state, LifecycleState.RECONCILIATION_REQUIRED
        )
        self.assertEqual(accounting, (3, "ADJUSTED"))
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        self.store.load_verified("repo-1")

    def test_t23_terminal_receipt_preserves_completed_and_released_slot(
        self,
    ) -> None:
        request, attestation = self._prepare_finalization()
        finalized = self.store._finalize_operation(
            request, attestation, self.authority
        )
        self.oracle.allowed_head = finalized.event_hash
        late = self.store._record_effect_observation(
            EffectObservationRequest(
                "observation-2", "observe-command-2", "observation-event-2",
                "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
                "receipt-2", self.capability.claim_id, "descriptor-digest",
                3, "settlement-event-2", "",
            )
        )
        self.oracle.allowed_head = late.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            event_kind = connection.execute(
                "SELECT event_kind FROM events WHERE event_id = ?",
                (late.event_id,),
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(event_kind, "LATE_RECEIPT_RECORDED")
        self.assertEqual(late.resulting_state, LifecycleState.COMPLETED)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.store.load_verified("repo-1")

    def test_t19_t23_before_t26_keeps_stop_fence_target_scoped(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        self._stop_run()
        late = self.store._record_effect_observation(
            EffectObservationRequest(
                "late-observation-1", "late-observe-command-1",
                "late-observation-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "attempt-1", "late-receipt-1",
                self.capability.claim_id, "descriptor-digest", 2,
                "late-settlement-1", "",
            )
        )
        self.oracle.allowed_head = late.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            event_kind, plan_id, plan_hash = connection.execute(
                "SELECT event_kind, (SELECT plan_id FROM validation_plans "
                "WHERE run_id = 'run-1'), (SELECT event_hash FROM "
                "validation_plans WHERE run_id = 'run-1') FROM events "
                "WHERE event_id = ?",
                (late.event_id,),
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(event_kind, "LATE_RECEIPT_RECORDED")
        settled = self.store.settle_terminal_validation(
            TerminalValidationSettlementRequest(
                "terminal-settlement-1", "terminal-command-1",
                "terminal-event-1", "repo-1", "run-1", "item-1",
                "effect-1", plan_id, "revision-1", "check-1", "PLAN",
                plan_id, plan_hash, "CANCELLED_WITHOUT_START",
            )
        )
        self.oracle.allowed_head = settled.event_hash
        self.assertTrue(settled.slot_released)

        def prepare_intent(
            suffix: str, item_id: str, logical_effect_id: str
        ):
            grant = SyntheticGrant(
                f"grant-{suffix}", "repo-1", logical_effect_id,
                f"attempt-{suffix}", f"scope-{suffix}",
            )
            self.authority.register(grant)
            capability = self.authority.claim(*grant.__dict__.values())
            plan = self.store.accept_plan(
                PlanAcceptanceRequest(
                    f"plan-{suffix}", f"plan-command-{suffix}",
                    f"plan-event-{suffix}", "repo-1", f"run-{suffix}",
                    item_id, logical_effect_id, f"revision-{suffix}",
                    "descriptor-digest", grant.scope_digest,
                    "budget-policy-digest", (f"check-{suffix}",),
                ),
                expected_head=self.oracle.allowed_head,
                writer_epoch=20 + int(suffix),
            )
            self.oracle.allowed_head = plan.event_hash
            request = replace(
                self.request(), run_id=f"run-{suffix}", item_id=item_id,
                command_id=f"command-{suffix}", event_id=f"event-{suffix}",
                logical_effect_id=logical_effect_id,
                attempt_id=f"attempt-{suffix}",
                permission_use_id=f"permission-use-{suffix}",
                reservation_id=f"reservation-{suffix}",
            )
            return request, capability, plan

        for suffix, item_id, logical_effect_id in (
            ("2", "item-1", "effect-2"),
            ("3", "item-3", "effect-1"),
        ):
            with self.subTest(
                item_id=item_id, logical_effect_id=logical_effect_id
            ):
                request, capability, plan = prepare_intent(
                    suffix, item_id, logical_effect_id
                )
                with self.assertRaisesRegex(
                    DispatchDenied, "active dispatch fence"
                ):
                    self.store.commit_intent(
                        request, capability, self.authority,
                        expected_head=plan.event_hash,
                        writer_epoch=30 + int(suffix),
                    )

        request, capability, plan = prepare_intent("4", "item-4", "effect-4")
        committed = self.store.commit_intent(
            request, capability, self.authority,
            expected_head=plan.event_hash, writer_epoch=34,
        )
        self.oracle.allowed_head = committed.event_hash
        self.assertFalse(committed.replayed)
        self.assertEqual(
            self.store.load_run_lifecycle("run-4"), LifecycleState.RUNNING
        )
        self.store.load_verified("repo-1")

    def test_t19_stop_blocks_new_validator_launch_and_tamper_fails_recovery(
        self,
    ) -> None:
        parent = self._record_effect_observation(check_ids=("check-1",))
        intent, validator_capability = self._validator_intent(parent)
        stopped = self.store.stop(
            self._stop_request(),
            self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        with self.assertRaisesRegex(DispatchDenied, "durable VALIDATING"):
            self.store.commit_validator_intent(
                intent, validator_capability, self.authority
            )
        self.assertEqual(self.store.table_counts()["validator_intents"], 0)

        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE stop_actions SET reason_code = 'TAMPERED' "
                "WHERE stop_id = 'stop-1'"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(StorageIntegrityError, "stop-action"):
            self.store.load_verified("repo-1")

    def test_t04_pause_is_atomic_and_dual_events_are_hash_chained(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        capability = self._pause_capability()
        request = self._pause_request()
        with self.assertRaises(InjectedFailure):
            self.store.pause_before_dispatch(
                request, capability, self.authority,
                failure_hook=raise_at("after_pause_requested_before_settled"),
            )
        counts = self.store.table_counts()
        self.assertEqual(counts["events"], 1)
        self.assertEqual(counts["control_actions"], 0)
        self.assertEqual(counts["operator_redemptions"], 0)
        self.assertEqual(counts["dispatch_fences"], 0)
        self.assertEqual(self.store.load_run_lifecycle("run-1").value, "PLANNED")

        receipt = self.store.pause_before_dispatch(
            request, capability, self.authority
        )
        self.oracle.allowed_head = receipt.event_hash
        self.assertEqual(receipt.resulting_state.value, "PAUSED")
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            rows = connection.execute(
                "SELECT event_id, event_kind, previous_event_hash, event_hash "
                "FROM events WHERE command_id = ? ORDER BY sequence",
                (request.command_id,),
            ).fetchall()
        finally:
            connection.close()
        self.assertEqual(
            [row["event_kind"] for row in rows],
            ["PAUSE_REQUESTED", "PAUSE_SETTLED"],
        )
        self.assertEqual(rows[1]["previous_event_hash"], rows[0]["event_hash"])
        self.store.load_verified("repo-1")

    def test_t04_acknowledgement_loss_replays_and_capability_cannot_rebind(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        capability = self._pause_capability()
        request = self._pause_request()
        with self.assertRaises(InjectedFailure):
            self.store.pause_before_dispatch(
                request, capability, self.authority,
                failure_hook=raise_at("after_pause_commit_before_acknowledgement"),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            committed_hash = connection.execute(
                "SELECT event_hash FROM control_actions WHERE control_id = ?",
                (request.pause_id,),
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = committed_hash
        replay = self.store.pause_before_dispatch(
            request, capability, self.authority
        )
        self.assertTrue(replay.replayed)
        self.assertEqual(replay.event_hash, committed_hash)
        with self.assertRaisesRegex(DispatchDenied, "already redeemed"):
            self.store.pause_before_dispatch(
                self._pause_request("2"), capability, self.authority
            )

    def test_t04_recovery_rejects_tampered_pause_fence(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        receipt = self.store.pause_before_dispatch(
            self._pause_request(), self._pause_capability(), self.authority
        )
        self.oracle.allowed_head = receipt.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE dispatch_fences SET reason_code = 'TAMPERED' "
                "WHERE fence_id = 'pause-fence-1'"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(StorageIntegrityError, "dispatch-fence"):
            self.store.load_verified("repo-1")

    def _validator_intent(
        self,
        observation,
        *,
        suffix: str = "1",
        check_id: str | None = None,
        validator_attempt_id: str | None = None,
        recovery_id: str | None = None,
        cap_units: int = 10,
    ):
        check_id = check_id or f"check-{suffix}"
        validator_attempt_id = validator_attempt_id or f"validator-attempt-{suffix}"
        grant = SyntheticValidatorGrant(
            f"validator-grant-{suffix}",
            "repo-1",
            "effect-1",
            "revision-1",
            check_id,
            "input-1",
            validator_attempt_id,
            f"read-only-scope-{suffix}",
        )
        self.authority.register_validator(grant)
        capability = self.authority.claim_validator(*grant.__dict__.values())
        request = ValidatorIntentRequest(
            f"validator-intent-{suffix}",
            f"validator-command-{suffix}",
            f"validator-event-{suffix}",
            "repo-1",
            "run-1",
            "item-1",
            "effect-1",
            "attempt-1",
            "observation-1",
            observation.event_hash,
            "revision-1",
            check_id,
            "input-1",
            validator_attempt_id,
            f"validator-permission-{suffix}",
            f"validator-reservation-{suffix}",
            "validator-budget-policy-1",
            1,
            2,
            cap_units,
            recovery_id,
        )
        return request, capability

    def _record_validator_result(
        self,
        *,
        verdict: str = "PASS",
        only_check: bool = False,
        aggregate_gate_ids=None,
    ):
        check_ids = ("check-1",) if only_check else ("check-1", "check-2")
        observation = self._record_effect_observation(
            check_ids, aggregate_gate_ids
        )
        return self._record_validator_result_for(
            observation, suffix="1", verdict=verdict
        )

    def _record_validator_result_for(
        self, observation, *, suffix: str, verdict: str = "PASS"
    ):
        intent_request, capability = self._validator_intent(
            observation, suffix=suffix
        )
        intent = self.store.commit_validator_intent(
            intent_request, capability, self.authority
        )
        self.oracle.allowed_head = intent.event_hash
        settlement_request = BudgetSettlementRequest(
            f"validator-settlement-{suffix}",
            f"validator-reservation-{suffix}", "",
            BudgetDisposition.CONSUMED, 1,
            f"validator-result-{suffix}",
            "VALIDATOR_USAGE_REPORTED",
        )
        settlement = self.store._settle_budget(
            settlement_request,
            self.authority.issue_settlement_proof(
                f"validator-proof-{suffix}",
                settlement_request,
            ),
            self.authority,
        )
        self.oracle.allowed_head = settlement.settlement_hash
        recorded = self.store._record_validator_observation(
            ValidatorObservationRequest(
                f"validator-observation-{suffix}",
                f"validator-observe-command-{suffix}",
                f"validator-observation-event-{suffix}",
                "repo-1", "run-1", "item-1", "effect-1",
                f"validator-intent-{suffix}", f"validator-attempt-{suffix}",
                f"validator-result-{suffix}", capability.claim_id,
                "revision-1", f"check-{suffix}", "input-1",
                f"result-digest-{suffix}", verdict, 1,
                f"validator-settlement-{suffix}", settlement.settlement_hash,
            )
        )
        self.oracle.allowed_head = recorded.event_hash
        return recorded

    def _record_validator_cessation_for(
        self, *, suffix: str = "1", result_available: bool = False
    ):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            intent = connection.execute(
                "SELECT * FROM validator_intents WHERE validator_intent_id = ?",
                (f"validator-intent-{suffix}",),
            ).fetchone()
        finally:
            connection.close()
        assert intent is not None
        validator_path = self.database_path.parent / "synthetic-validator.sqlite3"
        adapter = SyntheticValidatorAdapter(validator_path)
        adapter._canonical_repository_id = "repo-1"
        adapter._canonical_ledger_path = validator_path.resolve()
        if result_available:
            connection = sqlite3.connect(validator_path)
            try:
                connection.execute(
                    "INSERT INTO synthetic_validator_results VALUES "
                    "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)",
                    (
                        intent["capability_claim_id"],
                        f"validator-result-{suffix}", "repo-1", "effect-1",
                        "revision-1", f"check-{suffix}", "input-1",
                        f"validator-attempt-{suffix}",
                        f"result-digest-{suffix}", "PASS", 1,
                    ),
                )
                connection.commit()
            finally:
                connection.close()
        attestation = self.authority.issue_validator_cessation_attestation(
            f"cessation-attestation-{suffix}", f"cessation-{suffix}",
            adapter._target_digest("repo-1"), intent["capability_claim_id"],
            f"VALIDATOR:validator-intent-{suffix}", intent["event_hash"],
            "repo-1", "run-1", "item-1", "effect-1", "revision-1",
            f"check-{suffix}", f"validator-attempt-{suffix}",
        )
        seal = adapter.seal_cessation(attestation, self.authority)
        receipt = self.store.record_validator_cessation(
            ValidatorCessationRequest(
                f"cessation-{suffix}", f"cessation-command-{suffix}",
                f"cessation-event-{suffix}", "repo-1", "run-1", "item-1",
                "effect-1", f"validator-intent-{suffix}",
                f"validator-attempt-{suffix}", "revision-1",
                f"check-{suffix}", seal.cessation_hash,
            ),
            self.authority,
        )
        self.oracle.allowed_head = receipt.event_hash
        return receipt

    def _stop_run(self) -> str:
        receipt = self.store.stop(
            self._stop_request(),
            self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = receipt.event_hash
        return receipt.event_hash

    def test_unknown_validator_usage_cannot_be_released_after_result(self) -> None:
        observation = self._record_effect_observation(check_ids=("check-1",))
        intent_request, capability = self._validator_intent(observation)
        intent = self.store.commit_validator_intent(
            intent_request, capability, self.authority
        )
        self.oracle.allowed_head = intent.event_hash
        unknown = BudgetSettlementRequest(
            "validator-settlement-1", "validator-reservation-1", "",
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "validator-result-1", "VALIDATOR_USAGE_UNKNOWN",
        )
        settlement = self.store._settle_budget(
            unknown,
            self.authority.issue_settlement_proof("validator-proof-1", unknown),
            self.authority,
        )
        self.oracle.allowed_head = settlement.settlement_hash
        recorded = self.store._record_validator_observation(
            ValidatorObservationRequest(
                "validator-observation-1", "validator-observe-command-1",
                "validator-observation-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "validator-intent-1", "validator-attempt-1",
                "validator-result-1", capability.claim_id, "revision-1",
                "check-1", "input-1", "result-digest-1", "PASS", None,
                "validator-settlement-1", settlement.settlement_hash,
            )
        )
        self.oracle.allowed_head = recorded.event_hash
        release = BudgetSettlementRequest(
            "validator-release-1", "validator-reservation-1",
            settlement.settlement_hash, BudgetDisposition.RELEASED, None,
            "validator-nondispatch-proof", "NONDISPATCH",
            non_dispatch_proven=True, zero_liability_proven=True,
        )

        with self.assertRaisesRegex(
            DispatchDenied, "cannot release liability"
        ):
            self.store._settle_budget(
                release,
                self.authority.issue_settlement_proof(
                    "validator-release-proof-1", release
                ),
                self.authority,
            )
        self.assertEqual(self.store.table_counts()["budget_settlements"], 2)

    def test_recovery_rejects_validator_unknown_usage_state_suppression(
        self,
    ) -> None:
        observation = self._record_effect_observation(check_ids=("check-1",))
        intent_request, capability = self._validator_intent(observation)
        intent = self.store.commit_validator_intent(
            intent_request, capability, self.authority
        )
        self.oracle.allowed_head = intent.event_hash
        unknown = BudgetSettlementRequest(
            "validator-settlement-1", "validator-reservation-1", "",
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "validator-result-1", "VALIDATOR_USAGE_UNKNOWN",
        )
        settlement = self.store._settle_budget(
            unknown,
            self.authority.issue_settlement_proof(
                "validator-proof-1", unknown
            ),
            self.authority,
        )
        self.oracle.allowed_head = settlement.settlement_hash
        recorded = self.store._record_validator_observation(
            ValidatorObservationRequest(
                "validator-observation-1", "validator-observe-command-1",
                "validator-observation-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "validator-intent-1", "validator-attempt-1",
                "validator-result-1", capability.claim_id, "revision-1",
                "check-1", "input-1", "result-digest-1", "PASS", None,
                "validator-settlement-1", settlement.settlement_hash,
            )
        )
        self.assertEqual(
            recorded.resulting_state, LifecycleState.RECONCILIATION_REQUIRED
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    (recorded.event_id,),
                ).fetchone()[0]
            )
            body["lifecycle_to"] = LifecycleState.VALIDATING.value
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (event_hash, body_json, recorded.event_id),
            )
            connection.execute(
                "UPDATE validator_observations SET event_hash = ?, "
                "resulting_state = ?, body_json = ? WHERE observation_id = ?",
                (
                    event_hash, LifecycleState.VALIDATING.value, body_json,
                    recorded.observation_id,
                ),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                (event_hash, recorded.command_id),
            )
            connection.execute(
                "UPDATE runs SET lifecycle_state = ?, head_hash = ? WHERE run_id = ?",
                (LifecycleState.VALIDATING.value, event_hash, "run-1"),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, "repo-1"),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(
            StorageIntegrityError, "validator observation semantics"
        ):
            self.store.load_verified("repo-1")

    def _classification(self, observation, classification: str):
        return self.authority.issue_classification(
            f"classification-{classification.lower()}", "repo-1", "run-1",
            "item-1", "effect-1", "revision-1", "check-1",
            "validator-attempt-1", "validator-observation-1",
            observation.event_hash, "result-digest-1", verdict="FAIL",
            policy_id="failure-policy", policy_version="1",
            classification=classification,
        )

    def _prepare_recoverable_application(self):
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        failed = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1", "validator-observation-1",
            ),
            classification=self._classification(observation, "RECOVERABLE"),
        )
        self.oracle.allowed_head = failed.event_hash
        return observation, failed

    def _validation_recovery_pair(
        self,
        failed,
        *,
        suffix: str = "1",
        expected_run_head: str | None = None,
        successor_validator_attempt_id: str = "validator-attempt-2",
    ):
        recovery_id = f"recovery-{suffix}"
        request = ValidationRecoveryRequest(
            recovery_id, f"recovery-command-{suffix}",
            f"recovery-event-{suffix}", "repo-1", "run-1", "item-1",
            "effect-1", "plan-1", "revision-1", "check-1",
            "application-1", "validator-attempt-1",
            successor_validator_attempt_id,
            f"remediation-evidence-{suffix}",
            expected_run_head or failed.event_hash, "attempt-1", 1,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            plan_event_hash = connection.execute(
                "SELECT event_hash FROM validation_plans WHERE plan_id = 'plan-1'"
            ).fetchone()[0]
            parent_event_hash = connection.execute(
                "SELECT event_hash FROM effect_observations "
                "WHERE observation_id = 'observation-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        attestation = self.authority.issue_validation_recovery_attestation(
            f"recovery-attestation-{suffix}", request.recovery_id,
            request.repository_id, request.run_id, request.item_id,
            request.logical_effect_id, request.plan_id, plan_event_hash,
            request.revision_digest, request.check_id,
            request.failed_application_id, failed.event_hash,
            request.failed_validator_attempt_id,
            request.successor_validator_attempt_id,
            request.remediation_evidence_digest, request.expected_run_head,
            request.expected_slot_attempt_id, request.expected_slot_generation,
        )
        return request, attestation, parent_event_hash

    def _prepare_finalization(
        self, *, aggregate_gate_ids=None
    ):
        self._record_validator_result(
            only_check=True, aggregate_gate_ids=aggregate_gate_ids
        )
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1", "check-1",
                "validator-attempt-1", "validator-observation-1",
            ),
        )
        self.oracle.allowed_head = applied.event_hash
        return self._finalization_request_and_attestation(applied.event_hash)

    def _finalization_request_and_attestation(self, evaluated_run_head: str):
        request = FinalizeOperationRequest(
            "finalization-1", "finalize-command-1", "finalize-event-1",
            "repo-1", "run-1", "item-1", "effect-1", "plan-1",
            "revision-1", "attempt-1", 1,
        )
        finalization_key = self.store.finalization_key(
            "repo-1", "run-1", "item-1", "effect-1", "plan-1", "revision-1"
        )
        connection = sqlite3.connect(self.database_path)
        try:
            plan_event_hash, gate_set_digest = connection.execute(
                "SELECT event_hash, gate_set_digest FROM validation_plans "
                "WHERE plan_id = 'plan-1'"
            ).fetchone()
        finally:
            connection.close()
        attestation = self.authority.issue_finalization_attestation(
            "attestation-1", "repo-1", "run-1", "item-1", "effect-1",
            "plan-1", plan_event_hash, "revision-1", evaluated_run_head,
            finalization_key, gate_set_digest, "attempt-1", 1,
        )
        return request, attestation

    def _reissue_finalization_attestation(self, attestation, **changes):
        values = {
            name: getattr(attestation, name)
            for name in attestation.__dataclass_fields__
            if name != "issuer_mac"
        }
        values.update(changes)
        return self.authority.issue_finalization_attestation(**values)

    def test_c05_pass_application_is_atomic_replay_safe_and_retains_slot(self) -> None:
        self._record_validator_result()
        request = ValidationApplicationRequest(
            "application-1", "apply-command-1", "apply-event-1", "repo-1",
            "run-1", "item-1", "effect-1", "revision-1", "check-1",
            "validator-attempt-1", "validator-observation-1",
        )
        with self.assertRaises(InjectedFailure):
            self.store._apply_validator_observation(
                request,
                failure_hook=raise_at(
                    "after_validation_application_writes_before_commit"
                ),
            )
        self.assertEqual(self.store.table_counts()["validation_applications"], 0)
        with self.assertRaises(InjectedFailure):
            self.store._apply_validator_observation(
                request,
                failure_hook=raise_at(
                    "after_validation_application_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            event_hash = connection.execute(
                "SELECT event_hash FROM validation_applications WHERE application_id = 'application-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash
        replay = self.store._apply_validator_observation(
            request
        )
        self.assertTrue(replay.replayed)
        self.assertEqual(replay.resulting_state.value, "VALIDATING")
        self.assertEqual(self.store.table_counts()["validation_applications"], 1)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        self.store.load_verified("repo-1")

    def test_c05_last_pass_blocks_for_distinct_finalization(self) -> None:
        self._record_validator_result(only_check=True)
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1", "check-1",
                "validator-attempt-1", "validator-observation-1",
            ),
        )
        self.assertEqual(applied.resulting_state.value, "BLOCKED")
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        connection = sqlite3.connect(self.database_path)
        try:
            cursor = connection.execute(
                "SELECT continuation_cursor FROM validation_applications "
                "WHERE application_id = 'application-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(cursor, "FINALIZING")

    def _terminal_application_request(
        self, disposition: str
    ) -> TerminalValidationSettlementRequest:
        connection = sqlite3.connect(self.database_path)
        try:
            application_hash = connection.execute(
                "SELECT event_hash FROM validation_applications "
                "WHERE application_id = 'application-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        return TerminalValidationSettlementRequest(
            "terminal-settlement-1", "terminal-command-1",
            "terminal-event-1", "repo-1", "run-1", "item-1",
            "effect-1", "plan-1", "revision-1", "check-1",
            "VALIDATION_APPLICATION", "application-1", application_hash,
            disposition, "validator-intent-1", "validator-attempt-1",
        )

    def _assert_r_stop_01_application_closure(
        self, *, verdict: str, mode: StopMode
    ) -> None:
        if verdict == "PASS":
            self._prepare_finalization()
            expected_cursor = "FINALIZING"
            disposition = "PASSED"
        else:
            self._prepare_recoverable_application()
            expected_cursor = LifecycleState.VALIDATING.value
            disposition = "FAILED"
        stopped = self.store.stop(
            self._stop_request(mode),
            self._stop_capability(mode),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        connection = sqlite3.connect(self.database_path)
        try:
            run_cursor, retained_cursor = connection.execute(
                "SELECT run.continuation_cursor, stop.retained_continuation_cursor "
                "FROM runs AS run JOIN stop_actions AS stop ON "
                "stop.run_id = run.run_id WHERE run.run_id = 'run-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(run_cursor, expected_cursor)
        self.assertEqual(retained_cursor, expected_cursor)

        second_grant = SyntheticGrant(
            "grant-2", "repo-1", "effect-2", "attempt-2", "scope-2"
        )
        self.authority.register(second_grant)
        second_capability = self.authority.claim(
            *second_grant.__dict__.values()
        )
        second_plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-2", "plan-command-2", "plan-event-2", "repo-1",
                "run-2", "item-2", "effect-2", "revision-2",
                "descriptor-digest", "scope-2", "budget-policy-digest",
                ("check-2",),
            ),
            expected_head=stopped.event_hash,
            writer_epoch=40,
        )
        self.oracle.allowed_head = second_plan.event_hash
        second_request = replace(
            self.request(), run_id="run-2", item_id="item-2",
            command_id="command-2", event_id="event-2",
            logical_effect_id="effect-2", attempt_id="attempt-2",
            permission_use_id="permission-use-2",
            reservation_id="reservation-2",
        )
        with self.assertRaisesRegex(DispatchDenied, "repository slot"):
            self.store.commit_intent(
                second_request, second_capability, self.authority,
                expected_head=second_plan.event_hash, writer_epoch=41,
            )

        settled = self.store.settle_terminal_validation(
            self._terminal_application_request(disposition)
        )
        self.assertEqual(settled.resulting_state, LifecycleState.STOPPED)
        self.assertTrue(settled.slot_released)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.oracle.allowed_head = settled.event_hash
        self.store.load_verified("repo-1")
        committed = self.store.commit_intent(
            second_request, second_capability, self.authority,
            expected_head=settled.event_hash, writer_epoch=42,
        )
        self.oracle.allowed_head = committed.event_hash
        replay = self.store.commit_intent(
            second_request, second_capability, self.authority,
            expected_head=committed.event_hash, writer_epoch=43,
        )
        self.assertTrue(replay.replayed)
        self.assertEqual(replay.event_hash, committed.event_hash)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

    def test_r_stop_03_immediate_stop_charges_contacted_unknown(self) -> None:
        request = self.request()
        committed = self._commit_planned_intent(
            request, self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        launched = self.store.claim_operation_launch(request, committed)
        self.oracle.allowed_head = launched.event_hash
        self.store._contact_claimed_operation(
            request, self.capability, committed, launched,
            self.store._adapter_target_digest("repo-1", "EFFECT"),
        )
        connection = sqlite3.connect(self.database_path)
        try:
            contact_hash = connection.execute(
                "SELECT event_hash FROM adapter_contacts WHERE "
                "contact_kind = 'EFFECT'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = contact_hash

        stopped = self.store.stop(
            self._stop_request(),
            self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            accounting = connection.execute(
                "SELECT held_units, charged_units, uncertainty, disposition "
                "FROM budget_reservations WHERE reservation_id = ?",
                ("reservation-1",),
            ).fetchone()
            stop_body = json.loads(connection.execute(
                "SELECT body_json FROM stop_actions WHERE stop_id = 'stop-1'"
            ).fetchone()[0])
            epoch_rows = connection.execute(
                "SELECT event_kind, event_id, sequence FROM events WHERE "
                "writer_epoch = ? ORDER BY rowid",
                (stop_body["writer_epoch"],),
            ).fetchall()
        finally:
            connection.close()
        self.assertEqual(
            accounting,
            (0, 5, 1, BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value),
        )
        self.assertEqual(
            epoch_rows,
            [
                (
                    "BUDGET_SETTLED",
                    stop_body["uncertainty_snapshot"][0]["settlement_event_id"],
                    stop_body["sequence"] - 1,
                ),
                ("STOP_RECORDED", "stop-event-1", stop_body["sequence"]),
            ],
        )
        self.store.load_verified("repo-1")

    def test_r_stop_03_precontact_stop_retains_reserve(self) -> None:
        request = self.request()
        committed = self._commit_planned_intent(
            request, self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        launched = self.store.claim_operation_launch(request, committed)
        self.oracle.allowed_head = launched.event_hash
        stopped = self.store.stop(
            self._stop_request(), self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            accounting = connection.execute(
                "SELECT held_units, charged_units, disposition FROM "
                "budget_reservations WHERE reservation_id = 'reservation-1'"
            ).fetchone()
            body = json.loads(connection.execute(
                "SELECT body_json FROM stop_actions WHERE stop_id = 'stop-1'"
            ).fetchone()[0])
        finally:
            connection.close()
        self.assertEqual(accounting, (3, 0, BudgetDisposition.RESERVED.value))
        self.assertEqual(body["uncertainty_snapshot"], [])
        self.store.load_verified("repo-1")

    def test_r_stop_03_crash_boundaries_replay_exactly_once(self) -> None:
        request = self.request()
        committed = self._commit_planned_intent(
            request, self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        launched = self.store.claim_operation_launch(request, committed)
        self.oracle.allowed_head = launched.event_hash
        self.store._contact_claimed_operation(
            request, self.capability, committed, launched,
            self.store._adapter_target_digest("repo-1", "EFFECT"),
        )
        connection = sqlite3.connect(self.database_path)
        try:
            self.oracle.allowed_head = connection.execute(
                "SELECT event_hash FROM adapter_contacts WHERE "
                "contact_kind = 'EFFECT'"
            ).fetchone()[0]
        finally:
            connection.close()
        stop_request = self._stop_request()
        capability = self._stop_capability(StopMode.IMMEDIATE)
        for point in (
            "after_stop_unknown_settlement_before_stop_recorded",
            "after_stop_writes_before_commit",
        ):
            with self.assertRaises(InjectedFailure):
                self.store.stop(
                    stop_request, capability, self.authority,
                    failure_hook=raise_at(point),
                )
            self.assertEqual(self.store.table_counts()["stop_actions"], 0)
            self.assertEqual(self.store.table_counts()["budget_settlements"], 0)
        with self.assertRaises(InjectedFailure):
            self.store.stop(
                stop_request, capability, self.authority,
                failure_hook=raise_at(
                    "after_stop_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            stop_hash = connection.execute(
                "SELECT event_hash FROM stop_actions WHERE stop_id = 'stop-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = stop_hash
        replay = self.store.stop(stop_request, capability, self.authority)
        self.assertTrue(replay.replayed)
        self.assertEqual(self.store.table_counts()["stop_actions"], 1)
        self.assertEqual(self.store.table_counts()["budget_settlements"], 1)
        self.store.load_verified("repo-1")

    def test_r_stop_03_recovery_rejects_snapshot_retarget(self) -> None:
        request = self.request()
        committed = self._commit_planned_intent(
            request, self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        launched = self.store.claim_operation_launch(request, committed)
        self.oracle.allowed_head = launched.event_hash
        self.store._contact_claimed_operation(
            request, self.capability, committed, launched,
            self.store._adapter_target_digest("repo-1", "EFFECT"),
        )
        connection = sqlite3.connect(self.database_path)
        try:
            self.oracle.allowed_head = connection.execute(
                "SELECT event_hash FROM adapter_contacts WHERE "
                "contact_kind = 'EFFECT'"
            ).fetchone()[0]
        finally:
            connection.close()
        stopped = self.store.stop(
            self._stop_request(), self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(connection.execute(
                "SELECT body_json FROM stop_actions WHERE stop_id = 'stop-1'"
            ).fetchone()[0])
            body["uncertainty_snapshot"][0]["contact_id"] = "forged-contact"
            forged_hash = self.store._event_hash(body)
            body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                "event_id = 'stop-event-1'", (forged_hash, body_json)
            )
            connection.execute(
                "UPDATE stop_actions SET event_hash = ?, body_json = ? WHERE "
                "stop_id = 'stop-1'", (forged_hash, body_json)
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE "
                "command_id = 'stop-command-1'", (forged_hash,)
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (forged_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE "
                "repository_id = 'repo-1'", (forged_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = forged_hash
        with self.assertRaises(StorageIntegrityError):
            self.store.load_verified("repo-1")

    def test_r_stop_03_validator_contact_is_unknown_but_known_effect_retained(
        self,
    ) -> None:
        observation = self._record_effect_observation(check_ids=("check-1",))
        request, capability = self._validator_intent(observation)
        committed = self.store.commit_validator_intent(
            request, capability, self.authority
        )
        self.oracle.allowed_head = committed.event_hash
        self.store._contact_committed_validator(
            request, capability, committed,
            self.store._adapter_target_digest("repo-1", "VALIDATOR"),
            self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            self.oracle.allowed_head = connection.execute(
                "SELECT event_hash FROM adapter_contacts WHERE "
                "contact_kind = 'VALIDATOR'"
            ).fetchone()[0]
        finally:
            connection.close()
        stopped = self.store.stop(
            self._stop_request(), self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            accounting = connection.execute(
                "SELECT reservation_id, disposition, charged_units FROM "
                "budget_reservations ORDER BY reservation_id"
            ).fetchall()
            body = json.loads(connection.execute(
                "SELECT body_json FROM stop_actions WHERE stop_id = 'stop-1'"
            ).fetchone()[0])
        finally:
            connection.close()
        self.assertEqual(accounting[0][1], BudgetDisposition.CONSUMED.value)
        self.assertEqual(
            accounting[1],
            (
                "validator-reservation-1",
                BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value,
                2,
            ),
        )
        self.assertEqual(
            body["uncertainty_snapshot"][0]["contact_kind"], "VALIDATOR"
        )
        self.store.load_verified("repo-1")

    def test_r_stop_03_late_authoritative_usage_adjusts_without_reopen(self) -> None:
        request = self.request()
        committed = self._commit_planned_intent(
            request, self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        launched = self.store.claim_operation_launch(request, committed)
        self.oracle.allowed_head = launched.event_hash
        self.store._contact_claimed_operation(
            request, self.capability, committed, launched,
            self.store._adapter_target_digest("repo-1", "EFFECT"),
        )
        connection = sqlite3.connect(self.database_path)
        try:
            self.oracle.allowed_head = connection.execute(
                "SELECT event_hash FROM adapter_contacts WHERE "
                "contact_kind = 'EFFECT'"
            ).fetchone()[0]
        finally:
            connection.close()
        stopped = self.store.stop(
            self._stop_request(), self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            unknown_hash = connection.execute(
                "SELECT settlement_head_hash FROM budget_reservations WHERE "
                "reservation_id = 'reservation-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        adjustment = BudgetSettlementRequest(
            "late-stop-adjustment-1", "reservation-1", unknown_hash,
            BudgetDisposition.ADJUSTED, 2, "late-authoritative-bill-1",
            "AUTHORITATIVE_LATE_USAGE",
        )
        adjusted = self.store._settle_budget(
            adjustment,
            self.authority.issue_settlement_proof(
                "late-stop-adjustment-proof-1", adjustment
            ),
            self.authority,
        )
        self.oracle.allowed_head = adjusted.settlement_hash
        self.assertEqual(
            self.store.load_run_lifecycle("run-1"), LifecycleState.STOPPED
        )
        connection = sqlite3.connect(self.database_path)
        try:
            accounting = connection.execute(
                "SELECT charged_units, uncertainty, disposition FROM "
                "budget_reservations WHERE reservation_id = 'reservation-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(accounting, (2, 0, BudgetDisposition.ADJUSTED.value))
        reopened = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        )
        reopened.load_verified("repo-1")

    def test_r_stop_03_reused_attempt_on_other_run_cannot_hide_contact(
        self,
    ) -> None:
        self._prepare_finalization()
        stopped_1 = self.store.stop(
            self._stop_request(), self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped_1.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            first_stop_body = json.loads(connection.execute(
                "SELECT body_json FROM stop_actions WHERE stop_id = 'stop-1'"
            ).fetchone()[0])
            first_disposition = connection.execute(
                "SELECT disposition FROM budget_reservations WHERE "
                "reservation_id = 'reservation-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(first_stop_body["uncertainty_snapshot"], [])
        self.assertEqual(first_disposition, BudgetDisposition.CONSUMED.value)
        closed = self.store.settle_terminal_validation(
            self._terminal_application_request("PASSED")
        )
        self.oracle.allowed_head = closed.event_hash
        plan_2 = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-2", "plan-command-2", "plan-event-2", "repo-1",
                "run-2", "item-2", "effect-2", "revision-2",
                "descriptor-2", "scope-2", "budget-policy-2", ("check-2",),
            ),
            expected_head=closed.event_hash, writer_epoch=90,
        )
        self.oracle.allowed_head = plan_2.event_hash
        grant_2 = SyntheticGrant(
            "grant-2", "repo-1", "effect-2", "attempt-1", "scope-2"
        )
        self.authority.register(grant_2)
        capability_2 = self.authority.claim(*grant_2.__dict__.values())
        request_2 = replace(
            self.request(), run_id="run-2", item_id="item-2",
            command_id="command-2", event_id="event-2",
            logical_effect_id="effect-2", permission_use_id="permission-use-2",
            reservation_id="reservation-2", effect_descriptor_digest="descriptor-2",
            budget_policy_digest="budget-policy-2",
        )
        committed_2 = self.store.commit_intent(
            request_2, capability_2, self.authority,
            expected_head=plan_2.event_hash, writer_epoch=91,
        )
        self.oracle.allowed_head = committed_2.event_hash
        launched_2 = self.store.claim_operation_launch(request_2, committed_2)
        self.oracle.allowed_head = launched_2.event_hash
        self.store._contact_claimed_operation(
            request_2, capability_2, committed_2, launched_2,
            self.store._adapter_target_digest("repo-1", "EFFECT"),
        )
        connection = sqlite3.connect(self.database_path)
        try:
            self.oracle.allowed_head = connection.execute(
                "SELECT event_hash FROM adapter_contacts WHERE run_id = 'run-2'"
            ).fetchone()[0]
        finally:
            connection.close()
        stop_2 = replace(
            self._stop_request(StopMode.IMMEDIATE, "2"), run_id="run-2"
        )
        stop_grant_2 = SyntheticOperatorGrant(
            "stop-grant-2", "repo-1", "run-2", "STOP_IMMEDIATE",
            "stop-scope-2",
        )
        self.authority.register_operator(stop_grant_2)
        stopped_2 = self.store.stop(
            stop_2,
            self.authority.claim_operator(*stop_grant_2.__dict__.values()),
            self.authority,
        )
        self.oracle.allowed_head = stopped_2.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            disposition = connection.execute(
                "SELECT disposition FROM budget_reservations WHERE "
                "reservation_id = 'reservation-2'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(
            disposition, BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value
        )
        self.store.load_verified("repo-1")

    def test_t20_escalation_atomically_charges_unknown_and_replays(self) -> None:
        request = self.request()
        committed = self._commit_planned_intent(
            request, self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        launched = self.store.claim_operation_launch(request, committed)
        self.oracle.allowed_head = launched.event_hash
        graceful_request = replace(
            self._stop_request(StopMode.GRACEFUL),
            drain_deadline_utc="2000-01-01T00:00:00Z",
        )
        stopped = self.store.stop(
            graceful_request,
            self._stop_capability(StopMode.GRACEFUL),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        escalation_request = StopEscalationRequest(
            "escalation-1", "escalation-command-1", "escalation-event-1",
            "repo-1", "run-1", graceful_request.stop_id,
            graceful_request.event_id,
            graceful_request.drain_deadline_utc,
            "GRACEFUL_DEADLINE_EXPIRED",
            (
                StopEscalationSettlement(
                    "reservation-1", "escalation-settlement-event-1", ""
                ),
            ),
        )
        capability = self._stop_escalation_capability()

        escalated = self.store.escalate_stop(
            escalation_request, capability, self.authority
        )
        self.oracle.allowed_head = escalated.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            accounting = connection.execute(
                "SELECT held_units, charged_units, uncertainty, disposition "
                "FROM budget_reservations WHERE reservation_id = ?",
                ("reservation-1",),
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(
            accounting,
            (0, 5, 1, BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value),
        )
        self.assertEqual(escalated.resulting_state, LifecycleState.STOPPED)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        replay = self.store.escalate_stop(
            escalation_request, capability, self.authority
        )
        self.assertTrue(replay.replayed)
        self.assertEqual(replay.event_hash, escalated.event_hash)
        self.assertEqual(self.store.table_counts()["budget_settlements"], 1)
        self.store.load_verified("repo-1")

    def test_t20_crash_boundaries_are_atomic_and_exactly_once(self) -> None:
        request = self.request()
        committed = self._commit_planned_intent(
            request, self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        launched = self.store.claim_operation_launch(request, committed)
        self.oracle.allowed_head = launched.event_hash
        graceful = replace(
            self._stop_request(StopMode.GRACEFUL),
            drain_deadline_utc="2000-01-01T00:00:00Z",
        )
        stopped = self.store.stop(
            graceful, self._stop_capability(StopMode.GRACEFUL), self.authority
        )
        self.oracle.allowed_head = stopped.event_hash
        escalation = StopEscalationRequest(
            "escalation-1", "escalation-command-1", "escalation-event-1",
            "repo-1", "run-1", graceful.stop_id, graceful.event_id,
            graceful.drain_deadline_utc, "GRACEFUL_DEADLINE_EXPIRED",
            (StopEscalationSettlement(
                "reservation-1", "escalation-settlement-event-1", ""
            ),),
        )
        capability = self._stop_escalation_capability()

        with self.assertRaises(InjectedFailure):
            self.store.escalate_stop(
                escalation, capability, self.authority,
                failure_hook=raise_at(
                    "after_stop_escalation_writes_before_commit"
                ),
            )
        self.assertEqual(self.store.table_counts()["stop_escalations"], 0)
        self.assertEqual(self.store.table_counts()["budget_settlements"], 0)
        connection = sqlite3.connect(self.database_path)
        try:
            self.assertEqual(
                connection.execute(
                    "SELECT disposition FROM budget_reservations WHERE "
                    "reservation_id = 'reservation-1'"
                ).fetchone()[0],
                BudgetDisposition.RESERVED.value,
            )
        finally:
            connection.close()

        with self.assertRaises(InjectedFailure):
            self.store.escalate_stop(
                escalation, capability, self.authority,
                failure_hook=raise_at(
                    "after_stop_escalation_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            escalation_hash = connection.execute(
                "SELECT event_hash FROM stop_escalations WHERE "
                "escalation_id = 'escalation-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = escalation_hash
        replay = self.store.escalate_stop(
            escalation, capability, self.authority
        )
        self.assertTrue(replay.replayed)
        self.assertEqual(self.store.table_counts()["stop_escalations"], 1)
        self.assertEqual(self.store.table_counts()["budget_settlements"], 1)
        self.assertEqual(self.store.table_counts()["operator_redemptions"], 2)
        self.store.load_verified("repo-1")

    def test_t20_denies_predeadline_immediate_and_no_activity(self) -> None:
        request = self.request()
        committed = self._commit_planned_intent(
            request, self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        launched = self.store.claim_operation_launch(request, committed)
        self.oracle.allowed_head = launched.event_hash
        graceful = self._stop_request(StopMode.GRACEFUL)
        stopped = self.store.stop(
            graceful, self._stop_capability(StopMode.GRACEFUL), self.authority
        )
        self.oracle.allowed_head = stopped.event_hash
        escalation = StopEscalationRequest(
            "escalation-1", "escalation-command-1", "escalation-event-1",
            "repo-1", "run-1", graceful.stop_id, graceful.event_id,
            graceful.drain_deadline_utc, "GRACEFUL_DEADLINE_EXPIRED",
            (StopEscalationSettlement(
                "reservation-1", "escalation-settlement-event-1", ""
            ),),
        )
        with self.assertRaisesRegex(DispatchDenied, "has not expired"):
            self.store.escalate_stop(
                escalation, self._stop_escalation_capability(), self.authority
            )

        with tempfile.TemporaryDirectory() as directory:
            oracle = MutableFreshnessOracle()
            store = SQLiteStateStore(
                Path(directory) / "state.sqlite3", oracle, "repo-1"
            )
            authority = SyntheticAuthority()
            store._bind_classification_authority(authority)
            plan = store.accept_plan(
                PlanAcceptanceRequest(
                    "plan-x", "plan-command-x", "plan-event-x", "repo-1",
                    "run-x", "item-x", "effect-x", "revision-x",
                    "descriptor-x", "scope-x", "budget-x", ("check-x",),
                ),
                expected_head="", writer_epoch=1,
            )
            oracle.allowed_head = plan.event_hash
            stop_grant = SyntheticOperatorGrant(
                "stop-grant-x", "repo-1", "run-x", "STOP_GRACEFUL",
                "stop-scope-x",
            )
            authority.register_operator(stop_grant)
            stop_capability = authority.claim_operator(
                *stop_grant.__dict__.values()
            )
            no_activity_stop = StopRequest(
                "stop-x", "stop-command-x", "stop-event-x", "repo-1",
                "run-x", StopMode.GRACEFUL, "OPERATOR_STOP",
                "2000-01-01T00:00:00Z",
            )
            stopped_x = store.stop(
                no_activity_stop, stop_capability, authority
            )
            oracle.allowed_head = stopped_x.event_hash
            escalation_grant = SyntheticOperatorGrant(
                "escalation-grant-x", "repo-1", "run-x", "STOP_ESCALATE",
                "escalation-scope-x",
            )
            authority.register_operator(escalation_grant)
            escalation_capability = authority.claim_operator(
                *escalation_grant.__dict__.values()
            )
            with self.assertRaisesRegex(DispatchDenied, "drain obligations"):
                store.escalate_stop(
                    StopEscalationRequest(
                        "escalation-x", "escalation-command-x",
                        "escalation-event-x", "repo-1", "run-x", "stop-x",
                        "stop-event-x", "2000-01-01T00:00:00Z",
                        "GRACEFUL_DEADLINE_EXPIRED",
                    ),
                    escalation_capability,
                    authority,
                )

    def test_t20_retains_known_and_existing_unknown_accounting(self) -> None:
        observation = self._record_effect_observation(check_ids=("check-1",))
        intent_request, validator_capability = self._validator_intent(observation)
        intent = self.store.commit_validator_intent(
            intent_request, validator_capability, self.authority
        )
        self.oracle.allowed_head = intent.event_hash
        unknown = BudgetSettlementRequest(
            "validator-unknown-1", "validator-reservation-1", "",
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "deadline-unknown", "VALIDATOR_DRAIN_UNKNOWN",
        )
        settled = self.store._settle_budget(
            unknown,
            self.authority.issue_settlement_proof("validator-proof-1", unknown),
            self.authority,
        )
        self.oracle.allowed_head = settled.settlement_hash
        graceful = replace(
            self._stop_request(StopMode.GRACEFUL),
            drain_deadline_utc="2000-01-01T00:00:00Z",
        )
        stopped = self.store.stop(
            graceful, self._stop_capability(StopMode.GRACEFUL), self.authority
        )
        self.oracle.allowed_head = stopped.event_hash
        escalated = self.store.escalate_stop(
            StopEscalationRequest(
                "escalation-1", "escalation-command-1",
                "escalation-event-1", "repo-1", "run-1", graceful.stop_id,
                graceful.event_id, graceful.drain_deadline_utc,
                "GRACEFUL_DEADLINE_EXPIRED",
            ),
            self._stop_escalation_capability(),
            self.authority,
        )
        self.oracle.allowed_head = escalated.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            accounting = connection.execute(
                "SELECT reservation_id, disposition, charged_units, "
                "settlement_head_hash FROM budget_reservations ORDER BY "
                "reservation_id"
            ).fetchall()
        finally:
            connection.close()
        self.assertEqual(len(accounting), 2)
        self.assertEqual(accounting[0][1], BudgetDisposition.CONSUMED.value)
        self.assertEqual(
            accounting[1],
            (
                "validator-reservation-1",
                BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value,
                2,
                settled.settlement_hash,
            ),
        )
        self.assertEqual(self.store.table_counts()["budget_settlements"], 2)
        self.store.load_verified("repo-1")

    def test_t20_history_survives_later_adjustment_release_and_restart(self) -> None:
        request = self.request()
        committed = self._commit_planned_intent(
            request, self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        launched = self.store.claim_operation_launch(request, committed)
        self.oracle.allowed_head = launched.event_hash
        graceful = replace(
            self._stop_request(StopMode.GRACEFUL),
            drain_deadline_utc="2000-01-01T00:00:00Z",
        )
        stopped = self.store.stop(
            graceful, self._stop_capability(StopMode.GRACEFUL), self.authority
        )
        self.oracle.allowed_head = stopped.event_hash
        escalated = self.store.escalate_stop(
            StopEscalationRequest(
                "escalation-1", "escalation-command-1",
                "escalation-event-1", "repo-1", "run-1", graceful.stop_id,
                graceful.event_id, graceful.drain_deadline_utc,
                "GRACEFUL_DEADLINE_EXPIRED",
                (StopEscalationSettlement(
                    "reservation-1", "escalation-settlement-event-1", ""
                ),),
            ),
            self._stop_escalation_capability(), self.authority,
        )
        self.oracle.allowed_head = escalated.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            unknown_hash = connection.execute(
                "SELECT settlement_head_hash FROM budget_reservations WHERE "
                "reservation_id = 'reservation-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        adjustment_request = BudgetSettlementRequest(
            "late-adjustment-event-1", "reservation-1", unknown_hash,
            BudgetDisposition.ADJUSTED, 2, "late-receipt-1",
            "AUTHORITATIVE_LATE_USAGE",
        )
        adjusted = self.store._settle_budget(
            adjustment_request,
            self.authority.issue_settlement_proof(
                "late-adjustment-proof-1", adjustment_request
            ),
            self.authority,
        )
        self.oracle.allowed_head = adjusted.settlement_hash
        late = self.store._record_effect_observation(
            EffectObservationRequest(
                "late-observation-1", "late-observe-command-1",
                "late-observation-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "attempt-1", "late-receipt-1",
                self.capability.claim_id, "descriptor-digest", 2,
                "late-adjustment-event-1", adjusted.settlement_hash,
            )
        )
        self.oracle.allowed_head = late.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            plan_id, plan_hash = connection.execute(
                "SELECT plan_id, event_hash FROM validation_plans WHERE "
                "run_id = 'run-1'"
            ).fetchone()
        finally:
            connection.close()
        terminal = self.store.settle_terminal_validation(
            TerminalValidationSettlementRequest(
                "terminal-settlement-1", "terminal-command-1",
                "terminal-event-1", "repo-1", "run-1", "item-1",
                "effect-1", plan_id, "revision-1", "check-1", "PLAN",
                plan_id, plan_hash, "CANCELLED_WITHOUT_START",
            )
        )
        self.assertTrue(terminal.slot_released)
        self.oracle.allowed_head = terminal.event_hash
        reopened = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        )
        reopened.load_verified("repo-1")

    def test_t20_recovery_rejects_self_consistent_snapshot_tamper(self) -> None:
        request = self.request()
        committed = self._commit_planned_intent(
            request, self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        launched = self.store.claim_operation_launch(request, committed)
        self.oracle.allowed_head = launched.event_hash
        graceful = replace(
            self._stop_request(StopMode.GRACEFUL),
            drain_deadline_utc="2000-01-01T00:00:00Z",
        )
        stopped = self.store.stop(
            graceful, self._stop_capability(StopMode.GRACEFUL), self.authority
        )
        self.oracle.allowed_head = stopped.event_hash
        escalated = self.store.escalate_stop(
            StopEscalationRequest(
                "escalation-1", "escalation-command-1",
                "escalation-event-1", "repo-1", "run-1", graceful.stop_id,
                graceful.event_id, graceful.drain_deadline_utc,
                "GRACEFUL_DEADLINE_EXPIRED",
                (StopEscalationSettlement(
                    "reservation-1", "escalation-settlement-event-1", ""
                ),),
            ),
            self._stop_escalation_capability(), self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM stop_escalations WHERE "
                    "escalation_id = 'escalation-1'"
                ).fetchone()["body_json"]
            )
            body["obligation_snapshot"][0]["activity_id"] = "forged-launch"
            forged_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                "event_id = 'escalation-event-1'",
                (forged_hash, body_json),
            )
            connection.execute(
                "UPDATE stop_escalations SET event_hash = ?, body_json = ? "
                "WHERE escalation_id = 'escalation-1'",
                (forged_hash, body_json),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE "
                "command_id = 'escalation-command-1'",
                (forged_hash,),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (forged_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE "
                "repository_id = 'repo-1'",
                (forged_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = forged_hash
        with self.assertRaisesRegex(
            StorageIntegrityError, "obligation snapshot"
        ):
            self.store.load_verified("repo-1")

    def test_t20_recovery_rejects_self_consistent_item_retarget(self) -> None:
        request = self.request()
        committed = self._commit_planned_intent(
            request, self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        launched = self.store.claim_operation_launch(request, committed)
        self.oracle.allowed_head = launched.event_hash
        graceful = replace(
            self._stop_request(StopMode.GRACEFUL),
            drain_deadline_utc="2000-01-01T00:00:00Z",
        )
        stopped = self.store.stop(
            graceful, self._stop_capability(StopMode.GRACEFUL), self.authority
        )
        self.oracle.allowed_head = stopped.event_hash
        self.store.escalate_stop(
            StopEscalationRequest(
                "escalation-1", "escalation-command-1",
                "escalation-event-1", "repo-1", "run-1", graceful.stop_id,
                graceful.event_id, graceful.drain_deadline_utc,
                "GRACEFUL_DEADLINE_EXPIRED",
                (StopEscalationSettlement(
                    "reservation-1", "escalation-settlement-event-1", ""
                ),),
            ),
            self._stop_escalation_capability(), self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM stop_escalations WHERE "
                    "escalation_id = 'escalation-1'"
                ).fetchone()["body_json"]
            )
            body["item_id"] = "forged-item"
            forged_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET item_id = ?, event_hash = ?, "
                "body_json = ? WHERE event_id = 'escalation-event-1'",
                ("forged-item", forged_hash, body_json),
            )
            connection.execute(
                "UPDATE stop_escalations SET item_id = ?, event_hash = ?, "
                "body_json = ? WHERE escalation_id = 'escalation-1'",
                ("forged-item", forged_hash, body_json),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE "
                "command_id = 'escalation-command-1'",
                (forged_hash,),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (forged_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE "
                "repository_id = 'repo-1'",
                (forged_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = forged_hash
        with self.assertRaisesRegex(
            StorageIntegrityError, "source binding"
        ):
            self.store.load_verified("repo-1")

    def test_t20_rejects_incomplete_stale_and_forged_requests(self) -> None:
        request = self.request()
        committed = self._commit_planned_intent(
            request, self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        launched = self.store.claim_operation_launch(request, committed)
        self.oracle.allowed_head = launched.event_hash
        graceful = replace(
            self._stop_request(StopMode.GRACEFUL),
            drain_deadline_utc="2000-01-01T00:00:00Z",
        )
        stopped = self.store.stop(
            graceful, self._stop_capability(StopMode.GRACEFUL), self.authority
        )
        self.oracle.allowed_head = stopped.event_hash
        base = StopEscalationRequest(
            "escalation-1", "escalation-command-1", "escalation-event-1",
            "repo-1", "run-1", graceful.stop_id, graceful.event_id,
            graceful.drain_deadline_utc, "GRACEFUL_DEADLINE_EXPIRED",
            (StopEscalationSettlement(
                "reservation-1", "escalation-settlement-event-1", ""
            ),),
        )
        capability = self._stop_escalation_capability()
        with self.assertRaisesRegex(DispatchDenied, "exactly cover"):
            self.store.escalate_stop(
                replace(base, unknown_settlements=()),
                capability,
                self.authority,
            )
        with self.assertRaisesRegex(DispatchDenied, "stale"):
            self.store.escalate_stop(
                replace(
                    base,
                    unknown_settlements=(StopEscalationSettlement(
                        "reservation-1", "escalation-settlement-event-1",
                        "stale-hash",
                    ),),
                ),
                capability,
                self.authority,
            )
        with self.assertRaisesRegex(DispatchDenied, "was not issued here"):
            self.store.escalate_stop(
                base,
                replace(capability, issuer_mac="forged"),
                self.authority,
            )
        with self.assertRaisesRegex(DispatchDenied, "deadline binding"):
            self.store.escalate_stop(
                replace(
                    base,
                    expected_drain_deadline_utc="1999-01-01T00:00:00Z",
                ),
                capability,
                self.authority,
            )

    def test_t20_rejects_immediate_stop_as_source(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            oracle = MutableFreshnessOracle()
            store = SQLiteStateStore(
                Path(directory) / "state.sqlite3", oracle, "repo-1"
            )
            authority = SyntheticAuthority()
            store._bind_classification_authority(authority)
            effect_grant = SyntheticGrant(
                "grant-x", "repo-1", "effect-x", "attempt-x", "scope-x"
            )
            authority.register(effect_grant)
            effect_capability = authority.claim(*effect_grant.__dict__.values())
            intent = IntentRequest(
                "repo-1", "run-x", "item-x", "command-x", "event-x",
                "effect-x", "descriptor-x", "attempt-x", "permission-x",
                "reservation-x", "budget-x", 1, 2, 5,
            )
            plan = store.accept_plan(
                PlanAcceptanceRequest(
                    "plan-x", "plan-command-x", "plan-event-x", "repo-1",
                    "run-x", "item-x", "effect-x", "revision-x",
                    "descriptor-x", "scope-x", "budget-x", ("check-x",),
                ),
                expected_head="", writer_epoch=1,
            )
            oracle.allowed_head = plan.event_hash
            committed = store.commit_intent(
                intent, effect_capability, authority,
                expected_head=plan.event_hash, writer_epoch=2,
            )
            oracle.allowed_head = committed.event_hash
            launched = store.claim_operation_launch(intent, committed)
            oracle.allowed_head = launched.event_hash
            stop_grant = SyntheticOperatorGrant(
                "stop-grant-x", "repo-1", "run-x", "STOP_IMMEDIATE",
                "stop-scope-x",
            )
            authority.register_operator(stop_grant)
            immediate = StopRequest(
                "stop-x", "stop-command-x", "stop-event-x", "repo-1",
                "run-x", StopMode.IMMEDIATE, "OPERATOR_STOP",
            )
            stopped = store.stop(
                immediate,
                authority.claim_operator(*stop_grant.__dict__.values()),
                authority,
            )
            oracle.allowed_head = stopped.event_hash
            escalation_grant = SyntheticOperatorGrant(
                "escalation-grant-x", "repo-1", "run-x", "STOP_ESCALATE",
                "escalation-scope-x",
            )
            authority.register_operator(escalation_grant)
            with self.assertRaisesRegex(DispatchDenied, "graceful stop"):
                store.escalate_stop(
                    StopEscalationRequest(
                        "escalation-x", "escalation-command-x",
                        "escalation-event-x", "repo-1", "run-x", "stop-x",
                        "stop-event-x", "2000-01-01T00:00:00Z",
                        "GRACEFUL_DEADLINE_EXPIRED",
                        (StopEscalationSettlement(
                            "reservation-x", "escalation-settlement-x", ""
                        ),),
                    ),
                    authority.claim_operator(*escalation_grant.__dict__.values()),
                    authority,
                )

    def test_r_stop_01_t18_closes_applied_pass(self) -> None:
        self._assert_r_stop_01_application_closure(
            verdict="PASS", mode=StopMode.GRACEFUL
        )

    def test_r_stop_01_t19_closes_applied_pass(self) -> None:
        self._assert_r_stop_01_application_closure(
            verdict="PASS", mode=StopMode.IMMEDIATE
        )

    def test_r_stop_01_t18_closes_applied_recoverable_failure(self) -> None:
        self._assert_r_stop_01_application_closure(
            verdict="FAIL", mode=StopMode.GRACEFUL
        )

    def test_r_stop_01_t19_closes_applied_recoverable_failure(self) -> None:
        self._assert_r_stop_01_application_closure(
            verdict="FAIL", mode=StopMode.IMMEDIATE
        )

    def test_r_stop_01_application_closure_crash_replay_is_exactly_once(
        self,
    ) -> None:
        self._record_validator_result(verdict="PASS", only_check=True)
        application_request = ValidationApplicationRequest(
            "application-1", "apply-command-1", "apply-event-1", "repo-1",
            "run-1", "item-1", "effect-1", "revision-1", "check-1",
            "validator-attempt-1", "validator-observation-1",
        )
        with self.assertRaises(InjectedFailure):
            self.store._apply_validator_observation(
                application_request,
                failure_hook=raise_at(
                    "after_validation_application_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            application_hash = connection.execute(
                "SELECT event_hash FROM validation_applications "
                "WHERE application_id = 'application-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = application_hash
        application_replay = self.store._apply_validator_observation(
            application_request
        )
        self.assertTrue(application_replay.replayed)
        stopped = self.store.stop(
            self._stop_request(), self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        request = self._terminal_application_request("PASSED")
        with self.assertRaises(InjectedFailure):
            self.store.settle_terminal_validation(
                request,
                failure_hook=raise_at(
                    "after_terminal_settlement_writes_before_commit"
                ),
            )
        self.assertEqual(
            self.store.table_counts()["terminal_validation_settlements"], 0
        )
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        with self.assertRaises(InjectedFailure):
            self.store.settle_terminal_validation(
                request,
                failure_hook=raise_at(
                    "after_terminal_settlement_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            terminal_hash = connection.execute(
                "SELECT event_hash FROM terminal_validation_settlements "
                "WHERE terminal_settlement_id = 'terminal-settlement-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = terminal_hash
        reopened = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        )
        replay = reopened.settle_terminal_validation(request)
        self.assertTrue(replay.replayed)
        self.assertTrue(replay.slot_released)
        connection = sqlite3.connect(self.database_path)
        try:
            terminal_events = connection.execute(
                "SELECT COUNT(*) FROM events WHERE "
                "event_kind = 'TERMINAL_VALIDATION_SETTLED'"
            ).fetchone()[0]
            terminal_rows = connection.execute(
                "SELECT COUNT(*) FROM terminal_validation_settlements"
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual((terminal_events, terminal_rows), (1, 1))
        self.assertEqual(reopened.table_counts()["outstanding_slot"], 0)
        reopened.load_verified("repo-1")

    def test_r_stop_01_application_closure_rejects_misbound_sources(
        self,
    ) -> None:
        self._prepare_finalization()
        stopped = self.store.stop(
            self._stop_request(), self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        request = self._terminal_application_request("PASSED")
        cases = {
            "application": {"source_id": "application-missing"},
            "hash": {"source_event_hash": "forged-application-hash"},
            "mapping": {"disposition": "FAILED"},
            "attempt": {"validator_attempt_id": "validator-attempt-old"},
            "check": {"check_id": "check-missing"},
        }
        before = self.store.table_counts()
        for name, changes in cases.items():
            with self.subTest(name=name), self.assertRaises(DispatchDenied):
                self.store.settle_terminal_validation(
                    replace(
                        request,
                        terminal_settlement_id=f"terminal-{name}",
                        command_id=f"terminal-command-{name}",
                        event_id=f"terminal-event-{name}",
                        **changes,
                    )
                )
            self.assertEqual(self.store.table_counts(), before)

    def test_r_stop_01_application_closure_requires_complete_accounting(
        self,
    ) -> None:
        self._prepare_finalization()
        stopped = self.store.stop(
            self._stop_request(), self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE budget_reservations SET disposition = 'RELEASED' "
                "WHERE reservation_id = 'validator-reservation-1'"
            )
            connection.commit()
        finally:
            connection.close()
        with patch.object(self.store, "_verify_projections", return_value=None):
            with self.assertRaisesRegex(
                DispatchDenied, "accounting is not authoritative"
            ):
                self.store.settle_terminal_validation(
                    self._terminal_application_request("PASSED")
                )
        self.assertEqual(
            self.store.table_counts()["terminal_validation_settlements"], 0
        )
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

    def test_r_stop_01_application_closure_rejects_superseded_attempt(
        self,
    ) -> None:
        observation, failed = self._prepare_recoverable_application()
        recovery_request, attestation, parent_event_hash = (
            self._validation_recovery_pair(failed)
        )
        recovered = self.store.resolve_validation_blocker(
            recovery_request, attestation, self.authority
        )
        self.oracle.allowed_head = recovered.event_hash
        successor_request, successor_capability = self._validator_intent(
            replace(observation, event_hash=parent_event_hash),
            suffix="2", check_id="check-1", recovery_id="recovery-1",
        )
        successor = self.store.commit_validator_intent(
            successor_request, successor_capability, self.authority
        )
        self.oracle.allowed_head = successor.event_hash
        stopped = self.store.stop(
            self._stop_request(), self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash

        with self.assertRaisesRegex(DispatchDenied, "current attempt"):
            self.store.settle_terminal_validation(
                self._terminal_application_request("FAILED")
            )
        self.assertEqual(
            self.store.table_counts()["terminal_validation_settlements"], 0
        )
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

    def test_r_stop_01_recovery_rejects_self_consistent_application_tampering(
        self,
    ) -> None:
        self._prepare_finalization()
        stopped = self.store.stop(
            self._stop_request(), self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        settled = self.store.settle_terminal_validation(
            self._terminal_application_request("PASSED")
        )
        mutations = {
            "application": ("source_id", "application-missing"),
            "hash": ("source_event_hash", "forged-application-hash"),
            "mapping": ("disposition", "FAILED"),
            "attempt": ("validator_attempt_id", "validator-attempt-old"),
            "check": ("check_id", "check-missing"),
        }
        for name, (field, value) in mutations.items():
            with self.subTest(name=name):
                case_path = (
                    Path(self.temporary_directory.name)
                    / f"terminal-tamper-{name}.sqlite3"
                )
                shutil.copy2(self.database_path, case_path)
                connection = sqlite3.connect(case_path)
                try:
                    body = json.loads(
                        connection.execute(
                            "SELECT body_json FROM events WHERE event_id = ?",
                            (settled.event_id,),
                        ).fetchone()[0]
                    )
                    body[field] = value
                    request_body = {
                        key: body[key]
                        for key in TerminalValidationSettlementRequest.__dataclass_fields__
                    }
                    payload_digest = self.store._event_hash(request_body)
                    obligation_proof_key = self.store._event_hash(
                        {
                            key: value
                            for key, value in request_body.items()
                            if key not in {
                                "terminal_settlement_id", "command_id",
                                "event_id",
                            }
                        }
                    )
                    body["obligation_proof_key"] = obligation_proof_key
                    event_hash = self.store._event_hash(body)
                    body_json = json.dumps(
                        body, sort_keys=True, separators=(",", ":")
                    )
                    connection.execute(
                        "UPDATE events SET event_hash = ?, body_json = ? "
                        "WHERE event_id = ?",
                        (event_hash, body_json, settled.event_id),
                    )
                    connection.execute(
                        f"UPDATE terminal_validation_settlements SET {field} = ?, "
                        "obligation_proof_key = ?, payload_digest = ?, "
                        "event_hash = ?, body_json = ? WHERE "
                        "terminal_settlement_id = ?",
                        (
                            value, obligation_proof_key, payload_digest,
                            event_hash, body_json,
                            settled.terminal_settlement_id,
                        ),
                    )
                    connection.execute(
                        "UPDATE command_outcomes SET payload_digest = ?, "
                        "event_hash = ? WHERE command_id = ?",
                        (payload_digest, event_hash, settled.command_id),
                    )
                    connection.execute(
                        "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                        (event_hash,),
                    )
                    connection.execute(
                        "UPDATE repositories SET catalog_head = ? "
                        "WHERE repository_id = 'repo-1'",
                        (event_hash,),
                    )
                    connection.commit()
                finally:
                    connection.close()
                self.oracle.allowed_head = event_hash
                with self.assertRaisesRegex(
                    StorageIntegrityError, "terminal validation history"
                ):
                    SQLiteStateStore(
                        case_path, self.oracle, "repo-1"
                    ).load_verified("repo-1")

    def test_t16_finalization_is_atomic_replay_safe_and_releases_slot(self) -> None:
        request, attestation = self._prepare_finalization()
        with self.assertRaises(InjectedFailure):
            self.store._finalize_operation(
                request, attestation, self.authority,
                failure_hook=raise_at("after_finalization_writes_before_commit"),
            )
        self.assertEqual(self.store.table_counts()["operation_finalizations"], 0)
        with self.assertRaises(InjectedFailure):
            self.store._finalize_operation(
                request, attestation, self.authority,
                failure_hook=raise_at(
                    "after_finalization_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            final_hash, event_kind = connection.execute(
                "SELECT f.event_hash, e.event_kind FROM operation_finalizations f "
                "JOIN events e ON e.event_id = f.event_id"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(event_kind, "OPERATION_FINALIZED")
        self.oracle.allowed_head = final_hash
        replay = self.store._finalize_operation(
            request, attestation, self.authority
        )
        self.assertTrue(replay.replayed)
        self.assertEqual(replay.resulting_state.value, "COMPLETED")
        semantic_replay = self.store._finalize_operation(
            replace(
                request,
                finalization_id="finalization-retry",
                command_id="finalize-command-retry",
                event_id="finalize-event-retry",
            ),
            attestation,
            self.authority,
        )
        self.assertEqual(semantic_replay, replace(replay, replayed=True))
        self.assertEqual(self.store.table_counts()["operation_finalizations"], 1)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.store.load_verified("repo-1")
        with self.assertRaisesRegex(StorageIntegrityError, "rebound"):
            self.store._finalize_operation(
                replace(request, event_id="rebound-finalize-event"),
                attestation,
                self.authority,
            )
        with self.assertRaisesRegex(StorageIntegrityError, "reused"):
            self.store._finalize_operation(
                replace(
                    request,
                    finalization_id="another-finalization-retry",
                    command_id="plan-command-1",
                    event_id="another-finalize-event-retry",
                ),
                attestation,
                self.authority,
            )

    def test_t16_accepts_latest_authoritative_adjustment(self) -> None:
        self._prepare_finalization()
        connection = sqlite3.connect(self.database_path)
        try:
            previous_hash = connection.execute(
                "SELECT settlement_head_hash FROM budget_reservations "
                "WHERE reservation_id = 'reservation-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        adjustment = BudgetSettlementRequest(
            "settlement-adjusted", "reservation-1", previous_hash,
            BudgetDisposition.ADJUSTED, 3, "receipt-correction",
            "AUTHORITATIVE_CORRECTION",
        )
        adjusted = self.store._settle_budget(
            adjustment,
            self.authority.issue_settlement_proof(
                "proof-adjusted", adjustment
            ),
            self.authority,
        )
        self.oracle.allowed_head = adjusted.settlement_hash
        request, attestation = self._finalization_request_and_attestation(
            adjusted.settlement_hash
        )

        finalized = self.store._finalize_operation(
            request, attestation, self.authority
        )

        self.assertEqual(finalized.resulting_state.value, "COMPLETED")
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)

    def test_t16_late_authoritative_adjustment_does_not_reopen_completion(self) -> None:
        request, attestation = self._prepare_finalization()
        finalized = self.store._finalize_operation(
            request, attestation, self.authority
        )
        self.oracle.allowed_head = finalized.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            previous_hash = connection.execute(
                "SELECT settlement_head_hash FROM budget_reservations "
                "WHERE reservation_id = 'reservation-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        adjustment = BudgetSettlementRequest(
            "late-settlement-adjusted", "reservation-1", previous_hash,
            BudgetDisposition.ADJUSTED, 3, "late-receipt-correction",
            "AUTHORITATIVE_CORRECTION",
        )
        adjusted = self.store._settle_budget(
            adjustment,
            self.authority.issue_settlement_proof(
                "late-proof-adjusted", adjustment
            ),
            self.authority,
        )
        self.oracle.allowed_head = adjusted.settlement_hash
        self.store.load_verified("repo-1")
        connection = sqlite3.connect(self.database_path)
        try:
            charged_units, lifecycle_state = connection.execute(
                "SELECT b.charged_units, r.lifecycle_state "
                "FROM budget_reservations b JOIN runs r ON r.run_id = b.run_id "
                "WHERE b.reservation_id = 'reservation-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(charged_units, 3)
        self.assertEqual(lifecycle_state, "COMPLETED")
        self.assertEqual(self.store.table_counts()["operation_finalizations"], 1)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)

    def test_t16_late_unknown_accounting_recovers_for_correction(self) -> None:
        request, attestation = self._prepare_finalization()
        finalized = self.store._finalize_operation(
            request, attestation, self.authority
        )
        self.oracle.allowed_head = finalized.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            previous_hash = connection.execute(
                "SELECT settlement_head_hash FROM budget_reservations "
                "WHERE reservation_id = 'reservation-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        unknown = BudgetSettlementRequest(
            "late-unknown", "reservation-1", previous_hash,
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "late-unknown-evidence", "ADDITIONAL_LIABILITY_UNKNOWN",
            additional_liability=True,
        )
        unknown_receipt = self.store._settle_budget(
            unknown,
            self.authority.issue_settlement_proof("late-unknown-proof", unknown),
            self.authority,
        )
        self.oracle.allowed_head = unknown_receipt.settlement_hash

        reopened = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        )
        reopened._bind_classification_authority(self.authority)
        reopened.load_verified("repo-1")
        correction = BudgetSettlementRequest(
            "late-correction", "reservation-1",
            unknown_receipt.settlement_hash, BudgetDisposition.ADJUSTED, 3,
            "late-authoritative-evidence", "AUTHORITATIVE_CORRECTION",
        )
        corrected = reopened._settle_budget(
            correction,
            self.authority.issue_settlement_proof(
                "late-correction-proof", correction
            ),
            self.authority,
        )
        self.oracle.allowed_head = corrected.settlement_hash
        reopened.load_verified("repo-1")
        connection = sqlite3.connect(self.database_path)
        try:
            charged_units, uncertainty, lifecycle_state = connection.execute(
                "SELECT b.charged_units, b.uncertainty, r.lifecycle_state "
                "FROM budget_reservations b JOIN runs r ON r.run_id = b.run_id "
                "WHERE b.reservation_id = 'reservation-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual((charged_units, uncertainty), (3, 0))
        self.assertEqual(lifecycle_state, "COMPLETED")
        self.assertEqual(reopened.table_counts()["operation_finalizations"], 1)
        self.assertEqual(reopened.table_counts()["outstanding_slot"], 0)
        self.assertEqual(reopened.table_counts()["dispatch_fences"], 0)

    def test_f21_process_termination_keeps_fence_clearance_atomic(self) -> None:
        request, attestation = self._prepare_finalization()
        finalized = self.store._finalize_operation(
            request, attestation, self.authority
        )
        self.oracle.allowed_head = finalized.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            previous_hash = connection.execute(
                "SELECT settlement_head_hash FROM budget_reservations "
                "WHERE reservation_id = 'reservation-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        unknown = BudgetSettlementRequest(
            "late-unknown", "reservation-1", previous_hash,
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "late-unknown-evidence", "ADDITIONAL_LIABILITY_UNKNOWN",
            additional_liability=True,
        )
        unknown_receipt = self.store._settle_budget(
            unknown,
            self.authority.issue_settlement_proof("late-unknown-proof", unknown),
            self.authority,
        )
        self.oracle.allowed_head = unknown_receipt.settlement_hash
        correction = BudgetSettlementRequest(
            "late-correction", "reservation-1",
            unknown_receipt.settlement_hash, BudgetDisposition.ADJUSTED, 3,
            "late-authoritative-evidence", "AUTHORITATIVE_CORRECTION",
        )
        context = multiprocessing.get_context("spawn")
        issuer_key = self.authority._issuer_key

        for stage in (
            "after_settlement_writes_before_commit",
            "after_settlement_commit_before_acknowledgement",
        ):
            ready = context.Event()
            process = context.Process(
                target=_settle_until_terminated,
                args=(
                    self.database_path,
                    issuer_key,
                    unknown_receipt.settlement_hash,
                    correction,
                    stage,
                    ready,
                ),
            )
            process.start()
            try:
                self.assertTrue(
                    ready.wait(10),
                    f"child did not reach {stage}",
                )
            finally:
                process.terminate()
                process.join(10)
                if process.is_alive():
                    process.kill()
                    process.join(10)
            self.assertFalse(process.is_alive())

            connection = sqlite3.connect(self.database_path)
            try:
                correction_row = connection.execute(
                    "SELECT settlement_hash FROM budget_settlements "
                    "WHERE settlement_event_id = 'late-correction'"
                ).fetchone()
                fence_ids = {
                    row[0] for row in connection.execute(
                        "SELECT fence_id FROM dispatch_fences"
                    )
                }
            finally:
                connection.close()
            if stage == "after_settlement_writes_before_commit":
                self.assertIsNone(correction_row)
                self.assertEqual(
                    fence_ids, {"additional-liability:late-unknown"}
                )
            else:
                self.assertIsNotNone(correction_row)
                self.assertEqual(fence_ids, set())

        self.oracle.allowed_head = correction_row[0]
        replay = self.store._settle_budget(
            correction,
            self.authority.issue_settlement_proof(
                "replay-proof", correction
            ),
            self.authority,
        )
        self.assertTrue(replay.replayed)
        self.store.load_verified("repo-1")

    def test_t16_accepts_zero_aggregate_gates_with_pass_attestation(self) -> None:
        request, attestation = self._prepare_finalization(aggregate_gate_ids=())
        finalized = self.store._finalize_operation(
            request, attestation, self.authority
        )
        self.assertEqual(finalized.resulting_state.value, "COMPLETED")
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)

    def test_t16_waits_for_checks_and_aggregate_attestation_then_finalizes_once(self) -> None:
        observation = self._record_effect_observation(
            ("check-1", "check-2"), ("aggregate-release",)
        )
        self._record_validator_result_for(observation, suffix="1")
        first = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1", "check-1",
                "validator-attempt-1", "validator-observation-1",
            )
        )
        self.oracle.allowed_head = first.event_hash
        self.assertEqual(first.resulting_state.value, "VALIDATING")
        with self.assertRaisesRegex(DispatchDenied, "BLOCKED/FINALIZING"):
            request, attestation = self._finalization_request_and_attestation(
                first.event_hash
            )
            self.store._finalize_operation(
                request, attestation, self.authority
            )
        self._record_validator_result_for(observation, suffix="2")
        second = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-2", "apply-command-2", "apply-event-2", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1", "check-2",
                "validator-attempt-2", "validator-observation-2",
            )
        )
        self.oracle.allowed_head = second.event_hash
        self.assertEqual(second.resulting_state.value, "BLOCKED")
        request, attestation = self._finalization_request_and_attestation(
            second.event_hash
        )
        with self.assertRaisesRegex(DispatchDenied, "attestation is unavailable"):
            self.store._finalize_operation(
                request, None, self.authority
            )
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        finalized = self.store._finalize_operation(
            request, attestation, self.authority
        )
        self.assertEqual(finalized.resulting_state.value, "COMPLETED")
        self.assertEqual(self.store.table_counts()["operation_finalizations"], 1)

    def test_t16_denies_stale_head_attestation_and_slot_rebinding(self) -> None:
        request, attestation = self._prepare_finalization()
        with self.assertRaisesRegex(ValueError, "generation must be positive"):
            self.store._finalize_operation(
                replace(request, expected_slot_generation=True),
                attestation,
                self.authority,
            )
        stale = self.authority.issue_finalization_attestation(
            "attestation-stale", "repo-1", "run-1", "item-1", "effect-1",
            "plan-1", attestation.plan_event_hash, "revision-1", "stale-head",
            attestation.finalization_key, attestation.gate_set_digest,
            "attempt-1", 1,
        )
        with self.assertRaisesRegex(DispatchDenied, "current durable state"):
            self.store._finalize_operation(request, stale, self.authority)
        rebound_request = replace(
            request, expected_slot_attempt_id="another-attempt"
        )
        rebound = self.authority.issue_finalization_attestation(
            "attestation-rebound", "repo-1", "run-1", "item-1", "effect-1",
            "plan-1", attestation.plan_event_hash, "revision-1",
            attestation.evaluated_run_head, attestation.finalization_key,
            attestation.gate_set_digest, "another-attempt", 1,
        )
        with patch.object(
            self.store, "_accounting_closure_error", return_value=None
        ):
            with self.assertRaisesRegex(DispatchDenied, "own the slot"):
                self.store._finalize_operation(
                    rebound_request, rebound, self.authority
                )

    def test_t16_denies_forged_rebound_and_unsupported_attestations(self) -> None:
        request, attestation = self._prepare_finalization()
        with self.assertRaisesRegex(DispatchDenied, "not issued"):
            self.store._finalize_operation(
                request,
                replace(attestation, issuer_mac="0" * 64),
                self.authority,
            )
        rebound_values = {
            "repository_id": "repo-other",
            "run_id": "run-other",
            "item_id": "item-other",
            "logical_effect_id": "effect-other",
            "plan_id": "plan-other",
            "plan_event_hash": "plan-hash-other",
            "revision_digest": "revision-other",
            "evaluated_run_head": "run-head-other",
            "finalization_key": "finalization-key-other",
            "gate_set_digest": "gate-digest-other",
            "slot_attempt_id": "attempt-other",
            "slot_generation": 2,
        }
        for field, value in rebound_values.items():
            with self.subTest(field=field):
                rebound = self._reissue_finalization_attestation(
                    attestation,
                    attestation_id=f"attestation-{field}",
                    **{field: value},
                )
                with self.assertRaisesRegex(
                    DispatchDenied, "current durable state"
                ):
                    self.store._finalize_operation(
                        request, rebound, self.authority
                    )
        for field, value in (
            ("verdict", "FAIL"),
            ("policy_id", "unsupported-policy"),
            ("policy_version", "unsupported-version"),
        ):
            with self.subTest(field=field):
                with self.assertRaises(ValueError):
                    self._reissue_finalization_attestation(
                        attestation, **{field: value}
                    )
        other_authority = SyntheticAuthority(b"o" * 32)
        other_attestation = other_authority.issue_finalization_attestation(
            **{
                name: getattr(attestation, name)
                for name in attestation.__dataclass_fields__
                if name != "issuer_mac"
            }
        )
        with self.assertRaisesRegex(DispatchDenied, "not issued"):
            self.store._finalize_operation(
                request, other_attestation, self.authority
            )
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        self.assertEqual(self.store.table_counts()["operation_finalizations"], 0)

    def test_t16_denies_event_derived_budget_fence(self) -> None:
        self._prepare_finalization()
        connection = sqlite3.connect(self.database_path)
        try:
            previous_settlement_hash = connection.execute(
                "SELECT settlement_head_hash FROM budget_reservations "
                "WHERE reservation_id = 'reservation-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        settlement_request = BudgetSettlementRequest(
            "settlement-fence", "reservation-1",
            previous_settlement_hash, BudgetDisposition.ADJUSTED, 11,
            "receipt-reconciled", "USAGE_RECONCILED",
        )
        settlement = self.store._settle_budget(
            settlement_request,
            self.authority.issue_settlement_proof(
                "proof-reconciled", settlement_request,
            ),
            self.authority,
        )
        self.oracle.allowed_head = settlement.settlement_hash
        request, attestation = self._finalization_request_and_attestation(
            settlement.settlement_hash
        )
        with self.assertRaisesRegex(DispatchDenied, "active dispatch fence"):
            self.store._finalize_operation(request, attestation, self.authority)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

    def test_t16_final_effect_observation_must_bind_slot_attempt(self) -> None:
        request, attestation = self._prepare_finalization()
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE effect_observations SET attempt_id = 'other-attempt'"
            )
            connection.commit()
        finally:
            connection.close()
        with patch.object(self.store, "_verify_projections"):
            with self.assertRaisesRegex(
                DispatchDenied, "final effect observation"
            ):
                self.store._finalize_operation(
                    request, attestation, self.authority
                )

    def test_t16_denies_defense_in_depth_active_validator(self) -> None:
        request, attestation = self._prepare_finalization()
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE validator_intents SET status = 'ACTIVE'"
            )
            connection.commit()
        finally:
            connection.close()
        with patch.object(self.store, "_verify_projections"):
            with self.assertRaisesRegex(DispatchDenied, "validator activity"):
                self.store._finalize_operation(
                    request, attestation, self.authority
                )

    def test_t16_denies_defense_in_depth_unsettled_accounting(self) -> None:
        request, attestation = self._prepare_finalization()
        for field, value in (
            ("held_units", 1),
            ("uncertainty", 1),
            ("disposition", "RESERVED"),
            ("disposition", "RELEASED"),
            ("charged_units", 3),
        ):
            with self.subTest(field=field):
                connection = sqlite3.connect(self.database_path)
                try:
                    connection.execute(
                        f"UPDATE budget_reservations SET {field} = ? "
                        "WHERE reservation_id = 'reservation-1'",
                        (value,),
                    )
                    connection.commit()
                finally:
                    connection.close()
                with patch.object(self.store, "_verify_projections"):
                    with self.assertRaisesRegex(
                        DispatchDenied, "accounting remains unsettled"
                    ):
                        self.store._finalize_operation(
                            request, attestation, self.authority
                        )
                connection = sqlite3.connect(self.database_path)
                try:
                    connection.execute(
                        "UPDATE budget_reservations SET held_units = 0, "
                        "uncertainty = 0, disposition = 'CONSUMED', "
                        "charged_units = 2 "
                        "WHERE reservation_id = 'reservation-1'"
                    )
                    connection.commit()
                finally:
                    connection.close()

    def test_t16_denies_released_validator_accounting(self) -> None:
        request, attestation = self._prepare_finalization()
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE budget_reservations SET disposition = 'RELEASED' "
                "WHERE reservation_id = 'validator-reservation-1'"
            )
            connection.commit()
        finally:
            connection.close()

        with patch.object(self.store, "_verify_projections"):
            with self.assertRaisesRegex(
                DispatchDenied, "accounting remains unsettled"
            ):
                self.store._finalize_operation(
                    request, attestation, self.authority
                )
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

    def test_t16_denies_missing_final_effect_observation(self) -> None:
        request, attestation = self._prepare_finalization()
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute("DELETE FROM effect_observations")
            connection.commit()
        finally:
            connection.close()
        with patch.object(self.store, "_verify_projections"):
            with self.assertRaisesRegex(
                DispatchDenied, "final effect observation"
            ):
                self.store._finalize_operation(
                    request, attestation, self.authority
                )

    def test_t16_freshness_denial_leaves_finalization_state_unchanged(self) -> None:
        request, attestation = self._prepare_finalization()
        before = self.store.table_counts()
        self.oracle.allowed_head = "independently-stale"
        with self.assertRaisesRegex(DispatchDenied, "freshness proof"):
            self.store._finalize_operation(request, attestation, self.authority)
        after = self.store.table_counts()
        self.assertEqual(after, before)
        connection = sqlite3.connect(self.database_path)
        try:
            state = connection.execute(
                "SELECT lifecycle_state, continuation_cursor FROM runs "
                "WHERE run_id = 'run-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(state, ("BLOCKED", "FINALIZING"))
        self.assertEqual(after["outstanding_slot"], 1)

    def test_t16_recovery_rejects_finalization_state_tampering(self) -> None:
        request, attestation = self._prepare_finalization()
        finalized = self.store._finalize_operation(
            request, attestation, self.authority
        )
        self.oracle.allowed_head = finalized.event_hash
        mutations = {
            "deleted-projection": "DELETE FROM operation_finalizations",
            "changed-projection": (
                "UPDATE operation_finalizations "
                "SET attestation_digest = 'tampered'"
            ),
            "changed-projection-body": (
                "UPDATE operation_finalizations SET body_json = '{}'"
            ),
            "released-terminal-accounting": (
                "UPDATE budget_reservations SET disposition = 'RELEASED' "
                "WHERE reservation_id = 'reservation-1'"
            ),
            "restored-cursor": (
                "UPDATE runs SET continuation_cursor = 'FINALIZING' "
                "WHERE run_id = 'run-1'"
            ),
            "resurrected-slot": (
                "INSERT INTO outstanding_slot VALUES "
                "(1, 'repo-1', 'run-1', 'effect-1', 'attempt-1', 1)"
            ),
            "changed-event": (
                "UPDATE events SET body_json = '{}' "
                "WHERE event_kind = 'OPERATION_FINALIZED'"
            ),
        }
        for name, statement in mutations.items():
            with self.subTest(name=name):
                case_path = Path(self.temporary_directory.name) / f"{name}.sqlite3"
                shutil.copy2(self.database_path, case_path)
                connection = sqlite3.connect(case_path)
                try:
                    connection.execute(statement)
                    connection.commit()
                finally:
                    connection.close()
                with self.assertRaises(StorageIntegrityError):
                    SQLiteStateStore(
                        case_path, self.oracle, "repo-1"
                    ).load_verified("repo-1")

    def test_t16_recovery_rejects_self_consistent_unsigned_finalization(self) -> None:
        request, attestation = self._prepare_finalization()
        finalized = self.store._finalize_operation(
            request, attestation, self.authority
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    (request.event_id,),
                ).fetchone()[0]
            )
            body["attestation_evidence"]["issuer_mac"] = "0" * 64
            body["attestation_digest"] = self.store._event_hash(
                body["attestation_evidence"]
            )
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (event_hash, body_json, request.event_id),
            )
            connection.execute(
                "UPDATE operation_finalizations SET attestation_digest = ?, "
                "event_hash = ?, body_json = ? WHERE finalization_id = ?",
                (
                    body["attestation_digest"], event_hash, body_json,
                    request.finalization_id,
                ),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                (event_hash, request.command_id),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = ?",
                (event_hash, request.run_id),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, request.repository_id),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(
            StorageIntegrityError, "finalization attestation"
        ):
            self.store.load_verified("repo-1", authority=self.authority)

    def test_t16_recovery_rejects_accepted_plan_pin_tampering(self) -> None:
        self._prepare_finalization(aggregate_gate_ids=("aggregate-release",))
        mutations = {
            "effect-descriptor": ("effect_descriptor_digest", "tampered"),
            "permission-scope": ("permission_scope_digest", "tampered"),
            "budget-policy": ("budget_policy_digest", "tampered"),
            "gate-set": (
                "aggregate_gate_ids_json", '["aggregate-tampered"]'
            ),
            "gate-digest": ("gate_set_digest", "tampered"),
            "policy-id": ("finalization_policy_id", "tampered"),
            "policy-version": ("finalization_policy_version", "tampered"),
            "issuer": ("finalization_issuer_fingerprint", "tampered"),
        }
        for name, (column, value) in mutations.items():
            with self.subTest(name=name):
                case_path = (
                    Path(self.temporary_directory.name) / f"plan-{name}.sqlite3"
                )
                shutil.copy2(self.database_path, case_path)
                connection = sqlite3.connect(case_path)
                try:
                    connection.execute(
                        f"UPDATE validation_plans SET {column} = ? "
                        "WHERE plan_id = 'plan-1'",
                        (value,),
                    )
                    connection.commit()
                finally:
                    connection.close()
                with self.assertRaisesRegex(
                    StorageIntegrityError, "validation-plan projection"
                ):
                    SQLiteStateStore(
                        case_path, self.oracle, "repo-1"
                    ).load_verified("repo-1")

    def test_c05_denies_fail_without_trusted_classification(self) -> None:
        self._record_validator_result(verdict="FAIL")
        with self.assertRaisesRegex(DispatchDenied, "trusted failure classification"):
            self.store._apply_validator_observation(
                ValidationApplicationRequest(
                    "application-1", "apply-command-1", "apply-event-1",
                    "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                    "check-1", "validator-attempt-1",
                    "validator-observation-1",
                ),
            )
        self.assertEqual(self.store.table_counts()["validation_applications"], 0)

    def test_c05_recoverable_failure_blocks_and_retains_slot(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        classification = self._classification(observation, "RECOVERABLE")
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1", "validator-observation-1",
            ),
            classification=classification,
        )
        self.oracle.allowed_head = applied.event_hash
        self.assertEqual(applied.resulting_state.value, "BLOCKED")
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        self.store.load_verified("repo-1")

    def test_t16_recovery_authorizes_exactly_one_t27_successor(self) -> None:
        observation, failed = self._prepare_recoverable_application()
        recovery_request, attestation, parent_event_hash = (
            self._validation_recovery_pair(failed)
        )
        recovered = self.store.resolve_validation_blocker(
            recovery_request, attestation, self.authority
        )
        self.oracle.allowed_head = recovered.event_hash
        retry_request, retry_capability = self._validator_intent(
            replace(observation, event_hash=parent_event_hash),
            suffix="2",
            check_id="check-1",
            recovery_id="recovery-1",
        )
        retry = self.store.commit_validator_intent(
            retry_request, retry_capability, self.authority
        )
        self.oracle.allowed_head = retry.event_hash

        self.assertEqual(self.store.table_counts()["validation_recoveries"], 1)
        self.store.load_verified("repo-1")
        duplicate_request, duplicate_capability = self._validator_intent(
            replace(observation, event_hash=parent_event_hash),
            suffix="3",
            check_id="check-1",
            validator_attempt_id="validator-attempt-2",
            recovery_id="recovery-1",
        )
        with self.assertRaisesRegex(DispatchDenied, "not current"):
            self.store.commit_validator_intent(
                duplicate_request,
                duplicate_capability,
                self.authority,
            )
        settlement_request = BudgetSettlementRequest(
            "validator-settlement-2", "validator-reservation-2", "",
            BudgetDisposition.CONSUMED, 1, "validator-result-2",
            "VALIDATOR_USAGE_REPORTED",
        )
        settlement = self.store._settle_budget(
            settlement_request,
            self.authority.issue_settlement_proof(
                "validator-proof-2", settlement_request
            ),
            self.authority,
        )
        self.oracle.allowed_head = settlement.settlement_hash
        passed_observation = self.store._record_validator_observation(
            ValidatorObservationRequest(
                "validator-observation-2", "validator-observe-command-2",
                "validator-observation-event-2", "repo-1", "run-1",
                "item-1", "effect-1", "validator-intent-2",
                "validator-attempt-2", "validator-result-2",
                retry_capability.claim_id, "revision-1", "check-1",
                "input-1", "result-digest-2", "PASS", 1,
                "validator-settlement-2", settlement.settlement_hash,
            )
        )
        self.oracle.allowed_head = passed_observation.event_hash
        passed = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-2", "apply-command-2", "apply-event-2",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-2", "validator-observation-2",
            )
        )
        self.oracle.allowed_head = passed.event_hash
        finalization_request, finalization_attestation = (
            self._finalization_request_and_attestation(passed.event_hash)
        )
        finalized = self.store._finalize_operation(
            finalization_request, finalization_attestation, self.authority
        )
        self.oracle.allowed_head = finalized.event_hash

        self.assertEqual(finalized.resulting_state.value, "COMPLETED")
        self.assertEqual(self.store.table_counts()["validation_applications"], 2)
        SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        ).load_verified("repo-1", authority=self.authority)

    def test_t16_recovery_is_atomic_replay_safe_and_rejects_rebinding(self) -> None:
        _, failed = self._prepare_recoverable_application()
        request, attestation, _ = self._validation_recovery_pair(failed)
        with self.assertRaises(InjectedFailure):
            self.store.resolve_validation_blocker(
                request, attestation, self.authority,
                failure_hook=raise_at(
                    "after_validation_recovery_writes_before_commit"
                ),
            )
        self.assertEqual(self.store.table_counts()["validation_recoveries"], 0)
        self.assertEqual(self.store.load_run_lifecycle("run-1").value, "BLOCKED")

        with self.assertRaises(InjectedFailure):
            self.store.resolve_validation_blocker(
                request, attestation, self.authority,
                failure_hook=raise_at(
                    "after_validation_recovery_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            recovery_hash = connection.execute(
                "SELECT event_hash FROM validation_recoveries "
                "WHERE recovery_id = 'recovery-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = recovery_hash
        replay = self.store.resolve_validation_blocker(
            request, attestation, self.authority
        )
        self.assertTrue(replay.replayed)
        with self.assertRaisesRegex(StorageIntegrityError, "was rebound"):
            self.store.resolve_validation_blocker(
                replace(
                    request,
                    remediation_evidence_digest="different-remediation",
                ),
                attestation,
                self.authority,
            )
        self.store.load_verified("repo-1")

    def test_t16_recovery_rejects_stale_or_forged_attestation(self) -> None:
        _, failed = self._prepare_recoverable_application()
        stale_request, stale_attestation, _ = self._validation_recovery_pair(
            failed, expected_run_head="stale-run-head"
        )
        with self.assertRaisesRegex(DispatchDenied, "run head is stale"):
            self.store.resolve_validation_blocker(
                stale_request, stale_attestation, self.authority
            )
        request, attestation, _ = self._validation_recovery_pair(failed)
        forged = replace(
            attestation, remediation_evidence_digest="forged-remediation"
        )
        with self.assertRaisesRegex(DispatchDenied, "was not issued here"):
            self.store.resolve_validation_blocker(
                request, forged, self.authority
            )
        self.assertEqual(self.store.table_counts()["validation_recoveries"], 0)

    def test_t16_recovery_rejects_self_consistent_unsigned_blocker_recovery(
        self,
    ) -> None:
        _, failed = self._prepare_recoverable_application()
        request, attestation, _ = self._validation_recovery_pair(failed)
        recovered = self.store.resolve_validation_blocker(
            request, attestation, self.authority
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    (recovered.event_id,),
                ).fetchone()[0]
            )
            body["attestation_evidence"]["issuer_mac"] = "0" * 64
            body["attestation_digest"] = self.store._event_hash(
                body["attestation_evidence"]
            )
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (event_hash, body_json, recovered.event_id),
            )
            connection.execute(
                "UPDATE validation_recoveries SET attestation_digest = ?, "
                "event_hash = ?, body_json = ? WHERE recovery_id = ?",
                (
                    body["attestation_digest"], event_hash, body_json,
                    recovered.recovery_id,
                ),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                (event_hash, recovered.command_id),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = ?",
                (event_hash, request.run_id),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, request.repository_id),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(
            StorageIntegrityError, "validation recovery attestation"
        ):
            self.store.load_verified("repo-1", authority=self.authority)

    def test_t27_retry_requires_current_exact_recovery(self) -> None:
        observation, failed = self._prepare_recoverable_application()
        recovery_request, attestation, parent_event_hash = (
            self._validation_recovery_pair(failed)
        )
        missing_request, missing_capability = self._validator_intent(
            replace(observation, event_hash=parent_event_hash),
            suffix="2", check_id="check-1",
        )
        with self.assertRaisesRegex(DispatchDenied, "durable VALIDATING"):
            self.store.commit_validator_intent(
                missing_request, missing_capability, self.authority
            )
        recovered = self.store.resolve_validation_blocker(
            recovery_request, attestation, self.authority
        )
        self.oracle.allowed_head = recovered.event_hash
        wrong_request, wrong_capability = self._validator_intent(
            replace(observation, event_hash=parent_event_hash),
            suffix="3", check_id="check-1",
            validator_attempt_id="validator-attempt-2",
            recovery_id="wrong-recovery",
        )
        with self.assertRaisesRegex(DispatchDenied, "does not bind"):
            self.store.commit_validator_intent(
                wrong_request, wrong_capability, self.authority
            )
        self.assertEqual(self.store.table_counts()["validator_intents"], 1)

    def test_t27_denies_retry_of_already_passed_check(self) -> None:
        effect_observation = self._record_effect_observation()
        validator_observation = self._record_validator_result_for(
            effect_observation, suffix="1"
        )
        passed = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1", "validator-observation-1",
            )
        )
        self.oracle.allowed_head = passed.event_hash
        request, capability = self._validator_intent(
            effect_observation, suffix="3", check_id="check-1"
        )
        with self.assertRaisesRegex(DispatchDenied, "already passed"):
            self.store.commit_validator_intent(
                request, capability, self.authority
            )

    def test_t27_validator_contact_rechecks_recovery_binding(self) -> None:
        observation, failed = self._prepare_recoverable_application()
        recovery_request, attestation, parent_event_hash = (
            self._validation_recovery_pair(failed)
        )
        recovered = self.store.resolve_validation_blocker(
            recovery_request, attestation, self.authority
        )
        self.oracle.allowed_head = recovered.event_hash
        request, capability = self._validator_intent(
            replace(observation, event_hash=parent_event_hash),
            suffix="2", check_id="check-1", recovery_id="recovery-1",
        )
        committed = self.store.commit_validator_intent(
            request, capability, self.authority
        )
        self.oracle.allowed_head = committed.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE validation_recoveries SET "
                "successor_validator_attempt_id = 'tampered-attempt' "
                "WHERE recovery_id = 'recovery-1'"
            )
            connection.commit()
        finally:
            connection.close()
        with patch.object(self.store, "_verify_projections", return_value=None):
            with self.assertRaisesRegex(DispatchDenied, "lost its T16 recovery"):
                self.store._contact_committed_validator(
                    request, capability, committed,
                    self.store._adapter_target_digest("repo-1", "VALIDATOR"),
                    self.authority,
                )

    def test_t16_migrates_populated_legacy_validation_schema(self) -> None:
        _, failed = self._prepare_recoverable_application()
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute("PRAGMA foreign_keys = OFF")
            connection.execute(
                "DROP INDEX uq_validator_intents_recovery_id"
            )
            connection.execute("DROP TABLE validation_recoveries")
            connection.execute(
                "ALTER TABLE validator_intents DROP COLUMN recovery_id"
            )
            connection.execute(
                "CREATE TABLE validation_applications_snapshot AS "
                "SELECT * FROM validation_applications"
            )
            connection.execute("DROP TABLE validation_applications")
            connection.execute(
                "ALTER TABLE validation_applications_snapshot "
                "RENAME TO validation_applications"
            )
            connection.execute(
                "CREATE UNIQUE INDEX legacy_plan_check_unique ON "
                "validation_applications(plan_id, check_id)"
            )
            connection.commit()
        finally:
            connection.close()

        migrated = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        )
        migrated._bind_classification_authority(self.authority)
        migrated.load_verified("repo-1")
        connection = sqlite3.connect(self.database_path)
        try:
            validator_columns = {
                row[1]
                for row in connection.execute(
                    "PRAGMA table_info(validator_intents)"
                )
            }
            application_indexes = {
                row[1]: tuple(
                    column[2]
                    for column in connection.execute(
                        f"PRAGMA index_info('{row[1]}')"
                    )
                )
                for row in connection.execute(
                    "PRAGMA index_list(validation_applications)"
                )
                if row[2]
            }
            foreign_key_errors = connection.execute(
                "PRAGMA foreign_key_check"
            ).fetchall()
            migrated_rows = connection.execute(
                "SELECT application_id, verdict, classification FROM "
                "validation_applications"
            ).fetchall()
            before_noop = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertIn("recovery_id", validator_columns)
        self.assertNotIn(("plan_id", "check_id"), application_indexes.values())
        self.assertEqual(foreign_key_errors, [])
        self.assertEqual(
            migrated_rows, [("application-1", "FAIL", "RECOVERABLE")]
        )

        reopened = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        )
        reopened._bind_classification_authority(self.authority)
        connection = sqlite3.connect(self.database_path)
        try:
            after_noop = tuple(connection.iterdump())
            with self.assertRaises(sqlite3.IntegrityError):
                connection.execute(
                    "UPDATE validation_applications SET verdict = 'INVALID' "
                    "WHERE application_id = 'application-1'"
                )
        finally:
            connection.close()
        self.assertEqual(after_noop, before_noop)
        recovery_request, attestation, _ = self._validation_recovery_pair(failed)
        recovered = reopened.resolve_validation_blocker(
            recovery_request, attestation, self.authority
        )
        self.oracle.allowed_head = recovered.event_hash
        reopened.load_verified("repo-1")

    def test_t16_rejects_malformed_existing_recovery_schema(self) -> None:
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute("DROP TABLE validation_recoveries")
            connection.execute("DROP INDEX uq_validator_intents_recovery_id")
            connection.execute(
                "CREATE TABLE validation_recoveries (recovery_id TEXT PRIMARY KEY)"
            )
            connection.execute(
                "CREATE INDEX uq_validator_intents_recovery_id ON "
                "validator_intents(command_id)"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(
            StorageIntegrityError, "recovery schema is incompatible"
        ):
            SQLiteStateStore(self.database_path, self.oracle, "repo-1")

    def test_t16_rejects_weakened_recovery_index_predicate(self) -> None:
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute("DROP INDEX uq_validator_intents_recovery_id")
            connection.execute(
                "CREATE UNIQUE INDEX uq_validator_intents_recovery_id ON "
                "validator_intents(recovery_id) WHERE recovery_id IS NULL"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(
            StorageIntegrityError, "recovery schema is incompatible"
        ):
            SQLiteStateStore(self.database_path, self.oracle, "repo-1")

    def test_t16_rejects_weakened_recovery_table_constraint(self) -> None:
        connection = sqlite3.connect(self.database_path)
        try:
            table_sql = connection.execute(
                "SELECT sql FROM sqlite_master WHERE type = 'table' AND "
                "name = 'validation_recoveries'"
            ).fetchone()[0]
            weakened_sql = table_sql.replace(
                "resulting_state TEXT NOT NULL CHECK (resulting_state = 'VALIDATING')",
                "resulting_state TEXT NOT NULL",
            )
            self.assertNotEqual(weakened_sql, table_sql)
            connection.execute("DROP TABLE validation_recoveries")
            connection.execute(weakened_sql)
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(
            StorageIntegrityError, "recovery schema is incompatible"
        ):
            SQLiteStateStore(self.database_path, self.oracle, "repo-1")

    def test_r_stop_01_migrates_populated_terminal_validation_schema(
        self,
    ) -> None:
        observation = self._record_validator_result(verdict="FAIL")
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1",
                "validator-observation-1",
            ),
            classification=self._classification(observation, "FINAL"),
        )
        self.oracle.allowed_head = applied.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            plan_hash = connection.execute(
                "SELECT event_hash FROM validation_plans WHERE plan_id = 'plan-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        settled = self.store.settle_terminal_validation(
            TerminalValidationSettlementRequest(
                "terminal-settlement-1", "terminal-command-1",
                "terminal-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "plan-1", "revision-1", "check-2", "PLAN",
                "plan-1", plan_hash, "CANCELLED_WITHOUT_START",
            )
        )
        self.oracle.allowed_head = settled.event_hash

        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute("PRAGMA foreign_keys = OFF")
            target_sql = connection.execute(
                "SELECT sql FROM sqlite_master WHERE type = 'table' AND "
                "name = 'terminal_validation_settlements'"
            ).fetchone()[0]
            legacy_sql = target_sql.replace(
                "'VALIDATION_APPLICATION', ", ""
            )
            self.assertNotEqual(legacy_sql, target_sql)
            before_rows = connection.execute(
                "SELECT * FROM terminal_validation_settlements"
            ).fetchall()
            before_event_bodies = connection.execute(
                "SELECT event_id, body_json FROM events ORDER BY event_id"
            ).fetchall()
            connection.execute(
                "ALTER TABLE terminal_validation_settlements RENAME TO "
                "terminal_validation_settlements_snapshot"
            )
            connection.execute(legacy_sql)
            columns = ", ".join(
                row[1]
                for row in connection.execute(
                    "PRAGMA table_info(terminal_validation_settlements)"
                )
            )
            connection.execute(
                f"INSERT INTO terminal_validation_settlements ({columns}) "
                f"SELECT {columns} FROM terminal_validation_settlements_snapshot"
            )
            connection.execute(
                "DROP TABLE terminal_validation_settlements_snapshot"
            )
            connection.commit()
        finally:
            connection.close()

        migrated = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        )
        migrated._bind_classification_authority(self.authority)
        connection = sqlite3.connect(self.database_path)
        try:
            after_rows = connection.execute(
                "SELECT * FROM terminal_validation_settlements"
            ).fetchall()
            after_event_bodies = connection.execute(
                "SELECT event_id, body_json FROM events ORDER BY event_id"
            ).fetchall()
            migrated_sql = connection.execute(
                "SELECT sql FROM sqlite_master WHERE type = 'table' AND "
                "name = 'terminal_validation_settlements'"
            ).fetchone()[0]
            foreign_key_errors = connection.execute(
                "PRAGMA foreign_key_check"
            ).fetchall()
        finally:
            connection.close()
        self.assertEqual(after_rows, before_rows)
        self.assertEqual(after_event_bodies, before_event_bodies)
        self.assertIn("VALIDATION_APPLICATION", migrated_sql)
        self.assertEqual(foreign_key_errors, [])
        migrated.load_verified("repo-1")

    def test_r_stop_01_rejects_incompatible_terminal_schema_without_mutation(
        self,
    ) -> None:
        connection = sqlite3.connect(self.database_path)
        try:
            target_sql = connection.execute(
                "SELECT sql FROM sqlite_master WHERE type = 'table' AND "
                "name = 'terminal_validation_settlements'"
            ).fetchone()[0]
            weakened_sql = target_sql.replace(
                "slot_generation INTEGER NOT NULL CHECK (slot_generation = 1)",
                "slot_generation INTEGER NOT NULL",
            )
            self.assertNotEqual(weakened_sql, target_sql)
            connection.execute("DROP TABLE terminal_validation_settlements")
            connection.execute(weakened_sql)
            connection.commit()
            before = tuple(connection.iterdump())
        finally:
            connection.close()

        with self.assertRaisesRegex(
            StorageIntegrityError, "terminal validation schema is incompatible"
        ):
            SQLiteStateStore(self.database_path, self.oracle, "repo-1")
        connection = sqlite3.connect(self.database_path)
        try:
            after = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after, before)

    def test_c05_recoverable_failure_rolls_back_and_replays_after_lost_ack(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        classification = self._classification(observation, "RECOVERABLE")
        request = ValidationApplicationRequest(
            "application-1", "apply-command-1", "apply-event-1",
            "repo-1", "run-1", "item-1", "effect-1", "revision-1",
            "check-1", "validator-attempt-1", "validator-observation-1",
        )
        with self.assertRaises(InjectedFailure):
            self.store._apply_validator_observation(
                request, classification=classification,
                failure_hook=raise_at(
                    "after_validation_application_writes_before_commit"
                ),
            )
        self.assertEqual(self.store.table_counts()["validation_applications"], 0)
        with self.assertRaises(InjectedFailure):
            self.store._apply_validator_observation(
                request, classification=classification,
                failure_hook=raise_at(
                    "after_validation_application_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            self.oracle.allowed_head = connection.execute(
                "SELECT event_hash FROM validation_applications "
                "WHERE application_id = 'application-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        recovered = SQLiteStateStore(self.database_path, self.oracle, "repo-1")
        recovered._bind_classification_authority(self.authority)
        replay = recovered._apply_validator_observation(request)
        self.assertTrue(replay.replayed)
        self.assertEqual(replay.resulting_state.value, "BLOCKED")

    def test_c05_final_failure_is_atomic_replay_safe_and_permanently_fenced(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        classification = self._classification(observation, "FINAL")
        request = ValidationApplicationRequest(
            "application-1", "apply-command-1", "apply-event-1",
            "repo-1", "run-1", "item-1", "effect-1", "revision-1",
            "check-1", "validator-attempt-1", "validator-observation-1",
        )
        with self.assertRaises(InjectedFailure):
            self.store._apply_validator_observation(
                request, classification=classification,
                failure_hook=raise_at(
                    "after_validation_application_writes_before_commit"
                ),
            )
        self.assertEqual(self.store.table_counts()["validation_applications"], 0)
        with self.assertRaises(InjectedFailure):
            self.store._apply_validator_observation(
                request, classification=classification,
                failure_hook=raise_at(
                    "after_validation_application_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            event_hash = connection.execute(
                "SELECT event_hash FROM validation_applications "
                "WHERE application_id = 'application-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash
        replay = self.store._apply_validator_observation(
            request,
        )
        self.assertTrue(replay.replayed)
        self.assertEqual(replay.resulting_state.value, "FAILED_FINAL")
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.assertEqual(self.store.table_counts()["dispatch_fences"], 1)
        self.store.load_verified("repo-1")
        recovered_store = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        )
        recovered_store._bind_classification_authority(self.authority)
        recovered_replay = recovered_store._apply_validator_observation(request)
        self.assertTrue(recovered_replay.replayed)

        second_grant = SyntheticGrant(
            "grant-2", "repo-1", "effect-2", "attempt-2", "scope-2"
        )
        self.authority.register(second_grant)
        second_capability = self.authority.claim(*second_grant.__dict__.values())
        second_plan = recovered_store.accept_plan(
            PlanAcceptanceRequest(
                "plan-2", "plan-command-2", "plan-event-2", "repo-1",
                "run-2", "item-2", "effect-2", "revision-2",
                "descriptor-digest", "scope-2", "budget-policy-digest",
                ("check-2",),
            ),
            expected_head=replay.event_hash,
            writer_epoch=20,
        )
        self.oracle.allowed_head = second_plan.event_hash
        second_intent = recovered_store.commit_intent(
            replace(
                self.request(), run_id="run-2", item_id="item-2",
                command_id="command-2", event_id="event-2",
                logical_effect_id="effect-2", attempt_id="attempt-2",
                permission_use_id="permission-use-2",
                reservation_id="reservation-2",
            ),
            second_capability,
            self.authority,
            expected_head=second_plan.event_hash,
            writer_epoch=21,
        )
        self.assertFalse(second_intent.replayed)
        self.assertEqual(
            recovered_store.load_run_lifecycle("run-2").value, "RUNNING"
        )

    def test_c05_final_failure_with_pending_check_retains_slot(self) -> None:
        observation = self._record_validator_result(verdict="FAIL")
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1", "validator-observation-1",
            ),
            classification=self._classification(observation, "FINAL"),
        )
        self.oracle.allowed_head = applied.event_hash
        self.assertEqual(applied.resulting_state.value, "FAILED_FINAL")
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        self.store.load_verified("repo-1")

    def test_t26_terminal_settlement_closes_unstarted_check_and_slot(self) -> None:
        observation = self._record_validator_result(verdict="FAIL")
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1", "validator-observation-1",
            ),
            classification=self._classification(observation, "FINAL"),
        )
        self.oracle.allowed_head = applied.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            plan_hash = connection.execute(
                "SELECT event_hash FROM validation_plans WHERE plan_id = 'plan-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        request = TerminalValidationSettlementRequest(
            "terminal-settlement-1", "terminal-command-1", "terminal-event-1",
            "repo-1", "run-1", "item-1", "effect-1", "plan-1",
            "revision-1", "check-2", "PLAN", "plan-1", plan_hash,
            "CANCELLED_WITHOUT_START",
        )
        with self.assertRaises(InjectedFailure):
            self.store.settle_terminal_validation(
                request,
                failure_hook=raise_at(
                    "after_terminal_settlement_writes_before_commit"
                ),
            )
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        with self.assertRaises(InjectedFailure):
            self.store.settle_terminal_validation(
                request,
                failure_hook=raise_at(
                    "after_terminal_settlement_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            terminal_hash = connection.execute(
                "SELECT event_hash FROM terminal_validation_settlements WHERE "
                "terminal_settlement_id = 'terminal-settlement-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = terminal_hash
        settled = self.store.settle_terminal_validation(request)

        self.assertEqual(settled.resulting_state, LifecycleState.FAILED_FINAL)
        self.assertTrue(settled.slot_released)
        self.assertTrue(settled.replayed)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.assertEqual(self.store.table_counts()["dispatch_fences"], 1)
        self.store.load_verified("repo-1")

    def test_t26_recovery_rejects_mandatory_slot_retention(self) -> None:
        observation = self._record_validator_result(verdict="FAIL")
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1", "validator-observation-1",
            ),
            classification=self._classification(observation, "FINAL"),
        )
        self.oracle.allowed_head = applied.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            plan_hash = connection.execute(
                "SELECT event_hash FROM validation_plans WHERE plan_id = 'plan-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        settled = self.store.settle_terminal_validation(
            TerminalValidationSettlementRequest(
                "terminal-settlement-1", "terminal-command-1",
                "terminal-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "plan-1", "revision-1", "check-2", "PLAN",
                "plan-1", plan_hash, "CANCELLED_WITHOUT_START",
            )
        )
        self.assertTrue(settled.slot_released)
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    (settled.event_id,),
                ).fetchone()[0]
            )
            body["slot_released"] = False
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (event_hash, body_json, settled.event_id),
            )
            connection.execute(
                "UPDATE terminal_validation_settlements SET slot_released = 0, "
                "event_hash = ?, body_json = ? WHERE terminal_settlement_id = ?",
                (event_hash, body_json, settled.terminal_settlement_id),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                (event_hash, settled.command_id),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = ?",
                (event_hash, "run-1"),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, "repo-1"),
            )
            connection.execute(
                "INSERT INTO outstanding_slot VALUES (1, ?, ?, ?, ?, 1)",
                ("repo-1", "run-1", "effect-1", "attempt-1"),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(
            StorageIntegrityError, "terminal validation release decision"
        ):
            self.store.load_verified("repo-1")

    def test_t24_validator_cessation_is_target_serialized_and_replay_safe(
        self,
    ) -> None:
        parent = self._record_effect_observation(check_ids=("check-1",))
        intent, capability = self._validator_intent(parent)
        committed = self.store.commit_validator_intent(
            intent, capability, self.authority
        )
        self.oracle.allowed_head = committed.event_hash
        validator_path = self.database_path.parent / "synthetic-validator.sqlite3"
        adapter = SyntheticValidatorAdapter(validator_path)
        adapter._canonical_repository_id = "repo-1"
        adapter._canonical_ledger_path = validator_path.resolve()
        attestation = self.authority.issue_validator_cessation_attestation(
            "cessation-attestation-1", "cessation-1",
            adapter._target_digest("repo-1"), capability.claim_id,
            "VALIDATOR:validator-intent-1", committed.event_hash,
            "repo-1", "run-1", "item-1", "effect-1", "revision-1",
            "check-1", "validator-attempt-1",
        )
        seal = adapter.seal_cessation(attestation, self.authority)
        self.assertFalse(seal.result_available)
        request = ValidatorCessationRequest(
            "cessation-1", "cessation-command-1", "cessation-event-1",
            "repo-1", "run-1", "item-1", "effect-1",
            "validator-intent-1", "validator-attempt-1", "revision-1",
            "check-1", seal.cessation_hash,
        )
        receipt = self.store.record_validator_cessation(
            request, self.authority
        )
        self.oracle.allowed_head = receipt.event_hash
        replay = self.store.record_validator_cessation(request, self.authority)

        self.assertTrue(replay.replayed)
        self.assertEqual(replay.event_hash, receipt.event_hash)
        self.assertFalse(receipt.result_available)
        self.store.load_verified("repo-1")

        class ContactAlreadyClaimed:
            @staticmethod
            def _contact_committed_validator(*args, **kwargs) -> None:
                return None

        with self.assertRaisesRegex(DispatchDenied, "sealed as ceased"):
            adapter._execute_committed(
                capability,
                SyntheticValidatorRequest(
                    "repo-1", "effect-1", "revision-1", "check-1",
                    "input-1", "validator-attempt-1", "read-only-scope-1",
                    "late-result", "PASS",
                ),
                self.authority,
                ContactAlreadyClaimed(),
                committed,
                intent,
                usage_units=1,
            )

    def test_t26_terminal_result_is_atomic_and_replay_safe(self) -> None:
        parent = self._record_effect_observation()
        pending_observation = self._record_validator_result_for(
            parent, suffix="1", verdict="PASS"
        )
        cessation = self._record_validator_cessation_for(
            suffix="1", result_available=True
        )
        stop_hash = self._stop_run()
        request = TerminalValidationSettlementRequest(
            "terminal-settlement-1", "terminal-command-1", "terminal-event-1",
            "repo-1", "run-1", "item-1", "effect-1", "plan-1",
            "revision-1", "check-1", "VALIDATOR_OBSERVATION",
            "validator-observation-1", pending_observation.event_hash,
            "PASSED", "validator-intent-1", "validator-attempt-1",
            "cessation-1", cessation.event_hash,
        )
        with self.assertRaisesRegex(
            DispatchDenied, "does not bind cessation proof"
        ):
            self.store.settle_terminal_validation(
                replace(
                    request,
                    terminal_settlement_id="wrong-cessation-settlement",
                    command_id="wrong-cessation-command",
                    event_id="wrong-cessation-event",
                    cessation_event_hash="wrong-cessation-hash",
                )
            )
        with self.assertRaises(InjectedFailure):
            self.store.settle_terminal_validation(
                request,
                failure_hook=raise_at(
                    "after_terminal_settlement_writes_before_commit"
                ),
            )
        self.assertEqual(
            self.store.table_counts()["terminal_validation_settlements"], 0
        )
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

        with self.assertRaises(InjectedFailure):
            self.store.settle_terminal_validation(
                request,
                failure_hook=raise_at(
                    "after_terminal_settlement_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            terminal_hash = connection.execute(
                "SELECT event_hash FROM terminal_validation_settlements WHERE "
                "terminal_settlement_id = 'terminal-settlement-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = terminal_hash
        reopened = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        )
        replay = reopened.settle_terminal_validation(request)

        self.assertTrue(replay.replayed)
        self.assertFalse(replay.slot_released)
        self.assertEqual(replay.resulting_state, LifecycleState.STOPPED)
        misbound_path = self.database_path.parent / "misbound-t26.sqlite3"
        shutil.copy2(self.database_path, misbound_path)
        connection = sqlite3.connect(misbound_path)
        connection.row_factory = sqlite3.Row
        try:
            row = connection.execute(
                "SELECT body_json FROM terminal_validation_settlements WHERE "
                "terminal_settlement_id = 'terminal-settlement-1'"
            ).fetchone()
            body = json.loads(row["body_json"])
            body["source_event_hash"] = "forged-observation-hash"
            request_body = {
                key: body[key]
                for key in TerminalValidationSettlementRequest.__dataclass_fields__
            }
            payload_digest = self.store._event_hash(request_body)
            obligation_proof_key = self.store._event_hash(
                {
                    key: value
                    for key, value in request_body.items()
                    if key not in {
                        "terminal_settlement_id", "command_id", "event_id"
                    }
                }
            )
            body["obligation_proof_key"] = obligation_proof_key
            misbound_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                "event_id = 'terminal-event-1'",
                (misbound_hash, body_json),
            )
            connection.execute(
                "UPDATE terminal_validation_settlements SET "
                "source_event_hash = ?, obligation_proof_key = ?, "
                "payload_digest = ?, event_hash = ?, body_json = ? WHERE "
                "terminal_settlement_id = 'terminal-settlement-1'",
                (
                    "forged-observation-hash", obligation_proof_key,
                    payload_digest, misbound_hash, body_json,
                ),
            )
            connection.execute(
                "UPDATE command_outcomes SET payload_digest = ?, "
                "event_hash = ? WHERE command_id = 'terminal-command-1'",
                (payload_digest, misbound_hash),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (misbound_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE "
                "repository_id = 'repo-1'",
                (misbound_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        misbound_oracle = MutableFreshnessOracle()
        misbound_oracle.allowed_head = misbound_hash
        with self.assertRaisesRegex(
            StorageIntegrityError, "result/cessation binding is invalid"
        ):
            SQLiteStateStore(
                misbound_path, misbound_oracle, "repo-1"
            ).load_verified("repo-1")
        tampered_path = self.database_path.parent / "tampered-t26.sqlite3"
        shutil.copy2(self.database_path, tampered_path)
        connection = sqlite3.connect(tampered_path)
        connection.row_factory = sqlite3.Row
        try:
            row = connection.execute(
                "SELECT body_json FROM terminal_validation_settlements WHERE "
                "terminal_settlement_id = 'terminal-settlement-1'"
            ).fetchone()
            body = json.loads(row["body_json"])
            body["slot_released"] = True
            tampered_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                "event_id = 'terminal-event-1'",
                (tampered_hash, body_json),
            )
            connection.execute(
                "UPDATE terminal_validation_settlements SET event_hash = ?, "
                "slot_released = 1, body_json = ? WHERE "
                "terminal_settlement_id = 'terminal-settlement-1'",
                (tampered_hash, body_json),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE "
                "command_id = 'terminal-command-1'",
                (tampered_hash,),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (tampered_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE "
                "repository_id = 'repo-1'",
                (tampered_hash,),
            )
            connection.execute(
                "DELETE FROM outstanding_slot WHERE repository_id = 'repo-1'"
            )
            connection.commit()
        finally:
            connection.close()
        tampered_oracle = MutableFreshnessOracle()
        tampered_oracle.allowed_head = tampered_hash
        with self.assertRaisesRegex(
            StorageIntegrityError, "required validation checks remain unsettled"
        ):
            SQLiteStateStore(
                tampered_path, tampered_oracle, "repo-1"
            ).load_verified("repo-1")
        connection = sqlite3.connect(self.database_path)
        try:
            plan_hash = connection.execute(
                "SELECT event_hash FROM validation_plans WHERE plan_id = 'plan-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        final = reopened.settle_terminal_validation(
            TerminalValidationSettlementRequest(
                "terminal-settlement-2", "terminal-command-2",
                "terminal-event-2", "repo-1", "run-1", "item-1",
                "effect-1", "plan-1", "revision-1", "check-2", "PLAN",
                "plan-1", plan_hash, "CANCELLED_WITHOUT_START",
            )
        )
        self.oracle.allowed_head = final.event_hash
        self.assertTrue(final.slot_released)
        self.assertEqual(final.resulting_state, LifecycleState.STOPPED)
        self.assertEqual(reopened.table_counts()["outstanding_slot"], 0)
        reopened.load_verified("repo-1")

    def test_t26_before_t23_recovers_without_releasing_slot(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1", "check-2"),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        committed = self.store.commit_intent(
            self.request(), self.capability, self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        self.oracle.allowed_head = committed.event_hash
        self._stop_run()
        early = self.store.settle_terminal_validation(
            TerminalValidationSettlementRequest(
                "terminal-settlement-1", "terminal-command-1",
                "terminal-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "plan-1", "revision-1", "check-1", "PLAN",
                "plan-1", plan.event_hash, "CANCELLED_WITHOUT_START",
            )
        )
        self.oracle.allowed_head = early.event_hash
        self.assertFalse(early.slot_released)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

        tampered_path = self.database_path.parent / "tampered-t26-slot.sqlite3"
        shutil.copy2(self.database_path, tampered_path)
        connection = sqlite3.connect(tampered_path)
        connection.row_factory = sqlite3.Row
        try:
            row = connection.execute(
                "SELECT body_json FROM terminal_validation_settlements WHERE "
                "terminal_settlement_id = 'terminal-settlement-1'"
            ).fetchone()
            body = json.loads(row["body_json"])
            body["slot_attempt_id"] = "forged-attempt"
            tampered_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                "event_id = 'terminal-event-1'",
                (tampered_hash, body_json),
            )
            connection.execute(
                "UPDATE terminal_validation_settlements SET "
                "slot_attempt_id = 'forged-attempt', event_hash = ?, "
                "body_json = ? WHERE terminal_settlement_id = "
                "'terminal-settlement-1'",
                (tampered_hash, body_json),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE "
                "command_id = 'terminal-command-1'",
                (tampered_hash,),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (tampered_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE "
                "repository_id = 'repo-1'",
                (tampered_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        tampered_oracle = MutableFreshnessOracle()
        tampered_oracle.allowed_head = tampered_hash
        with self.assertRaisesRegex(
            StorageIntegrityError, "operation slot attempt"
        ):
            SQLiteStateStore(
                tampered_path, tampered_oracle, "repo-1"
            ).load_verified("repo-1")

        reopened = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        )
        reopened._bind_classification_authority(self.authority)
        reopened.load_verified("repo-1")
        late = reopened._record_effect_observation(
            EffectObservationRequest(
                "late-observation-1", "late-observe-command-1",
                "late-observation-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "attempt-1", "late-receipt-1",
                self.capability.claim_id, "descriptor-digest", 2,
                "late-settlement-1", "",
            )
        )
        self.oracle.allowed_head = late.event_hash
        reopened.load_verified("repo-1")
        final = reopened.settle_terminal_validation(
            TerminalValidationSettlementRequest(
                "terminal-settlement-2", "terminal-command-2",
                "terminal-event-2", "repo-1", "run-1", "item-1",
                "effect-1", "plan-1", "revision-1", "check-2", "PLAN",
                "plan-1", plan.event_hash, "CANCELLED_WITHOUT_START",
            )
        )
        self.oracle.allowed_head = final.event_hash
        self.assertTrue(final.slot_released)
        self.assertEqual(reopened.table_counts()["outstanding_slot"], 0)
        reopened.load_verified("repo-1")

    def test_t26_last_check_before_t23_releases_slot_on_late_receipt(
        self,
    ) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        committed = self.store.commit_intent(
            self.request(), self.capability, self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        self.oracle.allowed_head = committed.event_hash
        self._stop_run()
        early = self.store.settle_terminal_validation(
            TerminalValidationSettlementRequest(
                "terminal-settlement-1", "terminal-command-1",
                "terminal-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "plan-1", "revision-1", "check-1", "PLAN",
                "plan-1", plan.event_hash, "CANCELLED_WITHOUT_START",
            )
        )
        self.oracle.allowed_head = early.event_hash
        self.assertFalse(early.slot_released)

        reopened = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        )
        reopened._bind_classification_authority(self.authority)
        reopened.load_verified("repo-1")
        late = reopened._record_effect_observation(
            EffectObservationRequest(
                "late-observation-1", "late-observe-command-1",
                "late-observation-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "attempt-1", "late-receipt-1",
                self.capability.claim_id, "descriptor-digest", 2,
                "late-settlement-1", "",
            )
        )
        self.oracle.allowed_head = late.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    (late.event_id,),
                ).fetchone()[0]
            )
        finally:
            connection.close()
        self.assertTrue(body["slot_released"])
        self.assertEqual(body["slot_attempt_id"], "attempt-1")
        self.assertEqual(reopened.table_counts()["outstanding_slot"], 0)
        reopened.load_verified("repo-1")

    def test_t23_recovery_rejects_mandatory_late_receipt_slot_retention(
        self,
    ) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        committed = self.store.commit_intent(
            self.request(), self.capability, self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        self.oracle.allowed_head = committed.event_hash
        self._stop_run()
        early = self.store.settle_terminal_validation(
            TerminalValidationSettlementRequest(
                "terminal-settlement-1", "terminal-command-1",
                "terminal-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "plan-1", "revision-1", "check-1", "PLAN",
                "plan-1", plan.event_hash, "CANCELLED_WITHOUT_START",
            )
        )
        self.oracle.allowed_head = early.event_hash
        self.assertFalse(early.slot_released)
        late = self.store._record_effect_observation(
            EffectObservationRequest(
                "late-observation-1", "late-observe-command-1",
                "late-observation-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "attempt-1", "late-receipt-1",
                self.capability.claim_id, "descriptor-digest", 2,
                "late-settlement-1", "",
            )
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    (late.event_id,),
                ).fetchone()[0]
            )
            self.assertTrue(body["slot_released"])
            body["slot_released"] = False
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (event_hash, body_json, late.event_id),
            )
            connection.execute(
                "UPDATE effect_observations SET event_hash = ?, body_json = ? "
                "WHERE observation_id = ?",
                (event_hash, body_json, late.observation_id),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                (event_hash, late.command_id),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = ?",
                (event_hash, "run-1"),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, "repo-1"),
            )
            connection.execute(
                "INSERT INTO outstanding_slot VALUES (1, ?, ?, ?, ?, 1)",
                ("repo-1", "run-1", "effect-1", "attempt-1"),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(
            StorageIntegrityError, "effect observation semantics"
        ):
            self.store.load_verified("repo-1")

    def test_t23_correction_after_t26_releases_failed_final_slot(
        self,
    ) -> None:
        observation = self._record_validator_result(verdict="FAIL")
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1", "validator-observation-1",
            ),
            classification=self._classification(observation, "FINAL"),
        )
        self.oracle.allowed_head = applied.event_hash
        unknown = self.store._record_effect_observation(
            EffectObservationRequest(
                "late-unknown-observation", "late-unknown-command",
                "late-unknown-event", "repo-1", "run-1", "item-1",
                "effect-1", "attempt-1", "late-unknown-receipt",
                self.capability.claim_id, "descriptor-digest", None,
                "late-unknown-settlement", "",
            )
        )
        self.oracle.allowed_head = unknown.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            plan_hash = connection.execute(
                "SELECT event_hash FROM validation_plans WHERE plan_id = 'plan-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        terminal = self.store.settle_terminal_validation(
            TerminalValidationSettlementRequest(
                "terminal-settlement-1", "terminal-command-1",
                "terminal-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "plan-1", "revision-1", "check-2", "PLAN",
                "plan-1", plan_hash, "CANCELLED_WITHOUT_START",
            )
        )
        self.oracle.allowed_head = terminal.event_hash
        self.assertFalse(terminal.slot_released)

        corrected = self.store._record_effect_observation(
            EffectObservationRequest(
                "late-known-observation", "late-known-command",
                "late-known-event", "repo-1", "run-1", "item-1",
                "effect-1", "attempt-1", "late-known-receipt",
                self.capability.claim_id, "descriptor-digest", 3,
                "late-known-settlement", "",
            )
        )
        self.oracle.allowed_head = corrected.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    (corrected.event_id,),
                ).fetchone()[0]
            )
        finally:
            connection.close()
        self.assertEqual(corrected.resulting_state, LifecycleState.FAILED_FINAL)
        self.assertTrue(body["slot_released"])
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.store.load_verified("repo-1")

    def test_t26_settles_started_validator_from_authoritative_cessation(
        self,
    ) -> None:
        parent = self._record_effect_observation(check_ids=("check-1",))
        intent, capability = self._validator_intent(parent)
        committed = self.store.commit_validator_intent(
            intent, capability, self.authority
        )
        self.oracle.allowed_head = committed.event_hash
        cessation = self._record_validator_cessation_for()
        settlement_request = BudgetSettlementRequest(
            "validator-settlement-1", "validator-reservation-1", "",
            BudgetDisposition.CONSUMED, 1, "cessation-1",
            "VALIDATOR_CESSATION_COST_SETTLED",
        )
        settlement = self.store._settle_budget(
            settlement_request,
            self.authority.issue_settlement_proof(
                "validator-settlement-proof-1", settlement_request
            ),
            self.authority,
        )
        self.oracle.allowed_head = settlement.settlement_hash
        self._stop_run()
        request = TerminalValidationSettlementRequest(
            "terminal-settlement-1", "terminal-command-1", "terminal-event-1",
            "repo-1", "run-1", "item-1", "effect-1", "plan-1",
            "revision-1", "check-1", "VALIDATOR_CESSATION",
            "cessation-1", cessation.event_hash, "CANCELLED_AFTER_START",
            "validator-intent-1", "validator-attempt-1", "cessation-1",
            cessation.event_hash,
        )
        settled = self.store.settle_terminal_validation(request)
        self.oracle.allowed_head = settled.event_hash
        replay = self.store.settle_terminal_validation(
            replace(
                request,
                terminal_settlement_id="terminal-settlement-retry",
                command_id="terminal-command-retry",
                event_id="terminal-event-retry",
            )
        )

        self.assertEqual(settled.resulting_state, LifecycleState.STOPPED)
        self.assertTrue(settled.slot_released)
        self.assertTrue(replay.replayed)
        self.assertEqual(replay.terminal_settlement_id, "terminal-settlement-1")
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.assertEqual(
            self.store.table_counts()["terminal_validation_settlements"], 1
        )
        self.store.load_verified("repo-1")

    def test_t24_retains_result_after_t26_started_cancellation(self) -> None:
        parent = self._record_effect_observation(check_ids=("check-1",))
        intent, capability = self._validator_intent(parent)
        committed = self.store.commit_validator_intent(
            intent, capability, self.authority
        )
        self.oracle.allowed_head = committed.event_hash
        cessation = self._record_validator_cessation_for(
            result_available=True
        )
        settlement_request = BudgetSettlementRequest(
            "validator-settlement-1", "validator-reservation-1", "",
            BudgetDisposition.CONSUMED, 1, "validator-result-1",
            "VALIDATOR_USAGE_REPORTED",
        )
        settlement = self.store._settle_budget(
            settlement_request,
            self.authority.issue_settlement_proof(
                "validator-settlement-proof-1", settlement_request
            ),
            self.authority,
        )
        self.oracle.allowed_head = settlement.settlement_hash
        self._stop_run()
        terminal = self.store.settle_terminal_validation(
            TerminalValidationSettlementRequest(
                "terminal-settlement-1", "terminal-command-1",
                "terminal-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "plan-1", "revision-1", "check-1",
                "VALIDATOR_CESSATION", "cessation-1", cessation.event_hash,
                "CANCELLED_AFTER_START", "validator-intent-1",
                "validator-attempt-1", "cessation-1", cessation.event_hash,
            )
        )
        self.oracle.allowed_head = terminal.event_hash
        late = self.store._record_validator_observation(
            ValidatorObservationRequest(
                "validator-observation-1", "validator-observe-command-1",
                "validator-observation-event-1", "repo-1", "run-1",
                "item-1", "effect-1", "validator-intent-1",
                "validator-attempt-1", "validator-result-1",
                capability.claim_id, "revision-1", "check-1", "input-1",
                "result-digest-1", "PASS", 1, "validator-settlement-1",
                settlement.settlement_hash,
            )
        )
        self.oracle.allowed_head = late.event_hash

        self.assertEqual(late.resulting_state, LifecycleState.STOPPED)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        connection = sqlite3.connect(self.database_path)
        try:
            disposition = connection.execute(
                "SELECT disposition FROM terminal_validation_settlements"
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(disposition, "CANCELLED_AFTER_START")
        self.store.load_verified("repo-1")

    def test_recovery_rejects_post_terminal_cessation_state_change(self) -> None:
        parent = self._record_effect_observation(check_ids=("check-1",))
        intent, capability = self._validator_intent(parent)
        committed = self.store.commit_validator_intent(
            intent, capability, self.authority
        )
        self.oracle.allowed_head = committed.event_hash
        self._stop_run()
        cessation = self._record_validator_cessation_for()
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    (cessation.event_id,),
                ).fetchone()[0]
            )
            body["lifecycle_to"] = LifecycleState.COMPLETED.value
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? "
                "WHERE event_id = ?",
                (event_hash, body_json, cessation.event_id),
            )
            connection.execute(
                "UPDATE validator_cessations SET event_hash = ?, "
                "resulting_state = ?, body_json = ? WHERE cessation_id = ?",
                (
                    event_hash, LifecycleState.COMPLETED.value, body_json,
                    cessation.cessation_id,
                ),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                (event_hash, cessation.command_id),
            )
            connection.execute(
                "UPDATE runs SET lifecycle_state = ?, head_hash = ? WHERE run_id = ?",
                (LifecycleState.COMPLETED.value, event_hash, "run-1"),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, "repo-1"),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(
            StorageIntegrityError, "terminal lifecycle"
        ):
            self.store.load_verified("repo-1")

    def test_t26_rejects_historical_result_after_successor_intent(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        cessation = self._record_validator_cessation_for(
            result_available=True
        )
        failed = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1", "validator-observation-1",
            ),
            classification=self._classification(observation, "RECOVERABLE"),
        )
        self.oracle.allowed_head = failed.event_hash
        recovery_request, attestation, parent_event_hash = (
            self._validation_recovery_pair(failed)
        )
        recovered = self.store.resolve_validation_blocker(
            recovery_request, attestation, self.authority
        )
        self.oracle.allowed_head = recovered.event_hash
        successor, successor_capability = self._validator_intent(
            replace(observation, event_hash=parent_event_hash),
            suffix="2", check_id="check-1", recovery_id="recovery-1",
        )
        committed = self.store.commit_validator_intent(
            successor, successor_capability, self.authority
        )
        self.oracle.allowed_head = committed.event_hash
        self._stop_run()

        with self.assertRaisesRegex(DispatchDenied, "current attempt"):
            self.store.settle_terminal_validation(
                TerminalValidationSettlementRequest(
                    "terminal-settlement-1", "terminal-command-1",
                    "terminal-event-1", "repo-1", "run-1", "item-1",
                    "effect-1", "plan-1", "revision-1", "check-1",
                    "VALIDATOR_OBSERVATION", "validator-observation-1",
                    observation.event_hash, "FAILED", "validator-intent-1",
                    "validator-attempt-1", "cessation-1",
                    cessation.event_hash,
                )
            )
        self.assertEqual(
            self.store.table_counts()["terminal_validation_settlements"], 0
        )
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

    def test_t26_rejects_terminal_history_without_permanent_fence(self) -> None:
        observation = self._record_validator_result(verdict="FAIL")
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1", "validator-observation-1",
            ),
            classification=self._classification(observation, "FINAL"),
        )
        self.oracle.allowed_head = applied.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            plan_hash = connection.execute(
                "SELECT event_hash FROM validation_plans WHERE plan_id = 'plan-1'"
            ).fetchone()[0]
            connection.execute(
                "DELETE FROM dispatch_fences WHERE fence_id = "
                "'failed-final:application-1'"
            )
            connection.commit()
        finally:
            connection.close()

        with self.assertRaisesRegex(StorageIntegrityError, "dispatch-fence"):
            self.store.settle_terminal_validation(
                TerminalValidationSettlementRequest(
                    "terminal-settlement-1", "terminal-command-1",
                    "terminal-event-1", "repo-1", "run-1", "item-1",
                    "effect-1", "plan-1", "revision-1", "check-2",
                    "PLAN", "plan-1", plan_hash,
                    "CANCELLED_WITHOUT_START",
                )
            )
        self.assertEqual(
            self.store.table_counts()["terminal_validation_settlements"], 0
        )

    def test_t26_consumes_terminal_t25_nonexecution_proof(self) -> None:
        parent = self._record_effect_observation(check_ids=("check-1",))
        validator_request, validator_capability = self._validator_intent(parent)
        committed = self.store.commit_validator_intent(
            validator_request, validator_capability, self.authority
        )
        self.oracle.allowed_head = committed.event_hash
        self._stop_run()
        validator_path = self.database_path.parent / "synthetic-validator.sqlite3"
        adapter = SyntheticValidatorAdapter(validator_path)
        adapter._canonical_repository_id = "repo-1"
        adapter._canonical_ledger_path = validator_path.resolve()
        attestation = self.authority.issue_nonexecution_attestation(
            "terminal-nonexecution-attestation", "terminal-nonexecution-seal",
            "VALIDATOR", adapter._target_digest("repo-1"),
            validator_capability.claim_id, "VALIDATOR:validator-intent-1",
            committed.event_hash, "validator-reservation-1", "repo-1",
            "run-1", "item-1", "effect-1", "validator-attempt-1",
        )
        seal = adapter.seal_nonexecution(attestation, self.authority)
        nonexecution_request = BudgetSettlementRequest(
            "terminal-nonexecution", "validator-reservation-1", "",
            BudgetDisposition.RELEASED, None, "terminal-nonexecution-evidence",
            "NONDISPATCH_PROVEN", non_dispatch_proven=True,
            zero_liability_proven=True, all_obligations_settled=True,
            attempt_id="validator-attempt-1",
            nonexecution_seal_id=seal.seal_id,
        )
        nonexecution = self.store._settle_budget(
            nonexecution_request,
            self.authority.issue_settlement_proof(
                "terminal-nonexecution-proof", nonexecution_request
            ),
            self.authority,
        )
        self.oracle.allowed_head = nonexecution.settlement_hash
        connection = sqlite3.connect(self.database_path)
        try:
            status = connection.execute(
                "SELECT status FROM validator_intents WHERE "
                "validator_intent_id = 'validator-intent-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(status, "ACTIVE")
        request = TerminalValidationSettlementRequest(
            "terminal-settlement-1", "terminal-command-1", "terminal-event-1",
            "repo-1", "run-1", "item-1", "effect-1", "plan-1",
            "revision-1", "check-1", "NONDISPATCH_PROVEN",
            "terminal-nonexecution", nonexecution.settlement_hash,
            "CANCELLED_WITHOUT_START", "validator-intent-1",
            "validator-attempt-1",
        )
        settled = self.store.settle_terminal_validation(request)
        self.oracle.allowed_head = settled.event_hash

        self.assertEqual(settled.resulting_state, LifecycleState.STOPPED)
        self.assertTrue(settled.slot_released)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.store.load_verified("repo-1")

    def test_c05_final_failure_with_unsettled_accounting_retains_slot(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE budget_reservations SET disposition = 'RELEASED' "
                "WHERE reservation_id = 'reservation-1'"
            )
            connection.commit()
        finally:
            connection.close()

        with patch.object(self.store, "_verify_projections"):
            applied = self.store._apply_validator_observation(
                ValidationApplicationRequest(
                    "application-1", "apply-command-1", "apply-event-1",
                    "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                    "check-1", "validator-attempt-1",
                    "validator-observation-1",
                ),
                classification=self._classification(observation, "FINAL"),
            )

        self.assertEqual(applied.resulting_state.value, "FAILED_FINAL")
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

    def test_c05_final_fence_denies_matching_item_or_effect(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1", "validator-observation-1",
            ),
            classification=self._classification(observation, "FINAL"),
        )
        self.oracle.allowed_head = applied.event_hash
        for suffix, item_id, effect_id, writer_epoch in (
            ("same-item", "item-1", "effect-2", 30),
            ("same-effect", "item-2", "effect-1", 32),
        ):
            grant = SyntheticGrant(
                f"grant-{suffix}", "repo-1", effect_id, f"attempt-{suffix}",
                f"scope-{suffix}",
            )
            self.authority.register(grant)
            capability = self.authority.claim(*grant.__dict__.values())
            with self.subTest(scope=suffix), self.assertRaisesRegex(
                DispatchDenied, "dispatch fence"
            ):
                self._commit_planned_intent(
                    replace(
                        self.request(), run_id=f"run-{suffix}", item_id=item_id,
                        command_id=f"command-{suffix}",
                        event_id=f"event-{suffix}", logical_effect_id=effect_id,
                        attempt_id=f"attempt-{suffix}",
                        permission_use_id=f"permission-{suffix}",
                        reservation_id=f"reservation-{suffix}",
                    ),
                    capability, self.authority,
                    expected_head=self.oracle.allowed_head,
                    writer_epoch=writer_epoch,
                )

    def test_c05_exact_replay_rejects_rebound_request(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        request = ValidationApplicationRequest(
            "application-1", "apply-command-1", "apply-event-1",
            "repo-1", "run-1", "item-1", "effect-1", "revision-1",
            "check-1", "validator-attempt-1", "validator-observation-1",
        )
        applied = self.store._apply_validator_observation(
            request, classification=self._classification(observation, "FINAL")
        )
        self.oracle.allowed_head = applied.event_hash
        for rebound in (
            replace(request, item_id="item-2"),
            replace(request, revision_digest="revision-2"),
            replace(request, validator_attempt_id="validator-attempt-2"),
        ):
            with self.subTest(rebound=rebound):
                with self.assertRaisesRegex(StorageIntegrityError, "identity"):
                    self.store._apply_validator_observation(rebound)

    def test_c05_replay_rejects_supplied_contradictory_classification(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        request = ValidationApplicationRequest(
            "application-1", "apply-command-1", "apply-event-1",
            "repo-1", "run-1", "item-1", "effect-1", "revision-1",
            "check-1", "validator-attempt-1", "validator-observation-1",
        )
        applied = self.store._apply_validator_observation(
            request, classification=self._classification(observation, "FINAL")
        )
        self.oracle.allowed_head = applied.event_hash
        contradictory = self.authority.issue_classification(
            "classification-contradictory", "repo-1", "run-1", "item-1",
            "effect-1", "revision-1", "check-1", "validator-attempt-1",
            "validator-observation-1", observation.event_hash,
            "result-digest-1", verdict="FAIL", policy_id="failure-policy",
            policy_version="1", classification="RECOVERABLE",
        )
        with self.assertRaisesRegex(StorageIntegrityError, "contradictory"):
            self.store._apply_validator_observation(
                request, classification=contradictory
            )

    def test_c05_rejects_replacement_issuer_after_restart(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        replacement = SyntheticAuthority(b"r" * 32)
        reopened = SQLiteStateStore(self.database_path, self.oracle, "repo-1")
        with self.assertRaisesRegex(DispatchDenied, "accepted plan"):
            reopened._bind_classification_authority(replacement)
        self.assertEqual(observation.resulting_state, LifecycleState.VALIDATING)

    def test_c05_rejects_tampered_event_history_before_application(self) -> None:
        self._record_validator_result(verdict="FAIL", only_check=True)
        connection = sqlite3.connect(self.database_path)
        try:
            body_json = connection.execute(
                "SELECT body_json FROM events "
                "WHERE event_id = 'validator-observation-event-1'"
            ).fetchone()[0]
            body = json.loads(body_json)
            body["verdict"] = "PASS"
            connection.execute(
                "UPDATE events SET body_json = ? "
                "WHERE event_id = 'validator-observation-event-1'",
                (json.dumps(body, sort_keys=True, separators=(",", ":")),),
            )
            connection.execute(
                "UPDATE validator_observations SET verdict = 'PASS' "
                "WHERE observation_id = 'validator-observation-1'"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(StorageIntegrityError, "event body hash"):
            self.store._apply_validator_observation(
                ValidationApplicationRequest(
                    "application-1", "apply-command-1", "apply-event-1",
                    "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                    "check-1", "validator-attempt-1",
                    "validator-observation-1",
                )
            )
        self.assertEqual(self.store.table_counts()["validation_applications"], 0)

    def test_c05_classification_policy_is_closed(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        with self.assertRaisesRegex(ValueError, "unsupported.*policy"):
            self.authority.issue_classification(
                "classification-other", "repo-1", "run-1", "item-1",
                "effect-1", "revision-1", "check-1",
                "validator-attempt-1", "validator-observation-1",
                observation.event_hash, "result-digest-1", verdict="FAIL",
                policy_id="other-policy", policy_version="1",
                classification="FINAL",
            )

    def test_c05_rejects_pass_classification_and_untrusted_fail_evidence(self) -> None:
        pass_observation = self._record_validator_result(only_check=True)
        pass_classification = self.authority.issue_classification(
            "classification-pass", "repo-1", "run-1", "item-1", "effect-1",
            "revision-1", "check-1", "validator-attempt-1",
            "validator-observation-1", pass_observation.event_hash,
            "result-digest-1", verdict="FAIL", policy_id="failure-policy",
            policy_version="1", classification="FINAL",
        )
        with self.assertRaisesRegex(DispatchDenied, "PASS application"):
            self.store._apply_validator_observation(
                ValidationApplicationRequest(
                    "application-1", "apply-command-1", "apply-event-1",
                    "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                    "check-1", "validator-attempt-1",
                    "validator-observation-1",
                ),
                classification=pass_classification,
            )

    def test_c05_rejects_forged_and_rebound_failure_classification(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        valid = self._classification(observation, "FINAL")
        forged = replace(valid, issuer_mac="0" * len(valid.issuer_mac))
        rebound = self.authority.issue_classification(
            "classification-rebound", "repo-1", "run-1", "item-1",
            "effect-1", "revision-1", "check-1", "validator-attempt-1",
            "validator-observation-1", "wrong-event-hash", "result-digest-1",
            verdict="FAIL", policy_id="failure-policy", policy_version="1",
            classification="FINAL",
        )
        for evidence in (forged, rebound):
            with self.subTest(classification_id=evidence.classification_id):
                with self.assertRaises(DispatchDenied):
                    self.store._apply_validator_observation(
                        ValidationApplicationRequest(
                            "application-1", "apply-command-1", "apply-event-1",
                            "repo-1", "run-1", "item-1", "effect-1",
                            "revision-1", "check-1", "validator-attempt-1",
                            "validator-observation-1",
                        ),
                        classification=evidence,
                    )
        self.assertEqual(self.store.table_counts()["validation_applications"], 0)

    def test_c05_recovery_rejects_tampered_classification_projection(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1", "validator-observation-1",
            ),
            classification=self._classification(observation, "FINAL"),
        )
        self.oracle.allowed_head = applied.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE validation_applications SET classification = 'RECOVERABLE' "
                "WHERE application_id = 'application-1'"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(StorageIntegrityError, "validation-application"):
            self.store.load_verified("repo-1")

    def test_c05_recovery_rejects_tampered_final_fence_scope(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1", "validator-observation-1",
            ),
            classification=self._classification(observation, "FINAL"),
        )
        self.oracle.allowed_head = applied.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE dispatch_fences SET item_id = 'item-2' "
                "WHERE reason_code = 'FAILED_FINAL_APPLICATION'"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(StorageIntegrityError, "dispatch-fence"):
            self.store.load_verified("repo-1")

    def test_c05_recovery_rejects_released_terminal_accounting(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1", "validator-observation-1",
            ),
            classification=self._classification(observation, "FINAL"),
        )
        self.oracle.allowed_head = applied.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE budget_reservations SET disposition = 'RELEASED' "
                "WHERE reservation_id = 'reservation-1'"
            )
            connection.commit()
        finally:
            connection.close()

        with self.assertRaises(StorageIntegrityError):
            self.store.load_verified("repo-1")

    def test_c05_late_unknown_accounting_recovers_for_correction(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1", "validator-observation-1",
            ),
            classification=self._classification(observation, "FINAL"),
        )
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.oracle.allowed_head = applied.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            previous_hash = connection.execute(
                "SELECT settlement_head_hash FROM budget_reservations "
                "WHERE reservation_id = 'reservation-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        unknown = BudgetSettlementRequest(
            "failed-final-late-unknown", "reservation-1", previous_hash,
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "failed-final-late-evidence", "ADDITIONAL_LIABILITY_UNKNOWN",
            additional_liability=True,
        )
        unknown_receipt = self.store._settle_budget(
            unknown,
            self.authority.issue_settlement_proof(
                "failed-final-late-proof", unknown
            ),
            self.authority,
        )
        self.oracle.allowed_head = unknown_receipt.settlement_hash
        reopened = SQLiteStateStore(self.database_path, self.oracle, "repo-1")
        reopened._bind_classification_authority(self.authority)
        reopened.load_verified("repo-1")

        correction = BudgetSettlementRequest(
            "failed-final-late-correction", "reservation-1",
            unknown_receipt.settlement_hash, BudgetDisposition.ADJUSTED, 3,
            "failed-final-authoritative-evidence", "AUTHORITATIVE_CORRECTION",
        )
        corrected = reopened._settle_budget(
            correction,
            self.authority.issue_settlement_proof(
                "failed-final-correction-proof", correction
            ),
            self.authority,
        )
        self.oracle.allowed_head = corrected.settlement_hash
        reopened.load_verified("repo-1")
        connection = sqlite3.connect(self.database_path)
        try:
            charged_units, uncertainty, lifecycle_state = connection.execute(
                "SELECT b.charged_units, b.uncertainty, r.lifecycle_state "
                "FROM budget_reservations b JOIN runs r ON r.run_id = b.run_id "
                "WHERE b.reservation_id = 'reservation-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual((charged_units, uncertainty), (3, 0))
        self.assertEqual(lifecycle_state, "FAILED_FINAL")
        connection = sqlite3.connect(self.database_path)
        try:
            fences = connection.execute(
                "SELECT fence_id, reason_code, originating_event_id FROM "
                "dispatch_fences ORDER BY fence_id"
            ).fetchall()
        finally:
            connection.close()
        self.assertEqual(
            fences,
            [(
                "failed-final:application-1",
                "FAILED_FINAL_APPLICATION",
                "apply-event-1",
            )],
        )
        self.assertEqual(reopened.table_counts()["outstanding_slot"], 0)

    def test_c05_recovery_rejects_tampered_application_projection(self) -> None:
        self._record_validator_result(only_check=True)
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1", "check-1",
                "validator-attempt-1", "validator-observation-1",
            ),
        )
        self.oracle.allowed_head = applied.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE validation_applications SET revision_digest = 'tampered' "
                "WHERE application_id = 'application-1'"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(StorageIntegrityError, "validation-application"):
            self.store.load_verified("repo-1")

    def test_c05_recovery_rejects_self_consistent_completed_forgery(self) -> None:
        self._record_validator_result(only_check=True)
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1",
                "validator-observation-1",
            ),
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    ("apply-event-1",),
                ).fetchone()[0]
            )
            body["lifecycle_to"] = LifecycleState.COMPLETED.value
            body["continuation_cursor"] = None
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? "
                "WHERE event_id = ?",
                (event_hash, body_json, "apply-event-1"),
            )
            connection.execute(
                "UPDATE validation_applications SET event_hash = ?, "
                "resulting_state = ?, continuation_cursor = NULL, "
                "body_json = ? WHERE application_id = ?",
                (
                    event_hash, LifecycleState.COMPLETED.value, body_json,
                    "application-1",
                ),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                (event_hash, "apply-command-1"),
            )
            connection.execute(
                "UPDATE runs SET lifecycle_state = ?, continuation_cursor = NULL, "
                "head_hash = ? WHERE run_id = ?",
                (LifecycleState.COMPLETED.value, event_hash, "run-1"),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, "repo-1"),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(
            StorageIntegrityError, "validation application semantics"
        ):
            self.store.load_verified("repo-1")

    def test_c05_recovery_rejects_self_consistent_pass_slot_release(self) -> None:
        self._record_validator_result(only_check=True)
        self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1",
                "validator-observation-1",
            ),
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    ("apply-event-1",),
                ).fetchone()[0]
            )
            body["slot_released"] = True
            connection.execute("DELETE FROM outstanding_slot")
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = self._rewrite_application_tail(body)

        with self.assertRaisesRegex(
            StorageIntegrityError, "validation application semantics"
        ):
            self.store.load_verified("repo-1")

    def test_c05_recovery_rejects_self_consistent_final_slot_retention(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1",
                "validator-observation-1",
            ),
            classification=self._classification(observation, "FINAL"),
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    ("apply-event-1",),
                ).fetchone()[0]
            )
            body["slot_released"] = False
            connection.execute(
                "INSERT INTO outstanding_slot VALUES (1, ?, ?, ?, ?, 1)",
                ("repo-1", "run-1", "effect-1", "attempt-1"),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = self._rewrite_application_tail(body)

        with self.assertRaisesRegex(
            StorageIntegrityError, "validation application semantics"
        ):
            self.store.load_verified("repo-1")

    def test_t27_validator_intent_is_atomic_replay_safe_and_subordinate_to_slot(self) -> None:
        observation = self._record_effect_observation()
        request, capability = self._validator_intent(observation)

        with self.assertRaises(InjectedFailure):
            self.store.commit_validator_intent(
                request,
                capability,
                self.authority,
                failure_hook=raise_at("after_validator_intent_writes_before_commit"),
            )
        self.assertEqual(self.store.table_counts()["validator_intents"], 0)
        self.assertEqual(self.store.table_counts()["budget_reservations"], 1)

        with self.assertRaises(InjectedFailure):
            self.store.commit_validator_intent(
                request,
                capability,
                self.authority,
                failure_hook=raise_at(
                    "after_validator_intent_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            validator_hash = connection.execute(
                "SELECT event_hash FROM validator_intents WHERE validator_intent_id = 'validator-intent-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = validator_hash
        replay = self.store.commit_validator_intent(
            request, capability, self.authority
        )

        self.assertTrue(replay.replayed)
        self.assertEqual(replay.event_hash, validator_hash)
        self.assertEqual(self.store.table_counts()["validator_intents"], 1)

    def test_t27_validator_contact_rejects_any_durable_request_change(self) -> None:
        observation = self._record_effect_observation(check_ids=("check-1",))
        request, capability = self._validator_intent(observation)
        committed = self.store.commit_validator_intent(
            request, capability, self.authority
        )
        self.oracle.allowed_head = committed.event_hash
        changed = replace(request, cap_units=request.cap_units + 1)
        with self.assertRaisesRegex(DispatchDenied, "changed the durable"):
            self.store._contact_committed_validator(
                changed,
                capability,
                committed,
                self.store._adapter_target_digest("repo-1", "VALIDATOR"),
                self.authority,
            )
        with self.assertRaisesRegex(DispatchDenied, "was not issued here"):
            self.store._contact_committed_validator(
                request,
                replace(capability, issuer_mac="forged-mac"),
                committed,
                self.store._adapter_target_digest("repo-1", "VALIDATOR"),
                self.authority,
            )
        replacement_authority = SyntheticAuthority(b"r" * 32)
        with self.assertRaisesRegex(DispatchDenied, "accepted plan"):
            self.store._contact_committed_validator(
                request,
                capability,
                committed,
                self.store._adapter_target_digest("repo-1", "VALIDATOR"),
                replacement_authority,
            )
        connection = sqlite3.connect(self.database_path)
        try:
            contact_count = connection.execute(
                "SELECT COUNT(*) FROM adapter_contacts"
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(contact_count, 0)
        self.assertEqual(self.store.table_counts()["budget_reservations"], 2)
        self.assertEqual(self.store.table_counts()["effect_observations"], 1)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        self.store.load_verified("repo-1")

    def test_t27_validator_contact_denies_on_fence_alone(self) -> None:
        observation = self._record_effect_observation(check_ids=("check-1",))
        request, capability = self._validator_intent(observation)
        committed = self.store.commit_validator_intent(
            request, capability, self.authority
        )
        self.oracle.allowed_head = committed.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "INSERT INTO dispatch_fences VALUES (?, ?, ?, ?, ?, ?)",
                (
                    "test-fence", "repo-1", None, None,
                    "TEST_ONLY_FENCE", "test-origin",
                ),
            )
            connection.commit()
        finally:
            connection.close()

        with patch.object(self.store, "_verify_projections", return_value=None):
            with self.assertRaisesRegex(
                DispatchDenied, "active dispatch fence"
            ):
                self.store._contact_committed_validator(
                    request,
                    capability,
                    committed,
                    self.store._adapter_target_digest("repo-1", "VALIDATOR"),
                    self.authority,
                )

        connection = sqlite3.connect(self.database_path)
        try:
            contact_count = connection.execute(
                "SELECT COUNT(*) FROM adapter_contacts"
            ).fetchone()[0]
            reservation, fence = (
                connection.execute(
                    "SELECT disposition, settlement_head_hash FROM "
                    "budget_reservations WHERE reservation_id = ?",
                    (request.reservation_id,),
                ).fetchone(),
                connection.execute(
                    "SELECT fence_id, reason_code, originating_event_id FROM "
                    "dispatch_fences"
                ).fetchone(),
            )
        finally:
            connection.close()
        self.assertEqual(contact_count, 0)
        self.assertEqual(reservation, ("RESERVED", ""))
        self.assertEqual(fence, ("test-fence", "TEST_ONLY_FENCE", "test-origin"))

    def test_validator_contact_claim_prevents_non_dispatch_release(self) -> None:
        observation = self._record_effect_observation(check_ids=("check-1",))
        request, capability = self._validator_intent(observation)
        committed = self.store.commit_validator_intent(
            request, capability, self.authority
        )
        self.oracle.allowed_head = committed.event_hash
        self.store._contact_committed_validator(
            request,
            capability,
            committed,
            self.store._adapter_target_digest("repo-1", "VALIDATOR"),
            self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            contact_hash = connection.execute(
                "SELECT event_hash FROM adapter_contacts WHERE "
                "contact_kind = 'VALIDATOR'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = contact_hash
        release = BudgetSettlementRequest(
            "validator-release-1", "validator-reservation-1", "",
            BudgetDisposition.RELEASED, None, "non-dispatch-evidence",
            "NONDISPATCH_PROVEN", non_dispatch_proven=True,
            zero_liability_proven=True,
            attempt_id="validator-attempt-1",
        )
        connection = sqlite3.connect(self.database_path)
        try:
            before_denial = tuple(connection.iterdump())
        finally:
            connection.close()
        with self.assertRaisesRegex(
            DispatchDenied, "canonical nonexecution seal"
        ):
            self.store._settle_budget(
                release,
                self.authority.issue_settlement_proof(
                    "validator-release-proof-1", release
                ),
                self.authority,
            )
        connection = sqlite3.connect(self.database_path)
        try:
            after_denial = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_denial, before_denial)

    def test_state_owner_intents_enforce_accepted_plan_issuer_after_restart(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="",
            writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        replacement = SyntheticAuthority(b"r" * 32)
        replacement_grant = SyntheticGrant(
            "replacement-grant", "repo-1", "effect-1", "attempt-1", "scope-1"
        )
        replacement.register(replacement_grant)
        replacement_capability = replacement.claim(
            *replacement_grant.__dict__.values()
        )
        reopened = SQLiteStateStore(self.database_path, self.oracle, "repo-1")
        connection = sqlite3.connect(self.database_path)
        try:
            before_denial = tuple(connection.iterdump())
        finally:
            connection.close()
        with self.assertRaisesRegex(DispatchDenied, "accepted plan"):
            reopened.commit_intent(
                self.request(), replacement_capability, replacement,
                expected_head=plan.event_hash, writer_epoch=2,
            )
        connection = sqlite3.connect(self.database_path)
        try:
            after_denial = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_denial, before_denial)

    def test_t27_denies_check_not_declared_by_accepted_plan(self) -> None:
        observation = self._record_effect_observation()
        request, capability = self._validator_intent(observation, suffix="3")
        with self.assertRaisesRegex(DispatchDenied, "not declared"):
            self.store.commit_validator_intent(request, capability, self.authority)
        self.assertEqual(self.store.table_counts()["validator_intents"], 0)

    def test_t27_denies_another_active_validator_and_budget_over_cap(self) -> None:
        observation = self._record_effect_observation()
        first_request, first_capability = self._validator_intent(observation)
        first = self.store.commit_validator_intent(
            first_request, first_capability, self.authority
        )
        self.oracle.allowed_head = first.event_hash
        second_request, second_capability = self._validator_intent(
            observation, suffix="2"
        )
        with self.assertRaisesRegex(DispatchDenied, "active"):
            self.store.commit_validator_intent(
                second_request, second_capability, self.authority
            )

        second_store = SQLiteStateStore(
            Path(self.temporary_directory.name) / "budget-state.sqlite3",
            MutableFreshnessOracle(),
            "repo-1",
        )
        second_authority = SyntheticAuthority()
        second_store._bind_classification_authority(second_authority)
        second_authority.register(
            SyntheticGrant("grant-1", "repo-1", "effect-1", "attempt-1", "scope-1")
        )
        second_capability = second_authority.claim(
            "grant-1", "repo-1", "effect-1", "attempt-1", "scope-1"
        )
        original_store, original_authority, original_capability, original_oracle = (
            self.store,
            self.authority,
            self.capability,
            self.oracle,
        )
        try:
            self.store = second_store
            self.authority = second_authority
            self.capability = second_capability
            self.oracle = second_store._freshness_oracle
            second_observation = self._record_effect_observation()
            over_cap_request, over_cap_capability = self._validator_intent(
                second_observation, cap_units=2
            )
            with self.assertRaisesRegex(DispatchDenied, "budget cap"):
                second_store.commit_validator_intent(
                    over_cap_request, over_cap_capability, second_authority
                )
        finally:
            self.store, self.authority, self.capability, self.oracle = (
                original_store,
                original_authority,
                original_capability,
                original_oracle,
            )

    def test_t27_rejects_stale_parent_and_tampered_projection(self) -> None:
        observation = self._record_effect_observation()
        stale_request, stale_capability = self._validator_intent(observation)
        stale_request = ValidatorIntentRequest(
            **{**stale_request.__dict__, "parent_event_hash": "stale-hash"}
        )
        with self.assertRaisesRegex(DispatchDenied, "parent observation"):
            self.store.commit_validator_intent(
                stale_request, stale_capability, self.authority
            )

        request, capability = self._validator_intent(observation, suffix="2")
        committed = self.store.commit_validator_intent(
            request, capability, self.authority
        )
        self.oracle.allowed_head = committed.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE validator_intents SET input_digest = 'tampered' WHERE validator_intent_id = ?",
                (request.validator_intent_id,),
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(StorageIntegrityError, "validator-intent projection"):
            self.store.load_verified("repo-1")

    def test_t27_denies_when_repository_has_derived_dispatch_fence(self) -> None:
        observation = self._record_effect_observation()
        connection = sqlite3.connect(self.database_path)
        try:
            previous_hash = connection.execute(
                "SELECT settlement_head_hash FROM budget_reservations WHERE reservation_id = 'reservation-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        settlement_request = BudgetSettlementRequest(
            "settlement-2",
            "reservation-1",
            previous_hash,
            BudgetDisposition.ADJUSTED,
            11,
            "receipt-adjustment-1",
            "AUTHORITATIVE_CORRECTION",
        )
        proof = self.authority.issue_settlement_proof(
            "proof-2", settlement_request
        )
        breached = self.store._settle_budget(
            settlement_request,
            proof,
            self.authority,
        )
        self.oracle.allowed_head = breached.settlement_hash
        request, capability = self._validator_intent(
            observation, cap_units=20
        )

        with self.assertRaisesRegex(DispatchDenied, "active dispatch fence"):
            self.store.commit_validator_intent(
                request, capability, self.authority
            )
        self.assertEqual(self.store.table_counts()["validator_intents"], 0)

    def test_t24_result_intake_is_atomic_replay_safe_and_remains_unapplied(self) -> None:
        observation = self._record_effect_observation()
        intent_request, capability = self._validator_intent(observation)
        intent = self.store.commit_validator_intent(
            intent_request, capability, self.authority
        )
        self.oracle.allowed_head = intent.event_hash
        settlement_request = BudgetSettlementRequest(
            "validator-settlement-1",
            "validator-reservation-1",
            "",
            BudgetDisposition.CONSUMED,
            1,
            "validator-result-1",
            "VALIDATOR_USAGE_REPORTED",
        )
        proof = self.authority.issue_settlement_proof(
            "validator-proof-1",
            settlement_request,
        )
        settlement = self.store._settle_budget(
            settlement_request, proof, self.authority
        )
        self.oracle.allowed_head = settlement.settlement_hash
        request = ValidatorObservationRequest(
            "validator-observation-1",
            "validator-observe-command-1",
            "validator-observation-event-1",
            "repo-1",
            "run-1",
            "item-1",
            "effect-1",
            "validator-intent-1",
            "validator-attempt-1",
            "validator-result-1",
            capability.claim_id,
            "revision-1",
            "check-1",
            "input-1",
            "result-digest-1",
            "PASS",
            1,
            "validator-settlement-1",
            settlement.settlement_hash,
        )

        with self.assertRaises(InjectedFailure):
            self.store._record_validator_observation(
                request,
                failure_hook=raise_at(
                    "after_validator_observation_writes_before_commit"
                ),
            )
        self.assertEqual(self.store.table_counts()["validator_observations"], 0)

        with self.assertRaises(InjectedFailure):
            self.store._record_validator_observation(
                request,
                failure_hook=raise_at(
                    "after_validator_observation_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            result = connection.execute(
                "SELECT event_hash, applied FROM validator_observations WHERE observation_id = ?",
                (request.observation_id,),
            ).fetchone()
            status = connection.execute(
                "SELECT status FROM validator_intents WHERE validator_intent_id = ?",
                (request.validator_intent_id,),
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = result[0]
        replay = self.store._record_validator_observation(request)

        self.assertTrue(replay.replayed)
        self.assertEqual(result[1], 0)
        self.assertEqual(status, "ACTIVE")
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        self.store.load_verified("repo-1")

    def test_operation_slot_release_denies_after_dispatch_with_active_validator(self) -> None:
        observation = self._record_effect_observation()
        intent_request, capability = self._validator_intent(observation)
        intent = self.store.commit_validator_intent(
            intent_request, capability, self.authority
        )
        self.oracle.allowed_head = intent.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            previous_hash = connection.execute(
                "SELECT settlement_head_hash FROM budget_reservations WHERE reservation_id = 'reservation-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        release_request = BudgetSettlementRequest(
            "release-settlement-1", "reservation-1", previous_hash,
            BudgetDisposition.RELEASED, None, "receipt-1",
            "ALL_OPERATION_OBLIGATIONS_CLAIMED_SETTLED",
            non_dispatch_proven=True, zero_liability_proven=True,
            release_slot=True, all_obligations_settled=True,
        )
        proof = self.authority.issue_settlement_proof(
            "release-proof-1", release_request
        )

        with self.assertRaisesRegex(DispatchDenied, "illegal budget settlement"):
            self.store._settle_budget(
                release_request,
                proof,
                self.authority,
            )

        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        self.assertEqual(self.store.table_counts()["budget_settlements"], 1)

    def test_t24_unknown_validator_usage_is_recorded_unapplied_for_reconciliation(self) -> None:
        observation = self._record_effect_observation()
        intent_request, capability = self._validator_intent(observation)
        intent = self.store.commit_validator_intent(
            intent_request, capability, self.authority
        )
        self.oracle.allowed_head = intent.event_hash
        settlement_request = BudgetSettlementRequest(
            "validator-settlement-1", "validator-reservation-1", "",
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "validator-result-unknown-1", "VALIDATOR_USAGE_UNKNOWN",
        )
        proof = self.authority.issue_settlement_proof(
            "validator-proof-1", settlement_request
        )
        settlement = self.store._settle_budget(
            settlement_request,
            proof,
            self.authority,
        )
        self.oracle.allowed_head = settlement.settlement_hash

        recorded = self.store._record_validator_observation(
            ValidatorObservationRequest(
                "validator-observation-unknown-1", "validator-observe-unknown-command-1",
                "validator-observation-unknown-event-1", "repo-1", "run-1",
                "item-1", "effect-1", "validator-intent-1",
                "validator-attempt-1", "validator-result-unknown-1",
                capability.claim_id, "revision-1", "check-1", "input-1",
                "result-digest-unknown-1", "FAIL", None,
                "validator-settlement-1", settlement.settlement_hash,
            )
        )

        self.assertEqual(recorded.resulting_state.value, "RECONCILIATION_REQUIRED")
        connection = sqlite3.connect(self.database_path)
        try:
            row = connection.execute(
                "SELECT applied FROM validator_observations WHERE observation_id = ?",
                ("validator-observation-unknown-1",),
            ).fetchone()
            status = connection.execute(
                "SELECT status FROM validator_intents WHERE validator_intent_id = 'validator-intent-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(row[0], 0)
        self.assertEqual(status, "ACTIVE")
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

    def test_consumed_settlement_cannot_release_slot_before_finalization(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = committed.event_hash
        request = BudgetSettlementRequest(
            "settlement-1",
            "reservation-1",
            "",
            BudgetDisposition.CONSUMED,
            2,
            "usage-evidence",
            "USAGE_REPORTED",
            release_slot=True,
            all_obligations_settled=True,
        )
        proof = self.authority.issue_settlement_proof(
            "proof-1",
            request,
        )
        with self.assertRaisesRegex(DispatchDenied, "T16 finalization"):
            self.store._settle_budget(request, proof, self.authority)
        self.assertEqual(self.store.table_counts()["budget_settlements"], 0)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

    def test_budget_breach_records_fence_and_retains_operation_slot(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = committed.event_hash
        settlement = BudgetSettlementRequest(
            "settlement-1",
            "reservation-1",
            "",
            BudgetDisposition.CONSUMED,
            11,
            "usage-evidence",
            "USAGE_REPORTED",
        )
        proof = self.authority.issue_settlement_proof(
            "proof-1",
            settlement,
        )
        settlement_receipt = self.store._settle_budget(
            settlement, proof, self.authority
        )
        self.oracle.allowed_head = settlement_receipt.settlement_hash
        second_authority = self.authority
        second_authority.register(
            SyntheticGrant(
                "grant-2", "repo-1", "effect-2", "attempt-2", "scope-2"
            )
        )
        second_capability = second_authority.claim(
            "grant-2", "repo-1", "effect-2", "attempt-2", "scope-2"
        )
        second_request = IntentRequest(
            **{
                **self.request().__dict__,
                "run_id": "run-2",
                "item_id": "item-2",
                "command_id": "command-2",
                "event_id": "event-2",
                "logical_effect_id": "effect-2",
                "attempt_id": "attempt-2",
                "permission_use_id": "permission-use-2",
                "reservation_id": "reservation-2",
            }
        )
        self.assertEqual(self.store.table_counts()["dispatch_fences"], 1)
        with self.assertRaisesRegex(DispatchDenied, "repository slot"):
            self._commit_planned_intent(
                second_request,
                second_capability,
                second_authority,
                expected_head=settlement_receipt.settlement_hash,
                writer_epoch=4,
            )

    def test_freshness_rejects_snapshot_missing_complete_settlement_tail(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = committed.event_hash
        snapshot_path = Path(self.temporary_directory.name) / "pre-settlement.sqlite3"
        shutil.copy2(self.database_path, snapshot_path)
        settlement = BudgetSettlementRequest(
            "settlement-1",
            "reservation-1",
            "",
            BudgetDisposition.CONSUMED,
            2,
            "usage-evidence",
            "USAGE_REPORTED",
        )
        proof = self.authority.issue_settlement_proof(
            "proof-1",
            settlement,
        )
        settlement_receipt = self.store._settle_budget(
            settlement, proof, self.authority
        )
        self.oracle.allowed_head = settlement_receipt.settlement_hash
        stale_store = SQLiteStateStore(snapshot_path, self.oracle, "repo-1")
        with self.assertRaisesRegex(DispatchDenied, "freshness"):
            stale_store.load_verified("repo-1")

    def test_late_accounting_after_release_adds_fence_without_replacing_slot(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = committed.event_hash
        first = BudgetSettlementRequest(
            "settlement-1",
            "reservation-1",
            "",
            BudgetDisposition.RELEASED,
            None,
            "initial-usage",
            "NONDISPATCH_PROVEN",
            non_dispatch_proven=True,
            zero_liability_proven=True,
            release_slot=True,
            all_obligations_settled=True,
        )
        first_proof = self.authority.issue_settlement_proof(
            "proof-1",
            first,
        )
        first_receipt = self.store._settle_budget(first, first_proof, self.authority)
        self.oracle.allowed_head = first_receipt.settlement_hash
        late = BudgetSettlementRequest(
            "settlement-2",
            "reservation-1",
            first_receipt.settlement_hash,
            BudgetDisposition.ADJUSTED,
            3,
            "late-usage",
            "LATE_USAGE_REPORTED",
        )
        late_proof = self.authority.issue_settlement_proof(
            "proof-2",
            late,
        )
        late_receipt = self.store._settle_budget(late, late_proof, self.authority)
        self.oracle.allowed_head = late_receipt.settlement_hash

        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.assertEqual(self.store.table_counts()["dispatch_fences"], 1)
        self.store.load_verified("repo-1")

    def test_release_cannot_repeat_after_late_unknown_accounting(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        released = BudgetSettlementRequest(
            "settlement-1", "reservation-1", "", BudgetDisposition.RELEASED,
            None, "nondispatch-1", "NONDISPATCH_PROVEN",
            non_dispatch_proven=True, zero_liability_proven=True,
        )
        first = self.store._settle_budget(
            released,
            self.authority.issue_settlement_proof("proof-1", released),
            self.authority,
        )
        self.oracle.allowed_head = first.settlement_hash
        unknown = BudgetSettlementRequest(
            "settlement-2", "reservation-1", first.settlement_hash,
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "late-unknown-1", "LATE_LIABILITY_UNKNOWN",
        )
        second = self.store._settle_budget(
            unknown,
            self.authority.issue_settlement_proof("proof-2", unknown),
            self.authority,
        )
        self.oracle.allowed_head = second.settlement_hash
        repeated = BudgetSettlementRequest(
            "settlement-3", "reservation-1", second.settlement_hash,
            BudgetDisposition.RELEASED, None, "nondispatch-2",
            "NONDISPATCH_REASSERTED", non_dispatch_proven=True,
            zero_liability_proven=True,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            before_denial = tuple(connection.iterdump())
        finally:
            connection.close()

        with self.assertRaisesRegex(DispatchDenied, "already released"):
            self.store._settle_budget(
                repeated,
                self.authority.issue_settlement_proof("proof-3", repeated),
                self.authority,
            )
        connection = sqlite3.connect(self.database_path)
        try:
            after_denial = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_denial, before_denial)


if __name__ == "__main__":
    unittest.main()
