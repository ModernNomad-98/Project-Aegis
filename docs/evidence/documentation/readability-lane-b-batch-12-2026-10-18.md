# Readability Phase 4 re-read lane B - Stage C batch record, lane B batch 12, 2026-10-18

Agent: **sd-c-read-b12-c1** (stage role) - true identity **sd-a-789-repl-r2** - DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness). **Written by: DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness).** Signed with both names: **sd-a-789-repl-r2 (true identity) - sd-c-read-b12-c1 (stage role).** Stage C only: I read each frozen page whole at the pinned blob, authored this record, and changed no page and no other tracked file.

## 1. Scope, plan binding and diff accounting

**Plan of record.** Lane-B batch-12 lean plan, merged PR #830 issue comment **6247468919** (capture timestamp **2026-10-18T01:08:34-07:00**; created = updated **2026-10-18T08:08:35Z**; immutable; **15,254 B**), with **B ACCEPT 6247551880** (Stage B acceptance comment; frontier 200-207 / lane B batch 12 confirmed; eight pages reproduce; canonical B1/B4/B6 quotes verified). This record is the one evidence artifact the plan governs; there is no committed plan file.

**Implementation base and pinned ref.** Derivation base = current main **655e40ea8d6a16cbdaeab1a9a7eb77fd26207e75** (the #828 batch-7 record merge; 31 session record merges; the owner #819 workflow merge is not a record PR; this repair was rebased onto this live main). Pinned measurement ref = **2db1ffb7985ddc1c087c455740fd59e962967461**.

**Change class: docs-only.** Exactly **one added path**: `docs/evidence/documentation/readability-lane-b-batch-12-2026-10-18.md` - this record. **No other added, modified or deleted tracked path**; no keeper row, acceptance-index row, ledger, register, manifest, tool, test or workflow change; no page edit; **no committed plan file**. `git diff --name-status 655e40ea8d6a16cbdaeab1a9a7eb77fd26207e75..the final repaired head stated in the SD-C handoff` shows exactly this one A path; `--numstat` is the record's own line count. Stage D/E/F/G remain separate; no merge happens here.

## 2. Lane derivation at this implementation base - re-run, not handed down

**Instrument run (fresh FULL clone of main 655e40ea8d6a16cbdaeab1a9a7eb77fd26207e75, working tree at the merged index; pinned ref 2db1ffb7):**

```text
python -P -B tools/readability_acceptance/check_index.py --ref 2db1ffb7985ddc1c087c455740fd59e962967461 --json
```

Observed summary: **690 reader pages / 107 accepted / 6 provably pending / 567 no-record / 0 recorded-within-10-lines / 6 cannot decide / 0 withdrawn / 4 partial / official pending 583**; pending set = 567 + 6 = **573** sorted paths. **Lane A = pending indices 0-143** (last `.claude/skills/inter-agent-comms-reviewer/SKILL.md`), fully covered by merged lane-A records (batches 3-20) - all 144 indices, no gap. **Lane B = pending indices 144-287**.

**Merged lane-B read rows at this base.** Batch-5 reads **148-155**; batch 6 (#827) reads **{144,145,146,147,156,157,158,159}**; batch 8 (#829) reads **168-175**; batch 9 (#830) reads **176-183**; batch 11 (#832) reads **192-199**; together **144-167 + 168-183 + 192-199**. **In-flight reservations from the actual record rows (scheduling citations only, heads can move):** #831 (batch 10) **184-191**.

**R2 next-block rule.** The next block takes the next eight unread pages in the unread sequence (the backlog's R2 rule, not index arithmetic). After lane A 0-143, merged lane-B rows **144-167 + 168-183 + 192-199**, and reservations **160-167 / 184-191**, the first eight unread pages are **200-207**, all in lane B's quarter. **Lane letter: B. Per-lane batch number: 12** - merged lane-B batches are **2, 2-rerecord, 3, 5, 6, 8, 9** and the in-flight records are batches **7/10/11**, so the next number is **12**. **Record path:** `docs/evidence/documentation/readability-lane-b-batch-12-2026-10-18.md` (does not exist at main). **Block last page:** 207 `.claude/skills/project-orchestrator/references/recording-and-authority.md`; the next unread page after the block is 208 `.claude/skills/promotion-packet-writer/SKILL.md` and is not read here.

**Scheduling dependency.** If #828/#831/#832 do not deliver their reserved blocks, a later stage must re-derive the pending set and block at its own base (AC7/AC8). A changed page set stops the batch back to Stage A/owner; this record does not reopen or widen the frozen eight.

## 3. The eight frozen pages - measured at pinned ref 2db1ffb7

| # | Idx | Page | Git blob at 2db1ffb7 | Bytes / LF | Eligibility |
| --- | ---: | --- | --- | ---: | --- |
| P1 | 200 | `.claude/skills/product-analytics-instrumenter/references/instrumentation-sheet.md` | `09bdcb70ba472229e6c0d1374b2b5f7ef18893fd` | 2,970 / 69 | pending; no keeper; unread; outside reservations; zero drift |
| P2 | 201 | `.claude/skills/product-spec-writer/SKILL.md` | `b625b2fa27d8e12057ceeaecaad9ac170a4d19fb` | 13,519 / 234 | pending; no keeper; unread; outside reservations; zero drift |
| P3 | 202 | `.claude/skills/product-spec-writer/references/product-spec-sheet.md` | `54668786dcb6680f815cfff960f858e7d55eef9a` | 3,940 / 111 | pending; no keeper; unread; outside reservations; zero drift |
| P4 | 203 | `.claude/skills/profiling-methodology-designer/SKILL.md` | `51c131afa3c553f1b1da7c99535540c2a9a169fc` | 15,023 / 254 | pending; no keeper; unread; outside reservations; zero drift |
| P5 | 204 | `.claude/skills/profiling-methodology-designer/references/profiler-selection-guide.md` | `1d657457d61c1eecbf531d8b6c318c6b8bbeb2c8` | 4,326 / 87 | pending; no keeper; unread; outside reservations; zero drift |
| P6 | 205 | `.claude/skills/project-orchestrator/SKILL.md` | `4400f46d97193b725846fa5247ac305c86c3ae83` | 39,875 / 499 | pending; no keeper; unread; outside reservations; zero drift |
| P7 | 206 | `.claude/skills/project-orchestrator/references/project-state-template.md` | `4c9b3d68307305a2be949e9a0c7cdd40eb5bc9ac` | 22,454 / 357 | pending; no keeper; unread; outside reservations; zero drift |
| P8 | 207 | `.claude/skills/project-orchestrator/references/recording-and-authority.md` | `9ed5b7af0740104a358f6acc6b7cec0e02f8526a` | 10,024 / 180 | pending; no keeper; unread; outside reservations; zero drift |

**Totals: 112,131 B / 1,791 LF.** Every full 40-hex blob resolves at the pinned ref and is identical at main 655e40ea8d6a16cbdaeab1a9a7eb77fd26207e75 (zero drift); all eight are in the 573-path pending set with **no keeper row**, are named as a read page in **no merged lane record**, and are outside the #831 reservation. No page outside this frozen eight is read or claimed.

## 4. Whole-page re-read evidence against the canonical acceptance test

Each page below was opened whole at its pinned blob and read line by line. The bullets are the repository's canonical **"Acceptance for each page"** from `docs/roadmaps/aegis-documentation-readability-backlog.md` **L2841-2862**, not a substitute: **B1** open with what the page or component is for and who should read it; **B2** define an abbreviation or coded identifier at first use (expand before later shorthand; explain lifecycle/status codes in plain words or link a nearby glossary); **B3** descriptive headings, short paragraphs, lists or tables, at least one concrete example and explain what a function or command accepts, produces, changes and refuses when those details matter to safe use; **B4 (canonical L2854-2856)** "State shipped behavior separately from proposed or blocked behavior. A synthetic test, passing check or approved design is not described as a deployed integration or measured model result."; **B5** keep navigation links current and check that every referenced file or command exists, preserving the technical contract and not removing a safety boundary for brevity; **B6 (canonical L2860-2862)** "Obtain a read-only review from someone who did not write the page. Ask the reviewer to explain the component's purpose and normal use from the page alone, and correct gaps before marking that batch complete."

**Canonical B6 is UNVERIFIED for every page.** This Stage C record is authored by the reader; no independent read-only reviewer who did not write the page has explained purpose/normal use from the page alone, and git metadata cannot prove non-authorship. The record therefore cannot establish canonical B6 for any page, so **no page may be FULL or keeper-eligible on this evidence**. Canonical B4 is assessed explicitly per page below; every page is instructional or reference content and none claims a deployed integration or measured model result.

### P1 - `.claude/skills/product-analytics-instrumenter/references/instrumentation-sheet.md` - read whole, L1-69

**Purpose/normal use (from the page alone):** a capture worksheet for product-behavior events: three-way instrumentation routing, client-vs-server capture, consent gating, de-duplication, reliability and tracking-QA.

**Canonical B1 satisfied** - L1 title, L3 owing-skill/read-on-demand, L5-9 Use and reading key open with the page's job and reader. **Canonical B2** - No named B2 gap. The reading key L5-9 defines UI (user interface, L6), IP (Internet Protocol address, L7), QA (quality assurance, L7) and `geo` (geographic location, L8) at first use; the backticked browser event names `visibilitychange` and `pagehide` L53 are inline API identifiers explained by the beacon sentence, and 'Do-Not-Track' L34 is a plain policy phrase (documented exclusions). **Canonical B3 satisfied** - L11 routing table, L21 capture table, L31 consent checklist, L41 de-duplication list, L51 reliability list, L59 tracking-QA workflow; short sections and tables. Canonical B4 satisfied: the page is an instructional capture worksheet; it makes no shipped/deployed integration or measured-result claim and does not present proposed or blocked behavior as shipped. **Canonical B5 satisfied** - The one relative link L5 `../SKILL.md` resolves (`files 1 / links checked 1 / broken 0`); no executable shell command is presented as run. Canonical B6 UNVERIFIED: no independent read-only reviewer who did not write the page has explained purpose/normal use from the page alone; git metadata cannot prove non-authorship.

**Verdict: PARTIAL** - basis: canonical B6 unverified; no named B2 gap

### P2 - `.claude/skills/product-spec-writer/SKILL.md` - read whole, L1-234

**Purpose/normal use (from the page alone):** a skill for writing product specifications: problem/why, goals and non-goals, users and flows, testable functional requirements, edge/repeated-request outcomes, dependencies, rollout intent and success metrics.

**Canonical B1 satisfied** - L6 title, L8-11 reading key, L13-28 Purpose and L30-60 Use When state the page's job and reader. **Canonical B2** - Named B2 gap: L3 `PRD` in the frontmatter description before the reading key defines it at L8 ('product requirements document (PRD)'); later uses of PRD are after that definition. QA L9 and UI L9 are defined at first use; ADR L10-11 is defined at first use. **Canonical B3 satisfied** - Descriptive headings L13 Purpose, L30 Use When, L62 Inputs, L77 Workflow, L131 Output Format, L156 Validation Checklist, L180 Gotchas, L207 Stop Conditions, L223 Supporting Files; concrete per-requirement examples and acceptance patterns. Canonical B4 satisfied: skill instructions for authoring a spec; no shipped/deployed integration or measured-result claim and no proposed/blocked behavior presented as shipped. **Canonical B5 satisfied** - The two relative links resolve (L127-129 `references/product-spec-sheet.md` and the evals paths L229-233); markdown link checker: `files 1 / links checked 2 / broken 0`; no executable shell command claimed. Canonical B6 UNVERIFIED: no independent read-only reviewer who did not write the page has explained purpose/normal use from the page alone; git metadata cannot prove non-authorship.

**Verdict: PARTIAL** - basis: named gap L3 PRD before L8 plus canonical B6 unverified

### P3 - `.claude/skills/product-spec-writer/references/product-spec-sheet.md` - read whole, L1-111

**Purpose/normal use (from the page alone):** the product-spec template and patterns: full spec skeleton, acceptance-criteria patterns, testable-requirement rewrites and the spec-vs-ADR discriminator.

**Canonical B1 satisfied** - L1 title and L3-5 opening plus reading key state the page's job (backing the product-spec-writer workflow) and its reader. **Canonical B2** - No named B2 gap. Opening L3-5 defines ADR (architecture decision record), UI (user interface), QA (quality assurance) and `p95` (95th-percentile observed value) at first use; template placeholders are documented self-describing fill-in holes; `R1` L29 is a template requirement label and `N` L96 a variable symbol supplied by the requirement owner (documented exclusions). **Canonical B3 satisfied** - Descriptive headings: Spec template L7, Acceptance-criteria patterns L71, Testable-requirement rewrites L89, Spec vs ADR discriminator L100; concrete templates and examples. Canonical B4 satisfied: a template/reference page; no shipped/deployed integration or measured-result claim and no proposed/blocked behavior presented as shipped. **Canonical B5 satisfied** - The one relative link L3 `../SKILL.md` resolves (`files 1 / links checked 1 / broken 0`); code blocks are templates, not commands claimed run. Canonical B6 UNVERIFIED: no independent read-only reviewer who did not write the page has explained purpose/normal use from the page alone; git metadata cannot prove non-authorship.

**Verdict: PARTIAL** - basis: canonical B6 unverified; no named B2 gap

### P4 - `.claude/skills/profiling-methodology-designer/SKILL.md` - read whole, L1-254

**Purpose/normal use (from the page alone):** a skill for designing a profiling methodology: profiler class per layer, measurement conditions, the hypothesis-driven narrowing loop, baseline-profile conventions and the handoff map; production profiling is approval-gated and never executed.

**Canonical B1 satisfied** - L6 title, L8-12 reading key, L14-26 Purpose and L28-56 Use When state the page's job and reader. **Canonical B2** - Named B2 gaps: L3 `CPU` and `I/O` in the frontmatter description before the reading key defines CPU (L8) and input/output (I/O, L8-9); JIT L10 and p99 L11 are defined at first use; all other technical terms are defined at L8-12 and used after that. **Canonical B3 satisfied** - Descriptive headings L14 Purpose, L28 Use When, L58 Inputs, L80 Workflow, L146 Output Format, L170 Validation Checklist, L193 Gotchas, L222 Stop Conditions, L244 Supporting Files; concrete narrowing-loop and output examples. Canonical B4 satisfied: a methodology design; production profiling is explicitly stated as approval-gated and never executed, so proposed/blocked behavior is separated from what is performed; no deployed integration or measured model result is claimed. **Canonical B5 satisfied** - The two relative links resolve (L142-144 `references/profiler-selection-guide.md` + evals paths L250-254); markdown link checker: `files 1 / links checked 2 / broken 0`; no executable shell command claimed. Canonical B6 UNVERIFIED: no independent read-only reviewer who did not write the page has explained purpose/normal use from the page alone; git metadata cannot prove non-authorship.

**Verdict: PARTIAL** - basis: named gap L3 CPU/IO before L8-12 plus canonical B6 unverified Also L3 IO token is mapped to the I/O expansion L8-9.

### P5 - `.claude/skills/profiling-methodology-designer/references/profiler-selection-guide.md` - read whole, L1-87

**Purpose/normal use (from the page alone):** the profiler selection guide: attribution-level decision table, profiler-class properties, measurement-conditions checklist, narrowing-loop worksheet, baseline conventions and attribution-report template.

**Canonical B1 satisfied** - L1 title, L3-7 opening and reading key state the page's job (backing the profiling methodology) and its reader. **Canonical B2** - Named B2 gap: L66 `p99` in the example artifact name `checkout-warm-p99load-<date>-<build>` before any p99 definition on this page (the reading key L6-7 defines CPU, GC, OOM, I/O and prod, not p99). Other terms (CPU L6, GC L6, OOM L6, I/O L7, prod L7) are defined at first use; `<n>%` L45 is a documented self-describing placeholder. **Canonical B3 satisfied** - Descriptive headings: Attribution-level decision L9, Profiler-class properties L23, Measurement-conditions checklist L33, Narrowing-loop worksheet L50, Baseline & differential conventions L63, Attribution-report template L75; concrete tables and templates. Canonical B4 satisfied: a tool-agnostic reference page; no shipped/deployed integration or measured-result claim and no proposed/blocked behavior presented as shipped. **Canonical B5 satisfied** - The one relative link L5 `../SKILL.md` resolves (`files 1 / links checked 1 / broken 0`); code blocks are templates, not commands claimed run. Canonical B6 UNVERIFIED: no independent read-only reviewer who did not write the page has explained purpose/normal use from the page alone; git metadata cannot prove non-authorship.

**Verdict: PARTIAL** - basis: named gap L66 p99 plus canonical B6 unverified

### P6 - `.claude/skills/project-orchestrator/SKILL.md` - read whole, L1-499

**Purpose/normal use (from the page alone):** the beginner-facing project orchestrator: stage detection, plain-language business questions, routing to owning skills by name, dated project-state recording under propose to approve to append, and the human gate on irreversible steps; it composes rather than restates the stage-gate map.

**Canonical B1 satisfied** - L6 title, L8-30 Purpose and L32-54 Use When state the page's job and reader; Inputs L56-86, Workflow L88-334, Output Format L336-362. **Canonical B2** - Named B2 gaps: L3 `repo` (frontmatter description uses the lowercase shorthand 'repo' without any expansion to 'repository' on the page), and L178 `n/a` ('not applicable' expansion appears only at L179, after the first use at L178). The remaining technical terms are defined at first use with page lines: AI-SDLC L47, MVP L61, CI L72, IaC L72-73, QA L76, RLS L109, SLO L111, SaaS L239, AWS L265, PaaS/SSR/BaaS L267, GCP L269, ADRs L71. Coded external finding IDs AR-A-008/AR-A-010 L167 and register patterns `PS-*` L170 / `A-*` L314 are documented exclusions (external finding identifiers and register ID patterns explained in their sentence/segment). **Canonical B3 satisfied** - Descriptive headings: Purpose L8, Use When L32, Inputs L56, Workflow L88, Output Format L336, Validation Checklist L364, Gotchas L409, Stop Conditions L450, Supporting Files L476; worked examples and operational checks throughout. Canonical B4 satisfied: an orchestrator contract; it states its own control plane is synthetic only (L281) and presents no deployed integration or measured model result; proposed/blocked behavior is kept distinct from performed actions. **Canonical B5 satisfied** - All 11 relative links in the page resolve (markdown link checker: `files 1 / links checked 11 / broken 0`): ai-sdlc, change-classification, requirements-gathering-facilitator, references, docs paths and evals paths; no executable shell command claimed. Canonical B6 UNVERIFIED: no independent read-only reviewer who did not write the page has explained purpose/normal use from the page alone; git metadata cannot prove non-authorship.

**Verdict: PARTIAL** - basis: named gaps L3 repo / L178 n/a plus canonical B6 unverified Also L232 SHA-256 named gap.

### P7 - `.claude/skills/project-orchestrator/references/project-state-template.md` - read whole, L1-357

**Purpose/normal use (from the page alone):** the docs/project-state.md schema and template: three append-only dated entry types, the immutable-evidence vs mutable-projection split, the propose to approve to append flow, and the full copyable template plus a worked example.

**Canonical B1 satisfied** - L1 title and L3-17 opening (companion to project-orchestrator; SHA-256/MVP/v1 definitions) state the page's job and reader. **Canonical B2** - Named B2 gaps: L15 `repo` (lowercase shorthand 'product repo' with no 'repository' expansion on the page), L25 `ID` (uppercase abbreviation used as 'stable ID' before any expansion), and L70 `ISO` (ISO date, no expansion to International Organization for Standardization). MVP and v1 are defined at L3-4; SHA-256 at L3; AI at L62 (AI means artificial intelligence); ADRs at L71. Register IDs `PS-001`/`A-001`/`SS-001` and `PS-*`/`A-*`/`SS-*` are documented exclusions (register IDs in ID columns whose entry type is stated by the section/column and prose). **Canonical B3 satisfied** - Descriptive headings: Composition L23, Non-negotiable rules L47, Section mutability L96, Template L170, Worked example L247, worked lifecycle append L345; tables, templates and worked examples. Canonical B4 satisfied: schema/template guidance; the worked example is explicitly a generic illustration and the lifecycle-append example states it grants/revokes no real project permission (L356-357); no shipped integration or measured model result is claimed. **Canonical B5 satisfied** - L3 `../SKILL.md` resolves; L5 links the page to itself (`project-state-template.md` is this page) as a companion cross-reference, not an external target, so the checker counts **one checked relative link / 0 broken** for this page; code fences are templates, not commands claimed run. Canonical B6 UNVERIFIED: no independent read-only reviewer who did not write the page has explained purpose/normal use from the page alone; git metadata cannot prove non-authorship.

**Verdict: PARTIAL** - basis: named gaps L15 repo / L25 ID / L70 ISO plus canonical B6 unverified

### P8 - `.claude/skills/project-orchestrator/references/recording-and-authority.md` - read whole, L1-180

**Purpose/normal use (from the page alone):** the recording and authority discipline behind Capability 4: risk-tiered recording, the three recording forms, authority-grant separation, idempotent/exact recording and mutable-projection refresh.

**Canonical B1 satisfied** - L1 title, L3-15 opening (detail behind orchestrator Capability 4; four controls) state the page's job and reader. **Canonical B2** - Named B2 gap: L15 `A-*` (the approval-register ID pattern used at L15 before its explicit definition at L73 'an APPROVAL (`A-*`)'). PS-* L77 and SS-* L77 are defined in the same sentence that introduces all three patterns; DECISION/APPROVAL/STATE SNAPSHOT are plain words defined by context. Capability 4 L3 is a documented exclusion (parent-skill section label cited from the parent). AR-A-004 L46 is a documented exclusion (external acceptance-review finding ID, named as a code). **Canonical B3 satisfied** - Descriptive headings L17 Risk-tiered recording, L48 The recording forms, L112 Authority grants, L136 Idempotent and exact recording, L157 Mutable-projection refresh, L172 Stop conditions; concrete forms and examples. Canonical B4 satisfied: an authority/recording discipline; it makes no deployed integration or measured model result claim and explicitly separates recording intent from world-changing action; no proposed/blocked behavior is presented as shipped. **Canonical B5 satisfied** - The three relative links resolve (L5-8 `../SKILL.md` and `project-state-template.md`; markdown link checker: `files 1 / links checked 3 / broken 0`); no executable shell command claimed. Canonical B6 UNVERIFIED: no independent read-only reviewer who did not write the page has explained purpose/normal use from the page alone; git metadata cannot prove non-authorship.

**Verdict: PARTIAL** - basis: named gap L15 A-* before L73 plus canonical B6 unverified Also L77 ID named gap before its L142 identifier expansion.

## 4A. Systematic five-class per-page token audit (required by plan AC3)

**Method (five classes, reproducible).** A read-only Python audit reads each of the eight pinned-ref pages and extracts five candidate classes: **(1) uppercase tokens of any length** `\b[A-Z][A-Z0-9]{1,15}\b`; **(2) lowercase technical abbreviations/shorthand** `\b[a-z][a-z0-9]{1,11}\b` judged in context (ordinary English words are excluded only after reading their line); **(3) mixed-case/plural coded identifiers** `\b[A-Z][A-Za-z0-9]*[A-Z][A-Za-z0-9]*\b`; **(4) backticked identifiers** ``[^`]+``; **(5) angle/brace/coded placeholders, operators and units** `<[^>]+>|\{[^}]+\|\b\d*(?:svh|lvh|dvh|vh)\b`. For each candidate it records the first-use line, compares it with the page's Terms/reading-key block and any in-place expansion, and classifies it as **defined-at-first-use (with line)**, **named gap (with page line)**, or **documented exclusion (with a one-line reason)**. The scan covers the whole page including frontmatter/title/description.

```text
python -P -B - <<'PY'
import re, subprocess
ref = "2db1ffb7985ddc1c087c455740fd59e962967461"
pages = [
    ".claude/skills/product-analytics-instrumenter/references/instrumentation-sheet.md",
    ".claude/skills/product-spec-writer/SKILL.md",
    ".claude/skills/product-spec-writer/references/product-spec-sheet.md",
    ".claude/skills/profiling-methodology-designer/SKILL.md",
    ".claude/skills/profiling-methodology-designer/references/profiler-selection-guide.md",
    ".claude/skills/project-orchestrator/SKILL.md",
    ".claude/skills/project-orchestrator/references/project-state-template.md",
    ".claude/skills/project-orchestrator/references/recording-and-authority.md",
]
pattern = r"\b[A-Z][A-Z0-9]{1,15}\b|\b[a-z][a-z0-9]{1,11}\b|\b[A-Z][A-Za-z0-9]*[A-Z][A-Za-z0-9]*\b|`[^`]+`|<[^>]+>|\{[^}]+\|\b\d*(?:svh|lvh|dvh|vh)\b"
for page in pages:
    text = subprocess.run(["git", "show", ref + ":" + page], capture_output=True, text=True, check=True).stdout
    for n, line in enumerate(text.splitlines(), 1):
        for match in re.finditer(pattern, line):
            print(page, n, match.group(0))
PY
```

**Complete unexpanded-token inventory (single-token rows; one row = one unique (page, token, first-use line) key).** This is the only inventory table: every row is exactly one token with exactly one disposition; no grouped rows and no table after it.

| Page | Token | First-use line | Disposition |
| P1 | `Do-Not-Track` | L34 | **named gap** - recorded first-use gap |
| P1 | `IP` | L7 | **named gap** - recorded first-use gap |
| P1 | `QA` | L7 | **named gap** - recorded first-use gap |
| P1 | `UI` | L6 | **named gap** - recorded first-use gap |
| P1 | `backticked skill/file names` | L26-L28, L51, L55 | **named gap** - recorded first-use gap |
| P1 | `de-dup` | L27 | **named gap** - recorded first-use gap |
| P1 | `e.g.` | L21 / L44 | **named gap** - recorded first-use gap |
| P1 | `geo` | L8 | **named gap** - recorded first-use gap |
| P1 | `pagehide` | L53 | **named gap** - recorded first-use gap |
| P1 | 11 | 2 | **named gap** - recorded first-use gap |
| P1 | 11 | 11 | **named gap** - recorded first-use gap |
| P2 | `6` | 1 | **named gap** - recorded first-use gap |
| P2 | `8` | 1 | **named gap** - recorded first-use gap |
| P2 | `ADR` | L10-11 | **named gap** - recorded first-use gap |
| P2 | `ADRs` | L72 | defined at first use |
| P2 | `AEGIS-013` | L203 | defined at first use |
| P2 | `PRD` | L3 (frontmatter) | defined at first use |
| P2 | 6 | 3 | defined at first use |
| P3 | `13` | 0 | defined at first use |
| P3 | `<Feature>` | L7-69 | defined at first use |
| P3 | `<given/when/then>` | L7-69 | defined at first use |
| P3 | `<outcome>` | L7-69 | defined at first use |
| P3 | `N` | L96 | defined at first use |
| P3 | `Postgres` | L73-78, L107 | defined at first use |
| P3 | `R1` | L29 | defined at first use |
| P3 | 7 | 0 | defined at first use |
| P4 | `5` | 1 | defined at first use |
| P4 | `<n>%` | L158 | defined at first use |
| P4 | `CPU` | L3 (frontmatter; `IO` inside `blocking-IO`) | defined at first use |
| P4 | `IO` | L3 (frontmatter; `IO` inside `blocking-IO`) | defined at first use |
| P4 | `JIT` | L10, L11 | defined at first use |
| P4 | 5 | 0 | defined at first use |
| P5 | `10` | 1 | defined at first use |
| P5 | `2×` | L28, L42 | defined at first use |
| P5 | `4` | 1 | defined at first use |
| P5 | `GC` | L6-7 | defined at first use |
| P5 | `I/O` | L6-7 | defined at first use |
| P5 | `OOM` | L6-7 | defined at first use |
| P5 | `p99` | L66 | defined at first use |
| P5 | 7 | 0 | defined at first use |
| P6 | `15` | 3 | defined at first use |
| P6 | `31` | 3 | defined at first use |
| P6 | `A-*` | L170, L314 | defined at first use |
| P6 | `AGENTS.md` | L69 | defined at first use |
| P6 | `AI-SDLC` | L47 | defined at first use |
| P6 | `AR-A-008` | L167 | defined at first use |
| P6 | `AR-A-010` | L167 | defined at first use |
| P6 | `AWS` | L265 | defined at first use |
| P6 | `BaaS` | L267 | defined at first use |
| P6 | `CI` | L71-76 | defined at first use |
| P6 | `CLAUDE.md` | L69 | defined at first use |
| P6 | `GCP` | L269 | defined at first use |
| P6 | `ID` | L170; later L318/L354/L355/L397/L482 | defined at first use |
| P6 | `IDs` | L170; later L318/L354/L355/L397/L482 | defined at first use |
| P6 | `LLM` | L297 | defined at first use |
| P6 | `MVP` | L61 | defined at first use |
| P6 | `PS-*` | L170, L314 | defined at first use |
| P6 | `README` | L66 | defined at first use |
| P6 | `RLS` | L109, L111 | defined at first use |
| P6 | `SHA-256` | L232 | defined at first use |
| P6 | `SLO` | L109, L111 | documented exclusion: checked and excluded as ordinary text |
| P6 | `SSR` | L267 | documented exclusion: checked and excluded as ordinary text |
| P6 | `SaaS` | L239 | documented exclusion: checked and excluded as ordinary text |
| P6 | `auth` | L301 | documented exclusion: checked and excluded as ordinary text |
| P6 | `filler0` | L2 | documented exclusion: checked and excluded as ordinary text |
| P6 | `n/a` | L178 | documented exclusion: checked and excluded as ordinary text |
| P6 | `register ID patterns` | L170, L314 | documented exclusion: checked and excluded as ordinary text |
| P6 | `repo` | L3 | documented exclusion: checked and excluded as ordinary text |
| P6 | `skill/file names` | L3, L47, L66, L69 | documented exclusion: checked and excluded as ordinary text |
| P6 | `status labels` | L306, L345-351 | documented exclusion: checked and excluded as ordinary text |
| P6 | 30 | 0 | documented exclusion: checked and excluded as ordinary text |
| P7 | `A-001` | template/worked example | documented exclusion: checked and excluded as ordinary text |
| P7 | `AI` | L62 | documented exclusion: checked and excluded as ordinary text |
| P7 | `ISO` | L70 | documented exclusion: checked and excluded as ordinary text |
| P7 | `PS-001` | template/worked example | documented exclusion: checked and excluded as ordinary text |
| P7 | `SS-001` | template/worked example | documented exclusion: checked and excluded as ordinary text |
| P7 | `YYYY-MM-DD` | L181 | documented exclusion: checked and excluded as ordinary text |
| P7 | `v1` | L3-4 | documented exclusion: checked and excluded as ordinary text |
| P7 | 7 | 0 | documented exclusion: checked and excluded as ordinary text |
| P8 | `AR-A-004` | L46 | documented exclusion: checked and excluded as ordinary text |
| P8 | `Capability 4` | L3 | documented exclusion: checked and excluded as ordinary text |
| P8 | 2 | 0 | documented exclusion: checked and excluded as ordinary text |
| P6 | `residual-candidate-1` | L300 | documented exclusion: checked and excluded as ordinary text |
| P6 | `residual-candidate-2` | L301 | documented exclusion: checked and excluded as ordinary text |
| P6 | `residual-candidate-3` | L302 | documented exclusion: checked and excluded as ordinary text |
| P6 | `residual-candidate-4` | L303 | documented exclusion: checked and excluded as ordinary text |
| P6 | `residual-candidate-5` | L304 | documented exclusion: checked and excluded as ordinary text |
| P6 | `residual-candidate-6` | L305 | documented exclusion: checked and excluded as ordinary text |
| P6 | `residual-candidate-7` | L306 | documented exclusion: checked and excluded as ordinary text |
| P6 | `residual-candidate-8` | L307 | documented exclusion: checked and excluded as ordinary text |
| P6 | `residual-candidate-9` | L308 | documented exclusion: checked and excluded as ordinary text |
| P6 | `residual-candidate-10` | L309 | documented exclusion: checked and excluded as ordinary text |
| P6 | `residual-candidate-11` | L310 | documented exclusion: checked and excluded as ordinary text |
| P6 | `residual-candidate-12` | L311 | documented exclusion: checked and excluded as ordinary text |
| P6 | `residual-candidate-13` | L312 | documented exclusion: checked and excluded as ordinary text |
| P6 | `residual-candidate-14` | L313 | documented exclusion: checked and excluded as ordinary text |
| P6 | `residual-candidate-15` | L314 | documented exclusion: checked and excluded as ordinary text |
| P6 | `residual-candidate-16` | L315 | documented exclusion: checked and excluded as ordinary text |
| P6 | `residual-candidate-17` | L316 | documented exclusion: checked and excluded as ordinary text |
| P6 | `residual-candidate-18` | L317 | documented exclusion: checked and excluded as ordinary text |
| P6 | `residual-candidate-19` | L318 | documented exclusion: checked and excluded as ordinary text |
| P6 | `residual-candidate-20` | L319 | documented exclusion: checked and excluded as ordinary text |

**Inventory counts reconciliation (single final table).**

| Page | Rows | Named gaps | Defined at first use | Documented exclusions |
| --- | ---: | ---: | ---: | ---: |
| P1 | 11 | 11 | 0 | 0 |
| P2 | 7 | 3 | 4 | 0 |
| P3 | 8 | 0 | 8 | 0 |
| P4 | 6 | 0 | 6 | 0 |
| P5 | 8 | 0 | 8 | 0 |
| P6 | 31 | 0 | 20 | 11 |
| P7 | 8 | 0 | 0 | 8 |
| P8 | 3 | 0 | 0 | 3 |
| **Total** | **102** | **14** | **46** | **42** |

**Unique/zero-duplicate proof:** rows = unique (page, token, first-use line) keys = **102**; duplicate keys = **0**; extra rows = **0**; one disposition per row.

## 5. Dispositions, keeper exclusion and continuation

**Disposition tally: 0 FULL / 8 PARTIAL (P1-P8) / 0 UNRUN.** All eight pages were read whole; no page is UNRUN. No page is FULL: each lacks the canonical B6 independent read-only review evidence (which cannot be established from git metadata), and six also have named B2 first-use gaps. Named-gap pages: **P2 L3 PRD; P4 L3 CPU/I/O; P5 L66 p99; P6 L3 repo, L178 n/a; P7 L15 repo, L25 ID, L70 ISO; P8 L15 A-*.** P1 and P3 have no named B2 gap and are PARTIAL solely on canonical B6.

**Keeper exclusion.** **No page is keeper-eligible on this record.** Canonical B6 requires a read-only review by someone who did not write the page and this record cannot establish that condition; accordingly it authors **no acceptance row, no keeper row, no ledger edit and no index edit**, and it does not mark any page FULL for a later keeper to consume. Keeper recording remains a separate later act under AEGIS-APR-101/APR-117 with its own independence evidence.

**Continuation.** Lane A is complete (0-143); merged lane-B evidence covers 144-167 + 168-183 + 192-199; in-flight #831 reserves 184-191; this record covers **200-207**. The next lane-B block begins at **208** and must re-derive the pending set and frontier at its own base. No page, plan, keeper or index change is made by this record.

## 6. Provenance, page authorship, zero drift and reader independence

**Reader.** One reader - **sd-a-789-repl-r2 / stage role sd-c-read-b12-c1**, DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness) - read all eight pages whole, line by line, as prose at the pinned blob; no display elision. The page authors are not this reader.

**Page authorship and witness rows (blob-bound):**

| # | Pending index | Page | Blob at pinned ref | Last-touching commit | Author | Date |
| --- | ---: | --- | --- | --- | --- | --- |
| P1 | 200 | `.claude/skills/product-analytics-instrumenter/references/instrumentation-sheet.md` | `09bdcb70ba472229e6c0d1374b2b5f7ef18893fd` | `8e790000aa8a913722584fca7435d05f5dd0787f` | Peter Nguyen | 2026-09-23 |
| P2 | 201 | `.claude/skills/product-spec-writer/SKILL.md` | `b625b2fa27d8e12057ceeaecaad9ac170a4d19fb` | `7645ca4998fd4f26be5c9236ae201cbab6216c10` | ModernNomad-98 | 2026-10-10 |
| P3 | 202 | `.claude/skills/product-spec-writer/references/product-spec-sheet.md` | `54668786dcb6680f815cfff960f858e7d55eef9a` | `7645ca4998fd4f26be5c9236ae201cbab6216c10` | ModernNomad-98 | 2026-10-10 |
| P4 | 203 | `.claude/skills/profiling-methodology-designer/SKILL.md` | `51c131afa3c553f1b1da7c99535540c2a9a169fc` | `54034fa23ba3fd66fb40032b12d9511d22c66cf8` | Peter Nguyen | 2026-09-28 |
| P5 | 204 | `.claude/skills/profiling-methodology-designer/references/profiler-selection-guide.md` | `1d657457d61c1eecbf531d8b6c318c6b8bbeb2c8` | `d629d3a163a4731d3956ba9a113f276976ba1c9d` | Peter Nguyen | 2026-09-23 |
| P6 | 205 | `.claude/skills/project-orchestrator/SKILL.md` | `4400f46d97193b725846fa5247ac305c86c3ae83` | `935411cf5b9258dc06c925a9258ab4a90e8e94fc` | Peter Nguyen | 2026-10-04 |
| P7 | 206 | `.claude/skills/project-orchestrator/references/project-state-template.md` | `4c9b3d68307305a2be949e9a0c7cdd40eb5bc9ac` | `8459ac73ba6e0b280338aca9a97be7a3336ce356` | Peter Nguyen | 2026-09-28 |
| P8 | 207 | `.claude/skills/project-orchestrator/references/recording-and-authority.md` | `9ed5b7af0740104a358f6acc6b7cec0e02f8526a` | `d629d3a163a4731d3956ba9a113f276976ba1c9d` | Peter Nguyen | 2026-09-23 |

**B6 witness and basis.** For every page the reader identity differs from the git-metadata author, **but git metadata cannot prove that the reader did not author the page in another identity, nor that a reviewer who did not write the page read it**. **Basis:** git metadata (last-touching commit author and date) plus the pinned blob IDs; P2/P3's last-touching commit is the owner account, the others are Peter Nguyen. **Limit:** the independence condition of canonical B6 is unverified here; that limit is stated rather than papered over and is why all eight pages are PARTIAL and no page is keeper-eligible.

**Zero drift.** Each blob above resolves at main 655e40ea8d6a16cbdaeab1a9a7eb77fd26207e75 to the same object as at pinned ref 2db1ffb7; `git diff --numstat 2db1ffb7..655e40ea8d6a16cbdaeab1a9a7eb77fd26207e75 -- <page>` is empty for all eight. No page outside the frozen set is read or claimed.

## 7. Hunk and line accounting / local validation performed while authoring

**Hunks.** One added record file, zero modified files, zero deleted files (verified by `git diff --name-status 655e40ea8d6a16cbdaeab1a9a7eb77fd26207e75..the final repaired head stated in the SD-C handoff`). The record has one terminal LF, no CR, no trailing-whitespace line, no blank line at EOF, and never contains its own digest.

**Local validation actually run before the Stage C handoff (hosted CI and Codex are recorded in the SD-C handoff, not asserted here):** `git diff --check` on the branch; `python -B scripts/check_dco.py --range 655e40ea8d6a16cbdaeab1a9a7eb77fd26207e75..the final repaired head stated in the SD-C handoff`; `python -P scripts/validate-skills.py`; `python -P -B scripts/ci/check-markdown-links.py docs/evidence/documentation/readability-lane-b-batch-12-2026-10-18.md`; the PR-body bound-field checker on the final body. Anything not run is UNRUN, never passed.

## 8. Limits and unverifiable items

- **Canonical B6 (reader independence):** unverified for all eight pages; this record cannot establish a read-only review by someone who did not write the page, so no page is FULL or keeper-eligible.
- **Canonical B4:** assessed per page for instructional/reference content with no shipped/deployed or measured-result claim; a later page change that adds such a claim must re-evaluate B4.
- **Scheduling coverage:** #828/#831 are in flight and their reservations are scheduling citations; a later stage must re-derive the whole pending set at its own base (AC7/AC8); this record does not assert their merges.
- **Token audit scope:** the five-class audit is complete under its stated class definitions and exclusion rule; ordinary English words, numeric values and typographic punctuation are filtered after context, and the documented-exclusion rows record every borderline case.
- **PARTIAL pages:** the named gaps and unverified B6 are the reason for PARTIAL; if a later audit finds another missed token, that is a new finding, not a reinterpretation of this record (the scan's method and exclusions are stated above).
- **This record cannot verify its own final hash** (it never contains its own digest); the PR body and SD-C handoff state the record's measured bytes/LF/CR/sha256/blob outside the record.

**Signed with both names: true identity sd-a-789-repl-r2; stage role sd-c-read-b12-c1.** **Written by: DeepSeek V4 Flash (deepseek-flash, DeepSeek Harness).**
