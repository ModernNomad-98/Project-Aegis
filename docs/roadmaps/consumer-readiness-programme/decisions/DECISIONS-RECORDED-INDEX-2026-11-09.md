# OWNER-DECISIONS — DECISIONS RECORDED INDEX (2026-11-09)

Status of the 15 ROD requests after the owner's 2026-11-08/09 decisions. The request files themselves remain byte-unchanged (REQUESTS still marked UNDECIDED as issued); the decision records below are authoritative.

| Item | Status | Decision record (path / bytes / SHA-256) |
|---|---|---|
| ROD-01 remote delivery / merge authority | **AUTHORIZED** (delivery executed; PR #1001 merged as `3a420ed7`) | `OWNER-ROD01-DELIVERY-AUTHORIZATION-2026-11-08.md` · 2,596 B · `5cb3c5e6…` |
| PR #1001 administrator bypass of the approving-review requirement | **AUTHORIZED** (used once at the merged head; recorded as bypass only) | `OWNER-PR1001-MERGE-BYPASS-AUTHORIZATION-2026-11-08.md` · 3,062 B · `ecad749e…` |
| ROD-11 A3 artifact-expiry handling | **KEEP FAIL-CLOSED DEFAULT** (no change; deadline 2026-11-13 23:15:44 PST) | `OWNER-A3-EXPIRY-HANDLING.md` · 1,380 B · `813b34e2…` |
| ROD-02/03/04/05/06/07/08/09/10/12/13/14/15 (all remaining) | **HOLD / DEFER** (blanket owner line) | `OWNER-REMAINING-DECISIONS-HOLD-2026-11-08.md` · 2,297 B · `a412178b…` |
| Delivery execution rules (parallel local work; no push until ready; one PR at a time) | Recorded operating rule | `DELIVERY-EXECUTION-RULES-2026-11-08.md` · 1,600 B · `308bf944…` |

**Closure effect:** only the plan closures keyed to the recorded decisions can pass from these records (CL-11 merge authorization+receipt, CL-40 A3 handling); the held items green nothing — their plan closures remain FAIL/UNRUN by design. Request files are unchanged; no decision is inferred from silence.

**Prepared by:** Lead (DeepSeek Harness; route deepseek-flash; serving model not observable). **Local record only.** **Timestamp label:** 2026-11-09T02:20:00Z.