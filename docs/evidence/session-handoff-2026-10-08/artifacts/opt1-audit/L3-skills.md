# OPT1-AUDIT — Lane L3: skills, agents, validators, consumer-copy path

- Lane: L3 (read-only audit). Repository: `/home/user/Project-Aegis`, HEAD `7d1d05e8170254ae60e8deb175c74e244a284a80` (= origin/main, #677), clean tree (`git status --porcelain | wc -l` → `0`, before and after all runs).
- Role: A, the source library. All four landmarks are present: README top line `# Project Aegis`, `docs/skills-catalog.md`, `scripts/validate-skills.py` and `artifacts/audits/skill-contract-audit-baseline.json`.
- Start: 2026-10-07T20:34:45Z. Finish: 2026-10-07T20:43:52Z (`date -u`). Measured wall time is about 9 minutes, against an ETA of 45 minutes. Active time was not measured separately, so the wall-time comparison is imperfect.
- All writes went to `…/opt1-audit/` (this file, plus `L3-run/` holding tool outputs and two helper scripts). There were no repo edits and no `--write` runs.

## Aegis skills used
- **Applied:**
  - `agent-startup-context-gate`: verified role and landmarks, HEAD and a clean tree before acting.
  - `source-of-truth-reconciler`: weighed the ledger against the index as competing authorities (question d).
  - `context-co-update-ci-gate`: assessed the possible later CI drift check.
  - `library-diff-reviewer`: checked what a library PR reviewer would flag if index churn rode along in PRs.
- **Read as audit subjects (evidence only):**
  - `docs-as-code-architect`, `docs-retention-index`, `readme-craftsman`, `api-doc-generator-designer`, `diataxis-doc-organizer`, `onboarding-doc-designer`, `skill-quality-reviewer` and `ai-closeout-reporter`.
  - The MANUAL-ONLY skills `ci-pipeline-architect` and `aegis-setup` were noted but not used.
- **No owning skill:** no skill covers "regenerate/own the readability acceptance index". That work is procedural (see F12).

## Answers in one line each
- **(a) Skill, agent, validator or baseline changes needed?** No.
  - No skill or agent text references the ledger, the index or the rule.
  - The validator and the contract audit do not read `docs/roadmaps/` or `tools/readability_acceptance/`.
  - Both pass at HEAD.
  - A later CI check **would** touch the gate-guard-protected `.github/workflows/` (see F10).
- **(b) Are consumer repositories affected?** No, unless Option 1's rule text is written into `AGENTS.md`, `CLAUDE.md` or a `SKILL.md`. Those are the only files the consumer copy carries (F5).
- **(c) Is doc editing slower, or does it need new steps?** Authors and reviewers of skill/doc PRs get no new step, provided regeneration stays a separate, single-holder PR that runs when a count is published (C3 should say so).
  - Bundling regeneration into each PR would cause merge conflicts and reviewer findings (F6).
  - A stale index miscounts skill additions and retirements (F7).
- **(d) Does existing guidance favour an option?** Yes, Option 1, through the "count with a command" and single-source/generate rules (F13). But the source-of-truth guidance requires that the ledger stop publishing its own competing count after the switch (F14 → proposed C9).

## Findings

| # | Finding | Rating | Mitigated by |
|---|---|---|---|
| F1 | 0 of 195 skills and 0 of 7 agents reference the readability ledger, the acceptance index, the 10-line rule or pending/accepted page status. The 6 "readability" hits are generic English. | NEUTRAL | — |
| F2 | `validate-skills.py` and `audit-skill-contracts.py` do not scan `docs/roadmaps/` or `tools/readability_acceptance/`. Results at HEAD: validator 195 OK / 0 warnings; audit exit 0; validator self-tests 181 pass; audit self-tests 76 pass. The only check that touches Option 1's files is the gate-job Markdown link checker, which runs over every tracked `.md`. It applies to both options. | NEUTRAL | — |
| F3 | The PR #670 rule (no cross-skill file dependencies) applies only to links that reach into another skill's internals. Option 1 adds no such link. A future skill citing `../../../tools/readability_acceptance/…` would pass the validator but not resolve in a consumer copy. | NEUTRAL (RISK if violated) | proposed C7 |
| F4 | `artifacts/audits/*.json` baselines are frozen at `5dbf7bc9` (186 skills, 316 findings); the live run gives 195 skills and 339 findings. This drift is pre-existing and not gated. The baseline file is a role landmark asserted by `test_validator.py`. Option 1 touches none of this. | NEUTRAL | — |
| F5 | The consumer copy is an allow-list: per skill, `SKILL.md` plus `references/`, `assets/` and `scripts/`, with optional `CLAUDE.md` and `AGENTS.md`. `tools/`, `docs/roadmaps/` and `artifacts/` are never copied, and `AGENTS.md`/`CLAUDE.md` contain 0 readability references. Leakage happens only if the rule is written into a copied file. | NEUTRAL (RISK) | proposed C6 |
| F6 | Skill pages dominate the readability surface: 373 of 602 index rows and 172 of 212 provably-pending pages (142 of them `SKILL.md`). The 10-line rule already applies under both options. If regeneration rides in each docs/skill PR, the risks are: <br>• `acceptance-index.json` (8,543 lines, 350,376 bytes, with `source_revision` rewritten on every build) conflicts across parallel lanes; <br>• `library-diff-reviewer` Area 3 flags "generated … files smuggled into the diff". <br>The mechanical cost is small (`build --report` 3.3 s, `check_index` 9.1 s). The cost is in the process. | SLOWS (avoidable) | C3, if C3 specifies a separate single-holder PR run at publish time |
| F7 | `check_index.py` loops only over the index's rows and never compares them with the pages tracked at `--ref`. The committed index (`d6e48418`, 53 commits behind) misses 7 reader pages, including `docs/delivery-workflow.md`. A retired or renamed skill left in a stale index counts as pending: `git diff --numstat 8b471c3a^ HEAD -- .claude/skills/system-prompt-leakage-reviewer/SKILL.md` → `0 175`. New skills are invisible until the index is rebuilt. Measured since 2026-09-30: 11 of 101 PR merges added, deleted or renamed a `.md`; 10 touched `.claude/skills`. | RISK | proposed C8 |
| F8 | The rebuild depends on which clone runs it. Building at HEAD in this clone drops 6 stated acceptances for the `cloud-security-baseline-reviewer` pages ("STATED DROPPED (revision unresolved) `65bacc7`"), so those rows become "no recorded acceptance". The committed index lists them as unreachable/cannot_decide. `database-backup-verifier/SKILL.md` changes from `d3dcb62` to `a8906694`. All 7 lost-acceptance rows are skill pages, and C4 cannot restore them. | RISK | C5, plus proposed C10 |
| F9 | C4's "tag" does not meet the tool's reachability rule. Reachability is `git for-each-ref --contains <sha> refs/remotes/` (`build_index.py:78-85, 224-225`; `check_index.py:59, 124-125`), and tags live in `refs/tags/`. Not reproduced: across the committed index's 39 resolvable acceptance revisions and a HEAD build's 40, every one is an ancestor of origin/main, so there are **0 side-branch-only** revisions. | RISK | amend C4 |
| F10 | A later CI drift check has these costs: <br>• `.github/workflows/` is protected by gate-guard: a red required check, then manual owner merge; <br>• tools code may not run in gate jobs, and the advisory tools jobs are path-scoped to `^tools/`, so they skip the docs/skill PRs that cause drift; <br>• `tools-tests-linux` uses a shallow checkout (no `fetch-depth: 0`), so every row would be undecidable; <br>• the owning design skill `ci-pipeline-architect` is MANUAL-ONLY; <br>• the tool's 7 unit tests are not run by CI today. | RISK / SLOWS (later step) | new condition at extension time |
| F11 | `RULE_LINES` hard-codes the rule at tracker L2484-2493. At HEAD the rule text is at L2776 (it was L2487 at `d6e48418`). `verify_rule_lines` checks only that the end line is ≤ the file length. Ledger edits under C2 silently invalidate the citations. This is cross-lane (tools). | RISK | C5 |
| F12 | All 7 agents are read-only (`Read, Grep, Glob`); the validator hard-fails any widening, and gate-guard protects `.claude/agents/`. C3's named role therefore cannot be an agent definition: it must be a coding-agent lane or a human. | NEUTRAL | C3 wording |
| F13 | Existing guidance favours a count derived by command from a source record: `AGENTS.md:51`, `CONTRIBUTING.md:138`, `api-doc-generator-designer:83-87`, `readme-craftsman:89,145`, `docs-as-code-architect:160-165`, `ai-closeout-reporter:112`. | HELPS (Option 1) | — |
| F14 | Guidance on two competing authorities: `source-of-truth-reconciler:131-135` (two canonical claims, and generated artifacts double-counting their input) and `docs-retention-index:181-183` (an index that drifts from its docs is two sources of truth). If the ledger keeps stating a hand-made pending figure, there are two published counts. | RISK | proposed C9 |

## Proposed conditions (added to C1–C5)
- **C6:** Write Option 1's rule only in Role-A-only pages: `CONTRIBUTING.md`, the ledger, `docs/delivery-workflow.md` and the tool README. If it must go in `AGENTS.md`, scope it explicitly to Role A. Never put it in a `SKILL.md` or `CLAUDE.md`.
- **C7:** No skill or agent cites the ledger, the index or `tools/readability_acceptance/`.
- **C8:** `check_index.py` refuses to produce an official figure (exits non-zero) when the index's page set differs from the reader pages tracked at `--ref`. Alternatively, C3 requires a rebuild immediately before every published count. The rebuild runs as its own single-holder PR, never inside docs or skill PRs.
- **C9:** After the switch, the ledger publishes no independent pending figure. It cites `check_index` output at a named ref, and it records which source governs: the index count is official, and the ledger is the input record.
- **C10:** The C5 review requires byte-identical rebuilds from two fresh clones of the canonical remote. The 7 lost-acceptance skill pages need either a fresh full-page review or an explicit "pending" record.
- **Amend C4:** Preserve the acceptance commits on a remote branch (which appears under `refs/remotes/` in clones). Otherwise widen the probe to include `refs/tags/` and fetch tags; that is a tool change, and it needs review.

## Option 2 costs (L3 view)
Option 2 also needs no skill or validator change. Its costs:
- The figure is a hand-made count, which conflicts with `AGENTS.md:51` and `CONTRIBUTING.md:138`.
- The ledger keeper must notice skill edits by hand. Skill edits account for 81% of provably-pending pages, and about 10 skill PR merges landed in the last week.
- The hand figures have already needed reconciliation once (#677).
- The keeper's time per figure is unknown.

## Evidence (commands → output excerpts)
- **Searches over skills and agents:**
  - `grep -rlniE 'readability|acceptance[-_ ]index|readability_acceptance|readability-backlog|…' .claude/skills .claude/agents` → 6 generic hits (`tenant-modeler:93`, `code-simplifier/references`, `gated-deployment-prompt-template/references`, three eval prompts).
  - The 10-line-rule and pending/accepted-page searches → 0 relevant hits.
  - `grep -ciE readability AGENTS.md CLAUDE.md` → `0`, `0`.
- **Validator and audit runs:**
  - `python3 -B scripts/validate-skills.py` → `OK: 195 skill(s) valid, 0 warning(s)`, exit 0.
  - `python3 -B scripts/audit-skill-contracts.py --json/--markdown/--graph/--manifest <scratch>` → `findings: 339 (P0 2, P1 82, P2 0, info 255)`, exit 0. Baseline summary: `repo_sha 5dbf7bc9…`, `skill_count 186`, `finding_count 316`.
  - `scripts/tests/test_validator.py` → `OK: 181 …`.
  - `scripts/tests/test_audit_skill_contracts.py` → `OK: 76 …`.
  - `python -B -m unittest discover -s tools/readability_acceptance/tests` → `Ran 7 tests … OK`.
- **Index build and check:**
  - `build_index.py --report` → exit 0 in 3.34 s; `reader_pages 609`, `stated_candidates 13`; 6 × `STATED DROPPED (revision unresolved) … 65bacc7`.
  - `check_index.py --json` → exit 0 in 9.13 s; `provably_pending 212`, `no_recorded_acceptance 159`, `cannot_decide_unreachable_acceptance 7`.
  - Pending paths split: 172 under `.claude/skills/` (142 `SKILL.md`), 0 under agents.
  - Index row split: 373 skill rows and 7 agent rows out of 602.
  - Committed index `source_revision d6e48418…`; `git rev-list --count d6e48418..HEAD` → `53`.
  - `git cat-file -t 65bacc7d6b85` / `d3dcb62a335d` → `Not a valid object name`.
- **Consumer copy and CI:**
  - `README.md:388-391, 417-420, 438-444, 463-467, 521-530, 559-567` (allow-list and dependency notes).
  - `.github/workflows/validate-skills.yml`:
    - `:37-42` gate isolation;
    - `:94-98` the `^tools/` path filter;
    - `:361, 373-374` tools-tests checkout with no `fetch-depth`;
    - `:186-224` link checker over all `.md`;
    - `:467-600` gate-guard, whose pattern includes `.github/workflows/`, `.claude/agents` and `scripts/` but not `tools/readability_acceptance/`.
  - `grep -rli readability .github` → none.
- **Rule location in the ledger:** `grep -n 'more than 10 changed lines'` gives HEAD L345 and L2776, and `d6e48418` L56 and L2487. `wc -l` on the ledger gives 3,836 newlines. The brief says "~3,950"; the difference is minor.
- **Merge-rate sample (approximate):** first-parent PR merges since 2026-09-30, counted by `(#NNN)` subjects → 101 total; 11 added, deleted or renamed a `.md`; 10 touched `.claude/skills/`.

## Not checked
- Ledger content and the correctness of the harvester's blind spots: other lanes.
- Whether the brief's "side-branch-only" acceptances exist in a repaired harvester's set. Not derivable from current code.
- Live skill behaviour in a fresh session, and real consumer repos (the consumer-copy findings are static analysis of the allow-list).
- GitHub-side PR-comment acceptances, Windows CI, and how GitHub forks behave (unverified).
- The ledger keeper's per-update time.
