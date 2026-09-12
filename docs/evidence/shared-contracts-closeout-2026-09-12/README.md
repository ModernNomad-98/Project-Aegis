# Shared skill contracts — implementation and review record

Prepared 2026-09-12 from merged main `f5e04ad07a5fd2b34b7470bffd38a50c15ce691a`.
This records the implementation candidate; submitted-revision checks and merge
disposition are recorded separately. The owner authorized fixes, automated tests,
commits, pushes and merges after PR #88. Read-only agents have standing permission.

## Prior delivery and revised scope

[PR #88](https://github.com/ModernNomad-98/Project-Aegis/pull/88) merged at that
base after explicit authorization for its administrator merge. Its tree matches
tested head `d53752d2b600410da122d4b85429c35f30d7c873`, and
[post-merge run 34668951280](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/34668951280)
passed. That authorization was specific to PR #88; it does not authorize a later
protected-workflow bypass.

The shared-contract preflight audited all 184 skills and 704 corpus files. All
98 semantic candidates were reviewed: **19 confirmed and repaired, 79 false
positives, zero unresolved**. Context review found three additional write-boundary
defects. The expanded invocation work uses the original plan's contingency:
shared-contract engineering/review estimate revised from 12–24 to **16–32 active
hours**, with external review waits additional. Permanent offline CI remains a
separate **2–4 hour** change after these commands and contracts are settled.

## Dated implementation decisions

- Preserve immutable grants and append lifecycle facts. Derive effective authority
  from actual human evidence, expiry, use and invalidation history; a successor's
  revocation cannot revive an old grant. Existing current-session authorization
  remains valid before transcription and does not require repeat consent.
- Reconcile the standard, orchestrator and reviewer around bounded documentary
  create/append, immutable decision transcription and exactly six named projection
  refreshes. Operative permission/governance/agent-instruction changes remain
  excluded. TALI is not activated by this change.
- Keep Now/Next/Later horizons nonbinding. Readiness and confidence do not make
  human commitments, and moving a horizon does not cancel an actual commitment.
- Reclassify nine execution-capable skills as manual-only under the existing
  policy. Total skills stay **184**; manual skills change **18 → 27**. Their
  workflows and explicit-invocation fixtures preserve existing grants. ADR and
  reconciliation writers draft first; prompt/governance authors use a separate
  manual persistence route. Registry rows, narrative counts and consumer paths
  follow the actual posture.
- Fix the audit's raw-file line anchors in v1.13.1 without changing ARTF-001's
  semantic detector. Retain the earlier frozen v1.12.0 baseline and retired
  AEGIS-060 disposition.
- Extend the existing BER approval grader with optional, trusted, hash-bound
  lifecycle version 1.0.0. Preserve legacy plan hashes and result shapes. Strengthen
  the existing acceptance replay's full-document boundary check instead of adding
  an unused parallel authorization service.

## Evidence and limits

- [GitHub review corrections](github-review-fixes.md) records two findings on the
  first submitted revision, their fixes and corrected shipped-skill count proof.
- [Submitted implementation verification](verification.md) records exact commits,
  source-identity checks, raw logs, platform skips and final read-only reviews.
- [Prepared offline CI follow-up](offline-ci-followup.md) records the separately
  scoped next change; this PR does not claim that coverage is already hosted.
- [Complete candidate dispositions](candidate-dispositions.md),
  [machine-readable dispositions](candidate-dispositions.json), and the
  [unaltered fresh baseline](before.json) retain every semantic candidate.
- [After-remediation working audit](after-working.json) retains 80 semantic
  candidates and 308 informational route observations. [All residual candidate
  dispositions](remaining-candidates.json) explain why none remains a confirmed
  open defect; three regex matches remain after their contracts were repaired.
  A regex count of zero was never the acceptance criterion.
- [Lifecycle grader contract and limitations](../../approval-lifecycle-grading.md)
  distinguishes synthetic recorded-evidence checks from real consent, live
  execution and measured model behavior. New skill eval prompts/assertions are
  authored fixtures, not executed model-evaluation results.

Three independent read-only reviewers covered the semantic candidates, modified
skill contracts and connected evals, the approval grader, and actual replay code.
The collision sweep compared all 184 parsed descriptions against 19 changed jobs;
no newly introduced ownership collision was found. Inner-loop skill reviews
approved the repaired core and execution/draft slices, subject to final checks.
Code review found multiple Markdown-boundary bypasses; fixes have dedicated
negative cases rather than being waived by the earlier passing suite.

The first full Windows run found one schema-parity test that still assumed all
plan fields were mandatory. The corrected test checks required and optional keys
separately while retaining exact schema parity and the trusted-version constraint.
The original failed run is preserved with verification evidence.

Changes to `scripts/tests/` intentionally trigger the existing `gate-guard` manual
review route. No workflow, CODEOWNERS, DCO implementation or branch-protection
setting is weakened. The required GitHub approving review and any administrator
merge authorization must be resolved for the concrete submitted revision.

Measured WP-2B-3 calibration, replacement approved inputs and labels, holdout
execution, OD-1 and WP-2B-4 remain open. This change uses no provider credentials
or live requests and does not close the full historical AEGIS remediation program.
