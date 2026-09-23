# First 20 skill documents: bounded readability correction — 2026-09-23

## Scope and estimate

The first 20 skill documents were audited for first-use terminology and output
clarity. This correction changes only the [A/B Test Designer](../../../.claude/skills/ab-test-designer/SKILL.md)
and [Accessibility Test Harness](../../../.claude/skills/accessibility-test-harness/SKILL.md)
entrypoints, plus this evidence note. The other 18 audited skills were not
rewritten. The shared documentation readability ledger is reserved for the
coordinator's later integration.

The isolated worktree started from `70ca4eef13521d27c11754979b2bfb90ce3981c5`,
the `origin/main` head after pull request (PR) #149. The prior estimate for this
correction item was **none**; the new bounded batch estimate is **2–4 active
hours**. The selected remaining backlog total at start was **175–394 active
hours**. Active-only work and observed wall time are separate measurements.

## Contract-preserving changes

- The A/B skill now defines minimum detectable effect (MDE), confidence
  interval (CI), sample-ratio mismatch (SRM), and alpha before they appear in
  its workflow and output template. Template values now spell out the
  corresponding measurement or decision while retaining the experiment's
  hypothesis, power, fixed horizon, validity, and ship/kill/iterate contract.
- The accessibility skill now defines WCAG, E2E, CI, a11y, EN 301 549, ADA,
  ARIA, SR, AT, and VPAT before the body uses them. Its output template expands
  opaque labels while retaining the accessibility harness, automated/manual
  split, criterion, severity, evidence, and execution-handoff contract.
- Both skills' YAML frontmatter and selection descriptions remain unchanged.
  Their trigger and behavior evaluation files remain unchanged. No skill
  invocation or execution authorization was added.

No private input, provider, credential, or real host was accessed.

## Verification and timing

Work started at **2026-09-23 19:31:24 UTC**. At the **19:33:39 UTC** local
checkpoint, the observed wall interval was **2 minutes 15 seconds**.
`python -B scripts/validate-skills.py` passed with **185 valid skills and zero
warnings**; all **6 local links** across the three scoped pages resolved, and
`git diff --check` passed. The YAML frontmatter of both skills and their four
trigger/behavior evaluation files were unchanged after newline normalization.
Their routing descriptions and evaluation criteria therefore remain available
for the same focused trigger and behavior checks; no live model evaluation was
run for this wording-only correction. Independent read-only review cleared the
three-path draft at **19:34:38 UTC** with no blocker. The final local checkpoint
was **19:35:08 UTC**, **3 minutes 44 seconds** after the start. Active-only
labor is not instrumented.
