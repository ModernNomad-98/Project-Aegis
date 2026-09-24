# Issue #101 package 3 — offline advisory-contract scope

**Reader key:** This page is for the owner and reviewers of issue #101 package
3. An identifier (ID) names a catalog entry; the Developer Certificate of
Origin (DCO) is commit sign-off; continuous integration (CI) runs automated
checks. Behavioral Eval Runner (BER) names the separate evaluation tool;
control plane (CP) names the delivery kernel. The package 3 advisory contract
has shipped, while the proposal below preserves its earlier decision context.
A pull request (PR) proposes a repository change; `AEGIS-APR` identifies an
entry in the owner approval register.

> **Current status, 2026-09-23:** Package 3 shipped in
> [PR #121](https://github.com/ModernNomad-98/Project-Aegis/pull/121)
> under [owner approval AEGIS-APR-008](../approvals/APPROVAL_REGISTER.md#aegis-apr-008-issue-101-offline-advisory-routing-contract).
> Package 2 also shipped in
> [PR #124](https://github.com/ModernNomad-98/Project-Aegis/pull/124)
> under [AEGIS-APR-007](../approvals/APPROVAL_REGISTER.md#aegis-apr-007-issue-101-conversational-setup-aegis-only-completion).
> See the [setup plan](aegis-setup-routing-plan.md) and
> [package-3 review](../evidence/setup/issue-101-package-3-review.md) for the
> delivered boundaries. The advisory contract has no real host hook or dispatch.
> The proposal below preserves its earlier package-2 status as history.

**Historical authorization proposal follows.**

Prepared 2026-09-23 from public `main` at
`d187849287e5047fc821f7a1070b0c59cc5b32b9`. **Historical proposal.**
The owner approved this bounded scope in AEGIS-APR-008, effective at merge
`1af342712d27d5e6ea482b3f451106b4dccaf125`. The implementation evidence
is in [the package-3 review](../evidence/setup/issue-101-package-3-review.md).
The [live issue #101](https://github.com/ModernNomad-98/Project-Aegis/issues/101)
and [package-1 design](aegis-setup-routing-plan.md) define the feature. The
[package-2 proposal](aegis-setup-package-2-authorization-proposal.md) covers
conversation and saved selection, but has no implementation grant yet.
Package 3 can specify and test an offline decision seam independently of the
package-2 state writer. Merging this document grants no runtime authority.

## Recommended delivery

Create one provider-neutral, **advisory-only** Python standard-library contract
and synthetic fake adapter. It accepts a bounded task synopsis, stage and
catalog/policy versions, eligible agent and skill IDs with short descriptions,
and the host's mandatory agent/skill and explicit user selections. It returns
known offered IDs or an explicit abstain. The host remains the authority for
eligibility, required reviewers, manual-only restrictions, approvals and
dispatch. A decision cannot change an agent's permissions or claim completion.

The first implementation has **no host hook**. Its compatibility checker takes
synthetic installed-catalog facts and reports `compatible`, `unsupported` or
`unknown` with reasons; it does not probe or claim support for an unselected
real assistant version, machine, model or provider. A fake adapter exercises
malformed, unknown-ID, stale-version, missing-mandatory, forbidden-manual-only,
timeout, overlong and ambiguous responses. Every such case returns a typed
fail-closed disposition for a future host to consume. The offline contract
neither dispatches nor contacts an online service; actual Aegis-only fallback
remains a later host-integration proof.

## Proposed exact implementation grant

The owner may approve this bounded package only after a separate approval
register entry and exact-scope governance PR are reviewed and merged. The
implementation branch starts at that exact merged grant commit; later changes
to issue #101, the package-1 design, or package-2 state contract are reconciled
before code. Accepting this proposal PR alone does not grant the code work.

| Field | Proposed bound |
| --- | --- |
| Repository | `ModernNomad-98/Project-Aegis`, source-library Role A; no consumer repository writes |
| Exact implementation paths | `tools/aegis_setup/__init__.py` (new); `tools/aegis_setup/routing_contract.py` (new); `tools/aegis_setup/tests/test_routing_contract.py` (new); `tools/aegis_setup/README.md` (new); `docs/roadmaps/aegis-setup-routing-plan.md`; `docs/roadmaps/aegis-setup-package-3-authorization-proposal.md`; `docs/evidence/setup/issue-101-package-3-review.md` (new). The separate grant must repeat this exact list. |
| Time and size | Maximum 12 active implementation hours and 1,200 added code/test lines; stop and re-scope before exceeding either. The current package-3 forecast is 6–12 active hours. |
| Spend and data | USD $0 task-controlled external spend; synthetic temporary fixtures only. No install, download, dependency change, credential, provider/model call, customer data, sealed holdout or external transmission. |
| Delivery | One DCO-signed PR, exact-path staging, local focused tests and skill validation, independent contract/authority review, all exact-head GitHub Actions green before merge under the standing merge approval. |
| Outside this grant | `.claude/skills/`, setup-state writer, real host bridge/hook, provider-specific adapter, model weights, classifier inference, online connection, CI changes, BER/CP paths, deployment and claims of measured accuracy or token savings. |

The protected approval register is transcribed in a **separate governance PR**
after the owner grants the scope. Its protected-file guard must be handled on
that PR's own evidence and owner decision; the PR #104-only exception is not
reusable. No implementation begins merely because this proposal merges.

## Contract acceptance

- The request has a closed version and strict byte/item bounds. It contains
  only a short, one-line task synopsis and the offered IDs/descriptions needed
  for this decision. No fields for raw conversation, repository files or
  arbitrary tool output are accepted. The parser rejects common URL, path and
  secret-marker shapes, but cannot establish that free text contains no
  sensitive data. A future host must curate the synopsis before sending it
  to any adapter. Identifier and version comparisons are exact.
- The host supplies eligibility and mandatory sets before a helper is called.
  A helper may rank or abstain among offered IDs; it cannot add an ID, remove a
  mandatory specialist/skill, select a manual-only skill without explicit user
  invocation, or convert a read-only reviewer into a writer.
- The result distinguishes `recommend`, `abstain`, `timeout`, `invalid` and
  `unavailable` without turning model confidence into an authorization. A
  score is optional and has no cross-provider meaning until calibrated.
- The checker treats missing, contradictory or stale catalog/policy facts as
  `unknown` or `unsupported`, never as verified host compatibility. Each
  synthetic negative case demonstrates that the contract returns no dispatch
  authority or online destination. Actual host fallback is not claimed.
- Tests cover valid subsets, empty offers, duplicate IDs, unknown IDs, missing
  mandatory IDs, explicit selections, manual-only skill attempts, stale and
  malformed versions, oversized data, timeout/error, and local-to-online
  fallback attempts. No mocked pass may be reported as a real host proof.

Package 4 still needs a selected host/version, an actual pre-dispatch hook,
verified consumption/fallback, frozen evaluation inputs and separate authority.
Packages 5/6 remain conditional on that evaluation and the owner's selection.
Package 7 cannot claim end-to-end release readiness from this offline seam.
