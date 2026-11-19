# Owner operating-mode policy (2026-11-18)

**Status:** policy-of-record for the owner's standing operating-mode answers, transcribed from the owner's reply of 2026-11-18 and the owner's explicit adoption instruction of 2026-11-19. **This file is not an entry in the owner approval register and creates or widens no authority**; it records the owner's words, and the owner's words govern.

**Source capture.** The owner's T-14 answer text below is stored verbatim in the session evidence file `C:/tmp/aegis-t15-evidence-2026-11-18/t14/owner-answers-2026-11-18.txt` (1,925 bytes, sha256 `b0749ad998fcead9fcfe373d1dfc8b00c182ef657f9c8d9382c7ab435f088e15`). The 2026-11-19 instruction is stored in `owner-instruction-2026-11-19.txt` (116 bytes, sha256 `839a0accbd4a5b2e858db92cb845d576565bb24a0b600ec10e0f282a3300c792`). The exact time of the 2026-11-18 reply was not recorded in the session decision log (D-86 records the date); the text is preserved, not reconstructed.

## Owner's T-14 answers, verbatim (2026-11-18)

```text
Owner reply — T-14 owner answers (recorded 2026-11-18; session record D-86)

TABLED 2 — T-14: OWNER ANSWERS (record verbatim as owner decisions)
- T14-D1: D — local work, PR and merge.
- T14-D2: C — standing merges: merge on green (D-52) and admin merge under D-64 as amended above. No deploy or release; no arming GitHub auto-merge.
- T14-D3: Plan audits: two rounds, then proceed with your recommendation and record dissent. Code review: the D-52 two-round cap; at the cap or a third REVISE, park that item, table it and continue independent work. No unresolved P1 is ever merged. "Round" = one REVISE → fix → re-review cycle; "candidate" = one published PR head (resolves T14-C2).
- T14-D4: A — three candidates per change; a fourth is tabled for me.
- T14-D5: B — if Codex is unavailable for the exact head, a fresh Claude Code CLI session (different vendor from the Lead) is the pre-authorised fallback reviewer; record the gap.
- T14-D6: B — the approval register, the AGENTS.md authority rules and my 2026-11-18 operating-mode direction together are the authority floor.
- T14-D7: B — standing approval, review by 2026-12-31. "stop everything" suspends it instantly; "resume all" resumes it. Restate the grant at each session start.
- T14-D8: B — local evidence and RUN-LOG, plus PR receipts and disposition comments on GitHub.
- T14-D9: already running since my 2026-11-18 direction; record that as the start.
- T14-D10: A — Project Aegis (Role A) only.
- T14-D11: A — park the item, continue independent work.
- T14-C1…C8 are resolved by these answers; for T14-C3, the five MG conditions plus D-64 apply.
Then write the adopted policy into the repository where a fresh agent will find it, as its own D0-4 item: plan → fresh audit confirming every sentence traces to these answers and widens nothing → PR. This PR defines your own authority: open it, then table the merge for my read.
```

## Owner's adoption instruction, verbatim (2026-11-19)

```text
Owner instruction, 2026-11-19 (received in the active Aegis session; quote verbatim with this source): "merge t-14"
```

## Operative policy

1. **Authority floor (T14-D6).** The owner approval register, the `AGENTS.md` authority rules, and the owner's 2026-11-18 operating-mode direction together are the authority floor. This file is not a register entry and creates no grant; every paraphrase below yields to the verbatim owner text above.
2. **Delivery mode (T14-D1).** Work is local: implement in this repository, open a PR, and merge it here.
3. **Merging (T14-D2).** Merge on green under D-52 (the owner's phrase; see the limitation in item 15) and admin merge under D-64 as amended, recorded on `main` as **AEGIS-APR-175**. No deploy, no release, and no arming of GitHub auto-merge. GitHub PR receipts and disposition comments required by T14-D8 remain permitted and required.
4. **Merge-gate conditions (T14-C3).** Every merge under this mode also meets the five merge-gate conditions **MG1–MG5** in `docs/delivery-workflow.md` (pointer only; not restated here) plus D-64/AEGIS-APR-175 where an admin merge is used.
5. **Review caps and definitions (T14-D3).** Plan audits: two rounds, then proceed with the recorded recommendation and record dissent. Code review: the D-52 two-round cap; at the cap or a third REVISE, park that item, table it, and continue independent work. No unresolved P1 is ever merged. 'Round' = one REVISE → fix → re-review cycle; 'candidate' = one published PR head.
6. **Candidate budget (T14-D4).** Three candidates per change; a fourth is tabled for the owner.
7. **Reviewer fallback (T14-D5).** If Codex is unavailable for the exact head, a fresh Claude Code CLI session (different vendor from the Lead) is the pre-authorised fallback reviewer; the gap is recorded in the PR evidence.
8. **Standing approval (T14-D7).** Standing approval, **review by 2026-12-31** — a review date, not an expiry; what happens at that date is the owner's decision. It covers only the operating mode in items 2–7 and 9–11 and adds no new grant. 'stop everything' suspends it instantly; 'resume all' resumes it; at each session start the operating mode is restated.
9. **Evidence (T14-D8).** Local evidence and RUN-LOG, plus PR receipts and disposition comments on GitHub.
10. **Start and scope (T14-D9/D10).** The start is recorded as 2026-11-18, the date of the operating-mode direction. Scope is Project Aegis (Role A) only; consumer repositories do not inherit this policy.
11. **Blocked work (T14-D11).** Park the item and continue independent work.
12. **Owner-reserved items, each with its source.** (a) Required checks, workflows, gate-guard, branch protection and the approval mechanism: AEGIS-APR-175 'Scope FORBIDDEN' on `main`. (b) Deploy, release and arming auto-merge: T14-D2 verbatim above. (c) This adoption PR and its merge: the owner's explicit instruction above. (d) **Deletions, secrets, tags, releases and schedules are not asserted as new restrictions by this file.** The session operating-mode direction that mentioned them is not on `main`, and no verbatim owner text for that list was captured; this file therefore leaves them where the existing authority already puts them and asserts nothing new. A fresh agent must not read this item as a new reservation.
13. **Non-alteration (F11/A1) and the authority test.** This policy narrows, amends and replaces no register entry — including SDP-2 (AEGIS-APR-162) and AEGIS-APR-175. A merger relying on D-52 **must satisfy AEGIS-APR-162's conditions and cite AEGIS-APR-162**; the owner's verbatim text above is additional context, not an alternative route, and this file is not a register entry. MG1–MG5 do not replace APR-162's conditions.
14. **Adoption-merge rule (F9/R2-3).** No agent merges this adoption PR under any standing authority. It merges only on the owner's explicit instruction; the owner gave it in the 2026-11-19 message quoted above. After a fresh head-bound review and green required checks, the merge uses admin bypass only for the approving-review count under AEGIS-APR-175; the PR body quotes the instruction with this source.
15. **Limitations recorded honestly.** (a) The decision-log text of D-52 is not on the default branch; the only `D52` there is an unrelated reconciliation note. D-52 is cited as the owner's phrase in the verbatim reply, and a merger must cite AEGIS-APR-162 or the owner's text (item 13). (b) T14-D7 is not entered in the owner approval register; whether to record it there is the owner's decision and is left as a PR follow-up, not settled here. (c) The 2026-11-18 reply's exact time was not captured; the text is verbatim and its file hash is above.

## Traceability

| Policy item | Owner source |
| --- | --- |
| 1 authority floor | T14-D6 |
| 2 mode | T14-D1 |
| 3 merging / no deploy-release-auto-merge | T14-D2; AEGIS-APR-175 |
| 4 MG1–MG5 + D-64 | T14-C3; `docs/delivery-workflow.md` |
| 5 caps, definitions, P1 rule | T14-D3 (resolves C2) |
| 6 candidates | T14-D4 |
| 7 fallback reviewer | T14-D5 |
| 8 standing approval / review date / suspend-resume | T14-D7 |
| 9 evidence | T14-D8 |
| 10 start and scope | T14-D9, T14-D10 |
| 11 blocked work | T14-D11 |
| 12 owner-reserved items | AEGIS-APR-175; T14-D2; owner instruction 2026-11-19; (d) explicitly non-operative here (no durable owner text) |
| 13 non-alteration | owner answers; AEGIS-APR-162/175 |
| 14 adoption-merge rule | owner instruction 2026-11-19 (verbatim above) |
| 15 limitations | capture record above; decision-log adoption gap (D-52 text not on main) |

## Relationship to existing authority

- This file does not replace the [owner approval register](APPROVAL_REGISTER.md), the [merge policy](../../docs/reconciliation/auto-merge-policy.md), or the `AGENTS.md` authority rules; they remain in force.
- It adds no exception, no new delegation, no workflow/required-check/gate-guard change, and no consumer-repository authority.
- The owner's direct instructions still take precedence over this file.
