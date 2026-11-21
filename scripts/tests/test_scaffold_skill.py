"""Tests for scripts/scaffold-skill.py.

Stdlib unittest only (the repo's scripts/tests convention; not CI-wired).
Run from the repository root:

    python -B -P scripts/tests/test_scaffold_skill.py

The temp root is created with a plain Path.mkdir under artifacts/tmp so a
sandbox ACL refusal surfaces as an explicit skip with its reason, not as a
misleading test failure.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import shutil
import types
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = REPO_ROOT / "scripts"
TMP_PARENT = REPO_ROOT / "artifacts" / "tmp"
SKILL_REL = Path(".claude") / "skills" / "sample-skill"
GENERATED = ("SKILL.md", "evals/evals.json", "evals/trigger-evals.json")


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scaffold = _load("aegis_scaffold_skill", SCRIPTS_DIR / "scaffold-skill.py")
validator = _load(
    "aegis_validate_skills_tests", SCRIPTS_DIR / "validate-skills.py")

try:
    import yaml
except ImportError:  # optional; the exact quoted-line assertion covers it
    yaml = None


def valid_config(**overrides):
    config = {
        "name": "sample-skill",
        "description": (
            "Use when the user's task needs the sample skill's deterministic "
            "deliverable checked before merge."
        ),
        "purpose": "Produce a deterministic sample deliverable.",
        "use_when": [
            "A task needs the sample deliverable.",
            "A review must check the deliverable.",
        ],
        "inputs": ["The request.", "The repository tree."],
        "workflow": [
            "Read the inputs.",
            "Produce the deliverable.",
            "Check the result.",
        ],
        "output_format": ["A short report.", "A list of checks."],
        "validation_checklist": [
            "All inputs were read.",
            "The report names each check.",
        ],
        "gotchas": ["Do not invent values."],
        "stop_conditions": ["Stop when the request is ambiguous."],
        "supporting_files": [],
        "positive_prompt": (
            "Use the sample skill to produce and check the deliverable."),
        "negative_prompt": "Design an A/B test with power and sample size.",
        "overlaps_with": ["fixture-neighbor"],
    }
    config.update(overrides)
    return config


def _fresh_root(test_name):
    try:
        TMP_PARENT.mkdir(parents=True, exist_ok=True)
        root = TMP_PARENT / f"{test_name}-{os.getpid()}"
        if root.exists():
            shutil.rmtree(root, ignore_errors=True)
        root.mkdir(parents=True)
        fixture = root / ".claude" / "skills" / "fixture-neighbor" / "SKILL.md"
        fixture.parent.mkdir(parents=True)
        fixture.write_text("# Fixture neighbor\n", encoding="utf-8")
    except OSError as exc:
        raise unittest.SkipTest(
            f"cannot create temp root with Path.mkdir (ACL?): {exc}")
    return root


def _files_under(path):
    return sorted(
        p.relative_to(path).as_posix() for p in path.rglob("*") if p.is_file())


class ScaffoldSkillTests(unittest.TestCase):
    def setUp(self):
        self.root = _fresh_root(self._testMethodName)
        self.addCleanup(shutil.rmtree, self.root, True)

    def _write_config(self, config, file_name="config.json"):
        path = self.root / file_name
        path.write_text(
            json.dumps(config, indent=2) + "\n", encoding="utf-8")
        return path

    def _run(self, *args):
        out = io.StringIO()
        err = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = scaffold.main(list(args))
        return code, out.getvalue(), err.getvalue()

    def _apply(self, config_path, force=False):
        args = ["--config", str(config_path),
                "--repo-root", str(self.root), "--apply"]
        if force:
            args.append("--force")
        return self._run(*args)

    def _apply_config(self, config, force=False):
        return self._apply(self._write_config(config), force=force)

    def test_dry_run_writes_nothing_and_lists_three_paths(self):
        config_path = self._write_config(valid_config())
        before = _files_under(self.root)
        code, out, err = self._run(
            "--config", str(config_path), "--repo-root", str(self.root))
        self.assertEqual(code, 0, err)
        self.assertEqual(err, "")
        self.assertEqual(before, _files_under(self.root))
        self.assertFalse((self.root / SKILL_REL).exists())
        for rel in GENERATED:
            header = f"=== {SKILL_REL.as_posix()}/{rel} ==="
            self.assertIn(header, out)
        self.assertIn("Closures (the generator does not perform these):", out)

    def test_apply_creates_exactly_three_files(self):
        code, out, err = self._apply_config(valid_config())
        self.assertEqual(code, 0, err)
        self.assertEqual(_files_under(self.root / SKILL_REL), list(GENERATED))
        for rel in GENERATED:
            self.assertIn(f"wrote {SKILL_REL.as_posix()}/{rel}", out)

    def test_nine_sections_in_canonical_order(self):
        code, _, err = self._apply_config(valid_config())
        self.assertEqual(code, 0, err)
        text = (self.root / SKILL_REL / "SKILL.md").read_text(
            encoding="utf-8")
        headings = [
            line[3:].strip() for line in text.splitlines()
            if line.startswith("## ")
        ]
        self.assertEqual(headings, list(validator.REQUIRED_SECTIONS))
        self.assertEqual(len(headings), 9)

    def test_frontmatter_name_and_description(self):
        config = valid_config()
        code, _, err = self._apply_config(config)
        self.assertEqual(code, 0, err)
        text = (self.root / SKILL_REL / "SKILL.md").read_text(
            encoding="utf-8")
        fm_text, _body = validator.split_frontmatter(text)
        self.assertIsNotNone(fm_text)
        desc_line = next(
            line for line in fm_text.splitlines()
            if line.startswith("description: "))
        self.assertTrue(desc_line.startswith("description: '"))
        self.assertTrue(desc_line.endswith("'"))
        self.assertIn("''", desc_line)
        if yaml is not None:
            parsed = yaml.safe_load(fm_text)
            self.assertEqual(parsed["name"], config["name"])
            self.assertEqual(parsed["description"], config["description"])
        else:
            doubled = config["description"].replace("'", "''")
            self.assertEqual(desc_line, f"description: '{doubled}'")
            self.assertIn("name: sample-skill", fm_text)
        self.assertLess(len(config["description"]), 1024)

    def test_evals_json_shape(self):
        config = valid_config()
        code, _, err = self._apply_config(config)
        self.assertEqual(code, 0, err)
        payload = json.loads(
            (self.root / SKILL_REL / "evals" / "evals.json").read_text(
                encoding="utf-8"))
        self.assertEqual(
            payload["$schema"],
            "https://json.schemastore.org/claude-skill-evals.json")
        self.assertEqual(payload["skill"], config["name"])
        self.assertEqual(
            payload["description"],
            "Trigger and behavior cases for sample-skill: "
            "Produce a deterministic sample deliverable.")
        self.assertNotEqual(payload["description"], config["description"])
        cases = payload["cases"]
        self.assertEqual([case["id"] for case in cases],
                         ["positive-1", "negative-1"])
        positive, negative = cases
        self.assertEqual(positive["type"], "should_trigger")
        self.assertEqual(positive["prompt"], config["positive_prompt"])
        self.assertIs(positive["expect"]["triggers"], True)
        assertions = positive["expect"]["assertions"]
        self.assertGreaterEqual(len(assertions), 2)
        self.assertLessEqual(len(assertions), 3)
        self.assertIn(config["workflow"][0], assertions[0])
        self.assertEqual(negative["type"], "should_not_trigger")
        self.assertEqual(negative["prompt"], config["negative_prompt"])
        self.assertIs(negative["expect"]["triggers"], False)
        self.assertTrue(any(
            "fixture-neighbor" in item
            for item in negative["expect"]["assertions"]))

    def test_trigger_evals_json_shape(self):
        config = valid_config()
        code, _, err = self._apply_config(config)
        self.assertEqual(code, 0, err)
        payload = json.loads(
            (self.root / SKILL_REL / "evals" / "trigger-evals.json").read_text(
                encoding="utf-8"))
        self.assertEqual(payload["skill"], config["name"])
        self.assertEqual(payload["description"], config["description"])
        self.assertEqual(payload["overlaps_with"], config["overlaps_with"])
        cases = payload["cases"]
        self.assertEqual([case["id"] for case in cases],
                         ["positive-1", "negative-1"])
        positive, negative = cases
        self.assertEqual(positive["expected_skill"], config["name"])
        self.assertEqual(
            positive["should_not_trigger"], config["overlaps_with"])
        self.assertTrue(positive["reason"].strip())
        self.assertEqual(negative["expected_skill"],
                         config["overlaps_with"][0])
        self.assertEqual(negative["should_not_trigger"], [config["name"]])
        self.assertIn(config["overlaps_with"][0], negative["reason"])

    def test_overlaps_resolve_to_installed_skills(self):
        config = valid_config()
        code, _, err = self._apply_config(config)
        self.assertEqual(code, 0, err)
        for overlap in config["overlaps_with"]:
            path = (self.root / ".claude" / "skills" / overlap / "SKILL.md")
            self.assertTrue(path.is_file(), overlap)

    def test_invalid_configs_exit_2_with_one_line(self):
        cases = {
            "name-uppercase": {"name": "BadName"},
            "name-reserved": {"name": "docx"},
            "description-too-long": {"description": "x" * 1024},
            "description-newline": {"description": "line one\nline two"},
            "description-manual-only": {
                "description": "MANUAL-ONLY; never auto-invoke. sample"},
            "workflow-empty": {"workflow": []},
            "unknown-key": {"surprise": "value"},
            "overlap-missing": {"overlaps_with": ["missing-skill"]},
            "overlap-self": {"overlaps_with": ["sample-skill"]},
        }
        for label, overrides in cases.items():
            with self.subTest(label=label):
                config_path = self._write_config(
                    valid_config(**overrides), f"{label}.json")
                code, out, err = self._apply(config_path)
                self.assertEqual(code, 2, out)
                self.assertEqual(out, "")
                self.assertTrue(err.strip(), label)
                self.assertEqual(len(err.strip().splitlines()), 1, err)
                self.assertFalse((self.root / SKILL_REL).exists(), label)

    def test_invalid_utf8_config_exits_2_without_traceback(self):
        path = self.root / "bad-utf8.json"
        path.write_bytes(b'{"name": "x\xff"}')
        code, out, err = self._run(
            "--config", str(path), "--repo-root", str(self.root))
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertEqual(len(err.strip().splitlines()), 1, err)
        self.assertIn("UTF-8", err)
        self.assertNotIn("Traceback", err)
        self.assertFalse((self.root / SKILL_REL).exists())

    def test_missing_validator_constants_fail_closed(self):
        saved = scaffold._VALIDATOR
        self.addCleanup(setattr, scaffold, "_VALIDATOR", saved)
        constants = {
            "RESERVED_BUNDLED_NAMES": frozenset(),
            "SKILL_SHELL_INJECTION_RES": (),
            "MAX_SKILL_LINES": 500,
        }
        config_path = self._write_config(valid_config())
        for missing in constants:
            with self.subTest(attribute=missing):
                present = {
                    key: value for key, value in constants.items()
                    if key != missing
                }
                scaffold._VALIDATOR = types.SimpleNamespace(**present)
                code, out, err = self._run(
                    "--config", str(config_path),
                    "--repo-root", str(self.root))
                self.assertEqual(code, 2)
                self.assertEqual(out, "")
                self.assertEqual(len(err.strip().splitlines()), 1, err)
                self.assertIn(missing, err)
                self.assertNotIn("Traceback", err)
                self.assertFalse((self.root / SKILL_REL).exists())

    def test_existing_dir_refuses_then_force_overwrites_only_three(self):
        config_path = self._write_config(valid_config())
        skill_dir = self.root / SKILL_REL
        skill_dir.mkdir(parents=True)
        (skill_dir / "notes.txt").write_text("keep\n", encoding="utf-8")
        (skill_dir / "SKILL.md").write_text("OLD\n", encoding="utf-8")

        code, _out, err = self._apply(config_path)
        self.assertEqual(code, 2)
        self.assertIn("already exists", err)
        self.assertEqual(
            (skill_dir / "SKILL.md").read_text(encoding="utf-8"), "OLD\n")

        code, _out, err = self._apply(config_path, force=True)
        self.assertEqual(code, 0, err)
        text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        self.assertNotEqual(text, "OLD\n")
        self.assertIn("## Purpose", text)
        self.assertEqual(
            (skill_dir / "notes.txt").read_text(encoding="utf-8"), "keep\n")
        self.assertEqual(
            sorted(_files_under(skill_dir)),
            sorted(list(GENERATED) + ["notes.txt"]))

        changed = valid_config(purpose="A changed purpose.")
        code, _out, err = self._apply_config(changed, force=True)
        self.assertEqual(code, 0, err)
        text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("A changed purpose.", text)
        self.assertEqual(
            (skill_dir / "notes.txt").read_text(encoding="utf-8"), "keep\n")

    def test_two_applies_are_byte_identical(self):
        config = valid_config()
        config_path = self._write_config(config)
        code, _, err = self._apply(config_path)
        self.assertEqual(code, 0, err)
        skill_dir = self.root / SKILL_REL
        first = {rel: (skill_dir / rel).read_bytes() for rel in GENERATED}

        code, _, err = self._apply(config_path, force=True)
        self.assertEqual(code, 0, err)
        second = {rel: (skill_dir / rel).read_bytes() for rel in GENERATED}
        self.assertEqual(first, second)

        other = self.root / "second-repo"
        fixture = other / ".claude" / "skills" / "fixture-neighbor" / "SKILL.md"
        fixture.parent.mkdir(parents=True)
        fixture.write_text("# Fixture neighbor\n", encoding="utf-8")
        code, _, err = self._run(
            "--config", str(config_path), "--repo-root", str(other), "--apply")
        self.assertEqual(code, 0, err)
        third = {
            rel: (other / SKILL_REL / rel).read_bytes() for rel in GENERATED
        }
        self.assertEqual(first, third)
        self.assertNotIn(
            str(self.root), first["SKILL.md"].decode("utf-8"))

    def test_no_catalog_readme_manifest_or_baseline_created(self):
        code, _, err = self._apply_config(valid_config())
        self.assertEqual(code, 0, err)
        for rel in (
            "docs/skills-catalog.md",
            "README.md",
            "tools/skills-manifest.json",
            "artifacts/audits/skill-contract-audit-baseline.json",
        ):
            self.assertFalse((self.root / rel).exists(), rel)

    def test_closures_print_in_order(self):
        config_path = self._write_config(valid_config())
        code, out, err = self._run(
            "--config", str(config_path), "--repo-root", str(self.root))
        self.assertEqual(code, 0, err)
        markers = [
            "Review the generated text",
            "docs/skills-catalog.md row",
            "--refresh-skills-manifest",
            "--write-readme-counts and commit",
            "test_audit_skill_contracts.py",
            "skill-contract-audit-baseline.json and review the diff",
        ]
        positions = [out.find(marker) for marker in markers]
        for marker, position in zip(markers, positions):
            self.assertNotEqual(position, -1, marker)
        self.assertEqual(positions, sorted(positions))

    def _assert_bad_overlap(self, overlap):
        """A bad overlap name is refused before the path or existence check."""
        config_path = self._write_config(
            valid_config(overlaps_with=[overlap]))
        before = _files_under(self.root)
        code, out, err = self._apply(config_path)
        self.assertEqual(code, 2, err)
        self.assertEqual(out, "")
        self.assertEqual(len(err.strip().splitlines()), 1, err)
        self.assertIn("name pattern", err)
        self.assertEqual(before, _files_under(self.root))
        self.assertFalse((self.root / SKILL_REL).exists())

    def test_overlap_with_colon_is_rejected_by_name_pattern(self):
        self._assert_bad_overlap("C:x")

    def test_overlap_with_parent_traversal_is_rejected_by_name_pattern(self):
        self._assert_bad_overlap("../evil")

    def test_overlap_with_slash_is_rejected_by_name_pattern(self):
        self._assert_bad_overlap("a/b")

    def test_overlap_with_uppercase_is_rejected_by_name_pattern(self):
        self._assert_bad_overlap("UPPER")

    def test_trigger_note_with_newline_is_rejected(self):
        for note in ("line one\nline two", "line one\rline two"):
            with self.subTest(note=repr(note)):
                config_path = self._write_config(
                    valid_config(trigger_note=note))
                before = _files_under(self.root)
                code, out, err = self._apply(config_path)
                self.assertEqual(code, 2, err)
                self.assertEqual(out, "")
                self.assertEqual(len(err.strip().splitlines()), 1, err)
                self.assertIn("trigger_note", err)
                self.assertIn("one-line", err)
                self.assertEqual(before, _files_under(self.root))
                self.assertFalse((self.root / SKILL_REL).exists())


def tearDownModule():
    try:
        TMP_PARENT.rmdir()
    except OSError:
        pass


if __name__ == "__main__":
    unittest.main(verbosity=2)
