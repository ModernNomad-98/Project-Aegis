# APR099-CLOSEOUT-1 — Stage A plan, revision 1

Planner: `/root/apr099_closeout_plan` (Astra, xhigh); Stage A only.
First observed start: 2026-10-09 13:39:46 UTC. Initial active-work estimate:
15–25 minutes. Active time is not separately metered; the completion report
will give measured wall time and the captured SHA-256 of this plan.

**SD-A: COMPLETE.** This is a scratch plan awaiting a different agent's
hash-bound Stage B audit. It is not a register entry, an implementation, a
grant, or a merge disposition.

## 1. One intent and source of authority

Append one factual `CONSUMED` lifecycle event for AEGIS-APR-099 to
`docs/approvals/APPROVAL_REGISTER.md`, if the delivery and missing-event facts
below still hold when implemented. The entry records exhaustion of APR-099's
one-package limit by PR #569; it creates no permission and certifies no new
runtime or provider result.

The current owner instruction is **"Continue with other backlogs"** in this
Project Aegis conversation. The coordinator selected this bounded record gap
and assigned this planner a scratch-only Stage A task. APR-099 itself says
**"One package; consumed at its merge, which a later lifecycle event records.
No calendar expiry stated."** The register preamble requires later consumption
events to be appended under unique IDs while prior entries remain immutable.
This is recording a use-limit fact under the original grant, not an owner
approval of a new grant. The exhausted APR-099 does not authorize new changes
to its old implementation files.

Source role was corroborated in `route002/impl` by the README's `# Project
Aegis` heading and the local catalog, validator and audit-baseline landmarks
required by `AGENTS.md`. The source checkout and isolated clones are this
source library, not a consumer product repository.

## 2. Classification, exact scope and blast radius

Classification from `change-classification-gate`: **docs-only, factual
governance recording**. The allowed change is a non-executable lifecycle
append; it does not alter permission controls, agent instructions, any grant's
scope, or the delivery workflow. If the candidate does any of those things,
stop and return to A/B for reclassification rather than expanding this plan.

- Sole candidate source path: `docs/approvals/APPROVAL_REGISTER.md`.
- Append at EOF only; preserve the complete prior Git blob as an exact byte
  prefix, including its existing final newline. No inline correction or old
  `Status at recording` edit.
- No new decision (`D`) entry is needed: this event records the outcome of an
  existing one-use condition and chooses no policy. If a policy choice emerges,
  it is a different task.
- Do not add this work to a held PR or copy another lane's unmerged register
  append. This task gets its own isolated candidate and stage chain.
- Keep runtime files, skills, baselines, scripts, CI, provider settings,
  approval controls, #682/#683 dispositions and ROWPOLICY unchanged.

Blast radius is the documentary effective-status history for APR-099 only.
The PR template answer is **Yes — `docs/approvals/APPROVAL_REGISTER.md`**, a
listed security-relevant surface in `CONTRIBUTING.md`. This maintainer/agent
task does not by itself meet MG5's outside-contribution clause; the eventual
reviewer must determine applicability from the actual contribution source.
The M workflow's `gate_pattern` at line 528 does not match the register path.
Recheck the actual pattern at the implementation base; there is no guard
exception or guard-edit scope in this plan.

## 3. Pinned evidence and honest limits

Planning main M is `8e11c8f4c2777265e254057ce0fa1e52f0cf03bf`.
The coordinator independently reported a live main read at M. This planner
made **no provider calls or fetches**; all independent checks below were local.
M's register blob is `288232321d751aae47e827d44f912f12b75323fc`.

| Claim | Evidence inspected in this Stage A turn | Result and limit |
| --- | --- | --- |
| The one-use condition already exists | M register lines 3003–3069, APR-099 in full; preamble lines 8–16 and 27–35; `scoped-approval-register/references/register-format.md` effective-status procedure | PROVEN: merge consumes the package even before the recording event exists. |
| No separate APR-099 lifecycle event at M | Read the complete M register into a block parser; inspect every defining heading, event and status; search the entire file for `AEGIS-APR-099`; read full matching APR-086 and APR-099 bodies and the APR-086 correction note | PROVEN at M: 119 defining entry headings, 0 duplicate IDs; 4 exact APR-099 occurrences, confined to APR-086's later note and APR-099. No later entry targets APR-099. This is a full-file lifecycle scan, not reliance on the last few entries. |
| #569's delivered content is the package in question | Source clone: `git show --format= --numstat b9c382c40e2be58123f79bee56fd0f507216576b`; full three-file diff read | PROVEN: register +68/0 adding APR-099; delivery-control README +1/−2; engine.py +2/−3, removing the false transaction clause. No other paths in this immutable commit. |
| PR head and merge commit identify different commits with identical content | Source clone: `git show --no-patch --format='%H%n%P%n%cI%n%s'` for both objects; `git rev-parse '<object>^{tree}'`; `git diff --name-status <head> <merge>` | PROVEN: head `ee27b83e0c16f1327ab80862a78bb3b43c87acd7`, merge `b9c382c40e2be58123f79bee56fd0f507216576b`; both have parent `c97c060d5b92c1fbff5e11b5c26b49134bf60ffd` and tree `26a30340c03769f5f92fa56d78e15a52d0b38e76`; diff empty. |
| The delivery is in M's history | `route002/impl`: `git merge-base --is-ancestor b9c382c40e2be58123f79bee56fd0f507216576b 8e11c8f4c2777265e254057ce0fa1e52f0cf03bf` | PROVEN: exit 0. The source clone lacks M, and its separate attempted ancestry check exited 128; it is not used as ancestry proof. |
| GitHub identifies the merge and its exact time | Coordinator's current-turn relay of `gh api repos/ModernNomad-98/Project-Aegis/pulls/569` | RELAYED, not independently reproduced here: `state=closed`, `merged_at=2026-09-30T17:50:04Z`, merge `b9c382c...`, head `ee27b83...`, base `c97c060...`. Local merge commit's committer time is `2026-09-30T10:50:04-07:00`, consistent with that time but not independently a GitHub `merged_at` proof. C/D must read or validate the retained provider receipt before the final append states the API fact. |
| Current parallel record edits can collide | Local #683 checkout `cifix/preg-e-h1-clone` resolves to `abc49113a83a5fce54ce525912416b79859ba232`; its register has APR-120 and APR-121. ROWPOLICY's `STAGE-C-HANDOFF-draft.md` 2026-10-09 08:49 UTC addendum and coordinator checkpoint were read | PROVEN local artifacts; live open status and current heads are UNVERIFIED by this planner. ROWPOLICY's APR122 is tentative, not allocated; its own handoff requires fresh main plus every open record-touching head. |

Read-method limit: an initial large register output was truncated. It is not
counted as a complete visual read. The later complete-file block/reference
scan above supplies lifecycle coverage, while relevant complete entries and
the preamble were read separately. Stage B must independently challenge this
coverage, including aliases or an indirectly targeted later event.

The source clone supplied the old blobs; `route002/impl` supplied M's graph
and register. The latter's attempt to display the old full diff failed for a
missing old blob; the full local source-clone diff resolved that evidence gap
without fetching. `GIT_NO_LAZY_FETCH=1` was used for later object reads.

Do not repeat APR-099's historical "all three required statements
byte-identical" certification as a newly proven claim. The immutable engine
diff includes grammatical changes around the deletion (`inline:` becomes
`inline in`). This task records use, not a retrospective certification of
every original compliance claim. Historical suites, reviews and CI for #569
were not rerun or audited here, and no such claim is needed in the new event.

## 4. Reconciliation and assumptions

- **IS conflict:** APR-099's historical `ACTIVE` text versus its one-package
  use limit and delivered merge. The limit and delivery evidence govern
  effective status under the register preamble and `scoped-approval-register`;
  the historical status field remains unchanged. The missing event is a
  recording gap, not unused execution authority.
- **IS conflict:** M's apparently next free numeric ID versus unmerged
  record edits. Live main and every relevant open head jointly determine
  collision risk; the local M maximum alone cannot allocate a new ID.
- No new SHOULD decision is proposed. No new, reopened or superseding grant
  is inferred from the owner's backlog instruction.
- Assumptions to refresh: M has not advanced; no later event or parallel PR
  has recorded APR-099 consumption; #683/ROWPOLICY still have the stated
  append shapes. If any is wrong, reassess the event/ID before editing. Never
  append a duplicate fact solely to follow this plan.

## 5. Implementation sequence and proposed event

1. A different Stage B holder audits this exact plan hash. C starts only
   after a posted `SD-B: ACCEPT` for that revision.
2. C obtains a fresh main SHA and the complete register at it, inspects every
   currently open PR touching the register, and reconciles proposed IDs with
   their holders and ROWPOLICY. Record each head/base and its proposed IDs.
   **No ID is assigned or reserved by this plan.** In particular, do not
   take 120/121 from #683 or assume that provisional 122 is free. #683 need
   not merge first merely to do this reconciliation.
3. Reverify #569's `merged_at`, head, merge commit, immutable three-file diff,
   and ancestry to that fresh main. Re-scan the complete register and open
   register diffs for an existing APR-099 event. A provider-read refusal is a
   stop on that dependent evidence; retain the plan without a workaround.
4. In a clean isolated checkout of the fresh main, append one uniquely
   allocated event. Use the actual recording time and recorder; distinguish
   it from the 2026-09-30 effective merge time. Review the exact append before
   committing. The draft shape is below; placeholders are instructions for C
   and must not reach the candidate.

```markdown
### AEGIS-APR-[allocate after reconciliation]: Consumption of the APR-099 guard-documentation correction grant

- **Event:** CONSUMED; target grant AEGIS-APR-099.
- **Status at recording:** AEGIS-APR-099 has no remaining use.
- **Effective at:** 2026-09-30 17:50:04 UTC, the verified merge time of PR #569.
- **Recorded at / By:** [actual UTC append timestamp] / [actual recorder].
- **New authority:** None. This event records the existing one-package limit;
  it does not reopen AEGIS-APR-099 or AEGIS-APR-086, authorize another code or
  documentation change under them, or supply a merge exception.
- **Reason:** AEGIS-APR-099 states that its one package is consumed at merge.
  The correction package merged in PR #569; this later event records that use.
- **Evidence:** [PR #569](https://github.com/ModernNomad-98/Project-Aegis/pull/569)
  merged head `ee27b83e0c16f1327ab80862a78bb3b43c87acd7` as
  `b9c382c40e2be58123f79bee56fd0f507216576b` at the time above. The head and
  merge commit resolve to tree `26a30340c03769f5f92fa56d78e15a52d0b38e76`.
  The delivered diff appended APR-099 and removed the false transaction
  clause from `tools/aegis_delivery_control/engine.py` and its README.
  This records package consumption, not a new certification of historical
  tests or of every claim in the immutable grant.
```

5. Run the checks below. C records the immutable candidate head H, tree and
   base B, exact one-path diff and preservation evidence. Commit with the
   applicable signing/sign-off settings and exact-path staging only; never
   disable signing to bypass a credential/sandbox failure. Publication and
   later stages use their existing scoped task authority, not this plan as
   a new grant. Keep one holder per PR and obtain independent D–G stages.

## 6. Acceptance criteria and validation

| ID | Criterion for the candidate | Verification |
| --- | --- | --- |
| AC1 | Exactly one source path changes, by one EOF lifecycle append; every prior register byte is preserved, with no deletions | `git diff --name-status B H`, `git diff --numstat B H`, `git diff --check B H`; raw `git show B:path` and `git show H:path` byte-prefix equality. Confirm exactly one new defining heading and no unrelated additions. |
| AC2 | One unique event targets APR-099 as CONSUMED, records no remaining use/new authority none, and preserves the original grants | Parse defining IDs and lifecycle targets in the full B/H register; compare old byte prefix; examine the entry and its relationship to APR-086/099 manually. |
| AC3 | Evidence correctly distinguishes original head, merge commit, equal tree, effective time and actual recording time; merge is an ancestor of the fresh base | Retained/reverified #569 provider response and local immutable objects/diff; `git merge-base --is-ancestor <merge> B`; exact timestamp and recorder check. No unsupported historical green/test/compliance claims. |
| AC4 | The event is still missing before this candidate, and the assigned ID does not collide with current main or any open record-touching head/provisional allocation | Fresh complete-register scan plus dated open-PR/head/path/ID inventory and coordinator allocation receipt. Recheck before publication and before merge. A changed main or competing append requires fresh reconciliation. |
| AC5 | The one-file documentation candidate passes mandatory local checks and its links/anchors resolve | `python -B -P scripts/validate-skills.py`; `python -B -P scripts/tests/test_validator.py`; `python -B -P scripts/ci/check-markdown-links.py docs/approvals/APPROVAL_REGISTER.md`; `git diff --check B H`; independent reading of the appended entry. Retain exit codes and tell-tale output. |
| AC6 | C's completion and handoff bind fixed content and preserve all workflow rules | Immutable 40-character H, resolved tree and B; exact changed/not-touched lists; preservation inventory; own skills rows; next-holder instruction; `SD-C` disposition. No merge-gate rule or old record is changed. |

**Head-verifiability declaration:** AC1–AC6 are all verifiable at the proposed
immutable implementation head using its retained fresh evidence. None is
predeclared UNRUN or waived for D. If a needed object, API fact, check or
collision inventory cannot be obtained, C remains incomplete or D returns
REVISE; do not relabel the criterion out of scope.

Actual future GitHub checks, automated-review evidence, F's published verdict
and a merge receipt cannot exist at Stage A. They are downstream workflow
gates, not substitutes for these candidate criteria. No new tests are planned
for a documentary append. E selects proportionate validation under the
repository's workflow, executes it as a separate stage and honestly lists
UNRUN items; such a list is not proof that the owner's green merge condition
is met. The original #569 tests are intentionally not rerun as this task's
validation.

## 7. A–G handoffs and delivery stops

| Stage | Separate holder's task and bound evidence |
| --- | --- |
| A | This scratch plan, classification and AC1–AC6; captured file SHA-256 in completion message. |
| B | Astra xhigh; independently inspect exact plan text, immutable delivery evidence, coverage of the complete lifecycle history and the proposed ID reconciliation; post `SD-B` with the plan hash. |
| C | Sol high; accepted plan only, one isolated writer, fresh base/ID/evidence, one-file append, mandatory local checks; provide H/tree/B and `SD-C`. |
| D | Astra xhigh; independently check AC1–AC6 one by one as MET/NOT MET/UNRUN at H, plus preservation inventory; post `SD-D` at H. |
| E | Separate validation holder; use classification and current repository procedure, run checks at H and retain honest output/UNRUN disposition under `SD-E`. |
| F | Astra xhigh; final independent PR review at H, source-check each exact self-authored skills row, security answer and reconciliation witness, bind completed metadata hash, and post `SD-F`. |
| G | Separate authorized merge holder; freshly derive canonical MG1–MG5 at H and the current merge tree, retain the MG-keyed receipt, then verify the published merge if performed. |

The canonical workflow is `docs/delivery-workflow.md` at the actual candidate
base. Its seven-stage independence, head invalidation and bound-field
invalidation rules remain binding. The owner's latest condition is quoted
verbatim: **"for merge, once local and github checks are green, approved for
merge."** APR-100 and the current scoped standing instructions govern
delivery mechanics for separately authorized work; no old one-use grant is
reused. Unknown provider-check applicability is unresolved, not green. No
automated-review trigger is authorized by this plan.

Stop dependent work if the record is already present, the historical delivery
does not match, an ID collision cannot be reconciled, the append changes old
bytes, the path set grows, a local check fails, signing/publishing is denied,
or any mandatory stage/merge evidence is missing. Reconcile a mechanical
collision within scope; return to A/B for substantive changes. Never bypass
an automatic approval denial through another provider, shell or agent.

## 8. Skills, invocation evidence and continuation

Skills actually read and applied from `.claude/skills/` in the verified source
clone (none MANUAL-ONLY):

| Skill | Stage / agent | How applied | Result / evidence |
| --- | --- | --- | --- |
| [source-of-truth-reconciler](https://github.com/ModernNomad-98/Project-Aegis/blob/8e11c8f4c2777265e254057ce0fa1e52f0cf03bf/.claude/skills/source-of-truth-reconciler/SKILL.md) | A / /root/apr099_closeout_plan, revision 1 | Reconciled historical ACTIVE wording against the one-use limit and delivered merge; separated local immutable evidence from relayed live facts. | Sections 3–4 record the evidence winner and remaining freshness limits; original text is preserved. |
| [scoped-approval-register](https://github.com/ModernNomad-98/Project-Aegis/blob/8e11c8f4c2777265e254057ce0fa1e52f0cf03bf/.claude/skills/scoped-approval-register/SKILL.md) | A / /root/apr099_closeout_plan, revision 1 | Read its lifecycle template/effective-status reference; traced register history and planned a unique EOF event with separate effective and recording times. | Sections 3, 5–6 define factual consumption, no new authority, byte preservation and ID reconciliation; no source entry was written. |
| [change-classification-gate](https://github.com/ModernNomad-98/Project-Aegis/blob/8e11c8f4c2777265e254057ce0fa1e52f0cf03bf/.claude/skills/change-classification-gate/SKILL.md) | A / /root/apr099_closeout_plan, revision 1 | Inspected the sole target, security surface and gate pattern; locked documentary scope and required validation. | Section 2 classifies docs-only factual recording; AC1–AC6 and the reclassification stop prohibit grant or instruction changes. |

No installed skill owns writing a single change's Stage A plan; that part is
procedurally enforced by the repository workflow. The rows above describe
supporting procedures actually used. The authorized publisher may copy these
exact self-authored rows with this plan's captured digest; do not invent later
holders' rows or omit their limitations.

Changed by Stage A: this one scratch plan only.
Intentionally not done: source edits, candidate/ID allocation, test execution,
provider calls/fetches, commit, push, PR publication or merge. No source
repository, Git configuration, dirty-root artifact or existing PR was edited.

Continuation: hand this captured plan and its SHA-256 to a different Astra
xhigh Stage B agent. C needs B's exact-revision ACCEPT and the fresh evidence
and collision reconciliation in section 5; this plan allocates no ID and
does not itself release a held lane.
