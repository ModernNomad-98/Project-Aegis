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

### AEGIS-APR-022: Consumption of offline evidence-policy proof grant

- **Event:** CONSUMED; target grant AEGIS-APR-012.
- **Status at recording:** AEGIS-APR-012 has no remaining use.
- **Effective at:** 2026-09-24 15:57:16 UTC.
- **Recorded at / By:** 2026-09-24 / Project Aegis agent.
- **New authority:** None.
- **Reason:** The one bounded synthetic implementation package authorized by
  AEGIS-APR-012 was delivered. This records its already exhausted use; it is
  separate from the PR #139 guard exception consumed by AEGIS-APR-015.
- **Evidence:** [PR #139](https://github.com/ModernNomad-98/Project-Aegis/pull/139)
  merged as `b4b1195d6162728ffc37d22d038a08e3722db7c0`.

### AEGIS-APR-023: Bounded synthetic evidence-policy integration

- **Event:** GRANT.
- **Status at recording:** Owner approved; ACTIVE only after the separate
  reviewed governance PR containing BER-DEC-013 and this entry merges.
- **Date / Grantor:** 2026-09-24 / Peter Nguyen.
- **Reason:** Make the selected 30-day complete-bundle policy usable by an
  explicitly opted-in local caller while preserving the shipped evidence bytes
  and refusing unknown host facts.
- **Scope allowed:** The owner's exact answer was "Approve this bounded scope"
  to the question approving the synthetic-only BER-BKL-009 follow-up in the
  merged [PR #253 proposal](../roadmaps/ber-bkl-009-policy-scope-amendment-proposal.md):
  exactly its ten named implementation paths, at most 16 active implementation
  hours, 1,500 added code/test lines, and $0 task-controlled external spend.
  It authorizes one opt-in, offline, synthetic implementation package, subject
  to that proposal's acceptance and delivery gates. Create the implementation
  branch directly from this governance PR's exact merge commit and record that
  commit and tree. A signed code PR needs focused and full offline BER tests,
  skill validation, independent architecture/security review, and exact-head
  Linux and Windows Actions. A simulated passing preflight must say
  `SIMULATION_ONLY`; unknown or contradictory host facts must stop. Preserve
  legacy evidence bytes and failed/incomplete bundles.
- **Scope FORBIDDEN:** No other path, real-host access or attestation, access
  control or encryption change, recovery-key handling, provider call, private
  input, credential, live run, production driver wiring, publication clearance,
  evidence deletion, dependency or unversioned schema/accepted-byte change is
  covered. A protected gate-guard failure still needs its own PR-specific owner
  disposition; this entry does not waive a failed check or close BER-BKL-009's
  later host, privacy, runtime and cleanup gates.
- **Evidence:** Direct owner reply on 2026-09-24 to the exact-scope question in
  the Project Aegis conversation, quoted above; the ten paths and behavior are
  in the merged [PR #253 proposal](../roadmaps/ber-bkl-009-policy-scope-amendment-proposal.md).
- **Expiry / use limit:** One bounded synthetic implementation package; no
  calendar expiry stated. Stop and return for a new scope if any cap or boundary
  would be exceeded.

### AEGIS-APR-024: Session-scoped commit, push and merge approval

- **Event:** GRANT.
- **Status at recording:** ACTIVE for the work in this Project Aegis conversation
  session, subject to the stated checks.
- **Date / Grantor:** 2026-09-24 / Peter Nguyen.
- **Reason:** Avoid repeated delivery approvals for already authorized work in
  this session.
- **Scope allowed:** The owner's exact instruction was: "I pre-approve all
  commit,push, merge from the work in this session as long as local tests and
  github action checks are green". It covers commits, pushes and merges for
  separately authorized Project Aegis source-library work in this session
  when applicable local tests and GitHub Actions checks are green. For a new
  head, local checks precede commit/push; exact-head Actions are checked after
  publication and before merge, because they cannot run on that head before
  push. Existing APR-013 administrator-merge terms remain in force.
- **Scope FORBIDDEN:** This delivery grant does not start or enlarge a work
  package, waive a failed local test or GitHub Actions check, waive a protected
  guard, alter branch protection, or authorize provider, host, private-data,
  deployment or release work. A separate applicable work grant is still needed.
- **Evidence:** Direct owner message in the Project Aegis conversation on
  2026-09-24, quoted above, during the ongoing backlog delivery loop.
- **Expiry / use limit:** Work in this conversation session only; no calendar
  expiry or one-use count stated. It is not a standing all-work grant for later
  sessions.

### AEGIS-APR-025: PR #257 protected gate-guard exception

- **Event:** GRANT.
- **Status at recording:** ACTIVE when granted; later consumed by AEGIS-APR-026.
- **Date / Grantor:** 2026-09-24 / Peter Nguyen.
- **Reason:** Permit the independently reviewed synthetic evidence-policy
  integration to merge after its protected runner paths triggered the guard.
- **Scope allowed:** The owner's exact reply was "approved" to the pending
  PR-specific decision for [PR #257](https://github.com/ModernNomad-98/Project-Aegis/pull/257)
  at head `7176009113fa208a1b2e816d90d7f929805e93ae`: a one-time
  `gate-guard` exception and administrator merge. Exact-head Linux and Windows
  checks passed; `gate-guard` failed because the PR changed protected runner
  paths. The local offline suite and independent reviews passed.
- **Scope FORBIDDEN:** This reply covered only that PR and head. It did not
  waive other checks, grant another protected-guard exception, or authorize
  host, provider, private-data, production or deletion work.
- **Evidence:** Direct owner reply "approved" on 2026-09-24 in the Project
  Aegis conversation following the PR #257 exception question and explanation
  of the guard; [PR #257 merge receipt](https://github.com/ModernNomad-98/Project-Aegis/pull/257).
- **Expiry / use limit:** One PR #257 merge; no calendar expiry stated.

### AEGIS-APR-026: Consumption of PR #257 exception

- **Event:** CONSUMED; target grant AEGIS-APR-025.
- **Status at recording:** AEGIS-APR-025 has no remaining use.
- **Effective at:** 2026-09-24 22:04:09 UTC.
- **Recorded at / By:** 2026-09-24 / Project Aegis agent.
- **New authority:** None.
- **Reason:** The sole approved administrator merge completed.
- **Evidence:** [PR #257](https://github.com/ModernNomad-98/Project-Aegis/pull/257)
  merged as `53351b3fac3d75cbbc23341cc96dbeadc1e116ee`.

### AEGIS-APR-027: Consumption of synthetic policy-integration grant

- **Event:** CONSUMED; target grant AEGIS-APR-023.
- **Status at recording:** AEGIS-APR-023 has no remaining use.
- **Effective at:** 2026-09-24 22:04:09 UTC.
- **Recorded at / By:** 2026-09-24 / Project Aegis agent.
- **New authority:** None.
- **Reason:** The one bounded synthetic implementation package authorized by
  AEGIS-APR-023 was delivered. Later real-host, privacy, runtime and cleanup
  gates remain outside that grant.
- **Evidence:** [PR #257](https://github.com/ModernNomad-98/Project-Aegis/pull/257)
  merged as `53351b3fac3d75cbbc23341cc96dbeadc1e116ee`;
  [integration review](../evidence/ber-bkl-009-policy-integration-review.md).

### AEGIS-APR-028: Agent-assisted disposable VirtualBox VM setup

- **Event:** GRANT.
- **Status at recording:** ACTIVE for one disposable VM setup; Ubuntu guest
  installation and final configuration remain to be verified.
- **Date / Grantor:** 2026-09-24 / Peter Nguyen.
- **Reason:** Prepare the owner-controlled Linux candidate for a later,
  separately authorized BER R4/R5 Stage A capability proof.
- **Scope allowed:** The owner's exact reply was "Approve agent-assisted VM
  setup" to a question authorizing verified VirtualBox and Ubuntu downloads,
  installation with owner participation for Windows elevation and an Ubuntu
  password, and one disposable VM with four virtual CPUs, 8 GiB memory and a
  dynamically allocated 60 GiB disk. The [reviewed setup proposal](../roadmaps/ber-virtualbox-stage-a-setup-proposal.md)
  supplies the chosen VirtualBox/Linux platform, temporary setup networking
  and no-sharing boundaries. The VM uses the existing VirtualBox default
  machine folder, whose personal path is kept outside this public register.
  The owner keeps passwords
  private. Exact installed software and VM configuration must be verified.
- **Scope FORBIDDEN:** This grant does not authorize BER Stage A or Stage B
  tests, source transfer into the guest, provider/model calls, private inputs,
  credentials in chat or source, paid services, production use, changes to
  Windows security or hypervisor features, or VM/evidence deletion. A separate
  BER-DEC grant is required before even the offline Stage A host probe.
- **Evidence:** Direct owner reply on 2026-09-24 to the agent-assisted VM setup
  question in the Project Aegis conversation. VirtualBox 7.2.20 was already
  installed when setup resumed; its existing installer matched Oracle's
  published SHA-256 and the installed executable had a valid Oracle signature.
  The Ubuntu 24.04.5.1 ISO matched Ubuntu's published SHA-256. These supply
  chain checks do not substitute for verifying the installed guest.
- **Expiry / use limit:** One named disposable VM setup in this session; no
  calendar expiry stated. Stop for review if the host, identity, isolation or
  software configuration differs materially from the approved setup.

### AEGIS-APR-029: PR #274 protected gate-guard exception

- **Event:** GRANT.
- **Status at recording:** ACTIVE when granted; later consumed by AEGIS-APR-030.
- **Date / Grantor:** 2026-09-25 UTC / Peter Nguyen.
- **Reason:** Permit the reviewed BER receipt-prevalidation fix to merge after
  its protected BER paths triggered the guard.
- **Scope allowed:** The owner's exact answer was "Approve exact-head exception
  and merge (Recommended)" to the question approving a one-time `gate-guard`
  exception and administrator merge of
  [PR #274](https://github.com/ModernNomad-98/Project-Aegis/pull/274) at
  `7768ed543eea321102ad7f6d3e4b2aebaa862380`. The question reported
  1,070 local tests passed and 14 skipped; exact-head Linux and Windows checks
  passed, while only `gate-guard` failed because of protected BER paths.
- **Scope FORBIDDEN:** No other PR, head or failed check was covered. This
  grant did not change the guard or branch protection, or authorize another
  BER work package.
- **Evidence:** Direct owner answer quoted above in the Project Aegis
  conversation on 2026-09-25 UTC; the [PR #274 merge receipt](https://github.com/ModernNomad-98/Project-Aegis/pull/274)
  confirms the exact head and check results.
- **Expiry / use limit:** One merge of PR #274 at the named head; consumed at
  the merge recorded in AEGIS-APR-030.

### AEGIS-APR-030: Consumption of PR #274 exception

- **Event:** CONSUMED; target grant AEGIS-APR-029.
- **Status at recording:** AEGIS-APR-029 has no remaining use.
- **Effective at:** 2026-09-25 04:18:23 UTC.
- **Recorded at / By:** 2026-09-25 / Project Aegis agent.
- **New authority:** None.
- **Reason:** The sole exact-head administrator merge completed.
- **Evidence:** [PR #274](https://github.com/ModernNomad-98/Project-Aegis/pull/274)
  merged head `7768ed543eea321102ad7f6d3e4b2aebaa862380` as
  `97e61c590091a3388dc504d72d61ea283772c2fa` at the time above.

### AEGIS-APR-031: Issue #101 Stage 4A offline bridge implementation

- **Event:** GRANT.
- **Status at recording:** ACTIVE for one bounded offline implementation.
- **Date / Grantor:** 2026-09-25 UTC / Peter Nguyen.
- **Reason:** Prove synthetic callback routing and denial behavior before any
  real SDK session or provider use.
- **Scope allowed:** The owner's exact answer was "Approve bounded offline
  implementation (Recommended)" to the Stage 4A question covering the
  [reviewed proposal](../roadmaps/aegis-setup-package-4a-host-preparation-proposal.md)
  merged in [PR #271](https://github.com/ModernNomad-98/Project-Aegis/pull/271).
  This authorizes the proposal's exact 11 paths and synthetic offline
  callback/bridge tests, at most 12 active implementation hours, 1,200 added
  handwritten code/test lines and $0 task-controlled external spend. The
  preferred pinned dependency resolution contains 107 packages; the SDK uses
  Anthropic commercial terms. A scripts-disabled install may occur only after
  review of the exact committed lock and package bodies passes. The grant covers the
  proposal's fail-closed test matrix and pinned offline CI steps.
- **Exact implementation files:** `tools/aegis_setup/host_bridge/.gitignore`,
  `tools/aegis_setup/host_bridge/package.json`,
  `tools/aegis_setup/host_bridge/package-lock.json`,
  `tools/aegis_setup/host_bridge/tsconfig.json`,
  `tools/aegis_setup/host_bridge/bridge.ts`,
  `tools/aegis_setup/host_bridge/contract_worker.py`,
  `tools/aegis_setup/host_bridge/bridge.test.ts`,
  `tools/aegis_setup/host_bridge/README.md`,
  `docs/roadmaps/aegis-setup-routing-plan.md`,
  `docs/evidence/setup/issue-101-package-4a-offline-review.md`, and
  `.github/workflows/validate-skills.yml`.
- **Scope FORBIDDEN:** No SDK `query()`, Claude CLI process, provider/model
  call, credentials, private data, VM work or deployment. Synthetic tests
  cannot claim real Claude interception or token savings. This grant does not
  waive a later protected CI guard failure; that requires a separate decision.
  Stop for a reviewed scope change before exceeding any cap or path boundary.
- **Evidence:** Direct owner answer quoted above in the Project Aegis
  conversation on 2026-09-25 UTC to the exact-scope question. That question
  also disclosed local downloads, disk space, future maintenance and Anthropic
  commercial terms, and required exact lock and package-body safety review
  before scripts-disabled installation. The 11-path proposal was merged in
  PR #271 before the grant.
- **Expiry / use limit:** One bounded Stage 4A offline implementation; no
  calendar expiry stated. Stage 4B requires separate authority.

### AEGIS-APR-032: PR #281 original-head gate-guard exception

- **Event:** GRANT.
- **Status at recording:** ACTIVE for the named head only; later expired without
  use as recorded in AEGIS-APR-033.
- **Date / Grantor:** 2026-09-25 UTC / Peter Nguyen.
- **Reason:** Permit the reviewed Stage 4A offline bridge PR to pass its
  protected-path `gate-guard` failure at the then-current exact head.
- **Scope allowed:** The owner's exact reply was "allow" to the PR #281
  exact-head exception request for
  `0bb51c19bd42261a5604fb25762069ce7867141b`. Its scope was the
  one-time protected `gate-guard` exception and administrator merge of that
  head of [PR #281](https://github.com/ModernNomad-98/Project-Aegis/pull/281).
- **Scope FORBIDDEN:** No other PR or head was covered; no host session,
  provider call, credential use, VM work or Stage 4B execution was granted.
- **Evidence:** Direct owner reply quoted above in the Project Aegis
  conversation on 2026-09-25 UTC to the original exact-head request.
- **Expiry / use limit:** One merge at the named head; the head changed before
  merge, so this exception had no remaining applicable use.

### AEGIS-APR-033: Original PR #281 exception expired unused

- **Event:** EXPIRED; target grant AEGIS-APR-032.
- **Status at recording:** AEGIS-APR-032 has no remaining applicable use and
  was never consumed by a merge.
- **Effective at:** 2026-09-25 07:26:36 UTC, when the replacement head
  `fd2e27e48fcfe85a5361345ebe70bb424e422abf` was committed after a
  merge conflict made the original head unusable.
- **Recorded at / By:** 2026-09-25 / Project Aegis agent.
- **New authority:** None.
- **Reason:** The exact-head condition of AEGIS-APR-032 could no longer be
  satisfied; the original head was not merged.
- **Evidence:** [PR #281](https://github.com/ModernNomad-98/Project-Aegis/pull/281)
  and replacement commit `fd2e27e48fcfe85a5361345ebe70bb424e422abf`.

### AEGIS-APR-034: PR #281 replacement-head gate-guard exception

- **Event:** GRANT.
- **Status at recording:** ACTIVE when granted; later consumed by
  AEGIS-APR-035.
- **Date / Grantor:** 2026-09-25 UTC / Peter Nguyen.
- **Reason:** Authorize the protected-path exception for the reviewed
  replacement head after the conflict resolution.
- **Scope allowed:** The owner's exact reply was "parooved" to the immediately
  preceding decision message naming [PR #281](https://github.com/ModernNomad-98/Project-Aegis/pull/281)
  at `fd2e27e48fcfe85a5361345ebe70bb424e422abf`. It authorized the
  one-time `gate-guard` exception and administrator merge of that head. The
  exact-head Linux and Windows checks were green; the protected-path
  `gate-guard` check failed.
- **Scope FORBIDDEN:** No other PR, head or failed check was covered; no SDK
  session, provider/model call, credentials, VM work or Stage 4B execution.
- **Evidence:** Direct owner reply quoted above in the Project Aegis
  conversation on 2026-09-25 UTC to the replacement exact-head decision message;
  the [PR #281 merge receipt](https://github.com/ModernNomad-98/Project-Aegis/pull/281)
  identifies the merged head and merge commit.
- **Expiry / use limit:** One merge of PR #281 at the named replacement head.

### AEGIS-APR-035: Consumption of PR #281 replacement-head exception

- **Event:** CONSUMED; target grant AEGIS-APR-034.
- **Status at recording:** AEGIS-APR-034 has no remaining use.
- **Effective at:** 2026-09-25 07:43:44 UTC.
- **Recorded at / By:** 2026-09-25 / Project Aegis agent.
- **New authority:** None.
- **Reason:** The one-time exact-head administrator merge completed.
- **Evidence:** [PR #281](https://github.com/ModernNomad-98/Project-Aegis/pull/281)
  merged `fd2e27e48fcfe85a5361345ebe70bb424e422abf` as
  `ea40ab481ff78267cd5f151c393e946805ba8d01` at the time above.

### AEGIS-APR-036: Stage 4A offline bridge package completed

- **Event:** CONSUMED; target grant AEGIS-APR-031.
- **Status at recording:** AEGIS-APR-031's one bounded Stage 4A offline
  implementation is complete and has no remaining use.
- **Effective at:** 2026-09-25 07:43:44 UTC.
- **Recorded at / By:** 2026-09-25 / Project Aegis agent.
- **New authority:** None.
- **Reason:** PR #281 merged the authorized synthetic offline bridge package.
- **Evidence:** [PR #281](https://github.com/ModernNomad-98/Project-Aegis/pull/281)
  merged as `ea40ab481ff78267cd5f151c393e946805ba8d01` at the time above.
  This closes one Stage 4A implementation; it is not Stage 4B host proof.

### AEGIS-APR-037: PR #304 protected gate-guard exception

- **Event:** GRANT.
- **Status at recording:** Consumed by AEGIS-APR-038; no remaining use.
- **Date / Grantor:** 2026-09-25 UTC / Peter Nguyen.
- **Reason:** Permit the independently reviewed synthetic BER Stage A expiry
  repair to merge after its protected BER paths triggered the guard.
- **Scope allowed:** The owner's exact reply was "approved" to the one-time
  `gate-guard` exception request for
  [PR #304](https://github.com/ModernNomad-98/Project-Aegis/pull/304) at
  `df7e5b2bb5b6b3211fada10ead0f8c723874d6d5`. The request reported
  1,074 local offline BER tests with 14 expected skips, independent review,
  passing exact-head Linux and Windows Actions, and a `gate-guard` failure
  solely because protected BER source paths changed. The grant covered one
  administrator merge of that exact head through that guard result.
- **Scope FORBIDDEN:** No other PR, head or failed check was covered. This
  did not alter branch protection or authorize a real host, provider call,
  private input, production driver, publication or evidence deletion.
- **Evidence:** Direct owner reply quoted above in the Project Aegis
  conversation; the [PR #304 merge receipt](https://github.com/ModernNomad-98/Project-Aegis/pull/304)
  confirms the exact head and check results.
- **Expiry / use limit:** One merge of PR #304 at the named head; consumed
  by the merge recorded in AEGIS-APR-038.

### AEGIS-APR-038: Consumption of PR #304 exception

- **Event:** CONSUMED; target grant AEGIS-APR-037.
- **Status at recording:** AEGIS-APR-037 has no remaining use.
- **Effective at:** 2026-09-25 23:30:28 UTC.
- **Recorded at / By:** 2026-09-25 / Project Aegis agent.
- **New authority:** None.
- **Reason:** The sole exact-head administrator merge completed.
- **Evidence:** [PR #304](https://github.com/ModernNomad-98/Project-Aegis/pull/304)
  merged `df7e5b2bb5b6b3211fada10ead0f8c723874d6d5` as
  `e6f13e3376e2b5d7ad85ab6ca097dedde96f5fe2` at the time above.

### AEGIS-APR-039: Reaffirmation of ongoing backlog delivery approval

- **Event:** GRANT; reaffirmation of AEGIS-APR-013 and AEGIS-APR-024.
- **Status at recording:** ACTIVE for the ongoing Project Aegis backlog task.
- **Date / Grantor:** 2026-09-25 / Peter Nguyen.
- **Reason:** Preserve the owner's standing delivery and persistence direction
  for the ongoing backlog task without repeated permission requests.
- **Owner instruction:** "you should be using multi-agent per our rule. Loop
  through all backlogs and issues until all are resolved. Pre-approve for all
  commit, push, and merge including admin merges. Do not stop until everything
  is completed"
- **Scope allowed:** Continue authorized Project Aegis backlog work with
  parallel agents and deliver its commits, branch pushes, pull requests and
  merges, including administrator merges, without repeated delivery approval.
  Apply the existing local-test and GitHub Actions conditions; verify a
  published candidate's exact-head checks before merging.
- **Scope FORBIDDEN:** This delivery grant does not waive a failed protected
  `gate-guard`, renew a consumed one-use implementation grant, resume the
  paused virtual machine, or authorize provider calls, private input,
  real-host proof, deployment or evidence deletion.
- **Interpretation:** The latest instruction reaffirms delivery authority and
  persistence; it does not expressly retract the green-check conditions in
  AEGIS-APR-013/024. Continue other authorized backlog work while a separate
  decision is pending.
- **Evidence:** Direct owner message quoted above in the ongoing Project
  Aegis conversation; prior standing delivery conditions are in
  AEGIS-APR-013 and AEGIS-APR-024.
- **Expiry / use limit:** Ongoing backlog task; no one-use limit stated.

### AEGIS-APR-040: Issue #101 offline routing request binding revision

- **Event:** GRANT.
- **Status at recording:** ACTIVE for one bounded synthetic offline implementation.
- **Date / Grantor:** 2026-09-26 UTC / Peter Nguyen.
- **Reason:** Bind each offline routing advice response to its own callback so a
  response from an earlier synthetic call cannot authorize a later one.
- **Scope allowed:** The owner's exact reply was "approve all" to the two
  pending decisions, including the bounded routing version 2 implementation
  in the [reviewed proposal](../roadmaps/aegis-setup-routing-request-binding-proposal.md)
  merged in [PR #310](https://github.com/ModernNomad-98/Project-Aegis/pull/310).
  Use a fresh unpredictable 128-bit request ID for each callback; require a
  matching 32-character lowercase hexadecimal ID in version 2 requests and
  responses, including abstentions; reject version 1 without fallback. The
  exact eight implementation paths are `tools/aegis_setup/routing_contract.py`,
  `tools/aegis_setup/tests/test_routing_contract.py`,
  `tools/aegis_setup/README.md`,
  `tools/aegis_setup/host_bridge/bridge.ts`,
  `tools/aegis_setup/host_bridge/bridge.test.ts`,
  `tools/aegis_setup/host_bridge/README.md`,
  `docs/roadmaps/aegis-setup-routing-plan.md`, and the new
  `docs/evidence/setup/issue-101-routing-request-binding-review.md`. Limit
  work to 12 active implementation hours, 500 added handwritten code/test
  lines and $0 task-controlled external spend. Use invented offline fixtures,
  focused Python and Node tests, skill validation, independent contract and
  authority review, and exact-head GitHub Actions before the signed PR merges.
- **Scope FORBIDDEN:** No SDK `query()`, Claude process, provider call,
  credential, private data, VM work, dependency change, deployment or real
  callback invocation. This grant does not authorize Stage 4B host proof or
  waive a future protected `gate-guard` failure. Stop before exceeding a path
  or resource bound.
- **Evidence:** Direct owner reply "approve all" in the Project Aegis
  conversation on 2026-09-26 UTC to the immediately preceding two-decision
  summary, whose first decision named the bounded routing version 2 scope in
  PR #310. The owner's following message reiterated approval of backlog
  delivery under local-test and GitHub Actions conditions.
- **Expiry / use limit:** One bounded offline routing version 2 implementation;
  no calendar expiry stated.

### AEGIS-APR-041: PR #313 protected gate-guard exception

- **Event:** GRANT.
- **Status at recording:** Consumed by AEGIS-APR-042; no remaining use.
- **Date / Grantor:** 2026-09-26 UTC / Peter Nguyen.
- **Reason:** Permit the independently reviewed BER reporting-integrity repair
  to merge when its protected source paths triggered the guard.
- **Scope allowed:** The owner's exact reply was "approve all" to the two
  pending decisions, whose second decision named the one-time `gate-guard`
  exception and administrator merge of
  [PR #313](https://github.com/ModernNomad-98/Project-Aegis/pull/313) at exact
  head `8535727539a3c2afc67583d2fa10476edc0ea04b`. The request reported
  1,078 passing local BER tests with 14 expected skips, independent review,
  passing exact-head Linux and Windows Actions, and a `gate-guard` failure
  solely for four protected BER paths. This grant covered one administrator
  merge of that head through that specific guard result.
- **Scope FORBIDDEN:** No other PR, head or failed check was covered. This did
  not change branch protection or authorize real-host access, provider calls,
  private input, production wiring, publication or evidence deletion.
- **Evidence:** Direct owner reply "approve all" in the Project Aegis
  conversation on 2026-09-26 UTC to the immediately preceding two-decision
  summary. The [PR #313 merge receipt](https://github.com/ModernNomad-98/Project-Aegis/pull/313)
  confirms the exact head, passing Linux and Windows checks, failing
  `gate-guard`, and completed merge.
- **Expiry / use limit:** One merge of PR #313 at the named head; consumed by
  the merge recorded in AEGIS-APR-042.

### AEGIS-APR-042: Consumption of PR #313 exception

- **Event:** CONSUMED; target grant AEGIS-APR-041.
- **Status at recording:** AEGIS-APR-041 has no remaining use.
- **Effective at:** 2026-09-26 01:58:24 UTC.
- **Recorded at / By:** 2026-09-26 / Project Aegis agent.
- **New authority:** None.
- **Reason:** The sole exact-head administrator merge completed.
- **Evidence:** [PR #313](https://github.com/ModernNomad-98/Project-Aegis/pull/313)
  merged `8535727539a3c2afc67583d2fa10476edc0ea04b` as
  `9b85140d03f69ce563dc39c51cd2bf71f3094773` at the time above.
