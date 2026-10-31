"""Run limits, the owner allowlist and the live configuration record.

The strict model pins, judge routes and credential environment-variable names
live in exactly one module, live/providers.py, and are re-exported here. The
price table is a PINNED configuration input, not an observed bill: the ceiling
is enforced against it in integer cents, rounded up per call, and a config file
that declares a different price table is refused rather than silently used.

The judge allowlist is an owner artifact. An empty allowlist authorizes no judge
dispatch, and the gate record is the only source that can populate it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from . import LIVE_SCHEMA_VERSION
from .errors import LiveError
from .providers import (  # re-exported: the single provider-naming module
    CREDENTIAL_ENV_VARS,
    JUDGE_PINS,
    SUBJECT_PINS,
    ModelPin,
    judge_pin_for,
)

#: Owner pilot limits (2026-10-29 brief): $150 subject to a $120 provider cap.
OWNER_PILOT_CEILING_CENTS = 15000
OWNER_PROVIDER_CAP_CENTS = 12000
#: Pilot A shape: 20 skills, 3 runs per case, with and without baseline.
OWNER_PILOT_CASE_COUNT = 20
OWNER_PILOT_RUNS_PER_CASE = 3

DEFAULT_MAX_OUTPUT_TOKENS = 2048
DEFAULT_REQUEST_TIMEOUT_SECONDS = 300
#: Per-request input bound (bytes). An uncapped request is an open-ended bill;
#: a request over this bound is refused BEFORE any reservation or dispatch.
DEFAULT_MAX_INPUT_BYTES = 200_000

#: Live-setting floor for the output budget. The first Pilot A live dispatch
#: halted fail-closed after one call because the build-only dry-run template
#: (max_output_tokens 512) had never been raised for live: the subject response
#: was truncated at the provider stop reason. A live verb refuses any config
#: below this floor BEFORE it resolves a credential or reserves a call. 4096 is
#: the owner-directed live value: twice the build-only package default (2048),
#: with headroom for the longest committed case prompt and long-form answer,
#: and a worst-case reservation bound that stays under the unchanged $120 cap
#: (see live/config/pilot-a-live-config.json and the fix PR cost table).
MIN_LIVE_MAX_OUTPUT_TOKENS = 4096

#: The single-case live smoke hard ceiling, in cents ($0.50). The smoke meter
#: uses min(this, config ceiling, gate ceiling, provider cap), so a smoke cannot
#: spend more than 5000 cents even when handed the full pilot gate and config.
SMOKE_CEILING_CENTS = 5000

#: The committed build-only/no-spend dry-run config template, relative to the
#: repository root. A live verb refuses this source: its spend-affecting values
#: were authored for a synthetic mock run and never had a live-setting review.
DRY_RUN_CONFIG_TEMPLATE_RELPATH = (
    "tools/behavioral_eval_runner/live/config/dry-run-config.json"
)


def expected_price_table() -> dict[str, Any]:
    return {vendor: pin.to_dict() for vendor, pin in sorted(SUBJECT_PINS.items())}


def expected_owner_limits() -> dict[str, Any]:
    return {
        "pilot_ceiling_cents": OWNER_PILOT_CEILING_CENTS,
        "provider_cap_cents": OWNER_PROVIDER_CAP_CENTS,
        "pilot_case_count": OWNER_PILOT_CASE_COUNT,
        "pilot_runs_per_case": OWNER_PILOT_RUNS_PER_CASE,
        # Descriptive owner-pilot shape; the gate enforces the spend ceiling,
        # the pinned models, the terms and the dataset, not a fixed case count.
        "pilot_case_count_is_descriptive": True,
    }


@dataclass(frozen=True, slots=True)
class OwnerAllowlist:
    """Owner-authorized judge models. Empty means no judge dispatch."""

    entries: tuple[tuple[str, str], ...] = ()

    def permits(self, vendor: str, model: str) -> bool:
        return (vendor, model) in self.entries

    def validate(self) -> None:
        for vendor, model in self.entries:
            if not isinstance(vendor, str) or not vendor:
                raise LiveError("allowlist vendor must be a non-empty string")
            if not isinstance(model, str) or not model:
                raise LiveError("allowlist model must be a non-empty string")
        if len(set(self.entries)) != len(self.entries):
            raise LiveError("allowlist contains a duplicate judge entry")

    def to_dict(self) -> dict[str, Any]:
        return {
            "judge_models": [
                {"vendor": vendor, "model": model}
                for vendor, model in sorted(self.entries)
            ]
        }


@dataclass(frozen=True, slots=True)
class LiveConfig:
    """Runtime configuration for the gated verbs (owner artifact, JSON file)."""

    spend_ceiling_cents: int
    judge_allowlist: OwnerAllowlist
    max_output_tokens: int = DEFAULT_MAX_OUTPUT_TOKENS
    max_input_bytes: int = DEFAULT_MAX_INPUT_BYTES
    runs_per_case: int = OWNER_PILOT_RUNS_PER_CASE
    request_timeout_seconds: int = DEFAULT_REQUEST_TIMEOUT_SECONDS
    subject_vendors: tuple[str, ...] = tuple(SUBJECT_PINS)
    schema_version: str = LIVE_SCHEMA_VERSION

    def validate(self) -> None:
        if self.schema_version != LIVE_SCHEMA_VERSION:
            raise LiveError(
                f"config schema_version must be {LIVE_SCHEMA_VERSION}, got "
                f"{self.schema_version!r}"
            )
        if not isinstance(self.spend_ceiling_cents, int) or isinstance(
            self.spend_ceiling_cents, bool
        ):
            raise LiveError("spend_ceiling_cents must be an int")
        if not 0 < self.spend_ceiling_cents <= OWNER_PILOT_CEILING_CENTS:
            raise LiveError(
                "spend_ceiling_cents must be > 0 and <= the owner ceiling "
                f"{OWNER_PILOT_CEILING_CENTS}"
            )
        for name, value in (
            ("max_output_tokens", self.max_output_tokens),
            ("max_input_bytes", self.max_input_bytes),
            ("runs_per_case", self.runs_per_case),
            ("request_timeout_seconds", self.request_timeout_seconds),
        ):
            if not isinstance(value, int) or isinstance(value, bool) or value < 1:
                raise LiveError(f"{name} must be an int >= 1 (bool is not accepted)")
        if self.runs_per_case > OWNER_PILOT_RUNS_PER_CASE:
            raise LiveError(
                f"runs_per_case must be <= {OWNER_PILOT_RUNS_PER_CASE} (owner shape)"
            )
        if not self.subject_vendors or len(set(self.subject_vendors)) != len(
            self.subject_vendors
        ):
            raise LiveError("subject_vendors must be a non-empty unique tuple")
        for vendor in self.subject_vendors:
            if vendor not in SUBJECT_PINS:
                raise LiveError(f"subject vendor {vendor!r} has no pinned model")
        self.judge_allowlist.validate()

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "spend_ceiling_cents": self.spend_ceiling_cents,
            "max_output_tokens": self.max_output_tokens,
            "max_input_bytes": self.max_input_bytes,
            "runs_per_case": self.runs_per_case,
            "request_timeout_seconds": self.request_timeout_seconds,
            "subject_vendors": list(self.subject_vendors),
            "judge_allowlist": self.judge_allowlist.to_dict(),
            "price_table": expected_price_table(),
            "owner_limits": expected_owner_limits(),
        }

    _KEYS = frozenset(
        {
            "schema_version",
            "spend_ceiling_cents",
            "max_output_tokens",
            "max_input_bytes",
            "runs_per_case",
            "request_timeout_seconds",
            "subject_vendors",
            "judge_allowlist",
            # Evidence views emitted by to_dict; accepted only if they match
            # the code constants exactly, so a config round-trips and a tampered
            # price table is refused.
            "price_table",
            "owner_limits",
        }
    )

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "LiveConfig":
        if not isinstance(payload, Mapping):
            raise LiveError("the live configuration must be a JSON object")
        unknown = set(payload) - cls._KEYS
        if unknown:
            raise LiveError(f"LiveConfig: unknown keys {sorted(unknown)}")
        raw_allow = payload.get("judge_allowlist", {})
        if not isinstance(raw_allow, Mapping):
            raise LiveError("judge_allowlist must be an object")
        if set(raw_allow) - {"judge_models"}:
            raise LiveError(
                f"judge_allowlist has unknown keys {sorted(set(raw_allow) - {'judge_models'})}"
            )
        raw_models = raw_allow.get("judge_models", [])
        if not isinstance(raw_models, list):
            raise LiveError("judge_allowlist.judge_models must be a list")
        entries: list[tuple[str, str]] = []
        for item in raw_models:
            if not isinstance(item, Mapping) or set(item) != {"vendor", "model"}:
                raise LiveError("judge_allowlist entries need exactly vendor and model")
            vendor, model = item["vendor"], item["model"]
            if not isinstance(vendor, str) or not isinstance(model, str):
                raise LiveError("judge_allowlist vendor and model must be strings")
            entries.append((vendor, model))
        if "price_table" in payload and payload["price_table"] != expected_price_table():
            raise LiveError("config price_table does not match the pinned price table")
        if "owner_limits" in payload and payload["owner_limits"] != expected_owner_limits():
            raise LiveError("config owner_limits do not match the owner limits")
        raw_vendors = payload.get("subject_vendors", tuple(SUBJECT_PINS))
        if not isinstance(raw_vendors, (list, tuple)) or not all(
            isinstance(item, str) for item in raw_vendors
        ):
            raise LiveError("subject_vendors must be a list of vendor strings")
        config = cls(
            spend_ceiling_cents=payload.get("spend_ceiling_cents", 0),
            judge_allowlist=OwnerAllowlist(tuple(sorted(entries))),
            max_output_tokens=payload.get(
                "max_output_tokens", DEFAULT_MAX_OUTPUT_TOKENS
            ),
            max_input_bytes=payload.get("max_input_bytes", DEFAULT_MAX_INPUT_BYTES),
            runs_per_case=payload.get("runs_per_case", OWNER_PILOT_RUNS_PER_CASE),
            request_timeout_seconds=payload.get(
                "request_timeout_seconds", DEFAULT_REQUEST_TIMEOUT_SECONDS
            ),
            subject_vendors=tuple(raw_vendors),
            schema_version=payload.get("schema_version", ""),
        )
        config.validate()
        return config
