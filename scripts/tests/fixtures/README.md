# Validator and contract-audit test fixtures

This guide is for maintainers changing Project Aegis validation or contract
audits. It identifies the synthetic inputs used by the offline self-tests and
shows how to check them from the source-library root. For the separate
beginner-workflow acceptance fixture, use the [Scenario A runbook](../../../docs/acceptance/scenario-a-runbook.md).

Except for this guide, the files under this directory are **synthetic input for
`scripts/tests/test_validator.py`** (decision D55, the validator self-test
decision), except `contract-audit/repo/`,
which is consumed by `scripts/tests/test_audit_skill_contracts.py`. None of
those fixture inputs is a shipped skill, agent, workflow, or product guide:

- they live outside `.claude/skills/`, `.claude/agents/`, `.github/workflows/`
  and `docs/paths/`, so `scripts/validate-skills.py` never discovers it during
  a normal run;
- every fixture is reached only by an explicit path argument from the test
  suite.

Fixtures include passing and deliberately failing cases. The failing cases
prove that an invalid input is rejected. Decision D43 is the README skill-count
and family-roster reconciliation check; for workflow actions, a SHA pin is a
full commit identifier used to keep the action at a reviewed revision.

Run the two offline self-test suites from the repository root with Python 3:

```powershell
python scripts/tests/test_validator.py
python scripts/tests/test_audit_skill_contracts.py
```

Each command exits with status 0 when its assertions pass. The self-tests use
these synthetic fixtures; they do not execute the separate Scenario A
fresh-session behavioral acceptance.

| Path | Exercises |
|------|-----------|
| `skills/good-skill/` | the whole per-skill path, expected 0 errors |
| `skills/missing-section/` | required-section presence |
| `skills/out-of-order-sections/` | section ORDER, end to end through `validate_skill` |
| `skills/long-description/` | parsed-description length ceiling |
| `agents/*/` | `.claude/agents/` schema (one directory per failure mode) |
| `workflows/*/` | action SHA-pinning |
| `readme/` | the D43 SKILL-COUNT / family-roster reconciliation |
| `paths-tree/` | guided-path + README link resolution, in a miniature repo layout |
| `claude-bridge/` | startup bridge imports and instruction integrity |
| `contract-audit/repo/` | advisory contract-audit detectors and exception fixtures |
