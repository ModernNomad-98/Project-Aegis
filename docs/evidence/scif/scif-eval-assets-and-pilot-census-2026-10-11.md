# SCIF eval assets and the bounded pilot census — 2026-10-11

**What this page is.** The evidence record for the SCIF package's outcome (3)
(fitted eval coverage for the necessity/reuse check) and outcome (4) (a bounded
pilot, where a pilot is genuinely executable). Base
`09a5d2b3c9a3e9e3cff307d94b6f241600e0dc2d`. Fixed sources:
`SCIF-PLAN-rev5.md` (above-footer sha256
`35da913b3f3f856e2287100eb5e50ce6da2e157f217997f58dd129ae301e3bac`, the plan
whose section 3 mandates the assets) and `SCIF-AUDIT-B5.md` (above-footer
sha256 `7710653923b1772f5b818299df45d44135a10587ff36b58a666b899ddda0c595`,
SD-B ACCEPT, zero findings).

**The five sections below are different kinds of evidence and must not be read
as one.** **Assets** are what exists; **static** checks are machine properties
of those files; **deterministic** results involve no model; **actual agent
runs** are the only place an agent's observed behaviour belongs; **UNRUN** is
everything not executed. Standing honesty rules: an unavailable check is
`UNRUN`, never a pass; a receipt is a record, not a gate; and **no rate,
score or "the evals pass" claim is made anywhere on this page.**

## 1. Assets — the five new eval cases (present and well-formed; nothing more)

| # | File | Case id | Type | Plan scenario | Assertions |
| --- | --- | --- | --- | --- | --- |
| 1 | `.claude/skills/risk-tiered-validation-selector/evals/evals.json` | `invalidate-and-re-tier-on-a-changed-input` | `should_trigger` | #2, with the forced-full path of #7 as an assertion set | 4 |
| 2 | the same file | `fast-checkpoint-is-not-a-validation-tier` | `should_not_trigger` | #4 (negative control) | 4 |
| 3 | `.claude/skills/ai-task-decomposer/evals/evals.json` | `reuse-an-accepted-diagnostic` | `should_trigger` | #1, with #6 as an assertion | 5 |
| 4 | the same file | `one-reviewable-change-is-not-a-programme` | `should_not_trigger` | #5 (negative control) | 4 |
| 5 | `.claude/skills/acceptance-criteria-reviewer/evals/evals.json` | `existing-criteria-check-does-not-take-over-ownership` | `should_trigger` | #3, #8 and #9 as one case's assertion set | 4 |

Totals: **+2 / +2 / +1 = 5 cases**, **+21 assertions** (8 / 9 / 4 per file).
The case ids are unique within each file and across the three files. **No
`SKILL.md` is edited**, so no frontmatter, trigger contract, Security
Rules or Stop Conditions surface changes. The claim here is *present and
well-formed* — nothing more.

## 2. Static checks — parse, shape, links, whitespace, validator

| Check | Command (at the candidate head) | Result |
| --- | --- | --- |
| JSON parse, all three eval files | `python -m json.tool <file>` for each | exit **0** each |
| Schema shape | each new case carries `id`, `type`, `prompt`, `expect.triggers` and at least one `expect.assertions` entry | **5/5** cases carry all of them; **21** assertions |
| Markdown links and anchors | `python -B -P scripts/ci/check-markdown-links.py --root . docs/aegis-scif-naming-and-necessity.md docs/delivery-workflow.md docs/README.md docs/reconciliation/step-0-reconciliation-v4.md` | `files: 4   links checked: 138   anchors checked: 92   broken: 0   dead: 0   external-skipped: 6   other-skipped: 0`, exit **0** |
| Whitespace | `git diff --check` | no output, exit **0** |
| Skills validator | `python -B -P scripts/validate-skills.py` | `OK: 205 skill(s) valid, 0 warning(s)`, exit **0** |
| Validator self-tests | `python -B -P scripts/tests/test_validator.py` | `OK: 181 gate self-test assertion(s) passed.`, exit **0** |
| DCO sign-off | `python -B -P scripts/check_dco.py --range <base>..HEAD` | the exact output is in this PR's Stage C record |
| Protected paths | the live `gate_pattern` extracted from `.github/workflows/validate-skills.yml:545`, applied to the eight changed paths | **clear** for all eight; `gate-guard` is expected green |

## 3. Deterministic results — the bounded pilot (offline; no model)

**The pilot is the local, offline, read-only `census` at a pinned
revision.** Nothing in this section involves a model, a provider, a live session
or the network. Command, run in the Stage C clone:

```text
python -m tools.behavioral_eval_runner census --repo . --ref <pinned revision> --out <a scratch path outside the repository>
```

**Pinned base `09a5d2b3c9a3e9e3cff307d94b6f241600e0dc2d`** — exit **0**;
1,176,179 bytes of JSON written outside the repository; the tool's own
`census_sha256` =
`afcaa814b3a7a0e8e54a720fdf5e71d8ac4414bfa8d674f88c46595a4c2456d1`; the
written file's whole-file sha256 =
`3b01b5d9dcaa137ee8cf533834e041cecc5f1c4a8461f2707c64c0071af171f8`:

| Figure | At the base |
| --- | --- |
| `runner_version` / `schema_version` | `0.1.0-wp2b1` / `1.0.0-wp2b1` |
| `source_commit` / `source_tree` | `09a5d2b3c9a3e9e3cff307d94b6f241600e0dc2d` / `cefc3471f2864175565a492bca72f0e0534fa3fe` |
| `behavior_cases` | **1329** |
| `behavior_eval_files` | **205** |
| `trigger_eval_files` | 203 |
| `assertions_total` | **4192** |
| `should_trigger` / `should_not_trigger` | 969 / 360 |
| `risk-tiered-validation-selector` | 6 cases, 17 assertions |
| `ai-task-decomposer` | 8 cases, 19 assertions |
| `acceptance-criteria-reviewer` | 8 cases, 18 assertions |
| `shipped_skills` | 205 |

**After the case additions.** The same command re-run at the committed head with
the same offline, read-only profile:

| Figure | At the head | Delta |
| --- | --- | --- |
| `behavior_cases` | **1334** | **+5** |
| `assertions_total` | **4213** | **+21** |
| `behavior_eval_files` | **205** | **0** |
| `risk-tiered-validation-selector` | **8 cases** | **+2** |
| `ai-task-decomposer` | **10 cases** | **+2** |
| `acceptance-criteria-reviewer` | **9 cases** | **+1** |

The head's `source_commit`, `source_tree`, `generated_at`,
tool `census_sha256` and the written JSON's whole-file sha256 are recorded
in this PR's Stage C record, **not in these bytes**: a commit cannot name its own
SHA, its own tree, or the digest of a file whose content contains them. The delta
figures do not depend on that limit — they are a function of the three eval
files, which are fixed in the same commit.

**Also deterministic and reported here:** `python -m tools.behavioral_eval_runner version`
→ `runner_version 0.1.0-wp2b1`, `schema_version 1.0.0-wp2b1`,
`work_package WP-2B-1`, `authorization_id BER-DEC-006`, exit 0;
`self-check` → `self_check: PASS` (21 checks, every one PASS),
`live_dispatch: DISABLED`, exit 0; `capabilities` →
`claude_code_adapter` activation observation `UNAVAILABLE` with its
recorded disposition — the runner still reports that it cannot start a live
session.

**Not run here, and why:** `preflight`, `schedule`,
`grade-fixture` and `verify-evidence` each require a declared input
this change does not have (`--manifest`; `--selection`;
`--grader`/`--plan`/`--evidence`; `--root`), and
`materialize` writes and needs a genuinely fresh or empty destination. They
are `UNRUN` (section 5) — not failures, and not passes.

## 4. Actual agent runs — the only place agent observation belongs

Today this section holds **the SCIF lane's own usage**, not an eval execution:

- **Stage A (plan author, `scif-planner-a-rev5`, round 5)** wrote
  `SCIF-PLAN-rev5.md` (above-footer sha256 `35da913b…e3bac`),
  which designs the check and the five fitted cases. The plan does **not** carry
  a separate self-application answer set: the check is not yet normative at that
  revision, so there was nothing for it to answer. Recorded as **not applicable
  at that revision** — not as a pass.
- **Stage B (plan auditor, `scif-auditor-b5`, round 1)** audited that
  revision against its five mandated items and returned **SD-B ACCEPT, zero
  findings** (`SCIF-AUDIT-B5.md`, above-footer sha256 `77106539…0c595`).
  Its audit did not test five-question answers, for the same reason; it tested
  the plan's hash, its remedies, its minimal-diff claim, its rev4 core and its
  citations.
- **Stage C (implementer, `scif-implementer-c2`, round 1)** applies the
  new rule to this PR itself: the five-question answers are in the PR body's
  Plan section, and this stage ran the census above. Its own skills rows are
  authored in its SD-C record.
- **Stage A/B skills rows** are owed by their own authors and bound to the two
  fixed sources above. They are not authored here and cannot be paraphrased into
  existence.

**No eval case has been executed by any agent.** No session was given a case's
prompt, no output was graded, and nothing here observes whether an agent obeys
the new normative sentence. That is section 5's second item.

## 5. UNRUN — everything not executed, and what would resolve it

| Unrun item | What it is | What would resolve it |
| --- | --- | --- |
| **Scenario #10 as a case** | "Required independent stage or exact-head review missing — never trade it for speed": the plan fits **no** asset to it (plan section 5.1, row 10). | The rule is carried by the new normative subsection and evidenced by the existing stage-separation and exact-head rules; a fitted case would need a scenario where an agent is offered a missing stage as a shortcut. Not invented here. |
| **Every one of the five new cases, as an execution** | The cases are present and well-formed; none has been run by an agent. | A fresh session given the skill's `SKILL.md` and the case prompt verbatim, graded by a separate fresh instance against the case's own assertions ([skill-eval-behavioral-test-procedure](../../skill-eval-behavioral-test-procedure.md), steps 3–6). No rate and no score may be claimed until then. |
| **"Does an agent obey the new sentence?"** | The normative subsection is procedural; nothing machine-enforces it, and no observation of model behaviour exists. | The same fresh-session run above, plus the enforcement account's own limit (no runner can see which agent held which stage). |
| `preflight`, `schedule`, `grade-fixture`, `verify-evidence` | Declared-input commands; no such input is named for this change. | A named manifest, selection, grader/plan/evidence triple or evidence-bundle root, at a pinned revision. |
| `materialize` | Writes; it needs a genuinely fresh or empty destination. | A fresh destination outside the repository, declared before the run. |
| Any provider-backed execution, live session, measured calibration or Scenario A run | Not available to the offline core (`live_dispatch: DISABLED`). | Their own gates (the skill-eval harness execution-path decision; the BER backlog). Not claimable here. |

**Nothing on this page is a verdict.** Stage D re-derives the figures, Stage E
reproduces them, and a later reader re-runs the commands instead of trusting this
page.
