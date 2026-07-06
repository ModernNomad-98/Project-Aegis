---
name: ai-closeout-reporter
description: Produce the end-of-task closeout report — what changed, what was intentionally NOT done or was omitted (always a dedicated section, "None" written explicitly when empty), files touched, tests and validation actually run with real results, evidence, risks, skipped checks, and the recommended next action. Use when finishing a task, handing off work, opening or closing a PR, or when asked what was actually done. Scope reductions must be disclosed, never silent.
---

# AI Closeout Reporter

## Purpose

End every task with a report that lets a human trust — or correctly distrust —
the work without re-deriving it. The report's defining feature is mandatory
disclosure of scope reductions: a permanent "Intentionally not done / omitted"
section means anything consciously skipped is stated with its reason and made
visible, never discovered later by surprise.

## Use When

- Use when: finishing a task or a phase of work.
- Use when: handing work off, opening a PR for review, or closing one out.
- Use when: asked "what did you actually do?" about completed work.
- Do NOT use when: giving a mid-task progress update — that is a lighter status
  note; closeout is terminal.
- Do NOT use when: shaping a commit or staged diff — that is
  `reviewable-diff-discipline` (its parked items feed this report).

## Inputs to Inspect

1. **The ORIGINAL request — re-read it.** The report is written against what
   was asked, not against what was done.
2. The actual diff and created files: `git status`, `git diff --stat`, the
   commit list.
3. Command outputs for every validation actually run (tests, builds, linters,
   validators).
4. Parked or out-of-scope items recorded during the work.
5. Approvals granted during the task, and their scope.

## Workflow

1. Re-read the original request; extract every explicit or implied deliverable
   into a checklist.
2. Mark each deliverable: done | partially done | intentionally not done |
   not applicable.
3. Everything not fully done goes into "Intentionally not done / omitted" with
   its reason — including quiet downgrades (asked for 10, delivered 6).
4. List files touched from git output, not from memory.
5. Record validation with the actual commands and their actual results —
   failures verbatim. Anything the change class expected but that was NOT run
   goes under "Skipped validation" with the reason.
6. State risks and known gaps.
7. Recommend the next action.
8. Run the Validation Checklist, then deliver the report as the final message
   (or as a file if asked), following
   [assets/closeout-template.md](assets/closeout-template.md).

## Output Format

All eight sections, in order, every time
(template: [assets/closeout-template.md](assets/closeout-template.md)):

```
CLOSEOUT REPORT
1. Summary — what changed and why
2. Intentionally not done / omitted — REQUIRED ALWAYS; "None." must be explicit
3. Files touched — exact paths, from git
4. Tests & validation run — command → actual result (failures verbatim)
5. Evidence — outputs, links, screenshots, PR
6. Risks & known gaps
7. Skipped validation — what wasn't run, and why
8. Next actions / handoff
```

## Validation Checklist

- [ ] Section 2 present even when empty — "None." written explicitly.
- [ ] Every deliverable from the ORIGINAL request accounted for in section 1
      or section 2.
- [ ] File list generated from git, not recalled.
- [ ] Every validation claim backed by a command actually run this session —
      no "tests pass" without output.
- [ ] Failures and skips reported verbatim, not smoothed over.
- [ ] No claim exceeds the evidence (e.g., "evals present and well-formed" is
      not "evals pass").

## Gotchas

- Silent scope reduction is the incident class this skill exists to prevent:
  partial delivery reported as complete because nothing forced the omission to
  be stated. Mandatory section 2 is that forcing function.
- Reports drift toward describing what WAS done; only auditing against the
  original request surfaces what wasn't.
- The classic honesty failures: "validated" with no runner, "tests pass"
  without running them, and failures summarized into vagueness.
- A closeout listing 40 files "for completeness" hides the 3 that matter —
  be exact but curated, and point to the PR/diff for the full list.

## Stop Conditions

- Asked to write a closeout claiming validation that did not happen → refuse;
  report the actual state (the skipped-validation section exists for exactly
  this).
- The actual diff contains changes the task cannot explain → stop; investigate
  or escalate before reporting.
- Unable to determine whether a requested deliverable was completed → say so
  explicitly in the report rather than guessing a status.

## Supporting Files

- [assets/closeout-template.md](assets/closeout-template.md) — copyable report
  template with all eight sections.
- `evals/evals.json` — trigger + behavior cases, including mandatory
  scope-reduction disclosure.
- Trigger is distinct within the pack (terminal reporting), so no
  trigger-evals file is required.
