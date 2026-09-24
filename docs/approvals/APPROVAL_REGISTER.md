# Project Aegis owner approval register

This is the documentary record of Peter Nguyen's grants for the
`ModernNomad-98/Project-Aegis` source repository. It applies to work on that
repository from its clones and local worktrees. Copying Aegis skills or startup
files into another repository does not transfer these grants.

Grant entries are immutable. Append later revocation, expiry, consumption or
supersession events with unique IDs and the affected grant ID; do not edit old
entries. An action is covered only by an effectively ACTIVE human grant whose
scope includes it, after considering the full history and any actual limits.
Historical ACTIVE text alone is insufficient. Current direct user instructions
are valid source evidence before transcription and do not need repeated consent.

This record preserves the owner's decisions; it does not create them or change
GitHub settings. Project-specific direct owner grants take precedence over
generic skill guidance that would require asking for the same approval again.

## Grants and lifecycle events

### AEGIS-APR-001: Read-only agents

- **Event:** GRANT
- **Status at recording:** ACTIVE
- **Date / Grantor:** Peter Nguyen; grant present in the project conversation,
  previously transcribed locally on 2026-09-10; recorded here on 2026-09-12.
- **Reason:** Preserve the standing instruction across sessions and computers.
- **Scope allowed:** The owner's exact instruction was: "yes, read only agaent
  are always allowed. Keep this in your working memory permanently for this
  project". Read-only agents for Project Aegis may be used without asking again.
- **Scope FORBIDDEN:** None additionally stated. This is a read-only-agent grant;
  authority for other actions comes from their applicable task instructions.
- **Evidence:** Verbatim owner instruction in the Project Aegis conversation
  history; the prior local transcription was in
  `C:/Users/PeterNguyen/.codex/AGENTS.md`. The source grant is the human message,
  not that local file. This repository record makes it recoverable from GitHub.
- **Expiry / use limit:** None stated; recurring use, not a one-use grant.

### AEGIS-APR-002: Administrator merges

- **Event:** GRANT
- **Status at recording:** ACTIVE
- **Date / Grantor:** 2026-09-12 / Peter Nguyen.
- **Reason:** Approve PR #91's administrator merge and eliminate repeated
  administrator-merge approval requests for subsequent Project Aegis work.
- **Scope allowed:** The owner's exact instruction was: "approved. I
  pre-approved all administrator merge moving forward". This approves the
  proposed administrator merge of PR #91 at
  `69915fec415cddfce608eed7fd4f989d226af903`, bypassing its protected-file guard
  and missing GitHub approving review, and grants standing approval for future
  administrator merges in this project. No new case-by-case consent is required
  merely because an authorized delivery uses an administrator merge.
- **Scope FORBIDDEN:** None additionally stated. The grant concerns
  administrator merges in this project; it does not itself instruct agents to
  start unrelated work or change repository settings.
- **Evidence:** Current-session owner message on 2026-09-12, quoted above,
  responding to: "Approve administrator merge of PR #91 at `69915fe`, bypassing
  those two requirements?" The preceding request identified the protected-file
  guard and missing GitHub approving review. PR:
  <https://github.com/ModernNomad-98/Project-Aegis/pull/91>.
- **Expiry / use limit:** None stated; "all administrator merge moving forward"
  is recurring authority, not consumed by PR #91 or another routine use.

### AEGIS-APR-003: Pull request updates

- **Event:** GRANT
- **Status at recording:** ACTIVE
- **Date / Grantor:** 2026-09-13 / Peter Nguyen; recorded here on 2026-09-17.
- **Reason:** Preserve the standing pull-request update instruction across
  sessions and computers.
- **Scope allowed:** The owner's exact instruction was: "yes, i pre-approve all
  updates to PRs as needed". Project Aegis pull requests may be updated as
  needed without repeated case-by-case consent.
- **Scope FORBIDDEN:** None additionally stated. This grant concerns updates to
  pull requests; authority to start unrelated work or perform actions beyond a
  pull-request update comes from the applicable task instructions.
- **Evidence:** Direct owner instruction in the Project Aegis conversation on
  2026-09-13, quoted above and durably transcribed in the description of
  [PR #95](https://github.com/ModernNomad-98/Project-Aegis/pull/95).
- **Expiry / use limit:** None stated; recurring use, not a one-use grant.

### AEGIS-APR-004: CP-WP-002 offline kernel implementation

- **Event:** GRANT
- **Status at recording:** ACTIVE
- **Date / Grantor:** 2026-09-17 / Peter Nguyen.
- **Reason:** Authorize the separately gated CP-WP-002 offline state and
  recovery kernel after completion of CP-WP-001.
- **Scope allowed:** The owner's exact instruction was: "a", selecting option
  A, "Approve the proposed CP-WP-002 scope", in direct response to the
  2026-09-17 approval request. That proposal authorizes implementation under
  `tools/aegis_delivery_control/` using a standard-library SQLite transactional
  store under the OS user-state directory, a repository-wide stable OS lock,
  one outstanding synthetic operation, process-crash atomicity with
  `synchronous=FULL`, fail-closed uncertain/corrupt/stale recovery, an injected
  synthetic freshness oracle, synthetic-only adapters, the complete versioned
  budget lifecycle, and synthetic T01-T28, C01-C09 and F01-F21 tests. It also
  authorizes the corresponding README and update to
  `docs/roadmaps/resumable-control-plane-backlog.md` with scope and evidence.
- **Scope FORBIDDEN:** As stated in the proposal: no BER changes, dependency or
  CI changes, production data, external or provider calls, releases, Git
  mutation by the kernel, or artifact-directory changes. No real authority
  source, credential, deployment or real execution adapter is authorized.
- **Evidence:** Current-session owner message on 2026-09-17, quoted above,
  responding to the immediately preceding structured approval request whose
  option A and proposed technical contract are summarized in this entry.
- **Expiry / use limit:** Applies to the proposed CP-WP-002 implementation
  package; no calendar expiry stated.

### AEGIS-APR-005: PR #104 protected-file guard exception

- **Event:** GRANT
- **Status at recording:** ACTIVE
- **Date / Grantor:** 2026-09-23 / Peter Nguyen.
- **Reason:** Resolve the explicit conflict between the 2026-09-23 all-green
  Actions instruction and the guard's documented manual-review failure for
  protected BER files in PR #104.
- **Scope allowed:** The owner's exact answer was "Permit this narrow exception"
  to the question: "For PR #104 only, may I use the pre-approved administrator
  merge despite the documented protected-file gate-guard failure? Linux and
  Windows verification passed, and the independent audit found no blocker.
  The 2026-09-23 handoff says this narrow exception still needs your explicit
  decision because your newer instruction requires all Actions green."
  This permits an administrator merge of PR #104 when the sole failed check
  on its final candidate is that documented guard condition, all execution
  and test jobs pass, and independent audits have no unresolved blocker.
- **Scope FORBIDDEN:** The grant does not excuse another failed check, waive
  BER-BKL-007's separate final-shape owner acceptance, change the guard or
  branch protection, or apply to another PR.
- **Evidence:** The owner's direct answer in the Project Aegis conversation
  on 2026-09-23, quoted above, after the exact PR #104 check results were
  presented. The final PR revision and check results must be verified again
  before use.
- **Expiry / use limit:** PR #104 only; one merge at most. No calendar expiry
  stated.

### AEGIS-APR-006: Control-plane offline capability proofs, first increment

- **Event:** GRANT, effective only after this reviewed register change merges.
- **Status at recording:** ACTIVE on that merge.
- **Date / Grantor:** 2026-09-23 / Peter Nguyen.
- **Owner decision:** "go with your recommendations and approve. do not stop,
  keep going until all backlogs and issues are resolved per original goal. DO
  NOT STOP!" This answered the immediately preceding recommendation to approve
  the bounded control-plane work package 003A proposal in
  [PR #114](https://github.com/ModernNomad-98/Project-Aegis/pull/114).
- **Reason:** Authorize the first offline proof increment after the completed
  synthetic recovery kernel, without declaring a real source or host ready.
- **Scope allowed:** Build only the synthetic, offline capability proof and
  fail-closed dispatch interface described in
  [the exact proposal](../roadmaps/cp-wp-003-offline-proof-proposal.md).
  Start its implementation branch at this grant's exact merge commit. The
  implementation may use Python's standard library, synthetic temporary
  fixtures, checked read-only probes, and the proposal's negative tests.
- **Exact implementation files:** `tools/aegis_delivery_control/capabilities.py`
  (new), `tools/aegis_delivery_control/authority.py`,
  `tools/aegis_delivery_control/adapters.py`,
  `tools/aegis_delivery_control/dispatch.py`,
  `tools/aegis_delivery_control/evidence.py`,
  `tools/aegis_delivery_control/owned_paths.py`,
  `tools/aegis_delivery_control/README.md`,
  `tools/aegis_delivery_control/tests/test_capabilities.py` (new),
  `tools/aegis_delivery_control/tests/test_dispatch.py`,
  `tools/aegis_delivery_control/tests/test_platform.py`,
  `tools/aegis_delivery_control/tests/test_recovery.py`,
  `docs/roadmaps/resumable-control-plane-backlog.md`, and
  `docs/evidence/control-plane/cp-wp-003a-review.md` (new).
- **Scope FORBIDDEN and size limits:** At most 10 active implementation hours
  and 2,000 added code/test
  lines; zero task-controlled external spending. No real authority source,
  credential, customer data, provider call, deployment, real mutation, or
  phase advance. The public command-line interface stays synthetic-only.
  Source and host guarantees remain unproven until separately selected and
  tested. Stop for a reviewed scope change before exceeding any bound.
- **Delivery:** One signed implementation pull request, local Windows and
  pinned Linux checks, independent architecture/security/quality review, and
  all exact-head GitHub Actions green before merge. This grant does not waive
  a protected-file guard failure on that future request.
- **Evidence:** Direct owner instruction quoted above, following the exact
  PR #114 recommendation and proposal. PR #114 alone was a proposal; this
  reviewed register merge is its required implementation gate.
- **Expiry / use limit:** One bounded implementation package; no calendar
  expiry stated. Scope revisions require a separate reviewed owner decision.

### AEGIS-APR-007: Issue #101 conversational setup, Aegis-only completion

- **Event:** GRANT, effective only after this reviewed register change merges.
- **Status at recording:** ACTIVE on that merge.
- **Date / Grantor:** 2026-09-23 / Peter Nguyen.
- **Owner decision:** The same direct approval quoted in AEGIS-APR-006 answered
  the recommendation to approve the bounded package-2 proposal in
  [PR #113](https://github.com/ModernNomad-98/Project-Aegis/pull/113).
- **Reason:** Deliver a truthful Aegis-only setup path before selecting or
  connecting any optional routing helper.
- **Scope allowed:** Implement the four-choice, manually invoked setup
  conversation and an Aegis-only saved selection on tested single-user Windows
  PowerShell, following [the exact proposal](../roadmaps/aegis-setup-package-2-authorization-proposal.md).
  Start from this grant's exact merge commit. Helper integrations remain
  unavailable. Other operating systems may show the conversation but cannot
  claim saved-state support until separately tested.
- **Exact implementation files:** `.claude/skills/aegis-setup/SKILL.md`,
  `.claude/skills/aegis-setup/evals/evals.json`,
  `.claude/skills/aegis-setup/evals/trigger-evals.json`,
  `.claude/skills/aegis-setup/references/state-contract.md`,
  `.claude/skills/aegis-setup/scripts/selection.ps1`,
  `.claude/skills/aegis-setup/scripts/test-selection.ps1`,
  `docs/skills-catalog.md`, `README.md`,
  `docs/roadmaps/aegis-setup-routing-plan.md`, and
  `docs/evidence/setup/issue-101-package-2-review.md` (new).
- **Scope FORBIDDEN and size limits:** At most 12 active implementation hours
  and 1,200 added lines
  across code, tests and documentation; zero task-controlled external spending.
  No install, credential, provider/model call, customer data, private holdout,
  host routing hook, classifier, deployment, or claimed measured token saving.
  The setup skill is manual-only; a saved choice grants no provider authority.
  Stop for a reviewed scope change before exceeding any bound.
- **Delivery:** One signed implementation pull request with explicit file
  staging, meaningful Windows PowerShell state tests, structural validation,
  independent conversation/authority review, and all exact-head GitHub Actions
  green before merge. This grant does not waive a future guard failure.
- **Evidence:** Direct owner instruction quoted in AEGIS-APR-006, following the
  exact PR #113 recommendation and proposal.
- **Expiry / use limit:** One bounded package-2 implementation; no calendar
  expiry stated. Scope revisions require a separate reviewed owner decision.

### AEGIS-APR-008: Issue #101 offline advisory routing contract

- **Event:** GRANT, effective only after this reviewed register change merges.
- **Status at recording:** ACTIVE on that merge.
- **Date / Grantor:** 2026-09-23 / Peter Nguyen.
- **Owner decision:** The same direct approval quoted in AEGIS-APR-006 answered
  the recommendation to approve the bounded package-3 proposal in
  [PR #115](https://github.com/ModernNomad-98/Project-Aegis/pull/115).
- **Reason:** Prove a host-neutral advisory contract without granting a helper
  dispatch or a real host integration.
- **Scope allowed:** Build the provider-neutral, advisory-only offline
  contract, compatibility checker and synthetic fake adapter in
  [the exact proposal](../roadmaps/aegis-setup-package-3-authorization-proposal.md).
  Start from this grant's exact merge commit; the host retains all eligibility,
  approval and dispatch authority. There is no real host hook.
- **Exact implementation files:** `tools/aegis_setup/__init__.py` (new),
  `tools/aegis_setup/routing_contract.py` (new),
  `tools/aegis_setup/tests/test_routing_contract.py` (new),
  `tools/aegis_setup/README.md` (new),
  `docs/roadmaps/aegis-setup-routing-plan.md`,
  `docs/roadmaps/aegis-setup-package-3-authorization-proposal.md`, and
  `docs/evidence/setup/issue-101-package-3-review.md` (new).
- **Scope FORBIDDEN and size limits:** At most 12 active implementation hours
  and 1,200 added code/test
  lines; zero task-controlled external spending. Synthetic temporary fixtures
  only. No install, dependency change, credential, provider/model call,
  customer data, private holdout, real host bridge, model weights, classifier
  inference, deployment, or measured accuracy/token-saving claim. Stop for a
  reviewed scope change before exceeding any bound.
- **Delivery:** One signed implementation pull request, exact-path staging,
  local focused tests and skill validation, independent authority review, and
  all exact-head GitHub Actions green before merge. This grant does not waive a
  future guard failure.
- **Evidence:** Direct owner instruction quoted in AEGIS-APR-006, following the
  exact PR #115 recommendation and proposal.
- **Expiry / use limit:** One bounded package-3 implementation; no calendar
  expiry stated. Scope revisions require a separate reviewed owner decision.

### AEGIS-APR-009: Behavioral Eval Runner evidence-policy selection

- **Event:** POLICY DECISION. This selects a policy target; it does not grant
  implementation, deletion or a live run.
- **Status at recording:** ACTIVE on this reviewed register merge.
- **Date / Grantor:** 2026-09-23 / Peter Nguyen.
- **Owner decision:** The same direct approval quoted in AEGIS-APR-006 answered
  the recommendation to use the [30-day complete-bundle evidence policy](../roadmaps/ber-bkl-009-evidence-policy-decision.md)
  proposed in [PR #108](https://github.com/ModernNomad-98/Project-Aegis/pull/108).
- **Reason:** Select the retention, reader and encryption target needed before
  a separately scoped evidence-policy implementation can be proposed.
- **Scope allowed (selected policy):** One 30-calendar-day clock from first
  evidence creation
  for the complete Stage A and Stage B runtime verification bundle, including
  the detached marker. Expiration makes cleanup eligible for owner review;
  failures and incomplete runs remain preserved until resolved and reviewed.
  The owner and required runner/verifier components are the intended readers;
  the current Windows work package 2B-3 root requires owner plus operating-system
  SYSTEM access and host-verified BitLocker encryption before use. A different
  selected host requires its own verified mechanism and access decision.
  Private versioned calibration inputs remain in the separate owner-only
  repository until an owner-reviewed deletion; public Git holds only reviewed
  sanitized records. The proposal's reader matrix, redaction, publication and
  marker-gated cleanup controls are the policy target.
- **Scope FORBIDDEN:** Current metadata and operating-system enforcement are
  incomplete. Behavioral Eval Runner backlog item 009 remains partially
  delivered. A separately reviewed decision-log amendment must define exact
  code/runbook scope before implementation. This decision grants no automatic
  deletion, additional reader, provider call, holdout access, or measured
  result.
- **Evidence:** Direct owner instruction quoted in AEGIS-APR-006, following the
  PR #108 evidence-policy recommendation and decision options.
- **Expiry / use limit:** No calendar expiry or one-use limit stated. This is
  a policy selection; any replacement requires a later recorded owner choice.

### AEGIS-APR-010: PR #119 protected-file guard exception

- **Event:** GRANT.
- **Status at recording:** Consumed by the lifecycle event below.
- **Date / Grantor:** 2026-09-23 / Peter Nguyen.
- **Reason:** Resolve the documented protected-file guard failure on the
  Behavioral Eval Runner documentation change in PR #119.
- **Scope allowed:** The owner's exact answer was "Permit a PR #119-only
  administrator merge with this documented guard failure (recommended)" to
  the question: "PR #119 is independently reviewed and mergeable at `985209c`.
  Linux and Windows passed; `gate-guard` failed solely because it protects the
  Behavioral Eval Runner README that this PR rewrites. The handoff's prior
  exception covered PR #104 only, while your newer rule requires green
  Actions. Which disposition do you approve for PR #119?" The approval
  permits the administrator merge of this reviewed revision despite that
  specific failed guard check.
- **Scope FORBIDDEN:** It does not apply to another pull request or any other
  failed check, and does not alter branch protection or the guard itself.
- **Evidence:** Direct owner reply in the Project Aegis conversation on
  2026-09-23, quoted above; the exact revision and check results are recorded
  in [PR #119](https://github.com/ModernNomad-98/Project-Aegis/pull/119#issuecomment-5799428285).
- **Expiry / use limit:** PR #119 only, one merge. No calendar expiry stated.

### AEGIS-APR-011: Consumption of PR #119 guard exception

- **Event:** CONSUMED; target grant AEGIS-APR-010.
- **Status at recording:** AEGIS-APR-010 has no remaining use.
- **Effective at:** 2026-09-23 17:18:03 UTC.
- **Recorded at / By:** 2026-09-23 / Project Aegis agent, transcribing the
  completed merge.
- **New authority:** None.
- **Reason:** The sole approved administrator merge completed.
- **Evidence:** [PR #119](https://github.com/ModernNomad-98/Project-Aegis/pull/119)
  merged as `d2053b61fa80738d9dd2c669980652914bb5c872`. Its final timing and
  check disposition are in [the completion comment](https://github.com/ModernNomad-98/Project-Aegis/pull/119#issuecomment-5799438319).

### AEGIS-APR-012: Offline Behavioral Eval Runner evidence-policy proof

- **Event:** GRANT, effective only after this reviewed register and
  Behavioral Eval Runner decision-log change merges.
- **Status at recording:** ACTIVE on that merge.
- **Date / Grantor:** 2026-09-23 / Peter Nguyen.
- **Owner decision:** "A. Approve bounded offline proof (recommended)" in
  response to the question presenting [PR #131's exact proposal](../roadmaps/ber-bkl-009a-offline-policy-scope-proposal.md): APR-009 selected the
  30-day policy but requires a separate implementation grant; option A permits
  only the offline synthetic proof after its exact grant is recorded and
  merged, excluding real inputs, provider calls, deletion and a future
  protected-file guard exception.
- **Reason:** Prove the selected complete-bundle evidence contract before any
  real-host storage or cleanup implementation.
- **Scope allowed:** One synthetic-only WP-2B-1B policy checker and
  regression package for child item BER-BKL-009, under the seven exact paths
  and acceptance evidence in
  the merged PR #131 proposal. Start its implementation branch from this
  grant's exact merge commit. The paired append-only decision is BER-DEC-011
  in [the Behavioral Eval Runner governance log](../roadmaps/behavioral-eval-runner-backlog.md).
- **Scope FORBIDDEN and size limits:** At most 8 active implementation hours,
  1,000 added code/test lines and zero task-controlled external spend. No
  real host, credentials, customer/private/holdout data, provider calls,
  external evidence root, actual deletion, publication, or schema change
  without a separate versioned decision. This grant does not waive a future
  protected-file guard failure. Stop for a reviewed scope change before
  exceeding a bound.
- **Delivery:** One signed implementation PR, exact-path staging, synthetic
  positive/negative and legacy regression tests, full relevant offline
  suite, skill validation, independent architecture/security review, and
  exact-head Linux and Windows Actions. A future failed protected-file guard
  requires its own explicit owner disposition before merge.
- **Evidence:** Direct owner option-A reply in the Project Aegis conversation
  on 2026-09-23, quoted above, after the exact PR #131 proposal and limits
  were presented. [PR #131](https://github.com/ModernNomad-98/Project-Aegis/pull/131)
  merged at `e783f0f772700d30e203390b31e56c25187a1bc6`.
- **Expiry / use limit:** One bounded implementation package; no calendar
  expiry stated. No broader BER-BKL-009 work follows automatically.

### AEGIS-APR-013: Later condition on standing administrator merges

- **Event:** GRANT; later clarification of AEGIS-APR-002 for future routine use.
- **Status at recording:** ACTIVE.
- **Date / Grantor:** 2026-09-24 / Peter Nguyen.
- **Reason:** Preserve the owner's updated standing merge condition across
  sessions and computers.
- **Scope allowed:** The owner's exact instruction was: "I pre-approve all admin
  merges required as long as local tests and github actions are green". Apply
  this condition to future routine administrator merges for this source
  repository, within the separately authorized work being delivered.
- **Scope FORBIDDEN:** The instruction does not grant a routine administrator
  merge with a failing local test or GitHub Actions check. A separate,
  PR-specific owner exception may address a documented guard failure; this
  standing condition is not such an exception. It does not authorize unrelated
  work or change branch protection.
- **Evidence:** Direct owner message in the Project Aegis conversation on
  2026-09-24, quoted above, after the owner separately approved the guarded
  merges of PRs #139 and #197. The earlier recurring administrator-merge grant
  is AEGIS-APR-002; this later condition governs routine future use.
- **Expiry / use limit:** None stated; recurring conditional approval.

### AEGIS-APR-014: PR #139 protected-file guard exception

- **Event:** GRANT.
- **Status at recording:** Consumed by AEGIS-APR-015.
- **Date / Grantor:** 2026-09-24 / Peter Nguyen.
- **Reason:** Permit the reviewed offline BER evidence-policy proof through its
  documented protected-file guard failure.
- **Scope allowed:** The owner's exact answer was "Approve this PR and merge"
  to the question approving a one-time gate-guard exception and merge of
  [PR #139](https://github.com/ModernNomad-98/Project-Aegis/pull/139) at
  `515432d43c574ad778ba7f0ece1ca47ecf477cbf`. Linux and Windows checks
  passed; `gate-guard` was the sole failing check.
- **Scope FORBIDDEN:** PR #139 only at that reviewed head; no other failed
  check, PR, guard-policy change, or later BER phase is covered.
- **Evidence:** Direct owner reply to the exact-head question in the Project
  Aegis conversation on 2026-09-24, quoted above.
- **Expiry / use limit:** One PR #139 merge; no calendar expiry stated.

### AEGIS-APR-015: Consumption of PR #139 exception

- **Event:** CONSUMED; target grant AEGIS-APR-014.
- **Status at recording:** AEGIS-APR-014 has no remaining use.
- **Effective at:** 2026-09-24 15:57:16 UTC.
- **Recorded at / By:** 2026-09-24 / Project Aegis agent.
- **New authority:** None.
- **Reason:** The sole approved administrator merge completed.
- **Evidence:** [PR #139](https://github.com/ModernNomad-98/Project-Aegis/pull/139)
  merged as `b4b1195d6162728ffc37d22d038a08e3722db7c0`.

### AEGIS-APR-016: PR #197 protected-file guard exception

- **Event:** GRANT.
- **Status at recording:** Consumed by AEGIS-APR-017.
- **Date / Grantor:** 2026-09-24 / Peter Nguyen.
- **Reason:** Permit the reviewed BER runner README explanation through its
  documented protected-file guard failure.
- **Scope allowed:** The owner's exact answer was "Approve this PR and merge"
  to the separate one-time gate-guard question for
  [PR #197](https://github.com/ModernNomad-98/Project-Aegis/pull/197) at
  `4c176f68e101c64d3efb95c368f8d45c3b231ab6`. Linux and Windows passed;
  `gate-guard` was the sole failing check.
- **Scope FORBIDDEN:** PR #197 only at that reviewed head; no other failed
  check, PR, or change to the guard or branch protection is covered.
- **Evidence:** Direct owner reply to the exact-head question in the Project
  Aegis conversation on 2026-09-24, quoted above.
- **Expiry / use limit:** One PR #197 merge; no calendar expiry stated.

### AEGIS-APR-017: Consumption of PR #197 exception

- **Event:** CONSUMED; target grant AEGIS-APR-016.
- **Status at recording:** AEGIS-APR-016 has no remaining use.
- **Effective at:** 2026-09-24 15:58:43 UTC.
- **Recorded at / By:** 2026-09-24 / Project Aegis agent.
- **New authority:** None.
- **Reason:** The sole approved administrator merge completed.
- **Evidence:** [PR #197](https://github.com/ModernNomad-98/Project-Aegis/pull/197)
  merged as `ebaba9362e3eedba2f419a9072c6477f3ce23024`.

### AEGIS-APR-018: PR #239 protected-file guard exception

- **Event:** GRANT.
- **Status at recording:** Consumed by AEGIS-APR-019.
- **Date / Grantor:** 2026-09-24 / Peter Nguyen.
- **Reason:** Permit the independently reviewed fixture README and evidence
  note through their documented protected-file guard failure.
- **Scope allowed:** The owner's exact answer was "Approve this PR and merge"
  to the one-time gate-guard question for
  [PR #239](https://github.com/ModernNomad-98/Project-Aegis/pull/239) at
  `7999709e442535e03ca687bcc1b6e1cb5a9ad949`. Linux and Windows passed;
  `gate-guard` was the sole failing check.
- **Scope FORBIDDEN:** PR #239 only at that reviewed head; no other failed
  check, PR, or change to the guard or branch protection is covered.
- **Evidence:** Direct owner reply to the exact-head question in the Project
  Aegis conversation on 2026-09-24, quoted above.
- **Expiry / use limit:** One PR #239 merge; no calendar expiry stated.

### AEGIS-APR-019: Consumption of PR #239 exception

- **Event:** CONSUMED; target grant AEGIS-APR-018.
- **Status at recording:** AEGIS-APR-018 has no remaining use.
- **Effective at:** 2026-09-24 16:00:05 UTC.
- **Recorded at / By:** 2026-09-24 / Project Aegis agent.
- **New authority:** None.
- **Reason:** The sole approved administrator merge completed.
- **Evidence:** [PR #239](https://github.com/ModernNomad-98/Project-Aegis/pull/239)
  merged as `66ae4deb5f5600a4ab54f0a86bee858b8b9d7c76`.

### AEGIS-APR-020: PR #249 protected-file guard exception

- **Event:** GRANT.
- **Status at recording:** Consumed by AEGIS-APR-021.
- **Date / Grantor:** 2026-09-24 / Peter Nguyen.
- **Reason:** Permit the independently reviewed synthetic offline holdout-support
  implementation through its documented protected-file guard failure.
- **Scope allowed:** The owner's exact answer was "Approve this exact PR and
  merge" to the separate one-time gate-guard question for
  [PR #249](https://github.com/ModernNomad-98/Project-Aegis/pull/249) at
  `bf72d391831c9c6c30eedd295d07a2ff32b47fe4`. The local Windows suite
  passed 1,050 tests with 14 expected skips; Linux and Windows GitHub Actions
  passed. `gate-guard` was the sole failing check, and BER-DEC-012 required
  this separate owner disposition.
- **Scope FORBIDDEN:** PR #249 only at that reviewed head; no other failed
  check, PR, guard-policy change, branch-protection change, provider request,
  private holdout execution, or later BER phase is covered.
- **Evidence:** Direct owner reply to the exact-head question in the Project
  Aegis conversation on 2026-09-24, quoted above.
- **Expiry / use limit:** One PR #249 merge; no calendar expiry stated.

### AEGIS-APR-021: Consumption of PR #249 exception

- **Event:** CONSUMED; target grant AEGIS-APR-020.
- **Status at recording:** AEGIS-APR-020 has no remaining use.
- **Effective at:** 2026-09-24 17:36:47 UTC.
- **Recorded at / By:** 2026-09-24 / Project Aegis agent.
- **New authority:** None.
- **Reason:** The sole approved administrator merge completed.
- **Evidence:** [PR #249](https://github.com/ModernNomad-98/Project-Aegis/pull/249)
  merged as `fa37c0e545dfd096e8327ca5357b0dfc6e2f8bb5`.
