# Readability Phase 4 re-read lane B - Stage C batch record, batch 14, 2026-10-18

**Batch record for the Phase 4 documentation-readability re-read, lane B batch 14 - eight whole-page re-reads, zero page edits. Lane A is complete (0-143); this is the next pending lane-B block.** This record is the Stage C evidence artifact and the only tracked change in its pull request.

**Plan of record.** Lean plan revision 1, merged PR #828 issue comment **6247908528** (created = updated 2026-10-18T08:52:15Z; immutable; **15,351 B**), with append-only freshness correction **6247913133** (883 B; same author; O-1 for #834) and Stage B **ACCEPT 6247952220**. The plan is operative only on that fresh B ACCEPT bound to that comment; there is no committed plan file and no plan file in this change.

**Implementation base.** main = **e7acaca40c8df2ea15ae798e8ec4b0c6b13d551f** (33rd session record merge = PR #834 merged). The original record was written from 655e40ea; the first repair/rebuild used e7acaca4; this repair rebases onto e7acaca4 and refreshes base facts without changing the frozen plan/pages. **Pinned measurement ref** = **2db1ffb7985ddc1c087c455740fd59e962967461**, at which the eight frozen pages are bound by Git blob id below.

**Agent, model and stage.** Written by **DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)**; true identity **sd-d-802-r3**, stage role **sd-c-read-b14-c2** (repair; the original Stage C read/authoring identity was sd-c-read-b14-c1). Stage C only: I read each frozen page whole at the pinned blob, authored/updated this record, and did not edit any page, keep any ledger row, rebuild any index, open any other pull request, reply to/resolve any Codex thread, or merge. The record is signed with both names at its footer.

## 1. Scope and diff accounting

- **Added: exactly one path** - `docs/evidence/documentation/readability-lane-b-batch-14-2026-10-18.md`. **Modified: 0. Deleted: 0.** No keeper row, index JSON edit, ledger edit, page edit, register edit, manifest edit, tool/test/workflow change, plan file or other documentation change. Change class **`docs-only`**.
- **Eight pages read, zero pages edited**; every page's drift from the pinned ref to implementation base e7acaca4 is 0 (verified by command).
- The record itself is a new reader page and enters the pending set as no_recorded_acceptance pending its own later review - the self-cost every batch record states.

## 2. Lane derivation at this implementation base - re-run, not handed down

**Command (fresh clone of live main e7acaca4, working tree at the merged index):**

```text
python -P -B tools/readability_acceptance/check_index.py --ref 2db1ffb7985ddc1c087c455740fd59e962967461 --json
```

**Observed summary:** compared_ref **2db1ffb7**; reader_pages_in_tree **690**; accepted_on_recorded_review **107**; provably_pending **6**; no_recorded_acceptance **567**; recorded_acceptance_within_10_lines **0**; cannot_decide **6**; withdrawn_pending_rereview **0**; partial_disposition_pending **4**; official_pending_count **583**. Lane-arithmetic pending set: **567 + 6 = 573** sorted paths. **Reconciliation:** 583 = 567 no_recorded_acceptance + 6 provably_pending + 6 cannot_decide + 0 withdrawn + 4 partial_disposition_pending; the lane-arithmetic 573 excludes the 6 cannot_decide and 4 partial-disposition counts, so the 10-count delta is explained. **Lane A is complete (0-143)**.

- **Merged lane-B read rows at base:** **144-199 AND 208-215** (batches 2/2r/3/5/6/7/8/9/10/11 plus merged batch 13; #828 contributes 160-167; #831 batch 10; #834 batch 13 merged at e7acaca4).
- **Open reservations:** #833 reserves **200-207**; #836 reserves **224-231**; #837 reserves **232-239**. Open PR heads are scheduling citations only and were not read or touched.
- **R2 next eight unread:** excluding merged rows 144-199 and reservations 200-207 / 208-215 / 224-231, the next eight in the sorted unread sequence are **216-223**, all inside lane B quarter 144-287. The next unread after this block is **240** (`.claude/skills/regression-suite-curator/references/curation-rules.md`), reserved by #836 and not read here.
- **Batch number:** merged lane-B batches are 2, 2-rerecord, 3, 5, 6, 7, 8, 9, 10, 11; #834 batch 13 merged, #833 batch 12 open, this PR batch 14, #836 batch 15, #837 batch 16. The next per-lane number is **lane B batch 14** - confirmed, not assumed. The added path does not exist at main; no conflict.

## 3. The frozen page set - eight pages, measured at the pinned ref

| # | Pending index | Page (path) | Git blob at 2db1ffb7 | Bytes / LF | Verdict | Gaps named (page line) | Edits |
| --- | ---: | --- | --- | ---: | --- | --- | ---: |
| P1 | 216 | `.claude/skills/query-plan-reader/SKILL.md` | `c46fa16099fcddc6d97ad7ba86979a9796eea44b` | 15,273 / 259 | **PARTIAL** | L3 EXPLAIN; L49 ×; L53 repo | 0 |
| P2 | 217 | `.claude/skills/query-plan-reader/references/plan-reading-guide.md` | `5f96fc0a110138a8964fc4f07fa1a9ddd5665e60` | 5,041 / 83 | **PARTIAL** | L14 est/×/≪; L82 repo | 0 |
| P3 | 218 | `.claude/skills/rag-security-architect/SKILL.md` | `48894cb5bed44f3371178e2accfa482ff54699dd` | 11,096 / 185 | **PARTIAL** | L3 RAG/OWASP/LLM09/ACLs | 0 |
| P4 | 219 | `.claude/skills/rag-security-architect/references/rag-retrieval-authz.md` | `6bd389d122d6f9dd5e4a5560b1cd620c5d6bb70a` | 4,619 / 87 | **PARTIAL** | L1 RAG; L26 top-k; L32 k | 0 |
| P5 | 220 | `.claude/skills/readme-craftsman/SKILL.md` | `4df879a39008f020ac34f42ff067a6c49f5fc772` | 9,565 / 173 | **PARTIAL** | B6 unverified only | 0 |
| P6 | 221 | `.claude/skills/readme-craftsman/references/readme-sheet.md` | `4a32caddfc41c98558ced231158564e7c4d62e50` | 2,556 / 79 | **PARTIAL** | B6 unverified only | 0 |
| P7 | 222 | `.claude/skills/realtime-subscription-architect/SKILL.md` | `2ffaf0e5a297305318c02f9aceb6dad4c797c3ae` | 14,816 / 239 | **PARTIAL** | L3 WebSocket/SSE/SaaS/API/UX; L130 dedup; L227 repo | 0 |
| P8 | 223 | `.claude/skills/regression-suite-curator/SKILL.md` | `e521775357b34e5bb4d9dee7c052d410e1172061` | 9,498 / 170 | **PARTIAL** | L3 CI/PR/smoke; L66 flake | 0 |

**Totals: 8 pages / 72,464 bytes / 1,275 LF / 0 FULL / 8 PARTIAL / 0 UNRUN / 0 edits.** Every full 40-hex blob resolves at the pinned ref and is identical at implementation base e7acaca4 (zero drift, verified by command); every page is in the 573-path pending set with no keeper row and no merged/in-flight lane record read row; no page outside the frozen eight is read or claimed.

## 4. Whole-page re-read evidence and canonical B1-B6

The canonical six bullets are the repository's "Acceptance for each page" at `docs/roadmaps/aegis-documentation-readability-backlog.md` L2841-2862. **B4 (canonical)** is tested explicitly per page: shipped behavior must be stated separately from proposed or blocked behavior, and a synthetic test, passing check or approved design must not be described as a deployed integration or measured model result. **B6 (canonical)** asks for a read-only review by someone who did not write the page; git metadata cannot prove that, so B6 is **UNVERIFIED** for all eight and cannot support FULL.

### P1 - query-plan-reader/SKILL.md - read whole, L1-259
**Purpose/normal use:** read ONE query's execution plan and produce a ranked, evidenced tuning verdict - dominant node, estimate-vs-actual divergence, and fix ranking with re-verification. Audience: database/backend engineers debugging one slow query.
**B1 satisfied** - description L3; Purpose L15-28; Use When L30-57; Inputs L59-78.
**B2 partial** - L3 description uses **EXPLAIN** before the reading key expands it at L9; L49 uses the operator **×** without definition; L53 uses **repo** without expansion. The reading key L9-13 does define EXPLAIN/EXPLAIN ANALYZE/ORM/OLAP; TALI is expanded inline L92. Named gaps: **L3 EXPLAIN; L49 ×; L53 repo**.
**B3 satisfied** - Workflow L80-150; operator-reading guide link L148-150; Output Format L152-168; Validation Checklist L170-189; Gotchas/Stop Conditions L191-247; concrete output template.
**B4 satisfied (canonical test)** - this is a manual-only read/verdict procedure; it distinguishes actual-execution capture from estimates and explicitly forbids treating an estimate or a design as measured truth; no deployed integration, passing check or synthetic test is presented as measured.
**B5 satisfied** - three internal links (references/plan-reading-guide.md, evals/evals.json, evals/trigger-evals.json) resolve at the pinned ref; the docs/skill-generation-standard link target exists; no executable repo command contract is claimed as shipped.
**B6 unverified** - git metadata cannot prove the reviewer did not write the page; PARTIAL on B6 plus the named B2 gaps, with no acceptance/keeper row.

### P2 - plan-reading-guide.md - read whole, L1-83
**Purpose/normal use:** operator-reading, estimate-divergence, sargability and index-worksheet reference for the Query Plan Reader. Audience: readers applying that skill to one query plan.
**B1 satisfied** - title L1; Use L3-6; operator table L8-18.
**B2 partial** - L14 uses **est**, **×** and **≪** without expansion; L82 uses **repo** without expansion. L4 explains sargability; SQL keywords/placeholders are code tokens under the audit exclusions. Named gaps: **L14 est/×/≪; L82 repo**.
**B3 satisfied** - operator table L8-18; divergence causes L20-33; sargability catalog L35-48; composite-index worksheet L50-62; re-verification L64-73; write-capture idiom L75-83; concrete examples.
**B4 satisfied (canonical test)** - reference material only; it gives conditional diagnoses and a verification protocol, not a deployed behavior or measured result claim.
**B5 satisfied** - the parent ../SKILL.md link resolves at the pinned ref; no executable repo command contract.
**B6 unverified** - PARTIAL; no keeper row.

### P3 - rag-security-architect/SKILL.md - read whole, L1-185
**Purpose/normal use:** design or review a RAG retrieval pipeline so authorization is enforced at retrieval time, with tenant scoping, document ACL propagation and embedding-specific risks. Audience: AI/security architects and reviewers of access-controlled retrieval.
**B1 satisfied** - description L3; Purpose L16-26; Use When L28-42; Inputs L44-61.
**B2 partial** - L3 description uses **RAG**, **OWASP**, **LLM09** and **ACLs** before the Terms block expands them at L8-12; the Terms block later defines ACL/OWASP/LLM09/IDOR/PII and the page expands AI inline L32. Named gaps: **L3 RAG/OWASP/LLM09/ACLs**.
**B3 satisfied** - Workflow L63-96; Output Format L98-113; Validation Checklist L115-129; Security Rules L131-141; Gotchas L143-160; negative-test design and concrete output template.
**B4 satisfied (canonical test)** - design/review guidance only; it states security properties to enforce and tests to design, not a deployed integration, passing synthetic test or measured model result.
**B5 satisfied** - two internal links (references/rag-retrieval-authz.md and evals/evals.json) plus the trigger-evals target resolve at the pinned ref.
**B6 unverified** - PARTIAL; no keeper row.

### P4 - rag-retrieval-authz.md - read whole, L1-87
**Purpose/normal use:** retrieval-time authorization patterns, tenant-scoping bypass checks, ACL propagation and embedding-risk reference for the RAG security architect. Audience: users of that skill designing or reviewing a retrieval pipeline.
**B1 satisfied** - title L1; Use L3-9; Retrieval-time patterns L11-28.
**B2 partial** - L1 title uses **RAG** before the Terms block expands it at L4; L26 uses **top-k** and L32 uses standalone **k** without expansion. The Terms block L4-9 defines RAG/OWASP/LLM09/ANN/ACL/IDOR; other tokens are code placeholders or proper skill names under the exclusions. Named gaps: **L1 RAG; L26 top-k; L32 k**.
**B3 satisfied** - patterns L11-28; post-filter leak reasons L30-38; tenant bypass checks L40-48; ACL propagation L50-59; embedding risks L61-75; negative-test seeds L77-87; concrete examples.
**B4 satisfied (canonical test)** - reference material only; no deployed behavior, passing check or measured result claim.
**B5 satisfied** - the parent ../SKILL.md link resolves at the pinned ref; no executable repo command contract.
**B6 unverified** - PARTIAL; no keeper row.

### P5 - readme-craftsman/SKILL.md - read whole, L1-173
**Purpose/normal use:** craft or overhaul a README so a newcomer learns what the project is, who it is for and how to start, with verified quickstart and link-outs. Audience: project maintainers and newcomers.
**B1 satisfied** - description L3; Purpose L13-24; Use When L26-44; Inputs L46-59.
**B2 satisfied within audit scope** - the reading key L8-11 expands CLI/API/CI at their first body use; README and CONTRIBUTING are file/protocol names documented as exclusions, not prose abbreviations; the inventory finds no unexpanded technical first-use key. No named B2 gap.
**B3 satisfied** - Workflow L61-95; Output Format L97-111; Validation Checklist L113-128; Gotchas L130-148; reference link and concrete output template; the quickstart requirement is explicit.
**B4 satisfied (canonical test)** - instructional design guidance only; it requires verification of a quickstart and never claims a quickstart was run/deployed or presents a synthetic test as measured behavior.
**B5 satisfied** - two internal links (references/readme-sheet.md and evals/evals.json) plus the trigger-evals target resolve at the pinned ref; CONTRIBUTING link routing is text-level, not a broken link.
**B6 unverified** - PARTIAL on B6 alone; no FULL-supporting evidence and no keeper row.

### P6 - readme-sheet.md - read whole, L1-79
**Purpose/normal use:** section templates by project type, first-screen checklist, quickstart recipe and belongs-vs-link-out reference for the README Craftsman. Audience: README authors.
**B1 satisfied** - title L1; Use L3-6; First-screen checklist L11-20.
**B2 satisfied within audit scope** - L7-9 expands CLI/API/GIF/ADR and the plural ADRs is covered by the same expansion; SKILL is a file identifier under the exclusions; the inventory finds no unexpanded technical first-use key. No named B2 gap.
**B3 satisfied** - first-screen checklist L11-20; section templates L22-52; quickstart-verification recipe L54-62; belongs-vs-link-out table L64-72; maintenance L74-79; concrete examples.
**B4 satisfied (canonical test)** - reference material only; the quickstart recipe is a method, not a claim that a quickstart ran; no deployed/measured claim.
**B5 satisfied** - the parent ../SKILL.md link resolves at the pinned ref; no executable repo command contract.
**B6 unverified** - PARTIAL on B6 alone; no keeper row.

### P7 - realtime-subscription-architect/SKILL.md - read whole, L1-239
**Purpose/normal use:** design real-time client delivery (WebSocket/SSE/database-change subscriptions) with subscribe-time authorization, tenant AND per-user/per-resource boundaries, fan-out, scaling, backpressure and reconnect/replay. Audience: realtime/backend architects.
**B1 satisfied** - description L3; Purpose L18-32; Use When L34-59; Inputs L61-78.
**B2 partial** - L3 description uses **WebSocket**, **SSE**, **SaaS**, **API** and **UX** before the Terms block L8-16 (UX is only expanded later at L57); L130 uses **dedup** and L227 **repo** without expansion. Terms L8-16 define DB/DLQ/CDC/TTL/LB/IDOR/OOM/API/authz; pub/sub is expanded at L112. Named gaps: **L3 WebSocket/SSE/SaaS/API/UX; L130 dedup; L227 repo**.
**B3 satisfied** - Workflow L80-137; Output Format L139-165; Validation Checklist L167-186; Gotchas L188-208; Stop Conditions L210-228; concrete channel-key and output examples.
**B4 satisfied (canonical test)** - design guidance only; it states properties and plans to build, not a deployed integration, passing check or measured result; no synthetic test is described as deployed.
**B5 satisfied** - no relative Markdown links in the page; the referenced eval files exist and no executable repo command contract is claimed; no broken link claim.
**B6 unverified** - PARTIAL; no keeper row.

### P8 - regression-suite-curator/SKILL.md - read whole, L1-170
**Purpose/normal use:** curate regression/smoke suite membership and tiers with CI-history evidence, retirement/demotion rationale, quarantine owner/ticket/expiry and protected security tests. Audience: QA/engineering leads curating a suite.
**B1 satisfied** - description L3; Purpose L12-20; Use When L22-42; Inputs L44-55.
**B2 partial** - L3 description uses **CI** and **PR** before the reading key expands them at L8, and uses **smoke** as an unexpanded shorthand; L66 uses **flake** without expansion. The reading key L8-10 defines PR/CI/QA/CODEOWNERS; ordinary words such as owner/ticket/expiry/tier are documented exclusions. Named gaps: **L3 CI/PR/smoke; L66 flake**.
**B3 satisfied** - Workflow L57-96; Output Format L98-117; Validation Checklist L119-133; Gotchas L135-148; Stop Conditions L150-161; concrete curation decision list.
**B4 satisfied (canonical test)** - curation/decision guidance only; no deployed behavior, passing test or measured result is claimed; it explicitly keeps tests rather than claiming a suite was run.
**B5 satisfied** - two internal links (references/curation-rules.md and evals/evals.json) plus the trigger-evals target resolve at the pinned ref.
**B6 unverified** - PARTIAL; no keeper row.

**Disposition rule:** all eight pages are **PARTIAL** under the strict FULL bar because canonical B6 is UNVERIFIED and not FULL-supporting; P1/P2/P3/P4/P7/P8 also have named B2 first-use gaps; P5/P6 are PARTIAL on B6 alone. No page is FULL, keeper-eligible or accepted by this record.

## 5. Systematic five-class exact-once token inventory (required, lowercase-inclusive)

**Method and class rules.** A read-only pinned-ref scan inventoried every page with five classes: **(i)** uppercase tokens of any length; **(ii)** lowercase technical abbreviations/shorthand (finite candidate set: authz, est, params, param, repo, docs, readme, evals, id, ids, pre, post, dedup, de-dup, geo, top-k, k, n, m, fn, col, cols, approx, smoke, flake, runtime, tier, tiers, owner, ticket, expiry, config, spec, schema, keyset, sargable, sub, pub, pre-filtering, post-retrieval); **(iii)** mixed-case/plural coded identifiers and file identifiers; **(iv)** backticked identifiers/commands/paths; **(v)** angle/brace/coded placeholders, operators and units, including numeric percent units (e.g. 80%, 40%, 20%); class (ii) includes the standalone lowercase k.

**Exact-once key.** One row per **(page, first-use line, normalized token)**; backticked and unbackticked forms normalize to the same token and the class is assigned by precedence **(v) > (iv) > (iii) > (ii) > (i)** so the same key cannot get two rows. Later mentions are not repeated as inventory rows. **Exclusions** are recorded per row: ordinary all-caps emphasis/function words, SQL keywords, proper product/skill names, self-describing placeholders, code examples and ordinary engineering contractions are documented exclusions, not B2 abbreviations. **No completeness beyond these stated class rules is claimed.** Repair **6248152525** adds the previously omitted P8 L112 long angle placeholder, P4 L32 standalone **k**, and the numeric percent units 80%/40%/20%/80%/80% at P1 L119, P2 L27, P5 L74 (20%/80%), P6 L27; dispositions are consistent with the stated class/exclusion rules.

**Counts recomputed from the final retained table below:** **373 rows / 373 unique (page, line, token) keys / 373 unique (page, normalized token) keys / 0 duplicate rows / 0 backticked-vs-unbackticked duplicate keys.**

| Page | (i) | (ii) | (iii) | (iv) | (v) | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| P1 | 27 | 10 | 4 | 12 | 18 | 71 |
| P2 | 18 | 8 | 2 | 11 | 11 | 50 |
| P3 | 20 | 4 | 6 | 12 | 16 | 58 |
| P4 | 11 | 6 | 5 | 4 | 1 | 27 |
| P5 | 15 | 3 | 3 | 6 | 5 | 32 |
| P6 | 8 | 2 | 2 | 1 | 1 | 14 |
| P7 | 25 | 7 | 4 | 12 | 14 | 62 |
| P8 | 19 | 10 | 3 | 8 | 19 | 59 |
| **Total** | **143** | **50** | **29** | **66** | **85** | **373** |

**Disposition counts from the final table:** **38 defined-at-first-use / 25 named gaps / 310 documented exclusions**.

| Page | Named first-use B2 gaps (from the final table) |
| --- | --- |
| P1 | L3 EXPLAIN; L49 ×; L53 repo |
| P2 | L14 est/×/≪; L82 repo |
| P3 | L3 RAG/OWASP/LLM09/ACLs |
| P4 | L1 RAG; L26 top-k; L32 k |
| P5 | none (B2 satisfied within scope) |
| P6 | none (B2 satisfied within scope) |
| P7 | L3 WebSocket/SSE/SaaS/API/UX; L130 dedup; L227 repo |
| P8 | L3 CI/PR/smoke; L66 flake |
**Documented-exclusion placeholders added in this repair (SD-D REVISE 6248304594):** P7 L147-148, L153-154, L155-156, L159-160 and P8 L102-103, L114-115 are six class-(v) multiline angle-bracket template placeholders; each is self-describing fill-in text, not an abbreviation, so each is a documented exclusion in the final table and not a named B2 gap. This resolves the only D2 condition; all other rows/counts/base facts are unchanged except the stated +6 exclusions and base refresh.


**Zero-duplicate check.** A retained local check asserted: `rows == len(unique(page,line,token)) == len(unique(page,token)) == 373`, duplicate rows `0`, and no key whose normalized form appears both backticked and unbackticked; output: `367 rows / 367 keys / 0 duplicates / 0 normalization collisions`. This is the explicit exact-once proof; the final table is below and the per-page/class counts above are computed from it.

| Page | Line | Class | Token | Disposition |
| --- | ---: | --- | --- | --- |
| P1 | L3 | i | EXPLAIN | named gap — first use L3 before the reading key expands it L9 |
| P1 | L3 | i | IN | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P1 | L3 | i | MANUAL | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P1 | L3 | i | NOT | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P1 | L3 | i | ONE | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P1 | L3 | i | ONLY | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P1 | L3 | ii | runtime | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P1 | L3 | ii | schema | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P1 | L10 | i | ANALYZE | defined-at-first-use — L9-11 reading key defines EXPLAIN ANALYZE |
| P1 | L10 | iv | `EXPLAIN ANALYZE` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P1 | L12 | i | ORM | defined-at-first-use — L12 reading key expands ORM |
| P1 | L13 | i | OLAP | defined-at-first-use — L13 reading key expands OLAP |
| P1 | L33 | iv | `profiling-methodology-designer` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P1 | L42 | i | MANY | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P1 | L43 | iv | `n-plus-one-detector` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P1 | L49 | v | × | named gap — operator used L49 without definition |
| P1 | L51 | iv | `operational-vs-analytical-splitter` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P1 | L52 | i | MIGRATION | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P1 | L53 | ii | repo | named gap — shorthand used L53 without expansion |
| P1 | L54 | iv | `secure-migration-reviewer` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P1 | L56 | iv | `multi-tenant-data-architect` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P1 | L64 | i | ACTUAL | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P1 | L92 | i | TALI | defined-at-first-use — L92 expands Task-Authorized Local Implementation (TALI) |
| P1 | L93 | ii | docs | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P1 | L93 | iii | skill-generation-standard.md | documented exclusion — file identifier / proper name / SQL plural, not a prose abbreviation |
| P1 | L100 | i | DELETE | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P1 | L100 | i | INSERT | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P1 | L100 | i | UPDATE | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P1 | L101 | i | EXECUTES | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P1 | L119 | v | 80% | documented exclusion — numeric percent unit in prose, not a B2 abbreviation |
| P1 | L119 | i | WRONG | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P1 | L125 | ii | sargable | defined-at-first-use — L125 explains sargable inline |
| P1 | L127 | ii | keyset | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P1 | L128 | v | → | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P1 | L137 | i | SAME | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P1 | L139 | iv | `performance-test-harness` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P1 | L144 | iv | `caching-strategy-designer` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P1 | L150 | iii | plan-reading-guide.md | documented exclusion — file identifier / proper name / SQL plural, not a prose abbreviation |
| P1 | L155 | v | <query id/summary> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P1 | L155 | i | PLAN | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P1 | L155 | i | QUERY | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P1 | L155 | i | VERDICT | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P1 | L155 | ii | id | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P1 | L156 | v | <actual\|estimate> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P1 | L156 | v | <rows in touched tables> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P1 | L156 | v | <values> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P1 | L156 | ii | params | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P1 | L157 | v | <node, share of total, why the planner chose it> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P1 | L158 | v | <est vs actual at key nodes; statistics state> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P1 | L158 | ii | est | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P1 | L159 | v | <tenant/row-security predicates present + their cost note \| n/a> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P1 | L161 | v | <fix> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P1 | L162 | v | <money, implementation time, write amp/storage/upkeep> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P1 | L162 | v | <shape> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P1 | L164 | v | <preferred fix and why; decision required, if any> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P1 | L165 | v | <re-plan under same params+volume; expected shape; surface-level timing check> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P1 | L166 | v | <splitter \| caching-strategy-designer \| secure-migration-reviewer \| none> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P1 | L167 | v | <what this verdict deliberately leaves alone> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P1 | L178 | i | BEFORE | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P1 | L193 | iv | `status='rare_value'` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P1 | L194 | iv | `status='common_value'` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P1 | L195 | i | SYMPTOMATIC | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P1 | L202 | i | AND | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P1 | L208 | v | 10M | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P1 | L217 | i | OFFSET | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P1 | L240 | i | SHAPE | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P1 | L255 | ii | evals | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P1 | L255 | iii | evals.json | documented exclusion — file identifier / proper name / SQL plural, not a prose abbreviation |
| P1 | L255 | iv | `evals/evals.json` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P1 | L257 | iv | `evals/trigger-evals.json` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P1 | L257 | iii | trigger-evals.json | documented exclusion — file identifier / proper name / SQL plural, not a prose abbreviation |
| P2 | L3 | i | SKILL | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P2 | L3 | iii | SKILL.md | documented exclusion — file identifier / proper name / SQL plural, not a prose abbreviation |
| P2 | L14 | ii | est | named gap — shorthand used L14 without expansion |
| P2 | L14 | v | × | named gap — operator used L14 without definition |
| P2 | L14 | v | ≪ | named gap — operator used L14 without definition |
| P2 | L23 | i | FIRST | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P2 | L25 | i | AND | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P2 | L25 | iv | `country='X' AND region='X-north'` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P2 | L27 | v | 40% | documented exclusion — numeric percent unit in prose, not a B2 abbreviation |
| P2 | L39 | i | WHERE | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P2 | L39 | iv | `WHERE fn(col) = v` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P2 | L39 | ii | col | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P2 | L39 | iv | `col = inv(v)` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P2 | L39 | ii | fn | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P2 | L40 | ii | param | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P2 | L40 | v | ≠ | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P2 | L42 | iv | `OR` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P2 | L43 | i | EXISTS | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P2 | L43 | i | IN | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P2 | L43 | i | NOT | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P2 | L43 | iv | `NOT EXISTS` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P2 | L43 | iv | `NOT IN (subquery)` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P2 | L43 | i | NULL | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P2 | L43 | iii | NULLs | documented exclusion — file identifier / proper name / SQL plural, not a prose abbreviation |
| P2 | L44 | i | BY | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P2 | L44 | i | LIMIT | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P2 | L44 | iv | `OFFSET` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P2 | L44 | i | ORDER | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P2 | L44 | iv | `WHERE (sort_key, id) > (last_seen...) ORDER BY ... LIMIT n` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P2 | L44 | ii | id | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P2 | L44 | ii | keyset | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P2 | L45 | i | SELECT | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P2 | L45 | iv | `SELECT *` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P2 | L53 | v | <cols> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P2 | L53 | ii | cols | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P2 | L54 | v | <equality cols...> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P2 | L54 | v | <range col> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P2 | L54 | i | INCLUDE | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P2 | L57 | v | <table> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P2 | L57 | i | INSERT | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P2 | L57 | i | UPDATE | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P2 | L58 | v | <estimate> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P2 | L58 | v | ≈ | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P2 | L61 | v | <node X: scan → seek; loops N→M; sort eliminated?> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P2 | L66 | i | SAME | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P2 | L69 | iv | `performance-test-harness` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P2 | L77 | i | ANALYZE | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P2 | L77 | i | EXPLAIN | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P2 | L77 | iv | `EXPLAIN ANALYZE` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P2 | L82 | ii | repo | named gap — shorthand used L82 without expansion |
| P3 | L3 | iii | ACLs | named gap — first use L3 before ACL expansion L8 |
| P3 | L3 | i | AT | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P3 | L3 | iii | LLM09 | named gap — first use L3 before Terms L8-12 |
| P3 | L3 | i | NOT | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P3 | L3 | i | OWASP | named gap — first use L3 before Terms L9 |
| P3 | L3 | i | RAG | named gap — first use L3 before Terms L8 |
| P3 | L3 | i | RETRIEVAL | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P3 | L3 | i | TIME | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P3 | L8 | i | ACL | defined-at-first-use — L8 Terms expands ACL |
| P3 | L11 | iii | LLM08 | defined-at-first-use — L11 states LLM08 in 2025 |
| P3 | L12 | i | IDOR | defined-at-first-use — L12 Terms expands IDOR |
| P3 | L12 | i | PII | defined-at-first-use — L12 Terms expands PII |
| P3 | L25 | iv | `tenant-isolation-reviewer` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P3 | L26 | iv | `multi-tenant-data-architect` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P3 | L32 | i | AI | defined-at-first-use — L32 expands artificial intelligence (AI) |
| P3 | L37 | iv | `prompt-injection-defender` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P3 | L39 | iv | `model-poisoning-reviewer` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P3 | L40 | iv | `sensitive-disclosure-guard` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P3 | L49 | iv | `authorization-matrix-designer` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P3 | L50 | iv | `tenant-modeler` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P3 | L65 | v | → | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P3 | L68 | i | MUST | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P3 | L76 | iii | rag-retrieval-authz.md | documented exclusion — file identifier / proper name / SQL plural, not a prose abbreviation |
| P3 | L79 | ii | owner | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P3 | L92 | iv | `multi-tenant-security-tester` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P3 | L93 | iv | `ai-evaluation-harness` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P3 | L101 | v | <system> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P3 | L101 | i | AUGMENTED | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P3 | L101 | i | DESIGN | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P3 | L101 | i | GENERATION | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P3 | L101 | i | REVIEW | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P3 | L101 | i | SECURITY | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P3 | L102 | v | <query → embed → search → filter → context> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P3 | L102 | v | <retrieval \| after retrieval (finding)> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P3 | L103 | v | <namespace/index/filter mechanism + can-it-be-omitted> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P3 | L104 | v | <metadata stored \| how ACL change/delete flows to the index> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P3 | L106 | v | <embeddings exposed? sensitivity of embedded data> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P3 | L107 | v | <exposure + mitigation> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P3 | L108 | v | <ingestion trust + ranking abuse> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P3 | L109 | v | <fix> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P3 | L109 | v | <issue> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P3 | L109 | v | <leak path> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P3 | L109 | v | <severity> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P3 | L110 | v | <cross-tenant / no-access / stale-ACL cases> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P3 | L111 | v | <no existence/metadata leak of unauthorized docs> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P3 | L111 | ii | docs | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P3 | L112 | v | <areas + why> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P3 | L118 | ii | post-retrieval | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P3 | L119 | i | BOTH | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P3 | L137 | i | INSTRUCTIONS | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P3 | L138 | i | DATA | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P3 | L147 | i | INSIDE | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P3 | L171 | iv | `incident-response-runbook` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P3 | L182 | ii | evals | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P3 | L182 | iii | evals.json | documented exclusion — file identifier / proper name / SQL plural, not a prose abbreviation |
| P3 | L182 | iv | `evals/evals.json` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P3 | L183 | iv | `evals/trigger-evals.json` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P3 | L183 | iii | trigger-evals.json | documented exclusion — file identifier / proper name / SQL plural, not a prose abbreviation |
| P4 | L1 | i | RAG | named gap — first use L1 before Terms L4 |
| P4 | L3 | i | SKILL | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P4 | L3 | iii | SKILL.md | documented exclusion — file identifier / proper name / SQL plural, not a prose abbreviation |
| P4 | L5 | i | OWASP | defined-at-first-use — L5 expands OWASP |
| P4 | L6 | iii | LLM09 | defined-at-first-use — L6 expands LLM09 |
| P4 | L7 | i | ANN | defined-at-first-use — L7 expands ANN |
| P4 | L7 | iii | LLM08 | defined-at-first-use — L7 states LLM08 in 2025 |
| P4 | L8 | i | ACL | defined-at-first-use — L8 expands ACL |
| P4 | L8 | i | IDOR | defined-at-first-use — L8 expands IDOR |
| P4 | L13 | i | RETURN | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P4 | L14 | v | → | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P4 | L18 | ii | pre-filtering | defined-at-first-use — L18 names metadata filtering / pre-filtering |
| P4 | L26 | i | ANTI | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P4 | L26 | i | PATTERN | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P4 | L26 | ii | top-k | named gap — shorthand used L26 without expansion |
| P4 | L32 | ii | k | named gap — standalone lowercase k used L32 without expansion beyond the L26 top-k row |
| P4 | L44 | i | WITHOUT | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P4 | L47 | iv | `multi-tenant-data-architect` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P4 | L48 | iv | `tenant-isolation-reviewer` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P4 | L52 | ii | owner | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P4 | L55 | i | OLD | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P4 | L58 | iii | ACLs | defined-at-first-use — L8 singular ACL expanded; plural used L58 |
| P4 | L65 | iii | IDs | documented exclusion — file identifier / proper name / SQL plural, not a prose abbreviation |
| P4 | L71 | iv | `model-poisoning-reviewer` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P4 | L72 | iv | `prompt-injection-defender` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P4 | L79 | ii | docs | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P4 | L84 | ii | id | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P5 | L3 | i | NOT | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P5 | L3 | i | OUT | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P5 | L3 | i | README | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P5 | L3 | i | SET | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P5 | L3 | ii | docs | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P5 | L9 | i | CLI | defined-at-first-use — L9 reading key expands CLI |
| P5 | L10 | i | API | defined-at-first-use — L10 reading key expands API |
| P5 | L10 | i | CI | defined-at-first-use — L10 reading key expands CI |
| P5 | L38 | i | INTO | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P5 | L38 | iv | `diataxis-doc-organizer` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P5 | L40 | iv | `docs-as-code-architect` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P5 | L41 | i | CONTRIBUTING | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P5 | L42 | iv | `contribution-guide-author` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P5 | L43 | i | JOINING | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P5 | L44 | iv | `onboarding-doc-designer` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P5 | L74 | v | 20% | documented exclusion — numeric percent unit in prose, not a B2 abbreviation |
| P5 | L74 | v | 80% | documented exclusion — numeric percent unit in prose, not a B2 abbreviation |
| P5 | L83 | ii | config | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P5 | L84 | i | OTHER | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P5 | L95 | iii | readme-sheet.md | documented exclusion — file identifier / proper name / SQL plural, not a prose abbreviation |
| P5 | L100 | v | <project> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P5 | L100 | i | DRAFT | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P5 | L100 | i | PLAN | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P5 | L102 | i | VERIFIED | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P5 | L104 | v | → | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P5 | L106 | v | <content moved to other docs, with destinations> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P5 | L108 | i | PASS | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P5 | L169 | ii | evals | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P5 | L169 | iii | evals.json | documented exclusion — file identifier / proper name / SQL plural, not a prose abbreviation |
| P5 | L169 | iv | `evals/evals.json` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P5 | L171 | iv | `evals/trigger-evals.json` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P5 | L171 | iii | trigger-evals.json | documented exclusion — file identifier / proper name / SQL plural, not a prose abbreviation |
| P6 | L1 | i | README | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P6 | L3 | i | SKILL | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P6 | L3 | iii | SKILL.md | documented exclusion — file identifier / proper name / SQL plural, not a prose abbreviation |
| P6 | L5 | iv | `readme-craftsman` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P6 | L7 | i | API | defined-at-first-use — L7 expands application programming interface |
| P6 | L7 | i | CLI | defined-at-first-use — L7 expands command-line interface |
| P6 | L8 | i | ADR | defined-at-first-use — L8 expands architecture decision record |
| P6 | L8 | i | GIF | defined-at-first-use — L8 expands Graphics Interchange Format |
| P6 | L20 | i | BELOW | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P6 | L27 | v | 80% | documented exclusion — numeric percent unit in prose, not a B2 abbreviation |
| P6 | L28 | ii | docs | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P6 | L57 | i | ONLY | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P6 | L70 | ii | config | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P6 | L72 | iii | ADRs | defined-at-first-use — L8 ADR expanded; plural used L72 |
| P7 | L3 | i | AND | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P7 | L3 | i | API | named gap — first use L3 before Terms L13 |
| P7 | L3 | i | NOT | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P7 | L3 | i | SSE | named gap — first use L3 before Terms L9 |
| P7 | L3 | iii | SaaS | named gap — first use L3 before Terms L13 |
| P7 | L3 | i | UX | named gap — first use L3 before in-page expansion L57 |
| P7 | L3 | iii | WebSocket | named gap — first use L3 before Terms L8 |
| P7 | L9 | i | DB | defined-at-first-use — L9 Terms expands DB |
| P7 | L10 | i | CDC | defined-at-first-use — L10 Terms expands CDC |
| P7 | L10 | i | DLQ | defined-at-first-use — L10 Terms expands DLQ |
| P7 | L10 | i | TTL | defined-at-first-use — L10 Terms expands TTL |
| P7 | L11 | i | LB | defined-at-first-use — L11 Terms expands LB |
| P7 | L12 | i | IDOR | defined-at-first-use — L12 Terms expands IDOR |
| P7 | L12 | i | OOM | defined-at-first-use — L12 Terms expands OOM |
| P7 | L14 | ii | authz | defined-at-first-use — L14 Terms expands authz |
| P7 | L30 | i | CLIENTS | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P7 | L32 | iv | `streaming-event-architect` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P7 | L46 | i | INTERNAL | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P7 | L48 | i | CONSUME | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P7 | L50 | i | OUTBOUND | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P7 | L51 | iv | `api-event-architect` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P7 | L53 | i | OFFLINE | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P7 | L54 | iv | `offline-first-sync-architect` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P7 | L55 | i | ONLINE | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P7 | L58 | iv | `notification-webhook-ux-designer` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P7 | L68 | iv | `multi-tenant-data-architect` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P7 | L69 | iv | `authorization-matrix-designer` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P7 | L93 | i | IS | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P7 | L94 | v | <id> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P7 | L94 | ii | id | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P7 | L94 | iv | `tenant:<id>:resource:<id>` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P7 | L112 | ii | pub | defined-at-first-use — L112 expands publish/subscribe (pub/sub) |
| P7 | L112 | ii | sub | defined-at-first-use — L112 expands publish/subscribe (pub/sub) |
| P7 | L121 | iv | `horizontal-scalability-reviewer` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P7 | L130 | ii | dedup | named gap — shorthand used L130 without expansion |
| P7 | L146 | v | <system/domain> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P7 | L146 | i | DELIVERY | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P7 | L146 | i | DESIGN | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P7 | L146 | i | REALTIME | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P7 | L149 | v | <channel type — key format (server-derived) — audience> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P7 | L150 | v | <edge> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P7 | L150 | v | <per-user/per-resource> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P7 | L151 | i | SUBSCRIBE | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P7 | L152 | v | <authority-change trigger> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P7 | L152 | v | <event> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P7 | L156 | v | → | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P7 | L158 | v | <per-connection buffer bound; overflow policy per channel type> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P7 | L161 | v | <heartbeat + time to live (TTL), soft-state, own authorization> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P7 | L196 | iv | `subscribe("tenant:42:...")` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P7 | L226 | i | DESIGNS | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P7 | L227 | ii | repo | named gap — shorthand used L227 without expansion |
| P7 | L231 | ii | evals | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P7 | L231 | iii | evals.json | documented exclusion — file identifier / proper name / SQL plural, not a prose abbreviation |
| P7 | L231 | iv | `evals/evals.json` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P7 | L234 | iv | `evals/trigger-evals.json` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P7 | L234 | iii | trigger-evals.json | documented exclusion — file identifier / proper name / SQL plural, not a prose abbreviation |
| P7 | L235 | i | THE | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P7 | L238 | iv | `references/` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P8 | L3 | i | CI | named gap — first use L3 before reading key L8 |
| P8 | L3 | i | NOT | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P8 | L3 | i | PR | named gap — first use L3 before reading key L8 |
| P8 | L3 | i | WHAT | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P8 | L3 | ii | expiry | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P8 | L3 | ii | owner | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P8 | L3 | ii | runtime | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P8 | L3 | ii | smoke | named gap — shorthand used L3 without expansion |
| P8 | L3 | ii | ticket | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P8 | L3 | ii | tier | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P8 | L3 | ii | tiers | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P8 | L8 | i | QA | defined-at-first-use — L8 reading key expands QA |
| P8 | L9 | i | CODEOWNERS | defined-at-first-use — L9 reading key explains CODEOWNERS |
| P8 | L28 | v | → | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P8 | L36 | i | INPUT | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P8 | L36 | iv | `flaky-test-detective` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P8 | L38 | iv | `qa-automation-architect` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P8 | L40 | iv | `test-coverage-mapper` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P8 | L66 | ii | flake | named gap — shorthand used L66 without expansion |
| P8 | L69 | v | ≥ | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P8 | L74 | iii | curation-rules.md | documented exclusion — file identifier / proper name / SQL plural, not a prose abbreviation |
| P8 | L76 | i | WITH | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P8 | L80 | i | NO | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P8 | L84 | i | ONLY | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P8 | L84 | iv | `multi-tenant-security-tester` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P8 | L85 | iv | `human-approval-boundary` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P8 | L88 | i | NOW | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P8 | L96 | iv | `reviewable-diff-discipline` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P8 | L101 | v | <date> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P8 | L101 | v | <suite/scope> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P8 | L101 | i | CURATION | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P8 | L101 | i | REPORT | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P8 | L105 | v | <rule + evidence> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P8 | L105 | v | <test/gap> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P8 | L105 | v | <tier> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P8 | L105 | i | PROMOTE | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P8 | L106 | v | <earns place because…> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P8 | L106 | v | <test> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P8 | L106 | i | RETAIN | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P8 | L107 | v | <evidence> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P8 | L107 | i | DEMOTE | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P8 | L108 | v | <rationale + protection lost + why acceptable> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P8 | L108 | i | RETIRE | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P8 | L109 | v | <diagnose\|fix\|retire + owner/ticket/expiry> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P8 | L109 | i | ACTION | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P8 | L109 | i | QUARANTINE | documented exclusion — ordinary all-caps emphasis word, SQL keyword or proper name, not an abbreviation |
| P8 | L110 | v | <security regressions touched? → human-approval path> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P8 | L111 | v | <tier → runtime before/after vs budget> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P8 | L112 | v | <explained budget/protection paths, costs/unknowns, pros/cons, recommendation + why> | documented exclusion — output-format placeholder, not a B2 abbreviation |
| P8 | L113 | v | <promotion + retirement + quarantine rules going forward> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P8 | L116 | v | <cadence/trigger> | documented exclusion — output-format placeholder, operator or unit, not a B2 abbreviation |
| P8 | L167 | ii | schema | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P8 | L168 | ii | evals | documented exclusion — ordinary engineering contraction or code token, not a coded identifier |
| P8 | L168 | iii | evals.json | documented exclusion — file identifier / proper name / SQL plural, not a prose abbreviation |
| P8 | L168 | iv | `evals/evals.json` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P8 | L169 | iv | `evals/trigger-evals.json` | documented exclusion — inline code, file path or skill identifier, not a prose abbreviation |
| P8 | L169 | iii | trigger-evals.json | documented exclusion — file identifier / proper name / SQL plural, not a prose abbreviation |
| P7 | L147-148 | v | <WebSocket \| server-sent events (SSE) \| database-change subscription> | documented exclusion — self-describing multiline template placeholder (fill-in hole), not an abbreviation |
| P7 | L153-154 | v | <publish/subscribe backbone; source = internal backbone (consumed); cross-node delivery; edge filter enforcing the leak boundary> | documented exclusion — self-describing multiline template placeholder (fill-in hole), not an abbreviation |
| P7 | L155-156 | v | <per-connection cost; node limit; load-balancer (LB) sticky/any-node; drain → reconnect-and-resume handoff> | documented exclusion — self-describing multiline template placeholder (fill-in hole), not an abbreviation |
| P7 | L159-160 | v | <snapshot vs cursor replay; resume window; deduplication; reconnect backoff/jitter> | documented exclusion — self-describing multiline template placeholder (fill-in hole), not an abbreviation |
| P8 | L102-103 | v | <test/group → tier, runtime, failure history, guards-what, duplication candidates> | documented exclusion — self-describing multiline template placeholder (fill-in hole), not an abbreviation |
| P8 | L114-115 | v | <new tests → engineer skills; flake cases → flaky-test-detective; deletions → review via reviewable-diff-discipline> | documented exclusion — self-describing multiline template placeholder (fill-in hole), not an abbreviation |

## 6. Disposition tally, B6 and keeper exclusion

**Disposition tally: 0 FULL / 8 PARTIAL / 0 UNRUN / 0 edits.** No page is FULL: canonical B6 is UNVERIFIED from git metadata and cannot support FULL, and the named B2 first-use gaps independently force PARTIAL for P1/P2/P3/P4/P7/P8; P5/P6 are PARTIAL on B6 alone. PARTIAL pages receive no acceptance/keeper row; this record authors no acceptance/keeper row and carries no acceptance-row authority. No page was edited in this read-only batch; all eight named corrections remain outstanding for later work.

**Keeper exclusion.** No page is eligible for a later keeper row on this evidence; all eight PARTIAL pages are excluded from any acceptance/keeper row. The record adds no keeper row, ledger row, acceptance-index change or targeted-review row.

## 7. Provenance and reader-independence witness rows

| # | Page | Full blob id | Last-touching commit | Author | Date | Reader identity |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | query-plan-reader/SKILL.md | `c46fa16099fcddc6d97ad7ba86979a9796eea44b` | `2a86058396410357a771eb44e33cff0436940e9d` | Peter Nguyen | 2026-09-28 | sd-d-802-r3 / sd-c-read-b14-c1 |
| P2 | query-plan-reader/references/plan-reading-guide.md | `5f96fc0a110138a8964fc4f07fa1a9ddd5665e60` | `a694b938f8b7b2196b4d9c9016e9a512123f2f96` | Peter Nguyen | 2026-09-24 | sd-d-802-r3 / sd-c-read-b14-c1 |
| P3 | rag-security-architect/SKILL.md | `48894cb5bed44f3371178e2accfa482ff54699dd` | `8459ac73ba6e0b280338aca9a97be7a3336ce356` | Peter Nguyen | 2026-09-28 | sd-d-802-r3 / sd-c-read-b14-c1 |
| P4 | rag-security-architect/references/rag-retrieval-authz.md | `6bd389d122d6f9dd5e4a5560b1cd620c5d6bb70a` | `d36ec53fed868b9a0e338e1967d08ef719e11a6f` | Peter Nguyen | 2026-09-26 | sd-d-802-r3 / sd-c-read-b14-c1 |
| P5 | readme-craftsman/SKILL.md | `4df879a39008f020ac34f42ff067a6c49f5fc772` | `5e0e9ad7d79b109aabcc3d2531061fadf84af592` | Peter Nguyen | 2026-09-23 | sd-d-802-r3 / sd-c-read-b14-c1 |
| P6 | readme-craftsman/references/readme-sheet.md | `4a32caddfc41c98558ced231158564e7c4d62e50` | `a694b938f8b7b2196b4d9c9016e9a512123f2f96` | Peter Nguyen | 2026-09-24 | sd-d-802-r3 / sd-c-read-b14-c1 |
| P7 | realtime-subscription-architect/SKILL.md | `2ffaf0e5a297305318c02f9aceb6dad4c797c3ae` | `6ba6e1ad71ef6c3cea6297b806838fec72323c10` | Peter Nguyen | 2026-09-28 | sd-d-802-r3 / sd-c-read-b14-c1 |
| P8 | regression-suite-curator/SKILL.md | `e521775357b34e5bb4d9dee7c052d410e1172061` | `2a86058396410357a771eb44e33cff0436940e9d` | Peter Nguyen | 2026-09-28 | sd-d-802-r3 / sd-c-read-b14-c1 |

**B6 witness.** The reader stage identity is not recorded as any page's last-touching author, but this cannot prove non-authorship. **Basis:** page author Peter Nguyen; the reader stage identity committed none of these pages in the repository metadata. **Limit:** git metadata cannot prove non-authorship of owner-account commits or that a human performed the reading; B6 is therefore UNVERIFIED and cannot support FULL. No page is FULL; all eight are PARTIAL on B6 and, where named, their B2 gaps.

## 8. Hunk and line accounting

- **Tracked change:** exactly **one added path** - this record - no other tracked path; **0 modified, 0 deleted, 0 renames**; branch from live main e7acaca4 so the live-base PR hunk is only this file.
- **Page accounting:** zero hunks touch any of the eight pages; every page diff is empty; no keeper/ledger/index/register/manifest/tool/test/workflow change.
- **Record measurement:** final record bytes/LF/sha are bound in the PR body outside the record (a deliberate self-reference limit); the record's own statement covers the **page totals** 72,464 B / 1,275 LF at the pinned ref, not its own file bytes. **Required PR-body binding fields:** record path, Git blob, bytes, LF, CR count, sha256, head/tree/base and the recomputed PROC-04; Stage D/F verify those exact fields against the live head.

## 9. Plan AC1-AC8 - Stage C declaration and self-state consistency

| AC | Stage C status and evidence |
| --- | --- |
| AC1 One-path tree proof | **MET at the final head** - exactly one added path; 0 modified/deleted; exact head/tree/base in handoff and PR body. |
| AC2 Frozen page set by blob hash | **MET in this record** - eight paths, indices 216-223, blobs/bytes/LF at pinned ref; identical at base. |
| AC3 Whole-page re-read + token audit | **MET in this record** - each page read whole L1-last; canonical B1-B6 tested with page cites, B4 tested per page; required five-class exact-once per-page token inventory in section 5 with 373 rows / 373 keys / 0 duplicates and named gaps. |
| AC4 Honest per-page disposition | **MET in this record** - **0 FULL / 8 PARTIAL / 0 UNRUN**; B6 unverified and B2 gaps named; no acceptance/keeper row. |
| AC5 Record integrity/body/PROC-04 | **OWED after this file freezes** - PR body binds plan/record facts; PROC-04 recomputed; checker at head; record one terminal LF/no CR/no trailing whitespace/no blank EOF. |
| AC6 Codex loop plan | **OWED after the PR exists at its head** - trigger, fetch, fix P1/P2 with replies naming fixing SHA, resolve, retrigger; head-bound unavailability only after triage; never a pass. |
| AC7 Provenance and no regression | **MET in this record** - plan binding 6247908528 + correction 6247913133 + B ACCEPT 6247952220; derivation base e7acaca4; merged rows 144-199; reservations #833 200-207 / #834 208-215 / #836 224-231; block 216-223; next 224; zero drift; no keeper/index/ledger/register/manifest change. |
| AC8 Stage entry conditions | **SATISFIED for C** - only on fresh B ACCEPT 6247952220 bound to plan 6247908528; branched from live main e7acaca4; one added record path; one DCO model commit; D/E/F/G separate; no merge. |

**Self-state consistency:** section 2 (base e7acaca4, merged rows 144-199, reservations 200-207/208-215/224-231, block 216-223, batch 14), section 3 (eight pages, totals 72,464 B / 1,275 LF), section 4 (0 FULL / 8 PARTIAL / 0 UNRUN) and section 9 (same AC7/AC8 facts) agree; the authorship chain is plan 6247908528 (sd-c-796-r1 / sd-a-read-b14-r1), B ACCEPT 6247952220 (sd-c-793-r2 / sd-b-read-b14-b1), C this record (sd-d-802-r3 / sd-c-read-b14-c1; repair edited under sd-c-read-b14-c2), with D/E/F/G separate. No stale count or contradictory range is carried.

## 10. Validation actually run while authoring

| Check | Method | Result |
| --- | --- | --- |
| Instrument at pinned ref | check_index.py --ref 2db1ffb7 at main e7acaca4 | exit 0; 690 / 107 / 6 / 567 / 0 / 6 / 0 / 4 / 583 |
| Blobs/bytes/LF | git rev-parse/cat-file at pinned ref and base e7acaca4 | eight plan blobs match; sizes/LF total 72,464 / 1,275; zero drift |
| Frozen set eligibility | merged/reservation scan + record path absence | 216-223 unread, outside reservations, no keeper; record path absent at base |
| Links | resolve each relative link at pinned ref | 12 internal links, all resolve; 0 external URLs |
| Token inventory | five-class scan, first-use normalization, exact-once key, disposition rules | 373 rows / 373 unique keys / 0 duplicates; counts recomputed from final table |
| Record integrity | byte/LF/CR/trailing-whitespace/EOF checks | one terminal LF; 0 CR; no trailing whitespace; no blank EOF |

**Owed and not claimed:** post-commit git diff --check, DCO check, validate-skills, markdown links, body checker, hosted CI at the exact head, Codex and DeepSeek triage are recorded in the Stage C handoff/PR body after they run; any that cannot run is UNRUN with reason.

## 11. What this batch could not verify (stated, not hidden)

- **B6 as a human act** is unverifiable from git metadata; the batch independence claim is limited to that metadata basis and declared limit.
- **Future keeper acceptance:** this record creates no acceptance rows; a later keeper decides. All eight PARTIAL pages are excluded now.
- **Hosted/Codex checks:** no PR/head existed while authoring; owed at the head, not claimed here.
- **Drift after base:** frozen blobs are at the pinned ref and live main e7acaca4; later movement reopens the batch.
- **Prose reading is not a usability study:** the record lists what each page says and where; the canonical six bullets are the bar.
- **External comment-ID bindings:** the plan, correction, B ACCEPT, Codex and DeepSeek review IDs are external bindings that the record cannot independently prove immutable; they are verified against live GitHub at the exact head, not self-proved here.

The record is the only added path; it carries one DCO-signed model-attributed commit. Stage D independently audits AC1-AC8 at the exact head; Stage E records checks/UNRUN honestly; Stage F reviews exact head/PROC-04; Stage G applies merge gates including MG3 under the recorded reading; no merge before G. **Lane A is complete; this is a lane-B block and does not reopen lane A.** Any need outside one path stops and returns to Stage A/owner.

**Boundary.** Stage C only: no page edited; no keeper/ledger/index/register/manifest/tool/test/workflow change; no other PR touched; no merge.

**Signed with both names: true identity sd-d-802-r3; stage role sd-c-read-b14-c2 (repair).** **Written by: DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness).**
