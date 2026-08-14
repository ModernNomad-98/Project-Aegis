"""Trusted grading plans (R2 correction; PR85 §4).

A ``TrustedGradingPlan`` is the versioned, immutable, canonical, hash-bound
TRUSTED context a deterministic grader grades against: expected targets,
answer-bank identity, required start state, loop threshold, owner-gate IDs,
semantic gates, expected final IDs, expected workspace/stage state, and the
exact required deterministic oracle set — all bound to the current control
contract by hash. Plans are control-plane material: OBSERVED evidence can
neither contain nor override any plan field, and every grader binds the plan
hash and the observed-evidence hash separately in its result."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from .. import GRADING_SCHEMA_VERSION
from ..canonical import sha256_of_obj
from ..enums import InvocationMode, TargetKind
from ..errors import SchemaValidationError, UnknownEnumValueError
from ..identity import parse_case_uid
from .contract import CONTRACT_VERSION, load_contract
from .records import ORACLE_IDS, VALID_CONTROL_IDS

PLAN_SCHEMA_VERSION = GRADING_SCHEMA_VERSION

_HEX = set("0123456789abcdef")

_WORKSPACE_ROLES = ("consumer", "source_library")

_SEMANTIC_GATE_KEYS = frozenset(
    {
        "spec_acceptance_id",
        "spec_owner_completion_id",
        "stage2_owner_ids",
        "stage3_snapshot_id",
        "forbidden_snapshot_ids",
    }
)

_ID_SECTIONS = ("State snapshots", "Decision log", "Approvals")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise SchemaValidationError(message)


def _require_str_list(value: Any, where: str, allow_empty: bool = True) -> tuple[str, ...]:
    _require(
        isinstance(value, (list, tuple))
        and all(isinstance(item, str) and item for item in value),
        f"{where} must be a JSON list of non-empty strings, got {value!r}",
    )
    result = tuple(value)
    if not allow_empty:
        _require(bool(result), f"{where} must not be empty")
    return result


def _deep_freeze(obj: Any) -> Any:
    if isinstance(obj, Mapping):
        return MappingProxyType({str(k): _deep_freeze(v) for k, v in obj.items()})
    if isinstance(obj, (list, tuple)):
        return tuple(_deep_freeze(v) for v in obj)
    return obj


def _to_plain(obj: Any) -> Any:
    if isinstance(obj, Mapping):
        return {k: _to_plain(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_plain(v) for v in obj]
    return obj


@dataclass(frozen=True, slots=True)
class TrustedGradingPlan:
    plan_id: str
    case_uid: str
    control_id: str
    contract_version: str
    contract_sha256: str
    required_oracle_ids: tuple[str, ...]
    trusted_source_refs: tuple[str, ...]
    plan_sha256: str
    expected_target: Mapping[str, str] | None = None
    answer_bank: Mapping[str, Any] | None = None
    required_start_state: str | None = None
    loop_threshold: int | None = None
    required_gate_ids: tuple[str, ...] | None = None
    semantic_gates: Mapping[str, Any] | None = None
    expected_final_ids: Mapping[str, Any] | None = None
    expected_workspace_role: str | None = None
    expected_stage_zero: bool | None = None
    plan_version: str = PLAN_SCHEMA_VERSION
    schema_version: str = PLAN_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.expected_target is not None:
            object.__setattr__(self, "expected_target", _deep_freeze(self.expected_target))
        if self.answer_bank is not None:
            object.__setattr__(self, "answer_bank", _deep_freeze(self.answer_bank))
        if self.semantic_gates is not None:
            object.__setattr__(self, "semantic_gates", _deep_freeze(self.semantic_gates))
        if self.expected_final_ids is not None:
            object.__setattr__(
                self, "expected_final_ids", _deep_freeze(self.expected_final_ids)
            )
        object.__setattr__(
            self, "required_oracle_ids", tuple(self.required_oracle_ids)
        )
        object.__setattr__(
            self, "trusted_source_refs", tuple(self.trusted_source_refs)
        )
        if self.required_gate_ids is not None:
            object.__setattr__(
                self, "required_gate_ids", tuple(self.required_gate_ids)
            )

    # ---------------------------------------------------------------- content
    def _content_dict(self) -> dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "plan_version": self.plan_version,
            "case_uid": self.case_uid,
            "control_id": self.control_id,
            "contract_version": self.contract_version,
            "contract_sha256": self.contract_sha256,
            "required_oracle_ids": list(self.required_oracle_ids),
            "trusted_source_refs": list(self.trusted_source_refs),
            "expected_target": _to_plain(self.expected_target)
            if self.expected_target is not None
            else None,
            "answer_bank": _to_plain(self.answer_bank)
            if self.answer_bank is not None
            else None,
            "required_start_state": self.required_start_state,
            "loop_threshold": self.loop_threshold,
            "required_gate_ids": list(self.required_gate_ids)
            if self.required_gate_ids is not None
            else None,
            "semantic_gates": _to_plain(self.semantic_gates)
            if self.semantic_gates is not None
            else None,
            "expected_final_ids": _to_plain(self.expected_final_ids)
            if self.expected_final_ids is not None
            else None,
            "expected_workspace_role": self.expected_workspace_role,
            "expected_stage_zero": self.expected_stage_zero,
            "schema_version": self.schema_version,
        }

    def validate(self) -> None:
        _require(
            isinstance(self.plan_id, str) and bool(self.plan_id), "plan_id required"
        )
        parse_case_uid(self.case_uid)
        _require(
            self.control_id in VALID_CONTROL_IDS,
            f"control_id must be a Scenario A control A-Q, got {self.control_id!r}",
        )
        _require(
            self.contract_version == CONTRACT_VERSION,
            f"contract_version must be {CONTRACT_VERSION}",
        )
        contract = load_contract()
        _require(
            self.contract_sha256 == contract.contract_hash(),
            "contract_sha256 does not match the current grading contract "
            "(the plan is bound to the contract it was authored against)",
        )
        control = next(
            c for c in contract.controls if c.control_id == self.control_id
        )
        _require(
            self.required_oracle_ids == control.required_oracle_ids,
            f"{self.control_id}: plan required_oracle_ids "
            f"{list(self.required_oracle_ids)} must equal the contract's "
            f"{list(control.required_oracle_ids)}",
        )
        for oracle_id in self.required_oracle_ids:
            _require(
                oracle_id in ORACLE_IDS, f"unknown oracle id {oracle_id!r}"
            )
        _require_str_list(
            self.trusted_source_refs, "trusted_source_refs", allow_empty=False
        )
        if self.expected_target is not None:
            _require(
                isinstance(self.expected_target, Mapping)
                and set(self.expected_target)
                == {"target_kind", "target_name", "invocation_mode"},
                "expected_target must carry exactly "
                "{target_kind, target_name, invocation_mode}",
            )
            try:
                TargetKind.parse(self.expected_target["target_kind"])
                InvocationMode.parse(self.expected_target["invocation_mode"])
            except UnknownEnumValueError as exc:
                raise SchemaValidationError(str(exc)) from exc
            _require(
                isinstance(self.expected_target["target_name"], str)
                and bool(self.expected_target["target_name"]),
                "expected_target.target_name required",
            )
        if self.answer_bank is not None:
            _require(
                isinstance(self.answer_bank, Mapping)
                and set(self.answer_bank)
                == {"bank_id", "version", "sha256", "answer_ids"},
                "answer_bank must carry exactly {bank_id, version, sha256, answer_ids}",
            )
            _require(
                isinstance(self.answer_bank["bank_id"], str)
                and bool(self.answer_bank["bank_id"]),
                "answer_bank.bank_id required",
            )
            _require(
                isinstance(self.answer_bank["version"], str)
                and bool(self.answer_bank["version"]),
                "answer_bank.version required",
            )
            answer_ids = _require_str_list(
                self.answer_bank["answer_ids"], "answer_bank.answer_ids",
                allow_empty=False,
            )
            expected_sha = sha256_of_obj(list(answer_ids))
            _require(
                self.answer_bank["sha256"] == expected_sha,
                "answer_bank.sha256 does not match the canonical hash of "
                "answer_ids (bank identity is hash-bound)",
            )
        if self.required_start_state is not None:
            _require(
                isinstance(self.required_start_state, str)
                and self.required_start_state.startswith("STEP_"),
                "required_start_state must be a Scenario A state id",
            )
        if self.loop_threshold is not None:
            _require(
                isinstance(self.loop_threshold, int)
                and not isinstance(self.loop_threshold, bool)
                and self.loop_threshold >= 2,
                "loop_threshold must be an int >= 2",
            )
        if self.required_gate_ids is not None:
            _require_str_list(
                self.required_gate_ids, "required_gate_ids", allow_empty=False
            )
        if self.semantic_gates is not None:
            _require(
                isinstance(self.semantic_gates, Mapping)
                and set(self.semantic_gates) == _SEMANTIC_GATE_KEYS,
                f"semantic_gates must carry exactly {sorted(_SEMANTIC_GATE_KEYS)}",
            )
            for key in ("spec_acceptance_id", "spec_owner_completion_id",
                        "stage3_snapshot_id"):
                _require(
                    isinstance(self.semantic_gates[key], str)
                    and bool(self.semantic_gates[key]),
                    f"semantic_gates.{key} must be a non-empty string",
                )
            for key in ("stage2_owner_ids", "forbidden_snapshot_ids"):
                _require_str_list(
                    self.semantic_gates[key], f"semantic_gates.{key}"
                )
        if self.expected_final_ids is not None:
            _require(
                isinstance(self.expected_final_ids, Mapping)
                and set(self.expected_final_ids) <= set(_ID_SECTIONS),
                f"expected_final_ids sections must be within {_ID_SECTIONS}",
            )
            for section, ids in self.expected_final_ids.items():
                _require_str_list(
                    ids, f"expected_final_ids[{section!r}]", allow_empty=False
                )
        if self.expected_workspace_role is not None:
            _require(
                self.expected_workspace_role in _WORKSPACE_ROLES,
                f"expected_workspace_role must be one of {_WORKSPACE_ROLES}",
            )
        if self.expected_stage_zero is not None:
            _require(
                isinstance(self.expected_stage_zero, bool),
                "expected_stage_zero must be a boolean",
            )
        _require(
            self.plan_version == PLAN_SCHEMA_VERSION
            and self.schema_version == PLAN_SCHEMA_VERSION,
            f"plan/schema version must be {PLAN_SCHEMA_VERSION}",
        )
        expected_hash = sha256_of_obj(self._content_dict())
        _require(
            self.plan_sha256 == expected_hash,
            "plan_sha256 does not match the plan content (tampered or "
            "mis-built trusted plan)",
        )

    def to_dict(self) -> dict[str, Any]:
        payload = self._content_dict()
        payload["plan_sha256"] = self.plan_sha256
        return payload

    _KEYS = frozenset(
        {
            "plan_id",
            "plan_version",
            "case_uid",
            "control_id",
            "contract_version",
            "contract_sha256",
            "required_oracle_ids",
            "trusted_source_refs",
            "expected_target",
            "answer_bank",
            "required_start_state",
            "loop_threshold",
            "required_gate_ids",
            "semantic_gates",
            "expected_final_ids",
            "expected_workspace_role",
            "expected_stage_zero",
            "schema_version",
            "plan_sha256",
        }
    )

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "TrustedGradingPlan":
        unknown = set(payload) - cls._KEYS
        _require(not unknown, f"TrustedGradingPlan: unknown keys {sorted(unknown)}")
        missing = cls._KEYS - set(payload)
        _require(not missing, f"TrustedGradingPlan: missing keys {sorted(missing)}")
        for list_key in ("required_oracle_ids", "trusted_source_refs"):
            _require(
                isinstance(payload[list_key], list),
                f"{list_key} must be a JSON list",
            )
        if payload["required_gate_ids"] is not None:
            _require(
                isinstance(payload["required_gate_ids"], list),
                "required_gate_ids must be a JSON list or null",
            )
        plan = cls(
            plan_id=payload["plan_id"],
            plan_version=payload["plan_version"],
            case_uid=payload["case_uid"],
            control_id=payload["control_id"],
            contract_version=payload["contract_version"],
            contract_sha256=payload["contract_sha256"],
            required_oracle_ids=tuple(payload["required_oracle_ids"]),
            trusted_source_refs=tuple(payload["trusted_source_refs"]),
            expected_target=payload["expected_target"],
            answer_bank=payload["answer_bank"],
            required_start_state=payload["required_start_state"],
            loop_threshold=payload["loop_threshold"],
            required_gate_ids=(
                tuple(payload["required_gate_ids"])
                if payload["required_gate_ids"] is not None
                else None
            ),
            semantic_gates=payload["semantic_gates"],
            expected_final_ids=payload["expected_final_ids"],
            expected_workspace_role=payload["expected_workspace_role"],
            expected_stage_zero=payload["expected_stage_zero"],
            schema_version=payload["schema_version"],
            plan_sha256=payload["plan_sha256"],
        )
        plan.validate()
        return plan


def make_plan(
    control_id: str,
    case_uid: str,
    trusted_source_refs: tuple[str, ...],
    plan_id: str | None = None,
    expected_target: Mapping[str, str] | None = None,
    answer_bank_ids: tuple[str, ...] | None = None,
    answer_bank_id: str = "answer-bank.scenario-a.synthetic",
    answer_bank_version: str = "1.0.0-wp2b2",
    required_start_state: str | None = None,
    loop_threshold: int | None = None,
    required_gate_ids: tuple[str, ...] | None = None,
    semantic_gates: Mapping[str, Any] | None = None,
    expected_final_ids: Mapping[str, Any] | None = None,
    expected_workspace_role: str | None = None,
    expected_stage_zero: bool | None = None,
) -> TrustedGradingPlan:
    """Build, hash-bind, and validate a trusted grading plan."""
    contract = load_contract()
    control = next(
        (c for c in contract.controls if c.control_id == control_id), None
    )
    _require(control is not None, f"unknown control {control_id!r}")
    answer_bank = None
    if answer_bank_ids is not None:
        ids = list(answer_bank_ids)
        answer_bank = {
            "bank_id": answer_bank_id,
            "version": answer_bank_version,
            "sha256": sha256_of_obj(ids),
            "answer_ids": ids,
        }
    provisional = TrustedGradingPlan(
        plan_id=plan_id or f"plan.{control_id}.{case_uid.split('::')[2]}",
        case_uid=case_uid,
        control_id=control_id,
        contract_version=contract.contract_version,
        contract_sha256=contract.contract_hash(),
        required_oracle_ids=control.required_oracle_ids,
        trusted_source_refs=tuple(trusted_source_refs),
        expected_target=expected_target,
        answer_bank=answer_bank,
        required_start_state=required_start_state,
        loop_threshold=loop_threshold,
        required_gate_ids=required_gate_ids,
        semantic_gates=semantic_gates,
        expected_final_ids=expected_final_ids,
        expected_workspace_role=expected_workspace_role,
        expected_stage_zero=expected_stage_zero,
        plan_sha256="0" * 64,
    )
    bound = TrustedGradingPlan(
        **{
            **{k: getattr(provisional, k) for k in (
                "plan_id", "plan_version", "case_uid", "control_id",
                "contract_version", "contract_sha256", "required_oracle_ids",
                "trusted_source_refs", "expected_target", "answer_bank",
                "required_start_state", "loop_threshold", "required_gate_ids",
                "semantic_gates", "expected_final_ids",
                "expected_workspace_role", "expected_stage_zero",
                "schema_version",
            )},
            "plan_sha256": sha256_of_obj(provisional._content_dict()),
        }
    )
    bound.validate()
    return bound
