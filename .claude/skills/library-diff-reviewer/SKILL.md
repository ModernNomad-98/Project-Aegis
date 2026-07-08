---
name: library-diff-reviewer
description: Review a whole library-changing PR end-to-end — skill-adding, skill-modifying, or skill-retiring — as the integration layer above single-skill quality review. Verifies a fresh mechanical-validator run tied to the PR head (stale or merely claimed passes rejected), registration consistency (catalog, README, status tables, decision-log entry, banked-candidate graduation, skill-count arithmetic agreeing everywhere), collision of each added skill against the shipped corpus AND its in-batch siblings, diff coherence (every changed file maps to the stated intent; nothing smuggled in), and per-skill quality via skill-quality-reviewer as the inner loop — one PR verdict with per-area findings. Use when a skill-library PR needs review before merge, or re-verification after. Do NOT use for ONE skill's quality alone (skill-quality-reviewer), a product-code diff (code-reviewer), the approval/merge-authority trail (agent-governance-audit), or a release go/no-go (release-readiness-reviewer).
---

# Library Diff Reviewer

## Purpose

Give a library-changing PR the review its pieces cannot give themselves. The
mechanical validator proves each skill is structurally valid;
`skill-quality-reviewer` judges whether ONE skill is good; neither answers
the PR-level question: does this change integrate correctly into the library
as a whole — is every registration surface consistent, does the count
arithmetic agree everywhere it appears, do the added skills collide with the
shipped corpus or with EACH OTHER, and does the diff contain exactly what its
stated intent covers? The deliverable is one PR verdict (approve /
request-changes) with per-area findings a maintainer can act on before merge
— or a re-verification of a PR already merged.

## Use When

- Use when: a PR that adds one or more skills to the library needs end-to-end
  review before merge — validator evidence, registration, collisions,
  coherence, and the quality of each added skill.
- Use when: a PR modifies shipped skills (descriptions, triggers, evals) and
  the change needs collision re-checking and integration review.
- Use when: a PR retires or removes a skill — verifying registration rows
  move to a retired record, no dangling references remain, and the count
  arithmetic decrements everywhere.
- Use when: re-verifying an already-merged library PR against the merged
  tree.
- Do NOT use when: the question is one skill's internal quality outside any
  PR context — trigger phrasing, eval integrity, scope — that is
  `skill-quality-reviewer`; this skill composes it per added skill and adds
  the PR-level integration checks around it.
- Do NOT use when: reviewing a product-code diff for correctness or security
  — that is `code-reviewer` / `security-pr-reviewer`. This skill's target is
  a PR whose subject is the skill library itself.
- Do NOT use when: auditing WHO approved, who armed auto-merge, or whether
  the change followed process — that is `agent-governance-audit` (the
  process trail); this skill judges the diff's content, not its authority
  chain.
- Do NOT use when: gating a product release (deploy risk, migrations,
  rollback) — that is `release-readiness-reviewer`.
- Do NOT use when: designing HOW a skill should be retired — that is
  `skill-deprecation-planner`; this skill reviews the retirement PR once it
  exists.

## Inputs to Inspect

1. The PR itself: stated intent (title/body, the declared before→after skill
   count), the full changed-file list, and the head commit SHA the review is
   pinned to.
2. Fresh mechanical-validator output on the PR head — run
   `python scripts/validate-skills.py` on a checkout of the head SHA, or a CI
   run whose recorded head SHA equals the PR's current head (purpose:
   freshness; a green run from an earlier push proves nothing about the
   current diff).
3. Every added or modified skill directory in the diff: `SKILL.md`,
   `evals/evals.json`, `evals/trigger-evals.json`, `references/*`.
4. The registration surfaces at the PR head: the skills catalog, the README
   (shipped list and any phase/status tables), and the decision log — every
   place a skill list or count appears.
5. The shipped corpus of skill descriptions (all of `.claude/skills/*/SKILL.md`
   at the PR head) — the collision sweep target.
6. For a retirement PR: the deprecation plan it claims to execute (from
   `skill-deprecation-planner`, when one exists).

## Workflow

1. **Pin the review target.** Record the head SHA. Enumerate every changed
   file and classify it: new skill directory / modified skill / registration
   doc (catalog, README, decision log) / other. Every "other" file is a
   coherence finding candidate — nothing rides along unexamined.
2. **Gate on fresh validator evidence.** Confirm the mechanical validator
   passed ON THIS HEAD (checkout-and-run, or a CI run pinned to the same
   SHA). What the validator enforces — structure, sections, lengths,
   registration PRESENCE, exact-name collisions, eval JSON parse — is
   settled by that run and never re-scored here. A validator FAIL stops the
   review after areas 1 and 3 (registration and coherence notes still help
   the author); no quality verdicts are issued on a structurally invalid
   head.
3. **Area 1 — registration consistency.** The validator checks presence;
   this area checks placement and truth: each added skill sits in the right
   catalog cluster with an accurate summary; README status text describes
   the post-merge state (never "this branch" or "in this PR"); banked
   candidates the PR builds are marked graduated at their banking site; a
   dated decision-log entry exists and matches the diff; and the skill-count
   arithmetic (before→after) agrees at EVERY site a count appears — catalog
   status, README narrative, tables, decision entry.
4. **Area 2 — collision sweep, shipped AND in-batch.** For each added or
   trigger-modified skill, sweep its description against the shipped corpus
   (this is `skill-quality-reviewer`'s check 2, composed) — and additionally
   against its own PR siblings, which a single-skill review has no reason to
   read: two skills added in the same PR can collide with each other while
   each passes alone. Name every colliding pair and quote the request that
   confuses them.
5. **Area 3 — diff coherence.** Map every changed file to the stated
   intent. Flag: edits to skills the intent never mentions, deletions not
   declared, registration edits that disagree with the declared count
   change, and generated or unrelated files smuggled into the diff.
6. **Area 4 — per-skill quality (inner loop).** Run `skill-quality-reviewer`
   for each added skill and each substantially modified one. Inherit its
   verdicts: any per-skill revise/reject caps this review at
   request-changes. Do not re-perform its checks at the PR level — compose
   them.
7. **For retirement PRs**, additionally verify: registration rows moved to a
   retired record rather than vanishing, a reverse-link sweep shows no
   dangling references (no neighbor description or trigger-eval still names
   the removed skill as live), and the executed steps match the deprecation
   plan when one exists.
8. **Deliver the verdict.** Per-area PASS/CONCERN/FAIL with evidence, the
   per-skill inner-loop verdicts, and ONE overall recommendation: approve or
   request-changes with the blocking items listed. The review is an
   artifact: it never merges, approves on-platform, or arms auto-merge —
   merge authority stays human.

Per-area pass criteria, the count-arithmetic site list, the in-batch
collision procedure, and post-merge re-verification notes:
[references/pr-review-checklist.md](references/pr-review-checklist.md).

## Output Format

```
LIBRARY DIFF REVIEW — <PR ref / branch>
Head:        <SHA>    Intent: <stated scope and before→after count>
Validator:   PASS on head (<output line>) | FAIL → quality areas skipped, findings below
Areas:
  1 Registration consistency   PASS | CONCERN | FAIL — <site + quoted mismatch | "consistent at N sites">
  2 Collision (shipped+batch)  PASS | CONCERN | FAIL — <colliding pair + confusing request | "none found">
  3 Diff coherence             PASS | CONCERN | FAIL — <out-of-intent file(s) | "all files map to intent">
  4 Per-skill quality          <skill> → ship | revise | reject | make-it-an-extension (inner loop: skill-quality-reviewer)
Retirement checks (when applicable): <rows-moved / dangling-references / plan-conformance>
Verdict:     APPROVE | REQUEST CHANGES — <blocking items, each mapped to an area>
Not inspected: <what this review did not read, and why>
```

## Validation Checklist

- [ ] The review is pinned to a named head SHA, and the validator evidence
      is tied to that exact SHA — no green-from-an-earlier-push accepted.
- [ ] Nothing the validator enforces was re-scored as a finding.
- [ ] Count arithmetic was checked at every site a count appears, and the
      sites are listed in the report.
- [ ] The collision sweep covered both the shipped corpus and the PR's own
      siblings; colliding pairs are NAMED with the confusing request.
- [ ] Every changed file was classified; every out-of-intent file appears in
      area 3.
- [ ] Each added skill has an inner-loop verdict from
      `skill-quality-reviewer`; none was waved through at the PR level.
- [ ] The verdict is exactly approve or request-changes; the review performed
      no platform action (no merge, no approval click, no auto-merge arming).
- [ ] Not-inspected list present and honest.

## Gotchas

- Stale validator evidence: a green check from an earlier push survives on
  the PR page after new commits. Freshness means the run's head SHA equals
  the PR's current head — verify the SHA, not the badge color.
- "This branch" registration text: status lines written from the branch's
  point of view become false the moment the PR merges. Registration text
  must describe the post-merge world.
- Count drift: the before→after count appears in more places than authors
  remember (catalog status, README narrative, tables, decision entry). One
  missed site ships a permanent inconsistency.
- In-batch collisions are invisible to single-skill review: each sibling is
  reviewed against the SHIPPED corpus and passes; the two siblings still
  collide with each other. Only the PR-level sweep sees the pair.
- Smuggled edits dressed as registration: a diff labeled "add 4 skills" that
  also rewrites a neighbor's description is two changes; the second needs
  its own declaration or its own PR.
- On squash-merge platforms the merged result is ONE commit — post-merge
  re-verification reviews the merged tree, not the branch's commit list, and
  a bad merge reverts as one ordinary `git revert <squash-sha>`.
- Historical decision-log entries are immutable: a PR that edits an older
  dated entry (rather than appending a new one) is a coherence FAIL even
  when the edit looks like a tidy-up.
- The inner loop is not optional for "small" skills: a 100-line skill can
  still be unpickable or colliding; PR-level review without per-skill
  quality verdicts is registration proofreading, not review.

## Stop Conditions

- Asked to approve BECAUSE CI is green or the validator passed → refuse the
  rubber stamp: mechanical evidence is the entry ticket; the four areas and
  the inner loop are the review. Run them or return no verdict.
- Asked to merge, approve on-platform, or arm auto-merge as part of the
  review → refuse: this skill produces a review artifact; merge authority is
  a human decision outside it.
- The PR head cannot be checked out or its changed-file list retrieved →
  stop; there is no end-to-end review of a diff from its description.
- Asked to soften a finding or unname a colliding pair → refuse; the report
  states what the evidence states.
- The validator FAILS on the head → deliver areas 1 and 3 findings only,
  state that quality areas were skipped, and stop.
- The PR mixes library changes with product-code changes → review the
  library slice, state the product slice is out of scope here
  (`code-reviewer`), and flag the mix itself as a coherence concern.

## Supporting Files

- [references/pr-review-checklist.md](references/pr-review-checklist.md) —
  per-area pass criteria, the count-arithmetic site list, the in-batch
  collision procedure, retirement-PR checks, and post-merge re-verification
  notes for squash-merge platforms.
- `evals/evals.json` — behavior cases including the retirement-PR edge and
  the green-CI rubber-stamp refusal.
- `evals/trigger-evals.json` — discrimination against
  `skill-quality-reviewer` (the pinned seam: whole PR vs ONE skill),
  `code-reviewer`, `agent-governance-audit`, and
  `release-readiness-reviewer`.
