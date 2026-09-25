"""One-shot, bounded local validator for the offline TypeScript callback candidate."""

from __future__ import annotations

import json
import sys

from tools.aegis_setup.routing_contract import ContractError, decide, parse_request

MAX_FRAME = 6144


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate key")
        result[key] = value
    return result


def run(frame: bytes) -> bool:
    if len(frame) > MAX_FRAME:
        return False
    try:
        data = json.loads(frame, object_pairs_hook=unique_pairs)
        if not isinstance(data, dict) or set(data) != {"request", "response", "kind", "target"}:
            return False
        if data["kind"] not in ("agent", "skill") or not isinstance(data["target"], str):
            return False
        if not isinstance(data["request"], str) or not isinstance(data["response"], str):
            return False
        request = parse_request(data["request"])
        decision = decide(request, data["response"])
        offered = request.agents if data["kind"] == "agent" else request.skills
        selected = decision.agents if data["kind"] == "agent" else decision.skills
        if data["target"] not in {offer.id for offer in offered}:
            return False
        return decision.disposition == "recommend" and data["target"] in selected
    except (ContractError, ValueError, TypeError, KeyError, UnicodeError):
        return False


def main() -> int:
    frame = sys.stdin.buffer.read(MAX_FRAME + 1)
    sys.stdout.write("allow\n" if run(frame) else "deny\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
