# Behavioral Eval Runner backlog readability batch — 2026-09-23

## Scope and forecast

This batch adds a current entry point to the [Behavioral Eval Runner (BER)
backlog](../../roadmaps/behavioral-eval-runner-backlog.md) while retaining its
original normative and historical body. It began in an isolated worktree at
`cf63696`, the merged pull request (PR) #145 head. The only other edit is
this dated evidence note. The shared documentation readability ledger is
reserved for the coordinator's later integration.

The previous BER backlog page estimate was **2–4 active hours**. This bounded
batch was also estimated at **2–4 active hours**. The selected remaining
backlog total was **175–394 active hours** at start. Those are scope forecasts;
observed wall time below is separate from active-only labor.

## Current-source reconciliation

- The original first screen begins with 2026-09-12 and earlier delivery
  checkpoints. Those are historical records, so the new top section names
  its maintainer/agent audience and routes readers to the binding
  authorization protocol, status vocabulary, phase records, evidence gates,
  governance log, approval register and current forecast.
- The new current map distinguishes delivered offline/limited work packages
  2B-0, 2B-1, 2B-1A and 2B-2; authorized but unfinished measured calibration
  in 2B-3; blocked live work in 2B-4; and later backlog packages 2B-5–7.
  Accepted Outcome B evidence dispositions do not prove a live host.
- Approval APR-009 selected the 30-day complete-bundle evidence policy.
  APR-012 and BER-DEC-011 authorize only a synthetic offline first proof under
  WP-2B-1B. PR #139 was open at the review checkpoint. Child backlog item
  BER-BKL-009 remains partial and real-host controls remain separate.
- The glossary explains work-package, backlog and decision identifiers,
  status codes and the distinction between generic CI and selected-host
  evidence. It does not alter any approval, provider or holdout gate.

No original register paragraph, work-package record, backlog entry or
decision-log event was rewritten. No private input, provider, credential or
real host was accessed.

## Verification and timing

- Checked the current approval register through APR-012, the owning BER
  register records, latest forecast, and live PR #139 state.
- The original register body was byte-equal to its starting revision after
  newline normalization (225,123 bytes). All 83 local links and 12 anchors
  across the two scoped pages resolved. `python -B scripts/validate-skills.py`
  passed with 185 valid skills and zero warnings; `git diff --check` passed.
  Git status showed only the two authorized paths.
- Independent read-only review and exact-head checks remain delivery gates.
  This batch does not complete the full documentation sweep.

Work started at **2026-09-23 19:05:27 UTC**. The local verification checkpoint
was **2026-09-23 19:09:35 UTC**, an observed wall interval of **4 minutes 8
seconds**. Active-only implementation time was not instrumented.
