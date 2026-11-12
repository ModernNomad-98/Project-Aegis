# Consumer-proof row readability acceptance (fourth set) — 2026-11-13

Acceptance revision: `9011761e389f3f8d15309a2d20a97b1c36fc3cd2`. Three CP rows accepted for **readability only**: CP-01 PASS; CP-03 FAIL; CP-09 FAIL. The FAIL verdicts remain FAIL and are not converted.

### 1. CP-01 — fresh owner-authorized Codex session (PASS)
- Page blob `9178f5595161ad4f5fd935f88df85cbaaf5035a7`; 1,240 B / 16 lines.
- Review PASS (`READABILITY-CP01-REVIEW-2026-11-13.md`, 360b8bdd).
- Quote: "the owner defined the run as the closing observation."
- Reviewer: c03-contract-owner.

### 2. CP-03 — installer control (FAIL; preserved)
- Page blob `1b93f660aff220eab988eebfad6a61315da9936d`; 1,277 B / 16 lines.
- Readability PASS (`READABILITY-CP03-REVIEW-2026-11-13.md`, c53b5350); **row verdict remains FAIL**.
- Quote: "The pre-registered N1 installer control (one packaged file removed from the installed set) **exited 0 and healed 40 → 41 installed files** where a stop was required."
- Reviewer: evidence-lineage-steward.

### 3. CP-09 — public consumer metadata (FAIL; preserved)
- Page blob `4c089b1cb97db08aa14cee8a1a2cdb3e25ff7b62`; 1,304 B / 16 lines.
- Readability PASS (`READABILITY-CP09-REVIEW-2026-11-13.md`, bf550e76); **row verdict remains FAIL**.
- Quote: "**Basis observed.** Public consumer commit metadata contains plan-forbidden product names and PR numbers, and a personal full name. Owner CP-09=A: **FAIL stands**; the final ledger records it; a prevention item is added; no retroactive exception and no history rewrite. This bundle does **not** republish the identifier scan, because that scan enumerates the very strings the row prohibits."
- Reviewer: records-steward.

## Limits
Readability acceptance only. CP-03 and CP-09 remain FAIL; no FAIL-to-PASS conversion, no retry, no exception, no history rewrite. CP-01 remains PASS.

Recorded by: Lead. Local record only.