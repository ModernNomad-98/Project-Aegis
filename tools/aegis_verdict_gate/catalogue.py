"""aegis.verdict-bound/v2.1 catalogue projection (single in-code field list).

This module is the one and only in-code location that names the canonical
verdict field set consumed by this checker.  It is a *projection* of the
contract-owned set documented in

  C03-M1-CANONICAL-VERDICT-FIELDS-DELTA-2026-11-10.md  (section 2.3, 62 entries)
  C03-M1-ERRATA-V2-1-2026-11-10.md                     (v2.1 corrected semantics)

and it does not restate the contract's semantics: it records ids, canonical
dotted paths, requiredness (R/O/C) and group membership only.  Semantics live
in the contract records named above; this tool consumes them by reference and
must not define a second, competing field list (AC3, plan section 6
"one-source rule").

v2.1 changes the required semantics of exactly seven entries:
VB-A09, VB-A10, VB-C07, VB-C08, VB-D01, VB-F09, VB-H07.

No network, no provider SDK, no I/O.  Standard library only.
"""

from __future__ import annotations

import typing

BOUND_SET_ID = "aegis.verdict-bound/v2.1"
BOUND_SET_VERSION = "2.1"
CANONICALIZATION_VERSION = "JCS-RFC8785-v1"
CONTRACT_SCHEMA_ID = "aegis.capability-status/v2"
CONTRACT_DELTA_RECORD = "C03-M1-CANONICAL-VERDICT-FIELDS-DELTA-2026-11-10.md"
ERRATA_RECORD = "C03-M1-ERRATA-V2-1-2026-11-10.md"
REVISION_STORE_SCHEMA = "aegis.revision-store/v1"
REVISION_STATE_SCHEMA = "aegis.revision-state/v1"
TRIAGE_SCHEMA = "aegis.triage/v1"

REQUIRED = "R"
OPTIONAL = "O"
CONDITIONAL = "C"
REQUIREDNESS = (REQUIRED, OPTIONAL, CONDITIONAL)

GROUP_NAMES = {
    "A": "identity and context",
    "B": "exact code state at verdict",
    "C": "policy, plan, revision/counters, evidence input",
    "D": "bound stage evidence records",
    "E": "canonical triage",
    "F": "F reviewer and verdict record",
    "G": "owner line and merge authority",
    "H": "skills, security and reconciliation-witness bindings",
    "I": "the bound hash",
}

GROUP_COUNTS = {"A": 12, "B": 4, "C": 9, "D": 3, "E": 4, "F": 15, "G": 3, "H": 11, "I": 1}

# Entries whose required semantics change in v2.1 (errata sections 2.2, 3.2, 4.2).
V2_1_CHANGED_ENTRIES = (
    "VB-A09",
    "VB-A10",
    "VB-C07",
    "VB-C08",
    "VB-D01",
    "VB-F09",
    "VB-H07",
)


class Entry(typing.NamedTuple):
    """One catalogue entry: id, canonical dotted path, requiredness, group."""

    entry_id: str
    path: str
    requiredness: str
    group: str


ENTRIES: typing.Tuple[Entry, ...] = (
    # A. identity and context (12)
    Entry("VB-A01", "repo.owner", REQUIRED, "A"),
    Entry("VB-A02", "repo.name", REQUIRED, "A"),
    Entry("VB-A03", "change.type", REQUIRED, "A"),
    Entry("VB-A04", "change.id", REQUIRED, "A"),
    Entry("VB-A05", "change.url", OPTIONAL, "A"),
    Entry("VB-A06", "merge_target.ref", REQUIRED, "A"),
    Entry("VB-A07", "candidate_id", REQUIRED, "A"),
    Entry("VB-A08", "contract_schema_version", REQUIRED, "A"),
    Entry("VB-A09", "bound_set_id", REQUIRED, "A"),
    Entry("VB-A10", "bound_set_version", REQUIRED, "A"),
    Entry("VB-A11", "canonicalization_version", REQUIRED, "A"),
    Entry("VB-A12", "conditionals_applied", REQUIRED, "A"),
    # B. exact code state at verdict (4)
    Entry("VB-B01", "head_sha", REQUIRED, "B"),
    Entry("VB-B02", "tree_sha", REQUIRED, "B"),
    Entry("VB-B03", "base_sha", REQUIRED, "B"),
    Entry("VB-B04", "parents", OPTIONAL, "B"),
    # C. policy, plan, revision/counters, evidence input (9)
    Entry("VB-C01", "policy_ref", REQUIRED, "C"),
    Entry("VB-C02", "policy_sha256", REQUIRED, "C"),
    Entry("VB-C03", "plan.sha256", CONDITIONAL, "C"),
    Entry("VB-C04", "plan.revision_count", OPTIONAL, "C"),
    Entry("VB-C05", "plan.basis_ref", CONDITIONAL, "C"),
    Entry("VB-C06", "revision_state_sha256", REQUIRED, "C"),
    Entry("VB-C07", "review_heads.used", REQUIRED, "C"),
    Entry("VB-C08", "review_heads.exception_id", CONDITIONAL, "C"),
    Entry("VB-C09", "evidence_inputs_sha256", REQUIRED, "C"),
    # D. bound stage evidence records (3)
    Entry("VB-D01", "stage_records", REQUIRED, "D"),
    Entry("VB-D02", "plan_audit_applies", REQUIRED, "D"),
    Entry("VB-D03", "plan_audit_waiver_ref", CONDITIONAL, "D"),
    # E. canonical triage (4)
    Entry("VB-E01", "triage.schema_version", REQUIRED, "E"),
    Entry("VB-E02", "triage.sha256", REQUIRED, "E"),
    Entry("VB-E03", "triage.open_blocking", REQUIRED, "E"),
    Entry("VB-E04", "triage.residual_accepted_count", OPTIONAL, "E"),
    # F. F reviewer and verdict record (15)
    Entry("VB-F01", "reviewer.identity_ref", REQUIRED, "F"),
    Entry("VB-F02", "reviewer.role", REQUIRED, "F"),
    Entry("VB-F03", "reviewer.auth_method", REQUIRED, "F"),
    Entry("VB-F04", "reviewer.auth_verified", REQUIRED, "F"),
    Entry("VB-F05", "reviewer.independence.class", REQUIRED, "F"),
    Entry("VB-F06", "reviewer.independence.distinct_from", REQUIRED, "F"),
    Entry("VB-F07", "reviewer.independence.attestation_ref", REQUIRED, "F"),
    Entry("VB-F08", "verdict.stage", REQUIRED, "F"),
    Entry("VB-F09", "verdict.value", REQUIRED, "F"),
    Entry("VB-F10", "verdict.record_id", REQUIRED, "F"),
    Entry("VB-F11", "verdict.record_sha256", REQUIRED, "F"),
    Entry("VB-F12", "verdict.posted_at", REQUIRED, "F"),
    Entry("VB-F13", "verdict.posted_after_last_commit", REQUIRED, "F"),
    Entry("VB-F14", "verdict.edit_state", REQUIRED, "F"),
    Entry("VB-F15", "verdict.event_ref", REQUIRED, "F"),
    # G. owner line and merge authority (3)
    Entry("VB-G01", "owner_line.id", REQUIRED, "G"),
    Entry("VB-G02", "owner_line.register_sha256", REQUIRED, "G"),
    Entry("VB-G03", "merge_authority_ref", CONDITIONAL, "G"),
    # H. skills, security and witness bindings (11)
    Entry("VB-H01", "skills.rows", REQUIRED, "H"),
    Entry("VB-H02", "skills.none_reason", CONDITIONAL, "H"),
    Entry("VB-H03", "skills.sha256", REQUIRED, "H"),
    Entry("VB-H04", "security.surfaces_touched", REQUIRED, "H"),
    Entry("VB-H05", "security.mitigations", REQUIRED, "H"),
    Entry("VB-H06", "security.residual", REQUIRED, "H"),
    Entry("VB-H07", "security.secret_read_or_logged", REQUIRED, "H"),
    Entry("VB-H08", "security.sha256", REQUIRED, "H"),
    Entry("VB-H09", "witness.diff_name_only", REQUIRED, "H"),
    Entry("VB-H10", "witness.probes", REQUIRED, "H"),
    Entry("VB-H11", "witness.sha256", REQUIRED, "H"),
    # I. the bound hash (1)
    Entry("VB-I01", "bound_fields_sha256", REQUIRED, "I"),
)

# The G group's gate-time row is deliberately NOT a catalogue entry and is
# never hashed (contract: "gate-time, not hashed"; plan section 4 A9 fix).
GATE_TIME_ONLY_PATHS: typing.Tuple[str, ...] = ("owner_line.effective_status_at_gate",)

# The single declared metadata envelope a supplied verdict record may carry.
# Its contents are record/display material and are excluded from the bound
# hash (contract section 2.5.3 metadata exclusions; see canonical.py).
DECLARED_METADATA_KEYS: typing.Tuple[str, ...] = ("record",)


def _check_catalogue() -> None:
    if len(ENTRIES) != 62:
        raise RuntimeError("catalogue must contain exactly 62 entries, found %d" % len(ENTRIES))
    counts: typing.Dict[str, int] = {}
    seen_ids = set()
    seen_paths = set()
    for entry in ENTRIES:
        counts[entry.group] = counts.get(entry.group, 0) + 1
        if entry.entry_id in seen_ids:
            raise RuntimeError("duplicate entry id %s" % entry.entry_id)
        if entry.path in seen_paths:
            raise RuntimeError("duplicate entry path %s" % entry.path)
        if entry.requiredness not in REQUIREDNESS:
            raise RuntimeError("bad requiredness for %s" % entry.entry_id)
        if entry.group not in GROUP_COUNTS:
            raise RuntimeError("bad group for %s" % entry.entry_id)
        seen_ids.add(entry.entry_id)
        seen_paths.add(entry.path)
    if counts != GROUP_COUNTS:
        raise RuntimeError("group counts %r do not match %r" % (counts, GROUP_COUNTS))
    for changed in V2_1_CHANGED_ENTRIES:
        if changed not in seen_ids:
            raise RuntimeError("v2.1 changed entry missing from catalogue: %s" % changed)


_check_catalogue()

ENTRIES_BY_ID: typing.Dict[str, Entry] = {entry.entry_id: entry for entry in ENTRIES}
ENTRIES_BY_PATH: typing.Dict[str, Entry] = {entry.path: entry for entry in ENTRIES}


def entries_for_group(group: str) -> typing.Tuple[Entry, ...]:
    """Return the entries of one group letter, in catalogue order."""

    return tuple(entry for entry in ENTRIES if entry.group == group)


def hashed_entries() -> typing.Tuple[Entry, ...]:
    """Entries covered by bound_fields_sha256: A01..H11 (VB-I01 is excluded).

    VB-I01 hashes the projection, so it cannot hash itself; the G gate-time
    row is not a catalogue entry at all.  This is the R/O/C projection the
    contract hashes (plan section 4 A9 fix), not all 62 catalogue entries.
    """

    return tuple(entry for entry in ENTRIES if entry.group != "I")


def hashed_paths() -> typing.Tuple[str, ...]:
    return tuple(entry.path for entry in hashed_entries())


def required_paths() -> typing.Tuple[str, ...]:
    return tuple(entry.path for entry in hashed_entries() if entry.requiredness == REQUIRED)


def conditional_entries() -> typing.Tuple[Entry, ...]:
    return tuple(entry for entry in hashed_entries() if entry.requiredness == CONDITIONAL)


def _schema_tree() -> typing.Dict[str, typing.Any]:
    """Nested closed-schema tree built from the catalogue paths.

    A leaf is an empty dict (scalar or list-valued field: it must not be an
    object with named members); an intermediate node maps member names to
    their own subtree.
    """

    root: typing.Dict[str, typing.Any] = {}
    for entry in ENTRIES:
        node = root
        parts = entry.path.split(".")
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node.setdefault(parts[-1], {})
    return root


def allowed_schema() -> typing.Dict[str, typing.Any]:
    """Closed-schema tree for the canonical set (see _schema_tree)."""

    return _schema_tree()


def allowed_top_level() -> typing.Dict[str, typing.FrozenSet[str]]:
    """Top-level closed-schema map: key -> allowed immediate sub-keys.

    A key mapped to an empty frozen set is a scalar or list-valued field.
    Kept for callers that only need the first level; allowed_schema() is the
    full tree used by the checker.
    """

    return {
        key: frozenset(subtree) for key, subtree in _schema_tree().items()
    }


def declared_metadata_keys() -> typing.Tuple[str, ...]:
    return DECLARED_METADATA_KEYS


def split_path(path: str) -> typing.Tuple[str, ...]:
    return tuple(path.split("."))


def get_path(document: object, path: str) -> typing.Tuple[bool, object]:
    """Return (present, value) for a dotted path; missing => (False, None)."""

    current: object = document
    for part in split_path(path):
        if not isinstance(current, dict) or part not in current:
            return (False, None)
        current = current[part]
    return (True, current)


def set_path(document: typing.Dict[str, object], path: str, value: object) -> None:
    """Set a dotted path in a nested dict, creating intermediate objects."""

    parts = split_path(path)
    current: typing.Dict[str, object] = document
    for part in parts[:-1]:
        nxt = current.get(part)
        if not isinstance(nxt, dict):
            nxt = {}
            current[part] = nxt
        current = nxt
    current[parts[-1]] = value
