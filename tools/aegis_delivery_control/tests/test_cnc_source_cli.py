"""Source wrapper checks; these tests are not copied to consumers."""
from contextlib import redirect_stderr, redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from tools.aegis_delivery_control import cli, cnc_reporting


class _BinaryCapture:
    """Expose only the bytes buffer the JSON emitter writes to."""

    def __init__(self):
        self.buffer = io.BytesIO()


class SourceCliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="cnc-source-")
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "capture.json"
        self.data = json.loads((Path(__file__).parent / "fixtures" / "cnc-report-cases.json").read_text("utf-8"))["input"]
        self.path.write_text(json.dumps(self.data), encoding="utf-8")

    def run_cli(self, repository="ModernNomad-98/Project-Aegis", extra=()):
        return subprocess.run([sys.executable,"-B","-m","tools.aegis_delivery_control",
            "--repository-id",repository,"cnc-report","--input",str(self.path),*extra],capture_output=True)

    def test_native_entrypoint_consumes_fixed_profile(self):
        run=self.run_cli()
        self.assertEqual(run.returncode,0,run.stderr)
        report=json.loads(run.stdout)
        self.assertEqual(report["items"][0]["native_routes"]["authority"]["route"],"LOCATE_ORIGINAL_AUTHORITY")
        self.assertEqual(report["native_record"],self.data["native_record"])
        self.assertEqual(report["report_status"],"RENDERED_NON_AUTHORIZING")
        self.assertEqual(run.stderr,b"")
        self.assertNotIn(b"\r",run.stdout)
        self.assertEqual(run.stdout.count(b"\n"),1)

    def test_retained_record_native_replay_binds_input_without_writes(self):
        cases=json.loads((Path(__file__).parent / "fixtures" / "cnc-report-cases.json").read_text("utf-8"))
        self.path.write_text(json.dumps(cases["retained_replay"]),encoding="utf-8")
        before=self.path.read_bytes()
        run=self.run_cli()
        self.assertEqual(run.returncode,0,run.stderr)
        report=json.loads(run.stdout)
        import hashlib
        self.assertEqual(report["input_sha256"],hashlib.sha256(before).hexdigest())
        self.assertEqual(self.path.read_bytes(),before)
        self.assertIn("issuecomment-6614470166",report["native_record"]["locator"])
        self.assertEqual([item["task"] for item in report["items"]],["proof2-retained"])
        self.assertNotIn("source-995-record",[item["task"] for item in report["items"]])
        self.assertEqual(report["items"][0]["next_action"],
            "Use existing retention/deletion reminder; no new run or cleanup")
        self.assertIsNone(report["items"][0]["coordinator_answer"]["value"])

    def test_foreign_and_override_refused_without_echo(self):
        for extra in (("--profile","DO_NOT_LEAK"),("--contract","DO_NOT_LEAK"),("--unknown","DO_NOT_LEAK")):
            run=self.run_cli(extra=extra)
            self.assertEqual(run.returncode,2)
            self.assertEqual(run.stdout,b"")
            self.assertEqual(json.loads(run.stderr)["error_code"],"CLI_INVALID")
            self.assertNotIn(b"DO_NOT_LEAK",run.stderr)
        run=self.run_cli(repository="foreign/repository")
        self.assertEqual(json.loads(run.stderr)["error_code"],"IDENTITY_MISMATCH")
        self.assertEqual(run.stdout,b"")

    def test_report_mode_tracks_shared_top_level_option_metadata(self):
        # The detector and build_parser must agree on the top-level surface.
        expected = {spec["name"] for spec in cli._TOP_LEVEL_OPTIONS}
        parser = cli.build_parser(report_mode=True)
        self.assertEqual(
            set(parser._option_string_actions) - {"-h", "--help"}, expected)
        extra = {"name": "--ledger", "required": True, "takes_value": True}
        flag = {"name": "--verbose", "required": False, "takes_value": False}
        with patch.object(cli, "_TOP_LEVEL_OPTIONS",
                          cli._TOP_LEVEL_OPTIONS + (extra, flag)):
            parser = cli.build_parser(report_mode=True)
            self.assertIn("--ledger", parser._option_string_actions)
            self.assertIn("--verbose", parser._option_string_actions)
            self.assertTrue(cli._report_mode([
                "--repository-id", "example", "--ledger", "book",
                "cnc-report", "--input", "capture.json"]))
            self.assertTrue(cli._report_mode([
                "--repository-id=example", "--ledger=book", "cnc-report",
                "--input", "capture.json"]))
            self.assertTrue(cli._report_mode([
                "--verbose", "--repository-id", "example", "cnc-report",
                "--input", "capture.json"]))
            self.assertFalse(cli._report_mode([
                "--repository-id", "example", "--ledger", "book", "status"]))

    def test_report_mode_uses_the_selected_subcommand(self):
        self.assertFalse(cli._report_mode(["--repository-id","example","status"]))
        self.assertFalse(cli._report_mode(["--repository-id","example","fast-save",
            "--state","cnc-report","--checkpoint","out.json"]))
        self.assertTrue(cli._report_mode(["--repository-id","example","cnc-report",
            "--input","capture.json"]))
        self.assertTrue(cli._report_mode(["--repository-id=example","cnc-report",
            "--input","capture.json"]))
        # An abbreviated top-level option is recognized for report-mode
        # detection, but the strict parser still refuses the abbreviation.
        self.assertTrue(cli._report_mode(["--repo","example","cnc-report",
            "--input","capture.json"]))
        self.assertTrue(cli._report_mode(["--re=example","cnc-report",
            "--input","capture.json"]))
        self.assertFalse(cli._report_mode(["--repo","example","status"]))
        # A value that spells cnc-report must not switch the parser class: an
        # ordinary unknown option stays an ordinary argparse error.
        run=subprocess.run([sys.executable,"-B","-m","tools.aegis_delivery_control",
            "--repository-id","example","fast-save","--state","cnc-report",
            "--checkpoint",str(self.path),"--bogus"],capture_output=True)
        self.assertEqual(run.returncode,2)
        self.assertEqual(run.stdout,b"")
        self.assertIn(b"usage:",run.stderr)
        self.assertNotIn(b"error_code",run.stderr)
        # The abbreviated top-level option cannot bypass report parsing: it is
        # refused as an abbreviation, but through the fixed JSON error path.
        run=subprocess.run([sys.executable,"-B","-m","tools.aegis_delivery_control",
            "--repo","ModernNomad-98/Project-Aegis","cnc-report","--input",
            str(self.path)],capture_output=True)
        self.assertEqual(run.returncode,2)
        self.assertEqual(run.stdout,b"")
        self.assertEqual(json.loads(run.stderr)["error_code"],"CLI_INVALID")
        # An abbreviated cnc-report option is refused for the same reason.
        run=subprocess.run([sys.executable,"-B","-m","tools.aegis_delivery_control",
            "--repository-id","ModernNomad-98/Project-Aegis","cnc-report","--inp",
            str(self.path)],capture_output=True)
        self.assertEqual(run.returncode,2)
        self.assertEqual(run.stdout,b"")
        self.assertEqual(json.loads(run.stderr)["error_code"],"CLI_INVALID")
        # Abbreviations are refused consistently on the ordinary surface too.
        run=subprocess.run([sys.executable,"-B","-m","tools.aegis_delivery_control",
            "--repo","example","status"],capture_output=True)
        self.assertEqual(run.returncode,2)
        self.assertEqual(run.stdout,b"")
        self.assertIn(b"usage:",run.stderr)
        self.assertNotIn(b"error_code",run.stderr)

    def test_report_mode_scans_past_unknown_tokens(self):
        # Unknown options and values before the subcommand do not end the scan:
        # the first KNOWN subcommand still decides, so a malformed cnc-report
        # invocation reaches the fixed JSON path instead of ordinary argparse.
        vectors=(
            ["--repository-id","example","--bogus=DO_NOT_LEAK","cnc-report",
             "--input","capture.json"],
            ["--repository-id","example","--bogus","DO_NOT_LEAK","cnc-report",
             "--input","capture.json"],
            ["--repository-id","example","--bogus","status","cnc-report",
             "--input","capture.json"],
            ["--bogus","cnc-report","--input","capture.json"],
            ["--bogus=DO_NOT_LEAK","--","cnc-report","--input","capture.json"])
        for argv in vectors:
            with self.subTest(argv=argv):
                self.assertTrue(cli._report_mode(argv))
        # A known non-report subcommand stops the scan first, so a value that
        # happens to spell cnc-report cannot switch the parser class.
        vectors=(
            ["--repository-id","example","--bogus","status"],
            ["--repository-id","example","status","--bogus"],
            ["--repository-id","example","fast-save","--state","cnc-report",
             "--checkpoint","out.json","--bogus"],
            ["--repository-id","example","--bogus"])
        for argv in vectors:
            with self.subTest(argv=argv):
                self.assertFalse(cli._report_mode(argv))

    def test_top_level_option_prefix_must_be_unambiguous(self):
        # With two top-level options sharing a prefix, a shortening must not
        # resolve to the first one; only an exact or unique prefix matches.
        options=({"name":"--ledger","required":True,"takes_value":True},
                 {"name":"--ledger-file","required":False,"takes_value":True})
        with patch.object(cli,"_TOP_LEVEL_OPTIONS",options):
            self.assertIsNone(cli._top_level_option("--l"))
            self.assertIsNone(cli._top_level_option("--led"))
            self.assertEqual(cli._top_level_option("--ledger")["name"],
                             "--ledger")
            self.assertEqual(cli._top_level_option("--ledger-f")["name"],
                             "--ledger-file")
            self.assertIsNone(cli._top_level_option("--repository"))

    def test_unknown_option_separated_value_equal_to_subcommand(self):
        base=[sys.executable,"-B","-m","tools.aegis_delivery_control",
              "--repository-id","ModernNomad-98/Project-Aegis"]
        # The unknown option is assumed to take "status" as its value, so the
        # later cnc-report token still selects the fixed JSON error path.
        run=subprocess.run([*base,"--bogus","status","cnc-report","--input",
                            str(self.path)],capture_output=True)
        self.assertEqual(run.returncode,2)
        self.assertEqual(run.stdout,b"")
        self.assertEqual(json.loads(run.stderr),
                         {"error_code":"CLI_INVALID",
                          "message":cnc_reporting.ERRORS["CLI_INVALID"][1]})
        self.assertEqual(run.stderr.count(b"\n"),1)
        self.assertNotIn(b"\r",run.stderr)
        self.assertNotIn(b"usage:",run.stderr)
        self.assertTrue(cli._report_mode(["--repository-id","example","--bogus",
                                          "status","cnc-report","--input","x"]))
        self.assertFalse(cli._report_mode(["--repository-id","example","--bogus",
                                           "status"]))

    def test_declared_subcommands_match_build_parser_choices(self):
        parser=cli.build_parser()
        actions=[action for action in parser._subparsers._group_actions]
        self.assertEqual(len(actions),1)
        self.assertEqual(set(actions[0].choices),set(cli._SUBCOMMANDS))
        self.assertEqual(len(cli._SUBCOMMANDS),len(set(cli._SUBCOMMANDS)))
        self.assertIn("cnc-report",cli._SUBCOMMANDS)

    def test_unknown_option_before_report_subcommand_stays_fixed_json(self):
        base=[sys.executable,"-B","-m","tools.aegis_delivery_control",
              "--repository-id","ModernNomad-98/Project-Aegis"]
        # (a) An unknown option before cnc-report is not echoed by argparse; it
        # reaches the report parser's fixed JSON CLI_INVALID error path.
        for extra in (("--bogus=DO_NOT_LEAK",),("--bogus","DO_NOT_LEAK")):
            run=subprocess.run([*base,*extra,"cnc-report","--input",
                                str(self.path)],capture_output=True)
            with self.subTest(extra=extra):
                self.assertEqual(run.returncode,2)
                self.assertEqual(run.stdout,b"")
                self.assertEqual(json.loads(run.stderr)["error_code"],
                                 "CLI_INVALID")
                self.assertNotIn(b"DO_NOT_LEAK",run.stdout)
                self.assertNotIn(b"DO_NOT_LEAK",run.stderr)
                self.assertNotIn(b"usage:",run.stderr)
        # (b) The abbreviated top-level option keeps the same fixed JSON path.
        run=subprocess.run([sys.executable,"-B","-m",
            "tools.aegis_delivery_control","--repo","ModernNomad-98/Project-Aegis",
            "cnc-report","--input",str(self.path)],capture_output=True)
        self.assertEqual(run.returncode,2)
        self.assertEqual(run.stdout,b"")
        self.assertEqual(json.loads(run.stderr)["error_code"],"CLI_INVALID")
        self.assertNotIn(b"usage:",run.stderr)
        # (c) An unknown option on a non-report command stays an ordinary usage
        # error; the fixed JSON error object is never emitted.
        for extra in (("status","--bogus"),("--bogus","status")):
            run=subprocess.run([*base,*extra],capture_output=True)
            with self.subTest(extra=extra):
                self.assertEqual(run.returncode,2)
                self.assertEqual(run.stdout,b"")
                self.assertIn(b"usage:",run.stderr)
                self.assertNotIn(b"error_code",run.stderr)

    def test_report_branches_before_database_and_preserves_capabilities(self):
        stdout,stderr=_BinaryCapture(),_BinaryCapture()
        with patch.object(cli,"_database_path",side_effect=AssertionError("database path")), \
             patch.object(cli.sqlite3,"connect",side_effect=AssertionError("database")), \
             redirect_stdout(stdout),redirect_stderr(stderr):
            status=cli.main(["--repository-id","ModernNomad-98/Project-Aegis","cnc-report","--input",str(self.path)])
        self.assertEqual(status,0,stderr.buffer.getvalue())
        payload=stdout.buffer.getvalue()
        self.assertNotIn(b"\r",payload)
        self.assertEqual(payload.count(b"\n"),1)
        self.assertEqual(json.loads(payload)["report_status"],"RENDERED_NON_AUTHORIZING")
        run=subprocess.run([sys.executable,"-B","-m","tools.aegis_delivery_control","--repository-id",
            "ModernNomad-98/Project-Aegis","capabilities"],capture_output=True)
        self.assertEqual(run.returncode,0)
        self.assertFalse(json.loads(run.stdout)["real_adapters"])

    def test_fixed_source_adapter_hash_matches_shipped_bytes(self):
        source=Path(cli.__file__).resolve().parent/"cnc"/"adapter-aegis.json"
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),
                         cli.ADAPTER_SHA256)

    def test_source_adapter_mutations_rejected_before_projection(self):
        cases=json.loads((Path(__file__).parent / "fixtures" /
            "cnc-report-cases.json").read_text("utf-8"))
        support=Path(self.tmp.name)/"support"
        (support/"cnc").mkdir(parents=True)
        source=Path(cli.__file__).resolve().parent/"cnc"
        (support/"cnc"/"cnc-evidence-contract-v2.json").write_bytes(
            (source/"cnc-evidence-contract-v2.json").read_bytes())
        mutations={
            "repository": lambda p:p.update(repository="evil/repository"),
            "id": lambda p:p.update(id="aegis-other"),
            "stage_label": lambda p:p["stage_labels"][0].update(label="planning"),
            "activation": lambda p:p.update(activation="adopted_with_receipt",
                adoption_receipt={"value":"record:adoption","unknown_reason":None}),
            "fabricated_receipt": lambda p:p.update(
                activation="adopted_with_receipt",
                adoption_receipt={"value":"fabricated receipt","unknown_reason":None}),
            "policy_locator": lambda p:p.update(
                authority_policy_locator="docs/other-policy.md"),
        }
        for name,mutate in mutations.items():
            profile=json.loads(json.dumps(cases["profile"]))
            mutate(profile)
            (support/"cnc"/"adapter-aegis.json").write_text(
                json.dumps(profile),encoding="utf-8")
            repository=("evil/repository" if name=="repository"
                        else "ModernNomad-98/Project-Aegis")
            data=json.loads(json.dumps(cases["input"]))
            data["repository_id"]=repository
            self.path.write_text(json.dumps(data),encoding="utf-8")
            stdout,stderr=_BinaryCapture(),_BinaryCapture()
            with patch.object(cli,"__file__",str(support/"cli.py")), \
                 patch.object(cnc_reporting,"_routes",
                              side_effect=AssertionError("projection reached")), \
                 redirect_stdout(stdout),redirect_stderr(stderr):
                status=cli.main(["--repository-id",repository,"cnc-report",
                                 "--input",str(self.path)])
            with self.subTest(mutation=name):
                self.assertEqual(status,2,stderr.buffer.getvalue())
                self.assertEqual(stdout.buffer.getvalue(),b"")
                self.assertEqual(json.loads(stderr.buffer.getvalue())["error_code"],
                                 "PROFILE_INVALID")


if __name__ == "__main__":
    unittest.main()
