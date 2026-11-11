"""C4.2 R9 metric computation and C4.1 support-matrix checks.

The pilot is the existing five-change pilot: the first three eligible cases are
the baseline/checkpoint and all five are the final comparison.  There is no
separate pilot and no new telemetry.  Every number names its source and
denominator; active/owner time is UNKNOWN unless it was actually instrumented;
dollars are refused unless a measured invoice figure is supplied; a shortfall
is reported, never filled or dated.

The support-matrix check is evidence-only: T5 mounted coverage is not assumed,
a simulated host is never counted, and a QUALIFIED cell needs a real evidence
identity and an independence statement.
"""

from __future__ import annotations

import typing

from . import schema

MEASURE_SHEET_FIELDS = ("definitions", "denominators")
CASE_FIELDS = (
    "change_id",
    "case_ordinal",
    "eligible",
    "candidate_heads",
    "head_exception",
    "review_rounds",
    "stage_elapsed",
    "active_vs_wait",
    "audit_suite_minutes",
    "reuse_events",
    "exceptions_bypasses",
    "owner_touches",
    "defects",
    "triage_categories",
    "unrun",
    "dispositions",
)
CASE_OPTIONAL = ("measured_cost",)
PILOT_FIELDS = ("schema_version", "as_of", "measure_sheet", "cases", "cap_tuning")
STAGES = ("B", "D", "E", "F")
HEAD_LIMIT = 3
PILOT_TARGET = 5
MATRIX_FIELDS = ("schema_version", "as_of", "rows", "simulated_host_counted")
MATRIX_ROW_FIELDS = (
    "configuration",
    "claim",
    "prerequisites",
    "evidence_identity",
    "assurance_class",
    "independence",
    "limitations",
    "permitted_next_action",
)
REQUIRED_CONFIGURATIONS = (
    "mode A one-agent/no-inbox",
    "optional subagent",
    "bounded real multi-platform handoff",
    "selected inbox when authorised",
    "inbox-disabled zero activity",
    "recovery/status states",
)


def _check_number(value: object, where: str, report: schema.Report) -> typing.Optional[float]:
    if not schema.is_number(value) or value < 0:
        report.add("METRIC_NUMBER_INVALID", "%s must be a non-negative number" % where)
        return None
    return float(value)


def _check_string_list(value: object, where: str, report: schema.Report) -> typing.List[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        report.add("METRIC_LIST_INVALID", "%s must be a non-empty-string list" % where)
        return []
    return list(value)


def _check_case(
    case: typing.Any, report: schema.Report, position: int
) -> typing.Optional[typing.Dict[str, object]]:
    where = "cases[%d]" % position
    checked = schema.check_object(case, where, CASE_FIELDS, CASE_OPTIONAL, report)
    if checked is None:
        return None
    schema.check_string(checked.get("change_id"), where + ".change_id", report)
    ordinal = checked.get("case_ordinal")
    if not schema.is_int(ordinal) or ordinal < 1:
        report.add("METRIC_ORDINAL_INVALID", "%s.case_ordinal must be an integer >= 1" % where)
    eligible = checked.get("eligible")
    if not schema.is_bool(eligible):
        report.add("METRIC_ELIGIBLE_INVALID", "%s.eligible must be a boolean" % where)
    heads = checked.get("candidate_heads")
    head_list: typing.List[str] = []
    if not isinstance(heads, list) or not heads:
        report.add("METRIC_HEADS_INVALID", "%s.candidate_heads must be a non-empty list" % where)
    else:
        for index, head in enumerate(heads):
            if not isinstance(head, str) or not schema.HEX40_RE.match(head):
                report.add(
                    "METRIC_HEAD_INVALID",
                    "%s.candidate_heads[%d] must be a 40-hex head" % (where, index),
                )
            else:
                head_list.append(head)
    exception = checked.get("head_exception")
    if len(head_list) > HEAD_LIMIT:
        if not isinstance(exception, dict):
            report.add(
                "HEAD_BUDGET_EXCEPTION_MISSING",
                "%s has %d heads; a fourth head needs a recorded scoped exception"
                % (where, len(head_list)),
            )
        else:
            for field in ("exception_ref", "blocking_finding_ref", "authority_ref"):
                schema.check_string(
                    exception.get(field), where + ".head_exception." + field, report
                )
    elif exception not in (None, {}):
        report.add(
            "HEAD_BUDGET_EXCEPTION_UNUSED",
            "%s records a fourth-head exception without a fourth head" % where,
        )
    rounds = checked.get("review_rounds")
    checked_rounds = schema.check_object(
        rounds,
        where + ".review_rounds",
        STAGES + ("automated_submissions",),
        (),
        report,
    )
    if checked_rounds is not None:
        for field in STAGES + ("automated_submissions",):
            value = checked_rounds.get(field)
            if not schema.is_int(value) or value < 0:
                report.add(
                    "METRIC_ROUND_INVALID",
                    "%s.review_rounds.%s must be an integer >= 0" % (where, field),
                )
    elapsed = checked.get("stage_elapsed")
    if not isinstance(elapsed, dict) or any(
        not isinstance(key, str) or not (schema.is_number(value) or value == "UNKNOWN")
        for key, value in elapsed.items()
    ):
        report.add(
            "METRIC_STAGE_ELAPSED_INVALID",
            "%s.stage_elapsed must map stage names to minutes or UNKNOWN" % where,
        )
    active = checked.get("active_vs_wait")
    checked_active = schema.check_object(
        active,
        where + ".active_vs_wait",
        ("active", "active_instrumented", "wait_wall_minutes"),
        (),
        report,
    )
    if checked_active is not None:
        ae = checked_active.get("active")
        instrumented = checked_active.get("active_instrumented")
        if not schema.is_bool(instrumented):
            report.add(
                "METRIC_INSTRUMENTED_INVALID",
                "%s.active_vs_wait.active_instrumented must be a boolean" % where,
            )
        if instrumented is True:
            _check_number(ae, where + ".active_vs_wait.active", report)
        elif ae != "UNKNOWN":
            report.add(
                "METRIC_ACTIVE_UNKNOWN_REQUIRED",
                "%s.active_vs_wait.active must be UNKNOWN unless instrumented" % where,
            )
        _check_number(
            checked_active.get("wait_wall_minutes"),
            where + ".active_vs_wait.wait_wall_minutes",
            report,
        )
    suite = checked.get("audit_suite_minutes")
    checked_suite = schema.check_object(
        suite,
        where + ".audit_suite_minutes",
        ("value", "definition", "source"),
        (),
        report,
    )
    if checked_suite is not None:
        _check_number(checked_suite.get("value"), where + ".audit_suite_minutes.value", report)
        schema.check_string(
            checked_suite.get("definition"), where + ".audit_suite_minutes.definition", report
        )
        schema.check_string(
            checked_suite.get("source"), where + ".audit_suite_minutes.source", report
        )
    for field in ("reuse_events", "exceptions_bypasses", "defects", "unrun", "dispositions"):
        _check_string_list(checked.get(field), where + "." + field, report)
    owner = checked.get("owner_touches")
    checked_owner = schema.check_object(
        owner,
        where + ".owner_touches",
        ("observable", "latency"),
        ("latency_instrumented",),
        report,
    )
    if checked_owner is not None:
        if not schema.is_int(checked_owner.get("observable")) or checked_owner.get("observable") < 0:
            report.add(
                "METRIC_OWNER_TOUCH_INVALID",
                "%s.owner_touches.observable must be an integer >= 0" % where,
            )
        latency = checked_owner.get("latency")
        if checked_owner.get("latency_instrumented") is True:
            _check_number(latency, where + ".owner_touches.latency", report)
        elif latency != "UNKNOWN":
            report.add(
                "METRIC_OWNER_LATENCY_UNKNOWN_REQUIRED",
                "%s.owner_touches.latency must be UNKNOWN unless instrumented" % where,
            )
    triage = checked.get("triage_categories")
    if not isinstance(triage, dict) or any(
        not isinstance(key, str) or not schema.is_int(value) or value < 0
        for key, value in triage.items()
    ):
        report.add(
            "METRIC_TRIAGE_INVALID",
            "%s.triage_categories must map categories to integer counts" % where,
        )
    measured = checked.get("measured_cost")
    if measured is not None:
        checked_cost = schema.check_object(
            measured,
            where + ".measured_cost",
            ("amount", "currency", "invoice_ref"),
            (),
            report,
        )
        if checked_cost is not None:
            _check_number(checked_cost.get("amount"), where + ".measured_cost.amount", report)
            schema.check_string(
                checked_cost.get("invoice_ref"), where + ".measured_cost.invoice_ref", report
            )
    return checked


def validate_pilot(document: typing.Mapping[str, object]) -> typing.Dict[str, object]:
    report = schema.Report()
    schema.check_schema_version(document, schema.SCHEMA_PILOT_METRICS, report)
    schema.check_object(document, "pilot metrics", PILOT_FIELDS, (), report)
    schema.check_iso(document.get("as_of"), "as_of", report)
    sheet = schema.check_object(
        document.get("measure_sheet"), "measure_sheet", MEASURE_SHEET_FIELDS, (), report
    )
    if sheet is not None:
        if not isinstance(sheet.get("definitions"), dict) or not sheet.get("definitions"):
            report.add("MEASURE_DEFINITIONS_MISSING", "measure_sheet.definitions must be a non-empty object")
        if not isinstance(sheet.get("denominators"), dict) or not sheet.get("denominators"):
            report.add("MEASURE_DENOMINATORS_MISSING", "measure_sheet.denominators must be a non-empty object")
    cases = document.get("cases")
    if not isinstance(cases, list):
        report.add("PILOT_CASES_INVALID", "cases must be a list")
        cases = []
    checked_cases: typing.List[typing.Dict[str, object]] = []
    for position, case in enumerate(cases):
        checked = _check_case(case, report, position)
        if checked is not None:
            checked_cases.append(checked)
    ordinals = [case.get("case_ordinal") for case in checked_cases]
    if len(set(ordinals)) != len(ordinals):
        report.add("PILOT_ORDINALS_DUPLICATE", "case_ordinal values must be unique")
    for case in checked_cases:
        for key in case:
            if key in ("dollars", "dollar_savings", "hours_saved", "delay_hours"):
                report.add(
                    "METRIC_DOLLAR_OR_DELAY_INVENTED",
                    "unmeasured dollar/delay field %r is forbidden" % key,
                )
    eligible = [case for case in checked_cases if case.get("eligible") is True]
    baseline_count = min(3, len(eligible))
    shortfall = len(eligible) < PILOT_TARGET
    heads_total = sum(len(case.get("candidate_heads") or []) for case in eligible)
    rounds_total = {stage: 0 for stage in STAGES}
    suite_total = 0.0
    unknown_active = 0
    for case in eligible:
        rounds = case.get("review_rounds")
        if isinstance(rounds, dict):
            for stage in STAGES:
                value = rounds.get(stage)
                if schema.is_int(value):
                    rounds_total[stage] += value
        suite = case.get("audit_suite_minutes")
        if isinstance(suite, dict) and schema.is_number(suite.get("value")):
            suite_total += float(suite["value"])
        active = case.get("active_vs_wait")
        if isinstance(active, dict) and active.get("active") == "UNKNOWN":
            unknown_active += 1
    cap_tuning = document.get("cap_tuning")
    if cap_tuning is None:
        cap_tuning = []
    if not isinstance(cap_tuning, list) or cap_tuning:
        report.add(
            "CAP_TUNING_FORBIDDEN",
            "the five cases may tune the rubric, never the caps; cap_tuning must be empty",
        )
    return {
        **schema.base_report(schema.SCHEMA_PILOT_METRICS),
        "valid": report.valid,
        "eligible_cases": len(eligible),
        "baseline_cases": baseline_count,
        "final_cases": len(eligible),
        "pilot_target": PILOT_TARGET,
        "bounded_shortfall": shortfall,
        "shortfall": {
            "reported": shortfall,
            "eligible": len(eligible),
            "required": PILOT_TARGET,
            "reason": "EXTERNAL_WAIT_NO_INVENTED_CASES" if shortfall else None,
        },
        "heads_total": heads_total,
        "review_rounds_total": rounds_total,
        "audit_suite_minutes_total": round(suite_total, 3),
        "active_unknown_cases": unknown_active,
        "no_cap_tuning": True,
        "issues": [issue.as_dict() for issue in report.issues],
        "not_verifiable": list(schema.NOT_VERIFIABLE),
    }


def validate_support_matrix(document: typing.Mapping[str, object]) -> typing.Dict[str, object]:
    report = schema.Report()
    schema.check_schema_version(document, schema.SCHEMA_SUPPORT_MATRIX, report)
    schema.check_object(
        document, "support matrix", MATRIX_FIELDS, ("t5_mounted_coverage",), report
    )
    schema.check_iso(document.get("as_of"), "as_of", report)
    simulated = document.get("simulated_host_counted")
    if simulated is not False:
        report.add(
            "MATRIX_SIMULATED_HOST_COUNTED",
            "a simulated host is never counted as qualification evidence",
        )
    if "t5_mounted_coverage" in document:
        if document.get("t5_mounted_coverage") not in ("NOT_ASSUMED", "UNRUN"):
            report.add("MATRIX_T5_OVERCLAIM", "T5 mounted coverage is not assumed in this slice")
    rows = document.get("rows")
    if not isinstance(rows, list) or not rows:
        report.add("MATRIX_ROWS_MISSING", "rows must be a non-empty list")
        rows = []
    seen: typing.List[str] = []
    for position, row in enumerate(rows):
        where = "rows[%d]" % position
        checked = schema.check_object(row, where, MATRIX_ROW_FIELDS, (), report)
        if checked is None:
            continue
        for field in MATRIX_ROW_FIELDS:
            if field != "assurance_class":
                schema.check_string(checked.get(field), where + "." + field, report)
        configuration = checked.get("configuration")
        if isinstance(configuration, str):
            seen.append(configuration)
        assurance = schema.check_enum(
            checked.get("assurance_class"),
            where + ".assurance_class",
            schema.ASSURANCE_CLASSES,
            report,
        )
        evidence = checked.get("evidence_identity")
        if assurance == "QUALIFIED":
            if not schema.is_nonempty_str(evidence) or evidence in ("UNRUN", "UNKNOWN"):
                report.add(
                    "MATRIX_QUALIFIED_WITHOUT_EVIDENCE",
                    "%s is QUALIFIED without a real evidence identity" % where,
                )
            independence = checked.get("independence")
            if not schema.is_nonempty_str(independence) or independence in ("UNRUN", "UNKNOWN"):
                report.add(
                    "MATRIX_QUALIFIED_WITHOUT_INDEPENDENCE",
                    "%s is QUALIFIED without an independence record" % where,
                )
        if assurance in ("UNRUN", "UNKNOWN") and schema.is_nonempty_str(evidence) and evidence not in ("UNRUN", "UNKNOWN", "NONE"):
            report.add(
                "MATRIX_UNRUN_WITH_EVIDENCE",
                "%s is %s but cites evidence; a cell is not both" % (where, assurance),
            )
    missing = sorted(set(REQUIRED_CONFIGURATIONS) - set(seen))
    if missing:
        report.add(
            "MATRIX_CONFIGURATION_MISSING",
            "support matrix omits configuration/claim(s): %s" % ", ".join(missing),
        )
    return {
        **schema.base_report(schema.SCHEMA_SUPPORT_MATRIX),
        "valid": report.valid,
        "rows": len(rows),
        "qualified": sum(1 for row in rows if isinstance(row, dict) and row.get("assurance_class") == "QUALIFIED"),
        "unrun": sum(1 for row in rows if isinstance(row, dict) and row.get("assurance_class") == "UNRUN"),
        "t5_mounted_coverage": document.get("t5_mounted_coverage", "NOT_ASSUMED"),
        "issues": [issue.as_dict() for issue in report.issues],
        "not_verifiable": list(schema.NOT_VERIFIABLE),
    }


def validate(document: typing.Mapping[str, object]) -> typing.Dict[str, object]:
    if document.get("schema_version") == schema.SCHEMA_SUPPORT_MATRIX:
        return validate_support_matrix(document)
    return validate_pilot(document)
