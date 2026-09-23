# Operational proposal status pointers — 2026-09-23

## Scope

This documentation-only batch starts from `37c018d166f0647703b4a0f7009ae0ca4c5e32b0`
(merged pull request #169). Five historical proposal and decision pages now
begin with dated current-state pointers:

- [Issue #101 package 2](../../roadmaps/aegis-setup-package-2-authorization-proposal.md)
  and [package 3](../../roadmaps/aegis-setup-package-3-authorization-proposal.md):
  their separate owner grants and merged deliveries are clear; neither page
  suggests a helper or real host hook has shipped.
- [Measured calibration decision package](../../roadmaps/behavioral-eval-runner-wp-2b-3-authorization-decision-package.md):
  work package 2B-3 is authorized but incomplete; historical pre-merge
  prohibitions and the signed 35 decisions remain in place.
- [Evidence-policy decision](../../roadmaps/ber-bkl-009-evidence-policy-decision.md)
  and [offline proof scope](../../roadmaps/ber-bkl-009a-offline-policy-scope-proposal.md):
  the selected 30-day policy and later synthetic-only proof grant are distinct.
  Real-host controls and cleanup remain separate gates.

Original proposal and decision bodies compare equal after removing the new
opening pointers and labels. No approval-register, execution-metrics, runtime,
provider or private-input file changed.

## Verification and limits

- The local source tree contains merged setup [PR #121](https://github.com/ModernNomad-98/Project-Aegis/pull/121)
  and [PR #124](https://github.com/ModernNomad-98/Project-Aegis/pull/124),
  owner approvals AEGIS-APR-007/008/009/012, and Behavioral Eval Runner
  decisions BER-DEC-008/011.
- Pull request #139 is absent from this merge tree. A live GitHub check at
  2026-09-23 21:13 UTC found it OPEN at
  `8928383f0838e2d99ee3a89c44b98b7aba7f1c9b`: Linux and Windows passed,
  and the protected-file guard failed. Recheck its live state before acting.
- `python -B scripts/validate-skills.py`: 185 valid skills, zero warnings.
- All relative link targets in the five pages exist; `git diff --check` passed.
- Independent read-only review: pending on the frozen draft.

The previous small-guide estimate was 2–4 active hours; this batch's estimate
is 2–4 active hours. The selected backlog remains provisionally 175–394
active hours. Preparation and editing began at 21:10:19 UTC. Active-only time
is not instrumented; the frozen-draft wall interval is recorded below.

**Frozen draft:** 21:12:34 UTC, 2m15s observed wall time from the first
preparation checkpoint.
