# Task plan template

The plan template and size rules for the owning
[AI Task Decomposer](../SKILL.md). A pull request (PR) proposes one
repository change for review; an application programming interface (API) is
the interface other code calls; UI means user interface. A spike is a short,
time-boxed investigation whose only output is an answer. A feature flag is a
switch that turns code on or off without a new release.

## Size rules: a task is ready when

1. **One intent.** The task can be described in one sentence without "and"
   joining two unrelated changes.
2. **One reviewable PR.** One reviewer, or one reviewer specialty, can review
   it in one sitting. If it needs a database reviewer, a security reviewer and
   a front-end reviewer at once, split it.
3. **Checkable on its own.** Its acceptance criterion can be proven by
   evidence produced by this task alone (a test, a command output, a
   screenshot, a query result), without waiting for a later task.
4. **Mergeable on its own.** Merging it leaves the product working, behind a
   feature flag if the behavior is not ready for users.
5. **Honest about what it touches.** Its likely files or layers are named and
   marked verified (found in the repository) or assumed.

## Split-again checks

Split a task again when any of these is true:

- It changes the database schema and the code that depends on the change
  (plan the additive schema change first, then the code, then any removal).
- It spans the schema, the API and the UI together.
- Its acceptance criterion needs the word "and" to join two outcomes.
- It mixes a refactor with a behavior change.
- It crosses a human-approval boundary and also carries unrelated work.
- Its evidence would only exist after another task lands.

Stop splitting when each task passes the size rules; many one-line tasks are
as hard to review as one oversized one.

## Human-approval boundaries to flag

Flag a task for `human-approval-boundary` when it will: change the schema or
run a destructive migration; change row-level security, access or other
security policy; touch production data; add, rotate or move secrets; deploy
or release; change billing; rewrite git history; or refactor broadly across
many files. The flag is a planning note; the approval itself is requested
when the task starts.

## Template

```
TASK PLAN — <goal / epic / spec id>
Source:        <path, ticket id or message; goal quoted>
Goal:          <one sentence>
Done when:     <observable end state for the whole goal>
Layers:        <layer — likely files/dirs — verified | assumed>
Summary:       <n> tasks · <n> spikes · <n> approval-flagged · <n> owner questions
Tasks (in order):
  T<n> <short title>
       Intent:      <one intent>
       Done when:   <observable acceptance criterion>
       Evidence:    <test / command output / screenshot / query that proves it>
       Touches:     <likely files or layers — verified | assumed>
       Class:       <provisional change class> (confirm with change-classification-gate)
       Risks:       <known risks | none known>
       Depends on:  <T ids | none>
       Approval:    <boundary crossed → human-approval-boundary | none>
  S<n> <spike title> — question: <what it answers> — time box: <limit> —
       output: <the answer, not shipped code> — unblocks: <T ids>
Owner questions (ranked, blocking first):
  Q<n> <question> — unblocks <T/S ids>
Not planned here: <gaps routed elsewhere | none>
Next:          first ready task → change-classification-gate when work starts
Not changed:   no task started, no ticket created, no file edited.
```

## Worked example (shortened)

Goal: "Add team invitations: an owner invites a teammate by email, the invite
expires, and the owner picks the teammate's role."

```
T1 Add the invitations table (additive migration)
   Done when:  migration applies and rolls back cleanly on a copy of the schema
   Evidence:   migration up/down output; schema diff
   Class:      schema/migration — Approval: schema change → human-approval-boundary
T2 Create-invitation API with role choice (owner only)
   Done when:  owner gets 201 with an invite record; member gets 403
   Evidence:   API tests for owner, member and other-tenant caller
   Class:      backend/API — Depends on: T1
T3 Send the invitation email with a signed, expiring link
   Done when:  a test inbox receives one email whose link expires at the set time
   Evidence:   email integration test; expiry test with a controlled clock
   Class:      backend/API — Depends on: T2
T4 Accept-invitation API (expired and reused links rejected)
   Done when:  a valid link adds the member with the chosen role; expired or
               reused links return an error and add no one
   Evidence:   API tests for valid, expired and reused links
   Class:      backend/API — Depends on: T3
T5 Invite form in team settings, behind a feature flag
   Done when:  with the flag on, an owner can send an invite from settings;
               with it off, the form is absent
   Evidence:   UI test for both flag states; screenshot
   Class:      UI — Depends on: T2
Q1 How long should an invitation stay valid? — unblocks T3, T4
```

The accept page in the UI is a sixth task, left out here for length. The
expiry length is left as an owner question, not picked by the planner.
