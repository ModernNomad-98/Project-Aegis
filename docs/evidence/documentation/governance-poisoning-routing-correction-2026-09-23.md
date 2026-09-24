# Revert and live incident routing correction — 2026-09-23

## Purpose and scope

This bounded correction fixes two instructions that could mislead a human
operator or an artificial intelligence agent. It changes the
[merge-as-deploy governance skill](../../../.claude/skills/merge-is-deploy-governance/SKILL.md),
the [model poisoning review skill](../../../.claude/skills/model-poisoning-reviewer/SKILL.md),
the [governance behavior evaluation](../../../.claude/skills/merge-is-deploy-governance/evals/evals.json),
and this record. A separate reference-page batch updates the governance
template and poisoning controls; its review and delivery are tracked in its
own pull request.

The previous bounded correction estimate was **1–3 active hours**. This
owning-skill correction was estimated at **1–3 active hours**; the selected
backlog total at start was **175–394 active hours**. The isolated worktree was
created at **2026-09-23 20:28:26 Coordinated Universal Time (UTC)**. These
are planning ranges, separate from observed wall time; active-only labor was
not instrumented.

## Verified behavior and revised instruction

- A squash merge creates an ordinary, single-parent commit. For that commit,
  the governance skill now recommends `git revert <commit>`. Git's
  [revert documentation](https://git-scm.com/docs/git-revert) describes
  `-m <parent-number>` as choosing the mainline parent when reverting a merge.
  It is unnecessary for an ordinary commit. The previous claim that `-m 1`
  always fails on a squash commit was too strong and was removed from the
  skill and its behavior-evaluation assertion. The skill directs readers to
  inspect a true merge's parents and choose its mainline deliberately.
- The model poisoning skill previously sent confirmed production poisoning
  to `incident-response-runbook`. That skill's own selection description says
  it **authors** runbooks and never runs an incident. Live response now routes
  to the named human incident owner using the current approved runbook;
  the authoring skill can revise that document. Containment and rollback
  remain human decisions and any remediation remains separately approved.

The related reference-page writer is correcting a reversed two-dot commit
range. Git's [revision-range documentation](https://git-scm.com/docs/gitrevisions)
defines `A..B` as commits reachable from `B` but not `A`; a newest-to-oldest
range would exclude the intended linear-history commits. This note does not
claim that any revert or live incident operation was run.

## Verification and delivery limit

The governance skill's selection description was shortened to fit its
frontmatter length limit without changing its use cases. Its behavior
evaluation was corrected so it no longer rewards the false failure claim;
other evaluation fixtures and both skills' invocation posture remain
unchanged. The skill validator passed for **185 skills with zero warnings**;
the evaluation file parsed as JSON, all **seven local links** resolved, and
the whitespace check passed. Independent read-only review cleared the
corrected four-file draft at **20:35:35 UTC** with no blocker. No runtime
file, Git history, live host, provider, credential, or private input was
changed or accessed by this correction.
