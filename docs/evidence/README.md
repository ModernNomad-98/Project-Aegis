# Project Aegis evidence: where to read next

This index helps maintainers and reviewing agents find **15 selected decision
and delivery evidence pages**. These pages record what was checked or decided
at a particular time. They are not a current work queue, approval grant, or
instruction to repeat an old run. For current authority and status, read the
[owner approval register](../approvals/APPROVAL_REGISTER.md),
[Behavioral Eval Runner backlog](../roadmaps/behavioral-eval-runner-backlog.md),
[control-plane backlog](../roadmaps/resumable-control-plane-backlog.md), and
[setup routing plan](../roadmaps/aegis-setup-routing-plan.md).
The current-reading boundaries below were checked on 2026-09-23 against the
source-library tree at `e2145b1`; recheck the owning registers after later work.

**Reading key:** Behavioral Eval Runner (BER) is the skill evaluation tool;
control plane (CP) is the delivery state and recovery component. A work package
(WP) is a bounded delivery phase; a backlog item (BKL) records a narrower need.
`BER-DEC` names a BER owner decision, `AEGIS-APR` an approval-register entry,
and `OD-1` the later owner ratification of measured judge calibration. R1–R5
name BER capability-evidence gates. A pull request (PR) carries a reviewed
repository change. Continuous integration (CI) runs automated source checks;
it does not prove a real host or provider is ready. `PENDING` means human
review is not complete; `BLOCKED` means a required gate is missing. A source
SHA is a commit hash. Historic test counts, versions, and status labels belong
to the dated record that reports them.

## Find the evidence by decision

| If you need to understand… | Read | Current-reading boundary |
| --- | --- | --- |
| Which backlog statuses were corrected in September 2026 | [Backlog status crosswalk](backlog-status-reconciliation-2026-09-12.md) | A dated correction, not a complete current inventory. |
| Why the first BER host/capability spike accepted limited scope | [WP-2B-0 summary](behavioral-eval-runner-wp-2b-0-summary.md) | Outcome B is historical; later offline packages shipped, while live gates remain. |
| What the offline runner core delivered | [WP-2B-1 summary](behavioral-eval-runner-wp-2b-1-summary.md) | Non-live control-plane evidence; no provider execution proof. |
| What the non-live Scenario A graders delivered | [WP-2B-2 summary](behavioral-eval-runner-wp-2b-2-summary.md) | Mock and recorded evidence only; no measured judge calibration. |
| What the original calibration engineering and preflight recorded | [WP-2B-3 summary](behavioral-eval-runner-wp-2b-3-summary.md) | Its original approved input bytes are unavailable; current labels and execution are separate gates. |
| How schema-integrity work was checked | [BKL-007 review](ber-bkl-007-schema-integrity.md) | PR #104 merged; the old conditional DONE statement is historical. |
| Why PR #88's engineering closeout was accepted | [PR #88 closeout](ber-pr88-closeout-2026-09-12/README.md) | Its preflight and implementation evidence have different dates. |
| What the PR #88 preflight planned before delivery | [Preflight final plan](ber-pr88-closeout-2026-09-12/preflight/final-plan.md) | PR #88, shared contracts and offline CI later merged; do not rerun the old plan. |
| What survived the lost-computer recovery | [Recovery handoff](ber-recovery-2026-09-11/README.md) | Source survived; original calibration inputs did not. |
| How replacement inputs were originally proposed | [Replacement plan](ber-recovery-2026-09-11/replacement-plan.md) | A private candidate packet now exists but still awaits owner label review. |
| What the new candidate packet publicly establishes | [Sanitized candidate summary](ber-replacement-candidate-1-summary.md) | Candidate labels are PENDING; no private case bytes appear here. |
| Why the control-plane design was accepted | [CP-WP-001 review](control-plane/cp-wp-001-review.md) | Documentation-only design evidence, not a live controller. |
| Which synthetic control-plane capability failures were tested | [CP-WP-003A review](control-plane/cp-wp-003a-review.md) | PR #123 delivered the offline proof; real CP-WP-003 remains BLOCKED. |
| What issue #101 package 2 delivered | [Package 2 review](setup/issue-101-package-2-review.md) | Windows-tested Aegis-only saved choice shipped; no helper or provider connection. |
| What issue #101 package 3 delivered | [Package 3 review](setup/issue-101-package-3-review.md) | Offline advisory contract shipped; a host hook and actual fallback remain future work. |

Other dated records are reachable from the owning backlogs and the
[documentation index](../README.md). Do not infer that an unlisted evidence
page has been reviewed or that these 15 pages cover the full repository.
