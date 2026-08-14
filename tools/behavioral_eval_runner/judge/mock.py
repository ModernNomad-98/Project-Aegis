"""Recorded-fixture mock judge client (WP-2B-2; R2 §6).

Returns ONLY pre-recorded responses keyed by request_id — and only after
proving the supplied envelope bytes are EXACTLY the envelope the request
binds (``sha256(envelope_bytes) == request.envelope_sha256``). The mock
ignores no envelope byte: a mismatched envelope resolves to
TRANSPORT_ERROR before any recorded PASS/FAIL response is looked up. It
computes no verdict, calls no model, and counts zero model calls by
construction."""

from __future__ import annotations

from typing import Mapping

from ..canonical import sha256_hex
from .interface import JudgeClient, JudgeRequest, JudgeResponse, TransportOutcome


class MockJudgeClient(JudgeClient):
    def __init__(self, recorded_responses: Mapping[str, JudgeResponse]) -> None:
        self._responses = dict(recorded_responses)
        self.model_calls = 0  # stays 0 forever: nothing here calls a model

    def dispatch(self, request: JudgeRequest, envelope_bytes: bytes) -> JudgeResponse:
        request.validate()
        if not isinstance(envelope_bytes, (bytes, bytearray)) or (
            sha256_hex(bytes(envelope_bytes)) != request.envelope_sha256
        ):
            # Fail closed BEFORE any recorded response lookup: the envelope
            # bytes are not the envelope this request binds.
            return JudgeResponse(
                request_id=request.request_id,
                response_id=f"mock-envelope-mismatch-{request.request_id}",
                transport_outcome=TransportOutcome.TRANSPORT_ERROR,
                raw_output=None,
            )
        recorded = self._responses.get(request.request_id)
        if recorded is None:
            return JudgeResponse(
                request_id=request.request_id,
                response_id=f"mock-missing-{request.request_id}",
                transport_outcome=TransportOutcome.TRANSPORT_ERROR,
                raw_output=None,
            )
        return recorded
