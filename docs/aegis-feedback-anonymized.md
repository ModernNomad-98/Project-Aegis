# Feedback log — anonymized

Anonymized copy of the feedback log. Identifying details are removed: no product name, owner name, accounts, repository or file names, dates, prices, devices or vendors. Owner quotes are summarised, not reproduced. It is never sent anywhere; passing it on is the owner's decision.

Owner experience level: not recorded.

## Owner-raised

### U-1 — Work stopped while the queue was not empty
Stage: deliver. Category: autonomy.
What happened: the session marked its goal complete and posted a closing report while an actionable improvement item remained open.
Effect: the owner had to repeat the instruction; one extra cycle, not measured.
Idea: a goal may not complete while an actionable item it owns is open.
Status: fixed for the project; open as a default.

### U-2 — No feedback log was being kept
Stage: records. Category: records.
What happened: no tracker file existed; dispositions lived only in pull-request bodies and receipts.
Effect: the owner had to ask; history was harder to inspect.
Idea: create tracker files at project start.
Status: fixed for the project; open as a default.

### U-3 — A merge direction had to be repeated
Stage: deliver. Category: approvals.
What happened: a docs-only change stayed open because an advisory gate was red with a missing machine-readable input; the owner then directed the merge.
Effect: one extra cycle and an owner exception, not measured.
Idea: give the advisory gate a neutral state or a documented input format.
Status: fixed for the project by exception; open.

### U-4 — Repeated stopping
Stage: deliver. Category: autonomy.
What happened: turns ended with reports while work remained.
Effect: repeated owner prompts, not measured.
Idea: an autonomy goal with a do-not-stop rule.
Status: fixed for the project; open.

### U-5 — The same pattern a second time
Stage: deliver. Category: autonomy.
What happened: a report was posted instead of continuing; repeats U-4.
Effect: an extra owner message.
Idea: treat a report-without-work as a process failure when the queue is not empty.
Status: fixed for the project; open.

### U-6 — The agent ignored its own skill-first governance
Stage: deliver. Category: process.
What happened: an implementation was started from a brief before the matching Aegis safety skill was read; the feedback log was updated only after the owner prompted.
Effect: repeated implementation-audit rounds; record lagged the work. Not measured.
Idea: require the matching skill and source hash in the coordinator brief before build dispatch.
Status: corrected for the session; open.

## Build-session noticed

### A-1 — A scoped item was deferred instead of built
Stage: plan. Category: planning.
What happened: an improvement item was scoped into a follow-up issue instead of being delivered in the same cycle, then delivered next round.
Effect: one extra planning/review cycle.
Idea: plan a small item into the current cycle rather than opening a deferral.
Status: fixed for the project; open.

### A-2 — Plan-audit wording loops
Stage: plan. Category: review.
What happened: two changes needed five plan-audit rounds each, mostly for wording and determinacy (as reported by the build session).
Effect: audit time, not measured.
Idea: a determinacy checklist before capture.
Status: open.
Status update: fixed for the project (checklist added); open as a default.

### A-3 — An advisory gate blocks merges without a machine-readable input
Stage: deliver. Category: approvals.
What happened: a docs-only change was blocked because the advisory gate's stage declarations have no pinned machine-readable form.
Effect: an owner exception, not measured.
Idea: publish the format or record the gate as intentionally not wired.
Status: fixed for the project by exception; open.

### A-4 — Reviewers could not verify checks or hashes
Stage: review. Category: records.
What happened: reviewers' shells were blocked, so they read packet files only and the coordinator recomputed hashes and check states.
Effect: extra coordinator verification, not measured.
Idea: a machine-readable checks/hash export in the packet.
Status: open.
Status update: fixed for the project (packet tool added); the reviewers' shell limit remains.

### A-5 — New tool self-tests are not CI-wired
Stage: validate. Category: testing.
What happened: three new suites (48 tests, as reported by the build session) run only by hand; wiring them needs a protected workflow change and an owner grant.
Effect: they can be skipped without a red check.
Idea: a small workflow step for these suites.
Status: open (needs a grant).

### A-6 — Docs claimed no repository script executes while one is imported
Stage: deliver. Category: accuracy.
What happened: the docs said the tool runs no repository script, but it imports a checker in-process; a review caught it and the wording was fixed.
Effect: one review round.
Idea: describe in-process imports explicitly.
Status: fixed for the project.

### A-7 — A review verdict was not posted before the merge attempt
Stage: review. Category: records.
What happened: a review returned ACCEPT but the verdict was not posted; the merger refused because no posted head-bound verdict existed, and a second merger was needed.
Effect: one extra merger cycle, not measured.
Idea: require the posted verdict id in the merger brief and post it first.
Status: fixed for the project; open.

### A-8 — Skill-first sequencing failed while building an Aegis tool
Stage: implement. Category: process.
What happened: the adopt/doctor build began before its matching tool-safety skill was read; six or more D3 rounds then surfaced symlink, wrapper-execution, partial-write, mode and read-only defects that a tool matrix would have front-loaded.
Effect: avoidable review cycles; not measured.
Idea: a machine-checkable "skills applied" row in every build brief; fail the brief if missing.
Status: open.

## Worked well

### W-1 — Independent audits caught real defects before merge
Stage: review. Category: review.
What happened: separate reviewers caught a closure-order failure, a false docs claim and error-contract bugs before merge.
Effect: defects were fixed before merge.
Idea: keep the separate-agent audit chain.
Status: working.

### W-2 — Head-bound verdicts and fresh merger receipts made merges auditable
Stage: deliver. Category: records.
What happened: the merges in this batch carry verdicts naming the exact head and receipts naming check states and authority (as reported by the build session).
Effect: each of these merges can be re-checked from its receipt.
Idea: keep this default.
Status: working.

