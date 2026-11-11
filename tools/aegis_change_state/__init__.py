"""Aegis C1.2 change-state producers and validators (auditable tooling, not enforcement).

Package marker and version constants bound to aegis.change-state/v1.

This package produces and validates the *supplied inputs* the merged C1.1a
checker (tools/aegis_verdict_gate/) already consumes: a candidate freeze
record, a settlement record, B/D/E stage declarations, a per-head snapshot
manifest, an authoritative head-history export and an append-only change
ledger.  It never computes readiness, never approves anything and never
claims a host control is enforced.

Assurance status: AUDITABLE.  mounted coverage: UNKNOWN.  ENFORCED: blocked.

The merged checker and the merged revision-state store are consumed by
reference and are not modified.  Store/change-state provenance is UNVERIFIED
while owner decision T24 (AUTH-STORE) is unresolved, and production readiness
is BLOCKED while T6 is undecided; this package displays both states and has
no code path that turns either into a green result.
"""

from __future__ import annotations

__version__ = "1.0.0"

TOOL_NAME = "aegis-change-state"
SCHEMA_VERSION = "aegis.change-state/v1"
FREEZE_SCHEMA_VERSION = "aegis.change-state/freeze/v1"
SETTLEMENT_SCHEMA_VERSION = "aegis.change-state/settlement/v1"
STAGE_SCHEMA_VERSION = "aegis.change-state/stage-declaration/v1"
SNAPSHOT_SCHEMA_VERSION = "aegis.change-state/snapshot/v1"
HEAD_HISTORY_SCHEMA_VERSION = "aegis.change-state/head-history/v1"

SNAPSHOT_METHOD = "git-archive"
SNAPSHOT_FORMAT_VERSION = "git-archive-tar/v1"
SNAPSHOT_FLAGS = ("--format=tar",)

# The merged checker is the only readiness authority.  These constants are
# display values, not predicates.
ASSURANCE = {"claim": "AUDITABLE", "mounted_coverage": "UNKNOWN"}
PROVENANCE_BINDING_STATUS = "UNVERIFIED"

NOT_VERIFIABLE = (
    "production readiness (owner decision T6 is UNVERIFIED+BLOCKED)",
    "verified store/change-state provenance (AUTH-STORE / T24 unresolved)",
    "real fourth-head exception and unavailable-review disposition (T7 undefined)",
    "real mounted host coverage and denial evidence (T5 export not authorized)",
    "required-context gating or enforcement (T4 declined; C1.1b separate)",
)

__all__ = [
    "ASSURANCE",
    "FREEZE_SCHEMA_VERSION",
    "HEAD_HISTORY_SCHEMA_VERSION",
    "NOT_VERIFIABLE",
    "PROVENANCE_BINDING_STATUS",
    "SCHEMA_VERSION",
    "SETTLEMENT_SCHEMA_VERSION",
    "SNAPSHOT_FLAGS",
    "SNAPSHOT_FORMAT_VERSION",
    "SNAPSHOT_METHOD",
    "SNAPSHOT_SCHEMA_VERSION",
    "STAGE_SCHEMA_VERSION",
    "TOOL_NAME",
    "__version__",
]
