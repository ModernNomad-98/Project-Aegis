# Something's broken — describe the symptom, not the cause

*This path names who acts and in what order — each skill owns its own how.*

**Who this is for:** something in your app is wrong and you don't know why.

**How to run it:** in your agent tool (Claude Code, Codex command-line
interface (CLI), or any Agent Skills tool),
describe the symptom in plain words — "users can see someone else's data", "tests fail only
in continuous integration (CI), the automated checks on each change". For example,
paste: **"In this product repository, users see an error when saving a job. Help
me reproduce it, find the cause from evidence, and verify one fix."** Advisory
specialists can be selected automatically; specialists marked
**manual-only** require you to explicitly invoke them by name before execution.
For an unknown cause, say: **"Use the systematic-debugger skill on this
symptom; reproduce it before changing anything."**
The table maps symptoms to owners. Auto-selection quality varies by tool; see
the README's [tools section](../../README.md#using-aegis-with-codex-cli-and-other-agent-skills-tools).

## The symptom map

| The symptom, in plain words | Who owns it |
|---|---|
| "Users can see data that isn't theirs." | [`tenant-isolation-reviewer`](../../.claude/skills/tenant-isolation-reviewer/SKILL.md) — finds every surface where one customer's data can reach another. |
| "I removed someone / revoked their access / they logged out — and the old access still works." Or: "they changed plans and still see the old tier." | [`authority-invalidation-architect`](../../.claude/skills/authority-invalidation-architect/SKILL.md) — finds every place the old access survives and proves the change actually took effect. |
| "One query or page is slow." / "It gets slower as data grows." / "I don't know where the time goes." | [`query-plan-reader`](../../.claude/skills/query-plan-reader/SKILL.md) **manual-only** for the slow query · [`n-plus-one-detector`](../../.claude/skills/n-plus-one-detector/SKILL.md) **manual-only** for slows-with-more-data · [`frontend-perf-engineer`](../../.claude/skills/frontend-perf-engineer/SKILL.md) for a slow page · [`profiling-methodology-designer`](../../.claude/skills/profiling-methodology-designer/SKILL.md) when nobody knows where the time goes. |
| "Tests fail randomly / only in CI." | [`flaky-test-detective`](../../.claude/skills/flaky-test-detective/SKILL.md) **manual-only** — separates flaky from genuinely broken, with the evidence. |
| "Production is down right now." | Alert the human on-call owner and follow your **existing** incident runbook. If the cause is unknown, explicitly invoke [`systematic-debugger`](../../.claude/skills/systematic-debugger/SKILL.md) **manual-only** for diagnosis within the responder's authority. |
| "It fails and none of the above fits." | [`systematic-debugger`](../../.claude/skills/systematic-debugger/SKILL.md) **manual-only** — the general case: drives from symptom to root cause instead of guessing. |

For a live outage, [`incident-response-runbook`](../../.claude/skills/incident-response-runbook/SKILL.md)
is a skill for *authoring or improving* the procedure after the incident; it
does not run the live response. [`rollback-runbook-author`](../../.claude/skills/rollback-runbook-author/SKILL.md)
prepares the next release's rollback plan; it does not execute a live rollback.

## After the diagnosis

Whichever specialist takes it, close with the evidence-backed diagnosis and
a clear next action. Some specialists only measure or design a response;
their output is a plan or finding, not an applied fix. When an authorized
fix is actually applied, verify its effect and record the result instead of
assuming "should be fine now". If the diagnosis reveals a design gap or
security hole, name the owning follow-up skill and hand it off instead of
stretching a debugging session into a redesign.
