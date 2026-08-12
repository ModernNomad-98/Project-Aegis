"""Materializer: full-library rule, profiles, landmarks, three manifests,
leakage rejection, partial-install scoping, path/reparse safety
(areas 9–13, part of 20)."""

from __future__ import annotations

import os
import tempfile
import unittest

from tools.behavioral_eval_runner import AUTHORIZATION_MERGE_SHA
from tools.behavioral_eval_runner.enums import ClaimScope, MaterializationProfile, WorkspaceRole
from tools.behavioral_eval_runner.errors import (
    PathEscapeError,
    PartialSurfaceViolationError,
    RoleMismatchError,
    SnapshotVerificationError,
)
from tools.behavioral_eval_runner.materialize import (
    FixtureDefinition,
    GitSnapshot,
    MaterializationRequest,
    SyntheticSnapshot,
    discover_shipped_skills,
    materialize,
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
            )
        )
        runtime = self._runtime_paths()
        for landmark in SOURCE_LANDMARK_PATHS:
            self.assertIn(landmark, runtime)
        self.assertTrue(record.baseline_eligible)

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
