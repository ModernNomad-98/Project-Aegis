# Skill-eval behavioral test procedure

This page is the repeatable procedure for testing whether a skill's own
`evals/evals.json` cases can actually be **satisfied by an agent that obeys
that skill**. It turns a one-off manual test into a method any maintainer — or
reviewing agent — can run again and check.

It is a **procedure, not a grant**. It authorizes no session, no provider call
and no spend. Executing it needs its own owner decision under the
[owner approval register](approvals/APPROVAL_REGISTER.md); read the register
before running anything.

**Reading key.** A **skill** is a `SKILL.md` instruction package under
`.claude/skills/`. An **eval case** is one entry in a skill's
`evals/evals.json`. An **assertion** is one expected behavior string in that
case's `expect.assertions`. The **answer key** is the skill's own `evals/`
directory. A **transcript** is the record of what the tested agent said and
did. A **fresh session** is an agent instance with no prior conversation and no
knowledge of the answer key. **D3** is the repository's structural-evaluation
decision in [the skill generation standard](skill-generation-standard.md).
The **Behavioral Eval Runner (BER)** is the shipped offline harness under
`tools/behavioral_eval_runner/`. `UNRUN` means no observation was recorded —
the honest state for a case nobody executed. A **PR** is a pull request, a
proposed repository change. **WP** means work package, a BER backlog
delivery unit.

## Why this exists

Structural validation proves an eval file **parses**. It cannot prove the case
is **satisfiable**. [PR #561](https://github.com/ModernNomad-98/Project-Aegis/pull/561)
found a case in `.claude/skills/scoped-approval-register/` that no
correct-behaving agent could pass: the case demanded a *write*, while its own
prompt supplied no quotable grantor wording, and the skill requires the
grantor's words and says to record nothing when scope is unresolved. An agent
obeying the skill failed that case; an agent inventing authority passed it.

That defect was **invisible to reading**. Every other defect that round was
caught by re-deriving a number; this one was caught by **running the skill**. It
was also the only such defect found, and the test that found it was never
repeated.

The shipped BER cannot repeat it either. Its generic commands are offline: it
inventories cases, prepares inputs, and grades **recorded** observations. Its
only concrete host adapter denies every session spawn, and its generic
`evals.json` execution path is unbuilt (backlog WP-2B-5). So the satisfiability
check below is, today, a **human-in-the-loop or agent-in-the-loop procedure**.

## When to use it

- A skill's eval case looks wrong, hollow, contradictory, or too strict.
- A skill's `SKILL.md` changed and its evals may now be stale.
- A skill was reported as "failing its evals" and you need to know whether the
  **skill**, the **case**, or the **agent** is at fault.
- You are reviewing a PR that edits `SKILL.md` or `evals/evals.json`.

Do **not** use it to produce a pass/fail score for the library. One skill, a few
cases, one run each is the intended unit. See
[the claim boundary](#the-claim-boundary).

## The procedure

### 1. Pin the revision and name the skill

Record the full commit identifier you are testing. A short hash is not enough.

```
git rev-parse HEAD
```

Pick **one** skill. Its `SKILL.md` is the instruction set under test; its
`evals/evals.json` is the answer key.

### 2. Read the answer key yourself

Read the skill's `evals/evals.json`. Choose **three** cases, one of each kind:

| Case kind | What it probes |
| --- | --- |
| happy path | the ordinary request the skill exists to serve |
| edge case | an ambiguous or adversarial variant |
| `should_not_do` (or refusal) | the shortcut the skill must refuse |

Take the case `prompt` **verbatim**. Do not improve it — a case is under test as
written, and rewriting it destroys the finding. Note each case's `id`, its
`expect.assertions`, and its `type`.

### 3. Build the tested agent's session

The tested agent gets:

- the skill's `SKILL.md`, and any `references/` file that `SKILL.md` tells a
  reader to consult;
- the case prompt, verbatim.

The tested agent must **not** get:

- the `evals/` directory, any `evals.json`, or `trigger-evals.json` — that is
  the answer key, and seeing it converts the test into a copy exercise;
- your own notes about what you expect to see.

**One case per fresh session.** A session that has already reasoned about one
case is context that biases the next one. This is the least negotiable rule in
the procedure.

### 4. Capture the transcript

Keep what the agent actually said, verbatim, including any file it wrote and
any question it asked. A **question is a legitimate output** — several skills
require one when scope is unresolved. Do not paraphrase it into an answer.

### 5. Grade with an independent grader

Use a **separate agent instance with fresh context**. It judges the transcript
against the chosen case's own `expect.assertions`, item by item, and must state
per assertion:

- **satisfied** — with the transcript line that satisfies it;
- **violated** — with the transcript line that violates it;
- **indeterminate** — the transcript does not show enough to decide.

An indeterminate assertion is reported as indeterminate, never as a pass. The
grader must not see your expectations, and must not be the agent under test.

### 6. Attribute the defect

For every violated assertion, decide **whose fault it is**:

| Attribution | Test |
| --- | --- |
| **skill defect** | an agent obeying `SKILL.md` provably cannot satisfy the assertion — the case demands something the skill forbids, or omits wording the skill requires |
| **case defect** | the assertion is unsatisfiable, self-contradictory, unjudgeable as written, or tests something the skill is not about |
| **agent defect** | the assertion is satisfiable by an obedient agent, and this agent simply failed |

Attribution is the finding. A case that only a disobedient agent can pass is a
**skill or case defect**, even though the obedient agent "failed" it.

**A transcript does not always settle this call, and this step must not pretend
that it does.** Step 5 already allows `indeterminate` for assertions the
transcript cannot settle, and the same limit applies here: the **case's own
framing** can decide whether a failure was the agent's fault or the case's. Two
signals that a violation is **not** the agent's fault, worth checking before
writing "agent defect":

- **The case's premise may not hold.** If the prompt asserts something about the
  register, dataset or system that is false *for the fixture the case depends
  on*, an obedient agent can behave correctly and still fail. Check the premise
  against the material the case actually supplies — a skill may ship its own
  fixture, in which case the real repository is **not** the reference.
- **The prompt's voice may hide whether wording is quotable.** The skill's rule
  is that **second-hand agreement is not quotable wording** — "the owner agreed"
  with no words, date or pointer leaves a new scope unsupported. So a
  first-person prompt ("I just approved it") supplies text that **can** be
  quoted, while a bare third-person one ("the owner approved it") usually does
  not, and may need the wording asked for. The same refusal is an **agent**
  defect under the first and a **case** defect under the second. Judge the
  prompt's voice, and check whether it carries words, a date or a pointer.

When either signal is present, report the attribution as **provisional**, say
which premise you could not settle, and leave the assertion's status open. A
wrong attribution is worse than an open one: it sends the maintainer to fix the
wrong artifact. This is not hypothetical — the first recorded run produced
exactly this ambiguity, and its own author made a false finding by checking a
case's premise against the wrong file. Both are recorded in the
[first run record](evidence/skill-eval-run-2026-09-30.md).

### 7. Record the evidence

Record: the pinned revision, the skill, the case `id`s, the prompts used
verbatim, the transcript, the per-assertion verdicts with their transcript
lines, the attribution, and any change proposed. Cite where the record lives.

**Also record the execution configuration. This is not optional.** A figure
without it cannot be checked, because nothing identifies what produced it:

| Field | Why it is required |
| --- | --- |
| **Agent and host identity** | which agent kind ran it, and whether a chat host or the offline BER drove the session |
| **Model name and version** | a per-case figure is a claim about *a model on a skill*; with no model recorded it is a claim about nothing |
| **Decoding parameters** | temperature, top-p, seed and reasoning effort, **where the host lets you set them** |
| **Date and pinned revision** | the revision alone is not enough, because the skill can change after the run |

**Where a session was driven in a chat host and no model is recoverable, say so
explicitly** — never silently omit the field — **and mark the run's
figures unreproducible.** A figure with no model attached is not evidence of a
rate.

**This page currently mandates an artifact it has no tooling to produce
reproducibly.** It "authorizes no session, no provider call and no spend", and
the shipped adapter "denies every session spawn"; so the host is a human or a
chat agent whose model and decode settings this procedure cannot capture from the
repository. Until that changes, expect step 7 to be only **partly** satisfiable,
and state which parts held. That partial answer is the honest output — not a
filled-in form.

**A figure derived from a single unrepeated session is not evidence of a rate.**
One run of one case is one observation. Report it as an observation, or do not
report it; never as a rate, and never as a score for the skill.

A new record under [evidence](evidence/README.md) is a **new tracked page**.
Under the [readability backlog](roadmaps/aegis-documentation-readability-backlog.md)
it joins the pending set and the stated totals move with it. Record that rather
than leaving the ledger wrong.

## Reporting a case as unsatisfiable

Report a case unsatisfiable **only** with proof attached: the prompt used, the
transcript of an obedient agent failing it, and the `SKILL.md` text that makes
success impossible. An intuition that a case "looks unfair" is not a finding.

Then fix the **right** thing. [PR #561](https://github.com/ModernNomad-98/Project-Aegis/pull/561)
replaced one unsatisfiable case with two honest ones — one where no wording
exists yet (the correct output is a question, and nothing is written), one where
wording exists (the correct output is an append). It also added the two
`SKILL.md` rules that had been missing, because the test had exposed them.

## The claim boundary

Per [the skill generation standard](skill-generation-standard.md) §6 and
decision D3, skill evals are **validated structurally only**. Report them as
**"present and well-formed, not as passing behavioral evaluations."**

So, after this procedure:

- You **may** say: "case `X` is unsatisfiable as written, here is the proof."
- You **may** say: "on revision `<sha>`, this agent failed assertion 3."
- You **must not** say: "the evals pass", "the skill is verified", or "coverage
  is measured" — unless an authorized execution run produced recorded
  observations for every case you are claiming, which this procedure does not.
- Cases you did not run stay **`UNRUN`**.

This procedure repairs or proves **cases**. It never becomes a quality score.

## Stop conditions

- **Asked to report an evals pass/fail rate from this procedure** → refuse: it
  runs a handful of cases in one revision, and §6/D3 forbids the claim.
- **Asked to run it against many skills or the full corpus** → stop; that is
  corpus execution, which the [BER backlog](roadmaps/behavioral-eval-runner-backlog.md)
  gates behind WP-2B-4 and WP-2B-5.
- **No authority for a live session or provider call** → stop and ask; neither
  this page nor the standing delivery grants authorize execution.
- **Asked to skip the independent grader** → refuse; a single agent judging its
  own transcript is not the test, and the #561 finding depended on the split.
- **The tested agent was shown the answer key** → discard the run; it is not
  evidence.

## Provenance

Transcribed from the documented test in
[PR #561](https://github.com/ModernNomad-98/Project-Aegis/pull/561)'s body,
which found the unsatisfiable case in
`.claude/skills/scoped-approval-register/evals/evals.json` on 2026-09-29 and
repaired it in merge commit `410b90aa`. The protocol there was: a fresh agent
given only the skill's `SKILL.md`; three real prompts from that skill's own
evals; a second, independent agent grading the transcript against the eval's
own assertions and naming defects in the **skill** where the skill was at fault.
