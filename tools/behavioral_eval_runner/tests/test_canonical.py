"""Canonical serialization and stable hashing (area 2)."""

from __future__ import annotations

import json
import unittest

from tools.behavioral_eval_runner.canonical import (
    canonical_bytes,
    canonical_json,
    is_roundtrip_stable,
    sha256_hex,
    sha256_of_obj,
)
from tools.behavioral_eval_runner.errors import CanonicalizationError


class TestCanonicalJson(unittest.TestCase):
    def test_key_order_never_matters(self) -> None:
        a = {"b": 1, "a": {"y": 2, "x": 3}}
        b = {"a": {"x": 3, "y": 2}, "b": 1}
        self.assertEqual(canonical_json(a), canonical_json(b))
        self.assertEqual(sha256_of_obj(a), sha256_of_obj(b))

    def test_minimal_separators_and_ascii(self) -> None:
        self.assertEqual(canonical_json({"a": [1, 2]}), '{"a":[1,2]}')
        self.assertEqual(canonical_json({"s": "café"}), '{"s":"caf\\u00e9"}')

    def test_stable_under_noop_serialization(self) -> None:
        sample = {
            "list": [1, "two", None, True, {"nested": [0.5]}],
            "text": "value",
        }
        self.assertTrue(is_roundtrip_stable(sample))
        reparsed = json.loads(canonical_json(sample))
        self.assertEqual(canonical_bytes(sample), canonical_bytes(reparsed))

    def test_nan_and_infinity_rejected(self) -> None:
        for bad in (float("nan"), float("inf"), float("-inf")):
            with self.assertRaises(CanonicalizationError):
                canonical_json({"x": bad})

    def test_non_string_keys_rejected(self) -> None:
        with self.assertRaises(CanonicalizationError):
            canonical_json({1: "x"})

    def test_unrepresentable_types_rejected(self) -> None:
        with self.assertRaises(CanonicalizationError):
            canonical_json({"x": object()})
        with self.assertRaises(CanonicalizationError):
            canonical_json({"x": b"bytes"})

    def test_sha256_hex_requires_bytes(self) -> None:
        with self.assertRaises(CanonicalizationError):
            sha256_hex("text")  # type: ignore[arg-type]


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
