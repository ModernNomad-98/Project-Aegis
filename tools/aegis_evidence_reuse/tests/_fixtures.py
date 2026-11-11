"""Load and build the synthetic reuse fixtures.

The fixture JSON files carry the record payload and the evidence set; the
provenance digest is computed here (tests may not hard-code a digest that the
validator would then trust).  All identities are synthetic: no real PR,
person, secret or approval.
"""

from __future__ import annotations

import copy
import json
import pathlib

from tools.aegis_evidence_reuse import schema

FIXTURE_DIR = pathlib.Path(__file__).resolve().parent / "fixtures"


def case_names() -> list:
    return sorted(path.stem for path in FIXTURE_DIR.glob("*.json"))


def load_case(name: str) -> dict:
    path = FIXTURE_DIR / (name if name.endswith(".json") else name + ".json")
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_record(case: dict) -> dict:
    record = copy.deepcopy(case["record"])
    provenance = record.setdefault("provenance", {})
    provenance["source_ref"] = "fixture:reuse"
    provenance["as_of"] = "2026-11-11T00:00:00Z"
    provenance["producer_role"] = "implementer"
    provenance.setdefault("producer_identity_ref", None)
    provenance["declared_payload_sha256"] = schema.payload_digest(record)
    provenance["declared_payload_bytes"] = schema.payload_bytes(record)
    return record
