# Standing Approval Policy — Full Template & Mechanics

Companion to the [Standing Approval and Auto Advance](../SKILL.md). The template below is what
the skill instantiates for a repo; every `<placeholder>` is filled by the
adopting HUMAN, not by an agent. PR means pull request (a proposed branch change
awaiting review), CI means continuous integration (automated checks run on each
push), and `APR-<NNN>` is the adopted policy's approval-register entry number.

## Policy template

```markdown
# Standing Approval Policy — <repo>

Adopted: <YYYY-MM-DD> by <named human/role> (register entry APR-<NNN>)
Reviewed by: human-agent-trust-reviewer pass on <date> (recommended)

## 1. Hard floor (never covered by this policy)

The following require an applicable explicit human decision under
`agent-authorization-matrix`:
- merging to protected branches
- deploys/releases, production data, secrets, git history rewrites
Arming auto-merge is forbidden to agents by default and requires its own
separate, explicit recorded decision before any change to that rule. An
approval to merge does not also approve arming auto-merge.
An agent finding auto-merge already armed treats it as a hazard:
check current authority for changing that PR state, then disarm
(`gh pr merge --disable-auto <n>`) if covered; otherwise flag and stop
the affected merge path for a human decision.

## 2. Standing scope (named steps only)

Within phases approved under §4, the agent may, without re-asking:
- commit to branches matching <branch-pattern>
- push those branches; open PRs against <base>
- monitor CI; fix red checks; re-push
- pull/rebase after an authorized merge
Covered change classes: <classes, e.g. docs-only, qa-test-only, …>
Everything not named here is not covered.

## 3. Merge profile (explicit choice)

Explain before asking for adoption: a pull request (PR) proposes a branch's
changes for review; green checks mean required automated tests passed, not
that a person approved the merge. A protected branch has repository rules for
merging. GitHub auto-merge is a setting that queues a merge when conditions
later pass; selecting a standing profile does not enable that setting.

| Choice | Review time and setup/upkeep | Benefits | Risks and money |
| --- | --- | --- | --- |
| Open PR and stop | A person reviews and merges each PR; little policy setup, but recurring review time. | A human sees each change before merge and can catch context missed by tests. | Delivery may wait for reviewer availability. No added software purchase is required by this policy; CI usage or reviewer cost depends on the repo and is unknown until checked. |
| Merge under an existing explicit grant | First verify and record the grant's scope, limits, and later instructions; maintain those checks for every PR. Less per-PR approval time within that scope. | Approved routine changes can flow sooner. | A mistaken scope match can merge an unwanted change; green tests cannot cover every judgment. CI usage and maintenance effort depend on the repo; check actual pricing and workload rather than promise zero cost. |

Recommend **open PR and stop** when the repository has no applicable merge
grant or human review is required for this change: it keeps the decision with
the person who has authority. Where an applicable active grant already covers
the work and no reviewer or gate block remains, recommend the granted profile
to reduce repeated mechanical approvals; explain the exact grant and why it
fits. A protected-file gate exception needs its own decision. An unanswered choice creates no new approval.

Grant fields (all recorded, never inferred): adoption-valid flag (the grant was
valid when the policy was adopted), armed flag (auto-advance was actually
enabled), grandfathered flag (recorded at adoption when the base grant was
grandfathered rather than newly issued), attestation deadline (the re-attestation
date), review deadline where the register records one (when several deadlines
apply, the SOONEST governs), recorded expiry/use limit (nullable; absence of a
value means no expiry and never an inferred default), and consumption/one-use
semantics exactly as recorded (a one-use grant records its consumed state; a
consumed one-use grant is EXPIRED). Re-attestation happens at the review/
attestation deadline recorded with the grant, whichever is sooner when several
apply, and cannot extend past the recorded expiry/use limit.

**EXPIRED is a TERMINAL state, not a blocked state.** A grant whose recorded
expiry/use limit has passed is EXPIRED in every case; it is checked BEFORE the
precedence table, cannot be revived by re-attestation, and only a NEW grant
restores any permission.

States and precedence: first, if the recorded expiry/use limit has passed, the
grant is EXPIRED (terminal; stop). Otherwise the precedence is BLOCKED >
GRANDFATHERED > ACTIVE (first matching row wins). ACTIVE requires a recorded
future attestation deadline and not blocked. GRANDFATHERED requires
valid-at-adoption, recorded, not blocked, and a recorded attestation deadline
that has not passed. BLOCKED is a halt state for a non-EXPIRED grant, entered by
a reviewer block, a passed attestation deadline, or a transition trigger; an
absent attestation deadline is only the initial/entry classification for a grant
that has no recorded deadline - it is not reachable from ACTIVE or GRANDFATHERED
because both require a recorded deadline. FAIL-SAFE: any NON-EXPIRED grant with
no recorded attestation deadline is BLOCKED regardless of how it entered that
state; the entry classification is not an exemption (a grant whose recorded
expiry has passed is EXPIRED first, never BLOCKED).

Canonical precedence table (EXPIRED checked first; BLOCKED > GRANDFATHERED > ACTIVE):

| Precedence | State | Condition | Auto-advance |
| --- | --- | --- | --- |
| 0 | EXPIRED | recorded expiry/use limit has passed (checked first; terminal) | none; a new grant is required |
| 1 | BLOCKED | reviewer block OR attestation deadline passed OR no recorded attestation deadline for a NON-EXPIRED grant OR transition trigger | disabled; blocking does not itself expire the grant, but the recorded expiry/use limit keeps running; only in-scope human/manual actions remain and no agent-initiated action proceeds |
| 2 | GRANDFATHERED | valid at adoption AND recorded AND not BLOCKED AND a recorded attestation deadline exists and has not passed | preserved only when the register records armed at adoption; otherwise disabled |
| 3 | ACTIVE | not blocked AND a recorded attestation deadline is in the future | enabled only if the register records armed; an unarmed active grant is ACTIVE without auto-advance |

Effects: BLOCKED does not itself expire the grant, but the recorded expiry/use
limit keeps running and still applies; only in-scope human/manual actions remain,
and no agent-initiated action proceeds. The reviewer-block halt is immediate for
every agent-initiated action, states what blocked, and waits for the human;
GRANDFATHERED never bypasses a reviewer block. Preserve consumption/one-use
semantics exactly as recorded: a consumed one-use grant is EXPIRED (terminal)
and is never reset or recharged; re-attestation uses the sooner of the recorded
review and attestation deadlines. EXPIRED has no usable authority
at all: no agent-initiated and no in-scope manual action proceeds on the expired
grant; a new grant is required.

Allowed transitions (EXPIRED is checked first and is terminal; no transition out
of EXPIRED exists):
1. ACTIVE -> BLOCKED on a reviewer block, a passed attestation deadline, or a transition trigger.
2. GRANDFATHERED -> BLOCKED on a reviewer block, a passed attestation deadline, or a transition trigger.
3. ACTIVE or GRANDFATHERED cannot enter BLOCKED on an absent attestation deadline: both require a recorded deadline, so that source condition is impossible and is not listed.
4. BLOCKED -> ACTIVE only on recorded re-attestation with a recorded FUTURE attestation deadline, the block cleared, and a recorded expiry/use limit that has NOT passed (grant not EXPIRED).
5. BLOCKED -> GRANDFATHERED only when the grant is valid-at-adoption, the recorded grandfathered flag is SET, the block has cleared, a recorded attestation deadline exists and has not passed, and the recorded expiry/use limit has NOT passed (grant not EXPIRED).
6. GRANDFATHERED -> ACTIVE on recorded re-attestation/upgrade with a recorded future attestation deadline and a recorded expiry/use limit not passed (grant not EXPIRED).
7. ACTIVE, GRANDFATHERED or BLOCKED -> EXPIRED when the recorded expiry/use limit passes OR when a recorded one-use grant is consumed; EXPIRED is terminal and a new grant is required.
8. Recorded expiry passing is EXPIRED, never a BLOCKED transition; 'expiry' must not be listed as a BLOCKED entry.

[ ] open-PR-and-STOP (DEFAULT without an applicable merge grant)
[ ] opt-in merge under a separate, explicit human decision: <grant ID, source,
    repository, exact action, scope, expiry, later instructions>. This choice
    does not arm GitHub auto-merge. The opt-out phrase (§5) suspends it.
Unchecked = default. The profile choice and its human authority are recorded.
An owner grant in one source repository does not travel with copied skills to
a consumer repository. Recheck the current instruction and grant history.

## 4. Phase-advance rule

Auto-advance continues only into the next phase that is ALREADY named and
individually approved in <plan-of-record doc>. Renamed, reordered,
re-scoped, or inserted phases end auto-advance and return to the human.

## 5. Opt-out phrase

"<EXACT PHRASE>" — said in prompt or PR comment, suspends this policy
immediately, mid-loop, for the session/PR named. Any clear current-session
owner pause or stop instruction does the same without matching these bytes.
The owner instruction always wins.

## 6. Required prompt pattern (per session)

Sessions operating under this policy OPEN with:
> Operating under standing approval APR-<NNN>: <one-line scope>.
> Opt-out: "<EXACT PHRASE>". Merge profile: <profile>.
A session that does not restate the policy cannot claim this template's
auto-advance coverage. An independently effective direct owner grant remains
effective within its own scope and lifecycle.

## 7. Reviewer-block path

A human hold, failing required check that cannot be fixed within scope, or
reviewer objection requiring an owner/scope decision stops auto-advance for
that item until resolved. Ordinary requested changes within active scope are
fixed and re-reviewed before advancing. The agent never argues with or
routes around a reviewer.

## 8. Rationale (do not delete)

The governance elements above — named scope, opt-out, restated approval,
reviewer block, and explicit human authority for merge — separate this policy from
the ungoverned-auto-merge incident (a prior session armed auto-merge; a
security PR merged to main with zero human review — encoded as eval cases in
agent-authorization-matrix). Remove an element and this policy becomes that
incident with better paperwork.
```

## Design notes per element

| Element | Why non-optional (incident tie) |
| --- | --- |
| Named scope | The incident's arming happened because "finish the job" had no named edge; elastic scope is how mechanical loops swallow merge authority. |
| Restated approval (prompt pattern) | Authority that is never restated cannot be consciously renewed or revoked; the arming session believed it was still covered. |
| Opt-out phrase | Fatigue cuts both ways: without a zero-cost brake, humans let the loop run past their comfort; the phrase makes stopping cheaper than tolerating. |
| Reviewer-block path | Green CI is not consent. The incident's merge was green — what was missing was a human, and a block path is how a human re-enters a running loop. |
| Opt-in merge profile | Default-on merge is exactly the incident's mechanism (armed → green → merged, nobody deciding). Making it a deliberate, register-recorded choice restores a decider. |
| Phase-advance bound | Advancing into unapproved work is scope drift with momentum; binding advance to named+approved phases keeps "keep going" inside what was actually blessed. |

## Fatigue evidence worksheet (inputs step 3)

Collect before designing, from recent sessions/PRs:

- approvals granted with < ~30s consideration or identical wording each time
  (candidates for standing coverage);
- approvals with real deliberation, questions back, or occasional "no"
  (load-bearing gates — do NOT thin);
- steps re-asked although inside an already-approved phase (auto-advance
  candidates);
- any past occurrence of the loop stopping on a reviewer block (evidence the
  block path works — or has never been exercised).

## Anti-patterns

- **"And similar routine steps"** in the scope list — elasticity clause;
  delete it.
- **Opt-out that requires justification** — a brake you must argue for is
  not a brake.
- **Restating the policy only in docs** — the pattern is per-SESSION
  restatement; docs are where the policy lives, not proof it is active.
- **Merge profile inherited from a template default** — the whole point is
  that a human selects it, eyes open, recorded.
- **Treating this policy as the authority source** — it is downstream of the
  matrix and any separate applicable human grants. The default matrix floor
  remains when no grant covers the action; later owner constraints also apply.
