---
name: agent-instruction-consolidator
description: Audit and align agent instruction files across tools — CLAUDE.md (root, nested, local), AGENTS.md, Cursor rules, GitHub Copilot instructions, Windsurf and Cline rules, and similar — into one consistent source of truth. Invoke explicitly when instruction files conflict, duplicate each other, or have drifted, or after adopting a new AI tool. Produces an inventory, a conflict and duplication matrix, and a consolidation proposal with a rule-preservation diff; edits files only after the proposal is approved. Manual-only, because instruction files steer every future agent run.
disable-model-invocation: true
---

# Agent Instruction Consolidator

## Purpose

Make every AI tool in the repo read the same truth. This skill inventories all
agent-instruction files, extracts and compares their rules, exposes conflicts
and drift, and consolidates to a designated canonical source with thin
per-tool pointers — proving with a before/after rule inventory that no rule
was silently lost or changed along the way.

## Use When

- Use when (explicitly invoked by a human): instruction files disagree
  (different test commands, contradictory style rules), duplicated content has
  drifted apart, a new AI tool was adopted, or an audit of agent guidance is
  requested.
- Do NOT use when: authoring a first instruction file for a repo that has none
  — there is nothing to consolidate.
- Do NOT use when: resolving conflicts between docs and code — that is
  `source-of-truth-reconciler`; this skill is specifically about
  agent-instruction files.
- Never auto-invoked: consolidation edits files that steer every future agent
  run — supply-chain-sensitive, human-initiated only
  (`disable-model-invocation: true`).

## Inputs to Inspect

1. Every instruction file present — locate them with
   [references/instruction-file-map.md](references/instruction-file-map.md):
   `CLAUDE.md` (root and nested), `CLAUDE.local.md`, `AGENTS.md`,
   `.cursorrules` and `.cursor/rules/`, `.github/copilot-instructions.md` and
   `.github/instructions/`, `.windsurfrules`, `.clinerules`, plus repo-custom
   standards docs that function as agent instructions.
2. Which tools are actually in use (configs, CI, teammate signals).
3. Each tool's precedence semantics (nested overrides root? local overrides
   repo? per the map).
4. Git history of the instruction files — who drifted from whom, and when.

## Workflow

1. **Inventory:** find every instruction file; record path, the tool(s) that
   read it, its scope (repo / directory / user), and its precedence semantics.
2. **Extract rules:** normalize each file into discrete rules (build/test
   commands, style, security, workflow, tone).
3. **Build the matrix:** rule × file. Classify every rule: unique | duplicate
   (identical) | drifted (same topic, different content) | conflicting
   (incompatible) | stale (references removed tooling or paths).
4. **Propose consolidation:** designate ONE canonical source; per-tool files
   become thin pointers or minimal tool-specific supplements; nested or
   dir-scoped overrides are preserved intentionally and documented. Include
   migration steps and a before/after rule inventory giving every rule a
   disposition: kept | merged | superseded-by | dropped-with-reason.
5. **STOP for approval.** Present the matrix and proposal. No file edits
   before explicit approval.
6. **Apply (after approval):** make exactly the approved edits, nothing more.
7. **Verify:** re-run the inventory; the post-state matrix must show zero
   conflicts and no undisposed rules.

## Output Format

```
INSTRUCTION CONSOLIDATION REPORT
Inventory: <file → tool(s), scope, precedence>
Matrix:    <rule × file, with classification>
Conflicts: <each, with the divergent texts quoted>
Proposal:  canonical = <file>; <per-file plan>
Rule preservation: <every rule → kept | merged | superseded | dropped (reason)>
Status: AWAITING APPROVAL | APPLIED (verified)
```

## Validation Checklist

- [ ] Every known instruction-file location checked, not just the famous ones.
- [ ] Every rule in the matrix has a disposition; none vanish without a stated
      reason.
- [ ] Tool precedence semantics respected — a nested override is intent, not
      drift, unless shown otherwise.
- [ ] No edits made before explicit approval.
- [ ] Post-apply inventory re-run and clean.

## Gotchas

- Instruction files are executable-adjacent: a bad merge here silently changes
  every future agent run in the repo. That is why this skill is manual-only
  and proposal-first.
- Nested `CLAUDE.md` files are often deliberate directory-scoped overrides —
  consolidating them "up" can destroy intended behavior.
- Tools differ on precedence and even on which files they read; verify against
  the map rather than assuming symmetry.
- `CLAUDE.local.md` and user-level files may live outside the repo and explain
  "phantom" behavior differences between machines.
- Two files that agree today will drift again — the end state is one canonical
  file plus pointers, not N synchronized copies.

## Stop Conditions

- Proposal complete → full stop until explicit human approval. Applying an
  unapproved consolidation is this skill's defining failure.
- A conflict encodes a genuine team disagreement (both rules actively defended)
  → escalate; do not pick a winner.
- An instruction file contains security-relevant rules that consolidation
  would weaken or reorder → halt and flag before proposing.
- Rules exist for a tool that cannot be identified → ask before classifying
  them as stale.

## Supporting Files

- [references/instruction-file-map.md](references/instruction-file-map.md) —
  file locations, owning tools, scope, and precedence semantics.
- `evals/evals.json` — behavior cases, including the no-edit-before-approval
  stop.
- Manual-only invocation prevents trigger overlap, so no trigger-evals file.
