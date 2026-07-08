---
name: pii-lifecycle-designer
description: Design the end-to-end lifecycle for personal data across the WHOLE data estate — a PII inventory and classification (direct/indirect identifiers, sensitive classes) mapped to every store it lands in (operational tables, analytics, logs, caches, search indexes, vector stores, backups, third-party processors), minimization at collection (purpose stated per field; collect nothing without one), retention schedules per class with enforcement mechanics, deletion/erasure design that PROPAGATES (a data-subject request reaches derived copies and states the backup policy honestly), anonymization vs pseudonymization chosen with re-identification risk named, and residency constraints carried per store. Produces the lifecycle policy + per-store data map; compliance evidence packaging stays with the compliance pack and LLM-context redaction with sensitive-disclosure-guard. Use when designing PII handling, retention/erasure (DSR) flows, or when nobody can say where personal data lives. Do NOT use for audit-record retention (audit-log-architect) or PII-safe TEST data (test-data-architect).
---

# PII Lifecycle Designer

## Purpose

Personal data is easy to collect and nearly impossible to un-collect: it
fans out from the signup form into analytics extracts, log lines, caches,
search indexes, vector embeddings, backups, and a third-party CRM — and
the first erasure request discovers all of it the hard way. This skill
designs the lifecycle so the estate can answer, with evidence, the four
questions regulators and customers ask: what personal data do you hold,
why, for how long, and how does it die. The deliverable is the
classification, the per-store data map, retention schedules with
enforcement, and an erasure design that actually propagates. It designs
policy-as-mechanism; packaging it as audit evidence is the compliance
pack's job, and keeping PII out of LLM context is
`sensitive-disclosure-guard`'s.

## Use When

- Use when: designing or overhauling how personal data is collected,
  classified, retained, and deleted — greenfield or retrofit.
- Use when: implementing data-subject rights (erasure, export, access)
  and the propagation across stores needs design.
- Use when: nobody can enumerate where PII lives (the data-map question)
  or what the retention story is per field.
- Use when: choosing anonymization vs pseudonymization for analytics or
  data sharing, and the re-identification risk must be assessed.
- Use when: residency constraints (data must stay in region X) need to be
  carried into per-store decisions.
- Do NOT use when: the retention/redaction question is about AUDIT
  records — the audit trail's schema, retention, and redaction are
  `audit-log-architect`; this skill treats the audit log as one more
  store on the map, consuming that design.
- Do NOT use when: generating PII-safe TEST data — synthetic data and
  anonymization paths for test fixtures are `test-data-architect`.
- Do NOT use when: preventing PII from entering LLM prompts/context/logs
  — the AI-boundary redaction pipeline is `sensitive-disclosure-guard`;
  this skill's classification feeds it.
- Do NOT use when: producing auditor-facing control evidence or mapping
  to framework criteria — `compliance-control-foundation` and the
  framework projections own that; they cite this design as the
  implementing mechanism.

## Inputs to Inspect

1. Collection surfaces: signup/profile forms, API payloads, support
   channels, imports, enrichment vendors — every field of personal data
   entering the system, and the stated purpose per field (or its
   absence).
2. The store inventory: operational tables, analytical zones
   (`warehouse-lake-architect` design if present), logs, caches, search
   indexes, vector stores, object storage, queues/streams with retention,
   backups/snapshots, and third-party processors receiving data.
3. Existing schemas and data samples' SHAPE (field names/types — not
   bulk-reading actual personal values) to locate PII columns, including
   the disguised ones (free-text notes, JSON blobs, URLs with emails).
4. Current retention reality: what is deleted today by what mechanism,
   TTLs that exist, and backup rotation schedules.
5. Legal/policy constraints already stated by the org (privacy policy
   promises, contractual clauses, residency commitments) — the design
   must at least meet what is already promised publicly.
6. The tenant model: whether tenant offboarding implies bulk deletion
   obligations distinct from individual subject requests.

## Workflow

1. **Build the classification.** Classes with concrete field examples:
   direct identifiers (email, name, phone, government ids), indirect/
   quasi-identifiers (birth date, postcode, device ids — dangerous in
   combination), sensitive classes (health, financial, biometrics —
   elevated handling), and derived personal data (behavioral profiles,
   embeddings OF personal content). Every class gets: lawful-purpose
   requirement, retention class, and allowed stores.
2. **Draw the data map.** Per store from input 2: which classes land
   there, in what form (raw, pseudonymized, aggregated), via which flow,
   with what retention TODAY vs designed. The map includes the
   embarrassing rows — logs and free-text fields — or it is fiction.
3. **Design minimization at collection.** Per field: purpose stated or
   field dropped; collection-time transforms (store the hash where only
   matching is needed; truncate where precision is unneeded); default-off
   for enrichment. New-field discipline: adding a personal-data field
   requires a purpose and a retention class in the same change — a
   review-time rule.
4. **Set retention schedules with enforcement mechanics.** Per class ×
   store: the period, the trigger (account closure, last activity,
   collection date), and the MECHANISM (TTL index, partition drop,
   scheduled job with completion evidence) — policy without a mechanism
   is a wish. State what "deleted" means per store honestly (row delete
   vs crypto-erasure vs tombstone-then-compact).
5. **Design erasure propagation (DSR).** The subject-id resolution
   (mapping a request to every keyed and derived record), the propagation
   order across the map (operational → caches/indexes → analytics →
   vendor APIs), per-store deletion semantics, completion evidence per
   store, and the honest backup stance: backups age out on rotation
   rather than being surgically edited — state the rotation window,
   restore-time re-deletion procedure, and say exactly that in the
   user-facing policy. Free-text and embedding stores get their stated
   strategy (redaction pass; embedding deletion keyed to source doc).
6. **Choose anonymization vs pseudonymization deliberately.**
   Pseudonymized data (key exists somewhere) IS personal data — retention
   and erasure still apply; state key custody. Anonymization claims get a
   re-identification risk check (quasi-identifier combinations, k-style
   thresholds stated) — most "anonymized" datasets are pseudonymized with
   optimism. Aggregation floors for published/cross-tenant stats.
7. **Carry residency per store.** Which classes are region-pinned, which
   stores replicate across regions (including backups and vendor
   processing locations), and the conflict list where current
   infrastructure violates stated constraints.
8. **Define the standing checks.** Detection of new PII fields (schema
   review rule + periodic scan of field names/free-text samples),
   retention-job completion monitoring, DSR completion SLA tracking —
   standing monitors are specified with `data-quality-monitor-designer`
   where they assert on data, and the evidence trail feeds the
   compliance pack.
9. **Deliver the design** in the Output Format with the residual-risk
   list explicit (stores where erasure is approximate, vendors without
   deletion APIs, legacy backups) — honesty over gloss.

Classification tables, the data-map row format, per-store deletion
semantics, and the DSR propagation checklist:
[references/lifecycle-matrix.md](references/lifecycle-matrix.md).

## Output Format

```
PII LIFECYCLE DESIGN — <scope>
Classification: <classes with field examples; purpose + retention class + allowed stores per class>
Data map:       <per store: classes present, form (raw|pseudo|aggregate), flow in, retention today→designed>
Minimization:   <collection-time drops/transforms; new-field discipline>
Retention:      <per class×store: period, trigger, MECHANISM, meaning of "deleted">
Erasure (DSR):  <subject resolution; propagation order; per-store semantics + evidence;
                 backup stance (rotation window + restore re-deletion); free-text/embedding strategy>
Anonymization:  <pseudo vs anon per dataset; key custody; re-identification check + floors>
Residency:      <class→region pins; replicating stores; conflict list>
Standing checks:<new-PII detection; retention-job monitoring; DSR SLA>
Handoffs:       audit records → audit-log-architect; test data → test-data-architect;
                LLM context → sensitive-disclosure-guard; evidence packaging → compliance pack
Residual risk:  <approximate-erasure stores, vendor gaps, legacy backups — explicit>
```

## Validation Checklist

- [ ] Every classified field has a purpose; fields without one are
      flagged for drop, not silently kept.
- [ ] The data map covers the unglamorous stores: logs, caches, search
      indexes, vector stores, queues, backups, third parties.
- [ ] Every retention entry names a MECHANISM and what "deleted" means in
      that store — no policy-only rows.
- [ ] Erasure design resolves a subject to derived copies (not just the
      primary row) and states completion evidence per store.
- [ ] The backup stance is honest and appears in user-facing policy terms
      (rotation aging, restore-time re-deletion) — no silent surgical-
      backup-edit claims.
- [ ] Nothing labeled "anonymized" without the re-identification check;
      pseudonymized data is treated as personal data with key custody
      stated.
- [ ] Residency conflicts are listed, not smoothed over.
- [ ] The residual-risk list exists and is specific.

## Gotchas

- Logs are the shadow PII store: emails in URLs, names in error messages,
  whole request bodies at debug level. The map that skips logs fails its
  first real DSR. Structured-logging redaction rules are part of the
  design (and align with what `sensitive-disclosure-guard` enforces at
  the AI boundary).
- Free-text fields defeat column-level thinking: support notes contain
  whatever users typed, including other people's data. They need a
  stated strategy (classification as PII-bearing, redaction pass on
  erasure), not exclusion from the map.
- Pseudonymization with the key next door: a "de-identified" analytics
  store whose join key back to identity sits in the same access scope is
  personal data wearing a costume. Key custody and access separation
  make the difference — state them.
- Deletion that isn't: soft-delete flags, tombstones pending compaction,
  and cache TTLs all mean "still there for a while". Per-store semantics
  exist because "deleted" is five different facts in five stores.
- Backups make liars of absolute promises: "we delete within 30 days"
  is false if backups rotate over 90. Align the public promise with the
  rotation window or shorten the rotation — never leave the gap silent.
- Derived data outlives its source: embeddings, ML features, and
  aggregates computed from erased rows persist unless the derivation is
  keyed for deletion. Erasure design includes derivation lineage.
- Vendor deletion is an API call and a prayer: propagation to processors
  needs their deletion mechanism named and its completion evidence
  captured — "we sent the request" is not evidence of deletion.
- Tenant offboarding ≠ subject erasure: deleting a tenant's workspace
  bulk-removes tenant-owned data but individual DSRs from that tenant's
  users may still apply to residue (logs, support tickets). Design both
  paths.

## Stop Conditions

- Asked to label a dataset "anonymized" to skip retention/erasure
  obligations when the re-identification check fails or the
  pseudonymization key exists → refuse the label; present the honest
  classification and what would make anonymization real (key
  destruction, aggregation floors).
- The design would require reading bulk actual personal values (not
  schemas/shapes) to build the map → stop; the map is built from
  structure, samples' shape, and owners' knowledge — widening access to
  personal data in order to govern it defeats the purpose. Escalate
  where structure alone is insufficient.
- A stated residency or public privacy-policy promise is violated by
  current infrastructure and no compliant design exists within scope →
  halt and surface the conflict to a human; do not design around a
  broken promise silently.
- Retention periods are requested with no legal/policy input and the
  class is sensitive (health, financial, minors) → stop and require the
  constraint from counsel/policy owner; engineering defaults are not a
  lawful basis.
- Asked to also execute deletions or run the DSR against live stores →
  decline execution; this skill designs the mechanism, and destructive
  operations follow the repo's human-approval path.

## Supporting Files

- [references/lifecycle-matrix.md](references/lifecycle-matrix.md)
  — classification table with field examples, data-map row format,
  per-store deletion semantics table, DSR propagation checklist, and the
  re-identification check.
- `evals/evals.json` — behavior cases including the backup-honesty edge
  and the fake-anonymization refusal.
- `evals/trigger-evals.json` — discrimination against
  `sensitive-disclosure-guard`, `audit-log-architect`,
  `test-data-architect`, and the compliance pack
  (`compliance-control-foundation`).
