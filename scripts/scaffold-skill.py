#!/usr/bin/env python3
"""Scaffold a validator-safe skill: SKILL.md plus both eval fixtures.

One JSON config generates exactly three files under
.claude/skills/<name>/:

  * SKILL.md
  * evals/evals.json
  * evals/trigger-evals.json

The config is validated before anything is written, unknown keys are
rejected, the name is checked against the skill validator's
RESERVED_BUNDLED_NAMES (imported with importlib; the validator has a
__main__ guard, so its main() is never run), and every overlaps_with entry
must resolve to .claude/skills/<overlap>/SKILL.md.

Dry run is the default: it prints the three files and the closure list and
writes nothing. --apply refuses an existing skill directory unless --force,
which overwrites only the three generated files.

The generator never edits docs/skills-catalog.md, README.md,
tools/skills-manifest.json or
artifacts/audits/skill-contract-audit-baseline.json: registration, README
counts, the manifest refresh and the audit baseline each keep their owning
tool. It runs no shell command, makes no network call, emits no timestamp,
and exits 2 with one line of error text on an invalid argument or config.
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z][a-z0-9-]{2,63}$")
DESCRIPTION_LIMIT = 1024
SKILLS_REL = Path(".claude") / "skills"

CONFIG_KEYS = (
    "name",
    "description",
    "purpose",
    "use_when",
    "inputs",
    "workflow",
    "output_format",
    "validation_checklist",
    "gotchas",
    "stop_conditions",
    "supporting_files",
    "positive_prompt",
    "negative_prompt",
    "overlaps_with",
    "trigger_note",
)
REQUIRED_KEYS = tuple(k for k in CONFIG_KEYS if k != "trigger_note")
LIST_KEYS = (
    "use_when",
    "inputs",
    "workflow",
    "output_format",
    "validation_checklist",
    "gotchas",
    "stop_conditions",
    "supporting_files",
    "overlaps_with",
)
EMPTY_LIST_ALLOWED = frozenset({"supporting_files"})

CLOSURES = (
    "Review the generated text and replace the placeholder assertions with "
    "checks specific to this skill.",
    "Add the docs/skills-catalog.md row and the README selected/coverage "
    "entry, and hand-bump the README family-roster count by one (do NOT run "
    "--write-readme-counts yet: it fails closed until the manifest matches "
    "disk).",
    "Commit the skill, then run python -P scripts/validate-skills.py "
    "--refresh-skills-manifest --manifest-ref=<content-commit> and commit the "
    "manifest. That refresh exits 1 because the README count is still stale, "
    "but it writes the manifest before that check; the failure is expected.",
    "Run python -P scripts/validate-skills.py --write-readme-counts and "
    "commit the result.",
    "Run python -P scripts/validate-skills.py, then python -P "
    "scripts/tests/test_audit_skill_contracts.py.",
    "Regenerate the baseline with python -P "
    "scripts/audit-skill-contracts.py --json "
    "artifacts/audits/skill-contract-audit-baseline.json and review the diff.",
)

USAGE = (
    "usage: scaffold-skill.py --config <config.json> [--repo-root <dir>] "
    "[--apply] [--force]"
)

_VALIDATOR = None


class ScaffoldError(Exception):
    """A one-line, user-facing refusal (exit 2)."""


def _one_line(text: object) -> str:
    return " ".join(str(text).split())


def _load_validator():
    """Load scripts/validate-skills.py without running its main()."""
    global _VALIDATOR
    if _VALIDATOR is not None:
        return _VALIDATOR
    path = Path(__file__).resolve().parent / "validate-skills.py"
    if not path.is_file():
        raise ScaffoldError(f"skill validator not found: {path}")
    spec = importlib.util.spec_from_file_location(
        "aegis_validate_skills", path)
    if spec is None or spec.loader is None:
        raise ScaffoldError(f"cannot load skill validator: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # __main__ guard: main() does not run
    _VALIDATOR = module
    return module


def _require_attr(module, name: str, kinds) -> object:
    """Return a validator constant, refusing to fail open if it moved."""
    try:
        value = getattr(module, name)
    except AttributeError:
        raise ScaffoldError(
            f"skill validator does not expose {name}; refusing to fail open"
        ) from None
    if not isinstance(value, kinds) or isinstance(value, bool):
        raise ScaffoldError(
            f"skill validator {name} has an unexpected type; refusing to "
            "fail open")
    return value


def _parse_args(argv):
    """Manual parser so every usage error stays one line and exits 2."""
    config = None
    repo_root = "."
    apply_files = False
    force = False
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg in ("-h", "--help"):
            print(USAGE)
            return None
        if arg == "--config" or arg.startswith("--config="):
            if arg == "--config":
                index += 1
                if index >= len(argv):
                    raise ScaffoldError("--config requires a path")
                config = argv[index]
            else:
                config = arg.split("=", 1)[1]
        elif arg == "--repo-root" or arg.startswith("--repo-root="):
            if arg == "--repo-root":
                index += 1
                if index >= len(argv):
                    raise ScaffoldError("--repo-root requires a directory")
                repo_root = argv[index]
            else:
                repo_root = arg.split("=", 1)[1]
        elif arg == "--apply":
            apply_files = True
        elif arg == "--force":
            force = True
        else:
            raise ScaffoldError(f"unknown argument: {arg}")
        index += 1
    if not config:
        raise ScaffoldError("--config is required")
    if force and not apply_files:
        raise ScaffoldError("--force requires --apply")
    if not repo_root:
        raise ScaffoldError("--repo-root must not be empty")
    return config, repo_root, apply_files, force


def _load_config(path: Path) -> dict:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ScaffoldError(
            f"config is not valid UTF-8: {_one_line(exc)}") from None
    except OSError as exc:
        raise ScaffoldError(
            f"cannot read config {path}: {_one_line(exc)}") from None
    try:
        data = json.loads(text)
    except ValueError as exc:
        raise ScaffoldError(
            f"config is not valid JSON: {_one_line(exc)}") from None
    if not isinstance(data, dict):
        raise ScaffoldError("config root must be a JSON object")

    unknown = sorted(set(data) - set(CONFIG_KEYS))
    if unknown:
        raise ScaffoldError(
            "unknown config key(s): " + ", ".join(unknown))
    missing = [key for key in REQUIRED_KEYS if key not in data]
    if missing:
        raise ScaffoldError(
            "missing required config key(s): " + ", ".join(missing))
    return data


def _require_text(config: dict, key: str) -> str:
    value = config[key]
    if not isinstance(value, str) or not value.strip():
        raise ScaffoldError(
            f"config key '{key}' must be a non-empty one-line string")
    if "\n" in value or "\r" in value:
        raise ScaffoldError(
            f"config key '{key}' must be a one-line string")
    return value


def _require_list(config: dict, key: str, *, allow_empty: bool) -> list:
    value = config[key]
    if not isinstance(value, list):
        raise ScaffoldError(f"config key '{key}' must be a list of strings")
    if not value and not allow_empty:
        raise ScaffoldError(f"config key '{key}' must be a non-empty list")
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ScaffoldError(
                f"config key '{key}' must contain only non-empty strings")
        if "\n" in item or "\r" in item:
            raise ScaffoldError(
                f"config key '{key}' items must each be one line")
    return value


def _validate_config(config: dict, repo_root: Path, validator) -> None:
    name = _require_text(config, "name")
    if not NAME_RE.fullmatch(name):
        raise ScaffoldError(
            "config key 'name' must match ^[a-z][a-z0-9-]{2,63}$")
    reserved = _require_attr(
        validator, "RESERVED_BUNDLED_NAMES", (set, frozenset))
    if name in reserved:
        raise ScaffoldError(
            f"name '{name}' is a reserved bundled skill name")

    description = _require_text(config, "description")
    if len(description) >= DESCRIPTION_LIMIT:
        raise ScaffoldError(
            f"config key 'description' is {len(description)} chars "
            f"(must be < {DESCRIPTION_LIMIT})")
    if description.startswith("MANUAL-ONLY"):
        raise ScaffoldError(
            "config key 'description' must not start with MANUAL-ONLY "
            "(scaffolded skills are auto-invocable)")
    if "---" in description:
        raise ScaffoldError(
            "config key 'description' must not contain '---' "
            "(it would end the YAML frontmatter early)")

    _require_text(config, "purpose")
    _require_text(config, "positive_prompt")
    _require_text(config, "negative_prompt")
    for key in LIST_KEYS:
        _require_list(config, key, allow_empty=key in EMPTY_LIST_ALLOWED)

    trigger_note = config.get("trigger_note")
    if trigger_note is not None:
        if not isinstance(trigger_note, str):
            raise ScaffoldError(
                "config key 'trigger_note' must be a string")
        if "\n" in trigger_note or "\r" in trigger_note:
            raise ScaffoldError(
                "config key 'trigger_note' must be a one-line string")

    overlaps = config["overlaps_with"]
    for overlap in overlaps:
        if not NAME_RE.fullmatch(overlap):
            raise ScaffoldError(
                f"overlap '{overlap}' must match the skill name pattern "
                "^[a-z][a-z0-9-]{2,63}$")
    if len(set(overlaps)) != len(overlaps):
        raise ScaffoldError(
            "config key 'overlaps_with' must not repeat a skill name")
    for overlap in overlaps:
        if overlap == name:
            raise ScaffoldError(
                "config key 'overlaps_with' must not name the new skill")
        if not overlap.strip() or "/" in overlap or "\\" in overlap \
                or overlap in (".", ".."):
            raise ScaffoldError(
                f"overlap '{overlap}' is not a directory name under "
                ".claude/skills/")
        skill_md = repo_root / SKILLS_REL / overlap / "SKILL.md"
        if not skill_md.is_file():
            raise ScaffoldError(
                f"overlap '{overlap}' has no "
                f"{SKILLS_REL.as_posix()}/{overlap}/SKILL.md")


def _bullets(items: list) -> list:
    return [f"- {item.strip()}" for item in items]


def _render_skill_md(config: dict) -> str:
    name = config["name"]
    description = config["description"].replace("'", "''")
    title = " ".join(
        part[:1].upper() + part[1:] for part in name.split("-"))
    lines = [
        "---",
        f"name: {name}",
        f"description: '{description}'",
        "---",
        "",
        f"# {title}",
        "",
        "## Purpose",
        "",
        config["purpose"].strip(),
        "",
        "## Use When",
        "",
    ]
    lines += _bullets(config["use_when"])
    lines += ["", "## Inputs to Inspect", ""]
    lines += _bullets(config["inputs"])
    lines += ["", "## Workflow", ""]
    lines += [f"{i}. {item.strip()}"
              for i, item in enumerate(config["workflow"], start=1)]
    lines += ["", "## Output Format", ""]
    lines += _bullets(config["output_format"])
    lines += ["", "## Validation Checklist", ""]
    lines += [f"- [ ] {item.strip()}"
              for item in config["validation_checklist"]]
    lines += ["", "## Gotchas", ""]
    lines += _bullets(config["gotchas"])
    lines += ["", "## Stop Conditions", ""]
    lines += _bullets(config["stop_conditions"])
    lines += ["", "## Supporting Files", ""]
    if config["supporting_files"]:
        lines += _bullets(config["supporting_files"])
    else:
        lines.append("- None yet.")
    return "\n".join(lines).rstrip("\n") + "\n"


def _assertions(config: dict) -> list:
    workflow = config["workflow"]
    assertions = [
        "Follows the Workflow section in order, beginning with: "
        + workflow[0].strip(),
    ]
    if len(workflow) > 1:
        assertions.append(
            "Completes the Workflow through its final step: "
            + workflow[-1].strip())
    assertions.append(
        "Runs the Validation Checklist before declaring done, beginning "
        "with: " + config["validation_checklist"][0].strip())
    return assertions


def _trigger_reason(config: dict) -> str:
    note = config.get("trigger_note")
    if isinstance(note, str) and note.strip():
        return note.strip()
    return (
        f"{config['name']} owns this request; the overlapping skills named "
        "in should_not_trigger cover adjacent work."
    )


def _first_sentence(text: str) -> str:
    cleaned = " ".join(text.split())
    match = re.match(r"(.+?[.!?])(?:\s|$)", cleaned)
    if match:
        return match.group(1)
    return cleaned.rstrip(".") + "."


def _render_evals(config: dict) -> str:
    name = config["name"]
    overlaps = list(config["overlaps_with"])
    payload = {
        "$schema": "https://json.schemastore.org/claude-skill-evals.json",
        "skill": name,
        "description": (
            f"Trigger and behavior cases for {name}: "
            f"{_first_sentence(config['purpose'])}"
        ),
        "cases": [
            {
                "id": "positive-1",
                "type": "should_trigger",
                "prompt": config["positive_prompt"],
                "expect": {
                    "triggers": True,
                    "assertions": _assertions(config),
                },
            },
            {
                "id": "negative-1",
                "type": "should_not_trigger",
                "prompt": config["negative_prompt"],
                "expect": {
                    "triggers": False,
                    "assertions": [
                        f"Does not invoke {name}; it names {overlaps[0]} as "
                        "the owning skill instead."
                    ],
                },
            },
        ],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def _render_trigger_evals(config: dict) -> str:
    name = config["name"]
    overlaps = list(config["overlaps_with"])
    payload = {
        "skill": name,
        "description": config["description"],
        "overlaps_with": overlaps,
        "cases": [
            {
                "id": "positive-1",
                "prompt": config["positive_prompt"],
                "expected_skill": name,
                "should_not_trigger": overlaps,
                "reason": _trigger_reason(config),
            },
            {
                "id": "negative-1",
                "prompt": config["negative_prompt"],
                "expected_skill": overlaps[0],
                "should_not_trigger": [name],
                "reason": (
                    f"{overlaps[0]} owns this request; {name} must not claim "
                    "it."
                ),
            },
        ],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def _validate_rendered(text: str, validator) -> None:
    patterns = _require_attr(
        validator, "SKILL_SHELL_INJECTION_RES", (tuple, list))
    for pattern in patterns:
        if pattern.search(text):
            raise ScaffoldError(
                "generated SKILL.md would contain a shell-injection "
                "pattern; remove it from the config")
    max_lines = _require_attr(validator, "MAX_SKILL_LINES", int)
    count = len(text.splitlines())
    if count >= max_lines:
        raise ScaffoldError(
            f"generated SKILL.md would be {count} lines (must be < "
            f"{max_lines})")


def _render_files(config: dict, validator) -> dict:
    skill_md = _render_skill_md(config)
    _validate_rendered(skill_md, validator)
    base = SKILLS_REL / config["name"]
    return {
        (base / "SKILL.md").as_posix(): skill_md,
        (base / "evals" / "evals.json").as_posix(): _render_evals(config),
        (base / "evals" / "trigger-evals.json").as_posix():
            _render_trigger_evals(config),
    }


def _write_files(skill_dir: Path, contents: dict) -> None:
    for rel, text in contents.items():
        target = skill_dir.joinpath(*rel.split("/")[3:])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8", newline="\n")


def _print_closures() -> None:
    print()
    print("Closures (the generator does not perform these):")
    for number, closure in enumerate(CLOSURES, start=1):
        print(f"{number}. {closure}")


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    try:
        parsed = _parse_args(argv)
        if parsed is None:
            return 0
        config_path, repo_root_arg, apply_files, force = parsed
        repo_root = Path(repo_root_arg).resolve()
        if not repo_root.is_dir():
            raise ScaffoldError(
                f"--repo-root is not a directory: {repo_root_arg}")
        config = _load_config(Path(config_path))
        validator = _load_validator()
        _validate_config(config, repo_root, validator)
        contents = _render_files(config, validator)

        skill_dir = repo_root / SKILLS_REL / config["name"]
        if apply_files:
            if skill_dir.exists() and not force:
                raise ScaffoldError(
                    f"skill directory already exists: "
                    f"{skill_dir.relative_to(repo_root).as_posix()} "
                    "(use --force to overwrite the three files)")
            _write_files(skill_dir, contents)
            for rel in contents:
                print(f"wrote {rel}")
        else:
            for rel, text in contents.items():
                print(f"=== {rel} ===")
                print(text, end="" if text.endswith("\n") else "\n")
        _print_closures()
        return 0
    except ScaffoldError as exc:
        print(f"ERROR: {_one_line(exc)}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"ERROR: {_one_line(exc)}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
