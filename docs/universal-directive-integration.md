# Universal agent directive integration — GitHub Pages, security governance and mock retirement

**Status:** normative operational detail for the owner directive effective **2026-11-01** in the Project Aegis source library. This page is the single detailed rendering of the directive's operational requirements. It is a documentation and instruction change only: it grants **no** merge, pull-request publication, deployment, production-change, destructive-delete, credential, settings or paid authority, and it does not relax any existing approval boundary.

**Binding record.** Directive `UNIVERSAL-DIRECTIVE-2026-11-01.md` — 6,623 bytes, sha256 `09362db4c5b3a510d26568e96c7536a22f6563bd31e21a2f3c5010eacfb748d3`; effective 2026-11-01; source: owner message in the recorded session; governance: Project Aegis ZT-AIED and Aegis SCIF. The binding entry point for agents is [AGENTS.md](../AGENTS.md); the seven-stage delivery rule is [docs/delivery-workflow.md](delivery-workflow.md). Stage A/B evidence for this integration: plan 16,365 bytes sha256 `ba67caef15e14c02bfaf747969475ab122e87da1d3472177c0e79495e5c9b577`, evidence map `EVIDENCE-MAP.md` 11,409 bytes sha256 `58ee297ae69c463211fc18845e5c5ce04b30258ba4ae60117548f796e9951c3a`, **prior** independent Stage B audit 4,528 bytes sha256 `212f7925a32b0fa453fdc2d98cc227a9f61c787d64c6a7db182b52490a8ba71f` (prior-revision ACCEPT) and Stage B addendum 4,671 bytes sha256 `200d912f25182c6c1fca5013244e7d4256e7f3b4d72b49b4ee17335d6a01c3fd` (ACCEPT corrected Stage A/B authority evidence) (all in the owner's local work package, not repository files). Consumer and future-repository integration remains **queued / UNRUN** (§9).

## 1. Scope, precedence and authority

- **Repository scope of this implementation.** This page and the AGENTS.md binding section are the complete Stage C implementation in the canonical Project-Aegis repository. They do not change code, skills, registry, workflows, settings, approval records or any consumer copy.
- **Universal applicability is not inherited authority.** The directive applies to every existing and future project, but each repository must verify its own identity, instructions, ownership, approvals, environment and deployment architecture, and integrate the directive through its own authorized contribution process. No permission, approval or exception from one repository carries into another.
- **Higher-priority controls are preserved.** This integration preserves all existing sections and controls: [AGENTS.md](../AGENTS.md), the `CLAUDE.md` import, [docs/delivery-workflow.md](delivery-workflow.md), [docs/ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md](ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md), [docs/manual-only-policy.md](manual-only-policy.md) and the [owner approval register](approvals/APPROVAL_REGISTER.md). No section is removed, weakened, merged away or reordered.
- **Conflict rule.** Where the directive appears to conflict with a higher-priority repository control or an active owner decision, the higher-priority control governs; record the conflict and escalate the genuine conflict rather than silently weakening either source. Do not use the directive to bypass the seven-stage order, manual-only skill rules, the approval register, security controls or a hold.
- **No new authority.** Nothing in this page or the AGENTS.md section authorizes publication, deployment, merge, production SQL, destructive deletion, credential use, settings changes or spending. Those actions stay with the applicable owner/authority and existing gates.
- **No fabricated evidence.** Every requirement below is carried out with recorded evidence; unverified or inaccessible items are labeled `UNRUN` or `UNKNOWN`, never described as zero or passed.

## 2. GitHub Pages standard (evaluation and appropriate use)

GitHub Pages is the preferred hosting option for suitable **static public content**: landing pages, documentation, installation and tutorial content, release notes, onboarding material, synthetic-data demonstrations and public API documentation. Use it when it is technically appropriate for the content and the repository; do not replace working production hosting merely because Pages exists.

Pages is **not a backend**, not a security boundary for private data, and not a substitute for authentication, authorization or tenant isolation. Verify the actual deployment URL before making any live-site claim; an evaluated-but-not-checked URL is `UNRUN`. A private repository does not by itself make a Pages site private. No Pages site or deployment is authorized or created by this integration.

## 3. Mandatory security checklist before any Pages publication or update

All of the following must be completed and recorded before publishing or updating a Pages site. Items that cannot be evidenced are `UNRUN`/blocked, not assumed.

1. **Visibility:** verify the repository and intended site are truly public and that public exposure is intended; never equate a private repository with a private site.
2. **Artifact scan:** scan every deployed artifact (documents, images, examples, generated assets) for credentials/secrets, customer data, internal infrastructure details and sensitive metadata.
3. **Transport and browser protections:** HTTPS enabled, no mixed content, and no claim about the live URL without checking it.
4. **Supply chain and permissions:** pin and validate dependencies and GitHub Actions; use least-privilege Pages/deployment permissions (no `write-all`); validate the build.
5. **Backend isolation:** backend authentication and tenant isolation are unaffected; Pages is static content and never a security boundary.
6. **Synthetic data only:** no real customer data, secrets, internal endpoints, raw transcripts or personal data.
7. **Custom domain/DNS:** if a custom domain is used, check DNS and subdomain-takeover risk and document the owner.
8. **Independent review and approval:** independent security review plus an explicit, authorized deployment approval.
9. **Verification after deploy:** a passing CI run is not production-security evidence; verify the deployed revision and URL after deployment.
10. **Record and rollback:** record evidence, unresolved risks and a rollback/disable plan before relying on the site.

## 4. Mandatory retirement of obsolete mocks and placeholders

For work in the assigned scope, identify obsolete mockups, mocks, placeholders, temporary demonstrations, simulated integrations, hardcoded sample responses and shortcuts. Remove obsolete **production-facing** mock behavior once the real replacement is approved, implemented, independently verified, and the mock is no longer needed by production, supported development, required tests or rollback.

Cleanup includes removing mock components and dead code, unused imports/dependencies/config, outdated screenshots/preview assets and misleading documentation; updating tests to the real implementation; and running regression checks. Legitimate **test mocks, synthetic fixtures, contract/security regression tests and rollback artifacts are retained** with their justification.

Do not rewrite history to erase mocks, and preserve audit evidence and retention. Do not delete public deployments, production resources or shared files without authority. Approval of a mockup is not evidence that its replacement is implemented.

## 5. One-time retroactive mock/placeholder baseline audit

**Scope.** Mockups, mocks, placeholders, temporary demos, simulated integrations, hardcoded sample responses and shortcuts created **before 2026-11-01 00:00 America/Los_Angeles**, in every project this repository can access (including prior agents and sessions): current trees, git history, pull requests/issues, work artifacts, design documents, deployments and evidence directories. Inaccessible sources are `UNKNOWN`; the audit does not infer them.

**Inventory categories.** UI/UX mockups and prototypes; mock APIs and simulated responses; temporary or hardcoded data; placeholder dashboards and metrics; mock integrations, authentication and authorization; demo components and routes; old static previews/Pages demos; unused images, CSS, scripts and assets; obsolete flags and configuration; demo-only code that has since been implemented; misleading documents and screenshots.

**Row schema.** `id, repository, path/artifact, type/category, created date/evidence, current use, replacement feature + approval/merge/deployment evidence, independent verification evidence, tests/regressions, rollback/dependency assessment, owner, retention need, classification, next action, evidence sha256`.

**Classifications.** `REMOVE` — replacement approved, implemented and independently verified; removal authorized; no regression or rollback loss. `RETAIN` — required by tests, development, rollback or a supported use, with the justification recorded. `BLOCKED` — a genuine unresolved approval, risk or dependency. `VERIFY` — insufficient evidence to classify. `UNKNOWN` — evidence is unavailable; never silently zero or removed. A prior agent's completion report alone is not grounds for `REMOVE`.

**Acceptance.** Every inventoried item carries a disposition; authorized removals are executed and validated; exceptions record an owner and next action; evidence gaps are recorded; history is not rewritten; audit evidence is retained. The audit is complete only when all items and removals are dispositioned and verified; partial inventories remain open work. Cleanup uses the project's ordinary authorized workflow, and rollback is retained until safe.

## 6. New-mock policy

Every new mock, placeholder or simulated integration is registered with its purpose, owner, scope, replacement plan, lifecycle state and expiry/review date. Legitimate test mocks, synthetic fixtures, contract/security regression tests and rollback artifacts are `RETAIN` with justification. Production-facing mock behavior is removed once the replacement is approved, implemented, independently verified and no longer needed. Every completed feature includes a mock-retirement assessment; a green CI run alone is not replacement evidence.

## 7. Required coordinator report

One durable report per project/release records: **Repository** (verified identity); **GitHub Pages** (existing/eligible/ineligible/proposed, with no live claim without a checked URL); **Security** (checks, results, unresolved risks); **Historical mocks** (pre-2026-11-01 inventory); **New mocks** (inventory and lifecycle); **Implementations** (verified replacement evidence); **Cleanup status** (removed/retained/blocked/pending); **Tests** (regression/acceptance); **Aegis skills** (the exact skills actually applied, with evidence); **Approvals** (recorded project-specific authorization); **Outstanding work** (blockers, owners, next actions). The report labels `UNRUN` and `UNKNOWN` honestly and does not fabricate completion.

## 8. Stage mapping and holds (Aegis SCIF)

| Stage | How this integration touches it | Hold |
| --- | --- | --- |
| A PLAN | A plan for a directive-relevant change carries the Pages, security, mock-retirement, audit and reporting requirements by reference to this page; the plan records delivery classification and acceptance criteria. | Merge/deploy/publication authority is not granted by the plan. |
| B INDEPENDENT PLAN AUDIT | The independent auditor tests the plan's directive coverage and the captured-revision binding. | Auditor does not implement. |
| C IMPLEMENT | This Stage C change implements only the three paths: AGENTS.md binding section, this page, and one delivery-workflow cross-reference. | No source, skill, registry, workflow or settings change. |
| D INDEPENDENT IMPLEMENTATION AUDIT | A different agent checks the implementation against the accepted plan and criteria. | Read-only; no self-approval. |
| E VALIDATE | Existing repository checks only; every unrun check is named `UNRUN`, never absorbed as a pass. | No new CI gate is invented here. |
| F FINAL INDEPENDENT PR REVIEW | The final reviewer checks the delivered documentation, the directive compliance record and the PR-body evidence. | Reviewer does not author or merge. |
| G MERGE | Only a separate holder with applicable authority merges, after all gates and the exact-head review. | Merge/deploy/publication remain reserved. |

The directive's overall release-and-cleanup sequence is: Discover → Plan → Review → Implement → Test → Independently verify → obtain required release approval → Deploy → Verify → retire obsolete mocks → Revalidate → Report. Implemented, merged, deployed and production-verified are distinct states and must not be conflated. Do not remove rollback prematurely.

## 9. Consumer and future rollout (queued / UNRUN)

| Target | Current evidence | Status | Hold / next action |
| --- | --- | --- | --- |
| Project-Aegis canonical source | This repository at the implemented commit | **In scope for this implementation** | Existing A-G review; publication/merge reserved. |
| `aegis-consumer-proof-2` | Evidence-only in the owner's workspace (PR #1 Stage F evidence; no local checkout; README scaffold; no Pages evidence) | **QUEUED / UNRUN** | The consumer project owner must provide/authorize a checkout and integrate through that project's own rules; no inherited approvals or authority. |
| Future adopting projects | No repositories or instruction surfaces identified | **QUEUED / UNRUN** | Each project's owner schedules its own A-G integration; no universal rollout is implied. |

The audit/observation scope is wider than this implementation, but Stage C implementation remains bounded to canonical Project-Aegis. Live Pages settings, URLs, deployments and an authenticated settings/API check are `UNRUN` and reserved.

## 10. Evidence, labels and change control

- **Unrun is not passed.** Every check that did not run, every URL/settings value not checked and every source not accessible is recorded as `UNRUN`/`UNKNOWN` with what would resolve it.
- **No duplicate work.** Apply the directive without disrupting higher-priority authorized work; keep blocked work in the durable decision queue and continue unrelated authorized work.
- **No self-approval.** The author of this page does not audit or merge it; the seven-stage separations apply.
- **Change control.** Changes to this page follow the repository's authorized contribution process. Do not weaken higher-priority controls or the holds above; genuine conflicts are escalated to the owner rather than resolved by silent edits.
- **Directive drift.** If the source directive changes, re-capture it, compare against this page, and route the difference through the authorized process; do not silently retarget this page to a newer or remembered directive.

## Related instruments

- [AGENTS.md](../AGENTS.md) — binding agent instructions; the directive binding section is the entry point.
- [docs/delivery-workflow.md](delivery-workflow.md) — seven-stage rule, stage dispositions, handoff and merge receipt.
- [docs/ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md](ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md) — zero-trust engineering discipline preserved by this integration.
- [docs/manual-only-policy.md](manual-only-policy.md) — manual-only skill policy; unaffected.
- [owner approval register](approvals/APPROVAL_REGISTER.md) — recorded owner grants and lifecycle events; this page does not amend it.
