# Queued owner request (do not start until FU-1 and FU-2 are both merged and complete)
Owner, verbatim, direct chat 2026-10-08: "after fu-1 and fu-2 is merged and completed, start planning for this:
A batch from the unselected skill expansion"
Scope: PLANNING ONLY (stage A + plan audit). Building needs the owner's batch choice and merge terms.
Starting point: docs/roadmaps/aegis-backlog-forecast.md "Unselected skill expansion" (68–140 agent-h after D69–D71),
docs/150-claude-skills-roadmap.md, docs/300-repeatable-software-saas-skills-roadmap.md, docs/skills/*.md priorities.
Owner follow-up, verbatim: "when you do the planning, it should be on Open 5.5 xhigh, you may add agents to assist in the planning"
(Coordinator reading: "Open 5.5" = Opus 5.5. Planning lead and any assisting research agents run on Opus 5.5 at xhigh;
an independent plan auditor, also Opus 5.5 xhigh, audits the result.)

## Start condition met
FU-2 #679 merged 15:55:22Z (c1acc075; post-merge run 37804698446 success); FU-1 #680 merged 16:13:04Z (52289779;
post-merge run 37807051981 success). Base for planning: origin/main 52289779 (re-verify).

## The six remaining candidate groups (forecast docs/roadmaps/aegis-backlog-forecast.md:723-735 and :212; sum 68–140)
G1 QA Tier 2 (12–24): visual-regression-test-designer, role-based-qa-matrix, mobile-viewport-qa,
   exploratory-testing-charter, mock-strategy-designer, ci-shard-parallel-isolation (reconciliation v4 :251-261)
G2 QA Tier 3 (8–16): property-based-test-designer, mutation-testing-reviewer, soak-test-planner, chaos-test-planner (:263-270)
G3 Phase 2 (18–36): api-contract-designer, idempotency-first-designer, validation-boundary-designer,
   observability-by-design, operational-runbook-author, system-context-mapper, bounded-context-identifier,
   dependency-direction-guard, refactor-safety-planner (skills-catalog :1300-1304)
G4 Phase 3 (8–16): tenant-provisioning-designer, membership-invitation-designer, role-permission-architect,
   security-impact-note-author (catalog :1311-1314)
G5 Phase 4 (20–40): topics only — auth/session review, CSRF/XSS/SQLi deep-dives, storage-policy review, webhook
   security, rate-limit design, logging redaction, compliance-evidence mapping, privacy-by-design, security-drift
   detection, security-impact-note authoring (catalog :1322-1326)
G6 Phase 5 extras (2–8): e2e-test-architect, qa-closeout-reporter, remaining untiered cat-06 rows (catalog :1334-1342)
Coordinator check: none of the named skills exists by exact name in .claude/skills/ (196 entries). Overlap by
function is NOT checked yet — that is the helpers' job.
Shown to the owner 2026-10-08 ~16:05Z; owner gave no exclusions.

## Owner instruction (verbatim, direct chat in this session, 2026-10-08)
"make sure you store these plans in the repo's backlog.
Add more agents for the planning"
Coordinator reading: the planning output (the recommended batch, alternatives, per-candidate overlap/cost evidence)
is stored in the repository as a backlog/proposal document, following the convention of the earlier
docs/roadmaps/*-skill-batch-proposal.md files and whatever backlog index/forecast/catalog pointers they used. That is a
repository change, so it goes through all seven stages in its own PR. Merge terms for that PR are NOT yet granted —
the coordinator asks the owner. Storing a proposal selects nothing and builds nothing.
Helpers re-split: QA-A = G1 only; QA-B = G2 + G6; P34 helper = G4 only; new SEC helper = G5; new MECH helper (delivery
mechanics, measured costs, repo-storage convention); new DEMAND helper (cross-cutting gap/demand evidence).
Recorded by coordinator at 2026-10-08T16:18:57Z (date -u).

## Owner answer: merge terms for the plan-storage PR (AskUserQuestion, this session, 2026-10-08; verbatim)
Q: "The PR that stores the skill-batch plan in the repo is a proposal page only: it selects and builds nothing. May the team merge it on the same terms as FU-1 and FU-2 (all seven stages passed, all checks green, admin merge allowed, fix and retry on failure)?"
-> "Yes, same terms (Recommended)" — option text: "It merges once every stage passes and every check is green. Choosing which batch to build stays a separate decision of yours."
This is the merge authority for the plan-storage PR only (replaces "NOT yet granted" above). It authorizes no build.
Recorded by coordinator at 2026-10-08T16:23:22Z (date -u).

## Owner instruction (verbatim, direct chat in this session, 2026-10-08) — binds every recommendation
"always audit and scrutinize your recommendations. Do not make any assumptions on your recommendation, if you are unsure, look for evidence or research it first."
Coordinator application: every recommendation (batch choice, overlap verdict, estimate, MANUAL-ONLY call, procedure
choice) must carry its evidence (file:line, command output, PR/commit) or be researched until it does; anything still
unproven is labelled "unverified" and is NOT used as a basis for the recommendation. Each recommendation section ends
with a self-scrutiny note: the strongest counter-argument and what evidence would change it. The coordinator's own
earlier expectation that the batch "lean towards QA Tier 2 or Phase 3" was an unverified guess and carries no weight.
Recorded by coordinator at 2026-10-08T17:10:06Z (date -u).
