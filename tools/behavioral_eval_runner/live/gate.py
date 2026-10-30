"""Owner gate and fact provenance for real-host live execution.

A live verb needs a committed/gated owner record that states the dataset
revision and digest, the pinned model identifiers, the model-terms
acknowledgment and the spend ceiling. A SYNTHETIC record can exercise the
dry-run pipeline but can never authorize a live run: real host facts and
synthetic facts are different classes and are labeled as such everywhere.
"""

from __future__ import annotations

import datetime as dt
import json
import os
from dataclasses import dataclass
from typing import Any, Mapping

from ..canonical import canonical_bytes, sha256_hex
from . import LIVE_SCHEMA_VERSION
from .config import (
    JUDGE_PINS,
    OWNER_PILOT_CEILING_CENTS,
    OWNER_PROVIDER_CAP_CENTS,
    SUBJECT_PINS,
    LiveConfig,
    ModelPin,
)
from .errors import JudgeVendorGuardError, LiveGateRefusedError

GATE_KIND = "ber-live-owner-gate"
SYNTHETIC = "SYNTHETIC"
REAL_HOST = "REAL_HOST"
FACT_ORIGINS = frozenset({SYNTHETIC, REAL_HOST})


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise LiveGateRefusedError(message)


def _require_str(value: Any, where: str) -> str:
    _require(isinstance(value, str) and value.strip() != "", f"{where} must be a non-empty string")
    return value


def _is_hex(value: Any, length: int) -> bool:
    return isinstance(value, str) and len(value) == length and set(value) <= set("0123456789abcdef")


def _parse_time(value: Any, where: str) -> dt.datetime:
    if not isinstance(value, str) or not value:
        raise LiveGateRefusedError(f"{where} must be an ISO-8601 timestamp")
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise LiveGateRefusedError(f"{where} is not ISO-8601: {value!r}") from exc
    if parsed.tzinfo is None:
        raise LiveGateRefusedError(f"{where} must be timezone-aware")
    return parsed.astimezone(dt.timezone.utc)


@dataclass(frozen=True, slots=True)
class ModelTermsAcknowledgment:
    acknowledged: bool
    terms_ref: str
    acknowledged_on: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "acknowledged": self.acknowledged,
            "terms_ref": self.terms_ref,
            "acknowledged_on": self.acknowledged_on,
        }


@dataclass(frozen=True, slots=True)
class OwnerGateRecord:
    """The committed/gated record every live verb must present."""

    gate_id: str
    owner_decision_ref: str
    fact_origin: str
    dataset_revision: str
    dataset_path: str
    dataset_sha256: str
    case_count: int
    subject_models: Mapping[str, str]
    judge_models: Mapping[str, Mapping[str, str]]
    model_terms: ModelTermsAcknowledgment
    spend_ceiling_cents: int
    provider_cap_cents: int
    created_at: str
    expires_at: str
    schema_version: str = LIVE_SCHEMA_VERSION

    # ------------------------------------------------------------- validation
    def validate(self) -> None:
        _require(self.schema_version == LIVE_SCHEMA_VERSION, "gate schema_version mismatch")
        _require_str(self.gate_id, "gate_id")
        _require_str(self.owner_decision_ref, "owner_decision_ref")
        _require(self.fact_origin in FACT_ORIGINS, f"fact_origin must be one of {sorted(FACT_ORIGINS)}")
        _require(_is_hex(self.dataset_revision, 40), "dataset_revision must be a 40-hex commit")
        _require_str(self.dataset_path, "dataset_path")
        _require(
            not os.path.isabs(self.dataset_path) and ".." not in self.dataset_path.replace("\\", "/").split("/"),
            "dataset_path must be repository-relative with no parent traversal",
        )
        _require(_is_hex(self.dataset_sha256, 64), "dataset_sha256 must be a 64-hex SHA-256")
        _require(
            isinstance(self.case_count, int) and not isinstance(self.case_count, bool) and self.case_count > 0,
            "case_count must be a positive int",
        )
        _require(
            isinstance(self.subject_models, Mapping),
            "subject_models must be an object",
        )
        _require(
            set(self.subject_models) == set(SUBJECT_PINS),
            f"subject_models must pin exactly {sorted(SUBJECT_PINS)}",
        )
        for vendor, model in self.subject_models.items():
            _require_str(model, f"subject_models[{vendor}]")
            _require(
                model == SUBJECT_PINS[vendor].model,
                f"subject_models[{vendor}] must be the pinned {SUBJECT_PINS[vendor].model!r}, "
                f"got {model!r} (strict model pinning: no substitution)",
            )
        _require(
            isinstance(self.judge_models, Mapping),
            "judge_models must be an object",
        )
        _require(
            set(self.judge_models) == set(SUBJECT_PINS),
            "judge_models must route exactly the pinned subject vendors",
        )
        for subject_vendor, route in self.judge_models.items():
            _require(isinstance(route, Mapping), f"judge_models[{subject_vendor}] must be an object")
            _require(set(route) == {"vendor", "model"}, "judge route needs exactly vendor and model")
            _require_str(route.get("vendor"), f"judge_models[{subject_vendor}].vendor")
            _require_str(route.get("model"), f"judge_models[{subject_vendor}].model")
            expected = JUDGE_PINS.get((subject_vendor, SUBJECT_PINS[subject_vendor].model))
            _require(expected is not None, f"no pinned judge route for {subject_vendor}")
            _require(
                route["vendor"] != subject_vendor,
                f"judge_models[{subject_vendor}] shares the subject vendor: a judge must differ "
                "from the subject vendor",
            )
            _require(
                (route["vendor"], route["model"]) == (expected.vendor, expected.model),
                f"judge_models[{subject_vendor}] must be the pinned cross-vendor route "
                f"{expected.vendor}/{expected.model}",
            )
        _require(self.model_terms.acknowledged is True, "model terms must be explicitly acknowledged")
        _require_str(self.model_terms.terms_ref, "model terms reference")
        _require_str(self.model_terms.acknowledged_on, "model terms date")
        _require(
            isinstance(self.spend_ceiling_cents, int)
            and not isinstance(self.spend_ceiling_cents, bool)
            and 0 < self.spend_ceiling_cents <= OWNER_PILOT_CEILING_CENTS,
            f"spend_ceiling_cents must be > 0 and <= {OWNER_PILOT_CEILING_CENTS}",
        )
        _require(
            isinstance(self.provider_cap_cents, int)
            and not isinstance(self.provider_cap_cents, bool)
            and 0 < self.provider_cap_cents <= OWNER_PROVIDER_CAP_CENTS,
            f"provider_cap_cents must be > 0 and <= {OWNER_PROVIDER_CAP_CENTS}",
        )
        created = _parse_time(self.created_at, "created_at")
        expires = _parse_time(self.expires_at, "expires_at")
        _require(expires > created, "expires_at must be after created_at")

    # -------------------------------------------------------------- accessors
    def effective_ceiling_cents(self, config: LiveConfig) -> int:
        """The binding ceiling: config, gate ceiling and provider cap, minimum."""
        return min(
            config.spend_ceiling_cents,
            self.spend_ceiling_cents,
            self.provider_cap_cents,
        )

    def judge_pin(self, subject_vendor: str) -> ModelPin:
        route = self.judge_models[subject_vendor]
        vendor = str(route["vendor"])
        model = str(route["model"])
        pin = JUDGE_PINS.get((subject_vendor, SUBJECT_PINS[subject_vendor].model))
        if pin is None or pin.vendor != vendor or pin.model != model:
            raise JudgeVendorGuardError(
                f"judge route for {subject_vendor} is not the pinned cross-vendor route",
                context={"subject_vendor": subject_vendor, "judge_vendor": vendor, "judge_model": model},
            )
        return pin

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "gate_kind": GATE_KIND,
            "gate_id": self.gate_id,
            "owner_decision_ref": self.owner_decision_ref,
            "fact_origin": self.fact_origin,
            "dataset": {
                "revision": self.dataset_revision,
                "path": self.dataset_path,
                "sha256": self.dataset_sha256,
                "case_count": self.case_count,
            },
            "models": {
                "subjects": dict(sorted(self.subject_models.items())),
                "judges": {k: dict(sorted(v.items())) for k, v in sorted(self.judge_models.items())},
            },
            "model_terms": self.model_terms.to_dict(),
            "spend": {
                "ceiling_cents": self.spend_ceiling_cents,
                "provider_cap_cents": self.provider_cap_cents,
            },
            "created_at": self.created_at,
            "expires_at": self.expires_at,
        }

    def digest(self) -> str:
        return sha256_hex(canonical_bytes(self.to_dict()))

    # ------------------------------------------------------------- deserialization
    _KEYS = frozenset(
        {
            "schema_version",
            "gate_kind",
            "gate_id",
            "owner_decision_ref",
            "fact_origin",
            "dataset",
            "models",
            "model_terms",
            "spend",
            "created_at",
            "expires_at",
        }
    )

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "OwnerGateRecord":
        if not isinstance(payload, Mapping):
            raise LiveGateRefusedError("gate record must be an object")
        unknown = set(payload) - cls._KEYS
        if unknown:
            raise LiveGateRefusedError(f"gate record has unknown keys {sorted(unknown)}")
        if payload.get("gate_kind") != GATE_KIND:
            raise LiveGateRefusedError(f"gate_kind must be {GATE_KIND!r}")
        dataset = payload.get("dataset", {})
        models = payload.get("models", {})
        terms = payload.get("model_terms", {})
        spend = payload.get("spend", {})
        for name, value, keys in (
            ("dataset", dataset, {"revision", "path", "sha256", "case_count"}),
            ("models", models, {"subjects", "judges"}),
            ("model_terms", terms, {"acknowledged", "terms_ref", "acknowledged_on"}),
            ("spend", spend, {"ceiling_cents", "provider_cap_cents"}),
        ):
            if not isinstance(value, Mapping) or set(value) != keys:
                raise LiveGateRefusedError(f"gate {name} must contain exactly {sorted(keys)}")
        if not isinstance(models.get("subjects"), Mapping):
            raise LiveGateRefusedError("gate models.subjects must be an object")
        judges = models.get("judges", {})
        if not isinstance(judges, Mapping):
            raise LiveGateRefusedError("gate models.judges must be an object")
        record = cls(
            gate_id=payload.get("gate_id", ""),
            owner_decision_ref=payload.get("owner_decision_ref", ""),
            fact_origin=payload.get("fact_origin", ""),
            dataset_revision=dataset.get("revision", ""),
            dataset_path=dataset.get("path", ""),
            dataset_sha256=dataset.get("sha256", ""),
            case_count=dataset.get("case_count", 0),
            subject_models=dict(models.get("subjects", {})),
            judge_models={
                key: dict(value) if isinstance(value, Mapping) else value
                for key, value in judges.items()
            },
            model_terms=ModelTermsAcknowledgment(
                acknowledged=terms.get("acknowledged", False),
                terms_ref=terms.get("terms_ref", ""),
                acknowledged_on=terms.get("acknowledged_on", ""),
            ),
            spend_ceiling_cents=spend.get("ceiling_cents", 0),
            provider_cap_cents=spend.get("provider_cap_cents", 0),
            created_at=payload.get("created_at", ""),
            expires_at=payload.get("expires_at", ""),
            schema_version=payload.get("schema_version", ""),
        )
        record.validate()
        return record


def load_gate(path: str) -> OwnerGateRecord:
    """Load the committed/gated owner record; missing or invalid fails closed."""
    if not path or not os.path.isfile(path):
        raise LiveGateRefusedError(
            f"owner gate record not found: {path!r}",
            context={"gate_path": path, "required": True},
        )
    try:
        with open(path, encoding="utf-8") as handle:
            payload = json.load(handle)
    except (OSError, ValueError) as exc:
        raise LiveGateRefusedError(
            f"owner gate record is unreadable: {exc}", context={"gate_path": path}
        ) from exc
    return OwnerGateRecord.from_dict(payload)


def authorize_judges(gate: OwnerGateRecord, config: LiveConfig) -> dict[str, ModelPin]:
    """Every gate judge route must be inside the owner allowlist."""
    authorized: dict[str, ModelPin] = {}
    for subject_vendor in sorted(gate.judge_models):
        pin = gate.judge_pin(subject_vendor)
        if pin.vendor == subject_vendor:
            raise JudgeVendorGuardError(
                "judge vendor equals the subject vendor; refusing",
                context={"subject_vendor": subject_vendor, "judge_vendor": pin.vendor},
            )
        if not config.judge_allowlist.permits(pin.vendor, pin.model):
            raise JudgeVendorGuardError(
                f"judge {pin.vendor}/{pin.model} is not in the owner allowlist",
                context={
                    "subject_vendor": subject_vendor,
                    "judge_vendor": pin.vendor,
                    "judge_model": pin.model,
                    "allowlist": config.judge_allowlist.to_dict(),
                },
            )
        authorized[subject_vendor] = pin
    return authorized


def require_live_gate(
    gate: OwnerGateRecord | None,
    config: LiveConfig,
    *,
    now: dt.datetime | None = None,
    allowed_origins: frozenset[str] = frozenset({REAL_HOST}),
) -> int:
    """Refuse unless the gate is real-host, unexpired and inside owner limits.

    Returns the effective spend ceiling in integer cents.
    """
    if gate is None:
        raise LiveGateRefusedError(
            "no owner gate record was supplied; a live verb is refused",
            context={"required": ["dataset revision", "model pins", "model terms", "spend ceiling"]},
        )
    now = now or dt.datetime.now(dt.timezone.utc)
    if gate.fact_origin not in allowed_origins:
        raise LiveGateRefusedError(
            f"gate fact_origin {gate.fact_origin} cannot authorize this verb "
            f"(allowed: {sorted(allowed_origins)})",
            context={"fact_origin": gate.fact_origin, "allowed_origins": sorted(allowed_origins)},
        )
    if _parse_time(gate.created_at, "created_at") > now:
        raise LiveGateRefusedError(
            "the owner gate was created in the future",
            context={"created_at": gate.created_at, "now": now.isoformat()},
        )
    if now >= _parse_time(gate.expires_at, "expires_at"):
        raise LiveGateRefusedError(
            "the owner gate has expired",
            context={"expires_at": gate.expires_at, "now": now.isoformat()},
        )
    authorize_judges(gate, config)
    return gate.effective_ceiling_cents(config)
