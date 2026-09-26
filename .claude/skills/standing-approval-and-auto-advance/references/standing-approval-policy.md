# Standing Approval Policy — Full Template & Mechanics

Companion to the [Standing Approval and Auto Advance](../SKILL.md). The template below is what
the skill instantiates for a repo; every `<placeholder>` is filled by the
adopting HUMAN, not by an agent.

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
fits. A protected-file gate exception needs its own decision. An unanswered
choice creates no new approval.

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
