# Issue #101 package 2 — conversational setup and Aegis-only scope

> **Current status, 2026-09-23:** Package 2 shipped in
> [PR #124](https://github.com/ModernNomad-98/Project-Aegis/pull/124)
> under [owner approval AEGIS-APR-007](../approvals/APPROVAL_REGISTER.md#aegis-apr-007-issue-101-conversational-setup-aegis-only-completion).
> The [setup plan](aegis-setup-routing-plan.md) and
> [delivery review](../evidence/setup/issue-101-package-2-review.md) describe
> the tested Windows PowerShell Aegis-only selection. The proposal below records
> the pre-implementation scope and keeps its original status wording as history.
> Helper routes and saved selection on other operating systems remain unavailable.

**Historical authorization proposal follows.**

Prepared 2026-09-23 from public `main` at
`fa79092f1c0fb1984b75245d8bce6a41982e5419`. **Proposal only.**
The [live issue #101](https://github.com/ModernNomad-98/Project-Aegis/issues/101)
and merged [package-1 plan](aegis-setup-routing-plan.md) define the product
direction. Package 1 delivered design in PR #109; it did not authorize a
setup skill or state writer. The public source repository has no shipped
`aegis-setup` skill today. This document sets a bounded implementation
decision for the owner; merging this proposal grants no runtime authority.

## Recommended first shippable slice

Deliver the four-choice conversation in the existing coding assistant and a
real **Aegis-only** completion path. Show **Aegis only**, **Aegis plus a local
helper**, **Aegis plus an online helper**, and **Help me choose** at entry.
Local and online helper paths remain `unavailable` until a separately selected,
tested integration ships. Exploration of either path always offers a return
to Aegis only. No named candidate is recommended or installed. Guidance asks
one plain-language preference at a time and never asks a user to estimate
RAM, GPUs or token thresholds.

The first supported persisted selection path is **Windows PowerShell on a
single user account and one local project checkout**. It uses the PowerShell
built into supported Windows versions; no Python, model, package or service
installation is required for Aegis-only completion. The skill files remain
self-contained so they copy with `.claude/skills/` into a consumer repository.
Other operating systems may use the conversation but must report saved-state
support as unverified/unavailable until a later tested implementation exists;
do not claim a completed remembered selection there. This deliberate initial
support limit is reviewed again in package 7 before broad release wording.

## Proposed exact implementation authority

The owner may approve one package-2 implementation PR **only after** the
approval is recorded in the Project Aegis owner register and the exact scope
record is merged. The proposed grant is:

The register is a protected path. The PR #104 guard exception is specific to
that PR and cannot be reused. If the future exact grant PR has the guard's
documented manual-review failure, prepare its verified candidate and seek a
separate narrow owner decision before merging; other failing checks remain
blocking. Do not bypass or weaken the guard to accelerate this package.

| Field | Bound |
| --- | --- |
| Repository/base | `ModernNomad-98/Project-Aegis` Role A; new implementation branch from the exact governance-grant merge, with later main reconciled before changes |
| Time | Maximum 12 active implementation hours, excluding owner/CI wait; stop and re-scope if exceeded. This is a ceiling; forecast remains 6–12 hours active. |
| Spend/data | USD $0 task-controlled external spend; synthetic test data only; no provider/model calls, credentials, real customer data, private holdouts or installs |
| Allowed implementation files | Exactly `.claude/skills/aegis-setup/SKILL.md`, `evals/evals.json`, `evals/trigger-evals.json`, `references/state-contract.md`, `scripts/selection.ps1`, `scripts/test-selection.ps1`; plus `docs/skills-catalog.md`, `README.md`, `docs/roadmaps/aegis-setup-routing-plan.md`, and `docs/evidence/setup/issue-101-package-2-review.md`. Add no other paths without owner-approved scope revision. The earlier grant transcription belongs in a separate governance PR, not this implementation file set. |
| Size | At most 1,200 added lines across skill/script/tests/docs. No generated dependency or binary asset. |
| Delivery | Focused DCO-signed PR, explicit-path staging, structural validation, meaningful PowerShell state tests on Windows and a read-only conversation/authority audit; final exact-head GitHub Actions all green before the standing-approved merge |
| Forbidden | Host routing hook, classifier/LLM adapter, provider account/connection, model recommendation, paid test, deployment, BER/CP changes, auto-merge or a claim of measured token savings |

The new skill is **manual-only** under the
[skill generation standard](../skill-generation-standard.md): its description
starts with `MANUAL-ONLY; never auto-invoke. ` and it sets
`disable-model-invocation: true` because saving a selection writes outside
scratch. The explicit phrases "Help me set up Aegis" and "Help me change my
Aegis setup" name the setup task and are the intended human invocations of
`aegis-setup`; a host with exact supported skill routing may use them to
present the four choices directly. If that host cannot establish a deliberate
setup invocation, it may present the four choices in ordinary conversation
but must request a named invocation before running the state writer. It may
not infer setup from a vague product idea or silently write state. The skill
must not trigger on
ordinary engineering tasks or displace `project-orchestrator`'s product
stage navigation. Its evals include explicit setup/change triggers and
nontriggers for vague product requests, security reviews, BER runs, ordinary
skill selection and instructions that ask for a different skill. The repo's
validator checks eval structure, not conversational behavior; manual review
must inspect the actual flow and wording.

## Saved-state contract to prove

- **Location/scope:** one user-local Windows record under
  `%LOCALAPPDATA%\ProjectAegis\setup\v1\`, keyed by SHA-256 of a canonical
  physical checkout root. It is never written into the public source or a
  consumer repository by default. A copied project on another host starts
  unselected and may be configured again. No synchronization is implied.
- **Record:** closed versioned JSON containing the project key, choice,
  `selected/configured/verified/unavailable` state, selected/updated UTC
  timestamps, a distinct `setup_completed_at_utc` field and evidence version
  where applicable. Never store a raw credential, task text, transcript or
  model result. Package 2 records Aegis-only as `selected` with a completion
  timestamp; it does not use `verified`, which remains reserved for a proven
  host/helper invocation. A helper choice remains `unavailable` even if
  selected.
- **Writer:** canonicalize and validate the project path; verify the state
  directory is user-local, not a reparse redirect or checkout path; create a
  temporary record in the same directory, flush it, then perform a verified
  atomic same-volume create/replace. If atomic replacement is unsupported or
  fails, preserve the previous valid record, report save failure and do not
  claim completion. Use a bounded lock or reject concurrent writers. A failed
  save cannot say completion succeeded. Reject unknown schema versions and
  malformed/ambiguous records without silently upgrading them.
- **Recovery:** a missing record is `unselected` with ordinary Aegis behavior;
  corruption yields a clear repair/change prompt and no helper activation.
  `Help me change my Aegis setup` reads the record, shows its scope/status,
  permits explicit switch to Aegis only and invalidates any former helper
  status. Tests cover fresh selection, persistence across sessions, overwrite,
  corrupt/versioned state, concurrency, a moved checkout and a failed write.

The state record is a preference, **not** authority to invoke any provider or
write tool. Package 3/4 later owns host integration and eligibility. No future
helper can infer `verified` solely from this file or silently switch local
failure to online processing.

## Acceptance and next gate

The human can complete Aegis-only setup directly after the four choices,
through Help me choose, and while leaving either unavailable add-on path.
Every path explains who it suits, extra setup/cost, possible token effect,
difficulty rationale and where selected text would be processed. It says
explicitly that tokens are text-processing units, that savings are unmeasured,
that existing assistant costs remain, and that local routing would not make
the whole workflow offline. The online path does not imply an account exists
or accept a credential. Selection and persisted status are recoverable in a
later session on the supported Windows host; no false provider verification.

After local PowerShell tests and structural validation, an independent
reviewer checks trigger overlap, state/side-effect boundary, honest unavailable
wording and all user paths. The PR reports exact commands/exits and remaining
OS limitations. Package 2 can be marked delivered only for the tested scope.
Packages 3–7 and any local/online integration still require their own grants,
host evidence and comparison results. Accepting this proposal does not select
GLiClass, Jev or any other model.
