# Elicitation Sheet

Detail for `requirements-gathering-facilitator`. Read on demand.

## How to use this sheet (INTERNAL CHECKLIST — never a questionnaire)

Everything below — the ladder, the question bank, the five-whys, and the conflict
guide — is an INTERNAL CHECKLIST for the facilitator. It is NEVER displayed to the
stakeholder as a questionnaire, a numbered list, or a "pick any" menu. The
headings and bullet groups are discovery **coverage areas**, not a user-facing
batch to send at once.

Each interactive turn:

1. select the single highest-value UNANSWERED item from the checklist;
2. ask exactly ONE plain-language question (one information or decision target);
3. STOP and wait for the answer — nothing else that turn;
4. update the internal checklist with the answer (mark it covered; note new gaps);
5. repeat on a LATER turn with the next single question.

Only once no spec-blocking coverage area is unresolved do you assemble the FINAL
requirements brief (template below).

**Valid — one question, one target:**

- "Who handles appointment bookings today?"
- "Should patients be able to book appointments themselves in the first version?"
  (a short option list may clarify the one question — staff-only, self-serve, or
  both — without adding a second requested answer)

**Invalid — a question dump or a compound question (never do this):**

- Presenting "Users & context", "Problem & job", "Scope & non-goals",
  "Constraints", and "Success" as numbered groups and saying "take them in any
  order."
- "Who handles bookings, how many staff use the diary, and how many therapists do
  you schedule?" (three targets welded into one turn).

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

INTERNAL checklist — select ONE unanswered item and ask ONE question per turn;
never display this list as a questionnaire. The groups are coverage areas.

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
