"""Materializer: full-library rule, profiles, landmarks, three manifests,
leakage rejection, partial-install scoping, path/reparse safety
(areas 9–13, part of 20)."""

from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from unittest import mock

from tools.behavioral_eval_runner import AUTHORIZATION_MERGE_SHA
from tools.behavioral_eval_runner.enums import ClaimScope, MaterializationProfile, WorkspaceRole
from tools.behavioral_eval_runner.errors import (
    PathEscapeError,
    PartialSurfaceViolationError,
    RoleMismatchError,
    SnapshotVerificationError,
    MaterializationError,
    ReparsePointError,
)
from tools.behavioral_eval_runner.materialize import (
    WRITE_INTEGRITY_BASELINE,
    _POSIX_NOFOLLOW_WRITE,
    FixtureDefinition,
    GitSnapshot,
    MaterializationRequest,
    SyntheticSnapshot,
    discover_shipped_skills,
    materialize,
    verify_materialization_manifests,
)
from tools.behavioral_eval_runner.tests.helpers import REPO_ROOT, synthetic_corpus_files

SOURCE_LANDMARK_PATHS = (
    "README.md",
    "docs/skills-catalog.md",
    "scripts/validate-skills.py",
    "artifacts/audits/skill-contract-audit-baseline.json",
)


def _request(
    dest: str,
    profile: MaterializationProfile = MaterializationProfile.CONSUMER_SKILLS_ONLY,
    role: WorkspaceRole = WorkspaceRole.CONSUMER,
    claim: ClaimScope = ClaimScope.FULL_LIBRARY,
    **kwargs,
) -> MaterializationRequest:
    return MaterializationRequest(
        snapshot=SyntheticSnapshot(synthetic_corpus_files()),
        profile=profile,
        workspace_role=role,
        claim_scope=claim,
        destination_root=dest,
        **kwargs,
    )


class TestSyntheticMaterialization(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.dest = self._tmp.name
        self.addCleanup(self._tmp.cleanup)

    def _runtime_paths(self) -> set[str]:
        found: set[str] = set()
        runtime_root = os.path.join(self.dest, "runtime_surface")
        for directory, _dirs, files in os.walk(runtime_root):
            for name in files:
                full = os.path.join(directory, name)
                found.add(os.path.relpath(full, runtime_root).replace("\\", "/"))
        return found

    @unittest.skipUnless(os.name == "nt", "Windows 8.3 aliases only")
    def test_short_destination_alias_materializes_and_verifies(self) -> None:
        destination = os.path.realpath(self.dest)
        # A fixed, read-only command asks Windows for the short spelling of
        # cwd. No caller path is interpolated into shell code; /d disables
        # AutoRun and /u makes the built-in echo output unambiguous Unicode.
        alias = subprocess.check_output(
            'cmd /d /u /c for %I in (.) do @echo "%~fsI"',
            cwd=destination, encoding="utf-16le", timeout=10,
        ).strip().removeprefix('"').removesuffix('"')
        self.assertTrue(os.path.samefile(alias, destination))
        if os.path.normcase(alias) == os.path.normcase(destination):
            self.skipTest("this volume supplies no distinct 8.3 alias")

        record = materialize(_request(alias))
        self.assertTrue(verify_materialization_manifests(alias, record)["verified"])
        self.assertTrue(verify_materialization_manifests(destination, record)["verified"])
        for path in record.manifest_paths.values():
            self.assertEqual(os.path.normcase(path), os.path.normcase(os.path.realpath(path)))

    def test_real_host_default_materialization_is_non_baseline(self) -> None:
        # §6.A: with no injected write-integrity capability, a real-host
        # materialization must NOT be baseline-eligible — write-integrity is
        # NON_BASELINE on this host and the record must say so, machine-readably.
        record = materialize(_request(self.dest))
        self.assertFalse(record.write_integrity_baseline)
        self.assertFalse(record.baseline_eligible)
        self.assertTrue(
            any("write-integrity" in r for r in record.baseline_ineligibility_reasons),
            record.baseline_ineligibility_reasons,
        )

    def test_empty_fixture_materializes_and_verifies(self) -> None:
        record = materialize(_request(self.dest))
        self.assertEqual(record.product_fixture_manifest["files"], [])
        self.assertTrue(os.path.isdir(os.path.join(self.dest, "product_fixture")))
        self.assertTrue(verify_materialization_manifests(self.dest, record)["verified"])

    def test_empty_control_plane_materializes_and_verifies(self) -> None:
        record = materialize(MaterializationRequest(
            snapshot=SyntheticSnapshot({".claude/skills/skill-a/SKILL.md": b"# skill-a"}),
            profile=MaterializationProfile.CONSUMER_SKILLS_ONLY,
            workspace_role=WorkspaceRole.CONSUMER,
            claim_scope=ClaimScope.FULL_LIBRARY,
            destination_root=self.dest,
        ))
        self.assertEqual(record.control_plane_manifest["files"], [])
        self.assertTrue(os.path.isdir(os.path.join(self.dest, "control_plane")))
        self.assertTrue(verify_materialization_manifests(self.dest, record)["verified"])

    def test_removed_empty_area_is_not_verified(self) -> None:
        record = materialize(_request(self.dest))
        os.rmdir(os.path.join(self.dest, "product_fixture"))
        with self.assertRaisesRegex(MaterializationError, "missing materialized area"):
            verify_materialization_manifests(self.dest, record)

    @unittest.skipUnless(os.name == "nt", "Windows writer creates absent destination parents")
    def test_empty_control_plane_with_absent_destination(self) -> None:
        destination = os.path.join(self.dest, "new", "destination")
        record = materialize(MaterializationRequest(
            snapshot=SyntheticSnapshot({".claude/skills/skill-a/SKILL.md": b"# skill-a"}),
            profile=MaterializationProfile.CONSUMER_SKILLS_ONLY,
            workspace_role=WorkspaceRole.CONSUMER,
            claim_scope=ClaimScope.FULL_LIBRARY,
            destination_root=destination,
        ))
        self.assertEqual(record.control_plane_manifest["files"], [])
        self.assertTrue(verify_materialization_manifests(destination, record)["verified"])

    @unittest.skipUnless(_POSIX_NOFOLLOW_WRITE, "requires POSIX no-follow directory descriptors")
    def test_empty_area_swap_cannot_redirect_creation(self) -> None:
        mkdir = os.mkdir
        with tempfile.TemporaryDirectory() as outside:
            def swap_area(path, *args, **kwargs):
                result = mkdir(path, *args, **kwargs)
                if path == "product_fixture" and "dir_fd" in kwargs:
                    os.rmdir(path, dir_fd=kwargs["dir_fd"])
                    os.symlink(outside, path, dir_fd=kwargs["dir_fd"])
                return result

            with mock.patch("os.mkdir", side_effect=swap_area):
                with self.assertRaises(ReparsePointError):
                    materialize(_request(self.dest))
            self.assertEqual(os.listdir(outside), [])

    def test_full_library_materializes_every_shipped_skill(self) -> None:
        record = materialize(_request(self.dest))
        self.assertEqual(record.shipped_skill_count, 3)
        self.assertEqual(record.materialized_skill_count, 3)
        runtime = self._runtime_paths()
        for skill in ("skill-a", "skill-b", "skill-c"):
            self.assertIn(f".claude/skills/{skill}/SKILL.md", runtime)
        self.assertNotIn(".claude/skills/_template/SKILL.md", runtime)

    def test_no_control_plane_file_in_runtime_surface(self) -> None:
        materialize(_request(self.dest))
        runtime = self._runtime_paths()
        for path in runtime:
            self.assertNotIn("/evals/", f"/{path}")
            self.assertFalse(path.endswith(("evals.json", "trigger-evals.json")), path)

    def test_ambiguous_file_excluded_and_recorded(self) -> None:
        record = materialize(_request(self.dest))
        self.assertIn(".claude/skills/skill-b/notes.bin", record.ambiguous_excluded)
        self.assertNotIn(".claude/skills/skill-b/notes.bin", self._runtime_paths())

    def test_consumer_profiles_exclude_source_landmarks(self) -> None:
        materialize(
            _request(
                self.dest,
                profile=MaterializationProfile.CONSUMER_WITH_STARTUP_ROUTING,
            )
        )
        runtime = self._runtime_paths()
        for landmark in SOURCE_LANDMARK_PATHS:
            self.assertNotIn(landmark, runtime)
        self.assertIn("AGENTS.md", runtime)
        self.assertIn("CLAUDE.md", runtime)

    def test_skills_only_profile_has_no_startup_files_or_subagents(self) -> None:
        materialize(_request(self.dest))
        runtime = self._runtime_paths()
        self.assertNotIn("AGENTS.md", runtime)
        self.assertNotIn("CLAUDE.md", runtime)
        self.assertFalse(any(p.startswith(".claude/agents/") for p in runtime))

    def test_subagents_only_in_subagent_profile(self) -> None:
        record = materialize(
            _request(
                self.dest,
                profile=MaterializationProfile.CONSUMER_WITH_SUBAGENTS,
            )
        )
        self.assertEqual(record.subagent_count, 1)
        self.assertIn(".claude/agents/reviewer-agent.md", self._runtime_paths())

    def test_source_library_includes_landmarks(self) -> None:
        # Use a clean corpus (no ambiguous supporting file) so this test isolates
        # landmark inclusion and clean-source baseline eligibility.
        clean = {
            k: v for k, v in synthetic_corpus_files().items() if not k.endswith("notes.bin")
        }
        record = materialize(
            MaterializationRequest(
                snapshot=SyntheticSnapshot(clean),
                profile=MaterializationProfile.SOURCE_LIBRARY,
                workspace_role=WorkspaceRole.SOURCE_LIBRARY,
                claim_scope=ClaimScope.FULL_LIBRARY,
                destination_root=self.dest,
                # §6.A: inject a PROVEN synthetic write-integrity capability so this
                # deterministic offline test can exercise a baseline-eligible run.
                # A real-host default omits it and is NON_BASELINE.
                write_integrity_capability=WRITE_INTEGRITY_BASELINE,
            )
        )
        runtime = self._runtime_paths()
        for landmark in SOURCE_LANDMARK_PATHS:
            self.assertIn(landmark, runtime)
        self.assertTrue(record.baseline_eligible)
        self.assertTrue(record.write_integrity_baseline)

    def test_ambiguous_material_makes_baseline_ineligible(self) -> None:
        # C5: the ambiguous notes.bin is excluded AND marks the run ineligible.
        record = materialize(_request(self.dest))
        self.assertFalse(record.baseline_eligible)
        self.assertTrue(
            any("ambiguous" in r for r in record.baseline_ineligibility_reasons)
        )

    def test_role_profile_mismatch_fails_closed(self) -> None:
        with self.assertRaises(RoleMismatchError):
            materialize(
                _request(self.dest, profile=MaterializationProfile.SOURCE_LIBRARY)
            )
        with self.assertRaises(RoleMismatchError):
            materialize(_request(self.dest, role=WorkspaceRole.SOURCE_LIBRARY))

    def test_three_manifests_hashed_separately(self) -> None:
        record = materialize(
            _request(
                self.dest,
                fixture=FixtureDefinition(
                    fixture_id="fx-1", files={"app/readme.txt": b"fixture"}
                ),
            )
        )
        hashes = {
            record.control_plane_manifest_sha256,
            record.runtime_surface_manifest_sha256,
            record.product_fixture_manifest_sha256,
        }
        self.assertEqual(len(hashes), 3)
        self.assertEqual(record.control_plane_manifest["manifest_kind"], "authored_eval_corpus")
        self.assertEqual(
            record.runtime_surface_manifest["manifest_kind"], "sanitized_runtime_surface"
        )
        self.assertEqual(record.product_fixture_manifest["manifest_kind"], "product_fixture")
        for entry in record.runtime_surface_manifest["files"]:
            self.assertEqual(len(entry["sha256"]), 64)

    def test_partial_requires_matching_profile_and_claim(self) -> None:
        with self.assertRaises(PartialSurfaceViolationError):
            materialize(_request(self.dest, partial_skill_subset=("skill-a",)))
        with self.assertRaises(PartialSurfaceViolationError):
            materialize(
                _request(
                    self.dest,
                    profile=MaterializationProfile.CONSUMER_PARTIAL_INSTALL,
                    claim=ClaimScope.FULL_LIBRARY,
                    partial_skill_subset=("skill-a",),
                )
            )
        with self.assertRaises(PartialSurfaceViolationError):
            materialize(
                _request(
                    self.dest,
                    profile=MaterializationProfile.CONSUMER_PARTIAL_INSTALL,
                    claim=ClaimScope.PARTIAL_INSTALL,
                )
            )

    def test_partial_install_marked_baseline_ineligible(self) -> None:
        record = materialize(
            _request(
                self.dest,
                profile=MaterializationProfile.CONSUMER_PARTIAL_INSTALL,
                claim=ClaimScope.PARTIAL_INSTALL,
                partial_skill_subset=("skill-a",),
            )
        )
        self.assertFalse(record.baseline_eligible)
        self.assertTrue(record.baseline_ineligibility_reasons)
        self.assertEqual(record.materialized_skill_count, 1)

    def test_fixture_path_escape_refused(self) -> None:
        for evil in ("../evil.txt", "a/../../evil", "/abs.txt", "C:/x.txt"):
            with self.assertRaises(PathEscapeError):
                materialize(
                    _request(
                        self.dest,
                        fixture=FixtureDefinition(fixture_id="fx", files={evil: b"x"}),
                    )
                )


class TestGitSnapshot(unittest.TestCase):
    def test_real_repo_tree_verification(self) -> None:
        expected_tree = "def17d77fa2cd9c854bd4b16687f0b0350ebdefe"
        snapshot = GitSnapshot(REPO_ROOT, AUTHORIZATION_MERGE_SHA, expected_tree)
        files = snapshot.files()
        skills = discover_shipped_skills(files)
        self.assertEqual(len(skills), 184)
        self.assertNotIn("_template", skills)

    def test_tree_mismatch_fails_closed(self) -> None:
        with self.assertRaises(SnapshotVerificationError):
            GitSnapshot(REPO_ROOT, AUTHORIZATION_MERGE_SHA, "0" * 40)

    def test_short_sha_rejected(self) -> None:
        with self.assertRaises(SnapshotVerificationError):
            GitSnapshot(REPO_ROOT, "fc98ee6", "def17d77fa2cd9c854bd4b16687f0b0350ebdefe")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
