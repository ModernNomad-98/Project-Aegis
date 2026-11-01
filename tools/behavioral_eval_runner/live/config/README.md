# Gated live configuration templates

This directory holds the JSON runtime configuration templates for the gated
Behavioral Eval Runner (BER) live package. A template is a *setting record*, not
a bill: the package validates it, the committed owner gate bounds it, and the
cost meter enforces the smallest of the config ceiling, the gate ceiling and the
provider cap in integer cents before every call.

## Smoke completion under the 200c cap - NOT PROVEN

A refusing cost meter proves the $2 spend **stop**, not that the two-call smoke
can **complete**. At the current max-of-old/documented reservation rates and the
enforced judge-request limit, the minimum worst-case-safe smoke reservation is
**204c** (subject 32c + judge 172c) and the fallback safe bound is **314c**
(200,000-byte request limit); both exceed the 200c ceiling. For a safe bound to
fit 200c, the judge input cap would need to be at most 86,080 bytes, below the
enforced 90,000-byte cap; that is an owner decision and is not changed here.
An actual short request path (~118c) can finish, but it is not a worst-case-safe
completion proof. Paid-smoke readiness is therefore **NOT PROVEN**; this is a
reservation/planning incompatibility for a later owner checkpoint, not a paid
claim and not a silent cap change. The cap, the 16,384 output target and the
reservation semantics remain unchanged.

## The templates

| File | Used by | Spend class | `max_output_tokens` | Ceiling | Shape |
| --- | --- | --- | --- | --- | --- |
| `dry-run-config.json` | `live-dry-run` (synthetic gate, mock transport) | build-only / no-spend | 512 | 15000 cents | 20 cases x 2 arms x 3 runs x 2 vendors |
| `pilot-a-live-config.json` | historical/full-pilot template - **NOT dispatchable** (exceeds the 12,000c aggregate; kept for reference only) | live | 16384 | 12000 cents | 20 cases x 2 arms x 3 runs x 2 vendors |
| `pilot-a-smoke-config.json` | `eval-smoke` single-case gate | live | 16384 | 200 cents ($2.00 hard cap) | one case, one arm, one run, one vendor |
| `pilot-a-trial-config.json` | **`eval-run` bounded trial dispatch** (owner-approved; the only accepted eval-run template) | live | 16384 | 12000 cents | 20 cases x 2 arms x 1 run x 2 vendors (workflow narrows) |

## Build-only and live settings are different classes

A template authored for a build-only or dry-run package has **never** had its
spend-affecting values reviewed as live settings. The 2026-10-30 Pilot A
failure is the proof: the first live dispatch reused the build-only
`dry-run-config.json` with `max_output_tokens` 512, the subject response was
truncated at the provider stop reason, and the run halted fail-closed after one
call ($0.08). Preflight made no call by design, so it could not catch this.

Two independent guards now fail closed before any credential is resolved or any
call is reserved (`live/pipeline.py`):

1. a live verb refuses the build-only dry-run template **by resolved path and by
   the `dry-run-config.json` filename** (`DRY_RUN_CONFIG_REFUSED`);
2. a live verb refuses any config whose `max_output_tokens` is below
   `MIN_LIVE_MAX_OUTPUT_TOKENS` = 4096 (`LIVE_OUTPUT_TOKENS_TOO_LOW`). The floor
   also catches a renamed or staged copy of a build-only template.

## Required live-setting review before the first live dispatch

Any file merged under a build-only/no-spend label and later referenced by a live
dispatch must receive a fresh **live-setting review** before that first dispatch.
Preflight does not satisfy this review, because preflight makes no call.

A review record must contain:

- the named reviewer (a fresh independent reviewer, not the author);
- the review date and the exact 40-character candidate head SHA;
- every reviewed config path with its sha256 and its source class;
- an explicit **PASS or REVISE on each spend-affecting value**, never a single
  overall PASS;
- the reasoning that binds the values to the unchanged owner caps;
- the reviewer signature/disposition.

The spend-affecting values are:

`spend_ceiling_cents`, `max_output_tokens`, `runs_per_case`, `subject_vendors`
(the number of billed subject routes), `max_input_bytes`,
`request_timeout_seconds`, the `judge_allowlist` entries (which vendor/model is
allowed to be billed as a judge), and the pinned model/price table the config
round-trips against (`price_table`, `owner_limits`) — the owner-approved 2026-10-31
pricing repair uses the maximum of the pre-repair conservative values and the
documented standard rates (anthropic 300/1500, openai 1000/5000 cents per MTok)
as the conservative reservation basis. Over-reservation is intentional and safe;
under-reservation is not.

## Required gate before a full Pilot A dispatch

`eval-smoke` (`.github/workflows/eval-smoke.yml`, `workflow_dispatch` only) runs
exactly one subject call and one judge call on one committed case, hard-capped
at 200 integer cents ($2.00) inside the unchanged 12,000-cent aggregate, and
publishes a proof artifact only when the judge finishes
(judge terminal finish reason recorded in the run evidence). A full Pilot A
`eval-run` dispatch is required to run only after `eval-smoke` passed on the
same exact head; the full dispatch refuses when no passing proof at that head
exists.

