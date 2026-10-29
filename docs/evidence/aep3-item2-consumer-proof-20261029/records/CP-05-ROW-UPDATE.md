# CP-05 row update — fresh consumer startup — **revised criterion**

**Base records, none edited by this file:**
`_A/work-package-3/item2-cp-ledger/CP-LEDGER.md` (CP-05: BLOCKED at line 62),
`_A/work-package-3/item2-cp-replication/LEDGER-UPDATE.md` (CP-05: UNRUN),
`_A/work-package-3/item2-cp-closeout/CP-CLOSEOUT-RECORD.md`,
`_A/work-package-3/item2-cp18-closure/evidence/cp18-row-update.md` (latest totals: 9 PASS /
12 UNRUN / 1 BLOCKED).

**Change:** CP-05 moves from **UNRUN** to **PASS**, scored against the revised sentence and
labelled **revised criterion** (revision entry: `PLAN-REVISION-CP05.md`, owner decision
CP-05 = B, 2026-10-29). Denominator stays 22; NOT-APPLICABLE stays 0.

| Case | Producer | Old verdict | New verdict | Criterion | Evidence | Decisive observation |
| --- | --- | --- | --- | --- | --- | --- |
| **CP-05** fresh consumer startup | S4a | **UNRUN** (Stage-0 clause absent) | **PASS — revised criterion** | revised sentence (Stage-0 clause removed): a new session given only the repository location and a resume request reports consumer Role B on the current consumer repository, with no sibling-app redirect and no inherited source authority | `item2-cp-replication/evidence/cp05-startup-readback.md` (7,998 B, `9270fdb4…`), `cp05-session.jsonl` (94,306 B, `db26f39b…`, session `c00a03db`), `cp05-reads.json` (4,046 B, `5c50d621…`), `cp05-prompt.txt` (74 B, `3896883c…`), this package's `evidence/` | A genuinely new `claude -p` session (id `c00a03db-5ac6-4cb5-b74e-eb5e393ed7f8`, model `claude-sonnet-5-5`) was given only the repository URL and "Resume.", and reported: "**Role:** this is your product repository, not the Aegis source library … The Aegis skills here are copied tools." It proposed no sibling app and claimed no source authority. Stage 0 was **not** reported — and the revision removes that clause |

This is a **re-score of a retained observation, not a re-run**. No new session was started for
this update; the transcript, prompt, ordered reads and hashes are the ones recorded on
2026-10-28/29 by the replication turn.

---

## 1. The revised sentence, as scored

> On the current consumer repository, a new session given only the repository location and a
> resume request reports consumer Role B, with no sibling-app redirect and no inherited source
> authority.

Derived from the plan row by removing "and Stage 0" and adding the owner's locality qualifier;
the derivation and its exact diff are in `PLAN-REVISION-CP05.md` §2.2.

## 2. Clause by clause — observed or not

| Clause | Observed? | Basis (all quotes verbatim from the transcript) |
| --- | --- | --- |
| **On the current consumer repository** | **yes** | Fresh clone of `https://github.com/ModernNomad-98/aegis-consumer-proof`, branch `aep3-i2/startup-readback` at `338ba82`; the branch and commit are still live at the provider (checked 2026-10-29T06:24-07:00, `evidence/RP-04`). See §4 L1 for what "current" does and does not cover. |
| **Given only the repository location and a resume request** | **yes** | Prompt is 74 bytes, byte-identical to `evidence/cp05-prompt.txt`, SHA-256 `3896883c…`: `Repository: https://github.com/ModernNomad-98/aegis-consumer-proof` + `Resume.`. No task, no case ID, no role, no mention of Stage 0. |
| **Reports consumer Role B** | **yes** | "this is your product repository, not the Aegis source library. Only `README.md` exists of the five landmark files, and it opens `# Checklist`, not `# Project Aegis`." Reached from the README title and the absent source landmarks — not from the presence of `.claude/skills`, which the same sentence calls "copied tools". |
| **No sibling-app redirect** | **yes** | The session works in the cloned repository; it proposes no second or sibling product directory anywhere in the final answer. Its three offered next steps are all in-repo (run the readback here; open a PR; work on the checklist site or release evidence). |
| **No inherited source authority** | **yes** | It denies the source-library role explicitly and attributes the skills to the consumer copy ("copied tools"). It claims no release, deploy or merge authority, and wrote nothing. |
| ~~Reports Stage 0~~ | **no — clause removed by the revision** | The answer never says Stage 0. It reports the branch, the last two commits and a candidate next step instead. Under the original sentence this was the decisive gap; under the revised sentence there is no such gap. |
| No writes | **yes** (as recorded) | No write tool was used: the transcript contains 9 tool calls, all `Bash` (5), `Glob` (3) and `Read` (1). The record states `git status --porcelain` was empty before and after; that reading is the session's own, not re-taken here. |
| No recap needed | **yes, with a caveat** | It derived branch, HEAD, the last two commits and its role itself, then asked "Which should I resume?" — a task-selection question, not a request to be told its own state. The judgement is disclosed as a judgement in §4 L5. |

## 3. Why PASS and not UNRUN, and why not FAIL

**Not UNRUN.** UNRUN was correct while the sentence demanded Stage 0: the clause was absent, and
its absence was a property of the repository, not of the run. The owner has removed that clause.
Every remaining clause has a retained, verbatim, hashed observation. Nothing decisive is
missing, so UNRUN would now understate the evidence.

**Not FAIL.** The plan's S4a fail condition is "Redirect to a sibling app, inherited source
authority, or a recap needed → FAIL, record" (`CONSUMER-RELEASE-PLAN-v4.md` line 258). None of
the three occurred: no sibling app, no inherited authority, and the closing question is a
task-selection question asked *after* the session had derived its own state. The third element
is a judgement call and is disclosed as one; it is also outside the revised sentence, which
carries no recap clause.

**Not a manufactured observation.** The run was not repeated and no clause is inferred from the
record's own summary: the transcript, the prompt bytes and the ordered reads are retained and
hashed, and the quotes above are extracted from the transcript, not from the prior record's
prose.

## 4. Limits — what this PASS does not cover

**L1 — currency of "the current consumer repository".** The readback was taken at
`aep3-i2/startup-readback` `338ba82`. At the provider today (2026-10-29T06:24-07:00):

| Ref | Commit | Carries the installed starter? |
| --- | --- | --- |
| `refs/heads/aep3-i2/startup-readback` | `338ba824…` | yes — 41 installed root files + `docs/consumer-install-record.md` (the observed tree) |
| `refs/heads/aep3-i2/next-action-record` | `3998af11…` | yes — `338ba82` + `docs/project-state.md` + one line in `docs/evidence/index.md` |
| `refs/heads/main` | `4f312931…` | **no** — 19 files, no `CLAUDE.md`/`AGENTS.md`/`.claude/skills`; main has since taken the CP-12 guard merge |

So the observation is on the install branch, not on `main`, and one commit behind the newest
install-state head. It is not re-run at `3998af1` here. What can be said without a new session,
and is checked in `evidence/RP-04` §2: at `3998af1` three of the four source-package landmarks
`AGENTS.md` line 5 names are still absent (`docs/skills-catalog.md`, `scripts/validate-skills.py`,
`artifacts/audits/skill-contract-audit-baseline.json`) and `README.md` still opens `# Checklist`,
so the Role B basis is unchanged by that commit. That is a static check of a tree, **not** a new
behavioural observation, and it is not presented as one. If a reviewer reads "current" as "the
newest install-state commit", one fresh readback at `3998af1` (~5 min) closes the gap.

**L2 — change control.** The freeze's §4 requires an R2 with independent review and new digests
before a reworded acceptance is used after a result exists. This revision does not re-freeze;
the PASS is labelled `revised criterion` for exactly that reason and must not be counted against
`case_set_sha256` `48a28ba1…` until that step is recorded. See `PLAN-REVISION-CP05.md` §5.

**L3 — evidence location.** The plan's CP-05 row names
`docs/evidence/closeout/startup-readback.md` in the consumer repository. No such file exists
there: the observation record is in the planning workspace at
`_A/work-package-3/item2-cp-replication/evidence/cp05-startup-readback.md`, and the install
record discloses that the CP-05/07/18 observations are recorded outside the repository. The
observation is retained and hashed; its planned location is not. A reviewer who requires the
artifact in the consumer repository would need one content commit.

**L4 — harness.** "Given only the repository location" is exact for the prompt, not for the
harness: the CLI loaded its own user-level plugins and one user-level skill
(`source-of-truth-reconciler`, visible in the `system/init` event). Disclosed by the prior
record and re-confirmed from the transcript here.

**L5 — the closing question.** "Which should I resume?" with three options is read as task
selection, not as a request for a recap of its own state. It had already stated the branch, the
commits, the role and a candidate next step. A reviewer who reads any closing question as "a
recap needed" would have to FAIL the row; that reading is not adopted, and the reason is stated
rather than hidden.

**L6 — one session, one model, one run.** `claude-sonnet-5-5`, one `claude -p` process, one
transcript. Not a human session and not presented as one. `gh` was denied in that session (4
permission-denied events), so "no PR" is its own caveat, not an observation of this record.

**L7 — reviewer independence.** The plan assigns CP-05 verification to RV-5. This re-score was
performed by an agent that did not run the observed session, but it is **not** an RV-5
verification and does not fill that role. The freeze's roll-up rule 4 (a PASS needs a reviewer
independent of the actor) is therefore satisfied only in the narrow sense that the scorer and
the observed session are different agents; the formal RV-5 review remains open.

## 5. Totals if this row is applied

Arithmetic from the last recorded totals (`item2-cp18-closure/evidence/cp18-row-update.md`:
9 PASS / 12 UNRUN / 1 BLOCKED), changing **only** CP-05. Not a re-adjudication of any other row;
CP-12 in particular stays UNRUN pending its merged-main re-run.

| Verdict | Count | Cases |
| --- | ---: | --- |
| PASS (observed) | **10** | CP-04, **CP-05 (revised criterion)**, CP-07, CP-08, CP-09, CP-10, CP-13, CP-14, CP-16, CP-18 |
| UNRUN | **11** | CP-01, CP-02, CP-03, CP-11, CP-12, CP-15, CP-17, CP-19, CP-20, CP-21, CP-22 |
| BLOCKED (owner) | **1** | CP-06 |
| NOT-APPLICABLE | **0** | forbidden by the freeze |
| **Total** | **22** | denominator unchanged |

One of the ten is not like the others: CP-05 is PASS **only** under the revised criterion and
carries the L2 label. A matrix total that mixes it with PASS rows scored against R1 text would
overstate what the frozen set measured.

## 6. What this update does not do

- It does not re-run CP-05, and it starts no session.
- It does not touch CP-07, CP-18 or any other row.
- It does not edit `CP-LEDGER.md`, `LEDGER-UPDATE.md`, the closeout record, the plan, the freeze
  or `cases.json`.
- It does not close U6: the remaining non-browser rows are still not all RUN, and the R-series
  end state and closeout are unchanged.
- It does not fill the RV-5 reviewer slot (L7).

**Model:** DeepSeek (deepseek-flash). The observed session's model is `claude-sonnet-5-5`.
