"""WP-2B-2 NON-LIVE semantic judge scaffold (BER-DEC-007).

This package contains NO provider implementation. The only concrete judge
clients are ``DisabledJudgeProvider`` (denies every dispatch with
LIVE_DISPATCH_DISABLED) and the recorded-fixture ``MockJudgeClient``. Zero
actual judge/provider calls are possible from this package; no measured
calibration exists or is claimed; OD-1 remains OPEN; R2 remains BLOCKED.
"""
