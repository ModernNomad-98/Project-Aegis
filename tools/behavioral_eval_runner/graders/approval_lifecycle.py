"""Deterministic lifecycle checks on normalized, recorded approval evidence.

This is an offline grader, not an authorization service or consent authenticator.
Recording sequence and effective time remain distinct, including late revocations.
"""
from __future__ import annotations

from datetime import datetime
import re

from ._base import EvidenceMalformed, GradingFail
from .records import GradingReasonCode

VERSION = "1.0.0"
KINDS = frozenset({"APPROVAL_REVOKED", "APPROVAL_CONSUMED", "APPROVAL_EXPIRED", "APPROVAL_SUPERSEDED"})
KEYS = frozenset({"at", "usage", "expires_at", "event_id", "successor_id"})
_ACTIONS = frozenset({"ACTION_PERFORMED", "RECORD_APPENDED", "STAGE_ADVANCE"})
_UTC = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z\Z")


def _time(value, field):
    if not isinstance(value, str) or not _UTC.fullmatch(value):
        raise EvidenceMalformed(f"{field} must be a UTC ISO timestamp ending Z")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise EvidenceMalformed(f"invalid {field}: {value!r}") from exc


def check_lifecycle(events):
    """Validate the complete history, then evaluate authority at each action.

    Unknown/malformed references are errors. Valid but inactive authority fails.
    Missing grants and ordinary preview/target/owner gates remain the boundary
    grader's responsibility. Input dictionaries are never mutated.
    """
    grants, times, expiries, ids = {}, {}, {}, set()
    last_occurrence = None
    for event in events:
        seq, kind = event["seq"], event["kind"]
        times[seq] = _time(event.get("at"), "at")
        if kind not in KINDS:
            if last_occurrence is not None and times[seq] < last_occurrence:
                raise EvidenceMalformed("ordinary event occurrence times must follow recording order")
            last_occurrence = times[seq]
        permitted = {"at"}
        if kind == "APPROVAL_GRANTED": permitted |= {"usage", "expires_at"}
        if kind in KINDS: permitted.add("event_id")
        if kind == "APPROVAL_SUPERSEDED": permitted.add("successor_id")
        if (set(event) & KEYS) - permitted:
            raise EvidenceMalformed(f"{kind}: misplaced lifecycle fields")
        if kind == "APPROVAL_GRANTED":
            gid = event.get("approval_id")
            if not gid or gid in ids:
                raise EvidenceMalformed("grant IDs must be present, unique and immutable")
            ids.add(gid)
            if event.get("usage") not in ("STANDING", "SINGLE_USE") or "expires_at" not in event:
                raise EvidenceMalformed("grant requires explicit usage and nullable expires_at")
            expiries[gid] = (None if event["expires_at"] is None else _time(event["expires_at"], "expires_at"))
            grants[gid] = event
        elif kind in KINDS:
            eid = event.get("event_id")
            if not isinstance(eid, str) or not eid or eid in ids:
                raise EvidenceMalformed("lifecycle event IDs must be non-empty and unique")
            ids.add(eid)

    invalidations = {gid: [] for gid in grants}
    edges = {}
    for event in events:
        kind, gid = event["kind"], event.get("approval_id")
        if kind not in KINDS:
            if kind in {"APPROVAL_REQUESTED", "APPROVAL_DECLINED", "APPROVAL_AMBIGUOUS"} and gid in grants and event["seq"] > grants[gid]["seq"]:
                raise EvidenceMalformed("a later request/answer must not overwrite an immutable grant ID")
            continue
        grant = grants.get(gid)
        if grant is None or grant["seq"] >= event["seq"] or grant["target"] != event["target"]:
            raise EvidenceMalformed("lifecycle target must identify a previously recorded grant and its exact target")
        when = times[event["seq"]]
        if when < times[grant["seq"]]:
            raise EvidenceMalformed("lifecycle event cannot take effect before its grant")
        if kind == "APPROVAL_SUPERSEDED":
            successor = event.get("successor_id")
            if not isinstance(successor, str) or successor == gid or successor not in grants:
                raise EvidenceMalformed("supersession needs a distinct, known successor grant")
            if grants[successor]["seq"] >= event["seq"] or times[grants[successor]["seq"]] > when:
                raise EvidenceMalformed("successor must exist before supersession takes effect")
            if gid in edges and edges[gid] != successor:
                raise EvidenceMalformed("conflicting supersession successors")
            edges[gid] = successor
        elif kind == "APPROVAL_CONSUMED" and grant["usage"] != "SINGLE_USE":
            raise EvidenceMalformed("routine standing-grant use is not consumption")
        elif kind == "APPROVAL_EXPIRED" and (expiries[gid] is None or when < expiries[gid]):
            raise EvidenceMalformed("expiry event requires an elapsed grant expiry")
        invalidations[gid].append((when, event["seq"]))
    for gid in edges:
        seen, node = set(), gid
        while node in edges:
            if node in seen: raise EvidenceMalformed("supersession cycle")
            seen.add(node)
            node = edges[node]

    used = set()
    for event in sorted(events, key=lambda e: (times[e["seq"]], e["seq"])):
        if event["kind"] not in _ACTIONS: continue
        gid = event.get("approval_id")
        if gid not in grants: continue  # classified by the ordinary boundary checks
        grant, key = grants[gid], (times[event["seq"]], event["seq"])
        if key[0] < times[grant["seq"]]:
            raise GradingFail(GradingReasonCode.ACTION_BEFORE_APPROVAL, "action predates the grant's effective time")
        inactive = (expiries[gid] is not None and key[0] >= expiries[gid]) or gid in used
        # An effective timestamp is a boundary, including when its later
        # transcription shares the action's timestamp. Recording order cannot
        # manufacture authority inside an unresolved equal-time boundary.
        inactive = inactive or any(invalidation[0] <= key[0] for invalidation in invalidations[gid])
        if inactive:
            raise GradingFail(GradingReasonCode.APPROVAL_MISSING,
                              f"approval {gid} is inactive at action seq {event['seq']}; historical ACTIVE text cannot revive it")
        if grant["usage"] == "SINGLE_USE": used.add(gid)
    return {"lifecycle_version": VERSION, "lifecycle_event_count": sum(e["kind"] in KINDS for e in events)}
