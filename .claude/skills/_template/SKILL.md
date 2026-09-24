---
name: _template
description: 'TEMPLATE ONLY — not a real skill and never invoked. Copy this directory to .claude/skills/<your-skill-name>/, rename it, set `name` to match the new directory, and rewrite every section against docs/skill-generation-standard.md. Write the real description to the Portability contract: front-load what the skill DOES in the first ~90 characters, keep it ONE strict-YAML-valid line (single-quote it like this one and double internal apostrophes, ''like this''), parsed value under 1024 characters.'
# disable-model-invocation: true   # uncomment if the real skill has side effects — the
#   description must then START with the exact 32-char sentinel (trailing space included):
#   MANUAL-ONLY; never auto-invoke.
#   (validator-enforced; see the Portability contract in the standard)
#   TWO bounded exceptions (standard §5). Exception 1 permits exact authorized
#   non-executable documentation/project-state create or append, immutable
#   transcription of evidenced human decisions, and only six named state-
#   projection refreshes. Show the exact path/content and honor applicable
#   current-session authority; seek content-specific approval only when missing.
#   The exclusions in §5 remain manual-only. Exception 2 — TALI: a separately
#   classified, separately activated execution
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

When this skill asks the user to choose among viable build options, first
define unfamiliar terms; explain each relevant option's reason, money/setup/
maintenance costs (or uncertainty), and case-specific pros and cons; recommend
one with a reason tied to the user's context; then ask one atomic question.
If a sound recommendation needs a missing fact, ask for that fact first.
Factual discovery and simple execution approval do not need an option menu.

## Output Format

Describe the exact deliverable: file path(s) and naming, report structure, or data
schema. Be specific enough that two runs produce consistent shapes.
For a user-facing build choice, include the explained options, recommendation
and reason before the one decision question. A preference is not authorization
for a side effect.

## Validation Checklist

- [ ] Output matches the shape declared above.
- [ ] Any user-facing build choice explains terms, reasons, costs, pros and cons,
      and a context-based recommendation before one atomic decision question;
      unknown costs and missing facts are stated, not guessed.
- [ ] No **Stop Conditions** were silently bypassed.
- [ ] Any side-effecting step has applicable authority. Standard §5 Exception 1
      permits only the exact bounded documentary writes it names: show the path
      and content, use an existing current-session instruction when it covers the
      write, or obtain content-specific approval when it does not. It does not
      authorize source/test editing; that needs a separately classified and
      activated TALI route (Exception 2, §5).
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
- Before an Exception 1 documentary write: show the exact path and content or
  diff. Use an applicable existing current-session instruction; otherwise wait
  for content-specific approval. A changed proposal needs coverage by the actual
  grant. Transcription cannot create authority or change a recorded grant.
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
