"""Regression tests for the exact-head PR #83 independent-review blockers.

The three clusters pin:

- explicit isolated execution-profile states for baseline eligibility;
- cryptographically bound, complete, reparse-safe materialization verification;
- Windows emergency-kill resolution from an OS trust source, never environment.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import types
import unittest
from dataclasses import replace
from unittest import mock

from tools.behavioral_eval_runner.canonical import canonical_bytes, sha256_hex
from tools.behavioral_eval_runner.enums import (
    ClaimScope,
    MaterializationProfile,
    WorkspaceRole,
)
from tools.behavioral_eval_runner.errors import (
    MaterializationError,
    ProcessControlError,
    ProfileError,
    ReparsePointError,
)
from tools.behavioral_eval_runner.execution_profile import (
    REQUIRED_FOR_BASELINE,
    ExecutionProfile,
    synthetic_isolated_profile,
)
from tools.behavioral_eval_runner.materialize import (
    _POSIX_NOFOLLOW_WRITE,
    MaterializationRecord,
    reparse_write_capability,
    verify_materialization_manifests,
)
from tools.behavioral_eval_runner.process_control import (
    _trusted_taskkill_path,
    _windows_system_directory,
)


class TestExecutionProfileIsolation(unittest.TestCase):
    def test_approved_isolated_profile_remains_eligible(self) -> None:
        self.assertTrue(synthetic_isolated_profile().baseline_eligible)

    def test_every_baseline_field_rejects_unapproved_observed_state(self) -> None:
        base = synthetic_isolated_profile().to_dict(include_derived=False)
        unsafe = {
            "runtime_version": "2.1.0",
            "managed_settings_status": "loaded",
            "user_settings_status": "loaded",
            "project_settings_status": "unverified",
            "local_settings_status": "loaded",
            "claude_md_scopes": "global",
            "auto_memory_state": "active",
            "user_skill_scope": "global",
            "project_skill_scope": "unverified",
            "subagent_scope": "global",
            "plugin_scope": "global",
            "hook_scope": "unrestricted",
            "mcp_scope": "global",
            "permission_policy": "allow-all",
            "sandbox_tool_policy": "unrestricted",
            "auto_update_state": "auto",
        }
        for field_name, value in unsafe.items():
            with self.subTest(field=field_name):
                profile = ExecutionProfile.from_dict(
                    dict(base, **{field_name: value})
                )
                self.assertFalse(profile.baseline_eligible)
                self.assertTrue(
                    any(
                        field_name in reason
                        for reason in profile.baseline_ineligibility_reasons()
                    )
                )

    def test_schema_baseline_true_is_limited_to_the_same_safe_states(self) -> None:
        schema_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "schemas",
            "execution-profile.schema.json",
        )
        with open(schema_path, encoding="utf-8") as handle:
            schema = json.load(handle)
        safe_properties = schema["allOf"][0]["then"]["properties"]
        self.assertEqual(set(safe_properties), set(REQUIRED_FOR_BASELINE))
        self.assertEqual(
            safe_properties["permission_policy"]["enum"],
            ["deny-by-default"],
        )
        self.assertEqual(
            safe_properties["sandbox_tool_policy"]["enum"],
            ["isolated", "synthetic-mock"],
        )


class TestMaterializationManifestIntegrity(unittest.TestCase):
    def setUp(self) -> None:
        self._temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self._temporary.cleanup)
        self.root = self._temporary.name
        manifest_dir = os.path.join(self.root, "materialization_manifests")
        os.makedirs(manifest_dir)

        definitions = (
            (
                "control_plane_manifest.json",
                "authored_eval_corpus",
                "control_plane",
                "evals/case.json",
                b"{}",
            ),
            (
                "runtime_surface_manifest.json",
                "sanitized_runtime_surface",
                "runtime_surface",
                ".claude/skills/x/SKILL.md",
                b"# x",
            ),
            (
                "product_fixture_manifest.json",
                "product_fixture",
                "product_fixture",
                "app/readme.txt",
                b"fixture",
            ),
        )
        manifests: dict[str, dict] = {}
        paths: dict[str, str] = {}
        hashes: dict[str, str] = {}
        for name, kind, area, relative, content in definitions:
            target = os.path.join(self.root, area, *relative.split("/"))
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, "wb") as handle:
                handle.write(content)
            manifest = {
                "schema_version": "1.0.0-wp2b1",
                "manifest_kind": kind,
                "source_commit": "0" * 40,
                "source_tree": "1" * 40,
                "materialization_profile": "consumer_skills_only",
                "file_count": 1,
                "files": [
                    {
                        "path": relative,
                        "bytes": len(content),
                        "sha256": sha256_hex(content),
                    }
                ],
            }
            if kind == "product_fixture":
                manifest["fixture_id"] = "fixture"
                manifest["fixture_version"] = "1"
            body = canonical_bytes(manifest)
            manifest_path = os.path.join(manifest_dir, name)
            with open(manifest_path, "wb") as handle:
                handle.write(body)
            manifests[name] = manifest
            paths[name] = manifest_path
            hashes[name] = sha256_hex(body)

        self.record = MaterializationRecord(
            source_commit="0" * 40,
            source_tree="1" * 40,
            profile=MaterializationProfile.CONSUMER_SKILLS_ONLY,
            workspace_role=WorkspaceRole.CONSUMER,
            claim_scope=ClaimScope.FULL_LIBRARY,
            shipped_skill_count=1,
            materialized_skill_count=1,
            subagent_count=0,
            ambiguous_excluded=(),
            control_plane_manifest=manifests["control_plane_manifest.json"],
            runtime_surface_manifest=manifests["runtime_surface_manifest.json"],
            product_fixture_manifest=manifests["product_fixture_manifest.json"],
            control_plane_manifest_sha256=hashes["control_plane_manifest.json"],
            runtime_surface_manifest_sha256=hashes[
                "runtime_surface_manifest.json"
            ],
            product_fixture_manifest_sha256=hashes[
                "product_fixture_manifest.json"
            ],
            baseline_eligible=True,
            baseline_ineligibility_reasons=(),
            manifest_paths=paths,
        )

    def _rewrite_manifest(
        self,
        name: str,
        mutate,
        *,
        rebind_hash: bool = False,
        rebind_body: bool = False,
    ) -> MaterializationRecord:
        path = self.record.manifest_paths[name]
        with open(path, encoding="utf-8") as handle:
            manifest = json.load(handle)
        mutate(manifest)
        body = canonical_bytes(manifest)
        with open(path, "wb") as handle:
            handle.write(body)
        updates = {}
        if rebind_hash:
            hash_field = {
                "control_plane_manifest.json": "control_plane_manifest_sha256",
                "runtime_surface_manifest.json": "runtime_surface_manifest_sha256",
                "product_fixture_manifest.json": "product_fixture_manifest_sha256",
            }[name]
            updates[hash_field] = sha256_hex(body)
        if rebind_body:
            body_field = {
                "control_plane_manifest.json": "control_plane_manifest",
                "runtime_surface_manifest.json": "runtime_surface_manifest",
                "product_fixture_manifest.json": "product_fixture_manifest",
            }[name]
            updates[body_field] = manifest
        return replace(self.record, **updates)

    def test_valid_manifests_verify_against_expected_record(self) -> None:
        result = verify_materialization_manifests(self.root, self.record)
        self.assertTrue(result["verified"])
        self.assertEqual(len(result["manifests"]), 3)

    def test_expected_record_is_required(self) -> None:
        with self.assertRaises(MaterializationError):
            verify_materialization_manifests(self.root, None)  # type: ignore[arg-type]

    def test_manifest_omission_rejected_even_if_hash_and_body_are_rebound(self) -> None:
        def omit(manifest: dict) -> None:
            manifest["files"] = []
            manifest["file_count"] = 0

        rebound = self._rewrite_manifest(
            "runtime_surface_manifest.json",
            omit,
            rebind_hash=True,
            rebind_body=True,
        )
        with self.assertRaises(MaterializationError):
            verify_materialization_manifests(self.root, rebound)

    def test_manifest_substitution_rejected(self) -> None:
        source = self.record.manifest_paths["control_plane_manifest.json"]
        target = self.record.manifest_paths["runtime_surface_manifest.json"]
        with open(source, "rb") as source_handle:
            content = source_handle.read()
        with open(target, "wb") as target_handle:
            target_handle.write(content)
        with self.assertRaises(MaterializationError):
            verify_materialization_manifests(self.root, self.record)

    def test_extra_on_disk_file_rejected(self) -> None:
        extra = os.path.join(self.root, "runtime_surface", "extra.txt")
        with open(extra, "wb") as handle:
            handle.write(b"extra")
        with self.assertRaises(MaterializationError):
            verify_materialization_manifests(self.root, self.record)

    def test_duplicate_manifest_path_rejected_with_rebound_record(self) -> None:
        def duplicate(manifest: dict) -> None:
            manifest["files"].append(dict(manifest["files"][0]))
            manifest["file_count"] = 2

        rebound = self._rewrite_manifest(
            "runtime_surface_manifest.json",
            duplicate,
            rebind_hash=True,
            rebind_body=True,
        )
        with self.assertRaises(MaterializationError):
            verify_materialization_manifests(self.root, rebound)

    def test_source_identity_change_rejected_with_rebound_hash(self) -> None:
        def change_source(manifest: dict) -> None:
            manifest["source_commit"] = "f" * 40

        rebound = self._rewrite_manifest(
            "runtime_surface_manifest.json",
            change_source,
            rebind_hash=True,
        )
        with self.assertRaises(MaterializationError):
            verify_materialization_manifests(self.root, rebound)

    def test_symlink_replacement_rejected(self) -> None:
        target = os.path.join(
            self.root,
            "runtime_surface",
            ".claude",
            "skills",
            "x",
            "SKILL.md",
        )
        outside = os.path.join(self.root, "outside.txt")
        with open(outside, "wb") as handle:
            handle.write(b"# x")
        os.unlink(target)
        try:
            os.symlink(outside, target)
        except (OSError, NotImplementedError):
            self.skipTest("symlink creation unavailable")
        with self.assertRaises(MaterializationError):
            verify_materialization_manifests(self.root, self.record)


class _RegistryKey:
    def __init__(self, values: dict[str, tuple[str, int]]) -> None:
        self.values = values

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        return None


class TestTrustedTaskkill(unittest.TestCase):
    def test_windows_system_directory_uses_registry_not_environment(self) -> None:
        trusted_root = os.path.abspath(os.path.join(os.sep, "trusted-windows"))
        fake_winreg = types.SimpleNamespace(
            KEY_READ=1,
            KEY_WOW64_64KEY=2,
            HKEY_LOCAL_MACHINE=object(),
            REG_SZ=1,
            OpenKey=lambda *_args: _RegistryKey({}),
            QueryValueEx=lambda _key, _name: (trusted_root, 1),
        )
        with (
            mock.patch.object(sys, "platform", "win32"),
            mock.patch.dict(sys.modules, {"winreg": fake_winreg}),
            mock.patch.dict(
                os.environ,
                {
                    "SystemRoot": os.path.join(os.sep, "attacker"),
                    "windir": os.path.join(os.sep, "attacker"),
                },
                clear=False,
            ),
        ):
            self.assertEqual(
                _windows_system_directory(),
                os.path.normpath(os.path.join(trusted_root, "System32")),
            )

    def test_poisoned_environment_cannot_select_taskkill_binary(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            malicious = os.path.join(root, "malicious", "System32")
            trusted = os.path.join(root, "trusted-System32")
            os.makedirs(malicious)
            os.makedirs(trusted)
            fake = os.path.join(malicious, "taskkill.exe")
            real = os.path.join(trusted, "taskkill.exe")
            with open(fake, "wb") as handle:
                handle.write(b"fake")
            with open(real, "wb") as handle:
                handle.write(b"real")
            with (
                mock.patch.dict(
                    os.environ,
                    {
                        "SystemRoot": os.path.dirname(malicious),
                        "windir": os.path.dirname(malicious),
                    },
                    clear=False,
                ),
                mock.patch(
                    "tools.behavioral_eval_runner.process_control._windows_system_directory",
                    return_value=trusted,
                ),
            ):
                self.assertEqual(_trusted_taskkill_path(), real)
                self.assertNotEqual(_trusted_taskkill_path(), fake)

    def test_reparse_system_directory_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            real = os.path.join(root, "real-System32")
            link = os.path.join(root, "link-System32")
            os.makedirs(real)
            with open(os.path.join(real, "taskkill.exe"), "wb") as handle:
                handle.write(b"real")
            try:
                os.symlink(real, link, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("symlink creation unavailable")
            with mock.patch(
                "tools.behavioral_eval_runner.process_control._windows_system_directory",
                return_value=link,
            ):
                with self.assertRaises(ProcessControlError):
                    _trusted_taskkill_path()


# =============================================================== Fresh finding A
class TestExecutionProfileDerivedClaims(unittest.TestCase):
    """A: from_dict must reject supplied derived fields that disagree with the
    authoritative recomputation, not silently discard them."""

    def _unsafe_serialized(self) -> dict:
        base = synthetic_isolated_profile().to_dict(include_derived=False)
        base["permission_policy"] = "allow-all"  # not an approved isolated state
        prof = ExecutionProfile.from_dict(base)
        self.assertFalse(prof.baseline_eligible)  # authoritative truth = False
        payload = prof.to_dict(include_derived=True)
        return payload

    def test_fabricated_baseline_eligible_rejected(self) -> None:
        payload = self._unsafe_serialized()
        payload["baseline_eligible"] = True  # contradicts recomputed False
        payload["baseline_ineligibility_reasons"] = []
        with self.assertRaises(ProfileError):
            ExecutionProfile.from_dict(payload)

    def test_fabricated_hash_rejected(self) -> None:
        payload = synthetic_isolated_profile().to_dict(include_derived=True)
        payload["execution_profile_hash"] = "0" * 64
        with self.assertRaises(ProfileError):
            ExecutionProfile.from_dict(payload)

    def test_matching_derived_fields_accepted(self) -> None:
        payload = synthetic_isolated_profile().to_dict(include_derived=True)
        prof = ExecutionProfile.from_dict(payload)  # must not raise
        self.assertTrue(prof.baseline_eligible)

    # --- Round 2 §7: serialized derived fields must be strictly TYPED before the
    # value comparison, so a JSON int/collection/mis-cased hash cannot slip past
    # Python's loose equality (1 == True, list({}) == []). ----------------------
    def test_nonbool_baseline_eligible_rejected(self) -> None:
        payload = synthetic_isolated_profile().to_dict(include_derived=True)
        # Recomputed value is True; a JSON int 1 must NOT be accepted as the bool
        # (1 == True would otherwise sneak past the value comparison).
        payload["baseline_eligible"] = 1
        with self.assertRaises(ProfileError):
            ExecutionProfile.from_dict(payload)

    def test_reasons_empty_nonlist_rejected(self) -> None:
        # For an eligible profile the recomputed reasons are []; an empty string
        # or empty dict must NOT be accepted just because list("")/list({}) == [].
        for bad in ("", {}, ["a", 123]):
            payload = synthetic_isolated_profile().to_dict(include_derived=True)
            payload["baseline_ineligibility_reasons"] = bad
            with self.assertRaises(ProfileError):
                ExecutionProfile.from_dict(payload)

    def test_hash_wrong_format_rejected(self) -> None:
        base = synthetic_isolated_profile().to_dict(include_derived=True)
        good = base["execution_profile_hash"]
        for bad in (good.upper(), good[:63], good + "a", "z" * 64, 123):
            payload = dict(base)
            payload["execution_profile_hash"] = bad
            with self.assertRaises(ProfileError):
                ExecutionProfile.from_dict(payload)


# =============================================================== Fresh finding B
class TestMaterializationRecordClaimBinding(TestMaterializationManifestIntegrity):
    """B: verification must recompute the record's derivable claims from the
    verified file sets and enforce cross-field invariants, not trust them."""

    def test_inflated_materialized_skill_count_rejected(self) -> None:
        bad = replace(self.record, materialized_skill_count=999)
        with self.assertRaises(MaterializationError):
            verify_materialization_manifests(self.root, bad)

    def test_inflated_subagent_count_rejected(self) -> None:
        bad = replace(self.record, subagent_count=999)
        with self.assertRaises(MaterializationError):
            verify_materialization_manifests(self.root, bad)

    def test_false_baseline_eligible_with_ambiguity_rejected(self) -> None:
        bad = replace(
            self.record, ambiguous_excluded=("x/ambiguous.bin",), baseline_eligible=True
        )
        with self.assertRaises(MaterializationError):
            verify_materialization_manifests(self.root, bad)

    def test_partial_install_claiming_baseline_eligible_rejected(self) -> None:
        bad = replace(
            self.record,
            claim_scope=ClaimScope.PARTIAL_INSTALL,
            baseline_eligible=True,
        )
        with self.assertRaises(MaterializationError):
            verify_materialization_manifests(self.root, bad)

    # --- Round 2 §4: the derivable claims must be BOUND, and the claims that
    # cannot be bound from the three manifests must be classified UNVERIFIED,
    # never silently certified. -------------------------------------------------
    _AMBIGUITY_REASON = (
        "ambiguous_needs_owner_review files were excluded from the runtime "
        "surface: ['x/amb.bin']"
    )

    def test_full_library_inflated_shipped_count_rejected(self) -> None:
        # A full-library record materializes EVERY shipped skill, so the shipped
        # total must equal the materialized count; 999 is unbound inflation the
        # >=-floor let through.
        bad = replace(self.record, shipped_skill_count=999)
        with self.assertRaises(MaterializationError):
            verify_materialization_manifests(self.root, bad)

    def test_fabricated_ineligibility_reasons_rejected(self) -> None:
        # Ineligible for a real (ambiguity) cause, but the reason TEXT is a
        # fabrication that does not match the recomputed reason.
        bad = replace(
            self.record,
            ambiguous_excluded=("x/amb.bin",),
            baseline_eligible=False,
            baseline_ineligibility_reasons=("totally fabricated reason",),
        )
        with self.assertRaises(MaterializationError):
            verify_materialization_manifests(self.root, bad)

    def test_ineligible_record_with_empty_reasons_rejected(self) -> None:
        bad = replace(
            self.record,
            ambiguous_excluded=("x/amb.bin",),
            baseline_eligible=False,
            baseline_ineligibility_reasons=(),
        )
        with self.assertRaises(MaterializationError):
            verify_materialization_manifests(self.root, bad)

    def test_eligible_record_with_spurious_reasons_rejected(self) -> None:
        bad = replace(
            self.record,
            baseline_eligible=True,
            baseline_ineligibility_reasons=("spurious reason on an eligible record",),
        )
        with self.assertRaises(MaterializationError):
            verify_materialization_manifests(self.root, bad)

    def test_ambiguity_inventory_is_classified_unverified(self) -> None:
        # Even a fully self-consistent record cannot have its ambiguity inventory
        # bound from the three (include-only) manifests, so it must NOT be
        # certified — only the derivable claims are.
        result = verify_materialization_manifests(self.root, self.record)
        self.assertFalse(result["record_claims_verified"])
        self.assertTrue(result["record_derivable_claims_verified"])
        self.assertIn(
            "ambiguous_excluded_inventory", result["record_claims_unverifiable"]
        )
        # The verifier reads only the destination, so the shipped TOTAL against
        # the source library is disclosed unverified even for a full-library run.
        self.assertIn(
            "shipped_skill_count_total", result["record_claims_unverifiable"]
        )
        self.assertTrue(
            result["record_claims"]["shipped_skill_count_total"].startswith("unverified")
        )

    def test_fabricated_ambiguity_inventory_not_certified(self) -> None:
        # A fabricated/deleted ambiguity list that is internally self-consistent
        # cannot be refuted from the manifests, so it is disclosed UNVERIFIED
        # rather than silently certified.
        rebound = replace(
            self.record,
            ambiguous_excluded=("x/amb.bin",),
            baseline_eligible=False,
            baseline_ineligibility_reasons=(self._AMBIGUITY_REASON,),
        )
        result = verify_materialization_manifests(self.root, rebound)
        self.assertFalse(result["record_claims_verified"])
        self.assertIn(
            "ambiguous_excluded_inventory", result["record_claims_unverifiable"]
        )


# =============================================================== Fresh finding D
class TestEnumerationFailsClosed(TestMaterializationManifestIntegrity):
    """D: an os.walk/scandir enumeration failure must fail closed, never be
    silently skipped (which would omit an extra unlisted subtree)."""

    def test_walk_error_is_fail_closed(self) -> None:
        import tools.behavioral_eval_runner.materialize as materialize_module

        real_walk = os.walk

        def exploding_walk(top, topdown=True, onerror=None, followlinks=False):
            # Simulate an unreadable subtree: the real walk yields the top, then
            # a scandir error occurs on a child that os.walk reports via onerror.
            yielded = False
            for entry in real_walk(top, topdown=topdown, onerror=onerror, followlinks=followlinks):
                yield entry
                if not yielded and onerror is not None:
                    err = OSError("simulated scandir permission error")
                    err.filename = os.path.join(top, "unreadable-subtree")
                    onerror(err)
                yielded = True

        with mock.patch.object(materialize_module.os, "walk", exploding_walk):
            with self.assertRaises(MaterializationError) as ctx:
                verify_materialization_manifests(self.root, self.record)
        self.assertIn("enumerat", str(ctx.exception).lower())


# =============================================================== Fresh finding F
class TestManifestPathsPortability(TestMaterializationManifestIntegrity):
    """F: the schema-governed record must not carry operator-local absolute
    manifest paths (privacy) and must satisfy its additionalProperties:false
    schema."""

    def test_to_dict_omits_absolute_manifest_paths(self) -> None:
        payload = self.record.to_dict()
        # No operator-local absolute path may leak into the portable record.
        blob = json.dumps(payload)
        self.assertNotIn(self.root.replace("\\", "/"), blob)
        self.assertNotIn(":\\", blob)  # windows drive-absolute
        self.assertNotIn("manifest_paths", payload)

    def test_to_dict_keys_subset_of_schema(self) -> None:
        schema_path = os.path.join(
            os.path.dirname(materialize_schema_dir()),
            "schemas",
            "materialization.schema.json",
        )
        with open(schema_path, encoding="utf-8") as handle:
            schema = json.load(handle)
        self.assertFalse(schema.get("additionalProperties", True))
        allowed = set(schema["properties"])
        self.assertTrue(
            set(self.record.to_dict()).issubset(allowed),
            f"record emits keys outside the schema: {set(self.record.to_dict()) - allowed}",
        )


def materialize_schema_dir() -> str:
    import tools.behavioral_eval_runner.materialize as m

    return m.__file__


# =============================================================== Fresh finding C
class TestMaterializationWriteReparse(unittest.TestCase):
    """C (concrete gap): every write, INCLUDING the persisted-manifest writes,
    must go through the reparse-checked write path. The residual cross-platform
    TOCTOU window is documented as a platform non-claim, not silently claimed."""

    def test_write_file_refuses_symlinked_parent(self) -> None:
        from tools.behavioral_eval_runner.materialize import _write_file

        with tempfile.TemporaryDirectory() as root:
            outside = os.path.join(root, "outside")
            os.makedirs(outside)
            link_parent = os.path.join(root, "dest", "nested")
            os.makedirs(os.path.join(root, "dest"))
            try:
                os.symlink(outside, link_parent, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("symlink creation unavailable")
            with self.assertRaises(ReparsePointError):
                _write_file(os.path.join(root, "dest"), "nested/escaped.txt", b"x")

    def test_manifest_writes_use_reparse_checked_path(self) -> None:
        # The persisted-manifest writes must route through _write_file (not a
        # raw open); assert by source inspection that materialize() no longer
        # opens manifest targets with a bare open().
        import inspect
        import tools.behavioral_eval_runner.materialize as m

        src = inspect.getsource(m.materialize)
        self.assertNotIn('open(target, "wb")', src, "manifest write bypasses _write_file")

    # --- Round 2 §5: the parent-chain TOCTOU claim is corrected. On a host
    # without dir-fd no-follow (Windows here) the mid-operation parent swap is
    # honestly reported UNAVAILABLE / NON-BASELINE; on POSIX it is PREVENTED. ---
    def test_reparse_write_capability_matches_platform(self) -> None:
        from tools.behavioral_eval_runner.materialize import (
            _POSIX_NOFOLLOW_WRITE,
            reparse_write_capability,
        )

        report = reparse_write_capability()
        if _POSIX_NOFOLLOW_WRITE:
            self.assertEqual(report["parent_component_toctou"], "PREVENTED")
            self.assertEqual(report["baseline_status"], "IMPLEMENTED_BUT_UNRUN")
        else:
            # Windows evidence host: no dir-fd no-follow, so a mid-operation
            # parent swap cannot be prevented in stdlib — NOT claimed solved.
            self.assertEqual(report["parent_component_toctou"], "UNAVAILABLE")
            self.assertEqual(report["baseline_status"], "NON_BASELINE")

    def test_windows_host_has_no_dirfd_nofollow_write(self) -> None:
        if os.name != "nt":
            self.skipTest("Windows-only residual assertion")
        from tools.behavioral_eval_runner.materialize import _POSIX_NOFOLLOW_WRITE

        self.assertFalse(
            _POSIX_NOFOLLOW_WRITE,
            "Windows stdlib has no dir-fd O_NOFOLLOW; the atomic no-reparse write "
            "must stay UNAVAILABLE / NON-BASELINE (Finding C), not claimed solved",
        )

    @unittest.skipUnless(
        _POSIX_NOFOLLOW_WRITE,
        "descriptor-relative no-follow write is POSIX-only (UNRUN on Windows)",
    )
    def test_posix_parent_swap_between_check_and_open_fails_closed(self) -> None:
        # IMPLEMENTED BUT UNRUN in the WP-2B-1 Windows evidence environment.
        # Interleave an attacker that replaces a freshly-created parent component
        # with a symlink; the no-follow reopen relative to the dir fd must refuse
        # it, so the write fails closed rather than escaping the destination.
        from tools.behavioral_eval_runner.materialize import _write_file

        real_mkdir = os.mkdir

        with tempfile.TemporaryDirectory() as root:
            dest = os.path.join(root, "dest")
            os.makedirs(dest)
            outside = os.path.join(root, "outside")
            os.makedirs(outside)

            def swapping_mkdir(name, mode=0o777, *, dir_fd=None):
                # Simulate the TOCTOU: instead of a real directory, an attacker
                # plants a symlink to an outside directory at this component.
                os.symlink(outside, name, dir_fd=dir_fd)

            with mock.patch("os.mkdir", side_effect=swapping_mkdir):
                with self.assertRaises((ReparsePointError, MaterializationError)):
                    _write_file(dest, "nested/escaped.txt", b"x")
            # And the attack must not have produced a file outside the root.
            self.assertFalse(os.path.exists(os.path.join(outside, "escaped.txt")))
            self.assertEqual(real_mkdir, os.mkdir)  # patch fully reverted


# =============================================================== Fresh finding E
class TestSupervisorDescendantCleanup(unittest.TestCase):
    """E (Round 2): the process group is bound at CREATION, cleanup is VERIFIED,
    and an unverifiable/failed cleanup is never reported as success."""

    @staticmethod
    def _exited_process(pid: int = 777):
        return types.SimpleNamespace(
            pid=pid, poll=lambda: 0, wait=lambda timeout=None: 0
        )

    def test_cleanup_runs_on_normal_leader_exit(self) -> None:
        from tools.behavioral_eval_runner.process_control import (
            SessionCleanupResult,
            SessionWatchdog,
            SupervisedProcess,
        )

        watchdog = SessionWatchdog(timeout_seconds=30)
        supervised = SupervisedProcess(
            process=self._exited_process(4321), session_pgid=4321, isolated=True
        )
        verified = SessionCleanupResult(
            "posix_killpg", True, "VERIFIED_EMPTY", "group empty"
        )
        with mock.patch.object(
            watchdog, "_terminate_and_verify_session", return_value=verified
        ) as cleanup:
            result = watchdog.supervise(supervised)
        self.assertIsNone(result)
        cleanup.assert_called_once()
        self.assertTrue(watchdog.last_cleanup.is_confirmed_clean)

    def test_group_is_bound_at_creation_not_by_late_getpgid(self) -> None:
        # spawn_supervised must record the session pgid at creation. On POSIX,
        # start_new_session=True makes the child its own group leader, so
        # pgid == pid with no getpgid race window (leader may already be gone).
        import subprocess
        from tools.behavioral_eval_runner.process_control import spawn_supervised

        fake_proc = types.SimpleNamespace(pid=4242)
        with (
            mock.patch.object(sys, "platform", "linux"),
            mock.patch.object(subprocess, "Popen", return_value=fake_proc),
        ):
            supervised = spawn_supervised([sys.executable, "-c", "pass"])
        self.assertEqual(supervised.session_pgid, 4242)
        self.assertTrue(supervised.isolated)

    def test_descendants_remaining_after_kill_fails_closed(self) -> None:
        # Cleanup was attempted, but the group is still non-empty on every
        # bounded check: this MUST fail closed, never report success.
        from tools.behavioral_eval_runner.process_control import (
            ProcessControlError,
            SessionWatchdog,
            SupervisedProcess,
        )

        watchdog = SessionWatchdog(timeout_seconds=30)
        watchdog._verify_attempts = 3
        watchdog._verify_interval = 0.0
        supervised = SupervisedProcess(
            process=self._exited_process(), session_pgid=555, isolated=True
        )
        with (
            mock.patch.object(sys, "platform", "linux"),
            mock.patch.object(watchdog, "_posix_kill_group", return_value=None),
            mock.patch.object(watchdog, "_posix_group_alive", return_value=True),
        ):
            with self.assertRaises(ProcessControlError):
                watchdog.supervise(supervised)
        self.assertEqual(watchdog.last_cleanup.verification, "FAILED_NONEMPTY")

    def test_killpg_failure_is_not_swallowed(self) -> None:
        from tools.behavioral_eval_runner.process_control import (
            ProcessControlError,
            SessionWatchdog,
            SupervisedProcess,
        )

        watchdog = SessionWatchdog(timeout_seconds=30)
        supervised = SupervisedProcess(
            process=self._exited_process(), session_pgid=556, isolated=True
        )
        with (
            mock.patch.object(sys, "platform", "linux"),
            mock.patch.object(
                watchdog, "_posix_kill_group", side_effect=OSError("EPERM")
            ),
        ):
            with self.assertRaises(ProcessControlError):
                watchdog.supervise(supervised)
        self.assertEqual(watchdog.last_cleanup.verification, "FAILED_NONEMPTY")

    def test_windows_post_leader_cleanup_is_unavailable_not_success(self) -> None:
        # On Windows, once the leader has exited, descendant reaping cannot be
        # verified in stdlib. The result must be UNAVAILABLE (NOT confirmed
        # clean) — honest NON-BASELINE — and must not raise (it is not a failure,
        # it is unverifiable) and must not claim verified success.
        if os.name != "nt":
            self.skipTest("Windows-only residual assertion")
        from tools.behavioral_eval_runner.process_control import (
            SessionWatchdog,
            SupervisedProcess,
        )

        watchdog = SessionWatchdog(timeout_seconds=30)
        supervised = SupervisedProcess(
            process=self._exited_process(), session_pgid=None, isolated=True
        )
        result = watchdog.supervise(supervised)
        self.assertIsNone(result)
        self.assertEqual(watchdog.last_cleanup.verification, "UNAVAILABLE")
        self.assertFalse(watchdog.last_cleanup.is_confirmed_clean)

    @unittest.skipUnless(os.name == "posix", "POSIX process-group semantics")
    def test_posix_background_child_terminated_after_leader_exit(self) -> None:  # pragma: no cover - POSIX only
        import subprocess

        from tools.behavioral_eval_runner.process_control import (
            SessionWatchdog,
            spawn_supervised,
        )

        leader_src = (
            "import subprocess,sys,os\n"
            "c=subprocess.Popen([sys.executable,'-c','import time;time.sleep(60)'])\n"
            "print(c.pid, flush=True)\n"
        )
        supervised = spawn_supervised(
            [sys.executable, "-c", leader_src], stdout=subprocess.PIPE
        )
        child_pid = int(supervised.process.stdout.readline().decode().strip())
        SessionWatchdog(timeout_seconds=30).supervise(supervised)
        import time as _t

        _t.sleep(0.5)
        alive = True
        try:
            os.kill(child_pid, 0)
        except ProcessLookupError:
            alive = False
        self.assertFalse(alive, "background child must be terminated after leader exit")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
