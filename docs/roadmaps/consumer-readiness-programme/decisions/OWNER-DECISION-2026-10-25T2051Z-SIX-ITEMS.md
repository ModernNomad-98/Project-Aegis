# OWNER DECISION - six items (direct session message, received 2026-10-25T20:51:26-07:00 America/Los_Angeles)

Source: direct owner message in the DSH session, 2026-10-25T20:51:26-07:00 (occurrence context: scheduled reminder batch turn 91 step 4). Verbatim text as typed by Peter Nguyen:

> OWNER DECISION — six items.
>
> 1. #913: C, narrowly. Merge only (i) glued hyphen fragment after "shipped as" fails closed as an unknown token, (ii) every token after "shipped as" is checked independently (closes Codex R2-CX-1), and (iii) the differential base-vs-head test asserting zero base-detected claims lost. Revert every other predicate change in the branch to base 4cdc86a8/ed753df7 content. No class carrying an open fail-open P1 merges. If the branch cannot be cut to that cleanly, close #913 without merge and open a fresh minimal PR for exactly (i)-(iii), planned with plan-of-record-author once it ships. No sixteenth round on the current content.
>
> 2. #915: yes, covered. The standing green-checks grants are not head-specific; a fresh SD-F at the exact head is what they require. It has zero protected paths. D10 is right to block on the TTL fail-open and the offline-auth contradiction; run REV-12. Apply the same ladder: if REV-12 does not clear D, narrow to the validated contract items and merge those.
>
> 3. D7 = YES — ratify the plan-stage skills wave (plan-of-record-author + plan-audit-reviewer), supersede the 2026-10-21 decision for stages A and B only (C and E stay procedural), and confirm defaults D1, D2, D3, D4, D6 with D5 deferred. The recurring need is demonstrated and the plan should cite it: batch-25 r1-r5, batch-26 r1-r4, pilot block B r1-r4, R4 fourteen rounds, R5 seven, R6 six, the UX extension plan r1-r4, and #913 at fifteen. PR-1's two protected scripts paths are routine count/registration edits under APR-140. Unblock Stage C now.
>
> 4. AD-10: RATIFIED as written. Must-fix before merge is anything that lets invalid data through, any security hole, any false claim about what was tested or merged, or a required check that could not run; everything else is a carry with provider, comment id and reason recorded in the stage record. A bot severity label alone never forces a change; a real fail-open always does.
>
> 5. AD-11 and AD-12: RATIFIED, with one amendment. When the bounded final round still fails, do not present me A/B/C — apply the disposition ladder: revert the oscillating constructs, keep the validated subset, disclose, merge. Asking is for a genuine trade between two safety properties only.
>
> 6. #912 one-time authority: RATIFIED. The 10:17 PDT decision (OD-1) was mine, issued in the chat and quoted verbatim in STATUS 6405202059. Transcribe it with the tools/behavioral_eval_runner extension as APR-142 and the R1 clarification as APR-143. Do NOT queue that docs-only register PR behind #913 — it shares no files with anything open; open it now.

## Immediate application
- (1) #913 is reset by disposition ladder: keep only (i) glued-hyphen unknown, (ii) every-token-independent check, (iii) base-vs-head zero-claim-loss differential; revert all other predicate changes to base content; no open fail-open P1 class merges; if not cleanly cuttable -> close #913 and do a fresh minimal PR (planned with plan-of-record-author after it ships). No sixteenth round.
- (2) #915 R1 coverage confirmed; REV-12 runs; same ladder if REV-12 does not clear D -> narrow to validated contract items and merge those; zero protected paths; fresh SD-F at exact head required.
- (3) D7 = YES recorded; Stage C of the plan-stage skills wave unblocked now; PR-1 scripts count/registration edits covered by APR-140; plan to cite the demonstrated recurring-need list verbatim.
- (4) AD-10 RATIFIED as written.
- (5) AD-11/AD-12 RATIFIED with the amendment: bounded-final-round failure -> disposition ladder (revert oscillating constructs, keep validated subset, disclose, merge); ask owner only for genuine trade between two safety properties.
- (6) #912 OD-1 RATIFIED; register transcription as APR-142 (tools/behavioral_eval_runner extension) + APR-143 (R1 clarification) to be opened NOW as a docs-only PR, not queued behind #913.