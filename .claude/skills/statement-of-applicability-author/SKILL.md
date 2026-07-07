---
name: statement-of-applicability-author
description: Author the Statement of Applicability — the ISO-mandatory document tying every reference control to a per-control inclusion or exclusion justification through the 6.1.3 risk-treatment process; serves BOTH ISO 27001:2022 (Annex A controls) and ISO 42001:2023 (Annex A control objectives) from one procedure. Rows record include/exclude with a risk-or-obligation trace, implementation status mapped to the compliance-control-foundation catalog, and controlled-document metadata (version, named approver). Requires the licensed standard's actual Annex A table — never reconstructs entries or counts from memory or secondary sources. The largest net-new ISO artifact SOC 2 lacks. Use when asked to write or update an SoA, or when ISO 27001/42001 certification prep reaches the applicability document. Do NOT use for the whole management system (iso-27001-isms-architect / iso-42001-aims-architect), the control catalog (compliance-control-foundation), or cross-framework references (multi-framework-crosswalk).
---

# Statement of Applicability Author

## Purpose

Produce the Statement of Applicability (SoA) — the document ISO
certification audits open first: for every control in the standard's
Annex A, is it applicable to this organization, why (traced to the 6.1.3
risk-treatment process or an obligation), and what is its implementation
state. One procedure serves both certifiable ISO standards — ISO 27001:2022
(Annex A "Information security controls reference", normative) and
ISO 42001:2023 (Annex A "Reference control objectives and controls",
normative) — because the SoA logic is identical even though the control
lists differ. Implementation status maps to the
`compliance-control-foundation` catalog so the SoA points at real
mechanisms, not aspirations. The SoA is a controlled document: this skill
authors proposals and diffs, with versioning and a named approver — it
never silently rewrites an operating SoA.

## Use When

- Use when: asked to write, draft, or update a Statement of Applicability
  for ISO 27001, ISO 42001, or both.
- Use when: ISO certification prep reaches the point of deciding which
  Annex A controls/objectives apply and justifying exclusions.
- Use when: the risk-treatment process (6.1.3) has produced treatment
  decisions that must be reflected as control applicability.
- Do NOT use when: designing the management system around the SoA —
  `iso-27001-isms-architect` / `iso-42001-aims-architect` (they mandate
  and consume the SoA; this skill writes it).
- Do NOT use when: authoring the framework-agnostic control catalog
  (`compliance-control-foundation`) or mapping controls across frameworks
  (`multi-framework-crosswalk`).
- Do NOT use when: SOC 2 work — SOC 2 has no SoA; scoping lives in
  `soc2-trust-criteria-mapper`.

## Inputs to Inspect

1. **The licensed standard text's Annex A table** for the target
   standard(s) — the actual control IDs, titles, and (for 42001) control
   objectives. This input is hard-required; see Stop Conditions.
2. Risk-treatment outputs: the risk register and treatment decisions the
   6.1.3 process produced (technical inputs from `threat-modeler` /
   `ai-threat-modeler`; for 42001, AI risk and impact assessments from
   `iso-42001-aims-architect`'s 6.1.2/6.1.4 machinery).
3. The `compliance-control-foundation` catalog and
   `multi-framework-crosswalk` rows — what mechanisms exist for each
   included control and where they live.
4. Legal/contractual/regulatory obligations that force inclusion
   independent of risk appetite.
5. Any existing SoA (version, approver, last review) — updates are diffs
   against it, never replacements.

## Workflow

1. **Confirm target standard(s) and obtain Annex A.** ISO 27001:2022,
   ISO 42001:2023, or both (two SoAs or one combined document with
   per-standard columns — org's choice, recorded). Without the licensed
   Annex A table, stop.
2. **Assemble the row skeleton** from the actual Annex A entries using
   [assets/soa-template.md](assets/soa-template.md). Never paraphrase
   control titles — quote them as the standard writes them.
3. **Decide applicability per control.** Include when a risk-treatment
   decision selects it or an obligation requires it; exclude only with a
   justification that survives an auditor ("no mobile app development" —
   concrete, verifiable), traced to the risk assessment scope.
4. **Justify inclusions by trace.** Each included control cites the risk(s)
   it treats or the obligation demanding it — "best practice" is not a
   justification; that's how SoAs bloat into unauditable checklists.
5. **Record implementation status per included control** by mapping to the
   foundation catalog: implemented (mechanism named) / partial (residue
   named) / planned (owner + date). The SoA never claims implemented
   without a mechanism to point at.
6. **Apply controlled-document discipline.** Version, date, author, named
   approver, review cadence; changes to an existing SoA are proposed as a
   reviewable diff with rationale per changed row
   (`human-approval-boundary` for approval).
7. **Hand off.** SoA → the owning ISO projection (internal audit and
   management review consume it), `compliance-evidence-collector`
   (included controls need operating evidence), `compliance-gap-auditor`
   (planned/partial rows are gaps with owners).

## Output Format

```
STATEMENT OF APPLICABILITY — <org>, <ISO/IEC 27001:2022 | ISO/IEC 42001:2023 | both>
Version <n> | Date | Author | Approver: <named human> | Review cadence: <e.g. annual + on major change>
Source: Annex A of the licensed standard text (edition pinned) — entries quoted, never reconstructed
Per Annex A entry:
  <Annex A id — title as published>
    Applicable: yes | no
    Justification: <risk-treatment trace (risk id) | obligation | concrete exclusion rationale>
    Status: implemented (<mechanism from compliance-control-foundation>) | partial (<residue>) | planned (<owner, date>)
    Evidence hook: <→ compliance-evidence-collector>
Exclusions summary: <count + one-line rationale each>
Open items: <controls awaiting risk-treatment decisions>
```

## Validation Checklist

- [ ] Every row comes from the licensed standard's Annex A table; zero
      entries reconstructed from memory or secondary sources.
- [ ] Every inclusion traces to a risk-treatment decision or named
      obligation; every exclusion has a concrete, verifiable justification.
- [ ] Implementation status maps to real mechanisms in the foundation
      catalog; no "implemented" without a named mechanism.
- [ ] Controlled-document metadata complete: version, author, named
      approver, review cadence.
- [ ] Updates delivered as diffs against the existing SoA with per-row
      rationale — no silent rewrite.
- [ ] 42001 rows treat Annex A entries as control objectives and controls
      per that standard's own structure, not as 27001 clones.

## Compliance Precision Rules

- The SoA obligation and its tie to the risk-treatment process come from
  clause 6.1.3 — verify the exact clause wording against the licensed
  standard before quoting it.
- **Never state ISO 27001 Annex A control counts** (the widely cited
  93 = 37/8/14/34 across A.5 Organizational / A.6 People / A.7 Physical /
  A.8 Technological is from secondary sources) **without verifying against
  the Annex A table itself**; never state ISO 42001 Annex A counts at all
  from memory — secondary sources conflict, so counts come only from the
  standard text in hand.
- ISO 27001/42001 are **certifiable** management-system standards; SOC 2 is
  an AICPA **attestation** with no SoA — never import SoA language into
  SOC 2 deliverables or vice versa.
- The SoA asserts applicability and status; it never asserts that the
  organization "is certified" or "will pass" — the accredited certification
  body decides.

## Gotchas

- Include-everything SoAs are self-inflicted audit scope: every included
  control must be implemented and evidenced. Include by risk trace, not by
  fear of exclusions.
- Exclusion justifications age: "no remote work" from 2019 fails today's
  audit. The review cadence exists to catch these; stale justifications
  are findings.
- Copying another org's SoA imports their risk assessment; auditors ask
  for YOUR 6.1.3 trace and the mismatch shows immediately.
- For a combined 27001+42001 document, keep per-standard applicability
  distinct — an AI control objective excluded for 42001 reasons says
  nothing about a 27001 control, and vice versa.
- "Planned" rows without owner and date are decoration; auditors read them
  as unmanaged gaps.
- The SoA is not the risk assessment — it consumes treatment decisions. If
  the risk register doesn't exist yet, the SoA is blocked, not improvised.

## Stop Conditions

- The licensed standard's Annex A table is not available — stop and say
  so; reconstructing Annex A entries from memory or vendor summaries
  produces a certifiably wrong document.
- No risk-treatment output exists to trace inclusions to — route to the
  owning ISO projection to run the 6.1 machinery first.
- Asked to rewrite or replace an operating SoA in place — produce a diff
  proposal for the named approver instead (`human-approval-boundary`).
- Asked to declare exclusions for controls whose risk relevance is
  genuinely undecided — surface the open decision to the risk owner; the
  SoA records decisions, it does not make them.
- Asked to write an SoA "for SOC 2" — explain SOC 2 has no SoA and hand
  scope questions to `soc2-trust-criteria-mapper`.

## Supporting Files

- [assets/soa-template.md](assets/soa-template.md) — the SoA row template,
  controlled-document header, and justification patterns (inclusion by
  risk trace / by obligation; exclusion rationale tests).
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the compliance
  cluster (SoA vs ISMS/AIMS design vs catalog vs crosswalk) and against
  `soc2-trust-criteria-mapper`.
