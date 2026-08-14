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
- No Scenario A execution, no generic eval execution.

WP-2B-2 addition (BER-DEC-007, authorization PR #84, squash merge
1145cb75d79bc6ab13876438527235c93320278b): the NON-LIVE Scenario A grading
stack — deterministic graders over recorded synthetic evidence, the semantic
judge scaffold (no provider implementation; every dispatch path absent or
denied), and the deterministic/mock calibration harness. The Outcome B
boundaries above remain binding: zero runner-generated, grading-stack-
generated, or test-harness-generated model/provider dispatches, zero actual
judge/provider calls, no measured calibration, OD-1 OPEN, and R1/R2/R4/R5
still NOT technically solved.
"""

RUNNER_VERSION = "0.1.0-wp2b1"
SCHEMA_VERSION = "1.0.0-wp2b1"
SCHEDULING_POLICY_VERSION = "1.0.0-wp2b1"

AUTHORIZATION_ID = "BER-DEC-006"
WORK_PACKAGE = "WP-2B-1"
AUTHORIZATION_MERGE_SHA = "fc98ee6bf59bb516064be62ed8c5dc8861c92697"

# WP-2B-2 Scenario A grading stack (additive; WP-2B-1 identifiers unchanged).
GRADING_STACK_VERSION = "0.1.0-wp2b2"
GRADING_SCHEMA_VERSION = "1.0.0-wp2b2"
WP2B2_AUTHORIZATION_ID = "BER-DEC-007"
WP2B2_WORK_PACKAGE = "WP-2B-2"
WP2B2_AUTHORIZATION_MERGE_SHA = "1145cb75d79bc6ab13876438527235c93320278b"

# WP-2B-3 measured-judge-calibration controls (additive; BER-DEC-008 Stage
# A1: offline implementation only — zero provider/model/metadata calls, zero
# credential access; owner label approval PENDING; OD-1 OPEN).
CALIBRATION_STACK_VERSION = "0.1.0-wp2b3"
CALIBRATION_SCHEMA_VERSION = "1.0.0-wp2b3"
WP2B3_AUTHORIZATION_ID = "BER-DEC-008"
WP2B3_WORK_PACKAGE = "WP-2B-3"
WP2B3_AUTHORIZATION_MERGE_SHA = "1c3e4931329179d9a3f9cc9ec1bb93020378c043"
WP2B3_AUTHORIZATION_TREE_SHA = "feb7cf261d8efa624c18363c9928e7f0cbdfed4c"

__all__ = [
    "RUNNER_VERSION",
    "SCHEMA_VERSION",
    "SCHEDULING_POLICY_VERSION",
    "AUTHORIZATION_ID",
    "WORK_PACKAGE",
    "AUTHORIZATION_MERGE_SHA",
    "GRADING_STACK_VERSION",
    "GRADING_SCHEMA_VERSION",
    "WP2B2_AUTHORIZATION_ID",
    "WP2B2_WORK_PACKAGE",
    "WP2B2_AUTHORIZATION_MERGE_SHA",
    "CALIBRATION_STACK_VERSION",
    "CALIBRATION_SCHEMA_VERSION",
    "WP2B3_AUTHORIZATION_ID",
    "WP2B3_WORK_PACKAGE",
    "WP2B3_AUTHORIZATION_MERGE_SHA",
    "WP2B3_AUTHORIZATION_TREE_SHA",
]
