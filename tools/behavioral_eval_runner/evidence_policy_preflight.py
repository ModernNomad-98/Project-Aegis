"""Synthetic-only evidence-host preflight; never inspects a host.

Every fact is supplied by the caller.  Even complete, consistent assertions
produce only SIMULATION_ONLY, never an attestation or permission to run.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath, PureWindowsPath
from typing import TypeAlias


Claim: TypeAlias = bool | None | tuple[bool | None, ...]


@dataclass(frozen=True, slots=True)
class SyntheticHostFacts:
    """Caller assertions about one proposed evidence root, without probing it.

    A tuple records multiple caller assertions about one property. Disagreement
    stops the preflight; a lone true assertion is only a simulation input.
    """

    expected_path: str | None = None
    asserted_path: str | None = None
    path_owned: Claim = None
    acl_restricted: Claim = None
    inheritance_disabled: Claim = None
    encryption_enabled: Claim = None
    recovery_key_custody_confirmed: Claim = None


@dataclass(frozen=True, slots=True)
class SyntheticPreflightResult:
    status: str
    reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, str | list[str]]:
        """Return a sanitized record without paths, principals or key details."""
        return {"status": self.status, "reasons": list(self.reasons)}


def _claim_problem(name: str, claim: object) -> str | None:
    values = claim if isinstance(claim, tuple) else (claim,)
    if not values or any(value is None for value in values):
        return f"{name}_UNKNOWN"
    if any(type(value) is not bool for value in values):
        return f"{name}_INVALID"
    if len(set(values)) > 1:
        return f"{name}_CONFLICT"
    if values[0] is False:
        return f"{name}_FALSE"
    return None


def _normalized_absolute_path(value: object) -> bool:
    """Check spelling only; PurePath never queries a filesystem or resolves links."""
    if not isinstance(value, str) or not value or "\x00" in value:
        return False
    if value.startswith("/") and not value.startswith("//") and "\\" not in value:
        path = PurePosixPath(value)
    else:
        path = PureWindowsPath(value)
        # A drive-rooted local path has unambiguous lexical Windows spelling.
        if len(path.drive) != 2 or not path.drive.endswith(":"):
            return False
    return (
        path.is_absolute()
        and str(path) == value
        and len(path.parts) > 1  # an evidence root cannot be a volume root
        and all(part not in (".", "..") and not part.endswith((".", " "))
                for part in path.parts[1:])
    )


def evaluate_synthetic_host_facts(facts: SyntheticHostFacts) -> SyntheticPreflightResult:
    """Evaluate supplied assertions only; STOP on every unresolved condition.

    This function has no filesystem, operating-system, credential, provider or
    network calls. A simulated success grants no real-host authority.
    """
    if not isinstance(facts, SyntheticHostFacts):
        return SyntheticPreflightResult("STOP", ("FACTS_INVALID",))

    reasons: list[str] = []
    if not facts.expected_path or not facts.asserted_path:
        reasons.append("EXACT_PATH_UNKNOWN")
    elif not (_normalized_absolute_path(facts.expected_path)
              and _normalized_absolute_path(facts.asserted_path)):
        reasons.append("EXACT_PATH_INVALID")
    elif facts.expected_path != facts.asserted_path:
        reasons.append("EXACT_PATH_CONFLICT")

    for name, claim in (
        ("OWNERSHIP", facts.path_owned),
        ("ACL", facts.acl_restricted),
        ("INHERITANCE", facts.inheritance_disabled),
        ("ENCRYPTION", facts.encryption_enabled),
        ("RECOVERY_KEY", facts.recovery_key_custody_confirmed),
    ):
        problem = _claim_problem(name, claim)
        if problem is not None:
            reasons.append(problem)

    if reasons:
        return SyntheticPreflightResult("STOP", tuple(reasons))
    return SyntheticPreflightResult("SIMULATION_ONLY", ())
