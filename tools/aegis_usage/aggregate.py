#!/usr/bin/env python3
"""Offline central-model importer and cohort calculator for Project Aegis.

Offline by construction: no networking, no threads, no subprocess, no hosted
service. It models the steward side of the workflow-outcomes contract on
synthetic data only: manually issued admissions, a minimized raw store with
bounded retention, deletion, and honest cohort arithmetic with suppression.

The importer never enrolls: a payload is accepted only when it names an
existing active admission and proves possession of that admission's
capability secret. Withdrawal or natural expiry removes the admission, so an
old export can only be rejected, never re-created.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import secrets
import sys
from datetime import date, timedelta
from pathlib import Path

try:  # running as a module from the checkout root
    from tools.aegis_usage import local_report as contract
except ImportError:  # running as a script next to local_report.py
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import local_report as contract

STORE_VERSION = 1
CENTRAL_RETENTION_DAYS = 90
PENDING_ADMISSION_DAYS = 7
DELETION_RECEIPT_DAYS = 7
QUARANTINE_DAYS = 90
PROSPECTIVE_START_DAYS = 7
OUTCOME_FLOOR = 20
CELL_FLOOR = 5
STAGE_FLOOR = 20
MAX_AGGREGATE_RECORDS = 5000
REPORT_VERSION = "workflow-outcomes-aggregate-v1"
ADMISSION_CONTEXT = "aegis-admission-v1"
TERMINAL = contract.TERMINAL_STATUSES


def _fail(code: str, message: str, path: str = "") -> None:
    raise contract.ContractError(code, message, path)


def new_store() -> dict:
    return {
        "store_version": STORE_VERSION,
        "admissions": {},
        "admission_tombstones": {},
        "records": {},
        "quarantine": [],
        "expired_cohorts": {},
        "deletion_receipts": {},
        "withdrawals": 0,
        "ignored": 0,
    }


def load_store(path: Path) -> dict:
    if not path.exists():
        return new_store()
    try:
        store = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        _fail("store_unreadable", "central model store cannot be read: " + str(exc), str(path))
    if not isinstance(store, dict) or store.get("store_version") != STORE_VERSION:
        _fail("store_version", "central model store version is not supported", str(path))
    for key, value in new_store().items():
        store.setdefault(key, value)
    return store


def save_store(path: Path, store: dict) -> None:
    contract.write_private_store(path, json.dumps(store, indent=2, sort_keys=True, ensure_ascii=True) + "\n")


def day(value: str) -> date:
    return contract.parse_day(value, "day")


def add_days(value: str, days: int) -> str:
    return (day(value) + timedelta(days=days)).isoformat()


# --------------------------------------------------------------------------
# Admission: a separate manual enrollment operation, never created by import
# --------------------------------------------------------------------------


def admission_verifier(admission_ref: str, capability: str) -> str:
    material = ADMISSION_CONTEXT + "|" + admission_ref + "|" + capability
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def enrollment_fields(envelope: dict) -> dict:
    """The immutable enrollment tuple fixed in the acknowledged start."""
    snapshot = envelope["snapshot"]
    return {
        "schema": envelope["schema"],
        "library_revision": envelope["library_revision"],
        "capture_tier": envelope["capture_tier"],
        "consent_policy_version": envelope["consent_policy_version"],
        "reporting_window_days": envelope["reporting_window_days"],
        "start_day": snapshot["start_day"],
        "applicable_stages": list(snapshot["applicable_stages"]),
        "criteria_frozen_before_work": snapshot["criteria_frozen_before_work"],
        "criteria_contract_ref": snapshot["criteria_contract_ref"],
    }


def enrollment_fingerprint(envelope: dict) -> str:
    encoded = json.dumps(enrollment_fields(envelope), sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def issue_admission(store: dict, notice: dict, *, issued_day: str) -> dict:
    """Issue a fresh random admission after a prospective eligibility review.

    The notice is the minimized start information the participant sent through
    the approved private channel: workflow_ref, start_day, applicable stages,
    the frozen-criteria flag and the random criteria contract reference. No
    identity is accepted or stored.
    """
    issued = day(issued_day)
    start = contract.parse_day(notice.get("start_day"), "start_day")
    if start > issued:
        _fail("start_in_future", "a start cannot follow its acknowledgement", "start_day")
    if start < issued - timedelta(days=PROSPECTIVE_START_DAYS):
        _fail("start_outside_window", "a prospective start is at most seven days old", "start_day")
    workflow_ref = contract.parse_ref(notice.get("workflow_ref"), "workflow_ref", "wf-")
    if workflow_ref in store["records"]:
        _fail("already_enrolled", "this workflow already has a central record", "workflow_ref")
    for existing in store["admissions"].values():
        if existing["workflow_ref"] == workflow_ref:
            _fail("admission_exists", "an active admission already covers this workflow", "workflow_ref")
    stages = notice.get("applicable_stages")
    if stages is None:
        stages = list(contract.STAGES)
    if not isinstance(stages, list) or not stages:
        _fail("invalid_stages", "applicable_stages needs at least one stage", "applicable_stages")
    if any(stage not in contract.STAGES for stage in stages) or [s for s in contract.STAGES if s in stages] != list(stages):
        _fail("invalid_stages", "applicable_stages must be an ordered subset of the five stages", "applicable_stages")
    frozen = notice.get("criteria_frozen_before_work")
    if not isinstance(frozen, bool):
        _fail("invalid_type", "criteria_frozen_before_work must be boolean", "criteria_frozen_before_work")
    contract_ref = contract.parse_ref(notice.get("criteria_contract_ref"), "criteria_contract_ref", "crit-")
    admission_ref = contract.random_ref("adm-")
    capability = secrets.token_hex(32)
    enrollment = {
        "schema": contract.SCHEMA_NAME,
        "library_revision": contract.SUPPORTED_LIBRARY_REVISIONS[0],
        "capture_tier": contract.CAPTURE_TIER,
        "consent_policy_version": contract.SUPPORTED_CONSENT_POLICIES[0],
        "reporting_window_days": contract.REPORTING_WINDOW_DAYS,
        "start_day": contract.day_str(start),
        "applicable_stages": [stage for stage in contract.STAGES if stage in stages],
        "criteria_frozen_before_work": frozen,
        "criteria_contract_ref": contract_ref,
    }
    fingerprint = hashlib.sha256(
        json.dumps(enrollment, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    ).hexdigest()
    store["admissions"][admission_ref] = {
        "workflow_ref": workflow_ref,
        "verifier": admission_verifier(admission_ref, capability),
        "issued_day": issued_day,
        "first_receipt": None,
        "expires_at": None,
        "enrollment_fingerprint": fingerprint,
        "enrollment": enrollment,
    }
    return {"admission_ref": admission_ref, "capability": capability, "enrollment_fingerprint": fingerprint}


def _verify_capability(store: dict, admission_ref: str, capability: str) -> dict:
    """Authenticate a capability without deciding whether import is allowed.

    An expired admission keeps a verification-only tombstone for as long as
    linked raw or quarantined data is retained, so withdrawal does not depend
    on import eligibility.
    """
    if not isinstance(admission_ref, str):
        _fail("unknown_admission", "no active admission for this reference", "admission_ref")
    record = store["admissions"].get(admission_ref)
    if record is None:
        record = store.get("admission_tombstones", {}).get(admission_ref)
    if record is None:
        _fail("unknown_admission", "no active admission for this reference", "admission_ref")
    if not isinstance(capability, str) or not secrets.compare_digest(
        admission_verifier(admission_ref, capability), record["verifier"]
    ):
        _fail("bad_capability", "the admission capability does not verify", "capability")
    return record


def _require_admission(store: dict, admission_ref: str, capability: str, receipt_day: str) -> dict:
    if not isinstance(admission_ref, str) or admission_ref not in store["admissions"]:
        _fail("unknown_admission", "no active admission for this reference", "admission_ref")
    admission = store["admissions"][admission_ref]
    if not isinstance(capability, str) or not secrets.compare_digest(
        admission_verifier(admission_ref, capability), admission["verifier"]
    ):
        _fail("bad_capability", "the admission capability does not verify", "capability")
    today = day(receipt_day)
    if admission["expires_at"] is not None:
        if today > day(admission["expires_at"]):
            _fail("expired_admission", "the admission reached its 90-day expiry", "admission_ref")
    elif today > day(admission["issued_day"]) + timedelta(days=PENDING_ADMISSION_DAYS):
        _fail("expired_admission", "an unacknowledged admission expires in seven days", "admission_ref")
    return admission


# --------------------------------------------------------------------------
# Import: dedupe, revision invariants, bounded retention
# --------------------------------------------------------------------------


def import_export(store: dict, payload: object, *, capability: str, receipt_day: str) -> dict:
    """Import one previewed export. Importing never creates an enrollment."""
    raw = payload if isinstance(payload, (bytes, bytearray)) else contract.canonical_bytes(payload)
    envelope = contract.loads_strict(bytes(raw))
    contract.validate_envelope(envelope)
    snapshot = envelope["snapshot"]
    admission_ref = envelope["admission_ref"]
    admission = _require_admission(store, admission_ref, capability, receipt_day)
    if admission["workflow_ref"] != snapshot["workflow_ref"]:
        _fail("admission_mismatch", "the admission names a different workflow", "workflow_ref")
    today = day(receipt_day)
    if today < day(admission["issued_day"]):
        _fail("receipt_before_issue", "an export cannot be received before its admission was issued", "day")
    for event in snapshot["transitions"]:
        if day(event["effective_day"]) > today:
            _fail(
                "event_after_receipt",
                "an event cannot be effective after the day its export was received",
                "snapshot.transitions",
            )
    fingerprint = enrollment_fingerprint(envelope)
    if fingerprint != admission["enrollment_fingerprint"]:
        return _quarantine(
            store,
            receipt_day,
            "enrollment_change",
            envelope,
            "the immutable enrollment fields differ from the acknowledged enrollment",
        )

    record = store["records"].get(snapshot["workflow_ref"])
    if record is not None and today < day(record["last_receipt_day"]):
        _fail("receipt_day_regression", "a received export cannot predate the record's last receipt", "day")
    if record is None:
        if today > day(snapshot["start_day"]) + timedelta(days=PENDING_ADMISSION_DAYS):
            prospective = False
        else:
            prospective = True
        if admission["first_receipt"] is None:
            admission["first_receipt"] = receipt_day
            admission["expires_at"] = add_days(receipt_day, CENTRAL_RETENTION_DAYS)
        transitions = [_stamp(event, receipt_day) for event in snapshot["transitions"]]
        record = {
            "workflow_ref": snapshot["workflow_ref"],
            "enrollment": admission["enrollment"],
            "enrollment_fingerprint": fingerprint,
            "revision": snapshot["revision"],
            "export_ref": snapshot["export_ref"],
            "first_receipt_day": receipt_day,
            "last_receipt_day": receipt_day,
            "expires_at": admission["expires_at"] or add_days(receipt_day, CENTRAL_RETENTION_DAYS),
            "prospective": prospective,
            "late_entries": 0,
            "transitions": transitions,
            "canonical_export": _canonical_text(envelope),
        }
        store["records"][snapshot["workflow_ref"]] = record
        return {
            "status": "accepted",
            "revision": record["revision"],
            "prospective": prospective,
            "first_receipt": record["first_receipt_day"],
        }

    if record["enrollment_fingerprint"] != fingerprint:
        return _quarantine(
            store, receipt_day, "enrollment_change", envelope, "a later revision altered immutable enrollment"
        )

    revision = snapshot["revision"]
    if revision < record["revision"]:
        store["ignored"] += 1
        return {"status": "ignored", "revision": revision, "stored_revision": record["revision"]}
    if revision == record["revision"]:
        if record["canonical_export"] == _canonical_text(envelope):
            return {"status": "duplicate", "revision": revision}
        return _quarantine(
            store, receipt_day, "conflicting_revision", envelope, "the same revision carries different bytes"
        )

    accepted = {event["event_ref"]: event for event in record["transitions"]}
    incoming = {event["event_ref"]: event for event in snapshot["transitions"]}
    for ref, stored in accepted.items():
        candidate = incoming.get(ref)
        if candidate is None:
            return _quarantine(
                store, receipt_day, "history_rewrite", envelope, "an accepted event was removed by a higher revision"
            )
        for key in ("kind", "effective_day", "value", "stage"):
            if candidate.get(key) != stored.get(key):
                return _quarantine(
                    store, receipt_day, "history_rewrite", envelope, "an accepted event was changed by a higher revision"
                )
    transitions = []
    for event in snapshot["transitions"]:
        stamped = _stamp(event, receipt_day)
        stored = accepted.get(event["event_ref"])
        if stored is not None:
            stamped["first_receipt_day"] = stored["first_receipt_day"]
        transitions.append(stamped)
    close_day = add_days(record["enrollment"]["start_day"], contract.REPORTING_WINDOW_DAYS + contract.LAG_DAYS)
    record["transitions"] = transitions
    record["revision"] = revision
    record["export_ref"] = snapshot["export_ref"]
    record["last_receipt_day"] = receipt_day
    record["canonical_export"] = _canonical_text(envelope)
    if receipt_day > close_day:
        record["late_entries"] = int(record.get("late_entries", 0)) + 1
    return {"status": "updated", "revision": revision, "first_receipt": record["first_receipt_day"]}


def _stamp(event: dict, receipt_day: str) -> dict:
    return {
        "event_ref": event["event_ref"],
        "kind": event["kind"],
        "effective_day": event["effective_day"],
        "value": event["value"],
        "stage": event["stage"],
        "first_receipt_day": receipt_day,
    }


def _canonical_text(envelope: dict) -> str:
    return contract.canonical_bytes(envelope).decode("utf-8")


def _quarantine(store: dict, receipt_day: str, code: str, envelope: dict, message: str) -> dict:
    snapshot = envelope["snapshot"]
    store["quarantine"].append(
        {
            "received_day": receipt_day,
            "code": code,
            "message": message,
            "workflow_ref": snapshot["workflow_ref"],
            "revision": snapshot["revision"],
            "payload": _canonical_text(envelope),
        }
    )
    return {"status": "quarantined", "code": code, "revision": snapshot["revision"]}


# --------------------------------------------------------------------------
# Withdrawal, expiry and retention
# --------------------------------------------------------------------------


def withdraw(store: dict, *, admission_ref: str, capability: str, decision_day: str) -> dict:
    """Delete a workflow's admission, raw snapshots and quarantine copies.

    The deletion receipt is a random, unlinkable id with its own seven-day
    expiry; no tombstone keeps the workflow or admission reference alive.
    """
    identity = _verify_capability(store, admission_ref, capability)
    workflow_ref = identity["workflow_ref"]
    removed = 1 if workflow_ref in store["records"] else 0
    store["records"].pop(workflow_ref, None)
    store["quarantine"] = [entry for entry in store["quarantine"] if entry["workflow_ref"] != workflow_ref]
    store["admissions"].pop(admission_ref, None)
    store.get("admission_tombstones", {}).pop(admission_ref, None)
    receipt_id = secrets.token_hex(16)
    store["deletion_receipts"][receipt_id] = {
        "deleted_day": decision_day,
        "expires_at": add_days(decision_day, DELETION_RECEIPT_DAYS),
    }
    store["withdrawals"] = int(store.get("withdrawals", 0)) + 1
    return {"receipt_id": receipt_id, "deleted_records": removed, "raw_rows": 0, "received_day": decision_day}


def expire(store: dict, *, today: str) -> dict:
    """Apply 90-day central retention, quarantine and receipt expiry.

    An expired admission leaves a capability-verification tombstone while any
    linked raw record or quarantine payload survives, so the participant can
    still withdraw; the tombstone is deleted with the last linked datum.
    """
    now = day(today)
    removed_admissions = 0
    removed_tombstones = 0
    for admission_ref, admission in list(store["admissions"].items()):
        expiry = admission["expires_at"]
        if expiry is not None:
            if now > day(expiry):
                store.setdefault("admission_tombstones", {})[admission_ref] = {
                    "workflow_ref": admission["workflow_ref"],
                    "verifier": admission["verifier"],
                    "expired_day": expiry,
                }
                del store["admissions"][admission_ref]
                removed_admissions += 1
        elif now > day(admission["issued_day"]) + timedelta(days=PENDING_ADMISSION_DAYS):
            store.setdefault("admission_tombstones", {})[admission_ref] = {
                "workflow_ref": admission["workflow_ref"],
                "verifier": admission["verifier"],
                "expired_day": add_days(admission["issued_day"], PENDING_ADMISSION_DAYS),
            }
            del store["admissions"][admission_ref]
            removed_admissions += 1
    removed_records = 0
    for workflow_ref, record in list(store["records"].items()):
        if now > day(record["expires_at"]):
            month = record["enrollment"]["start_day"][:7]
            cohorts = store.setdefault("expired_cohorts", {})
            cohorts[month] = int(cohorts.get(month, 0)) + 1
            del store["records"][workflow_ref]
            removed_records += 1
    kept_quarantine = []
    for entry in store["quarantine"]:
        if now <= day(entry["received_day"]) + timedelta(days=QUARANTINE_DAYS):
            kept_quarantine.append(entry)
    removed_quarantine = len(store["quarantine"]) - len(kept_quarantine)
    store["quarantine"] = kept_quarantine
    removed_receipts = 0
    for receipt_id, receipt in list(store["deletion_receipts"].items()):
        if now > day(receipt["expires_at"]):
            del store["deletion_receipts"][receipt_id]
            removed_receipts += 1
    linked = set(store["records"]) | {entry["workflow_ref"] for entry in store["quarantine"]}
    for admission_ref, tombstone in list(store.get("admission_tombstones", {}).items()):
        if tombstone["workflow_ref"] not in linked:
            del store["admission_tombstones"][admission_ref]
            removed_tombstones += 1
    return {
        "admissions": removed_admissions,
        "tombstones": removed_tombstones,
        "records": removed_records,
        "quarantine": removed_quarantine,
        "receipts": removed_receipts,
    }


# --------------------------------------------------------------------------
# Cohort arithmetic
# --------------------------------------------------------------------------


def _rate(numerator: int, denominator: int) -> dict:
    if denominator == 0:
        return {"numerator": 0, "denominator": 0, "rate": None, "status": "unavailable"}
    return {"numerator": numerator, "denominator": denominator, "rate": round(numerator / denominator, 4), "status": "available"}


def _classify(record: dict, close_day: str, cutoff: str) -> dict:
    """Reconstruct the day-30 state from events effective by day 30.

    Events first received after the seven-day reporting lag are excluded from
    the rate (they are counted as late) so a late report can never rewrite an
    earlier outcome.
    """
    usable = [
        event
        for event in record["transitions"]
        if event["effective_day"] <= cutoff and event["first_receipt_day"] <= close_day
    ]
    usable.sort(key=lambda event: (event["effective_day"], event["event_ref"]))
    late_events = [
        event
        for event in record["transitions"]
        if event["first_receipt_day"] > close_day and event["effective_day"] <= cutoff
    ]
    terminal = [event for event in usable if event["kind"] == "status"]
    if terminal:
        outcome = terminal[-1]["value"]
        delivery_day = terminal[-1]["effective_day"] if outcome == "delivered" else None
    elif any(event["kind"] == "observation" and event["value"] == "ongoing" and event["effective_day"] == cutoff for event in usable):
        outcome = "ongoing"
        delivery_day = None
    else:
        outcome = "unknown"
        delivery_day = None
    acceptance_events = [event for event in usable if event["kind"] == "acceptance"]
    acceptance = acceptance_events[-1]["value"] if acceptance_events else "not_assessed"
    acceptance_day = acceptance_events[-1]["effective_day"] if acceptance_events else None
    frozen_claimed = bool(record["enrollment"]["criteria_frozen_before_work"])
    scope_changed = any(
        event["kind"] == "scope_change" and event["effective_day"] <= cutoff for event in usable
    )
    frozen_valid = frozen_claimed and not scope_changed
    stages = {}
    for stage in contract.STAGES:
        if stage not in record["enrollment"]["applicable_stages"]:
            stages[stage] = {"applicable": False, "complete": False}
            continue
        complete = any(
            event["kind"] == "stage" and event["stage"] == stage and event["value"] == "complete"
            for event in usable
        )
        stages[stage] = {"applicable": True, "complete": complete}
    return {
        "outcome": outcome,
        "delivery_day": delivery_day,
        "acceptance": acceptance,
        "acceptance_day": acceptance_day,
        "frozen_valid": frozen_valid,
        "frozen_claimed": frozen_claimed,
        "scope_changed": scope_changed,
        "stages": stages,
        "late_events": len(late_events),
    }


def compute_report(store: dict, *, as_of: str) -> dict:
    """Build the restricted cohort report as of one day."""
    today = day(as_of)
    months: dict[str, dict] = {}
    open_months: dict[str, int] = {}
    incomplete_months: dict[str, int] = {}
    retrospective = 0
    expired_excluded = 0
    for month, count in (store.get("expired_cohorts") or {}).items():
        incomplete_months[month] = incomplete_months.get(month, 0) + int(count)
        expired_excluded += int(count)
    records = sorted(store["records"].values(), key=lambda record: record["workflow_ref"])
    truncated = False
    if len(records) > MAX_AGGREGATE_RECORDS:
        records = records[:MAX_AGGREGATE_RECORDS]
        truncated = True
    for record in records:
        enrollment = record["enrollment"]
        start = enrollment["start_day"]
        close_day = add_days(start, contract.REPORTING_WINDOW_DAYS + contract.LAG_DAYS)
        cutoff = add_days(start, contract.REPORTING_WINDOW_DAYS)
        if today > day(record["expires_at"]):
            expired_excluded += 1
            incomplete_months[start[:7]] = incomplete_months.get(start[:7], 0) + 1
            continue
        if today < day(close_day):
            open_months[start[:7]] = open_months.get(start[:7], 0) + 1
            continue
        if not record["prospective"]:
            retrospective += 1
            continue
        state = _classify(record, close_day, cutoff)
        cell = months.setdefault(
            start[:7],
            {
                "month": start[:7],
                "closed_on": close_day,
                "n": 0,
                "outcomes": {"delivered": 0, "failed": 0, "abandoned": 0, "ongoing": 0, "unknown": 0},
                "stages": {stage: {"complete": 0, "denominator": 0, "not_applicable": 0} for stage in contract.STAGES},
                "acceptance_self": {"passing": 0, "assessed": 0},
                "acceptance_independent": {"passing": 0, "assessed": 0},
                "attested_success": 0,
                "frozen_invalidated": 0,
                "late_entries": 0,
                "late_events": 0,
                "incomplete": False,
            },
        )
        if close_day > cell["closed_on"]:
            cell["closed_on"] = close_day
        cell["n"] += 1
        cell["outcomes"][state["outcome"]] += 1
        if state["frozen_claimed"] and state["scope_changed"]:
            cell["frozen_invalidated"] += 1
        cell["late_entries"] += int(record.get("late_entries", 0))
        cell["late_events"] += state["late_events"]
        for stage in contract.STAGES:
            if not state["stages"][stage]["applicable"]:
                cell["stages"][stage]["not_applicable"] += 1
                continue
            cell["stages"][stage]["denominator"] += 1
            if state["stages"][stage]["complete"]:
                cell["stages"][stage]["complete"] += 1
        if state["outcome"] == "delivered":
            if state["acceptance"] in ("self_reported_pass", "self_reported_fail"):
                cell["acceptance_self"]["assessed"] += 1
                if state["acceptance"] == "self_reported_pass":
                    cell["acceptance_self"]["passing"] += 1
            if state["acceptance"] in ("independent_attested_pass", "independent_attested_fail"):
                cell["acceptance_independent"]["assessed"] += 1
                if state["acceptance"] == "independent_attested_pass":
                    cell["acceptance_independent"]["passing"] += 1
            if (
                state["frozen_valid"]
                and state["acceptance"] == "independent_attested_pass"
                and state["acceptance_day"] is not None
                and state["acceptance_day"] <= cutoff
            ):
                cell["attested_success"] += 1

    for month, expired_count in incomplete_months.items():
        if month in months:
            months[month]["incomplete"] = True
            months[month]["expired_excluded"] = expired_count

    for cell in months.values():
        n = cell["n"]
        outcomes = cell["outcomes"]
        discovered = outcomes["delivered"] + outcomes["failed"] + outcomes["abandoned"] + outcomes["ongoing"]
        cell["metrics"] = {
            "delivery_30d": _rate(outcomes["delivered"], n),
            "follow_up_coverage": _rate(discovered, n),
            "unknown_share": _rate(outcomes["unknown"], n),
            "ongoing_share": _rate(outcomes["ongoing"], n),
            "abandoned_share": _rate(outcomes["abandoned"], n),
            "failed_share": _rate(outcomes["failed"], n),
            "stage_reach": {
                stage: {
                    "numerator": cell["stages"][stage]["complete"],
                    "denominator": cell["stages"][stage]["denominator"],
                    "rate": (
                        None
                        if cell["stages"][stage]["denominator"] == 0
                        else round(cell["stages"][stage]["complete"] / cell["stages"][stage]["denominator"], 4)
                    ),
                    "not_applicable": cell["stages"][stage]["not_applicable"],
                }
                for stage in contract.STAGES
            },
            "assessed_acceptance_self_report": _rate(cell["acceptance_self"]["passing"], cell["acceptance_self"]["assessed"]),
            "assessed_acceptance_independent": _rate(
                cell["acceptance_independent"]["passing"], cell["acceptance_independent"]["assessed"]
            ),
            "independently_attested_success": _rate(cell["attested_success"], n),
        }
        cell["frozen_criteria_invalidated"] = cell["frozen_invalidated"]
        del cell["acceptance_self"]
        del cell["acceptance_independent"]
        del cell["attested_success"]
        del cell["frozen_invalidated"]

    return {
        "report_version": REPORT_VERSION,
        "as_of": as_of,
        "schema": contract.SCHEMA_NAME,
        "capture_tier": contract.CAPTURE_TIER,
        "horizon_days": contract.REPORTING_WINDOW_DAYS,
        "lag_days": contract.LAG_DAYS,
        "cohorts": {month: months[month] for month in sorted(months)},
        "open_cohorts": {month: open_months[month] for month in sorted(open_months)},
        "retrospective_excluded": retrospective,
        "expired_excluded": expired_excluded,
        "incomplete_cohorts": {
            month: count for month, count in sorted(incomplete_months.items()) if month not in months
        },
        "withdrawals": int(store.get("withdrawals", 0)),
        "quarantine": len(store["quarantine"]),
        "ignored": int(store.get("ignored", 0)),
        "truncated": truncated,
        "limitations": [
            "Opt-in starts are not a representative sample and are not adoption.",
            "Withdrawn workflows leave the denominator; the withheld count is non-linkable.",
            "Participant-reported independent attestation is not centrally verified success.",
            "A cohort with an observed expired record is marked incomplete and withheld from the publishable view.",
            "No public pilot metrics are authorized.",
        ],
    }


def publishable_report(report: dict) -> dict:
    """Apply sparse, complementary and differencing suppression to a report."""
    if report.get("truncated"):
        # A capped store yields partial denominators; refuse the rehearsal view
        # rather than publishing a cohort computed from part of the record set.
        _fail(
            "report_truncated",
            "the retained store exceeded the aggregate record cap; a partial cohort is never publishable",
            "",
        )
    open_months = report.get("open_cohorts") or {}
    published: list = []
    last_counts = None
    suppressed_cells: list = []
    for month in sorted(report["cohorts"]):
        cell = report["cohorts"][month]
        n = cell["n"]
        outcomes = cell["outcomes"]
        if month in open_months:
            suppressed_cells.append({"month": month, "reason": "cohort_open"})
            continue
        if cell.get("incomplete"):
            suppressed_cells.append({"month": month, "reason": "retention_incomplete"})
            continue
        if n < OUTCOME_FLOOR:
            suppressed_cells.append({"month": month, "reason": "cohort_below_floor"})
            continue
        sparse = [name for name, count in outcomes.items() if 0 < count < CELL_FLOOR]
        if sparse:
            suppressed_cells.append({"month": month, "reason": "sparse_outcome", "cells": sorted(sparse)})
            continue
        counts = [outcomes[name] for name in ("delivered", "failed", "abandoned", "ongoing", "unknown")]
        if last_counts is not None and any(abs(left - right) in (1, 2, 3, 4) for left, right in zip(last_counts, counts)):
            suppressed_cells.append({"month": month, "reason": "differencing_withheld"})
            continue
        attested = cell["metrics"]["independently_attested_success"]
        entry = {
            "month": month,
            "closed_on": cell["closed_on"],
            "n": n,
            "outcomes": {name: outcomes[name] for name in ("delivered", "failed", "abandoned", "ongoing", "unknown")},
            "delivery_30d": cell["metrics"]["delivery_30d"],
            "follow_up_coverage": cell["metrics"]["follow_up_coverage"],
            "independently_attested_success": (
                {"status": "withheld", "reason": "sparse_attestation_cell"}
                if 0 < attested["numerator"] < CELL_FLOOR
                else attested
            ),
            "stage_reach": {},
            "late_entries": cell["late_entries"],
            "late_events": cell["late_events"],
        }
        for stage, metric in cell["metrics"]["stage_reach"].items():
            denominator = metric["denominator"]
            numerator = metric["numerator"]
            if denominator >= STAGE_FLOOR and (numerator == 0 or numerator >= CELL_FLOOR):
                entry["stage_reach"][stage] = metric
            else:
                entry["stage_reach"][stage] = {"status": "withheld", "reason": "sparse_stage_cell"}
        max_share = max(counts) / n if n else 0
        entry["flags"] = []
        if max_share >= 0.5 and n < 40:
            entry["flags"].append("dominant_contributor_review")
        published.append(entry)
        last_counts = counts
    if len(published) == 1 and len(report["cohorts"]) > 1:
        suppressed_cells.append({"month": published[0]["month"], "reason": "complementary_suppression"})
        published = []
    return {
        "disclosure": {
            "public_release": False,
            "reason": "No public pilot metrics are authorized; this suppressed view is a rehearsal only.",
        },
        "report_version": report["report_version"],
        "as_of": report["as_of"],
        "cohorts": published,
        "suppressed_cohorts": suppressed_cells,
        "withdrawals": report["withdrawals"],
        "limitations": report["limitations"],
    }


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Offline central-model importer and cohort calculator.")
    parser.add_argument("--store", required=True, help="path to the central model store (outside the repository)")
    sub = parser.add_subparsers(dest="command", required=True)

    issue = sub.add_parser("issue-admission", help="issue a fresh admission after prospective review")
    issue.add_argument("--notice", required=True, help="JSON file with the minimized start notice")
    issue.add_argument("--day", required=True)

    import_cmd = sub.add_parser("import", help="import one previewed export")
    import_cmd.add_argument("--payload", required=True)
    import_cmd.add_argument("--capability")
    import_cmd.add_argument("--capability-file", help="file holding the capability secret (preferred)")
    import_cmd.add_argument("--day", required=True)

    withdraw_cmd = sub.add_parser("withdraw", help="delete a workflow's linked reporting data")
    withdraw_cmd.add_argument("--admission-ref", required=True)
    withdraw_cmd.add_argument("--capability")
    withdraw_cmd.add_argument("--capability-file", help="file holding the capability secret (preferred)")
    withdraw_cmd.add_argument("--day", required=True)

    expire_cmd = sub.add_parser("expire", help="apply central retention and receipt expiry")
    expire_cmd.add_argument("--day", required=True)

    report = sub.add_parser("report", help="compute the cohort report")
    report.add_argument("--as-of", required=True)
    report.add_argument("--publishable", action="store_true", help="print the suppressed rehearsal view")
    return parser


def _capability(args) -> str:
    """Read the capability secret, preferring a file over argv."""
    chosen = int(bool(args.capability)) + int(bool(args.capability_file))
    if chosen != 1:
        _fail("invalid_arguments", "supply exactly one of --capability or --capability-file", "capability")
    if args.capability_file:
        try:
            value = Path(args.capability_file).read_text(encoding="utf-8").strip()
        except OSError as exc:
            _fail("capability_unreadable", "the capability file cannot be read: " + str(exc), args.capability_file)
        if not value:
            _fail("capability_unreadable", "the capability file is empty", args.capability_file)
        return value
    sys.stderr.write(
        "WARNING capability_in_argv: a secret in argv is visible to other local processes and shell history; prefer --capability-file\n"
    )
    return args.capability


def main(argv: list | None = None) -> int:
    args = _parser().parse_args(argv)
    store_path = Path(args.store)
    try:
        store = load_store(store_path)
        if args.command == "issue-admission":
            try:
                notice = json.loads(Path(args.notice).read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                _fail("notice_unreadable", "the start notice cannot be read: " + str(exc), str(args.notice))
            result = issue_admission(store, notice, issued_day=args.day)
            save_store(store_path, store)
            print(json.dumps(result, sort_keys=True))
            return 0
        if args.command == "import":
            try:
                raw = Path(args.payload).read_bytes()
            except OSError as exc:
                _fail("payload_unreadable", "the payload cannot be read: " + str(exc), str(args.payload))
            result = import_export(store, raw, capability=_capability(args), receipt_day=args.day)
            save_store(store_path, store)
            print(json.dumps(result, sort_keys=True))
            return 0
        if args.command == "withdraw":
            result = withdraw(store, admission_ref=args.admission_ref, capability=_capability(args), decision_day=args.day)
            save_store(store_path, store)
            print(json.dumps(result, sort_keys=True))
            return 0
        if args.command == "expire":
            result = expire(store, today=args.day)
            save_store(store_path, store)
            print(json.dumps(result, sort_keys=True))
            return 0
        if args.command == "report":
            report = compute_report(store, as_of=args.as_of)
            view = publishable_report(report) if args.publishable else report
            print(json.dumps(view, indent=2, sort_keys=True))
            return 0
    except contract.ContractError as exc:
        sys.stderr.write("ERROR " + exc.code + ": " + exc.message + (" [" + exc.path + "]" if exc.path else "") + "\n")
        return 2
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        sys.stderr.write("ERROR store_unreadable: " + str(exc) + "\n")
        return 2
    return 2


if __name__ == "__main__":
    sys.exit(main())
