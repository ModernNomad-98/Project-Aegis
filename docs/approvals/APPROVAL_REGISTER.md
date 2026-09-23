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
