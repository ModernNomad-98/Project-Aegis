# Aegis Maturity Package — program record (owner directive 2026-11-04)

This page records the owner's 2026-11-04 direction to permanently register the program name **Aegis Maturity Package** and the readable-item naming rule in this repository, together with the program's 11 readable item names, phases and dependencies, authority and preservation boundaries, current status and next action. It is a decision/status record in the pattern of the [P0-B FAST SAVE directive record](p0b-fast-save-directive-2026-10-11.md) and [Owner decisions of 2026-10-15](OWNER-DECISIONS-2026-10-15.md): it records what the owner directed, and **it closes nothing and grants nothing**.

- **Item:** the **Aegis Maturity Package Registration and Naming Rule** (blueprint labels: WP-01 registration and program record, reference only).
- **Program id:** `AEGIS-MATURITY-PACKAGE-2026-11-04` — an administrative label only, not an item naming scheme.
- **Authoritative naming rule:** the permanent rule appended to [AGENTS.md](../../AGENTS.md) by the same change that adds this page; that rule governs if this page and the rule ever diverge.
- **Class:** DOCUMENTED POLICY. **No mechanical enforcement exists or is claimed**; the rule is checked procedurally by the independent plan, implementation and final reviewers under the [delivery workflow](../delivery-workflow.md).

**Model attribution (the 2026-10-13 rule).** This page was drafted by a dedicated **DeepSeek** teammate (`packaging-host`, DeepSeek Harness; configured route `deepseek-flash`; serving model not observable), the Stage C implementing agent for the registration slice, from the owner's captured instruction and the session name register. Nothing in this page claims the owner typed into this repository.

## S1. Source, authority and provenance

- **Source.** The owner's current direct instruction of **2026-11-04**, received in the program session, captured in the session name register `_A/strengthening-program-2026-11-04/AEGIS-MATURITY-PACKAGE.md`, which is a workspace record **not retrievable from this repository**. The owner's words, verbatim:

  > "name this Aegis improvement work as "Aegis Maturity Package". Items being worked on must have a readable name, not AM3-xx. Register this into the repo and rules permanently"

- **Capture note.** The session register and the Lead's capture are the verbatim source used here. A task-tracking copy uses single quotation marks around the program name; that is a tracking-field capture style difference only and does not change the instruction's content.
- **Transcription authority.** Per the [approval register preamble](../approvals/APPROVAL_REGISTER.md) (lines 12-13), **"Current direct user instructions are valid source evidence before transcription and do not need repeated consent."** The registration therefore rests on the current owner instruction itself, not on a pre-existing grant.
- **What this page is not.** It is a record, not an authorization. **It grants nothing by itself.** The [approval register](../approvals/APPROVAL_REGISTER.md) remains the documentary grant register; registration is not authorization for any push, review, merge, publication, deployment, spend or credential action.

## S2. Naming rule (summary; authoritative copy in AGENTS.md)

The authoritative, normative copy of the rule is the permanent rule appended to [AGENTS.md](../../AGENTS.md), titled **"Source-library owner rule: Aegis Maturity Package naming and item names (owner directive 2026-11-04 — permanent)"**. In summary:

1. The improvement work is always called the **Aegis Maturity Package**; an abbreviation-only label is not the program's name.
2. Every item being worked on has a readable, plain-language name. Code-like item names such as `AM3-xx`, `AM3-01` or `WP-02A` are prohibited as item names.
3. Where an identifier is operationally unavoidable (a file slug, a task-board field, a technical work-package label on a control), it appears **beside** the readable name, never instead of it.
4. Existing decision, gate, stage and approval identifiers (`D-*`, `Q-*`, `H*`, `MG*`, `SD-*`, `AEGIS-APR-*`, and blueprint work-package labels) remain valid references, but they are never used as an item's name and carry the plain-English description the existing owner preference requires when reported (AGENTS.md line 153 preference).
5. Owner-facing reports, status lines, to-do panel entries, ETA tables and pull-request summaries use the readable name plus a one-line description. Task-board ids are tracking fields only.
6. The canonical list of readable item names is maintained **only** in this page (section S3); do not fork a second maintained list into AGENTS.md or another entry point.
7. The rule changes no review stage, gate, approval requirement, protected path, evidence obligation, merge condition or bound field, and grants no new authority to plan, edit, test, commit, merge, publish, deploy, dispatch, spend, access credentials or remove a skill. It takes effect when its change is merged to the default branch; until then it is staged in the local isolated worktree and grants nothing.

## S3. The 11 readable item names

This table is the single maintained copy of the program's readable item names. It is copied from the session name register with its characters preserved (including em dashes).

| # | Readable item name | What it is (one line) | Blueprint label (reference only) | Phase |
|---|---|---|---|---|
| 1 | **Program Baseline and Registration** | Verified starting point, exact-tree baseline, preservation baseline, queue/ownership map and this registration | WP-01 + program record | Phase 0 baseline registered; Stage C local implementation complete; Stage D–F and merge pending |
| 2 | **Requirements-to-Evidence Conformance Catalog** | Versioned catalog that ties each requirement to its authoritative source, enforcing mechanism and observed evidence, with deterministic checks | FND-01 | Phase 1 |
| 3 | **Consumer Packaging Manifest and Read-Only Verification** | Complete distributed-payload manifest, dependency closure and a verify path that never repairs or mutates a target | WP-02 | Phase 1 |
| 4 | **Host Compatibility Qualification** | Named host/product/OS configurations with explicit supported vs unsupported capability evidence | WP-03 | Phase 1/2 |
| 5 | **Verification and Skill-Preservation CI Check** | Suite inventory plus a check that reports/blocks any lost, hidden or undiscoverable skill; never prunes | WP-04 | Phase 1 |
| 6 | **Behavioral and Consumer-Outcome Evaluation** | Reproducible fixtures, graders and scoped effectiveness evidence for selected workflows | WP-05 | Phase 2/3 |
| 7 | **Live-Evaluation Admission and Budget Recovery** | Reconciliation of prior live-eval work, admission/binding rules and uncertain-exposure recovery — no live run | WP-06 | Phase 2 |
| 8 | **Maintainability Measurement and Refactoring** | Measured change/review-cost baseline and one evidence-backed extraction with equivalence tests | WP-07 | Phase 1/2 |
| 9 | **AI-Product Engineering Profile** | One bounded AI-dependent reference workflow composed from existing skills | WP-08 | Phase 2/3 |
| 10 | **Release Evidence and Documentation** | Provenance-bound, privacy-reviewed release claims, current docs and full-catalog guided entry | WP-10 | Phase 3 |
| 11 | **Bounded Real-Execution Integration** | Separately authorized read-only then one reversible action in a disposable target — NOT authorized now | WP-09 | Owner-gated |

## S4. Phases and dependencies

| Phase | Content |
| --- | --- |
| Phase 0 | Program baseline and registration: verified exact-tree baseline, preservation baseline, queue/ownership map and this registration — **COMPLETE** |
| Phase 1 | Planning and first implementation slices for the Phase 1 items in the table above |
| Phase 2 | Independent plan audits and the Phase 2/3 items' planning slices |
| Phase 3 | Implementation slices for the Phase 3 items |
| Phase 4 | Implementation audit and validation |
| Phase 5 | Final review and local freeze |
| Phase 6 | Owner-gated remote delivery — **not authorized** by the current local-only directive |

Milestone dependencies (from the program goal record): M0 baseline; M1 requirements-to-evidence conformance catalog; M2 consumer packaging manifest and read-only verification; M3 verification and skill-preservation CI check; M4 host qualification and evaluation fixtures; M5 maintainability, AI-product profile and release evidence; M6 live admission / real-execution integration, under separate owner scope.

**ETA pointer.** Item-level and phase-level estimates live in the session workspace record `_A/strengthening-program-2026-11-04/ETA-TRACKER.md`, a workspace record **not retrievable from this repository**. No ETA is restated here as a commitment, and no ETA is invented on this page.

## S5. Authority and preservation boundaries

Authorized now, per the owner directive recorded in the program goal record: read and reconcile local and read-only remote facts; maintain local goal, planning, evidence and checkpoint records; prepare bounded Stage A packets; obtain independent review from genuinely available holders; implement reversible local changes inside an accepted slice in isolated local worktrees; execute inspected bounded offline tests with existing tooling; make local commits with truthful non-owner attribution; correct verified failures and repeat review/validation.

Not authorized: pushing; creating or updating remote pull requests, issues, comments or reviews; dispatching hosted workflows; creating scheduled tasks; merging, publishing, releasing or deploying; paid model calls or spend; new credential access, rotation or wider permissions; repository settings or branch protection; overriding specific owner holds or protected-path requirements; overwriting another agent's work; deleting, disabling, hiding, renaming or consolidating any skill.

**Protected surfaces** (unchanged by this record): `.claude/skills/**` and their references/evals; `docs/skills-catalog.md`; the root `README.md` roster; `tools/skills-manifest.json`; `AGENTS.md` (this change is the owner-directed exception, bounded by independent plan audit, accepted plan and Lead authorization); `CLAUDE.md`; `docs/delivery-workflow.md`; `docs/approvals/APPROVAL_REGISTER.md`; `.github/**`; `artifacts/audits/**`; plan-preservation CI wiring (owner constraint); `local-base/**`; other holders' scopes and owner files under `_A/`.

**Skill-preservation invariant.** Frozen baseline: 255 skill directories / 255 `SKILL.md` (254 named skills + `_template`); 996 skill files; 215 with references; 255 with `evals.json`; 254 with `trigger-evals.json`; entrypoint manifest 254 entries; catalog and README coverage 254/254; validator `OK: 254 skill(s) valid, 0 warning(s)`. This slice edits no skill, catalog, manifest or discovery surface and adds no remove/uninstall/prune/cleanup path. Any reduction, omission or availability change is a **STOP** condition.

## S6. Status and next action (as of this record's drafting)

M0 (program baseline and registration) is **registered, not merged**: the baseline record exists, but Stage D implementation audit, Stage E validation, Stage F final review and merge are pending, so this item is not “complete”. Four Stage A packets were delivered for the first item slices (requirements-to-evidence conformance; consumer packaging manifest and read-only verification; verification/evaluation; maintainability/AI-product profile/release evidence). The registration packet was independently audited at Stage B and **ACCEPTed**, so the registration slice is at **Stage C — local implementation complete; Stage D–F and merge pending**. The commit remains local until a separately authorized merge; no push, PR, review posting, merge or publication is authorized by this page.

**Next action.** Complete the Stage C commit for exactly the three registration paths (`AGENTS.md` append, this page, one `docs/README.md` pointer), re-run the validator and Markdown link checker at the exact candidate, then hand the candidate to independent Stage D review. Remote/owner-gated actions remain untouched.

## S7. Owner-held items

Publication is held (program decision D-P5); live or paid evaluation remains unauthorized (D-P4); real-execution integration remains out of scope (D-P6); the first supported host/profile choice remains owner-held (D-P1); repository settings/branch-protection changes are proposal-only (D-P3); **no skill removal is recommended and none is authorized (D-P7)**. The consolidated program decision queue is the session workspace record `_A/strengthening-program-2026-11-04/DECISION-QUEUE.md`, **not retrievable from this repository**. Pre-existing held pull-request families (tracking references Q-CNC-02 and Q-994-M) are not re-asked or answered by this record. The `OD-AMP-1` other-entry-point question is a Lead/plan scope choice at this stage; the owner may optionally confirm it later.

## S8. Enforcement and limits

The naming rule is a documented rule: no machine check verifies that a report or item actually uses a readable name, and none is claimed. The independent plan, implementation and final reviewers check it as part of their existing duties under the delivery workflow. This page is a record, not a gate: it changes no stage, gate, receipt, bound field or required check. The validator and Markdown link checker treat it as documentation only; its presence and this page's presence are checkable only as text, and their semantic use remains procedural. A malformed or code-like report is corrected by its author, not by a machine gate.

**Timestamp:** 2026-11-04 14:32 PST (2026-11-04T22:32Z) — PST + UTC (America/Los_Angeles).
