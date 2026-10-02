# Skill-eval harness authorization request

**Reading key.** A **skill** is a `SKILL.md` instruction package under
`.claude/skills/`. An **eval case** is one entry in a skill's
`evals/evals.json`. A **fresh session** is an agent instance with no prior
conversation and no access to the answer key. The **Behavioral Eval Runner
(BER)** is the shipped offline harness under `tools/behavioral_eval_runner/`.
A **host adapter** is BER's boundary object for starting a session on a real
execution host. **`gate-guard`** is the continuous-integration check that fails
when a pull request (PR) changes a protected file path; `AEGIS-APR` identifies
an entry in the [owner approval register](../approvals/APPROVAL_REGISTER.md).
A **work package (WP)** is a numbered BER delivery phase. `UNRUN` means no
observation was recorded. Decision identifiers such as **BER-DEC-008** name
entries in the [BER decision log](behavioral-eval-runner-backlog.md).

> **Current reading, checked 2026-09-30 against `6a37c8d8`:** This is an
> **authorization request**, not a grant. It authorizes nothing. It asks the
> owner for a decision the repository already gates, and it presents two
> options at different costs. The standing delivery grants
> ([AEGIS-APR-039](../approvals/APPROVAL_REGISTER.md#aegis-apr-039-reaffirmation-of-ongoing-backlog-delivery-approval))
> authorize writing, committing and merging this page; they do **not**
> authorize a provider call, a live session or a protected-file change.
>
> **The owner has since chosen Option 1 in the docs-only form**, and the
> [procedure](../skill-eval-behavioral-test-procedure.md) it depends on
> merged in PR #564. Option 2 remains unselected and unauthorized. That run's
> findings are **not** restated here: a run's results belong to its own
> evidence page, and **no such page is committed yet**, so any claim about
> what the run found is currently an unattributed assertion. The procedure
> page's step 6 is known to need a caveat, disclosed in PR #564's review
> record.

> **Later clarification — 2026-10-01.** The evidence page this blockquote
> said was not yet committed **is now committed**: it is
> [the skill-eval run of 2026-09-30](../evidence/skill-eval-run-2026-09-30.md),
> added in PR #568. The claim "**no such page is committed yet**" is
> therefore superseded, and a run's results now have an attributable record.
> Nothing above is changed, and no finding of that run is restated here.
> This records a fact; it grants nothing and alters no authorization.

## The gap this asks about

A skill's evals are validated **structurally only**. The validator proves
`evals/evals.json` **exists and parses**; it does not execute a case. The
[generation standard](../skill-generation-standard.md) §6 and decision D3 require
evals to be reported as *"present and well-formed, not as passing behavioral
evaluations."*

That leaves a real blind spot, and it has already cost one defect. In PR #561 a
case in `.claude/skills/scoped-approval-register/evals/evals.json` demanded a
*write* while its own prompt supplied no quotable grantor wording. The skill
requires the grantor's words and says to record nothing when scope is
unresolved, so **an agent obeying the skill failed the case, and an agent
inventing authority passed it.** It was the only defect that round that reading
could not have found; it was found by **running the skill**.

The
[skill-eval behavioral test procedure](../skill-eval-behavioral-test-procedure.md)
now writes that test down, so a maintainer can repeat it by hand. This request
is the step after that: making it **executable without a person driving both
sides**.

## Why the shipped runner does not already do this

Measured at `68b5e7e5`:

| Component | State | Consequence |
| --- | --- | --- |
| `adapters/claude_code.py` | every path raises `LiveDispatchDisabledError` (`LIVE_DISPATCH_DISABLED`) | no fresh session can be spawned |
| `adapters/base.py` | interface only — `spawn_fresh_session` is `NotImplementedError` | the boundary exists; no host backs it |
| `graders/` | Scenario A controls only (`CONTROL_ID = "SCENARIO_A_CONTROL_*"`) | nothing grades a generic `evals.json` assertion |
| `census.py` | reads and counts `evals/evals.json` offline | inventory is built; execution is not |
| generic corpus execution | backlog **WP-2B-5**, depends on WP-2B-4 DONE | not started |
| Scenario A live suite | **WP-2B-4**, BLOCKED on R1/R2/R4/R5, OD-1 and a live budget | first-live phase, not authorized |

`census --ref 68b5e7e5` reports **195** behavior eval files and **1,268**
behavior cases (918 `should_trigger`, 350 `should_not_trigger`), **30**
manual-only skills, and **0** unjudgeable-as-written candidates. None of those
cases has ever been executed.

So this is not a request to relax the runner's gates. It is a request to decide
**whether to build the execution path the gates reserve**, at a scope small
enough to be honest.

## Proposed next decision

Choose **one** of the two options below. Both are deliberately narrow: **one
skill, one run per case**, the skill whose evals already produced a defect.

> **Owner decision, 2026-09-30.** Option 1 was selected, in its **docs-only**
> form: run the procedure on one skill and record the evidence as a page, with
> no code change and no new grant. Option 2 was **not** selected and remains
> unauthorized. The record of what the first run found belongs to the procedure
> page and its evidence page, not here; this page keeps both options so the
> choice and its cost are still visible.

### Option 1 — offline, human-graded ($0) — **SELECTED (docs-only form)**

No provider call, no fresh live session, no new spend. The procedure in
[skill-eval behavioral test procedure](../skill-eval-behavioral-test-procedure.md)
is executed by a maintainer or an authorized agent, and this option adds only
**the record and the checks**: a schema for the observation, a runnable
recording that a reviewer can re-read, and an explicit `UNRUN` default.

| Boundary | Proposed scope |
| --- | --- |
| Spend | **$0**. No provider, model or network call. |
| New code | One record shape and its validator; no host adapter, no session spawn. |
| Claim | None. Cases not run stay `UNRUN`; §6's wording is preserved verbatim. |
| Value | Turns the #561 method into a repeatable artifact with real evidence. |
| Ceiling | Does **not** automate execution; a person still runs both sides. |

### Option 2 — provider-backed execution (owner-set budget)

Adds the missing seam for real: a live host adapter and a generic grading path,
bounded to one skill. This is the option that actually removes the human from
the loop.

| Boundary | Proposed scope |
| --- | --- |
| Repository and base | `ModernNomad-98/Project-Aegis`, Role A; branch cut from the grant's own merge commit. |
| Scope | **One** skill (`scoped-approval-register`), **one run per case**, a stated case ceiling (recommend ≤12 cases). |
| New code | A live host adapter implementing the existing `HostAdapter` interface, and an assertion-judging path for generic `evals.json` assertions. Existing contracts, canonical hashing and evidence bundles are reused, never duplicated. |
| Isolation | One case per fresh session. The answer key is withheld from the tested session. The judge is a separate call with the transcript and rubric only. |
| Spend | **Owner sets the cap.** The proposal is a per-case and total call ceiling plus a token or dollar ceiling and a stop condition. No cap, no run. |
| Evidence | A sanitized record under `docs/evidence/`, published only after review. |
| Claim | §6 still applies. The output is per-case observations, never a pass rate. |

## The two authorities this needs

A PR implementing **Option 2** needs **both** of these, recorded before the
branch is cut:

1. **A `gate-guard` exception.** The guard's pattern matches
   `tools/behavioral_eval_runner/` and `scripts/`. The standing exception
   [AEGIS-APR-047](../approvals/APPROVAL_REGISTER.md#aegis-apr-047-standing-gate-guard-exception-for-four-ber-files)
   covers exactly four files — `reporting.py`, `aggregation.py`,
   `tests/test_reporting.py`, `tests/test_aggregation.py` — and states that
   *"expanding the four-path list needs a new owner decision."* An adapter and
   a generic grading path are **outside** that list.
2. **Provider/model-call authority.** The standing delivery grant states its
   scope does not authorize provider calls, and
   [AEGIS-APR-095](../approvals/APPROVAL_REGISTER.md#aegis-apr-095-consumption-of-the-ber-non-executed-aggregate-correction-grant)
   records the previous BER grant consumed on 2026-09-29 with *"New authority:
   None."* This is therefore a **new decision**, not a renewal, and it should
   not be described as continuing prior work.

A later `AEGIS-APR` entry should carry the exact wording, and a `BER-DEC` entry
should record the scope, in the form used by
[APR-085](../approvals/APPROVAL_REGISTER.md#aegis-apr-085-ber-non-executed-aggregate-correction).

## Scope FORBIDDEN (proposed)

- No change to any `SKILL.md`, to any authored eval assertion, or to any case's
  prompt. The runner reports; it never rewrites a case to make it pass. (If a
  run proves a case unsatisfiable, that is a **finding**, and repairing it is
  ordinary [AEGIS-APR-051](../approvals/APPROVAL_REGISTER.md#aegis-apr-051-eval-file-maintenance-of-delivered-skills-is-backlog-delivery)
  eval maintenance in its own PR.)
- No corpus-wide or full-library run; no claim of coverage.
- No promotion of any check to required; no change to branch protection, the
  validator or the guard.
- No weakening of any BER gate, and no relaxation of the `UNRUN`,
  `JUDGE_ERROR` or `PRECHECK_EXCLUDED` semantics.
- No real host proof, no VM work, no private or holdout input, no credential
  beyond the single authorized provider path.
- No pass/fail score for the library, and no wording that describes an
  unexecuted case as passing.

## If this is refused

Refusal is a useful outcome and needs no replacement. The repository keeps the
structural floor (§6/D3), the defect class that #561 exposed stays findable
**by hand** through the procedure page, and the reason is on the record so the
next round does not re-litigate it. WP-2B-4 and WP-2B-5 remain the designed
route for the automated form.

## Provenance

Prepared 2026-09-30 from public `main` at
`68b5e7e5ea67b8d489315ea7dd8492cb096ad9b0`. Counts were produced by
`python -B -m tools.behavioral_eval_runner census --repo . --ref 68b5e7e5ea67b8d489315ea7dd8492cb096ad9b0 --canonical`
and by reading
`tools/behavioral_eval_runner/adapters/claude_code.py`, `graders/__init__.py`
and the [BER backlog](behavioral-eval-runner-backlog.md) work-package register.
**Proposal only — this page grants nothing and starts nothing.**
