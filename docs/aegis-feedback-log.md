# Aegis feedback log

**What this is.** A running record of what slowed the owner down, confused them, or cost a decision, plus what worked well. Part A is raised by the owner; Part B is noticed by the build session and is not yet confirmed by the owner. It is **not an authority record**: decisions, approvals and merges remain in their own records. Entries are added, never rewritten; a correction or Status change goes beneath the entry with the date it was made, and the original text stays.

**Owner experience level:** not recorded in this project's records. No guess is made here.

**Start:** 2026-11-20. Dates are the owner's local date (America/Los_Angeles) unless a record says otherwise. Times are omitted where the record does not retain them.

## Part A — raised by the owner

### U-1 — The agent stopped while work remained (2026-11-20)
In the owner's words: "what part of continuously and autonomously working do you not understand?"
What happened: the autonomous backlog goal was marked complete and a closing report posted while the scaffold generator was an open, actionable item (issue #1182, created by the session). Record: goal goal-e5f49066-444d-4c4b-ad52-c24deabc0dd9 (completed), issue #1182, later delivered by PR #1183 (merge 2ced1e5f).
Effect: the owner had to repeat the instruction and spend an extra cycle. Not measured.
Idea for Aegis: a goal must not be marked complete while any actionable issue created or owned by the session is still open.
Status: fixed for this project (goal re-armed; #1182 delivered). Still open for Aegis as a default rule.

### U-2 — The feedback log was not being kept (2026-11-20)
In the owner's words: "are you still tracking and updating the aegis feedback log?"
What happened: no tracker file existed in the repository or the checkpoint; review dispositions lived only in PR bodies and receipts. Record: repository search for a feedback-log file returned none; checkpoint support files contain no such log.
Effect: the owner had to ask; the process history was harder to inspect.
Idea for Aegis: create the tracker files at project start and update them in batches.
Status: fixed for this project (these four files). Open for Aegis as a default.

### U-3 — Merge direction had to be repeated (2026-11-20)
In the owner's words: "continue to push and merge as directed"
What happened: PR #1185 stayed open after the merger refused because the advisory aegis-verdict-gate was red with REQUIRED_INPUT_UNAVAILABLE; the owner then directed the merge. Record: PR #1185 comment 7056113957 and receipt 7056134282.
Effect: one extra cycle and an owner exception for a docs-only change. Not measured.
Idea for Aegis: give the advisory gate a documented neutral state or a machine-readable input, or state when it is intentionally not wired.
Status: fixed for this project (merged as 851a4dd8 under the owner exception). Open for Aegis.

### U-4 — Repeated stopping (2026-11-20)
In the owner's words: "why are you keep stopping? you're supposed to continously and autonomously work until you clear the queue and backlogs"
What happened: turns ended with status reports while actionable work remained. Record: this chat (not independently citable); the goal rounds were introduced after this message.
Effect: repeated owner prompts. Not measured.
Idea for Aegis: an autonomy goal with an explicit do-not-stop rule and automatic continuation.
Status: fixed for this project (goal rounds). Open for Aegis.

### U-5 — The same stopping pattern a second time (2026-11-20)
In the owner's words: "ok you are supposed to work autnomously" (spelling preserved)
What happened: this repeats the U-4 pattern: a report was posted instead of continuing. Record: this chat (not independently citable).
Effect: an extra owner message.
Idea for Aegis: treat a report-without-work as a process failure when the queue is not empty.
Status: fixed for this project by the continuing goal. Open for Aegis.

### U-6 — The agent ignored its own skill-first governance (2026-11-22)
In the owner's words: "that's bad, you ignored your own governance"
What happened: while building the adopt/doctor tool, the coordinator started from a brief instead of loading the matching Aegis skills first; `agent-tool-safety-guard` was only read after the owner challenged the process, and the feedback log was not updated until prompted. Record: this chat; the safety review then found repeated wrapper/path/atomicity defects.
Effect: avoidable D3 review cycles; the governance record lagged the implementation. Not measured.
Idea for Aegis: a machine-checkable coordinator brief that records the matching skill and source hash before a builder is dispatched, and blocks the dispatch when the field is absent.
Status: corrected for this session (skill read, log updated); open for Aegis.

## Part B — noticed by the build session (not owner-confirmed)

### B-001 — Scaffold generator was deferred after being scoped (2026-11-20)
In the owner's words: no direct quote; the plan was recorded in issue #1182 and delivered later.
What happened: the session opened #1182 to defer item 4 instead of building it, then delivered it in the next round (PR #1183, merge 2ced1e5f).
Effect: one extra planning and review cycle.
Idea for Aegis: when an item is small enough to plan, plan it into the current cycle rather than opening a deferral issue.
Status: fixed for this project (delivered). Open for Aegis.

### B-002 — Plan-audit wording loops (2026-11-20)
In the owner's words: no direct quote.
What happened: PR #1176 needed five plan-audit rounds and PR #1180 five, mostly for wording and determinacy, not new scope. Record: PR #1176 and PR #1180 bodies (as reported by the build session).
Effect: audit time; not measured.
Idea for Aegis: a determinacy checklist before capture (every condition stated, every step run/skip named).
Status: open for Aegis.
Status update (2026-11-20): fixed for this project — checklist added in PR #1187 (merge f37fd8f4, as reported by the build session); still open as an Aegis default.

### B-003 — Advisory gate blocks merges but has no machine-readable input (2026-11-20)
In the owner's words: no direct quote; the owner supplied the exception in U-3.
What happened: PR #1185's advisory gate returned REQUIRED_INPUT_UNAVAILABLE because its B/D/E stage declarations have no pinned machine-readable form (scripts/ci/aegis_verdict_gate_fetch.py line 116, as reported by the build session). Record: PR #1185 comments.
Effect: an owner exception for a docs-only merge.
Idea for Aegis: publish the stage-declaration format, or record the gate as intentionally not wired and neutral.
Status: fixed for Aegis by PR #1199 (merge 47cc2f9e, 2026-11-21): the gate is skipped by default, publishes no status/evidence and is never required. Option C remains deferred pending T6/T24/T23/T4.

### B-004 — Final reviewers could not verify checks or hashes (2026-11-20)
In the owner's words: no direct quote.
What happened: several Stage F reviewers reported that the sandbox blocked shell, git, grep and glob, so they read the packet files only; the coordinator recomputed hashes and check states. Record: Stage F comments on PRs #1177, #1179, #1181 and #1183 (as reported by the build session).
Effect: extra coordinator verification; not measured.
Idea for Aegis: put a machine-readable checks/hash export in the review packet.
Status: open for Aegis.
Status update (2026-11-20): fixed for this project — packet tool in PR #1188 (merge d525a2b9, as reported by the build session); the reviewers' shell limit remains an environment constraint.

### B-005 — New tool self-tests are not CI-wired (2026-11-20)
In the owner's words: no direct quote.
What happened: the ancestry, evidence-pack and scaffold suites (13+16+19 = 48 tests, as reported by the build session) run only by hand; wiring them needs a protected .github change and an owner grant. Record: docs/offline-ci.md and the three test files.
Effect: the tests can be skipped without a red check.
Idea for Aegis: a small workflow step for these suites.
Status: fixed by PR #1198 (merge b659e670): local-tool-tests runs the 48 ancestry/evidence-pack/scaffold tests. The newer run-record/adopt suites remain unwired (B-011).

### B-006 — Docs claimed no repository script executes while one is imported (2026-11-20)
In the owner's words: no direct quote.
What happened: the evidence-pack docs said the tool runs no repository script, but it imports scripts/check-manifest-ancestry.py in-process. D3 caught it on PR #1181; the wording was corrected.
Effect: one review round; the false claim would have misled reviewers.
Idea for Aegis: describe in-process imports explicitly in tool docs.
Status: fixed for this project.

### B-007 — The Stage F verdict was not posted before the merger was dispatched (2026-11-20)
In the owner's words: no direct quote.
What happened: on the tracker PR #1186 the Stage F review returned ACCEPT but the verdict comment was not posted; the merger correctly refused because no posted head-bound verdict existed, and a second merger was needed. Record: PR #1186 comments (as reported by the build session).
Effect: one extra merger cycle. Not measured.
Idea for Aegis: the merger brief must require the posted Stage F comment id, and the coordinator must post the verdict before dispatching it.
Status: fixed for this project (verdict posted, then merged 46bd3b40). Open for Aegis.

### B-008 — Sessions started without knowing Aegis existed (2026-11-21)
In the owner's words: "I just had two instance that didn't even know aegis existed anywhere."
What happened: two build sessions began in repositories that use Aegis but did not load it; the exact hosts/directories were not supplied. Aegis has no adoption marker or startup doctor; discovery relies on the host reading AGENTS.md/CLAUDE.md or .claude/skills.
Effect: sessions miss the skills entirely; not measured.
Idea for Aegis: one-command adopt writes .aegis/project.json, START-HERE, wrappers and startup blocks; doctor verifies them. Hosts that ignore startup files remain instruction-only, not enforced.
Status: fixed by PR #1205 (merge 21d16ce6): adopt/doctor/unadopt merged; doctor verifies the startup contract. Instruction-only: hosts that ignore startup files still miss Aegis.

### B-009 — Run Record needed a human command at every stage (2026-11-22)
In the owner's words: "that's manual as fuck, who's going to remember that at every stage?"
What happened: v1 required init/event/artifact/finish/export by hand at each stage. Fixed by sync/watch/hook (PR #1202, merge 3d4f779d) and the project-orchestrator call after confirmed project-state writes (PR #1203, merge 5aec94e3), with an explicit UNRUN fallback.
Effect: no per-stage human command when the tool is discoverable; a stock consumer still needs adopt.
Status: fixed for the source workflow; consumer adoption remains open (B-008).

### B-010 — Docs advertised a Python command that could not run (2026-11-22)
What happened: docs and the Stage B brief said `python -P -m tools.aegis_run` without PYTHONPATH; -P suppresses the current directory, so it raised ModuleNotFoundError. The correct forms are `python -m` from the Aegis root or `PYTHONPATH=<checkout> python -P -m` from elsewhere.
Effect: a reviewer following the docs would report the tool missing.
Idea for Aegis: test every documented invocation in the docs check.
Status: corrected in docs and skill text; regression test not yet wired.

### B-011 — New run-record/adopt self-tests are not CI-wired (2026-11-22)
What happened: the 72 run-record tests and 50 adopt tests run only by hand; CI's local-tool-tests covers the older 48. Wiring them needs a protected .github change and an owner grant.
Effect: regressions in the new tools can merge without a red check.
Idea for Aegis: add one local-tool-tests step for tools/aegis_run and tools/aegis_adopt.
Status: open for Aegis (needs a grant). The run-record, adopt and guard/adapter suites are also unwired (B-011).

### B-012 — Skill-first sequencing failed while building an Aegis tool (2026-11-22)
What happened: the adopt/doctor build was dispatched before its matching safety skill was read; the PR evidence table was not assembled at plan time; the feedback log was updated only after an owner prompt. D3 then surfaced symlink escape, wrapper execution, partial-write, mode-loss and read-only-target defects one at a time.
Effect: at least six extra D3 rounds that a tool-safety matrix would have front-loaded. Not measured.
Idea for Aegis: require a "skills applied" table before build dispatch and fail the brief if the matching skill row is missing; keep the feedback log as a running log, not a closing artifact.
Status: open for Aegis; the adopt PR is paused until the skill evidence is attached.

### B-013 — Enforcement stopped at L2 partial (2026-11-22)
What happened: the Claude Code 2.1.311 adapter was proven in a disposable repo: Bash, .env reads and policy writes were blocked; Read was allowed; SessionStart exit 2 did **not** block startup. Codex CLI's account rejects every tested model; Gemini is not installed; the VS Code extensions and Cursor are unqualified. There is no OS sandbox.
Effect: one L2 tool gate, not containment. A host that ignores hooks bypasses it; allowlisted commands can still run arbitrary code.
Idea for Aegis: require L3 external containment before any surface is called enforced; qualify each host/mode separately.
Status: open; L1 and L3 UNRUN.

## Worked well

### W-001 — Independent audits caught real defects before merge (2026-11-20)
What happened: D1/D3/Stage F caught the #1179 closure-order failure, the #1181 false docs claim, and the #1183 error-contract bugs. Record: D3/Stage F comments on PR #1181 and #1183 (as reported by the build session).
Effect: defects were fixed before merge.
Idea for Aegis: keep the separate-agent audit chain.
Status: working.

### W-002 — Head-bound verdicts and fresh merger receipts made merges auditable (2026-11-20)
What happened: each merged PR carries a Stage F verdict naming the exact head and a fresh merger receipt naming the check states and the authority. Record: receipts on the merged PRs in this batch, e.g. PR #1185 receipt 7056134282.
Effect: each of these merges carries a receipt that can be re-checked; example called out above.
Idea for Aegis: keep this as the default.
Status: working.