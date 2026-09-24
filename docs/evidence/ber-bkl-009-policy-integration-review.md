# BER-BKL-009 synthetic policy integration review

## Scope and source

This record covers one opt-in, offline, synthetic-only implementation under
[BER-DEC-013](../roadmaps/behavioral-eval-runner-backlog.md#ber-dec-013-bounded-synthetic-evidence-policy-integration--owner-approved)
and [APR-023](../approvals/APPROVAL_REGISTER.md#aegis-apr-023-bounded-synthetic-evidence-policy-integration).
The reviewed governance [PR #255](https://github.com/ModernNomad-98/Project-Aegis/pull/255)
merged on 2026-09-24 at
`0318b1ecde3ebf5f34bb32f8793efc37b574af39`; its tree is
`d35f4a6af25e4d5dd29641e0fa271bf782b1e7df`. The implementation branch
`feat/ber-bkl009-policy-integration` was created directly from that merge.
The tested code-and-runbook revision is the signed commit
`f0ef7bfae43a3f486288d0678efa5eae6b03e3b1` (tree
`081404ef88a6e507c8ce0c4e464797d20131655c`). The signed evidence-only
follow-up is PR #257 head `7176009113fa208a1b2e816d90d7f929805e93ae`.
It merged on 2026-09-24 at 22:04:09 UTC as
`53351b3fac3d75cbbc23341cc96dbeadc1e116ee` under the owner's one-time
protected-guard exception, recorded in APR-025 and consumed by APR-026.
The grant caps work at 16 active implementation hours, 1,500 added code/test
lines and $0 task-controlled external spend. The implementation package is
complete; selected-host and production-policy gates remain open.

## Changed-path and cap review

The exact permitted paths are listed in the [approved scope](../roadmaps/ber-bkl-009-policy-scope-amendment-proposal.md).
The signed code-and-runbook commit changes nine of them: `evidence.py`,
`evidence_policy.py`, new `evidence_policy_preflight.py`, their three named
test files, the runner `README.md`, the operator runbook, and the BER backlog.
This sanitized evidence review is the tenth path. `git show --numstat` for the
six code/test paths records **404 added code/test lines** (83 + 4 + 108 + 7 +
97 + 105), below the 1,500-line cap. A changed path outside these ten,
cap overrun,
published schema or accepted-byte change is a stop for a new owner decision.

| Check | Observed result |
| --- | --- |
| Tested code-and-runbook revision | Signed `f0ef7bfae43a3f486288d0678efa5eae6b03e3b1`, tree `081404ef88a6e507c8ce0c4e464797d20131655c`; signed evidence-only PR head `7176009113fa208a1b2e816d90d7f929805e93ae` |
| Changed paths compared with exact grant base | Ten named paths including this review; no tracked out-of-scope path |
| Added code/test lines | 404 added, 4 removed; under 1,500 added-line cap |
| Active implementation time and external spend | Exact active/review/CI split unavailable; implementation and tests completed between 18:59:41 and 19:19:43 UTC with parallel agents and a 20m02s elapsed interval. No provider, host or private-data operation; $0 task-controlled external spend. |
| Focused policy, evidence and synthetic-preflight tests | `python -B -m unittest tools.behavioral_eval_runner.tests.test_evidence_policy tools.behavioral_eval_runner.tests.test_evidence tools.behavioral_eval_runner.tests.test_evidence_policy_preflight -q`: 66 tests, 2 expected platform skips, exit 0 |
| Full offline Behavioral Eval Runner suite | Repository-owner context: `python -B -m unittest discover -s tools/behavioral_eval_runner/tests -p 'test_*.py' -q`: 1,062 tests, 14 expected skips, exit 0, 289.533s. A prior sandbox-user run had 12 environment errors from Git dubious ownership and synthetic process-kill restrictions; the owner-context rerun is the acceptance result. |
| Skill validator and whitespace/path checks | `python scripts/validate-skills.py`: 185 valid skills, zero warnings; `git diff --check` and staged diff check clean; exact ten-path list checked. |
| Independent architecture/security review | Two read-only reviewers reproduced three initial low-level handoff/policy-lookalike bypasses; fixes now fail before mutation and both reviewers accepted the corrected code. A separate full-page reviewer accepted the corrected README/runbook/backlog and this sanitized record. |
| Exact-head Linux and Windows GitHub Actions | Both SUCCESS at `7176009113fa208a1b2e816d90d7f929805e93ae` in [run 36047710329](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/36047710329). The protected `gate-guard` failed on changed runner paths. The owner approved the PR-specific exception and administrator merge; no other check failed. |

## Required behavioral evidence

The accepted test review covers: policy-bound input and report
classifications cannot fall back to implicit metadata; first-evidence time and
one 30-day complete-bundle review date stay bound across both stages and the
detached marker; legacy evidence bytes and per-artifact `expiration_at`
semantics remain unchanged; missing, altered, expired or incomplete chains
fail closed when their references or bytes conflict with the established
hash chain, without removing evidence; and synthetic host-fact preflight says
`STOP` for missing or contradictory facts and `SIMULATION_ONLY` for any
passing supplied facts. A passing synthetic result is no selected-host proof.
Hash agreement cannot establish authenticity against a coordinated rewrite
of every bundle file; BER-BKL-010 retains that separate owner decision.

## Residual gates

BER-BKL-009 remains partially delivered. Real-host ownership and access
control, inheritance, encryption and recovery-key custody, actual privacy
review and redaction, production runtime binding, and marker-gated operator
cleanup need separate source/host choices, owner authority and independent
evidence. The offline package authorizes no credential, private label,
provider call, live run, publication clearance or evidence deletion.
