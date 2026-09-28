# Acceptance criteria review sheet

Detail for `acceptance-criteria-reviewer`. Read on demand from the workflow.

## 1. The three-part testability check

A criterion is TESTABLE only when a tester who did not write it can answer
all three questions without asking anyone:

| Part | Question | Missing looks like |
| --- | --- | --- |
| Observable outcome | What will I see, query or measure? | "the data is handled correctly" |
| Pass or fail threshold | Which value, state or count means pass? | "quickly", "most users", "rarely" |
| Evidence | What artifact proves the result? | no test, log, screenshot, metric or record could show it |

Verdict rules:

- All three present → **TESTABLE**; name the evidence.
- Intent clear, one or more parts missing or vague → **NEEDS-REWRITE**; give
  a suggested rewrite.
- Intent itself unclear, or the text describes design rather than behavior →
  **UNTESTABLE**; give one unblocking question.

## 2. Vague-word catalog

| Vague wording | Why it fails | Rewrite pattern (placeholders stay visible) |
| --- | --- | --- |
| fast, quick, responsive, performant | no threshold | "<operation> completes within `<? ms>` at `<percentile>` for `<data size>`" |
| works, functions, handles, supports | no observable outcome | "given `<state>`, when `<action>`, then `<visible result>`" |
| user-friendly, intuitive, easy, clean | subjective | "a first-time `<role>` completes `<task>` in `<? steps / ? minutes>` without help" or a named usability check |
| secure, safe, protected | no attacker or rule named | "a `<role>` without `<permission>` receives `<error / 404 not found>` and no data" |
| appropriate, correct, proper, valid | rule not stated | name the rule or reference where it is written |
| as expected, same as today, as before | expectation not written down | quote or link the expected behavior |
| etc., and so on, all relevant | open-ended list | enumerate the items or ask which are in scope |
| should, may, ideally | optional or required? | ask whether it is a requirement; required criteria use "must" |
| rarely, most, usually, some | no count | "`<? %>` of `<population>` over `<window>`" |

Never replace a placeholder with a guessed value. A number the owner did not
give is a product decision.

## 3. Completeness classes

Check the whole set against each class. A class with no criterion becomes a
GAP with one question; it is never written as an agreed criterion.

| Class | Prompt questions |
| --- | --- |
| Negative | What happens with invalid input, missing data, an expired link or token, a duplicate submission, or a conflicting edit? |
| Boundary | What happens at empty, one, the maximum, and one past the maximum (size, count, length, date range)? |
| Permission | What does a signed-out user, a user with the wrong role, and a user from another tenant see or get? |
| Error and recovery | What does the user see when a dependency fails, and can they retry without losing work? |
| State and timing | What happens out of order, concurrently, or after a partial failure? |

Cross-tenant and wrong-role gaps that need a dedicated security test suite
are noted for `multi-tenant-security-tester` *(manual-only)*; a person must
name it to invoke it.

## 4. Worked examples

**NEEDS-REWRITE.** AC3 "The export should load fast."
Missing threshold and evidence. Suggested rewrite (author to accept): "Given
a workspace with `<? rows>`, when an owner requests a CSV (comma-separated values) export, then the
file download starts within `<? s>` at the 95th percentile, measured by
`<test or metric>`." Question: what size and time does the owner commit to?

**TESTABLE.** AC1 "Given an invited user with an unexpired link, when they
set a password, then they land on the workspace dashboard and the invite is
marked accepted." Evidence: an integration or end-to-end test asserting the
redirect and the invite record state.

**UNTESTABLE.** AC5 "The system uses a background queue for exports."
Design, not behavior. Question: what should the user observe (for example,
"the page stays usable while the export runs")?

**GAP.** No criterion covers an expired invite link. Question: should an
expired link show an error with a "request a new invite" action, or
something else?

**Contradiction.** AC2 "Only owners can export" vs AC6 "Admins can export
billing data." One question: may admins export billing data, and if so,
is AC2 limited to non-billing exports?
