"""Source wrapper checks; these tests are not copied to consumers."""
from contextlib import redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from tools.aegis_delivery_control import cli


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

    def test_report_mode_uses_the_selected_subcommand(self):
        self.assertFalse(cli._report_mode(["--repository-id","example","status"]))
        self.assertFalse(cli._report_mode(["--repository-id","example","fast-save",
            "--state","cnc-report","--checkpoint","out.json"]))
        self.assertTrue(cli._report_mode(["--repository-id","example","cnc-report",
            "--input","capture.json"]))
        self.assertTrue(cli._report_mode(["--repository-id=example","cnc-report",
            "--input","capture.json"]))
        # A value that spells cnc-report must not switch the parser class: an
        # ordinary unknown option stays an ordinary argparse error.
        run=subprocess.run([sys.executable,"-B","-m","tools.aegis_delivery_control",
            "--repository-id","example","fast-save","--state","cnc-report",
            "--checkpoint",str(self.path),"--bogus"],capture_output=True)
        self.assertEqual(run.returncode,2)
        self.assertEqual(run.stdout,b"")
        self.assertIn(b"usage:",run.stderr)
        self.assertNotIn(b"error_code",run.stderr)

    def test_report_branches_before_database_and_preserves_capabilities(self):
        stdout,stderr=io.StringIO(),io.StringIO()
        with patch.object(cli,"_database_path",side_effect=AssertionError("database path")), \
             patch.object(cli.sqlite3,"connect",side_effect=AssertionError("database")), \
             redirect_stdout(stdout),redirect_stderr(stderr):
            status=cli.main(["--repository-id","ModernNomad-98/Project-Aegis","cnc-report","--input",str(self.path)])
        self.assertEqual(status,0,stderr.getvalue())
        self.assertEqual(json.loads(stdout.getvalue())["report_status"],"RENDERED_NON_AUTHORIZING")
        run=subprocess.run([sys.executable,"-B","-m","tools.aegis_delivery_control","--repository-id",
            "ModernNomad-98/Project-Aegis","capabilities"],capture_output=True)
        self.assertEqual(run.returncode,0)
        self.assertFalse(json.loads(run.stdout)["real_adapters"])


if __name__ == "__main__":
    unittest.main()
