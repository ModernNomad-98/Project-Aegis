# Crosswalk Row Template

## Header (mandatory)

```
CONTROL CROSSWALK — <org> v<n>   Date: <YYYY-MM-DD>   Owner: <named human>
Editions pinned:
  ISO/IEC 27001:2022 [+ Amd 1:2024]   — Annex A table in hand: yes/no
  ISO/IEC 42001:2023                  — Annex A table in hand: yes/no
  TSC 2017 (revised PoF 2022, AICPA)  — criteria text in hand: yes/no
  NIST AI RMF 1.0                     — Core text in hand: yes/no (note: RMF 1.0 under revision — check current)
Rule: cells fill ONLY from text in hand; otherwise `unverified`. No memory-recalled IDs.
```

## Row

```
| Control (foundation) | 27001 Annex A | SOC 2 TSC | 42001 Annex A | AI RMF fn | Notes |
| --- | --- | --- | --- | --- | --- |
| CC-<dom>-<nn> <name> | <ref> · FULL/PARTIAL(<residue>)/NONE · verified/unverified | same shape | same shape | GOVERN/MAP/MEASURE/MANAGE/n-a | joint sets, edition notes |
```

## Satisfaction vocabulary

- **FULL** — the control as implemented covers the requirement's
  substance. Not "mostly."
- **PARTIAL(<residue>)** — names exactly what is not covered; residue
  feeds `compliance-gap-auditor`.
- **NONE** — listed only when the absence is informative (expected
  mapping that doesn't hold).

## Verification status

- **verified** — cell checked against the pinned edition's text in hand,
  by a named person/date (keep a verification log).
- **unverified** — placeholder pending text; renders in every consumer
  output as unverified. There is no third state.

## Maintenance events

| Event | Action |
| --- | --- |
| New/changed foundation control | add/re-verify its row only |
| Framework edition change | column-wide re-open; schedule verification |
| Control retired | re-open every joint set it participated in |
| Verification upgrade | flip status, log person/date |
