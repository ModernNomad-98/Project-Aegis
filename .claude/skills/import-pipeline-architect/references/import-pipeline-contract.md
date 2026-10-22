# Import pipeline contract: import-pipeline-architect artifact

## 1. Stage contract

| Stage | Input | Output | Authorization | Failure handling |
| --- | --- | --- | --- | --- |
| Inspect | source file/API metadata + sample | inventory + validation issues | tenant-scoped operator | reject file with reason |
| Map | source columns, target schema | mapping + transforms | tenant admin | map conflicts listed |
| Preview | mapped rows | per-row preview + errors | tenant admin | rows marked invalid |
| Review | preview result | approved/rejected rows | reviewer role | rejection reason recorded |
| Confirm | approved set | committed rows + status | tenant owner/authorized role | per-row commit/reversal |
| Outcome | job record | status + audit evidence | support/owner | retry/resume |

## 2. Mapping and validation

| Source column | Target field | Transform | Validation | Required |
| --- | --- | --- | --- | --- |
| <source> | <target> | trim/parse date/currency | type/range/regex | yes/no |
| external_id | idempotency key | none | unique per tenant | yes |

Every invalid row gets a status and reason; validation errors are returned per row, not only as a job-level failure.

## 3. Recovery matrix

| Failure point | State | Recovery | Reversal |
| --- | --- | --- | --- |
| validation | pre-commit | fix row, re-validate | none needed |
| partial commit | some rows committed | resume from failed rows (idempotency key) | reverse committed batch per tenant |
| downstream error | committed but status unknown | reconcile by idempotency key | reverse with audit record |

## 4. Completion checklist

- [ ] Stage table complete with authorization per stage.
- [ ] Validation/error reporting is per row.
- [ ] Idempotency and dedupe keys defined.
- [ ] Partial-failure recovery/reversal specified.
- [ ] Tenant isolation, audit evidence, test plan present; no import executed.
