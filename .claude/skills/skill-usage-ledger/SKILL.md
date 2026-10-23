---
name: skill-usage-ledger
description: 'Produce the six-field record of which Aegis skills a task used, each bound to its skills-manifest SHA-256, for pasting into a PR description or ledger. Emits the record in conversation and writes nothing.'
---

# Skill Usage Ledger

**Reading key:** a *skill* is one instruction set under `.claude/skills/`; the
*skills manifest* is `tools/skills-manifest.json`, the validator-generated
list that binds each skill's name to the SHA-256 of its `SKILL.md` bytes
(CRLF normalized); a *usage record* is one line per skill used: name and
manifest hash, reason, what was applied, the result, anything left
incomplete, and who produced the record.

## Purpose

Make skill usage recordable, verifiable, and expected. The repository's
delivery workflow asks every stage agent to record which skills it used;
external users copying the skills get the same practice. A record bound to
the manifest hash says WHICH skill (the hash pins the normalized SKILL.md bytes only; referenced instruction files are not covered), and the remaining fields say WHY, WHAT, and HOW IT WENT. This
skill EMITS that record in conversation — it performs no write: pasting the
block into the PR description or the user's own ledger is the user's action
outside the skill.

## Use When

- Use when: finishing work that used one or more Aegis skills and the task
  (or the repository workflow) asks for a skills-used record.
- Use when: someone asks "which skills did you use and why" for a completed
  task.
- Use when: preparing the skills section of a pull-request description.
- Do NOT use when: the task closeout itself is wanted — that is
  `ai-closeout-reporter`; this skill records WHICH skills, the closeout
  reports WHAT was done.

## Inputs to Inspect

1. `tools/skills-manifest.json` — the current manifest: every skill name and
   its SHA-256. Validate read-only first with `python scripts/validate-skills.py`
   (no refresh); refresh the manifest (`--refresh-skills-manifest`) only when the user authorizes a
   write.
2. The task's actual skill invocations — which skills were really applied
   and what each did, not which skills merely existed.
3. The target the record will be pasted into (a PR description, a ledger,
   or the user's own notes) and its required field order.

## Workflow

1. List each skill actually used in the task, in the order used.
2. Resolve each name to its SHA-256 in the manifest. A name not in the
   manifest is a stop (see Stop Conditions) — never guess or invent a hash.
3. For each skill, fill the six fields: `reason` (why this skill, not
   another), `applied` (what was actually done with it), `result` (the
   observable outcome), `incomplete` (what was left unfinished, or
   "None"), `by` (who produced the record — agent/stage or person).
4. Emit the record block (Output Format) in the conversation.
5. Instruct the user to paste the block into the PR description or their
   ledger — the paste is their action; this skill writes nothing.

## Output Format

One line per skill used, six fields separated by `/`:

```text
skill@<manifest-sha256[:12]> / reason / applied / result / incomplete / by
```

The short form uses the first 12 hex characters of the hash; the full
64-character hash is always acceptable and preferred when space allows.
The block echoes the delivery-workflow skills-row protocol's
author/source/result discipline: every named skill must resolve in the
manifest, no hash is invented, and `incomplete` is filled honestly.

## Validation Checklist

- [ ] Every named skill resolves in `tools/skills-manifest.json`.
- [ ] Every hash is copied from the manifest — never invented, never
  remembered.
- [ ] `reason` names why THIS skill and not its neighbor.
- [ ] `incomplete` is filled honestly, or reads exactly "None".
- [ ] `by` names the actual producer (agent/stage/round or person).

## Gotchas

- **Recording from memory invents hashes.** Copy the hash from the manifest
  at record time; a hash from a previous task may name a different
  `SKILL.md` after an update.
- **Signal-catalog epoch gate:** the consumer contract is owned and defined by `skill-usage-instrumenter` (its catalog/epoch rules); this ledger records and validates the read-only/hash-identity view and points at that contract rather than restating it.
- **A stale manifest fails the validator.** Read-only validation first; if the manifest is stale, stop and ask the user to authorize a refresh - do not refresh silently. State that any skill edit PR must carry the refreshed manifest.
- **Compliance is the user's.** This skill produces the record and the
  honesty framing; it does not enforce that the user pastes it. The record
  is an aid to verifiability, not a replacement for the user's own
  accountability.

## Stop Conditions

- A named skill cannot be resolved in the manifest → refuse to invent its
  hash; say which name failed and point at
  `python scripts/validate-skills.py` (no refresh unless the user authorizes a write; a stale manifest is never refreshed silently).
- The ask becomes authoring someone else's closeout or usage record → stop
  and route to the owning skill (`ai-closeout-reporter` owns the closeout;
  the stage-author owns its own skills rows).
- The manifest file itself is missing → stop and instruct regeneration
  rather than recording from memory.

## Supporting Files

- `evals/evals.json` — behavior cases: the two-skill record, the manifest
  miss, the closeout near-miss, the missing-manifest refusal.
- `evals/trigger-evals.json` — discrimination against `ai-closeout-reporter`
  (which-skills vs what-was-done), both auto-invocable.
