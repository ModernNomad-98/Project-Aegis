"""Offline tests for the read-only CI-run duration reader (P0-A A2).

Every fixture here is a replay of the payload shapes the plan records as
independently re-derived: run 38198781208 (push, head 4d5ccb0b..., attempt 1)
carries the AC1 durations 7/109/skipped/224/132/229 s, and the second fixture
mirrors the A1 page cross-check pair 8/111/skipped/241/100/165 s. No test
performs network I/O: the zero-socket proof patches socket.socket,
urllib.request.urlopen and ci_durations.HttpTransport together, and the
fixture path is additionally asserted never to construct a transport.

`RepairRoundTests` adds the negative fixtures for the Stage D findings F1-F9
and the nine Codex review comments at the same head: an unresolvable run head,
a `pull_request` run whose required `gate-guard` job was skipped, the Unicode
line separators, the real PR-only step states, a multi-record artifact and its
`pr_head_sha` binding, the cross-host redirect refusal, a truncated and a
paginated jobs list, and `--attempt` selection.

`UnexpectedSkipEnforcementTests` adds the SD-D round-2 finding N1: the
workflow's own per-event allowed-skip set is enforced, so a skipped
`validate-skills`, `changes`, `tools-tests-linux` or
`windows-offline-checks` job on an event that should run it is INCOMPLETE
with the job named, while the lawful `gate-guard` skip on a push and the
three advisory skips on a pull request stay COMPLETE.

`TokenHeaderRefusalTests` and `ArtifactCellTests` close the two MINOR
findings the #740 final review r4 carried into this follow-up round: F-r4-1
(a malformed `--token-env` value escaped as a traceback that quoted the raw
token, exit 1) and F-r4-2 (the artifact cell read `none_uploaded` on every
row). The F-r4-1 tests build their own fake-response/fake-opener double
(A2: the F7 tests patch nothing) and keep the NUL leg off the environment
(B1: an embedded NUL cannot be stored in a Windows environment variable -
`os.environ["V"] = "a\0b"` and `mock.patch.dict(os.environ, ...)` both
raise `ValueError: embedded null character`), so the assertion survives the
tools-tests-windows job.
"""

from __future__ import annotations

import hashlib
import io
import json
import os
from pathlib import Path
import socket
import sys
import tempfile
import traceback
import unittest
from unittest import mock
import urllib.request

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from tools.aegis_delivery_control import ci_durations  # noqa: E402
from tools.aegis_delivery_control.cli import main  # noqa: E402

HEAD = "4d5ccb0b38369812bef198b7083d113d559ad387"
OTHER_HEAD = "6ea8a723" + "0" * 32
RUN_ID = "38198781208"
A1_RUN_ID = "38184781825"
NOW = "2026-10-12T04:00:00Z"
API = ("https://api.github.com/repos/ModernNomad-98/Project-Aegis"
       "/actions/runs/")
TOKEN_SENTINEL = "ghp_SENTINELtokenVALUE0123456789"
UPLOAD_EXPIRES = "2026-11-01T00:00:00Z"


def _iso(second):
    return "2026-10-12T03:%02d:%02dZ" % (second // 60, second % 60)


STEP_NAMES = (
    "Set up job", "Checkout", "Validate the skill library",
    "Verify DCO sign-off on every commit", "pr-body-skills-check",
    "Retain offline-check evidence", "Complete job")


def steps(event, dco="success", pr_body="success"):
    """The step list the API returns for validate-skills (F4 fixture).

    `.github/workflows/validate-skills.yml` L260-274 runs both PR-only steps
    when `github.event_name == 'pull_request'`; on any other event the API
    reports them `skipped`.
    """
    return [{"name": name,
             "conclusion": ("skipped" if event != "pull_request"
                            else {"Verify DCO sign-off on every commit": dco,
                                  "pr-body-skills-check": pr_body}.get(
                                      name, "success"))}
            for name in STEP_NAMES]


# F-r4-2: a sentinel meaning "this record says nothing about artifacts". The
# live jobs endpoint carries no `artifacts` key at all (runs 38198781208 and
# 38212458000: `.jobs[] | has("artifacts")` -> false for all six), so the
# `job()` default omits the key instead of modelling `[]`; a test that needs
# a reported inventory passes `artifacts=[]` or a list explicitly.
ARTIFACTS_ABSENT = object()


def job(index, name, conclusion, start=None, end=None, html=None,
        step_list=None, artifacts=ARTIFACTS_ABSENT):
    entry = {"id": 100 + index, "name": name, "status": "completed",
             "conclusion": conclusion,
             "html_url": html or ("%s%s/job/%d" % (API, RUN_ID, 100 + index))}
    if artifacts is not ARTIFACTS_ABSENT:
        entry["artifacts"] = artifacts
    entry["started_at"] = _iso(start) if start is not None else None
    entry["completed_at"] = _iso(end) if end is not None else None
    entry["steps"] = list(step_list) if step_list is not None else list(
        steps("push"))
    return entry


def run_payload(head=HEAD, conclusion="success", status="completed",
                attempt=1, event="push", run_id=RUN_ID):
    return {"id": run_id, "name": "validate-skills",
            "workflow_id": 269900000, "run_attempt": attempt, "event": event,
            "status": status, "conclusion": conclusion, "head_sha": head,
            "created_at": "2026-10-12T03:11:20Z",
            "updated_at": "2026-10-12T03:15:40Z"}


def green_jobs(event="push"):
    """The push fixture: six real durations, `gate-guard` legitimately skipped."""
    return [job(1, "changes", "success", 0, 7, step_list=steps(event)),
            job(2, "validate-skills", "success", 0, 109,
                step_list=steps(event)),
            job(3, "gate-guard", "skipped", 71, 70, step_list=steps(event)),
            job(4, "windows-offline-checks", "success", 30, 254,
                step_list=steps(event)),
            job(5, "tools-tests-linux", "success", 40, 172,
                step_list=steps(event)),
            job(6, "tools-tests-windows", "success", 50, 279,
                step_list=steps(event))]


def filler_jobs(prefix, first, last):
    """Ordinary out-of-roster jobs, for the multi-page fixtures (F8)."""
    return [job(1000 + index, "%s-%d" % (prefix, index), "success", 0, 1)
            for index in range(first, last + 1)]


def pr_jobs(dco="success", pr_body="success", gate="success"):
    """A pull_request fixture: `gate-guard` REQUIRED and executing (F2).

    `changes` executes here: the workflow gives it no `if:` (L57), so its
    skip is a gap (N1) rather than the path-filter skip SD-C2 assumed.
    """
    return [job(1, "changes", "success", 0, 6,
                step_list=steps("pull_request")),
            job(2, "validate-skills", "success", 0, 118,
                step_list=steps("pull_request", dco, pr_body)),
            job(3, "gate-guard", gate, 0, 7,
                step_list=steps("pull_request")),
            job(4, "windows-offline-checks", "success", 0, 209,
                step_list=steps("pull_request")),
            job(5, "tools-tests-linux", "success", 0, 151,
                step_list=steps("pull_request")),
            job(6, "tools-tests-windows", "success", 0, 246,
                step_list=steps("pull_request"))]


def a1_jobs():
    return [job(1, "changes", "success", 0, 8),
            job(2, "validate-skills", "success", 0, 111),
            job(3, "gate-guard", "skipped", None, None),
            job(4, "windows-offline-checks", "success", 30, 271),
            job(5, "tools-tests-linux", "success", 40, 140),
            job(6, "tools-tests-windows", "success", 50, 215)]


ENTRY = object()


def fixture(jobs=None, run=None, run_id=RUN_ID, with_runs_list=False,
            head=HEAD, total_count=ENTRY, extra_pages=None):
    run = run if run is not None else run_payload(head=head, run_id=run_id)
    jobs = green_jobs() if jobs is None else jobs
    base = "%s%s" % (API, run_id)
    total = len(jobs) if total_count is ENTRY else total_count
    mapping = {base: run,
               "%s/jobs?per_page=100" % base:
                   {"total_count": total, "jobs": jobs}}
    for page, page_jobs in (extra_pages or {}).items():
        mapping["%s/jobs?per_page=100&page=%d" % (base, page)] = {
            "total_count": total, "jobs": page_jobs}
    if with_runs_list:
        mapping[("https://api.github.com/repos/ModernNomad-98/Project-Aegis"
                 "/actions/workflows/validate-skills.yml/runs?head_sha=%s"
                 "&per_page=100" % head)] = {"total_count": 1,
                                             "workflow_runs": [run]}
    return mapping


def paginated_fixture(pages, run_id=RUN_ID, head=HEAD, total_count=ENTRY):
    """A multi-page fixture: `pages` is a list of job lists, page 1 first."""
    run = run_payload(head=head, run_id=run_id)
    base = "%s%s" % (API, run_id)
    total = sum(len(page) for page in pages) \
        if total_count is ENTRY else total_count
    mapping = {base: run}
    for index, page_jobs in enumerate(pages, 1):
        url = ("%s/jobs?per_page=100" % base if index == 1
               else "%s/jobs?per_page=100&page=%d" % (base, index))
        mapping[url] = {"total_count": total, "jobs": page_jobs}
    return mapping


def invoke(jobs=None, run=None, run_id=RUN_ID, argv=(), fixture_path=ENTRY,
           with_runs_list=False, head=HEAD, artifact_dir=None, **kwargs):
    """Run the command in-process against a fixture; returns (code, stdout)."""
    if fixture_path is ENTRY:
        fixture_path = _write_fixture(
            fixture(jobs=jobs, run=run, run_id=run_id,
                    with_runs_list=with_runs_list, head=head, **kwargs))
    args = ["--repository-id", "p0a-a2", "ci-durations", "--now", NOW]
    if run_id is not None:
        args += ["--run-id", run_id]
    if fixture_path is not None:
        args += ["--fixture", str(fixture_path)]
    if artifact_dir is not None:
        args += ["--artifact-dir", str(artifact_dir)]
    args += list(argv)
    out, err = io.StringIO(), io.StringIO()
    with mock.patch("sys.stdout", out), mock.patch("sys.stderr", err):
        code = main(args)
    return code, out.getvalue(), err.getvalue()


_TEMP = []


def _write_fixture(mapping):
    handle = tempfile.NamedTemporaryFile(
        "w", suffix=".json", delete=False, encoding="utf-8", newline="\n")
    json.dump(mapping, handle)
    handle.close()
    _TEMP.append(handle.name)
    return Path(handle.name)


def evidence_of(jobs=None, run=None, run_id=RUN_ID, **kwargs):
    code, text, _ = invoke(jobs=jobs, run=run, run_id=run_id,
                           argv=("--format", "json", "--candidate", HEAD),
                           **kwargs)
    return code, json.loads(text)


def rows_of(evidence):
    return {row["job"]: row for row in evidence["jobs"]}


def columns_of(text):
    block = text.split("## ci-durations jobs")[1].split("\n\n")[0]
    return [line for line in block.splitlines() if line.startswith("|")]


class RosterAndDurationsTests(unittest.TestCase):
    """AC1, AC2, AC6: the six real durations and the skipped window."""

    def test_ac1_six_real_durations_and_skip(self):
        code, evidence = evidence_of()
        self.assertEqual(code, 0)
        durations = {name: row["duration_s"]
                     for name, row in rows_of(evidence).items()}
        self.assertEqual(durations, {
            "changes": 7, "validate-skills": 109, "gate-guard":
                "not_applicable", "windows-offline-checks": 224,
            "tools-tests-linux": 132, "tools-tests-windows": 229})

    def test_ac1_a1_cross_check_pair(self):
        _, evidence = evidence_of(jobs=a1_jobs(), run_id=A1_RUN_ID,
                                  run=run_payload(run_id=A1_RUN_ID))
        durations = {name: row["duration_s"]
                     for name, row in rows_of(evidence).items()}
        self.assertEqual(list(durations.values()),
                         [8, 111, "not_applicable", 241, 100, 165])

    def test_ac2_six_rows_and_identity_keys(self):
        _, evidence = evidence_of()
        self.assertEqual(len(evidence["jobs"]), 6)
        self.assertEqual([row["job"] for row in evidence["jobs"]],
                         list(ci_durations.JOB_ROSTER))
        identity = evidence["run_identity"]
        for key in ("repository", "workflow", "run_id", "run_attempt",
                    "run_head_sha", "fetched_at"):
            self.assertTrue(identity[key], key)
        self.assertEqual(evidence["status"], "COMPLETE")

    def test_ac6_skipped_windows_are_never_executed(self):
        for name, start, end in (("gate-guard", 71, 70),
                                 ("gate-guard", 71, 71),
                                 ("gate-guard", None, None)):
            with self.subTest(window=(start, end)):
                jobs = green_jobs()
                jobs[2] = job(3, name, "skipped", start, end)
                _, evidence = evidence_of(jobs=jobs)
                row = rows_of(evidence)[name]
                self.assertEqual(row["state"], "skipped")
                self.assertEqual(row["conclusion"], "skipped")
                self.assertEqual(row["duration_s"], "not_applicable")
                self.assertIn("event-filter", row["skip_reason"])
                self.assertNotEqual(row["duration_s"], 0)

    def test_ac6_zero_second_window_on_other_jobs(self):
        jobs = green_jobs()
        jobs[4] = job(5, "tools-tests-linux", "skipped", 60, 60)
        jobs[3] = job(4, "windows-offline-checks", "skipped", 30, 30)
        _, evidence = evidence_of(jobs=jobs)
        rows = rows_of(evidence)
        for name in ("tools-tests-linux", "windows-offline-checks"):
            self.assertEqual(rows[name]["duration_s"], "not_applicable")

    def test_ac6_null_window_executed_row_fails_closed(self):
        jobs = green_jobs()
        jobs[1] = job(2, "validate-skills", "success", None, None)
        code, evidence = evidence_of(jobs=jobs)
        row = rows_of(evidence)["validate-skills"]
        self.assertEqual(row["duration_s"], "not_recorded")
        self.assertEqual(evidence["status"], "INCOMPLETE")
        self.assertEqual(code, 1)
        self.assertIn("validate-skills", evidence["prerequisites"]
                      ["coverage_gaps"][0])

    def test_ac6_negative_executed_window_clamps_to_zero(self):
        jobs = green_jobs()
        jobs[0] = job(1, "changes", "success", 71, 60)
        _, evidence = evidence_of(jobs=jobs)
        row = rows_of(evidence)["changes"]
        self.assertEqual(row["duration_s"], 0)
        self.assertIn("executed-negative-window", row["note"])
        self.assertEqual(evidence["status"], "COMPLETE")

    def test_ac6_mutated_skipped_window_is_not_silently_accepted(self):
        jobs = green_jobs()
        jobs[2] = job(3, "gate-guard", "success", 71, 70)
        code, evidence = evidence_of(jobs=jobs)
        row = rows_of(evidence)["gate-guard"]
        self.assertEqual(row["state"], "executed")
        self.assertEqual(row["duration_s"], 0)
        self.assertEqual(row["coverage"], "demonstrated")
        self.assertNotEqual(row["duration_s"], "not_applicable")


class StatusHonestyTests(unittest.TestCase):
    """AC5, AC12: FAILED, UNBOUND, STALE, INCOMPLETE, roster drift."""

    def test_ac5_complete_requires_matching_candidate(self):
        code, _, _ = invoke(argv=("--candidate", HEAD))
        self.assertEqual(code, 0)

    def test_ac5_missing_candidate_is_unbound(self):
        code, text, _ = invoke()
        self.assertEqual(code, 1)
        self.assertIn("STATUS: UNBOUND", text)
        self.assertIn("candidate_sha: not_supplied", text)

    def test_ac5_differing_candidate_is_stale(self):
        code, text, _ = invoke(argv=("--candidate", OTHER_HEAD))
        self.assertEqual(code, 1)
        self.assertIn("STATUS: STALE", text)

    def test_ac5_non_completed_run_is_incomplete(self):
        run = run_payload(status="in_progress", conclusion=None)
        code, evidence = evidence_of(run=run)
        self.assertEqual(code, 1)
        self.assertEqual(evidence["status"], "INCOMPLETE")
        self.assertIn("run_status=in_progress", evidence["marker"]["reason"])

    def test_ac5_second_attempt_is_incomplete_with_attempt_recorded(self):
        code, evidence = evidence_of(run=run_payload(attempt=2))
        self.assertEqual(code, 1)
        self.assertEqual(evidence["status"], "INCOMPLETE")
        self.assertEqual(evidence["run_identity"]["run_attempt"], 2)
        self.assertIn("run_attempt=2", evidence["marker"]["reason"])

    def test_ac5_failed_run_is_failed_and_still_prints_six_rows(self):
        jobs = green_jobs()
        jobs[1] = job(2, "validate-skills", "failure", 0, 109)
        code, text, _ = invoke(
            jobs=jobs, run=run_payload(conclusion="failure"),
            argv=("--candidate", HEAD, "--format", "table"))
        self.assertEqual(code, 4)
        self.assertIn("STATUS: FAILED", text)
        self.assertIn("failing: validate-skills", text)
        self.assertEqual(len(columns_of(text)), 8)

    def test_ac5_cancelled_and_timed_out_runs_are_failed(self):
        for conclusion in ("cancelled", "timed_out"):
            with self.subTest(conclusion=conclusion):
                code, evidence = evidence_of(
                    run=run_payload(conclusion=conclusion))
                self.assertEqual(code, 4)
                self.assertEqual(evidence["status"], "FAILED")

    def test_r1_neutral_executed_job_is_not_green(self):
        jobs = green_jobs()
        jobs[4] = job(5, "tools-tests-linux", "neutral", 40, 172)
        code, evidence = evidence_of(jobs=jobs)
        self.assertEqual(code, 1)
        self.assertEqual(evidence["status"], "INCOMPLETE")
        self.assertIn("executed-job-not-green:tools-tests-linux",
                      evidence["marker"]["reason"])
        self.assertNotEqual(evidence["status"], "FAILED")

    def test_r1_run_conclusion_neutral_is_failed(self):
        code, evidence = evidence_of(run=run_payload(conclusion="neutral"))
        self.assertEqual(code, 4)
        self.assertEqual(evidence["status"], "FAILED")

    def test_ac12_roster_delta_is_visible_and_not_fatal(self):
        jobs = green_jobs() + [job(7, "markdown-links", "success", 0, 5)]
        code, evidence = evidence_of(jobs=jobs)
        self.assertEqual(code, 1)
        self.assertEqual(evidence["status"], "INCOMPLETE")
        self.assertEqual(evidence["prerequisites"]["roster_delta"],
                         ["markdown-links"])
        self.assertEqual(len(evidence["jobs"]), 6)

    def test_ac12_missing_roster_job_is_missing_not_a_pass(self):
        jobs = [entry for entry in green_jobs()
                if entry["name"] != "changes"]
        code, evidence = evidence_of(jobs=jobs)
        row = rows_of(evidence)["changes"]
        self.assertEqual(row["state"], "missing")
        self.assertEqual(row["coverage"], "not_demonstrated")
        self.assertEqual(code, 1)
        self.assertIn("changes", evidence["marker"]["reason"])

    def test_unresolved_conclusion_is_incomplete(self):
        jobs = green_jobs()
        jobs[5] = job(6, "tools-tests-windows", None, 50, 279)
        jobs[5]["status"] = "in_progress"
        code, evidence = evidence_of(jobs=jobs)
        self.assertEqual(rows_of(evidence)["tools-tests-windows"]["state"],
                         "unresolved")
        self.assertEqual(code, 1)


class OfflineProofTests(unittest.TestCase):
    """AC3, AC4, AC11: determinism, the socket-layer proof, no auto-run."""

    def test_ac3_two_invocations_are_byte_identical(self):
        for fmt in ("table", "json"):
            with self.subTest(format=fmt):
                path = _write_fixture(fixture())
                first = invoke(fixture_path=path,
                               argv=("--candidate", HEAD, "--format", fmt))[1]
                second = invoke(fixture_path=path,
                                argv=("--candidate", HEAD, "--format", fmt))[1]
                self.assertEqual(hashlib.sha256(first.encode()).hexdigest(),
                                 hashlib.sha256(second.encode()).hexdigest())

    def test_ac4_zero_sockets_and_no_transport_on_the_fixture_path(self):
        def explode(*args, **kwargs):
            raise AssertionError("the fixture path touched the network")

        built = []
        real_transport = ci_durations.HttpTransport

        def spy(token=None):
            built.append(token)
            return real_transport(token)

        with mock.patch.object(socket, "socket", explode), \
                mock.patch.object(urllib.request, "urlopen", explode), \
                mock.patch.object(ci_durations, "HttpTransport", spy):
            code, text, _ = invoke(argv=("--candidate", HEAD))
        self.assertEqual(code, 0)
        self.assertIn("STATUS: COMPLETE", text)
        self.assertEqual(built, [])
        self.assertIn("fixture_precedence: True", text)

    def test_ac4_allow_network_does_not_beat_the_fixture(self):
        def explode(*args, **kwargs):
            raise AssertionError("precedence failed: the network was used")

        with mock.patch.object(socket, "socket", explode), \
                mock.patch.object(urllib.request, "urlopen", explode):
            code, _, _ = invoke(
                argv=("--candidate", HEAD, "--allow-network"))
        self.assertEqual(code, 0)

    def test_ac4_no_fixture_and_no_flag_refuses_with_exit_two(self):
        code, text, err = invoke(fixture_path=None)
        self.assertEqual(code, 2)
        self.assertEqual(text, "")
        self.assertIn("--fixture", err)
        self.assertIn("--allow-network", err)

    def test_ac4_malformed_fixture_refuses_with_exit_two(self):
        path = Path(tempfile.mkstemp(suffix=".json")[1])
        path.write_text("{not json", encoding="utf-8")
        code, _, err = invoke(fixture_path=path)
        self.assertEqual(code, 2)
        self.assertIn("not valid JSON", err)

    def test_ac4_fixture_missing_a_payload_refuses(self):
        path = _write_fixture({})
        code, _, err = invoke(fixture_path=path)
        self.assertEqual(code, 2)
        self.assertIn("no payload", err)

    def test_ac4_non_success_fixture_status_is_a_transport_failure(self):
        mapping = fixture()
        key = "%s%s" % (API, RUN_ID)
        mapping[key] = {"status": 500, "body": mapping[key]}
        code, _, err = invoke(fixture_path=_write_fixture(mapping))
        self.assertEqual(code, 3)
        self.assertIn("HTTP 500", err)

    def test_ac4_head_resolution_reads_the_runs_list(self):
        path = _write_fixture(fixture(with_runs_list=True))
        code, text, _ = invoke(run_id=None, fixture_path=path,
                               argv=("--candidate", HEAD, "--head", HEAD))
        self.assertEqual(code, 0)
        self.assertIn("actions/workflows/validate-skills.yml/runs?head_sha=",
                      text)
        self.assertIn("per_page=100", text)
        code, _, err = invoke(run_id=None, fixture_path=_write_fixture({}),
                              argv=("--head", HEAD))
        self.assertEqual(code, 2)
        self.assertIn("no payload", err)

    def test_ac11_identity_block_is_fixed_and_exits_zero(self):
        code, text, _ = invoke(argv=("--show-identity",))
        self.assertEqual(code, 0)
        block = json.loads(text)
        self.assertEqual(block, ci_durations.identity())
        self.assertEqual(block["hosts"], ["api.github.com"])
        self.assertEqual(block["mutating_verbs"], [])
        self.assertEqual(block["network_default"], "off")
        self.assertTrue(block["read_only"])
        self.assertFalse(block["writes_files"])
        self.assertEqual(sorted(block["exit_codes"]),
                         ["0", "1", "2", "3", "4"])

    def test_ac11_no_argument_can_select_a_host(self):
        parser = ci_durations.build_parser(
            __import__("argparse").ArgumentParser().add_subparsers())
        options = {action.dest for action in parser._actions}
        for forbidden in ("api_base", "host", "base_url", "server"):
            self.assertNotIn(forbidden, options)
        self.assertEqual(ci_durations.FIXED_HOST, "api.github.com")


class ArtifactMappingTests(unittest.TestCase):
    """AC8: exit codes only from the real names, only head-bound."""

    def write_artifacts(self, directory, names, checkout_sha=HEAD,
                        exit_code=0):
        root = Path(directory)
        for name in names:
            folder = root / name
            folder.mkdir(parents=True, exist_ok=True)
            (folder / "delivery-control.json").write_text(
                json.dumps({"label": "delivery-control",
                            "checkout_sha": checkout_sha,
                            "exit_code": exit_code,
                            "elapsed_seconds": 1.5}),
                encoding="utf-8")

    def test_ac8_real_names_map_to_their_jobs(self):
        with tempfile.TemporaryDirectory() as directory:
            self.write_artifacts(directory, [
                "offline-checks-linux-38198781208-1",
                "offline-checks-windows-38198781208-1",
                "tools-tests-linux-38198781208-1",
                "tools-tests-windows-38198781208-1"], exit_code=0)
            code, evidence = evidence_of(artifact_dir=directory)
        rows = rows_of(evidence)
        self.assertEqual(code, 0)
        for name in ("validate-skills", "windows-offline-checks",
                     "tools-tests-linux", "tools-tests-windows"):
            self.assertEqual(rows[name]["exit_code"], 0)
            self.assertEqual(rows[name]["exit_codes"],
                             [["delivery-control", 0]])
            self.assertIn("bound_by=checkout_sha",
                          rows[name]["exit_codes_provenance"])
            self.assertIn("delivery-control.json",
                          rows[name]["exit_codes_provenance"])
        self.assertEqual(rows["changes"]["exit_code"], "not_recorded")
        self.assertEqual(rows["gate-guard"]["exit_code"], "not_recorded")
        self.assertEqual(evidence["prerequisites"]["artifact_unmapped"], [])

    def test_ac8_head_mismatch_is_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            self.write_artifacts(directory,
                                 ["offline-checks-linux-38198781208-1"],
                                 checkout_sha="f" * 40)
            code, evidence = evidence_of(artifact_dir=directory)
        row = rows_of(evidence)["validate-skills"]
        self.assertEqual(code, 0)
        self.assertEqual(row["exit_code"], "not_recorded")
        self.assertIn("head mismatch", row["exit_code_provenance"])

    def test_ac8_unrecognised_directory_is_not_mapped(self):
        with tempfile.TemporaryDirectory() as directory:
            self.write_artifacts(directory, ["mystery-bundle-1-1"])
            _, evidence = evidence_of(artifact_dir=directory)
        unmapped = evidence["prerequisites"]["artifact_unmapped"]
        self.assertEqual(len(unmapped), 1)
        self.assertIn("mystery-bundle-1-1", unmapped[0])
        self.assertIn("not_mapped", unmapped[0])

    def test_ac8_no_directory_leaves_every_exit_code_not_recorded(self):
        _, evidence = evidence_of()
        for row in evidence["jobs"]:
            self.assertEqual(row["exit_code"], "not_recorded")
        self.assertEqual(evidence["prerequisites"]["artifact_retention"],
                         "14d")

    def test_ac8_missing_artifact_directory_refuses(self):
        code, _, err = invoke(artifact_dir="no-such-directory-here")
        self.assertEqual(code, 2)
        self.assertIn("artifact directory not found", err)


def reported_upload(run_id=RUN_ID):
    """An uploaded artifact as the jobs payload reports it (F-r4-2)."""
    return {"id": 77, "name": "offline-checks-linux-%s-1" % run_id,
            "size_in_bytes": 4321, "expires_at": UPLOAD_EXPIRES,
            "expired": False}


def jobs_reporting(reported):
    """`green_jobs()` where only the named records carry an `artifacts` key.

    F-r4-2: key presence is the payload's own per-job statement, so this is
    the mixed shape that distinguishes a reported empty inventory from a
    record that said nothing at all.
    """
    return [dict(entry, artifacts=reported[entry["name"]])
            if entry["name"] in reported else entry
            for entry in green_jobs()]


class _FakeResponse:
    """The response surface the real `fetch` uses (F-r4-1 tests; A2).

    The F7 tests patch nothing, so this double is new test code. AF-2: the
    default `url` is a fixed-host URL on purpose - the real `fetch` checks
    `_same_host_target(resp.geturl())` before it reads the body, and
    `_same_host_target(None)` is False, so a default of None would fail every
    leg for the wrong reason. A leg that wants another URL passes one.
    """

    def __init__(self, body=b"{}", status=200,
                 url="https://api.github.com/"):
        self._body, self._status, self._url = body, status, url

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def getcode(self):
        return self._status

    def geturl(self):
        return self._url

    def read(self):
        return self._body


class _FakeOpener:
    """Records the Request; returns a response or raises (F-r4-1 tests)."""

    def __init__(self, response=None, raises=None):
        self.requests, self._response, self._raises = [], response, raises

    def open(self, request, timeout=None):
        self.requests.append(request)
        if self._raises is not None:
            raise self._raises
        return self._response


class TokenHeaderRefusalTests(unittest.TestCase):
    """F-r4-1: a malformed token refuses value-free and is never echoed."""

    URL = ("https://api.github.com/repos/ModernNomad-98/Project-Aegis"
           "/actions/runs/38198781208")

    def _spy(self):
        built = []
        real_transport = ci_durations.HttpTransport

        def spy(token=None):
            built.append(token)
            return real_transport(token)

        return built, spy

    def test_fr41_control_char_token_refuses_before_any_transport(self):
        token = "ghp_" + TOKEN_SENTINEL + "\r\nX-Inject: 1"
        built, spy = self._spy()
        with mock.patch.dict(os.environ, {"AEGIS_TOKEN": token}), \
                mock.patch.object(ci_durations, "HttpTransport", spy):
            code, out, err = invoke(fixture_path=None,
                                    argv=("--allow-network", "--token-env",
                                          "AEGIS_TOKEN"))
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertNotIn(TOKEN_SENTINEL, out + err)
        self.assertEqual(built, [])
        self.assertIn("--token-env", err)

    def test_fr41_nul_value_refuses_by_the_helper_and_the_mocked_environment(
            self):
        # B1: an embedded NUL cannot travel through a real environment
        # variable on this host - os.environ["V"] = "a\0b" and
        # mock.patch.dict(os.environ, {"V": "a\0b"}) both raise
        # `ValueError: embedded null character` - so the NUL assertion is
        # kept and moved off the environment: the helper is called directly,
        # and the CLI leg patches os.environ.get with a fall-through.
        nul_value = "ghp_" + TOKEN_SENTINEL + "\0"
        defect = ci_durations.token_header_defect(nul_value)
        self.assertIsNotNone(defect)
        self.assertNotIn(TOKEN_SENTINEL, defect)

        real_get = os.environ.get
        built, spy = self._spy()

        def mocked_get(key, default=None):
            if key == "AEGIS_TOKEN":
                return nul_value
            return real_get(key, default)

        with mock.patch("os.environ.get", side_effect=mocked_get), \
                mock.patch.object(ci_durations, "HttpTransport", spy):
            code, out, err = invoke(fixture_path=None,
                                    argv=("--allow-network", "--token-env",
                                          "AEGIS_TOKEN"))
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertNotIn(TOKEN_SENTINEL, out + err)
        self.assertEqual(built, [])

    def test_fr41_u2028_value_refuses_before_any_transport(self):
        # B1: U+2028 does round-trip through os.environ on Windows, so this
        # leg stays at the environment/CLI level. It is not latin-1
        # encodable, so the helper's encode check refuses it.
        token = "ghp_" + TOKEN_SENTINEL + "\u2028y"
        built, spy = self._spy()
        with mock.patch.dict(os.environ, {"AEGIS_TOKEN": token}), \
                mock.patch.object(ci_durations, "HttpTransport", spy):
            code, out, err = invoke(fixture_path=None,
                                    argv=("--allow-network", "--token-env",
                                          "AEGIS_TOKEN"))
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertNotIn(TOKEN_SENTINEL, out + err)
        self.assertEqual(built, [])

    def test_fr41_legal_token_still_builds_the_bearer_header(self):
        token = "ghp_" + TOKEN_SENTINEL
        transport = ci_durations.HttpTransport(token)
        opener = _FakeOpener(response=_FakeResponse(body=b'{"ok": true}'))
        with mock.patch.object(transport, "_opener", opener):
            payload, status = transport.fetch(self.URL)
        request = opener.requests[0]
        self.assertEqual(request.get_header("Authorization"),
                         "Bearer " + token)
        self.assertEqual(payload, {"ok": True})
        self.assertEqual(status, 200)
        self.assertEqual(
            {key.lower(): value for key, value in request.headers.items()},
            {"accept": "application/vnd.github+json",
             "x-github-api-version": ci_durations.API_VERSION,
             "user-agent": ci_durations.USER_AGENT,
             "authorization": "Bearer " + token})

    def test_fr41_no_token_sends_no_authorization_header(self):
        # B3: HttpTransport() is the default anonymous live path.
        self.assertIsNone(ci_durations.token_header_defect(None))
        self.assertIsNone(ci_durations.token_header_defect(""))
        transport = ci_durations.HttpTransport()
        opener = _FakeOpener(response=_FakeResponse(body=b'{"ok": true}'))
        with mock.patch.object(transport, "_opener", opener):
            payload, status = transport.fetch(self.URL)
        self.assertIsNone(opener.requests[0].get_header("Authorization"))
        self.assertEqual(payload, {"ok": True})
        self.assertEqual(status, 200)

        # A3 second leg: redact_token leaves a token-less message untouched,
        # so the placeholder is never interleaved through its characters.
        error = urllib.error.URLError("boom")
        failing = ci_durations.HttpTransport()
        with mock.patch.object(failing, "_opener", _FakeOpener(raises=error)):
            with self.assertRaises(ci_durations.TransportFailure) as caught:
                failing.fetch(self.URL)
        self.assertEqual(str(caught.exception),
                         "transport error for %s: %s" % (self.URL, error))
        self.assertNotIn(ci_durations.TOKEN_REDACTED,
                         str(caught.exception))

    def test_fr41_header_quoting_valueerror_is_redacted_and_uncaused(self):
        token = "ghp_" + TOKEN_SENTINEL
        transport = ci_durations.HttpTransport(token)
        opener = _FakeOpener(raises=ValueError(
            "Invalid header value b'Bearer %s'" % token))
        with mock.patch.object(transport, "_opener", opener):
            with self.assertRaises(ci_durations.TransportFailure) as caught:
                transport.fetch(self.URL)
        text = str(caught.exception)
        self.assertNotIn(TOKEN_SENTINEL, text)
        self.assertNotIn(token, text)
        self.assertIn("redacted", text)
        self.assertIsNone(caught.exception.__cause__)
        printed = "".join(traceback.format_exception(caught.exception))
        self.assertNotIn(TOKEN_SENTINEL, printed)
        self.assertNotIn("Invalid header value", printed)

    def test_fr41_decode_failure_is_not_reported_as_a_rejected_request_value(
            self):
        # B4: UnicodeDecodeError is a ValueError subclass and the body read
        # sits inside the same try block, so it must keep its base
        # disposition instead of inheriting the request-value diagnosis.
        transport = ci_durations.HttpTransport("ghp_" + TOKEN_SENTINEL)
        opener = _FakeOpener(response=_FakeResponse(body=b"\xff\xfe"))
        with mock.patch.object(transport, "_opener", opener):
            with self.assertRaises(UnicodeDecodeError) as caught:
                transport.fetch(self.URL)
        self.assertNotIsInstance(caught.exception,
                                 ci_durations.TransportFailure)
        self.assertNotIn("request value was rejected",
                         str(caught.exception))
        self.assertNotIn(ci_durations.TOKEN_REDACTED, str(caught.exception))

    def test_fr41_cli_reports_exit_three_without_a_traceback(self):
        token = "ghp_" + TOKEN_SENTINEL
        error = ValueError("Invalid header value b'Bearer %s'" % token)
        with mock.patch.dict(os.environ, {"AEGIS_TOKEN": token}), \
                mock.patch.object(urllib.request, "build_opener",
                                  lambda *args, **kwargs: _FakeOpener(
                                      raises=error)):
            code, out, err = invoke(fixture_path=None,
                                    argv=("--allow-network", "--token-env",
                                          "AEGIS_TOKEN"))
        self.assertEqual(code, 3)
        self.assertEqual(out, "")
        self.assertNotIn(TOKEN_SENTINEL, err)
        self.assertNotIn("Traceback", err)
        self.assertIn("ci-durations transport failure:", err)
        self.assertIn("redacted", err)


class ArtifactCellTests(unittest.TestCase):
    """F-r4-2: the cell reports the payload's own per-job statement."""

    OTHERS = ("changes", "gate-guard", "windows-offline-checks",
              "tools-tests-linux", "tools-tests-windows")

    def test_fr42_no_inventory_reads_not_recorded(self):
        # The live shape: no record carries an artifacts key at all.
        code, evidence = evidence_of(jobs=green_jobs())
        self.assertEqual(code, 0)
        self.assertEqual(len(evidence["jobs"]), len(ci_durations.JOB_ROSTER))
        for row in evidence["jobs"]:
            self.assertEqual(row["artifact"], "not_recorded")

    def test_fr42_reported_upload_maps_by_prefix_to_validate_skills(self):
        upload = reported_upload()
        code, evidence = evidence_of(
            jobs=jobs_reporting({"validate-skills": [upload]}))
        rows = rows_of(evidence)
        cell = rows["validate-skills"]["artifact"]
        self.assertIn(upload["name"], cell)
        self.assertIn("id=%s" % upload["id"], cell)
        self.assertIn("bytes=%s" % upload["size_in_bytes"], cell)
        self.assertIn("expires=%s" % upload["expires_at"], cell)
        self.assertIn("expired=False", cell)
        for name in self.OTHERS:
            self.assertNotIn(upload["name"], rows[name]["artifact"])
            self.assertEqual(rows[name]["artifact"], "not_recorded")
        self.assertEqual(code, 0)

    def test_fr42_reported_but_empty_inventory_reads_none_uploaded(self):
        code, evidence = evidence_of(
            jobs=[dict(entry, artifacts=[]) for entry in green_jobs()])
        self.assertEqual(code, 0)
        for row in evidence["jobs"]:
            self.assertEqual(row["artifact"], "none_uploaded")

    def test_fr42_mixed_payload_marks_only_the_reporting_job(self):
        # Sub-case 1: one record reports an empty inventory, the other five
        # say nothing - the shape revision 1's payload-global flag got wrong.
        with self.subTest(reported="empty-inventory"):
            _, evidence = evidence_of(
                jobs=jobs_reporting({"validate-skills": []}))
            rows = rows_of(evidence)
            self.assertEqual(rows["validate-skills"]["artifact"],
                             "none_uploaded")
            for name in self.OTHERS:
                self.assertEqual(rows[name]["artifact"], "not_recorded")
        # Sub-case 2: one record reports a real upload, the other five say
        # nothing - no silent job's row may claim none_uploaded.
        with self.subTest(reported="real-upload"):
            upload = reported_upload()
            _, evidence = evidence_of(
                jobs=jobs_reporting({"validate-skills": [upload]}))
            rows = rows_of(evidence)
            self.assertIn(upload["name"],
                          rows["validate-skills"]["artifact"])
            for name in self.OTHERS:
                self.assertEqual(rows[name]["artifact"], "not_recorded")

    def test_fr42_unmapped_artifact_name_is_never_attributed(self):
        mystery = {"id": 9, "name": "mystery-bundle-1-1",
                   "size_in_bytes": 1, "expires_at": UPLOAD_EXPIRES,
                   "expired": False}
        _, evidence = evidence_of(
            jobs=jobs_reporting({"validate-skills": [mystery]}))
        for row in evidence["jobs"]:
            self.assertNotIn("mystery-bundle-1-1", row["artifact"])
        # The record DID report an inventory, so its own row is an observed
        # absence - and a payload name never reaches the --artifact-dir
        # surface, which only a filesystem scan feeds.
        self.assertEqual(rows_of(evidence)["validate-skills"]["artifact"],
                         "none_uploaded")
        self.assertEqual(evidence["prerequisites"]["artifact_unmapped"], [])

    def test_fr42_missing_roster_job_artifact_is_not_recorded(self):
        jobs = [entry for entry in green_jobs()
                if entry["name"] != "changes"]
        code, evidence = evidence_of(jobs=jobs)
        row = rows_of(evidence)["changes"]
        self.assertEqual(row["state"], "missing")
        self.assertEqual(row["artifact"], "not_recorded")
        self.assertEqual(code, 1)

    def test_fr42_the_cell_is_not_a_constant(self):
        _, mapped = evidence_of(
            jobs=jobs_reporting({"validate-skills": [reported_upload()]}))
        _, empty = evidence_of(
            jobs=[dict(entry, artifacts=[]) for entry in green_jobs()])
        _, silent = evidence_of(jobs=green_jobs())
        values = {rows_of(mapped)["validate-skills"]["artifact"],
                  rows_of(empty)["validate-skills"]["artifact"],
                  rows_of(silent)["validate-skills"]["artifact"]}
        self.assertEqual(len(values), 3)


class EscapingTests(unittest.TestCase):
    """AC7: hostile payload strings cannot forge a row or a marker."""

    def test_ac7_hostile_strings_stay_on_one_line(self):
        hostile = ("evil" + chr(10) + "| fake | row |" + chr(27) + "[31m"
                   + chr(9) + "x" * 400)
        jobs = green_jobs()
        jobs[0] = job(1, "changes", "success", 0, 7, html=hostile)
        code, text, _ = invoke(
            jobs=jobs, argv=("--candidate", HEAD, "--format", "table"))
        self.assertEqual(code, 0)
        escaped = ci_durations.escape_text(hostile)
        for control in (chr(10), chr(13), chr(9), chr(27)):
            self.assertNotIn(control, escaped)
        self.assertIn(chr(92) + "x0a", escaped)
        self.assertIn(chr(92) + "x1b", escaped)
        self.assertIn(chr(92) + "x09", escaped)
        self.assertIn(chr(92) + "|", escaped)
        self.assertIn("[truncated", escaped)
        self.assertEqual(len(text.splitlines()),
                         len(ci_durations.render_table(
                             evidence_of()[1]).splitlines()))
        for line in text.splitlines():
            self.assertNotIn(chr(27), line)
        self.assertEqual(text.count("STATUS: "), 1)

    def test_ac7_json_and_table_agree_on_one_escape_rule(self):
        """F10: one canonical rule - the JSON string IS the table cell."""
        hostile = "line1" + chr(10) + "line2" + chr(27) + "|end"
        jobs = green_jobs()
        jobs[5] = job(6, "tools-tests-windows", "success", 50, 279,
                      html=hostile)
        _, evidence = evidence_of(jobs=jobs)
        row = rows_of(evidence)["tools-tests-windows"]
        escaped = ci_durations.escape_text(hostile)
        self.assertEqual(row["log_url"], hostile)
        for control in (chr(10), chr(13), chr(27)):
            self.assertNotIn(control, escaped)
        self.assertIn(chr(92) + "x0a", escaped)
        self.assertIn(chr(92) + "x1b", escaped)
        self.assertIn(chr(92) + "|", escaped)
        code, text, _ = invoke(jobs=jobs,
                               argv=("--candidate", HEAD, "--format", "table"))
        self.assertEqual(code, 0)
        cell = [column for column in columns_of(text)
                if column.startswith("| tools-tests-windows ")][0]
        self.assertIn(escaped, cell)
        self.assertNotIn(escaped.replace(chr(92), chr(92) * 2), cell)

    def test_ac7_escape_rules_are_exact(self):
        self.assertEqual(ci_durations.escape_text("a|b"), "a" + chr(92) + "|b")
        self.assertEqual(ci_durations.escape_text("a" + chr(92) + "b"),
                         "a" + chr(92) * 2 + "b")
        self.assertEqual(ci_durations.escape_text("tab\there"),
                         "tab" + chr(92) + "x09here")
        self.assertEqual(ci_durations.escape_text(None), "")
        long_text = ci_durations.escape_text("y" * 500)
        self.assertTrue(long_text.startswith("y" * 300))
        self.assertIn("[truncated 200]", long_text)




class RepairRoundTests(unittest.TestCase):
    """SD-D F1-F9 and the nine Codex findings: the negative fixtures.

    Each case is the exact payload the finding was reproduced with, so the
    suite fails if the honest behaviour regresses.
    """

    def test_f1_missing_head_sha_may_not_certify_complete(self):
        run = run_payload()
        del run["head_sha"]
        code, evidence = evidence_of(run=run)
        self.assertEqual(evidence["run_identity"]["candidate_status"],
                         "unresolvable")
        self.assertEqual(evidence["run_identity"]["run_head_sha"],
                         "not_recorded")
        self.assertEqual(evidence["status"], "INCOMPLETE")
        self.assertEqual(code, 1)
        self.assertIn("candidate_status=unresolvable",
                      evidence["marker"]["reason"])
        self.assertEqual(evidence["run_identity"]["stale"], False)

    def test_f1_non_string_head_sha_may_not_certify_complete(self):
        run = run_payload()
        run["head_sha"] = 12345
        code, evidence = evidence_of(run=run)
        self.assertEqual(evidence["run_identity"]["candidate_status"],
                         "unresolvable")
        self.assertEqual(evidence["status"], "INCOMPLETE")
        self.assertEqual(code, 1)
        self.assertIn("candidate_status=unresolvable",
                      evidence["marker"]["reason"])

    def test_f1_empty_string_head_sha_may_not_certify_complete(self):
        run = run_payload(head="")
        code, evidence = evidence_of(run=run)
        self.assertEqual(evidence["status"], "INCOMPLETE")
        self.assertEqual(code, 1)

    def test_f2_pull_request_skipped_gate_guard_is_not_complete(self):
        jobs = pr_jobs(gate="skipped")
        code, evidence = evidence_of(jobs=jobs,
                                     run=run_payload(event="pull_request"))
        row = rows_of(evidence)["gate-guard"]
        self.assertEqual(row["state"], "skipped")
        self.assertEqual(evidence["status"], "INCOMPLETE")
        self.assertEqual(code, 1)
        self.assertIn("required-job-skipped:gate-guard",
                      evidence["marker"]["reason"])
        self.assertEqual(evidence["marker"]["skipped_required_jobs"],
                         ["gate-guard"])
        self.assertEqual(row["skip_reason"],
                         "unexpected-skip-for-event (gate-guard is not "
                         "filter-skippable on event=pull_request; the marker "
                         "is INCOMPLETE)")
        self.assertNotIn("event-filter", row["skip_reason"])
        self.assertEqual(evidence["marker"]["unexpected_skipped_jobs"],
                         ["gate-guard"])

    def test_f2_pull_request_executed_gate_guard_stays_complete(self):
        code, evidence = evidence_of(jobs=pr_jobs(),
                                     run=run_payload(event="pull_request"))
        self.assertEqual(evidence["status"], "COMPLETE")
        self.assertEqual(code, 0)
        self.assertEqual(evidence["marker"]["skipped_required_jobs"], [])

    def test_f2_push_skipped_gate_guard_remains_event_filter(self):
        code, evidence = evidence_of()
        self.assertEqual(evidence["status"], "COMPLETE")
        self.assertEqual(code, 0)
        self.assertIn("event-filter",
                      rows_of(evidence)["gate-guard"]["skip_reason"])

    def test_n1_pull_request_skipped_changes_is_not_legitimate(self):
        """N1 corrected SD-C2's claim.

        SD-C2 held that `changes` skipping on a filtered pull_request was
        expected. The workflow disagrees: `changes` (L57) has no `if:`, so
        it always runs, and its skip is an unexpected skip - INCOMPLETE.
        """
        jobs = pr_jobs()
        jobs[0] = job(1, "changes", "skipped", None, None,
                      step_list=steps("pull_request"))
        code, evidence = evidence_of(
            jobs=jobs, run=run_payload(event="pull_request"))
        self.assertEqual(rows_of(evidence)["changes"]["state"], "skipped")
        self.assertEqual(evidence["status"], "INCOMPLETE")
        self.assertEqual(code, 1)
        self.assertEqual(evidence["marker"]["unexpected_skipped_jobs"],
                         ["changes"])
        self.assertIn("unexpected-skip-for-event:changes",
                      evidence["marker"]["reason"])
        self.assertNotIn("event-filter",
                         rows_of(evidence)["changes"]["skip_reason"])

    def test_f4_pr_run_reports_both_steps_executed(self):
        _, evidence = evidence_of(jobs=pr_jobs(),
                                  run=run_payload(event="pull_request"))
        details = {item["step"]: item
                   for item in evidence["prerequisites"]["step_details"]}
        self.assertEqual(sorted(details), [
            "Verify DCO sign-off on every commit", "pr-body-skills-check"])
        for name, item in details.items():
            self.assertEqual(item["state"], "executed", name)
            self.assertIn("not a job", item["detail"])
        self.assertEqual(evidence["prerequisites"]["step_skipped"], [])

    def test_f4_push_run_reports_both_steps_skipped(self):
        _, evidence = evidence_of()
        details = {item["step"]: item
                   for item in evidence["prerequisites"]["step_details"]}
        for name, item in details.items():
            self.assertEqual(item["state"], "skipped", name)
        skipped = evidence["prerequisites"]["step_skipped"]
        self.assertEqual(len(skipped), 2)
        self.assertTrue(any("DCO" in line for line in skipped))
        self.assertTrue(any("pr-body-skills-check" in line for line in skipped))

    def test_f4_pr_run_failed_pr_body_step_is_not_claimed_skipped(self):
        _, evidence = evidence_of(
            jobs=pr_jobs(pr_body="failure"),
            run=run_payload(event="pull_request"))
        details = {item["step"]: item for item in
                   evidence["prerequisites"]["step_details"]}
        state = details["pr-body-skills-check"]["state"]
        self.assertEqual(state, "executed")
        self.assertIn("failure", details["pr-body-skills-check"]["detail"])

    def test_f4_absent_step_payload_is_not_recorded_not_skipped(self):
        jobs = green_jobs()
        for entry in jobs:
            entry.pop("steps", None)
        _, evidence = evidence_of(jobs=jobs)
        states = {item["step"]: item["state"] for item in
                  evidence["prerequisites"]["step_details"]}
        self.assertEqual(set(states.values()), {"not_recorded"})
        self.assertEqual(evidence["prerequisites"]["step_skipped"], [])

    def test_f3_unicode_separators_are_escaped(self):
        for character in (chr(0x85), chr(0x2028), chr(0x2029)):
            with self.subTest(character=hex(ord(character))):
                escaped = ci_durations.escape_text("a" + character + "b")
                self.assertNotIn(character, escaped)
                self.assertIn("x%02x" % ord(character), escaped)
                self.assertEqual(len(escaped.splitlines()), 1)

    def test_f3_hostile_unicode_adds_no_line_and_no_marker(self):
        clean = invoke(argv=("--candidate", HEAD,
                             "--format", "table"))[1]
        for character in (chr(0x85), chr(0x2028), chr(0x2029)):
            with self.subTest(character=hex(ord(character))):
                jobs = green_jobs()
                jobs[0] = job(1, "changes", "success", 0, 7,
                              html="evil" + character + "STATUS: FAILED (exit 4)")
                code, text, _ = invoke(
                    jobs=jobs, argv=("--candidate", HEAD,
                                     "--format", "table"))
                self.assertEqual(code, 0)
                self.assertIn("STATUS: COMPLETE", text)
                self.assertEqual(len(text.splitlines()),
                                 len(clean.splitlines()))
                marker_lines = [line for line in text.splitlines()
                                if line.startswith("STATUS: ")]
                self.assertEqual(len(marker_lines), 1)
                self.assertEqual(marker_lines[0].split(" reason:")[0],
                                 "STATUS: COMPLETE (exit 0)")

    def test_f5_every_bound_record_is_reported_not_only_the_first(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory) / ("offline-checks-linux-%s-1" % RUN_ID)
            folder.mkdir(parents=True)
            for name, label, code in (("acceptance-core.json",
                                       "acceptance-core", 5),
                                      ("ber.json", "ber", 0)):
                (folder / name).write_text(json.dumps({
                    "label": label, "checkout_sha": HEAD, "exit_code": code,
                    "elapsed_seconds": 1.0}), encoding="utf-8")
            code, evidence = evidence_of(artifact_dir=directory)
        row = rows_of(evidence)["validate-skills"]
        self.assertEqual(row["exit_codes"],
                         [["acceptance-core", 5], ["ber", 0]])
        self.assertEqual(row["exit_code"], "not_applicable")
        self.assertEqual(code, 0)
        self.assertIn("acceptance-core.json", row["exit_codes_provenance"])
        self.assertIn("ber.json", row["exit_codes_provenance"])

    def test_f5_one_agreeing_record_still_fills_the_singular_cell(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory) / ("offline-checks-linux-%s-1" % RUN_ID)
            folder.mkdir(parents=True)
            for name, label in (("a.json", "alpha"), ("b.json", "beta")):
                (folder / name).write_text(json.dumps({
                    "label": label, "checkout_sha": HEAD, "exit_code": 0,
                    "elapsed_seconds": 1.0}), encoding="utf-8")
            _, evidence = evidence_of(artifact_dir=directory)
        row = rows_of(evidence)["validate-skills"]
        self.assertEqual(row["exit_code"], 0)
        self.assertEqual(len(row["exit_codes"]), 2)

    def test_f6_pull_request_artifact_binds_on_pr_head_sha(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory) / ("offline-checks-linux-%s-1" % RUN_ID)
            folder.mkdir(parents=True)
            (folder / "delivery-control.json").write_text(json.dumps({
                "label": "delivery-control", "checkout_sha": "f" * 40,
                "pr_head_sha": HEAD, "exit_code": 0,
                "elapsed_seconds": 1.5}), encoding="utf-8")
            code, evidence = evidence_of(
                artifact_dir=directory,
                run=run_payload(event="pull_request"), jobs=pr_jobs())
        row = rows_of(evidence)["validate-skills"]
        self.assertEqual(code, 0)
        self.assertEqual(row["exit_codes"], [["delivery-control", 0]])
        self.assertIn("bound_by=pr_head_sha", row["exit_codes_provenance"])

    def test_f6_push_artifact_still_binds_on_checkout_sha(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory) / ("offline-checks-linux-%s-1" % RUN_ID)
            folder.mkdir(parents=True)
            (folder / "delivery-control.json").write_text(json.dumps({
                "label": "delivery-control", "checkout_sha": HEAD,
                "pr_head_sha": "e" * 40, "exit_code": 0,
                "elapsed_seconds": 1.5}), encoding="utf-8")
            _, evidence = evidence_of(artifact_dir=directory)
        row = rows_of(evidence)["validate-skills"]
        self.assertEqual(row["exit_codes"], [["delivery-control", 0]])
        self.assertIn("bound_by=checkout_sha", row["exit_codes_provenance"])

    def test_f6_pull_request_record_without_pr_head_is_a_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory) / ("offline-checks-linux-%s-1" % RUN_ID)
            folder.mkdir(parents=True)
            (folder / "delivery-control.json").write_text(json.dumps({
                "label": "delivery-control", "checkout_sha": HEAD,
                "pr_head_sha": None, "exit_code": 0}), encoding="utf-8")
            _, evidence = evidence_of(
                artifact_dir=directory,
                run=run_payload(event="pull_request"), jobs=pr_jobs())
        row = rows_of(evidence)["validate-skills"]
        self.assertEqual(row["exit_code"], "not_recorded")
        self.assertIn("head mismatch", row["exit_code_provenance"])
        self.assertIn("pr_head_sha", row["exit_code_provenance"])

    def test_f7_cross_host_redirect_is_refused_before_any_header(self):
        handler = ci_durations._FixedHostRedirectHandler()
        request = urllib.request.Request(
            "https://%s/repos/x/y/actions/runs/1" % ci_durations.FIXED_HOST,
            headers={"Authorization": "Bearer secret-token"}, method="GET")
        for target in ("https://evil.example/repos/x/y",
                       "http://%s/repos/x/y" % ci_durations.FIXED_HOST,
                       "https://api.github.com.evil.example/x"):
            with self.subTest(target=target):
                with self.assertRaises(urllib.error.HTTPError):
                    handler.redirect_request(request, None, 302, "Found", {},
                                             target)

    def test_f7_same_host_redirect_is_still_followed(self):
        handler = ci_durations._FixedHostRedirectHandler()
        request = urllib.request.Request(
            "https://%s/repos/x/y/actions/runs/1" % ci_durations.FIXED_HOST,
            headers={"Authorization": "Bearer secret-token"}, method="GET")
        redirect = handler.redirect_request(
            request, None, 302, "Found", {},
            "https://%s/repos/x/y/actions/runs/1/jobs" % ci_durations.FIXED_HOST)
        self.assertIsNotNone(redirect)
        self.assertEqual(redirect.host, ci_durations.FIXED_HOST)

    def test_f7_transport_installs_the_redirect_handler(self):
        transport = ci_durations.HttpTransport(token="t")
        handlers = [type(handler) for handler in transport._opener.handlers]
        self.assertIn(ci_durations._FixedHostRedirectHandler, handlers)
        source = Path(ci_durations.__file__).read_text(encoding="utf-8")
        self.assertIn("_FixedHostRedirectHandler", source)

    def test_f8_truncated_jobs_page_is_incomplete(self):
        path = _write_fixture(fixture(total_count=150))
        code, text, _ = invoke(fixture_path=path,
                               argv=("--candidate", HEAD, "--format", "json"))
        evidence = json.loads(text)
        identity = evidence["run_identity"]
        self.assertEqual(identity["jobs_total_count"], 150)
        self.assertEqual(identity["jobs_reported_total"], 6)
        self.assertEqual(identity["jobs_truncated"], True)
        self.assertEqual(evidence["status"], "INCOMPLETE")
        self.assertEqual(code, 1)
        self.assertIn("jobs-truncated", evidence["marker"]["reason"])
        self.assertIn("truncated-jobs-page",
                      evidence["prerequisites"]["roster_delta"])

    def test_f8_later_pages_are_fetched_and_inspected(self):
        """A 200-job run: the roster is on page 1, the drift on page 2."""
        page_one = green_jobs() + filler_jobs("filler", 6, 99)
        page_two = ([job(20, "extra-job", "success", 0, 3)]
                    + filler_jobs("filler-b", 0, 98))
        path = _write_fixture(paginated_fixture([page_one, page_two],
                                                total_count=200))
        code, text, _ = invoke(fixture_path=path,
                               argv=("--candidate", HEAD, "--format", "json"))
        evidence = json.loads(text)
        self.assertEqual(evidence["run_identity"]["jobs_total_count"], 200)
        self.assertEqual(evidence["run_identity"]["jobs_reported_total"], 200)
        self.assertEqual(evidence["run_identity"]["jobs_truncated"], False)
        self.assertIn("extra-job", evidence["prerequisites"]["roster_delta"])
        self.assertEqual(code, 1)
        self.assertTrue(any("page=2" in call["url"]
                            for call in evidence["run_identity"]["api_urls"]))

    def test_f8_page_limit_truncation_is_never_green(self):
        """4000 advertised jobs: the MAX_JOB_PAGES cap must be visible."""
        pages = [green_jobs() + filler_jobs("page1", 6, 99)]
        for number in range(2, 12):
            pages.append(filler_jobs("page%d" % number, 0, 99))
        path = _write_fixture(paginated_fixture(pages, total_count=4000))
        code, text, _ = invoke(fixture_path=path,
                               argv=("--candidate", HEAD, "--format", "json"))
        evidence = json.loads(text)
        self.assertEqual(evidence["run_identity"]["jobs_total_count"], 4000)
        self.assertEqual(evidence["run_identity"]["jobs_reported_total"],
                         ci_durations.MAX_JOB_PAGES * 100)
        self.assertEqual(evidence["run_identity"]["jobs_truncated"], True)
        self.assertEqual(evidence["status"], "INCOMPLETE")
        self.assertEqual(code, 1)
        self.assertIn("jobs-truncated", evidence["marker"]["reason"])
        self.assertIn("truncated-jobs-page",
                      evidence["prerequisites"]["roster_delta"])

    def test_f8_complete_pages_without_truncation_stay_complete(self):
        _, evidence = evidence_of()
        self.assertEqual(evidence["run_identity"]["jobs_truncated"], False)
        self.assertEqual(evidence["run_identity"]["jobs_total_count"], 6)

    def test_f9_matching_attempt_is_accepted_and_recorded(self):
        code, text, _ = invoke(argv=("--candidate", HEAD, "--attempt", "1",
                                     "--format", "json"))
        evidence = json.loads(text)
        self.assertEqual(code, 0)
        self.assertEqual(evidence["run_identity"]["attempt_requested"], 1)
        self.assertEqual(evidence["run_identity"]["run_attempt"], 1)

    def test_f9_mismatched_attempt_refuses_loudly(self):
        code, text, err = invoke(argv=("--candidate", HEAD, "--attempt", "999"))
        self.assertEqual(code, 2)
        self.assertEqual(text, "")
        self.assertIn("--attempt 999", err)
        self.assertIn("run_attempt=1", err)

    def test_f9_unrecorded_attempt_refuses_loudly(self):
        run = run_payload()
        del run["run_attempt"]
        code, _, err = invoke(run=run,
                              argv=("--candidate", HEAD, "--attempt", "1"))
        self.assertEqual(code, 2)
        self.assertIn("records no run_attempt", err)

    def test_f9_absent_attempt_flag_is_not_selected(self):
        _, evidence = evidence_of()
        self.assertEqual(evidence["run_identity"]["attempt_requested"],
                         "not_selected")

    def test_f7_hostile_url_components_refuse_instead_of_crashing(self):
        """Codex P1: validate components before building the URL (exit 2)."""
        for argv, needle in (
                (("--repository", "x@evil.example"), "--repository"),
                (("--repository", "a/../../b"), "--repository"),
                (("--repository", "a/b/c"), "--repository"),
                (("--workflow", "bad\nname.yml"), "--workflow"),
                (("--run-id", "1/../2"), "--run-id")):
            with self.subTest(argv=argv):
                code, text, err = invoke(argv=argv)
                self.assertEqual(code, 2)
                self.assertEqual(text, "")
                self.assertIn(needle, err)
                self.assertNotIn("Traceback", err)

    def test_f7_safe_components_still_pass_validation(self):
        """The real owner/name and workflow file are accepted (no false stop)."""
        code, _, err = invoke(argv=("--repository",
                                     "ModernNomad-98/Project-Aegis",
                                     "--workflow", "validate-skills.yml",
                                     "--candidate", HEAD))
        self.assertEqual(code, 0, err)
        self.assertEqual(err, "")

    def test_ac2_exit_codes_column_and_provenance_are_in_the_table(self):
        code, text, _ = invoke(
            argv=("--candidate", HEAD, "--format", "table"))
        self.assertEqual(code, 0)
        self.assertIn("| exit_codes |", text)
        self.assertIn("| exit_code_provenance |", text)
        self.assertIn("- step_state: Verify DCO sign-off on every commit", text)


class UnexpectedSkipEnforcementTests(unittest.TestCase):
    """N1: a roster job may skip only where the workflow lets it.

    `.github/workflows/validate-skills.yml`: `changes` (L57) and
    `validate-skills` (L106) have no `if:`; `windows-offline-checks` (L289),
    `tools-tests-linux` (L380) and `tools-tests-windows` (L430) are
    `if: github.event_name == 'push' || <flag>`, and on a push the `changes`
    job forces both flags true (L86-89); `gate-guard` (L493) is
    pull_request-only. So on a push only `gate-guard` may skip and on a
    pull_request only the three advisory jobs may; any other skip is
    INCOMPLETE/exit 1 with the job named, never COMPLETE/exit 0.
    """

    def _skip(self, name, event):
        jobs = green_jobs(event) if event == "push" else pr_jobs()
        index = [entry["name"] for entry in jobs].index(name)
        jobs[index] = job(index + 1, name, "skipped", None, None,
                          step_list=steps(event))
        return jobs

    def _evidence(self, jobs, event):
        return evidence_of(jobs=jobs, run=run_payload(event=event))

    def test_n1_push_validate_skills_skip_is_incomplete(self):
        jobs = self._skip("validate-skills", "push")
        code, evidence = self._evidence(jobs, "push")
        self.assertEqual(evidence["status"], "INCOMPLETE")
        self.assertEqual(code, 1)
        self.assertEqual(evidence["marker"]["unexpected_skipped_jobs"],
                         ["validate-skills"])
        self.assertIn("unexpected-skip-for-event:validate-skills",
                      evidence["marker"]["reason"])
        row = rows_of(evidence)["validate-skills"]
        self.assertEqual(row["state"], "skipped")
        self.assertIn("not filter-skippable on event=push",
                      row["skip_reason"])
        self.assertNotIn("event-filter", row["skip_reason"])

    def test_n1_pull_request_validate_skills_skip_is_incomplete(self):
        jobs = self._skip("validate-skills", "pull_request")
        code, evidence = self._evidence(jobs, "pull_request")
        self.assertEqual(evidence["status"], "INCOMPLETE")
        self.assertEqual(code, 1)
        self.assertEqual(evidence["marker"]["unexpected_skipped_jobs"],
                         ["validate-skills"])
        self.assertIn("unexpected-skip-for-event:validate-skills",
                      evidence["marker"]["reason"])

    def test_n1_push_tools_tests_linux_skip_is_incomplete(self):
        jobs = self._skip("tools-tests-linux", "push")
        code, evidence = self._evidence(jobs, "push")
        self.assertEqual(evidence["status"], "INCOMPLETE")
        self.assertEqual(code, 1)
        self.assertEqual(evidence["marker"]["unexpected_skipped_jobs"],
                         ["tools-tests-linux"])
        self.assertNotIn("event-filter",
                         rows_of(evidence)["tools-tests-linux"]["skip_reason"])

    def test_n1_push_windows_offline_checks_skip_is_incomplete(self):
        jobs = self._skip("windows-offline-checks", "push")
        code, evidence = self._evidence(jobs, "push")
        self.assertEqual(evidence["status"], "INCOMPLETE")
        self.assertEqual(code, 1)
        self.assertEqual(evidence["marker"]["unexpected_skipped_jobs"],
                         ["windows-offline-checks"])
        self.assertNotIn(
            "event-filter",
            rows_of(evidence)["windows-offline-checks"]["skip_reason"])

    def test_n1_push_gate_guard_skip_is_the_lawful_event_filter(self):
        code, evidence = evidence_of()
        self.assertEqual(evidence["status"], "COMPLETE")
        self.assertEqual(code, 0)
        self.assertEqual(evidence["marker"]["unexpected_skipped_jobs"], [])
        self.assertIn("pull_request-only job",
                      rows_of(evidence)["gate-guard"]["skip_reason"])

    def test_n1_pull_request_advisory_skips_stay_lawful(self):
        jobs = pr_jobs()
        for name in ("windows-offline-checks", "tools-tests-linux",
                     "tools-tests-windows"):
            index = [entry["name"] for entry in jobs].index(name)
            jobs[index] = job(index + 1, name, "skipped", None, None,
                              step_list=steps("pull_request"))
        code, evidence = self._evidence(jobs, "pull_request")
        self.assertEqual(evidence["status"], "COMPLETE")
        self.assertEqual(code, 0)
        self.assertEqual(evidence["marker"]["unexpected_skipped_jobs"], [])
        for name in ("windows-offline-checks", "tools-tests-linux",
                     "tools-tests-windows"):
            self.assertIn("event-filter",
                          rows_of(evidence)[name]["skip_reason"])

    def test_n1_dependency_failed_skip_is_not_called_unexpected(self):
        jobs = green_jobs()
        jobs[0] = job(1, "changes", "failure", 0, 5)
        code, evidence = evidence_of(jobs=jobs)
        self.assertEqual(evidence["status"], "FAILED")
        self.assertEqual(code, 4)
        self.assertEqual(evidence["marker"]["unexpected_skipped_jobs"], [])
        self.assertIn("dependency-failed",
                      rows_of(evidence)["gate-guard"]["skip_reason"])

    def test_n1_expected_skip_sets_are_exact(self):
        """The enforced set is the workflow's truth, not a convenience."""
        self.assertEqual(ci_durations.EXPECTED_SKIPS_BY_EVENT, {
            "push": ("gate-guard",),
            "pull_request": ("windows-offline-checks", "tools-tests-linux",
                             "tools-tests-windows")})
        self.assertEqual(ci_durations.REQUIRED_JOBS_BY_EVENT,
                         {"pull_request": ("gate-guard",)})

    def test_n1_table_names_the_unexpected_skip(self):
        code, text, _ = invoke(
            jobs=self._skip("tools-tests-windows", "push"),
            argv=("--candidate", HEAD, "--format", "table"))
        self.assertEqual(code, 1)
        self.assertIn("unexpected-skip: tools-tests-windows", text)
        self.assertIn("unexpected-skip-for-event:tools-tests-windows", text)
        self.assertEqual(text.count("STATUS: "), 1)


class CliContractTests(unittest.TestCase):
    """AC10, AC11: the package surface, capabilities identity, no auto-run."""

    def test_ac10_capabilities_and_status_keys_are_unchanged(self):
        for command, expected in (("capabilities",
                                   ("external_io", "real_adapters")),
                                  ("status", ("initialized", "verified"))):
            out = io.StringIO()
            with mock.patch("sys.stdout", out):
                code = main(["--repository-id", "r", command])
            self.assertEqual(code, 0)
            for key in expected:
                self.assertIn(key, json.loads(out.getvalue()))

    def test_ac10_parser_registers_ci_durations_without_a_host_flag(self):
        from tools.aegis_delivery_control.cli import build_parser
        parser = build_parser()
        namespace = parser.parse_args(
            ["--repository-id", "r", "ci-durations", "--run-id", "1"])
        self.assertEqual(namespace.command, "ci-durations")
        self.assertFalse(hasattr(namespace, "api_base"))

    def test_ac11_module_reaches_no_writing_or_process_primitive(self):
        source = Path(ci_durations.__file__).read_text(encoding="utf-8")
        for forbidden in ("subprocess", "os.system", "shutil", "\"w\")",
                          "\"a\")", "method=\"POST", "'POST'"):
            self.assertNotIn(forbidden, source)
        self.assertIn("method=\"GET\"", source)

    def test_ac11_readme_documents_the_module_and_amended_boundary(self):
        readme = (Path(ci_durations.__file__).parent / "README.md").read_text(
            encoding="utf-8")
        self.assertIn("ci_durations.py", readme)
        self.assertIn("ci-durations", readme)
        self.assertIn("--allow-network", readme)
        self.assertIn("exit 0", readme)
        self.assertIn("UNBOUND", readme)
        self.assertIn("api.github.com", readme)
        self.assertIn("opt-in, read-only command", readme)
        self.assertIn("reads public GitHub run metadata", readme)
        boundary = " ".join(readme.split())
        self.assertIn(
            "exactly one opt-in, read-only command, "
            + chr(96) + "ci-durations" + chr(96), boundary)
        self.assertIn(
            "reads public GitHub run metadata and never writes or dispatches "
            "anything", boundary)


def tearDownModule():
    for name in _TEMP:
        try:
            Path(name).unlink()
        except OSError:
            pass


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
