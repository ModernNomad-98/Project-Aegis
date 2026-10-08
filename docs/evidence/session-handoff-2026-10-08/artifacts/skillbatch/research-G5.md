# G5 research: Phase 4 security expansion (topics, not yet named skills)

Helper: SEC helper (G5 only). Stage A support research, planning only. No repo file written, no commit, no GitHub write.
Started: 2026-10-08T17:11:40Z (`date -u`). Finish timestamp: see the handback report (taken after this file was written).

## 0. Base, method, skills used

- **Base.** `git ls-remote origin refs/heads/main` -> `5228977920ee479e1fe1ec6b8d56f8fc24c14947`. The local checkout HEAD
  was `c060a7cb` (behind main), so every read below is from a fresh `git archive 52289779` extract at
  `$S/skillbatch/g5-tree/`. Role A confirmed: `README.md` line 1 `# Project Aegis`; `docs/skills-catalog.md`,
  `scripts/validate-skills.py` and `artifacts/audits/skill-contract-audit-baseline.json` are present.
  `python3 -B scripts/validate-skills.py` -> `OK: 195 skill(s) valid, 0 warning(s)` (196 directory entries including `_template`).
  Earlier helpers' `desc*.txt` were NOT reused: descriptions were re-dumped with `yaml.safe_load` into
  `$S/skillbatch/g5-work/desc.json` (196 entries; 30 have `disable-model-invocation: true`).
- **Overlap method.** (1) a keyword sweep over all 195 shipped descriptions; (2) a body sweep of `SKILL.md`, `references/`
  and `evals/` for each topic's terms; (3) a full read of the nearest neighbors' Purpose, Use When, Workflow and Security Rules;
  (4) a read of the neighbors' `trigger-evals.json` cases that already route the topic's prompts.
- **Aegis skills used (dogfood).**
  - `prioritization-frame-picker`: applied to rank the topics. Why now: the owner asks for the best sub-batch of 3 to 6.
    What it does here: a coarse value-versus-effort cut, with each input marked [evidence] or [guess], a protected must-do
    lane, and a sensitivity check. Result: section 4.
  - `skill-quality-reviewer`: its `references/quality-review-checklist.md` rubric for check 2 (overlap and collision, :57-89),
    check 3 (duplication or extension, :91-106) and check 7 (invocation posture, :170-184) is the yardstick for the verdicts.
    This is NOT a full invocation. Its Stop Condition says a review needs a skill directory (SKILL.md:194-195), and no
    candidate has a draft yet. Each candidate still needs a real skill-quality review when it is built.
  - No MANUAL-ONLY skill was used. `appsec-implementer`, `secrets-identity-hardener`, `observability-operator` and
    `multi-tenant-security-tester` bodies were READ as overlap evidence only.

## 1. Source rows (docs/skills/03-saas-security-rls.md, "P0 foundation / P1 follow-on / P2 later", :14-16)

The catalog's "remaining cat-03 rows" (`docs/skills-catalog.md:1322-1326`) map to these roadmap rows:

| Topic (catalog :1322-1326) | Row(s), file:line, priority |
|---|---|
| authentication/session review | #108 Authentication Flow Review :50 **P0**; #109 Session Handling Security :51 **P0** |
| CSRF/XSS/SQLi deep-dives | #110 CSRF and Browser Boundary Review :52 P1; #111 XSS Defense Review :53 **P0**; #112 SQL Injection Defense Review :54 **P0** |
| storage-policy review | #115 Storage Access Policy Review :57 **P0** |
| webhook security | #116 Webhook Security Design :58 P1 |
| rate-limit design | #117 API Rate Limit Design :59 P1 |
| logging redaction | #124 Logging Redaction Review :66 **P0** |
| security-impact-note authoring | #127 Security Impact Note Authoring :69 **P0** (also G4, see 3.10) |
| compliance-evidence mapping | #128 Compliance Evidence Mapping :70 P1 |
| privacy-by-design | #129 Privacy-by-Design Review :71 P1 |
| security-drift detection | #130 Security Drift Detection :72 **P0** |

Forecast: `docs/roadmaps/aegis-backlog-forecast.md:730`: "Phase 4 expansion (about ten security topics) | 20–40 | Overlap
check against the shipped security skills first."

**Adjacent unlisted residue (flag).** Row #120 Security Header Review (:62, P1) is not in the catalog's remaining list. The
D8 OWASP gap audit nevertheless records it as open: "A02 residue: application/platform configuration — security headers,
CORS, XML-parser hardening … the app-config slice remains open residue" (`docs/reconciliation/step-0-reconciliation-v4.md:174-178`;
A02 is "partial" at :157). No shipped body mentions HSTS, X-Frame, frame-ancestors, Referrer-Policy or "security header";
the grep returned nothing. I fold #120 into candidate B below. Rows #105, #118, #119 and #125 are also absent from the
remaining list. #118 (audit-log-architect), #119 (error-handling-security-reviewer) and #125 (regression-suite-curator,
multi-tenant-security-tester) look covered from their descriptions. #105 (sensitive column masking) was **not checked in
depth (unverified)**.

## 2. Summary table

| # | Topic → proposed name | Overlap verdict | Posture | Estimate (active h, low confidence) | Batch call |
|---|---|---|---|---|---|
| A | auth/session → `authentication-session-reviewer` | PARTIAL: diff, design and fix lenses exist; no auto-invocable review of an existing auth or session implementation | auto | 3–5 | **RECOMMEND** |
| B | CSRF/XSS (+#120 headers, CORS) → `browser-boundary-reviewer` | PARTIAL: XSS has diff, SAST and implementer coverage; CSRF, security headers, CSP and CORS have no reviewer | auto | 3–5 | **RECOMMEND** |
| F+G | storage policy (#115) + DB-function dynamic SQL (#112 residue) → **extension of `rls-policy-auditor`** | PARTIAL, with a **proven seam defect** (see 3.3) | base stays auto | 1–2 | **RECOMMEND (must-do lane)** |
| D | rate limits → `rate-limit-architect` | PARTIAL: `api-event-architect` owns the public-API contract tiers; abuse-category limits and enforcement architecture are unowned | auto | 3–5 | **RECOMMEND** |
| C | logging redaction → `log-redaction-reviewer` | PARTIAL: the implementation path is manual-only; the detection skill explicitly disclaims safe log content | auto | 2.5–4 | **RECOMMEND** |
| E | webhook security → `inbound-webhook-security-designer` | PARTIAL: outbound (`api-event-architect`) and UX are covered; INBOUND receipt has only a threat-catalog question | auto | 2.5–4 (ext. alternative 1–2) | next batch |
| H | security drift → (later) `security-posture-drift-reviewer` | PARTIAL, mostly covered by six skills; the residual is narrow | auto | not estimated | DEFER |
| I | compliance-evidence mapping | **COVERED** (`compliance-evidence-collector` + foundation + crosswalk) | n/a | 0 | DROP |
| J | privacy-by-design | **COVERED** (`pii-lifecycle-designer`) | n/a | 0 | DROP |
| K | security-impact-note (#127; G5 owns per coordinator) → **extension of `change-classification-gate`** (rls-security floor + note template) | PARTIAL: all six elements have owners, but none produces a change-scoped author record; rollback direction is unowned | base stays auto | 0.75–1.5 | **optional add-on** (independent of the theme) |

Pre-build feasibility: draft descriptions for A, B, C, D and E were written and measured with `yaml.safe_load`
(`$S/skillbatch/g5-work/drafts.yaml`): 981, 909, 944, 966 and 905 characters, all under the 1,024 limit. The F+G
description extension measures 858 → 1,000 characters. These are illustrative drafts, not proposals of final text.

## 3. Per-candidate evidence

### 3.1 A — Authentication and session review (#108 P0, #109 P0) → `authentication-session-reviewer`

**Shipped coverage, quoted.**
- `secrets-identity-hardener` (**MANUAL-ONLY**, catalog maps #109 to it at `skills-catalog.md:465`). Its description says
  "tighten session/token handling (expiry, refresh, storage flags)". Its body is remediation: "This skill changes code and
  config, so it is manual-only" (SKILL.md:23-24), and workflow step 7 is "Tighten sessions/tokens if in scope: HttpOnly/Secure/
  SameSite cookies, sane expiry, working refresh, server-side revocation; add tests" (:83-84). It is not an auto-invocable review.
- `security-pr-reviewer`: "Security-focused review of an ACTUAL diff … hunts authn/authz gaps". Pass 1 checks only "Every
  new/changed endpoint requires authentication?" (references/security-review-passes.md:19-29). The skill's rule is no diff, no review.
- `threat-modeler`: design-time only, "BEFORE it is implemented … Use when designing a security-sensitive feature (auth, …)".
- `authority-invalidation-architect`: diagnoses revocation that fails to take effect ("logout doesn't end the session", SKILL.md:45).
- `share-link-access-architect`: guest sessions only. `cloud-security-baseline-reviewer` (Supabase reference :40) checks
  console-level "Auth redirect URLs are exact … sign-up and rate limits set".
- D8 marks A07 "covered" (`reconciliation:162`) by naming those three skills. Its rubric is "covered = the category's core risk is
  named in at least one shipped Phase 4 skill contract" (:167). That rubric measures naming, not depth.

**Body sweep (gap evidence).** "password reset|forgot password" appears only in `audit-log-architect`'s event taxonomy and
`threat-modeler`'s catalog actor row (threat-catalog.md:75). MFA, TOTP, WebAuthn and passkeys appear only in cloud-account
baselines and the security-event coverage sheet. SSO, SAML and OIDC appear only in cloud, CI and tenant-modeling contexts,
never as auth-flow security. "step-up" and "re-authenticate" appear nowhere. "refresh token" appears only in
`authority-invalidation-architect`. No skill reviews account enumeration in auth flows; the threat catalog only asks whether
errors "reveal record or user or tenant existence" (threat-catalog.md:28-29).

**Verdict: PARTIAL → NEW.** The remaining gap is an auto-invocable review of an EXISTING login, logout, reset, verification
and account-linking, MFA enrollment and recovery, SSO callback, session lifecycle (fixation, rotation, idle and absolute expiry,
refresh rotation with reuse detection, revocation on password or role change), step-up, and enumeration or brute-force exposure.
Check 3 rules out an extension: every base is diff-only, design-only or manual-only (checklist :101-106).
**Posture: auto-invocable.** It reads code, config and exports and reports (standard §5, `skill-generation-standard.md:270-275`;
checklist :176). Its Stop Conditions must forbid live sign-in attempts, credential stuffing or probing; that work is
`dast-safety-harness-designer`'s.
**Use when / not when.** Use it for "is our sign-in, reset, MFA, SSO or session handling safe?" with no diff, and before auth
launches. Do not use it for a diff (`security-pr-reviewer`), a pre-build threat model (`threat-modeler`), the fix
(`secrets-identity-hardener` or `appsec-implementer`), or stale access after revocation (`authority-invalidation-architect`).
**Trigger-eval pins:** `security-pr-reviewer`, `threat-modeler`, `secrets-identity-hardener` (plus `authority-invalidation-architect`).
**Value and dependencies.** Every SaaS has authentication, and both source rows are P0. The skill consumes
`authorization-matrix-designer` and `tenant-modeler`. It shares the brute-force seam with D, so building both in one batch lets
both sides of that seam be pinned. Wiring cost: `project-orchestrator` Stage 4 "Make it safe" lists no auth reviewer today
(SKILL.md:242-247).

### 3.2 B — CSRF, XSS, security headers and CORS (#110 P1, #111 P0, #120 P1) → `browser-boundary-reviewer`

**Shipped coverage.** For XSS, `security-pr-reviewer` covers it in a diff (the catalog maps #111/#112 to it, :467),
`appsec-implementer` (**MANUAL-ONLY**) implements output encoding (references/control-implementation-patterns.md:22-28),
`static-analysis-reviewer` triages scanner XSS findings, and `llm-output-safety-reviewer` covers LLM output sinks only.
For CSRF, only a gotcha in `secrets-identity-hardener` ("moving to HttpOnly cookies changes cross-site request forgery (CSRF)
posture", :151-153) and the cookie-flag pattern in `appsec-implementer` (patterns :47-53) mention it; no description mentions
CSRF (keyword sweep: 0). For headers and CSP, a body grep for HSTS, X-Frame, frame-ancestors, Referrer-Policy and "security
header" returns nothing, and "CSP" appears only in `llm-output-safety-reviewer`. For CORS, the diff pass ("broadened CORS",
security-review-passes.md:52) and the `full-codebase-auditor` checklist ("CORS/debug flags in prod config", :47-48) are the only
coverage. D8 records security headers and CORS as an open A02 residue (:174-178).

**Verdict: PARTIAL → NEW** for one boundary: the browser trust boundary. The scope fits row #110's own text: "browser-side
mutation paths, cookies, headers, origins, and cross-site risks". **Scope risk (check 6):** CSRF, XSS sinks, headers and CORS
must stay one boundary-shaped output (per-surface findings plus one header and CSRF policy), not four jobs. **Posture:
auto-invocable** only if it reviews supplied code, config and captured response headers and fetches nothing live, the same
pattern as `cloud-security-baseline-reviewer`'s "Reads only what it is given, calls no cloud API". **Name note:** avoid
`browser-security-reviewer`, which contains the reserved bundled name `security-review` (`scripts/validate-skills.py:147-163`;
near-miss rule in checklist :86-89).
**Use when / not when.** Use it for "are we safe from CSRF, XSS or clickjacking; set our CSP and headers; check CORS". Do not
use it for a diff, LLM-rendered output, cache headers or the fix.
**Trigger-eval pins:** `security-pr-reviewer`, `llm-output-safety-reviewer`, `caching-strategy-designer` (its trigger-evals
:44 owns "immutable cache headers"), plus `appsec-implementer`.
**Value:** high for every web SaaS. No dependencies.

### 3.3 F+G — Storage access policy (#115 P0) and DB-function dynamic SQL (#112 P0 residue) → extension of `rls-policy-auditor`

**The seam defect.** `file-upload-storage-architect` routes the audit away: "Do NOT use … for auditing existing storage
RLS/bucket policies (rls-policy-auditor)" (description; SKILL.md:51-53, :113, :150, :190). Its trigger-evals case
`existing-policy-audit-goes-to-rls-policy-auditor` expects `rls-policy-auditor` to win "We already have storage bucket policies …
Audit them for holes" (trigger-evals.json:26-31). But `grep -c -iE "storage|bucket|object"` counts **0** in
`rls-policy-auditor/SKILL.md`, **0** in `references/rls-audit-checklist.md` and **0** in `evals/evals.json`. Its 2 hits in
`trigger-evals.json` are unrelated routing prompts (:41, :50). A shipped routing promise therefore lands on a skill with no
storage content.
**Other coverage:** `tenant-isolation-reviewer` has a storage row ("signed URLs scoped and expiring",
isolation-surface-checklist.md:18). `cloud-security-baseline-reviewer` checks account-level "No public bucket unless
intended" (the AWS, Azure, GCP and Supabase references).
**SQLi residue:** `rls-policy-auditor` inspects helper functions only as policy helpers (Inputs :73-74, Workflow :97-101). A body
grep for dynamic, EXECUTE, format( and inject finds nothing in it or in `secure-migration-reviewer`, so dynamic SQL inside
callable database functions has no reviewer outside a diff.
**Verdict: PARTIAL → EXTENSION** (check 3, :101-103: "a bounded slice (a new surface …) that fits the base skill's Purpose
without changing its verdict shape"). Per-command policy audit plus a negative-test plan is the same shape. Bucket-IAM posture
on S3, GCS or Azure stays with `cloud-security-baseline-reviewer`. Description headroom: 858 → 1,000 characters measured.
**Posture:** the base stays auto-invocable ("`rls-policy-auditor` auto (delivers migrations, never runs DDL)", checklist :183-184).
**Pins:** `file-upload-storage-architect` (the existing case stays true), `cloud-security-baseline-reviewer`,
`tenant-isolation-reviewer`. **Platform specifics** (how a given host stores object metadata in Postgres) are verification items
at build time; they are **unverified** here.
**Alternative considered:** a NEW `storage-access-policy-auditor`. It is rejected for now because the main slice fits the base's
verdict shape. Demand for per-prefix bucket-policy audit on non-Postgres stores is **unverified**.

### 3.4 D — Rate-limit design (#117 P1) → `rate-limit-architect`

**Recorded priority signal:** D30 (2026-07-08): "pull these forward, HIGH priority … the unnamed rate-limit-design row (Phase 4 —
general per-tenant/plan API rate limits + noisy-neighbor defense; needs a NAME when pulled)" (reconciliation :745-753; repeated
at :1329). The private audit behind D30 cannot be inspected here (**unverified**).
**Counter-evidence:** `api-event-architect` already had "Design rate limits with a tenant/plan dimension … noisy-neighbor
protection" when Phase 3 shipped. `git show e72412a4:.claude/skills/api-event-architect/SKILL.md` shows lines :27-28 and :73-76,
dated 2026-07-06, before D30. The text is current at SKILL.md:95-98. So D30's stated framing is largely covered already.
Five shipped trigger-evals route public-API rate-limit prompts to `api-event-architect` (`api-doc-generator-designer`,
`command-gateway-architect`, `cross-team-dependency-negotiator`, `error-taxonomy-designer`, `pagination-cursor-designer`),
and four route AI rate limits to `ai-cost-guardrail-designer`.
**What remains unowned:** limits by IP, endpoint and abuse category (row #117: "by actor, tenant, IP, token, endpoint, feature,
and abuse category"), covering credential stuffing, reset and one-time-code abuse, sign-up spam, enumeration and costly
endpoints. Also unowned: the algorithm and the shared counter store, the enforcement tier, trusted client-IP derivation, and
per-endpoint fail-open or fail-closed behavior. `share-link-access-architect` only CONSUMES "Abuse/rate-limit infrastructure
available" (:62-63). `threat-modeler` only asks "Is the endpoint rate-limited per actor/tenant?" (threat-catalog.md:30).
`horizontal-scalability-reviewer` flags in-memory limiter state (:62, :156).
**Verdict: PARTIAL → NEW**, with a hard seam. The new skill must YIELD the published contract (tiers, headers, 429 shape) to
`api-event-architect`, and all five existing cases must stay true. An extension of `api-event-architect` (792 characters,
232 of headroom) is rejected: its Purpose is the external contract, and absorbing this work would need a new output block
(checklist :104-106).
**Posture:** auto-invocable (design only; edits no live config).
**Pins:** `api-event-architect`, `ai-cost-guardrail-designer`, `plan-entitlement-architect` (plus `share-link-access-architect`).
**Value:** high. Brute force and spam defense is basic hygiene [guess, but backed by D30's recorded signal].

### 3.5 C — Logging redaction (#124 P0) → `log-redaction-reviewer`

**Key evidence.** `security-logging-alerting-architect` explicitly disclaims this job: "This addresses the detection and alerting
portion of OWASP Top 10:2025 A09 … Log integrity, safe content handling, retention and backup require their own audit-log
design and operating controls" (SKILL.md:16-18). The audit-log design it points to is `audit-log-architect`, which excludes
app logs: "Do NOT use when: the need is debugging/observability (traces, metrics, app logs)" (:44-45).
OWASP Top 10:2025 A09, fetched 2026-10-08 from `top10.owasp.org/2025/A09_2025-Security_Logging_and_Alerting_Failures`, maps
**CWE-117** (Improper Output Neutralization for Logs) and **CWE-532** (Insertion of Sensitive Information into Log File). Its
description includes "logging sensitive information that should not be logged (such as PII or PHI)". D8 nonetheless marks
A09 "covered" (:164).
**Other coverage:**
- `observability-operator` (**MANUAL-ONLY**, 1,023-character description): "Redaction applied BEFORE emission" is its
  hands-on implementation (:67).
- `pii-lifecycle-designer`: logs are one store in its PII map ("Logs are the shadow PII store", :224-225). It covers PII only,
  not credentials or tokens.
- `sensitive-disclosure-guard`: AI-feature logs only. Its trigger seams with `model-context-designer` (:49) and
  `pii-lifecycle-designer` (:20) put AI-boundary redaction there.
- `security-pr-reviewer`: "Tokens/PII logged?" in a diff only (passes :46).
- `screenshot-evidence-planner`: screenshot masking only.

**Verdict: PARTIAL → NEW.** Every extension base fails check 3. `security-logging-alerting-architect` disclaims the job and
has 26 characters of headroom (998). `observability-operator` is side-effecting and manual-only, so a review placed there would
never auto-trigger. `pii-lifecycle-designer` covers PII only. `audit-log-architect` covers audit records only.
**Posture:** auto-invocable. It reviews code and supplied log samples, never a live log store. Its proof is a canary-secret test
plan.
**Pins:** `sensitive-disclosure-guard`, `pii-lifecycle-designer`, `observability-operator` (plus `audit-log-architect`).
Collision risk is the highest in this group: seven neighbors.

### 3.6 E — Webhook security (#116 P1) → `inbound-webhook-security-designer` (next batch)

**Coverage.** OUTBOUND webhooks are fully designed by `api-event-architect`: "signing with rotatable secrets, timestamped
signatures for replay protection" (:125-131), and "consumers are given a verification recipe including replay rejection; Webhook
target URLs are validated against SSRF" (Security Rules :201-205). `notification-webhook-ux-designer` owns the management UX.
INBOUND receipt appears only as a threat-catalog question: "Inbound webhooks signature-verified, replay-protected,
tenant-mapped?" (threat-catalog.md:51). `ai-threat-modeler`'s trigger-evals route "Threat-model the new billing webhook endpoint
— signature verification, replay, and idempotency" to `threat-modeler` (:14-18), which is enumeration, not a design.
**Verdict: PARTIAL → NEW** under check 3: the trigger is disjoint (receiving versus publishing) and the output differs (a
receiver pipeline). An extension of `api-event-architect` (232 characters of headroom) is a credible cheaper alternative
(1–2 h), and the build-time skill-quality review should settle it.
**Dependency:** pairs naturally with the G3 candidate `idempotency-first-designer` (unbuilt), which deduplicates by event id.
That pairing is why E goes to the next batch, not this one.
**Pins:** `api-event-architect`, `threat-modeler`, `notification-webhook-ux-designer`.

### 3.7 H — Security drift detection (#130 P0) → DEFER

It is covered in pieces by six skills:
- `security-pr-reviewer` pass 4 ("Does the diff LOOSEN an existing control … Report control weakening as its own finding",
  passes :50-54) works on any diff, including a release range.
- `code-reviewer` checks "weakened validation: tests deleted or skipped, assertions loosened" (:82).
- `regression-suite-curator`: "permanent security regression tests retire only through the human-approval path".
- `context-co-update-ci-gate` takes "auth/RLS" as important paths that force a docs update (:70).
- `iac-reviewer` checks "drift from documented architecture".
- `cloud-security-baseline-reviewer` runs "after console-made changes", and `compliance-gap-auditor` checks "drift after material change".

**Residual:** a scheduled comparison of documented security claims (threat-model mitigations, the authz matrix) against current
controls and the tests that pin them, with no diff in hand. That is narrow and composes existing skills, so it is not worth a
skill until demand evidence exists. A placeholder name if it is later built: `security-posture-drift-reviewer`.

### 3.8 I — Compliance-evidence mapping (#128 P1) → COVERED, DROP

Row #128: "Map controls to evidence such as logs, approvals, tests, policies, and change history".
`compliance-evidence-collector` does exactly this: "Per control (from compliance-control-foundation): evidence type, cadence …
population … collector, retention". Its workflow lists "system config, log extract, screenshot, ticket, review minutes, test run,
signed approval" and populations such as a "merged-PR list, audit-log query" (SKILL.md:73-80). `compliance-control-foundation`
supplies each control's "evidence hook", and `multi-framework-crosswalk` maps the controls to frameworks.

### 3.9 J — Privacy-by-design (#129 P1) → COVERED, DROP

Row #129 asks to minimize collection, define purpose, restrict access, support deletion and document retention.
`pii-lifecycle-designer` covers "minimization at collection (purpose stated per field), retention schedules … deletion/erasure
design that PROPAGATES". Its new-field discipline "requires a purpose and a retention class in the same change"
(SKILL.md:94-100). Access restriction is covered by `authorization-matrix-designer`. No body mentions a DPIA, so a legal
impact-assessment workflow is unowned. No evidence of demand for it was found (**unverified**), and the recommendation does not
rely on it.

### 3.10 K — Security-impact-note authoring (#127 P0): **owned by G5** (coordinator decision, 2026-10-08) → EXTENSION of `change-classification-gate`

**One capability, counted twice.** The catalog lists it in Phase 3 (`skills-catalog.md:1313`, as `security-impact-note-author`)
and again in Phase 4 (`:1325`, as "security-impact-note authoring"). It is also in reconciliation :135-137 and in the execution
plan's Phase 3 list (`senior-principal-claude-skills-execution-plan.md:402` and :741). The G4 helper's finding that the forecast
counts it twice (`aegis-backlog-forecast.md:729` and :730) is consistent with these lines; I re-read both catalog lines.
G4's "2–4 h double count" is derived from group averages, not stated anywhere (**unverified** as a figure).

**Row #127 (cat-03:69):** "Document impact, risks, mitigations, tests, rollback, and approval needs for security-sensitive
changes." Each element has a shipped owner today; I checked every body below.

| #127 element | Shipped owner and evidence | Does it fire for "a security-sensitive CHANGE"? |
|---|---|---|
| impact, risks, mitigations, tests | `threat-modeler` Output Format: Assets, Risk ranking, Mitigations, Validation plan | Design-time only. "Do NOT use when: reviewing an implemented diff … this skill works on designs and systems, not hunks" (SKILL.md:36-37) |
| control changes and tests, reviewer side | `security-pr-reviewer` Output: "Control changes", "Tests" | Reviewer verdict, not the author's record |
| approval needs | `change-classification-gate`: rls-security → "negative tests + security review", approval **yes** (SKILL.md:82); `human-approval-boundary` Output: Blast radius, Reversibility, Options | The approval request appears only when the action is not covered by a grant (its description) |
| rollback | `rollback-runbook-author` | Has no security content: `grep -iE "security|re-?open|vulnerab|policy|RLS"` on its SKILL.md returned nothing |
| residual risk of one implemented control | `appsec-implementer` (MANUAL-ONLY) Output: "Does NOT cover" | Only when that manual skill is invoked |
| risks at PR opening | `ai-closeout-reporter` §6 "Risks & known gaps" | Retrospective. Fixed format: "All eight sections, in order, every time" |

**What remains (by element, not a percentage).** No skill produces one author-side, change-scoped record that states:
- the security property before and after the change;
- the boundaries and tenants affected;
- risks introduced or removed;
- which mitigation is proven by which test that fails on revert;
- the **rollback direction**: reverting a security fix re-opens the hole, while reverting a loosening is the safe direction.
  This item is absent from `rollback-runbook-author`.
- the approval path.

**The decisive precedent.** `change-classification-gate`'s matrix already makes written notes part of a class's validation
floor:
- schema-migration: "Forward migration plan; explicit rollback; data-loss statement (even "none")" (`references/classification-matrix.md:18`);
- cloud-iac: "blast-radius statement" (:20);
- rls-security today: only "Negative tests (what must now FAIL); reviewer named; tenant-scope reasoning written down" (:19).

**Verdict: PARTIAL → EXTENSION of `change-classification-gate`.**
- Add a security-impact note, with the fields above, to the rls-security floor, plus a short note template in its references.
- The checklist's extension test fits (:101-103): it is a bounded slice that keeps the same verdict shape (class → floor), as
  the migration and IaC notes already do.
- Description headroom: 669 of 1,024, measured.
- Optional one-line Gotcha in `rollback-runbook-author` on rollback direction. Its body only: the description is 997 characters.

**Why not G4's lean (MERGE into `threat-modeler`).** I verified this independently instead of adopting it:
- `threat-modeler`'s own yield clause (:36-37) sends implemented changes to `security-pr-reviewer`, and impact notes are written
  for a concrete change.
- Its Output Format has no rollback or approval-needs field, so a merge needs a new output block. The checklist (:104-106) says
  that signals a separate artifact, not an extension.

**Why not `ai-closeout-reporter`.**
- Its description is at 1,015 of 1,024, so the phrase "security impact note" cannot be added and the section would never be
  triggered by name.
- Its eight-section format is fixed "every time".
- It looks back at finished work, while approval needs come before merge.

**Why not a NEW skill.** It would collide with five neighbors (`threat-modeler`, `security-pr-reviewer`,
`human-approval-boundary`, `change-classification-gate`, `ai-closeout-reporter`) for a template-sized artifact. The checklist's
"narrow-but-trivial … fold it into its natural parent" applies (:167-168).

**Why not DROP.** The rls-security floor has no written impact or rollback-direction record, yet migration and IaC changes get
one, and the row is P0.

**Posture:** `change-classification-gate` stays auto-invocable. It writes nothing; the author fills the note.
**Estimate:** 0.75–1.5 h, using precedent extension ranges (qa-tier1 :60; ai-sdlc :68); low confidence.
**Security-relevant surface:** not listed unless the edit touches the gate's Stop Conditions (CONTRIBUTING.md:238-249).
A reference-file and matrix edit alone answers **No**. This is unverified until the diff exists.
**Pins:** `threat-modeler` (design-time model), `security-pr-reviewer` (review verdict), `human-approval-boundary` (approval
request).
**Use when / not when.** Use it for "what must a security-class change carry before merge; write the note for this RLS
change". Do not use it for modelling a new feature's threats, or for reviewing someone's diff.

## 4. Recommendation (method: `prioritization-frame-picker`)

**Frame.** A coarse value-versus-effort cut in buckets. It fits because the inputs are qualitative and no usage data exists.
Its limit: no total order is claimed inside a bucket.

**Inputs.**
- Source priority [evidence; but per 03 doc :14-16 these are "original planning tiers"].
- Recorded repo residue or decision: D8 :174-178; D30 :745-753; seam defect 3.3 [evidence].
- Gap size after overlap [evidence: greps and quotes above].
- Neighbors to pin, counted from section 3 [evidence].
- Effort [guess, from precedent; see below].
- Value to a SaaS builder [guess, except where a recorded decision supports it].

**Protected must-do lane:** F+G. A shipped routing promise is false today (3.3), and the fix is correctness, not a value score.

**Recommended sub-batch: "Web application boundary" — 4 new skills + 1 extension.**

| Item | Active h |
|---|---|
| F+G `rls-policy-auditor` extension (storage policies; dynamic SQL in callable functions) | 1–2 |
| A `authentication-session-reviewer` | 3–5 |
| B `browser-boundary-reviewer` | 3–5 |
| D `rate-limit-architect` | 3–5 |
| C `log-redaction-reviewer` | 2.5–4 |
| Batch overhead (registration, decision row, reciprocity, trigger-evals on both sides, Stage 4 wiring) | 2–3.5 |
| **Total** | **14.5–24.5** (provisional, low confidence) |

**Cuts if the coordinator needs fewer items:**
- Core of four {F+G, A, B, D}: **11.5–20** (overhead 1.5–3).
- Minimum of three {F+G, A, B}: **8.5–15** (overhead 1.5–3).

**Optional sixth item:** K, the `change-classification-gate` extension (0.75–1.5 h). It is cheap and P0, but it is not part of
the "boundary" theme. It can ship in this batch, making it **15.25–26 h** (6 items: 4 new + 2 extensions), or in any later
governance batch.

**Next batch:** E, paired with G3 `idempotency-first-designer`. **Defer:** H. **Drop:** I and J.

**Forecast note.** #127 is counted in both the Phase 3 and the Phase 4 forecast rows (3.10). The 68–140 range should drop one
count when it is reconciled; the exact hours are **unverified**.

**Estimate basis.** No measured actuals exist. `grep -c -E "D69|D70|D71" docs/roadmaps/aegis-execution-metrics.md` returns 0,
and "active time not measured" appears 146 times. Per-item ranges therefore reuse the precedent proposals' provisional ranges:
- New review or design skills: 2–5 h (qa-tier1 :61-63; phase6 :75-79; phase7 :68; ai-sdlc :66).
- Extensions: 0.75–2 h.
- Overhead: 1–3.5 h (phase6 :80 is 2–3.5 h for 4 new + 1 extension).

I placed security skills at the top of the range (3–5) because each has five to seven neighbors to pin. Weak wall-time context,
not active time: PR #526 (one security reviewer skill, 17 files, +824) ran 1h58m18s from open to merge; PR #502 ran 4h12m36s
(`gh api …/pulls/{526,502}`).

**Posture.** All five items are auto-invocable read, review or design work (standard §5 :270-275; checklist :176). The extension
keeps `rls-policy-auditor` auto-invocable. There is no manual-only flip.

**Security-relevant surface implications (CONTRIBUTING.md:238-249).**
- Every new skill carries required Stop Conditions (standard §4 :197-222) and an invocation-posture decision. Security skills
  normally add Security Rules too (`api-event-architect` :199, `rls-policy-auditor` :166). The PR must therefore answer
  **Yes** to the template question (CONTRIBUTING.md:253-258). Precedent: PR #526 answered "[x] Yes … a new security skill's
  frontmatter invocation posture … and its Security Rules and Stop Conditions".
- The F+G extension is also **Yes** if it edits `rls-policy-auditor`'s Security Rules (:166) or Stop Conditions (:202).
- Reciprocity edits to neighbor DESCRIPTIONS are not a listed surface. Several neighbors are near the 1,024-character limit:
  `observability-operator` 1023, `llm-output-safety-reviewer` 1018, `notification-webhook-ux-designer` 1006,
  `security-logging-alerting-architect` 998, `cloud-security-baseline-reviewer` 994. Those may stay one-way, since ROUTE-002 is
  informational (qa-tier1 proposal, Terms).
- The additional explicit security review is required **for outside contributions only** (CONTRIBUTING.md:231-236, :258;
  open-decisions :103; AGENTS.md). An agent-built batch does not trigger it. A voluntary security-lens review is the
  coordinator's choice, not a rule.
- No item touches `scripts/`, `.github/`, `tools/`, `AGENTS.md`, the approval register or standard §5. No item is MANUAL-ONLY.

### Self-scrutiny

- **Strongest counter-argument.** D8 marked A05, A07 and A09 "covered" (:160, :162, :164). A reviewer could call A, B and C
  duplicates, and adding four auto-invocable security reviewers to a 195-skill corpus raises misrouting risk: "security-review my
  login" could split between A and `security-pr-reviewer`.
  - Reply: D8's own rubric counts naming, not depth (:167). The later catalog still lists these topics as open (:1322-1326).
    `security-logging-alerting-architect` itself disclaims safe log content (:16-18). The body greps show no reset, MFA, SSO,
    step-up, CSRF-review or header-review content anywhere.
  - Reply: the misrouting risk is real. The mitigation is the "diff → `security-pr-reviewer`; no diff → A or B" seam, pinned
    with trigger-evals on both sides. That mitigation is untested until built.
- **Least certain claims.**
  1. The value-to-builder ranking is partly [guess]. The DEMAND helper's evidence should override it.
  2. D's priority leans on D30, whose source audit cannot be inspected (**unverified**), while D30's stated framing is already
     largely covered by `api-event-architect`.
  3. B's scope may fail check 6 (one job) at build time.
  4. All hour ranges: no measured actuals exist.
  5. The SQLi slice (G) assumes DB functions are reachable as API calls on the user's platform; that is a platform-specific
     verification item.
  6. K's home has a timing problem: `change-classification-gate` runs BEFORE work, and the note is completed after it. The
     same is true of the migration "data-loss statement" floor, so this is precedent, not proof. If a build-time skill-quality
     review finds the note orphaned, the fallback is a change-note output mode for `threat-modeler`, which would require
     relaxing its "not hunks" yield clause.
- **Evidence that would change this.**
  - DEMAND evidence that inbound webhooks recur more often than rate limits would swap E for D.
  - A skill-quality review finding B's scope a catch-all would split CSRF and headers away from XSS, or drop XSS (already covered
    in the diff lens).
  - Proof that `rls-policy-auditor`'s policy audit already handles storage tables in practice would downgrade F to a wording fix.
  - An owner preference for fewer, larger skills would make E an `api-event-architect` extension.
  - If the coordinator's cross-group batch cannot hold five items, keep {F+G, A, B} first: that order is the same whether or not
    D30's evidence is discounted.

## 5. Not inspected

- Bodies of `iso-*`, `soc2-*` and `statement-of-applicability-author` beyond their descriptions; I relied on the compliance
  verdict from `compliance-evidence-collector`'s body.
- Row #105 in depth.
- `docs/delivery-workflow.md` beyond a size check (894 lines). Delivery mechanics are the MECH helper's job.
- Network sources other than the OWASP A09:2025 page.
- Live behavior of any skill: no eval was run.
