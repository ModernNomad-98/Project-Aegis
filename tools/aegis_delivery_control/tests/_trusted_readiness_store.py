"""Test-only store adapter that supplies explicit synthetic T01/T02 evidence.

Production callers must supply independently issued acceptance and readiness
evidence.  Legacy kernel tests exercise later transitions, so this adapter
constructs that evidence through the synthetic authority rather than preserving
the former implicit T01/T03 path.
"""

from __future__ import annotations

from contextlib import closing
import json
import sqlite3

from tools.aegis_delivery_control.authority import (
    SyntheticAuthority,
    SyntheticOperationReadinessEvidence,
)
from tools.aegis_delivery_control.contracts import (
    LifecycleState,
    ProvenNonexecutionIntentRequest,
    ReadinessEvaluationRequest,
    ValidationLaunchRequest,
)
from tools.aegis_delivery_control.storage import SQLiteStateStore as ProductionSQLiteStateStore


class SQLiteStateStore(ProductionSQLiteStateStore):
    """Production store with explicit, deterministic synthetic test evidence."""

    _known_test_authorities: dict[str, SyntheticAuthority] = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with closing(sqlite3.connect(self._database_path)) as connection:
            row = connection.execute(
                "SELECT classification_issuer_fingerprint FROM validation_plans "
                "WHERE classification_issuer_fingerprint IS NOT NULL LIMIT 1"
            ).fetchone()
        if row is not None:
            authority = self._known_test_authorities.get(str(row[0]))
            if authority is not None:
                super()._bind_classification_authority(authority)

    def _bind_classification_authority(self, authority):
        super()._bind_classification_authority(authority)
        self._known_test_authorities[authority.issuer_fingerprint] = authority

    def commit_validator_intent(self, request, capability, authority, **kwargs):
        """Adapt legacy tests onto the production unclaimed launch contract."""
        if capability is None:
            return super().commit_validator_intent(
                request, capability, authority, **kwargs
            )
        with authority._lock:
            issued = authority._validator_claims.get(capability.grant_id)
            committed = capability.claim_id in authority._committed_claims
        if issued == capability and not committed:
            authority.release_uncommitted_validator_claim(capability)
        suffix = request.command_id
        with closing(sqlite3.connect(self._database_path)) as connection:
            plan_id = connection.execute(
                "SELECT plan_id FROM validation_plans WHERE run_id = ?",
                (request.run_id,),
            ).fetchone()[0]
        launch = super().prepare_validation_launch(
            ValidationLaunchRequest(
                f"test-launch-evaluation:{suffix}",
                f"test-launch-decision:{suffix}",
                f"test-launch-command:{suffix}",
                f"test-launch-event:{suffix}",
                f"test-launch-decision-event:{suffix}",
                request.repository_id, request.run_id, request.item_id,
                request.logical_effect_id, plan_id, request.revision_digest,
                request.check_id,
            ),
            authority,
        )
        if not launch.ready:
            raise RuntimeError("test fixture validation launch is blocked")
        if hasattr(self._freshness_oracle, "allowed_head"):
            with closing(sqlite3.connect(self._database_path)) as connection:
                self._freshness_oracle.allowed_head = connection.execute(
                    "SELECT catalog_head FROM repositories WHERE "
                    "repository_id = ?", (request.repository_id,),
                ).fetchone()[0]
        snapshot = super().load_validation_launch_snapshot(
            launch.snapshot_id, authority
        )
        return super().commit_validator_intent(
            request, None, authority, grant_id=capability.grant_id,
            scope_digest=capability.scope_digest,
            launch_snapshot=snapshot, **kwargs,
        )

    def _next_test_writer_epoch(self) -> int:
        with closing(sqlite3.connect(self._database_path)) as connection:
            return int(
                connection.execute(
                    "SELECT COALESCE(MAX(writer_epoch), 0) + 1 FROM events"
                ).fetchone()[0]
            )

    def accept_plan(self, request, **kwargs):
        authority = kwargs.get("authority") or self._classification_authority
        if kwargs.get("acceptance_evidence") is None and authority is not None:
            kwargs["authority"] = authority
            kwargs["acceptance_evidence"] = (
                authority.issue_plan_acceptance_evidence(
                    evidence_id=f"acceptance:{request.plan_id}",
                    source_id="synthetic-test-plan-acceptor",
                    source_version="1",
                    operator_id="synthetic-test-operator",
                    operator_role="PLAN_ACCEPTOR",
                    action="ACCEPT_PLAN",
                    repository_id=request.repository_id,
                    run_id=request.run_id,
                    item_id=request.item_id,
                    plan_id=request.plan_id,
                    command_id=request.command_id,
                    acceptance_payload_digest=(
                        self.plan_acceptance_payload_digest(request)
                    ),
                )
            )
        if "writer_epoch" in kwargs:
            kwargs["writer_epoch"] = self._next_test_writer_epoch()
        return super().accept_plan(request, **kwargs)

    def evaluate_readiness(self, request, **kwargs):
        authority = kwargs.get("authority") or self._classification_authority
        if kwargs.get("readiness_evidence") is None and authority is not None:
            with closing(sqlite3.connect(self._database_path)) as connection:
                connection.row_factory = sqlite3.Row
                prior = connection.execute(
                    "SELECT body_json FROM readiness_evaluations WHERE "
                    "command_id = ?",
                    (request.command_id,),
                ).fetchone()
            if prior is None:
                evidence = self.issue_operation_readiness_evidence(
                    request,
                    authority,
                    evidence_id=f"readiness:{request.readiness_id}",
                    source_id="synthetic-test-readiness-verifier",
                )
            else:
                body = json.loads(str(prior["body_json"]))["readiness_evidence"]
                body["dependency_snapshot"] = tuple(
                    tuple(row) for row in body["dependency_snapshot"]
                )
                body["predecessor_head_vector"] = tuple(
                    tuple(row) for row in body["predecessor_head_vector"]
                )
                evidence = SyntheticOperationReadinessEvidence(**body)
            kwargs["authority"] = authority
            kwargs["readiness_evidence"] = evidence
        return super().evaluate_readiness(request, **kwargs)

    def commit_intent(self, request, capability, authority, **kwargs):
        with closing(sqlite3.connect(self._database_path)) as connection:
            connection.row_factory = sqlite3.Row
            run = connection.execute(
                "SELECT lifecycle_state, continuation_cursor, head_hash FROM runs "
                "WHERE repository_id = ? AND run_id = ?",
                (request.repository_id, request.run_id),
            ).fetchone()
            plan = connection.execute(
                "SELECT plan_id, revision_digest FROM validation_plans WHERE "
                "repository_id = ? AND run_id = ?",
                (request.repository_id, request.run_id),
            ).fetchone()
            current_readiness = connection.execute(
                "SELECT event_hash, resulting_state FROM readiness_evaluations "
                "WHERE repository_id = ? AND run_id = ? ORDER BY rowid DESC LIMIT 1",
                (request.repository_id, request.run_id),
            ).fetchone()
            slot_occupied = connection.execute(
                "SELECT 1 FROM outstanding_slot LIMIT 1"
            ).fetchone() is not None
            owned_recovery_slot = (
                isinstance(request, ProvenNonexecutionIntentRequest)
                and connection.execute(
                    "SELECT 1 FROM outstanding_slot WHERE repository_id = ? "
                    "AND run_id = ? AND logical_effect_id = ? AND attempt_id = ? "
                    "AND generation = ?",
                    (
                        request.repository_id,
                        request.run_id,
                        request.logical_effect_id,
                        request.prior_attempt_id,
                        request.expected_source_generation,
                    ),
                ).fetchone() is not None
            )
            authority_matches = (
                self._classification_authority is not None
                and authority.issuer_fingerprint
                == self._classification_authority.issuer_fingerprint
            )
            if (
                run is not None
                and plan is not None
                and (not slot_occupied or owned_recovery_slot)
                and authority_matches
                and run["lifecycle_state"]
                in {LifecycleState.PLANNED.value, LifecycleState.BLOCKED.value}
                and (
                    current_readiness is None
                    or current_readiness["event_hash"] != run["head_hash"]
                    or current_readiness["resulting_state"]
                    != LifecycleState.PLANNED.value
                )
            ):
                readiness_suffix = str(run["head_hash"])[:16]
                readiness = self.evaluate_readiness(
                    ReadinessEvaluationRequest(
                        readiness_id=(
                            f"readiness:{request.command_id}:{readiness_suffix}"
                        ),
                        command_id=(
                            f"readiness-command:{request.command_id}:{readiness_suffix}"
                        ),
                        event_id=(
                            f"readiness-event:{request.event_id}:{readiness_suffix}"
                        ),
                        repository_id=request.repository_id,
                        run_id=request.run_id,
                        item_id=request.item_id,
                        plan_id=str(plan["plan_id"]),
                        revision_digest=str(plan["revision_digest"]),
                        expected_run_head=str(run["head_hash"]),
                        expected_continuation_cursor=run["continuation_cursor"],
                        inputs_evidence_digest=f"inputs:{request.command_id}",
                        prerequisites_met=True,
                    )
                )
                if hasattr(self._freshness_oracle, "allowed_head"):
                    self._freshness_oracle.allowed_head = readiness.event_hash
                kwargs["expected_head"] = readiness.event_hash
                kwargs["writer_epoch"] = self._next_test_writer_epoch()
            elif "writer_epoch" in kwargs:
                kwargs["writer_epoch"] = self._next_test_writer_epoch()
        return super().commit_intent(request, capability, authority, **kwargs)
