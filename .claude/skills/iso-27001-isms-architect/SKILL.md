---
name: iso-27001-isms-architect
description: Design ISO/IEC 27001:2022 certification readiness — the ISMS per clauses 4–10 (context incl. the Amd 1:2024 climate-relevance check, leadership, risk assessment/treatment incl. the 6.1.3 process behind the SoA, support and documented information, operation, performance evaluation incl. internal audit and management review cadence, improvement) plus Annex A selection across the four themes (A.5 Organizational, A.6 People, A.7 Physical, A.8 Technological — public control counts are secondary-sourced; verify against the licensed text). Net-new is mostly management-system artifacts (risk register, internal audit, management review); technical controls MAP to shipped skills via compliance-control-foundation. Composes statement-of-applicability-author and compliance-evidence-collector. Use for ISO 27001 readiness, building an ISMS, or 27001 scoping. Do NOT use for the SoA document itself, the AIMS (iso-42001-aims-architect), SOC 2 (soc2-trust-criteria-mapper), or readiness gaps (compliance-gap-auditor).
---

# ISO 27001 ISMS Architect

## Purpose

Design the Information Security Management System that ISO/IEC 27001:2022
certification audits examine: the clause 4–10 machinery (scope and context,
leadership, risk-driven planning, support, operation, performance
evaluation, improvement) wrapped around Annex A control selection. The
D9 premise applies hard here: for an org with the shipped Phase 3/4 packs,
most Annex A-relevant technical controls already exist — the net-new work
is the management system itself (risk register and treatment process,
Statement of Applicability via `statement-of-applicability-author`,
internal audit program, management review cadence, documented information
discipline) plus the evidence plumbing via `compliance-evidence-collector`.
This skill produces the ISMS design and certification-readiness plan; it
never asserts the org is certified — an accredited certification body
decides that.

## Use When

- Use when: asked to design, build, or overhaul an ISMS, or to prepare for
  ISO 27001 certification.
- Use when: scoping ISO 27001 — what the ISMS covers, which clauses demand
  which artifacts, what a certification timeline requires.
- Use when: an ISO 27001 surveillance or recertification cycle needs the
  management-system machinery (internal audit, management review) stood up
  or repaired.
- Do NOT use when: writing the per-control applicability document — that is
  `statement-of-applicability-author` (this skill mandates and consumes it).
- Do NOT use when: the target is the AI management system
  (`iso-42001-aims-architect`), a SOC 2 attestation
  (`soc2-trust-criteria-mapper`), or a where-do-we-stand assessment
  (`compliance-gap-auditor`).
- Do NOT use when: implementing a technical control — route to the owning
  shipped skill via the `compliance-control-foundation` mapping.

## Inputs to Inspect

1. The licensed ISO/IEC 27001:2022 text (and Amd 1:2024) — clause wording
   and the Annex A table; without it, design proceeds on verified structure
   only (clauses 4–10, four Annex A themes) with every finer claim flagged
   for verification.
2. The `compliance-control-foundation` catalog and crosswalk rows — what
   controls exist, their owners, mechanisms, and statuses.
3. Organizational context: business, interested parties and their
   requirements, legal/regulatory/contractual obligations, and whether
   climate change is a relevant issue (Amd 1:2024 amends context clauses;
   exact inserted wording is secondary-sourced — verify in the licensed
   text).
4. Existing risk artifacts: risk register if any, `threat-modeler` /
   `ai-threat-modeler` outputs as technical inputs.
5. Existing management-system artifacts: policies, any SoA, audit reports,
   management review minutes — reuse and repair beat rewrite.

## Workflow

1. **Define ISMS scope and context (clause 4).** Boundaries (org units,
   systems, locations), interested parties and requirements, internal/
   external issues — including the climate-relevance determination the
   2024 amendment adds to context analysis. Scope statement is the anchor
   for the SoA's exclusion justifications.
2. **Establish leadership artifacts (clause 5).** Information security
   policy, top-management commitments, and role/responsibility assignments
   with NAMED humans (auditors and `compliance-gap-auditor` both ask who).
3. **Stand up the risk machinery (clause 6).** Risk assessment method
   (criteria, ownership), the risk register as a maintained artifact, and
   the risk-treatment process that selects controls and produces the SoA —
   delegate the document to `statement-of-applicability-author`. Fold in
   Amd 1:2024's planning implications where the licensed text confirms
   them. Objectives with measurable criteria complete the clause.
4. **Plan support (clause 7).** Competence, awareness, communication, and
   documented-information control (versioning, approval, availability) —
   the discipline the SoA and policies live under.
5. **Design operation (clause 8).** How the risk process and selected
   controls run in production, including externally provided processes —
   the vendor surface maps to `supply-chain-security-reviewer`.
6. **Select Annex A controls via the foundation.** Walk the four themes
   (A.5 Organizational, A.6 People, A.7 Physical, A.8 Technological)
   against the catalog using
   [references/isms-clause-map.md](references/isms-clause-map.md): existing
   mechanism → map; genuine gap → net-new control with owner. Never cite
   theme counts without the licensed table in hand.
7. **Build performance evaluation (clause 9).** Monitoring/measurement
   choices, the INTERNAL AUDIT PROGRAM (scope, independence, schedule
   covering the ISMS across the cycle, reporting), and MANAGEMENT REVIEW
   cadence with its input/output agenda — the two artifacts orgs most
   often lack; both feed `compliance-evidence-collector`.
8. **Close the loop (clause 10).** Nonconformity and corrective-action
   process — route findings the same way `incident-response-runbook`
   routes postmortem actions: every finding lands with an owner or is
   explicitly accepted.
9. **Produce the readiness plan.** Artifact list with owners and dates,
   evidence program handoff, and open verification items (clause wording,
   Annex A specifics) for the licensed text.

## Output Format

```
ISMS DESIGN — <org>, ISO/IEC 27001:2022 (+ Amd 1:2024)
Scope statement: <boundaries + exclusions rationale>
Context: <interested parties → requirements; issues incl. climate-relevance determination>
Clause artifacts:
  5: policy, roles (named humans)
  6: risk method + register, treatment → SoA (→ statement-of-applicability-author), objectives
  7: competence/awareness/comms, documented-information control
  8: operational integration, externally provided processes (→ supply-chain-security-reviewer)
  9: monitoring choices; internal audit program (scope/schedule/independence); management review cadence + agenda
  10: nonconformity + corrective action routing
Annex A selection: theme-by-theme map to compliance-control-foundation (mechanism | net-new+owner)
Evidence: → compliance-evidence-collector (incl. audit reports, review minutes)
Verification items: <claims pending the licensed text — clause wording, Annex A entries/counts, Amd 1 text>
Readiness plan: <artifact → owner → date>; certification decision belongs to the accredited body
```

## Validation Checklist

- [ ] Scope statement exists and anchors every SoA exclusion.
- [ ] All clause 4–10 artifacts designed with named human owners; none
      delegated to "the team".
- [ ] Risk register + treatment process feed the SoA; the SoA document
      itself is delegated to `statement-of-applicability-author`.
- [ ] Annex A selection maps to the foundation catalog — existing
      mechanisms mapped, not re-specified; genuine gaps carry owners.
- [ ] Internal audit program and management review cadence designed with
      evidence hooks.
- [ ] Climate-relevance check included in context; its exact required
      wording flagged as a verification item, not asserted.
- [ ] Every unverified standards claim sits in the verification-items
      list; no Annex A counts stated without the licensed table.

## Compliance Precision Rules

- ISO/IEC 27001:2022 is a **certifiable** management-system standard
  (third edition, 2022-10; clauses 4–10; Annex A normative, "Information
  security controls reference" — structure verified from the standard's
  own TOC). SOC 2 is an AICPA **attestation** — never conflate.
- Annex A four themes are verified; the **93 = 37/8/14/34 theme counts are
  secondary-sourced — verify against the licensed Annex A table before
  citing**, and prefer not citing counts at all.
- **Amd 1:2024** ("Climate action changes") existence/title is verified
  from the ISO catalog; the exact inserted 4.1/4.2 sentences are from
  secondary summaries — verify before quoting.
- NIS2-driven market demand for 27001 is positioning, not a standards
  claim — keep it out of ISMS artifacts.
- Output is readiness design; "certified"/"will pass" claims are never
  made — the accredited certification body decides.

## Gotchas

- The management system IS the audit: orgs with excellent security fail
  stage-1 audits on missing risk registers, internal audits, and
  management reviews. Prioritize the clause artifacts over more technical
  hardening.
- Internal audit needs independence: whoever built the ISMS should not be
  the only person auditing it; small orgs plan cross-review or external
  internal-audit support.
- Documented-information discipline decays fastest: unversioned policies
  with no approver fail clause 7 regardless of content quality.
- A scope drawn too wide multiplies evidence surface; too narrow (carving
  out the actual product) fails customer procurement review. Scope is a
  business decision — surface it, don't default it.
- Management review is not a status meeting: it has required inputs and
  outputs; minutes must show them or the clause is unmet.
- Certification-cycle arithmetic (stage 1/stage 2, surveillance years) is
  body-specific — plan with the chosen certification body, don't assert a
  universal timeline.

## Stop Conditions

- No organizational context is available (business, parties, obligations)
  — stop; clause 4 cannot be invented.
- Top management sponsorship is absent — an ISMS without clause 5
  commitment is theater; surface this to the human before designing
  further.
- The licensed standard text is unavailable AND the task requires
  clause-exact wording or Annex A entries — deliver structure-level design
  with a verification-items list; do not fabricate specifics.
- Asked to produce the SoA, assess readiness gaps, or implement technical
  controls — hand to `statement-of-applicability-author`,
  `compliance-gap-auditor`, or the owning shipped skill respectively.
- Asked to declare the org certification-ready or "compliant" — provide
  the readiness plan and open items; the certification body decides.

## Supporting Files

- [references/isms-clause-map.md](references/isms-clause-map.md) — clause
  4–10 artifact checklist, Annex A theme-to-foundation mapping walk, and
  the internal-audit/management-review design patterns.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the compliance
  cluster (ISMS vs AIMS vs SOC 2 vs SoA vs gaps) and against
  `threat-modeler`.
