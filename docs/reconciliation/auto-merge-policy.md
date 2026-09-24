# Auto-Merge Policy

This page describes who may merge a pull request (PR) and how the project's
continuous integration (CI) checks affect that decision. `AEGIS-APR-002` is
entry 002 in the owner approval register; `gate-guard` is the CI job that
flags protected-file changes for manual review. The dated `D34` code below
names a decision in the reconciliation record.

## Current policy — recorded 2026-09-12

Human authority governs merges. For `ModernNomad-98/Project-Aegis`, the owner
has granted recurring administrator-merge authority in
[AEGIS-APR-002](../approvals/APPROVAL_REGISTER.md#aegis-apr-002-administrator-merges).
Agents may use that grant for authorized delivery without asking for the same
approval again. Read the full register and any later lifecycle events before use.
The grant applies to this source repository's clones and worktrees; copied
startup files and skills do not grant authority over a consumer repository.

**Current reading, 2026-09-23:** The owner's later all-green GitHub Actions
instruction makes a PR-specific decision necessary before merging a reviewed
PR whose only failed check is the protected-file guard. The standing
administrator grant authorizes the merge mechanism for otherwise authorized
work; it does not itself decide a new failed-check exception. Require the
final reviewed revision, passing Linux and Windows jobs, an independent audit
without blockers, and the owner's exact-PR exception. Approval entries
[AEGIS-APR-005](../approvals/APPROVAL_REGISTER.md#aegis-apr-005-pr-104-protected-file-guard-exception)
and [AEGIS-APR-010](../approvals/APPROVAL_REGISTER.md#aegis-apr-010-pr-119-protected-file-guard-exception)
applied only to PRs #104 and #119. The later offline Behavioral Eval Runner
grant [AEGIS-APR-012](../approvals/APPROVAL_REGISTER.md#aegis-apr-012-offline-behavioral-eval-runner-evidence-policy-proof)
expressly does not waive a future guard failure. Keep the guard and branch
settings intact. When all checks are green, authorized work may use the
standing administrator grant without another merge-mechanism request.

Verify the reviewed PR revision and both offline verification jobs before merge.
An intentional protected-file `gate-guard` failure requires explicit review of
the affected enforcement surfaces. The older recorded grant included a guard
bypass, subject to the later all-green instruction above; do not weaken checks
or change repository settings to make a change mergeable. Auto-merge is not armed.

See [offline CI](../offline-ci.md) for current job names, protected paths and
post-merge verification, and [CONTRIBUTING](../../CONTRIBUTING.md) for delivery rules.

The historical policy below predates this owner grant and the expanded offline
CI guard. Its original dates, incident description and old guard message are
retained as history, rather than current instructions to request repeat consent.

## Historical policy and D34 correction

**Recorded:** 2026-07-06
**Repo:** `nguyenpv1980-wq/Claude-Skills` (renamed → `nguyenpv1980-wq/Project-Aegis` → `ModernNomad-98/Project-Aegis`; old URLs redirect)
**Context:** companion decision to the CI merge gate
([`.github/workflows/validate-skills.yml`](../../.github/workflows/validate-skills.yml));
extends the decisions in [`step-0-reconciliation-v4.md`](step-0-reconciliation-v4.md).

> **Correction (D34, 2026-07-10).** This document originally specified an **opt-in, per-phase
> auto-merge** mechanism (`gh pr merge --auto --squash`). Per the repo owner, that mechanism
> was **never adopted**: Aegis's entire development used **manual merge** by a human after the
> required checks passed, and auto-merge was never armed as policy. The policy below is
> corrected forward to describe the actual process; the original auto-merge-arming wording is
> summarized inline for provenance, not silently removed. See reconciliation §5, decision D34.
> The one time auto-merge fired — PR #7 — was the unauthorized incident recorded in §6, which
> is precisely why merge stays human-gated.

### Policy recorded in July 2026

1. **Merge is manual — a human is the gate.** Every PR is reviewed and merged by a human
   after all required status checks (`validate-skills` and `gate-guard`) pass. **Auto-merge is
   never armed** for this project's development. (The superseded original policy made
   auto-merge an opt-in, per-phase step via `gh pr merge --auto --squash`; that arming step was
   never adopted — see the correction above.)

2. **Merge-gate changes are never auto-merged.** Any change touching the merge gate itself —
   anything under `.github/workflows/` or the file `scripts/validate-skills.py` — always
   requires **manual human review and merge**, regardless of phase or opt-in status. The
   `gate-guard` job enforces this mechanically by failing such PRs with:

   > This PR modifies the merge gate itself and requires manual review and merge.

   A `gate-guard` failure is the intended signal, not a defect. Do not weaken the gate,
   rename its jobs, or bypass the failing check to "make CI green"; a human merges these
   PRs deliberately after reviewing the gate change.

### Historical rationale

The gate exists so skill-generation work lands safely: a human merges each validated PR, and
any PR that edits the validator or the workflows must be reviewed and merged manually
regardless. Keeping merge human-gated — never auto-armed — is the direct lesson of the
ungoverned-auto-merge incident (PR #7) this project absorbed and now encodes as an
`agent-authorization-matrix` eval. An auto-merge-arming step could otherwise loosen the checks
and then merge on its own (now weaker) green run; requiring a human at the merge keeps every
landing deliberate.
