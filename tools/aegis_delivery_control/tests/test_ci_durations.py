"""Offline tests for the read-only CI-run duration reader (P0-A A2).

Every fixture here is a replay of the payload shapes the plan records as
independently re-derived: run 38198781208 (push, head 4d5ccb0b..., attempt 1)
carries the AC1 durations 7/109/skipped/224/132/229 s, and the second fixture
mirrors the A1 page cross-check pair 8/111/skipped/241/100/165 s. No test
performs network I/O: the zero-socket proof patches socket.socket,
urllib.request.urlopen and ci_durations.HttpTransport together, and the
fixture path is additionally asserted never to construct a transport.
"""

from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path
import socket
import sys
import tempfile
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


def _iso(second):
    return "2026-10-12T03:%02d:%02dZ" % (second // 60, second % 60)


def job(index, name, conclusion, start=None, end=None, html=None):
    entry = {"id": 100 + index, "name": name, "status": "completed",
             "conclusion": conclusion, "artifacts": [],
             "html_url": html or ("%s%s/job/%d" % (API, RUN_ID, 100 + index))}
    entry["started_at"] = _iso(start) if start is not None else None
    entry["completed_at"] = _iso(end) if end is not None else None
    return entry


def run_payload(head=HEAD, conclusion="success", status="completed",
                attempt=1, event="push", run_id=RUN_ID):
    return {"id": run_id, "name": "validate-skills",
            "workflow_id": 269900000, "run_attempt": attempt, "event": event,
            "status": status, "conclusion": conclusion, "head_sha": head,
            "created_at": "2026-10-12T03:11:20Z",
            "updated_at": "2026-10-12T03:15:40Z"}


def green_jobs():
    return [job(1, "changes", "success", 0, 7),
            job(2, "validate-skills", "success", 0, 109),
            job(3, "gate-guard", "skipped", 71, 70),
            job(4, "windows-offline-checks", "success", 30, 254),
            job(5, "tools-tests-linux", "success", 40, 172),
            job(6, "tools-tests-windows", "success", 50, 279)]


def a1_jobs():
    return [job(1, "changes", "success", 0, 8),
            job(2, "validate-skills", "success", 0, 111),
            job(3, "gate-guard", "skipped", None, None),
            job(4, "windows-offline-checks", "success", 30, 271),
            job(5, "tools-tests-linux", "success", 40, 140),
            job(6, "tools-tests-windows", "success", 50, 215)]


def fixture(jobs=None, run=None, run_id=RUN_ID, with_runs_list=False,
            head=HEAD):
    run = run if run is not None else run_payload(head=head, run_id=run_id)
    jobs = green_jobs() if jobs is None else jobs
    base = "%s%s" % (API, run_id)
    mapping = {base: run,
               "%s/jobs?per_page=100" % base:
                   {"total_count": len(jobs), "jobs": jobs}}
    if with_runs_list:
        mapping[("https://api.github.com/repos/ModernNomad-98/Project-Aegis"
                 "/actions/workflows/validate-skills.yml/runs?head_sha=%s"
                 "&per_page=100" % head)] = {"total_count": 1,
                                             "workflow_runs": [run]}
    return mapping


ENTRY = object()


def invoke(jobs=None, run=None, run_id=RUN_ID, argv=(), fixture_path=ENTRY,
           with_runs_list=False, head=HEAD, artifact_dir=None, **kwargs):
    """Run the command in-process against a fixture; returns (code, stdout)."""
    if fixture_path is ENTRY:
        fixture_path = _write_fixture(
            fixture(jobs=jobs, run=run, run_id=run_id,
                    with_runs_list=with_runs_list, head=head))
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
            self.assertIn("artifact:", rows[name]["exit_code_provenance"])
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

    def test_ac7_json_carries_no_raw_control_character(self):
        hostile = "line1" + chr(10) + "line2" + chr(27) + "|end"
        jobs = green_jobs()
        jobs[5] = job(6, "tools-tests-windows", "success", 50, 279,
                      html=hostile)
        _, evidence = evidence_of(jobs=jobs)
        row = rows_of(evidence)["tools-tests-windows"]
        for control in (chr(10), chr(13), chr(27)):
            self.assertNotIn(control, row["log_url"])
        self.assertIn(chr(92) + "x0a", row["log_url"])
        self.assertIn(chr(92) + "x1b", row["log_url"])
        self.assertIn(chr(92) + "|", row["log_url"])

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
