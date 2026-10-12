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
  missing timestamp on an executed row, a red run, or an executed job that is
  not green all raise the status; none is rounded down to a pass.
* **head-bound completeness (D20).** `COMPLETE` and exit 0 require a
  `--candidate` equal to the run head; without one the marker is `UNBOUND`.

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
        "0": "printed and COMPLETE (head-bound, green)",
        "1": "printed but STALE, INCOMPLETE or UNBOUND",
        "2": "refused or unresolvable input",
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
    """Escape one payload- or file-derived string (D19).

    Backslash first, then every ASCII control character (newline, carriage
    return, tab, the ANSI/CSI introducer) as a hex escape, then the Markdown
    pipe. The result is capped at 300 characters with a visible marker, so no
    field can produce a second output line or forge a row or status marker.
    """
    text = "" if value is None else str(value)
    text = text.replace(BACKSLASH, BACKSLASH * 2)
    text = "".join(
        character if character >= " " and character != chr(127)
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
    """Derive the reason token for a job the API reported as skipped."""
    if job_name != "changes" and (
            changes_conclusion in NON_GREEN_EXECUTED_CONCLUSIONS):
        return "%s (changes=%s)" % (SKIP_REASON_DEPENDENCY_FAILED,
                                    changes_conclusion)
    if job_name == "gate-guard":
        return "%s (pull_request-only job)" % SKIP_REASON_EVENT_FILTER
    if job_name == "changes":
        return "%s (no path filter)" % SKIP_REASON_EVENT_FILTER
    return "%s (paths did not select it on event=%s)" % (
        SKIP_REASON_EVENT_FILTER,
        escape_text(event) if event else NOT_RECORDED)


def _artifact_text(artifact):
    if not artifact:
        return NONE_UPLOADED
    return "%s (id=%s, bytes=%s, expires=%s, expired=%s)" % (
        escape_text(artifact.get("name")), artifact.get("id"),
        artifact.get("size_in_bytes"), escape_text(artifact.get("expires_at")),
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
            "coverage": "not_demonstrated", "skip_reason": NOT_SELECTED,
            "artifact": NONE_UPLOADED, "log_url": NOT_RECORDED,
            "note": "roster-job-absent-from-api-response"}


def _segments(name):
    parts = name.rsplit("-", 2)
    return parts[0] if len(parts) == 3 and all(
        part.isdigit() for part in parts[1:]) else ""


def _apply_artifact_exit_codes(rows, run_head_sha, artifact_entries):
    """Attach an exit code only when a mapped record binds to the run head."""
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
        for record_path in sorted(directory.glob("*.json")):
            try:
                record = json.loads(record_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                entry["reason"] = "record-unreadable"
                continue
            if not isinstance(record, dict):
                entry["reason"] = "record-malformed"
                continue
            recorded_sha = record.get("checkout_sha")
            location = "%s/%s" % (escape_text(name),
                                  escape_text(record_path.name))
            if recorded_sha != run_head_sha:
                entry["reason"] = "artifact head mismatch"
                row["exit_code_provenance"] = (
                    "%s: head mismatch (record=%s run=%s)" % (
                        location, escape_text(recorded_sha),
                        escape_text(run_head_sha)))
                continue
            exit_code = record.get("exit_code")
            if not isinstance(exit_code, int) or isinstance(exit_code, bool):
                entry["reason"] = "record-gap: exit_code"
                continue
            row["exit_code"] = exit_code
            row["exit_code_provenance"] = (
                "artifact:%s (checkout_sha=%s, label=%s, elapsed_seconds=%s)"
                % (location, escape_text(recorded_sha),
                   escape_text(record.get("label")),
                   escape_text(record.get("elapsed_seconds"))))
            entry["reason"] = "mapped"
            entry["label"] = record.get("label")
            break


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
        row = {"job": name,
               "conclusion": escape_text(conclusion)
               if isinstance(conclusion, str) else NOT_RECORDED,
               "started_at": escape_text(started_at)
               if isinstance(started_at, str) else NOT_RECORDED,
               "completed_at": escape_text(completed_at)
               if isinstance(completed_at, str) else NOT_RECORDED,
               "exit_code": NOT_RECORDED, "exit_code_provenance": NOT_SELECTED,
               "artifact": _artifact_text(artifacts.get(name)),
               "log_url": escape_text(job.get("html_url"))
               if isinstance(job.get("html_url"), str) else NOT_RECORDED,
               "note": NOT_SELECTED}
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
    _apply_artifact_exit_codes(rows, run_head_sha, entries)
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


def _marker(status, exit_code, reason, failing=(), non_green=()):
    return {"status": status, "exit_code": exit_code, "reason": reason,
            "failing_jobs": list(failing), "non_green_jobs": list(non_green)}


def derive_status(run_identity, rows, roster_delta=()):
    """Resolve the one honest status marker; first match wins (D16/D20).

    R1, strictest honest reading: the green set is defined positively as
    exactly {success}. A terminal executed job outside it is either a hard
    failure (FAILED, exit 4) or, for the remaining terminal conclusions such
    as neutral, a soft non-green that forces INCOMPLETE and never exit 0.
    """
    executed = [row for row in rows if row["state"] == "executed"]
    failing = [row["job"] for row in executed
               if row["conclusion"] in NON_GREEN_EXECUTED_CONCLUSIONS]
    soft = [row["job"] for row in executed
            if row["conclusion"] not in GREEN_CONCLUSIONS
            and row["conclusion"] not in NON_GREEN_EXECUTED_CONCLUSIONS]
    run_conclusion = run_identity["run_conclusion"]
    run_red = (run_identity["run_status"] == "completed"
               and isinstance(run_conclusion, str)
               and run_conclusion not in GREEN_CONCLUSIONS)
    if run_red or failing:
        offending = list(failing)
        if run_red and run_conclusion and run_conclusion not in failing:
            offending.append("run_conclusion=%s" % run_conclusion)
        return _marker("FAILED", EXIT_FAILED, "not_green", offending,
                       failing + soft)
    if run_identity["candidate_sha"] == NOT_SUPPLIED:
        return _marker("UNBOUND", EXIT_INCOMPLETE, "no_candidate_supplied")
    if run_identity["stale"]:
        return _marker("STALE", EXIT_INCOMPLETE,
                       "candidate_differs_from_run_head")
    reasons = []
    for row in rows:
        if row["state"] in ("missing", "unresolved"):
            reasons.append("%s=%s" % (row["job"], row["state"]))
        elif row["state"] == "executed" and row["duration_s"] == NOT_RECORDED:
            reasons.append("%s=duration_not_recorded" % row["job"])
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
    if reasons:
        return _marker("INCOMPLETE", EXIT_INCOMPLETE, "; ".join(reasons),
                       (), soft)
    return _marker("COMPLETE", EXIT_COMPLETE, "head_bound_green")


def _prerequisites(rows, payload_jobs, artifact_entries):
    names = {job.get("name") for job in payload_jobs if isinstance(job, dict)}
    return {
        "failed_or_missing": [
            row["job"] for row in rows
            if row["state"] == "missing"
            or (row["state"] == "executed"
                and row["conclusion"] not in GREEN_CONCLUSIONS)],
        "coverage_gaps": ["%s: %s" % (row["job"], row["note"])
                          for row in rows
                          if row["coverage"] == "not_demonstrated"],
        "roster_delta": sorted(n for n in names if n not in JOB_ROSTER),
        "artifact_retention": "%dd" % ARTIFACT_RETENTION_DAYS,
        "artifact_unmapped": [
            "%s (reason=%s)" % (escape_text(e["directory"].name),
                                e.get("reason", "not_mapped"))
            for e in artifact_entries if e.get("job") is None],
        "step_skipped": [
            "validate-skills: Verify DCO sign-off on every commit "
            "(pull_request-only step; not a job)"]}


def build_evidence(run_identity, rows, prerequisites, api_calls, http_status):
    """Assemble the fixed output object (Blocks A, A', B, C, D)."""
    status = derive_status(run_identity, rows,
                           prerequisites["roster_delta"])
    fields = dict(run_identity)
    fields["api_urls"] = [{"url": escape_text(call["url"]),
                           "http_status": call["http_status"]}
                          for call in api_calls]
    fields["http_status"] = http_status
    return {"command_identity": identity(), "run_identity": fields,
            "jobs": rows, "prerequisites": prerequisites,
            "status": status["status"], "marker": status}


def render_json(evidence):
    return json.dumps(evidence, sort_keys=True, indent=2)


def render_table(evidence):
    """Render the same evidence as fixed-width Markdown-pipe text."""
    run = evidence["run_identity"]
    lines = ["## ci-durations run identity"]
    for key in ("repository", "workflow", "workflow_file", "run_id",
                "run_attempt", "run_event", "run_status", "run_conclusion",
                "run_head_sha", "candidate_sha", "candidate_status",
                "run_created_at", "run_updated_at", "fetched_at",
                "fixture_precedence", "http_status"):
        lines.append("- %s: %s" % (key, escape_text(run.get(key))))
    for call in run["api_urls"]:
        lines.append("- api_url: %s (http_status=%s)"
                     % (escape_text(call["url"]), call["http_status"]))
    columns = ("job", "state", "conclusion", "started_at", "completed_at",
               "duration_s", "duration_provenance", "exit_code", "coverage",
               "skip_reason", "artifact", "log_url")
    lines.append("")
    lines.append("## ci-durations jobs")
    lines.append("| %s |" % " | ".join(columns))
    lines.append("| %s |" % " | ".join("---" for _ in columns))
    for row in evidence["jobs"]:
        lines.append("| %s |" % " | ".join(
            escape_text(row.get(column)) for column in columns))
    lines.append("")
    lines.append("## ci-durations prerequisites and gaps")
    for key in ("failed_or_missing", "coverage_gaps", "roster_delta",
                "artifact_retention", "artifact_unmapped", "step_skipped"):
        value = evidence["prerequisites"][key]
        rendered = (", ".join(escape_text(item) for item in value)
                    if isinstance(value, list) else escape_text(value))
        lines.append("- %s: %s" % (key, rendered or "none"))
    marker = evidence["marker"]
    lines.append("")
    lines.append("STATUS: %s (exit %d) reason: %s" % (
        marker["status"], marker["exit_code"],
        escape_text(marker["reason"])))
    if marker["failing_jobs"]:
        lines.append("failing: %s" % ", ".join(
            escape_text(name) for name in marker["failing_jobs"]))
    return chr(10).join(lines)


class HttpTransport:
    """Fixed-host read-only transport; api.github.com is the only host."""

    def __init__(self, token=None):
        self._token = token

    def fetch(self, url):
        headers = {"Accept": "application/vnd.github+json",
                   "X-GitHub-Api-Version": API_VERSION,
                   "User-Agent": USER_AGENT}
        if self._token:
            headers["Authorization"] = "Bearer %s" % self._token
        request = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(
                    request, timeout=TIMEOUT_SECONDS) as response:
                status, body = response.getcode(), response.read().decode()
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


def _jobs_url(repository, run_id):
    return "%s/jobs?per_page=100" % _check_url(repository, run_id)


def _runs_url(repository, workflow, head, event):
    url = ("https://%s/repos/%s/actions/workflows/%s/runs"
           "?head_sha=%s&per_page=100") % (FIXED_HOST, repository, workflow,
                                           head)
    return url + ("&event=%s" % event if event else "")


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
                  candidate_status, fetched_at, fixture_precedence):
    run_attempt = run_payload.get("run_attempt")
    if not isinstance(run_attempt, int) or isinstance(run_attempt, bool):
        run_attempt = NOT_RECORDED
    head_sha = run_payload.get("head_sha")
    return {
        "repository": repository,
        "workflow": "%s (id=%s)" % (
            escape_text(run_payload.get("name") or workflow),
            escape_text(run_payload.get("workflow_id"))),
        "workflow_file": workflow, "run_id": str(run_id),
        "run_attempt": run_attempt, "run_event": _text(run_payload, "event"),
        "run_status": _text(run_payload, "status"),
        "run_conclusion": _text(run_payload, "conclusion"),
        "run_head_sha": head_sha if isinstance(head_sha, str)
        else NOT_RECORDED,
        "candidate_sha": candidate if candidate else NOT_SUPPLIED,
        "candidate_status": candidate_status,
        "stale": candidate_status == "differs",
        "run_created_at": _text(run_payload, "created_at"),
        "run_updated_at": _text(run_payload, "updated_at"),
        "fetched_at": fetched_at, "fixture_precedence": fixture_precedence}


def _fetch_run_and_jobs(transport, repository, run_id):
    check_url = _check_url(repository, run_id)
    run_payload, run_status = transport.fetch(check_url)
    if not isinstance(run_payload, dict):
        raise TransportFailure("malformed run payload from %s" % check_url)
    jobs_url = _jobs_url(repository, run_id)
    jobs_payload, jobs_status = transport.fetch(jobs_url)
    if not isinstance(jobs_payload, dict):
        raise TransportFailure("malformed jobs payload from %s" % jobs_url)
    payload_jobs = jobs_payload.get("jobs")
    if not isinstance(payload_jobs, list):
        raise TransportFailure("jobs payload has no job list")
    calls = [{"url": check_url, "http_status": run_status},
             {"url": jobs_url, "http_status": jobs_status}]
    return run_payload, payload_jobs, calls, jobs_status


def run_command(repository_id, *, repository=DEFAULT_REPOSITORY,
                workflow=DEFAULT_WORKFLOW, run_id=None, head=None, event=None,
                attempt=None, candidate=None, fixture=None,
                allow_network=False,
                token_env=None, artifact_dir=None, output_format="table",
                now=None):
    """Execute the reader; returns the process exit code (0/1/2/3/4)."""
    del repository_id, attempt  # identity only; never used to reach a host
    fetched_at = _now_iso(now)
    payload_fixture = _load_fixture(fixture) if fixture is not None else None
    if payload_fixture is None and not allow_network:
        raise RefusedInput(
            "refusing to read GitHub: supply --fixture <path> for offline "
            "replay or --allow-network for one live read of %s" % FIXED_HOST)
    if not run_id and not head:
        raise RefusedInput("supply --run-id or --head to identify a run")
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
    run_payload, payload_jobs, calls, jobs_status = _fetch_run_and_jobs(
        transport, repository, run_id)
    api_calls.extend(calls)
    candidate_status, stale = derive_staleness(candidate,
                                               run_payload.get("head_sha"))
    run_identity = _run_identity(repository, workflow, run_payload, run_id,
                                 candidate, candidate_status, fetched_at,
                                 fixture_precedence)
    artifact_entries = _collect_artifact_entries(artifact_dir)
    rows = _derive_job_rows(payload_jobs, run_payload.get("head_sha"),
                            run_identity["run_event"],
                            _artifacts_by_job(payload_jobs), artifact_entries)
    evidence = build_evidence(
        run_identity, rows,
        _prerequisites(rows, payload_jobs, artifact_entries), api_calls,
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
    parser.add_argument("--attempt", type=int)
    parser.add_argument("--candidate")
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
