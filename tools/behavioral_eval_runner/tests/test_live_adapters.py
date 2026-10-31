"""Gated live adapters: strict pinning, credentials, judge guard (offline).

No network call is made. Every transport is the mock transport and every
credential value is a fake literal that is not a provider key.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest

from tools.behavioral_eval_runner.canonical import canonical_json, sha256_hex_text
from tools.behavioral_eval_runner.live.config import SUBJECT_PINS, OwnerAllowlist
from tools.behavioral_eval_runner.live.credentials import (
    CREDENTIAL_ENV_VARS,
    missing_credential_env_vars,
    resolve_credentials,
)
from tools.behavioral_eval_runner.live.dataset import load_cases
from tools.behavioral_eval_runner.live.errors import (
    JudgeRubricSourceError,
    JudgeVendorGuardError,
    MissingCredentialError,
    ModelPinMismatchError,
)
from tools.behavioral_eval_runner.live.judge_adapter import (
    JudgeAdapter,
    parse_live_verdict,
)
from tools.behavioral_eval_runner.live.mock_transport import MockTransport
from tools.behavioral_eval_runner.live.providers import JUDGE_PINS
from tools.behavioral_eval_runner.live.subject import SubjectAdapter
from tools.behavioral_eval_runner.live.transport import (
    ProviderResponse,
    ProviderUsage,
)
from tools.behavioral_eval_runner.tests import live_helpers as helpers

PACKAGE_ROOT = helpers.PACKAGE_ROOT
LIVE_ROOT = os.path.join(PACKAGE_ROOT, "live")


def _response(model: str, text: str = "ok", *, served: str | None = None):
    return ProviderResponse(
        response_id="r-1",
        served_model=served if served is not None else model,
        text=text,
        usage=ProviderUsage(10, 5),
        stop_reason="end_turn",
    )


def _fixed_transport(model: str, *, served: str | None = None, text: str = "ok"):
    return MockTransport(lambda request: _response(model, text, served=served))


class SubjectPinningTests(unittest.TestCase):
    def _adapter(self, vendor: str, transport) -> SubjectAdapter:
        pin = SUBJECT_PINS[vendor]
        return SubjectAdapter(
            pin, transport, max_output_tokens=64, timeout_seconds=30
        )

    def test_request_carries_the_exact_pin_and_served_model_is_recorded(self):
        transport = _fixed_transport("claude-sonnet-5-5", text="fine")
        adapter = self._adapter("anthropic", transport)
        request = adapter.build_request(
            request_id="case:WITH_SKILL:run-1:subject:anthropic",
            prompt="hello",
            arm="WITH_SKILL",
            skill_instructions="owner approval rule",
        )
        self.assertEqual(request.model, "claude-sonnet-5-5")
        self.assertEqual(request.vendor, "anthropic")
        result, text = adapter.dispatch(request)
        self.assertEqual(text, "fine")
        self.assertEqual(result.served_model, "claude-sonnet-5-5")
        self.assertEqual(result.requested_model, "claude-sonnet-5-5")
        self.assertEqual(result.response_sha256, sha256_hex_text("fine"))
        self.assertNotIn("text", result.to_record())

    def test_served_model_mismatch_halts_with_structured_error_and_no_retry(self):
        transport = _fixed_transport(
            "claude-sonnet-5-5", served="claude-sonnet-5-5-2027-preview"
        )
        adapter = self._adapter("anthropic", transport)
        request = adapter.build_request(
            request_id="case:WITH_SKILL:run-1:subject:anthropic",
            prompt="hello",
            arm="WITH_SKILL",
            skill_instructions="owner approval rule",
        )
        with self.assertRaises(ModelPinMismatchError) as caught:
            adapter.dispatch(request)
        error = caught.exception
        self.assertEqual(error.reason_code, "MODEL_PIN_MISMATCH")
        self.assertTrue(error.context["halt"])
        self.assertEqual(error.context["served_model"], "claude-sonnet-5-5-2027-preview")
        self.assertEqual(error.context["requested_model"], "claude-sonnet-5-5")
        self.assertEqual(transport.call_count, 1)

    def test_empty_served_model_is_a_pin_mismatch_halt(self):
        transport = MockTransport(
            lambda request: ProviderResponse(
                response_id="r",
                served_model="",
                text="x",
                usage=ProviderUsage(1, 1),
                stop_reason="end_turn",
            )
        )
        adapter = self._adapter("openai", transport)
        request = adapter.build_request(
            request_id="rid", prompt="hello", arm="BASELINE"
        )
        with self.assertRaises(ModelPinMismatchError) as caught:
            adapter.dispatch(request)
        self.assertEqual(caught.exception.reason_code, "MODEL_PIN_MISMATCH")
        self.assertEqual(caught.exception.context["served_model"], "")


class CredentialTests(unittest.TestCase):
    def test_missing_key_fails_closed_and_names_only_the_variable(self):
        environ = {"ANTHROPIC_API_KEY": helpers.FAKE_ANTHROPIC_KEY}
        with self.assertRaises(MissingCredentialError) as caught:
            resolve_credentials(["anthropic", "openai"], environ)
        error = caught.exception
        self.assertEqual(error.reason_code, "CREDENTIAL_MISSING")
        self.assertEqual(error.context["missing_env_vars"], ["OPENAI_API_KEY"])
        self.assertNotIn(helpers.FAKE_ANTHROPIC_KEY, str(error))

    def test_credential_is_never_serialized(self):
        credentials = resolve_credentials(
            ["anthropic"],
            {"ANTHROPIC_API_KEY": helpers.FAKE_ANTHROPIC_KEY},
        )
        credential = credentials.for_vendor("anthropic")
        self.assertNotIn(helpers.FAKE_ANTHROPIC_KEY, repr(credentials))
        self.assertNotIn(helpers.FAKE_ANTHROPIC_KEY, repr(credential))
        self.assertEqual(credential.reveal(), helpers.FAKE_ANTHROPIC_KEY)
        self.assertEqual(
            credential.presence_record(),
            {"vendor": "anthropic", "env_var": "ANTHROPIC_API_KEY", "present": True},
        )

    def test_env_var_names_come_from_the_single_provider_module(self):
        self.assertEqual(
            CREDENTIAL_ENV_VARS,
            {"anthropic": "ANTHROPIC_API_KEY", "openai": "OPENAI_API_KEY"},
        )
        self.assertEqual(
            missing_credential_env_vars(["anthropic", "openai"], {}),
            ["ANTHROPIC_API_KEY", "OPENAI_API_KEY"],
        )


class JudgeGuardTests(unittest.TestCase):
    def _case(self):
        return load_cases(helpers.CASES_ROOT)[0]

    def _subject_result(self):
        from tools.behavioral_eval_runner.live.subject import SubjectResult

        return SubjectResult(
            request_id="rid",
            response_id="resp-1",
            vendor="anthropic",
            requested_model="claude-sonnet-5-5",
            served_model="claude-sonnet-5-5",
            response_sha256=sha256_hex_text("answer"),
            response_chars=6,
            usage=ProviderUsage(3, 2),
            stop_reason="end_turn",
        )

    def test_same_vendor_judge_is_refused(self):
        allowlist = OwnerAllowlist(
            (("anthropic", "claude-sonnet-5-5"), ("openai", "gpt-6-astra"))
        )
        adapter = JudgeAdapter(
            SUBJECT_PINS["anthropic"],
            allowlist,
            _fixed_transport("claude-sonnet-5-5"),
            max_output_tokens=64,
            timeout_seconds=30,
        )
        with self.assertRaises(JudgeVendorGuardError) as caught:
            adapter.guard("anthropic")
        self.assertEqual(caught.exception.reason_code, "JUDGE_VENDOR_GUARD")

    def test_allowlist_mismatch_is_refused(self):
        adapter = JudgeAdapter(
            JUDGE_PINS[("anthropic", "claude-sonnet-5-5")],
            OwnerAllowlist(()),
            _fixed_transport("gpt-6-astra"),
            max_output_tokens=64,
            timeout_seconds=30,
        )
        with self.assertRaises(JudgeVendorGuardError):
            adapter.guard("anthropic")

    def test_judge_model_pin_mismatch_halts(self):
        adapter = JudgeAdapter(
            JUDGE_PINS[("anthropic", "claude-sonnet-5-5")],
            OwnerAllowlist((("openai", "gpt-6-astra"),)),
            _fixed_transport("gpt-6-astra", served="gpt-6-astra-mini"),
            max_output_tokens=64,
            timeout_seconds=30,
        )
        case = self._case()
        subject = self._subject_result()
        request = adapter.build_request(
            request_id="jid",
            case=case,
            arm="WITH_SKILL",
            subject_vendor="anthropic",
            subject_result=subject,
            subject_text="answer",
        )
        with self.assertRaises(ModelPinMismatchError) as caught:
            adapter.dispatch(request, case=case, subject_text="answer")
        self.assertEqual(caught.exception.context["role"], "judge")

    def test_rubric_must_match_committed_hash(self):
        case = self._case()
        import dataclasses

        broken = dataclasses.replace(
            case, rubric={"rubric_id": "tampered"}
        )
        adapter = JudgeAdapter(
            JUDGE_PINS[("anthropic", "claude-sonnet-5-5")],
            OwnerAllowlist((("openai", "gpt-6-astra"),)),
            _fixed_transport("gpt-6-astra"),
            max_output_tokens=64,
            timeout_seconds=30,
        )
        with self.assertRaises(JudgeRubricSourceError):
            adapter.build_request(
                request_id="jid",
                case=broken,
                arm="WITH_SKILL",
                subject_vendor="anthropic",
                subject_result=self._subject_result(),
                subject_text="answer",
            )

    def test_verdict_parsing_fails_closed(self):
        rubric = "a" * 64
        response = "b" * 64
        valid = {
            "verdict": "PASS",
            "reason_code": "MEETS_RUBRIC",
            "failure_mode": None,
            "rubric_sha256": rubric,
            "response_sha256": response,
            "judge_model": "gpt-6-astra",
            "evidence_refs": ["response"],
        }
        verdict, error = parse_live_verdict(
            canonical_json(valid),
            rubric_sha256=rubric,
            response_sha256=response,
            judge_model="gpt-6-astra",
        )
        self.assertIsNone(error)
        self.assertEqual(verdict.verdict.value, "PASS")

        tampered = dict(valid, rubric_sha256="c" * 64)
        verdict, error = parse_live_verdict(
            canonical_json(tampered),
            rubric_sha256=rubric,
            response_sha256=response,
            judge_model="gpt-6-astra",
        )
        self.assertIsNone(verdict)
        self.assertEqual(error, "RUBRIC_MISMATCH")

        swapped = dict(valid, response_sha256="d" * 64)
        _, error = parse_live_verdict(
            canonical_json(swapped),
            rubric_sha256=rubric,
            response_sha256=response,
            judge_model="gpt-6-astra",
        )
        self.assertEqual(error, "CONTRADICTORY_EVIDENCE")

        _, error = parse_live_verdict(
            "not json", rubric_sha256=rubric, response_sha256=response,
            judge_model="gpt-6-astra",
        )
        self.assertEqual(error, "MALFORMED_JSON")

        prose = dict(valid, extra="prose")
        _, error = parse_live_verdict(
            canonical_json(prose), rubric_sha256=rubric, response_sha256=response,
            judge_model="gpt-6-astra",
        )
        self.assertEqual(error, "SCHEMA_INVALID")


class SkillArmTests(unittest.TestCase):
    def test_with_skill_loads_committed_instructions_and_baseline_does_not(self):
        transport = _fixed_transport("claude-sonnet-5-5")
        adapter = SubjectAdapter(
            SUBJECT_PINS["anthropic"], transport, max_output_tokens=64, timeout_seconds=30
        )
        with_skill = adapter.build_request(
            request_id="c:WITH_SKILL:run-1:subject:anthropic",
            prompt="hello",
            arm="WITH_SKILL",
            skill_instructions="OWNER APPROVAL RULE TEXT",
        )
        baseline = adapter.build_request(
            request_id="c:BASELINE:run-1:subject:anthropic",
            prompt="hello",
            arm="BASELINE",
        )
        self.assertIn("OWNER APPROVAL RULE TEXT", with_skill.system)
        self.assertNotIn("OWNER APPROVAL RULE TEXT", baseline.system)
        with self.assertRaises(ValueError):
            adapter.build_request(
                request_id="c:WITH_SKILL:run-2:subject:anthropic",
                prompt="hello",
                arm="WITH_SKILL",
            )


class MalformedJudgeOutputTests(unittest.TestCase):
    def test_unhashable_enum_values_fail_closed(self):
        rubric = "a" * 64
        response = "b" * 64
        for bad in (
            {"verdict": []},
            {"reason_code": []},
            {"failure_mode": []},
            {"verdict": 3},
            {"rubric_sha256": None},
        ):
            payload = {
                "verdict": "PASS",
                "reason_code": "MEETS_RUBRIC",
                "failure_mode": None,
                "rubric_sha256": rubric,
                "response_sha256": response,
                "judge_model": "gpt-6-astra",
                "evidence_refs": ["response"],
            }
            payload.update(bad)
            verdict, error = parse_live_verdict(
                canonical_json(payload),
                rubric_sha256=rubric,
                response_sha256=response,
                judge_model="gpt-6-astra",
            )
            self.assertIsNone(verdict, bad)
            self.assertEqual(error, "SCHEMA_INVALID", bad)

    def test_judge_envelope_is_blind_to_arm_and_subject_vendor(self):
        from tools.behavioral_eval_runner.live.judge_adapter import JudgeAdapter
        from tools.behavioral_eval_runner.live.providers import JUDGE_PINS
        from tools.behavioral_eval_runner.live.subject import SubjectResult

        case = load_cases(helpers.CASES_ROOT)[0]
        subject = SubjectResult(
            request_id="rid",
            response_id="resp",
            vendor="anthropic",
            requested_model="claude-sonnet-5-5",
            served_model="claude-sonnet-5-5",
            response_sha256=sha256_hex_text("answer"),
            response_chars=6,
            usage=ProviderUsage(3, 2),
            stop_reason="end_turn",
        )
        adapter = JudgeAdapter(
            JUDGE_PINS[("anthropic", "claude-sonnet-5-5")],
            OwnerAllowlist((("openai", "gpt-6-astra"),)),
            _fixed_transport("gpt-6-astra"),
            max_output_tokens=64,
            timeout_seconds=30,
        )
        request = adapter.build_request(
            request_id="jid",
            case=case,
            arm="WITH_SKILL",
            subject_vendor="anthropic",
            subject_result=subject,
            subject_text="answer",
        )
        payload = json.loads(request.user_content)
        self.assertNotIn("arm", payload)
        self.assertNotIn("subject_vendor", payload)


class ProviderContractTests(unittest.TestCase):
    def test_only_allowlisted_complete_statuses_are_graded(self):
        from tools.behavioral_eval_runner.live.errors import ProviderTransportError
        from tools.behavioral_eval_runner.live.providers import ensure_complete_response

        # The complete-status allowlist is vendor-INDEPENDENT (one package
        # source of truth); the value the provider returned is recorded raw and
        # never normalized away. "end_turn"/"stop_sequence" are the messages-API
        # vocabulary, "completed" the responses-API status, "stop" the
        # chat-completions-API finish_reason.
        for status in ("end_turn", "stop_sequence", "completed"):
            ensure_complete_response(status, vendor="anthropic")
        for status in ("stop", "completed"):
            ensure_complete_response(status, vendor="openai")
        for status in ("max_tokens", "length", "content_filter", "failed",
                       "cancelled", "incomplete", "", "UNKNOWN"):
            with self.assertRaises(ProviderTransportError):
                ensure_complete_response(status, vendor="openai")

    def test_usage_telemetry_is_required_and_typed(self):
        from tools.behavioral_eval_runner.live.errors import ProviderTransportError
        from tools.behavioral_eval_runner.live.providers import extract_usage
        from tools.behavioral_eval_runner.live.transport import ProviderUsage

        self.assertEqual(
            extract_usage(ProviderUsage(3, 4), vendor="anthropic").to_dict(),
            {"input_tokens": 3, "output_tokens": 4},
        )
        class NoUsage:
            input_tokens = 1
        class BoolUsage:
            input_tokens = True
            output_tokens = 1
        for usage in (None, NoUsage(), BoolUsage()):
            with self.assertRaises(ProviderTransportError):
                extract_usage(usage, vendor="openai")

    def test_transport_environment_overrides_are_refused(self):
        from tools.behavioral_eval_runner.live.errors import ProviderTransportError
        from tools.behavioral_eval_runner.live.providers import (
            detect_transport_env_violations,
            require_clean_transport_environment,
        )

        self.assertEqual(detect_transport_env_violations({}), [])
        self.assertEqual(
            detect_transport_env_violations({"OPENAI_BASE_URL": "https://elsewhere"}),
            ["OPENAI_BASE_URL"],
        )
        with self.assertRaises(ProviderTransportError):
            require_clean_transport_environment({"HTTPS_PROXY": "http://proxy"})
        require_clean_transport_environment({"OPENAI_API_KEY": "present"})

    def test_unknown_arm_is_rejected(self):
        adapter = SubjectAdapter(
            SUBJECT_PINS["anthropic"],
            _fixed_transport("claude-sonnet-5-5"),
            max_output_tokens=64,
            timeout_seconds=30,
        )
        with self.assertRaises(ValueError):
            adapter.build_request(request_id="r", prompt="p", arm="SOMETHING_ELSE")

    def test_judge_adapter_rejects_a_non_route_pin(self):
        from tools.behavioral_eval_runner.live.config import ModelPin
        from tools.behavioral_eval_runner.live.judge_adapter import JudgeAdapter

        with self.assertRaises(ModelPinMismatchError):
            JudgeAdapter(
                ModelPin("openai", "not-a-route", "OPENAI_API_KEY", 1, 1),
                OwnerAllowlist((("openai", "not-a-route"),)),
                _fixed_transport("not-a-route"),
                max_output_tokens=64,
                timeout_seconds=30,
            )


class ProviderConfinementTests(unittest.TestCase):
    def test_only_the_provider_module_names_either_provider(self):
        # Both vendor SDK names, and the dotted API host form for Anthropic,
        # are confined to the single provider-naming module.
        fragments = ("openai", "import anthropic", "from anthropic", "api.anthropic")
        offenders = []
        for directory, dirs, files in os.walk(LIVE_ROOT):
            dirs[:] = [name for name in dirs if name not in ("cases",)]
            for name in files:
                if not name.endswith(".py"):
                    continue
                path = os.path.join(directory, name)
                relative = os.path.relpath(path, PACKAGE_ROOT).replace("\\", "/")
                with open(path, encoding="utf-8") as handle:
                    lowered = handle.read().lower()
                if relative == "live/providers.py":
                    continue
                for fragment in fragments:
                    if fragment in lowered:
                        offenders.append(f"{relative}: {fragment}")
        self.assertEqual(offenders, [])

    def test_importing_the_live_package_loads_no_network_or_sdk_module(self):
        probe = (
            "import sys\n"
            "import tools.behavioral_eval_runner.live.pipeline\n"
            "import tools.behavioral_eval_runner.live.providers\n"
            "import tools.behavioral_eval_runner.cli\n"
            "loaded = [m for m in ('socket', 'urllib', 'urllib.request',"
            " 'http.client', 'ssl', 'anthropic', 'openai', 'httpx')"
            " if m in sys.modules]\n"
            "print(','.join(loaded) if loaded else 'CLEAN')\n"
        )
        completed = subprocess.run(
            [sys.executable, "-c", probe],
            shell=False,
            capture_output=True,
            timeout=120,
            cwd=helpers.REPO_ROOT,
        )
        self.assertEqual(
            completed.returncode, 0, completed.stderr.decode("utf-8", "replace")
        )
        self.assertEqual(
            completed.stdout.decode("utf-8", "replace").strip(), "CLEAN"
        )


if __name__ == "__main__":
    unittest.main()
