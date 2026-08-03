---
name: _template
description: 'TEMPLATE ONLY — not a real skill and never invoked. Copy this directory to .claude/skills/<your-skill-name>/, rename it, set `name` to match the new directory, and rewrite every section against docs/skill-generation-standard.md. Write the real description to the Portability contract: front-load what the skill DOES in the first ~90 characters, keep it ONE strict-YAML-valid line (single-quote it like this one and double internal apostrophes, ''like this''), parsed value under 1024 characters.'
# disable-model-invocation: true   # uncomment if the real skill has side effects — the
#   description must then START with the exact 32-char sentinel (trailing space included):
#   MANUAL-ONLY; never auto-invoke.
#   (validator-enforced; see the Portability contract in the standard)
#   TWO bounded exceptions (standard §5). Exception 1 — approved doc/state write: an
#   auto-invocable skill MAY create or append to a non-executable documentation or
#   project-state file in the working tree, but only as a second-phase action — show
#   the exact target path and exact content or diff, receive explicit, content-
#   specific, single-use approval in the current session, and write exactly what was
#   approved. Overwrite/delete/rename, source code, executable/config files, agent-
#   instruction files, security/identity/policy/CI files, secrets, network calls,
#   external mutation, spending, and deployment are NOT covered — those stay manual-
#   only. Exception 2 — TALI: a separately classified, separately activated execution
#   route confined to ordinary approved source/test files; behavior-based, no skill is
#   permanently eligible, and NO existing skill receives TALI authority by default — a
#   side-effecting skill still needs disable-model-invocation: true unless a specific
#   route is classified and activated under §5. This template activates neither.
# allowed-tools: Read, Grep, Glob  # optional & narrow only; omit to inherit defaults
---

# _template (reference skill)

> **This is a template, not a shipped skill.** It lives at `.claude/skills/_template/`
> and is deliberately ignored by `scripts/validate-skills.py`. Do not invoke it.
> To create a skill: copy this directory, rename it, and fill in every section below.
> Full rules: [docs/skill-generation-standard.md](../../../docs/skill-generation-standard.md).

## Purpose

State, in one paragraph, what the real skill produces and the value it delivers.
Example: "Produces a normalized spreadsheet and summary tab from a messy export."

## Use When

- Use when: the user's request matches the concrete trigger the skill is built for.
- Use when: an adjacent-but-in-scope variation of that request appears.
- Do NOT use when: the request looks similar but belongs to another skill or a
  plain response — name that case explicitly so the model doesn't over-trigger.

## Inputs to Inspect

- The repo files, docs, code, tests, and prior artifacts the real skill must read
  before acting. List them concretely so context precedes action.

## Workflow

1. Gather and validate the inputs the skill needs (see **Inputs to Inspect**).
2. Perform the core transformation, reading `references/` detail files on demand.
3. Produce the deliverable exactly as specified in **Output Format**.
4. Run the **Validation Checklist** before declaring done.

## Output Format

Describe the exact deliverable: file path(s) and naming, report structure, or data
schema. Be specific enough that two runs produce consistent shapes.

## Validation Checklist

- [ ] Output matches the shape declared above.
- [ ] No **Stop Conditions** were silently bypassed.
- [ ] Any side-effecting step was gated behind explicit human confirmation. Under
      standard §5, the write an auto-invocable skill may make by default (Exception 1)
      is the approved doc/state append: create/append a non-executable documentation
      or project-state file, AFTER showing the exact path + content and receiving
      explicit, content-specific, single-use approval — path and content unchanged
      between approval and write. Autonomous source/test editing is NOT implied here;
      it exists only inside a separately classified and activated TALI route
      (Exception 2, §5), never by default.
- [ ] Any autonomous TALI validation command produced NO unapproved repository
      working-tree output (no cache/coverage/build/generated/ignored/temporary/report/
      snapshot files outside the approved set), and any host-managed scratch stayed
      outside the repository and was removed before closeout.

## Gotchas

- Keep `SKILL.md` under 500 lines; push detail into `references/`.
- Keep the frontmatter `description` trigger-oriented and under 1024 chars.
- Directory name and frontmatter `name` must stay identical.

## Stop Conditions

- Stop and ask if required input is missing or the request is ambiguous.
- Stop and confirm before any irreversible or destructive action (delete, deploy,
  overwrite, spend).
- Before a documentation/project-state append under the standard-§5 approved-write
  exception (Exception 1): show the exact target path and exact content, wait for the
  explicit content-specific yes, and write only what was approved. A declined,
  ambiguous, or changed approval means NO write.
- Every side effect outside Exception 1 remains manual-only
  (`disable-model-invocation: true`) unless it is an ordinary approved source/test edit
  inside a separately classified and separately activated TALI route with every §5
  precondition satisfied. Delete or rename; Git mutation; package installation; network,
  API, webhook, or MCP access; database write or seeding; deployment, provisioning,
  spending, or live-state mutation; protected-surface change; security-control change;
  governance change; architecture change; and every other §5 FORBIDDEN UNDER TALI class
  remain forbidden and must hand off to the owning policy. A generic approval does not
  convert any forbidden operation into a TALI operation. This template activates no route.

## Supporting Files

- `evals/evals.json` — required for every real skill; the copy in this template
  directory ([evals/evals.json](evals/evals.json)) is the canonical starting point.
- `evals/trigger-evals.json` — add when the skill's trigger overlaps another skill.
- `references/`, `assets/`, `scripts/` — add only when they reduce errors (progressive
  disclosure). Use "None" here if the skill is self-contained.
