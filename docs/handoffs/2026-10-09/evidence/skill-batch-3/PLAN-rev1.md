# PLAN — Batch build of three QA design skills (skill-batch-3)

- **Stage:** A (PLAN). **Scope:** plan only — **no source edits** in this stage.
- **Base:** `origin/main` @ `b5cf2803cb8166446123b1b88f3f5565f2bd7e8c`, read from the clean worktree `_resume-2026-10-09/wt-main` (HEAD verified == the named SHA).
- **Source of truth for the owned gaps:** `docs/roadmaps/unselected-expansion-skill-batch-proposal.md` table rows 538–540 (group **G1 — QA expansion Tier 2**).
- **Classification:** skill additions to the library (three **BUILD** items). Governing change class: **ai-agentic**. Security answer: **Yes** (details in §5–§6).

---

## 0. Baseline counts — re-derived from main, not guessed

| Figure | Value | Evidence |
| --- | --- | --- |
| Shipped skills on disk | **195** | 196 directories under `.claude/skills/` minus `_template`; all 195 contain `SKILL.md`. |
| Discipline families | **23** | `<!-- FAMILY-COUNT -->23` marker, README line 750. Roster per-family counts sum to 194 + the one `project-orchestrator` front door = **195** ✓. |
| Family 6 "QA, E2E & evidence" | **19** | `*(Phase 5, 19)*` (README line 783) == the 19 QA-pack rows in the catalog (lines 517–537). |
| After this batch | **198** skills / **23** families / family 6 = **22** | 195 → 198; FAMILY-COUNT unchanged; family 6 19 → 22. |

The proposal itself confirms the current entrypoint count: *"If a later owner choice adds one new skill and no others, the entrypoint count would change from 195 to 196; no skill is added by this page."* (proposal line 126–127).

---

## 1. Batch overview

Three clean-BUILD, read-only **design** skills, all in QA family 6. Each produces a *design document* over supplied inputs and **edits/writes/drives nothing** — so per §5 each is **auto-invocable** (no `disable-model-invocation`, no `MANUAL-ONLY` sentinel). This matches the proposal's posture note (line 46–47): *"A proposed supplied-input review or design skill may remain **auto-invocable**; a later build must assess its exact permissions and workflow."*

| # | Directory name | Roadmap | Proposal row | Hours | Posture |
| --- | --- | --- | --- | --- | --- |
| 1 | `visual-regression-test-designer` | #203 P2 (adjacent #179/#202/#189) | 538 | 3.25–5 | auto-invocable |
| 2 | `exploratory-charter-designer` | #228 P1 (as `exploratory-testing-charter`) | 539 | 2–3.5 | auto-invocable |
| 3 | `mobile-journey-test-designer` | #230 P1 (as `mobile-viewport-qa`) | 540 | 2.5–4 | auto-invocable |

---

## 2. Per-skill plan

### 2.1 `visual-regression-test-designer` (#203 P2)

**What it does.** Design visual/pixel-regression test coverage for a web UI: which UI states are stable enough to capture, the deterministic baseline + diff/compare mechanics, the positive snapshot-selection rule with explicit update review (#202), and the deterministic state-rendering slice for fixture/render surfaces (#189). It produces the coverage *design*; it captures/compares **nothing**.

**Why (owned gap — quoted).** Proposal row 538: *"`screenshot-evidence-planner` points visual tooling at `qa-automation-architect`; a scoped search of that directory for visual/pixel/snapshot terms found no matching guidance. This is a textual mismatch, not a failed route. #202's positive snapshot-selection rule and #189's state-rendering residue are still unbuilt."* Roadmap #203: *"Capture critical UI states with stable data, deterministic viewport, and reviewable diffs."* Adjacent unbuilt slices: #179 *"Identify stable screens and states suitable for screenshots or visual diff testing"*, #202 *"Use snapshots only for stable, meaningful outputs with explicit update review"*, #189 *"Use local or test-only routes and deterministic fixtures for broad UI regression coverage."*

**Trigger / Use When.** Use when asked to design visual/pixel-regression coverage, decide which screens/states to snapshot, define a baseline/diff workflow, or govern snapshot selection/updates. **Do NOT use** for the evidence naming/masking/storage *policy* (`screenshot-evidence-planner`), a general per-change test plan (`test-plan-designer`), automation tooling/framework design (`qa-automation-architect`), retain/retire curation of existing tests (`regression-suite-curator`), or writing Playwright/E2E specs (`playwright-e2e-engineer`).

**Invocation posture (§5).** Read-only design over supplied inputs → **auto-invocable**; no `disable-model-invocation`; description does **not** start with the `MANUAL-ONLY` sentinel.

**Nine SKILL.md headings (content to be written at Stage C):**
1. **Purpose** — one paragraph: designs visual regression coverage (stable-state capture, baseline/diff, snapshot governance, deterministic rendering); captures nothing.
2. **Use When** — triggers + the Do-NOT list above.
3. **Inputs to Inspect** — UI surface/route inventory, existing `screenshot-evidence-planner` policy, repo snapshot tooling, stable vs dynamic data sources, CI config, risk-critical states.
4. **Workflow** — inventory critical states → classify stability (#179) → select positive snapshot candidates with a reviewable-diff rule (#202) → specify deterministic state-rendering (#189) → define baseline capture/compare/update-review gates → emit the design.
5. **Output Format** — coverage design: named stable states (data/viewport determinism), baseline/diff mechanics, snapshot-selection + update-review rule, deterministic-rendering notes, CI gate placement, out-of-scope; states what was chosen, why, and the main rejected alternative.
6. **Validation Checklist** — every state names its determinism; snapshots restricted to stable+meaningful outputs; update review explicit; CI placement named; out-of-scope present; no claim to run/capture.
7. **Gotchas** — unstable/meaningless-output snapshots flake; timezone/locale/animation drift; baseline drift; "update all" without review masks regressions; must not reproduce `screenshot-evidence-planner`'s policy.
8. **Stop Conditions** — missing UI/route inventory; ambiguous "critical state"; request drifts into executing captures (`playwright-e2e-engineer`/`clickthrough-test-engineer`) or writing the evidence policy (`screenshot-evidence-planner`); destructive/live-state action.
9. **Supporting Files** — `evals/evals.json`, `evals/trigger-evals.json`; `references/` only if snapshot-mechanics detail is needed (else "None").

**Evals.**
- `evals/evals.json`: (normal, `should_trigger`) design visual regression coverage for a UI; (edge, `should_trigger`) snapshot-selection for a state with dynamic content; (near-miss, `should_not_trigger`) "what should our screenshot naming/masking policy be" → defers to `screenshot-evidence-planner`; (refusal, `should_trigger`) ambiguous surface → halts and asks.
- `evals/trigger-evals.json` (`overlaps_with`: `screenshot-evidence-planner`, `test-plan-designer`, `qa-automation-architect`, `regression-suite-curator`): cases asserting this skill wins for "design visual/pixel coverage" and the named neighbor wins for policy/plan/tooling/curation prompts.

**Blast radius (per skill).** New directory `.claude/skills/visual-regression-test-designer/` with `SKILL.md` + `evals/evals.json` + `evals/trigger-evals.json`. No edit to any existing skill (one-way "Do NOT use" mentions are information, not a failure — ROUTE-002).

### 2.2 `exploratory-charter-designer` (#228 P1)

**What it does.** Produce an exploratory-testing charter: a timeboxed mission, the risks/open questions to probe, personas, data, entry paths, and note/evidence conventions — so a tester runs a focused exploratory session and reports findings instead of unguided wandering.

**Why (owned gap — quoted).** Proposal row 539: *"`qa-strategy-architect:142-144` says strategies that omit manual testing 'leave visual, UX, and exploratory risks unowned'; no shipped skill writes charters."* Roadmap #228: *"Define mission, risks, personas, data, paths, and timebox for exploratory testing."*

**Trigger / Use When.** Use when asked to design an exploratory-testing charter, define a timeboxed exploratory mission, or turn "we need to explore X" into a scoped session. **Do NOT use** for a deterministic test plan (`test-plan-designer`), scripted manual cases (`manual-test-case-creator`), the product-wide QA strategy (`qa-strategy-architect`), or executing a live walkthrough (`clickthrough-test-engineer`).

**Invocation posture (§5).** Read-only design → **auto-invocable**; no manual-only flag.

**Nine SKILL.md headings:**
1. **Purpose** — one paragraph: timeboxed exploratory charters (mission, risks, personas, data, paths) that make manual exploration scoped and reportable.
2. **Use When** — triggers + Do-NOT list above.
3. **Inputs to Inspect** — feature/surface to explore, known risks, personas/roles, available test data, prior defects/notes, the QA strategy's automation/manual split, timebox budget.
4. **Workflow** — state mission + timebox → enumerate risks/open questions → name personas/data/entry paths → bound scope (in/out) and defect-report conventions → emit the charter.
5. **Output Format** — charter: mission, timebox, risk list, personas, data, paths, note/evidence conventions, out-of-scope; states what was chosen, why, and the main rejected alternative.
6. **Validation Checklist** — mission + timebox present; risks map to probe areas; personas/data/paths concrete; scope bounded; no claim to have executed the session.
7. **Gotchas** — a charter is not a scripted case (no step-by-step expected results); the timebox keeps it bounded; output is findings, not pass/fail; must not absorb `manual-test-case-creator`/`clickthrough-test-engineer` jobs.
8. **Stop Conditions** — feature/scope ambiguous; no risk/entry context; request becomes executing a live session (`clickthrough-test-engineer`) or writing scripted cases (`manual-test-case-creator`).
9. **Supporting Files** — `evals/evals.json`, `evals/trigger-evals.json`; `references/` if charter templates are needed (else "None").

**Evals.**
- `evals/evals.json`: (normal) design an exploratory charter for a feature; (edge) a charter with a hard timebox and limited data; (near-miss, `should_not_trigger`) "write step-by-step manual test cases" → defers to `manual-test-case-creator`; (refusal) ambiguous target → halts and asks.
- `evals/trigger-evals.json` (`overlaps_with`: `manual-test-case-creator`, `clickthrough-test-engineer`, `test-plan-designer`, `qa-strategy-architect`): charter vs scripted-case vs live-walkthrough vs per-change-plan vs strategy.

**Blast radius (per skill).** New directory `.claude/skills/exploratory-charter-designer/` (`SKILL.md` + two eval files). No existing-skill edit.

### 2.3 `mobile-journey-test-designer` (#230 P1)

**What it does.** Design mobile-journey QA coverage: which critical journeys to verify on mobile breakpoints, the touch interactions, dialogs, navigation (and orientation/keyboard/safe-area) to check, and how the pass is executed/evidenced — the mobile counterpart that `mobile-viewport-craft` (layout) explicitly does not own.

**Why (owned gap — quoted).** Proposal row 540: *"Layout is `mobile-viewport-craft`'s; journey checks on phones are not ('Deep responsive QA is its own effort', `clickthrough-test-engineer/references/clickthrough-route-catalog.md:31`)."* Roadmap #230: *"Verify critical journeys on mobile breakpoints, touch interactions, dialogs, and navigation."*

**Trigger / Use When.** Use when asked to design mobile/phone journey test coverage, verify critical journeys on mobile breakpoints, or plan mobile touch/dialog/navigation QA. **Do NOT use** for layout/touch/viewport *correctness* design (`mobile-viewport-craft`), executing a live clickthrough (`clickthrough-test-engineer`), implementing permanent E2E specs (`playwright-e2e-engineer`), or a general per-change test plan (`test-plan-designer`).

**Invocation posture (§5).** Read-only design → **auto-invocable**; no manual-only flag.

**Nine SKILL.md headings:**
1. **Purpose** — one paragraph: mobile-journey QA design (critical journeys × mobile breakpoints/touch/dialogs/navigation), distinct from layout craft.
2. **Use When** — triggers + Do-NOT list above.
3. **Inputs to Inspect** — critical journeys/routes, responsive surfaces, `mobile-viewport-craft`'s layout spec (correctness assumptions), existing E2E/clickthrough coverage, personas/devices/breakpoints, network/offline considerations.
4. **Workflow** — identify critical journeys → enumerate mobile-specific checks (breakpoints, touch, dialogs, navigation, orientation, keyboard, safe-area) → map journeys to a device/viewport + data matrix → specify pass execution + evidence (composing `screenshot-evidence-planner` naming/masking) → emit the design.
5. **Output Format** — mobile-journey QA design: named journeys, the mobile check matrix, device+data matrix, execution/evidence conventions, out-of-scope; states what was chosen, why, and the main rejected alternative.
6. **Validation Checklist** — journeys are the critical ones; mobile-specific checks enumerated; device/viewport matrix named; evidence follows `screenshot-evidence-planner`; out-of-scope present; no claim to drive a browser.
7. **Gotchas** — journey QA ≠ layout correctness (`mobile-viewport-craft`); touch/dialog/orientation are commonly missed by desktop E2E; it must not execute (that is `clickthrough-test-engineer`/`playwright-e2e-engineer`); evidence rules come from `screenshot-evidence-planner`.
8. **Stop Conditions** — no journey/route inventory; request becomes a layout redesign (`mobile-viewport-craft`) or executing a pass (`clickthrough-test-engineer`); destructive/live actions.
9. **Supporting Files** — `evals/evals.json`, `evals/trigger-evals.json`; `references/` if the device matrix is large (else "None").

**Evals.**
- `evals/evals.json`: (normal) design mobile-journey QA for an app; (edge) a journey that only differs on a small breakpoint; (near-miss, `should_not_trigger`) "fix the 100vh layout on phones" → defers to `mobile-viewport-craft`; (refusal) no route inventory → halts and asks.
- `evals/trigger-evals.json` (`overlaps_with`: `mobile-viewport-craft`, `clickthrough-test-engineer`, `playwright-e2e-engineer`, `test-plan-designer`): journey-QA design vs layout-craft vs live-walkthrough vs E2E-spec vs per-change-plan.

**Blast radius (per skill).** New directory `.claude/skills/mobile-journey-test-designer/` (`SKILL.md` + two eval files). No existing-skill edit.

---

## 3. Shared registration (the batch)

All three skills register identically. Per `CONTRIBUTING.md` "How to add a skill" step 3 (surfaces 3a–3f) and rule 8:

- **3a — `docs/skills-catalog.md`.** Add three rows to the **"### Skills (Phase 5 — QA, E2E, manual QA & evidence pack)"** table (lines 517–537), columns `Skill | Source (category doc) | Model-invocable? | Trigger summary`:
  - `visual-regression-test-designer` | cat 06 **#203** | **yes** | one-line trigger summary (stable-state capture, baseline/diff, snapshot governance, deterministic rendering; designs, captures nothing).
  - `exploratory-charter-designer` | cat 06 **#228** | **yes** | one-line trigger summary (timeboxed exploratory charter; designs, executes nothing).
  - `mobile-journey-test-designer` | cat 06 **#230** | **yes** | one-line trigger summary (critical-journey mobile QA design; layout stays with `mobile-viewport-craft`).
  - Also extend the Phase 5 prose + trigger-overlap-cluster note to name the three new skills (they ship `trigger-evals.json`), and mark #203/#228/#230 as **graduated** in the "Backlog by phase → Phase 5" note (line 1327) — the *banked-candidate graduation* that `library-diff-reviewer` checks.
- **3b — README "Skills (shipped)" table.** Add three rows to the Phase 5 QA table (lines 1138–1158), `Invocation = auto + manual`, e.g. `| `visual-regression-test-designer` | (G1, #203) Designs visual/pixel-regression coverage: stable-state capture, baseline/diff, positive snapshot-selection + update review, deterministic rendering. Designs; captures nothing. | auto + manual |`.
- **3c — README roster family.** Family 6 "QA, E2E & evidence" `*(Phase 5, 19)*` → `*(Phase 5, 22)*` (line 783). **No new flagship** `*e.g.*` entries (these are Tier 2 expansions, not flagships). **No new family**, so `FAMILY-COUNT` is unchanged.
- **3d — README count claims.** `<!-- SKILL-COUNT -->195<!-- /SKILL-COUNT -->` → **198** (line 750). `FAMILY-COUNT` stays **23**. Historical dated counts (e.g. the D68–D71 "186→195" row, line 1035) are left untouched as recorded-revision evidence.
- **3e — "The roles Aegis can play" table.** **No change.** The three skills extend the existing QA role (line 74), not a new user-facing capability/role.
- **3f — `docs/ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md`.** **No change.** None of the three is named under a doctrine pillar.
- **Decision record (recommended, not validator-enforced).** Bank one dated `D`-entry in `docs/reconciliation/step-0-reconciliation-v4.md` §5 recording the build decision (per CONTRIBUTING rule 4; precedent D68–D71 for skill-batch builds). This is judgment, not part of the 3a–3f validator set, but it is one of the registration-consistency items `library-diff-reviewer` checks.

**Validator-enforced (hard errors):** 3a name presence, 3b name presence, 3d SKILL-COUNT == skills on disk, and family-roster reconciliation (per-family counts + `project-orchestrator` == total; family-line count == FAMILY-COUNT). **Judgment:** 3c flagship choice, 3e role decision, 3f pillar link.

---

## 4. Change classification (via `change-classification-gate`)

```
CHANGE CLASSIFICATION
Deliverables:    3 new skills (.claude/skills/<name>/SKILL.md + evals/evals.json + evals/trigger-evals.json)
                 + registration edits (docs/skills-catalog.md, README.md)
Classes:         ai-agentic (the skills — "Prompts, skills, agent instructions, tool grants, model config",
                 matrix line 21); docs-only (catalog + README registration prose, not agent-instruction files)
Governing class: ai-agentic  (highest class governs)
Approval path:   human-approval-boundary — behavior changes (three new invocable procedures); already
                 authorized by the owner's batch selection, delivered under the seven-stage workflow
Validation plan: ai-agentic floor — eval cases added (evals.json + trigger-evals.json per skill) + guardrail
                 review (no allowed-tools/hooks/shell; no tool grants; no injection surface; read-only);
                 docs-only floor — links/references resolve; count arithmetic reconciles
Scope contract:  .claude/skills/{visual-regression-test-designer,exploratory-charter-designer,
                 mobile-journey-test-designer}/ + docs/skills-catalog.md + README.md
```

Rationale: skills are explicitly *not* docs-only (matrix line 14 "NOT agent-instruction files"; line 21 names "skills"). Adding three skills is an **ai-agentic** change with a docs-only registration component; the ai-agentic class governs the approval path. Each skill is read-only and adds no tool grants, so the ai-agentic approval is the owner's selection already recorded in the proposal (G1 BUILD rows), consumed through the seven-stage workflow.

---

## 5. Expected security answer (PR template — required)

**Yes.** The PR authors three new skills under `.claude/skills/`. Two named security-relevant surfaces from `CONTRIBUTING → External contributions` are touched:

- **each new skill's frontmatter invocation posture** — the posture decision (auto-invocable; no `disable-model-invocation`; no `MANUAL-ONLY` sentinel) is authored in each `SKILL.md` frontmatter; and
- **each new skill's Stop Conditions** — §8 requires them and they are authored here.

**Not touched** (so no broader surface list): `scripts/`, `.github/`, `AGENTS.md`, `.claude/agents/`, `tools/`, pinned dependency files, the owner approval register, `docs/skill-generation-standard.md` §5, and **no existing skill's** frontmatter posture, Security Rules, or Stop Conditions. No `allowed-tools`/`hooks`/`shell` keys and no tool grants are added.

---

## 6. Plan- and review-ownership (procedural vs skill-owned)

- **Who owns writing this plan: none.** `delivery-workflow.md` line 97: *"**No skill was found that owns writing a single change's plan**; treat that shape as procedural."* (`ai-task-decomposer` only splits a broad goal into PR-sized tasks; it is not the author of a single change's plan.) Stage A is therefore procedural.
- **Who owns reviewing a skill-library change: `library-diff-reviewer`.** `delivery-workflow.md` lines 100 and 102 route Stage D (implementation audit) and Stage F (final PR review) to `library-diff-reviewer` where the PR changes the skill library (`code-reviewer`'s own contract defers library diffs to it).

---

## 7. Acceptance criteria (AC1–AC8) — verifiable by Stage D

Stage D (independent implementation audit, `library-diff-reviewer`) checks these one by one at the exact implementation head:

- **AC1 — Directories.** `.claude/skills/visual-regression-test-designer/`, `.claude/skills/exploratory-charter-designer/`, and `.claude/skills/mobile-journey-test-designer/` each exist and each contain `SKILL.md`, `evals/evals.json`, and `evals/trigger-evals.json`.
- **AC2 — Contract.** Each `SKILL.md`: frontmatter `name` == directory name; `description` strict-YAML-valid, one physical line, parsed < 1024 chars, capability front-loaded (~90 chars); **no** `disable-model-invocation` (all three are read-only, auto-invocable, no `MANUAL-ONLY` sentinel); no forbidden `hooks`/`allowed-tools`/`shell` keys and no `!` shell-injection; < 500 lines; all nine §4 headings present and in order.
- **AC3 — Validator.** `python scripts/validate-skills.py` exits 0 and reconciles the skill count to **198**.
- **AC4 — Evals.** Each `evals/evals.json` carries a happy-path `should_trigger`, an edge `should_trigger`, a near-miss `should_not_trigger`, and a stop-condition `should_trigger` case with objective assertions; each `evals/trigger-evals.json` parses as JSON and discriminates the new skill against its named neighbors (`expected_skill` + `should_not_trigger`), per standard §6.
- **AC5 — Catalog (3a).** All three names appear in `docs/skills-catalog.md` Phase 5 implemented table with source `cat 06 #203`, `cat 06 #228`, `cat 06 #230` and "yes" (model-invocable), and #203/#228/#230 are marked graduated in the Phase 5 backlog note.
- **AC6 — README (3b/3c/3d).** All three names appear in README "Skills (shipped)" Phase 5 table with "auto + manual"; family 6 marker reads `*(Phase 5, 22)*`; `<!-- SKILL-COUNT -->` reads **198**; `<!-- FAMILY-COUNT -->` remains **23**.
- **AC7 — Coherence / blast radius.** The diff contains exactly the three new skill directories plus `docs/skills-catalog.md` and `README.md` (and the decision-record entry if Stage C banks one); no change to `.claude/agents/`, `scripts/`, `.github/`, `tools/`, `docs/skill-generation-standard.md` §5, or any existing skill's frontmatter/Security Rules/Stop Conditions — nothing smuggled in.
- **AC8 — PR body.** The PR states the classification (**ai-agentic** governing class) and answers the security question **Yes** with the two named surfaces (new skills' invocation posture + Stop Conditions), and the "Aegis skills used" table is filled; count arithmetic (195→198, family 6 19→22, families 23) agrees everywhere it appears.

---

## 8. What this batch deliberately does NOT do

- No EXTEND of `qa-automation-architect` (#213 timeout policy) — outside this batch.
- No `role-coverage-test-designer` (#229, DEFER) or `mock-strategy-designer` (#200/#201, DROP) work.
- No reciprocity edits to `screenshot-evidence-planner` or any existing skill (one-way "Do NOT use" is information, not a failure — ROUTE-002).
- No new family, no new roles-table row, no doctrine-pillar edit.

