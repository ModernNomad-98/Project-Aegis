"""Mocked tests for scripts/ci/aegis_verdict_gate_fetch.py (C1.1b G7).

No network and no live provider: every provider response is a mocked transport
object.  The adapter writes only into a temporary RUNNER_TEMP.  The moved
C1.1a package validators (inputs/canonical/catalogue/records) are exercised
against the adapter's real output, and the moved checker consumes it in one
integration test.
"""

from __future__ import annotations

import contextlib
import io
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

TESTS_DIR = pathlib.Path(__file__).resolve().parent
SCRIPTS_DIR = TESTS_DIR.parents[1]
CI_DIR = SCRIPTS_DIR / "ci"
REPO = TESTS_DIR.parents[2]
for directory in (SCRIPTS_DIR, TESTS_DIR, CI_DIR):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

import aegis_verdict_gate_fetch as adapter  # noqa: E402
from aegis_verdict_gate import gate, inputs  # noqa: E402

HEAD = subprocess.check_output(["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True).strip()
TOKEN = "ghs_mock_token_value_0123456789"
OWNER = "example-org"
NAME = "example-repo"
FULL = OWNER + "/" + NAME
API = "https://api.mock.test"
TREE = "b" * 40
OLD_HEAD = "c" * 40
PR = 77
FIXED_TIME = "2026-11-11T10:05:00Z"
COMMIT_TIME = "2026-11-11T09:30:00Z"


def response(document, status=200, headers=None):
    body = document if isinstance(document, bytes) else json.dumps(document).encode("utf-8")
    return adapter.Response(status, headers or {}, body)


def verdict_comment(head, *, value="PASS", cid=9001, author="reviewer-login",
                    created=FIXED_TIME, updated=None, detail="INDEPENDENT review."):
    body = "F verdict for %s\n\n%s\nVERDICT: %s\n" % (head, detail, value)
    return {
        "id": cid,
        "body": body,
        "created_at": created,
        "updated_at": updated or created,
        "user": {"login": author},
        "html_url": "https://mock.test/comments/%d" % cid,
    }


def commit(sha, *, author="author-login", date=COMMIT_TIME):
    return {
        "sha": sha,
        "author": {"login": author} if author else None,
        "commit": {
            "author": {"email": ("%s@example.test" % author) if author else "", "date": date},
            "committer": {"date": date},
        },
    }


class FakeTransport:
    def __init__(self, routes):
        self.routes = list(routes)
        self.calls = []
        self.headers = []

    def get(self, url, headers):
        self.calls.append(url)
        self.headers.append(dict(headers))
        for prefix, value in self.routes:
            if url.startswith(prefix):
                return value(url, headers) if callable(value) else value
        raise adapter.TransportError("no mocked route for the request")


class FailingTransport:
    def __init__(self):
        self.calls = 0

    def get(self, url, headers):
        self.calls += 1
        raise adapter.TransportError("request failed: TimeoutError")


class Harness:
    def __init__(self, temporary, **overrides):
        self.root = pathlib.Path(temporary)
        self.run_dir = self.root / "run"
        self.event_name = overrides.get("event_name", "pull_request_target")
        self.action = overrides.get("action", "opened")
        self.head = overrides.get("head", HEAD)
        self.base = overrides.get("base", HEAD)
        self.pr_head = overrides.get("pr_head", self.head)
        self.pr_base = overrides.get("pr_base", self.base)
        self.pr_state = overrides.get("pr_state", "open")
        self.api_pr_number = overrides.get("api_pr_number", PR)
        self.comments = overrides.get("comments", [verdict_comment(self.head)])
        self.commits = overrides.get("commits", [commit(self.head)])
        self.comment_list = overrides.get("comment_list", self.comments)
        self.non_pr = overrides.get("non_pr", False)
        self.token = overrides.get("token", TOKEN)
        self.pr_response = overrides.get("pr_response")
        self.comments_response = overrides.get("comments_response")
        self.transport_error = overrides.get("transport_error", False)
        self.pr = self._pr()
        self.event = self._event()
        (self.root / "event.json").write_text(json.dumps(self.event), encoding="utf-8")
        self.transport = FailingTransport() if self.transport_error else FakeTransport(self._routes())

    def _pr(self):
        return {
            "number": self.api_pr_number,
            "state": self.pr_state,
            "html_url": "https://mock.test/pull/%d" % PR,
            "user": {"login": "author-login"},
            "body": "Plan: bounded provider adapter. Owner line AEGIS-APR-047.",
            "created_at": "2026-11-11T09:00:00Z",
            "updated_at": "2026-11-11T10:00:00Z",
            "head": {
                "sha": self.pr_head,
                "ref": "feature-branch",
                "repo": {"full_name": FULL},
            },
            "base": {
                "sha": self.pr_base,
                "ref": "main",
                "repo": {"full_name": FULL},
            },
        }

    def _event_pr(self):
        # The event payload and the provider are different snapshots: the
        # event names the head/base it fired for, the API names the current
        # values.  Keeping them separate is what makes the head-moved and
        # base-mismatch cases testable.
        pull_request = json.loads(json.dumps(self.pr))
        pull_request["head"]["sha"] = self.head
        pull_request["base"]["sha"] = self.base
        return pull_request

    def _event(self):
        if self.event_name == "pull_request_target":
            return {
                "repository": {"full_name": FULL},
                "action": self.action,
                "number": PR,
                "pull_request": self._event_pr(),
            }
        issue = {"number": PR}
        if not self.non_pr:
            issue["pull_request"] = {"url": "https://mock.test/pull/%d" % PR}
        return {
            "repository": {"full_name": FULL},
            "action": self.action,
            "issue": issue,
            "comment": verdict_comment(self.head),
        }

    def _routes(self):
        routes = [
            (API + "/repos/" + FULL + "/pulls/%d/commits" % PR, response(self.commits)),
            (
                API + "/repos/" + FULL + "/issues/%d/comments" % PR,
                self.comments_response or response(self.comment_list),
            ),
            (
                API + "/repos/" + FULL + "/commits/" + self.head,
                response(
                    {
                        "sha": self.head,
                        "commit": {
                            "tree": {"sha": TREE},
                            "author": {"date": COMMIT_TIME},
                            "committer": {"date": COMMIT_TIME},
                        },
                        "parents": [],
                    }
                ),
            ),
            (API + "/repos/" + FULL + "/pulls/%d" % PR, self.pr_response or response(self.pr)),
        ]
        return routes

    @property
    def environ(self):
        values = {
            "GITHUB_REPOSITORY": FULL,
            "GITHUB_API_URL": API,
            "GITHUB_EVENT_NAME": self.event_name,
            "GITHUB_EVENT_PATH": str(self.root / "event.json"),
            "GITHUB_RUN_ID": "12345",
            "RUNNER_TEMP": str(self.root),
            "AEGIS_VERDICT_RUN_DIR": str(self.run_dir),
            "AEGIS_VERDICT_CHECKOUT_SHA": HEAD,
        }
        if self.token is not None:
            values["GITHUB_TOKEN"] = self.token
        return values

    def run(self, mode="fetch"):
        arguments = ["--resolve-only"] if mode == "resolve" else ["--fetch"]
        arguments += ["--repo-root", str(REPO)]
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = adapter.main(arguments, transport=self.transport, environ=self.environ)
        return code, out.getvalue(), err.getvalue()

    def result(self):
        return json.loads((self.run_dir / "adapter-result.json").read_text(encoding="utf-8"))

    def envelope(self, name):
        return json.loads((self.run_dir / name).read_text(encoding="utf-8"))


class AdapterTestCase(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="aegis-adapter-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = pathlib.Path(self.temporary.name)

    def harness(self, **overrides):
        return Harness(self.root, **overrides)

    def fetch_ok(self, harness):
        code, out, err = harness.run("resolve")
        self.assertEqual(0, code, out + err)
        code, out, err = harness.run("fetch")
        self.assertEqual(0, code, out + err)
        return out, err


class ValidEvaluationTests(AdapterTestCase):
    def test_valid_f_verdict_is_extracted_and_bound_to_the_head(self):
        harness = self.harness()
        out, err = self.fetch_ok(harness)
        payload = harness.envelope("verdict.json")["payload"]
        self.assertEqual(FULL.split("/")[0], payload["repo"]["owner"])
        self.assertEqual(PR, payload["change"]["id"])
        self.assertEqual(HEAD, payload["head_sha"])
        self.assertEqual(TREE, payload["tree_sha"])
        self.assertEqual("refs/heads/main", payload["merge_target"]["ref"])
        self.assertEqual("PASS", payload["verdict"]["value"])
        self.assertEqual("F", payload["verdict"]["stage"])
        self.assertTrue(payload["verdict"]["posted_after_last_commit"])
        self.assertEqual(0, payload["verdict"]["edit_state"]["post_post_edits"])
        self.assertFalse(payload["verdict"]["edit_state"]["deleted"])
        self.assertTrue(payload["verdict"]["edit_state"]["body_hash_match"])
        distinct = payload["reviewer"]["independence"]["distinct_from"]
        for identity in ("implementer", "pr-author", "author-login"):
            self.assertIn(identity, distinct)
        self.assertNotIn("reviewer-login", distinct)
        self.assertFalse(payload["reviewer"]["auth_verified"])
        self.assertEqual("UNVERIFIED", payload["reviewer"]["auth_method"])
        result = harness.result()
        self.assertFalse(result["pre_f"])
        self.assertEqual("PASS", result["verdict"]["value"])
        self.assertEqual([], result["stale_verdict_comment_ids"])
        self.assertFalse(TOKEN in out or TOKEN in err)

    def test_every_envelope_passes_the_moved_package_validators(self):
        harness = self.harness()
        self.fetch_ok(harness)
        for name in ("verdict.json", "freeze.json", "settlement.json", "head-history.json"):
            with self.subTest(envelope=name):
                envelope = inputs.load_envelope(harness.run_dir / name)
                self.assertEqual([], envelope.issues)
                self.assertEqual(
                    envelope.file_sha256,
                    envelope.report()["sha256"],
                )
        history_path = harness.run_dir / "head-history.json"
        history = inputs.load_envelope(history_path)
        self.assertEqual("UNVERIFIED", history.provenance["status"])
        validation = inputs.validate_head_history(history, harness.envelope("verdict.json")["payload"])
        codes = [issue.code for issue in validation.issues]
        self.assertIn("REQUIRED_INPUT_UNAVAILABLE", codes)
        self.assertEqual("UNVERIFIED", validation.status)

    def test_provenance_manifest_names_the_sources_and_the_unavailable_fields(self):
        harness = self.harness()
        self.fetch_ok(harness)
        manifest = harness.envelope("provenance-manifest.json")
        self.assertEqual(adapter.SCHEMA_PROVENANCE, manifest["schema"])
        names = [source["name"] for source in manifest["sources"]]
        for name in ("event_payload", "pull_request", "pull_request_commits", "pull_request_comments"):
            self.assertIn(name, names)
        self.assertEqual(
            sorted(["verdict.json", "freeze.json", "settlement.json", "head-history.json"]),
            sorted(manifest["files"]),
        )
        for field in ("candidate_id", "triage", "stage_records", "skills/security/witness"):
            self.assertIn(field, manifest["unavailable_fields"])
        self.assertIn("candidate_id", harness.result()["unavailable"])

    def test_moved_checker_consumes_the_adapter_output_and_fails_closed(self):
        harness = self.harness()
        self.fetch_ok(harness)
        arguments = dict(
            repo_root=REPO,
            verdict_path=str(harness.run_dir / "verdict.json"),
            freeze_path=str(harness.run_dir / "freeze.json"),
            settlement_path=str(harness.run_dir / "settlement.json"),
            head_history_path=str(harness.run_dir / "head-history.json"),
            stage_records_dir=str(harness.run_dir / "stage-records"),
            records_dir="docs/approvals/revision-state",
            fixture_mode=False,
        )
        first = gate.evaluate(**arguments)
        second = gate.evaluate(**arguments)
        self.assertFalse(first.readiness)
        self.assertTrue(first.blockers)
        self.assertEqual("PRODUCTION", first.assurance["mode"])
        self.assertEqual(first.as_dict(), second.as_dict())
        self.assertNotEqual(0, len(first.blockers))

    def test_issue_comment_resolves_the_pull_request_from_the_provider(self):
        harness = self.harness(event_name="issue_comment", action="created")
        out, err = self.fetch_ok(harness)
        context = harness.envelope("gate-context.json")
        self.assertEqual("evaluate", context["decision"])
        self.assertEqual(HEAD, context["head_sha"])
        self.assertEqual(HEAD, context["base_sha"])
        self.assertFalse(TOKEN in out or TOKEN in err)

    def test_output_is_deterministic_for_identical_provider_data(self):
        first = self.harness()
        self.fetch_ok(first)
        second_root = pathlib.Path(tempfile.mkdtemp(dir=str(self.root)))
        second = Harness(second_root)
        self.fetch_ok(second)
        for name in ("verdict.json", "freeze.json", "settlement.json", "head-history.json", "provenance-manifest.json"):
            with self.subTest(file=name):
                self.assertEqual(
                    (first.run_dir / name).read_bytes(),
                    (second.run_dir / name).read_bytes(),
                )
        self.assertEqual(first.result(), second.result())


class VerdictFailureTests(AdapterTestCase):
    def test_pre_f_pull_request_writes_no_verdict_and_blocks_settlement(self):
        harness = self.harness(comments=[])
        self.fetch_ok(harness)
        payload = harness.envelope("verdict.json")["payload"]
        self.assertNotIn("verdict", payload)
        self.assertNotIn("reviewer", payload)
        self.assertTrue(harness.result()["pre_f"])
        settlement = harness.envelope("settlement.json")["payload"]
        self.assertFalse(settlement["settled"])
        self.assertEqual("PENDING", settlement["review_sources"][0]["state"])

    def test_f_verdict_at_another_head_is_not_bound(self):
        harness = self.harness(comments=[verdict_comment(OLD_HEAD)])
        self.fetch_ok(harness)
        result = harness.result()
        self.assertTrue(result["pre_f"])
        self.assertEqual([9001], result["stale_verdict_comment_ids"])
        self.assertNotIn("verdict", harness.envelope("verdict.json")["payload"])

    def test_duplicate_f_verdicts_at_the_head_are_ambiguous(self):
        harness = self.harness(
            comments=[verdict_comment(HEAD, cid=1), verdict_comment(HEAD, cid=2)]
        )
        self.fetch_ok(harness)
        result = harness.result()
        self.assertTrue(result["pre_f"])
        self.assertIsNotNone(result["ambiguity_detail"])
        self.assertEqual([1, 2], sorted(result["ambiguous_verdict_comment_ids"]))
        self.assertNotIn("verdict", harness.envelope("verdict.json")["payload"])

    def test_edited_f_comment_marks_post_post_edits_and_blocks_settlement(self):
        edited = verdict_comment(HEAD, updated="2026-11-11T10:06:00Z")
        harness = self.harness(event_name="issue_comment", action="edited", comments=[edited])
        self.fetch_ok(harness)
        verdict = harness.envelope("verdict.json")["payload"]["verdict"]
        self.assertEqual(1, verdict["edit_state"]["post_post_edits"])
        self.assertFalse(verdict["edit_state"]["body_hash_match"])
        self.assertFalse(harness.envelope("settlement.json")["payload"]["settled"])

    def test_deleted_f_comment_is_recorded_as_deleted(self):
        harness = self.harness(
            event_name="issue_comment", action="deleted", comments=[]
        )
        self.fetch_ok(harness)
        verdict = harness.envelope("verdict.json")["payload"]["verdict"]
        self.assertTrue(verdict["edit_state"]["deleted"])
        self.assertFalse(verdict["edit_state"]["body_hash_match"])
        self.assertFalse(harness.envelope("settlement.json")["payload"]["settled"])

    def test_non_pr_issue_comment_is_a_recorded_noop_without_a_token(self):
        harness = self.harness(event_name="issue_comment", action="created", non_pr=True, token=None)
        code, out, err = harness.run("resolve")
        self.assertEqual(0, code, out + err)
        result = harness.result()
        self.assertEqual("no-op", result["decision"])
        self.assertEqual(0, result["provider_calls"])
        self.assertEqual([], list(harness.transport.calls))
        self.assertFalse((harness.run_dir / "verdict.json").exists())


class ProviderRefusalTests(AdapterTestCase):
    def test_foreign_pull_request_is_refused(self):
        harness = self.harness(api_pr_number=78)
        code, out, err = harness.run("resolve")
        self.assertEqual(5, code, out + err)
        self.assertEqual("failed", harness.result()["outcome"])

    def test_foreign_repository_is_refused(self):
        harness = self.harness()
        harness.event["repository"]["full_name"] = "other-org/other-repo"
        (harness.root / "event.json").write_text(json.dumps(harness.event), encoding="utf-8")
        code, out, err = harness.run("resolve")
        self.assertEqual(5, code, out + err)
        self.assertEqual("failed", harness.result()["outcome"])
        self.assertEqual([], list(harness.transport.calls))

    def test_missing_token_fails_closed_before_any_provider_call(self):
        harness = self.harness(token=None)
        code, out, err = harness.run("resolve")
        self.assertEqual(7, code, out + err)
        self.assertEqual([], list(harness.transport.calls))
        self.assertNotIn("ghs_", out + err)

    def test_base_mismatch_fails_closed_and_keeps_the_context(self):
        harness = self.harness(base=OLD_HEAD)
        code, out, err = harness.run("resolve")
        self.assertEqual(6, code, out + err)
        context = harness.envelope("gate-context.json")
        self.assertEqual(OLD_HEAD, context["base_sha"])
        self.assertFalse(context["base_matches"])
        self.assertEqual("failed", harness.result()["outcome"])
        self.assertFalse((harness.run_dir / "verdict.json").exists())

    def test_issue_comment_with_an_older_base_defers_to_the_resolved_base_checkout(self):
        harness = self.harness(event_name="issue_comment", action="created", base=OLD_HEAD)
        code, out, err = harness.run("resolve")
        self.assertEqual(0, code, out + err)
        context = harness.envelope("gate-context.json")
        self.assertEqual(OLD_HEAD, context["base_sha"])
        self.assertFalse(context["base_matches"])
        code, out, err = harness.run("fetch")
        self.assertEqual(6, code, out + err)
        self.assertIn("resolved base", out + err)

    def test_head_moved_after_the_event_fails_closed(self):
        harness = self.harness(head=OLD_HEAD, pr_head=HEAD)
        code, out, err = harness.run("resolve")
        self.assertEqual(8, code, out + err)
        self.assertEqual("failed", harness.result()["outcome"])
        self.assertFalse((harness.run_dir / "verdict.json").exists())

    def test_pull_request_closed_after_the_event_is_a_noop(self):
        harness = self.harness(pr_state="closed")
        code, out, err = harness.run("resolve")
        self.assertEqual(0, code, out + err)
        self.assertEqual("no-op", harness.result()["decision"])

    def test_force_pushed_history_is_never_reconstructed_or_guessed(self):
        harness = self.harness(commits=[commit(OLD_HEAD), commit(HEAD)])
        self.fetch_ok(harness)
        history = harness.envelope("head-history.json")
        self.assertEqual([], history["payload"]["heads"])
        self.assertEqual("UNVERIFIED", history["provenance"]["status"])
        self.assertNotIn("review_heads", harness.envelope("verdict.json")["payload"])
        codes = [issue["code"] for issue in harness.result()["derivations"]["head_history"]]
        self.assertIn("REQUIRED_INPUT_UNAVAILABLE", codes)

    def test_provider_failures_map_to_stable_exit_codes(self):
        cases = (
            ("401", adapter.Response(401, {}, b"{}"), 7),
            ("403", adapter.Response(403, {}, b"{}"), 7),
            ("404", adapter.Response(404, {}, b"{}"), 4),
            ("429", adapter.Response(429, {}, b"{}"), 4),
            ("500", adapter.Response(500, {}, b"{}"), 4),
            ("malformed", adapter.Response(200, {}, b"not json"), 4),
            ("oversized", adapter.Response(200, {}, b"x" * (adapter.MAX_BODY_BYTES + 1)), 4),
        )
        for label, pr_response, expected in cases:
            with self.subTest(case=label):
                root = pathlib.Path(tempfile.mkdtemp(dir=str(self.root)))
                harness = Harness(root, pr_response=pr_response)
                code, out, err = harness.run("resolve")
                self.assertEqual(expected, code, label + ": " + out + err)
                self.assertEqual("failed", harness.result()["outcome"])
                self.assertNotIn(TOKEN, out + err)

    def test_transport_timeout_is_a_provider_failure(self):
        harness = self.harness(transport_error=True)
        code, out, err = harness.run("resolve")
        self.assertEqual(4, code, out + err)
        self.assertIn("TimeoutError", out)

    def test_truncated_pagination_is_a_provider_failure(self):
        comments_url = API + "/repos/" + FULL + "/issues/%d/comments" % PR
        loop = adapter.Response(200, {"Link": '<%s>; rel="next"' % comments_url}, b"[]")
        harness = self.harness(comments_response=loop)
        code, out, err = harness.run("resolve")
        self.assertEqual(0, code, out + err)
        code, out, err = harness.run("fetch")
        self.assertEqual(4, code, out + err)
        self.assertIn("pagination", out)

    def test_missing_commit_author_is_recorded_and_blocks_independence(self):
        harness = self.harness(commits=[commit(HEAD, author=None)])
        self.fetch_ok(harness)
        result = harness.result()
        self.assertTrue(result["findings"]["missing_commit_author"])
        payload = harness.envelope("verdict.json")["payload"]
        self.assertNotIn("reviewer", payload)
        self.assertNotIn("commit_authors", payload["record"])


class SafetyTests(AdapterTestCase):
    def test_token_never_reaches_output_or_artifacts(self):
        harness = self.harness()
        code, out, err = harness.run("resolve")
        self.assertEqual(0, code, out + err)
        code, out, err = harness.run("fetch")
        self.assertEqual(0, code, out + err)
        self.assertNotIn(TOKEN, out + err)
        for path in self.root.rglob("*"):
            if path.is_file():
                with self.subTest(path=path.name):
                    self.assertNotIn(TOKEN, path.read_text(encoding="utf-8", errors="replace"))
        for headers in harness.transport.headers:
            self.assertEqual("Bearer " + TOKEN, headers["Authorization"])

    def test_adapter_reuses_the_package_validators_and_defines_no_second_schema(self):
        source = (CI_DIR / "aegis_verdict_gate_fetch.py").read_text(encoding="utf-8")
        self.assertIn("from aegis_verdict_gate import canonical, catalogue, inputs, records", source)
        for definition in ("def load_envelope", "def canonical_bytes", "def project_bound_fields", "def digest("):
            self.assertNotIn(definition, source)

    def test_adapter_executes_no_pull_request_code(self):
        source = (CI_DIR / "aegis_verdict_gate_fetch.py").read_text(encoding="utf-8")
        for forbidden in ("os.system", "eval(", "exec(", "refs/pull", "git checkout", "git fetch", "shell=True"):
            self.assertNotIn(forbidden, source)
        self.assertIn('"rev-parse", "HEAD"', source)

    def test_fetch_without_a_resolved_context_is_a_usage_error(self):
        harness = self.harness()
        code, out, err = harness.run("fetch")
        self.assertEqual(2, code, out + err)
        self.assertIn("no resolved gate context", out + err)

    def test_run_directory_outside_runner_temp_is_refused(self):
        harness = self.harness()
        environment = harness.environ
        environment["AEGIS_VERDICT_RUN_DIR"] = str(self.root.parent / "outside-run-dir")
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = adapter.main(["--resolve-only", "--repo-root", str(REPO)],
                                transport=harness.transport, environ=environment)
        self.assertEqual(2, code, out.getvalue() + err.getvalue())
        self.assertIn("RUNNER_TEMP", out.getvalue() + err.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
