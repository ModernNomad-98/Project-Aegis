# Skill-eval harness execution path — owner decision packet

**Status: decision packet only — it grants nothing.** This page presents one open
owner question (section 6) and pre-answers none of it. Every quoted line was read
from the repository at the pinned ref recorded in section 9. Nothing here
authorizes a session, a provider call, a spend, a protected-file change, a
register edit or a merge.

**Reading key.** **Option 1** and **Option 2** are the two options of the
[skill-eval harness authorization request](skill-eval-harness-authorization-request.md).
**BER** is the Behavioral Eval Runner, the shipped offline harness under
`tools/behavioral_eval_runner/`. **WP** means work package, a numbered BER
delivery phase. `UNRUN` means no observation was recorded. A **skill** is a
`SKILL.md` instruction package under `.claude/skills/`; an **eval case** is one
entry in a skill's `evals/evals.json`. **§6/D3** is the repository's
structural-evaluation rule (section 2). `AEGIS-APR` identifies an entry in the
[owner approval register](../approvals/APPROVAL_REGISTER.md), and **BER-DEC**
identifies an entry in the [BER decision log](behavioral-eval-runner-backlog.md).
Register and backlog field lines are quoted below without their leading `- `
list marker; every character after that marker is byte-exact, and the cited
line is named in each case.

## 1. What is already decided — Option 1 (docs-only), delivered

The owner decided this on **2026-09-30**. The authorization request page records
the decision in its "Proposed next decision" section (L115-120):

> **Owner decision, 2026-09-30.** Option 1 was selected, in its **docs-only**
> form: run the procedure on one skill and record the evidence as a page, with
> no code change and no new grant. Option 2 was **not** selected and remains
> unauthorized. The record of what the first run found belongs to the procedure
> page and its evidence page, not here; this page keeps both options so the
> choice and its cost are still visible.

The page's current-reading banner (L24-26) says the same:

> **The owner has since chosen Option 1 in the docs-only form**, and the [procedure](../skill-eval-behavioral-test-procedure.md) it depends on merged in PR #564. Option 2 remains unselected and unauthorized.

The session record carries the scope as a decision row (L115):

> **Skill-eval harness scope** | **Option 1, docs-only** — run the procedure on one skill and record the evidence as a page. No code, **no new grant**. Option 2 (provider-backed execution) was **not** selected and remains unauthorized.

**What Option 1 produced — delivered, verified above the pinned base:**

| Deliverable | Verified evidence at this page's base |
| --- | --- |
| The procedure page (PR #564) | `docs/skill-eval-behavioral-test-procedure.md`; merge `6a37c8d8` ("docs: add the skill-eval behavioral test procedure (#564)"). Page L8-9: "It is a **procedure, not a grant**. It authorizes no session, no provider call and no spend." |
| The run evidence page (PR #568) | `docs/evidence/skill-eval-run-2026-09-30.md`; merge `1bf9340b` ("docs: record the skill-eval behavioural run as evidence (#568)"), named in the session record L38. Run: 3 of 12 `scoped-approval-register` cases, 9 `UNRUN`, per-case observations only (L22-26, L63-72). |
| The step-6 attribution caveat (PR #570) | Procedure page L137-164; merge `a7ac614b` ("docs(skill-eval): add the step-6 attribution caveat the first run exposed (#570)"). |
| Later clarifications of the request page | Blockquotes L33-47 and L93-108, merged in PRs #612, #616 and #618 (the zero-execution claim superseded; the evidence page now committed; the step-6 caveat now in-page). |
| The post-run finding acted on | `scoped-approval-register` `SKILL.md` edited by PR #585, merge `5c806348` ("docs(skills): add the authorized clarifications to two skills (#585)"); the run evidence page L202-223 records it and marks the old figure **UNREPRODUCED** (L215-217). |

**Option 1 is closed and is not re-offered here.** It was selected and delivered
as recorded above; the only choice this page presents is the open one in
section 6. Nothing in this page invites a new decision on Option 1.

## 2. The one open choice

The repository can prove a skill's eval file **exists and parses**, but not that
any case in it is satisfiable. The request page states the rule and the gap
(L51-55):

> A skill's evals are validated **structurally only**. The validator proves
> `evals/evals.json` **exists and parses**; it does not execute a case. The
> [generation standard](../skill-generation-standard.md) §6 and decision D3 require
> evals to be reported as *"present and well-formed, not as passing behavioral
> evaluations."*

An actual defect already crossed that gap once. The request page records it
(L57-63):

> In PR #561 a case in `.claude/skills/scoped-approval-register/evals/evals.json` demanded a
> *write* while its own prompt supplied no quotable grantor wording. The skill
> requires the grantor's words and says to record nothing when scope is
> unresolved, so **an agent obeying the skill failed the case, and an agent
> inventing authority passed it.**

Option 1 wrote the test down as a **manual** procedure, and one run of it
produced the record in section 1. The choice still open is whether to make that
test executable now, in the bounded form the request page calls Option 2; leave
it to the BER backlog's designed automated route (WP-2B-4, then WP-2B-5); or
refuse and close the request. The three options are sections 3, 4 and 5.

**Boundary: this page is the presentation, not the decision.** It creates no
grant, and no option below is authorized by anything written here.

## 3. Option A — authorize preparing the bounded Option 2 execution path now

Option A is **Option 2 of the request page, restated — nothing wider.** An
Option A answer authorizes **preparing** that path — drafting the
implementation proposal — and nothing further: the code, every provider/model
call, the `gate-guard` exception and the cap numbers are separate owner actions
(sections 3b, 3c and 8). Its own scope table (request page L146-152) fixes the
shape:

- Scope: "**One** skill (`scoped-approval-register`), **one run per case**, a stated case ceiling (recommend ≤12 cases)."
- New code: "A live host adapter implementing the existing `HostAdapter` interface, and an assertion-judging path for generic `evals.json` assertions. Existing contracts, canonical hashing and evidence bundles are reused, never duplicated."
- Isolation: "One case per fresh session. The answer key is withheld from the tested session. The judge is a separate call with the transcript and rubric only."
- Spend: "**Owner sets the cap.** The proposal is a per-case and total call ceiling plus a token or dollar ceiling and a stop condition. No cap, no run."
- Evidence: "A sanitized record under `docs/evidence/`, published only after review."
- Claim: "§6 still applies. The output is per-case observations, never a pass rate."

The case ceiling holds at this page's pin: the census in section 9 counts
`scoped-approval-register` at **12 behavior cases**, the same denominator as the
"3 of 12 / 9 `UNRUN`" run record in section 1.

### 3a. The executable seam does not exist yet

At this page's base, the live adapter still refuses every dispatch path. In
`tools/behavioral_eval_runner/adapters/claude_code.py`, `spawn_fresh_session`
raises `LiveDispatchDisabledError` (L58-62) and `stream_events`, `shutdown` and
`emergency_kill` deny through the same helper (L64-71). The helper's message
(L51-56) denies the operation naming `LIVE_DISPATCH_DISABLED` and states that
every live-dispatch path is disabled in WP-2B-1 (BER-DEC-006; 0 dispatches,
0 live sessions, USD $0). Option A would build that seam; it cannot run on what
ships today.

### 3b. The authorities and resolutions Option A needs

The request page says a PR implementing Option 2 "needs **both** of these,
recorded before the branch is cut" (L154-158). **Neither exists today**, and
neither is covered by an existing grant; a third requirement the request page's
two items do not cover is unresolved as well:

1. **A new `gate-guard` exception.** The request page records it (L159-165):

   > 1. **A `gate-guard` exception.** The guard's pattern matches
   >    `tools/behavioral_eval_runner/` and `scripts/`. The standing exception
   >    [AEGIS-APR-047](../approvals/APPROVAL_REGISTER.md#aegis-apr-047-standing-gate-guard-exception-for-four-ber-files)
   >    covers exactly four files — `reporting.py`, `aggregation.py`,
   >    `tests/test_reporting.py`, `tests/test_aggregation.py` — and states that
   >    *"expanding the four-path list needs a new owner decision."* An adapter and
   >    a generic grading path are **outside** that list.

   The register's own text confirms both halves. Its Scope allowed names the
   four eligible paths:

   > The four eligible paths are
   > `tools/behavioral_eval_runner/reporting.py`,
   > `tools/behavioral_eval_runner/aggregation.py`,
   > `tools/behavioral_eval_runner/tests/test_reporting.py` and
   > `tools/behavioral_eval_runner/tests/test_aggregation.py`.

   (APPROVAL_REGISTER L1255-1259). Its Scope FORBIDDEN closes: "Expanding
   the four-path list needs a new owner decision." (L1283-1284). An adapter
   file and a generic grading path are not on that list, so Option A needs a
   **new** owner exception; AEGIS-APR-047 does not stretch to cover them.

2. **New provider/model-call authority.** The request page records it
   (L166-171):

   > 2. **Provider/model-call authority.** The standing delivery grant states its
   >    scope does not authorize provider calls, and
   >    [AEGIS-APR-095](../approvals/APPROVAL_REGISTER.md#aegis-apr-095-consumption-of-the-ber-non-executed-aggregate-correction-grant)
   >    records the previous BER grant consumed on 2026-09-29 with *"New authority:
   >    None."* This is therefore a **new decision**, not a renewal, and it should
   >    not be described as continuing prior work.

   The register's AEGIS-APR-095 entry (L2857-2867) is the consumption event for
   the BER non-executed-aggregate correction grant. It records "**Effective at:**
   2026-09-29 16:31:26 UTC" (L2861) and "**New authority:** None. This merge
   used the standing AEGIS-APR-047 exception, which stays ACTIVE. Any further
   BER report-contract change, including the second tightening the owner did not
   approve, needs a new owner decision." (L2864-2867).

   Two later entries postdate APR-095 and do **not** supply provider-call
   authority either. `AEGIS-APR-127` (register L5414) supersedes the WSL2
   platform decision, and `AEGIS-APR-128` (register L5438-5491) grants one
   **offline** BER R4/R5 Stage A host probe on the WSL2 distro, "ON THE WSL2
   UBUNTU-24.04 DISTRO ONLY" (L5451-5452). Its Scope FORBIDDEN (L5473-5475)
   keeps (L5473-5476) "BER Stage B tests or any model-driven session; real
   baselines or production isolation claims; provider/model calls; credentials in
   chat or source; paid services; production use" forbidden, and it closes: "A separate
   authorization is required before any Stage B model-driven proof."
   (L5480-5481). The matching decision-log entry `BER-DEC-016` records the same
   offline scope: the 2026-10-10 owner "go" authorized the next step after the
   prepared WSL2 distribution, and Stage A is "the proposed offline host probe
   without model or provider calls" (BER backlog L3984-3985).

   So provider-call authority for Option A is a **new** owner decision. It must
   not be described as renewing, continuing or consuming any prior BER grant.

3. **The first-live prerequisites those two items do not cover.** Items 1 and 2
   are necessary but not sufficient for any run. Section 4 records that WP-2B-4
   is **BLOCKED** and "NOT authorized by BER-DEC-007", unblocking only when R1
   (a truthful activation-identifying mechanism, or an owner-approved bounded
   claim), R2/OD-1 (measured calibration and OD-1 ratification through
   WP-2B-3), R4 (per-tool-path confinement proven for the selected live host)
   and R5 (execution-profile observability and isolation proven, or a narrower
   owner-approved claim scope) are resolved, together with the separate
   reviewed and merged WP-2B-4 authorization carrying a live-token budget, a
   live external evidence root, evidence-handling and retention terms, and
   live stop conditions (backlog L1239-1242, L1251-1269; L1270-1272). Before
   any run, each of those must either be resolved or be covered by an explicit
   bounded owner override recorded in that authorization. Absent those
   resolutions or overrides, an Option A answer reaches non-live scaffolding
   only: it authorizes **preparing** the path (section 8), and no run follows
   from it.

### 3c. Costs and boundaries

- **Spend.** No cap, no run: the owner sets the per-case and total call ceiling,
  the token or dollar ceiling and the stop condition (request page L150).
- **Protected path.** The implementation touches
  `tools/behavioral_eval_runner/` — a protected path under the guard — so it
  needs its own PR and the new exception in 3b.1 as separate owner actions;
  this docs page cannot supply either.
- **Claim boundary.** §6/D3 stays in force (section 2). The output would be
  per-case observations, never a pass rate; a case not run stays `UNRUN`.
- **Record.** An Option A grant would be recorded as a new `AEGIS-APR` entry
  and a `BER-DEC` entry carrying the exact wording and scope, in the form the
  request page names (L173-175) — those register and backlog edits need their
  own grants at that time.

## 4. Option B — defer to the designed WP-2B-4 → WP-2B-5 route

Deferral means: no grant now; the automated form is built by the BER backlog's
own route. The backlog's map row states the current status (L41):

> WP-2B-4 is **BLOCKED**; 2B-5, 2B-6 and 2B-7 remain **BACKLOG**.

**WP-2B-4** — "Scenario A Limited-Scope Live Suite (separate first-live phase)" —
records (L1239-1242):

> - **Status:** BLOCKED — separate first-live phase; NOT authorized by BER-DEC-007. Unblocks
>   only when every dependency below exists, including a separate reviewed and merged WP-2B-4
>   authorization with a live-token budget, a live external evidence root, evidence-handling and
>   retention terms, and live stop conditions.

Its dependency list (L1251-1269) is an ALL-of enumeration: WP-2B-1 and WP-2B-2
DONE (satisfied); "WP-2B-3 DONE, which remains UNMET (WP-2B-3 is AUTHORIZED by
merged BER-DEC-008, not DONE)" (L1254-1255); a truthful R1 activation-identifying
mechanism or an owner-approved bounded claim; R2 measured calibration and OD-1
ratification through WP-2B-3; R4 per-tool-path confinement proven for the
selected live host; R5 execution-profile observability and isolation proven or a
narrower owner-approved claim scope; and the separate reviewed and merged WP-2B-4
authorization with its live-token budget, evidence root, evidence terms and stop
conditions.

**WP-2B-5** — "Generic `evals.json` + `trigger-evals.json` execution" — is
"**Status:** BACKLOG" (L1311-1317). Its dependencies (L1339-1341):

> **Dependencies:** WP-2B-4 DONE; the 2B-0 gate resolved to outcome A or an
> owner-approved limitation (broad general-corpus execution precondition, §19); owner
> authorization for WP-2B-5.

and its owner-decision line (L1357-1358):

> **Owner decision required:** Phase authorization; tier selection scope for early runs;
> full-corpus runs remain separately owner-authorized events (D3).

The horizon is long and gated: WP-2B-4 cannot even be authorized while R1,
R2/OD-1, R4 or R5 remains unresolved for the selected live execution profile
(L1270-1272).

### 4a. The cost of waiting — the gap stays manual, dated and current

**Dated figure (the request page's own clarification).** The page's "Later
clarification — 2026-10-01" block (L103-108) states:

> "The wider 1,268 have not been run" above is imprecise: the three cases that did run sit inside that 1,268, so the unexecuted remainder is **1,265**. The paragraph's point is unaffected — 1,265 cases remain unrun, the run measures no coverage, and those three observations are not a result for any skill.

That figure is time-scoped: it is keyed to the corpus as counted at ref
`68b5e7e5`, where the same page records that `census --ref 68b5e7e5` "reports
**195** behavior eval files and **1,268** behavior cases (918 `should_trigger`,
350 `should_not_trigger`), **30** manual-only skills, and **0**
unjudgeable-as-written candidates" (L84-86). It is **not** the current corpus.

**Current figures at this page's pin (command census, re-run for this page).**
See section 9 for the command and the excerpt of its output: **205** shipped skills,
**1,329** behavior cases (969 `should_trigger` + 360 `should_not_trigger`),
1,133 discrimination cases, **2,462** authored single-prompt units, 30
manual-only skills, 203 trigger-eval files, 4,192 assertions. The current
unexecuted remainder is therefore **1,326** = 1,329 − the 3 recorded 2026-09-30
observations. Under either figure the run measures no coverage, and the
run evidence page's own boundary holds (L22-26):

> **It is not an evaluation of the skill's quality, and it measures no coverage.** Three of twelve cases ran. The remaining nine are **`UNRUN`**. Per §6 and D3, evals are reported as *"present and well-formed, not as passing behavioral evaluations"*: this page reports **per-case observations**, never a pass rate, and no case here is described as making the skill "verified".

## 5. Option C — refuse and close the request

The request page states what refusal means (L196-200):

> Refusal is a useful outcome and needs no replacement. The repository keeps the
> structural floor (§6/D3), the defect class that #561 exposed stays findable
> **by hand** through the procedure page, and the reason is on the record so the
> next round does not re-litigate it. WP-2B-4 and WP-2B-5 remain the designed
> route for the automated form.

Cost: no immediate spend and no new grant — but **not unconditionally zero**.
Refusal explicitly retains the by-hand procedure quoted above, so future checks
of this defect class keep consuming maintainer setup and execution time while the
class stays unautomated; that ongoing maintenance and opportunity cost is real,
and this page does not measure its size (**unknown**). Benefit: a clean close on
the record, with the manual procedure and the structural floor unchanged.

## 6. The exact owner question (one, atomic)

**Recommendation: Option B — defer to the designed WP-2B-4 → WP-2B-5 route.**
It is the only one of the three that needs no new authority and no spend: it
leaves the automated form to the route the backlog already designs and gates
(section 4), keeps the manual procedure and the structural floor unchanged, and
closes nothing that cannot be reopened. Option A cannot run on what ships today
(3a); it needs two authorities that do not exist, an owner-set cap and a
protected-path exception (3b), and it would still wait on the same unresolved
first-live prerequisites (3b.3) — so an answer now buys preparation, not a run.
Option C closes the request while the defect class stays unautomated and the
by-hand cost in section 5 continues. **This recommendation is not authority and
pre-answers nothing**: it names the best fit among the constraints recorded
above, and the choice remains the owner's.

> Should the bounded Option 2 execution path (one skill, owner-set spend cap) be
> authorized now — where an Option A answer authorizes preparing that path only
> — left deferred to WP-2B-4/WP-2B-5, or refused and closed?

The three answers correspond to sections 3 (authorize preparing), 4 (defer) and
5 (refuse and close), in that order. The recommendation sits first, in the
packet, per the owner's one-question convention — session record L120, "**One
question at a time**, waiting for the answer, with the recommendation **first**
among the choices" — so it no longer depends on a later coordinator
presentation. Beyond that recommendation, nothing above or below pre-answers
the question.

## 7. Evidence each option needs

- **Option A (authorize preparing):** the owner's cap numbers (per-case and
  total call ceiling, token or dollar ceiling, stop condition) plus both
  authorities in 3b and the resolutions or bounded overrides in 3b.3, recorded
  as a new `AEGIS-APR` entry and a `BER-DEC` entry carrying the exact wording
  and scope (request page L173-175). The implementation PR, the protected-path
  exception and any provider call remain separately gated.
- **Option B (defer):** nothing. The status quo needs no new evidence; the
  backlog rows in section 4 are the current state.
- **Option C (refuse and close):** nothing. Refusal is self-contained (request
  page L196-200).

## 8. What an answer does and does not authorize

- **An Option A answer authorizes only preparing the implementation PR** — the
  bounded Option 2 path is prepared, not run. The code itself, every
  provider/model call, the `gate-guard` exception and the cap numbers are each
  separate owner actions, and no run follows while the first-live prerequisites
  in 3b.3 remain unresolved. No spend begins without the cap numbers; no merge
  is implied.
- **An Option B or Option C answer authorizes no work at all.** Deferral leaves
  the WP-2B-4/5 route exactly as it stands; refusal closes the request with the
  manual procedure and the structural floor intact.
- **No answer authorizes** a corpus-wide or full-library run, a claim of
  coverage, a pass/fail score for the library, a change to any `SKILL.md` or
  authored case, a promotion of any check to required, or any weakening of the
  `UNRUN`, `JUDGE_ERROR` or `PRECHECK_EXCLUDED` semantics.

## 9. Provenance, counts and boundaries

**Pinned ref.** This page was prepared and every quoted line read at
`279338a938168843fabebff12acd30359a0fc414` (= `origin/main` at
2026-10-11 15:38 -07:00, inside this page's recorded 15:38:47 finish minute;
tree `dc3ac8470378be65fd647ba7e6376bc0e9be9f72`) in a clone created for this
deliverable. `AEGIS-APR-047`'s and `AEGIS-APR-128`'s
line numbers above are from that ref; register, backlog, request-page, procedure
and evidence line numbers are all read at the same ref.

**Command census (this page's own run, at the pinned ref) — a relevant excerpt,
not an exact transcript.** Run in the clone at that ref; the block below keeps
the command line and the fields this page relies on, replaces the rest of the
canonical JSON with ellipses, and appends the process exit status on its own
`exit 0` line — that last line is the status this page observed, not output the
command printed:

```text
$ python -B -m tools.behavioral_eval_runner census --repo . --ref 279338a938168843fabebff12acd30359a0fc414 --canonical
... "source_commit":"279338a938168843fabebff12acd30359a0fc414", ... "source_tree":"dc3ac8470378be65fd647ba7e6376bc0e9be9f72", ...
"totals":{"assertions_max":7,"assertions_min":1,"assertions_total":4192,"authored_single_prompt_cases":2462,"behavior_case_types":{"should_not_trigger":360,"should_trigger":969},"behavior_cases":1329,"behavior_eval_files":205,"conversation_suite_paths":["docs/acceptance/scenario-a-runbook.md"],"conversation_suites":1,"discrimination_cases":1133,"distinct_subagent_targets":2,"manual_only_skills":30,"potential_units":2463,"proposed_risk_class_distribution":{"CRITICAL":552,"HIGH":528,"STANDARD":1382},"runtime_classification_totals":{"ambiguous_needs_owner_review":0,"control_plane_only":410,"runtime_required":382},"shipped_skills":205,"should_not_trigger_size_distribution":{"1":884,"2":187,"3":59,"4":3},"subagent_definitions_present":7,"subagent_target_cases":4,"template_excluded":true,"trigger_eval_files":203}
exit 0
```

The same run's per-skill line for this option's one skill reads
`"assertions":35,"behavior_cases":12,"discrimination_cases":5`, `"skill":"scoped-approval-register"`.

**The pinned-historical-baseline observation (O1, with the exit code this run
printed).** The same command with `--verify-baseline` prints:

```text
$ python -B -m tools.behavioral_eval_runner census --repo . --ref 279338a938168843fabebff12acd30359a0fc414 --canonical --verify-baseline
{
  "detail": "pinned corpus differs from the expected baseline; surface to the owner before proceeding: {\"authored_single_prompt_cases\": {\"actual\": 2462, \"expected\": 1740}, \"behavior_cases\": {\"actual\": 1329, \"expected\": 882}, \"behavior_eval_files\": {\"actual\": 205, \"expected\": 184}, \"discrimination_cases\": {\"actual\": 1133, \"expected\": 858}, \"potential_units\": {\"actual\": 2463, \"expected\": 1741}, \"shipped_skills\": {\"actual\": 205, \"expected\": 184}, \"trigger_eval_files\": {\"actual\": 203, \"expected\": 181}}",
  "error": "CensusBaselineMismatchError"
}
exit 2
```

The exit code above is the one this page's own re-run printed: **2**. Plan rev2's
parenthetical "(exit code 1 observed this session)" is not reproduced — the SD-B
rev2 audit flagged that digit — and the code path is visible at this ref:
`tools/behavioral_eval_runner/cli.py` L1403-1408 catches `RunnerError` (the
parent of `CensusBaselineMismatchError`) and returns 2, and
`tools/behavioral_eval_runner/__main__.py` L6 raises `SystemExit(main())`. The
observation stands, with its semantics corrected: the `EXPECTED_PINNED_BASELINE`
constant in `tools/behavioral_eval_runner/census.py` (L154-162) is **not** a
current-count assertion and is **not stale** — it is the deliberately pinned
historical baseline, and its own comment fixes its only consumer: "Expected
pinned baseline (prompt Phase 8). Consumed ONLY by verify_expected_baseline —
never by census computation." (L152-153). The BER README documents the flag the
same way: `--verify-baseline` "checks one pinned historical census (882
behavioral cases and 858 trigger cases), counted from commit `e2f1da0` and set
on 2026-08-13 in commit `72e74af`. A later revision may legitimately have
different counts." (README L84-88). Running that check against this page's
current ref therefore **fails by design** — it compares today's corpus with the
historical pin, and the mismatch above is the expected outcome of that
comparison, not evidence that the constant is stale. The pin holds 184 shipped
skills / 184 behavior eval files / 882 behavior cases / 181 trigger-eval files /
858 discrimination cases / 1,740 authored units / 1 conversation suite / 1,741
potential units, against the actuals above; the check belongs to the historical
revision `e2f1da0`, and this page does not run it there. **No figure in this
page is taken from that constant.** The 1,740 figure also appears in WP-2B-5's
own text as "the design-time count at `e2f1da0`" (L1321-1326); it is not a
current count.

**Boundaries this page does not cross.**

- **Not in the register's open table, and not published as an actionable open
  choice.** The register
  `docs/roadmaps/aegis-open-decisions-2026-09-23.md` lists five open items in
  its "Still open for the owner" table (L229-235): Issue #101 Stage 4B host
  proof; CP-WP-003 and CP-WP-004; private BER candidate labels; the disposable
  Linux VM; and the lighter review path for machine-checked rebuild PRs.
  **None of the five is this decision.** The table's own rule (L226-227) is
  "Each item below needs an owner choice or read before work that depends on it
  can start. Listing an item here grants nothing." This page therefore does not
  claim register authority it does not have; adding a row there would be a
  register edit needing its own owner grant, and this page does not make it.
  Until that row exists in the canonical table, a coordinator enumerating
  pending owner choices from it will not find this decision: this page presents
  the choice for the owner and **does not publish it as an actionable open
  item** in that index. Registering it there — the only step that makes the
  choice enumerable from the canonical set — remains owed to a separately
  governed register edit, and this page neither performs nor pre-claims it.
- **Record gap on an owner answer.** A new `AEGIS-APR` entry and `BER-DEC`
  entry for an Option A grant are approval-register and backlog edits requiring
  their own grants at that time (request page L173-175).
- **Implementation gap.** An Option A implementation PR would touch the
  protected `tools/behavioral_eval_runner/` and needs the new `gate-guard`
  exception and the new provider-call authority as separate owner actions
  (section 3b) — beyond docs-only and beyond this page.

**Stage B checklist items 10 and 12, as applied here.** Item 10 (dated vs
current counts): "1,265" appears in this page only as the request page's dated
2026-10-01 clarification with its 1,268-at-`68b5e7e5` basis (section 4a); the
current corpus figures are the command-run census output above; no figure is
taken from the pinned historical `EXPECTED_PINNED_BASELINE` constant. Item 12
(Option 1 recorded as delivered, not re-offered): section 1 states the
2026-09-30 selection and its delivery (#564/#568/#570; corrections
#612/#616/#618; the post-run finding fixed in #585), and every "Option 1"
occurrence in this page is that delivery record — the only choice presented is
section 6's open one.

### Item timing (owner rule)

| Field | Value |
| --- | --- |
| Item | Decision packet 1 docs deliverable (skill-eval harness execution path) |
| Start timestamp | 2026-10-11 15:31:06 America/Los_Angeles (PDT; 22:31:06 UTC) — runtime-context snapshot at turn 1 |
| ETA at start | 60 minutes (inputs + both dogfood skills read, clone/branch/fetch, census re-run at the pin, byte-verification, deliverable write, six gates, commit, PR + readback, SD-C comment, evidence file) |
| Finish timestamp | 2026-10-11 15:38:47 America/Los_Angeles (PDT; 22:38:47 UTC) — captured immediately before the deliverable's commit |
| Wall time | 7.7 minutes (15:31:06 → 15:38:47 = 7m41s) |
| ETA vs wall | Wall within the 60-minute ETA by 52.3 minutes; active time not measured, so wall is an imperfect comparison |

---

**This page grants nothing and starts nothing. Proposal only.**
