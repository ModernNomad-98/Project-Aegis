# Lifecycle Matrix

Classification, data-map, deletion-semantics, and DSR templates backing
the workflow. All examples use placeholders — never live values.

## Classification table (template rows)

| Class | Field examples | Handling floor | Retention class | Allowed stores |
|---|---|---|---|---|
| Direct identifier | email, name, phone, government id | purpose required; access-scoped | tied to account lifecycle | operational; pseudo in analytics |
| Quasi-identifier | birth date, postcode, device id, IP | dangerous in combination — count them per dataset | shortest viable | operational; generalized in analytics |
| Sensitive | health, financial detail, biometrics | elevated: explicit basis, encryption, restricted roles | counsel-set, never defaulted | operational only unless explicitly approved |
| Derived personal | behavioral profiles, embeddings of personal content, ML features | inherits source class; deletion keyed to source | follows source | named stores with lineage |
| Free-text (PII-bearing) | support notes, comments | treat as PII-bearing; redaction strategy required | per containing record | operational; excluded or redacted downstream |

## Data-map row format

```
STORE <name/type: operational table | log stream | cache | search index |
       vector store | analytics zone | queue | backup set | vendor <processor>>
Classes present: <from table above>   Form: raw | pseudonymized | aggregated
Flow in:        <producing surface/pipeline>
Retention:      today=<observed> designed=<period + trigger + MECHANISM>
"Deleted" means:<see semantics table>
Erasure path:   <how a subject's rows/derivatives are found and removed here>
Residency:      <region + replication reality>
```

## Per-store deletion semantics (state honestly)

| Store type | "Deleted" typically means | Watch for |
|---|---|---|
| Relational table | row delete (hard) / flag (soft — NOT deletion) | soft-delete flags sold as erasure; FK-orphaned copies |
| Log stream | retention expiry only — no per-record delete | redact at EMISSION; retroactive scrubbing is rarely real |
| Cache | TTL expiry + explicit key purge | keys derived from PII; long TTLs outliving the source delete |
| Search index | document removal + segment merge lag | stale segments serving "deleted" docs briefly |
| Vector store | embedding delete keyed by source-doc id | embeddings with no source linkage = undeletable |
| Analytics (columnar/lake) | partition rewrite or crypto-erasure | append-only formats needing rewrite jobs — schedule them |
| Queue/stream | retention expiry; compaction tombstones | compacted topics keeping latest-per-key forever |
| Backups | AGING OUT on rotation; restore-time re-deletion | promises shorter than the rotation window |
| Vendor/processor | their API's semantics + completion evidence | "request sent" recorded as "deleted" |

## DSR propagation checklist (erasure)

1. Resolve subject → all keys (user id, emails, device ids, vendor ids)
   and derived-data lineage.
2. Operational stores first (source of truth), evidence per store.
3. Caches + search indexes purged (keys enumerated, not guessed).
4. Analytics zones: pseudonymized rows located via key custody; rewrite
   or crypto-erase; aggregates checked against the floor (no rewrite
   needed if truly above it — say why).
5. Vector/derived stores via lineage.
6. Vendors: deletion API called; completion evidence captured (response,
   attestation, or their audit artifact).
7. Backup stance recorded on the request: rotation window + restore-time
   re-deletion procedure reference.
8. Free-text redaction pass on flagged fields.
9. Completion report: per-store evidence, exceptions (legal holds —
   scoped and time-bound), SLA timestamp.

Export (access/portability) reuses steps 1–2's resolution with a
read-and-package path — design it from the same map.

## Re-identification check (before any "anonymized" label)

- Enumerate quasi-identifiers present; assess combination uniqueness
  (would <k> individuals share every combination? state the k used).
- Check join paths: does any in-scope actor hold a dataset that links
  back (including the pseudonymization key)? Key exists ⇒ pseudonymized,
  not anonymous — retention/erasure still apply; state key custody and
  rotation.
- Aggregation floor for published/cross-tenant stats: minimum cohort
  size stated; suppression rule for small cells.
- Record the check's evidence with the dataset; "anonymized" without a
  recorded check is a finding.

## New-PII detection (standing)

- Schema-review rule: personal-data field additions require purpose +
  retention class in the same change (review convention, CI-assisted
  where field-name heuristics allow).
- Periodic scan: field-name heuristics (email, phone, name, address,
  dob) + sampled free-text shape checks on new datasets — routed as
  data-map update proposals, never silent additions.
