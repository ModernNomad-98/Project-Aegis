# OWNER AUTHORITY PACKET — T24 record-store provenance authority (2026-11-10)

Basis: C11-B1-STAGE-A-PLAN-REV2-2026-11-10.md (100,773 B / dc7edc52...), REV2 §5.3/§9 AUTH-STORE; Stage B B3.

## Decision needed
The C1.1 record-store manifest needs a provenance authority kind. REV2 supports REGISTER_ENTRY / OWNER_LINE_RECORD / UNKNOWN with VERIFIED/UNVERIFIED/ABSENT and fails closed; it seeds UNKNOWN and does not fabricate a register id. The programme needs an owner decision on which authority source should back the store/gate record.

## Exact lines (NOT GRANTED; choose one)
A (register entry): "I authorize the approval-register holder to append a bounded entry for the C1.1 revision/review-head record store and verdict gate, binding its exact schema/version and authority scope; C1.1 may then use REGISTER_ENTRY provenance when VERIFIED."
B (owner-line record): "For C1.1, I accept an owner-line record as the provenance authority kind for the record store and gate where no register entry exists; the manifest must record it as OWNER_LINE_RECORD and remain fail-closed when absent/unverified."
C (remain UNKNOWN): "For C1.1, keep store provenance UNKNOWN/VERIFIED-absent until an applicable register entry exists; the checker must remain fail-closed and no VERIFIED claim may be made."

## Conditions
No fabricated register id or hash; no plan revision; no implementation authority by this line; applies only to the C1.1 store/gate provenance.

Recorded by: Lead (DeepSeek Harness; route deepseek-flash). Local record only.