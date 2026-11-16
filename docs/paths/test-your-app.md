# Test your app and find the bugs

*This path names who acts and in what order — each skill owns its own how.*

**Who this is for:** you have a running app (or a build you can run) and you
want to know what actually breaks before real users find out. Maybe an
artificial intelligence (AI) coding tool wrote much of the app; maybe you are
the engineer. You do not need to know what any of the skill names below mean;
each one is a specialist that explains itself when it runs.

The door is `qa-orchestrator` (the QA conductor): you say **help me test my
app**, it picks **one** QA play, names every skill it will use before starting,
and leaves one plain-language report. A QA pass is not a fix pass — it finds
and classifies defects; fixes are separate work.

**Before you start — install the QA skills.** The
[starter package](../consumer-starter-package.md) does **not** include
`qa-orchestrator` and installs **no** manual-only skill. This is a two-stage
copy using the selected-skills allow-list route in
[Using the skills in your own project](../../README.md#using-the-skills-in-your-own-project):
1) copy `qa-orchestrator` itself; 2) invoke it, and it names the play order
before starting, so you copy only the play skills that order reports. That
route is also how you extend the starter package. Check `.claude/skills/<name>/`
(Claude Code startup mode), or `.agents/skills/<name>/` and
`~/.agents/skills/<name>/` (native Agent Skills mode), for each skill. When a
play step needs a skill you have not installed, record the extension as a
DECISION in `docs/project-state.md` (the starter package section 4.2 rule)
before the step runs; `docs/consumer-install-record.md` is the install receipt
written by the starter install, not a hand-edit log.

**How to run it:** open your project in your agent tool (Claude Code, OpenAI's
Codex command-line interface (CLI), or any Agent Skills tool) and say a plain
sentence — **Help me test my app** — or name `qa-orchestrator`. For most QA
steps the named skill selects itself. A **manual-only** step needs a valid
recorded standing trigger-scoped override covering that exact step; without
one, **you** name the exact skill and invoke it. The conductor never runs or
chains a manual-only skill. (Auto-selection quality varies by tool — see the README's
[tools section](../../README.md#using-aegis-with-codex-cli-and-other-agent-skills-tools).)

## The order

1. **Open the QA door —
   [`qa-orchestrator`](../../.claude/skills/qa-orchestrator/SKILL.md).**
   It asks at most four plain questions, chooses one play, and prints the
   order, which skills are installed, which are manual-only, and which steps
   are conditional before anything runs. Say **play A** if you want the
   find-bugs-now route explicitly.

2. **Play A — find bugs now (a running app).** The shipped order starts with
   production safety and ends with triage.

   - **On a deployed production app only:**
     [`production-safe-smoke-tester`](../../.claude/skills/production-safe-smoke-tester/SKILL.md)
     first **designs** the read-only probes; the human/operational owner executes
     them. Live status goes to the manual-only
     [`observability-operator`](../../.claude/skills/observability-operator/SKILL.md).
     The conductor never executes production probes, never writes, and never uses
     real customer tenants.
   - [`exploratory-charter-designer`](../../.claude/skills/exploratory-charter-designer/SKILL.md)
     is optional (time-boxed charters).
   - [`clickthrough-test-engineer`](../../.claude/skills/clickthrough-test-engineer/SKILL.md)
     is **CONDITIONAL**: it applies only when it is installed, authorized under
     your recorded manual-only policy, **and** the host can drive a browser.
     If any of those three conditions does not hold, the play uses its
     **written-walkthrough route** instead:
     [`manual-test-case-creator`](../../.claude/skills/manual-test-case-creator/SKILL.md)
     writes the cases, a person runs the steps, and
     [`defect-triage-facilitator`](../../.claude/skills/defect-triage-facilitator/SKILL.md)
     triages. That is the play's route, not a substitution and not a skipped
     check; the report states which route ran and what the human route could not
     cover. If `manual-test-case-creator` itself is absent (an applying,
     non-conditional step), or no person can run the generated cases, the play
     **stops**, names the exact skill or the gap, gives the selected-skills copy
     route, and hands the copy plus the extension decision to you (the human).
   - [`defect-triage-facilitator`](../../.claude/skills/defect-triage-facilitator/SKILL.md)
     closes the play by classifying the findings (residuals need a recorded
     disposition and follow-up identifier).

3. **Play C — check before release (changed routes and release readiness).**
   [`risk-tiered-validation-selector`](../../.claude/skills/risk-tiered-validation-selector/SKILL.md)
   selects depth only and never executes.
   [`sharded-validation-with-resume`](../../.claude/skills/sharded-validation-with-resume/SKILL.md)
   applies only when a sharded suite exists; it designs the shard map/resume
   machinery and never executes. Run the selected validation tier through the
   project's own execution owner — when that route is the manual-only
   [`local-ci-mirror-preflight`](../../.claude/skills/local-ci-mirror-preflight/SKILL.md),
   the conductor lists it as the execution owner and hands it to you; it never
   auto-runs or chains it. The changed-routes
   [`clickthrough-test-engineer`](../../.claude/skills/clickthrough-test-engineer/SKILL.md)
   step is **CONDITIONAL** with the same three conditions; when they fail, the
   same **written-walkthrough route** applies (or the play stops if
   `manual-test-case-creator` is absent or no person can run the cases), exactly
   as in Play A. Then
   [`defect-triage-facilitator`](../../.claude/skills/defect-triage-facilitator/SKILL.md)
   classifies findings and
   [`release-readiness-reviewer`](../../.claude/skills/release-readiness-reviewer/SKILL.md)
   gates on evidence: with no CI evidence it reports the CI dimension
   **MISSING** and cannot claim a pass. A direct **is this ready to ship?**
   request routes to `release-readiness-reviewer`, not a conductor play.

4. **Read the report.** One plain-language report lists what was tested, what
   was not and why, the route taken (clickthrough or written-walkthrough) and
   what the human route could not cover, defects classed
   blocking/residual/nit, and the single most important next action. Only when
   `docs/project-state.md` exists **and you have explicitly authorized
   documentation recording** (or given a content-specific single-use approval)
   does the conductor append **one** `STATE SNAPSHOT` row (following the
   installed template schema). No fixes
   happen during the pass.

The three clickthrough conditions are always stated explicitly: **installed**,
**authorized under your recorded manual-only policy** (a recorded standing
trigger-scoped override, or you invoking the exact skill yourself), and
**browser-capable host**. There is no complete browser pass promised on either
route; the conductor reports which route ran.

## What this is — and isn't

This is a guided order, not a guarantee. On a fresh starter package the
conductor and the play's auto skills must first be copied through the
selected-skills route; that is why the page starts with install, not with a
pass.

It is **not** a complete browser regression suite: the starter package installs
no manual-only skill, so when the clickthrough conditions fail, the route is
the written-walkthrough route (or a stop if `manual-test-case-creator` is
missing **or no person can run the generated cases**) — never a claim that the
browser was tested. There is no **always
stops at clickthrough** rule: a conditional step whose condition fails is
routed, not stopped. Manual-only steps are never auto-applied, chained, or
simulated. There is no host-support claim and no readiness claim; readiness
belongs to `release-readiness-reviewer` on evidence. The evidence is the
report; the state entry, when the file exists, is only the pointer.
