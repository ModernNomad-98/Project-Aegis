---
name: readme-craftsman
description: Craft or overhaul a README so a newcomer can understand, evaluate, and start using a project in minutes — the above-the-fold what/why/who in the first screen, a quickstart that actually runs, install and minimal usage, and links OUT to deeper docs (the README is the entry point, not the manual). Orders by reader need, resists dumping the whole manual inline, and keeps it maintainable. Use when writing or overhauling a README, when a project's front door does not explain what it is or how to start, or when the README has bloated into a kitchen sink. Do NOT use to organize a whole documentation SET by type (diataxis-doc-organizer), design the docs toolchain/pipeline (docs-as-code-architect), write the contributor guide (contribution-guide-author), or design new-hire onboarding docs (onboarding-doc-designer).
---

# README Craftsman

## Purpose

The README is a project's front door, and most are either a locked door
(no idea what this is) or a hoarder's garage (the entire manual, badges
three rows deep, and the actual "what is this" buried on screen four). A
visitor decides in seconds whether to keep reading; if the first screen
doesn't say what the project is, who it's for, and why they'd use it,
they leave. This skill crafts a README that earns those seconds: the
what/why/who above the fold, a quickstart that actually runs on a clean
machine, the minimum install-and-use, and links OUT to the deeper docs
rather than inlining them. It treats the README as an entry point and a
router, not the manual — and keeps it lean enough to stay current.

## Use When

- Use when: writing a README for a new project, or overhauling one that
  doesn't explain what the project is or how to start.
- Use when: the README has bloated into a kitchen sink (the full manual,
  every option, walls of badges) and needs re-focusing on the newcomer.
- Use when: a capable project has low adoption because its front door is
  confusing, intimidating, or silent about the value.
- Use when: auditing whether a README's first screen passes the
  "what/why/who in seconds" test.
- Do NOT use when: the task is organizing an entire documentation SET
  into tutorials/how-to/reference/explanation — that is
  `diataxis-doc-organizer` (the README links INTO that set).
- Do NOT use when: the task is the docs toolchain/pipeline (generator,
  build, deploy, CI checks) — that is `docs-as-code-architect`.
- Do NOT use when: the task is the CONTRIBUTING guide (how to contribute)
  — that is `contribution-guide-author`; the README links to it.
- Do NOT use when: the task is onboarding docs for someone JOINING the
  team/codebase — that is `onboarding-doc-designer`.

## Inputs to Inspect

1. The project itself: what it does, who it's for, its stage (prototype,
   library, service, app), and what genuinely differentiates it — the raw
   material for the first screen.
2. The current README (if any): where the "what is this" actually
   appears, what's bloated, what's stale, and whether the quickstart
   still runs.
3. The real quickstart path: the minimum steps from nothing to a working
   result on a clean environment — tested, not assumed.
4. The rest of the docs: what deeper material exists (or should) so the
   README links out instead of inlining, and the entry points to it.
5. The audience's starting point: prior knowledge assumed, and the
   platforms/prerequisites a newcomer actually has.

## Workflow

1. **Nail the first screen.** Open with a one-line description a stranger
   understands, then what it's for and who it's for, and why they'd
   choose it. This is the highest-leverage text in the project; everything
   else is secondary. No badges or tables before the reader knows what
   this is.
2. **Provide a quickstart that runs.** The shortest path from zero to a
   visible result — copy-pasteable, on a clean machine, with prerequisites
   stated. Verify it works; a broken quickstart is worse than none because
   it burns the trust the first screen earned.
3. **Add minimal install and usage.** Just enough to get going — the
   common case, not every flag. Depth goes to the deeper docs; the README
   shows the 20% that covers 80%.
4. **Route to the rest.** Link OUT to full docs, the contribution guide,
   examples, API reference, and support/community. The README is a hub;
   its job is to get readers to the right next page, not to be every
   page.
5. **Order by reader need, not by author convenience.** Newcomer-critical
   content first (what/why/quickstart), maintainer/edge content later or
   elsewhere. Badges, license, and status belong below the fold or in a
   compact row — never ahead of comprehension.
6. **Cut what doesn't belong.** Full API dumps, exhaustive config,
   changelog, and deep architecture are OTHER documents — link them.
   Every paragraph in the README competes with the quickstart for
   attention.
7. **Design for maintenance.** Keep it short enough that it stays true;
   note the parts most likely to drift (version numbers, commands) and
   prefer linking to generated/single-source content over duplicating it.
8. **Deliver** the README (or the overhaul plan) in the Output Format,
   with the first-screen test explicitly passed.

Section templates by project type (library / CLI / service / app), the
first-screen checklist, and the quickstart-verification recipe:
[references/readme-sheet.md](references/readme-sheet.md).

## Output Format

```
README PLAN / DRAFT — <project>
First screen:  one-liner; what it does; who it's for; why choose it   (badges below)
Quickstart:    minimal, copy-pasteable, prereqs stated, VERIFIED to run
Install/usage: common case only; depth linked out
Routes:        → full docs / CONTRIBUTING / examples / API reference / support
Below fold:    badges, license, status, acknowledgements
Cut/link-out:  <content moved to other docs, with destinations>
Maintenance:   drift-prone spots; single-sourced/generated where possible
First-screen test: what/why/who understandable in seconds — PASS
Boundaries:    corpus org → diataxis-doc-organizer; pipeline → docs-as-code-architect;
               CONTRIBUTING → contribution-guide-author; onboarding → onboarding-doc-designer
```

## Validation Checklist

- [ ] The first screen states what it is, who it's for, and why to use it
      — understandable by a stranger in seconds.
- [ ] A quickstart exists, is copy-pasteable, states prerequisites, and
      has been verified to run on a clean environment.
- [ ] Install/usage shows the common case, not every option; depth is
      linked out.
- [ ] The README routes to the deeper docs, CONTRIBUTING, examples, and
      support rather than inlining them.
- [ ] Badges/license/status sit below comprehension, not ahead of it.
- [ ] Content that belongs in other documents has been cut and linked.
- [ ] Drift-prone values are single-sourced/linked rather than
      duplicated.
- [ ] Corpus organization, pipeline, contribution, and onboarding
      concerns are handed to their owning skills.

## Gotchas

- The single most common README failure is burying "what is this" below
  the fold under badges and a table of contents. If a stranger can't tell
  what the project is in the first paragraph, nothing else matters.
- A quickstart that doesn't run on a clean machine is a trust bomb: it
  proves the docs are stale and makes the reader doubt everything else.
  Verify it, prerequisites and all.
- The README is not the manual. Inlining every option and edge case
  pushes the quickstart off-screen and guarantees the whole thing goes
  stale. Link out; keep the front door lean.
- Badge walls signal activity to maintainers and noise to newcomers. A
  compact row is fine; three stacked rows above the description are
  vanity.
- Duplicating version numbers, commands, and config that live elsewhere
  means they'll drift. Single-source or generate them.
- "Comprehensive" is the enemy of "read". A README nobody finishes helps
  nobody; optimize for the reader who leaves after ten seconds, then the
  one who stays for two minutes.

## Stop Conditions

- The task is organizing the whole documentation corpus by type
  (tutorials/how-to/reference/explanation) → route to
  `diataxis-doc-organizer`.
- The task is the docs toolchain — generator, build, preview, deploy, CI
  link-checking → route to `docs-as-code-architect`.
- The task is the contribution guide or new-hire onboarding docs → route
  to `contribution-guide-author` or `onboarding-doc-designer`.
- The quickstart cannot be verified because the project can't be run in a
  clean environment from the available information → flag it; do not ship
  an unverified quickstart as if it works.

## Supporting Files

- [references/readme-sheet.md](references/readme-sheet.md) — section
  templates by project type (library/CLI/service/app), the first-screen
  checklist, the quickstart-verification recipe, and a what-belongs-vs-
  link-out table.
- `evals/evals.json` — behavior cases including the buried-what-is-this
  fix, the unverified-quickstart refusal, and the kitchen-sink trim.
- `evals/trigger-evals.json` — discrimination against `diataxis-doc-organizer`,
  `docs-as-code-architect`, `contribution-guide-author`, and
  `onboarding-doc-designer`.
