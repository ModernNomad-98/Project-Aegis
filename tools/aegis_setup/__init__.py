"""Offline, advisory-only Aegis setup routing contract."""

from .routing_contract import (
    Compatibility,
    Decision,
    FakeAdapter,
    Request,
    check_compatibility,
    decide,
    parse_request,
)

__all__ = [
    "Compatibility", "Decision", "FakeAdapter", "Request",
    "check_compatibility", "decide", "parse_request",
]
