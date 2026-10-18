# Readability Phase 4 re-read lane B - Stage C batch record, batch 18, 2026-10-18

**Written by: DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness).** Agent true identity **sd-d-793-r2**; stage role **sd-c-read-b18-c1**. Stage C implementation of accepted lane-B batch-18 plan **6248432832** and Stage B ACCEPT **6248458364**. Signed with both names: **sd-d-793-r2 (true identity) - sd-c-read-b18-c1 (stage role).**

This record is the Stage C evidence artifact for the eight frozen lane-B batch-18 pages. It is the only added tracked path in its pull request; no page edit, plan file, keeper row, index/ledger/register/manifest change or other tracked path is included.

## 1. Plan and derivation

| Item | Value |
| --- | --- |
| Plan of record | merged PR #834 issue comment **6248432832** (14,619 B; immutable; author sd-e-802-r1 / sd-a-read-b18-r1) |
| Stage B audit | **6248458364 ACCEPT** - canonical B1-B6 verbatim; frontier 248-255/batch 18 confirmed; eight pages 63,988 B / 1,085 LF reproduce |
| Live base | main **e7acaca40c8df2ea15ae798e8ec4b0c6b13d551f** = 33rd session record merge (PR #834 merged; first parent 84a5295d) |
| Merge attribution | e7acaca4 = #834 33rd; 84a5295d = #831 32nd; 655e40ea = #828 31st; 883bf690 = #832 30th |
| Merged lane-B rows | **144-199 AND 208-215** (batches 2/2r/3/5/6/7/8/9/10/11/13) |
| Open reservations (not read) | **#833 200-207; #835 216-223; #836 224-231; #837 232-239; #838 240-247** |
| This block | **P1-P8 = pending indices 248-255**, lane B batch **18** |
| Next unread after block | **256** .claude/skills/security-pr-reviewer/SKILL.md (not read here) |
| Pinned ref / instrument | 2db1ffb7; instrument run at base: 690 / 107 / 6 / 567 / 0 / 6 / 0 / 4 / official 583; pending 573; lane A 0-143 complete; lane B 144-287 |

## 2. The eight frozen pages

| # | Index | Page | Blob at 2db1ffb7 | Bytes / LF | Eligibility |
| --- | ---: | --- | --- | ---: | --- |
| P1 | 248 | .claude/skills/screenshot-evidence-planner/references/evidence-rules.md | b0db745fe67523f7afd9b35b5837aaca3368b7af | 3,389 / 66 | pending; no keeper; unread; outside reservations; zero drift |
| P2 | 249 | .claude/skills/search-architecture-designer/SKILL.md | 82834f24ddb23b0d389a946b741dd8c7fe36e9f0 | 14,005 / 229 | pending; no keeper; unread; outside reservations; zero drift |
| P3 | 250 | .claude/skills/secrets-identity-hardener/SKILL.md | c0b456f9e0d8484b4837c6e526ae447f4e6775a0 | 10,160 / 176 | pending; no keeper; unread; outside reservations; zero drift |
| P4 | 251 | .claude/skills/secrets-identity-hardener/references/secret-classification-and-rotation.md | b8a04d1734e57fb376ea27219358bdd6223e9659 | 4,401 / 86 | pending; no keeper; unread; outside reservations; zero drift |
| P5 | 252 | .claude/skills/secure-migration-reviewer/SKILL.md | e04d9e625bb49950ebc7d8a28b502f5714f29d4b | 10,403 / 178 | pending; no keeper; unread; outside reservations; zero drift |
| P6 | 253 | .claude/skills/secure-migration-reviewer/references/migration-safety-checklist.md | 6be0519f1be417af53e71d66488b5e9b314c695d | 3,867 / 79 | pending; no keeper; unread; outside reservations; zero drift |
| P7 | 254 | .claude/skills/security-logging-alerting-architect/SKILL.md | 4e2d299325548f3bbe2518e29caa02c0ac6e2234 | 13,576 / 216 | pending; no keeper; unread; outside reservations; zero drift |
| P8 | 255 | .claude/skills/security-logging-alerting-architect/references/security-event-coverage-sheet.md | d6fb69dd169f25bcd6c6944f464277c4fa4b7a86 | 4,187 / 55 | pending; no keeper; unread; outside reservations; zero drift |
| **Totals** | | **eight pages** | | **63,988 / 1,085** | |

**Totals: 8 pages / 63,988 bytes / 1,085 LF / 0 FULL / 8 PARTIAL / 0 UNRUN / 0 edits.** Every 40-hex blob resolves at pinned ref 2db1ffb7 and is identical at live base e7acaca4 (zero drift); all eight are pending with no keeper and outside the open reservations.

## 3. Whole-page evidence and per-page canonical B1-B6

### P1 - index 248 - .claude/skills/screenshot-evidence-planner/references/evidence-rules.md

**Whole-page read:** L1-66 opened whole at the pinned blob b0db745fe67523f7afd9b35b5837aaca3368b7af; 3,389 bytes / 66 LF. Purpose/opening: Detail file for `screenshot-evidence-planner`. Loaded on demand..
**B1 (purpose/reader):** opening description/purpose plus headings identify the page job and reader: L1 # Evidence Rules Reference; L13 ## Checkpoint selection catalog; L29 ## Naming token table.
**B2 (first-use expansion):** named gaps found by the inventory: L8 SHA; L9 PII; L9 PR; L10 CI; L10 M0; L10 M3; L33 DEFECT; L33 id; L44 M1; L45 M2. These first uses precede or lack in-page expansion, so the page is PARTIAL on B2 where present.
**B3 (structure/example/contract):** L1 # Evidence Rules Reference; L13 ## Checkpoint selection catalog; L17 \| State class \| Why captured \|; L18 \| --- \| --- \|; the page provides structured sections plus concrete examples/checklists and preserves its technical contract.
**B4 (shipped vs proposed):** tested explicitly; shipped/proposed/blocked/design candidate statements at L22; L43; L66. No synthetic test, passing check or approved design is described as a deployed integration or measured result.
**B5 (navigation/contract):** 1 markdown link(s) at L6; referenced paths/commands checked at the pinned ref and current; technical contract preserved and no safety boundary removed.
**B6 (independent read-only review):** **UNVERIFIED** - the reader is not an independent non-author reviewer; git metadata cannot prove non-authorship, so B6 cannot support FULL.
**Verdict: PARTIAL** - basis: canonical B6 unverified; B2 named gap(s): L8 SHA, L9 PII, L9 PR, L10 CI.

### P2 - index 249 - .claude/skills/search-architecture-designer/SKILL.md

**Whole-page read:** L1-229 opened whole at the pinned blob 82834f24ddb23b0d389a946b741dd8c7fe36e9f0; 14,005 bytes / 229 LF. Purpose/opening: Design search/discovery for a multi-tenant SaaS — in-database full-text (tsvector / trigram) vs a dedicated search engine chosen by scale and relevance need; the indexing pipeline and its freshness lag; relevance/ranking; the per-tenant search-isolation boundary (every query AND every index scoped so results never cross tenants — the search leak); and the faceting/pagination seam. Produces the engine decision, indexing + freshness plan, ranking model, and the tenant-isolation contract. Use when adding search, autocomplete, or discovery, when search is slow, stale, or irrelevant, or when search results must be tenant-isolated. Do NOT use for AI/semantic vector retrieval and its security (rag-security-architect), the base data-store tenancy model (multi-tenant-data-architect), or cursor/pagination mechanics (pagination-cursor-designer) — this designs keyword/faceted search and defers those..
**B1 (purpose/reader):** opening description/purpose plus headings identify the page job and reader: L6 # Search Architecture Designer; L13 ## Purpose; L29 ## Use When.
**B2 (first-use expansion):** named gaps found by the inventory: L3 AI; L10 DB; L10 GIN; L40 SEMANTIC; L48 MECHANICS; L66 LIKE; L106 FAILS; L135 ARCHITECTURE; L135 SEARCH; L139 FRESHNESS. These first uses precede or lack in-page expansion, so the page is PARTIAL on B2 where present.
**B3 (structure/example/contract):** L6 # Search Architecture Designer; L13 ## Purpose; L134 ```; L153 ```; the page provides structured sections plus concrete examples/checklists and preserves its technical contract.
**B4 (shipped vs proposed):** tested explicitly; shipped/proposed/blocked/design candidate statements at L3; L81; L92; L99. No synthetic test, passing check or approved design is described as a deployed integration or measured result.
**B5 (navigation/contract):** 0 markdown link(s); referenced paths/commands checked at the pinned ref and current; technical contract preserved and no safety boundary removed.
**B6 (independent read-only review):** **UNVERIFIED** - the reader is not an independent non-author reviewer; git metadata cannot prove non-authorship, so B6 cannot support FULL.
**Verdict: PARTIAL** - basis: canonical B6 unverified; B2 named gap(s): L3 AI, L10 DB, L10 GIN, L40 SEMANTIC.

### P3 - index 250 - .claude/skills/secrets-identity-hardener/SKILL.md

**Whole-page read:** L1-176 opened whole at the pinned blob c0b456f9e0d8484b4837c6e526ae447f4e6775a0; 10,160 bytes / 176 LF. Purpose/opening: MANUAL-ONLY; never auto-invoke. Harden how an application handles secrets and identity — move hardcoded credentials/tokens/keys into a secret manager or server-only env, classify each variable as public vs server-only (and catch client-bundle exposure like VITE_/NEXT_PUBLIC_ leaks), enforce least-privilege service accounts, add rotation and revocation, and tighten session/token handling (expiry, refresh, storage flags) — with tests proving a secret is unreachable from the client and a rotated credential is honored. Use when secrets are hardcoded/committed, env classification is unclear, a key needs rotation, or service accounts are over-privileged. Side-effecting and manual-only. Do NOT use to implement one app-layer control (appsec-implementer), audit RLS/service-role in the DB (rls-policy-auditor), or model threats (threat-modeler)..
**B1 (purpose/reader):** opening description/purpose plus headings identify the page job and reader: L7 # Secrets & Identity Hardener; L14 ## Purpose; L26 ## Use When.
**B2 (first-use expansion):** named gaps found by the inventory: L3 DB; L3 MANUAL-ONLY; L3 RLS; L9 CD; L9 CI; L11 KMS; L12 authz; L28 repo; L31 CI-; L42 REVIEW. These first uses precede or lack in-page expansion, so the page is PARTIAL on B2 where present.
**B3 (structure/example/contract):** L7 # Secrets & Identity Hardener; L14 ## Purpose; L95 ```; L108 ```; the page provides structured sections plus concrete examples/checklists and preserves its technical contract.
**B4 (shipped vs proposed):** tested explicitly; shipped/proposed/blocked/design candidate statements at L51; L105; L126. No synthetic test, passing check or approved design is described as a deployed integration or measured result.
**B5 (navigation/contract):** 1 markdown link(s) at L171; referenced paths/commands checked at the pinned ref and current; technical contract preserved and no safety boundary removed.
**B6 (independent read-only review):** **UNVERIFIED** - the reader is not an independent non-author reviewer; git metadata cannot prove non-authorship, so B6 cannot support FULL.
**Verdict: PARTIAL** - basis: canonical B6 unverified; B2 named gap(s): L3 DB, L3 MANUAL-ONLY, L3 RLS, L9 CD.

### P4 - index 251 - .claude/skills/secrets-identity-hardener/references/secret-classification-and-rotation.md

**Whole-page read:** L1-86 opened whole at the pinned blob b8a04d1734e57fb376ea27219358bdd6223e9659; 4,401 bytes / 86 LF. Purpose/opening: Progressive-disclosure detail for `secrets-identity-hardener`. Operate on.
**B1 (purpose/reader):** opening description/purpose plus headings identify the page job and reader: L1 # Secret Classification & Rotation; L16 ## Environment-variable classification rubric; L31 ## Client-bundle exposure checks (verify the ARTIFACT, not the convention).
**B2 (first-use expansion):** named gaps found by the inventory: L4 LOCATIONS; L4 NAMES; L8 API; L9 DB; L9 URL; L10 CI; L10 CRA; L10 KMS; L11 RLS; L11 XSS. These first uses precede or lack in-page expansion, so the page is PARTIAL on B2 where present.
**B3 (structure/example/contract):** L1 # Secret Classification & Rotation; L16 ## Environment-variable classification rubric; L18 \| Class \| Definition \| May ship to client? \| Example \|; L19 \|---\|---\|---\|---\|; the page provides structured sections plus concrete examples/checklists and preserves its technical contract.
**B4 (shipped vs proposed):** tested explicitly over the whole page; no statement presents proposed/blocked/synthetic behavior as shipped, and no deployed-integration claim is made.
**B5 (navigation/contract):** 0 markdown link(s); referenced paths/commands checked at the pinned ref and current; technical contract preserved and no safety boundary removed.
**B6 (independent read-only review):** **UNVERIFIED** - the reader is not an independent non-author reviewer; git metadata cannot prove non-authorship, so B6 cannot support FULL.
**Verdict: PARTIAL** - basis: canonical B6 unverified; B2 named gap(s): L4 LOCATIONS, L4 NAMES, L8 API, L9 DB.

### P5 - index 252 - .claude/skills/secure-migration-reviewer/SKILL.md

**Whole-page read:** L1-178 opened whole at the pinned blob e04d9e625bb49950ebc7d8a28b502f5714f29d4b; 10,403 bytes / 178 LF. Purpose/opening: Review a database migration for security and deploy safety before it ships — privilege/GRANT changes, effective RLS scope for the intended app role, unsafe defaults, destructive or irreversible operations, tenant-scoped backfills, lock/downtime risk, and forward/rollback safety with deploy-order coupling. A new tenant table with RLS enabled but no applicable policy is default-denied, an availability finding rather than exposure. Produces evidenced findings, rollback assessment, and negative tests for tenant/authorization changes. Use to review or gate a migration/DDL change. Delegate deep RLS analysis to rls-policy-auditor. Do NOT use for app-code diffs (security-pr-reviewer), dependency/CI risk (supply-chain-security-reviewer), or SAST triage (static-analysis-reviewer)..
**B1 (purpose/reader):** opening description/purpose plus headings identify the page job and reader: L6 # Secure Migration Reviewer; L8 ## Purpose; L21 ## Use When.
**B2 (first-use expansion):** named gaps found by the inventory: L3 CI; L3 DDL; L3 GRANT; L3 RLS; L3 SAST; L31 CHECK; L31 DEFINER; L31 SECURITY; L31 USING; L40 ORM. These first uses precede or lack in-page expansion, so the page is PARTIAL on B2 where present.
**B3 (structure/example/contract):** L6 # Secure Migration Reviewer; L8 ## Purpose; L95 ```; L111 ```; the page provides structured sections plus concrete examples/checklists and preserves its technical contract.
**B4 (shipped vs proposed):** tested explicitly; shipped/proposed/blocked/design candidate statements at L17; L44; L81; L122. No synthetic test, passing check or approved design is described as a deployed integration or measured result.
**B5 (navigation/contract):** 2 markdown link(s) at L138; L172; referenced paths/commands checked at the pinned ref and current; technical contract preserved and no safety boundary removed.
**B6 (independent read-only review):** **UNVERIFIED** - the reader is not an independent non-author reviewer; git metadata cannot prove non-authorship, so B6 cannot support FULL.
**Verdict: PARTIAL** - basis: canonical B6 unverified; B2 named gap(s): L3 CI, L3 DDL, L3 GRANT, L3 RLS.

### P6 - index 253 - .claude/skills/secure-migration-reviewer/references/migration-safety-checklist.md

**Whole-page read:** L1-79 opened whole at the pinned blob 6be0519f1be417af53e71d66488b5e9b314c695d; 3,867 bytes / 79 LF. Purpose/opening: Progressive-disclosure detail for the owning Secure Migration Reviewer..
**B1 (purpose/reader):** opening description/purpose plus headings identify the page job and reader: L1 # Migration Safety Checklist; L8 ## Security checklist; L25 ## Tenant-scope data-op checklist.
**B2 (first-use expansion):** named gaps found by the inventory: L5 RLS; L10 ENABLE; L10 LEVEL; L10 ROW; L10 SECURITY; L15 FORCE; L17 ALTER; L17 DEFAULT; L17 PRIVILEGES; L19 DEFINER. These first uses precede or lack in-page expansion, so the page is PARTIAL on B2 where present.
**B3 (structure/example/contract):** L1 # Migration Safety Checklist; L8 ## Security checklist; L35 \| Operation \| Risk \| Note \|; L36 \|---\|---\|---\|; the page provides structured sections plus concrete examples/checklists and preserves its technical contract.
**B4 (shipped vs proposed):** tested explicitly over the whole page; no statement presents proposed/blocked/synthetic behavior as shipped, and no deployed-integration claim is made.
**B5 (navigation/contract):** 1 markdown link(s) at L3; referenced paths/commands checked at the pinned ref and current; technical contract preserved and no safety boundary removed.
**B6 (independent read-only review):** **UNVERIFIED** - the reader is not an independent non-author reviewer; git metadata cannot prove non-authorship, so B6 cannot support FULL.
**Verdict: PARTIAL** - basis: canonical B6 unverified; B2 named gap(s): L5 RLS, L10 ENABLE, L10 LEVEL, L10 ROW.

### P7 - index 254 - .claude/skills/security-logging-alerting-architect/SKILL.md

**Whole-page read:** L1-216 opened whole at the pinned blob 4e2d299325548f3bbe2518e29caa02c0ac6e2234; 13,576 bytes / 216 LF. Purpose/opening: Design the security-event detection and alerting layer — DETECTION coverage (what must be logged: authn failures/anomalies, access-control denials, privilege/config changes, injection/abuse signals, sensitive-data access), ALERTING rules (alert vs ticket, thresholds justified against baselines, correlation, noise control), and response WIRING (every alert has an owner, severity, escalation, runbook link). Addresses the detection and alerting portion of OWASP Top 10:2025 A09 (Security Logging and Alerting Failures). Use when designing security monitoring/detection/alerting or asking "would we notice this attack?". Do NOT use for the audit RECORD (audit-log-architect — records, never detects/alerts), system/perf telemetry or alert-config edits (observability-operator), reliability SLOs/paging (slo-reliability-architect), checking audit logging is on in an account (cloud-security-baseline-reviewer), or the playbook AFTER an alert (incident-response-runbook — this designs what fires it)..
**B1 (purpose/reader):** opening description/purpose plus headings identify the page job and reader: L6 # Security Logging & Alerting Architect; L8 ## Purpose; L22 ## Use When.
**B2 (first-use expansion):** named gaps found by the inventory: L3 A09; L3 ALERTING; L3 DETECTION; L3 OWASP; L3 RECORD; L3 WIRING; L34 MONITORING; L38 ON; L38 TOP; L39 EDITING. These first uses precede or lack in-page expansion, so the page is PARTIAL on B2 where present.
**B3 (structure/example/contract):** L6 # Security Logging & Alerting Architect; L8 ## Purpose; L209 — starter security-event classes with example events, required fields,; the page provides structured sections plus concrete examples/checklists and preserves its technical contract.
**B4 (shipped vs proposed):** tested explicitly; shipped/proposed/blocked/design candidate statements at L3; L10; L18; L19. No synthetic test, passing check or approved design is described as a deployed integration or measured result.
**B5 (navigation/contract):** 4 markdown link(s) at L82; L208; L211; L214; referenced paths/commands checked at the pinned ref and current; technical contract preserved and no safety boundary removed.
**B6 (independent read-only review):** **UNVERIFIED** - the reader is not an independent non-author reviewer; git metadata cannot prove non-authorship, so B6 cannot support FULL.
**Verdict: PARTIAL** - basis: canonical B6 unverified; B2 named gap(s): L3 A09, L3 ALERTING, L3 DETECTION, L3 OWASP.

### P8 - index 255 - .claude/skills/security-logging-alerting-architect/references/security-event-coverage-sheet.md

**Whole-page read:** L1-55 opened whole at the pinned blob d6fb69dd169f25bcd6c6944f464277c4fa4b7a86; 4,187 bytes / 55 LF. Purpose/opening: Starter classes for the detection coverage map. Every event: structured, with.
**B1 (purpose/reader):** opening description/purpose plus headings identify the page job and reader: L1 # Security-Event Coverage Sheet; L22 ## Event classes; L35 ## Noise-control patterns.
**B2 (first-use expansion):** named gaps found by the inventory: L5 id; L14 IP; L15 authz; L15 MFA; L16 IDOR; L16 RLS; L17 API; L17 WAF; L18 AI; L18 SSRF. These first uses precede or lack in-page expansion, so the page is PARTIAL on B2 where present.
**B3 (structure/example/contract):** L1 # Security-Event Coverage Sheet; L22 ## Event classes; L24 \| Class \| Example events \| Detection-critical fields \| Default posture \|; L25 \|---\|---\|---\|---\|; the page provides structured sections plus concrete examples/checklists and preserves its technical contract.
**B4 (shipped vs proposed):** tested explicitly; shipped/proposed/blocked/design candidate statements at L14; L48; L54. No synthetic test, passing check or approved design is described as a deployed integration or measured result.
**B5 (navigation/contract):** 1 markdown link(s) at L13; referenced paths/commands checked at the pinned ref and current; technical contract preserved and no safety boundary removed.
**B6 (independent read-only review):** **UNVERIFIED** - the reader is not an independent non-author reviewer; git metadata cannot prove non-authorship, so B6 cannot support FULL.
**Verdict: PARTIAL** - basis: canonical B6 unverified; B2 named gap(s): L5 id, L14 IP, L15 authz, L15 MFA.

## 4. Required five-class exact-once token inventory

**Method:** one contiguous table; one row per real page token at its real first-use line. Classes: (i) uppercase/acronym; (ii) lowercase technical/shorthand; (iii) mixed-case/file identifier; (iv) backticked identifier/command; (v) angle/brace placeholder/operator/unit/lifecycle-status token. Key is (page, first-use line, normalized token); backticked/unbackticked forms normalize to one token. No fabricated, numeric-only or grouped residual rows.

| Page | Line | Class | Token | Disposition |
| --- | ---: | --- | --- | --- |
| P1 | 3 | iv | screenshot-evidence-planner | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P1 | 6 | iv | cp-id | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P1 | 6 | iii | SKILL | documented exclusion — exact file/reference name, not an abbreviation |
| P1 | 6 | iii | SKILL.md | documented exclusion — exact file name/reference, not an abbreviation |
| P1 | 7 | iv | CP-INV-03 | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P1 | 7 | iv | MC-INVITE-004 | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P1 | 8 | i | SHA | named gap — first use before any expansion on this page |
| P1 | 9 | i | PII | named gap — first use before any expansion on this page |
| P1 | 9 | i | PR | named gap — first use before any expansion on this page |
| P1 | 10 | i | CI | named gap — first use before any expansion on this page |
| P1 | 10 | i | M0 | named gap — first use before any expansion on this page |
| P1 | 10 | i | M3 | named gap — first use before any expansion on this page |
| P1 | 31 | v | <build> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P1 | 31 | v | <cp-id> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P1 | 31 | v | <cp-id>--<route-or-case>--<persona>--<build>--<yyyymmdd-hhmmss>.png | documented exclusion — backticked self-describing template placeholder, not an abbreviation |
| P1 | 31 | v | <persona> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P1 | 31 | v | <route-or-case> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P1 | 31 | v | <yyyymmdd-hhmmss> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P1 | 33 | v | <id> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P1 | 33 | i | DEFECT | named gap — first use before any expansion on this page |
| P1 | 33 | v | DEFECT-<id> | documented exclusion — backticked self-describing template placeholder, not an abbreviation |
| P1 | 33 | ii | id | named gap — lowercase technical shorthand first use; no expansion on this page |
| P1 | 34 | iv | route-or-case | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P1 | 34 | iv | settings-billing | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P1 | 35 | iv | admin | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P1 | 35 | iv | member | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P1 | 35 | iv | persona | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P1 | 36 | iv | build | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P1 | 37 | iv | Screenshot (47).png | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P1 | 44 | i | M1 | named gap — first use before any expansion on this page |
| P1 | 45 | i | M2 | named gap — first use before any expansion on this page |
| P1 | 63 | ii | repo | named gap — lowercase technical shorthand first use; no expansion on this page |
| P2 | 3 | i | AI | named gap — first use before any expansion on this page |
| P2 | 3 | i | AND | documented exclusion — ordinary English all-caps emphasis/status word with plain meaning, not a coded identifier |
| P2 | 3 | i | NOT | documented exclusion — ordinary English all-caps emphasis/status word with plain meaning, not a coded identifier |
| P2 | 9 | i | RAG | defined-at-first-use — expanded on this line |
| P2 | 10 | i | DB | named gap — first use before any expansion on this page |
| P2 | 10 | i | GIN | named gap — first use before any expansion on this page |
| P2 | 26 | iv | rag-security-architect | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P2 | 37 | iv | tsvector | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P2 | 38 | iv | pg_trgm | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P2 | 40 | i | SEMANTIC | named gap — first use before any expansion on this page |
| P2 | 45 | iv | tenant_id | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P2 | 46 | iv | multi-tenant-data-architect | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P2 | 48 | i | MECHANICS | named gap — first use before any expansion on this page |
| P2 | 50 | iv | pagination-cursor-designer | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P2 | 66 | i | LIKE | named gap — first use before any expansion on this page |
| P2 | 66 | iv | LIKE '%x%' | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P2 | 106 | i | CLOSED | documented exclusion — ordinary English all-caps emphasis/status word with plain meaning, not a coded identifier |
| P2 | 106 | i | FAILS | named gap — first use before any expansion on this page |
| P2 | 122 | iv | observability-operator | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P2 | 135 | v | <system/domain> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P2 | 135 | i | ARCHITECTURE | named gap — first use before any expansion on this page |
| P2 | 135 | i | SEARCH | named gap — first use before any expansion on this page |
| P2 | 136 | v | <in-DB full-text (tsvector/pg_trgm) \| dedicated engine> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P2 | 138 | v | <entities, per-tenant + total size, query volume, result type> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P2 | 139 | i | FRESHNESS | named gap — first use before any expansion on this page |
| P2 | 139 | i | LAG | named gap — first use before any expansion on this page |
| P2 | 142 | v | <server-derived tenant filter, non-overridable by client> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P2 | 143 | v | <per-tenant index or mandatory tenant field + enforced filter> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P2 | 144 | v | <forgetting the filter returns nothing, not everything> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P2 | 145 | v | <query as A never returns B's docs> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P2 | 145 | ii | docs | named gap — lowercase technical shorthand first use; no expansion on this page |
| P2 | 146 | v | <signals, boosts, tie-break, evaluation method, stable sort> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P2 | 147 | v | <facets/counts; stable sort/tiebreak → pagination-cursor-designer> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P2 | 152 | v | <each with risk-if-wrong / who answers> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P2 | 161 | i | HONEST | named gap — first use before any expansion on this page |
| P2 | 164 | i | BOTH | named gap — first use before any expansion on this page |
| P2 | 183 | i | ALL | documented exclusion — ordinary English all-caps emphasis/status word with plain meaning, not a coded identifier |
| P2 | 187 | v | 404s | documented exclusion — operator/unit token, not an abbreviation |
| P2 | 190 | iv | LIKE '%term%' | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P2 | 192 | iv | ILIKE | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P2 | 199 | i | WILL | named gap — first use before any expansion on this page |
| P2 | 217 | i | DESIGNS | named gap — first use before any expansion on this page |
| P2 | 218 | ii | repo | named gap — lowercase technical shorthand first use; no expansion on this page |
| P2 | 222 | ii | evals | named gap — lowercase technical shorthand first use; no expansion on this page |
| P2 | 222 | iii | evals.json | documented exclusion — exact file name/reference, not an abbreviation |
| P2 | 222 | iii | evals/evals.json | documented exclusion — exact file path/reference name, not an abbreviation |
| P2 | 222 | ii | json | named gap — lowercase technical shorthand first use; no expansion on this page |
| P2 | 225 | iii | evals/trigger-evals.json | documented exclusion — exact file path/reference name, not an abbreviation |
| P2 | 225 | iii | trigger-evals.json | documented exclusion — exact file name/reference, not an abbreviation |
| P2 | 228 | iii | references/ | documented exclusion — exact file path/reference name, not an abbreviation |
| P3 | 3 | i | DB | named gap — first use before any expansion on this page |
| P3 | 3 | i | MANUAL-ONLY | named gap — first use before any expansion on this page |
| P3 | 3 | i | NEXT_PUBLIC_ | defined-at-first-use — expanded on this line |
| P3 | 3 | i | NOT | documented exclusion — ordinary English all-caps emphasis/status word with plain meaning, not a coded identifier |
| P3 | 3 | i | RLS | named gap — first use before any expansion on this page |
| P3 | 3 | i | VITE_ | defined-at-first-use — expanded on this line |
| P3 | 9 | i | CD | named gap — first use before any expansion on this page |
| P3 | 9 | i | CI | named gap — first use before any expansion on this page |
| P3 | 11 | i | KMS | named gap — first use before any expansion on this page |
| P3 | 12 | ii | authz | named gap — lowercase technical shorthand first use; no expansion on this page |
| P3 | 28 | ii | repo | named gap — lowercase technical shorthand first use; no expansion on this page |
| P3 | 31 | i | CI- | named gap — first use before any expansion on this page |
| P3 | 37 | iv | appsec-implementer | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P3 | 39 | iv | rls-policy-auditor | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P3 | 41 | iv | threat-modeler | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P3 | 42 | i | REVIEW | named gap — first use before any expansion on this page |
| P3 | 43 | iv | security-pr-reviewer | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P3 | 47 | iii | .env | documented exclusion — exact file path/reference name, not an abbreviation |
| P3 | 50 | iv | REACT_APP_ | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P3 | 66 | iv | change-classification-gate | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P3 | 68 | iv | human-approval-boundary | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P3 | 73 | i | FAILS | named gap — first use before any expansion on this page |
| P3 | 83 | iv | HttpOnly | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P3 | 83 | iv | SameSite | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P3 | 83 | iv | Secure | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P3 | 88 | iv | reviewable-diff-discipline | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P3 | 90 | i | BFG | named gap — first use before any expansion on this page |
| P3 | 96 | v | <app/scope> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P3 | 96 | i | HARDENING | named gap — first use before any expansion on this page |
| P3 | 96 | i | IDENTITY | named gap — first use before any expansion on this page |
| P3 | 96 | i | SECRETS | named gap — first use before any expansion on this page |
| P3 | 97 | v | <var — public \| server-only \| CI-only \| deploy-only> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P3 | 98 | v | <name/location — how exposed> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P3 | 99 | v | <class> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P3 | 99 | v | <path / obtained?> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P3 | 100 | v | <cmd> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P3 | 100 | i | FAIL | documented exclusion — ordinary English all-caps emphasis/status word with plain meaning, not a coded identifier |
| P3 | 100 | i | PASS | documented exclusion — ordinary English all-caps emphasis/status word with plain meaning, not a coded identifier |
| P3 | 101 | v | <how> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P3 | 101 | v | <proxy> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P3 | 101 | v | <secret — moved to <store> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P3 | 102 | v | <credential — rotated? (approval) \| rotation still required> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P3 | 103 | v | <identity — grants removed → least privilege> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P3 | 104 | v | <flags/expiry/revocation added + tests> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P3 | 105 | v | <git history, secrets not yet rotated, out-of-scope stores> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P3 | 106 | v | <exact paths> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P3 | 116 | i | ROTATED | named gap — first use before any expansion on this page |
| P3 | 131 | i | VALUES | named gap — first use before any expansion on this page |
| P3 | 151 | i | XSS | defined-at-first-use — expanded on this line |
| P3 | 152 | i | CSRF | defined-at-first-use — expanded on this line |
| P3 | 171 | iii | secret-classification-and-rotation.md | documented exclusion — exact file name/reference, not an abbreviation |
| P3 | 174 | ii | evals | named gap — lowercase technical shorthand first use; no expansion on this page |
| P3 | 174 | iii | evals.json | documented exclusion — exact file name/reference, not an abbreviation |
| P3 | 174 | iii | evals/evals.json | documented exclusion — exact file path/reference name, not an abbreviation |
| P3 | 174 | ii | json | named gap — lowercase technical shorthand first use; no expansion on this page |
| P3 | 175 | iii | evals/trigger-evals.json | documented exclusion — exact file path/reference name, not an abbreviation |
| P3 | 175 | iii | trigger-evals.json | documented exclusion — exact file name/reference, not an abbreviation |
| P4 | 3 | iv | secrets-identity-hardener | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P4 | 4 | i | LOCATIONS | named gap — first use before any expansion on this page |
| P4 | 4 | i | NAMES | named gap — first use before any expansion on this page |
| P4 | 7 | iii | SKILL | documented exclusion — exact file/reference name, not an abbreviation |
| P4 | 7 | iii | SKILL.md | documented exclusion — exact file name/reference, not an abbreviation |
| P4 | 8 | i | API | named gap — first use before any expansion on this page |
| P4 | 9 | i | DB | named gap — first use before any expansion on this page |
| P4 | 9 | i | URL | named gap — first use before any expansion on this page |
| P4 | 10 | i | CI | named gap — first use before any expansion on this page |
| P4 | 10 | i | CRA | named gap — first use before any expansion on this page |
| P4 | 10 | i | KMS | named gap — first use before any expansion on this page |
| P4 | 11 | i | RLS | named gap — first use before any expansion on this page |
| P4 | 11 | i | XSS | named gap — first use before any expansion on this page |
| P4 | 12 | i | BFG | named gap — first use before any expansion on this page |
| P4 | 12 | i | CSRF | named gap — first use before any expansion on this page |
| P4 | 22 | i | CI- | named gap — first use before any expansion on this page |
| P4 | 23 | ii | id | named gap — lowercase technical shorthand first use; no expansion on this page |
| P4 | 23 | ii | repo | named gap — lowercase technical shorthand first use; no expansion on this page |
| P4 | 31 | i | ARTIFACT | defined-at-first-use — expanded on this line |
| P4 | 33 | iv | VITE_ | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P4 | 34 | iv | define | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P4 | 34 | iv | envPrefix | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P4 | 35 | iii | dist/ | documented exclusion — exact file path/reference name, not an abbreviation |
| P4 | 36 | i | NOT | documented exclusion — ordinary English all-caps emphasis/status word with plain meaning, not a coded identifier |
| P4 | 37 | iv | NEXT_PUBLIC_ | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P4 | 38 | iii | .env | documented exclusion — exact file path/reference name, not an abbreviation |
| P4 | 39 | iv | REACT_APP_ | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P4 | 54 | i | OLD | documented exclusion — ordinary English all-caps emphasis/status word with plain meaning, not a coded identifier |
| P4 | 64 | i | CAN | documented exclusion — ordinary English all-caps emphasis/status word with plain meaning, not a coded identifier |
| P4 | 64 | i | NEEDS | named gap — first use before any expansion on this page |
| P4 | 68 | i | BYPASSRLS | named gap — first use before any expansion on this page |
| P4 | 69 | iv | rls-policy-auditor | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P4 | 73 | iv | HttpOnly | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P4 | 73 | iv | SameSite | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P4 | 73 | iv | Secure | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P4 | 74 | i | XSS- | defined-at-first-use — expanded on this line |
| P5 | 3 | i | CI | named gap — first use before any expansion on this page |
| P5 | 3 | i | DDL | named gap — first use before any expansion on this page |
| P5 | 3 | i | GRANT | named gap — first use before any expansion on this page |
| P5 | 3 | i | NOT | documented exclusion — ordinary English all-caps emphasis/status word with plain meaning, not a coded identifier |
| P5 | 3 | i | RLS | named gap — first use before any expansion on this page |
| P5 | 3 | i | SAST | named gap — first use before any expansion on this page |
| P5 | 19 | iv | rls-policy-auditor | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P5 | 29 | iv | security-pr-reviewer | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P5 | 31 | i | CHECK | named gap — first use before any expansion on this page |
| P5 | 31 | i | DEFINER | named gap — first use before any expansion on this page |
| P5 | 31 | i | SECURITY | named gap — first use before any expansion on this page |
| P5 | 31 | i | USING | named gap — first use before any expansion on this page |
| P5 | 31 | i | WITH | documented exclusion — ordinary English all-caps emphasis/status word with plain meaning, not a coded identifier |
| P5 | 35 | iv | supply-chain-security-reviewer | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P5 | 36 | iv | static-analysis-reviewer | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P5 | 40 | i | ORM | named gap — first use before any expansion on this page |
| P5 | 47 | i | ENABLE | named gap — first use before any expansion on this page |
| P5 | 47 | iii | ENABLE/FORCE ROW LEVEL SECURITY | documented exclusion — exact file path/reference name, not an abbreviation |
| P5 | 47 | i | FORCE | named gap — first use before any expansion on this page |
| P5 | 47 | i | LEVEL | named gap — first use before any expansion on this page |
| P5 | 47 | i | ROW | named gap — first use before any expansion on this page |
| P5 | 48 | i | ALTER | named gap — first use before any expansion on this page |
| P5 | 48 | i | CREATE | named gap — first use before any expansion on this page |
| P5 | 48 | iv | CREATE ROLE | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P5 | 48 | iii | CREATE/ALTER POLICY | documented exclusion — exact file path/reference name, not an abbreviation |
| P5 | 48 | i | POLICY | named gap — first use before any expansion on this page |
| P5 | 48 | iv | REVOKE | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P5 | 48 | i | ROLE | named gap — first use before any expansion on this page |
| P5 | 48 | iv | SECURITY DEFINER | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P5 | 49 | iv | ALTER DEFAULT PRIVILEGES | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P5 | 49 | i | DEFAULT | named gap — first use before any expansion on this page |
| P5 | 49 | i | PRIVILEGES | named gap — first use before any expansion on this page |
| P5 | 50 | i | INSERT | named gap — first use before any expansion on this page |
| P5 | 50 | iv | INSERT … SELECT | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P5 | 50 | i | SELECT | named gap — first use before any expansion on this page |
| P5 | 50 | iv | UPDATE | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P5 | 57 | i | AND | documented exclusion — ordinary English all-caps emphasis/status word with plain meaning, not a coded identifier |
| P5 | 60 | iv | change-classification-gate | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P5 | 61 | iv | human-approval-boundary | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P5 | 69 | i | ALL | documented exclusion — ordinary English all-caps emphasis/status word with plain meaning, not a coded identifier |
| P5 | 69 | iv | GRANT ALL | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P5 | 70 | iv | anon | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P5 | 70 | i | BYPASSRLS | named gap — first use before any expansion on this page |
| P5 | 73 | iv | is_admin | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P5 | 73 | iv | role | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P5 | 78 | i | COLUMN | named gap — first use before any expansion on this page |
| P5 | 78 | i | DROP | named gap — first use before any expansion on this page |
| P5 | 78 | iii | DROP TABLE/COLUMN | documented exclusion — exact file path/reference name, not an abbreviation |
| P5 | 78 | i | TABLE | named gap — first use before any expansion on this page |
| P5 | 78 | iv | TRUNCATE | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P5 | 79 | iv | NOT NULL | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P5 | 79 | i | NULL | named gap — first use before any expansion on this page |
| P5 | 86 | i | FK | named gap — first use before any expansion on this page |
| P5 | 90 | iv | multi-tenant-security-tester | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P5 | 96 | v | <migration id/name> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P5 | 96 | ii | id | named gap — lowercase technical shorthand first use; no expansion on this page |
| P5 | 96 | i | MIGRATION | named gap — first use before any expansion on this page |
| P5 | 96 | i | REVIEW | named gap — first use before any expansion on this page |
| P5 | 96 | i | SECURE | named gap — first use before any expansion on this page |
| P5 | 97 | v | <present? adequate?> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P5 | 98 | v | <path / obtained?> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P5 | 100 | v | <security or safety issue> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P5 | 100 | v | <statement/line> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P5 | 100 | i | CRITICAL | documented exclusion — ordinary English all-caps emphasis/status word with plain meaning, not a coded identifier |
| P5 | 100 | i | HIGH | documented exclusion — ordinary English all-caps emphasis/status word with plain meaning, not a coded identifier |
| P5 | 100 | i | LOW | documented exclusion — ordinary English all-caps emphasis/status word with plain meaning, not a coded identifier |
| P5 | 100 | i | MEDIUM | documented exclusion — ordinary English all-caps emphasis/status word with plain meaning, not a coded identifier |
| P5 | 101 | v | <migration line / schema fact> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P5 | 101 | v | <remediation> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P5 | 102 | v | <gap?> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P5 | 102 | v | <route to rls-policy-auditor> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P5 | 102 | v | <unsafe?> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P5 | 102 | v | <widened?> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P5 | 103 | v | <backfill scope correct? credentials?> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P5 | 104 | v | <op — data loss? reversible?> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P5 | 105 | v | <expand/contract respected? breaks live code?> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P5 | 106 | v | <hot-table lock risk + online alternative> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P5 | 107 | v | <reversible cleanly \| forward-fix only \| irreversible (accepted?)> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P5 | 108 | v | <tenant/authz change → test> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P5 | 108 | ii | authz | named gap — lowercase technical shorthand first use; no expansion on this page |
| P5 | 109 | v | <...> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P5 | 110 | v | <areas + why> | documented exclusion — self-describing template placeholder (fill-in hole), not an abbreviation |
| P5 | 138 | iii | claude-skills-master-generation-prompts-v4.md | documented exclusion — exact file name/reference, not an abbreviation |
| P5 | 138 | ii | docs | defined-at-first-use — expanded on this line |
| P5 | 153 | iv | ALTER TABLE | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P5 | 167 | i | APPLY | named gap — first use before any expansion on this page |
| P5 | 172 | iii | migration-safety-checklist.md | documented exclusion — exact file name/reference, not an abbreviation |
| P5 | 175 | ii | evals | named gap — lowercase technical shorthand first use; no expansion on this page |
| P5 | 175 | iii | evals.json | documented exclusion — exact file name/reference, not an abbreviation |
| P5 | 175 | iii | evals/evals.json | documented exclusion — exact file path/reference name, not an abbreviation |
| P5 | 175 | ii | json | named gap — lowercase technical shorthand first use; no expansion on this page |
| P5 | 176 | iii | evals/trigger-evals.json | documented exclusion — exact file path/reference name, not an abbreviation |
| P5 | 176 | iii | trigger-evals.json | documented exclusion — exact file name/reference, not an abbreviation |
| P5 | 178 | iv | code-reviewer | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P6 | 3 | iii | SKILL | documented exclusion — exact file/reference name, not an abbreviation |
| P6 | 3 | iii | SKILL.md | documented exclusion — exact file name/reference, not an abbreviation |
| P6 | 5 | i | RLS | named gap — first use before any expansion on this page |
| P6 | 6 | iv | rls-policy-auditor | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P6 | 10 | i | ENABLE | named gap — first use before any expansion on this page |
| P6 | 10 | iv | ENABLE ROW LEVEL SECURITY | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P6 | 10 | i | LEVEL | named gap — first use before any expansion on this page |
| P6 | 10 | i | ROW | named gap — first use before any expansion on this page |
| P6 | 10 | i | SECURITY | named gap — first use before any expansion on this page |
| P6 | 15 | i | FORCE | named gap — first use before any expansion on this page |
| P6 | 15 | iv | FORCE ROW LEVEL SECURITY | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P6 | 16 | i | ALL | documented exclusion — ordinary English all-caps emphasis/status word with plain meaning, not a coded identifier |
| P6 | 16 | iv | GRANT | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P6 | 16 | iv | GRANT ALL | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P6 | 16 | iv | REVOKE | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P6 | 17 | i | ALTER | named gap — first use before any expansion on this page |
| P6 | 17 | iv | ALTER DEFAULT PRIVILEGES | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P6 | 17 | iv | anon | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P6 | 17 | iv | BYPASSRLS | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P6 | 17 | i | DEFAULT | named gap — first use before any expansion on this page |
| P6 | 17 | i | PRIVILEGES | named gap — first use before any expansion on this page |
| P6 | 17 | iv | public | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P6 | 19 | i | DEFINER | named gap — first use before any expansion on this page |
| P6 | 19 | iv | SECURITY DEFINER | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P6 | 22 | iv | is_admin default true | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P6 | 22 | iv | tenant_id | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P6 | 27 | i | INSERT | named gap — first use before any expansion on this page |
| P6 | 27 | iv | INSERT … SELECT | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P6 | 27 | i | SELECT | named gap — first use before any expansion on this page |
| P6 | 27 | i | SET | named gap — first use before any expansion on this page |
| P6 | 27 | i | UPDATE | named gap — first use before any expansion on this page |
| P6 | 27 | iv | UPDATE … SET | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P6 | 30 | i | QUERY | named gap — first use before any expansion on this page |
| P6 | 37 | i | COLUMN | named gap — first use before any expansion on this page |
| P6 | 37 | i | DROP | named gap — first use before any expansion on this page |
| P6 | 37 | i | TABLE | named gap — first use before any expansion on this page |
| P6 | 38 | i | TRUNCATE | named gap — first use before any expansion on this page |
| P6 | 39 | i | NOT | documented exclusion — ordinary English all-caps emphasis/status word with plain meaning, not a coded identifier |
| P6 | 39 | i | NULL | named gap — first use before any expansion on this page |
| P6 | 59 | i | CONCURRENTLY | defined-at-first-use — expanded on this line |
| P6 | 59 | i | CREATE | defined-at-first-use — expanded on this line |
| P6 | 59 | iv | CREATE INDEX CONCURRENTLY | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P6 | 59 | i | INDEX | defined-at-first-use — expanded on this line |
| P6 | 59 | i | PG | defined-at-first-use — expanded on this line |
| P6 | 61 | i | CONSTRAINT | named gap — first use before any expansion on this page |
| P6 | 61 | i | FK | named gap — first use before any expansion on this page |
| P6 | 61 | iv | NOT VALID | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P6 | 61 | i | VALID | named gap — first use before any expansion on this page |
| P6 | 61 | i | VALIDATE | named gap — first use before any expansion on this page |
| P6 | 61 | iv | VALIDATE CONSTRAINT | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P6 | 70 | i | AND | documented exclusion — ordinary English all-caps emphasis/status word with plain meaning, not a coded identifier |
| P6 | 72 | iv | human-approval-boundary | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P6 | 74 | ii | authz | defined-at-first-use — expanded on this line |
| P6 | 77 | i | DB | defined-at-first-use — expanded on this line |
| P6 | 78 | iv | multi-tenant-security-tester | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P7 | 3 | i | A09 | named gap — first use before any expansion on this page |
| P7 | 3 | i | AFTER | documented exclusion — ordinary English all-caps emphasis/status word with plain meaning, not a coded identifier |
| P7 | 3 | i | ALERTING | named gap — first use before any expansion on this page |
| P7 | 3 | ii | authn | defined-at-first-use — expanded on this line |
| P7 | 3 | i | DETECTION | named gap — first use before any expansion on this page |
| P7 | 3 | i | NOT | documented exclusion — ordinary English all-caps emphasis/status word with plain meaning, not a coded identifier |
| P7 | 3 | i | OWASP | named gap — first use before any expansion on this page |
| P7 | 3 | i | RECORD | named gap — first use before any expansion on this page |
| P7 | 3 | i | WIRING | named gap — first use before any expansion on this page |
| P7 | 34 | i | MONITORING | named gap — first use before any expansion on this page |
| P7 | 36 | iv | audit-log-architect | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P7 | 38 | i | ON | named gap — first use before any expansion on this page |
| P7 | 38 | i | TOP | named gap — first use before any expansion on this page |
| P7 | 39 | i | EDITING | named gap — first use before any expansion on this page |
| P7 | 40 | iv | observability-operator | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P7 | 43 | iv | slo-reliability-architect | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P7 | 46 | iv | cloud-security-baseline-reviewer | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P7 | 49 | i | DO | named gap — first use before any expansion on this page |
| P7 | 50 | iv | incident-response-runbook | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P7 | 51 | i | FIRES | named gap — first use before any expansion on this page |
| P7 | 56 | iv | ai-threat-modeler | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P7 | 56 | iv | threat-modeler | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P7 | 82 | iii | security-event-coverage-sheet.md | documented exclusion — exact file name/reference, not an abbreviation |
| P7 | 90 | ii | id | named gap — lowercase technical shorthand first use; no expansion on this page |
| P7 | 185 | i | D8 | named gap — first use before any expansion on this page |
| P7 | 185 | ii | repo | named gap — lowercase technical shorthand first use; no expansion on this page |
| P7 | 187 | iv | framework-edition-tracker | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P7 | 195 | i | EDIT | named gap — first use before any expansion on this page |
| P7 | 211 | ii | evals | defined-at-first-use — expanded on this line |
| P7 | 211 | iii | evals.json | documented exclusion — exact file name/reference, not an abbreviation |
| P7 | 211 | ii | json | defined-at-first-use — expanded on this line |
| P7 | 214 | iii | trigger-evals.json | documented exclusion — exact file name/reference, not an abbreviation |
| P8 | 5 | ii | id | named gap — lowercase technical shorthand first use; no expansion on this page |
| P8 | 13 | iii | SKILL | documented exclusion — exact file/reference name, not an abbreviation |
| P8 | 13 | iii | SKILL.md | documented exclusion — exact file name/reference, not an abbreviation |
| P8 | 14 | i | IP | named gap — first use before any expansion on this page |
| P8 | 15 | ii | authz | named gap — lowercase technical shorthand first use; no expansion on this page |
| P8 | 15 | i | MFA | named gap — first use before any expansion on this page |
| P8 | 16 | i | IDOR | named gap — first use before any expansion on this page |
| P8 | 16 | i | RLS | named gap — first use before any expansion on this page |
| P8 | 17 | i | API | named gap — first use before any expansion on this page |
| P8 | 17 | i | WAF | named gap — first use before any expansion on this page |
| P8 | 18 | i | AI | named gap — first use before any expansion on this page |
| P8 | 18 | i | SSRF | named gap — first use before any expansion on this page |
| P8 | 19 | i | HTTP | named gap — first use before any expansion on this page |
| P8 | 19 | iv | N | documented exclusion — exact command/identifier/code span, not a prose abbreviation |
| P8 | 27 | v | 403s | documented exclusion — operator/unit token, not an abbreviation |
| P8 | 27 | i | IDOR- | defined-at-first-use — expanded on this line |
| P8 | 27 | ii | ids | named gap — lowercase technical shorthand first use; no expansion on this page |
| P8 | 30 | i | SSRF- | named gap — first use before any expansion on this page |
| P8 | 30 | i | WAF- | named gap — first use before any expansion on this page |
| P2 | 139 | D backticked/placeholder/unit/operator | <sync vs async; write→searchable path; FRESHNESS LAG stated; reindex/backfill; delete + permission-change propagation to index> | documented exclusion — self-describing multiline template placeholder (fill-in hole), not an abbreviation |
| P2 | 148 | D backticked/placeholder/unit/operator | <index growth, reindex cost, freshness/error monitoring, engine-down degrade behavior> | documented exclusion — self-describing multiline template placeholder (fill-in hole), not an abbreviation |

## 5. Inventory counts, reconciliation and zero-duplicate proof

| Page | (i) | (ii) | (iii) | (iv) | (v) | Rows | Named gaps | Defined | Exclusions |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P1 | 9 | 2 | 2 | 11 | 8 | 32 | 11 | 0 | 21 |
| P2 | 20 | 4 | 5 | 12 | 11 | 52 | 19 | 1 | 32 |
| P3 | 22 | 4 | 6 | 11 | 14 | 57 | 19 | 4 | 34 |
| P4 | 20 | 2 | 4 | 10 | 0 | 36 | 17 | 2 | 17 |
| P5 | 40 | 5 | 9 | 21 | 19 | 94 | 36 | 1 | 57 |
| P6 | 32 | 1 | 2 | 20 | 0 | 55 | 24 | 6 | 25 |
| P7 | 16 | 5 | 3 | 8 | 0 | 32 | 16 | 3 | 13 |
| P8 | 12 | 3 | 2 | 1 | 1 | 19 | 14 | 1 | 4 |
| **Total** | **171** | **26** | **33** | **94** | **53** | **377** | **156** | **18** | **203** |

**Zero-duplicate proof:** final table rows = 377 = unique (page, line, token) keys = 377; duplicate keys = 0; extra rows after the final table = 0; per-page/class/disposition sums equal the row count; one contiguous table only, no second inventory table.


**Documented-exclusion placeholders added in this repair (SD-D REVISE 6248561626):** P2 (249) L139-140 and L148-149 are two self-describing multiline class-D template placeholders; each is a documented exclusion in the final table and not a named B2 gap. This is the only table change; both rows resolve to the pinned page text.

**Reconciliation:** section 3 B2/verdicts and section 5 named-gap list agree with this table: every page is PARTIAL under the strict FULL bar because canonical B6 is UNVERIFIED and named B2 gaps are named; no page is FULL/keeper-eligible, and no undocumented first use is omitted.

## 6. AC1-AC8 status at this Stage C handoff

| AC | Status | Evidence |
| --- | --- | --- |
| AC1 one-path | MET | exactly one added record path; no other path |
| AC2 frozen pages | MET | eight blobs/bytes/LF; 63,988/1,085; zero drift; no page outside set |
| AC3 whole-page + exact-once inventory | MET in this record | canonical B1-B6 per page; one contiguous inventory; zero duplicates; real first-use lines |
| AC4 honest dispositions | MET in this record | 0 FULL / 8 PARTIAL / 0 UNRUN; B6 UNVERIFIED; no keeper |
| AC5 record/body/PROC-04 + self-state | C handoff | record facts and body binding; PROC-04 and self-state proof in PR body/handoff |
| AC6 Codex | C handoff | trigger/state recorded; never a pass; D/E/F/G own final audit |
| AC7 provenance | MET | plan 6248432832 + B 6248458364; base e7acaca4; merge attribution/reservations accurate; no keeper/index/etc. change |
| AC8 stage entry | MET | fresh B ACCEPT bound to plan; branch from live main e7acaca4; one DCO model commit; D/E/F/G separate; no merge |

## 7. Authorship chain and stage boundary

| Stage | Agent / artifact |
| --- | --- |
| A plan | sd-e-802-r1 / sd-a-read-b18-r1 - plan 6248432832 (standalone no-matching-skill statement included verbatim in the plan) |
| B audit | sd-b-read-b18-b1 - B ACCEPT 6248458364 (canonical B1-B6) |
| C record | sd-d-793-r2 / sd-c-read-b18-c1 - this record, one DCO model commit |
| D/E/F/G | separate stages; no merge authority here |

**Boundary.** Stage C only: no page edit, no plan file, no keeper/index/ledger/register/manifest/tool/test/workflow change, no other PR touched, no merge. The record is the self-cost entry of this batch and remains pending; no keeper row is claimed.

**Signed with both names: sd-d-793-r2 (true identity) - sd-c-read-b18-c1 (stage role).** **Written by: DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness).**
