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
)
from tools.behavioral_eval_runner.execution_profile import (
    REQUIRED_FOR_BASELINE,
    ExecutionProfile,
    synthetic_isolated_profile,
)
from tools.behavioral_eval_runner.materialize import (
    MaterializationRecord,
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


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
