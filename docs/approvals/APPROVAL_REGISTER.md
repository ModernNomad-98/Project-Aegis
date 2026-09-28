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

## How to read this register

Read this page before asking the owner for an approval, or when you need to
cite the authority for an action. It is written for maintainers and coding
agents working on this repository. The terms below are reading aids only;
they do not change any entry's scope. Where an entry and this list differ,
the entry governs.

- **AEGIS-APR-nnn** is an entry ID; some entries shorten it to **APR-nnn**.
  Event types are GRANT, POLICY DECISION (selects a policy target, grants no
  work), CONSUMED (a limited grant was used up) and EXPIRED (a grant's time,
  session or other limit ended, whether or not it was used). Some GRANT
  entries clarify, condition or reaffirm an earlier grant and name it on
  their Event line. "Status at recording" is the status when
  the entry was written; later events can change it. A one-use grant can be
  used up even before a later event records that; check its use limit and
  linked delivery record.
- **PR** is a GitHub pull request; **issue #nnn** is a GitHub issue. The
  **head** or **exact head** is the specific latest commit of a pull request
  that was checked and approved; a 40-character hexadecimal value is a Git
  object ID (SHA), a commit unless the entry calls it a tree, often shortened
  to 7 characters.
- **CI** (continuous integration) is the GitHub Actions jobs in
  `.github/workflows/validate-skills.yml`: `validate-skills` (the Linux run),
  `windows-offline-checks` (the Windows run) and `gate-guard`. On pull
  requests, `validate-skills` and `gate-guard` are the required checks;
  `gate-guard` runs on pull requests only. The **DCO** (Developer
  Certificate of Origin) sign-off check is a pull-request step inside
  `validate-skills` that requires every commit to be signed off.
- **gate-guard**, also called the **protected-file guard**, fails whenever a
  pull request changes a protected path: the merge gate or a surface that
  enforces it, such as workflow files, `CODEOWNERS`, the validator, the DCO
  script, CI scripts and tests, or `tools/behavioral_eval_runner/`. A
  **gate-guard exception** is an owner decision to merge despite that
  failure: usually one-time for one exact head, except the standing
  four-file exception in AEGIS-APR-047. An **administrator merge** uses repository
  administrator rights to merge past branch-protection requirements.
- **Codex** is an automated pull-request reviewer; **P1** and **P2** are its
  two highest finding priority levels. In AEGIS-APR-073, **P0**, **P1**,
  **P2** and **info** are instead the skill-contract audit report's four
  finding severity levels, P0 the most severe. **SHIP** is an independent
  reviewer's verdict that a head is ready to merge.
- **Claude Code** is Anthropic's command-line coding agent. A **headless**
  Claude Code session runs without a person typing into it.
- **BER** is the Behavioral Eval Runner under `tools/behavioral_eval_runner/`,
  planned in [the BER backlog](../roadmaps/behavioral-eval-runner-backlog.md).
  There, **BER-BKL-nnn** is a BER backlog item, **BER-DEC-nnn** an entry in
  the append-only BER decision log, **WP-…** or "work package …" a BER work
  package (except "control-plane work package 003A" in AEGIS-APR-006, which
  is CP-WP-003A below), **OD-1** owner decision 1, and **R4** and **R5** two
  of the five
  capability-evidence gates R1–R5 (R4 is operating-system/host isolation and
  per-tool-path confinement; R5 is execution-profile observability and
  isolation).
- **Stage A / Stage B** has two BER senses; read the entry's context. For the
  evidence bundle (APR-009, APR-037), Stage A binds the pre-judge input
  evidence and Stage B binds the final report, as defined in
  [the evidence-policy decision](../roadmaps/ber-bkl-009-evidence-policy-decision.md).
  For **R4/R5** host proof (APR-028), Stage A is the offline, non-model host
  capability probe and Stage B the later bounded tool-path proof, as defined
  in [the selected-host capability decision](../roadmaps/ber-selected-host-capability-decision.md).
- **CP-WP-nnn** is a control-plane work package in
  [the resumable control-plane backlog](../roadmaps/resumable-control-plane-backlog.md);
  a letter suffix, as in CP-WP-003A, names one increment of that package.
  The backlog marks packages DONE (delivered, with the required evidence and
  owner disposition recorded) or BLOCKED (entry conditions or authority
  absent). Its numbered test cases are **T** (a state transition, T01–T28), **C** (a
  crash boundary, C01–C09) and **F** (a finding-specific negative acceptance
  family, F01–F21, where F04 is split into separate F04a and F04b rows, so
  there are 22 F rows), each defined in
  [the control-plane design](../design/resumable-control-plane-v1.md).
- **Package 2, package 3, Stage 4A and Stage 4B** are successive parts of the
  issue #101 setup and routing plan in
  [the routing plan](../roadmaps/aegis-setup-routing-plan.md). Stage 4A is
  the offline bridge; Stage 4B is the real host proof and is not granted by
  any Stage 4A entry.
- **ROUTE-002** is a skill-contract audit rule that reports one skill
  excluding another when the other skill does not return the exclusion. The
  audit **engine** (for example v1.13.2) is
  `scripts/audit-skill-contracts.py`. The **AEGIS-060+ register** is
  [the contract-audit findings register](../audits/aegis-060-plus-register.md).
  **D61** is a numbered decision in
  [the planning record](../reconciliation/step-0-reconciliation-v4.md).
- Other abbreviations: **ID** identifier, **OS** operating system, **VM**
  virtual machine, **CPU** central processing unit (processor), **SDK**
  software development kit, **CLI** command-line
  interface, **UTC** Coordinated Universal Time, **PDT** Pacific Daylight
  Time, **GiB** gibibyte, **ISO** a disc-image file, **SHA-256** a file
  checksum, **JSON** JavaScript Object Notation, **eval** evaluation (a
  skill's test cases in its `evals/*.json` files).

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

### AEGIS-APR-043: Consumption of issue #101 offline routing grant

- **Event:** CONSUMED; target grant AEGIS-APR-040.
- **Status at recording:** AEGIS-APR-040 has no remaining use.
- **Effective at:** 2026-09-26 02:24:21 UTC.
- **Recorded at / By:** 2026-09-26 / Project Aegis agent.
- **New authority:** None.
- **Reason:** The one bounded synthetic offline version-2 request-binding
  implementation merged after its exact-head checks passed.
- **Evidence:** [PR #319](https://github.com/ModernNomad-98/Project-Aegis/pull/319)
  merged exact head `550151dcf286f8ec64480bc91f47e390454417d2` as
  `a59c015c01b4035ab1a438533736134f96deac13` at the time above.
  [Exact-head Actions](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/36211342637)
  passed `validate-skills`, `windows-offline-checks` and `gate-guard`.

### AEGIS-APR-044: PR #315 protected gate-guard exception

- **Event:** GRANT.
- **Status at recording:** Consumed by AEGIS-APR-045; no remaining use.
- **Date / Grantor:** 2026-09-26 UTC / Peter Nguyen.
- **Reason:** Permit the offline BER aggregate-integrity repair to merge when its
  two protected reporting paths triggered the guard.
- **Scope allowed:** The owner's reply was "Approved" following the specific
  request for a one-time `gate-guard` exception and administrator merge of
  [PR #315](https://github.com/ModernNomad-98/Project-Aegis/pull/315) at exact
  head `5b78c77535ac76c99c10becb2d437b24867f69f9`. The request reported
  1,080 passing local BER tests with 14 expected skips, passing exact-head
  Linux and Windows Actions in
  [run 36219047092](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/36219047092),
  and a `gate-guard` failure solely for
  `tools/behavioral_eval_runner/reporting.py` and
  `tools/behavioral_eval_runner/tests/test_reporting.py`. The grant covered
  one administrator merge of that head through that specific guard result.
- **Scope FORBIDDEN:** No other PR, head or failed check was covered. This did
  not change branch protection or authorize a real host, provider call,
  private input, measured calibration, publication or evidence deletion.
- **Evidence:** Direct owner reply "Approved" in the Project Aegis
  conversation, following the owner's question about the recurring
  `gate-guard` check. It answered the exact-head exception request above;
  the [PR #315 merge receipt](https://github.com/ModernNomad-98/Project-Aegis/pull/315)
  confirms the head, checks and merge. The question about the recurring guard
  did not expand this one-time exception.
- **Expiry / use limit:** One merge of PR #315 at the named head; consumed by
  the merge recorded in AEGIS-APR-045.

### AEGIS-APR-045: Consumption of PR #315 exception

- **Event:** CONSUMED; target grant AEGIS-APR-044.
- **Status at recording:** AEGIS-APR-044 has no remaining use.
- **Effective at:** 2026-09-26 05:31:33 UTC.
- **Recorded at / By:** 2026-09-26 / Project Aegis agent.
- **New authority:** None.
- **Reason:** The sole exact-head administrator merge completed.
- **Evidence:** [PR #315](https://github.com/ModernNomad-98/Project-Aegis/pull/315)
  merged `5b78c77535ac76c99c10becb2d437b24867f69f9` as
  `658fa22edbfde2c953f7d21678d08baa79b75052` at the time above.

### AEGIS-APR-046: BER selected-precheck aggregate correction

- **Event:** GRANT.
- **Status at recording:** Owner approved; ACTIVE only after the separate
  reviewed governance PR containing BER-DEC-014 and this entry merges.
- **Date / Grantor:** 2026-09-26 / Peter Nguyen.
- **Reason:** Make a Behavioral Eval Runner (BER) report reject a selected case
  that its pre-run check (preflight) excluded (`PRECHECK_EXCLUDED`) unless its
  planned attempts stay unexecuted (`UNRUN`) and its case-level result
  (aggregate) records the same exclusion, so an excluded case cannot appear
  unselected (`NOT_SELECTED`) or vanish from the excluded-case count.
- **Owner decision:** "Approve fix + #333 opt A (Recommended)", answering a
  question that described both options. The selected option read: "Approve
  the bounded fix using the brief's scoped wording, and also approve #333
  option A, a standing gate-guard allowlist that already covers these two
  files." The #333 part, which the owner later confirmed as option A as
  defined, is recorded separately in AEGIS-APR-047.
- **Scope allowed:** The approved scoped wording was: "I approve the bounded
  synthetic BER precheck-aggregate correction in merged PR #331's proposal
  (docs/roadmaps/ber-precheck-aggregate-validation-proposal.md), and only
  that. Scope: exactly two paths: tools/behavioral_eval_runner/reporting.py
  and tools/behavioral_eval_runner/tests/test_reporting.py. Limits: at most 8
  active implementation hours and 300 added code/test lines; $0
  task-controlled external spend; synthetic local fixtures only; no provider,
  model or metadata calls, private labels, credentials, host probes,
  dependency installs or live sessions. Order: this takes effect only after a
  separate reviewed governance PR merges that appends BER-DEC-014 to the BER
  decision log and APR-046 to the approval register; that governance PR also
  updates the backlog lifecycle entry and records the repository, branch and
  base, exact paths, acceptance tests, budget, evidence and stop conditions.
  Delivery: one implementation branch created from that governance PR's exact
  merge commit, with its commit and tree recorded; one DCO-signed
  implementation PR with exact-path staging, the focused and full offline BER
  test suites on Windows and pinned Linux, independent security and quality
  review, and exact-head checks. Use limit: one implementation package;
  consumed at its merge." (DCO is the Developer Certificate of Origin commit
  sign-off check.) The [merged proposal](../roadmaps/ber-precheck-aggregate-validation-proposal.md)
  defines the permitted change at each path. Branch, acceptance tests and
  evidence handling are recorded in BER-DEC-014 in
  [the BER governance log](../roadmaps/behavioral-eval-runner-backlog.md#ber-dec-014-bounded-synthetic-selected-precheck-aggregate-correction--owner-approved).
- **Scope FORBIDDEN:** From the approved wording: "Stop conditions: stop and
  come back to the owner before exceeding any limit, touching another path,
  changing the approved report contract, or if review finds a legitimate
  consumer that depends on the empty selected-case shape. What this does not
  cover: it does not change private-label, selected-host, provider-budget,
  OD-1 or later live-suite gates." OD-1 is owner decision 1, the later
  ratification of a measured judge-calibration result. This grant does not
  itself waive a failed check; a `gate-guard` result on the implementation PR
  is governed by AEGIS-APR-047's conditions.
- **Evidence:** Direct owner answer in the Project Aegis conversation on
  2026-09-26, quoted above, relayed by the coordinating agent with the exact
  scoped wording. The proposal merged in
  [PR #331](https://github.com/ModernNomad-98/Project-Aegis/pull/331) as
  `1bf35dc88d76a6177b67ecc18fbffcb6f8f849fb`.
- **Expiry / use limit:** One implementation package; consumed at its merge.
  No calendar expiry stated.

### AEGIS-APR-047: Standing gate-guard exception for four BER files

- **Event:** GRANT; narrow later condition on AEGIS-APR-013, AEGIS-APR-024 and
  AEGIS-APR-039 for one signal only.
- **Status at recording:** ACTIVE from the owner's 2026-09-26 decision,
  confirmed the same day. Recurring until the owner revokes or replaces it. It changes no CI job,
  guard pattern, required check or branch setting.
- **Date / Grantor:** 2026-09-26 / Peter Nguyen.
- **Reason:** Stop repeated one-time owner exceptions for authorized repairs
  to four BER reporting/aggregation files while keeping the protected-file
  guard, independent review and a deliberate administrator merge.
- **Owner decision:** The same answer quoted in AEGIS-APR-046, "Approve fix +
  #333 opt A (Recommended)", selected "option A, a standing gate-guard
  allowlist that already covers these two files". "Allowlist" was the
  coordinating agent's shorthand. After the coordinator explained that option
  A is the packet's documented owner exception, not a CI allowlist
  (`gate-guard` stays failed, a qualifying PR uses a deliberate administrator
  merge with a receipt, and the seven conditions apply), the owner confirmed
  on 2026-09-26: "Yes, option A as defined (Recommended)". Option A is defined in the
  [merged decision packet](../roadmaps/gate-guard-friction-decision.md#option-a-proposed-recurring-scope)
  as an owner exception, not a workflow allowlist: the `gate-guard` check
  still fails and is recorded as failed with an authorized disposition.
- **Scope allowed:** Option A's grant language, now approved: "For authorized
  work in `ModernNomad-98/Project-Aegis`, permit deliberate administrator
  merge when every changed protected path is one of the four eligible BER
  files listed below, the sole failed GitHub Actions check is the existing
  `gate-guard` protected-path condition, and every condition below is
  satisfied. This narrowly supersedes the all-green condition in
  AEGIS-APR-013/024/039 for that signal only. It does not authorize unrelated
  implementation, change the protected path set or branch settings, or waive
  another failed check. Apply until the owner revokes or replaces this
  standing exception." The four eligible paths are
  `tools/behavioral_eval_runner/reporting.py`,
  `tools/behavioral_eval_runner/aggregation.py`,
  `tools/behavioral_eval_runner/tests/test_reporting.py` and
  `tools/behavioral_eval_runner/tests/test_aggregation.py`. Ordinary
  unprotected documentation may accompany an eligible repair. Each use must
  meet the seven conditions in the packet as merged at
  `f7ac19bf4ee3811db3d25774a7d461ac4c87f8a1` (summarized here; that merged
  text governs): separate active work authority; passing
  local checks and Linux `validate-skills` and Windows
  `windows-offline-checks` on the candidate; a guard log showing only its
  protected-path match; independent review of the changed protected surfaces
  with reviewer identity and reviewed head, no unresolved blocker; exact-head
  recheck immediately before merge; a PR receipt recording the PR, full head,
  protected paths, review, local and hosted results, this grant and the merge
  result, describing the guard as failed with an authorized disposition; and
  a post-merge main check, with no unattended auto-merge.
- **Scope FORBIDDEN:** From option A: a PR also touching any other protected
  file is ineligible as a whole; workflow/CI files, CODEOWNERS, the validator,
  Developer Certificate of Origin (DCO) check, guard scripts and tests,
  requirements, parent import files, acceptance machinery and all other BER
  paths keep separate one-time owner decisions. Changes that disable or weaken
  checking, alter merge/review authority, change protected-path policy, or
  modify the guard or approval mechanism need a separate one-time decision
  wherever the code is. Tests cannot be weakened to obtain a pass. A work
  package rule that explicitly reserves its future guard exception for a
  separate decision stays in force unless the owner amends it. No provider
  call, credential access, real-host proof, private input, deployment,
  evidence deletion or spent implementation grant is authorized. Expanding
  the four-path list needs a new owner decision.
- **Evidence:** Direct owner answers in the Project Aegis conversation on
  2026-09-26: the selection quoted in AEGIS-APR-046 and the confirmation
  quoted above, both relayed by the coordinating agent. The decision packet
  merged in [PR #333](https://github.com/ModernNomad-98/Project-Aegis/pull/333)
  as `f7ac19bf4ee3811db3d25774a7d461ac4c87f8a1`.
- **Expiry / use limit:** None stated; recurring until owner revocation or
  replacement. Revocation returns protected merges to per-PR exceptions and
  cannot undo completed merges.

### AEGIS-APR-048: Standing administrator merge once checks are green

- **Event:** GRANT; restates and conditions AEGIS-APR-013 for the merge
  mechanism. It creates no authority beyond AEGIS-APR-013's terms.
- **Status at recording:** ACTIVE from the owner's 2026-09-26 instruction.
  Recurring until the owner revokes or replaces it.
- **Date / Grantor:** 2026-09-26 / Peter Nguyen.
- **Reason:** A governance audit of merged PRs #345–#360 found this
  instruction existed only in chat, so its authority could not be checked
  from the repository.
- **Owner decision:** The owner's exact chat instruction at about 20:15 UTC
  on 2026-09-26 was: "approve admin merge for all future PR once local and
  github action checks are green". On 2026-09-26 at about 20:58 UTC the owner
  approved recording it here as worded: "Approve all five as worded
  (Recommended)", answering a question that listed AEGIS-APR-048 through
  AEGIS-APR-052 by number and one-line summary.
- **Scope allowed:** For separately authorized work in this repository, a
  deliberate administrator merge of a pull request at its exact reviewed head
  (`--match-head-commit`) once that head's required GitHub Actions checks are
  green and local checks pass (see AEGIS-APR-049 for what satisfies the local
  leg). The first uses were
  [PR #355](https://github.com/ModernNomad-98/Project-Aegis/pull/355) and
  [PR #356](https://github.com/ModernNomad-98/Project-Aegis/pull/356), merged
  at 20:17 UTC the same day.
- **Scope FORBIDDEN:** It does not waive a failed `gate-guard` or any other red
  check; AEGIS-APR-039's rule stands, and a protected-path failure is governed
  only by AEGIS-APR-047 or a one-time owner decision. It does not arm
  auto-merge, change branch settings, or authorize work that lacks its own
  grant. It is subject to the review-wait condition in AEGIS-APR-050.
- **Evidence:** Direct owner instruction and direct owner recording approval
  in the Project Aegis conversation on 2026-09-26, quoted above, received by
  the coordinating agent and transcribed here.
- **Expiry / use limit:** None stated; recurring until owner revocation or
  replacement.

### AEGIS-APR-049: Exact-head CI satisfies the local-test condition

- **Event:** GRANT; clarification of AEGIS-APR-013 and AEGIS-APR-048.
- **Status at recording:** ACTIVE from the owner's 2026-09-26 answer.
  Recurring.
- **Date / Grantor:** 2026-09-26 / Peter Nguyen.
- **Reason:** The audit of PRs #345–#360 found that every PR body claimed a
  local validator run but only the hosted re-run of the same checks on the
  exact head was verifiable.
- **Owner decision:** Asked whether a green required-check run on the exact
  merged head counts as satisfying AEGIS-APR-013's "local tests" leg, the
  owner answered on 2026-09-26 at about 20:52 UTC: "Yes, CI on exact head
  suffices (Recommended)". Recording approved as in AEGIS-APR-048.
- **Scope allowed:** A green run of the required GitHub Actions checks on the
  exact merged head, which re-runs `scripts/validate-skills.py`, the offline
  test suites and the Developer Certificate of Origin check, satisfies the
  local-test leg of AEGIS-APR-013 and AEGIS-APR-048. No per-PR attachment of
  local output is required. The coordinating agent applied this reading to
  close the audit's local-test finding for PRs #345–#360, whose bodies claimed
  local runs that CI re-ran on their exact heads; the owner's answer did not
  name those PRs. A work grant that names its own local acceptance tests (for
  example the Windows and pinned-Linux suites in AEGIS-APR-046, or "applicable
  local checks" in AEGIS-APR-047) still requires those runs.
- **Scope FORBIDDEN:** It does not excuse a red or missing check, a check run
  on a different head, or a check whose result was rewritten by a later run.
  A work grant that names additional local acceptance tests (for example the
  Windows and pinned-Linux suites in AEGIS-APR-046) keeps that requirement.
- **Evidence:** Direct owner answer in the Project Aegis conversation on
  2026-09-26, quoted above.
- **Expiry / use limit:** None stated; recurring.

### AEGIS-APR-050: Merges wait for the automated Codex review

- **Event:** GRANT; a policy condition on AEGIS-APR-013 and AEGIS-APR-048.
- **Status at recording:** ACTIVE from the owner's 2026-09-26 answer.
  Recurring.
- **Date / Grantor:** 2026-09-26 / Peter Nguyen.
- **Reason:** The audit of PRs #345–#360 found that the Codex automated
  reviewer posted findings one to four minutes after six merges (including
  three P1 findings on PR #349) and that none had been triaged.
- **Owner decision:** Asked whether merges should wait for Codex, the owner
  answered on 2026-09-26 at about 20:52 UTC: "Wait for Codex, then triage
  (Recommended)". Recording approved as in AEGIS-APR-048.
- **Scope allowed:** Before an administrator merge under AEGIS-APR-013 or
  AEGIS-APR-048, wait until the Codex review has posted on the pull request,
  or until Codex is confirmed unavailable for it (for example a usage-limit
  notice, as on PRs #345–#347). Triage every P1 and P2 finding (Codex's two
  highest priority levels) before merging: fix it, or record in the pull
  request why it is not a defect.
- **Scope FORBIDDEN:** Codex output is not an approval and grants nothing; it
  cannot replace the independent review a work grant requires. Waiting for
  Codex does not extend any other deadline or waive any check.
- **Evidence:** Direct owner answer in the Project Aegis conversation on
  2026-09-26, quoted above.
- **Expiry / use limit:** None stated; recurring until owner revocation.

### AEGIS-APR-051: Eval-file maintenance of delivered skills is backlog delivery

- **Event:** GRANT; clarification of AEGIS-APR-039's scope, with retroactive
  ratification of two merged pull requests.
- **Status at recording:** ACTIVE from the owner's 2026-09-26 answer.
  Recurring.
- **Date / Grantor:** 2026-09-26 / Peter Nguyen.
- **Reason:** PRs #359 and #361 edited `aegis-setup` eval files that are on
  AEGIS-APR-007's exact file list. The implementing and reviewing agents
  classified the edits as maintenance rather than a scope revision, but no
  owner ruling existed.
- **Owner decision:** Asked whether to record such a ruling, the owner
  answered on 2026-09-26 at about 20:52 UTC: "Ratify as maintenance
  (Recommended)". Recording approved as in AEGIS-APR-048.
- **Scope allowed:** Edits confined to `evals/*.json` of an already-delivered
  skill — no change to its `SKILL.md` workflow or authority text and no
  script change — are backlog delivery under AEGIS-APR-039, even when the
  file is named in a consumed one-use implementation grant. This ratifies
  [PR #359](https://github.com/ModernNomad-98/Project-Aegis/pull/359)
  (`639d22fcbf50e81eebe87032ca56ece108cc3507`) and
  [PR #361](https://github.com/ModernNomad-98/Project-Aegis/pull/361)
  (`135eb7f6dfab1627407dafce9dd4da89cc8b3edb`), each of which changed only
  `.claude/skills/aegis-setup/evals/*.json`.
- **Scope FORBIDDEN:** Any edit to a delivered skill's `SKILL.md`, scripts,
  references or state contract keeps the original grant's scope-revision
  rule. It does not reopen a consumed grant's budget or file list.
- **Evidence:** Direct owner answer in the Project Aegis conversation on
  2026-09-26, quoted above.
- **Expiry / use limit:** None stated; recurring.

### AEGIS-APR-052: Consumption of the package-2 implementation grant

- **Event:** CONSUMED; target grant AEGIS-APR-007.
- **Status at recording:** AEGIS-APR-007 has no remaining use.
- **Effective at:** 2026-09-23 16:54:58 UTC.
- **Recorded at / By:** 2026-09-26 / Project Aegis agent, on the owner's
  recording approval quoted in AEGIS-APR-048.
- **New authority:** None. Later eval-only maintenance of the delivered skill
  is covered by AEGIS-APR-051.
- **Reason:** The one bounded package-2 implementation was delivered.
- **Evidence:** [PR #124](https://github.com/ModernNomad-98/Project-Aegis/pull/124)
  merged as `d598390f4b7bb367ce79dd1276157f91ae36556b` at the time above (Git
  merge-commit timestamp 2026-09-23 11:54:58 -05:00).
  [The package-2 review](../evidence/setup/issue-101-package-2-review.md)
  records that package 2 shipped in PR #124.

### AEGIS-APR-053: Consumption of the selected-precheck correction grant

- **Event:** CONSUMED; target grant AEGIS-APR-046.
- **Status at recording:** AEGIS-APR-046 has no remaining use.
- **Effective at:** 2026-09-26 23:24:51 UTC.
- **Recorded at / By:** 2026-09-26 / Project Aegis agent, under the delivery
  grant in AEGIS-APR-039.
- **New authority:** None. This merge was the first use of AEGIS-APR-047; that
  standing exception stays ACTIVE.
- **Reason:** The one bounded implementation package merged, which was
  AEGIS-APR-046's stated use limit.
- **Evidence:**
  [PR #374](https://github.com/ModernNomad-98/Project-Aegis/pull/374) merged
  exact head `6f5d2744a6a0d1f6313af28c682be0ef954055e3` by deliberate
  administrator merge as `7390ae0ac388a7c64ab87a5026fbfa2727113857` at the
  time above. Its branch `fix/ber-precheck-aggregate-validation` was cut from
  the governance merge commit `2aed8dd377e821148b74e077f7c58f4edba6c01e` (tree
  `e0c8f2986fd60a559475bbbe89a93f5c0aa16dac`) and changed exactly
  `tools/behavioral_eval_runner/reporting.py` and
  `tools/behavioral_eval_runner/tests/test_reporting.py`, with 227 added and 5
  deleted lines. The PR body's receipt records independent security and
  quality reviews that passed, the quality review re-verifying the committed
  head, and a Codex review that completed with no findings (AEGIS-APR-050).
  The receipt's original `gate-guard` log citation (job 108487562791, run
  36279161962) was wrong; a correction comment on the PR at 23:43:47 UTC,
  after the merge, replaced it with exact-head job 108505418068 in the run
  below.
  [Exact-head Actions](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/36278386968)
  passed Linux `validate-skills` (full offline BER suite: 1,088 tests, 5
  skipped) and `windows-offline-checks`; `gate-guard` failed, and its log
  lists only the two paths above, dispositioned under AEGIS-APR-047. The
  [post-merge main run](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/36279366010)
  passed Linux and Windows checks; the PR-only guard was skipped.

### AEGIS-APR-054: PR #373 protected-path validator and audit fix

- **Event:** GRANT.
- **Status at recording:** Consumed by AEGIS-APR-056; no remaining use.
- **Date / Grantor:** 2026-09-26 / Peter Nguyen.
- **Reason:** Two protected `scripts/` files blocked reviewed work. A
  validator test pinned project-orchestrator at exactly 49 eval cases and
  requirements-gathering-facilitator at exactly 12, which blocked every
  reviewed eval addition. The skill-contract audit stripped the leading space
  of the first `git status --porcelain` line, so the first dirty path was
  silently dropped from its report.
- **Owner decision:** At about 14:27 Pacific Daylight Time (PDT; 21:27 UTC)
  the owner answered "Approve both, one PR (Recommended)", approving one
  bounded PR that changes `scripts/tests/test_validator.py` (the pinned 49/12
  counts become floors) and `scripts/audit-skill-contracts.py` (keep the
  leading space of the first porcelain line), plus the two eval cases deferred
  for the pins. At about 15:03 PDT (22:03 UTC) the owner answered "Yes, add
  the test to this PR", widening the same PR to a fifth file holding a
  hermetic regression test. After Codex's P2 finding at 23:06 UTC, the two new
  eval ids were also added to that test file's existing exactly-once id lists.
  The owner's answers did not name that detail; it stays within the approved
  file, and the owner's exception in AEGIS-APR-055 approved merging the exact
  head that contains it.
- **Scope allowed:** One pull request changing exactly these five paths:
  `scripts/tests/test_validator.py`, `scripts/audit-skill-contracts.py`,
  `scripts/tests/test_audit_skill_contracts.py`,
  `.claude/skills/project-orchestrator/evals/evals.json` and
  `.claude/skills/requirements-gathering-facilitator/evals/evals.json`,
  for the changes described above.
- **Scope FORBIDDEN:** No other path or behavior change is covered. This
  grant does not itself waive a failed `gate-guard`; the exception for this
  PR's exact head is recorded separately in AEGIS-APR-055. It changes no
  guard pattern, required check or branch setting.
- **Evidence:** Direct owner answers in the Project Aegis conversation on
  2026-09-26, quoted above, relayed by the coordinating agent.
  [PR #373](https://github.com/ModernNomad-98/Project-Aegis/pull/373)
  records the change.
- **Expiry / use limit:** One PR; consumed by the merge recorded in
  AEGIS-APR-056.

### AEGIS-APR-055: PR #373 protected gate-guard exception

- **Event:** GRANT.
- **Status at recording:** Consumed by AEGIS-APR-056; no remaining use.
- **Date / Grantor:** 2026-09-26 / Peter Nguyen.
- **Reason:** Permit the AEGIS-APR-054 fix to merge when its three protected
  `scripts/` paths triggered the guard. They are outside AEGIS-APR-047's four
  BER files, so a one-time owner decision was required.
- **Scope allowed:** The owner answered "Approve exception for 86e45ad" to the
  request for a one-time `gate-guard` exception and administrator merge of
  [PR #373](https://github.com/ModernNomad-98/Project-Aegis/pull/373) at exact
  head `86e45adbef5c407f5926bc329ba848ef806669a2`. The coordinator gave the
  time as about 16:33 PDT, but the PR receipt quoting the answer was posted at
  23:32:12 UTC (16:32:12 PDT), so the answer came no later than that, three
  seconds before the merge. The request reported that
  [exact-head run 36279392000](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/36279392000)
  passed `validate-skills` and `windows-offline-checks`, and that `gate-guard`
  failed with a log matching only `scripts/audit-skill-contracts.py`,
  `scripts/tests/test_audit_skill_contracts.py` and
  `scripts/tests/test_validator.py`. An independent code and security review
  passed; per the PR receipt it reviewed an earlier diff, and the fifth-file
  test and pinned ids were added afterwards at the reviewer's and Codex's
  requests. Codex raised one P2 finding (its second-highest priority level),
  which was fixed at this head, and its re-review of `86e45ad` found no major
  issues. The grant covered one administrator merge of that head through that
  guard result.
- **Scope FORBIDDEN:** No other PR, head or failed check was covered. This
  did not change branch protection or the protected path set, and it did not
  widen AEGIS-APR-047.
- **Evidence:** Direct owner answer in the Project Aegis conversation on
  2026-09-26, quoted above, relayed by the coordinating agent; the
  exception receipt comment on PR #373 records the head, checks, review and
  merge.
- **Expiry / use limit:** One merge of PR #373 at the named head; consumed by
  the merge recorded in AEGIS-APR-056.

### AEGIS-APR-056: Consumption of PR #373 grants

- **Event:** CONSUMED; target grants AEGIS-APR-054 and AEGIS-APR-055.
- **Status at recording:** AEGIS-APR-054 and AEGIS-APR-055 have no remaining
  use.
- **Effective at:** 2026-09-26 23:32:15 UTC.
- **Recorded at / By:** 2026-09-26 / Project Aegis agent, under the delivery
  grant in AEGIS-APR-039.
- **New authority:** None.
- **Reason:** The sole exact-head administrator merge of the one approved PR
  completed.
- **Evidence:** [PR #373](https://github.com/ModernNomad-98/Project-Aegis/pull/373)
  merged `86e45adbef5c407f5926bc329ba848ef806669a2` as
  `4ca04c1effce1de10ec221f4756698bb33d1ae77` at the time above, changing
  exactly the five AEGIS-APR-054 paths. The
  [post-merge main run](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/36279755880)
  passed Linux and Windows checks; the PR-only guard was skipped.

### AEGIS-APR-057: Live startup-routing acceptance test re-run

- **Event:** GRANT.
- **Status at recording:** ACTIVE; granted and not yet consumed. A later
  lifecycle event records its consumption or expiry.
- **Date / Grantor:** 2026-09-27 / Peter Nguyen.
- **Reason:** The README says automatic skill selection was "verified by a
  live acceptance test on 2026-07-30 against the startup files from decision
  D61". That evidence predates later startup-file changes: seven commits
  after 2026-07-30 changed `CLAUDE.md` or `AGENTS.md`, the latest on
  2026-09-25. The claim needs a fresh live run against the current files.
- **Owner decision:** In chat with the Claude Code coordinator on 2026-09-27,
  the owner first chose three runs per case, then chose "Approve, 1 run per
  case". The later one-run choice is the grant; the three-run choice was
  replaced before any run started.
- **Scope allowed:** A one-time grant, as worded: "Live startup-routing
  acceptance test re-run: up to 9 headless Claude Code 2.1.283 sessions on
  claude-opus-5-5 (8 scored cases x 1 run + 1 unscored reference), in new
  scratch folders built from Project-Aegis at
  da2636d049db25a4fc367c025e44636c9de66e6d; tool writes denied in tested
  sessions; stop at 20M input tokens." Committing the redacted evidence
  file is allowed under the existing delivery grants (AEGIS-APR-039 and
  AEGIS-APR-048).
- **Scope FORBIDDEN:** As worded: "Excluded: VirtualBox VM, Stage 4B host
  proof, SDK query(), host bridge/hooks, installs, deployment, private
  data, claims about token savings or host enforcement." No other
  restriction was stated.
- **Evidence:** Direct owner answers in the Project Aegis conversation on
  2026-09-27, quoted above, relayed by the coordinating agent. The README
  claim is in the README section
  [From idea to shipped](../../README.md#from-idea-to-shipped-the-no-experience-path)
  and cites decision D61 in the
  [planning record](../reconciliation/step-0-reconciliation-v4.md).
- **Expiry / use limit:** One run of at most nine sessions. "Expires when the
  run finishes or 2026-09-30."

### AEGIS-APR-058: Overwrite the skill-contract audit baselines

- **Event:** GRANT.
- **Status at recording:** ACTIVE; granted and not yet consumed. A later
  lifecycle event records its consumption.
- **Date / Grantor:** 2026-09-27 / Peter Nguyen.
- **Reason:** The committed audit baselines in `artifacts/audits/` and their
  companion report were produced on 2026-08-07 by engine v1.12.0 (184 skills,
  414 findings). Later remediation and the v1.13.x engine corrections left
  them describing an older corpus. A scoping review found no test, CI
  (continuous integration) job or eval that reads their contents; the source
  library role check only tests that the baseline JSON (JavaScript Object
  Notation) file exists.
- **Owner decision:** In chat with the Claude Code coordinator on 2026-09-27,
  after being told the costs (it breaks comparisons with past audits, touches
  a source-library landmark file, supersedes the earlier "left exactly as it
  is" promise in the AEGIS-060+ register, and leaves the old numbers only in
  git history), the owner chose to overwrite the baselines with that day's
  audit numbers. The decision was relayed by the coordinating agent; no
  verbatim wording is recorded here.
- **Scope allowed:** One pull request that regenerates, with
  `scripts/audit-skill-contracts.py` run unchanged on a clean checkout of
  main, exactly these files:
  `artifacts/audits/skill-contract-audit-baseline.json`,
  `artifacts/audits/corpus-route-graph.json`,
  `artifacts/audits/corpus-manifest-baseline.json` and the companion
  `docs/audits/skill-contract-audit-baseline.md` (with a hand-written
  provenance preface); adds dated notes and history links to
  `docs/audits/aegis-060-plus-register.md`; and appends this entry.
- **Scope FORBIDDEN:** No protected path. In particular, nothing under
  `scripts/` or `tools/` changes, including the three source comments that
  describe the v1.12.0 baseline; they stay as true statements of history. No
  historical count in the AEGIS-060+ register is rewritten.
- **Evidence:** Owner decision in the Project Aegis conversation on
  2026-09-27, relayed by the coordinating agent. The previous baseline files
  remain in git history at commit
  `e2f1da0beb6e4aed07044ca3a90e841962bfd590` (PR #77).
- **Expiry / use limit:** One PR; consumed by its merge, which a later
  lifecycle event records.

### AEGIS-APR-059: Consumption of the live startup-routing test grant

- **Event:** CONSUMED; target grant AEGIS-APR-057.
- **Status at recording:** AEGIS-APR-057 has no remaining use.
- **Effective at:** 2026-09-27 20:54:39 UTC, when the last of the nine
  sessions ended; the grant expired "when the run finishes".
- **Recorded at / By:** 2026-09-27 / Project Aegis agent, under the delivery
  grants in AEGIS-APR-039 and AEGIS-APR-048.
- **New authority:** None. Another live run needs a new owner grant.
- **Reason:** The one approved run finished within its scope.
- **Evidence:** Nine sessions (eight scored cases and one unscored
  reference) ran on 2026-09-27 from 20:06:49 to 20:54:39 UTC and used
  1,444,651 input and 16,725 output tokens in total, far below the
  20-million-input-token stop. No session was retried and no tenth session
  ran, no session attempted a write, and the scope in AEGIS-APR-057 was not exceeded. The
  [live acceptance record](../evidence/startup-routing/2026-09-live-acceptance.md)
  holds the manifest and token table; [PR #433](https://github.com/ModernNomad-98/Project-Aegis/pull/433)
  merged it as `9104cff1f676b7aef310ec83c0f0966020ec85d5` on 2026-09-27 at
  22:58:53 UTC.

### AEGIS-APR-060: Consumption of the audit-baseline overwrite grant

- **Event:** CONSUMED; target grant AEGIS-APR-058.
- **Status at recording:** AEGIS-APR-058 has no remaining use.
- **Effective at:** 2026-09-27 22:44:15 UTC.
- **Recorded at / By:** 2026-09-27 / Project Aegis agent, under the delivery
  grant in AEGIS-APR-039.
- **New authority:** None. The later one-time regeneration with engine
  v1.13.2 is a separate grant, AEGIS-APR-065.
- **Reason:** The one approved PR merged.
- **Evidence:** [PR #432](https://github.com/ModernNomad-98/Project-Aegis/pull/432)
  merged head `d37ae1fc2c792df4631d74a1bd7a66f752c1197c` as
  `7894567d49d301f82f40cb6445b668581d5799ac` at the time above. It changed
  the three `artifacts/audits/` baseline files,
  `docs/audits/skill-contract-audit-baseline.md`,
  `docs/audits/aegis-060-plus-register.md` and this register, and nothing
  under `scripts/` or `tools/`. The regenerated report names engine v1.13.1
  at main commit `656194426e2ea3358fa29fcf19e05f0278d9c270`.

### AEGIS-APR-061: PR #425 protected gate-guard exception

- **Event:** GRANT.
- **Status at recording:** Consumed by AEGIS-APR-062; no remaining use.
  Recorded after the merge.
- **Date / Grantor:** 2026-09-27 / Peter Nguyen.
- **Reason:** The owner's 2026-09-27 decision to date the BER README's pinned
  counts changes `tools/behavioral_eval_runner/README.md`, a protected path
  outside AEGIS-APR-047's four BER files. That decision said the change
  needed a one-time, exact-head `gate-guard` exception at merge and did not
  grant one.
- **Scope allowed:** One `gate-guard` exception and administrator merge of
  [PR #425](https://github.com/ModernNomad-98/Project-Aegis/pull/425) at
  exact head `4c1324a687356af1d11e69e8ae261760f00cbb60`, which changed only
  `tools/behavioral_eval_runner/README.md`.
  [Exact-head run 36347344897](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/36347344897)
  passed `validate-skills` and `windows-offline-checks`; `gate-guard` failed
  on that protected path. An independent review of that head returned SHIP.
  Codex posted only a usage-limit notice after the head.
- **Scope FORBIDDEN:** No other PR, head or failed check was covered. It did
  not change branch protection or the protected path set, and it did not
  widen AEGIS-APR-047.
- **Evidence:** Direct owner answer "Grant for 4c1324a only (Recommended)"
  to the coordinating agent's multiple-choice question in the Project Aegis
  conversation on 2026-09-27, relayed by that agent. The
  [review comment](https://github.com/ModernNomad-98/Project-Aegis/pull/425#issuecomment-5859686774)
  and the
  [exception receipt](https://github.com/ModernNomad-98/Project-Aegis/pull/425#issuecomment-5860244524)
  on PR #425 record the head, checks, review and merge.
- **Expiry / use limit:** One merge of PR #425 at the named head; consumed
  by the merge recorded in AEGIS-APR-062.

### AEGIS-APR-062: Consumption of the PR #425 exception

- **Event:** CONSUMED; target grant AEGIS-APR-061.
- **Status at recording:** AEGIS-APR-061 has no remaining use.
- **Effective at:** 2026-09-27 22:04:12 UTC.
- **Recorded at / By:** 2026-09-27 / Project Aegis agent, under the delivery
  grant in AEGIS-APR-039.
- **New authority:** None.
- **Reason:** The sole exact-head administrator merge completed.
- **Evidence:** [PR #425](https://github.com/ModernNomad-98/Project-Aegis/pull/425)
  merged `4c1324a687356af1d11e69e8ae261760f00cbb60` as
  `7b8884133fe92da8adae6b929c5440e05c1ed10b` at the time above.

### AEGIS-APR-063: PR #429 protected gate-guard exception

- **Event:** GRANT.
- **Status at recording:** Consumed by AEGIS-APR-064; no remaining use.
  Recorded after the merge.
- **Date / Grantor:** 2026-09-27 / Peter Nguyen.
- **Reason:** The owner's 2026-09-27 decision to fix the ROUTE-002
  false positive changes `scripts/audit-skill-contracts.py` and its test,
  protected paths outside AEGIS-APR-047's four BER files. That decision said
  the merge needed a one-time, exact-head `gate-guard` exception and did not
  grant one.
- **Scope allowed:** One `gate-guard` exception and administrator merge of
  [PR #429](https://github.com/ModernNomad-98/Project-Aegis/pull/429) at
  exact head `13a0682b3e70b9290a6a8c7a25fe291dcec93201`, which changed only
  `scripts/audit-skill-contracts.py` (engine v1.13.2) and
  `scripts/tests/test_audit_skill_contracts.py`.
  [Exact-head run 36350453443](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/36350453443)
  passed `validate-skills` and `windows-offline-checks`; `gate-guard` failed
  on those protected paths. An independent code review of that head returned
  SHIP and found that the only audit change was ROUTE-002 going from 233 to
  232 findings, the known false positive. Codex posted only a usage-limit
  notice after the head.
- **Scope FORBIDDEN:** No other PR, head or failed check was covered. It did
  not change branch protection or the protected path set, and it did not
  widen AEGIS-APR-047.
- **Evidence:** Direct owner answer "Grant for 13a0682 only (Recommended)"
  to the coordinating agent's multiple-choice question in the Project Aegis
  conversation on 2026-09-27, relayed by that agent. The
  [review comment](https://github.com/ModernNomad-98/Project-Aegis/pull/429#issuecomment-5860298094)
  and the
  [exception receipt](https://github.com/ModernNomad-98/Project-Aegis/pull/429#issuecomment-5860441506)
  on PR #429 record the head, checks, review and merge.
- **Expiry / use limit:** One merge of PR #429 at the named head; consumed
  by the merge recorded in AEGIS-APR-064.

### AEGIS-APR-064: Consumption of the PR #429 exception

- **Event:** CONSUMED; target grant AEGIS-APR-063.
- **Status at recording:** AEGIS-APR-063 has no remaining use.
- **Effective at:** 2026-09-27 22:31:32 UTC.
- **Recorded at / By:** 2026-09-27 / Project Aegis agent, under the delivery
  grant in AEGIS-APR-039.
- **New authority:** None.
- **Reason:** The sole exact-head administrator merge completed.
- **Evidence:** [PR #429](https://github.com/ModernNomad-98/Project-Aegis/pull/429)
  merged `13a0682b3e70b9290a6a8c7a25fe291dcec93201` as
  `169e8be44d80f08938b7728000251dcfce2223bb` at the time above.

### AEGIS-APR-065: Regenerate the audit baselines once more with engine v1.13.2

- **Event:** GRANT.
- **Status at recording:** ACTIVE; granted and not yet consumed. A later
  lifecycle event records its consumption.
- **Date / Grantor:** 2026-09-27 / Peter Nguyen.
- **Reason:** The baselines written under AEGIS-APR-058 came from engine
  v1.13.1 at main commit `656194426e2ea3358fa29fcf19e05f0278d9c270`. Later
  merges change what the audit reports. The owner's question named three of
  them: PR #424 (`5711ddf`) and PR #428 (`0cb0777`) extended skills, and PR
  #429 (`169e8be`) moved the engine to v1.13.2, which removes the ROUTE-002
  false positive. Other skill changes merged after that commit, including PR
  #427 (`0030e73`), are also picked up by any main commit that contains all
  three.
- **Owner decision:** Asked whether to regenerate the baselines again once
  those PRs merged, the owner answered "Yes, once after all merge
  (Recommended)" to the coordinating agent's multiple-choice question in chat
  on 2026-09-27. All three had merged when
  this entry was written.
- **Scope allowed:** One pull request that regenerates, with
  `scripts/audit-skill-contracts.py` at engine v1.13.2 run unchanged on a
  clean checkout of a main commit that contains PRs #424, #428 and #429,
  exactly these files:
  `artifacts/audits/skill-contract-audit-baseline.json`,
  `artifacts/audits/corpus-route-graph.json`,
  `artifacts/audits/corpus-manifest-baseline.json` and the companion
  `docs/audits/skill-contract-audit-baseline.md` with its provenance preface;
  adds dated notes and history links, as AEGIS-APR-058 did, to
  `docs/audits/aegis-060-plus-register.md`.
- **Scope FORBIDDEN:** No protected path. Nothing under `scripts/` or
  `tools/` changes. No historical count in the AEGIS-060+ register is
  rewritten. No further regeneration is covered.
- **Evidence:** Direct owner answer in the Project Aegis conversation on
  2026-09-27, quoted above, relayed by the coordinating agent. The
  baselines it replaces are in git history at
  `7894567d49d301f82f40cb6445b668581d5799ac` (PR #432).
- **Expiry / use limit:** One PR; consumed by its merge, which a later
  lifecycle event records.

### AEGIS-APR-066: Consumption of the engine v1.13.2 baseline regeneration grant

- **Event:** CONSUMED; target grant AEGIS-APR-065.
- **Status at recording:** AEGIS-APR-065 has no remaining use.
- **Effective at:** 2026-09-27 23:45:02 UTC.
- **Recorded at / By:** 2026-09-27 / Project Aegis agent, under the delivery
  grant in AEGIS-APR-039.
- **New authority:** None. Any further regeneration needs a new grant.
- **Reason:** The one approved PR merged.
- **Evidence:** [PR #441](https://github.com/ModernNomad-98/Project-Aegis/pull/441)
  merged head `d864597108658985a115fdee39e500454409056a` as
  `3c51fb2f6f4a22c6120b38d2a7e9f0074b6bf69c` at the time above. It changed
  exactly the five allowed paths: the three `artifacts/audits/` baseline
  files, `docs/audits/skill-contract-audit-baseline.md` and
  `docs/audits/aegis-060-plus-register.md`. It changed no protected path and
  nothing under `scripts/` or `tools/`. The regenerated report names engine
  v1.13.2 at main commit `5dbf7bc9e958d932bd0c5b093ebecfe61be41840` and
  records 316 findings, 232 of them ROUTE-002. The
  [independent review](https://github.com/ModernNomad-98/Project-Aegis/pull/441#issuecomment-5860898839)
  of that head reproduced the regeneration and returned SHIP.

### AEGIS-APR-067: Consumption of the CP-WP-002 kernel grant

- **Event:** CONSUMED; target grant AEGIS-APR-004.
- **Status at recording:** AEGIS-APR-004 has no remaining use.
- **Effective at:** 2026-09-23 10:10:29 UTC.
- **Recorded at / By:** 2026-09-28 / Project Aegis agent. The owner decided
  in chat on 2026-09-28, answering the coordinating agent's question, to
  record this closeout; the coordinator relayed the decision, not its exact
  wording.
- **New authority:** None. This event records a past delivery and grants
  nothing. Any later control-plane package, including wiring the
  delivery-control suite into CI, needs its own grant.
- **Reason:** The CP-WP-002 implementation package that AEGIS-APR-004 applied
  to was delivered, so the grant's stated use is spent. This missed
  consumption is recorded after the fact, as AEGIS-APR-052 did for
  AEGIS-APR-007.
- **Evidence:** [PR #99](https://github.com/ModernNomad-98/Project-Aegis/pull/99)
  merged head `8dfe237280f8837c6254e456767e405d44fbd148` as
  `be552fb778ec50fd0cbe82eff9f1022235ec11d8` at the time above (Git
  merge-commit timestamp 2026-09-23 05:10:28 -05:00). It changed 20 paths:
  the `tools/aegis_delivery_control/` package and tests,
  `docs/roadmaps/resumable-control-plane-backlog.md`,
  `docs/evidence/control-plane/cp-wp-002-codex-handoff.md`, `README.md` and
  `docs/README.md`. [The control-plane backlog](../roadmaps/resumable-control-plane-backlog.md)
  marks CP-WP-002 DONE under AEGIS-APR-004 through PR #99, with all 28 T,
  9 C and 22 F rows covered.

### AEGIS-APR-068: Consumption of the CP-WP-003A capability-proof grant

- **Event:** CONSUMED; target grant AEGIS-APR-006.
- **Status at recording:** AEGIS-APR-006 has no remaining use.
- **Effective at:** 2026-09-23 16:49:28 UTC.
- **Recorded at / By:** 2026-09-28 / Project Aegis agent, on the owner's
  2026-09-28 chat decision described in AEGIS-APR-067.
- **New authority:** None. This event records a past delivery and grants
  nothing. CP-WP-003 beyond this first increment, CP-WP-004 and any real
  dispatch stay blocked and need their own grants.
- **Reason:** The one bounded CP-WP-003A implementation package was
  delivered, which was AEGIS-APR-006's stated use limit.
- **Evidence:** [PR #123](https://github.com/ModernNomad-98/Project-Aegis/pull/123)
  merged head `d097d25cc65ebbd86cf5d5c132d772111bca690d` as
  `c965595c3c388c94f15174d45fc3d2fa8fd073b4` at the time above (Git
  merge-commit timestamp 2026-09-23 11:49:28 -05:00). Its head descends from
  the grant's merge commit `1af342712d27d5e6ea482b3f451106b4dccaf125`. It
  changed 10 paths, all on AEGIS-APR-006's exact file list, with 557 added
  and 4 deleted lines. [The CP-WP-003A review](../evidence/control-plane/cp-wp-003a-review.md)
  records CP-WP-003A as DONE through PR #123, and
  [the control-plane backlog](../roadmaps/resumable-control-plane-backlog.md)
  keeps CP-WP-003 BLOCKED.

### AEGIS-APR-069: Consumption of the issue #101 package-3 grant

- **Event:** CONSUMED; target grant AEGIS-APR-008.
- **Status at recording:** AEGIS-APR-008 has no remaining use.
- **Effective at:** 2026-09-23 16:42:21 UTC.
- **Recorded at / By:** 2026-09-28 / Project Aegis agent, on the owner's
  2026-09-28 chat decision described in AEGIS-APR-067.
- **New authority:** None. This event records a past delivery and grants
  nothing. The later version-2 revision had its own grant, AEGIS-APR-040,
  already consumed by AEGIS-APR-043.
- **Reason:** The one bounded package-3 implementation was delivered, which
  was AEGIS-APR-008's stated use limit.
- **Evidence:** [PR #121](https://github.com/ModernNomad-98/Project-Aegis/pull/121)
  merged head `d1f7adcb240fd863ef59c57953e50b2626f5d4b1` as
  `34241baf5fd1911f3d7d07915adc3bacd272d4b2` at the time above (Git
  merge-commit timestamp 2026-09-23 11:42:21 -05:00). Its head descends from
  the grant's merge commit `1af342712d27d5e6ea482b3f451106b4dccaf125`. It
  changed exactly the seven paths on AEGIS-APR-008's file list, with 496
  added and 4 deleted lines. [The package-3 review](../evidence/setup/issue-101-package-3-review.md)
  records that package 3 shipped in PR #121, and
  [the setup routing plan](../roadmaps/aegis-setup-routing-plan.md) marks it
  delivered.

### AEGIS-APR-070: Expiry of the 2026-09-24 session delivery grant

- **Event:** EXPIRED; target grant AEGIS-APR-024.
- **Status at recording:** AEGIS-APR-024 has no remaining applicable use.
- **Effective at:** The end of the Project Aegis conversation session in
  which it was granted on 2026-09-24; that date is the grant's, not the
  session's end. The exact end time is not recorded; the
  owner confirmed on 2026-09-28 that the session has ended.
- **Recorded at / By:** 2026-09-28 / Project Aegis agent, on the owner's
  2026-09-28 chat decision described in AEGIS-APR-067.
- **New authority:** None. This event grants nothing and removes nothing
  beyond AEGIS-APR-024 itself. It does not change AEGIS-APR-013,
  AEGIS-APR-039, AEGIS-APR-047 or AEGIS-APR-048, which are separate grants
  with their own terms.
- **Reason:** AEGIS-APR-024 was limited to "Work in this conversation session
  only" and "is not a standing all-work grant for later sessions". That
  session has ended.
- **Evidence:** The expiry wording in AEGIS-APR-024, quoted above, and the
  owner's 2026-09-28 decision.

### AEGIS-APR-071: PR #443 protected gate-guard exception

- **Event:** GRANT.
- **Status at recording:** Consumed by AEGIS-APR-072; no remaining use.
  Recorded after the merge.
- **Date / Grantor:** 2026-09-28 / Peter Nguyen.
- **Reason:** [PR #443](https://github.com/ModernNomad-98/Project-Aegis/pull/443)
  is a Dependabot pull request (GitHub's automated dependency-update bot)
  that bumps the `actions/setup-node` action from v4.4.0 to v7.0.0. It
  changes only `.github/workflows/validate-skills.yml`, a protected workflow
  path outside AEGIS-APR-047's four BER files, so `gate-guard` fails and a
  one-time owner exception is required. The workflow names the action by a
  commit SHA (a "SHA pin"); the new pin
  `820762786026740c76f36085b0efc47a31fe5020` is the commit of the upstream
  `v7.0.0` tag, replacing `49933ea5288caeca8642d1e84afbd3f7d6820020`
  (`v4.4.0`) in both places the workflow uses the action.
- **Scope allowed:** One `gate-guard` exception and administrator merge of
  PR #443 at exact head `7d138eec55bb45bbfa8426960c6ab2efe3f512c8`, which
  changed only `.github/workflows/validate-skills.yml`.
  [Exact-head run 36382534007](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/36382534007)
  passed `validate-skills` and `windows-offline-checks`; `gate-guard` failed
  on that protected path. An independent read-only review of that head,
  covering supply-chain risk (whether the new pin is the genuine upstream
  release) and release readiness (whether it is safe to merge), recommended
  merge; it was reported to the owner in the conversation and, after the
  merge, posted on the PR in the
  [review and exception receipt](https://github.com/ModernNomad-98/Project-Aegis/pull/443#issuecomment-5866908461).
  Codex posted only a
  [usage-limit notice](https://github.com/ModernNomad-98/Project-Aegis/pull/443#issuecomment-5866555248)
  at 2026-09-28 08:46:29 UTC, after the head commit (05:34:52 UTC).
- **Scope FORBIDDEN:** No other PR, head or failed check was covered. It did
  not change branch protection or the protected path set, and it did not
  widen AEGIS-APR-047.
- **Evidence:** Direct owner answer "Approve one-time exception
  (Recommended)" to the coordinating agent's multiple-choice question on a
  one-time `gate-guard` exception for PR #443 at head `7d138ee`, and the
  later answer "Yes, like #429 (Recommended)" choosing to record it after
  the merge, as AEGIS-APR-063 was. Both were given in the Project Aegis
  conversation on 2026-09-28 and relayed by that agent.
- **Expiry / use limit:** One merge of PR #443 at the named head; consumed
  by the merge recorded in AEGIS-APR-072.

### AEGIS-APR-072: Consumption of the PR #443 exception

- **Event:** CONSUMED; target grant AEGIS-APR-071.
- **Status at recording:** AEGIS-APR-071 has no remaining use.
- **Effective at:** 2026-09-28 09:07:40 UTC.
- **Recorded at / By:** 2026-09-28 / Project Aegis agent, under the delivery
  grant in AEGIS-APR-039.
- **New authority:** None. A later Dependabot or other workflow change needs
  its own exception.
- **Reason:** The sole exact-head administrator merge completed.
- **Evidence:** [PR #443](https://github.com/ModernNomad-98/Project-Aegis/pull/443)
  merged `7d138eec55bb45bbfa8426960c6ab2efe3f512c8` as
  `e251c5146f627ec31b7d2f750f0dbabe0bca7ede` at the time above.

### AEGIS-APR-073: Make the audit baseline report readable on its own (engine v1.13.3)

- **Event:** GRANT.
- **Status at recording:** ACTIVE; granted and not yet consumed. A later
  lifecycle event records its consumption.
- **Date / Grantor:** 2026-09-28 / Peter Nguyen.
- **Reason:** The generated report `docs/audits/skill-contract-audit-baseline.md`
  uses shorthand it never explains (for example Repo SHA, sha256, JSON,
  P0/P1/P2/info, the `[severity/confidence/kind]` bracket, "maps: AEGIS-0NN",
  "§5" and the rule codes). Its ROUTE-002 example is cut off mid-sentence by
  a fixed 120-character slice in `to_markdown()`, the audit engine's function
  that writes the report. A fixed sentence still says the report "freezes the
  state of the corpus BEFORE remediation", which has not been true since the
  baselines were regenerated after remediation under AEGIS-APR-058, and again
  under AEGIS-APR-065.
  Readability fixes to a generated report belong in its generator, the
  protected file `scripts/audit-skill-contracts.py`.
- **Owner decision:** The owner answered "Approve as described
  (Recommended)" to the coordinating agent's multiple-choice question in the
  Project Aegis conversation on 2026-09-28, which proposed the terms below.
- **Scope allowed:** One pull request that changes exactly these paths:
  - `scripts/audit-skill-contracts.py`: output format only. `TOOL_VERSION`
    (the engine version constant) goes from 1.13.2 to 1.13.3; `to_markdown()`
    adds a "How to read this report" glossary with a table of rules generated
    from `RULES` (the engine's rule inventory); the ROUTE-002 example is shown
    whole instead of cut at 120 characters; and the stale sentence that says
    the report "freezes the state of the corpus BEFORE remediation" is
    reworded.
  - `scripts/tests/test_audit_skill_contracts.py`: the pinned engine version
    and one new test of the report format.
  - `artifacts/audits/skill-contract-audit-baseline.json` and
    `artifacts/audits/corpus-manifest-baseline.json`: the engine version,
    `engine_sha256` (the engine file's SHA-256 checksum) and the run's
    `branch` value only. The v1.13.3 engine scans a clean checkout
    (`core.autocrlf=false`, the Git setting that leaves line endings
    unconverted) of `5dbf7bc9e958d932bd0c5b093ebecfe61be41840`,
    the commit the v1.13.2 baseline scanned, so `repo_sha` and the corpus
    stay the same.
  - `artifacts/audits/corpus-route-graph.json`, only if regeneration changes
    it.
  - `docs/audits/skill-contract-audit-baseline.md`: regenerated, with its
    hand-written preface carried forward.
  - `docs/audits/aegis-060-plus-register.md`: one dated note.
- **Scope FORBIDDEN:** No change to finding logic, rules, severities, the
  route graph, manifest semantics or provenance logic. No new command-line option
  or input. No other regeneration. The `findings`, `rule_inventory`,
  `vocabulary_census` and `corpus_content_hash` fields of the regenerated
  JSON must be identical to the v1.13.2 baseline. This grant does not waive
  `gate-guard`: merging the PR needs a separate one-time owner exception for
  its exact head, recorded as its own entry.
- **Evidence:** Direct owner answer in the Project Aegis conversation on
  2026-09-28, quoted above, relayed by the coordinating agent. The scan
  target comes from the owner's later answer "Frozen commit 5dbf7bc
  (Recommended)" to the coordinating agent's multiple-choice question in the
  same conversation on 2026-09-28, after the
  [register review](https://github.com/ModernNomad-98/Project-Aegis/pull/453#issuecomment-5866957640)
  found that the grant did not name one. The v1.13.2
  baselines it replaces are in git history at
  `3c51fb2f6f4a22c6120b38d2a7e9f0074b6bf69c` (PR #441, recorded in
  AEGIS-APR-066).
- **Expiry / use limit:** One PR; consumed by its merge, which a later
  lifecycle event records.

### AEGIS-APR-074: PR #461 protected gate-guard exception

- **Event:** GRANT.
- **Status at recording:** Consumed by AEGIS-APR-075; no remaining use.
  Recorded after the merge.
- **Date / Grantor:** 2026-09-28 / Peter Nguyen.
- **Reason:** [PR #461](https://github.com/ModernNomad-98/Project-Aegis/pull/461)
  is the one pull request AEGIS-APR-073 allowed: it moves the audit engine to
  v1.13.3 and changes only the format of its report. It changes
  `scripts/audit-skill-contracts.py` and
  `scripts/tests/test_audit_skill_contracts.py`, protected paths outside
  AEGIS-APR-047's four BER files, so `gate-guard` fails. AEGIS-APR-073 said
  merging the PR needs a separate one-time owner exception for its exact
  head, and did not grant one.
- **Scope allowed:** One `gate-guard` exception and administrator merge of
  PR #461 at exact head `ae719e69b3927e6ff14b2e173e1d3e0466211a5f`, which
  changed only six of the paths AEGIS-APR-073 allows.
  [Exact-head run 36403836890](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/36403836890)
  passed `validate-skills` and `windows-offline-checks`; `gate-guard` failed
  only on `scripts/audit-skill-contracts.py` and
  `scripts/tests/test_audit_skill_contracts.py`, both allowed by
  AEGIS-APR-073. An
  [independent review](https://github.com/ModernNomad-98/Project-Aegis/pull/461#issuecomment-5867286256)
  of that head returned SHIP. It regenerated the baselines from scratch on a
  clean checkout of the frozen commit
  `5dbf7bc9e958d932bd0c5b093ebecfe61be41840` and got byte-identical files.
  Codex posted only usage-limit notices after the head commit (09:27:11
  UTC): at 09:29:34, 09:29:51 and 09:34:49 UTC on 2026-09-28.
- **Scope FORBIDDEN:** No other PR, head or failed check was covered. It did
  not change branch protection or the protected path set, and it did not
  widen AEGIS-APR-047.
- **Evidence:** Direct owner answer "Approve for ae719e6 only (Recommended)"
  to the coordinating agent's multiple-choice question in the Project Aegis
  conversation (Claude Code session) on 2026-09-28, relayed by that agent. The
  [exception receipt](https://github.com/ModernNomad-98/Project-Aegis/pull/461#issuecomment-5867334304)
  on PR #461 records the head, checks, review and merge.
- **Expiry / use limit:** One merge of PR #461 at the named head; consumed
  by the merge recorded in AEGIS-APR-075.

### AEGIS-APR-075: Consumption of the PR #461 exception

- **Event:** CONSUMED; target grant AEGIS-APR-074.
- **Status at recording:** AEGIS-APR-074 has no remaining use.
- **Effective at:** 2026-09-28 09:36:56 UTC.
- **Recorded at / By:** 2026-09-28 / Project Aegis agent, under the delivery
  grant in AEGIS-APR-039.
- **New authority:** None. A later change to a protected path needs its own
  exception.
- **Reason:** The sole exact-head administrator merge completed.
- **Evidence:** [PR #461](https://github.com/ModernNomad-98/Project-Aegis/pull/461)
  merged `ae719e69b3927e6ff14b2e173e1d3e0466211a5f` as
  `dc3c767dc91d936cc8cc70589137ca33e6f44b7c` at the time above.

### AEGIS-APR-076: Consumption of the engine v1.13.3 report-format grant

- **Event:** CONSUMED; target grant AEGIS-APR-073.
- **Status at recording:** AEGIS-APR-073 has no remaining use.
- **Effective at:** 2026-09-28 09:36:56 UTC.
- **Recorded at / By:** 2026-09-28 / Project Aegis agent, under the delivery
  grant in AEGIS-APR-039.
- **New authority:** None. Any further change to the audit engine or
  regeneration of the baselines needs a new grant.
- **Reason:** The one approved PR merged.
- **Evidence:** [PR #461](https://github.com/ModernNomad-98/Project-Aegis/pull/461)
  merged head `ae719e69b3927e6ff14b2e173e1d3e0466211a5f` as
  `dc3c767dc91d936cc8cc70589137ca33e6f44b7c` at the time above. It changed
  six of the paths AEGIS-APR-073 allows:
  `scripts/audit-skill-contracts.py`,
  `scripts/tests/test_audit_skill_contracts.py`,
  `artifacts/audits/skill-contract-audit-baseline.json`,
  `artifacts/audits/corpus-manifest-baseline.json`,
  `docs/audits/skill-contract-audit-baseline.md` and
  `docs/audits/aegis-060-plus-register.md`. It did not change
  `artifacts/audits/corpus-route-graph.json`, because regeneration produced
  the same file. The regenerated report names engine v1.13.3 at the frozen
  commit `5dbf7bc9e958d932bd0c5b093ebecfe61be41840`. Its findings are
  unchanged from the v1.13.2 baseline: 316 in total, 232 of them ROUTE-002.

### AEGIS-APR-077: PR #475 protected gate-guard exception

- **Event:** GRANT.
- **Status at recording:** Consumed by AEGIS-APR-078; no remaining use.
  Recorded after the merge.
- **Date / Grantor:** 2026-09-28 / Peter Nguyen.
- **Reason:** [PR #475](https://github.com/ModernNomad-98/Project-Aegis/pull/475)
  applies six readability edits to `tools/behavioral_eval_runner/README.md`
  from the owner-ordered re-check of documentation pages edited before the
  current readability rule. That file is a protected
  path outside AEGIS-APR-047's four BER files, so `gate-guard` fails, and
  merging needs a one-time owner exception for the exact head.
- **Scope allowed:** One `gate-guard` exception and administrator merge of
  PR #475 at exact head `acdcdad4563bc74e8dfd78c473678cc9a0b39c0b`, which
  changed only `tools/behavioral_eval_runner/README.md`.
  [Exact-head run 36442330809](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/36442330809)
  passed `validate-skills` and `windows-offline-checks`, each running the
  complete offline BER suite (1,088 tests, result OK); `gate-guard` failed only on
  `tools/behavioral_eval_runner/README.md`. An
  [independent review](https://github.com/ModernNomad-98/Project-Aegis/pull/475#issuecomment-5873052127)
  of that head returned ACCEPT, meaning ready to merge, and found the diff
  is exactly the six required edits. Codex posted only usage-limit notices
  after the head
  commit (15:16:05 UTC): at 15:16:35, 15:16:48 and 15:21:27 UTC on
  2026-09-28.
- **Scope FORBIDDEN:** No other PR, head or failed check was covered. It did
  not change branch protection or the protected path set, and it did not
  widen AEGIS-APR-047.
- **Evidence:** Direct owner answers "Prepare it (Recommended)" (to prepare
  the PR) and "Approve for acdcdad only (Recommended)" (the exception) to the
  coordinating agent's multiple-choice questions in the Project Aegis
  conversation (Claude Code session) on 2026-09-28, relayed by that agent.
  The [exception receipt](https://github.com/ModernNomad-98/Project-Aegis/pull/475#issuecomment-5873259254)
  on PR #475 records the head, checks, review and merge.
- **Expiry / use limit:** One merge of PR #475 at the named head; consumed
  by the merge recorded in AEGIS-APR-078.

### AEGIS-APR-078: Consumption of the PR #475 exception

- **Event:** CONSUMED; target grant AEGIS-APR-077.
- **Status at recording:** AEGIS-APR-077 has no remaining use.
- **Effective at:** 2026-09-28 15:31:48 UTC.
- **Recorded at / By:** 2026-09-28 / Project Aegis agent, under the delivery
  grant in AEGIS-APR-039.
- **New authority:** None. A later change to a protected path needs its own
  exception.
- **Reason:** The sole exact-head administrator merge completed.
- **Evidence:** [PR #475](https://github.com/ModernNomad-98/Project-Aegis/pull/475)
  merged `acdcdad4563bc74e8dfd78c473678cc9a0b39c0b` as
  `59b2fb7cbc5dbc27ff33a1d2bf59792d5e865ccc` at the time above.

### AEGIS-APR-079: Second format-only change to the audit report (engine v1.13.4)

- **Event:** GRANT.
- **Status at recording:** ACTIVE; granted and not yet consumed. A later
  lifecycle event records its consumption.
- **Date / Grantor:** 2026-09-28 / Peter Nguyen.
- **Reason:** Under the owner's
  [generated-report rule](../roadmaps/aegis-documentation-readability-backlog.md#remaining-page-review-in-larger-batches),
  the generated report `docs/audits/skill-contract-audit-baseline.md` gets
  one output-format review. That review of the v1.13.3 report returned
  FIX-FIRST (fix before acceptance), and every fix belongs in the generator,
  `scripts/audit-skill-contracts.py`. That review was not published, so
  its required findings are recorded here in full. The report uses three
  names for one kind of finding. It does not spell out "hex"
  (hexadecimal). It never explains CENSUS, STRUCTURAL, Stage-2,
  NOT-COMMIT-ABLE, auto-invocable or the SIDE-004 side-effect classes. Its
  Coverage section says "the validator's surface" instead of naming
  `scripts/validate-skills.py`. A comment in the test file is stale.
  AEGIS-APR-073, the grant for the first format-only change, was consumed
  by the PR #461 merge (AEGIS-APR-076), so this change needs a new grant.
- **Owner decision:** The owner answered "Approve (Recommended)" to the
  coordinating agent's question in the Project Aegis conversation (Claude
  Code session) on 2026-09-28. The question proposed "a second format-only
  change (engine 1.13.3 → 1.13.4) on the same terms as last time: same
  frozen commit 5dbf7bc, findings must stay identical, grant recorded
  first, then one PR, with a one-time guard exception asked at merge". The
  terms below follow AEGIS-APR-073, the precedent, with the version and
  fixes updated.
- **Scope allowed:** One pull request that changes exactly these paths:
  - `scripts/audit-skill-contracts.py`: output format only. `TOOL_VERSION`
    (the engine version constant) goes from 1.13.3 to 1.13.4, and only the
    wording of `_markdown_glossary()` (the function that writes the report's
    "How to read this report" glossary) and of the Coverage section in
    `to_markdown()` (the function that writes the report) changes.
  - `scripts/tests/test_audit_skill_contracts.py`: the pinned engine
    version, the stale comment, and checks that the glossary explains the
    terms above.
  - `artifacts/audits/skill-contract-audit-baseline.json` and
    `artifacts/audits/corpus-manifest-baseline.json`: the engine version,
    `engine_sha256` (the engine file's SHA-256 checksum) and, if it differs,
    the run's `branch` value only.
  - `artifacts/audits/corpus-route-graph.json`, only if regeneration changes
    it.
  - `docs/audits/skill-contract-audit-baseline.md`: regenerated, with its
    hand-written preface carried forward and its version and grant
    references updated.
  - `docs/audits/aegis-060-plus-register.md`: one dated note.

  The v1.13.4 engine scans a clean checkout (`core.autocrlf=false`) of
  `5dbf7bc9e958d932bd0c5b093ebecfe61be41840`, the same frozen commit the
  v1.13.3 baseline scanned, on a branch named
  `chore/audit-engine-v1134-report-format`. The `findings`,
  `rule_inventory`, `vocabulary_census` and `corpus_content_hash` fields of
  the regenerated JSON must be identical to the v1.13.3 baseline merged in
  PR #461 as `dc3c767dc91d936cc8cc70589137ca33e6f44b7c`. The only allowed
  JSON differences are the engine version, `engine_sha256` and, if it
  differs, the run's `branch` value.
- **Scope FORBIDDEN:** No change to finding logic, rules, rule purpose or
  classification text, severities, the route graph, manifest semantics or
  provenance logic. No new command-line option or input. No other
  regeneration. This grant does not waive `gate-guard`: merging the PR
  needs a separate one-time owner exception for its exact head, recorded as
  its own entry.
- **Evidence:** Direct owner answer in the Project Aegis conversation on
  2026-09-28, quoted above, relayed by the coordinating agent. Precedent:
  AEGIS-APR-073 granted the first format-only change on these terms, and
  AEGIS-APR-076 records its consumption by
  [PR #461](https://github.com/ModernNomad-98/Project-Aegis/pull/461), which
  merged head `ae719e69b3927e6ff14b2e173e1d3e0466211a5f` as
  `dc3c767dc91d936cc8cc70589137ca33e6f44b7c`. That merge holds the v1.13.3
  baselines this grant's PR replaces.
- **Expiry / use limit:** One PR; consumed by its merge, which a later
  lifecycle event records.

### AEGIS-APR-080: PR #501 protected gate-guard exception

- **Event:** GRANT.
- **Status at recording:** Consumed by AEGIS-APR-081; no remaining use.
  Recorded after the merge.
- **Date / Grantor:** 2026-09-28 / Peter Nguyen.
- **Reason:** [PR #501](https://github.com/ModernNomad-98/Project-Aegis/pull/501)
  stops new modules from shadowing imports in the gate checks. It changes
  `.github/workflows/validate-skills.yml` and two test files under
  `scripts/tests/`, protected paths outside AEGIS-APR-047's four BER files,
  so `gate-guard` fails, and merging needs a one-time owner exception for
  the exact head.
- **Scope allowed:** One `gate-guard` exception and administrator merge of
  PR #501 at exact head `9ca82d53f351c696813e242577401789a5cdca78`, which
  changed only `.github/workflows/validate-skills.yml`, `docs/offline-ci.md`,
  `scripts/tests/test_audit_skill_contracts.py` and
  `scripts/tests/test_offline_ci.py`.
  [Exact-head run 36468780089](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/36468780089)
  passed `validate-skills` and `windows-offline-checks`; `gate-guard` failed
  only on `.github/workflows/validate-skills.yml`,
  `scripts/tests/test_audit_skill_contracts.py` and
  `scripts/tests/test_offline_ci.py`. An
  [independent security review](https://github.com/ModernNomad-98/Project-Aegis/pull/501#issuecomment-5878003536)
  of that head returned SHIP. Codex posted only usage-limit notices after
  the head commit (18:52:45 UTC): at 18:56:58 and 18:57:20 UTC on
  2026-09-28, so it was confirmed unavailable under AEGIS-APR-050.
- **Scope FORBIDDEN:** No other PR, head or failed check was covered. It did
  not change branch protection or the protected path set, and it did not
  widen AEGIS-APR-047.
- **Evidence:** Direct owner answer "Approve exception, merge (Recommended)"
  to the coordinating agent's multiple-choice question in the Project Aegis
  conversation (Claude Code session) on 2026-09-28, relayed by that agent.
  The [security review](https://github.com/ModernNomad-98/Project-Aegis/pull/501#issuecomment-5878003536)
  on PR #501 records the head and verdict. No separate exception receipt
  was posted on the PR; this entry and AEGIS-APR-081 record the checks and
  merge.
- **Expiry / use limit:** One merge of PR #501 at the named head; consumed
  by the merge recorded in AEGIS-APR-081.

### AEGIS-APR-081: Consumption of the PR #501 exception

- **Event:** CONSUMED; target grant AEGIS-APR-080.
- **Status at recording:** AEGIS-APR-080 has no remaining use.
- **Effective at:** 2026-09-28 20:59:19 UTC.
- **Recorded at / By:** 2026-09-28 / Project Aegis agent, under the delivery
  grant in AEGIS-APR-039.
- **New authority:** None. A later change to a protected path needs its own
  exception.
- **Reason:** The sole exact-head administrator merge completed.
- **Evidence:** [PR #501](https://github.com/ModernNomad-98/Project-Aegis/pull/501)
  merged `9ca82d53f351c696813e242577401789a5cdca78` as
  `c17a567185d4c7f75036c444d07ee6990905317d` at the time above.

### AEGIS-APR-082: PR #503 protected gate-guard exception

- **Event:** GRANT.
- **Status at recording:** Consumed by AEGIS-APR-083; no remaining use.
  Recorded after the merge.
- **Date / Grantor:** 2026-09-28 / Peter Nguyen.
- **Reason:** [PR #503](https://github.com/ModernNomad-98/Project-Aegis/pull/503)
  is the one pull request AEGIS-APR-079 allowed: it moves the audit engine to
  v1.13.4 and changes only the format of its report. It changes
  `scripts/audit-skill-contracts.py` and
  `scripts/tests/test_audit_skill_contracts.py`, protected paths outside
  AEGIS-APR-047's four BER files, so `gate-guard` fails. AEGIS-APR-079 said
  merging the PR needs a separate one-time owner exception for its exact
  head, and did not grant one.
- **Scope allowed:** One `gate-guard` exception and administrator merge of
  PR #503 at exact head `52269aabc8f4dc86db2df95035ef38f6a86d06fb`, which
  changed only six of the paths AEGIS-APR-079 allows.
  [Exact-head run 36483209962](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/36483209962)
  passed `validate-skills` and `windows-offline-checks`; `gate-guard` failed
  only on `scripts/audit-skill-contracts.py` and
  `scripts/tests/test_audit_skill_contracts.py`, both allowed by
  AEGIS-APR-079. An
  [independent reproduction review](https://github.com/ModernNomad-98/Project-Aegis/pull/503#issuecomment-5878051730)
  of the earlier head `9a1d8412f3ae9f365290d6c9499f24f915776e6d` regenerated
  the baselines from scratch on a clean checkout of the frozen commit
  `5dbf7bc9e958d932bd0c5b093ebecfe61be41840` and got byte-identical files.
  It returned FIX-FIRST (fix before acceptance) for one missing
  documentation edit: the dated note in
  `docs/audits/aegis-060-plus-register.md`. A
  [corrected-candidate check](https://github.com/ModernNomad-98/Project-Aegis/pull/503#issuecomment-5878694559)
  of the exact head returned ACCEPT, meaning ready to merge. It found that
  the head adds only that note and that every other file is unchanged from
  the reproduced head. Codex posted only usage-limit notices after the head
  commit (21:00:22 UTC): at 21:01:56 and 21:12:26 UTC on 2026-09-28, so it
  was confirmed unavailable under AEGIS-APR-050.
- **Scope FORBIDDEN:** No other PR, head or failed check was covered. It did
  not change branch protection or the protected path set, and it did not
  widen AEGIS-APR-047 or AEGIS-APR-079.
- **Evidence:** Direct owner answers "Approve exception, merge (Recommended)"
  (the exception) and, later, "Confirm, record it (Recommended)" (to confirm
  this record) to the coordinating agent's multiple-choice questions in the
  Project Aegis conversation (Claude Code session) on 2026-09-28, relayed by
  that agent. The
  [corrected-candidate check](https://github.com/ModernNomad-98/Project-Aegis/pull/503#issuecomment-5878694559)
  on PR #503 records the head, checks and verdict. No separate exception
  receipt was posted on the PR; this entry and AEGIS-APR-083 record the
  checks and merge.
- **Expiry / use limit:** One merge of PR #503 at the named head; consumed
  by the merge recorded in AEGIS-APR-083.

### AEGIS-APR-083: Consumption of the PR #503 exception

- **Event:** CONSUMED; target grant AEGIS-APR-082.
- **Status at recording:** AEGIS-APR-082 has no remaining use.
- **Effective at:** 2026-09-28 22:07:08 UTC.
- **Recorded at / By:** 2026-09-28 / Project Aegis agent, under the delivery
  grant in AEGIS-APR-039.
- **New authority:** None. A later change to a protected path needs its own
  exception.
- **Reason:** The sole exact-head administrator merge completed.
- **Evidence:** [PR #503](https://github.com/ModernNomad-98/Project-Aegis/pull/503)
  merged `52269aabc8f4dc86db2df95035ef38f6a86d06fb` as
  `c14338d254bde3fd7fb9b8060033299cde5d5197` at the time above.

### AEGIS-APR-084: Consumption of the engine v1.13.4 report-format grant

- **Event:** CONSUMED; target grant AEGIS-APR-079.
- **Status at recording:** AEGIS-APR-079 has no remaining use.
- **Effective at:** 2026-09-28 22:07:08 UTC.
- **Recorded at / By:** 2026-09-28 / Project Aegis agent, under the delivery
  grant in AEGIS-APR-039.
- **New authority:** None. Any further change to the audit engine or
  regeneration of the baselines needs a new grant.
- **Reason:** The one approved PR merged.
- **Evidence:** [PR #503](https://github.com/ModernNomad-98/Project-Aegis/pull/503)
  merged head `52269aabc8f4dc86db2df95035ef38f6a86d06fb` as
  `c14338d254bde3fd7fb9b8060033299cde5d5197` at the time above. It changed
  six of the paths AEGIS-APR-079 allows:
  `scripts/audit-skill-contracts.py`,
  `scripts/tests/test_audit_skill_contracts.py`,
  `artifacts/audits/skill-contract-audit-baseline.json`,
  `artifacts/audits/corpus-manifest-baseline.json`,
  `docs/audits/skill-contract-audit-baseline.md` and
  `docs/audits/aegis-060-plus-register.md`. It did not change
  `artifacts/audits/corpus-route-graph.json`, because regeneration produced
  the same file. The regenerated report names engine v1.13.4 at the frozen
  commit `5dbf7bc9e958d932bd0c5b093ebecfe61be41840`, with engine SHA-256
  `e64b7430488c5f47c31faf1abcfa5f46aae876f3362ed8e0de105e988ff10153`. Its
  findings are unchanged from the v1.13.3 baseline: 316 in total, 232 of
  them ROUTE-002.
