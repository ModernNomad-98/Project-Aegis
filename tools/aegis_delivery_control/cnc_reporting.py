"""Portable, stdlib-only local C&C evidence projection. Never authorizes actions.

Narrow Python adaptation of cnc-adapter.mjs, SHA256
ad02d1955526041d3b6e703265bc22ad707ed8f1a4979e3f977de59606f91478.
Source: retained reconciliation-v2 portable helper (2026-11-03 capture).
Intentional corrections: a foreign grant is rejected before a missing locator;
expired, revoked and consumed grants route to new authority even when the
original or locator is missing; every authority route carries the profile's
policy locator; a null finding is unknown, never "no finding"; a material
finding without matching evidence or primary detail stays unresolved; all
finding adjudication remains native. Inputs are caller claims, never
authenticated here. CLI output is one LF-terminated JSON object written as
bytes.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import math
import os
import re
import stat
import sys

CONTRACT_SHA256 = "1b2469b3f663d9b04712c4dbbdb997fdfdc0c6a28727c5647c954854850a3268"
CONTRACT_ID = "cnc-evidence-contract-v2"
ERRORS = {
    "CLI_INVALID": (2, "Invalid command arguments."),
    "INPUT_INVALID": (2, "Input is not valid for this report contract."),
    "PROFILE_INVALID": (2, "Profile is not valid for this report contract."),
    "CONTRACT_INVALID": (2, "Contract is not supported."),
    "IDENTITY_MISMATCH": (2, "Repository identities do not match."),
    "INPUT_UNAVAILABLE": (3, "An explicitly selected input is unavailable."),
    "PROFILE_UNAVAILABLE": (3, "The explicitly selected profile is unavailable."),
    "CONTRACT_UNAVAILABLE": (3, "The explicitly selected contract is unavailable."),
    "REPORT_FAILED": (3, "Report could not be produced."),
}
_BAD_CHARS = re.compile(r"[\x00-\x1f\x7f-\x9f\u061c\u200e-\u200f\u2028-\u202e\u2066-\u2069\ud800-\udfff]")
_SECRETS = [
    re.compile(r"(?:ghp_|gho_|ghu_|ghs_|ghr_|github_pat_|sk-proj-|sk-ant-|AKIA|ASIA)"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----", re.I),
    re.compile(r"\bBearer\s+\S+", re.I),
    re.compile(r"[A-Za-z][A-Za-z0-9+.-]*://[^/@\s]+:[^/@\s]+@", re.I),
    re.compile(r"[?&](?:token|id[_-]?token|access[_-]?token|refresh[_-]?token|auth[_-]?token|secret|client[_-]?secret|private[_-]?key|secret[_-]?key|password|passwd|pwd|api[_-]?key|access[_-]?key|credential|authorization|signature|sig|session(?:[_-]?id)?)=[^&#\s]+", re.I),
]


class ReportError(Exception):
    """Fixed non-echoing report refusal; never carries input contents."""
    def __init__(self, code):
        self.code = code
        super().__init__(ERRORS[code][1])


def _require(condition):
    if not condition:
        raise ValueError("invalid")


def _obj(value, keys):
    _require(type(value) is dict and set(value) == set(keys.split()))


def _text(value, limit=4096):
    _require(type(value) is str and bool(value.strip()) and len(value) <= limit)


def _identifier(value):
    _text(value, 128)


def _bool(value):
    _require(type(value) is bool)


def _number(value):
    _require(type(value) in (int, float) and 0 <= value <= 1000000000000 and math.isfinite(value))


def _count(value):
    _require(type(value) is int)
    _number(value)


def _enum(value, options):
    _require(type(value) is str and value in options.split())


_TIMESTAMP = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?Z")


def _time(value):
    # ASCII digits only: Unicode decimal digits must not satisfy the contract.
    _require(type(value) is str and _TIMESTAMP.fullmatch(value))
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _hash(value, length):
    _require(type(value) is str and re.fullmatch("[0-9a-f]{"+str(length)+"}", value))


def _maybe(value, validator):
    _obj(value, "value unknown_reason")
    if value["value"] is None:
        _text(value["unknown_reason"])
    else:
        _require(value["unknown_reason"] is None)
        validator(value["value"])


def _texts(value, limit=1000, nonempty=False):
    _require(type(value) is list and len(value) <= limit and (not nonempty or bool(value)))
    for entry in value:
        _text(entry)


def _scan_depth(text):
    depth = 0
    quoted = escaped = False
    for char in text:
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char in "[{":
            depth += 1
            _require(depth <= 16)
        elif char in "]}":
            depth -= 1
            _require(depth >= 0)


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result)
        result[key] = value
    return result


def _constant(_value):
    raise ValueError("invalid")


def _walk(value, depth=0):
    _require(depth <= 16)
    if type(value) is str:
        _text(value)
        _require(not _BAD_CHARS.search(value) and not any(p.search(value) for p in _SECRETS))
    elif type(value) is dict:
        for key, child in value.items():
            _walk(key, depth + 1)
            _walk(child, depth + 1)
    elif type(value) is list:
        _require(len(value) <= 1000)
        for child in value:
            _walk(child, depth + 1)
    elif type(value) in (float, int):
        _require(math.isfinite(value))
    else:
        _require(value is None or type(value) is bool)


def _read(path, maximum, invalid_code, unavailable_code):
    """One explicit regular descriptor, bounded read, no final symlink following.

    Availability failures carry the code of the document being read, so a broken
    profile or contract installation is not reported as an unavailable capture.

    This is not protection against a hostile actor racing parent directories.
    Cloud/network-backed mounts cannot be identified portably by this helper.
    """
    try:
        path_text = os.fspath(path)
        if (type(path_text) is not str or path_text == "-" or
                path_text.startswith(("\\\\", "//")) or
                re.match(r"^[A-Za-z][A-Za-z0-9+.-]*://", path_text)):
            raise ReportError(unavailable_code)
        before = os.lstat(path_text)
        if not stat.S_ISREG(before.st_mode) or stat.S_ISLNK(before.st_mode):
            raise ReportError(unavailable_code)
        flags = (os.O_RDONLY | getattr(os, "O_BINARY", 0) |
                 getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))
        descriptor = os.open(path_text, flags)
        with os.fdopen(descriptor, "rb") as stream:
            actual = os.fstat(stream.fileno())
            if (not stat.S_ISREG(actual.st_mode) or
                    (before.st_dev, before.st_ino) != (actual.st_dev, actual.st_ino)):
                raise ReportError(unavailable_code)
            raw = stream.read(maximum + 1)
    except ReportError:
        raise
    except (OSError, TypeError, ValueError):
        raise ReportError(unavailable_code) from None
    try:
        _require(len(raw) <= maximum)
        text = raw.decode("utf-8", errors="strict")
        _require(not text.startswith("\ufeff"))
        _scan_depth(text)
        value = json.loads(text, object_pairs_hook=_pairs, parse_constant=_constant)
        _require(type(value) is dict)
        _walk(value)
        return value, hashlib.sha256(raw).hexdigest()
    except (ValueError, TypeError, UnicodeError, RecursionError, OverflowError):
        raise ReportError(invalid_code) from None


def _finding(value):
    _obj(value, "status evidence primary applicable_acceptance_verified_reported")
    _identifier(value["status"])
    _maybe(value["evidence"], _text)
    _maybe(value["primary"], _text)
    _bool(value["applicable_acceptance_verified_reported"])


def _input(value):
    _obj(value, "schema_version repository_id native_record candidate collection items metrics")
    _require(type(value["schema_version"]) is int and value["schema_version"] == 1)
    _identifier(value["repository_id"])
    _obj(value["native_record"], "locator revision")
    for entry in value["native_record"].values():
        _text(entry)
    _obj(value["candidate"], "head base tree plan_sha256")
    for key, entry in value["candidate"].items():
        _maybe(entry, lambda v: _hash(v, 64 if key == "plan_sha256" else 40))
    collection = value["collection"]
    _obj(collection, "kind paused manual_task_authorized_reported inbox_total positions complete")
    _enum(collection["kind"], "manual heartbeat")
    for key in ("paused", "manual_task_authorized_reported", "complete"):
        _bool(collection[key])
    _require(collection["complete"] is False)
    _maybe(collection["inbox_total"], _count)
    positions = collection["positions"]
    _require(type(positions) is list and len(positions) <= 6)
    for position in positions:
        _count(position)
    total = collection["inbox_total"]["value"]
    expected = [] if total is None else list(range(max(1, total-5), total+1))
    _require(positions == expected)
    items = value["items"]
    _require(type(items) is list and len(items) <= 1000)
    seen = set()
    for item in items:
        _obj(item, "event_id task description evidence_label progress scope responsible_actor source_locator source_sha256 retrieved_at first_observed_at authority dependencies_and_holds owner_notification_delivery_evidence coordinator_answer execution_evidence accepted_completion_scope next_action next_check_or_due_reason change finding")
        _identifier(item["event_id"])
        _require(item["event_id"] not in seen)
        seen.add(item["event_id"])
        _identifier(item["task"])
        for key in ("description", "scope", "responsible_actor", "source_locator", "next_action", "next_check_or_due_reason"):
            _text(item[key])
        _enum(item["evidence_label"], "Observed Reported Inferred Planned UNRUN Unknown Historical")
        _enum(item["progress"], "acknowledgment substantive_answer execution_milestone accepted_completion")
        _maybe(item["source_sha256"], lambda v: _hash(v, 64))
        _time(item["retrieved_at"])
        _maybe(item["first_observed_at"], _time)
        for key in ("owner_notification_delivery_evidence", "coordinator_answer", "accepted_completion_scope"):
            _maybe(item[key], _text)
        _texts(item["dependencies_and_holds"])
        _texts(item["execution_evidence"], 100)
        if item["progress"] == "accepted_completion":
            _require(item["source_sha256"]["value"] is not None and
                     bool(item["execution_evidence"]) and item["accepted_completion_scope"]["value"] is not None)
        authority = item["authority"]
        _obj(authority, "repository scope original_verified_reported lifecycle conditions_satisfied_reported source_locator")
        _identifier(authority["repository"])
        _text(authority["scope"])
        _bool(authority["original_verified_reported"])
        _bool(authority["conditions_satisfied_reported"])
        _enum(authority["lifecycle"], "unknown active expired revoked consumed")
        _maybe(authority["source_locator"], _text)
        change = item["change"]
        _obj(change, "kind changes_head changes_scope material_finding consumed_by_check")
        _enum(change["kind"], "receipt_only other")
        for key in ("changes_head", "changes_scope", "material_finding", "consumed_by_check"):
            _bool(change[key])
        _maybe(item["finding"], _finding)
    metrics = value["metrics"]
    _obj(metrics, "unit explicit_start explicit_finish first_observation last_observation active_effort_seconds comparable_reported baseline_elapsed_seconds current_elapsed_seconds baseline_attributed_cost current_attributed_cost attributable_benefit incremental_cost cost_provenance")
    _enum(metrics["unit"], "artifact_review accepted_product_delivery")
    _bool(metrics["comparable_reported"])
    for key in ("explicit_start", "explicit_finish", "first_observation", "last_observation"):
        _maybe(metrics[key], _time)
    for key in ("active_effort_seconds", "baseline_elapsed_seconds", "current_elapsed_seconds", "baseline_attributed_cost", "current_attributed_cost", "attributable_benefit", "incremental_cost"):
        _maybe(metrics[key], _number)
    _maybe(metrics["cost_provenance"], _text)


_PROFILE_ID = re.compile(r"[a-z][a-z0-9_-]{0,63}")


def _profile(value):
    _obj(value, "schema_version id repository contract_id native_record_locator native_policy_revision native_references stage_labels authority_policy_locator head_policy_locator receipt_policy_locator finding_policy_locator role_boundary activation adoption_receipt")
    _require(type(value["schema_version"]) is int and value["schema_version"] == 1)
    # Consumer profiles are portable: any lowercase slug identifies one, and
    # only the Aegis profile pins the source stage labels A-G below.
    _require(type(value["id"]) is str and _PROFILE_ID.fullmatch(value["id"]))
    _identifier(value["repository"])
    _require(value["contract_id"] == CONTRACT_ID)
    for key in ("native_record_locator", "native_policy_revision", "authority_policy_locator", "head_policy_locator", "receipt_policy_locator", "finding_policy_locator", "role_boundary"):
        _text(value[key])
    _texts(value["native_references"], 100, True)
    labels = value["stage_labels"]
    _require(type(labels) is list and 0 < len(labels) <= 1000)
    ids = []
    for label in labels:
        _obj(label, "id label")
        _identifier(label["id"])
        _text(label["label"])
        ids.append(label["id"])
    _require(len(ids) == len(set(ids)))
    if value["id"] == "aegis":
        _require(ids == list("ABCDEFG"))
    _enum(value["activation"], "candidate adopted_with_receipt")
    _maybe(value["adoption_receipt"], _text)
    if value["activation"] == "adopted_with_receipt":
        _require(value["adoption_receipt"]["value"] is not None)


def _authority_route(item, profile):
    """Route one reported grant; a missing original stays a gap, not proof.

    The repository is compared first, so a grant issued elsewhere is never
    described as an authority this project may locate and reuse. Expired,
    revoked and consumed grants are terminal and are decided before a missing
    original or locator: locating cannot restore a non-reusable lifecycle, so
    only a new authority decision can help. A missing original or locator is
    otherwise a reconciliation gap. An unknown lifecycle stays a reconciliation
    route because neither state is established. Every route carries the
    profile's authority policy locator. No supplied input establishes that the
    owner withheld permission, so "ownerWithheld" remains unknown rather than an
    affirmative claim.
    """
    a = item["authority"]
    if a["repository"] != profile["repository"]:
        route = "FOREIGN_GRANT_REJECTED"
    elif a["lifecycle"] in ("expired", "revoked", "consumed"):
        route = "NON_REUSABLE_GRANT_NEW_AUTHORITY_REQUIRED"
    elif not a["original_verified_reported"] or a["source_locator"]["value"] is None:
        route = "LOCATE_ORIGINAL_AUTHORITY"
    elif a["lifecycle"] != "active" or not a["conditions_satisfied_reported"] or a["scope"] != item["scope"]:
        route = "RECONCILE_EXACT_SCOPE_OR_CONDITIONS"
    else:
        route = "REUSE_VERIFIED_APPLICABLE_GRANT"
    return {"route": route, "policy": profile["authority_policy_locator"],
            "grantsNewExecutionAuthority": False, "ownerWithheld": None}


_AUTHORITY_GAP_REASONS = {
    "FOREIGN_GRANT_REJECTED":
        "the reported grant is from another repository and cannot be reused",
    "NON_REUSABLE_GRANT_NEW_AUTHORITY_REQUIRED":
        "the reported grant is expired, revoked or consumed",
    "LOCATE_ORIGINAL_AUTHORITY":
        "the original grant or locator is not verified",
    "RECONCILE_EXACT_SCOPE_OR_CONDITIONS":
        "the grant scope or conditions do not match, or its lifecycle is unknown",
}


def _authority_gap(event_id, route):
    """One consolidated authority-reconciliation gap for a non-reuse route."""
    return ("Authority for event " + event_id + ": " + route + "; " +
            _AUTHORITY_GAP_REASONS[route] + ".")


def _finding_route(item, profile):
    """Route one finding assessment without inferring absence from a null.

    The schema uses null only for an unknown value with a nonempty reason, so a
    null finding is unknown, never proof that no finding exists. The three
    states are explicit: a supplied record is "reported"; a caller that has
    positively assessed the change as having no finding supplies a record whose
    status is "none"; a null value is "unknown". A material finding reported
    without matching details is unresolved and routes to native disposition
    instead of "NO_FINDING". For a material finding, a non-"none" record also
    needs at least one evidence or primary detail; a status alone is not matching
    detail. Non-material supplied records remain reported assessments for native
    disposition.
    """
    value = item["finding"]["value"]
    policy = profile["finding_policy_locator"]
    absent = value is None
    declared_none = not absent and value["status"].strip().casefold() == "none"
    has_detail = (not absent and not declared_none and
                  (value["evidence"]["value"] is not None or
                   value["primary"]["value"] is not None))
    if item["change"]["material_finding"] and (absent or declared_none or not has_detail):
        state, route = "unresolved_material", "UNRESOLVED_NATIVE_DISPOSITION"
        if absent:
            gap = "A material finding is reported without finding details; native disposition is unresolved."
        elif declared_none:
            gap = "A material finding is reported while the supplied finding record declares none; native disposition is unresolved."
        else:
            gap = "A material finding is reported without an evidence or primary detail; native disposition is unresolved."
    elif absent:
        state, route = "unknown", "UNKNOWN_FINDING_NATIVE_DISPOSITION"
        gap = "The finding value is unknown; absence is not proof that no finding exists."
    elif declared_none:
        state, route, gap = "none", "NO_FINDING", None
    else:
        state, route, gap = "reported", "NATIVE_DISPOSITION_POLICY", None
    return {"state": state, "route": route, "policy": policy,
            "closed": False, "evidenceGap": gap}


def _routes(item, profile):
    change = item["change"]
    if any(change[key] for key in ("changes_head", "changes_scope", "material_finding", "consumed_by_check")):
        change_route, policy = "NATIVE_POLICY_ASSESSMENT", profile["head_policy_locator"]
    elif change["kind"] == "receipt_only":
        change_route, policy = "RECEIPT_READBACK_AND_NATIVE_RECEIPT_CHECKS", profile["receipt_policy_locator"]
    else:
        change_route, policy = "IDENTIFY_CHANGED_INPUTS", profile["head_policy_locator"]
    return {
        "authority": _authority_route(item, profile),
        "change": {"route": change_route, "policy": policy,
                   "automaticFullRerun": False, "clearsNativeGates": False},
        "finding": _finding_route(item, profile),
    }


def _metrics(metrics):
    def value(key):
        return metrics[key]["value"]
    reasons = []
    provenance = value("cost_provenance")
    explicit = value("explicit_start") is not None and value("explicit_finish") is not None
    first, last = (value("explicit_start"), value("explicit_finish")) if explicit else (value("first_observation"), value("last_observation"))
    wall = None
    basis = "Unknown"
    if first is not None and last is not None:
        seconds = (_time(last) - _time(first)).total_seconds()
        if seconds >= 0:
            wall, basis = seconds, "explicit_review_wall_window" if explicit else "observation_span_lower_bound"
        else:
            reasons.append("Reverse wall interval; wall seconds unknown.")
    else:
        reasons.append("Missing complete time interval; wall seconds unknown.")
    speed = savings = roi = None
    if not metrics["comparable_reported"]:
        reasons.append("No reported matched comparison; speed, savings and ROI unknown.")
    else:
        baseline, current = value("baseline_elapsed_seconds"), value("current_elapsed_seconds")
        if baseline is not None and baseline > 0 and current is not None:
            speed = (baseline-current)/baseline
        else:
            reasons.append("Missing or zero baseline elapsed comparison; speed unknown.")
        if provenance is not None:
            baseline_cost, current_cost = value("baseline_attributed_cost"), value("current_attributed_cost")
            if baseline_cost is not None and current_cost is not None:
                savings = baseline_cost-current_cost
            else:
                reasons.append("Missing attributed costs; savings unknown.")
            benefit, cost = value("attributable_benefit"), value("incremental_cost")
            if benefit is not None and cost is not None and cost > 0:
                roi = (benefit-cost)/cost
            else:
                reasons.append("Missing benefit or nonpositive incremental cost; ROI unknown.")
    # Finite input bounds do not prevent floating-point division overflow.
    computed = [speed, savings, roi]
    for i, number in enumerate(computed):
        if number is not None and not math.isfinite(number):
            computed[i] = None
            reasons.append("Nonfinite comparison result; value unknown.")
    if provenance is None:
        # One reason only: the specific unknown reason, with the affected
        # comparison named when a reported matched comparison exists.
        reason = ("Cost provenance unknown: " +
                  metrics["cost_provenance"]["unknown_reason"])
        if metrics["comparable_reported"]:
            reason += " Savings and ROI unknown."
        reasons.append(reason)
    if value("active_effort_seconds") is None:
        reasons.append("Active effort not measured: " + metrics["active_effort_seconds"]["unknown_reason"])
    return {"unit":metrics["unit"], "wall_seconds":wall, "wall_basis":basis,
            "active_effort_seconds":value("active_effort_seconds"),
            "speed_improvement":computed[0], "cost_savings":computed[1], "roi":computed[2],
            "reasons":reasons, "comparison_basis":"reported_inputs" if any(x is not None for x in computed) else "unknown",
            "cost_provenance":provenance}


def report_from_paths(repository_id, input_path, profile_path, contract_path,
                      expected_repository_id=None,
                      expected_profile_sha256=None):
    """Validate selected local documents in deterministic order, then project.

    All authority, completion and monetary claims remain caller-reported.
    No sibling discovery, environment input, fetch, database or output write.
    The optional expected_repository_id is the source wrapper's fixed identity;
    it is checked in the identity step, after input, profile and contract
    validation and before any projection work. The optional
    expected_profile_sha256 is the source wrapper's byte pin for its fixed
    adapter; a mismatch is PROFILE_INVALID during profile validation.
    """
    data, input_hash = _read(input_path, 1048576, "INPUT_INVALID", "INPUT_UNAVAILABLE")
    try:
        _input(data)
    except (ValueError, TypeError, KeyError, RecursionError, OverflowError):
        raise ReportError("INPUT_INVALID") from None
    profile, profile_hash = _read(profile_path, 65536, "PROFILE_INVALID", "PROFILE_UNAVAILABLE")
    try:
        _profile(profile)
    except (ValueError, TypeError, KeyError, RecursionError, OverflowError):
        raise ReportError("PROFILE_INVALID") from None
    if expected_profile_sha256 is not None and profile_hash != expected_profile_sha256:
        raise ReportError("PROFILE_INVALID")
    contract, contract_hash = _read(contract_path, 65536, "CONTRACT_INVALID", "CONTRACT_UNAVAILABLE")
    if contract_hash != CONTRACT_SHA256 or contract.get("id") != CONTRACT_ID or contract.get("schemaVersion") != 2:
        raise ReportError("CONTRACT_INVALID")
    if not (type(repository_id) is str and repository_id == data["repository_id"] == profile["repository"]):
        raise ReportError("IDENTITY_MISMATCH")
    if expected_repository_id is not None and repository_id != expected_repository_id:
        raise ReportError("IDENTITY_MISMATCH")
    collection = {**data["collection"], "infer_deletions":False, "overwrite_baseline":False}
    gaps = []
    if collection["inbox_total"]["value"] is None:
        gaps.append("Inbox total unknown; empty scoped window cannot infer deletion.")
    if profile["activation"] == "candidate":
        gaps.append("Profile is a candidate; native adoption and Lead uptake are not established.")
    items = []
    for item in data["items"]:
        routes = _routes(item, profile)
        authority_route = routes["authority"]["route"]
        if authority_route in _AUTHORITY_GAP_REASONS:
            gaps.append(_authority_gap(item["event_id"], authority_route))
        if routes["finding"]["evidenceGap"] is not None:
            gaps.append("Finding for event " + item["event_id"] + ": " + routes["finding"]["evidenceGap"])
        items.append({**item, "native_routes":routes,
                      "authority_assessment_basis":"reported_input_not_verified"})
    return {"report_version":1, "report_status":"RENDERED_NON_AUTHORIZING",
            "repository_id":repository_id, "input_sha256":input_hash,
            "profile_sha256":profile_hash, "contract_sha256":contract_hash,
            "native_record":data["native_record"], "candidate":data["candidate"],
            "collection":collection,
            "items":items,
            "evidence_gaps":gaps, "metrics":_metrics(data["metrics"]),
            "limits":["All observations, authority and acceptance claims are supplied inputs, not independently verified.",
                      "No execution authority, finding closure, gate clearance or readiness is generated.",
                      "No collection consent, retention change, telemetry export or native publication permission is generated."]}


class ReportParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("allow_abbrev", False)
        super().__init__(*args, **kwargs)

    def error(self, _message):
        raise ReportError("CLI_INVALID")


def _write_json_line(value, stream):
    """Write one LF-terminated JSON object as bytes; never translate newlines."""
    data = (json.dumps(value, ensure_ascii=True, allow_nan=False,
                       sort_keys=True) + "\n").encode("ascii")
    stream.buffer.write(data)
    stream.buffer.flush()


def emit_error(error):
    _write_json_line({"error_code":error.code, "message":ERRORS[error.code][1]},
                     sys.stderr)
    return ERRORS[error.code][0]


def emit_report(report):
    _write_json_line(report, sys.stdout)
    return 0


def main(argv=None):
    parser = ReportParser(description="Local JSON-only evidence report; non-authorizing, no external effects.")
    for name in ("repository-id", "input", "profile", "contract"):
        parser.add_argument("--"+name, required=True)
    try:
        args = parser.parse_args(argv)
        return emit_report(report_from_paths(args.repository_id, args.input, args.profile, args.contract))
    except ReportError as error:
        return emit_error(error)
    except Exception:
        return emit_error(ReportError("REPORT_FAILED"))


if __name__ == "__main__":
    raise SystemExit(main())
