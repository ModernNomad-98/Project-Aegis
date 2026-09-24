---
name: standing-approval-and-auto-advance
description: 'MANUAL-ONLY; never auto-invoke. Design the governed approval-fatigue layer: documented standing approval for named delivery steps, phase advance only through already-approved phases, per-session restatement, an opt-out phrase, and reviewer blocks. Protected-branch merge remains approval-required; an applicable explicit, active, scoped human grant can satisfy that requirement without another request. Never infer merge authority from green checks or this skill. Arming auto-merge remains forbidden to agents by default. Merge-after-green is never the default template. Use when repetitive mechanical approvals erode real gates. Do not use to record one grant (scoped-approval-register), define authority floors (agent-authorization-matrix), or stress-test approval experience (human-agent-trust-reviewer).'
disable-model-invocation: true
---

# Standing Approval & Auto-Advance

## Purpose

Codify what does NOT need re-approval — safely. Approval fatigue is a real
attack on governance: when every mechanical push and PR re-asks permission,
humans learn to rubber-stamp, and the gates that matter die with the ones
that don't. This skill designs the governed inverse of
`human-approval-boundary`: a documented standing approval for the mechanical
delivery loop within named scope, an auto-advance rule for already-approved
phases, and the control surfaces (restated approval, opt-out phrase,
reviewer-block path) that keep the human in command of the loop they are no
longer asked to bless step-by-step. Both source repos in the extraction
evidence ran this pattern in production; the difference between it and an
autonomy incident is precisely the governance elements this skill refuses to
omit.

**Why manual-only:** this skill authors standing authority — it thins future
human gates. A model auto-invoking the skill that widens its own autonomy is
self-escalation; like `agent-authorization-matrix`, it must be a human who
opens this door.

## Use When

- Use when (human-invoked): approval fatigue is visible — the human
  rubber-stamps mechanical steps, or complains about being asked for every
  push/PR inside work already approved.
- Use when: writing a repo's standing-approval policy — what the delivery
  loop may do without re-asking, and where it must still stop.
- Use when: an existing "just keep going" habit is UNdocumented — converting
  informal autonomy into named, bounded, revocable autonomy.
- Do NOT use when: recording a single granted approval — that is
  `scoped-approval-register`; the adopted standing approval itself is
  recorded there as an entry, with scope allowed and forbidden.
- Do NOT use when: defining which actions agents may EVER take (the
  deny-by-default floors) — that is `agent-authorization-matrix`. This skill
  does not grant authority by itself. An applicable, explicit human decision
  recorded for the repository may satisfy an approval-required matrix cell;
  this design cannot silently move the floor.
- Do NOT use when: adversarially reviewing whether an approval flow trains
  rubber-stamping — that is `human-agent-trust-reviewer`; run it against the
  policy this skill produces.
- Do NOT use when: the platform's merge-deploy coupling is the question —
  that is `merge-is-deploy-governance`.

## Inputs to Inspect

1. `agent-authorization-matrix` (or the repo's equivalent policy): the
   approval-required and forbidden actions this design cannot silently
   authorize — protected-branch merge, arming auto-merge, deploys,
   production data, secrets, and history rewrites.
2. The incident record that motivates the floors — in this library, the
   ungoverned-auto-merge incident encoded in `agent-authorization-matrix`'s
   evals: a prior session armed auto-merge and a security PR merged to main
   with zero human review. Every governance element below exists because of
   a failure shaped like that one.
3. The actual fatigue evidence: which approvals the human granted
   mechanically in recent sessions (rate and latency of "yes"), which steps
   were re-asked although already covered.
4. The delivery loop as practiced: branch conventions, CI checks, merge
   strategy, who merges today.
5. The phase/plan structure: are phases named and individually approved
   (auto-advance has something to advance THROUGH), or is work amorphous
   (then phase-advance has no substrate — fix planning first)?

## Workflow

1. **Fix the hard floor first.** Restate the approval-required and forbidden
   actions from `agent-authorization-matrix`. A standing policy does not
   approve an action merely by naming it. A protected-branch merge may proceed
   only when a separate, explicit, active human grant covers the exact repo,
   action, and constraints. Check later owner instructions before relying on a
   grant. No design work proceeds until this floor is written.
2. **Name the standing scope.** Enumerate the mechanical loop steps covered
   (e.g. commit to feature branch, push, open PR, monitor CI, fix red,
   re-push, pull after human merge) and the boundaries (which repo, which
   branch patterns, which change classes — compose
   `change-classification-gate` classes here). Unnamed = not covered.
3. **Write the phase-advance rule.** Auto-advance may continue ONLY into a
   phase that is already individually named AND approved in the plan of
   record. Encountering an unnamed, reordered, or scope-changed phase ends
   auto-advance and returns to the human.
4. **Define the required prompt pattern.** Each session operating under
   standing approval must RESTATE it (scope + opt-out phrase) in its opening
   exchange — approval that is invisible cannot be revoked, and restating is
   what keeps the human consciously renewing rather than passively leaking
   authority. Template in
   [references/standing-approval-policy.md](references/standing-approval-policy.md).
5. **Define the opt-out phrase.** One explicit, unambiguous phrase (e.g.
   "HOLD: manual approvals this session") that suspends the standing
   approval instantly, mid-loop, no questions asked. Document where it may
   be said (prompt, PR comment) and that it always wins over the policy.
6. **Template merge-after-green as OPT-IN only.** The source pattern
   includes default-on autonomous merge after green validation. This library
   never makes that the default profile. Without a separate applicable human
   merge grant, the profile is open-PR-and-STOP. An explicit, recorded grant
   may authorize a named protected-branch merge or a durable class of merges;
   apply its actual scope, lifecycle, and later constraints. Green checks
   alone never supply approval. Do not treat a grant to merge as permission
   to arm GitHub auto-merge; that action needs its own explicit decision.
7. **Write the reviewer-block exception path.** A human review request,
   requested change, failing required check, or ANY reviewer objection
   suspends auto-advance for that item: the loop stops, states what blocked,
   and waits. Auto-advance never argues with, re-requests, or routes around
   a reviewer.
8. **Route the adopted policy to record.** The human's adoption is a grant:
   record it via `scoped-approval-register` (scope allowed = the named loop;
   scope FORBIDDEN = the floors and everything unnamed). Recommend
   `human-agent-trust-reviewer` as the adversarial check on the resulting
   approval surface.

## Output Format

```
STANDING APPROVAL POLICY (draft for human adoption)
Hard floor:                   <approval-required and forbidden actions from the matrix>
Applicable grants:            <separate, active human decisions; repo, scope, limits, later instructions>
Standing scope (named):       <loop steps + branches + change classes covered>
Phase-advance rule:           <auto-advance only into named+approved phases; exits on drift>
Required prompt pattern:      <the restatement each session must open with>
Opt-out phrase:               <exact phrase; where it may be said; always wins>
Merge profile:                open-PR-and-STOP (default) | opt-in: <named profile backed by an applicable human decision>
Reviewer-block path:          <what suspends the loop; what the loop does when blocked>
Rationale:                    governance elements are non-optional — cites the ungoverned
                              auto-merge incident (agent-authorization-matrix evals)
Adoption:                     pending human approval → then recorded via scoped-approval-register
```

## Validation Checklist

- [ ] Approval-required actions have an applicable explicit human decision
      before execution; forbidden actions remain forbidden without a separate
      recorded decision. A merge grant does not authorize arming auto-merge.
- [ ] Every covered step is NAMED; the policy contains no "and similar
      routine steps" elasticity.
- [ ] Merge-after-green appears only as an explicit opt-in profile with the
      default being open-PR-and-STOP.
- [ ] The opt-out phrase is defined, exact, and documented as always winning.
- [ ] The prompt pattern forces per-session restatement of scope + opt-out.
- [ ] Phase-advance is bounded to already-named-and-approved phases.
- [ ] The reviewer-block path suspends the loop rather than arguing with it.
- [ ] The rationale cites the ungoverned-auto-merge incident; the policy is
      delivered as a DRAFT for human adoption, not enacted by this skill.

## Gotchas

- **Scope elasticity is the failure mode.** "The mechanical loop" quietly
  grows to include tagging, releasing, merging. Each action needs explicit
  scope; a project's existing merge grant is applied only in that project.
- **Auto-advance across a re-planned phase:** the plan changed since
  approval; advancing into the renamed phase is advancing into unapproved
  work. The rule binds to phases as approved, not positions in a list.
- **The invisible standing approval:** a policy adopted months ago that no
  session restates is indistinguishable from no governance — restating is
  the difference between standing approval and folklore.
- **Opt-in decay:** an opt-in merge profile selected once, then treated as
  eternal. Profile selection is a register entry with an expiry like any
  grant.
- **Fatigue theater in reverse:** thinning approvals that were load-bearing.
  Only approvals whose evidence shows mechanical granting (instant yes,
  zero variance) are candidates; a slow, considered approval is a real gate
  — leave it.
- **Armed auto-merge from a prior session** converts "green CI" into an
  unreviewed merge even when THIS session behaves. The loop must check for
  armed state (`gh pr view <n> --json autoMergeRequest`) rather than assume
  its own restraint is the whole story.

## Stop Conditions

- Asked to include protected-branch merge or arming auto-merge merely because
  this skill was invoked, or to make merge-after-green the default → refuse,
  cite the matrix and the incident. If a separate active owner grant is cited,
  verify its repository, action, limits, and later instructions before use.
- No `agent-authorization-matrix` (or equivalent authority policy) exists →
  stop; the floors must exist before the fatigue layer that presumes them.
  Offer to route there first.
- The phase plan has no named, individually-approved phases → phase-advance
  has no substrate; deliver the standing-scope design only and say why
  auto-advance was withheld.
- Asked to enact the policy immediately without human adoption → refuse;
  this skill drafts, the human adopts, the register records.

## Supporting Files

- [references/standing-approval-policy.md](references/standing-approval-policy.md)
  — full policy template: prompt-pattern wording, opt-out mechanics,
  profile definitions, and the incident-anchored rationale section.
- `evals/evals.json` — behavior cases incl. refusing default-on merge and
  refusing to cover matrix floors.
- `evals/trigger-evals.json` — discrimination against
  `scoped-approval-register`, `agent-authorization-matrix`,
  `human-approval-boundary`, and `human-agent-trust-reviewer`.
