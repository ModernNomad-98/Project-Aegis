"""Read-only CI-run duration reader for one GitHub Actions run.

The delivery-control kernel is offline and synthetic. This module is its one
deliberate, opt-in exception: it reads public GitHub run metadata over HTTPS
and prints evidence to stdout. It writes no file, calls no mutating verb,
downloads no artifact, never invokes `gh`, and can contact exactly one host
(`api.github.com`) because no argument exists that selects another.

Three honesty rules are load-bearing and explain the shape of this module:

* **conclusion-first state (D15).** A job is skipped or executed because of
  its API `conclusion`, never because of its timestamp window. A skipped job
  carries `not_applicable` whatever its window looks like (-1 s, 0 s, null
  or absent).
* **fail closed (D16, D24).** A missing job, an unresolved conclusion, a
  missing timestamp on an executed row, a red run, an executed job that is
  not green, a job the event makes required but the API reports skipped, and
  a jobs page the API declares longer than the pages actually read all raise
  the status; none is rounded down to a pass.
* **head-bound completeness (D20).** `COMPLETE` and exit 0 require a
  `--candidate` equal to the run head *and* a run payload that records a head
  SHA at all: a candidate that cannot be bound to a run head is
  `candidate_status=unresolvable`, and an unresolvable head is never a pass.

Design: P0-A A2 PLAN revision 2 (D15-D24). Read-only: no POST, PUT, PATCH or
DELETE, no file writes, and nothing on stdout except the chosen rendering.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_REPOSITORY = "ModernNomad-98/Project-Aegis"
DEFAULT_WORKFLOW = "validate-skills.yml"
FIXED_HOST = "api.github.com"
ARTIFACT_RETENTION_DAYS = 14
API_VERSION = "2022-11-28"
USER_AGENT = "aegis-delivery-control-ci-durations"
ESCAPE_MAX_LENGTH = 300
TIMEOUT_SECONDS = 30.0
BACKSLASH = chr(92)

# F3: every separator Python's str.splitlines() recognises must be escaped,
# not only the C0 controls, or a payload string can add a table line and forge
# a status marker. NEXT LINE (U+0085), LINE SEPARATOR (U+2028) and PARAGRAPH
# SEPARATOR (U+2029) are the three above ASCII.
UNICODE_LINE_SEPARATORS = frozenset((0x85, 0x2028, 0x2029))

EXIT_COMPLETE = 0
EXIT_INCOMPLETE = 1
EXIT_REFUSED = 2
EXIT_TRANSPORT = 3
EXIT_FAILED = 4

NOT_RECORDED = "not_recorded"
NOT_APPLICABLE = "not_applicable"
NOT_SELECTED = "not_selected"
NOT_SUPPLIED = "not_supplied"
NONE_UPLOADED = "none_uploaded"

JOB_ROSTER = ("changes", "validate-skills", "gate-guard",
              "windows-offline-checks", "tools-tests-linux",
              "tools-tests-windows")

# D17: literal uploaded artifact names. The suffix -<run_id>-<attempt> is
# stripped before lookup, so a run id containing hyphens cannot be mis-split;
# an unmatched directory is reported not_mapped and never guessed at.
ARTIFACT_JOB_MAP = {"offline-checks-linux": "validate-skills",
                    "offline-checks-windows": "windows-offline-checks",
                    "tools-tests-linux": "tools-tests-linux",
                    "tools-tests-windows": "tools-tests-windows"}

# D15: the conclusion decides; the window never does.
TERMINAL_CONCLUSIONS = frozenset((
    "success", "failure", "cancelled", "timed_out", "action_required",
    "stale", "neutral", "skipped"))
GREEN_CONCLUSIONS = frozenset(("success",))
NON_GREEN_EXECUTED_CONCLUSIONS = frozenset((
    "failure", "cancelled", "timed_out", "action_required", "stale"))

SKIP_REASON_EVENT_FILTER = "event-filter"
SKIP_REASON_DEPENDENCY_FAILED = "dependency-failed"
SKIP_REASON_UNEXPECTED = "unexpected-skip-for-event"

# F2: a job the inspected workflow makes unconditional on an event is a
# prerequisite of that event's run, so its absence is a gap and never a pass.
# `gate-guard` is gated `if: github.event_name == 'pull_request'`
# (.github/workflows/validate-skills.yml L484-493, the `if:` at L493) and is
# one of the two registered required contexts, so a pull_request run may not
# skip it; only a push may, and only as the event filter the workflow itself
# encodes.
#
# N1: the same rule must hold for EVERY roster job, so the allowed-skip set is
# derived from the workflow's own conditions and enforced, not left as dead
# code. `changes` (L57) and `validate-skills` (L106) carry no `if:` at all:
# on both events they always run, and a skip is a gap. `windows-offline-checks`
# (L285-289), `tools-tests-linux` (L378-380) and `tools-tests-windows`
# (L428-430) are `if: github.event_name == 'push' || <flag>`, and on a push the
# `changes` job forces both flags true (L86-89), so on a push those three
# always run and only `gate-guard` may skip; on a pull_request the same three
# may skip when the path filter did not select them. A skipped roster job
# outside its event's set is INCOMPLETE with the job named, never COMPLETE.
REQUIRED_JOBS_BY_EVENT = {"pull_request": ("gate-guard",)}
EXPECTED_SKIPS_BY_EVENT = {
    "push": ("gate-guard",),
    "pull_request": ("windows-offline-checks", "tools-tests-linux",
                     "tools-tests-windows"),
}

# F4: the two PR-only validate-skills steps. Their real state comes from the
# steps the API returned for that job, never from a hard-coded assumption.
PR_ONLY_STEP_NAMES = (
    "Verify DCO sign-off on every commit",
    "pr-body-skills-check")
PR_STEP_LOCATIONS = {
    "Verify DCO sign-off on every commit":
        ".github/workflows/validate-skills.yml L260-267",
    "pr-body-skills-check": ".github/workflows/validate-skills.yml L269-274"}

# F8: page 1 keeps the historical URL; later pages append `&page=N` and are
# requested only while the API keeps advertising an unfetched remainder.
JOBS_PER_PAGE = 100
MAX_JOB_PAGES = 10  # 1000 jobs; beyond this the report is TRUNCATED, never green

IDENTITY_BLOCK = {
    "name": "aegis_delivery_control.ci_durations",
    "command": ("python -m tools.aegis_delivery_control "
                "--repository-id <id> ci-durations"),
    "read_only": True, "writes_files": False, "hosts": [FIXED_HOST],
    "requires_network_flag": True,
    "token_env": ("optional single environment-variable name via --token-env, "
                  "applied only to the fixed host; no token is required"),
    "mutating_verbs": [], "download_artifacts": False, "invokes_gh": False,
    "exit_codes": {
        "0": ("printed and COMPLETE (candidate bound to the run head, green, "
              "no required job skipped, no unexpected skip, no uninspected "
              "jobs)"),
        "1": "printed but STALE, INCOMPLETE or UNBOUND",
        "2": ("refused or unresolvable input (including an --attempt the run "
              "payload cannot confirm)"),
        "3": "transport or API failure",
        "4": "printed but FAILED (run or executed job not green)"},
    "output_formats": ["table", "json"], "network_default": "off"}


class RefusedInput(Exception):
    """The command cannot resolve its inputs; exit 2, no evidence."""


class TransportFailure(Exception):
    """The read failed at the transport or API layer; exit 3."""


class FixtureMiss(RefusedInput):
    """The offline fixture has no payload for a requested URL."""


def identity():
    """Return the fixed command identity block (D21)."""
    return json.loads(json.dumps(IDENTITY_BLOCK))


def escape_text(value) -> str:
    """Escape one payload- or file-derived string (D19, F3, F10).

    Backslash first, then every character that can start a new logical line -
    the ASCII controls, DEL (U+007F) and the Unicode separators U+0085,
    U+2028 and U+2029 - as a hex escape, then the Markdown pipe. The result
    is capped at 300 characters with a visible marker, so no field can
    produce a second output line or forge a row or status marker.

    F10: this is the ONE canonical escape rule, and it is applied in exactly
    one place, `render_table`. The evidence object stores RAW payload
    values; the table is the single escaping pass and never escapes a stored
    string twice. `render_json` serialises those same raw values, so the
    JSON leg is control-safe only through `json.dumps`, which escapes the
    ASCII controls and non-ASCII code points itself. The 300-character cap
    and the pipe escape are table rules and do NOT apply to the JSON
    rendering: D19's "both renderings" wording is a known, disclosed
    deviation, and the JSON is the raw, authoritative record.
    """
    text = "" if value is None else str(value)
    text = text.replace(BACKSLASH, BACKSLASH * 2)
    text = "".join(
        character if character >= " " and character != chr(127)
        and ord(character) not in UNICODE_LINE_SEPARATORS
        else BACKSLASH + "x%02x" % ord(character)
        for character in text)
    text = text.replace("|", BACKSLASH + "|")
    if len(text) > ESCAPE_MAX_LENGTH:
        marker = chr(8230) + "[truncated %d]" % (len(text) - ESCAPE_MAX_LENGTH)
        text = text[:ESCAPE_MAX_LENGTH] + marker
    return text


def _iso(value):
    if not isinstance(value, str) or not value:
        return None
    try:
        moment = datetime.fromisoformat(
            value[:-1] + "+00:00" if value.endswith("Z") else value)
    except ValueError:
        return None
    return moment.astimezone(timezone.utc) if moment.tzinfo else None


def duration_seconds(started_at, completed_at):
    """Integer seconds between two ISO-8601 stamps, or None if unparseable."""
    started, completed = _iso(started_at), _iso(completed_at)
    if started is None or completed is None:
        return None
    return int((completed - started).total_seconds())


def _derive_skip_reason(job_name, event, changes_conclusion):
    """Derive the reason token for a job the API reported as skipped.

    F2/N1: only a job inside EXPECTED_SKIPS_BY_EVENT for this event may be
    called an `event-filter` skip. Any other skip - an unconditional job, or
    a filtered job on the event whose `if:` forces it to run - is
    `unexpected-skip-for-event`, because saying `event-filter` there would
    launder a gap. A skip the failed `changes` prerequisite explains stays
    `dependency-failed`: it is a consequence of that failure, which already
    makes the run FAILED.
    """
    if job_name != "changes" and (
            changes_conclusion in NON_GREEN_EXECUTED_CONCLUSIONS):
        return "%s (changes=%s)" % (SKIP_REASON_DEPENDENCY_FAILED,
                                    changes_conclusion)
    if job_name not in EXPECTED_SKIPS_BY_EVENT.get(event, ()):
        return ("%s (%s is not filter-skippable on event=%s; the marker is "
                "INCOMPLETE)" % (SKIP_REASON_UNEXPECTED, job_name,
                                 event if event else NOT_RECORDED))
    if job_name == "gate-guard":
        return "%s (pull_request-only job)" % SKIP_REASON_EVENT_FILTER
    return "%s (paths did not select it on event=%s)" % (
        SKIP_REASON_EVENT_FILTER,
        event if event else NOT_RECORDED)


def _artifact_text(artifact):
    if not artifact:
        return NONE_UPLOADED
    return "%s (id=%s, bytes=%s, expires=%s, expired=%s)" % (
        artifact.get("name"), artifact.get("id"),
        artifact.get("size_in_bytes"), artifact.get("expires_at"),
        bool(artifact.get("expired")))


def _artifacts_by_job(jobs):
    mapping = {}
    for job in jobs:
        if not isinstance(job, dict):
            continue
        for artifact in job.get("artifacts") or []:
            if isinstance(artifact, dict):
                mapping[artifact.get("name")] = artifact
    return mapping


def _negative_note(seconds):
    return ("executed-negative-window raw=%ds" % seconds if seconds < 0
            else NOT_SELECTED)


def _missing_row(name):
    return {"job": name, "state": "missing", "conclusion": NOT_RECORDED,
            "started_at": NOT_RECORDED, "completed_at": NOT_RECORDED,
            "duration_s": NOT_RECORDED, "duration_provenance": NOT_SELECTED,
            "exit_code": NOT_RECORDED, "exit_code_provenance": NOT_SELECTED,
            "exit_codes": NOT_SELECTED, "exit_codes_provenance": NOT_SELECTED,
            "coverage": "not_demonstrated", "skip_reason": NOT_SELECTED,
            "artifact": NONE_UPLOADED, "log_url": NOT_RECORDED,
            "note": "roster-job-absent-from-api-response"}


def _segments(name):
    parts = name.rsplit("-", 2)
    return parts[0] if len(parts) == 3 and all(
        part.isdigit() for part in parts[1:]) else ""


def run_event_field(event):
    """The recorded-head field this event is expected to carry (F6)."""
    return "pr_head_sha" if event == "pull_request" else "checkout_sha"


def _recorded(record, key):
    """A recorded string field, or an explicit absence marker."""
    value = record.get(key)
    return value if isinstance(value, str) else NOT_RECORDED


def _records_bind(record, run_head_sha, event):
    """F6: which recorded head binds this artifact to the run head?

    `.github/workflows/validate-skills.yml` L256-258 documents that on a
    `pull_request` event the checkout is GitHub's synthetic merge commit, so
    `checkout_sha` (record-check.py L63) is NOT the run head; the run payload
    carries the pull request head, which record-check.py stores separately as
    `pr_head_sha` (L66, fed by workflow L54 `AEGIS_PR_HEAD_SHA`). On a push the
    checkout IS the head, so `checkout_sha` binds.
    """
    key = "pr_head_sha" if event == "pull_request" else "checkout_sha"
    recorded = record.get(key)
    if isinstance(recorded, str) and recorded == run_head_sha:
        return key
    return None


def _exit_codes_text(exit_codes):
    """One rendered cell for a per-job exit-code set (F5)."""
    if not isinstance(exit_codes, list) or not exit_codes:
        return NOT_SELECTED
    return ",".join("%s=%s" % (label, code) for label, code in exit_codes)


def _apply_artifact_exit_codes(rows, run_head_sha, artifact_entries, event):
    """F5/F6: report the whole per-job exit-code SET, bound to the run head.

    A real uploaded directory is written by MANY record-check.py invocations
    (the `offline-checks-linux` artifact is fed by the recorded steps at
    validate-skills.yml L149-243), so promoting one alphabetically first
    record to the whole job row would misreport a job whose later check
    failed. Every record of the directory is examined, every bound record
    contributes its own (label, exit_code) pair, and the singular
    `exit_code` key is filled only when every bound record agrees on one
    code; otherwise it is `not_applicable` and the set carries the truth.
    """
    by_job = {row["job"]: row for row in rows}
    for entry in artifact_entries:
        directory = entry["directory"]
        name = directory.name
        job_name = ARTIFACT_JOB_MAP.get(_segments(name))
        if job_name is None:
            entry["reason"] = "not_mapped"
            continue
        entry["job"] = job_name
        row = by_job[job_name]
        codes, bounded, notes, mismatches, unreadable = [], [], [], [], []
        for record_path in sorted(directory.glob("*.json")):
            try:
                record = json.loads(record_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                unreadable.append("%s: record-unreadable" % record_path.name)
                continue
            if not isinstance(record, dict):
                unreadable.append("%s: record-malformed" % record_path.name)
                continue
            label = record.get("label") or record_path.name
            location = "%s/%s" % (name, record_path.name)
            field = _records_bind(record, run_head_sha, event)
            if field is None:
                mismatches.append("%s: head mismatch (bound field %s, "
                                  "record=%s run=%s)" % (
                                      location, run_event_field(event),
                                      _recorded(record,
                                                run_event_field(event)),
                                      run_head_sha))
                continue
            bounded.append(label)
            exit_code = record.get("exit_code")
            if not isinstance(exit_code, int) or isinstance(exit_code, bool):
                notes.append("%s: record-gap: exit_code" % location)
                continue
            codes.append([label, exit_code])
            notes.append(
                "%s (bound_by=%s, checkout_sha=%s, pr_head_sha=%s, "
                "elapsed_seconds=%s)" % (
                    location, field,
                    _recorded(record, "checkout_sha"),
                    _recorded(record, "pr_head_sha"),
                    record.get("elapsed_seconds")))
        row["exit_codes"] = codes
        row["exit_codes_provenance"] = (" | ".join(notes) if notes
                                        else NOT_SELECTED)
        if mismatches:
            row["exit_code_provenance"] = " | ".join(mismatches)
        elif notes:
            row["exit_code_provenance"] = row["exit_codes_provenance"]
        if codes and len({code for _, code in codes}) == 1 \
                and len(codes) == len(bounded):
            row["exit_code"] = codes[0][1]
        elif bounded:
            row["exit_code"] = NOT_APPLICABLE
        if codes:
            entry["reason"] = "mapped"
        elif mismatches:
            entry["reason"] = "artifact head mismatch"
        elif unreadable:
            entry["reason"] = "record-unreadable"
        else:
            entry["reason"] = "record-gap: exit_code"
        entry["records"] = len(bounded) + len(mismatches) + len(unreadable)
        entry["label"] = ", ".join(label for label, _ in codes) or None
        entry["exit_codes"] = codes



def _derive_job_rows(payload_jobs, run_head_sha, event, artifacts, entries):
    """Build one row per roster job; always len(JOB_ROSTER) rows."""
    by_name = {}
    for job in payload_jobs:
        if isinstance(job, dict) and isinstance(job.get("name"), str):
            by_name.setdefault(job["name"], job)
    changes_conclusion = (by_name.get("changes") or {}).get("conclusion")
    rows = []
    for name in JOB_ROSTER:
        job = by_name.get(name)
        if job is None:
            rows.append(_missing_row(name))
            continue
        conclusion = job.get("conclusion")
        started_at = job.get("started_at")
        completed_at = job.get("completed_at")
        # F10: raw payload values are stored here and escaped by exactly one
        # pass, in render_table; render_json emits these same raw values, so
        # the table never double-escapes a stored string and the JSON stays
        # the raw, authoritative record.
        row = {"job": name,
               "conclusion": conclusion
               if isinstance(conclusion, str) else NOT_RECORDED,
               "started_at": started_at
               if isinstance(started_at, str) else NOT_RECORDED,
               "completed_at": completed_at
               if isinstance(completed_at, str) else NOT_RECORDED,
               "exit_code": NOT_RECORDED, "exit_code_provenance": NOT_SELECTED,
               "exit_codes": NOT_SELECTED, "exit_codes_provenance": NOT_SELECTED,
               "artifact": _artifact_text(artifacts.get(name)),
               "log_url": job.get("html_url")
               if isinstance(job.get("html_url"), str) else NOT_RECORDED,
               "state": NOT_RECORDED, "duration_s": NOT_RECORDED,
               "duration_provenance": NOT_SELECTED, "coverage": "not_demonstrated",
               "skip_reason": NOT_SELECTED, "note": NOT_SELECTED}
        if conclusion == "skipped":
            row.update({"state": "skipped", "duration_s": NOT_APPLICABLE,
                        "duration_provenance": NOT_SELECTED,
                        "coverage": "not_selected",
                        "skip_reason": _derive_skip_reason(
                            name, event, changes_conclusion)})
        elif conclusion in TERMINAL_CONCLUSIONS:
            row["state"] = "executed"
            row["skip_reason"] = NOT_SELECTED
            seconds = duration_seconds(started_at, completed_at)
            if seconds is None:
                row.update({"duration_s": NOT_RECORDED,
                            "duration_provenance": NOT_SELECTED,
                            "coverage": "not_demonstrated",
                            "note": "required-field-gap: timestamp missing"})
            else:
                row.update({"duration_s": 0 if seconds < 0 else seconds,
                            "duration_provenance":
                                "api:jobs.started_at->completed_at",
                            "coverage": "demonstrated",
                            "note": _negative_note(seconds)})
        else:
            row.update({"state": "unresolved", "duration_s": NOT_RECORDED,
                        "duration_provenance": NOT_SELECTED,
                        "coverage": "not_demonstrated",
                        "skip_reason": NOT_SELECTED,
                        "note": "required-field-gap: no terminal conclusion"})
        rows.append(row)
    _apply_artifact_exit_codes(rows, run_head_sha, entries, event)
    return rows


def derive_staleness(candidate_sha, run_head_sha):
    """Return (candidate_status, stale): head binding, or NOT_SUPPLIED."""
    if not candidate_sha:
        return NOT_SUPPLIED, False
    if not isinstance(run_head_sha, str) or not run_head_sha:
        return "unresolvable", False
    if candidate_sha.strip().lower() != run_head_sha.strip().lower():
        return "differs", True
    return "matches", False


def _marker(status, exit_code, reason, failing=(), non_green=(),
            skipped_required=(), unexpected_skips=()):
    return {"status": status, "exit_code": exit_code, "reason": reason,
            "failing_jobs": list(failing), "non_green_jobs": list(non_green),
            "skipped_required_jobs": list(skipped_required),
            "unexpected_skipped_jobs": list(unexpected_skips)}


def _unexpected_skips(rows, event):
    """N1: roster jobs skipped outside their event's allowed-skip set.

    EXPECTED_SKIPS_BY_EVENT is the workflow's own truth (see its comment); a
    job outside that set for this event should have run, so its skip is a
    prerequisite gap. A skip explained by a failed `changes` prerequisite is
    not counted here: that failure is already FAILED on its own and naming the
    dependent jobs twice would misdescribe why they stopped. An unrecorded
    event yields the empty set, so every skip is then unexpected (fail closed).
    """
    changes_conclusion = next(
        (row["conclusion"] for row in rows if row["job"] == "changes"), None)
    dependency_failed = (
        isinstance(changes_conclusion, str)
        and changes_conclusion in NON_GREEN_EXECUTED_CONCLUSIONS)
    allowed = EXPECTED_SKIPS_BY_EVENT.get(event, ())
    return [row["job"] for row in rows
            if row["state"] == "skipped" and row["job"] not in allowed
            and not (dependency_failed and row["job"] != "changes")]


def derive_status(run_identity, rows, roster_delta=(), event=None,
                  truncated=False):
    """Resolve the one honest status marker; first match wins (D16/D20).

    R1, strictest honest reading: the green set is defined positively as
    exactly {success}. A terminal executed job outside it is either a hard
    failure (FAILED, exit 4) or, for the remaining terminal conclusions such
    as neutral, a soft non-green that forces INCOMPLETE and never exit 0.

    F1: `candidate_status == "matches"` is required, not merely `not stale`.
    An unresolvable run head is a gap, not a pass.
    F2: a job the event makes required (REQUIRED_JOBS_BY_EVENT) that the API
    reports as skipped is a prerequisite gap and forces INCOMPLETE.
    N1: any other roster job skipped outside EXPECTED_SKIPS_BY_EVENT for the
    run's event is the same class of gap; every offending job is named in the
    marker and in the reason, so the run can never certify COMPLETE/exit 0.
    F8: a jobs payload that advertises more jobs than the pages read forces
    INCOMPLETE through `truncated` and the named roster_delta entries.
    """
    executed = [row for row in rows if row["state"] == "executed"]
    failing = [row["job"] for row in executed
               if row["conclusion"] in NON_GREEN_EXECUTED_CONCLUSIONS]
    soft = [row["job"] for row in executed
            if row["conclusion"] not in GREEN_CONCLUSIONS
            and row["conclusion"] not in NON_GREEN_EXECUTED_CONCLUSIONS]
    skipped_required = [row["job"] for row in rows
                        if row["state"] == "skipped"
                        and row["job"] in REQUIRED_JOBS_BY_EVENT.get(
                            event, ())]
    unexpected = _unexpected_skips(rows, event)
    run_conclusion = run_identity["run_conclusion"]
    run_red = (run_identity["run_status"] == "completed"
               and isinstance(run_conclusion, str)
               and run_conclusion not in GREEN_CONCLUSIONS)
    if run_red or failing:
        offending = list(failing)
        if run_red and run_conclusion and run_conclusion not in failing:
            offending.append("run_conclusion=%s" % run_conclusion)
        return _marker("FAILED", EXIT_FAILED, "not_green", offending,
                       failing + soft, skipped_required, unexpected)
    if run_identity["candidate_sha"] == NOT_SUPPLIED:
        return _marker("UNBOUND", EXIT_INCOMPLETE, "no_candidate_supplied",
                       (), (), skipped_required, unexpected)
    if run_identity["stale"]:
        return _marker("STALE", EXIT_INCOMPLETE,
                       "candidate_differs_from_run_head", (), (),
                       skipped_required, unexpected)
    blocked = []
    if run_identity["candidate_status"] != "matches":
        # F1: derived from the equality test, never from the `stale` boolean,
        # so "unresolvable" cannot slip through as a head-bound claim.
        blocked.append("candidate_status=%s" % run_identity["candidate_status"])
    reasons = []
    for row in rows:
        if row["state"] in ("missing", "unresolved"):
            reasons.append("%s=%s" % (row["job"], row["state"]))
        elif row["state"] == "executed" and row["duration_s"] == NOT_RECORDED:
            reasons.append("%s=duration_not_recorded" % row["job"])
    for name in skipped_required:
        reasons.append("required-job-skipped:%s" % name)
    for name in unexpected:
        reasons.append("%s:%s" % (SKIP_REASON_UNEXPECTED, name))
    if truncated:
        reasons.append("jobs-truncated")
    if soft:
        reasons.append("executed-job-not-green:%s" % ",".join(sorted(soft)))
    if run_identity["run_status"] != "completed":
        reasons.append("run_status=%s" % run_identity["run_status"])
    if not isinstance(run_conclusion, str):
        reasons.append("run_conclusion=not_recorded")
    if run_identity["run_attempt"] != 1:
        reasons.append("run_attempt=%s" % run_identity["run_attempt"])
    if roster_delta:
        reasons.append("roster_delta=%s" % ",".join(sorted(roster_delta)))
    if reasons or blocked:
        return _marker("INCOMPLETE", EXIT_INCOMPLETE,
                       "; ".join(blocked + reasons), (), soft,
                       skipped_required, unexpected)
    return _marker("COMPLETE", EXIT_COMPLETE, "head_bound_green", (), (),
                   skipped_required, unexpected)


def _validate_skills_job(payload_jobs):
    for job in payload_jobs:
        if isinstance(job, dict) and job.get("name") == "validate-skills":
            return job
    return None


def _step_belongs(step, name):
    if not isinstance(step, dict):
        return False
    recorded = step.get("name")
    if not isinstance(recorded, str):
        return False
    return recorded == name or recorded.startswith(name + " ")


def _step_states(payload_jobs):
    """F4: the REAL state of the two PR-only validate-skills steps.

    The old unconditional `step_skipped` line claimed a validation gap on
    every run, including the pull_request runs where the workflow executes
    both steps (validate-skills.yml L260-267 and L269-274). The state now
    comes from the steps the API returned for the `validate-skills` job, and
    an unreported step is `not_recorded` - a gap, not a skip.
    """
    job = _validate_skills_job(payload_jobs)
    states = []
    for name in PR_ONLY_STEP_NAMES:
        match = None
        for step in (job or {}).get("steps") or []:
            if _step_belongs(step, name):
                match = step
                break
        if job is None:
            state = "not_recorded"
            detail = "validate-skills job absent; step state unavailable"
        elif match is None:
            state = "not_recorded"
            detail = "step absent from the API job payload"
        else:
            conclusion = match.get("conclusion")
            if conclusion == "skipped":
                state = "skipped"
                detail = "API reports the step skipped"
            elif conclusion is None:
                state = "not_recorded"
                detail = "step has no terminal conclusion"
            else:
                state = "executed"
                detail = "API reports the step executed (conclusion=%s)" % \
                    conclusion
        states.append({"step": name, "state": state,
                       "location": PR_STEP_LOCATIONS[name],
                       "detail": "validate-skills: %s (%s; not a job)" % (
                           name, detail)})
    return states


def _prerequisites(rows, payload_jobs, artifact_entries, event=None,
                   truncated=False):
    names = {job.get("name") for job in payload_jobs if isinstance(job, dict)}
    roster_delta = sorted(n for n in names if n not in JOB_ROSTER)
    if truncated:
        roster_delta.append("truncated-jobs-page")
    step_details = _step_states(payload_jobs)
    return {
        "failed_or_missing": [
            row["job"] for row in rows
            if row["state"] == "missing"
            or (row["state"] == "executed"
                and row["conclusion"] not in GREEN_CONCLUSIONS)],
        "coverage_gaps": ["%s: %s" % (row["job"], row["note"])
                          for row in rows
                          if row["coverage"] == "not_demonstrated"],
        "roster_delta": roster_delta,
        "artifact_retention": "%dd" % ARTIFACT_RETENTION_DAYS,
        "artifact_unmapped": [
            "%s (reason=%s)" % (e["directory"].name,
                                e.get("reason", "not_mapped"))
            for e in artifact_entries if e.get("job") is None],
        "step_details": step_details,
        # F4: only genuinely skipped steps are listed, so a pull_request run
        # no longer claims a gap the workflow does not have.
        "step_skipped": [item["detail"] for item in step_details
                         if item["state"] == "skipped"]}


def build_evidence(run_identity, rows, prerequisites, api_calls, http_status):
    """Assemble the fixed output object (Blocks A, A', B, C, D)."""
    status = derive_status(
        run_identity, rows, prerequisites["roster_delta"],
        run_identity.get("run_event"),
        "truncated-jobs-page" in prerequisites["roster_delta"])
    fields = dict(run_identity)
    fields["api_urls"] = [{"url": call["url"],
                           "http_status": call["http_status"]}
                          for call in api_calls]
    fields["http_status"] = http_status
    return {"command_identity": identity(), "run_identity": fields,
            "jobs": rows, "prerequisites": prerequisites,
            "status": status["status"], "marker": status}


def render_json(evidence):
    return json.dumps(evidence, sort_keys=True, indent=2)


def render_table(evidence):
    """Render the same evidence as fixed-width Markdown-pipe text.

    F10: this is the SINGLE escaping pass (escape_text). The evidence object
    stores raw payload values and render_json emits them unchanged, so the
    table names - through escapes - exactly the characters the JSON carries
    raw, instead of double-escaping a pre-escaped stored string.
    """
    run = evidence["run_identity"]
    lines = ["## ci-durations run identity"]
    for key in ("repository", "workflow", "workflow_file", "run_id",
                "run_attempt", "attempt_requested", "run_event", "run_status",
                "run_conclusion", "run_head_sha", "candidate_sha",
                "candidate_status", "run_created_at", "run_updated_at",
                "fetched_at", "jobs_total_count", "jobs_reported_total",
                "jobs_truncated", "fixture_precedence", "http_status"):
        lines.append("- %s: %s" % (key, escape_text(run.get(key))))
    for call in run["api_urls"]:
        lines.append("- api_url: %s (http_status=%s)"
                     % (escape_text(call["url"]), call["http_status"]))
    columns = ("job", "state", "conclusion", "started_at", "completed_at",
               "duration_s", "duration_provenance", "exit_code",
               "exit_codes", "exit_code_provenance", "coverage",
               "skip_reason", "artifact", "log_url")
    lines.append("")
    lines.append("## ci-durations jobs")
    lines.append("| %s |" % " | ".join(columns))
    lines.append("| %s |" % " | ".join("---" for _ in columns))
    for row in evidence["jobs"]:
        lines.append("| %s |" % " | ".join(
            escape_text(_exit_codes_text(row.get(column)))
            if column == "exit_codes"
            else escape_text(row.get(column)) for column in columns))
    lines.append("")
    lines.append("## ci-durations prerequisites and gaps")
    for key in ("failed_or_missing", "coverage_gaps", "roster_delta",
                "artifact_retention", "artifact_unmapped", "step_skipped"):
        value = evidence["prerequisites"][key]
        rendered = (", ".join(escape_text(item) for item in value)
                    if isinstance(value, list) else escape_text(value))
        lines.append("- %s: %s" % (key, rendered or "none"))
    for item in evidence["prerequisites"]["step_details"]:
        lines.append("- step_state: %s [%s] %s" % (
            escape_text(item["step"]), escape_text(item["state"]),
            escape_text(item["detail"])))
    marker = evidence["marker"]
    lines.append("")
    lines.append("STATUS: %s (exit %d) reason: %s" % (
        marker["status"], marker["exit_code"],
        escape_text(marker["reason"])))
    if marker["failing_jobs"]:
        lines.append("failing: %s" % ", ".join(
            escape_text(name) for name in marker["failing_jobs"]))
    if marker.get("skipped_required_jobs"):
        lines.append("required-job-skipped: %s" % ", ".join(
            escape_text(name) for name in marker["skipped_required_jobs"]))
    if marker.get("unexpected_skipped_jobs"):
        lines.append("unexpected-skip: %s" % ", ".join(
            escape_text(name) for name in marker["unexpected_skipped_jobs"]))
    return chr(10).join(lines)


def _same_host_target(url):
    """True when `url` keeps the fixed scheme and host (F7)."""
    parts = urllib.parse.urlsplit(url)
    return parts.scheme == "https" and parts.hostname == FIXED_HOST


class _FixedHostRedirectHandler(urllib.request.HTTPRedirectHandler):
    """F7: refuse any redirect that changes scheme or host.

    `urllib.request.HTTPRedirectHandler.redirect_request` copies every header
    except content-length/content-type onto the redirected request - the
    bearer token from `--token-env` included. Following a cross-host 3xx would
    therefore contact a second host AND disclose the token, which the fixed
    one-host identity block forbids. This handler raises HTTPError instead,
    before any header is rebuilt, so the token cannot leave api.github.com.
    """

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not _same_host_target(newurl):
            raise urllib.error.HTTPError(
                req.full_url, code,
                "refusing cross-host redirect to %s" % newurl, headers, fp)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class HttpTransport:
    """Fixed-host read-only transport; api.github.com is the only host.

    F7: the opener installs `_FixedHostRedirectHandler`, and the response URL
    is re-checked after the read, so the one-host guarantee holds by
    construction rather than by trusting the requested URL.
    """

    def __init__(self, token=None):
        self._token = token
        self._opener = urllib.request.build_opener(
            _FixedHostRedirectHandler)

    def fetch(self, url):
        headers = {"Accept": "application/vnd.github+json",
                   "X-GitHub-Api-Version": API_VERSION,
                   "User-Agent": USER_AGENT}
        if self._token:
            headers["Authorization"] = "Bearer %s" % self._token
        if not _same_host_target(url):
            raise TransportFailure("refusing to contact a non-fixed host")
        request = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with self._opener.open(request, timeout=TIMEOUT_SECONDS) as resp:
                if not _same_host_target(resp.geturl()):
                    raise TransportFailure(
                        "redirected off %s" % FIXED_HOST)
                status, body = resp.getcode(), resp.read().decode()
        except urllib.error.HTTPError as error:
            raise TransportFailure(
                "HTTP %s for %s" % (error.code, url)) from error
        except (urllib.error.URLError, OSError) as error:
            raise TransportFailure(
                "transport error for %s: %s" % (url, error)) from error
        try:
            return json.loads(body), status
        except json.JSONDecodeError as error:
            raise TransportFailure("malformed JSON from %s" % url) from error


class FixtureTransport:
    """Offline replay of a url -> payload fixture map; never a socket."""

    def __init__(self, fixture):
        self._fixture = fixture

    def fetch(self, url):
        if url not in self._fixture:
            raise FixtureMiss("fixture has no payload for %s" % url)
        payload = self._fixture[url]
        if isinstance(payload, dict) and set(payload) >= {"body", "status"}:
            status, body = payload["status"], payload["body"]
        else:
            status, body = 200, payload
        if not isinstance(status, int) or not 200 <= status < 300:
            raise TransportFailure("HTTP %s for %s (fixture)" % (status, url))
        return body, status


def _check_url(repository, run_id):
    return "https://%s/repos/%s/actions/runs/%s" % (
        FIXED_HOST, repository, run_id)


def _jobs_url(repository, run_id, page=1):
    """Page 1 keeps the historical URL; later pages append `&page=N` (F8)."""
    base = "%s/jobs?per_page=%d" % (_check_url(repository, run_id),
                                    JOBS_PER_PAGE)
    return base if page == 1 else "%s&page=%d" % (base, page)


def _runs_url(repository, workflow, head, event):
    url = ("https://%s/repos/%s/actions/workflows/%s/runs"
           "?head_sha=%s&per_page=100") % (FIXED_HOST, repository, workflow,
                                           head)
    return url + ("&event=%s" % event if event else "")


# Codex P1 (4244631210), second half: a component that would build a URL
# `http.client` rejects must be refused as input (exit 2) instead of escaping
# as a traceback. Only the characters GitHub actually uses are accepted.
SAFE_COMPONENT = re.compile(r"^[A-Za-z0-9._/-]{1,140}$")
SAFE_HEAD = re.compile(r"^[A-Za-z0-9._-]{1,100}$")


def _checked_components(repository, workflow, head, run_id):
    """Refuse an input the fixed-host URL could not carry (exit 2)."""
    if not SAFE_COMPONENT.match(repository or ""):
        raise RefusedInput(
            "--repository must be owner/name of [A-Za-z0-9._-]; got %r"
            % repository)
    if "/" in repository and repository.count("/") != 1:
        raise RefusedInput(
            "--repository must be exactly owner/name; got %r" % repository)
    if not SAFE_COMPONENT.match(workflow or ""):
        raise RefusedInput(
            "--workflow must be a file name of [A-Za-z0-9._-]; got %r"
            % workflow)
    if head is not None and not SAFE_HEAD.match(head):
        raise RefusedInput("--head must be a revision of [A-Za-z0-9._-]; "
                           "got %r" % head)
    if run_id is not None and not str(run_id).isdigit():
        raise RefusedInput("--run-id must be digits; got %r" % run_id)


def _load_fixture(path):
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except OSError as error:
        raise RefusedInput("fixture unreadable: %s" % error) from error
    except json.JSONDecodeError as error:
        raise RefusedInput("fixture is not valid JSON: %s" % error) from error
    if not isinstance(value, dict):
        raise RefusedInput("fixture must be a JSON object of url -> payload")
    return value


def _resolve_run_id(transport, repository, workflow, head, event):
    url = _runs_url(repository, workflow, head, event)
    payload, status = transport.fetch(url)
    if not isinstance(payload, dict):
        raise TransportFailure("malformed runs payload from %s" % url)
    runs = payload.get("workflow_runs")
    if not isinstance(runs, list) or not runs:
        raise RefusedInput("no run found for workflow=%s head=%s event=%s"
                           % (workflow, head, event or "any"))
    newest = runs[0]
    run_id = newest.get("id") if isinstance(newest, dict) else None
    if run_id is None:
        raise RefusedInput("resolved run has no id")
    return str(run_id), [{"url": url, "http_status": status}]


def _collect_artifact_entries(artifact_dir):
    if artifact_dir is None:
        return []
    root = Path(artifact_dir)
    if not root.is_dir():
        raise RefusedInput("artifact directory not found: %s" % artifact_dir)
    return [{"directory": child, "job": None, "reason": "not_mapped"}
            for child in sorted(root.iterdir()) if child.is_dir()]


def _now_iso(now):
    if now:
        if _iso(now) is None:
            raise RefusedInput("--now must be an ISO-8601 timestamp")
        return now
    return (datetime.now(timezone.utc).replace(microsecond=0).isoformat()
            .replace("+00:00", "Z"))


def _text(run_payload, key):
    value = run_payload.get(key)
    return value if isinstance(value, str) else NOT_RECORDED


def _run_identity(repository, workflow, run_payload, run_id, candidate,
                  candidate_status, fetched_at, fixture_precedence,
                  attempt=None, jobs_total=None, jobs_read=0, truncated=None):
    """The run identity block; raw values, escaped once by render_table (F10)."""
    run_attempt = run_payload.get("run_attempt")
    if not isinstance(run_attempt, int) or isinstance(run_attempt, bool):
        run_attempt = NOT_RECORDED
    head_sha = run_payload.get("head_sha")
    if truncated is None:
        truncated = (NOT_RECORDED if jobs_total is None
                     else jobs_read < jobs_total)
    return {
        "repository": repository,
        "workflow": "%s (id=%s)" % (
            run_payload.get("name") or workflow,
            run_payload.get("workflow_id")),
        "workflow_file": workflow, "run_id": str(run_id),
        "run_attempt": run_attempt,
        # F9: the requested attempt is recorded, not silently discarded.
        "attempt_requested": attempt if attempt else NOT_SELECTED,
        "run_event": _text(run_payload, "event"),
        "run_status": _text(run_payload, "status"),
        "run_conclusion": _text(run_payload, "conclusion"),
        "run_head_sha": head_sha if isinstance(head_sha, str)
        else NOT_RECORDED,
        "candidate_sha": candidate if candidate else NOT_SUPPLIED,
        "candidate_status": candidate_status,
        "stale": candidate_status == "differs",
        # F8: the advertised total, what was actually read, and the verdict.
        "jobs_total_count": jobs_total if jobs_total is not None
        else NOT_RECORDED,
        "jobs_reported_total": jobs_read,
        "jobs_truncated": truncated,
        "run_created_at": _text(run_payload, "created_at"),
        "run_updated_at": _text(run_payload, "updated_at"),
        "fetched_at": fetched_at, "fixture_precedence": fixture_precedence}


def _reported_total(jobs_payload):
    """The `total_count` the API advertised, or None when it said nothing."""
    total = jobs_payload.get("total_count")
    if isinstance(total, int) and not isinstance(total, bool) and total >= 0:
        return total
    return None


def _fetch_run_and_jobs(transport, repository, run_id):
    """F8: page through the jobs list; never trust a truncated first page.

    The old code requested `per_page=100` and ignored `total_count`, so a run
    with more than 100 jobs could look green while jobs on later pages were
    never inspected. Later pages are fetched only while the advertised total
    exceeds what has been received, and anything still missing is reported as
    a `truncated-jobs-page` roster entry that forces INCOMPLETE.
    """
    check_url = _check_url(repository, run_id)
    run_payload, run_status = transport.fetch(check_url)
    if not isinstance(run_payload, dict):
        raise TransportFailure("malformed run payload from %s" % check_url)
    calls = [{"url": check_url, "http_status": run_status}]
    payload_jobs, page, pages_read = [], 1, 0
    jobs_status = None
    total = None
    while page <= MAX_JOB_PAGES:
        jobs_url = _jobs_url(repository, run_id, page)
        jobs_payload, jobs_status = transport.fetch(jobs_url)
        if not isinstance(jobs_payload, dict):
            raise TransportFailure(
                "malformed jobs payload from %s" % jobs_url)
        page_jobs = jobs_payload.get("jobs")
        if not isinstance(page_jobs, list):
            raise TransportFailure("jobs payload has no job list")
        if _reported_total(jobs_payload) is not None:
            total = _reported_total(jobs_payload)
        payload_jobs.extend(page_jobs)
        pages_read += 1
        calls.append({"url": jobs_url, "http_status": jobs_status})
        # A short page is the last page; a full page means read on while the
        # advertised total still exceeds what has been collected.
        if not page_jobs or len(page_jobs) < JOBS_PER_PAGE:
            break
        if total is not None and len(payload_jobs) >= total:
            break
        if page >= MAX_JOB_PAGES:
            break
        page += 1
    # F8: the report is TRUNCATED whenever the API advertised more jobs than
    # were actually read - whether the list simply stopped short, or the
    # MAX_JOB_PAGES ceiling was reached after a full page.
    truncated = (total is not None and len(payload_jobs) < total
                 and (pages_read >= MAX_JOB_PAGES
                      or len(payload_jobs) < JOBS_PER_PAGE * pages_read))
    return run_payload, payload_jobs, calls, jobs_status, total, truncated


def run_command(repository_id, *, repository=DEFAULT_REPOSITORY,
                workflow=DEFAULT_WORKFLOW, run_id=None, head=None, event=None,
                attempt=None, candidate=None, fixture=None,
                allow_network=False,
                token_env=None, artifact_dir=None, output_format="table",
                now=None):
    """Execute the reader; returns the process exit code (0/1/2/3/4)."""
    del repository_id  # identity only; never used to reach a host
    fetched_at = _now_iso(now)
    payload_fixture = _load_fixture(fixture) if fixture is not None else None
    if payload_fixture is None and not allow_network:
        raise RefusedInput(
            "refusing to read GitHub: supply --fixture <path> for offline "
            "replay or --allow-network for one live read of %s" % FIXED_HOST)
    if not run_id and not head:
        raise RefusedInput("supply --run-id or --head to identify a run")
    _checked_components(repository, workflow, head, run_id)
    fixture_precedence = payload_fixture is not None
    if fixture_precedence:
        transport = FixtureTransport(payload_fixture)
    else:
        token = os.environ.get(token_env) if token_env else None
        if token_env and not token:
            raise RefusedInput(
                "environment variable %s is empty or unset" % token_env)
        transport = HttpTransport(token)
    api_calls = []
    if not run_id:
        run_id, calls = _resolve_run_id(transport, repository, workflow, head,
                                        event)
        api_calls.extend(calls)
    run_payload, payload_jobs, calls, jobs_status, jobs_total, truncated = \
        _fetch_run_and_jobs(transport, repository, run_id)
    api_calls.extend(calls)
    recorded_attempt = run_payload.get("run_attempt")
    if attempt is not None:
        # F9: `--attempt` selects or refuses; it is never accepted and ignored.
        if not isinstance(recorded_attempt, int) \
                or isinstance(recorded_attempt, bool):
            raise RefusedInput(
                "--attempt %s requested but the run payload records no "
                "run_attempt" % attempt)
        if recorded_attempt != attempt:
            raise RefusedInput(
                "--attempt %s requested but run %s reports run_attempt=%s"
                % (attempt, run_id, recorded_attempt))
    candidate_status, stale = derive_staleness(candidate,
                                               run_payload.get("head_sha"))
    artifact_entries = _collect_artifact_entries(artifact_dir)
    run_identity = _run_identity(
        repository, workflow, run_payload, run_id, candidate, candidate_status,
        fetched_at, fixture_precedence, attempt, jobs_total,
        len(payload_jobs), truncated)
    rows = _derive_job_rows(payload_jobs, run_payload.get("head_sha"),
                            run_identity["run_event"],
                            _artifacts_by_job(payload_jobs), artifact_entries)
    prerequisites = _prerequisites(
        rows, payload_jobs, artifact_entries, run_identity["run_event"],
        truncated)
    evidence = build_evidence(run_identity, rows, prerequisites, api_calls,
                              jobs_status)
    print(render_json(evidence) if output_format == "json"
          else render_table(evidence))
    return evidence["marker"]["exit_code"]


def build_parser(subparsers):
    """Register the ci-durations subcommand on the package parser."""
    parser = subparsers.add_parser(
        "ci-durations",
        help="Read one GitHub Actions run's per-job durations (read-only).",
        description=("Read one public GitHub Actions run's per-job durations "
                     "and print honest coverage evidence. Offline unless "
                     "--allow-network is given; contactable host: %s only."
                     % FIXED_HOST))
    parser.add_argument("--repository", default=DEFAULT_REPOSITORY)
    parser.add_argument("--workflow", default=DEFAULT_WORKFLOW)
    parser.add_argument("--run-id")
    parser.add_argument("--head")
    parser.add_argument("--event", choices=("pull_request", "push"))
    parser.add_argument(
        "--attempt", type=int,
        help=("require this run_attempt; the run payload must confirm it or "
              "the command refuses with exit 2"))
    parser.add_argument(
        "--candidate",
        help=("commit SHA to bind to the run head; only an exact match can "
              "produce COMPLETE and exit 0"))
    parser.add_argument("--fixture", type=Path)
    parser.add_argument("--allow-network", action="store_true")
    parser.add_argument("--token-env")
    parser.add_argument("--artifact-dir", type=Path)
    parser.add_argument("--format", choices=("table", "json"),
                        default="table")
    parser.add_argument("--now")
    parser.add_argument("--show-identity", action="store_true")
    return parser


def main(arguments) -> int:
    """Adapter used by the package CLI; input refusals map to exit 2."""
    if getattr(arguments, "show_identity", False):
        print(json.dumps(identity(), sort_keys=True, indent=2))
        return 0
    try:
        return run_command(
            arguments.repository_id, repository=arguments.repository,
            workflow=arguments.workflow, run_id=arguments.run_id,
            head=arguments.head, event=arguments.event,
            attempt=arguments.attempt, candidate=arguments.candidate,
            fixture=arguments.fixture, allow_network=arguments.allow_network,
            token_env=arguments.token_env, artifact_dir=arguments.artifact_dir,
            output_format=arguments.format, now=arguments.now)
    except RefusedInput as error:
        print("ci-durations refused: %s" % error, file=sys.stderr)
        return EXIT_REFUSED
    except TransportFailure as error:
        print("ci-durations transport failure: %s" % error, file=sys.stderr)
        return EXIT_TRANSPORT
