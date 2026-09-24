# PR #88, then shared skill contracts — audited execution plan

**Reading key:** This is a historical plan for Behavioral Eval Runner (BER)
pull request (PR) #88, not an instruction to restart it. Owner decision (OD)
is a later human calibration disposition. A software development kit (SDK)
is a provider's programming package; Portable Operating System Interface
(POSIX) refers to Unix-like host behavior; Developer Certificate of Origin
(DCO) means commit sign-off. Priority zero (P0) and priority one (P1) mark
finding urgency, with P0 the more urgent class. Continuous integration (CI)
runs automated checks. Quality assurance (QA) means independent test review;
JavaScript Object Notation (JSON) is a data format; a large language model
(LLM) generates model output. An estimated time to complete (ETA) is a work
forecast. `TEMP` and `TMP` name temporary-directory environment variables,
not the repository root.

> **Current reading, checked 2026-09-23:** This is the preflight plan as it
> stood before delivery. Pull request (PR) #88's engineering, PR #90's shared
> contracts and PR #91's offline continuous integration (CI) have since merged.
> The [PR #88 closeout](../README.md) and
> [current BER backlog](../../../roadmaps/behavioral-eval-runner-backlog.md#start-here-status-and-routes)
> record that delivery and the remaining measured-calibration gates. The
> original authorization, estimates, branch state and action list below are
> historical evidence, not instructions to reopen those PRs or start a run.

Prepared 2026-09-12. This is the requested preflight and final plan; implementation,
publication and merging have not started in this turn. The owner authorized fixes,
commits, pushes, merges and repeated Actions remediation. That authorization persists;
routine execution does not need repeated permission. Read-only agents have standing
authorization. GitHub's actual merge requirements still apply.

## Estimates and scope

| Task, in execution order | Active engineering/review estimate | Completion condition |
| --- | --- | --- |
| PR #88 engineering closure | 5–11 hours; reserve another 4–8 only for substantive new findings | Corrections integrated, Windows test portability addressed, current-revision evidence and reviews complete, required checks accepted, PR merged, resulting main verified |
| Shared skill contracts | 12–24 hours; reserve another 8–16 if candidate triage confirms broader defects | Every current candidate dispositioned, confirmed in-scope defects fixed, aligned contracts/examples/evals checked, PR merged and main verified |
| Permanent BER and contract-test Actions coverage | 2–4 additional hours, separately reviewed after the test commands are settled | Offline suites run on relevant PRs and main; protected-workflow change follows the explicit reviewed merge route |

Base total: 19–39 active hours, approximately 3–5 focused working days. External
review/runner waits are additional and cannot be promised a fixed duration. Estimates
are planning ranges, not measured delivery commitments. Re-estimate after candidate
triage or any material new defect.

PR #88 will describe the delivered calibration controls and development-driver
hardening. It will not claim measured calibration is complete. Replacement dataset,
human label approval, final holdout execution, measured acceptance/report wiring and
OD-1 remain separately recorded WP-2B-3 work. No provider calls are part of this plan.

## Preflight evidence

- Workspace verified as the source library using all four local landmarks.
- Live GitHub main: `000352f55b71f0c3e897a482d279d34bfaa3d66b` (PR #89).
- Live PR #88 head: `ac9e1cdb020f4efb7a52e5ea606c3b329fb486e2`.
- Correction branch: `review/ber-phase01-corrections`,
  `a231bc5db820c89467b32dbec533adf01eb56676`, six commits ahead of PR #88.
- PR #88 is OPEN and mergeable, but GitHub reports BLOCKED / REVIEW_REQUIRED.
  Both existing checks, `validate-skills` and `gate-guard`, passed at the old PR head.
  Current main's validation workflow also passed. These are not checks of a future
  integrated revision.
- All 12 review threads remain unresolved on GitHub. Their exact IDs are mapped to
  fixes and regressions in the correction branch's phase01 review record. Recheck
  each disposition after integration before resolving its thread.
- Main's branch protection requires one approving review; none exists. Local AI
  reviews do not satisfy GitHub's approving-review requirement. Administrator
  capability was observed, but no bypass or protection change is assumed authorized.
- The only workflow runs validator tests, skill validation, and PR DCO checks. It
  does not run BER tests or contract-audit tests. Editing workflows or `scripts/tests/`
  deliberately makes `gate-guard` fail. That is a policy gate, not a software defect.
- Read-only merge analysis found no text conflict against current main. The audit
  register is changed on both branches; retain PR #89's engine/test corrections and
  reconcile its current-status text after integration.
- Active runtime README and PR body contain stale availability, approval, review and
  completion claims. Historical records remain dated; correct active instructions.

### Local checks actually run

Baseline used a separate detached main worktree. Logs are in this directory.

| Check | Main `000352f` | Corrections `a231bc5` |
| --- | --- | --- |
| Validator self-tests | 91 assertions pass | 91 assertions pass |
| Skill validator | 184 valid, zero warnings | 184 valid, zero warnings |
| Contract-audit self-tests | 62 assertions pass | 50 assertions pass; older engine before PR #89 integration |
| Runner self-check | PASS | PASS |
| DCO | Not applicable to main's push event | 12 commits checked; all signed or exempt |
| Diff whitespace | PASS | PASS |
| Protected-path diff, current correction proposal | Not applicable | No protected gate files changed |
| Windows full BER suite, Python 3.14.7 / OpenAI SDK 3.0.0 | Full suite not run | Initial sandbox run: 962 tests, 2 failures, 19 errors, 13 skips |
| Same 21 failed Windows cases, original sandbox context | Same 2 failures and 19 errors reproduced | Initial failures retained |
| Exact 21 Windows failures, owner context and canonical TEMP/TMP | Not run in this context | 21/21 pass, 3.197 seconds; no source changes |
| POSIX full BER suite, Python 3.12.3 | Not run | 962 tests run, 11 skips, zero failures/errors; 28.318 seconds test time |

The initial baseline DCO invocation used `origin/main..HEAD`, an empty range, and
correctly failed closed. The workflow does not run DCO for a main push. This is an
inapplicable preflight invocation, not an unsigned-commit defect; its original log
is retained. The real correction-branch range passes. No history rewrite is needed.

The Windows failures comprise four families in production/test files unchanged
between main and corrections: 11 Git ownership errors; 8 manifest fixture path
effects; one junction fallback rejecting a short-path `~`; one synthetic watchdog
termination failure. All 21 pass under the checkout owner with process-local
canonical TEMP/TMP, without changing code, disabling ownership checks, or loosening
path verification. This confirms that execution context matters; it does not prove
that sandbox process termination works or that short-path fixtures are correct.
Retain the initial failed run. The final combined revision still needs a complete
Windows run in its intended supported context.

The path failures expose inherited fixture portability assumptions worth repairing:
test records use a raw short alias while production records use canonical paths;
the junction test's guarded fallback rejects the alias before reaching its assertion.
Add 1–3 hours for this work (included in the revised PR estimate). Fix fixtures and
exercise the real short-path materialize/verify route; do not merely hide the case
with a chosen TEMP directory or weaken the verifier. The same 21-case comparison
on main reproduced all 2 failures and 19 errors; see `windows-main-failed-cases.json`
and its log. The owner-context correction check is recorded in
`windows-owner-canonical-failed-cases.json` and its log.

The POSIX run used the existing local image
`sha256:9bd26ad900bb5e0f4dee75839e957a89ae89c2b7ab1e76050e559790e946b948`,
with no network, an unprivileged container user, a read-only project mount, and a
disposable checkout of exact commit `a231bc5`. Its Python differs from CI's 3.14;
SDK-dependent and platform-specific skips are recorded in the log. It is useful
platform evidence, not complete parity with the GitHub environment.

Fresh main audit v1.13.0 inspected 704 skill-corpus files across 184 skills. It
reports 98 semantic candidates (2 P0, 96 P1) and 311 informational routing entries.
Candidate severity is a review priority, not proof of a bug. The two STATE-001 P0
candidates already have documented false-positive dispositions. Preserve the old
baseline; the fresh output is `main-contract-audit.json` / `.md` here.

## Execution 1 — PR #88

1. Integrate the existing correction commits into PR #88's branch without force
   pushing or discarding work; merge verified current main. Check the real combined
   tree, especially the register and PR #89 audit fixes.
2. Correct active README/status documentation and rewrite the PR title/body around
   its delivered engineering scope. Preserve historical approvals as history and
   state that the approved input bytes are unavailable. Keep calibration and OD-1 open.
   Address the preflight's Windows fixture portability findings as an explicitly
   identified inherited test-harness correction, with focused regressions and
   preserved production containment/path checks. Record the intended execution
   context for process-control tests; sandbox capability remains a distinct claim.
   The added 1–3 hours covers confirmed fixture assumptions. Git ownership and
   restricted process termination are environment issues unless new evidence proves
   a repository defect; this PR does not attempt to remove sandbox limitations.
3. Automate declared pre-commit CI equivalents and focused regression checks. Verify
   each of the 12 review findings against the integrated source and its regression.
   Preserve this plan and the useful preflight evidence with the project on GitHub
   as part of the implementation commits.
4. Create the signed candidate commit, then run definitive pinned-SDK Windows and
   POSIX suites and independent Aegis read-only reviews against that exact commit:
   QA coverage, execution/security boundaries, and focused code/architecture review.
   Record commands, platform/dependency versions, commit/tree, results and skips.
   A substantiated fix produces a new signed candidate and affected validation;
   definitive evidence must identify the actual submitted SHA.
5. Push the verified candidate to the PR branch and inspect Actions and review
   feedback for that exact head. Resolve a thread only after verifying its fix.
   Repeat the repair loop below for new findings. Earlier-head checks never stand
   in for current checks.
6. Merge through the normal protected-branch route after the required approving
   review and checks. If GitHub still blocks, present the concrete reviewed revision
   and exact remaining requirement; do not silently use administrator bypass.
7. Verify the resulting main commit contains the changes and its post-merge checks
   pass. Repair any post-merge regression through a reviewed follow-up PR before
   treating this task as complete. Start contracts only after this checkpoint.

## Execution 2 — shared skill contracts

1. Branch from verified merged main and regenerate the audit. Disposition every
   current semantic candidate in justified root-cause groups: confirmed defect,
   false positive, already fixed, or unresolved with named evidence needed. Do not
   edit all 98 mechanically or count the 311 informational entries as defects.
2. Resolve the three confirmed inconsistencies:
   - Approval lifecycle: append immutable grant/revocation/expiry/supersession records
     and derive effective status; old ACTIVE records must not revive revoked grants.
   - Mutable projections: define the narrowly authorized refresh of named current-view
     sections while preserving immutable records. Reconcile the generation standard
     and orchestrator contract explicitly.
   - Roadmap language: Now/Next/Later describe planning horizons; delivery commitment
     requires a named human decision. Estimates and confidence do not create grants.
3. Keep current explicit user authorization effective. Recording a grant must not
   narrow its scope arbitrarily or require repeat permission for authorized actions.
   Update affected skill instructions, references, templates and evals together.
4. Add/run meaningful deterministic checks for lifecycle replay, expiry, supersession,
   projection boundaries and immutable preservation where the existing harness can
   test them. Review semantic eval cases independently; edited JSON alone is not
   evidence that an LLM passed a behavioral evaluation.
5. Use the same exact-revision review, signed commit, push, Actions repair, normal
   merge and post-merge verification loop as PR #88. Confirmed defects cannot be
   closed by marking them false positives without supporting evidence.

## Permanent automation

Add BER regression tests and contract-audit self-tests to GitHub Actions in a
separately reviewed change after the two primary tasks establish the final commands.
Use pinned dependencies, record skips, keep provider calls disabled, and preserve the
existing structural gate. This is additional 2–4-hour work within the automation
objective, not an implicit claim that current CI already provides this protection.

Workflow changes, and any new contract tests under `scripts/tests/`, trigger the
existing protective guard. Complete and review the concrete change before obtaining
any required owner disposition for that gate. Do not disable, rename or weaken a
check, or treat intentional rejection as an infinite test-fix loop.
Any later owner disposition concerns the specific protection mechanism blocking the
concrete reviewed change; it is not a repeat request to edit, test, commit, push,
or perform a normal merge already authorized by the owner.

## Repair loop and stopping rule

Collect evidence -> reproduce/classify -> minimal fix -> affected tests -> focused
independent review -> signed commit/push -> current-head Actions/review inspection.
At the final candidate, run the required complete validation set. Re-run affected
validation after later changes; do not repeat broad suites without new evidence.

Classify failures as code defects, pre-existing defects, infrastructure/environment
issues, or intentional policy gates. Investigate transient failures with bounded
retries; do not retry until a lucky pass, relax thresholds, hide failures or remove
tests. Keep unrelated baseline repairs in separately scoped changes.

Completion means no unresolved confirmed in-scope defects, all current candidates
accounted for, accepted current-revision checks/reviews, merged changes verified on
main, and accurate backlog/status records. This does not promise discovery of every
possible future bug. A named external merge requirement remains a dependency, not
permission to fabricate approval or report completion.

## Independent scrutiny and resulting changes

Three bounded read-only reviews covered PR test readiness, shared contracts, and
the proposed plan itself. Their strongest objections led to these changes:

- Separate PR engineering completion from measured calibration completion.
- Treat GitHub's missing approving review as a present dependency in the ETA.
- Require evidence for the actual integrated/submitted revision, not only prior fixes.
- Make permanent CI coverage explicit and account for protected-file handling.
- Separate candidate triage from remediation and retain contingency for new findings.
- Preserve explicit current-session authorization without repeated consent ceremonies.

Planning disposition: ready for implementation with the named merge dependency and
validation residuals. No code change, push, merge, review comment, or provider call
was performed during this preflight. The clean temporary baseline worktree was
removed; test-generated bytecode was preserved outside the source worktree.
