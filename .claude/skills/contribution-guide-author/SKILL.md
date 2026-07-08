---
name: contribution-guide-author
description: Design a CONTRIBUTING guide that takes a contributor from zero to a merged change — environment setup, the contribution workflow (fork/branch/PR or the project's flow), coding standards and commit/PR conventions, how to run tests and checks locally, the review and merge process, honest expectation-setting (response times, what gets accepted), code-of-conduct and licensing/DCO-CLA pointers, and lowering the first-contribution barrier (good-first-issues, where to ask). Designs contribution guides GENERICALLY and product-agnostically. Use when writing or overhauling a CONTRIBUTING guide, when contributors churn on unclear process, or when onboarding external contributors to an open or inner-source project. Do NOT use to onboard a new EMPLOYEE/team member to the codebase (onboarding-doc-designer), write the README (readme-craftsman), or design the docs contribution toolchain/mechanics (docs-as-code-architect).
---

# Contribution Guide Author

## Purpose

A would-be contributor arrives with a fix and leaves without merging it,
because the project never told them how: no setup steps that work, no
idea which branch, tests that fail for reasons the docs don't mention, a
PR that sits for weeks with no word on whether it's even wanted. Every
one of those is a contribution lost to missing process, not missing
willingness. This skill designs the CONTRIBUTING guide that closes those
gaps — the path from zero to a merged change: setup, workflow, standards,
running checks locally, the review and merge process, honest expectations
about response and acceptance, the governance pointers (conduct, license,
security), and the on-ramps that make a first contribution feel possible.
It designs contribution guides generically — for any project, with
placeholders, not one specific repo.

## Use When

- Use when: writing or overhauling a CONTRIBUTING guide for an open-source
  or inner-source project.
- Use when: contributors churn or bounce because the process (setup,
  workflow, review) is unclear or undocumented.
- Use when: opening a project to external contribution and you need the
  on-ramp, standards, and expectations written down.
- Use when: a project gets low-quality or misdirected PRs because scope
  and conventions were never stated.
- Do NOT use when: the task is onboarding a new EMPLOYEE/team member to
  the codebase and how-we-work — that is `onboarding-doc-designer` (an
  internal joiner, not an external contributor).
- Do NOT use when: the task is the README front door — that is
  `readme-craftsman` (which links to CONTRIBUTING).
- Do NOT use when: the task is the docs contribution TOOLCHAIN/mechanics
  (edit-on-page, preview builds, CI) — that is `docs-as-code-architect`;
  this skill writes the guide's CONTENT.

## Inputs to Inspect

1. The project's contribution model: open-source (external, fork-based)
   vs inner-source (internal, branch-based), and maintainer capacity and
   expectations.
2. The actual workflow: how changes really get in — branching, PRs,
   required checks, who can merge — so the guide matches reality, not an
   ideal.
3. The local dev setup: the real steps to clone, install, build, run, and
   test on a clean machine (the most common bounce point).
4. Standards and automation: linters/formatters, commit/PR conventions,
   test requirements — prefer pointing at automated tooling over prose
   rules.
5. Governance artifacts: code of conduct, license, any CLA/DCO sign-off
   requirement, and the security-disclosure process.

## Workflow

1. **Map the zero-to-merged path.** The guide's spine is the journey:
   find something to work on → set up locally → make the change → run
   checks → open the PR → get reviewed → merge. Every section serves a
   step on that path; anything that doesn't is noise.
2. **Nail the setup.** Exact, verified steps to clone, install, build,
   run, and run the tests on a clean environment — with prerequisites.
   Broken setup is where most first contributions die; treat it like
   `readme-craftsman` treats the quickstart.
3. **State the workflow concretely.** Fork vs branch, naming, how to keep
   up to date, how to open the PR, and what a good PR looks like (scope,
   description, linked issue). Match the project's real process.
4. **Point at automated standards.** Coding style enforced by a
   formatter/linter (run this command), commit/PR conventions, and the
   test/checks that must pass. Automated checks beat prose rules nobody
   reads — tell contributors how to run them locally before pushing.
5. **Explain review and merge honestly.** Who reviews, realistic
   turnaround, how feedback works, what gets accepted vs declined (scope,
   roadmap fit, quality bar), and who merges. Setting expectations
   prevents the silent-PR frustration.
6. **Cover governance and safety.** Link the code of conduct, the license
   and any CLA/DCO sign-off, and — critically — the security-disclosure
   process (report privately, do NOT open a public issue for a
   vulnerability). These are pointers, not full texts.
7. **Lower the first-contribution barrier.** Good-first-issues, where to
   ask questions (discussions/chat), and a short first-PR checklist. The
   difference between a thriving project and a closed one is often just
   how possible the first contribution feels.
8. **Keep it product-agnostic and maintainable.** Use placeholders, not a
   single repo's specifics; single-source commands where possible; and
   keep it current with the real process (a stale CONTRIBUTING is worse
   than none). Deliver in the Output Format.

The zero-to-merged section skeleton, the setup-verification checklist,
and the expectation-setting patterns:
[references/contribution-guide-sheet.md](references/contribution-guide-sheet.md).

## Output Format

```
CONTRIBUTING GUIDE — <project> (product-agnostic template)
Path:          find work → setup → change → run checks → PR → review → merge
Setup:         exact, verified clone/install/build/run/test steps + prereqs
Workflow:      fork/branch model; PR conventions; what a good PR looks like
Standards:     linter/formatter (run: <cmd>); commit/PR conventions; required checks (run locally)
Review/merge:  who reviews; realistic turnaround; accept-vs-decline criteria; who merges
Governance:    code of conduct; license; CLA/DCO; SECURITY disclosure (private, not public issue)
On-ramps:      good-first-issues; where to ask; first-PR checklist
Maintenance:   placeholders; single-sourced commands; kept current with real process
Boundaries:    new-hire onboarding → onboarding-doc-designer; README → readme-craftsman;
               docs edit mechanics → docs-as-code-architect
```

## Validation Checklist

- [ ] The guide follows the zero-to-merged path; every section serves a
      step on it.
- [ ] Setup steps are exact, prerequisite-stated, and verified on a clean
      environment.
- [ ] The contribution workflow matches the project's REAL process, not an
      idealized one.
- [ ] Standards point at automated tooling with the commands to run checks
      locally.
- [ ] Review/merge expectations are honest: turnaround, accept-vs-decline
      criteria, who merges.
- [ ] Code of conduct, license, CLA/DCO, and a PRIVATE security-disclosure
      process are linked.
- [ ] First-contribution on-ramps (good-first-issues, where to ask, a
      checklist) exist.
- [ ] It's product-agnostic (placeholders) and the new-hire/README/toolchain
      concerns are handed off.

## Gotchas

- Broken or incomplete setup steps kill more contributions than any other
  section — someone spends an hour fighting the build and gives up. Verify
  setup on a clean machine like a quickstart.
- A CONTRIBUTING guide that describes an idealized workflow the project
  doesn't actually follow sends contributors down the wrong path and
  wastes maintainer time correcting them. Document reality.
- Prose style rules nobody runs are ignored; a formatter/linter with a
  one-command check is obeyed. Automate the standard and tell people how
  to run it before pushing.
- Silent PRs are the top contributor frustration. Stating realistic
  review turnaround and what gets accepted — even "we're volunteers, allow
  a week" — beats leaving people guessing.
- Omitting the security-disclosure process invites someone to file a
  public issue for a vulnerability, turning a private report into a
  zero-day. Always point to a private channel.
- No first-contribution on-ramp (good-first-issues, a place to ask) means
  only the already-expert contribute; the barrier stays high and the
  contributor base stays tiny.
- This is a contributor guide (external), not new-hire onboarding
  (internal) — conflating the two produces a document that serves neither
  audience well.

## Stop Conditions

- The audience is a new EMPLOYEE/team member joining the codebase (first
  week, how-we-work, orientation) → route to `onboarding-doc-designer`;
  that's an internal joiner, not an external contributor.
- The task is the README front door → route to `readme-craftsman` (which
  links to CONTRIBUTING).
- The task is the docs contribution TOOLCHAIN (edit-on-page, preview
  builds, CI mechanics) → route to `docs-as-code-architect`; this skill
  writes the guide content.
- The real blocker is that the project has NO defined contribution process
  to document → surface that the process must be decided (by maintainers)
  before it can be written down; don't invent a workflow the project won't
  follow.

## Supporting Files

- [references/contribution-guide-sheet.md](references/contribution-guide-sheet.md)
  — the zero-to-merged section skeleton, the setup-verification checklist,
  expectation-setting patterns, and the governance-pointers list.
- `evals/evals.json` — behavior cases including the process-churn fix, the
  automate-the-standard move, and the security-disclosure requirement.
- `evals/trigger-evals.json` — discrimination against `onboarding-doc-designer`
  (contributor vs new hire), `readme-craftsman`, and `docs-as-code-architect`.
