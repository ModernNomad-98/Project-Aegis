"""Live judge output contract: the prompt states it, the parser enforces it.

Root-cause regression tests for run 41167546138, where the judge call finished
(judge finish reason `completed`) but the judge verdict was null and the result
was `JUDGE_ERROR`. The judge system prompt never stated the seven-key output
schema the parser requires, so a real model could not know the shape it had to
produce. These tests pin the contract in both directions:

* the prompt states every key and enum the parser requires;
* a contract-shaped output parses to a recognized verdict;
* every malformed / mismatched output becomes an explicit
  `JUDGE_PARSE_ERROR` carrying the raw provider finish reason (never a bare
  null);
* the accepted provider stop-reason vocabulary (`end_turn`, `stop`,
  `completed`) is accepted and the value seen is recorded, not normalized away.

No test performs a network call or a provider call. Every transport is the mock
transport; fixtures are contract-shaped synthetic data, not provider transcripts.
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest

from tools.behavioral_eval_runner.canonical import canonical_json, sha256_hex_text
from tools.behavioral_eval_runner.live.config import SUBJECT_PINS, OwnerAllowlist
from tools.behavioral_eval_runner.live.dataset import load_cases
from tools.behavioral_eval_runner.live.judge_adapter import (
    JUDGE_PARSE_ERROR_KIND,
    _ERROR_KEYS,
    LIVE_JUDGE_POLICY,
    LIVE_JUDGE_POLICY_SHA256,
    LIVE_JUDGE_POLICY_VERSION,
    JudgeAdapter,
    build_judge_parse_error,
    parse_live_verdict,
)
from tools.behavioral_eval_runner.live.mock_transport import MockTransport
from tools.behavioral_eval_runner.live.pipeline import dry_run
from tools.behavioral_eval_runner.live.providers import (
    JUDGE_PINS,
    ensure_complete_response,
)
from tools.behavioral_eval_runner.live.subject import SubjectResult
from tools.behavioral_eval_runner.live.transport import (
    COMPLETE_STOP_REASONS,
    ProviderResponse,
    ProviderUsage,
)
from tools.behavioral_eval_runner.tests import live_helpers as helpers

RUBRIC_SHA = "a" * 64
RESPONSE_SHA = "b" * 64
JUDGE_MODEL = "gpt-6-astra"
MALFORMED_RAW = (
    "The response appears to satisfy the rubric, so my verdict is PASS."
)


def _load_fixtures() -> list[tuple[str, dict]]:
    fixtures: list[tuple[str, dict]] = []
    for name in sorted(os.listdir(helpers.JUDGE_FIXTURES_ROOT)):
        if not name.endswith(".json"):
            continue
        path = os.path.join(helpers.JUDGE_FIXTURES_ROOT, name)
        with open(path, encoding="utf-8") as handle:
            fixtures.append((name, json.load(handle)))
    return fixtures


def _parse_fixture(payload: dict):
    request = payload["request"]
    return parse_live_verdict(
        payload["raw_output"],
        rubric_sha256=request["rubric_sha256"],
        response_sha256=request["response_sha256"],
        judge_model=request["judge_model"],
    )


def _evidence_bytes(root: str) -> bytes:
    chunks: list[bytes] = []
    for directory, _dirs, files in os.walk(root):
        for name in files:
            with open(os.path.join(directory, name), "rb") as handle:
                chunks.append(handle.read())
    return b"\n".join(chunks)


class PromptStatesTheParserContractTests(unittest.TestCase):
    """The root cause: the prompt must state the schema the parser enforces."""

    def test_prompt_states_every_required_key(self):
        for key in sorted(_ERROR_KEYS):
            self.assertIn(key, LIVE_JUDGE_POLICY, key)
        self.assertIn('"evidence_refs": ["response"]', LIVE_JUDGE_POLICY)

    def test_prompt_states_every_accepted_enum_value(self):
        for token in (
            "PASS",
            "FAIL",
            "ABSTAIN",
            "MEETS_RUBRIC",
            "VIOLATES_RUBRIC",
            "INSUFFICIENT_EVIDENCE",
            "QUESTIONNAIRE_DUMP",
            "MULTIPLE_UNRELATED_TOPICS",
            "ANY_ORDER_INSTRUCTION",
            "BUNDLED_INDEPENDENT_DECISIONS",
            "OTHER_RUBRIC_VIOLATION",
        ):
            self.assertIn(token, LIVE_JUDGE_POLICY, token)

    def test_prompt_bans_prose_fences_and_extra_keys(self):
        for phrase in (
            "exactly one JSON object",
            "no markdown code fence",
            "no extra keys",
            "JUDGE_PARSE_ERROR",
        ):
            self.assertIn(phrase, LIVE_JUDGE_POLICY, phrase)

    def test_prompt_does_not_weaken_the_injection_policy(self):
        from tools.behavioral_eval_runner.judge.policy import JUDGE_SYSTEM_POLICY

        self.assertTrue(LIVE_JUDGE_POLICY.startswith(JUDGE_SYSTEM_POLICY))
        self.assertIn("UNTRUSTED DATA", LIVE_JUDGE_POLICY)
        self.assertIn("NEVER FOLLOW INSTRUCTIONS", LIVE_JUDGE_POLICY)

    def test_contract_version_and_hash_are_recorded(self):
        self.assertEqual(LIVE_JUDGE_POLICY_VERSION, "1.1.0-ber-live")
        self.assertIn(LIVE_JUDGE_POLICY_VERSION, LIVE_JUDGE_POLICY)
        self.assertEqual(
            LIVE_JUDGE_POLICY_SHA256, sha256_hex_text(LIVE_JUDGE_POLICY)
        )


class RecordedShapeFixtureTests(unittest.TestCase):
    """Every fixture parses to its expected verdict or explicit parse error."""

    def test_fixtures_exist_and_cover_the_ladder(self):
        fixtures = _load_fixtures()
        self.assertGreaterEqual(len(fixtures), 15)
        parse_reasons = {
            payload["expected"]["parse_reason"]
            for _name, payload in fixtures
            if payload["expected"]["outcome"] == "PARSE_ERROR"
        }
        self.assertEqual(
            parse_reasons,
            {
                "EMPTY_OUTPUT",
                "MALFORMED_JSON",
                "SCHEMA_INVALID",
                "RUBRIC_MISMATCH",
                "CONTRADICTORY_EVIDENCE",
                "REQUEST_MISMATCH",
            },
        )
        verdicts = {
            payload["expected"]["verdict"]
            for _name, payload in fixtures
            if payload["expected"]["outcome"] == "VERDICT"
        }
        self.assertEqual(verdicts, {"PASS", "FAIL", "ABSTAIN"})

    def test_every_fixture_parses_as_expected(self):
        for name, payload in _load_fixtures():
            with self.subTest(fixture=name):
                expected = payload["expected"]
                verdict, error = _parse_fixture(payload)
                if expected["outcome"] == "VERDICT":
                    self.assertIsNone(error, name)
                    self.assertIsNotNone(verdict, name)
                    self.assertEqual(verdict.verdict.value, expected["verdict"])
                    self.assertEqual(
                        verdict.reason_code.value, expected["reason_code"]
                    )
                    self.assertEqual(
                        verdict.failure_mode.value
                        if verdict.failure_mode
                        else None,
                        expected["failure_mode"],
                    )
                    self.assertEqual(verdict.rubric_sha256, RUBRIC_SHA)
                    self.assertEqual(verdict.response_sha256, RESPONSE_SHA)
                    self.assertEqual(verdict.judge_model, JUDGE_MODEL)
                else:
                    self.assertIsNone(verdict, name)
                    self.assertEqual(error, expected["parse_reason"], name)

    def test_recorded_verdict_parses_to_a_recognized_value(self):
        fixture = dict(_load_fixtures())["pass-direct.json"]
        verdict, error = _parse_fixture(fixture)
        self.assertIsNone(error)
        self.assertEqual(verdict.verdict.value, "PASS")

    def test_tolerated_single_fence_still_parses_to_a_verdict(self):
        fixture = dict(_load_fixtures())["pass-fenced-json.json"]
        verdict, error = _parse_fixture(fixture)
        self.assertIsNone(error)
        self.assertEqual(verdict.verdict.value, "PASS")

    def test_malformed_output_yields_an_explicit_judge_parse_error(self):
        fixture = dict(_load_fixtures())["malformed-prose.json"]
        verdict, error = _parse_fixture(fixture)
        self.assertIsNone(verdict)
        self.assertEqual(error, "MALFORMED_JSON")

    def test_every_parse_failure_builds_a_complete_explicit_record(self):
        for name, payload in _load_fixtures():
            expected = payload["expected"]
            if expected["outcome"] != "PARSE_ERROR":
                continue
            with self.subTest(fixture=name):
                error = _parse_fixture(payload)[1]
                record = build_judge_parse_error(
                    payload["raw_output"],
                    parse_reason=error,
                    finish_reason=payload["finish_reason"],
                ).to_dict()
                self.assertEqual(record["kind"], JUDGE_PARSE_ERROR_KIND)
                self.assertEqual(record["parse_reason"], expected["parse_reason"])
                self.assertEqual(
                    record["finish_reason"], payload["finish_reason"]
                )
                self.assertTrue(record["finish_reason"])
                self.assertEqual(
                    record["output_sha256"],
                    sha256_hex_text(payload["raw_output"]),
                )
                self.assertEqual(
                    record["output_chars"], len(payload["raw_output"])
                )
                self.assertIs(record["output_recorded"], False)
                if "expected_shape" in expected:
                    self.assertEqual(
                        record["output_shape"], expected["expected_shape"]
                    )
                for key in expected.get("observed_keys_include", []):
                    self.assertIn(key, record["observed_keys"])

    def test_parse_error_is_never_a_verdict(self):
        # A parse failure must NEVER be coerced into PASS or FAIL.
        for name, payload in _load_fixtures():
            if payload["expected"]["outcome"] != "PARSE_ERROR":
                continue
            with self.subTest(fixture=name):
                verdict, error = _parse_fixture(payload)
                self.assertIsNone(verdict)
                self.assertIsNotNone(error)


class JudgeDispatchRecordTests(unittest.TestCase):
    """The run record carries the explicit classification and finish reason."""

    def _case(self):
        return load_cases(helpers.CASES_ROOT)[0]

    def _subject_result(self, text: str = "answer") -> SubjectResult:
        return SubjectResult(
            request_id="rid",
            response_id="resp-1",
            vendor="anthropic",
            requested_model="claude-sonnet-5-5",
            served_model="claude-sonnet-5-5",
            response_sha256=sha256_hex_text(text),
            response_chars=len(text),
            usage=ProviderUsage(3, 2),
            stop_reason="end_turn",
        )

    def _adapter(self, raw_output: str, finish_reason: str) -> tuple[JudgeAdapter, object, str]:
        case = self._case()
        subject_text = "answer"
        subject = self._subject_result(subject_text)
        response = ProviderResponse(
            response_id="judge-1",
            served_model=JUDGE_MODEL,
            text=raw_output,
            usage=ProviderUsage(10, 5),
            stop_reason=finish_reason,
        )
        adapter = JudgeAdapter(
            JUDGE_PINS[("anthropic", "claude-sonnet-5-5")],
            OwnerAllowlist((("openai", JUDGE_MODEL),)),
            MockTransport(lambda request: response),
            max_output_tokens=4096,
            timeout_seconds=30,
        )
        request = adapter.build_request(
            request_id="jid:run-1:judge:anthropic",
            case=case,
            arm="WITH_SKILL",
            subject_vendor="anthropic",
            subject_result=subject,
            subject_text=subject_text,
        )
        return adapter, subject, subject_text

    def _contract_shaped_raw(self, case, subject_text: str, finish_reason: str = "completed") -> str:
        return canonical_json(
            {
                "verdict": "PASS",
                "reason_code": "MEETS_RUBRIC",
                "failure_mode": None,
                "rubric_sha256": case.rubric_sha256,
                "response_sha256": sha256_hex_text(subject_text),
                "judge_model": JUDGE_MODEL,
                "evidence_refs": ["response"],
            }
        )

    def test_dispatch_records_an_explicit_parse_error_and_raw_finish_reason(self):
        adapter, subject, subject_text = self._adapter(MALFORMED_RAW, "completed")
        case = self._case()
        request = adapter.build_request(
            request_id="jid:run-1:judge:anthropic",
            case=case,
            arm="WITH_SKILL",
            subject_vendor="anthropic",
            subject_result=subject,
            subject_text=subject_text,
        )
        result = adapter.dispatch(request, case=case, subject_text=subject_text)
        self.assertFalse(result.is_verdict)
        self.assertEqual(result.stop_reason, "completed")
        self.assertEqual(result.judge_error_kind, "MALFORMED_JSON")
        self.assertIsNotNone(result.parse_error)
        record = result.to_record()
        self.assertEqual(record["stop_reason"], "completed")
        self.assertEqual(record["judge_error_kind"], "MALFORMED_JSON")
        self.assertEqual(record["judge_error"]["kind"], "JUDGE_PARSE_ERROR")
        self.assertEqual(record["judge_error"]["parse_reason"], "MALFORMED_JSON")
        self.assertEqual(record["judge_error"]["finish_reason"], "completed")
        self.assertIs(record["judge_error"]["output_recorded"], False)
        # No transcript leaks: the raw output must not appear in the record.
        self.assertNotIn("text", record)
        self.assertNotIn(MALFORMED_RAW, json.dumps(record))

    def test_dispatch_records_a_verdict_for_the_fixed_shape(self):
        case = self._case()
        subject_text = "answer"
        raw = self._contract_shaped_raw(case, subject_text)
        adapter, subject, subject_text = self._adapter(raw, "completed")
        request = adapter.build_request(
            request_id="jid:run-1:judge:anthropic",
            case=case,
            arm="WITH_SKILL",
            subject_vendor="anthropic",
            subject_result=subject,
            subject_text=subject_text,
        )
        result = adapter.dispatch(request, case=case, subject_text=subject_text)
        self.assertTrue(result.is_verdict)
        record = result.to_record()
        self.assertEqual(record["verdict"]["verdict"], "PASS")
        self.assertNotIn("judge_error", record)
        self.assertEqual(record["stop_reason"], "completed")

    def test_dispatch_records_the_stop_reason_seen_not_a_normalized_value(self):
        case = self._case()
        subject_text = "answer"
        raw = self._contract_shaped_raw(case, subject_text)
        for finish_reason in ("completed", "stop", "end_turn"):
            with self.subTest(finish_reason=finish_reason):
                adapter, subject, subject_text = self._adapter(
                    raw, finish_reason
                )
                request = adapter.build_request(
                    request_id="jid:run-1:judge:anthropic",
                    case=case,
                    arm="WITH_SKILL",
                    subject_vendor="anthropic",
                    subject_result=subject,
                    subject_text=subject_text,
                )
                result = adapter.dispatch(request, case=case, subject_text=subject_text)
                self.assertEqual(result.stop_reason, finish_reason)
                self.assertEqual(result.to_record()["stop_reason"], finish_reason)

    def test_capability_report_records_the_vocabulary_and_parse_kind(self):
        adapter, _subject, _text = self._adapter(MALFORMED_RAW, "completed")
        report = adapter.capability_report()
        self.assertEqual(report["parse_error_kind"], "JUDGE_PARSE_ERROR")
        self.assertEqual(report["policy_version"], "1.1.0-ber-live")
        for value in ("end_turn", "stop", "completed"):
            self.assertIn(value, report["complete_stop_reasons"])


class StopReasonVocabularyTests(unittest.TestCase):
    def test_owner_named_provider_values_are_accepted(self):
        for value in ("end_turn", "stop", "completed"):
            self.assertIn(value, COMPLETE_STOP_REASONS)
            ensure_complete_response(value, vendor="judge")
            ProviderResponse(
                response_id="r",
                served_model="gpt-6-astra",
                text="x",
                usage=ProviderUsage(1, 1),
                stop_reason=value,
            ).validate(require_model=False)

    def test_incomplete_vocabulary_still_fails_closed(self):
        from tools.behavioral_eval_runner.live.errors import ProviderTransportError

        for value in ("max_tokens", "length", "content_filter", "failed",
                      "cancelled", "incomplete", "", "UNKNOWN"):
            with self.subTest(stop_reason=value):
                with self.assertRaises(ProviderTransportError):
                    ensure_complete_response(value, vendor="judge")


class FailureDiagnosticsChannelTests(unittest.TestCase):
    """The retained job-log channel carries the explicit failure diagnostics."""

    def _summary(self):
        return {
            "status": "COMPLETED",
            "results": [
                {
                    "case_id": "pilot-a-01",
                    "arm": "WITH_SKILL",
                    "run_index": 1,
                    "result_state": "JUDGE_ERROR",
                    "reason_code": "JUDGE_PARSE_ERROR",
                    "judge": {
                        "stop_reason": "completed",
                        "judge_error": {
                            "kind": "JUDGE_PARSE_ERROR",
                            "parse_reason": "MALFORMED_JSON",
                            "finish_reason": "completed",
                            "output_sha256": sha256_hex_text(MALFORMED_RAW),
                            "output_chars": len(MALFORMED_RAW),
                            "output_shape": "NOT_JSON",
                            "observed_keys": [],
                            "output_recorded": False,
                        },
                    },
                }
            ],
        }

    def test_diagnostics_extract_the_explicit_classification_and_finish_reason(self):
        from tools.behavioral_eval_runner.cli import _judge_failure_diagnostics

        diagnostics = _judge_failure_diagnostics(self._summary())
        self.assertEqual(len(diagnostics), 1)
        item = diagnostics[0]
        self.assertEqual(item["kind"], "JUDGE_PARSE_ERROR")
        self.assertEqual(item["parse_reason"], "MALFORMED_JSON")
        self.assertEqual(item["finish_reason"], "completed")
        self.assertIs(item["output_recorded"], False)
        self.assertEqual(item["reason_code"], "JUDGE_PARSE_ERROR")

    def test_stderr_channel_retains_the_finish_reason_and_no_raw_output(self):
        import contextlib
        import io

        from tools.behavioral_eval_runner.cli import (
            _emit_judge_failure_diagnostics,
        )

        stream = io.StringIO()
        with contextlib.redirect_stderr(stream):
            _emit_judge_failure_diagnostics(self._summary())
        line = stream.getvalue().strip()
        self.assertTrue(line)
        payload = json.loads(line)
        self.assertEqual(payload["event"], "judge_failure_diagnostics")
        self.assertEqual(
            payload["judge_errors"][0]["kind"], "JUDGE_PARSE_ERROR"
        )
        self.assertEqual(
            payload["judge_errors"][0]["finish_reason"], "completed"
        )
        self.assertNotIn(MALFORMED_RAW, line)

    def test_no_diagnostics_line_for_a_passing_run(self):
        import contextlib
        import io

        from tools.behavioral_eval_runner.cli import (
            _emit_judge_failure_diagnostics,
        )

        stream = io.StringIO()
        with contextlib.redirect_stderr(stream):
            _emit_judge_failure_diagnostics(
                {
                    "status": "COMPLETED",
                    "results": [
                        {"result_state": "PASS", "judge": {"verdict": {}}}
                    ],
                }
            )
        self.assertEqual(stream.getvalue(), "")


class FailClosedEndToEndTests(unittest.TestCase):
    """The packaged live smoke path: a judge failure is explicit, never null."""

    ENVIRON = {
        "ANTHROPIC_API_KEY": helpers.FAKE_ANTHROPIC_KEY,
        "OPENAI_API_KEY": helpers.FAKE_OPENAI_KEY,
    }

    def _smoke_paths(self, tmp: str):
        with open(helpers.SMOKE_CONFIG, encoding="utf-8") as handle:
            config = json.load(handle)
        return helpers.make_paths(
            tmp,
            config=config,
            gate=helpers.gate_payload(fact_origin="REAL_HOST"),
            run_id="judge-contract-smoke",
        )

    def _run_smoke(self, tmp: str, judge_transport):
        from tools.behavioral_eval_runner.live.pipeline import live_run

        paths = self._smoke_paths(tmp)
        result = live_run(
            paths,
            environ=self.ENVIRON,
            subject_transport_factory=lambda credentials: helpers.mock_subject_transport(),
            judge_transport_factory=lambda credentials: judge_transport,
            smoke=True,
        )
        return paths, result

    @staticmethod
    def _malformed_judge_transport() -> MockTransport:
        def handler(request):
            return ProviderResponse(
                response_id="mock-judge",
                served_model=request.model,
                text=MALFORMED_RAW,
                usage=ProviderUsage(len(request.user_content), 64),
                stop_reason="completed",
            )

        return MockTransport(handler, name="mock-malformed-judge")

    def test_smoke_run_with_a_malformed_judge_records_judge_parse_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths, result = self._run_smoke(tmp, self._malformed_judge_transport())
            self.assertEqual(result["status"], "COMPLETED")
            self.assertEqual(result["planned_calls"], 2)
            self.assertEqual(result["dispatched_calls"], 2)
            self.assertEqual(result["results_by_state"], {"JUDGE_ERROR": 1})
            record = result["results"][0]
            self.assertEqual(record["result_state"], "JUDGE_ERROR")
            self.assertEqual(record["reason_code"], "JUDGE_PARSE_ERROR")
            self.assertEqual(record["citability"], "INJECTED_TRANSPORT_NOT_CITABLE")
            judge = record["judge"]
            self.assertEqual(judge["stop_reason"], "completed")
            self.assertEqual(judge["judge_error"]["kind"], "JUDGE_PARSE_ERROR")
            self.assertEqual(judge["judge_error"]["parse_reason"], "MALFORMED_JSON")
            self.assertEqual(judge["judge_error"]["finish_reason"], "completed")
            self.assertIs(judge["judge_error"]["output_recorded"], False)
            smoke = result["smoke"]
            self.assertEqual(smoke["judge_finish_reasons"], ["completed"])
            self.assertEqual(
                smoke["judge_parse_errors"][0]["kind"], "JUDGE_PARSE_ERROR"
            )
            for value in ("end_turn", "stop", "completed"):
                self.assertIn(value, smoke["complete_stop_reasons"])
            # The retained evidence carries the explicit classification and the
            # raw finish reason, but not the raw judge output.
            evidence = _evidence_bytes(paths.evidence_root)
            self.assertIn(b'"JUDGE_PARSE_ERROR"', evidence)
            self.assertIn(b'"finish_reason":"completed"', evidence)
            self.assertNotIn(MALFORMED_RAW.encode("utf-8"), evidence)
            with open(
                os.path.join(paths.evidence_root, "final_report.json"),
                encoding="utf-8",
            ) as handle:
                final_report = json.load(handle)
            self.assertEqual(
                final_report["smoke"]["judge_parse_errors"][0]["kind"],
                "JUDGE_PARSE_ERROR",
            )

    def test_smoke_run_with_the_fixed_shape_records_a_rule_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths, result = self._run_smoke(tmp, helpers.mock_judge_transport())
            self.assertEqual(result["results_by_state"], {"PASS": 1})
            record = result["results"][0]
            self.assertEqual(record["result_state"], "PASS")
            self.assertIsNone(record["reason_code"])
            self.assertEqual(record["judge"]["verdict"]["verdict"], "PASS")
            self.assertEqual(record["judge"]["stop_reason"], "end_turn")
            self.assertEqual(result["smoke"]["judge_parse_errors"], [])
            self.assertTrue(result["evidence"]["verified"])


if __name__ == "__main__":
    unittest.main()

