# Elicitation Sheet

Detail for `requirements-gathering-facilitator`. Read on demand.

## Problem-vs-solution ladder

A stakeholder hands you a rung; climb up to the problem before designing.

```
"Add an export button"            (solution)
  ↑ why? → "So I can get the data out"
"Get the data into a spreadsheet"  (still a solution)
  ↑ why? → "To send my boss a weekly summary"
"Report progress to my boss weekly" (the job-to-be-done) ← design for THIS
```

Design at the highest rung that still names the user's real goal. A
scheduled emailed report may beat the export button they asked for.

## Question bank by discovery area

**Users & context**
- Who hits this problem? Who actually does the work (vs who asked)?
- Walk me through the last time this happened. What did you do?
- How do you cope today? (the current workaround)

**Problem & job**
- What can't you do today that you need to?
- What happens if we do nothing?
- Five-whys: why is that a problem? …and why does THAT matter?

**Scope & non-goals**
- What is explicitly out of scope / not this feature?
- What would make this feel over-built?
- Which edge cases matter; which are we choosing to ignore?

**Constraints**
- Deadlines, platforms, budgets?
- Legal/compliance/data-handling obligations?
- Dependencies on other teams/systems?

**Success**
- How will you know it worked? (observable outcome)
- What would you measure? (metric — accept "we don't know" over a
  fabricated number)
- What does merely "done" look like vs "successful"?

## Five-whys guardrail

Stop when you reach a root cause the team can act on, not when you hit
five literally. Don't drive to an abstraction so high it loses the
concrete need ("to delight users").

## Handling conflict

- Name the disagreement in the stakeholders' own terms.
- Separate must-have from preference for each side.
- Identify the decider; record the trade-off and evidence.
- Do NOT average positions or decide priority yourself — route it out.

## Requirements-brief template

```
Problem: <job-to-be-done>
Users/jobs: <who / context / requester-vs-user>
Current workaround: <...>
Requirements:
  [confirmed]  ...
  [assumed]    ...
  [to-confirm] ...
Non-goals: <...>
Constraints: <deadline / platform / compliance / deps>
Success: <observable outcome + metric?>
Conflicts: <named; decider>
Open questions (blocking spec): <q — owner>
Handoff → product-spec-writer
```
