# Export QA Strategy Reference

## Contract table
| Stage | Contract/precondition | Failure outcome | Evidence |
|---|---|---|---|
| authorize | caller/tenant authority verified | unauthorized refused | auth report |
| scope | exact rows/fields/tenant bounded | over-broad scope refused | scope report |
| build | format/encoding complete | error report | build report |
| redact | secrets/PII masked before write | unmasked field refused | redaction evidence |
| deliver | destination and channel bound | failed delivery recorded | delivery report |
| expire | expiry/use limit recorded | expired link refused | expiry evidence |
| audit | every export recorded | missing audit is failure | audit record |

## Dataset / edge matrix
Representative valid; boundary min/max/length; malformed encoding/type; large volume; tenant boundary; missing optional/required; expiry boundary.

## Negative and partial-failure cases
Unauthorized, wrong tenant, over-broad scope, missing redaction, failed/partial delivery, expired link, replay/duplicate delivery. Each names expected result and evidence.

## Idempotency / recovery
Duplicate export same idempotency key must not duplicate delivery; failed/partial delivery resumes or is retried per recorded contract; evidence records input hash, run id and counts.

## Tenant isolation
Exported rows and links are scoped to the authorized tenant; cross-tenant access is refused and recorded; tenant id comes from authority, not payload.

## Volume / latency
State tested volume, duration and abort criteria; measure export rate and failure behavior at volume; no production-only data.

## Expected results and handoff
Every check states forbidden/pass outcome and evidence; hand implementation to export-pipeline-architect; limitations and untested edges listed.
