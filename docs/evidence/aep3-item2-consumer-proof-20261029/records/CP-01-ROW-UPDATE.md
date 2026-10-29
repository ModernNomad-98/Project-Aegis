# CP-01 row update — paste-ready replacement for CP-LEDGER.md

**What this file is.** The CP-01 observation made on 2026-10-29 changes one row of `_A/work-package-3/item2-cp-ledger/CP-LEDGER.md`. This file carries the exact replacement text so the ledger can be edited without re-deriving anything. It does not itself edit the ledger.

| item | before | after |
| --- | --- | --- |
| CP-01 verdict | UNRUN | **PASS** |
| Totals | PASS 5 / UNRUN 14 / BLOCKED 3 | **PASS 6 / UNRUN 13 / BLOCKED 3** |
| Denominator | 22 | 22 (unchanged) |
| NOT-APPLICABLE | 0 | 0 (unchanged) |

---

## 1. Replacement for the CP-01 row in §3 (line 58)

> | CP-01 host capability | S0, S2 | **PASS** | E-06, E-08, E-09, E-34, E-35, E-36, E-37 | A genuinely new coding session (OpenAI `gpt-6-astra`, `codex exec` CLI 0.163.0-alpha.10.2, thread `01a187dc-7a82-79b1-8680-d72b53899da9`) started cold in a fresh clone of `aep3-i2/startup-readback` at `338ba82` with an 863-byte business prompt and no answer key (0 workspace paths in the clone). It discovered and read `AGENTS.md`, `CLAUDE.md` and the startup skill, classified **Role B** from landmark absence, and read back 13 rules with line anchors — all 13 passages verified verbatim in the cited bytes, 7 anchors exact and 6 off by 3–31 lines. It then executed a read-only 41-row integrity check: **0 writes**, clean tree, exit 0. Independent review contexts are the non-author CP-08 and CP-10 reviews. Residual: the "before investing in the build" ordering cannot be shown retroactively (note N-6). | — (see note N-6) |

---

## 2. New note for §4

> **N-6 — CP-01.** The three named components are observed, not inferred: discovery/readback is a transcript of file reads plus quotations that were re-checked against the bytes by the adjudicating session; "independent review contexts" rests on the same non-author reviews that already carry CP-08 and CP-10; the new session is a separate process with a new thread id, a cold prompt and no fork. Two limits are recorded rather than hidden. First, the frozen sentence places the demonstration "before investing in the build", and releases A and B already exist — the mechanism is shown to work, the original ordering cannot be recovered. Second, the PATH CLI on this host (0.149.1) cannot use the configured model; the session used the newer binary bundled with the installed Codex app, so a host with only 0.149.1 cannot start this session at all. If the owner requires the strict temporal reading, this row reverts to UNRUN on that clause alone.

---

## 3. Replacement for the §2 totals table

| Verdict | Count | Cases |
| --- | ---: | --- |
| **PASS (observed)** | **6** | CP-01, CP-08, CP-10, CP-13, CP-14, CP-16 |
| **UNRUN** | **13** | CP-02, CP-03, CP-04, CP-09, CP-11, CP-12, CP-15, CP-17, CP-18, CP-19, CP-20, CP-21, CP-22 |
| **BLOCKED (owner decision required)** | **3** | CP-05, CP-06, CP-07 |
| **NOT-APPLICABLE** | **0** | forbidden by the freeze; not used |
| **Total** | **22** | denominator unchanged |

---

## 4. §5 group table — the "needs a genuinely new session" line

Before: `| Needs a genuinely new session | CP-01, CP-18 | a new coding session was never started; forking is disqualified |`

After: `| Needs a genuinely new session | CP-18 | a new session now exists and closes CP-01; CP-18 still fails its own decisive clause — no durable next-action record exists in the repository, so the receiver cannot derive the next action (the CP-01 session said so itself) |`

---

## 5. §7 STATUS block — replacement text

~~~text
ITEM 2 / CP LEDGER — CP-01 closed on an observed session; 21 rows unchanged by this update.
PASS observed (6): CP-01 host capability, CP-08 plan acceptance, CP-10 code/pipeline reviews,
CP-13 delivery configuration, CP-14 recovery readiness, CP-16 exact B release.
UNRUN (13): CP-02, CP-03, CP-04, CP-09, CP-11, CP-12, CP-15, CP-17, CP-18, CP-19, CP-20, CP-21, CP-22.
BLOCKED on owner (3): CP-05 and CP-07 (U8), CP-06 (A-13 and the four Stage 2 outcomes).
CP-01 evidence: new OpenAI codex session 01a187dc, cold clone at 338ba82, 0 writes, exit 0;
discovery/readback verified quote-by-quote; residual = the "before the build" ordering (N-6).
New-session-only remaining: CP-18. Browser-only: CP-11, CP-15, CP-17, CP-20. Closeout: CP-22 (+U6).
Live state unchanged by this update: no dispatch, no deploy, no settings change, no consumer write.
~~~

---

## 6. New rows for the §6 evidence register

| Ref | Path | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| E-34 | _A/work-package-3/item2-cp01/CP-01-RECORD.md | 16,857 | 67691b4fe6699c7f2ed0a38e84dab8bb9cf82cdeb46aa4090c9660f1accc3e46 |
| E-35 | _A/work-package-3/item2-cp01/SESSION-TRANSCRIPT.md | 58,005 | 2907c8eee347d7dade6560f463ae691aa6cef6c454e85a13fa5c42c038374e48 |
| E-36 | _A/work-package-3/item2-cp01/evidence/session.jsonl | 259,611 | 3cdcbac33b0306e0518588555b8aecd92d0f9fadf9c3d103ab2839a771ee5d2c |
| E-37 | _A/work-package-3/item2-cp01/READ-LEDGER.json | 24,210 | bfc11e8d9cbe41c6f64456a31b6ca10618c38520df96061be7c44f8e2715a50a |
| E-38 | _A/work-package-3/item2-cp01/evidence/denied-provider-attempts.json | 4,764 | fea537fb86f38975dbe2f69215e83767fcfa40310f3a98352440b7fd8e358ca6 |

---

## 7. What this update does not do

- It does not edit `CP-LEDGER.md`; that file is an adjudication record and its next revision is a Lead decision.
- It does not touch CP-18. A new session that *runs* is not a new session that *recovers*; the repository still has no durable next-action record.
- It does not re-open CP-05/CP-06/CP-07, and it changes no evidence hash already in the register.
