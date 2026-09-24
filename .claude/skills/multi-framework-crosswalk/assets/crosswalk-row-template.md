# Crosswalk Row Template

Use this template when the [multi-framework crosswalk skill](../SKILL.md)
asks for a control mapping. The reviewer fills one row from framework text
actually in hand; an unchecked cell stays `unverified`. `TSC` means Trust
Services Criteria, `PoF` means Points of Focus, and `AICPA` means American
Institute of Certified Public Accountants. `AI RMF` means Artificial
Intelligence Risk Management Framework; `fn` is one of its named functions.
`CC-<dom>-<nn>` is a placeholder for a foundation control identifier,
with a domain and number supplied by the owning control set.

## Header (mandatory)

```
CONTROL CROSSWALK — <org> v<n>   Date: <YYYY-MM-DD>   Owner: <named human>
Editions pinned:
  ISO/IEC 27001:2022 [+ Amd 1:2024]   — Annex A table in hand: yes/no
  ISO/IEC 42001:2023                  — Annex A table in hand: yes/no
  TSC 2017 (revised PoF 2022, AICPA)  — criteria text in hand: yes/no
  NIST AI RMF 1.0                     — Core text in hand: yes/no (note: RMF 1.0 under revision — check current)
Rule: cells fill ONLY from text in hand; otherwise `unverified`. No memory-recalled IDs.
Coverage level: DESIGN ONLY unless organizational implementation and operation evidence is separately verified and cited.
```

## Row

```
| Control (foundation) | 27001 Annex A | SOC 2 TSC | 42001 Annex A | AI RMF fn | Notes |
| --- | --- | --- | --- | --- | --- |
| CC-<dom>-<nn> <name> | <ref> · FULL/PARTIAL(<residue>)/NONE design coverage · text verified/unverified | same shape | same shape | GOVERN/MAP/MEASURE/MANAGE/n-a | joint design coverage, edition notes; operated evidence if claimed |
```

## Satisfaction vocabulary

- **FULL** — the control design covers the requirement's substance. Label
  this design coverage; claim operational satisfaction only after separately
  verifying organizational implementation and evidence. Not "mostly."
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
