"""Project Aegis Behavioral Eval Runner — WP-2B-1 offline core.

Authorized by BER-DEC-006 (authorization PR #82, squash merge
fc98ee6bf59bb516064be62ed8c5dc8861c92697). This package is the NON-LIVE
control plane and minimum guardrails phase of the Behavioral Eval Runner
described by docs/design/behavioral-eval-runner-v1.md.

Hard boundaries of this phase (Outcome B constraints):

- ZERO model/provider dispatches; ZERO live Claude Code sessions.
- Every live-dispatch path is disabled and denies with LIVE_DISPATCH_DISABLED.
- Real-host capabilities (activation observation, containment, execution-profile
  isolation, reservation units) are reported UNAVAILABLE/UNKNOWN, never assumed.
- R1, R2, R3, R4, R5 are NOT technically solved by this package; R2 remains
  BLOCKED and OD-1 remains OPEN.
- No Scenario A execution, no generic eval execution, no graders, no judge.
"""

RUNNER_VERSION = "0.1.0-wp2b1"
SCHEMA_VERSION = "1.0.0-wp2b1"
SCHEDULING_POLICY_VERSION = "1.0.0-wp2b1"

AUTHORIZATION_ID = "BER-DEC-006"
WORK_PACKAGE = "WP-2B-1"
AUTHORIZATION_MERGE_SHA = "fc98ee6bf59bb516064be62ed8c5dc8861c92697"

__all__ = [
    "RUNNER_VERSION",
    "SCHEMA_VERSION",
    "SCHEDULING_POLICY_VERSION",
    "AUTHORIZATION_ID",
    "WORK_PACKAGE",
    "AUTHORIZATION_MERGE_SHA",
]
