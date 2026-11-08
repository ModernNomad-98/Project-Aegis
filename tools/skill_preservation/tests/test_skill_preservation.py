#!/usr/bin/env python3
"""Self-tests for the Skill-Preservation Guard (synthetic fixtures only; no network)."""
import hashlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

TESTS_DIR = Path(__file__).resolve().parent
TOOL_DIR = TESTS_DIR.parent
sys.path.insert(0, str(TOOL_DIR))
import check_skill_preservation as guard


class TempRoot:
    """Small temp-root helper: some sandboxed hosts deny writes inside tempfile.mkdtemp dirs."""

    def __init__(self, name):
        self.name = name

    def cleanup(self):
        shutil.rmtree(self.name, ignore_errors=True)


def make_temp_root():
    import uuid
    bases = [Path(tempfile.gettempdir()), TOOL_DIR, Path.cwd()]
    for base in bases:
        try:
            root = Path(base) / ("guard-tests-" + uuid.uuid4().hex[:12])
            probe = root / "probe"
            probe.mkdir(parents=True)
            probe.rmdir()
            return TempRoot(str(root))
        except OSError:
            continue
    raise RuntimeError("no writable temporary root available for guard tests")

SKILL_MD_TEMPLATE = """---
name: {name}
description: 'A synthetic test skill named {name} for guard self-tests.'
---

# {name}

Synthetic body for guard tests. It contains no private data and no executable content.
"""


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def manifest_entries(tree):
    skills = sorted(p for p in (tree / ".claude" / "skills").iterdir()
                    if p.is_dir() and p.name != "_template")
    entries = []
    for skill in skills:
        data = (skill / "SKILL.md").read_bytes().replace(b"\r\n", b"\n")
        entries.append({
            "name": skill.name,
            "path": ".claude/skills/%s/SKILL.md" % skill.name,
            "sha256": sha256_bytes(data),
        })
    return entries


def build_fixture_tree(root):
    root = Path(root)
    for name in ("alpha", "beta"):
        skill = root / ".claude" / "skills" / name
        write(skill / "SKILL.md", SKILL_MD_TEMPLATE.format(name=name))
        write(skill / "references" / "notes.md", "# notes for %s\n" % name)
        write(skill / "evals" / "evals.json", json.dumps({"cases": []}) + "\n")
        write(skill / "evals" / "trigger-evals.json", json.dumps({"cases": []}) + "\n")
    template = root / ".claude" / "skills" / "_template"
    write(template / "SKILL.md", SKILL_MD_TEMPLATE.format(name="_template"))
    write(root / "docs" / "skills-catalog.md",
          "# Catalog\n\n- alpha\n- beta\n")
    write(root / "README.md", "# Project Aegis fixture\n\nSkills: alpha, beta.\n")
    write(root / "tools" / "skills-manifest.json", json.dumps({
        "schema": guard.MANIFEST_SCHEMA,
        "source_revision": "fixture-revision",
        "hash_input": guard.MANIFEST_HASH_INPUT,
        "skills": manifest_entries(root),
    }, indent=2) + "\n")
    write(root / "docs" / "consumer-starter-package.md",
          "# Consumer starter package fixture\n\n"
          "| file | bytes | lines |\n|---|---|---|\n"
          "| .claude/skills/alpha/SKILL.md | 100 | 10 |\n"
          "| .claude/skills/beta/SKILL.md | 100 | 10 |\n")
    write(root / "tools" / "other" / "keep.txt", "unrelated fixture file\n")
    return root


def copy_tree(source, destination):
    shutil.copytree(str(source), str(destination))
    return Path(destination)


class GuardSelfTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = make_temp_root()
        cls.base_root = build_fixture_tree(Path(cls.tmp.name) / "clean")
        cls.baseline = guard.build_baseline(str(cls.base_root),
                                           source_revision="fixture-revision",
                                           source_tree="fixture-tree",
                                           base_commit="fixture-commit")
        cls.baseline_path = Path(cls.tmp.name) / "baseline.json"
        guard.atomic_write_bytes(str(cls.baseline_path),
                                 guard.dump_json(cls.baseline).encode("utf-8"))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def new_candidate(self, label):
        return copy_tree(self.base_root, Path(self.tmp.name) / ("candidate-" + label))

    def run_check(self, tree, extra_args=None):
        argv = ["check", "--tree", str(tree), "--baseline", str(self.baseline_path), "--json"]
        if extra_args:
            argv.extend(extra_args)
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = guard.main(argv)
        payload = None
        if out.getvalue().strip():
            payload = json.loads(out.getvalue())
        return code, payload, out.getvalue(), err.getvalue()

    def rules(self, payload):
        return [item["rule"] for item in payload["findings"]]

    def test_c01_clean_tree_passes(self):
        code, payload, out, err = self.run_check(self.new_candidate("clean"))
        self.assertEqual(code, 0)
        self.assertEqual(payload["summary"]["BLOCK"], 0)
        self.assertEqual(payload["findings"], [])

    def test_c02_disappeared_skill_blocks(self):
        tree = self.new_candidate("removed")
        shutil.rmtree(str(tree / ".claude" / "skills" / "alpha"))
        code, payload, out, err = self.run_check(tree)
        self.assertEqual(code, 1)
        self.assertIn("DISAPPEARED_SKILL", self.rules(payload))

    def test_c02b_template_removal_blocks(self):
        tree = self.new_candidate("template-removed")
        shutil.rmtree(str(tree / ".claude" / "skills" / "_template"))
        code, payload, out, err = self.run_check(tree)
        self.assertEqual(code, 1)
        self.assertIn("TEMPLATE_DISAPPEARED", self.rules(payload))

    def test_c02b2_template_supporting_file_removal_blocks(self):
        tree = self.new_candidate("template-file-removed")
        (tree / ".claude" / "skills" / "_template" / "SKILL.md").unlink()
        code, payload, out, err = self.run_check(tree)
        self.assertEqual(code, 1)
        rules = self.rules(payload)
        self.assertTrue("MISSING_SUPPORTING_FILE" in rules or "TEMPLATE_SKILL_MD_MISSING" in rules)

    def test_c02c_inline_comment_boolean_is_parsed(self):
        tree = self.new_candidate("inline-comment-boolean")
        skill_md = tree / ".claude" / "skills" / "alpha" / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8").replace(
            "name: alpha", "name: alpha\ndisable-model-invocation: true # inline comment", 1)
        write(skill_md, text)
        code, payload, out, err = self.run_check(tree)
        self.assertEqual(code, 1)
        self.assertIn("SILENT_DISABLE", self.rules(payload))

    def test_c02e_nested_baseline_shapes_fail_closed(self):
        tail = self.new_candidate("malformed-nested-baseline")
        for label, mutate in (
            ("starter-null", lambda b: b["starter"].__setitem__("declared_paths", None)),
            ("mentions-null", lambda b: b["discovery"].__setitem__("catalog_mentions", None)),
            ("skill-md-string", lambda b: b["skills"]["alpha"].__setitem__("skill_md", "bad")),
        ):
            bad = json.loads(json.dumps(self.baseline))
            mutate(bad)
            bad["baseline_id"] = guard.compute_baseline_id(bad)
            bad_path = Path(self.tmp.name) / ("malformed-" + label + ".json")
            guard.atomic_write_bytes(str(bad_path), guard.dump_json(bad).encode("utf-8"))
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = guard.main(["check", "--tree", str(tail),
                                   "--baseline", str(bad_path), "--json"])
            self.assertEqual(code, 2, label)

    def test_c02f_block_scalar_sentinel_blocks(self):
        tree = self.new_candidate("block-sentinel")
        skill_md = tree / ".claude" / "skills" / "alpha" / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8").replace(
            "description: 'A synthetic test skill named alpha for guard self-tests.'",
            "description: >\n  MANUAL-ONLY; never auto-invoke. synthetic", 1)
        write(skill_md, text)
        code, payload, out, err = self.run_check(tree)
        self.assertEqual(code, 1)
        self.assertIn("SILENT_DISABLE", self.rules(payload))

    def test_c02g_flow_mapping_disable_is_not_ignored(self):
        tree = self.new_candidate("flow-mapping")
        skill_md = tree / ".claude" / "skills" / "alpha" / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8").replace(
            "name: alpha", "name: alpha\ndisable-model-invocation : true", 1)
        write(skill_md, text)
        code, payload, out, err = self.run_check(tree)
        self.assertEqual(code, 1)
        self.assertIn("SILENT_DISABLE", self.rules(payload))

    def test_c02i_quoted_disable_keys_block(self):
        for label, line in (
            ("double", '"disable-model-invocation": true'),
            ("single", "'disable-model-invocation': true"),
        ):
            tree = self.new_candidate("quoted-key-" + label)
            skill_md = tree / ".claude" / "skills" / "alpha" / "SKILL.md"
            text = skill_md.read_text(encoding="utf-8").replace(
                "name: alpha", "name: alpha\n" + line, 1)
            write(skill_md, text)
            code, payload, out, err = self.run_check(tree)
            self.assertEqual(code, 1, label + ": " + out)
            self.assertIn("SILENT_DISABLE", self.rules(payload), label)

    def test_c02i2_nested_flow_or_quoted_json_is_not_a_top_level_setting(self):
        for label, line in (
            ("nested-flow", 'meta: {description: x, "disable-model-invocation": true}'),
            ("quoted-json",
             'description: \'Example JSON: {"disable-model-invocation": true}\''),
        ):
            tree = self.new_candidate("nested-dmi-" + label)
            skill_md = tree / ".claude" / "skills" / "alpha" / "SKILL.md"
            text = skill_md.read_text(encoding="utf-8")
            if label == "nested-flow":
                text = text.replace("name: alpha", "name: alpha\n" + line, 1)
            else:
                text = text.replace(
                    "description: 'A synthetic test skill named alpha for guard self-tests.'",
                    line, 1)
            write(skill_md, text)
            code, payload, out, err = self.run_check(tree)
            self.assertEqual(code, 0, label + ": " + out)
            self.assertNotIn("SILENT_DISABLE", self.rules(payload), label)

    def test_c02i3_prose_sentinel_mention_is_not_a_manual_only_declaration(self):
        tree = self.new_candidate("prose-sentinel")
        skill_md = tree / ".claude" / "skills" / "alpha" / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8").replace(
            "description: 'A synthetic test skill named alpha for guard self-tests.'",
            "description: 'A note: MANUAL-ONLY; never auto-invoke. appears in prose only.'", 1)
        write(skill_md, text)
        code, payload, out, err = self.run_check(tree)
        self.assertEqual(code, 0, out)
        self.assertNotIn("SILENT_DISABLE", self.rules(payload))

    def test_c02k_exact_sentinel_without_trailing_space_blocks(self):
        for label, extra in (("quoted", ""), ("block", ""), ("missing-name", "")):
            tree = self.new_candidate("exact-sentinel-" + label)
            skill_md = tree / ".claude" / "skills" / "alpha" / "SKILL.md"
            text = skill_md.read_text(encoding="utf-8")
            if label == "block":
                text = text.replace(
                    "description: 'A synthetic test skill named alpha for guard self-tests.'",
                    "description: >\n  MANUAL-ONLY; never auto-invoke.", 1)
            else:
                text = text.replace("name: alpha", "name: alpha", 1)
                text = text.replace(
                    "description: 'A synthetic test skill named alpha for guard self-tests.'",
                    "description: 'MANUAL-ONLY; never auto-invoke.'", 1)
            if label == "missing-name":
                text = text.replace("name: alpha\n", "", 1)
            write(skill_md, text)
            code, payload, out, err = self.run_check(tree)
            self.assertEqual(code, 1, label + ": " + out)
            self.assertIn("SILENT_DISABLE", self.rules(payload), label)

    def test_c02j_unparseable_frontmatter_still_blocks_silent_disable(self):
        tree = self.new_candidate("unparseable-silent-disable")
        skill_md = tree / ".claude" / "skills" / "alpha" / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8").replace("name: alpha", "", 1)
        text = text.replace("description:", "disable-model-invocation: true\ndescription:", 1)
        write(skill_md, text)
        code, payload, out, err = self.run_check(tree)
        self.assertEqual(code, 1)
        self.assertIn("SILENT_DISABLE", self.rules(payload))

    def test_c02h_skill_mention_is_token_bounded(self):
        self.assertFalse(guard.mentions_skill("ai-threat-modeler", "threat-modeler"))
        self.assertTrue(guard.mentions_skill("- threat-modeler", "threat-modeler"))
        self.assertFalse(guard.mentions_skill("my_alpha", "alpha"))
        self.assertFalse(guard.mentions_skill("alpha_beta", "alpha"))
        self.assertTrue(guard.mentions_skill("alpha", "alpha"))

    def test_p2e_missing_name_is_block(self):
        tree = self.new_candidate("missing-name-block")
        skill_md = tree / ".claude" / "skills" / "alpha" / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8").replace("name: alpha\n", "", 1)
        write(skill_md, text)
        code, payload, out, err = self.run_check(tree)
        self.assertEqual(code, 1, out)
        findings = [item for item in payload["findings"] if item["rule"] == "NAME_MISSING"]
        self.assertEqual(1, len(findings))
        self.assertEqual("BLOCK", findings[0]["severity"])

    def test_p2f_mention_masking_and_path_mentions(self):
        cases = {
            "underscore": "# Catalog\n\n- beta\n- my_alpha\n",
            "dot": "# Catalog\n\n- beta\n- alpha.md\n",
            "suffix": "# Catalog\n\n- beta\n- alpha_old\n",
        }
        for label, text in cases.items():
            tree = self.new_candidate("mention-mask-" + label)
            (tree / "docs" / "skills-catalog.md").write_text(text, encoding="utf-8")
            code, payload, out, err = self.run_check(tree)
            self.assertEqual(code, 1, label)
            self.assertIn("DISCOVERY_OMISSION_CATALOG", self.rules(payload), label)
        self.assertFalse(guard.mentions_skill("alpha-v2", "alpha"))
        self.assertTrue(guard.mentions_skill("skills/alpha/SKILL.md", "alpha"))
        self.assertFalse(guard.mentions_skill("my_alpha", "alpha"))
        self.assertFalse(guard.mentions_skill("alpha.md", "alpha"))

    def test_p2f_shipped_baseline_mentions_match_current_matcher(self):
        repo = TESTS_DIR.parents[2]
        baseline = json.loads((repo / "tools" / "skill_preservation" / "baseline.json")
                              .read_text(encoding="utf-8"))
        catalog_text = (repo / "docs" / "skills-catalog.md").read_text(encoding="utf-8")
        readme_text = (repo / "README.md").read_text(encoding="utf-8")
        mismatches = []
        for skill, recorded in (baseline["discovery"]["catalog_mentions"] or {}).items():
            if guard.mentions_skill(catalog_text, skill) != recorded:
                mismatches.append(("catalog", skill))
        for skill, recorded in (baseline["discovery"]["readme_mentions"] or {}).items():
            if guard.mentions_skill(readme_text, skill) != recorded:
                mismatches.append(("readme", skill))
        self.assertEqual([], mismatches,
                         "baseline mention booleans differ from the current matcher; "
                         "a reviewed re-baseline is required")

    def test_p2f_missing_or_empty_name_blocks(self):
        cases = {
            "absent": lambda text: text.replace("name: alpha\n", "", 1),
            "empty": lambda text: text.replace("name: alpha", "name:", 1),
            "quoted-empty": lambda text: text.replace("name: alpha", "name: ''", 1),
        }
        for label, mutate in cases.items():
            tree = self.new_candidate("name-block-" + label)
            skill_md = tree / ".claude" / "skills" / "alpha" / "SKILL.md"
            write(skill_md, mutate(skill_md.read_text(encoding="utf-8")))
            code, payload, out, err = self.run_check(tree)
            self.assertEqual(code, 1, label + ": " + out)
            self.assertIn("NAME_MISSING", self.rules(payload), label)
        tree = self.new_candidate("name-and-description-block")
        skill_md = tree / ".claude" / "skills" / "alpha" / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8").replace("name: alpha\n", "", 1)
        text = text.replace("description: 'A synthetic test skill named alpha for guard self-tests.'",
                            "description: ''", 1)
        write(skill_md, text)
        code, payload, out, err = self.run_check(tree)
        self.assertEqual(code, 1, out)
        self.assertIn("NAME_MISSING", self.rules(payload))
        self.assertIn("EMPTY_DESCRIPTION", self.rules(payload))

    def test_p2e_candidate_discovery_read_error_is_exit2(self):
        tree = self.new_candidate("discovery-read-error")
        original = guard.read_text

        def fake(path):
            if str(path).replace("\\", "/").endswith("docs/skills-catalog.md"):
                raise OSError("simulated unreadable discovery surface")
            return original(path)

        with mock.patch.object(guard, "read_text", side_effect=fake):
            code, payload, out, err = self.run_check(tree)
        self.assertEqual(code, 2)

    def test_c02d_malformed_baseline_section_fails_closed(self):
        tail = self.new_candidate("malformed-baseline")
        bad = dict(self.baseline)
        bad["discovery"] = None
        bad["baseline_id"] = guard.compute_baseline_id(bad)
        bad_path = Path(self.tmp.name) / "malformed-baseline.json"
        guard.atomic_write_bytes(str(bad_path), guard.dump_json(bad).encode("utf-8"))
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = guard.main(["check", "--tree", str(tail), "--baseline", str(bad_path), "--json"])
        self.assertEqual(code, 2)

    def test_c03_renamed_skill_blocks(self):
        tree = self.new_candidate("renamed")
        os.rename(str(tree / ".claude" / "skills" / "alpha"),
                  str(tree / ".claude" / "skills" / "gamma"))
        code, payload, out, err = self.run_check(tree)
        self.assertEqual(code, 1)
        self.assertIn("RENAMED_OR_HIDDEN_SKILL", self.rules(payload))

    def test_c04_skill_md_content_change_not_blocked(self):
        tree = self.new_candidate("typo")
        skill_md = tree / ".claude" / "skills" / "alpha" / "SKILL.md"
        skill_md.write_text(skill_md.read_text(encoding="utf-8") + "\nA typo fix.\n",
                            encoding="utf-8", newline="\n")
        code, payload, out, err = self.run_check(tree)
        self.assertEqual(code, 0)
        self.assertIn("SKILL_MD_CHANGED", self.rules(payload))
        self.assertEqual(payload["summary"]["BLOCK"], 0)

    def test_c05_missing_reference_blocks(self):
        tree = self.new_candidate("ref")
        (tree / ".claude" / "skills" / "alpha" / "references" / "notes.md").unlink()
        code, payload, out, err = self.run_check(tree)
        self.assertEqual(code, 1)
        self.assertIn("MISSING_SUPPORTING_FILE", self.rules(payload))

    def test_c06_missing_evals_blocks(self):
        tree = self.new_candidate("evals")
        (tree / ".claude" / "skills" / "beta" / "evals" / "evals.json").unlink()
        code, payload, out, err = self.run_check(tree)
        self.assertEqual(code, 1)
        self.assertIn("MISSING_SUPPORTING_FILE", self.rules(payload))

    def test_c07_catalog_omission_blocks(self):
        tree = self.new_candidate("catalog")
        (tree / "docs" / "skills-catalog.md").write_text("# Catalog\n\n- beta\n", encoding="utf-8")
        code, payload, out, err = self.run_check(tree)
        self.assertEqual(code, 1)
        self.assertIn("DISCOVERY_OMISSION_CATALOG", self.rules(payload))

    def test_c08_readme_omission_blocks(self):
        tree = self.new_candidate("readme")
        (tree / "README.md").write_text("# Fixture\n\nSkills: beta.\n", encoding="utf-8")
        code, payload, out, err = self.run_check(tree)
        self.assertEqual(code, 1)
        self.assertIn("DISCOVERY_OMISSION_README", self.rules(payload))

    def test_c09_manifest_entry_dropped_blocks(self):
        tree = self.new_candidate("manifest")
        path = tree / "tools" / "skills-manifest.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["skills"] = [entry for entry in payload["skills"] if entry["name"] != "alpha"]
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n")
        code, report, out, err = self.run_check(tree)
        self.assertEqual(code, 1)
        self.assertIn("DISCOVERY_OMISSION_MANIFEST", self.rules(report))

    def test_c10_manifest_hash_input_changed_blocks(self):
        tree = self.new_candidate("hashinput")
        path = tree / "tools" / "skills-manifest.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["hash_input"] = "different semantics"
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n")
        code, report, out, err = self.run_check(tree)
        self.assertEqual(code, 1)
        self.assertIn("DISCOVERY_SEMANTICS_CHANGED", self.rules(report))

    def test_c11_silent_disable_field_blocks(self):
        tree = self.new_candidate("disable-field")
        skill_md = tree / ".claude" / "skills" / "alpha" / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8").replace(
            "description:", "disable-model-invocation: true\ndescription:", 1)
        skill_md.write_text(text, encoding="utf-8", newline="\n")
        code, report, out, err = self.run_check(tree)
        self.assertEqual(code, 1)
        self.assertIn("SILENT_DISABLE", self.rules(report))

    def test_c12_silent_disable_sentinel_blocks(self):
        tree = self.new_candidate("disable-sentinel")
        skill_md = tree / ".claude" / "skills" / "beta" / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8").replace(
            "description: 'A synthetic", "description: 'MANUAL-ONLY; never auto-invoke. A synthetic", 1)
        skill_md.write_text(text, encoding="utf-8", newline="\n")
        code, report, out, err = self.run_check(tree)
        self.assertEqual(code, 1)
        self.assertIn("SILENT_DISABLE", self.rules(report))

    def test_c13_empty_description_and_name_mismatch_block(self):
        tree = self.new_candidate("fm-empty")
        skill_md = tree / ".claude" / "skills" / "alpha" / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8").replace(
            "description: 'A synthetic test skill named alpha for guard self-tests.'",
            "description: ''", 1)
        skill_md.write_text(text, encoding="utf-8", newline="\n")
        code, report, out, err = self.run_check(tree)
        self.assertEqual(code, 1)
        self.assertIn("EMPTY_DESCRIPTION", self.rules(report))

        tree = self.new_candidate("fm-name")
        skill_md = tree / ".claude" / "skills" / "beta" / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8").replace("name: beta", "name: gamma", 1)
        skill_md.write_text(text, encoding="utf-8", newline="\n")
        code, report, out, err = self.run_check(tree)
        self.assertEqual(code, 1)
        self.assertIn("NAME_DIRECTORY_MISMATCH", self.rules(report))

    def test_c14_declared_installed_set_reduction_blocks(self):
        tree = self.new_candidate("installed-set")
        (tree / ".claude" / "skills" / "beta" / "SKILL.md").unlink()
        code, report, out, err = self.run_check(tree)
        self.assertEqual(code, 1)
        self.assertIn("INSTALLED_SET_REDUCTION", self.rules(report))
        self.assertIn("MISSING_SUPPORTING_FILE", self.rules(report))

    def test_c15_consumer_install_record_unrun(self):
        code, report, out, err = self.run_check(self.new_candidate("consumer"))
        self.assertEqual(code, 0)
        self.assertTrue(report["unrun"])
        self.assertIn("consumer install record", json.dumps(report["unrun"]))
        self.assertNotIn('"result": "PASS"', out)
        self.assertEqual(report["summary"]["result"], "CLEAN")

    def test_c16_cleanup_path_additions(self):
        tree = self.new_candidate("cleanup-warn")
        write(tree / "tools" / "cleanup-helper" / "run.py", "# helper\n")
        code, report, out, err = self.run_check(tree)
        self.assertEqual(code, 0)
        self.assertIn("CLEANUP_PATH_ADDITION", self.rules(report))
        severities = [item["severity"] for item in report["findings"]
                      if item["rule"] == "CLEANUP_PATH_ADDITION"]
        self.assertEqual(severities, ["WARN"])

        tree = self.new_candidate("cleanup-block-skill")
        write(tree / ".claude" / "skills" / "alpha" / "extra.md", "extra\n")
        code, report, out, err = self.run_check(tree)
        self.assertEqual(code, 1)
        self.assertIn("ADDED_PATH_IN_SKILL_SURFACE", self.rules(report))

        tree = self.new_candidate("cleanup-block-guard")
        write(tree / "tools" / "skill_preservation" / "prune_skills.py", "# forbidden\n")
        code, report, out, err = self.run_check(tree)
        self.assertEqual(code, 1)
        self.assertIn("CLEANUP_PATH_ADDITION", self.rules(report))
        severities = [item["severity"] for item in report["findings"]
                      if item["rule"] == "CLEANUP_PATH_ADDITION"]
        self.assertEqual(severities, ["BLOCK"])

    def test_c16b2_new_skill_with_removal_verb_is_allowed(self):
        tree = self.new_candidate("cleanup-helper")
        write(tree / ".claude" / "skills" / "cleanup-helper" / "SKILL.md",
              SKILL_MD_TEMPLATE.format(name="cleanup-helper"))
        code, payload, out, err = self.run_check(tree)
        self.assertEqual(code, 0, out)
        self.assertNotIn("CLEANUP_PATH_ADDITION", self.rules(payload))

    def test_c16b3_candidate_starter_unparsable_blocks(self):
        tree = self.new_candidate("starter-unparsable")
        write(tree / "docs" / "consumer-starter-package.md", "# no table here" + chr(10))
        code, payload, out, err = self.run_check(tree)
        self.assertEqual(code, 1, out)
        self.assertIn("INSTALLED_SET_UNVERIFIABLE", self.rules(payload))

    def test_c16b4_yaml_boolean_synonyms_block(self):
        for token in ("yes", "on", "1"):
            tree = self.new_candidate("dmi-" + token)
            skill_md = tree / ".claude" / "skills" / "alpha" / "SKILL.md"
            text = skill_md.read_text(encoding="utf-8").replace(
                "name: alpha", "name: alpha\ndisable-model-invocation: " + token, 1)
            write(skill_md, text)
            code, payload, out, err = self.run_check(tree)
            self.assertEqual(code, 1, token + ": " + out)
            self.assertIn("SILENT_DISABLE", self.rules(payload), token)

    def test_c16b_new_skill_addition_is_not_blocked(self):
        tree = self.new_candidate("new-skill")
        write(tree / ".claude" / "skills" / "gamma" / "SKILL.md",
              SKILL_MD_TEMPLATE.format(name="gamma"))
        code, report, out, err = self.run_check(tree)
        self.assertEqual(code, 0)
        rules = self.rules(report)
        self.assertIn("ADDED_SKILL", rules)
        self.assertNotIn("ADDED_PATH_IN_SKILL_SURFACE", rules)

    def test_c16c_json_quiet_output_is_pure_json(self):
        tree = self.new_candidate("json-quiet")
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = guard.main(["check", "--tree", str(tree),
                               "--baseline", str(self.baseline_path), "--json", "--quiet"])
        self.assertEqual(code, 0)
        json.loads(out.getvalue())

    def test_c16d_report_cannot_overwrite_baseline(self):
        tree = self.new_candidate("report-overwrite")
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = guard.main(["check", "--tree", str(tree),
                               "--baseline", str(self.baseline_path),
                               "--report", str(self.baseline_path), "--json"])
        self.assertEqual(code, 2)

    def test_c17_missing_baseline_fails_closed(self):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = guard.main(["check", "--tree", str(self.base_root),
                               "--baseline", str(Path(self.tmp.name) / "absent.json"), "--json"])
        self.assertEqual(code, 2)

    def test_c18_malformed_baseline_fails_closed(self):
        bad = Path(self.tmp.name) / "bad.json"
        bad.write_text("{not json", encoding="utf-8")
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            code = guard.main(["check", "--tree", str(self.base_root), "--baseline", str(bad)])
        self.assertEqual(code, 2)

        unknown = dict(self.baseline)
        unknown["schema"] = "unknown/9"
        unknown_path = Path(self.tmp.name) / "unknown.json"
        unknown_path.write_text(guard.dump_json(unknown), encoding="utf-8")
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            code = guard.main(["check", "--tree", str(self.base_root), "--baseline", str(unknown_path)])
        self.assertEqual(code, 2)

        tampered = dict(self.baseline)
        tampered["counts"] = dict(tampered["counts"])
        tampered["counts"]["named_skills"] = 999
        tampered_path = Path(self.tmp.name) / "tampered.json"
        tampered_path.write_text(guard.dump_json(tampered), encoding="utf-8")
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            code = guard.main(["check", "--tree", str(self.base_root), "--baseline", str(tampered_path)])
        self.assertEqual(code, 2)

    def test_c19_empty_tree_fails_closed(self):
        empty = Path(self.tmp.name) / "empty-tree"
        empty.mkdir()
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            code = guard.main(["check", "--tree", str(empty),
                               "--baseline", str(self.baseline_path), "--json"])
        self.assertEqual(code, 2)

    def test_c20_check_is_read_only(self):
        tree = self.new_candidate("readonly")
        before = {rel: sha256_bytes((tree / rel).read_bytes())
                  for rel in guard.iter_repo_files(str(tree))}
        self.run_check(tree)
        after = {rel: sha256_bytes((tree / rel).read_bytes())
                 for rel in guard.iter_repo_files(str(tree))}
        self.assertEqual(before, after)

    def test_c21_report_inside_tree_refused(self):
        tree = self.new_candidate("report-inside")
        report = tree / "report.json"
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            code = guard.main(["check", "--tree", str(tree), "--baseline",
                               str(self.baseline_path), "--report", str(report)])
        self.assertEqual(code, 2)
        self.assertFalse(report.exists())

    def test_c22_deterministic_json(self):
        tree = self.new_candidate("determinism")
        first = self.run_check(tree)[2]
        second = self.run_check(tree)[2]
        self.assertEqual(first, second)
        self.assertTrue(first)
        self.assertTrue(all(ord(ch) < 128 for ch in first))
        self.assertIn("summary", first)

    def test_c23_baseline_case_collision_rejected(self):
        tampered = json.loads(guard.dump_json(self.baseline))
        tampered["skills"]["Alpha"] = tampered["skills"]["alpha"]
        tampered["baseline_id"] = guard.compute_baseline_id(tampered)
        bad_path = Path(self.tmp.name) / "collision.json"
        bad_path.write_text(guard.dump_json(tampered), encoding="utf-8")
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            code = guard.main(["check", "--tree", str(self.base_root), "--baseline", str(bad_path)])
        self.assertEqual(code, 2)

    def test_p2d_candidate_discovery_surface_symlink_refused(self):
        for label, rel in (("catalog", "docs/skills-catalog.md"), ("readme", "README.md")):
            tree = self.new_candidate("discovery-symlink-" + label)
            external = Path(self.tmp.name) / ("external-" + label + ".md")
            external.write_text("# External\n\n- alpha\n- beta\n", encoding="utf-8")
            surface = tree / rel
            surface.unlink()
            created = False
            try:
                os.symlink(str(external), str(surface))
                created = True
            except (OSError, NotImplementedError):
                pass
            if created:
                code, payload, out, err = self.run_check(tree)
            else:
                # Host-limited reparse creation: exercise the same fail-closed code path
                # with a path-scoped patch of the reparse detector (documented UNRUN host
                # limitation for real symlink creation).
                surface_abs = os.path.normcase(os.path.realpath(str(surface)))
                original = guard.is_reparse_point

                def fake(path):
                    return (os.path.normcase(os.path.realpath(str(path))) == surface_abs
                            or original(path))

                with mock.patch.object(guard, "is_reparse_point", side_effect=fake):
                    code, payload, out, err = self.run_check(tree)
            self.assertEqual(code, 2, label)

    def test_p2d_baseline_skills_root_symlink_refused(self):
        tree = self.new_candidate("skills-root-symlink")
        external = Path(self.tmp.name) / "external-skills"
        shutil.copytree(str(tree / ".claude" / "skills"), str(external))
        skills_dir = tree / ".claude" / "skills"
        backup = tree / ".claude" / "skills-backup"
        skills_dir.rename(backup)
        created = False
        try:
            os.symlink(str(external), str(skills_dir), target_is_directory=True)
            created = True
        except (OSError, NotImplementedError):
            backup.rename(skills_dir)
        if created:
            code, out = self.run_baseline_cli(tree, "skills-root-symlink.json")
        else:
            skills_abs = os.path.normcase(os.path.realpath(str(tree / ".claude" / "skills")))
            original = guard.is_reparse_point

            def fake(path):
                return (os.path.normcase(os.path.realpath(str(path))) == skills_abs
                        or original(path))

            with mock.patch.object(guard, "is_reparse_point", side_effect=fake):
                code, out = self.run_baseline_cli(tree, "skills-root-symlink.json")
        self.assertEqual(code, 2)
        self.assertFalse(out.exists())

    def test_c24_symlink_refused(self):
        link = Path(self.tmp.name) / "link-tree"
        try:
            os.symlink(str(self.base_root), str(link), target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("host cannot create symlinks without privileges")
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            code = guard.main(["check", "--tree", str(link), "--baseline", str(self.baseline_path)])
        self.assertEqual(code, 2)

    def test_c25_static_hygiene(self):
        source = (TOOL_DIR / "check_skill_preservation.py").read_text(encoding="utf-8")
        allowed_imports = {"__future__", "argparse", "hashlib", "json", "os", "re", "sys", "tempfile"}
        imported = set()
        import re as re_module
        for line in source.splitlines():
            match = re_module.match(r"^(?:from\s+([A-Za-z0-9_.]+)\s+import|import\s+([A-Za-z0-9_., ]+))", line)
            if match:
                name = match.group(1) or match.group(2)
                for part in name.split(","):
                    imported.add(part.strip().split(".")[0])
        self.assertTrue(imported <= allowed_imports, "unexpected imports: %s" % (imported - allowed_imports))
        forbidden = ["import socket", "import ssl", "import http", "import urllib",
                     "import subprocess", "import ctypes", "import requests", "os.system",
                     "os.popen", "subprocess.", "socket.", "urlopen", "eval(", "exec("]
        for token in forbidden:
            self.assertNotIn(token, source, "forbidden token in tool source: %r" % token)

    def test_c26_stateless_repeatability(self):
        tree = self.new_candidate("repeat")
        first = guard.compare(self.baseline, str(tree))
        second = guard.compare(self.baseline, str(tree))
        self.assertEqual(guard.dump_json(first), guard.dump_json(second))

    def run_baseline_cli(self, tree, out_name):
        out = Path(self.tmp.name) / out_name
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            code = guard.main(["baseline", "--tree", str(tree), "--out", str(out)])
        return code, out

    def test_p2_baseline_required_surfaces_missing_fail_closed(self):
        for rel in ("tools/skills-manifest.json", "docs/skills-catalog.md",
                    "README.md", "docs/consumer-starter-package.md"):
            label = rel.replace("/", "-")
            tree = self.new_candidate("surface-" + label)
            (tree / rel).unlink()
            code, out = self.run_baseline_cli(tree, "surface-" + label + ".json")
            self.assertEqual(code, 2, rel)
            self.assertFalse(out.exists(), rel)

    def test_p2_baseline_malformed_manifest_fails_closed(self):
        tree = self.new_candidate("bad-manifest-baseline")
        (tree / "tools" / "skills-manifest.json").write_text("{not json", encoding="utf-8")
        code, out = self.run_baseline_cli(tree, "bad-manifest-baseline.json")
        self.assertEqual(code, 2)
        self.assertFalse(out.exists())

    def test_p2_starter_declared_traversal_path_refused(self):
        tree = self.new_candidate("starter-traversal")
        write(tree / "docs" / "consumer-starter-package.md",
              "| file | bytes | lines |" + chr(10) + "|---|---|---|" + chr(10)
              + "| .claude/skills/alpha/../../escape.txt | 10 | 1 |" + chr(10))
        code, out = self.run_baseline_cli(tree, "starter-traversal.json")
        self.assertEqual(code, 2)
        self.assertFalse(out.exists())

    def test_p2_starter_declared_traversal_path_refused_on_check(self):
        tree = self.new_candidate("starter-traversal-check")
        write(tree / "docs" / "consumer-starter-package.md",
              "| .claude/skills/alpha/../../escape.txt | 10 | 1 |" + chr(10))
        code, payload, out, err = self.run_check(tree)
        self.assertEqual(code, 2)
        self.assertIsNone(payload)

    def test_p2_unrecognized_disable_value_is_warn_not_block(self):
        tree = self.new_candidate("dmi-unknown")
        skill_md = tree / ".claude" / "skills" / "alpha" / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8").replace(
            "name: alpha", "name: alpha" + chr(10) + "disable-model-invocation: maybe", 1)
        write(skill_md, text)
        code, payload, out, err = self.run_check(tree)
        self.assertEqual(code, 0, out)
        self.assertNotIn("SILENT_DISABLE", self.rules(payload))
        warn = [item for item in payload["findings"]
                if item["rule"] == "FRONTMATTER_UNREADABLE_BY_GUARD"]
        self.assertEqual(1, len(warn))
        self.assertEqual("WARN", warn[0]["severity"])

    def test_p2_description_mentioning_setting_not_blocked(self):
        for label, replacement in (
            ("block-scalar",
             "description: >" + chr(10)
             + "  A synthetic test skill that documents disable-model-invocation: true in prose." + chr(10)
             + "  It does not set the key."),
            ("inline",
             "description: 'Notes about disable-model-invocation: true appear in this prose.'"),
        ):
            tree = self.new_candidate("desc-" + label)
            skill_md = tree / ".claude" / "skills" / "alpha" / "SKILL.md"
            text = skill_md.read_text(encoding="utf-8").replace(
                "description: 'A synthetic test skill named alpha for guard self-tests.'",
                replacement, 1)
            write(skill_md, text)
            code, payload, out, err = self.run_check(tree)
            self.assertEqual(code, 0, label + ": " + out)
            self.assertNotIn("SILENT_DISABLE", self.rules(payload), label)

    def test_p2_existing_skill_added_file_blocks_without_info_duplicate(self):
        tree = self.new_candidate("added-existing-skill")
        write(tree / ".claude" / "skills" / "alpha" / "extra.md", "extra" + chr(10))
        code, payload, out, err = self.run_check(tree)
        self.assertEqual(code, 1, out)
        self.assertIn("ADDED_PATH_IN_SKILL_SURFACE", self.rules(payload))
        self.assertNotIn("ADDED_SKILL_FILE", self.rules(payload))

    def tampered_baseline(self, label, mutate):
        bad = json.loads(guard.dump_json(self.baseline))
        mutate(bad)
        bad["baseline_id"] = guard.compute_baseline_id(bad)
        path = Path(self.tmp.name) / ("tampered-" + label + ".json")
        guard.atomic_write_bytes(str(path), guard.dump_json(bad).encode("utf-8"))
        return path

    def assert_baseline_refused(self, label, mutate):
        path = self.tampered_baseline(label, mutate)
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            code = guard.main(["check", "--tree", str(self.base_root),
                               "--baseline", str(path), "--json"])
        self.assertEqual(code, 2, label)

    def test_p2c_tampered_baseline_required_flags_fail_closed(self):
        cases = {
            "catalog-false": lambda bad: bad["discovery"].__setitem__("catalog_present", False),
            "readme-false": lambda bad: bad["discovery"].__setitem__("readme_present", False),
            "manifest-false": lambda bad: bad["discovery"]["manifest"].__setitem__("present", False),
            "manifest-empty": lambda bad: bad["discovery"]["manifest"].__setitem__("entries", {}),
            "starter-false": lambda bad: bad["starter"].__setitem__("present", False),
            "starter-unparsed": lambda bad: bad["starter"].__setitem__("parsed", False),
        }
        for label, mutate in cases.items():
            self.assert_baseline_refused(label, mutate)

    def test_p2c_tampered_baseline_starter_paths_fail_closed(self):
        cases = {
            "dotdot": lambda bad: bad["starter"].__setitem__("declared_paths", ["../escape.txt"]),
            "absolute": lambda bad: bad["starter"].__setitem__("declared_paths", ["C:/windows/win.ini"]),
            "backslash": lambda bad: bad["starter"].__setitem__("declared_paths", ["a\\b.txt"]),
            "dot-segment": lambda bad: bad["starter"].__setitem__(
                "declared_paths", [".claude/skills/alpha/./x.md"]),
            "dotdot-skill": lambda bad: bad["starter"].__setitem__(
                "declared_paths", [".claude/skills/alpha/../../x.md"]),
        }
        for label, mutate in cases.items():
            self.assert_baseline_refused(label, mutate)

    def test_baseline_out_inside_tree_refused(self):
        tree = self.new_candidate("baseline-out")
        target = tree / "baseline.json"
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            code = guard.main(["baseline", "--tree", str(tree), "--out", str(target)])
        self.assertEqual(code, 2)
        self.assertFalse(target.exists())

    def test_baseline_determinism_and_id(self):
        first = guard.build_baseline(str(self.base_root), source_revision="fixture-revision")
        second = guard.build_baseline(str(self.base_root), source_revision="fixture-revision")
        self.assertEqual(guard.dump_json(first), guard.dump_json(second))
        self.assertEqual(first["baseline_id"], guard.compute_baseline_id(first))
        self.assertEqual(first["counts"]["skill_directories"], 3)
        self.assertEqual(first["counts"]["named_skills"], 2)
        self.assertEqual(first["counts"]["manifest_entries"], 2)
        self.assertEqual(first["counts"]["starter_declared_files"], 2)


if __name__ == "__main__":
    unittest.main()

