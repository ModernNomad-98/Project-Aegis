# Local Aegis checkout inventory — 2026-10-09 pause

Read-only, scoped census of `.git` checkouts at depth one below `C:\src\Codex Projects\Project Aegis`. Each HEAD and status was obtained with command-scoped `safe.directory`; no repository config or checkout was changed. Short HEADs are for orientation only. Re-run full `git worktree list --porcelain` and status on restart before touching a path.

| Checkout below workspace root | Branch or detached | HEAD prefix | Dirty at census |
| --- | --- | --- | --- |
| `apr099closeout/impl-c` | `docs/apr099-consumption-20261009` | `39e7e8828a6a` | clean |
| `cadence/impl` | `docs/cadence-1-through-685-20261009` | `e834ea707906` | clean |
| `cifix/pfix-base-repo` | `claude/sharp-lovelace-urgxpz-ci-fix` | `5228977920ee` | clean |
| `cifix/pfix-repo` | `claude/sharp-lovelace-urgxpz-ci-fix` | `a33aa2a62058` | clean |
| `cifix/preg-e-clone` | detached | `7721376b976c` | clean |
| `cifix/preg-e-h1-clone` | detached | `abc49113a83a` | clean |
| `cifix/preg-e-h1-integration` | detached | `ae0b2d4df78d` | clean |
| `cifix/preg-repo` | `docs/cifix-pr682-gate-guard-exception-20261008` | `abc49113a83a` | clean |
| `cifix/validate-e` | detached | `a33aa2a62058` | clean |
| `forecastfix/implementation` | `docs/forecast-127-overlap` | `d6646ac623bd` | clean |
| `linkbound/impl` | detached | `8e11c8f4c277` | **2 staged:** `scripts/ci/check-markdown-links.py`, `scripts/tests/test_markdown_links.py` |
| `metricsfix/implementation` | `docs/metrics-1-ci-duration` | `c03f8c38c1cd` | clean |
| `pause-checkpoint/repo` | `docs/pause-checkpoint-20261009` | `625fc66711ea` at initial census | clean at initial census; handoff files were added afterward |
| `policyfix/implementation` | `docs/policy-path-scoped-ci-reading-20261008` | `8cd649ae6562` | clean |
| `readability_staleroot/impl` | `docs/readability-staleroot-1` | `f369585d7b9c` | clean |
| `route002/impl` | `docs/route002-new-edge-triage-20261009` | `8107f50a48cf` | clean |
| `rowpolicy/implementation` | `docs/rowpolicy-1-sourced-skills-rows` | `5228977920ee` | **3 unstaged:** `.github/pull_request_template.md`, `docs/delivery-workflow.md`, `docs/reconciliation/step-0-reconciliation-v4.md` |
| `skillbatch/proposal-repo` | `docs/unselected-expansion-skill-batch-proposal` | `c76114e00013` | clean |
| `stage4b-reconcile/impl-c` | `main` | `625fc66711ea` | clean |

Separately, `C:\src\Project Aegis\Project-Aegis` exists at branch `docs/apr-108-stage-4b-first-tranche-grant` and had untracked `.agents/`, `.codex/`, `artifacts/recovery/`, and `artifacts/reviews/` in a read-only status check. Preserve them. Its `git worktree list --porcelain` enumerated **107 registered worktrees**, including this root and `C:\src\Project Aegis\coord-main`. Each registered worktree's status was subsequently read individually in the table below: 66 clean and 41 with status entries; none was inaccessible. The 19-checkout scoped census above does not include the legacy set.


## Legacy source clone registered worktrees

`git worktree list --porcelain` on `C:\src\Project Aegis\Project-Aegis` returned 107 registered worktrees. Status below was read individually using command-scoped `safe.directory`. This inventory is local and time-sensitive; do not clean, stash, reset or move these worktrees based on this table.

| Path | Branch/ref | HEAD | Dirty state |
| --- | --- | --- | --- |
| C:/src/Project Aegis/Project-Aegis | docs/apr-108-stage-4b-first-tranche-grant | f7c48212bce508512fac4d45f3aa2e43c05b59a4 | ?? .agents/<br>?? .codex/<br>?? artifacts/recovery/<br>?? artifacts/reviews/ |
| C:/src/Project Aegis/coord-main | detached | 797ca687c58a059f76b585993cbd72032bc33c88 | ?? artifacts/coord/ |
| C:/src/Project Aegis/Project-Aegis/.worktrees/apr010-pr119-exception | docs/apr010-pr119-exception | b587261620cbe9c2c02ceae1e187ae12fb22383d | ?? .pr-body-apr010.md |
| C:/src/Project Aegis/Project-Aegis/.worktrees/apr012-ber-policy-proof | docs/apr012-ber-policy-proof | 8542c351fa824bcb0f65b4cfb5125b7fecb5454e | ?? .pr-body-apr012.md |
| C:/src/Project Aegis/Project-Aegis/.worktrees/apr046-consumed | docs/apr-046-consumed | 52a6cb353c8af7cc42fca2277793bcd472c7d94f |  M .claude/skills/agent-authorization-matrix/SKILL.md<br> M .claude/skills/agent-authorization-matrix/evals/trigger-evals.json<br> M .claude/skills/api-event-architect/SKILL.md<br> M .claude/skills/api-event-architect/evals/evals.json<br> M .claude/skills/feature-flag-rollout-strategist/SKILL.md<br> M .claude/skills/feature-flag-rollout-strategist/evals/evals.json<br> M .claude/skills/human-agent-trust-reviewer/SKILL.md<br> M .claude/skills/human-agent-trust-reviewer/evals/trigger-evals.json<br> M .claude/skills/intra-tenant-scope-architect/SKILL.md<br> M .claude/skills/intra-tenant-scope-architect/evals/evals.json<br> M .claude/skills/load-test-planner/SKILL.md<br> M .claude/skills/load-test-planner/evals/trigger-evals.json<br> M .claude/skills/notification-webhook-ux-designer/SKILL.md<br> M .claude/skills/notification-webhook-ux-designer/evals/evals.json<br> M .claude/skills/profiling-methodology-designer/SKILL.md<br> M .claude/skills/profiling-methodology-designer/evals/trigger-evals.json<br> M .claude/skills/staff-scope-selector/SKILL.md<br> M .claude/skills/staff-scope-selector/evals/evals.json<br> M .claude/skills/sunset-deprecation-communicator/SKILL.md<br> M .claude/skills/sunset-deprecation-communicator/evals/evals.json<br> M .claude/skills/sunset-deprecation-communicator/references/sunset-comms-sheet.md<br> M docs/approvals/APPROVAL_REGISTER.md<br> M docs/roadmaps/aegis-documentation-readability-backlog.md<br> M docs/roadmaps/behavioral-eval-runner-backlog.md |
| C:/src/Project Aegis/Project-Aegis/.worktrees/ber-bkl-009a-implementation | feat/ber-bkl-009a-offline-policy | 515432d43c574ad778ba7f0ece1ca47ecf477cbf | ?? .pr139-integration-comment.md<br>?? tools/behavioral_eval_runner/__pycache__/<br>?? tools/behavioral_eval_runner/adapters/__pycache__/<br>?? tools/behavioral_eval_runner/graders/__pycache__/<br>?? tools/behavioral_eval_runner/judge/__pycache__/ |
| C:/src/Project Aegis/Project-Aegis/.worktrees/ber-bkl009-residual-scope | docs/ber-bkl009-residual-scope | 85ee0286afe595944e2f2b592affa7a24080fc30 | ?? docs/roadmaps/ber-bkl-009-residual-host-runtime-privacy-cleanup-proposal.md |
| C:/src/Project Aegis/Project-Aegis/.worktrees/ber-bkl009a-proposal | docs/ber-bkl009a-offline-scope | 0502e8d8dd43ad7fcc01250cd8083c9e08293198 | ?? .pr-body-bkl009a.md |
| C:/src/Project Aegis/Project-Aegis/.worktrees/ber-holdout-summary-matrix | fix/ber-holdout-summary-matrix | c700f9ce00bb66ef9f14fb8fcb3f3d627ab30273 | ?? ber-full-test.log<br>?? tools/behavioral_eval_runner/__pycache__/<br>?? tools/behavioral_eval_runner/adapters/__pycache__/<br>?? tools/behavioral_eval_runner/graders/__pycache__/<br>?? tools/behavioral_eval_runner/judge/__pycache__/<br>?? tools/behavioral_eval_runner/tests/__pycache__/ |
| C:/src/Project Aegis/Project-Aegis/.worktrees/ber-preflight-report-integrity | fix/ber-preflight-report-integrity | 791d136d73b5741864014aa3a70bf24c86b456ff | ?? tools/behavioral_eval_runner/__pycache__/<br>?? tools/behavioral_eval_runner/tests/__pycache__/ |
| C:/src/Project Aegis/Project-Aegis/.worktrees/cadence-20261001b | chore/cadence-log-20261001b | bcfd6237882d3db56a6f699477ab3f5e626e3a3e | clean |
| C:/src/Project Aegis/Project-Aegis/.worktrees/cadence-fix | chore/cadence-log-timestamp-correction | 47baf3f28bd709a0fe5b1e28179366fadf59a9d1 | clean |
| C:/src/Project Aegis/Project-Aegis/.worktrees/cadence-log | docs/coordinator-idle-check-log | 967222b50eb9a52ba3178516284ed9c85e23cb8e |  M docs/roadmaps/coordinator-idle-checks.jsonl |
| C:/src/Project Aegis/Project-Aegis/.worktrees/cadence-log-reconciliation | chore/cadence-log-reconciliation | 0d9b2e2f9afa276b2b77d5fcfc37ebc50769e6ef | clean |
| C:/src/Project Aegis/Project-Aegis/.worktrees/checkpoint-after-232 | docs/checkpoint-after-232 | 6ddd14c6e59f24210117ca2df74b93ef2623534a | ?? .merge-comment.md<br>?? .pr-body.md |
| C:/src/Project Aegis/Project-Aegis/.worktrees/checkpoint-after-284 | docs/checkpoint-after-284 | d9e1517deaf35e3ce15df61ea9329fd1b4518502 | ?? .pr-body.md |
| C:/src/Project Aegis/Project-Aegis/.worktrees/choice-education-core | fix/choice-education-core | 69be30a3a71d21c70f13a6b20d7da5e15e023d17 |  M .claude/skills/architecture-advisor/SKILL.md<br> M .claude/skills/architecture-designer/SKILL.md<br> M .claude/skills/cloud-architecture-decider/SKILL.md<br> M .claude/skills/saas-platform-architect/SKILL.md |
| C:/src/Project Aegis/Project-Aegis/.worktrees/choice-education-extra-architects | fix/choice-education-extra-architects | 9c4c9effd5d93c0f74a756630090bb30d59df6e6 |  M .claude/skills/integration-test-designer/SKILL.md<br> M .claude/skills/model-context-designer/SKILL.md<br> M .claude/skills/qa-automation-architect/SKILL.md<br> M .claude/skills/realtime-subscription-architect/SKILL.md<br> M .claude/skills/search-architecture-designer/SKILL.md<br> M .claude/skills/search-architecture-designer/evals/evals.json<br> M .claude/skills/streaming-event-architect/SKILL.md |
| C:/src/Project Aegis/Project-Aegis/.worktrees/choice-gaps-am | fix/choice-gaps-am | da553307092d755b07111317c2b0ac5617146302 |  M .claude/skills/accessibility-test-harness/SKILL.md<br> M .claude/skills/appsec-implementer/SKILL.md<br> M .claude/skills/flaky-test-detective/SKILL.md<br> M .claude/skills/frontend-perf-engineer/SKILL.md<br> M .claude/skills/mobile-viewport-craft/SKILL.md |
| C:/src/Project Aegis/Project-Aegis/.worktrees/choice-gaps-nz | fix/choice-gaps-nz | da553307092d755b07111317c2b0ac5617146302 |  M .claude/skills/performance-test-harness/SKILL.md<br> M .claude/skills/playwright-e2e-engineer/SKILL.md<br> M .claude/skills/schema-evolution-planner/SKILL.md<br> M .claude/skills/skill-deprecation-planner/SKILL.md<br> M .claude/skills/skill-usage-instrumenter/SKILL.md<br> M .claude/skills/warehouse-lake-architect/SKILL.md |
| C:/src/Project Aegis/Project-Aegis/.worktrees/choice-shared-boundary-fix | fix/choice-shared-boundary-fix | 9c4c9effd5d93c0f74a756630090bb30d59df6e6 |  M .claude/skills/human-approval-boundary/SKILL.md |
| C:/src/Project Aegis/Project-Aegis/.worktrees/coordinator-role-rule | docs/coordinator-role-rule | 1df98ab77cc95922e9e8862ff4173748dee65efa | clean |
| C:/src/Project Aegis/Project-Aegis/.worktrees/cp003-real-authority-decision | docs/cp003-real-authority-decision | 85ee0286afe595944e2f2b592affa7a24080fc30 | ?? docs/roadmaps/cp-wp-003-real-authority-decision-packet.md |
| C:/src/Project Aegis/Project-Aegis/.worktrees/d8-gloss-fix | docs/fix-owasp-d8-gloss | 6b30b9d91f3c6f460e94d4a801777154dfaa6cb8 | clean |
| C:/src/Project Aegis/Project-Aegis/.worktrees/dco-docs-fix | docs/dco-bot-exemption | e09a9d579c457bb36f3593610c00c86df76fd2ab | clean |
| C:/src/Project Aegis/Project-Aegis/.worktrees/dco-sweep | docs/dco-categorical-sweep | c37a6543518c1035174beee81f1fde11ff13493f | clean |
| C:/src/Project Aegis/Project-Aegis/.worktrees/docs-batch-after-208 | docs/batch-after-208 | 3d01e1c5ba90f89d25ab0d0f81eef6f2311476bf | ?? .batch-merge-comment.md<br>?? .batch-pr-body.md |
| C:/src/Project Aegis/Project-Aegis/.worktrees/docs-batch-after-209 | docs/batch-after-209 | 2c8ecaf102b5780f3153a2a5aa614412f59f3c6e | ?? .batch2-merge-comment.md<br>?? .batch2-pr-body.md |
| C:/src/Project Aegis/Project-Aegis/.worktrees/docs-readme-fixes | docs/docs-readme-fidelity | ccf6e9bde9d9db7868902cfbe86d3c0b3e82d6dd | clean |
| C:/src/Project Aegis/Project-Aegis/.worktrees/docs-readme-nav | docs/readme-nav-completeness | d8602bf66bab8264750052707c5e07ee1fdb56e2 | clean |
| C:/src/Project Aegis/Project-Aegis/.worktrees/exec-claim | docs/roadmaps-skill-eval-execution-claim | b329cff94232c8215cd6407d0d366b443d99d545 | clean |
| C:/src/Project Aegis/Project-Aegis/.worktrees/forecast-after-130 | docs/forecast-after-130 | 7aba3045d5b9172cd2d6ba8c4a32c186678cf742 | ?? .pr-body-forecast130.md |
| C:/src/Project Aegis/Project-Aegis/.worktrees/forecast-after-135 | docs/forecast-after-135 | 7e42abcff8942154ae78dd87b5eddc8045e52b39 | ?? .pr-body-forecast135.md |
| C:/src/Project Aegis/Project-Aegis/.worktrees/forecast-after-207 | docs/forecast-after-207 | 25183e5ba669785aac4ede43e6587ecb71daced8 | ?? .forecast-merge-comment.md<br>?? .forecast-pr-body.md |
| C:/src/Project Aegis/Project-Aegis/.worktrees/forecast-after-227 | docs/forecast-after-227 | 02203d0288120a47f7ef9eac1f2620e8ee83ccca | ?? .merge-comment.md<br>?? .pr-body.md |
| C:/src/Project Aegis/Project-Aegis/.worktrees/fullpage-after-225 | docs/fullpage-after-225 | 773a87272fb9b568b213a1511e28fbf8ca969de1 | ?? .merge-comment.md<br>?? .pr-body.md |
| C:/src/Project Aegis/Project-Aegis/.worktrees/fullpage-after-226 | docs/fullpage-after-226 | f0e993730509123c36272f4a24ffdf575e903488 | ?? .merge-comment.md<br>?? .pr-body.md |
| C:/src/Project Aegis/Project-Aegis/.worktrees/fullpage-after-228 | docs/fullpage-after-228 | f3a9c70e3a5ca56765a0505e86e4a8b2011f95a4 | ?? .merge-comment.md<br>?? .pr-body.md |
| C:/src/Project Aegis/Project-Aegis/.worktrees/fullpage-after-229 | docs/fullpage-after-229 | cce5c378d8702dbc9b8b67f1cae9d5a1bea2dd8e | ?? .merge-comment.md<br>?? .pr-body.md |
| C:/src/Project Aegis/Project-Aegis/.worktrees/fullpage-after-230 | docs/fullpage-after-230 | f3afd19dbf71e885855ef48e02de87881799b08c | ?? .merge-comment.md<br>?? .pr-body.md |
| C:/src/Project Aegis/Project-Aegis/.worktrees/fullpage-after-231 | docs/fullpage-after-231 | d629d3a163a4731d3956ba9a113f276976ba1c9d | ?? .merge-comment.md<br>?? .pr-body.md |
| C:/src/Project Aegis/Project-Aegis/.worktrees/gated-backlog-decision-packets | docs/gated-backlog-decision-packets | afeefd5365861e03ee573f2f1a7d519e06aaf1d9 | ?? .pr-body.md |
| C:/src/Project Aegis/Project-Aegis/.worktrees/iso-scope-choice-guidance | fix/iso-scope-choice-guidance | 3212c383dc4a61f724d7f977cf1fae9509005f8a | clean |
| C:/src/Project Aegis/Project-Aegis/.worktrees/issue101-p4-shortlist-sync | docs/issue101-p4-shortlist-sync | 4ca03a9441aea581270e0bf27659b60dfd0a59dc | ?? .pr-body-issue101-sync.md |
| C:/src/Project Aegis/Project-Aegis/.worktrees/od-dco | docs/open-decisions-gloss-dco | 6fbb2201f2be150755e1723962f61fa17aa92a0d | clean |
| C:/src/Project Aegis/Project-Aegis/.worktrees/prov-reloc-2 | docs/skills-provenance-relocations-2 | b3a4cbd788a95433b23971af376be7c50063ad92 | clean |
| C:/src/Project Aegis/Project-Aegis/.worktrees/readability-acceptance-audit | docs/readability-acceptance-audit | f897d472dd5979c41cb9812802022027d12d97fd | clean |
| C:/src/Project Aegis/Project-Aegis/.worktrees/readability-ledger-current-truth | docs/readability-ledger-current-truth | 5cf574c7c84d8c2344c56e730031469ff5f6eeec | clean |
| C:/src/Project Aegis/Project-Aegis/.worktrees/readme-fixes | docs/readme-dco-and-codes | be9dd63bf108050e8479571420fd77ef9849a485 | clean |
| C:/src/Project Aegis/Project-Aegis/.worktrees/recon-banner | docs/reconciliation-stale-banner | 5b0c50848f25a54870bb446bbeee713cdee0042a | clean |
| C:/src/Project Aegis/Project-Aegis/.worktrees/recon-pointer | docs/reconciliation-banner-pointer-fix | 40961f023d70d06dd993169e4451dac9d3dbe737 | clean |
| C:/src/Project Aegis/Project-Aegis/.worktrees/roadmap-fixes-1 | docs/roadmap-readability-fixes-1 | f38dcc25c4be3e9d66fbe1011a8f672eeacc3896 | ?? - |
| C:/src/Project Aegis/Project-Aegis/.worktrees/roadmaps-fixes | docs/roadmaps-provenance-labels | cf72a5d8fe4e28ded92f488f2de6786819f6597c | clean |
| C:/src/Project Aegis/Project-Aegis/.worktrees/root-readme-workspace-routing | docs/root-readme-workspace-routing | 3596442f92d7340ef62ba6140acdbcf3ee498f05 | ?? .pr-body-readme-routing.md |
| C:/src/Project Aegis/Project-Aegis/.worktrees/route002-engine-fix | fix/route002-whole-name-matching | 13a0682b3e70b9290a6a8c7a25fe291dcec93201 |  M .github/pull_request_template.md<br> M CONTRIBUTING.md<br> M README.md<br> M docs/approvals/APPROVAL_REGISTER.md<br> M docs/reconciliation/step-0-reconciliation-v4.md<br> M docs/roadmaps/aegis-open-decisions-2026-09-23.md<br> M docs/skills-catalog.md<br> M scripts/audit-skill-contracts.py<br> M scripts/tests/test_audit_skill_contracts.py |
| C:/src/Project Aegis/Project-Aegis/.worktrees/scenario-a-readability | docs/scenario-a-runbook-readability | 089b97a12667e8af78f155ed91e3dcda278a06a2 | ?? .pr-body-scenario-a.md |
| C:/src/Project Aegis/Project-Aegis/.worktrees/sdk-4a-archive-audit | docs/sdk-4a-archive-audit | 69be30a3a71d21c70f13a6b20d7da5e15e023d17 |  M docs/evidence/setup/issue-101-package-4a-host-feasibility.md<br> M docs/roadmaps/aegis-setup-package-4a-host-preparation-proposal.md |
| C:/src/Project Aegis/Project-Aegis/.worktrees/skill-eval-stale-fact | docs/roadmaps-skill-eval-stale-fact | fe32082a7f45754b265849ce2b6a913f47e117c1 | clean |
| C:/src/Project Aegis/Project-Aegis/.worktrees/skill-fixes-1 | docs/skill-readability-fixes-1 | 235624bd414d8426d4797e0aa25a10233f90bf47 | clean |
| C:/src/Project Aegis/Project-Aegis/.worktrees/skill-fixes-2 | docs/skill-readability-fixes-2 | 5accdb775693921cc3d4ec7fb55b5944bc54271b | clean |
| C:/src/Project Aegis/Project-Aegis/.worktrees/skill-fixes-3 | docs/skill-readability-fixes-3 | 3ebab2c4e6b9d4c369973825cc675d7db2d65c7d | clean |
| C:/src/Project Aegis/Project-Aegis/.worktrees/skill-fixes-4 | docs/skill-readability-fixes-4 | d50b53959e35bb84270656ca33d05f348b1b399a | clean |
| C:/src/Project Aegis/Project-Aegis/.worktrees/soa-choice-guidance | fix/soa-choice-guidance | 8d985c0d5d7dda5e7095ee97b3bcac038b3414dc | clean |
| C:/src/Project Aegis/Project-Aegis/.worktrees/stage4b-host-proof-protocol | docs/stage4b-host-proof-protocol | 6ebfa5fbc86e5071f3b04b7da3cf70b7e6b01a36 | ?? .pr-body.md |
| C:/src/Project Aegis/Project-Aegis/.worktrees/stale-figs | docs/roadmaps-stale-figures-bundle | 9aeb4b60adb8c3cdad61e43de913edcc69baf741 | clean |
| C:/src/Project Aegis/Project-Aegis/.worktrees/standing-approval-choice-guidance | fix/standing-approval-choice-guidance | e3e8589e8150792d5460f73ff87c3c365826af69 | clean |
| C:/src/Project Aegis/Project-Aegis/.worktrees/step6-caveat | docs/roadmaps-skill-eval-step6-caveat | 6f68d742298abff25f521a11f61d5bc03903d4c4 | clean |
| C:/src/Project Aegis/Project-Aegis/.worktrees/tech-spec-choice-guidance | fix/tech-spec-choice-guidance | c31559af52e7136f0adad2132b25fcc29aec0521 | clean |
| C:/src/Project Aegis/Project-Aegis/.worktrees/wp2b3-prerequisite-checklist | docs/wp2b3-prerequisite-checklist | 85ee0286afe595944e2f2b592affa7a24080fc30 | ?? docs/roadmaps/ber-wp2b3-measurement-prerequisite-decision-packet.md |
| C:/src/Project Aegis/rv629b | detached | 7c52b6f63dc14dd1cb794b486135c2d9eb988302 | clean |
| C:/src/Project Aegis/wt-accept | docs/acceptance-conversion-process | 20857201c8e3d8ed028cf713419a91369c520d1f | clean |
| C:/src/Project Aegis/wt-agents | docs/agents-security-review-scope | c7a7f83a9fa19127751f620dbdfc087e1d7191ab | clean |
| C:/src/Project Aegis/wt-ancestry | docs/tracker-ancestry-correction | 582d01e3189d5eec549bb883678bebbc01724e41 | clean |
| C:/src/Project Aegis/wt-apr101 | docs/apr-101-ledger-keeper | 5d99a3735c300d831330e54b8e490304f62bfe06 | clean |
| C:/src/Project Aegis/wt-baseline | detached | b0d3ab717438cbff37e85ad8f4f64e6015633889 | clean |
| C:/src/Project Aegis/wt-batch-a | docs/readability-batch-a | 82c215c29ffc95ed2ef88607942d416c6eb93536 | clean |
| C:/src/Project Aegis/wt-batch-b | docs/readability-batch-b | e6fc8d24ad782cfc93e3b2639c1e2b6e5a35b08e | clean |
| C:/src/Project Aegis/wt-batch-b-t2 | docs/readability-batch-b-ledgers-t2 | a06344226bfe777a5009a69b079283c2577d9570 | clean |
| C:/src/Project Aegis/wt-batch-c | docs/readability-batch-c | d6e484189cc30c67dc69aeb973e15f89b693537d | clean |
| C:/src/Project Aegis/wt-batch-c2 | docs/readability-batch-c-skills-r2 | 757f1a5181f8977df08c8e42b2d94ae21a2d204c | clean |
| C:/src/Project Aegis/wt-cadence | chore/cadence-log-20261002 | fc29229d8c0e879ec271b9c5cd6596fa0bc47e44 | clean |
| C:/src/Project Aegis/wt-cadence2 | chore/cadence-log-append | a1144a1445afff320a2ebe3245858f38ec20c30d | clean |
| C:/src/Project Aegis/wt-cadence3 | chore/cadence-log-append-2 | fa339bcae44565c4181937b6535d3aa6d2c1135f | clean |
| C:/src/Project Aegis/wt-cadence4 | chore/cadence-log-append-3 | 0f62022defedc32b27db3db1576f004a58eb0fea | clean |
| C:/src/Project Aegis/wt-design | docs/readability-design-docs | 2ba20c71ce698f00784775734afdfc4e2166f3fa | clean |
| C:/src/Project Aegis/wt-docfix | docs/offline-ci-recorder-fallback | 8d8f0db0c64213fa34e7811acaadae226ecb8e3c | clean |
| C:/src/Project Aegis/wt-floor | docs/readability-pending-floor-correction | 1e8b81e74b4d64ce86884807df4bee4ee557c208 | clean |
| C:/src/Project Aegis/wt-gate | chore/gate-agents-md | 30199a4543ccea1fdcff5dbd30390cc082680dac | clean |
| C:/src/Project Aegis/wt-hazard | docs/stale-checkout-hazard | 8113ed8b91361cd82ac5dab98424f200e53aa61c | clean |
| C:/src/Project Aegis/wt-index | docs/readability-acceptance-index | 797ca687c58a059f76b585993cbd72032bc33c88 | clean |
| C:/src/Project Aegis/wt-integration | docs/integration-roadmap-approval | 3e50926440e5b3387b5b3e5211fab53cd582c331 | clean |
| C:/src/Project Aegis/wt-ledger | docs/ledger-keeper-pilot | ffa5df1ce13a4052828e37246bda85d29a462738 | clean |
| C:/src/Project Aegis/wt-lessons | docs/session-lessons-class7 | d91aaf21952f135b9f78d83daf22b874c60bf9c0 | clean |
| C:/src/Project Aegis/wt-linkfix | fix/link-checker-wrapped-links | 2786841a1f4eed14e3deba8010f34bd7b77da00e | clean |
| C:/src/Project Aegis/wt-misdesc | docs/fix-acceptance-note-misdescription | 7c5f3b53351dc469420fdc6dffdb716f9fdb012e | clean |
| C:/src/Project Aegis/wt-nofab | docs/no-fabrication-rule | 0b3a9b2ea7d7816ff44e9cda6c769f2d7838cb48 | clean |
| C:/src/Project Aegis/wt-pin-ber | detached | 14e3f17c380dd26ddba1f27c7e041b6064509ba4 | clean |
| C:/src/Project Aegis/wt-protect | chore/protected-link-check-and-recorder-lock | 5e8331c70214c9e1674dad41ee8b2939044cd736 | clean |
| C:/src/Project Aegis/wt-q2 | docs/readability-ledger-premises | a3715be7a8d05ef20d5480a6fb33fc2cd5235a27 | clean |
| C:/src/Project Aegis/wt-q5-counting | docs/q5-register-counting-claims | d571ed5b5dfee1e5da33596a12bfc53808705cd1 | clean |
| C:/src/Project Aegis/wt-register | docs/process-issues-and-prevention | c4e0197c3507f8554288c0939af5b85d88ed3bcd | clean |
| C:/src/Project Aegis/wt-reviewrule2 | docs/review-record-invariants | 38cd81bad3c2e01999f7713e3757ead4cf745035 | clean |
| C:/src/Project Aegis/wt-rules | docs/agents-merge-gate-traps | e42a08d97e37ed891a5905a551e86f8d14c97e04 | clean |
| C:/src/Project Aegis/wt-ten | docs/readability-ten-missed-pages | 145647cc9dc74dff259f651442ab7c9c8a14f70a | clean |
| C:/Temp/aegis-coord/wt85 | docs/proc08-cadence-run-q4 | d87d7b2c037beb1a8ba9b70bfa4349ad0370cd8f | clean |
| C:/Users/PeterNguyen/AppData/Local/Temp/cadence3-baseline | detached | 583b330afda2086f0842cd1149d8e8edfef56260 | clean |
| C:/Users/PeterNguyen/AppData/Local/Temp/rev645 | detached | 3e50926440e5b3387b5b3e5211fab53cd582c331 | clean |
