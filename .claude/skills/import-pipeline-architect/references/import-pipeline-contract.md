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

## 1b. Export-contract mirroring

The import mirrors the shipped export pipeline contract dimension by dimension; a missing counterpart is a design gap.

| Export dimension | Import counterpart | Where specified |
| --- | --- | --- |
| Request + requester authority/tenant scope | inspect stage authority + tenant scope | stage contract (section 1) |
| Async job/status model | staged preview/review/confirm status transitions | stage contract (section 1) |
| Download/result artifact | outcome artifact + per-row result/report | stage contract (section 1) |
| Field-level redaction | masking/redaction of sensitive fields in preview/outcome | mapping/validation (section 2) |
| Expiry/retention | retention of uploaded files and staged previews | recovery matrix/audit plan |

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
