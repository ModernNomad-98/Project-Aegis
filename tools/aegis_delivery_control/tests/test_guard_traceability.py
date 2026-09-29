"""Trace the engine's advisory guard catalog to the inline checks that enforce it.

``TransitionEngine.authorize`` compares each transition's ``required_guards``
with the guards a caller reports as satisfied, but every production caller
reports the full catalog, so that comparison never denies. The guards are
enforced by inline checks in ``storage.py`` and the authority and contract
checks it calls. This module pins that calling pattern and maps each of the
69 transition-guard pairs to its inline check sites and to one test that is
denied when the guard fails.
"""

from __future__ import annotations

import ast
import functools
import importlib
from contextlib import closing
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
import shutil
import sqlite3
import sys
import unittest
from unittest.mock import patch

from tools.aegis_delivery_control.contracts import (
    BudgetDisposition,
    DispatchDenied,
    EffectObservationRequest,
    PauseExternalMutationRequest,
    ValidationApplicationRequest,
)
from tools.aegis_delivery_control.engine import TRANSITIONS
from tools.aegis_delivery_control.tests import test_storage as storage_tests

PACKAGE = Path(__file__).resolve().parents[1]
S = "test_storage.SQLiteStateStoreTests."
D = "test_dispatch.MediatedDispatchTests."
P = "test_platform.PlatformContractTests."
G = "test_guard_traceability.GuardGapTests."
OPERATOR = "authority.verify_operator_issued(capability)"
ISSUED = ("authority.py", "verify_operator_issued", "synthetic operator capability was not issued here")


def _one(module: str, function: str, marker: str):
    return ((module, function, marker),)


# (transition, guard) -> (inline check sites, test denied when the guard fails).
# A site is (module, function, marker): a raise, return or call statement in
# that function whose source or string literal contains the marker. Several
# sites mean layered checks; the test must be denied while any of them remains.
GUARD_TRACE = {
    ("T01", "definition_valid"): (_one("contracts.py", "canonical_check_order", "must be acyclic"), S + "test_t01_v2_rejects_cyclic_or_incomplete_check_bindings"),
    ("T01", "acceptance_check_present"): (_one("contracts.py", "validate", "at least one validation check"), S + "test_t01_plan_acceptance_replays_and_rejects_empty_or_tampered_checks"),
    ("T02", "history_verified"): (_one("authority.py", "verify_operation_readiness_evidence", "synthetic operation readiness is untrusted"), S + "test_t01_t02_reject_forged_trusted_evidence_before_mutation"),
    ("T02", "cursor_typed"): ((("storage.py", "_verify_projections", "continuation-cursor projection diverges from event history"), ("storage.py", "_verify_projections", "lifecycle projection diverges from event history")), S + "test_t02_unknown_cursor_fails_closed_before_append"),
    ("T03", "ready"): ((("storage.py", "commit_intent", "T03 requires current verified readiness"), ("storage.py", "_verify_current_readiness_for_intent", "T03 requires current verified readiness"), ("storage.py", "_verify_current_readiness_for_intent", "current readiness body is invalid")), S + "test_t03_denies_direct_dispatch_without_verified_readiness"),
    ("T03", "fresh"): ((("storage.py", "_verify_current_readiness_for_intent", "T03 requires current verified readiness"), ("storage.py", "_verify_current_readiness_for_intent", "T03 readiness head-vector successor is invalid")), S + "test_t03_rejects_readiness_vector_after_catalog_intervention"),
    ("T03", "authority_current"): (_one("storage.py", "_require_effective_authority", "authority is not effective"), S + "test_t13_pre_action_revocation_blocks_matching_effect_grant"),
    ("T03", "no_fence"): (_one("storage.py", "commit_intent", "repository has an active dispatch fence"), S + "test_c05_final_fence_denies_matching_item_or_effect"),
    ("T03", "slot_available"): ((("storage.py", "_readiness_blockers", 'blockers.add("OPERATION_SLOT_OCCUPIED")'), ("storage.py", "commit_intent", "another operation owns the repository slot")), G + "test_t03_occupied_slot_denies_other_run_intent"),
    ("T03", "effect_binding_valid"): ((("storage.py", "commit_intent", "intent does not match accepted plan execution pins"), ("storage.py", "commit_intent", "operation intent does not bind the accepted plan")), S + "test_t03_requires_exact_accepted_plan_and_rejects_run_substitution"),
    ("T03", "budget_available"): (_one("storage.py", "commit_intent", "budget cap would be exceeded"), G + "test_t03_budget_cap_denies_intent"),
    ("T04", "operator_authentic"): ((("storage.py", "pause_before_dispatch", OPERATOR), ISSUED), G + "test_t04_forged_operator_capability_denies_pause"),
    ("T05", "operator_authentic"): (_one("authority.py", "verify_operator_issued", "synthetic operator capability was not issued here"), S + "test_t05_rejects_forged_or_foreign_operator_capability"),
    ("T05", "attempt_owned"): (_one("storage.py", "pause_local_execution", "local pause does not bind the durable intent"), S + "test_t05_rejects_non_owned_attempt_bindings_without_mutation"),
    ("T06", "operator_authentic"): ((("storage.py", "pause_external_mutation", OPERATOR), ISSUED), G + "test_t06_forged_operator_capability_denies_external_pause"),
    ("T06", "effect_bound"): ((("storage.py", "pause_external_mutation", "T09 effect pause does not bind a contacted operation"), ("storage.py", "pause_external_mutation", "external pause does not bind the exact adapter contact")), S + "test_t06_requires_contact_and_denies_already_recorded_receipt"),
    ("T07", "activity_accounted"): (_one("storage.py", "settle_activity_pause", "activity settlement accounting head is stale"), S + "test_t07_rejects_stale_or_rebound_t25_accounting"),
    ("T08", "operator_authentic"): ((("storage.py", "pause_active_validation", OPERATOR), ISSUED), G + "test_t08_forged_operator_capability_denies_validation_pause"),
    ("T09", "operator_authentic"): ((("storage.py", "pause_reconciliation", OPERATOR), ISSUED), G + "test_t09_forged_operator_capability_denies_reconciliation_pause"),
    ("T09", "effect_bound"): (_one("storage.py", "pause_external_mutation", "external pause does not bind the exact adapter contact"), S + "test_t06_rejects_wrong_contact_chain_and_slot_without_mutation"),
    ("T10", "receipt_bound"): ((("dispatch.py", "intake_effect_receipt", "canonical receipt does not bind this observation"), ("dispatch.py", "intake_effect_receipt", "observation targets a different repository"), ("authority.py", "verify_source_control_evidence", "source/control evidence was not issued here")), D + "test_c04_canonical_receipt_cannot_be_substituted_across_attempts"),
    ("T10", "usage_classified"): (_one("storage.py", "_record_effect_observation", "raise DispatchDenied(accounting_error)"), G + "test_t10_receipt_usage_mismatch_denies_observation"),
    ("T10", "source_claim_classified"): (_one("storage.py", "_record_effect_observation", "new observations require complete source/control evidence"), S + "test_t17_new_observation_requires_typed_source_evidence"),
    ("T11", "observation_unapplied"): (_one("storage.py", "_apply_validator_observation", "validation application identity was reused with another result"), S + "test_c05_exact_replay_rejects_rebound_request"),
    ("T11", "application_guards_met"): (_one("storage.py", "_apply_validator_observation", "PASS application does not accept a failure classification"), S + "test_c05_rejects_pass_classification_and_untrusted_fail_evidence"),
    ("T11", "accounting_settled"): (_one("storage.py", "_apply_validator_observation", "validator accounting is not fully settled"), G + "test_t11_t12_unsettled_validator_accounting_denies_application"),
    ("T12", "observation_unapplied"): (_one("storage.py", "_apply_validator_observation", "validation application identity was reused with another result"), S + "test_c05_exact_replay_rejects_rebound_request"),
    ("T12", "failure_classified"): (_one("storage.py", "_apply_validator_observation", "FAIL application requires a trusted failure classification"), S + "test_c05_denies_fail_without_trusted_classification"),
    ("T12", "accounting_settled"): (_one("storage.py", "_apply_validator_observation", "validator accounting is not fully settled"), G + "test_t11_t12_unsettled_validator_accounting_denies_application"),
    ("T13", "authority_fact_trusted"): (_one("authority.py", "verify_authority_lifecycle_evidence", "authority lifecycle evidence was not issued here"), G + "test_t13_forged_lifecycle_evidence_denies_fact"),
    ("T13", "effective_time_compared"): (_one("storage.py", "record_authority_fact", "source authority correction is not yet effective"), S + "test_f03_source_time_order_and_exact_corrections"),
    ("T14", "authority_current"): (_one("storage.py", "_require_effective_authority", "authority is not effective"), S + "test_f02_safe_same_effect_retry_is_distinct_bounded_and_one_use"),
    ("T14", "fresh"): (_one("storage.py", "resume_activity_settlement", "independent recovery freshness proof failed"), S + "test_t14_resumes_t07_only_to_blocked_with_recovery_cursor"),
    ("T14", "indexes_complete"): (_one("storage.py", "resume", "resume current head vector does not match verified history"), S + "test_t14_resume_vector_mismatch_denies_without_clearing_pause"),
    ("T14", "owner_exclusive"): (_one("storage.py", "__enter__", "repository writer lock is unavailable"), P + "test_t21_second_process_cannot_take_writer_lock"),
    ("T15", "binding_mismatch"): (_one("storage.py", "record_binding_mismatch", "binding mismatch expected value is not the accepted binding"), S + "test_t15_rejects_forged_stale_and_store_unverified_mismatch"),
    ("T16", "resolution_bound"): ((("storage.py", "resolve_validation_blocker", "validation recovery run head is stale"), ("authority.py", "verify_validation_recovery_attestation", "was not issued")), S + "test_t16_recovery_rejects_stale_or_forged_attestation"),
    ("T16", "current_guards_met"): (_one("storage.py", "_finalize_operation", "operation finalization has an active dispatch fence"), S + "test_t16_denies_event_derived_budget_fence"),
    ("T17", "proof_bound"): (_one("storage.py", "reconcile_verified_receipt", "verified receipt lookup source or response is invalid"), D + "test_t06_contact_without_intaken_receipt_is_fenced_and_worst_case_charged"),
    ("T17", "accounting_classified"): (_one("storage.py", "reconcile_verified_receipt", "verified receipt must settle the exact applicable operation uncertainty set"), D + "test_t06_contact_without_intaken_receipt_is_fenced_and_worst_case_charged"),
    ("T18", "stop_authorized"): (_one("storage.py", "stop", OPERATOR), S + "test_t19_alternate_identity_replay_authenticates_capability"),
    ("T19", "stop_authorized"): (_one("storage.py", "stop", OPERATOR), S + "test_t19_alternate_identity_replay_authenticates_capability"),
    ("T20", "drain_outstanding"): (_one("storage.py", "escalate_stop", "stop escalation requires retained drain obligations"), S + "test_t20_denies_predeadline_immediate_and_no_activity"),
    ("T20", "escalation_authorized"): (_one("storage.py", "escalate_stop", "T20 requires the exact recorded graceful stop"), S + "test_t20_rejects_immediate_stop_as_source"),
    ("T21", "owner_lock_unavailable"): (_one("storage.py", "__enter__", "repository writer lock is unavailable"), P + "test_t21_second_process_cannot_take_writer_lock"),
    ("T22", "terminal_verified"): (_one("storage.py", "report_terminal_restart", "RUN_IS_NONTERMINAL"), S + "test_t22_reports_nonterminal_without_evaluating_dispatch"),
    ("T23", "receipt_bound"): (_one("storage.py", "_record_effect_observation", "observation does not bind the durable intent"), S + "test_f13_post_release_receipt_preserves_different_slot_owner"),
    ("T23", "accounting_classified"): (_one("storage.py", "_record_effect_observation", "raise DispatchDenied(accounting_error)"), G + "test_t23_late_receipt_usage_mismatch_denies_observation"),
    ("T24", "validator_intent_recorded"): (_one("storage.py", "_record_validator_observation", "validator observation does not bind the durable intent"), G + "test_t24_unrecorded_validator_intent_denies_observation"),
    ("T24", "observation_bound"): (_one("storage.py", "_record_validator_observation", "validator intent and attempt already has its one result observation"), S + "test_t24_late_fail_atomically_records_accepted_terminal_policy"),
    ("T24", "accounting_classified"): (_one("storage.py", "_record_validator_observation", "validator usage does not match settled accounting"), G + "test_t24_known_usage_on_unknown_accounting_denies_observation"),
    ("T25", "intent_recorded"): (_one("storage.py", "_verify_nonexecution_seal", "durable handoff requires a canonical nonexecution seal"), S + "test_t25_intent_only_recovery_denies_missing_or_rebound_seal"),
    ("T25", "proof_all_paths"): (_one("storage.py", "_settle_budget", "contradictory nonexecution proof cannot release liability"), D + "test_t25_contradictory_target_facts_are_retained_and_fenced"),
    ("T25", "accounting_classified"): (_one("storage.py", "_settle_budget", "validator nonexecution cannot release the parent operation slot"), D + "test_t25_validator_seal_blocks_result_and_settles_subintent"),
    ("T26", "terminal_verified"): (_one("storage.py", "settle_terminal_validation", "T26 requires durable STOPPED or FAILED_FINAL state"), G + "test_t26_nonterminal_run_denies_terminal_settlement"),
    ("T26", "validator_activity_settled"): (_one("storage.py", "settle_terminal_validation", "terminal validation does not bind cessation proof"), S + "test_t26_terminal_result_is_atomic_and_replay_safe"),
    ("T27", "check_declared"): (_one("storage.py", "prepare_validation_launch", "validation launch check is not dependency-ordered"), S + "test_t27_denies_check_not_declared_by_accepted_plan"),
    ("T27", "prerequisites_met"): (_one("storage.py", "commit_validator_intent", "validation launch snapshot is stale or rebound"), S + "test_t27_rejects_tampered_or_stale_snapshot_before_claim"),
    ("T27", "authority_current"): (_one("storage.py", "_require_effective_authority", "authority is not effective"), S + "test_t13_future_denial_is_rechecked_before_adapter_contact"),
    ("T27", "budget_available"): (_one("storage.py", "commit_validator_intent", "budget cap would be exceeded"), S + "test_t27_denies_another_active_validator_and_budget_over_cap"),
    ("T27", "validator_contained"): (_one("contracts.py", "validate", "validator containment specification is required"), S + "test_f20_missing_containment_denies_before_validator_intent"),
    ("T27", "slot_owned"): ((("storage.py", "commit_validator_intent", "validator intent parent observation lost its slot binding"), ("storage.py", "commit_validator_intent", "validator intent does not own the operation slot")), G + "test_t27_rebound_slot_generation_denies_validator_intent"),
    ("T27", "no_active_validator"): ((("storage.py", "prepare_validation_launch", "validation launch does not bind a VALIDATING plan"), ("storage.py", "commit_validator_intent", "another validator obligation is active")), S + "test_t27_denies_another_active_validator_and_budget_over_cap"),
    ("T27", "no_fence"): (_one("storage.py", "commit_validator_intent", "repository has an active dispatch fence"), S + "test_t27_denies_when_repository_has_derived_dispatch_fence"),
    ("T28", "adoption_authorized"): (_one("storage.py", "adopt_verified_effect", "adoption capability does not bind the exact adoption"), S + "test_t28_adopts_completed_effect_without_delivery_or_reused_charge"),
    ("T28", "fresh"): (_one("storage.py", "adopt_verified_effect", "independent recovery freshness proof failed"), S + "test_t28_adopts_completed_effect_without_delivery_or_reused_charge"),
    ("T28", "predecessor_settled"): (_one("storage.py", "adopt_verified_effect", "adoption root is not an exact completed final effect"), G + "test_t28_unfinalized_root_denies_adoption"),
    ("T28", "slot_available"): (_one("storage.py", "adopt_verified_effect", "effect adoption requires the repository slot to be free"), S + "test_t28_adopts_completed_effect_without_delivery_or_reused_charge"),
    ("T28", "effect_binding_valid"): (_one("storage.py", "adopt_verified_effect", "adoption readiness does not bind current accepted inputs"), S + "test_t28_adopts_completed_effect_without_delivery_or_reused_charge"),
}

# Every production authorize call passes the transition's full guard catalog.
# The single listed exception adds the T09 pause-request variant guard; the
# storage path and the dispatch path each use it once, for PAUSE_REQUESTED.
FULL_CATALOG = "TRANSITIONS[{}].required_guards"
T09_VARIANT = (
    "TRANSITIONS[transition_id].required_guards | "
    "(frozenset({'effect_bound'}) if transition_id == 'T09' else frozenset())"
)
PRODUCTION_CALLS = {"dispatch.py": 28, "storage.py": 28}
T09_VARIANT_CALLS = {"dispatch.py": 1, "storage.py": 1}


@functools.lru_cache(maxsize=None)
def _tree(module: str) -> tuple[ast.Module, tuple[str, ...]]:
    source = (PACKAGE / module).read_text(encoding="utf-8")
    return ast.parse(source), tuple(source.splitlines())


def _site_statements(module: str, function: str, marker: str) -> list[ast.stmt]:
    tree, lines = _tree(module)
    return [
        node
        for definition in ast.walk(tree)
        if isinstance(definition, ast.FunctionDef) and definition.name == function
        for node in ast.walk(definition)
        if isinstance(node, (ast.Raise, ast.Return, ast.Expr))
        and (
            marker in "\n".join(lines[node.lineno - 1:node.end_lineno])
            or any(
                isinstance(constant, ast.Constant)
                and isinstance(constant.value, str)
                and marker in constant.value
                for constant in ast.walk(node)
            )
        )
    ]


def _authorize_calls(module: str) -> list[ast.Call]:
    tree, _ = _tree(module)
    return [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "authorize"
    ]


class GuardTraceabilityTests(unittest.TestCase):
    def test_every_transition_guard_pair_is_traced(self) -> None:
        pairs = {
            (transition_id, guard)
            for transition_id, spec in TRANSITIONS.items()
            for guard in spec.required_guards.union(
                *(guards for _kind, guards in spec.event_variants)
            )
        }
        self.assertEqual(len(pairs), 69)
        self.assertEqual(set(GUARD_TRACE), pairs)

    def test_every_inline_check_site_exists(self) -> None:
        for pair, (sites, _test) in GUARD_TRACE.items():
            for site in sites:
                with self.subTest(pair=pair, site=site):
                    self.assertTrue(_site_statements(*site))

    def test_every_traced_test_exists(self) -> None:
        for pair, (_sites, test_name) in GUARD_TRACE.items():
            module_name, class_name, method = test_name.split(".")
            module = importlib.import_module(
                f"tools.aegis_delivery_control.tests.{module_name}"
            )
            with self.subTest(pair=pair, test=test_name):
                self.assertTrue(
                    callable(getattr(getattr(module, class_name), method, None))
                )

    def test_production_calls_pass_the_full_guard_catalog(self) -> None:
        modules = sorted(path.name for path in PACKAGE.glob("*.py"))
        found = {
            module: len(_authorize_calls(module)) for module in modules
            if _authorize_calls(module)
        }
        self.assertEqual(found, PRODUCTION_CALLS)
        variants = {}
        for module in PRODUCTION_CALLS:
            for call in _authorize_calls(module):
                transition = ast.unparse(call.args[0])
                argument = (
                    call.args[3] if len(call.args) > 3 else next(
                        keyword.value for keyword in call.keywords
                        if keyword.arg == "satisfied_guards"
                    )
                )
                text = ast.unparse(argument)
                if text == T09_VARIANT:
                    variants[module] = variants.get(module, 0) + 1
                with self.subTest(module=module, line=call.lineno):
                    self.assertIn(
                        text,
                        {FULL_CATALOG.format(transition), T09_VARIANT},
                    )
                    if text == T09_VARIANT:
                        self.assertEqual(transition, "transition_id")
                        self.assertEqual(
                            [
                                ast.unparse(keyword.value)
                                for keyword in call.keywords
                                if keyword.arg == "event_kind"
                            ],
                            ["'PAUSE_REQUESTED'"],
                        )
        self.assertEqual(variants, T09_VARIANT_CALLS)


class GuardGapTests(storage_tests.SQLiteStateStoreTests):
    """Negative tests for guards that had no denial test of their own."""

    def _forged(self, capability):
        return replace(capability, issuer_mac="forged")

    def _denied(self, message: str, call, *args, **kwargs) -> None:
        with self.assertRaisesRegex(DispatchDenied, message):
            call(*args, **kwargs)

    def test_t03_budget_cap_denies_intent(self) -> None:
        original = self.store.commit_intent
        denied = []

        def commit_intent(request, capability, authority, **kwargs):
            if request.run_id == "run-dependent" and not denied:
                over_cap = replace(
                    request, reserved_units=3, worst_case_units=3, cap_units=3
                )
                self._denied(
                    "budget cap would be exceeded", original,
                    over_cap, capability, authority, **kwargs,
                )
                denied.append(True)
            return original(request, capability, authority, **kwargs)

        self.store.commit_intent = commit_intent
        self.test_t01_t02_t03_completed_dependency_permits_ready_dispatch()
        self.assertEqual(denied, [True])

    def test_t03_occupied_slot_denies_other_run_intent(self) -> None:
        self.test_t02_repository_slot_in_another_run_blocks_readiness()
        grant = storage_tests.SyntheticGrant(
            "grant-2", "repo-1", "effect-2", "attempt-2", "scope-2"
        )
        self.authority.register(grant)
        with closing(sqlite3.connect(self.database_path)) as connection:
            head = connection.execute(
                "SELECT catalog_head FROM repositories WHERE repository_id = 'repo-1'"
            ).fetchone()[0]
        self.oracle.allowed_head = head
        self._denied(
            "T03 requires durable PLANNED state|"
            "T03 requires current verified readiness|"
            "another operation owns the repository slot",
            self.store.commit_intent,
            storage_tests.IntentRequest(
                "repo-1", "run-2", "item-2", "command-2", "event-2",
                "effect-2", "descriptor-2", "attempt-2", "permission-2",
                "reservation-2", "budget-policy-2", 1, 2, 10,
            ),
            self.authority.claim(*grant.__dict__.values()), self.authority,
            expected_head=head, writer_epoch=100,
        )
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

    def test_t04_forged_operator_capability_denies_pause(self) -> None:
        plan = self.store.accept_plan(
            storage_tests.PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        self._denied(
            "not issued here", self.store.pause_before_dispatch,
            self._pause_request(), self._forged(self._pause_capability()),
            self.authority,
        )
        self.assertEqual(self.store.table_counts()["control_actions"], 0)

    def test_t06_forged_operator_capability_denies_external_pause(self) -> None:
        committed = self._running_operation()
        launched = self.store.claim_operation_launch(self.request(), committed)
        self.oracle.allowed_head = launched.event_hash
        request = PauseExternalMutationRequest(
            "external-pause-forged", "external-command-forged",
            "external-event-forged", "external-fence-forged",
            "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
            committed.event_id, committed.event_hash, launched.launch_id,
            launched.event_id, launched.event_hash, "contact-forged",
            "contact-event-forged", "contact-hash-forged",
            self.store._adapter_target_digest("repo-1", "EFFECT"), 1,
            "OPERATOR_PAUSE_EXTERNAL_MUTATION",
        )
        self._denied(
            "not issued here", self.store.pause_external_mutation, request,
            self._forged(self._pause_capability("external-forged")),
            self.authority,
        )
        self.assertEqual(self.store.table_counts()["external_pause_actions"], 0)

    def test_t08_forged_operator_capability_denies_validation_pause(self) -> None:
        request, capability, activity = self._active_validation_pause_fixture(
            "forged"
        )
        self._denied(
            "not issued here", self.store.pause_active_validation, request,
            self._forged(capability), activity, self.authority,
        )

    def test_t09_forged_operator_capability_denies_reconciliation_pause(
        self,
    ) -> None:
        self._contacted_operation("forged")
        self._denied(
            "not issued here", self.store.pause_reconciliation,
            self._reconciliation_pause_request(self.store, suffix="forged"),
            self._forged(self._pause_capability("reconciliation-forged")),
            self.authority,
        )

    def _settled_operation(self, disposition, usage):
        plan = self.store.accept_plan(
            storage_tests.PlanAcceptanceRequest(
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
        settlement_request = storage_tests.BudgetSettlementRequest(
            "settlement-1", "reservation-1", "", disposition, usage,
            "receipt-1", "USAGE_REPORTED",
        )
        settlement = self.store._settle_budget(
            settlement_request,
            self.authority.issue_settlement_proof("proof-1", settlement_request),
            self.authority,
        )
        self.oracle.allowed_head = settlement.settlement_hash
        return settlement

    def _observation(self, usage, settlement_hash, suffix="1"):
        return EffectObservationRequest(
            f"observation-{suffix}", f"observe-command-{suffix}",
            f"observation-event-{suffix}", "repo-1", "run-1", "item-1",
            "effect-1", "attempt-1", f"receipt-{suffix}",
            self.capability.claim_id, "descriptor-digest", usage,
            f"settlement-{suffix}", settlement_hash,
        )

    def test_t10_receipt_usage_mismatch_denies_observation(self) -> None:
        settlement = self._settled_operation(BudgetDisposition.CONSUMED, 2)
        self._denied(
            "known receipt usage does not match settled accounting",
            self._record_signed_effect_observation,
            self._observation(3, settlement.settlement_hash),
        )
        self._record_signed_effect_observation(
            self._observation(2, settlement.settlement_hash)
        )

    def test_t23_late_receipt_usage_mismatch_denies_observation(self) -> None:
        settlement = self._settled_operation(BudgetDisposition.CONSUMED, 2)
        self._stop_run()
        self._denied(
            "known receipt usage does not match settled accounting",
            self._record_signed_effect_observation,
            self._observation(3, settlement.settlement_hash),
        )
        late = self._record_signed_effect_observation(
            self._observation(2, settlement.settlement_hash)
        )
        with closing(sqlite3.connect(self.database_path)) as connection:
            body = connection.execute(
                "SELECT body_json FROM events WHERE event_id = ?",
                (late.event_id,),
            ).fetchone()[0]
        self.assertIn('"event_kind":"LATE_RECEIPT_RECORDED"', body)

    def _unknown_validator_accounting(self):
        observation = self._record_effect_observation(check_ids=("check-1",))
        intent_request, capability = self._validator_intent(observation)
        intent = self.store.commit_validator_intent(
            intent_request, capability, self.authority
        )
        self.oracle.allowed_head = intent.event_hash
        unknown = storage_tests.BudgetSettlementRequest(
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
        return storage_tests.ValidatorObservationRequest(
            "validator-observation-1", "validator-observe-command-1",
            "validator-observation-event-1", "repo-1", "run-1", "item-1",
            "effect-1", "validator-intent-1", "validator-attempt-1",
            "validator-result-1", capability.claim_id, "revision-1",
            "check-1", "input-1", "result-digest-1", "PASS", None,
            "validator-settlement-1", settlement.settlement_hash,
        )

    def test_t11_t12_unsettled_validator_accounting_denies_application(
        self,
    ) -> None:
        self._record_validator_result(only_check=True)
        with closing(sqlite3.connect(self.database_path)) as connection:
            previous_hash = connection.execute(
                "SELECT settlement_head_hash FROM budget_reservations "
                "WHERE reservation_id = 'validator-reservation-1'"
            ).fetchone()[0]
        unknown = storage_tests.BudgetSettlementRequest(
            "validator-late-unknown", "validator-reservation-1",
            previous_hash, BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "validator-late-evidence", "ADDITIONAL_LIABILITY_UNKNOWN",
            additional_liability=True,
        )
        settlement = self.store._settle_budget(
            unknown,
            self.authority.issue_settlement_proof("validator-late-proof", unknown),
            self.authority,
        )
        self.oracle.allowed_head = settlement.settlement_hash
        self._denied(
            "validator accounting is not fully settled",
            self.store._apply_validator_observation,
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1", "validator-observation-1",
            ),
        )
        self.assertEqual(self.store.table_counts()["validation_applications"], 0)

    def test_t24_unrecorded_validator_intent_denies_observation(self) -> None:
        request = self._unknown_validator_accounting()
        self._denied(
            "does not bind the durable intent",
            self.store._record_validator_observation,
            replace(request, validator_attempt_id="validator-attempt-other"),
        )

    def test_t24_known_usage_on_unknown_accounting_denies_observation(
        self,
    ) -> None:
        request = self._unknown_validator_accounting()
        self._denied(
            "validator usage does not match settled accounting",
            self.store._record_validator_observation,
            replace(request, usage_units=1),
        )
        self.store._record_validator_observation(request)

    def test_t27_rebound_slot_generation_denies_validator_intent(self) -> None:
        observation = self._record_effect_observation()
        request, capability = self._validator_intent(observation)
        real = self.store._operation_attempt_generation

        def rebound(*args, **kwargs):
            generation, recovery = real(*args, **kwargs)
            if sys._getframe(1).f_code.co_name == "commit_validator_intent":
                return generation + 1, recovery
            return generation, recovery

        with patch.object(self.store, "_operation_attempt_generation", rebound):
            self._denied(
                "validator intent parent observation lost its slot binding",
                self.store.commit_validator_intent, request, capability,
                self.authority,
            )
        self.assertEqual(self.store.table_counts()["validator_intents"], 0)
        self.store.commit_validator_intent(request, capability, self.authority)

    def test_t13_forged_lifecycle_evidence_denies_fact(self) -> None:
        request = self.request()
        plan = self.store.accept_plan(
            storage_tests.PlanAcceptanceRequest(
                "plan-t13", "plan-command-t13", "plan-event-t13",
                request.repository_id, request.run_id, request.item_id,
                request.logical_effect_id, "revision-1",
                request.effect_descriptor_digest, self.capability.scope_digest,
                request.budget_policy_digest, ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        fact = storage_tests.AuthorityLifecycleFactRequest(
            "fact-t13", "fact-command-t13", "fact-event-t13",
            request.repository_id, request.run_id, request.item_id,
            request.logical_effect_id, "EFFECT", self.capability.grant_id,
            "EXECUTE_EFFECT", self.capability.scope_digest,
            storage_tests.AuthorityFactKind.REVOKED,
            storage_tests.GovernedOrder.BEFORE, "NO_ACTION", None, None,
        )
        evidence = self.authority.issue_authority_lifecycle_evidence(
            "proof-t13", fact
        )
        self.oracle.allowed_head = plan.event_hash
        self._denied(
            "authority lifecycle evidence was not issued here",
            self.store.record_authority_fact, fact, self._forged(evidence),
            self.authority, expected_head=plan.event_hash, writer_epoch=2,
        )

    def test_t26_nonterminal_run_denies_terminal_settlement(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        with closing(sqlite3.connect(self.database_path)) as connection:
            plan_id, plan_hash = connection.execute(
                "SELECT plan_id, event_hash FROM validation_plans "
                "WHERE run_id = 'run-1'"
            ).fetchone()
        self._denied(
            "T26 requires durable STOPPED or FAILED_FINAL state",
            self.store.settle_terminal_validation,
            storage_tests.TerminalValidationSettlementRequest(
                "terminal-settlement-1", "terminal-command-1",
                "terminal-event-1", "repo-1", "run-1", "item-1", "effect-1",
                plan_id, "revision-1", "check-1", "PLAN", plan_id, plan_hash,
                "CANCELLED_WITHOUT_START",
            ),
        )

    def test_t28_unfinalized_root_denies_adoption(self) -> None:
        original = self.store.adopt_verified_effect
        calls, adopted = [], []

        def adopt_verified_effect(request, readiness, *args, **kwargs):
            calls.append(
                (Path(self.database_path).read_bytes(), request, readiness)
            )
            result = original(request, readiness, *args, **kwargs)
            adopted.append(request)
            return result

        self.store.adopt_verified_effect = adopt_verified_effect
        self.test_t28_adopts_completed_effect_without_delivery_or_reused_charge()
        # The earliest call carrying the adopted request sees the pre-adoption state.
        before = next(call for call in calls if call[1] == adopted[0])
        self.assertEqual(
            self._forged_root_adoption(*before),
            "adoption root is not an exact completed final effect",
        )

    def _forged_root_adoption(self, database, request, readiness) -> str:
        """Replay the successful adoption's pre-state with a never-finalized root."""
        path = Path(self.temporary_directory.name) / "forged-root.sqlite3"
        path.write_bytes(database)
        oracle = storage_tests.MutableFreshnessOracle()
        with closing(sqlite3.connect(path)) as connection:
            oracle.allowed_head = connection.execute(
                "SELECT catalog_head FROM repositories WHERE repository_id = 'repo-1'"
            ).fetchone()[0]
        store = storage_tests.SQLiteStateStore(
            path, oracle, "repo-1",
            utc_now=lambda: datetime(2026, 9, 21, tzinfo=timezone.utc),
        )
        store._bind_classification_authority(self.authority)
        forged = replace(
            request, root_finalization_key="never-finalized-root",
            adoption_grant_id="adoption-grant-forged",
        )
        grant = self.authority.issue_source_grant(
            grant_id="adoption-grant-forged",
            grant_kind=storage_tests.SyntheticGrantKind.ADOPTION,
            action="ADOPT_VERIFIED_EFFECT", repository_id="repo-1",
            logical_effect_id="effect-1",
            source_id=forged.adoption_source_id,
            source_version=forged.adoption_source_version,
            terms_digest=forged.adoption_terms_digest,
            scope_digest=forged.adoption_scope_digest,
            binding_digest=store.adoption_binding_digest(forged),
            not_before="2026-09-20T00:00:00.000000Z",
            expires_at="2026-09-22T00:00:00.000000Z", use_limit=1,
        )
        oracle.allowed_head = store.register_synthetic_source_grant(
            grant, self.authority
        ).event_hash
        catalog_head, heads = store.load_verified("repo-1")
        forged = replace(
            forged, expected_catalog_head=catalog_head,
            expected_run_head=heads["run-2"],
            expected_head_vector_digest=store._complete_head_vector_digest(heads),
        )
        fields = {
            key: value for key, value in readiness.__dict__.items()
            if key not in {"issuer_mac", "issuer_fingerprint"}
        }
        fields.update(
            catalog_head=catalog_head,
            head_vector_digest=forged.expected_head_vector_digest,
            evidence_head=heads["run-2"],
            request_digest=store._event_hash({
                **forged.__dict__,
                "immediate_origin_kind": forged.immediate_origin_kind.value,
                "expected_lifecycle": forged.expected_lifecycle.value,
            }),
        )
        capability = self.authority.issue_source_capability(
            grant,
            consumer_kind=storage_tests.SyntheticSourceConsumerKind.EFFECT_ADOPTION,
            consumer_key=store.adoption_key(forged),
            binding_digest=grant.binding_digest,
        )
        try:
            store.adopt_verified_effect(
                forged, self.authority.issue_adoption_readiness_evidence(**fields),
                capability, self.authority,
            )
        except DispatchDenied as error:
            return str(error)
        return "adopted"


def load_tests(loader, standard_tests, pattern):
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(GuardTraceabilityTests))
    suite.addTests(
        GuardGapTests(name) for name in sorted(vars(GuardGapTests))
        if name.startswith("test_")
    )
    return suite
