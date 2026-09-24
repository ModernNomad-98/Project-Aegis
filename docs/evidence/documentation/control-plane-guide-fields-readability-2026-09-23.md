# Control-plane guide field explanations — 2026-09-23

**Current reading (2026-09-24):** The independent review pending at this
draft-freeze snapshot was completed during the delivery of this batch. Read
the [current control-plane package guide](../../../tools/aegis_delivery_control/README.md)
and [documentation ledger](../../roadmaps/aegis-documentation-readability-backlog.md)
for present status. The 10-link and 185-skill receipts below remain dated
evidence of this correction.

Edit start: 22:24:45 Coordinated Universal Time (UTC). Base: exact pull
request (PR) #191 merge `761915207f7974b3d4cab7fb099216188ef3e968`.
The previous deep component screen was estimated at 2–4 active hours; this
bounded guide correction is estimated at 1–3 active hours. The selected
remaining backlog estimate was 175–394 active hours. These estimates do not
measure elapsed work time.

## Scope and source

This batch changes only the [control-plane guide](../../../tools/aegis_delivery_control/README.md)
and this note. It explains the embedded database, digest, Linux state directory
and transaction sync setting near their first use. It also explains the
expected-vector fields and synthetic issuer key used by the read-only `verify`
command. The [offline command-line fixture](../../../tools/aegis_delivery_control/tests/test_dispatch.py)
and [command parser](../../../tools/aegis_delivery_control/cli.py) were read to
verify the exact JavaScript Object Notation (JSON) field names and command
behavior. The fixture demonstrates shape and parsing with locally prepared
synthetic state; it is not independent freshness evidence. No fixture or
command implementation changed.

The guide still describes a synthetic offline kernel. These explanations do
not create real authority, an external adapter, provider access, private input
access, a host proof, or a deployment route. The example requires independent
synthetic source facts and deliberately supplies no credential or fabricated
freshness value.

## Verification and review

Draft freeze: 22:26:12 UTC, 1 minute 27 seconds observed wall time from edit
start; active effort was not separately instrumented. All 10 relative links
across the two scoped pages resolve locally. `python -B scripts/validate-skills.py`
reported 185 valid skills and zero warnings. The read-only `verify --help`
command displayed both required file arguments without opening a state
database. `git diff --check` passed; only this note and the guide changed.
Independent read-only review is pending at draft freeze.
