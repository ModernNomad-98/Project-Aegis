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

## Atomic discovery cards

INTERNAL checklist. Select ONE uncovered card per turn, ask its ONE question in
plain language, and STOP for the answer. Never display this list as a
questionnaire, a numbered menu, or a "pick any" batch — the coverage-area grouping
is not a batch to send. Each card carries one Target (one independently answerable
information or decision target) and one quoted Ask (one atomic question).

**Users & context**

- Target: current operator
  Ask: "Who usually does this work today?"
- Target: requester vs user
  Ask: "Who asked for this — the same people who will use it, or someone else?"
- Target: current workaround
  Ask: "How do you handle this problem today?"

**Problem & job**

- Target: unmet need
  Ask: "What can't you do today that you need to?"
- Target: consequence of inaction
  Ask: "What happens if this stays exactly as it is?"
- Target: root cause (one why)
  Ask: "Why is that a problem for you?"

**Scope & non-goals**

- Target: explicit non-goal
  Ask: "What should the first version deliberately NOT do?"
- Target: over-build signal
  Ask: "What would make this feel over-built?"
- Target: edge-case priority
  Ask: "Which single edge case worries you most?"

**Constraints**

- Target: deadline
  Ask: "Is there a deadline for the first version?"
- Target: budget
  Ask: "Is there a budget limit I should account for?"
- Target: required devices/platform
  Ask: "Which devices must the first version work on?"

**Compliance & data handling**

- Target: compliance obligation
  Ask: "Are there legal or privacy rules the first version must follow?"
- Target: sensitive data
  Ask: "Does this handle any personal or sensitive data?"

**Dependencies**

- Target: external dependency
  Ask: "Does this depend on another system or team?"

**Success & measurement**

- Target: observable success
  Ask: "What would you observe that tells you this worked?"
- Target: success metric
  Ask: "Is there a number you would measure to know it worked?"
- Target: done vs successful
  Ask: "What does merely 'done' look like?"

## The observed compound failure and its decomposition

A live Stage 1 turn bundled FOUR targets into one turn. It is recorded ONLY as an
INVALID example, never reusable as a card:

INVALID — four targets (current process + actor + recent incident + failure point):

"Walk me through the booking process, include who does each step, and tell me about a recent double booking and where it went wrong."

There is no lone "and" to ban and no second question mark, yet a complete answer
needs four independent things — proof that counting punctuation is not enough.
Decompose across separate turns, one atomic target each:

- Turn A: "What happens today when a patient books an appointment?"  -> STOP
- Turn B: "Who usually records the appointment in the paper diary?"  -> STOP
- Turn C: "What happened the most recent time a double booking occurred?"  -> STOP
- Turn D: "Where in the booking process did that double booking occur?"  -> STOP

These four are illustrative, not a mandatory script; the rule is one atomic target
per turn.

## Five-whys guardrail

Five-whys obeys one target per turn: ask ONE "why?" question, wait for the answer,
then decide on a LATER turn whether another "why?" is warranted — never stack
several "why?" questions into one turn. Stop when you reach a root cause the team
can act on, not when you hit five literally. Don't drive to an abstraction so high
it loses the concrete need ("to delight users").

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
