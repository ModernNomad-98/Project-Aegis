# Readability Phase 4 re-read lane A — Stage C batch record, batch 9, 2026-10-18

**Batch record for the Phase 4 documentation-readability re-read, lane A batch 9 — eight whole-page re-reads, zero page edits.** This record is the Stage C evidence artifact for the batch-9 item; it is the only tracked change in its pull request.

**Plan of record.** Lean plan revision 2, PR #809 issue comment **6243633250** (created = updated 2026-10-18T00:17:38Z; immutable; 13,508 bytes; author sd-d-793-r2 / stage role sd-a-read-b9-r2), with Stage B re-audit **ACCEPT 6243652578** (2026-10-18T00:19:55Z; F1/F2/F3 fixed; eight pages re-verified). The plan is operative only on that fresh B ACCEPT bound to that comment; it is not a committed plan file and no plan file exists in this change.

**Implementation base.** `main` = **147479583fc498c50028f1b7dbf8311c8708544e** (live `origin/main` at branch creation). **Pinned measurement ref** = **2db1ffb7985ddc1c087c455740fd59e962967461** (the merged acceptance index's `built_at_ref`), at which the eight frozen pages are bound by Git blob id below.

**Agent, model and stage.** Written by **DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)**; agent identity **sd-c-793-r2**, stage role **sd-c-read-b9-c1**. Stage C only: I read each frozen page whole at the pinned blob, authored this record, and did not edit any page, keep any ledger row, rebuild any index, open any other pull request, act on any other Codex thread, or merge. The record is signed with both names at its footer.

## 1. Lane derivation at this implementation base

**Instrument run (command and result).** In a fresh clone of `main` 14747958, run from the repository root:

```text
python -P -B tools/readability_acceptance/check_index.py --ref 2db1ffb7985ddc1c087c455740fd59e962967461 --json
```

The run exits 0 and returns exactly: **reader_pages_in_tree 690; accepted_on_recorded_review 107; provably_pending 6; no_recorded_acceptance 567; recorded_acceptance_within_10_lines 0; cannot_decide 6; withdrawn_pending_rereview 0; partial_disposition_pending 4; official_pending_count 583** at the pinned ref. The lane-arithmetic pending set is the two pending buckets: **567 + 6 = 573 sorted paths**.

**Lane A bounds (re-derived, not copied).** Sorting those 573 paths by repository path and taking the first quarter gives lane A = indices **0–143**, first path `.claude/skills/adr-writer/assets/adr-template.md` and last path `.claude/skills/inter-agent-comms-reviewer/SKILL.md`.

**Read frontier and this block.** The merged lane A batch records on `main` 14747958 (batch-1, batch-2, batch-2 APR-117 rerecord, batch-3, batch-4 2026-10-15, batch-4 2026-10-17, batch-5) name their P1–P8 read pages. Mapping those pages into the current 573-path lane A sorted range yields **24 unique in-range read paths occupying indices 0–23** — the contiguous read frontier ends at **23** — and the assignment's following blocks are batch 6 = **24–31**, batch 7 = **32–39**, batch 8 = **40–47**, this item batch 9 = **48–55**. **Re-derived block starts:** index 24 `.claude/skills/ai-closeout-reporter/SKILL.md`; 32 `.claude/skills/ai-human-in-the-loop-designer/SKILL.md`; 40 `.claude/skills/ai-sdlc-operating-model/SKILL.md`; **48 `.claude/skills/api-doc-generator-designer/SKILL.md`** (first page of this batch); 56 `.claude/skills/architecture-designer/SKILL.md` (first path after this batch).

**Eligibility of the eight frozen pages (measured in this clone).** Each page is in the 573-path pending set at the pinned ref (so no keeper row exists for it), is in lane A's 0–143 range, is named as a read page in no merged lane A batch record, and has **empty `git diff --numstat 2db1ffb7..14747958 -- <page>` drift** (same blob at the pinned ref and at the implementation base). **No page outside the frozen eight is read or claimed in this record.**

## 2. Roster, reader independence and role separation

- **Reader (this batch):** one reader — **sd-c-793-r2 / stage role sd-c-read-b9-c1**, DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness) — read all eight pages whole, line by line, as prose at the pinned blob, in this session. No display elision was used: each page was read from its first line to its last, and every line number cited below is from the pinned blob.
- **Page authorship (from git metadata).** The last-touching commit and author of each frozen page are recorded in section 7; no page was written by this reader (page authors are Peter Nguyen and the ModernNomad-98 account; the reader's stage role is a distinct agent identity). The record claims no more than the metadata can carry.
- **Role separation.** Stage C is the evidence author, not the page author, not the keeper and not the merger. Keeper recording is a separate later act under AEGIS-APR-101/APR-117 by an eligible keeper; this record authors **no** keeper row, no ledger edit, no index rebuild, no acceptance-row insertion and no approval change. Stage D audits this record at the exact head; Stage E runs the repository checks; Stage F reviews; Stage G owns the merge.
- **Concurrency.** One reader is used for this eight-page batch; the record makes no multi-reader claim for batch 9.

## 3. The frozen page set — eight pages, measured at the pinned ref

All eight pages were read whole at the pinned ref blob; the bytes/LF values below were measured by command (`git cat-file -s` and `git show | wc -l` equivalents) and sum to **64,259 bytes / 1,155 LF**, matching the plan's frozen totals. **No page was edited; every page's diff count is 0.**

| # | Lane A index | Page (path) | Git blob at `2db1ffb7` | Bytes / LF | Verdict | Gaps named (page line) | Edits |
| --- | ---: | --- | --- | ---: | --- | --- | ---: |
| P1 | 48 | `.claude/skills/api-doc-generator-designer/SKILL.md` | `ce0c26dbf2bc1fdd3dd6b610f5e8dd9b9f4ba2ee` | 11,692 / 206 | **FULL** | none | 0 |
| P2 | 49 | `.claude/skills/api-doc-generator-designer/references/api-doc-sheet.md` | `aaa9134f3106736450e816af57f6e9c8c709ea05` | 2,624 / 68 | **PARTIAL** | L6: `REST` unexpanded | 0 |
| P3 | 50 | `.claude/skills/api-event-architect/SKILL.md` | `4bc92cf83f3737b7027256076331a2aa3952968d` | 16,163 / 270 | **FULL** | none | 0 |
| P4 | 51 | `.claude/skills/api-event-architect/references/api-event-contract-conventions.md` | `c9dec9807a6ec34839ddf3f9b624e000d9cb70c5` | 4,188 / 83 | **PARTIAL** | L8: `HTTP`; L42: `HTTPS` unexpanded | 0 |
| P5 | 52 | `.claude/skills/appsec-implementer/SKILL.md` | `726ee517b6fd4dac246d23affc914f28f65f3183` | 10,511 / 183 | **FULL** | none | 0 |
| P6 | 53 | `.claude/skills/appsec-implementer/references/control-implementation-patterns.md` | `0602bd7603d2d3e5f6dd1e53146d5cc1e80f0590` | 3,892 / 78 | **PARTIAL** | L18–19: `4xx`; L24–25: `HTML`/`JS`/`CSS`/`URL` unexpanded | 0 |
| P7 | 54 | `.claude/skills/architecture-advisor/SKILL.md` | `c844bb13fec84570cc702271598fb0493bac6d60` | 12,358 / 206 | **FULL** | none | 0 |
| P8 | 55 | `.claude/skills/architecture-advisor/references/architecture-style-sheet.md` | `9ca2aa084c66cce53f492f74f8381e2cb36a45a1` | 2,831 / 61 | **PARTIAL** | L26: `w/o` unexpanded | 0 |

**Totals: 8 pages / 64,259 bytes / 1,155 LF / 4 FULL / 4 PARTIAL / 0 UNRUN / 0 edits.** Full 40-character blob IDs are in the table above; every ID resolves at pinned ref `2db1ffb7` and every page's blob is identical at `main` 14747958 (zero drift).

## 4. Per-page dispositions — what is and is not accepted

The record uses the lane's established vocabulary: **FULL** means all six acceptance bullets of the repository's "Acceptance for each page" hold for the whole page at the bound revision; **PARTIAL** means at least one named defect stands against the page at the bound revision; **UNRUN-with-reason** means the page could not be read or judged and the reason is recorded. No disposition is upgraded: if a defect were recorded for a page anywhere, that page's verdict would be PARTIAL, not FULL.

**Disposition tally: 4 FULL / 4 PARTIAL / 0 UNRUN.** Only the four FULL pages (**P1, P3, P5, P7**) are **eligible to receive a full-page acceptance row from a later keeper**; the four PARTIAL pages (**P2, P4, P6, P8**) receive no acceptance row; this record authors none itself (section 11). No page is claimed accepted-by-this-record: the record is evidence, and the keeper role and the acceptance register remain separate. No page needed an edit and none was made.

**Keeper exclusion (stated so a partial page cannot be laundered).** Only the four FULL pages (P1, P3, P5, P7) are eligible for a later keeper row; the four PARTIAL pages (P2, P4, P6, P8) are excluded from any acceptance/keeper row. The record does not add a keeper row, a ledger row, an acceptance-index change or a targeted-review row; it carries no acceptance-row authority. A later eligible keeper may record these rows under AEGIS-APR-101/APR-117 from this evidence, subject to the keeper protocol.

## 5. Per-page read detail — ranges, six acceptance bullets, purpose restatements, defects

The six bullets are the repository's "Acceptance for each page" in `docs/roadmaps/aegis-documentation-readability-backlog.md`: **B1** open with what the page is for and who should read it; **B2** define an abbreviation or coded identifier at first use; **B3** descriptive headings, short paragraphs, lists or tables for distinct functions, at least one concrete example where the purpose would otherwise stay abstract, and what a command accepts/produces/changes/refuses where safe use depends on it; **B4** state shipped behavior separately from proposed or blocked behavior; **B5** keep navigation links current and check every referenced file or command exists, preserving the technical contract and safety boundaries; **B6** obtain a read-only review from someone who did not write the page, who can explain the component's purpose and normal use from the page alone.

### P1 — `.claude/skills/api-doc-generator-designer/SKILL.md` — read whole, L1–206

**Purpose and normal use (restated from the page alone):** a design skill for generated API reference documentation: it makes the API's machine-readable source of truth explicit, generates the exhaustive reference from that source, keeps authored guides separate, pushes descriptions/examples into the source rather than the output, chooses an API-doc toolchain that fits the docs pipeline, and versions the generated reference with the API; it documents a contract another skill designed, and validates the source against the implementation rather than hand-maintaining reference prose.

**B1 satisfied** — the frontmatter description L2–3 states the job and the trigger; **Purpose** L12–27 opens with the drift problem and what the skill designs; **Use When** L29–48 names the reader's situation and the explicit do-not-use boundaries. **B2 satisfied** — the page expands API, CI, PR, SDK and SoT at L8–10; standard technology names (OpenAPI, GraphQL, TypeDoc, Sphinx) are product/format names; the one framework proper noun, "Diátaxis", at L81 is used as a known documentation-framework name (measured library convention: the term appears on 11 skill files, including its owning `diataxis-doc-organizer` reference; recorded as an observation, not a gap). **B3 satisfied** — descriptive section headings, a numbered 8-step workflow L67–110, a copyable Output Format block L116–133, a validation checklist L135–157, and concrete examples: the renamed-parameter drift narrative L14–17, the generated-vs-authored split example L73–82, and the toolchain examples L93–95. **B4 satisfied** — it designs a documentation generation approach; it makes no shipped-vs-proposed claim about a running system, and its boundaries (does not design the contract, pipeline or corpus organization) are explicit at L26–27 and L180–193. **B5 satisfied** — both internal links (L114, L197–200 to the reference sheet) resolve at the bound revision; all four named skills used in routing exist (`api-event-architect`, `docs-as-code-architect`, `diataxis-doc-organizer`, `error-taxonomy-designer`); the named `evals/evals.json` and `evals/trigger-evals.json` exist; the page names no shell command. **B6 — basis:** git metadata names the page authors (Peter Nguyen / the ModernNomad-98 account) and this reader stage identity committed none of these pages; **limit:** metadata cannot prove non-authorship of commits made under the owner account or that a human executed the read, so this FULL verdict rests on that metadata-level basis plus the declared limit (section 7).
**Verdict: FULL, no edit. No defect recorded.** Observation (not counted): "Diátaxis" is a framework proper noun rather than an internal coded identifier; the library-conventions measurement is in section 6.

### P2 — `.claude/skills/api-doc-generator-designer/references/api-doc-sheet.md` — read whole, L1–68

**Purpose and normal use:** the owning skill's reference sheet — the source-of-truth options and their drift cost, the generated-vs-authored content split, schema-enrichment patterns, example-validation techniques, versioning/deprecation surfacing, and the auth/try-it guidance.

**B1 satisfied** — L1 title and L3 "Detail for the owning [API Doc Generator Designer]" make its place clear; L4–8 expands the base vocabulary. **B2 partial** — API, SoT, RPC, SDK and CI are expanded at L4–8, but **`REST` at L6 is not expanded** (`REST and remote procedure call (RPC)` names RPC only); the table items are product/format names, and "Diátaxis" at L37 is the framework proper noun recorded as an observation in P1. The unexpanded first use is a B2 gap and the page verdict is PARTIAL. **B3 satisfied** — five tables separate source options L12–18, generated-vs-authored split L26–35, enrichment L42–47, validation L51–54 and versioning L58–62; concrete tokens such as `description`, `example`, `examples`, `x-` extensions, `.proto` and `deprecated: true` are shown; the auth/try-it rule L64–68 states the safety boundary. **B4 satisfied** — the page is guidance reference: it labels the options, the not-possible case L20–22 and the ownership of the versioning policy L61–62; it makes no shipped-behavior claim. **B5 satisfied** — the one internal link (L3 to `../SKILL.md`) resolves; the named skills exist; no shell command is given. **B6 — basis:** git metadata names the page authors and this reader stage identity committed none of these pages; **limit:** metadata cannot prove non-authorship of commits made under the owner account or that a human executed the read, so this PARTIAL verdict uses that declared limit (section 7); the PARTIAL comes from the B2 gap above.
**Verdict: PARTIAL, no edit. Named defect: L6 — `REST` used as an abbreviation without a first-use expansion.**

### P3 — `.claude/skills/api-event-architect/SKILL.md` — read whole, L1–270

**Purpose and normal use:** designs the external contracts of a multi-tenant SaaS — API surface and event/webhook feed: tenant-context contract, per-operation request/response schemas, idempotency, tenant/plan rate limits, versioning and deprecation policy, event taxonomy and versioned envelope, tenant-scoped signed webhook delivery, and contract migration/rollback.

**B1 satisfied** — description L2–3, Purpose L16–27, and Use When L29–65 state the job, the reader and the boundaries. **B2 satisfied** — API, SaaS, UX, URL, SSRF and HMAC are expanded at L8–11; 404/403/429 are explained at L11–13; **N** is defined as a chosen retry count at L14; the remaining tokens are ordinary technical terms or named skills. **B3 satisfied** — descriptive headings; an 8-step workflow L84–148; a copyable Output Format L150–172; checklists L174–198; Tenant Isolation Rules L200–211 and Security Rules L213–224; concrete examples include the aggregator-tenant exception L86–92 and the deprecation sequence L109–127. **B4 satisfied** — the page designs contracts and states that a published contract is a promise with a support burden (L26–27); it makes no deployed-integration claim, and its Stop Conditions L248–260 separate design from implementation. **B5 satisfied** — the reference link L129 resolves; every named skill used in its routing exists (fourteen named skill tokens measured); the named evals files exist; no shell command is given. **B6 — basis:** git metadata names the page authors and this reader stage identity committed none of these pages; **limit:** metadata cannot prove non-authorship of commits made under the owner account or that a human executed the read, so this FULL verdict rests on that metadata-level basis plus the declared limit (section 7).
**Verdict: FULL, no edit. No defect recorded.**

### P4 — `.claude/skills/api-event-architect/references/api-event-contract-conventions.md` — read whole, L1–83

**Purpose and normal use:** the owning skill's convention sheet — versioned event-envelope schema and naming, webhook delivery-policy table, per-operation API schema conventions, the consumer checklist that ships with the docs, and the deprecation-sequence template.

**B1 satisfied** — L1 title and L3 "Supporting detail for the owning [API Event Architect]"; L4–8 expands API, RFC 3339, HMAC-SHA256 and SSRF, and defines `2xx`. **B2 partial** — API, RFC 3339, HMAC-SHA256, SSRF and `2xx` are expanded at first use, but **`HTTP` at L8 and `HTTPS` at L42 are not expanded**; `JSON` appears only as a code-block language marker and is a standard format name, and the remaining text is technical vocabulary defined by its sentence (thin payload, idempotency, dead-letter, jitter). The unexpanded first uses are B2 gaps and the page verdict is PARTIAL. **B3 satisfied** — a concrete JSON envelope example L12–21; the naming example L23–24; the delivery-policy table L33–42; the operation-schema table L51–56; the consumer checklist L61–70; and the five-step deprecation template L72–83. **B4 satisfied** — the page is a template/guidance sheet, and labels the full-payload option as requiring a stated reason and data-egress review (L25–27); no shipped claim. **B5 satisfied** — the L3 internal link resolves; the two named skills used as ownership handoffs exist; no command is given. **B6 — basis:** git metadata names the page authors and this reader stage identity committed none of these pages; **limit:** metadata cannot prove non-authorship of commits made under the owner account or that a human executed the read, so this PARTIAL verdict uses that declared limit (section 7); the PARTIAL comes from the B2 gaps above.
**Verdict: PARTIAL, no edit. Named defects: L8 — `HTTP` and L42 — `HTTPS` used without first-use expansions.**

### P5 — `.claude/skills/appsec-implementer/SKILL.md` — read whole, L1–183

**Purpose and normal use:** a manual-only skill that turns one named, already-decided application-security control into a small test-first code change — negative test red then green, minimal control at the authoritative boundary, positive coverage where over-blocking is possible, and a scoped diff — so a security reviewer can verify it.

**B1 satisfied** — the description L2–3 (MANUAL-ONLY; never auto-invoke) and Purpose L13–21 say what the skill is and who should read it; Use When L23–40 names the reader's named-control situation and the do-not-use boundaries. **B2 satisfied** — AppSec, API, ORM, UX, authz and the § symbol are expanded at L9–11; RLS is expanded at L37, UI at L118, SSRF in the description L3; MANUAL-ONLY is the library's own marker (measured: the token appears on 129 skill files) and the standard cookie attribute names HttpOnly/Secure/SameSite are used as control names (measured on 4 skill files) — recorded as observations, not gaps. **B3 satisfied** — a numbered 8-step workflow L58–86, a copyable Output Format L88–106, a validation checklist L108–122, Security Rules L124–136, concrete control examples L25–29, and the red→green negative-test shape L96–99. **B4 satisfied** — the skill is explicitly manual-only and side-effecting (L3), separates a decided control from invention (L20–21), requires the change-classification and approval path (L69–71), and makes no shipped-behavior claim. **B5 satisfied** — the internal link to the reference sheet L178–180 resolves; the referenced master-prompt path L126–128 resolves at the head; every named skill in its routing exists (ten named skill tokens measured); the evals files exist; output-template command slots are placeholders, not concrete commands, so there is no command contract to verify. **B6 — basis:** git metadata names the page authors and this reader stage identity committed none of these pages; **limit:** metadata cannot prove non-authorship of commits made under the owner account or that a human executed the read, so this FULL verdict rests on that metadata-level basis plus the declared limit (section 7).
**Verdict: FULL, no edit. No defect recorded.**

### P6 — `.claude/skills/appsec-implementer/references/control-implementation-patterns.md` — read whole, L1–78

**Purpose and normal use:** per-control checklists for the owning skill — input validation, output encoding/XSS, parameterized queries, object-level authorization/IDOR, session and cookie flags, safe file handling, and SSRF/open-redirect — each with the boundary, the minimal practice and the shape of the negative test that proves it.

**B1 satisfied** — L1 title and L3 "Progressive-disclosure detail for the owning [AppSec Implementer]"; L3–11 explains what each pattern gives. **B2 partial** — XSS, SQL/NoSQL injection, ORM, IDOR and SSRF are explained at L4–8, but **`HTML`/`JS`/`CSS`/`URL` at L24–25 and `4xx` at L18–19 are used without a first-use expansion**; HttpOnly/Secure/SameSite are named in the checklist as standard cookie attributes. The library-norm counts are corrected in section 6 and give no B2 exception; the unexpanded first uses are B2 gaps and the page verdict is PARTIAL. **B3 satisfied** — seven headed pattern sections, each with **Boundary / Do / Negative test**, plus general rules L72–78; concrete payload examples at L27, L35, L61–62 and L69–70; positive-case guidance L19–20. **B4 satisfied** — a checklist/template page that closes with the general rules; no shipped-behavior claim. **B5 satisfied** — the L3 internal link resolves; the one named skill (multi-tenant-security-tester) exists; no shell command is given. **B6 — basis:** git metadata names the page authors and this reader stage identity committed none of these pages; **limit:** metadata cannot prove non-authorship of commits made under the owner account or that a human executed the read, so this PARTIAL verdict uses that declared limit (section 7); the PARTIAL comes from the B2 gaps above.
**Verdict: PARTIAL, no edit. Named defects: L24–25 — `HTML`/`JS`/`CSS`/`URL` and L18–19 — `4xx` used without first-use expansions.**

### P7 — `.claude/skills/architecture-advisor/SKILL.md` — read whole, L1–206

**Purpose and normal use:** advises on architecture STYLE/paradigm for a given system — interview the need first, present only the genuinely relevant candidates, weigh them for this case with honest costs, recommend one with reasoning and sensitivity, resist trend-chasing in both directions, and hand off concrete architecture, cloud posture, tenancy and domain modeling to their owning skills.

**B1 satisfied** — description L2–3, Purpose L12–27 and Use When L29–53 state the job, the reader and the boundaries. **B2 satisfied** — SOA and ops are expanded at L8–10; the style names (monolith, modular monolith, microservices, event-driven, serverless, SOA, hybrid) are explained in Purpose and Workflow rather than left as codes. **B3 satisfied** — a numbered 8-step workflow L70–113, copyable Output Format L119–134, validation checklist L136–155, and concrete examples: the sensitivity examples L98–100 ("if the team splits into four and traffic 10×es"), the case-specific cost guidance L87–91, and the distributed-monolith warning L166–168. **B4 satisfied** — advisory guidance only; it makes no shipped-behavior claim and explicitly says the recommendation is not adopted silently (L92–96). **B5 satisfied** — the reference link L115–117 resolves; every named skill in the handoffs exists (five named skill tokens measured); the evals files exist; no shell command is given. **B6 — basis:** git metadata names the page authors and this reader stage identity committed none of these pages; **limit:** metadata cannot prove non-authorship of commits made under the owner account or that a human executed the read, so this FULL verdict rests on that metadata-level basis plus the declared limit (section 7).
**Verdict: FULL, no edit. No defect recorded.**

### P8 — `.claude/skills/architecture-advisor/references/architecture-style-sheet.md` — read whole, L1–61

**Purpose and normal use:** the owning advisor's style sheet — the need-interview checklist that must be completed before advice, the per-style fit factors table, the trend-trap and distributed-monolith warnings, the recommendation requirements, and the handoff list.

**B1 satisfied** — L1 title and L3 "Detail for the owning [Architecture Advisor]. Read on demand."; L4–6 expands SOA and ops. **B2 partial** — SOA and ops are defined at L4–6 and the style names are the table's own explained rows, but **`w/o` at L26 is not expanded**. The unexpanded first use is a B2 gap and the page verdict is PARTIAL. **B3 satisfied** — the checklist L8–19, the seven-row fit table L21–31, the warnings L33–46, the recommendation requirements L48–54 and the handoff list L56–61 give concrete use; examples such as "traffic ×N" appear at L53 and the "boring option" case at L44–46. **B4 satisfied** — a checklist/reference sheet; no shipped-behavior claim. **B5 satisfied** — the L3 internal link resolves; all four named skills in the handoffs exist; no shell command is given. **B6 — basis:** git metadata names the page authors and this reader stage identity committed none of these pages; **limit:** metadata cannot prove non-authorship of commits made under the owner account or that a human executed the read, so this PARTIAL verdict uses that declared limit (section 7); the PARTIAL comes from the B2 gap above.
**Verdict: PARTIAL, no edit. Named defect: L26 — `w/o` used as an abbreviation without a first-use expansion.**

## 6. Library-norm measurements for tokens that could look like gaps

These counts were re-measured at `main` 14747958 across the **383** Markdown files under `.claude/skills` (command: `git grep -l -F -- <token> 14747958 -- .claude/skills`, counting files): **Diátaxis** 11; **4xx** 6; **HttpOnly** 4; **MANUAL-ONLY** 129; **OpenAPI** 9; **GraphQL** 10; **HTML** 16. **The B2 bullet has no library-norm exception.** These measurements are context only: a token frequency across the library does not define it on the page, so they do not convert an unexpanded first use into compliance and no page verdict is reduced or raised by them. The B2 gaps on P2, P4, P6 and P8 stand as named gaps in section 5.

## 7. Provenance, page authorship and reader-independence witness rows

**Blob and commit provenance.** Each row's blob id below resolves at the pinned ref `2db1ffb7` and is identical at `main` 14747958 (zero drift, section 1). The last-touching commit is the commit that most recently changed that path on `main`; the author is git metadata, not an authorship claim beyond it.

| # | Page | Full blob id (40 hex) | Last-touching commit (40 hex) | Commit author | Commit date | Reader identity (did not write the page) |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | `.claude/skills/api-doc-generator-designer/SKILL.md` | `ce0c26dbf2bc1fdd3dd6b610f5e8dd9b9f4ba2ee` | `2a86058396410357a771eb44e33cff0436940e9d` | Peter Nguyen | 2026-09-28 | sd-c-793-r2 / sd-c-read-b9-c1 |
| P2 | `.claude/skills/api-doc-generator-designer/references/api-doc-sheet.md` | `aaa9134f3106736450e816af57f6e9c8c709ea05` | `5e0e9ad7d79b109aabcc3d2531061fadf84af592` | Peter Nguyen | 2026-09-23 | sd-c-793-r2 / sd-c-read-b9-c1 |
| P3 | `.claude/skills/api-event-architect/SKILL.md` | `4bc92cf83f3737b7027256076331a2aa3952968d` | `7645ca4998fd4f26be5c9236ae201cbab6216c10` | ModernNomad-98 | 2026-10-10 | sd-c-793-r2 / sd-c-read-b9-c1 |
| P4 | `.claude/skills/api-event-architect/references/api-event-contract-conventions.md` | `c9dec9807a6ec34839ddf3f9b624e000d9cb70c5` | `7645ca4998fd4f26be5c9236ae201cbab6216c10` | ModernNomad-98 | 2026-10-10 | sd-c-793-r2 / sd-c-read-b9-c1 |
| P5 | `.claude/skills/appsec-implementer/SKILL.md` | `726ee517b6fd4dac246d23affc914f28f65f3183` | `14ecd0c3dc9dd0b2402990fd757df46ac28986e5` | Peter Nguyen | 2026-09-28 | sd-c-793-r2 / sd-c-read-b9-c1 |
| P6 | `.claude/skills/appsec-implementer/references/control-implementation-patterns.md` | `0602bd7603d2d3e5f6dd1e53146d5cc1e80f0590` | `5e0e9ad7d79b109aabcc3d2531061fadf84af592` | Peter Nguyen | 2026-09-23 | sd-c-793-r2 / sd-c-read-b9-c1 |
| P7 | `.claude/skills/architecture-advisor/SKILL.md` | `c844bb13fec84570cc702271598fb0493bac6d60` | `76544ad9efef325710ca27caacf8c468f244795f` | Peter Nguyen | 2026-09-26 | sd-c-793-r2 / sd-c-read-b9-c1 |
| P8 | `.claude/skills/architecture-advisor/references/architecture-style-sheet.md` | `9ca2aa084c66cce53f492f74f8381e2cb36a45a1` | `5e0e9ad7d79b109aabcc3d2531061fadf84af592` | Peter Nguyen | 2026-09-23 | sd-c-793-r2 / sd-c-read-b9-c1 |

**Reader-independence witness (B6).** For every page, the reader is a different agent identity from the git-metadata author recorded above. **Basis:** the page authors are Peter Nguyen or the ModernNomad-98 account, and this reader stage identity committed none of these pages; the surviving FULL verdicts (P1, P3, P5, P7) state that metadata basis at page level in section 5. **Limit:** git metadata cannot prove non-authorship of commits made under the owner account, nor that a human executed the reading; the record does not claim more than the metadata can carry (section 11). The four PARTIAL pages are PARTIAL for their recorded B2 gaps and do not rely on B6 for a FULL.

## 8. Hunk and line accounting

- **Tracked change:** exactly **one added path** — this record, `docs/evidence/documentation/readability-lane-a-batch-9-2026-10-18.md` — and no other tracked path; **0 modified, 0 deleted, 0 renames**. The branch is created from `main` 14747958, so the only hunk in the PR diff is the addition of this file.
- **Page accounting:** **zero hunks touch any of the eight pages**; every page's `git diff --numstat 2db1ffb7..main -- <page>` is empty (section 1), and the batch made no page edit, no keeper row, no index/ledger/register/manifest/tool/test/workflow change.
- **Record's own measurement:** per the plan's AC6, this record's final bytes, LF and sha256 are measured and stated in the **PR body binding outside this record**, not inside it; the body is updated after this file is frozen at the PR head. No self-computed size claim is made here.

## 9. Plan AC1–AC8 — Stage C declaration (what is met, what is owed)

| AC | Stage C status and evidence |
| --- | --- |
| AC1 Tree proof | **MET at the final head by construction** — exactly one added path (this record) from main 14747958; 0 modified/deleted; the exact head/tree/base are posted in the Stage C handoff and the PR body. |
| AC2 Frozen page set by blob hash | **MET in this record** — eight paths, indices 48–55, blobs/bytes/LF at pinned ref `2db1ffb7`, identical at the base (zero drift). |
| AC3 Whole-page re-read evidence | **MET in this record** — each page read whole L1–last; six bullets addressed with page-line cites; links, named files and tokens measured. |
| AC4 Honest per-page disposition | **MET in this record (repaired)** — 4 FULL / 4 PARTIAL / 0 UNRUN, one basis per page; the four B2 gaps on P2/P4/P6/P8 are named with page lines and are not upgraded; no acceptance row is authored for any PARTIAL page; the section-6 counts are corrected (D F5) and B6 is stated at page level for the surviving FULLs (D O1). |
| AC5 Provenance and attribution | **MET in this record** — blob ids, last-touching commits/authors/dates, reader identity and the independence limit (section 7); DCO/model attribution is applied to the commit and the PR body. |
| AC6 PR body and PROC-04 | **OWED after this file is frozen** — the PR body binds the plan capture and the record's final bytes/LF/sha256 outside the record; its PROC-04 is computed from the final body and the repository body checker is run at the head. |
| AC7 Codex loop | **OWED after the PR exists at its head** — trigger, fetch every inline finding, fix P1/P2 (or record not-a-defect under AEGIS-APR-050), reply naming the fixing SHA, resolve, retrigger; head-bound unavailability only after all P1/P2 are triaged; never a pass. |
| AC8 Stage entry conditions | **SATISFIED for C** — acted only on the fresh Stage B ACCEPT 6243652578 bound to plan comment 6243633250, branched from then-current main, re-derived the pending set and lane bounds, added exactly the one record path, one DCO-signed commit, then posts the handoff; D/E/F/G remain separate agents and G owns the merge. |

## 10. Validation actually run while authoring (before commit)

| Check | Command / method | Result |
| --- | --- | --- |
| Instrument at the pinned ref | `python -P -B tools/readability_acceptance/check_index.py --ref 2db1ffb7... --json` in a fresh clone of main 14747958 | **exit 0**; summary 690 / 107 / 6 / 567 / 0 / 6 / 0 / 4 / 583 (the lane derivation in section 1) |
| Page blobs, bytes, LF | `git rev-parse 2db1ffb7:<page>`, `git cat-file -s`, line counts over the pinned blob for all eight | **blob ids match the plan/B table; sizes/LF match; totals 64,259 B / 1,155 LF** |
| Zero drift to the base | `git diff --numstat 2db1ffb7..14747958 -- <page>` for all eight | **empty for all eight** |
| Internal links resolve | extract every Markdown link from the eight pages and resolve each relative target at main 14747958 | **0 broken links**; the only external links are documentation URLs, not fetched here |
| Named files and skills exist | resolve every backticked skill token to `.claude/skills/<name>/SKILL.md` at main; check each named `evals/` path | **all named skills exist; evals files exist where a SKILL page names them** |
| Commands in the pages | search for concrete shell command lines in the eight pages | **no concrete shell commands are given** (template slots such as <cmd> are placeholders), so there is no command-existence claim to verify |
| Authorship metadata | `git log -1 --format=%H|%an|%ad --date=short -- <page>` for all eight | **recorded in section 7** |
| Library-norm tokens (corrected) | `git grep -l -F -- <token> 14747958 -- .claude/skills` over the 383 Markdown files under `.claude/skills` | **Diátaxis 11 / 4xx 6 / HttpOnly 4 / MANUAL-ONLY 129 / OpenAPI 9 / GraphQL 10 / HTML 16**; counts are context only and create no B2 exception (section 6) |
| Repair revision (Stage C repair) | D verdict **6243802528**: four FULL claims failed on B2 gaps and the section-6 counts did not reproduce | **P2/P4/P6/P8 corrected to PARTIAL with named page lines; section 6 recomputed; B6 stated at page level for P1/P3/P5/P7; page set/blobs/bytes/LF unchanged and no page re-read substituted** |
| Page edits | branch state before adding this record | **none of the eight pages modified; the only pending change is this added record** |

**Not yet run at this point (owed and declared, never claimed):** post-commit `git diff --check`, DCO check, `validate-skills.py`, the repository Markdown-link test suite, the PR-body bound-field checker, hosted CI results at the exact head, and the Codex loop. They are recorded in the Stage C handoff and the PR body at the exact head once they have actually run; any that cannot run is recorded **UNRUN** with its reason.

## 11. What this batch could not verify (stated, not hidden)

- **B6 as a human act.** The metadata shows the reader identity differs from the page authors, but it cannot prove non-authorship of commits made under the owner account or that a human performed the reading; the batch independence claim is limited to that metadata-level basis and declared limit (sections 5 and 7).
- **Future keeper acceptance.** This record does not create acceptance rows; a later eligible keeper under AEGIS-APR-101/APR-117 decides which rows to record and remains separate from this reader.
- **Hosted checks and Codex.** No pull request or head existed while this record was authored; hosted CI results, the PR-body checker outcome, and the Codex loop are owed at the head and are not claimed here.
- **Drift after the base.** The frozen blobs are measured at the pinned ref and main 14747958; a later movement of the pages, the index or the lane bounds would reopen the batch and is not claimed away.
- **Prose reading as a quality judgment.** This record lists what the page says and where; it does not claim a formal usability study beyond the six acceptance bullets.

## Repair revision — Stage D REVISE 6243802528 answered (2026-10-18)

Stage D exact-head audit returned **REVISE** (verdict **6243802528**): AC1-AC3 and AC5-AC8 were MET and reproduced, but **AC4 was NOT MET** because four all-FULL dispositions were unjustified by B2 first-use gaps, and the section-6 library-norm counts did not reproduce. This repair revision answers the findings without re-selecting or re-reading the frozen page set:

- **F1 (P2):** the page `REST` at **L6** is not expanded (`RPC` is the only expansion there); P2 is now **PARTIAL** with that gap named.
- **F2 (P4):** `HTTP` at **L8** and `HTTPS` at **L42** are not expanded; P4 is now **PARTIAL** with both gaps named.
- **F3 (P6):** `HTML`/`JS`/`CSS`/`URL` at **L24-25** and `4xx` at **L18-19** are not expanded; P6 is now **PARTIAL** with those gaps named, and the section-6 counts no longer supply an exception.
- **F4 (P8):** `w/o` at **L26** is not expanded; P8 is now **PARTIAL** with that gap named.
- **F5 (section 6):** the count table is corrected to **Diátaxis 11, 4xx 6, HttpOnly 4, MANUAL-ONLY 129, OpenAPI 9, GraphQL 10, HTML 16** across **383** skill Markdown files at main 14747958; the measurements are context only and create no B2 exception.
- **O1 (B6):** the surviving FULLs (P1/P3/P5/P7) now state the metadata-level B6 basis and its declared limit at page level; the PARTIAL pages do not rely on B6 for a FULL.
- **O2 (Codex trigger):** the missing model-attribution line on trigger 6243734017 is recorded as an observation; the repair re-trigger at the new head carries the model line.
- **O3 (PR body):** the body eight-page summary, library-norm sentence and AC4 row are updated with this revision, and the body names the repair commit and the new head.

**Repaired disposition tally: 4 FULL / 4 PARTIAL / 0 UNRUN.** The frozen page set, blobs, bytes/LF and zero drift are unchanged; no page was edited or re-read in place of the original whole-page read; P2/P4/P6/P8 keep their original full-page reads and are now honestly PARTIAL. No keeper/acceptance row is authored here. The record own final bytes/LF/sha256 remain in the PR body outside the record (plan AC6).

## 12. Continuation — what the next stage needs

The record is the only added path; the branch is created from `main` 14747958 and needs one DCO-signed commit naming this record. **Stage D** independently audits AC1–AC8 at the exact head (no C/D sharing), including the frozen blob set, the pure-append tree proof, the dispositions and the body binding. **Stage E** runs the repository checks at the head and records every UNRUN honestly. **Stage F** reviews the exact head with the final PROC-04. **Stage G** applies the merge gates including MG3 under the recorded reading; **no merge occurs before G**, and any need outside the one-path blast radius stops the ladder and returns to Stage A/the owner.

**Boundary.** Stage C only: this record is authored evidence; no page was edited, no keeper row, ledger, index, register, manifest, tool, test or workflow changed; no other PR was touched; no Codex thread was replied to or resolved from this stage; no merge occurred.

**Signed with both names: true identity sd-c-793-r2; stage role sd-c-read-b9-c2 (Stage C repair revision; original Stage C role sd-c-read-b9-c1).** **Written by: DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness).**
