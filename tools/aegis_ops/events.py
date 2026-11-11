"""C3.1 event catalogue, duplicate semantics and ordering checks.

The catalogue is closed and derived only from the existing GitHub event set.
Unknown `(event_name, action)` pairs are refused; a duplicate delivery is a
no-op only when the catalogue says NO_OP; an out-of-order delivery is refused.
There is no polling loop, no new trigger source and no network call.
"""

from __future__ import annotations

import typing

from . import schema

SOURCES = (
    "pull_request",
    "push",
    "workflow_run",
    "check_suite",
    "issue_comment",
    "workflow_dispatch",
)

CATALOGUE_FIELDS = (
    "event_name",
    "action",
    "source",
    "stage_action",
    "deterministic_check",
    "authority_role",
    "state_update",
    "duplicate_semantics",
)

EVENT_FIELDS = ("delivery_id", "event_name", "action", "head_sha", "sequence")


def validate_catalogue(
    document: typing.Mapping[str, object],
) -> typing.Tuple[schema.Report, typing.Dict[typing.Tuple[str, str], typing.Dict[str, object]]]:
    """Validate the closed catalogue and index it by (event, action)."""

    report = schema.Report()
    schema.check_schema_version(document, schema.SCHEMA_EVENT, report)
    schema.check_object(
        document,
        "event catalogue",
        required=("schema_version", "catalogue", "events"),
        optional=(),
        report=report,
    )
    catalogue = document.get("catalogue")
    index: typing.Dict[typing.Tuple[str, str], typing.Dict[str, object]] = {}
    rows = catalogue if isinstance(catalogue, list) else []
    if not isinstance(catalogue, list) or not catalogue:
        report.add("CATALOGUE_MISSING", "catalogue must be a non-empty list")
    for position, row in enumerate(rows):
        where = "catalogue[%d]" % position
        checked = schema.check_object(row, where, CATALOGUE_FIELDS, (), report)
        if checked is None:
            continue
        event_name = schema.check_enum(
            checked.get("event_name"), where + ".event_name", SOURCES, report
        )
        source = schema.check_enum(
            checked.get("source"), where + ".source", SOURCES, report
        )
        if event_name is not None and source is not None and event_name != source:
            report.add(
                "CATALOGUE_SOURCE_MISMATCH",
                "%s.event_name %r does not equal source %r" % (where, event_name, source),
            )
        for field in (
            "stage_action",
            "deterministic_check",
            "authority_role",
            "state_update",
        ):
            schema.check_string(checked.get(field), where + "." + field, report)
        duplicate = schema.check_enum(
            checked.get("duplicate_semantics"),
            where + ".duplicate_semantics",
            schema.DUPLICATE_SEMANTICS,
            report,
        )
        action = checked.get("action")
        if not isinstance(action, str):
            report.add("EVENT_ACTION_INVALID", "%s.action must be a string (empty for push)" % where)
        elif action and not action.strip():
            report.add("EVENT_ACTION_INVALID", "%s.action must be empty or non-blank" % where)
        key = (str(event_name), str(action))
        if key in index:
            report.add(
                "CATALOGUE_DUPLICATE_ROW",
                "%s repeats the %r/%r catalogue row" % (where, key[0], key[1]),
            )
        if event_name is not None and duplicate is not None:
            index[key] = checked
    return report, index


def validate_events(
    document: typing.Mapping[str, object],
) -> typing.Dict[str, object]:
    """Validate one synthetic event sequence against the catalogue."""

    report, index = validate_catalogue(document)
    events = document.get("events")
    if not isinstance(events, list) or not events:
        report.add("EVENTS_MISSING", "events must be a non-empty list")
        events = []
    results: typing.List[typing.Dict[str, object]] = []
    applied: typing.List[str] = []
    duplicates: typing.List[str] = []
    refused: typing.List[str] = []
    seen: typing.Dict[typing.Tuple[str, str, str], int] = {}
    last_sequence: typing.Optional[int] = None
    for position, event in enumerate(events):
        where = "events[%d]" % position
        checked = schema.check_object(event, where, EVENT_FIELDS, (), report)
        if checked is None:
            continue
        delivery = schema.check_string(
            checked.get("delivery_id"), where + ".delivery_id", report
        )
        event_name = schema.check_enum(
            checked.get("event_name"), where + ".event_name", SOURCES, report
        )
        action_value = checked.get("action")
        action = "" if action_value in (None, "") else str(action_value)
        head = schema.check_hex40(checked.get("head_sha"), where + ".head_sha", report)
        sequence_value = checked.get("sequence")
        if not schema.is_int(sequence_value):
            report.add("EVENT_SEQUENCE_INVALID", "%s.sequence must be an integer" % where)
            sequence_value = None
        if sequence_value is not None and last_sequence is not None and sequence_value <= last_sequence:
            report.add(
                "EVENT_OUT_OF_ORDER",
                "%s sequence %d is not greater than the previous %d"
                % (where, sequence_value, last_sequence),
            )
            refused.append(str(delivery))
        if sequence_value is not None:
            last_sequence = sequence_value
        row = index.get((str(event_name), action))
        if row is None:
            report.add(
                "EVENT_UNKNOWN",
                "%s names %r/%r, which is not in the closed catalogue"
                % (where, event_name, action),
            )
            refused.append(str(delivery))
            continue
        key = (str(event_name), action, str(head))
        duplicate_semantics = row["duplicate_semantics"]
        decision = "APPLY"
        reason = "first delivery"
        if key in seen:
            if duplicate_semantics == "NO_OP":
                decision = "DUPLICATE_NOOP"
                reason = "catalogue duplicate_semantics=NO_OP"
            elif duplicate_semantics == "RESTART_NOT_ALLOWED":
                decision = "REFUSED"
                reason = "catalogue duplicate_semantics=RESTART_NOT_ALLOWED"
            else:
                decision = "REFUSED"
                reason = "catalogue duplicate_semantics=INVALID"
        seen[key] = seen.get(key, 0) + 1
        if decision == "APPLY":
            applied.append(str(row["stage_action"]))
        elif decision == "DUPLICATE_NOOP":
            duplicates.append(str(delivery))
        else:
            refused.append(str(delivery))
        results.append(
            {
                "delivery_id": delivery,
                "event_name": event_name,
                "action": action,
                "head_sha": head,
                "decision": decision,
                "reason": reason,
                "stage_action": row["stage_action"],
            }
        )
    blocked = bool(refused) or not report.valid
    return {
        **schema.base_report(schema.SCHEMA_EVENT),
        "valid": report.valid and not refused,
        "blocked": blocked,
        "catalogue_rows": len(index),
        "results": results,
        "applied_actions": sorted(applied),
        "duplicate_noops": sorted(duplicates),
        "refused": sorted(refused),
        "issues": [issue.as_dict() for issue in report.issues],
        "not_verifiable": list(schema.NOT_VERIFIABLE),
    }


def validate(document: typing.Mapping[str, object]) -> typing.Dict[str, object]:
    return validate_events(document)
