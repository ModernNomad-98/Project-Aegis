# Control-plane design entry point — 2026-09-23

## Purpose and scope

This note records a bounded readability change to the
[control-plane design contract](../../design/resumable-control-plane-v1.md).
Its 2026-09-12 opening described the documentation-only first package as if
no controller kernel existed. The current first screen now distinguishes the
delivered offline synthetic kernel and negative proofs from blocked real work.
It routes readers to current status, supported offline commands, owner grants
and the original design review.

The previously stated estimate for this page was **none recorded**. This
bounded batch was estimated at **2–4 active hours**. The selected backlog
forecast at start was **175–394 active hours**, including **80–200** for the
full documentation sweep. Work began about **19:18 UTC**. Actual merge wall
time belongs in the pull request closeout; active-only time was not measured.

## Line-position and authority boundary

Only physical lines 3–13 were replaced, with exactly 11 new physical lines.
The design retains 966 physical lines, and the text from line 14 onward is
byte-equal to the merged main base after newline normalization. This matters
because an existing
control-plane evidence report links to exact `#L` line positions in the
design, including transitions and crash/failure requirements hundreds of
lines below the opening. The new entry point changes neither those targets
nor the normative contract.

The current state was checked against the [package guide](../../../tools/aegis_delivery_control/README.md),
[work-package register](../../roadmaps/resumable-control-plane-backlog.md),
[CP-WP-003A evidence](../control-plane/cp-wp-003a-review.md), and
[approval register](../../approvals/APPROVAL_REGISTER.md). This edit grants no
real authority, provider call, deployment, or later work package. The root
worktree's unrelated local modification to the design was not changed.

## Verification

The design still has **966 physical lines**. After newline normalization,
every line from 14 onward matches the merged base, including lines 420, 447,
455, 599, 607, 939 and 960 targeted or near-targeted by existing evidence
links. All **29 local links** in the two scoped pages resolved. `python -B
scripts/validate-skills.py` passed with **185 valid skills and zero warnings**;
`git diff --check` passed. Independent review and exact-head GitHub Actions
remain delivery gates; their final results belong in the pull request. The
wider documentation sweep remains open.
