"""Recorded-fixture mock judge client (WP-2B-2).

Returns ONLY pre-recorded responses keyed by request_id. It computes no
verdict, calls no model, and counts zero model calls by construction. A
request with no recording resolves to TRANSPORT_ERROR (which the verdict
layer maps to JUDGE_ERROR) — never a fabricated verdict."""

from __future__ import annotations

from typing import Mapping

from .interface import JudgeClient, JudgeRequest, JudgeResponse, TransportOutcome


class MockJudgeClient(JudgeClient):
    def __init__(self, recorded_responses: Mapping[str, JudgeResponse]) -> None:
        self._responses = dict(recorded_responses)
        self.model_calls = 0  # stays 0 forever: nothing here calls a model

    def dispatch(self, request: JudgeRequest, envelope_bytes: bytes) -> JudgeResponse:
        request.validate()
        recorded = self._responses.get(request.request_id)
        if recorded is None:
            return JudgeResponse(
                request_id=request.request_id,
                response_id=f"mock-missing-{request.request_id}",
                transport_outcome=TransportOutcome.TRANSPORT_ERROR,
                raw_output=None,
            )
        return recorded
