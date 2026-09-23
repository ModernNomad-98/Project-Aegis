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
- **Purpose and scope:** Build only the synthetic, offline capability proof and
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
- **Limits:** At most 10 active implementation hours and 2,000 added code/test
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

### AEGIS-APR-007: Issue #101 conversational setup, Aegis-only completion

- **Event:** GRANT, effective only after this reviewed register change merges.
- **Status at recording:** ACTIVE on that merge.
- **Date / Grantor:** 2026-09-23 / Peter Nguyen.
- **Owner decision:** The same direct approval quoted in AEGIS-APR-006 answered
  the recommendation to approve the bounded package-2 proposal in
  [PR #113](https://github.com/ModernNomad-98/Project-Aegis/pull/113).
- **Purpose and scope:** Implement the four-choice, manually invoked setup
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
- **Limits:** At most 12 active implementation hours and 1,200 added lines
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

### AEGIS-APR-008: Issue #101 offline advisory routing contract

- **Event:** GRANT, effective only after this reviewed register change merges.
- **Status at recording:** ACTIVE on that merge.
- **Date / Grantor:** 2026-09-23 / Peter Nguyen.
- **Owner decision:** The same direct approval quoted in AEGIS-APR-006 answered
  the recommendation to approve the bounded package-3 proposal in
  [PR #115](https://github.com/ModernNomad-98/Project-Aegis/pull/115).
- **Purpose and scope:** Build the provider-neutral, advisory-only offline
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
- **Limits:** At most 12 active implementation hours and 1,200 added code/test
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

### AEGIS-APR-009: Behavioral Eval Runner evidence-policy selection

- **Event:** POLICY DECISION. This selects a policy target; it does not grant
  implementation, deletion or a live run.
- **Status at recording:** ACTIVE on this reviewed register merge.
- **Date / Grantor:** 2026-09-23 / Peter Nguyen.
- **Owner decision:** The same direct approval quoted in AEGIS-APR-006 answered
  the recommendation to use the [30-day complete-bundle evidence policy](../roadmaps/ber-bkl-009-evidence-policy-decision.md)
  proposed in [PR #108](https://github.com/ModernNomad-98/Project-Aegis/pull/108).
- **Selected policy:** One 30-calendar-day clock from first evidence creation
  for the complete Stage A and Stage B runtime verification bundle, including
  the detached marker. Expiration makes cleanup eligible for owner review;
  failures and incomplete runs remain preserved until resolved and reviewed.
  The owner and required runner/verifier components are the intended readers;
  the current Windows work package 2B-3 root requires owner plus operating-system
  SYSTEM access and host-verified BitLocker encryption before use. A different
  selected host requires its own verified mechanism and access decision.
  Private versioned calibration inputs remain in the separate owner-only
  repository until an owner-reviewed deletion; public Git holds only reviewed
  sanitized records.
- **Boundary:** The proposal's reader matrix, redaction, publication and
  marker-gated cleanup controls are the policy target. Current metadata and
  operating-system enforcement are incomplete. Behavioral Eval Runner backlog
  item 009 remains partially delivered. A separately reviewed decision-log
  amendment must define exact code/runbook scope before implementation. This
  decision grants no automatic deletion, additional reader, provider call,
  holdout access, or measured result.
- **Evidence:** Direct owner instruction quoted in AEGIS-APR-006, following the
  PR #108 evidence-policy recommendation and decision options.
