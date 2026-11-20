"""Catalogue tests: 62 entries, group counts, v2.1 identity, one source (AC3)."""

from __future__ import annotations

import pathlib
import re
import sys
import typing
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
SCRIPTS_DIR = pathlib.Path(__file__).resolve().parents[2]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from aegis_verdict_gate import catalogue  # noqa: E402

TOOL_DIR = pathlib.Path(__file__).resolve().parents[1]
SCAN_ROOTS = ("docs", "tools", "scripts", ".github")
SCAN_SUFFIXES = {".md", ".py", ".json", ".jsonl", ".yml", ".yaml", ".txt"}
SKIP_DIRS = {"evidence", "artifacts", ".git", "fixtures", "revision-state"}

# One source rule (docs/delivery-workflow.md, "Authenticated independent verdict
# consumption"): the canonical set is CONSUMED BY VERSION LABEL and restated
# nowhere, so a version-label reference is allowed and only a second field list -
# an actual restatement of the canonical set - is refused.  The selector looks
# for the label plus a restatement, or a dense restatement without the label.
# (The earlier rule treated ANY mention of the label, or of VB-F09, as a second
# field list; that flagged the contract references the CI run reported.)
BOUND_SET_LABEL = "aegis.verdict-bound"
VB_ENTRY_ID = re.compile(r"\bVB-[A-J][0-9]{2}\b")
RESTATED_ENTRY_ID_COUNT = 2
RESTATED_PATH_COUNT = 3
RESTATED_TOTAL_TOKENS = 3
DENSE_PATH_COUNT = 12

# Canonical paths whose names also belong to unrelated schemas (git identity,
# change-state records, preflight bundles).  A contract reference - or a
# consumer of the contract - may legitimately name one or two of them, so they
# are not counted as evidence that the canonical field list was restated.
SHARED_FIELD_PATHS = frozenset(
    {
        "base_sha",
        "candidate_id",
        "change.id",
        "change.type",
        "change.url",
        "head_sha",
        "merge_target.ref",
        "parents",
        "plan.basis_ref",
        "plan.revision_count",
        "plan.sha256",
        "policy_ref",
        "policy_sha256",
        "repo.name",
        "repo.owner",
        "stage_records",
        "tree_sha",
        "verdict.record_id",
        "verdict.record_sha256",
        "verdict.stage",
    }
)
CONTRACT_ONLY_PATHS = tuple(
    path for path in catalogue.hashed_paths() if path not in SHARED_FIELD_PATHS
)

# The six contract-reference documents the CI run named as offenders before this
# selector existed.  They consume the contract by version label; they are not
# field lists.
CI_FLAGGED_REFERENCES = (
    "docs/roadmaps/consumer-readiness-programme/authority/OWNER-AUTHORITY-PACKETS-2026-11-10.md",
    "docs/roadmaps/consumer-readiness-programme/plans/C12-C14-STAGE-A-PLAN-REV4-2026-11-11.md",
    "docs/roadmaps/consumer-readiness-programme/plans/C2-STAGE-A-PLAN-REV2-2026-11-11.md",
    "docs/roadmaps/consumer-readiness-programme/plans/C3-C4-STAGE-A-PLAN-REV3-2026-11-11.md",
    "docs/roadmaps/consumer-readiness-programme/plans/E2-E4-STAGE-A-PLAN-DRAFT-2026-11-11.md",
    "docs/roadmaps/consumer-readiness-programme/registers/C&C-BACKLOG-PREPLAN-REV3-2026-11-11.md",
)


def second_field_list_evidence(text: str) -> str:
    """Return why text restates the canonical field list, or "" when it does not."""

    entry_ids = sorted(set(VB_ENTRY_ID.findall(text)))
    contract_paths = [path for path in CONTRACT_ONLY_PATHS if path in text]
    labelled = BOUND_SET_LABEL in text
    restated_tokens = len(entry_ids) + len(contract_paths)
    if labelled and len(entry_ids) >= RESTATED_ENTRY_ID_COUNT:
        return "contract label plus %d bound-verdict entry ids" % len(entry_ids)
    if labelled and len(contract_paths) >= RESTATED_PATH_COUNT:
        return "contract label plus %d contract-only field paths" % len(contract_paths)
    if labelled and restated_tokens >= RESTATED_TOTAL_TOKENS:
        # Entry ids and field paths can be mixed in one list; counting them
        # separately would let a mixed three-row list evade both thresholds
        # (Codex P2 on the first head).
        return "contract label plus %d mixed restatement tokens" % restated_tokens
    if len(contract_paths) >= DENSE_PATH_COUNT:
        return "%d contract-only field paths" % len(contract_paths)
    return ""


def scan_offenders() -> typing.List[typing.Tuple[str, str]]:
    """Every file outside the tool that restates the canonical field list."""

    offenders = []
    for root_name in SCAN_ROOTS:
        root = REPO_ROOT / root_name
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix not in SCAN_SUFFIXES:
                continue
            try:
                relative = path.relative_to(REPO_ROOT)
            except ValueError:
                continue
            if (
                relative.parts
                and relative.parts[0] == "scripts"
                and len(relative.parts) > 1
                and relative.parts[1] == TOOL_DIR.name
            ):
                continue
            if any(part in SKIP_DIRS for part in relative.parts):
                continue
            if path.stat().st_size > 400_000:
                continue
            evidence = second_field_list_evidence(path.read_text(encoding="utf-8", errors="ignore"))
            if evidence:
                offenders.append((str(relative), evidence))
    return offenders


class CatalogueTest(unittest.TestCase):
    def test_exactly_62_entries(self):
        self.assertEqual(len(catalogue.ENTRIES), 62)
        self.assertEqual(len(catalogue.ENTRIES_BY_ID), 62)
        self.assertEqual(len(catalogue.ENTRIES_BY_PATH), 62)

    def test_group_counts(self):
        counts = {}
        for entry in catalogue.ENTRIES:
            counts[entry.group] = counts.get(entry.group, 0) + 1
        self.assertEqual(counts, {"A": 12, "B": 4, "C": 9, "D": 3, "E": 4, "F": 15, "G": 3, "H": 11, "I": 1})
        self.assertEqual(catalogue.GROUP_COUNTS, counts)

    def test_entry_ids_are_contiguous_per_group(self):
        for group, count in catalogue.GROUP_COUNTS.items():
            entries = catalogue.entries_for_group(group)
            self.assertEqual(len(entries), count)
            expected = ["VB-%s%02d" % (group, index) for index in range(1, count + 1)]
            self.assertEqual([entry.entry_id for entry in entries], expected)

    def test_requiredness_vocabulary(self):
        seen = {entry.requiredness for entry in catalogue.ENTRIES}
        self.assertEqual(seen, {"R", "O", "C"})
        conditional = {entry.entry_id for entry in catalogue.conditional_entries()}
        self.assertEqual(conditional, {"VB-C03", "VB-C05", "VB-C08", "VB-D03", "VB-G03", "VB-H02"})

    def test_v2_1_identity_and_changed_entries(self):
        self.assertEqual(catalogue.BOUND_SET_ID, "aegis.verdict-bound/v2.1")
        self.assertEqual(catalogue.BOUND_SET_VERSION, "2.1")
        self.assertEqual(catalogue.CANONICALIZATION_VERSION, "JCS-RFC8785-v1")
        self.assertNotEqual(catalogue.BOUND_SET_ID, "aegis.verdict-bound/v2")
        self.assertEqual(len(catalogue.V2_1_CHANGED_ENTRIES), 7)
        for entry_id in catalogue.V2_1_CHANGED_ENTRIES:
            self.assertIn(entry_id, catalogue.ENTRIES_BY_ID)

    def test_hashed_projection_is_61_not_62(self):
        hashed = catalogue.hashed_entries()
        self.assertEqual(len(hashed), 61)
        self.assertNotIn("VB-I01", [entry.entry_id for entry in hashed])
        self.assertIn("VB-I01", catalogue.ENTRIES_BY_ID)
        self.assertNotIn("bound_fields_sha256", catalogue.hashed_paths())

    def test_gate_time_row_is_not_a_catalogue_entry(self):
        self.assertNotIn("owner_line.effective_status_at_gate", catalogue.ENTRIES_BY_PATH)
        self.assertIn("owner_line.effective_status_at_gate", catalogue.GATE_TIME_ONLY_PATHS)
        schema = catalogue.allowed_schema()
        self.assertEqual(set(schema["owner_line"]), {"id", "register_sha256"})

    def test_closed_schema_covers_every_top_level_group(self):
        schema = catalogue.allowed_schema()
        tops = {entry.path.split(".")[0] for entry in catalogue.ENTRIES}
        self.assertEqual(set(schema), tops)
        self.assertEqual(set(schema["reviewer"]), {"identity_ref", "role", "auth_method", "auth_verified", "independence"})
        self.assertEqual(set(schema["reviewer"]["independence"]), {"class", "distinct_from", "attestation_ref"})
        self.assertEqual(set(schema["plan"]), {"sha256", "revision_count", "basis_ref"})

    def test_one_source_rule_no_second_field_list(self):
        offenders = scan_offenders()
        self.assertEqual(offenders, [], "a second canonical field list must not exist outside the tool")


class OneSourceRuleTest(unittest.TestCase):
    """Reconciles "consume by version label" with "no second field list" (AC4)."""

    def test_version_label_reference_is_allowed(self):
        text = (
            "The canonical set is consumed by version, never restated: the merged "
            "checker's bound-verdict schema (aegis.verdict-bound/v2.1) is referenced "
            "by label only."
        )
        self.assertEqual(second_field_list_evidence(text), "")

    def test_reference_naming_one_entry_or_one_path_is_allowed(self):
        text = "aegis.verdict-bound/v2.1 - VB-F09 evidence_inputs_sha256 pointer row only; no list."
        self.assertEqual(second_field_list_evidence(text), "")

    def test_two_entry_ids_beside_the_label_are_a_second_list(self):
        text = "aegis.verdict-bound/v2.1\nVB-A01 repo.owner\nVB-A02 repo.name\n"
        self.assertEqual(
            second_field_list_evidence(text),
            "contract label plus 2 bound-verdict entry ids",
        )

    def test_three_contract_only_paths_beside_the_label_are_a_second_list(self):
        text = (
            "aegis.verdict-bound/v2.1: reviewer.auth_verified; "
            "reviewer.independence.class; witness.probes"
        )
        self.assertEqual(
            second_field_list_evidence(text),
            "contract label plus 3 contract-only field paths",
        )

    def test_a_mixed_restatement_beside_the_label_is_a_second_list(self):
        # Codex P2 on the first head: one entry id plus two contract-only paths
        # is a three-row list and must not evade the separate thresholds.
        text = (
            "aegis.verdict-bound/v2.1:\n"
            "VB-B01 head_sha\n"
            "reviewer.auth_verified\n"
            "witness.probes\n"
        )
        self.assertEqual(
            second_field_list_evidence(text),
            "contract label plus 3 mixed restatement tokens",
        )

    def test_a_dense_restatement_without_the_label_is_a_second_list(self):
        text = "\n".join(CONTRACT_ONLY_PATHS[:DENSE_PATH_COUNT])
        self.assertEqual(
            second_field_list_evidence(text),
            "%d contract-only field paths" % DENSE_PATH_COUNT,
        )

    def test_a_full_copy_of_the_projection_is_a_second_list(self):
        text = "\n".join(catalogue.hashed_paths())
        self.assertTrue(second_field_list_evidence(text))

    def test_the_canonical_projection_itself_is_recognised(self):
        source = (TOOL_DIR / "catalogue.py").read_text(encoding="utf-8")
        self.assertNotEqual(second_field_list_evidence(source), "")

    def test_the_ci_flagged_contract_references_are_not_offenders(self):
        for relative in CI_FLAGGED_REFERENCES:
            path = REPO_ROOT / relative
            self.assertTrue(path.is_file(), "%s must exist" % relative)
            self.assertEqual(
                second_field_list_evidence(path.read_text(encoding="utf-8", errors="ignore")),
                "",
                "%s references the contract by version label; it is not a second field list" % relative,
            )


if __name__ == "__main__":
    unittest.main()
