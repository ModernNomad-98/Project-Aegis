# Stage-Gate Map — default composition table

The default lifecycle for the owning [AI SDLC Operating Model](../SKILL.md):
how artificial intelligence (AI) agents and humans move a change through the
software development lifecycle (SDLC). Read it when drafting or adapting a
team's operating model. A pull request (PR) proposes a repository change;
continuous integration (CI) runs automated checks. Skills marked
*(manual-only)* run only when a person names them; hand them to the user,
never invoke them automatically.
Every row composes an
existing skill by name; the model document cites this table and adapts rows to
the repo — it never copies skill procedures into itself.

| Stage | Entry condition | Exit gate | Authority | Enforcing skill | Evidence left behind |
|---|---|---|---|---|---|
| Context | task received | repo identity + governing docs verified; assumptions listed | agent | `agent-startup-context-gate` | context report (facts vs assumptions) |
| Reconcile | sources conflict (any stage may route here) | one resolved truth, assumptions surfaced | agent | `source-of-truth-reconciler` | reconciliation report with citations |
| Classify | context verified | change class + validation floor + approval path declared; scope locked | agent | `change-classification-gate` | declared class + file-set scope |
| Plan / approve | class known | boundaries identified; approvals obtained for boundary-crossing steps | human decides; agent requests | `human-approval-boundary` + `agent-authorization-matrix` *(manual-only)* | approval records with scope wording |
| Implement | scope + approvals in place | diff matches declared intent; only intended files staged | agent | `reviewable-diff-discipline` *(manual-only)* (with `docs-first-implementer` *(manual-only)*, `tdd-engineer` *(manual-only)* as the work demands) | scoped diff; commit trail |
| Validate | diff complete | change-class validation floor met with real outputs | agent | class floor from `change-classification-gate`; quality assurance (QA) testing skills (catalog Phase 5) as applicable; `local-ci-mirror-preflight` *(manual-only)* before push | command outputs, CI runs |
| Review | validation green | human/agent review recorded; security lens where class requires | human (agent may pre-review) | `code-reviewer` / `security-pr-reviewer` | review record on the PR |
| Merge | review + checks green | merge by the authority holder under the applicable matrix and current approval register; absent a scoped grant, obtain the named human decision | human, or agent within a recorded merge grant | `agent-authorization-matrix` *(manual-only)* | merge event traceable to the authority and approval record |
| Close | merged (or work stopped) | closeout delivered incl. intentionally-not-done | agent | `ai-closeout-reporter` | closeout report |
| Learn | closeout delivered | memory updated per write rules; periodic compliance spot-check scheduled | agent proposes; human approves memory/policy edits | `agent-memory-governance` *(manual-only)*, `agent-governance-audit` | governed memory entries; audit reports |

Failure at any stage routes to `agent-failure-recovery` *(manual-only)* (broken tree/branch
state) or back to Reconcile (conflicting truths). Instruction-file drift found
along the way routes to `agent-instruction-consolidator` *(manual-only)*.

## Authority levels

- **agent** — autonomous within the stage's contract; evidence still required.
- **agent-with-approval** — agent executes only inside a recorded approval's
  scope (one-time or durable; never wider than its wording).
- **human** — the decision itself is human; the agent may prepare everything
  up to the decision point and must stop there.

## Multi-tool topologies (documented options)

Choose from observed practice and record the choice in the model; neither is
the default.

| Topology | Shape | Holds when |
|---|---|---|
| Per-tool spokes | Thin entry file per tool (`AGENTS.md`, `CLAUDE.md`, …) pointing into a shared `docs/` tree; a platform-role table states which tool reads which entry file and its role; a file-ownership table marks tool-specific, shared, generated (never edit) and append-only files | each tool needs its own entry file and the shared tree is the real source |
| Hub-and-spoke | One authoritative rulebook; per-tool pointer files MUST point back to it and MUST NOT contain conflicting rules | many tools, one rule set to keep consistent |

**Collision rule.** When two tools can edit the same surface — for example
a two-way-sync platform editor and a coding agent on the same frontend — only
one tool edits that surface per phase (one approved chunk of work). Record which tool owns which surface
in the plan/approve row. Drift between the files routes to
`agent-instruction-consolidator` *(manual-only)*.

## Adoption sequencing notes

1. Adopt the merge-authority row first — it is where the worst incidents live
   (unreviewed merges via auto-merge armed in an earlier session).
2. Then the classify + approve rows (scope lock, boundary approvals), which
   prevent most drift at the source.
3. Then evidence rows (validate, close), which make the audit stage possible.
4. Schedule `agent-governance-audit` spot-checks only after the rows they
   would audit are adopted — auditing unadopted policy produces noise.
5. Revisit the model on its review date with audit findings in hand; the map
   is versioned policy, not scripture.
