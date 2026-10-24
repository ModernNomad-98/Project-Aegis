---
name: ai-closeout-reporter
description: 'Produce the end-of-task closeout report — what changed, what was intentionally NOT done or was omitted (always a dedicated section, "None" written explicitly when empty), files touched, tests and validation actually run with real results, a per-deliverable trace from request item to files, checks and evidence (commit SHA, CI run, logs, known skips), risks, skipped checks, and the recommended next action. Use when finishing a task, handing off work, opening or closing a pull request (PR), or when asked what was actually done. Scope reductions must be disclosed, never silent. Do NOT use to verify a closeout''s claims or audit a finished change''s process compliance (agent-governance-audit), design a cross-stage handoff protocol (phased-work-handoff-designer), write a lane''s pre-work guide (lane-authoring-guide), reconcile chat-only history against the repo (chat-backlog-reconciliation), assemble a promotion packet (promotion-packet-writer), or set screenshot-evidence policy (screenshot-evidence-planner).'
---

# Artificial Intelligence (AI) Closeout Reporter

**Reading key:** PR is pull request; CI is continuous integration, the
automated build-and-test run; SHA is Secure Hash Algorithm, and a commit SHA
names one exact commit. The head is the latest commit on the branch being reported. A diff is the set of line changes the work made. An exit code is the number a command returns; 0 means success. A migration is a recorded database schema change. Evals are evaluation cases, the test prompts a skill is checked against.

## Purpose

End every task, whether a person or an artificial intelligence (AI) agent did
it, with a report that lets a human trust — or correctly distrust — the work
without re-deriving it. The report's defining feature is mandatory
disclosure of scope reductions: a permanent "Intentionally not done / omitted"
section means anything consciously skipped is stated with its reason and made
visible, never discovered later by surprise.

## Use When

- Use when: finishing a task or a phase of work.
- Use when: handing work off, opening a pull request (PR) for review, or closing one out.
- Use when: asked "what did you actually do?" about completed work.
- Do NOT use when: writing a full terminal closeout for a mid-task progress update —
  that is a lighter status note; the live-read-back rule below still applies to ALL
  status reports, including progress and handoff notes.
- Do NOT use when: shaping a commit or staged diff — that is
  `reviewable-diff-discipline` *(manual-only)* (its parked items feed this report).
- Do NOT use when: verifying a closeout's claims (`agent-governance-audit`),
  designing a cross-stage handoff (`phased-work-handoff-designer`), writing a
  lane's pre-work guide (`lane-authoring-guide`), or reconciling chat-only
  history against the repository (`chat-backlog-reconciliation`).
- Do NOT use when: assembling a promotion packet (`promotion-packet-writer`)
  or setting screenshot-evidence policy (`screenshot-evidence-planner`);
  this skill reports one finished task.

## Inputs to Inspect

1. **The ORIGINAL request — re-read it.** The report is written against what
   was asked, not against what was done.
2. The actual diff and created files: `git status`, `git diff --stat`, the
   commit list.
3. Command outputs for every validation actually run (tests, builds, linters,
   validators).
4. Parked or out-of-scope items recorded during the work.
5. Approvals granted during the task, and their scope.

## Workflow

1. Re-read the original request; extract every explicit or implied deliverable
   into a checklist.
2. Mark each deliverable: done | partially done | intentionally not done |
   not applicable.
3. Everything not fully done goes into "Intentionally not done / omitted" with
   its reason — including quiet downgrades (asked for 10, delivered 6).
4. List files touched from git output, not from memory.
5. Record validation with the actual commands and their actual results —
   failures verbatim. Anything this kind of change normally requires that was NOT run
   goes under "Skipped validation" with the reason.
   - When verification spans several surfaces (endpoints, pages, roles,
     tenants), report a per-surface pass/fail table AND a negative-path table
     (what must be refused or fail, and whether it did).
   - Decompose skips: every skipped check or skipped-test count broken down
     by reason, never a bare total.
   - When a local preflight ran (a local copy of the CI checks, from `local-ci-mirror-preflight` *(manual-only)*),
     include its evidence block in section 4 as recorded, not paraphrased.
6. Build the per-deliverable trace in section 5: one row per deliverable from
   step 1, naming the request item, the files that serve it, the check that
   proves it, and the evidence item. Each evidence item carries its
   provenance: the command and its exit code, or the CI run link, tied to the
   exact head commit SHA. Migration proof and known skips are rows, not
   prose. A deliverable with no proving check reads "not verified" and also
   appears under "Skipped validation"; it is never marked done.
7. State risks and known gaps. Write an unqualified "complete" / "verified
   complete" only after every recorded gap is closed; otherwise qualify the
   claim and name the open gaps.
8. Recommend the next action. When a phase is finished, add a
   completion-baseline anchor: "<work> is complete; do not treat as pending",
   pinned to immutable evidence (merged PR number, merge commit SHA — the
   Secure Hash Algorithm identifier of the merge commit — and
   applied-migration identifier) so later sessions do not re-open or redo it.
   Anchor only merged or applied facts, never open-PR state.
9. Run the Validation Checklist, then deliver the report as the final message
   (or as a file if asked), following
   [assets/closeout-template.md](assets/closeout-template.md).


## Live read-back for every GitHub/remote-change claim

This rule applies to ALL status reports - progress, handoff, PR body, closeout and
chat status - not only terminal closeouts. Any claim that a GitHub or remote change was
made (PR/comment/review/merge/label/check-run/commit push or ref update) must quote the
live read-back: the exact command and the observed output, including the observed
head/ref. A prior action, intention or cached memory is not evidence. When no successful
read-back was performed, write UNVERIFIED and do not claim the change.

Per-claim live-read-back inventory (quote command plus observed output):

- PR claim: gh pr view <n> --json number,state,headRefOid,baseRefOid,isDraft,mergeCommit --jq '.' - quote observed number/state/headRefOid/mergeCommit.
- PR comment claim: gh api repos/{owner}/{repo}/issues/<n>/comments --paginate --jq '.[] | {id,user:.user.login,created_at,body}' - quote the matching id/body excerpt.
- Review claim: gh api repos/{owner}/{repo}/pulls/<n>/reviews --paginate --jq '.[] | {id,user:.user.login,state,commit_id,submitted_at}' - quote id/state/commit_id.
- Merge claim: gh pr view <n> --json state,mergeCommit,mergedAt,headRefOid - quote exact mergeCommit/mergedAt/head.
- Label claim: gh api repos/{owner}/{repo}/issues/<n>/labels --jq '.[].name' - quote observed labels.
- Check-run claim: gh api repos/{owner}/{repo}/commits/<sha>/check-runs --jq '.check_runs[] | {name,status,conclusion,head_sha}' - quote name/status/conclusion/head_sha.
- Push/ref claim: git ls-remote <remote> <ref> - quote the exact sha; or git rev-parse <ref> plus git log -1 --format=%H%x20%s.

Rule: every claim quotes command and observed output; missing or negative read-back
=> UNVERIFIED, never a claim.

## Implementation-PR body requirement

Every implementation PR body (M-2) carries exactly one five-column Aegis-skills-applied
table: Skill and source revision | Actor / role | Purpose | How applied | Result, evidence,
and limitations. The body also carries a PR-body review-evidence disposition record for
every provider/page/cursor: provider, link, reviewed original_commit_id,
concern/applicability, disposition, evidence, uncertainty. Missing reviews are not clean.
This SKILL states the requirement; D/F stages verify the actual PR body.

## Output Format

All eight sections, in order, every time
(template: [assets/closeout-template.md](assets/closeout-template.md)):

```
CLOSEOUT REPORT
1. Summary — what changed and why
2. Intentionally not done / omitted — REQUIRED ALWAYS; "None." must be explicit
3. Files touched — exact paths, from git
4. Tests & validation run — command → actual result (failures verbatim);
   per-surface + negative-path tables; preflight evidence block if one ran
5. Evidence — per-deliverable trace (request item → files → check →
   evidence with commit SHA or CI run); outputs, links, screenshots, PR
6. Risks & known gaps
7. Skipped validation — what wasn't run, and why
8. Next actions / handoff — incl. completion-baseline anchor when a phase ends
```

## Validation Checklist

- [ ] Section 2 present even when empty — "None." written explicitly.
- [ ] Every deliverable from the ORIGINAL request accounted for in section 1
      or section 2.
- [ ] File list generated from git, not recalled.
- [ ] Every validation claim backed by a command actually run this session —
      no "tests pass" without output.
- [ ] Failures and skips reported verbatim, not smoothed over.
- [ ] No claim exceeds the evidence (e.g., "evals present and well-formed" is
      not "evals pass").
- [ ] Every delivered item has a trace row naming its files, check and
      evidence.
- [ ] Every evidence item names its commit SHA or CI run; a run on an older
      commit is not evidence for the head.
- [ ] Multi-surface work has per-surface pass/fail and negative-path tables;
      skips are decomposed by reason.
- [ ] "Complete" is unqualified only when no recorded gap remains open.
- [ ] Any completion-baseline anchor cites merged/applied evidence (PR, SHA,
      migration), not in-flight state.

## Gotchas

- Silent scope reduction is the incident class this skill exists to prevent:
  partial delivery reported as complete because nothing forced the omission to
  be stated. Mandatory section 2 is that forcing function.
- Reports drift toward describing what WAS done; only auditing against the
  original request surfaces what wasn't.
- The classic honesty failures: "validated" with no runner, "tests pass"
  without running them, and failures summarized into vagueness.
- A closeout listing 40 files "for completeness" hides the 3 that matter —
  be exact but curated, and point to the PR/diff for the full list.
- "12 skipped" hides whether 11 could not run in this environment and 1 was the check
  that mattered; only a per-reason breakdown shows it.
- Separate lists of files, checks and evidence do not show which test proves
  which requested item, or which commit a green run came from; the trace row
  does.
- Finished work with no pinned evidence invites a later session to re-open
  or re-implement it; the anchor is the report's defense against that.

## Stop Conditions

- Asked to write a closeout claiming validation that did not happen → refuse;
  report the actual state (the skipped-validation section exists for exactly
  this).
- The actual diff contains changes the task cannot explain → stop; investigate
  or escalate before reporting.
- Asked to list CI as passed when the only CI run is on an older commit than
  the reported head → refuse; the trace row names both SHAs and marks the
  check "not verified" for the head.
- Unable to determine whether a requested deliverable was completed → say so
  explicitly in the report rather than guessing a status.

## Supporting Files

- [assets/closeout-template.md](assets/closeout-template.md) — copyable report
  template with all eight sections and the per-deliverable trace table.
- `evals/evals.json` — trigger + behavior cases, including mandatory
  scope-reduction disclosure and the per-deliverable trace.
- `evals/trigger-evals.json` — discrimination against the neighbours that
  route toward this skill: `agent-governance-audit`,
  `phased-work-handoff-designer`, `lane-authoring-guide`,
  `chat-backlog-reconciliation`, `promotion-packet-writer`, and
  `screenshot-evidence-planner`.
