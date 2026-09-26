# Decision proposal: reduce recurring protected-file merge interruptions

**Status:** Proposed; no new authority or CI behavior takes effect from this
document. **Prepared:** 2026-09-26. **Owner:** Peter Nguyen.

Recommend option A: a standing, conditional exception for the existing
protected-file signal on four named BER reporting/aggregation source and test
files, with fresh verification, independent review and a
receipt for every merge. This removes repeated owner questions while retaining
the existing guard and deliberate administrator merge. The check will still
be red. If making approved protected PRs green is essential, choose option B
for a separately reviewed implementation proposal.

## What is happening

Continuous integration (CI) runs automated checks on a pull request (PR).
`gate-guard` is the job that detects changes to protected files. The current
[workflow](../../.github/workflows/validate-skills.yml) exits unsuccessfully
whenever the changed paths include a protected path. It does not read reviews,
owner approvals or the approval register. Re-running it on the same protected
diff cannot acknowledge an approval or change that result.

Protected paths include the workflow and validation machinery and the entire
Behavioral Eval Runner (BER), including its tests and documentation. The
[offline CI guide](../offline-ci.md#protected-files) explains the complete
scope. This prevents routine delivery from silently changing the machinery
used to judge its own work. The
[guard regressions](../../scripts/tests/test_offline_ci.py) deliberately verify
failure for protected changes, including renames and unusual filenames.

An **administrator merge** deliberately uses repository administrator authority
to merge despite a required check. An **exact head** is the full commit ID of
the candidate: changing a commit invalidates evidence tied to the previous
head. A **standing exception** authorizes a defined class of future actions
under conditions; a **one-time exception** covers only its named action.

PR [#313](https://github.com/ModernNomad-98/Project-Aegis/pull/313) changed four
protected BER files. PR
[#315](https://github.com/ModernNomad-98/Project-Aegis/pull/315) changed two:
`reporting.py` and `tests/test_reporting.py`. Both passed Linux and Windows
verification while the guard failed. The owner separately approved each
merge. #315's approval is recorded in AEGIS-APR-044 and consumed in
AEGIS-APR-045: it was one-time and grants no recurring exception.

The [approval register](../approvals/APPROVAL_REGISTER.md) records standing
administrator delivery authority, but AEGIS-APR-013 and AEGIS-APR-024 require
green local tests and GitHub Actions. AEGIS-APR-039 preserves that condition.
The [current merge policy](../reconciliation/auto-merge-policy.md) consequently
requires a separate decision for this intentional failed check. The recurring
interruption comes from combining an always-failing protected-path signal with
the all-green condition.

## Options and costs

These are planning estimates, not measured implementation commitments. Active
hours exclude owner/reviewer waits and hosted CI queue time. All options retain
the underlying code review and verification work.

| Option | Why consider it; benefits | Drawbacks | Setup, money and upkeep |
| --- | --- | --- | --- |
| **A. Standing conditional exception for four BER files — recommended** | Ends repeated owner exceptions for authorized reporting/aggregation repairs; keeps protected-file detection, independent review and deliberate merge. | The guard stays red; every other protected path still needs its separate owner decision. Evidence must distinguish an approved signal from a real failed check. | Estimate 1–3 active hours for approved policy/record/document updates and review; no new service or dependency, $0 new task-controlled spend. Each eligible PR needs a reviewed receipt, roughly 5–15 active minutes beyond existing checks/review; owner wait is removed only for eligible changes. |
| **B. Trusted approval check** | Can represent reviewed, authorized protected changes as green, with mechanically checked evidence. | Adds a security-sensitive service/workflow and new failure modes; approval freshness and trusted identity must be maintained. | Estimate 4–8 active hours for discovery and a bounded design proposal. Implementation is unestimated until repository capabilities and a trust mechanism are selected. App hosting, Actions usage or plan costs are unknown; recurring permission, credential, API and workflow maintenance is required. |
| **C. Keep a separate owner exception for every PR** | Preserves the present process with no policy change or new machinery; owner sees each protected merge. | Repeated interruption and owner waiting continue; each new head can require a replacement exception. | No implementation or new service cost. Each PR still needs an exact-head decision and receipt, roughly 5–15 active minutes of administration plus unbounded owner wait and the existing checks/review. |

Option A fits the immediate need because the existing process already gathers
the technical evidence for reporting repairs such as #315; the repeated step is
owner disposition of the same intentional signal. The narrow path scope leaves
per-PR owner oversight of CI and the machinery protecting merges in place.
It preserves review evidence and the ability to stop a merge. It will not
eliminate interruptions for other BER work or changes outside these four files.
Option B becomes worthwhile if green-only dashboards or stronger mechanical
enforcement justify its added implementation and operating cost. Neither a
label alone nor simply ignoring failures provides equivalent review protection.

## Option A: proposed recurring scope

This is proposed grant language for owner review, not an active grant:

> For authorized work in `ModernNomad-98/Project-Aegis`, permit deliberate
> administrator merge when every changed protected path is one of the four
> eligible BER files listed below, the sole failed GitHub Actions check is the
> existing `gate-guard` protected-path condition, and every condition below is
> satisfied.
> This narrowly supersedes the all-green condition in AEGIS-APR-013/024/039 for
> that signal only. It does not authorize unrelated implementation, change the
> protected path set or branch settings, or waive another failed check. Apply
> until the owner revokes or replaces this standing exception.

The exact eligible paths are:

- `tools/behavioral_eval_runner/reporting.py`
- `tools/behavioral_eval_runner/aggregation.py`
- `tools/behavioral_eval_runner/tests/test_reporting.py`
- `tools/behavioral_eval_runner/tests/test_aggregation.py`

This is an exact allowlist, not the whole BER directory. Ordinary unprotected
documentation may accompany an eligible repair. A PR also touching any other
protected file is ineligible as a whole. In particular, workflow/CI files,
CODEOWNERS, validator, DCO, guard scripts and tests, requirements, parent import
files, acceptance machinery and all other BER paths retain separate one-time
owner decisions. Expanding this allowlist requires a new owner decision.

Eligibility also depends on purpose: changes that disable or weaken checking,
alter merge/review authority, change protected-path policy, or modify the guard
or approval mechanism require a separate one-time owner decision wherever the
code is located. Tests cannot be weakened merely to obtain a passing result.

Required conditions for each use:

1. The implementation has separate active authority. Any work-package rule
   explicitly reserving its future guard exception for a separate decision
   remains in force unless the owner separately amends that rule.
2. Applicable local checks and both Linux `validate-skills` and Windows
   `windows-offline-checks` pass for the candidate. No missing, cancelled,
   stale, pending or failed verification result counts as success.
3. Read the guard log: it must show only its documented protected-path match.
   A checkout, fetch, script or infrastructure failure is ineligible.
4. Independent review explicitly covers the changed protected surfaces and
   finds no unresolved blocker. Record reviewer identity and the reviewed
   head; an author cannot supply their own independent review. A read-only
   agent's technical review may satisfy the independent-review evidence but
   cannot create owner approval. The standing grant must come from the owner;
   a candidate PR's newly written grant text cannot authorize that same PR.
5. Immediately before merge, verify the PR still has that head, the review
   and checks still apply, the authority is active, and no reviewer block has
   appeared. A changed head requires fresh applicable checks and review.
6. Record the PR, full head, protected paths, review evidence, local results,
   hosted run/check links, standing grant and merge result in a PR receipt.
   Keep the guard result accurately described as failed with an authorized
   disposition. A later successful main run does not rewrite the PR result.
7. Recheck the post-merge main verification and handle any regression under
   the existing delivery process. Do not arm unattended auto-merge.

No provider call, credential access, real-host proof, private input, deployment,
evidence deletion or spent implementation grant becomes authorized by this
exception. Explicit work-package limits still apply. A blocker or ambiguous
authority means resolve that issue or obtain the applicable separate decision.

If approved, append the owner's exact decision to the register and update
`docs/reconciliation/auto-merge-policy.md` and `docs/offline-ci.md` in a reviewed
documentation change. Never edit historical grant text. For revocation, record
the owner's lifecycle event and return future protected merges to option C;
the guard already remains enforced. Revocation cannot undo completed merges.

## Option B: what a separate design must establish

A **dedicated GitHub App** is a separately identified integration with scoped
permissions. A **centrally trusted workflow** is approval-checking code whose
version and execution authority the candidate PR cannot modify. Either could
verify independent review and authority for the full candidate commit ID.
This is a design direction, not a claim that the current repository or plan
already supports a particular enforcement arrangement.

Discovery must verify current branch/ruleset protections, check identity
binding, GitHub permissions, owner-approved reviewers and available hosting.
The later design must explain how required checks transition from the current
unconditional guard to protected-path detection plus validated approval. An
extra green check alone cannot satisfy the present required red `gate-guard`.

The design must prevent candidate code or candidate-written approval data from
authorizing its own merge. It must verify the exact head and applicable review,
handle new commits, dismissed reviews and revoked grants, reject an author
self-approval, and fail closed on absent or ambiguous evidence. A PR label or
unverified approval-register addition cannot itself be authority. Any standing
policy input must come from an already trusted, owner-authorized source.

Privileged approval handling must not execute PR code or expose a privileged
token to it. Specify minimum API permissions, credential custody, trusted
workflow versioning, replay/event ordering, audit receipts, maintenance owner,
and rollback to the current guard. Test stale heads/reviews, unauthorized
actors, forged checks, revoked authority, API outages and attempts to alter the
approval machinery. Selecting this option authorizes only preparation of that
bounded design proposal; code, App installation, permissions and branch-setting
changes need their own reviewed scope before implementation.

## Owner decision

- **A — adopt the proposed standing conditional exception for four BER files.**
  Approve the exact recurring scope above and its documentation/approval-record updates. No CI
  or repository-setting changes are included.
- **B — prepare the trusted-check design.** Authorize only its 4–8 active-hour
  discovery/proposal step, with $0 task-controlled spend and read-only platform
  inspection. Keep the current per-PR process until a later implementation and
  activation decision.
- **C — retain the present per-PR exception process.** No new grant or work.

**One decision:** Choose A (the narrow four-file standing exception), B
(prepare only the trusted-check design), or C (retain per-PR exceptions).

The selected action affects only the Project Aegis source repository, not
consumer repositories carrying copied skills. Merging this proposal alone
selects none of these options. #315's consumed exception is not approval of A
or B, and this packet does not change the approval register, CI or branch
protection.
