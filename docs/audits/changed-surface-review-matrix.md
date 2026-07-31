# Changed-surface review matrix — AEGIS remediation program

Every PR in the AEGIS-001..059 remediation program classifies its changed
files against this matrix and runs the owning INDEPENDENT review for each
surface class it touches. "Independent" means an isolated review session
against the actual diff — never the authoring session grading its own work
(the AEGIS-061 candidate finding). A REQUEST CHANGES verdict from an owning
reviewer blocks the batch's completion until resolved.

Mechanical gates prove objective facts; the reviewer skills own semantic
judgment. Neither substitutes for the other.

| Changed surface | Mechanical gate(s) | Owning independent reviewer skill(s) | Notes |
|---|---|---|---|
| `.claude/skills/**` (shipped skill contracts, references, evals) | `scripts/validate-skills.py`; `scripts/audit-skill-contracts.py` (report-only) | `skill-quality-reviewer` per changed skill; `library-diff-reviewer` for the whole skill-changing PR | Semantic trigger/substance quality is NEVER mechanically certified |
| `.claude/agents/**` (reviewer subagents) | validator `check_agents_schema` (read-only tool set is HARD) | `library-diff-reviewer`; `security-pr-reviewer` when a tool grant widens | A tools widening is a privilege escalation, not a preference |
| `scripts/*.py`, `scripts/tests/**` (gate + audit tooling) | self-test suites (`test_validator.py`, `test_audit_skill_contracts.py`); gate-guard (RED by design on `scripts/tests/`, `scripts/validate-skills.py`, `scripts/check_dco.py`) | `code-reviewer` (correctness + tests); `security-pr-reviewer` when security-sensitive | ⚠ gate-guard's path filter does NOT currently cover `scripts/audit-skill-contracts.py` or `scripts/audit-rules.yaml` — see AEGIS-061 (candidate) |
| `scripts/audit-rules.yaml` (audit POLICY) | catalog loader fails closed (missing fields, unknown detectors, dead fixtures); self-tests | `code-reviewer` (detector semantics); `agent-governance-audit` (does the cited authority really own the rule?) | Policy changes are program-governance changes, not tooling tweaks |
| `.github/workflows/**`, `.github/CODEOWNERS` | gate-guard RED by design; workflow SHA-pin check (validator) | `security-pr-reviewer`; `agent-governance-audit` | Human admin merge only |
| `docs/audits/**` (frozen evidence, registers, this matrix) | hash statements in the docs themselves; link checks | `agent-governance-audit` (evidence integrity, approval trail) | Frozen baselines are append-only history: corrections are new dated entries |
| `artifacts/audits/**` (generated baselines, graph, queue) | regenerated ONLY by the engine; deterministic (no timestamps; corpus content hash embedded) | `code-reviewer` alongside the engine/catalog change that regenerated them | A hand-edited artifact is a falsified baseline |
| `docs/**` (other), `README.md` | validator D43 count markers; D55 guided-path link checks | `library-diff-reviewer` | Current-state totals live only in the README marker pair (D59 rule) |
| `CLAUDE.md`, `AGENTS.md` (startup contracts) | validator `check_claude_bridge` (HARD, D61) | `agent-governance-audit`; `security-pr-reviewer` (behavior-steering surface) | Behavior-steering files are outside the approved-write exception (standard §5) |

## Program rules this matrix encodes

1. **No self-certification.** The session that authored a change never
   supplies its only review. Owning reviewers run in isolated sessions
   against the actual diff (AEGIS-061 candidate; this matrix is its first
   control).
2. **Verdicts are reported separately, per reviewer,** never merged into a
   single "validated" claim (program rule: separate proof types).
3. **Semantic queue, not inline sweeps.** Corpus-wide semantic review is
   executed from the structured queue
   (`artifacts/audits/semantic-review-queue.json`), cluster by cluster —
   never by manually walking all skills in one conversation.
4. **Behavioral evals are UNRUN** until the AEGIS-018 runner exists, and are
   always reported as such.
