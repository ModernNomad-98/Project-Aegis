#!/usr/bin/env python3
"""Self-tests for scripts/verify_consumer_live.py.

Every case runs the script as a subprocess over a local HTTP server, so the
assertions cover the real exit status and the real report rather than an
imported function: a check that cannot fail is not a check. No test touches the
public network -- the server binds 127.0.0.1 on an ephemeral port and serves a
temporary directory.

The test matrix is the failure taxonomy the script claims to distinguish, one
case per class: match, changed byte with the byte count held constant, changed
byte count, changed LF count, a tampered manifest SHA-256, a missing served
file, an extra manifest row, a missing manifest row, both aggregate fields, an
unreachable base URL, and the manifest-shape refusals. Two further cases prove
properties rather than verdicts: a run writes nothing, and two runs print the
same bytes.
"""
from __future__ import annotations

import functools
import hashlib
import http.server
import importlib.util
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import threading
import unittest

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts/verify_consumer_live.py"

OK, FINDING, MANIFEST, TRANSPORT = 0, 1, 2, 3
ZERO_SHA = "0" * 64


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def row_of(name: str, data: bytes) -> tuple[str, int, int, str]:
    return (name, len(data), data.count(b"\n"), sha256(data))


def ordered(rows):
    return sorted(rows, key=lambda row: row[0].encode("utf-8"))


def serialize(rows) -> bytes:
    return "".join("%s\t%d\t%d\t%s\n" % row for row in ordered(rows)).encode("utf-8")


def manifest_text(rows, *, aggregate=None, serialized_bytes=None,
                  declared_rows=None) -> str:
    """A manifest in the documented shape, with optional deliberate damage."""
    serialized = serialize(rows)
    aggregate = sha256(serialized) if aggregate is None else aggregate
    serialized_bytes = (len(serialized) if serialized_bytes is None
                        else serialized_bytes)
    declared_rows = len(rows) if declared_rows is None else declared_rows
    body = "".join("%s\t%d\t%d\t%s\n" % row for row in ordered(rows))
    return body + ("# aggregate rows=%d serialized_bytes=%d sha256=%s\n"
                   % (declared_rows, serialized_bytes, aggregate))


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    """A static file handler that keeps the test output clean."""

    def log_message(self, *args):  # noqa: D102 - silence access logging
        pass


class Site:
    """A local static server for one site directory, on an ephemeral port."""

    def __init__(self, directory: Path) -> None:
        handler = functools.partial(QuietHandler, directory=str(directory))
        self.httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()

    @property
    def base_url(self) -> str:
        host, port = self.httpd.server_address[:2]
        return "http://%s:%d/" % (host, port)

    def close(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(5)


def load_module():
    spec = importlib.util.spec_from_file_location("verify_consumer_live", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class LiveVerifyCase(unittest.TestCase):
    """Shared fixture: a three-file site, its matching manifest, and a server."""

    FILES = {
        "app.js": b"console.log('boot');\nrun();\n",
        "index.html": b"<!doctype html>\n<title>proof</title>\n",
        "styles.css": b"body{color:#111}\n",
    }

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.site = self.root / "site"
        self.site.mkdir()
        for name, data in self.FILES.items():
            (self.site / name).write_bytes(data)
        self.manifest = self.root / "manifest.txt"
        self.write_manifest([row_of(name, data) for name, data in self.FILES.items()])
        self.server = Site(self.site)
        self.addCleanup(self.server.close)

    def write_manifest(self, rows, **overrides) -> None:
        text = manifest_text(rows, **overrides)
        self.manifest.write_bytes(text.encode("utf-8"))

    def rows(self):
        return [row_of(name, data) for name, data in self.FILES.items()]

    def run_verify(self, *extra: str, cache_bust: bool = False):
        command = [sys.executable, "-B", str(SCRIPT),
                   "--base-url", self.server.base_url,
                   "--manifest", str(self.manifest),
                   "--timeout", "10", *extra]
        if not cache_bust:
            command.append("--no-cache-bust")
        return subprocess.run(command, cwd=str(REPO), capture_output=True, text=True)

    def assertReason(self, result, text: str) -> None:
        self.assertIn(text, result.stdout + result.stderr)


class MatchTests(LiveVerifyCase):
    def test_match_reports_ok_and_the_aggregate(self):
        result = self.run_verify()
        self.assertEqual(OK, result.returncode, result.stdout + result.stderr)
        expected_aggregate = sha256(serialize(self.rows()))
        self.assertReason(result, "OK: ")
        self.assertReason(result, "files=3 serialized_bytes=")
        self.assertReason(result, "aggregate=" + expected_aggregate)
        self.assertNotIn("FAIL", result.stdout)
        self.assertNotIn("MISMATCH", result.stdout)

    def test_cache_bust_query_is_on_by_default(self):
        (self.site / "styles.css").unlink()
        result = self.run_verify(cache_bust=True)
        self.assertEqual(FINDING, result.returncode, result.stdout + result.stderr)
        self.assertReason(result, "?v=live-verify")

    def test_require_flag_narrows_the_required_set(self):
        result = self.run_verify("--require", "app.js")
        self.assertEqual(FINDING, result.returncode, result.stdout + result.stderr)
        self.assertEqual(2, result.stdout.count("FAIL row-extra:"), result.stdout)
        self.assertReason(result, "'index.html'")
        self.assertReason(result, "'styles.css'")


class ContentMismatchTests(LiveVerifyCase):
    def test_changed_byte_same_length_reports_only_the_sha(self):
        target = self.site / "app.js"
        original = target.read_bytes()
        target.write_bytes(original.replace(b"boot", b"boor"))
        result = self.run_verify()
        self.assertEqual(FINDING, result.returncode, result.stdout + result.stderr)
        self.assertReason(result, "FAIL file-sha: app.js")
        self.assertNotIn("FAIL file-bytes:", result.stdout)
        self.assertNotIn("FAIL file-lf:", result.stdout)

    def test_changed_byte_count_reports_bytes_and_sha(self):
        target = self.site / "app.js"
        served_bytes = len(target.read_bytes()) + 1
        target.write_bytes(target.read_bytes() + b"x")
        result = self.run_verify()
        self.assertEqual(FINDING, result.returncode, result.stdout + result.stderr)
        self.assertReason(result, "FAIL file-bytes: app.js served "
                         + str(served_bytes) + " B")
        self.assertReason(result, "FAIL file-sha: app.js")
        self.assertNotIn("FAIL file-lf:", result.stdout)

    def test_changed_lf_count_reports_the_count_and_the_delta(self):
        target = self.site / "styles.css"
        target.write_bytes(target.read_bytes() + b"\n")
        result = self.run_verify()
        self.assertEqual(FINDING, result.returncode, result.stdout + result.stderr)
        self.assertReason(result, "FAIL file-lf: styles.css served 2 LF")
        self.assertReason(result, "(+1)")
        self.assertReason(result, "FAIL file-bytes: styles.css")

    def test_tampered_manifest_sha_reports_that_row_only(self):
        rows = self.rows()
        tampered = [(name, nbytes, nlf,
                     (ZERO_SHA if name == "app.js" else sha))
                    for name, nbytes, nlf, sha in rows]
        # The aggregate comment still describes the true served rows, so the
        # aggregate must stay green: this isolates the per-file SHA check.
        self.write_manifest(tampered,
                            aggregate=sha256(serialize(rows)))
        result = self.run_verify()
        self.assertEqual(FINDING, result.returncode, result.stdout + result.stderr)
        self.assertReason(result, "FAIL file-sha: app.js")
        self.assertReason(result, ZERO_SHA)
        self.assertNotIn("FAIL file-bytes:", result.stdout)
        self.assertNotIn("FAIL aggregate-", result.stdout)

    def test_missing_served_file_reports_404(self):
        (self.site / "styles.css").unlink()
        result = self.run_verify()
        self.assertEqual(FINDING, result.returncode, result.stdout + result.stderr)
        self.assertReason(result, "FAIL served-missing: styles.css is not served (HTTP 404)")
        self.assertNotIn("FAIL aggregate-", result.stdout)


class RowSetTests(LiveVerifyCase):
    def test_extra_manifest_row_is_reported(self):
        rows = self.rows() + [row_of("legacy.js", b"old();\n")]
        (self.site / "legacy.js").write_bytes(b"old();\n")
        self.write_manifest(rows)
        result = self.run_verify()
        self.assertEqual(FINDING, result.returncode, result.stdout + result.stderr)
        self.assertReason(result, "FAIL row-extra: the manifest records a row for 'legacy.js'")
        # The four-row aggregate cannot match a three-file required set, and the
        # script says so rather than stopping at the row-set finding.
        self.assertReason(result, "FAIL aggregate-")

    def test_missing_manifest_row_is_reported(self):
        rows = [row for row in self.rows() if row[0] != "styles.css"]
        self.write_manifest(rows)
        result = self.run_verify()
        self.assertEqual(FINDING, result.returncode, result.stdout + result.stderr)
        self.assertReason(result, "FAIL row-missing: the manifest has no row for required file 'styles.css'")


class AggregateTests(LiveVerifyCase):
    def test_aggregate_sha_mismatch_is_isolated(self):
        self.write_manifest(self.rows(), aggregate=ZERO_SHA)
        result = self.run_verify()
        self.assertEqual(FINDING, result.returncode, result.stdout + result.stderr)
        self.assertReason(result, "FAIL aggregate-sha:")
        self.assertReason(result, ZERO_SHA)
        self.assertNotIn("FAIL file-", result.stdout)
        self.assertNotIn("FAIL row-", result.stdout)

    def test_aggregate_serialized_bytes_mismatch_is_reported(self):
        serialized_bytes = len(serialize(self.rows())) + 1
        self.write_manifest(self.rows(), serialized_bytes=serialized_bytes)
        result = self.run_verify()
        self.assertEqual(FINDING, result.returncode, result.stdout + result.stderr)
        self.assertReason(result, "FAIL aggregate-bytes:")
        self.assertNotIn("FAIL aggregate-sha:", result.stdout)


class ManifestShapeTests(LiveVerifyCase):
    def test_cr_byte_is_refused(self):
        self.manifest.write_bytes(
            manifest_text(self.rows()).replace("\n", "\r\n").encode("utf-8"))
        result = self.run_verify()
        self.assertEqual(MANIFEST, result.returncode, result.stdout + result.stderr)
        self.assertReason(result, "manifest-cr:")

    def test_malformed_aggregate_comment_is_refused(self):
        text = manifest_text(self.rows())
        text = re.sub(r"(?m)^# aggregate .*$", "# aggregate rows=3", text)
        self.manifest.write_bytes(text.encode("utf-8"))
        result = self.run_verify()
        self.assertEqual(MANIFEST, result.returncode, result.stdout + result.stderr)
        self.assertReason(result, "manifest-comment-format:")

    def test_row_with_the_wrong_field_count_is_refused(self):
        text = manifest_text(self.rows())
        text = re.sub(r"(?m)^app\.js\t.*$", "app.js\t31\t2", text)
        self.manifest.write_bytes(text.encode("utf-8"))
        result = self.run_verify()
        self.assertEqual(MANIFEST, result.returncode, result.stdout + result.stderr)
        self.assertReason(result, "manifest-row-fields:")

    def test_uppercase_sha_is_refused(self):
        text = manifest_text(self.rows())
        text = re.sub(r"(?m)^(app\.js\t[^\t]+\t[^\t]+\t)([0-9a-f]{64})$",
                      lambda m: m.group(1) + m.group(2).upper(), text)
        self.manifest.write_bytes(text.encode("utf-8"))
        result = self.run_verify()
        self.assertEqual(MANIFEST, result.returncode, result.stdout + result.stderr)
        self.assertReason(result, "manifest-row-sha:")

    def test_symlinked_manifest_is_refused(self):
        real = self.root / "manifest-real.txt"
        real.write_bytes(self.manifest.read_bytes())
        link = self.root / "manifest-link.txt"
        try:
            link.symlink_to(real)
        except (OSError, NotImplementedError) as exc:
            self.skipTest("this host cannot create symlinks: " + str(exc))
        self.manifest = link
        result = self.run_verify()
        self.assertEqual(MANIFEST, result.returncode, result.stdout + result.stderr)
        self.assertReason(result, "manifest-symlink:")


class TransportTests(unittest.TestCase):
    def test_unreachable_base_url_exits_3(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            site = root / "site"
            site.mkdir()
            files = {
                "app.js": b"console.log('boot');\nrun();\n",
                "index.html": b"<!doctype html>\n",
                "styles.css": b"body{color:#111}\n",
            }
            for name, data in files.items():
                (site / name).write_bytes(data)
            manifest = root / "manifest.txt"
            manifest.write_bytes(
                manifest_text([row_of(name, data) for name, data in files.items()])
                .encode("utf-8"))
            server = Site(site)
            base_url = server.base_url
            server.close()
            result = subprocess.run(
                [sys.executable, "-B", str(SCRIPT), "--base-url", base_url,
                 "--manifest", str(manifest), "--no-cache-bust", "--timeout", "5"],
                cwd=str(REPO), capture_output=True, text=True)
            self.assertEqual(TRANSPORT, result.returncode,
                             result.stdout + result.stderr)
            self.assertIn("unreachable", result.stdout)
            self.assertIn("FAIL transport: ", result.stdout)


class PropertyTests(LiveVerifyCase):
    def test_a_run_writes_nothing(self):
        def snapshot(directory: Path):
            return {path.name: (path.stat().st_size, sha256(path.read_bytes()))
                    for path in sorted(directory.iterdir()) if path.is_file()}

        before_site = snapshot(self.site)
        before_root = snapshot(self.root)
        before_manifest = sha256(self.manifest.read_bytes())
        (self.site / "styles.css").write_bytes(b"body{color:#222}\n")
        changed_site = snapshot(self.site)
        result = self.run_verify()
        self.assertEqual(FINDING, result.returncode, result.stdout + result.stderr)
        self.assertEqual(changed_site, snapshot(self.site))
        self.assertEqual(before_root, snapshot(self.root))
        self.assertEqual(before_manifest, sha256(self.manifest.read_bytes()))
        self.assertNotEqual(before_site, changed_site)

    def test_two_runs_print_identical_stdout(self):
        first = self.run_verify()
        second = self.run_verify()
        self.assertEqual(first.returncode, second.returncode)
        self.assertEqual(first.stdout, second.stdout)


class SerializationRuleTests(unittest.TestCase):
    def test_serialization_reproduces_the_retained_release_b_aggregate(self):
        """The rule the script implements must equal the producer's rule.

        These four values per row are copied from the retained Release B
        manifest in this repository, and the expected aggregate is that file's
        own aggregate comment. Reproducing it here proves the script did not
        invent a serialization that only agrees with itself.
        """
        module = load_module()
        rows = [
            module.Row("app.js", 11776, 452,
                       "4ae8bf8ede12a97627c63696f4b99172ba9cdbead519696a282035c4eab8d733"),
            module.Row("index.html", 1666, 42,
                       "27d54db89978ea1e9677ac953689a04ed077991f6dc35cf00a713e413fc385a2"),
            module.Row("styles.css", 3914, 252,
                       "94c4ee228c4e192c07e1794e6abe957bd3506a66235e8573842d39a4cf8b84f8"),
        ]
        serialized = module.serialize(rows)
        self.assertEqual(251, len(serialized))
        self.assertEqual(
            "36bc4407514265db0bd0fcaa9dde87ad2db18373ed5646fd178ec97af5a9ba4a",
            hashlib.sha256(serialized).hexdigest())
        self.assertTrue(serialized.endswith(b"\n"))

    def test_parse_manifest_sorts_rows_and_reads_the_comment(self):
        module = load_module()
        rows = [module.Row("b.txt", 1, 0, "a" * 64),
                module.Row("a.txt", 2, 1, "b" * 64)]
        serialized = module.serialize(rows)
        raw = (b"b.txt\t1\t0\t" + b"a" * 64 + b"\n"
               b"a.txt\t2\t1\t" + b"b" * 64 + b"\n"
               b"# aggregate rows=2 serialized_bytes=" + str(len(serialized)).encode()
               + b" sha256=" + hashlib.sha256(serialized).hexdigest().encode() + b"\n")
        parsed, serialized_bytes, aggregate = module.parse_manifest(raw)
        self.assertEqual(["a.txt", "b.txt"], [row.name for row in parsed])
        self.assertEqual(len(serialized), serialized_bytes)
        self.assertEqual(hashlib.sha256(serialized).hexdigest(), aggregate)

    def test_parse_manifest_refuses_a_row_outside_the_documented_shape(self):
        module = load_module()
        for raw, expected in (
            (b"a.txt\t2\t1\n# aggregate rows=1 serialized_bytes=0 sha256=" + b"c" * 64 + b"\n",
             "manifest-row-fields:"),
            # A data row with no aggregate comment at all.
            (b"a.txt\t2\t1\t" + b"b" * 64 + b"\n",
             "manifest-comment-count:"),
        ):
            with self.subTest(expected=expected):
                with self.assertRaises(module.ManifestError) as raised:
                    module.parse_manifest(raw)
                self.assertIn(expected, str(raised.exception))


if __name__ == "__main__":
    unittest.main()
