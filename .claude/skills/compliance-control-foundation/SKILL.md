---
name: compliance-control-foundation
description: Author the framework-agnostic common control set that ISO 27001, ISO 42001, and SOC 2 work all consumes — one catalog across access control, cryptography, change management, logging/monitoring, incident response, vendor management, and risk assessment, each control written ONCE with objective, owner, implementing mechanism, and evidence hook, then projected per framework instead of rebuilt per framework. Controls MAP to shipped implementations by name (authorization-matrix-designer, rls-policy-auditor, audit-log-architect, incident-response-runbook, and the rest of the Phase 3/4 packs) — this skill documents and maps, never rebuilds. Use when starting a compliance program, asked for a common/baseline control set, or when multiple frameworks threaten parallel control lists. Do NOT use for one framework's management system (the iso-*/soc2-* projections), control→criteria references (multi-framework-crosswalk), or gap assessment (compliance-gap-auditor).
---

# Compliance Control Foundation

## Purpose

Produce the single framework-agnostic control catalog that the framework
projections (`iso-27001-isms-architect`, `iso-42001-aims-architect`,
`soc2-trust-criteria-mapper`) consume, so the same access-control, crypto,
change-management, logging, incident-response, vendor-management, and
risk-assessment controls are written once and satisfy every framework via
`multi-framework-crosswalk` — never three parallel control lists. Each
control states its objective, owner, the concrete implementing mechanism
(named shipped skill or system artifact), its evidence hook for
`compliance-evidence-collector`, and an honest implementation status. The
batch premise (D9): most technical controls already exist in the shipped
Phase 3/4 packs — this skill MAPS them into compliance shape and exposes
what is genuinely missing; it does not re-derive or re-implement them.

## Use When

- Use when: starting a compliance/certification program and the common
  control baseline does not exist yet.
- Use when: asked for a "common control set", "control framework",
  "security control baseline", or to unify controls across ISO 27001,
  ISO 42001, and/or SOC 2.
- Use when: framework work is producing duplicate per-framework control
  lists that drift from each other.
- Do NOT use when: building one framework's management system or scoping —
  `iso-27001-isms-architect`, `iso-42001-aims-architect`,
  `soc2-trust-criteria-mapper` (they consume this catalog).
- Do NOT use when: attaching framework clause/criteria references to
  controls — `multi-framework-crosswalk`; or assessing where the org
  stands — `compliance-gap-auditor`.
- Do NOT use when: implementing or fixing a control (route to the owning
  skill, e.g. `appsec-implementer`, `secrets-identity-hardener`).

## Inputs to Inspect

1. Shipped control artifacts to map, not rebuild: the authorization matrix
   (`authorization-matrix-designer`), RLS audit + negative tests
   (`rls-policy-auditor`, `multi-tenant-security-tester`), tenant-isolation
   review (`tenant-isolation-reviewer`), secret/credential posture
   (`secrets-identity-hardener`), migration review practice
   (`secure-migration-reviewer`), audit-log taxonomy/schema
   (`audit-log-architect`), incident machinery
   (`incident-response-runbook`), supply-chain review
   (`supply-chain-security-reviewer`), threat models (`threat-modeler`,
   `ai-threat-modeler`), secure-dev review practice
   (`security-pr-reviewer`, `static-analysis-reviewer`).
2. AI-governance artifacts for the AI-facing controls: the Phase 1.5 pack
   (`ai-sdlc-operating-model`, `agent-authorization-matrix`,
   `agent-memory-governance`, `agent-governance-audit`) and
   `ai-governance-risk-reviewer` outputs.
3. Which framework(s) the org is targeting and any existing policy or
   control documents (to reconcile, not duplicate — conflicts go to
   `source-of-truth-reconciler`).
4. Known control residue from the reconciliation doc (e.g. OWASP D8:
   encryption-in-transit/at-rest design and app-config hardening are
   partial) — the catalog must carry these as honest status, not silence.

## Workflow

1. **Confirm scope and consumers.** Which frameworks will project from this
   catalog, and who owns it. No target framework or owner named → Stop
   Conditions.
2. **Inventory existing controls from shipped artifacts.** Walk the inputs
   above and list what already operates: mechanism, where it lives, who
   runs it. Map-don't-rebuild is the rule — a control that exists gets a
   pointer, never a re-specification.
3. **Normalize into the seven domains** using
   [references/common-control-set.md](references/common-control-set.md):
   access control, cryptography, change management, logging & monitoring,
   incident response, vendor management, risk assessment. Add AI-specific
   controls (AI SDLC governance, agent authority, AI risk review) as an
   eighth domain when ISO 42001 / AI RMF is in scope.
4. **Write each control once.** Per control: stable ID, objective (what
   risk it treats), description, named owner, implementing mechanism
   (named skill/system artifact — evidence it exists), evidence hook
   (what proves it operates — feeds `compliance-evidence-collector`), and
   status: implemented / partial / missing, with the residue named.
5. **Keep it framework-neutral.** No clause or criteria citations in the
   catalog — framework references are `multi-framework-crosswalk` rows so
   a framework edition change never rewrites the catalog.
6. **Mark gaps honestly.** Controls with no mechanism are `missing`, not
   aspirational prose; partial coverage names what's absent (e.g.
   encryption design review beyond key custody). Remediation ordering is
   `compliance-gap-auditor`'s job — record status here, don't prioritize.
7. **Hand off.** Catalog → projections (selection), crosswalk (references),
   evidence collector (hooks), gap auditor (baseline). Propose as a new
   versioned document; treat any existing catalog as controlled — changes
   as a reviewable diff.

## Output Format

```
COMMON CONTROL SET — <org/system> v<n> (owner: <named human>)
Consumers: <iso-27001-isms-architect | iso-42001-aims-architect | soc2-trust-criteria-mapper | ...>
Domains: access control | cryptography | change mgmt | logging & monitoring |
         incident response | vendor mgmt | risk assessment [| AI governance]
Per control:
  [CC-<domain>-<nn>] <name>
    Objective: <risk treated>
    Owner: <named human/role>
    Mechanism: <named shipped skill / system artifact / process — or MISSING>
    Evidence hook: <what proves operation> (→ compliance-evidence-collector)
    Status: implemented | partial (<residue>) | missing
Known residue carried: <e.g. crypto design review, app-config hardening>
Framework references: none here — see multi-framework-crosswalk
```

## Validation Checklist

- [ ] Every control has a stable ID, objective, named owner, mechanism (or
      explicit MISSING), evidence hook, and honest status.
- [ ] Existing implementations are mapped by name to shipped artifacts —
      nothing that exists was re-specified from scratch.
- [ ] All seven domains covered (plus AI governance when 42001/RMF in
      scope); domain gaps stated, not skipped.
- [ ] Zero framework clause/criteria citations inside the catalog.
- [ ] Known residue (e.g. D8 crypto/app-config partials) appears as
      partial/missing status, not silence.
- [ ] Catalog is versioned with an owner; changes proposed as diffs.

## Compliance Precision Rules

- SOC 2 is an AICPA **attestation** (a CPA's examination); ISO 27001/42001
  are **certifiable** management-system standards. Never write
  "SOC 2 certified" anywhere in the catalog or its consumers.
- Do not cite ISO Annex A control counts or IDs here at all — 27001 counts
  are secondary-sourced and 42001 counts conflict across sources; framework
  references live in the crosswalk with their verification flags.
- The ~60–80% cross-framework overlap figure is an industry estimate, not a
  standard-derived number — cite it only as such.
- Market rationale (SOC 2 for US procurement, 27001 via NIS2 pull, 42001 in
  EU public procurement) is positioning, not a standards claim — keep it
  out of control text.

## Gotchas

- Parallel-list drift is the failure this skill exists to prevent: the
  moment a projection writes its own control text instead of selecting
  from this catalog, the frameworks fork and evidence duplicates.
- Control theater: a policy sentence with no mechanism is not a control.
  Mechanism must name something that exists and runs — or status is
  `missing`.
- Vocabulary capture: writing the catalog in one framework's idiom (e.g.
  TSC phrasing) makes the other projections awkward — keep control
  language plain and operational.
- The rebuild temptation: the shipped Phase 3/4 skills already implement
  most technical controls; re-specifying them here creates a second source
  of truth that rots. Point, don't paraphrase.
- Owners must be humans/roles, not team abstractions — auditors ask "who",
  and so does `compliance-gap-auditor`.

## Stop Conditions

- No target framework(s) and no catalog owner can be named — stop; an
  ownerless control set is unauditable by design.
- Shipped artifacts contradict each other (e.g. two authorization sources
  disagree) — route to `source-of-truth-reconciler` before cataloging.
- Asked to implement or change a control, not document it — hand to the
  owning skill (`appsec-implementer`, `secrets-identity-hardener`, ...) and
  stop.
- Asked to assert the org is "compliant" or "audit-ready" from this catalog
  alone — that is `compliance-gap-auditor`'s parameterized assessment, and
  even it never issues an audit opinion.
- An existing controlled catalog would be overwritten — propose a diff for
  named-human approval instead (`human-approval-boundary`).

## Supporting Files

- [references/common-control-set.md](references/common-control-set.md) —
  the seven-domain control scaffold with per-domain starter controls and
  the shipped-skill mechanism map.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the compliance cluster
  (foundation vs projections vs crosswalk vs gap audit vs evidence) and
  against `threat-modeler` and `authorization-matrix-designer`.
