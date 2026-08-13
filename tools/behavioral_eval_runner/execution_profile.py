"""Versioned execution-profile representation (design §5e; prompt Phase 12).

WP-2B-1 does NOT claim any of these values are observable on the real host
(R5 is INCOMPLETE/BLOCKED). The real Claude Code profile source reports every
unobservable value as UNAVAILABLE or UNKNOWN — never a silent default — and
any required unknown/unisolatable value makes the record
``baseline_eligible = false``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, fields
from typing import Any, Mapping

from . import SCHEMA_VERSION
from .canonical import sha256_of_obj
from .enums import CapabilityState
from .errors import ProfileError

UNAVAILABLE = CapabilityState.UNAVAILABLE.value
UNKNOWN = CapabilityState.UNKNOWN.value
_SENTINELS = frozenset({UNAVAILABLE, UNKNOWN})

#: Fields whose value must be OBSERVED and ISOLATED for baseline eligibility.
REQUIRED_FOR_BASELINE = (
    "runtime_version",
    "managed_settings_status",
    "user_settings_status",
    "project_settings_status",
    "local_settings_status",
    "claude_md_scopes",
    "auto_memory_state",
    "user_skill_scope",
    "project_skill_scope",
    "subagent_scope",
    "plugin_scope",
    "hook_scope",
    "mcp_scope",
    "permission_policy",
    "sandbox_tool_policy",
    "auto_update_state",
)

#: WP-2B-1 is an OFFLINE synthetic runner. A baseline-eligible runtime must be
#: an explicitly pinned synthetic runtime; an arbitrary observed host version
#: is evidence, but is not isolated baseline evidence in this phase.
_BASELINE_SAFE_RUNTIME_VERSION = re.compile(
    r"^synthetic-[A-Za-z0-9][A-Za-z0-9._+-]{0,127}$"
)

#: Explicit isolated states accepted for every other baseline-critical field.
#: Values outside these sets remain representable as observed evidence, but
#: they make the profile baseline-ineligible. This prevents a non-empty string
#: such as ``allow-all``/``global``/``unrestricted`` from being treated as safe.
_BASELINE_SAFE_VALUES: Mapping[str, frozenset[str]] = {
    "managed_settings_status": frozenset({"absent", "pinned"}),
    "user_settings_status": frozenset({"absent", "suppressed"}),
    "project_settings_status": frozenset({"pinned"}),
    "local_settings_status": frozenset({"absent"}),
    "claude_md_scopes": frozenset({"none", "project-only"}),
    "auto_memory_state": frozenset(
        {"disabled", "isolated", "deterministically_empty"}
    ),
    "user_skill_scope": frozenset({"none", "suppressed"}),
    "project_skill_scope": frozenset({"none", "pinned-manifest"}),
    "subagent_scope": frozenset({"none", "pinned-manifest"}),
    "plugin_scope": frozenset({"none", "pinned-manifest"}),
    "hook_scope": frozenset({"none", "pinned-manifest"}),
    "mcp_scope": frozenset({"none", "pinned-manifest"}),
    "permission_policy": frozenset({"deny-by-default"}),
    "sandbox_tool_policy": frozenset({"isolated", "synthetic-mock"}),
    "auto_update_state": frozenset({"pinned", "disabled"}),
}


@dataclass(frozen=True, slots=True)
class ExecutionProfile:
    """Pinned execution-profile record. String fields hold either an observed
    value or the honest sentinel ``UNAVAILABLE`` / ``UNKNOWN``."""

    profile_id: str
    runtime_version: str = UNKNOWN
    managed_settings_status: str = UNKNOWN
    user_settings_status: str = UNKNOWN
    project_settings_status: str = UNKNOWN
    local_settings_status: str = UNKNOWN
    claude_md_scopes: str = UNKNOWN
    auto_memory_state: str = UNKNOWN
    user_skill_scope: str = UNKNOWN
    project_skill_scope: str = UNKNOWN
    subagent_scope: str = UNKNOWN
    plugin_scope: str = UNKNOWN
    hook_scope: str = UNKNOWN
    mcp_scope: str = UNKNOWN
    permission_policy: str = UNKNOWN
    sandbox_tool_policy: str = UNKNOWN
    auto_update_state: str = UNKNOWN
    schema_version: str = SCHEMA_VERSION

    def validate(self) -> None:
        if not self.profile_id:
            raise ProfileError("profile_id required")
        for item in fields(self):
            value = getattr(self, item.name)
            if not isinstance(value, str) or value == "":
                raise ProfileError(
                    f"{item.name} must be a non-empty string (use the "
                    f"{UNAVAILABLE}/{UNKNOWN} sentinels, never a silent default)"
                )
        if self.schema_version != SCHEMA_VERSION:
            raise ProfileError(f"schema_version must be {SCHEMA_VERSION}")

    def unobserved_fields(self) -> tuple[str, ...]:
        return tuple(
            name
            for name in REQUIRED_FOR_BASELINE
            if getattr(self, name) in _SENTINELS
        )

    def baseline_ineligibility_reasons(self) -> tuple[str, ...]:
        reasons = [
            f"{name} is {getattr(self, name)}" for name in self.unobserved_fields()
        ]
        if (
            self.runtime_version not in _SENTINELS
            and _BASELINE_SAFE_RUNTIME_VERSION.fullmatch(self.runtime_version) is None
        ):
            reasons.append(
                f"runtime_version {self.runtime_version!r} is not an approved "
                "pinned synthetic runtime"
            )
        for name, allowed in _BASELINE_SAFE_VALUES.items():
            value = getattr(self, name)
            if value not in _SENTINELS and value not in allowed:
                reasons.append(
                    f"{name} {value!r} is not an approved isolated state"
                )
        return tuple(reasons)

    @property
    def baseline_eligible(self) -> bool:
        """Eligible only when every required value is observed AND isolated."""
        return not self.baseline_ineligibility_reasons()

    @property
    def profile_hash(self) -> str:
        return sha256_of_obj(self.to_dict(include_derived=False))

    def to_dict(self, include_derived: bool = True) -> dict[str, Any]:
        payload: dict[str, Any] = {
            item.name: getattr(self, item.name) for item in fields(self)
        }
        if include_derived:
            payload["baseline_eligible"] = self.baseline_eligible
            payload["baseline_ineligibility_reasons"] = list(
                self.baseline_ineligibility_reasons()
            )
            payload["execution_profile_hash"] = self.profile_hash
        return payload

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "ExecutionProfile":
        field_names = {item.name for item in fields(cls)}
        derived = {
            "baseline_eligible",
            "baseline_ineligibility_reasons",
            "execution_profile_hash",
        }
        unknown = set(payload) - field_names - derived
        if unknown:
            raise ProfileError(f"ExecutionProfile: unknown keys {sorted(unknown)}")
        profile = cls(**{k: v for k, v in payload.items() if k in field_names})
        profile.validate()
        # Finding A: supplied derived fields are NOT silently discarded — each
        # is compared against the authoritative recomputation and any mismatch
        # is rejected, so a serialized record cannot claim a false
        # baseline_eligible / reasons / hash.
        if "baseline_eligible" in payload and payload["baseline_eligible"] != profile.baseline_eligible:
            raise ProfileError(
                f"supplied baseline_eligible={payload['baseline_eligible']!r} does "
                f"not match the recomputed value {profile.baseline_eligible!r}"
            )
        if "baseline_ineligibility_reasons" in payload and list(
            payload["baseline_ineligibility_reasons"]
        ) != list(profile.baseline_ineligibility_reasons()):
            raise ProfileError(
                "supplied baseline_ineligibility_reasons do not match the "
                "recomputed reasons"
            )
        if "execution_profile_hash" in payload and payload[
            "execution_profile_hash"
        ] != profile.profile_hash:
            raise ProfileError(
                "supplied execution_profile_hash does not match the recomputed hash"
            )
        return profile


class RealClaudeCodeProfileSource:
    """The REAL host profile source for WP-2B-1: everything honestly unobserved.

    R5 (execution-profile observability/isolation) is INCOMPLETE/BLOCKED per
    the owner-accepted WP-2B-0 Outcome B. This source therefore reports every
    field UNAVAILABLE/UNKNOWN and never fabricates an observation; the
    resulting record is never baseline-eligible.
    """

    CAPABILITY = CapabilityState.UNAVAILABLE

    def capture(self) -> ExecutionProfile:
        profile = ExecutionProfile(
            profile_id="claude-code-real-host-wp2b1",
            runtime_version=UNKNOWN,
            managed_settings_status=UNAVAILABLE,
            user_settings_status=UNAVAILABLE,
            project_settings_status=UNAVAILABLE,
            local_settings_status=UNAVAILABLE,
            claude_md_scopes=UNAVAILABLE,
            auto_memory_state=UNKNOWN,
            user_skill_scope=UNAVAILABLE,
            project_skill_scope=UNAVAILABLE,
            subagent_scope=UNAVAILABLE,
            plugin_scope=UNKNOWN,
            hook_scope=UNKNOWN,
            mcp_scope=UNKNOWN,
            permission_policy=UNAVAILABLE,
            sandbox_tool_policy=UNAVAILABLE,
            auto_update_state=UNKNOWN,
        )
        profile.validate()
        return profile


def synthetic_isolated_profile(profile_id: str = "synthetic-isolated") -> ExecutionProfile:
    """A fully observed synthetic profile for deterministic offline tests."""
    profile = ExecutionProfile(
        profile_id=profile_id,
        runtime_version="synthetic-1.0",
        managed_settings_status="absent",
        user_settings_status="suppressed",
        project_settings_status="pinned",
        local_settings_status="absent",
        claude_md_scopes="project-only",
        auto_memory_state="disabled",
        user_skill_scope="suppressed",
        project_skill_scope="pinned-manifest",
        subagent_scope="none",
        plugin_scope="none",
        hook_scope="none",
        mcp_scope="none",
        permission_policy="deny-by-default",
        sandbox_tool_policy="synthetic-mock",
        auto_update_state="disabled",
    )
    profile.validate()
    return profile
