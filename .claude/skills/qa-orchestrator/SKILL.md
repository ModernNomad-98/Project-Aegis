---
name: qa-orchestrator
description: 'Conduct a complete QA pass on the user''s app — choose one fixed play (find bugs now, plan tests for a change, pre-release check, set up automated tests), name every skill it will use before starting, handle manual-only skills through the consumer''s recorded override policy, and leave ONE plain-language report plus one docs/project-state.md entry. Use when asked "help me test my app", "find the bugs", "QA this feature/release", or "set up automated tests" end to end. Do NOT use when the request is already one scoped QA skill (route straight to it), root-cause debugging/fixes (systematic-debugger, manual-only), a security scan (security-scan-orchestrator), or writing implementation/tests (the engineer skills), or a direct ship/no-ship release checklist that belongs to release-readiness-reviewer.'
---

# QA Orchestrator (the QA conductor)

Terms used below: **QA** means quality assurance; **E2E** means end-to-end; **CI** means continuous integration; **PII** means personally identifiable information. A **play** is one fixed order of skills for one user goal. **Manual-only** means a skill a human must invoke by exact name (its description starts `MANUAL-ONLY; never auto-invoke.`); the consumer overrides it only through the manual-only policy, never here. "The consumer's recorded policy" means the manual-only policy the consumer adopted and its consumer-local `docs/consumer-authority-register.md`.

## Purpose

A user who does not know the QA vocabulary needs one door: "help me test my app". This skill is that door. It asks at most four plain questions, picks exactly one of four fixed plays, names every skill it will use in order BEFORE starting, checks which of those skills are installed, handles manual-only steps through the recorded override policy, runs the play as a single test pass, and closes with ONE plain-language report plus one STATE SNAPSHOT row in `docs/project-state.md` so `project-orchestrator` can continue the journey; the report path is handed to `release-readiness-reviewer` as an evidence artifact (it does not read the state file). It runs no app itself, writes no tests, creates no accounts, fixes nothing, and never claims more than the evidence shows. One pass gives one report; a fix round is a separate, bounded activity under this skill's own exit rules.

## Use When

- Use when: the user asks to test their app, find bugs, "does this work?", QA a feature or release, or set up automated tests, and does not name a specific QA skill.
- Use when: the user is a non-developer who needs the QA work chosen and sequenced for them (guided mode), or an engineer who wants one conductor for the same plays (direct mode).
- Use when: the request spans several QA steps (e.g., "check this before release and tell me what to fix first").
- Do NOT use when: the request is exactly one scoped QA skill ("write a test plan for X", "map our test coverage", "review these acceptance criteria") — route straight to that skill; the conductor is for a user who does not know the next QA step.
- Do NOT use when: the user asks for a direct ship/no-ship decision or release checklist on a specific release ("is this ready to ship?", "check this release") — route straight to `release-readiness-reviewer`; the conductor is for a user who does not know the next QA step.
- Do NOT use when: the ask is a root-cause fix (that is `systematic-debugger`, manual-only — the conductor names it and stops; it never runs it), a security scan (`security-scan-orchestrator`), a code review (`code-reviewer`/`security-pr-reviewer`), or writing implementation/tests outside a play's engineer step.
- Do NOT use when: no safe test login/data exists for a live pass and the user will not provide one — stop (see Stop Conditions) rather than probing production.
- Do NOT use when: the user wants continuous monitoring or a lasting CI service — this is a bounded pass plus a report.

## Inputs to Inspect

1. `docs/project-state.md` if present — current stage, next action, prior QA entries, and the record location the consumer uses.
2. The consumer install record (the active receipt the installer documents as current) and `docs/consumer-authority-register.md` if present — install mode, recorded manual-only policy/trigger, and any standing override.
3. What is installed: the skills present under the project's skill directory (never assume one is present), and the project's docs/tests/CI configuration.
4. The app under test: where it runs (local, preview/staging, deployed production), the build or commit, the start command if local, and which login/data are safe.
5. The change or feature under test when the user names one: the diff/commit range, acceptance criteria, and any prior QA reports.
6. The consumer's evidence conventions: where reports live, screenshot naming/masking rules, and who reads the result (`project-orchestrator`, `release-readiness-reviewer`).

## Workflow

**1. Intake — at most four questions.** Ask only: (a) what the app is and where it runs; (b) what the user wants (find bugs / plan tests / pre-release check / set up automated tests); (c) which login and data are safe to use; (d) how hands-on the user wants to be. Do not ask what you can read from the repo. In guided mode ask one at a time and confirm each answer; in direct mode accept a one-line scope and report tersely.

**2. Choose exactly one play and state the order before starting.** Print the play, every skill in it in order, which are installed, which are manual-only, and which steps are conditional. The fixed orders are in `references/play-orders.md`:
- **Play A — Find bugs now** (a running app): optional `exploratory-charter-designer` → `clickthrough-test-engineer` → `defect-triage-facilitator`; `production-safe-smoke-tester` first if the running app is deployed production.
- **Play B — Plan tests for a feature/change**: `acceptance-criteria-reviewer` only when criteria exist → `test-plan-designer` → `manual-test-case-creator` for the plan's manual items; name engineer skills without running them.
- **Play C — Check before release**: `risk-tiered-validation-selector` (depth only, never executes) -> `sharded-validation-with-resume` only when a sharded suite exists (it designs the shard map/resume machinery and never executes) -> run the selected validation tier through the project own validation command: when the project route is the manual-only `local-ci-mirror-preflight`, list it as the EXECUTION OWNER and hand it to the human under the manual-only policy (never auto-run or chain it) -> `clickthrough-test-engineer` on the changed routes -> `defect-triage-facilitator` -> `release-readiness-reviewer`; with no CI evidence the release gate must report the CI dimension MISSING and cannot claim a pass.
- **Play D — Set up or improve automated tests**: `test-coverage-mapper` -> `qa-strategy-architect` -> `qa-automation-architect` (its blueprint selects the tools/layers for THIS repo stack) -> `test-data-architect` -> `test-tenant-provisioner` (manual-only, ONLY when non-production test accounts must be created; before any engineer run that needs them) -> the engineer skill(s) the blueprint SELECTS (for example `vitest-unit-component-engineer` AND/OR `playwright-e2e-engineer`, not automatically both; name unselected ones as conditional) -> `regression-suite-curator`; a stack with no browser layer names no browser engineer.

**3. Installed-skill check.** List which play skills are present. For any absent skill, apply the repository's absent-skill rule (gate vs advisory as installed), name the exact missing skill(s), and point to the repository's selected-skills allow-list copy route (the README "Selected skills" section) as the way to get them; the documented QA pack list is a separate planned page and is not cited as existing until it ships. Never invent, substitute, or paraphrase a missing skill. If an absent skill owns a stop/gate step, stop the play (Stop Conditions).

**4. Manual-only authorization — through the recorded policy only.** For each manual-only step (clickthrough, vitest/playwright engineers, test-tenant-provisioner, systematic-debugger if named), explain in four parts: the exact skill, what it will do, the scope/target, and what it will not touch; then ask. If the consumer's recorded policy has one standing trigger-scoped override that covers this exact skill, named trigger and scope, use it — do not ask again. Otherwise the user names each skill per run; no per-invocation override is recorded (forbidden by the policy). Never chain into a manual-only skill without one of those. When recording is requested, append the policy fields (actor, exact skill, reason, named trigger, scope, date, exact head/commit where applicable, pin/version at each sync, revocation) to the consumer-local register — show the entry before writing.

**5. Run the play once.** Execute the in-scope steps; for manual-only steps, hand off to the human with exact instructions and wait. Do not fix anything during the pass. Record what ran, what did not, and why; the build/commit under test; and each defect with reproduction steps and evidence. On a deployed production system use only `production-safe-smoke-tester` checks — never writes, never real customer tenants.

**6. Class findings and choose the single next action.** Classify every finding as **BLOCKING**, **RESIDUAL**, or **NIT** using the repository delivery-workflow definitions. BLOCKING = must be fixed before the claimed gate (an unmet applicable acceptance, authorization, security or required-validation condition is always blocking). NIT = stylistic/non-behavioural. RESIDUAL = a real non-blocking defect whose impact is understood and bounded, and it may be called residual ONLY when a named human decision-maker (owner or reviewer) has a recorded disposition (finding id, head, evidence reference, classification, decision-maker, outcome) AND a follow-up backlog id; the conductor cannot manufacture either. A real non-blocking defect without that record is reported as blocking-undisposed for triage, not accepted.

**7. Bounded fix round (only if the user asks).** Nothing is fixed during the pass. If the user asks for repairs, batch the known blocking/residual repairs, hand implementation to the owning engineer skill (never implement here), then re-verify only the affected areas once. One fix round per batch; if it still fails, report and stop — do not loop.

**8. Write ONE report and, only when the state file exists, ONE record entry.** Show the report path and content to the user before writing. Write the plain-language report (Output Format). Then: if `docs/project-state.md` exists, append exactly ONE **STATE SNAPSHOT** row that follows the installed template schema (ID, Date, Current stage (plain language), Next recommended action): preserve the current lifecycle stage from the latest snapshot, put the QA result and report path in the next-action cell, and show the exact row before writing. If `docs/project-state.md` does not exist, write the report only and state in the report that no state snapshot was written because the role-B state file is absent (project-orchestrator cold-start owns its creation); never fabricate a stage or create a second record location. Use only a current-session instruction that explicitly authorizes the documentation recording, or obtain content-specific single-use approval first — a business answer alone is not an instruction to persist a document. Never use a different entry type or transcribe an approval the human did not give.

## Output Format

```
QA REPORT — <app / feature> @ <build|commit> — <date>
Mode: guided | direct        Play: A | B | C | D
Skills used (in order): <name — installed | manual-only — ran | handed to human>
Not used / unavailable: <skill — why, and what is UNKNOWN as a result>
Tested: <what was tested, with entry paths and test data (no secrets)>
Not tested: <what was not, and why — capability gap vs scope decision>
Findings (one per defect):
  [BLOCKING|RESIDUAL|NIT] <finding id> — <title>
    Steps: <numbered reproduction>
    Expected: <...>   Actual: <...>
    Evidence: <report/screenshot reference under the consumer's evidence conventions>
Fix rounds: <none | one — affected re-verification result>
Next action: <the single most important next step>
Handoff: project-orchestrator next stage | release-readiness-reviewer evidence | owner
```
Then, only if docs/project-state.md exists, exactly one STATE SNAPSHOT row: | <QA id> | <date> | <current stage preserved> | QA pass result + report path; single next action | — no second record, no invented stage or approval. If the file is absent, the report states that no state row was written and why.

## Validation Checklist

- [ ] At most four intake questions; each needed fact read from the repo instead when possible.
- [ ] Exactly one play chosen; every skill named in order BEFORE starting; manual-only and conditional steps marked.
- [ ] Installed skills checked; absent skills follow the absent-skill rule and name the exact missing skill(s) plus the selected-skills copy route (no invented QA pack); no substitution.
- [ ] Every manual-only step has a valid recorded override or the user named that skill; nothing chained.
- [ ] One pass, one report; no fixes during the pass; at most one bounded fix round if requested.
- [ ] Findings classed blocking/residual/nit; a residual has a named decision-maker, recorded disposition fields (finding id, head, evidence, outcome) and a follow-up backlog id; undisposed non-blocking defects are reported as blocking-undisposed.
- [ ] Play C ran the selected validation tier through the project ownership route (manual-only local-ci-mirror-preflight handed to the human when that is the route; no CI evidence reported as MISSING).
- [ ] Play D provisioned non-production test accounts before engineer runs that need them, and invoked only the engineer skills the automation blueprint selected.
- [ ] If docs/project-state.md exists, exactly one STATE SNAPSHOT row follows the template schema with the current stage preserved; if absent, the report says no state row was written and why.
- [ ] Production only through `production-safe-smoke-tester`; test accounts/data only; build/commit recorded.
- [ ] Report and the single project-state entry shown before writing and written only under existing authority.
- [ ] No claim of host support, independence, or a successful run beyond what the evidence shows.

## Gotchas

- "Test everything" is not a play. If the goal matches none of A-D, ask one scoping question; do not invent a fifth order.
- A missing skill is not an invitation to improvise: name the exact missing skill and the selected-skills copy route, and if the absent skill owns a gate, stop. The documented QA pack list is a separate planned page, not an existing recovery route.
- A manual-only skill named in the report is not authorization: without a valid override (or per-run naming) it is not run.
- "Zero findings" from a pass whose browser step silently failed is a false green — record the capability gap and say what is UNKNOWN.
- Fixing during a test pass invalidates the pass; classify, report, and only then consider the one bounded fix round.
- Production smoke checks are read-only probes; seeded fixtures are not production data, and a real customer tenant is never a test target.
- The report is the evidence, the state entry is the pointer — never duplicate the report inside `docs/project-state.md`.
- Independence: the testing session should not be the session that wrote the change; if the host cannot provide a fresh session, say so and claim no independent verification.

## Stop Conditions

- No safe test login or test data, and the user will not provide one → stop; do not probe production with real credentials.
- The play needs a production write, a real customer tenant, or destructive action → refuse; route to the human owner.
- A manual-only step is needed and there is no valid override and the user has not named the exact skill → stop and ask; never simulate it.
- A play skill is absent AND owns a stop/gate step -> stop, name the exact missing skill plus the selected-skills copy route, and do not continue the play without it.
- The user asks for a direct ship/no-ship gate or release checklist -> hand to `release-readiness-reviewer`; this conductor does not replace that gate.
- A real non-blocking defect needs a residual disposition or follow-up backlog id that only the owner/reviewer can record -> stop and ask; never accept it unilaterally.
- The host cannot drive a browser where the play needs one → switch to written manual cases (a person runs them) and say so; no claim of the browser route.
- The one bounded fix round still fails the affected re-verification, or a new blocking defect appears → report and stop; do not loop.
- The user asks the conductor to run root-cause debugging, security scanning, code review, or to write implementation/tests itself → hand to the owning skill; this skill orchestrates QA only.

## Supporting Files

- `references/play-orders.md` — the four fixed orders with conditional steps, fallback route, manual-only/conditional companions, and the no-CI correction.
- `evals/evals.json` — behavior cases: guided Play A happy path; direct Play C with missing CI evidence; should-not-do cases (auto-chain a manual-only skill; fix in the pass; claim host support without a run).
- `evals/trigger-evals.json` — discrimination against `project-orchestrator` (journey vs QA pass), `qa-strategy-architect` (strategy vs play), `test-plan-designer` (single plan request), `security-scan-orchestrator` (security scan), and `systematic-debugger` (root cause, manual-only).
