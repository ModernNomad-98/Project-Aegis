"""Versioned, bounded offline advice. No dispatch, network, or host integration."""

from __future__ import annotations

from dataclasses import dataclass
import json
import re
from typing import Any, Mapping


VERSION = "1"
MAX_REQUEST_BYTES = 4096
MAX_RESPONSE_BYTES = 1024
MAX_ITEMS = 16
ID = re.compile(r"[a-z][a-z0-9-]{0,63}\Z")
VERSION_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}\Z")
STAGES = frozenset({"discovery", "design", "implementation", "review", "release"})


class ContractError(ValueError):
    """Malformed or unsafe contract input."""


def _pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        if key in result:
            raise ContractError("duplicate JSON key")
        result[key] = value
    return result


def _decode(value: bytes | str | Mapping[str, Any], limit: int) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        try:
            encoded = json.dumps(value, ensure_ascii=False, allow_nan=False).encode("utf-8")
        except (TypeError, ValueError, UnicodeError) as exc:
            raise ContractError("unencodable object") from exc
    elif isinstance(value, str):
        try:
            encoded = value.encode("utf-8", errors="strict")
        except UnicodeError as exc:
            raise ContractError("invalid Unicode") from exc
    elif isinstance(value, bytes):
        encoded = value
    else:
        raise ContractError("expected JSON object")
    if len(encoded) > limit:
        raise ContractError("byte limit exceeded")
    try:
        decoded = json.loads(encoded, object_pairs_hook=_pairs,
                             parse_constant=lambda _: (_ for _ in ()).throw(ContractError("nonfinite number")))
    except (ValueError, UnicodeError) as exc:
        raise ContractError("invalid JSON") from exc
    if not isinstance(decoded, dict):
        raise ContractError("expected JSON object")
    return decoded


def _keys(value: Mapping[str, Any], expected: set[str]) -> None:
    if set(value) != expected:
        raise ContractError("unexpected or missing fields")


def _string(value: Any, limit: int, pattern: re.Pattern[str] | None = None) -> str:
    if not isinstance(value, str) or not 1 <= len(value) <= limit:
        raise ContractError("invalid string")
    try:
        value.encode("utf-8", errors="strict")
    except UnicodeError as exc:
        raise ContractError("invalid Unicode") from exc
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in value):
        raise ContractError("control character")
    if pattern is not None and pattern.fullmatch(value) is None:
        raise ContractError("invalid identifier")
    return value


def _ids(value: Any, offered: set[str] | None = None) -> tuple[str, ...]:
    if not isinstance(value, list) or len(value) > MAX_ITEMS:
        raise ContractError("invalid ID list")
    ids = tuple(_string(item, 64, ID) for item in value)
    if len(set(ids)) != len(ids):
        raise ContractError("duplicate ID")
    if offered is not None and not set(ids) <= offered:
        raise ContractError("ID not offered")
    return ids


@dataclass(frozen=True)
class Offer:
    id: str
    description: str
    read_only: bool = False
    manual_only: bool = False


@dataclass(frozen=True)
class Request:
    version: str
    synopsis: str
    stage: str
    catalog_version: str
    policy_version: str
    agents: tuple[Offer, ...]
    skills: tuple[Offer, ...]
    mandatory_agents: tuple[str, ...]
    mandatory_skills: tuple[str, ...]
    selected_agents: tuple[str, ...]
    selected_skills: tuple[str, ...]
    invoked_manual_skills: tuple[str, ...]


def parse_request(raw: bytes | str | Mapping[str, Any]) -> Request:
    """Validate a minimized host-supplied offer. Raises before adapter use."""
    data = _decode(raw, MAX_REQUEST_BYTES)
    _keys(data, {"version", "synopsis", "stage", "catalog_version", "policy_version",
                 "agents", "skills", "mandatory_agents", "mandatory_skills",
                 "selected_agents", "selected_skills", "invoked_manual_skills"})
    if data["version"] != VERSION:
        raise ContractError("unsupported contract version")
    synopsis = _string(data["synopsis"], 512)
    if any(ch in synopsis for ch in "\u0085\u2028\u2029"):
        raise ContractError("synopsis must be one line")
    # A short synopsis is the only free-text task field. Refuse common structured
    # data and destination forms rather than forwarding raw content to an adapter.
    if re.search(r"https?://|(?:[A-Za-z]:\\|/[^ ]+/)|\b(?:api[_-]?key|password|secret|token)\s*[:=]",
                 synopsis, re.IGNORECASE):
        raise ContractError("synopsis contains prohibited data shape")
    stage = _string(data["stage"], 32)
    if stage not in STAGES:
        raise ContractError("unknown stage")
    versions = (_string(data[name], 64, VERSION_ID) for name in ("catalog_version", "policy_version"))
    catalog_version, policy_version = versions

    def offers(value: Any, kind: str) -> tuple[Offer, ...]:
        if not isinstance(value, list) or len(value) > MAX_ITEMS:
            raise ContractError("invalid offers")
        result = []
        for item in value:
            if not isinstance(item, dict):
                raise ContractError("invalid offer")
            expected = {"id", "description", "read_only"} if kind == "agent" else {"id", "description", "manual_only"}
            _keys(item, expected)
            flag = item["read_only" if kind == "agent" else "manual_only"]
            if type(flag) is not bool:
                raise ContractError("invalid offer flag")
            result.append(Offer(_string(item["id"], 64, ID), _string(item["description"], 120),
                                read_only=flag if kind == "agent" else False,
                                manual_only=flag if kind == "skill" else False))
        if len({offer.id for offer in result}) != len(result):
            raise ContractError("duplicate offer ID")
        return tuple(result)

    agents = offers(data["agents"], "agent")
    skills = offers(data["skills"], "skill")
    agent_ids = {offer.id for offer in agents}
    skill_ids = {offer.id for offer in skills}
    mandatory_agents = _ids(data["mandatory_agents"], agent_ids)
    mandatory_skills = _ids(data["mandatory_skills"], skill_ids)
    selected_agents = _ids(data["selected_agents"], agent_ids)
    selected_skills = _ids(data["selected_skills"], skill_ids)
    invoked = _ids(data["invoked_manual_skills"], skill_ids)
    manual_ids = {offer.id for offer in skills if offer.manual_only}
    if not set(invoked) <= set(selected_skills) & manual_ids:
        raise ContractError("manual invocation must be an explicit selection")
    if (set(mandatory_skills) | set(selected_skills)) & manual_ids - set(invoked):
        raise ContractError("manual-only skill lacks invocation")
    return Request(VERSION, synopsis, stage, catalog_version, policy_version,
                   agents, skills, mandatory_agents, mandatory_skills,
                   selected_agents, selected_skills, invoked)


@dataclass(frozen=True)
class Decision:
    disposition: str  # recommend, abstain, timeout, invalid, unavailable
    agents: tuple[str, ...] = ()
    skills: tuple[str, ...] = ()
    score: float | None = None  # uncalibrated, never authorization
    reason: str = ""


def decide(request: Request, raw: bytes | str | Mapping[str, Any] | None = None,
           *, failure: str | None = None) -> Decision:
    """Validate untrusted advice. All failures carry empty selections."""
    if failure is not None:
        if failure not in {"timeout", "unavailable"}:
            return Decision("invalid", reason="unknown adapter failure")
        return Decision(failure, reason="adapter failure")
    try:
        data = _decode(raw, MAX_RESPONSE_BYTES)  # type: ignore[arg-type]
        required = {"version", "catalog_version", "policy_version", "status", "agents", "skills"}
        if not required <= set(data) or set(data) - required - {"score"}:
            raise ContractError("unexpected or missing fields")
        if data["version"] != VERSION or data["catalog_version"] != request.catalog_version or data["policy_version"] != request.policy_version:
            raise ContractError("stale or malformed version")
        if data["status"] not in ("recommend", "abstain"):
            raise ContractError("invalid status")
        agents = _ids(data["agents"], {offer.id for offer in request.agents})
        skills = _ids(data["skills"], {offer.id for offer in request.skills})
        score = data.get("score")
        if score is not None and (type(score) not in (int, float) or not 0 <= score <= 1):
            raise ContractError("invalid score")
        if data["status"] == "abstain":
            if agents or skills or score is not None:
                raise ContractError("abstain carries selections")
            return Decision("abstain")
        if not agents and not skills:
            raise ContractError("empty recommendation")
        if not set(request.mandatory_agents + request.selected_agents) <= set(agents):
            raise ContractError("missing mandatory or explicit agent")
        if not set(request.mandatory_skills + request.selected_skills) <= set(skills):
            raise ContractError("missing mandatory or explicit skill")
        manual = {offer.id for offer in request.skills if offer.manual_only}
        if set(skills) & manual - set(request.invoked_manual_skills):
            raise ContractError("manual-only skill not invoked")
        return Decision("recommend", agents, skills, float(score) if score is not None else None)
    except (ContractError, TypeError, ValueError) as exc:
        return Decision("invalid", reason=str(exc))


@dataclass(frozen=True)
class Compatibility:
    status: str  # compatible, unsupported, unknown
    reasons: tuple[str, ...]


def check_compatibility(facts: Mapping[str, Any], request: Request) -> Compatibility:
    """Check supplied synthetic facts only; never probes an actual host."""
    required = {"contract_version", "catalog_version", "policy_version", "agent_ids", "skill_ids"}
    if not isinstance(facts, Mapping) or set(facts) != required:
        return Compatibility("unknown", ("missing or contradictory facts",))
    try:
        if not all(isinstance(facts[key], str) and VERSION_ID.fullmatch(facts[key])
                   for key in ("contract_version", "catalog_version", "policy_version")):
            raise ContractError("malformed version facts")
        for key in ("agent_ids", "skill_ids"):
            _ids(facts[key])
    except ContractError:
        return Compatibility("unknown", ("malformed catalog facts",))
    reasons = []
    if facts["contract_version"] != VERSION:
        reasons.append("unsupported contract version")
    if facts["catalog_version"] != request.catalog_version:
        reasons.append("stale catalog version")
    if facts["policy_version"] != request.policy_version:
        reasons.append("stale policy version")
    if not {offer.id for offer in request.agents} <= set(facts["agent_ids"]):
        reasons.append("offered agent absent from installed catalog")
    if not {offer.id for offer in request.skills} <= set(facts["skill_ids"]):
        reasons.append("offered skill absent from installed catalog")
    return Compatibility("unsupported", tuple(reasons)) if reasons else Compatibility("compatible", ())


class FakeAdapter:
    """Single scripted local response; no IO and no implicit fallback."""

    def __init__(self, response: Any = None, *, failure: str | None = None):
        self.response = response
        self.failure = failure

    def advise(self, request: Request) -> Decision:
        return decide(request, self.response, failure=self.failure)
