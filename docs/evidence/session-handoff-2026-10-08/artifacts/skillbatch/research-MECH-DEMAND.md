# Skill-batch planning research: MECH (delivery mechanics, measured cost, storage convention) and DEMAND (gap/demand evidence)

Helper: MECH-DEMAND research helper (Stage A support only; writes no repository file, no GitHub writes).
Start: 2026-10-08T17:11:40Z (`date -u`). Finish: see the hand-back report (stamped at hand-back).
Base: `origin/main` = `5228977920ee479e1fe1ec6b8d56f8fc24c14947` (`git ls-remote origin refs/heads/main`, checked at start and again at 17:29:54Z; unchanged).
Working tree used: a fresh `git archive origin/main` export at `$S/skillbatch/mech2` (S = this session's scratchpad). `diff -rq` against the earlier `mech-tree` export: no differences. The local checkout is at `c060a7cb`, which is BEHIND origin/main, so it was not used for file reads.
Role: Role A. All four landmarks present: `README.md` line 1 is `# Project Aegis`; `docs/skills-catalog.md`, `scripts/validate-skills.py` and `artifacts/audits/skill-contract-audit-baseline.json` exist. `python3 -B scripts/validate-skills.py` on the export: `OK: 195 skill(s) valid, 0 warning(s)`, exit 0.
Raw evidence kept in scratch: `$S/skillbatch/mech-prs/` (REST JSON for PRs #383, #492–#527, #670–#680, their file lists and commits, open/all issues, old/new audit baselines, the validator log). Scripts: `$S/skillbatch/mech-scripts/` (`dangling.py`, `walls.py`, `calib.py`).

## Aegis skills used (dogfood rule)

| Skill | Why it applies | What it did here |
| --- | --- | --- |
| `agent-startup-context-gate` (auto-invocable; read in full at `.claude/skills/agent-startup-context-gate/SKILL.md`) | Start of a repository research task in a session with stale local state | Role A verified from the four landmarks; noticed the local checkout (`c060a7cb`) is behind `origin/main` (`52289779`) and switched to a fresh export; recorded facts vs assumptions below. |
| `source-of-truth-reconciler` (auto-invocable; read in full) | Several planning sources disagree (forecast vs proposals, "backlog" surfaces, historical priorities, a defect marked "corrected") | Produced the reconciliation report in section 0 with precedence rules; proposed no silent edits. |

No MANUAL-ONLY skill was used. No skill owns "research a skill-batch plan" as such; the delivery workflow records that no skill owns Stage A planning (`docs/delivery-workflow.md:97`).

## 0. Reconciliation report (source-of-truth-reconciler format)

```
RECONCILIATION REPORT
Conflicts:
  C1: Forecast prices every unselected candidate at a flat 2–4 agent-h (six groups = 68–140;
      docs/roadmaps/aegis-backlog-forecast.md:212, table :723-735; arithmetic re-run: 68/140)
      vs the four precedent proposals, which after overlap triage landed at 0.49x–1.45x of
      their forecast group ranges (qa-tier1…:65, ai-sdlc…:71, phase7…:72, phase6…:81).
      Type: IS (cost).  Verdict: no active-time measurement exists to settle it (rule 2 cannot
      apply); hold both. The proposal page states its own triaged estimate and COMPARES it to the
      forecast, as every precedent did; the forecast is re-estimated at its own checkpoint.
  C2: Coordinator reading "follow the precedent proposals' pointers" vs owner's "store these plans
      in the repo's backlog". Precedent proposal PRs #492/#494/#495/#496 each changed exactly ONE
      file (REST files list). Type: SHOULD. Verdict: owner instruction outranks precedent (rule 1);
      a page under docs/roadmaps/ satisfies "in the repo"; the repository's own designated list of
      "items in the backlog at the owner's request" is open-decisions :243-246 — see §(c) option B.
  C3: The catalog is where the expansion backlog is listed (docs/skills-catalog.md:1300-1342) vs the
      catalog's SHA-256 is recorded in the just-refreshed audit baselines
      (artifacts/audits/skill-contract-audit-baseline.json:15-17 and corpus-manifest-baseline.json:14-16
      = 6e32cee1…7fd01, equal to `sha256sum docs/skills-catalog.md` at 52289779).
      Type: SHOULD. Verdict: the storage PR must not edit the catalog (an edit stales the baseline
      provenance; regeneration needs a new grant — APPROVAL_REGISTER.md:2366-2367, APR-119 at :5064).
  C4: docs/skills/*.md priorities (P0/P1/P2) vs their own legend: "original planning tiers … A
      priority does not state whether a row shipped" (01-software-architecture-engineering.md:14-16);
      product-agnostic roadmap is a "Historical proposal" (product-agnostic…:3-6).
      Type: IS. Verdict: use priorities only as planning-time value, never as observed demand.
  C5: VolunteerFlow AEGIS-013/-028 rows say "Symptom corrected" (Defect-Handoff…:1005, :1020) vs the
      same report's authority rule "A same-session correction … does not resolve a Project Aegis
      repository defect" (:21). Type: IS. Verdict (rule 2, actual repo state): product-spec-writer and
      requirements-gathering-facilitator contain no idempotency/repeated-request lens (grep for
      idempoten|retry|duplicate|repeated|replay found only unrelated hits), so the spec-level fix is not
      visible in the shipped skills. Least-certain: a fix could exist under wording I did not search.
Assumptions surfaced: none used as a basis; unverified items are labelled inline.
Stale sources to fix (follow-up, not done here): docs/README.md:74-90 lists only the feature-flag
  proposal, not the four D68–D71 batch proposals.
Blocked: none for this helper.
```

---

# PART 1 — MECH

## (a) How the last four batches went from proposal to merged skills

### Sequence, with PR evidence (REST `pulls/{n}` and `pulls/{n}/files`)

| Step | D68 QA Tier 1 | D69 AI-SDLC | D70 Phase 7 | D71 Phase 6 |
| --- | --- | --- | --- | --- |
| 1. Proposal page PR (1 file each) | #492, opened 17:51:44Z, merged 20:48:10Z (`e0f1d244`), +597 | #494, merged 21:52:38Z (`4ee21152`), +554 | #495, merged 21:52:48Z (`e77403cc`), +548 | #496, merged 22:07:18Z (`76b399b1`), +687 |
| 2. Owner decision | chat, "Build it as recommended (Recommended)" (reconciliation :3388-3392) | same (:3460-3463) | same (:3529-3532) | "Build all, backup verifier first (Recommended)" (:3605-3608) |
| 3. Decision-record PR | #493: D68 in reconciliation §5 (+55) and one open-decisions row (+6/-4); merged 21:51:56Z | #510: D69+D70+D71 together (+228 reconciliation, +5/-2 open-decisions); merged 23:35:32Z | (in #510) | (in #510) |
| 4. Build PRs (one per new skill, one per extension) | #499 `acceptance-criteria-reviewer`, #500 `test-tenant-provisioner`, #502 `ci-failure-classifier`, #498 `test-plan-designer` ext. | #517 `ai-task-decomposer`, #511 `ai-closeout-reporter` ext., #515 `code-reviewer` ext. | #518 `ai-human-in-the-loop-designer`, #513 `ai-router-architect` ext., #519 `model-context-designer` ext. | #523 `database-backup-verifier` (first), #522 `resilience-architecture-reviewer`, #526 `cloud-security-baseline-reviewer`, #521 `environment-parity-reviewer`, #527 `data-migration-runbook-author` ext. |
| Skill count | 186→189 | 189→190 | 190→191 | 191→195 |

All dates 2026-09-28/29 UTC; merge SHAs and times match the forecast's #554 window table (`aegis-backlog-forecast.md:145-206`). Commit-to-merge mapping was re-derived with `git merge-base --is-ancestor` over `git rev-list --first-parent origin/main` (e.g. `89eec69c`→#499 `f0c4b242`; `f9634b01`→#521 `f728880a`).

Key mechanics observed:

- **Per-skill PRs, not batch PRs.** 15 build PRs for 9 new skills + 6 extensions; each PR carried exactly one skill or one extension plus its neighbours' reciprocity edits. Decisions could be batched (#510 recorded three decisions).
- **Build lanes ran in parallel** and D68's build PRs opened before the proposal and decision PRs merged (#499 opened 18:51:11Z; #492 merged 20:48:10Z; #493 merged 21:51:56Z). No build merged before its decision PR merged (#499 merged 22:07:13Z).
- **Parallel new-skill PRs collide on the README count marker.** Three D68 PRs were titled "(186 to 187)"; #502 had to be "Rebased onto `main` and renumbered to 188 to 189 (its title still says 186 to 187)… the new head needs a check" (`session-checkpoint-2026-09-28-evening.md:119`). Under today's seven-stage rule "A moved head **voids** the verdicts bound to the old head" (`CONTRIBUTING.md:99-100`), so each rebase now re-triggers implementation audit, validation and final review. D71 avoided it by pre-assigning counts in titles (#523 "188 to 189", #522 "192 to 193", #526 "193 to 194", #521 "194 to 195").
- **Decision numbers are provisional until recorded.** #496 claimed D70; Phase 7 was recorded first and took D70, Phase 6 took D71 (reconciliation :3535-3540, :3611-3613). Highest on main now: D73 (`grep -o '^- \*\*D[0-9]+'` → 71, 72, 73); no page mentions D74 (`grep -rn 'D74\b'` → empty).
- **Authority pattern.** Each D-entry "authorizes exactly this batch", relies on AEGIS-APR-039 + APR-048/049/050, does not waive `gate-guard`, does not authorize changing `scripts/audit-skill-contracts.py` or its baseline (reconciliation :3440-3452, :3506-3518, :3583-3595, :3664-3678). No approval-register entry was created for any of the four batches.

### Files each new skill PR carried (REST file lists, e.g. #517, #523, #526)

- `.claude/skills/<name>/SKILL.md` (231–339 lines), `evals/evals.json`, `evals/trigger-evals.json`, and at least one `references/` or `assets/` file (#526 shipped five per-provider baselines).
- Neighbour reciprocity: each neighbour's `SKILL.md` (description exclusion) plus that neighbour's `evals/trigger-evals.json` (e.g. #518 touched `human-approval-boundary`, `agent-tool-safety-guard`, `ai-governance-risk-reviewer` and their trigger evals).
- Registration: `README.md` (SKILL-COUNT marker, roster family count, "Skills (shipped)" row — #523 changed family 7 from `(Phase 6, 10)` to `(Phase 6, 11)`), `docs/skills-catalog.md` (row + section prose), `docs/reconciliation/step-0-reconciliation-v4.md` (the backlog table's "✅ built (Dxx)" marker). Stage-map wiring where decided (#517 edited `project-orchestrator/SKILL.md` and `ai-sdlc-operating-model/references/stage-gate-map.md`).
- Median per new-skill PR: 10 files, 729 changed lines (`calib.py`).
- Extension PRs: 5–6 files, median 160.5 changed lines.

### Gates every new skill must pass (current, cited)

- **Validator** (`scripts/validate-skills.py:4-75`; run in CI): strict-YAML frontmatter, `name` = directory, description < 1024 parsed chars, MANUAL-ONLY sentinel bidirectional with `disable-model-invocation`, frontmatter key allow-list (no `hooks`/`allowed-tools`/`shell`), no `!` shell injection, body < 500 lines, nine sections in canonical order, `evals/evals.json` exists and parses, trigger-evals parse if present, name present in catalog AND README (substring test, :565-576), README `SKILL-COUNT`/`FAMILY-COUNT`/roster reconciliation (D43), name collisions, config-surface and symlink checks, and since #670 **`check_no_cross_skill_file_dependencies`** (:1263).
- **#670 rule** (merged 2026-10-05 as `935411cf`): a skill may link a sibling only at its `SKILL.md` entrypoint (delegation); a link into another skill's `references/` etc. is an error; absolute, UNC, drive-letter or repo-escaping targets are errors; percent-encoding is decoded first. Test suite 141→164 assertions (commit message). A new skill's references must therefore be self-contained.
- **Standard §6** (`docs/skill-generation-standard.md:565-581`): evals.json with happy, edge, should-not-do and objective assertions; `trigger-evals.json` MUST ship when the trigger overlaps a neighbour (every one of the nine batch skills shipped one); a MANUAL-ONLY `expected_skill` case must start `Explicitly invoke <skill>. ` (not machine-enforced).
- **Contract audit.** CI runs only its self-tests (`validate-skills.yml:168-169`); the audit is "Not a merge gate (yet)" (`audit-skill-contracts.py:28-31`). The precedent review path compared ROUTE-002 before and after by hand and did not regenerate the frozen baseline (qa-tier1 proposal :521-532). Regeneration needs a new owner grant each time ("Any further change to the audit engine or regeneration of the baselines needs a new grant", `APPROVAL_REGISTER.md:2366-2367`); the 186→195 lag lasted until #679 under AEGIS-APR-119 (`:5064`).
- **Seven-stage workflow** (D72, 2026-10-03; applies to every PR now, the D68–D71 builds predate it): plan with proportionate acceptance criteria → independent plan audit bound to a content hash → implement (head, tree, base recorded) → independent implementation audit per criterion → validate (UNRUN listed) → final review naming the 40-char head plus a hash over three bound PR-body fields → merge receipt with `MG1`–`MG5` (`delivery-workflow.md:25-34`, `:126-134`, `:614-636`). PR body must carry the "Aegis skills used" table, the security answer and the 8-row `## Reconciliation witness` (`.github/pull_request_template.md`).
- **Registration surfaces** (`CONTRIBUTING.md:152-201`): 3a catalog, 3b README table, 3c roster/flagship and family count, 3d count markers, 3e roles table (judgment), 3f discipline doc (judgment).

### Calibration point: ROUTE-002 predictions were exact

The four proposals predicted 8 + 4 + 2 + 10 = 24 new one-way ROUTE-002 findings and one cleared finding. Diffing ROUTE-002 `(owning_skill, related_skills)` pairs between `1d1a5096^` and `1d1a5096` baselines: old 232, new 255, **added 24, removed 1**; every added pair is one the proposals named (D68 list at reconciliation :3410-3417; D69 :3493-3505; D70 :3574-3582; D71 :3647-3663), and the one removal is `agent-harness-architect -> model-context-designer`, which D70 said the extension would clear (:3565-3567, "clears an existing one-way ROUTE-002 finding"). The proposal-time prediction method can be reused with confidence.

### Readability-ledger obligations observed

- A new page "starts pending and stays pending until someone reads it whole" (`aegis-documentation-readability-backlog.md:730`). A skill review that gives no full-page verdict leaves new skill pages pending (#499, ledger :2985; #500, :2984). Later rounds accepted them (#520 "D68 pages", #532 "CFC pages"; ledger :2979-2980 for #521/#526).
- Follow-up churn after the builds (first-parent commits touching each new skill, `git log --first-parent`): `test-tenant-provisioner` 3 later PRs (#520, #611, #637), `ci-failure-classifier` 2 (#532, #602), `database-backup-verifier` 2 (#522 reciprocity, #585), `cloud-security-baseline-reviewer` 1 (#602), `resilience-architecture-reviewer` 1 (#607), `acceptance-criteria-reviewer` 1 (#520); three skills had none. These readability/gloss rounds were not in the batch estimates.
- Recording an acceptance now needs the ledger keeper role (AEGIS-APR-101, `APPROVAL_REGISTER.md`: keeper ≠ author ≠ accepting reviewer; coordinator excluded).

## (b) Measured cost per skill and per batch vs estimates

### What was never measured

- **Active time for any skill build: not measured.** The metrics page says of the feature-flag delivery "without active time neither can be scored" (`aegis-execution-metrics.md:571-572`); its newest checkpoint is "after #491" (`:15`), i.e. before all D68–D71 builds. A scan of all 22 batch PR bodies for active/wall/elapsed/actual/hours found estimate tables only, no actuals (`$S/skillbatch/mech-prs`, python scan).
- Therefore **no estimate in the four proposals has ever been scored**, and any "calibrated" range is anchored to estimates plus wall-time proxies, not to measured active hours.

### Estimates (proposal tables)

| Kind | Precedent estimates (active h) | Mean low–high (`calib.py`) |
| --- | --- | --- |
| New skill (n=9) | ACR 2–3.5, TTP 3–5, CFC 2.5–4 (qa-tier1 :61-63); ATD 2.5–4 (ai-sdlc :66); HITL 3–5 (phase7 :68); CSBR 3–5, RAR 3–4.5, EPR 2.5–4, DBV 3–5 (phase6 :75-79) | 2.72–4.44 (min 2, max 5) |
| Extension (n=6) | 0.75–1.5, 1–2, 0.75–1.5, 1–2, 1–1.5, 1–2 | 0.92–1.75 |
| Drop | 0–0.25 | — |
| Batch overhead | 1.5–3, 1–2, 1.5–2.5, 2–3.5 (qa-tier1 :64, ai-sdlc :70, phase7 :71, phase6 :80) | 1–3.5 |
| Batch totals | 9.75–17.25; 5.25–9.75; 6.5–11.25; 14.5–24 (sum 36–62.25) | vs forecast group ranges: ×0.97/0.86, ×0.53/0.49, ×0.81/0.56, ×1.45/1.20 |

The forecast's flat 2–4 h per candidate (all four groups G1–G4 compute to exactly 2–4 per candidate) is therefore a pre-triage price: triage moved real batches from 0.49× to 1.45× of it.

### Wall-time proxies (REST timestamps; include CI, review and Codex waits; exclude drafting before the first commit)

- New-skill PR, first commit → merge: sorted 2.62, 2.62, 3.26, 3.30, 3.37, 3.73, 3.84, 4.27, 16.29 h; **median 3.37 h** (n=9). The 16.29 h is #521, which waited overnight (`open→merge` 15.96 h). Feature-flag #383: 1.94 h.
- Extension PR, first commit → merge: 1.19–3.95 h, **median 2.25 h** (n=6).
- Commits per new-skill PR: 2–6 (fix rounds).
- Batch, decision commit → last build merge: D68 4.78 h, D69 2.96 h, D70 3.81 h, D71 16.88 h (4.61 h to #526; #521 overnight).
- All four batches: from the first proposal commit (17:50:52Z) to #526 (03:33:26Z next day) ≈ 9.7 h wall for 4 proposals, 2 decision PRs, 9 skills and 6 extensions, with many PRs open at once (at 23:10Z, nine PRs besides the checkpoint's own were open: `session-checkpoint-2026-09-28-evening.md:41`). Wall time cannot be compared with summed active estimates.

### Seven-stage overhead (the only measurement since D72)

FU-1 (#680, 7 files, +140/−15) stage records in session scratch (`$S/fu1/*.md`, not repository records): plan A 25.5 min, plan B 16.3, plan-B audits 10.6 + 3.6, plan-A audit rev2 4.3, implementation ≤ 18.0, implementation audit 11.2, validate 12.4, final review 19.5, merge 5.0 → **≥ 2.11 agent-wall-hours of recorded stage intervals, ≥ 1.81 h of it outside implementation**; three stage finishes were not recorded, so this is a floor. End-to-end wall 2.09 h. FU-2 (#679): plan start 14:13:37Z → merge 15:55:22Z (`$S/fu2/PLAN-E-rev1.md:9`, `MERGE-RECEIPT.md:6`) ≥ 1.70 h end-to-end (a floor: `PLAN-D-rev1.md` records no start time). n=1 for the stage sum; a docs PR, not a skill PR; wall per agent, not active time.

### Calibrated per-skill range (with basis and confidence)

| Unit | Range | Basis | Confidence |
| --- | --- | --- | --- |
| New skill, read-only/design-only, no per-provider material | 2.5–4 active h | ACR, CFC, ATD, EPR, RAR estimates; wall median 3.37 h per PR is the same order | low (never scored) |
| New skill with per-provider references or manual-only refusal design | 3–5 active h | TTP, HITL, CSBR, DBV estimates | low |
| Extension | 0.75–2 | six precedent estimates | low |
| Drop / covered note | 0–0.25 | precedent | medium (trivial) |
| Batch overhead (decision row, registration, reciprocity, census) | 1–3.5 per batch | four precedents | low |
| Seven-stage allowance per PR (not in any precedent estimate) | +1–2 agent-h | FU-1 floor of 1.81 h non-implementation stage time; skill PRs already had 2–3 review agents in D68–D71, so not all of it is new | very low (n=1, docs PR) |

Derived, so labelled: under today's process a new-skill PR is about 3.5–7 agent-hours including its own stage overhead, an extension about 1.75–4. Unmeasured items still excluded: readability follow-up rounds, rebase re-reviews from count-marker collisions, and any baseline-refresh PR (needs its own grant).

**Recommendation for the plan page:** state per-candidate estimates with this table as the basis, say explicitly that no precedent estimate has been scored against active time, and record start/finish timestamps for each build PR so that the next batch can score them (metrics rule `aegis-execution-metrics.md:54-60`).

## (c) What the owner-requested "store these plans in the repo's backlog" PR must contain

### By precedent (verified)

- Precedent batch-proposal PRs changed **exactly one file**: #492, #494, #495, #496 (REST file lists). The earlier feature-flag proposal #378 also changed `docs/README.md` (+3) and the readability ledger (+22).
- Path and name: `docs/roadmaps/<scope>-skill-batch-proposal.md` (4 such pages on main: `git ls-tree … | grep -c 'skill-batch-proposal\.md$'` = 4).
- Banner, verbatim from all four (e.g. `qa-tier1-skill-batch-proposal.md:3-5`): "> **Status:** Proposal only, waiting for an owner decision. This page grants no authority and builds nothing. No skill, evaluation file, catalog row or decision-log row was created or changed by the pull request that adds it."
- Prepared-from line: "Prepared 2026-10-08 from `ModernNomad-98/Project-Aegis` `origin/main` at `<sha>`, where `python -B scripts/validate-skills.py` reported 195 valid skills." (195 measured at `52289779`.)
- Section order used by all four: Terms used on this page → Decision in one read (table: candidate (roadmap row) | recommendation | manual-only? | active hours (provisional), with a batch-overhead row and a total; then a sentence comparing with the forecast's range) → one section per candidate (roadmap text, purpose, claimed gap, what shipped skills already do with quoted descriptions, boundary table, recommendation, manual-only, draft description measured with `yaml.safe_load`, ROUTE-002 edits, evals, estimate) → Batch summary (recommended set, suggested PRs, total, review path, provisional decision number, expected ROUTE-002 census) → What the owner must answer (one reply answers all, recommended options marked) → What this page does not do (grants nothing; "Checked for this proposal" and "Not checked" lists).
- Decision number: write "would be recorded as **D74**; D73 is the highest on main at `<sha>` and no page mentions D74; recheck at decision time" (D70/D71 renumbering precedent).

### Paths: gate-guard and security surface

- The gate-guard regex (`.github/workflows/validate-skills.yml:528`), run with `nocasematch` on the candidate paths: `docs/roadmaps/<new page>.md`, `aegis-open-decisions-2026-09-23.md`, `aegis-backlog-forecast.md`, the readability ledger, `docs/README.md`, `docs/skills-catalog.md`, the approval register and the reconciliation log all **not matched**; `scripts/validate-skills.py` matched (control). `gate-guard` will pass.
- Security-relevant surfaces (`CONTRIBUTING.md:238-251`) do not include `docs/roadmaps/` or `docs/README.md`; the approval register IS on the list. Answer: **No**, provided the register is not touched. (MG5's extra review applies to outside contributions only in any case.)
- CI checks that do apply: the Markdown link checker runs over every tracked `.md` (`validate-skills.yml:219-227`), so every relative link and anchor in the new page must resolve (heading anchors with backticks and `#` numbers need care); `changes`, `validate-skills`, `gate-guard` run on every PR (PR template checklist).

### What must NOT be in it

- No edit to `docs/skills-catalog.md` (C3: its hash is in the refreshed baselines; precedent banner says no catalog row).
- No D-entry in the reconciliation log and no open-decisions "Decided" row (nothing is decided; precedent puts these in the decision PR).
- No approval-register entry. Nothing is granted; the merge authority is the owner's verbatim answer recorded in `$S/skillbatch/BRIEF.md` ("Yes, same terms (Recommended)"), which `AGENTS.md` accepts for `MG4` ("the owner's instruction quoted verbatim in its brief with its source"). A register edit would also flip the security answer to Yes.
- No `.claude/skills/`, README, `docs/paths/` or forecast-figure change; no baseline regeneration.

### Backlog pointer options (choice)

| Option | Files | For | Against |
| --- | --- | --- | --- |
| A. Page only | 1 | exact precedent (#492–#496) | weaker literal fit to "store in the repo's backlog"; nothing in a backlog list points at it |
| **B. Page + one bullet under open-decisions "Owner-requested backlog items"** (recommended) | 2 | that section is the repository's designated list ("These items are in the backlog at the owner's request. Listing one here does not authorize its implementation.", `aegis-open-decisions-2026-09-23.md:243-246`); precedents: the feature-flag item and the paused readability program the owner asked to "turn … into a low priority backlog item" (feature-flag bullet :248; paused readability item :277) | one more page touched; keep the bullet ≤ 10 net lines and add no section so an independent targeted review retains any existing acceptance (ledger :2890-2899) |
| C. B + dated note in the forecast | 3 | forecast is the backlog's quantity record | forecast changes happen at five-merge checkpoints or on a material owner decision (metrics :66-69); storing a proposal is neither; 4,709-line page |
| D. Any option + `docs/README.md` line | +1 | #378 precedent | the index lists none of the four batch proposals (`docs/README.md:74-90`), so one line would be inconsistent unless all four are back-filled (scope creep) |

### Readability-ledger effects

- Tracked Markdown goes 675 → 676 (`git ls-tree -r --name-only origin/main | grep -c '\.md$'` = 675); the link-checked set 619 → 620 (floor guard 600).
- The new page starts **pending** (ledger :730) unless an independent full-page review against "Acceptance for each page" passes and a ledger keeper (APR-101; not the author, not the reviewer, not the coordinator) records it. Precedent: the four proposals were accepted by independent full-page reads during their PRs and recorded in later ledger PRs (ledger :2985-2987). The PR body must name the pages reviewed and still pending (`CONTRIBUTING.md:134-137`).
- The acceptance index (`tools/readability_acceptance/`) does not list pages added after it was built (ledger :50-53) and its repair program is paused; nothing to do there.

### PR body and metrics obligations

Plan with proportionate acceptance criteria; audited plan revision hash; "Aegis skills used" table; security answer "No"; 8-row reconciliation witness (all `unchanged-and-verified` for a page that does not touch `delivery-workflow.md` or `AGENTS.md`); DCO sign-off; bound-field marker lines kept. Per `aegis-execution-metrics.md:54-60` and `AGENTS.md`'s timing preference: previously published ETA (none), the item's own ETA, the entire-backlog figures (selected 71–146, no finite total; unselected expansion 68–140), start/finish timestamps and measured wall time.

### Page-design consideration (judgment, no precedent)

Precedent pages ran 548–687 lines for five candidates. The six groups hold about 37 candidates (G5 is topics). Full precedent depth for all would make one very long pending page. Options: full-depth sections only for the recommended sub-batch with one evidence row per other candidate (one page), or a page plus an evidence appendix (two pending pages). Either choice is the planner's; no repository rule decides it.

---

# PART 2 — DEMAND

## (d) Where the shipped library points at missing skills

| Source | Method | Result |
| --- | --- | --- |
| Shipped skills (`.claude/skills/**/*.md, *.json`) | `dangling.py`: every backticked kebab token with a skill-like suffix that is not a skill directory | 5 tokens: `ai-security-red-team-reviewer` (5 hits), `secure-saas-reviewer`, `principal-architecture-reviewer` are **subagents** in `.claude/agents/` (`ls`); `orchestrator-via-product-spec-writer` is an attribution placeholder (`project-orchestrator/references/project-state-template.md:157`); `validation-gate` is a CI check name (`sharded-validation-with-resume/references/shard-runner-design.md:86`). **0 references to a missing skill.** |
| All six groups' names, plain text | `grep -rl` per name | 0 hits in `.claude/skills` and README for every name except `qa-closeout-reporter`: 1 hit, `screenshot-evidence-planner/evals/trigger-evals.json:25`: "The closeout report is the shipped ai-closeout-reporter … this is why a separate qa-closeout-reporter stays in the backlog." |
| `artifacts/audits/corpus-route-graph.json` (refreshed by #679) | node set vs disk; edge endpoints | 195 nodes = 195 skill dirs; 1,075 edges (694 description, 381 body); **0 dangling**. By construction it only records edges to existing skills, so it cannot show demand for a missing one. `unreferenced_skills` (10 shipped skills with no inbound edge) is a discoverability matter, not a missing-skill signal. |
| `project-orchestrator` stages 1–9 | read `SKILL.md:148-283` | The only stated missing skill: **Stage 8 GCP** — "state plainly that no dedicated GCP mapping skill exists yet and PAUSE" (`:269-272`); the managed-tier mapper is absent "by design". Outside the six groups. No stage names a six-group candidate or states a gap they would fill. |
| GitHub issues (read-only) | REST pages 1–7 of `issues?state=all` filtered to non-PRs; MCP `list_issues` (totalCount 1); MCP `search_issues` for skill topics (0) | One issue ever: #101 (reserved scope; conversational setup). **0 skill requests.** |
| Routed-elsewhere notes in shipped skills | grep for unowned/no-skill wording | `screenshot-evidence-planner/SKILL.md:33-35` routes visual-regression pixel-diff tooling to `qa-automation-architect`; `qa-strategy-architect/SKILL.md:142-144` says a strategy without manual testing leaves visual, UX and exploratory risks unowned (a rule about strategy content, not a missing skill); `compliance-control-foundation/references/common-control-set.md:33`: encryption design review "is unowned" (outside the six groups). |
| Acceptance-test findings (VolunteerFlow, `docs/audits/volunteerflow/…AEGIS-001-to-059.md`) | grep candidate topics | **AEGIS-013** (:363-374) and **AEGIS-028** (:558-568): the product spec omitted repeated-request/idempotency behaviour; required improvement: an "idempotency lens"/"idempotency matrix" (:1166). See C5: not visible in `product-spec-writer`. No finding about invitations, provisioning, visual regression, mobile, mocks, mutation, chaos or soak. |
| Planned composition | reconciliation D31 note | `command-gateway-architect` seams list "backlog components `validation-boundary-designer` / `idempotency-first-designer`" (reconciliation :639-640); the shipped skill does not name them (dangling scan) and already runs an idempotency step in its pipeline (description). |
| Usage telemetry | grep docs/evidence, docs/roadmaps | None exists; demand cannot be measured from use. |

## (e) Which candidates the evidence supports, and which it does not

**The demand evidence is structurally thin.** One issue ever, no usage telemetry, and a route graph that cannot hold dangling edges mean "no demand signal" is not "no demand". Demand can rule candidates out where a recorded rule ties building to demand; it cannot rank the rest strongly. The batch choice has to rest mainly on the group helpers' overlap verdicts and on planning priority.

| Group / candidate | Demand evidence | Planning priority (C4: planning-time only) | Verdict on demand |
| --- | --- | --- | --- |
| G3 `idempotency-first-designer` | Only observed failure in the repo's own acceptance test (AEGIS-013/-028) plus the D31 planned-component note | P0 (#17, `01-…:40`) | **Most supported**, but the observed gap is spec-level, which points to a `product-spec-writer` extension as much as a new skill; 21 shipped `SKILL.md` already mention idempotency (`command-gateway-architect` 16, `background-job-orchestration-architect` 17). Overlap check decides the shape. |
| G4 all four | No demand signal; no contrary rule | all P0 (`02-…:26-28` #57-59; `03-…:69` #127) | **Supported by priority only.** Strongest planning-time case among groups with no on-demand rule. |
| G3 other eight | Planned-component note for `validation-boundary-designer` only | 7×P0, `operational-runbook-author` P1 (`01-…:25-60`) | Priority-only support. Coverage pointers for whoever checks G3: `domain-modeler`'s description already lists "subdomains, bounded contexts" and its step 4 is "Draw bounded contexts" (`domain-modeler/SKILL.md:3, :55`); `architecture-designer` produces dependency maps; `api-event-architect` covers routes, versioning, idempotency; `observability-operator` (manual-only) instruments correlation IDs. |
| G1 QA Tier 2 (six) | None; visual regression is routed to `qa-automation-architect` by a shipped skill | P1 ×5 rows, #203 P2 promoted (reconciliation :250-261) | Priority-only. The forecast's "Ideally after Tier 1" (forecast :726) is satisfied: D68 delivered Tier 1. Name-adjacent shipped skills the QA-A helper must check exist: `mobile-viewport-craft`, `sharded-validation-with-resume`, `clickthrough-test-engineer`, `playwright-e2e-engineer` (`ls`). |
| G2 QA Tier 3 (four) | None | all P2; D10: "build on demand only" (reconciliation :263-270); forecast "Built on demand only" (:727) | **Not supported.** The repository's own rule makes demand the trigger, and no demand signal exists. |
| G6 `qa-closeout-reporter` | The shipped library itself says it stays in backlog because `ai-closeout-reporter` covers the closeout (`screenshot-evidence-planner/evals/trigger-evals.json:25`); catalog and forecast record the overlap | #235 P0 | **Not supported** (negative signal). |
| G6 `e2e-test-architect` | None | #187 P1; P0 only in the historical product-agnostic roadmap (:147) | Not supported by demand; priority conflicting. |
| G5 security topics | None | not examined here (SEC helper) | Not supported by demand; the forecast requires an overlap check against shipped security skills first (:730). |

## Self-scrutiny

- **Strongest counter-argument to the cost range:** the "calibrated" range is the precedent estimates restated; nothing has scored them. The wall-time median (3.37 h per new-skill PR) only shows the estimates are not wildly off in magnitude, and wall includes waits while excluding pre-commit drafting, so it could understate or overstate active time. The seven-stage allowance rests on one docs PR.
- **Strongest counter-argument to option B:** the precedent is unanimous for page-only (4 of 4 batch proposals), and adding a second page widens review. I recommend B only because the owner's words name "the repo's backlog" and the open-decisions section is the repository's own designated list; option A is fully defensible if the coordinator reads "backlog" as the `docs/roadmaps/` folder.
- **Strongest counter-argument to the demand ranking:** the only "observed" signal (VolunteerFlow) is a single July exploratory test, and its idempotency finding is about specs, not design; P0 labels are July planning tiers. A reader could fairly say the demand evidence supports no group.
- **Least certain claims:** (1) that the VolunteerFlow idempotency gap is unresolved in shipped skills (C5; searched wording may miss a fix); (2) the +1–2 h seven-stage allowance; (3) whether the open-decisions page currently holds acceptance (not derivable here; the readability count itself is "NOT DERIVABLE", ledger :53-54).
- **Coverage gap for the coordinator:** the helper re-split in `$S/skillbatch/BRIEF.md` names QA-A (G1), QA-B (G2+G6), P34 (G4), SEC (G5), MECH and DEMAND; **no helper is named for G3 (Phase 2, nine candidates, 18–36 h)**. Unverified whether another helper holds it.
- **What would change the recommendations:** measured active time from any skill build (rescales the range); an owner statement of what "backlog" means (settles A vs B); a GitHub issue, usage data or a new acceptance-test finding naming a candidate (re-ranks demand); a G3/G4 overlap verdict of COVERED (removes that priority-only support).

## What I did not do

No repository file, commit, push, PR, issue comment or other GitHub write. No overlap verdicts for G1, G2, G4, G5 or G6 (other helpers own them); G3 pointers above are pointers, not verdicts. No reserved-scope work. No register reading beyond the entries cited.
