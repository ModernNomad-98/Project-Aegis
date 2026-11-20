#!/usr/bin/env python3
"""Regression tests for scripts/ci/bound_fields_hash.py (issue #1143).

The bug: a bound-fields hash reproduction that decoded the PR body with the
host locale default (cp1252 on the machine where the artifact was observed)
produced a different hash from the UTF-8 one, because each U+2013, U+2014 and
U+2192 character is three bytes in UTF-8 and therefore three characters under
cp1252. The recorded instance is PR #1142 review round 3: the cp1252 decode
gave f47b07e932e0b3f6 where the correct UTF-8 hash was 1889afe37b1217fa.

These tests prove both halves of the issue's required proof:
  * fail under cp1252 - decoding the same body bytes as cp1252 expands each
    affected character from 1 character to 3 and changes the hash;
  * pass under UTF-8 - the tool and its explicit UTF-8 read/write produce the
    published method's hash, identical under a hostile PYTHONIOENCODING and
    under the host's cp1252 default.

They also prove the tool never silently falls back to the locale: a
cp1252-encoded body is refused with exit 2 and no hash, and a static AST check
rejects locale-default reads and writes in the tool source.

Run locally (the file is not wired into a CI step; adding one would change
.github/workflows/, which is outside this change):
    python -P scripts/tests/test_bound_fields_hash.py
"""
import ast
import hashlib
import importlib.util
import json
import locale
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOL_PATH = REPO_ROOT / "scripts" / "ci" / "bound_fields_hash.py"
FIELDS = ("witness", "skills", "security")
EN_DASH = "\u2013"
EM_DASH = "\u2014"
ARROW = "\u2192"
HOST_LOCALE = locale.getencoding().lower()


def load_tool():
    spec = importlib.util.spec_from_file_location(
        "bound_fields_hash_under_test", TOOL_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fixture_body():
    return (
        "# Fixture pull-request body " + EN_DASH + " unicode bound fields\n\n"
        "Intro " + EM_DASH + " with " + ARROW + " outside the bound fields.\n\n"
        "<!-- bound-field: witness -->\n\n"
        "| 1 | The MG block | unchanged " + EN_DASH + " verified |\n"
        "| 2 | The SD block | unchanged " + EM_DASH + " verified |\n\n"
        "<!-- bound-field: end -->\n\n"
        "<!-- bound-field: skills -->\n\n"
        "| Skill | Stage / agent | How applied | Result / evidence |\n"
        "| --- | --- | --- | --- |\n"
        "| a | b " + EN_DASH + " c | d " + ARROW + " e | f |\n\n"
        "<!-- bound-field: end -->\n\n"
        "<!-- bound-field: security -->\n\n"
        "- [x] No " + EM_DASH + " no security-relevant surface\n\n"
        "<!-- bound-field: end -->\n"
    )


def reference_payloads(body):
    """Independent whole-line-sentinel implementation of the published method."""
    lines = re.split(r"\r\n|\n|\r", body)
    payloads = {}
    for field in FIELDS:
        marker = "<!-- bound-field: " + field + " -->"
        starts = [i for i, line in enumerate(lines) if line.strip() == marker]
        assert len(starts) == 1, "fixture must open " + field + " exactly once"
        start = starts[0]
        ends = [i for i in range(start + 1, len(lines))
                if lines[i].strip() == "<!-- bound-field: end -->"]
        assert ends, "fixture must close " + field
        payload = "\n".join(lines[start + 1:ends[0]])
        payloads[field] = re.sub(r"\s+", " ", payload).strip()
    return payloads


def reference_joined(body):
    payloads = reference_payloads(body)
    return "\n".join(payloads[field] for field in FIELDS)


def reference_hash16(body):
    return hashlib.sha256(reference_joined(body).encode("utf-8")).hexdigest()[:16]


def reference_sha256(body):
    return hashlib.sha256(reference_joined(body).encode("utf-8")).hexdigest()


def run_cli(arguments, stdin_bytes=None, env_extra=None):
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [sys.executable, "-P", str(TOOL_PATH), *arguments],
        cwd=str(REPO_ROOT), input=stdin_bytes, capture_output=True, env=env)


class BoundFieldsHashTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool = load_tool()

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="aegis-t1143-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def write_body(self, name, text, encoding="utf-8"):
        path = self.root / name
        path.write_bytes(text.encode(encoding))
        return path

    # -- the pass-under-UTF-8 half -------------------------------------------

    def test_utf8_body_matches_published_method(self):
        record = self.tool.report(fixture_body())
        self.assertEqual(reference_hash16(fixture_body()), record["hash16"])
        self.assertEqual(reference_sha256(fixture_body()), record["sha256"])
        self.assertEqual("utf-8", record["encoding"])
        expected = reference_payloads(fixture_body())
        for field in FIELDS:
            self.assertEqual(len(expected[field]),
                             record["fields"][field]["chars"])

    def test_cli_utf8_body_passes_and_records_encoding(self):
        path = self.write_body("body.md", fixture_body())
        result = run_cli(["--body-file", str(path)])
        self.assertEqual(0, result.returncode, result.stderr.decode("utf-8"))
        output = result.stdout.decode("utf-8")
        self.assertIn("bound-fields hash: " + reference_hash16(fixture_body()),
                      output)
        self.assertIn("sha256: " + reference_sha256(fixture_body()), output)
        self.assertIn("encoding: UTF-8", output)
        self.assertIn("no locale default", output)

    def test_cli_json_records_encoding_and_is_deterministic(self):
        path = self.write_body("body.md", fixture_body())
        first = run_cli(["--body-file", str(path), "--json"])
        second = run_cli(["--body-file", str(path), "--json"])
        self.assertEqual(0, first.returncode, first.stderr.decode("utf-8"))
        self.assertEqual(0, second.returncode, second.stderr.decode("utf-8"))
        self.assertEqual(first.stdout, second.stdout)
        payload = json.loads(first.stdout.decode("utf-8"))
        self.assertEqual("utf-8", payload["encoding"])
        self.assertEqual(reference_hash16(fixture_body()), payload["hash16"])
        self.assertEqual(reference_sha256(fixture_body()), payload["sha256"])
        for field in FIELDS:
            self.assertEqual(len(reference_payloads(fixture_body())[field]),
                             payload["fields"][field]["chars"])

    def test_stdin_read_is_utf8(self):
        result = run_cli(["--body-file", "-"],
                         stdin_bytes=fixture_body().encode("utf-8"))
        self.assertEqual(0, result.returncode, result.stderr.decode("utf-8"))
        self.assertIn("bound-fields hash: " + reference_hash16(fixture_body()),
                      result.stdout.decode("utf-8"))

    def test_locale_hostile_environment_output_identical(self):
        path = self.write_body("body.md", fixture_body())
        normal = run_cli(["--body-file", str(path)])
        hostile = run_cli(
            ["--body-file", str(path)],
            env_extra={"PYTHONIOENCODING": "cp1252", "PYTHONUTF8": "0"})
        self.assertEqual(0, normal.returncode)
        self.assertEqual(0, hostile.returncode,
                         hostile.stderr.decode("utf-8", "replace"))
        self.assertEqual(normal.stdout, hostile.stdout)
        self.assertIn("encoding: UTF-8",
                      hostile.stdout.decode("utf-8"))

    def test_fixture_exercises_en_dash_em_dash_and_arrow(self):
        body = fixture_body()
        joined = "\n".join(reference_payloads(body).values())
        for character in (EN_DASH, EM_DASH, ARROW):
            self.assertIn(character, body)
            self.assertIn(character, joined)

    # -- the fail-under-cp1252 half ------------------------------------------

    def test_each_affected_character_expands_under_cp1252(self):
        body = fixture_body()
        raw = body.encode("utf-8")
        mojibake = raw.decode("cp1252")
        for character in (EN_DASH, EM_DASH, ARROW):
            decoded = character.encode("utf-8").decode("cp1252")
            self.assertEqual(3, len(decoded),
                             "each UTF-8 byte must become one cp1252 character")
            self.assertNotEqual(character, decoded)
        self.assertGreater(len(mojibake), len(body))
        self.assertGreater(len(mojibake.encode("utf-8")), len(raw))
        self.assertNotEqual(reference_joined(body),
                            reference_joined(mojibake))

    def test_cp1252_decode_changes_the_hash(self):
        raw = fixture_body().encode("utf-8")
        mojibake = raw.decode("cp1252")
        correct = reference_hash16(fixture_body())
        artifact = reference_hash16(mojibake)
        self.assertNotEqual(correct, artifact)
        # The tool returns the UTF-8 figure, never the cp1252 artifact.
        self.assertEqual(correct, self.tool.report(fixture_body())["hash16"])
        self.assertNotEqual(artifact,
                            self.tool.report(fixture_body())["hash16"])

    def test_cp1252_encoded_body_is_refused_not_decoded(self):
        cp1252_body = fixture_body().replace(ARROW, "")
        path = self.root / "cp1252.md"
        path.write_bytes(cp1252_body.encode("cp1252"))
        result = run_cli(["--body-file", str(path)])
        self.assertEqual(2, result.returncode)
        self.assertIn("UTF-8", result.stderr.decode("utf-8", "replace"))
        self.assertNotIn("bound-fields hash:",
                         result.stdout.decode("utf-8", "replace"))

    def test_host_locale_default_read_would_differ(self):
        if HOST_LOCALE.startswith("utf-8") or HOST_LOCALE.startswith("utf8"):
            self.skipTest("host default encoding is UTF-8; no cp1252 artifact")
        path = self.write_body("body.md", fixture_body())
        explicit = path.read_text(encoding="utf-8")
        try:
            default_text = path.open("r").read()
        except UnicodeDecodeError:
            return
        self.assertEqual(explicit, fixture_body())
        self.assertNotEqual(default_text, explicit)
        self.assertNotEqual(reference_hash16(default_text),
                            reference_hash16(explicit))

    # -- fail-closed sentinel handling ---------------------------------------

    def test_missing_sentinel_is_error(self):
        without_witness = fixture_body().replace(
            "<!-- bound-field: witness -->\n\n"
            "| 1 | The MG block | unchanged " + EN_DASH + " verified |\n"
            "| 2 | The SD block | unchanged " + EM_DASH + " verified |\n\n"
            "<!-- bound-field: end -->\n\n", "")
        path = self.write_body("missing.md", without_witness)
        result = run_cli(["--body-file", str(path)])
        self.assertEqual(2, result.returncode)
        self.assertIn("witness", result.stderr.decode("utf-8", "replace"))
        self.assertNotIn("bound-fields hash:",
                         result.stdout.decode("utf-8", "replace"))

    def test_duplicate_opening_sentinel_is_error(self):
        duplicated = fixture_body().replace(
            "<!-- bound-field: skills -->",
            "<!-- bound-field: skills -->\n\n<!-- bound-field: skills -->")
        path = self.write_body("duplicate.md", duplicated)
        result = run_cli(["--body-file", str(path)])
        self.assertEqual(2, result.returncode)
        self.assertIn("duplicate", result.stderr.decode("utf-8", "replace"))

    def test_quoted_sentinel_text_is_not_a_sentinel(self):
        quoted = ("| the skills table | `<!-- bound-field: skills -->` | "
                  "`<!-- bound-field: end -->` |\n\n" + fixture_body())
        self.assertEqual(reference_hash16(fixture_body()),
                         reference_hash16(quoted))
        self.assertEqual(reference_hash16(fixture_body()),
                         self.tool.report(quoted)["hash16"])

    def test_whitespace_is_collapsed_and_trimmed(self):
        variant = fixture_body().replace(
            "| 1 | The MG block | unchanged " + EN_DASH + " verified |",
            "| 1 |   The MG block   | unchanged\n  " + EN_DASH
            + "  verified   |")
        self.assertEqual(reference_hash16(fixture_body()),
                         reference_hash16(variant))
        self.assertEqual(reference_hash16(fixture_body()),
                         self.tool.report(variant)["hash16"])

    # -- no locale default in the source -------------------------------------

    def test_source_has_no_locale_default_read_or_write(self):
        source = TOOL_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source)
        offenders = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split(".")[0] == "locale":
                        offenders.append("imports locale")
            if not isinstance(node, ast.Call):
                continue
            function = node.func
            encoding_kw = any(keyword.arg == "encoding"
                              for keyword in node.keywords)
            if isinstance(function, ast.Name) and function.id == "open":
                if not encoding_kw:
                    offenders.append("open() without encoding line "
                                     + str(node.lineno))
            if isinstance(function, ast.Attribute):
                if function.attr in ("read_text", "write_text") \
                        and not encoding_kw:
                    offenders.append(function.attr
                                     + "() without encoding line "
                                     + str(node.lineno))
                if function.attr == "read" \
                        and isinstance(function.value, ast.Attribute) \
                        and function.value.attr == "stdin":
                    offenders.append("sys.stdin.read() text-mode read line "
                                     + str(node.lineno))
            if isinstance(function, ast.Name) and function.id == "print":
                offenders.append("print() locale text write line "
                                 + str(node.lineno))
        self.assertEqual([], offenders)
        self.assertIn('.decode("utf-8")', source)
        self.assertIn('.encode("utf-8")', source)
        self.assertIn("sys.stdin.buffer.read()", source)
        self.assertIn("stream.buffer.write", source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
