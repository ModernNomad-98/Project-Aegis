---
name: code-reviewer
description: 'Review an ACTUAL diff — a PR, branch delta, or staged/working changes obtained from git — and report findings by severity (blocker/major/minor/nit), each with file:line evidence and a concrete remediation. Covers correctness, security, performance, reliability, maintainability, test adequacy, migration safety, and agent-typical faults: scope beyond the stated intent, drift from recorded architecture decisions, tests weakened or skipped to pass. Use when asked to review a diff, PR, branch, or commit. Do NOT use for security-focused review (security-pr-reviewer), skill-library PRs (library-diff-reviewer), behavior-preserving cleanup application (code-simplifier), whole-repository audits (full-codebase-auditor), strategic architecture assessment of a subsystem (principal-code-analyst), or gating AI-generated code before it is saved, committed or run (llm-output-safety-reviewer). Never reviews imagined code: no diff, no review.'
---

# Code Reviewer

**Reading key:** PR means pull request, a proposed code change; CI means
continuous integration; RLS means row-level security; authz means
authorization; I/O means input and output; ADR means architecture decision
record, a written record of a design decision and its rules; a layering rule
says which parts of the code may call which, for example that user interface
code must go through a service layer.
An N+1 query pattern means one list query triggers an additional database
query for each returned item.

## Purpose

Produce a review a maintainer can act on: findings ordered by severity, each
anchored to file:line in the real diff, each explaining the failure it causes
and the concrete fix. The review's authority comes from evidence — a claim
without an anchor and a failure scenario is an opinion, and opinions are
labeled as such or dropped. Verdict included: approve, approve-with-nits, or
request-changes, with the blocking findings named.

## Use When

- Use when: asked to review a PR, a branch against its base, a commit, or
  the current staged/working diff.
- Use when: a change is about to merge and needs a correctness/security/test
  pass with severity-ranked output.
- Use when: a coding agent wrote the change; the same review also checks
  for tests weakened to pass and drift from accepted ADRs.
- Do NOT use when: the request is to *apply* simplifications — that is
  `code-simplifier` (side-effecting, manual-only).
- Do NOT use when: the scope is the whole repository's health, not one change
  — that is `full-codebase-auditor`.
- Do NOT use when: the ask is a strategic architecture read on a subsystem —
  that is `principal-code-analyst`.
- Do NOT use when: the review is security-focused — that is
  `security-pr-reviewer`; this skill gives the general severity-ranked pass.
- Do NOT use when: the PR changes the skill library — that is
  `library-diff-reviewer`; this skill reviews product-code diffs.
- Do NOT use when: the ask is the gate artificial intelligence (AI)-generated code passes before it is
  saved, committed or run — that is `llm-output-safety-reviewer`.
- Never review from a description of a change. No diff obtained = no review;
  say so.

## Inputs to Inspect

1. The actual diff: `gh pr diff <n>` / `git diff <base>...<branch>` /
   `git diff` + `git diff --staged`. Record which one was reviewed.
2. The stated intent: PR description, commit messages, linked issue — the
   review judges the diff against its declared purpose.
3. Surrounding unchanged code of every modified hunk — callers, callees, and
   invariants the hunk relies on; a diff-only read misses broken contracts.
4. The tests touched or conspicuously not touched by the change.
5. Migrations, schema, config, CI, and dependency changes riding along —
   the risky lines often hide outside `src/`.
6. The repository's ADRs and documented layering rules that cover the
   changed code; note "none found" rather than assuming there are none.

## Workflow

1. **Obtain the real diff** and its base; note size and file spread. If it
   mixes unrelated intents, note that as a finding
   (`reviewable-diff-discipline` violation) and review anyway.
2. **Read the intent** and form the question the review answers: does this
   diff do what it claims, and only that, safely?
3. **First pass — correctness:** logic errors, inverted conditions, off-by-
   one, error paths, null/empty/boundary handling, concurrency around shared
   state. Read callers of changed functions, not just the hunks.
4. **Second pass — security:** input validation at boundaries, authz on new
   paths, injection surfaces, secrets in code/config/logs, unsafe
   deserialization, tenant-scope leaks on data access.
5. **Third pass — reliability & performance:** failure modes of new I/O
   (timeouts, retries, partial failure), resource leaks, N+1 queries, work
   moved onto hot paths, unbounded growth.
6. **Fourth pass — tests & migrations:** do tests pin the new behavior and
   its edges (would they fail if the change were reverted?); are migrations
   forward-safe, rollback-considered, and deploy-order-safe? Then check for
   **weakened validation**: tests deleted or skipped, assertions loosened,
   timeouts or retries raised, or CI steps removed in the same diff. Each is
   at least MAJOR, naming the test or step, unless the stated intent explains
   it (for example, a test deleted together with the feature it covered).
7. **Fifth pass — maintainability:** naming, duplication, dead code,
   convention drift — reported as minor/nit unless it hides a defect. Drift
   from an accepted ADR or a layering rule in the repository's docs is MAJOR
   and cites the ADR or rule; with no such decision on file, convention drift
   stays minor/nit.
8. **Write findings** with severity, anchor, failure scenario, remediation.
   Uncertain claims are marked "needs verification", not asserted.
9. **Deliver the verdict** with blockers listed; note what was NOT reviewed
   (generated files, vendored code) so the human knows coverage.

## Output Format

```
CODE REVIEW — <PR/branch/diff id> (base: <ref>, N files, +A/−D)
Intent: <what the change claims to do>
Verdict: approve | approve-with-nits | request-changes
Findings (by severity):
  [BLOCKER] <file:line> — <defect>; fails when <scenario>; fix: <remediation>
  [MAJOR]   ...
  [MINOR]   ...
  [NIT]     ...
Tests: <adequate | gaps: which behaviors are unpinned>
Validation integrity: <intact | weakened: which tests, assertions or CI steps>
Migrations/config/deps: <safe | findings>
Not reviewed: <exclusions + why>
Positive notes: <what the change does well — optional but earned>
```

## Validation Checklist

- [ ] Reviewed an actual obtained diff; command recorded.
- [ ] Every finding has file:line, a failure scenario, and a remediation.
- [ ] Severity reflects impact, not annoyance — style nits are never majors.
- [ ] Callers/callees of changed code were read, not just the hunks.
- [ ] Test adequacy judged by "would the tests catch a revert?".
- [ ] Deleted, skipped or loosened tests and removed CI steps were checked;
      each one the intent does not explain is at least MAJOR.
- [ ] Accepted ADRs and layering rules were read; drift from them is MAJOR
      and cites the ADR or rule.
- [ ] Migration/dependency/CI changes in the diff got explicit attention.
- [ ] Verdict states which findings block; unverified suspicions labeled.

## Gotchas

- The bug is often in the unchanged line the diff now invalidates — review
  the contract, not the hunk in isolation.
- Renames and moves hide edits: `git diff -M` shows what actually changed
  inside "moved" files.
- A green CI run tells you the existing tests pass, not that the new behavior
  is tested — check the diff of the tests, not the badge.
- Reviewing generated files line-by-line wastes the budget; verify the
  generator input changed correspondingly and say generated output was skipped.
- Big diffs induce rubber-stamping; if attention degraded past a size,
  say where coverage got thinner rather than implying uniform scrutiny.
- Comment-only and doc changes still merit a scan — stale docs that now
  contradict the code are a finding.

## Stop Conditions

- No diff can be obtained (no branch/PR/changes) → stop; do not review from
  a verbal description.
- The diff touches security policy, RLS, auth flows, or production config in
  ways whose implications are unclear → flag for human security review via
  `human-approval-boundary`; do not approve on inference.
- The diff is so large or generated-heavy that a line-level review would be
  theater → say so, propose a split or a scoped review, and review the
  reviewable core.
- Asked to both review and silently fix the findings in one pass → review
  first; fixes are a separate, explicitly-approved change.

## Supporting Files

- [references/severity-rubric.md](references/severity-rubric.md) — severity
  definitions with boundary examples, and the per-pass checklists in full.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `code-simplifier`,
  `principal-code-analyst`, and `full-codebase-auditor` (review/audit
  cluster), and against `security-pr-reviewer`, `test-coverage-mapper`,
  `llm-output-safety-reviewer` and `agent-governance-audit` for reviews of
  agent-written changes.
