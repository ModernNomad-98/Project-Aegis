# Aegis feedback log

Purpose: the record this project keeps for the next Aegis improvement cycle — what went wrong and what worked, so improvements are based on evidence rather than memory.

Rules: Part A entries are raised by the owner. Part B entries are noticed by the build session and not yet confirmed by the owner (the owner may move an entry to Part A or strike it). Entries are added, never rewritten; a later correction goes beneath the entry with its own date. Each statement carries the record it comes from; anything not recorded says so. No personal data in this file.

Entry index: owner-raised U-1..U-4; build-session A-1..A-12 (one "Worked well" class: A-8, A-9).

---

## Part A — raised by the owner

### U-1 — Scope: keep work to the project repository and report anything else (2026-11-14)
- In the owner's words: "only work on aegis repository, anything else ignore and inform me"
- What happened: while locating the missing audit evidence, the build session had searched several host locations outside the project repository (read-only: the user Downloads folder, C:\temp and C:\tmp). The owner then limited the working scope to the Aegis repository and asked to be informed of anything else.
- Effect: not measured; the out-of-repository searches were stopped and remained read-only.
- Idea for Aegis: resume/preflight guidance should limit evidence search to the checkpoint's declared paths, and any broader host search should require an explicit owner instruction recorded in the preflight.
- Status: fixed for this project (scope limited; evidence supplied at the declared location). Still open for Aegis: resume templates still invite broad "locate the evidence" searching.

### U-2 — Work in parallel, cost-efficiently, and merge when ready (2026-11-14)
- In the owner's words: "work in parallel locally with separate workstream and separate worktrees. Push and merge when ready as long as it doesn't conflict and cause a re-run of CI. Push and merge as cost effective and efficient as possible. Group small fixes into one PR to save on cost" and "show your goal and todo"
- What happened: the build session had been executing the three-PR delivery serially with one working tree. After this instruction it created one worktree and branch per PR (pr-a, pr-b, pr-c), ran plan audits and validations in parallel, and later added agents for a second workstream.
- Effect: not measured. Parallelism increased agent count and conversation length; the merge-authority change required a clarification question (see U-3).
- Idea for Aegis: default to one worktree per independent PR when a delivery splits into independent PRs, and require an explicit merge-authority sentence at intake (including whether agent merges are allowed).
- Status: adopted for this project (worktrees and parallel audits in use). Still open for Aegis: templates do not express the parallel/cost default.

### U-3 — Merge authority changed mid-flight (2026-11-14)
- In the owner's words: earlier "Merging: open the PRs and stop. Do not merge, not even under SDP-2. I will merge."; later "Push and merge when ready as long as it doesn't conflict and cause a re-run of CI"; asked which applied, the owner selected "Authorize me to merge" (merge gated on reviews/validation passing, CI green, no conflict or CI re-run) and "Keep three separate PRs".
- What happened: the two owner statements conflicted; the build session paused and asked before any merge. No merge happened before the answer. The answer also kept the three-PR structure.
- Effect: one extra owner question and a blocked merge decision; no merge attempted without authority.
- Idea for Aegis: record merge authority as an owner decision with a change protocol (who may change it, how the change is recorded) so later messages can supersede it explicitly rather than by inference.
- Status: resolved for this PR set (merge authorized under gates). Still open for Aegis: no standing field for merge authority in the delivery record.

### U-4 — Audit evidence package missing at the declared locations (2026-11-14)
- In the owner's words: "Confirmed. The audit package is still absent, so P0 remains blocked at preflight." then later "[download path redacted for privacy] unzip and find it"
- What happened: the checkpoint's declared audit-evidence roots were absent, and a bounded host search found no report file. The owner then supplied the package as a zip in the user Downloads folder (zip timestamp 19:23:28 PST); the build session extracted it, verified every bound artifact hash against its plan-binding file, and ran the closures.
- Effect: measured — about 13 minutes between the zip being observed and full extraction/verification, after the task had already been blocked at preflight from the checkpoint time.
- Idea for Aegis: the checkpoint/save template should record how evidence will be delivered (path and form) and the preflight should check the delivery folder before declaring the task blocked.
- Status: fixed for this project (package verified and used). Still open for Aegis: checkpoints do not carry evidence delivery instructions.

---

## Part B — noticed by the build session (not yet confirmed by the owner)

### A-1 — Closure was satisfiable by a neighbouring marker, not its own (2026-11-14)
- In the owner's words: not recorded (raised by an independent plan audit, not by the owner).
- What happened: the first PR-A plan relied on the closure's one-line tolerance: it counted routes as marked when a different skill's manual-only note happened to sit within one line. The independent plan audit rejected this; the plan was revised to give all 68 absent-name routes their own marker. Records: PR-A plan audit round 1 (MAJOR-1), plan r2 disposition table, closure A-08.
- Effect: one extra plan revision round (plan r1 audit 20:18 PST to plan r2 freeze 20:34-20:52 PST).
- Idea for Aegis: write "own-line marker" into such closures instead of a one-line window, and make the judgement step machine-checkable so audits do not have to reverse-engineer intent.
- Status: fixed for this project (plan r2 + round-3 wording). Still open for Aegis: closure definitions use proximity windows.

### A-2 — The PR body was a pre-push draft at final review time (2026-11-14)
- In the owner's words: not recorded.
- What happened: the PR body drafted before the pull request existed said "no pull request has been opened", "CI: UNRUN" and "no automated review" while PR #1095 was open with check results and automated reviews. The Stage F reviewer rejected the body as stale (MAJOR-1).
- Effect: one extra review round; the body had to be regenerated against live facts.
- Idea for Aegis: generate the PR body after the branch is pushed and CI has run, or make the body template require live-fact fields that cannot be filled before the PR exists.
- Status: fixed for this project (body refreshed and re-bound). Still open for Aegis.

### A-3 — No stage agent had authored its own skills-table row (2026-11-14)
- In the owner's words: not recorded.
- What happened: the PR body's machine-checked "Aegis skills used" table requires each stage agent's own row. Stages A/C/D had not authored rows; only the plan auditors had. Fixtures: Stage F review findings, body refresh requests to the implementers and plan author. One implementer correctly reported "no skill applied".
- Effect: one extra owner-side data-collection round across agents (about 30-40 minutes of agent work) before the skills field could be completed honestly.
- Idea for Aegis: make "publish your own skills row" an explicit stage-exit deliverable, so the final body never has to chase earlier stages.
- Status: fixed for this project (rows published by their authors, gaps disclosed). Still open for Aegis.

### A-4 — A CI test pinned a line that a legitimate marker edit split (2026-11-14)
- In the owner's words: not recorded.
- What happened: PR-A added an absent-skill marker in the middle of a project-orchestrator line that a contract-audit test requires to remain a contiguous substring. Two required CI jobs failed (run 43683321634, validate-skills and windows-offline-checks; test_audit_skill_contracts line 1302). The fix moved the marker to the end of the same line without editing scripts; the pinned substring is intact and the test passes.
- Effect: one failed CI cycle (two required jobs) plus a fix commit; no merge occurred on the failed head.
- Idea for Aegis: where validators pin literal sentences, document which substrings are pinned (or strip markup before comparison), so markers can be placed predictably.
- Status: fixed for this project (marker moved; contract-audit passes). Still open for Aegis: pinned-substring tests are not discoverable from the skill/page that is being edited.

### A-5 — A known non-required check fails on every PR and blocks the merge gate definition (2026-11-14)
- In the owner's words: not recorded.
- What happened: aegis-verdict-gate fails on PR #1095 heads (run 43688728739, 18-22 s) because of a pre-existing temp-path determinism defect in its own test (documented in the audit as GV-03/RA-07/CI-04; its correction A-17 is not in the three authorized PRs). The merge gate says every applicable check must be green, so the known failure needs an explicit owner disposition. Recorded failed, never green.
- Effect: the merge decision is blocked on an owner decision; one additional question.
- Idea for Aegis: either fix the determinism defect or mark the job expected-fail/skip on the PR lane with a visible reason, so a known defect does not masquerade as a failing PR.
- Status: open for this project (owner disposition pending) and open for Aegis.

### A-6 — An interactive owner question was lost on tool timeout (2026-11-14)
- In the owner's words: not recorded.
- What happened: a structured question asking the owner to choose between finishing PR-A or pausing it, and whether to grant an exception for the known failing check, hit the tool execution deadline and no answer was recorded; the question had to be re-stated in prose.
- Effect: a decision delay; the question remains unanswered in the record.
- Idea for Aegis: harness guidance should persist interactive questions to a file before waiting, so a timeout cannot lose the question.
- Status: open for this project (question repeated in prose) and open for Aegis.

### A-7 — Long validation and agent turnaround dominated elapsed time (2026-11-14)
- In the owner's words: not recorded.
- What happened: the validator self-test suite takes about 6-11 minutes per run (observed 6m21s, 9m07s, 10m45s, 11m28s in different runs), and several stage agents took 20-40+ minutes wall time. Records: agent reports and CI timings in this session.
- Effect: not measured in owner time; it set the pace of the whole delivery.
- Idea for Aegis: cache or parallelise the long suite, and add a "start the long validation early in the background" step to the delivery guidance.
- Status: open for Aegis.

### A-8 — Worked well: independent stage agents caught real defects before merge (2026-11-14)
- In the owner's words: not recorded.
- What happened: separate agents for plan audit, implementation audit, validation and final review caught: closure window-gaming (A-1), stale pre-push body (A-2), contract self-contradictions, a CI pin break (A-4), and missing skills rows (A-3). No defect found by these stages was shipped or merged.
- Effect: positive; it cost review rounds but prevented an unsound contract from merging.
- Idea for Aegis: keep the different-agent stage separation; it is doing real work, not ceremony.
- Status: working well in this project; keep for Aegis.

### A-9 — Worked well: checkpoint/resume preserved state across a long session (2026-11-14)
- In the owner's words: not recorded.
- What happened: the checkpoint's recorded revision, clean-worktree exception (one preserved untracked file), audit-package identity and readability counts all matched on resume; pre-existing work (the untracked file, branches, worktrees, tags) was preserved throughout.
- Effect: positive; no lost work and no rework of accepted prior batches.
- Idea for Aegis: keep the preservation checklist and the "do not delete unknown work" rule in the save template.
- Status: working well; keep.

### A-10 — An unknown worktree appeared and cost investigation (2026-11-14)
- In the owner's words: not recorded.
- What happened: a worktree and branch not created by the build session appeared in the repository (a custody-named worktree at 19:36:34 PST). It was preserved and reported to the owner; its origin is not recorded.
- Effect: a few minutes of investigation and one owner notice.
- Idea for Aegis: save/resume should list worktrees created by other sessions and label them, so an agent does not treat them as its own or delete them.
- Status: open for Aegis.

### A-11 — Resume claimed twelve inactive teammates; none were present (2026-11-14)
- In the owner's words: not recorded.
- What happened: the saved checkpoint said twelve teammates were inactive and available, but the resumed session listed none; the build session had to plan for spawning fresh agents. The checkpoint had not recorded a verified availability check.
- Effect: not measured; it changed staffing assumptions at resume.
- Idea for Aegis: record verified agent availability (a listed status) in the checkpoint instead of an assumed roster.
- Status: open for Aegis.

### A-12 — Automated reviews multiplied across heads and doubled the disposition burden (2026-11-14)
- In the owner's words: not recorded.
- What happened: PR #1095 collected three automated review bodies plus inline comments across three heads; the final body needed about 50 review-disposition rows. The last review arrived after the body was being finalized.
- Effect: a large disposition-writing effort in the PR body (not measured).
- Idea for Aegis: keep one automated review per head, deduplicate findings across heads, and require the PR body to link one review summary rather than enumerate repeated findings.
- Status: open for Aegis.
