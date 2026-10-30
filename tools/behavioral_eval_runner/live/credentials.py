"""Environment-only credentials with fail-closed, non-logging behavior.

A credential value is read from exactly one environment variable and is never
serialized: repr/str mask it, structured records carry only the variable name
and presence, and no exception message includes the value. Missing values fail
closed before any transport object is constructed.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Iterable, Mapping

from .errors import MissingCredentialError
#: The only accepted credential environment variables, by vendor (the identity
#: lives in the single provider-naming module).
from .providers import CREDENTIAL_ENV_VARS



@dataclass(frozen=True, slots=True)
class Credential:
    """One resolved credential. The value is hidden from repr and records."""

    vendor: str
    env_var: str
    _value: str

    def __repr__(self) -> str:
        return f"Credential(vendor={self.vendor!r}, env_var={self.env_var!r}, value=***)"

    __str__ = __repr__

    def reveal(self) -> str:
        """Return the secret for the transport call only (never logged)."""
        return self._value

    def presence_record(self) -> dict[str, object]:
        return {"vendor": self.vendor, "env_var": self.env_var, "present": True}


@dataclass(frozen=True, slots=True)
class CredentialSet:
    credentials: Mapping[str, Credential]

    def __repr__(self) -> str:
        return f"CredentialSet(vendors={sorted(self.credentials)}, values=***)"

    __str__ = __repr__

    def for_vendor(self, vendor: str) -> Credential:
        try:
            return self.credentials[vendor]
        except KeyError:
            raise MissingCredentialError(
                f"no credential resolved for vendor {vendor!r}",
                context={"vendor": vendor, "env_var": CREDENTIAL_ENV_VARS.get(vendor)},
            ) from None

    def presence_records(self) -> list[dict[str, object]]:
        return [self.credentials[v].presence_record() for v in sorted(self.credentials)]


def missing_credential_env_vars(
    vendors: Iterable[str], environ: Mapping[str, str] | None = None
) -> list[str]:
    """Names (never values) of absent credential variables, sorted."""
    environ = os.environ if environ is None else environ
    missing: list[str] = []
    for vendor in vendors:
        env_var = CREDENTIAL_ENV_VARS.get(vendor)
        if env_var is None:
            missing.append(f"<no-pinned-env-for:{vendor}>")
            continue
        if not environ.get(env_var):
            missing.append(env_var)
    return sorted(set(missing))


def resolve_credentials(
    vendors: Iterable[str], environ: Mapping[str, str] | None = None
) -> CredentialSet:
    """Resolve credentials from the environment only; fail closed when absent."""
    environ = os.environ if environ is None else environ
    wanted = sorted(set(vendors))
    missing = missing_credential_env_vars(wanted, environ)
    if missing:
        raise MissingCredentialError(
            "missing credential environment variable(s): " + ", ".join(missing),
            context={"missing_env_vars": missing, "vendors": wanted},
        )
    resolved: dict[str, Credential] = {}
    for vendor in wanted:
        env_var = CREDENTIAL_ENV_VARS[vendor]
        resolved[vendor] = Credential(vendor, env_var, environ[env_var])
    return CredentialSet(resolved)
