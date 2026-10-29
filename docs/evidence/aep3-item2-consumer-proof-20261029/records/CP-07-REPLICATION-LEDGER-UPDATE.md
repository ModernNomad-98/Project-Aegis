# LEDGER UPDATE — CP-05, CP-07, CP-18

**Base ledger:** `_A/work-package-3/item2-cp-ledger/CP-LEDGER.md` (202 lines, 21,278 bytes),
as changed by `_A/work-package-3/item2-cp-closeout/LEDGER-UPDATE.md` (7 PASS / 12 UNRUN /
3 BLOCKED). Neither file is edited; this is a new file carrying only the three rows this task
re-adjudicated. Unlisted rows keep their current verdict.

**Change set:** CP-07 moves from BLOCKED to **PASS**. CP-05 moves from BLOCKED to **UNRUN**
(its U8 blocker is gone, but its decisive clause is not observable in this repository). CP-18
stays **UNRUN** with a new, exact basis. No row moves to FAIL. Denominator stays 22;
NOT-APPLICABLE stays 0.

---

| Case | Old verdict | New verdict | Decisive observation | Evidence |
| --- | --- | --- | --- | --- |
| CP-05 fresh consumer startup | BLOCKED (U8 not granted) | **UNRUN** | A genuinely new `claude -p` session given only the repository URL and "Resume." reports **Role B**, classifies it from the absent source landmarks rather than from `.claude/skills`, makes **no sibling-app redirect** and claims **no source authority**. It does **not** report **Stage 0**, and cannot truthfully: the repository has 19 base files, a live release A and a built release B. The Stage 0 clause is the decisive one and is absent | `evidence/cp05-startup-readback.md`, `cp05-session.jsonl` (session `c00a03db`), `cp05-reads.json` |
| CP-07 routing / manual-only triggers | BLOCKED (U8 not granted) | **PASS** | 20/20 installed owner/content paths reachable and SHA-256-equal to the manifest (18 skill owners + `AGENTS.md` + `CLAUDE.md`); routing text quoted with line numbers from the copied bytes; the five manual-only trigger classes recorded present/absent and invoked/not-invoked **before** any invocation; 0 invocations; U4 not exercised; no override register exists, and none was needed | `evidence/cp07-routing-ledger.md`, `cp07-routing-ledger.json` |
| CP-18 new-agent recovery | UNRUN (no new session) | **UNRUN** (new basis) | A second new session derives **state** (branch, HEAD `338ba82`, parent `7954d8a`, `main` `390363f`, 41 files, manifest hash), **decisions** (release A live, B built but not deployed, SDP-1) and **authority** (owner conditions + owner record), and writes nothing. It does **not** derive the **next action**: "No in-repo file says what to do next … That is my inference". Missing dependency: a durable next-action record (`docs/project-state.md` or equivalent) | `evidence/cp18-recovery.md`, `cp18-session.jsonl` (session `6ff5bc92`), `cp18-reads.json` |

---

## Totals after this update

| Verdict | Count | Cases |
| --- | ---: | --- |
| PASS (observed) | **8** | CP-04, CP-07, CP-08, CP-09, CP-10, CP-13, CP-14, CP-16 |
| UNRUN | **13** | CP-01, CP-02, CP-03, CP-05, CP-11, CP-12, CP-15, CP-17, CP-18, CP-19, CP-20, CP-21, CP-22 |
| BLOCKED (owner) | **1** | CP-06 |
| NOT-APPLICABLE | **0** | forbidden by the freeze |
| Total | 22 | denominator unchanged |

---

## Notes that must travel with these rows

1. **CP-05 is not one observation short of a PASS by accident.** Its acceptance sentence asks a
   new session to report Role B **and Stage 0**. The repository is past Stage 0; the honest
   readback says so. Two ways to close it: run the readback against a genuinely fresh,
   Stage-0-shaped consumer repository seeded with the installed starter, or revise the CP-05
   sentence for a repository that already carries releases. Until one of those happens, PASS
   would require claiming an observation that did not occur.
2. **CP-07's PASS rests on bytes, not on an agent's behaviour.** Reachability is proved by path
   + hash against the manifest; the trigger ledger is quoted from the copied files. The row's
   "invoked/not-invoked" column is all "not invoked", which is the state the case requires
   before any invocation.
3. **CP-18's gap is a repository artifact, not a session failure.** The session re-derived the
   manifest hash and the install counts on its own; it stopped short only where the repository
   has no record to derive from. If a reviewer accepts a candidate next action plus one
   question as "derives the next action", the row can move to PASS on the same transcript; this
   update does not make that call.
4. **The plan's "10 skill owners" is wrong.** The manifest has 18 `SKILL.md` owners. CP-07
   enumerates 18. A later reviewer using the plan's number would under-count the routing surface.
5. **Nothing here changes the U6 picture.** U6 still waits on every non-browser CP row being RUN
   with a recorded verdict (CP-05 and CP-18 are still UNRUN), the R-series end state and the
   closeout.

**Model:** DeepSeek (deepseek-flash).
