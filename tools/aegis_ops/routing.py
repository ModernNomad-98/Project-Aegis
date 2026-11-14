"""C3.2 dependency-aware path/check routing and the bounded E1 invariants.

The matrix is closed over the six existing workflow checks.  'validate-skills'
and 'gate-guard' are required and can never be routed away; an unmapped path
fails closed.  The workflow analyser checks the E1 edit's bounded shape
(routing/path-scope only): job set, required-job unconditionality, the push
lane forcing every output true, the closed 'docs_skills' predicate, per-job
advisory routing and pinned
actions.  It does not write the workflow and it makes no settings or
required-context claim.
"""

from __future__ import annotations

import fnmatch
import os
import re
import typing

from . import schema

CHECKS = (
    "changes",
    "validate-skills",
    "gate-guard",
    "windows-offline-checks",
    "tools-tests-linux",
    "tools-tests-windows",
)
REQUIRED_CHECKS = ("gate-guard", "validate-skills")
ADVISORY_CHECKS = ("windows-offline-checks", "tools-tests-linux", "tools-tests-windows")
ROW_FIELDS = (
    "check",
    "required",
    "inputs",
    "min_affected_set",
    "legitimate_passing_path",
    "never_skip",
    "push_lane_behaviour",
)
MATRIX_FIELDS = ("schema_version", "rows", "changed_paths")


def path_matches(pattern: str, path: str) -> bool:
    """Match one repository-relative path against one matrix input pattern."""

    if pattern == "**":
        return True
    if pattern.endswith("/**"):
        return path == pattern[:-3] or path.startswith(pattern[:-3] + "/")
    return fnmatch.fnmatchcase(path, pattern)


def _validate_rows(
    rows: typing.Any, report: schema.Report
) -> typing.List[typing.Dict[str, object]]:
    if not isinstance(rows, list) or not rows:
        report.add("ROUTING_ROWS_MISSING", "rows must be a non-empty list")
        return []
    seen: typing.Set[str] = set()
    valid_rows: typing.List[typing.Dict[str, object]] = []
    for position, row in enumerate(rows):
        where = "rows[%d]" % position
        checked = schema.check_object(row, where, ROW_FIELDS, (), report)
        if checked is None:
            continue
        name = schema.check_enum(checked.get("check"), where + ".check", CHECKS, report)
        if name in seen:
            report.add("ROUTING_DUPLICATE_ROW", "%s repeats %s" % (where, name))
        seen.add(str(name))
        inputs = checked.get("inputs")
        if not isinstance(inputs, list) or not inputs or any(
            not isinstance(value, str) or not value for value in inputs
        ):
            report.add("ROUTING_INPUTS_INVALID", "%s.inputs must be a non-empty string list" % where)
        for field in ("min_affected_set", "legitimate_passing_path", "push_lane_behaviour"):
            schema.check_string(checked.get(field), where + "." + field, report)
        required = checked.get("required")
        never_skip = checked.get("never_skip")
        if not schema.is_bool(required):
            report.add("ROUTING_REQUIRED_INVALID", "%s.required must be a boolean" % where)
        if not schema.is_bool(never_skip):
            report.add("ROUTING_NEVER_SKIP_INVALID", "%s.never_skip must be a boolean" % where)
        if name in REQUIRED_CHECKS:
            if required is not True or never_skip is not True:
                report.add(
                    "ROUTING_REQUIRED_CHECK_SKIPPABLE",
                    "%s is a required check and must set required=true and never_skip=true"
                    % name,
                )
            if isinstance(inputs, list) and "**" not in inputs:
                report.add(
                    "ROUTING_REQUIRED_CHECK_UNMAPPED",
                    "%s must claim the full changed-path surface (**)" % name,
                )
        elif name in ADVISORY_CHECKS and required is True:
            report.add(
                "ROUTING_ADVISORY_MARKED_REQUIRED",
                "%s is an advisory job and cannot be declared a required context" % name,
            )
        valid_rows.append(checked)
    missing = sorted(set(CHECKS) - seen)
    if missing:
        report.add("ROUTING_CHECK_MISSING", "matrix omits existing check(s): %s" % ", ".join(missing))
    return valid_rows


def validate_matrix(document: typing.Mapping[str, object]) -> typing.Dict[str, object]:
    report = schema.Report()
    schema.check_schema_version(document, schema.SCHEMA_ROUTING, report)
    schema.check_object(document, "routing matrix", MATRIX_FIELDS, (), report)
    rows = _validate_rows(document.get("rows"), report)
    changed = document.get("changed_paths")
    paths: typing.List[str] = []
    if not isinstance(changed, list) or not changed:
        report.add("ROUTING_PATHS_MISSING", "changed_paths must be a non-empty list")
    elif any(not isinstance(path, str) or not path for path in changed):
        report.add("ROUTING_PATH_INVALID", "changed_paths must contain non-empty strings")
    else:
        for path in changed:
            if os.path.isabs(path) or path.startswith("../") or "/../" in path:
                report.add("ROUTING_PATH_ESCAPES", "changed path %r is not repository-relative" % path)
            else:
                paths.append(path)
    affected: typing.Dict[str, typing.List[str]] = {}
    unmapped: typing.List[str] = []
    for path in paths:
        matched = sorted(
            str(row["check"])
            for row in rows
            if isinstance(row.get("inputs"), list)
            and any(path_matches(str(pattern), path) for pattern in row["inputs"])
        )
        affected[path] = matched
        if not matched:
            unmapped.append(path)
            report.add(
                "ROUTING_UNMAPPED_PATH",
                "changed path %r matches no matrix row (fails closed)" % path,
            )
            continue
        missing_required = sorted(set(REQUIRED_CHECKS) - set(matched))
        if missing_required:
            report.add(
                "ROUTING_REQUIRED_CHECK_ROUTED_AWAY",
                "changed path %r would skip required check(s): %s"
                % (path, ", ".join(missing_required)),
            )
    docs_skills = schema.classify_docs_skills(paths)
    affected_union: typing.Set[str] = set()
    for checks in affected.values():
        affected_union.update(checks)
    skipped_advisory = sorted(
        check for check in ADVISORY_CHECKS if check not in affected_union
    )
    return {
        **schema.base_report(schema.SCHEMA_ROUTING),
        "valid": report.valid,
        "changed_paths": paths,
        "affected_checks": affected,
        "unmapped_paths": sorted(unmapped),
        "required_checks": list(REQUIRED_CHECKS),
        "required_always_run": not report.issues,
        "docs_skills": docs_skills,
        "skipped_advisory": skipped_advisory,
        "issues": [issue.as_dict() for issue in report.issues],
        "not_verifiable": list(schema.NOT_VERIFIABLE),
    }


def _jobs(text: str) -> typing.Dict[str, typing.List[str]]:
    """Split the workflow's jobs block into name -> lines (shallow parse)."""

    lines = text.splitlines()
    jobs: typing.Dict[str, typing.List[str]] = {}
    in_jobs = False
    current: typing.Optional[str] = None
    for line in lines:
        if line.rstrip() == "jobs:":
            in_jobs = True
            continue
        if not in_jobs:
            continue
        if line and not line.startswith(" "):
            break
        if (
            line.startswith("  ")
            and not line.startswith("    ")
            and line.rstrip().endswith(":")
            and not line.strip().startswith("#")
        ):
            name = line.strip()[:-1]
            current = name
            jobs[name] = []
            continue
        if current is not None:
            jobs[current].append(line)
    return jobs


def _job_if(lines: typing.List[str]) -> typing.Optional[str]:
    for line in lines:
        if line.startswith("    if:") and not line.startswith("      "):
            return line.split("if:", 1)[1].strip()
    return None


def check_workflow_text(text: str) -> typing.Dict[str, object]:
    """Check the bounded E1 shape of the validate-skills workflow."""

    report = schema.Report()
    jobs = _jobs(text)
    expected_jobs = set(CHECKS)
    if set(jobs) != expected_jobs:
        report.add(
            "E1_JOB_SET_CHANGED",
            "job set must stay %s, not %s" % (sorted(expected_jobs), sorted(jobs)),
        )
    if "if:" in text.split("jobs:", 1)[0]:
        report.add("E1_TOP_LEVEL_IF", "no top-level if: may be added")
    if "pull_request:" not in text or "types: [opened, synchronize, reopened, edited]" not in text:
        report.add("E1_TRIGGER_CHANGED", "pull_request trigger/types must be retained")
    if "push:" not in text or "branches:" not in text:
        report.add("E1_PUSH_TRIGGER_CHANGED", "push-to-main trigger must be retained")
    if "contents: read" not in text:
        report.add("E1_PERMISSIONS_CHANGED", "contents: read must be retained")
    if re.search(r"(?m)^\s*continue-on-error:\s*true\s*$", text):
        report.add("E1_CONTINUE_ON_ERROR", "continue-on-error may not be introduced")
    changes_job_text = "\n".join(jobs.get("changes", []))
    if "docs_skills: $" not in changes_job_text:
        report.add("E1_DOCS_SKILLS_OUTPUT", "the changes job must expose docs_skills")
    for name in ("tools", "offline", "docs_skills"):
        expected_output = ("%s: $" + "{{ steps.filter.outputs.%s }}") % (name, name)
        if expected_output not in "\n".join(jobs.get("changes", [])):
            report.add("E1_OUTPUT_MISSING", "changes.outputs.%s is missing" % name)
    validate_if = _job_if(jobs.get("validate-skills", []))
    if validate_if is not None:
        report.add("E1_REQUIRED_VALIDATE_CONDITIONAL", "validate-skills must stay unconditional")
    gate_if = _job_if(jobs.get("gate-guard", []))
    if gate_if != "github.event_name == 'pull_request'":
        report.add(
            "E1_GATE_GUARD_CONDITION",
            "gate-guard must stay pull-request-only (unchanged), not %r" % gate_if,
        )
    for name in ADVISORY_CHECKS:
        job_text = "\n".join(jobs.get(name, []))
        is_tools_job = name in ("tools-tests-linux", "tools-tests-windows")
        if is_tools_job and "needs.changes.outputs.docs_skills != 'true'" in job_text:
            report.add(
                "E1_ADVISORY_TOOLS_DOCS_SKIP",
                "%s must not carry the docs_skills skip: a schema-only PR sets "
                "tools=true and docs_skills=true and must still run" % name,
            )
        condition = _job_if(jobs.get(name, []))
        if condition is None or not condition.startswith("github.event_name == 'push'"):
            report.add("E1_ADVISORY_PUSH_LANE", "%s must still run on push" % name)
            continue
        if name == "windows-offline-checks":
            if "needs.changes.outputs.offline == 'true'" not in condition:
                report.add("E1_ADVISORY_ROUTE", "%s must route on offline" % name)
            if "needs.changes.outputs.docs_skills != 'true'" not in job_text:
                report.add("E1_ADVISORY_DOCS_SKIP", "%s must skip docs/skills-only PRs" % name)
        elif "needs.changes.outputs.tools == 'true'" not in condition:
            report.add("E1_ADVISORY_ROUTE", "%s must route on tools" % name)
    changes_text = "\n".join(jobs.get("changes", []))
    for token in ("tools=true", "offline=true", "docs_skills=true"):
        if token not in changes_text:
            report.add("E1_PUSH_FORCES_OUTPUT", "push lane must force %s" % token)
    if r"grep -Ev '^(docs/|\.claude/skills/)'" not in changes_text:
        report.add("E1_DOCS_SKILLS_PREDICATE", "the closed docs_skills predicate is missing")
    uses = [
        line.strip()
        for line in text.splitlines()
        if line.strip().startswith(("uses:", "- uses:"))
    ]
    for use in uses:
        ref = use.split("@", 1)[1].split("#", 1)[0].strip() if "@" in use else ""
        if not schema.HEX40_RE.match(ref):
            report.add("E1_ACTION_UNPINNED", "action is not pinned to a 40-hex commit: %s" % use)
    normalised = " ".join(text.lower().split())
    if "next-to-merge" not in normalised or "final base" not in normalised:
        report.add("E1_BASE_COMMENT_MISSING", "the next-to-merge/final-base comment is missing")
    return {
        **schema.base_report(schema.SCHEMA_ROUTING),
        "valid": report.valid,
        "jobs": sorted(jobs),
        "issues": [issue.as_dict() for issue in report.issues],
        "not_verifiable": list(schema.NOT_VERIFIABLE),
    }


def check_workflow(path: str) -> typing.Dict[str, object]:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            text = handle.read()
    except OSError as error:
        report = schema.Report()
        report.add("E1_WORKFLOW_UNREADABLE", "cannot read %s: %s" % (path, error))
        return {
            **schema.base_report(schema.SCHEMA_ROUTING),
            "valid": False,
            "issues": [i.as_dict() for i in report.issues],
        }
    result = check_workflow_text(text)
    result["workflow_path"] = path
    return result


def validate(document: typing.Mapping[str, object]) -> typing.Dict[str, object]:
    return validate_matrix(document)
