"""WP-2B-3 calibration transport contract (BER-DEC-008 decisions 3, 4, 29, 31).

Offline only: no test in this module performs a network call. SDK-dependent
assertions run only when the pinned SDK is importable (the isolated WP-2B-3
venv); they are skipped, never faked, elsewhere.
"""

from __future__ import annotations

import unittest

from tools.behavioral_eval_runner import CALIBRATION_SCHEMA_VERSION
from tools.behavioral_eval_runner.judge import calibration_transport as ct
from tools.behavioral_eval_runner.judge.calibration_credential import (
    CREDENTIAL_ENV_VAR,
    CalibrationCredential,
    consume_process_scoped_credential,
)
from tools.behavioral_eval_runner.judge.calibration_errors import (
    CalibrationReservationDenied,
    CalibrationStopError,
    CalibrationStopReason,
)

try:  # the pinned SDK exists only inside the isolated WP-2B-3 venv
    import openai as _openai  # noqa: F401

    _SDK_AVAILABLE = True
except ImportError:
    _SDK_AVAILABLE = False

DUMMY_SECRET = "dummy-sentinel-not-a-real-credential"


class TestAuthorizedConstants(unittest.TestCase):
    def test_pinned_authorization_terms(self) -> None:
        self.assertEqual(ct.AUTHORIZED_MODEL_SNAPSHOT, "gpt-5.5-2026-04-23")
        self.assertEqual(ct.AUTHORIZED_BASE_URL, "https://api.openai.com/v1")
        self.assertEqual(ct.AUTHORIZED_EGRESS_HOST, "api.openai.com")
        self.assertEqual(ct.AUTHORIZED_EGRESS_PORT, 443)
        self.assertEqual(ct.AUTHORIZED_SDK_VERSION, "3.0.0")
        self.assertEqual(
            ct.AUTHORIZED_SDK_WHEEL_SHA256,
            "8d32ac3a6647a66910d6cb8a64f0fa5a6c823604b6e82db83d9d055c6709bd51",
        )
        self.assertEqual(
            ct.AUTHORIZED_SDK_SDIST_SHA256,
            "ffd00ef1678d70957e1f1ed98d5bfcf1d661f41ea4482f22e7d0144a66435a49",
        )
        self.assertEqual(ct.CONNECT_TIMEOUT_SECONDS, 15.0)
        self.assertEqual(ct.TOTAL_REQUEST_TIMEOUT_SECONDS, 300.0)
        self.assertEqual(ct.SDK_MAX_RETRIES, 0)
        self.assertEqual(ct.REASONING_EFFORT, "medium")
        self.assertEqual(ct.MAX_INPUT_TOKENS_PER_JUDGMENT, 8000)
        self.assertEqual(ct.DEV_MAX_OUTPUT_TOKENS, 25000)
        self.assertEqual(ct.HOLDOUT_MAX_OUTPUT_TOKENS_RANGE, (8192, 25000))
        self.assertEqual(
            ct.AUTHORIZED_METADATA_ENDPOINT,
            "GET /v1/models/gpt-5.5-2026-04-23",
        )


class TestProxyAndTlsEnvFailClosed(unittest.TestCase):
    def test_clean_environment_has_no_violations(self) -> None:
        self.assertEqual(ct.detect_transport_env_violations({}), [])

    def test_every_proxy_variable_is_detected(self) -> None:
        for name in (
            "HTTP_PROXY",
            "HTTPS_PROXY",
            "ALL_PROXY",
            "http_proxy",
            "https_proxy",
            "all_proxy",
            "OPENAI_PROXY",
        ):
            violations = ct.detect_transport_env_violations({name: "http://proxy:1"})
            self.assertTrue(violations, name)

    def test_tls_override_variables_are_detected(self) -> None:
        for name in ("SSL_CERT_FILE", "SSL_CERT_DIR", "REQUESTS_CA_BUNDLE",
                     "CURL_CA_BUNDLE"):
            violations = ct.detect_transport_env_violations({name: r"C:\x"})
            self.assertTrue(violations, name)

    def test_base_url_env_override_is_detected(self) -> None:
        violations = ct.detect_transport_env_violations(
            {"OPENAI_BASE_URL": "https://evil.example"}
        )
        self.assertTrue(violations)

    def test_unrelated_variables_are_ignored(self) -> None:
        self.assertEqual(
            ct.detect_transport_env_violations({"PATH": "x", "TEMP": "y"}), []
        )

    def test_build_client_fails_closed_on_proxy_env(self) -> None:
        credential = CalibrationCredential(DUMMY_SECRET)
        with self.assertRaises(CalibrationStopError) as ctx:
            ct.build_judge_client(
                credential, environ={"HTTPS_PROXY": "http://proxy:1"}
            )
        self.assertIs(
            ctx.exception.stop_reason, CalibrationStopReason.PROXY_ENV_PRESENT
        )


class TestCredentialBoundary(unittest.TestCase):
    def test_credential_repr_and_str_are_redacted(self) -> None:
        credential = CalibrationCredential(DUMMY_SECRET)
        self.assertNotIn(DUMMY_SECRET, repr(credential))
        self.assertNotIn(DUMMY_SECRET, str(credential))
        self.assertIn("REDACTED", repr(credential))

    def test_consume_reads_and_removes_the_process_variable(self) -> None:
        environ = {CREDENTIAL_ENV_VAR: DUMMY_SECRET, "OTHER": "keep"}
        credential = consume_process_scoped_credential(environ)
        self.assertEqual(credential.reveal_for_transport_use_only(), DUMMY_SECRET)
        self.assertNotIn(CREDENTIAL_ENV_VAR, environ)  # consume-once
        self.assertEqual(environ["OTHER"], "keep")

    def test_missing_credential_is_a_stop_condition(self) -> None:
        with self.assertRaises(CalibrationStopError) as ctx:
            consume_process_scoped_credential({})
        self.assertIs(
            ctx.exception.stop_reason, CalibrationStopReason.CREDENTIAL_MISSING
        )

    def test_presence_check_never_reveals_the_value(self) -> None:
        present, detail = ct.credential_presence_check(
            {CREDENTIAL_ENV_VAR: DUMMY_SECRET}
        )
        self.assertTrue(present)
        self.assertNotIn(DUMMY_SECRET, detail)
        absent, _ = ct.credential_presence_check({})
        self.assertFalse(absent)


class TestClosedRequestKwargs(unittest.TestCase):
    def _kwargs(self) -> dict:
        return ct.build_responses_request_kwargs(
            instructions="POLICY", input_text="ENVELOPE",
            max_output_tokens=ct.DEV_MAX_OUTPUT_TOKENS,
        )

    def test_exact_closed_key_set(self) -> None:
        kwargs = self._kwargs()
        self.assertEqual(set(kwargs), set(ct.REQUIRED_REQUEST_KEYS))

    def test_request_settings_closure(self) -> None:
        kwargs = self._kwargs()
        self.assertEqual(kwargs["model"], ct.AUTHORIZED_MODEL_SNAPSHOT)
        self.assertIs(kwargs["store"], False)
        self.assertIs(kwargs["background"], False)
        self.assertEqual(kwargs["reasoning"], {"effort": "medium"})
        self.assertEqual(kwargs["max_output_tokens"], 25000)
        fmt = kwargs["text"]["format"]
        self.assertEqual(fmt["type"], "json_schema")
        self.assertIs(fmt["strict"], True)
        # No tools / functions / search / code / conversation state of any kind.
        for forbidden in ct.FORBIDDEN_REQUEST_KEYS:
            self.assertNotIn(forbidden, kwargs)

    def test_forbidden_keys_cover_every_tool_and_state_channel(self) -> None:
        for name in (
            "tools", "tool_choice", "parallel_tool_calls", "max_tool_calls",
            "previous_response_id", "conversation", "prompt", "metadata",
            "temperature", "top_p", "stream", "include", "service_tier",
            "truncation", "moderation", "safety_identifier",
            "prompt_cache_key", "prompt_cache_retention", "context_management",
            "top_logprobs", "user", "stream_options", "prompt_cache_options",
            "instructions_override",
        ):
            if name == "instructions_override":
                continue  # not a real SDK parameter; guard the loop shape
            self.assertIn(name, ct.FORBIDDEN_REQUEST_KEYS, name)

    def test_validate_rejects_extra_or_missing_or_mutated_keys(self) -> None:
        good = self._kwargs()
        ct.validate_request_kwargs(good)
        extra = dict(good)
        extra["tools"] = []
        with self.assertRaises(CalibrationStopError):
            ct.validate_request_kwargs(extra)
        missing = dict(good)
        del missing["store"]
        with self.assertRaises(CalibrationStopError):
            ct.validate_request_kwargs(missing)
        mutated = dict(good)
        mutated["store"] = True
        with self.assertRaises(CalibrationStopError):
            ct.validate_request_kwargs(mutated)
        wrong_model = dict(good)
        wrong_model["model"] = "gpt-5.6-sol"
        with self.assertRaises(CalibrationStopError):
            ct.validate_request_kwargs(wrong_model)

    def test_development_output_cap_is_enforced(self) -> None:
        with self.assertRaises(CalibrationReservationDenied):
            ct.build_responses_request_kwargs(
                instructions="P", input_text="E", max_output_tokens=25001
            )
        with self.assertRaises(CalibrationReservationDenied):
            ct.build_responses_request_kwargs(
                instructions="P", input_text="E", max_output_tokens=0
            )


class TestInputTokenBudget(unittest.TestCase):
    def test_estimator_is_conservative_and_deterministic(self) -> None:
        self.assertEqual(ct.estimate_input_tokens(""), 0)
        self.assertEqual(ct.estimate_input_tokens("abc"), 1)
        self.assertEqual(ct.estimate_input_tokens("a" * 30), 10)

    def test_budget_gate_blocks_oversized_input(self) -> None:
        small = "x" * 300
        ct.enforce_input_token_budget(small, "policy")
        oversized = "x" * (3 * 8001)
        with self.assertRaises(CalibrationReservationDenied):
            ct.enforce_input_token_budget(oversized, "policy")

    def test_budget_counts_instructions_and_input_together(self) -> None:
        half = "x" * (3 * 4001)
        with self.assertRaises(CalibrationReservationDenied):
            ct.enforce_input_token_budget(half, half)


class TestStructuredOutputSchema(unittest.TestCase):
    def test_schema_matches_the_verdict_contract(self) -> None:
        schema = ct.structured_verdict_output_schema()
        self.assertEqual(schema["type"], "object")
        self.assertIs(schema["additionalProperties"], False)
        from tools.behavioral_eval_runner.judge.verdict import StructuredVerdict

        expected_keys = set(StructuredVerdict._KEYS)
        self.assertEqual(set(schema["properties"]), expected_keys)
        self.assertEqual(set(schema["required"]), expected_keys)
        self.assertEqual(
            schema["properties"]["verdict"]["enum"], ["PASS", "FAIL", "ABSTAIN"]
        )
        self.assertEqual(
            schema["properties"]["schema_version"]["enum"], ["1.0.0-wp2b2"]
        )

    def test_schema_version_constant(self) -> None:
        self.assertEqual(CALIBRATION_SCHEMA_VERSION, "1.0.0-wp2b3")


@unittest.skipUnless(_SDK_AVAILABLE, "pinned OpenAI SDK not installed here")
class TestPinnedSdkClientConfiguration(unittest.TestCase):
    """Prove the CONFIGURED client owns zero SDK retries (BER-DEC-008 dec 21)."""

    def test_sdk_version_is_the_authorized_pin(self) -> None:
        ct.verify_sdk_version()

    def test_client_factory_configuration(self) -> None:
        credential = CalibrationCredential(DUMMY_SECRET)
        client = ct.build_judge_client(credential, environ={})
        self.assertEqual(client.max_retries, 0)  # zero SDK-owned retries
        self.assertEqual(str(client.base_url), "https://api.openai.com/v1/")
        timeout = client.timeout
        self.assertEqual(timeout.connect, 15.0)
        self.assertEqual(timeout.read, 300.0)

    def test_client_verification_rejects_nonzero_retries(self) -> None:
        credential = CalibrationCredential(DUMMY_SECRET)
        client = ct.build_judge_client(credential, environ={})
        client.max_retries = 2
        with self.assertRaises(CalibrationStopError) as ctx:
            ct.verify_client_invariants(client)
        self.assertIs(
            ctx.exception.stop_reason,
            CalibrationStopReason.SDK_RETRY_CONFIG_INVALID,
        )

    def test_client_verification_rejects_wrong_base_url(self) -> None:
        credential = CalibrationCredential(DUMMY_SECRET)
        client = ct.build_judge_client(credential, environ={})
        client.base_url = "https://evil.example/v1"
        with self.assertRaises(CalibrationStopError) as ctx:
            ct.verify_client_invariants(client)
        self.assertIs(
            ctx.exception.stop_reason, CalibrationStopReason.BASE_URL_MISMATCH
        )

    def test_inner_http_client_ignores_environment(self) -> None:
        credential = CalibrationCredential(DUMMY_SECRET)
        client = ct.build_judge_client(credential, environ={})
        inner = client._client
        self.assertFalse(getattr(inner, "_trust_env", True))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
