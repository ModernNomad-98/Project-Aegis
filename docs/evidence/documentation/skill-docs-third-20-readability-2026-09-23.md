# Third 20 skill documents: bounded readability correction — 2026-09-23

## Scope and estimate

A read-only audit of the next 20 stable, sorted skill entrypoints, from
`caching-strategy-designer` through `data-quality-monitor-designer`, found
first-use terminology gaps in three. This correction changes only
[CI Pipeline Architect](../../../.claude/skills/ci-pipeline-architect/SKILL.md),
[Compliance Gap Auditor](../../../.claude/skills/compliance-gap-auditor/SKILL.md),
[Data Quality Monitor Designer](../../../.claude/skills/data-quality-monitor-designer/SKILL.md),
and this dated note. The other 17 audited skills were not rewritten. The
coordinator owns any shared documentation readability ledger update.

The isolated worktree began from `3ba17903033ffd1cefc30f4b61857cc36ef1f0e6`,
the `origin/main` head after pull request #151. The prior batch estimate was
**2–4 active hours**; this new bounded batch estimate is also **2–4 active
hours**. The selected remaining backlog estimate at start was **175–394 active
hours**. These are planning ranges, separate from observed wall time.

## Contract-preserving changes

- The CI pipeline skill defines CI/CD, E2E, OIDC, PR, SAST, and YAML in its
  body and spells out the credential and forked-request fields in its output
  template. Its `MANUAL-ONLY` description and `disable-model-invocation: true`
  frontmatter remain unchanged. This batch did not invoke the skill or edit a
  pipeline definition.
- The compliance gap skill defines ISO, SOC 2, CPA, SoA, TSC, AI RMF, Amd1, and its four
  requirement verdicts. Its template makes the framework options and evidence
  fields readable while preserving the missing-text and missing-evidence
  limits. It remains a readiness assessment, never an audit opinion.
- The data quality skill distinguishes per-dataset service-level agreements
  from journey service-level objectives and defines DLQ, DAG, PII, and LLM.
  Its template expands abbreviated labels without changing the three failure
  actions, quarantine obligation, incident routing, or ownership boundary.

The relevant names were checked against [NIST's AI RMF](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10),
[ISO's Amendment 1 record](https://www.iso.org/standard/88435.html),
[ISO's Statement of Applicability note](https://committee.iso.org/files/live/sites/jtc1sc27/files/resources/ISO-IECJTC1-SC27-WG1_N3298_Auditing%20Practices%20Note%20-%20SoA.pdf),
and [AICPA's Trust Services Criteria page](https://www.aicpa-cima.com/resources/download/2017-trust-services-criteria-with-revised-points-of-focus-2022).
No licensed framework text was reproduced. No private input, provider,
credential, or real host was accessed.

## Verification and timing

Work started at **2026-09-23 19:44:38 UTC**. At the **19:47:12 UTC** local
checkpoint, the observed wall interval was **2 minutes 34 seconds**.
`python -B scripts/validate-skills.py` passed with **185 valid skills and zero
warnings**; all **5 local links** in the four scoped pages resolved, and
`git diff --check` passed. The three YAML frontmatter blocks and their six
trigger/behavior evaluation files were unchanged after newline normalization.
Those unchanged selection descriptions and criteria bound the focused eval
impact review; no live model evaluation was run for these wording changes.
Independent read-only review found three further first-use terms (ISO, SOC 2,
CPA) in the compliance skill. They were defined, the validator and diff check
were rerun, and read-only re-review cleared the four-path draft at **19:50:53
UTC** with no blocker. The final local checkpoint was **19:51:13 UTC**, **6
minutes 35 seconds** after the start. Active-only labor is not instrumented.
