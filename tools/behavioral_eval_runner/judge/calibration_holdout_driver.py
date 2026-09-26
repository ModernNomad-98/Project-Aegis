"""One-pass WP-2B-3 sealed-holdout driver, behind the owner freeze gate.

The production freeze and execution-source trust pins are deliberately unset.
Importing this module, and its offline tests, make no external request.
"""

from __future__ import annotations

import json
import os
import time
from typing import Any, Callable

from ..canonical import sha256_hex, sha256_of_obj
from . import calibration_gates as gates
from . import calibration_ledger as ledger_module
from . import calibration_provider as provider
from . import calibration_transport as transport
from . import policy, rubric, verdict
from .calibration_dataset import (
    CalibrationItemContent, CandidateDataset, calibration_request_id,
    development_items, holdout_items, split_map_sha256,
)
from .calibration_development_driver import (
    ApprovedArtifactIdentity, PRODUCTION_APPROVED_ARTIFACTS,
    DEVELOPMENT_RESULT_SUMMARY_RELPATH, _MANIFEST_BINDING_KEYS,
    _MANIFEST_KEYS, _canonical_path, _sha256_file, _utc_day,
    build_run_manifest, canonical_ledger_path, canonical_manifest_path,
    load_approved_dataset, load_owner_approval, verify_evidence_root,
    VerifiedEvidenceRoot, _resolve_repo_identity,
)
from .calibration_envelope import (
    build_calibration_envelope, build_calibration_judge_request,
)
from .calibration_errors import (
    CalibrationAuthorizationError, CalibrationLedgerError,
    CalibrationReservationDenied, CalibrationStopError,
    CalibrationStopReason,
)
from .calibration_io import checked_open, exclusive_lock
from .calibration_provider import TransportExceptionTypes

# Independently reviewed original DEVELOPMENT source. A caller-provided
# manifest cannot approve its own head/tree. Production pins remain unset.
APPROVED_DEVELOPMENT_EXECUTION_HEAD_SHA: str | None = None
APPROVED_DEVELOPMENT_EXECUTION_TREE_SHA: str | None = None
APPROVED_DEVELOPMENT_MANIFEST_SHA256: str | None = None
APPROVED_DEVELOPMENT_SUMMARY_SHA256: str | None = None
HOLDOUT_RESULT_SUMMARY_RELPATH = "runs/wp2b3-holdout-result-summary-v1.json"


def _source_hash(module: Any) -> str:
    with checked_open(module.__file__, "rb") as handle:
        return sha256_hex(handle.read())


def frozen_artifact_hashes(
    dataset: CandidateDataset,
    expected: ApprovedArtifactIdentity,
    verified_root: VerifiedEvidenceRoot,
    max_output_tokens: int,
) -> dict[str, str]:
    """Recompute decision-35 evidence from the current approved artifacts.

    File-backed contracts use current source bytes; the remaining terms use
    the exact runtime constants and approved artifact identities. The caller
    cannot supply a replacement digest map.
    """
    t, l = transport, ledger_module
    values: dict[str, Any] = {
        "model_snapshot": {"provider": t.AUTHORIZED_PROVIDER,
                           "model": t.AUTHORIZED_MODEL_SNAPSHOT},
        "endpoint": {"base_url": t.AUTHORIZED_BASE_URL,
                     "egress_host": t.AUTHORIZED_EGRESS_HOST,
                     "egress_port": t.AUTHORIZED_EGRESS_PORT},
        "sdk_transport_version": {
            "sdk": t.AUTHORIZED_SDK_NAME, "version": t.AUTHORIZED_SDK_VERSION,
            "wheel_sha256": t.AUTHORIZED_SDK_WHEEL_SHA256,
            "sdist_sha256": t.AUTHORIZED_SDK_SDIST_SHA256,
            "transport_source_sha256": _source_hash(t),
        },
        "system_policy": {"text": policy.JUDGE_SYSTEM_POLICY,
                          "source_sha256": _source_hash(policy)},
        "rubric_contracts": {"source_sha256": _source_hash(rubric)},
        "verdict_schema": {
            "source_sha256": _source_hash(verdict),
            "provider_source_sha256": _source_hash(provider),
        },
        "labels": [
            {"item_id": item.item_id,
             "label": item.candidate_expected_label.value,
             "status": item.owner_label_status.value}
            for item in sorted(dataset.items, key=lambda item: item.item_id)
        ],
        "thresholds": {
            "agreement_min": [114, 120], "false_pass_max": [1, 60],
            "critical_false_pass_max": 0, "false_fail_max": [3, 60],
            "abstain_max": [6, 120], "judge_error_max": [1, 120],
        },
        "retry_policy": {
            "attempts_per_judgment": l.MAX_ATTEMPTS_PER_JUDGMENT,
            "sdk_retries": t.SDK_MAX_RETRIES,
            "connection_timeout_seconds": t.CONNECT_TIMEOUT_SECONDS,
            "total_request_timeout_seconds": t.TOTAL_REQUEST_TIMEOUT_SECONDS,
            "concurrency": 1,
        },
        "call_token_dollar_caps": {
            "judgment_attempts": l.MAX_JUDGMENT_ATTEMPTS,
            "metadata_requests": l.MAX_METADATA_REQUESTS,
            "total_requests": l.MAX_TOTAL_EXTERNAL_REQUESTS,
            "input_tokens": t.MAX_INPUT_TOKENS_PER_JUDGMENT,
            "holdout_output_tokens": max_output_tokens,
            "total_spend_nanousd": l.MAX_TOTAL_SPEND_NANOUSD,
            "single_day_spend_nanousd": l.MAX_SINGLE_DAY_SPEND_NANOUSD,
            "total_run_deadline_seconds": l.TOTAL_RUN_DEADLINE_SECONDS,
        },
        "retention_settings": {
            "marker_sha256": verified_root.marker_sha256,
            "marker_retention": verified_root.marker.get("retention_policy"),
            "marker_cleanup": verified_root.marker.get("cleanup_policy"),
            "marker_expiry": verified_root.marker.get("expires_utc"),
        },
    }
    result = {name: sha256_of_obj(value) for name, value in values.items()}
    result["dataset"] = expected.dataset_semantic_sha256
    result["split_map"] = expected.split_map_sha256
    assert set(result) == set(gates.FREEZE_HASH_FIELDS)
    return result


def _read_verified_manifest(
    root: VerifiedEvidenceRoot, expected: ApprovedArtifactIdentity,
) -> str:
    path = canonical_manifest_path(root)
    if not os.path.isfile(path) or os.path.isfile(path + ".pending"):
        raise CalibrationAuthorizationError("the immutable development manifest is missing or pending")
    with checked_open(path, encoding="utf-8") as handle:
        recorded = json.load(handle)
    if not isinstance(recorded, dict) or set(recorded) != _MANIFEST_KEYS:
        raise CalibrationAuthorizationError("development manifest shape mismatch")
    if (APPROVED_DEVELOPMENT_EXECUTION_HEAD_SHA is None
            or APPROVED_DEVELOPMENT_EXECUTION_TREE_SHA is None
            or recorded["audited_execution_head_sha"]
            != APPROVED_DEVELOPMENT_EXECUTION_HEAD_SHA
            or recorded["audited_execution_tree_sha"]
            != APPROVED_DEVELOPMENT_EXECUTION_TREE_SHA):
        raise CalibrationAuthorizationError(
            "original development source lacks independent trusted pins"
        )
    original = build_run_manifest(
        verified=root, expected=expected,
        audited_head_sha=recorded["audited_execution_head_sha"],
        audited_tree_sha=recorded["audited_execution_tree_sha"],
        started_utc=recorded["started_utc"],
    )
    if any(recorded[key] != original[key] for key in _MANIFEST_BINDING_KEYS):
        raise CalibrationAuthorizationError("development manifest binding changed")
    digest = _sha256_file(path)
    if (APPROVED_DEVELOPMENT_MANIFEST_SHA256 is None
            or digest != APPROVED_DEVELOPMENT_MANIFEST_SHA256):
        raise CalibrationAuthorizationError(
            "development manifest lacks an independent reviewed digest"
        )
    return digest


def _read_development_completion(
    root: VerifiedEvidenceRoot, dataset: CandidateDataset,
    expected: ApprovedArtifactIdentity,
) -> str:
    path = _canonical_path(root, DEVELOPMENT_RESULT_SUMMARY_RELPATH)
    if not os.path.isfile(path):
        raise CalibrationAuthorizationError("development result summary is missing")
    with checked_open(path, encoding="utf-8") as handle:
        summary = json.load(handle)
    if (not isinstance(summary, dict)
            or summary.get("summary_kind") != "wp2b3-development-result-summary"
            or summary.get("state") != "OWNER_WAIT"
            or summary.get("items_total") != 40):
        raise CalibrationAuthorizationError("development summary is not an OWNER_WAIT completion")
    ledger_path = canonical_ledger_path(root)
    events = ledger_module._load_verified_chain(ledger_path)
    attempt_to_logical: dict[str, str] = {}
    outcomes: dict[str, str] = {}
    for event in events:
        kind = event["event_kind"]
        if kind in ("ATTEMPT_STARTED", "ATTEMPT_TERMINAL"):
            attempt_id = event.get("attempt_id") or event.get("internal_request_id")
            if attempt_id and event.get("logical_judgment_id"):
                attempt_to_logical[attempt_id] = event["logical_judgment_id"]
        elif kind == "SEMANTIC_OUTCOME":
            logical = attempt_to_logical.get(event.get("internal_request_id", ""))
            if logical:
                if logical in outcomes:
                    raise CalibrationAuthorizationError("duplicate development semantic outcome")
                outcomes[logical] = event["outcome"]
    expected_ids = {
        calibration_request_id(item.item_id, expected.dataset_semantic_sha256)
        for item in development_items(dataset)
    }
    if len(expected_ids) != 40 or not expected_ids <= outcomes.keys():
        raise CalibrationAuthorizationError("all 40 development outcomes must be terminal")
    summary_rows = summary.get("per_item_outcomes")
    if (not isinstance(summary_rows, list) or len(summary_rows) != 40
            or {row.get("request_id"): row.get("outcome") for row in summary_rows
                if isinstance(row, dict)} != {key: outcomes[key] for key in expected_ids}):
        raise CalibrationAuthorizationError("development summary differs from durable outcomes")
    digest = _sha256_file(path)
    if (APPROVED_DEVELOPMENT_SUMMARY_SHA256 is None
            or digest != APPROVED_DEVELOPMENT_SUMMARY_SHA256):
        raise CalibrationAuthorizationError(
            "development summary lacks an independent reviewed digest"
        )
    return digest


def _holdout_summary(
    root: VerifiedEvidenceRoot, items: tuple[Any, ...],
    expected: ApprovedArtifactIdentity,
) -> dict[str, Any]:
    events = ledger_module._load_verified_chain(canonical_ledger_path(root))
    attempt_to_logical: dict[str, str] = {}
    outcomes: dict[str, str] = {}
    for event in events:
        kind = event["event_kind"]
        if kind in ("ATTEMPT_STARTED", "ATTEMPT_TERMINAL"):
            attempt = event.get("attempt_id") or event.get("internal_request_id")
            if attempt and event.get("logical_judgment_id"):
                attempt_to_logical[attempt] = event["logical_judgment_id"]
        elif kind == "SEMANTIC_OUTCOME":
            logical = attempt_to_logical.get(event.get("internal_request_id", ""))
            if logical:
                if logical in outcomes:
                    raise CalibrationAuthorizationError("duplicate semantic outcome")
                outcomes[logical] = event["outcome"]
    def empty_counts() -> dict[str, int]:
        return {"agreement": 0, "false_pass": 0,
                "critical_false_pass": 0, "false_fail": 0,
                "abstain": 0, "judge_error": 0}

    def empty_matrix() -> dict[str, dict[str, int]]:
        return {gold: {observed: 0 for observed in
                       ("PASS", "FAIL", "ABSTAIN", "JUDGE_ERROR")}
                for gold in ("PASS", "FAIL")}

    def denominators(group: tuple[Any, ...]) -> dict[str, int]:
        return {"agreement": len(group),
                "false_pass": sum(item.candidate_expected_label.value == "FAIL"
                                  for item in group),
                "critical_false_pass": sum(
                    item.candidate_expected_label.value == "FAIL"
                    and item.risk_class.value == "CRITICAL" for item in group),
                "false_fail": sum(item.candidate_expected_label.value == "PASS"
                                  for item in group),
                "abstain": len(group), "judge_error": len(group)}

    counts = empty_counts()
    matrix = empty_matrix()
    adversarial_counts = empty_counts()
    adversarial_matrix = empty_matrix()
    adversarial_items = tuple(item for item in items if item.adversarial)
    rows: list[dict[str, str]] = []
    for item in items:
        request_id = calibration_request_id(
            item.item_id, expected.dataset_semantic_sha256,
        )
        observed = outcomes.get(request_id)
        if observed is None:
            raise CalibrationAuthorizationError(
                "all 120 holdout outcomes must be terminal before summary"
            )
        gold = item.candidate_expected_label.value
        if observed in ("VALIDATED_PASS", "VALIDATED_FAIL",
                        "VALIDATED_ABSTAIN"):
            observed_label = observed.removeprefix("VALIDATED_")
        elif observed.startswith("JUDGE_ERROR"):
            observed_label = "JUDGE_ERROR"
        else:
            raise CalibrationAuthorizationError("unknown holdout outcome")
        matrix[gold][observed_label] += 1
        if item.adversarial:
            adversarial_matrix[gold][observed_label] += 1
        category = (
            "agreement" if observed_label == gold else
            "false_pass" if gold == "FAIL" and observed_label == "PASS" else
            "false_fail" if gold == "PASS" and observed_label == "FAIL" else
            "abstain" if observed_label == "ABSTAIN" else "judge_error"
        )
        counts[category] += 1
        if item.adversarial:
            adversarial_counts[category] += 1
        if category == "false_pass" and item.risk_class.value == "CRITICAL":
            counts["critical_false_pass"] += 1
            if item.adversarial:
                adversarial_counts["critical_false_pass"] += 1
        rows.append({"item_id": item.item_id,
                     "request_id": request_id, "outcome": observed})
    limits = {"agreement": [">=", 114], "false_pass": ["<=", 1],
              "critical_false_pass": ["<=", 0],
              "false_fail": ["<=", 3], "abstain": ["<=", 6],
              "judge_error": ["<=", 1]}
    passed = {name: counts[name] >= limit if operator == ">="
              else counts[name] <= limit
              for name, (operator, limit) in limits.items()}
    return {"summary_kind": "wp2b3-sealed-holdout-result-summary",
            "stage": "SEALED_HOLDOUT", "state": "HOLDOUT_COMPLETE",
            "items_total": len(items), "counts": counts,
            "confusion_matrix": matrix, "denominators": denominators(items),
            "adversarial_subset": {
                "items_total": len(adversarial_items),
                "counts": adversarial_counts,
                "confusion_matrix": adversarial_matrix,
                "denominators": denominators(adversarial_items),
            },
            "pre_registered_thresholds": limits, "thresholds_passed": passed,
            "all_thresholds_passed": all(passed.values()),
            "per_item_outcomes": rows}


class Wp2b3HoldoutDriver:
    """Verify the old evidence, durably unseal once, then dispatch 120 items."""

    def __init__(
        self, *, verified_root: VerifiedEvidenceRoot,
        freeze_artifact: gates.HoldoutFreezeArtifact,
        audited_head_sha: str, audited_tree_sha: str,
        current_head_sha: str, current_tree_sha: str,
        expected_artifacts: ApprovedArtifactIdentity = PRODUCTION_APPROVED_ARTIFACTS,
        time_source: Callable[[], float] = time.time,
        day_provider: Callable[[], str] = _utc_day,
    ) -> None:
        if not isinstance(verified_root, VerifiedEvidenceRoot):
            raise CalibrationAuthorizationError("a marker-verified evidence root is required")
        self.root = verified_root
        self.expected = expected_artifacts
        self.freeze_artifact = freeze_artifact
        self.audited_head_sha = audited_head_sha
        self.audited_tree_sha = audited_tree_sha
        self.current_head_sha = current_head_sha
        self.current_tree_sha = current_tree_sha
        self.time_source = time_source
        self.day_provider = day_provider
        self.dataset: CandidateDataset | None = None
        self.authorization: gates.HoldoutDispatchAuthorization | None = None
        self.ledger: ledger_module.CalibrationLedger | None = None
        self.binding: dict[str, Any] | None = None

    def prepare(self) -> None:
        # Revalidate the marker on disk; a stale/forged VerifiedEvidenceRoot
        # cannot move execution to a different path after construction.
        verified = verify_evidence_root(self.root.root)
        if verified != self.root:
            raise CalibrationAuthorizationError("evidence-root marker changed")
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 "..", "..", ".."))
        actual_head, actual_tree = _resolve_repo_identity(repo_root)
        if (actual_head != self.current_head_sha
                or actual_tree != self.current_tree_sha):
            raise CalibrationAuthorizationError("current source differs from audited holdout head/tree")
        self.expected.validate()
        dataset = load_approved_dataset(self.root, self.expected)
        approval = load_owner_approval(self.root, self.expected)
        authorization = gates.authorize_holdout_dispatch(
            approval=approval, dataset_identity=self.expected.gate_identity(),
            dataset=dataset, freeze_artifact=self.freeze_artifact,
            current_head_sha=self.current_head_sha,
            current_tree_sha=self.current_tree_sha,
        )
        if (authorization.approved_head_sha != self.audited_head_sha
                or authorization.approved_tree_sha != self.audited_tree_sha):
            raise CalibrationAuthorizationError("audited holdout source differs from approved source")
        actual = frozen_artifact_hashes(
            dataset, self.expected, self.root, authorization.max_output_tokens,
        )
        if actual != dict(self.freeze_artifact.frozen_sha256):
            raise CalibrationAuthorizationError("a decision-35 frozen artifact changed")
        manifest_sha = _read_verified_manifest(self.root, self.expected)
        summary_sha = _read_development_completion(self.root, dataset, self.expected)
        self.dataset = dataset
        self.authorization = authorization
        self.binding = {
            "freeze_sha256": sha256_of_obj(self.freeze_artifact.to_dict()),
            "dataset_sha256": self.expected.dataset_semantic_sha256,
            "audited_head_sha": self.audited_head_sha,
            "audited_tree_sha": self.audited_tree_sha,
            "development_manifest_sha256": manifest_sha,
            "development_summary_sha256": summary_sha,
            "max_output_tokens": authorization.max_output_tokens,
        }

    def execute(
        self, *, sdk_client: Any,
        exception_types: TransportExceptionTypes | None = None,
    ) -> dict[str, Any]:
        # The root-scoped lock spans the final preflight, durable transition,
        # every fake/live-capable dispatch and result write.
        with exclusive_lock(_canonical_path(self.root, "wp2b3-execution.lock")):
            return self._execute_locked(sdk_client, exception_types)

    def _execute_locked(
        self, sdk_client: Any,
        exception_types: TransportExceptionTypes | None,
    ) -> dict[str, Any]:
        self.prepare()  # never rely on cached preflight before the lock
        assert self.authorization is not None and self.dataset is not None
        assert self.binding is not None
        self.authorization.validate_current()
        ledger_path = canonical_ledger_path(self.root)
        ledger = ledger_module.CalibrationLedger(ledger_path)
        self.ledger = ledger
        if ledger.current_run_state() != ledger_module.RUN_STATE_OWNER_WAIT:
            raise CalibrationAuthorizationError("holdout requires durable OWNER_WAIT and a first unseal")
        if ledger.orphaned_attempt_ids or not ledger.metadata_success_recorded():
            raise CalibrationAuthorizationError("development accounting is incomplete")
        ledger.authorize_holdout_transition(**self.binding)
        # If the process dies here, the durable transition prevents a second
        # pass. If it dies after opening the segment, the open segment also
        # blocks replay. Either case requires a new owner disposition.
        ledger.begin_active_segment("SEALED_HOLDOUT", self.time_source())
        try:
            client = provider.CalibrationJudgeClient(
                authorization=self.authorization, ledger=ledger,
                sdk_client=sdk_client, exception_types=exception_types,
                day_provider=self.day_provider, time_source=self.time_source,
            )
            items = tuple(sorted(
                holdout_items(self.dataset, self.authorization.freeze_authorization),
                key=lambda item: item.item_id,
            ))
            if len(items) != 120:
                raise CalibrationAuthorizationError("sealed holdout must contain 120 items")
            for item in items:
                self.authorization.validate_current()
                content = CalibrationItemContent.from_item(
                    item, holdout_authorization=self.authorization.freeze_authorization,
                )
                envelope = build_calibration_envelope(content)
                request = build_calibration_judge_request(
                    content=content, envelope=envelope,
                    dataset_id=self.expected.dataset_id,
                    dataset_version=self.expected.dataset_version,
                    dataset_sha256=self.expected.dataset_semantic_sha256,
                )
                outcome = provider.dispatch_calibration_judgment(client, request, envelope)
                if not outcome.is_verdict:
                    entries = [entry for entry in ledger.entries()
                               if entry.logical_judgment_id == request.request_id]
                    if entries and not any(entry.outcome_kind == "OUTPUT_RECEIVED_UNVALIDATED"
                                           for entry in entries):
                        ledger.record_semantic_outcome(
                            entries[-1].internal_request_id,
                            f"JUDGE_ERROR_{outcome.judge_error_kind or 'UNCLASSIFIED'}",
                            detail=request.request_id,
                        )
        except (CalibrationStopError, CalibrationReservationDenied) as exc:
            ledger.record_run_state(
                ledger_module.RUN_STATE_STOPPED,
                reason=exc.stop_reason.value if isinstance(exc, CalibrationStopError)
                else CalibrationStopReason.CAP_WOULD_BE_EXCEEDED.value,
            )
            ledger.end_active_segment(self.time_source())
            raise
        ledger.end_active_segment(self.time_source())
        summary = _holdout_summary(self.root, items, self.expected)
        summary["freeze_sha256"] = self.binding["freeze_sha256"]
        summary["development_manifest_sha256"] = self.binding[
            "development_manifest_sha256"
        ]
        summary["development_summary_sha256"] = self.binding[
            "development_summary_sha256"
        ]
        self._persist_summary(summary)
        return summary

    def _persist_summary(self, summary: dict[str, Any]) -> None:
        summary_path = _canonical_path(self.root, HOLDOUT_RESULT_SUMMARY_RELPATH)
        with checked_open(summary_path, "x", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(summary, sort_keys=True, indent=2) + "\n")
            handle.flush()
            os.fsync(handle.fileno())

    def recover_summary(self) -> dict[str, Any]:
        """Complete a crashed result write from immutable evidence only.

        This never constructs a client or reopens provider execution. It is
        allowed solely after one fully closed 120-outcome holdout pass.
        """
        with exclusive_lock(_canonical_path(self.root, "wp2b3-execution.lock")):
            self.prepare()
            assert self.authorization is not None and self.dataset is not None
            assert self.binding is not None
            path = _canonical_path(self.root, HOLDOUT_RESULT_SUMMARY_RELPATH)
            if os.path.exists(path):
                raise CalibrationAuthorizationError("holdout result summary already exists")
            events = ledger_module._load_verified_chain(canonical_ledger_path(self.root))
            transitions = [e for e in events if e["event_kind"] == "HOLDOUT_TRANSITION"]
            if (len(transitions) != 1 or any(
                transitions[0].get(key) != value
                for key, value in self.binding.items()
            )):
                raise CalibrationAuthorizationError("durable holdout binding is missing or changed")
            started = {e["attempt_id"] for e in events
                       if e["event_kind"] == "ATTEMPT_STARTED"}
            terminal = {e["internal_request_id"] for e in events
                        if e["event_kind"] == "ATTEMPT_TERMINAL"}
            holdout_begins = [e for e in events if e["event_kind"] == "ACTIVE_SEGMENT_BEGIN"
                              and e.get("stage") == "SEALED_HOLDOUT"]
            holdout_ends = [e for e in events if e["event_kind"] == "ACTIVE_SEGMENT_END"
                            and e["event_seq"] > transitions[0]["event_seq"]]
            if (started - terminal or len(holdout_begins) != 1
                    or len(holdout_ends) != 1
                    or any(e["event_kind"] == "RUN_STATE_TRANSITION"
                           and e.get("run_state") == ledger_module.RUN_STATE_STOPPED
                           for e in events if e["event_seq"] > transitions[0]["event_seq"])):
                raise CalibrationAuthorizationError("holdout pass is incomplete or stopped")
            items = tuple(sorted(holdout_items(
                self.dataset, self.authorization.freeze_authorization,
            ), key=lambda item: item.item_id))
            if len(items) != 120:
                raise CalibrationAuthorizationError("sealed holdout must contain 120 items")
            summary = _holdout_summary(self.root, items, self.expected)
            summary.update({key: self.binding[key] for key in (
                "freeze_sha256", "development_manifest_sha256",
                "development_summary_sha256",
            )})
            self._persist_summary(summary)
            return summary
