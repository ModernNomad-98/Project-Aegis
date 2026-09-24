# Backlog status reconciliation — 2026-09-12

> **Current reading, checked 2026-09-24:** This crosswalk records what was
> reconciled on September 12, 2026. Its present-tense references to an open
> runner schema item or unfinished pull request #88 belong to that date;
> subsequent requests merged. Use the
> [current Behavioral Eval Runner backlog](../roadmaps/behavioral-eval-runner-backlog.md#start-here-status-and-routes)
> and [evidence index](README.md) for today's status. The original crosswalk
> below remains historical and grants no new implementation or execution.

**Reading key:** Behavioral Eval Runner (BER) is the evaluation tool;
`BER-BKL` names a runner backlog item; `BER-DEC` names a runner decision-log
entry; shorter `D` labels identify catalog decisions. `AEGIS-APR` names an
owner approval-register entry. Owner
decision (OD) is a later human disposition of measured calibration. A pull
request (PR) proposes a repository change. The old status words below apply
to the dated source revision, not necessarily to current main. Row-level
security (RLS) restricts database rows by the acting user's policy.

The owner requested cleanup of stale entries for completed work. Source inspected:
`review/ber-phase01-corrections` at `6bd5abadd16a3ab6cfd89cc15dfaa5572ac9dedd`;
merged main at `000352f55b71f0c3e897a482d279d34bfaa3d66b`.
This is a documentation correction, not new implementation or execution authority.

## Completion crosswalk

| Entry / former claim | Corrected disposition | Evidence and limits |
| --- | --- | --- |
| BER-BKL-001: “BACKLOG” | DONE | PR #83; `CoverageMetrics` in [models.py](../../tools/behavioral_eval_runner/models.py), [report construction](../../tools/behavioral_eval_runner/reporting.py) and [reporting tests](../../tools/behavioral_eval_runner/tests/test_reporting.py) distinguish accounting from actual grading. OD-2 remains open. |
| BER-BKL-004: scaffolding “may be built” | DONE for the scoped offline deliverable | Accepted spike dispositions and PR #83's [containment](../../tools/behavioral_eval_runner/containment.py), [execution profiles](../../tools/behavioral_eval_runner/execution_profile.py) and tests. Live R4/R5 proof remains outstanding under WP-2B-4. |
| BER-BKL-006: offline budget machinery “BACKLOG” | DONE for the scoped offline deliverable | PR #83's [budget state machine](../../tools/behavioral_eval_runner/budget.py) and [budget tests](../../tools/behavioral_eval_runner/tests/test_budget.py). R3's real-host cost-enforcement limitation remains. |
| BER-BKL-008: census “BACKLOG” | DONE | PR #83's [generator](../../tools/behavioral_eval_runner/census.py), [census artifact](../../artifacts/evidence/behavioral-eval-runner-wp-2b-1-census.json) and [reproducibility tests](../../tools/behavioral_eval_runner/tests/test_census.py). New corpus revisions require regeneration; OD-2/OD-3 are separate gates. |
| D12.2/.4/.5/.6/.7: “remain banked candidates” | Implemented | [Catalog implemented sections](../skills-catalog.md) and 30 corresponding skill directories: 5 product, 8 docs, 6 PM-interface, 4 analytics, 7 staff-craft skills; D24–D26. |
| `docs-retention-index`: “stays banked” | Implemented in D25 | [Shipped skill](../../.claude/skills/docs-retention-index/SKILL.md), catalog D12.4 and D25 decision. |
| RLS author / negative-test skills “deferred to Phase 4” | Delivered through `rls-policy-auditor` | [Shipped skill](../../.claude/skills/rls-policy-auditor/SKILL.md) and catalog Phase 4 mapping. No separate unbuilt skills implied. |
| Catalog: “there is no runner yet” | Historical statement | PRs #83/#85 delivered the offline core and non-live Scenario A stack. Calibration and live corpus execution are unfinished. |
| AEGIS-060: unremediated fixture candidate in this branch | REJECTED CANDIDATE on merged main | PR #89 retired the false positive and corrected the audit engine. This branch predates that engine change; preserve it during integration. Valid `(subagent)` annotations must remain. |

GitHub merge metadata was verified on 2026-09-12:

- [PR #83](https://github.com/ModernNomad-98/Project-Aegis/pull/83): merged
  2026-08-13, `72e74af6f0183fef25e353ec2bf3a851d83b5df6`.
- [PR #85](https://github.com/ModernNomad-98/Project-Aegis/pull/85): merged
  2026-08-14, `b84e43ad9f42a793c6f68c2f5aebf0abfad2b8ed`.
- [PR #87](https://github.com/ModernNomad-98/Project-Aegis/pull/87): merged
  2026-08-14, `1c3e4931329179d9a3f9cc9ec1bb93020378c043`.
- [PR #89](https://github.com/ModernNomad-98/Project-Aegis/pull/89): merged
  2026-08-17, `000352f55b71f0c3e897a482d279d34bfaa3d66b`.

## Partial work and unresolved items

BER-BKL-002 stays open: enum names exist, but a completed standalone naming sweep
is not established. BER-BKL-007 separates delivered schemas from the missing
explicit migration/compatibility policy. BER-BKL-009 separates the shipped writer
and scoped handling terms from the complete production policy still required.
Those partial implementations do not settle their whole policy contracts.

BER-BKL-003 remains blocked on real activation evidence or an accepted limitation.
BER-BKL-005 remains blocked on measured calibration and OD-1, while recording that
the non-live stack, judge selection, threshold pre-registration and original phase
authorization already exist. WP-2B-3 now records the actual PR #87 merge.
Missing calibration inputs, replacement-label approval, remaining readiness,
PR #88 integration/merge and later work-package gates remain unresolved.

## Reconciliation rule and verification

These are current-state conflicts: merged implementation, tests and recorded
decisions outrank stale backlog labels. Scope and acceptance criteria remain
binding; no closure claims unmeasured live behavior. The source-of-truth
reconciliation and reviewable-diff skills were applied within the owner's cleanup
request. Original BER IDs, requirements and the §13 governance log are preserved.
The AEGIS baseline is marked historical rather than rewritten.

No missing evidence is assumed to exist: where a separate policy or sweep was
not found, the item stays open. The full 300-capability mapping, semantic audit
candidate triage, production policies and runtime changes are intentionally
outside this cleanup.

Validation: 55 existing reporting/census/budget/containment/profile tests passed
without skips; 91 validator self-test assertions passed; 184 skills validated
with zero warnings. Document checks verified all 15 BER inventory IDs, exactly
four scoped DONE entries, the unchanged §13 governance log, all 30 pack skills
and their eval files, and the new catalog anchors and crosswalk links. No new
tests or runtime changes were introduced.
