# Project Aegis evidence: where to read next

This index helps maintainers and reviewing agents find **17 selected decision
and delivery evidence pages**. These pages record what was checked or decided
at a particular time. They are not a current work queue, approval grant, or
instruction to repeat an old run. For current authority and status, read the
[owner approval register](../approvals/APPROVAL_REGISTER.md),
[Behavioral Eval Runner backlog](../roadmaps/behavioral-eval-runner-backlog.md),
[control-plane backlog](../roadmaps/resumable-control-plane-backlog.md), and
[setup routing plan](../roadmaps/aegis-setup-routing-plan.md).
The current-reading boundaries below were checked on 2026-09-23 against the
source-library tree at `e2145b1`; recheck the owning registers after later work.
This index was created that day and fifteen of its seventeen rows date from that
sweep. **Exactly two rows post-date it and are therefore not covered by it:** the SCIF
close-out corrections row, added 2026-10-11 by commit `503c3b30`, whose provenance is
that commit's record; and the FU-3 record publication row, added 2026-10-13 by the
workspace-citation-durability change against base `dbe2ee28`, which states its own date
and base revision in the row itself. Neither row can name the commit that contains it -
a page cannot cite its own commit, the convention
`docs/roadmaps/aegis-ci-baseline-2026-10-11.md` L51-L52 states for itself.

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
| What the offline runner core delivered | [WP-2B-1 summary](behavioral-eval-runner-wp-2b-1-summary.md) | Behavioral Eval Runner control evidence only; no provider execution proof. |
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
| What the #723/#729 close-out record got wrong, corrected forward | [SCIF close-out corrections](scif/scif-closeout-corrections-2026-10-11.md) | Dated corrections only; the approval register is untouched and no authority is created. |
| Where the evidence cited by the O-F1 publication note now lives, and the rule that keeps citations retrievable | [FU-3 record publication](fu3-record-publication-2026-10-13/README.md) | Published copies with per-file sha256 digests; the superseded citations were accurate but not retrievable from a fresh checkout. **Added 2026-10-13 by the workspace-citation-durability change, against base `dbe2ee28` - not part of the 2026-09-23 sweep at `e2145b1`.** |

Other dated records are reachable from the owning backlogs and the
[documentation index](../README.md). Do not infer that an unlisted evidence
page has been reviewed or that these 17 pages cover the full repository.

## Citation durability

A permanent record here — a governance log entry, a register entry, a dated evidence page or a roadmap
fact — supports each claim with evidence a fresh checkout can retrieve: a path inside this repository,
written as a Markdown link so the repository's own link checker proves it resolves. Where the artifact
cannot be published (an oversized archive, an external system, a private input), the record carries the
artifact's digest, names the locator it is known by, and says plainly that the artifact is **not
retrievable from this repository**. An out-of-tree path alone is not acceptable support. A digest pins
identity; it never makes an absent artifact retrievable.

**The rule is prospective, and this is its effective date.** It binds citations **added from this change forward** -
the change that states it, merged `2026-10-13`. It does **not** retroactively invalidate records already merged:
**five archive citations in earlier, merged records remain OWED**, enumerated with their dispositions in section 3 of the
publication record [docs/evidence/fu3-record-publication-2026-10-13/README.md](fu3-record-publication-2026-10-13/README.md) and tracked as open items. Those
records neither **violate** this rule nor are **silently excused** by it: they predate it, the work that would publish
their evidence is named and outstanding, and this paragraph exists so a reader can tell the two cases apart. **A rule
stated as a universal invariant while five known sites remain unmet is a false claim about its own scope** - Codex
raised exactly that, and the scope sentence is the repair.

This is a documented rule, not a machine-enforced one, and the difference is stated rather than blurred:
the "Run Markdown link checker over the repository's own pages" step of `validate-skills` validates the
links a record **already contains** - it goes red when a written link stops resolving - and it does
**not** require a record to contain a durable citation at all. A record can cite an out-of-tree path as
plain text, or omit its evidence entirely, and that step stays green. Supplying the citation this rule
requires is therefore a **documentation obligation that nothing machine-checks**; the *digest* half is
checked by nothing either, and a record that relies on it says so.
