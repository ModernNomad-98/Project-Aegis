---
name: source-of-truth-reconciler
description: Resolve conflicts between current user instructions, repo docs, code, tests, PR history, and older chat or memory context before acting on any of them. Use when two sources disagree (a doc says X, the code does Y), when instructions reference repo state that no longer exists, when planning docs overlap or contradict, or when remembered context conflicts with what the repo actually contains. Produces a precedence-ordered reconciliation with cited evidence (file:line) and surfaces every assumption explicitly — never silently picks a side and never silently obeys a stale instruction.
---

# Source-of-Truth Reconciler

## Purpose

Turn "the sources disagree" into a recorded, evidence-backed decision. This
skill enumerates the conflicting claims, classifies each conflict, applies a
declared precedence order, and outputs a reconciliation report that cites its
evidence — so downstream work builds on one resolved truth instead of a quiet
guess. It also carries the no-silent-assumptions rule: every assumption made
while reconciling is stated with its risk.

## Use When

- Use when: a doc contradicts the code or tests.
- Use when: the user's instruction references state that no longer exists
  (deleted branch, moved file, superseded plan).
- Use when: two planning docs cover the same ground with different answers.
- Use when: recalled memory or prior-chat context conflicts with current repo state.
- Do NOT use when: nothing conflicts — plain reading needs no reconciliation.
- Do NOT use when: the question is whether a risky action may proceed — that is
  `human-approval-boundary`.
- Do NOT use when: starting a task and loading context — that is
  `agent-startup-context-gate` (it may HAND OFF here when it finds a conflict).

## Inputs to Inspect

1. The conflicting claims themselves — quote each verbatim with its anchor
   (file:line, PR number, message).
2. Source metadata: dates, canonical/historical markers, reconciliation records.
3. Actual repo state: the code, tests, and migrations as they are now.
4. Merged PR and commit history, for claims about what happened.
5. Any repo-designated precedence policy — it overrides the default order below.

## Workflow

1. **Enumerate claims verbatim**, each with an evidence anchor.
2. **Tag each source:** type, date, and status — canonical | current |
   historical | generated | memory.
3. **Classify each conflict:** an IS-question (what does the system actually
   do?) or a SHOULD-question (what is intended/required?).
4. **Apply precedence** (default; a repo policy overrides it):
   1. Explicit current-session user instruction — unless it rests on stale
      facts (surface and confirm first) or crosses a safety boundary (route to
      `human-approval-boundary`).
   2. For IS-questions: actual repo state — code, tests, migrations.
   3. Docs marked canonical / current reconciliation records — for
      SHOULD-questions these outrank code (intent-vs-implementation drift is a
      finding to report, not a tie).
   4. Merged PR and commit history.
   5. Historical or superseded docs.
   6. Prior chat memory / recalled context.
5. **Record a verdict per conflict:** winner, precedence rule applied, evidence.
6. **Surface every assumption** made along the way, each with risk-if-wrong.
7. **Propose corrections** to the losing stale sources as follow-up work — do
   not silently edit them as a side effect of reconciling.

## Output Format

```
RECONCILIATION REPORT
Conflicts:
  C1: <claim A (source:line)> vs <claim B (source:line)>
      Type: IS | SHOULD
      Verdict: <winner> — precedence rule <n>, because <reason>
Assumptions surfaced: <each with risk-if-wrong>
Stale sources to fix: <file → proposed correction (follow-up, not done here)>
Blocked: <conflicts with no winner — questions for the human>
```

## Validation Checklist

- [ ] Every claim quoted with a file:line / PR / message anchor.
- [ ] Every verdict names the precedence rule it applied.
- [ ] IS vs SHOULD recorded per conflict.
- [ ] No stale source silently edited; fixes proposed as follow-ups.
- [ ] Every assumption listed with its risk-if-wrong.
- [ ] Security- or data-affecting conflicts routed to `human-approval-boundary`,
      not decided by precedence.

## Gotchas

- Recently modified is not canonical — a stale doc can carry a fresh timestamp
  from an unrelated touch-up.
- The user's instruction can itself be stale (built on a view of the repo that
  has moved on). Surfacing that and confirming beats both silently obeying and
  silently overriding.
- Docs describing DESIRED state read like descriptions of CURRENT state;
  misclassifying SHOULD as IS inverts the verdict.
- Two docs may both claim to be canonical — that is a conflict to escalate, not
  one to resolve by picking the newer file.
- Generated artifacts (lockfiles, build output, generated API docs) mirror
  their inputs; citing them as an independent source double-counts one claim.

## Stop Conditions

- The conflict affects security, data handling, tenant isolation, or
  destructive behavior → stop; hand to `human-approval-boundary`.
- Two sources of equal current standing disagree and no repo precedence policy
  exists → stop and ask.
- Resolution would require rewriting docs or history beyond the current task's
  scope → propose it, don't do it.

## Supporting Files

- [references/conflict-resolution-examples.md](references/conflict-resolution-examples.md) —
  worked examples: doc-vs-code, stale-branch instruction, dueling canonical docs.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `agent-startup-context-gate`
  and `human-approval-boundary`.
