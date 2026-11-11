"""Read-only C3/C4 operational-overhead and qualification tooling.

`tools/aegis_ops/` is an auditable, non-enforcing package:

* standard library only; no network, provider SDK or subprocess at runtime;
* it validates supplied facts and prints deterministic JSON; it never writes
  a file, mutates repository state, polls or approves anything;
* it consumes the merged C1.1a checker and the accepted C2/C1.2-C1.4
  interfaces by reference, and does not restate their schemas;
* assurance is AUDITABLE with mounted coverage UNKNOWN.  T6 is
  UNVERIFIED+BLOCKED, T24 is UNVERIFIED, T7 is OPEN, T5 is not assumed and T4
  is declined.  A green/readiness/enforcement claim is not available here.
"""

from .schema import PACKAGE_VERSION, RECORD_FAMILY

__all__ = ["PACKAGE_VERSION", "RECORD_FAMILY"]
__version__ = PACKAGE_VERSION
