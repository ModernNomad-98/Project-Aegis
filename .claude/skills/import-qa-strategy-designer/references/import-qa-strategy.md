# Import QA Strategy Reference

## Contract table
| Stage | Contract/precondition | Failure outcome | Evidence |
|---|---|---|---|
| parse | source format/encoding/size valid | rejected file, row errors | parser report + counts |
| map | columns map to target fields explicitly | unmapped/missing columns rejected | mapping report |
| validate | types, required fields, ranges, referential/tenant scope | invalid rows quarantined/rejected | errors by row |
| preview | diff/counts/sample visible before commit | no commit until confirmed | preview snapshot |
| commit | atomic write or declared per-row recovery | partial commit only if allowed + recorded | commit/rollback report |
| rollback | reversal bound and tested | rollback outcome recorded | rollback evidence |

## Dataset / edge matrix
Representative valid; boundary min/max/length; malformed encoding/type; duplicate id; overlapping tenant; large volume; missing optional/required; future/expired dates.

## Negative and partial-failure cases
Unauthorized, wrong tenant, missing field, type mismatch, duplicate/replay, partial commit, rollback failure, interrupted retry. Each names expected result and evidence.

## Idempotency / recovery
Duplicate import same idempotency key must not double-write; replay of partial failure resumes or rolls back per recorded contract; evidence records input hash, run id and counts.

## Tenant isolation
Imported rows are scoped to the authorized tenant; cross-tenant read/write attempts are refused and recorded; tenant id comes from authority, not row payload.

## Volume / latency
State tested volume, duration and abort criteria; measure import rate and failure behavior at volume; no production-only data.

## Expected results and handoff
Every check states forbidden/pass outcome and evidence; hand implementation to import-pipeline-architect; limitations and untested edges listed.
