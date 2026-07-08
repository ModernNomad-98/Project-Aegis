# Standing Approval Policy — Full Template & Mechanics

Companion to `standing-approval-and-auto-advance`. The template below is what
the skill instantiates for a repo; every `<placeholder>` is filled by the
adopting HUMAN, not by an agent.

## Policy template

```markdown
# Standing Approval Policy — <repo>

Adopted: <YYYY-MM-DD> by <named human/role> (register entry APR-<NNN>)
Reviewed by: human-agent-trust-reviewer pass on <date> (recommended)

## 1. Hard floor (never covered by this policy)

The following remain human-only regardless of anything below, per
agent-authorization-matrix:
- merging to protected branches
- arming auto-merge (any strategy)
- deploys/releases, production data, secrets, git history rewrites
An agent finding auto-merge already armed treats it as a hazard:
disarm (`gh pr merge --disable-auto <n>`) and flag — never let it ride.

## 2. Standing scope (named steps only)

Within phases approved under §4, the agent may, without re-asking:
- commit to branches matching <branch-pattern>
- push those branches; open PRs against <base>
- monitor CI; fix red checks; re-push
- pull/rebase after a HUMAN merges
Covered change classes: <classes, e.g. docs-only, qa-test-only, …>
Everything not named here is not covered.

## 3. Merge profile (explicit choice)

[ ] open-PR-and-STOP (DEFAULT — the agent's terminal action is an open PR)
[ ] opt-in autonomous merge: ONLY lawful if the authorization matrix was
    human-amended to delegate a NAMED non-protected surface; scope: <surface>;
    opt-out phrase (§5) suspends it instantly.
Unchecked = default. The profile choice is itself a register entry.

## 4. Phase-advance rule

Auto-advance continues only into the next phase that is ALREADY named and
individually approved in <plan-of-record doc>. Renamed, reordered,
re-scoped, or inserted phases end auto-advance and return to the human.

## 5. Opt-out phrase

"<EXACT PHRASE>" — said in prompt or PR comment, suspends this policy
immediately, mid-loop, for the session/PR named. Always wins.

## 6. Required prompt pattern (per session)

Sessions operating under this policy OPEN with:
> Operating under standing approval APR-<NNN>: <one-line scope>.
> Opt-out: "<EXACT PHRASE>". Merge profile: <profile>.
A session that does not restate the policy does not enjoy it.

## 7. Reviewer-block path

Any of: change-requested review, human comment asking to hold, failing
required check the agent cannot fix inside scope, or ANY reviewer objection
→ the loop STOPS for that item, states what blocked it, and waits.
The agent never re-requests review, argues, or routes around a reviewer.

## 8. Rationale (do not delete)

The governance elements above — named scope, opt-out, restated approval,
reviewer-block, human-only merge floor — are what separate this policy from
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
  matrix; on any conflict the matrix wins and the policy is defective.
