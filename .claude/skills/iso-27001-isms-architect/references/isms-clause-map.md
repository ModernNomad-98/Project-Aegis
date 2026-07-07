# ISMS Clause Map — ISO/IEC 27001:2022 (+ Amd 1:2024)

Clause structure verified from the standard's own TOC (preview PDF, third
edition 2022-10). Finer wording claims are verification items against the
licensed text.

## Clause 4–10 artifact checklist

| Clause | Theme | Artifacts to design | Common state |
| --- | --- | --- | --- |
| 4 Context | org + parties + scope | issue analysis (incl. climate-relevance determination per Amd 1:2024 — verify exact wording), interested-party requirements, ISMS scope statement | usually missing |
| 5 Leadership | commitment, policy, roles | information security policy, top-management commitments, named role assignments | policy often exists, roles unnamed |
| 6 Planning | risk + objectives | risk assessment method, RISK REGISTER, risk-treatment process → SoA (`statement-of-applicability-author`), measurable objectives | register usually missing as a maintained artifact |
| 7 Support | resources, competence, docs | competence/awareness records, communication plan, documented-information control (version, approver, availability) | ad hoc |
| 8 Operation | run the system | operational planning of the risk process + controls; externally provided processes (→ `supply-chain-security-reviewer`) | partially exists via engineering practice |
| 9 Performance evaluation | monitor, audit, review | monitoring/measurement decisions; INTERNAL AUDIT PROGRAM; MANAGEMENT REVIEW cadence + minutes | the two most-missed artifacts |
| 10 Improvement | fix the system | nonconformity + corrective-action process with finding routing | route like postmortem actions |

## Annex A theme walk (selection via compliance-control-foundation)

Four themes (verified): **A.5 Organizational, A.6 People, A.7 Physical,
A.8 Technological**. Public theme counts (93 = 37/8/14/34) are
secondary-sourced — verify against the licensed table; avoid citing counts.

| Theme | Foundation domains that mostly cover it | Typical genuine gaps |
| --- | --- | --- |
| A.5 Organizational | risk assessment, vendor mgmt, incident response, logging policy domains | policy suite completeness, threat-intel, cloud-use policy, evidence of reviews |
| A.6 People | change mgmt (approval discipline) partially | screening, terms, awareness training records, disciplinary process |
| A.7 Physical | — (SaaS orgs largely inherit from providers) | provider-inheritance documentation; office/device physical controls |
| A.8 Technological | access control, crypto, change mgmt, logging & monitoring domains (shipped Phase 3/4 packs) | data-leakage prevention breadth, backup verification, the D8 residues (crypto design review, security alerting) |

Selection rule: per Annex A entry → include/exclude decision is the SoA's
(with 6.1.3 trace); this map only pre-sorts where mechanisms already exist
(map) vs where net-new work lands (owner + date).

## Internal audit program pattern

- Scope: the whole ISMS across the audit cycle (not one annual snapshot of
  everything — planable slices with full coverage per cycle).
- Independence: auditor ≠ owner of the audited area; small orgs
  cross-review or use external internal-audit support.
- Output: findings with owners routed via clause 10; report retained as
  evidence (→ `compliance-evidence-collector`).

## Management review pattern

- Cadence: scheduled (commonly annual + triggered by major change — set by
  the org, evidence must match the stated cadence).
- Inputs/outputs: use the clause's required agenda from the licensed text
  (status of actions, changes in issues, performance, audit results,
  risk-treatment status → decisions on improvement/resources/changes).
  Minutes must show the required elements — an unstructured status meeting
  does not satisfy the clause.

## Amd 1:2024 note

"Climate action changes" — existence/title verified via the ISO catalog
listing. Reported effect (secondary sources): clause 4.1 gains a
determination of whether climate change is a relevant issue; clause 4.2
notes interested parties can have climate-related requirements. **Verify
the inserted sentences in the licensed amendment before quoting them in
ISMS documents.**
