# Statement of Applicability — template

Controlled document. Rows are seeded from the LICENSED standard's Annex A
table (ISO/IEC 27001:2022 and/or ISO/IEC 42001:2023) — never from memory or
secondary summaries.

## Header block

```
Organization / ISMS-AIMS scope:  <scope statement reference>
Standard(s):                     ISO/IEC 27001:2022 | ISO/IEC 42001:2023 | both
Version:                         <n>       Date: <YYYY-MM-DD>
Author:                          <name>
Approver (named human):          <name, role>
Review cadence:                  <e.g. annual + on major change/risk-assessment update>
Risk assessment referenced:      <register id/version — the 6.1.3 trace source>
Annex A source:                  licensed standard text, edition pinned
```

## Row template

```
| Annex A ref | Control title (as published) | Applicable | Justification | Status | Mechanism / owner | Evidence hook |
| --- | --- | --- | --- | --- | --- | --- |
| <id> | <quoted title> | yes/no | <see patterns below> | implemented / partial(<residue>) / planned(<owner,date>) | <compliance-control-foundation CC-id or named artifact> | <→ compliance-evidence-collector> |
```

## Justification patterns

**Inclusion — by risk trace (preferred):**
`Treats R-<id> <risk name> per treatment decision <ref>.`

**Inclusion — by obligation:**
`Required by <law/contract/policy ref> independent of risk appetite.`

**Exclusion — must pass all three tests:**
1. Concrete: names the absent activity/asset ("no physical data centers
   operated"), not a vibe ("not relevant").
2. Verifiable: an auditor can check it against the scope statement.
3. Current: dated; re-verified each review cycle — stale justifications
   are findings.

## Per-standard notes

- **27001:2022**: Annex A is normative, titled "Information security
  controls reference"; controls group into four themes (A.5 Organizational,
  A.6 People, A.7 Physical, A.8 Technological). Do not cite theme control
  counts without verifying against the table in hand — public counts are
  secondary-sourced.
- **42001:2023**: Annex A is normative, titled "Reference control
  objectives and controls"; rows carry objective + control structure.
  Annex B (normative) holds implementation guidance. Do not state Annex A
  counts from public sources — they conflict; count only what the licensed
  text shows.
- Combined documents keep per-standard applicability columns — decisions
  never bleed across standards.
