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
- **PR** is a GitHub pull request; **issue #nnn** is a GitHub issue. A bare
  **#nnn** does not say which: `#333`, for example, is PR #333, and only the
  word before it tells the two apart. The
  **head** or **exact head** is the specific latest commit of a pull request
  that was checked and approved; a 40-character hexadecimal value is a Git
  object ID (SHA), a commit unless the entry calls it a tree, often shortened
  to 7 characters.
- **CI** (continuous integration) is the GitHub Actions jobs in
  `.github/workflows/validate-skills.yml`: `validate-skills` (the Linux run),
  `windows-offline-checks` (the Windows run), `tools-tests-linux` and
  `tools-tests-windows` (the two tools-test runs) and `gate-guard`. On pull
  requests, `validate-skills` and `gate-guard` are the required checks;
  `gate-guard` runs on pull requests only, and the other three jobs are
  visible coverage that is not registered as required. The **DCO** (Developer
  Certificate of Origin) sign-off check is a pull-request step inside
  `validate-skills` that requires every commit to be signed off, except two
  exempt machine authors — `dependabot[bot]` and `github-actions[bot]` — that
  cannot sign off; [D60](../reconciliation/step-0-reconciliation-v4.md)
  records the exemption and that it is deliberately **not an authentication
  boundary**.
- **gate-guard**, also called the **protected-file guard**, fails whenever a
  pull request changes a protected path: the merge gate or a surface that
  enforces it, such as workflow files, `CODEOWNERS`, the validator, the DCO
  script, CI scripts and tests, or `tools/behavioral_eval_runner/`. The
  paths it matches are the **protected-path pattern**, the shell variable
  `gate_pattern` in `.github/workflows/validate-skills.yml`; [the offline CI
  guide](../offline-ci.md) instead calls it the `gate-guard` pattern, and
  AEGIS-APR-096 is the one entry that calls it `gate_pattern`. A
  **gate-guard exception** is an owner decision to merge despite that
  failure: usually one-time for one exact head, except the standing
  four-file exception in AEGIS-APR-047. An **administrator merge** uses repository
  administrator rights to merge past branch-protection requirements.
- **Codex** is an automated pull-request reviewer; **P1** and **P2** are its
  two highest finding priority levels. In AEGIS-APR-073, **P0**, **P1**,
  **P2** and **info** are instead the skill-contract audit report's four
  finding severity levels, P0 the most severe. An independent reviewer's
  verdict on a head is one of four: **SHIP** means ready to merge,
  **ACCEPT** means accepted, ready to merge, **REVISE** means changes are
  needed before merge, and **FIX-FIRST** means fix a named finding before
  acceptance.
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
- Six coded identifiers, used in AEGIS-APR-079 and defined only by the audit
  engine's own glossary in the report `docs/audits/skill-contract-audit-baseline.md`
  (written by `_markdown_glossary()` in `scripts/audit-skill-contracts.py`):
  **CENSUS** marks a rule whose hits are `info` census data, not defects;
  **STRUCTURAL** marks a rule that checks only that something is present, not
  that it works; **Stage-2** is `project-orchestrator`'s "Define the product"
  stage; **NOT-COMMIT-ABLE** is the commitment-readiness result recorded when
  the evidence a delivery commitment needs is missing;
  **auto-invocable** describes a skill the model may start on its own, one
  whose description does not begin MANUAL-ONLY; and **SIDE-004** is the rule
  that flags an auto-invocable skill's Workflow instructing a side effect,
  its `[class]` being one of the section 5 mutation classes named in
  [the skill-generation standard](../skill-generation-standard.md#5-least-privilege--side-effects).
- Other abbreviations: **ID** identifier, **OS** operating system, **VM**
  virtual machine, **CPU** central processing unit (processor), **SDK**
  software development kit, **CLI** command-line
  interface, **UTC** Coordinated Universal Time, **PDT** Pacific Daylight
  Time, **GiB** gibibyte, **ISO** a disc-image file, **SHA-256** a file
  checksum, **JSON** JavaScript Object Notation, **eval** evaluation (a
  skill's test cases in its `evals/*.json` files).
- **A correction note governs.** Where an entry carries a trailing note block
  (`>` lines, as AEGIS-APR-086 does), read the entry body with that note: the
  note records what is now known or was later changed, and it governs over
  the body it corrects — it is part of the entry, so the rule above still
  holds. Some entry bodies therefore state a premise a reader should not rely
  on until the note at their end has been read.

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

> **Consumption — 2026-09-23, appended 2026-09-30.** The one-use exception
> above was used: PR #104's exact head `cc713da3a1f280c5a7e5add2495e1f76bbae3fcf`
> merged as `c83a0601d9b7945ad407b6fa81bd2563ab501475` at 2026-09-23 15:39:26
> UTC, a single-parent commit on `main`, so the head itself is not in `main`'s
> history. The grant has no remaining use; a later protected-path merge needs
> its own exception. `CONTRIBUTING.md` still cites this entry as the canonical
> example of a PR-limited exception, which it is — of a spent one.

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

> **Appended note — 2026-09-30.** The `#333` in the owner's quoted answer is
> **PR #333**, not an issue; its merge is recorded in this entry, above. The
> preamble's bare-`#nnn` line gives the general rule.

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
  `docs/audits/aegis-060-plus-register.md`. The exact head then had a
  [corrected-candidate check](https://github.com/ModernNomad-98/Project-Aegis/pull/503#issuecomment-5878694559),
  a re-check of the head after that fix. It returned ACCEPT, meaning ready
  to merge. It found that
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

### AEGIS-APR-087: PR #505 protected gate-guard exception

- **Event:** GRANT.
- **Status at recording:** Consumed by AEGIS-APR-088; no remaining use.
  Recorded after the merge.
- **Date / Grantor:** 2026-09-29 / Peter Nguyen.
- **Reason:** [PR #505](https://github.com/ModernNomad-98/Project-Aegis/pull/505)
  makes the validator reject agent files whose frontmatter (the settings block at the top of the file) can run commands
  or widen permissions, and adds `.claude/agents` paths to the paths
  `gate-guard` protects. It changes `.github/workflows/validate-skills.yml`,
  `scripts/validate-skills.py` and test files under `scripts/tests/`,
  protected paths outside AEGIS-APR-047's four BER files, so `gate-guard`
  fails, and merging needs a one-time owner exception for the exact head.
- **Scope allowed:** One `gate-guard` exception and administrator merge of
  PR #505 at exact head `ebda783f8edc3c29bc9da076dbde0eb596d21b9f`, which
  changed only `.github/workflows/validate-skills.yml`, `CONTRIBUTING.md`,
  `README.md`, `docs/offline-ci.md`, `scripts/validate-skills.py`,
  `scripts/tests/test_offline_ci.py`, `scripts/tests/test_validator.py` and
  11 new fixture files under `scripts/tests/fixtures/agents/`.
  [Exact-head run 36506163908](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/36506163908)
  passed `validate-skills` and `windows-offline-checks`; `gate-guard` failed
  only on `.github/workflows/validate-skills.yml`,
  `scripts/validate-skills.py`, `scripts/tests/test_offline_ci.py`,
  `scripts/tests/test_validator.py` and the 11 fixture files. Independent
  security reviews of three earlier heads returned REVISE (changes needed before merge):
  [`9ec3cb1150fda27f758ef413800e5966b87505ef`](https://github.com/ModernNomad-98/Project-Aegis/pull/505#issuecomment-5878774628),
  [`ccb28a21ea7b2e13ac9e366ae87056c58c04d79e`](https://github.com/ModernNomad-98/Project-Aegis/pull/505#issuecomment-5880081301)
  and
  [`89f851586df3179edc6374864757060f511f55d5`](https://github.com/ModernNomad-98/Project-Aegis/pull/505#issuecomment-5880986085).
  The [security re-review](https://github.com/ModernNomad-98/Project-Aegis/pull/505#issuecomment-5881821301)
  of the exact head returned SHIP. Codex posted only usage-limit notices
  after the head commit (01:04:30 UTC): at 01:05:30 and 01:21:53 UTC on
  2026-09-29, so it was confirmed unavailable under AEGIS-APR-050.
- **Scope FORBIDDEN:** No other PR, head or failed check was covered. It did
  not change branch protection, it removed no path from the protected path
  set, and it did not widen AEGIS-APR-047.
- **Evidence:** Direct owner answer "Approve exception, merge (Recommended)"
  to the coordinating agent's multiple-choice question in the Project Aegis
  conversation (Claude Code session) on 2026-09-29, relayed by that agent.
  The [security re-review](https://github.com/ModernNomad-98/Project-Aegis/pull/505#issuecomment-5881821301)
  on PR #505 records the head, checks and verdict. No separate exception
  receipt was posted on the PR; this entry and AEGIS-APR-088 record the
  checks and merge.
- **Expiry / use limit:** One merge of PR #505 at the named head; consumed
  by the merge recorded in AEGIS-APR-088.

### AEGIS-APR-088: Consumption of the PR #505 exception

- **Event:** CONSUMED; target grant AEGIS-APR-087.
- **Status at recording:** AEGIS-APR-087 has no remaining use.
- **Effective at:** 2026-09-29 01:36:07 UTC.
- **Recorded at / By:** 2026-09-29 / Project Aegis agent, under the delivery
  grant in AEGIS-APR-039.
- **New authority:** None. A later change to a protected path needs its own
  exception.
- **Reason:** The sole exact-head administrator merge completed.
- **Evidence:** [PR #505](https://github.com/ModernNomad-98/Project-Aegis/pull/505)
  merged `ebda783f8edc3c29bc9da076dbde0eb596d21b9f` as
  `9f501f3dba4cf39980663bcd7d6d3c359b10715f` at the time above.

### AEGIS-APR-085: BER non-executed-aggregate correction

- **Event:** GRANT.
- **Status at recording:** Owner approved; ACTIVE only after the reviewed
  governance PR containing BER-DEC-015 and this entry merges.
- **Date / Grantor:** 2026-09-28 / Peter Nguyen.
- **Reason:** Code-health finding P2-4 (a priority-2 finding from the
  coordinator's 2026-09-28 code-health review) showed that the Behavioral
  Eval Runner (BER) report builder, `build_run_report`, re-derives a case's
  aggregate (its case-level result) only when the case was `RUNNABLE` and
  had an executed attempt, or was selected and excluded by preflight (the
  check before a case runs). Every other aggregate is trusted, so a report
  could publish a wrong reason for a case that never ran, for example a
  ready case "excluded by preflight" or an unselected case "out of budget".
  No verdict can change, and the builder has no production caller yet.
  AEGIS-APR-046, which covered these two paths once, was consumed by PR #374
  (AEGIS-APR-053), and the BER backlog requires a new owner decision to
  tighten the report contract, so this repair needs a new grant.
- **Owner decision:** "Approve the bounded fix (Recommended)", answering the
  coordinating agent's question in the Project Aegis conversation (Claude
  Code session) on 2026-09-28 about whether to approve the bounded synthetic
  BER correction whose recommended approval wording is quoted below. The
  coordinator relayed and attests the answer. The owner did not select the
  optional second tightening ("a selected case may never report
  `NOT_SELECTED`"), which the investigation recommended against for now.
- **Scope allowed:** The approved wording was: "I approve the bounded
  synthetic BER non-executed-aggregate correction (code-health finding
  P2-4), and only that. Scope: exactly two paths,
  `tools/behavioral_eval_runner/reporting.py` and
  `tools/behavioral_eval_runner/tests/test_reporting.py`. It may tighten the
  report contract in exactly these ways: a PRECHECK_EXCLUDED aggregate is
  accepted only for a selected case that preflight excluded; an unselected
  case must report NOT_SELECTED; every other aggregate must equal its
  re-derivation from its attempts. The selected-exclusion shape (attempts may
  carry NOT_SELECTED) is unchanged. Limits: at most 3 active implementation
  hours and 250 added code/test lines; $0 external spend; synthetic local
  fixtures only; no provider, model or network calls, credentials, host
  probes, dependency installs or live sessions. Order: takes effect after a
  reviewed governance PR appends BER-DEC-015 and the matching APR entry.
  Delivery: one DCO-signed PR from that governance merge commit, exact-path
  staging, focused and full offline BER suites on Windows and pinned Linux,
  independent security and quality review, exact-head checks; `gate-guard`
  dispositioned under AEGIS-APR-047. Use limit: one package, consumed at
  merge." `PRECHECK_EXCLUDED` means preflight excluded the case, and
  `NOT_SELECTED` means the case was not in the run. The branch, acceptance
  tests, evidence handling and stop conditions are recorded in BER-DEC-015 in
  [the BER governance log](../roadmaps/behavioral-eval-runner-backlog.md#ber-dec-015-bounded-synthetic-non-executed-aggregate-correction--owner-approved).
  AEGIS-APR-047 already lists both paths, so a `gate-guard` failure limited
  to them may be dispositioned under its conditions, with this grant as the
  separate active work authority its first condition requires.
- **Scope FORBIDDEN:** Any path other than the two above; any report-contract
  change beyond the three stated rules, including the excluded-case attempt
  contract and the unapproved second tightening; provider, model or network
  calls, credentials, host probes, dependency installs, live sessions, real
  evidence or private inputs. It does not change private-label,
  selected-host, provider-budget, OD-1 or later live-suite gates, and it
  waives no failed check other than a `gate-guard` failure that
  AEGIS-APR-047 covers.
- **Evidence:** Direct owner answer in the Project Aegis conversation on
  2026-09-28, quoted above, relayed and attested by the coordinating agent.
  The investigation reproduced six contradictory synthetic shapes that
  `build_run_report` accepted on `main` at
  `76b399b11e8068ca26171dbd6d715f161757f35e`; neither path changed between
  that commit and this governance PR's base,
  `7bbd4f05306ab52b0cece585e616d396ad1462c9`.
- **Expiry / use limit:** One implementation package; consumed at its merge,
  which a later lifecycle event records. No calendar expiry stated.

### AEGIS-APR-086: CP-WP-002 maintenance for P2-6 guard documentation and tests

- **Event:** GRANT.
- **Status at recording:** Owner approved; ACTIVE only after the reviewed
  governance PR containing this entry merges.
- **Date / Grantor:** 2026-09-28 / Peter Nguyen; limits and delivery
  conditions added by his 2026-09-29 (UTC) answer.
- **Reason:** Code-health finding P2-6 concerns the delivery-control engine
  in `tools/aegis_delivery_control/`. A guard is a named precondition, such
  as `no_fence` or `budget_available`, that the control-plane design requires
  before a state transition commits; a transition-guard pair is one guard
  listed for one transition (28 transitions, 48 distinct guards, 69 pairs).
  `TransitionEngine.authorize` denies a call whose `satisfied_guards` lack a
  required guard, but every one of the 56 production calls passes exactly
  the guard set the engine requires, so that step can never deny. The real
  protection is inline checks in `storage.py` that raise inside the same
  database transaction. The engine's guard step is therefore advisory (it
  documents the guard catalog but enforces nothing), while its docstring
  suggests a second, independent check. A refactor that deleted an inline
  check would be caught only by that check's own negative test, and some
  guards, possibly `budget_available`, may have none. AEGIS-APR-004, the
  CP-WP-002 kernel grant, was consumed (AEGIS-APR-067), and no active grant
  covers edits to `tools/aegis_delivery_control/`.
- **Owner decision:** "Document + traceability tests (Recommended)",
  answering the coordinating agent's question in the Project Aegis
  conversation (Claude Code session) on 2026-09-28. The option selected the
  investigation's option (b), documenting the guard list as advisory and
  pinning current behaviour, together with (b+), the traceability test
  table. It did not select option (a): making each caller compute
  `satisfied_guards` from the checks that actually ran (evidence-computed
  guards). The coordinator relayed and attests the answer; the scope below
  is the coordinator's statement of the selected option. On 2026-09-29, before
  this entry merged, the owner answered a follow-up question about limits and
  delivery conditions with "Add caps + conditions (Recommended)". The option
  he chose read: "Cap at 12 active hours and 800 added lines (mostly the
  traceability test table), $0, one package; same delivery conditions as the
  P2-4 grant; stop and come back if a guard has no inline check." The
  coordinator relayed and attests that answer too.
- **Scope allowed:** One maintenance package, named "CP-WP-002 maintenance:
  P2-6 guard documentation and traceability tests", with no runtime
  behaviour change:
  - `tools/aegis_delivery_control/engine.py`: docstrings (the in-code
    documentation strings) only, stating that
    the transition guard list is advisory, a declarative catalog mirrored by
    authoritative inline checks in `storage.py`, and that the state-pair,
    event-variant and terminal-state checks are the engine's live controls.
  - `tools/aegis_delivery_control/README.md`: the same explanation.
  - `tools/aegis_delivery_control/dispatch.py`: annotate, or remove, the
    three pre-checks that hard-code the current state (T03 `PLANNED ->
    RUNNING`, T10 from `RUNNING`, and T27 `VALIDATING -> VALIDATING`; about
    lines 675, 804 and 919 at the base below), only if the change is
    behaviour-neutral. Otherwise leave them unchanged.
  - `tools/aegis_delivery_control/tests/test_engine.py` and one new test
    module, `tools/aegis_delivery_control/tests/test_guard_traceability.py`,
    holding:
    - one test pinning current behaviour: every production `authorize` call
      passes `TRANSITIONS[tid].required_guards`, with the T09
      pause-request variant, which adds `effect_bound`, as the one listed
      exception, so a partial guard set cannot appear without a
      test and documentation change;
    - a traceability test table mapping each of the 69 transition-guard
      pairs to a named test that proves the inline denial when that guard
      fails;
    - new negative tests filling any gap the table finds, for example
      `budget_available`.

  Limits, from the owner's 2026-09-29 answer: at most 12 active
  implementation hours, excluding CI and owner waiting; at most 800 added
  lines across the listed paths, mostly the traceability test table; USD $0
  external spend; one package. The investigation estimated about 1 to 1.5
  active days. Recording delivery
  and consumption in the control-plane backlog and this register is a later
  separate reviewed governance change. Option (a), evidence-computed guards,
  becomes an entry criterion for CP-WP-003.
- **Scope FORBIDDEN:** No runtime behaviour change: no change to `storage.py`,
  to the engine's decisions, or to any other runtime path. If a traceability
  gap shows a guard with no inline enforcement, adding a check would change
  runtime behaviour, so stop and return to the owner, as the owner's
  2026-09-29 answer also requires. Also stop and return before exceeding
  any limit above. Option (a) is not granted. No CP-WP-003 or CP-WP-004
  work, real authority or real dispatch is authorized. None additionally
  stated.
- **Delivery and guard:** The owner's 2026-09-29 answer applies the same
  delivery conditions as the P2-4 grant, AEGIS-APR-085: one DCO-signed
  implementation PR with exact-path staging, the delivery-control test suite
  run on Windows and in the pinned Linux environment, independent review,
  and exact-head checks. At the base of this governance PR,
  `7bbd4f05306ab52b0cece585e616d396ad1462c9`, the `gate-guard` protected
  pattern in `.github/workflows/validate-skills.yml` does not match
  `tools/aegis_delivery_control/` or any path listed above, so no
  `gate-guard` exception is needed. If the pattern changes before delivery
  and a listed path becomes protected, that failure needs its own owner
  decision.
- **Evidence:** Direct owner answers in the Project Aegis conversation on
  2026-09-28 and 2026-09-29, quoted above, relayed and attested by the
  coordinating agent. On 2026-09-29 the coordinator also asked the owner
  directly: "You chose 'Add caps + conditions (Recommended)' for the P2-6
  grant: cap 12 active hours and 800 added lines, $0, one package; the same
  delivery conditions as the P2-4 grant (sign-off, exact-file staging,
  independent review, Windows + Linux test runs, exact-head checks); stop and
  come back if a guard has no inline check. Confirm?" The owner answered
  "Confirm, record it (Recommended)". The investigation traced all 56
  production calls on `main` at
  `76b399b11e8068ca26171dbd6d715f161757f35e`, traced every T03 guard to its
  inline check and sampled T27 and T28. Between that commit and this
  governance PR's base, `tools/aegis_delivery_control/` changed only in test
  modules outside this grant's paths (PR #512 changed
  `tests/_owner_private_fixtures.py`, `tests/_owner_private_umask.py`,
  `tests/windows_owner_diagnostic.py`, `tests/test_capabilities.py`,
  `tests/test_dispatch.py`, `tests/test_platform.py`, `tests/test_recovery.py`,
  `tests/test_shared_authority_claims.py` and `tests/test_storage.py`);
  `engine.py`, `dispatch.py`, `storage.py`, `README.md` and
  `tests/test_engine.py` did not change.
- **Expiry / use limit:** One maintenance package; consumed at its merge,
  which a later lifecycle event records. No calendar expiry stated.

> **Correction — 2026-09-30, AEGIS-APR-099.** The `Reason` above states that
> the real protection is inline checks in `storage.py` "that raise inside the
> same database transaction". That is **false** for at least one path:
> `storage.py`'s `_record_effect_observation` calls `request.validate()` and
> `authority.verify_source_control_evidence(...)` **before** `BEGIN
> IMMEDIATE`, and the ordering is identical at this grant's own delivery
> commit `2bb44db2`, so the sentence was false when written. It was **not**
> one of the three statements this grant's `Scope allowed` required, and
> AEGIS-APR-099 deleted it from the two delivered files. Read the `Reason`
> above with this note.
>
> **On the recorded certification.** This grant's own entry text is left
> **byte-unchanged**; only additions were made, and no entry text anywhere was
> edited. The certification recorded in the readability ledger hashes the
> register text **from `### AEGIS-APR-001` to the end of the file at that
> commit**, with the trailing newline stripped — verified: that span at
> `e0c9a000` is 169,099 bytes and yields `c80d02f5…` exactly. (Note it is
> **not** "up to `### AEGIS-APR-099`": APR-099 did not exist at `e0c9a000`,
> which held 98 entries ending at APR-098.) Because later commits appended
> inside that span, it no longer reproduces, which is expected growth on an
> append-only register and **not** a tamper signal. To re-verify, compare
> **entry text**, using an explicit convention — a span that ends before this
> note, since the note is the thing being added:
>
> > **Entry hash convention.** The entry text runs from its `### AEGIS-APR-NNN`
> > heading through the **last non-blank line that is not part of an appended
> > `>` note** — every field body included, so a wrapped field's continuation
> > lines count as part of it — with no trailing newline. (Cutting instead at
> > the last line that opens a field, `- **`, would drop continuation lines
> > that most entries carry, so it is not the convention.)
>
> Under that convention APR-086's entry is **7,512 bytes** and hashes to
> **`b0bff36194f1048b4aaee0aac36acf11a3b51bc1b1c506549556692c6c215f55`**, and it
> does so at `2bb44db2` (this grant's delivery), at `e0c9a000` (the certified
> commit), at `99556551`, and here. A span that instead runs to the next
> heading now includes this note and will not match — that is the growth, not
> a defect.

### AEGIS-APR-089: PR #528 protected gate-guard exception

- **Event:** GRANT.
- **Status at recording:** Consumed by AEGIS-APR-090; no remaining use.
  Recorded after the merge.
- **Date / Grantor:** 2026-09-29 / Peter Nguyen.
- **Reason:** [PR #528](https://github.com/ModernNomad-98/Project-Aegis/pull/528)
  guards Claude Code and Git configuration files and skill frontmatter: the
  validator rejects unsafe settings, and `gate-guard` protects more
  configuration paths. It changes `.github/workflows/validate-skills.yml`,
  `scripts/validate-skills.py` and test files under `scripts/tests/`,
  protected paths outside AEGIS-APR-047's four BER files, so `gate-guard`
  fails, and merging needs a one-time owner exception for the exact head.
- **Scope allowed:** One `gate-guard` exception and administrator merge of
  PR #528 at exact head `1e1cc705460603fd760f86f0d172965cd344380d`, which
  changed only `.claude/skills/_template/SKILL.md`,
  `.github/workflows/validate-skills.yml`, `CONTRIBUTING.md`, `README.md`,
  `docs/offline-ci.md`, `docs/skill-generation-standard.md`,
  `scripts/tests/test_offline_ci.py`, `scripts/tests/test_validator.py` and
  `scripts/validate-skills.py`.
  [Exact-head run 36515208724](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/36515208724)
  passed `validate-skills` and `windows-offline-checks`; `gate-guard` failed
  only on `.github/workflows/validate-skills.yml`,
  `scripts/tests/test_offline_ci.py`, `scripts/tests/test_validator.py` and
  `scripts/validate-skills.py`. An
  [independent security review](https://github.com/ModernNomad-98/Project-Aegis/pull/528#issuecomment-5882576389)
  of the earlier head `ef4cf49cc61e122830e686220cad7315443b827c` returned
  REVISE. The
  [corrected-candidate security review](https://github.com/ModernNomad-98/Project-Aegis/pull/528#issuecomment-5883096195)
  of the exact head returned SHIP. Codex posted only a usage-limit notice
  after the head commit (03:00:20 UTC): at 03:00:37 UTC on 2026-09-29, so it
  was confirmed unavailable under AEGIS-APR-050.
- **Scope FORBIDDEN:** No other PR, head or failed check was covered. It did
  not change branch protection, it removed no path from the protected path
  set, and it did not widen AEGIS-APR-047.
- **Evidence:** Direct owner answer "Approve exception, merge (Recommended)"
  in the Project Aegis conversation (Claude Code session) on 2026-09-29, to
  the coordinating agent's question "…PR #528 (config-file guards) is ready
  … needs your exact-head exception to merge. Head: 1e1cc705. … Approve the
  exception and merge?", relayed by that agent. The selected option read: "I
  merge #528 at exactly 1e1cc705 and record the exception in the approval
  register afterwards." The
  [corrected-candidate security review](https://github.com/ModernNomad-98/Project-Aegis/pull/528#issuecomment-5883096195)
  on PR #528 records the head and verdict. No separate exception receipt was
  posted on the PR; this entry and AEGIS-APR-090 record the checks and merge.
- **Expiry / use limit:** One merge of PR #528 at the named head; consumed
  by the merge recorded in AEGIS-APR-090.

### AEGIS-APR-090: Consumption of the PR #528 exception

- **Event:** CONSUMED; target grant AEGIS-APR-089.
- **Status at recording:** AEGIS-APR-089 has no remaining use.
- **Effective at:** 2026-09-29 06:52:03 UTC.
- **Recorded at / By:** 2026-09-29 / Project Aegis agent, under the delivery
  grant in AEGIS-APR-039.
- **New authority:** None. A later change to a protected path needs its own
  exception.
- **Reason:** The sole exact-head administrator merge completed.
- **Evidence:** [PR #528](https://github.com/ModernNomad-98/Project-Aegis/pull/528)
  merged `1e1cc705460603fd760f86f0d172965cd344380d` as
  `3e11d6bba4eade68b9226bec06ca3cd36ef035c3` at the time above.

### AEGIS-APR-091: PR #507 protected gate-guard exception

- **Event:** GRANT.
- **Status at recording:** Consumed by AEGIS-APR-092; no remaining use.
  Recorded after the merge.
- **Date / Grantor:** 2026-09-29 / Peter Nguyen.
- **Reason:** [PR #507](https://github.com/ModernNomad-98/Project-Aegis/pull/507)
  splits the CI workflow so the tools test suites run in their own Linux and
  Windows jobs, outside the gate checks. It changes
  `.github/workflows/validate-skills.yml` and
  `scripts/tests/test_offline_ci.py`, protected paths outside
  AEGIS-APR-047's four BER files, so `gate-guard` fails, and merging needs a
  one-time owner exception for the exact head.
- **Scope allowed:** One `gate-guard` exception and administrator merge of
  PR #507 at exact head `f4d92e4c9abd8cc348958e4b265d7f0a2ca99eec`, which
  changed only `.github/workflows/validate-skills.yml`, `docs/offline-ci.md`
  and `scripts/tests/test_offline_ci.py`.
  [Exact-head run 36533856126](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/36533856126)
  passed `validate-skills`, `windows-offline-checks`, `tools-tests-linux`
  and `tools-tests-windows`; `gate-guard` failed only on
  `.github/workflows/validate-skills.yml` and
  `scripts/tests/test_offline_ci.py`. Independent security reviews of the
  earlier heads `b9b0d29e658be19f60e277ee7da0131d7644d2b4`,
  `3f9c8f1b5c96958866971a1090857d0e63087163`,
  `a74ed455d8d9dcf7365069b5702799e4a08ecce3` and
  `ff8bd15dcab6f5384fc539305e3dd372faf67d3c` each returned SHIP; the PR was
  then rebased onto `main` after PR #528 merged. The
  [security check of the rebased candidate](https://github.com/ModernNomad-98/Project-Aegis/pull/507#issuecomment-5892802293)
  of the exact head returned SHIP. Codex posted only a usage-limit notice
  after the head commit (06:56:17 UTC): at 06:57:48 UTC on 2026-09-29, so it
  was confirmed unavailable under AEGIS-APR-050.
- **Scope FORBIDDEN:** No other PR, head or failed check was covered. It did
  not change branch protection, it removed no path from the protected path
  set, and it did not widen AEGIS-APR-047.
- **Evidence:** Direct owner answer "Approve exception, merge (Recommended)"
  in the Project Aegis conversation (Claude Code session) on 2026-09-29, to
  the coordinating agent's question "PR #507 (CI job split plus the new tools
  test jobs) is ready … needs your exact-head exception. Head: f4d92e4c. …
  Approve the exception and merge?", relayed by that agent. The selected
  option read: "I merge #507 at exactly f4d92e4c, record the exception in the
  register, then rebase #524 (dependency lock) onto it." The
  [security check of the rebased candidate](https://github.com/ModernNomad-98/Project-Aegis/pull/507#issuecomment-5892802293)
  on PR #507 records the head and verdict. No separate exception receipt was
  posted on the PR; this entry and AEGIS-APR-092 record the checks and merge.
- **Expiry / use limit:** One merge of PR #507 at the named head; consumed
  by the merge recorded in AEGIS-APR-092.

### AEGIS-APR-092: Consumption of the PR #507 exception

- **Event:** CONSUMED; target grant AEGIS-APR-091.
- **Status at recording:** AEGIS-APR-091 has no remaining use.
- **Effective at:** 2026-09-29 15:44:08 UTC.
- **Recorded at / By:** 2026-09-29 / Project Aegis agent, under the delivery
  grant in AEGIS-APR-039.
- **New authority:** None. A later change to a protected path needs its own
  exception.
- **Reason:** The sole exact-head administrator merge completed.
- **Evidence:** [PR #507](https://github.com/ModernNomad-98/Project-Aegis/pull/507)
  merged `f4d92e4c9abd8cc348958e4b265d7f0a2ca99eec` as
  `e143daff092a3fae59e05d3b169f6f9319d6c0f4` at the time above.

### AEGIS-APR-093: PR #524 protected gate-guard exception

- **Event:** GRANT.
- **Status at recording:** Consumed by AEGIS-APR-094; no remaining use.
  Recorded after the merge.
- **Date / Grantor:** 2026-09-29 / Peter Nguyen.
- **Reason:** [PR #524](https://github.com/ModernNomad-98/Project-Aegis/pull/524)
  installs the CI Python dependencies from a hash-locked file and adds grouped
  Dependabot updates. It changes `.github/workflows/validate-skills.yml`,
  `requirements-ci.txt` and `scripts/tests/test_offline_ci.py`, protected
  paths outside AEGIS-APR-047's four BER files, so `gate-guard` fails, and
  merging needs a one-time owner exception for the exact head.
- **Scope allowed:** One `gate-guard` exception and administrator merge of
  PR #524 at exact head `b0fd5a43b9899a0610a02846ad4bade9ec6f8401`, which
  changed only `.github/dependabot.yml`,
  `.github/workflows/validate-skills.yml`, `README.md`, `docs/offline-ci.md`,
  `requirements-ci.in`, `requirements-ci.txt` and
  `scripts/tests/test_offline_ci.py`.
  [Exact-head run 36594262045](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/36594262045)
  passed `validate-skills`, `windows-offline-checks`, `tools-tests-linux`
  and `tools-tests-windows`; `gate-guard` failed only on
  `.github/workflows/validate-skills.yml`, `requirements-ci.txt` and
  `scripts/tests/test_offline_ci.py`. An
  [independent review](https://github.com/ModernNomad-98/Project-Aegis/pull/524#issuecomment-5882771535)
  of the earlier head `2d583c881b4a9d54b1026167caf7b29da11f15ca` returned
  REVISE for one small required fix. The
  [corrected-candidate review](https://github.com/ModernNomad-98/Project-Aegis/pull/524#issuecomment-5894140686)
  of the exact head, rebased onto `main` after PR #507 merged, returned
  SHIP. Codex posted only a usage-limit notice after the head commit
  (15:58:10 UTC): at 15:58:56 UTC on 2026-09-29, so it was confirmed
  unavailable under AEGIS-APR-050.
- **Scope FORBIDDEN:** No other PR, head or failed check was covered. It did
  not change branch protection or the protected path set, and it did not
  widen AEGIS-APR-047.
- **Evidence:** Direct owner answer "Approve exception, merge (Recommended)"
  in the Project Aegis conversation (Claude Code session) on 2026-09-29, to
  the coordinating agent's question "PR #524 (hash-locked CI dependencies) is
  ready … needs your exact-head exception. Head: b0fd5a43. … Approve the
  exception and merge?", relayed by that agent. The selected option read: "I
  merge #524 at exactly b0fd5a43 and record the exception in the approval
  register with #528's and #507's." The
  [corrected-candidate review](https://github.com/ModernNomad-98/Project-Aegis/pull/524#issuecomment-5894140686)
  on PR #524 records the head and verdict. No separate exception receipt was
  posted on the PR; this entry and AEGIS-APR-094 record the checks and merge.
- **Expiry / use limit:** One merge of PR #524 at the named head; consumed
  by the merge recorded in AEGIS-APR-094.

### AEGIS-APR-094: Consumption of the PR #524 exception

- **Event:** CONSUMED; target grant AEGIS-APR-093.
- **Status at recording:** AEGIS-APR-093 has no remaining use.
- **Effective at:** 2026-09-29 16:19:29 UTC.
- **Recorded at / By:** 2026-09-29 / Project Aegis agent, under the delivery
  grant in AEGIS-APR-039.
- **New authority:** None. A later change to a protected path needs its own
  exception.
- **Reason:** The sole exact-head administrator merge completed.
- **Evidence:** [PR #524](https://github.com/ModernNomad-98/Project-Aegis/pull/524)
  merged `b0fd5a43b9899a0610a02846ad4bade9ec6f8401` as
  `8fcb4e4ba4055c3d0fbb397f2ab80ba7017af3db` at the time above.

### AEGIS-APR-095: Consumption of the BER non-executed-aggregate correction grant

- **Event:** CONSUMED; target grant AEGIS-APR-085.
- **Status at recording:** AEGIS-APR-085 has no remaining use.
- **Effective at:** 2026-09-29 16:31:26 UTC.
- **Recorded at / By:** 2026-09-29 / Project Aegis agent, under the delivery
  grant in AEGIS-APR-039.
- **New authority:** None. This merge used the standing AEGIS-APR-047
  exception, which stays ACTIVE. Any further BER report-contract change,
  including the second tightening the owner did not approve, needs a new
  owner decision.
- **Reason:** The one bounded implementation package merged, which was
  AEGIS-APR-085's stated use limit.
- **Evidence:** [PR #535](https://github.com/ModernNomad-98/Project-Aegis/pull/535)
  merged exact head `bcd778cf7fb46a8678480ade19476a1805eed304` by deliberate
  administrator merge as `5d006aca2b1b5695efc1d6dc239be5890c4a3aac` at the
  time above. Its branch `fix/ber-non-executed-aggregate-provenance` was cut
  from the governance merge commit
  `a103990ab4de68190650cc4b216be49ad39e8f0f` (PR #525; tree
  `268f00a622746c518ca80f66239273de6a780bf1`) and changed exactly
  `tools/behavioral_eval_runner/reporting.py` and
  `tools/behavioral_eval_runner/tests/test_reporting.py`, with 208 added and
  22 deleted lines. An
  [independent security and quality review](https://github.com/ModernNomad-98/Project-Aegis/pull/535#issuecomment-5894264964)
  of the exact head returned SHIP with no blocking findings.
  [Exact-head run 36587362843](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/36587362843)
  passed Linux `validate-skills` and `windows-offline-checks`; `gate-guard`
  failed, and its log lists only the two paths above, dispositioned under
  AEGIS-APR-047. The
  [merge receipt](https://github.com/ModernNomad-98/Project-Aegis/pull/535#issuecomment-5894408507)
  records the head, protected paths, work authority, review, local and
  hosted results and merge result. Codex posted only usage-limit notices
  after the head commit (15:02:40 UTC): at 15:04:20, 15:04:33 and 16:24:10
  UTC on 2026-09-29, so it was confirmed unavailable under AEGIS-APR-050.
  The [post-merge main run](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/36598341550)
  passed.

### AEGIS-APR-096: PR #543 protected gate-guard exception

- **Event:** GRANT.
- **Status at recording:** Consumed by AEGIS-APR-097; no remaining use.
  Recorded after the merge.
- **Date / Grantor:** 2026-09-29 / Peter Nguyen.
- **Reason:** [PR #543](https://github.com/ModernNomad-98/Project-Aegis/pull/543)
  adds `.github/dependabot.yml` (and `.yaml`) to the paths `gate-guard`
  protects, carrying out the owner's 2026-09-29 decision "Protect it
  (Recommended)". It adds one alternative to `gate_pattern` and removes none.
  It changes `.github/workflows/validate-skills.yml` and
  `scripts/tests/test_offline_ci.py`, protected paths outside
  AEGIS-APR-047's four BER files, so `gate-guard` fails, and merging needs a
  one-time owner exception for the exact head.
- **Scope allowed:** One `gate-guard` exception and administrator merge of
  PR #543 at exact head `8fce63f6fb162617869a574b347f9cd37a94ecc1`, which
  changed only `.github/workflows/validate-skills.yml`, `docs/offline-ci.md`
  and `scripts/tests/test_offline_ci.py`.
  [Exact-head run 36625345752](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/36625345752)
  passed `validate-skills`, `windows-offline-checks`, `tools-tests-linux`
  and `tools-tests-windows`; `gate-guard` failed only on
  `.github/workflows/validate-skills.yml` and
  `scripts/tests/test_offline_ci.py`. The
  [independent review](https://github.com/ModernNomad-98/Project-Aegis/pull/543#issuecomment-5899042081)
  of the exact head returned SHIP. Codex posted only a usage-limit notice
  after the head commit (20:17:25 UTC): at 20:17:51 UTC on 2026-09-29, so it
  was confirmed unavailable under AEGIS-APR-050.
- **Scope FORBIDDEN:** No other PR, head or failed check was covered. It did
  not change branch protection, it removed no path from the protected path
  set, and it did not widen AEGIS-APR-047.
- **Evidence:** Direct owner answer "Approve exception, merge (Recommended)"
  in the Project Aegis conversation (Claude Code session) on 2026-09-29,
  before the merge, to the coordinating agent's question "PR #543 adds
  .github/dependabot.yml (and .yaml) to gate-guard's protected paths, as you
  decided. It's ready to merge. … gate-guard: red, as expected. It flags
  exactly .github/workflows/validate-skills.yml and
  scripts/tests/test_offline_ci.py. No register grant covers these two
  paths, so merging needs your one-time exception for this exact commit.
  Head: 8fce63f6fb162617869a574b347f9cd37a94ecc1. Approve the exception and
  merge?", relayed by that agent. The selected option read: "I merge #543 at
  exactly 8fce63f6 (the merge fails if the head moves) and record the
  exception in the approval register afterwards." The
  [merge receipt](https://github.com/ModernNomad-98/Project-Aegis/pull/543#issuecomment-5899449010)
  on PR #543 records the grant, head, flagged paths, review, checks and
  merge.
- **Expiry / use limit:** One merge of PR #543 at the named head; consumed
  by the merge recorded in AEGIS-APR-097.

### AEGIS-APR-097: Consumption of the PR #543 exception

- **Event:** CONSUMED; target grant AEGIS-APR-096.
- **Status at recording:** AEGIS-APR-096 has no remaining use.
- **Effective at:** 2026-09-29 21:36:59 UTC.
- **Recorded at / By:** 2026-09-29 / Project Aegis agent, under the delivery
  grant in AEGIS-APR-039.
- **New authority:** None. A later change to a protected path needs its own
  exception.
- **Reason:** The sole exact-head administrator merge completed.
- **Evidence:** [PR #543](https://github.com/ModernNomad-98/Project-Aegis/pull/543)
  merged `8fce63f6fb162617869a574b347f9cd37a94ecc1` as
  `74411bc59072400a7eb7452c96a6061413c4065d` at the time above, with the
  merge pinned to that head.

### AEGIS-APR-098: Consumption of the CP-WP-002 P2-6 maintenance grant

- **Event:** CONSUMED; target grant AEGIS-APR-086.
- **Status at recording:** AEGIS-APR-086 has no remaining use.
- **Effective at:** 2026-09-29 19:43:17 UTC.
- **Recorded at / By:** 2026-09-29 / Project Aegis agent, under the delivery
  grant in AEGIS-APR-039. AEGIS-APR-086 requires recording its delivery and
  consumption in the control-plane backlog and this register as a later
  separate reviewed governance change; this entry and the accompanying
  backlog update are that change.
- **New authority:** None. AEGIS-APR-086's option (a), evidence-computed
  guards, remains ungranted and is an entry criterion for CP-WP-003, not
  authorization. No CP-WP-003 or CP-WP-004 work, real authority or real
  dispatch follows from this consumption.
- **Reason:** The one bounded maintenance package, "CP-WP-002 maintenance:
  P2-6 guard documentation and traceability tests", merged, which was
  AEGIS-APR-086's stated use limit.
- **Evidence:** [PR #539](https://github.com/ModernNomad-98/Project-Aegis/pull/539)
  merged exact head `df1906534fb8d696a1e15837b8fb115fc12a3d0e` by
  administrator merge as `2bb44db234fa8f98c8e84110528eabb982ce79f7` at the
  time above. Its branch `fix/p2-6-guard-traceability` was cut from the
  governance merge commit `43d8b6be70bab21b76080bea5afb702f148ba755` (PR
  #537) and changed exactly `tools/aegis_delivery_control/engine.py` (+39/−2),
  `tools/aegis_delivery_control/README.md` (+14/−1) and the new
  `tools/aegis_delivery_control/tests/test_guard_traceability.py` (+681),
  with 734 added and 3 deleted lines: inside AEGIS-APR-086's
  800-added-line cap and its one-package limit, both demonstrated directly by
  the line counts and the three changed paths. The grant's 12-active-hour cap
  is recorded as the implementer's attestation; it is not independently
  verifiable from the repository or GitHub. The delivery changed no
  `storage.py`, `dispatch.py`, `test_engine.py` or other runtime path.
  An
  [independent review](https://github.com/ModernNomad-98/Project-Aegis/pull/539#issuecomment-5897366819)
  of the exact head returned SHIP with no blocking findings; the reviewer
  confirmed `engine.py`'s parsed code structure is identical to the base once
  docstrings are removed, so the change is behaviour-neutral.
  [Exact-head run 36619296295](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/36619296295)
  passed all five checks: `gate-guard`, `validate-skills`,
  `windows-offline-checks`, `tools-tests-linux` and `tools-tests-windows`;
  no `gate-guard` exception was needed, because
  `tools/aegis_delivery_control/` is not a protected path. Codex posted only
  usage-limit notices after the head commit (19:26:40 UTC): at 19:38:05 and
  19:42:04 UTC on 2026-09-29, so it was confirmed unavailable under
  AEGIS-APR-050. The two non-blocking review findings were recorded rather
  than fixed: the T03 slot-test tightening is a test-only follow-up that
  AEGIS-APR-086's delivery conditions did not authorize changing after the
  fact, and the unreachable
  `receipt accounting transition is not permitted` branch in `storage.py`
  is recorded in the control-plane backlog as a note for CP-WP-003, because
  removing it would be a runtime change that AEGIS-APR-086 forbids.

### AEGIS-APR-099: Correction of an un-required clause in the AEGIS-APR-086 guard documentation

- **Event:** GRANT; a bounded correction, not a reopening of AEGIS-APR-086.
- **Status at recording:** ACTIVE from the owner's 2026-09-30 answer.
- **Date / Grantor:** 2026-09-30 / Peter Nguyen.
- **Reason:** AEGIS-APR-086 froze guard documentation in
  `tools/aegis_delivery_control/engine.py` and
  `tools/aegis_delivery_control/README.md`, and AEGIS-APR-098 records it
  consumed. An audit of every owner grant that freezes documentation wording
  found that its **`Scope allowed` requires exactly three statements**: that
  the transition guard list is advisory; that it is a declarative catalog
  mirrored by authoritative inline checks in `storage.py`; and that the
  state-pair, event-variant and terminal-state checks are the engine's live
  controls. The delivered text added a **fourth, un-required clause** —
  that those checks "raise inside the same database transaction that would
  record the event". That clause is **false**:
  `storage.py`'s `_record_effect_observation` calls `request.validate()` and
  `authority.verify_source_control_evidence(...)` **before** `BEGIN
  IMMEDIATE`, and the ordering is identical at AEGIS-APR-086's own delivery
  commit `2bb44db2`, so the clause was false when written. It is not a
  stated limitation of the synthetic kernel: the package does contain
  transactional raises; this method's deny path is simply not one.
  No owner-approved source states the transaction relationship — the design
  document contains no match — so there was nothing to point readers at
  instead. Because the frozen clause is not among the three required
  statements, deleting it **restores** the grant's own intent rather than
  contradicting owner-approved wording, which is why this is a correction and
  not a revocation.
- **Owner decision:** Asked on 2026-09-30 whether to correct the clause, the
  owner selected the option: "Grant the narrow correction scoped to the EXTRA
  clause only — delete the un-required false clause in `engine.py` and
  `README.md`, leaving all three required statements byte-identical, and
  correct the Register's Reason premise."
- **Scope allowed:** Exactly two prose deletions, no others:
  - `tools/aegis_delivery_control/engine.py`: remove the clause "raise inside
    the same database transaction that would record the event" from the module
    docstring, leaving the inline-check statement and the sentence that
    follows it intact.
  - `tools/aegis_delivery_control/README.md`: remove the same clause from the
    guard explanation, leaving the inline-check statement and the link to
    `tests/test_guard_traceability.py` intact.
  - Append this entry. The Reason premise in AEGIS-APR-086 is corrected **by
    this entry**, not by editing AEGIS-APR-086, whose entry is immutable
    under the register's own preamble.
  The three statements AEGIS-APR-086 actually required are unchanged byte for
  byte.
- **Scope FORBIDDEN:** No runtime behaviour change of any kind: no change to
  `storage.py`, to the engine's decisions, to any other runtime path, or to
  any non-docstring code. No edit to AEGIS-APR-086's own entry. No edit to
  AEGIS-APR-086's other delivery paths (`dispatch.py`, `test_engine.py`,
  `test_guard_traceability.py`) — the traceability table that pins the guard
  pairs is not to be altered, because it pins verified behaviour. No change to
  any other wording in the two files. No provider call, credential, real-host
  proof, real dispatch, CP-WP-003 or CP-WP-004 work, or spent-grant renewal.
- **Evidence:** The owner's 2026-09-30 answer, quoted above, in the Project
  Aegis conversation. The false clause was located by a multiline-aware search
  over tracked files, which found **three** locations where a line-oriented
  search found one: `tools/aegis_delivery_control/engine.py`,
  `tools/aegis_delivery_control/README.md` and this register's AEGIS-APR-086
  Reason. Behaviour neutrality is demonstrated the same way AEGIS-APR-086's own
  delivery demonstrated it: `ast.dump` of the module with docstrings stripped
  is identical before and after the change, so the parsed code structure is
  unchanged. The focused suites `test_guard_traceability` and `test_engine`
  pass (27 tests, OK), and `scripts/validate-skills.py` reports 195 valid with
  0 warnings.
- **Expiry / use limit:** One package; consumed at its merge, which a later
  lifecycle event records. No calendar expiry stated.
### AEGIS-APR-100: Standing commit, push and merge pre-approval

- **Event:** GRANT; a new grant. It does not renew, widen or supersede
  AEGIS-APR-024, and it changes no other grant.
- **Status at recording:** ACTIVE. The owner settled the standing question on
  2026-09-30 by directing that this authority be recorded as **standing** and
  **forward-only**.
- **Date / Grantor:** 2026-09-28 / Peter Nguyen. That is the date the owner's
  words were first written into this repository (commit `36be74b5`); the
  2026-09-30 direction only records them.
- **Reason:** The instruction existed only in chat. The open-decisions row that
  preserves it states at that recording that it "has no register entry", and
  eleven pages reference or cite it (a search for its wording and its known
  paraphrases; several state it as an operative rule), so the authority behind
  this repository's commits, pushes and merges could not be checked from the
  repository. Recording it closes the gap that earlier produced AEGIS-APR-048
  and AEGIS-APR-050.
- **Scope allowed:** The owner's exact instruction, quoted verbatim as recorded
  in this repository, is: "all commits, push, and merges are pre-approved as
  long as they passed local tests and green on github actions". It covers
  commits, pushes and merges for separately authorized Project Aegis
  source-library work when applicable local tests and GitHub Actions checks are
  green. For a new head, local checks precede commit/push; exact-head Actions
  are checked after publication and before merge, because they cannot run on
  that head before push.

  Relationship to existing grants, all of which remain in force and unchanged:
  AEGIS-APR-002 and AEGIS-APR-013 (administrator merges, the latter with the
  green-check condition) and AEGIS-APR-048 (standing administrator merge once
  checks are green). This entry restates their green condition for commits,
  pushes and merges and adds no authority beyond it. AEGIS-APR-049 (a green
  exact-head required-check run satisfies the local-test leg) and
  AEGIS-APR-050 (merges wait for the Codex review, or for Codex to be confirmed
  unavailable) continue to apply. AEGIS-APR-047 remains the only standing
  `gate-guard` exception, and AEGIS-APR-039's delivery rule stands.

  It is a **new grant**, not a renewal or widening of AEGIS-APR-024: that entry
  quoted a different instruction ("I pre-approve all commit,push, merge from the
  work in this session ...") and was EXPIRED because it was session-scoped and
  "is not a standing all-work grant for later sessions", whereas this
  instruction names no session and the owner has now recorded it as standing.

  **Forward-only.** This grant does not retroactively cover merges made before
  it was recorded. It is not needed for them: each was independently reviewed
  and merged at its exact reviewed head under the then-applicable standing
  grants.
- **Scope FORBIDDEN:** This delivery grant does not start or enlarge a work
  package, waive a failed local test or GitHub Actions check, waive a protected
  `gate-guard` (a protected-path failure still needs a one-time exact-head owner
  exception, or the standing AEGIS-APR-047 exception where all its conditions
  hold), waive the independent-review requirement, alter branch protection, arm
  auto-merge, or authorize provider, host, private-data, deployment or release
  work. A separate applicable work grant is still needed. It is a grant about
  delivery mechanics, not a grant of work.
- **Evidence:** The instruction is recorded verbatim in
  `docs/roadmaps/aegis-open-decisions-2026-09-23.md` under "Decided on
  2026-09-28", in the row "Standing chat instruction on commits, pushes and
  merges", written by Peter Nguyen in commit `36be74b5` ("docs: record later
  2026-09-28 owner decisions in the open-decisions index",
  2026-09-28 02:29:04 -0700) and retrievable with
  `git show origin/main:docs/roadmaps/aegis-open-decisions-2026-09-23.md`. The
  owner's 2026-09-30 direction to record it as a standing, forward-only new
  entry is the answer to decision 1 in
  `docs/evidence/session-continuation-2026-09-30-evening.md`, which is on
  `main` as of commit `1955c222` (PR #586). That page's section 4 records the
  owner's choice in the words "Standing, forward-only", and its section 6
  rule row cross-references the same choice; its section 6 heading calls the
  section TEMPORARY, so this entry relies on section 4, not section 6.
- **Expiry / use limit:** None stated. It survives this session; the owner
  recorded it as standing on 2026-09-30. It may be revoked or superseded by a
  later lifecycle event, which must be appended rather than applied by editing
  this entry.
### AEGIS-APR-101: Ledger keeper role and two historical recording acts

- **Event:** GRANT and explicit ratification.
- **Status at recording:** ACTIVE only after explicit owner approval and recording on the default branch.
- **Date / Grantor:** 2026-10-03 UTC / Peter Nguyen. Owner approval was given on 2026-10-02 at 18:05:09 America/Los_Angeles; the repository recording date is 2026-10-03 UTC, which is the same UTC date as the approval and a later instant than it.
- **Reason:** Establish authority for recording completed documentation reviews and resolve the authority gap for the two recording acts delivered in PR #635.
- **Scope allowed:** Establish a standing ledger keeper role for recording qualifying documentation acceptances in `docs/roadmaps/aegis-documentation-readability-backlog.md`. The keeper must be a different agent from the page's author and accepting reviewer. The coordinator may not hold this role. The keeper may record an existing qualifying review decision, bound to the exact reviewed revision and its posted evidence; it may not independently confer acceptance. If the reviewer declines acceptance or the required evidence is missing, record no acceptance.
- **Historical ratification:** Ratify only the two recording acts delivered in PR #635 for `docs/evidence/setup/issue-101-package-4a-host-feasibility.md` and `docs/evidence/setup/issue-101-package-4a-offline-review.md`, based on REVIEW-2's PR #625 comment 5963410567 at revision `e6fc8d24ad782cfc93e3b2639c1e2b6e5a35b08e`. This ratification does not assert that authority existed beforehand or that later document versions remain accepted.
- **Scope FORBIDDEN:** No self-review, overriding review findings, merging by the keeper, or waiver of existing review and delivery requirements. No approval of the charter's proposed canonical index, its precedence, or changed counting rules. No Stage 4B, helper comparison, private BER candidate approval, or other work-package authority.
- **Evidence:** In the Project Aegis decision conversation, the owner was asked, "Do you approve this limited role and the two historical recording acts, with the coordinator excluded?" The owner answered "approved" on 2026-10-02 at 18:05:09 America/Los_Angeles, equivalent to 2026-10-03 at 01:05:09 UTC. The subsequent owner-supplied handoff prompt authorizes transcription and narrowly scoped consistency updates. Link PR #635 and PR #625 comment 5963410567 as evidence of the historical recording acts, not as substitutes for owner approval.
- **Expiry / use limit:** Standing until revoked or superseded; historical ratification is limited to the two recording acts above. Append subsequent lifecycle events without rewriting this entry.
### AEGIS-APR-102: Gradual integration roadmap and release policy

- **Event:** POLICY DECISION; a policy decision only, not a GRANT. It selects a
  policy target and grants no work.
- **Status at recording:** ACTIVE as policy. It takes effect once this entry is
  on the default branch.
- **Date / Grantor:** 2026-10-02 / Peter Nguyen. The owner approved the roadmap
  and release policy on 2026-10-02; this entry was recorded at
  2026-10-03T01:33:16Z.
- **Reason:** The owner decided how the six candidate integrations — Claude,
  Codex, DeepSeek, Copilot, Cursor and Kimi — are to be taken up, so that an
  unproven candidate cannot reach users and so that one integration completes
  its proofs before the next begins. Without a recorded decision the backlog
  ordering and the visibility rule existed only in chat.
- **Scope allowed:** The owner approved a gradual integration roadmap and
  release policy for those six integrations, on these five binding
  constraints:
  1. **Release one integration at a time.** Complete the selected
     integration's required proof, independent review and scoped release
     requirements before beginning implementation of the next. If the current
     integration cannot meet those requirements, explicitly stop and return it
     to PARKED before selecting another.
  2. **Show users only proven, released integrations.** Aegis's normal setup,
     recommendations and integration-selection menus must contain only
     integrations that passed verification and were released. Never display
     untested candidates as selectable, experimental, unavailable or
     coming-soon choices. Research candidates belong in the development
     backlog.
  3. **Park everything not selected.** Unproven integrations remain PARKED in
     the backlog until explicitly selected for a bounded increment. Selection
     permits only the work separately authorized for that increment; it does
     not make the integration available to users.
  4. **Bind support to the tested configuration.** Record the coding
     application, operating system, relevant versions, provider/model
     configuration and verified capabilities. Do not extend a successful
     result automatically to another model, editor, terminal, cloud
     environment or software version.
  5. **Keep proof and release separate.** Passing Stage 4B does not by itself
     authorize release, establish helper quality or prove cost savings. The
     applicable later evaluation and release requirements must be completed
     before presenting the integration to users.

  **Candidate ordering.** The owner retained the existing Claude Agent SDK
  bridge as the first planning candidate and Codex as the proposed second
  candidate. The remaining integrations stay PARKED. The exact DeepSeek coding
  environment must be identified before its increment can be selected.

  This approves the roadmap and release policy **only**. It bears on
  integration selection and release visibility; it resolves no open-decisions
  row and begins no increment by itself.
- **Scope FORBIDDEN:** No installation, credential access, live session,
  provider spending, helper evaluation or release execution. No integration
  becomes user-visible by virtue of this entry. Each increment requires its own
  exact scope and applicable authority, recorded before it takes effect. It
  does not grant Stage 4B, host proof, or CP-WP-003 and CP-WP-004 selection,
  and it does not authorize any real host session, provider call, paid
  evaluation or helper default. It waives no review, green-check, `gate-guard`
  or DCO requirement.
- **Evidence:** The owner's 2026-10-02 instruction approving the gradual
  integration roadmap and release policy is the source of this entry. The
  event vocabulary used above is this register's own, at
  [the preamble](#how-to-read-this-register), where `POLICY DECISION` "selects
  a policy target, grants no work". The open-decisions rows this entry leaves
  unresolved are in `docs/roadmaps/aegis-open-decisions-2026-09-23.md`: "Issue
  #101 Stage 4B host proof" and "CP-WP-003 and CP-WP-004", the latter reading
  "then selection of one bounded real integration for CP-WP-004; both need
  separate reviewed scope and grants". The first planning candidate's
  in-repository identity is the offline package 4A prototype direction
  described in `docs/roadmaps/aegis-setup-routing-plan.md`; the phrase "Claude
  SDK bridge" appears in no file on the default branch, so this entry does not
  quote it. The owner's approval text itself exists **outside** the repository
  and is not a repository artifact: that text is **unsure** here — it is not
  repo-verifiable, and this entry rests on the owner's instruction rather than
  on any repository citation of it.
- **Expiry / use limit:** The policy stands until superseded by a later
  recorded owner decision. The candidate order is revisable only by a later
  recorded owner decision. Append subsequent lifecycle events without
  rewriting this entry.

### AEGIS-APR-103: PR #648 protected gate-guard exception

- **Event:** GRANT.
- **Status at recording:** Consumed by the merge recorded in this entry; no
  remaining use. Recorded after the merge.
- **Date / Grantor:** 2026-10-03 / Peter Nguyen.
- **Reason:** [PR #648](https://github.com/ModernNomad-98/Project-Aegis/pull/648)
  teaches the Markdown link checker to resolve links that line-wrapping split,
  and adds the fixtures for it. It changes
  `scripts/ci/check-markdown-links.py`,
  `scripts/tests/test_markdown_links.py` and five fixtures under
  `scripts/tests/fixtures/markdown-links/wrapped/`, protected paths outside
  AEGIS-APR-047's four BER files, so `gate-guard` fails, and merging needs a
  one-time owner exception for the exact head.
- **Owner decision:** "Grant + merge now, track the bound as a follow-up" — a
  choice among dispositions offered to the owner on 2026-10-03 in the Project
  Aegis session. The same answer authorized landing the change **with** the
  non-blocking `[MAJOR]` below tracked as a follow-up, which is why this entry
  records that bound rather than treating the review as clean.
- **Scope allowed:** One `gate-guard` exception and administrator merge of
  PR #648 at exact head `33c81fdabc6e8e59a8378c2206b551fc82ff31dd`, merged as
  `20fadd4804a965819a2e2c444b30a62ce7c24477` at 2026-10-03T06:20:30Z under
  `--match-head-commit`, so the merge would have been refused had the head
  moved. The head changed only `scripts/ci/check-markdown-links.py`,
  `scripts/tests/test_markdown_links.py` and five fixtures under
  `scripts/tests/fixtures/markdown-links/wrapped/` (`README.md`, `code.md`,
  `target-split.md`, `unwrapped-twin.md`, `wrapped-target.md`) — seven paths,
  +579/−12. At that exact head `validate-skills`, `windows-offline-checks`,
  `tools-tests-linux` and `tools-tests-windows` concluded SUCCESS and
  **`gate-guard` concluded FAILURE**; that failure is recorded here as
  **failed with an authorized disposition, not waived and not a pass**. The
  [independent review](https://github.com/ModernNomad-98/Project-Aegis/pull/648#issuecomment-5966274908)
  of the same head, by a reviewer that was not the author, returned
  **ACCEPT** with `[BLOCKER] none`. The
  [merge receipt](https://github.com/ModernNomad-98/Project-Aegis/pull/648#issuecomment-5966307995)
  records the head, checks, review and merge.

  **Accepted with a tracked bound — one non-blocking `[MAJOR]`.** In
  `scripts/ci/check-markdown-links.py:226-249` (`unwrap_links`) the merge is
  quadratic — Θ(L²) in the merged length `L` — for a paragraph containing an
  unclosed `[`; the input is entirely contributor-controlled. Measured by the
  reviewer: a single 1.66 MB paragraph costs **20.9 s** at this head against
  **0.135 s** at `2786841a`, with a fitted exponent of **2.22–2.26**, and
  roughly an **8.4 MB** single paragraph reaches the `gate-guard` job's
  15-minute timeout. The trigger is the unclosed `[`, not size alone: the same
  832 KB shape costs **0.151 s** clean against **4.425 s** with one stray
  bracket. The real corpus is unaffected at this head (`docs/` +0.19 s,
  whole tracked tree +0.46 s), and the checker is **unreachable from every
  automated path** — `git grep check-markdown-links 33c81fda -- .github/`
  returns 0 hits, and only its own self-test module invokes it — so this is
  [MAJOR] and not a BLOCKER. The reviewer recorded that it **becomes REVISE**
  the moment the checker is wired into CI over the tracked tree. The
  reviewer's preferred remedy is folding the open-construct state
  incrementally (O(L) with an O(1) per-line test, behaviour-preserving, so the
  23 pinned tests remain valid evidence); a per-merge cap is acceptable only
  if it is **loud** — a silent cap would recreate the very defect this PR
  removes. A **`[MINOR]`** was also recorded: commit `33c81fda`'s message says
  "49 files gained counted links" where the measured figure is **48** over the
  667 files present at both the base and that head. Neither finding was
  resolved by this merge; both remain owed work.
- **Scope FORBIDDEN:** No other PR, head or failed check was covered. It did
  not change branch protection or the protected path set, and it did not widen
  AEGIS-APR-047. It grants no authority to wire the link checker into CI, to
  leave the quadratic bound unfixed, or to treat either the `[MAJOR]` or the
  `[MINOR]` above as discharged.
- **Evidence:** The owner's decision reached the merge agents **relayed through
  the coordinating agent**, in the Project Aegis conversation on 2026-10-03: it
  is a transcription of the owner's selected option, not a message an agent can
  read directly, and the owner did not type into this register. The register's
  preamble makes that valid source evidence — "Current direct user instructions
  are valid source evidence before transcription and do not need repeated
  consent" — so this entry rests on the owner's instruction and does not claim
  a repository citation of the owner's own text. The repository artifacts that
  independently record the facts above are the
  [independent review](https://github.com/ModernNomad-98/Project-Aegis/pull/648#issuecomment-5966274908)
  and the
  [merge receipt](https://github.com/ModernNomad-98/Project-Aegis/pull/648#issuecomment-5966307995)
  on PR #648. Codex posted no review of this head; the record here is the
  independent human-account review named above.
- **Expiry / use limit:** One merge of PR #648 at the named head; consumed by
  the merge recorded in this entry. No calendar expiry stated.

### AEGIS-APR-104: PR #649 protected gate-guard exception

- **Event:** GRANT.
- **Status at recording:** Consumed by the merge recorded in this entry; no
  remaining use. Recorded after the merge.
- **Date / Grantor:** 2026-10-03 / Peter Nguyen.
- **Reason:** [PR #649](https://github.com/ModernNomad-98/Project-Aegis/pull/649)
  runs the Markdown link-checker's own self-tests from the CI workflow and
  documents the checker. It changes `.github/workflows/validate-skills.yml`, a
  protected path outside AEGIS-APR-047's four BER files — so `gate-guard`
  fails, and merging needs a one-time owner exception for the exact head.
  AEGIS-APR-047 does not reach this PR: its Scope FORBIDDEN keeps
  "workflow/CI files, CODEOWNERS, the validator, … " for
  "separate one-time owner decisions". The red was therefore cured by this
  one-time decision and by nothing standing.
- **Owner decision:** "Grant + merge now" — a choice among dispositions offered
  to the owner on 2026-10-03 in the Project Aegis session. No follow-up was
  attached to this answer.
- **Scope allowed:** One `gate-guard` exception and administrator merge of
  PR #649 at exact head `86725c2aebacf140513fb22f802df0a8c6193998`, merged as
  `25cc0e7a284843075b7da79cfe0c481d18fe059a` at 2026-10-03T06:22:23Z under
  `--match-head-commit`, so the merge would have been refused had the head
  moved. The head changed only `.github/workflows/validate-skills.yml` and the
  unprotected `docs/offline-ci.md` — two paths, +19/−2. At that exact head
  `validate-skills`, `windows-offline-checks`, `tools-tests-linux` and
  `tools-tests-windows` concluded SUCCESS and **`gate-guard` concluded
  FAILURE**; that failure is recorded here as **failed with an authorized
  disposition, not waived and not a pass**. The
  [independent review](https://github.com/ModernNomad-98/Project-Aegis/pull/649#issuecomment-5966277042)
  of the same head, by a reviewer that was not the author, returned **SHIP**
  with `[BLOCKER]` none, `[MAJOR]` none and `[MINOR]` none, and one declined
  `[NIT]` about a follow-up that the review found declared but not recorded.
  The
  [merge receipt](https://github.com/ModernNomad-98/Project-Aegis/pull/649#issuecomment-5966323491)
  records the head, checks, review and merge.

  **An earlier verdict on this PR was voided, and is recorded as voided.** A
  first review at head `e93c4887` returned SHIP. The head then moved to
  `86725c2a` for a required documentation sync, which **voided** that verdict,
  and a **fresh** review was performed at the new head. The exception above
  covers the merge at `86725c2a` only; the voided verdict at `e93c4887` is not
  authority for anything and is recorded here so that no later reader mistakes
  it for a live review of the merged head.
- **Scope FORBIDDEN:** No other PR, head or failed check was covered. It did
  not change branch protection, it removed no path from the protected path
  set, and it did not widen AEGIS-APR-047. It does not cover the voided
  `e93c4887` head, and it does not authorize wiring the link checker over the
  tracked tree — this PR wires only the checker's own self-tests.
- **Evidence:** The owner's decision reached the merge agents **relayed through
  the coordinating agent**, in the Project Aegis conversation on 2026-10-03: it
  is a transcription of the owner's selected option, not a message an agent can
  read directly, and the owner did not type into this register. The register's
  preamble makes that valid source evidence — "Current direct user instructions
  are valid source evidence before transcription and do not need repeated
  consent" — so this entry rests on the owner's instruction and does not claim
  a repository citation of the owner's own text. The repository artifacts that
  independently record the facts above are the
  [independent review](https://github.com/ModernNomad-98/Project-Aegis/pull/649#issuecomment-5966277042),
  which states in its own words that "the earlier verdict at `e93c4887` was
  voided by the head move", and the
  [merge receipt](https://github.com/ModernNomad-98/Project-Aegis/pull/649#issuecomment-5966323491)
  on PR #649, which records the red `gate-guard` as "the authorised
  disposition, not a waived check".
- **Expiry / use limit:** One merge of PR #649 at the named head; consumed by
  the merge recorded in this entry. No calendar expiry stated.

### AEGIS-APR-105: Seven-stage delivery workflow policy

- **Event:** POLICY DECISION. This selects a policy target — the delivery
  workflow this source repository follows — and grants no work of any kind. It
  is not a GRANT.
- **Status at recording:** ACTIVE on this reviewed register merge.
- **Date / Grantor:** 2026-10-03 / Peter Nguyen.
- **Owner decision:** Adopted from the owner's direct instruction. **Quoted
  verbatim, as relayed:**

  > Make the workflow below a permanent, repository-wide rule for ANY coding agent working on the Project Aegis source repository, regardless of model, provider, editor, or harness:
  >
  > PLAN → INDEPENDENT PLAN AUDIT → IMPLEMENT → INDEPENDENT IMPLEMENTATION AUDIT → VALIDATE → FINAL INDEPENDENT PR CODE REVIEW → MERGE
  >
  > The merge must never occur before the required final PR review is posted, accepted, and verified against the exact candidate head.
  >
  > This is a standing instruction until I explicitly supersede it. Record it durably through the repository's established instruction and approval mechanisms. It governs future changes, not just this session.

  Each paragraph above is reproduced on one line so the quotation is not
  sensitive to line wrapping; the stage arrow sequence is exactly as given.
- **Reason:** The stage order and the merge prohibition existed only partially
  and inconsistently across `AGENTS.md`, `CONTRIBUTING.md` and the pull-request
  template, and the parts that existed had no recorded policy home. Recording
  them once, in one canonical page, makes the process auditable and gives every
  later reader the same answer. Registering it here matters because `AGENTS.md`
  sends every agent to this register before requesting consent, and a reader who
  finds the merge exceptions and nothing about the workflow governing them has
  an incomplete picture.
- **Scope allowed (selected policy):** The selected policy target is the
  seven-stage delivery workflow stated in
  [`docs/delivery-workflow.md`](../delivery-workflow.md): the stage order and
  stage separation, each stage's entry and exit evidence, the exact-head
  invalidation rule, the merge prohibition, proportionality, the required
  four-column "Aegis skills used" table, the Role A source-library scope, and the
  enforced-versus-procedural split. The companion decision entry is `D72` in the
  [reconciliation record](../reconciliation/step-0-reconciliation-v4.md) §5. This
  selection changes no permission control, no branch protection, no protected
  path pattern and no harness configuration.
- **Scope FORBIDDEN:** It grants nothing, so **nothing may cite
  `AEGIS-APR-105` as authority for any action.** It authorizes no merge, no
  administrator merge, no `gate-guard` exception and no waiver of any check; it
  does not widen `AEGIS-APR-002` or `AEGIS-APR-047`. It covers no specific pull
  request or head. It does not add `AGENTS.md` or `CLAUDE.md` to the
  protected-path pattern, and it does not decide that open question. It does not
  make the workflow machine-enforced: the page records that the stage order,
  stage separation, exact-head invalidation and proportionality have no
  mechanical control behind them.
- **Evidence:** The owner's instruction was received in the coordinating session
  and **relayed here verbatim through the coordinating agent's brief** for this
  work item, on 2026-10-03. The owner did not type into this register, and the
  quotation above is a transcription of that relay, not the owner's own signed
  text. The register's preamble makes it valid source evidence — "Current direct
  user instructions are valid source evidence before transcription and do not
  need repeated consent" — so this entry rests on the owner's current direct
  instruction and **does not claim a repository citation of the owner's own
  words**.
  An earlier revision of this entry paraphrased that instruction. It was
  replaced by the verbatim quotation above on the same terms the preamble
  permits, and **the replacement is not a rewriting of history**: `AEGIS-APR-105`
  does not exist on `origin/main`, whose highest entry is `AEGIS-APR-104`, so
  this entry has never been merged and has no recorded history to preserve. Once
  merged, any further change to it is an append.
  The repository artifact that independently records the decision is `D72` in the
  [reconciliation record](../reconciliation/step-0-reconciliation-v4.md) §5,
  added by this same change.
- **Expiry / use limit:** No calendar expiry and no one-use limit stated. This is
  a policy selection and stands until explicitly superseded; any replacement
  requires a later recorded owner choice.

### AEGIS-APR-106: PR #661 one-time protected-path decision

- **Event:** GRANT — one-time, bound to one exact head. Not a standing
  exception and not a policy decision.
- **Status at recording:** ACTIVE and **unspent** as recorded. It is consumed by
  the merge of PR #661 at the exact head named below, and by nothing else. It
  authorises no action before that merge and none after it.
- **Date / Grantor:** 2026-10-03 / Peter Nguyen.
- **Reason:** [PR #661](https://github.com/ModernNomad-98/Project-Aegis/pull/661)
  changes `.github/workflows/validate-skills.yml`, a protected path, so
  `gate-guard` fails by construction and the merge needs a one-time owner
  decision for the exact head. The independent implementation audit at Stage D
  returned **ACCEPT** and raised **one merge-gate condition rather than a defect
  in the change**: *"The merge agent must establish it on the record — and
  confirm it from the register, not from a brief — before merging. **The PR
  cannot create that entry for itself.**"* This entry is that record, which is
  why it is a separate change from the pull request it authorises.

  **AEGIS-APR-047 does not reach this merge.** Its title is *"Standing
  gate-guard exception for four BER files"*, and its **Scope FORBIDDEN** keeps
  *"workflow/CI files, CODEOWNERS, the validator, Developer Certificate of
  Origin (DCO) check, guard scripts and tests, requirements, parent import
  files, acceptance machinery and all other BER paths"* for *"separate
  one-time owner decisions"*. The red `gate-guard` was therefore cured by this
  one-time decision and by nothing standing.

  **The register's existing decisions on this workflow are head-scoped to their
  own pull requests**, so none of them is spendable here. `AEGIS-APR-104`
  permitted a merge of *"PR #649 at exact head
  `86725c2aebacf140513fb22f802df0a8c6193998`"* — one head, and that pull
  request. Under this repository's exact-head rule a grant naming one head
  cannot be spent on another, so #649's exception buys nothing for #661.
- **Owner decision:** The owner **selected**, from four presented blocked
  outcomes, the one authorising:

  > One-time owner decision on the protected paths
  > (`.github/workflows/validate-skills.yml` and/or
  > `scripts/ci/check-markdown-links.py`), plus an exclusion mechanism for the
  > 21 deliberately-broken fixture files.

  **This is a transcription of a selection, not a quotation of the owner's own
  words.** The owner chose one of four options put to them; the text above is
  the option's wording, which is why it is introduced as a selection rather than
  as the owner speaking. The register's preamble makes a current direct user
  instruction valid source evidence before transcription — *"Current direct user
  instructions are valid source evidence before transcription and do not need
  repeated consent"* — so this entry rests on that instruction and **does not
  claim a repository citation of the owner's own text**.
- **Scope allowed:** One `gate-guard` exception and a **manual-review merge** of
  PR #661 at exact head `4a9e09dd2db7f4cfb59568f198b206e366f63aea`, and nothing
  else. The head changes **one file**, `.github/workflows/validate-skills.yml`,
  `+49/−0`. **The change uses only the FIRST of the two named paths** — the
  workflow file — so `scripts/ci/check-markdown-links.py` is covered by this
  decision but **unused** by it; the second path is not touched by #661 and this
  grant confers nothing on any other change to it. The `gate-guard` failure at
  that head is recorded here as **failed with an authorised disposition — not
  waived, and not a pass**.

  **`gate_pattern` is unchanged by this head**, which is what keeps the
  exception from outliving the rule it excepts. Measured: the pattern line is
  byte-identical between this base and #661's head, its SHA-256 first-16 is
  **`f22f82ce229d9650`** over the raw line, and `gate_pattern` appears **0**
  times in #661's diff. The pattern itself is neither read from nor cited here —
  it lives in the workflow, and this entry changes no protection pattern.
- **Scope FORBIDDEN:** No other pull request, head, path or failed check is
  covered. It is **not a standing exception**, creates **no precedent**, and
  must not be cited as authority for any later merge. It does **not** change
  `gate_pattern`, branch protection, the protected path set, any required check,
  or any workflow setting. It does **not** reach `scripts/ci/check-markdown-
  links.py` **in this change** — that path is named in the decision and unused
  by it. It does not extend `AEGIS-APR-047`, and it does not revive or widen
  `AEGIS-APR-104`. A moved head voids it: the exception covers the merge at the
  named head only, and a later push to #661's branch leaves this entry
  spendable on nothing.
- **Evidence:** The decision reached this register **relayed through the
  coordinating agent** in the Project Aegis conversation on 2026-10-03, as a
  selection among four options; the owner did not type into this register. The
  evidence splits by where it lives. **Two items are corroborating session
  artifacts, identified by hash so that a holder can verify them; neither is a
  tracked file and neither is reachable from this repository**: the **Stage A
  plan**, whose SHA-256 is
  `44a4a5968c19b47acc6bb98f183f3a1eee6fdf67bb1fc8d1823342df41e859b0` and which
  quotes the grant at its L28; and the **Stage B ACCEPT** on that plan. **One
  item is the repository artifact** — reachable from this repository as a public
  pull-request comment — the
  [**Stage D independent implementation audit**](https://github.com/ModernNomad-98/Project-Aegis/pull/661#issuecomment-5974367602),
  comment `5974367602`, which returns **ACCEPT** at head
  `4a9e09dd2db7f4cfb59568f198b206e366f63aea` bound to `9e6039f5f17d55e3`, states
  that `gate_pattern` is byte-identical, and raises the register condition this
  entry answers. The head, the single changed path and the `+49/−0` figure were
  re-measured from `git` against `origin/main` for this entry rather than taken
  from the brief.
- **Expiry / use limit:** **One use.** It authorises one merge of PR #661 at the
  named head and is consumed by that merge. No calendar expiry is stated; the
  exact-head rule is the operative limit, and it is spent on that head or not at
  all.

### AEGIS-APR-107: Consumption of the PR #661 exception

- **Event:** CONSUMED; target grant AEGIS-APR-106.
- **Status at recording:** AEGIS-APR-106 has no remaining use. That entry's own
  `Status at recording` field reads **ACTIVE and `unspent` as recorded**, which
  was true when it was written and is not true now; **this entry is how the
  register records the later change of state, and it does not rewrite the
  earlier field.**
- **Effective at:** 2026-10-03 23:36:19 UTC.
- **Recorded at / By:** 2026-10-03 / Project Aegis agent, under the delivery
  grant in AEGIS-APR-039.
- **New authority:** None. A later change to a protected path needs its own
  exception.
- **Reason:** The sole exact-head administrator merge completed.

  **The bound head is not the commit now on `main`, and there is no continuity
  between the two SHAs.** AEGIS-APR-106 bound **the act of merging at
  `4a9e09dd2db7f4cfb59568f198b206e366f63aea`** — in its own words *"the exception
  covers the merge at the named head only"* and *"one merge of PR #661 at the
  named head"*. The merge was a **squash**, so the commit that landed on `main`
  is a **different object**: `cc8fd2cb22666a316aa2dca9981aa75d88f78e06`. Measured:
  the two SHAs are distinct commits, and **`4a9e09dd…` is not an ancestor of
  `cc8fd2cb…`** (`git merge-base --is-ancestor` exits non-zero). **`cc8fd2cb…`
  must not be read as "the bound head."** The binding was satisfied by the merge
  **act** at the named head, which `--match-head-commit` guaranteed, and not by
  the identity of the resulting commit. A reader who assumes the merged commit
  *is* the bound head would be misreading this record, and this sentence exists
  to prevent that.
- **Scope FORBIDDEN:** This consumption spends the **first** named path only. The
  second, `scripts/ci/check-markdown-links.py`, remains **covered by
  AEGIS-APR-106 and unused**, exactly as that entry records it, and **neither
  this entry nor that one spends or extends it**. `AEGIS-APR-047` **still does
  not reach workflow/CI files**. Nothing here revives `AEGIS-APR-104`, and
  nothing here authorises any later protected-path change: **the grant is
  exhausted and cannot be spent again.**
- **Evidence:** [PR #661](https://github.com/ModernNomad-98/Project-Aegis/pull/661)
  merged `4a9e09dd2db7f4cfb59568f198b206e366f63aea` as
  `cc8fd2cb22666a316aa2dca9981aa75d88f78e06` at the time above, with the merge
  pinned to that head. The
  [merge receipt](https://github.com/ModernNomad-98/Project-Aegis/pull/661#issuecomment-5974654607),
  comment `5974654607`, records the disposition as *"MERGED (squash) at the exact
  reviewed head, under the one-time authority of AEGIS-APR-106"*. **`gate-guard`
  FAILED on that pull request and the merge proceeded under the one-time
  disposition** — recorded here as **failed with an authorised disposition,
  not waived, and not a pass.**

### AEGIS-APR-109: One-use merge authority over three agent-authored branches

- **Event:** GRANT — one use, three-branch merge authority, held by a designated
  merge agent. It is not a standing merge grant, not a policy decision, and it
  creates no precedent.
- **Status at recording:** ACTIVE and **unspent** as recorded. It authorises the
  three merges named in `Scope allowed` and nothing else, and it ends when all
  three complete or when the owner supersedes it.

  **As recorded, this entry takes effect when it is merged into `main`, not when
  its branch is pushed.** This entry is carried by the **open pull request
  [`ModernNomad-98/Project-Aegis#666`](https://github.com/ModernNomad-98/Project-Aegis/pull/666)**
  against `main`, so the merge path is open but **not complete**: until that pull
  request merges, this text is a draft on a branch, and **no action is covered by
  it**. A reader holding the branch cannot cite it as authority; the register on
  `main` is the record. **No authority audit should read this entry as predating
  its pull request** — the record above is the state of an open, unmerged
  proposal.
- **Date / Grantor:** 2026-10-04 / Peter Nguyen.
- **Reason:** Three agent-authored branches, all based on `3006d0a7`, were each
  waiting on a merge path: `fix/consumer-copy-and-containment`,
  `docs/consumer-copy-worked-example` and `docs/no-cross-skill-delegation`. The
  owner was asked how those merges should proceed and selected a **specific
  agent merge authority** over exactly these three branches, together with the
  security-review carve-out recorded below, rather than a standing grant or a
  per-branch one-time exception. This entry widens no existing entry and restates
  none of them: `AEGIS-APR-100` remains the standing delivery grant for
  separately authorized work, and its own `Scope FORBIDDEN` still withholds a
  protected `gate-guard` waiver — a limit the `docs/no-cross-skill-delegation`
  clause in `Scope FORBIDDEN` below preserves rather than relaxes.

  **The entry ID is derived, not assumed.** The register at this base carries
  `AEGIS-APR-001` through `AEGIS-APR-107` — **107 headings, no gaps and no
  duplicates**, measured by extracting every `### AEGIS-APR-nnn:` heading. The
  headings are **not in strict numeric order** (`087` sits before `085`/`086`),
  so the highest present was taken and the range checked for gaps rather than the
  last heading read. **`AEGIS-APR-108` is reserved by the unmerged
  [PR #665](https://github.com/ModernNomad-98/Project-Aegis/pull/665)** (its
  title records the Stage 4B first-tranche execution grant as `AEGIS-APR-108`;
  the register carries no `108` at this base), so this entry is `109` and the gap
  at `108` is deliberate — it closes when that pull request lands.
- **Owner decisions, recorded as relayed:** The owner's decisions reached this
  register **relayed through the coordinating agent** in the Project Aegis
  conversation on 2026-10-04; **the owner did not type into this register.** Two
  selections were made:

  1. **Merge authority — a specific agent.** From the presented options the owner
     selected **"Grant a specific agent merge authority"**, and designated
     `plan-scrutineer` as the merge agent for the three branches named in
     `Scope allowed`.
  2. **Security-review carve-out.** For these agent-authored branches the owner
     selected **"Carve-out applies"**.

  **These are transcriptions of selections, not quotations of the owner's own
  words.** The owner chose among options put to them, so the wordings above are
  reproduced as they were relayed, not as the owner speaking. The register's
  preamble makes a current direct user instruction valid source evidence before
  transcription — *"Current direct user instructions are valid source evidence
  before transcription and do not need repeated consent"* — so this entry rests
  on that instruction and **does not claim a repository citation of the owner's
  own text.**

  **The designated agent name is a coordinator-session designation, not a
  repository identity.** `plan-scrutineer` has **no repository definition**: a
  search of every tracked file at `3006d0a7` returns **0** occurrences
  (`git grep -F 'plan-scrutineer'` exits 1). It is named here because the owner
  designated it in the coordinating session, and readers should treat it as the
  **object of the grant** — the role the owner designated — rather than as an
  identity resolvable from this repository. This register's convention is to name
  a role rather than a session instance: "the coordinating agent" appears 31
  times at this base and "the merge agent" twice. Where a session instance had to
  be recorded, the Stage 4B first-tranche draft declines to name one and leaves
  it `UNKNOWN` instead — *"no host is named and no agent instance is
  designated"* (`f7c48212`, `docs/approvals/APPROVAL_REGISTER.md:3723-3724`).
  **Consequence, stated because this entry exists to be citable later:** a merge
  performed under this name cannot be attributed from the repository alone, so
  the merge receipt for each branch must carry enough identity to be checkable
  later — the agent instance, the session that designated it, and the exact head
  merged — or the grant's holder stays unresolvable. The name is otherwise
  unresolvable by design here, not by oversight.
- **Scope allowed:** Merge authority over, and only over, these three branches,
  exercised by the designated merge agent `plan-scrutineer`:

  - `fix/consumer-copy-and-containment`
  - `docs/consumer-copy-worked-example`
  - `docs/no-cross-skill-delegation`

  All three are based on `3006d0a7`. Measured for this entry rather than taken
  from the brief: `git merge-base --is-ancestor 3006d0a7 <branch>` exits **0**
  for each of the three.

  **The grant names no head, deliberately.** For each branch the binding to a
  head is established at merge time by condition (a) below, which requires the
  accepted review to name the exact head being merged. `AEGIS-APR-106` records
  the consequence of the alternative: a grant naming one head cannot be spent on
  another, so freezing a head here would void the grant the moment a branch moved
  — and one of these three branches had already moved before this entry was
  written.

  **Measured more precisely than that first wording: two of the three had moved
  before this entry's commit, each for the last time within twelve minutes of
  it** — `docs/consumer-copy-worked-example` (`3d15f7c2` and `0165e06e`, committer
  timestamps 08:48:24 and 08:51:31) and `docs/no-cross-skill-delegation`
  (`29a103e7`, committer timestamp 08:55:47) — against this entry's creating
  commit `623632b9` at 09:03:20. **These are transferred commit timestamps, read
  with `git show -s --format=%cd <sha>` from commits reachable in any fresh clone
  from their branches. They are deliberately not remote-tracking reflog entries:
  a reflog is local to one checkout, expires, and is not transferred, so it is not
  evidence this register may rest on.** From the committer timestamps the two last
  movements are **11 min 49 s and 7 min 33 s** before the creating commit, so the
  twelve-minute statement holds on durable evidence. "One" understated the
  measurement; the argument it supports is unaffected.

  **The anchor in that sentence is named precisely: `623632b9` at 09:03:20 — the
  commit that created this entry, not whichever later commit carries the text a
  reader holds.** A later revision that carried it (`e8081718`, 09:17:02) puts the
  same two movements at **25 min 31 s and 21 min 15 s** before that commit, so the
  twelve-minute statement holds only for `623632b9` and is anchored to it here.
  **The durable facts are the commit identifiers and their committer timestamps
  (`3d15f7c2` 08:48:24, `0165e06e` 08:51:31, `29a103e7` 08:55:47), each reachable
  from its branch in a fresh clone. The reflog entries that first recorded the
  pushes are local to one checkout and expire; this entry does not rest on them
  and does not present them as independently verifiable.** This entry makes no
  general claim about the interval measured to any other revision.

  **Conditional limits — all three must hold for each branch, or that branch is
  not covered:**

  (a) the **final independent review is posted and accepted naming the exact head
  being merged** for that branch;
  (b) **all checks for that head are green** — not only the
  branch-protection-required ones — **or, for `docs/no-cross-skill-delegation`
  only, all checks green EXCEPT `gate-guard`, which remains RED and is disposed
  by the owner's PR-specific exception naming that pull request and that exact
  head.** Such a merge is recorded as **failed with an authorised disposition —
  never green, never waived, and not a pass.** Conditions (a) and (c) still hold
  in full for that branch, and **the other two branches keep the unconditional
  all-green requirement, with no exception available to them.** This restates
  the governing rule rather than relaxing it: `AGENTS.md`:91-96 requires that the
  head's checks are all green — "not only the branch-protection-required ones —
  unless an active owner exception covering that exact head and scope is cited,
  in which case the failed check is recorded as failed with its authorized
  disposition, never as green and never as waived". **Without an owner exception
  covering that exact head and scope, `gate-guard` red means that branch is not
  covered and may not merge** — this clause permits no self-service exception,
  and the exception must name the pull request and the head, so a moved head
  voids it;
  (c) the **required review wait has completed**.

  **A head that moves voids that branch's coverage.** A later push leaves this
  entry spendable on nothing for that branch until a review naming the new head is
  posted and accepted **and that new head satisfies condition (b) as amended above
  — not an unconditional all-green requirement, which would make recovery
  impossible for the one branch whose `gate-guard` is red by construction.** For
  `docs/no-cross-skill-delegation` only, restoring coverage after a later push
  therefore requires **both** a fresh review naming the new head **and a fresh
  owner PR-specific exception naming the new pull request and the new head**,
  disposing the red `gate-guard` and recorded as **failed with an authorised
  disposition — never green, never waived, and not a pass.** A prior exception
  does not carry over: it is void with the head it named, and the fresh exception
  must name the new pull request and the new head. **The other two branches keep
  the unconditional all-green requirement at any new head, with no exception
  available to them.**

  **One merge slot per branch, and each slot is consumed by its first merge.**
  Each named branch may be merged **exactly once** under this grant. **The first
  merge of a branch consumes that branch's coverage immediately** and removes
  that branch from the grant, whether or not the other two branches have merged:
  a later pull request from an already-merged branch cannot satisfy conditions
  (a)–(c) again, and **a second merge of any named branch is forbidden and is
  outside this grant** — the prohibition is on the branch, not only on other
  branch names, so the count of merges this entry can authorise is **three, one
  per branch, and never four.** The grant is fully consumed when all three have
  merged once.

  **Each consumption is recorded, not inferred.** After each merge, a `CONSUMED`
  follow-up entry is appended under a unique ID naming the target grant
  (`AEGIS-APR-109`), the branch merged, the pull request, the exact head merged,
  and the branches still unspent — following the register's own event
  convention: *"Grant entries are immutable. Append later revocation, expiry,
  consumption or supersession events with unique IDs and the affected grant ID;
  do not edit old entries"* (base lines 8-10). This entry is not edited by that
  event; the append is how the later change of state is recorded, exactly as
  `AEGIS-APR-107` records the consumption of `AEGIS-APR-106` without rewriting
  it. The requirement is not optional bookkeeping: `AGENTS.md`:150-153 requires a
  later reader to apply "the recorded human scope and later lifecycle events",
  which is possible only if each slot's end is written down.

  **Security-review carve-out.** For these agent-authored branches the owner
  applied the `CONTRIBUTING.md` carve-out: **no additional mandatory security
  review beyond the ordinary independent review.** The page's own scope is the
  basis: [`CONTRIBUTING.md`](../../CONTRIBUTING.md) attaches that additional
  review to **external** contributions — *"External contributions are reviewed by
  the maintainer before merge; pull requests touching a security-relevant surface
  receive an additional explicit security review"*, and *"An outside contribution
  that touches any listed surface gets the additional security review described
  above, whatever it answers."* **The page does not itself say that
  agent-authored owner-directed work is exempt; the owner's decision is what
  applies the carve-out to these three branches**, and it is recorded here as a
  selection, not as a reading the page already contained. It reaches **only**
  these three branches, is not a standing reading of `CONTRIBUTING.md`, and
  grants nothing to any later change.

  **Read that sentence as scoped to `CONTRIBUTING.md` and to no other page: the
  repository's own instructions file already states the identical limit.**
  [`AGENTS.md`](../../AGENTS.md):71-74 says that a further security review is
  inserted where *"CONTRIBUTING.md's security-relevant-surface list (wider than
  `gate-guard`)"* requires one — *"which is required for OUTSIDE contributions
  only and is not extended to the maintainer's or other agents' own PRs."* That
  scope is not this entry's reading of that page: `AGENTS.md`:75-81 records it as
  the owner's own instruction, stating that it *"is the one the owner recorded on
  2026-09-27"* in the "Security-surface rule" row of
  [`docs/roadmaps/aegis-open-decisions-2026-09-23.md`](../roadmaps/aegis-open-decisions-2026-09-23.md),
  and that *"on the owner's direct instruction this file now states the same
  limit (2026-10-02)"*. So the carve-out for agent-authored PRs is **already
  recorded repository policy carrying the owner's own provenance**, and the
  2026-10-04 selection recorded above applies that standing scope to these three
  branches. **Whether that selection creates the exemption or confirms the scope
  already recorded on 2026-09-27 is not determinable from the repository** — only
  the owner can settle it — and both readings reach the same result for these
  three branches, so this entry claims neither. The question is recorded as an
  open owner decision. This paragraph was added after an independent review
  measured **0** occurrences of `AGENTS.md`, `2026-09-27` and `OUTSIDE
  contributions` in this block as first written; the correction touches no
  earlier entry.
- **Scope FORBIDDEN:** **No branch other than the three named above is covered**,
  at any head, and no later branch may cite this entry as authority. Specific
  prohibitions:

  - **No merge of any other branch**, under any reading of conditions (a)–(c).
  - **No `gate-guard` waiver.** `docs/no-cross-skill-delegation` changes
    `scripts/validate-skills.py` and `scripts/tests/test_validator.py`, and the
    gate pattern in `.github/workflows/validate-skills.yml` matches `scripts/` —
    measured for this entry by applying the workflow's own `gate_pattern` under
    its own bash construct — so `gate-guard` fails on that branch by
    construction. **`AEGIS-APR-047` does not reach it**: that entry's own
    `Scope FORBIDDEN` keeps *"workflow/CI files, CODEOWNERS, the validator,
    Developer Certificate of Origin (DCO) check, guard scripts and tests,
    requirements, parent import files, acceptance machinery and all other BER
    paths"* for *"separate one-time owner decisions"*. That branch may therefore
    **not** be merged while `gate-guard` fails unless the owner grants a
    **PR-specific exception naming that pull request and head**. This entry is
    not that exception, waives no check, and must not be read as a pass: a red
    check stays red, and if such a merge proceeds it is **failed with an
    authorised disposition, not waived**.
  - **No authority to author, review, edit or reopen.** This is merge authority
    only. It does not make `plan-scrutineer` an author or a reviewer of the three
    branches, does not authorise editing them, and does not authorise reopening a
    merged, closed or superseded pull request.
  - **No credential of any kind** may be requested, read, recorded, transmitted
    or stored under this entry.
  - **Nothing on `main` except via the granted merges.** No direct push, no
    force-push, no branch-protection change, no required-check change, no
    auto-merge arming and no other commit to `main` is authorised.
  - It does not widen `AEGIS-APR-100`, `AEGIS-APR-048`, `AEGIS-APR-047` or any
    other entry, and it decides nothing about the open question of what belongs in
    the protected-path set.
- **Evidence:** The decisions reached this register **relayed through the
  coordinating agent** in the Project Aegis conversation on 2026-10-04; **the
  owner did not type into this register**, and the selections above are
  transcriptions of options put to the owner rather than the owner's own signed
  text. Three recorded owner decisions are the source: the merge-authority choice
  **"Grant a specific agent merge authority"**, the merge-agent designation of
  `plan-scrutineer`, and the security-review carve-out **"Carve-out applies"**.
  The register's preamble makes a current direct user instruction valid source
  evidence before transcription — *"Current direct user instructions are valid
  source evidence before transcription and do not need repeated consent"*. **No
  repository artifact records the owner's words for these three decisions**, and
  this entry claims no repository citation of them. Every repository fact asserted
  above was measured against `3006d0a7` for this entry rather than taken from the
  brief: the three branches' ancestry, the register's own ID coverage, the
  absence of `108` at this base, and the `gate_pattern` match on `scripts/`.

  **The grant's direct source is a verbatim instruction typed by the owner.**
  Owner, 2026-10-04, coordinating session, relayed here as a quotation:

  > why are you waiting on me, merge them if they are good

  That sentence is the owner's own wording, not an option label, and it **is the
  direct source** of the merge authority this entry records. The two option
  selections above are the **proposal context** the instruction answered: the
  presented choices and the label the owner selected were **"Grant a specific
  agent merge authority"** (selected; designating `plan-scrutineer`) and
  **"Carve-out applies"** (selected; the security-review carve-out). The wording
  of any option that was **not** selected is not recorded here because this entry
  does not hold it, and writing owner-facing option text that was never
  transcribed is exactly what a register must not do. The preamble makes a
  current direct user instruction valid source evidence before transcription —
  *"Current direct user instructions are valid source evidence before
  transcription and do not need repeated consent"* (base lines 12-13) — so this
  entry now rests on the owner's **verbatim instruction**, quoted with its date
  and source, and not on selection labels alone. The governing rule asks for
  precisely this: `AGENTS.md`:97-100 says the merge agent confirms authority from
  "a register entry on the default branch that passes the preamble test below, or
  the owner's instruction quoted verbatim in its brief with its source; a brief's
  bare assertion of authority is not authority". The two are recorded so neither
  is over-read: **the verbatim instruction authorises the merges; the selections
  record what the owner was choosing between when they said it.** The earlier
  statement in this field stands unchanged — **no repository artifact records the
  owner's words**, and this entry still claims no repository citation of them;
  the quotation above is relayed from the coordinating session, not read out of a
  tracked file.
- **Expiry / use limit:** **One use**, covering the three named merges and
  nothing else. **It is consumed branch by branch: each named branch's coverage
  ends at that branch's first merge (see the consumption rule in `Scope
  allowed`), and the grant is fully consumed when all three have merged once**;
  it also ends earlier if the owner supersedes it. A branch that loses coverage
  under a moved head does not free the grant for any other branch. No calendar
  expiry is stated.
