"""Aegis distributed-payload manifest and read-only verifier (stdlib only).

Schema: aegis.distributed-payload-manifest/1.
CLI verbs: build, verify, check-manifest. There is no install, repair, upgrade,
uninstall, prune or cleanup verb, and verification never mutates a target.
"""
from .manifest import (  # noqa: F401
    SCHEMA,
    HASH_CONTRACT,
    TOOL_NAME,
    TOOL_VERSION,
    ManifestError,
    build_manifest,
    create_binding,
    manifest_identity,
    serialize_manifest,
    validate_manifest,
    write_manifest_atomic,
)
from .verify import (  # noqa: F401
    REPORT_SCHEMA,
    check_manifest,
    verify_target,
)

__all__ = [
    "SCHEMA",
    "HASH_CONTRACT",
    "TOOL_NAME",
    "TOOL_VERSION",
    "ManifestError",
    "build_manifest",
    "create_binding",
    "manifest_identity",
    "serialize_manifest",
    "validate_manifest",
    "write_manifest_atomic",
    "REPORT_SCHEMA",
    "check_manifest",
    "verify_target",
]
