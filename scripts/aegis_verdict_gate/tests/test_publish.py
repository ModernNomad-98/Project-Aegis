"""Mocked tests for scripts/ci/aegis_verdict_gate_publish.py (C1.1b G9).

No network: the read-only pull-request re-check and the single status POST are
served by a mocked transport that records every call.  The tests cover the
success/failure/error mapping, every refusal path, the no-op path, token
handling and the one-and-only-one-status discipline.
"""

from __future__ import annotations

import contextlib
import io
import json
import pathlib
import sys
import tempfile
import unittest

TESTS_DIR = pathlib.Path(__file__).resolve().parent
SCRIPTS_DIR = TESTS_DIR.parents[1]
CI_DIR = SCRIPTS_DIR / "ci"
for directory in (SCRIPTS_DIR, TESTS_DIR, CI_DIR):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

import aegis_verdict_gate_publish as publisher  # noqa: E402

HEAD = "a" * 40
OLD_HEAD = "c" * 40
BASE = "b" * 40
TOKEN = "ghs_mock_publish_token_0123456789"
OWNER = "example-org"
NAME = "example-repo"
FULL = OWNER + "/" + NAME
API = "https://api.mock.test"
SERVER = "https://server.mock.test"
PR = 77
CONTEXT = "aegis-verdict-gate"

BLOCKED_RESULT = {
    "readiness": False,
    "assurance": {"claim": "AUDITABLE", "mounted_coverage": "UNKNOWN", "mode": "PRODUCTION"},
    "blockers": [
        {
            "code": "VERDICT_STALE_OR_UNVERIFIED",
            "classification": "MANDATORY",
            "detail": "the verdict was not posted after the last commit",
        }
    ],
}
SUCCESS_RESULT = {
    "readiness": True,
    "assurance": {"claim": "AUDITABLE", "mounted_coverage": "UNKNOWN", "mode": "PRODUCTION"},
    "blockers": [],
}


def write_json(path, document):
    path.write_text(json.dumps(document), encoding="utf-8")


class PublisherHarness:
    def __init__(self, root, **overrides):
        self.root = pathlib.Path(root)
        self.run_dir = self.root / "run"
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.head = overrides.get("head", HEAD)
        self.base = overrides.get("base", BASE)
        self.repo = overrides.get("repo", FULL)
        self.decision = overrides.get("decision", "evaluate")
        self.change_type = overrides.get("change_type", "PR")
        self.checker_exit = overrides.get("checker_exit", 1)
        self.checker_result = overrides.get("checker_result", BLOCKED_RESULT)
        self.adapter = overrides.get(
            "adapter",
            {
                "schema": "aegis.verdict-gate-adapter-result/v1",
                "phase": "fetch",
                "outcome": "ok",
                "exit_code": 0,
                "head_sha": self.head,
            },
        )
        self.verdict_head = overrides.get("verdict_head", self.head)
        self.verdict_base = overrides.get("verdict_base", self.base)
        self.omit_verdict = overrides.get("omit_verdict", False)
        self.omit_adapter = overrides.get("omit_adapter", False)
        self.omit_checker = overrides.get("omit_checker", False)
        write_json(
            self.run_dir / "gate-context.json",
            {
                "schema": "aegis.verdict-gate-context/v1",
                "event_name": "pull_request_target",
                "event_action": "opened",
                "decision": self.decision,
                "reason": overrides.get("reason", "the issue is not a pull request"),
                "repo": self.repo,
                "change_type": self.change_type,
                "pull_request": PR,
                "head_sha": self.head,
                "base_sha": self.base,
                "run_id": "12345",
            },
        )
        if not self.omit_verdict:
            write_json(
                self.run_dir / "verdict.json",
                {
                    "payload": {
                        "repo": {"owner": OWNER, "name": NAME},
                        "change": {"type": "PR", "id": PR},
                        "head_sha": self.verdict_head,
                        "base_sha": self.verdict_base,
                    },
                    "provenance": {},
                },
            )
        if not self.omit_adapter:
            write_json(self.run_dir / "adapter-result.json", self.adapter)
        if not self.omit_checker:
            write_json(self.root / "checker.json", {"label": "verdict-gate", "exit_code": self.checker_exit})
            if isinstance(self.checker_result, str):
                (self.root / "checker.log").write_text(self.checker_result, encoding="utf-8")
            else:
                write_json(self.root / "checker.log", self.checker_result)

    @property
    def environ(self):
        return {
            "GITHUB_TOKEN": TOKEN,
            "GITHUB_REPOSITORY": FULL,
            "GITHUB_API_URL": API,
            "GITHUB_SERVER_URL": SERVER,
        }

    def run(self, transport, environ=None):
        arguments = [
            "--run-dir", str(self.run_dir),
            "--checker-record", str(self.root / "checker.json"),
            "--checker-log", str(self.root / "checker.log"),
        ]
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = publisher.main(arguments, transport=transport, environ=environ or self.environ)
        return code, out.getvalue(), err.getvalue()

    def result(self):
        return json.loads((self.run_dir / "publish-result.json").read_text(encoding="utf-8"))

    def summary(self):
        path = self.run_dir / "summary.md"
        return path.read_text(encoding="utf-8") if path.is_file() else ""


class FakeTransport:
    def __init__(self, **overrides):
        self.pr_head = overrides.get("pr_head", HEAD)
        self.pr_state = overrides.get("pr_state", "open")
        self.pr_number = overrides.get("pr_number", PR)
        self.post_status = overrides.get("post_status", 201)
        self.post_confirm = overrides.get("post_confirm")
        self.get_error = overrides.get("get_error", False)
        self.post_error = overrides.get("post_error", False)
        self.gets = []
        self.posts = []

    def get(self, url, headers):
        self.gets.append((url, dict(headers)))
        if self.get_error:
            raise publisher.TransportError("request failed: TimeoutError")
        return publisher.Response(
            200,
            {},
            json.dumps(
                {"number": self.pr_number, "state": self.pr_state, "head": {"sha": self.pr_head}}
            ).encode("utf-8"),
        )

    def post(self, url, headers, body):
        self.posts.append((url, dict(headers), body))
        if self.post_error:
            raise publisher.TransportError("request failed: TimeoutError")
        if self.post_status != 201:
            return publisher.Response(self.post_status, {}, b"{}")
        document = json.loads(body)
        confirmation = self.post_confirm or {
            "sha": self.pr_head,
            "context": CONTEXT,
            "state": document["state"],
        }
        return publisher.Response(201, {}, json.dumps(confirmation).encode("utf-8"))


class PublisherTestCase(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="aegis-publish-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = pathlib.Path(self.temporary.name)

    def harness(self, **overrides):
        return PublisherHarness(self.root, **overrides)


class StatusStateTests(PublisherTestCase):
    def test_success_posts_exactly_one_success_status(self):
        harness = self.harness(checker_exit=0, checker_result=SUCCESS_RESULT)
        transport = FakeTransport()
        code, out, err = harness.run(transport)
        self.assertEqual(0, code, out + err)
        self.assertEqual(1, len(transport.posts))
        url, headers, body = transport.posts[0]
        document = json.loads(body)
        self.assertEqual(API + "/repos/" + FULL + "/statuses/" + HEAD, url)
        self.assertEqual("success", document["state"])
        self.assertEqual(CONTEXT, document["context"])
        self.assertEqual(SERVER + "/" + FULL + "/actions/runs/12345", document["target_url"])
        self.assertLessEqual(len(document["description"]), publisher.MAX_DESCRIPTION)
        self.assertNotIn("Authorization", json.dumps(document))
        result = harness.result()
        self.assertTrue(result["posted"])
        self.assertEqual("success", result["state"])
        self.assertIn("not merge authority", harness.summary())
        self.assertIn("published status: success", harness.summary())

    def test_blocked_checker_posts_failure(self):
        harness = self.harness(checker_exit=1, checker_result=BLOCKED_RESULT)
        transport = FakeTransport()
        code, out, err = harness.run(transport)
        self.assertEqual(0, code, out + err)
        self.assertEqual(1, len(transport.posts))
        document = json.loads(transport.posts[0][2])
        self.assertEqual("failure", document["state"])
        self.assertIn("VERDICT_STALE_OR_UNVERIFIED", document["description"])
        self.assertEqual("failure", harness.result()["state"])

    def test_invalid_checker_posts_failure(self):
        harness = self.harness(checker_exit=2, checker_result="invalid input: missing --verdict")
        transport = FakeTransport()
        code, out, err = harness.run(transport)
        self.assertEqual(0, code, out + err)
        self.assertEqual("failure", json.loads(transport.posts[0][2])["state"])

    def test_internal_checker_posts_error(self):
        harness = self.harness(checker_exit=3, checker_result="")
        transport = FakeTransport()
        code, out, err = harness.run(transport)
        self.assertEqual(0, code, out + err)
        self.assertEqual("error", json.loads(transport.posts[0][2])["state"])

    def test_adapter_block_posts_failure_without_a_verdict_file(self):
        harness = self.harness(
            adapter={
                "schema": "aegis.verdict-gate-adapter-result/v1",
                "outcome": "failed",
                "exit_code": 6,
                "reason": "the resolved base does not equal the base-only checkout",
            },
            omit_verdict=True,
            omit_checker=True,
        )
        transport = FakeTransport()
        code, out, err = harness.run(transport)
        self.assertEqual(0, code, out + err)
        self.assertEqual(1, len(transport.posts))
        self.assertEqual("failure", json.loads(transport.posts[0][2])["state"])
        self.assertIn("base-only checkout", json.loads(transport.posts[0][2])["description"])

    def test_adapter_internal_posts_error(self):
        harness = self.harness(
            adapter={
                "schema": "aegis.verdict-gate-adapter-result/v1",
                "outcome": "failed",
                "exit_code": 3,
                "reason": "internal error: RuntimeError",
            },
            omit_verdict=True,
            omit_checker=True,
        )
        transport = FakeTransport()
        code, out, err = harness.run(transport)
        self.assertEqual(0, code, out + err)
        self.assertEqual("error", json.loads(transport.posts[0][2])["state"])

    def test_checker_exit_zero_without_readiness_true_is_never_success(self):
        harness = self.harness(checker_exit=0, checker_result={"readiness": False, "blockers": []})
        transport = FakeTransport()
        code, out, err = harness.run(transport)
        self.assertEqual(3, code, out + err)
        self.assertEqual([], transport.posts)
        self.assertFalse(harness.result()["posted"])

    def test_readiness_true_with_nonzero_exit_is_not_success(self):
        harness = self.harness(checker_exit=1, checker_result=SUCCESS_RESULT)
        transport = FakeTransport()
        code, out, err = harness.run(transport)
        self.assertEqual(0, code, out + err)
        self.assertEqual("failure", json.loads(transport.posts[0][2])["state"])

    def test_description_is_bounded_and_single_line(self):
        blocker = {
            "readiness": False,
            "blockers": [{"code": "REQUIRED_INPUT_UNAVAILABLE", "classification": "MANDATORY", "detail": "x" * 500}],
        }
        harness = self.harness(checker_exit=1, checker_result=blocker)
        transport = FakeTransport()
        harness.run(transport)
        description = json.loads(transport.posts[0][2])["description"]
        self.assertLessEqual(len(description), publisher.MAX_DESCRIPTION)
        self.assertNotIn("\n", description)


class RefusalTests(PublisherTestCase):
    def test_foreign_repository_is_refused(self):
        harness = self.harness(repo="other-org/other-repo")
        transport = FakeTransport()
        code, out, err = harness.run(transport)
        self.assertEqual(5, code, out + err)
        self.assertEqual([], transport.posts)
        self.assertFalse(harness.result()["posted"])

    def test_non_pr_noop_posts_nothing_and_needs_no_token(self):
        harness = self.harness(decision="no-op", omit_checker=True, omit_verdict=True, omit_adapter=True)
        environment = dict(harness.environ)
        environment.pop("GITHUB_TOKEN")
        transport = FakeTransport()
        code, out, err = harness.run(transport, environ=environment)
        self.assertEqual(0, code, out + err)
        self.assertEqual([], transport.posts)
        self.assertEqual([], transport.gets)
        self.assertFalse(harness.result()["posted"])

    def test_head_moved_before_publication_is_refused(self):
        harness = self.harness(checker_exit=0, checker_result=SUCCESS_RESULT)
        transport = FakeTransport(pr_head=OLD_HEAD)
        code, out, err = harness.run(transport)
        self.assertEqual(5, code, out + err)
        self.assertEqual(1, len(transport.gets))
        self.assertEqual([], transport.posts)
        self.assertIn("head moved", harness.result()["reason"])

    def test_closed_pull_request_is_refused(self):
        harness = self.harness(checker_exit=0, checker_result=SUCCESS_RESULT)
        transport = FakeTransport(pr_state="closed")
        code, out, err = harness.run(transport)
        self.assertEqual(5, code, out + err)
        self.assertEqual([], transport.posts)

    def test_verdict_head_mismatch_is_refused(self):
        harness = self.harness(verdict_head=OLD_HEAD)
        transport = FakeTransport()
        code, out, err = harness.run(transport)
        self.assertEqual(5, code, out + err)
        self.assertEqual([], transport.posts)
        self.assertIn("does not bind the resolved head", harness.result()["reason"])

    def test_missing_token_is_refused(self):
        harness = self.harness()
        environment = dict(harness.environ)
        environment.pop("GITHUB_TOKEN")
        transport = FakeTransport()
        code, out, err = harness.run(transport, environ=environment)
        self.assertEqual(7, code, out + err)
        self.assertEqual([], transport.posts)
        self.assertNotIn(TOKEN, out + err)

    def test_adapter_result_missing_is_an_error(self):
        harness = self.harness(omit_adapter=True)
        transport = FakeTransport()
        code, out, err = harness.run(transport)
        self.assertEqual(3, code, out + err)
        self.assertEqual([], transport.posts)

    def test_provider_get_failure_posts_nothing(self):
        harness = self.harness()
        transport = FakeTransport(get_error=True)
        code, out, err = harness.run(transport)
        self.assertEqual(4, code, out + err)
        self.assertEqual([], transport.posts)

    def test_provider_post_failure_is_one_attempt_and_no_success(self):
        harness = self.harness(checker_exit=0, checker_result=SUCCESS_RESULT)
        transport = FakeTransport(post_status=500)
        code, out, err = harness.run(transport)
        self.assertEqual(4, code, out + err)
        self.assertEqual(1, len(transport.posts))
        self.assertFalse(harness.result()["posted"])

    def test_provider_post_timeout_is_one_attempt(self):
        harness = self.harness()
        transport = FakeTransport(post_error=True)
        code, out, err = harness.run(transport)
        self.assertEqual(4, code, out + err)
        self.assertEqual(1, len(transport.posts))

    def test_unconfirmed_post_is_an_error_and_not_retried(self):
        harness = self.harness(checker_exit=0, checker_result=SUCCESS_RESULT)
        transport = FakeTransport(post_confirm={"sha": OLD_HEAD, "context": CONTEXT, "state": "success"})
        code, out, err = harness.run(transport)
        self.assertEqual(3, code, out + err)
        self.assertEqual(1, len(transport.posts))
        self.assertEqual("unknown", harness.result()["posted"])


class SafetyTests(PublisherTestCase):
    def test_token_never_reaches_output_or_artifacts(self):
        harness = self.harness(checker_exit=0, checker_result=SUCCESS_RESULT)
        transport = FakeTransport()
        code, out, err = harness.run(transport)
        self.assertEqual(0, code, out + err)
        self.assertNotIn(TOKEN, out + err)
        for path in self.root.rglob("*"):
            if path.is_file():
                with self.subTest(path=path.name):
                    self.assertNotIn(TOKEN, path.read_text(encoding="utf-8", errors="replace"))
        self.assertEqual("Bearer " + TOKEN, transport.gets[0][1]["Authorization"])

    def test_publisher_is_the_only_writer_and_posts_once(self):
        harness = self.harness(checker_exit=0, checker_result=SUCCESS_RESULT)
        transport = FakeTransport()
        harness.run(transport)
        self.assertEqual(1, len(transport.posts))
        self.assertEqual(1, transport.posts[0][1]["Content-Type"].count("application/json"))
        self.assertIn("statuses/" + HEAD, transport.posts[0][0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
