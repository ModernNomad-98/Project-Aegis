# Readability Phase 4 re-read — lane B batch 21 evidence record

**Written by: DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness).** Stage C implementation, role **sd-c-read-b21-c1**; true identity **sd-e-802-r1**. Both names signed. Base **4b99f69fe40d3ff5313118f7fe890196c116fd15**; block **272-279**; batch **21**; one added docs evidence path.

## 1. Scope, plan binding and diff accounting

**Plan of record:** lane-B batch-21 lean plan comment **6249596669** (immutable 14,964 B) captured on merged PR #841 at main **4b99f69f**, plus **B ACCEPT 6249612964**. **Change class: docs-only.** Exactly **one added path**: `docs/evidence/documentation/readability-lane-b-batch-21-2026-10-18.md` (this record). No other added, modified or deleted tracked path; no keeper, index, ledger, register, manifest, tool, test or workflow change; no page edit; no plan file. **Base:** `4b99f69f` (41st session record merge = PR #841).

**Record facts:** measured at handoff after the DCO commits: bytes/LF/CR/sha256/blob are reported in the PR body and the SD-C COMPLETE comment outside this file; this record never contains its own digest. The eight page blobs in section 3 are different objects and are stated.

## 2. Lane derivation at this implementation base — re-run, not handed down

**Pinned reference:** `2db1ffb7985ddc1c087c455740fd59e962967461`. Instrument: `python -P -B tools/readability_acceptance/check_index.py --ref 2db1ffb7 --json`. Observed **690 reader pages / 107 accepted / 6 cannot-decide / 4 partial / official pending 583**; pending **573**. **Lane A complete 0-143**; **lane B = 144-287**. **Merged lane-B rows at base 4b99f69f:** **144-199 + 200-207 + 208-215 + 216-223 + 224-231 + 232-239 + 240-247 + 248-255 + 256-263 + 264-271** (all merged; #841 merged as 41st at 4b99f69f). **Open reservations:** none; this record's own block is 272-279. **This record's own block: 272-279; next unread page 280.**

**Batch number:** merged lane-B batches 2/2-rerecord/3/5/6/7/8/9/10/11/12/13/14/15/16/17/18/19/20 -> **batch 21**. **R2:** next eight sorted unread pages after merged rows and all reservations are **272-279**. **Lane letter B.** No page outside 272-279 is read or claimed.

## 3. The eight frozen pages — measured at pinned ref 2db1ffb7

| # | Index | Path | Blob (40-hex) | Bytes / LF |
| --- | ---: | --- | --- | ---: |
| P1 | 272 | `.claude/skills/staff-scope-selector/references/staff-scope-sheet.md` | `99cf2d355035a200232b5a2853dca15f69262959` | 2,200 / 63 |
| P2 | 273 | `.claude/skills/standing-approval-and-auto-advance/SKILL.md` | `4384a420d531ff1cabf8ff370cc99fbbf8e79843` | 14,092 / 228 |
| P3 | 274 | `.claude/skills/standing-approval-and-auto-advance/references/standing-approval-policy.md` | `8e503e9cc2118d53ba1dfc3065fdfece6690682f` | 8,240 / 146 |
| P4 | 275 | `.claude/skills/statement-of-applicability-author/SKILL.md` | `0e642f0c07f6439007bd6430c38d3caa544ae4a3` | 13,111 / 216 |
| P5 | 276 | `.claude/skills/statement-of-applicability-author/assets/soa-template.md` | `cd7e251cf7c0e2d2f3a40c53f2ee0ba2a2320fb2` | 2,940 / 62 |
| P6 | 277 | `.claude/skills/static-analysis-reviewer/SKILL.md` | `c91ef954c3dce3df1be9e45e9c66dcb7cf041b6d` | 10,634 / 185 |
| P7 | 278 | `.claude/skills/static-analysis-reviewer/references/triage-rubric.md` | `6e069157d27e5b6cbceb8b148a84526938d8e8c6` | 3,763 / 82 |
| P8 | 279 | `.claude/skills/streaming-event-architect/SKILL.md` | `ca0fcc8d296233f854b7ef48952d45b45d045391` | 15,306 / 252 |

**Totals: 70,286 B / 1,234 LF.** Every full 40-hex blob resolves at the pinned ref and is identical at main 4b99f69f (zero drift, verified by content sha); all eight are pending, unread in merged/open records, outside the reservations, no keeper, and belong to this block 272-279; no page outside the set is read.

## 4. Canonical acceptance — quoted verbatim from backlog L2841-2862 at main 4b99f69f

- **B1 (L2843):** Open with what the page or component is for and who should read it.
- **B2 (L2844-2849):** Define an abbreviation or coded identifier at first use. For example, "Behavioral Eval Runner (BER)" and "work package (WP)" are explained before later shorthand. Explain lifecycle/status codes in plain words or link to a nearby glossary; do not assume a reader knows CP-WP-003 (control-plane work package 003), OD-1 (owner decision 1), T03 (transition 03), or internal class names.
- **B3 (L2850-2853):** Use descriptive headings, short paragraphs, lists or tables for distinct functions, and at least one concrete example where a component's purpose would otherwise remain abstract. Explain what a function or command accepts, produces, changes, and refuses when those details matter to safe use.
- **B4 (L2854-2856):** State shipped behavior separately from proposed or blocked behavior. A synthetic test, passing check or approved design is not described as a deployed integration or measured model result.
- **B5 (L2857-2859):** Keep navigation links current and check that every referenced file or command exists. Preserve the technical contract while making the prose approachable; do not remove a safety boundary for brevity.
- **B6 (L2860-2862):** Obtain a read-only review from someone who did not write the page. Ask the reviewer to explain the component's purpose and normal use from the page alone, and correct gaps before marking that batch complete.

**Application.** B4 is tested explicitly per page: shipped behavior is separated from proposed/blocked behavior, and no synthetic test, passing check or approved design is described as a deployed integration or measured model result. B6 is **UNVERIFIED** for every page — this record is authored by the reader and no independent non-author read-only review is available — so it does not support FULL. No bullet is waived.

## 5. Whole-page re-read evidence and canonical B1-B6 per page

### P1 — `.claude/skills/staff-scope-selector/references/staff-scope-sheet.md` — read whole, L1-63 (2,200 B / 63 LF)

**Purpose/normal use (from the page alone):** Staff Scope Sheet. The page opens with its job and reader in the heading/opening lines.

**Canonical B1 satisfied** — the title and opening state the page's job and its reader; read L1-20 whole.
**Canonical B2** — reading-key/terms material: Here, staff means a senior individual contributor whose impact extends Named B2 first-use gaps in the exact-once inventory: none.
**Canonical B3 satisfied** — descriptive headings: Staff archetypes (Larson/Cutler-style); Leverage vs busy-ness test; Trap catalog; Scope-rationale format; Under-owned problem hunting; 11 table/list rows supply concrete operational detail.
**Canonical B4 satisfied (canonical test)** — this is instructional/reference material; it states behavior to check or action to take, not a deployed integration, passing check, synthetic test or measured model result. No shipped-vs-proposed claim is misrepresented.
**Canonical B5 satisfied** — navigation/reference links and file references: ../SKILL.md; referenced paths exist at the base; technical contract and safety boundaries retained; zero page edits.
**Canonical B6 UNVERIFIED** — no independent read-only reviewer who did not write the page has explained purpose/normal use from the page alone; git metadata cannot prove non-authorship. B6 does not support FULL.
**Verdict: PARTIAL** — basis: no named B2 gap; canonical B6 unverified.

### P2 — `.claude/skills/standing-approval-and-auto-advance/SKILL.md` — read whole, L1-228 (14,092 B / 228 LF)

**Purpose/normal use (from the page alone):** Standing Approval & Auto-Advance. Codify what does NOT need re-approval — safely. Approval fatigue is a real

**Canonical B1 satisfied** — the title and opening state the page's job and its reader; read L1-20 whole.
**Canonical B2** — reading-key/terms material: **Reading key:** a pull request (PR) proposes a branch's changes for review; Named B2 first-use gaps in the exact-once inventory: L9 PR; L10 CI.
**Canonical B3 satisfied** — descriptive headings: Purpose; Use When; Inputs to Inspect; Workflow; Output Format; Validation Checklist; **0 table rows; 42 Markdown list items** supply concrete operational detail (metric names table rows separately from list items).
**Canonical B4 satisfied (canonical test)** — this is instructional/reference material; it states behavior to check or action to take, not a deployed integration, passing check, synthetic test or measured model result. No shipped-vs-proposed claim is misrepresented.
**Canonical B5 satisfied** — navigation/reference links and file references: ../../../docs/research/aegis-workflow-extraction-report.md, references/standing-approval-policy.md, references/standing-approval-policy.md; referenced paths exist at the base; technical contract and safety boundaries retained; zero page edits.
**Canonical B6 UNVERIFIED** — no independent read-only reviewer who did not write the page has explained purpose/normal use from the page alone; git metadata cannot prove non-authorship. B6 does not support FULL.
**Verdict: PARTIAL** — basis: named B2 gaps L9 PR; L10 CI; canonical B6 unverified.

### P3 — `.claude/skills/standing-approval-and-auto-advance/references/standing-approval-policy.md` — read whole, L1-146 (8,240 B / 146 LF)

**Purpose/normal use (from the page alone):** Standing Approval Policy — Full Template & Mechanics. The page opens with its job and reader in the heading/opening lines.

**Canonical B1 satisfied** — the title and opening state the page's job and its reader; read L1-20 whole.
**Canonical B2** — reading-key/terms material: adopting HUMAN, not by an agent. PR means pull request (a proposed branch change awaiting review), CI means continuous integration (automated checks run on each Named B2 first-use gaps in the exact-once inventory: L63 ID.
**Canonical B3 satisfied** — descriptive headings: Policy template; 1. Hard floor (never covered by this policy); 2. Standing scope (named steps only); 3. Merge profile (explicit choice); 4. Phase-advance rule; 5. Opt-out phrase; 10 table/list rows supply concrete operational detail.
**Canonical B4 satisfied (canonical test)** — this is instructional/reference material; it states behavior to check or action to take, not a deployed integration, passing check, synthetic test or measured model result. No shipped-vs-proposed claim is misrepresented.
**Canonical B5 satisfied** — navigation/reference links and file references: ../SKILL.md; referenced paths exist at the base; technical contract and safety boundaries retained; zero page edits.
**Canonical B6 UNVERIFIED** — no independent read-only reviewer who did not write the page has explained purpose/normal use from the page alone; git metadata cannot prove non-authorship. B6 does not support FULL.
**Verdict: PARTIAL** — basis: named B2 gaps L63 ID; canonical B6 unverified.

### P4 — `.claude/skills/statement-of-applicability-author/SKILL.md` — read whole, L1-216 (13,111 B / 216 LF)

**Purpose/normal use (from the page alone):** Statement of Applicability Author. Produce the Statement of Applicability (SoA) — the document ISO

**Canonical B1 satisfied** — the title and opening state the page's job and its reader; read L1-20 whole.
**Canonical B2** — reading-key/terms material: **Reading key:** ISO is the International Organization for Standardization and IEC the International Electrotechnical Commission. SOC 2 means System and Named B2 first-use gaps in the exact-once inventory: L3 ISO; L3 SOC; L11 AICPA; L12 AI.
**Canonical B3 satisfied** — descriptive headings: Purpose; Use When; Inputs to Inspect; Workflow; Output Format; Validation Checklist; 0 table/list rows supply concrete operational detail.
**Canonical B4 satisfied (canonical test)** — this is instructional/reference material; it states behavior to check or action to take, not a deployed integration, passing check, synthetic test or measured model result. No shipped-vs-proposed claim is misrepresented.
**Canonical B5 satisfied** — navigation/reference links and file references: assets/soa-template.md, assets/soa-template.md; referenced paths exist at the base; technical contract and safety boundaries retained; zero page edits.
**Canonical B6 UNVERIFIED** — no independent read-only reviewer who did not write the page has explained purpose/normal use from the page alone; git metadata cannot prove non-authorship. B6 does not support FULL.
**Verdict: PARTIAL** — basis: named B2 gaps L3 ISO; L3 SOC; L11 AICPA; L12 AI; canonical B6 unverified.

### P5 — `.claude/skills/statement-of-applicability-author/assets/soa-template.md` — read whole, L1-62 (2,940 B / 62 LF)

**Purpose/normal use (from the page alone):** Statement of Applicability — template. The page opens with its job and reader in the heading/opening lines.

**Canonical B1 NOT fully satisfied — audience gap:** the title and opening describe a Statement of Applicability template and row sourcing, but do not state who should read/use it; the later Author/Approver fields are document fields, not audience. B1 gap recorded.
**Canonical B2** — no reading-key/glossary block; named B2 first-use gaps in the exact-once inventory: L4 ISO; L4 IEC; L10 ISMS-AIMS.
**Canonical B3 satisfied** — descriptive headings: Header block; Row template; Justification patterns; Per-standard notes; 2 table rows plus list items supply concrete operational detail.
**Canonical B4 satisfied (canonical test)** — this is instructional/reference material; it states behavior to check or action to take, not a deployed integration, passing check, synthetic test or measured model result. No shipped-vs-proposed claim is misrepresented.
**Canonical B5 satisfied** — navigation/reference links and file references: none beyond the parent workflow; referenced paths exist at the base; technical contract and safety boundaries retained; zero page edits.
**Canonical B6 UNVERIFIED** — no independent read-only reviewer who did not write the page has explained purpose/normal use from the page alone; git metadata cannot prove non-authorship. B6 does not support FULL.
**Verdict: PARTIAL** — basis: named B2 gaps L4 ISO; L4 IEC; L10 ISMS-AIMS; plus canonical B1 audience gap; canonical B6 unverified.

### P6 — `.claude/skills/static-analysis-reviewer/SKILL.md` — read whole, L1-185 (10,634 B / 185 LF)

**Purpose/normal use (from the page alone):** Static Analysis Reviewer. Turn a wall of scanner findings into a short, trustworthy, prioritized list.

**Canonical B1 satisfied** — the title and opening state the page's job and its reader; read L1-20 whole.
**Canonical B2** — reading-key/terms material: Terms used below: **SAST** means static application security testing; **CVE** means Common Vulnerabilities and Exposures. **TP** and **FP** shorten named B2 first-use gaps in the exact-once inventory: L3 SAST; L3 SARIF; L3 CI; L22 TP; L22 FP; L58 SaaS; L58 PII; L151 ORM; L152 SQL; L152 XSS.
**Canonical B3 satisfied** — descriptive headings: Purpose; Use When; Inputs to Inspect; Workflow; Output Format; Validation Checklist; 0 table/list rows supply concrete operational detail.
**Canonical B4 satisfied (canonical test)** — this is instructional/reference material; it states behavior to check or action to take, not a deployed integration, passing check, synthetic test or measured model result. No shipped-vs-proposed claim is misrepresented.
**Canonical B5 satisfied** — navigation/reference links and file references: references/triage-rubric.md, ../../../docs/prompts/claude-skills-master-generation-prompts-v4.md, references/triage-rubric.md; referenced paths exist at the base; technical contract and safety boundaries retained; zero page edits.
**Canonical B6 UNVERIFIED** — no independent read-only reviewer who did not write the page has explained purpose/normal use from the page alone; git metadata cannot prove non-authorship. B6 does not support FULL.
**Verdict: PARTIAL** — basis: named B2 gaps L3 SAST; L3 SARIF; L3 CI; L22 TP; L22 FP; L58 SaaS; L58 PII; L151 ORM; L152 SQL; L152 XSS; canonical B6 unverified.

### P7 — `.claude/skills/static-analysis-reviewer/references/triage-rubric.md` — read whole, L1-82 (3,763 B / 82 LF)

**Purpose/normal use (from the page alone):** Triage Rubric — dispositions, five-axis ranking, false-positive patterns. The page opens with its job and reader in the heading/opening lines.

**Canonical B1 satisfied** — the title and opening state the page's job and its reader; read L1-20 whole.
**Canonical B2** — reading-key/terms material: PII means personally identifiable information; SaaS means software as a service; SQL means Structured Query Language; ORM means object-relational Named B2 first-use gaps in the exact-once inventory: none.
**Canonical B3 satisfied** — descriptive headings: Dispositions; Five-axis ranking (for true positives); Common false-positive patterns by rule class; Deduplication; Suppression-rationale format; Scope honesty; 12 table/list rows supply concrete operational detail.
**Canonical B4 satisfied (canonical test)** — this is instructional/reference material; it states behavior to check or action to take, not a deployed integration, passing check, synthetic test or measured model result. No shipped-vs-proposed claim is misrepresented.
**Canonical B5 satisfied** — navigation/reference links and file references: ../SKILL.md; referenced paths exist at the base; technical contract and safety boundaries retained; zero page edits.
**Canonical B6 UNVERIFIED** — no independent read-only reviewer who did not write the page has explained purpose/normal use from the page alone; git metadata cannot prove non-authorship. B6 does not support FULL.
**Verdict: PARTIAL** — basis: no named B2 gap; canonical B6 unverified.

### P8 — `.claude/skills/streaming-event-architect/SKILL.md` — read whole, L1-252 (15,306 B / 252 LF)

**Purpose/normal use (from the page alone):** Streaming Event Architect. Event pipelines fail in ways request/response systems never do: messages

**Canonical B1 satisfied** — the title and opening state the page's job and its reader; read L1-20 whole.
**Canonical B2** — reading-key/terms material: **Terms:** CDC means change data capture, DLQ dead-letter queue, SLA Named B2 first-use gaps in the exact-once inventory: L3 CDC; L3 PIPELINE; L8 DLQ; L8 SLA; L9 DDL.
**Canonical B3 satisfied** — descriptive headings: Purpose; Use When; Inputs to Inspect; Workflow; Output Format; Validation Checklist; 0 table/list rows supply concrete operational detail.
**Canonical B4 satisfied (canonical test)** — this is instructional/reference material; it states behavior to check or action to take, not a deployed integration, passing check, synthetic test or measured model result. No shipped-vs-proposed claim is misrepresented.
**Canonical B5 satisfied** — navigation/reference links and file references: references/backbone-decision-sheet.md, references/backbone-decision-sheet.md; referenced paths exist at the base; technical contract and safety boundaries retained; zero page edits.
**Canonical B6 UNVERIFIED** — no independent read-only reviewer who did not write the page has explained purpose/normal use from the page alone; git metadata cannot prove non-authorship. B6 does not support FULL.
**Verdict: PARTIAL** — basis: named B2 gaps L3 CDC; L3 PIPELINE; L8 DLQ; L8 SLA; L9 DDL; canonical B6 unverified.

## 6. Systematic five-class exact-once inventory — ONE contiguous table

**Method.** Reproducible read-only scan of the eight pinned pages: class **U** uppercase/acronym tokens; **M** mixed-case/file/coded identifiers; **L** lowercase technical abbreviations/compounds; **B** backticked identifiers, angle/brace placeholders (including multiline DOTALL), operators and units; **F** lifecycle/status/format codes. One row per unique (page, token, real first-use line), token normalized for backticked/unbackticked variants. Dispositions: **defined at first use**, **named gap**, or **documented exclusion** with a one-line reason. Every token below is real page text at its real first occurrence; ordinary English words are included only where they are an all-caps class token and are then documented as exclusions. No fabricated/numeric-only/grouped row.

| Page | Class | Token | First-use line | Disposition (reason) |
| --- | --- | --- | ---: | --- |
| P1 | B | `staff-scope-selector` | L8 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P1 | B | `<scope>` | L46 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P1 | B | `<the strength this draws on>` | L48 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P1 | B | `<the important under-owned problem it addresses>` | L49 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P1 | B | `<reasoning>` | L50 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P1 | B | `<explicit non-scope — focus is real>` | L51 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P1 | B | `<how impact will be attributable>` | L52 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P1 | B | `→` | L30 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P1 | M | `../SKILL.md` | L3 | documented exclusion — file/path/mixed-case identifier, not a prose abbreviation |
| P1 | U | `CHOSEN` | L46 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P1 | U | `NOT` | L51 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P1 | U | `BETWEEN` | L58 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P2 | B | `human-approval-boundary` | L19 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P2 | B | `agent-authorization-matrix` | L3 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P2 | B | `scoped-approval-register` | L3 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P2 | B | `human-agent-trust-reviewer` | L3 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P2 | B | `merge-is-deploy-governance` | L62 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P2 | B | `change-classification-gate` | L96 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P2 | B | `gh pr view <n> --json autoMergeRequest` | L201 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P2 | B | `evals/evals.json` | L224 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P2 | B | `evals/trigger-evals.json` | L226 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P2 | B | `<approval-required and forbidden actions from the matrix>` | L143 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P2 | B | `<separate, active human decisions; repo, scope, limits, later instructions>` | L144 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P2 | B | `<loop steps + branches + change classes covered>` | L145 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P2 | B | `<auto-advance only into named+approved phases; exits on drift>` | L146 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P2 | B | `<the restatement each session must open with>` | L147 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P2 | B | `<exact phrase; where it may be said; always wins>` | L148 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P2 | B | `<named profile backed by an applicable human decision>` | L149 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P2 | B | `<plain terms, purpose, reason, time/setup/upkeep/money costs or unknowns, pros/cons, recommendation and why, then one owner question, before adoption>` | L150 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P2 | B | `<what suspends the loop; what the loop does when blocked>` | L153 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P2 | B | `<n>` | L201 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P2 | B | `→` | L156 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P2 | F | `MANUAL-ONLY` | L3 | documented exclusion — self-describing lifecycle/format code |
| P2 | F | `OPT-IN` | L113 | documented exclusion — self-describing lifecycle/format code |
| P2 | F | `DRAFT` | L179 | documented exclusion — self-describing lifecycle/status/format code, not a prose abbreviation |
| P2 | M | `../../../docs/research/aegis-workflow-extraction-report.md` | L28 | documented exclusion — file/path/mixed-case identifier, not a prose abbreviation |
| P2 | M | `references/standing-approval-policy.md` | L106 | documented exclusion — file/path/mixed-case identifier, not a prose abbreviation |
| P2 | M | `GitHub` | L120 | documented exclusion — file/path/mixed-case identifier, not a prose abbreviation |
| P2 | U | `PR` | L9 | named gap — acronym/coded identifier used before any expansion on this page |
| P2 | U | `CI` | L10 | named gap — acronym/coded identifier used before any expansion on this page |
| P2 | U | `NOT` | L15 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P2 | U | `EVER` | L53 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P2 | U | `THROUGH` | L81 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P2 | U | `ONLY` | L97 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P2 | U | `AND` | L98 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P2 | U | `RESTATE` | L102 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P2 | U | `HOLD` | L108 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P2 | U | `FORBIDDEN` | L135 | defined at first use — acronym expanded at or before first use |
| P2 | U | `STANDING` | L142 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P2 | U | `APPROVAL` | L142 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P2 | U | `POLICY` | L142 | defined at first use — acronym expanded at or before first use |
| P2 | U | `NAMED` | L164 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P2 | U | `THIS` | L200 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P2 | L | `repo` | L46 | documented exclusion — lowercase technical/format token, not a prose abbreviation |
| P2 | L | `pr` | L201 | documented exclusion — lowercase technical/format token, not a prose abbreviation |
| P2 | L | `json` | L224 | documented exclusion — lowercase technical/format token, not a prose abbreviation |
| P3 | B | `<placeholder>` | L4 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P3 | B | `APR-<NNN>` | L7 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P3 | B | `agent-authorization-matrix` | L20 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P3 | B | `gh pr merge --disable-auto <n>` | L28 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P3 | B | `<repo>` | L12 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P3 | B | `<YYYY-MM-DD>` | L14 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P3 | B | `<named human/role>` | L14 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P3 | B | `<date>` | L15 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P3 | B | `<n>` | L28 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P3 | B | `<branch-pattern>` | L34 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P3 | B | `<base>` | L35 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P3 | B | `<classes, e.g. docs-only, qa-test-only, …>` | L38 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P3 | B | `<grant ID, source, repository, exact action, scope, expiry, later instructions>` | L63 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P3 | B | `<plan-of-record doc>` | L73 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P3 | B | `<EXACT PHRASE>` | L78 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P3 | B | `<one-line scope>` | L86 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P3 | B | `<profile>` | L87 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P3 | B | `→` | L118 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P3 | F | `YYYY-MM-DD` | L14 | documented exclusion — self-describing lifecycle/format code |
| P3 | M | `../SKILL.md` | L3 | documented exclusion — file/path/mixed-case identifier, not a prose abbreviation |
| P3 | M | `GitHub` | L46 | documented exclusion — file/path/mixed-case identifier, not a prose abbreviation |
| P3 | M | `PRs` | L35 | documented exclusion — file/path/mixed-case identifier, not a prose abbreviation |
| P3 | U | `HUMAN` | L5 | defined at first use — acronym expanded at or before first use |
| P3 | U | `PR` | L5 | defined at first use — acronym expanded at or before first use |
| P3 | U | `CI` | L6 | defined at first use — acronym expanded at or before first use |
| P3 | U | `NNN` | L7 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P3 | U | `DEFAULT` | L62 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P3 | U | `ID` | L63 | named gap — acronym/coded identifier used before any expansion on this page |
| P3 | U | `ALREADY` | L72 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P3 | U | `EXACT` | L78 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P3 | U | `PHRASE` | L78 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P3 | U | `OPEN` | L85 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P3 | U | `NOT` | L128 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P3 | L | `repo` | L4 | documented exclusion — lowercase technical/format token, not a prose abbreviation |
| P3 | L | `pr` | L28 | defined at first use — expanded on or before first use |
| P4 | B | `compliance-control-foundation` | L3 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P4 | B | `iso-27001-isms-architect` | L3 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P4 | B | `iso-42001-aims-architect` | L3 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P4 | B | `multi-framework-crosswalk` | L3 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P4 | B | `soc2-trust-criteria-mapper` | L45 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P4 | B | `threat-modeler` | L53 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P4 | B | `ai-threat-modeler` | L54 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P4 | B | `human-approval-boundary` | L113 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P4 | B | `compliance-evidence-collector` | L115 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P4 | B | `compliance-gap-auditor` | L116 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P4 | B | `evals/evals.json` | L213 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P4 | B | `evals/trigger-evals.json` | L214 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P4 | B | `<org>` | L122 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P4 | B | `<ISO/IEC 27001:2022 \| ISO/IEC 42001:2023 \| both>` | L122 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P4 | B | `<n>` | L123 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P4 | B | `<named human>` | L123 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P4 | B | `<e.g. annual + on major change>` | L123 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P4 | B | `<incomplete while any applicability decision is pending>` | L124 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P4 | B | `<Annex A id — title as published>` | L127 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P4 | B | `<risk-treatment trace (risk id) \| obligation \| concrete exclusion rationale \| missing decision and evidence>` | L129 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P4 | B | `<mechanism from compliance-control-foundation>` | L130 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P4 | B | `<residue>` | L130 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P4 | B | `<owner, date>` | L130 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P4 | B | `<→ compliance-evidence-collector \| missing decision/evidence (pending only)>` | L131 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P4 | B | `<count + one-line rationale each>` | L132 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P4 | B | `<controls awaiting risk-treatment decisions>` | L133 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P4 | B | `<plain definitions, options and reasons, costs or unknowns, benefits and drawbacks, recommended fit and why, one format or risk-owner question>` | L134 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P4 | B | `→` | L114 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P4 | M | `6.1.2/6.1.4` | L55 | documented exclusion — file/path/mixed-case identifier, not a prose abbreviation |
| P4 | M | `assets/soa-template.md` | L88 | documented exclusion — file/path/mixed-case identifier, not a prose abbreviation |
| P4 | M | `SoA` | L3 | documented exclusion — file/path/mixed-case identifier, not a prose abbreviation |
| P4 | M | `SoAs` | L67 | documented exclusion — file/path/mixed-case identifier, not a prose abbreviation |
| P4 | M | `IDs` | L50 | documented exclusion — file/path/mixed-case identifier, not a prose abbreviation |
| P4 | U | `ISO` | L3 | named gap — acronym/coded identifier used before any expansion on this page |
| P4 | U | `BOTH` | L3 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P4 | U | `SOC` | L3 | named gap — acronym/coded identifier used before any expansion on this page |
| P4 | U | `NOT` | L3 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P4 | U | `IEC` | L9 | defined at first use — acronym expanded at or before first use |
| P4 | U | `AICPA` | L11 | named gap — acronym/coded identifier used before any expansion on this page |
| P4 | U | `ISMS` | L11 | defined at first use — acronym expanded at or before first use |
| P4 | U | `AIMS` | L12 | defined at first use — acronym expanded at or before first use |
| P4 | U | `AI` | L12 | named gap — acronym/coded identifier used before any expansion on this page |
| P4 | U | `STATEMENT` | L122 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P4 | U | `OF` | L122 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P4 | U | `APPLICABILITY` | L122 | defined at first use — acronym expanded at or before first use |
| P4 | U | `YOUR` | L183 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P4 | L | `id` | L127 | defined at first use — expanded on or before first use |
| P4 | L | `json` | L213 | documented exclusion — lowercase technical/format token, not a prose abbreviation |
| P5 | B | `pending risk-owner decision` | L26 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P5 | B | `Treats R-<id> <risk name> per treatment decision <ref>.` | L37 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P5 | B | `Required by <law/contract/policy ref> independent of risk appetite.` | L40 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P5 | B | `<scope statement reference>` | L10 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P5 | B | `<n>` | L12 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P5 | B | `<YYYY-MM-DD>` | L12 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P5 | B | `<name>` | L13 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P5 | B | `<name, role>` | L14 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P5 | B | `<e.g. annual + on major change/risk-assessment update>` | L15 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P5 | B | `<register id/version — the 6.1.3 trace source>` | L16 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P5 | B | `<id>` | L26 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P5 | B | `<quoted title>` | L26 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P5 | B | `<see patterns below>` | L26 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P5 | B | `<residue>` | L26 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P5 | B | `<owner,date>` | L26 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P5 | B | `<compliance-control-foundation CC-id or named artifact, or risk owner if pending>` | L26 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P5 | B | `<→ compliance-evidence-collector, or missing decision/evidence if pending>` | L26 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P5 | B | `<risk name>` | L37 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P5 | B | `<ref>` | L37 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P5 | B | `<law/contract/policy ref>` | L40 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P5 | B | `→` | L26 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P5 | U | `ISMS-AIMS` | L10 | named gap — acronym/coded identifier used before any expansion on this page |
| P5 | F | `YYYY-MM-DD` | L12 | documented exclusion — self-describing lifecycle/format code |
| P5 | U | `LICENSED` | L3 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P5 | U | `ISO` | L4 | named gap — acronym/coded identifier used before any expansion on this page |
| P5 | U | `IEC` | L4 | named gap — acronym/coded identifier used before any expansion on this page |
| P5 | L | `id` | L16 | documented exclusion — lowercase technical/format token, not a prose abbreviation |
| P6 | B | `supply-chain-security-reviewer` | L3 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P6 | B | `security-pr-reviewer` | L3 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P6 | B | `secure-migration-reviewer` | L3 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P6 | B | `threat-modeler` | L41 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P6 | B | `sast-orchestration-designer` | L3 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P6 | B | `security-scan-orchestrator` | L3 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P6 | B | `appsec-implementer` | L91 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P6 | B | `human-approval-boundary` | L142 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P6 | B | `evals/evals.json` | L182 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P6 | B | `evals/trigger-evals.json` | L183 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P6 | B | `code-reviewer` | L185 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P6 | B | `<tool + scope>` | L100 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P6 | B | `<N raw findings>` | L103 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P6 | B | `<M after dedup>` | L103 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P6 | B | `<n>` | L104 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P6 | B | `<rule id>` | L106 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P6 | B | `<file:line>` | L106 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P6 | B | `<what the code actually does on the flagged path>` | L107 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P6 | B | `<who reaches it, how, what they get; tenant blast>` | L108 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P6 | B | `<direction>` | L110 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P6 | B | `<rule id @ loc — why refuted (code fact)>` | L111 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P6 | B | `<rule id @ loc — written rationale, owner, date>` | L112 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P6 | B | `<yes — per-finding rationale recorded>` | L113 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P6 | B | `<findings/areas not reached + why>` | L114 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P6 | B | `→` | L51 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P6 | F | `HIGH` | L83 | documented exclusion — self-describing lifecycle/status/format code, not a prose abbreviation |
| P6 | F | `LOW` | L106 | defined at first use — status/format code explained at first use |
| P6 | F | `CRITICAL` | L83 | documented exclusion — self-describing lifecycle/status/format code, not a prose abbreviation |
| P6 | F | `MEDIUM` | L106 | defined at first use — status/format code explained at first use |
| P6 | M | `references/triage-rubric.md` | L78 | documented exclusion — file/path/mixed-case identifier, not a prose abbreviation |
| P6 | M | `../../../docs/prompts/claude-skills-master-generation-prompts-v4.md` | L134 | documented exclusion — file/path/mixed-case identifier, not a prose abbreviation |
| P6 | M | `CodeQL` | L3 | documented exclusion — file/path/mixed-case identifier, not a prose abbreviation |
| P6 | M | `SaaS` | L58 | named gap — acronym/coded identifier used before any expansion on this page |
| P6 | M | `CVEs` | L33 | documented exclusion — file/path/mixed-case identifier, not a prose abbreviation |
| P6 | U | `SAST` | L3 | named gap — acronym/coded identifier used before any expansion on this page |
| P6 | U | `SARIF` | L3 | named gap — acronym/coded identifier used before any expansion on this page |
| P6 | U | `NOT` | L3 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P6 | U | `CI` | L3 | named gap — acronym/coded identifier used before any expansion on this page |
| P6 | U | `CVE` | L22 | defined at first use — acronym expanded at or before first use |
| P6 | U | `TP` | L22 | named gap — acronym/coded identifier used before any expansion on this page |
| P6 | U | `FP` | L22 | named gap — acronym/coded identifier used before any expansion on this page |
| P6 | U | `PII` | L58 | named gap — acronym/coded identifier used before any expansion on this page |
| P6 | U | `WHY` | L73 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P6 | U | `WITH` | L87 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P6 | U | `STATIC` | L100 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P6 | U | `ANALYSIS` | L100 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P6 | U | `TRIAGE` | L100 | defined at first use — acronym expanded at or before first use |
| P6 | U | `RULE` | L147 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P6 | U | `ORM` | L151 | named gap — acronym/coded identifier used before any expansion on this page |
| P6 | U | `SQL` | L152 | named gap — acronym/coded identifier used before any expansion on this page |
| P6 | U | `XSS` | L152 | named gap — acronym/coded identifier used before any expansion on this page |
| P6 | U | `MISSED` | L159 | documented exclusion — ordinary all-caps emphasis word, not an abbreviation |
| P6 | L | `ids` | L50 | documented exclusion — lowercase technical/format token, not a prose abbreviation |
| P6 | L | `auth` | L57 | documented exclusion — lowercase technical/format token, not a prose abbreviation |
| P6 | L | `id` | L87 | documented exclusion — lowercase technical/format token, not a prose abbreviation |
| P6 | L | `dedup` | L103 | documented exclusion — lowercase technical/format token, not a prose abbreviation |
| P6 | L | `json` | L182 | documented exclusion — lowercase technical/format token, not a prose abbreviation |
| P7 | B | `static-analysis-reviewer` | L9 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P7 | B | `escapeHtml()` | L22 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P7 | B | `security-pr-reviewer` | L81 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P7 | B | `threat-modeler` | L81 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P7 | B | `appsec-implementer` | L82 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P7 | B | `<rule id>` | L68 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P7 | B | `<file:line>` | L68 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P7 | B | `<specific, auditable>` | L70 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P7 | B | `<who>` | L71 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P7 | B | `<YYYY-MM-DD>` | L71 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P7 | B | `<human-approval-boundary ref, if accepted risk>` | L71 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P7 | B | `→` | L44 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P7 | F | `YYYY-MM-DD` | L71 | documented exclusion — self-describing lifecycle/format code |
| P7 | F | `HIGH` | L41 | documented exclusion — self-describing lifecycle/status/format code, not a prose abbreviation |
| P7 | F | `CRITICAL` | L41 | documented exclusion — self-describing lifecycle/status/format code, not a prose abbreviation |
| P7 | F | `MEDIUM` | L44 | documented exclusion — self-describing lifecycle/status/format code, not a prose abbreviation |
| P7 | M | `../SKILL.md` | L3 | documented exclusion — file/path/mixed-case identifier, not a prose abbreviation |
| P7 | M | `SaaS` | L5 | documented exclusion — file/path/mixed-case identifier, not a prose abbreviation |
| P7 | U | `PII` | L5 | defined at first use — acronym expanded at or before first use |
| P7 | U | `SQL` | L6 | defined at first use — acronym expanded at or before first use |
| P7 | U | `ORM` | L6 | defined at first use — acronym expanded at or before first use |
| P7 | U | `XSS` | L7 | defined at first use — acronym expanded at or before first use |
| P7 | U | `FP` | L7 | defined at first use — acronym expanded at or before first use |
| P7 | U | `ACTUALLY` | L57 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P7 | U | `ONE` | L63 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P7 | U | `SUPPRESS` | L68 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P7 | L | `auth` | L35 | documented exclusion — lowercase technical/format token, not a prose abbreviation |
| P7 | L | `id` | L62 | documented exclusion — lowercase technical/format token, not a prose abbreviation |
| P8 | B | `api-event-architect` | L3 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P8 | B | `operational-vs-analytical-splitter` | L3 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P8 | B | `audit-log-architect` | L3 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P8 | B | `schema-evolution-planner` | L52 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P8 | B | `background-job-orchestration-architect` | L55 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P8 | B | `realtime-subscription-architect` | L57 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P8 | B | `event-schema-architect` | L3 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P8 | B | `multi-tenant-data-architect` | L74 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P8 | B | `observability-operator` | L142 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P8 | B | `data-migration-runbook-author` | L217 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P8 | B | `evals/evals.json` | L248 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P8 | B | `evals/trigger-evals.json` | L250 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P8 | B | `<system/domain>` | L159 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P8 | B | `<N producer→consumer flows, classified>` | L160 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P8 | B | `<flow>` | L162 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P8 | B | `<stream\|queue>` | L162 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P8 | B | `<key>` | L162 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P8 | B | `<per-key guarantee, producer/broker/consumer assumptions and non-guarantees>` | L162 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P8 | B | `<mechanism>` | L164 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P8 | B | `<policy>` | L165 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P8 | B | `<dest, owner, drain SLA>` | L165 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P8 | B | `<procedure>` | L165 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P8 | B | `<time/size\|compacted>` | L166 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P8 | B | `<version, compat rule>` | L166 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P8 | B | `<counts, skew notes (tenant hot-key risk)>` | L167 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P8 | B | `<sources, mechanism, snapshot policy, drift handling>` | L168 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P8 | B | `<lag thresholds/owners; producer behavior when slow>` | L169 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P8 | B | `<what this design does NOT promise (e.g., cross-key ordering)>` | L172 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P8 | B | `<scope>` | L180 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P8 | B | `→` | L95 | documented exclusion — inline code/path/placeholder/operator, not a prose abbreviation |
| P8 | M | `references/backbone-decision-sheet.md` | L150 | documented exclusion — file/path/mixed-case identifier, not a prose abbreviation |
| P8 | M | `DLQs` | L208 | documented exclusion — file/path/mixed-case identifier, not a prose abbreviation |
| P8 | U | `INTERNAL` | L3 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P8 | U | `CDC` | L3 | named gap — acronym/coded identifier used before any expansion on this page |
| P8 | U | `PIPELINE` | L3 | named gap — acronym/coded identifier used before any expansion on this page |
| P8 | U | `NOT` | L3 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P8 | U | `DLQ` | L8 | named gap — acronym/coded identifier used before any expansion on this page |
| P8 | U | `SLA` | L8 | named gap — acronym/coded identifier used before any expansion on this page |
| P8 | U | `DDL` | L9 | named gap — acronym/coded identifier used before any expansion on this page |
| P8 | U | `DESIGN` | L17 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P8 | U | `BETWEEN` | L22 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P8 | U | `PUBLIC` | L39 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P8 | U | `WHETHER` | L46 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P8 | U | `DATABASE` | L50 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P8 | U | `EXECUTION` | L53 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P8 | U | `CLIENT` | L56 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P8 | U | `IDEMPOTENT` | L113 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P8 | U | `REPLAY` | L121 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P8 | U | `STREAMING` | L159 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P8 | U | `BACKBONE` | L159 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P8 | U | `INSIDE` | L206 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P8 | U | `THE` | L251 | documented exclusion — ordinary all-caps emphasis word, heading or proper name, not an abbreviation |
| P8 | L | `id` | L113 | documented exclusion — lowercase technical/format token, not a prose abbreviation |
| P8 | L | `dedup` | L113 | documented exclusion — lowercase technical/format token, not a prose abbreviation |
| P8 | L | `config` | L240 | documented exclusion — lowercase technical/format token, not a prose abbreviation |
| P8 | L | `repo` | L241 | documented exclusion — lowercase technical/format token, not a prose abbreviation |
| P8 | L | `json` | L248 | documented exclusion — lowercase technical/format token, not a prose abbreviation |

**Zero-duplicate proof.** Final table rows = **308**; unique (page, first-use line, normalized token) keys = **308**; duplicates = **0**; extra rows = **0**. **Independent cell-count proof:** every row above parses as exactly five pipe-delimited cells after escaping literal pipes (escaped tokens/reasons), **308/308 rows = five cells**, zero malformed rows; the count table below was derived from this final table.

**Counts recomputed from the FINAL table above.**

| Page | Rows | U | M | L | B | F | Defined | Named gaps | Exclusions |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P1 | 12 | 3 | 1 | 0 | 8 | 0 | 0 | 0 | 12 |
| P2 | 44 | 15 | 3 | 3 | 20 | 3 | 2 | 2 | 40 |
| P3 | 35 | 11 | 3 | 2 | 18 | 1 | 4 | 1 | 30 |
| P4 | 48 | 13 | 5 | 2 | 28 | 0 | 5 | 4 | 39 |
| P5 | 27 | 4 | 0 | 1 | 21 | 1 | 0 | 3 | 24 |
| P6 | 57 | 18 | 5 | 5 | 25 | 4 | 4 | 10 | 43 |
| P7 | 28 | 8 | 2 | 2 | 12 | 4 | 5 | 0 | 23 |
| P8 | 57 | 20 | 2 | 5 | 30 | 0 | 0 | 5 | 52 |
| **Total** | **308** | **92** | **21** | **20** | **162** | **13** | **20** | **25** | **263** |

**Reconciliation and proof.** Row sum **308** equals class sum **308** and disposition sum **308**; page sums equal the row count. The named-gap rows below are exactly the named gaps cited in section 5; every row resolves to pinned page text at its stated first occurrence; zero duplicates and zero fabricated rows.

**Named-gap list aligned with section 5:** P1 none; P2 L9 PR, L10 CI; P3 L63 ID; P4 L3 ISO, L3 SOC, L11 AICPA, L12 AI; P5 L10 ISMS-AIMS, L4 ISO, L4 IEC; P6 L58 SaaS, L3 SAST, L3 SARIF, L3 CI, L22 TP, L22 FP, L58 PII, L151 ORM, L152 SQL, L152 XSS; P7 none; P8 L3 CDC, L3 PIPELINE, L8 DLQ, L8 SLA, L9 DDL;

## 7. Dispositions, keeper exclusion and continuation

**Disposition tally: 20 defined at first use / 25 named gaps / 263 documented exclusions = 308 rows.** **Disposition tally: 0 FULL / 8 PARTIAL / 0 UNRUN.** All eight pages were read whole; no page is UNRUN. No page is FULL because canonical B6 is unverified for every page; named B2 gaps independently force PARTIAL where present. **No keeper/acceptance row:** this record creates no acceptance rows; a later keeper decides.

**Continuation.** Lane A is complete 0-143; merged lane-B rows **144-199 + 200-207 + 208-215 + 216-223 + 224-231 + 232-239 + 240-247 + 248-255 + 256-263 + 264-271**; no open reservations; this record covers **272-279**; next unread page is **280**.

## 8. Provenance, page authorship, zero drift and reader independence

**Base:** 4b99f69f (merge commit of #841, 41st session record merge). **Plan:** 6249596669 + B ACCEPT 6249612964. **Reader:** sd-c-read-b21-c1 read all eight pages whole at the pinned blob; no display elision. **Page authors are not this reader** (git metadata only; not B6 proof). **Witness rows:** section 3 is the per-page witness (index, path, pinned blob, measured bytes/LF); each blob resolves at 2db1ffb7 and is identical at base 4b99f69f (zero drift). **Author metadata only — NOT B6 evidence.**

## 9. Stage C declaration, AC statuses and self-state consistency

| AC | Status | Evidence |
| --- | --- | --- |
| AC1 one-path | MET in this record | exactly one added record path; no other tracked path; **three DCO-signed model commits** (initial 0107e5bc + repair cc46de87 + this triage repair commit) |
| AC2 pages | MET in this record | eight pages 272-279 by blob; totals 70,286/1,234; zero drift; no keeper |
| AC3 inventory | MET in this record | one contiguous **308-row table; 308 unique keys**; zero duplicates/extra; five-cell proof; counts recomputed; no fabricated rows |
| AC4 dispositions | MET in this record | strict FULL bar; 0 FULL/8 PARTIAL/0 UNRUN; B6 unverified; named gaps aligned |
| AC5 record/body/PROC | MET in this record | record bytes/LF/sha/blob measured in handoff; body binds facts; PROC-04 published == live-body recompute; body checker 0 |
| AC6 Codex loop | **NOT CLAIMED — head-bound unavailable; never a pass** | prior-head Codex findings triaged; replies/resolutions recorded after this repair; current-head Codex review unavailable; D/G decides AC6; no pass claimed |
| AC7 provenance | MET in this record | plan/B lineage, base and reservations, merge attribution, zero drift, absent path |
| AC8 stages | MET for C | C only acts here; D/E/F/G separate; no merge |

**Self-state consistency.** Section 2's scheduling facts, section 6's counts and this table agree: base 4b99f69f; merged lane-B 144-271; no open reservations; this block 272-279; next 280; batch 21. **Merge attribution:** 4b99f69f = #841 41st; 2c3c6ffe = #840 40th; 38212595 = #839 39th; f325daac = #838 38th; 7cea211e = #837 37th; 6f584c9d = #833 36th; a06360d4 = #835 35th; a141c64f = #836 34th; e7acaca4 = #834 33rd; 84a5295d = #831 32nd; 655e40ea = #828 31st; 883bf690 = #832 30th. No unresolved head placeholder; **actual commit count = three DCO-signed model commits** (initial 0107e5bc + repair cc46de87 + this triage repair commit).


## 10. My Stage C skills rows, Row sources and six-field lines

| Skill | Stage / agent | How applied | Result / evidence |
| --- | --- | --- | --- |
| acceptance-criteria-reviewer @ c6e5d5649bf8 | C batch-21 / sd-c-read-b21-c1 (true identity sd-e-802-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Read all eight pinned pages; applied AC1-AC8 and canonical B1-B6, B4 per page, B6 UNVERIFIED; built exact-once inventory. | inventory / unique-key / zero-duplicate proof; B4 per page; B6 UNVERIFIED |
| source-of-truth-reconciler @ b5fd9feda972 | C batch-21 / sd-c-read-b21-c1 (DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Re-derived pinned pending set, base 4b99f69f, merged rows 144-271, no open reservations, block 272-279; measured blobs/totals/zero drift. | 573 pending; pages 272-279 70,286 B / 1,234 LF; zero drift |
| change-classification-gate @ 08d91a834460 | C batch-21 / sd-c-read-b21-c1 (DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Classified docs-only with exactly one added record path and no other tracked change. | one A docs/evidence/documentation/readability-lane-b-batch-21-2026-10-18.md |
| skill-usage-ledger @ 6a27b5c8e690 | C batch-21 / sd-c-read-b21-c1 (DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)) | Resolved four manifest names at main 4b99f69f; authored these C rows, per-row Row sources and six-field lines. | four rows / four per-row sources / four six-field lines |

<!-- Row source: agent=sd-c-read-b21-c1 (true identity sd-e-802-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)); stage=C; round=1; row=1; target=lane-B batch-21 plan 6249596669 / B ACCEPT 6249612964 / base 4b99f69f / block 272-279; source=_A/evidence/read-b21-c1/C-rows.txt row 1; binding=sha256 a6682cd910fbfa5f664e2e1ab0be1c6438ce4d676016aca34e6cb9f3399eff76; limits=this per-row record binds its retained row, not human identity; this stage only. -->

<!-- Row source: agent=sd-c-read-b21-c1 (true identity sd-e-802-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)); stage=C; round=1; row=2; target=lane-B batch-21 plan 6249596669 / B ACCEPT 6249612964 / base 4b99f69f / block 272-279; source=_A/evidence/read-b21-c1/C-rows.txt row 2; binding=sha256 a3537b038b9297f6163e8dc58421ce3d3c0add64d68314520ec0bef97e2752a9; limits=this per-row record binds its retained row, not human identity; this stage only. -->

<!-- Row source: agent=sd-c-read-b21-c1 (true identity sd-e-802-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)); stage=C; round=1; row=3; target=lane-B batch-21 plan 6249596669 / B ACCEPT 6249612964 / base 4b99f69f / block 272-279; source=_A/evidence/read-b21-c1/C-rows.txt row 3; binding=sha256 f04ed86838d42515fddf8bb7e7421fb96f91ac9f6b6ffc619a5421735b9b1dcc; limits=this per-row record binds its retained row, not human identity; this stage only. -->

<!-- Row source: agent=sd-c-read-b21-c1 (true identity sd-e-802-r1; DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)); stage=C; round=1; row=4; target=lane-B batch-21 plan 6249596669 / B ACCEPT 6249612964 / base 4b99f69f / block 272-279; source=_A/evidence/read-b21-c1/C-rows.txt row 4; binding=sha256 26cb94fe6bf70dc8b0360d822bad029298f3d8e379f01449f73f16432cc4d819; limits=this per-row record binds its retained row, not human identity; this stage only. -->

~~~text
acceptance-criteria-reviewer@c6e5d5649bf8 / stage=C row=1 / reason: C owes canonical AC/inventory evidence / applied: read eight pages whole; B1-B6, B4 per page, B6 UNVERIFIED; inventory / result: AC3/AC4 evidence complete / incomplete: D/E/F/G follow / by: C, sd-c-read-b21-c1 (true identity sd-e-802-r1), DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)
source-of-truth-reconciler@b5fd9feda972 / stage=C row=2 / reason: C owes base/object truth / applied: pending 573, base 4b99f69f, merged 144-271, no reservations, block 272-279, blobs/totals / result: 70,286/1,234; zero drift / incomplete: D/E/F/G follow / by: C, sd-c-read-b21-c1 (true identity sd-e-802-r1), DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)
change-classification-gate@08d91a834460 / stage=C row=3 / reason: C owes docs-only one-path proof / applied: one added record path, no other tracked change / result: one A record path / incomplete: D/E/F/G follow / by: C, sd-c-read-b21-c1 (true identity sd-e-802-r1), DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)
skill-usage-ledger@6a27b5c8e690 / stage=C row=4 / reason: C owes self-authored provenance / applied: four names at main 4b99f69f; rows/per-row sources/six fields; binding sha256 a6682cd910fbfa5f664e2e1ab0be1c6438ce4d676016aca34e6cb9f3399eff76 / result: four rows/four sources/four six-field lines / incomplete: publisher/body insertion / by: C, sd-c-read-b21-c1 (true identity sd-e-802-r1), DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness)
~~~

## 11. Limits and unverifiable items

Canonical B6 is unverified for all eight pages; no page is FULL and no keeper is created. B4 is assessed for instructional/reference content only; no synthetic test, passing check or approved design is described as deployed or measured. Hosted CI/Codex states are observed in the handoff. **Signed with both names: true identity sd-e-802-r1; stage role sd-c-read-b21-c1.** **Written by: DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness).**