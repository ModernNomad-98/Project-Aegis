"""S3 serialized provider request/token-budget proof tests (offline).

Uses the real SubjectAdapter/JudgeAdapter request builders and the shared
runtime reservation/admission functions. No provider call, network, credential,
tokenizer dependency or paid action occurs. Actual wire framing and actual
tokenizer counts remain UNKNOWN; the documented safe upper bound is used.
"""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

from tools.behavioral_eval_runner.canonical import sha256_hex_text
from tools.behavioral_eval_runner.live.config import (
    MAX_JUDGE_REQUEST_BYTES,
    OWNER_PROVIDER_CAP_CENTS,
    SMOKE_CEILING_CENTS,
    OwnerAllowlist,
)
from tools.behavioral_eval_runner.live.cumulative import (
    actual_byte_reservation_cents,
    actual_byte_smoke_bounds,
    admit_paid_call,
)
from tools.behavioral_eval_runner.live.dataset import load_cases
from tools.behavioral_eval_runner.live.judge_adapter import JudgeAdapter
from tools.behavioral_eval_runner.live.providers import JUDGE_PINS, SUBJECT_PINS
from tools.behavioral_eval_runner.live.subject import SubjectAdapter, SubjectResult
from tools.behavioral_eval_runner.live.transport import ProviderUsage

OUTPUT_TOKENS = 16_384
FRAMING_OVERHEAD_BYTES = 1_024
SUBJECT_PIN = SUBJECT_PINS["anthropic"]
JUDGE_PIN = JUDGE_PINS[("anthropic", "claude-sonnet-5-5")]
ALLOWLIST = OwnerAllowlist((("openai", "gpt-6-astra"),))
HISTORICAL_LEDGER_CENTS = 222
HISTORICAL_SMOKE_CENTS = 18
HISTORICAL_TOTAL_CENTS = 240


def _subject_body_bytes(request) -> int:
    body = {
        "model": request.model,
        "max_tokens": request.max_output_tokens,
        "system": request.system,
        "messages": [{"role": "user", "content": request.user_content}],
    }
    return len(json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


def _judge_body_bytes(request) -> int:
    body = {
        "model": request.model,
        "max_output_tokens": request.max_output_tokens,
        "messages": [
            {"role": "system", "content": request.system},
            {"role": "user", "content": request.user_content},
        ],
    }
    return len(json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


def _cents(input_bytes: int, pin) -> int:
    return actual_byte_reservation_cents(
        input_bytes=input_bytes,
        input_cents_per_mtok=pin.input_cents_per_mtok,
        output_tokens=OUTPUT_TOKENS,
        output_cents_per_mtok=pin.output_cents_per_mtok,
    )


class S3SerializedBudgetProofTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        root = Path(__file__).resolve().parents[3]
        cls.cases = load_cases(str(root / "tools/behavioral_eval_runner/live/pilot-a/cases"))
        cls.result = SubjectResult(
            "r", "rid", "anthropic", SUBJECT_PIN.model, SUBJECT_PIN.model,
            sha256_hex_text("x"), 1, ProviderUsage(1, 1), "end_turn",
        )
        rows = []
        for case in cls.cases:
            for arm in ("WITH_SKILL", "BASELINE"):
                subject = SubjectAdapter(
                    SUBJECT_PIN, None,
                    max_output_tokens=OUTPUT_TOKENS, timeout_seconds=300,
                ).build_request(
                    request_id="s", prompt=case.prompt, arm=arm,
                    skill_instructions=case.skill_instructions if arm == "WITH_SKILL" else None,
                )
                judge = JudgeAdapter(
                    JUDGE_PIN, ALLOWLIST, None,
                    max_output_tokens=OUTPUT_TOKENS, timeout_seconds=300,
                ).build_request(
                    request_id="j", case=case, arm=arm, subject_vendor="anthropic",
                    subject_result=cls.result, subject_text="",
                )
                rows.append((_subject_body_bytes(subject), _judge_body_bytes(judge)))
        cls.rows = rows
        cls.subject_max = max(row[0] for row in rows)
        cls.judge_scaffold_max = max(row[1] for row in rows)
        cls.smoke_subject = _cents(rows[0][0] + FRAMING_OVERHEAD_BYTES, SUBJECT_PIN)
        cls.smoke_judge = _cents(MAX_JUDGE_REQUEST_BYTES + FRAMING_OVERHEAD_BYTES, JUDGE_PIN)
        cls.trial_subject = _cents(cls.subject_max + FRAMING_OVERHEAD_BYTES, SUBJECT_PIN)
        cls.trial_judge = cls.smoke_judge
        cls.trial_call = cls.trial_subject + cls.trial_judge
        cls.trial_total = 40 * cls.trial_call
        cls.full_total = 120 * cls.trial_call

    def test_standard_rates_and_caps_are_unchanged(self) -> None:
        self.assertEqual(SUBJECT_PIN.vendor, "anthropic")
        self.assertEqual(SUBJECT_PIN.price(), (200, 1000))
        self.assertEqual(JUDGE_PIN.vendor, "openai")
        self.assertEqual(JUDGE_PIN.price(), (1000, 5000))
        self.assertEqual(OUTPUT_TOKENS, 16_384)
        self.assertEqual(SMOKE_CEILING_CENTS, 200)
        self.assertEqual(OWNER_PROVIDER_CAP_CENTS, 12_000)
        self.assertEqual(MAX_JUDGE_REQUEST_BYTES, 90_000)
        # Only input/output billable categories are modelled; explicit standard
        # list price, no batch/cache/priority discount is applied.
        self.assertEqual(set(SUBJECT_PIN.to_dict()), {
            "vendor", "model", "credential_env_var",
            "input_cents_per_mtok", "output_cents_per_mtok",
        })

    def test_serialized_maxima_and_runtime_bounds(self) -> None:
        self.assertEqual(len(self.rows), 40)
        self.assertEqual(self.subject_max, 35_337)
        self.assertEqual(self.judge_scaffold_max, 5_556)
        smoke = actual_byte_smoke_bounds(
            subject_request_bytes=self.rows[0][0] + FRAMING_OVERHEAD_BYTES,
            max_judge_request_bytes=MAX_JUDGE_REQUEST_BYTES + FRAMING_OVERHEAD_BYTES,
            max_output_tokens=OUTPUT_TOKENS,
            subject_input_cents_per_mtok=SUBJECT_PIN.input_cents_per_mtok,
            subject_output_cents_per_mtok=SUBJECT_PIN.output_cents_per_mtok,
            judge_input_cents_per_mtok=JUDGE_PIN.input_cents_per_mtok,
            judge_output_cents_per_mtok=JUDGE_PIN.output_cents_per_mtok,
        )
        self.assertEqual(smoke["subject_cents"], 22)
        self.assertEqual(smoke["judge_cents"], 173)
        self.assertEqual(smoke["smoke_cents"], 195)
        self.assertLessEqual(smoke["smoke_cents"], SMOKE_CEILING_CENTS)
        self.assertLessEqual(HISTORICAL_TOTAL_CENTS + self.trial_total, OWNER_PROVIDER_CAP_CENTS)
        self.assertGreater(HISTORICAL_TOTAL_CENTS + self.full_total, OWNER_PROVIDER_CAP_CENTS)

    def test_full_pilot_rejected_pre_dispatch(self) -> None:
        historical_smoke = {"historical": HISTORICAL_SMOKE_CENTS}
        trial = admit_paid_call(
            ceiling_cents=OWNER_PROVIDER_CAP_CENTS,
            prior_ledger_spend_cents=HISTORICAL_LEDGER_CENTS,
            prior_smoke_spend_records=historical_smoke,
            reservation_cents=self.trial_total,
        )
        full = admit_paid_call(
            ceiling_cents=OWNER_PROVIDER_CAP_CENTS,
            prior_ledger_spend_cents=HISTORICAL_LEDGER_CENTS,
            prior_smoke_spend_records=historical_smoke,
            reservation_cents=self.full_total,
        )
        self.assertTrue(trial["admitted"])
        self.assertFalse(full["admitted"])
        self.assertLess(full["snapshot"]["remaining_cents"], 0)

    def test_safe_input_upper_bound_and_tokenizer_unavailable(self) -> None:
        self.assertIsNone(importlib.util.find_spec("tiktoken"))
        self.assertIsNone(importlib.util.find_spec("tokenizers"))
        # Documented safe upper bound: one input token cannot encode fewer than
        # one byte; output is capped exactly by max_output_tokens. Actual token
        # counts are UNKNOWN without a supported tokenizer.
        self.assertEqual(OUTPUT_TOKENS, 16_384)

    def _unicode_samples(self):
        return {
            "ascii": "plain ASCII text",
            "quotes": 'He said "hello" and \\ path',
            "newline": "line1\nline2\r\nline3\t",
            "c0": "\x00\x01\x02\x1f",
            "cjk": "漢字" * 100,
            "astral": "\U0001f600 \U0001f680 \U0001f4a9" * 100,
            "mixed": "A\"\n\x00漢\U0001f600" * 100,
        }

    def test_unicode_corpus_through_subject_then_judge(self) -> None:
        subject_adapter = SubjectAdapter(
            SUBJECT_PIN, None,
            max_output_tokens=OUTPUT_TOKENS, timeout_seconds=300,
        )
        judge_adapter = JudgeAdapter(
            JUDGE_PIN, ALLOWLIST, None,
            max_output_tokens=OUTPUT_TOKENS, timeout_seconds=300,
        )
        for label, sample in self._unicode_samples().items():
            subject_req = subject_adapter.build_request(
                request_id="u-" + label, prompt=sample, arm="WITH_SKILL",
                skill_instructions=self.cases[0].skill_instructions,
            )
            judge_req = judge_adapter.build_request(
                request_id="j-" + label, case=self.cases[0], arm="WITH_SKILL",
                subject_vendor="anthropic", subject_result=self.result,
                subject_text=sample,
            )
            self.assertGreater(_subject_body_bytes(subject_req), 0)
            self.assertGreater(_judge_body_bytes(judge_req), 0)
            raw = len(sample.encode("utf-8"))
            encoded = len(judge_req.user_content.encode("utf-8"))
            self.assertGreaterEqual(encoded, raw, label)
        huge = judge_adapter.build_request(
            request_id="j-huge", case=self.cases[0], arm="WITH_SKILL",
            subject_vendor="anthropic", subject_result=self.result,
            subject_text="漢" * 16_384,
        )
        huge_bytes = len(huge.system.encode("utf-8")) + len(huge.user_content.encode("utf-8"))
        self.assertGreater(huge_bytes, MAX_JUDGE_REQUEST_BYTES)
        # The encoded guard refuses AFTER a paid subject call: a partial
        # outcome, never a completion proof.
        self.assertGreater(_judge_body_bytes(huge), MAX_JUDGE_REQUEST_BYTES)


if __name__ == "__main__":
    unittest.main()
