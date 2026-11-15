"""Projection test for the required-governance contract (plan section 5.2.1 / B05).

Reads the committed task-33 inventory (mirrored byte-for-byte under
docs/governance/inputs/), the committed rule-projection mapping and the committed
contract. It pins every direct field byte-for-byte against the inventory and
re-runs the committed classifier to assert every derived field. The plan document
is never an oracle here.
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.aegis_preflight import governance as gov  # noqa: E402

DIRECT_FIELDS = {
    "anchor": "anchor",
    "class": "cls",
    "dimension": "dim",
    "lifecycle": "lifecycle",
}


class RuleProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.inventory = gov.load_inventory(REPO_ROOT)
        cls.projection = gov.load_projection(REPO_ROOT)
        cls.contract, cls.contract_bytes = gov.load_contract(REPO_ROOT)
        cls.inventory_rules = {rule["id"]: rule for rule in cls.inventory["rules"]}
        cls.contract_rules = {rule["rule_id"]: rule for rule in cls.contract["rule_applicability"]}

    def test_inventory_identity_is_pinned(self) -> None:
        raw = (REPO_ROOT / gov.INVENTORY_RELPATH).read_bytes()
        self.assertEqual(len(raw), gov.INVENTORY_BYTES)
        self.assertEqual(gov.sha256_upper(raw), gov.INVENTORY_SHA256)
        self.assertEqual(raw.count(b"\n"), gov.INVENTORY_LF)
        self.assertEqual(len(self.inventory_rules), 187)

    def test_rule_id_set_is_the_inventory_set(self) -> None:
        self.assertEqual(sorted(self.contract_rules), sorted(self.inventory_rules))
        self.assertEqual(len(self.contract["rule_applicability"]), 187)
        self.assertEqual(
            [rule["rule_id"] for rule in self.contract["rule_applicability"]],
            sorted(self.inventory_rules),
        )

    def test_direct_fields_are_byte_equal_to_the_inventory(self) -> None:
        for rule_id, rule in self.contract_rules.items():
            source = self.inventory_rules[rule_id]
            for field, inventory_field in DIRECT_FIELDS.items():
                self.assertEqual(rule[field], source[inventory_field], "%s %s" % (rule_id, field))
            consumer = source["consumer"]
            self.assertEqual(rule["adoption_status"], consumer["adoption_status"], rule_id)
            self.assertEqual(rule["consumer_effect"], consumer.get("effect") or "", rule_id)

    def test_derived_fields_are_reproduced_by_the_committed_classifier(self) -> None:
        derived = gov.derive_projection_output(self.inventory, self.projection)["rules"]
        for rule_id, rule in self.contract_rules.items():
            expected = derived[rule_id]
            for field in ("source_document", "applies_to_roles", "authority_action", "enforcement_class", "enforcement_ref"):
                self.assertEqual(rule[field], expected[field], "%s %s" % (rule_id, field))
            enforcement_class, enforcement_ref = gov.classify_enforcement(
                self.inventory_rules[rule_id].get("enforce"), self.projection
            )
            self.assertEqual(rule["enforcement_class"], enforcement_class, rule_id)
            self.assertEqual(rule["enforcement_ref"], enforcement_ref, rule_id)
        self.assertEqual(
            self.projection["derived"]["classifier_version"],
            self.projection["enforcement_classifier"]["version"],
        )
        self.assertEqual(self.projection["derived"], gov.derive_projection_output(self.inventory, self.projection))

    def test_source_mapping_is_total_and_primary_is_first(self) -> None:
        inventory_sources = {rule["source"] for rule in self.inventory_rules.values()}
        mapping = self.projection["source_to_doc_id"]
        self.assertEqual(set(mapping), inventory_sources)
        document_ids = {row["doc_id"] for row in self.projection["document_ids"]}
        for source, entry in mapping.items():
            self.assertEqual(entry["primary"], entry["all"][0], source)
            self.assertTrue(set(entry["all"]) <= document_ids, source)
            self.assertEqual(self.contract_rules_by_source(source), [])
            for rule in self.inventory_rules.values():
                if rule["source"] == source:
                    self.assertEqual(
                        self.contract_rules[rule["id"]]["source_document"], entry["primary"], rule["id"]
                    )

    def contract_rules_by_source(self, source: str) -> list:
        return [
            rule["rule_id"]
            for rule in self.inventory_rules.values()
            if rule["source"] == source and rule["id"] not in self.contract_rules
        ]

    def test_document_citations_are_the_rules_the_document_sources(self) -> None:
        expected: dict = {}
        for rule in self.inventory_rules.values():
            for doc_id in self.projection["source_to_doc_id"][rule["source"]]["all"]:
                expected.setdefault(doc_id, set()).add(rule["id"])
        for document in self.contract["documents"]:
            self.assertEqual(document["citations"], sorted(expected.get(document["doc_id"], set())), document["doc_id"])

    def test_document_identities_match_the_checkout(self) -> None:
        for document in self.contract["documents"]:
            identity = gov.file_identity(REPO_ROOT, document["path"])
            self.assertEqual(document["bytes"], identity["bytes"], document["path"])
            self.assertEqual(document["lf"], identity["lf"], document["path"])
            self.assertEqual(document["sha256"], identity["sha256"], document["path"])

    def test_counts_match_the_inventory(self) -> None:
        classes: dict = {}
        dimensions: dict = {}
        lifecycles: dict = {}
        adoption: dict = {}
        portable_adoption: dict = {}
        portable = 0
        for rule in self.inventory_rules.values():
            classes[rule["cls"]] = classes.get(rule["cls"], 0) + 1
            dimensions[rule["dim"]] = dimensions.get(rule["dim"], 0) + 1
            lifecycles[rule["lifecycle"]] = lifecycles.get(rule["lifecycle"], 0) + 1
            status = rule["consumer"]["adoption_status"]
            adoption[status] = adoption.get(status, 0) + 1
            if rule["consumer"].get("portable"):
                portable += 1
                portable_adoption[status] = portable_adoption.get(status, 0) + 1
        self.assertEqual(classes, self.inventory["counts"]["by_class"])
        self.assertEqual(dimensions, self.inventory["counts"]["by_dimension"])
        self.assertEqual(lifecycles, self.inventory["counts"]["by_lifecycle"])
        self.assertEqual(portable, self.inventory["counts"]["portable_rules"])
        self.assertEqual(portable_adoption, self.inventory["counts"]["portable_by_adoption_status"])
        self.assertEqual(adoption["not-portable"], 95)
        self.assertEqual(adoption["proposed-default"], 73)
        self.assertEqual(adoption["adopted-if-consumer-adopts"], 11)
        self.assertEqual(adoption["adopted-by-copy"], 7)
        self.assertEqual(adoption["adopted-boundary"], 1)
        self.assertEqual(classes["action-permission"], 17)
        authority_action = [rule for rule in self.contract_rules.values() if rule["authority_action"]]
        self.assertEqual(len(authority_action), 17)
        self.assertTrue(all(rule["class"] == "action-permission" for rule in authority_action))

    def test_no_aggregate_enforcement_tally_is_published(self) -> None:
        serialized = json.dumps(self.contract, sort_keys=True)
        self.assertNotIn("enforcement_summary", serialized)
        self.assertNotIn("enforcement_counts", serialized)
        self.assertNotIn("enforced_count", serialized)
        self.assertFalse(self.projection["enforcement_classifier"]["aggregate_count_published"])

    def test_contract_is_non_circular(self) -> None:
        text = self.contract_bytes.decode("utf-8")
        self.assertNotIn(gov.sha256_upper(self.contract_bytes), text)
        manifest = (REPO_ROOT / gov.MANIFEST_RELPATH).read_bytes()
        self.assertNotIn(gov.sha256_upper(manifest), text)

    def test_contract_bytes_are_canonical_and_rendered_byte_identically(self) -> None:
        self.assertEqual(gov.canonical_bytes(self.contract), self.contract_bytes)
        self.assertEqual(gov.render_contract_bytes(REPO_ROOT), self.contract_bytes)
        self.assertEqual(
            gov.render_projection_bytes(REPO_ROOT), (REPO_ROOT / gov.PROJECTION_RELPATH).read_bytes()
        )

    def test_manifest_binds_the_contract(self) -> None:
        manifest = json.loads((REPO_ROOT / gov.MANIFEST_RELPATH).read_text(encoding="utf-8"))
        entries = {entry["path"]: entry for entry in manifest["entries"]}
        self.assertIn("required-governance-contract.v1.json", entries)
        self.assertEqual(entries["required-governance-contract.v1.json"]["sha256_raw"], gov.sha256_raw(self.contract_bytes))
        self.assertNotIn("manifest_identity", manifest)


if __name__ == "__main__":
    unittest.main()
