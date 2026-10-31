"""BER live-adapter enablement package (BUILD-ONLY; live is GATED).

This subpackage is the *enablement* surface for pilot A: subject adapters for the
two pinned subject vendors, a cross-vendor judge adapter, a spend ceiling with a
hard halt, an owner gate for real-host facts, and the preflight/dry-run/run verbs
that sit behind it. It is NOT enabled by default and ships with zero dispatches:

- every live verb requires a committed/gated owner record (dataset revision,
  pinned model identifiers, model-terms acknowledgment, spend ceiling);
- credentials are read only from the environment variables named by the pinned
  vendor records, and a missing key fails closed;
- a served-model string that differs from the pinned identifier HALTS the run
  with a structured MODEL_PIN_MISMATCH error (no silent substitution);
- the cross-vendor judge is only reachable through the owner allowlist, and a
  judge must never share the subject vendor;
- every call is preceded by a reservation against the configured ceiling, and a
  denied reservation halts dispatch: remaining cases are UNRUN/BUDGET_CAP and
  are never recorded as PASS.

Nothing here performs a provider request at import time. The single module that
names a vendor SDK (live/providers.py) imports it lazily inside the dispatch
function, so importing this package loads no network machinery. Tests inject a
mock transport and use fake environment values; the build used no keys and made
no provider call.
"""

LIVE_PACKAGE_VERSION = "0.2.0-ber-live"
LIVE_SCHEMA_VERSION = "1.0.0-ber-live"
LIVE_CAPABILITY_STATE = "GATED"
LIVE_ENABLED_BY_DEFAULT = False
LIVE_GATE_REQUIRED = True
LIVE_BUILD_DISPATCHES = 0
LIVE_BUILD_SPEND_USD = "$0"

__all__ = [
    "LIVE_PACKAGE_VERSION",
    "LIVE_SCHEMA_VERSION",
    "LIVE_CAPABILITY_STATE",
    "LIVE_ENABLED_BY_DEFAULT",
    "LIVE_GATE_REQUIRED",
    "LIVE_BUILD_DISPATCHES",
    "LIVE_BUILD_SPEND_USD",
]
