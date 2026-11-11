"""C3.5 inbox configuration identity and disabled zero-activity evidence.

The inbox is optional.  Its supported/enabled values are explicit booleans;
missing, whitespace, non-boolean or auto-enabled configuration is refused.  A
disabled claim requires an end-to-end observation (not just a static config)
and all seven activity fields false.  Enabling needs separate authority and is
out of scope here.  No service, queue, dependency or telemetry is added.
"""

from __future__ import annotations

import typing

from . import schema

CONFIG_FIELDS = ("inbox.supported", "inbox.enabled")
ACTIVITY_FIELDS = (
    "polling",
    "handshake",
    "external_reporting",
    "background_task",
    "network",
    "provider_call",
    "queue_activity",
)
EVIDENCE_FIELDS = (
    "kind",
    "disabled_run_ref",
    "activity",
    "observed_at",
    "source_ref",
    "independent_confirmation_ref",
)
TOP_FIELDS = (
    "schema_version",
    "config",
    "selected_by",
    "config_identity",
    "evidence",
    "local_path_evidence",
    "display_state",
    "authority_ref",
    "dependencies",
)
DISABLED_DISPLAY = "inbox disabled - zero associated activity"


def _check_config(
    config: object, report: schema.Report
) -> typing.Optional[typing.Dict[str, object]]:
    checked = schema.check_object(config, "config", CONFIG_FIELDS, (), report)
    if checked is None:
        return None
    for field in CONFIG_FIELDS:
        value = checked.get(field)
        if not schema.is_bool(value):
            report.add(
                "INBOX_CONFIG_INVALID",
                "config.%s must be an explicit boolean, not %r" % (field, value),
            )
    supported = checked.get("inbox.supported")
    enabled = checked.get("inbox.enabled")
    if enabled is True and supported is not True:
        report.add(
            "INBOX_ENABLED_WITHOUT_SUPPORT",
            "inbox.enabled=true requires inbox.supported=true",
        )
    return checked


def validate(document: typing.Mapping[str, object]) -> typing.Dict[str, object]:
    report = schema.Report()
    schema.check_schema_version(document, schema.SCHEMA_INBOX, report)
    schema.check_object(document, "inbox record", TOP_FIELDS, (), report)
    config = _check_config(document.get("config"), report)
    schema.check_string(document.get("selected_by"), "selected_by", report)
    schema.check_string(document.get("config_identity"), "config_identity", report)
    identity = document.get("config_identity")
    if config is not None and schema.is_nonempty_str(identity):
        expected = schema.digest(config)
        if identity != expected:
            report.add(
                "INBOX_CONFIG_IDENTITY_MISMATCH",
                "config_identity does not recompute from the explicit config",
            )
    schema.check_string(
        document.get("local_path_evidence"), "local_path_evidence", report
    )
    display = document.get("display_state")
    schema.check_string(display, "display_state", report)
    if isinstance(display, str) and display.lower() != DISABLED_DISPLAY:
        report.add(
            "INBOX_DISPLAY_INVALID",
            "disabled display must read %r" % DISABLED_DISPLAY,
        )
    authority = document.get("authority_ref")
    enabled = config.get("inbox.enabled") if config is not None else None
    if enabled is True:
        if not schema.is_nonempty_str(authority):
            report.add(
                "INBOX_ENABLED_WITHOUT_AUTHORITY",
                "enabling the inbox needs a separate authority ref; this slice does not grant it",
            )
    elif enabled is False:
        if authority not in (None, ""):
            report.add(
                "INBOX_DISABLED_WITH_AUTHORITY",
                "a disabled inbox does not need, and must not claim, an enabling authority",
            )
    dependencies = document.get("dependencies")
    if not isinstance(dependencies, list):
        report.add("INBOX_DEPENDENCIES_INVALID", "dependencies must be a list")
        dependencies = []
    if dependencies:
        report.add(
            "INBOX_NEW_DEPENDENCY",
            "the inbox must add no service/queue/provider dependency: %s"
            % ", ".join(str(item) for item in dependencies),
        )
    evidence = document.get("evidence")
    checked_evidence = schema.check_object(
        evidence, "evidence", EVIDENCE_FIELDS, (), report
    )
    activity: typing.Dict[str, object] = {}
    zero_activity = False
    if checked_evidence is not None:
        schema.check_string(checked_evidence.get("kind"), "evidence.kind", report)
        if checked_evidence.get("kind") != "END_TO_END_OBSERVATION":
            report.add(
                "INBOX_EVIDENCE_NOT_END_TO_END",
                "a disabled zero-activity claim needs END_TO_END_OBSERVATION, not static config",
            )
        schema.check_string(
            checked_evidence.get("disabled_run_ref"),
            "evidence.disabled_run_ref",
            report,
        )
        schema.check_string(checked_evidence.get("source_ref"), "evidence.source_ref", report)
        schema.check_iso(checked_evidence.get("observed_at"), "evidence.observed_at", report)
        schema.check_string(
            checked_evidence.get("independent_confirmation_ref"),
            "evidence.independent_confirmation_ref",
            report,
        )
        checked_activity = schema.check_object(
            checked_evidence.get("activity"), "evidence.activity", ACTIVITY_FIELDS, (), report
        )
        if checked_activity is not None:
            activity = checked_activity
            for field in ACTIVITY_FIELDS:
                value = checked_activity.get(field)
                if not schema.is_bool(value):
                    report.add(
                        "INBOX_ACTIVITY_INVALID",
                        "evidence.activity.%s must be a boolean" % field,
                    )
            zero_activity = all(checked_activity.get(field) is False for field in ACTIVITY_FIELDS)
            if enabled is False:
                for field in ACTIVITY_FIELDS:
                    if checked_activity.get(field) is not False:
                        report.add(
                            "INBOX_HIDDEN_ACTIVITY",
                            "inbox disabled but evidence.activity.%s is not false" % field,
                        )
    if enabled is False and not zero_activity:
        report.add(
            "INBOX_ZERO_ACTIVITY_UNPROVEN",
            "disabled inbox needs an observed all-false activity record",
        )
    return {
        **schema.base_report(schema.SCHEMA_INBOX),
        "valid": report.valid,
        "blocked": not report.valid,
        "enabled": enabled,
        "display_state": display,
        "zero_activity_observed": zero_activity,
        "activity": activity,
        "issues": [issue.as_dict() for issue in report.issues],
        "not_verifiable": list(schema.NOT_VERIFIABLE),
    }
